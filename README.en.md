# windfarm-research-topic-skill

English documentation | 中文文档: [README.md](README.md)

`windfarm-research-topic-skill` is a Codex skill source repository for research-topic construction, evidence-chain auditing, experiment-validation planning, and manuscript-structure planning. It started as a wind farm layout and cable routing optimization skill, and has now become a profile-driven framework that can be packaged as a generic `research-topic-skill`.

Current version: `v0.4.1-generic-profile-packaging`

Released tag:

- `v0.4.0`: manuscript-grounded writing and reviewer-response planning

Current working-tree capabilities:

- Keeps the mature `windfarm-layout-cabling` profile.
- Adds the domain-neutral `generic-research` profile.
- Builds an installable `research-topic-skill` package.
- Supports logic-only, literature-grounded, experiment-grounded, and manuscript-grounded modes.

## 1. Purpose

This project is not a generic prompt and not an automatic paper generator. Its purpose is to make Codex maintain a reviewable, traceable, revisable, and verifiable research reasoning chain:

```text
research context
-> domain structure
-> research tension
-> research gap
-> research problem
-> theoretical positioning
-> contribution claim
-> literature evidence
-> validation plan
-> manuscript structure
-> reviewer-risk defense
```

It helps researchers answer:

- What is the problem structure?
- Is the gap evidence-backed or only guessed?
- Can each contribution be traced to a problem, theory element, and evidence source?
- What baselines, metrics, ablations, statistical tests, and reproducibility artifacts are needed?
- Does each manuscript-level claim have a citation requirement or result placeholder?
- Which reviewer objections are likely, and what response strategy is needed?

It does not replace:

- Real literature search.
- Real citation verification.
- Real experiment execution.
- Real figure generation.
- Real manuscript writing.
- Real reviewer comments.
- Real rebuttal drafting.
- Submission judgment.

## 2. Version Overview

### v0.1.0: modular topic reasoning

Base workflow:

```text
Project Intake
-> Domain Scan
-> Problem Identification
-> Theoretical Positioning
-> Contribution Argumentation
-> Chain Consistency Audit
-> Final Topic Package
```

Core capabilities:

- Workspace initialization.
- Persisted module outputs.
- Loose coupling through `next_input.json`.
- Schema validation.
- Resume support.
- Unsafe novelty and overclaim detection.

### v0.2.0: literature-grounded topic selection

Literature grounding chain:

```text
bibliographic record
-> paper card
-> extracted evidence claim
-> literature matrix
-> evidence claim map
-> literature gap audit
-> corpus-scoped topic decision
```

Core capabilities:

- Accepts JSON, YAML, and BibTeX literature inputs.
- Builds paper cards.
- Builds a literature matrix.
- Builds an evidence claim map.
- Builds a literature gap audit.
- Separates real evidence from synthetic examples.
- Prevents absence of evidence from becoming a field-wide no-one-studied claim.

### v0.3.0: experiment-grounded validation planning

Validation planning chain:

```text
contribution claim
-> validation target
-> experiment design
-> baseline plan
-> metric plan
-> ablation plan
-> case study / dataset plan
-> statistical analysis plan
-> reproducibility plan
-> validation adequacy audit
```

Core capabilities:

- Maps each contribution to validation targets.
- Requires ablations for algorithmic contributions.
- Requires Pareto metrics for multi-objective claims.
- Requires feasibility and violation metrics for constrained optimization claims.
- Requires sequential or decoupled baselines for joint optimization claims.
- Blocks fake results, fake p-values, and unsupported outperform claims.

### v0.4.0: manuscript-grounded writing support

Manuscript grounding chain:

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
-> contribution-to-manuscript traceability table
```

Core capabilities:

- Maps topic logic into manuscript structure.
- Maps contributions into manuscript claims.
- Maps manuscript claims into sections and paragraphs.
- Generates citation requirements, not fabricated citations.
- Generates result placeholders, not fabricated results.
- Generates anticipated reviewer objections, not fabricated real reviewer comments.
- Audits Introduction, Related Work, Method, Experiment, and Discussion chains.

### v0.4.1: generic profile packaging

Generic packaging layer:

- `profiles/generic-research/profile.json`
- `profiles/windfarm-layout-cabling/profile.json`
- `profiles/profile.schema.json`
- `scripts/validate_profiles.py`
- `scripts/build_skill_package.py`

The repository remains the mature windfarm source implementation while producing an installable generic `research-topic-skill`.

## 3. Operating Modes

### 3.1 Logic-only mode

Use when:

- The user has only an initial idea.
- No real literature is provided.
- No experiment platform or result exists.

Output behavior:

- Produces a topic reasoning chain.
- Marks literature-related judgments as `needs_literature_verification`.
- Does not claim a real gap, real novelty, or field-wide conclusion.

### 3.2 Literature-grounded mode

Use when:

- The user provides literature records, BibTeX, paper notes, or structured evidence.
- The task is to judge whether a gap or contribution has corpus-level support.

Output behavior:

- Produces `literature_evidence/` artifacts.
- Requires every grounded claim to link to `evidence_id`.
- Keeps gap claims corpus-scoped by default.
- Treats synthetic literature only as a structure example.

### 3.3 Experiment-grounded mode

Use when:

- A contribution chain exists.
- The task is to design reviewer-credible validation.

Output behavior:

- Produces `experiment_validation/` artifacts.
- Maps every contribution to a validation target.
- Makes baselines, metrics, ablations, statistics, and reproducibility artifacts traceable.
- Does not generate experiment results or performance claims.

### 3.4 Manuscript-grounded mode

Use when:

- A final topic package or draft manuscript structure exists.
- The task is to map the topic chain into manuscript structure.
- Reviewer-risk planning is needed.

Output behavior:

- Produces `manuscript_grounding/` artifacts.
- Requires each paragraph claim to have `manuscript_claim_status` and `claim_safety_level`.
- Treats citation requirements as requirements, not citations.
- Treats result placeholders as placeholders, not results.
- Treats anticipated reviewer objections as risks, not received reviewer comments.

## 4. Profiles

Profiles isolate domain knowledge so that domain terms, baselines, metrics, and reviewer risks do not leak into the generic core.

Current profiles:

| profile_id | Purpose |
| --- | --- |
| `generic-research` | Domain-neutral default profile for technical research topics |
| `windfarm-layout-cabling` | Mature profile for wind farm layout and cabling optimization |

Profile files:

```text
profiles/
  profile.schema.json
  generic-research/
    profile.json
  windfarm-layout-cabling/
    profile.json
```

Each profile contains:

- `domain_terms`
- `problem_structures`
- `method_families`
- `baseline_families`
- `metric_families`
- `reviewer_risks`
- `claim_boundaries`

For a new domain, add a profile first. Do not fork the core schemas unless the generic contract is truly insufficient.

## 5. Repository Structure

```text
windfarm-research-topic-skill/
  SKILL.md
  README.md
  README.en.md
  skill_manifest.json
  modules/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  schemas/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  templates/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  profiles/
    generic-research/
    windfarm-layout-cabling/
  scripts/
  examples/
    literature/
    experiment/
    manuscript/
  tests/
  workspaces/
    .gitkeep
```

`workspaces/` is a runtime output directory. Real run workspaces must not be committed. The source repository keeps only `workspaces/.gitkeep`.

## 6. Packaging and Installation

### 6.1 Build the generic skill package

```bash
cd /Users/zbh0528/Documents/windfarm-research-topic-skill

python3 scripts/validate_profiles.py
python3 scripts/build_skill_package.py \
  --output /private/tmp/windfarm_skill_package \
  --overwrite
```

Output:

```text
/private/tmp/windfarm_skill_package/research-topic-skill/
```

The packaging script:

- Rewrites the `SKILL.md` frontmatter name to `research-topic-skill`.
- Rewrites `skill_manifest.json` name to `research-topic-skill`.
- Preserves `source_skill_name: windfarm-research-topic-skill`.
- Copies profiles, modules, schemas, templates, scripts, examples, and docs.
- Excludes runtime `workspaces/` artifacts.

### 6.2 Install into Codex

```bash
cp -R /private/tmp/windfarm_skill_package/research-topic-skill \
  /Users/zbh0528/.codex/skills/

python3 /Users/zbh0528/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/zbh0528/.codex/skills/research-topic-skill
```

Restart Codex after installation so that the skill index is refreshed.

## 7. Quick Usage

### 7.1 Use from Codex chat

Generic research topic:

```text
Use research-topic-skill to create a reviewable research topic package.
profile: generic-research
domain: multi-objective optimization
materials: ...
Requirements:
1. Do not fabricate citations.
2. Do not fabricate results.
3. Do not fabricate reviewer comments.
4. Make every claim traceable.
5. End with validation and manuscript grounding audits.
```

Wind farm layout and cabling:

```text
Use the windfarm-layout-cabling profile from research-topic-skill
to build a research topic package for joint wind farm layout and cable routing optimization.
Do not invent literature, experiment results, novelty claims, or reviewer comments.
```

### 7.2 Initialize a workspace manually

```bash
python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id demo_project \
  --overwrite
```

Validate the base workspace:

```bash
python3 scripts/validate_outputs.py \
  --workspace workspaces/demo_project
```

## 8. Literature Grounding Workflow

```bash
python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id lit_demo \
  --overwrite

python3 scripts/ingest_literature.py \
  --workspace workspaces/lit_demo \
  --input examples/literature/sample_literature_input.json \
  --corpus-id lit_demo_synthetic_corpus \
  --overwrite

python3 scripts/build_literature_matrix.py \
  --workspace workspaces/lit_demo \
  --overwrite

python3 scripts/validate_literature.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/lit_demo \
  --strict
```

Complete-chain acceptance:

```bash
python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/lit_demo \
  --strict \
  --require-complete-chain
```

Notes:

- Plain `--strict` audits existing structured claims.
- `--require-complete-chain` requires a real final topic package and complete evidence traceability.
- Demo or draft workspaces are expected to fail complete-chain mode.

## 9. Experiment Validation Planning Workflow

```bash
python3 scripts/build_validation_plan.py \
  --workspace workspaces/lit_demo \
  --overwrite \
  --demo-if-missing

python3 scripts/validate_experiment_plan.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_validation_adequacy.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/generate_reproducibility_checklist.py \
  --workspace workspaces/lit_demo
```

Notes:

- The output is a validation plan, not experiment results.
- `expected_result_pattern` must remain conditional.
- Unsupported `outperforms`, `p < 0.05`, and `statistically significant` wording is forbidden.

## 10. Manuscript Grounding Workflow

```bash
python3 scripts/build_manuscript_blueprint.py \
  --workspace workspaces/lit_demo \
  --overwrite \
  --demo-if-missing

python3 scripts/validate_manuscript_plan.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/generate_reviewer_response_plan.py \
  --workspace workspaces/lit_demo \
  --overwrite

python3 scripts/generate_manuscript_checklist.py \
  --workspace workspaces/lit_demo
```

Complete manuscript-chain acceptance:

```bash
python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/lit_demo \
  --strict \
  --require-complete-manuscript-chain
```

Notes:

- Plain `--strict` audits the existing manuscript plan for fake citations, fake results, unsupported claims, and related risks.
- `--require-complete-manuscript-chain` requires a real final topic package, non-demo manuscript blueprint, complete traceability table, and real result evidence.
- Demo or draft workspaces are expected to fail complete-chain mode.

## 11. Full Acceptance Commands

```bash
python3 scripts/validate_outputs.py \
  --workspace workspaces/lit_demo \
  --literature-grounded \
  --strict-evidence \
  --experiment-grounded \
  --strict-validation \
  --manuscript-grounded \
  --strict-manuscript
```

Full test suite:

```bash
python3 -m pytest tests -q -ra
```

Profile and package checks:

```bash
python3 scripts/validate_profiles.py
python3 scripts/build_skill_package.py \
  --output /private/tmp/windfarm_skill_package \
  --overwrite
```

## 12. Output Artifacts

Base modules:

```text
00_project_intake/
01_domain_scan/
02_problem_identification/
03_theoretical_positioning/
04_contribution_argumentation/
05_chain_consistency_audit/
06_final_topic_package/
```

Each module directory contains:

```text
input.json
output.json
output.md
next_input.json
validation_report.md
```

Literature grounding:

```text
literature_evidence/
  bibliographic_records.json
  paper_cards.json
  literature_matrix.json
  evidence_claim_map.json
  literature_gap_audit.json
  literature_grounding_report.json
```

Experiment grounding:

```text
experiment_validation/
  validation_targets.json
  experiment_design.json
  baseline_plan.json
  metric_plan.json
  ablation_plan.json
  case_study_plan.json
  statistical_analysis_plan.json
  reproducibility_plan.json
  experiment_grounding_report.json
```

Manuscript grounding:

```text
manuscript_grounding/
  manuscript_blueprint.json
  section_argument_map.json
  paragraph_claim_plan.json
  citation_requirement_map.json
  result_placeholder_map.json
  method_section_alignment.json
  experiment_section_alignment.json
  discussion_limitations_plan.json
  reviewer_objection_map.json
  reviewer_response_strategy.json
  manuscript_adequacy_audit.json
  manuscript_grounding_report.json
```

## 13. Safety Boundaries

Forbidden:

- Fabricating authors, years, venues, DOI values, or citations.
- Fabricating experiment results, p-values, runtime values, rankings, or significance conclusions.
- Treating synthetic evidence as real field evidence.
- Treating a result placeholder as an observed result.
- Treating an anticipated reviewer objection as a received reviewer comment.
- Turning a corpus-scoped gap into a field-wide no-one-studied claim.
- Packaging ordinary algorithm application as a contribution.
- Using `first`, `novel`, `state-of-the-art`, or `outperforms all` without a complete evidence chain.

Allowed:

- Marking `needs_literature_verification`.
- Marking `requires_empirical_results`.
- Generating citation requirements.
- Generating result placeholders.
- Generating anticipated reviewer objections.
- Generating reviewer response strategy plans.
- Generating manuscript adequacy audits.

## 14. Quality Gates

Before release:

```bash
python3 -m pytest tests -q -ra
python3 scripts/validate_profiles.py
find workspaces -maxdepth 2 -type f | sort
```

Expected `workspaces/` output:

```text
workspaces/.gitkeep
```

For real projects, also run:

```bash
python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/<project> \
  --strict \
  --require-complete-chain

python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/<project> \
  --strict \
  --require-complete-manuscript-chain
```

## 15. Maintenance Principles

- Keep the core profile-neutral.
- Put domain knowledge into `profiles/`.
- Add a profile before forking schemas.
- Label synthetic example data explicitly.
- Do not commit runtime workspaces.
- Use README for users and maintainers; use SKILL.md for Codex runtime behavior.
- Do not turn v0.5.0 into an automatic full-paper generator. A better direction is a human-in-the-loop manuscript drafting and revision workflow.

## 16. Current Status

Completed:

- `v0.4.0` manuscript-grounded high-quality initial release.
- `v0.4.1` generic profile packaging.
- Package generation and local installation validation.

Boundary:

```text
research-topic-skill = generic research-topic evidence-chain framework
windfarm-research-topic-skill = mature source implementation and profile for wind farm layout/cabling
```
