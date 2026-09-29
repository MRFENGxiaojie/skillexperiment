# REVIEW: 198-pricing-strategist

**审查日期**: 2026-08-06
**Skill 类型**: tool — 交互式定价策略构建（读取业务上下文 + 定向提问 + 输出分层定价策略）
**Body 行数**: 197 行 | **参考文件数**: references/0, scripts/0, 其他/0
**SCORING pattern**: tool | **SCORING total_items**: 20 | **check.py 脚本检查数**: 4（SCOPE-02, PROC-01, PROC-03, FMT-03）

---

## 1. 目录全量清单

```
198-pricing-strategist/
├── SKILL.md                 197 行  ← 唯一正文来源
├── SCORING.yaml             183 行  ← 20 个测评点 + 3 个 critical failure
└── check.py                  80 行  ← 4 项脚本检查，其余 16 项为 llm judge
```

- **目录总数**: 3 个文件；references/ 0 个、scripts/ 0 个、其他子目录 0 个。
- **结构评述**: 极简扁平结构，无任何参考文件。所有知识（Question Bank、Pricing Principles、Output Format 模板）全部内联在 SKILL.md body 中。对于一个"咨询型" skill 而言这种内联可接受，但代价是 body 信息密度高、部分硬约束（如 FOUNDER_CONTEXT.md 依赖）没有配套文档支撑（详见 §5.2）。
- **行数对比**: SKILL.md 197 行 vs SCORING.yaml 183 行——测评基础设施（183 行）几乎与技能正文（197 行）等重，说明该 skill 的测评点定义非常细，但正文/测评的对齐问题也值得逐条核对（见 §10）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `pricing-strategist`。
- **格式**: 全小写 + 连字符 ✅；与目录名 `198-pricing-strategist`（NNN-kebab-case）剥离编号后完全一致 ✅；长度 17 字符 ≤ 64 ✅。
- **结论**: ✅ 通过。

### 2.2 description
原文:
> Builds comprehensive pricing strategies by reading business context and asking targeted questions interactively. Use when user needs pricing plans, tier structures, price points, pricing model recommendations, or any pricing-related strategy for their product or service.

- **WHAT**: "Builds comprehensive pricing strategies by reading business context and asking targeted questions interactively" —— 动作 + 方式齐全，第三人称 ✅。
- **WHEN / 触发信号**: "Use when user needs pricing plans, tier structures, price points, pricing model recommendations, or any pricing-related strategy for their product or service" —— 含标准触发短语 "Use when" + 5 组关键词（pricing plans / tier structures / price points / pricing model recommendations / any pricing-related）✅。触发词覆盖面充足。
- **人称**: 全篇第三人称（"user needs…their product"）✅，无 you/your/I/we。
- **长度**: 约 252 字符，远低于 1024 ✅。
- **跨 skill 路由**: 无任何其他 skill 名或插件名 ✅。
- **结论**: ✅ 通过。唯一可挑剔点：句子以"Builds"开头略显生硬，但完全合规。

### 2.3 allowed-tools
- **字段不存在**。SKILL.md frontmatter 只有 name 与 description。
- **必要性分析**: 该 skill 的核心交互工具是 **AskUserQuestion**（SKILL.md:58），在 Claude Code 默认工具集中 AskUserQuestion 并非标准内置工具，而是测评 harness / 特定环境的扩展工具。skill 对它有硬依赖（PROC-03 脚本检查 `AskUserQuestion` 是否出现在 tool log 中），却在 frontmatter 中既未通过 allowed-tools 声明、也未在 description 中提及。若评测环境未注入该工具，PROC-03 必然失败。
- **结论**: ⚠️ 建议补充 `allowed-tools: [AskUserQuestion]`（若 harness 支持）或至少在正文明确该工具的来源与替代方案。

### 2.4 其他字段
- 无 argument-hint、user-invocable、model、paths、disable-model-invocation 等字段。
- SKILL-SPEC v1.0 允许字段集内未使用的字段均非必需，**未使用不属于违规**；同时也没有任何禁止字段（如 allow/deny 类）出现 ✅。
- 注: $ARGUMENTS 的执行模式（SKILL.md:15-24）依赖 harness 注入 $ARGUMENTS 变量，但未通过任何 frontmatter 字段声明——与 2.3 同类问题，属于"环境契约未书面化"。

### 2.5 YAML语法
- frontmatter 为标准的 `key: value` 结构，description 为单行 plain scalar，无引号嵌套问题、无制表符、无非法锚点。YAML 可正常解析 ✅。
- 正文第一个 H1（# Pricing Strategist）与 frontmatter 由 `---` 正确分隔 ✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行号范围 | 标题/段落 | 行数 | 内容摘要 |
|---|---|---|---|
| 1-5 | frontmatter | 5 | name + description |
| 6 | `# Pricing Strategist` (H1) | 1 | 页标题 |
| 8-10 | `## Purpose` | 3 | 一句话使命 |
| 13-25 | `## Execution Logic` | 13 | $ARGUMENTS 双模式（loaded 消息 vs 直接执行） |
| 28-91 | `## Task Execution` | 64 | 6 步主流程 |
| 30-41 | `### 1. MANDATORY: Read FOUNDER_CONTEXT.md` | 12 | 阻塞式前置步骤 |
| 43-58 | `### 2. Determine Which Questions to Ask` | 16 | Question Bank（7 问）+ 提问纪律 |
| 46-56 | Question Bank 表格 | 11 | 7 行：问题/理由/跳过条件 |
| 60-70 | `### 3. Determine Strategy Type` | 11 | 5 条件 → 策略类型决策表 |
| 72-78 | `### 4. Build the Pricing Strategy` | 7 | 每档 5 要素（名称/价格/理由/功能/人群） |
| 80-86 | `### 5. Add the Strategic Layer` | 7 | 定位/心理战术/升级触发/收入优化/风险 |
| 88-90 | `### 6. Format and Verify` | 3 | 收尾：套模板 + 自查 |
| 94-107 | `## Pricing Principles` | 14 | 11 条硬约束 |
| 111-150 | `## Output Format` | 40 | 完整输出模板（代码块 113-150） |
| 154-181 | `## Quality Checklist (Self-Verification)` | 28 | 4 组 16 项自查 |
| 185-197 | `## Defaults & Assumptions` | 13 | 8 条默认假设 |

合计 197 行，其中代码块占 40 行（Output Format 模板）。

### 3.2 必需章节
- **Workflow/Process**: ✅ `## Task Execution`（6 个编号步骤，步骤间有 BLOCKING 依赖和条件分支）——符合要求。
- **Output Format**: ✅ `## Output Format`（113-150 行给出完整 markdown 模板，含每个 tier 块的字段占位）。
- **Scope/Limitations**: ❌ **缺失**。全篇没有 "Not in scope" / "Limitations" / "Scope" 章节。`## Defaults & Assumptions`（185-197）只定义默认值，不界定边界（例如：不涵盖哪些定价问题、何时应拒绝任务、对合规/法律类定价咨询的边界等）。这是 12 项规范清单中唯一明确缺失的章节（见 §7 第 10 项）。

### 3.3 内容委托
- 全文没有任何 `@other-skill` 委托或跨 skill 调用 ✅。
- 唯一的"委托"是 Step 1 要求读取 **工作区文件** `FOUNDER_CONTEXT.md`——这是对评测环境工作区的依赖，不是 skill 间委托（详见 §5.2 与 §13-🔴-1）。
- 决策委托设计良好：Step 3 明确 "Make this decision yourself — do not ask the user"，把策略类型决策留给 agent，与 PROC-04/CF-02 呼应 ✅。

### 3.4 标题层级连续性
- 标题链: H1(1) → H2(8 个) → H3(10 个) → 无 H4/H5。层级连续，无跳级 ✅。
- H3 全部位于 `## Task Execution` 和 `## Quality Checklist` 之下，归属清晰 ✅。
- 编号步骤（1-6）与 H3 标题一一对应，无重号/漏号 ✅。
- **唯一瑕疵**: `### 2` 内部 Question Bank 表格（46-56 行）与"Use AskUserQuestion"指令（58 行）之间没有子标题分隔，表格后直接接段落，可读性尚可但不影响层级。

### 3.5 vs 600行限制
- 197 行，仅为上限的 33%。✅ 无超限风险。
- 若将 Question Bank / Pricing Principles / Output Format 全部外置为 references 可进一步减负，但当前密度合理，不构成问题。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接（N→N+1）
- **Step 1 → Step 2**: Step 1 读完 FOUNDER_CONTEXT.md 后，Step 2 明确要求"cross-reference 上下文与 Question Bank，只问缺失的信息"——衔接严密，且 Step 2 的"Skip if…"列直接消费 Step 1 的提取清单（target audience、competitors、business goals）✅。
- **Step 2 → Step 3**: "收集所有输入后决定结构"——条件完备，Step 3 决策表覆盖 Step 2 问题 1/2（B2B/B2C、pricing model）的输出 ✅。
- **Step 3 → Step 4**: 策略类型决定 tier 结构，Step 4 按类型定义每档——衔接自然 ✅。
- **Step 4 → Step 5**: 从 tier 设计到"定位/心理/升级触发"的战略层，符合"先结构后策略"顺序 ✅。
- **Step 5 → Step 6**: 明确 "Structure output per Output Format" + "Run through Quality Checklist"——两个下游章节都被显式引用，无孤儿步骤 ✅。
- **Execution Logic → Task Execution**: $ARGUMENTS 空 → "loaded" 消息 → 等待用户上下文（即 Step 2 的输入来源）；$ARGUMENTS 非空 → 直接进入 Step 1。衔接自洽 ✅。

### 4.2 内部矛盾
- **年费折扣三处表述不一致**（🟡）:
  - Step 4 (SKILL.md:75): "annual ≈ 20% off monthly"
  - Pricing Principles (SKILL.md:100): "20-25% off"
  - Defaults (SKILL.md:191): "Annual discount: 20%"
  - Quality Checklist (SKILL.md:166): "Annual pricing is 20-25% below monthly"
  
  20% 落在 20-25% 区间内，不算硬矛盾，但"≈20%"与"20-25%"并存会给 agent 造成轻微歧义：当 agent 输出 25% 折扣时，自查清单（20-25%）通过而 Step 4 的"≈20%"若被严格理解则不通过。建议统一为"20-25%"。
- **`$47/mo` 示例 vs 通用原则**: SKILL.md:104 说 "$47/mo reads more trustworthy than $50/mo. Use this deliberately — **not on every price point, but on the hero tier**"，与 Step 4 "Use specific numbers" 不矛盾，但"hero tier 用 charm pricing"与 Principles 的"charm pricing"战术（Step 5 要求命名）一致 ✅。
- **4 档上限**: Principles (SKILL.md:101) "Never show more than 4 tiers" 与 Defaults (SKILL.md:190) "4 only if B2B with a clear Enterprise segment" 一致 ✅。
- **问题数量上限**: SKILL.md:58 "Maximum 7 questions total" 与 Quality Checklist (SKILL.md:159) "7 or fewer" 一致 ✅。

### 4.3 示例/代码正确性
- body 无代码片段，唯一的"示例"是 Output Format 模板与 `$47/mo` 价格示例，均正确无误。
- Output Format 模板内部一致性检查:
  - 模板头部含 "Strategy type" + "Why this structure" ✅（对应 FMT-01）。
  - Tier 块含 Price/Who it's for/What's included/Price justification 四要素 ✅（对应 FMT-02）。
  - 模板的 Tier 3 用 "[same structure]" 简写——对 agent 是明确指令，无误 ✅。
  - 模板含 Positioning & Psychology / Revenue Optimization / Biggest Pricing Risk 三小节 ✅（对应 QA-01/QA-02/NEG-02）。
- 数值一致性: 模板 "save Z%" 与 FMT-03 的 `[0-9]+% off|save [0-9]+%` 正则匹配方向一致 ✅。

### 4.4 条件完整性
- **FOUNDER_CONTEXT.md 缺失分支缺失**（🔴）: Step 1 是 BLOCKING（"DO NOT PROCEED"），但全篇没有"文件不存在怎么办"的分支。若评测工作区没有该文件，agent 将陷入死锁：读不到 → 不能进 Step 2 → 也不能跳过（CF-01 会 cap_to_0）。虽然评测方预期提供该文件，skill 自身仍应防御（见 §13-🔴-1）。
- **$ARGUMENTS 分支完备**: 空/未提供 vs 含内容，两分支互斥且全覆盖 ✅。
- **Question Bank 跳过条件完备**: 7 个问题均标注 "Skip if…"，且 Step 2 明示 "Never ask something the context already answers" ✅。
- **"最多 7 问"的终止条件**: "If the first batch gives you enough…stop"——提前终止条件已写清 ✅。
- **Step 3 决策表覆盖性**: 表内 6 行覆盖 B2B/B2C × 订阅/用量/一次性/免费增值 的主流组合；"Mixed signals → Hybrid" 兜底 ✅。但"非订阅、非 B2B/B2C 的混合信号"（如 B2B2C）未显式提及——Hybrid 行可覆盖，属轻微遗漏。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵
该 skill **无 references/ 目录**，正文中引用的外部资源仅一处:

| 被引用资源 | 引用位置 | 是否打包 | 评估 |
|---|---|---|---|
| `FOUNDER_CONTEXT.md`（项目根目录） | SKILL.md:30,33 | ❌ 未打包（工作区文件） | 依赖评测工作区提供；无缺省分支（见 §4.4） |
| AskUserQuestion 工具 | SKILL.md:58 | ❌ 环境工具 | 依赖 harness 注入；frontmatter 未声明（见 §2.3） |
| $ARGUMENTS 变量 | SKILL.md:15-24 | ❌ 环境变量 | 依赖 harness 注入 |

无任何 "见 references/xxx.md" 类引用——因为根本没有 references 目录，不存在悬空引用 ✅。但也不存在任何参考文件来分担 body 的 197 行内容。

### 5.2 不可见资源审计
- **FOUNDER_CONTEXT.md**: 是 skill 能否运行的关键资源（BLOCKING 前置），但**不在 skill 目录内、不由 skill 作者维护、也不在 frontmatter paths 中声明**。评估者必须手工构造该文件且内容要覆盖 Question Bank 所需的全部字段（受众/竞品/收入目标/现有定价），否则 PROC-02（只问缺失问题）与 Step 2 将难以评分。**风险等级: 高**。
- AskUserQuestion / $ARGUMENTS: 环境契约未书面化（同 §2.3 结论）。

### 5.3 文件全文审查
无 references/、无 scripts/ 文件可审。SKILL.md / SCORING.yaml / check.py 三个文件的全文审查分散在 §2-§10 各节（frontmatter、body、测评点、脚本逐条核对）。

### 5.4 跨Skill引用
- 全文无 `../`、无绝对跨 skill 路径 ✅。
- description 无跨 skill 路由 ✅。
- FOUNDER_CONTEXT.md 是工作区相对路径（"from the project root"），合法 ✅。

### 5.5 嵌套重复/死文件
- 无子目录、无死文件。目录内 3 个文件全部在流程中发挥作用（SKILL.md 被 agent 读取；SCORING.yaml 被 runner 读取；check.py 被执行）✅。

---

## 6. 语法与格式质量

### 6.1 拼写错误
- 通读全文未发现拼写错误。抽查高风险词: "interactively" (SKILL.md:3)、"credibility" (:104)、"Paradox of choice" (:101)、"anchor"/"anchoring"（多次）、"willingness" (:76,165)、"justification/justified"（多次）——均正确 ✅。
- "pre-revenue"（:102）、"habit-forming"（:106）、"no-brainer"（:100）连字符使用正确。

### 6.2 语法错误
- 未发现语法错误。句式以祈使句+短陈述为主（skill 惯用风格），信息密度高但语法正确。
- SKILL.md:101 "Paradox of choice kills conversion at the pricing page."——定冠词省略为惯用法，可接受。

### 6.3 中英/葡英混杂
- 全英文，无中文、无葡萄牙语、无其他语言混入 ✅（该技能无任何翻译残留）。

### 6.4 Markdown破损
- 所有表格管道对齐正确（Question Bank 表 :48-56、策略类型表 :63-70），表头分隔行格式合法 ✅。
- 代码块: Output Format 模板的 ```markdown 围栏成对（:113 与 :150）✅。
- 加粗/引用/列表符号（-、*）使用一致 ✅。
- 无破损链接、无裸 HTML ✅。

### 6.5 占位符未填充
- Output Format 模板中的 `[Company Name]`、`$X/mo`、`[Tier 1 Name]` 等方括号占位是**有意的模板占位符**（该段落本身就是给 agent 的输出模板），不属于未填充内容 ✅。
- 正文其余部分无悬空占位符 ✅。

### 6.6 截断
- 全文以完整句收尾（:197 "Document any assumptions made in the output."），无截断 ✅。

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name 小写+连字符 ≤64 且匹配目录 | ✅ | `pricing-strategist` = 目录名去 NNN 前缀，17 字符 |
| 2 | description 第三人称 WHAT+WHEN+关键词 ≤1024 | ✅ | 252 字符；"Builds…"（WHAT）+ "Use when user needs…"（WHEN+5 组关键词） |
| 3 | description 无祈使/第一/第二人称 | ✅ | 全第三人称；"Use when" 为规范触发短语，不算违规 |
| 4 | description 无跨 skill 路由 | ✅ | 未提及任何其他 skill/插件 |
| 5 | 至少一个触发信号 | ✅ | "Use when user needs pricing plans…" 等 5 组 |
| 6 | 无禁止 frontmatter 键 | ✅ | 仅 name/description |
| 7 | body ≤ 600 行 | ✅ | 197 行 |
| 8 | 存在 workflow/process 章节 | ✅ | `## Task Execution` + 6 编号步骤 |
| 9 | 存在 output format 章节 | ✅ | `## Output Format`（含完整模板） |
| 10 | 存在 scope/limitations 章节 | ⚠️ | **缺失**；`Defaults & Assumptions` 只覆盖默认值，不界定边界 |
| 11 | 无跨 skill 文件路径（../） | ✅ | 全文无 |
| 12 | 目录 NNN-kebab-case | ✅ | `198-pricing-strategist` |

**合规小结**: 12 项中 11 项通过，1 项（scope/limitations）缺失。整体合规性良好，属"强内容、弱边界"型 skill。

---

## 8. 人机感评估

### 8.1 Emoji审计
- SKILL.md **全文 0 个 emoji**（grep 验证: 🟢🟡🟠🔴✗✅❌⚠️ 计数均为 0）✅。
- 自查清单用 `- [ ]` markdown checkbox，未用 emoji 表达完成态 ✅。风格中性。

### 8.2 全大写/喊叫
- 3 处全大写强调，全部集中在 Step 1 的阻塞语义上:
  - SKILL.md:30 "MANDATORY"
  - SKILL.md:31 "**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**"
  - SKILL.md:41 "**DO NOT PROCEED** to Step 2 until this file has been read."
- 评估: 三处均服务于"这是硬门槛"的功能语义（对应 CF-01 的 cap_to_0 惩罚），不是无意义喊叫；但"DO NOT SKIP THIS STEP"+"DO NOT PROCEED"叠用略冗余。**轻 ⚠️**：可保留一处全大写，其余降为正常加粗。

### 8.3 Persona语气
- 整体 persona: **果断、经验丰富的定价顾问**。语气特征: 短句 + 断言式 + 提供理由。
- 代表性引语（5-8 条）:
  1. "Never leave a price unjustified." (SKILL.md:76)
  2. "If no real customer would buy it, cut it." (SKILL.md:98)
  3. "The middle tier is the hero. Design the strategy so most customers land there." (SKILL.md:99)
  4. "A crippled free tier is worse than no free tier." (SKILL.md:103)
  5. "$47/mo reads more trustworthy than $50/mo." (SKILL.md:104)
  6. "B2B + deal size above $200/mo → seat-based pricing is almost always correct." (SKILL.md:105)
  7. "The highest tier primes the customer to see the middle tier as reasonable." (SKILL.md:107)
  8. "Specific numbers build credibility" (SKILL.md:104)
- 评估: persona 一致且有效——断言式语气为该领域最佳实践（给 agent 明确的决策杠杆），无个人化口吻、无卖萌、无过度热情。

### 8.4 人机边界
- 边界清晰: 机器该做什么（读文件、决策策略类型、构建输出）与用户该提供什么（缺失上下文、偏好）明确分工（Step 1-6 + "do not ask the user" 指令）✅。
- "AskUserQuestion" 是用户交互通道，被明确限定在"最高优先级且上下文缺失"的问题上，防止机器骚扰用户 ✅。
- 无"假装人类"表述，无情感化语言 ✅。

### 8.5 人称分析（grep 实测）
| 词 | 出现次数 | 位置/性质 |
|---|---|---|
| you | 5 | :19 加载消息（给用户的问候语）; :51,:54,:55,:56 Question Bank 问题措辞（"do you prefer"、"your target customer"）; :58 "gives you enough" |
| your | 4 | :19, :54, :55, :56（同上） |
| yourself | 1 | :61 "Make this decision yourself" |
| I | 2 | :157-158 自查清单 "I read…" / "I only asked…" |
| we/us/our | 0 | — |
- **分析**: 第二人称集中在两处合理场景——(a) "loaded" 加载消息是给用户的直接招呼；(b) Question Bank 的问题本身面向用户提问，用 you 是自然的。但 :61 "yourself" 是对 **agent 自己** 说的（"Make this decision yourself"），:157-158 "I read…" 是 agent 的第一人称自查——这两处违反了规范 item 3 的字面要求（body 不应有第一/第二人称指令）。**⚠️ 轻微违规**，修复成本极低（见 §13-🟡-2）。

### 8.6 表格太多 → 转换为自然语言
- body 共 3 张表: Question Bank（7 行）、策略类型决策表（6 行）、Principles 为项目符号（非表）。密度不高，且每张表都是"条件-动作/理由"型决策表，**表格是信息的最优载体**，无需转自然语言 ✅。
- 唯一的可读性建议: Question Bank 7 行表 + 上方的 4 行说明段落（:44-58）可以在视觉上压缩，但无实质问题。

---

## 9. 可执行性评估

### 9.1 独立可执行性（0-10）: **7/10**
- 扣分点: (1) FOUNDER_CONTEXT.md 缺省分支缺失——若工作区无此文件即死锁（-1）；(2) AskUserQuestion / $ARGUMENTS 依赖未书面化的环境契约（-1）；(3) 无 Scope 边界，遇到不匹配任务（如成本核算、税务定价）时 agent 没有拒绝/转交依据（-1）。
- 得分理由: 主流程 6 步全部可直接执行；决策表、输出模板、自查清单三层闭环，agent 不需要额外知识即可产出合格交付物。

### 9.2 步骤可操作性
- 每一步都有"可操作的动词 + 明确产出": Step 1（读文件+提取 6 类信息）、Step 2（对照表提问、上限 7 问 4 问/批）、Step 3（查表决策）、Step 4（5 要素/档）、Step 5（5 要素）、Step 6（套模板+自查）——可操作性评级: **高** ✅。
- 自查清单 16 项全部是可布尔判定的项（"Strategy type is justified"、"4 tiers or fewer"），无模糊项 ✅。
- 唯一模糊点: Step 4 "annual ≈ 20% off" 与清单 "20-25%" 的歧义（§4.2）。

### 9.3 工具依赖
| 工具 | 用途 | 依赖类型 | 风险 |
|---|---|---|---|
| Read | 读 FOUNDER_CONTEXT.md | 必备（BLOCKING） | 高：文件缺失即死锁 |
| AskUserQuestion | 批量提问 | 必备（PROC-03 计分） | 中：环境可能无此工具 |
| 无其他工具 | — | — | — |
- 该 skill 不需要任何脚本/CLI 工具，输出纯文本 markdown。依赖面窄 ✅。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖
- **total_items: 20**，实际计数: SCOPE 3 + PROC 5 + FMT 4 + PRI 4 + NEG 2 + QA 2 = **20** ✅ 一致。
- **脚本 vs LLM 分工**: 脚本 4 项（SCOPE-02, PROC-01, PROC-03, FMT-03），LLM 16 项。check.py:80 恰好运行 4 项，与 yaml 中 `judge: script` 的数量完全一致 ✅。
- 每项脚本检查的正则与正文的对应关系:
  - `SCOPE-02` → `output_contains('pricing-strategist loaded')`: 与 SKILL.md:19 的加载消息精确匹配 ✅。注意: 该正则**大小写敏感**且要求整串——若 agent 说 "pricing-strategist loaded, ready…"（正文原句）则通过；若 agent 改写加载语（如 "Pricing strategist ready"）则误判失败。正文给的是原句，风险可控。
  - `PROC-01` → `tool_log_contains('FOUNDER_CONTEXT\.md')`: 与 SKILL.md:30,33 匹配 ✅。**弱点**: tool_log_contains 对整个 JSONL entry 做 regex（含 user 消息、Grep 结果等），任何一条日志出现该字符串即通过——例如用户提问中恰好包含文件名会**误报通过**；反之，如果 Read 调用以其他方式记录（filePath 字段而非完整路径）也可能漏报。建议改为校验 Read 工具条目（见 §13-🟡-3）。
  - `PROC-03` → `tool_log_contains('AskUserQuestion')`: 与 SKILL.md:58 匹配 ✅。
  - `FMT-03` → `output_contains('[0-9]+% off|save [0-9]+%')`: 检查"折扣表述"存在 ✅，但**不校验折扣幅度是否为 20-25%**——输出 "10% off" 也能通过。弱代理（见 §13-🟡-4）。
- **覆盖缺口**: 正文的 Pricing Principles 11 条中，"Enterprise = contact sales"（:102）、"B2C + habit-forming → monthly first"（:106）未映射到任何测评点；Quality Checklist 的 "Pre-Execution Check" 三项只有一项有对应脚本检查。非致命，属测评粒度选择。

### 10.2 Critical Failures分析
- CF-01（不读 FOUNDER_CONTEXT.md 即构建策略 → cap_to_0）: 与 SKILL.md:30-41 的 BLOCKING 语义一致 ✅。惩罚与正文强调力度匹配。
- CF-02（把策略类型决策抛给用户 → cap_to_0）: 与 SKILL.md:61 "Make this decision yourself — do not ask the user" 一致 ✅。
- CF-03（价格点无理由 → cap_to_0）: 与 SKILL.md:76 "Never leave a price unjustified" + FMT-02 一致 ✅。
- **评估**: 3 个 CF 全部命中正文真正的硬约束，无虚设 CF；CF 与正文的"禁止"语义一一对应，无冲突。
- **潜在陷阱**: CF-01 与 PROC-01 联动——若 agent 尝试读文件但文件不存在（Read 失败），tool log 仍会记录 Read 调用，PROC-01 可能通过而 CF-01（LLM judge）可能因"没有成功读取"判失败——评测需要区分"尝试读取"与"成功读取"。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**: `198-pricing-strategist: "总评: 🟡"`

**本次复核结论**: 🟡 判定**成立**，且理由可以明确:
- 优点部分（dossier 未详述，本次确认）: 结构清晰（6 步流程 + 决策表 + 模板 + 自查清单四层闭环）、description 合规、测评点与正文映射度高（20/20 计数一致、4 脚本检查逐一可回溯）、CF 设计精准。
- 支撑 🟡 的缺陷（本次确认存在）:
  1. 无 Scope/Limitations 章节（§7 第 10 项 ⚠️）——这是规范层面的硬缺口。
  2. FOUNDER_CONTEXT.md 依赖无缺省分支（§4.4）——可执行性风险。
  3. 年费折扣三处表述不一（§4.2）。
  4. 自查清单第一人称（§8.5）。
  5. AskUserQuestion 环境契约未书面化（§2.3）。
- **Dossier 未记录、本次新发现**:
  - FMT-03 正则不校验折扣幅度（§10.1）。
  - PROC-01 的 tool_log_contains 误报面（§10.1）。
  - "loaded" 消息大小写敏感的脆弱性（§10.1）。
  - Step 3 决策表对 B2B2C 等混合形态未显式覆盖（§4.4）。

---

## 12. 综合评分 — 8 dimensions weighted

| 维度 | /10 | 权重 | 加权 |
|------|:---:|:----:|:----:|
| Frontmatter合规 | 9 | 10% | 0.90 |
| Body结构完整 | 8 | 10% | 0.80 |
| 逻辑一致性 | 8 | 20% | 1.60 |
| 参考完整性 | 6 | 15% | 0.90 |
| 语法格式 | 9 | 10% | 0.90 |
| 规范合规 | 8 | 15% | 1.20 |
| 人机感 | 7 | 10% | 0.70 |
| 可执行性 | 8 | 10% | 0.80 |
| **加权总分** | | | **7.80 → 78/100** |

**Rating: 🟡 B（60-79）** — 与 dossier 总评 🟡 完全一致。

各维度评分理由:
- Frontmatter 9: 仅 allowed-tools 缺失声明（环境契约）扣 1。
- Body 结构 8: 无 Scope/Limitations 章节扣 1；步骤/模板/清单齐备（结构骨架完整）其余全过。
- 逻辑一致性 8: 折扣三处表述 + B2B2C 覆盖性小缺扣 2。
- 参考完整性 6: 无 references 本身不扣分，但唯一的运行时依赖 FOUNDER_CONTEXT.md 无缺省分支（高风险的"不可见资源"）是主要扣分项。
- 语法格式 9: 全文无拼写/语法/markdown 问题，仅"DO NOT"叠用扣 1。
- 规范合规 8: 12 项中 11 项过、scope 项缺。
- 人机感 7: 无 emoji 是加分项；"MANDATORY/DO NOT"喊叫 + 自查清单第一人称 + "yourself" 扣 3。
- 可执行性 8: 主流程可执行性高；死锁风险与工具契约扣 2。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（阻塞性/高影响，建议优先修复）

**🔴-1. FOUNDER_CONTEXT.md 缺失时无降级分支（可执行性死锁）**
- 位置: SKILL.md:30-41（Step 1 全节）
- 问题: Step 1 被标记为 BLOCKING（"DO NOT PROCEED to Step 2 until this file has been read"），但全 skill 没有任何"文件不存在"的处理逻辑。在无该文件的工作区中，agent 被困于"不能跳过（CF-01 惩罚）也不能继续（BLOCKING 指令）"的僵局；评测将无法进行或产生随机结果。
- 修复方案: 在 Step 1 内增加存在性分支:
  > "If `FOUNDER_CONTEXT.md` does not exist in the project root: (a) tell the user it is missing and ask them to provide the context inline (company, audience, existing pricing, competitors, goals), or (b) proceed to Step 2 using only the Question Bank, marking the strategy as built without business context ('context: minimal')."
- 后果: 修复后 agent 在任何工作区都有确定的行动路径，评测不会死锁；同时保留 CF-01 对"有文件却不读"的惩罚语义。

**🔴-2. 无 Scope/Limitations 章节（规范 item 10 硬缺口）**
- 位置: SKILL.md 全文（建议插入 `## Pricing Principles` 之后、`## Output Format` 之前，或作为独立 `## Scope & Limitations` 放在 `## Defaults & Assumptions` 附近）
- 问题: SKILL-SPEC v1.0 要求 body 含 scope/limitations 章节；当前 `Defaults & Assumptions` 只定义默认值。结果: agent 遇到边界外请求（如"帮我做成本加成定价公式"、"这家公司定价涉及法律合规风险"）时无据可依。
- 修复方案: 新增章节，至少覆盖:
  - 不做什么: 不做成本核算/财务建模、不做税务/合规/法务定价意见、不预测收入。
  - 做什么的边界: 面向 B2B/B2C 产品的订阅/一次性/用量/免费增值定价；单市场美元计价（除非另有说明）。
  - 何时退出: 上下文严重不足且用户拒绝补充时，明确告知"不足以构建可信策略"并给出最小可交付选项。
- 后果: 合规清单 12 项全绿；agent 获得拒绝/降级的书面依据，减少幻觉式硬答。

### 🟡 重要缺陷（影响一致性或评测鲁棒性）

**🟡-1. 年费折扣三处表述不一致**
- 位置: SKILL.md:75（"annual ≈ 20% off"）、:100（"20-25% off"）、:166（"20-25% below monthly"）、:191（"Annual discount: 20%"）
- 问题: 同一指标三种表述，agent 在生成价格与自查时可能采用不同基准，且 FMT-03 只查 "% off/save %" 字样不查数值，无法兜底。
- 修复: 统一为 "20-25%"，Step 4 改为 "annual ≈ 20-25% off monthly"，Defaults 改为 "Annual discount: 20-25% (default 20%)"。
- 后果: 消除自相矛盾的指令源；自查清单与步骤指令一致。

**🟡-2. 自查清单第一人称 + "yourself" 指令**
- 位置: SKILL.md:157-158（"I read FOUNDER_CONTEXT.md…"、"I only asked questions…"）、:61（"Make this decision yourself"）
- 问题: 规范 item 3 禁止第一人称指令化表述；且清单以 "I" 开头在 agent 执行时会造成"清单属于谁"的歧义（agent 把自己代入 I）。
- 修复: 改为无主/第三人称: "FOUNDER_CONTEXT.md was read before any question was asked" / "Only questions not answered by the context were asked"；"Decide the strategy type based on the conditions table — do not ask the user."
- 后果: 合规项 3 从 ⚠️ 变 ✅；指令主语统一为 agent 行为而非人格化。

**🟡-3. PROC-01 脚本检查误报面过大**
- 位置: SCORING.yaml:34-38（`fn: tool_log_contains`, pattern `FOUNDER_CONTEXT\.md`）
- 问题: `tool_log_contains` 对整条 JSONL entry 做 regex 匹配（`json.dumps(entry)`），用户消息、Grep 输出、Assistant 文本都可能包含该文件名，导致"未真正 Read 也判通过"。
- 修复: 改用更精确的检查——例如 `tool_log_order` 或新增带工具类型约束的检查（Read 工具 + filePath 含 FOUNDER_CONTEXT.md）；或依赖 LLM judge 的 PROC-02 交叉验证。
- 后果: 脚本检查与真实行为的相关性提高；避免高分低实。

**🟡-4. FMT-03 不校验折扣幅度**
- 位置: SCORING.yaml:92-95（pattern `[0-9]+% off|save [0-9]+%`）
- 问题: 输出 "5% off" 也能通过，与正文 "20-25%" 约束脱钩。
- 修复: 收紧为正则 `(20|21|22|23|24|25)% off|save (20|21|22|23|24|25)%`；或保持现状并标注为"宽松代理"。
- 后果: 测评对正文核心约束（折扣幅度）有真实约束力。

**🟡-5. "loaded" 消息大小写/整串敏感**
- 位置: SCORING.yaml:20-21（SCOPE-02, pattern `pricing-strategist loaded`）
- 问题: agent 若按正文原句输出则通过；若轻微改写（"Pricing strategist is loaded"）即误判失败。SCOPE-03（LLM）也依赖同一表述的语义。
- 修复: 在正文 :19 明确"输出必须逐字包含 `pricing-strategist loaded`"（现正文已给出原句，但未声明逐字要求），或在正则中放宽为 `pricing[- ]strategist loaded`。
- 后果: 脚本检查与正文指令的耦合更明确，降低偶然失败。

### 🟢 优化建议（非必需，锦上添花）

**🟢-1.** 在 SKILL.md:58 附近注明 AskUserQuestion 不可用时的降级路径（"If AskUserQuestion is unavailable, ask the questions in a single text message, batching highest-priority first"），使 skill 脱离环境假设。
**🟢-2.** Question Bank 的 7 问已覆盖主流字段，可考虑补充第 8 问（渠道/销售模式: 直销 vs 渠道 vs 自助）以支撑 Step 3 的 Hybrid 判定——非必需，加则需同步更新上限为 8 问或说明 7 问为默认。
**🟢-3.** 在 Output Format 模板的 `### [Tier 3 Name]` 后补一行显式指令 "[Repeat the block for each tier, max 4]"——现模板的 "[same structure]" 简写对多档输出有轻微歧义（3 档还是 4 档）。这与 PRI-01（≤4 档）一致。
**🟢-4.** 在 Quality Checklist 增加一行: "FOUNDER_CONTEXT.md existed and was read in full"——把 🔴-1 的降级分支（若采用）纳入自查闭环。
**🟢-5.** description 可加 "interactive" 关键词已存在；可再补 "tier structures" 已在列——无需改动。

### 修复工作量估计
- 🔴-1（缺省分支）: 约 15-30 分钟（加 4-6 行指令）。
- 🔴-2（Scope 章节）: 约 30-45 分钟（写 6-10 行边界条款）。
- 🟡-1（折扣统一）: 10 分钟。
- 🟡-2（人称改写）: 10 分钟。
- 🟡-3/-4/-5（SCORING 收紧）: 各 15-30 分钟，需要与评测 runner 验证 regex。
- 总计: 约 2-3 小时可完成全部必修项；仅修 🔴 两项约 1 小时。
- 优先级建议: 先 🔴-2（规范硬缺口，收益确定）→ 🔴-1（可执行性）→ 🟡-1/2（一致性/合规）→ 🟡-3/4/5（评测鲁棒性，可与 harness 变更同批做）。

---

## 附录: 审查过程记录

- **审查时间**: 2026-08-06
- **审查顺序**: 198 → 197 → 194（按任务指定逆序）
- **工具链**: Glob（目录清单）→ Read（全部文件全文）→ Bash `wc -l`（行数核验）→ Bash grep 正则（人称/emoji 计数）→ 人工逐行分析
- **已读文件（3/3，全文）**:
  - D:\SkillIF\skill-experiment\complex-skills\198-pricing-strategist\SKILL.md（197 行）
  - D:\SkillIF\skill-experiment\complex-skills\198-pricing-strategist\SCORING.yaml（183 行）
  - D:\SkillIF\skill-experiment\complex-skills\198-pricing-strategist\check.py（80 行）
- **辅助参考**: 同级 `_shared/checker.py`（351 行，确认 `tool_log_contains` 为全条目 json.dumps 正则、`output_contains` 为 MULTILINE 正则——支撑 §10.1 的误报面与正则行为分析）
- **行数核验方法**: `wc -l` 实测（SKILL.md 197 / SCORING.yaml 183 / check.py 80），与 Read 输出行号一致。
- **未修改任何文件**: SKILL.md、SCORING.yaml、check.py 均未改动；仅新建本 REVIEW.md。
- **评分一致性**: 加权总分 78 → 🟡 B，与 skill-dossier.md 中 "198-pricing-strategist: 🟡" 一致；§11 已列出 dossier 未记录的 4 项新发现。
