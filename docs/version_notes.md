# Version Notes

## v0.1.0

- version: `v0.1.0`
- status: `high-quality initial`
- date: 2026-06-30

## Verified capabilities

- Modular workflow from intake to final topic package.
- Persisted module artifacts: `input.json`, `output.json`, `output.md`, `next_input.json`, and `validation_report.md`.
- Resume support from any module through direct upstream `next_input.json`.
- JSON Schema validation for module outputs.
- Negative validation for missing global fields, invalid evidence status, invalid JSON, unsafe overclaims, and over-coupled `next_input.json`.
- Red-team fixtures for algorithm-first, fake-literature, and overclaim inputs.

## Known limitations

- Demo outputs are acceptance fixtures, not real research conclusions.
- Literature-related judgments remain `needs_literature_verification` unless grounded by real literature search.
- The validator catches common unsafe wording and structural failures; it does not replace expert review.
- No real experiment, baseline, ablation, or citation database is bundled.

## Next target

Build real-literature-grounded topic selection by connecting verified literature notes, citation metadata, and evidence-backed novelty boundaries.

## v0.2.0

- version: `v0.2.0-real-literature-grounded-topic-selection`
- status: `literature-grounded upgrade`
- capability: paper cards, literature matrix, evidence claim map, grounding audit, corpus-scoped gap judgment, stricter novelty safety
- limitation: no automatic systematic review, no external DOI verification, no replacement for human literature reading, synthetic examples are not evidence
- next target: `v0.3.0 experiment-grounded validation planning`

## v0.3.0

- version: `v0.3.0-experiment-grounded-validation-planning`
- status: `experiment-grounded validation planning upgrade`
- new capabilities:
  - validation target extraction
  - contribution-to-experiment mapping
  - baseline adequacy planning
  - metric adequacy planning
  - ablation design
  - case study / dataset planning
  - statistical analysis planning
  - reproducibility checklist
  - validation adequacy audit
- known limitations:
  - does not run experiments
  - does not fabricate results
  - does not verify performance
  - does not replace real optimization code or simulation
  - planned validation still requires implementation and empirical results
- next target: `v0.4.0 manuscript-structure and reviewer-response grounded writing support`

## v0.4.0

- version: `v0.4.0-manuscript-structure-and-reviewer-response-grounded-writing-support`
- status: `manuscript-grounded writing support upgrade`
- new capabilities:
  - manuscript blueprint
  - section argument map
  - paragraph claim plan
  - citation requirement map
  - result placeholder map
  - method section alignment
  - experiment section alignment
  - discussion limitations plan
  - reviewer objection map
  - reviewer response strategy
  - manuscript adequacy audit
  - contribution-to-manuscript traceability
- known limitations:
  - does not generate a final manuscript
  - does not fabricate citations or results
  - does not fabricate reviewer comments
  - citation requirements are not citations
  - result placeholders are not results
  - anticipated objections are not received reviewer comments
- next target: real user manuscript drafting can be added only after verified final topic package, verified citations, and real experiment outputs exist.
