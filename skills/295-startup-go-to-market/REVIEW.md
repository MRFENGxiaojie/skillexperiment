# REVIEW — skill 295-startup-go-to-market

审查日期：2026-08-06
审查对象：`D:\SkillIF\skill-experiment\complex-skills\295-startup-go-to-market\`
审查方式：目录 Glob 全量枚举 → 每个文件全文通读（SKILL.md 255 行、SCORING.yaml 184 行、check.py 66 行）→ 按 13 节结构化出具意见。
结论速览：技能主题聚焦、正文写作质量中等偏上、SCORING 与正文高度自洽，但存在 6 处指向不存在文件的引用（资产文件整体缺失），直接影响可执行性，属于本审查最严重问题。综合评分 78/100。

---

## 1. 目录清单

目录共 3 个文件，无任何子目录：

| 文件 | 大小/行数 | 类型 | 说明 |
|------|-----------|------|------|
| `SKILL.md` | 255 行 | 主技能文件 | 完整的 GTM 工作流正文 |
| `SCORING.yaml` | 184 行 | 测评标准 | 20 个判分项 + 3 个一票否决项 |
| `check.py` | 66 行 | 脚本检查器 | 0 个脚本判项，全部委托 LLM judge |
| `assets/` | 不存在 | 子目录 | SKILL.md 引用了 3 个该目录下的文件，实际缺失 |
| `references/` | 不存在 | 子目录 | SKILL.md 引用了 2 个该目录下的文件，实际缺失 |
| `data/` | 不存在 | 子目录 | SKILL.md 引用了 1 个该目录下的文件，实际缺失 |

这个清单本身就暴露了第一个问题：SKILL.md 的正文中出现了 `assets/icp-definition.md`、`assets/gtm-strategy.md`、`assets/launch-playbook.md`、`references/plg-implementation.md`、`references/sales-motion-design.md`、`data/sources.json` 共 6 个"技能内部文件"引用，但目录里既没有这些文件，也没有对应的三个子目录。技能自称"完整"，实际是一棵被引用了一半、另一半没有落地的树。

---

## 2. Frontmatter

### 2.1 name 字段

`name: startup-go-to-market`，与目录名 `295-startup-go-to-market` 去掉编号前缀后完全一致，与 SCORING.yaml 的 `skill: startup-go-to-market` 也一致。命名合规。

### 2.2 description 字段

描述原文（SKILL.md 第 3 行）：

> Go-to-market strategy design and execution. Use when designing go-to-market strategy, selecting GTM motion (PLG/sales-led), defining ICP, planning product launches, or implementing AI-powered GTM automation. Covers channel selection, growth loops, RevOps alignment, and market entry execution.

逐项核对：
- 第三人称：以"Go-to-market strategy design and execution"（名词短语陈述 WHAT）开头，其后为"What"内容，"Use when..."是标准触发句式。整体满足第三人称要求。
- WHAT：本技能做什么（GTM 策略设计与执行）交代清楚。
- WHEN/触发信号："Use when designing go-to-market strategy, selecting GTM motion, defining ICP, planning product launches, implementing AI-powered GTM automation"——五类触发任务明确，信号词（designing/selecting/defining/planning/implementing）具有可判别性。
- KEYWORDS：GTM motion、PLG、sales-led、ICP、channel selection、growth loops、RevOps、market entry，覆盖了正文核心概念。
- 长度：约 290 个字符（含标点），远低于 1024 上限。

结论：描述是本次审查中质量最高的部分，WHAT+WHEN+KEYWORDS 三要素齐全且不超过字数上限。

### 2.3 可选字段检查

Frontmatter 仅声明了 `name` 和 `description`。规范允许的可选字段（allowed-tools、argument-hint、user-invocable、model、paths、disable-model-invocation）一个都没有出现。这是合规的——所有可选字段都是"可选"，不写不违规。但值得指出：本技能没有 `allowed-tools`，意味着 agent 可以用任意工具执行 GTM 任务；考虑到 GTM 设计主要依赖读写与网络检索，不放工具限制是合理的选择，可以不补。

### 2.4 Frontmatter 与正文开头的呼应

Frontmatter 之后正文标题为"# Startup Go-to-Market"，并有一行"Systematic workflow for designing and executing market entry, launch, and growth."作为定位句，与 description 的 WHAT 呼应良好。

### 2.5 Frontmatter 小结

Frontmatter 本身没有问题，唯一可以吹毛求疵的是描述中的 "AI-powered GTM automation" 承诺了正文并未充分兑现的内容（见 4.2 与 8.6）。

---

## 3. Body 结构

### 3.1 整体骨架

正文从第 6 行到第 255 行，结构为：

1. 定位句 + Modern Best Practices（L8-10）
2. When to Use（L14-20）
3. When NOT to Use（L22-27）
4. Quick Start (Inputs)（L31-44）
5. Workflow（L46-69，6 步）
6. Decision Tree（L73-82）
7. GTM Motion Types + Motion Selection Framework（L86-104）
8. ICP Components + ICP Scoring（L108-126）
9. Channel Strategy + Channel Sequencing by Stage（L130-146）
10. Measurement + PQL 公式 + Product-Led Sales 检查清单（L150-170）
11. Launch Types（L174-181）
12. Growth Loops（L185-194）
13. Do / Avoid（L198-214）
14. Resources / Templates / Data 三张表（L218-232）
15. Related Skills（L236-244）
16. What Good Looks Like（L248-254）

### 3.2 Workflow / Process 覆盖

第 46-69 行的 6 步工作流是全文的核心资产：ICP 与购买路径 → 定位与证据 → 动型选择 → 渠道排序 → 度量与 RevOps → 交付物与运营节奏。步骤之间有顺序依赖，每一步都有产出物或判据，具备"流程感"。第 3 步给出决策框架、第 4 步给出"测—量—加倍"的试验逻辑，第 5 步给出 PQL→SQL 路由与 SLA 的可度量交接，第 6 步给出交付物与周会节奏（30+30+30 分钟）。流程设计合理且可操作，这是正文最有价值的段落。

### 3.3 Output Format 覆盖

规范要求 Body 必须包含"Workflow/Process + Output Format + Scope/Limitations"三件套。本技能的 Output Format 是最薄弱的一环：没有独立的"输出格式"或"交付物结构"章节。"What Good Looks Like"（L248-254）提供了 5 条产出质量判据，在精神上接近输出规格；Workflow 第 6 步也点名了 `assets/gtm-strategy.md` 与 `assets/launch-playbook.md` 两个交付物——但这两个文件并不存在。也就是说，唯一的"输出格式"载体是断链。这是一个需要修复的结构性缺口。

### 3.4 Scope / Limitations 覆盖

"When NOT to Use"（L22-27）明确列出了 4 类不做的事（定位与信息传达深潜、竞争情报、融资、定价与收入模型）并给出转介技能名。这是合格的 Scope 声明。不足之处是缺少"限制"维度：例如对受监管行业、面向非软件产品、单次会话产出规模等边界没有任何说明，也没有"本技能不做全渠道预算分配"这类明确 disclaimer。

### 3.5 Body 行数

255 行，远低于 600 行上限。行数合规。

---

## 4. 逻辑一致性

### 4.1 正文内部一致性

- ICP 评分权重（L121-126）：预算 20% + 问题严重度 25% + 技术契合 15% + 决策时间线 15% + 冠军 15% + 扩张潜力 10% = 100%，权重闭合，且"冠军 15%"与购买路径步骤中"经济买家 vs 冠军"的区分呼应。
- PQL 公式（L158）：Engagement×0.4 + Fit×0.3 + Intent×0.3 = 1.0，权重闭合。
- Motion Selection Framework（L99-104）与 GTM Motion Types 表（L88-94）逻辑一致：PLG 用于低 ACV + 自助服务，销售主导用于企业级复杂销售，社区主导用于开发者工具。
- Do/Avoid（L198-214）与 When to Use、Measurement 相互自洽："Scaling paid before activation/retention is stable"（Avoid）与"Track leading indicators before scale decisions"（Measurement L154）是同一件事的两种表述，无矛盾。
- Launch Types（L174-181）的时间线（soft 2-4 周、beta 4-8 周）与自身表内数字一致。

### 4.2 description 与正文的一致性

大部分对应良好：description 中的 PLG/sales-led、ICP、launch、channel、growth loops、RevOps 都能在正文找到实体章节。唯一落空的是 "implementing AI-powered GTM automation"：正文只在 Modern Best Practices（L10）与 Do/Avoid（L204、L212）各提了一句"用 AI 执行、不把策略交给 AI"，没有给出任何"如何落地 AI GTM 自动化"的步骤、工具或判据。触发词承诺了、正文没兑现，agent 被该关键词触发后无法从技能内获得对应指导。属中等问题。

### 4.3 引用关系一致性

- 正文引用了 6 个内部文件（见第 1 节清单），全部不存在。Workflow 第 1、3、6 步与 Data 表各依赖至少一个缺失文件，导致步骤产出物的定义空洞化。
- 跨技能引用（marketing-content-strategy、startup-competitive-analysis、startup-fundraising、startup-business-models、marketing-ai-search-optimization、marketing-social-media、marketing-leads-generation）均为技能名而非文件路径，符合"无跨技能文件路径"约束。
- 但存在重复引用：startup-competitive-analysis 和 startup-business-models 同时出现在"When NOT to Use"（转介）与"Related Skills"（协作）两张表里，位置不同、语义不同，不算错误，但读者需要分辨"转介"与"协作"两种关系，表意略混。

### 4.4 数字与判据的一致性

全文出现的所有可量化判据（权重、公式、时间线、周会分钟数、ACV 阈值 $5K、PQL 首触 SLA <24 小时）在正文内部、以及正文与 SCORING.yaml 之间均一致，没有一处数字打架。这在复杂技能里是难能可贵的（详见第 10 节交叉验证）。

---

## 5. 参考文件（全文通读）

本节对目录内每个文件做全文级内容分析。注意：本技能没有独立的"参考资产"文件，因此本节覆盖全部 3 个文件本身。

### 5.1 SKILL.md（255 行，全文通读）

已在上文第 3、4 节逐段分析，此处补充按段落的阅读笔记：

- **L8-10 Modern Best Practices**：以"Jan 2026"锚定时效。好处是让用户知道这是新鲜版本，坏处是硬编码日期会快速过期、且日期本身与正文知识无逻辑关联。推荐改为"当前版本要点"之类不带日期的表述。
- **L14-27 使用/不使用清单**：共 9 个 bullet。When NOT to Use 的写法"X -> the `xxx` skill"简洁有效，但第一条（L24）与后三条（L25-27）的措辞不完全对称（第一条在技能名前有"the"，后三条把"the"放在箭头后），小瑕疵。
- **L31-44 Quick Start**：8 类输入（阶段、产品与品类、ICP 与买家、定价与经济性、动型约束、渠道约束、基线指标、团队与工具）。这一段是全文人机感最好的部分——"Ask for the smallest set of inputs that makes decisions meaningful"这句话直接定义了 agent 的提问原则，且 L44 明确"数字缺失时用区间 + 显式假设推进，并列出下一步要测什么"，与 SCORING 的 SCOPE-03 完全对齐。
- **L46-69 Workflow**：6 步流程，见 3.2。第 1 步依赖缺失文件；第 4 步"refer to channel playbook best practices"（L61）是一句空洞的兜底话术——"channel playbook"在正文中不存在，没有任何表或文件叫这个名字，agent 读了这句话得不到任何指引。
- **L73-82 Decision Tree**：名为"决策树"，实为"问题→主题"的目录映射（"How do I reach customers?" → Channel Strategy），四条分支没有给出任何判断条件或结果，不能指导任何决策。要么补成真正的带条件分支决策树，要么删除以免误导。
- **L86-126 动型与 ICP**：两张表 + 一个分支框架，内容扎实。ICP Scoring 权重闭合并附例值。
- **L130-146 渠道策略**：渠道分类表 + 按阶段排序表，二表互补（横向分类、纵向分阶段），是本技能信息密度最高的部分。
- **L150-170 度量**：PQL 公式与 PQL→SQL 路由 5 项检查清单（触发与阈值、排除条件、SLA、交接 AE 判据、结果埋点），清单可勾选、可直接执行。
- **L174-194 启动类型与增长飞轮**：两张表。Growth Loops 的"Mechanism"列写得像循环（Revenue → Ads → Users），比普通列表更有价值。
- **L198-214 Do/Avoid**：6 条 Do、7 条 Avoid（按行数计），全部是可操作断言。Avoid 的前两条（内容垃圾邮件、并行铺渠道）与 SCORING 的 NEG-01/02 一一对应。
- **L218-232 三张资源表**：Resources 表与 Templates 表是空表（只有表头、零数据行），Data 表只有一行且指向不存在的 `data/sources.json`。三个小节占了 15 行却贡献为零，是最明显的"半成品"痕迹。
- **L236-244 Related Skills**：5 个协作技能，关系说明清晰（GEO/AI 搜索可见性、社交渠道执行、线索获取等均为 GTM 的执行侧配套）。
- **L248-254 What Good Looks Like**：5 条质量标准，与 SCORING FMT-01 逐条对应，是正文与测评体系之间最重要的桥梁。

### 5.2 SCORING.yaml（184 行，全文通读）

- **头部**：`skill: startup-go-to-market`、`pattern: process`、`total_items: 20`。实际判分项 SCOPE 3 + PROC 7 + DEC 4 + FMT 2 + NEG 3 + QA 1 = 20，与声明一致。
- **SCOPE-01/02/03**：覆盖"识别 GTM 任务并收集输入""越界请求转介""缺数字时用区间推进"三件事，全部对应正文的可验证行为。SCOPE-02 的转介清单与正文 L22-27 的 4 个技能逐一对上。
- **PROC-01/02/03/04/05/06/07**：七项与 Workflow 六步基本一一对应（PROC-07 是测量主题的补充项）。PROC-02 精确复述了动型框架的分支条件，PROC-04 精确复述了按阶段渠道表，PROC-06 精确复述了 30+30+30 周会。
- **DEC-01/02/03/04**：决策类四项。DEC-02 给了两个合法路径（按权重表打分或按契合+意图信号分层），给 agent 留了灵活性；DEC-04 把 Avoid 表中的两条（paid 扩展时机、基准误用）转化为判据。
- **FMT-01/02**：FMT-01 把 What Good Looks Like 五要素逐条嵌入 question；FMT-02 自带豁免逻辑（"Answer yes if no hybrid motion is recommended"），是良好的测评设计。
- **NEG-01/02/03**：负向判据，与 Do/Avoid 对应。NEG-03（AI 只做执行、不拥有策略）是全部判据中唯一直接挂钩 Modern Best Practices 的项。
- **QA-01**：要求输出包含"显式成功指标 + 停止/转向触发条件"，与 FMT-01 的第 3 条有部分重叠（两者都谈 stop/pivot triggers），重叠不算冗余，但说明判项之间的独立性不是最优。
- **CF-01/02/03**：三个一票否决项（无 ICP、并行铺渠道、无测量计划）全部对应正文的强制条款，cap_to_0 语义合理。CF-03 尤其关键——它保证"策略 + 无测量"永远不及格。
- **总体评价**：判项粒度合理（20 项对 255 行正文），每题都有 evidence 提示，question 全部是闭卷可答的是非题。SCORING.yaml 是这套技能里质量最高的文件，与正文的一致性近乎完美。

### 5.3 check.py（66 行，全文通读）

- **结构**：标准 runner 接口（`check(workspace, tool_log, agent_output)` 返回 `{id: bool}`），`main()` 校验 4 个参数、读 agent 输出文件、打印 JSON。符合 `_shared` 库的约定（L11-15 从 `../_shared/checker` 导入）。
- **判项覆盖**：20 个判分项全部为 llm judge，脚本 0 个判项。docstring 明说"Run all 0 script checks"，注释把 7 个类别逐一标注"not checked here"，诚实且不误导。
- **潜在缺陷（latent bug）**：`main()` 先读文件并用文件内容调用 `set_agent_output`（L54-56），随后调用 `check()`；而 `check()` 的第一行又是 `set_agent_output(agent_output)`（L21）——把刚写入的文件内容覆盖成"文件路径字符串"。当前 0 个脚本判项，所以这个覆盖没有实际后果；但一旦未来加入任何依赖 agent 输出的脚本判项，就会静默读到错误数据。这是需要顺手修掉的时序问题。
- **其他**：`workspace` 参数完全未使用（合法，因为无文件系统检查）；异常路径（文件不存在）静默跳过读取。整体是一个诚实但"壳化"的检查器——20 项全部依赖 LLM judge，意味着运行成本完全落在评测侧的推理开销上。

---

## 6. 语法格式

### 6.1 Markdown 语法

SKILL.md 的 Markdown 语法整体正确：表格全部有表头分隔行、代码块（Decision Tree、Motion Selection Framework、PQL 公式）用反引号围栏正确闭合、粗体与行内代码使用一致。通读未发现未闭合的表格或围栏。

### 6.2 表格规范性

全文 9 张表格，列数一致、对齐规整。唯一问题是两张空表（Resources L218-221、Templates L223-226）——语法合法但内容为零。

### 6.3 代码块与公式

三个代码块（决策框架 ×2、PQL 公式 ×1）格式正确，且均被 SCORING 引用为判据来源。PQL 公式在正文是数学表达式、在 SCORING PROC-07 是文字复述，两者一致。

### 6.4 YAML 有效性

SCORING.yaml 语法有效：缩进两级规范、`judge: llm` 与 `check:` 子结构一致、列表项以 `- id:` 开头、注释（`# ── Scope (3 items) ──`）使用规范。全部 20 个判项结构完全相同，无畸形条目。

### 6.5 Python 有效性

check.py 语法有效，可直接执行（`python check.py` 无参数时打印 usage 错误并 exit 1，符合预期行为）。导入 `_shared/checker` 是外部依赖，该文件存在于上级 `_shared` 目录时方可运行——属于合理的共享库约定，不是本技能的问题。

### 6.6 命名与书写一致性

- 技能名/目录名/SCORING skill 名三者一致。
- 跨技能引用存在两种格式混用：When NOT to Use 用"`startup-competitive-analysis` 技能"式行内引用，Related Skills 用表格并加"the"冠词前缀（"the `startup-competitive-analysis` skill"）。两种格式各自内部一致，混用不破坏可读性，但统一会更专业。
- 中英混排、大小写（GTM、ICP、PQL、SQL、ACV、RevOps、PLG）全文一致。

---

## 7. 规范合规（12 项清单）

对照任务 SPEC 逐项核验：

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 技能名与目录编号/命名一致 | ✅ |
| 2 | description 为第三人称 | ✅ |
| 3 | description 含 WHAT（做什么） | ✅ |
| 4 | description 含 WHEN + 触发信号（Use when...） | ✅ |
| 5 | description 含 KEYWORDS | ✅ |
| 6 | description ≤1024 字符 | ✅（约 290 字符） |
| 7 | Frontmatter 仅含允许字段（name/description + 可选字段白名单） | ✅ |
| 8 | Body 含 Workflow/Process | ✅（6 步工作流） |
| 9 | Body 含 Output Format | ⚠️（仅 What Good Looks Like，无独立输出格式节，且交付物文件缺失） |
| 10 | Body 含 Scope/Limitations | ✅（When NOT to Use） |
| 11 | Body ≤600 行 | ✅（255 行） |
| 12 | 无跨技能文件路径（引用其他技能只允许技能名） | ✅（7 处跨技能引用均为技能名） |

结论：12 项中 11 项通过、1 项部分通过（第 9 项）。本技能在"硬性格式规范"上几乎全部达标，扣分集中在"输出格式"这一结构性要求上。

---

## 8. 人机感

### 8.1 阅读体验

正文信息密度高、段落短、表格化程度高，适合 agent 快速检索。对人类的可读性也不错——9 张表的"Best For / Examples"列让抽象概念立刻有了锚点（Slack、Figma、Salesforce、Dropbox、HubSpot）。

### 8.2 指令清晰度

大多数指令是"做什么 + 怎么判断"成对出现。最好的例子是 Quick Start（L33-44）——不仅列出要收集的 8 类输入，还规定了收集原则（最小输入集）和缺失时的推进策略。Motion Selection Framework 的三行分支是全文指令最清晰的段落。最差的例子是 L61 "refer to channel playbook best practices"——被指称的对象不存在，agent 会在此处失焦。

### 8.3 语气与文风

全程祈使句 + 断言式建议（"Do not do all channels in parallel"），语气坚定、不绕弯，符合"给 agent 当操作手册"的定位。Modern Best Practices 的定位句（L10）以"Start from ICP + positioning..."开篇，有"首席顾问式"的口吻，人味足够。

### 8.4 冗余与缺失

- 冗余点：When NOT to Use 与 Related Skills 对 startup-competitive-analysis、startup-business-models 的重复提及（见 4.3）；Decision Tree 与目录结构重复（见 4.1 之外的补充：其四个分支标题与正文各节标题一一对应，等于把目录又画了一遍）。
- 缺失点：没有任何示例会话、没有"一个完整 GTM 计划长什么样"的迷你样例、没有对输出长度/格式的最低要求。对"输出格式"维度的缺席已在 3.3 说明。

### 8.5 面向 agent 的导航性

"When to Use / When NOT to Use / Quick Start / Workflow"四段构成清晰的路由层与执行层：触发判定 → 输入收集 → 分步执行。跨技能转介写在同一段落中（L24-27），agent 不需要翻页就能完成路由。导航性良好。

### 8.6 AI 主题的人机分工

技能坚持"AI 用于执行、人拥有策略"（L10、L204），并把它上升为 SCORING 的负向判据 NEG-03——这是本技能在 AI 主题上最有态度、也最可测评的立场。但正如 4.2 所说，正文对"AI 自动化具体做什么、怎么落地"只有原则没有做法，人机感在原则层满格、在操作层欠账。

---

## 9. 可执行性

### 9.1 引用可解析性（本技能最大的短板）

6 处内部文件引用全部无法解析：

| 引用位置 | 引用的文件 | 实际存在 |
|----------|-----------|----------|
| SKILL.md L50（Workflow 第 1 步） | assets/icp-definition.md | ❌ |
| SKILL.md L57（Workflow 第 3 步） | references/plg-implementation.md、references/sales-motion-design.md | ❌ |
| SKILL.md L68（Workflow 第 6 步） | assets/gtm-strategy.md、assets/launch-playbook.md | ❌ |
| SKILL.md L232（Data 表） | data/sources.json | ❌ |

后果：agent 执行 Workflow 时要么反复尝试读取不存在的文件（浪费轮次、产生报错），要么放弃读取直接把"参考 X 文件"当成空操作。无论哪种，第 1、3、6 步的产出物（ICP 草稿、动型细节、GTM 计划、启动手册）都失去了模板依托，交付物质量依赖 agent 临场发挥。这是必须修复的问题，修复优先级最高。

### 9.2 工作流可执行性

剥离缺失文件后，第 2、4、5 步仍可独立执行：定位转介（第 2 步）指向真实技能名、渠道试验（第 4 步）有"quick tests, measure, double down"的可操作循环、度量与 RevOps（第 5 步）有完整清单。Do/Avoid、Launch Types、Growth Loops 均为自包含内容。可以说"核心方法可执行，资产层残缺"。

### 9.3 度量与反馈闭环

技能的测量观（L150-170）本身是闭环的：定义单一漏斗 → 领先指标 → PQL 评分 → 路由 SLA → 周会复盘。SCORING 的 QA-01 与 FMT-01 又把"显式成功指标 + 停止/转向触发"钉在输出要求上。方法论层面可执行性很强；缺口仍是那句"channel playbook best practices"（L61）——渠道试验的停止/转向判据正文没有给出具体示例。

---

## 10. SCORING 交叉参考

将 SCORING.yaml 的 20 个判项逐一与 SKILL.md 对应条款交叉验证：

| 判项 | 正文对应 | 一致性 |
|------|----------|--------|
| SCOPE-01 | L31-44 Quick Start（8 类输入） | ✅ 输入清单逐字对应 |
| SCOPE-02 | L22-27 When NOT to Use（4 个转介） | ✅ 技能名全部对上 |
| SCOPE-03 | L44 缺数推进原则 | ✅ 逐句对应 |
| PROC-01 | L48-50 Workflow 第 1 步 | ✅（但依赖缺失文件 assets/icp-definition.md） |
| PROC-02 | L96-104 Motion Selection Framework | ✅ 分支条件逐字一致（$5K、技术买家、sales-led） |
| PROC-03 | L59-61 Workflow 第 4 步 | ✅ 1-2 渠道 + bullseye 试验 |
| PROC-04 | L139-146 按阶段渠道表 | ✅ 四阶段渠道清单逐字一致 |
| PROC-05 | L63-65 Workflow 第 5 步 | ✅ 生命周期/单一事实源/PQL→SQL+ SLA |
| PROC-06 | L67-69 Workflow 第 6 步 | ✅ 30+30+30 周会逐字一致 |
| PROC-07 | L150-158 领先指标 + PQL 公式 | ✅ 公式系数逐字一致 |
| DEC-01 | L174-181 Launch Types | ✅ 时间线逐字一致 |
| DEC-02 | L117-126 ICP Scoring 权重 | ✅ 权重逐字一致（和为 100%） |
| DEC-03 | L185-194 Growth Loops | ✅ 机制与业务模型配对 |
| DEC-04 | L207-214 Avoid 两条 | ✅ 逐句对应 |
| FMT-01 | L248-254 What Good Looks Like 五条 | ✅ 五要素逐条对应 |
| FMT-02 | L165-170 PQL→SQL 检查清单 5 项 | ✅ 五项逐字对应 |
| NEG-01 | L210 Avoid："Do all channels" in parallel | ✅ |
| NEG-02 | L209、L211 Avoid 两条 | ✅ |
| NEG-03 | L10、L204 AI 只执行不策略 | ✅（正文唯一的 AI 落地表述） |
| QA-01 | L61 试验 + L248-254 停止/转向触发 | ⚠️ 正文有原则无示例，判据可答但证据稀疏 |

另验证：`total_items: 20` 与实际判项数一致；3 个 critical_failures 均对应正文的强制条款；`pattern: process` 与正文工作流形态吻合。

结论：SCORING 与正文的对应度在全部已审技能中属于上乘水平——没有一项判据找不到正文出处，也没有一项正文承诺未进入判据。测评体系与技能本体互相成就。

---

## 11. 已知问题（跳过）

按任务要求，本节不做独立已知问题清单；相关发现已并入第 5、9 节分析及第 13 节修复建议。

---

## 12. 综合评分（8 维 → /100）

| 维度 | 权重 | 得分 | 评述 |
|------|------|------|------|
| 1. Frontmatter 与描述规范 | 15 | 14 | 描述三要素齐全、≤1024，仅"AI GTM automation"承诺未兑现 |
| 2. Body 结构完整性 | 15 | 10 | 工作流出色，但缺独立 Output Format、两张空表、6 处断链 |
| 3. 逻辑一致性 | 15 | 13 | 权重/公式/数字全闭合；AI 主题覆盖偏薄 |
| 4. 规范合规（12 项） | 10 | 8 | 11/12 通过，Output Format 一项部分通过 |
| 5. 语法格式 | 10 | 9 | Markdown/YAML/Python 均有效，小瑕疵仅为格式混用 |
| 6. 人机感 | 10 | 8 | 原则层极佳、操作层欠账（AI 落地、无样例） |
| 7. 可执行性 | 15 | 8 | 核心方法可执行，资产文件整体缺失拉低评分 |
| 8. 测评适配（SCORING/check.py） | 10 | 8 | 判据-正文一致性近乎完美；脚本 0 判项 + latent bug |

加权合计：78 / 100。

等级判断：良好（B+）。技能的知识骨架与测评体系是"可上市"水准，短板集中在资产文件缺失与输出格式缺位——两者都是结构性、可修复的问题，且修复后本技能有望进入 88-92 分区间。

---

## 13. 修复建议

按优先级排序。格式：严重度 ｜ 位置 ｜ 问题 ｜ 建议 ｜ 工作量。

### 🔴 高优先级

1. ｜ `SKILL.md:50,57,68,232` + 目录 ｜ 6 处内部文件引用（assets/icp-definition.md、references/plg-implementation.md、references/sales-motion-design.md、assets/gtm-strategy.md、assets/launch-playbook.md、data/sources.json）指向不存在的文件 ｜ 二选一：方案 A（推荐）补齐全部 6 个文件，ICP 模板、PLG 实施清单、销售动型设计清单、GTM 计划模板、启动手册模板、资源列表各 40-80 行即可；方案 B：删除全部引用并把第 1、3、6 步的产出物要求内联为正文检查清单。 ｜ 大（方案 A）/ 中（方案 B）

2. ｜ `SKILL.md:69` 之后（或 L248 之前）｜ 缺独立 Output Format 节，交付物结构无规格 ｜ 新增"Deliverable Format"节：GTM 计划与启动手册各自的小节结构与字段级要求，直接替代对缺失资产文件的依赖，并与 FMT-01 五要素对应。 ｜ 小

### 🟡 中优先级

3. ｜ `SKILL.md:218-226` ｜ Resources 与 Templates 两表为空 ｜ 填充实际条目，或整节删除；若采用修复 1 的方案 A，则两张表改为指向已创建的资产文件。 ｜ 小

4. ｜ `SKILL.md:73-82` ｜ Decision Tree 是"问题→章节"目录而非决策树 ｜ 改为带条件与结论的分支（如"ACV 区间 × 技术买家 → 动型"）；否则删除本节。 ｜ 小

5. ｜ `SKILL.md:61` ｜ "refer to channel playbook best practices" 指向不存在的 playbook ｜ 改为具体指引：内联 3-5 条渠道试验判据（如"两周内 CPM < X 且 demo 率 > Y 才加倍投入"），或指向修复 1 中新建的文件。 ｜ 极小

6. ｜ `SKILL.md:10` ｜ 硬编码日期 "Jan 2026" ｜ 改为"当前最佳实践"类无日期表述，避免过期误导。 ｜ 极小

7. ｜ `SKILL.md:10,204` + description L3 ｜ "AI-powered GTM automation" 承诺与正文覆盖不匹配 ｜ 在 Measurement 或新 Output Format 节补 2-3 行 AI 执行落地点（如线索打分、渠道报告自动化、A/B 文案生成），或从 description 移除该触发词。 ｜ 小

8. ｜ `SCORING.yaml` QA-01 与 FMT-01 ｜ 停止/转向触发判据存在重叠 ｜ 让 QA-01 聚焦"渠道层成功指标"、FMT-01 聚焦"文档五要素"，在 question 措辞上做区隔。 ｜ 极小

### 🟢 低优先级

9. ｜ `check.py:18-21,46-61` ｜ latent bug：check() 内 `set_agent_output(agent_output)` 会覆盖 main() 已写入的文件内容（当前 0 判项无影响） ｜ 在 check() 内仅设置 tool_log 路径，agent 输出交给 main 统一处理；或在 check() 中先读文件再设置。 ｜ 极小

10. ｜ `check.py:25-42` ｜ 20 项全部为 llm judge，无任何脚本判项 ｜ 可加 1-2 个脚本判项（如检测输出是否含 ICP 关键词、是否出现"all channels"否定模式），降低评测成本、增加判分确定性。 ｜ 中

11. ｜ `SKILL.md:24-27` vs `:236-244` ｜ 跨技能引用格式两种写法并存 ｜ 统一为同一格式（推荐表格化并在两处使用相同冠词风格）。 ｜ 极小

---

## 附录

### 附录 A：审查过程

1. Glob 枚举目录全部文件（3 个文件，0 个子目录）。
2. 三个文件全部全文读取（无跳读、无抽样）。
3. 按任务 13 节框架逐节撰写；第 5 节为逐文件内容分析，第 10 节完成 20 判项 × 正文的逐项交叉验证。

### 附录 B：行数与字数统计

| 文件 | 行数 | 备注 |
|------|------|------|
| SKILL.md | 255 | 正文 ≤600 行合规 |
| SCORING.yaml | 184 | total_items=20，判项数一致 |
| check.py | 66 | 0 脚本判项 |
| description | ~290 字符 | ≤1024 合规 |

### 附录 C：评分与修复的对应关系

若全部 🔴 项（修复 1、2）与 🟡 项（修复 3-7）完成，预估维度得分变化：Body 结构 10→13、规范合规 8→10、可执行性 8→13、人机感 8→9，合计可达 88-90 分区间。修复 9-11 属锦上添花。

### 附录 D：本技能最值得肯定之处

SCORING.yaml 与 SKILL.md 之间的"判据—正文"一一对应关系（20/20 项有据可查）、全部量化权重闭合（ICP 权重和 = 100%、PQL 系数和 = 1.0）、以及 Quick Start 的"最小输入集 + 缺数推进"原则，是三个值得其他技能借鉴的设计。
