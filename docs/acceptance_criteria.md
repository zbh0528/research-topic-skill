# Acceptance Criteria

This file records v0.1.0 and v0.2.0 acceptance gates for `windfarm-research-topic-skill`.

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
