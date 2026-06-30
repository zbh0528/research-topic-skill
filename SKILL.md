---
name: windfarm-research-topic-skill
description: Use when constructing an evidence-bounded research topic package for computer science, evolutionary computation, wind farm layout optimization, wind farm cable routing optimization, joint layout-cabling optimization, multi-objective optimization, constrained optimization, mixed discrete-continuous optimization, or spatial-network coupled optimization. Typical inputs include researcher background, target domain, materials, method preferences, excluded directions, target venue level, literature notes, code or experiment platforms, and constraints. Produces persistent modular outputs through project intake, domain scan, problem identification, theoretical positioning, contribution argumentation, chain audit, and final topic package. Do not use for fabricating papers, literature reviews, citations, experiments, novelty claims, or unsupported conclusions; route real literature review, experiment execution, manuscript drafting, and citation verification elsewhere.
---

# Windfarm Research Topic Skill

## Skill Name

`windfarm-research-topic-skill`

## Version

`v0.2.0-real-literature-grounded-topic-selection`

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

## Do Not Use This Skill For

- Directly fabricating a paper, literature review, citations, DOI, author list, venue, or experiment result.
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

Always read `modules/00_global_protocol.md` before running any module.

## Run Modes

### Mode A: logic-only mode

Use when the user has not provided real literature evidence. Keep the v0.1.0 logic chain. All judgments about existing research, research gaps, novelty, or baseline sufficiency must be marked `needs_literature_verification`. Do not claim a real gap is proven.

### Mode B: literature-grounded mode

Use when the user provides real literature data. Build paper cards, literature matrix, evidence claim map, and gap audit. Important claims in domain scan, problem identification, theoretical positioning, contribution argumentation, audit, and final topic package must link to `evidence_id` or be marked `ungrounded` / `needs_literature_verification`. Gap and novelty judgments are corpus-scoped unless the user provides systematic-review evidence.

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
