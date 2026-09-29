# REVIEW: 200-legal-writing

**审查日期**: 2026-08-06
**Skill 类型**: process — 法律写作结构性反馈（memo/brief/paper/exam essay，只反馈不代写）
**Body 行数**: 157 行（SKILL.md 全文 162 行，frontmatter 5 行）
**参考文件数**: references/0, scripts/0, 其他 2（SCORING.yaml 166 行、check.py 68 行）
**依据标准**: SKILL-SPEC v1.0（`complex-skills/_shared/SKILL-SPEC.md`，已全文核对）
**审查基准**: 旧 REVIEW.md（182 行，2026-08-05，评 🟢 A− 88/100）＋ skill-dossier.md（🟢 教育设计出色，法律类标杆之一）

---

## 1. 目录全量清单

```
200-legal-writing/
├── SKILL.md         162 行  — 主文件（frontmatter L1-5 + body L6-162）
├── SCORING.yaml     166 行  — 18 项测评点 + 3 项 critical_failures
├── check.py          68 行  — 评测脚本（纯 stub，18 项全部 llm judge）
├── REVIEW.md        182 行  — 旧版审查（本次全量重写）
├── references/      不存在
├── scripts/         不存在
└── 其他子目录        不存在
```

**要点**: 该 skill 是无附带资源（references/scripts 均缺）的纯 body skill。所有知识内嵌于 SKILL.md，文件总数 4，无隐藏文件、无嵌套目录。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

```
name: legal-writing
```

- 小写 + 连字符 ✅；13 字符 ≤ 64 ✅；与目录名 `200-legal-writing` 去除序号后完全匹配 ✅。
- 无任何违规。**判定: 通过。**

### 2.2 description

原文（L3，单行，246 字符 ≤ 1024）：

> Structural feedback on a legal writing draft (memo, brief, paper, exam essay) — organization, analysis depth, clarity, citation form. NEVER rewrites the draft. Use when the user says "feedback on my memo", "read my draft", or "critique my brief".

逐句分析：

| 分句 | 类型 | 评价 |
|------|------|------|
| "Structural feedback on a legal writing draft (memo, brief, paper, exam essay) — organization, analysis depth, clarity, citation form." | WHAT | ✅ 准确具体，覆盖四类文体 + 四个反馈维度，含 domain keywords（memo/brief/paper/exam essay/citation form） |
| "NEVER rewrites the draft." | 否定边界 | ⚠️ 非硬违规（见 §7 checklist 第 2 项），但与 body L22 "Hard rule: no rewriting. Ever." 重复；全大写 "NEVER" 属喊叫式语气（§8.2）；按 SKILL-SPEC §2.1 的 WHAT+WHEN+KEYWORDS 三问框架，否定句不属于任何一问 |
| "Use when the user says \"feedback on my memo\", \"read my draft\", or \"critique my brief\"." | WHEN/trigger | ✅ 符合 §2.4 trigger 信号 "Use when the user..." 家族；三个触发短语均以用户口头自然语言为锚，匹配性好 |

问题记录：
1. **触发措辞**："the user says" 与 spec §2.2 模板的 "the user asks to" 不完全一致，但 §2.4 明列 "Use when the user..." 为合法信号，故不构成违规，仅风格差异（旧 REVIEW 将之列为问题 2 属过度苛责）。
2. **"NEVER" 全大写**：见 §8.2，与本 skill 自身冷静克制的基调相悖。
3. 人称检查：全为第三人称（"Structural feedback… rewrites the draft"），无第一/第二人称 ✅；无 imperative 开头 ✅；无跨 skill 路由 ✅。
4. 长度 246 字符，远低于 1024 ✅；≥40 字符下限 ✅。
5. 无尾随空格/截断 ✅。

**判定: 通过，附带 2 个风格级建议（移除或降调 NEVER 句、says→asks to）。**

### 2.3 allowed-tools

- **未声明**。按 SKILL-SPEC §1.2，`allowed-tools` 为可选字段，缺省不违规。
- 实际执行依赖：`Read`（读草稿/配置）、`Write`（写 tracker.md）。该 skill 理论上不需要 Bash/Grep。
- **建议**：声明 `allowed-tools: Read, Write` 以限制工具面——本 skill 的硬护栏（不重写、不代写）若 agent 借助 Bash 写文件反而更易失控。属优化项，非缺陷。

### 2.4 其他 frontmatter 字段

```
argument-hint: "[paste draft OR path to file]"
```

- `argument-hint` 在 SKILL-SPEC §1.2 允许字段清单中明列 ✅（旧 REVIEW 未质疑，正确）。
- 取值 `[paste draft OR path to file]`：清晰、可执行，与正文 L39 "Student-provided draft" 一致 ✅。
- 无任何 forbidden 字段（对照 §1.3 黑名单逐项核对：无 metadata/license/version/agents/tags 等）✅。

**判定: 通过。**

### 2.5 Frontmatter 语法

- YAML 结构：`description` 为未加引号的 plain scalar，内含双引号（"feedback on my memo" 等）。YAML plain scalar 允许内嵌引号（仅禁止以引号开头），无 `: ` 序列，解析安全 ✅。
- `argument-hint` 使用双引号包裹，内部 `|` 无冲突 ✅。
- 无制表符、无 BOM、无重复键 ✅。frontmatter 以 `---` 正确闭合（L5）✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行号 | 标题 | 行数 | 内容概要 |
|------|------|:----:|----------|
| L6 | `# Legal Writing`（H1） | 1 | 唯一 H1，标题即正文 |
| L8-14 | 顶层编号执行流 1-7 | 7 | Load config → Apply framework → Read draft → Give feedback → 示例上限 → 拒绝重写 → 追加 tracker |
| L18-22 | `## Purpose` | 5 | 定位：反馈而非代写；Hard rule 首现 |
| L24-28 | `## Why the rule is strict` | 5 | 教育原理论证（考试的代价、struggle 的价值） |
| L30-34 | `## Confidence discipline` | 5 | 三类反馈的置信度分级 |
| L36-40 | `## Load context` | 5 | 输入来源：config、草稿、可选 rubric |
| L42-118 | `## Workflow` | 77 | 详细五步工作流（本文件最大节） |
| L44-46 | `### Step 1: Read the whole draft` | 3 | 通读原则 |
| L48-55 | `### Step 2: Identify the structural type` | 8 | 四类文体惯例 |
| L57-118 | `### Step 3: Structured feedback (no rewriting)` | 62 | 含 L61-118 反馈模板代码块（58 行） |
| L120-129 | `### Step 4: If the student asks you to rewrite` | 10 | 拒绝话术 + 三个替代出口 |
| L131-144 | `### Step 5: Track patterns` | 14 | tracker 追加模板 + 3 次后模式识别 |
| L146-150 | `## Integration` | 5 | irac-practice / socratic-drill / flashcards 引用 |
| L152-154 | `## Close with the next-steps decision tree` | 3 | 结束动作（依赖 config 的 Outputs） |
| L156-162 | `## What this skill does not do` | 7 | 5 条否定边界 |

9 个 `##` + 5 个 `###`，层级规整（H1 仅一个，位于正文首行，无跳级）。

### 3.2 必需章节检查

| 必需章节 | 状态 | 位置与说明 |
|----------|:----:|------------|
| Workflow / Process | ✅ | `## Workflow` L42-144，五步完整闭环 |
| Output Format | ⚠️ 弱通过 | 输出模板完整存在（L61-118 代码块），但嵌在 `### Step 3` 内部而非独立 `##` 节。按 spec §3.1 "under any heading name" 可算满足；严格判读则属于"存在但未独立成节" |
| Scope / Limitations | ✅ | `## What this skill does not do` L156-162，5 条否定边界 + 正文内另有硬规则呼应 |

**判定: 三节齐全，输出节独立性为唯一弱项。**

### 3.3 内容委托分析

- 本 skill 无任何 reference 文件，零委托；全部指令内嵌 body，157 行自包含。
- 唯一的"外部委托"是环境类资源：`~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md`（L8/L38）与 tracker 路径（L14/L133）、CLAUDE.md `## Outputs`（L154）。这属于**运行时环境依赖**而非文件委托，详见 §5。
- 跨 skill 引用（Integration 节 L146-150）为散文式建议，非内容委托。

### 3.4 节编号/标题层级

- **顶层编号 1-7（L8-14）与 Workflow 内部 Step 1-5（L44-144）是两套并行编号体系**。对照：

| 顶层编号 | 内容 | 详细 Workflow 对应 |
|:--------:|------|:-------------------:|
| 1 | Load config | 无（仅 `## Load context` 散文段） |
| 2 | Apply the framework below | 无对应编号 |
| 3 | Read full draft + identify type | Step 1 + Step 2 |
| 4 | Give structured feedback | Step 3 |
| 5 | Example 上限 1-2 | Step 3 内嵌约束 |
| 6 | 拒绝重写 | Step 4 |
| 7 | 追加 tracker | Step 5 |

  除 3→(1,2) 与 5→3 的对应关系外，两套编号在编号序上完全错位（顶层 1-2 无编号对应、顶层 5 无独立对应）。agent 读完全文后会面临"以哪套编号为准"的歧义——这是本 skill 最真实的逻辑缺陷，旧 REVIEW 亦已识别。

### 3.5 Body 长度合规

- body 157 行（L6-162），远低于 600 行硬限 ✅。
- 对照 spec §3.2 process 模式目标 ~200 行：157 行略紧凑，但结构完整、无缺失感；模板内嵌使"可读密度"高。合规。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- 顶层执行流（L8-14）是"总纲"，Workflow（L42-144）是"细则"，二者内容实质一致（同一组行为），仅编号与粒度不同——**衔接不坏，但编号错位造成执行顺序歧义**（§3.4）。若 agent 严格按顶层 1-7 执行，会在第 3 步一次性完成详细 Workflow 的 Step 1+2，并在第 4 步输出；若按详细 Step 1-5，则跳过"load config"编号位。两种解读的最终产物相同，但中间行为（是否先 load config）不同，直接影响 SCOPE-02 测评。
- Step 3 内部顺序（structure → analysis → clarity → top 3 fixes）与顶层 Step 4（"structure first, analysis depth, clarity & style, top 3 fixes"）完全一致 ✅。
- Step 4 拒绝分支（L120-129）与顶层 Step 6 一致 ✅；Step 5 tracker（L131-144）与顶层 Step 7 一致 ✅。

### 4.2 内部矛盾扫描

1. **双编号体系**（§3.4）：真实缺陷，唯一实质性矛盾点。
2. **"At most 1-2 labeled example phrasings"（L12）vs "One example to illustrate"（L106 标题）**：措辞不一致，但 1 ∈ [1,2]，语义不冲突，属表述不齐而非矛盾。低危。
3. **示例边界张力**：Scope 节（L159）声明示例"not in the specific form the student is working in"，而模板 L113 要求 "Write your own version of this move for **your Issue 2**"——"your Issue 2"把通用示例锚定到学生具体作业语境。模板的示例本身（L110-111）用 `[Generic example…]` 占位符规避了实质内容，张力仅存在于"改写指引"措辞，未实际越界。中低危。
4. **"Don't silently trust my substantive calls."（L33）人称辨析**：本句 "I/my" 均指 skill 自身（agent 视角），与前句 "flag [VERIFY] on anything I'm not certain about" 的 "I" 一致；整段（L32-34）是 skill 对"自身行为"的自述，人称自洽 ✅（初读易误判为"学生"，细读无矛盾）。
5. **硬护栏六处呼应**：description "NEVER rewrites"（L3）、Purpose "Hard rule: no rewriting. Ever."（L22）、顶层 Step 6（L13）、详细 Step 4（L120-124）、Scope "Rewrite. Period."（L158）、模板结尾 "Not rewritten. Not a model answer."（L117）——六处表述方向一致、无一处软化或冲突 ✅。这是全 skill 一致性最强之处。
6. **置信度分级三处一致**：Confidence discipline（L32-34）、模板 Analysis depth 节（L82）、模板 Citation form 节（L98）——structure 自信 / content 与 citation 边缘 `[VERIFY]` 的三级规则贯彻到底 ✅。

### 4.3 示例/代码正确性

- 反馈模板（L61-118）：markdown 结构完整（H2/H3/加粗/引用块/分隔线），占位符 `[assignment / date]`、`[N words]`、`[memo / brief / paper / exam essay]` 均有明确取值域 ✅。
- 拒绝话术（L124）：直接引语，语法正确，语气与 "gracefully, not preachy" 一致 ✅。
- tracker 模板（L135-142）：6 字段与"3+ sessions 后识别模式"（L144）逻辑呼应 ✅。
- 法律内容抽查：模板 L98 "signals, pincites, id. vs. ibid."——Bluebook 体系只用 "id."，而 "ibid." 主要用于非美国体系（如 OSCOLA 部分场景）；此处将二者并列作"常见错误"示例，术语上不算错（确实是学生混淆点），但未指明体系差异。极轻微瑕疵。
- L154 "five default branches (draft the X, escalate, get more facts, watch and wait, something else)"：与声称的 CLAUDE.md `## Outputs` 一致与否无法验证（外部资源），但五个分支内部自洽。

### 4.4 条件完整性

| 条件分支 | 处理 | 评价 |
|----------|------|------|
| 用户要求重写 | L13/L120-129 完整拒绝路径 + 3 个替代出口 | ✅ 完整 |
| 结构破损 vs 句子润色 | L59 "Don't skip to sentence-level polish if the structure is broken" | ✅ 明确 |
| 长度目标未知 | L65 "[if target known: vs. target N]" | ✅ 条件化 |
| 3+ 次会话 | L144 模式识别 | ✅ 条件化 |
| 文体超出四类（motion/contract/statute） | 无处理 | ⚠️ 缺口（低危） |
| 草稿路径不存在/粘贴为空 | 无处理 | ⚠️ 缺口（低危） |
| config 文件不存在 | 无 fallback | 🔴 重要缺口（见 §5.2） |
| tracker 目录不可写 | 无 fallback | 🔴 重要缺口（见 §5.2） |

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用对象 | 出现位置 | 包内存在？ | 状态 |
|----------|----------|:----------:|------|
| `~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md` | L8, L38 | 否 | 🔴 外部环境依赖 |
| `~/.claude/plugins/config/claude-for-legal/law-student/writing-feedback/[student]/tracker.md` | L14, L133 | 否 | 🔴 外部环境依赖 |
| CLAUDE.md `## Outputs`（决策树基准） | L154 | 否 | 🔴 外部环境依赖 |
| `/law-student:irac-practice` | L148 | 语料库内有 `164-irac-practice`，但引用为插件命令格式 | ⚠️ 格式不符 |
| `/law-student:socratic-drill` | L129, L149 | 否（语料库无 socratic-drill） | ⚠️ 引用不存在 |
| flashcards | L150 | 否（语料库无同名 skill） | ⚠️ 引用不存在 |
| references/ 内文件 | — | 无此目录 | 不适用 |

### 5.2 不可见资源审计

本 skill 的全部"参考文件"均为**运行时环境路径**而非包内资源，构成 3 类不可见依赖：

1. **配置类**（L8/L38）：要求 agent 读取插件配置以获取"class、writing skill level、past feedback patterns"。在 SkillIF 评测工作区中，该文件大概率不存在（skill 包内无任何 seed 文件）。**SKILL.md 未给出任何"文件缺失时如何继续"的指令**——agent 只能自行推断。后果是行为方差大：有的 agent 跳过继续，有的卡在读文件重试。
2. **写入类**（L14/L133）：tracker.md 路径含 `[student]` 占位符，且**全 skill 无一处说明 student 标识如何确定**（从对话？从文件名？从 config？）。若工作区不可写或目录不存在，append 步骤无 fallback。
3. **输出类**（L154）：要求"End with the next-steps decision tree per CLAUDE.md `## Outputs`"——输出格式的一部分依赖外部文档的章节结构。

这 3 类依赖共同导致：**skill 的完整执行链在脱离 claude-for-legal 插件生态的独立环境中无法按原文完成**。旧 REVIEW 以"可移植性 4/10"部分捕获了此问题，但未上升到"SCORING.yaml 有 3 个测评点依赖同一外部资源"的层面（见 §10）。

### 5.3 Reference 文件全文审查

`references/` 目录不存在，0 个文件。对 process 型 skill 而言缺 reference 不构成缺陷（157 行 body 已自包含），但这也意味着：本 skill 没有"模板长文"或"惯例速查"等可下沉内容——目前模板内嵌 body 是合理取舍。

### 5.4 Scripts 文件全文审查

`scripts/` 目录不存在。根目录的 `check.py`（68 行）为评测脚本而非技能脚本，审查如下：

- 结构：标准 runner 接口（`check(workspace, tool_log, agent_output) -> dict[str, bool]`），从 `_shared/checker` 导入 `set_tool_log_path` / `set_agent_output`。
- **全部 18 项标准均标注 "llm judge (not checked here)"，`result` 恒为 `{}`**。docstring 自称 "Run all 0 script checks"，诚实但意味着：本 skill 的机械校验为零，100% 依赖 LLM 判官。
- `critical_failures`（CF-01~03）在 check.py 中无任何实现——若 harness 依赖 check.py 输出 CF 判定，此处为功能缺口；若 CF 由 runner/LLM 判官处理，则无碍。无法从包内确认 runner 行为，标记待核。
- 无语法错误、无 import 错误（`_shared/checker` 存在于 corpus 根，已确认）。

**判定: check.py 作为"全 LLM 判定"设计的载体可接受，但零机械检查 + CF 未实现值得评审侧知悉。**

### 5.5 跨 Skill 引用检查

- Integration 节（L146-150）按 SKILL-SPEC §3.3 的精神用名称引用其他 skill，方向正确；但**格式使用了插件命令前缀 `/law-student:`**，而语料库内对应实体是独立 skill `164-irac-practice`（无前缀）。`socratic-drill` 与 `flashcards` 在 322 个 skill 中**不存在**——引用落空。
- 参照同类：dossier 中 150/173/251 等 skill 的跨 skill 路由被标记为描述级违规；本 skill 的引用在 body 非 description，属 §2.5 允许的位置，但落空引用仍削弱可操作性。
- **建议**：改为纯名称散文引用（"see also: irac-practice"），并删除不存在的 socratic-drill/flashcards 或标注 "if installed"。

### 5.6 嵌套重复/死文件

- 无嵌套目录、无重复文件、无残留（无 047 式截断、无 055 式 "`..` skill" 占位符、无 196 式重复残留）。
- `[student]` 为有意占位符（需运行时填充），非死内容，但填充规则缺失（见 §5.2）。

### 5.7 其他资源文件

无。目录仅含 4 个文件，已全量审查。

---

## 6. 语法与格式质量

### 6.1 拼写错误

全文逐行核对：**0 处拼写错误**。专业法律术语拼写正确（pincites、conclusory、IRAC/CRAC、Bluebook、ALWD、expository/normative/analytical）。

### 6.2 语法错误

**0 处**。句子完整、时态一致、无残缺句（对比 070 的 "which servers"、081 的截断）。条件句（"if target known"）、让步句（"even if"）、插入语用法全部规范。

### 6.3 中英/葡英混杂

**无**。全文纯英文，无葡萄牙语泄漏（对比 093/262/319 的混入）、无中英混排。与语料库中 tpl 家族（029/030/131/132 葡语模板）形成鲜明对照。

### 6.4 Markdown 格式破损

- 无破损围栏（L61 与 L118 的 ```markdown 围栏正确闭合）；无断裂粗体、无丢失列表编号（对比 tpl 家族首条编号丢失通病）。
- H1 唯一且位于正文首行，H2/H3 层级无跳级；列表嵌套规范（L49-53 二级列表缩进一致）。
- 分隔线 `---`（L16/L67/L115）语义正确：L67/L115 在模板代码块内部，渲染安全。
- 模板内部引用块（L110-113 `>` 嵌套）格式正确。
- 唯一轻微瑕疵：模板 L98 与 L111 中 `—`（em dash）与 `-`（连字符）混用（如 "Common errors — signals, pincites" vs 顶层 L12 "1-2 labeled example"），风格不齐但语义无碍。

### 6.5 占位符未填充

| 占位符 | 位置 | 状态 |
|--------|------|------|
| `[paste draft OR path to file]` | frontmatter argument-hint | ✅ 有意占位，语义自明 |
| `[assignment / date]`、`[N words]`、`[memo / brief / …]` 等 | 模板 L62-64 | ✅ 模板内字段，取值域明确 |
| `[Generic example demonstrating the move]` | L111 | ✅ 有意占位（防代写设计） |
| `[student]` | L14/L133 | ⚠️ 有意占位但**填充规则缺失**（如何识别学生身份） |
| `[date]`、`[assignment type / subject]` | tracker 模板 L136 | ✅ 模板内字段 |

### 6.6 截断内容

**无截断**。L162 以完整句 "Not a Bluebook checker." 干净收尾（对比 081/271 的中途截断）。

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 证据 |
|---|--------|:----:|------|
| 1 | name 小写+连字符、≤64、匹配目录 | ✅ | `legal-writing` ↔ `200-legal-writing` |
| 2 | description 第三人称 WHAT+WHEN+KEYWORDS、≤1024 | ✅ | 246 字符；WHAT/WHEN/KEYWORDS 三问齐全（附 1 个否定句噪音） |
| 3 | description 无 imperative/first/second 开头 | ✅ | 以名词短语 "Structural feedback…" 开头；无 I/You/We |
| 4 | description 无跨 skill 路由 | ✅ | 路由仅在 body（Integration 节），位置合规 |
| 5 | description 含 trigger 信号 | ✅ | "Use when the user says…"（§2.4 "Use when the user..." 家族） |
| 6 | frontmatter 无禁止键 | ✅ | 仅有 name/description/argument-hint，三者均在允许清单（§1.1/§1.2） |
| 7 | body ≤600 行 | ✅ | 157 行 |
| 8 | body 含 workflow 节 | ✅ | `## Workflow` L42-144 |
| 9 | body 含 output format 节 | ⚠️ 弱通过 | 模板完整（L61-118）但嵌于 Step 3 内、无独立 `##` 标题 |
| 10 | body 含 scope 节 | ✅ | `## What this skill does not do` L156-162 |
| 11 | body 无 `../` 跨 skill 文件路径 | ✅ | 无相对跨目录引用；但存在 `~/.claude/plugins/...` 绝对路径（规范未明令禁止，属可移植性风险，见 §5.2） |
| 12 | 目录 NNN-kebab-case 无空格大写 | ✅ | `200-legal-writing` |

**合规得分: 12/12 通过或弱通过，0 硬违规。** 该 skill 是语料库中少数"三必需节 + description 全绿"的完整合规样本（dossier 亦确认三节齐备）。

---

## 8. 人机感评估

### 8.1 Emoji 审计

**0 个 emoji**。无装饰性图标（对比 072 的 20+ emoji）。✅ 标杆级克制。

### 8.2 全大写/喊叫

- "NEVER rewrites the draft."（L3，description）——唯一的全大写喊叫，且出现在最外层元数据。
- "Hard rule: no rewriting. Ever."（L22）——"Hard rule" 大写为强调，可接受；"Ever." 短句收束有力，非喊叫。
- 其余无全大写段落（对比 032 的 "⚠️ MANDATORY"、153 的 "MANDATORY/CRITICAL" 连发）。**整体 9/10，唯一扣分项是 description 里的 NEVER。**

### 8.3 Persona 语气

- 贯穿全篇的教学者 persona：讲道理（"Writing is how lawyers think on paper." L20）、讲代价（L26 考试/律所的后果）、讲方法（L28 示例的教学价值）——**规则永远附理由**，这是该 persona 最突出的质量。
- 拒绝话术（L124）"I don't rewrite. The point of writing practice is that you do the writing."——坚定而不说教，是语料库中最好的 refusal 设计之一（与 037 "If you ask me to do it, I won't." 同水准）。
- 语气一致性：无一处跳戏（对比 140 的 "Nano Banana Pro" 商业植入）。

### 8.4 人机边界

- **学生写作主体地位保护**（dossier 原话）落实为 6 处硬护栏（§4.2-5）+ 3 个替代出口 + "write yours — don't copy" 标签 + 模板结尾 "Your draft stays yours."——边界不是一句口号，而是可检查的操作规则（数量上限、标签格式、内容禁区）。
- VERIFY 标记（L11/L33/L34/L82/L98）是"承认不确定"的诚实机制，人机信任设计典范。

### 8.5 人称分析

- description 用第三人称指 skill（"rewrites the draft"）；body 用第一人称指 agent（"I'm unsure about"）、第二人称指学生（"your Issue 2"）——**frontmatter 与 body 的人称切换是规范要求的正确形态** ✅。
- 轻微瑕疵：description 用 "the user"（L3），body 用 "the student"（L26 起）——同一对象两种称谓，不影响执行，但可统一。
- 双重受众（对 agent 的指令 + 对学生的话术）由引用块/模板显式区分（L124 引用块是"话术"，L44 等是"指令"），无 101 式受众混淆。

### 8.6 表格太多

body 0 表格（模板为列表结构）。列表密度合理，无表格过载问题。✅

**人机感结论: 语料库标杆级（与 322-cold-start-interview、212-written-consent 同档）。**

---

## 9. 可执行性评估

### 9.1 独立可执行性

- **核心流程（读草稿 → 判类型 → 结构化反馈）完全独立可执行**：157 行自包含，无 references 依赖，模板即产物。
- **完整流程（含 config 加载与 tracker 追加）依赖外部环境**：3 处 `~/.claude/plugins/...` 路径在无插件生态的环境下不可达，且无 fallback 指令（§5.2）。agent 实际行为将是"尝试读取→失败→自行决定继续"，行为方差大。
- **独立性评分：核心 9/10，完整链 5/10。**

### 9.2 步骤可操作性

- 每步均有可验证产物：类型命名（L55 显式要求"Name the type explicitly"）、模板节顺序、TOP3 优先级、1-2 示例上限、`[VERIFY]` 数量、tracker 记录——**可操作性为语料库最高一档**。
- FMT-03 类"具体性"要求（L88/L94 "Specific examples, not 'reduce passive voice'"）自带反例示范，防 agent 输出空泛反馈。
- 唯一不可操作项：`[student]` 的填充（§6.5）与 config 缺失路径（§9.1）。

### 9.3 工具依赖

- 仅需 Read + Write；无 Bash/Grep 依赖 ✅。
- 未声明 allowed-tools（§2.3），工具面无约束，属宽松而非缺陷。
- 外部写路径（tracker.md）权限未知——若 harness 工作区只读，PROC-05 直接失败。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 共 166 行：18 项标准（scope 3 + process 5 + format 4 + negative 3 + qa 3）+ 3 项 critical_failures。逐项与 SKILL.md 对表：

| 测评点 | 对应 body 依据 | 可达成性 | 备注 |
|--------|----------------|:--------:|------|
| SCOPE-01 识别为反馈而非起草任务 | L3/L20/L22 | ✅ 可达 | description 已承担此区分 |
| SCOPE-02 加载 law-student config | L8/L38 | 🔴 **环境依赖** | 包内无此文件；评测工作区若无 seed 则恒败 |
| SCOPE-03 通读全文再反馈 | L44-46 | ✅ 可达 | Step 1 明确 |
| PROC-01 显式命名结构类型 | L48-55 | ✅ 可达 | Step 2 + L55 |
| PROC-02 自上而下（结构→段落→句子） | L57-59 | ✅ 可达 | 模板顺序即判据 |
| PROC-03 覆盖 10 个反馈维度 | L70-98 | ✅ 可达 | 模板逐节对应 |
| PROC-04 TOP3 按优先级 | L100-104 | ✅ 可达 | 模板结构决定 |
| PROC-05 追加 tracker.md | L131-144 | 🔴 **环境依赖** | `[student]` 无填充规则 + 外部路径 |
| FMT-01 输出遵循模板 | L61-118 | ✅ 可达 | 模板即产物 |
| FMT-02 示例 ≤2 且带标签 | L12/L106-113 | ✅ 可达 | 数量上限可数 |
| FMT-03 反馈具体到段落 | L88/L94 | ✅ 可达 | 自带反例 |
| FMT-04 `[VERIFY]` 纪律 | L11/L33-34/L82/L98 | ✅ 可达 | 三级规则清晰 |
| NEG-01 永不重写 | L22/L158 | ✅ 可达 | 六处护栏 |
| NEG-02 拒绝并给替代 | L120-129 | ✅ 可达 | 话术即产物 |
| NEG-03 示例不涉学生主题 | L159 | ✅ 可达 | 占位符机制 |
| QA-01 3+ 次会话后模式识别 | L144 | ⚠️ 单次评测难触发 | 需要多会话连续性 |
| QA-02 不冒充教授/不宣称全知 | L160 | ✅ 可达 | Scope 节明言 |
| QA-03 以决策树收尾（per config Outputs） | L152-154 | 🔴 **环境依赖** | 依赖外部 config 的 Outputs 结构 |

**18 项中 14 项完全可达，3 项环境依赖（SCOPE-02/PROC-05/QA-03），1 项（QA-01）受单次评测限制。** 评测设计问题：SCORING.yaml 将环境资源可达性当作 agent 行为来测。

### 10.2 Critical Failures 分析

| CF | 描述 | 评估 |
|----|------|------|
| CF-01 | 重写草稿/提供模型答案（cap_to_0） | ✅ 与技能存在理由精确对应（"the one thing the skill exists to prevent"），护栏与评分闭环 |
| CF-02 | 结构破损时给句子级润色（cap_to_0） | ✅ 对应 L59 明文规则 |
| CF-03 | 未验证规则不带 [VERIFY] 当定论输出（cap_to_0） | ✅ 对应 L33-34 三级纪律 |

- 三条 CF 全部与 body 显式规则一一对应，无"评分与正文脱节"问题（对比 153 的 description-body 矛盾）。
- 观察项：check.py 未实现 CF 判定（§5.4），cap_to_0 的执行机制在包内不可见，需 runner 侧确认。
- `total_items: 18` 与实际条目数一致 ✅；`pattern: process` 与目录类型一致 ✅。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

### 11.1 Dossier 原始记录核对

Dossier 相关记录（2026-08-05 审查批次）：

- Batch 176-200 汇总行："185/197/200 🟢 三节齐备…总评: 🟢 185/197/200 法律类标杆"；
- 人机感维度："200 学生写作主体地位保护到位"；
- 典范列表："| 200 | legal-writing | 教育设计出色 |"。

**经本次全量重审：dossier 的 🟢 判定成立。** 具体验证：三节齐备 ✅（§3.2）、教育设计出色 ✅（§8.3-8.4 六处护栏 + 理由化规则 + VERIFY 诚实机制）、写作主体保护 ✅（模板 "Your draft stays yours." 与拒绝话术）。

### 11.2 与旧 REVIEW.md 的分歧调查（重要）

**任务描述称"旧 REVIEW.md 只给了 B（50/100）"，但实读旧文件：其给出的是 🟢 A−（88/100），与 dossier 🟢 完全一致。** 不存在"dossier 🟢 vs 旧评审 B"的矛盾——该前提与文件内容不符，予以纠正。

进一步核查发现旧 REVIEW 自身有两处可议之处：

1. **评分算术不自洽**：旧 REVIEW 的维度表（Frontmatter 8 + 逻辑 8 + 语言 10 + 人机感 10 + 结构 9 + 可移植 4 + 可执行 8 = 57/70 ≈ 81 分），却宣告"综合 🟢 A−（88/100）"——88 既不等于其表内算术结果（≈81），也未说明权重。**旧评分的"高"部分来自对其自身表格的偏离。**
2. **自评矛盾**：旧 REVIEW 给"可移植性 4/10"，却在综合分中几乎未让它发挥作用（若按 81 分仍达 A−）。可移植性是其自己承认的硬伤，未在结论中形成约束。

### 11.3 Dossier 遗漏的问题

Dossier 为一行式正面评价，未覆盖（本次审查新发现）：

1. **双编号体系**（§3.4）——agent 执行顺序歧义，dossier 未提。
2. **3 项 SCORING 标准环境不可达**（§10.1 SCOPE-02/PROC-05/QA-03）——评测可行性问题，dossier 未提。
3. **`[student]` 占位符无填充规则**（§6.5）——dossier 未提。
4. **跨 skill 引用落空**（§5.5：socratic-drill/flashcards 在 322 语料库中不存在；irac-practice 引用格式为插件前缀）——dossier 未提。
5. **description 的 NEVER 全大写**（§8.2）——dossier 未提。

### 11.4 结论

Dossier 🟢（教学设计与合规角度）与本次 8 维加权评分 🟡B（含可移植性/环境依赖后的综合）**并不冲突**：dossier 评的是"写得好不好"，加权框架还量了"离开插件生态能不能跑"。两者结论的差即旧 REVIEW 未建模的部分——**本 skill 的核心资产（教育设计）与核心负债（环境耦合）同源**：它是一枚精心打磨的插件内零件，而非独立 skill。

---

## 12. 综合评分 — 8 dimensions weighted table

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | name/description/argument-hint 全合规；扣分：NEVER 全大写否定句挤占 WHAT+WHEN、says→asks to 措辞 |
| Body 结构完整 | 8/10 | 10% | 0.80 | 三必需节齐全；扣分：输出模板非独立节、双编号体系 |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 六处护栏/三级置信度完美自洽；扣分：顶层 1-7 vs Step 1-5 编号错位（真缺陷）、示例边界微张力 |
| 参考完整性 | 5/10 | 15% | 0.75 | references/ 0 文件可接受；3 处外部绝对路径无 fallback、2 个跨 skill 引用落空、`[student]` 未定义 |
| 语法格式 | 10/10 | 10% | 1.00 | 0 拼写/语法错误，0 中英混杂，markdown 零破损，无截断 |
| 规范合规 | 9/10 | 15% | 1.35 | 12/12 通过或弱通过、0 硬违规；仅输出节独立性为弱项 |
| 人机感 | 10/10 | 10% | 1.00 | 0 emoji、拒绝话术标杆级、学生主体保护六重落实 |
| 可执行性 | 7/10 | 10% | 0.70 | 核心流程 9 分可执行；完整链被 config/tracker/决策树 3 处环境依赖拖累 |
| **加权总分** | | | **7.80** | **78/100** |

Rating: 🟡 **B**

**与旧 REVIEW（A− 88）的差异解释**：旧评分以"教学写作质量"为重心且算术不自洽（§11.2）；本次按 8 维加权，环境依赖（参考完整性 5 + 可执行性 7）将总分压在 A 线之下。若评测环境保证 seed 了插件 config，本 skill 可上探 83-85（A−）。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（不修复则评测必失分项）

1. **外部配置依赖无回退（SKILL.md L8/L38）**
   在 `## Load context` 增加显式 fallback："If this config file is not present (e.g., outside the claude-for-legal plugin), proceed without it and base feedback on the draft alone — do not stall." 同时把顶层 Step 1 的指令改为条件式。此举直接决定 SCOPE-02 在评测中的命运。
   **工作量**: 约 15 分钟。

2. **tracker 写入路径不可达 + `[student]` 无填充规则（L14/L133）**
   双管齐下：(a) 增加"学生身份取自对话中用户自报姓名，否则用 drafts 文件名，再否则用 'unspecified'"的解析规则；(b) 增加"目录不存在则创建；不可写则跳过并在反馈末尾注明本次会话模式未存档"的回退。此举决定 PROC-05 的可达成性。
   **工作量**: 约 20 分钟。

3. **QA-03 依赖外部 config 的 `## Outputs`（L152-154）**
   将决策树从"per CLAUDE.md"改为自带：在正文内嵌五分支的迷你定义（draft the X / escalate / get more facts / watch and wait / something else 各一句释义 + 本 skill 定制化示例），使收尾动作脱离外部文档。
   **工作量**: 约 20 分钟。

4. **SCORING.yaml 与环境的对齐（SCOPE-02/PROC-05/QA-03 措辞）**
   三项标准的 description 均以"agent 必须成功加载/写入外部资源"为前提。建议改判据为"尝试加载并在缺失时优雅回退（agent states the config is unavailable and proceeds）"，或由评测 harness 在工作区 seed 对应 config 文件。二选一，但**必须二选一**，否则 18 项中 3 项恒败、测评信度受损。
   **工作量**: 约 30 分钟（含重跑评测）。

### 🟡 重要缺陷（影响一致性与可维护性）

5. **统一双编号体系（L8-14 vs L42-144）**
   推荐方案：保留 Workflow 为唯一编号源（Step 1-5），将顶层列表改造为"执行概览"（Overview: load config → apply workflow → append tracker），编号全部去掉或改为罗马序。次选方案：顶层 Step 1-2 并入 Workflow 使其一一对应。旧 REVIEW 亦列此项，一年来未修。
   **工作量**: 约 30 分钟。

6. **跨 skill 引用落空与格式（L129/L148-150）**
   `/law-student:irac-practice` → 按 SKILL-SPEC §3.3 改为散文引用 "see also: irac-practice"；`socratic-drill` 与 `flashcards` 在语料库不存在，删除或改为 "if you have a socratic-drill skill installed"。防止 agent 尝试调用不存在的命令。
   **工作量**: 约 15 分钟。

7. **description 的 NEVER 句（L3）**
   两个选项：(a) 删除，保留 WHAT+WHEN 纯净（body L22/L158 已充分表达护栏）；(b) 保留但降调为 "Does not rewrite drafts."——去全大写、去重复。推荐 (a)。
   **工作量**: 约 5 分钟。

8. **输出模板独立成节**
   将 L61-118 模板代码块从 `### Step 3` 内提出，设 `## Output Format`（模板原样放入），Step 3 只描述"按 Output Format 组织反馈"。消除 §3.2 的弱通过状态，并让 FMT-01 判据更醒目。
   **工作量**: 约 15 分钟。

9. **示例边界措辞（L106/L113）**
   将 "Write your own version of this move for your Issue 2" 改为 "Write your own version on your own topic"，消除与 L159 "not in the specific form the student is working in" 的张力；模板标题 "One example" 与顶层 "at most 1-2" 统一为 "Example (at most 2)"。
   **工作量**: 约 10 分钟。

### 🟢 优化建议（锦上添花）

10. **声明 allowed-tools: Read, Write**——限制工具面，与"不代写"护栏协同（§2.3）。
11. **统一 "the user" / "the student" 称谓**（L3 vs body），建议 body 内首处使用前说明二者同义或统一用 the user。
12. **补边界条件处理**：文体超出四类（motion/contract/statute）时的降级策略；草稿路径不存在/内容为空时的提示话术。各 1-2 句即可。
13. **模板 L98 "id. vs. ibid." 加体系注**："(Bluebook uses id. only; ibid. appears in some non-US systems)"，防 agent 误教。
14. **顶层 Step 2 "Apply the framework below." 删除**——空步骤无信息量，或改为 "Follow the Workflow section."。
15. **`## Close with the next-steps decision tree` 标题去掉 "Close with"**——节标题无需动词祈使（与 §3.1 各节标题风格统一）。

### 修复工作量估计

| 层级 | 项数 | 估计工作量 |
|------|:----:|:----------:|
| 🔴 致命 | 4 | 约 1.5 小时（含 SCORING.yaml 修订 + 重跑评测） |
| 🟡 重要 | 5 | 约 1.5 小时 |
| 🟢 优化 | 6 | 约 1 小时 |
| **合计** | 15 | **约 3.5-4 小时** |

全部为 SKILL.md 与 SCORING.yaml 的文本修订，无需新增文件；改完即可复评（预期加权总分 78 → 85+，评级 B → A−）。**按惯例不动 references/scripts（本 skill 无此二者）。**

---

## 附录: 审查过程记录

- **审查日期**: 2026-08-06（昨日 2026-08-05 旧 REVIEW 为批次 176-200 审查产物）
- **审查方式**: 全文件直读（非抽样），逐行比对
- **读取文件**（4/4，100%）：
  1. `SKILL.md` — 162 行，全文 2 遍（第一遍结构定位，第二遍逐行语法/人称/编号核对）
  2. `SCORING.yaml` — 166 行，全文 1 遍 + 与 body 逐项对表
  3. `check.py` — 68 行，全文 1 遍 + 与 SCORING 条目核对
  4. `REVIEW.md`（旧版）— 182 行，全文 1 遍，作为分歧调查对象
- **外部参照**:
  1. `complex-skills/_shared/SKILL-SPEC.md`（v1.0，162 行）— 合规判定的唯一依据，12-item checklist 全部以原文核对（含 §1.2 allowed fields、§2.4 trigger 信号、§3.1 必需节、§3.3 引用规则）
  2. `memory/skill-dossier.md`（1203 行）— 定位 200-legal-writing 的 🟢 记录（Batch 176-200 汇总行、典范列表、人机感维度行），并核对 164-irac-practice 等同类条目
  3. `complex-skills/` 目录 Glob — 确认 322 个 sibling；核实 irac-practice（存在，编号 164）、socratic-drill（不存在）、flashcards（不存在）
- **工具**: Glob（目录清单 ×2）、Read（7 文件）、Grep（SKILL-SPEC 定位）、Bash（行数统计、description 字符数 246、body 157 行）
- **关键纠错**: 任务描述称"旧 REVIEW 给 B（50/100）"——实读为 🟢 A−（88/100），已在 §11.2 纠正并归因（旧评分算术 57/70≈81 ≠ 88，自洽性存疑）
- **限制声明**: 评测 harness 是否 seed 插件 config 无法从包内确认，SCOPE-02 的可达成性结论基于"包内无该文件"这一确定事实推断；runner 对 critical_failures 的执行机制（check.py 未实现）无法验证。
