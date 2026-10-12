# REVIEW: 229-exam-forecast

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 法学生期末考情预测（past-exam 模式分析 → 权重预测）
**Body 行数**: 160 行（SKILL.md）
**参考文件数**: 0（无 references/ 目录，完全自包含于 SKILL.md）
**已有 REVIEW**: 否（本目录此前无 REVIEW.md，本次为初始审查）

---

## 1. 目录全量清单

```
229-exam-forecast/
├── SKILL.md     (160 行, 9,350 字节)
├── SCORING.yaml (143 行, 6,928 字节)
└── check.py     (69 行, 2,161 字节)
```

- 无 `references/` 子目录、无 `scripts/` 子目录 —— 结构极简。
- 审查上下文文件（非本 skill 文件，但影响结论）：
  - `../_shared/checker.py` (351 行) — check.py 依赖的共享检查函数库
  - `../_shared/SKILL-SPEC.md` — SKILL.md 规范 v1.0（合规性对照基准）
  - `../_shared/CHECKER-LIBRARY.md` — checker 函数库文档
  - 用户记忆 `skill-dossier.md` — 语料库逐项质量档案（229 相关条目）

---

## 2. Frontmatter 逐字段审查

### 2.1 name

`exam-forecast` — 全小写 + 连字符，长度 13 ≤ 64，与目录名 `229-exam-forecast` 匹配（NNN- 前缀分离）✅

### 2.2 description（逐句分析）

> Analyze past exams from the same professor to surface patterns — subject weighting, recurring issue-spot traps, favored hypo types, policy-vs-doctrine mix — and forecast likely emphases for the upcoming exam. Use when the user says "what's on the exam", "analyze past exams", "predict the exam", or shares past exams.

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 第三人称 | ✅ | 无 imperative / first-person / second-person 开头 |
| WHAT 具体性 | ✅ | 列举 4 类可提取模式（subject weighting / issue-spot traps / favored hypo types / policy-vs-doctrine mix）+ 1 个产出（forecast likely emphases），比"分析过往试卷"具体得多 |
| WHEN 触发场景 | ✅ | 3 个用户口语触发短语（"what's on the exam" / "analyze past exams" / "predict the exam"）+ 1 个行为触发（"shares past exams"） |
| KEYWORDS | ✅ | past exams, professor, weighting, hypo, policy-vs-doctrine, exam |
| 长度 | ✅ | ~340 字符 ≤ 1024 |
| 触发信号短语 | ✅ | 含 "Use when the user..." |
| 跨 skill 路由 | ✅ | 描述内无 "NOT for X" 式路由（负向路由在 body Integration 节，合规） |
| 与 body 一致性 | ✅ | "same professor" 与 Load context 的教授匹配逻辑一致 |

**评价**：描述质量优秀，属语料库上乘水平。触发短语覆盖意图表达与行为表达两类；"shares past exams" 行为触发使上传试卷即自动触发，符合该 skill 的实际使用路径。

**注意点**（非缺陷）：描述未提及 fallback 行为（无试卷时退化为 syllabus 概述），对触发判断略保守——若用户只说"我的宪法学考试会考什么"且未提供试卷，agent 可能先触发本 skill 再被 SCOPE-02/CF-01 约束，触发-降级链是正确的，但描述若能写"或仅询问考试内容（将回退为 syllabus 概述）"会更完整。

### 2.3 argument-hint

`[class name, with past exams shared or paths to them]`

- 属 SKILL-SPEC §1.2 允许字段 ✅
- 与 body 指令一致：参数是课程名 + 试卷（路径或内容），不要求教授名（body 明确"Don't ask the user to type in the professor's name"）✅
- 格式上不是严格 CLI 参数，而是上下文提示 —— 对 agent 触发型 skill 合理。

### 2.4 其他 frontmatter 字段

仅 name / description / argument-hint 三个字段，全部在允许列表内。未使用 allowed-tools / model / paths / user-invocable —— 不违规（这些是可选字段）。无任何 forbidden 字段（metadata, triggers, tags 等）✅

### 2.5 Frontmatter 语法

- 描述内含引号（"what's on the exam"）与 em dash（—），YAML 用双引号包裹整串 —— 引号嵌套正确，无解析风险 ✅
- `argument-hint` 含逗号与方括号，双引号包裹 ✅
- 三个字段均可被 YAML 安全解析（对照同类 skill 验证）

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
L6    # Exam Forecast                       （标题）
L8-14  快速开始：编号步骤 1-7                 （load 配置 → 套用工作流 → 摄入试卷 → 逐卷分析 → 跨卷分析 → 结合 syllabus → 写文件）
L18-22 ## Purpose                            （"Every professor's exam has fingerprints" + "Not magic" 双重定调）
L24-29 ## Confidence discipline              （置信度纪律：UNCERTAIN 默认、thin sample 声明、新教授降级）
L31-37 ## Load context                       （外部配置 + 用户材料 + 教授名匹配原则）
L39-140 ## Workflow
        L41-50   Step 1: Intake              （5 个摄入问题 + <3 卷警告 + 跨课程警告）
        L52-62   Step 2: Read each past exam （6 维分析清单）
        L64-80   Step 3: Cross-exam pattern analysis（stable / variable / absent 三分法）
        L82-136  Step 4: Forecast            （header 要求 + 完整输出模板 L92-136）
        L138-140 Step 5: Output location     （写入路径 + 版本化说明）
L142-147 ## Integration                      （outline-builder / flashcards / bar-prep-questions / irac-practice 引用）
L149-151 ## Close with the next-steps decision tree（收尾决策树，引用外部 CLAUDE.md ## Outputs 约定）
L153-159 ## What this skill does not do      （5 条负面清单）
```

### 3.2 必需章节检查（SKILL-SPEC §3.1）

| 必需节 | 位置 | 判定 |
|--------|------|:----:|
| Workflow / Process | L39-140，5 步递进（intake → per-exam → cross-exam → forecast → output） | ✅ 完整 |
| Output Format | 无独立 `## Output` 节；输出规范以"Step 4 内嵌模板"形式存在（header + 元信息块 + 5 个子节 + 表格） | ⚠️ 部分满足 |
| Scope / Limitations | L153-159 `## What this skill does not do`，5 条（不预测具体题 / 无试卷不工作 / 不替代全面复习 / 不感知未知变化 / 1-2 卷不可靠） | ✅ 完整 |

**判定说明**：Output Format 以"模板即规范"方式嵌入 Step 4，内容完整（可执行性甚至优于独立节），但与 SKILL-SPEC 建议的独立 Output 节结构不同。dossier 记为"三节齐全"可辩护，本节记为 ⚠️ 结构偏差。

### 3.3 结构特点

1. **双轨结构**：顶部 7 步快速索引（L8-14）+ 详细 5 步工作流（L39-140）。信息完全一致（索引是详节的浓缩），但编号体系不同（1-7 vs Step 1-5），读者需做映射。轻微冗余。
2. **模板优先**：Step 4 给出可原样复制的 markdown 模板（含表头、占位符 `[N]`、示例值），可执行性极强。
3. **护栏密度高**：Confidence discipline + What it does not do 双重负向约束，属全语料库较高水平。

---

## 4. 逻辑一致性深度审查

### C-1 顶部索引 vs 详细步骤：映射完整 ✅
顶部 1-7 与 Step 1-5 + 写文件一一对应：load→workflow→intake→analyze→cross-exam→combine+syllabus→write。内容无矛盾，仅编号体系双轨（见 §3.3）。

### C-2 置信度阈值一致 ✅
- 模板 `**Sample confidence:** [thin (<3) / moderate (3-5) / strong (6+)]`（L98）
- Step 1 `If fewer than 3 past exams: flag as thin sample`（L49）
- Confidence discipline `If only 1-2 past exams are available, say so explicitly`（L28）
三处阈值完全一致（1-2 卷 → thin，3-5 → moderate，6+ → strong）。✅

### C-3 header 三重定义一致（但冗余）⚠️
header 在文件中出现三处定义/实例：
- L84-88：文字要求 + 单独 code fence 示例
- L92-94：完整模板内第一行
- L98（间接）：SCORING OUT-01 正则
三处文本一致（"STUDY NOTES — NOT LEGAL ADVICE"，em dash 统一）✅。但同一常量定义三次是漂移风险——任一处被编辑而其他未同步，CON 判定即失真。

### C-4 教授名处理逻辑自洽 ✅
- Load context（L37）：从材料提取教授名，不询问用户
- Step 1（L43）：只问 "Which class are we forecasting for?"，不问教授名
- SCORING CON-03：与上述一致
问课程不问教授名，逻辑闭环，无冲突。✅

### C-5 输出路径一致 ✅
顶部 L14、Step 5 L140、SCORING OUT-03 正则三者路径片段一致（exam-forecasts/[class]/forecast-YYYY-MM-DD.md）。✅

### C-6 "## [UNCERTAIN — framing]" 标题歧义 🔴（重要）
模板 L133：`## [UNCERTAIN — framing]`。
- 方括号在 markdown 中同时是元注释/标注惯用写法。agent 可能：(a) 将整节视为"标注说明"而省略（CON-01 判定依赖该节的 [UNCERTAIN] 显式框架，省略即扣分）；(b) 保留方括号作为字面标题，格式生硬。
- 且该节内容（L135"基于 N 份试卷…教授会轮换…"）实际上与 Confidence discipline 的措辞重复，作为独立标题节的必要性存疑——建议改为正文中的 `> [UNCERTAIN]` 引用块，或改为明确标题 `## Uncertainty framing`。

### C-7 外部依赖三处悬空 🔴（重要）
- L8：Step 1 硬读 `~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md`
- L84：header 要求的依据是 "Per plugin config `## Outputs`"
- L151：next-steps decision tree 的依据是 "per CLAUDE.md `## Outputs`"，且默认五分支（draft the X, escalate, get more facts, watch and wait, something else）只在文字中出现，未给出任何格式/判据
问题：三处均依赖一个**非本 skill 文件**，而该文件不在 skill 目录内、不属于语料库、隔离测评环境中几乎必然不存在。SKILL.md 未定义文件缺失时的降级行为（Step 1 若读不到 CLAUDE.md 怎么办？决策树五分支若不可见怎么"customize"？）。这是本 skill 最大的自包含性缺口。

### C-8 集成节死引用 🔴（重要）
L144-147 引用 4 个 skill：outline-builder / flashcards / bar-prep-questions / irac-practice。经 grep 语料库（complex-skills/ 全部 322 个目录），**只有 164-irac-practice 存在**；outline-builder、flashcards、bar-prep-questions 均不存在。3 个引用是死路由。SKILL-SPEC §3.3 允许"按名引用另一 skill"，但引用的对象应真实存在，否则 agent 可能尝试调用不存在的 skill。

### C-9 "re-run and append" 措辞与机制不符 🟡
L140："Versioned — if the student gets another past exam mid-semester, re-run and append."
文件名按 `forecast-[YYYY-MM-DD].md` 版本化——不同日期产生不同文件，不存在"追加"目标。"append" 与"版本化"两个机制概念冲突：追加到旧文件会破坏版本化，生成新文件则不是 append。应明确为"re-run 生成新日期的文件"。

### C-10 样本置信度与模板 Caveats 互补 ✅
模板 Caveats 示例（"one of the past exams was an open-book final; your upcoming is closed-book. Pattern transfer is partial."）与 Step 1 的格式变体识别（L46）呼应，机制闭环。

### C-11 分析与测评追踪性 ✅
Step 2 的 6 维清单（format / subject coverage / question style / fact-pattern density / recurring traps / policy-vs-doctrine ratio）与 SCORING PROC-02 描述逐字对应；Step 3 三分法与 PROC-03 对应。SKILL.md → SCORING.yaml 追踪链清晰，属语料库规范做法。

### C-12 缺失路径：PDF 解析失败 🟡
Step 2 未定义 PDF 不可读（扫描件无 OCR、损坏文件）时的降级路径。输入形态声明了"PDF, paste, or paths"（L10），但无"解析失败 → 请用户粘贴文本"的指令。属小缺口。

### C-13 header 在文件内位置一致 ✅
模板内 header（L93）在文件标题（L95）之前，满足"first line of the saved file"（L84）。chat 内 header 同理。无内部矛盾。

---

## 5. SCORING.yaml 内容级审查

> 本 skill 无 references/ 参考文件，本节承接"参考文件内容级审查"职能，对测评文件做逐项内容审查。

### 5.1 总体结构

- `total_items: 15`，实际 criteria 15 条：scope 2 + process 6（CON-01~03 归入 process 类别）+ output 4 + negative 2 —— 与声明数一致 ✅
- `pattern: process` 与 SKILL.md 的 process 型定位一致 ✅
- critical_failures 3 条 ✅

### 5.2 逐项对照表

| id | 类别 | judge | 对应 SKILL.md | 合理性 |
|----|------|:----:|--------------|:------:|
| SCOPE-01 | scope | llm | description 触发短语 | ✅ |
| SCOPE-02 | scope | llm | "What this skill does not do" 第 2 条 + L29 | ✅ 与 CF-01 强重叠（双保险，可接受） |
| CON-01 | process | llm | Confidence discipline L26-27 + 模板 L133-135 | ✅ |
| CON-02 | process | llm | Step 1 L49 + L28 | ✅ |
| CON-03 | process | llm | Load context L37 | ✅ |
| PROC-01 | process | llm | Step 1 L43-47 | ⚠️ 4 项合一（class/数量/同课程/格式变体），全或无 |
| PROC-02 | process | llm | Step 2 L56-62 | ⚠️ 6 项合一，全或无 |
| PROC-03 | process | llm | Step 3 L68-80 | ✅ |
| PROC-04 | process | llm | Step 4 L90-91 | ✅ |
| OUT-01 | output | script | L84-88, L93 | ⚠️ 描述-实现 gap（见 5.3） |
| OUT-02 | output | llm | 模板 5 组件 | ⚠️ 5 项合一 |
| OUT-03 | output | script | Step 5 L140 | ⚠️ 见 5.3 |
| OUT-04 | output | llm | L149-151 | ⚠️ 依赖外部决策树定义（C-7） |
| NEG-01 | negative | llm | "What it does not do" 第 1 条 | ✅ |
| NEG-02 | negative | llm | 第 3 条（weighting not elimination）| ✅ |

### 5.3 script 项实现 gap

**OUT-01（`output_contains("STUDY NOTES.*NOT LEGAL ADVICE")`）**
- 描述承诺："begins with the verbatim header ... as the first line, unmodified and not relocated"（首行 + verbatim + 不移位）
- 脚本实现：re.search 同行包含——header 出现在输出**任意位置**的任意行内即通过，无法验证"首行"、"未移位"、"verbatim"（`.*` 容忍任意分隔符变体，如 3 个连字符也会通过）。
- 结论：**描述比实现严格**。agent 在中段输出 header 也能得分；反过来，描述为 CF-02 提供了"移位即 cap"的依据，但脚本/llm 判定都无法可靠检测。建议二选一：脚本升级为首行精确匹配，或描述降级为"output includes the header"。

**OUT-03（`tool_log_contains("exam-forecasts/.*/forecast-\\d{4}-\\d{2}-\\d{2}\\.md")`）**
- 描述承诺："Forecast file is written to ..."（文件被写出）
- 脚本实现：只查工具日志中**出现**该路径字符串，不验证文件真实存在（Write 失败/被拒写的日志也可能含路径，或写失败后工具日志记录 ERROR 仍含参数）。
- 建议：增加 `file_exists("**/exam-forecasts/**/forecast-*.md")`（相对 workspace）双检查。
- Windows 路径风险：若工具日志记录 Windows 原生反斜杠路径（`...\exam-forecasts\Torts\forecast-2026-08-06.md`），正则要求字面 `/`，`\\` 不匹配 → 误判失败。Claude Code 通常以正斜杠记录路径，风险为中等，但在 Windows 测评环境值得兼容（正则允许 `[\\/]`）。
- 描述中附加的 "(in-chat and saved file both carry the header)" 属性与 tool_log 检查无关——header-in-file 属性未被任何检查覆盖（需要 file_contains 检查写出文件的头部）。

### 5.4 critical_failures 分析

| CF | 条件 | 与 SKILL.md 对应 | 合理性 | 重叠 |
|----|------|-----------------|:------:|------|
| CF-01 | 无试卷仍产出 forecast | L29 / "What it does not do" 第 2 条 | ✅ | 与 SCOPE-02 高度重叠（cap_to_0 vs 单项判断——双保险可接受） |
| CF-02 | header 缺失/改写/移位 | L84-88 | ✅ | 与 OUT-01 部分重叠，但 CF 施加 cap_to_0，更严格 |
| CF-03 | 以预测口吻呈现 | L26-27 / L135 | ✅ | 与 CON-01 重叠 |

**建议新增 CF-04**：Agent 编造 past exam 内容或虚报样本数（幻觉分析）→ cap_to_0。法律学习场景中虚构"往年考了 X"对学生的误导性极强，现有 15 条均未显式覆盖（CON-02 只覆盖 thin sample 声明，不覆盖虚报样本数）。这是本 skill 最重要的测评缺口。

### 5.5 llm judge 问题质量

- 问题多为单一 yes/no，evidence 字段指向明确（"Agent's intake questions"、"Agent's forecast framing section"）✅
- 复合问题（PROC-01 四合一、PROC-02 六合一、OUT-02 五合一）：binary 判定苛刻——缺任一子项即 fail，且 judge 难以给出粒度。建议改为"≥N 项满足即通过"或拆分子项，降低判定噪声。

---

## 6. 语法与格式质量（逐问题列举）

1. **拼写/语法**：未发现拼写错误；专业术语（issue-spotter, hypo, hobby horses）使用准确。✅
2. **标点一致性**：em dash（—）使用统一（header、L20 等处一致）；`[UNCERTAIN — framing]` 内 em dash 与全篇一致。✅
3. **header 三重定义**（L84-88 / L93 / SCORING OUT-01）：文本一致但常量重复定义，漂移风险（见 C-3）。
4. **"## [UNCERTAIN — framing]" 方括号歧义**（L133）：见 C-6。
5. **顶部编号风格**：L14 "Framed as weighting heuristic, not prediction." 以句号结尾，而 L8-13 无句号——列表标点风格不统一（极轻微）。
6. **模板占位符风格**：`[topic 1]` `[%]` `[yes/partial/no]` `[heavier / stable / lighter]` 风格统一，可读性好。✅
7. **双编号体系**：顶部 1-7 vs Step 1-5（见 §3.3）。
8. **表格格式**：Step 4 模板表格 4 列 + 分隔行规范（L105-107）。✅
9. **口语化表达**：L37 "If the user volunteers it in conversation that's fine; don't prompt for it." —— 非正式但指令清晰，属有意为之的友好语气，可接受。
10. **无 emoji 滥用**：SKILL.md 正文无 emoji；`🟢🟡🟠🔴` 仅用于本 REVIEW.md 评分标识。✅

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规范条目 | 结果 | 说明 |
|---|----------|:----:|------|
| 1 | name: 小写+连字符, ≤64, 匹配目录 | ✅ | exam-forecast / 229-exam-forecast |
| 2 | description: 第三人称, WHAT+WHEN+KEYWORDS, ≤1024 | ✅ | §2.2 |
| 3 | description: 无 imperative/first/second-person 开头 | ✅ | 以 "Analyze past exams..."（第三人称）开头 |
| 4 | description: 无 cross-skill routing | ✅ | 路由仅在 body Integration 节 |
| 5 | description: 至少一个触发信号短语 | ✅ | "Use when the user says..." |
| 6 | frontmatter: 无 forbidden keys | ✅ | 仅 name/description/argument-hint |
| 7 | body: ≤600 行 | ✅ | 160 行 |
| 8 | body: 有 workflow/process 节 | ✅ | L39-140 |
| 9 | body: 有 output format 节 | ⚠️ | 无独立节，模板内嵌于 Step 4（内容完整、结构偏差） |
| 10 | body: 有 scope/limitations 节 | ✅ | L153-159 |
| 11 | body: 无跨 skill 文件引用 (../other-skill/) | ✅ | 无文件级跨引用；仅有按名引用（集成节） |
| 12 | 目录: NNN-kebab-case | ✅ | 229-exam-forecast |

**补充核对**：
- §3.3 "引用另一 skill 用其名字 in prose" —— 集成节按名引用 ✅，但 3 个名字指向不存在的 skill（C-8），引用形式合规、引用对象失效。
- §3.2 process 型目标 ~200 行：实际 160 行，量级匹配 ✅。
- §3.4 内容指南：具体示例 ✅（"consideration and modification account for 30%"）；anti-patterns ✅（"Don't ask the user to type in the professor's name"）；decision tree——引用外部定义而非内嵌，⚠️。

**合规评级：🟢（无硬违规，1 项结构偏差）**

---

## 8. 人机感评估

| 维度 | 评分 | 说明 |
|------|:----:|------|
| 语气专业度 | 9/10 | 专业、克制、不夸大；"Not magic. A forecast, not a prediction." 的定调极佳 |
| 预期管理 | 10/10 | Purpose + Confidence discipline + What it does not do 三重护栏，全语料库标杆水平 |
| 对用户自主权的尊重 | 9/10 | 不强迫用户输入教授名（从材料提取）；"The tree is the output; the lawyer picks" 把决策权明确交还用户 |
| 风险提示 | 9/10 | "Skipping a topic ... is how students get burned" 具体、有温度；thin sample 主动声明 |
| 体验细节 | 7/10 | 要求 chat 回复首行为固定 header，多次调用时仪式化重复；`## [UNCERTAIN — framing]` 标题读感生硬 |
| 隐私/伦理 | 10/10 | 无敏感信息采集；输出含 NOT LEGAL ADVICE 免责标记，法律场景责任意识强 |

**综合评价**：本 skill 是"Agent 严苛纪律 + 人类判断出口"的典型范例（与 dossier 中 212/226 的哲学一致）。置信度纪律是核心卖点：默认 [UNCERTAIN]、阈值量化（3/5/6+）、显式 caveats、负面清单防过度承诺。人机感评分 **9/10**。

---

## 9. 可执行性评估

### 9.1 可直接执行的部分 ✅
- Step 4 模板完整可直接产出（header + 元信息 + 权重表 + 风格预测 + hobby horses + 少测主题 + 学习重点 + UNCERTAIN 框架）
- 输入形态明确（PDF / 粘贴文本 / 路径）
- 输出路径与文件名格式逐字符给出（含 `[YYYY-MM-DD]` 占位符）
- 教授匹配启发式明确（材料中提取，不询问）

### 9.2 依赖与风险

| 编号 | 风险 | 严重度 | 详情 |
|------|------|:------:|------|
| R-1 | Step 1 硬读插件 CLAUDE.md | 🔴 | `~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md` 不存在时无降级指令（文件缺失时该步骤行为未定义） |
| R-2 | 输出写入插件配置目录 | 🔴 | (a) 沙箱/隔离环境可能禁止写 home 目录 → 写失败 → OUT-03 假阴性；(b) 将用户学习产物写入插件配置目录是架构异味（配置目录非数据目录，且位于 ~/.claude 内部，用户不易发现产物） |
| R-3 | next-steps 决策树未自包含 | 🔴 | 五分支内容仅提及名字，无格式/判据/示例；无 CLAUDE.md 时无法执行 L151 指令 |
| R-4 | 集成节 3 个死引用 | 🟡 | outline-builder / flashcards / bar-prep-questions 不存在（C-8） |
| R-5 | PDF 解析失败无降级 | 🟡 | 无 OCR / 粘贴文本替代路径（C-12） |
| R-6 | OUT-03 Windows 路径正则 | 🟡 | 反斜杠路径失配风险（§5.3） |

### 9.3 可执行性评分

**6/10** —— 核心分析流程（摄入→逐卷分析→跨卷→预测→写出）无需任何外部工具即可执行，但 3 处 🔴 依赖在隔离测评环境中全部悬空，导致"读配置"与"收尾决策树"两个环节实际不可执行。若测评 runner 提供真实 CLAUDE.md，可升至 8/10。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖完备性

15 条 criteria 全部能在 SKILL.md 中找到对应指令（§5.2 表格逐条给出行号），无凭空 criterion，无"SKILL.md 有指令但未测评"的明显遗漏，除：
- L140 "Versioned — re-run and append"：无 criterion 覆盖（再次运行时生成新日期文件的行为未测评）——影响小
- 集成节引用：无 criterion 覆盖——可接受（集成是辅助信息）

### 10.2 Critical Failures 完备性

三个 CF 均直接映射 SKILL.md 的显式红线（无试卷不预测 / header 不移位 / 不作预测口吻），映射质量高。**缺口**：CF-04 幻觉（编造试卷内容或样本数）——见 §5.4，是本 skill 伦理风险最高而测评最薄弱的环节。

### 10.3 judge 分配合理性

- 13 llm + 2 script：OUT-01 / OUT-03 可脚本化 ✅（但实现有 gap，§5.3）
- CON/PROC/NEG 必须 llm 判断 ✅
- OUT-03 应升级为双检查（tool_log + file_exists），把"产物真实存在"纳入脚本验证——这是当前最值得补的脚本项。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 中 229 无独立条目，仅批次摘要记录（Batch 226-250，dossier L1004-1009）：

> **逻辑**: 229 样本摄入→跨卷模式分析→权重预测自洽
> **合规**: 🟢 226/227/229/231 三节齐全
> **总评**: 🟢 全组法律/合规类均为高质量

**验证结论**：
- "三节齐全" ✅ 成立（Workflow / Output 模板 / Scope 均存在，结构偏差见 §3.2 的 ⚠️）
- "逻辑自洽" 基本成立 ✅ —— 本次深度审查未发现核心分析逻辑的内部矛盾（阈值、路径、教授名处理均一致）；微问题集中在措辞（C-9 append）与标题歧义（C-6）
- **dossier 遗漏项**（本次审查新增发现）：
  - R-1/R-2/R-3 三处插件外部依赖悬空（可执行性问题，dossier 未记录）
  - 集成节 3 个死引用（C-8）
  - OUT-01 描述-实现 gap 与 OUT-03 无产物校验（测评严谨性问题）
  - CF-04 幻觉防护缺失（测评覆盖缺口）

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 10/10 | 10% | 1.00 | 描述为语料库上乘，触发设计完整 |
| Body 结构完整 | 8/10 | 10% | 0.80 | Output 无独立节（模板内嵌），双编号体系冗余 |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 核心自洽；UNCERTAIN 标题歧义、append 措辞、三处外部依赖 |
| 测评完整性 | 8/10 | 15% | 1.20 | 15 项全可追溯；OUT-01 gap、OUT-03 无产物校验、CF-04 缺失 |
| 语法格式 | 9/10 | 10% | 0.90 | 专业规范；header 三处重复、双编号为微瑕 |
| 规范合规 | 9/10 | 15% | 1.35 | 无硬违规；Output 独立节缺失为唯一结构偏差 |
| 人机感 | 9/10 | 10% | 0.90 | 置信度纪律与预期管理为全语料库标杆 |
| 可执行性 | 6/10 | 10% | 0.60 | 3 处 🔴 外部依赖在隔离环境悬空 |
| **加权总分** | | | **81.5/100** | |

### 12.2 评级

🟡 **B+** (81.5/100) — 高质量 skill：分析逻辑、置信度纪律、模板可执行性均为上乘；失分集中于**自包含性（外部插件依赖）**与**测评严谨性（脚本-描述 gap、无产物校验）**。修复 §13 的 🔴 项后可升至 🟢 A 档（90+）。

> 对照：dossier 批次总评为 🟢"高质量"——本审查结论与其一致，但按更严格的自包含标准（SKILL.md 应能在无外部插件 CLAUDE.md 时独立工作）评级为 🟡 B+。这一差异反映审查维度不同，非结论冲突。

---

## 13. 修复建议（按优先级分层）

### 🔴 高优先级（影响隔离环境下的可执行性与测评可靠性）

1. **解除 claude-for-legal 插件 CLAUDE.md 硬依赖**（SKILL.md L8 / L84 / L151）
   - Step 1 增加存在性检测与降级：`若 ~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md 不存在，跳过并注明"未找到课程配置文件"，以用户提供的材料为准`
   - 不修复后果：无插件环境中 Step 1 指令悬空，agent 行为不可预期

2. **将 next-steps decision tree 自包含进 SKILL.md**（L149-151）
   - 在 SKILL.md 内给出默认五分支模板（draft / escalate / more facts / watch and wait / something else）的格式与判据示例，外部 CLAUDE.md 仅作为"若存在则以其为准"的增强项
   - 不修复后果：agent 无法知道"决策树"长什么样，L151 与 OUT-04 的判定失去依据

3. **输出路径迁出插件配置目录**（L14 / L140）
   - 建议改为 `~/exam-forecasts/[class]/forecast-[YYYY-MM-DD].md`（用户可见、沙箱可写）或 `${WORKSPACE}/exam-forecasts/...`
   - 不修复后果：隔离环境写 ~/.claude 可能被拒 → 无 Write 工具记录 → OUT-03 假阴性；用户也难找到产物

4. **OUT-03 升级为双检查**（SCORING.yaml + check.py）
   - 脚本同时执行 `tool_log_contains(...)` 与 `file_exists("**/exam-forecasts/**/forecast-*.md")`；正则分隔符兼容 `[\\/]`
   - 不修复后果：Write 失败仍可能得分；Windows 路径环境可能误判

### 🟡 重要缺陷（建议修复）

5. **解决 `## [UNCERTAIN — framing]` 标题歧义**（L133）
   - 改为 `## Uncertainty framing`，正文以 `> [UNCERTAIN]` 引用块标注不确定性（与 Confidence discipline 措辞统一，去重）
   - 不修复后果：agent 可能省略该节导致 CON-01 判定失败（假阴性）

6. **OUT-01 描述与脚本对齐**（SCORING.yaml L84-88）
   - 方案 A：脚本升级——首行精确匹配 `^STUDY NOTES — NOT LEGAL ADVICE`（容忍空白）
   - 方案 B：描述降级为 "output includes the verbatim header"
   - 不修复后果：描述承诺了脚本验证不了的"首行/未移位"性质，测评结果不可复现

7. **统一 "re-run and append" 措辞**（L140）
   - 改为 "re-run 生成新日期文件；同日重复运行覆盖当日文件"
   - 不修复后果：agent 可能对旧文件做追加，破坏版本化

8. **新增 CF-04：幻觉防护**（SCORING.yaml）
   - `Agent 编造 past exam 内容、虚报样本数或虚构教授模式` → cap_to_0
   - 不修复后果：本 skill 最高伦理风险无测评兜底

9. **清理集成节死引用**（L144-147）
   - outline-builder / flashcards / bar-prep-questions 不存在于语料库——删除或改为"若已安装"条件式表述；保留 irac-practice
   - 不修复后果：agent 可能尝试调用不存在的 skill

10. **PDF 解析失败降级路径**（L10 / Step 2）
    - 增加"PDF 无法解析时告知用户并请其粘贴文本"的指令

### 🟢 优化建议（锦上添花）

11. **合并 header 三重定义**（L84-88 / L93）
    - 只保留模板内一处定义，L84 引用之（"模板第一行"），消除漂移风险

12. **顶部索引与 Step 1-5 编号统一**
    - 顶部改为纯索引行（intake → per-exam → cross-exam → forecast → output），或直接删除

13. **清理 check.py 未使用 import**（check.py L12-20）
    - 14 个未使用：file_exists, file_contains, file_valid_json, json_field_exists, json_field_equals, json_field_matches, json_array_nonempty, json_array_all_have_keys, timestamp_before, timestamp_after, tool_log_not_contains, tool_log_read_before_write, tool_log_order, output_not_contains；check() 的 workspace 参数亦未使用

14. **复合问题容错**（SCORING PROC-01 / PROC-02 / OUT-02）
    - 改为"≥N 项满足即通过"或拆分子项，降低 llm judge 的 binary 噪声

### 修复工作量估计

- 预计修改文件数：3（SKILL.md + SCORING.yaml + check.py）
- 预计新增行数：~50-70（存在性检测 + 决策树模板 + 降级路径 + CF-04 + 双检查）
- 预计修改行数：~20-30（标题、措辞、路径、imports）
- 预计可提升分数：81.5 → 90+（A 档），其中 🔴 四项合计约 +6 分，🟡 五项约 +4 分

---

## 变更记录

- 2026-08-06: 初始深度审查。读取本 skill 全部 3 个文件（SKILL.md 160 行 + SCORING.yaml 143 行 + check.py 69 行）+ 3 个上下文文件（checker.py 351 行 + SKILL-SPEC.md + CHECKER-LIBRARY.md）+ skill-dossier.md 相关批次条目。本目录此前无 REVIEW.md。

---

## 附录: 审查过程记录

- 读取文件数：6（3 个 skill 文件 + 3 个上下文/规范文件）
- 读取总行数：~980 行（skill 文件 372 行 + 上下文 608 行）
- 验证手段：
  - grep 语料库 complex-skills/ 全部目录，确认集成节 4 个引用中仅 164-irac-practice 存在（3 个死引用）
  - 逐正则推演 OUT-01 / OUT-03 在 Unix 正斜杠与 Windows 反斜杠路径下的匹配行为
  - 逐条将 SCORING.yaml 15 条 criteria 映射回 SKILL.md 行号，验证可追溯性
  - 对照 SKILL-SPEC.md v1.0 12 项合规清单逐项核验
  - 对照 skill-dossier.md Batch 226-250 条目交叉验证既有结论
- 重点深度审查文件：SKILL.md（全文件）、SCORING.yaml（全文件）、check.py（全文件）
- 审查立场：以"skill 应自包含、测评应可复现"为标准；外部插件 CLAUDE.md 视为环境依赖而非 skill 内容
