# Literature Grounding Workflow

## Goal

v0.2.0 upgrades the skill from logic-only topic reasoning to user-provided literature evidence grounding. It does not search the web, read PDFs, or prove field-wide novelty.

## Why v0.1.0 Was Not Enough

v0.1.0 can build a strong reasoning chain, but `semantic_demo` is simulated. It cannot prove a real gap, baseline sufficiency, or contribution novelty without user-provided literature evidence.

## Data Flow

```text
user literature input
-> bibliographic records
-> paper cards
-> extracted claims
-> literature matrix
-> evidence claim map
-> grounded domain tensions
-> grounded problem cards
-> grounded contribution claims
-> final topic package
```

## Step Gates

- Intake: keep only user-provided metadata; never complete missing DOI, author, venue, year, abstract, or result.
- Paper cards: extract claims only from `abstract`, `user_notes`, or `relevant_excerpts`; title-only records create bibliographic facts only.
- Literature matrix: every non-empty cell must link `paper_id` and `evidence_id`; underrepresented cells are corpus-scoped.
- Evidence claim map: every claim must include `claim_type`, `grounding_status`, `support_strength`, `corpus_scope`, and safer wording.
- Gap audit: reject gap claims that only mean "not seen"; record counterevidence and required additional literature.
- Pipeline integration: pass only compact `evidence_context` through `next_input.json`, not full paper text.

## Claim Status Rules

Mark a claim `verified` only when it comes from user-provided real material and has `paper_id`, `claim_id`, and `source_field` or `source_excerpt`.

Mark `needs_literature_verification` when metadata is missing, evidence is title-only, the statement is field-general, or the corpus is too small.

Synthetic examples are structural fixtures only. They must use `is_synthetic: true` and cannot support real research conclusions.

## Counterevidence

If a paper card contradicts a gap, output `counterevidence`, `contradiction_type`, `impact_on_gap`, and `safer_reformulation`. Do not hide contradiction in the final topic package.

## Corpus-Scoped Gaps

Use wording such as `within the provided corpus` or `under the current evidence set`. Do not write `first`, `novel`, `state-of-the-art`, `unprecedented`, or field-wide absence claims without a user-provided systematic review.

## Title-Only Rule

Never infer method family, objectives, constraints, findings, or contribution from title keywords alone.

## Evidence Context Contract

```json
{
  "corpus_id": "...",
  "corpus_scope": "...",
  "paper_count": 0,
  "key_grounded_claims": [],
  "candidate_gap_claims": [],
  "counterevidence_summary": [],
  "claims_requiring_verification": [],
  "evidence_policy": {},
  "trace_context": {}
}
```
