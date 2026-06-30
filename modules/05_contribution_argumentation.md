# 05 Contribution Argumentation

## Module ID

Document ID: `05_contribution_argumentation`  
Workspace ID: `04_contribution_argumentation`

## Module Name

Contribution Argumentation

## Purpose

Convert theoretical positioning into defensible contribution claims with evidence requirements and reviewer-risk defenses.

## What This Module Does

- Generate a central thesis.
- Generate contribution candidates.
- Link each contribution to the selected problem.
- Link each contribution to theoretical positioning.
- Define required validation for each contribution.
- Define reviewer risk for each contribution.
- Define safe wording for each contribution.
- Remove unsupported overclaims.
- Generate `next_input` for chain consistency audit.

## What This Module Does Not Do

- It does not claim novelty without verified evidence.
- It does not invent completed experimental validation.
- It does not write final paper prose.

## Required Input

Direct upstream `03_theoretical_positioning/next_input.json`.

## Required Output Files

- `workspaces/<project_id>/04_contribution_argumentation/input.json`
- `workspaces/<project_id>/04_contribution_argumentation/output.json`
- `workspaces/<project_id>/04_contribution_argumentation/output.md`
- `workspaces/<project_id>/04_contribution_argumentation/next_input.json`
- `workspaces/<project_id>/04_contribution_argumentation/validation_report.md`

## Required `structured_output` Fields

- `central_thesis`
- `contributions`
- `contribution_to_problem_links`
- `contribution_to_theory_links`
- `required_validation`
- `unsafe_claims_removed`
- `safer_wording_map`
- `evidence_requirements`
- `uncertainty_log`

Each contribution must include `contribution_id`, `contribution_type`, `contribution_claim`, `linked_problem_id`, `linked_problem_property`, `linked_theoretical_positioning`, `linked_domain_tension_id`, `required_evidence`, `required_experiment`, `likely_reviewer_question`, `defense_strategy`, `unsafe_wording_to_avoid`, `safer_wording`, `boundary_of_claim`, and `evidence_status`.

## Required `next_input` Fields

- `central_thesis`
- `contributions`
- `contribution_links`
- `required_validation`
- `reviewer_risks`
- `evidence_policy`
- `trace_context`

## Procedure

1. Generate central thesis.
2. Generate contribution candidates.
3. Link each contribution to selected problem.
4. Link each contribution to theoretical positioning.
5. Define required validation for each contribution.
6. Define reviewer risk for each contribution.
7. Define safe wording for each contribution.
8. Remove unsupported overclaims.
9. Generate `next_input` for `chain_consistency_audit`.

## Contribution Types

Allowed contribution types include modeling contribution, algorithmic contribution, experimental contribution, benchmark contribution, theoretical framing contribution, and engineering insight contribution.

## Quality Gates

- Every contribution answers why it is not ordinary algorithm application.
- Every contribution links to problem and theory identifiers.
- Unsafe wording is removed or downgraded.
- Required evidence is sufficient and concrete.

## Common Failure Modes

- Writing vague claims such as "improves performance".
- Claiming novelty before literature verification.
- Omitting required baselines or ablation studies.
- Losing the problem-to-theory-to-contribution link.

## Evidence Status Requirements

Use `inferred` for contribution candidates derived from problem/theory links. Use `needs_literature_verification` for novelty or prior-work comparison. Use `speculative` for untested mechanisms.

## Reviewer-Risk Requirements

Each contribution must include likely reviewer question and defense strategy.

## Revision Hooks

- Edit `central_thesis` to change paper direction.
- Edit `contributions` to add or remove claims.
- Edit `required_validation` to strengthen evidence plan.
- Changing claims affects `06_chain_consistency_audit`.

## Downstream Contract

`next_input.json` must provide approved candidate claims, links, required validation, and reviewer risks for audit.

## Literature-Grounded Mode Requirements

- Each contribution must include `linked_evidence_ids`, `linked_claim_ids`, `corpus_scope`, `grounding_status`, `counterevidence`, `evidence_limitations`, `claim_scope`, and `novelty_safety_level`.
- Allowed `novelty_safety_level`: `unsafe`, `corpus_scoped`, `evidence_supported_but_not_exhaustive`, `verified_by_user_provided_systematic_review`.
- A contribution without evidence links is only a proposed contribution, not a verified contribution.
- `first`, `novel`, `state-of-the-art`, and `unprecedented` are unsafe by default.
- `safer_wording` must exist for every contribution claim.
