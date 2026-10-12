# REVIEW：288-skill-judge（Skill Judge）

- 审查日期：2026-08-06
- 审查方式：全文通读（10 个文件全部逐行读取）
- 审查依据：`complex-skills/_shared/SKILL-SPEC.md` v1.0（12 项合规清单）、`_shared/checker.py` 接口、skill 自身声称的标准（17+ 官方示例、D1–D8 八维评分体系）
- 文件统计：SKILL.md 500 行；README.md 245 行；SCORING.yaml 142 行；check.py 62 行；references/ 下 6 个文件共 75 行；合计 1024 行（与 SKILL.md 的 500 行形成奇妙的巧合，恰为 2^10）

---

## 1. 目录清单

| 文件 | 行数 | 类型 | 一句话定位 |
|------|------|------|-----------|
| SKILL.md | 500 | 主文件 | 八维评分体系（D1–D8）+ 核心哲学 + NEVER 清单 |
| README.md | 245 | 人类文档 | 完整报告模板、9 大失败模式、使用示例（Agent 不可见） |
| SCORING.yaml | 142 | 评测规范 | 15 条全 LLM 评审准则（scope/process/output/negative/qa 五类） |
| check.py | 62 | 检查脚本 | 零脚本检查存根，返回空字典 |
| references/evaluation-protocol.md | 53 | 参考文件 | 5 步评估协议（Step 5 截断、代码围栏未闭合） |
| references/summary.md | 5 | 参考文件 | 报告 Summary 节模板（占位符） |
| references/dimension-scores.md | 11 | 参考文件 | 报告维度得分表模板（D2 命名与 SKILL.md 不一致） |
| references/critical-issues.md | 1 | 参考文件 | 单行占位标题 |
| references/top-3-improvements.md | 3 | 参考文件 | 三条占位编号列表 |
| references/detailed-recommendations.md | 2 | 参考文件 | 占位标题 + 占位条目 |

总体观察：目录结构符合 "references/ 收尾资源" 的分层惯例，6 个参考文件全部存在，但其中有 5 个是**模板占位符**而非可用参考内容；SKILL.md 末尾的 Reference Files 清单是全篇唯一的引用入口，且是 skill 自己在 D5 中判定为 "Poor" 的那种"被动列出、无加载指引"的形式。这个 skill 的结构自我违例是全篇审查最突出的主线。

---

## 2. Frontmatter

Frontmatter 为标准 YAML，共 2 个字段：

```yaml
---
name: skill-judge
description: Evaluate Agent Skill designs against official specifications and best practices. Use when reviewing, auditing, or improving SKILL.md files and skill packages. Provides multi-dimensional scoring and actionable improvement suggestions.
---
```

**name 字段**：`skill-judge`，小写、连字符、长度合规（≤64）。与目录名 `288-skill-judge` 的匹配关系：严格按 SKILL-SPEC §1.1 "MUST match directory name" 字面理解，二者不一致（缺 NNN 前缀）；若按语料库惯例"NNN- 为序号前缀、匹配时忽略"理解则通过。语料内大概率沿用后者，故判为 ⚠️ 边缘项而非违规项，但审查意见中如实记录。

**description 字段**：233 字符（实测，≤1024 通过）。逐要素拆解：

- WHAT：明确。"Evaluate Agent Skill designs against official specifications and best practices" + "Provides multi-dimensional scoring and actionable improvement suggestions"，功能陈述具体。
- WHEN：有。"Use when reviewing, auditing, or improving SKILL.md files and skill packages" 是显式触发场景。
- KEYWORDS：部分。含 reviewing、auditing、improving、SKILL.md、skill packages、scoring 等动作动词与领域词，但缺少更易命中的口语化触发词（"evaluate this skill"、"skill quality"、"score"、"audit skill" 等）。README.md 第 30–36 行列了 6 条触发短语，可惜那部分内容 Agent 永远不会读到——触发词应当下沉到 description 本身。
- 人称：第三人称，无第一/第二人称、无 "Use this skill to..." 命令式开头。✓
- 触发信号：`"Use when reviewing..."` 是规范列出的信号形式（"Use when the user..."、"Use for..."）的变体，缺 "the user" 主语。规范 §2.4 要求"至少出现一个"所列信号——本描述出现的恰好是"列表之外的近似形式"，判为 ⚠️ 边缘通过（合规讨论见第 7 节第 5 项）。

**可选字段**：allowed-tools / argument-hint / user-invocable / model / paths / disable-model-invocation 全部未使用。可选字段缺席本身不违规，但对照该 skill 的使用场景（用户给出一个 skill 路径做评估），argument-hint 的缺失让描述里没有调用形态提示，README 里的使用示例（"Evaluate the skill at skills/my-new-skill/SKILL.md"）无法被 Agent 看到，属于可优化的点（🟢 级）。

**禁止字段**：无。仅 name + description，没有 §1.3 列举的任何禁用键。✓

**元数据位置**：SPELL 规范 §1.3 允许把 license/author 等放进正文末尾的 `## Metadata` 段——本 skill 没有此类内容，无违例。

---

## 3. Body 结构

正文 500 行（wc -l 实测），按 SKILL-SPEC §3.1 的"三段必备结构"逐一对照：

**Workflow / Process —— 缺失 ✗**

正文没有 `## Workflow` / `## Process` 这类"分步执行流程"章节。真正的工作流（5 步协议：知识增量扫描 → 结构分析 → 分维评分 → 合计定级 → 生成报告）被放在了 references/evaluation-protocol.md 里，而正文从未指示 Agent 去读它（详见第 5 节 D5 违例）。正文中的 D1–D8 各维度更接近"评分准则手册"，是 rubrics 而非流程；Agent 读完正文后并不知道"先做什么、后做什么"。这是该 skill 对自身宣称的"official specifications"最直接的背离——它教别人必须有 Workflow 段，自己却没有。

**Output Format —— 缺失 ✗**

正文没有报告输出格式定义。完整报告模板（Summary 字段、维度表、Critical Issues、Top 3、Detailed Analysis 骨架）分散在 README.md（第 146–167 行，Agent 不可见）和 5 个 references 模板碎片里（summary.md、dimension-scores.md、critical-issues.md、top-3-improvements.md、detailed-recommendations.md，均无加载触发器）。更关键的是**定级量表（A/B/C/D/F 及各档分数区间）只存在于 README.md 和 evaluation-protocol.md**，正文 500 行里找不到 "90%+ 为 A" 这样的换算规则。一个被调用的 Agent 无法按该 skill 产出规范报告，因为产出规范不在它能看到的任何地方。

**Scope / Limitations —— 缺失 ✗**

正文没有"本 skill 不做什么"的边界说明。例如：不适用于 MCP server 配置评估、不评估 tool 本身、单文件 vs 多文件 skill 的适用差异（D5 末尾"简单 skill 打分方式"只是评分特例而非边界声明）。SPELL §2.5 明确"cross-skill routing 属于正文 Scope 段"——本 skill 没有该段，也没有任何 NOT-for 说明。

**已具备的部分**：

- 核心哲学（第 13–74 行）：What is a Skill、Core Formula、Tool vs Skill、三类知识。质量见 D1 自评——按它自己的红牌标准（"What is [basic concept]" 节）这段恰恰是红区，详见第 4、12 节。
- 八维评分体系（第 78–476 行）：D1–D8 每维有分值、评分表、正反例、测试问题，是全篇知识密度最高的部分。
- NEVER Do When Evaluating（第 479–489 行）：10 条反模式清单，质量高（见 D3 评述）。
- Reference Files（第 494–501 行）：6 条被动列表，无任何加载条件。

**行数**：500 行 ≤ 600 硬上限 ✓；但 SKILL.md 自身 D5 节写着 "Ideal: < 500 lines"，且自身 D7 模式表给出 Process 模式 ~200 行、Tool 模式 ~300 行——本文件 500 行，按它自己的标准判，"Tool" 尺寸的内容承载了接近双倍的体量，与其 SCORING.yaml 自报的 `pattern: process` 不匹配。自我违例的又一个实例。

**结论**：三段必备结构中 0/3 出现在正文；12 项合规清单中对应第 8、9、10 三项全挂。对于一个以"规范遵从度"为第 4 维核心的评估 skill，这是讽刺性的硬伤。

---

## 4. 逻辑一致性

**内部一致的方面**：

- 总分核算：20+15+15+15+15+15+10+15 = 120，与各处 "120 points total" 一致 ✓
- 定级量表换算自洽：108/120=90%、96/120=80%、84/120=70%、72/120=60%，README 与 evaluation-protocol.md 两处区间完全一致 ✓
- D5 三层加载模型（metadata→body→resources）与 SPELL 精神一致 ✓
- D7 模式表（Mindset ~50 / Navigation ~30 / Philosophy ~150 / Process ~200 / Tool ~300）与 SKILL-SPEC §3.2 的官方目标行数完全吻合，说明该部分确实源于官方语料分析 ✓
- SCORING.yaml 的 SCOPE-02 对八维的列举与正文 D1–D8 完全对得上 ✓

**不一致的方面**：

1. **D2 维度命名漂移**：正文标题是 "D2: Appropriate Mindset + Procedures"（SKILL.md 第 112 行），references/dimension-scores.md 第 6 行写 "D2: Mindset vs Mechanics"，SCORING.yaml 第 32–34 行写 "Mindset vs mechanics"（PROC-02）。同一维度三个名字，Agent 引用维度时会无所适从，也影响 SCORING 评审者的证据核对。🟡
2. **"17 official" vs "17+"**：SKILL.md 第 410 行 "Through analysis of 17 official Skills"，description 写 "17+ official examples"——同一语料两个口径，小事但属于精度瑕疵。🟢
3. **9 大失败模式只见于 README**：README.md 第 102–114 行列举 9 个 common failure patterns（The Tutorial、The Dump、The Orphan References……），正文完全没有；而正文 NEVER 清单、D1 红牌区、D5 触发器等级表本应与之互为印证。这个最精彩的总结性内容放在了 Agent 永远看不到的 README 里，属于"知识放错了层"。🟡
4. **报告模板被切成 6 片**：evaluation-protocol.md 的 Step 5 模板在 "# Skill Evaluation Report: [Skill Name]" 处戛然而止（文件在第 53 行结束，代码围栏未闭合），其余章节分别躺在另外 5 个模板文件里。Agent 即使读了 protocol 也拿不到完整模板；模板碎片之间的唯一粘合剂是 README——Agent 又看不到。整条"产出格式"链路逻辑上是断的。🔴
5. **自述模式与 SCORING 模式矛盾**：SCORING.yaml 声明 `pattern: process`，而正文 500 行、以评分 rubrics + 示例代码块为主体的形态更接近 Tool 模式（~300 行）的膨胀版；按它自己的 D7 评分表，这属于 "Partially follows a pattern with significant deviations"（4–6 分档）。🟡
6. **D5 触发器自评与实际不符**：正文 D5 节（第 318–325 行）用四级量表（Poor/Mediocre/Good/Excellent）衡量"带 references 的 skill"的加载触发器，而它自己第 494–501 行的 Reference Files 清单就是量表里 "Poor" 的原型（"References listed at the end, no loading guidance"）。评分为零的技巧被用在自己身上。🔴（语义上属逻辑矛盾，见第 5、9 节展开。）

---

## 5. 参考文件（逐文件全文分析）

### 5.1 references/evaluation-protocol.md（53 行）

5 步协议全文：Step 1 知识增量扫描（[E]/[A]/[R] 三分类 + E:A:R 比例阈值：好 skill >70% Expert、<20% Activation、<10% Redundant）；Step 2 结构分析（frontmatter、行数、参考文件清点、模式识别、触发器检查）；Step 3 分维评分（引证行号、一行理由、低于满分的改进建议）；Step 4 合计与定级（复用 README 中的 A–F 量表，两处一致）；Step 5 生成报告（模板在此开片，第 53 行 "# Skill Evaluation Report: [Skill Name]" 即文件末尾，**未闭合的 ```markdown 代码围栏**让整个文件在渲染器里成为代码块，模板下半部分被后续的 5 个模板文件分割承接）。

这实际上是全 skill 唯一正式的 Workflow 定义，质量尚可（5 步顺序合理、有可操作的阈值），但它有三个致命问题：(a) 正文从未触发加载它；(b) 末尾截断 + 围栏未闭合（语法错误，见第 6 节）；(c) E:A:R 比例阈值只在"流程"里出现一次，正文 D1 从未提过这个量化口径，两者对"知识增量如何量化"的陈述不统一。🔴

### 5.2 references/summary.md（5 行）

报告 Summary 节模板：Total Score X/120、Grade、Pattern、Knowledge Ratio E:A:R、Verdict 五行占位。内容本身正确，与 README 的模板头部一致；但它是"输出格式碎片 #1"，孤立存在、无触发。🟡

### 5.3 references/dimension-scores.md（11 行）

维度得分表模板，8 行占位（X / 20、X / 15……）。其中 D2 列名 "Mindset vs Mechanics" 与正文 "Appropriate Mindset + Procedures" 不一致（见第 4 节第 1 项）。表格结构完整可用。🟡

### 5.4 references/critical-issues.md（1 行）

单行占位：`## Critical Issues` + `[List issues that must be fixed...]`。纯占位，无任何内容。🟡

### 5.5 references/top-3-improvements.md（3 行）

三条编号占位（"[Highest-impact improvement to make]" 等）。纯占位。🟡

### 5.6 references/detailed-recommendations.md（2 行）

`## Detailed Recommendations` + 一条占位 bullet，且该行后跟着一个 ` ``` `（evaluation-protocol.md 未闭合围栏的"尾巴"被甩进了这个文件）——这是截断模板的残骸，语法层面的连锁证据。🟡

**六文件综合评述**：5 个文件是输出模板碎片，1 个文件是流程协议且被截断。它们彼此之间靠 README 串联，而 README 不在 Agent 加载路径上。用这个 skill 自己的术语讲：这是一组**Orphan References**（README 列出的 9 大失败模式之三）加 **Checkbox 模板**——参考文件体系在"设计意图"上想实现渐进披露，在"实际交付"上是一堆没人会被指引去读的占位符。若 Agent 主动读全这 6 个文件，它能拼出报告模板；但没有任何机制促使其这么做，D5 触发器评分理应得最低档。

---

## 6. 语法格式

**SKILL.md**：

- Frontmatter YAML 解析正常（name 字符串、description 单行无引号包裹但无冒号冲突，233 字符可安全内联）✓
- Markdown 结构：标题层级规范（# → ## → ###），表格语法均合法 ✓
- **"SKILL ACTIVATION FLOW" 示意图（第 231–238 行）错乱**：本应为对齐的 ASCII 流程图，实际被自动换行打断，呈现在文件里是：
  ```
  User Request - Agent sees ALL descriptions - Decides which
                     of skills (only descriptions,  to activate
                     not bodies!)
  ```
  三行内容互相穿行，"which / of skills / to activate" 被拦腰折断；且这段文本既无代码围栏也无缩进，视觉上是三行杂乱的散文。对 "THE MOST IMPORTANT FIELD" 的论证火力被排版事故抵消。🔴（第 13 节给出修复方案）
- 第 33 行 "hot-swappable LoRA adapter"、"educating AI" 等比喻行文流畅；第 44 行 "context window is a shared public resource" 表达清晰 ✓
- 代码围栏配对检查：第 143–149、151–158、231–238（未成对，见上）、457–467 行各围栏中仅 231 处有围栏缺失问题；457–467 行围栏内嵌套了 "**Common issues**:" 加粗文本，作为示例内容合法 ✓
- 全篇无残留占位符、无 TODO ✓（讽刺的是占位符全部集中在 references 里）

**references/evaluation-protocol.md**：第 53 行文件在 ```markdown 打开后无闭合即 EOF——未闭合代码围栏，多数渲染器会把 Step 5 模板全部渲染为代码块，且该围栏的闭合反引号散落在 detailed-recommendations.md 的第 2 行（"```"），跨文件围栏配对是明显的编辑事故。🔴

**SCORING.yaml**：结构合法（嵌套 map 缩进统一、注释以 `#` 正确书写、锚点无引用问题）；全部 15 条 `judge: llm`，无 `script:` 检查项，与 check.py 的"0 script checks"自述一致 ✓。语料内容（question/evidence 字段）无换行引号转义问题 ✓。

**check.py**：语法无误、可运行（imports 链 `../_shared/checker` 已确认存在，checker.py 提供 set_tool_log_path / set_agent_output / output_contains 等函数）。逻辑细节问题见第 9 节。

**README.md**：格式良好，无语法问题。

---

## 7. 规范合规（12 项逐项核对，依据 SKILL-SPEC.md §5）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | name：小写+连字符、≤64、匹配目录名 | ⚠️ | 格式 ✓；目录 `288-skill-judge` vs name `skill-judge`，NNN 前缀剥离是否算"匹配"取决于语料惯例，字面不符 |
| 2 | description：第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✓ | 233 字符；三段要素齐全（KEYWORDS 偏弱但不缺失） |
| 3 | description 无命令式/第一/第二人称开头 | ✓ | "Evaluate Agent Skill designs..." 第三人称陈述 |
| 4 | description 无跨 skill 路由 | ✓ | 无 "NOT for X, use Y" |
| 5 | description 至少一个触发信号短语 | ⚠️ | "Use when reviewing..." 是 "Use when the user..." 的变体，缺 "the user"，位于规范所列信号列表之外 |
| 6 | frontmatter 无允许列表之外键 | ✓ | 仅 name + description |
| 7 | body ≤600 行 | ✓ | 500 行 |
| 8 | body 有 workflow/process 段 | ✗ | 流程在未触发的 references/evaluation-protocol.md 里，正文零流程 |
| 9 | body 有 output format 段 | ✗ | 模板碎片在 references/README，正文零格式定义、零定级量表 |
| 10 | body 有 scope/limitations 段 | ✗ | 完全缺席 |
| 11 | body 无跨 skill 文件引用（../other-skill/） | ✓ | 正文唯一链接指向本 skill 的 references/；提到 docx、pdf、xlsx、frontend-design 等仅为示例文本（非路径），合规 |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✓ | `288-skill-judge` |

**合计：9 通过 / 3 未通过（第 8、9、10 项）/ 2 边缘（第 1、5 项）。**

最刺眼的是第 8、9、10 三项——恰是"三段必备结构"整体缺失。该 skill 的 D4 维度（规范遵从）在满分 15 里按它自己的标准只能拿到中低分：frontmatter 与 description 部分合格（11–13 档的特征），但正文结构不合格把 D4 总分拉向 6–10 档。第 11 项值得肯定：示例中的 `scripts/create-doc.py`、`docx-js.md`、`ooxml.md` 等均以**示例代码块**形式出现、是其他 skill 的插图而非本 skill 的引用路径，处理方式正确。

---

## 8. 人机感

**正向观感**：全文语气自信、笃定，行文带有强烈的"方法论宣言"色彩——"A Skill with perfect content but poor description is useless"（第 240 行）、"brutal truth"（第 240 行）这类表述让 skill 读起来像一位严苛而专业的评审导师；D1–D8 每维都有"评分表 + 正反例 + 测试问题"三件套，示例都是真实的判断场景（Inter 字体、紫色渐变、"too AI-generated"），这些细节让人机信任度建立得很扎实。NEVER 清单（第 479–489 行）的 10 条全部是具体可执行禁令，没有任何 "be careful" 式空话——按照它自己的 D3 标准，这是 12–15 分档的表现。

**负向观感**：最大的信任损耗来自**元讽刺**——一个宣称"我审查规范遵从"的 skill 自己缺了 Workflow/Output/Scope 三段、自己的参考文件是孤儿、自己的流程图排版错乱、自己的行数 500 行踩着自己 "ideal <500" 的上限。用户在第一次读到 D5 "Poor trigger" 示例（第 344–351 行）再翻到自己文件末尾第 494–501 行时会立刻发现"它骂的就是它自己"。这对评估类 skill 的可信度是实质性伤害——它输出的评估报告里任何关于"渐进披露"或"规范遵从"的判词都会被打上问号。另外，"17+ official examples" 无出处可查，"official" 一词用得多但无引证（SPELL 才是官方文本，语料总结不是），严谨性上有水分。**Trigger 体验**：description 的 "Use when reviewing, auditing, or improving" 与 README 里的触发短语（"Review my SKILL.md"、"Score this skill"）若能合流进 description，调用体验会明显改善。

---

## 9. 可执行性

**Agent 侧（执行 skill 的人）**：

- 能做的：给 Agent 一个 SKILL.md，它按正文 D1–D8 rubrics 打分没有问题——各维度的评分表边界清晰（如 D1 红牌区 5 条、D4 三问、D6 自由光谱表），决策树（"High consequence → Low freedom"）可走通；NEVER 清单可防住 9 类常见放水。
- 做不到的：**按统一格式出报告**。没有 Output 段、没有 A–F 定级表，两次执行之间的报告结构必然漂移；**按协议流程走**——5 步协议从未被触发，Agent 大概率直接跳到评分而跳过知识增量扫描（PROC-01 的 E:A:R 比率计算依赖的协议文件不会被读）；**控制加载**——6 个参考文件无 MUST-READ / DO-NOT-Load 指令，读或不读全凭运气，而读了 evaluation-protocol.md 还会遇到截断模板和未闭合围栏。
- 结论：执行路径"评分"部分高度可用（约 8/10 可用度），"流程 + 产出"部分几乎不可执行（输出格式要靠 Agent 即兴发挥）。整体可执行性评分中下（D8 = 8/15，见第 12 节）。

**Harness 侧（评测自动化）**：

- check.py 可运行：参数校验（3 参数）、`../_shared/checker` 导入（已确认 checker.py 存在且函数签名匹配）、JSON 输出协议均正确。
- 但存在 3 个问题：(a) **零脚本检查**——`check()` 返回空字典，15 条标准全部 `judge: llm`，脚本在评测管线里是纯装饰，SCORING.yaml 的 `total_items: 15` 与 "0 script checks" 自洽，但意味着这条 skill 的自动化验证完全依赖 LLM 评审者的纪律；(b) **set_agent_output 调用顺序颠倒**——`check()`（第 20–21 行）先以路径字符串调用 `set_agent_output(agent_output)`，`main()`（第 51–53 行）再以文件内容覆盖。当前因结果为空而无实害，一旦将来有人给该 skill 加 script 检查项，会拿到路径字符串而非内容，埋雷；(c) `check(workspace, ...)` 的 workspace 参数未使用，docstring "Run all 0 script checks" 与实现一致，属知情留空而非 bug。🟡
- SCORING.yaml 缺评分聚合规则：15 条 pass/fail 如何映射到 120 分量表（或产出分数）没有定义，无权重、无阈值、无 per-category 折算——只定义了 `cap_to_0` 的 critical_failures。评测结果的可复现性依赖 runner 的外部约定。🟡

---

## 10. SCORING 交叉参考

将 SCORING.yaml 的 15 条准则与本 skill 的实际内容供给能力逐一对照（"内容供给能力"指：被调用的 Agent 在不读 README、无外部输入的前提下，仅凭 skill 自身能否满足该条）：

| 准则 | 内容供给 | 分析 |
|------|---------|------|
| SCOPE-01（识别评估请求并应用官方框架） | ✓ 基本满足 | description 与正文均明确评估对象，识别无歧义 |
| SCOPE-02（覆盖 D1–D8 八维） | ✓ 满足 | 八维全部在正文 |
| PROC-01（[E]/[A]/[R] 标注 + 比率 + 20 分制） | ⚠️ 风险 | 标注与比率只在 evaluation-protocol.md（未触发），正文仅有"计数段落分类"的弱化表述，Agent 可能只打分不标注 |
| PROC-02（D2 思维模式 vs 机制） | ✓ 满足 | D2 节完整 |
| PROC-03（D3 具体 NEVER 带 WHY 计 12–15） | ✓ 满足 | 评分锚点齐全 |
| PROC-04（D4 描述三问） | ✓ 满足 | D4 节完整 |
| PROC-05（D5 分层 + 触发器等级 + DO-NOT-Load） | ✓ 满足 | 概念完整（自身未践行是另一回事） |
| PROC-06（D6 脆弱性映射 + D7 模式识别） | ✓ 满足 | 两节完整 |
| PROC-07（D8 决策树试走/示例核对/回退） | ✓ 满足 | D8 节完整 |
| OUT-01（总分 X/120 + 等级 + 模式 + E:A:R + 结论句） | ⚠️ 风险 | 定级量表不在正文；E:A:R 的获取依赖 PROC-01 的弱化路径 |
| OUT-02（维度表 + 关键问题 + Top3 + 详评，引用行号） | ⚠️ 风险 | 模板碎片未触发，Agent 大概率自由发挥格式 |
| OUT-03（低于满分的维度都有改进建议） | ✓ 满足 | rubrics 内含"note specific improvements if score < maximum"（protocol Step 3）与正文 D8 的建议模式，正文可支撑 |
| NEG-01 / NEG-02（不注水、不放水） | ✓ 满足 | NEVER 清单 + D1 红牌区双重约束 |
| QA-01（完整读 SKILL.md、查 frontmatter、清点行数与引用、证据化） | ⚠️ 风险 | 协议在未触发的参考文件里；行数清点等 QA 动作无正文背书 |

**汇总**：15 条中 9 条内容供给充分，4 条存在依赖未触发参考文件的风险（PROC-01、OUT-01、OUT-02、QA-01），全部落在"流程与产出"侧——再次印证第 3、9 节的判断：评分能力完备，流程与产出的知识链路断裂。**若按现状跑评测，受影响条目恰好是 OUT 类（3 条中有 2 条）与 QA 类（1/1），即"报告质量"与"过程证据"两类最容易被扣分的条目**。critical_failures 三条（不读内容、无证据打分、按观感注水）有正文 NEVER 清单直接兜底，设计意图与风险结构是对称的——问题只出在"把协议藏进无人读取的 references"这一步。

---

## 11. 已知问题

按审查指令，本节跳过（已知问题已在第 4、5、7 节以"自我违例"与"合规缺口"形式分散记录，不重复列示）。

---

## 12. 综合评分（8 维 → /100）

按该 skill 自身的 D1–D8 维度与分值权重（满分 120）逐维打分，并换算为百分制。

| 维度 | 满分 | 得分 | 依据摘要 |
|------|------|------|---------|
| D1 知识增量 | 20 | 12 | rubrics、红牌/绿牌信号、D4 描述三问等是真专家内容；但第 13–74 行核心哲学（"What is a Skill"、成本算式、Tool vs Skill 表）恰踩中它自己 D1 的红牌标准（"What is [basic concept]" 节），[A]/[R] 内容占比约 20–25% |
| D2 心智模式 + 流程 | 15 | 10 | 思考框架出色（"Would an expert say I learned this the hard way?"、激活流、自由光谱）；但 5 步协议锁在未触发的截断文件里，域流程供给断链 |
| D3 反模式质量 | 15 | 11 | NEVER 清单 10 条具体且多数带理由，弱反模式反例（"Avoid making mistakes"）辨析清楚；扣分于自己成为孤儿引用与 Checkbox 模板的标本 |
| D4 规范遵从 | 15 | 7 | frontmatter 合法、description 233 字三要素齐（约 12 分档能力）；正文缺三段必备结构、name 与目录边缘性不符、触发信号非规范原文，拉回 6–10 档 |
| D5 渐进披露 | 15 | 5 | 概念教学满分，实践零分：Reference Files 为 "Poor" 级被动列表、无 MUST-READ/DO-NOT-Load、6 个参考文件 5 个是占位符、README 内容错层 |
| D6 自由校准 | 15 | 11 | 评估任务属中低自由，正文用评分表 + 阈值 + 禁令锁定，校准合理；产出环节自由度过大（无格式约束）是缺口 |
| D7 模式识别 | 10 | 6 | SCORING 声明 process，实际 500 行 Tool 形制，偏差显著；"17" 与 "17+" 口径不一 |
| D8 实用可用性 | 15 | 8 | 评分可立即执行、决策测试可走通；报告格式、定级量表、流程步骤不可得，两次执行输出必然漂移 |
| **合计** | **120** | **70** | **58.3%** |

**百分制：58.3 / 100（70/120）**。

**按它自己的定级量表**：58.3% < 60%，落入 **F 档（<60%）"Poor — needs fundamental redesign"**——一个教别人写 skill 的 skill，按自己教的尺子量自己，勉强不及格。用同一把尺子的逐维批评：D5（5/15）与 D4（7/15）是主要失分项，恰好对应"结构硬伤 × 2"；D1、D3 的中等分说明内容质量本身（评分方法论）是有真实价值的，问题集中在**组织与交付层**而非**知识层**。修复后（见第 13 节）D4 可回 11–13、D5 可回 11–13、D8 可回 11–13，总分有望到 90–95/120（75–79%，C 档），已修复形态具有 B–A 档的潜力。

---

## 13. 修复建议（🔴 必修 / 🟡 应修 / 🟢 可修；含文件与行号、工作量）

### 🔴 必修（影响规范合规与产出可用性，合计中等工作量）

1. **正文补 `## Workflow / Process` 段**（SKILL.md，建议插入第 11 行 "# Skill Judge" 之后或第 76 行分隔线之前）。把 evaluation-protocol.md 的 5 步协议整体移入正文（或正文写出浓缩版 + 明确 MUST-READ 指向完整版），并在每步挂上对应 D 维度锚点与参考文件触发条件。工作量：中（约 60–80 行新增，含 5 步的逐步示例）。
2. **正文补 `## Output Format` 段**：把 README.md 第 146–167 行的完整报告模板移入正文（含 A–F 定级量表与百分比区间，量表目前只存在于 README 与 protocol 两处不可达位置）。同时删除 references 下 5 个模板碎片文件或将它们合并为单一 `references/report-template.md` 并在正文 Workflow 第 5 步加 "MANDATORY - READ" 触发。工作量：中。
3. **正文补 `## Scope / Limitations` 段**：明确不适用的对象（MCP server 配置、tool 定义评估、非 SKILL.md 文件）、单文件 vs 多文件 skill 的适用差异、对"无 references 的简单 skill"的评分特例归位到本段而非 D5 注释。工作量：小。
4. **修复 evaluation-protocol.md 的截断与围栏**（references/evaluation-protocol.md 第 52–54 行）：闭合 ```markdown 围栏；若报告模板移出（建议 2），此处 Step 5 改为指向正文 Output Format 段的一句话指引。工作量：小。
5. **Reference Files 清单升级为带触发条件的加载表**（SKILL.md 第 494–501 行）：为每个参考文件补 WHEN（如 "protocol：首次执行评估前 MUST-READ"；"summary/dimension-scores：生成报告时对照"），并给用不到的场景加 "DO NOT Load" 行。工作量：小。

### 🟡 应修（影响内部一致性、触发率与自我形象，合计小工作量）

6. **修复 SKILL ACTIVATION FLOW 错乱图**（SKILL.md 第 231–238 行）：将三行错位文本重排为对齐的代码围栏块（` ```text `），恢复 "User Request → Agent sees ALL descriptions → Decides which of skills to activate (only descriptions, not bodies!)" 的完整语义。工作量：极小（纯排版）。
7. **D2 命名统一**：三处（SKILL.md 第 112 行 / references/dimension-scores.md 第 6 行 / SCORING.yaml 第 33 行 PROC-02）统一为 "Mindset + Procedures" 或协商一致后的单一名称。工作量：极小。
8. **description 强化触发**（SKILL.md 第 3 行）：将 "Use when reviewing..." 改为规范原文信号 "Use when the user asks to review, audit, evaluate, or score a skill or SKILL.md..."，并追加 KEYWORDS（evaluate this skill、skill quality、score、audit skill）。工作量：极小。可顺带补 argument-hint（如 `[skill path | SKILL.md path]`）。
9. **9 大失败模式下沉进正文**（README.md 第 102–114 行 → SKILL.md）：在 NEVER Do When Evaluating 节后加一小节"Common Failure Patterns"，或至少把 The Orphan References 等与 D5 触发器表对应起来。工作量：小。
10. **核心哲学瘦身**（SKILL.md 第 13–74 行）：按它自己的 D1 标准把 "What is a Skill"、成本算式（$10,000–$1,000,000+）、Tool vs Skill 表压缩为 2–3 行激活级陈述，预计净省 40–60 行，目标 500 → 440 行以内，兑现 "ideal < 500" 与 Process 模式 ~200 行的自承诺（若行数仍超 300，建议把 D 维示例代码块整段移入 references，正文留索引）。工作量：小。
11. **check.py 顺序修正**（check.py 第 18–21、48–53 行）：在 `check()` 内不调 `set_agent_output`，统一由 `main()` 读文件后调用一次；对 agent_output 文件不存在的情况补分支。工作量：极小。
12. **SCORING.yaml 补聚合规则**（SCORING.yaml 第 3–4 行附近）：声明 15 条到 120 分的映射（或加权、或 pass 数阈值），消除评测结果对 runner 外部约定的隐式依赖。工作量：小。

### 🟢 可修（打磨项）

13. **name 与目录名对齐**（SKILL.md 第 2 行）：如语料惯例允许 NNN 前缀剥离则无需改；若严格执行 SPELL §1.1，将目录/name 统一（更建议改 name 为与目录一致）。工作量：极小。
14. **"17" 与 "17+" 口径统一**（SKILL.md 第 410 行 / 第 3 行）：统一为 "17 official examples" 或 "17+"。工作量：极小。
15. **README 与 SKILL.md 去重**：将 README 收敛为纯人类导读（指向正文），避免同一方法论两处维护、两处漂移（当前 9 大失败模式即漂移案例）。工作量：小。

---

## 附录 A：自我镜像映射（该 skill 用自己的尺子量自己）

| 自己的判词 | 出处 | 对自己的适用 |
|-----------|------|-------------|
| "What is [basic concept]" 段 → D1 红牌 ≤5 | SKILL.md 第 92 行 | "What is a Skill?" 节（第 15–34 行）同构 |
| Poor 触发器："References listed at the end, no loading guidance" | SKILL.md 第 322 行 | 第 494–501 行 Reference Files 即原样 |
| The Orphan References：参考文件从不被加载 | README.md 第 108 行 | 6 个参考文件全部无触发 |
| The Checkbox Procedure：机械步骤无思维框架 | README.md 第 109 行 | 5 个模板碎片 = Checkbox 模板 |
| "a 43-line Skill can outperform a 500-line one" | SKILL.md 第 483 行 | 本文件恰好 500 行 |
| Ideal: < 500 lines（D5 层 2） | SKILL.md 第 305 行 | 500 行 = 未小于 |
| Process 模式 ~200 行 | SKILL.md 第 417 行 | 500 行，自报 process |

## 附录 B：描述字段全文（供复核对）

> Evaluate Agent Skill designs against official specifications and best practices. Use when reviewing, auditing, or improving SKILL.md files and skill packages. Provides multi-dimensional scoring and actionable improvement suggestions.

（233 字符；第三段继续 WHAT；触发信号 "Use when reviewing..." 为 "Use when the user..." 变体，缺主语 "the user"。）

## 附录 C：审查结论一句话

知识层扎实（评分方法论可打 8–9 分水平），交付层断裂（流程、产出、边界三段全缺，参考文件自锁成孤儿）——按它自己的 F 档定义（"needs fundamental redesign"），本次审查判定 **70/120（58.3%）F 档**，修复优先级集中在第 13 节 🔴 五项，修复后预期升至 C 档，具备 B–A 档潜力。
