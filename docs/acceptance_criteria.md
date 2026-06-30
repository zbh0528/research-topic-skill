# Acceptance Criteria

This file records acceptance gates for `windfarm-research-topic-skill`.

## Engineering gates

- `python3 -m pytest tests` must pass.
- `init_workspace.py` must create every module directory and the five persisted module files.
- `resume_from_module.py` must rebuild a target module input from the direct upstream `next_input.json`.
- `validate_outputs.py` must write `validation_summary.md` and per-module `validation_report.md`.
- Draft workspace warnings are acceptable only for generated placeholder modules. Validated semantic or red-team cases should have `fail_count: 0`.

## Schema negative gates

Validation must fail when:

- `reviewer_risks` is missing.
- `trace_context` is missing.
- `evidence_status` is outside the allowed enum.
- `next_input.json` is empty or invalid JSON.
- `output.json` is invalid JSON.
- A contribution claim uses unsupported strong wording such as `the first state-of-the-art framework`.
- `next_input.json` is a copied full `output.json`.

## Loose-coupling gate

Downstream modules may read only the direct upstream `next_input.json`.

The sentinel test must show that a value present only in upstream `output.json` does not appear in the downstream `input.json`, while a value present in upstream `next_input.json` does.

## Research semantic scoring

Score final semantic outputs from 0 to 5 on:

- Domain scan depth.
- Problem identification quality.
- Theoretical positioning specificity.
- Problem-property-to-method-implication logic.
- Contribution traceability.
- Evidence discipline.
- Reviewer-risk quality.
- Validation plan adequacy.
- Modularity and resume support.
- Resistance to algorithm wrapping.

Average score must be at least 4.0 for a high-quality initial version.

## Veto conditions

Any one of these blocks acceptance:

- Fabricated literature, authors, years, journals, DOI, experiments, or results.
- Unsupported `first`, `novel`, `state-of-the-art`, or equivalent novelty/performance claims.
- Treating "use a certain algorithm" as the research problem.
- Contributions that cannot be traced to problem and theory identifiers.
- Missing validation plan in the final topic package.
- Theory positioning that is only labels and does not derive method implications.

## v0.2.0 Engineering Gates

- New literature scripts run: `ingest_literature.py`, `validate_literature.py`, `build_literature_matrix.py`, and `audit_claim_grounding.py`.
- New literature schemas validate generated sample outputs.
- Existing v0.1.0 tests still pass.
- Synthetic literature sample can be ingested without metadata fabrication.
- Literature matrix, evidence claim map, and gap audit can be generated.
- `validate_outputs.py --literature-grounded --strict-evidence` checks evidence context without breaking default logic-only validation.

## v0.2.0 Semantic Gates

- Each grounded domain tension can link `evidence_id`.
- Each selected problem can link `evidence_id`.
- Each contribution claim can link `problem_id`, theory element, and `evidence_id`.
- Gap claims do not treat absence of evidence as evidence of absence.
- Novelty wording is corpus-scoped unless a user-provided systematic review supports stronger scope.
- Counterevidence is not hidden.
- Ungrounded or unsupported verified claims are detected by audit.

## v0.2.0 Veto Conditions

- Fabricated literature.
- Synthetic examples treated as real evidence.
- Unsupported `first`, `novel`, or `state-of-the-art` claims.
- `grounded` claim without `evidence_id`.
- Counterevidence hidden from final topic package.
- Title keywords used as paper contribution evidence.
- Gap claim without `corpus_scope`.
- Contribution claim without evidence link.
- `audit_claim_grounding.py` cannot detect unsupported verified claims.

## v0.3.0 Engineering Gates

- Experiment schemas are legal JSON Schema files.
- Experiment scripts run: `build_validation_plan.py`, `validate_experiment_plan.py`, `audit_validation_adequacy.py`, and `generate_reproducibility_checklist.py`.
- New v0.3.0 tests pass.
- Existing v0.1.0 and v0.2.0 tests still pass.
- Validation plan generation, strict experiment validation, validation adequacy audit, and reproducibility checklist generation all work.

## v0.3.0 Semantic Gates

- Each contribution claim has a validation target.
- Each algorithmic contribution has an ablation plan.
- Each multi-objective claim has a Pareto metric plan.
- Each constrained optimization claim has feasibility and violation metrics.
- Each joint layout-cabling claim has a sequential or decoupled baseline unless justified.
- Each baseline has `why_needed` and fairness requirements.
- Each metric has a linked claim and interpretation rule.
- Each statistical plan has independent runs and test rationale.
- Experiment planning contains no fake results.
- Final topic package has a Contribution-to-Experiment Traceability Table in complete-chain acceptance.

## v0.3.0 Veto Conditions

- Fabricated experimental results.
- `outperform` claims without results.
- Statistical significance claims without experiments.
- Algorithmic contribution without ablation.
- Multi-objective contribution without Pareto metric.
- Constrained contribution without feasibility analysis.
- Joint layout-cabling contribution without sequential or decoupled baseline and without justification.
- Cherry-picked or obviously weak baseline.
- Metric and contribution mismatch.
- Final topic package missing the Contribution-to-Experiment Traceability Table in complete-chain acceptance.
- v0.1.0 or v0.2.0 tests fail.

## v0.4.0 Engineering Gates

- Manuscript schemas are legal JSON Schema files.
- Manuscript scripts run: `build_manuscript_blueprint.py`, `validate_manuscript_plan.py`, `audit_manuscript_claims.py`, `generate_reviewer_response_plan.py`, and `generate_manuscript_checklist.py`.
- New v0.4.0 tests pass.
- Existing v0.1.0, v0.2.0, and v0.3.0 tests still pass.
- `validate_outputs.py --manuscript-grounded --strict-manuscript` works without breaking default validation.

## v0.4.0 Semantic Gates

- Every manuscript claim has `manuscript_claim_status` and `claim_safety_level`.
- Every gap or background claim has citation requirements or verified evidence links.
- Every empirical or effectiveness claim has result placeholders until real results exist.
- Introduction links background, streams, gap, problem, contribution, and validation preview.
- Related Work is organized by research stream and limitation, not citation dumping.
- Method claims link method components to problem properties and ablation requirements.
- Experiment-section claims link to validation targets, baselines, metrics, statistics, and artifacts.
- Discussion exposes limitations, counterevidence, and generalization boundaries.
- High-risk reviewer objections have response strategies.
- Complete-chain acceptance has a Contribution-to-Manuscript Traceability Table.

## v0.4.0 Veto Conditions

- Fabricated citations, author-year references, DOI values, numerical results, p-values, or reviewer comments.
- Result placeholders written as observed findings.
- Citation requirements written as real citations.
- Anticipated reviewer objections written as received reviewer comments.
- Unsupported field-wide novelty or performance claims.
- Manuscript claim without traceability.
- Final manuscript generation from draft/demo artifacts.
