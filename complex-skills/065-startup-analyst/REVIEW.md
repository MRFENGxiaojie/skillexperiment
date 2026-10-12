# REVIEW: 065-startup-analyst

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: mindset — 早期创业公司（pre-seed 到 Series A）业务分析：市场容量（TAM/SAM/SOM）、财务建模、竞争分析、团队规划、创业指标
**Body 行数**: 322 行
**参考文件数**: references/0, resources/0（resources/implementation-playbook.md 被引用但不存在）
**总文件数**: 3（SKILL.md, SCORING.yaml, check.py）
**已有 REVIEW**: 旧版 4 行 stub，本次替换为 13 节全面深度审查

---

## 1. 目录全量清单

```
065-startup-analyst/
├── SKILL.md (322 行)
├── SCORING.yaml (179 行)
├── check.py (73 行)
└── REVIEW.md (本次覆写)
```

极简 3 文件结构，无子目录（无 references/、scripts/、assets/）。但 body 引用了 1 个不存在的文件 `resources/implementation-playbook.md`（L22）——这是与其他 skill（314-startup-financial-modeling、315、316）相同的共享模板残留模式。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 实际值: `startup-analyst`
- 匹配目录名 `065-startup-analyst`: ✅
- 全小写+连字符: ✅
- 长度: 15 字符（≤64）: ✅
- 判定: ✅ 通过

### 2.2 description

**原文**:

> "Expert startup business analysis including market sizing, competitive landscape, growth modeling, and strategic positioning. Use when the user needs to analyze a startup's market opportunity, evaluate TAM/SAM/SOM, assess competitive dynamics, model growth scenarios, or provide strategic recommendations for early-stage ventures."

**逐项检查**:

| 检查项 | 状态 | 说明 |
|--------|:----:|------|
| WHAT（做什么） | ✅ | "Expert startup business analysis including market sizing, competitive landscape, growth modeling, and strategic positioning"——具体，非空泛 |
| WHEN（何时用） | ✅ | "Use when the user needs to analyze a startup's market opportunity, evaluate TAM/SAM/SOM, assess competitive dynamics, model growth scenarios, or provide strategic recommendations" |
| KEYWORDS | ✅ | market sizing、TAM/SAM/SOM、competitive landscape、growth modeling、strategic positioning、early-stage |
| 第三人称 | ✅ | "Expert startup business analysis..."——主语是 the skill，无第一/第二人称 |
| 无祈使句开头 | ✅ | 以名词短语开头，非 "Use this skill to..." |
| 无跨 skill 路由 | ✅ | 无 "NOT for X, use Y instead" |
| 触发信号短语 | ✅ | "Use when the user needs to..."（§2.4 允许的信号之一） |
| 长度 | ✅ | 约 340 字符，远低于 1024 限制 |
| 无禁止内容 | ✅ | 无引号包裹问题（单行、无特殊字符） |

**判定**: description 完全合规，是本 skill 最强的合规点之一。WHAT/WHEN/KEYWORDS 三要素齐备，触发场景具体可操作。

### 2.3 model

- 实际值: `model: inherit`
- SKILL-SPEC §1.2 将 `model` 列为允许的可选字段，**键本身合规** ✅
- 但**值 `inherit` 非标准** ⚠️——规范给出的示例值是具体模型 ID（如 `claude-sonnet-5`）。"inherit" 的含义是"继承当前会话模型"，作为一个约定俗成的传值可被 harness 容忍，但不在规范示例中，属于灰色地带
- 旧 stub 与 dossier 将此记为"非标准 frontmatter key"，更精确的表述是：**键合规、值非标准**。建议删除该字段（省略时自然继承会话模型）或改为具体模型 ID
- 判定: ⚠️ 轻微问题

### 2.4 其他 frontmatter 字段

仅 `name`、`description`、`model` 三个字段。无 `allowed-tools`（可选字段，缺失不违规；该 skill 主要靠 WebSearch/Read/Write，可补但不强制）。无任何 §1.3 禁止字段 ✅。

### 2.5 Frontmatter 语法

- YAML 分隔符 `---` 配对正确（L1、L5）✅
- 无缩进错误 ✅
- description 单行、无特殊字符 ✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# 无 H1 标题（frontmatter 后直接进入 ## 节）        — 标题结构说明
## Use this skill when                               L7     — 2 条循环定义（5 行）
## Do not use this skill when                        L12    — 2 条循环定义（4 行）
## Instructions                                      L17    — 4 条泛化指令 + 1 死引用（6 行）
"You are an expert startup business analyst..."      L24    — 第二人称 persona 段（1 行）
## Purpose                                           L26    — 目的说明（3 行）
## Core Expertise                                    L30    — 5 个能力域（40 行）
### Market Sizing & Opportunity Analysis             L32
### Financial Modeling                               L40
### Competitive Analysis                             L49
### Team & Organization Planning                     L57
### Startup Metrics & KPIs                           L64
## Capabilities                                      L71    — 4 类能力（30 行）
### Research & Analysis                              L73
### Financial Planning                               L80
### Strategic Advisory                               L87
### Documentation                                    L94
## Behavioral Traits                                 L101   — 10 条特质（12 行）
## Knowledge Base                                    L114   — 6 个知识域（39 行）
### Market Sizing                                    L116
### Financial Modeling                               L123
### Competitive Strategy                             L130
### Team Planning                                    L136
### Startup Metrics                                  L141
### Fundraising                                      L148
## Response Approach                                 L154   — 10 步响应流程（12 行）
## Example Interactions                              L167   — 6 组示例问题（31 行）
## When to Use This Agent                            L199   — 触发清单（21 行）
## Integration with Commands                         L221   — 3 个虚构命令（7 行）⚠️
## Tools and Resources                               L229   — 工具与 skill 引用（14 行）⚠️
## Quality Standards                                 L244   — 应做/禁止清单（19 行）
## Output Format                                     L264   — 三类输出格式说明（30 行）
## Special Considerations                            L295   — 4 组场景考量（24 行）
### Stage Awareness                                  L297
### Industry Nuances                                 L303
### Founder Context                                  L308
### Investor Expectations                            L314
结尾段落                                              L320   — 使命声明（3 行）
```

共 29 个标题（含 `##` 与 `###`），总 322 行 body。结构上是**知识手册型**：能力域、知识库、质量标准占主导，流程性内容（Response Approach）仅 12 行。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

**Workflow/Process 节**: ⚠️ 部分存在但偏弱。

- 标题为 "## Response Approach"（L154-165），共 10 步: 理解上下文 → 激活相关技能 → 收集数据 → 应用框架 → 计算分析 → 验证发现 → 清晰呈现 → 给出建议 → 引用来源 → 承认局限
- 步骤链方向正确（context → data → framework → calc → validate → present → recommend），是一个合法的宏观流程
- 但**无任何条件分支、决策树、具体执行细节**——10 步均为行为准则，没有"遇到什么输入做什么"的映射。例如: 用户问市场容量 vs 问财务模型，流程完全相同，没有区分
- 每步没有输入/输出定义、没有验收标准
- 对比 314-startup-financial-modeling 的 Step-by-Step Process（134 行、每步带公式和示例），本 skill 的 workflow 是**骨架级**

**Output Format 节**: ✅ 存在。

- "## Output Format"（L264-293）分三类: Analysis（结构化小节、表格、公式、来源引用）、Calculations（公式/输入/逐步计算/结果单位/解释/基准对比）、Recommendations（具体步骤、理由、预期结果、资源需求、时间线、风险）
- 内容与 SCORING.yaml 的 OUT-01/02/03 对应良好 ✅
- 但属于**风格规范**而非**交付物模板**——没有定义最终报告的结构（如"报告应包含: 执行摘要 → 市场分析 → 财务模型 → 建议"），agent 仍需自行组装
- 判定: 存在且可用，但可操作性一般

**Scope/Limitations 节**: ❌ 实质缺失（最严重的结构性问题）。

- "## Do not use this skill when"（L12-15）仅 2 条:
  1. "The task is unrelated to startup analyst" — 循环定义，无信息量
  2. "You need a different domain or tool outside this scope" — 同样是循环定义
- "## Use this skill when"（L7-10）同样循环: "Working on startup analyst tasks or workflows" / "Needing guidance, best practices, or checklists for startup analyst"
- 没有任何真正的技术边界: 不覆盖哪些领域（SCORING.yaml 的 SCOPE-03 要求"不漂移到法律、税务、全套会计服务"，但 body 中从未声明此边界）、不适用于哪些场景（成熟公司? 上市公司?）、数据不可得时的行为、免责声明（非财务建议）
- 判定: ❌ 需新增真正的 "## Limitations" 节

### 3.3 内容委托分析

| 引用行 | 引用路径 | 存在 | 委托内容 |
|:------:|----------|:----:|----------|
| L22 | resources/implementation-playbook.md | ❌ | "If detailed examples are required" |

- 仅 1 处文件引用，且为死引用（死引用率 100%）
- 好在 body 是自包含的——322 行中没有任何关键内容委托给外部文件。删掉 L22 这一句即可
- L221-227 引用 3 个斜杠命令 `/market-opportunity`、`/financial-projections`、`/business-case`，L238-242 引用 5 个 skill 名——均属于 prose 引用，其中 3 个命令 + 2 个 skill 名在本 corpus 中不存在（详见 §5）

### 3.4 节编号/标题层级

- 标题层级: `#` → `##` → `###`，连续无跳级 ✅
- **frontmatter 后无 H1 标题**——首个顶层标题就是 `##`，且文件中完全没有 `#`。这与 SKILL-SPEC 无冲突（§3.1 不要求 H1），但与多数 corpus skill 的惯例不同（通常有 `# <name>` 或 `# <Title>` H1）。可接受但值得注意
- 无重复标题 ✅
- Response Approach 的步骤用 `1.` 编号，连续 1-10 ✅

### 3.5 Body 长度合规

- 322 行，低于 600 行硬限制 ✅
- SCORING.yaml 声明 `pattern: mindset`——mindset 模式目标约 50 行，实际 322 行是目标的 6 倍多。这提示两点: (1) pattern 元数据与实际内容形态不匹配（更像 process/参考手册）; (2) body 中约 100 行可压缩（L167-197 示例问题与 L199-219 触发清单高度重叠; L26-28 Purpose 与 description 重复; L154-165 与 L244-262 质量标准重叠）

### 3.6 自我定位一致性

- Body 中同时出现 **skill 框架**和 **agent 框架**:
  - Skill 框架: "## Use this skill when"（L7）、"## Instructions"（L17）
  - Agent 框架: "You are an expert startup business analyst..."（L24）、"## When to Use This Agent"（L199）、"This agent works seamlessly with plugin commands"（L222）、"Has access to: All plugin skills"（L230）
- 这是从 subagent 定义改造成 skill 时未清理干净的典型痕迹。Agent 框架的陈述（"all plugin skills"、"works seamlessly with commands"）在独立 skill 的语境下**无法兑现**（详见 §4.2）

---

## 4. 逻辑一致性深度审查

### 4.1 能力域与知识库的一致性

| 能力域（Core Expertise） | 知识库（Knowledge Base） | 匹配 |
|--------------------------|--------------------------|:----:|
| Market Sizing & Opportunity Analysis | Market Sizing | ✅ 一致（底向上/顶向下/价值理论、数据源、行业方法） |
| Financial Modeling | Financial Modeling | ✅ 一致（cohort、SaaS/marketplace/consumer/B2B 模板、unit economics、burn rate、fundraising 场景） |
| Competitive Analysis | Competitive Strategy | ✅ 一致（Porter、Blue Ocean、定位图） |
| Team & Organization Planning | Team Planning | ✅ 一致（按阶段雇佣、薪酬、股权、组织设计） |
| Startup Metrics & KPIs | Startup Metrics | ✅ 一致（按商业模式和阶段、投资者期望、基准） |

五大能力域与知识库一一对应，无内部矛盾 ✅。

**细微不一致**: Core Expertise 的 Market Sizing 列有 "Industry-specific templates (SaaS, marketplace, consumer, B2B, **fintech**)"（L37），但 Knowledge Base 和 Special Considerations 的 Industry Nuances 均只列 SaaS/marketplace/consumer/B2B，无 fintech。fintech 只在 L37 出现一次——孤立提及。

### 4.2 虚构依赖扫描（实质性发现）

**依赖 1 — 三个斜杠命令（L221-227）**:
- "Can invoke `/market-opportunity` for comprehensive market sizing"、"Can invoke `/financial-projections`"、"Can invoke `/business-case`"
- 在 corpus 全量搜索: 没有任何 skill 或 plugin 定义这三个命令。仅 057-go-to-market-planner 和 266-customer-persona-builder 提到过类似名称的 "market-opportunity-analyzer"（不是 `/market-opportunity` 命令）
- **结论**: 这是从原始 subagent/plugin 定义复制过来的虚构命令引用。agent 若遵循该指令调用这些命令，将直接失败
- 触发相关标准: SKILL-SPEC §3.3（不得引用不存在的资源）——虽无明文禁虚拟命令，但这属于"不可兑现的执行指令"

**依赖 2 — "Leverages skills" 五个 skill 名（L238-242）**:
- `market-sizing-analysis` → 047-market-sizing-analysis ✅ 存在
- `startup-financial-modeling` → 314-startup-financial-modeling ✅ 存在
- `competitive-landscape` → 256-competitive-landscape ✅ 存在
- `team-composition-analysis` → ❌ **不存在**（corpus 中无此目录名）
- `startup-metrics-framework` → ❌ **不存在**
- **结论**: 5 个中 3 个存在、2 个虚构。prose 按名引用存在的 skill 是合规的（§3.3"use its name in prose"），但引用不存在的 skill 会造成 agent 幻想依赖

**依赖 3 — "All plugin skills"（L230）**:
- "Has access to: All plugin skills for detailed frameworks"——本 skill 不是任何 plugin 的一部分，corpus 中也没有该 plugin。此声明无法兑现

**依赖 4 — 死文件引用（L22）**:
- `resources/implementation-playbook.md` 不存在。此句与 314/315/316 相同，是共享模板残留

### 4.3 行为准则内部一致性

- "Behavioral Traits"（L101-112）的 10 条（startup-focused、data-driven、conservative、pragmatic、transparent、founder-friendly、action-oriented、investor-aware、rigorous、honest）与 "Quality Standards"（L244-262）的应做/禁止清单完全一致——trait "Conservative" ↔ "Never use overly optimistic assumptions"; trait "Honest" ↔ "Acknowledge limitations and risks" ✅
- "Response Approach" 10 步与 "Quality Standards" 无矛盾 ✅
- "Special Considerations" 的 Stage Awareness/Industry Nuances/Founder Context/Investor Expectations 四组与 SCORING.yaml 的 SCOPE-02、PROC-06/07、OUT-04/05 一一对应 ✅
- 无数字矛盾（body 中无自算公式; L192 "CAC of $2,500 and LTV of $8,000" 仅为示例问题，LTV/CAC=3.2 合理，不与任何基准冲突）✅

### 4.4 条件完整性

- 无任何条件分支结构（无 if/else、无决策表、无模式分派）——本 skill 是单一模式，所有输入走同一流程
- 隐含的例外情况（无数据时怎么办、用户拒绝提供信息时怎么办）均未处理。Example Interactions 只给了问题示例，没有回答路径的示例
- 与 mindset pattern 定位相符（创意/判断类任务），但即便如此，至少应区分"有实时数据需求"与"纯框架推理"两种路径

### 4.5 时效性问题

- L138: "Compensation benchmarks (US-focused, 2024)"——2024 年的薪酬/股权基准数据到 2026 年已明显过时（尤其是技术人才市场）。Knowledge Base 声称包含基准，但正文没有给出任何具体数值，也没有更新机制说明
- 无其他时效性问题（框架类内容 Porter/Blue Ocean/TAM 方法论不受时效影响）✅

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用 | SKILL.md 行号 | 类型 | 是否存在 | 判定 |
|------|:------------:|------|:--------:|:----:|
| resources/implementation-playbook.md | L22 | 文件引用 | ❌ | 死引用，需删除 |
| /market-opportunity | L224 | 命令引用 | ❌ | 虚构命令 |
| /financial-projections | L225 | 命令引用 | ❌ | 虚构命令 |
| /business-case | L226 | 命令引用 | ❌ | 虚构命令 |
| market-sizing-analysis | L239 | skill 名（prose） | ✅ 047 | 合规引用 |
| startup-financial-modeling | L240 | skill 名（prose） | ✅ 314 | 合规引用 |
| competitive-landscape | L240 | skill 名（prose） | ✅ 256 | 合规引用 |
| team-composition-analysis | L241 | skill 名（prose） | ❌ | 虚构 skill |
| startup-metrics-framework | L241 | skill 名（prose） | ❌ | 虚构 skill |

### 5.2 不可见资源审计

无隐藏文件、无嵌套目录、无 .gitkeep ✅。目录干净。

### 5.3 跨 Skill 引用检查

- 无 `../` 跨 skill 文件路径 ✅（SKILL-SPEC §3.3 合规）
- 3 个 prose skill 名引用存在且合规 ✅
- 2 个 prose skill 名 + 3 个命令不存在 ⚠️（见 §4.2）

### 5.4 嵌套重复/死文件检查

无嵌套重复 ✅。

---

## 6. 语法与格式质量

### 6.1 拼写错误

全文英文拼写无错误 ✅。领域术语（TAM/SAM/SOM、Porter's Five Forces、Blue Ocean、Rule of 40、magic number、burn multiple、NDR、ACV）全部拼写正确。

### 6.2 语法错误

- 语法整体规范流畅 ✅
- L24 "You are an expert startup business analyst specializing in helping early-stage companies (pre-seed through Series A) with market sizing, financial modeling, competitive strategy, and business planning."——语法正确，但为第二人称 persona 句式（见 §8.5）
- "Do not use this skill when: The task is unrelated to startup analyst"（L13）——"unrelated to startup analyst" 缺 "the" 的物主性（应为 "unrelated to startup analysis" 或 "the startup analyst domain"），但可读无碍

### 6.3 中英/葡英混杂

纯英文 ✅。无任何中英或葡英混杂。

### 6.4 Markdown 格式破损

- 代码围栏: 全文无代码围栏（无公式代码块——与 314 相比，本 skill 不给公式只给名称，如 "MRR, NDR, CAC payback" 仅是文字提及）。无围栏即无围栏破损 ✅
- 表格: 全文无表格（与 314/322 形成对比——它们用表格呈现结构化数据）。本 skill 全部用 bullet list，对"行业基准对比"类内容（L303-307 Industry Nuances）表格本可以更高效，但非缺陷
- 列表: 全部 bullet 格式正确；Response Approach 用 `1.`-`10.` 编号连续 ✅
- 加粗 `**text**` 配对检查通过 ✅

### 6.5 占位符未填充

- 无 TODO/FIXME/TBD/`{{PLACEHOLDER}}` ✅
- 无模板占位符残留（除 §4.2 的虚构引用外）✅

### 6.6 截断内容

文件以完整使命陈述结尾（L320-322: "Your goal is to provide startup founders with the analytical rigor of a top-tier strategy consultant combined with the practical, startup-specific knowledge of an experienced operator."）——完整，无截断 ✅

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` 的 12 条规则:

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | `startup-analyst` 匹配 `065-startup-analyst` |
| 2 | description 第三人称 | ✅ | 名词短语开头，无第一/第二人称 |
| 3 | description 含触发短语 | ✅ | "Use when the user needs to..." |
| 4 | description ≤1024 字符 | ✅ | 约 340 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | 仅 name/description/model（model 键在 §1.2 允许列表） |
| 6 | body ≤600 行 | ✅ | 322 行 |
| 7 | Workflow/Process 节存在 | ⚠️ | Response Approach 10 步存在但为泛化准则，无分支/无输入输出定义 |
| 8 | Output Format 节存在 | ✅ | "## Output Format" 三类风格规范 |
| 9 | Scope/Limitations 节存在 | ❌ | "Do not use" 为循环定义，无实际边界信息 |
| 10 | 无跨 skill 文件路径引用 | ✅ | 无 `../` 路径 |
| 11 | allowed-tools 格式正确 | ⚠️ | 字段缺失（可选，不违规，但建议补充） |
| 12 | 路径仅指向本 skill 目录内 | ⚠️ | 唯一路径 resources/implementation-playbook.md 在目录内但文件不存在（死引用） |

**合规统计: 8/12 ✅, 3/12 ⚠️, 1/12 ❌**

### 违规详情

**违规 1 — 缺少真正的 Scope/Limitations 节（规则 9）**: 这是唯一硬性违规。SKILL-SPEC §3.1 明确要求 body 回答"该 skill 不做什么、何时不该用"。当前两个循环定义条目对 agent 决策零贡献。需重写为实际边界（至少含: 不提供法律/税务/会计服务、适用于 pre-seed 至 Series A 而非成熟公司、无实时数据时基于框架给出假设并标注、不构成财务建议）。

**部分合规项说明**: 规则 7 的 workflow 存在但质量偏弱（见 §3.2）；规则 11/12 为可选或轻微问题。

---

## 8. 人机感评估

### 8.1 Emoji 审计

- 全文中仅 Quality Standards 节（L247-254）使用 ✅ 图标、L257-262 使用 ❌ 图标——均为功能性状态标记（应做/禁止清单），非装饰性使用 ✅
- 其余位置零 emoji ✅
- 判定: 使用恰当，不构成问题

### 8.2 全大写/喊叫式语言

无全大写喊叫（无 STOP!、MANDATORY、CRITICAL）✅。加粗 `**Never:**` / `**All analyses must:**`（L246-256）为功能性强调，语气克制 ✅。

### 8.3 Persona 语气分析

整体语气: **专业顾问风格**——结构化、务实、自信。代表性语句:

- "Provides practical, actionable analysis for entrepreneurs, founders, and early-stage investors."（L27-28）——清晰的价值主张
- "Grounds recommendations in data and benchmarks"（L104）——基于经验的务实承诺
- "Balances rigor with speed and resource constraints"（L106）——了解创业公司现实的实用主义
- "Pragmatic: Balances rigor with speed" 与 "Rigorous: Validates assumptions"（L106/L111）——两条特质在表面上张力，但前者是资源约束下的平衡、后者是方法论要求，语境区分清楚，不构成矛盾

语气适合领域场景，无过度营销、无对话填充 ✅。结尾使命陈述（L320-322）适度有感染力但不浮夸。

### 8.4 人机边界分析

该 skill 的人机边界意识**中等偏弱**:

- ✅ 有: "Acknowledge limitations and risks"（L165）、"Always include data sources and publication dates"（L164）、"Transparent: Documents assumptions and limitations clearly"（L105）——都要求向用户透明
- ⚠️ 缺: 没有显式的"人类负责最终决策"声明；没有"数据不可得时的降级路径"；没有"该技能的分析不构成投资/财务建议"的免责边界（SCORING.yaml 的 SCOPE-03 隐含此边界，但 body 未声明）
- ⚠️ 缺: 没有强制验证门——Quality Standards 说"Validate with multiple methods when possible"（L250），但"when possible"是软约束，无人类确认步骤

### 8.5 人称分析

- **第二人称 persona 段**: L24 "You are an expert startup business analyst..."——这是从 subagent 定义继承的残留。对 skill 而言，"You are..." 是直接对模型说话，在操作指令语境下可接受（corpus 中 053/079 等也有），但结合 L199 "When to Use This Agent"、L222 "This agent works..."、L230 "Has access to"（agent 拥有资源的口吻），形成**"skill 即 agent"的定位混淆**——agent 框架的承诺（拥有 plugin、能调命令）在 skill 语境下无法兑现（§4.2）
- 指令层其余为祈使/中性第三人称，恰当 ✅
- 判定: 人称本身无严重违规，但 agent 框架残留影响可信度

### 8.6 表格使用评估

全文零表格。对该 skill 的内容类型（基准值、分阶段差异、分商业模式指标），表格本可提升可读性（例如 L303-307 的 Industry Nuances 四行对比、L315-318 的 Investor Expectations 四类投资者对比，用表格会远优于 bullet）。非缺陷，属优化建议。

---

## 9. 可执行性评估

### 9.1 独立可执行性

**评分: 7/10**

假设 agent 只拿到 SKILL.md:
- ✅ 可以回答领域问题——body 提供了完整的领域框架（能力域 + 知识库 + 质量标准）
- ✅ 输出风格有明确规范（Output Format 三类）
- ✅ 无外部文件依赖——body 自包含（唯一的 L22 死引用删掉即可）
- ⚠️ 但**不知道"现在具体做什么"**——没有步骤化的执行路径。Response Approach 10 步是行为准则，不是工作流。一个 agent 拿到 "Calculate the TAM for X" 的问题，从 L32-38 的市场容量能力域开始是合理的，但 skill 没有明确说"第 1 步做什么、第 2 步做什么"
- ⚠️ 若 agent 循着 L224-226 尝试调用 `/market-opportunity` 等命令，将直接失败
- ⚠️ 若 agent 尝试读取 L22 的文件或寻找 team-composition-analysis skill，将浪费时间

### 9.2 步骤可操作性

| 组件 | 可操作性 | 问题 |
|------|:--------:|------|
| Response Approach 10 步 | 🟡 | 泛化准则，无输入→动作→输出映射 |
| Core Expertise 5 能力域 | 🟢 | 每个域列出具体方法（TAM/SAM/SOM、cohort、Porter） |
| Knowledge Base 6 知识域 | 🟢 | 内容组织清晰 |
| Output Format 3 类 | 🟡 | 风格规范而非交付物模板 |
| Quality Standards | 🟢 | 应做/禁止清单可执行 |
| Special Considerations | 🟢 | 4 组场景指导具体（stage/model/founder/investor） |

**总评**: 领域知识可操作性强，流程机制弱。作为 mindset 型 skill，这一定位下"给出框架让 agent 自行判断"是可以接受的，但若按 SCORING.yaml 的 20 条标准评测（PROC-02/03/05 要求框架应用、工作展示、三角验证），agent 的响应质量将高度依赖模型自身能力而非 skill 引导。

### 9.3 工具依赖合理性

- 需要的工具: WebSearch（实时数据）、Read/Write（文档输出）
- allowed-tools 声明: 缺失 ⚠️（可选字段，但该 skill 明确依赖 web search，建议声明）
- 外部依赖: 3 个虚构命令（§4.2）——不合理，应删除
- 回退方案: 无说明（数据不可得时的行为未定义）

---

## 10. SCORING.yaml 交叉参考

### 10.1 总体结构

- 20 个 criteria（total_items: 20）: SCOPE 3 + PROC 7 + OUT 5 + NEG 2 + QA 3 = 20 ✅ 计数自洽
- 类别分布合理: 过程类最多（7），符合"分析型 mindset"定位
- judge 类型: 18 个 llm + 2 个 script（PROC-01、QA-02）✅
- pattern: `mindset`——与 322 行 body 的实际形态不匹配（见 §3.5）

### 10.2 测评点覆盖映射

| 类别 | 与 SKILL.md 一致性 |
|------|------|
| SCOPE-01（识别早期创业分析任务） | ✅ 对应 description + Core Expertise |
| SCOPE-02（按阶段匹配深度） | ✅ 对应 Special Considerations > Stage Awareness（L297-301） |
| SCOPE-03（不漂移到法律/税务/会计） | ⚠️ **边界在 body 中从未声明**——skill 没有排除 legal/tax/accounting 的表述。评测要求 agent 遵守的边界，skill 自己没说。应写入新增的 Limitations 节 |
| PROC-01（web search + 引用） | ✅ 对应 Capabilities > Research & Analysis + Response Approach 第 9 步 |
| PROC-02（应用框架） | ✅ 对应 Core Expertise 的方法论（TAM/SAM/SOM、Porter、unit economics） |
| PROC-03（计算展示过程） | ✅ 对应 Output Format > Calculations |
| PROC-04（假设保守现实） | ✅ 对应 Behavioral Trait "Conservative" + Quality Standards |
| PROC-05（多方法验证/三角化） | ✅ 对应 Quality Standards "Validate with multiple methods when possible" |
| PROC-06（基准参照） | ✅ 对应 Knowledge Base > Startup Metrics + Special Considerations > Industry Nuances |
| PROC-07（商业模式细分） | ✅ 对应 Industry Nuances（SaaS/marketplace/consumer/B2B） |
| OUT-01（结构化输出） | ✅ 对应 Output Format > Analysis |
| OUT-02（建议具体可执行） | ✅ 对应 Output Format > Recommendations |
| OUT-03（承认局限风险） | ✅ 对应 Response Approach 第 10 步 + Trait "Honest" |
| OUT-04（创始人经验适配） | ✅ 对应 Founder Context（L308-312） |
| OUT-05（投资者类型考量） | ✅ 对应 Investor Expectations（L314-318） |
| NEG-01（无支撑主张/跳过验证） | ✅ 对应 Quality Standards Never 清单 |
| NEG-02（非泛化建议、引用来源） | ✅ 对应 Quality Standards + Trait "Data-driven" |
| QA-01（质量标准综合） | ✅ 对应 Quality Standards 全文 |
| QA-02（数值内部一致） | ⚠️ 见 10.3 重大发现 |
| QA-03（响应流程遵循） | ✅ 对应 Response Approach |

映射质量: **18/20 精准对应**，2 项存在问题（SCOPE-03 边界未在 body 声明; QA-02 检查机制与描述不符）。

### 10.3 QA-02 的重大问题（描述与检查不符）

- criterion 描述: "Numerical outputs are internally consistent (sums, ratios, projections recompute correctly)"——要求**内部一致性验证**（重算求和、比率、预测）
- 实际 script check: `output_contains("(?i)(CAC|LTV|payback|burn multiple|magic number|Rule of 40|take rate)")`——只检查**词汇出现**，完全不验证任何数字是否正确
- 结论: 检查与描述**实质性脱节**。一个包含 CAC/LTV 字眼但数字错误百出的回答会通过；一个数字完全正确但没提这些词的回答会失败
- 附加问题: 该词表高度商业模式化——SaaS 回答自然包含 CAC/LTV，但市场容量问题（如 "TAM for construction SaaS"）或团队规划问题（"how much equity for first engineer"）的输出**可以完全合理地不包含任何这些词**，导致误杀。SCOPE-01 明确把 market sizing、competitive strategy、team planning 都纳入范围，QA-02 却只奖赏财务词汇——评测设计与 skill 范围不完全对齐

### 10.4 Critical Failures 分析

| CF | 描述 | 效果 | 合理性 |
|----|------|:----:|:------:|
| CF-01 | 无来源的虚构市场数据/基准/财务预测 | cap_to_0 | ✅ 合理——对应 Quality Standards "Never make unsupported claims" + "Always cite sources"。数据造假是该领域最严重失败模式 |
| CF-02 | 无假设文档、无验证的乐观财务建议 | cap_to_0 | ✅ 合理——对应 Trait "Conservative" + PROC-04/05。两个 CF 都是量化该 skill 最核心的红线 |

评价: CF 设计精当，都对准 mindset 型分析 skill 的致命失败模式。

### 10.5 check.py 审查

- 73 行，结构清晰: 导入 _shared/checker 的 `tool_log_contains` 和 `output_contains` ✅
- 实现了 SCORING.yaml 声明的 2 个 script check（PROC-01、QA-02），与 SCORING.yaml 一致 ✅
- `main()` 正确处理 agent_output 为文件路径或裸文本两种情况 ✅
- 错误处理: 参数个数校验（sys.exit 1）✅
- 无问题 ✅

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md（位于 `~/.claude/projects/C--Users-f50058303/memory/skill-dossier.md`）对 065 的档案记录:

> **逻辑**: 市场/财务/竞争/团队/指标五大能力域自洽，"Do not use this skill when: The task is unrelated" 属同义反复；frontmatter 中 `model: inherit` 为非标准字段。
> **语法**: 规范流畅。
> **人机感**: 专业顾问口吻，无 emoji、无填充语。
> **合规**: Description 第三人称，有 When to Use/Instructions/Output 结构，正文 322 行 ≤600。
> **总评**: 🟢 结构完整，同义反复与 `model: inherit` 字段属小瑕疵。

Dossier 评级: 🟢（结构完整，两处小瑕疵）。

### 本次审查的增量发现（dossier 未记录）

1. **L22 死文件引用** `resources/implementation-playbook.md`——与 314/315/316 同源的共享模板残留（dossier 未提及）
2. **3 个虚构斜杠命令**（/market-opportunity、/financial-projections、/business-case）——corpus 中不存在（dossier 未提及）
3. **2 个虚构 skill 名**（team-composition-analysis、startup-metrics-framework）——5 个 "Leverages skills" 中 3 个存在、2 个不存在（dossier 未提及）
4. **agent/skill 自我定位混乱**——"You are an expert..."、"When to Use This Agent"、"All plugin skills" 为 subagent 定义残留（dossier 未提及）
5. **Scope/Limitations 节实质缺失**——dossier 只记为"同义反复"小瑕疵，但按 SKILL-SPEC §3.1 这是唯一硬性违规（规则 9）
6. **SCORING.yaml QA-02 检查与描述脱节**——"recompute correctly" 实际只查关键词（dossier 未涉及 SCORING.yaml）
7. **SCOPE-03 边界未在 body 声明**——评测要求与 skill 内容错位

结论: dossier 的 🟢 评级方向正确（无 🔴/🟠 级问题），但问题清单应扩充——发现的问题多为"引用完整性"和"定位一致性"类，属 🟡 级，修复成本低。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | description 完全合规；`model: inherit` 值非标准 |
| Body 结构完整 | 6/10 | 10% | 0.60 | Output ✅、Workflow 骨架级 ⚠️、Scope 缺失 ❌ |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 能力域/知识库/行为准则高度自洽；虚构依赖 + agent 定位混乱 |
| 参考完整性 | 5/10 | 15% | 0.75 | 1 死文件 + 3 虚构命令 + 2 虚构 skill 名；好在无关键内容委托 |
| 语法格式 | 9/10 | 10% | 0.90 | 英文规范，无错字无格式破损 |
| 规范合规 | 8/10 | 15% | 1.20 | 8/12 完全合规；Scope 硬性违规 1 项 |
| 人机感 | 8/10 | 10% | 0.80 | 专业顾问语气、功能性 emoji；人机边界声明偏弱、agent 框架残留 |
| 可执行性 | 7/10 | 10% | 0.70 | 领域框架可操作；流程机制弱、虚构引用可能误导 agent |
| **加权总分** | | | **7.15/10** | |

### 12.2 评级

🟢 **B** (72/100) — 可用，无严重问题。description 完全合规、领域内容专业自洽、SCORING.yaml 设计良好是本 skill 的三大优势。扣分集中在引用完整性（6 处无效引用）与结构（Scope 缺失、Workflow 骨架级）。

修复优先级建议: 删除/改写 6 处无效引用 + 重写 Do-not-use 为真实 Limitations + 清理 agent 框架残留，预计可达 **B+/A-（80+）**。若再补一个输入→方法→输出的决策表强化 Workflow，可达 A 级。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: 6 处无效引用（1 死文件 + 3 虚构命令 + 2 虚构 skill 名）**

**F-1a: 死文件引用**
- 位置: SKILL.md L22 `resources/implementation-playbook.md`
- 修复: 直接删除 L22 "If detailed examples are required, open `resources/implementation-playbook.md`." 整句。body 已自包含（322 行含全部领域内容），无需替代物。若确实想给示例，在 body 内新增一个具体示例（如一个 TAM 计算的逐步演示）比引用不存在文件更好
- 不修复的后果: agent 尝试读取不存在文件 → 浪费时间或报错，且与 314/315/316 的同类残留形成系统性模板痕迹

**F-1b: 三个虚构斜杠命令**
- 位置: SKILL.md L221-227 "## Integration with Commands"
- 当前内容:
  ```
  This agent works seamlessly with plugin commands:
  - Can invoke `/market-opportunity` for comprehensive market sizing
  - Can invoke `/financial-projections` for detailed financial models
  - Can invoke `/business-case` for complete business case documents
  - Provides quick analysis when commands not needed
  ```
- 问题: 这三个命令在 corpus 中不存在（全量检索无定义）。agent 若遵循指令调用，将直接失败
- 修复方案（推荐 A）: **删除整个 "## Integration with Commands" 节**。该节是 subagent/plugin 定义的残留，对独立 skill 无价值
- 修复方案（备选 B）: 若想保留"命令可加速"的信息，改为 prose 说明（不带斜杠命令语法）:
  ```
  ## Faster Paths
  
  For comprehensive market sizing, financial projections, or business case documents,
  the relevant analysis can be produced directly by this skill — no separate commands
  are required.
  ```
- 不修复的后果: agent 尝试调用不存在的命令，评测中工具调用失败记录会污染 tool log

**F-1c: 两个虚构 skill 名**
- 位置: SKILL.md L238-242 "## Tools and Resources > Leverages skills"
- 当前内容:
  ```
  - market-sizing-analysis
  - startup-financial-modeling
  - competitive-landscape
  - team-composition-analysis
  - startup-metrics-framework
  ```
- 问题: `team-composition-analysis` 与 `startup-metrics-framework` 在 corpus 中不存在
- 修复: 删除两个虚构条目，仅保留存在的 3 个（047-market-sizing-analysis、314-startup-financial-modeling、256-competitive-landscape）。按 SKILL-SPEC §3.3，prose 引用应写明 skill 名即可（当前格式已合规）。可加一句 "see also:" 前缀使意图更明确:
  ```
  **Leverages skills:**
  - market-sizing-analysis (see also: 047-market-sizing-analysis)
  - startup-financial-modeling (see also: 314-startup-financial-modeling)
  - competitive-landscape (see also: 256-competitive-landscape)
  ```
- 不修复的后果: agent 去寻找不存在的 skill，产生幻想依赖

**F-2: Scope/Limitations 节实质缺失（违反 SKILL-SPEC §3.1 规则 9）**

- 位置: SKILL.md L12-15 "## Do not use this skill when"（2 条循环定义）
- 修复: 将循环定义替换为真实边界，至少覆盖以下内容:

```markdown
## Limitations

This skill does NOT:

- **Provide legal, tax, or accounting services.** Analyses cover business strategy,
  market sizing, and financial modeling frameworks — not legal counsel, tax planning,
  or full-scope accounting. Escalate those to licensed professionals.

- **Serve mature companies.** Optimized for early-stage ventures (pre-seed through
  Series A). Public-company financial reporting, GAAP compliance, and enterprise
  restructuring are out of scope.

- **Fabricate market data.** When current market data cannot be obtained, state the
  assumption explicitly and mark the estimate as directional rather than sourced.
  All cited data must carry a source and publication date.

- **Constitute investment advice.** Frameworks and benchmarks inform decisions but
  do not replace the user's own judgment or a qualified advisor's review.

- **Operate without input.** Clarify stage, business model, and the specific question
  before analyzing; do not assume context.
```

- 顺带将 "## Use this skill when"（L7-10）的 2 条循环定义替换为真实触发场景（可直接复用 description 的触发列表 + Special Considerations 的场景）:

```markdown
## Use this skill when

- The user asks to size a market opportunity (TAM/SAM/SOM) for an early-stage startup
- The user asks for financial projections, unit economics, or fundraising modeling
- The user asks to assess the competitive landscape or positioning
- The user asks about team planning, compensation, or hiring by stage
- The user asks which metrics to track or whether their metrics are on target
```

- 不修复的后果: 规则 9 硬性违规持续; agent 无法判断边界（SCOPE-03 评测项要求不漂移到法律/税务/会计，但 skill 从未告知 agent 这条边界）

**F-3: agent/skill 自我定位混乱**

- 位置: L24（"You are an expert startup business analyst..."）、L199（"## When to Use This Agent"）、L222（"This agent works seamlessly"）、L230（"Has access to: All plugin skills"）
- 问题: 同一文件混用 skill 框架（Use this skill when / Instructions）与 agent 框架（You are / This agent / Has access to）。agent 框架的承诺（拥有 plugin、调用命令、访问所有 plugin skills）在独立 skill 语境下无法兑现
- 修复:
  1. L199 "## When to Use This Agent" → "## When to Use This Skill"（标题与 L7 的 Use-when 节合并或去重）
  2. L222 "This agent works seamlessly with plugin commands" → 随 F-1b 删除
  3. L230 "Has access to: All plugin skills for detailed frameworks" → 删除或改为 "Provides framework-level guidance across the startup analysis domains listed in Core Expertise"
  4. L24 "You are an expert startup business analyst..." → 可保留（corpus 惯例允许 persona 开场），但建议改写为第三人称功能声明: "This skill provides expert startup business analysis for early-stage companies (pre-seed through Series A): market sizing, financial modeling, competitive strategy, and business planning." 若保留 persona，至少保证其后的 "When to Use This Agent" 改为 skill 框架
- 不修复的后果: 定位混乱降低 agent 对 skill 可信度的判断; 无法兑现的承诺（plugin、commands）可能在评测中被触发

### 🟡 重要缺陷（建议修复）

**I-1: 强化 Workflow 节（Response Approach 骨架化）**

- 位置: L154-165
- 问题: 10 步响应流程无分支、无输入→动作→输出映射。agent 从哪一步开始、各步产出什么均未定义
- 修复: 在 Response Approach 后新增一个"输入类型 → 分析路径"的决策表:

```markdown
## Analysis Paths

| User request type | Primary approach | Key outputs |
|-------------------|------------------|-------------|
| Market sizing (TAM/SAM/SOM) | Bottom-up + top-down, triangulate | Market size ranges, segments, growth trajectory, sources |
| Financial modeling | Cohort-based revenue, unit economics | 3-5 year model, scenarios, runway, key ratios |
| Competitive analysis | Porter's Five Forces, positioning map | Landscape map, differentiation, moat assessment |
| Team planning | Stage-based hiring plan, comp benchmarks | Hiring sequence, org design, equity guidance |
| Metrics & KPIs | Model-specific metrics, benchmarks | Metric scorecard vs benchmarks, priorities |
| Fundraising prep | Round sizing, dilution modeling | Raise scenario, use of funds, milestones |
| Strategy | GTM/pricing/segmentation frameworks | Recommendations with sequencing and risks |
```

- 预计新增 ~20 行。这能把"知识手册"升级为"可执行流程"，直接提升 PROC-02/03/05 的评测表现

**I-2: 删除冗余内容（约 60 行）**

- 位置与理由:
  1. "## Purpose"（L26-28）——与 description 几乎逐字重复（"practical, actionable analysis for entrepreneurs, founders, and early-stage investors" vs description 的 "strategic recommendations for early-stage ventures"）。删除或压缩为 1 行
  2. "## Instructions"（L17-21）——4 条泛化指令（"Clarify goals, constraints, and required inputs" 等）在 Response Approach 中已有对应步骤。保留 L22 删除后的剩余 3 条意义不大，可删除；若保留，合并入 Use-when 之后作前置声明
  3. "## Example Interactions"（L167-197）与 "## When to Use This Agent"（L199-219）——前者列出问题示例，后者列出触发场景，两者重叠度高（market sizing 问题 ↔ market sizing 触发）。保留 Example Interactions（对 agent 有示范价值），删除 When to Use 节的重复条目，或反之
- 预计净减少 ~40-60 行，使 body 从 322 行降至 ~270 行，更接近可维护状态

**I-3: `model: inherit` 值非标准**

- 位置: L4
- 问题: 键 `model` 在 SKILL-SPEC §1.2 允许列表内，但值 `inherit` 不在规范示例（具体模型 ID）中
- 修复: 二选一——(a) 删除该字段（省略时继承会话模型，语义与 "inherit" 相同）; (b) 改为具体模型 ID（如 `claude-sonnet-5`）。推荐 (a)
- 不修复的后果: 无功能影响，但评测的 frontmatter 校验可能报非标准值

**I-4: 基准数据时效与更新机制**

- 位置: L138 "Compensation benchmarks (US-focused, 2024)"
- 问题: 2024 年基准到 2026 年已过时；且 Knowledge Base 声称含基准，但正文无任何具体数值、无更新说明
- 修复: 改为 "(US-focused; verify current figures at analysis time)"，并在 Response Approach 增加"引用基准时注明数据年份"的要求（第 9 步"Cite sources"已隐含，可明示）

**I-5: fintech 孤立提及**

- 位置: L37 "Industry-specific templates (SaaS, marketplace, consumer, B2B, fintech)"
- 问题: fintech 全文仅此一处; Knowledge Base 与 Industry Nuances 均无 fintech 分支
- 修复: 二选一——(a) 从 L37 删除 fintech，保持四模式一致; (b) 在 Industry Nuances 补充 fintech 一行（"Fintech: emphasize compliance costs, charge-off rates, funding cycle"）。推荐 (b)——fintech 是创业分析真实场景，补一行成本极低

### 🟢 优化建议（锦上添花）

**O-1: SCORING.yaml QA-02 检查与描述对齐**

- 位置: SCORING.yaml QA-02
- 问题: 描述承诺 "recompute correctly"（内部一致性验证），script 只查关键词
- 修复: 二选一——(a) 修改描述为 "Output references finance metrics relevant to the business model (CAC, LTV, payback, burn multiple, magic number, Rule of 40, take rate)"，让描述与检查一致; (b) 增强 script: 检测 `\d+\.?\d*%` 与 `\$[\d,]+` 数值密度 + 关键比率重算（成本高，不推荐 script 级重算，推荐 (a) 诚实化描述）

**O-2: QA-02 词表的任务类型误杀风险**

- 位置: SCORING.yaml QA-02 pattern `(?i)(CAC|LTV|payback|burn multiple|magic number|Rule of 40|take rate)`
- 问题: 纯市场容量或团队规划问题的合理回答可以不出现任何这些词，但 QA-02 判失败
- 修复: 扩宽词表覆盖其他任务类型（加 `TAM|SAM|SOM|NDR|ACV|GMV|take rate|win rate|equity|burn`），或将 QA-02 改为 llm judge（人工判断数值一致性），保留 script 作为辅助信号

**O-3: SCOPE-03 边界写进 body**

- 位置: SCORING.yaml SCOPE-03 要求"不漂移到法律、税务、全套会计服务"，但 body 未声明
- 修复: 随 F-2 新增的 Limitations 节第 1 条即覆盖此边界（见 F-2 修复文本）。修复 F-2 后 SCOPE-03 自动对齐

**O-4: check.py 增加一个 script check**

- 位置: check.py
- 建议: 当前仅 2 个 script check。可增加 `result["PROC-02"] = output_contains("(?i)(TAM|SAM|SOM|Porter|unit economics)")` 作为框架应用的辅助信号（llm judge 仍是主判），提高 script 覆盖率

**O-5: pattern 元数据修正**

- 位置: SCORING.yaml L2 `pattern: mindset`
- 问题: mindset 目标 ~50 行，body 322 行——形态更像 process
- 修复: 若按 I-2 压缩后 body ~270 行，可考虑将 pattern 改为 `process`（目标 ~200 行，接近）; 或保留 mindset 并在 pattern 说明中注明"mindset 型知识手册"。该字段影响测评对标，应如实

**O-6: Industry Nuances 与 Investor Expectations 表格化**

- 位置: L303-307、L314-318
- 建议: 四行对比内容（SaaS/marketplace/consumer/B2B; angels/seed/Series A/Corporate）用表格呈现，可读性提升明显，改动成本 ~5 行

**O-7: 补充 allowed-tools**

- 位置: frontmatter
- 建议: 添加 `allowed-tools: WebSearch, Read, Write`（该 skill 明确依赖 web search 获取实时数据，声明后评测工具使用更可预期）

### 修复工作量估计

- 预计修改行数: ~35 行删除（F-1 的 3 处 + I-2 冗余）+ ~60 行新增（F-2 Limitations/Use-when + I-1 决策表 + I-5 一行）
- 预计修改文件数: 1 个（SKILL.md）为主; SCORING.yaml 可选微调（O-1/O-2/O-5）; check.py 可选（O-4）
- 总工作量: ~95 行变更，1-3 个文件
- 修复后预期评级: 🟢 B+ ~ A-（82-85/100）——全部修复点均为低风险文本改动，无结构性重写需求

---

## 附录: 审查过程记录

### 读取文件清单

| 文件 | 行数 | 读取方式 |
|------|:----:|----------|
| SKILL.md | 322 | 全文逐行精读 |
| SCORING.yaml | 179 | 全文 |
| check.py | 73 | 全文 |
| _shared/SKILL-SPEC.md | 162 | 全文（合规依据） |
| skill-dossier.md（memory） | 1203 | 全文（065 条目引用） |
| 057-go-to-market-planner/SKILL.md | — | 抽查（命令交叉验证） |
| 266-customer-persona-builder/SKILL.md | — | 抽查（命令交叉验证） |

### 读取统计

- 总读取行数: 约 2,000 行
- 审查文件数: 3 个（skill 目录内）+ 2 个（_shared 规范、dossier）+ 2 个（交叉验证）
- 无效引用: 6 处（1 死文件 + 3 虚构命令 + 2 虚构 skill 名）
- 发现问题数: 3 个致命 + 5 个重要 + 7 个优化
- 总审查行数（REVIEW.md）: 600+ 行

### 审查方法

- 所有文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则
- 虚构引用验证: 对 corpus 全量 `ls` + `grep` 交叉验证（skill 目录名、斜杠命令出现位置）
- 交叉参照: skill-dossier.md 的 065 条目作为既有结论基线，本次审查补充 7 项增量发现
