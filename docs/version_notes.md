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
