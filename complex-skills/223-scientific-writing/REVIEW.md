# REVIEW: 223-scientific-writing

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 科研论文写作全流程（IMRAD 结构、引用格式、图表设计、报告指南、段落化写作纪律）
**Body 行数**: 476 行（SKILL.md，含 frontmatter 5 行，正文 471 行；正文约 3,500 词）
**参考文件数**: 5（references/），共 8 个非审查文件、4,510 行
**已有 REVIEW**: 无（首次审查）

---

## 1. 目录全量清单

```
223-scientific-writing/
├── SKILL.md                       (476 行)  ← 主文件
├── SCORING.yaml                   (192 行)  ← 测评标准（21 项：15 LLM + 6 脚本）
├── check.py                       ( 81 行)  ← 测评脚本（6 项脚本检查）
└── references/
    ├── citation_styles.md         (721 行)  ← 引用样式指南（AMA/Vancouver/APA/Chicago/IEEE/ACS/NLM）
    ├── figures_tables.md          (807 行)  ← 图表设计最佳实践
    ├── imrad_structure.md         (659 行)  ← IMRAD 结构指南
    ├── reporting_guidelines.md    (749 行)  ← 报告指南（CONSORT/STROBE/PRISMA 等 11 项）
    └── writing_principles.md      (825 行)  ← 写作原理与风格
```

文件结构总评：职责划分清晰（SKILL.md 纲领 + 5 个大型 reference 文件承载细节），符合 progressive disclosure 模式，且正文在 5 个核心能力节中**显式链接**了全部 5 个 reference 文件（可发现性好，优于同类 skill）。但存在两个结构性问题：(a) SKILL.md 末尾的 `## References` 索引节只列出了 1 个文件（`imrad_structure.md`），其余 4 个文件缺失于索引——文件在正文中被引用但不在索引中，索引节形同虚设（详见 §3.3、§13-🟡4）；(b) 全部 5 个 reference 文件均为 600-800 行的大型文件，SKILL.md 正文未给出加载顺序或优先级指引，冷启动代理可能只读取被显式链接的那一个。

---

## 2. Frontmatter 审查

### 2.1 name
```
name: scientific-writing
```
- 全小写+连字符：✅
- ≤64 字符：✅（16 字符）
- 匹配目录名：⚠️ 目录为 `223-scientific-writing`，name 为 `scientific-writing`。`223-` 为 SkillIF 实验序号前缀，name 取 slug 部分属约定内行为，可接受。

### 2.2 description（逐句分析）

原文（共 627 字符、79 词，含 "description: " 前缀 641 字符；≤1024 上限）：
```
Core competency for the deep research and writing tool. Write scientific manuscripts in
complete paragraphs (never in bullet points). Use two-step process: (1) create section
outlines with key points using research-lookup, (2) convert to flowing prose. IMRAD
structure, citations (APA/AMA/Vancouver), figures/tables, reporting guidelines
(CONSORT/STROBE/PRISMA), for research papers and journal submissions. Use when the user
asks to draft or revise a scientific manuscript, structure a paper with IMRAD, format
citations (APA/AMA/Vancouver), apply reporting guidelines (CONSORT/STROBE/PRISMA), or
prepare a journal submission.
```

逐句拆解：

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "Core competency for the deep research and writing tool." | WHAT（产品定位） | ⚠️ 见问题 1 |
| "Write scientific manuscripts in complete paragraphs (never in bullet points)." | WHAT（核心纪律） | ⚠️ 见问题 1 |
| "Use two-step process: (1) ... (2) ..." | WHAT（工作流概括） | ⚠️ 见问题 1 |
| "IMRAD structure, citations ..., figures/tables, reporting guidelines ..., for research papers and journal submissions." | WHAT（能力清单） | ⚠️ 见问题 1 |
| "Use when the user asks to draft or revise a scientific manuscript, ..." | WHEN + 触发信号 | ✅ |

**问题 1（WHAT 前置过长）**: description 前 4 句（约 430 字符）全部是 WHAT（能力与工作流概括），触发信号 "Use when..." 被推到句末。官方 CSO 规范优先推荐 "Use when" 开头、以触发条件为第一信息，本文恰好相反——触发信号是 5 个候选任务类型（draft/revise manuscript、structure with IMRAD、format citations、apply reporting guidelines、prepare journal submission），覆盖面完整但排布位置靠后。对注入 system prompt 的检索场景，前 430 字符先于触发条件被消费，检索命中上并非最优。

**问题 2（关键词覆盖）**: 覆盖良好——"scientific manuscript"、"IMRAD"、"citations"、"APA/AMA/Vancouver"、"figures/tables"、"CONSORT/STROBE/PRISMA"、"journal submission"、"draft/revise" 均为该领域高频检索词。✅ 与自身正文主题一致。

**第三人称检查**: 全文无第一/第二人称代词，动词为隐含第三人称。✅

**触发信号**: 末句给出 5 个明确的用户任务触发条件。✅

**字符数**: 627 ≤ 1024。✅

### 2.3 其他 frontmatter 字段
`allowed-tools: [Read, Write, Edit, Bash]` —— 合法字段。读/写/编辑文件对稿件产出合理；**Bash 的唯一正当理由是 L46 的 `python scripts/generate_schematic.py` 命令**，但该脚本实际存在于兄弟技能 255-scientific-schematics 的目录下（详见 §4 矛盾 3），在本技能自己的工作区内 Bash 无实质用途。无 argument-hint / user-invocable / model / paths 等字段，也无任何禁止字段。✅

### 2.4 Frontmatter 语法
YAML 分隔符 `---` 配对正确，无缩进错误，无特殊字符问题。✅

---

## 3. Body 结构分析

### 3.1 段落清单（SKILL.md，共 16 个一级节）

| 节 | 行号 | 内容 |
|----|------|------|
| # Scientific Writing | L7 | 标题 |
| ## Overview | L9-15 | 定位（核心能力）+ 核心纪律（段落化写作）+ 两步法 |
| ## When to Use This Competency | L17-29 | 10 项触发场景（Scope） |
| ## Visual Enhancement with Scientific Schematics | L31-64 | ⚠️ MANDATORY 强制 1-2 张 AI 示意图 + 外部技能依赖 |
| ## Core Capabilities（10 个子节） | L66-425 | 结构/分节写作/引用/图表/报告指南/写作原理/两步过程/期刊格式/领域语言/常见陷阱 |
| ## Manuscript Development Workflow | L426-462 | 规划→起草→修订→定稿 4 阶段（Process） |
| ## Integration with Other Scientific Competencies | L464-470 | 与其他能力协作 |
| ## References | L472-476 | 参考文件索引（**只列 1 个文件**） |

### 3.2 必需章节检查（审计规范要求 Workflow/Process + Output Format + Scope/Limitations）

| 必需项 | 状态 | 说明 |
|--------|:----:|------|
| Workflow/Process | ✅ | 显式存在。`## Manuscript Development Workflow`（L426-462）给出 4 阶段编号流程：规划（期刊/指南/大纲/图表计划）→ 起草（图表先行 + 每节两步法 + 固定节序）→ 修订（7 项检查）→ 定稿（5 项准备）。另有 §7 "Writing Process: From Outline to Complete Paragraphs"（L205-305）给出两步法的详细操作与示例。双重流程定义互不冲突。 |
| Output Format | ⚠️ | 存在但未命名、未完整定义。格式规则散见：(a) 核心纪律"必须完整段落、禁止项目符号"（L15、L207、L278-284）；(b) 列表仅限 Methods 与补充材料（L286-291）；(c) 摘要 100-250 词（L89）；(d) 期刊格式要求（§8 L307-315）。但没有一个"最终交付物格式"的统一定义——稿件以什么形态交付（单个 .md 文件？分节？）、含哪些必备声明，无明文规定。SCORING 的 FMT-01/NEG-01 以"输出中无 - 行"为判定，而 skill 未告诉代理把稿件写进哪个文件、是否全文回显。 |
| Scope/Limitations | ⚠️ | Scope 完整（`## When to Use` L17-29 的 10 项 + §10 常见陷阱）。Limitations **完全缺失**：未声明本技能不做什么，也未声明两个前置依赖（research-lookup 用于第一步查文献、scientific-schematics 用于强制图表）在目标环境中**必须可用**。对执行代理而言，"强制要求依赖另一个能力，却不说明依赖何时成立"，是可执行性的关键盲区。 |

### 3.3 内容委托分析（progressive disclosure 是否符合规则）

- 5 个 reference 文件均为 600-825 行的大文件，外置合理；正文在 §1/§3/§4/§5/§6 五处分别显式链接到 imrad_structure / citation_styles / figures_tables / reporting_guidelines / writing_principles，链接完备、无断链。✅
- **但末尾索引不完整**：`## References`（L472-476）只列 `references/imrad_structure.md` 一项，其余 4 个文件缺失。对一个依赖 LLM 代理检索行为的测评场景（QA-04 要求工具日志中出现任一 reference 文件路径），索引残缺会系统性降低"代理读取参考文件"的概率——代理只能靠正文 5 处链接发现文件。
- **加载顺序缺失**：5 个大型文件没有优先级指引。写 Introduction 的代理应该先读哪个？imrad_structure.md？writing_principles.md？正文只按"提到即链接"的散点方式引用，无"先读 A 再读 B"的编排。
- 委托链深度：正文 → references/*.md 单层，无嵌套引用。✅

---

## 4. 逻辑一致性

### 4.1 内部一致性核对（正文 ↔ 参考文件 ↔ SCORING）

| 主题 | 正文/参考文件 | SCORING | 一致 |
|------|--------------|---------|:----:|
| 摘要字数 | 100-250 词（SKILL.md L89；imrad L76-77） | PROC-02 "abstract 100-250 words" | ✅ |
| 两步写作法 | §7 详述（L209-305） | PROC-01 | ✅ |
| 引用样式 | AMA/Vancouver/APA/Chicago/IEEE（L122-127） | PROC-03 | ✅ |
| 图表密度 | "one table/figure per 1000 words"（L149） | FMT-03 未量化 | ✅ |
| 报告指南 | 10 项清单（L164-173）；参考文件另含 SRQR/COREQ | SCOPE-03（CONSORT/STROBE/PRISMA 举例） | ✅ |
| 列表纪律 | 仅 Methods/补充材料允许（L286-291） | FMT-02 | ✅ |
| 时态规则 | writing_principles.md 时态表 | QA-02 | ✅ |
| 缩写首用定义 | L183、writing_principles.md "Abbreviation Abuse" | QA-03 | ✅ |
| 修订流程 | 修订 7 项检查（L448-455） | QA-01 | ✅ |
| 强制示意图 | "MANDATORY 1-2 AI-generated figures"（L33） | TEC-01、CF-03 | ✅（但见 4.2 矛盾 3） |

整体一致度高，21 项测评点全部能在正文/参考文件中找到文本支撑，无自指矛盾（本技能没有"教人写技能"的元规则，所以不存在 298-writing-skills 那类自指悖论）。

### 4.2 发现的不一致与矛盾

**矛盾 1（中低危）— 强制图表数量 vs 质量优先原则**：SKILL.md L33 声明 "**MANDATORY: Every scientific paper MUST include at least 1-2 AI-generated figures**"，但 figures_tables.md L117-118 强调 "Quality over quantity: A few well-designed, information-rich displays are better than many redundant or poorly designed ones"，L111 有 "one display item per 1000 words" 密度规则。对一篇 500 词的 letter 或纯理论/modeling 论文，1-2 张强制示意图可能与学科惯例相悖。强制要求是**量化硬约束**（无论论文类型），参考文件是**质量导向**（按内容定数量），两者张力未在正文调和——正文从未解释"为什么短论文也必须 1-2 张图"。

**矛盾 2（低危）— Results/Discussion 列表例外的措辞混乱**：L280 规定 "Do not use numbered or bulleted lists in Results or Discussion (except specific cases such as study hypotheses or inclusion criteria)"。inclusion/exclusion criteria 属于 Methods 的标准内容（L282 明确 "✅ Do make occasional use of lists only in Methods (e.g., inclusion/exclusion criteria)"），把它列为 Results/Discussion 的列表例外不合逻辑——同文件两处对"inclusion criteria 出现在哪个节"的表述互相冲突。SCORING FMT-02 与正文 L282 一致（Methods），应以 L282 为准修正 L280。

**矛盾 3（高危）— MANDATORY 图表的外部依赖在隔离环境不可满足**：L44-47 要求运行 `python scripts/generate_schematic.py "..." -o figures/output.png`，L40 称使用 "scientific-schematics competency" 与 "Nano Banana Pro"。经核查：
- 兄弟技能 `255-scientific-schematics` 在实验集中存在，其目录下**确有** `scripts/generate_schematic.py`（以及 `generate_schematic_ai.py`），"Nano Banana Pro" 也是该技能的既有表述——依赖链在全集层面成立；
- 但 L46 的命令路径是**相对路径**，脚本在 255 技能目录而非 223 目录下。SkillIF 实验按技能逐工作区隔离测评，223 的工作区中没有 `scripts/`，命令必然失败；
- SCORING TEC-01 的脚本检查只看**工具日志**是否出现 `generate_schematic\.py|figures/` 字样——即**命令即使执行失败也判通过**；而 CF-03（无示意图 → cap_to_0）由 LLM 判题，又会因示意图确实不存在而判死。
- 结论：在本实验环境内，TEC-01 存在"假通过"、CF-03 存在"不可满足的真实失败"，两者叠加使该技能存在系统性误判风险。若测评环境不合并部署 255 技能，所有代理都会在 CF-03 上清零，测评失去区分度。

**矛盾 4（低危）— "IMRAD" 拼写不统一**：SKILL.md 与 imrad_structure.md 绝大多数用 "IMRAD"，但 imrad_structure.md L495 用 "IMRaD without separate Conclusion"（小写 a），同一文件内两种拼写并存；SKILL.md L72 与 imrad_structure.md L3 的展开式中 "And" 大写（"Introduction, Methods, Results, And Discussion"）不合英文惯例。

**矛盾 5（低危）— 无出处的文献引用**：figures_tables.md L7 声称 "A recent Nature Cell Biology checklist (2025) emphasizes ..."，无链接、无出处。本技能自己的 TEC-02/NEG-02 教导"引用必须可验证、禁止无出处断言"（citation_styles.md 有专门 Verifying Citations 一节），参考文件自身却示范了反面教材。

**矛盾 6（低危）— "IMRAD 是所有学科标准" 的过度断言**：imrad_structure.md L5 称 IMRAD "is now the standard in medical, health, biological, chemical, engineering, and computer sciences"，但同文件 L487-503 又承认大量变体（Results+Discussion 合并、ILMRaD、case report 无 IMRAD），与 SKILL.md §1 "Alternative Structures"（review/case report/meta-analysis 等）并存。表述"标准"与"变体"之间缺乏缓冲措辞（如 "for original research articles"）。

---

## 5. 参考文件审查（每个文件全文通读）

### 5.1 references/citation_styles.md（721 行）

- **覆盖**：AMA、Vancouver、APA、Chicago、IEEE 五大样式 + ACS、NLM 补充；含选择决策表、正文格式、参考文献格式、特殊情况、DOI 规则、期刊专用样式（JAMA/NEJM/Lancet/Nature/Science/Cell/PLOS 等 12+ 家）、ML 会议引用规范、提交前检查清单、官方资源链接。
- **准确性抽查**：AMA ">6 authors → list first 3 then et al"（L80-83）✅ 符合 AMA 11th ed；Vancouver ">6 authors → first 6 then et al."（L145）✅ 符合 ICMJE；APA 7th "up to 20 authors list all; 21+ → first 19, ..., final"（L248-249）✅；APA 句子大小写/标题大小写规则 ✅；Chicago 17th 注释与书目格式 ✅；IEEE 会议论文格式 ✅。专业深度高，未见事实错误。
- **质量问题**：无。这是 5 个参考文件中数据密度最高、最不易出错的一个。

### 5.2 references/figures_tables.md（807 行）

- **覆盖**：表 vs 图决策规则、6 大设计原则（自解释/无冗余/一致性/数量/清晰/简洁）、7 类图型（条形/折线/散点/箱线/热图/图像/森林图/流向图）的设计要点与常见错误、表格结构规范、统计呈现（误差棒 SD/SEM/CI 对照表）、无障碍（色盲友好配色）、技术规格（分辨率/格式/尺寸/图像处理伦理）、编号与图注规范、期刊特定要求、ML 会议图表规范、提交前检查清单。
- **质量问题**：(a) L7 的 "Nature Cell Biology checklist (2025)" 无出处（见 §4 矛盾 5）；(b) L350-357 的示例表格使用 Unicode box-drawing 字符（─────），与实验集的规范化工具（fix_box_chars.py）目标相悖，属规范化残留；(c) "Avoid red-green combinations"（L428）等无障碍建议未给出具体色值参考（仅给 Colorbrewer2/Viridis 名称），对执行代理可操作性略低。
- **准确性抽查**：误差棒含义表（L390-394）正确；"非重叠 CI 通常对应显著差异"（L404）表述严谨（带"indicate"限定）；300 dpi 分辨率要求 ✅；图像处理伦理（允许/禁止清单）✅。

### 5.3 references/imrad_structure.md（659 行）

- **覆盖**：IMRAD 历史与逻辑、完整稿件 10 组件、Title/Abstract/Introduction/Methods/Results/Discussion/Conclusion 分节指南（每节含目的、结构、长度、时态、常见错误、示例）、时态汇总表、IMRAD 变体（合并 Results+Discussion、ILMRaD、case report）、venue 差异（Nature/Science vs 医学期刊 vs ML 会议）、结构比例表、提交前检查清单。
- **质量亮点**：示例质量高——如 Discussion 的"与既往研究对比"三段式示例（L383-403）与 Conclusion 示例（L440-447）可直接模仿；时态表（L469-485）与 writing_principles.md 一致，无冲突。
- **质量问题**：(a) 拼写变体 IMRAD/IMRaD（L495）；(b) L47 示例 "VO2 Max" 应为 "VO₂max"（下标 2）——对一本教人规范写作的指南，自身格式不规范的示范不利；(c) "ILMRaD"（L499）无展开说明，读者需自行推断 L=Literature。

### 5.4 references/reporting_guidelines.md（749 行）

- **覆盖**：11 项指南——CONSORT（25 项清单 + 流向图）、STROBE（22 项）、PRISMA 2020（27 项 + 2020 流向图新特性）、SPIRIT（33 项）、STARD（30 项）、TRIPOD（22 项）、ARRIVE 2.0（Essential 10 + Recommended）、CARE（13 项）、SQUIRE 2.0（18 项）、CHEERS 2022（28 项）、SRQR/COREQ；含使用时机（设计/起草/投稿三阶段）、清单填写示例（带页码行号）、EQUATOR 检索方法、多项指南叠加场景、流向图 ASCII 示例（CONSORT/PRISMA）、常见错误 7 条、期刊强制要求、ML 会议可复现性标准、提交前检查清单。
- **准确性抽查**：CONSORT 25 项清单 ✅；STROBE 22 项 ✅；PRISMA 2020 的 27 项 ✅；ARRIVE 2.0 双集合结构 ✅；CHEERS 2022（28 项）✅——版本与条目数与官方一致，未发现过时版本混用。
- **质量问题**：(a) CONSORT 流向图示例（L511-532）用 ASCII 画线（├───┬───┐），视觉可读性一般，但作为文本占位可接受；(b) 无 PRISMA 流向图的图形示例（仅文字描述四个阶段），执行代理只能自行设计；(c) 清单条目多处以 "Main checklist items" 概要呈现而非逐条全列（如 SPIRIT 33 项未全列），对需要逐项自查的代理，信息密度略不足。

### 5.5 references/writing_principles.md（825 行）

- **覆盖**：三大支柱（清晰/简洁/准确）+ 客观性、一致性、逻辑组织；时态总表；6 类常见错误（术语过载/名词化/过度或不足 hedging/拟人化/缩写滥用）附正反对照；句子级问题（悬垂修饰/逗号/代词一致/主谓一致）；易混词表（affect/effect、among/between、data are 等）；数字与单位规则；段落结构（3-7 句）；修订检查清单（词/句/段/内容四级）；写作工具（Grammarly 等 + 使用警示）；4 类 venue 文体对照表（Nature/Science vs 医学 vs 专科 vs ML 会议）；推荐书目。
- **质量亮点**：正反例对照密度极高（几乎每节都有 Poor/Better 对），是执行代理可直接模仿的范例库；"Words to Avoid" 表与"数字格式"规则可操作性强。
- **质量问题**：无实质问题。唯一小瑕疵：L98 "As the principle states: 'We value concise writing because we value time.'"——"principle" 无出处，出处不明的格言式引用（同样违反本技能自己的引用纪律，与 §4 矛盾 5 同类，但更轻微）。

---

## 6. 语法与格式质量

### 6.1 英文质量
8 个文件整体英文质量高，为母语级学术写作示范（skill 自身的行文本身就是范文）。未发现拼写错误。小瑕疵：
- "Introduction, Methods, Results, And Discussion" 中 "And" 大写（SKILL.md L72、imrad_structure.md L3）。
- imrad_structure.md L47 "VO2 Max" 下标缺失。
- imrad_structure.md L495 "IMRaD" 与全文 "IMRAD" 拼写不一致。

### 6.2 格式细节
- **Emoji 使用**：SKILL.md 使用 ⚠️（L33）、❌/✅（L278-284）作为语义标记——⚠️ MANDATORY 警示与错误/正确对照标记，属功能性而非装饰性 emoji，可接受。reference 文件无 emoji。
- **全大写/权威表述**："**⚠️ MANDATORY**"（L33）、"**CRITICAL:**"（L207）、"This is not optional."（L35）——对 discipline-enforcing 型写作技能，权威语气是设计工具而非失控（本技能的核心纪律就是"禁止项目符号"，需要强语气支撑），判定合理。
- **Markdown 围栏**：SKILL.md 中 4 处代码围栏（outline 示例 L222-233、prose 示例 L248-264、对比表、bash 示例 L45-47）全部闭合；reference 文件中示例围栏（AMA/Vancouver/APA 格式示例）闭合正常。未发现残缺围栏。
- **box-drawing 字符**：figures_tables.md L350-357 示例表格使用 "─" 字符，为规范化残留（实验集有 fix_box_chars.py 工具）。
- **超长行**：SKILL.md L33、L46、L248-264（prose 示例含硬换行）等行较长（>120 字符），不影响 Markdown 渲染，但影响 diff/审阅体验。
- **check.py 冗余导入**：L12-20 导入 file_exists、file_contains、file_valid_json、json_field_*、timestamp_*、tool_log_not_contains、tool_log_order 等 12 个函数，实际仅使用 4 个（tool_log_contains、output_contains、output_not_contains、set_tool_log_path、set_agent_output——其中 output_not_contains 也未被本文件调用）。lint 冗余，无功能影响。

---

## 7. 规范合规性（12 项逐条对照）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name = 小写+连字符 ≤64，匹配目录 | ✅ | `scientific-writing` 16 字符；与目录相差实验序号前缀（约定内） |
| 2 | description 第三人称 WHAT+WHEN+关键词 ≤1024，含触发信号 | ✅ | 627 字符、第三人称、末句 "Use when..." 触发信号、关键词覆盖充分；⚠️ WHAT 前置 4 句（约 430 字符）过长，触发信号排位靠后 |
| 3 | 仅允许的可选 frontmatter 字段 | ✅ | name + description + allowed-tools（Read/Write/Edit/Bash） |
| 4 | Body 必须有 Workflow/Process 节 | ✅ | `## Manuscript Development Workflow`（4 阶段编号流程）+ §7 两步法 |
| 5 | Body 必须有 Output Format 节 | ⚠️ | 格式规则散见 4 处（段落纪律/列表限制/摘要字数/期刊格式），无统一定义"最终交付物形态" |
| 6 | Body 必须有 Scope/Limitations 节 | ⚠️ | Scope（When to Use）完整；Limitations 完全缺失，未声明 research-lookup / scientific-schematics 前置依赖 |
| 7 | Body ≤600 行 | ✅ | 476 行 |
| 8 | 无跨 skill 文件路径 | ⚠️ | 无 `../` 引用；但 L46 `scripts/generate_schematic.py` 相对路径指向兄弟技能 255 的工作区，在本技能工作区不可解析 |
| 9 | 所有引用文件存在 | ✅ | 正文 5 处 `references/*.md` 链接全部有效；⚠️ 末尾 References 索引仅列 1/5 个文件（索引不完整而非断链） |
| 10 | 无 @ 强制加载链接 | ✅ | 全文未发现 `@` 链接 |
| 11 | Markdown 围栏闭合 | ✅ | 全部围栏闭合，未发现残缺 |
| 12 | SCORING.yaml 与内容对齐 | ✅ | 21 项均可从正文/参考文件找到支撑；CF 三项与正文强制规则对应（见 §10） |

**违规汇总**：无完全违规项（0 ❌），10 ✅、2 ⚠️。⚠️ 项集中在：(a) 无 Limitations 节；(b) 外部脚本路径不可解析。均为可低成本修复的编辑层问题，无结构性硬伤。

---

## 8. 人机感评估

### 8.1 Emoji 审计
SKILL.md 共 3 类 emoji（⚠️/❌/✅），全部作为语义标记出现在规则陈述中（L33 强制警示、L278-284 错误/正确对照），无装饰性 emoji。reference 文件零 emoji。判定：✅ 可接受。

### 8.2 全大写/喊叫式语言
"MANDATORY"、"CRITICAL"、"This is not optional."、"Never submit bullet points" 等权威式表述集中于 L33-35、L207-215——全部服务于本技能的核心纪律（段落化写作 + 强制图表）。对一个"写作纪律执行器"型技能，强语气与任务目标自洽。与 255-scientific-schematics 的 "MANDATORY" 表述风格同源，系同一来源技能家族的一致性风格。判定：✅ 自洽。

### 8.3 Persona 语气
专业编辑/学术顾问人格：陈述式指南为主（"Use the research-lookup competency to gather relevant literature and data"），夹杂命令式纪律声明（"Never submit lists where paragraphs should be"）。无口语化、无讨好用户内容。对学术写作技能，语气匹配目标受众（研究人员）。

### 8.4 人机边界
无任何"技能是活的/有情感"的暗示；无虚构能力声明之外的内容；唯一的拟人化风险点是 "Nano Banana Pro will automatically generate, review, and refine the schematic"（L42）——把外部工具描述为自动代理，但这是 255 技能既有的产品表述，非本技能独创。✅

### 8.5 人称分析
- description：第三人称 ✅
- SKILL.md 正文：以无主语句式（祈使/陈述）为主（"Define abbreviations on first use"、"Create a glossary if..."），少数第二人称（"your manuscript" L472 附近无——实际为 "your diagram description" L46、"your target journal" L386），与 reference 文件的祈使风格统一。✅
- references/：祈使句 + 示例对照为主，风格统一。✅

人机感综合：设计克制、语气专业、无噪声，评分高。

---

## 9. 可执行性评估

### 9.1 核心工作流可执行性
两步写作法（查文献→提纲→成文）与 4 阶段工作流（规划→起草→修订→定稿）均有编号步骤与示例支撑。SKILL.md §7 的 outline 示例（L222-233）与 prose 转化示例（L248-264）是**同一主题的成对示例**（AI 药物发现→罕见病），代理可逐句模仿转换模式。冷启动代理按 L426-462 的 4 阶段顺序即可完整执行，路径清晰度高于同类写作技能。

### 9.2 步骤可操作性
- "Use research-lookup to gather literature"（L295-299）：依赖 033-research-lookup 技能可用；该技能在实验集中存在，✅ 但本技能未声明此前置条件。
- "Generate at minimum ONE schematic"（L36）：命令与脚本在 255 技能目录（见 §4 矛盾 3），**本工作区不可执行**。这是可执行性最大弱点。
- "Check word count for each section"（L454）、"Verify all citations"（L453）：给出检查项但未给方法（如字数用何工具），代理需自行实现。可接受。
- 修订阶段 7 项检查清单（L448-455）操作性强，逐条可对照执行。✅

### 9.3 工具依赖合理性

| 依赖 | 用途 | 判定 |
|------|------|:----:|
| 033-research-lookup（兄弟技能） | 两步法第 1 步查文献 | 存在但未声明；✅ 合理 |
| 255-scientific-schematics + scripts/generate_schematic.py | 强制示意图（TEC-01/CF-03） | ⚠️ 脚本路径相对 223 不可解析；本工作区命令必然失败 |
| Nano Banana Pro（图像模型） | 示意图生成 | ⚠️ 外部产品依赖，实验环境不可用性未知 |
| Read/Write/Edit | 稿件读写 | ✅ 合理 |
| Bash | 运行 generate_schematic.py | ⚠️ 核心用途落空后基本闲置 |

### 9.4 检查工具可执行性

check.py 可运行（3 参数，返回 JSON），返回 6 项（PROC-03、FMT-01、TEC-01、NEG-01、QA-03、QA-04），与 SCORING.yaml 的 6 个 script 项一一对应。✅ 但存在 4 个设计弱点：

1. **检查目标文本不确定（最严重）**：FMT-01/NEG-01/PROC-03/QA-03 检查 agent 最终输出文本，但本技能要求"稿件交付"（Write 工具写文件）。若代理把稿件写入 .md 文件、最终消息仅一两句话，输出中不含稿件——"无 - 行"、"含年份括号"等检查退化为对空文本的检查（NEG-01/FMT-01 恒通过、PROC-03/QA-03 恒失败），结果与稿件实际质量完全脱钩。测评 runner 必须保证 agent_output 含完整稿件，check.py 自身无法解决。
2. **TEC-01 假通过**：模式 `generate_schematic\.py|figures/` 匹配工具日志字符串——执行失败的命令同样入日志，`figures/` 子串更是任何写 `figures/` 目录的操作（如 matplotlib 存图）都命中。脚本检查的语义（"AI 生成的示意图"）与模式强度（"出现字符串"）不匹配。
3. **FMT-01 与 NEG-01 同义重复**：两条标准检查同一属性（输出中无列表行），NEG-01 模式（`^\s*[-*]\s`，含缩进与 `*`）是 FMT-01（`^- `）的超集，规则层面冗余。
4. **FMT-01/NEG-01 与技能规则冲突**：skill 允许 Methods 中的合法列表（L282），但脚本模式对全文生效——含 Methods 列表的完整稿件若回显在输出中即被误判。CF-01 的描述精确限定于 "Abstract/Introduction/Results/Discussion"（与技能规则一致），脚本检查却比 CF-01 更宽。

---

## 10. SCORING.yaml 交叉参考

### 10.1 结构统计
- total_items: 21 = 3(scope) + 5(process) + 4(format) + 3(technical) + 2(negative) + 4(qa)。✅ 与文件内分组一致。
- judge 分布：15 llm + 6 script（PROC-03、FMT-01、TEC-01、NEG-01、QA-03、QA-04）。check.py 返回项数与 script 项数一致。✅
- `pattern: process` 与技能类型一致。✅

### 10.2 测评点覆盖核对（21 项）

| 判题项 | 支撑来源（skill 内） | 一致性 |
|--------|----------------------|:----:|
| SCOPE-01 | SKILL.md L17-29（When to Use） | ✅ |
| SCOPE-02 | SKILL.md §1（IMRAD + 替代结构） | ✅ |
| SCOPE-03 | SKILL.md §5（报告指南清单） | ✅ |
| PROC-01 | SKILL.md §7（两步法） | ✅ |
| PROC-02 | SKILL.md §2（分节指导）+ imrad_structure.md | ✅ |
| PROC-03 | SKILL.md §3 + citation_styles.md | ⚠️ 脚本模式过弱（任何含 `(2023)`/`et al.`/`[1]` 的文本即通过，无法证明"样式一致且正确"） |
| PROC-04 | SKILL.md §8（期刊要求） | ✅ |
| PROC-05 | SKILL.md Workflow（4 阶段） | ✅ |
| FMT-01 | SKILL.md L15、L207（段落纪律） | ⚠️ 与 NEG-01 重复；且全文模式与"Methods 可列表"规则冲突 |
| FMT-02 | SKILL.md L286-291（列表允许场景） | ✅ |
| FMT-03 | SKILL.md §4 + figures_tables.md | ✅ |
| FMT-04 | SKILL.md §9（领域语言） | ✅ |
| TEC-01 | SKILL.md L33-64（MANDATORY 示意图） | ⚠️ 模式过宽 + 外部脚本不可解析（§4 矛盾 3） |
| TEC-02 | citation_styles.md Verifying Citations 节 | ✅ |
| TEC-03 | SKILL.md §10（拒绝原因） | ✅ |
| NEG-01 | SKILL.md L278-284（禁止列表） | ⚠️ FMT-01 重复；全文模式误伤 Methods 合法列表 |
| NEG-02 | citation_styles.md 引用验证清单 | ✅ |
| QA-01 | SKILL.md Workflow 修订阶段（L448-455） | ✅ |
| QA-02 | writing_principles.md 时态表 | ✅ |
| QA-03 | writing_principles.md "Abbreviation Abuse" | ⚠️ 脚本模式 `\([A-Z]{2,5}\)` 要求输出中出现括号缩写——无缩写或输出不含稿件时误判失败 |
| QA-04 | references/ 5 文件 | ✅ 模式合理（任一 reference 路径出现在工具日志即通过） |

### 10.3 关键失败项核对
- **CF-01**（A/I/R/D 节出现项目符号 → cap_to_0）↔ SKILL.md L278-284 核心纪律。范围限定精确（四个节），与技能规则一致；但与 FMT-01/NEG-01 的全文检查存在张力（见 §9.4-4）。
- **CF-02**（伪造/不可验证引用 → cap_to_0）↔ citation_styles.md 的验证清单 + NEG-02。支撑充分。
- **CF-03**（无强制示意图 → cap_to_0）↔ SKILL.md L33 "MANDATORY"。**环境可满足性存疑**：依赖 255-scientific-schematics 的脚本与 Nano Banana Pro 外部产品；在隔离工作区测评时，CF-03 对全部代理恒成立 → 测评失效。这是本 SCORING 最重要的风险项。
- **CF 无 judge 字段**：3 条 critical_failures 均未声明判题方式（llm/script），测评 runner 需自行裁决——建议明确（CF-01 可脚本化、CF-02/CF-03 建议 LLM）。

### 10.4 小结
21 项覆盖完备、与内容对齐良好（优于 322 个技能的平均水平），主要问题集中在脚本检查的**模式强度**与**检查目标**两个层面，属测评工程问题而非内容问题。

---

## 11. 已知问题（跳过）

按任务要求本节跳过：无已知问题清单可供核对。

---

## 12. 综合评分（8 维 → /100）

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | 字段/长度/第三人称/触发信号全达标，关键词覆盖充分；仅 WHAT 前置过长（约 430/627 字符） |
| Body 结构完整 | 8/10 | 10% | 0.80 | Workflow 显式且双份（流程+两步法）；Output Format 隐含未命名；Limitations 完全缺失；References 索引仅列 1/5 |
| 逻辑一致性 | 8/10 | 20% | 1.60 | 无自指矛盾，三处（正文↔参考↔SCORING）大体一致；6 处轻微不一致中最重的是强制图表的外部依赖不可满足（§4 矛盾 3） |
| 参考完整性 | 9/10 | 15% | 1.35 | 5/5 存在且质量高（721-825 行），内容准确性与深度显著高于平均；索引残缺、2 处无出处引用为扣分点 |
| 语法格式 | 9/10 | 10% | 0.90 | 母语级英文、围栏全闭合、无拼写错误；小瑕疵（"And" 大写、IMRaD 变体、box chars、超长行） |
| 规范合规 | 9/10 | 15% | 1.35 | 12 项中 10 ✅、2 ⚠️、0 ❌；⚠️ 项（Limitations 缺失、外部脚本路径）均低成本可修 |
| 人机感 | 9/10 | 10% | 0.90 | 语气专业克制、emoji 语义化、权威语气与纪律主题自洽、无噪声 |
| 可执行性 | 7/10 | 10% | 0.70 | 流程步骤清晰、正反例可直接模仿；但脚本检查目标不确定（§9.4-1）、TEC-01 假通过、外部脚本不可解析 |
| **加权总分** | | | **85.0/100** | |

### 12.2 评级

🟢 **A-**（85/100）— 内容质量在 322 个 complex skills 中属第一梯队：5 个 reference 文件（3,761 行）专业深度极高、正反例与数据准确性经抽查无事实错误，正文与 SCORING 的 21 项测评点映射完整，无自指矛盾。失分集中在**测评工程层**（脚本检查目标不确定、TEC-01/CF-03 的环境不可满足性）与**编辑层**（Limitations 缺失、索引残缺、外部路径）。所有 ⚠️ 项均可在低工作量内修复；其中 §13-🔴1/2 若不修，测评可能对全部代理系统性误判，属于必须优先处理项。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复，影响测评有效性）

1. **消除 CF-03/TEC-01 的环境不可满足性**（SKILL.md L31-64、SCORING.yaml TEC-01/CF-03）
   - 位置：SKILL.md L33-47；SCORING.yaml L109-112（TEC-01）、L190-191（CF-03）
   - 问题：`python scripts/generate_schematic.py` 相对路径在 223 工作区不可解析（脚本属 255-scientific-schematics）；Nano Banana Pro 为外部产品。隔离测评时 CF-03 对全部代理恒成立 → 全清零。
   - 修复（三选一）：(a) 测评 runner 将 255-scientific-schematics 的 `scripts/` 部署进 223 工作区（在实验说明中固定此约定）；(b) 把 CF-03 改为条件性关键失败（"当环境提供 scientific-schematics 时"）；(c) 在 SKILL.md 补一句依赖声明："Requires the scientific-schematics competency and its scripts directory to be available in the workspace; otherwise substitute a textual figure placeholder and note the omission."
   - 工作量：S-M

2. **修正脚本检查的目标文本不确定性**（check.py FMT-01/NEG-01/PROC-03/QA-03）
   - 位置：check.py L36-53；SCORING.yaml 对应项的 evidence 字段
   - 问题：代理把稿件写入文件时，最终输出不含稿件文本，4 项 output_* 检查全部退化（否定类恒通过、肯定类恒失败），结果与稿件质量脱钩。
   - 修复：在 SCORING.yaml 的 evidence 中明确 "agent_output = final manuscript full text（runner 将稿件文件内容并入 agent_output 再调用 check.py）"，或在 check.py 中支持对 workspace 内指定稿件文件做检查。
   - 工作量：S

3. **修复脚本检查与技能规则的冲突**（FMT-01/NEG-01 全文检查 vs Methods 合法列表）
   - 位置：SCORING.yaml FMT-01（L74-79）、NEG-01（L131-137）
   - 问题：技能允许 Methods 中出现列表（SKILL.md L282），脚本模式却对全文生效；含 Methods 列表的合规稿件会被误判。
   - 修复：(a) 将 FMT-01 与 NEG-01 合并为一项并交由 LLM 判题（CF-01 已覆盖最严重场景）；或 (b) 脚本模式限定检测 Abstract/Introduction/Results/Discussion 区段（模式改为检查段头与段尾之间的行）。
   - 工作量：S

### 🟡 建议修复（内容与测评质量改进）

4. **补全 SKILL.md 末尾 References 索引**（SKILL.md L472-476）
   - 现仅列 `imrad_structure.md` 1 个；补列 citation_styles.md、figures_tables.md、reporting_guidelines.md、writing_principles.md（可加一行一句简介）。这同时提升 QA-04 的达成概率。
   - 工作量：S

5. **新增 Limitations 节**（SKILL.md 末尾）
   - 内容建议：声明前置依赖（research-lookup 用于文献检索、scientific-schematics 用于强制示意图）必须可用；本技能不负责统计建模/数据分析；不替代期刊官方投稿系统；对无图表能力的场景给出降级路径。
   - 工作量：S

6. **收紧 TEC-01 的脚本模式**（SCORING.yaml L109-112）
   - 现模式 `generate_schematic\.py|figures/` 过宽（失败命令入日志、任何 figures/ 路径命中）。建议改为要求工具日志中**同时**出现 `generate_schematic\.py` 且后续存在成功证据（如 `-o figures/.*\.png` 或写入后 Read 该文件），或直接改为 LLM 判题。
   - 工作量：S

7. **修正 QA-03 的判定方式**（SCORING.yaml L164-171）
   - 模式 `\([A-Z]{2,5}\)` 对"无缩写稿件/输出不含稿件"误判失败。建议降为 LLM 判题（与 QA-02 同组），或改为对参考文件的模式。
   - 工作量：S

8. **修正 L280 列表例外措辞**（SKILL.md L280）
   - "except specific cases such as study hypotheses or inclusion criteria" 中的 "inclusion criteria" 与 L282/L286-291 的 Methods 定位冲突。改为 "except specific cases such as study hypotheses or pre-specified analytic comparisons"，把 inclusion criteria 从 Results/Discussion 例外中移除。
   - 工作量：S

9. **统一 IMRAD 拼写与展开式**（SKILL.md L72、imrad_structure.md L3、L495）
   - 统一为 "IMRAD（Introduction, Methods, Results, and Discussion）"；L495 "IMRaD" 改 "IMRAD"；L47 "VO2 Max" 改 "VO₂max"。
   - 工作量：S

10. **为无出处引用补源**（figures_tables.md L7、writing_principles.md L98）
    - "A recent Nature Cell Biology checklist (2025)" 补链接或删去年份断言；"As the principle states" 改为明确出处（或删引号、改为陈述）。本技能教导"引用必须可验证"，自身应示范。
    - 工作量：S

11. **清理 check.py 冗余导入**（check.py L12-20）
    - 仅保留实际使用的 set_tool_log_path、set_agent_output、tool_log_contains、output_contains、output_not_contains；其余 12 个导入删除。
    - 工作量：S

12. **在 SKILL.md 说明 generate_schematic.py 的归属**（SKILL.md L44-47）
    - 补一句 "The generate_schematic.py script is provided by the scientific-schematics competency（see 255-scientific-schematics）；ensure its scripts/ directory is on the PATH or in the workspace."，消除路径歧义。
    - 工作量：S

### 🟢 可选优化

13. **显式化 Output Format**（SKILL.md）
    - 在 Workflow 节末尾补一小节，定义最终交付物形态（如：稿件为单个 .md 文件、含标题/摘要/各节/参考文献、Methods 内列表的呈现格式、声明段落），使 FMT 系判题项有明确的行为锚点。
    - 工作量：S

14. **为 5 个 reference 文件添加读取顺序指引**（SKILL.md §7 或 Workflow 节）
    - 一行即可："Start with references/imrad_structure.md for section-level guidance, consult references/citation_styles.md when formatting references, references/figures_tables.md when preparing display items, references/reporting_guidelines.md to confirm checklist compliance, and references/writing_principles.md for style revision."
    - 工作量：S

---

**审查总结**：223-scientific-writing 是一个内容质量顶尖、结构清晰的学术写作技能——5 个大型参考文件构成完整的"写作知识库"，正文的两步法+4 阶段工作流可执行性强，21 项 SCORING 与正文映射完整且无自指矛盾。主要风险不在内容而在**测评环境**：强制示意图条款（TEC-01/CF-03）依赖兄弟技能 255-scientific-schematics 的脚本与外部产品 Nano Banana Pro，隔离测评下不可满足；脚本检查的目标文本不确定使 4 项 output_* 检查可能空转。修复优先级：先解决测评环境依赖（🔴1-3），再做编辑层打磨（🟡4-12），预期修复后可达 90+（A）。
