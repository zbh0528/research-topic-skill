#!/usr/bin/env python3
"""Validate v0.3 experiment-grounded validation plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiment_grounding_common import (
    evaluate_plan,
    experiment_dir,
    load_plan,
    plan_file_map,
    report_lines,
    resolve_workspace,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_MAP = {
    "validation_targets": "validation_target.schema.json",
    "experiment_design": "experiment_design.schema.json",
    "baseline_plan": "baseline_plan.schema.json",
    "metric_plan": "metric_plan.schema.json",
    "ablation_plan": "ablation_plan.schema.json",
    "case_study_plan": "case_study_plan.schema.json",
    "statistical_analysis_plan": "statistical_analysis_plan.schema.json",
    "reproducibility_plan": "reproducibility_plan.schema.json",
    "experiment_grounding_report": "experiment_grounding_report.schema.json",
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
    parser.add_argument("--experiment-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    exp_dir = experiment_dir(workspace, args.experiment_dir)
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []
    if not exp_dir.exists():
        failures.append(f"FAIL experiment_validation directory missing: {exp_dir}")
        plan = {}
    else:
        passes.append(f"PASS experiment_validation directory exists: {exp_dir}")
        plan = load_plan(exp_dir, failures)

    Validator, schema_warning = try_jsonschema()
    if schema_warning:
        warnings.append(schema_warning)
    if Validator:
        for key, schema_name in SCHEMA_MAP.items():
            if key not in plan:
                continue
            schema_path = ROOT / "schemas" / "experiment_grounding" / schema_name
            if not schema_path.exists():
                failures.append(f"FAIL missing schema: {schema_path}")
                continue
            schema = json.loads(schema_path.read_text())
            errors = sorted(Validator(schema).iter_errors(plan[key]), key=lambda err: list(err.path))
            if errors:
                for err in errors[:10]:
                    failures.append(f"FAIL schema {schema_name}: {list(err.path)} {err.message}")
            else:
                passes.append(f"PASS schema validation: {schema_name}")

    missing = sorted(set(plan_file_map()) - set(plan))
    for key in missing:
        failures.append(f"FAIL missing required plan section: {key}")

    if plan:
        p, w, f = evaluate_plan(plan, strict=args.strict)
        passes.extend(p)
        warnings.extend(w)
        failures.extend(f)

    lines = report_lines("Experiment Plan Validation Report", passes, warnings, failures)
    report = "\n".join(lines)
    if exp_dir.exists():
        (exp_dir / "experiment_validation_report.md").write_text(report)
    print(report)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
