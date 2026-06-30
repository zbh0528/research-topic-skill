#!/usr/bin/env python3
"""Generate a reproducibility checklist from a v0.3 validation plan."""

from __future__ import annotations

import argparse
from pathlib import Path

from experiment_grounding_common import experiment_dir, read_json, resolve_workspace


CHECKLIST_SECTIONS = [
    ("Code availability", "code_requirements"),
    ("Dependency environment", "environment_requirements"),
    ("Random seeds", "random_seed_policy"),
    ("Parameter settings", "parameter_requirements"),
    ("Computational budget", "computational_budget_policy"),
    ("Hardware/software", "environment_requirements"),
    ("Input instances", "data_requirements"),
    ("Data source", "data_requirements"),
    ("Preprocessing", "data_requirements"),
    ("Result tables", "result_reporting_schema"),
    ("Statistical scripts", "artifact_requirements"),
    ("Figure generation", "figure_table_plan"),
    ("Experiment logs", "experiment_log_requirements"),
    ("Artifact versioning", "artifact_traceability_table"),
    ("Supplementary material checklist", "artifact_requirements"),
]


def as_lines(value: object) -> list[str]:
    if value is None or value == "":
        return ["MISSING"]
    if isinstance(value, list):
        return [str(item) for item in value] or ["MISSING"]
    if isinstance(value, dict):
        return [f"`{key}`: {item}" for key, item in value.items()] or ["MISSING"]
    return [str(value)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--experiment-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    exp_dir = experiment_dir(workspace, args.experiment_dir)
    path = exp_dir / "reproducibility_plan.json"
    if not path.exists():
        raise SystemExit(f"FAIL reproducibility_plan.json not found: {path}")
    data = read_json(path)
    lines = [
        "# Reproducibility Checklist",
        "",
        "This checklist records planned reproducibility requirements only. It does not claim that experiments were run.",
        "",
    ]
    for title, key in CHECKLIST_SECTIONS:
        lines.append(f"## {title}")
        values = as_lines(data.get(key))
        for value in values:
            lines.append(f"- [ ] {value}")
        lines.append("")
    output = exp_dir / "reproducibility_checklist.md"
    output.write_text("\n".join(lines))
    print(f"PASS generated reproducibility checklist: {output}")


if __name__ == "__main__":
    main()
