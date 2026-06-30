# LG00 Literature Grounding Protocol

## Module ID
`LG00_literature_grounding_protocol`

## Module Name
Literature Grounding Protocol

## Purpose
Define the v0.2.0 evidence layer that feeds compact `evidence_context` into the existing workflow.

## What this module does
- Enables literature-grounded mode only when the user provides literature data.
- Defines `paper_id`, `claim_id`, `evidence_id`, and `gap_id` naming: `P001`, `CL001`, `EV001`, `G001`.
- Defines `evidence_status`, `grounding_status`, `support_strength`, synthetic rules, corpus scope, counterevidence, novelty safety, and title-only prohibition.

## What this module does not do
- It does not search online, read PDFs, OCR files, or complete missing metadata.
- It does not prove field-wide novelty.

## Required input
User-provided JSON, YAML, BibTeX, CSV, Markdown notes, paper cards, abstracts, or excerpts.

## Required output files
- `literature_evidence/bibliographic_records.json`
- `literature_evidence/paper_cards.json`
- `literature_evidence/literature_matrix.json`
- `literature_evidence/evidence_claim_map.json`
- `literature_evidence/literature_gap_audit.json`

## Required structured_output fields
`corpus_id`, `corpus_scope`, `paper_count`, `claim_type_rules`, `grounding_status_rules`, `support_strength_rules`, `novelty_safety_rules`, `counterevidence_policy`, `evidence_context`.

## Required next_input fields
`evidence_context`.

## Procedure
1. Assign stable IDs.
2. Preserve only user-provided metadata.
3. Extract claims only from provided abstract, notes, or excerpts.
4. Build matrix cells only from paper-card claims.
5. Mark gaps as corpus-scoped.
6. Surface counterevidence.
7. Pass compact `evidence_context`.

## Quality gates
- No fabricated literature.
- No title-only method inference.
- No absence-of-evidence fallacy.
- No field-wide novelty claim without systematic review evidence.

## Common failure modes
- Treating bibliography as evidence for complex claims.
- Hiding contradictory evidence.
- Copying whole paper text into `next_input.json`.

## Evidence requirements
Each important claim needs `paper_id`, `claim_id`, `claim_type`, `evidence_id`, `source_field`, `source_excerpt`, `grounding_status`, and `support_strength`.

## Reviewer-risk requirements
Flag unsupported novelty, missing baselines, weak evidence, synthetic misuse, and counterevidence.

## Revision hooks
Revise `corpus_scope`, `gap_candidates`, and `claims_requiring_verification` when new literature is added.

## Downstream contract
Downstream modules read `evidence_context`; they cite `evidence_id` instead of copying full source text.
