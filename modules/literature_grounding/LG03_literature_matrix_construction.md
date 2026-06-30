# LG03 Literature Matrix Construction

## Module ID
`LG03_literature_matrix_construction`

## Module Name
Literature Matrix Construction

## Purpose
Build a corpus-scoped matrix for streams, methods, objectives, constraints, and coupling dimensions.

## What this module does
- Creates coverage cells with `paper_ids` and `evidence_ids`.
- Identifies underrepresented, saturated, and contradictory cells inside the provided corpus.

## What this module does not do
- It does not turn sparse corpus coverage into a field-wide gap.

## Required input
`literature_evidence/paper_cards.json`.

## Required output files
- `literature_evidence/literature_matrix.json`
- `literature_evidence/literature_matrix.md`

## Required structured_output fields
`corpus_id`, `corpus_scope`, `paper_count`, `research_streams`, `method_families`, `problem_dimensions`, `objective_dimensions`, `constraint_dimensions`, `coupling_dimensions`, `evidence_density`, `coverage_map`, `underrepresented_cells`, `saturated_cells`, `contradictory_cells`, `matrix_limitations`.

## Required next_input fields
`coverage_map`, `candidate_underrepresented_cells`, `corpus_scope`.

## Procedure
1. Read paper cards.
2. Populate cells only from explicit card fields and extracted claims.
3. Add `coverage_level` and limitations.
4. Mark empty cells as `empty_in_current_corpus`, not field gaps.

## Quality gates
- Every non-empty cell links evidence IDs.
- Underrepresented cells include corpus scope.

## Common failure modes
- Matrix filled from titles.
- Saturation claimed without density and corpus limitations.

## Evidence requirements
Every cell needs `cell_id`, `dimension_values`, `paper_ids`, `evidence_ids`, `coverage_level`, `grounding_status`, and `limitations`.

## Reviewer-risk requirements
Flag weak matrix density and missing counterevidence.

## Revision hooks
Rebuild matrix when paper cards change.

## Downstream contract
LG04 maps matrix-backed evidence into claims.
