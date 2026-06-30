#!/usr/bin/env python3
"""Audit contribution-to-experiment validation adequacy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiment_grounding_common import (
    evaluate_plan,
    experiment_dir,
    load_plan,
    report_lines,
    resolve_workspace,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--require-complete-validation-chain", action="store_true")
    parser.add_argument("--experiment-dir", type=Path)
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    exp_dir = experiment_dir(workspace, args.experiment_dir)
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []
    if not workspace.exists():
        raise SystemExit(f"FAIL workspace not found: {workspace}")
    if not exp_dir.exists():
        failures.append(f"FAIL experiment_validation directory missing: {exp_dir}")
        plan = {}
    else:
        plan = load_plan(exp_dir, failures)
        passes.append(f"PASS loaded experiment validation plan: {exp_dir}")

    if plan:
        p, w, f = evaluate_plan(
            plan,
            strict=args.strict,
            require_complete_validation_chain=args.require_complete_validation_chain,
            workspace=workspace,
        )
        passes.extend(p)
        warnings.extend(w)
        failures.extend(f)

    decision = "fail_requires_revision" if failures else ("pass_with_warnings" if warnings else "pass")
    audit = {
        "validation_chain_status": "fail_due_to_validation_gap" if failures else ("pass_with_minor_risks" if warnings else "pass"),
        "unsupported_contributions": [f for f in failures if "contribution" in f],
        "missing_validation_targets": [f for f in failures if "validation target" in f],
        "missing_experiment_designs": [f for f in failures if "experiment design" in f],
        "missing_baselines": [f for f in failures if "baseline" in f],
        "weak_baseline_risks": [f for f in failures + warnings if "weak baseline" in f or "cherry" in f],
        "missing_metrics": [f for f in failures if "metric" in f],
        "metric_claim_mismatches": [f for f in failures if "metric" in f and "missing" in f],
        "missing_ablations": [f for f in failures if "ablation" in f],
        "missing_statistical_tests": [f for f in failures if "statistical" in f or "independent runs" in f],
        "missing_reproducibility_items": [f for f in failures if "reproducibility" in f or "artifact" in f],
        "fabricated_result_risks": [f for f in failures if "fabricated result" in f or "unsupported empirical" in f],
        "unfair_comparison_risks": [f for f in failures if "fair" in f or "baseline" in f],
        "reviewer_validation_questions": [
            "Is each baseline fair and necessary?",
            "Are metrics aligned with each contribution claim?",
            "Are ablations sufficient for algorithmic mechanisms?",
            "Are stochastic effects handled through independent runs and statistics?",
            "Are synthetic cases labeled and limited?",
        ],
        "repair_actions": repair_actions(failures),
        "pass_or_revise_decision": decision,
        "pass_count": len(passes),
        "warning_count": len(warnings),
        "fail_count": len(failures),
        "passes": passes,
        "warnings": warnings,
        "failures": failures,
    }
    if exp_dir.exists():
        write_json(exp_dir / "validation_adequacy_audit.json", audit)
        lines = report_lines("Validation Adequacy Audit", passes, warnings, failures, decision_key="audit_decision")
        actions = audit["repair_actions"]
        if actions:
            lines.extend(["## REPAIR ACTIONS", *[f"- {action}" for action in actions], ""])
        (exp_dir / "validation_adequacy_audit.md").write_text("\n".join(lines))
        print("\n".join(lines))
    else:
        print(json.dumps(audit, indent=2))
    if failures:
        raise SystemExit(1)


def repair_actions(failures: list[str]) -> list[str]:
    actions: list[str] = []
    for failure in failures:
        lower = failure.lower()
        if "ablation" in lower:
            actions.append("Add a no-coevolution, non-decomposed, no-repair, or no-local-search variant matching the claimed mechanism.")
        elif "pareto" in lower:
            actions.append("Add hypervolume, IGD/IGD+ when a reference is available, spread/spacing, and Pareto visualization.")
        elif "feasibility" in lower:
            actions.append("Add feasibility rate, total constraint violation, maximum violation, and constraint-specific violation metrics.")
        elif "sequential baseline" in lower:
            actions.append("Add layout-only, cabling-only, or cabling-after-layout sequential baseline, or justify not applicable.")
        elif "statistical" in lower or "independent runs" in lower:
            actions.append("Add independent runs, random seed policy, statistical test rationale, and multiple-comparison policy when needed.")
        elif "reproducibility" in lower or "artifact" in lower:
            actions.append("Add random seeds, parameters, budget, environment, result schema, and artifact traceability.")
        elif "fabricated" in lower or "unsupported empirical" in lower:
            actions.append("Rewrite result-like wording as a validation objective or conditional expected_result_pattern.")
        elif "traceability" in lower:
            actions.append("Add Contribution-to-Experiment Traceability Table to the final topic package.")
    return sorted(set(actions))


if __name__ == "__main__":
    main()
