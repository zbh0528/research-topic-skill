# 00 Global Protocol

This file defines mandatory protocol for every module. Treat it as a contract, not background reading.

## Evidence Status Protocol

Use only these `evidence_status` values:

| Value | Meaning | Allowed use |
| --- | --- | --- |
| `verified` | Checked against primary evidence available in the workspace or user-provided source. | Use only when the evidence is inspectable. |
| `user_provided` | Explicitly stated by the user but not independently verified. | Use for user constraints, preferences, or claims. |
| `inferred` | Reasoned from verified or user-provided material. | Include the source fields in `trace_context`. |
| `needs_literature_verification` | Literature-related statement that requires real search or citation checking. | Default for claims about prior work when no real literature evidence is supplied. |
| `speculative` | Candidate idea, possible mechanism, or planning hypothesis. | Use for tentative topic ideas and untested mechanisms. |

Every important claim, gap, problem, theory element, contribution, validation requirement, and reviewer defense must carry an evidence status.

## Claim Safety Protocol

Do not:

- Claim `first`, `novel`, `unprecedented`, `never studied`, `the first framework`, `state-of-the-art`, or `outperforms all` without verified evidence.
- Package ordinary algorithm application as a contribution without a problem-structure argument.
- Package domain common sense as a research gap.
- Write planned experiments as completed results.
- Write literature guesses as facts.
- Fabricate citations, years, journals, DOI, authors, datasets, baselines, or experimental outcomes.

Prefer conservative expressions such as:

- `a structure-aware framework`
- `a joint modeling perspective`
- `a problem-guided evolutionary optimization approach`
- `an empirical analysis of aerodynamic-electrical-economic trade-offs`
- `a candidate framework requiring literature verification`

## Module Output Contract

Each module must save these files:

- `input.json`
- `output.json`
- `output.md`
- `next_input.json`
- `validation_report.md`

Every `output.json` must include:

- `status`
- `module_id`
- `module_name`
- `input_summary`
- `structured_output`
- `next_input`
- `assumptions`
- `uncertainty_log`
- `evidence_requirements`
- `reviewer_risks`
- `revision_hooks`
- `trace_context`

Allowed `status` values:

- `draft`
- `complete`
- `validated`
- `needs_revision`

## Loose Coupling Rule

Downstream modules may only use the direct upstream module's `next_input.json`.

They must not depend on:

- Complete output from earlier upstream modules.
- Unstructured drafts.
- Hidden AI reasoning.
- Unsaved temporary notes.
- Chat-only decisions not written into saved JSON.

`next_input.json` may include compact `trace_context`, but it must not be a full copy of `output.json`.

## Resume Rule

Before running a module, check:

- Whether the direct upstream `next_input.json` exists.
- Whether current `output.json` already exists.
- Whether overwrite is explicitly allowed.
- Whether a new version should be generated.
- Whether `project_state.json` needs an update.

Resume must not force upstream reruns unless upstream evidence changed, upstream schema validation failed, or the direct upstream `next_input.json` is insufficient.

## Chain Integrity Rule

Maintain this traceable chain:

```text
domain facts
-> domain structure
-> research tension
-> research gap
-> research problem
-> theoretical positioning
-> method requirement
-> contribution claim
-> validation evidence
-> reviewer perception
```

Use stable identifiers:

- `domain_tension_id`
- `problem_id`
- `problem_property`
- `theory_element_id`
- `contribution_id`
- `validation_item_id`

## Reviewer Perception Rule

For every major conclusion, ask:

- Why is the problem important?
- Why is the proposed method necessary?
- What is new beyond combining existing models?
- Are the baselines sufficient?
- Are the claims supported by experiments?
- Is this more than applying an evolutionary algorithm to a domain problem?
- Does joint optimization produce different trade-offs than sequential optimization?
- Are the mathematical model and experiments sufficient to support the claims?

Record risks in `reviewer_risks`.

## Revision Hook Rule

Every module must output `revision_hooks` explaining:

- Which field to edit for common user changes.
- Which downstream module is affected.
- Whether upstream rerun is required.
- Which identifiers must remain stable for traceability.
