#!/usr/bin/env python3
"""Generate an anticipated reviewer-response planning report from manuscript grounding."""

from __future__ import annotations

import argparse
from pathlib import Path

from manuscript_grounding_common import load_plan, manuscript_dir, resolve_workspace, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--manuscript-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    ms_dir = manuscript_dir(workspace, args.manuscript_dir)
    failures: list[str] = []
    plan = load_plan(ms_dir, failures)
    if failures:
        raise SystemExit("\n".join(failures))

    output_path = ms_dir / "reviewer_response_plan.md"
    if output_path.exists() and not args.overwrite:
        raise SystemExit(f"FAIL reviewer response plan already exists: {output_path}")

    objections = plan.get("reviewer_objection_map", {}).get("reviewer_objections", [])
    strategies = {
        item.get("linked_reviewer_objection_id"): item
        for item in plan.get("reviewer_response_strategy", {}).get("response_strategies", [])
        if isinstance(item, dict)
    }

    lines = [
        "# Reviewer Response Plan",
        "",
        "This is an anticipated response plan only. It does not fabricate received reviewer comments.",
        "",
    ]
    for objection in objections:
        if not isinstance(objection, dict):
            continue
        strategy = strategies.get(objection.get("reviewer_objection_id"), {})
        lines.extend(
            [
                f"## {objection.get('reviewer_objection_id', 'OB?')}: {objection.get('objection_type', 'objection')}",
                "",
                f"- Anticipated concern: {objection.get('likely_question', '')}",
                f"- Evidence needed: {', '.join(objection.get('required_evidence', []))}",
                f"- Manuscript repair: {strategy.get('manuscript_revision', 'NEEDS_USER_DECISION')}",
                f"- Response stance: {strategy.get('direct_answer_plan', 'NEEDS_USER_DECISION')}",
                f"- Unsafe response to avoid: {strategy.get('unsafe_response_to_avoid', 'Do not overclaim.')}",
                "",
            ]
        )

    response_plan = {
        "is_received_reviewer_response": False,
        "source": "anticipated_objection_map",
        "objection_count": len([item for item in objections if isinstance(item, dict)]),
        "strategy_count": len(strategies),
        "output_path": str(output_path),
    }
    write_json(ms_dir / "reviewer_response_plan.json", response_plan)
    output_path.write_text("\n".join(lines))
    print(f"PASS generated reviewer response plan: {output_path}")


if __name__ == "__main__":
    main()
