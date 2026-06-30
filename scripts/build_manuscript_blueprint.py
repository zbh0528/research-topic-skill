#!/usr/bin/env python3
"""Build a manuscript-grounded writing plan without drafting the paper."""

from __future__ import annotations

import argparse
from pathlib import Path

from manuscript_grounding_common import build_sample_plan, final_topic_is_real, manuscript_dir, resolve_workspace, write_plan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--from-final-topic-package", action="store_true")
    parser.add_argument("--from-experiment-grounding", action="store_true")
    parser.add_argument("--demo-if-missing", action="store_true")
    parser.add_argument("--manuscript-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    if not workspace.exists():
        raise SystemExit(f"FAIL workspace not found: {workspace}")
    is_demo = not final_topic_is_real(workspace)
    if is_demo and not args.demo_if_missing:
        raise SystemExit("FAIL no real final topic package found; use --demo-if-missing for a conservative demo manuscript plan")
    if is_demo:
        print("WARNING no real final topic package found; generating conservative demo manuscript plan")
    plan = build_sample_plan(workspace.name, is_demo=is_demo)
    ms_dir = manuscript_dir(workspace, args.manuscript_dir)
    write_plan(ms_dir, plan, overwrite=args.overwrite)
    print(f"PASS built manuscript blueprint: {ms_dir}")
    if is_demo:
        print("WARNING demo manuscript plan requires real final topic package and real results")


if __name__ == "__main__":
    main()
