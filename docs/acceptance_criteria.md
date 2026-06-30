# Acceptance Criteria

This file records the v0.1.0 acceptance gates for `windfarm-research-topic-skill`.

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
