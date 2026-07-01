# windfarm-research-topic-skill

中文文档 | English version: [README.en.md](README.en.md)

`windfarm-research-topic-skill` 是一个面向科研选题、证据链审计、实验验证规划和论文结构规划的 Codex skill 源仓库。它最初面向风电场布局优化、风电场布线优化和布局-布线联合优化，当前已经升级为可打包成通用 `research-topic-skill` 的 profile-driven 研究选题框架。

当前版本：`v0.4.1-generic-profile-packaging`

已封版 tag：

- `v0.4.0`：manuscript-grounded writing and reviewer-response planning

当前工作树能力：

- 保留成熟 `windfarm-layout-cabling` profile。
- 新增 `generic-research` 通用 profile。
- 可构建可安装包 `research-topic-skill`。
- 支持 logic-only、literature-grounded、experiment-grounded、manuscript-grounded 四种工作模式。

## 1. 项目定位

这个项目不是普通 prompt，也不是自动论文生成器。它的目标是让 Codex 在研究选题阶段形成一条可审稿、可追踪、可修改、可验证的推理链：

```text
research context
-> domain structure
-> research tension
-> research gap
-> research problem
-> theoretical positioning
-> contribution claim
-> literature evidence
-> validation plan
-> manuscript structure
-> reviewer-risk defense
```

它能帮助研究人员回答：

- 这个方向的问题结构是什么？
- gap 是否只是猜测，还是有文献证据支撑？
- contribution 是否能追踪到 problem、theory 和 evidence？
- 实验需要哪些 baseline、metric、ablation、statistics 和 reproducibility artifact？
- 论文结构中每个 claim 是否有 citation requirement 或 result placeholder？
- reviewer 可能攻击哪些点，response strategy 应该如何规划？

它不会替代：

- 真实文献检索。
- 真实引用核验。
- 真实实验运行。
- 真实图表生成。
- 真实论文写作。
- 真实审稿意见。
- 真实 rebuttal。
- 投稿判断。

## 2. 版本能力概览

### v0.1.0：模块化选题链

建立基础 topic reasoning workflow：

```text
Project Intake
-> Domain Scan
-> Problem Identification
-> Theoretical Positioning
-> Contribution Argumentation
-> Chain Consistency Audit
-> Final Topic Package
```

核心能力：

- workspace 初始化。
- 模块持久化输出。
- `next_input.json` 松耦合传递。
- schema 验证。
- resume 支持。
- unsafe novelty / overclaim 拦截。

### v0.2.0：literature-grounded topic selection

新增文献接地层：

```text
bibliographic record
-> paper card
-> extracted evidence claim
-> literature matrix
-> evidence claim map
-> literature gap audit
-> corpus-scoped topic decision
```

核心能力：

- 支持 JSON、YAML、BibTeX 文献输入。
- 生成 paper cards。
- 生成 literature matrix。
- 生成 evidence claim map。
- 生成 literature gap audit。
- 区分 real evidence 与 synthetic examples。
- 防止把 absence of evidence 写成 field-wide gap。

### v0.3.0：experiment-grounded validation planning

新增实验验证规划层：

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
```

核心能力：

- 为每个 contribution 建立 validation target。
- 为算法性贡献要求 ablation。
- 为多目标贡献要求 Pareto metric。
- 为约束优化贡献要求 feasibility / violation metric。
- 为 joint optimization claim 要求 sequential 或 decoupled baseline。
- 拦截 fake result、fake p-value、unsupported outperform claim。

### v0.4.0：manuscript-grounded writing support

新增论文结构和审稿人回应规划层：

```text
final topic package
-> manuscript blueprint
-> section argument map
-> paragraph claim plan
-> citation requirement map
-> result placeholder map
-> method section alignment
-> experiment section alignment
-> discussion limitations plan
-> reviewer objection map
-> reviewer response strategy
-> manuscript adequacy audit
-> contribution-to-manuscript traceability table
```

核心能力：

- 将 topic logic 映射到论文结构。
- 将 contribution 映射到 manuscript claim。
- 将 manuscript claim 映射到 section 和 paragraph。
- 生成 citation requirement，而不是伪造 citation。
- 生成 result placeholder，而不是伪造 result。
- 生成 anticipated reviewer objection，而不是伪造真实审稿意见。
- 审计 Introduction、Related Work、Method、Experiment、Discussion 的链条完整性。

### v0.4.1：generic profile packaging

新增通用化封装层：

- `profiles/generic-research/profile.json`
- `profiles/windfarm-layout-cabling/profile.json`
- `profiles/profile.schema.json`
- `scripts/validate_profiles.py`
- `scripts/build_skill_package.py`

目标是把本仓库作为成熟 windfarm profile 源仓库，同时生成可安装的通用 `research-topic-skill`。

## 3. 四种运行模式

### 3.1 logic-only mode

适用场景：

- 用户只有初步想法。
- 没有真实文献输入。
- 没有实验平台或实验结果。

输出特点：

- 可以生成 topic reasoning chain。
- 所有文献相关判断必须标记为 `needs_literature_verification`。
- 不允许声明真实 gap、真实 novelty 或真实 field-wide conclusion。

### 3.2 literature-grounded mode

适用场景：

- 用户提供文献表、BibTeX、paper notes 或 structured evidence。
- 需要判断 gap 和 contribution 是否有 corpus-level support。

输出特点：

- 生成 `literature_evidence/` artifacts。
- 每个 grounded claim 必须链接 `evidence_id`。
- gap claim 默认是 corpus-scoped。
- synthetic literature 只能作为结构示例，不能作为真实 field evidence。

### 3.3 experiment-grounded mode

适用场景：

- 已经有 contribution chain。
- 需要设计 reviewer 能接受的验证方案。

输出特点：

- 生成 `experiment_validation/` artifacts。
- 每个 contribution 必须链接 validation target。
- baseline、metric、ablation、statistics、reproducibility requirement 必须可追踪。
- 不生成实验结果，不写 performance claim。

### 3.4 manuscript-grounded mode

适用场景：

- 已有 final topic package 或 draft manuscript structure。
- 准备把选题链条映射到论文结构。
- 需要提前做 reviewer-risk planning。

输出特点：

- 生成 `manuscript_grounding/` artifacts。
- 每个 paragraph claim 必须有 `manuscript_claim_status` 和 `claim_safety_level`。
- citation requirement 不是 citation。
- result placeholder 不是 result。
- anticipated reviewer objection 不是 received reviewer comment。

## 4. Profile 机制

Profile 用来隔离领域知识，避免把某个领域的术语、baseline、metric 和 reviewer risk 写死到通用 core 中。

当前 profile：

| profile_id | 用途 |
| --- | --- |
| `generic-research` | 通用技术研究选题默认 profile |
| `windfarm-layout-cabling` | 风电场布局、布线、布局-布线联合优化成熟 profile |

Profile 文件：

```text
profiles/
  profile.schema.json
  generic-research/
    profile.json
  windfarm-layout-cabling/
    profile.json
```

Profile 包含：

- `domain_terms`
- `problem_structures`
- `method_families`
- `baseline_families`
- `metric_families`
- `reviewer_risks`
- `claim_boundaries`

新增领域时，优先新增 profile，不要改 core schema。

## 5. 目录结构

```text
windfarm-research-topic-skill/
  SKILL.md
  README.md
  README.en.md
  skill_manifest.json
  modules/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  schemas/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  templates/
    literature_grounding/
    experiment_grounding/
    manuscript_grounding/
  profiles/
    generic-research/
    windfarm-layout-cabling/
  scripts/
  examples/
    literature/
    experiment/
    manuscript/
  tests/
  workspaces/
    .gitkeep
```

`workspaces/` 是运行产物目录，不提交真实运行 workspace。源码仓库只保留 `workspaces/.gitkeep`。

## 6. 安装和打包

### 6.1 构建通用 skill 包

```bash
cd /Users/zbh0528/Documents/windfarm-research-topic-skill

python3 scripts/validate_profiles.py
python3 scripts/build_skill_package.py \
  --output /private/tmp/windfarm_skill_package \
  --overwrite
```

输出：

```text
/private/tmp/windfarm_skill_package/research-topic-skill/
```

打包脚本会：

- 将 `SKILL.md` frontmatter name 改为 `research-topic-skill`。
- 将 `skill_manifest.json` 的 `name` 改为 `research-topic-skill`。
- 保留 `source_skill_name: windfarm-research-topic-skill`。
- 复制 profiles、modules、schemas、templates、scripts、examples、docs。
- 排除 `workspaces/` 运行产物。

### 6.2 安装到 Codex 本底

```bash
cp -R /private/tmp/windfarm_skill_package/research-topic-skill \
  /Users/zbh0528/.codex/skills/

python3 /Users/zbh0528/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/zbh0528/.codex/skills/research-topic-skill
```

安装后需要重启 Codex，让 skill index 重新扫描。

## 7. 快速使用

### 7.1 在 Codex 对话中调用

通用研究方向：

```text
请使用 research-topic-skill，为这个研究方向建立一个可审稿的 research topic package。
profile: generic-research
领域: 多目标优化
材料: ...
要求:
1. 不伪造 citation
2. 不伪造 result
3. 不伪造 reviewer comment
4. 所有 claim 必须可追踪
5. 最后输出 validation 和 manuscript grounding audit
```

风电场布局/布线方向：

```text
请使用 research-topic-skill 的 windfarm-layout-cabling profile，
为风电场布局-布线联合优化构建 research topic package。
不要编造文献、实验结果、novelty claim 或 reviewer comment。
```

### 7.2 手动初始化 workspace

```bash
python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id demo_project \
  --overwrite
```

验证基础 workspace：

```bash
python3 scripts/validate_outputs.py \
  --workspace workspaces/demo_project
```

## 8. 文献接地流程

```bash
python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id lit_demo \
  --overwrite

python3 scripts/ingest_literature.py \
  --workspace workspaces/lit_demo \
  --input examples/literature/sample_literature_input.json \
  --corpus-id lit_demo_synthetic_corpus \
  --overwrite

python3 scripts/build_literature_matrix.py \
  --workspace workspaces/lit_demo \
  --overwrite

python3 scripts/validate_literature.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/lit_demo \
  --strict
```

完整链条验收：

```bash
python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/lit_demo \
  --strict \
  --require-complete-chain
```

说明：

- 普通 `--strict` 检查已有 structured claims。
- `--require-complete-chain` 要求真实 final topic package 和完整 evidence traceability。
- demo/draft workspace 在 complete-chain 模式下失败是正确行为。

## 9. 实验验证规划流程

```bash
python3 scripts/build_validation_plan.py \
  --workspace workspaces/lit_demo \
  --overwrite \
  --demo-if-missing

python3 scripts/validate_experiment_plan.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_validation_adequacy.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/generate_reproducibility_checklist.py \
  --workspace workspaces/lit_demo
```

说明：

- 生成的是 validation plan，不是实验结果。
- `expected_result_pattern` 必须保持 conditional。
- 不允许写 `outperforms`、`p < 0.05`、`statistically significant` 等未验证结果。

## 10. 论文结构接地流程

```bash
python3 scripts/build_manuscript_blueprint.py \
  --workspace workspaces/lit_demo \
  --overwrite \
  --demo-if-missing

python3 scripts/validate_manuscript_plan.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/generate_reviewer_response_plan.py \
  --workspace workspaces/lit_demo \
  --overwrite

python3 scripts/generate_manuscript_checklist.py \
  --workspace workspaces/lit_demo
```

完整 manuscript chain 验收：

```bash
python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/lit_demo \
  --strict \
  --require-complete-manuscript-chain
```

说明：

- 普通 `--strict` 检查已有 manuscript plan 是否有 fake citation、fake result、unsupported claim 等问题。
- `--require-complete-manuscript-chain` 要求真实 final topic package、非 demo manuscript blueprint、完整 traceability table 和真实 result evidence。
- demo/draft workspace 在 complete-chain 模式下失败是正确行为。

## 11. 全模式验收命令

```bash
python3 scripts/validate_outputs.py \
  --workspace workspaces/lit_demo \
  --literature-grounded \
  --strict-evidence \
  --experiment-grounded \
  --strict-validation \
  --manuscript-grounded \
  --strict-manuscript
```

全量测试：

```bash
python3 -m pytest tests -q -ra
```

Profile 和打包测试：

```bash
python3 scripts/validate_profiles.py
python3 scripts/build_skill_package.py \
  --output /private/tmp/windfarm_skill_package \
  --overwrite
```

## 12. 输出 artifact

基础模块：

```text
00_project_intake/
01_domain_scan/
02_problem_identification/
03_theoretical_positioning/
04_contribution_argumentation/
05_chain_consistency_audit/
06_final_topic_package/
```

每个模块目录包含：

```text
input.json
output.json
output.md
next_input.json
validation_report.md
```

文献接地：

```text
literature_evidence/
  bibliographic_records.json
  paper_cards.json
  literature_matrix.json
  evidence_claim_map.json
  literature_gap_audit.json
  literature_grounding_report.json
```

实验接地：

```text
experiment_validation/
  validation_targets.json
  experiment_design.json
  baseline_plan.json
  metric_plan.json
  ablation_plan.json
  case_study_plan.json
  statistical_analysis_plan.json
  reproducibility_plan.json
  experiment_grounding_report.json
```

论文结构接地：

```text
manuscript_grounding/
  manuscript_blueprint.json
  section_argument_map.json
  paragraph_claim_plan.json
  citation_requirement_map.json
  result_placeholder_map.json
  method_section_alignment.json
  experiment_section_alignment.json
  discussion_limitations_plan.json
  reviewer_objection_map.json
  reviewer_response_strategy.json
  manuscript_adequacy_audit.json
  manuscript_grounding_report.json
```

## 13. 安全边界

禁止行为：

- 伪造作者、年份、期刊、DOI、引用。
- 伪造实验结果、p-value、runtime、ranking、显著性结论。
- 把 synthetic evidence 当成真实 field evidence。
- 把 result placeholder 写成 observed result。
- 把 anticipated reviewer objection 写成 received reviewer comment。
- 把 corpus-scoped gap 写成 field-wide no-one-studied claim。
- 把普通算法套用包装成 contribution。
- 在没有完整 evidence chain 时写 `first`、`novel`、`state-of-the-art`、`outperforms all`。

允许行为：

- 标记 `needs_literature_verification`。
- 标记 `requires_empirical_results`。
- 生成 citation requirement。
- 生成 result placeholder。
- 生成 anticipated reviewer objection。
- 生成 reviewer response strategy plan。
- 生成 manuscript adequacy audit。

## 14. 质量门

封版前必须满足：

```bash
python3 -m pytest tests -q -ra
python3 scripts/validate_profiles.py
find workspaces -maxdepth 2 -type f | sort
```

`workspaces/` 理想输出：

```text
workspaces/.gitkeep
```

对于真实项目，还应运行：

```bash
python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/<project> \
  --strict \
  --require-complete-chain

python3 scripts/audit_manuscript_claims.py \
  --workspace workspaces/<project> \
  --strict \
  --require-complete-manuscript-chain
```

## 15. 维护原则

- Core 保持 profile-neutral。
- 领域知识进入 `profiles/`。
- 新领域先新增 profile，不先 fork schema。
- 示例数据必须明确 synthetic。
- 运行 workspace 不提交。
- README 面向使用者和维护者，SKILL.md 面向 Codex runtime。
- 不把 v0.5.0 做成自动全文生成器。更合理方向是 human-in-the-loop manuscript drafting and revision workflow。

## 16. 当前状态

当前仓库已经完成：

- `v0.4.0` manuscript-grounded high-quality initial release。
- `v0.4.1` generic profile packaging。
- 安装包生成和本地安装验证。

当前能力边界清楚：

```text
research-topic-skill = 通用研究选题证据链框架
windfarm-research-topic-skill = windfarm layout/cabling 成熟源实现和 profile
```
