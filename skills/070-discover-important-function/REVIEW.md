# REVIEW: 070-discover-important-function

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — Python 代码库 fuzz 目标定位（文件定位 → 函数定位 → 测试总结 → FUT 决策四阶段管道）
**Body 行数**: 403 行
**参考文件数**: references/0, resources/0, scripts/0（技能完全自包含，无任何文件引用）
**总文件数**: 4（SKILL.md, SCORING.yaml, check.py, REVIEW.md）
**已有 REVIEW**: 旧版 4 行 stub，本次替换为 13 节全面深度审查

**审查标准**: `_shared/SKILL-SPEC.md` v1.0（12 项合规清单）+ SCORING.yaml 20 项测评标准 + `skill-dossier.md` 档案记录
**审查方式**: 目录内全部文件逐文件全文阅读；SKILL.md 与 SCORING.yaml / check.py 逐条交叉验证；关键正则与 YAML 解析做了实证运行（见附录 B）
**结论先行**: 综合得分 82/100，评级 🟡 B（可用但有小问题）。核心方法论（可解释启发式打分 + 双扫描方案 + 测试硬性要求 + 结构化 note-to-self）设计扎实、四阶段管道高度自洽，且是罕见的"零死引用"自包含技能；主要问题集中在三处：① 正文语法与列表格式粗糙（4 处拼写/断句缺陷，dossier 已记录）；② 测评侧 SCOPE-03 正则存在实证误伤——按该正则，agent 只要 Read 任意 .py 文件（本任务的核心动作）SCOPE-03 即判失败；③ PROC-05 脚本检查只认 AST 证据，与"Approach 1 或 Approach 2 皆可"的描述失配。

---

## 1. 目录全量清单

```
070-discover-important-function/
├── SKILL.md (403 行, 15 KB)  — 技能主体
├── SCORING.yaml (20 项 criteria + 3 项 critical_failures)
├── check.py (82 行)          — 7 项脚本检查入口
└── REVIEW.md (本次覆写)
```

极简 4 文件结构，无 `references/`、`scripts/`、`resources/`、`assets/` 子目录。技能运行时依赖仅为"能读文件、能跑命令"（SKILL.md:31-43），本体完全自包含——不引用任何外部文件，因此不存在 065/314 那类死引用问题，也没有可执行的附属脚本（与 301/302 的"脚本+测试+夹具"结构不同，本技能无脚本层可审查）。

`check.py` 与 `SCORING.yaml` 属测评基础设施（evaluation harness），非技能运行内容，但作为"技能与测评对接"的界面，本次一并做了交叉验证（见 §9、§10）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

`name: discover-important-function`。小写 + 连字符，25 字符，远小于 64 上限。目录名为 `070-discover-important-function`，符合 SKILL-SPEC §4 的 `NNN-kebab-case` 格式。

按语料惯例（name 不含 NNN 前缀，抽查 069-demand-received、071-don-norman-principles-audit、072-mobile-design 三个相邻技能均如此），本技能 name 判定合规，无需修改。

### 2.2 description

实测 352 字符（≤1024 ✓），单行 plain scalar，YAML 解析成功。逐项检查：

- **第三人称**：全文第三人称（"this skill observes..."、"it produces..."），无第一/第二人称开头，符合 §2.3。
- **触发信号**：第 3 句 "Use when the user asks to find the best functions to fuzz..." 命中规范要求的触发短语，符合 §2.4。
- **WHEN（触发场景）**：后半句给出 4 个具体场景——找 fuzz 目标函数、识别 parsers/decoders/validators、按测试覆盖决策、产出带 harness 指导的 shortlist。触发覆盖面好，且关键词密集（fuzz、parsers、decoders、validators、test coverage、fuzz targets、harness guidance），利于意图匹配。
- **WHAT（技能功能）**：前半句 "When given a project codebase, this skill observes the important functions in the codebase for future action" —— 是本 description 最弱的一环。"observes"（观察）用词不当，定位/排序任务的核心动词应为 identifies / locates / ranks / maps；"for future action" 语义含糊（什么 future action？）。好在后半句的触发场景部分实质上补充了 WHAT，整体信息量足够，只是首句措辞欠佳。详见 §13 🟡-10。
- **无跨技能路由**：无 "NOT for X, use Y instead" 句式，符合 §2.5。

### 2.3 可选字段与违禁字段

Frontmatter 仅 `name` + `description` 两个键。未声明任何可选字段（allowed-tools、argument-hint、user-invocable、model、paths、disable-model-invocation 均无），也无任何违禁键（metadata、license、tags、dependencies 等均无），完全合规。

可选字段缺位的实际影响很小：技能需要的工具（Read、Bash/Glob）是常见默认允许项，且技能不依赖任何第三方脚本，权限弹窗风险低于 301 那种需要 Bash 跑脚本的技能。

### 2.5 Frontmatter 小结

Frontmatter 整体合规。唯一打磨点是 description 首句 "observes...for future action" 的措辞（🟡-10），以及 description 与正文标题 "Fuzz Target Localizer" 之间的术语一致性（正文用 localize/rank，description 用 observe，建议统一）。

---

## 3. Body 逐段结构分析

### 3.1 总体结构

正文 403 行，远低于 600 行硬上限。结构为 6 个 H1 级章节：

```
# Fuzz Target Localizer            L6   — 目的/触发/输入/输出/护栏（58 行）
# Localize important files          L64  — 阶段一：文件定位（52 行）
# Localize important functions      L116 — 阶段二：函数定位（158 行，含双 Approach）
# Summarize existing unit tests     L274 — 阶段三：测试总结（50 行）
# Decide function under test...     L324 — 阶段四：FUT 决策（70 行）
# Final JSON block                  L394 — 输出契约（9 行）
```

结构问题：**6 个 H1 平级共存**。首节 "Fuzz Target Localizer" 下的 Purpose/When to use/Inputs/Outputs/Guardrails 是 H2，而后面四个工作流阶段却是 H1——标题层级跳跃（阶段章节逻辑上是首节内容的展开，应为 H2）。Markdown 渲染无碍，但层次语义混乱，见 §13 🟡-9。

### 3.2 Workflow / Process（必备项 ✅）

四阶段管道完整且衔接清晰：文件定位（树形建图 → 排除低价值区 → 启发式打分 → Top-N 排序）→ 函数定位（双 Approach 扫描 → 边界风险优先 → 测试早期介入 → 定向精读 → 排序）→ 测试总结（盘点 → 意图归纳 → 推断 oracles → 找缺口）→ FUT 决策（1-5 个 + 结构化 note）。每阶段均有 Goal / Procedure / Output format 三件套，可执行性强。

### 3.3 Output Format（必备项 ✅）

每阶段都有明确输出格式：文件级（path/score/rationale/indicators_hit，L105-112）、函数级（qualname/file/line_range/score/rationale/dependencies/harnessability，L180-190 与 L259-270 两版）、测试总结（test_map/inferred_oracles/gaps，L316-320）、FUT 决策（selected_futs + notes_to_self，L387-390），最后以 # Final JSON block（L394-402）收口为 5 键 JSON。输出契约在语料中属于最完备的一档。

### 3.4 Scope / Limitations（必备项 ⚠️ 内容存在但无独立标题）

- "Do not use this skill when"（L27-29）：3 条明确排除——修 bug、重构、立即实现 harness。真实的范围声明，非循环定义（对比 065 的 "The task is unrelated" 同义反复）。
- Guardrails（L53-60）：6 条护栏——分析优先、不改源码、默认只读、不臆断运行时行为、必须考虑现有测试、FUT 保持 1-5。
- 按 SKILL-SPEC §3.1 判"有 Scope 内容"，但标题不是 Scope/Limitations，规范未强制标题名，判通过带保留（§7 第 10 项）。

### 3.5 引用与路径规范

正文零文件引用——无 `references/`、无 `scripts/`、无跨技能路径、无 `../` 引用。唯一产物路径是仓库根 `APIs.txt`（L50）。符合 §3.3 精神，且规避了本语料最常见的"死引用"问题类别（对比 065 的 6 处无效引用、188/195/196 的缺失脚本）。这是本技能的重要亮点。

### 3.6 关键设计亮点

1. **可解释打分**：文件打分绑定 6 类具体指标（public API 暴露、输入边界关键词、格式处理器、原生边界、中心模块、测试邻近），函数候选同样给出 explainable rubric（输入面、边界风险、结构复杂度、测试覆盖、可 harness 性）——全程"可解释、可追溯"，与 SCORING PROC-03/PROC-06 的 LLM 判定口径一致。
2. **测试硬性要求**："## Hard requirement"（L280-287）把"检查并纳入现有测试"绑定到排名、FUT 选择、输入模型、种子语料四个环节，是语料中少见的显式硬约束写法。
3. **双 Approach 设计**：AST 头/文档串扫描（省 token）与全量精读（深分析）互为备选，配合"非随机挑选"的底线要求。
4. **note-to-self 模板**：9 个子节的 "Fuzzing Target Note" 模板（目标/原因/可调用契约/输入模型/oracles/harness 计划/风险旗标/下一步）是交付质量的关键保障，与 QA-01 检查口径逐字对应。

---

## 4. 逻辑一致性深度审查

### 4.1 Approach 1 与 Approach 2 之间无选择规则（dossier 已记录，最实质的逻辑缺口）

SKILL.md:122-190（Approach 1: AST 头/文档串扫描）与 SKILL.md:192-270（Approach 2: 全量阅读）是两个互斥的完整流程：不同的收集方式、不同的候选生成步骤、不同的输出格式（Approach 2 独有 `implementation_notes` 字段）。但正文**从头到尾没有给出"何时选哪个"的规则**——没有决策表、没有条件分支、没有默认推荐。Agent 读到两个平级方案时只能任意选择，而选择直接决定后续输出字段集合（L270 vs L180-190）。考虑到 Approach 1 的开篇目标写着 "minimizing full-body reading until needed"（L120），读者可推测 Approach 1 是默认，但正文未明说。修复见 §13 🟡-4。

### 4.2 JSON 契约漏掉 Approach 2 的 implementation_notes

Approach 2 的每函数输出必含 `implementation_notes`（L270），但 # Final JSON block 的 important_functions 字段（L399）只列 `{qualname, file, line_range, score, rationale, dependencies, harnessability}`，没有 implementation_notes。若 agent 按 Approach 2 执行，其"合格输出"在最终 JSON 里没有对应位置——文档自身两处规定冲突。修复见 §13 🟡-5。

### 4.3 Outputs 节的产物语义歧义（影响测评可达性）

L49-51 原文：

> A report in any format with the following information: - Localize important files - Localize important functions - Summarize existing unit tests - Decide function under test for fuzzing
> This file should be placed in the root of the repository as `APIs.txt`, which servers as the guidelines for future fuzzing harness implementation.

三重歧义：

1. **"any format" vs "APIs.txt" 矛盾**——既说任意格式的报告，又强制写成名为 APIs.txt 的特定文件；
2. **APIs.txt 内容未定义**——是报告全文，还是仅 API/目标清单？SCORING OUT-01 只查文件存在性，不查内容，agent 写什么都能过 OUT-01，但 agent 需要知道写什么；
3. **交付位置未约定**——SCORING OUT-03 与 QA-01 检查的是 **agent 的文本输出**（`output_contains` 读 `_agent_output`，见 `_shared/checker.py:339-343`），而 SKILL.md 只指示写 APIs.txt，未指示报告须同时出现在最终回复中。一个严格执行技能的 agent 完全可能只写文件、回复极简，导致 OUT-03/QA-01 落空。这是"技能内容 ↔ 测评机制"脱节的一处实证风险。修复见 §13 🔴-3 与 🟡-6。

### 4.4 四阶段管道内部一致性（亮点）

- 阶段一的 6 类打分指标（L92-100）→ 阶段二候选优先级（L148-156）→ SCORING PROC-03/PROC-06 的提问口径，三者逐条对应；
- 测试硬性要求（L280-287）→ 两个 Approach 中的"用测试提前细化"步骤（L157-163 / L242-248）→ PROC-08 脚本检查（conftest|pytest|_test.py|tests/），链路完整；
- "FUT 保持 1-5"（L60、L328）↔ PROC-10 的 "typically 1-5"；
- note 模板（L344-385）↔ PROC-11 的 7 要素 ↔ QA-01 的 "Fuzzing Target Note|qualname|File / location:"，逐字对应；
- Guardrails "不改源码"（L55-56）↔ SCOPE-03 ↔ CF-02，三方一致。

结论：除 4.1-4.3 三处外，技能内容与测评标准整体咬合度在语料中属于上乘。

### 4.5 小一致性瑕疵

- L131 "Do not read full function bodies during the initial pass unless needed" 与 Approach 1 步骤 4 "For the top candidates (typically 10-20), read the full function bodies"（L164-170）——"initial pass"与"top candidates 精读"之间未定义过渡条件（多少文件算 initial pass？何时切换？），仅靠上下文可推断，建议一句话明确；
- Inputs 说 "Ability to run local commands (optional but recommended)"（L37），但 Approach 1 依赖 Python `ast` 模块——若环境无 Python，Approach 1 不可执行而 Approach 2 可兜底；正文未说明这一依赖关系（恰好强化了 4.1 的"无选择规则"问题，Approach 2 在此场景是唯一可行解，却没有任何指引）。见 §13 🟢-11；
- L399 的 important_functions 字段与 PROC-07 的 LLM 提问（qualname/file/line_range/score/rationale/dependencies/harnessability）完全一致——PROC-07 反而没问 implementation_notes，所以 4.2 的字段缺口在测评侧不产生惩罚，属纯文档自洽问题。

---

## 5. 参考文件内容级审查

目录内无 `references/`、`resources/`、`scripts/` 子目录，正文零文件引用，技能 100% 自包含。因此本节的审查结论为：

- **无死引用**（目录中不存在却被正文引用的文件）：0 处。对比语料中 065（1 死文件）、188/195/196（引用缺失/路径错误）、314-316（共享模板残留）等高频问题，本技能完全免疫此类缺陷；
- **无内容委托**：全部领域知识（启发式指标、AST 用法、oracle 类型、note 模板）均在正文内，不存在"骨架 + 外推"的空壳模式（对比 045/317/320）；
- **无跨技能路径**：无 `../`、无 `skills/` 前缀路径（对比 026 的过时安装路径、301 的 `skills/...` 前缀）。

唯一的"文件系统交互"是产物写入 `APIs.txt`（L50）——路径为仓库根相对路径，与 SCORING OUT-01 的 `file_exists(workspace/APIs.txt)` 一致（实测匹配，见 §10）。

---

## 6. 语法与格式质量

### 6.1 拼写错误

- **L51 "which servers as the guidelines"** ——"servers" 应为 "serves"（dossier 已记录）。且后接 "as the guidelines" 单复数搭配欠佳（"serves as the guideline" 或 "serve as guidelines" 更顺），两处问题叠加。

### 6.2 残缺句与句式不一致

- **L25 "- Automating testing pipeline setup for a new or existing Python project."** ——动名词开头，与前四条 "Find/Identify/Decide/Produce" 命令式动词不一致，且是无主语的残缺句（dossier 已记录"末句为残缺句"）。拟修复句见 §13 🟡-7。
- **L44 "Produce result:"** ——残缺引导语，后接的是一整段描述而非冒号后的清单，读感生硬。

### 6.3 列表格式挤占单行

- **L49** "A report in any format with the following information: - Localize important files - Localize important functions - Summarize existing unit tests - Decide function under test for fuzzing" —— 4 个并列项全部挤在一行，Markdown 渲染为一段连续文本而非列表（dossier 已记录"连字符列表挤在一行"）。这是正文最显眼的排版破损。

### 6.4 Markdown 粗体与 dunder 名称冲突

- **L94 "Public API exposure: **init**.py re-exports, **all**, api modules"** ——原意显然是 `__init__.py` 与 `__all__`（双下划线），但写成了 `**init**`/`**all**` 形式，在 Markdown 中渲染为**粗体** "init"/"all" 而非代码样式。读者看到的是 "Public API exposure: init.py re-exports, all, api modules"——术语失真。修复见 §13 🟡-8。

### 6.5 标题层级

- 6 个 H1 平级（L6/L64/L116/L274/L324/L394），其中首节下还有 5 个 H2 子节——层级跳跃（见 §3.1）。同语料规范技能（如 301 的"一个 H1 + 十个 H2"）相比是明显风格瑕疵。

### 6.6 编码、YAML 与格式整洁度

- Frontmatter 与 SCORING.yaml 均实测 `yaml.safe_load` 解析成功，无语法错误；
- 全文件 UTF-8 无 BOM；行尾风格混合（SKILL.md 为 CRLF、SCORING.yaml 为 LF），Windows 环境属正常混合，不影响解析（实测通过）；
- 全正文与 SCORING.yaml **零 emoji**（grep 实测），符合人机感预期（见 §8）；
- 字段名术语统一：qualname / line_range / rationale / indicators_hit / harnessability / test_map / inferred_oracles / selected_futs / notes_to_self 在 SKILL.md 与 SCORING.yaml 中逐字一致，无枚举分叉（对比 301 的标签集合三版本问题）。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

1. ✅ **name 小写+连字符 ≤64 且匹配目录**：`discover-important-function` 25 字符；目录 `070-discover-important-function` 为 NNN-kebab 格式；按语料惯例 name 不含 NNN 前缀（抽查 069/071/072 验证）。
2. ✅ **description 第三人称、含 WHAT+WHEN+KEYWORDS、≤1024 字符**：352 字符；WHEN/KEYWORDS 充实，WHAT 措辞偏弱但信息存在（"observes the important functions"）。
3. ✅ **description 无命令式/第一/第二人称开头**：第三人称。
4. ✅ **description 无跨技能路由**。
5. ✅ **description 含至少一个触发信号**："Use when the user asks to" 命中。
6. ✅ **frontmatter 无违禁键**：仅 name + description。
7. ✅ **正文 ≤600 行**：403 行。
8. ✅ **正文含 Workflow/Process 章节**：四个阶段章节各含 Goal/Procedure。
9. ✅ **正文含 Output Format 章节**：各阶段 Output format 块 + Final JSON block。
10. ⚠️ **正文含 Scope/Limitations 章节**：内容存在（L27-29 三条排除 + L53-60 六条护栏），但无独立 "Scope"/"Limitations" 标题，规范未强制标题名，判通过带保留意见。
11. ✅ **正文无跨技能文件引用**：零文件引用，完全合规。
12. ✅ **目录 NNN-kebab-case、无空格无大写**。

结论：**12/12 通过**（第 10 项带保留意见）。规范遵从度在语料中属于第一梯队——这是本技能合规面最大的加分项。

---

## 8. 人机感评估

### 8.1 语言基调

全篇中性专业的技术指令语气，无 emoji、无填充语、无营销腔（对比 072 的 20+ emoji 与全大写喊话）。Guardrails 用 "Prefer analysis and reporting over code changes"、"Avoid assumptions about runtime behavior" 这类克制表述，符合 process 型技能惯例。

### 8.2 面向对象一致性

正文全部面向 agent 下指令（"Build a repository map"、"Score files using explainable heuristics"），未出现对用户说话的第二人称段落（对比 101/115-116 的"规则对用户说话"混淆）。唯一面向用户的内容是 "Do not use this skill when..." 的范围声明，属正常文体。

### 8.3 轻微机械感

- L44 "Produce result:" 是自动机风格的残缺引导语；
- L280 "## Hard requirement" 单独成节，与其余以动词开头的标题（Localize/Summarize/Decide）风格不统一，但语义清晰，不算问题。

### 8.4 人机边界

技能明示"Do not modify source code unless the user explicitly requests changes"（L55-56）与"Default to read-only analysis"（L58），与 SCORING SCOPE-03/CF-02 呼应，是安全边界设计良好的一侧。FUT 决策把"人类用户的测试意图"作为权重项（L342-343），符合"机器定位、人做裁决"的协作模型。

评分：9/10。全文无噪音，仅 "Produce result:" 一处机械感。

---

## 9. 可执行性评估

### 9.1 命令与工具可运行性

- 仓库建图：优先 `tree`（L41），回退递归列举（L43）——两条路径都有保障，与 PROC-01 脚本检查（`\btree\b|ls -R|find .*-type|**/*.py`）对应；
- 函数扫描：Approach 1 用 Python `ast`（L124-129），命令形式未给出具体示例（如 `python -c "import ast; ast.parse(...)"`），但步骤描述足以让 agent 自行构造；Approach 2 纯 Read，零命令依赖；
- **依赖注意**：Approach 1 需要 Python 环境，Inputs 却把"运行命令"标为 optional——若环境无 Python，Approach 1 不可执行，且正文无降级指引（见 §4.5）。这是可执行性上唯一需要补一句的地方。

### 9.2 流程量化程度

从 Top-N 文件（默认 10-30，L103）、精读候选（10-20，L165）、FUT 数量（1-5，L328）到 note 模板的 9 个子节（L344-385），所有环节都有明确的数量与结构约束，agent 无需自行发明格式。这是"可执行性"维度的最强项。

### 9.3 测评对接的三处硬伤（实证）

1. **SCOPE-03 正则误伤 Read .py**（SCORING.yaml:25-31 + check.py:37，实证见附录 B）：`tool_log_not_contains('(?i)("tool"\s*:\s*"Edit"|"file_path"\s*:\s*"[^"]*\.py")')` —— 第二个备选分支匹配**任意**工具调用中含 `"file_path": "...py"` 的 JSON 行。实测：一次普通的 `Read src/parser.py` 即命中 → SCOPE-03 判定失败。而阅读 .py 文件正是本任务的核心动作（Approach 2 几乎全程 Read .py，Approach 1 也要精读 top 候选），**按此正则，任何成功完成任务的 agent 都必然挂掉 SCOPE-03**。同时第一个分支 `"tool": "Edit"` 又不区分文件类型——Edit README.md 也算违规。该 criterion 的实际语义是"不得修改源码"，但正则无法表达。这是本次审查发现的测评侧最严重缺陷，修复见 §13 🔴-1。
2. **PROC-05 只认 AST 证据**（SCORING.yaml:65-71 + check.py:42）：描述明文 "uses AST-based header/docstring scan (approach 1) **or full-file read (approach 2)**"，但脚本检查 `tool_log_contains('(?i)(ast\.parse|import ast|ast\.walk|ast\.get_source_segment)')` 只认 AST。选择 Approach 2 的合规 agent 必然失败——描述允许的两条路径只有一条能过脚本检查。修复见 §13 🔴-2。
3. **输出位置契约缺失**（见 §4.3 第 3 点）：OUT-03/QA-01 检查 agent 文本输出，SKILL.md 只要求写 APIs.txt。修复见 §13 🔴-3。

### 9.4 check.py 代码质量

- `import _shared.checker` 实测成功（依赖存在），7 项脚本检查（SCOPE-03/PROC-01/PROC-05/PROC-08/OUT-01/OUT-03/QA-01）与 SCORING.yaml 的 ID 逐字一致，参数与 `_shared/checker.py` 函数签名匹配；
- 小瑕疵：check.py:26-31 用 try/except(OSError, ValueError) 包裹 `os.path.exists(agent_output)`——`os.path.exists` 只会在嵌入空字符时抛 ValueError，防御面定义模糊；且 main() 已把文件内容读入 agent_output，check() 内的路径判断分支在 runner 流程下几乎恒走 `set_agent_output` 分支，逻辑冗余但不影响正确性。见 §13 🟢-12。

### 9.5 脚本/测试层

本技能无附属脚本与测试文件，不存在脚本正确性风险（与 301/302 的脚本审查维度不同）。可执行性风险全部集中在"技能 ↔ 测评"接口（9.3）。

---

## 10. SCORING.yaml 交叉参考

### 10.1 结构完整性

20 项 criteria 逐项核对（实测解析）：category 分布为 scope 3 + process 11 + output 4 + negative 1 + qa 1 = 20，与 `total_items: 20` 一致；无重复 ID、无编号断层；3 项 critical_failures（CF-01 无报告归零 / CF-02 改源码归零 / CF-03 幻造 FUT 归零）全部对应正文的硬性约束。判定方式为 7 项 script + 13 项 llm。

### 10.2 逐项追溯表（20 项）

| ID | judge | 与 SKILL.md 对应 | 判定 |
|---|---|---|---|
| SCOPE-01 | llm | L27-29 "Do not use" 范围声明 | ✅ 一致 |
| SCOPE-02 | llm | 全程针对用户目标仓库的指令 | ✅ 一致 |
| SCOPE-03 | script | L55-56 不改源码护栏 | ❌ 正则失配（见 9.3-1） |
| PROC-01 | script | L41 tree/回退列举 | ✅ 一致 |
| PROC-02 | llm | L89-90 排除低价值区清单 | ✅ 一致 |
| PROC-03 | llm | L92-100 六类启发式指标 | ✅ 逐条对应 |
| PROC-04 | llm | L105-112 Top-N 输出格式 | ✅ 一致 |
| PROC-05 | script | L122/L192 双 Approach | ❌ 只认 AST（见 9.3-2） |
| PROC-06 | llm | L148-156/L222-229 边界风险优先 | ✅ 一致 |
| PROC-07 | llm | L180-190/L259-270 函数输出格式 | ✅ 一致（含 4.2 的文档侧字段缺口） |
| PROC-08 | script | L280-287 测试硬性要求 | ✅ 一致 |
| PROC-09 | llm | L316-320 test_map/inferred_oracles/gaps | ✅ 一致 |
| PROC-10 | llm | L328 "typically 1-5"+判据 | ✅ 一致 |
| PROC-11 | llm | L344-385 note 模板 7 要素 | ✅ 一致 |
| OUT-01 | script | L50 APIs.txt 仓库根 | ✅ 一致（实测 glob 命中） |
| OUT-02 | llm | 报告含文件+函数双排名 | ✅ 一致 |
| OUT-03 | script | L394-402 JSON 5 键 | ⚠️ 检查 agent 文本输出，交付位置未约定（见 9.3-3） |
| OUT-04 | llm | L316-320 测试总结 | ✅ 一致 |
| NEG-01 | llm | L242-248/L342 测试覆盖纳入 FUT 选择 | ✅ 一致 |
| QA-01 | script | L348/L352 "Fuzzing Target Note"/"File / location:" | ⚠️ 同 OUT-03 的输出位置风险 |

结论：**18/20 与技能内容精确咬合**（语料中罕见的追溯完整性），2 项因正则设计失配（SCOPE-03、PROC-05），2 项受"输出位置契约"影响的连带风险（OUT-03、QA-01）。

### 10.3 值得肯定的设计

- SCOPE-01 的 LLM 问题没有问"是否做了任务"，而是问"是否把任务框定为 fuzz 目标定位而非修 bug/重构"——直击 skill 的核心边界；
- PROC-08 把"测试检查"做成硬性脚本检查（conftest/pytest/_test.py/tests/ 任一命中），与 SKILL.md 的 "Hard requirement" 措辞形成双保险；
- CF-03（从别的代码库选 FUT 或幻造函数归零）直接锚定正文"分析用户目标仓库"的指令，防幻觉设计到位。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md（位于 `~/.claude/projects/C--Users-f50058303/memory/skill-dossier.md`）对 070 的档案记录：

> **逻辑**: 文件定位→函数定位→测试总结→FUT 决策流程连贯，但 Approach 1（AST 扫描）与 Approach 2（全量阅读）之间未给出选择规则。
> **语法**: 明显瑕疵——"which servers as the guidelines"（应为 serves）、连字符列表挤在一行、末句 "Automating testing pipeline setup..." 为残缺句子。
> **人机感**: 中性专业，无 emoji。
> **合规**: Description 第三人称，有 Procedure/Output 结构，正文 403 行 ≤600。
> **总评**: 🟡 方法论扎实，但拼写、断句与列表格式多处粗糙需校对。

Dossier 评级: 🟡。

### 本次审查的增量发现（dossier 未记录）

1. **SCOPE-03 正则实证误伤**（SCORING.yaml:31 / check.py:37）——Read 任意 .py 即判失败，成功完成任务必挂（dossier 未涉及 SCORING 层）
2. **PROC-05 与描述失配**（SCORING.yaml:71 / check.py:42）——描述允许 Approach 2，脚本只认 AST（dossier 未涉及 SCORING 层）
3. **输出位置契约缺失**——OUT-03/QA-01 检查 agent 文本输出，SKILL.md 只指示写 APIs.txt（dossier 未涉及）
4. **`**init**`/`**all**` Markdown 粗体渲染错误**（SKILL.md:94）——`__init__.py`/`__all__` 术语失真（dossier 未记录）
5. **6 个 H1 平级导致标题层级跳跃**（SKILL.md:L6/L64/L116/L274/L324/L394）（dossier 未记录）
6. **description 首句 "observes...for future action" 措辞含糊**（dossier 记为合规，未点评措辞质量）
7. **JSON 契约漏 implementation_notes**（SKILL.md:270 vs 399）（dossier 未记录）

结论：dossier 的 🟡 评级方向正确，且其记录的三处语法问题（servers、列表挤行、残缺句）经复核全部属实。增量发现集中在测评对接层（第 1-3 条，其中第 1 条为严重设计缺陷）与格式细节（第 4-7 条）。无 🔴/🟠 级内容问题，技能方法论本身扎实。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 权重 | 得分 | 说明 |
|------|:----:|:----:|------|
| Frontmatter 合规 | 10% | 9.0 | description 352 字符全合规，仅 "observes" 措辞欠佳 |
| Body 结构完整 | 10% | 8.5 | 四阶段+输出契约+JSON 齐全；多 H1 层级瑕疵 |
| 逻辑一致性 | 20% | 7.0 | 管道自洽；Approach 选择规则缺失、JSON 漏字段、APIs.txt 语义歧义 |
| 参考完整性 | 10% | 10.0 | 零引用零死链，100% 自包含 |
| 语法格式 | 10% | 6.5 | servers/serves、残缺句、列表挤行、`**init**` 渲染错误 4 处 |
| 规范合规 | 15% | 9.5 | 12/12 通过（Scope 项带保留意见） |
| 人机感 | 10% | 9.0 | 中性专业零 emoji；"Produce result:" 略机械 |
| 可执行性与测评对接 | 15% | 7.0 | 流程高度量化可执行；SCOPE-03/PROC-05/输出位置三处对接硬伤 |
| **加权总分** | | **8.175/10** | |

加权计算：9.0×0.10 + 8.5×0.10 + 7.0×0.20 + 10.0×0.10 + 6.5×0.10 + 9.5×0.15 + 9.0×0.10 + 7.0×0.15 = 0.90 + 0.85 + 1.40 + 1.00 + 0.65 + 1.425 + 0.90 + 1.05 = **8.175 → 82/100**。

### 12.2 评级

🟡 **B** (82/100) — 可用但有小问题（与 dossier 评级一致）。三大加分项：规范 12/12 全过、四阶段方法论与 20 项测评标准 18/20 精确咬合、零死引用完全自包含。三大扣分项：正文 4 处语法/格式粗糙（纯校对工作）、测评侧 SCOPE-03 正则误伤（影响 criterion 有效性，需修复而非技能改写）、PROC-05 检查与描述失配。

修复后预期：完成 §13 的 🔴-1/2/3 三处对接修复 + 🟡-4/5/6/7/8 五处文档修复后，预计可达 **A-（88+）**。

---

## 13. 修复建议（按优先级分层）

### 🔴 高优先级（影响测评有效性或核心语义，工作量均为 S）

**R-1: 修复 SCOPE-03 正则误伤（测评侧，本次审查最重要发现）**

- 位置: `SCORING.yaml:31`（pattern）+ `check.py:37`（同 pattern）
- 当前正则:
  ```
  (?i)("tool"\s*:\s*"Edit"|"file_path"\s*:\s*"[^"]*\.py")
  ```
- 实测问题（附录 B 第 2 项）:
  1. 第二个备选分支 `"file_path"\s*:\s*"[^"]*\.py"` 不限定工具类型——`Read` 调用 `src/parser.py` 即命中，而读 .py 是本任务的核心动作，**任何成功完成任务的 agent 必然触发 SCOPE-03 失败**；
  2. 第一个分支 `"tool": "Edit"` 不限定文件类型——编辑 README.md 等非源码文件也被判违规，与 criterion 语义（"不修改源代码"）不符。
- 修复方案（推荐 A）: 限定为"对 .py 文件的写操作"，即要求同一工具调用内同时出现 Edit/Write 与 .py 路径:
  ```
  (?i)("tool"\s*:\s*"(Edit|Write)"[^}]*"file_path"\s*:\s*"[^"]*\.py")
  ```
  （`[^}]*` 限定在同一 args 块内；`\s` 类含换行符，缩进 JSON 亦可命中）
- 修复方案（备选 B）: 若不想改正则，把该 criterion 改为 `judge: llm`，由 LLM 依据 tool log 判定"是否修改了源码"。
- 不修复的后果: SCOPE-03 在语料实测中恒失败（或恒受 Read 次数支配），该 criterion 失去区分度，且会造成"越认真分析、越容易误挂"的测评失真。

**R-2: PROC-05 检查与双 Approach 描述对齐（测评侧）**

- 位置: `SCORING.yaml:65-71`（description 允许 approach 1 **或** approach 2）+ `check.py:42`
- 当前检查: `tool_log_contains('(?i)(ast\.parse|import ast|ast\.walk|ast\.get_source_segment)')` —— 只认 AST 证据
- 问题: 按 SKILL.md:192 选择 Approach 2（全量阅读）的合规 agent 没有任何 ast 调用，PROC-05 必失败；而 PROC-05 的 description 明文允许两种方式。
- 修复方案（推荐 A，改动最小）: pattern 增加 Approach 2 的证据分支:
  ```
  (?i)(ast\.parse|import ast|ast\.walk|ast\.get_source_segment|"tool"\s*:\s*"Read"[^}]*"file_path"\s*:\s*"[^"]*\.py")
  ```
  （Approach 2 的合规 agent 必然大量 Read .py；Approach 1 精读 top 候选时也常命中，双分支覆盖两种路径）
- 修复方案（备选 B，语义更准）: 改为 `judge: llm`，提问改为"函数发现是否基于系统性的 AST 扫描或全量文件阅读，而非随机挑选"——与 description 的 "not a random pick" 底线逐字对齐。
- 不修复的后果: 选择 Approach 2 的 agent 被系统性扣分，测评结果偏向 Approach 1，无法反映技能设计的双路径意图。

**R-3: 补输出位置契约（SKILL.md + 连带 OUT-03/QA-01 可达性）**

- 位置: `SKILL.md:46-51`（## Outputs 节）
- 问题: OUT-03/QA-01 检查的是 agent 文本输出（`_shared/checker.py:339-343` 的 `_agent_output`），而 SKILL.md 只指示"把报告写入仓库根 APIs.txt"。严格执行技能的 agent 若只在回复里给一句"已写入 APIs.txt"，OUT-03 与 QA-01 将同时落空。
- 修复: 在 Outputs 节补一句双位置交付要求，例如:
  > Produce the full report in your final response, including the final JSON block, and write the same content to the repository root as `APIs.txt` (serves as the guideline for future fuzzing harness implementation).
  - 同时把 # Final JSON block（L394）改为明确"JSON 块位于最终回复末尾（以及 APIs.txt 内）"，消除 4.3 的"报告放哪"歧义。
- 不修复的后果: 每次运行的 OUT-03/QA-01 结果取决于 agent 的回复习惯而非技能遵循度，测评分不可复现。

### 🟡 中优先级（一致性与可读性，工作量均为 S）

**Y-4: 补充 Approach 1 / Approach 2 的选择规则（对应 dossier 记录的逻辑缺口）**

- 位置: `SKILL.md:116-120`（# Localize important functions 引言处）
- 建议新增决策表:
  | 条件 | 选择 |
  |---|---|
  | 仓库大（文件多 / token 预算紧张） | Approach 1（AST 头/文档串扫描） |
  | 重要文件数量少且需实现细节支撑打分 | Approach 2（全量阅读） |
  | 环境无 Python（无法运行 ast） | Approach 2 |
  | 默认 | Approach 1（与 L120 "minimizing full-body reading" 目标一致） |
- 不修复的后果: agent 的选择无依据，且 Approach 2 的额外字段（implementation_notes）是否产出完全随机。

**Y-5: Final JSON block 补齐 implementation_notes 字段**

- 位置: `SKILL.md:399`（important_functions 字段）
- 修复: 改为 `important_functions: [{qualname, file, line_range, score, rationale, dependencies, harnessability, implementation_notes}]`，并注明 "implementation_notes required when Approach 2 is used"。
- 不修复的后果: 4.2 节的文档自洽缺口——按 Approach 2 执行时"合格输出"无对应 JSON 位置。

**Y-6: 澄清 APIs.txt 内容与 "any format" 的矛盾**

- 位置: `SKILL.md:49-51`
- 修复: 明确 APIs.txt 内容 = 报告全文（含 JSON 块），删除 "in any format" 或改写为 "Produce the report (format flexible) as `APIs.txt` in the repository root..."，并补一句 APIs.txt 的用途（"as the guideline for future fuzzing harness implementation"——顺手修正 servers 拼写，见 Y-7）。
- 不修复的后果: agent 可能写"任意格式"文件或不写内容，OUT-01 只查存在性掩盖内容缺失，误导下游 harness 实现。

**Y-7: 修复正文 4 处语法/格式缺陷（对应 dossier 记录的语法问题）**

- 位置与修复:
  1. `SKILL.md:51` "which servers as the guidelines" → "which serves as the guideline"（或 "serve as guidelines"）；
  2. `SKILL.md:25` "- Automating testing pipeline setup for a new or existing Python project." → "- Automate testing pipeline setup for a new or existing Python project."（与前四条命令式动词 Find/Identify/Decide/Produce 对齐，消除残缺句）；
  3. `SKILL.md:49` 将行内 "- Localize important files - Localize important functions..." 改写为真正的换行列表:
     ```
     A report with the following information:
     - Localize important files
     - Localize important functions
     - Summarize existing unit tests
     - Decide function under test for fuzzing
     ```
  4. `SKILL.md:44` "Produce result:" → 删除冒号或改写为 "## Output" 风格标题。
- 不修复的后果: 三个 dossier 已记录的拼写/断句问题继续存在，且 6.3 的列表挤行在 Markdown 渲染下持续失真。

**Y-8: 修复 `**init**`/`**all**` 粗体渲染错误**

- 位置: `SKILL.md:94`
- 当前: "Public API exposure: **init**.py re-exports, **all**, api modules"
- 修复: "Public API exposure: `__init__.py` re-exports, `__all__`, api modules"（反引号代码样式替代粗体，双下划线还原）。
- 不修复的后果: 渲染为 "init.py re-exports, all"——术语失真会误导 agent 的指标理解（public API 暴露判定是 PROC-03 的检查点之一）。

**Y-9: 统一标题层级为单一 H1**

- 位置: `SKILL.md:64/116/274/324/394`（五个工作流阶段 H1）
- 修复: 全部降为 `##`，使 `# Fuzz Target Localizer` 成为唯一 H1；各阶段的 `## Goal/## Procedure/## Output format` 相应降为 `###`。或反向操作：首节升格逻辑改为 `##`，与其余章节平级——二选一，保持一致即可。
- 不修复的后果: 6 个 H1 平级 + 首节 H2 混用，标题层级语义混乱（§3.1/§6.5）。

**Y-10: description 首句措辞打磨**

- 位置: `SKILL.md:3`
- 当前: "When given a project codebase, this skill observes the important functions in the codebase for future action."
- 修复: "When given a project codebase, this skill identifies and ranks the most important functions as candidate fuzz targets."（动词 identifies/ranks 与正文 Localize/Rank 术语统一，消除 "for future action" 的含糊）。
- 不修复的后果: 触发匹配时 WHAT 信号偏弱，且与正文术语不一致。

### 🟢 低优先级（打磨项）

**G-11: 注明 Approach 1 的 Python 依赖与降级路径**

- 位置: `SKILL.md:31-43`（## Inputs expected from the environment）
- 修复: 在 Inputs 或 Approach 1 开头补一句 "Approach 1 requires a Python interpreter for `ast`; if unavailable, fall back to Approach 2."——顺带部分弥补 4.1 的选择规则缺口。
- 工作量: XS。

**G-12: check.py 冗余防御清理**

- 位置: `check.py:26-31`
- 修复: 删除 try/except(OSError, ValueError) 包装与 `_is_path` 分支判断（main() 已把文件内容读入 agent_output，check() 内直接 `set_agent_output(agent_output)` 即可），或统一由调用方传内容。
- 工作量: XS。

**G-13: note 模板与 JSON 块的字段对齐声明**

- 位置: `SKILL.md:344-390` 与 `SKILL.md:394-402`
- 修复: 在 Final JSON block 补一句 "notes_to_self entries follow the Fuzzing Target Note template above"——目前两处各自成文，靠读者自行关联（QA-01 已通过模板标记词兜底，属锦上添花）。
- 工作量: XS。

**G-14: 阶段一 → 阶段二的过渡条件一句话说明**

- 位置: `SKILL.md:131`（"Do not read full function bodies during the initial pass unless needed"）
- 修复: 补 "The initial pass covers the Top-N files from the previous stage; switch to targeted reading for the top 10-20 candidates."，消除 4.5 的过渡歧义。
- 工作量: XS。

### 修复建议小结

| 层级 | 数量 | 性质 |
|------|:----:|------|
| 🔴 高优先级 | 3 | 2 项测评侧正则/检查修复（SCOPE-03、PROC-05）+ 1 项输出位置契约（SKILL.md） |
| 🟡 中优先级 | 7 | 1 项逻辑缺口（Approach 选择规则）+ 1 项文档自洽（JSON 字段）+ 5 项语法/格式/层级 |
| 🟢 低优先级 | 4 | 4 项打磨 |

全部 14 项中无一项触及方法论本身——技能的四阶段管道、双 Approach 设计、测试硬性要求、note 模板均无需改动，这正是其被评为 🟡 而非 🟠 的原因：问题全部集中在"文面校对"与"测评对接"两层，修复成本低、修复后可达 A-。

---

## 附录

### 附录 A：文件清单与规模

SKILL.md 403 行（15 KB）；SCORING.yaml 20 项 criteria + 3 项 critical_failures；check.py 82 行。合计约 490 行（不含共享库）。无 references/scripts/resources 子目录。

### 附录 B：本次审查执行验证

1. **YAML 解析**：SKILL.md frontmatter 与 SCORING.yaml 均 `yaml.safe_load` 成功；SCORING 20 项 criteria 分类计数（scope 3 / process 11 / output 4 / negative 1 / qa 1）与 `total_items: 20` 一致；3 项 CF 齐全。
2. **SCOPE-03 正则实测**（本次审查关键证据）：构造标准 JSONL 工具日志行逐一匹配——
   | 日志行 | 匹配结果 | 说明 |
   |---|---|---|
   | `{"tool": "Read", "args": {"file_path": "src/parser.py"}}` | **True（误伤）** | 核心任务动作被判违规 |
   | `{"tool": "Read", "args": {"file_path": "README.md"}}` | False | 正常 |
   | `{"tool": "Edit", "args": {"file_path": "README.md"}}` | True（误伤） | 非源码编辑被判违规 |
   | `{"tool": "Bash", "args": {"command": "tree src"}}` | False | 正常 |
   | `{"tool": "Glob", "args": {"pattern": "**/*.py"}}` | False | 正常 |
   确认 9.3-1 的结论：SCOPE-03 在成功完成任务的前提下必然失败。
3. **PROC-01/PROC-05/PROC-08 正则实测**：Bash `tree` 与 Glob `**/*.py` 命中 PROC-01；Bash 含 `import ast` 命中 PROC-05；含 tests/ 路径的日志命中 PROC-08——三个检查在正常流程下可过，仅 PROC-05 在 Approach 2 场景不可过（9.3-2）。
4. **check.py 导入**：`import _shared.checker` 链路实测成功，模块加载无语法错误。
5. **description 实测**：352 字符（≤1024），单行 YAML 字符串。
6. **emoji 扫描**：SKILL.md 与 SCORING.yaml 全零 emoji（Unicode 范围正则）。
7. **语料惯例抽查**：069/071/072 三个相邻技能的 name 均不含 NNN 前缀，确认本技能 name 判定合规。

### 附录 C：术语对照

FUT = Function Under Test（被测函数，fuzz 目标）；AST = Abstract Syntax Tree（抽象语法树，Approach 1 的扫描手段）；Top-N = 排名前 N 的文件清单（默认 10-30）；harnessability = 可 harness 性（低/中/高三档）；oracle = 测试预言（round-trip 属性、幂等性、无崩溃等）；note to self = 面向后续实现的结构化备忘（Fuzzing Target Note 模板）；APIs.txt = 仓库根目录的定位报告产物。
