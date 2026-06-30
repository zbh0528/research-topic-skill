#!/usr/bin/env python3
"""Validate workspace output files and module contracts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ["input.json", "output.json", "output.md", "next_input.json", "validation_report.md"]
GLOBAL_FIELDS = [
    "status",
    "module_id",
    "module_name",
    "input_summary",
    "structured_output",
    "next_input",
    "assumptions",
    "uncertainty_log",
    "evidence_requirements",
    "reviewer_risks",
    "revision_hooks",
    "trace_context",
]
LEAKED_OUTPUT_FIELDS = {
    "status",
    "module_id",
    "module_name",
    "input_summary",
    "structured_output",
    "assumptions",
    "uncertainty_log",
    "evidence_requirements",
    "revision_hooks",
}
UNSAFE_CLAIM_PATTERNS = [
    re.compile(r"(?<!algorithm-)\bfirst\b", re.IGNORECASE),
    re.compile(r"\bnovel\b", re.IGNORECASE),
    re.compile(r"state-of-the-art", re.IGNORECASE),
    re.compile(r"state of the art", re.IGNORECASE),
    re.compile(r"\bSOTA\b", re.IGNORECASE),
    re.compile(r"\bunprecedented\b", re.IGNORECASE),
    re.compile(r"outperforms all", re.IGNORECASE),
    re.compile(r"the first framework", re.IGNORECASE),
]
UNSAFE_ALLOWED_PATH_PARTS = {
    "unsafe_claims_removed",
    "unsafe_wording_to_avoid",
    "safer_wording_map",
    "overclaim_risks",
    "reviewer_risks",
    "reviewer_risk_and_defense",
    "uncertainty_log",
    "evidence_requirements",
    "revision_hooks",
    "novelty_risk",
    "known_constraints",
    "constraints",
    "exclusion_boundary",
    "required_repairs",
    "repair_actions",
    "novelty_safety_level",
    "counterevidence",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_manifest() -> dict:
    return json.loads((ROOT / "skill_manifest.json").read_text())


def load_json(path: Path, failures: list[str]) -> object:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        failures.append(f"FAIL invalid JSON: {path}: {exc}")
        return {}


def try_jsonschema():
    try:
        from jsonschema import Draft202012Validator  # type: ignore

        return Draft202012Validator, None
    except ImportError:
        return None, "WARNING jsonschema not installed; ran basic checks only"


def write_module_report(module_dir: Path, lines: list[str]) -> None:
    (module_dir / "validation_report.md").write_text("# Validation Report\n\n" + "\n".join(f"- {line}" for line in lines) + "\n")


def is_allowed_unsafe_path(path: tuple[object, ...]) -> bool:
    return any(str(part) in UNSAFE_ALLOWED_PATH_PARTS for part in path)


def find_unsafe_claims(value: object, path: tuple[object, ...] = ()) -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            findings.extend(find_unsafe_claims(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_unsafe_claims(child, (*path, index)))
    elif isinstance(value, str) and not is_allowed_unsafe_path(path):
        for pattern in UNSAFE_CLAIM_PATTERNS:
            if pattern.search(value):
                findings.append(f"{'.'.join(map(str, path))}: {value}")
                break
    return findings


def iter_dicts(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def has_evidence_link(item: dict) -> bool:
    return bool(item.get("linked_evidence_ids") or item.get("supporting_evidence_ids") or item.get("evidence_ids") or item.get("evidence_id"))


def has_source_evidence(item: dict) -> bool:
    return bool(item.get("source_field") or item.get("source_excerpt") or has_evidence_link(item))


def contains_evidence_context(value: object) -> bool:
    if isinstance(value, dict):
        if "evidence_context" in value:
            return True
        return any(contains_evidence_context(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_evidence_context(child) for child in value)
    return False


def find_forbidden_next_input_fields(value: object, path: tuple[object, ...] = ()) -> list[str]:
    forbidden = {"source_excerpt", "abstract", "full_text", "relevant_excerpts", "paraphrase"}
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden:
                findings.append(".".join(map(str, (*path, key))))
            findings.extend(find_forbidden_next_input_fields(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_forbidden_next_input_fields(child, (*path, index)))
    return findings


def load_synthetic_papers(literature_dir: Path) -> set[str]:
    records_path = literature_dir / "bibliographic_records.json"
    if not records_path.exists():
        return set()
    records = json.loads(records_path.read_text())
    if not isinstance(records, dict):
        return set()
    return {
        record.get("paper_id")
        for record in records.get("bibliographic_records", [])
        if isinstance(record, dict) and record.get("is_synthetic")
    }


def load_evidence_index(literature_dir: Path) -> dict[str, dict]:
    path = literature_dir / "evidence_claim_map.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        return {}
    return {
        obj.get("evidence_id"): obj
        for obj in data.get("evidence_objects", [])
        if isinstance(obj, dict) and obj.get("evidence_id")
    }


def evidence_ids_from(item: dict) -> list[str]:
    ids = item.get("linked_evidence_ids") or item.get("supporting_evidence_ids") or item.get("evidence_ids") or item.get("evidence_id") or []
    if isinstance(ids, str):
        return [ids]
    return [str(eid) for eid in ids]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict-evidence", action="store_true")
    parser.add_argument("--literature-grounded", action="store_true")
    parser.add_argument("--literature-dir", type=Path)
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    literature_dir = args.literature_dir or workspace / "literature_evidence"
    if args.literature_dir and not args.literature_dir.is_absolute():
        literature_dir = workspace / args.literature_dir
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    if not workspace.exists():
        raise SystemExit(f"FAIL workspace not found: {workspace}")

    state_path = workspace / "project_state.json"
    if not state_path.exists():
        failures.append(f"FAIL missing project_state.json: {state_path}")
        state = {}
    else:
        state = load_json(state_path, failures)
        passes.append("PASS project_state.json exists")

    modules = load_manifest()["modules"]
    module_order = [m["workspace_id"] for m in modules]
    completed = state.get("completed_modules", []) if isinstance(state, dict) else []
    if completed and completed != module_order[: len(completed)]:
        failures.append("FAIL completed_modules must be a prefix of module_order")

    Validator, schema_warning = try_jsonschema()
    if schema_warning:
        warnings.append(schema_warning)

    synthetic_papers = load_synthetic_papers(literature_dir) if args.literature_grounded else set()
    evidence_index = load_evidence_index(literature_dir) if args.literature_grounded else {}
    saw_evidence_context = False

    for index, module in enumerate(modules):
        module_id = module["workspace_id"]
        module_dir = workspace / module_id
        module_lines: list[str] = []
        if not module_dir.exists():
            failures.append(f"FAIL missing module directory: {module_dir}")
            continue
        passes.append(f"PASS module directory exists: {module_id}")
        module_lines.append("PASS module directory exists")

        for filename in REQUIRED_FILES:
            path = module_dir / filename
            if not path.exists():
                failures.append(f"FAIL missing file: {path}")
                module_lines.append(f"FAIL missing file: {filename}")
            else:
                passes.append(f"PASS file exists: {module_id}/{filename}")
                module_lines.append(f"PASS file exists: {filename}")

        output_path = module_dir / "output.json"
        next_path = module_dir / "next_input.json"
        input_path = module_dir / "input.json"
        if not output_path.exists() or not next_path.exists() or not input_path.exists():
            write_module_report(module_dir, module_lines)
            continue

        output = load_json(output_path, failures)
        next_input = load_json(next_path, failures)
        input_data = load_json(input_path, failures)

        if isinstance(output, dict):
            placeholder_draft = output.get("status") == "draft" and "PENDING_MODULE_OUTPUT" in json.dumps(output)
            if args.literature_grounded and not placeholder_draft:
                for item in iter_dicts(output):
                    if item.get("evidence_status") == "verified" and not has_source_evidence(item):
                        failures.append(f"FAIL unsupported verified claim in {output_path}: {item.get('claim_id') or item.get('evidence_id') or item.get('contribution_id')}")
                    if item.get("grounding_status") == "grounded" and not has_evidence_link(item):
                        failures.append(f"FAIL grounded claim lacks evidence link in {output_path}: {item.get('claim_id') or item.get('gap_id')}")
                    if item.get("grounding_status") == "grounded":
                        missing_ids = [eid for eid in evidence_ids_from(item) if eid not in evidence_index]
                        if missing_ids:
                            failures.append(f"FAIL grounded claim links unknown evidence_id in {output_path}: {', '.join(missing_ids)}")
                    if item.get("claim_type") == "gap_claim" and not item.get("corpus_scope"):
                        failures.append(f"FAIL gap claim lacks corpus_scope in {output_path}: {item.get('claim_id')}")
                    if item.get("claim_type") == "contribution_claim" and not item.get("claim_scope"):
                        failures.append(f"FAIL contribution_claim lacks claim_scope in {output_path}: {item.get('claim_id') or item.get('contribution_id')}")
                    if item.get("claim_scope") == "field_general" and item.get("support_strength") != "direct":
                        failures.append(f"FAIL field_general claim lacks direct evidence in {output_path}: {item.get('claim_id')}")
                    if item.get("evidence_status") == "verified":
                        linked_papers = set(item.get("linked_paper_ids", []) or [item.get("paper_id")])
                        for eid in evidence_ids_from(item):
                            if eid not in evidence_index:
                                failures.append(f"FAIL verified claim links unknown evidence_id in {output_path}: {eid}")
                            elif evidence_index[eid].get("paper_id"):
                                linked_papers.add(evidence_index[eid]["paper_id"])
                        if linked_papers & synthetic_papers:
                            failures.append(f"FAIL synthetic evidence used as verified evidence in {output_path}: {item.get('claim_id') or item.get('evidence_id')}")
                if module_id == "02_problem_identification":
                    selected = output.get("structured_output", {}).get("selected_problem", {})
                    if isinstance(selected, dict) and selected and not selected.get("corpus_scope"):
                        failures.append(f"FAIL selected_problem lacks corpus_scope in {output_path}")
                if module_id == "06_final_topic_package":
                    structured = output.get("structured_output", {})
                    if isinstance(structured, dict) and not (structured.get("evidence_traceability_table") or structured.get("Evidence Traceability Table")):
                        failures.append(f"FAIL final_topic_package lacks Evidence Traceability Table in {output_path}")
            missing = [field for field in GLOBAL_FIELDS if field not in output]
            if missing:
                failures.append(f"FAIL {output_path} missing global fields: {', '.join(missing)}")
                module_lines.append(f"FAIL missing global fields: {', '.join(missing)}")
            else:
                module_lines.append("PASS output.json global fields")
            if output.get("module_id") != module_id:
                failures.append(f"FAIL {output_path} module_id mismatch: {output.get('module_id')} != {module_id}")
            if output.get("status") == "draft":
                warnings.append(f"WARNING {module_id} output status is draft")
                module_lines.append("WARNING output status is draft")

            unsafe_claims = find_unsafe_claims(output)
            for finding in unsafe_claims:
                failures.append(f"FAIL unsafe strong claim in {output_path}: {finding}")
            if unsafe_claims:
                module_lines.append(f"FAIL unsafe strong claims: {len(unsafe_claims)}")

            if Validator:
                schema_path = ROOT / module["schema"]
                schema = json.loads(schema_path.read_text())
                errors = sorted(Validator(schema).iter_errors(output), key=lambda err: list(err.path))
                if errors:
                    for err in errors[:10]:
                        failures.append(f"FAIL schema {module_id}: {list(err.path)} {err.message}")
                    module_lines.append(f"FAIL schema validation errors: {len(errors)}")
                else:
                    module_lines.append("PASS schema validation")

        if isinstance(next_input, dict):
            forbidden_next_fields = find_forbidden_next_input_fields(next_input)
            if args.literature_grounded and args.strict_evidence and forbidden_next_fields:
                failures.append(f"FAIL next_input contains over-expanded evidence fields: {', '.join(forbidden_next_fields[:5])}")
            if args.literature_grounded and contains_evidence_context(next_input):
                saw_evidence_context = True
            if isinstance(output, dict) and "next_input" in output and next_input != output.get("next_input"):
                failures.append(f"FAIL {next_path} must match output.json next_input")
                module_lines.append("FAIL next_input.json differs from output.json next_input")
            leaked_global_fields = [field for field in LEAKED_OUTPUT_FIELDS if field in next_input]
            if leaked_global_fields:
                failures.append(f"FAIL {next_path} appears to contain full output fields: {', '.join(leaked_global_fields)}")
                module_lines.append("FAIL next_input.json contains full output fields")
            if not next_input and module_id != module_order[-1]:
                if isinstance(output, dict) and output.get("status") in {"complete", "validated"}:
                    failures.append(f"FAIL completed upstream module has empty next_input.json: {next_path}")
                else:
                    warnings.append(f"WARNING draft module has empty next_input.json: {next_path}")

        if index > 0 and isinstance(input_data, dict):
            if args.literature_grounded and contains_evidence_context(input_data):
                saw_evidence_context = True
            expected_upstream = module_order[index - 1]
            declared = input_data.get("source_module_id")
            if declared and declared != expected_upstream:
                failures.append(f"FAIL {input_path} source_module_id must be direct upstream {expected_upstream}, got {declared}")
            source_path = str(input_data.get("source_output_path", ""))
            if source_path.endswith("output.json"):
                failures.append(f"FAIL {input_path} must not depend on upstream output.json")

        write_module_report(module_dir, module_lines)

    if args.literature_grounded:
        if not literature_dir.exists():
            failures.append(f"FAIL literature_evidence directory missing: {literature_dir}")
        else:
            passes.append(f"PASS literature_evidence directory exists: {literature_dir}")
        if not saw_evidence_context:
            failures.append("FAIL literature-grounded mode requires evidence_context in module input or next_input")
        elif args.strict_evidence:
            passes.append("PASS evidence_context is present for strict evidence mode")

    summary_lines = [
        f"# Validation Summary",
        "",
        f"- workspace: `{workspace}`",
        f"- generated_at: `{now()}`",
        f"- pass_count: {len(passes)}",
        f"- warning_count: {len(warnings)}",
        f"- fail_count: {len(failures)}",
        "",
        "## PASS",
        *[f"- {line}" for line in passes],
        "",
        "## WARNING",
        *[f"- {line}" for line in warnings],
        "",
        "## FAIL",
        *[f"- {line}" for line in failures],
        "",
    ]
    summary = "\n".join(summary_lines)
    (workspace / "validation_summary.md").write_text(summary)
    print(summary)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
