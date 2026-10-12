# REVIEW — 087-copy（SaaS/Startup Copywriter Skill）

| 元信息 | 值 |
|--------|----|
| 审查日期 | 2026-08-06 |
| 审查对象 | `D:\SkillIF\skill-experiment\complex-skills\087-copy\` 全目录 |
| 审查依据 | `_shared\SKILL-SPEC.md` v1.0、`_shared\CHECKER-LIBRARY.md`、skill-dossier（2026-08-05）087 条目 |
| 审查方法 | 5 维度（逻辑一致性、语法可读性、人机感、规范合规性、整体评价）+ 实验适配性（SCORING/check.py/测评风险）深审 |
| 文件状态 | 6 个文件全部存在且可读，引用关系闭合，无缺失引用 |

---

## §1 审查概述

087-copy 是 SkillIF complex-skills 语料库中编号 087 的文案写作技能，`pattern: mindset`。技能定位为「面向 SaaS 与初创公司的专业文案（copywriter）」，覆盖落地页文案、定位（positioning）、信息传达（messaging）、转化率优化（conversion optimization）与客户之声研究（voice-of-customer, VOC）。

本次审查的目标有三层：

1. **规范层**：对照 SKILL-SPEC.md v1.0 逐条核验 frontmatter、description、正文结构、目录命名与引用路径；
2. **内容层**：检验 SKILL.md 与三个 reference 文件之间的逻辑一致性、知识冗余度（knowledge delta）、事实准确性；
3. **实验层**：站在 SkillIF 2 Mode × 5 Harness 测评矩阵的角度，审查 SCORING.yaml 19 项 LLM judge 标准的可判定性、check.py 空实现的影响、以及该技能在测评运行中可能诱发的 agent 行为偏差。

总评先行：**内容质量高、人机感好、description 合规**，但存在三处结构性缺口（无显式 Output Format 节、无显式 Scope/Limitations 节、body 超 mindset 目标体量 8 倍）与三处跨文件不一致（3 秒/5 秒测试、标题公式措辞、假设格式字段），综合评级建议由 dossier 的 🟢 下调至 🟡。

---

## §2 文件清单与规模统计

| 文件 | 行数 | 作用 | 状态 |
|------|:----:|------|------|
| `SKILL.md` | 396（正文 ≈ 391） | 技能主体：理念、框架、工作流、原则 | 存在 |
| `SCORING.yaml` | 175 | 19 项评分标准（全部 `judge: llm`）+ 3 项 critical failures | 存在 |
| `check.py` | 81 | 脚本检查桩：返回空 dict（0 项脚本可验证） | 存在 |
| `references/frameworks-and-methodology.md` | 464 | 框架与方法论（Hormozi、标题策略、offer 设计等） | 存在 |
| `references/landing-page-workflow.md` | 551 | 落地页 10 阶段工作流（策略→VOC→架构→测试→优化） | 存在 |
| `references/tools-and-resources.md` | 344 | 工具栈、书单、清单、速查公式 | 存在 |
| **合计** | **2011** | | |

规模观察：

- SKILL.md 正文 391 行，远超 `pattern: mindset` 的目标体量（SKILL-SPEC §3.2 表格：mindset ~50 行），甚至超过 `process`（~200 行）与接近 `tool`（~300 行）目标。虽在 600 行硬上限内，但超出本 pattern 目标约 8 倍。
- 三个 reference 合计 1359 行，是 SKILL.md 的 3.4 倍——该技能是「正文自包含 + 引用冗余」型，与「正文薄、内容在 references」的 045/269/317 型恰好相反。
- 全部引用文件存在，无悬空链接（§8 进一步核验了锚点）。

---

## §3 规范合规性审查（SKILL-SPEC v1.0）

### 3.1 Frontmatter

- `name: copy` — 小写 + 连字符，≤64 字符，与目录名 `087-copy`（NNN- + name）一致。通过。
- `description`（L3，约 320 字符 ≤1024）— 仅含 `name`、`description` 两个字段，无任何禁止字段（§1.3 清单）。通过。
- 无 `allowed-tools`、无空值字段。通过。

### 3.2 Description 规范

逐条对照 §2.1–§2.6：

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 第三人称 | 通过 | 无第一/第二人称、无祈使句开头 |
| WHAT（做什么） | 通过 | "Professional copywriter for SaaS and startups" 明确、具体 |
| WHEN（何时用） | 通过 | "Use when writing compelling copy for SaaS products, landing pages, marketing materials..." |
| KEYWORDS | 通过 | landing page copy / positioning / messaging / conversion optimization / voice-of-customer |
| 触发信号短语 | 通过 | "Use when..."（规范模板逐字命中） |
| 无跨技能路由 | 通过 | description 中无 "NOT for X, use Y" |
| 长度 ≥40 字符 | 通过 | 约 320 字符 |

唯一值得商榷处：`marketing materials` 一词范围较宽（可涵盖广告文案、邮件、社媒文案），而技能内容以落地页为中心，且 SCOPE-01 标准要求 agent 区分「非广告平台文案」。description 与标准之间存在一个未闭合的边界（详见 §6、§10）。

### 3.3 正文三必需节（§3.1）

SKILL-SPEC 要求 body 必须包含 Workflow/Process、Output Format、Scope/Limitations 三节（标题不限）。

| 必需节 | 判定 | 最接近的节 | 评注 |
|--------|:----:|-----------|------|
| Workflow/Process | 通过 | `## Essential Workflows`（L146）+ `## When Helping Users → Your Process`（L371） | VOC 研究、假设测试、落地页结构、6 步个人流程俱全，步骤清晰可执行 |
| Output Format | **缺失** | `## Quick Reference`（L384，速查表） | 速查表是「任务→要点→引用」索引，不是输出规格；正文从未定义交付物形态（message bank 格式？headline 选项列表？最终文案结构？）。唯一算输出描述的是 VOC 一节的 message bank 表（L176-180），但那是过程工具而非交付物定义 |
| Scope/Limitations | **缺失** | `## Quick Decision Framework`（L38，何时用哪种文案切入） | 该节回答「市场awareness不同时用哪种方法」，不是技能边界；`## Key Principles → Avoid`（L301）是文案内容禁区，也不是技能边界。全文无「本技能不做什么/何时不应使用」声明 |

**结论**：dossier 判定「三节齐全」偏宽松。若按 §3.1「MUST include」字面执行，Output Format 与 Scope/Limitations 两节实质缺失。这是本技能最明确的规范缺口（语料库最常见的共性问题，见 dossier 汇总「缺 Scope 节 ~220 个」「缺 Output Format 节 ~180 个」）。

### 3.4 体量与知识增量（§3.2、§3.4）

- 391 行 vs mindset 目标 ~50 行：超出但未触 600 行硬上限。
- §3.4「Knowledge delta over redundancy」违反明显：SKILL.md 与 frameworks-and-methodology.md 存在大段逐字/近逐字重复（详见 §5 冗余清单），如 Slippery Slide 十步列表、Pain Is the Pitch 示例、Hormozi 公式块、Hero 公式及示例。
- 正面的「Concrete over abstract」执行出色：全文几乎每条规则都配 Not/Yes 或 Bad/Good 对比示例（L128-142、L291-305）。

### 3.5 引用与路径（§3.3）

- 全部引用为技能内相对路径：`references/frameworks-and-methodology.md`、`references/landing-page-workflow.md`、`references/tools-and-resources.md`。通过。
- 无跨技能引用（无 `../`）。通过。
- 锚点核验：`#headline-formula-selection`（L388）、`#phase-2-voice-of-customer-research-voc`（L389）、`#headline-strategy`（L69）、`#phase-7-form-a-hypothesis-backlog`（L216）、`#cta-optimization-quick-guide`、`#hypothesis-testing-process`、`#social-proof` 等全部与目标文件实际标题 slug 一致。通过。

### 3.6 目录命名（§4）

`087-copy`：NNN-kebab-case，无空格、无大写，与 name 一致。通过。

### 3.7 合规检查清单汇总

| # | 检查项 | 结果 |
|---|--------|:----:|
| 1 | name 小写+连字符 ≤64，匹配目录 | 通过 |
| 2 | description 第三人称 + WHAT/WHEN/KEYWORDS ≤1024 | 通过 |
| 3 | description 无祈使/第一/第二人称开头 | 通过 |
| 4 | description 无跨技能路由 | 通过 |
| 5 | 至少一个触发信号短语 | 通过 |
| 6 | frontmatter 无禁止键 | 通过 |
| 7 | body ≤600 行 | 通过（391） |
| 8 | workflow/process 节 | 通过 |
| 9 | output format 节 | **不通过** |
| 10 | scope/limitations 节 | **不通过** |
| 11 | 无跨技能文件引用 | 通过 |
| 12 | 目录 NNN-kebab-case | 通过 |

**合规小结：10/12 通过，2 项缺失。**

---

## §4 逻辑一致性审查

### 4.1 SKILL.md 内部一致性

技能内部的核心主张链完整闭环：定位先行（L12）→ VOC 提取（L13、L369）→ 消息层级（L125-142）→ 写作（L372-378）→ 假设测试（L184-216）→ 文档化学习（L378）。各框架之间互相印证：

- Hero 公式（L110-115）与 3-秒测试（L117-122）一致：两者都用「What is this / Who is it for / Why care now」三问；
- 消息层级（Outcome→Benefit→Feature）与 Key Principles「Benefits before features, outcomes before benefits」（L287）一致；
- Landing Page Structure 九段（L220-229）与 SCORING PROC-06 的九段序列逐字对应；
- CTA 原则（L71-83、L295-299）与 NEG-01 标准（禁 "Submit"/"Click here"/"Learn more"、禁 fake scarcity）一致；
- ICE 公式（L212）在 SKILL.md 与 landing-page-workflow（L311）中一致；
- 反对意见预处置表（L333-338）四条映射（贵→ROI、复杂→速度、不适合→保证、不着急→损失）与 frameworks 对应节（L309-325）一致。

**未发现正文内部矛盾。**

### 4.2 跨文件不一致（重点发现）

| # | 不一致点 | SKILL.md 表述 | references 表述 | 严重度 |
|---|---------|--------------|----------------|:----:|
| I1 | **测试时限与问题集** | 「3-Second Test」（L117-122）：What is this / Who is it for / **Why should I care now** | frameworks-and-methodology.md L380-388：「**5-Second Test**」：What is this / Who is it for / **What's the main benefit** | 中 |
| I2 | **标题公式措辞** | 「Get [Result] in [Time] **Without** [Pain]」（L64） | frameworks L82：「Get [Specific Result] in [Timeframe] **With Less** [Pain/Effort]」 | 低 |
| I3 | **假设格式字段数** | 5 字段：If/Then/Because/Measured by/Success criteria（L188-194） | landing-page-workflow L270-277：7 字段（另加 Risk、Effort） | 低 |
| I4 | **Message bank 列数** | 4 列 Theme/Quote/Source/Use In（L176-180） | landing-page-workflow L87-92：5 列（另加 Awareness Stage、Notes） | 低 |

其中 I1 最具实质影响：同一技能内存在「3 秒测试」（三问含 "Why should I care now"）与「5 秒测试」（三问含 "What's the main benefit"）两套定义，且二者问题集不同。LLM judge 在核验 PROC-05（hero 通过 3 秒测试）时面对双标准，agent 也可能在两条指令间摇摆。三个文件中，landing-page-workflow（L126-133）与 tools-and-resources（L193）均写 3 秒，frameworks 是唯一 5 秒源——应统一为 3 秒。

I2/I3/I4 为措辞级差异，不影响行为，但同一语料库内部标准文本不一致会削弱「文案作为规范」的说服力，建议顺手对齐。

### 4.3 事实/时效性核验

- Hormozi Value Equation（`Value = (Dream Outcome × Perceived Likelihood) ÷ (Time Delay × Effort & Sacrifice)`）：与《$100M Offers》公开表述一致。通过。
- Schwartz 五级 awareness（landing-page-workflow L14：Unaware→Problem-aware→Solution-aware→Product-aware→Most aware）：与《Breakthrough Advertising》一致。通过。
- 「Headlines do 80% of the conversion work」（frameworks L77）：**无来源的定量断言**，属于营销经验法则而非可核验事实；不构成错误，但作为「科学化」标榜的 skill 略有违和（§10 展开）。
- Google Optimize「Free (being deprecated)」（landing-page-workflow L322）：Google Optimize 已于 2023 年 9 月正式停服，措辞「正在弃用」已过时。低严重度，建议改为「已停用」并删除。
- 其余工具/书单条目（Dovetail、Grain、Clarity、Webflow、Framer 等）均为真实产品，价格可能变动但不构成逻辑错误。

---

## §5 内容冗余与知识增量分析

SKILL.md 与 references 之间存在系统性重复。逐项清点（SKILL.md → frameworks-and-methodology.md）：

| # | 内容块 | SKILL.md | frameworks | 冗余程度 |
|---|--------|:--------:|:----------:|:--------:|
| D1 | Hormozi 公式块 + 四象限展开 | L89-106 | L11-47 | 高（结构逐项对应） |
| D2 | Hero 公式 + 示例（"Turn 3-Hour Reports Into 5-Minute Dashboards"、"Trusted by 2,500+ SaaS companies"） | L110-115 | L170-178 | 逐字级 |
| D3 | Slippery Slide 十步列表 | L311-325 | L327-341 | 逐字级 |
| D4 | Pain Is the Pitch（"3 hours crafting the perfect email campaign, hit send, and get 2% open rates. Again."） | L340-346 | L66-71 | 逐字级 |
| D5 | 反对意见预处置四条映射 | L333-338 | L309-325 | 高（同四条、同示例） |
| D6 | 「mom 3 秒」规则 | L376 | L424 | 近逐字 |
| D7 | 「goldfish memory」 | L378 | L460 | 近逐字 |
| D8 | 消息层级（Outcome/Benefit/Feature） | L125-142 | L51-64（Sell the Outcome, Not the Features） | 高（概念相同、示例不同） |
| D9 | 落地页九段结构 | L220-229 | landing-page-workflow L101-111 | 高（近逐字） |
| D10 | CTA 优化要点 | L71-83 | landing-page-workflow L160-169 | 中 |
| D11 | 假设测试格式 + ICE 公式 | L184-216 | landing-page-workflow L263-313 | 中 |

**量化评估**：SKILL.md 391 行中，与 references 重复的内容约 150-180 行（D1-D11 合计），占比约 40-45%。若将 D2-D7 六块压缩为一行指针链接，可减约 120 行。

**结构后果**：

1. 违反 SKILL-SPEC §3.4「Knowledge delta over redundancy」——正文承担了 references 已完整覆盖的知识，references 沦为装饰性冗余而非知识延伸；
2. 变相制造了 I1-I3 的不一致风险（同一内容两处维护，必然漂移，3 秒/5 秒测试即为实证）；
3. 稀释了 mindset 型技能的「轻量触发、重判断」定位——agent 加载 391 行正文 + 1359 行 references 才能获得约 200 行的净知识。

**正面补充**：SKILL.md 也存在 references 未覆盖的独有内容：Discovery Questions 五问（L352-358）、Request from Users 四类材料清单（L361-368）、Quick Reference 索引表（L384-395）、When to Use Each Copy Approach 三分类（L42-58）。这些是保留价值最高的部分。

---

## §6 SCORING.yaml 质量审查

### 6.1 元数据与结构

- `skill: copy`、`pattern: mindset`、`total_items: 19` —— 与实际 criteria 计数（3+10+3+2+1=19）一致。通过。
- 19 项全部 `judge: llm`，无 `judge: script` 项；critical_failures 3 项（CF-01 无 VOC 基础写稿、CF-02 空话堆砌、CF-03 跳过定位），effect 均为 `cap_to_0`。与 corpus 惯例一致。

### 6.2 标准→技能内容可追溯性矩阵

| id | 类别 | 标准要点 | SKILL.md 依据 | 可判定性 |
|----|------|---------|--------------|:--------:|
| SCOPE-01 | scope | 识别为文案任务（非广告平台文案/代码） | description + 全篇 | 良（广告文案边界未在正文定义，见 6.3） |
| SCOPE-02 | scope | 先定位后写作 | L12、L373「Get strategy brief approved before writing」 | 优 |
| SCOPE-03 | scope | 要求/使用 VOC，不凭直觉 | L13、L369「Don't write without VOC research. Ever.」 | 优 |
| PROC-01 | process | 消息层级 Outcome→Benefit→Feature | L125-142 | 优 |
| PROC-02 | process | 标题匹配 awareness 层级并有理由 | L42-58 | 优 |
| PROC-03 | process | 应用标题公式 | L64-67 四公式 | 优 |
| PROC-04 | process | Hormozi 值等式框架 offer | L89-106 | 优 |
| PROC-05 | process | hero 过 3 秒测试 | L117-122 | 中（受 I1 双标准干扰） |
| PROC-06 | process | 九段落地页结构 | L220-229 | 优 |
| PROC-07 | process | 逐字使用客户语言（verbatim） | L174-180、L294-302 | 中（judge 需辨别引用来源） |
| PROC-08 | process | 具体化声明 + 具名社会证明 | L283-293 | 优 |
| PROC-09 | process | CTA 动作+利益、去摩擦 | L71-83 | 优 |
| PROC-10 | process | 反对意见预处置 | L333-338 | 优 |
| OUT-01 | output | 避免口号/术语/空泛声明 | L301-305 | 优 |
| OUT-02 | output | 清晰优先于机灵 | L376 | 优 |
| OUT-03 | output | 假设五段格式 | L186-194 | 优（与 SKILL.md 一致；与 workflow 7 段不一致是低危边角） |
| NEG-01 | negative | 无弱 CTA、无虚假稀缺 | L295-299 | 优 |
| NEG-02 | negative | 不先讲功能 | L125-142 | 优 |
| QA-01 | qa | 上下文单薄时问 5 类发现性问题 | L352-358 | 优 |

**19 项中 17 项可在 SKILL.md 正文找到明确依据且问题文本与技能指令一一对应，可追溯性在语料库中属上乘。**

### 6.3 标准设计缺口

1. **SCOPE-01 的「非广告平台文案」边界无正文支撑**：标准要求 agent 识别任务「不是广告平台文案」，但 SKILL.md 全文未提及广告文案边界，description 反而用宽泛的 "marketing materials"。agent 面对 Facebook 广告文案任务时无法从技能获得「这是边界外」的信号。
2. **无「阅读 references」类标准**：由于正文自包含，19 项标准全部可仅凭正文满足，三个 references 在测评中不产生任何被检测的行为约束——references 的价值（如 workflow 的 10 阶段、frameworks 的 headline types）在评分系统中完全隐形。若本技能设计意图是「正文导航 + references 深内容」的 navigation 型，SCORING 应补一项 references 使用证据类标准（如 tool_log 中出现 Read 引用文件）；若意图是自包含，则应删减正文冗余（§5）。
3. **PROC-05 建议显式写明「3 秒测试」**（当前问题文本写 "pass the 3-second test"，因 I1 存在，judge 可能误用 5 秒测试问法）。
4. **CF-01 与 QA-01 的组合张力**：用户薄上下文时，合规 agent 必须问发现性问题；但若用户不提供 VOC 材料，技能没有「降级路径」（§10 详述）。SCORING 未定义该情形下 judge 应如何裁决，建议在 SCORING 注释中写明：「agent 在无 VOC 材料时主动索要或标注假设 = 通过；无 VOC 材料直接写稿 = CF-01」。

---

## §7 check.py 检查器审查

- 结构：`check(workspace, tool_log, agent_output) -> dict[str, bool]`，按 `_shared/checker.py` 约定导入 `set_tool_log_path` / `set_agent_output`。与 CHECKER-LIBRARY.md 的 runner 协议一致。
- 行为：19 项全部为 llm judge，函数返回空 dict `{}`（注释自认 "0 script-verifiable checks"）。在 runner 的 JSON 结果中，本技能只产出 llm 判定，无脚本信号。这与 SCORING.yaml 完全自洽。
- 代码质量：可运行、无死代码。两处小冗余：(a) `check()` 内再次探测 `agent_output` 是否为路径（`os.path.exists`），而 `main()` 已将文件内容读入并替换为原文——双重探测逻辑实际不生效（理论上极短的输出文本恰好命中现存路径时才可能误判，概率可忽略）；(b) `workspace` 参数完全未使用。
- **测评影响**：全 LLM 判定意味着分数完全取决于 judge 对 `{skill_content + task_prompt + agent_output + tool_log}` 的综合判断。对 copy 这类「产出为自然语言、行为在过程中」的技能，这比脚本检查更合理；但 judge 必须依赖 tool_log 核验「agent 是否真的 Read 了 reviews/tickets」（CF-01 判定），建议在测评配置中把 judge prompt 明确要求引用 tool_log 证据（CHECKER-LIBRARY.md 已说明 judge 会收到 tool_log，只需在任务配置中强调）。

---

## §8 引用文件深度审查

### 8.1 references/frameworks-and-methodology.md（464 行）

- 结构：Hormozi 值框架（含公式与四象限）→ Headline Strategy（公式 + 4 种标题类型：BAB/PAS/Question-Answer/How-To）→ Offer Design = Copy（价值堆叠、价格锚定示例算术正确）→ Landing Page 应用（hero 公式、证明、pain breakdown、offer stack、timing）→ Copy Techniques → Conversion Mindset → Message Testing（5 秒测试、Mom Test、前后对比）→ Common Mistakes → Key Takeaways。
- 质量：方法论内容准确，示例具体（"Pays for itself in < 30 days"、"60-day money-back" 等全部一致），「Don't fake it: False scarcity destroys trust permanently」（L264）与 NEG-01 呼应。
- 问题：(a) 与 SKILL.md 重复面最大（§5 D1-D7）；(b) 「5-Second Test」（L380）与技能主文冲突（I1）；(c) 「Headlines do 80% of the conversion work」无出处；(d) 唯一标注的 Primary Source 为《$100M Offers》，无其他来源链——作为「科学」立场的 skill 略单薄，但可接受。
- 该文件保留价值最高的是 SKILL.md 未覆盖的：4 种标题类型、offer 工程/价值堆叠、证明层级（video > 实名 > 量化）、Mom Test 具体话术。

### 8.2 references/landing-page-workflow.md（551 行）

- 结构：Phase 1 策略定位（含 Strategy Brief 模板、5 个定位问题）→ Phase 2 VOC（5 类来源 + message bank 5 列表格 + Awareness Stage 列）→ Phase 3 消息架构（九段结构 + 写作标准 + 3 秒测试清单）→ Phase 4 布局设计 → Phase 5 线框 → Phase 6 构建与埋点（GA4/Clarity/PostHog、漏斗、预上线清单）→ Phase 7 假设积压（7 段格式 + ICE）→ Phase 8 A/B 测试（样本量公式示例、sequential learning 低流量替代）→ Phase 9 学习报告（完整 markdown 报告模板 + 指标）→ Phase 10 持续优化（周/月/季/年节奏）→ 常见失败模式 7 种 → 成功指标。
- 质量：是三个引用中工程价值最高的——Phase 7-9 提供了可落地的实验纪律（样本量计算示例、学习报告模板），Phase 2 的 Awareness Stage 分类比 SKILL.md 的 message bank 更专业。
- 问题：(a) 与 SKILL.md 的九段结构近逐字重复（D9）；(b) Phase 7 假设格式 7 字段 vs SKILL.md 5 字段（I3）；(c) Google Optimize 已停用未更新（§4.3）；(d) 该文件 40% 内容（Phase 4-6、8-10）实际是 CRO/产品工程范畴而非「文案」范畴——与技能边界（copywriting）有轻微 scope creep，但因技能定位含 conversion optimization，可辩护；(e) 示例中「15,000 visitors per variation」「30 days」等数字内部自洽（2% 基数 + 20% MDE 推算合理）。

### 8.3 references/tools-and-resources.md（344 行）

- 结构：6 类工具表（Research/Heatmaps/Analytics/Copy/A-B Testing/Builders）+ 排版指南与字体配对 + 参考书单（8 本，其中《$100M Offers》《Breakthrough Advertising》《Mom Test》《Thinking Fast and Slow》选书恰当）+ SaaS 灵感库 + 4 份方法论清单（Pre-Launch/A-B Test/Conversion Audit）+ 4 个速查公式（PAS/AIDA/FAB/4Ps）+ 学习资源（newsletter/podcast/community）。
- 质量：清单型文件，无逻辑风险；Pre-Launch 与 Conversion Audit 清单与 SKILL.md 原则逐条对应（3 秒测试、16px、WCAG AA、实名证明等）。
- 问题：(a) 无实质内容错误，但工具价格时效性不可验证（属知识快照类，可接受）；(b) 「Methodology Checklists」与 landing-page-workflow 的 Phase 6 预上线清单部分重叠（低危）；(c) 书单中 4 本书无链接（Breakthrough Advertising、Influence、Made to Stick、Don't Make Me Think），格式不统一（低危）。

---

## §9 人机感与语气审查

- **总体**：这是语料库中语气最鲜明的 mindset 型技能之一。「Positioning comes first. If the positioning is wrong, the page is doomed.」（L12）、「Don't write copy. Extract it from users.」（L13）、「Intuition is not a strategy.」（L15）、「Don't write without VOC research. Ever.」（L369）——格言体、命令短句、强烈立场。对文案创意类技能，这种「品牌化人格」是合理的刻意选择（dossier 亦如此判断），且对 agent 有强指令效力：核心纪律（先定位、先 VOC、具体优于空泛）几乎不可能被 agent 忽略。
- **正面**：全文零 emoji（语料库中少见）；「When Helping Users」将用户请求与 agent 行动分离，是成熟的人机交互设计；「If mom doesn't get it in 3 seconds, too clever」（L376）这类口语化锚点帮助 agent 校准输出语气。
- **风险面**：
  1. 人格与「科学化」的自称并存：「lab-coat-wearing conversion scientist」（L380）要求 agent「You stop guessing. You test.」——当用户无法提供测试条件（无数据、无实验环境）时，该指令无降级出口（§10）。
  2. 「Ever.」式绝对命令（L369）与 QA-01 配合时，agent 可能陷入「无 VOC 就绝不写」的死锁。
  3. 少量语录式断言（「Headlines do 80% of the conversion work」）是营销界的经验法则，由技能正文传达时可能被 agent 当作事实复述给用户——建议加「经验法则」限定词。
- **结论**：人机感 8.5/10。语气是资产，绝对化指令需要配套降级路径。

---

## §10 潜在 Agent 执行风险（测评视角）

站在 SkillIF 2 Mode × 5 Harness 矩阵审视，本技能有以下测评相关风险：

| # | 风险 | 场景 | 后果 | 缓解 |
|---|------|------|------|------|
| R1 | **VOC 材料可得性死锁** | 任务 prompt 给出产品描述但无 reviews/tickets/访谈材料 | 合规 agent 依 L369 拒绝写稿或只问问题 → 任务未完成；写稿则触发 CF-01 cap_to_0 | 任务 prompt 必须内置 VOC 材料（或规定「agent 可自行抓取公开评论」的 harness 才有 web 权限）；在 SCORING 注释中明确「索要材料=通过」 |
| R2 | **架空式虚构 VOC 的鉴别难度** | agent 编造「用户原话」规避 CF-01 | PROC-07/CF-01 全靠 judge 辨别引用来源 | judge prompt 要求以 tool_log 中的 Read 证据交叉核验引用出处 |
| R3 | **双测试标准（I1）** | judge 用「5 秒/What's the main benefit」问法核验 PROC-05 | 同一 agent 行为得到不同判定 | 修复 I1；PROC-05 问题文本显式写「3 秒、三问（是什么/给谁/为何现在）」 |
| R4 | **trigger 面过宽** | no-trigger 对照组任务含「写点营销文案」「帮我做品牌文案」 | description 的 "marketing materials / product positioning" 尾部可能诱导对照组 agent 误触发，污染 Mode 对照 | 对照集任务设计时避开 marketing 类表面词，或本技能对照组明确排除 |
| R5 | **无 references 使用检测** | agent 仅读 SKILL.md 即满分 | 评分无法区分「深度使用 10 阶段工作流」与「浅层套模板」 | §6.3 建议：SCORING 增 references 使用项（tool_log 证据），或正文去冗余 |
| R6 | **绝对指令与完成任务的对立** | 用户催促「别问了快写」 | agent 在「纪律」与「响应」间两难 | 正文补「VOC 不可得时的降级路径」（见 §12 修复建议） |

R1 是本技能在测评中最可能系统性失效的点，必须在任务 prompt 设计中解决（与 139-clearance 等「门控型」技能同理，但本技能的门是材料依赖型而非权限依赖型）。

---

## §11 与 Skill Dossier 对照

dossier（2026-08-05，batch 076-100）对 087-copy 的记录：

> 逻辑: 定位→VOC 提取→消息层级→写作→假设测试→学习完整循环，各框架一致。语法: 干净、有力、专业文案文体。人机感: Persona-based 第二人称是文案 skill 的刻意品牌选择。合规: 🟢 完全合规——三节齐全，body ~397 行。总评: 🟢 完整、精心打造的 skill。

本审查与之对照：

| 维度 | dossier 判断 | 本审查判断 | 差异说明 |
|------|------------|-----------|---------|
| 逻辑 | 各框架一致 | 大体一致，但发现 I1-I4 四处跨文件不一致 | dossier 未做跨文件比对 |
| 语法 | 干净有力 | 同意 | 一致 |
| 人机感 | 刻意品牌选择 | 同意，另指出绝对指令缺降级路径（R6） | 补充 |
| 合规 | 🟢 三节齐全 | **部分不符**：Output Format 与 Scope/Limitations 两节实质缺失（§3.3）；body 实测 391 行 vs 记录 ~397 | 判定口径差异：dossier 把 Essential Workflows/Quick Reference/When to Use 视为三节，本审查按 §3.1「MUST」字面执行 |
| 总评 | 🟢 | **🟡** | 差异由两处结构缺失 + 冗余（§5）+ 跨文件不一致（§4.2）支撑 |

说明：dossier 的宽松判定在其「速扫 322 个」的吞吐下可以理解，且其对 087-copy 的定性与本审查高度一致（内容确实精良）；但作为实验语料，结构缺口与一致性漂移会直接传导到测评判定（§10），故建议按 🟡 处理并执行 §12 修复。

---

## §12 修复建议清单（按优先级）

### P0（测评前必改）

| # | 建议 | 位置 | 工作量 |
|---|------|------|:----:|
| F1 | 新增 `## Scope / Limitations` 节：明确排除广告平台文案、社媒 caption 批量写作、SEO 博客文章、非 SaaS 消费品（或显式声明覆盖）；写明「VOC 材料不可得时：向用户索要 → 用户无法提供时改以公开渠道自行检索 → 仍不可得则基于行业常识撰写并显著标注假设，不得伪装成 VOC 原话」——补上 R6/R1 的降级路径 | SKILL.md 正文 | 小 |
| F2 | 新增 `## Output Format` 节：定义交付物清单（① 策略简报/定位摘要 ② message bank（沿用 5 列格式）③ headline 选项 3-5 条及公式标注 ④ 按九段结构的落地页文案 ⑤ 假设卡（五段格式）⑥ 学习笔记）；写明给用户的呈现方式 | SKILL.md 正文 | 小 |
| F3 | 统一测试标准：将 frameworks L380-388 的「5-Second Test」改为「3-Second Test」并与 SKILL.md 三问对齐 | frameworks-and-methodology.md | 极小 |
| F4 | SCORING.yaml 补注释：CF-01 的判定边界（索要材料=合规；无材料写稿=cap 0；标注假设的降级写稿=不触发 CF-01 但 PROC-07 降分）；PROC-05 问题文本显式写「3 秒」 | SCORING.yaml | 极小 |

### P1（推荐）

| # | 建议 | 位置 | 工作量 |
|---|------|------|:----:|
| F5 | 删除 D2-D7 六块逐字重复（Slippery Slide、Pain Is the Pitch、Hero 公式示例、反对意见表、mom 规则、goldfish 句），改为一行指针链接；预计正文 391 → ~260 行 | SKILL.md | 中 |
| F6 | 统一 I2/I3/I4：标题公式措辞、假设格式（建议 5 段为主、workflow 的 Risk/Effort 作为可选补充行）、message bank 列（建议统一为 5 列） | 三个文件 | 小 |
| F7 | 新增 SCORING 项「reference 使用证据」：agent 在产线中 Read 至少一个 references 文件（`tool_log` 可验证，可做成 `judge: script` 的 `tool_log_contains` 项，让 check.py 不再空转） | SCORING.yaml + check.py | 中 |
| F8 | 「Headlines do 80%...」加「经验法则（非实证）」限定；Google Optimize 条目改为「已停用（2023）」 | references | 极小 |

### P2（可选）

| # | 建议 | 工作量 |
|---|------|:----:|
| F9 | check.py 移除冗余的双重路径探测、未用参数；或干脆删除 check.py 并在 runner 配置中声明该技能无脚本检查 | 小 |
| F10 | 书单中 4 本无链接书目补链接或统一格式 | 极小 |
| F11 | 将「When to Use Each Copy Approach」微扩为三行边界表（本技能做什么/不做什么/何时应找别的技能） | 小 |

---

## §13 综合评估结论

### 13.1 维度评分汇总

| 维度 | 评分 | 一句话 |
|------|:----:|--------|
| 内容质量 | 9.0/10 | 框架准确、示例具体、纪律鲜明，语料库 mindest 型前列 |
| 逻辑一致性 | 7.5/10 | 正文内部自洽；跨文件存在 1 处实质不一致（3 秒/5 秒）与 3 处措辞级漂移 |
| 语法与可读性 | 9.5/10 | 干净、有力、零错字；格言体有效 |
| 人机感 | 8.5/10 | 品牌化 persona 是资产；绝对指令缺降级路径 |
| 规范合规性 | 7.0/10 | frontmatter/description/命名/引用全通过；Output 与 Scope 两必需节缺失；体量超 mindset 目标 8 倍 |
| SCORING 质量 | 8.5/10 | 19 项可追溯性上乘；缺 references 检测与广告文案边界支撑 |
| 检查器 | 6.0/10 | 与全 llm 判定自洽；check.py 空转，无客观信号 |
| 测评就绪度 | 7.0/10 | 需先解决 R1（VOC 材料供给）与 I1，否则判定方差大 |

**综合评级：🟡（可用但有明确问题，建议微调后达 🟢）**

### 13.2 优势详述

1. **纪律性最强的内容骨架**。从 Core Philosophy 到 When Helping Users，每一条核心纪律都有锚点与示例：「Positioning comes first」（L12）→「Get strategy brief approved before writing」（L373）；「Extract it from users」（L13）→ message bank 表（L176-180）；「Intuition is not a strategy」（L15）→ 假设五段格式 + ICE（L184-216）。这类「宣言→机制→工具」的三层结构在语料库中只有法律类顶级 skill（如 054、067）可与之比肩。
2. **SCORING 与正文的逐条映射**。19 项标准中 17 项能在正文找到近乎逐字对应的指令（§6.2），这意味着 judge 判定有明确依据，agent 有明确行为契约——对测评实验而言这是最宝贵的设计属性，因为判定的解释方差被压到最低。
3. **description 完全合规且触发面恰当**。「Use when...」逐字命中规范模板，WHAT/WHEN/KEYWORDS 三要素齐全，无路由污染。
4. **引用体系闭合**。三个 references 全部存在、锚点全部有效、无跨技能路径；references 各自也有独立增量（frameworks 的标题类型与 offer 工程、workflow 的实验纪律与学习报告、tools 的书单与清单）。
5. **人机交互设计成熟**。Discovery Questions 明确列出五类信息；「Request from Users」在写稿前框定材料清单；「Mom Test」类锚点将抽象标准（清晰/具体）落为可执行的检查。全篇无 emoji、无喊叫式大写、无商业化推销（对比 007 的 K-Dense 推销、072 的 emoji 泛滥）。

### 13.3 弱项详述（含证据）

按严重度排序：

1. **【中】Output Format 节缺失（§3.3）**。正文最接近输出描述的是 L176-180 的 message bank 表（过程工具）与 L384-395 的 Quick Reference（索引）。交付物形态（策略简报、标题选项、按九段结构的完整文案、假设卡）全部只隐含不定义。后果：agent 输出的「成品」无契约可依，judge 在 OUT-01/02/03 之外无「结构符合交付约定」的判定锚点。
2. **【中】Scope/Limitations 节缺失（§3.3）**。技能边界（不做广告文案、不做批量社媒文案、非 SaaS 场景）完全未声明；description 的 "marketing materials" 反而拓宽了边界。后果：误触发面扩大（R4），SCOPE-01 的「非广告平台文案」判定失去正文依据（§6.3）。
3. **【中】3 秒/5 秒测试不一致（I1，§4.2）**。同一技能内并存「3-Second Test（三问：是什么/给谁/为何现在）」（SKILL.md L117-122、landing-page-workflow L126-133、tools L193）与「5-Second Test（三问：是什么/给谁/主要好处）」（frameworks L380-388）。PROC-05 的判定将随 judge 采信哪一处而漂移（R3）。
4. **【中】VOC 材料依赖无降级路径（R1/R6）**。「Don't write without VOC research. Ever.」（L369）是优秀纪律，但没有「材料不可得怎么办」的分支。在测评 harness 中这是系统性失效源：合规即卡死，写稿即 CF-01。必须由 SCORING 注释与正文降级路径（F1/F4）共同闭合。
5. **【中】40-45% 正文冗余（§5）**。D2-D7 六块逐字级重复使正文膨胀至 391 行（mindset 目标 ~50 行），并直接催生了 I1-I3 的多点维护漂移。冗余本身不致命，但「references 沦为装饰」与「SCORING 无 references 检测」（§6.3-2）叠加，使三个 1359 行的高价值文件在测评中零可见度。
6. **【低】SCOPE-01 广告文案边界无正文支撑**（§6.3-1）。标准文本要求 agent 识别「非广告平台文案」，正文未提供该判别的任何特征信号。
7. **【低】check.py 空实现与双路径探测冗余**（§7）。与全 llm 判定自洽，但 runner 侧可考虑以 `tool_log_contains` 类脚本项回收一点客观信号（F7）。
8. **【低】时效性小瑕疵**：Google Optimize「正在弃用」（workflow L322，实际 2023 已停用）；「Headlines do 80%...」（frameworks L77）无来源；书单 4 项无链接格式不统一。

### 13.4 SKILL.md 逐节走查（行为契约视角）

| 节（行区间） | 内容 | 对 agent 的行为指令 | 与 SCORING 的联动 |
|-------------|------|--------------------|-------------------|
| Core Philosophy（L10-16） | 5 条信条 | 定位优先、VOC 基础、框架化、信息架构、测量迭代 | SCOPE-02/03、PROC-04 的宣言层 |
| Your Expertise（L18-34） | 四能力域 | 无独立指令，定义能力边界 | SCOPE-01 的认知框架 |
| Quick Decision Framework（L38-83） | 三分类切入 + 标题公式表 + CTA 速查 | 按 awareness 选切入、套公式、CTA 动作+利益 | PROC-02/03/09、NEG-01 |
| Core Frameworks（L87-142） | Hormozi 等式、Hero 公式、消息层级 | 最大化分子、最小化分母；三问测试；O→B→F 排序 | PROC-01/04/05 |
| Essential Workflows（L146-230） | VOC 来源+message bank、假设五段格式+ICE、九段落地页结构 | 挖引用、建消息库；测试前写假设卡；按九段组织页面 | PROC-06/07/08、OUT-03、CF-01 |
| Reference Guides（L234-272） | 三 references 索引 | 深内容入口（正文已自包含，此为知识延伸） | 当前无 SCORING 项（§6.3-2） |
| Key Principles（L275-305） | 五组原则 + Avoid 清单 | 具体化声明、实名证明、去摩擦 CTA、禁口号/术语/空话 | PROC-08/09、OUT-01/02、NEG-01/02 |
| Common Patterns（L309-346） | Slippery Slide、反对意见预处置、Pain Is the Pitch | 页面流设计、预处置四反对、痛感具体化 | PROC-10（与 frameworks 重复，§5 D3-D5） |
| When Helping Users（L350-380） | 发现性五问、材料清单、6 步过程 | 先问后写、索要 VOC、定位简报先行、标注假设 | QA-01、SCOPE-02/03、R1/R6 风险所在 |
| Quick Reference（L384-395） | 任务→要点→锚点速查表 | 检索辅助，无新指令 | 无 |

走查结论：行为指令密度自 L38 起逐段增高，至 When Helping Users 达到契约最强点（无 VOC 不写稿）。该强契约既是本技能区分度之源，也是 R1 死锁之源。

### 13.5 判定演练（worked example，验证 19 项标准的可执行性）

为检验 SCORING 在真实 harness 中的可操作性，构造两个假设运行：

**运行 A（合规 agent）**：任务 prompt 含产品简介 + 3 条 G2 评论 + 2 条支持工单。agent 先输出策略简报（受众=年营收 $1M+ 的 SaaS 运营负责人、差异化=报表自动化），用评论原话建 message bank，按九段结构写出落地页，hero 标题「Turn 3-Hour Reports Into 5-Minute Dashboards」（源自工单原话），CTA「Start Free Trial — No credit card required」，并在末尾给出假设卡「If we: 将 CTA 从 Sign Up 改为 Start Free Trial / Then: 点击率上升 / Because: VOC 显示用户需要免费保证 / Measured by: CTA 点击率 / Success: +10% vs 基线」。

预期判定：19/19 通过。SCOPE-01（任务识别）✓；SCOPE-02（先定位）✓（策略简报在文案之前）；SCOPE-03（用 VOC）✓（tool_log 有 Read 评论文件）；PROC-01/02/03/04/05/06/07/08/09/10 全部有可直接引用的文本证据；OUT-01/02/03 ✓（假设卡逐字符合五段格式）；NEG-01/02 ✓；QA-01 因上下文不薄而不适用（标准文本「when thin context」自带条件门，判定无歧义）。判定全程只需读 agent 输出，tool_log 仅作 CF-01 的交叉证据——可操作性良好。

**运行 B（非合规 agent）**：无 VOC 材料即写稿，标题「Revolutionary AI-Powered Synergistic Ecosystem」，CTA「Submit」。预期判定：SCOPE-01 ✓（识别为文案任务），SCOPE-02 部分（有定位但未简报），SCOPE-03 ✗、PROC-01/02/03/04/05/07/08/09/10 多数 ✗，OUT-01/02 ✗（口号+术语+空话），NEG-01/02 ✗，OUT-03 若未提假设 ✗；CF-01 触发 → 总分归零。

**判定演练的发现**：(a) 19 项标准在良/劣两极运行上均能给出明确且互斥的判定，区分度验证通过；(b) 中间态（SCOPE-02 部分）需要 judge 作程度判断，是唯一模糊带，但 CF 机制兜底；(c) 运行 B 的 CF-01 依赖 judge 核验「无 VOC 材料」这一前提——要求 task prompt 明确声明提供或未提供 VOC 材料，否则判定证据不足。此点应写入测评运行说明。

### 13.6 与 dossier 判定差异的复核

dossier 对 087-copy 的 🟢 在「内容与语气」维度完全成立，本审查无异议；差异集中在合规口径（三节是否齐全、body 行数 391 vs 记录 ~397）与跨文件一致性两个此前未检查的维度。综合 13.1 的 8 个维度得分，🟡 比 🟢 更准确地反映「内容上乘、结构待修」的实际状态。此差异不影响 dossier 的整体统计（其汇总已注明「缺 scope 节」为语料库共性问题，087-copy 正是其中一员）。

### 13.5 实验就绪度评估（SkillIF 2 Mode × 5 Harness）

| 就绪项 | 状态 | 说明 |
|--------|:----:|------|
| 触发可靠性（trigger 模式） | 良 | description 触发词丰富（landing page/positioning/messaging/copy），SaaS 文案类任务召回高 |
| 对照隔离（no-trigger 模式） | 中 | "marketing materials / product positioning" 尾部有跨任务误触发风险（R4），对照集需避让 |
| 判定可行性（llm judge 19 项） | 良 | 17 项有正文锚点；PROC-05 需先修 I1；PROC-07/CF-01 需 judge 依赖 tool_log |
| 任务 prompt 设计要求 | **高** | 必须内置 VOC 材料（reviews/tickets/访谈片段），否则 R1 死锁；建议任务 prompt 附 1 段用户评论 + 1 条支持工单 + 产品简介，覆盖全部 19 项的可触发条件 |
| 脚本信号 | 无 | check.py 空转；可考虑 F7 回收 1 项 references 使用证据 |
| 对照组行为基线 | 未知 | 无 trigger 对照集中，未经本技能约束的 agent 写文案的行为基线待测——本技能纪律性极强，预期 compliance 差距大、区分度高，是理想的 Mode 对比样本 |

**结论**：本技能作为「高区分度测评样本」的潜力很大（纪律与普通 agent 直觉行为的差距显著，如「先定位」「用客户原话」「假设格式」），但前提是 P0 四项修复（F1-F4）完成，否则 R1（VOC 死锁）与 R3（测试标准漂移）会成为判定噪声的主要来源。

### 13.6 最终裁定

- **评级**：🟡（dossier 的 🟢 需下调一档）
- **一句话**：内容与语气是语料库顶级文案 skill，但缺两必需节、超 mindset 体量 8 倍、跨文件存在一处实质不一致，且 VOC 绝对指令缺降级路径——修复 F1-F4（估 1 小时内）后可稳定达到 🟢 并作为 mindset 型测评样本。
- **行动项**：P0 四项（F1-F4）在测评启用前完成；P1 五项（F5-F8）建议同批处理；P2 三项（F9-F11）可择机。
