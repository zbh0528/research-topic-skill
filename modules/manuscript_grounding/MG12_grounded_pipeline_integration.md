# Grounded Pipeline Integration

Connects v0.1-v0.3 outputs to v0.4 manuscript planning while preserving backward compatibility.

Inputs: project workspace, optional literature evidence, optional experiment validation plan, and final topic package when real.

Outputs: structured JSON plus Markdown mirrors under `manuscript_grounding/`.

Hard stop: do not generate final manuscript prose, fake citations, fake experiment results, or fabricated reviewer comments.
