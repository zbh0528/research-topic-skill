#!/usr/bin/env python3
"""Audit manuscript claims for evidence, result, and reviewer-risk grounding."""

from __future__ import annotations

import argparse
from pathlib import Path

from manuscript_grounding_common import evaluate_plan, load_plan, manuscript_dir, report_lines, resolve_workspace, write_json


def repair_actions(failures: list[str]) -> list[str]:
    actions: list[str] = []
    for failure in failures:
        lower = failure.lower()
        if "citation" in lower:
            actions.append("Rewrite as citation_requirement and add verified corpus evidence before submission.")
        if "result" in lower or "empirical" in lower:
            actions.append("Replace result wording with result_placeholder until real result evidence exists.")
        if "introduction" in lower:
            actions.append("Repair Introduction chain: background -> streams -> gap -> problem -> contribution -> validation preview.")
        if "related work" in lower:
            actions.append("Reorganize Related Work by research stream, limitation, relation to problem, and baseline relevance.")
        if "algorithm wrapping" in lower or "method component" in lower:
            actions.append("Map each method component to problem_property, contribution_id, and ablation requirement.")
        if "experiment section" in lower:
            actions.append("Link Experiment section to validation targets, baselines, metrics, ablations, statistics, and artifacts.")
        if "limitation" in lower:
            actions.append("Add corpus-scope, synthetic-demo, missing-result, counterevidence, and generalization limitations.")
        if "reviewer" in lower:
            actions.append("Use anticipated reviewer objection wording and attach a response strategy.")
        if "traceability" in lower:
            actions.append("Add Contribution-to-Manuscript Traceability table.")
    return sorted(set(actions))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--require-complete-manuscript-chain", action="store_true")
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
        plan = load_plan(ms_dir, failures)
        passes.append(f"PASS loaded manuscript grounding plan: {ms_dir}")
    if plan:
        p, w, f = evaluate_plan(plan, strict=args.strict, require_complete=args.require_complete_manuscript_chain, workspace=workspace)
        passes.extend(p)
        warnings.extend(w)
        failures.extend(f)
    decision = "fail_requires_revision" if failures else ("pass_with_warnings" if warnings else "pass")
    audit = {
        "manuscript_chain_status": "fail_due_to_manuscript_grounding_gap" if failures else ("pass_with_minor_risks" if warnings else "pass"),
        "unsupported_manuscript_claims": [f for f in failures if "claim" in f],
        "missing_traceability": [f for f in failures if "traceability" in f],
        "missing_citation_requirements": [f for f in failures if "citation" in f],
        "missing_result_placeholders": [f for f in failures if "result" in f],
        "fabricated_citation_risks": [f for f in failures if "fabricated citation" in f],
        "fabricated_result_risks": [f for f in failures if "fabricated result" in f or "empirical" in f],
        "overclaim_risks": [f for f in failures if "overclaim" in f],
        "weak_introduction_links": [f for f in failures if "introduction" in f],
        "weak_related_work_links": [f for f in failures if "related work" in f],
        "method_alignment_risks": [f for f in failures if "method" in f or "algorithm wrapping" in f],
        "experiment_alignment_risks": [f for f in failures if "experiment section" in f],
        "hidden_limitation_risks": [f for f in failures if "limitation" in f],
        "reviewer_response_gaps": [f for f in failures if "reviewer" in f or "response" in f],
        "repair_actions": repair_actions(failures),
        "pass_or_revise_decision": decision,
        "pass_count": len(passes),
        "warning_count": len(warnings),
        "fail_count": len(failures),
        "passes": passes,
        "warnings": warnings,
        "failures": failures,
    }
    if ms_dir.exists():
        write_json(ms_dir / "manuscript_adequacy_audit.json", audit)
        lines = report_lines("Manuscript Adequacy Audit", passes, warnings, failures, key="audit_decision")
        if audit["repair_actions"]:
            lines.extend(["## REPAIR ACTIONS", *[f"- {item}" for item in audit["repair_actions"]], ""])
        (ms_dir / "manuscript_adequacy_audit.md").write_text("\n".join(lines))
        print("\n".join(lines))
    else:
        print("\n".join(report_lines("Manuscript Adequacy Audit", passes, warnings, failures, key="audit_decision")))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
