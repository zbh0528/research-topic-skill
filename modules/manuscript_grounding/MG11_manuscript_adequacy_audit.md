# Manuscript Adequacy Audit

Audits manuscript readiness and fails unsafe claims, missing traceability, fake citations, fake results, and fake reviewer comments.

Inputs: project workspace, optional literature evidence, optional experiment validation plan, and final topic package when real.

Outputs: structured JSON plus Markdown mirrors under `manuscript_grounding/`.

Hard stop: do not generate final manuscript prose, fake citations, fake experiment results, or fabricated reviewer comments.
