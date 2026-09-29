# REVIEW — 241-readme-i18n

## 1. 审查概览

- 审查对象：`D:\SkillIF\skill-experiment\complex-skills\241-readme-i18n`
- 审查日期：2026-08-06
- 审查方法：逐一读取该目录下全部 5 个文件（SKILL.md、SCORING.yaml、check.py、references 下 2 个 reference 文件），并读取共享检查库 `D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py` 与 `CHECKER-LIBRARY.md`，以核实 check.py 中每个脚本检查的实际语义（glob 展开、正则转义、工具日志解析、输出文本判定）。
- 审查维度：技能内容质量、可操作性、触发设计、引用文件质量、评分体系（SCORING.yaml）设计、脚本实现（check.py）正确性、描述与检查之间的一致性、负面约束与关键失败模式的覆盖。
- 审查标准：以 SkillIF 测评矩阵的测量有效性为第一视角——不仅评估"技能写得如何"，更评估"评分装置能否真实测量 agent 对技能的遵从度"。
- 总体结论：技能本体（SKILL.md + 两个 reference）质量较高，指令明确、正反清单齐全、可操作性强的本地化工作流设计；但评估装置（SCORING.yaml + check.py）存在多处实质缺陷，其中两处属于"恒真/恒错"级别的硬伤（PROC-06 恒真假阳性、glob 模式会命中源文件 README.md），会直接扭曲测量结果，建议优先修复。
- 综合评级：技能内容 A，评估装置 B-，整体 B+（详见第 12、13 节问题清单与结论）。

## 2. 文件清单与目录结构

该技能目录结构如下（共 5 个文件）：

| 文件 | 行数 | 角色 |
|------|------|------|
| `SKILL.md` | 178 | 技能主文件：frontmatter + 完整工作流 |
| `SCORING.yaml` | 139 | 评分标准声明：13 项 criteria + 4 项 critical_failures |
| `check.py` | 79 | 脚本检查实现：7 项 script 判定 |
| `references/language-selector-reference.md` | 80 | 语言选择器的规范块、放置规则与更新规则 |
| `references/preservation-checklist.md` | 27 | 翻译前后的结构保留清单 |

- 目录结构简洁、职责分明：主文件 + 声明式评分 + 可执行检查 + 两个定向 reference，无冗余文件。
- 与 240-design-doc 相比，本技能没有 README.md（分发式文档），也没有示例目录——对 SkillIF 测评用途而言更精简。
- reference 文件名即职责名（"preservation-checklist"、"language-selector-reference"），SKILL.md 第 53、120 行以相对链接显式指向它们，且明确规定了"何时读"，这是良好的引用设计。
- 全目录合计约 503 行正文，体量适中——既没有单文件巨型化（可读性风险），也没有过度拆分（检索成本风险）。
- 文件间依赖关系：SKILL.md（第 53、120 行）→ references 两个文件；SCORING.yaml（pattern/check 声明）→ check.py（实现）；check.py → `_shared/checker.py`（共享库）。依赖单向、无环，符合库的约定。
- 版本线索：目录编号 241 与 240-design-doc 相邻，二者共享同一套 SCORING/check.py 模板（import 段逐字相同），属于同一批"过程型技能 + 自动评分"实验批次。
- 未发现任何隐藏文件、临时文件或与测评无关的残留（如 .git、__pycache__ 之外的垃圾文件），目录整洁。
- check.py 与 SCORING.yaml 的命名、目录位置符合本库约定（_shared/checker.py 为共享依赖），可被 runner 直接调用。

## 3. 元数据与触发条件分析

- frontmatter 中 `name: readme-i18n` 为 kebab-case，与目录名一致，命名规范。
- `description` 的触发词覆盖度良好，逐词分析如下：
  - "translate a repository README"——翻译类任务；
  - "make a repo multilingual"——多语言化任务；
  - "localize docs"——泛化本地化表述；
  - "add a language switcher"——选择器任务（本技能的核心差异化能力）；
  - "internationalize the README"——i18n 措辞变体；
  - "update localized README variants"——增量更新场景（对应 Example 3）。
- 六个触发短语覆盖了任务的绝大多数自然语言表达方式，且覆盖"更新既有变体"这一容易被漏判的场景——很多技能的触发设计只覆盖"从零翻译"，漏掉"增量维护"。
- 触发边界问题：SKILL.md 正文第 16 行明确划界 "This skill is for multilingual README workflows, not general website/app i18n"，但该负向边界**没有**出现在 description 中。触发阶段（agent 仅读 description）时，用户说 "localize our website" 之类的话可能被误触发。
- 建议：在 description 末尾补一句负向限定（description 当前约 180 字符，加一句后仍在安全长度内），例如 "Not for general website or application internationalization."。
- description 限定 "in a GitHub-style repository"，暗示 GitHub Flavored Markdown 专属语法（alerts、锚点 slug 等）是技能核心关切，与正文一致。
- 评分侧 SCOPE-01 的 description 与 question 与 description 触发词一一对应（"translate README, make repo multilingual, add language switcher, update localized variants"），触发设计与评分设计对齐良好。
- SCOPE-02 将"目标语言来源"限定为请求或仓库既有约定（文件、选择器、issues），并强制"不发明语言、ask once"——这条防线同时出现在正文（第 28 行）与评分（SCOPE-02）中，双重约束。
- 结论：触发覆盖优秀，唯一缺口是负向边界未进 description。

## 4. SKILL.md 信息架构与正文结构

- 正文结构完整：简介与默认任务 → Inputs → Defaults And Decision Rules → Workflow（8 步）→ Output → Maintenance Note → Example Prompts → Common Mistakes。
- 该结构覆盖了指令性技能所需的全部要素：输入契约、决策规则、步骤化流程、交付物定义、维护策略、示例、常见错误——完整性在本库复杂技能中属于第一梯队。
- 与评分维度的映射：13 项 criteria（2 scope + 7 process + 2 output + 2 negative）几乎都能在正文中找到对应的指令段落，正文与评分体系是同构的，这是本技能的一个突出优点。逐段映射如下：

| 正文段落 | 对应评分项 | 映射质量 |
|----------|------------|----------|
| Inputs（第 18-28 行） | SCOPE-02（目标语言来源）、PROC-01（源确立） | 直接对应 |
| Defaults And Decision Rules | PROC-01、PROC-06、PROC-07、NEG-02 | 9 条规则分散映射 4 项 |
| Workflow 步骤 2 | PROC-02、PROC-03 | 指令即检查的证据来源 |
| Workflow 步骤 3 | NEG-01、CF-02 | 双表与 CF 对应 |
| Workflow 步骤 5 | PROC-05、CF-01 | 对应 |
| Workflow 步骤 7 | PROC-07、CF-03 | 对应 |
| Workflow 步骤 8 | OUT-01 | 描述对应、检查不对应 |
| Output 节 | OUT-02 | 三件套与 question 对应 |
| Maintenance Note | NEG-02 | 直接对应 |
| Example Prompts / Common Mistakes | 全部（行为示范） | 间接支撑 |
- 篇幅 178 行，中等偏长但分层清晰（1-8 步编号 + 加粗小节），不存在"墙式文本"问题；逐段阅读发现无冗余段落，每句话都有指令价值。
- "Defaults And Decision Rules" 共 9 条决策规则，每条都是"可执行的断言"（如 "Update an existing language selector in place. Do not duplicate it."、"Translate only human-language content."），而不是模糊建议——这是触发类技能最需要的写法。
- 决策规则之间无冲突，且与 Workflow 步骤一一呼应（规则 4↔步骤 4、规则 5↔步骤 7、规则 6↔步骤 3），正文内部自洽。
- Output 节明确了交付物三件套（每个目标语言一个变体 + 全变体选择器 + 给用户的简短说明），与 OUT-02 的 llm 判定问题（"报告创建/更新文件、假设、未翻译术语"）直接对应。
- Maintenance Note 明确"以 diff 方式增量更新而非整文件重写"，对应 NEG-02；该节的存在意味着技能考虑了长期使用场景，而非一次性任务模板。
- 三个 Example Prompts 覆盖了三种典型任务形态（全新翻译、多语言化、既有变体增量），对 agent 起很强的示范作用；Common Mistakes 6 条均对应真实失败模式（围栏被译、选择器重复、锚点忘记重写、徽章 URL 被改、乱序）。

## 5. 工作流指令质量分析

按 8 个步骤逐一评估：

### 5.1 步骤 1：建立源 README 与语言

- 默认路径、语言推断、目标语言来源（请求或既有模式）、术语清单四要素齐全。
- "ask once. Do not invent target languages" 是防幻觉的关键约束，与 SCOPE-02 对齐。
- 不足之处：对"源语言推断"给出什么信号特征（如 README 中代码注释语言、issue 语言、仓库语言统计）没有提示，依赖 agent 常识——可接受，因为推断本身是通用能力。

### 5.2 步骤 2：翻译前审计 Markdown 结构

- 明确要求 "Read the source README once as structure, not prose"，并显式要求打开 preservation-checklist。
- 该指令与 PROC-03 的脚本检查（必须先读 checklist 再写文件）形成因果耦合，是"指令驱动检查"的正面范例。
- 8 类易损元素清单（标题、徽章行、表格、HTML、alerts、围栏、锚点、相对链接）与 checklist 表格 12 行完全对齐。
- 额外要求"如果已有本地化兄弟文件，先检查它们再选文件名或选择器风格"——避免与既有约定冲突，直接预防了 Example 3 场景的错误。

### 5.3 步骤 3：只翻译散文层

- 正面清单（可译：段落、列表项散文、表格单元格散文、HTML 可见文本、alt 文本、选择器标签）+ 负面清单（不可译：围栏代码、行内代码、命令、flags、env vars、URL、路径、标识符、徽章 URL）双表并列，覆盖面完整。
- "When in doubt, preserve the literal token and translate the surrounding sentence instead." 提供了原则性兜底，这比穷举规则更稳健——LLM 在边界情况下的默认行为被定向为"保守"。
- 徽章 alt 文本翻译的例外条件写得很精确："only when the change does not require changing the badge URL, query params, or image source"——直接命中 CF-02 的典型诱因。

### 5.4 步骤 4：保持结构

- 标题层级、围栏数量、表格形状、列表嵌套、HTML 包装、Markdown 注释六项要求，与 preservation-checklist 的表格行一一呼应。
- "Keep the same number of code fences unless the user explicitly asks to rewrite examples" 给出了唯一例外条件，无歧义。
- 相对链接的例外（指向本地化兄弟文件）被单独列出，避免"绝对禁止改动"的误读。

### 5.5 步骤 5：重写锚点与依赖锚点的链接

- 这是本地化工作中最易错、最难自动验证的环节，指令给出了明确规则：重写每个同文件 `(#...)` 链接使其匹配本地化标题 slug；保留自定义显式锚点 `<a id="...">`；逐一验证锚点目标存在。
- "Prefer a small heading wording adjustment over a broken anchor" 给出了冲突时的解决优先级，与 CF-01（锚点断链 cap_to_0）呼应。
- 不足：未提供 GitHub 对中文/非 ASCII 标题的 slug 生成规则（GitHub 对 CJK 标题的锚点生成与 ASCII 标题不同），完全依赖 agent 的知识——中等程度缺口，建议在 checklist 补一小节。

### 5.6 步骤 6：写兄弟文件

- 默认 `README.<bcp47-tag>.md` 模式给出三个示例（zh/es/fr），同时允许并鼓励保留仓库既有模式——规则无歧义，与 PROC-06 对应。
- bcp47-tag 的提法比常见的 "language code" 更准确（支持 zh-CN 等区域标签），体现领域精确性。

### 5.7 步骤 7：插入或更新语言选择器

- 先读 reference 再动手；放置位置（标题、徽章、hero 图、简介块之后）明确。
- 原位更新优先；新增时使用规范标记注释保证确定性可更新——"README-I18N:START/END" 标记方案是该技能的设计亮点（让后续 run 能以字符串匹配方式确定性更新）。
- 缺口：对"既有无标记选择器"是否应补标记存在歧义（reference 说 "normalize it in place"，SKILL 说 "if you add a new selector, use the canonical marker comments"），而 PROC-07 只认标记字符串。详见第 12 节问题 P2-6。

### 5.8 步骤 8：最终验证

- 7 项自检清单（文件名模式、恰一个选择器、围栏计数、URL 与相对链接、锚点解析、结构一致性）。
- 注意：OUT-01 的脚本判定只检查输出文本中的英文单词 "verif(y|ied|ication)"，并不验证这些自检是否真的发生（详见第 9 节）——步骤 8 写得好，但测量层没有承接。

8 个步骤的整体评估汇总：

| 步骤 | 指令清晰度 | 可检查性 | 主要风险点 |
|------|-----------|----------|------------|
| 1 建立源与语言 | 高 | llm 可判（SCOPE-02/PROC-01） | 语言推断依赖常识 |
| 2 审计结构 | 高 | 脚本可判（PROC-03 代理） | 只读清单≠遵守清单 |
| 3 只译散文层 | 高 | 弱（NEG-01 方向错误） | URL/围栏被改检测缺失 |
| 4 保持结构 | 高 | 弱（PROC-04 存在性） | 无法检测围栏计数变化 |
| 5 锚点重写 | 中 | 弱（PROC-05 存在性） | CJK slug 规则缺失 |
| 6 命名模式 | 高 | 恒真（PROC-06） | 检查失效 |
| 7 选择器 | 高 | 弱（PROC-07 字符串） | 无标记选择器歧义 |
| 8 最终验证 | 高 | 弱（OUT-01 关键词） | 检查与行为脱钩 |

- 整体评价：8 个步骤的指令质量均在线，全部为"确定性指令 + 例外条件"结构；但 8 个步骤中只有 2 个（步骤 1、2）有可靠测量承接，其余 6 个步骤的测量均为代理性或失效——这正是本技能评估装置需要优先修复的原因。

## 6. 引用文件审查

### 6.1 references/preservation-checklist.md（27 行）

- 12 行三列表格（Element / Translate? / Preserve exactly / What to verify），覆盖标题、段落列表、行内代码、围栏、徽章、图片、表格、HTML、GitHub alerts、相对链接、同文件锚点、HTML 注释共 12 类元素。
- 每行的三列设计巧妙："是否翻译"+"原样保留什么"+"验证什么"——同时服务于翻译决策和事后检查，是浓缩度极高的参考。
- 行内代码行的 "Preserve exactly" 列出 "Commands, flags, paths, env vars unchanged"，与 SKILL.md 负面清单一致。
- GitHub alerts 行要求保留 `[!NOTE]` 标记、只译正文——覆盖了 GitHub 专属语法这一易错点。
- "Fast Pass" 提供 5 条快速扫描项（围栏计数、`](#` 扫描、README. 链接、http 扫描、反引号抽查），可直接转译为人工/脚本检查动作——本库中少见的"自带验证步骤"的 reference。
- 小问题：表格第 11 行 "Same-file anchors" 的 "Translate?" 列为 "Link text sometimes"，与 SKILL.md 第 5 步规则一致，无矛盾。

### 6.2 references/language-selector-reference.md（80 行）

- 完整覆盖：放置规则（标题簇之后、全变体一致）→ 规范块（含 `<!-- README-I18N:START -->` / `<!-- README-I18N:END -->` 标记）→ 规则 4 条（当前语言加粗不链接、其他语言链接、使用 autonym、全文件顺序一致）→ 更新既有选择器的 3 条规则 → 文件名模式 → 3 个变体示例。
- 3 个变体示例（README.md / README.zh.md / README.es.md）逐文件演示"当前语言加粗"的正确形态，消除了唯一的排版歧义。
- 与 PROC-07 检查字符串 "README-I18N:START" 精确一致，说明参考设计者有意识地让"检查锚点字符串"与"规范标记"对齐——这在本库中并不常见，值得肯定。
- 使用 autonym（"汉语"而非 "Chinese"）的约定与"不翻译选择器标签之外的人类语言"的边界一致，自洽。
- 小问题：更新规则第 2 条 "normalize it in place" 未说明是否应同时补上规范标记，导致与 PROC-07 的严格字符串检查之间出现解释空间（详见第 12 节 P2-6）。

### 6.3 两个 reference 的协同评估

- 分工明确且互补：preservation-checklist 管"翻译决策与结构保全"，language-selector-reference 管"选择器这一最易出错的组件"，中间无重叠也无遗漏。
- 与 SKILL.md 的引用契约一致：SKILL.md 在步骤 2 与步骤 7 分别指向两个文件，恰好在"动手前"的时机点触发阅读——阅读时机设计合理。
- 与评分检查的耦合：preservation-checklist 是 PROC-03 脚本检查的必读文件，language-selector-reference 中的标记字符串是 PROC-07 的检查锚点——两个 reference 都承担了"检查证据来源"的职责，这在其他技能中少见。
- 信息量评估：两个文件合计 107 行，均为高密度参考（无铺垫、无重复），读一遍的成本低，这正是"供 agent 即时查阅"的参考文件的正确形态。

## 7. 评分体系审查（SCORING.yaml）

- `pattern: process`，`total_items: 13`，与 criteria 实际数量一致（2+2+7+2=13）。
- 判定方式分布如下表：

| 类别 | 数量 | llm 判定 | script 判定 |
|------|------|----------|-------------|
| scope | 2 | 2（SCOPE-01/02） | 0 |
| process | 7 | 2（PROC-01/02） | 5（PROC-03~07） |
| output | 2 | 1（OUT-02） | 1（OUT-01） |
| negative | 2 | 1（NEG-02） | 1（NEG-01） |
| 合计 | 13 | 6 | 7 |

- 脚本可自动判定 7/13（约 54%），在本库复杂技能中属于可判性较高的设计（对比 240-design-doc 仅 1/14 可脚本化）。
- 13 项 criteria 全表（id / 类别 / 判定方式 / 检查要点）：

| id | 类别 | 判定 | 检查要点 |
|----|------|------|----------|
| SCOPE-01 | scope | llm | 开场信息框定为 README 本地化任务 |
| SCOPE-02 | scope | llm | 目标语言来自请求/既有约定，ask once |
| PROC-01 | process | llm | 源 README 确立、源语言识别 |
| PROC-02 | process | llm | 翻译前结构审计并参考 checklist |
| PROC-03 | process | script | Read-before-Write（README.md + checklist） |
| PROC-04 | process | script | 本地化文件含代码围栏 |
| PROC-05 | process | script | 本地化文件含 `](#` 锚点链接 |
| PROC-06 | process | script | README.*.md 文件存在 |
| PROC-07 | process | script | 本地化文件含 README-I18N:START |
| OUT-01 | output | script | 输出文本含 "verif(y\|ied\|ication)" |
| OUT-02 | output | llm | 报告文件、假设、未翻译术语 |
| NEG-01 | negative | script | 本地化文件含 http(s) URL |
| NEG-02 | negative | llm | diff 更新而非整文件重写 |

- 逐项点评：
  - SCOPE-01/02：question 措辞具体（"opening message"、"file inventory it inspects"），证据来源明确，llm 判定可操作。
  - PROC-01：description 与 question 均聚焦"source-of-truth 确立与源语言识别"，判定面窄而准，避免 llm 判定大而化之。
  - PROC-02：question 要求 agent "referencing the preservation checklist" 且证据指向 "Reads of README.md and references/preservation-checklist.md"——llm 判定与脚本检查（PROC-03）共享同一证据源，双重保险设计良好。
  - PROC-03：description 声称"只有散文层被翻译、非散文原样保留"，脚本却只检查 Read-before-Write 顺序——代理性检查，见第 9 节。
  - PROC-04/05/07：三个 script 检查均为 file_contains + 存在性代理，存在多项缺陷（见第 8、9 节）。
  - PROC-06：file_exists + glob，恒真假阳性（见第 8 节）。
  - OUT-01：description 描述"执行了最终验证"，脚本却只查输出文本中的英文单词 "verif(y|ied|ication)"（见第 9 节）。
  - OUT-02：llm 判定，question 要求报告"创建/更新文件、假设、未翻译术语"，证据指向 "Agent's final response text"，判定面合理。
  - NEG-01：负面合规项却用"URL 存在"作为通过条件，代理方向与意图相反（见第 9 节）。
  - NEG-02：llm 判定，question 依赖"源 README 变化"的二次触发场景——若测试夹具只有单轮任务，该项实际不可判定，属于夹具依赖项。
- critical_failures 4 项（CF-01 锚点断链 / CF-02 非散文内容被译 / CF-03 选择器重复 / CF-04 结构偏离）覆盖了该任务的核心致命风险，且与 NEG/OUT 项形成两级惩罚结构（违规 vs 致命违规），设计合理。
- 但 YAML 中 critical_failures 未声明判定方式（llm 还是 runner 内置），实际执行时需依赖 runner 约定；CF-02 与 NEG-01 范围重叠但权重不同，语义上可接受。

## 8. check.py 实现审查

- 入口与文档字符串正确（`python check.py <workspace> <tool_log> <agent_output>`），调用 `_shared/checker.py`，输出 `{criterion_id: bool}`，符合本库 runner 约定。
- 严重问题 P1-1/P1-2：`localized_readme = os.path.join(workspace, "README.*.md")` 传入 file_contains/file_exists。核查 checker.py 源码确认三件事：
  1. Python glob 的 `*` 可以匹配空串，因此 `README.*.md` 会同时命中源文件 `README.md` 本身，而不仅是本地化变体；
  2. `file_contains` 对 glob 路径只检查第一个匹配文件（`matches[0]`，glob 结果不保证排序），且 `file_exists` 只要任意匹配即真；
  3. 因此：PROC-06 在源 README.md 存在时**恒为真**——即使 agent 一个本地化文件都没创建也通过，属于硬性假阳性；PROC-04/05/07/NEG-01 实际检查的可能是源文件 README.md 而不是本地化产物。
- 多变体场景影响：工作区同时存在 README.zh.md 与 README.es.md 时，所有 file_contains 检查只落在 glob 首匹配的一个文件上，其余变体完全不检查——与 OUT-01 声称的 "every README variant contains exactly one selector" 的能力要求（遍历全部变体）存在结构性缺口。
- `tool_log_read_before_write` 的旁路条件：checker.py 中 `first_write_ts is None`（日志中无任何 Write/Edit）时顺序约束失效，读到即通过。若 agent 用 Bash（cp/sed/echo）而非 Write/Edit 工具写文件，或测试场景本就不要求写文件，PROC-03 会无条件通过——代理假设（"读了清单就会遵守"）进一步弱化。
- 模式匹配细节：reads 模式 "README.md" 通过 re.search 匹配 Read 调用的 args 序列化字符串，可正确匹配绝对路径中的子串；"references/preservation-checklist.md" 同理，Windows 反斜杠路径亦可命中——无兼容问题。
- SCORING.yaml 声明的 `${SOURCE_README}` / `${LOCALIZED_README}` 变量在 check.py 中完全未使用（路径全部硬编码），声明层与实现层存在两套真相源，建议明确以 check.py 为权威。
- 模板残留：import 了 12 个未使用的 checker 函数（file_valid_json、json_field_*、timestamp_*、tool_log_contains、tool_log_order、output_not_contains 等），与 240-design-doc 的 check.py 完全相同——是共享模板的复制痕迹，不影响正确性但增加噪声。
- `main()` 中 `set_agent_output` 在 check() 内和 main() 内各调用一次，冗余但无害。
- 无路径存在性保护：workspace 不存在时各 file 检查返回 False，行为可接受；agent_output 文件不存在时输出为空字符串，output_contains 返回 False，行为确定。
- 每个脚本检查与 checker 函数签名的对应关系核实如下（对照 CHECKER-LIBRARY.md）：
  - PROC-03 → `tool_log_read_before_write(reads, require_all=True)`：reads 模式以 re.search 匹配 Read 调用的 args 序列化文本；"README.md" 模式可被包含该子串的任何路径命中（含 README.md 本身），"references/preservation-checklist.md" 模式同理。
  - PROC-04/05/07/NEG-01 → `file_contains(path, pattern)`：pattern 按 Python re 语义编译（re.MULTILINE）；"```" 模式无转义问题；"\\]\\(#" 在 Python 字符串字面量中正确折叠为 `\]\(#`。
  - PROC-06 → `file_exists(path)`：支持 glob，任意匹配即真——这是恒真问题的根源。
  - OUT-01 → `output_contains(pattern)`：对完整 agent 输出做 re.search（MULTILINE），大小写敏感，无单词边界——"verification" 之外任何含该子串的单词（如 "verified"）都会命中，代理性极强。
- 正则转义核对结论：check.py 内部 7 处 pattern 的转义全部正确；但 SCORING.yaml 中 PROC-05 的 `'\\]\\(#'` 与 240 技能 OUT-02 的 `'draw\\.io'` 存在同类问题——YAML 单引号标量不处理反斜杠转义，直接作为正则时双重反斜杠会匹配字面量反斜杠而非点号。两个技能均需统一 YAML 与 check.py 的表示（详见 P1-5）。
- 命名约定：`localized_readme` 变量名暗示"单数文件"，与 glob 的多变体语义不符，是"按单文件思维写多变体检查"的代码气味。

## 9. 描述与脚本检查的一致性分析

对 7 个 script 项逐一比对"description 声称的行为"与"脚本实际检查的内容"：

| 项 | description 声称 | 脚本实际检查 | 偏差类型 |
|----|------------------|--------------|----------|
| PROC-03 | 只翻译散文层，围栏/行内代码/URL 原样保留 | 先读 README.md 与 checklist 再写（tool_log_read_before_write） | 代理性检查：读了≠遵守；且无 Write/Edit 时恒通过 |
| PROC-04 | 结构保留：同层级、同围栏数、同表格形状 | 首个 glob 匹配文件包含 "```" | 存在性≠计数；可能检到源文件；源 README 无围栏时误判失败 |
| PROC-05 | 锚点重写并验证可解析 | 文件包含正则 `](#` | 无法验证"可解析"；源 README 无内部锚点时误判失败 |
| PROC-06 | 兄弟文件遵循命名模式 | file_exists("README.*.md") | 恒真：源文件 README.md 自身即匹配 glob |
| PROC-07 | 选择器原位更新、不重复、当前语言强调 | 文件包含 "README-I18N:START" | 字符串存在性代理；无法检测重复选择器；与"既有无标记选择器"路径有歧义 |
| OUT-01 | 执行了最终验证（7 项自检） | 输出文本含英文词 "verif(y\|ied\|ication)" | 关键词代理：写中文"验证"即误判失败；与验证行为无关 |
| NEG-01 | URL/徽章未被改动 | 文件包含 `https?://` | 方向性错误：存在≠未突变，改写过的 URL 同样通过 |

- 结论：7 项脚本检查中 5 项存在实质性的描述-检查偏差；其中 PROC-06 为恒真假阳性，NEG-01 为方向错误的弱代理，OUT-01 为语言敏感的弱代理。
- 偏差方向分析：大部分检查偏向"容易通过"（宽松代理），意味着测量到的通过率会系统性偏高；少数检查（OUT-01 的英文关键词、PROC-04/05 的夹具依赖）可能误杀合规 agent——两种偏差方向同时存在，矩阵解读时需要区分。
- 对测评实验的影响：PROC-03~07 的高通过率并不反映 agent 的真实能力，只反映代理检查的结构性盲区；在 SkillIF 矩阵分析中应将 PROC-03~07 的脚本项标注为"代理性证据"，其得分应与 llm 项（SCOPE/PROC-01/02/OUT-02/NEG-02）分开解读。
- 值得肯定：llm 项的 question 全部引用正文的具体指令（"small heading wording adjustment"、"ask once"、"diffing the changed prose"），说明评分设计者确实以技能内容为基准写作了判定问题——一致性问题集中在 script 层而非 llm 层。

## 10. 负面约束与关键失败模式分析

- NEG-01（不翻译/不改写 URL）：脚本实现方向错误（见第 9 节），且该 item 只配了 script、无 llm 兜底；实际防变异能力为零。若想真正检测 URL 突变，应改为工具日志层面的内容比对（如对比源文件与输出文件的 http 链接集合），或补 llm 判定。
- NEG-02（源变化时 diff 更新而非重写）：llm 判定，question 合理，但依赖测试夹具提供"源变化"的二次触发场景——若夹具只有单轮翻译任务，NEG-02 实际无法被判定（无变化可 diff），应标记为条件可判项。
- CF-01（锚点断链）与 CF-02（非散文被译）是此类任务最典型的两个失败，cap_to_0 权重恰当；CF-03（选择器重复）与 CF-04（结构偏离）同样恰当。
- 致命失败与脚本检查的能力缺口：CF-04 声明 "changed fence count" 会 cap_to_0，但脚本（PROC-04 存在性代理）无法检测围栏数量变化，只能依赖 llm——CF 层的能力与脚本层的能力不匹配，意味着 CF-04 的实际执行率取决于 runner 是否实现了 CF 判定。
- CF-02 与 NEG-01 的覆盖重叠：同一行为（URL 被改）既是 NEG 违规又是 CF 致命失败，但两者判定依据不同（NEG-01 靠脚本存在性检查、CF-02 靠人工/llm）——重叠本身合理，但检查能力的不对称使"该失败是否被记录"取决于判定路径。
- 负面约束整体判断：规则定义层面完善（负面清单 + 4 CF），执行层面薄弱，是本技能评估装置的最大短板；技能内容本身对负面行为的预防写得很好，但测量层没有承接这些预防。

## 11. 优点总结

- 技能内容质量高：决策规则 9 条均为可执行断言；"ask once / 不发明目标语言 / 有疑问时保留字面量"等反幻觉约束直接对抗 LLM 的典型失败模式。
- 引用文件设计是本库范例：SKILL.md 显式规定"何时读哪个 reference"，preservation-checklist 的"是否翻译/保留什么/验证什么"三列结构在信息密度上堪称模板。
- 规范标记设计（README-I18N:START/END）让选择器更新具备确定性，是可测试设计（testable design）的正面案例——字符串标记与检查字符串精确对齐。
- 评分维度与正文同构：13 项 criteria 几乎全部能在 SKILL.md 中找到对应指令，评估可追溯性强。
- 脚本可判性 7/13（54%），高于 240-design-doc（7%），证明该技能的评估结构设计更先进。
- 标题、锚点、徽章、表格、alerts、HTML 等 GitHub 生态特有的细节被系统性覆盖，体现领域知识深度。
- 双表（可译/不可译）加原则性兜底（"when in doubt, preserve the literal token"）的写作方式，是给 LLM 的指令中"确定性与鲁棒性兼得"的范本。
- CF 列表与正文 Common Mistakes 高度呼应，技能作者对失败模式的认知是系统的而非零散的。
- 示例设计质量：三个 Example Prompts 分别对应"全新翻译 + 保护性要求""多语言化 + 锚点 + 选择器联动""既有变体增量 + 原位更新"三种难度梯度，且每个示例都内嵌了技能的核心规则（badge URLs 保持不变、anchor links 保持可用、不重复选择器），示范即约束。
- 语言与措辞：全文无歧义代词、无"should consider"式弱指令；祈使句占比高，符合"指令性技能"的文体要求。
- 领域深度：对 GitHub 生态的细节（shields 徽章 URL 机制、`> [!NOTE]` alerts、`(#anchor)` 链接生成、HTML 显式锚点、autonym 命名）的处理说明本技能经过了真实 README 本地化实践的检验，而非从模板生成的表面技能。
- 与实验设计的契合度：该技能正好承载 SkillIF 矩阵中"触发器显隐 × harness 类型"的测试需求——其 description 触发词密集、工作流依赖多文件读写，适合作为过程型技能的实验样本。

## 12. 问题清单

| 编号 | 级别 | 位置 | 问题 | 影响 | 建议 |
|------|------|------|------|------|------|
| P1-1 | P1 | check.py:45 + SCORING PROC-06 | file_exists("README.*.md") 因源文件 README.md 本身匹配 glob 而恒真 | 假阳性：未创建任何本地化变体也通过 | 改为匹配 `README.[a-z][a-z].md`（或显式列举变体名），并保留"至少一个变体"语义 |
| P1-2 | P1 | check.py:30-31 + checker.py file_contains | glob 命中源文件 + 只检查首个匹配文件 | PROC-04/05/07/NEG-01 可能检的是源文件而非产物；多变体时只检一个 | 让 check.py 遍历所有 `README.*.md` 变体逐一检查，并显式排除 README.md |
| P1-3 | P1 | SCORING OUT-01 + check.py:49 | 用英文关键词 "verif(y\|ied\|ication)" 代理"执行了验证" | agent 用中文输出即误判失败；与真实验证行为无关 | 改 llm 判定，或改为检查输出中是否包含文件清单等更稳健的信号 |
| P1-4 | P1 | SCORING NEG-01 + check.py:53 | "负面合规"却用"URL 存在"作通过条件 | 无法检测 URL 被改写；方向性错误 | 用工具日志做源/产物 URL 集合比对，或补 llm 判定 |
| P1-5 | P1 | SCORING PROC-05 pattern '\\]\\(#' | YAML 单引号不折叠反斜杠，该字符串作为正则需匹配字面量 `\](#`，与文件中的 `](#` 不匹配 | 若 runner 直接消费 YAML pattern 则该项恒失败；与 check.py 中正确的 "\\]\\(#" 表示不一致 | 统一两处转义表示，并在 SCORING 加注释说明 |
| P2-6 | P2 | SKILL.md 第 7 步 vs PROC-07 | "既有无标记选择器 normalize in place"是否补标记未明确 | agent 不补标记时 PROC-07 失败；补标记又可能违反"原位更新"直觉 | 在 reference 中明确"normalize 时补上规范标记" |
| P2-7 | P2 | SKILL.md description | 负向边界（"not general website/app i18n"）只在正文第 16 行，不在 description | 触发阶段误触发风险 | 在 description 末尾补一句负向限定 |
| P2-8 | P2 | PROC-04/05 脚本 | 存在性检查强依赖测试夹具（源 README 必须有围栏和内部锚点） | 夹具设计不当则合规 agent 被误判失败 | 在夹具规范中固定"源 README 含围栏与锚点"；或检查改为"与源一致"的比对 |
| P2-9 | P2 | SCORING.yaml 变量 vs check.py | `${SOURCE_README}`/`${LOCALIZED_README}` 声明未与实现打通 | 声明层与实现层双真相源 | 明确 check.py 为权威，或让 runner 注入变量 |
| P2-10 | P2 | check.py | 12 个未使用 import 模板残留 | 噪声 | 清理 |
| P3-11 | P3 | SKILL.md 第 5 步 | 无 GitHub CJK 标题 slug 规则 | 中文标题锚点生成依赖 agent 知识 | 在 preservation-checklist 补一小节 slug 规则或验证手段 |
| P3-12 | P3 | SCORING NEG-02 | 依赖"源变化"二次触发场景，单轮夹具下不可判定 | 该项得分恒为默认值，数据无效 | 在夹具设计中加入二次变更任务，或标注为条件可判 |

## 13. 改进建议与总体结论

- 优先级建议：
  1. 先修 P1-1（PROC-06 恒真）与 P1-2（glob 命中源文件）——这两个是测量正确性层面的硬伤，直接影响矩阵数据可信度；
  2. 再修 P1-3/P1-4（OUT-01 关键词代理、NEG-01 方向错误）——前者改 llm 判定或换稳健信号，后者改内容比对；
  3. 统一 P1-5 的转义表示，避免"YAML 消费方"与"check.py 消费方"得出相反结论；
  4. 最后处理 P2 级问题（选择器标记歧义、description 边界、夹具约束），P3 级可在下一轮迭代顺带解决。
- 技能内容层面无需大改：SKILL.md 与两个 reference 已经达到"开箱即用"的程度；唯一值得补充的是第 5 步的 slug 规则提示与第 7 步的标记补写规则。
- 对测评实验的启示：本技能的脚本检查应被区分为"代理性证据"（PROC-03~07）与"行为性证据"（经修复后）；在矩阵分析中建议对 6 个 llm 项与 7 个 script 项分别聚合，避免代理性通过率稀释 llm 判定的区分度。
- 总体结论：241-readme-i18n 是一个领域聚焦明确、指令可执行性强、参考设计出色、评估维度与正文同构的技能；其短板不在技能本身，而在评估装置的代理性检查与 glob 语义缺陷。修复 P1 级问题后，本技能可以作为"过程型技能 + 脚本可判检查"结合的标杆样例。
- 复查声明：本 REVIEW 基于 2026-08-06 对目录内全部文件的通读，所有行号引用以当日文件状态为准；如后续对 SKILL.md、SCORING.yaml 或 check.py 有修订，P1-1 至 P1-5 的结论需相应复核。
- 一句话总结：好的技能、需要修的仪表——内容可作教材，测量装置建议在下一轮实验前完成一轮"检查修复 + 夹具对齐"。若无修复条件，建议在实验报告中显式标注 PROC-03~07 为代理性指标，避免误读。
