---
name: windfarm-research-topic-skill
description: Use when constructing an evidence-bounded research topic package or manuscript-grounding plan for computer science, evolutionary computation, wind farm layout optimization, wind farm cable routing optimization, joint layout-cabling optimization, multi-objective optimization, constrained optimization, mixed discrete-continuous optimization, or spatial-network coupled optimization. Typical inputs include researcher background, target domain, materials, method preferences, excluded directions, target venue level, literature notes, code or experiment platforms, manuscript section needs, reviewer-risk concerns, and constraints. Produces persistent modular outputs through project intake, domain scan, problem identification, theoretical positioning, contribution argumentation, chain audit, final topic package, optional literature grounding, optional experiment grounding, and optional manuscript grounding. Do not use for fabricating papers, literature reviews, citations, experiments, novelty claims, reviewer comments, or unsupported conclusions; route real literature review, experiment execution, final manuscript drafting, and citation verification elsewhere.
---

# Windfarm Research Topic Skill

## Skill Name

`windfarm-research-topic-skill`

## Version

`v0.4.0-manuscript-structure-and-reviewer-response-grounded-writing-support`

## Use This Skill For

Use this skill to build a traceable research-topic reasoning chain before writing a paper. Valid scenarios include:

- Research topic construction for wind farm layout optimization.
- Research topic construction for wind farm cable routing optimization.
- Joint layout-cabling optimization topic design.
- Evolutionary computation paper ideation.
- Multi-objective or constrained optimization paper ideation.
- Introduction pre-logic construction.
- Related work organization pre-logic construction.
- Method overview pre-logic construction.
- Experiment design pre-logic construction.
- Manuscript blueprint and section argument planning.
- Paragraph claim planning with citation requirements and result placeholders.
- Anticipated reviewer-objection planning before real reviewer comments exist.

## Do Not Use This Skill For

- Directly fabricating a paper, literature review, citations, DOI, author list, venue, or experiment result.
- Generating a final manuscript or final reviewer response letter from placeholder evidence.
- Writing received reviewer comments that the user did not provide.
- Claiming `first`, `novel`, `unprecedented`, `state-of-the-art`, or similar strong novelty without verified evidence.
- Turning ordinary algorithm application into a contribution without a problem-structure argument.
- Pure wind turbine blade aerodynamic design.
- Pure power system protection design.
- Wind energy topics unrelated to optimization problem structure.
- User requests that ask AI to invent experimental results or unverifiable conclusions.

## Required User Inputs

Ask for missing items or mark them in `uncertainty_log`; do not invent them.

- Researcher profile and background.
- Target field and subfield.
- Existing foundation: notes, papers, code, data, or experiment platform.
- Preferred algorithm directions.
- Avoided research directions.
- Target paper level, venue, or degree requirement.
- Acceptable theoretical depth.
- Acceptable experiment complexity.
- Whether offshore wind farm is in scope.
- Whether uncertainty modeling is in scope.
- Whether multi-objective optimization is in scope.
- Whether joint layout-cabling optimization is in scope.
- Whether a literature library exists.
- Whether code or experimental platform exists.
- Whether a target journal or conference exists.

## Fixed Workflow

Run the workflow in this order unless resuming from a saved workspace:

1. `01 Project Intake` using `modules/01_project_intake.md`.
2. Optional literature grounding using `modules/literature_grounding/LG00_literature_grounding_protocol.md` through `LG06_grounded_pipeline_integration.md`.
3. `02 Domain Scan` using `modules/02_domain_scan.md`.
4. `03 Problem Identification` using `modules/03_problem_identification.md`.
5. `04 Theoretical Positioning` using `modules/04_theoretical_positioning.md`.
6. `05 Contribution Argumentation` using `modules/05_contribution_argumentation.md`.
7. `06 Chain Consistency Audit` using `modules/06_chain_consistency_audit.md`.
8. `07 Final Topic Package` using `modules/07_final_topic_package.md`.
9. Optional manuscript grounding using `modules/manuscript_grounding/MG00_manuscript_grounding_protocol.md` through `MG12_grounded_pipeline_integration.md`.

Always read `modules/00_global_protocol.md` before running any module.

## Run Modes

### Mode A: logic-only mode

Use when the user has not provided real literature evidence. Keep the v0.1.0 logic chain. All judgments about existing research, research gaps, novelty, or baseline sufficiency must be marked `needs_literature_verification`. Do not claim a real gap is proven.

### Mode B: literature-grounded mode

Use when the user provides real literature data. Build paper cards, literature matrix, evidence claim map, and gap audit. Important claims in domain scan, problem identification, theoretical positioning, contribution argumentation, audit, and final topic package must link to `evidence_id` or be marked `ungrounded` / `needs_literature_verification`. Gap and novelty judgments are corpus-scoped unless the user provides systematic-review evidence.

### Mode C: experiment-grounded mode

Use when the user already has a contribution chain, or has completed the v0.1/v0.2 topic-selection chain. Generate validation targets, experiment designs, baseline plans, metric plans, ablation plans, case-study plans, statistical analysis plans, reproducibility requirements, and validation adequacy audits. Do not generate fake experimental results. Do not claim the method has already beaten a baseline. Every contribution claim must map to an experiment validation plan.

In this mode the chain is:

```text
contribution claim
-> validation objective
-> validation question
-> hypothesis
-> baseline set
-> metric set
-> ablation set
-> case study / dataset
-> statistical analysis
-> expected evidence threshold
-> artifact requirement
-> validation adequacy audit
-> reviewer defense
```

Allowed `validation_status` values are `validation_planned`, `partially_planned`, `insufficiently_planned`, `unsupported_by_experiment_plan`, `not_applicable`, and `requires_empirical_results`.

Allowed `experiment_support_status` values are `directly_tested_by_plan`, `indirectly_tested_by_plan`, `weakly_tested_by_plan`, `not_tested`, `requires_new_experiment`, and `cannot_be_validated_empirically`.

Allowed `experiment_risk_level` values are `low`, `medium`, `high`, and `critical`.

Allowed `validation_claim_type` values are `model_validity_claim`, `algorithm_effectiveness_claim`, `mechanism_necessity_claim`, `tradeoff_insight_claim`, `robustness_claim`, `scalability_claim`, `feasibility_claim`, `runtime_claim`, `constraint_handling_claim`, `pareto_quality_claim`, `engineering_value_claim`, `benchmark_claim`, and `reproducibility_claim`.

### Mode D: manuscript-grounded mode

Use when the user has a topic package, literature grounding, experiment validation plan, or draft manuscript structure and needs grounded writing support. Generate a manuscript blueprint, section argument map, paragraph claim plan, citation requirement map, result placeholder map, method and experiment section alignment, limitations plan, reviewer objection map, reviewer response strategy, manuscript adequacy audit, and manuscript traceability report.

Do not generate final manuscript prose. Do not invent citations, DOI values, author-year references, numerical results, p-values, or received reviewer comments. Every manuscript claim must be marked with claim status and safety level.

Allowed `manuscript_claim_status` values are `planned`, `evidence_supported`, `citation_required`, `experiment_result_required`, `partially_supported`, `unsupported`, `unsafe_until_verified`, and `not_applicable`.

Allowed `claim_safety_level` values are `safe`, `needs_citation`, `needs_experiment_result`, `corpus_scoped_only`, `overclaim_risk`, and `unsafe_until_verified`.

Allowed `section_role` values are `background_motivation`, `literature_positioning`, `gap_establishment`, `problem_statement`, `theory_framing`, `contribution_summary`, `method_rationale`, `algorithm_description`, `model_formulation`, `experimental_validation`, `result_interpretation`, `limitation_discussion`, `reviewer_risk_defense`, and `conclusion_synthesis`.

Allowed `paragraph_role` values are `context_setting`, `known_stream_summary`, `contrast_between_streams`, `gap_claim`, `problem_formulation`, `theoretical_positioning`, `contribution_claim`, `design_rationale`, `validation_setup`, `evidence_interpretation`, `limitation_statement`, `transition`, and `reviewer_preemption`.

Allowed `citation_requirement_type` values are `background_citation`, `domain_importance_citation`, `method_stream_citation`, `limitation_support_citation`, `gap_support_citation`, `baseline_support_citation`, `metric_support_citation`, `theory_support_citation`, `validation_protocol_citation`, and `counterevidence_citation`.

Allowed `result_placeholder_type` values are `baseline_comparison_result`, `pareto_quality_result`, `feasibility_result`, `runtime_result`, `ablation_result`, `sensitivity_result`, `statistical_test_result`, `case_study_result`, `reproducibility_artifact_result`, and `qualitative_interpretation_result`.

## Fixed Reasoning Chain

Maintain this chain explicitly:

Logic-only mode starts at `domain facts`. Literature-grounded mode prepends the literature chain:

```text
literature evidence
-> bibliographic record
-> paper card
-> extracted evidence claim
-> literature matrix
-> domain fact
-> domain structure
-> research tension
-> research gap
-> research problem
-> theoretical positioning
-> method requirement
-> contribution claim
-> validation evidence
-> reviewer perception
```

Experiment-grounded mode extends the end of the chain:

```text
contribution claim
-> validation target
-> experiment design
-> baseline selection
-> metric selection
-> ablation design
-> case study / dataset plan
-> statistical analysis plan
-> reproducibility plan
-> validation adequacy audit
-> final topic package validation section
```

Manuscript-grounded mode extends the end of the chain:

```text
final topic package
-> manuscript blueprint
-> section argument map
-> paragraph claim plan
-> citation requirement map
-> result placeholder map
-> method section alignment
-> experiment section alignment
-> discussion limitations plan
-> reviewer objection map
-> reviewer response strategy
-> manuscript adequacy audit
-> contribution-to-manuscript traceability report
```

## Global Operating Rules

- Each module output must become the next module input.
- Each module must persist `input.json`, `output.json`, `output.md`, `next_input.json`, and `validation_report.md`.
- Each module must produce both human-readable Markdown and machine-verifiable JSON.
- Downstream modules may read only the direct upstream module's `next_input.json`.
- Do not pass full upstream `output.json` files downstream.
- Do not depend on hidden reasoning, unsaved drafts, or unstructured temporary notes.
- Every substantive claim must include `evidence_status`.
- Allowed `evidence_status` values are `verified`, `user_provided`, `inferred`, `needs_literature_verification`, and `speculative`.
- Allowed `grounding_status` values are `grounded`, `partially_grounded`, `ungrounded`, `contradicted`, `needs_literature_verification`, and `corpus_scoped_only`.
- Allowed `support_strength` values are `direct`, `indirect`, `weak`, `contradictory`, `contextual`, and `not_applicable`.
- Allowed `claim_type` values are `bibliographic_fact`, `domain_fact`, `method_classification`, `objective_classification`, `constraint_classification`, `limitation_claim`, `gap_claim`, `problem_importance_claim`, `theory_positioning_claim`, `contribution_claim`, `validation_requirement`, `baseline_requirement`, and `reviewer_risk_claim`.
- Include `uncertainty_log`, `reviewer_risks`, `revision_hooks`, and `trace_context` in every `output.json`.
- Support resume from any module through saved direct-upstream `next_input.json`.
- Support local reruns without forcing all upstream modules to rerun.
- Preserve traceability from `domain_tension_id` to `problem_id`, `theory_element_id`, and `contribution_id`.

## Module Output Contract

Every module `output.json` must include:

- `status`
- `module_id`
- `module_name`
- `input_summary`
- `structured_output`
- `next_input`
- `assumptions`
- `uncertainty_log`
- `evidence_requirements`
- `reviewer_risks`
- `revision_hooks`
- `trace_context`

In literature-grounded mode, every module `output.json` must also include or explicitly justify absence of:

- `evidence_links`
- `grounded_claims`
- `grounding_summary`
- `corpus_scope`
- `counterevidence`
- `claim_grounding_risks`

In experiment-grounded mode, module outputs and compact contexts may include:

- `validation_targets`
- `experiment_links`
- `baseline_links`
- `metric_links`
- `ablation_links`
- `statistical_test_links`
- `reproducibility_requirements`
- `validation_adequacy_summary`
- `experiment_risks`
- `artifact_requirements`

In manuscript-grounded mode, module outputs and compact contexts may include:

- `manuscript_blueprint`
- `section_argument_map`
- `paragraph_claim_plan`
- `citation_requirement_map`
- `result_placeholder_map`
- `method_section_alignment`
- `experiment_section_alignment`
- `discussion_limitations_plan`
- `reviewer_objection_map`
- `reviewer_response_strategy`
- `manuscript_adequacy_audit`
- `contribution_to_manuscript_traceability_table`

Every module directory in a workspace must include:

- `input.json`
- `output.json`
- `output.md`
- `next_input.json`
- `validation_report.md`

## Claim Safety

Reject or rewrite unsupported strong claims. Prefer safer wording such as:

- `a structure-aware framework`
- `a joint modeling perspective`
- `a problem-guided evolutionary optimization approach`
- `an empirical analysis of aerodynamic-electrical-economic trade-offs`
- `a candidate framework requiring literature verification`

If real literature evidence is unavailable, mark literature-related judgments as `needs_literature_verification`. If a statement is only a design idea, mark it as `speculative`.

## Novelty Safety

- `first`, `novel`, `state-of-the-art`, `unprecedented`, and equivalent strong wording are unsafe by default.
- Without a user-provided systematic review and explicit search strategy, corpus absence only supports corpus-scoped wording.
- `corpus_scoped_only` does not mean field-proven.
- Never treat absence of evidence as evidence of absence.
- Never use title keyword matching as sufficient evidence for a paper's method, baseline, metric, result, or contribution.

## Final Topic Package Literature Requirements

In literature-grounded mode, the final topic package must include:

- `Literature Evidence Summary`
- `Corpus Scope`
- `Evidence-Backed Domain Gap`
- `Evidence-Backed Problem Statement`
- `Evidence-Backed Contribution Claims`
- `Counterevidence and Risks`
- `Claims Requiring Further Literature Verification`
- `Evidence Traceability Table`

Each evidence traceability row must include `final_claim_id`, `final_claim_text`, `claim_type`, `claim_scope`, `grounding_status`, `support_strength`, `linked_paper_ids`, `linked_evidence_ids`, `linked_problem_id`, `linked_contribution_id`, `counterevidence`, and `safer_wording`.

## Final Topic Package Experiment Requirements

In experiment-grounded mode, the final topic package must include:

- `Experiment-Grounded Validation Plan`
- `Contribution-to-Experiment Traceability Table`
- `Baseline Justification`
- `Metric Justification`
- `Ablation Study Plan`
- `Statistical Analysis Plan`
- `Reproducibility Checklist`
- `Reviewer Validation Risks`
- `Claims Not Yet Experimentally Supported`

Each Contribution-to-Experiment Traceability row must include `contribution_id`, `contribution_claim`, `validation_target_id`, `experiment_id`, `baseline_ids`, `metric_ids`, `ablation_ids`, `statistical_test_ids`, `artifact_ids`, `success_condition`, `failure_condition`, `reviewer_risk`, and `validation_status`.

Every contribution claim must link to at least one validation objective, one baseline or explicit no-baseline justification, one metric, one experiment design, one evidence threshold, one reviewer risk, and one artifact requirement. Algorithmic contributions also need ablation plans. Multi-objective claims need Pareto metric plans. Constrained optimization claims need feasibility and violation analysis. Joint layout-cabling claims need a sequential or decoupled baseline unless explicitly justified.

## Final Topic Package Manuscript Requirements

In manuscript-grounded mode, complete-chain acceptance requires:

- `Manuscript Blueprint`
- `Section Argument Map`
- `Paragraph Claim Plan`
- `Citation Requirement Map`
- `Result Placeholder Map`
- `Discussion Limitations Plan`
- `Reviewer Objection Map`
- `Reviewer Response Strategy`
- `Contribution-to-Manuscript Traceability Table`
- `Claims Not Ready for Manuscript`

Draft or demo workspaces may pass normal strict plan validation, but must fail `audit_manuscript_claims.py --strict --require-complete-manuscript-chain` until a real final topic package, verified citation links, and real result evidence exist.

## Manuscript Safety Boundaries

- v0.4.0 plans manuscript structure; it does not write a final paper.
- v0.4.0 does not fabricate citations, DOI values, author-year references, numerical results, p-values, or reviewer comments.
- Citation requirements are not citations.
- Result placeholders are not results.
- Anticipated reviewer objections are not received reviewer comments.
- Introduction must connect background, streams, gap, problem, contribution, and validation preview.
- Related Work must be stream-based and evidence-bound, not bibliography dumping.
- Method sections must link mechanisms to problem properties and ablation requirements.
- Experiment sections must link claims to validation targets, baselines, metrics, ablations, statistics, and artifacts.
- Discussion must surface limitations, counterevidence, and generalization boundaries.

## Experiment Safety Boundaries

- v0.3.0 only plans experiments; it does not run experiments.
- v0.3.0 does not fabricate experimental results, numeric outcomes, p-values, runtime values, convergence curves, rankings, or significance conclusions.
- `expected_result_pattern` must be conditional and must not be written as an observed result.
- Do not claim `outperform`, statistical significance, or empirical superiority before real experiments exist.
- Do not use weak baselines to make a contribution look stronger.
- Do not allow algorithmic contributions without ablation plans.
- Do not guarantee that a planned experiment will succeed or replace a real optimization platform.

## Literature Safety Boundaries

- Do not automatically fabricate literature.
- Do not claim full-field search is complete.
- Do not treat synthetic examples as real evidence.
- Do not treat bibliographic records or title keywords as sufficient claim support.
- Do not hide counterevidence.

## Reviewer-Risk Checks

Every important output must answer:

- Why is the problem important?
- Why is the proposed method necessary?
- What is new beyond combining existing models?
- Are the baselines sufficient?
- Are the claims supported by planned evidence?
- Is this more than applying an evolutionary algorithm to a wind farm problem?

## Resources

- `modules/`: module-level execution protocols and boundaries.
- `schemas/`: JSON Schema contracts for `output.json`.
- `templates/`: Markdown templates for `output.md`.
- `scripts/`: workspace initialization, validation, and resume tooling.
- `examples/`: input and output examples that avoid fabricated literature.
- `tests/`: pytest contract tests.
- `workspaces/`: generated project runs; do not treat generated workspaces as skill source.
