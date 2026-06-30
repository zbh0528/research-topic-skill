# 06 Chain Consistency Audit

## Module ID

Document ID: `06_chain_consistency_audit`  
Workspace ID: `05_chain_consistency_audit`

## Module Name

Chain Consistency Audit

## Purpose

Audit whether the reasoning chain from domain scan to contribution argumentation is complete, traceable, and defensible.

## What This Module Does

- Check whether domain scan supports problem identification.
- Check whether selected problem comes from a `domain_tension`.
- Check whether theoretical positioning serves selected problem.
- Check whether method implications come from problem properties.
- Check whether contributions link to problem and theory.
- Check whether validation supports contribution claims.
- Detect overclaiming, vague claims, missing baselines, missing ablations, reviewer jumps, algorithm-first logic, assumptions written as facts, and missing `evidence_status`.

## What This Module Does Not Do

- It does not silently rewrite earlier modules.
- It does not approve unsupported contributions.
- It does not create final topic package sections until readiness is established.

## Required Input

Direct upstream `04_contribution_argumentation/next_input.json`, which must contain compact links and trace context.

## Required Output Files

- `workspaces/<project_id>/05_chain_consistency_audit/input.json`
- `workspaces/<project_id>/05_chain_consistency_audit/output.json`
- `workspaces/<project_id>/05_chain_consistency_audit/output.md`
- `workspaces/<project_id>/05_chain_consistency_audit/next_input.json`
- `workspaces/<project_id>/05_chain_consistency_audit/validation_report.md`

## Required `structured_output` Fields

- `chain_status`
- `broken_links`
- `weak_links`
- `overclaim_risks`
- `vague_claims`
- `missing_evidence`
- `missing_experiments`
- `missing_baselines`
- `missing_ablations`
- `reviewer_questions`
- `repair_actions`
- `pass_or_revise_decision`
- `final_package_readiness`
- `evidence_requirements`
- `uncertainty_log`

`chain_status` should be one of `pass`, `pass_with_minor_risks`, `revise_required`, or `fail_due_to_broken_chain`.

## Required `next_input` Fields

- `audited_central_thesis`
- `approved_contributions`
- `required_repairs`
- `validation_plan_requirements`
- `reviewer_risk_summary`
- `final_package_sections`
- `evidence_policy`
- `trace_context`

## Procedure

1. Check domain-to-problem support.
2. Check problem-to-theory support.
3. Check theory-to-method support.
4. Check contribution links.
5. Check validation sufficiency.
6. Check baseline and ablation sufficiency.
7. Check evidence status coverage.
8. Check reviewer perception.
9. Decide pass, revise, or fail.
10. Generate `next_input` for final package.

## Reviewer Questions

Include questions such as:

- Why is the problem important?
- Why is the proposed method necessary?
- What is new beyond combining existing models?
- Are the baselines sufficient?
- Are the claims supported by experiments?
- Is this more than applying an evolutionary algorithm to a domain problem?
- Does joint optimization produce different trade-offs than sequential optimization?
- Are the mathematical model and experiments sufficient to support the claims?

## Quality Gates

- No contribution is approved without problem and theory links.
- No strong claim survives without evidence.
- Required validation is concrete enough for experiment design.
- Final package readiness is explicit.

## Common Failure Modes

- Treating weak links as pass.
- Missing algorithm-first logic errors.
- Ignoring missing baselines or ablations.
- Allowing literature guesses to remain as facts.

## Evidence Status Requirements

Flag missing or invalid `evidence_status`. Downgrade unverifiable literature claims to `needs_literature_verification`.

## Reviewer-Risk Requirements

Summarize reviewer risks and required defenses for the final package.

## Revision Hooks

- Repair broken links in the earliest affected module.
- Repair vague claims in `05_contribution_argumentation`.
- Repair method mismatch in `04_theoretical_positioning`.
- Repair problem mismatch in `03_problem_identification`.

## Downstream Contract

`next_input.json` must contain only audited material, required repairs, and final package section requirements.
