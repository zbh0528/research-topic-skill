# Experiment Grounding Workflow

## v0.3.0 Goal
v0.3.0 adds a planning layer that maps contribution claims to experiments needed for validation. It does not run experiments and does not report results.

## Why v0.2.0 Is Not Enough
v0.2.0 answers whether a gap or contribution is grounded in a provided literature corpus. It does not answer whether the contribution has fair baselines, aligned metrics, ablations, statistics, reproducibility artifacts, or reviewer defenses.

## Data Flow
```text
contribution claim
-> validation target
-> experiment design
-> baseline plan
-> metric plan
-> ablation plan
-> case study / dataset plan
-> statistical analysis plan
-> reproducibility plan
-> validation adequacy audit
-> final topic package validation section
```

## Inputs, Outputs, and Gates
- Validation target: input is contribution claims; output is `validation_targets.json`; gate is one target per contribution.
- Experiment design: input is validation targets; output is `experiment_design.json`; gate is linked experiment IDs and conditional expected-result wording.
- Baseline plan: input is experiment designs; output is `baseline_plan.json`; gate is `why_needed`, fairness, and no cherry-picking.
- Metric plan: input is claims and experiments; output is `metric_plan.json`; gate is claim-aligned metrics with limitations.
- Ablation plan: input is algorithmic mechanisms; output is `ablation_plan.json`; gate is one ablation per claimed mechanism.
- Case-study plan: input is validation questions; output is `case_study_plan.json`; gate is explicit synthetic/real labeling.
- Statistical plan: input is stochastic comparison needs; output is `statistical_analysis_plan.json`; gate is independent runs, seeds, and test rationale.
- Reproducibility plan: input is experiment design; output is `reproducibility_plan.json`; gate is seeds, parameters, budget, environment, result schema, and artifacts.
- Adequacy audit: input is all plan files; output is `validation_adequacy_audit.json`; gate is no missing critical link.

## Adequacy Rules
Baseline adequacy requires standard algorithm, problem-specific, sequential or decoupled, ablated, literature-supported, and simple sanity baselines where applicable.

Metric adequacy requires objective quality, feasibility, runtime, Pareto quality for multi-objective claims, engineering cost or energy relevance, robustness or sensitivity when claimed, and statistical comparison.

Ablation adequacy requires each claimed mechanism to have a controlled variant with all other conditions held constant.

Statistical adequacy requires independent runs, seed policy, nonparametric tests when appropriate, multiple comparison policy, and no significance claim before real results.

Reproducibility adequacy requires parameter settings, code expectation, hardware/software environment, random seeds, data/case description, termination criterion, computational budget, result schema, and artifact checklist.

## Special Experiment Types
Multi-objective optimization plans should include hypervolume, IGD/IGD+ when a reference front exists, spread/spacing/diversity, feasibility, runtime, statistical tests, and Pareto visualization. If no reference front exists, metric limitations must be stated.

Constrained optimization plans must include feasibility rate, total and maximum violation, violation by constraint type, repair success if a repair mechanism exists, feasible Pareto front comparison, and infeasible-solution handling.

Joint layout-cabling optimization plans must include or justify the absence of layout-only, cabling-only, sequential cabling-after-layout, and existing joint baselines. Metrics should cover aerodynamic, electrical, economic, topology, and feasibility trade-offs.

## Reviewer-Risk-Driven Design
Every plan should answer whether baselines are fair, metrics align with the claim, ablations isolate mechanisms, constraints are explicit, computational budgets are fair, stochastic effects are handled, case studies are representative, and engineering trade-offs are interpretable.

## Anti-Fabrication Rules
Do not write planned experiments as completed results. Do not use numeric claims, p-values, significance, rankings, or `outperform` wording unless real verified experiment outputs exist outside this planning layer.

## Preventing Vague Plans
Reject vague plans that say only "prove effectiveness". A valid plan names the contribution, validation target, experiment, baseline, metric, ablation if needed, statistical test, artifact, success condition, failure condition, and reviewer risk.

## Final Topic Package Injection
`experiment_context` is compact. It contains summaries and IDs only, while detailed plans remain under `workspaces/<project_id>/experiment_validation/`. The final topic package references IDs instead of copying complete plans.
