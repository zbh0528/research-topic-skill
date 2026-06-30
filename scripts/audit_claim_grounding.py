#!/usr/bin/env python3
"""Audit structured claim grounding without pretending to read papers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_OUTPUTS = [
    "01_domain_scan/output.json",
    "02_problem_identification/output.json",
    "03_theoretical_positioning/output.json",
    "04_contribution_argumentation/output.json",
    "05_chain_consistency_audit/output.json",
    "06_final_topic_package/output.json",
]
UNSAFE = re.compile(r"(?<!algorithm-)\bfirst\b|\bnovel\b|state-of-the-art|state of the art|\bSOTA\b|\bunprecedented\b", re.I)
ABSENCE = re.compile(r"\b(no one|nobody|no studies|not been studied|nobody has studied)\b", re.I)
SAFE_PATH_PARTS = {"unsafe_wording_to_avoid", "safer_wording", "novelty_risk", "overclaim_risk", "required_additional_literature"}


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def iter_items(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from iter_items(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_items(child, (*path, index))


def iter_strings(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_strings(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_strings(child, (*path, index))
    elif isinstance(value, str):
        yield path, value


def evidence_ids_from(item: dict) -> list[str]:
    ids = item.get("linked_evidence_ids") or item.get("supporting_evidence_ids") or item.get("evidence_ids") or item.get("evidence_id") or []
    if isinstance(ids, str):
        return [ids]
    return [str(eid) for eid in ids]


def has_evidence(item: dict) -> bool:
    return bool(evidence_ids_from(item))


def has_source(item: dict) -> bool:
    return bool(item.get("source_field") or item.get("source_excerpt") or has_evidence(item))


def claim_label(item: dict) -> str:
    for key in ("claim_id", "gap_id", "problem_id", "contribution_id", "risk_id", "evidence_id"):
        if item.get(key):
            return str(item[key])
    return "<unknown>"


def load_literature(workspace: Path) -> tuple[set[str], dict[str, str], set[str], list[str], list[dict]]:
    evidence_dir = workspace / "literature_evidence"
    synthetic_papers: set[str] = set()
    evidence_to_paper: dict[str, str] = {}
    valid_evidence_ids: set[str] = set()
    warnings: list[str] = []
    counterevidence: list[dict] = []
    records_path = evidence_dir / "bibliographic_records.json"
    if records_path.exists():
        records = load_json(records_path)
        for record in records.get("bibliographic_records", []) if isinstance(records, dict) else []:
            if record.get("is_synthetic"):
                synthetic_papers.add(record.get("paper_id"))
    claim_map_path = evidence_dir / "evidence_claim_map.json"
    if claim_map_path.exists():
        claim_map = load_json(claim_map_path)
        for obj in claim_map.get("evidence_objects", []) if isinstance(claim_map, dict) else []:
            if obj.get("evidence_id") and obj.get("paper_id"):
                evidence_to_paper[obj["evidence_id"]] = obj["paper_id"]
                valid_evidence_ids.add(obj["evidence_id"])
    gap_path = evidence_dir / "literature_gap_audit.json"
    if gap_path.exists():
        gap_audit = load_json(gap_path)
        if isinstance(gap_audit, dict):
            counterevidence = gap_audit.get("counterevidence_summary", [])
    else:
        warnings.append("WARNING literature_gap_audit.json missing")
    return synthetic_papers, evidence_to_paper, valid_evidence_ids, warnings, counterevidence


def audit_output(data: dict, strict: bool, synthetic_papers: set[str], evidence_to_paper: dict[str, str], valid_evidence_ids: set[str]) -> tuple[list[str], list[str], list[str]]:
    passes: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []
    module_id = data.get("module_id", "<unknown>")
    if data.get("status") == "draft" and "PENDING_MODULE_OUTPUT" in json.dumps(data):
        warnings.append(f"WARNING skipped draft module: {module_id}")
        return passes, warnings, failures

    for path, item in iter_items(data):
        if item.get("evidence_status") == "verified" and not has_source(item):
            failures.append(f"FAIL unsupported verified claim in {module_id}: {claim_label(item)}")
        if item.get("grounding_status") == "grounded" and not has_evidence(item):
            failures.append(f"FAIL grounded claim without evidence_id in {module_id}: {claim_label(item)}")
        if item.get("grounding_status") == "grounded":
            missing = [eid for eid in evidence_ids_from(item) if eid not in valid_evidence_ids]
            if missing:
                failures.append(f"FAIL grounded claim links unknown evidence_id in {module_id}: {', '.join(missing)}")
        if item.get("claim_scope") == "field_general" and (not has_evidence(item) or item.get("support_strength") != "direct"):
            failures.append(f"FAIL field-general claim without evidence in {module_id}: {claim_label(item)}")
        if item.get("claim_type") == "gap_claim" or item.get("gap_id"):
            if not item.get("corpus_scope"):
                failures.append(f"FAIL gap claim without corpus_scope in {module_id}: {claim_label(item)}")
        if item.get("claim_type") == "contribution_claim" or item.get("contribution_id"):
            if strict and not has_evidence(item):
                failures.append(f"FAIL contribution_claim without linked evidence in {module_id}: {claim_label(item)}")
        if strict and item.get("problem_id") and "selected_problem" in {str(p) for p in path} and not has_evidence(item):
            failures.append(f"FAIL selected_problem without evidence link in {module_id}: {claim_label(item)}")
        if item.get("evidence_status") == "verified":
            paper_ids = set(item.get("linked_paper_ids", []) or [item.get("paper_id")])
            evidence_ids = set(evidence_ids_from(item))
            missing = evidence_ids - valid_evidence_ids
            if missing:
                failures.append(f"FAIL verified claim links unknown evidence_id in {module_id}: {', '.join(sorted(missing))}")
            paper_ids.update(evidence_to_paper.get(eid) for eid in evidence_ids if evidence_to_paper.get(eid))
            if paper_ids & synthetic_papers:
                failures.append(f"FAIL synthetic evidence used as verified in {module_id}: {claim_label(item)}")

    for path, text in iter_strings(data):
        if any(part in SAFE_PATH_PARTS for part in path):
            continue
        if UNSAFE.search(text):
            failures.append(f"FAIL unsafe novelty wording in {module_id}: {'.'.join(map(str, path))}: {text}")
        if ABSENCE.search(text) and "within the provided corpus" not in text and "current corpus" not in text:
            failures.append(f"FAIL absence-of-evidence wording risk in {module_id}: {'.'.join(map(str, path))}: {text}")

    passes.append(f"PASS audited module: {module_id}")
    return passes, warnings, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    if not workspace.exists():
        raise SystemExit(f"FAIL workspace not found: {workspace}")
    synthetic_papers, evidence_to_paper, valid_evidence_ids, lit_warnings, counterevidence = load_literature(workspace)
    passes: list[str] = []
    warnings: list[str] = lit_warnings
    failures: list[str] = []

    final_output: dict | None = None
    for rel in MODULE_OUTPUTS:
        path = workspace / rel
        if not path.exists():
            warnings.append(f"WARNING missing module output: {rel}")
            continue
        data = load_json(path)
        if not isinstance(data, dict):
            failures.append(f"FAIL module output is not an object: {rel}")
            continue
        if rel.startswith("06_"):
            final_output = data
        p, w, f = audit_output(data, args.strict, synthetic_papers, evidence_to_paper, valid_evidence_ids)
        passes.extend(p)
        warnings.extend(w)
        failures.extend(f)

    cards_path = workspace / "literature_evidence" / "paper_cards.json"
    if cards_path.exists():
        cards = load_json(cards_path)
        for _, item in iter_items(cards):
            if item.get("source_field") in {"title", "title_keywords", "paper_title"} and item.get("claim_type") != "bibliographic_fact":
                failures.append(f"FAIL title-only inference risk: {claim_label(item)}")

    if counterevidence and final_output and final_output.get("status") != "draft":
        final_text = json.dumps(final_output, ensure_ascii=False).lower()
        if "counterevidence" not in final_text and "contradict" not in final_text:
            failures.append("FAIL hidden counterevidence risk in final topic package")
        missing_counter_ids: list[str] = []
        for item in counterevidence:
            if not isinstance(item, dict):
                continue
            for evidence_id in item.get("contradicting_evidence_ids", []):
                if str(evidence_id).lower() not in final_text:
                    missing_counter_ids.append(str(evidence_id))
        if missing_counter_ids:
            failures.append(f"FAIL hidden counterevidence ids in final topic package: {', '.join(sorted(set(missing_counter_ids)))}")

    decision = "fail_requires_revision" if failures else ("pass_with_warnings" if warnings else "pass")
    result = {
        "pass_count": len(passes),
        "warning_count": len(warnings),
        "fail_count": len(failures),
        "audit_decision": decision,
        "passes": passes,
        "warnings": warnings,
        "failures": failures,
    }
    write_json(workspace / "claim_grounding_audit.json", result)
    lines = [
        "# Claim Grounding Audit",
        "",
        f"- pass_count: {len(passes)}",
        f"- warning_count: {len(warnings)}",
        f"- fail_count: {len(failures)}",
        f"- audit_decision: {decision}",
        "",
        "## PASS",
        *[f"- {line}" for line in passes],
        "",
        "## WARNING",
        *[f"- {line}" for line in warnings],
        "",
        "## FAIL",
        *[f"- {line}" for line in failures],
    ]
    (workspace / "claim_grounding_audit.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
