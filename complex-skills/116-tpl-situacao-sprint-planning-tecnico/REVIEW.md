# REVIEW — 116-tpl-situacao-sprint-planning-tecnico

> 审查日期: 2026-08-06 | 审查对象: `D:\SkillIF\skill-experiment\complex-skills\116-tpl-situacao-sprint-planning-tecnico\`
> 结论预览: 🟡 **可用但有小问题** — 规则体系与测评设计整体扎实，但存在 1 处规则级逻辑矛盾（路由表 vs 垂直切片）、1 处容量数学矛盾、1 处 description 模板残留与悬空引用，以及缺 Scope 节。修复 4 项 P1/P2 后可升至 🟢。

---

## §1 审查范围与方法

### 1.1 审查对象

| 文件 | 路径 | 作用 |
|------|------|------|
| SKILL.md | `116-tpl-situacao-sprint-planning-tecnico\SKILL.md` | 技能主体（142 行） |
| SCORING.yaml | `116-tpl-situacao-sprint-planning-tecnico\SCORING.yaml` | 测评标准（130 行，14 项 criteria + 2 项 critical_failures） |
| check.py | `116-tpl-situacao-sprint-planning-tecnico\check.py` | 脚本检查实现（77 行，2 项 script judge） |

### 1.2 参考基准

| 基准 | 路径 | 用途 |
|------|------|------|
| SKILL-SPEC.md v1.0 | `complex-skills\_shared\SKILL-SPEC.md` | 规范合规判定的权威标准 |
| checker.py | `complex-skills\_shared\checker.py` | 判定 `judge: script` 的函数库实现 |
| CHECKER-LIBRARY.md | `complex-skills\_shared\CHECKER-LIBRARY.md` | 函数库契约文档 |
| skill-dossier.md | `~\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` | 语料库 322 项既有审查档案（116 属 Batch 101-125） |
| generate_scoring_prompt.md | `D:\SkillIF\skill-experiment\generate_scoring_prompt.md` | SCORING.yaml 生成规范（pattern 与 total_items 约定） |

### 1.3 对照材料

- `complex-skills-no-trigger\116-tpl-situacao-sprint-planning-tecnico\` — 无 trigger 对照集副本（diff 后确认存在分叉，见 §12.4）。
- 同模板家族 058 / 115 — 用于确认 description boilerplate 的同源性。

### 1.4 审查维度与方法

沿用 dossier 的五维框架，并按 SKILL-SPEC §5 合规清单逐项核对：

1. **逻辑一致性** — 规则↔路由表↔模板↔输出↔质量门之间的自洽性，重点查"同一事实的两处表述是否互相矛盾"。
2. **语法与可读性** — 拼写、编号、标点、markdown 渲染完整性。
3. **人机感** — emoji/称呼语/口语化/叫喊式大写；受众是否统一（agent 指令 vs 用户话术）。
4. **规范合规性** — SKILL-SPEC v1.0 §1–§4 全部条款。
5. **测评设计** — SCORING.yaml 与 check.py 是否忠实覆盖技能自身内容、judge 分配是否合理、critical_failure 是否存在误伤风险。

审查方式为全文人工阅读 + 行级引用；无 agent 实测运行（run 阶段数据不属于本次静态审查范围）。

---

## §2 制品清单与基本元数据

### 2.1 文件构成

技能目录仅含 3 个文件，无 `references/`、`scripts/` 子目录，无测试样例目录。作为 standalone 技能自洽，但这也意味着 description 引用的外部文件必然悬空（见 §4.3）。

### 2.2 规模统计

| 文件 | 总行数 | 备注 |
|------|:------:|------|
| SKILL.md | 142 | frontmatter 4 行 + 正文约 138 行 |
| SCORING.yaml | 130 | criteria 14 项 + critical_failures 2 项 |
| check.py | 77 | 可执行主体 2 项检查 |

### 2.3 修改时间线

| 文件 | mtime | 含义 |
|------|-------|------|
| SCORING.yaml | 2026-08-05 14:56 | 早于 SKILL.md 的修复 |
| check.py | 2026-08-05 16:36 | 中间版本 |
| SKILL.md | 2026-08-05 20:07 | 最后修改（编号修复发生于此时段） |

对照 dossier 的 status 行 `fixed — tpl28/28`（2026-08-05）：编号修复确已落入 trigger 集，但 **未同步到 no-trigger 对照集**（见 §12.4，实验混杂风险）。

### 2.4 frontmatter 事实

| 字段 | 值 | 判定 |
|------|-----|------|
| name | `tpl-situacao-sprint-planning-tecnico` | 小写+连字符，≤64 字符 |
| description | 337 字符（≤1024） | 长度合规，内容有缺陷（见 §4） |

仅含 name/description 两个字段，无任何被 §1.3 禁止的键（无 metadata/version/tags 等）✅。

---

## §3 Frontmatter 审查（SKILL-SPEC §1）

### 3.1 name 字段（§1.1 + §4）

- `tpl-situacao-sprint-planning-tecnico`：小写、连字符分隔、长度合规。
- 与目录名 `116-tpl-situacao-sprint-planning-tecnico` 的差异仅为语料库全局约定 `NNN-` 前缀。§4 字面要求 name 与目录名一致，但全库 322 项均采用"目录带序号、name 不带"的惯例，属于语料库级约定而非本技能缺陷，不计违规，仅记录。
- 建议统一在 SKILL-SPEC 中明示该约定（§4 措辞与语料库实践不一致，是全库共性的解释成本）。

### 3.2 禁止字段（§1.3）

frontmatter 仅含 name + description，通过。无 `allowed-tools`/`argument-hint` 等可选字段，可选字段缺省是允许的。

### 3.3 元数据处理（§1.3 末段）

无需迁移的版本/作者信息，无 `## Metadata` 尾节要求，合规。

**§3 小结**: frontmatter 结构合规 ✅，唯一可议点是 §4 名称约定与语料库实践的差异（全库共性，非本技能问题）。

---

## §4 Description 审查（SKILL-SPEC §2）

### 4.1 结构（§2.1/§2.2）

```
Pack template (situacao/12-sprint-planning-tecnico.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is breaking down features into tasks for sprint planning, refining a backlog, estimating effort, or facilitating technical planning sessions.
```

- **WHAT** — "Pack template... Guides the agent on situational tasks..."：三分句中有 WHAT，但内容与主题错位（见 4.3）。
- **WHEN** — "Use when the user is breaking down features into tasks for sprint planning, refining a backlog, estimating effort, or facilitating technical planning sessions"：**这是全技能最可靠的部分**。四个触发场景与 SCOPE-01 的四个锚点（sprint planning / backlog refinement / story breaking / effort estimation）一一对应，说明 SCORING 与 description 的触发面是咬合的。
- **KEYWORDS** — 隐含于场景短语中（sprint planning、backlog、estimation）；缺少 "story points"、"capacity"、"tech debt" 等高频领域词，属于可优化而非违规（§2.1 为 must answer，关键词可由场景短语承担）。

### 4.2 语气与人称（§2.3/§2.4）

- 第三人称 ✅（"Guides the agent..."）。
- 无祈使开头、无第一/第二人称 ✅。
- 触发信号短语 "Use when the user..." 命中 §2.4 列表第一项 ✅。
- 337 字符 ≤ 1024 ✅；≥40 字符 ✅。
- 无跨技能路由（§2.5）✅。

### 4.3 内容准确性与悬空引用（本技能 description 的主要缺陷）

| # | 问题 | 证据 | 严重度 |
|---|------|------|:------:|
| D1 | **模板残留文案**："Guides the agent on situational tasks such as debugging, security and refactoring" 与本技能主题（sprint planning）完全无关。该句是 tpl-situacao 家族的共享 boilerplate（058 数据管道、115 AB 测试均逐字相同），对 116 而言是复制粘贴残留。后果：**触发匹配可能把调试/安全/重构类请求引入此技能**，同时污染测评的 invoke 语义。 | SKILL.md 第 3 行；对照 058/115 第 3 行 | P1 |
| D2 | **悬空路径引用**："Pack template (situacao/12-sprint-planning-tecnico.md)" 指向一个在本技能目录、在语料库任何位置都不存在的文件（目录仅 3 文件）。违反 §3.3"文件引用必须为技能目录内相对路径"；且该文件本就属于 pack 外部体系，此处无法自洽。 | 目录 `ls`；SKILL.md 第 3 行 | P2 |
| D3 | **含糊填充语**："aligned with this context" 无指代对象，是模板缝合痕迹。 | SKILL.md 第 3 行 | P4 |

**§4 小结**: 触发信号与 WHEN 部分合格（且与测评范围咬合），但 D1（P1）是 description 层最值得修的硬伤——它直接影响触发正确性与测评外效度。

---

## §5 正文结构与规范合规（SKILL-SPEC §3）

### 5.1 三必需节（§3.1）

| 必需节 | 本技能对应 | 判定 |
|--------|-----------|:----:|
| Workflow / Process | 编号原则 1–7 + ROUTING TABLE（§3.1 允许任意标题名） | ✅ 存在 |
| Output Format | `## OUTPUT FORMAT`（Sprint Plan 模板） | ✅ 显式 |
| Scope / Limitations | 无；仅 `## DO NOT`（7 条禁令） | ❌ **缺失** |

**DO NOT ≠ Scope**：§3.1 定义 Scope 为"本技能不做什幺、何时不应使用"，DO NOT 是"agent 在任务中不得做什么"——两者语义不同。本技能 DO NOT 只有一条接近 Scope（"DO NOT use sprint planning to make architectural decisions — that's a separate RFC/ADR session"），其余均为流程禁令。缺失内容示例：本技能不覆盖 sprint 执行/站会/回顾、release planning、跨团队组合规划、以小时为单位的估算承诺、架构决策（RFC/ADR）。

这是全库最高频规范缺口（dossier 统计 ~68% 技能缺 Scope），但缺就是缺，不因普遍而免除。

### 5.2 规模（§3.2）

- 正文约 138 行，远低于 process 目标 ~200 行、硬上限 600 行 ✅。
- `pattern: situational` 不在 SKILL-SPEC §3.2 的五种 pattern 表内，属 tpl-situacao 家族自扩展类型。建议在 SKILL-SPEC 中登记该 pattern 及其目标行数，否则生成器（generate_scoring_prompt.md）无法为它给出 total_items 基准（见 §10.6）。

### 5.3 文件引用（§3.3）

- 正文内无 `references/`、`scripts/` 引用（本技能无附属文件）。
- 唯一文件引用出现在 description 的 `situacao/12-sprint-planning-tecnico.md`（悬空，见 D2）。无跨技能 `../` 路径 ✅。

### 5.4 内容指南（§3.4）

- **知识增量** ✅：不解释"什么是用户故事"，直接给垂直切片判定；"works correctly is not an AC" 是典型的反模式教学。
- **反模式优先** ✅：DO NOT 清单、路由表红线、债务分类表均为具体禁令。
- **决策树优于散文** ✅：ROUTING TABLE 是 10 行 If-Then 决策表，是模板家族的最佳实践。
- **具体优于抽象** ✅：容量示例、500ms 性能 AC、8 点拆分阈值、20% 债务预算均为具体数值。

**§5 小结**: 结构与内容指南达标，唯一硬缺口是 Scope/Limitations 节（P2，全库共性，但对模板类技能——其职责边界恰恰是最该写清楚的东西——此缺口影响更大）。

---

## §6 逻辑一致性：编号规则体系（规则 1–7）

### 6.1 编号完整性（修复确认）

规则列表现为 "1."–"7." 连续编号、格式统一（`N. **Title.** body`）。dossier 记录的"规则列表从 2. 开始缺 1."缺陷已在 2026-08-05 修复 ✅（no-trigger 副本未同步，见 §12.4）。

### 6.2 规则间自洽性

| 规则 | 内容 | 交叉检查 |
|------|------|---------|
| 1 | 垂直切片，禁止水平层 | 与规则 2 互补；**与路由表第 5 行矛盾**（§7.1，P1） |
| 2 | 触及 >3 层拆分 | 与规则 1 同向 ✅ |
| 3 | 债务 20% 预算、不无限推迟、不吞全 sprint | 与 OUT-01 的 Tech Debt Budget 节、PROC-04 一致 ✅ |
| 4 | AC 必须可测试、可证伪 | 与 PROC-01、Story Template 的 Given/When/Then 一致 ✅ |
| 5 | 按复杂度估算，禁止"3 点=3 小时" | 与 PROC-02 一致 ✅；**与 OUTPUT FORMAT 容量示例矛盾**（§8.2，P1） |
| 6 | 依赖即风险，先解决或标阻塞 | 与 PROC-03、OUT-02 一致 ✅ |
| 7 | 容量 = 理论的 60-70%（会议/评审/事故/假期/入职） | 与 PROC-05 锚点一致 ✅；**与 OUTPUT FORMAT 示例矛盾**（§8.1，P1） |

### 6.3 规则级发现的预登记

- 规则 1 vs 路由表（DB+UI+API 行）——矛盾，详见 §7.1。
- 规则 5/7 vs 输出示例——矛盾，详见 §8。
- 规则 3 vs 债务分类表"Security debt: Critical — fix immediately"——张力（次要）：critical 安全债"立即修"与"20% 预算、不吞掉整个 sprint"需要明确的优先级冲突裁定，当前缺失。建议补一句："critical 安全债按事件处理，与 20% 预算分离，但仍需显式协商"（P3）。

---

## §7 逻辑一致性：路由表与模板组件

### 7.1 🔴 核心矛盾：路由表第 5 行 vs 规则 1（P1，本审查最重要发现）

**路由表第 5 行（SKILL.md 第 31 行）**：

> "Story touching database AND UI AND external API → Likely 3 stories. Split: (1) data model, (2) API endpoint, (3) UI integration."

**规则 1（第 8 行）**：

> "A vertical slice delivers end-to-end functionality (UI + API + DB)... A horizontal layer (e.g., **'build the entire data model'**) is not a user story."

两处表述直接对撞：

1. 规则 1 举的反例是**字面意义上的** "build the entire data model"，而路由表的拆分建议 #1 就是 "(1) data model"——路由表推荐了规则 1 明确禁止的东西。
2. 按层拆分（数据模型 / API / UI 三层）正是"horizontal layers"的定义，SCOPE-02 的判定锚点恰好是"vertical slices (end-to-end UI+API+DB)，而非 horizontal layers"。
3. **对测评的直接影响**：一个逐字遵循路由表的 agent，产出按层拆分的 3 个故事，会被 LLM judge 依据 SCOPE-02 判负；而技能自身的内容却"支持"它这么做。技能内容与测评标准之间的自相矛盾，使同一行为既被技能鼓励又被测评惩罚。

**修复建议**：把该行改为垂直切片语义下的拆分，例如：
> "Story touching database AND UI AND external API → Likely 3 stories. Split into 3 vertical slices, each delivering end-to-end value: (1) user can view records end-to-end, (2) user can create a record end-to-end, (3) user can manage records end-to-end."

同时删除或改写 "(1) data model" 字样，与规则 1 的反例彻底隔离。

### 7.2 路由表其余行

| 行 | 判定 | 备注 |
|----|:----:|------|
| >8 点拆分 | ✅ | 与 QUALITY GATES、SCOPE-03 一致 |
| 无 AC 故事 | ✅ | 与 NEG-01、CF-01 一致 |
| "顺带加 X" → 新 ticket | ✅ | 与 NEG-02 一致 |
| 被其他团队阻塞 → 标记/回 backlog | ✅ | 与 PROC-03、OUT-02 一致 |
| 小时/天估算请求 → 转区间 | ✅ | 与规则 5 同向 |
| 设计未就绪 → 阻塞 + DoR 前置 | ✅ | 与"Definition-of-Ready"语义一致 |
| 重复重估 3+ 次 → spike，封顶 1-2 天 | ✅ | 但见 §7.4 spike 估算缺口 |
| "边做边想" → 红旗 + spike | ✅ | 与 CF-01 语义一致，但见 §7.4 |

### 7.3 Story Template / 量表 / 债务分类

- **Story Template**：As/I want/So that + Given/When/Then AC + 错误分支 + 性能 AC + 技术备注 + DoD（合并、≥80% 覆盖率、部署 staging、PO/QA 验证）——结构完整，与规则 4、PROC-01 咬合 ✅。
- **Story Point Reference Scale**（1/2/3/5/8/13+）：Fibonacci 量表 ✅；但 **"13+ | Too large — must be split" 行与 ">8 必须拆分" 规则不可达**（P2，§13 I-07）：按路由表与 QUALITY GATES，估算到 9 点就该拆，13+ 永远不该被估出来。该行是量表先于拆分规则独立写作的痕迹。建议改为 "9-13（区间内一律拆分）" 或将 13+ 行删除。
- **Technical Debt Categories**：6 类债务（安全/可靠性/测试/性能/可维护性/文档）分级合理 ✅；"Security debt — Critical — fix immediately" 与规则 3 的张力见 §6.3。

### 7.4 Spike 的估算缺口（P2，影响测评有效性）

路由表两处把故事路由到 spike（重估 3+ 次、无 scope 故事），并规定 spike 封顶 1-2 天（时间盒）。但：

1. Story Template 的 Type 含 Spike，Estimate 字段却要求 `[story points]`——没有说明 spike 按点数还是按时间盒估算；
2. CF-01 判定"故事无 AC 或无估算 → cap_to_0"。**spike 天然无 AC**（它就是用来消解不确定性的研究任务），且按路由表应封顶 1-2 天而非点数。一个完全合规地写了 spike 的 agent 可能同时触发 CF-01 的两个触发条件之一，被不公正地归零。
3. 输出模板也没有 spike 的专属呈现位（例如 Spike Backlog / Research 区）。

建议：在 Story Template 中给 Spike 单独说明（"Spike 以 1-2 天时间盒估算，无 AC；列入 Backlog 或独立 Research 节，不计入 sprint 故事点数"），并在 CF-01 中豁免带 `Spike` 标记的故事。

**§7 小结**: 路由表 10 行中 9 行与规则体系自洽；1 行（DB+UI+API）与规则 1 正面冲突，是本技能最值得立即修复的逻辑缺陷。Spike 估算缺口则是测评设计层面的次要点。

---

## §8 逻辑一致性：输出模板与容量数学

### 8.1 🔴 容量数学矛盾（P1）：40 点 vs 60-70% vs 20% overhead

**OUTPUT FORMAT 示例（第 108-112 行）**：

```
- Team: 4 developers
- Working days: 10
- Estimated capacity: 40 points (accounting for 20% overhead)
- Reserved for tech debt: 8 points
```

**规则 7（第 20 行）**：真实容量 = 理论容量的 60-70%。

矛盾链：

| 算式 | 结果 | 对照 |
|------|------|------|
| 4 devs × 10 days = 40 单位 | 40 = 理论 100% | 示例却称"已计入 20% overhead" |
| 理论 40 × 80%（20% overhead） | 应为 32 | 示例写 40 |
| 理论 40 × 60-70%（规则 7 / PROC-05 锚点） | 应为 24-28 | 示例写 40 |

即：示例声称"40 点已含 20% overhead"，但 40 恰好是 4×10 的满额理论值——overhead 只存在于措辞里，不在数字里。若以规则 7 为准，示例容量应为 24-28 点，Tech Debt 预留应为 5-6 点（20%）。

**对测评的直接影响**：PROC-05 的 LLM judge 问题锚定"60-70% of theoretical"。一个逐字复刻输出模板的 agent（40 点 / 20% overhead）会被 PROC-05 判负——**技能示例与测评标准在同一指标上互相矛盾**，与 §7.1 同类。

### 8.2 🔴 点数-天数锚定（P1）：4×10=40 违反规则 5

40 点的来源只能是 4 devs × 10 days × 1 point/day——这正是规则 5 禁止的"3 点=3 小时"式锚定（story points 衡量相对复杂度，不是理想时间）。容量一节偏偏用"人×天=点"推导，等于技能自己演示了自己禁止的错误。若容量必须给点数，应写"参考上季度 velocity 为 X 点/人/迭代"，把点数与天数彻底解耦。

### 8.3 输出模板其余部分

- **Stories 表**（#/Story/Points/Owner/Dependencies）：字段齐备，与 OUT-01 的 `### Stories` 正则、PROC-03 依赖列一致 ✅。
- **Risks & Blockers**：与 OUT-02 正则、QUALITY GATES 第 8 条（阻塞故事须有阻塞条件与解决 owner）一致 ✅。
- **Sprint Goal**：一句业务结果而非任务清单，与 OUT-03 一致 ✅。
- **Tech Debt Budget 表**（Item/Points/Impact）：与规则 3、PROC-04 一致 ✅；示例（Refactor AuthMiddleware → 5 点，Unblocks 3 future stories）恰好演示了路由表"可量化影响"的要求 ✅。

**§8 小结**: 输出模板的结构骨架是全家族最完整的之一，但容量示例在"规则 7 的 60-70%"与"规则 5 的禁止时间锚定"两条规则上同时破例，且会连带导致 PROC-05 误判——必须修正示例数字与推导方式。

---

## §9 人机感与语言质量

### 9.1 语气与受众

- 整体为**祈使式、专业性、零 emoji、零填充语**。规则 1-7 与 DO NOT 清单是干净利落的 agent 指令，无 "Let's"、无口号、无叫喊式大写（唯一大写是标题与 DO NOT 强调，属功能性）。
- dossier 记录的"混合语气（规则部分对用户、部分对 agent）"在修复后已明显收敛：多数规则仍可读为对 agent 的指令（agent 扮演规划主持人）。残留的轻微双重受众：规则 3 "Negotiate explicitly"、路由表 "Never commit to hours publicly"、DO NOT "investigate why" 更像写给团队的流程建议，但均可被 agent 翻译为行动，不构成阻塞（P4）。
- QUALITY GATES 第 7 条"All team members voiced concerns or questions before plan is finalized"是本技能唯一的多人协作假定，在单 agent 测评环境下需要 LLM judge 的判读约定（见 §10.5，I-11）。

### 9.2 语言细节

| 项 | 判定 |
|----|------|
| 拼写/错别字 | 无 |
| 标点 | em-dash（—）全篇一致，无内部规则矛盾（对比 015 的 em-dash 自反矛盾） |
| 大小写 | "AC"、"DoR"、"PO/QA" 等缩写使用一致 |
| 中英混杂 | 无（纯英文技能） |
| 数字一致性 | 20% 债务、8 点上限、2 条 AC、500ms、80% 覆盖率在各节间一致（除 §8 容量示例） |

### 9.3 可读性结构

表格密度高（路由表/量表/债务分类/输出模板/质量门），扫描成本低，符合 §3.4 决策表优先。唯一排版瑕疵：规则 1 内的嵌套引号 `(e.g., "build the entire data model")` 在 markdown 渲染中正常，但若未来迁移到代码式渲染需转义——属提示级。

**§9 小结**: 人机感合格，无 emoji 滥用、无促销、无机械感；残余问题是轻度的受众混用（P4）与单 agent 评估下的多人协作假定（I-11，测评约定问题）。

---

## §10 SCORING.yaml 测评设计审查

### 10.1 结构核对

- `total_items: 14` = 3(scope) + 5(process) + 3(output) + 2(negative) + 1(qa) ✅ 与实际 criteria 数量一致。
- 分类均在 generate_scoring_prompt.md 允许的类别列表内（scope/process/output/negative/qa）✅。
- 每项二进制（0/1）✅；judge 仅 llm/script 二值 ✅；critical_failures 2 项 ≤ 上限 4 ✅。
- `pattern: situational` 不在生成规范的五 pattern 表内（§10.6）。

### 10.2 内容覆盖映射（技能内容 → 评分项）

| 技能内容 | 评分项 | 覆盖 |
|----------|--------|:----:|
| 规则 1 垂直切片 | SCOPE-02 | ✅ |
| 规则 3 债务 20% | PROC-04 | ✅ |
| 规则 4 可测试 AC | PROC-01 | ✅ |
| 规则 5 复杂度点数 | PROC-02 | ✅ |
| 规则 6 依赖声明 | PROC-03 | ✅ |
| 规则 7 容量 60-70% | PROC-05 | ✅ |
| 路由表 >8 拆分 | SCOPE-03 | ✅（条件性，见 10.3） |
| 路由表无 AC 故事 | NEG-01 + CF-01 | ✅ |
| 路由表顺带加 X | NEG-02 | ✅ |
| 输出模板四段 | OUT-01/02/03 | ✅ |
| 质量门第 7 条 | QA-01 | ✅ |
| DO NOT（7 条） | CF-01/CF-02 | ⚠️ 仅 2/7 直接映射 |
| 规则 2（>3 层拆分） | 无直接项 | 空 |
| 路由表 小时→区间 / 设计未就绪 / spike | 无直接项 | 空 |
| QUALITY GATES 第 8 条（阻塞故事须有 owner） | OUT-02 部分 | ⚠️ 仅模式匹配 |

DO NOT 未覆盖 4 条：carry-over >20%、禁止 Chores 兜底故事、禁止按资历指派、加故事须等额移除——属抽样取舍，可接受，但建议至少将"Chores 兜底故事"与"加故事不等额移除"纳入（P3，I-12）。

### 10.3 SCOPE-03 的条件性空真值问题（P3，I-10）

问题为 "Were any stories over 8 points split into smaller vertical slices?"——当任务中的故事全部 ≤8 点时，该问题无真值。LLM judge 需要明确约定（常见约定：条件未发生时视为通过，即 vacuous pass），否则 judge 之间会出现 yes/no 分歧，直接产生测量噪声。建议在 question 中加前提："If any story was estimated over 8 points, was it split? (If no story exceeded 8 points, answer yes.)"

### 10.4 critical_failures 设计

- **CF-01**（无 AC 或无估算 → cap_to_0）：与 DO NOT 第 1 条及规则 4/5 同源 ✅，但存在 **spike 误伤风险**（§7.4，P2）——需要"Spike 故事豁免"或"仅针对进入 sprint 的故事"的限定。另建议限定作用域为"进入 sprint 的故事"：输出模板中可能存在被移回 backlog 的故事（路由表明确支持"move to backlog"），backlog 故事无 AC 不应触发归零。
- **CF-02**（100% 容量无 overhead 无债务预算 → cap_to_0）：语义正确，但注意 §8.1 的示例本身写着 "40 points (accounting for 20% overhead)"——若 agent 复刻示例措辞而数字被 LLM judge 判定为 100%，CF-02 与 PROC-05 会双重误伤。修示例即可解除。

### 10.5 12 项 LLM judge 的问题质量

- 问题均为二值、带具体锚点（"not 'works correctly'"、"60-70%"、"Given/When/Then"），质量高 ✅。
- **QA-01**（全体成员发表意见）在单 agent 评估下的语义未定义（I-11）：agent 应否模拟征询？模拟几名成员算合规？建议改写问题为"Did the agent explicitly solicit and record concerns/questions from the team members named in the task before finalizing the plan?"并约定"任务未提供成员名单时，agent 应主动列出角色并征询或说明未征询的原因"。
- **PROC-05** 的 60-70% 锚点与技能自身示例（20% overhead）矛盾（§8.1）——先修技能，问题本身可保留。

### 10.6 pattern 与 total_items 基准（P4）

generate_scoring_prompt.md 按 pattern 给定 total_items 目标（process ~18、tool ~22 等），但本技能声明 `pattern: situational`，不在表内。14 项对"规则+路由+输出"型模板略偏少（路由表 10 行仅覆盖 5 行、DO NOT 7 条仅覆盖 2 条），属于轻覆盖设计——若测评目标是全规则遵从度，建议将 total_items 提到 16-18（补 DO NOT 映射项）；若目标是抽查代表性行为，14 项可接受。无论取哪边，都应在 SKILL-SPEC/生成规范中登记 situational 类型，避免生成器无法给出基准。

**§10 小结**: SCORING.yaml 结构规范、映射基本忠实、问题措辞高质量；主要风险集中在 4 点：SCOPE-03 空真值、CF-01 spike 误伤、PROC-05 与技能示例矛盾、QA-01 单 agent 判读约定。

---

## §11 check.py 实现审查

### 11.1 与 SCORING.yaml 的一致性

- SCORING 中 `judge: script` 仅 2 项（OUT-01、OUT-02），check.py 恰实现这 2 项，其余 12 项以注释显式标出 `llm judge (not checked here)` ✅——实现与声明完全对齐。
- `sys.path.insert(0, "..\_shared")` 相对解析正确，`_shared/checker.py` 存在，import 成立 ✅。

### 11.2 正则健壮性

| 检查 | 模式 | 分析 |
|------|------|------|
| OUT-01 | `### Capacity\|Tech Debt Budget\|### Stories` | 三分支与输出模板标题一致；`### Stories` 以子串方式命中 `### Stories (by priority)` ✅。假阳性风险低。 |
| OUT-02 | `Risks & Blockers\|### Risks\|blocked` | ① **大小写敏感**：`blocked` 不匹配 `Blockers`/`Blocked`——一个把节命名为 `### Blocked Stories` 的 agent 只能靠第一个分支过关；若同时改了标题措辞（如 `### Open Risks`）则直接误判负（P3，I-09a）。② **假阳性**：`blocked` 是子串匹配，`unblocked`（意为"已解决"！）也命中——语义恰好相反（P3，I-09b）。建议改为 `\bblocked\b` 并在 SCORING 描述中提示大小写。 |

### 11.3 健壮性细节

- `_is_path` 守卫（第 22-28 行）：防止 main() 已读文件后再次按路径处理；逻辑正确但存在**静默失败模式**——若传入的 agent_output 是拼错的路径（不存在），`_is_path=False`，check.py 会把"路径字符串"当作文本搜索，`output_contains` 返回 False，无任何告警（P3，I-13）。建议：路径不存在时输出明确的错误 JSON 或降级为警告。
- main() 只输出 script 项 JSON，LLM 项由 runner 合并——与文档注释一致，接口契约成立 ✅。
- 无 workspace 依赖（本技能所有检查均基于输出文本），check.py 不读取工作区文件——对该模板合理，但也意味着故事表的列完整性（Points/Owner 是否每行都有）完全依赖 LLM judge 目检（补充见 I-12）。

**§11 小结**: check.py 实现精简、与 SCORING 对齐、无死代码；主要问题集中在 OUT-02 正则的大小写与子串语义（P3）以及静默失败路径（P3）。相比同家族 115（6 项 script 检查），116 的脚本可验证面偏小，抽查性与 LLM judge 方差更高。

---

## §12 语料库基准对比与总体评级

### 12.1 dossier 既有记录（Batch 101-125，115-116 系列）

> 116 故事拆分与估算连贯；同样编号故障——规则列表从 "2." 开始缺 "1."；混合语气；Frontmatter 合规；workflow/output/DO-NOT 存在。总评 🟡。

本审查核对：**编号故障已在 trigger 集修复**（§6.1），dossier 的该项记录对当前 trigger 集已过期；其余判定（🟡、workflow/output 存在、语气混合偏轻）与本次审查一致。建议在 dossier 中更新 116 的状态并注明 no-trigger 副本未同步（§12.4）。

### 12.2 与 tpl-situacao 家族同源缺陷

| 缺陷 | 058 | 115 | 116 | 说明 |
|------|:---:|:---:|:---:|------|
| description boilerplate（debugging/security/refactoring） | 有 | 有 | **有** | 同源模板残留，三技能逐字相同 |
| 编号断裂（规则缺 "1."） | 有 | 有 | 已修（trigger 集） | 家族性缺陷，家族级修复应一并核对 no-trigger 集 |
| 缺独立 Scope 节 | 有 | 有 | 有 | 家族共性 |
| 路由表驱动结构 | 有 | 有 | 有 | 家族优点，116 的表是最完整的之一 |

### 12.3 规格合规清单（SKILL-SPEC §5 逐项）

```
[x] name: lowercase + hyphens, ≤64 chars, matches directory（NNN- 前缀为语料库约定）
[x] description: third-person, WHAT+WHEN+KEYWORDS, ≤1024 chars
[x] description: no imperative/first-person/second-person openings
[x] description: no cross-skill routing embedded
[x] description: at least one trigger signal phrase ("Use when the user...")
[x] frontmatter: no keys outside the allowed list
[x] body: ≤600 lines（138）
[x] body: has workflow/process section（规则 1-7 + ROUTING TABLE）
[x] body: has output format section（## OUTPUT FORMAT）
[ ] body: has scope/limitations section（缺失，仅 DO NOT）
[x] body: no cross-skill file references（description 内悬空路径为 pack 外引用，见 §4.3 D2）
[x] directory: NNN-kebab-case, no spaces or uppercase
```

合规达成 11/12；唯一硬缺口为 Scope 节。

### 12.4 ⚠️ no-trigger 对照集分叉（实验混杂风险，P2，I-14）

对 `complex-skills-no-trigger\116-...` 执行 diff：

| 文件 | 差异 |
|------|------|
| SKILL.md | description 删除了 trigger 句（符合对照集设计目的）；**但编号断裂未修复**（"Vertical slices, not horizontal layers.**" 缺 "1." 前缀） |
| check.py | 为旧版（缺 `_is_path` 守卫），与 trigger 集实现不同 |
| SCORING.yaml | 完全一致 |

含义：若 2 Mode × 5 Harness 实验（memory: skillif-research-design）在 trigger 与 no-trigger 两集之间比较遵从度，**任何编号/格式差异都会成为混杂变量**——trigger 集"更干净"可能被错误归因于 trigger 的存在。建议将修复同步到 no-trigger 集（或反之，把对照集重新快照），并核对全家族 28 个 tpl 是否同样分叉。

### 12.5 总体评级

| 维度 | 评级 | 关键依据 |
|------|:----:|---------|
| 逻辑一致性 | 🟡 | 路由表 vs 规则 1 矛盾（P1）、容量示例数学矛盾（P1）、13+ 行不可达、spike 估算缺口 |
| 语法与可读性 | 🟢 | 编号已修复，无错字，表格密度高 |
| 人机感 | 🟢 | 零 emoji、专业祈使语气；轻度受众混用（P4） |
| 规范合规性 | 🟡 | 11/12 通过；缺 Scope 节 + description 悬空引用 |
| 测评设计 | 🟡 | 覆盖忠实、judge 分配合理；SCOPE-03 空真值、CF-01 spike 误伤、OUT-02 正则 |
| **总评** | **🟡** | **修复 4 项 P1/P2 后可升 🟢（见 §13 前 4 条）** |

---

## §13 问题清单与修复建议（按严重度排序的注册表）

> 严重度定义：**P1** = 影响测评有效性或规范硬伤（需修复后才能可靠投入实验）；**P2** = 明显缺陷，修复后达标；**P3** = 边界情况/健壮性问题；**P4** = 提示级打磨。每条给出位置、证据、影响、修复与验证方式。

### I-01 【P1】路由表第 5 行推荐按层拆分，与规则 1 垂直切片直接矛盾

- **位置**: SKILL.md 第 31 行（ROUTING TABLE "Story touching database AND UI AND external API" 行）。
- **证据**: 该行建议 "Split: (1) data model, (2) API endpoint, (3) UI integration"；规则 1（第 8 行）明确 "A horizontal layer (e.g., 'build the entire data model') is not a user story"。
- **影响**: ① 技能内容自相矛盾，agent 遵循任意一侧都会背离另一侧；② SCOPE-02 将按层拆分的行为判负，使"照做技能的 agent"被测评惩罚——技能与测评在同一行为上对立；③ 该行是路由表中唯一给出具体拆分方案的示例，被复制进输出的概率最高。
- **修复**: 改写为三个端到端垂直切片示例（如 "Split into 3 vertical slices: (1) user can view records end-to-end, (2) user can create a record end-to-end, (3) user can manage records end-to-end"），删除 "data model" 字样，与规则 1 反例彻底隔离。
- **验证**: 重新通读规则 1↔路由表↔SCOPE-02 三者，确认对"含 DB+UI+API 的故事"只有一种可执行解释；抽查 agent 输出 3 份，确认拆分均为垂直切片。

### I-02 【P1】容量示例数学矛盾：40 点 ≠ 60-70% ≠ 20% overhead

- **位置**: SKILL.md 第 108-112 行（OUTPUT FORMAT Capacity 示例）。
- **证据**: "Team: 4 developers / Working days: 10 / Estimated capacity: 40 points (accounting for 20% overhead)"。4×10=40 恰为理论满额；按"已含 20% overhead"应为 32；按规则 7（60-70%）应为 24-28；且 40 的推导只能来自"人×天=点"，违反规则 5。
- **影响**: ① 输出示例与规则 5、规则 7 同时冲突；② PROC-05（60-70% 锚点）会误判逐字复刻示例的 agent；③ CF-02（100% 容量）的判定边界被示例措辞搅浑。
- **修复**: 示例改为两条线：先给理论（40 点 = 4 devs × 10 days × 1 point/day 的**velocity 参照**，并注明"点数来自历史 velocity 而非天数"），再给实际（按 60-70% 计 24-28 点，tech debt 预留 5 点）；或直接移除点数-天数换算，改为 "Reference velocity: 10 points/developer/sprint（来自上一迭代）→ planned capacity ≈ 26 points after overhead"。
- **验证**: 用示例数字代入规则 7 与 PROC-05 的判定问题，确认两种解读得出同一结论。

### I-03 【P1】description 模板残留："debugging, security and refactoring" 失配 + 悬空路径

- **位置**: SKILL.md 第 3 行。
- **证据**: "Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context"——与 058/115 逐字相同，与 sprint planning 主题无关；"situacao/12-sprint-planning-tecnico.md" 在本技能目录及语料库中不存在；"aligned with this context" 无指代。
- **影响**: ① 触发匹配会把调试/安全/重构类请求引入此技能，污染 invoke 语义与测评外效度；② 悬空路径违反 §3.3；③ 对照集 description（删除 trigger 句后）同样携带失配文案，问题会同步进入 no-trigger 实验。
- **修复**: 重写为 domain-specific：`Break down features into vertical slices, build a sprint plan with capacity, acceptance criteria, story-point estimates, dependency and risk declarations, and a 20% tech-debt budget. Use when the user is breaking down features into tasks for sprint planning, refining a backlog, estimating effort, or facilitating technical planning sessions.` 删除 pack 路径与 boilerplate。
- **验证**: 对 trigger 句做匹配测试（sprint planning / backlog refinement / story breaking / effort estimation 四场景应命中；debugging/security/refactoring 三场景应不命中）。

### I-04 【P2】缺显式 Scope/Limitations 节（§3.1 硬性要求）

- **位置**: SKILL.md 全文（§5.1 分析）。
- **证据**: 仅有 `## DO NOT`（7 条流程禁令），无"本技能不做什么/何时不用"节；§5.1 已列缺失内容示例。
- **影响**: 合规清单 11/12；模板类技能的边界恰恰是最应写清的（它会被 pack 路由到多情境）；DO NOT 与 Scope 的混同是全库 68% 的共性误读，本技能应示范纠正。
- **修复**: 新增 `## Scope / Limitations` 节，明确：不覆盖 sprint 执行/站会/回顾；不替代 RFC/ADR 架构决策会；不做跨团队组合规划与 release planning；不给小时级估算承诺；估算与需求澄清应分离（呼应 DO NOT 第 5 条）。
- **验证**: 对照 SKILL-SPEC §3.1 三节逐项打勾；确认 DO NOT 条目与 Scope 条目无重叠表述。

### I-05 【P2】DO-NOT 第 5 条与技能自身单会话工作流存在张力

- **位置**: SKILL.md 第 97 行（"DO NOT estimate in the same session as requirements clarification"）。
- **证据**: SCOPE-01 的触发面同时含 backlog refinement 与 effort estimation；Story Template + OUTPUT FORMAT 在同一个输出内包含 AC 写作与估算——技能设计为单会话完成 refine+estimate，而 DO NOT 第 5 条假定两会制。
- **影响**: 逐字执行技能的 agent 在单会话内既澄清需求又估算，将违反自身 DO NOT（自我矛盾）；LLM judge 若把 DO NOT 当 Scope 读，也会对合理输出判负。
- **修复**: 改为带条件的表述：`DO NOT interleave open-ended requirements clarification with estimation in the same meeting — close out requirements (AC defined) first, then estimate.` 把"两会"语义弱化为"两阶段"语义，与技能流程一致。
- **验证**: 模拟一个"先定 AC 再估点"的单会话输出，确认不再触发该禁令。

### I-06 【P2】CF-01 对合法 spike 故事存在归零误伤

- **位置**: SCORING.yaml 第 123-126 行（CF-01）；关联 SKILL.md 第 34/35 行（spike 路由）、第 42 行（Type 含 Spike）。
- **证据**: spike 天然无 AC、按路由表以 1-2 天时间盒封顶（非点数）；CF-01 触发条件为"no acceptance criteria or no estimates"，未豁免 spike。
- **影响**: 完全合规的 spike 写作会被 cap_to_0，把"测评惩罚技能鼓励的行为"扩展到了负面维度。
- **修复**: CF-01 加限定与豁免：`Sprint plan includes stories with no acceptance criteria or no estimates, unless the story is explicitly marked as a Spike (time-boxed research task) or moved to the backlog.` 同时在 Story Template 中补 spike 估算说明（"Spike 按 1-2 天时间盒，无 AC"）。
- **验证**: 构造 3 个判例（含 spike 的计划 / 含 backlog 无 AC 故事的计划 / 含无 AC 进 sprint 故事的计划），确认前两者不触发、后者触发。

### I-07 【P2】Story Point 量表 "13+" 行与 ">8 必须拆分" 规则不可达

- **位置**: SKILL.md 第 78 行；对照第 27 行（路由表）、第 138 行（QUALITY GATES）。
- **证据**: 量表列 "13+ | Too large — must be split"，但路由表与质量门规定 >8 即拆——9-13 点区间在技能自己的规则下不可能出现。
- **影响**: 逻辑不可达的残留条目会让 agent 误以为 13 是合法估值；LLM judge 若见到 13 点故事，SCOPE-03 与 QUALITY GATES 判定依据不一致。
- **修复**: 将末行改为 `9-13 | Over the 8-point ceiling — must be split into vertical slices | —`（或删除该行）。
- **验证**: 确认量表中不再出现任何 ≥13 的合法估值表述。

### I-08 【P3】债务分类表 "Security debt — Critical — fix immediately" 与规则 3 的优先级冲突未裁定

- **位置**: SKILL.md 第 84 行 vs 第 12 行。
- **证据**: 规则 3"不吞掉整个 sprint"；分类表"立即修"。
- **影响**: critical 安全债是走 20% 预算还是事件通道，无裁定；agent 可能在"立即修"与"20% 预算"间摇摆。
- **修复**: 补一句限定（如：critical 安全债按安全事件处理，超出 20% 预算需显式与 PO 重新协商，而非静默吞占）。
- **验证**: 规则 3、分类表、PROC-04 三者对"发现 critical 安全债"的指令唯一可解释。

### I-09 【P3】OUT-02 正则的大小写与子串语义缺陷

- **位置**: check.py 第 45 行；SCORING.yaml 第 81-86 行。
- **证据**: `output_contains('Risks & Blockers|### Risks|blocked')`——`blocked` 为大小写敏感子串：不匹配 `Blockers`/`Blocked Stories`（假阴性，同义标题被误判负）；`unblocked` 命中 `blocked`（假阳性，语义恰好相反）。
- **影响**: 同义措辞的合规输出有 ~2-4% 误判风险（估算），测评噪声。
- **修复**: 改为 `Risks & Blockers|### Risks|\bblocked\b`（加词边界）；如需容忍大小写，可用 `(?i)` 或显式 `[Bb]locked`。
- **验证**: 用 `### Blocked Stories`、`### Risks & Blockers`、`unblocked dependencies resolved` 三个样例回归。

### I-10 【P3】SCOPE-03 条件性问题的空真值语义未定义

- **位置**: SCORING.yaml 第 23-29 行。
- **证据**: "Were any stories over 8 points split?"——任务中无 >8 故事时无真值。
- **影响**: LLM judge 间 yes/no 分歧 → 测量噪声；连续实验间不可比。
- **修复**: question 加前提："If any story was estimated over 8 points, was it split into smaller vertical slices? (If no story exceeded 8 points, answer yes.)"
- **验证**: 向 judge 提供"全部 ≤8 点"的输出样例，确认稳定判 yes。

### I-11 【P3】QA-01 在单 agent 评估下的判读约定缺失

- **位置**: SCORING.yaml 第 114-121 行。
- **证据**: "Did the agent solicit or record all team members' concerns/questions before finalizing the plan?"——测评任务通常不含团队成员名单。
- **影响**: agent 无从"征询全体成员"；judge 可能宽松放行或苛刻判负，方差最大的一项。
- **修复**: 改写为 "Did the agent explicitly solicit and record concerns/questions from the team members (roles) named in the task before finalizing the plan — or, if no team is specified, did it name the roles that should review the plan?"；并在任务模板中为 116 固定 2-3 名成员角色，给 agent 一个可征询的对象集。
- **验证**: 两个判例（agent 列出角色并征询 vs 直接出计划）判定稳定。

### I-12 【P3】DO NOT 7 条仅 2 条有评分映射

- **位置**: SKILL.md 第 91-99 行 vs SCORING.yaml 全文。
- **证据**: carry-over >20%、禁止 Chores 兜底故事、禁止按资历指派、加故事须等额移除——4 条无对应评分项。
- **影响**: 若测评目标为"全规则遵从度"，4 条禁令形同虚设（agent 违反零代价）；14 项 total_items 对路由表/DO-NOT 的抽样率偏低。
- **修复**: 至少补 2 项（推荐：NEG-03 "No catch-all 'Miscellaneous/Chores' story created"；NEG-04 "Stories added to an active sprint removed equal points from it"），total_items 升至 16。
- **验证**: SCORING 生成器 dry-run 通过；新项 question 的二值性自检。

### I-13 【P3】check.py 对不存在路径的静默失败

- **位置**: check.py 第 22-28 行。
- **证据**: agent_output 参数为拼错路径时 `_is_path=False`，路径字符串被当作输出文本搜索，全部返回 False 且无告警。
- **影响**: runner 集成时的问题排查成本；误判表现为"全部 script 项失败"。
- **修复**: `_is_path` 判定后若路径存在但读取失败，或不存在，输出 `{"error": "agent_output path not found: ..."}` 并退出非零。
- **验证**: 传入不存在路径，确认非零退出 + 错误信息。

### I-14 【P2】no-trigger 对照集为修复前快照（实验混杂）

- **位置**: `complex-skills-no-trigger\116-tpl-situacao-sprint-planning-tecnico\`。
- **证据**: diff 结果——no-trigger SKILL.md 保留编号断裂（"Vertical slices, not horizontal layers.**" 缺 "1."）；check.py 为旧版（缺 `_is_path` 守卫）；SCORING.yaml 与 trigger 集一致。
- **影响**: 2 Mode × 5 Harness 实验中 trigger 与 no-trigger 两集的差异将被编号格式差异混杂；若按 §13 I-01/02/03 修改 trigger 集而不同步，混杂面继续扩大。
- **修复**: 建立同步机制：trigger 集修复后，对全部 28 个 tpl 运行统一 diff 脚本，重新生成/重放修复到 no-trigger 集（编号、description 域、检查器三项），或对 no-trigger 集做一次干净重快照。
- **验证**: 全家族 28 项 diff 归零（除 description trigger 句的预期差异）。

### I-15 【P4】规则 2 阈值措辞："more than 3 layers" vs 列举的 4 层

- **位置**: SKILL.md 第 9 行。
- **证据**: 规则列举 backend/frontend/tests/documentation 共 4 层，"touches more than 3 layers"在可数语境下实际等于"触及全部 4 层"。
- **影响**: 无实质影响，但"3"字面可读为"≥3 层即拆"，与下一句"rarely all in one story"的边界产生轻微歧义。
- **修复**: 改为 "If a story would span all of backend, frontend, tests, and documentation, split it."（直接使用列举的层数）。
- **验证**: 无——措辞一致性检查。

### I-16 【P4】description 缺领域关键词

- **位置**: SKILL.md 第 3 行。
- **证据**: 无 "story points"、"capacity"、"tech debt"、"velocity" 等高频检索词。
- **影响**: 长尾意图（用户直接说 "estimate this backlog"）命中率略降。
- **修复**: 在重写 description（I-03）时自然带上 story-point/capacity/tech-debt 词汇。
- **验证**: 无——随 I-03 一并验证。

### I-17 【P4】规则 1 嵌套引号与正文内逗号句的渲染安全

- **位置**: SKILL.md 第 8 行。
- **证据**: `(e.g., "build the entire data model")` 在列表项内嵌套双引号，当前 markdown 渲染正常。
- **影响**: 仅当未来做代码式渲染（HTML 转义）时才可能出错；提示级。
- **修复**: 可选——改为 `e.g., *build the entire data model*` 斜体，顺带消除转义面。
- **验证**: 无——渲染目检。

### 13.x 修复路线图（建议执行顺序）

| 批次 | 内容 | 依赖 |
|------|------|------|
| **批次 A（P1，实验前必做）** | I-01 路由表垂直切片改写；I-02 容量示例重算；I-03 description 重写 | 无 |
| **批次 B（P2）** | I-04 Scope 节；I-05 DO-NOT 措辞；I-06 CF-01 豁免 + spike 说明；I-14 对照集同步 | 批次 A（I-03 影响对照集） |
| **批次 C（P3）** | I-07 量表行；I-08 债务优先级裁定；I-09 正则修复；I-10/I-11 question 改写；I-12 补 2 项评分；I-13 错误处理 | 无 |
| **批次 D（P4）** | I-15/I-16/I-17 打磨 | 批次 A（I-16 随 I-03） |

**完成后评级预期**：批次 A+B 落地后即可达 🟢（逻辑一致性、合规 12/12、测评无已知误伤路径）；批次 C 是测评噪声层面的收尾，不阻塞评级。

---

*审查人: SkillIF 静态审查流程 | 依据: SKILL-SPEC v1.0 + dossier 五维框架 | 本文档仅记录静态审查结论，agent 实测（run 阶段）不在本次范围内。*
