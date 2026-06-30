# LG01 Literature Intake

## Module ID
`LG01_literature_intake`

## Module Name
Literature Intake

## Purpose
Convert user-provided literature records into normalized bibliographic records.

## What this module does
- Accept JSON, YAML, BibTeX, CSV, and optional notes.
- Save raw input.
- Assign `paper_id`.
- Record missing metadata.

## What this module does not do
- It does not complete authors, years, venues, DOI, abstracts, or results.
- It does not infer contribution from title.

## Required input
User-provided literature file.

## Required output files
- `literature_evidence/raw/*`
- `literature_evidence/bibliographic_records.json`
- `literature_evidence/intake_report.md`
- `literature_evidence/validation_report.md`

## Required structured_output fields
`corpus_id`, `corpus_scope`, `input_files`, `bibliographic_records`, `synthetic_records`, `missing_metadata`, `ingestion_warnings`, `evidence_policy`.

## Required next_input fields
`bibliographic_records_path`, `corpus_id`, `corpus_scope`.

## Procedure
1. Parse input format.
2. Assign `P001...`.
3. Normalize required fields with `null` or `[]` for missing values.
4. Preserve extra user fields.
5. Write missing metadata report.

## Quality gates
- Missing DOI remains missing.
- BibTeX parser extracts only fields present in BibTeX.
- Synthetic records retain `is_synthetic: true`.

## Common failure modes
- Silent YAML parse failure.
- Inventing venue from title.
- Treating title list as literature review.

## Evidence requirements
Bibliographic records are not sufficient evidence for complex claims.

## Reviewer-risk requirements
Flag missing metadata and unverified bibliographic facts.

## Revision hooks
When metadata is supplied later, rerun intake with `--overwrite`.

## Downstream contract
LG02 reads normalized records only.
