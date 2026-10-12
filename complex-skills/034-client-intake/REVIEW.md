# REVIEW: 034-client-intake

**审查日期**: 2026-08-06 | **Skill 类型**: process — 多阶段法律诊所客户接待与案例摘要产出 | **Body 行数**: 238 | **参考文件数**: refs/5

---

## 1. 目录全量清单

目录 `D:\SkillIF\skill-experiment\complex-skills\034-client-intake\` 共 5 个文件（1 个 Body + 3 个附属文件 + 1 个参考文件 + 1 个本审查文档）：

| # | 文件路径 | 行数 | 类型 | 说明 |
|---|---|---|---|---|
| 1 | `SKILL.md` | 243 | Body | Frontmatter 5 行 + Body 238 行（L6–L243） |
| 2 | `SCORING.yaml` | 159 | 评测标准 | 17 条 criteria（3+3+4+6+1）+ 3 条 critical_failures |
| 3 | `check.py` | 73 | 评测脚本 | 2 个 script 检查（PROC-03 / TOOL-01），依赖 `_shared/checker.py` |
| 4 | `references/intake-templates/README.md` | 15 | 参考文件 | 模板目录说明，声明冷启动填充机制 |
| 5 | `REVIEW.md` | 7 | 审查文档 | 旧版 7 行 stub（本文件即为其替换物） |

要点：

- 目录结构与 corpus 标准一致：`NNN-kebab-case-name/` + 可选 `references/`、`SCORING.yaml`、`check.py`。
- `references/intake-templates/` 下**仅有 README.md**。SKILL.md L230 与 README L8–11 声称存在的 `immigration.md`、`housing.md`、`family.md`、`consumer.md` 四个模板文件**均不存在**（README L3–4 明确这是"cold-start"设计——教授提供表单前不生成，由 Step 2 内置默认问题集兜底）。这是设计意图而非疏漏，但构成引用矩阵中的"不可见资源"，详见 §5。
- 旧 REVIEW.md 为 7 行 stub（内容见附录），已被本文替换。

---

## 2. Frontmatter 逐字段审查

### 2.1 字段清单

| 字段 | 值 | 判定 | 依据 |
|---|---|---|---|
| `name` | `client-intake` | ✅ | 小写 + 连字符，≤64 字符；与目录 `034-client-intake` 的 kebab 部分完全一致（NNN 前缀属目录命名规范，不进入 name 字段，符合 corpus 惯例） |
| `description` | 见 2.2 逐句分析 | ✅ | ≤1024 字符（实测约 310 字符） |
| `argument-hint` | `"[optional: practice area hint]"` | ✅ | SPEC §1.2 允许字段；与 Step 1 路由逻辑衔接——提示可携带实践领域，agent 可直接跳过路由提问 |
| `allowed-tools` | 未声明 | ⚠️ | 可选字段。但 body 隐含需要 `Read`（加载插件 CLAUDE.md、guides）与 `Write`（TOOL-01 要求将摘要持久化为 `.md` 文件），显式声明可提高可执行性一致性，见 §13 |

无任何 SPEC §1.3 禁用键（无 `metadata`/`version`/`tags`/`trigger` 等）。YAML 语法合法，无引号转义问题，两行 frontmatter 均以 `---` 正确闭合。

### 2.2 description 逐句分析

原句（L3）：

> Structured intake — practice-area templates, cross-area issue spotting, conflict flags, and triage classification. Produces a formatted case summary the student analyzes and the professor reviews. Does NOT decide case acceptance. Use when starting a new client intake, running an intake interview, or writing up a new client's situation.

| 句 | 内容 | 三问定位 | 判定 |
|---|---|---|---|
| 句 1 | Structured intake — 模板、跨领域识别、冲突标记、分诊分类 | WHAT（动作 + 四个特性词） | ✅ 具体不空洞 |
| 句 2 | 产出 formatted case summary，学生分析、教授审阅 | WHAT（交付物 + 人类分工） | ✅ 清晰定义产物边界 |
| 句 3 | Does NOT decide case acceptance | 边界否定（防误用） | ✅ 与 Body "What this skill does NOT do" 呼应 |
| 句 4 | Use when starting a new client intake / running an intake interview / writing up a new client's situation | WHEN（三个触发场景） | ⚠️ 触发信号存在但句式非规范，见下 |

**Voice**：全程第三人称，无 imperative 开头、无第一/二人称，符合 SPEC §2.3。**无跨 skill 路由**（"NOT for X, use Y"）嵌入，符合 §2.5。

**触发信号**（§2.4 要求至少一条）：句 4 以 "Use when starting..." 开头——包含 "Use when" 信号但**未采用规范句式 "Use when the user ..."**。SPEC 列出的五个信号短语为 `"Use when the user..."`、`"Use when the user asks to..."`、`"Use when the user needs to..."`、`"Triggers on..."`、`"Use for..."`。严格比对时 `"Use when starting"` 不在清单内；语义上仍是无歧义的触发声明，我判为 ✅（含注），但建议标准化（见 §13，🟢P5）。

**KEYWORDS**：client intake、intake interview、practice area、case summary、triage、conflict——领域词齐全，动作动词（starting/running/writing up）可匹配用户意图。

### 2.3 语法

- 单引号外无未转义特殊字符；YAML 纯字符串值，无冒号歧义。
- `argument-hint` 中的 `[optional: ...]` 方括号为字面量，无解析问题。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（L6–L243）

| 行号 | 标题 | 级别 | 功能 | 备注 |
|---|---|---|---|---|
| L6 | `# Client Intake` | H1 | 标题残片 | **与 L20 重复**（见下） |
| L8–16 | 5 条编号 TL;DR + 代码块 | — | 极简总览 | **残片**：与全文重复且条目数（5）与工作流（7 步）不符 |
| L20 | `# Client Intake` | H1 | 正文标题 | 重复的第二个 H1 |
| L22–28 | `## Purpose` | H2 | 动机 + "What it doesn't do" | 边界声明前置，得体 |
| L30–32 | `## Load context` | H2 | 外部上下文加载 | 指向插件 CLAUDE.md |
| L34–38 | `## Read the supervisor guide` | H2 | 可选的领域指南覆盖 | **唯一带回退逻辑的外部依赖** |
| L40–143 | `## Workflow` | H2 | 7 步工作流 | 详见 3.2 |
| L145–226 | `## Output` | H2 | 输出模板（完整 Markdown 围栏） | 含 privilege 声明、provenance 词汇说明 |
| L228–230 | `## Practice-area intake template references` | H2 | 参考目录说明 | 冷启动机制 |
| L232–237 | `## What this skill does NOT do` | H2 | 边界（4 条） | 对应 SPEC 必需"Scope"节 |
| L239–241 | `## Close with the next-steps decision tree` | H2 | 收尾指令 | 委托插件 CLAUDE.md `## Outputs` |

### 3.2 必需章节（SPEC §3.1）

| 必需章节 | 位置 | 判定 |
|---|---|---|
| Workflow / Process | `## Workflow`（L40–143），7 个 `### Step N` | ✅ 完整、有序、每步可执行 |
| Output Format | `## Output`（L145–226），完整可复制的模板 | ✅ 详尽，含占位符与两处 provenance 说明 |
| Scope / Limitations | `## What this skill does NOT do`（L232–237） | ✅ 4 条显式边界 + Purpose 内的 "What it doesn't do" |

### 3.3 委托结构

- **本目录内委托**：`references/intake-templates/[area].md`（L230）——按设计冷启动，不存在时回退 Step 2 默认问题集。
- **外部插件委托**（关键）：`~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` 在 8 处被引用（L8/32/52/99/120/168/202/241），承担：实践领域清单、模板、监督风格、管辖地、flag 触发词、provenance 词汇表（`## Shared guardrails`）、输出约定（`## Outputs`）、决策树默认分支。**无回退**——这是本 skill 最大的可移植性风险（详见 §4/§5/§9/§13）。
- 无嵌套 skill；跨 skill 引用均为散文式命名（`deadlines` skill，L124/141），符合 SPEC §3.3。

### 3.4 层级健康度

- H1 出现两次（L6/L20）——同一文件内两个 `# Client Intake`，是重构残留（TL;DR 残片的一部分），应合并（§13 🟡P1）。
- H2 为主干（11 个），H3 用于 7 个 Step，层级 2–3 级、单调递增，无跳级。
- 段落长度：最长为 Output 模板（82 行，作为单块围栏合理）；Step 2 内含 4 个领域子列表（Immigration/Housing/Family/Consumer），信息密度均匀。

### 3.5 长度

- Body 238 行（含代码块与表格）。process 模式目标 ~200 行，超约 19%，处于健康区间；远低于 600 行硬上限。
- 与 dossier 记录的 242 行差 1 行（dossier 可能未计入末尾空行），无实质分歧。

---

## 4. 逻辑一致性深度审查

### 4.1 衔接与指代

| # | 发现 | 严重度 |
|---|---|---|
| 1 | **TL;DR 残片与全文脱节**：L8–12 的 5 条总览与 L40–143 的 7 步工作流不匹配——总览将"冲突检查 + 分诊"合并为一条（L11），且缺少 Step 6（监督 flag）与 Step 7（deadline 交付物）这两个关键步骤的表述。总览条目 1（Load CLAUDE.md）与正文 `## Load context` 重复。 | 🟡 |
| 2 | L15 代码块 `/legal-clinic:client-intake` 孤立出现在 TL;DR，正文再无说明该 slash command 与 skill 的关系（应视为插件注册的调用入口）。 | 🟢 |
| 3 | L38 指代正确："Step 1 of the workflow below" 指向 L42 的 Step 1；"re-check for the guide after routing" 逻辑自洽（guide 路径依赖实践领域）。 | ✅ |
| 4 | Step 7（L122–143）与 Output 模板 `## Deadlines to log`（L197）双向引用一致："emit ... as part of the intake output" ↔ "One block per surfaced deadline — Step 7"。 | ✅ |
| 5 | `due=` 规则三条款（L141–142）无矛盾：文档给定日期 → 直接填入；按天数计算 → 保留 `[VERIFY — student + supervisor compute]`；与 SCORING PROC-04 逐字对齐。 | ✅ |
| 6 | Step 6（L118–120）用条件式（"If formal queue or configurable flags are enabled, and a trigger is present"），Step 7 用强制性（"required deliverable, not a suggestion"）——两种强度刻意区分（flag 为可选项、deadline 为硬交付物），内部一致。 | ✅ |
| 7 | **generic-intake 注记无插入点**：L36 要求"note at the end of the intake summary"，但 Output 模板的尾部顺序是 Verification prompts → What this summary does NOT do →（正文外的）decision tree，模板内没有为这条注记预留位置，agent 需自行判断"end"指哪里。 | 🟡 |
| 8 | L224 `[Professor]`（带方括号、大写）与 L210 `[professor]`（无方括号、小写）指代同一角色，占位符样式不一致。 | 🟢 |

### 4.2 矛盾检查

- 无自我矛盾声明。全篇一致坚持"不决定接案、不给建议、不解决冲突、不产出最终文档"四条边界（L28 / L232–237），且与 description 句 3 呼应。
- 示例法条准确：L134 "UD complaint served 2026-05-04, CCP § 1167"（加州 Code of Civil Procedure §1167 为 unlawful detainer 起诉条款）用法正确；L171 "RLTO §5-12-080"（芝加哥 Residential Landlord and Tenant Ordinance，真实法令）格式合理。示例是真实法条而非编造，提升模板可信度。
- 跨领域触发表（L87–93）5 行全部合理，特别是 L93 "The landlord said he'd call ICE" 同时标记 housing + immigration + retaliation——法律判断正确（房东以 ICE 相威胁构成报复性威胁）。

### 4.3 代码与条件

- 无伪代码、无未定义的代码实体（对比 033-research-lookup 的教训——本 skill 引用的 `/legal-clinic:*` 命令属于外部插件命名空间，文档性质与"未定义类"不同）。
- 输出模板围栏内嵌 backtick（如 L197 行内代码）与 `[VERIFY — student + supervisor compute]` 标记，语法在 Markdown 围栏内合法。
- 条件分支（guide 存在/不存在、deadline 有无、flag 开关）均给出明确行为，无悬挂条件。

---

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用（位置） | 目标 | 类型 | 存在性 | 判定 |
|---|---|---|---|---|
| L8/32/52/99/120 | `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` | 外部插件配置 | 本目录不可验证 | ⚠️ 高依赖、无回退 |
| L168/202/241 | 插件 CLAUDE.md 的 `## Shared guardrails` / `## Outputs` 小节 | 外部文档内部锚点 | 不可验证 | ⚠️ provenance 词汇表与决策树默认分支依赖之 |
| L36 | `~/.claude/plugins/config/claude-for-legal/legal-clinic/guides/<practice-area>.md` | 外部文件 | 不可验证 | ✅ 有回退（generic intake + 注记） |
| L230 | `references/intake-templates/[area].md` | 本目录相对路径 | ❌ 4 个文件均不存在 | ⚠️ 冷启动设计（README L3–4 明示），但运行期引用不可解析 |
| L15/36/124/129/141/197 | `/legal-clinic:client-intake`、`/legal-clinic:build-guide`、`/legal-clinic:deadlines --add` | 插件 slash command | 不可验证 | ✅ 散文式跨 skill/插件引用合规 |
| L124/141 | "the deadline skill" | 跨 skill 散文式引用 | — | ✅ 符合 SPEC §3.3 |
| check.py L11 | `_shared/checker.py`（`sys.path.insert(0, "..", "_shared")`） | 共享库 | ✅ 存在，函数签名完全匹配（见 5.3） | ✅ |

### 5.2 不可见资源（风险清单）

1. **插件 CLAUDE.md（8 处引用）**：承担 practice areas、intake templates、supervision style、jurisdiction、flag triggers、provenance 词汇、输出约定、决策树默认分支共 8 类内容。若评测工作区未挂载 `~/.claude/plugins/config/claude-for-legal/`，则 Step 1 无法加载、Step 4/6 的"Per CLAUDE.md"指令悬空、输出模板的两处 provenance 说明（L168/202）与收尾决策树（L241）无定义来源。**这是全 skill 唯一没有兜底的关键路径**——对比之下，guides 反而有完整回退（L36），优先级倒挂。
2. **`~` 用户主目录路径**：硬编码相对用户主目录的绝对路径，跨机器不可移植（作者机可用、评测沙箱大概率不可用）。
3. **`references/intake-templates/` 四个模板文件**：README L8–11 列出文件与内容契约，但文件缺失。设计上有意（冷启动），且 Step 2 有完整默认问题集兜底，实际执行不会断裂——但任何"检查引用完整性"的静态审查都会报缺失，建议把设计意图显式写进 SKILL.md（§13）。

### 5.3 共享库验证

`D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py` 提供 `tool_log_contains`、`output_contains`、`set_tool_log_path`、`set_agent_output`，与 check.py 的 import 和调用签名逐一匹配；`output_contains` 的 MULTILINE 正则模式与 PROC-03 的 `legal-clinic:deadlines --add` 兼容。check.py 内部 L22–29 的"路径 vs 原始文本"二分支逻辑与 main()（L61–63）的读文件逻辑有轻微重复，但行为正确、无害。

### 5.4 嵌套与跨 Skill

无嵌套 skill；跨 skill 仅散文式命名（deadlines、build-guide），无 `../other-skill/` 文件级引用——完全符合 SPEC §3.3 的禁止条款。

---

## 6. 语法与格式质量

| 检查项 | 结果 | 说明 |
|---|---|---|
| 拼写 | ✅ | 全文无拼写错误（抽查 243 行） |
| 术语一致性 | ✅ | `intake` / `CLAUDE.md` / `practice area` / `provenance` / `deadlines --add` 用法一致 |
| Markdown 结构 | ✅ | 表格 3 处（跨领域、分诊、Key facts）、代码围栏 3 处（TL;DR 命令、deadline 块模板、输出模板）、引用块 1 处（开场问题 L46），语法全部合法 |
| 占位符 | ✅ | `[date]`、`[student]`、`[practice area]`、`[VERIFY — ...]` 等统一方括号风格，无残留未替换的真实数据 |
| 截断 | ✅ | 无中途截断迹象；L243 收尾完整 |
| 混杂 | ✅ | 全英文、无中英混杂、无乱码 |
| 标点 | ✅ | em dash（—）作为分隔符使用一致；L36 长句（60+ 词）可读性尚可 |
| 小瑕疵 | ⚠️ | (1) L6/L20 双 H1；(2) L15 孤悬代码块；(3) L210 `[professor]` vs L224 `[Professor]` 占位符大小写不一致；(4) L36 的 generic 注记位置未在模板定义（§4.1-#7） |

无 placeholder 残留（如 TODO/FIXME）、无 lorem 文本、无被截断的半句。整体为 corpus 中语法质量最高的梯队（与 dossier 评价"干净、精确"一致）。

---

## 7. 规范合规性（SKILL-SPEC.md 12 项清单）

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符，≤64，匹配目录 | ✅ | `client-intake` 与目录 kebab 部分一致 |
| 2 | description：第三人称，WHAT+WHEN+KEYWORDS，≤1024 | ✅ | 约 310 字符，三问齐备 |
| 3 | description：无 imperative/第一/二人称开头 | ✅ | 名词短语 + "Use when..." |
| 4 | description：无跨 skill 路由 | ✅ | 仅有单句边界否定（合规） |
| 5 | description：≥1 触发信号 | ✅* | "Use when starting..." 含信号但非标准句式，见 §2.2 注 |
| 6 | frontmatter：无允许列表外键 | ✅ | 仅 name/description/argument-hint |
| 7 | body ≤600 行 | ✅ | 238 行 |
| 8 | body 有 workflow/process 节 | ✅ | `## Workflow` 7 步 |
| 9 | body 有 output format 节 | ✅ | `## Output` 完整模板 |
| 10 | body 有 scope/limitations 节 | ✅ | `## What this skill does NOT do` |
| 11 | body 无跨 skill 文件引用 | ✅ | 无 `../` 引用 |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✅ | `034-client-intake` |

**结果：12/12 通过**（#5 带注）。合规性为 corpus 顶尖水平——三必需节齐全且质量高，这在 322 个 skill 中并不常见（dossier 中不少 🟡 的根因正是缺 output-format 节或 scope 单薄）。

---

## 8. 人机感评估

| 维度 | 结果 | 说明 |
|---|---|---|
| Emoji | ✅ 零使用 | 全文无 emoji（对比 036 将 emoji 限于模板数据内，本 skill 完全不用，更克制） |
| 全大写 | ✅ 仅模板标记 | `VERIFY`（L133/141）、`AI-ASSISTED DRAFT`（L151）、`QUEUED`（L210）均为模板数据标记，非语气性大写 |
| 语气 | ✅ 专业且适度温暖 | "This is the human story."（L164）、"Intake is one of the biggest bottlenecks... the waitlist grows"（L24）——有人味但不说教、无填充 |
| 人机边界 | ✅ 极清晰 | L28 "Claude accelerates the information-gathering and structuring, not the lawyering"；L241 "The tree is the output; the lawyer picks"；`## What this skill does NOT do` 4 条边界 |
| 人称 | ✅ | description 与 body 均第三人称；仅输出模板内出现 "your analysis"（L223–225）——那是给学生看的文档，属模板内容而非 agent 语气 |
| 表格密度 | ✅ 适中 | 3 张表 / 238 行 ≈ 1.3%，跨领域表、分诊表、Key facts 表均为"决策树化"的正确用例（SPEC §3.4：decisions → tables） |
| 场景温度 | ✅ | 敏感主题（家暴 L72、刑事记录 L59、ICE 威胁 L93）均标注"handle carefully / sensitive"的护理提示 |

评价：专业、克制、边界感强——"student/professor" 分工框架全文一致（dossier 同评），是法律领域 skill 的理想人机感样板。

---

## 9. 可执行性评估

**独立可执行性评分：7 / 10**（分环境差异极大，见下）

| 子项 | 得分 | 说明 |
|---|---|---|
| 步骤操作性 | 9/10 | 7 步每步都有具体指令：开场问题（L46 引用块）、四领域默认问题集（L54–81）、触发短语表、conflict 清单、分诊表、deadline 块逐字段格式 |
| 交付物明确性 | 8/10 | deadline 块字段级规格（case/type/description/due/source/owner/warnings + 3 条规则）是全 skill 最精确的部分；但"把摘要写进文件"未明说（TOOL-01 依赖此行为，见 §10） |
| 工具依赖 | 5/10 | 关键路径依赖插件 CLAUDE.md（8 处），无回退；`~` 绝对路径在沙箱大概率不可解析 |
| 独立运行（无插件环境） | 6/10 | Step 1/4/6 的 "Per CLAUDE.md" 指令悬空 → NAV-01/NAV-02/PHIL-02 的输出约定（provenance 词汇、决策树）失去定义；Step 2/3/5/7 与 Output 模板其余部分仍可自足执行 |
| 独立运行（插件环境） | 9.5/10 | 按设计用途（claude-for-legal 插件已安装）运行时近乎满分 |

结论：skill 本身的自洽性极高，瓶颈完全在外部依赖契约。修复 P0（§13）后独立可执行性可升至 8.5–9/10。

---

## 10. SCORING.yaml 交叉参考

### 10.1 17 条 criteria 溯源

| ID | 类别 | 检查点摘要 | Body 对应位置 | 判定方式 | 一致性 |
|---|---|---|---|---|---|
| MIND-01 | mindset | 不决定接案，归属学生分析+教授判断 | L28、L234–237 | llm | ✅ |
| MIND-02 | mindset | 接待中不给法律建议 | L236 | llm | ✅ |
| MIND-03 | mindset | 全程听跨领域问题 | Step 3（L83–95） | llm | ✅ |
| NAV-01 | navigation | 加载 legal-clinic 上下文 | `## Load context`（L32） | llm | ✅ 但依赖插件存在（§5.2-#1） |
| NAV-02 | navigation | 检查领域 guide，无则标注 generic | `## Read the supervisor guide`（L36） | llm | ✅ 有回退 |
| NAV-03 | navigation | 路由到正确模板 | Step 1（L42–48） | llm | ✅ |
| PHIL-01 | philosophy | 输出带 AI-ASSISTED 标签 + privilege 声明 | 输出模板 L151–153 | llm | ✅ |
| PHIL-02 | philosophy | 每条引用带 provenance tag | L168、L202 | llm | ✅ 词汇依赖插件 |
| PHIL-03 | philosophy | 冲突只标记不解决 | Step 4（L105）、模板 Conflict check | llm | ✅ |
| PHIL-04 | philosophy | 分诊是输入非接案决策 | Step 5（L109）、模板 Triage | llm | ✅ |
| PROC-01 | process | 摘要结构 9 节齐全 | 输出模板 L147–210 | llm | ✅ 模板节序与 criterion 列举一致 |
| PROC-02 | process | 跨领域标注 UNCERTAIN/转介标记 | 模板 L176 | llm | ✅ |
| PROC-03 | process | 每个 deadline 一个 `legal-clinic:deadlines --add` 块 | Step 7（L124）、L197 | script | ✅ 正则 `legal-clinic:deadlines --add` 与 body 逐字匹配 |
| PROC-04 | process | due= 规则（VERIFY vs 直接日期） | L141–142 | llm | ✅ 逐字对齐 |
| PROC-05 | process | 学生验证提示 | 模板 `## Verification prompts`（L216–219） | llm | ✅ |
| PROC-06 | process | 结尾定制化决策树 | `## Close with...`（L241） | llm | ✅ 依赖插件默认分支 |
| TOOL-01 | tool | 摘要持久化为 .md 文件（Write） | **无显式指令** | script | ⚠️ 见 10.3 |

### 10.2 critical_failures

| ID | 触发条件 | Body 对应 | 判定 |
|---|---|---|---|
| CF-01 | agent 决定接案/拒案 | MIND-01 边界 | ✅ 合理 cap_to_0 |
| CF-02 | 接待中给法律建议 | MIND-02 边界 | ✅ 合理 cap_to_0 |
| CF-03 | 有 deadline 却未产出 `deadlines --add` 块 | Step 7 强制性表述 | ✅ 合理 cap_to_0 |

### 10.3 发现的缝隙

1. **TOOL-01 vs Body 缝隙**：TOOL-01 要求工具日志中出现 `Write.*\.md`，但 Body 从未显式说"把摘要写入文件"（Output 节只给出模板，Step 7 只说"emit"deadline 块）。按字面执行 skill 的 agent 完全可能只在对话中产出模板，导致 TOOL-01 失败。修复：Output 节加一句持久化指令（§13 🟡P2）。
2. 17 条 criteria 与 3 条 CF 无冗余、无遗漏；categories 占比（mindset 3 / navigation 3 / philosophy 4 / process 6 / tool 1）与 process 模式匹配；`total_items: 17` 计数正确（3+3+4+6+1）。
3. check.py 仅实现 PROC-03 与 TOOL-01 两个 script 检查，其余 15 条为 llm judge——与 SCORING.yaml 标注一致，无错配。

---

## 11. 已知问题汇总（skill-dossier.md 引用）

Dossier 条目（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` L304–309）：

> - **逻辑**: 7 步工作流完全一致，所需的 `/legal-clinic:deadlines --add` 交付物集成到每个阶段。
> - **语法**: 干净、精确、诊所适当的文体。
> - **人机感**: 专业且适当温暖；"student/professor" 框架一致，无填充。
> - **合规**: 🟢 完全合规——三必需节齐全，242 行 ≤600。
> - **总评**: 🟢 彻底、连贯、合规——法律诊所 skill 家族的强样例。

对照评估：

| dossier 论断 | 本次审查 | 一致性 |
|---|---|---|
| 7 步工作流完全一致 | 工作流主体一致 ✅；但发现 TL;DR 残片（5 条 vs 7 步）与 generic 注记位置未定义两个衔接瑕疵 | 基本一致，本审查更细 |
| deadlines 交付物集成 | ✅ 确认——Step 7 + 模板 + SCORING PROC-03/CF-03 三方咬合 | 一致 |
| 干净精确的文体 | ✅ 确认（§6） | 一致 |
| 🟢 完全合规 | ✅ 12/12（§7，#5 带注） | 一致 |
| 242 行 | 实测 243 行（差 1，尾部空行计数差异） | 无实质分歧 |
| 总评 🟢 典范 | 本审查给 🟢 A−（87/100，§12）——比 dossier 更保守一级，扣分项集中在外部依赖回退与 TOOL-01 缝隙，均不推翻"强样例"定位 | 方向一致 |

旧 REVIEW.md stub（7 行）给出的结论"🟢 A− (55/100) — 仅可移植性扣分"与本审查结论一致（均判 A−，均以可移植性为主要扣分项）；本审查在此基础上补充了可移植性之外的新发现（TL;DR 残片、TOOL-01 缝隙、免责声明缺口、模板文件缺失）。

---

## 12. 综合评分（8 维度加权）

| 维度 | 权重 | 得分 | 依据 |
|---|---|---|---|
| 逻辑一致性 | 15% | 9.0 | 7 步自洽、三方咬合；扣分：TL;DR 残片条目不符、generic 注记无插入点 |
| 参考文件与资源 | 15% | 7.5 | README/checker.py 可用；扣分：4 模板文件缺失、插件依赖不可验证 |
| 语法与格式 | 10% | 9.5 | 全净；仅 [Professor]/[professor] 等微瑕 |
| 规范合规性 | 20% | 9.5 | 12/12 通过；触发句式非标准扣 0.5 |
| 人机感 | 10% | 9.5 | 零 emoji、边界极清晰、专业温暖 |
| 可执行性 | 10% | 7.0 | 步骤可操作性满分，但关键路径外部依赖无回退、Write 指令缺失 |
| SCORING 对齐 | 10% | 8.5 | 17+3 全可溯源；TOOL-01 与 Body 间缝扣 1.5 |
| 法律适切性 | 10% | 9.0 | privilege 声明、AI-ASSISTED 标签、接案边界齐全；缺显式 "not legal advice" 行 |

**加权总分 = 1.35 + 1.125 + 0.95 + 1.90 + 0.95 + 0.70 + 0.85 + 0.90 = 8.73 ≈ 8.7 / 10**

### 总评：🟢 A−（87/100）

法律诊所 skill 家族强样例（dossier 同评）。合规全绿、逻辑自洽、交付物规格精确，是 322 个 skill 中"流程型 skill 应长什么样"的教科书；扣分全部集中在**外部依赖契约**（硬编码插件路径无回退）与**两处执行缝隙**（TOOL-01 无显式 Write 指令、TL;DR 残片未清理）。修复 §13 的 P0–P2 后可达 9.3+（🟢 A）。

---

## 13. 修复建议（按优先级分层）★重点★

### 🔴 P0 — 致命（条件性）：外部插件依赖无回退

**问题**：`~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` 被 8 处引用、承载 8 类内容，但**全 skill 没有一处 fallback**。评测/沙箱环境若未挂载该插件（`~` 相对绝对路径在隔离工作区大概率不可解析），则 Step 1 加载失败、Step 4/6 "Per CLAUDE.md" 悬空、provenance 词汇表（L168/202）与决策树默认分支（L241）失去定义来源，NAV-01/PHIL-02/PROC-06 三条 criteria 直接不可达。讽刺的是，次重要的 guides（L36）反而有完整回退——优先级倒挂。

**修复**（工作量 ~30 分钟）：
1. 在 `## Load context` 加条件分支：

```
If `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` exists,
load it and follow its practice areas, templates, supervision style, jurisdiction,
and flag triggers. If it does not exist (no clinic config mounted), proceed with
the generic defaults below and note at the top of the summary:
"Clinic config not loaded — generic defaults applied."
```

2. 为 Step 4/6 追加同一回退句："no config loaded → use the generic conflict checklist / supervision defaults above"。
3. 为 L168/202 的 provenance 词汇与 L241 的决策树默认分支追加回退："if plugin CLAUDE.md is unavailable, use the tag vocabulary documented in this template and the five default branches listed here"——并把五默认分支（draft the X / escalate / get more facts / watch and wait / something else）从插件引用改为本文内显式列出（消除循环依赖）。

### 🟡 P1 — 重要：清理 TL;DR 残片（L6–17）

**问题**：SKILL.md 顶部保留着重构前的极简 stub——`# Client Intake` H1 出现两次（L6/L20），5 条总览与 7 步工作流条目数不符且缺失 Step 6/7，L15 的 `/legal-clinic:client-intake` 代码块孤立。与本文替换掉的 7 行 REVIEW stub 属于同一批"草稿残留"。

**修复**（工作量 ~15 分钟）：删除 L6–17 的整个 TL;DR 区块，保留 L20 起的正式正文；如要保留总览，改写为与 7 步一一对应的表格（比编号列表防漂移），并把 `/legal-clinic:client-intake` 挪到正文（如 `## Load context` 下注明"本 skill 由插件命令 `/legal-clinic:client-intake` 调用"）。

### 🟡 P2 — 重要：Output 节补显式持久化指令（对齐 TOOL-01）

**问题**：TOOL-01（script 检查）要求工具日志出现 `Write.*\.md`，但 Body 从未说"把摘要写入文件"。按字面执行的 agent 可能只在对话中产出模板 → 评测直接失分。

**修复**（工作量 ~10 分钟）：在 `## Output` 开头加一句：

```
Write the completed summary to `intake-summaries/<client-slug>.md` in the
workspace (persisted deliverable for the student), then emit the same content
in your reply with the next-steps decision tree.
```

同时建议在 frontmatter 显式声明 `allowed-tools: Read, Write, Glob, Grep`（工具契约化，与 body 需求一致）。

### 🟡 P3 — 重要：输出模板补显式免责声明行（法律适切性）

**问题**：本 skill 是 client intake（涉敏感个人信息与法律建议边界）。现有保护：AI-ASSISTED 标签 ✅、privilege/confidentiality 声明 ✅（L153，质量高）、不接案边界 ✅。但模板**缺少一句面向客户的显式 "not legal advice" 免责声明**——privilege 声明讲的是传播边界，不覆盖"本摘要不构成法律意见"这一面向。

**修复**（工作量 ~5 分钟）：在 L151 的 AI-ASSISTED 行后追加：

```
**Not legal advice.** This draft is an information-gathering artifact, not
legal advice or attorney work product. All conclusions are hypotheses for
supervised analysis.
```

### 🟡 P4 — 重要：模板引用文件缺失的两选项（二选一）

**问题**：`references/intake-templates/` 下 4 个模板文件（immigration/housing/family/consumer.md）缺失。README 声明为冷启动设计、Step 2 有默认问题集兜底，执行不断裂，但静态审查会持续误报"引用悬空"。

**修复**（二选一，工作量 30–60 分钟）：
- 方案 A（推荐，工作量 30 分钟）：把 SKILL.md L230 的措辞改为显式冷启动声明（"These files are populated at cold-start from the professor's intake forms; until then Step 2 defaults apply"），并在 README 保留现有说明——文档自洽即可消除误报；
- 方案 B（工作量 60 分钟）：直接为四个领域各写一份占位模板（把 Step 2 的默认问题集复制为文件），使引用真实可解析，README 同步改为"已内置默认模板，教授表单到位后覆盖"。

### 🟢 P5 — 优化：description 触发句式标准化

将 "Use when starting a new client intake..." 改为 "Use when the user starts a new client intake, runs an intake interview, or needs a write-up of a new client's situation."——落入 SPEC §2.4 的标准信号清单，消除 §7-#5 的"带注通过"。工作量 ~2 分钟。

### 🟢 P6 — 优化：占位符大小写统一

L210 `[professor]` 与 L224 `[Professor]` 统一为 `[Professor]`（与 L219/225 风格一致）；同时顺手把 L36 的 generic-intake 注记在模板中定义插入点（如 `## Verification prompts` 前加一行 `[Generic intake note, if applicable — see supervisor guide section]`），一并解决 §4.1-#7 的歧义。工作量 ~5 分钟。

### 🟢 P7 — 优化：TOOL-01 缝隙的回归测试

修复 P2 后，在任意沙箱工作区跑一遍 check.py（`python check.py <workspace> <tool_log> <agent_output>`），确认 `Write.*\.md` 与 `legal-clinic:deadlines --add` 两条 script 检查在实际 agent 轨迹中可命中——确保评测管线与 body 契约闭环。工作量 ~20 分钟。

### 修复工作量汇总

| 优先级 | 项数 | 工作量 | 修复后预期 |
|---|---|---|---|
| 🔴 P0 | 1 | ~30 分钟 | 可执行性 7.0 → 8.5+ |
| 🟡 P1–P4 | 4 | ~60–90 分钟 | 逻辑一致性/对齐 9.0+；合规仍 12/12 |
| 🟢 P5–P7 | 3 | ~30 分钟 | 细节无瑕，达 🟢 A（9.3/10） |
| **合计** | **8** | **约 2–2.5 小时** | 推荐全部执行，P0 必须 |

---

## 附录: 审查过程记录

- **审查日期**: 2026-08-06。
- **被替换文件**: 旧 `REVIEW.md`（7 行 stub），原文：

```
# REVIEW: 034-client-intake

**2026-08-05** | Claude | Dossier: 🟢 典范

硬编码路径（~/.claude/plugins/config/claude-for-legal/legal-clinic/）+ /legal-clinic:client-intake slash command。Dossier 验证三必需节齐全、242 行、法律诊所 skill 家族的强样例。

**综合**: 🟢 A− (55/100) — 仅可移植性扣分
```

- **过程时间线**:
  1. `Glob D:\SkillIF\skill-experiment\complex-skills\034-client-intake\**` → 得 5 文件清单；
  2. `Glob SKILL-SPEC.md` 首查 `_shared` 失败（路径不存在）→ 重定位 `complex-skills\_shared\SKILL-SPEC.md` 与 `complex-skills-no-trigger\_shared\SKILL-SPEC.md`，取前者（带评测 corpus 的本体）；
  3. `Read` SKILL.md（243 行，全文）→ SCORING.yaml（159 行）→ check.py（73 行）→ references/intake-templates/README.md（15 行）→ 旧 REVIEW.md（7 行）；
  4. `Read` SKILL-SPEC.md（163 行）→ 逐项比对 12 项合规清单；
  5. `Grep skill-dossier.md` 定位 "034" 条目（L304–309）+ 读取前后上下文（033/035 对比参照）；
  6. `Read _shared\checker.py`（351 行）验证 check.py 的 import 与函数签名匹配、正则兼容性；
  7. 交叉核对：SCORING 17+3 条 ↔ Body 行号 ↔ check.py 实现；dossier 与旧 stub 结论 ↔ 本次审查结论；
  8. 写作本 REVIEW.md（替换旧 stub）。
- **验证记录**: description 长度约 310 字符（≤1024 ✅）；Body 行数 238（≤600 ✅）；目录共 5 文件；`references/intake-templates/` 内 4 个模板文件确认不存在（Glob 全量结果无 `.md` 除 README 外）。
- **方法论备注**: 本审查独立于 dossier 结论重新走查全部文件；dossier 的 🟢 评价在复核中成立，但本次新发现 4 处 dossier 未记录的问题（TL;DR 残片、TOOL-01 缝隙、免责声明缺口、模板文件缺失），故维持 🟢 A− 评级而非上调。
