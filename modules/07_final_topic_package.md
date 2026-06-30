# 07 Final Topic Package

## Module ID

Document ID: `07_final_topic_package`  
Workspace ID: `06_final_topic_package`

## Module Name

Final Topic Package

## Purpose

Integrate audited content into a final research topic package for supervisor discussion, collaborator planning, or downstream paper writing.

## What This Module Does

- Produce candidate title and alternative titles.
- State one-sentence thesis.
- Summarize research background and domain gap.
- State core research problem.
- Explain theoretical positioning.
- List research questions.
- List contribution claims with safe wording.
- Derive method design implications.
- Define validation plan, baselines, and ablations.
- Prepare reviewer risk and defense.
- Build introduction logic outline.
- Build traceability table.
- List next research actions.

## What This Module Does Not Do

- It does not write the full paper.
- It does not fabricate completed validation.
- It does not erase unresolved risks.
- It does not upgrade uncertain claims to verified claims.

## Required Input

Direct upstream `05_chain_consistency_audit/next_input.json`.

## Required Output Files

- `workspaces/<project_id>/06_final_topic_package/input.json`
- `workspaces/<project_id>/06_final_topic_package/output.json`
- `workspaces/<project_id>/06_final_topic_package/output.md`
- `workspaces/<project_id>/06_final_topic_package/next_input.json`
- `workspaces/<project_id>/06_final_topic_package/validation_report.md`

## Required `structured_output` Fields

- `candidate_title`
- `alternative_titles`
- `central_thesis`
- `research_background`
- `domain_gap`
- `core_problem`
- `theoretical_positioning`
- `research_questions`
- `contribution_claims`
- `method_design_implications`
- `validation_plan`
- `required_baselines`
- `required_ablation_studies`
- `reviewer_risk_and_defense`
- `introduction_logic_outline`
- `traceability_table`
- `next_research_actions`
- `evidence_requirements`
- `uncertainty_log`

## Required `next_input` Fields

`next_input` may be an empty object, but it must exist.

## Procedure

1. Build final package sections.
2. Preserve audit-required repairs.
3. Build traceability table from domain tension to contribution.
4. Convert contribution wording to safe claim language.
5. Preserve evidence requirements and uncertainty.
6. Output final package for introduction, related work, method overview, experiment design, and reviewer-response preparation.

## Final Package Required Sections

- Candidate Title
- Alternative Titles
- One-sentence Thesis
- Research Background
- Domain Gap
- Core Research Problem
- Theoretical Positioning
- Research Questions
- Contribution Claims
- Method Design Implications
- Validation Plan
- Required Baselines
- Required Ablation Studies
- Reviewer Risk and Defense
- Introduction Logic Outline
- Traceability Table
- Next Research Actions

## Quality Gates

- Every final conclusion has a source module and identifier.
- Unverified literature statements remain marked.
- Contribution claims are bounded.
- Validation plan can support each contribution.
- Reviewer risks are visible.

## Common Failure Modes

- Producing only a title.
- Removing uncertainty to make the package look polished.
- Losing traceability.
- Using unsafe novelty wording.

## Evidence Status Requirements

Carry evidence status from upstream. Do not upgrade claims unless evidence changed and is recorded.

## Reviewer-Risk Requirements

Each contribution must include a likely reviewer risk and defense path.

## Revision Hooks

- Edit title and thesis locally if claims do not change.
- Edit contribution claims in `05_contribution_argumentation` if claim scope changes.
- Edit selected problem in `03_problem_identification` if the topic direction changes.

## Downstream Contract

The final package should be usable as input for introduction, related work, method overview, experiment design, and reviewer-response preparation.

## Literature-Grounded Mode Requirements

- Add sections: `Literature Evidence Summary`, `Corpus Scope`, `Evidence-Backed Domain Gap`, `Evidence-Backed Core Problem`, `Evidence-Backed Contribution Claims`, `Counterevidence and Limitations`, `Claims Requiring Further Literature Verification`, and `Evidence Traceability Table`.
- Each traceability row must include `final_claim_id`, `final_claim_text`, `claim_type`, `claim_scope`, `grounding_status`, `support_strength`, `linked_paper_ids`, `linked_evidence_ids`, `linked_problem_id`, `linked_contribution_id`, `counterevidence`, and `safer_wording`.
- Do not hide counterevidence.
- Do not upgrade corpus-scoped evidence into field-general novelty.

## Experiment-Grounded Mode Requirements

Add sections:

- `Experiment-Grounded Validation Plan`
- `Contribution-to-Experiment Traceability Table`
- `Baseline Justification`
- `Metric Justification`
- `Ablation Study Plan`
- `Statistical Analysis Plan`
- `Reproducibility Checklist`
- `Claims Not Yet Experimentally Supported`
- `Reviewer Validation Risk and Defense`

Each Contribution-to-Experiment Traceability Table row must include:

- `contribution_id`
- `contribution_claim`
- `validation_target_id`
- `experiment_id`
- `baseline_ids`
- `metric_ids`
- `ablation_ids`
- `statistical_test_ids`
- `artifact_ids`
- `success_condition`
- `failure_condition`
- `reviewer_risk`
- `validation_status`

Rules:

- Do not present a validation plan as executed experiments.
- Do not claim statistical significance, rankings, or performance superiority.
- Surface claims that are not yet experimentally supported.
- Surface validation limitations such as unavailable baselines or synthetic-only case studies.
