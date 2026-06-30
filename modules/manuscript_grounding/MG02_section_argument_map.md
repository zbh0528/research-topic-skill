# Section Argument Map

Checks whether Introduction, Related Work, Method, Experiments, Discussion, and Conclusion each have an explicit argument chain.

Inputs: project workspace, optional literature evidence, optional experiment validation plan, and final topic package when real.

Outputs: structured JSON plus Markdown mirrors under `manuscript_grounding/`.

Hard stop: do not generate final manuscript prose, fake citations, fake experiment results, or fabricated reviewer comments.
