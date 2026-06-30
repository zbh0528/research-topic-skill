# EG00_experiment_grounding_protocol Experiment Grounding Protocol

## Module ID
`EG00_experiment_grounding_protocol`

## Module Name
Experiment Grounding Protocol

## Purpose
Define the v0.3.0 experiment-grounding layer, ID rules, status rules, no-fabricated-results rule, adequacy rules, reproducibility rule, reviewer defense rule, and compact experiment_context contract.

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
- `workspaces/<project_id>/experiment_validation/experiment_grounding_report.json`
- `workspaces/<project_id>/experiment_validation/experiment_grounding_report.md`

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

## ID Rules
- validation_target_id: `VT001`, `VT002`, `VT003`
- experiment_id: `EX001`, `EX002`, `EX003`
- baseline_id: `B001`, `B002`, `B003`
- metric_id: `M001`, `M002`, `M003`
- ablation_id: `A001`, `A002`, `A003`
- case_study_id: `CS001`, `CS002`, `CS003`
- statistical_test_id: `ST001`, `ST002`, `ST003`
- artifact_id: `AR001`, `AR002`, `AR003`

## Status Rules
`validation_planned`, `partially_planned`, `insufficiently_planned`, `unsupported_by_experiment_plan`, `not_applicable`, `requires_empirical_results`.

## Experiment Support Rules
`directly_tested_by_plan`, `indirectly_tested_by_plan`, `weakly_tested_by_plan`, `not_tested`, `requires_new_experiment`, `cannot_be_validated_empirically`.

## Experiment Context Contract
```json
{
  "experiment_grounding_mode": "experiment_grounded",
  "validation_target_summary": [],
  "experiment_design_summary": [],
  "baseline_summary": [],
  "metric_summary": [],
  "ablation_summary": [],
  "statistical_analysis_summary": [],
  "reproducibility_summary": [],
  "validation_adequacy_summary": {},
  "experiment_risks": [],
  "claims_not_yet_supported_by_validation_plan": [],
  "trace_context": {}
}
```
