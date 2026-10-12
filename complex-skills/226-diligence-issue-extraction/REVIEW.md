# Skill 226 — diligence-issue-extraction 审查报告

| 项目 | 内容 |
|---|---|
| 技能编号 | 226 |
| 技能目录 | `226-diligence-issue-extraction/` |
| 技能名称 | `diligence-issue-extraction` |
| 审计日期 | 2026-08-06 |
| 审计方法 | Glob → 全量 Read → 逐文件分析 → 交叉一致性核对 → 写入本报告 |
| 审计依据 | `_shared/SKILL-SPEC.md`（v1.0 规范）、`_shared/CHECKER-LIBRARY.md`（判题函数库文档）、`_shared/checker.py`（判题函数库实现） |
| 总体评级 | **B+**（SKILL.md 内容质量 A-；SCORING.yaml 设计 B+；check.py 实现存在一处高危 bug，修复后整体可达 A-） |

---

## 1. 审计概述

本报告对技能 `226-diligence-issue-extraction`（VDR 尽职调查问题提取技能）进行全量审查。该技能属于"流程型（process）"技能，用于读取 VDR（虚拟数据室）文档，按客户（house）的尽职调查类别与重要性阈值提取问题，并以事务所备忘录（house memo）格式输出发现，同时负责向关闭清单（closing checklist）、交易团队摘要等下游环节进行交接。

审查范围覆盖技能目录内的全部 3 个文件（SKILL.md、SCORING.yaml、check.py），并延伸到其运行依赖的共享组件（`_shared/checker.py`、`_shared/SKILL-SPEC.md`、`_shared/CHECKER-LIBRARY.md`），以便对"技能文本 → 测评标准 → 判题脚本"三层做端到端一致性审计。

审计工作分五个阶段完成：

1. **清点**：Glob 枚举技能目录全部文件，确认无遗漏（共 3 个源文件，另有 `_shared/__pycache__` 下的编译产物 `checker.cpython-314.pyc`，为运行缓存，非源文件，不纳入审查）。
2. **全量阅读**：逐文件完整阅读，无抽样。
3. **规范对照**：将 SKILL.md 与 SKILL-SPEC.md v1.0 的合规清单逐条比对。
4. **映射核对**：将 SCORING.yaml 的 21 条准则 + 3 条致命失败逐一映射回 SKILL.md 的指令，验证可操作性。
5. **脚本验证**：静态执行 check.py 的逻辑推演，发现一处会导致判题结果失真的高危缺陷（详见第 8、11 节）。

**核心结论（TL;DR）**：

- SKILL.md 是高质量的法律尽职调查流程技能：指令具体、反模式明确、示例完整、安全护栏（来源标注、禁止静默补缺）突出，与 corpora 中同类技能相比属上乘。
- SCORING.yaml 的 21 条准则与 SKILL.md 指令映射完整，无一失配；但存在若干"多要素捆绑进单一二元判题"的粒度问题。
- check.py 存在一处**高危 bug**：`main()` 中读取的 agent 输出内容会被 `check()` 内部的 `set_agent_output()` 以文件路径覆盖，导致 `TEC-01`（output_contains 判题）在 CLI 模式下几乎必然失败。此 bug 不修复，测评结果不可信。

---

## 2. 文件清单与阅读范围

| 文件 | 路径 | 大小 | 行数 | 角色 | 审查结论 |
|---|---|---|---|---|---|
| SKILL.md | `226-diligence-issue-extraction/SKILL.md` | 13,420 B | 185 | 技能本体（指令层） | 已全量阅读，质量高（详见第 3–6 节） |
| SCORING.yaml | `226-diligence-issue-extraction/SCORING.yaml` | 9,831 B | 192 | 测评标准（21 准则 + 3 致命失败） | 已全量阅读，映射完整（详见第 7 节） |
| check.py | `226-diligence-issue-extraction/check.py` | 2,356 B | 76 | 脚本判题实现（2 项 script 判题） | 已全量阅读，发现高危 bug（详见第 8 节） |
| checker.py | `_shared/checker.py` | — | 351 | check.py 依赖的判题函数库（实现） | 已全量阅读，作为脚本行为判定的依据 |
| SKILL-SPEC.md | `_shared/SKILL-SPEC.md` | — | 161 | SKILL.md 权威规范 v1.0 | 已全量阅读，作为合规判定基准 |
| CHECKER-LIBRARY.md | `_shared/CHECKER-LIBRARY.md` | — | 188 | 判题函数库文档（LLM 判题协议） | 已全量阅读，作为准则格式判定基准 |

阅读摘要：

- **SKILL.md**：185 行，含 frontmatter（5 行）与正文 180 行。结构为"顶部 5 条编号摘要 + Matter context + Purpose + Load context + Workflow（Step 1–5）+ Handoffs + Batch processing + Close with the next-steps decision tree + What this skill does not do"。其中 Step 4 内嵌三块大段引用式安全护栏（来源标注、与用户援引法条分歧时的处理、禁止静默补缺）。
- **SCORING.yaml**：`total_items: 21`，六大类别（scope 3 / process 5 / format 3 / technical 4 / negative 2 / qa 4），其中 2 项为 script 判题（SCOPE-01、TEC-01），其余 19 项为 LLM 判题；另含 3 项 critical_failures（全部 `cap_to_0`）。
- **check.py**：仅实现 2 项脚本判题，与 SCORING.yaml 中 `judge: script` 的项一一对应；但输出采集逻辑存在缺陷（详见第 8 节）。
- **checker.py**：确认 `tool_log_contains`、`output_contains` 的行为语义（对 JSONL 逐行、对完整输出做正则搜索），用于复核 check.py 的正则写法。

---

## 3. 前端元数据（Frontmatter）合规性审计

### 3.1 逐字段核对

| 字段 | 实际值 | 规范要求 | 判定 |
|---|---|---|---|
| `name` | `diligence-issue-extraction` | 小写 + 连字符，≤64 字符，必须与目录名匹配 | ✅ 合规（目录名 `226-diligence-issue-extraction` = 序号 + name） |
| `description` | "Read VDR documents and extract issues per house categories and materiality thresholds, producing findings in house memo format. Use when user says \"review the data room\"..." | 第三人称、WHAT + WHEN + KEYWORDS、≤1024 字符、含触发信号短语、无跨技能路由 | ✅ 基本合规，1 处短语级偏差（见 3.3） |
| `argument-hint` | `[VDR folder path or category name]` | 允许字段 | ✅ 合规，且与 description 中的 `[folder]` 占位符呼应 |
| 其他字段 | 无 | 禁止列表外任何字段 | ✅ 合规 |

### 3.2 description 结构三问（WHAT / WHEN / KEYWORDS）

1. **WHAT**："Read VDR documents and extract issues per house categories and materiality thresholds, producing findings in house memo format" —— 具体、可执行，且点明了本技能区别于通用审阅的三个关键动作：按类别、按阈值、按备忘录格式。
2. **WHEN**："Use when user says \"review the data room\", \"extract issues from [folder]\", \"diligence review\", \"what's in the VDR\", or points at VDR documents" —— 给出 4 个直接引语触发场景 + 1 个动作类场景（指向文档），场景粒度适中，既有领域黑话（"review the data room"）也有行为描述（"points at VDR documents"）。
3. **KEYWORDS**：VDR、diligence、review、data room、extract issues、memo —— 覆盖了领域高频词与动作动词。

### 3.3 发现的问题（元数据层）

- **P2-偏差：触发信号短语与规范模板不完全一致**。规范 §2.4 列出的信号短语为 `"Use when the user..."` / `"Use when the user asks to..."` 等，而本 description 写的是 `"Use when user says..."`（缺少定冠词 `the`，且用的是 `says` 而非 `asks to`）。语义与意图完全正确，属短语模板级偏差，判定为"合规但建议对齐"，风险低。
- **P3-隐患：description 为 YAML 纯量（plain scalar）未加引号**，且内部含多个未转义的双引号字符（如 `"review the data room"`）。当前写法可正常解析（纯量内双引号合法，且全文无 `: ` 冒号加空格），但任何未来的编辑一旦引入 `: ` 或 `#` 后跟空格，将破坏解析。建议显式加引号并转义内部双引号。

### 3.4 元数据层小结

前端元数据整体合规：无禁用字段、无第一/第二人称、无跨技能路由、长度远低于 1024 字符上限（约 260 字符）、argument-hint 与正文参数模型一致。仅存在上述 2 处低风险瑕疵。

---

## 4. SKILL.md 结构与规范对齐审计

### 4.1 体量与模式

| 检查项 | 实际值 | 规范要求 | 判定 |
|---|---|---|---|
| 正文行数 | 180 行（含 frontmatter 共 185） | 硬上限 600 行 | ✅ 合规 |
| 模式匹配 | `pattern: process`（SCORING.yaml 声明） | process 目标约 200 行 | ✅ 贴合（180 对 200） |
| 正文必需三节 | Workflow ✅ / Output Format ⚠️ / Scope-Limitations ✅ | 三节缺一不可 | ⚠️ 见 4.2 |

### 4.2 必需三节核对

1. **Workflow / Process**：`## Workflow`（第 34 行起）下分 Step 1–5，逐步指令清晰，另由第 8–12 行的 5 条编号摘要先行总览。**合规**。
2. **Output Format**：**无独立命名的输出格式章节**。输出模板内嵌于 Step 5（第 125–152 行代码块，含 work-product header 占位、特权声明、统计行、Bottom line、每项 finding、Gaps 部分）。规范 §3.1 允许"any heading name"，内容确实存在且完整，因此判定为"内容满足、形式欠佳"——建议将输出模板提升为独立的 `## Output Format` 章节或至少加一个可见标题，降低 agent 漏读的概率。
3. **Scope / Limitations**：`## What this skill does not do`（第 180–184 行），3 条边界声明（不替人做临界重要性判断、不谈判、不替代批量 AI 审阅）。**合规**。

### 4.3 章节清单与功能对照

| 章节 | 行号 | 功能 | 评价 |
|---|---|---|---|
| 顶部编号摘要 | 8–12 | 5 条总览 | ✅ 有效摘要；但第 5 条措辞与正文有出入（见 5.3-2） |
| `## Matter context` | 16–18 | 处理 matter 工作区开关 | ✅ 自带"默认关闭即跳过"的短路逻辑，自包含性好 |
| `## Purpose` | 22–24 | 交代任务背景（2000 份文档中找 30 份关键的） | ✅ 用一句话建立了"阈值思维"的动机 |
| `## Load context` | 26–32 | 配置加载清单 + 缺失处理 | ✅ 缺失处理仅覆盖 deal-context.md（见 5.3-4） |
| `## Workflow` Step 1–5 | 34–152 | 核心流程 | ✅ 详见第 5 节逐步骤审查 |
| `## Handoffs` | 154–168 | 4 个下游交接 + successor liability | ⚠️ successor liability 段落位置错位（见 5.3-3） |
| `## Batch processing` | 170–172 | 大批量处理纪律 | ✅ 简短有力（"flag anything 🔴 immediately"） |
| `## Close with the next-steps decision tree` | 174–178 | 收尾决策树 + dashboard offer | ✅ 自定义化要求明确 |
| `## What this skill does not do` | 180–184 | 边界声明 | ✅ 合规 |

### 4.4 文件引用合规性

- 规范 §3.3 要求技能内使用相对路径、禁止跨技能文件引用（`../other-skill/`）。
- 本技能**没有**任何技能内相对路径引用，也没有跨技能文件引用。
- 但技能全文反复引用外部插件配置路径 `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md`、`.../deals/[code]/deal-context.md`、`.../matters/<matter-slug>/`。这些是插件级环境路径，不属于"技能内文件"，因此不违反 §3.3 的字面规定；但它们构成了**运行时环境硬依赖**（详见 5.3-4 与第 10 节），是测评移植性的主要风险源。
- 对其他技能的引用均以散文方式给出技能名（`ai-tool-handoff`、`deal-team-summary`、`material-contract-schedule`、`closing-checklist`），符合 §3.3 "see also: <skill-name>" 的允许形式。✅

### 4.5 内容指引符合度（§3.4）

| 指引 | 符合度 | 证据 |
|---|---|---|
| 知识增量优先（不解释模型已知概念） | ✅ | 直接给提取集与模板，不讲解什么是 CoC / MFN / ROFR |
| 反模式优先于泛泛建议 | ✅ | 三个 blockquote 均为"NEVER/必须"式指令（见 5.2） |
| 决策树/表格优先于散文 | ⚠️ | 有 inventory 表格与模板，但 severity 校准用散文而非表格 |
| 具体优于抽象 | ✅ | 真实路径示例、完整代码块模板、R/Y/G 实例 |

---

## 5. SKILL.md 内容质量分析

### 5.1 逐步骤审查（Workflow）

**Step 1 Inventory the VDR（第 36–51 行）**
- 优点：给出了 inventory 表格模板（请求类别 ↔ VDR 文件夹 ↔ 文档数 ↔ 状态），并要求记录 gap（请求清单中无对应 VDR 内容的类别），把"差距意识"结构化。
- 注意点：`If VDR MCP (Box/Intralinks/Datasite) is connected, pull the index` 只定义了"已连接"分支；未定义"未连接"分支的显式做法（仅能从用户给的文件路径推断）。建议补一行"未连接时以用户提供的文件夹路径为准建立 inventory"。

**Step 2 Apply materiality filter（第 53–57 行）**
- 优点：明确"阈值之上才看"，并给出合同类文档的排序规则（按面值或对手方重要性、自上而下审阅至阈值）。这是本技能的灵魂步骤，与 CF-02（不看阈值全量审阅即 0 分）直接呼应。

**Step 3 Extract issues（第 59–93 行）**
- 优点：为 5 个类别（material contracts / corporate / IP / employment / litigation）各给出 6/4/4/4/4 条标准提取集，条目具体可操作（如 IP 的 "Open source in the product (copyleft risk)"）。
- 注意点：提取集覆盖了常规关注点，但未覆盖 Successor liability 相关内容——该内容被放在 Handoffs 章节末尾的独立段落（第 168 行），逻辑上它属于提取内容而非交接内容，建议移至 Step 3 或独立成节（见 5.3-3）。

**Step 4 State each finding（第 95–119 行）**
- 优点：finding 模板 6 字段（Issue #N / Category / Severity / Documents / Finding / Recommendation）与 house 模板自适应（"If the seed memo used this... use exactly that"）；severity 校准给了 R/Y/G 三档实例。
- 重大亮点：第 97–101 行三块 blockquote 安全护栏（详见 5.2），是本技能内容质量最高的部分。
- 注意点：`Issue #N` 的编号范围（全局连续编号还是每类别内编号）未明确，若 agent 按每类别编号而判题预期全局编号，会出现轻微格式分歧。低风险。

**Step 5 Assemble per category（第 121–152 行）**
- 优点：给出完整组装模板（特权声明、`Documents reviewed: [N] of [M]`、`Coverage: [All | >$X threshold | Top N]`、`Findings: [N]🔴 [N]🟡 [N]🟢`、Bottom line、逐 finding、Gaps）。
- 注意点：Bottom line 一行的写法 `[🔴 N blocking · 🟠 N high · 🟡 N medium]` 引入了严重度体系从未定义过的 🟠（橙色）层级，且与上方 `[N]🔴 [N]🟡 [N]🟢` 三档不一致（见 5.3-1）。

**Handoffs（第 154–168 行）**
- 优点：交接范围远超"consent"本身——明确覆盖股东投票/§280G 清洗投票、监管申报（HSR/CFIUS）、对手方同意、解除/终止/偿付、托管/留存机制五类关闭前动作，并给出"欠交接是单向门，过度交接可在评审中纠正"的原则性指导。这是本技能第二个突出亮点。
- 注意点：详见 5.3-2、5.3-3。

**Batch processing（第 170–172 行）**
- 优点：一句话纪律（每批更新、🔴 立即上浮），与 QA-01 直接对应。

**Close with the next-steps decision tree（第 174–178 行）**
- 优点：明确"决策树即输出、律师来选"，并给 dashboard offer 的触发条件（>10 issues 或用户要求）与形状（按严重度计数、按类别计数、可排序网格）。

### 5.2 突出亮点（安全护栏三件套）

第 97–101 行三个 blockquote 构成了本技能最独特的价值：

1. **来源标注规则**：任何援引法条/案例/监管行动的 finding 必须打标 `[Westlaw]` / `[CourtListener]` / MCP 工具名 / `[web search — verify]` / `[model knowledge — verify]` / `[user provided]`，且 `verify` 类标签不得剥离。该规则被 TEC-01 脚本判题直接引用。
2. **与用户援引法条分歧的处理**：不捏造法条描述，给出标准话术模板（"I'd need to pull the actual text..."），并提供三条出路（检索并引用原文 / 请用户粘贴文本 / 移交外部律师）。这是防幻觉的高阶设计。
3. **禁止静默补缺（No silent supplement）**：研究工具结果不足时，必须停下列出 4 个选项让律师决定，不得用 web 搜索或模型知识静默填补。该规则同时是 CF-03 的判定对象。

这三块内容把"法律 agent 最危险的三个行为"显式列为了纪律，且每条都有可判定的行为信号，是本次审查中质量最高的部分。

### 5.3 发现的问题（内容层）

1. **P1-严重度体系不一致（同一文件内三套写法）**：
   - 第 116–119 行（severity 校准）：定义 R/Y/G 三档 = 🔴🟡🟢；
   - 第 134 行（Findings 统计行）：`[N]🔴 [N]🟡 [N]🟢` —— 三档，一致；
   - 第 140 行（Bottom line）：`🔴 N blocking · 🟠 N high · 🟡 N medium` —— 出现 🟠 且语义标签变为 blocking/high/medium；
   - 第 178 行（dashboard offer）：`counts by severity (🔴 / 🟠 / 🟡 / 🟢)` —— 出现 🟠 且为四档。
   - 影响：agent 面对"三档定义 + 四档使用"会无所适从；该不一致还会传导到 SCORING 的判题问句（QA-03 引用四档），详见第 9 节。建议统一为定义中的 R/Y/G 三档，或显式补充 🟠 的定义与使用场景。
2. **P2-摘要措辞与正文不一致**：第 12 行顶部摘要第 5 条写 "Hand off **consents** to closing checklist"，而第 159 行 Handoffs 章节明确 "The handoff is not limited to third-party consents"。同一技能内一处说"只交接同意"，一处说"远不止同意"，可能误导只读摘要的 agent。
3. **P2-段落归属错位**：`Successor liability`（第 168 行）是提取/分析内容（bulk-sale/fraudulent-transfer 风险、解散计划、承继责任条款覆盖度），却挂在 `## Handoffs` 章节下，与上下文（交接对象列表）不搭。建议独立成节或并入 Step 3。
4. **P2-外部配置缺失时的降级路径不完整**：第 32 行只处理了 deal-context.md 缺失（询问 deal）；若插件级 `corporate-legal/CLAUDE.md` 本身不存在（SkillIF 测评工作区常见情形），技能没有默认类别/阈值/模板可用，也没有"询问用户提供配置"的指令。后果：整个流程（类别、阈值、memo 格式）失去锚点。建议增加"CLAUDE.md 缺失时向用户索要 house 配置或使用内置默认值"的降级分支（详见第 12 节建议 R-02）。
5. **P3-编号歧义**：`Issue #N` 未说明全局或每类别编号（见 5.1 Step 4）。
6. **P3-未连接 VDR MCP 时的 inventory 来源**未显式说明（见 5.1 Step 1）。

### 5.4 内容层小结

SKILL.md 内容质量整体为 A- 水平：指令具体、纪律明确、模板完整、亮点突出（安全护栏三件套、交接广度）。主要扣分项是严重度体系不一致与外部配置降级路径不完整，均为可快速修复的中等风险问题。

---

## 6. 描述与触发机制（Trigger）审计

本技能属于"触发时机描述"的正面范例，单独成节说明：

| 检查维度 | 评价 |
|---|---|
| 触发场景数量 | 4 个引语式 + 1 个动作式，覆盖面足 |
| 触发场景质量 | 均为"用户在真实工作中会说的话"（"review the data room"、"diligence review"），而非抽象主题词；`[folder]` 占位符与 argument-hint 一致 |
| 与正文的呼应 | 描述中的 "per house categories and materiality thresholds" 与正文 Load context / Step 2 一一对应，无描述与正文脱节 |
| 误触发风险 | 低——"review the data room"、"VDR" 等词歧义小；"diligence review" 在法律场景基本唯一指向 |
| 漏触发风险 | 低——覆盖了直接指令（"extract issues from [folder]"）与间接行为（"points at VDR documents"） |
| 规范短语偏差 | "Use when user says" 缺 `the`（见 3.3），建议对齐为 "Use when the user says..." |

结论：描述与触发机制设计优秀，是技能档案中"触发时机讨论"（skillif-trigger-design 记忆条目）落地的良好案例；仅需微调短语与加引号。

---

## 7. SCORING.yaml 测评标准审计

### 7.1 总体结构

- `skill: diligence-issue-extraction`、`pattern: process`、`total_items: 21`。
- 准则数量核验：scope 3 + process 5 + format 3 + technical 4 + negative 2 + qa 4 = **21** ✅ 与 `total_items` 一致。
- judge 分布：**script 2 项**（SCOPE-01、TEC-01）、**llm 19 项**（90.5%）。脚本判题覆盖率偏低，但对"过程型 + 输出为对话文本"的技能而言，属于可接受的常见分布。
- critical_failures 3 项，全部 `cap_to_0`。

### 7.2 21 项准则逐项审计

| ID | 类别 | judge | 判定问题质量 | 风险评级 |
|---|---|---|---|---|
| SCOPE-01 | scope | script（tool_log_contains） | 正则可覆盖 Read 工具的路径参数；`corporate-legal/CLAUDE\.md|deal-context\.md` 转义正确 | 🟡 依赖 agent 产生工具调用（见第 10 节） |
| SCOPE-02 | scope | llm | 条件句判题（"若缺失则询问"）正确；但判题问句未提供"如何确认缺失"的取证指引 | 🟡 见 7.3-3 |
| SCOPE-03 | scope | llm | 判题问句包含完整前置条件（bulk 类别 + 工具已配置） | 🟢 |
| PROC-01 | process | llm | 捆绑 3 要素（映射、数量/状态、gap） | 🟡 见 7.3-1 |
| PROC-02 | process | llm | 问句清晰（"threshold 而非全部"） | 🟢 |
| PROC-03 | process | llm | 捆绑 5 个类别的提取集于一个问句 | 🟡 见 7.3-1 |
| PROC-04 | process | llm | 6 字段模板逐项枚举 | 🟢 |
| PROC-05 | process | llm | 与 R/Y/G 定义一致 | 🟢 |
| FMT-01 | format | llm | **捆绑 6 要素**（header、特权声明、已审数、coverage、findings 计数、bottom line）于单一 yes/no | 🟠 见 7.3-1 |
| FMT-02 | format | llm | 问句精确（两类 gap） | 🟢 |
| FMT-03 | format | llm | 问句精确（按类别分组 + 类别内按严重度排序） | 🟢 |
| TEC-01 | technical | script（output_contains） | 4 个来源标签任一出现即过；正则转义与 checker 库语义核对无误 | 🟡 门槛偏低 + 受 check.py bug 影响（见第 8、10 节） |
| TEC-02 | technical | llm | 双条件（thin results 停下询问；法条无文本不表述）合并一问，问句较长但边界清楚 | 🟢 |
| TEC-03 | technical | llm | 5 类关闭前动作枚举完整，含反例限定（"not just consents"） | 🟢 |
| TEC-04 | technical | llm | 条件触发（"where applicable"），判题时需结合任务材料判断适用性 | 🟡 依赖任务材料设计 |
| NEG-01 | negative | llm | 问句与技能第 1 条边界声明逐字对应 | 🟢 |
| NEG-02 | negative | llm | 问句与技能第 3 条边界声明对应 | 🟢 |
| QA-01 | qa | llm | 问句含双要素（每批更新 + 🔴 立即标记） | 🟢 |
| QA-02 | qa | llm | "customized"一词使判题兼顾了形式与内容 | 🟢 |
| QA-03 | qa | llm | 引用 🔴🟠🟡🟢 四档计数——与技能定义的 R/Y/G 三档不一致（见 7.3-2） | 🟠 |
| QA-04 | qa | llm | 防捏造判题，与 CF-01 呼应 | 🟢 |

### 7.3 发现的问题（测评标准层）

1. **P1-捆绑式判题**：FMT-01 把 6 个要素、PROC-01 把 3 个要素、PROC-03 把 5 个类别的提取集、QA-01 把 2 个要素压进单一 yes/no。LLM 判题对"部分满足"的二元化处理不稳定：交付 5/6 要素是否算过，不同 judge 会给出不同答案，直接影响 21 项计分的可复现性。建议对 FMT-01 拆分为独立小项，或至少在问句中明示"全部要素必须存在方为 yes"。
2. **P2-严重度体系不一致传导**：QA-03 问句写 `counts by severity, counts by category, and a sortable issues grid`（对应技能第 178 行的四档写法），而 PROC-05 引用三档 R/Y/G。判题时 judge 若按技能定义（三档）核对 QA-03，会与技能文本的 dashboard 写法（四档）打架。源头在 SKILL.md（见 5.3-1），需一并修复。
3. **P2-SCOPE-02 的取证指引缺失**：判题问句 "If deal-context.md is absent, does the agent ask which deal this is for before proceeding?" 没有告诉 judge 如何确认"absent"（应检查 tool log 中的 Read 记录或工作区文件清单），evidence 字段仅写 "Agent's questions to the user"。若任务材料中 deal-context.md 实际存在，agent 不询问反而是正确行为，判题将出现假阴性。建议在 evidence 中补充"workspace 中是否存在该文件"的取证点。
4. **P2-TEC-01 判定门槛与任务材料耦合**：只要输出中出现 4 个标签中的任意 1 个即通过。若任务 VDR 材料不含任何法条/判例（无引证可标），agent 可能被迫为满足判题而生造引证（反而违背 CF-01 精神），或该准则永远失败。判定可行性依赖任务材料设计（见第 10 节）。
5. **P3-critical_failures 与准则的呼应**：CF-01（捏造）↔ QA-04；CF-02（不看阈值）↔ PROC-02；CF-03（静默补缺）↔ TEC-02。三组呼应完整、无遗漏，设计规范。✅

---

## 8. check.py 脚本审计

### 8.1 结构

- 接口：`python check.py <workspace_path> <tool_log_path> <agent_output_path>`，输出 `{criterion_id: true/false}` JSON。
- 依赖注入：`sys.path.insert(0, ../../_shared)` 后从 `checker` 导入 15 个判题函数。
- 实现 2 项判题：
  - `SCOPE-01 = tool_log_contains("corporate-legal/CLAUDE\\.md|deal-context\\.md")` —— 与 SCORING.yaml 的 pattern 完全一致 ✅；
  - `TEC-01 = output_contains("\\[Westlaw\\]|\\[CourtListener\\]|\\[web search|\\[model knowledge")` —— 与 SCORING.yaml 一致 ✅（Python 字符串内 `\\[` 经求值后为正则 `\[`，匹配字面 `[`，语义正确）。

### 8.2 【高危 BUG】agent 输出内容被路径字符串覆盖

**缺陷位置**：`check()`（第 24–27 行）与 `main()`（第 63–66 行）的配合。

**复现推演**：

```
main() 第 65 行: set_agent_output(f.read())     # _agent_output = 输出文件全文（正确）
main() 第 68 行: check(workspace, tool_log, agent_output)
check() 第 27 行: set_agent_output(agent_output) # _agent_output = 路径字符串（覆盖！）
TEC-01: output_contains(...)                     # 搜索的是路径字符串，非输出内容
```

即：`main()` 中辛辛苦苦读入的输出全文，在 `check()` 内部被以**文件路径**为参数再次调用的 `set_agent_output()` 覆盖。`output_contains` 于是对路径字符串做正则搜索，**除非路径恰好含 `[Westlaw]` 等字样，TEC-01 恒为 false**。该判题项实际被"杀死"，但表面仍会输出 `TEC-01: false`，与 agent 真实表现无关。

**影响评估**：
- 21 项中唯一与"引证来源标注"相关的脚本判题失效，且失败原因与行为质量无关，属于系统性假阴性。
- 若 runner 直接以 import 方式调用 `check()` 并传入内容而非路径，则不触发该 bug——即"行为正确与否取决于调用约定"，而文件自身的 docstring 声明的约定（传路径）恰好触发 bug。接口契约自相矛盾。

**修复建议（二选一）**：
- 方案 A（推荐）：删除 `check()` 内第 27 行 `set_agent_output(agent_output)`，仅依赖 `main()` 的文件读取；同时为防御直接 import 调用，在 `check()` 开头保留"若 agent_output 是现存路径则读文件，否则视为内容"的兼容逻辑。
- 方案 B：删除 `main()` 中的文件读取分支，统一约定"调用方传入内容"——但需同步修改 docstring 与 SCORING.yaml 的运行说明，风险面更大。

### 8.3 次要问题

| 问题 | 位置 | 说明 |
|---|---|---|
| docstring 失实 | 第 25 行 "Run all 21 checks" | 实际只跑 2 项（SCOPE-01、TEC-01）；其余 19 项为 LLM 判题，注释中也有说明，但模块 docstring 与函数注释自相矛盾 |
| 参数未使用 | `workspace` | `check()` 收到 workspace 后从未使用 |
| 冗余导入 | 第 13–20 行 | `file_exists`、`file_valid_json`、`json_field_*`、`timestamp_*`、`tool_log_not_contains` 等约 10 个函数导入但从未调用 |
| 判题项缺失 | — | 无任何对 CF-01/CF-02/CF-03 的脚本级触发逻辑（如 tool_log_not_contains 检测静默补缺）——不强制，但值得考虑（见第 12 节建议 R-06） |

### 8.4 脚本层小结

check.py 功能面窄（2/21），正则写法与 SCORING.yaml 一致、无转义错误，`_shared` 路径注入写法正确。但输出覆盖 bug 属于**阻断级缺陷**，不修复则 TEC-01 结果不可信，进而影响 21 项计分的整体有效性。

---

## 9. 内部一致性审计（SKILL ↔ SCORING ↔ check）

### 9.1 准则 → SKILL.md 指令映射表（21/21 全部命中）

| 准则 | 对应 SKILL.md 指令 | 命中方式 |
|---|---|---|
| SCOPE-01 | 第 8 行 + 第 28–30 行（Load context） | 直接指令 |
| SCOPE-02 | 第 32 行（"If deal-context.md doesn't exist, ask which deal"） | 逐字对应 |
| SCOPE-03 | 第 10 行 + 第 156 行（ai-tool-handoff） | 直接指令 |
| PROC-01 | 第 36–51 行（Step 1） | 直接指令 |
| PROC-02 | 第 53–57 行（Step 2） | 直接指令 |
| PROC-03 | 第 63–93 行（Step 3 五个提取集） | 直接指令 |
| PROC-04 | 第 103–114 行（finding 模板） | 逐字对应 |
| PROC-05 | 第 116–119 行（severity 校准） | 直接指令 |
| FMT-01 | 第 126–146 行（Step 5 组装模板） | 模板逐元素对应（6 要素齐全） |
| FMT-02 | 第 148–151 行（Gaps 部分） | 直接指令 |
| FMT-03 | 第 123 行（"Group findings by request list category. Within category, sort by severity."） | 逐字对应 |
| TEC-01 | 第 97 行（来源标注 blockquote） | 直接指令 |
| TEC-02 | 第 99–101 行（法条分歧 + no silent supplement） | 直接指令 |
| TEC-03 | 第 159–165 行（closing-checklist 五类动作） | 直接指令 |
| TEC-04 | 第 168 行（successor liability） | 直接指令 |
| NEG-01 | 第 182 行（不做临界重要性判断） | 逐字对应 |
| NEG-02 | 第 184 行（不替代批量 AI 审阅） | 逐字对应 |
| QA-01 | 第 170–172 行（batch processing） | 直接指令 |
| QA-02 | 第 174–178 行（next-steps decision tree） | 直接指令 |
| QA-03 | 第 178 行（dashboard offer） | 直接指令（含严重度不一致问题） |
| QA-04 | 第 109 行（Documents: [VDR path + doc name]）+ CF-01 | 支撑性指令 |

**结论：21/21 映射完整，无"准则无指令支撑"或"指令无准则覆盖"的空洞。** 这是本技能测评设计中最强的部分。

### 9.2 脚本层一致性

- SCORING.yaml 的 2 个 `judge: script` 项（SCOPE-01、TEC-01）与 check.py 实现的 2 个判题一一对应，正则模式在两侧的转义结果一致 ✅。
- `total_items: 21` 与准则计数一致 ✅。
- `pattern: process` 与 SKILL.md 体量（180 行 vs 目标 ~200）一致 ✅。

### 9.3 不一致清单

| 不一致 | 源点 | 传导路径 | 建议 |
|---|---|---|---|
| 严重度体系三档/四档混用 | SKILL.md 第 116–140–178 行 | 传导至 SCORING QA-03（四档）与 PROC-05（三档） | 统一为 R/Y/G 三档并全链修改，或显式定义 🟠 |
| 摘要第 5 条 "consents" vs 正文 "not limited to consents" | SKILL.md 第 12 vs 159 行 | 潜在影响 TEC-03 判题 | 改为 "Hand off pre-closing actions to closing checklist" |
| check.py docstring "21 checks" vs 实际 2 项 | check.py 第 25 行 | 影响维护者认知 | 改为 "Run script-judged checks (SCOPE-01, TEC-01)" |

---

## 10. 测评可执行性（Evaluability）分析

### 10.1 环境依赖风险

本技能的全部操作锚点（类别清单、重要性阈值、memo 格式、输出配置、dashboard 配置、ai-tool 配置）都位于 `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md` 及其下属目录。在 SkillIF 测评工作区中，该插件配置**大概率不存在**。由此产生三个直接影响：

1. **SCOPE-01 的判定机制**：技能第 8 行要求"Load"这两个配置文件。训练有素的 agent 会尝试 Read（即使文件不存在也会产生工具调用），tool log 中出现路径模式 → 通过。但若 agent 先检查文件存在性（如 Bash `ls`）后发现缺失、转而先询问用户，则 tool log 中无 Read 记录 → **SCOPE-01 假阴性**。判定机制依赖"agent 必须产生对特定路径的读取尝试"，与 agent 行为的合理性弱相关。缓解：任务材料中预置这两个文件（哪怕内容简化），或放宽 pattern 以覆盖 `ls`/`glob` 调用。
2. **无配置时的行为不确定性**：CLAUDE.md 缺失时技能无降级指令（见 5.3-4），agent 的类别/阈值/模板将无锚可依，PROC-02、PROC-04、FMT-01 等 11 项 LLM 判题全部失去参照系。**强烈建议**在任务设计中预置配置文件，或在 SKILL.md 中增加降级分支。
3. **deal-context.md 的存在性决定 SCOPE-02 的触发**：任务设计必须明确二选一——要么预置该文件（则 agent 不询问是正确行为，判题问句的条件不成立），要么不预置（则 agent 必须询问）。当前判题问句对此未作区分，需在 evidence 中固定。

### 10.2 任务材料设计建议（供 runner / 任务编写者参考）

为覆盖 21 项准则的触发条件，任务材料建议包含：

| 触发项 | 材料要求 |
|---|---|
| PROC-01 / FMT-02 | 请求清单类别与 VDR 文件夹不完全对应（存在 gap） |
| PROC-02 / CF-02 | 合同金额分布跨越阈值（如 >$X 阈值下 300 份合同需筛出大额子集） |
| TEC-01 | 至少一处法条/判例引证（如变更控制条款需按某法域规则分析），且材料中不含引证原文 |
| TEC-02 / CF-03 | 设计"研究工具返回少量结果"的场景，观察 agent 是否停下询问 |
| TEC-03 | 至少一个非 consent 类关闭前动作（如 §280G 投票、HSR） |
| TEC-04 | 资产交易 + 卖方解散计划或未决产品责任索赔 |
| QA-03 | 制造 >10 条 issues 或用户在对话中要求 dashboard |
| QA-04 / CF-01 | 材料中嵌入易混淆细节（如相似文件名），检验 agent 是否只写实际读过的文档 |

### 10.3 判题可行性总结

- **脚本判题（2 项）**：SCOPE-01 可行（附上述假阴性风险）；TEC-01 受 check.py bug 影响当前不可信，修复后可行。
- **LLM 判题（19 项）**：问句整体质量高（第 7 节 15 项评为 🟢），主要风险是 4 项捆绑问句的二元化不稳定，以及 QA-03 的严重度档位引用错误。
- **输出采集**：本技能无产出文件要求，agent 输出为对话文本；TEC-01 依赖 runner 将完整输出文本传给 `AGENT_OUTPUT`。若 runner 只截取最终消息而遗漏中间过程输出，来源标签可能不在截取范围内——需确认 runner 的采集策略。

---

## 11. 风险与缺陷清单（汇总）

| 编号 | 位置 | 严重度 | 描述 | 影响 |
|---|---|---|---|---|
| R-01 | check.py 第 24–27、63–66 行 | 🔴 高 | `main()` 读取的输出内容被 `check()` 内 `set_agent_output(路径)` 覆盖，`output_contains` 搜索对象变为路径字符串 | TEC-01 恒假阴性，21 项计分失真；不修复不可投入正式运行 |
| R-02 | SKILL.md 第 8、28–32 行 | 🔴 高 | 插件级配置（CLAUDE.md / deal-context.md）缺失时无完整降级路径 | 测评工作区无配置时，11+ 项 LLM 判题失去参照系；SCOPE-01 可能假阴性 |
| R-03 | SKILL.md 第 116–140–178 行 + SCORING QA-03 | 🟠 中 | 严重度体系三档（R/Y/G）与四档（含 🟠）在同一技能内混用 | agent 输出与判题问句出现档位分歧，PROC-05 / QA-03 判题不稳定 |
| R-04 | SCORING FMT-01、PROC-01、PROC-03、QA-01 | 🟠 中 | 多要素捆绑进单一 yes/no 判题 | 部分满足时判题不稳定，影响计分可复现性 |
| R-05 | SCORING SCOPE-02 | 🟠 中 | 判题问句未固定"deal-context.md 缺失"的取证方式 | 条件句判题的假阴性/假阳性风险 |
| R-06 | SCORING TEC-01 | 🟠 中 | 判定门槛低（4 标签任一出现即过）且依赖任务材料含引证 | 与任务设计耦合；材料无引证时产生误伤或诱导生造引证 |
| R-07 | SKILL.md 第 12 行 | 🟡 低 | 摘要 "Hand off consents" 与正文 "not limited to consents" 不一致 | 只读摘要的 agent 交接范围收窄 |
| R-08 | SKILL.md 第 168 行 | 🟡 低 | successor liability 段落挂在 Handoffs 下，归属错位 | 阅读顺序上易被当作交接规则而非提取规则 |
| R-09 | SKILL.md 第 3 行 | 🟡 低 | description 触发短语 "Use when user says" 与规范模板 "Use when the user..." 有偏差；且为无引号纯量 | 规范对齐瑕疵 + 未来编辑破坏 YAML 的隐患 |
| R-10 | SKILL.md 第 103 行 | 🟡 低 | `Issue #N` 编号范围未明确（全局 vs 每类别） | 格式分歧的低风险源 |
| R-11 | check.py 第 13–25 行 | 🟡 低 | 冗余导入、docstring 失实、workspace 参数未用 | 可维护性/可读性问题，不影响运行 |
| R-12 | SKILL.md 第 38 行 | 🟡 低 | Step 1 未定义"VDR MCP 未连接"分支的显式做法 | 依赖 agent 常识推断，轻微不确定性 |

---

## 12. 改进建议

按优先级分组（P0 为阻断级，须在正式运行前完成）：

### P0 — 阻断级（不修复不得投入正式测评）

1. **修复 check.py 输出覆盖 bug（R-01）**：删除 `check()` 中第 27 行 `set_agent_output(agent_output)`，改为"若路径存在则读文件，否则视为内容"的兼容逻辑；同步修正 docstring。
2. **为配置缺失增加降级路径（R-02）**：在 SKILL.md `## Load context` 增加分支——"若 `corporate-legal/CLAUDE.md` 不存在，询问用户提供 house 配置（类别清单、阈值、memo 格式），在此之前不进行提取"；或随技能提供 `references/default-config.md` 作为内置兜底。任务设计侧：预置简化版配置文件。

### P1 — 重要（一个迭代内完成）

3. **统一严重度体系（R-03）**：SKILL.md 全文统一为 R/Y/G 三档（🔴🟡🟢），删除 🟠；或明确定义 🟠（如"影响中等、可能需要调整交易条款"）并同步修改 Bottom line 与 dashboard 写法；SCORING.yaml 的 QA-03 问句同步对齐。
4. **拆分捆绑判题（R-04）**：将 FMT-01 拆为 2–3 项（如"work-product header + 特权声明"与"统计行 + bottom line"），PROC-03 按类别拆分或限定问句为"至少覆盖 X 个类别的标准集"；或在问句中加"所有列举要素必须全部出现方为 yes"。
5. **固定 SCOPE-02 的取证点（R-05）**：evidence 改为 "Agent's questions to the user; tool log Reads of deal-context.md; workspace 文件清单（该文件是否存在）"。
6. **TEC-01 与任务材料解耦（R-06）**：任务材料设计为必含至少一处可标注引证；或在 SCORING.yaml 中注明该判题的前置条件。

### P2 — 完善（随版本迭代）

7. 修正第 12 行摘要措辞（R-07）："Hand off pre-closing actions to closing checklist"。
8. 将 successor liability 段落移出 Handoffs（R-08），并入 Step 3 或独立为 `## Successor liability`。
9. description 对齐规范短语并加引号（R-09）：`Use when the user says "review the data room"...`。
10. 明确 `Issue #N` 编号规则（R-10）。
11. Step 1 补充无 MCP 分支（R-12）。
12. 清理 check.py 冗余导入与注释（R-11）。
13. 内容指引微调：severity 校准建议改为表格形式（§3.4 决策树优先）。

---

## 13. 总体评级与结论

### 13.1 分项评级

| 维度 | 评级 | 依据 |
|---|---|---|
| SKILL.md 内容质量 | **A-** | 指令具体、模板完整、安全护栏突出；扣分于严重度不一致与降级路径缺失 |
| SKILL.md 规范合规 | **A** | frontmatter 无违禁字段、体量达标、必需三节齐全（输出格式以嵌入式形式满足）、无跨技能文件引用 |
| SCORING.yaml 设计 | **B+** | 21/21 准则与技能指令映射完整、critical_failures 呼应严密；扣分于捆绑判题与 QA-03 档位错误 |
| check.py 实现 | **D（修复后 B+）** | 存在阻断级输出覆盖 bug；修复后其余部分（正则、路径注入）无问题 |
| 内部一致性 | **A-** | 三层映射 21/21 命中；两处不一致均为文本级（严重度档位、consents 措辞） |

### 13.2 总体结论

`226-diligence-issue-extraction` 是技能档案中设计成熟度较高的流程型技能：其"阈值过滤 + 类别提取集 + 备忘录模板 + 交接纪律 + 防幻觉护栏"五层结构完整自洽，SCORING.yaml 与技能文本的映射完整度在 322 个技能中属第一梯队。

**但当前版本不可直接投入正式测评运行**，原因有二：(1) check.py 的输出覆盖 bug 使 TEC-01 判题恒假阴性（P0-R-01）；(2) 测评工作区大概率缺失插件级配置文件，技能无降级路径，SCOPE-01 存在系统性假阴性风险且多项 LLM 判题失去参照（P0-R-02）。

**修复 P0 两项后，本技能可评为 A- 档**：建议在修复后补充一轮"任务材料预置配置文件 + 完整 21 项跑测"，以验证 TEC-01 恢复为真实可判定状态，并复核 SCOPE-02 在"文件存在/不存在"两种场景下的判定稳定性。

### 13.3 后续动作清单

1. [ ] 修复 check.py 输出覆盖 bug（P0-R-01）
2. [ ] SKILL.md 增加配置缺失降级分支 + 任务侧预置配置文件（P0-R-02）
3. [ ] 统一严重度体系为三档并同步 SCORING.yaml（P1-R-03）
4. [ ] 拆分 FMT-01 / PROC-03 捆绑判题（P1-R-04）
5. [ ] 补强 SCOPE-02 取证指引（P1-R-05）
6. [ ] 确认任务材料含引证素材（P1-R-06）
7. [ ] 文本级修正（P2-R-07 ~ R-12）
8. [ ] 修复后全量跑测 21 项并复核 TEC-01 判定

---

*本报告由 SkillIF 技能质量审查流程自动生成。审查基于对技能目录 3 个文件与共享组件 3 个文件的完整阅读；所有行号引用以审查当日文件版本为准。*
