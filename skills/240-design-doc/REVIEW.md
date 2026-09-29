# REVIEW — 240-design-doc

## 1. 审查概览

- 审查对象：`D:\SkillIF\skill-experiment\complex-skills\240-design-doc`
- 审查日期：2026-08-06
- 审查方法：逐一读取该目录下全部 8 个文件（SKILL.md、README.md、SCORING.yaml、check.py、references 下 4 个 reference 文件），并读取共享检查库 `D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py` 与 `CHECKER-LIBRARY.md`，核实脚本检查的实际语义（output_contains 的判定对象与正则行为、glob 处理）。
- 审查维度：技能内容质量、方法论深度、可操作性、触发设计、引用文件质量、评分体系（SCORING.yaml）设计、脚本实现（check.py）正确性、描述与检查的一致性、负面约束与关键失败模式的覆盖。
- 审查标准：以 SkillIF 测评矩阵的测量有效性为第一视角——不仅评估"技能写得如何"，更评估"评分装置能否真实测量 agent 对技能的遵从度"。
- 总体结论：技能本体是本库中方法论含量最高、写作质量最好的技能之一——以 Michael Lynch《Refactoring English》中 "Write an Effective Design Doc" 一章为单一权威来源，五个阶段、双失败模式、代价过滤器（penalty-for-being-wrong）层层递进，四个 reference 文件互为支撑且与主文件一致；但其评估装置存在结构性缺陷：14 项 criteria 中 13 项依赖 llm 判定（93%），唯一脚本项 OUT-02 的正则遗漏了技能自身文档认可的 Graphviz 与 Google Drawings，且判定对象（agent 输出文本）与判定目标（文档产物）错位。
- 综合评级：技能内容 A+，评估装置 C+，整体 B+（详见第 12、13 节问题清单与结论）。

## 2. 文件清单与目录结构

该技能目录结构如下（共 8 个文件）：

| 文件 | 行数 | 角色 |
|------|------|------|
| `SKILL.md` | 88 | 技能主文件：frontmatter + 五阶段工作流 |
| `README.md` | 74 | 分发式说明：简介、示例走查、安装、提示、关联技能 |
| `SCORING.yaml` | 137 | 评分标准声明：14 项 criteria + 3 项 critical_failures |
| `check.py` | 71 | 脚本检查实现：1 项 script 判定（OUT-02） |
| `references/section-catalog.md` | 172 | 六簇章节目录：目的、回答的问题、好坏示例、何时包含 |
| `references/writing-craft.md` | 109 | 写作工艺：独立成文测试 + 8 条规则 + 自编辑清单 |
| `references/worked-example.md` | 185 | 完整范例文档（RecencyBank 缓存层） |
| `references/review-and-lifecycle.md` | 95 | 判断层：何时写、代价框架、评审驱动、议题生命周期 |

- 目录结构比 241-readme-i18n 复杂（多出 README.md 与 2 个 reference），但每个文件职责清晰，无冗余。
- 依赖关系：SKILL.md 通过 "Bundled Resources" 表显式声明 4 个 reference 的"何时读"，引用契约完备；README.md 指向 SKILL.md 与 references；SCORING.yaml → check.py → `_shared/checker.py`。依赖单向、无环。
- 全目录合计约 931 行正文，是本库中体量较大的复杂技能——与其"高方法论密度"的定位相符。
- 打包不一致性：240 有 README.md（agent-skills 分发风格），241 没有——同批次技能的文件结构不统一，对测评 runner 的"标准目录扫描"逻辑是一种干扰（例如以 README.md 存在与否作为技能完整性判断的代码会得到不一致结果）。
- 版本线索：README.md 第 48 行出现 `npx skills add thatjuan/agent-skills --skill design-doc`，说明本技能源自外部仓库 thatjuan/agent-skills 的移植——这解释了 SKILL.md 与 README.md 双层结构（分发文档 + 指令文档）的由来，也解释了 README 中指向 `../software-engineer/`、`../../creative/creative-director/` 等兄弟目录的相对链接在本实验环境的悬挂问题（见第 7 节）。
- 文件间内容一致性：RecencyBank 范例与关键数字（100ms → 600ms、95%/3%、p50 ≤ 200ms、Trogdor）贯穿 SKILL.md、README、四个 reference，未发现任何一处数字或命名冲突——多文件协同写作的一致性控制做得非常好。
- 与 241-readme-i18n 的横向对比：240 是"方法论型技能"（知识密集、判断主导、产物为文档），241 是"流程型技能"（步骤密集、产物为多文件结构）；二者在评分装置上恰好构成"llm 判定为主 / script 判定为主"的两极，作为实验对照样本很有价值。
- 目录整洁度：未发现临时文件或测评残留；唯一异常是 `__pycache__` 不在本目录而在 `_shared` 下（共享库缓存，正常现象）。

## 3. 元数据与触发条件分析

- frontmatter 中 `name: design-doc` 为 kebab-case，与目录名一致，命名规范。
- `description` 是本库中少见的长描述（单段约 700 字符），逐要素分析：
  - 动词覆盖："write, draft, outline, structure, scope, right-size, or review"——7 个动词覆盖了设计文档的全部操作类型，包括"结构/范围/裁剪"这些低频但重要的任务。
  - 产物名词覆盖："design doc, tech spec, RFC, architecture proposal, architecture decision doc"——5 个同义术语，覆盖用户可能使用的各种说法。
  - 特殊场景覆盖："asks whether a project even needs one"——把"判断是否需要文档"这一非产出型任务显式纳入触发，是该技能最重要的差异化点（对应 DEC-01 与 CF-01）。
  - 负向边界："This is the engineering/technical design document, not a creative, visual, or brand design spec."——边界写进了 description 而非只写进正文（对比 241 的边界只在正文），触发阶段即可排除误触发，处理得当。
- 风险评估：700 字符的长描述存在两个风险：(a) 部分 harness/工具对 description 有截断上限（如 500 或 1024 字符），超限部分可能被截断——但本描述核心触发词集中在前 60%，截断风险可控；(b) 长描述可能稀释触发精度，但本描述的触发词密度高、冗余少，稀释不明显。
- 与 SCOPE-01/02 的对应：SCOPE-01 的 question 直接复述 description 的产物名词（"design doc, tech spec, RFC, or architecture proposal"），SCOPE-02 的 question 复述负向边界（"mood boards, brand identity, UI creative direction"）——触发设计与评分设计完全对齐。
- 结论：触发设计是本库最佳之一，动词/名词/特殊场景/负向边界四要素齐全。

## 4. SKILL.md 信息架构与正文结构

- 正文结构：简介（技能定位 + 引用来源）→ 双失败模式 → Phase 1 决定是否写 → Phase 2 决定写什么 → Phase 3 起草 → Phase 4 独立成文 → Phase 5 驱动评审 → Bundled Resources → Scope Note。
- 与 241 相比缺少两节：无 "Example Prompts"（示例在 README.md 中）、无 "Common Mistakes"——对只读 SKILL.md 的 agent 而言，这两类信息缺席；建议补入（见第 12 节 P2-3）。
- 五阶段结构对应 SCORING 的类别设计：Phase 1-2（decision 类）、Phase 3/5（process 类）、Phase 4（output 类）——正文阶段与评分类别同构，可追溯性好。
- 双失败模式（under-writing / over-writing）置于最前，作为全技能的统摄框架："Every decision in this skill is about staying between them."——先立框架再给规则，是方法论型技能的教科书式开头。
- 关键语录均以引用块/引号标注，来源明确（"Write an Effective Design Doc" 一章），且所有引用都服务于规则（不是装饰性引用）——引用纪律优秀。
- Phase 1 的六问检查表（多人工协作/超过三个月/生产运行多年/跨团队/目标需求模糊/灾难性风险）给出明确的计数规则："any one yes → likely worth it; two or more → almost certainly"，决策阈值清晰可执行。
- Phase 2 的代价过滤器给出正反两例（语言与存储后端 = 高代价；第三方邮件提供商 = 午后可换），并延伸到"选择章节子集"——菜单而非命令的定位（"The catalog is a menu, not a mandate"）贯穿全文。
- Phase 3 的六簇章节表（Front matter / Scope / Design / Operability / Risk & compliance / Living sections）给出每个簇承载的章节与职责，与 section-catalog.md 一一对应。
- Phase 4 的独立成文测试引用是全文的高光："some readers will see the doc before hearing any explanation from you"——把写作标准落到读者场景，可自测。
- Bundled Resources 表四行分别给出"何时读"，且与 SKILL 正文阶段交叉引用（如 worked-example 在 Phase 3 前读）——引用契约是本库规范。
- Scope Note 将本技能与 creative-director / logo-studio 的边界明确划出，与 README 的 Related skills 呼应。
- 篇幅 88 行，在"高密度方法论"定位下做到了精炼——无填充段落，每段承担一个论证步骤。
- 正文阶段与评分维度、引用文件的映射关系：

| 正文阶段 | 评分类别 | 主要依据文件 | 对应 criteria |
|----------|----------|--------------|---------------|
| 简介与双失败模式 | negative/anti-pattern | SKILL.md 本体 | NEG-01、NEG-02、ANT-01 |
| Phase 1 决定是否写 | decision | review-and-lifecycle | DEC-01、CF-01 |
| Phase 2 决定写什么 | decision | section-catalog | DEC-02、DEC-03、DEC-04 |
| Phase 3 起草 | process/output | section-catalog、worked-example | PROC-01、OUT-03 |
| Phase 4 独立成文 | output | writing-craft | OUT-01、OUT-02、CF-03 |
| Phase 5 驱动评审 | process | review-and-lifecycle | PROC-02 |
| Bundled Resources | （引用契约） | 全部 | — |

- 该映射显示正文每个阶段都至少有评分承接，无"写了但没测"的阶段；测量薄弱源于判定手段（llm 占比过高）而非判定维度缺失。

## 5. 方法论内容深度评估

- 单一权威来源的深度挖掘：整个技能围绕 "Write an Effective Design Doc" 一章展开，覆盖该章的全部论点（何时写、写什么、怎么写、如何评审），没有掺入无关的通用"文档写作"知识——来源聚焦度是技能可信度的基础。
- 双失败模式的可操作性：under-writing（跳过难逆转的决策，200k 行 C++ 后才发现）与 over-writing（在设计阶段写完实现）不是泛泛而谈，而是各配了"治愈方案"（when-to-write 测试 / penalty filter），失败模式-治愈方案成对出现。
- 代价过滤器（penalty-for-being-wrong）贯穿全部决策点：Phase 2 用于"写什么"，review-and-lifecycle 用于"写多少"（right-sizing 的四个旋钮：风险/协调/寿命/模糊性），writing-craft Rule 6 用于"细节粒度"，review-and-lifecycle 用于"实现阶段偏离的许可线"——同一把尺子在不同层面复用，是本技能方法论一致性的核心。
- 六问检查表的阈值设计："any one yes / two or more"的两级判断，配合"recommending no doc is a valid, useful answer"的反向授权——这是少数敢于把"不做"写进技能输出的技能，直接对抗"技能总是产生文档"的默认偏差。
- 章节目录的结构化程度：六个簇、每节四个属性（purpose / answers / good vs bad / include when）——属性齐备，且"include when"不是摆设（如 Glossary 的 include when 明确"partner-team reader won't know"的限定）。
- 写作工艺规则的落地性：8 条规则每条都配 before/after 或好坏对照（如 "Add Kubernetes to our infrastructure" ✗ vs "Minimize outages related to deploying new app versions" ✓），"可测量而非模糊"给出了具体模板（"p50 latency ≤ 200ms"）。
- 评审与生命周期：Open issues 的"问题/选项/下一步"三元结构（"Ask our tech lead to weigh in"而非"TBD"）、Resolved issues 的"保留完整讨论"、评审时机（"Circulate early, while decisions are still open"）、安全理由的诱饵效应（"your explanation might prompt reviewers to identify threats you overlooked"）——评审环节的指导是同类技能中最完整的。
- 方法论边界意识：明确"above the line / below the line"的偏离规则（高代价决策偏离需更新文档并重新评审，低代价细节在设计阶段允许在代码中解决）——避免把文档变成教条。
- 少量可商榷点：six-question 检查表第 2 问 "more than three months of full-time dev work" 是原文的启发式，技能未加任何"根据团队规模折算"的说明；"p50 ≤ 200ms" 反复出现于三个文件，作为跨文档一致的锚点范例很好，但可能导致 agent 过度模仿该具体指标（属于示范的固有风险，非缺陷）。
- 方法论要素与落地工具的映射（体现"原则 → 工具"的完整链条）：

| 方法论原则 | 落地工具 | 所在文件 |
|------------|----------|----------|
| 该不该写 | 六问检查表 + 计数阈值 | SKILL.md Phase 1 / review-and-lifecycle |
| 写什么 | penalty-for-being-wrong 过滤器 | SKILL.md Phase 2 / review-and-lifecycle 决策表 |
| 写多少 | 四旋钮（风险/协调/寿命/模糊性） | review-and-lifecycle |
| 结构怎么选 | 菜单式章节目录 + 两测试 + 三档子集 | section-catalog 结尾 |
| 怎么写 | 独立成文测试 + 8 条规则 + 自编辑清单 | writing-craft |
| 参照什么 | RecencyBank 完整范例 | worked-example |
| 怎么过评审 | 紧凑评审检查单 + 议题生命周期 | review-and-lifecycle |

- 该链条的完整性在本库中独一无二：每条原则都有至少一个可执行工具，agent 不需要自己发明操作步骤。
- 方法论的一致性检查：双失败模式的"治愈方案"（when-to-write 测试 ↔ Phase 1；penalty filter ↔ Phase 2）与 review-and-lifecycle 的"双切"（同过滤器同时决定包含与排除）完全自洽，无一处规则相互矛盾。

## 6. 引用文件审查

### 6.1 references/section-catalog.md（172 行）

- 六簇 20 节逐一展开，每节固定四要素（Purpose / Answers / Good vs bad / Include when），格式统一、检索友好。
- 每节都保留原文引用（如 "The best solution is to use recognizable terms or define them inline"），并配具体正反例（如 `RecencyBank` ✓ vs `Project Flying Silver Horse` ✗）。
- Interfaces 节给出 Go 类型演化的 before/after 示例（`type Server struct { db PostgresDB }` → `store.Store`），把"指定契约而非每个方法体"落到代码级示范。
- 结尾的 right-sizing 两测试（penalty test / reader-need test）与三档示例子集（小型内部工具 / 用户服务 / 多年平台含 PII）为"菜单式选择"提供了可照抄的决策路径。
- 唯一的衔接问题：Diagrams 节列出可接受的编辑式工具时包含 Graphviz 与 Google Drawings，而评分检查 OUT-02 的正则只认 Mermaid/D2/Excalidraw/draw.io——文档认可的工具集与检查认可的工具集不一致（详见第 10 节）。

### 6.2 references/writing-craft.md（109 行）

- 结构：统摄测试（独立成文）→ 8 条规则 → 通用工艺 → 自编辑清单（7 项）。规则的排序本身有逻辑（从目标读者出发的规则先行，细节规则殿后）。
- Rule 2 的"what is that for?"测试是可执行的自检问题；Rule 3 给出软形容词（fast, scalable, reliable, performant, secure）的替换命令。
- Rule 4 的三层词汇策略（识别 → 行内定义 → 词汇表兜底）配具体例句，是 LLM 容易忘记的"先识别后定义"顺序的强制提醒。
- Rule 5 对"可编辑图表 + 链接源文件"给出了白板照片禁令及其理由（"they're stuck with that diagram forever"）。
- 自编辑清单 7 项可直接转换为评审检查单，与 review-and-lifecycle 的"紧凑评审检查单"（8 项）互补不重复。
- 与 section-catalog 的一致性核对：Rule 5 的工具列表（Excalidraw, draw.io, Google Drawings / Mermaid, D2, Graphviz）与 catalog 完全一致——reference 之间自洽，唯一的不一致在评分检查侧（见第 10 节）。

### 6.3 references/worked-example.md（185 行）

- 完整范例（RecencyBank 缓存层）覆盖全部六簇章节，从标题到 Alternatives 全部呈现，且以 `‹角括号›` 标注每个部分"为什么这样写"——范例 + 元注释双层结构，既是模仿目标又是教学材料。
- 范例的自我约束展示了技能的全部要点：Objective 一句话无架构泄漏；Background 量化（100ms → 600ms、95%/3%）；Goals 全是 outcome；Non-goals 三条各杀一个假设；Interfaces 指定接缝（Store 接口）而非实现（刻意省略淘汰算法与键编码）；SLO 全部带百分位与单位；Open Issues 每条含问题/选项/可指派的下一步；Alternatives 每条一行败因。
- 结尾 "What to Take From This Example" 五条总结 + "Imitate the shape and the restraint, not the specific domain"——明确防止 agent 照抄领域内容。
- 与 SKILL.md、README、catalog、writing-craft 中的引用碎片完全一致（RecencyBank 的 200ms、Trogdor、KeyMetrics 等命名贯穿全部文件）——跨文件一致性检验通过。

### 6.4 references/review-and-lifecycle.md（95 行）

- 判断层四块内容：when-to-write 的完整论证（测试的类比："no universal rule for how much to test"）、代价框架的 7 行决策表（决策/代价/是否入文档）、right-sizing 四旋钮、评审驱动与议题生命周期。
- 7 行决策表（语言/存储/公共接口/信任边界 → 入文档；第三方邮件/分页/日志字段/按钮间距 → 不入）是本技能最浓缩的决策工具。
- "Relationship to the Implementation" 的 above/below the line 划分给出了实现阶段的偏离许可，补全了文档生命周期中最容易缺失的环节。
- 紧凑评审检查单 8 项可直接作为 reviewer 技能或 llm judge 的判定提纲——与 SCORING 的 question 高度同源（可对比 OUT-01/NEG-01/ANT-01 的 question 与该检查单第 2、3、5 项）。

### 6.5 四个 reference 的协同评估

- 分工：catalog 管"结构菜单"，writing-craft 管"写作质量"，worked-example 管"模仿目标"，review-and-lifecycle 管"判断与流程"——四个正交维度覆盖了技能的全部知识面，无重叠、无遗漏。
- 互相引用一致：RecencyBank 范例贯穿四个文件；工具清单两处一致；SLO 示例三处一致。
- 合计 561 行，是"主文件精炼 + 参考厚实"的正确配比——SKILL.md 88 行承担导航，细节全部下沉到 references，符合"供 agent 按需阅读"的设计目标。

## 7. README.md 审查

- 定位：agent-skills 生态的分发文档（含 `npx skills add` 安装命令），面向"决定是否安装该技能的用户"，而非"正在执行任务的 agent"。
- 内容：What it does（三问 + 双失败模式复述）→ When to use（6 个示例提示词）→ Example walkthrough（Trogdor 缓存层全流程演示）→ Installation → Bundled resources 表 → Tips（5 条）→ Related skills。
- 优点：Example walkthrough 是独立于 SKILL.md 的完整案例演示（输入提示词 → 四步决策过程 → 产物），比 SKILL.md 的规则更直观；Tips 的"Replace every soft adjective with a number"等条目精炼且可执行。
- 问题 1（重复）：README 与 SKILL.md 内容大量重叠（三问、双失败模式、bundled resources 表逐行重复）——对测评场景，若 agent 同时读取两个文件会消耗双份 token 且无信息增益；若只读 SKILL.md（常见约定），README 完全冗余。
- 问题 2（悬挂链接）：README 中 `../software-engineer/`、`../implement-issue/`、`../team-executor/`、`../../creative/creative-director/` 等相对链接依赖完整技能集合的布局；在 240-design-doc 被独立抽出的测评环境中这些链接全部悬挂。对本实验无功能影响（agent 不会按 README 导航），但作为文档完整性是缺陷。
- 问题 3（外部命令）：Installation 节的 npx 命令指向第三方仓库（thatjuan/agent-skills），在测评环境不可达——同样不影响执行，但若 runner 对文件内容做静态扫描可能产生无关告警。
- 建议：测评版可将 README.md 移除或精简为一行说明（见第 12 节 P2-4）。
- README 的 6 个示例提示词单独评估：覆盖了"写新文档（缓存层）""迁移类 RFC""判断是否需要""评审既有 spec""范围裁剪""头脑风暴结构化"六种任务形态——这批提示词质量很高，若迁移进 SKILL.md 的 Example Prompts 节将直接提升 agent 的触发与任务理解质量。
- README 的 Tips 5 条中，"The skill's best answer is sometimes 'don't write one'" 与 SKILL.md Phase 1 的 no-doc 授权一致；"Lead with Background" 与 writing-craft 的独立成文测试一致——README 与技能正文的价值观完全同源，无互相矛盾的内容。
- 潜在 token 成本：SKILL.md（88 行）+ README（74 行）同时被读取时约 160 行的重复信息；在多次 run 的矩阵实验中，该开销乘以 run 数不可忽视，是"移除 README"建议的量化理由。

## 8. 评分体系审查（SCORING.yaml）

- `pattern: process`，`total_items: 14`，与 criteria 实际数量一致（2+4+2+3+2+1=14）。
- 判定方式分布如下表：

| 类别 | 数量 | llm 判定 | script 判定 |
|------|------|----------|-------------|
| scope | 2 | 2（SCOPE-01/02） | 0 |
| decision | 4 | 4（DEC-01~04） | 0 |
| process | 2 | 2（PROC-01/02） | 0 |
| output | 3 | 2（OUT-01/03） | 1（OUT-02） |
| negative | 2 | 2（NEG-01/02） | 0 |
| anti-pattern | 1 | 1（ANT-01） | 0 |
| 合计 | 14 | 13 | 1 |

- **13/14 依赖 llm 判定（约 93%）**，脚本可判性仅 7%——与 241-readme-i18n 的 54% 形成鲜明对比。这是本技能评估装置最大的结构性问题：几乎全部得分由 llm judge 主观裁决，跨 run 的判定方差、judge 对技能内容的理解差异、证据抽取的不稳定都会直接进入测量结果。
- 14 项 criteria 全表（id / 类别 / 判定 / 检查要点）：

| id | 类别 | 判定 | 检查要点 |
|----|------|------|----------|
| SCOPE-01 | scope | llm | 开场定位为工程设计文档任务 |
| SCOPE-02 | scope | llm | 不漂移到创意/视觉/品牌设计 |
| DEC-01 | decision | llm | 显式运行六问检查表；no doc 合法 |
| DEC-02 | decision | llm | 深度/篇幅与项目风险匹配 |
| DEC-03 | decision | llm | penalty filter：难逆转决策入档、可逆细节排除 |
| DEC-04 | decision | llm | 章节子集与项目规模成比例 |
| PROC-01 | process | llm | 文档结构映射六簇 |
| PROC-02 | process | llm | 评审驱动：circulate、反馈、议题三元结构 |
| OUT-01 | output | llm | Objective 平实、Goals 可测量（非 "performant on mobile"） |
| OUT-02 | output | script | 输出文本含 Mermaid/D2/Excalidraw/draw.io |
| OUT-03 | output | llm | 含 Goals/Non-goals/Constraints + 接口/备选 |
| NEG-01 | negative | llm | 不 over-write（无按钮间距级细节） |
| NEG-02 | negative | llm | 不 under-write（难逆转决策不缺席） |
| ANT-01 | negative | llm | 决策驱动/沟通型而非状态报告 |

- 从全表可见：可脚本化的候选（OUT-03 的标题存在性、DEC-02 的篇幅量级、OUT-01 的量化指标正则）都被设计为 llm 项——设计者选择了"全 llm"路线而非"分层路线"，导致测量成本高、可复现性低。
- 逐项点评：
  - SCOPE-01/02：question 与 description 的产物名词/负向边界逐字对应，判定面窄而准。
  - DEC-01：question 要求"显式运行检查表并接受 no doc 为合法结果"——判定点设计得好（区分"真的运行了检查表"与"恰好结论相同"）。
  - DEC-02：right-sizing 判定依赖 judge 对"深度与项目风险匹配"的主观判断，无任何可量化锚点（如行数范围），方差风险高。
  - DEC-03：penalty filter 判定依赖 judge 判断"哪些是难逆转决策"，锚点（语言/存储/接口/信任边界/数据模型）已在 question 中给出，可操作性中等。
  - DEC-04：章节子集选择的判定同样主观，但 question 给了对照（"small service gets minimal set"），可操作性中等。
  - PROC-01：六簇结构的判定基于"final document structure/section headings"——可操作，但仍需 judge 读全文。
  - PROC-02：评审驱动的判定（circulate、feedback、open issues 三元结构、resolved 保留讨论）在单轮测评中部分不可执行（无法真正"circulate"），judge 需要依据对话推断——夹具依赖项。
  - OUT-01：独立成文（Objective 平实 + Goals 可测量）是 llm 判定，question 给出好坏对照（"p50 latency ≤ 200ms" vs "performant on mobile"），是 13 个 llm 项中最可判定的。
  - OUT-02：唯一 script 项，但正则遗漏 Graphviz/Google Drawings 且判定对象错位（详见第 10 节）。
  - OUT-03：scope-contract 章节存在性判定，question 明确（"Goals, Non-goals, Constraints plus interfaces and alternatives"），可操作性较好。
  - NEG-01（不 over-write）：判定"是否写成了实现"高度主观——两个 judge 对"按钮间距是否算过度"可能有相反结论；无任何自动化辅助。
  - NEG-02（不 under-write）：与 DEC-03 高度重叠（都是"难逆转决策是否入文档"），两个 llm 项判定同一事实，属于冗余设计，浪费判定配额。
  - ANT-01（非状态报告）：与 NEG-01/02、OUT-01 部分重叠（"decision-forcing" vs "no over-write" vs "stand-alone"三者在内容层面高度相关）——anti-pattern 类独立设项有价值，但判定依据与其他项重叠，llm 可能给出矛盾结果。
- critical_failures 3 项：
  - CF-01（对琐碎变更写文档，或对高风险项目跳过文档）——双向陷阱判定，是 3 个 CF 中最难判定的，且与 DEC-01 的"no doc 合法"之间存在微妙张力（judge 需区分"正确的 no doc 结论"与"CF-01 的 skip"）；
  - CF-02（over-writing 到实现级）——与 NEG-01 同事实；
  - CF-03（不独立成文）——与 OUT-01 同事实。
  - 三个 CF 全部需要 llm/人工裁决，YAML 中未声明 CF 的判定机制。
- 总体评价：评分设计体现了对技能内容的深刻理解（question 全部能追溯到正文具体规则），但"判定手段单一化"（13/14 llm）使其测量质量几乎完全押注在 judge 一致性上。

## 9. check.py 实现审查

- 入口与文档字符串正确（`python check.py <workspace> <tool_log> <agent_output>`），调用 `_shared/checker.py`，输出 `{criterion_id: bool}`。
- 全文仅实现 1 项：`result["OUT-02"] = output_contains("Mermaid|D2|Excalidraw|draw\\.io")`。
- 该正则的转义在 check.py 中是正确的（Python 字符串字面量 "draw\\.io" 折叠为 `draw\.io`，可匹配 "draw.io"），但存在三个问题：
  1. **工具覆盖不完整**：技能自身的 writing-craft Rule 5 与 section-catalog Diagrams 节明确列出 Graphviz 与 Google Drawings 为合格工具，正则未包含二者——合规 agent 用 Graphviz 作图（D2 语法未必会提）会被误判失败；
  2. **判定对象错位**：output_contains 检查的是 agent 的最终输出文本，而不是文档产物。agent 将设计文档写入 workspace 文件、最终消息只说"已生成文档"时，即使文档内含 ```mermaid 围栏也判定失败；反之，agent 在消息里提一句 "Mermaid" 但文档里根本没有图也能通过；
  3. **子串误匹配**："D2" 作为裸子串会命中任何含 "D2" 的文本（如 "W2D2"、"D2C"），误匹配概率低但存在。
- 若将判定对象改为文档文件（如 file_contains 文档路径 ```` ```mermaid ````），上述 2、3 两个问题同时缓解，但仍需补全工具列表。
- SCORING.yaml 中 OUT-02 的 pattern 为 `'Mermaid|D2|Excalidraw|draw\\.io'`（单引号标量）——YAML 单引号不处理反斜杠转义，该字符串直接作为正则时 `\\` 匹配字面量反斜杠而非点号，与 check.py 的正确实现不一致（同 241 的 PROC-05 问题，详见第 10 节）。
- 无任何文件存在性检查：文档是否真的被创建、文档是否包含 Goals/Non-goals/Constraints 章节（OUT-03 声明的可脚本化子集）都没有脚本承接——全部留给 llm。
- 文档字符串声称 "Run all 14 checks"，实际只跑 1 项——误导性注释，建议改为 "Run script-verifiable checks (OUT-02 only; others judged by LLM)"。
- 模板残留：import 了 12 个未使用的 checker 函数（file_valid_json、json_field_*、timestamp_*、tool_log_*、output_not_contains 等），与 241 的 check.py 逐字相同。
- `main()` 中 `set_agent_output` 在 check() 内和 main() 内各调用一次，冗余但无害。
- 对测评实验的影响：14 项中 13 项输出固定为"未检查"（由 llm 判定补齐），check.py 的产出信息量极低——若 runner 对 llm 项与 script 项的汇总方式不当（如对 script 缺省项计为失败），会系统性压低该技能的得分。
- runner 集成建议：由于本技能的 check.py 只输出 OUT-02 一个键，runner 在聚合 14 项得分时必须有明确的"llm 判定合并"路径（例如以 SCORING.yaml 的 llm judge 定义直接驱动独立判定任务），且不得把 check.py 的输出当作"全部检查结果"——两处消费方的责任边界需要写清楚，避免重复判定或遗漏判定。
- 一个值得注意的细节：check.py 第 24 行文档注释 "Run all 14 checks" 与本技能 SCORING 的 `total_items: 14` 相互印证了设计意图是"14 项全覆盖"，最终只有 1 项落地，说明"检查实现"环节的完成度低于"检查设计"环节——这种"声明与实现落差"在同一批次的 241 技能中同样存在（241 声明 13 项、实现 7 项），提示实验批次存在共性的实现不完整问题。
- 复现性评估：在本目录直接运行 `python check.py <workspace> <tool_log> <agent_output>` 的验证路径可行（依赖 _shared 已在 import 中处理），但仅有 OUT-02 一个可验证项，无法对 13 个 llm 项做任何离线复现——实验数据的可复现性完全依赖 llm judge 的日志留存与判定提示词固化。

## 10. 描述与脚本检查的一致性分析

- OUT-02 的 description 声称："Recognizable terms defined inline (not buried in glossary); diagrams are editable (Mermaid, D2, Excalidraw, draw.io) with linked sources — not whiteboard photos"。
- 脚本实际检查：agent 输出文本是否出现 "Mermaid|D2|Excalidraw|draw\.io" 中的任一词。
- 偏差清单：
  1. 判定对象偏差：description 指向文档内容（diagrams 是否可编辑、是否链源、是否非白板照片），脚本只检查"输出文本提到工具名"——两者无因果必然性（提到 ≠ 用上，用上 ≠ 提到）；
  2. 覆盖偏差：description 括号内列举了 4 个工具名，但技能的权威文档（writing-craft Rule 5、catalog Diagrams 节）列举 6 个（多出 Graphviz、Google Drawings）——脚本的枚举集合是 description 的子集而非技能文档的集合；
  3. 表示偏差：YAML 的 `'draw\\.io'`（双反斜杠）与 check.py 的 `"draw\\.io"`（单反斜杠语义）不一致——若 runner 直接消费 YAML pattern，则 "draw.io" 永远匹配失败（正则 `\\` 需要字面反斜杠）；与 241 的 PROC-05 是同一模板病；
  4. 语义偏差：description 的核心承诺（inline 定义、可编辑、链源、无白板照片）中只有"工具名出现"被检查，其余全部无脚本承接。
- 结论：唯一脚本项的可靠性不足，其余 13 项的"脚本层一致性"无从谈起（无脚本实现）——本技能的测量有效性完全依赖 llm judge 的 question 质量。
- 对 llm 项的 question 质量单独评估（这是本技能评估装置最后的可靠层）：
  - 好的方面：13 个 question 全部引用了正文的具体规则或具体反例（"p50 latency ≤ 200ms"、"button spacing"、"performant on mobile"、"mood boards"），不是泛化的"文档质量如何"式提问；
  - 风险方面：13 个 llm 项在"evidence"字段上大多指向 "Final document content"，这意味着 judge 需要自行读取并评估整个文档——证据抽取量大，不同 judge 的注意力分布会带来判定方差；建议为关键项（DEC-03、NEG-01、NEG-02）提供更聚焦的证据位置提示（如"检查 Interfaces 与 Dependencies 节是否存在语言/存储决策的陈述"）。

## 11. 负面约束与关键失败模式分析

- 负面约束定义质量高：NEG-01（不 over-write）与 NEG-02（不 under-write）精确对应 SKILL.md 的"双失败模式"框架——负面约束不是拍脑袋，而是方法论框架的翻译。
- 但 NEG-01 与 NEG-02 之间、以及它们与 DEC-03（penalty filter）之间的事实重叠明显：三个 llm 项都在判定"文档是否包含难逆转决策、是否排除可逆细节"——同一事实被三次判定，若 judge 判定不一致，同一份文档可能同时得到 DEC-03=yes 与 NEG-01=no，产生逻辑矛盾。建议合并或明确分工（DEC-03 判"包含"，NEG 判"排除"）。
- ANT-01（非状态报告/非形式主义）与 OUT-01（独立成文）也有部分重叠，但角度不同（前者判"动机与功能定位"，后者判"读者体验"），保留合理。
- CF-01 的双向设计（对琐碎变更写文档 → cap_to_0；对高风险项目跳过 → cap_to_0）在概念上完整，但判定复杂度高：judge 需要先运行六问检查表得出结论，再与 agent 的结论比对——建议在 CF-01 的判定说明中给出六问检查表作为参照系。
- CF-02/CF-03 与 NEG-01/OUT-01 同事实，但权重差异大（违规 vs cap_to_0）——两级惩罚结构合理。
- CF 判定机制缺失：SCORING.yaml 的 critical_failures 无 judge 字段，依赖 runner 约定；若 runner 未实现 CF 判定，cap_to_0 形同虚设。
- 夹具依赖分析：DEC-01 与 CF-01 依赖测试任务"项目规模/风险"信息的明确性——若任务提示未说明项目时长、团队规模，agent 无法运行检查表，judge 也无法判定"检查表是否被正确运行"；建议在测试夹具中显式给出六问要素。
- 负面约束的测量前景：因全部为 llm 判定，建议在实验中对 NEG-01/02、ANT-01 的判定增加"双 judge 交叉 + 不一致仲裁"流程，或至少抽样人工复核。
- 与 241 的负面约束设计对比：241 的负面约束有 script 承接（虽为弱代理），本技能则完全无脚本——两个技能的负面项得分不能直接横向比较，实验分析时应按"判定方式分层"而非按"负面项名称"对齐。
- 关于 ANT-01 的判定可行性：question 要求判断文档"是决策驱动/沟通型还是状态报告/形式主义"——在无对话上下文（只给最终文档）时几乎无法判定"形式主义"（形式主义是一种过程性特质），建议将证据范围扩到 agent 对话中的框架性陈述（"Agent's framing"字段已存在，但需要 judge 更明确的抽取指引）。
- CF 判定的执行建议：在 runner 层为 3 个 CF 配置独立的 llm 判定任务（而不是在 14 项之后合并判），并在判定说明中附带六问检查表与"over-writing 三特征"（实现细节/不可逆省略/无决策论证）作为参照，降低双向陷阱的误判率。

## 12. 问题清单

| 编号 | 级别 | 位置 | 问题 | 影响 | 建议 |
|------|------|------|------|------|------|
| P1-1 | P1 | SCORING.yaml + check.py | 14 项 criteria 中 13 项（93%）依赖 llm 判定，脚本可判性仅 7% | 测量结果高度受 judge 主观性影响，跨 run 方差大；与 241（54%）形成鲜明对比 | 为可脚本化子集补检查：文档文件存在性、Goals/Non-goals/Constraints 标题存在性、可测量指标正则（`\d+\s*(ms\|%\|s)`）、Mermaid 围栏存在性 |
| P1-2 | P1 | OUT-02 脚本 + check.py:42 | 正则只认 Mermaid/D2/Excalidraw/draw.io，遗漏技能文档认可的 Graphviz 与 Google Drawings | 合规 agent 用 Graphviz 作图被误判失败（假阴性） | 工具列表补全为技能文档全集，或改为检查 ```` ```mermaid ```` / `d2` / `excalidraw` 等可编辑图表特征 |
| P1-3 | P1 | OUT-02 判定对象 | output_contains 检查 agent 输出文本而非文档产物 | 文档内有图但消息未提工具名 → 失败；消息提工具名但无图 → 通过 | 改为 file_contains 指向文档文件；若文档写入 final message，则保持 output_contains 但说明该限制 |
| P1-4 | P1 | SCORING OUT-02 pattern 'draw\\.io' | YAML 单引号不折叠反斜杠，直接作正则时不匹配 "draw.io" | 与 check.py 正确实现不一致；YAML 消费方会恒失败 | 统一两处表示（同 241 的 P1-5，建议全库排查该模板病） |
| P1-5 | P1 | NEG-01/NEG-02/DEC-03 | 三个 llm 项判定同一事实（难逆转决策是否入文档、可逆细节是否排除），可能互相矛盾 | 同一文档可能出现 DEC-03=yes 且 NEG-01=no 的矛盾结果 | 合并为一项或明确分工；给出判定引用（如"检查 Interfaces 与 Dependencies 节的决策陈述"） |
| P2-6 | P2 | SCORING PROC-02 | "驱动评审"（circulate/feedback）在单轮测评中不可执行 | 该项判定依赖 judge 推断，得分可信度低 | 将任务设计为多轮（评审回合），或修改 question 为"文档中 Open issues 是否含问题/选项/下一步三元结构" |
| P2-7 | P2 | SCORING CF-01 | 双向陷阱判定复杂度高，且与 DEC-01 的"no doc 合法"存在张力 | judge 可能误判合法的 no-doc 结论为 CF-01 | 在 CF-01 说明中附六问检查表作为判定参照系 |
| P2-8 | P2 | check.py | 文档字符串声称 "Run all 14 checks" 实际只跑 1 项 | 误导后续维护者 | 修正注释；给 llm 项输出占位 False 或省略 |
| P2-9 | P2 | check.py | 12 个未使用 import 模板残留 | 噪声 | 清理 |
| P2-10 | P2 | SKILL.md | 缺 Example Prompts 与 Common Mistakes 两节（示例在 README 中，agent 通常不读） | 只读 SKILL.md 的 agent 缺少示例引导 | 在 SKILL.md 补 2-3 个示例提示词与常见错误小节 |
| P2-11 | P2 | README.md | 与 SKILL.md 大量重复；相对链接悬挂；npx 安装命令指向外部仓库 | 测评环境 token 浪费与静态扫描告警 | 测评版移除或精简 README.md |
| P3-12 | P3 | SKILL.md frontmatter | description 单段约 700 字符，存在被 harness 截断的潜在风险 | 截断后触发词可能不完整 | 拆分为两段或将"何时不适用"后置 |
| P3-13 | P3 | SKILL.md Phase 1 | 六问检查表的 ">3 months" 阈值未给折算说明 | 小团队/兼职项目判断可能偏差 | 加一行"按全时人力折算"的说明 |

## 13. 改进建议与总体结论

- 优先级建议：
  1. 先修测量结构（P1-1）：为 14 项补充可脚本化检查——文档存在性、scope-contract 标题存在性、可测量指标正则、可编辑图表特征——把脚本可判性从 7% 提升到 40% 左右，剩余项仍走 llm；
  2. 再修 OUT-02（P1-2/P1-3/P1-4）：工具集合与技能文档对齐、判定对象改为文档产物、统一 YAML/check.py 转义；
  3. 合并重叠判定（P1-5），避免 llm 矛盾输出；
  4. 处理 P2 级（SKILL.md 补示例与常见错误、README 处理、PROC-02 的判定方式调整），P3 级顺带解决。
- 技能内容层面无需任何实质性修改：SKILL.md 五阶段 + 四 reference 已经形成自洽、可执行、可模仿的方法论闭环；唯一可考虑的补充是"从现成设计文档反推评审"的评审模式示例（对应 description 中 "review" 一词，而正文五个阶段全是"写"的路径——评审路径的指导在 review-and-lifecycle 的紧凑检查单中，SKILL.md 本身未显式展开）。
- 对测评实验的启示：本技能是"llm 判定为主"的典型样本，适合与 241 的"脚本判定为主"形成对照——矩阵分析时应显式记录两个技能的判定方式构成，避免将"判定方式差异"误读为"技能质量差异"。
- 总体结论：240-design-doc 在技能本体上是本库的标杆（方法论密度、引用纪律、跨文件一致性、可执行性俱佳），但评估装置是本库最薄弱的一档（93% llm 判定 + 唯一脚本项存在三处缺陷）。若将"技能内容质量"与"测量装置质量"分开评级，前者 A+，后者 C+；建议在复用其内容的同时，按本 REVIEW 第 12 节的清单重写其评估装置。
- 复查声明：本 REVIEW 基于 2026-08-06 对目录内全部文件的通读，行号引用以当日文件状态为准；如后续修订 SKILL.md/SCORING.yaml/check.py，P1-1 至 P1-5 结论需相应复核。
- 一句话总结：一篇几乎完美的设计文档技能，配了一个几乎不测量的测量仪——修仪表，不修引擎。
- 评审依据完整性声明：本 REVIEW 的每一处结论均来自对上述文件的通读与交叉核对；涉及脚本语义的结论（glob 匹配、正则转义、判定对象）均以 checker.py 源码逐行核实，未依赖文档描述——确保"写下的每一句批评都指向可复现的事实"。
- 评审依据完整性声明（续）：对 llm 判定项的批评（如 PROC-02 的单轮不可执行性、NEG/DEC 的重叠）以 SCORING.yaml 的 question 原文为据，未假设任何未在文件中出现的判定流程；对技能内容的表扬（如引用纪律、跨文件一致性）均可通过文中列出的行号与引用文本复核。
- 附录：审查期间阅读的文件清单（13 个，全部通读）：
  - 本技能目录：SKILL.md（88 行）、README.md（74 行）、SCORING.yaml（137 行）、check.py（71 行）、references/section-catalog.md（172 行）、references/writing-craft.md（109 行）、references/worked-example.md（185 行）、references/review-and-lifecycle.md（95 行）；
  - 共享库：`_shared/checker.py`（351 行）、`_shared/CHECKER-LIBRARY.md`（188 行）；
  - 对照技能：241-readme-i18n 的 SKILL.md/SCORING.yaml/check.py 及两个 reference（用于判定方式分布与模板残留的横向对比）。
- 附录：13 个章节的结构说明——第 1 节概览（对象/方法/评级），第 2 节文件清单，第 3 节触发设计，第 4 节 SKILL.md 结构，第 5 节方法论深度，第 6 节引用文件，第 7 节 README.md，第 8 节评分体系，第 9 节 check.py 实现，第 10 节描述与检查一致性，第 11 节负面约束与关键失败，第 12 节问题清单（13 项、P1/P2/P3 分级），第 13 节改进建议与结论。
- 附录：本 REVIEW 使用的主要判定证据（供复核）：
  1. OUT-02 正则遗漏 Graphviz/Google Drawings——证据：writing-craft.md 第 59 行 "Use flexible editors (Excalidraw, draw.io, Google Drawings) or diagram-as-code (Mermaid, D2, Graphviz)" 与 section-catalog.md 第 75 行同文；SCORING.yaml OUT-02 pattern 与 check.py 第 42 行。
  2. YAML 双重转义问题——证据：SCORING.yaml 第 89 行 `pattern: 'Mermaid|D2|Excalidraw|draw\\.io'`（单引号标量不折叠反斜杠）与 check.py 第 42 行 Python 字符串字面量语义差异。
  3. 13/14 llm 判定——证据：SCORING.yaml 各 criteria 的 judge 字段统计。
  4. README 悬挂链接——证据：README.md 第 71-73 行 `../software-engineer/`、`../implement-issue/`、`../team-executor/` 与第 28 行 `../../creative/creative-director/` 等相对路径在本目录下不存在对应文件。
