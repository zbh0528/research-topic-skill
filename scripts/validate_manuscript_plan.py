#!/usr/bin/env python3
"""Validate v0.4 manuscript-grounded writing plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manuscript_grounding_common import evaluate_plan, load_plan, manuscript_dir, plan_file_map, report_lines, resolve_workspace


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_MAP = {
    "manuscript_blueprint": "manuscript_blueprint.schema.json",
    "section_argument_map": "section_argument_map.schema.json",
    "paragraph_claim_plan": "paragraph_claim_plan.schema.json",
    "citation_requirement_map": "citation_requirement_map.schema.json",
    "result_placeholder_map": "result_placeholder_map.schema.json",
    "method_section_alignment": "method_section_alignment.schema.json",
    "experiment_section_alignment": "experiment_section_alignment.schema.json",
    "discussion_limitations_plan": "discussion_limitations_plan.schema.json",
    "reviewer_objection_map": "reviewer_objection_map.schema.json",
    "reviewer_response_strategy": "reviewer_response_strategy.schema.json",
    "manuscript_grounding_report": "manuscript_grounding_report.schema.json",
}


def try_jsonschema():
    try:
        from jsonschema import Draft202012Validator  # type: ignore

        return Draft202012Validator, None
    except ImportError:
        return None, "WARNING jsonschema not installed; ran structural checks only"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--manuscript-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    ms_dir = manuscript_dir(workspace, args.manuscript_dir)
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []
    if not ms_dir.exists():
        failures.append(f"FAIL manuscript_grounding directory missing: {ms_dir}")
        plan = {}
    else:
        passes.append(f"PASS manuscript_grounding directory exists: {ms_dir}")
        plan = load_plan(ms_dir, failures)

    Validator, schema_warning = try_jsonschema()
    if schema_warning:
        warnings.append(schema_warning)
    if Validator:
        for key, schema_name in SCHEMA_MAP.items():
            if key not in plan:
                continue
            schema_path = ROOT / "schemas" / "manuscript_grounding" / schema_name
            if not schema_path.exists():
                failures.append(f"FAIL missing schema: {schema_path}")
                continue
            schema = json.loads(schema_path.read_text())
            errors = sorted(Validator(schema).iter_errors(plan[key]), key=lambda err: list(err.path))
            if errors:
                failures.extend(f"FAIL schema {schema_name}: {list(err.path)} {err.message}" for err in errors[:10])
            else:
                passes.append(f"PASS schema validation: {schema_name}")

    for key in sorted(set(plan_file_map()) - set(plan)):
        failures.append(f"FAIL missing required manuscript plan section: {key}")
    if plan:
        p, w, f = evaluate_plan(plan, strict=args.strict)
        passes.extend(p)
        warnings.extend(w)
        failures.extend(f)
    lines = report_lines("Manuscript Plan Validation Report", passes, warnings, failures)
    report = "\n".join(lines)
    if ms_dir.exists():
        (ms_dir / "manuscript_validation_report.md").write_text(report)
    print(report)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
