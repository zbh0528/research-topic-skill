# 03 Problem Identification

## Module ID

Document ID: `03_problem_identification`  
Workspace ID: `02_problem_identification`

## Module Name

Problem Identification

## Purpose

Convert candidate domain tensions into candidate problem cards and select a main research problem.

## What This Module Does

- Convert each domain tension into a candidate gap.
- Convert candidate gaps into research problems.
- Classify problem type.
- Check specificity, researchability, and paper potential.
- Generate problem cards.
- Score each card.
- Select main problem and backup problems.
- Generate `next_input` for theoretical positioning.

## What This Module Does Not Do

- It does not begin with an algorithm.
- It does not claim novelty.
- It does not decide contribution wording.
- It does not run experiments.

## Required Input

Direct upstream `01_domain_scan/next_input.json`.

## Required Output Files

- `workspaces/<project_id>/02_problem_identification/input.json`
- `workspaces/<project_id>/02_problem_identification/output.json`
- `workspaces/<project_id>/02_problem_identification/output.md`
- `workspaces/<project_id>/02_problem_identification/next_input.json`
- `workspaces/<project_id>/02_problem_identification/validation_report.md`

## Required `structured_output` Fields

- `candidate_problems`
- `selected_problem`
- `backup_problems`
- `ranking_criteria`
- `rejected_problems`
- `selection_rationale`
- `evidence_requirements`
- `uncertainty_log`

Each problem card must include `problem_id`, `problem_title`, `problem_statement`, `source_domain_tension_id`, `source_domain_tension`, `problem_type`, `why_it_matters`, `why_not_solved_yet`, `research_question`, `evidence_needed`, `expected_contribution_opportunities`, `feasibility`, `novelty_risk`, `reviewer_risk`, `publishability_score`, `scoring_breakdown`, and `next_input_fragment`.

## Required `next_input` Fields

- `selected_problem`
- `backup_problems_summary`
- `problem_properties`
- `required_theoretical_positioning`
- `evidence_policy`
- `trace_context`

## Procedure

1. Convert each domain tension into a candidate gap.
2. Convert candidate gap into a research problem.
3. Classify problem type: modeling, algorithmic, theoretical, experimental, or application.
4. Check whether the problem is specific.
5. Check whether the problem is researchable.
6. Check whether the problem can support a paper.
7. Generate problem cards.
8. Score each card.
9. Select main problem and backup problems.
10. Generate `next_input` for `theoretical_positioning`.

## Scoring Criteria

Score each card by significance, novelty potential, theoretical depth, algorithmic opportunity, experimental feasibility, reviewer comprehensibility, and risk.

## Quality Gates

- The selected problem traces to a `domain_tension_id`.
- The problem statement describes a problem structure, not an algorithm preference.
- The problem is specific enough to guide theory positioning.
- Novelty status is not overstated.

## Common Failure Modes

- Writing "use algorithm X for wind farm optimization" as the research problem.
- Selecting a broad topic instead of a researchable problem.
- Omitting feasibility and reviewer risk.
- Losing traceability to the domain tension.

## Evidence Status Requirements

Use `inferred` for problem statements derived from candidate tensions. Use `needs_literature_verification` for claims that a problem is underexplored or unresolved.

## Reviewer-Risk Requirements

Record why a reviewer may view the problem as too incremental, too applied, already solved, or not distinct from sequential optimization.

## Revision Hooks

- Edit `candidate_problems` to add or remove problem cards.
- Edit `selected_problem` to change the main direction.
- Changing the selected problem affects all downstream modules.

## Downstream Contract

`next_input.json` must provide the selected problem, compact backup summary, problem properties, and theoretical positioning requirements only.

## Literature-Grounded Mode Requirements

- Candidate problems must come from grounded or partially grounded `domain_tension` records.
- `selected_problem` must include `linked_gap_id`, `linked_claim_ids`, `linked_evidence_ids`, `grounding_status`, `corpus_scope`, `counterevidence`, `novelty_risk`, and `evidence_limitations`.
- Weak evidence lowers `publishability_score`.
- Contradictory evidence must enter `reviewer_risk`.
- Field-wide novelty must stay `needs_literature_verification` unless the user provides systematic review evidence.
