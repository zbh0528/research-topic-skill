#!/usr/bin/env python3
"""Generate a manuscript grounding checklist from a v0.4 plan."""

from __future__ import annotations

import argparse
from pathlib import Path

from manuscript_grounding_common import evaluate_plan, load_plan, manuscript_dir, resolve_workspace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--manuscript-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    ms_dir = manuscript_dir(workspace, args.manuscript_dir)
    failures: list[str] = []
    plan = load_plan(ms_dir, failures)
    if failures:
        raise SystemExit("\n".join(failures))

    passes, warnings, audit_failures = evaluate_plan(plan, strict=args.strict, workspace=workspace)
    checklist = [
        "# Manuscript Grounding Checklist",
        "",
        "This checklist records manuscript planning adequacy only. It is not a generated paper.",
        "",
        "## Required Before Drafting",
        "- [ ] Replace demo plan with a real final topic package when available.",
        "- [ ] Replace all result placeholders with real experiment evidence before result claims are written.",
        "- [ ] Attach every citation requirement to verified corpus evidence.",
        "- [ ] Keep gap and contribution language corpus-scoped unless direct field-wide evidence exists.",
        "- [ ] Keep anticipated reviewer objections separate from received reviewer comments.",
        "",
        "## Current Audit Counts",
        f"- passes: {len(passes)}",
        f"- warnings: {len(warnings)}",
        f"- failures: {len(audit_failures)}",
        "",
    ]
    if warnings:
        checklist.extend(["## Warnings", *[f"- {item}" for item in warnings], ""])
    if audit_failures:
        checklist.extend(["## Failures", *[f"- {item}" for item in audit_failures], ""])

    output = ms_dir / "manuscript_checklist.md"
    output.write_text("\n".join(checklist))
    print(f"PASS generated manuscript checklist: {output}")


if __name__ == "__main__":
    main()
