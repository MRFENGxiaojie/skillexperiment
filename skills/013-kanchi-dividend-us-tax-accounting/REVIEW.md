# REVIEW: 013-kanchi-dividend-us-tax-accounting

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 美国股息税务分类与账户配置规划工作流，面向 Kanchi 风格收益型投资组合，涵盖从分类→持有期验证→税务表格映射→账户配置→年度备忘录的完整 5 步流程
**Body 行数**: 116 行（不含 frontmatter）
**参考文件数**: references/4, scripts/3, agents/1（共 8 个非核心文件）
**已有 REVIEW**: 是（旧版 22 行 stub，本次完全重写至 ≥500 行）

---

## 1. 目录全量清单

本 skill 目录共含 12 个文件（不含 REVIEW.md）：

```
D:\SkillIF\skill-experiment\complex-skills\013-kanchi-dividend-us-tax-accounting\
├── SKILL.md (120 行)                                    ← 主体：Overview + When to Use + Prerequisites
│                                                          + Guardrails + 5步Workflow + Output
│                                                          + Cadence + Multi-Skill Handoff + Resources
├── SCORING.yaml (170 行)                                ← 18 criteria (scope/process/output/principles/
│                                                          negative/qa) + 2 critical_failures
├── check.py (91 行)                                     ← 可执行检测器，7个script检查项
│                                                          调用 _shared/checker.py 的 json_field_exists,
│                                                          tool_log_contains, output_contains
├── agents/
│   └── openai.yaml (4 行)                               ← 🟡 非标准文件：display_name + short_description
│                                                          SKILL.md 中从未提及，可能为自动化工具链残留
├── references/
│   ├── input-schema.md (33 行)                          ← JSON 输入 schema：5个字段定义 + 默认值策略
│   │                                                      + 缺失数据处理规则
│   ├── qualified-dividend-checklist.md (53 行)          ← 分类检查清单：3步验证 + IRS 合规基准
│   │                                                      (60/121天 common, 90/181天 preferred)
│   │                                                      + 7个跟踪字段 + 4个陷阱 + 信源层次
│   ├── account-location-matrix.md (31 行)               ← 配置矩阵：5类工具的 taxable vs IRA 决策表
│   │                                                      + 冲突解决优先级(风控>流动性>税务)
│   │                                                      + 单行输出格式规范
│   └── annual-tax-memo-template.md (42 行)              ← 备忘录模板：8节Markdown结构
│                                                          (Filing Timeline→Scope→Assumptions→
│                                                          Classification→Actions→Risks→Advisor Qs)
└── scripts/
    ├── build_tax_planning_sheet.py (186 行)             ← 核心脚本：@dataclass PlanningRow 数据模型
    │                                                      + classify_holding() 分类引擎
    │                                                      + render_markdown()/write_csv() 双格式输出
    │                                                      + argparse CLI (--input, --output-dir, --as-of)
    └── tests/
        ├── conftest.py (7 行)                            ← pytest 路径配置 (sys.path.insert)
        └── test_build_tax_planning_sheet.py (76 行)     ← 4个单元测试：合格分类、缺失天数、
                                                             MLP排除、Markdown/CSV生成验证
```

**文件统计**: 共 12 个文件（不含 REVIEW.md）。核心资产齐全：4 个 reference 文件构成完整的税务规划知识库，1 个功能完整的 Python 脚本（含 4 个单元测试）。`agents/openai.yaml` 为非标准残留文件，在 SKILL-SPEC.md 中没有任何规定。

**目录健康度**: 结构良好，references/ 和 scripts/ 子目录各司其职，测试文件隔离在 scripts/tests/ 中。唯一的不洁点是 `agents/` 目录——仅含 1 个 4 行的 `.yaml` 配置文件，占用一个子目录名。

---

## 2. Frontmatter 逐字段审查

### 2.1 name 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 小写 + 连字符 | ✅ | `kanchi-dividend-us-tax-accounting` |
| ≤64 字符 | ✅ | 38 字符 |
| 与目录名匹配 | ✅ | 目录 `013-kanchi-dividend-us-tax-accounting`，去掉 NNN- 前缀后完全一致 |

"kanchi" 前缀表明这是 Kanchi 投资方法论系列 skill 之一，系列化命名是合理的组织方式。

### 2.2 description 字段逐句分析

**原文**（327 字符，含空格）：

> "Provide US dividend tax and account-location workflow for Kanchi-style income portfolios. Use when users ask about qualified vs ordinary dividends, 1099-DIV interpretation, REIT/BDC distribution treatment, holding-period checks, or taxable-vs-IRA account placement decisions for dividend assets."

**句子 1** — WHAT 声明:
"Provide US dividend tax and account-location workflow for Kanchi-style income portfolios."

- 主语为 skill（"Provide"），第三人称描述功能 ✅
- 功能声明具体明确：US dividend tax + account-location workflow ✅
- "Kanchi-style income portfolios" 是领域特定术语——指 Kanchi 投资方法论的收益型投资组合。对有领域知识的 agent 来说是可理解的领域信号，对没有该知识的 agent 来说不会产生误导（它仍然知道这是一个 dividend tax workflow）✅
- 无祈使句、无第一/第二人称 ✅

**句子 2** — WHEN + KEYWORDS 声明:
"Use when users ask about qualified vs ordinary dividends, 1099-DIV interpretation, REIT/BDC distribution treatment, holding-period checks, or taxable-vs-IRA account placement decisions for dividend assets."

- 🟡 "Use when users ask" — 使用了 "users"（复数）而非规范 §2.4 标准形式中的 "the user"（单数）。规范列出的五个标准形式为 "Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."。此处 "users" 为轻微人称偏差，不构成功能性违规——agent 仍然能识别 "Use when" 触发信号——但不符合规范的精确措辞
- 5 个触发场景精确列举，每个都是具体的用户意图：qualified vs ordinary dividends、1099-DIV interpretation、REIT/BDC distribution treatment、holding-period checks、taxable-vs-IRA account placement decisions ✅
- KEYWORDS 自然嵌入 WHEN 句中：qualified dividends、ordinary dividends、1099-DIV、REIT、BDC、holding-period、IRA——领域词密度高，有助于 agent 匹配用户意图 ✅
- 具体到税务表格名称（1099-DIV）和投资工具类型（REIT, BDC），不是模糊的"税务帮助" ✅

**禁止内容检查**:
- 无第一人称（I/we）✅
- 无祈使句开头（"Use this skill to..."）✅
- 无跨 skill 路由（"NOT for X, use Y instead"）✅
- 无实现细节、无模糊描述 ✅
- 长度 327 字符，远低于 1024 字符上限 ✅

**description 综合评分**: 8/10。内容质量高——WHAT 具体、WHEN 精确（5 个触发场景）、KEYWORDS 丰富。仅 "users" → "the user" 一处可优化的措辞偏差。

**修改建议**: 将 "Use when users ask about" 改为 "Use when the user asks about"，与规范 §2.4 的标准形式保持一致。

### 2.3 allowed-tools 字段

🔴 **完全缺失**。Frontmatter 仅含 `name` 和 `description` 两个字段。

详细分析 skill 实际需要的工具及其在 body 中的使用证据：

| Tool | 必要性 | Body 中的使用证据 |
|------|:------:|------------------|
| Read | ✅ 必须 | 读取 4 个 reference 文件（L29, L53, L76, L85 明确引用）；读取输入 JSON 文件 |
| Write | ✅ 必须 | Step 5 生成年度税务规划备忘录（L83-89）；Output 要求输出 4 类交付物 |
| Bash | ✅ 必须 | L34-37 运行 `build_tax_planning_sheet.py` 生成确定性产出物；L97-98 引用脚本路径 |
| Glob | 🟡 推荐 | 自动发现 `tax_input.json` 文件；查找 reports/ 目录下的历史版本 |

推荐值：`allowed-tools: Read, Write, Bash, Glob`

虽然在 SKILL-SPEC.md v1.0 中 `allowed-tools` 列为"可选"，但在现代 Claude Code 环境中，没有工具声明可能导致 agent 被工具限制阻挡——特别是 Bash 工具，没有它则无法运行核心的分类脚本。

### 2.4 其他 Frontmatter 字段

| 字段 | 存在 | 评估 |
|------|:----:|------|
| `model` | ❌ | 未设置——合理。税务分类不需要特定模型覆盖 |
| `argument-hint` | ❌ | 未设置。skill 通过自然语言触发而非命令行参数，合理 |
| `user-invocable` | ❌ | 未设置。适合用户直接调用，建议设为 `true` |
| `paths` | ❌ | 未设置。不基于文件路径触发 |
| 禁止字段 | ❌ | 无任何 SKILL-SPEC §1.3 列出的禁止字段 ✅ |

### 2.5 Frontmatter 语法

YAML 分隔符 `---` 成对出现 ✅。description 值无需要转义的特殊字符 ✅。无缩进错误 ✅。纯字符串值，无嵌套引号问题 ✅。

---

## 3. Body 逐段结构分析

### 3.1 完整段落树（含每节估计行数）

```
L6   # Kanchi Dividend Us Tax Accounting               — H1 标题
L8   ## Overview (6行)                                  — 核心理念声明：实用工作流+可审计+非法律建议
L13  ## When to Use (7行)                               — 4个触发场景（分类规划/持有期检查/账户配置/年度备忘录）
L21  ## Prerequisites (13行)                            — 4个必需输入字段 + JSON schema引用 + Bash命令
L29                                                     — 🔴 Bash命令使用repo-root路径格式
L39  ## Guardrails (4行)                                 — 税务免责声明（"not legal/tax advice replacement"）
L44  ## Workflow (46行)                                  — 🟢 5步工作流（核心Process节）
L46   ### 1) Classify each distribution stream (10行)   — 3类分布：qualified/ordinary/REIT-BDC
L56   ### 2) Validate holding-period eligibility (8行)  — 3项验证 + ASSUMPTION-REQUIRED标记
L65   ### 3) Map to reporting fields (9行)              — 3类税务表格字段：Ordinary total/Qualified subset/REIT
L74   ### 4) Build account-location recommendation (9行) — 矩阵驱动的taxable vs IRA配置 + 冲突解释
L83   ### 5) Produce annual planning memo (8行)          — 4项备忘录内容（assumptions/classification/placement/open items）
L91  ## Output (9行)                                     — 🟢 4项输出要求（分类表+配置表+风险清单+脚本产物）
L100 ## Cadence (6行)                                    — 3种时间节奏：年度60min/季度15min/临时
L107 ## Multi-Skill Handoff (6行)                        — 3个上下游skill的交接协议（kanchi-dividend-sop等）
L113 ## Resources (8行)                                   — 5个文件引用（scripts×2 + references×3）
```

**结构评价**: 逻辑流从宏观到微观清晰递进——先声明理念（Overview）→ 列出适用场景（When to Use）→ 准备输入（Prerequisites）→ 设置安全边界（Guardrails）→ 执行核心流程（Workflow 5步）→ 定义产出（Output）→ 嵌入人类节奏（Cadence）→ 协调上下游（Multi-Skill Handoff）→ 索引资源（Resources）。这是一个完整的"理念→场景→输入→安全→流程→输出→节奏→协作→资源"认知模型。

### 3.2 必需章节检查（详细）

**Workflow/Process 节**: ✅ 存在且质量高。"Workflow" (L44-89)，包含 5 个有序步骤，使用 `1) — 5)` 编号风格。每步的特点：
- Step 1 (Classify): 引用 `references/qualified-dividend-checklist.md` 作为分类依据——将决策规则委托给 reference 而非 body 中内联，保持 body 简洁 ✅
- Step 2 (Validate): 3 项持有期验证（ex-dividend windows、minimum holding days、at-risk flagging）。包含明确的 else 分支——"If data is incomplete, mark status as ASSUMPTION-REQUIRED" ✅
- Step 3 (Map): 映射到税务表格字段，使用 "form terminology consistently"——强调一致性 ✅
- Step 4 (Location): 引用 `references/account-location-matrix.md` 作为配置决策依据。包含冲突处理规则——"When constraints conflict...explain the tradeoff explicitly" ✅
- Step 5 (Memo): 引用 `references/annual-tax-memo-template.md`，列出 4 项备忘录必须包含的内容 ✅

**Output Format 节**: ✅ 存在。"Output" (L91-98)，列出 4 项具体输出要求：
1. Holding-level distribution classification table
2. Account-location recommendation table with rationale
3. Open-risk checklist for unresolved tax assumptions
4. Optional generated artifacts from build_tax_planning_sheet.py

输出描述具体可验证——分类表、配置推荐表（含理由）、风险检查清单都是明确的、可被 SCORING.yaml 的 script judge 检查的产出物。第 4 项 "Optional generated artifacts" 说明了脚本产出的可选的定位——agent 可以手动执行分类，脚本是自动化辅助而非强依赖 ✅。

**Scope/Limitations 节**: 🟡 无独立节。当前边界相关信息分布在：
- "Guardrails" (L39-42): "tax outcomes depend on individual facts and jurisdiction...Treat this skill as planning support, then escalate final filing decisions to a tax professional." ——这是合规必需的免责声明，说明 skill 的输出**不是**最终税务建议，但不是完整的范围声明
- "When to Use" (L13-19): 正向触发列表，没有说"不做什么"
- account-location-matrix.md 中的 MLP 行: "If MLP is outside mandate, mark it explicitly as OUT-OF-SCOPE" ——暗示了范围限制但未在 body 中声明

应增加独立的 `## Limitations` 节，明确声明：
- 不替代持牌税务专业人士（CPA/税务律师）的判断——这是法律要求
- 不涵盖国际税务或非美国税务管辖区
- 不涵盖实际税务申报表（Form 1040 等）的准备和提交
- MLP (Master Limited Partnership) 相关配置标记为 OUT-OF-SCOPE——因为涉及 K-1 和 UBTI 复杂性
- 该 skill 是"planning support"工具，最终申报决策由税务专业人员做出

### 3.3 内容委托分析

对 reference 文件的委托点统计：

| 委托点 | SKILL.md 行号 | 委托内容 | 合理性 |
|--------|:------------:|---------|:------:|
| input-schema.md | L29 | JSON 输入格式定义 | ✅ 合理——schema 是独立的知识单元 |
| qualified-dividend-checklist.md | L53-54 | 分类规则和持有期检查 | ✅ 合理——IRS 规则是参考材料 |
| account-location-matrix.md | L76 | 配置决策矩阵 | ✅ 合理——矩阵是查阅型内容 |
| annual-tax-memo-template.md | L85 | 备忘录模板 | ✅ 合理——模板是格式参考 |
| build_tax_planning_sheet.py | L34, L97-98, L115 | 脚本执行 | ✅ 合理——代码是独立执行单元 |

委托行数：~15 行（引用指令 + Resources 列表）。Body 总行数：116 行。委托比例：15/116 ≈ 13%。

**评估**: ✅ 委托比例合理。Body 包含完整的 5 步工作流——每步说明了做什么、用什么 reference 作为依据、产生什么中间输出。Agent 可以仅凭 body 理解整体流程和方法论，reference 文件提供执行所需的细节知识（分类规则、配置矩阵、模板结构）。这是教科书级的模块化设计——body 是流程骨架和决策路由，references 是知识库。

但有一个关键缺陷：Bash 命令（L34）使用 repo-root 路径 `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`，而非相对路径 `scripts/build_tax_planning_sheet.py`。Agent 不知道其工作目录在哪里——repo-root 路径在大多数部署环境中都是无效的。

### 3.4 节编号与标题层级

- H1 (L6) → H2 (L8, L13, L21, L39, L44, L91, L100, L107, L113) → H3 (L46, L56, L65, L74, L83) ✅
- 层级连续，无跳级 ✅
- Workflow 的 5 个子步骤使用 `### 1) — 5)` 编号，使用右括号而非点号，风格统一 ✅
- Resources 使用无序列表 ✅
- 无重复标题 ✅

### 3.5 Body 长度合规

116 行 body，远低于 600 行硬上限 ✅。对于 process 型 skill（规范建议 ~200 行），116 行偏薄但内容密度高——5 步工作流 + Output + Cadence + Multi-Skill Handoff + Resources，每步简洁但有实质内容。相比同类型的 008-tdd-workflow（149 行）和 005-project-analyze（171 行），116 行略显精炼但非不足。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析（逐对检查）

**Step 1 → Step 2**: Classify → Validate

Step 1 产生每个持仓的初步分类（potential qualified / ordinary / REIT-BDC）。Step 2 对潜在合格分类进行持有期验证。衔接逻辑：Step 1 的分类是一个**假设**（"potential qualified dividend"），Step 2 用 IRS 持有期规则**验证**这个假设。分类→验证是自然的因果链。Step 1 的输出（分类标签）被 Step 2 消费（仅对 "potential qualified" 的持仓进行持有期检查）。✅

**Step 2 → Step 3**: Validate → Map

Step 2 产生验证后的状态（qualified / ordinary / ASSUMPTION-REQUIRED）。Step 3 将验证后的分类映射到预期的税务表格字段（Ordinary dividend total / Qualified dividend subset / REIT-related components）。衔接逻辑：验证后才知道每个分布流属于哪个税务表格字段。Step 2 的输出（分类状态）是 Step 3 的输入（决定映射到哪个字段）。✅

**Step 3 → Step 4**: Map → Location

Step 3 产生每个持仓的税务特征（主要是 ordinary vs qualified 比例）。Step 4 基于税务特征和 account-location-matrix.md 做出 taxable vs tax-advantaged 配置推荐。衔接逻辑：税务特征决定账户配置——qualified-heavy 持仓适合 taxable 账户（税收效率更高），ordinary-income-heavy 持仓适合 tax-advantaged 账户（避税）。Step 3 的输出（税务特征）是 Step 4 的决策依据。✅

**Step 4 → Step 5**: Location → Memo

前 4 步的所有分析结果——分类、验证状态、表格映射、配置推荐——在 Step 5 中编译为标准化年度备忘录。衔接逻辑：综合输出。Step 5 消费前 4 步的全部输出并按照 annual-tax-memo-template.md 的结构组织。✅

**总体**: 5 步形成完整的 "分类假设 → 资格验证 → 表格映射 → 配置决策 → 备忘录输出" 闭环。每步的输出是下一步的输入，无跳跃、无重复、无死循环。这是本 skill 最强的设计特点。

### 4.2 内部矛盾扫描

**矛盾点 1 — 路径格式不一致**:

这是本 skill 最主要的不一致问题。SKILL.md 中使用两种不同的路径格式：

| 位置 | 路径格式 | 示例 |
|------|---------|------|
| L34 (Bash 命令) | repo-root 绝对路径 | `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py` |
| L53-54 (Step 1-2 reference) | 相对路径 | `references/qualified-dividend-checklist.md` |
| L76 (Step 4 reference) | 相对路径 | `references/account-location-matrix.md` |
| L85 (Step 5 reference) | 相对路径 | `references/annual-tax-memo-template.md` |
| L97-98 (Output 节) | repo-root 绝对路径 | `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py` |
| L115-116 (Resources 节) | repo-root 绝对路径 | `skills/kanchi-dividend-us-tax-accounting/scripts/...` |

references/ 文件全部使用正确的相对路径 ✅，但 scripts/ 文件全部使用 repo-root 路径格式 🔴。这种不一致来自早期的 skill 模板（"skills/<skill-name>/scripts/..." 是旧式语料库格式），在规范化过程中 references 被修正但 scripts 路径被遗漏。

**矛盾点 2 — 持有期天数表述微妙不统一**:

- qualified-dividend-checklist.md L16: "hold shares for **more than 60 days** during the **121-day period**"
- build_tax_planning_sheet.py L26-29: `required_days()` 对 common stock 返回 61，分类使用 `>= threshold` (即 `>= 61`)

两者的语义是完全一致的——"more than 60" 在整数天数的语境下等价于 "≥ 61"。但措辞方式不同：checklist 用自然语言的 "more than N"，代码用整数的 `>= N+1`。这在技术上是正确的（没有 bug），但在 skill 的可读性和可审计性上造成了轻微摩擦——人类读者在对照 checklist 和代码时可能会短暂困惑。建议统一为一致的表述方式。

**无其他内部矛盾** ✅：
- Guardrails 的 "not legal/tax advice replacement" 与 Output 中 "Open items for CPA/tax-advisor review" 一致
- Cadence 的时间估计（60min/15min/ad-hoc）与 5 步工作流的复杂度匹配
- Multi-Skill Handoff 中引用的 skill 名称（kanchi-dividend-sop, kanchi-dividend-review-monitor）与上下文的 "receive from / return to" 逻辑一致

### 4.3 示例与代码正确性

**Bash 命令**（SKILL.md L34-37）:
```bash
python3 skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py \
  --input /path/to/tax_input.json \
  --output-dir reports/
```

与 build_tax_planning_sheet.py 的实际 argparse 定义对比：
- `--input` (required=True) ✅ — 脚本确实接受 `--input` 参数
- `--output-dir` (default="reports") ✅ — 参数名和默认值匹配
- 除路径格式外，命令语法正确 ✅

**build_tax_planning_sheet.py 代码质量深度审查**（186 行）:

数据模型设计:
- `@dataclass PlanningRow` — 7 个字段的数据类，清晰定义了税务规划行的数据结构 ✅
- `required_days(security_type)` — 纯函数，返回 common stock 61 天、preferred stock 91 天。逻辑正确（>60 → ≥61, >90 → ≥91）✅

分类引擎 `classify_holding()`:
- REIT/BDC 分支（L45-53）→ `ordinary_likely` + `tax_advantaged_preferred` — 与 account-location-matrix.md 的 "REIT-heavy income holdings → Tax-advantaged account Often preferred" 一致 ✅
- MLP 分支（L55-64）→ `out_of_scope_mlp` + `case_by_case` — 与矩阵的 "Case-by-case, Caution in tax-advantaged accounts" 一致 ✅
- 缺失 hold_days 分支（L66-76）→ `assumption_required` + `taxable_preferred` — 与 SKILL.md Step 2 的 "If data is incomplete, mark status as ASSUMPTION-REQUIRED" 一致 ✅
- 正常分类分支（L78-93）→ 用 `required_days()` 阈值判断 qualified_likely vs ordinary_likely ✅

输出格式化:
- `render_markdown()` — 生成包含 as_of 时间戳、holding_count 统计、"Open Items" 部分的 Markdown 表格 ✅
- `write_csv()` — 正确使用 `csv.writer`，对 None 值写空字符串（避免 "None" 字面量污染 CSV）✅

错误处理:
- L167-168: `if not isinstance(holdings, list) or not holdings: raise SystemExit(...)` — 对空/非法输入有明确错误处理 ✅
- None hold_days 的 CSV 序列化：`row.hold_days_in_window if row.hold_days_in_window is not None else ""` ✅

命令行接口:
- `--as-of` 默认值使用 `date.today().isoformat()` — 良好的默认值，自动生成当天日期 ✅

**测试文件质量审查**（test_build_tax_planning_sheet.py, 76 行）:

4 个测试覆盖了核心场景：
1. `test_classify_stock_with_sufficient_days_is_qualified_likely` — JNJ common stock, 75 天 → qualified_likely ✅
2. `test_classify_missing_days_is_assumption_required` — PG stock, 无 hold_days → assumption_required ✅
3. `test_classify_mlp_is_out_of_scope` — ET MLP, 200 天 → out_of_scope_mlp (即使持有期充足，MLP 仍为 out_of_scope) ✅
4. `test_markdown_and_csv_generation` — 端到端测试：REIT(O) + stock(JNJ) → Markdown + CSV 输出验证 ✅

测试数据使用真实 ticker（JNJ, PG, ET, O）——有意义的测试用例，不是 `foo`/`bar` ✅。

🟡 导入路径依赖 `conftest.py` 的 `sys.path.insert` — 这是 pytest 的标准做法但脆弱。如果从项目根目录而非 scripts/ 目录运行 pytest，导入可能失败。

### 4.4 条件完整性

搜索所有 "if" / "when" / 条件分支：

| 条件 | 位置 | Else/Otherwise | 判定 |
|------|------|---------------|:----:|
| "If data is incomplete" | SKILL.md L63 (Step 2) | "mark status as ASSUMPTION-REQUIRED" | ✅ 明确的 else |
| "When constraints conflict (liquidity, strategy, concentration)" | SKILL.md L81 (Step 4) | "explain the tradeoff explicitly" | ✅ 冲突处理策略 |
| "If MLP is outside mandate" | account-location-matrix.md L15 | "mark it explicitly as OUT-OF-SCOPE" | ✅ 排除路径 |
| "When absent" (hold_days_in_window) | input-schema.md L28 | "emit assumption_required" | ✅ 缺失数据处理 |
| hold_days is None | build_tax_planning_sheet.py L67 | → assumption_required + taxable_preferred | ✅ 代码实现 |
| instrument_type is reit/bdc | build_tax_planning_sheet.py L45 | → ordinary_likely + tax_advantaged_preferred | ✅ 代码实现 |
| instrument_type is mlp | build_tax_planning_sheet.py L56 | → out_of_scope_mlp + case_by_case | ✅ 代码实现 |

条件覆盖充分 ✅。税务规划场景中的关键不确定性——数据缺失、投资工具类型超出范围、配置约束冲突——都有明确的处理路径。特别值得称赞的是 ASSUMPTION-REQUIRED 标记机制：它在所有不确定的情况下（数据不完整、hold_days 缺失、MLP out-of-scope）都强制 agent 显式声明不确定性，而非静默猜测。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

SKILL.md 中出现的每一个文件引用：

| 引用路径 | SKILL.md 行号 | 是否存在 | 文件行数 | 内容匹配度 |
|----------|:------------:|:--------:|:--------:|:---------:|
| references/input-schema.md | L29 | ✅ | 33 | 匹配 — 定义了 Prerequisites 中的 4 个字段 |
| references/qualified-dividend-checklist.md | L53-54 | ✅ | 53 | 匹配 — Step 1 的分类规则 + Step 2 的持有期检查 |
| references/account-location-matrix.md | L76 | ✅ | 31 | 匹配 — Step 4 的配置决策矩阵 |
| references/annual-tax-memo-template.md | L85 | ✅ | 42 | 匹配 — Step 5 的备忘录结构 |
| scripts/build_tax_planning_sheet.py | L34, L97-98, L115 | ✅ | 186 | 匹配 — 分类引擎的完整实现 |
| scripts/tests/test_build_tax_planning_sheet.py | L116 | ✅ | 76 | 匹配 — 4 个单元测试 |

6/6 引用全部存在 ✅。100% 引用率。但路径格式存在不一致——详见 §5.5。

### 5.2 不可见资源审计

目录中存在但 SKILL.md 中从未提及的文件：

**agents/openai.yaml（4 行）**:
- 内容：`display_name: "Kanchi Dividend Us Tax Accounting"` + `short_description: "Help with Kanchi Dividend Us Tax Accounting tasks"`
- 格式：简短的 YAML 键值对，`interface:` 为顶层键
- 分析：这是一个非标准文件。`agents/` 目录名和 `.yaml` 格式在 SKILL-SPEC.md v1.0 中没有任何规定。可能来源于某条自动化工具链（如 OpenAI Agents SDK 或类似的 agent 配置系统）的残留配置
- 如果 agent 不知道这个文件存在，后果：无——它是一个元数据配置文件（display_name + short_description），不包含任何 skill 执行逻辑，不影响 agent 的行为
- 建议：确认该文件的功能来源。如果无功能用途，移除以保持目录整洁；如果有用途，在 SKILL.md Resources 节中添加引用

**conftest.py（7 行）**:
- 内容：`sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))` — 将 scripts/ 父目录加入 Python 路径
- 分析：标准的 pytest 配置夹具。它不在 SKILL.md 中被引用是合理的——它是测试基础设施，不是 skill 的功能组件
- 判定：✅ 无需在 SKILL.md 中提及

### 5.3 Reference 文件全文审查

以下是对 4 个 reference 文件的逐一深度分析（已在本次审查中全文读取）：

**1. input-schema.md（33 行）— JSON 输入规范**

内容概要：定义了一个 JSON 输入格式，包含 `holdings` 数组，每个元素有 5 个字段——ticker (必需)、instrument_type (stock/reit/bdc/mlp, 默认 stock)、account_type (taxable/ira, 默认 unknown)、security_type (common/preferred, 默认 common)、hold_days_in_window (整数, 缺失时 emit assumption_required)。附带完整的 JSON 示例和每个字段的行为说明。

质量评价：✅ 优秀。默认值策略（"defaults to stock/common"）减少了输入摩擦——用户不需要为每个持仓指定所有字段。"UNKNOWN" ticker 标记和 "assumption_required" hold_days 策略体现了税务规划的谨慎性——不会在数据不完整时假装确定。"For a not-yet-owned candidate" 的特殊处理（故意省略 hold_days 以触发规划假设）展示了深度的领域理解。

问题列表：无。但建议在 JSON 示例中将 `hold_days_in_window: 75` 修改为实际可触发 qualified_likely 的值（≥61 for common）以提高示例的端到端可用性。

**2. qualified-dividend-checklist.md（53 行）— 合格股息分类检查清单**

内容概要：3 步分类验证流程（eligibility → holding-period → disqualifying conditions）+ IRS 合规基准（common: >60天/121天窗口, preferred: >90天/181天窗口）+ 7 个跟踪字段（Ticker, Account type, Ex-dividend date, Purchase date(s), Disposal date(s), Days held, Preliminary classification）+ 4 个常见陷阱（假设所有股息合格、忽略短期交易、等同 REIT/BDC、将特殊股息年度化）+ 3 级信息源层次（Broker documents → IRS publications → Issuer notices）。

质量评价：✅ 杰出——这是本 skill 最有价值的 reference 文件。持有期规则明确引用 IRS Publication 550 和 Form 1099-DIV 作为权威来源。"Common Pitfalls" 中的第 4 条——关于特殊/可变股息的处理——特别有深度：它不仅说明了问题，还定义了来自 kanchi-dividend-sop 的上游数据标记（`special_dividend_flag`, `variable_policy_flag`），并给出了具体的处理策略（"budget the regular run-rate as base income and the special/variable component separately"）。"Recommended Source Hierarchy" 将信息源按可靠性分层——这是一个在金融合规领域至关重要的设计。

问题列表：
- 🟡 持有期规则 "more than 60 days" (L16) 与脚本的 `>= 61` 语义一致但措辞不统一。建议在 checklist 中写成 "more than 60 days (i.e., at least 61 days)" 以消除歧义
- 🟡 Preliminary classification 的建议值 "qualified-likely" / "ordinary-likely" 使用连字符，而脚本输出的分类值使用下划线 "qualified_likely" / "ordinary_likely"——命名风格不一致

**3. account-location-matrix.md（31 行）— 账户配置矩阵**

内容概要：5 类投资工具的 Taxable vs Tax-advantaged 配置决策矩阵（详见表格）+ 3 级冲突解决优先级（Concentration/Risk > Liquidity > Tax optimization）+ 单行输出格式规范（`[Ticker] -> [Recommended Account] | Why: [one sentence]`）。

质量评价：✅ 优秀。矩阵的每行都包含 "Rationale" 列——不仅是 "放在哪个账户"，还解释了 "为什么"，这对于 agent 的决策透明性至关重要。冲突解决规则非常出色——明确声明 "Respect concentration and risk controls first. Respect liquidity/withdrawal constraints second. Optimize taxes third."。这个优先级顺序防止了 agent 过度追求税务优化而忽视投资风险和流动性需求——在金融 skill 中这是关键的 fiduciary 责任意识。

问题列表：
- 🟡 MLP 行 "Case-by-case" + "Caution in tax-advantaged accounts"——如果最终建议是 "Case-by-case"，agent 应该输出什么具体的配置建议？矩阵提供了警告（UBTI and K-1 complexity）但未给出决策流程。建议补充：当遇到 MLP 时，标记为 `OUT-OF-SCOPE`，列出需要人类评估的具体问题（K-1 状态、UBTI 阈值、基金结构），然后将决策升级给税务专业人员

**4. annual-tax-memo-template.md（42 行）— 年度备忘录模板**

内容概要：8 节 Markdown 模板——Filing Timeline（申报时间线）、Scope（覆盖范围）、Assumptions（使用的假设和规则版本）、Distribution Classification Summary（分类汇总表，含 Confidence 列）、Account-Location Actions（配置操作表）、Open Risks / Follow-Ups（开放风险和跟进项）、Advisor Questions（提交给 CPA/税务顾问的问题）。

质量评价：✅ 结构完整且专业。"Confidence" 列（High/Med/Low）是良好的不确定性管理实践——不假装每个分类都是确定的。"Advisor Questions" 节是最关键的设计——它显式地将 skill 无法回答的问题（需要人类专业判断的）转交给 CPA/税务顾问，这是税务规划 skill 的合规必需项。

问题列表：
- 🟡 所有表格中的占位符使用 "..." 而非示例数据。建议至少为第一行添加示例数据（如 "JNJ | taxable | $1,200 | $1,050 | — | High"），使模板更即时可用
- 🟡 "Filing Timeline" 节中的日期字段（Tax year, Filing deadline, Extension status）需要 agent 在运行时填充当前年份的信息——这是合理的动态模板设计，但建议添加注释说明这些字段的数据来源

### 5.4 Scripts 文件全文审查

**build_tax_planning_sheet.py（186 行）— 核心分类与输出脚本**

功能概要：接受 JSON 输入文件（holdings 列表），使用 `classify_holding()` 对每笔持仓执行分类（基于 instrument_type、hold_days、security_type），输出 Markdown 表格和 CSV 文件两种格式的税务规划表。

代码质量评价：✅ 优秀。
- 数据模型清晰：`@dataclass PlanningRow` 定义了 7 个字段的结构化输出
- 分类逻辑封装在纯函数 `classify_holding()` 中——无副作用、可测试
- 双格式输出（Markdown + CSV）实用——Markdown 适合人类阅读（可嵌入备忘录），CSV 适合数据处理和导入
- 错误处理：空/非法 holdings 抛出 `SystemExit`；None hold_days 在 CSV 中写空字符串
- 命令行接口标准：argparse 的 `--input`、`--output-dir`、`--as-of` 参数设计合理

问题列表：
- 🟡 `required_days("preferred")` 返回 91——与 checklist 的 "more than 90 days" 语义一致但建议在 docstring 中注明推导逻辑
- 🟡 `--output-dir` 默认值硬编码为 `"reports"`——如果 agent 的工作目录不是预期的，会在意外位置创建 reports/ 目录
- 🟡 脚本不接受 stdin 输入——仅接受文件路径 `--input`，限制了管道使用场景
- 🟢 建议：添加 `--format json` 输出选项以支持程序化消费

**test_build_tax_planning_sheet.py（76 行）— 单元测试**

功能概要：4 个 pytest 测试——验证合格分类逻辑、缺失天数处理、MLP 排除、Markdown/CSV 生成的端到端正确性。

代码质量评价：✅ 良好。测试命名遵循 Given-When-Then 风格（`test_classify_stock_with_sufficient_days_is_qualified_likely`），使用真实 ticker 提高可读性。`test_markdown_and_csv_generation` 同时验证两种输出格式的结构和内容——一个高价值的端到端测试。

问题列表：
- 🟡 导入路径 `from build_tax_planning_sheet import ...` 依赖 `conftest.py` 的 `sys.path.insert`——这是 pytest 的标准做法但脆弱
- 🟢 建议：增加一个测试覆盖 insufficient holding days 的场景（如 hold_days=30, common stock → ordinary_likely）

**conftest.py（7 行）— pytest 配置**

功能概要：将 scripts/ 父目录加入 sys.path 使测试能导入 build_tax_planning_sheet 模块。

代码质量评价：🟢 标准的 pytest 路径配置。内容极简、目的单一。

### 5.5 跨 Skill 引用检查

**路径引用格式**：

SKILL.md 中使用两种不同的路径格式，违反了 SKILL-SPEC §3.3 的相对路径规则：

- ❌ L34: `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py` — repo-root 绝对路径
- ❌ L97-98: `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py` — 同上
- ❌ L115-116: `skills/kanchi-dividend-us-tax-accounting/scripts/...` — 同上
- ✅ L29: `references/input-schema.md` — 正确的相对路径
- ✅ L53-54: `references/qualified-dividend-checklist.md` — 正确的相对路径
- ✅ L76: `references/account-location-matrix.md` — 正确的相对路径
- ✅ L85: `references/annual-tax-memo-template.md` — 正确的相对路径

这是本 skill 最需要修复的规范问题。repo-root 路径假设 agent 的工作目录恰好是 skill repo 的根——这在大多数部署场景中不成立。

**Prose 引用**（Multi-Skill Handoff 节，L107-111）:
- "kanchi-dividend-sop" — 上游 skill，prose 引用 ✅
- "kanchi-dividend-review-monitor" — 上游 skill，prose 引用 ✅

使用 skill 名称而非文件路径，符合规范 §3.3 的要求（"use its name in prose"）✅。

### 5.6 嵌套重复/死文件检查

- 无 self-nested 目录 ✅
- 无 `.gitkeep` 占位空目录 ✅
- `agents/openai.yaml` (4 行) 不是死文件（有有效内容）但是**非标准文件**——`agents/` 目录在 SKILL-SPEC.md 中无规定，占用了不必要的子目录

---

## 6. 语法与格式质量（逐问题列举）

### 6.1 拼写错误

无发现 ✅。全文拼写正确。专业税务术语使用准确：REIT (Real Estate Investment Trust), BDC (Business Development Company), MLP (Master Limited Partnership), UBTI (Unrelated Business Taxable Income), K-1 (Schedule K-1)。IRS 表格名称和出版物编号正确（1099-DIV, Publication 550）。

### 6.2 语法错误

- 主谓不一致：无 ✅。全文 subject-verb agreement 正确
- 时态混乱：无 ✅。全文统一使用现在时（"Provide", "Apply", "Focus on", "Use this skill when..."）和祈使/命令式（"Classify", "Validate", "Map", "Build", "Produce"）
- 残缺句：无 ✅。每个句子都有完整的主谓结构
- 悬垂修饰语：无 ✅

### 6.3 中英/葡英混杂

无 ✅。全文为纯英文。

### 6.4 Markdown 格式破损

逐项检查：

- 代码围栏：所有 ` ``` ` 正确配对 ✅（L5-6 frontmatter、L33-37 bash、L36 被 frontmatter 解析为围栏内容）
- 粗体标记：所有 `**...**` 正确闭合 ✅（qualified-dividend-checklist.md L39 的 "**Modeling special / variable dividends as steady qualified income**"）
- 列表编号：Workflow 5 步使用 `1) — 5)` 右括号风格，一致 ✅
- 表格格式：account-location-matrix.md 的 5 列表格语法正确 ✅。annual-tax-memo-template.md 的 5 列表格（含右对齐的数字列 `---:`）语法正确 ✅
- 链接格式：Resources 节使用裸文本（`` `path` ``）而非 Markdown 链接（`[text](path)`）——🟡 在不支持自动链接的渲染器中，裸文本不可点击。建议改为 `[build_tax_planning_sheet.py](scripts/build_tax_planning_sheet.py)`

### 6.5 占位符未填充

- SKILL.md L34: `/path/to/tax_input.json` — 示例路径占位符，合理 ✅（用户需要替换为实际路径）
- annual-tax-memo-template.md 表格: `...` — 表格占位符，建议添加一行示例数据 🟡
- 无 `TODO`、`FIXME`、`TBD` ✅
- 无 `{{PLACEHOLDER}}` 双花括号模板变量 ✅

### 6.6 截断内容

无 ✅。所有文件完整结束。SKILL.md 结束于 Resources 列表的最后一个条目（L119）。所有 reference 文件都有明确的结尾标记。脚本文件以 `if __name__ == "__main__": raise SystemExit(main())` 标准结尾。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

以下逐条对照 `_shared/SKILL-SPEC.md` 的全部 12 条规则：

| # | 规则 | 状态 | 详细说明 |
|---|------|:----:|---------|
| 1 | name 匹配目录名 | ✅ | `kanchi-dividend-us-tax-accounting` 匹配 `013-kanchi-dividend-us-tax-accounting` |
| 2 | description 第三人称 | ✅ | "Provide", "Use when users ask" — 主语为 skill |
| 3 | description 含触发短语 | ✅ | "Use when users ask about" — "Use when" 家族触发信号 |
| 4 | description ≤1024 字符 | ✅ | 327 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | 仅 name + description，无禁止字段 |
| 6 | body ≤600 行 | ✅ | 116 行 |
| 7 | Workflow/Process 节存在 | ✅ | "Workflow" — 5 个有序步骤，含明确的起始条件（Prerequisites）和终止条件（Output + Memo） |
| 8 | Output Format 节存在 | ✅ | "Output" — 4 项可验证的输出要求 |
| 9 | Scope/Limitations 节存在 | 🟡 | Guardrails 是合规免责声明但非完整范围边界，缺少"不做什么"的声明 |
| 10 | 无跨 skill 文件路径引用 | 🔴 | L34/L97-98/L115 使用 `skills/kanchi-.../scripts/...` repo-root 路径违反 §3.3 的相对路径规则 |
| 11 | allowed-tools 格式正确 | 🔴 | 完全缺失。如添加应为逗号分隔列表 `Read, Write, Bash, Glob` |
| 12 | 路径仅指向本 skill 目录内 | 🔴 | 路径虽指向本 skill 的文件但格式非相对路径。规范 §3.3 要求 "relative paths within the skill directory" |

**合规评分**: 9/12 通过，3 个红色失败。

3 个红色失败项高度相关——全部围绕路径格式和 allowed-tools 缺失。修复路径格式（将 3 处 repo-root 路径改为相对路径）即可解决 #10 和 #12。添加 allowed-tools 解决 #11。

---

## 8. 人机感评估

### 8.1 Emoji 审计

零 emoji 使用 ✅。在 SKILL.md body、所有 4 个 reference 文件、Python 脚本中均未发现任何 emoji 字符。

### 8.2 全大写/喊叫式语言

搜索 `STOP!`、`MANDATORY`、`CRITICAL`、`DO NOT`、`NEVER`、`ALWAYS`：

- "ASSUMPTION-REQUIRED"（SKILL.md L63, 多处）：功能性状态标记，作为一种数据分类标签使用——不是对 agent 的喊叫式命令 ✅
- "OUT-OF-SCOPE"（account-location-matrix.md L15）：功能性排除标记 ✅
- "UNKNOWN"（input-schema.md L21-22）：ticker 缺失时的占位值 ✅
- 无 "STOP!"、"MANDATORY"（全大写）、"DO NOT"、"NEVER"、"ALWAYS" 等喊叫式命令 ✅

使用频率：约 8 处全大写使用，全部为数据标记/分类标签，非喊叫式命令 ✅。

### 8.3 Persona 语气分析

整体语气判定：**审慎负责的税务顾问**——像一个有经验的 CPA/税务规划师在给客户做年度税务审查。

抽取 6 句代表性原文作为语气证据：

1. **L10-11**: "Apply a practical US-tax workflow for dividend investors while keeping decisions auditable. Focus on account placement and classification, not legal/tax advice replacement."
   — 以 "practical"（实用）和 "auditable"（可审计）锚定基调。后半句的 "not legal/tax advice replacement" 明确划出边界——这是金融 skill 的责任性语言。

2. **L41-42**: "Always state this clearly: tax outcomes depend on individual facts and jurisdiction. Treat this skill as planning support, then escalate final filing decisions to a tax professional."
   — 免责声明语气果断但不恐慌。"Always state this clearly" 确保 agent 在每次交互中都传达这条边界。"escalate"（升级）一词将决策权归还给人类专业人员。

3. **L63**: "If data is incomplete, mark status as ASSUMPTION-REQUIRED."
   — 不确定性管理的工程化方法。不是 "try to guess" 或 "assume the best case"，而是显式标记不确定性——这在税务合规中至关重要。

4. **L81**: "When constraints conflict (liquidity, strategy, concentration), explain the tradeoff explicitly."
   — 承认现实世界的复杂性，要求 agent 做透明的权衡分析而非隐藏冲突。这体现了对 agent 能力的恰当期望——agent 可以分析 tradeoff，但不应单方面做决定。

5. **qualified-dividend-checklist.md L39-46**: 关于特殊/可变股息的详细陷阱说明——从 kanchi-dividend-sop 的上游数据标记谈到具体的预算分离策略。语气从 "These are the rules" 转变为 "Here's a nuanced edge case and how to handle it"。
   — 这表明 skill 作者有深度的领域知识且不回避复杂性。

6. **account-location-matrix.md L19-21**: "Respect concentration and risk controls first. Respect liquidity/withdrawal constraints second. Optimize taxes third."
   — 短句、平行结构、明确的优先级。这是一个经验丰富的投资顾问的 wisdom distilled into three lines。

**语气适配性评分**: 9/10。非常适合金融/税务规划场景。专业但不傲慢，谨慎但不瘫痪，实用但不牺牲合规。

### 8.4 人机边界分析

本 skill 的人机边界设计是**全语料库最佳之一**。逐项分析：

- ✅ **Guardrails (L39-42)**: 明确声明 skill 输出为 "planning support"，最终申报决策 "escalate to a tax professional"。这不是一个模糊的 disclaimer——它要求 agent "Always state this clearly"，确保边界在每次交互中都被传达
- ✅ **ASSUMPTION-REQUIRED 机制**: 在数据不完整时（hold_days 缺失、MLP out-of-scope），不猜测、不假设、不静默填补——显式标记不确定性。这是 "agent 应该识别自己知识的边界" 的具体实现
- ✅ **Cadence (L100-105)**: 将人类审查嵌入工作流节奏——年度 60min 全面审查、季度 15min 快速刷新、临时触发。这不是 agent 自治运行，而是 agent 辅助人类按节奏执行
- ✅ **annual-tax-memo-template.md "Advisor Questions" 节**: 在备忘录末尾显式留出 "提交给 CPA 的问题" 空间——这是人类决策的正式接收区
- ✅ **Multi-Skill Handoff (L107-111)**: 与上下游 skill 的交接协议清晰——接收什么输入、返回什么输出。这防止了 agent 在 skill 边界处的越权行为
- ✅ **Conflict Resolution (account-location-matrix.md L19-21)**: 在不冲突时按矩阵推荐，在冲突时显式解释权衡——agent 不被允许在冲突时自行决定最优策略

**是否存在过度自动化倾向**: 否。Skill 在每一个需要人类判断的节点（数据不确定、配置冲突、最终申报）都有明确的升级/标记机制。

**是否存在硬编码的人类偏好**: 无。没有硬编码的姓名、偏好或特定于某个人的设置。

### 8.5 人称分析

- 第二人称（you/your）：0 处在 SKILL.md body 中 ✅
- 第一人称（I/we）：0 处在 SKILL.md body 中 ✅
- description 中 "users"（L3）：🟡 应为 "the user"，轻微人称偏差（见 §2.2）
- Body 中的祈使句（"Classify", "Validate", "Map" 等）：在 workflow 步骤中使用祈使句是合理的操作指令 ✅

### 8.6 表格密度检查

- SKILL.md body：0 个表格 ✅（全部使用列表和段落）
- account-location-matrix.md：1 个表格（5 行 × 4 列，功能性决策矩阵）✅
- annual-tax-memo-template.md：2 个表格（Distribution Classification Summary + Account-Location Actions，占位符格式）✅

共 3 个表格，全部在 reference 文件中且功能性强 ✅。符合用户偏好。

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 agent 只拿到了 SKILL.md（没有目录探索能力），能否开始工作？

Agent 能够从 body 中获取的信息：
- ✅ 完整的 5 步工作流，每步有明确的做什么 + 引用哪个 reference 文件作为执行依据
- ✅ 4 项输出要求和格式
- ✅ 税务免责声明和 ASSUMPTION-REQUIRED 机制
- ✅ 与上下游 skill 的交接协议
- 🟡 Body 不包含分类规则和配置矩阵的具体内容——这些在 reference 文件中。但 SKILL.md 中的引用路径正确（references 使用相对路径），agent 可以按路径读取
- 🔴 Bash 命令的 repo-root 路径可能无效——agent 可能无法定位和执行脚本

**独立可执行性评分**: 7/10。工作流逻辑完整、输出定义清晰、reference 文件齐全并可访问。扣分来自路径格式问题和缺少 allowed-tools。

### 9.2 步骤可操作性（逐步骤评估）

| Step | SKILL.md 描述 | 可操作性 | 详细分析 |
|------|-------------|:--------:|---------|
| 1 Classify | 将每笔持仓的现金流分类为 qualified/ordinary/REIT-BDC | 🟢 | 引用 qualified-dividend-checklist.md 提供具体的分类规则和 IRS 基准。Agent 有明确的决策依据 |
| 2 Validate | 检查 ex-dividend 窗口、持有天数、风险标记 | 🟢 | 明确的 3 项验证 + ASSUMPTION-REQUIRED else 分支。checklist 提供了精确的天数阈值 |
| 3 Map | 将分类映射到税务表格字段（Ordinary total/Qualified/REIT） | 🟢 | 3 个字段有明确的语义定义。要求 "use form terminology consistently" 确保一致性 |
| 4 Location | 基于矩阵做出 taxable vs IRA 配置推荐 | 🟢 | account-location-matrix.md 提供 5×3 决策矩阵。冲突时 "explain the tradeoff explicitly" 给出明确的处理策略 |
| 5 Memo | 按模板生成包含 4 项内容的年度备忘录 | 🟢 | annual-tax-memo-template.md 提供 8 节完整模板结构。每节有具体的占位符，agent 只需填充 |

全部 5 步均为 🟢 可操作 ✅。每步都有明确的：做什么（WHAT）、用什么规则（REFERENCE）、产生什么（OUTPUT）。

### 9.3 工具依赖合理性

| 需要的工具 | 是否声明 | 分析 |
|-----------|:------:|------|
| Read | ❌ | 必须——读取 4 个 reference 文件和输入 JSON |
| Write | ❌ | 必须——Step 5 生成年度备忘录 |
| Bash | ❌ | 必须——运行 build_tax_planning_sheet.py 生成确定性产出物 |
| Glob | ❌ | 推荐——自动发现 tax_input.json 和报告目录 |
| `python3` | N/A (外部运行时) | 合理——Python 是数据处理的标准语言 |
| IRS Publication 550 | N/A (reference 引用) | 合理——仅作为知识引用，非运行时依赖 |

🔴 核心问题：4 个必需/推荐工具无一在 allowed-tools 中声明。

**脚本回退方案**: 如果 `build_tax_planning_sheet.py` 不可用（路径无效或 Python 环境缺失），agent 可以按照 reference 文件中的分类规则手动执行分类和输出——这是良好设计的体现：脚本是自动化辅助，不是唯一执行路径。Output 节也明确标注脚本产物为 "Optional generated artifacts"。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

18 个 criteria，按类别分布：

| 类别 | 数量 | 评判方式 | 与 SKILL.md 的对应关系 |
|------|:----:|:--------:|----------------------|
| scope | 3 | 2 llm + 1 script | SCOPE-01/02 验证税务规划边界；SCOPE-03 检查 JSON 输入字段——对应 Prerequisites 和 input-schema.md ✅ |
| process | 6 | 4 llm + 2 script | PROC-01/02/04/05 精确对应 Workflow Step 1/2/3/4；PROC-03 检查 "ASSUMPTION-REQUIRED" 标记；PROC-06 检查 "Assumptions used" 和 "Open Items" ✅ |
| output | 4 | 3 script + 1 llm | OUT-01/03/04 对应 Output 节的 4 项要求；OUT-04 检查 tool_log 含 "build_tax_planning_sheet" ✅ |
| principles | 2 | 2 llm | PRI-01 guardrail 声明检验；PRI-02 冲突解释检验——对应 Guardrails 和 Step 4 的冲突处理 ✅ |
| negative | 2 | 2 llm | NEG-01 "不声称合格未经验证"——对应 Step 2；NEG-02 "不呈现为最终建议"——对应 Guardrails ✅ |
| qa | 1 | 1 script | QA-01 检查输出含 "CPA|tax advisor|tax professional" ✅ |

**一致性**: 所有 18 个 criteria 与 SKILL.md 内容一一对应 ✅。无脱节或不可判定的检查项。

**Script vs LLM 分工**:
- Script judge (7 项): SCOPE-03, PROC-03, PROC-06, OUT-01, OUT-03, OUT-04, QA-01 — 检查文件/输出中的确定性字段和模式
- LLM judge (11 项): 语义判断——分类是否正确、guardrail 是否声明、冲突是否解释等

分工合理：机械检查（字段存在性、模式匹配）由脚本执行，语义判断（分类质量、guardrail 措辞）由 LLM 执行 ✅。

### 10.2 Critical Failures 分析

**CF-01**: "Agent classifies distributions as qualified without running holding-period checks"
- 触发条件：agent 在没有验证持有期资格的情况下声称股息 qualified
- 合理性：✅ 精确对应 Workflow Step 2 和 qualified-dividend-checklist.md。这是税务规划中最危险的错误——错误地将 non-qualified 股息分类为 qualified 可能导致纳税人面临 IRS 罚款和利息
- 效应：cap_to_0——触发则总分归零。✅ 合理——这个错误的后果如此严重，以至于发生一次就应视为整个 skill 遵从失败

**CF-02**: "Agent presents the output as definitive tax advice without the guardrail disclaimer"
- 触发条件：agent 将输出呈现为确定的税务建议而非规划支持
- 合理性：✅ 精确对应 Guardrails 节和 NEG-02。缺失免责声明不仅是规范问题——在极端情况下可能引发法律问题（如果用户将 agent 输出误解为正式税务建议并据此行动）
- 效应：cap_to_0——✅ 合理

两 CF 设计精良且精确锚定 skill 的核心安全保障。每个 CF 都直接追溯到 SKILL.md 中的具体内容和 SCORING.yaml 中的对应 NEG 检查项。

**遗漏的 CF**: 建议增加 CF-03——"Agent makes account-location decisions when constraints conflict without explaining the tradeoff explicitly"（对应 Step 4 的冲突处理规则和 PRI-02）。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**（skill-dossier.md Batch 011-025, 编号 013）:

> **013-kanchi-dividend-us-tax-accounting**
> - **逻辑**: 分类→持有期→报告字段→账户位置→备忘录工作流连贯，护栏和多 skill 交接集成良好，但资源路径写作 repo-root 路径而非相对路径
> - **语法**: 干净、专业文体；无错字
> - **人机感**: 审慎负责的顾问语气；恰当谨慎而不机械
> - **合规**: Description 第三人称含触发，body 119 行，workflow 和 output 节存在，但无 Scope 节（护栏是免责声明而非范围）和自我引用的非相对路径
> - **总评**: 🟡 补 Scope 节并将路径规范为相对引用

**逐项验证**:

| Dossier 发现 | 当前状态 | 验证结果 |
|-------------|:------:|---------|
| Repo-root 路径格式 | 🔴 仍存在 | L34, L97-98, L115 仍使用 `skills/kanchi-.../scripts/...` |
| 无 Scope 节 | 🟡 仍存在 | "Guardrails" 是免责声明而非范围边界 |
| 5 步工作流连贯 | ✅ 仍正确 | 步骤衔接分析（§4.1）确认无退化 |
| 护栏和多 skill 交接良好 | ✅ 仍正确 | Guardrails + Multi-Skill Handoff 经审查验证为高质量设计 |
| 语法干净 | ✅ 仍正确 | 全文拼写/语法审查（§6）确认无新增错误 |

**Dossier 遗漏的增量发现**（本次审查新发现）:
1. 🔴 allowed-tools 完全缺失——dossier 未提及
2. 🟡 路径格式不一致——references 用相对路径 ✅，scripts 用 repo-root 路径 🔴，dossier 只提了 "repo-root 路径" 但未指出不一致性
3. 🟡 agents/openai.yaml 为非标准文件且在 SKILL.md 中未提及——dossier 未提及
4. 🟡 description 中 "users" → 应为 "the user"——dossier 未提及
5. 🟡 持有期天数在 checklist（"more than 60 days"）和脚本（`>= 61`）中措辞不统一——dossier 未提及
6. 🟢 build_tax_planning_sheet.py 代码质量优秀，测试覆盖良好——dossier 未评估（dossier 不涉及脚本审查）
7. 🟢 人机边界设计为全语料库最佳之一——dossier 评价 "审慎负责" 但未强调这一点

**Dossier 评级评估**: Dossier 给出的 🟡 评级**准确**。主要问题（路径格式、Scope 缺失）仍然存在。但 dossier 低估了本 skill 的优势——人机边界设计、脚本代码质量和 reference 文件深度都超出了 dossier 简评所暗示的水平。本次审查的综合评分 78/100 (B+) 反映了本 skill 的内容实力。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 详细说明 |
|------|:----:|:----:|:----:|---------|
| Frontmatter 合规 | 6/10 | 10% | 0.60 | desc 内容优质（8/10）但 allowed-tools 完全缺失🔴，扣 4 分 |
| Body 结构完整 | 8/10 | 10% | 0.80 | Workflow (5步) + Output (4项) 齐全且质量高。Scope 不独立——Guardrails 是免责声明非范围边界，扣 2 分 |
| 逻辑一致性 | 9/10 | 20% | 1.80 | 5 步衔接自然流畅，分类→验证→映射→配置→备忘录形成完整闭环。Guardrails/ASSUMPTION-REQUIRED/Cadence 内部一致。仅路径格式不一致和持有期措辞微瑕，扣 1 分 |
| 参考完整性 | 9/10 | 15% | 1.35 | 6/6 引用全部存在（100%）。4 个 reference 文件质量杰出。仅路径格式不一致和 openai.yaml 未提及，扣 1 分 |
| 语法格式 | 9/10 | 10% | 0.90 | 全文拼写/语法/标点近乎完美。仅 "users"→"the user" 和 Resources 节裸文本链接可改进，扣 1 分 |
| 规范合规 | 5/10 | 15% | 0.75 | 3 条红色失败高度相关——repo-root 路径违反 §3.3(扣2)、allowed-tools 缺失(扣2)、Scope 不独立(扣1) |
| 人机感 | 9/10 | 10% | 0.90 | 审慎税务顾问语气，ASSUMPTION-REQUIRED + Guardrails + Advisor Questions + Cadence 人机边界设计出色。零 emoji、零喊叫。仅 "users" 人称微瑕，扣 1 分 |
| 可执行性 | 7/10 | 10% | 0.70 | 5 步全部可操作、references 齐全。但路径格式可能导致脚本不可执行 + 缺 allowed-tools，扣 3 分 |
| **加权总分** | | | **7.80/10** | |

### 12.2 评级

🟢 **B+** (78/100) — 高质量，少量可选优化即可达到 A 级

本 skill 的核心设计质量（工作流逻辑、reference 文件深度、人机边界设计、脚本代码质量）处于语料库前列。扣分高度集中在路径格式和 allowed-tools 这两个规范/格式层面的问题——修复它们不需要改变 skill 的任何内容逻辑，仅需 3 处路径替换 + 1 行工具声明。修复后评分预计可达 85-88 (A-)。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**1. 统一 scripts 路径为相对路径格式**
- 精确位置：SKILL.md L34 (`skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`)、L97-98（同路径）、L115-116（同路径 + tests/）
- 修复方向：将 3 处 repo-root 路径替换为相对路径。`skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py` → `scripts/build_tax_planning_sheet.py`，`skills/kanchi-dividend-us-tax-accounting/scripts/tests/test_build_tax_planning_sheet.py` → `scripts/tests/test_build_tax_planning_sheet.py`
- 不修复的后果：Bash 命令和 Resources 列表中的路径可能在实际部署环境中无效——agent 的工作目录不一定是 repo root。这会导致脚本不可执行，workflow 的自动化部分无法运行
- 涉及规范：SKILL-SPEC §3.3（相对路径规则）
- 工作量：3 处文本替换

**2. 添加 allowed-tools 字段**
- 精确位置：SKILL.md L3（description 行之后，`---` 闭合之前）
- 修复方向：`allowed-tools: Read, Write, Bash, Glob`
- 不修复的后果：agent 可能因工具限制被阻挡——特别是 Bash 工具，没有它则无法运行核心的分类脚本
- 工作量：1 行

### 🟡 重要缺陷（建议修复）

**3. 新增独立的 `## Limitations` 节**
- 精确位置：SKILL.md "Guardrails" 节之后（L42 之后），"Workflow" 节之前（L44 之前）
- 修复方向：添加一个独立的 Limitations 节，明确声明 skill 不做什么。建议内容：
  - 不替代持牌税务专业人士（CPA/税务律师）的专业判断——这是法律和伦理要求
  - 不涵盖国际税务或非美国税务管辖区——skill 的范围限于 US federal dividend tax
  - 不涵盖实际税务申报表（Form 1040, Schedule B, Schedule D 等）的准备和正式提交——skill 是规划工具，不是报税软件
  - MLP (Master Limited Partnership) 相关配置标记为 OUT-OF-SCOPE——因涉及 K-1 和 UBTI 复杂性，需要人类税务专业人员的单独评估
  - 所有持有期和分类判定基于 IRS 一般规则——特殊情况（如 wash sale、constructive sale、straddle rules）不在覆盖范围内
- 不修复的后果：agent 可能在范围外的场景（国际税务、实际申报表准备）中尝试执行 skill，产生不准确或不合规的输出
- 工作量：~12 行

**4. 修正 description 中 "users" → "the user"**
- 精确位置：SKILL.md L3（frontmatter description 值）
- 修复方向：`Use when users ask about` → `Use when the user asks about`
- 工作量：1 个单词

**5. Resources 节使用 Markdown 链接格式**
- 精确位置：SKILL.md L113-119（Resources 节全部 5 行）
- 修复方向：将裸文本 `` `path` `` 格式改为 Markdown 链接 `[描述](path)` 格式。例如 `` `references/qualified-dividend-checklist.md`: ... `` → `[qualified-dividend-checklist.md](references/qualified-dividend-checklist.md): ...`
- 工作量：5 行

### 🟢 优化建议（锦上添花）

**6. 处理或移除 agents/openai.yaml**
- 精确位置：`agents/openai.yaml`
- 修复方向：确认该文件是否有功能用途（如用于某种 agent 配置系统）。如无——移除以保持目录整洁，并删除 `agents/` 空目录。如有——在 SKILL.md Resources 节中添加引用和说明
- 工作量：1 行（添加资源引用）或删除 1 个文件

**7. annual-tax-memo-template.md 表格添加示例数据**
- 精确位置：references/annual-tax-memo-template.md L22-29（两个表格的 "..." 占位符）
- 修复方向：在每张表格的第一行添加一行示例数据，使模板更即时可用。例如 Distribution Classification Summary 表：`| JNJ | taxable | 1,200 | 1,050 | — | High |`
- 工作量：2 行

**8. 统一 checklist 和代码中的持有期天数表述**
- 精确位置：qualified-dividend-checklist.md L16 + build_tax_planning_sheet.py L26-29
- 修复方向：在 checklist 中将 "more than 60 days" 改为 "more than 60 days (at least 61 days)" 以消除与代码 `>= 61` 之间的歧义。同理处理 preferred stock 的 "more than 90 days"
- 工作量：2 处文字微调

**9. 增加 CF-03 critical failure**
- 精确位置：SCORING.yaml critical_failures 节（CF-02 之后）
- 修复方向：添加 "Agent makes account-location decisions when constraints conflict without explaining the tradeoff explicitly"（效应 cap_to_0）
- 对应内容：SKILL.md Step 4 的冲突处理规则 + SCORING.yaml PRI-02
- 工作量：3 行

### 修复工作量估计

- 预计修改行数：~28 行（路径替换 3 处 + Limitations 节 12 行 + 链接格式 5 行 + 措辞修正 3 处 + CF-03 3 行）
- 预计修改文件数：4 个（SKILL.md + qualified-dividend-checklist.md + annual-tax-memo-template.md + SCORING.yaml）
- 可选操作：删除 agents/openai.yaml（1 个文件）
- 注意：按项目约束，**本审查只报告问题，不对任何文件做修改**

---

## 变更记录
- 2026-08-05: 初始 stub（22 行）——标记了路径引用和 description 的 "users" 问题
- 2026-08-06: 全面深度审查，完全重写至 ≥500 行。验证所有 dossier 问题状态，发现 7 个增量问题

## 附录: 审查过程记录

**读取的文件列表**（11 个文件，全部全文读取）：
- SKILL.md (120 行)
- SCORING.yaml (170 行)
- check.py (91 行)
- agents/openai.yaml (4 行)
- references/input-schema.md (33 行)
- references/qualified-dividend-checklist.md (53 行)
- references/account-location-matrix.md (31 行)
- references/annual-tax-memo-template.md (42 行)
- scripts/build_tax_planning_sheet.py (186 行)
- scripts/tests/test_build_tax_planning_sheet.py (76 行)
- scripts/tests/conftest.py (7 行)

**读取行数统计**: ~813 行总计

**审查覆盖**: 目录中 100% 文件（11/11）全部全文读取并分析 ✅。每个文件的分析结论体现在 §1（目录清单）、§5（references 文件审查）、§4（脚本代码验证）中。

**Dossier 对照**: skill-dossier.md 评级 🟡（经本次审查验证，评级准确；但综合评分 78/100 表明实际质量高于 dossier 简评所暗示的水平）
