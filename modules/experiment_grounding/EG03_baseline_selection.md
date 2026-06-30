# EG03_baseline_selection Baseline Selection

## Module ID
`EG03_baseline_selection`

## Module Name
Baseline Selection

## Purpose
Select and audit baseline sets for each experiment design.

## What this module does
- Builds one bounded part of the v0.3.0 experiment-grounding chain.
- Maps contribution claims to validation planning artifacts.
- Preserves IDs so downstream modules can cite compact references.

## What this module does not do
- It does not run experiments.
- It does not fabricate experimental results, p-values, rankings, or superiority claims.
- It does not replace real optimization code, simulation, engineering review, or human experimental judgment.

## Required input
- Direct upstream `next_input.json` or compact `experiment_context`.
- Contribution claims, reviewer risks, and optional literature `evidence_context`.

## Required output files
- `workspaces/<project_id>/experiment_validation/baseline_plan.json`
- `workspaces/<project_id>/experiment_validation/baseline_plan.md`

## Required structured_output fields
- IDs linking contribution, claim, validation target, experiment, baseline, metric, ablation, statistical test, and artifact.
- `validation_status` and `experiment_support_status`.
- `success_condition`, `failure_condition`, `reviewer_risk`, and `limitations`.

## Required next_input fields
- Compact IDs and summaries only.
- No full experiment draft, full literature text, or raw results.

## Procedure
1. Read only the declared upstream contract.
2. Create or validate stable IDs.
3. Map each contribution claim to the required validation element.
4. Record reviewer risks and repair hooks.
5. Write JSON and Markdown outputs.
6. Pass only compact summaries downstream.

## Quality gates
- No fabricated results.
- No unconditional `outperform` or significance wording.
- Every algorithmic mechanism has an ablation requirement.
- Every multi-objective claim has Pareto metric planning.
- Every constrained claim has feasibility and violation planning.
- Every joint layout-cabling claim has sequential or decoupled baseline planning unless justified.

## Common failure modes
- Treating expected_result_pattern as a real result.
- Listing baselines without fairness requirements.
- Selecting metrics that do not test the claim.
- Hiding synthetic-only or unavailable-baseline limitations.

## Evidence requirements
- Link to `contribution_id`, `claim_id`, and optional `evidence_id`.
- Use corpus-scoped literature support when v0.2 evidence exists.
- Mark unsupported content as planned or requiring empirical results.

## Validation requirements
- Validate JSON against schema.
- Audit ID uniqueness and references.
- Run strict validation before using the plan in a final topic package.

## Reviewer-risk requirements
- Ask whether baselines are fair, metrics align with claims, ablations isolate mechanisms, constraints are explicit, stochastic effects are handled, case studies are representative, and trade-offs are interpretable.

## Revision hooks
- Add missing baseline, metric, ablation, statistical, reproducibility, or artifact links.
- Downgrade claims that cannot be empirically supported.

## Downstream contract
Downstream modules cite IDs and summaries from `experiment_context`; detailed plans remain in `experiment_validation/`.
