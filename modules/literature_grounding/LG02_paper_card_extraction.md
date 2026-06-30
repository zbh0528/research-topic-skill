# LG02 Paper Card Extraction

## Module ID
`LG02_paper_card_extraction`

## Module Name
Paper Card Extraction

## Purpose
Create paper cards and extracted claims from user-provided abstracts, notes, or excerpts.

## What this module does
- Builds one `paper_card` per bibliographic record.
- Extracts claims only from `abstract`, `user_notes`, or `relevant_excerpts`.
- Marks title-only records as insufficient for detailed claims.

## What this module does not do
- It does not infer methods, objectives, constraints, or findings from titles.
- It does not treat synthetic records as real evidence.

## Required input
`literature_evidence/bibliographic_records.json`.

## Required output files
- `literature_evidence/paper_cards.json`
- `literature_evidence/paper_cards.md`

## Required structured_output fields
`paper_id`, `bibliographic_metadata`, `source_type`, `is_synthetic`, `research_stream`, `method_family`, `objectives`, `constraints`, `extracted_claims`, `extraction_uncertainty`, `evidence_status`.

## Required next_input fields
`paper_cards_path`, `claim_ids`, `evidence_ids`.

## Procedure
1. Load bibliographic records.
2. Create conservative card fields.
3. Extract only sourced claims.
4. Add `source_field`, `source_excerpt`, `support_strength`, and `grounding_status`.

## Quality gates
- Title-only records produce no detailed extracted claims.
- Synthetic records keep `is_synthetic: true`; `evidence_status=user_provided` only describes source status. Their `grounding_status` must not be treated as real evidence for real research claims.

## Common failure modes
- Keyword matching a title into a method claim.
- Dropping extraction uncertainty.

## Evidence requirements
Each extracted claim needs `claim_id`, `evidence_id`, `paper_id`, `claim_text`, `claim_type`, `source_field`, `source_excerpt`, `evidence_status`, `grounding_status`, `support_strength`, `confidence`, and `limitations`.

## Reviewer-risk requirements
Flag weak excerpts, missing source fields, and synthetic evidence.

## Revision hooks
Re-extract if the user adds abstracts, notes, or excerpts.

## Downstream contract
LG03 uses only paper-card fields and extracted claims.
