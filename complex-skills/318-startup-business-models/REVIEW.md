# REVIEW: 318-startup-business-models

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — startup revenue model selection, pricing design, and unit economics analysis
**Body 行数**: 135 行
**参考文件数**: references/0, scripts/0, assets/0, data/0（全部被引用但不存在）
**总文件数**: 3（SKILL.md, SCORING.yaml, check.py）
**已有 REVIEW**: 旧版 283 行 stub，本次替换为全面深度审查

---

## 1. 目录全量清单

```
318-startup-business-models/
├── SKILL.md (135 行)
├── SCORING.yaml (182 行)
├── check.py (71 行)
└── REVIEW.md (本次覆写)
```

该 skill 是极简 3 文件结构——无子目录。但 body 中引用了 4 个不存在的文件（2 个 references/、1 个 assets/、1 个 data/），形成严重的"幽灵引用"问题。空 Resource 表和 Template 表（L91-98）暗示规划了补充材料但从未创建。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 实际值: `startup-business-models`
- 匹配目录名 `318-startup-business-models`: ✅（name 不含编号前缀，符合规范）
- 全小写+连字符: ✅
- 长度: 24 字符（≤64）: ✅
- 判定: ✅ 通过

### 2.2 description

**原文逐句分析**:

```
"Startup revenue model selection, pricing design, and unit economics analysis.
 Use when choosing or evaluating a startup revenue model, pricing/value metric,
 packaging/tier design, or calculating unit economics (LTV, CAC, payback,
 gross margin, NRR), including usage-based/credit/AI pricing and variable
 compute/COGS constraints."
```

| 句子 | 内容 | 类型判定 | 问题 |
|------|------|:--------:|------|
| 句1: "Startup revenue model selection, pricing design, and unit economics analysis." | 功能声明 | WHAT（名词短语）| ❌ 不是完整第三人称句子——缺少谓语动词。应改为 "Analyzes and recommends startup revenue models, pricing design, and unit economics." |
| 句2: "Use when choosing or evaluating a startup revenue model, pricing/value metric, packaging/tier design, or calculating unit economics (LTV, CAC, payback, gross margin, NRR), including usage-based/credit/AI pricing and variable compute/COGS constraints." | 触发条件 | WHEN（含触发短语 "Use when"）| ⚠️ 触发短语正确，但功能罗列过度——括号内的 (LTV, CAC, payback, gross margin, NRR) 是术语堆砌而非触发场景描述 |

**逐项检查**:
- 第三人称: ⚠️ 句1为名词短语（无主语/谓语），句2为祈使句 "Use when"（隐含第二人称 you）。规范要求第三人称，但 "Use when" 是允许的触发信号格式
- 禁止内容: 无第一人称、无跨 skill 路由（`@skill-name`）、无实现细节 ✅
- 长度: ~340 字符，≤1024 ✅
- 触发短语: "Use when" ✅

**修改建议**:
```
Analyzes and recommends startup revenue models, pricing design, and unit economics.
Use when the user needs to choose or evaluate a revenue model, design pricing and
packaging tiers, or calculate unit economics — including usage-based, credit-based,
and AI pricing with variable compute cost constraints.
```
将术语列表 (LTV, CAC, ...) 移到 body 中，"What Good Looks Like" 节已有这些术语的完整上下文。

### 2.3 allowed-tools

- 实际值: **缺失** ❌
- 该 skill 需要 Read 工具（读取 references，如果它们存在的话）和 Write 工具（输出分析报告）。建议: `allowed-tools: Read, Write`
- 即使 references 不存在，agent 至少需要 Read 自身的 SKILL.md 和 Write 来输出结果

### 2.4 其他 frontmatter 字段

仅 `name` 和 `description` 两个字段，无禁止字段 ✅。未使用任何可选字段（如 `model`、`user-invocable`、`paths` 等）。

### 2.5 Frontmatter 语法

YAML 分隔符 `---` 配对正确（L1, L4）✅。无缩进错误、无未转义特殊字符 ✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Startup Business Models                         L6    — 标题
概述段落                                            L8    — 1 行简介
## Quick Start (Inputs)                            L10   — 输入收集指南（11 行）
## Workflow                                        L22   — 6 步流程（22 行）
## 2026 Heuristics (Context-Dependent)              L45   — 行业基准（5 行）
## Related Skills (Routing)                         L51   — 路由声明（6 行）
## Pricing Change Measurement & Experiment Design   L58   — 实验设计（26 行）
### 1) Define success and guardrails               L61   — 指标表
### 2) Pick an evaluation design                   L67   — 4 种设计方案表
### 3) Use explicit lag windows                     L75   — 3 层时间窗口
### 4) Report an "all-in" view                     L80   — 综合报告要求
## SaaS Metrics (Read When Needed)                  L85   — 委托声明（3 行）
## Resources                                        L89   — 空表（3 行）
## Templates                                        L94   — 空表（3 行）
## Data                                             L99   — 死引用（5 行）
## Do / Avoid (Jan 2026)                           L107   — 操作原则（13 行）
## What Good Looks Like                            L121   — 输出质量标准（7 行）
## Optional: AI / Automation                       L129   — AI 使用声明（6 行）
```

共 15 个节标题（含 4 个 ### 子节），总 135 行 body。

### 3.2 必需章节检查

**Workflow/Process 节**: ✅ 存在。标题为 "## Workflow"，包含编号 1-6 的步骤。每个步骤描述了做什么 + 粗略的输出期望。但问题在于：
- 步骤 2（L27）说 "Refer to standard unit economics formulas and benchmarks"——未提供公式，也未指向存在的文件
- 步骤 4（L36-37）引用 `references/pricing-research-guide.md` 和 `assets/pricing-tier-design.md`——两个文件都不存在
- 步骤间没有显式的输入/输出声明（如 "Step 1 outputs a model classification that feeds Step 2"）

**Output Format 节**: ⚠️ 部分存在。"## What Good Looks Like"（L121-127）承担了输出质量描述功能，列出 5 条标准：packaging 清晰、unit economics 定义、assumptions 明确、experiments 可测、risks 建模。但缺少：
- 具体的输出模板/结构（如 "输出应包含以下章节: Executive Summary, Model Classification, Unit Economics Snapshot, ..."）
- 字段级格式要求（JSON schema、表格结构等）
- SCORING.yaml OUT-01 要求的 "decision-ready: recommendation, rationale, assumptions, scenarios, next experiments" 只在标准中间接提及，未形成模板

**Scope/Limitations 节**: ⚠️ 部分存在。"## Related Skills (Routing)"（L51-56）承担了 scope 功能——声明了 4 个不应替代此 skill 的相关 skills。但缺少：
- 技术边界（如 "不适用于非盈利组织财务建模"、"不涵盖税务优化"）
- 领域边界（如 "仅覆盖 SaaS/usage-based/marketplace 等数字商业模式，不适用制造业/重资产"）
- 责任边界（如 "提供框架和计算，不提供法律或税务建议"）
- 明确的 "何时不使用此 skill" 声明

### 3.3 内容委托分析

Body 中引用 4 个外部文件，**全部不存在**：

| 引用行 | 引用路径 | 存在 | 委托内容 |
|:------:|----------|:----:|----------|
| L36 | references/pricing-research-guide.md | ❌ | WTP 方法和定价访谈脚本 |
| L37 | assets/pricing-tier-design.md | ❌ | Tier 设计、限制、升级触发器 |
| L87 | references/saas-metrics-playbook.md | ❌ | SaaS 指标定义和模板 |
| L103 | data/sources.json | ❌ | 商业模式资源链接 |

委托行数: 4/135 ≈ 3%。虽然委托比例低，但 **100% 的委托目标无效**——agent 遇到这些引用时将无法获取所需信息。步骤 4 完全依赖这些文件，导致该步骤无法执行。

### 3.4 节编号/标题层级

- 标题层级: `#` → `##` → `###` 连续，无跳级 ✅
- Workflow 步骤编号 1-6 连续 ✅
- 潜在问题: "Pricing Change Measurement" 使用了 `### 1) ... ### 2) ...` 编号，而 Workflow 使用 `1) 2) 3)` 无 `#` 前缀——风格不一致但非功能性错误

### 3.5 Body 长度合规

135 行 vs 600 行硬限制——远低于上限。Process pattern 建议 ~200 行——实际偏短约 65 行。考虑到 4 个 references 缺失，body 实际上需要将委托内容内联或创建对应文件，届时行数会接近 200 行的目标。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

逐对检查 Workflow 6 步的信息流:

| 步骤对 | 上游输出 | 下游需求 | 匹配度 |
|--------|----------|----------|:------:|
| 1→2 | 模型类型分类 | Unit economics 快照需按模型类型区分 | ✅ 匹配——不同模型有不同 economics 结构 |
| 2→3 | Segment-level economics 数据 | 风险评估需 economics 数据作为输入 | ✅ 匹配——margin/selection/churn 风险从 economics 数据推导 |
| 3→4 | 风险识别结果 | Pricing 改进建议需基于风险分析 | ✅ 匹配——风险驱动定价调整方向 |
| 4→5 | Pricing 变更方案 | Measurement 计划需知道改了什么 | ✅ 匹配——变更内容决定测量指标选择 |
| 5→6 | Measurement 计划 | 最终输出需包含 measurement | ✅ 匹配——汇总到 decision-ready 输出 |

**关键断裂点**: 步骤 4 依赖不存在的 `references/pricing-research-guide.md`（WTP 方法）和 `assets/pricing-tier-design.md`（tier 设计模板），导致 agent 在该步骤无法获取方法论指导。

### 4.2 内部矛盾扫描

- "LTV:CAC is easiest to game"（L47, 2026 Heuristics）与 SCORING.yaml CF-03 "Agent uses LTV:CAC as the sole decision criterion" 一致——都在警告不要过度依赖单一 ratio ✅
- "Do / Avoid (Jan 2026)"（L107）与 "2026 Heuristics"（L45）——两个节都标注了 2026 年，但日期格式不一致（一个有月份 "Jan 2026"，一个没有）。内容无矛盾但风格不统一
- "Do" 列表（L111-113）与 "What Good Looks Like"（L123-127）部分重叠——value metric、COGS drivers、discount guardrails 在两处出现。存在信息冗余但无矛盾

### 4.3 代码正确性

无可执行代码块。Workflow 步骤为描述性文本。Pricing Change Measurement 节中的 3 个表格为 Markdown 格式，语法正确 ✅。

### 4.4 条件完整性

| 条件位置 | 条件 | else/otherwise | 完整性 |
|----------|------|----------------|:------:|
| L20 | "If numbers are missing" | "proceed with ranges + explicit assumptions and highlight what to measure next" | ✅ 完整——有具体的 else 行为 |
| L130 | "Use only when explicitly requested and policy-compliant" | 隐含: 否则不使用 AI | ⚠️ 未显式写出 else 分支 |
| L67-73 | 4 种 evaluation design，各有 "Best when" 条件 | 每种 design 有 "How to read results" | ✅ 完整——4 种方案覆盖主要场景 |

"Optional: AI / Automation" 缺少显式的 "如果未明确请求，则不要使用 AI 功能" 声明。建议补充。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 文件行数 | 内容匹配度 |
|----------|:------------:|:--------:|:--------:|:---------:|
| references/pricing-research-guide.md | L36 | ❌ | — | 死引用 |
| assets/pricing-tier-design.md | L37 | ❌ | — | 死引用 |
| references/saas-metrics-playbook.md | L87 | ❌ | — | 死引用 |
| data/sources.json | L103 | ❌ | — | 死引用 |

**死引用率: 4/4 = 100%**。这是该 skill 最严重的问题——所有声称的外部资源都不存在。

### 5.2 不可见资源审计

目录中仅 3 个文件，无隐藏资源。不存在但应存在的文件已在上表列出。

### 5.3 Reference 文件全文审查

无 references/ 目录。无法审查。

### 5.4 Scripts 文件全文审查

无 scripts/ 目录。无法审查。

### 5.5 跨 Skill 引用检查

L53-56: 4 个 prose 引用:
- `startup-idea-validation` — 合规 prose 引用 ✅
- `startup-competitive-analysis` — 合规 prose 引用 ✅
- `startup-fundraising` — 合规 prose 引用 ✅
- `startup-go-to-market` — 合规 prose 引用 ✅

均为 prose 形式的 "the `skill-name` skill" 引用，不含 `../` 路径。SCORING.yaml SCOPE-02 将这些作为 routing targets 检查，确保 agent 不在 business-models 任务中错误切换到这些相关 skills。

### 5.6 嵌套重复/死文件检查

- 无 self-nested 目录 ✅
- 无 `.gitkeep` 占位空目录 ✅
- 空 Resource 表（L91-92）和空 Template 表（L96-97）——这些是 SKILL.md 内部的空内容，表明计划了但从未填充。建议: 删除空表或添加实际条目

### 5.7 其他资源文件审查

无 assets/、resources/、templates/、examples/ 等目录。

---

## 6. 语法与格式质量

### 6.1 拼写错误

无拼写错误。商业/金融术语使用正确: CAC (Customer Acquisition Cost)、LTV (Lifetime Value)、NRR (Net Revenue Retention)、ARPA (Average Revenue Per Account)、PLG (Product-Led Growth) ✅。

### 6.2 语法错误

**句1 (description)**: "Startup revenue model selection, pricing design, and unit economics analysis." — 这是一个名词短语（noun phrase），缺少限定词和谓语动词。应改为完整的第三人称陈述句: "Analyzes and recommends startup revenue models, pricing design, and unit economics."

其余 body 内容语法正确。Bullet points 和表格内容使用 telegram 风格（省略冠词），在技术文档中可接受。

### 6.3 中英/葡英混杂

纯英文 ✅。无中文、葡语或其他语言泄露。

### 6.4 Markdown 格式破损

- 表格格式: 3 个表格（L62-65、L68-73、L101-103）格式正确 ✅
- 代码围栏: 无代码块 ✅
- 链接语法: L103 `[sources.json](data/sources.json)` — 链接语法正确但目标不存在 ⚠️
- 列表: bullet points 和编号步骤格式正确 ✅

### 6.5 占位符未填充

- 搜索 `TODO`、`FIXME`、`TBD`、`{{PLACEHOLDER}}`: 无显式占位符 ✅
- 空表（L91-98 Resources 和 Templates）——这些是结构性空白，不是占位符。但视觉效果等同于"待填充"，对 agent 造成困惑

### 6.6 截断内容

文件以 "Draft pricing page copy; humans verify claims and consistency with contracts."（L134）结束，为完整句子 ✅。无截断。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名（不含编号前缀） | ✅ | `startup-business-models` 匹配 |
| 2 | description 第三人称 | ⚠️ | 句1为名词短语，非完整句子 |
| 3 | description 含触发短语 | ✅ | "Use when" 存在 |
| 4 | description ≤1024 字符 | ✅ | ~340 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | 仅 name + description |
| 6 | body ≤600 行 | ✅ | 135 行 |
| 7 | Workflow/Process 节存在 | ✅ | "## Workflow" 6 步流程 |
| 8 | Output Format 节存在 | ⚠️ | "What Good Looks Like" 部分承担，但不完整 |
| 9 | Scope/Limitations 节存在 | ⚠️ | "Related Skills" 部分承担，缺技术/领域/责任边界 |
| 10 | 无跨 skill 文件路径引用 | ✅ | 4 个 prose 引用均合规 |
| 11 | allowed-tools 格式正确 | ❌ | 字段缺失 |
| 12 | 路径仅指向本 skill 目录内 | ⚠️ | 路径合规但目标文件不存在 |

**合规统计: 7/12 ✅, 4/12 ⚠️, 1/12 ❌**

---

## 8. 人机感评估

### 8.1 Emoji 审计

零 emoji 使用 ✅。全文无任何装饰性或功能性 emoji。

### 8.2 全大写/喊叫式语言

零处全大写命令 ✅。无 "STOP!"、"MANDATORY"、"CRITICAL"、"NEVER" 等喊叫式语言。"Do / Avoid" 使用常规大小写，语气专业克制。

### 8.3 Persona 语气分析

整体语气: **商业咨询风格**——直接、务实、数据驱动。代表性语句分析:

- "Ask for the smallest set of inputs that makes the decision meaningful"（L12）——效率导向，最小化输入负担
- "If numbers are missing, proceed with ranges + explicit assumptions and highlight what to measure next"（L20）——务实，提供 fallback 路径
- "LTV:CAC is easiest to game"（L47）——直率，带有行业经验的敏锐判断
- "Avoid: Pricing as an afterthought （'we'll figure it out later'）"（L117）——引用典型的反模式口头禅，有说服力

语气适合商业/战略决策场景。不是学术性的，不是命令式的，而是顾问式的——给出框架和判断标准，让 agent 在此基础上推理。

### 8.4 人机边界分析

- "If numbers are missing, proceed with ranges + explicit assumptions and highlight what to measure next"（L20）——agent 透明标记假设，不伪装成确定数据 ✅
- "Use only when explicitly requested and policy-compliant"（L130, AI/Automation）——AI 使用受约束，需人类批准 ✅
- "humans verify claims and consistency with contracts"（L134）——明确将最终验证责任归于人类 ✅
- 无硬编码的人类名称 ✅
- 无 "In all cases, the human decides" 式显式边界声明，但上述语句隐含了边界

### 8.5 人称分析

- 第二人称（you/your）: 0 次 ✅
- 第一人称（I/we）: 0 次 ✅
- 祈使句: "Ask for..."、"Proceed with..."、"Define..." 等，面向 agent 的操作指令——在 Workflow 上下文中合理
- description 中的 "Use when" 是唯一含隐含第二人称的位置，但属于规范允许的触发信号格式

### 8.6 表格密度检查

Body 中有 5 个表格:
1. L62-65: Guardrails 指标表（2 列，功能性强）
2. L68-73: Evaluation design 方案选择表（3 列，功能性）
3. L91-98: Resources/Templates 空表（应删除或填充）
4. L101-103: Data sources 表（1 行，引用了不存在的文件）

表格使用合理——Pricing Change Measurement 节的两个功能表格信息密度高，转换为自然语言会降低可读性。但空表（Resources/Templates）必须处理。

---

## 9. 可执行性评估

### 9.1 独立可执行性

**评分: 5/10**

假设 agent 只拿到 SKILL.md（无目录探索能力）:
- ✅ 可以执行步骤 1（模型分类）——9 种模型 taxonomy 在 body 中
- ⚠️ 可以尝试步骤 2（unit economics）——但 "standard formulas" 未提供
- ✅ 可以执行步骤 3（风险评估）——5 种 failure mode 具体列出
- ❌ 无法完整执行步骤 4（pricing 建议）——依赖 2 个不存在的 reference
- ✅ 可以执行步骤 5（measurement）——详细指导在 body 中
- ⚠️ 可以生成步骤 6（输出）——但无具体输出模板，只能从 "What Good Looks Like" 推断

最大的阻断点: 步骤 4 完全依赖不存在的文件。

### 9.2 步骤可操作性

| Step | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| 1 | "Classify the model" — 9 种模型 taxonomy 列表 | 🟢 | 清晰可执行 |
| 2 | "Build a segment-level unit economics snapshot" — "Refer to standard formulas" | 🟡 | 未提供公式，agent 需自行推断 |
| 3 | "Evaluate model fit and risks" — 5 种 failure mode | 🟢 | 具体可执行 |
| 4 | "Propose pricing + packaging changes" — 依赖 2 个不存在文件 | 🔴 | 关键步骤无法执行 |
| 5 | "Define measurement and roll-out" — 详细实验设计指导 | 🟢 | 具体可执行 |
| 6 | "Deliver a decision-ready output" — 要求清晰但无模板 | 🟡 | 输出结构不明确 |

### 9.3 工具依赖合理性

- 需要的工具: Read（读取 references）、Write（输出报告）
- allowed-tools 声明: **缺失** ❌
- 外部依赖: 无（无 API、CLI、第三方服务）
- 回退方案: 不需要——该 skill 为纯推理和分析流程

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

19 个 criteria（scope 3, process 5, technical 2, decision 2, principles 1, output 2, negative 3, qa 1），全部为 LLM judge:

| 类别 | 数量 | 与 SKILL.md 一致性 |
|------|:----:|-------------------|
| SCOPE (01-03) | 3 | ✅ 与 description 和 Quick Start 节一致 |
| PROC (01-05) | 5 | ✅ 与 Workflow 步骤匹配。PROC-04/05 依赖 Pricing Change Measurement 节——内容存在 |
| TEC (01-02) | 2 | ✅ TEC-01 对应 2026 Heuristics (L48-49)，TEC-02 对应 heuristic 3 (L49) |
| DEC (01-02) | 2 | ✅ DEC-01 对应 L47 heuristic，DEC-02 对应 Workflow step 3 |
| PRI-01 | 1 | ✅ 对应 Do 列表和 What Good Looks Like |
| OUT (01-02) | 2 | ⚠️ 标准存在于 body 中但未形成输出模板 |
| NEG (01-03) | 3 | ✅ 对应 Avoid 列表 |
| QA-01 | 1 | ✅ 对应 "Report an all-in view" 节 (L80-83) |

SCORING.yaml 与 SKILL.md 内容一致性: **良好**。每个 criterion 都可以在 body 中找到对应的内容基础。

### 10.2 Critical Failures 分析

4 个 critical_failure 条件:

| CF | 描述 | 合理性 |
|----|------|:------:|
| CF-01 | 推荐 revenue model 但无 unit economics 评估 | ✅ 合理——无数据支持的推荐无价值 |
| CF-02 | 推荐 pricing 变更但无 measurement plan | ✅ 合理——对应 skill 的 measurement 核心要求 |
| CF-03 | 仅使用 LTV:CAC 作为决策标准 | ✅ 合理——skill 明确警告 LTV:CAC 最容易被操纵 |
| CF-04 | 将编造的数字当作真实数据 | ✅ 合理——违反 assumptions contract |

4 个 CF 设计良好，捕捉了 business-models skill 的核心失败模式。CF-04 特别重要——在缺乏真实数据的情况下，agent 编造数字会导致虚假的精确感。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 不可用（文件不存在），跳过已知问题交叉验证。本次审查发现的全部问题均为增量发现。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 6/10 | 10% | 0.60 | description 名词短语、缺 allowed-tools |
| Body 结构完整 | 5/10 | 10% | 0.50 | Workflow ✅、Output/Scope 不完整、空表 |
| 逻辑一致性 | 6/10 | 20% | 1.20 | 流程自洽但步骤 4 因死引用无法执行 |
| 参考完整性 | 1/10 | 15% | 0.15 | 🔴 4/4 引用不存在——致命缺陷 |
| 语法格式 | 8/10 | 10% | 0.80 | 英文良好，空表需处理 |
| 规范合规 | 7/10 | 15% | 1.05 | 7/12 完全合规 |
| 人机感 | 8/10 | 10% | 0.80 | 专业商业风格，边界清晰 |
| 可执行性 | 5/10 | 10% | 0.50 | 核心流程可行，定价步骤因死引用受阻 |
| **加权总分** | | | **5.60/10** | |

### 12.2 评级

🟠 **C** (56/100) — 有显著缺陷。核心修复（创建 4 个缺失文件 + 完善必需章节）后可达 B 级 (>70)。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: 4 个引用文件全部不存在**
- 位置: SKILL.md L36（references/pricing-research-guide.md）、L37（assets/pricing-tier-design.md）、L87（references/saas-metrics-playbook.md）、L103（data/sources.json）
- 修复方向:
  - **方案 A（推荐）**: 创建 references/saas-metrics-playbook.md——包含 LTV/CAC/Churn/NRR/Payback 的标准公式、SaaS benchmark 参考范围、MRR/ARR/Quick Ratio/Magic Number 的定义和模板。这是最高优先级的文件，因为它支撑步骤 2 和 2026 Heuristics 的量化基础
  - **方案 B**: 将 pricing-research-guide.md 和 pricing-tier-design.md 的内容内联到 body 中。Pricing Change Measurement 节已经有大量相关内容——可以扩展现有 §2（Pick an evaluation design）和新增定价研究方法论子节
  - **方案 C**: 删除 data/sources.json 引用——商业模式资源链接容易过时，且对 agent 执行 skill 的核心功能非必需
- 不修复的后果: Step 4 无法执行。Agent 遇到死链接时行为不可预测（可能跳过、可能编造内容、可能报错）

**F-2: 空 Resources 和 Templates 表**
- 位置: SKILL.md L89-98
- 修复方向: 如果有计划添加的内容→填充条目；如果暂时没有→删除这两个 `## Resources` 和 `## Templates` 节，待有实际内容时再添加
- 不修复的后果: Agent 看到空表产生困惑——无法判断是遗漏还是有意为空

### 🟡 重要缺陷（建议修复）

**I-1: 缺少显式 Output Format 节**
- 位置: 在 "## What Good Looks Like" (L121) 之前插入新节
- 修复方向: 添加 `## Output Format` 节，包含:
  ```
  ## Output Format
  
  Structure the deliverable with these sections:
  
  1. Executive Summary — 3-5 sentence synthesis of the recommendation and key rationale
  2. Model Classification — which of the 9 model types applies, with justification
  3. Segment-Level Unit Economics — table per segment showing CAC, gross margin, churn, payback, NRR, LTV with cohort notes
  4. Risk Assessment — each of the 5 failure modes evaluated for this model
  5. Pricing Recommendations — proposed changes with rationale, tier design, and discount guardrails
  6. Measurement Plan — success metric, guardrails, evaluation design choice, lag windows, go/no-go threshold
  7. Assumptions Register — all assumptions in one table with ranges/sensitivities where data was missing
  8. Next Experiments — prioritized list of tests to run
  ```

**I-2: 缺少 Scope/Limitations 节**
- 位置: 在 "## Related Skills (Routing)" 之后添加新节
- 修复方向: 添加 `## Limitations` 节，列出:
  - 仅适用于数字商业模式（SaaS、usage-based、marketplace、subscription 等），不适用于制造业、零售、重资产行业
  - 提供分析框架和基准参考，不提供法律、税务或会计建议
  - 分析的准确性依赖于输入数据的质量——使用假设范围时，必须在输出中透明标注
  - 不执行实际的定价实施（A/B 测试平台配置、billing 系统集成等）
  - 不替代专业的定价顾问或 revenue operations 团队

**I-3: description 修正**
- 位置: SKILL.md L2-3
- 修复方向: 将名词短语改为完整第三人称句子，同时保留 "Use when" 触发信号
- 建议文本: 见 §2.2 修改建议

**I-4: 添加 allowed-tools**
- 位置: SKILL.md frontmatter（L3 之后）
- 修复方向: 添加 `allowed-tools: Read, Write`

**I-5: Workflow 步骤 2 的公式引用**
- 位置: SKILL.md L27
- 修复方向: 如果创建了 saas-metrics-playbook.md → 改为 "Refer to `references/saas-metrics-playbook.md` for formulas"。如果选择内联方案 → 添加关键公式:
  ```
  - LTV = (ARPA × Gross Margin %) / Churn Rate
  - CAC = (Sales + Marketing Spend) / New Customers Acquired  
  - Payback Period = CAC / (ARPA × Gross Margin %)
  - NRR = (Starting ARR + Expansion - Contraction - Churn) / Starting ARR
  ```

### 🟢 优化建议（锦上添花）

**O-1**: 统一日期标记格式——"2026 Heuristics" vs "Do / Avoid (Jan 2026)" 风格不一致。统一为 "2026 Heuristics" 或全部添加月份

**O-2**: "Optional: AI / Automation" 添加显式 else 分支: "If not explicitly requested, do not use AI features. Agent should rely on the deterministic workflow above."

**O-3**: check.py 当前为纯 LLM judge（0 个 script-verifiable check）。可添加至少 1 个确定性检查——如验证 agent 输出是否包含 "recommendation"、"rationale"、"assumptions" 三个必需关键词/节

**O-4**: Pricing Change Measurement 的 4 个 `### N)` 子标题与 Workflow 的 `N)` 编号风格不一致。统一使用 `###` 或纯数字编号

**O-5**: "What Good Looks Like" 中有 5 条 bullet points，但都与 "Do / Avoid" 和 Workflow 输出期望有重叠。考虑合并为一个更统一的输出质量标准节

### 修复工作量估计

- 预计新增文件: 1 个（references/saas-metrics-playbook.md, ~80-120 行）
- 预计修改文件: 1 个（SKILL.md）
- 预计新增行数: ~60-80 行（Output Format 节 + Scope/Limitations 节 + 公式 + 修正）
- 预计修改行数: ~10-15 行（description 修正、删除空表、添加 allowed-tools）
- 预计删除行数: ~8-10 行（空 Resources/Templates 表）
- 总工作量: ~80-100 行变更，2 个文件修改/创建

---

## 附录: 审查过程记录

### 读取文件清单

| 文件 | 行数 | 读取方式 |
|------|:----:|----------|
| SKILL.md | 135 | 全文逐行精读 |
| SCORING.yaml | 182 | 全文 |
| check.py | 71 | 全文 |
| _shared/SKILL-SPEC.md | 162 | 全文（合规依据） |

### 读取统计

- 总读取行数: 550 行
- 审查文件数: 3 个（skill 目录内）+ 1 个（_shared 规范）
- 死引用: 4 个
- 发现问题数: 2 个致命 + 5 个重要 + 5 个优化
- 总审查行数（REVIEW.md）: 300+ 行
