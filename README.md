# windfarm-research-topic-skill

`windfarm-research-topic-skill` 是一个科研论文选题逻辑 Skill，用于帮助研究人员在“计算机 / 进化计算 / 风电场布局优化 / 风电场布线优化 / 布局-布线联合优化”方向构建可审稿、可追踪、可修改、可验证的选题论证链。

它不是普通 prompt，也不是论文生成器。它不会替代真实文献综述、实验运行、导师判断或投稿写作；没有真实文献输入时，所有文献相关判断都必须标记为 `needs_literature_verification`。

## 为什么采用模块化设计

- 模块化：每个模块只负责一类任务，避免把领域扫描、问题识别、理论定位和贡献论证混在一起。
- 松耦合：下游模块只能读取直接上游模块暴露的 `next_input.json`。
- 高内聚：每个模块说明自己的输入、输出、质量门槛、失败模式和下游契约。
- 断点续跑：可以从任意模块恢复，不需要重跑所有上游模块。
- 输出保存：每个模块保存 `input.json`、`output.json`、`output.md`、`next_input.json`、`validation_report.md`。
- 局部调试：修改某个模块后，只需要验证该模块及其直接下游。
- token 和时间节省：`next_input.json` 只传递必要字段，避免反复加载完整上游材料。

## 核心流程

```text
Project Intake
-> Domain Scan
-> Problem Identification
-> Theoretical Positioning
-> Contribution Argumentation
-> Chain Consistency Audit
-> Final Topic Package
```

固定论证链条：

```text
logic-only mode:
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

literature-grounded mode:
bibliographic record
-> paper card
-> extracted evidence claim
-> literature matrix
-> domain fact
-> domain tension
-> research gap
-> research problem
-> contribution claim
```

## 目录结构

```text
windfarm-research-topic-skill/
  SKILL.md                    # Skill 总控说明
  README.md                   # 项目说明和使用方法
  skill_manifest.json         # Skill manifest 和模块索引
  modules/                    # 各模块执行协议
  schemas/                    # output.json JSON Schema
  templates/                  # output.md Markdown 模板
  scripts/                    # 初始化、验证、断点续跑工具
  examples/                   # 示例输入和示例模块输出
  tests/                      # pytest 契约测试
  workspaces/                 # 生成的项目工作区
```

## Workspace 机制

每次真实使用建议创建独立 workspace：

```text
workspaces/<project_id>/
  project_state.json
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

`workspaces/` 是运行产物目录，默认不提交到版本库；源码仓库只保留 `workspaces/.gitkeep`。需要保留的教学或验收材料应压缩成稳定 fixture，放在 `examples/acceptance_cases/`，不要提交完整运行 workspace。

注意：`modules/01_project_intake.md` 是文档编号；workspace 中对应目录是 `00_project_intake/`。脚本会识别文档编号和 workspace 编号的映射。

## next_input.json 的作用

`next_input.json` 是唯一正式传递给下游模块的接口文件。

下游模块不得读取上上游完整 `output.json`，不得依赖隐藏推理、聊天记录或未保存草稿。`next_input.json` 可以携带必要的 `trace_context`，但不能把所有上游原始输出整体塞进去。

## 断点续跑机制

从任意模块恢复时，脚本会：

1. 识别目标模块编号并映射到 workspace 目录。
2. 检查目标模块是否存在。
3. 读取直接上游模块的 `next_input.json`。
4. 写入当前模块的 `input.json`。
5. 更新 `project_state.json` 的 `current_module` 和 `history`。
6. 不读取上上游模块内容，不重写上游模块输出。

## 初始化 workspace

```bash
python scripts/init_workspace.py --input examples/sample_project_input.yaml --project-id demo_project
```

如果 workspace 已存在且确认要覆盖：

```bash
python scripts/init_workspace.py --input examples/sample_project_input.yaml --project-id demo_project --overwrite
```

## 验证输出

```bash
python scripts/validate_outputs.py --workspace workspaces/demo_project
```

验证会检查：

- workspace 和 `project_state.json` 是否存在。
- 每个模块目录和五类输出文件是否存在。
- `output.json`、`next_input.json` 是否是合法 JSON。
- `output.json` 是否包含全局字段。
- 如果安装了 `jsonschema`，是否满足 `schemas/` 中的对应 schema。
- 链条是否只依赖直接上游 `next_input.json`。
- 是否生成 `validation_summary.md`。

## 从指定模块继续

```bash
python scripts/resume_from_module.py --workspace workspaces/demo_project --module-id 03_theoretical_positioning
```

覆盖当前模块输入或状态：

```bash
python scripts/resume_from_module.py --workspace workspaces/demo_project --module-id 03_theoretical_positioning --overwrite-current
```

## 人工修改某个模块并继续

1. 修改该模块的 `output.json`、`output.md` 和 `next_input.json`。
2. 确保 `output.json` 中保留 `status`、`uncertainty_log`、`reviewer_risks`、`revision_hooks`、`trace_context`。
3. 运行验证：

```bash
python scripts/validate_outputs.py --workspace workspaces/demo_project
```

4. 从直接下游模块恢复：

```bash
python scripts/resume_from_module.py --workspace workspaces/demo_project --module-id <next_module_id> --overwrite-current
```

## 避免文献伪造和贡献夸大

- 不编造引用、作者、年份、期刊、DOI 或实验结果。
- 没有真实文献输入时，所有“已有研究如何”的判断必须标记为 `needs_literature_verification`。
- 不使用无证据强断言，例如 `first`、`novel`、`state-of-the-art`、`outperforms all`。
- 贡献表达优先使用保守表述，例如 `problem-guided evolutionary optimization approach`。
- 研究问题必须来自问题结构，不能来自“想套用某个新算法”。

示例输出和验收 fixtures 只证明输出契约与防错逻辑，不代表真实研究结论。真实论文选题必须另行完成文献检索、引用核验、基线实验和消融验证；本 Skill 不能替代这些工作。

## 最小使用示例

```bash
python scripts/init_workspace.py --input examples/sample_project_input.yaml --project-id demo_project --overwrite
python scripts/resume_from_module.py --workspace workspaces/demo_project --module-id 01_domain_scan --overwrite-current
python scripts/validate_outputs.py --workspace workspaces/demo_project
```

后续人工或 AI agent 可以按模块读取 `templates/*.template.md`，生成每个模块的 `output.md` 和 `output.json`，再把必要内容压缩到 `next_input.json` 传递给下游。

## v0.2.0 literature grounding

v0.2.0 adds a literature-grounding layer that links domain scan, problem identification, theoretical positioning, and contribution claims to user-provided literature evidence.

Two modes are supported:

- `logic-only mode`: no real literature input; keep v0.1.0 behavior and mark literature judgments `needs_literature_verification`.
- `literature-grounded mode`: user provides literature data; build paper cards, literature matrix, evidence claim map, and gap audit.

Supported input formats:

- JSON
- YAML
- BibTeX
- CSV optional
- Markdown paper notes optional

Minimum literature fields:

- `paper_id` is assigned by the ingest script.
- `title`
- `source_type`
- `is_synthetic`
- `evidence_status`

Recommended real-literature fields:

- `authors`
- `year`
- `venue`
- `doi`
- `url`
- `abstract`
- `keywords`
- `user_notes`
- `relevant_excerpts`

New commands:

```bash
python3 scripts/ingest_literature.py \
  --workspace workspaces/demo_project \
  --input examples/literature/sample_literature_input.json

python3 scripts/validate_literature.py \
  --workspace workspaces/demo_project

python3 scripts/build_literature_matrix.py \
  --workspace workspaces/demo_project

python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/demo_project \
  --strict
```

Literature artifacts are written to:

```text
literature_evidence/
  paper_cards.json
  literature_matrix.json
  evidence_claim_map.json
  literature_gap_audit.json
```

The compact `evidence_context` is injected into `next_input.json`. It is not a substitute for `paper_cards.json` and must not contain full paper text.

v0.2.0 minimum flow:

```bash
cd windfarm-research-topic-skill

python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id lit_demo \
  --overwrite

python3 scripts/ingest_literature.py \
  --workspace workspaces/lit_demo \
  --input examples/literature/sample_literature_input.json

python3 scripts/validate_literature.py \
  --workspace workspaces/lit_demo

python3 scripts/build_literature_matrix.py \
  --workspace workspaces/lit_demo

python3 scripts/audit_claim_grounding.py \
  --workspace workspaces/lit_demo \
  --strict

python3 scripts/validate_outputs.py \
  --workspace workspaces/lit_demo
```

Usage boundaries:

- Without real literature input, a gap cannot be marked verified.
- Synthetic samples are only structure tests.
- `audit_claim_grounding.py` checks structured evidence links; it does not replace human paper reading.
- DOI, authors, years, venues, and citation truth require external bibliographic verification.
- v0.2.0 does not replace systematic review, discover all relevant papers, or prove novelty automatically.

Strict audit boundary:

- `audit_claim_grounding.py --strict` checks structured claims that already exist in module outputs. It intentionally skips untouched `PENDING_MODULE_OUTPUT` draft placeholders.
- Use `audit_claim_grounding.py --strict --require-complete-chain` for release-grade chain acceptance. That mode fails if the final topic package is incomplete, the Evidence Traceability Table is missing, selected problem evidence links are missing, or contribution evidence links are missing.

## v0.3.0 experiment grounding

v0.3.0 adds an experiment-grounding layer that maps contribution claims to validation objectives, baselines, metrics, ablations, case studies, statistical tests, reproducibility requirements, and reviewer-risk defenses.

The three supported modes are:

- `logic-only mode`: no real literature or experiment plan input; keep v0.1.0 behavior and mark literature judgments `needs_literature_verification` and experiment judgments `validation_required`.
- `literature-grounded mode`: use v0.2.0 paper cards, literature matrix, evidence claim map, and corpus-scoped gap judgment.
- `experiment-grounded mode`: ask what experiment plan a contribution needs before a reviewer should believe it.

The difference from v0.2.0 is:

- v0.2.0 asks: "Does this gap or contribution have literature evidence?"
- v0.3.0 asks: "What validation plan would make this contribution credible?"

New commands:

```bash
python3 scripts/build_validation_plan.py \
  --workspace workspaces/demo_project

python3 scripts/validate_experiment_plan.py \
  --workspace workspaces/demo_project \
  --strict

python3 scripts/audit_validation_adequacy.py \
  --workspace workspaces/demo_project \
  --strict

python3 scripts/generate_reproducibility_checklist.py \
  --workspace workspaces/demo_project
```

Minimum v0.3.0 flow:

```bash
cd windfarm-research-topic-skill

python3 scripts/init_workspace.py \
  --input examples/sample_project_input.yaml \
  --project-id exp_demo \
  --overwrite

# Optional literature grounding
python3 scripts/ingest_literature.py \
  --workspace workspaces/exp_demo \
  --input examples/literature/sample_literature_input.json \
  --corpus-id exp_demo_synthetic_corpus \
  --overwrite

python3 scripts/build_literature_matrix.py \
  --workspace workspaces/exp_demo \
  --overwrite

python3 scripts/validate_literature.py \
  --workspace workspaces/exp_demo \
  --strict

# Experiment validation planning
python3 scripts/build_validation_plan.py \
  --workspace workspaces/exp_demo \
  --overwrite \
  --demo-if-missing

python3 scripts/validate_experiment_plan.py \
  --workspace workspaces/exp_demo \
  --strict

python3 scripts/audit_validation_adequacy.py \
  --workspace workspaces/exp_demo \
  --strict

python3 scripts/generate_reproducibility_checklist.py \
  --workspace workspaces/exp_demo

python3 scripts/validate_outputs.py \
  --workspace workspaces/exp_demo \
  --literature-grounded \
  --strict-evidence \
  --experiment-grounded \
  --strict-validation
```

v0.3.0 limitations:

- It does not run experiments.
- It does not generate experimental results.
- It cannot guarantee planned experiments will lead to publication.
- It cannot replace real wind-farm simulation, optimization code, data, or engineering review.
- It only checks contribution-to-validation adequacy.

## 测试命令

```bash
python3 -m pytest tests
```

如果当前 Python 环境没有 `pytest`，请先安装或切换到包含 `pytest` 的环境；脚本本身主要使用 Python 标准库，`PyYAML` 和 `jsonschema` 会在可用时增强解析和验证能力。
