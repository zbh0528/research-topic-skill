#!/usr/bin/env python3
"""Build an experiment-grounded validation plan without fabricating results."""

from __future__ import annotations

import argparse
from pathlib import Path

from experiment_grounding_common import (
    build_sample_plan,
    experiment_dir,
    real_contribution_items,
    resolve_workspace,
    write_plan,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--from-final-topic-package", action="store_true")
    parser.add_argument("--from-contribution-chain", action="store_true")
    parser.add_argument("--demo-if-missing", action="store_true")
    parser.add_argument("--experiment-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    if not workspace.exists():
        raise SystemExit(f"FAIL workspace not found: {workspace}")

    contributions = real_contribution_items(workspace)
    is_demo = False
    if not contributions:
        if not args.demo_if_missing:
            raise SystemExit(
                "FAIL no real contribution chain found; rerun with --demo-if-missing to create a conservative demo plan"
            )
        is_demo = True
        print("WARNING no real contribution chain found; generating conservative demo validation plan")

    project_id = workspace.name
    plan = build_sample_plan(project_id, contributions or None, is_demo=is_demo)
    if not is_demo:
        for section in plan.values():
            if isinstance(section, dict):
                section["is_demo_plan"] = False
                section["requires_real_contribution_chain"] = False

    exp_dir = experiment_dir(workspace, args.experiment_dir)
    write_plan(exp_dir, plan, overwrite=args.overwrite)
    print(f"PASS built validation plan: {exp_dir}")
    if is_demo:
        print("WARNING demo plan requires real contribution chain before complete-chain acceptance")


if __name__ == "__main__":
    main()
