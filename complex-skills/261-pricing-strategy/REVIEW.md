# REVIEW — 261-pricing-strategy

**审查日期**：2026-08-06
**审查人**：Claude (SkillIF quality audit)
**Skill 类型**：process — SaaS 定价策略咨询（设计 / 优化 / 提价 / 定价页 / 定价调研五类场景）

审计方式：目录内全部 3 个文件全文通读（SKILL.md 310 行、SCORING.yaml 159 行、check.py 64 行）；另以脚本核验 description 长度、代码围栏配对、引用路径存在性、SCORING 计数一致性。
审计结论：内容专业度高、SKILL.md ↔ SCORING 的 17 项检查点映射精准、主动触发与置信度标注设计良好，是"问答式定价咨询"形态中质量靠前的技能；但存在两项**悬空引用**——SKILL.md 引用 `references/pricing-page-playbook.md` 与 `scripts/pricing_modeler.py`，两个文件均不存在。其中 `scripts/pricing_modeler.py` 同时是 SCORING 唯一脚本判定项（QA-02）的判定对象，**当前文件状态下 QA-02 恒为 False（17 项 criteria 中 1 项不可达）**；若 agent 按指令实际尝试运行该脚本，还会直接得到"文件不存在"错误。此外缺显式 Scope/Limitations 段、无编号化分步工作流、Output Format 无具体模板，属结构性缺口。

---

## 1. 目录清单

技能目录共 3 个文件，结构如下：

| # | 文件 | 行数 | 类型 |
|---|------|------|------|
| 1 | SKILL.md | 310 | 主文件（frontmatter + 三模式框架 + 9 个专题方法章节） |
| 2 | SCORING.yaml | 159 | 测评标准（17 项 criteria + 3 项 critical_failures） |
| 3 | check.py | 64 | 脚本检查（1 项：QA-02） |

**缺失项（关键）**：SKILL.md 第 263 行引用 `references/pricing-page-playbook.md`（定价页设计规格与文案模板），第 289 行引用 `scripts/pricing_modeler.py`（定价情景建模脚本）——目录中 **references/ 与 scripts/ 两个目录均不存在**，两个引用全部悬空（详见 4.3/4.4、9.2/9.3、第 13 节 R1/R2）。

结构观察：技能为"单文件自包含"形态，无 references/ 拆分。这在本评测集中属于少数派（322 个 skill 中大多数将深度内容拆入 references/）。对定价咨询类技能，单文件 310 行尚在可控范围，但"定价页设计规格"与"建模脚本"两处本应拆出的内容既未拆出、也未内联，留下两个空洞。

---

## 2. Frontmatter

### 2.1 name 字段

`name: pricing-strategy` 与目录名 261-pricing-strategy 的语义一致（去编号后缀），小写连字符命名规范，与 SCORING.yaml 的 `skill: pricing-strategy` 完全一致。合规。

### 2.2 description 的第三人称 WHAT+WHEN+KEYWORDS

description 全文（293 字符）：

> Design, optimize, and communicate SaaS pricing including tier structure, value metrics, pricing pages, and price increase strategy. Use when the user wants to create or revise pricing, design pricing tiers, choose value metrics, optimize pricing page UX, or plan price increase communications.

- WHAT：`Design, optimize, and communicate SaaS pricing including tier structure, value metrics, pricing pages, and price increase strategy` — 能力陈述，覆盖正文全部五个工作场景（设计 / 优化 / 提价 / 定价页 / 调研的"communicate"侧），与 Mode 1-3 + Pricing Page Design + Pricing Research Methods 章节一一对应。
- WHEN：显式的 `Use when the user wants to create or revise pricing, design pricing tiers, choose value metrics, optimize pricing page UX, or plan price increase communications`。
- KEYWORDS：pricing、tier、value metric、pricing page、price increase、SaaS — 密度适中，触发覆盖面与 SCORING SCOPE-01 的五类场景枚举对齐。
- 观察 1：WHAT 以祈使/动词短语（"Design, optimize, and communicate..."）开头，严格按 SKILL-SPEC 的"第三人称"字面要求，可改为 "Expert in designing, optimizing and communicating..."。语料库中此类能力短语写法被普遍接受（本技能在档案快速审查中亦被记为合规），属风格性而非阻断性偏差。
- 观察 2：description 未提及"输出含定价计分卡（0-100）"等具体交付物，但 OUT-03 的判定锚点（scorecard）在正文 Output Artifacts 表中有明确落点，description 不必重复。

### 2.3 description 长度

实测 293 字符（含标点），远低于 1024 上限。合规。

### 2.4 可选字段

Frontmatter 仅含 name 与 description，未使用任何可选字段（allowed-tools、argument-hint、user-invocable、model、paths、disable-model-invocation）。纯对话式咨询技能不依赖工具白名单，不设可选字段合理。合规。

### 2.5 禁止字段与格式

- 无 license、version、metadata 等规范禁止的自造字段。
- 描述中不含文件路径（`references/pricing-page-playbook.md` 与 `scripts/pricing_modeler.py` 出现在 body 中，见 4.3/4.4，属 body 内悬空引用而非 frontmatter 违规）。
- 无命令注入式内容；未出现 "import" 类引用。

结论：Frontmatter 整体合规，质量良好，仅在 WHAT 措辞人称上有可打磨空间。

---

## 3. Body 结构

### 3.1 Workflow/Process 完整性

Body 采用"三模式 + 九专题"结构：

```
Mode 1 Design Pricing From Scratch / Mode 2 Optimize Existing Pricing / Mode 3 Plan a Price Increase
  → The Three Axes（包装/价值指标/价格点）
  → Value Metric Selection → Good-Better-Best Tier Structure → Value-Based Pricing
  → Pricing Research Methods → Price Increase Strategies → Pricing Page Design
  → Proactive Triggers → Output Artifacts → Communication → Related Skills
```

- 三模式的分发逻辑清晰：Mode 1 走"指标→层级→价格点"完整链路，Mode 2 走审计（计分卡/对标/差距/快赢），Mode 3 走提价（策略选择/量化/沟通/90 天计划）。这与 SCORING 的 SCOPE-01（识别模式）要求兼容。
- **主要缺口：无编号化分步工作流**。正文对"做什么"描述充分（每个专题都有方法、表格、检查清单），但"先做 A 再做 B"的执行顺序约束只有一处显式声明——The Three Axes 节的"Define the metric first, then packaging, then test the number"（第 64 行）。Mode 1 的开场白（"We'll work on value metric selection, tier structure, price point research and pricing page design"）隐含了顺序，但未结构化。对 pattern: process 的 skill（160 个 process 型 skill 的中位数检查项 18-20），无编号流程意味着 PROC-01（价值指标先行）这类顺序约束只能靠章节自然顺序维持，agent 存在"先报价格再补指标"的跳序风险。对比同目录 296-pricing-strategy-architect 的 STEP 0-11 显式流程，本技能在流程可执行性上偏弱。
- 次级缺口：**无"模式选择门"**。SCOPE-01 要求 agent 开场识别模式（design/optimize/increase/page/research 五类），但正文从未指示 agent"先与用户确认属于哪种模式"。agent 只能从用户请求措辞自行推断。

### 3.2 Output Format 部分

- 有 Output Artifacts 表（六行：design/audit/increase/page/research/model 各对应交付物清单），如 "Design pricing" → "Three-tier structure with value metric, feature grid, price points and rationale"；"Audit my pricing" → "Pricing scorecard (0-100), conversion rate benchmarks, gap analysis, quick wins"。要素级输出定义清楚，与 OUT-01/OUT-03 的判定锚点直接对应。
- 有 Communication 标准（结论先行、What+Why+How、行动带 owner+deadline、🟢🟡🔴 置信度标记）——这是 OUT-02 的直接落点，且与本项目 trigger/沟通设计研究（confidence marking 约定）一致。
- **缺口：无具体输出模板**。相比 296 的 STEP 11 文档模板（含章节结构、元信息、文件命名），本技能只有"交付物要素清单"，没有"定价方案长什么样"的骨架示例。对纯对话交付可接受，但对"可复现输出格式"的测评友好度偏弱。

### 3.3 Scope/Limitations 部分

**缺失**。这是本技能最明确的结构缺口，且与档案快速审查（skill-dossier 2026-08-05 记 261 为 🟢"三节齐备"）判断不一致——本次全文审计确认：正文没有显式 Scope/Limitations 段落。仅有的隐含边界：

- description 将适用范围限为 SaaS；
- 提价策略表的 "Use When" 列（如 Uniform increase 用于"price clearly below market"）；
- "NOT free. Free is a separate strategy (freemium), not a tier"；
- Proactive Triggers 中 churn>5% 时"Before raising prices, fix churn"。

未声明的内容包括：非 SaaS 产品（实体产品、一次性服务、佣金制）如何适配；用户完全没有定价/转化数据时如何降级（所有提问都以"若已知"为前缀）；Van Westendorp 要求 n≥30 但用户通常拿不到样本时的处理；B2B 与 B2C 的定价差异；合规/法律限制（如价格歧视、涨价通知法定义务——虽有 grandfathered 条款，未提法律面）。建议在第 310 行后补一节 Scope & Limitations。

### 3.4 行数限制

SKILL.md 310 行，低于 600 行上限。合规（且留有余量，修复建议 R3/R5 若采纳仍有空间）。

### 3.5 跨技能文件路径

Related Skills 一节全部使用技能名（product-strategist、copywriting、churn-prevention、ab-test-setup、customer-success-manager、competitor-alternatives），无反引号文件路径、无 `../` 相对路径。每个条目还带一句"什么时候用它 / 什么时候不因该路由到它"的边界说明（如 "product-strategist: ... NOT for pricing page or price increase execution"），交叉路由质量高。合规。

---

## 4. 逻辑一致性

### 4.1 三轴顺序与 PROC-01 的一致性

"Most teams jump straight to the price point. That's backwards. Define the metric first, then packaging, then test the number."（第 64 行）与 PROC-01 的问题锚点（value metric 先行 → packaging → price point）完全一致。✓

### 4.2 模式枚举不一致（minor）

SCORING SCOPE-01 的判定问题枚举**五类模式**："design from scratch, optimize existing, plan a price increase, design a pricing page, or research"。而 SKILL.md 只定义 Mode 1-3，定价页设计（Pricing Page Design）与定价调研（Pricing Research Methods）是**独立章节而非模式**。语义上 agent 仍能识别全部五类（章节标题明确），判定可达，但"模式"一词的定义在两层不一致，建议二选一：把五个场景统一为 Mode 1-5，或改 SCOPE-01 措辞为"三种模式或两个专题场景"。

### 4.3 悬空引用 1：references/pricing-page-playbook.md（🔴 级问题）

SKILL.md 第 263 行：

> See references/pricing-page-playbook.md for design specifications and copy templates.

- 该行是 Pricing Page Design 章节的**收尾承接句**——章节前半部分只给了要素清单（Above the Fold 必须有计划名/账单切换/3-5 条 bullets/CTA/徽章；Below the Fold 要有对比表/FAQ/社会证明），承诺"设计规格与文案模板"在 playbook 里。
- 文件不存在。后果：a) PROC-05（定价页规格测评点）的深度内容无从产生，agent 只能靠通用常识补全；b) agent 若尝试 Read 该文件会得到错误，SKILL.md 里出现一条永远失败的指令路径。
- 修复选项：补建该文件（把要素清单展开为规格 + 文案模板），或把承诺的内容直接内联进正文（当前 310 行，有余量）。推荐补建——拆 reference 是评测集主流形态，且与 296 的 21 文件结构对齐。

### 4.4 悬空引用 2：scripts/pricing_modeler.py（🔴 级问题，联动测评）

SKILL.md 第 289 行 Output Artifacts 表末行：

> "Model pricing scenarios" | Run `scripts/pricing_modeler.py` with your inputs

- 文件不存在。后果链：
  1. agent 按指令运行 → `python scripts/pricing_modeler.py` 报"文件不存在" → 指令失败；
  2. agent 不运行 → SCORING QA-02（唯一脚本判定项，`tool_log_contains('scripts/pricing_modeler\\.py')`）判 False → 17 项 criteria 中 1 项**必然不可达**；
  3. 两种行为之间没有正确解——这是一个"怎么执行都错"的指令。
- 修复选项：方案 A——补写该脚本（一个 50-100 行的 MRR/ARPU/流失/提价情景计算器即可，评测时 agent 可真正调用）；方案 B——删除该行与 QA-02（把"建模"降级为 LLM 手工推算）。推荐 A：这是本技能唯一的脚本判定项，补上后测评体系多一个机械可验的维度。

### 4.5 SCOPE-02 的 marketing-context.md 位置歧义（minor）

"Before You Start" 说 "If marketing-context.md exists, read it before asking questions"。该文件既不在技能目录，也未说明应在工作区还是用户项目中查找——按"if exists"条件执行不算违规，但位置约定模糊（工作区查找 vs 技能目录查找行为不同）。建议一句注明"（检查当前工作区）"。

### 4.6 其余 17 项的一致性核验（全部通过）

逐项核对 SKILL.md 与 SCORING（详见第 10 节表格），除 QA-02 外全部有直接落点：

| 检查项 | 正文落点 | 一致性 |
|--------|---------|--------|
| SCOPE-03（先收集现状/业务/目标再提案） | Before You Start 第 1-3 组问题 | ✅ |
| SCOPE-04（非成本加成） | 引言 + Value-Based Pricing 全节 | ✅ |
| PROC-02（GBB：入口档付费且受限、中间档 2-3x 高亮、顶档企业功能） | Good-Better-Best 节逐条对应 | ✅ |
| PROC-03（10-20% 价值占比、不低于替代方案） | Value-Based Pricing Step 3 | ✅ |
| PROC-04（提价七要素：100/80/70% 留存量化、风险分层、60-90 天通知、理由、路径、CS 团队、60 天监控） | Price Increase Execution Checklist 1-7 条 | ✅ |
| PROC-05（定价页上下折叠要素） | Pricing Page Design 两小节 | ✅ |
| PROC-06（Van Westendorp n≥30 + MaxDiff） | Pricing Research Methods | ✅ |
| OUT-01（具体价格点/层级/价值指标/理由） | Output Artifacts + 各章节强制要素 | ✅ |
| OUT-02（沟通标准） | Communication 节 | ✅ |
| OUT-03（审计计分卡 0-100 + 对标 + 差距 + 快赢） | Output Artifacts "Audit my pricing" 行 | ✅ |
| NEG-01（不直接抄竞品价格、带定位分析） | "Don't just copy competitor prices" + 对标表 Step 5（premium 20-40% 上浮 / value 平价或更低） | ✅ |
| NEG-02（churn>5% 先修留存再提价） | Proactive Triggers 第 4 条 | ✅ |
| QA-01（主动触发：>40% 转化、单档客户、两年未提价、单一价格选项） | Proactive Triggers 六条 | ✅ |

映射质量在 322 个 skill 中属第一梯队——这正是本技能内容层的最大优点。

### 4.7 启发式数字未标注信源（minor）

正文给出多个经验值：">40% trial to paid → likely underpriced"、"15-30% healthy"、"10-20% of documented value"、"20-30% price increase → 5-15% churn"。这些是行业通行启发式，但全部以断言句呈现，未标注"经验值/需按行业校准"。考虑到 Communication 节定义了 🟢🟡🔴 置信度标记，正文自身的经验值却一个都没标——自诩的沟通标准未自洽应用到内容本身。建议给启发式数字补 🟡/🔴 标记或一句"经验值"声明。

---

## 5. 配套文件分析（SCORING.yaml / check.py）

本技能无 references/ 与 scripts/ 目录，本节分析两个配套文件，并给出目录完整性结论。

### 5.1 SCORING.yaml（159 行）

- **计数**：17 项 criteria = scope 4 + process 6 + output 3 + negative 2 + qa 2；`total_items: 17` 与实际条目数一致 ✅。3 项 critical_failures，`pattern: process`。
- **判定方式**：16 项 LLM + 1 项脚本（QA-02）。脚本化程度低（5.9%），对比同模式 008-tdd-workflow（14 script/20）、260 模板（12 script/18），本技能几乎全 LLM 判定——与"咨询决策类技能语义判断为主"的定位匹配，LLM 项的 question/evidence 锚点也都写得可判定（是/否问题 + 指明检查位置）。
- **critical_failures 定义合理且与正文红线对应**：
  - CF-01（无价值指标/层级、只有一个任意价格数 → cap 0）：对应正文"价值指标先行"的强制性与 Output Artifacts 的 tier 交付物；
  - CF-02（提价无量化/无沟通计划/不考虑留存 → cap 0）：对应 Execution Checklist 第 1/4/7 条；
  - CF-03（纯成本加成定价 → cap 0）：对应引言 "Pricing is not math" 与 Value-Based Pricing 全节。
- 唯一结构性缺陷：QA-02 的判定对象（scripts/pricing_modeler.py）不存在（见 4.4）。

### 5.2 check.py（64 行）

- 结构清晰：从 `../_shared/checker` 导入 `tool_log_contains`，check() 只执行 QA-02 一项，其余 16 项注释标明 "llm judge (not checked here)"。
- 正则 `'scripts/pricing_modeler\\.py'` 在 Python 中为 `scripts/pricing_modeler\.py`，与 SCORING.yaml 单引号串一致，转义正确 ✅。
- 问题 a（联动）：判定的行为对象是"调用不存在的脚本"——见 4.4，当前状态下该检查恒 False。
- 问题 b（潜在）：main() 中先 `set_agent_output(f.read())`（读入内容），随后调用的 check() 内部又 `set_agent_output(agent_output)`（把**路径字符串**覆写为 agent_output 值）——即 check() 执行后全局 agent_output 实际是文件路径而非内容。本技能未使用任何 output_* 检查，故无实际影响；但若未来新增输出检查项，会全部误判，建议顺手修正（两处调用二选一）。
- 文档字符串 "Run all 1 script checks" 与实际一致 ✅。

### 5.3 目录完整性

SKILL.md 共 2 处路径引用（references/pricing-page-playbook.md、scripts/pricing_modeler.py），**全部悬空**；目录无隐藏子目录、无多余残留文件。修复 R1/R2 后目录即自洽。

---

## 6. 语法格式

### 6.1 Markdown 围栏配对

全文 2 处 ``` 标记（Value-Based Pricing 的价格定位示意图，第 142-144 行），配对正常，无孤悬围栏。✅

### 6.2 标点与符号

- 全英文内容，ASCII 标点规范，无中英混排、无全角误用。
- emoji 使用克制且均为功能性：What Goes in Each Tier 表的 ✅/—（功能分配矩阵）、Output Artifacts/沟通标准的 🟢🟡🔴（置信度标记）。无装饰性 emoji，人机感干净（对比 072-mobile-design 的 20+ emoji 问题，本技能为零）。
- 表格内使用 "—" 表示"不提供"，风格统一。

### 6.3 标题层级

`# Pricing Strategy`（一级）+ ## 专题 + ### 小节，无跳级。"### PACKAGING / VALUE METRIC / PRICE POINT" 三轴小节用全大写样式作刻意强调，三处风格一致，可接受。

### 6.4 编号与排序

- Mode 1-3 编号连续；无步骤编号体系（与"缺编号工作流"的发现 3.1 呼应）。
- 五张表格（价值指标、层级内容、对标步骤、提价策略、输出物）行列对齐良好，无断裂行。

### 6.5 代码块与内联代码

- 文件路径与脚本名使用反引号（`references/pricing-page-playbook.md`、`scripts/pricing_modeler.py`），格式统一（内容悬空问题见 4.3/4.4）。
- 全文未发现拼写错误或断句问题；"That's backwards." 等轻口语化表达属风格选择。

---

## 7. 规范合规（12 项核查）

| # | 规范要求 | 结果 | 说明 |
|---|---------|------|------|
| 1 | description 第三人称 WHAT+WHEN+KEYWORDS | ✅ | 293 字符；WHAT 能力短语 + WHEN 显式 + 关键词齐备（WHAT 以动词短语开头，风格性偏差非阻断） |
| 2 | description ≤ 1024 字符 | ✅ | 实测 293 字符 |
| 3 | description 含触发信号（trigger signal） | ✅ | "Use when the user wants to create or revise pricing, design pricing tiers, choose value metrics, optimize pricing page UX, or plan price increase communications" |
| 4 | 可选字段仅限白名单 | ✅ | 未使用任何可选字段 |
| 5 | 无禁用/自造字段 | ✅ | frontmatter 仅 name + description |
| 6 | Body 含 Workflow/Process | ⚠️ | 三模式框架 + 专题方法齐全，但无编号分步流程、无模式选择门 |
| 7 | Body 含 Output Format | ⚠️ | Output Artifacts 表 + Communication 标准存在，无具体输出模板 |
| 8 | Body 含 Scope/Limitations | ❌ | 缺失（见 3.3） |
| 9 | Body ≤ 600 行 | ✅ | 310 行 |
| 10 | 无跨技能文件路径 | ✅ | Related Skills 仅技能名引用 |
| 11 | SKILL.md 内容与 SCORING 检查项一致 | ✅ | 17 项全部有落点（QA-02 落点悬空，见第 12 项） |
| 12 | 参考文件路径指向存在 | ❌ | references/pricing-page-playbook.md 与 scripts/pricing_modeler.py 均不存在 |

合规判定：12 项中 9 项完全合规，2 项有条件合规（第 6、7 项为"有但弱"），1 项缺失（Scope/Limitations），1 项违规（第 12 项悬空路径，且联动第 11 项的 QA-02）。总体约 75% 强合规——与"内容优质但交付链路有两处断点"的总体评价一致。

---

## 8. 人机感（8.1–8.6）

### 8.1 开场与价值主张

"Pricing is not math — it's positioning." + "Most SaaS products are underpriced. This skill is about fixing that, clearly and defensibly."——金句式开场直接建立咨询权威感，明确技能的价值主张与立场（"多数产品被低估"），用户一上来就知道这个技能"站在哪边"。这是本技能人机感的最佳部分，顾问口吻专业且不浮夸。

### 8.2 上下文自适应

Before You Start 要求先检查 marketing-context.md 再提问，"Use that context and ask only about what's missing"——尊重用户已有分析、避免重复提问，与 296 的 STEP 1 上下文检测设计同思路（296 因文件缺失执行失败，本技能的"if exists"条件写法反而更稳健）。唯一歧义是文件位置未注明（见 4.5）。

### 8.3 提问节奏与降级路径

三组前置问题（Current State / Business Context / Goals）结构化，每题都带示例值（ARPU、churn rate、grandfathered、partner margin），用户回答成本低。**缺口**：没有"不知道/没数据怎么填"的降级路径——例如用户答不出转化率时，技能未提供估算公式或"改为敏感性区间"的备选方案（296 的 CS3 就带估算公式，对比明显）。建议在问题组后补一句降级指引。

### 8.4 主动触发机制

Proactive Triggers 六条——>40% 试用转化提示提价、全员中间档提示缺企业档、用户请求档外功能提示 feature gating 漏收、churn>5% 先修留存、两年未提价提示通胀调价、单一价格选项提示加锚定档。这是本技能最具亮点的设计：**"不用用户问也会说"的机制**与本项目 trigger 设计研究（skillif-trigger-design）的结论一致，且六条全部直接转化为 SCORING 的 QA-01 判定锚点。加分项。

### 8.5 沟通协议

Communication 节把交付沟通协议化：结论先行、What+Why+How 三要素、行动必须有 owner 和 deadline（"no consider"）、🟢🟡🔴 置信度标记。这套协议既提升交付质量，又让 OUT-02 的 LLM 判定有明确检查对象——技能设计与测评设计的双向对齐，评测友好度高。唯一瑕疵是正文自身的经验值数字未应用该协议（见 4.7）。

### 8.6 语气与语言

专业顾问口吻，无 emoji 滥用、无喊叫式大写、无营销浮夸。示例（Salesforce/Notion/Linear/Stripe/Twilio/OpenAI）贴近 SaaS 受众，易引发共鸣。整体人机感评分高。

---

## 9. 可执行性（9.1–9.4）

### 9.1 主流程可执行性

高（对领域专家型 agent）。模式识别 → 上下文收集 → 专题方法（指标表/GBB 表/价值定价三步/对标五步/提价清单/页面要素）全部是"填充式"指导，无歧义弱指令。**注意**：无编号流程意味着顺序约束弱，PROC-01 依赖单句声明维持——在显式注入（Mode A）场景下 agent 大概率按章节顺序执行，问题不大；在自然激活（Mode B）场景下风险上升。建议 R4 补流程骨架。

### 9.2 定价页深度不可执行

Pricing Page Design 承诺的设计规格与文案模板全部委托给不存在的 playbook。PROC-05 的 LLM 判定锚点只检查要素（账单切换、bullets、CTA、徽章、FAQ、对比表、社会证明），agent 用通用常识可满足，**LLM 判定勉强可达**；但技能承诺的深度交付物（copy templates）不可达。属"浅层可达、深层断供"。

### 9.3 QA-02 不可执行（测评确定性损失）

QA-02 是唯一脚本判定项，其判定对象不存在。评测结果中该项恒 False，该技能的可机械验证维度为 0——即便 agent 完美遵从其余 16 项，17/17 的满分在本文件状态下不可达。这是本次审计发现的最具操作意义的缺陷（修复见 R1）。

### 9.4 其余判定可达性

15 项 LLM 判定 + 3 项 CF 全部可达（第 10 节表）。修复 R1/R2 后，本技能 17/17 可达，成为"全链路可测评"技能。

---

## 10. SCORING 交叉参考

逐项映射 17 项 criteria 与 3 项 critical_failures 到 SKILL.md，并评估可达性：

| ID | 类别 | 判定方式 | 指令落点 | 可达性 |
|----|------|---------|---------|--------|
| SCOPE-01 | scope | LLM | description + Mode 1-3 + Pricing Page/Research 章节 | ✅ 可达（五模式枚举与三模式定义不一致，不影响判定，见 4.2） |
| SCOPE-02 | scope | LLM | Before You Start（marketing-context.md 条件读取） | ✅ 条件可达（文件存在时） |
| SCOPE-03 | scope | LLM | Before You Start 第 1-3 组问题 | ✅ 可达 |
| SCOPE-04 | scope | LLM | 引言 + Value-Based Pricing 全节 | ✅ 可达 |
| PROC-01 | process | LLM | The Three Axes（metric → packaging → price） | ✅ 可达（顺序约束仅一处声明，Mode B 下风险，见 9.1） |
| PROC-02 | process | LLM | Good-Better-Best 节（入口档付费受限/2-3x 高亮/企业功能） | ✅ 可达 |
| PROC-03 | process | LLM | Value-Based Pricing Step 1-3（替代方案/价值估算/10-20%） | ✅ 可达 |
| PROC-04 | process | LLM | Execution Checklist 七条（100/80/70% 量化/分层/60-90 天/理由/路径/CS/60 天监控） | ✅ 可达 |
| PROC-05 | process | LLM | Pricing Page Design（上下折叠要素） | ✅ 可达（深度规格断供，见 9.2） |
| PROC-06 | process | LLM | Pricing Research Methods（VW n≥30 + MaxDiff） | ✅ 可达 |
| OUT-01 | output | LLM | Output Artifacts + 各专题强制要素 | ✅ 可达 |
| OUT-02 | output | LLM | Communication 节 | ✅ 可达 |
| OUT-03 | output | LLM | Output Artifacts "Audit" 行（scorecard 0-100/对标/差距/快赢） | ✅ 可达（非审计任务时按问题自答 yes） |
| NEG-01 | negative | LLM | "Don't just copy competitor prices" + 对标表 Step 5 | ✅ 可达 |
| NEG-02 | negative | LLM | Proactive Triggers 第 4 条（churn>5% 先修留存） | ✅ 可达 |
| QA-01 | qa | LLM | Proactive Triggers 六条 | ✅ 可达 |
| QA-02 | qa | **脚本** | Output Artifacts 表（scripts/pricing_modeler.py） | 🔴 文件缺失，恒 False |
| CF-01 | critical | LLM | — | ✅ 定义合理（无价值指标/层级即 0 分），与正文强制要素对应 |
| CF-02 | critical | LLM | — | ✅ 定义合理（提价无量化/无沟通/无留存考虑即 0 分），与 Checklist 对应 |
| CF-03 | critical | LLM | — | ✅ 定义合理（纯成本加成即 0 分），与引言/价值定价节对应 |

统计：可达 16 项、不可达 1 项（QA-02）。修复 R1 后全部 17 项可达。当前状态下脚本判定维度为 0，LLM 维度 16/16 可达——本技能的实测分数会系统性偏低 1/17，且这个损失与 agent 行为无关，纯属评测资产缺陷。

---

## 11. 已知问题（skip）

按审计规则本节跳过。相关问题已并入第 3、4、9 节的缺陷分析与第 13 节的修复建议中。

---

## 12. 综合评分

8 个维度各满分 12.5 分，合计 /100：

| 维度 | 得分 | 依据 |
|------|------|------|
| ① 描述与 Frontmatter | 11.5/12.5 | 293 字符、WHAT+WHEN+KEYWORDS 齐备、触发覆盖面与五场景对齐；唯一保留：WHAT 以动词短语开头的人称风格 |
| ② Body 结构 | 8.5/12.5 | 三模式 + 九专题内容完整、表格式指导可执行；无编号工作流、无模式选择门、Output 无模板、Scope 缺失 |
| ③ 逻辑一致性 | 10.0/12.5 | 17 项检查点与正文映射精准（第一梯队）；扣分：两处悬空引用、模式枚举不一致、marketing-context 位置歧义 |
| ④ 配套文件 | 6.5/12.5 | SCORING 结构与 CF 定义优秀；无 references/scripts 资产，且两个被引用的文件全部缺失，QA-02 恒挂 |
| ⑤ 语法格式 | 11.5/12.5 | 围栏配对、表格、emoji 功能性使用、无拼写错误；全大写轴标题为风格选择 |
| ⑥ 规范合规 | 9.5/12.5 | 12 项核查 9 项通过；Scope 缺失、悬空路径违规、Workflow/Output 为弱通过 |
| ⑦ 人机感 | 11.5/12.5 | 金句式开场、上下文自适应、主动触发机制、沟通协议为亮点；缺"无数据降级路径" |
| ⑧ 可执行性 | 8.5/12.5 | 主流程与 16 项判定可达；QA-02 恒 False、定价页深度断供、无编号流程弱化顺序约束 |

**总分：77.5 → 78 / 100（B-，🟡）**

评级解读：本技能处于 🟡 上游（对比 296 的 74 分、C+ 档：本技能无"输出格式三方冲突"级别的阻断矛盾，主体内容与测评映射质量明显更高）。档案快速审查（skill-dossier 2026-08-05）将其列为 🟢"三节齐备"——本次全文审计确认 Output Format/Scope 实际为"部分满足/缺失"，并新发现悬空引用问题（快速审查未覆盖引用存在性），故调整评级为 🟡。完成第 13 节 R1-R4 修复后，本技能有充分理由进入 🟢 级（45% 档以上）：其内容密度、SCORING 映射完整性与人机设计在同类型咨询技能中名列前茅。

---

## 13. 修复建议

按优先级（🔴 阻断 / 🟡 重要 / 🟢 建议）列出，均标注文件与行号与工作量（S=≤0.5 天，M=1-2 天）。

### 🔴 阻断级

**R1（🔴）补建 scripts/pricing_modeler.py，或删除建模功能引用并改造 QA-02**
- 位置：SKILL.md:289（Output Artifacts 表末行）；连带 SCORING.yaml:140-145（QA-02）、check.py:39。
- 内容：方案 A——补写 `scripts/pricing_modeler.py`（建议 50-100 行：输入 MRR、ARPU、流失率、计划涨幅与留存情景 100%/80%/70%，输出新 MRR 与净收入影响矩阵），SKILL.md 补一句调用示例；方案 B——若确认不做脚本化建模，删除 SKILL.md:289 该行、SCORING QA-02 与 check.py:39，将"建模定价场景"改为 LLM 手工推算（同时 SCORING 的 total_items 改为 16）。**推荐 A**：这是本技能唯一脚本判定项，补建后评测恢复机械验证维度。
- 工作量：S（方案 B）/ S-M（方案 A）。

**R2（🔴）补建 references/pricing-page-playbook.md，或内联定价页设计规格**
- 位置：SKILL.md:263（"See references/pricing-page-playbook.md..."）。
- 内容：方案 A——新建该文件：Above the Fold 布局规格（宽度/层级/切换交互）、Below the Fold 结构、5 条 FAQ 文案模板、CTA 文案变体、社会证明摆放规则；方案 B——把上述内容直接写进 SKILL.md Pricing Page Design 节（310 行 + 约 40 行仍在 600 上限内）。**推荐 A**：保持正文精简，且与 R1 一起让全部引用落地。
- 工作量：M（方案 A）/ S（方案 B）。

### 🟡 重要级

**R3（🟡）新增 Scope & Limitations 段**
- 位置：SKILL.md 末尾（第 310 行后，Related Skills 之前或之后）。
- 内容：声明适用边界——本技能面向 SaaS 定价（实体产品/服务行业需自行调整口径）；用户无定价数据时的降级路径（敏感性区间估算替代精确值）；Van Westendorp n≥30 不可满足时的替代（专家估计 + 注明置信度）；B2B/B2C 差异；不提供法律/合规意见（涨价通知义务等）。
- 工作量：S。

**R4（🟡）把 Mode 1-3 结构化为编号工作流并加模式选择门**
- 位置：SKILL.md:35-44（How This Skill Works 节）。
- 内容：为每个 Mode 给出 4-6 步编号流程（如 Mode 1：识别模式 → 收集上下文 → 定义价值指标 → 设计层级 → 定价研究 → 定价格点 → 出页面方案 → 交付），并加一句开场指令："开始时先向用户确认属于 Mode 1/2/3、定价页设计还是定价调研"。直接支撑 SCOPE-01 与 PROC-01 的判定。
- 工作量：S。

**R5（🟡）补一个输出模板骨架**
- 位置：SKILL.md Output Artifacts 表后。
- 内容：给"Design pricing"交付物一个 15-20 行的输出骨架（结论先行 → 价值指标与理由 → GBB 三层表 → 价格点与依据 → 定价页要点 → 置信度标注），让 OUT-01/02 的判定有可循格式。
- 工作量：S。

**R6（🟡）统一模式枚举口径**
- 位置：SCORING.yaml:8-13（SCOPE-01 的问题措辞）或 SKILL.md Mode 定义。
- 内容：二选一——SKILL.md 把定价页与调研并入 Mode 4/5，或 SCOPE-01 改问"识别三种模式或两个专题场景（定价页/调研）"。消除"五模式 vs 三模式"的定义错位。
- 工作量：S。

**R7（🟡）正文经验值标注置信度**
- 位置：SKILL.md:162-165（转化率信号）、228（提价流失 5-15%）、198（定位带 20-40%）。
- 内容：按 Communication 节自定的 🟡 协议给启发式数字补标注（如 ">40% trial to paid → likely underpriced（🟡 经验值）"），让沟通标准应用到内容自身。
- 工作量：S。

### 🟢 建议级

**R8（🟢）修正 check.py 的 set_agent_output 双重调用**
- 位置：check.py:20（check() 内）与 check.py:52-54（main() 内）。
- 内容：删除 check() 内的 `set_agent_output(agent_output)`（main 已读文件内容），避免未来新增 output_* 检查时全部误判。
- 工作量：S。

**R9（🟢）注明 marketing-context.md 的查找位置**
- 位置：SKILL.md:15。
- 内容：补"（在用户当前工作区查找）"一句，消除 SCOPE-02 执行歧义。
- 工作量：S。

**R10（🟢）给问题组补"无数据降级路径"**
- 位置：SKILL.md:17-33（Before You Start）。
- 内容：每类数据（转化率、ARPU、churn）补一句"若未知，给出估算并标 🟡，或改为敏感性区间"。
- 工作量：S。

修复顺序建议：R1 → R2（解锁测评与深度交付）→ R3/R4（结构合规）→ R5-R7（一致性打磨）→ R8-R10（收尾）。R1+R2 完成后，第 10 节中 QA-02 由不可达转可达，脚本判定维度从 0 恢复为 1，预计评分提升 3-5 分并消除"17/17 不可达"的测评资产缺陷；R3/R4 落地后结构性合规可达 11/12 项。

---

## 附录

### 附录 A：脚本核验记录

| 核验项 | 结果 |
|--------|------|
| description 字符数 | 293（上限 1024）✅ |
| SKILL.md 行数 | 310（上限 600）✅ |
| SKILL.md 代码围栏 | 2 处，配对正常 ✅ |
| references/pricing-page-playbook.md | 不存在 ❌ |
| scripts/pricing_modeler.py | 不存在 ❌ |
| references/、scripts/ 目录 | 均不存在 ❌ |
| 目录文件数 | 3（SKILL.md、SCORING.yaml、check.py），全部通读 ✅ |

### 附录 B：SCORING 数量核对

criteria 计数：SCOPE 4 + PROC 6 + OUT 3 + NEG 2 + QA 2 = 17，与 SCORING.yaml `total_items: 17` 一致；critical_failures 3 项；脚本判定 1 项（QA-02），LLM 判定 16 项，与 check.py 注释 "Run all 1 script checks" 一致。pattern: process 与 322 个 skill 的 pattern 分布（process 160 个占 49.7%）一致。

### 附录 C：评价总览

本技能是把 SaaS 定价方法论（价值定价、Good-Better-Best、Van Westendorp、提价工程）压缩为"三模式 + 九专题 + 六触发"的问答式咨询技能，内容密度高、SKILL.md 与 SCORING 的映射在 322 个技能中属第一梯队，主动触发与置信度标注设计贴合本项目 trigger 研究结论。当前两大障碍均为"资产缺失"型而非"内容错误"型：定价页 playbook 与建模脚本两个被引用文件不存在，使深度交付断供、唯一脚本判定项必挂。修复 R1-R4 后，本技能有充分理由进入 🟢 级。
