# Validation Policy

## Validation Target Definition
Each validation target must include `validation_target_id`, `linked_contribution_id`, `linked_claim_id`, `validation_question`, `hypothesis`, `validation_claim_type`, `required_evidence`, `experiment_support_status`, `validation_status`, `reviewer_risk`, `failure_condition`, `success_condition`, and `evidence_threshold`.

## Baseline Adequacy Policy
A sufficient baseline plan should cover standard algorithm baselines, problem-specific baselines, sequential or decoupled baselines for joint optimization claims, ablated variants for algorithmic mechanisms, literature-supported baselines when v0.2 evidence indicates one, and simple sanity baselines where useful.

Every baseline needs `why_needed`, linked contribution/question fields, fairness requirements, implementation requirements, expected role, and risk if missing. Weak baselines must not be used to package a contribution as stronger than it is.

## Metric Adequacy Policy
Metrics must cover objective quality, constraint feasibility, runtime or computational budget, Pareto quality for multi-objective claims, engineering cost or energy relevance, robustness or sensitivity when claimed, and statistical comparison.

Every metric must link to a claim or validation target and include an interpretation rule, failure pattern, and limitations.

## Ablation Adequacy Policy
Every claimed mechanism must have a corresponding ablation. The ablation should keep other conditions fixed and must include `linked_contribution_id` and `linked_mechanism_id`. An algorithmic contribution without ablation is high risk.

## Statistical Adequacy Policy
Plans for stochastic algorithm comparison must specify independent runs, random seeds, appropriate nonparametric tests when warranted, multiple-comparison correction when many algorithms are compared, effect size or confidence intervals where appropriate, and no significance claim before real results.

## Reproducibility Policy
The plan must specify parameter settings, code availability expectations, hardware/software environment, random seeds, data or case-study descriptions, termination criterion, computational budget, result schema, experiment logs, and artifact checklist.

## No Fabricated Result Policy
The planning layer must not pretend experiments were run. It must not make numeric claims, claim significance, claim superiority, rank algorithms, write fake p-values, or present conditional expectations as observed outcomes.

## Reviewer Defense Policy
Each validation plan must answer:

- Is the baseline fair?
- Are metrics aligned with the claim?
- Are ablations sufficient?
- Are constraints handled explicitly?
- Is the comparison computationally fair?
- Are stochastic effects handled?
- Are case studies representative?
- Are engineering trade-offs interpretable?

If any answer is missing, the plan should be revised before the contribution is used in a final topic package.

## Manuscript Grounding Policy

Every manuscript plan must separate planning artifacts from final manuscript evidence. A paragraph claim may be `planned`, `citation_required`, or `experiment_result_required`, but it must not be written as supported unless the required citation or result evidence exists.

Required manuscript checks:

- Introduction has background, streams, gap, problem, contribution, and validation preview.
- Related Work is organized by research stream and limitation.
- Method components link to problem properties, contribution IDs, and ablation needs.
- Experiment-section claims link to validation targets, baselines, metrics, statistics, and artifacts.
- Discussion lists limitations, counterevidence, and generalization boundaries.
- Reviewer objections are anticipated risks only unless real reviewer comments are supplied.
- Complete-chain acceptance requires a Contribution-to-Manuscript Traceability Table.

`audit_manuscript_claims.py --strict` validates the existing manuscript plan. `--require-complete-manuscript-chain` validates release-grade manuscript readiness and should fail draft/demo workspaces with explicit causes.
