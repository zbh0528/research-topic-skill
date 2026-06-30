# Manuscript Grounding Protocol

Defines the v0.4 safety boundary: plan section logic, claim status, citation needs, result placeholders, limitations, and reviewer-risk defenses without drafting a final paper.

Inputs: project workspace, optional literature evidence, optional experiment validation plan, and final topic package when real.

Outputs: structured JSON plus Markdown mirrors under `manuscript_grounding/`.

Hard stop: do not generate final manuscript prose, fake citations, fake experiment results, or fabricated reviewer comments.
