# REVIEW: 297-startup-idea-validation

**审查日期**: 2026-08-06
**Skill 类型**: analysis — 创业 idea 启动前验证（9 维评分卡 + 验证阶梯 + 证据分级 GO/NO-GO 决策）
**Body 行数**: 111 行（SKILL.md 总 116 行 = frontmatter 4 行 + 空行 1 行 + body 111 行）
**参考文件数**: references/0, scripts/0, assets/0, data/0 — 无任何子目录
**审查方法**: 全量文件读取 + 字节级（xxd / cat -A / Python Unicode 审计）核验 + 语料库跨引用核验

---

## 1. 目录全量清单

```
297-startup-idea-validation/
├── SKILL.md        (116 行, 5,414 bytes, UTF-8 无 BOM, mtime 2026-08-05 19:51)
├── SCORING.yaml    (167 行, 9,510 bytes, mtime 2026-08-05 15:00)
├── check.py        ( 65 行, 1,876 bytes, mtime 2026-08-05 16:38)
└── REVIEW.md       (168 行, 7,616 bytes, mtime 2026-08-05 20:39, 本次被全文重写)
```

- 无 `references/`、`scripts/`、`assets/`、`data/` 子目录（`ls -la` 与 `find -type f` 双重确认，无隐藏文件）。
- 四个文件全部为干净 UTF-8：Python 逐一扫描 `\ufffd`（替换符）、`\u200b`（零宽空格）、`\ufeff`（BOM）、`\u200d`（零宽连接符）均无命中。
- 外部依赖：`check.py` 导入 `../_shared/checker.py`（已确认存在于 `D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py`，255 行）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name — ✅ 合规

- 值：`startup-idea-validation`；小写 + 连字符 ✓；长度 22 字符 ≤ 64 ✓；与目录名 `297-startup-idea-validation` 完全一致（NNN- 前缀为语料编号，name 本体匹配）✓。

### 2.2 description — ⚠️ 基本合规但含内部细节

全文（1 行，412 字符 ≤ 1024 ✓，YAML 双引号包裹）：

> "Startup idea validation with evidence-based GO/NO-GO decision framework. Use when validating a startup idea before building. Produces evidence-based GO/NO-GO decisions using a 9-dimension scorecard (problem, market, timing, moat, unit economics, founder-market fit, feasibility, GTM, risk), a validation ladder (interviews -> smoke test -> concierge/WoZ -> paid pilot), and riskiest-assumption-first experiments."

逐句分析：

| 句 | 内容 | 判定 |
|---|---|---|
| 第 1 句 | "Startup idea validation with evidence-based GO/NO-GO decision framework." | WHAT ✓ 第三人称 ✓ 具体（evidence-based GO/NO-GO）✓ |
| 第 2 句 | "Use when validating a startup idea before building." | WHEN ✓ 触发短语 ✓（"Use when..."为 SKILL-SPEC §2.4 认可的信号模板）|
| 第 3 句 | "Produces evidence-based GO/NO-GO decisions using a 9-dimension scorecard (…9 维列举…), a validation ladder (…4 级列举…), and riskiest-assumption-first experiments." | ⚠️ 内部工作流细节。9 个维度名与验证阶梯 4 步在 body 中已有完整表格（L43-53, L71-76），description 属冗余罗列。虽提供关键词（scorecard / validation ladder / GO/NO-GO），有助于检索匹配，但与 SKILL-SPEC §2.1"具体而非模糊"的意图一致度可接受，非硬违规 |

- 人称：无第一/第二人称 ✓；第 2 句的 "Use when" 为规范允许的触发模板，不算祈使违规 ✓。
- 跨 skill 路由：无 ✓。
- 无截断、无占位符、无 `…` 截断痕迹（旧 REVIEW 曾怀疑截断，字节级确认 412 字符为完整句号收尾）。
- 微小不一致：第 3 句用 "feasibility"、"risk"（裸名词），body 评分卡表格用 "Technical feasibility"、"Risk profile"，SCORING FMT-01 用 "technical feasibility"、"risk profile"。检索时若用户说 "risk profile" 与 description 的 "risk" 匹配度略降 — 影响轻微。

### 2.3 allowed-tools — ✅ 未声明（合规）

- 未使用 `allowed-tools` 字段。该字段为可选（SKILL-SPEC §1.2）。本 skill 是分析型（pattern: analysis），执行主要依赖 LLM 推理与阅读参考文件，不调用 Bash/Write 等工具，不声明工具白名单合理。
- 若未来需要 agent 读取参考文件，无需工具白名单（Read 为默认能力）；如需执行计算或写实验脚本可考虑 `Read, Write, Bash`，当前非必需。

### 2.4 其他 frontmatter 字段 — ✅ 合规

- 仅 `name` + `description` 两个键。SKILL-SPEC §1.3 的禁止键列表（metadata/license/version/agents/source/risk/tags/trigger/title/related-skills 等 39 项）全部未出现 ✓。
- 无 `paths`、`model`、`argument-hint` 等可选字段 — 不强制。

### 2.5 Frontmatter 语法 — ✅ 合规

- YAML 结构正确：`---` 开闭正常，`name:` 与 `description:` 键值格式正确。
- description 为双引号包裹单行（412 字符），内含 `->` 箭头与括号，无未转义的双引号，无双引号内冒号问题，可正常解析。
- 无 BOM 前缀（xxd 首字节为 `2d 2d 2d` 即 `---`）✓。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（全部标题与行数）

| 行号 | 标题/内容 | 行数 | 备注 |
|---|---|---|---|
| L6 | `# Startup Idea Validation`（H1） | 1 | |
| L8 | 引言段落 | 1 | "define hypotheses, collect evidence, score, decide" |
| L10-17 | `## Operating Principles (2026)` | 8 | 6 条原则 |
| L19-25 | `## Intake Checklist (Ask First)` | 7 | 5 项检查项 |
| L27-30 | `## Choose the Right Output` | 4 | **空表**（表头 3 列，0 数据行）|
| L32-39 | `## Workflow` | 8 | 步骤 1-6 |
| L41-61 | `## 9-Dimension Scorecard` | 21 | 权重表 9 行 + 阈值 4 条 + 悬空段落（L61）|
| L63-67 | `## Evidence Rules` | 5 | 3 条规则 |
| L69-76 | `## Validation Ladder (Default)` | 8 | 4 级阶梯表 |
| L78-86 | `## AI / Automation Notes (2026)` | 9 | 3 条 AI 专项验证项 |
| L88-100 | `## Integration Points` | 13 | Receives From 3 + Feeds Into 3 |
| L102-105 | `## Resources` | 4 | **空表** |
| L107-110 | `## Templates` | 4 | **空表** |
| L112-116 | `## Data` | 5 | 1 行指向不存在的 `data/sources.json` |

### 3.2 必需章节检查 — ❌ 3 项中 1 项通过

| SKILL-SPEC §3.1 必需章节 | 状态 | 详细分析 |
|---|---|---|
| **Workflow / Process** | ✅ 通过 | `## Workflow`（L32-39）6 个步骤完整：澄清目标 → 识别 RAT → 按 RAT-first 收集证据 → 最便宜可证伪测试 + 预注册阈值 → 9 维打分 + 弱证据降分 → 决策备忘。顺序逻辑合理 |
| **Output Format** | ❌ 不通过 | 两处致命缺口：(a) `## Choose the Right Output`（L27-30）是**空表** — 表头 3 列（If the user asks… / Produce… / Use…）但 0 数据行，agent 无法得知"什么请求 → 什么产出"的映射；(b) 决策备忘仅有 Workflow 步骤 6 的一句描述（verdict + why + what would change + next smallest reversible step），无任何输出模板/格式示例。得分卡表格虽列出 9 维与权重，但无每维打分刻度、无合成公式、无示例输出 |
| **Scope / Limitations** | ❌ 不通过 | **完全缺失**。无任何章节说明该 skill 不做什么（不做 build roadmap、不做完整商业计划书、不替代真实客户访谈、不保证 idea 成功、处理不了什么输入）。这直接导致：边界不清 → agent 可能越界产出 build 建议；且 SKILL-SPEC 12 项清单第 10 项硬性不通过 |

### 3.3 内容委托分析 — 🔴 委托比例高且委托目标全部缺失

- **Body 内联资产**（好）：9 维权重表（L43-53）、判定阈值（L55-59）、证据规则（L63-67）、验证阶梯表（L69-76）、intake 清单（L19-25）、操作原则（L10-17）。
- **委托外部文件**（6 处，全部指向不存在的文件）：
  - Workflow 步骤 3 → `references/riskiest-assumption-test.md`（L36）🔴
  - Workflow 步骤 5 → `references/validation-scorecard.md`（L38）🔴
  - L61 悬空段 → `validation-methodology.md`（评分 rubric 与校准）🔴
  - AI 注记第 3 条 → `assets/financial-modeling-calculator.md`（成本模型）🔴
  - AI 注记末尾 → `hypothesis-testing-guide.md`（AI 实验模式）🔴
  - Data 表 → `data/sources.json`（L116）🔴
- **委托缺口后果**：9 维评分卡的 **rubric（每维打分量表、锚点描述）完全外置且缺失** — body 中只有"维度 + 权重 + 一句衡量内容"，没有"怎么打 1-10 分 / 什么证据得什么分"。这正是逻辑断层（见 §4.4）的根源。RAT 测试模式、AI 实验模式同理全部缺失。
- Body 独立性评级：**低** — 名义上有 111 行实质内容，但 6 步工作流中 2 步（步骤 3、5）硬依赖缺失文件，评分环节实际不可完成。

### 3.4 节编号/标题层级 — ✅ 合规

- 无编号前缀（`##` 纯标题），层级一致：1 个 H1 + 12 个 H2，无 H3/H4 错位，无跳级。
- 标题命名风格统一（名词短语），无中英混杂。

### 3.5 Body 长度合规 — ✅ 通过

- Body 111 行 ≪ 600 行硬上限 ✓。按 SKILL-SPEC §3.2，analysis/process 类目标 ~200 行，当前 111 行偏短，且**大量篇幅被 3 张空表与悬空段落占据**，实际信息密度更低 — 这同时说明：完全有余量把外置的 rubric / RAT 模式 / 输出模板内联进 body（修复建议见 §13）。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- **步骤 1→2 衔接**：先澄清目标（intake checklist）再识别 RAT — 合理。RAT 定义（"the assumption that kills the business if wrong"）在 SCORING PROC-01 中给出，但 **SKILL.md body 本身未定义 RAT 的含义** — 步骤 2 只说"identify the riskiest assumption"，读者（agent）只能从命名猜含义。SCORING 有定义而 body 无定义，是明显的语义倒挂。
- **步骤 2→3 重叠**：步骤 2"识别 RAT 并选择验证阶梯测试"与步骤 3"按 RAT-first 方法收集证据（见 references 文件）"内容高度重叠 — 步骤 3 实质是把步骤 2 的 RAT 决策推给一个不存在的文件展开。若删除步骤 3 的死引用，步骤 2 已覆盖其职责。
- **步骤 4→5→6 衔接**：运行测试（4）→ 打分（5）→ 决策备忘（6），顺序正确。但步骤 5 的"打分"缺乏操作细节（见 §4.4），步骤 6 的"决策备忘"依赖步骤 5 产出总分，而总分因量表缺失无法计算 — 链条在步骤 5 处断裂。

### 4.2 内部矛盾扫描

| # | 矛盾/不一致 | 位置 | 说明 |
|---|---|---|---|
| 1 | **评分量表未定义 vs 0-100 阈值** | L43-53 vs L55-59 | 权重表给出 9 维权重（合计 100%），阈值是 80/60/40（0-100 区间）。但 body 从未声明每维的打分区间。若每维打 0-10 分，加权合计最大 = 10 分，80/60/40 阈值**数学上永远达不到**；若每维 0-100，需要加权平均公式但未说明。量纲缺口使 GO/NO-GO 判定在数学上不可执行 |
| 2 | RAT 有定义（SCORING）无定义（body） | L34 vs SCORING PROC-01 | 测评标准定义的概念，技能正文反而没有 |
| 3 | 路径前缀不一致 | L36/L38 `references/` 前缀 vs L61/L86 无前缀 | `validation-methodology.md`、`hypothesis-testing-guide.md` 裸文件名；即使文件存在，agent 也会困惑其根目录位置 |
| 4 | 术语不一致 | L3 vs L51/L53 | description 用 "feasibility"/"risk"，表格用 "Technical feasibility"/"Risk profile" |
| 5 | 空 Resources/Templates 节与 Data 节矛盾 | L102-116 | 声称有资源/模板/数据资产，实际只有 1 条指向死文件 |

### 4.3 示例/代码正确性

- 权重算术：15+12+10+12+15+8+10+10+8 = **100%** ✓ 正确（旧 REVIEW 已确认，本次复核无误）。
- 阈值边界完整性：80-100 GO / 60-79 CONDITIONAL / 40-59 PIVOT / <40 NO-GO — 实数全覆盖，79/80、59/60、39/40 边界无缝隙、无重叠 ✓。
- 验证阶梯顺序：interviews → smoke test → concierge/WoZ → paid pilot — 成本递增、证据强度递增，方向正确 ✓。
- 无代码示例（本 skill 无代码需求）— 不适用。

### 4.4 条件完整性 — 🔴 分支不完整

- **判定四分支的后续动作只给了一个**：CONDITIONAL 有明确后续（"validate RAT first"），但 GO（→ 直接进入下一个最小可逆步骤？）、PIVOT（→ 转向什么？改假设？换市场？）、NO-GO（→ 停止？记录教训？）均无下一步指引。一个以"decisions over inventories"为第一原则的 skill，3/4 的决策分支没有落地动作。
- AI 依赖分支（L78-86）有三项明确检查（数据权利/可靠性/成本）✓，但"非 AI 场景"无对应分支（SCORING DEC-03 以 judge 内嵌 fallback 处理，见 §10）。
- 弱证据降级（"downgrade scores when evidence is weak"）无降级幅度/规则（降 1 档？降一半？），依赖缺失的 rubric。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵 — 🔴 6/6 全部失效

| 引用 | 出现位置 | 目标文件状态 | 失效后果 |
|---|---|---|---|
| `references/riskiest-assumption-test.md` | L36（Workflow 步骤 3） | 🔴 不存在（无 references/ 目录） | 步骤 3 无内容可执行 |
| `references/validation-scorecard.md` | L38（Workflow 步骤 5） | 🔴 不存在 | 打分 rubric 缺失 — 最严重 |
| `validation-methodology.md` | L61 | 🔴 不存在 + 缺 references/ 前缀 | "deep scoring rubrics and calibration" 缺失 |
| `assets/financial-modeling-calculator.md` | L84（AI 注记） | 🔴 不存在（无 assets/ 目录） | AI 成本验证无工具 |
| `hypothesis-testing-guide.md` | L86 | 🔴 不存在 + 缺前缀 | AI 实验模式缺失 |
| `data/sources.json` | L116（Data 表，链接形式） | 🔴 不存在（无 data/ 目录） | "curated validation resources" 为空 |

- **全部 6 个文件引用均为死链接**。SKILL.md 文件引用规范（SKILL-SPEC §3.3：使用 skill 内相对路径）在"语法"上合规（无 `../`），但"引用的文件必须真实存在"这一前提全部落空。Agent 若遵循 "See references/..." 指令，将遭遇读取失败，或（更糟）自行编造内容。
- 与旧 REVIEW 的对照：旧 REVIEW 已正确识别 6 个失效引用 ✓（该部分结论成立，维持原判）。

### 5.2 不可见资源审计

- 除 6 个显式引用外，无隐式依赖的资源。
- 依赖语料库外部共享库 `_shared/checker.py` — 已确认存在（255 行），非死依赖。但注意：check.py 的运行正确性取决于 runner 的 sys.path 处理（`..\_shared` 相对于 skill 目录，存在即有效）。

### 5.3 Reference 文件全文审查

- **references/ 目录不存在，0 个文件。** 无任何 Reference 文件可审查。这是本 skill 参考完整性得分的决定性事实。

### 5.4 Scripts 文件全文审查

- **scripts/ 目录不存在，0 个文件。** 唯一"脚本"是根目录 `check.py`（65 行），属测评基础设施而非 skill 内容，在 §10 详审。
- check.py 质量评估（作为脚本本身）：
  - 结构合规：标准入口（`main()` + `if __name__`）、参数校验、JSON 输出、docstring 说明调用方式 ✓。
  - 与 `_shared/checker.py` 接口匹配：导入 `set_tool_log_path` / `set_agent_output`，均存在 ✓。
  - 功能：**0 项脚本检查** — 18 个 criterion 全部 `judge: llm`，`check()` 返回空 dict `{}`。docstring 明言 "Run all 0 script checks" — 诚实、无 bug，但意味着 run 结果对 18 项全为 `null`，测评完全依赖 LLM judge。
  - 小瑕疵：`main()` 中读文件后 `set_agent_output(f.read())` 与 `check()` 内再次调用 `set_agent_output` 重复，无害但冗余。

### 5.5 跨 Skill 引用检查 — 🔴 6 个引用中 4 个指向不存在的 skill

Integration Points（L88-100）共引用 6 个 skill，逐一在语料库（323 个目录）核验：

| 引用 | 语料库状态 |
|---|---|
| `startup-review-mining` | 🔴 不存在（全库搜索无此名） |
| `startup-trend-prediction` | ✅ 存在（275-startup-trend-prediction），且其 SKILL.md L370 反向引用本 skill — 双向一致 |
| `startup-competitive-analysis` | 🔴 不存在（最接近：256-competitive-landscape，名称不匹配） |
| `router-startup` | 🔴 不存在（全库无 router 类 skill） |
| `product-management` | 🔴 不存在（最接近：105-product-manager-toolkit） |
| `startup-business-models` | ✅ 存在（318-startup-business-models），其 SKILL.md L53 反向引用本 skill — 双向一致 |

- **4/6 的跨 skill 引用是虚构/失效的**。引用格式（散文式 `the \`xxx\` skill`）符合 SKILL-SPEC §3.3 ✓，但被引对象大半不存在 — agent 若按 "Feeds Into the router-startup skill" 去查找，找不到目标。
- 入向引用（其他 skill 引用本 skill）：275 L370、318 L53 格式一致、内容有效 ✓。
- 注：275 与 318 自身也引用了不存在的 router-startup / product-management / startup-competitive-analysis — 这是语料库级系统问题，但本 skill 的 4 个死引用必须自行修复。

### 5.6 嵌套重复/死文件

- skill 目录内无冗余/嵌套文件（仅 4 个必备文件）。
- `REVIEW.md` 本身位于 skill 目录内 — 语料实验惯例（审查产物），不会被当作 skill 内容加载，但建议评估流程确认 runner 注入时排除 REVIEW.md（本审查不越权修改流程）。
- 无重复内容：body 与 SCORING 之间无整段复制（SCORING 是测评问题化描述，属正常转写）。

### 5.7 其他资源文件

- 无。assets/、data/、templates/ 均不存在 — 而 body 的 Resources/Templates/Data 三个章节声称存在这些资产，全部落空（见 §6.5 占位符审计）。

---

## 6. 语法与格式质量

### 6.1 拼写错误 — ✅ 无

- 全文抽查：willingness-to-pay、time-to-value、concierge/WoZ、goalposts、pre-register、triangulate、defensibility、procurement 等专业术语拼写全部正确。无 typos。

### 6.2 语法错误 — ✅ 无

- 英文语法流畅、句式标准。无时态混乱、无残缺从句。

### 6.3 中英/葡英混杂 — ✅ 无

- 全英文 skill，无中文/葡萄牙语混入（非 ASCII 字符审计仅见 5 处排版字符，见 6.4）。

### 6.4 Markdown 格式破损 — ⚠️ 轻微

- 表格语法：6 张表全部格式正确。特别澄清：`Choose the Right Output` 表的分隔行为 `|---|---|---|`（3 列，与 3 列表头匹配）— **字节级确认（cat -A + xxd 双验证）**。旧 REVIEW.md 声称该行为 `|---|---|---|---|`（4 列破损）**系误读**，实际文件为格式良好的空表。空表结论不变，但"格式破损"不成立。
- 非 ASCII 排版字符（合法但风格不统一）：
  - L29 表头省略号 `…`（3 处，代替 `...`）
  - L47 `Clear “why now” and tailwinds`、L67 `“fact” vs “assumption”` — 弯引号，而全文其余引用为 ASCII 直引号 — 风格不一致。
  - L56-58 阈值用 en-dash `–`（`80–100` 等）— 可接受。
- L61 悬空段落："Deep scoring rubrics and calibration live in validation-methodology.md." 孤悬在 Scorecard 表与 Verdict 阈值之后、Evidence Rules 之前，无上下文引导句，排版上突兀。

### 6.5 占位符未填充 — 🔴 结构性占位

- **`Choose the Right Output` 表：表头完整但 0 数据行** — 全 skill 最严重的占位空缺（也是 SCOPE-01 失效的直接原因，见 §10.1）。
- **`Resources` 表：0 行** — "Resource" 章节无任何资源。
- **`Templates` 表：0 行** — "Template" 章节无任何模板。
- 这 3 张空表是典型的脚手架残留（模板骨架未填内容），与 memory 中"去模板脚手架"的规范化方向相悖。
- 无 `TODO`/`XXX`/`<placeholder>` 文本占位符（grep 未命中）。

### 6.6 截断内容 — ✅ 无

- 全文无截断（无半句话、无 `...` 收尾残缺、无悬挂代码块）。description 以句号完整收尾。

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 证据 |
|---|---|:---:|---|
| 1 | name: 小写+连字符 ≤64 字符、匹配目录 | ✅ | `startup-idea-validation`（22 字符） |
| 2 | description: 第三人称 WHAT+WHEN+KEYWORDS ≤1024 字符 | ✅ | 412 字符；WHAT/WHEN/关键词齐备 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | 全第三人称；"Use when"为规范模板 |
| 4 | description: 无 cross-skill routing | ✅ | 无"NOT for X, use Y" |
| 5 | description: 至少一个触发信号 | ✅ | "Use when validating a startup idea before building" |
| 6 | frontmatter: 无禁止键 | ✅ | 仅 name+description |
| 7 | body: ≤600 行 | ✅ | 111 行 |
| 8 | body: 有 workflow/process 章节 | ✅ | `## Workflow` 6 步骤 |
| 9 | body: 有 output format 章节 | ❌ | Choose the Right Output 空表；无输出模板 |
| 10 | body: 有 scope/limitations 章节 | ❌ | 完全缺失 |
| 11 | body: 无 ../ 跨目录路径 | ✅（语法）| 无 `../`；但 6 个内部相对引用全部指向不存在的文件（内容层失败） |
| 12 | 目录: NNN-kebab-case 无空格大写 | ✅ | `297-startup-idea-validation` |

**结果：12 项中 10 项通过，2 项硬性不通过（Output Format、Scope/Limitations）。** 合规得分（不计权）8.3/10。

---

## 8. 人机感评估

### 8.1 Emoji 审计 — ✅ 无

- SKILL.md / SCORING.yaml / check.py 全文件零 emoji（Unicode 范围扫描 + 目检）。旧 REVIEW 未用 emoji 的结论维持 ✓。

### 8.2 全大写/喊叫 — ✅ 无

- GO / NO-GO / PASS / FAIL / RAT / WoZ / ICP / GTM / ACV / ARPU 均为领域术语大写，非喊叫。无 `!!!`、无 `IMPORTANT` 滥用。

### 8.3 Persona 语气 — ✅ 专业务实

- 全文为操作手册式口吻："Prefer decisions over inventories"、"Separate evidence quality from confidence" — 每条原则都是可执行要求，非空洞口号。Mom Test 框架（behavioral commitment with cost）、RAT、WoZ 等概念引用准确，专业性强。

### 8.4 人机边界 — ✅ 良好

- 面向 agent 的指令清晰："Stay safe and ethical: no misrepresentation, respect ToS" 提供伦理约束；"avoid moving goalposts" 是具体的行为禁止。无拟人化、无情感操纵。

### 8.5 人称分析 — ✅ 一致

- Body 使用祈使句/陈述句指令 agent，属预期风格；无第一人称（无 "I" / "we"）。"you can defend"（L8 引言）是唯一的第二人称，出现在产品描述而非指令中，可接受。

### 8.6 表格太多 — ⚠️ 6 张表，3 张是空壳

- 有内容的 3 张表（Scorecard 权重表、Validation Ladder 表、Intake 清单）是决策树的正确表达（SKILL-SPEC §3.4 推荐表格/决策树）✓。
- 但 Resources / Templates / Choose the Right Output 3 张空表是纯噪声 — 空表对 agent 无信息量，只制造"存在资产"的假象，属于人机感扣分点。

---

## 9. 可执行性评估

### 9.1 独立可执行性 — 🔴 低

- 名义资产充足（权重表、阈值、阶梯、证据规则均在 body），但两个核心环节无法独立完成：
  1. **打分环节不可计算**：无每维打分量表与合成公式（§4.2 矛盾 #1），agent 无法产出满足阈值语义的分数。
  2. **工作流 6 步中 2 步指向死文件**（步骤 3、5），AI 分支 2 处死引用（L84、L86）。
- 结论：一个**刚完成规范化的"半成品"** — 骨架与决策框架存在，执行细节被外置且外置失败。

### 9.2 步骤可操作性 — ⚠️ 部分可操作

| 步骤 | 可操作性 | 说明 |
|---|---|---|
| 1 澄清目标 | ✅ | intake checklist 明确 5 项 |
| 2 识别 RAT | ⚠️ | RAT 无定义（body 内），只能凭术语推断 |
| 3 RAT-first 收集证据 | 🔴 | 依赖不存在的 references/riskiest-assumption-test.md |
| 4 最便宜测试 + 预注册 | ✅ | 自包含 |
| 5 9 维打分 | 🔴 | 无量表、无 rubric、死引用 |
| 6 决策备忘 | ⚠️ | 4 要素已列出，但无模板/格式；总分计算不通则 memo 的 verdict 无来源 |

### 9.3 工具依赖 — ✅ 无外部工具需求

- 不依赖任何 CLI/网络/API。若参考文件存在，仅需 Read。工具依赖维度无问题 — 但反过来说，skill 也未能提供任何可执行资产（脚本/数据）来辅助验证（如 smoke test 模板、sources.json 资源库），分析型 skill 不算硬伤。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

- **结构**：`total_items: 18`；实际 18 条（SCOPE 3 + PROC 7 + DEC 3 + FMT 2 + NEG 2 + QA 1 = 18）✓ 数量一致；`skill` 字段匹配 frontmatter name ✓；`pattern: analysis` 与 skill 属性一致（注意：旧 REVIEW 头部标注 "Skill 类型: process"，与 SCORING 的 `pattern: analysis` 不符 — 旧 REVIEW 另一处事实错误）。
- **全部 18 项 `judge: llm`**，check.py 脚本检查为 0 — 属合法设计（全 LLM 判定），但意味着无任何客观自动化防线。
- **可回溯性矩阵**（每条 criterion 能否在 body 找到支撑）：

| 测评点 | Body 支撑 | 判定 |
|---|---|---|
| SCOPE-01 输出类型匹配 | ❌ **无支撑** — 要求 agent 使用 "Choose the Right Output 表"映射 6 种输出（scorecard+verdict / RAT+test plan / hypothesis canvas / market sizing / unit economics+runway / comparative scorecard），**该表为空，且 6 种输出类型（hypothesis canvas、market sizing、unit economics+runway、comparative scorecard）在 body 中 0 出现**。agent 无从学起，LLM judge 只能测评 agent 的临场发挥而非 skill 遵从 | 🔴 最严重错配 |
| SCOPE-02 intake 清单 | ✅ L19-25 5 项全对应 | ✓ |
| SCOPE-03 不产出 build 计划 | ✅ L12 "decisions over inventories" + L17 原则 | ✓ |
| PROC-01 RAT 先于测试 | ⚠️ L34 有步骤但 RAT 无定义（SCORING 自带定义，body 缺） | 部分 |
| PROC-02 阶梯顺序 | ✅ L35 + L69-76 | ✓ |
| PROC-03 预注册阈值 | ✅ L37 | ✓ |
| PROC-04 弱证据降分 | ✅ L38 | ✓ |
| PROC-05 memo 4 要素 | ✅ L39 | ✓ |
| PROC-06 阈值应用 | ✅ L55-59（但量表缺失使"应用"不可计算，见 §4.4） | ⚠️ |
| PROC-07 阈值校准 | ✅ L16 | ✓ |
| DEC-01 证据分级 | ✅ L65-67 | ✓ |
| DEC-02 三角验证 | ✅ L66 | ✓ |
| DEC-03 AI 专项 | ⚠️ L78-86 三项齐全；但 question 内嵌 judge 指令 "Answer yes if the idea does not depend on AI" — 与其他 17 条 question 风格不一致（唯一带 fallback 条款者），可能诱导宽松判定 | ⚠️ |
| FMT-01 9 维权重 | ✅ L43-53 完全一致（权重逐一核对） | ✓ |
| FMT-02 证据链 fact/assumption | ✅ L67 | ✓ |
| NEG-01 弱证据不 GO + 不移动门柱 | ✅ L13, L17 | ✓ |
| NEG-02 不提前 build + 不误导/ToS | ✅ L17 | ✓ |
| QA-01 每维以决策结尾 + 阈值合成 | ⚠️ L12 有"每维以决策结尾"；但"阈值合成"依赖量表（缺失） | ⚠️ |

- **结论**：18 项中 16 项可追溯（2 项有缺口），但 SCOPE-01 这一入口级测评点建立在空表之上，且 18 项全部默认"技能文件资产完整"前提 — 测评框架无法发现 6 个死引用（没有对应检查项），存在系统性盲区。

### 10.2 Critical Failures 分析

| CF | 内容 | 评估 |
|---|---|---|
| CF-01 | 未打分 9 维/无证据链就出 GO/NO-GO → cap_to_0 | ✅ 合理；与 SCOPE-03/QA-01 呼应；但对一个"无法打分"（量表缺失）的 skill 而言，agent 为满足 CF-01 可能自造分数系统 — 测评测的是应急能力 |
| CF-02 | 测试后移动门柱强推 GO → cap_to_0 | ✅ 合理；与 NEG-01 呼应，可判定性强 |
| CF-03 | 跳过验证阶梯直接建议 build → cap_to_0 | ✅ 合理；与 NEG-02 呼应 |

- CF 设置整体合理、无遗漏。但**未覆盖"skill 内容缺陷"类失败**（死引用、空表）— 这是 SCORING 的固有盲区（测评对象是 agent 行为，不是 skill 质量），应在语料级质检中补位（本 REVIEW 即属此）。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**（skill-dossier.md L1134 🔴 清单 & L1158 🟠 清单）：
> "🔴 核心工作流文本严重乱码且步骤 3 缺失"（memory 原文两处："核心工作流文本乱码，步骤缺失" / "工作流乱码"）

**逐项验证结果 — 两项均不成立（当前文件状态）**：

| Dossier 声称 | 验证方法 | 结果 |
|---|---|---|
| 工作流文本乱码 | xxd 全文 hexdump + Python Unicode 审计（\ufffd/\u200b/\ufeff/\u200d）+ 非 ASCII 扫描 | ❌ 不成立。全文件干净 UTF-8，仅 5 处合法排版字符（…、弯引号、en-dash）。Workflow 段落（L32-39）字节级完整可读 |
| 步骤缺失（"步骤 3 缺失"） | 全文通读 + 行号核对 | ❌ 不成立。步骤 1-6 顺序完整（L34-39），步骤 3 存在于 L36 |

**判定**：dossier 记录与当前文件状态不符。最可能的原因：(a) dossier 审查（2026-08-05）早于 SKILL.md 最后修改（mtime 2026-08-05 19:51），文件在 dossier 之后被修复过（Workflow 补全/重写），dossier 未更新；(b) dossier 误记。**以字节证据为准：当前 SKILL.md 无乱码、步骤完整。** 另外，dossier 将 297 同时登记在 🔴 与 🟠 两份清单（L1134 + L1158），属重复登记，建议清理。

**Dossier 遗漏的问题（本 REVIEW 新增发现）**：
1. **6 个文件引用全部失效**（§5.1）— 旧 REVIEW 已覆盖，dossier 未记录。
2. **3 张空表**（§6.5）— 旧 REVIEW 覆盖，dossier 未记录。
3. **评分量表/量纲矛盾**（§4.2 #1）：阈值 0-100 vs 未定义量表 — 新旧 REVIEW 均未识别，**本审查新增**。
4. **SCORING SCOPE-01 基于空表、6 种输出类型无 body 支撑**（§10.1）— 新增。
5. **4/6 跨 skill 引用指向不存在的 skill**（§5.5）— 旧 REVIEW 误判为"合规有效"（其 L96-97 声称 "符合 SKILL-SPEC §2.5" 且未核验存在性），**本审查修正**。
6. **RAT 在 body 无定义**（§4.1）— 新增。
7. **判定四分支仅 CONDITIONAL 有后续动作**（§4.4）— 新增。
8. **check.py 零脚本检查**（§5.4/§10.1）— 旧 REVIEW 未评估，新增。
9. **旧 REVIEW 自身的 3 处事实错误**：(i) 称 Choose the Right Output 表分隔行 4 列破损 — 实际 3 列格式良好（字节级证实）；(ii) 头部标注 Skill 类型 "process" — SCORING.yaml 为 `pattern: analysis`；(iii) 引用路径风格判定含未核验断言。

---

## 12. 综合评分 — 8 dimensions weighted

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | name/语法/触发全过；description 第 3 句内部细节冗余（-1.5）、术语与 body 不一致（-0.5） |
| Body 结构完整 | 4/10 | 10% | 0.40 | Workflow/原则/权重表/阶梯俱佳；Output Format 空表（-3）、Scope 缺失（-2）、3 张空表（-1） |
| 逻辑一致性 | 5/10 | 20% | 1.00 | 框架自洽、权重 100%、阈值边界完整；但量表/量纲矛盾使总分不可计算（-3）、分支不完整（-1）、步骤 2/3 重叠 + RAT 无定义（-1） |
| 参考完整性 | 2/10 | 15% | 0.30 | 6/6 引用全死、4/6 跨 skill 引用不存在、0 参考文件；仅跨引用格式合规与 275/318 双向链接可加分 |
| 语法格式 | 9/10 | 10% | 0.90 | 无拼写/语法/混杂/截断；弯引号与省略号风格不一致（-0.5）、悬空段落（-0.5） |
| 规范合规 | 8/10 | 15% | 1.20 | 12 项过 10 项；Output Format 与 Scope/Limitations 两项硬性失败（-2） |
| 人机感 | 8/10 | 10% | 0.80 | 专业务实、零 emoji、零喊叫、伦理约束好；3 张空表是噪声（-2） |
| 可执行性 | 3/10 | 10% | 0.30 | 步骤 3/5 死引用、打分不可计算、输出无模板；仅步骤 1/4 与 AI 分支可操作 |
| **加权总分** | | | **5.70/100** | |

**Rating: 🟠 C（57/100）**

评分解读：决策框架本身是语料库中质量较高的（9 维权重、阈值、验证阶梯、Mom Test 证据规则 — 方法论扎实），但**"框架成型、资产全空"**的结构性缺陷（死引用 + 空表 + 量表缺失）使其在实测中不可执行。57 分对应 🟠 C：修复成本低（详见 §13），修复后有望达 🟡 B+。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（不修则 skill 不可执行，共 5 项）

**1. 定义每维打分量表与合成公式（解决量纲矛盾）**
- 位置：SKILL.md L41-61（9-Dimension Scorecard 节）。
- 问题：L55-59 阈值为 0-100 区间，但 L43-53 未声明量表。若 0-10 分制，加权最大仅 10 分，80/60/40 阈值数学上不可达；0-100 分制则需明确公式。且 rubric 被外置到不存在的 validation-methodology.md。
- 修复：在 Scorecard 节新增一行说明 + rubric 内联，例如："Score each dimension 0–100 using the rubric below. Composite = Σ(weight × score). Thresholds: 80–100 GO, 60–79 CONDITIONAL (validate RAT first), 40–59 PIVOT, <40 NO-GO."，随后给出每维的 3 档锚点（如 0-40 weak / 40-70 partial / 70-100 strong evidence），并删除 L61 悬空段（或将其改写为指向真实的 rubric 锚点）。
- 后果：不修则 PROC-06 / QA-01 / CF-01 在实测中全部塌陷 — agent 无法计算总分，GO/NO-GO 无数学依据。

**2. 填充 `Choose the Right Output` 空表（L29-30）**
- 问题：SCOPE-01 要求 agent 用此表把请求映射到 6 种输出，表却 0 行；body 中 "hypothesis canvas / market sizing / unit economics + runway / comparative scorecard" 从未出现。
- 修复：按 SCORING SCOPE-01 的 6 种输出补全映射行，建议：
  `| 完整 idea 验证 | 9-dimension scorecard + verdict | ## 9-Dimension Scorecard |`
  `| 最危险假设是什么 | RAT + test plan | Workflow steps 2-4 |`
  `| 假设梳理/验证设计 | hypothesis canvas | … |`（3 行省略，共 6 行）
- 后果：不修则 agent 对"验证我的 idea"之外的请求（如"帮我算市场规模"）无任何输出指引，SCOPE-01 测评失真。

**3. 消除 6 个死引用 — 二选一：内联或补文件**
- 位置：L36（references/riskiest-assumption-test.md）、L38（references/validation-scorecard.md）、L61（validation-methodology.md）、L84（assets/financial-modeling-calculator.md）、L86（hypothesis-testing-guide.md）、L116（data/sources.json）。
- 推荐方案 A（内联，因 body 仅 111 行 ≪ 600）：把 RAT 判定模式（步骤 3 的内容）、9 维 rubric 锚点（步骤 5 的内容）、AI 实验要点内联进 body；删除 L84/L86/L116 三处引用；删掉 Data 节或改为真实数据。
- 推荐方案 B（补文件）：创建 `references/riskiest-assumption-test.md`、`references/validation-scorecard.md`、`references/hypothesis-testing-guide.md`、`data/sources.json`（内容必须真实，不能空壳）。
- 无论选哪种：统一路径前缀（L61/L86 必须加 `references/`），全部用 skill 内相对路径。
- 后果：不修则 agent 遇 "See X" 必读取失败或编造内容；5.1 矩阵 6 项全红维持。

**4. 新增 Output Format 节（满足 SKILL-SPEC §3.1）**
- 位置：Scorecard 节之后新增 `## Output Format`（或 `## Decision Memo`）。
- 修复：给出决策备忘的明确模板，例如：
  ```
  ## Decision Memo
  - Verdict: GO / CONDITIONAL / PIVOT / NO-GO (+ composite score)
  - Why: evidence summary by dimension (fact vs assumption)
  - What would change the decision: …
  - Next smallest reversible step: …
  ```
  并补一句证据链呈现格式（link + capture month，呼应 L67）。
- 后果：不修则 12 项合规清单第 9 项永久失败，且 agent 产出无固定形状，FMT-01/02 判定困难。

**5. 新增 Scope / Limitations 节（满足 SKILL-SPEC §3.1）**
- 位置：Integration Points 之前（或文末 Metadata 前）新增 `## Scope / Limitations`。
- 修复：明确列出（建议 5 条）：(a) 本 skill 不做 build roadmap / 功能规划（呼应 SCOPE-03）；(b) 不做完整商业计划书与深度财务建模；(c) 打分基于证据而非直觉，缺乏行为证据时以 CONDITIONAL/NO-GO 收口；(d) 不替代真实客户访谈与合规审查；(e) 验证结论仅代表当前证据状态，会随证据更新（呼应 NEG-01）。
- 后果：不修则 12 项清单第 10 项失败，且 agent 边界无约束。

### 🟡 重要缺陷（影响质量与准确性，共 5 项）

**6. 修正跨 skill 引用（L88-100）**
- 问题：6 个引用中 4 个（startup-review-mining / startup-competitive-analysis / router-startup / product-management）在语料库不存在。
- 修复：改指真实存在的同类 skill（如 275-startup-trend-prediction、318-startup-business-models 保留，startup-competitive-analysis → 256-competitive-landscape，product-management → 105-product-manager-toolkit），或删除无法对应者。保持散文式 `the \`xxx\` skill` 格式（合规）。
- 后果：不修则 agent 追踪输入/输出流时 2/3 目标不存在，"Feeds Into / Receives From" 地图半虚构。

**7. 补齐判定四分支的后续动作（L55-59）**
- 修复：GO → 进入下一个最小可逆步骤（如扩量测试/预销售）；PIVOT → 重述假设、更换最大风险维度再测；NO-GO → 记录失败证据与教训，停止投入。与 Operating Principles"decisions over inventories"呼应。
- 后果：不修则 3/4 决策分支无落地动作，QA-01"each dimension ends with a next action"精神贯彻不完整。

**8. 在 body 定义 RAT（L34 附近）**
- 修复：在 Workflow 步骤 2 内联一句定义："RAT = the assumption that, if wrong, kills the business — the cheapest test that can falsify it comes first."（与 SCORING PROC-01 对齐）。
- 后果：不修则 agent 对术语的理解依赖推理而非指令。

**9. check.py 增加文件存在性脚本检查**
- 位置：check.py。
- 修复：利用 `_shared/checker.py` 的 `file_exists` 对 6 个引用文件（或修复后实际存在的文件集）加 6 项脚本检查；同时可加 `file_contains` 校验 SKILL.md 包含 "## Scope" 与 "## Output Format" 节标题 — 为技能质量设自动防线。
- 后果：不修则测评对"死引用/缺章节"零检出（18 项全 LLM，SCOPE-01 依赖的空表无人拦截）。

**10. 术语与风格统一**
- (a) description 第 3 句与 scorecard 表的维度命名统一（feasibility → technical feasibility，risk → risk profile）；(b) 清理 3 张空表：Resources/Templates 若 30 天内不填实质内容则删除整节（空节比无节更误导）；(c) L47/L67 弯引号改直引号；(d) DEC-03 question 的 "Answer yes if..." fallback 条款删除，改为与其他 question 同构的措辞（如 "Does the agent, when the idea depends on AI, explicitly validate …? If the idea does not depend on AI, this item is vacuous." — 措辞上把 fallback 移出 question 或全库统一）。

### 🟢 优化建议（锦上添花，共 4 项）

**11. description 精简**：第 3 句删除 9 维与 4 级阶梯的完整罗列，压缩为 "…using a weighted 9-dimension scorecard and a riskiest-assumption-first validation ladder"（节省约 200 字符，信息量不变）。
**12. 步骤 2/3 合并**：Workflow 从 6 步压缩为 5 步（步骤 3 并入步骤 2），消除重叠。
**13. 证据链格式示例**：Evidence Rules 节补 1 行示例（如 `[TAM source](URL) — capture 2026-07 — assumption`），让 FMT-02 有模板可循。
**14. dossier 登记更新**：将 297 从 🔴 清单移入 🟠 或标记"已修复待复评"，并删除 L1158 的重复登记。

### 修复工作量估计

| 批次 | 内容 | 工作量 |
|---|---|---|
| 🔴 1-5 | 量表+公式内联、填 Choose 表、内联/建 5 文件、Output/Scope 两节 | 2.5-4 小时（若选内联方案约 2.5h） |
| 🟡 6-10 | 跨引用修正、分支后续、RAT 定义、check.py 6 项检查、术语统一 | 1-1.5 小时 |
| 🟢 11-14 | description 精简、步骤合并、示例、dossier 更新 | 0.5 小时 |
| **合计** | | **4-6 小时** |

优先执行 🔴 1 与 🔴 2（逻辑与入口），其次 🔴 3（引用），最后 🔴 4/5（章节）— 建议一次性完成，避免再次出现"修一半"状态。

---

## 附录: 审查过程记录

| 步骤 | 操作 | 证据/结论 |
|---|---|---|
| 1 | Glob `**/*` + `find -type f` + `ls -la` | 目录仅 4 文件，无子目录、无隐藏文件 |
| 2 | Read SKILL.md 全文（116 行） | 逐行分析（§2-4, 6） |
| 3 | Read SCORING.yaml 全文（167 行） | 18 项 criterion + 3 CF 全量核对（§10） |
| 4 | Read check.py 全文（65 行） | 0 脚本检查判定（§5.4, §10） |
| 5 | Read 旧 REVIEW.md 全文（168 行） | 逐项复核：3 处事实错误已修正（§11） |
| 6 | references//scripts//assets//data/ 目录 | 不存在 — 无法读取，已按"0 文件"审查（§5.3-5.4, 5.7） |
| 7 | xxd SKILL.md 全程 hexdump + cat -A 关键行 | 字节级验证：无乱码/BOM/零宽字符；Choose 表分隔行确为 3 列 `|---|---|---|`（推翻旧 REVIEW 的 4 列破损说）|
| 8 | Python Unicode 审计 4 文件 | \ufffd/\u200b/\ufeff/\u200d 全部无命中 |
| 9 | awk 行长扫描 | 最长行 L3 description（427 字符）；8 处 >100 字符行，无异常 |
| 10 | Python 计数 | description 412 字符；body 111 行；权重和 100% 复核 |
| 11 | 语料库跨引用核验（323 目录） | 6 个 integration skills 中 4 个不存在；275/318 反向引用格式一致 |
| 12 | grep 入向引用 | 275 L370、318 L53 引用本 skill（双向一致性确认） |
| 13 | Read `_shared/SKILL-SPEC.md`（161 行） | 12 项合规清单对照基准（§7） |
| 14 | Read `_shared/checker.py`（255 行） | check.py 依赖核验，file_exists 等可用性确认（§13 #9 依据）|
| 15 | Grep memory/skill-dossier.md | 297 记录两处（L1134 🔴 + L1158 🟠）；claims 与当前文件状态不符（§11）|

**审查限制说明**：(a) 未运行真实 agent 评测（本审查为静态深度审查）；(b) `_shared/checker.py` 与 SKILL-SPEC 位于 skill 目录之外，仅作背景阅读，未计入本 skill 资产；(c) dossier 声称的乱码无法在当前文件版本复现，已按字节证据下结论并标注可能性解释。

---

## 变更记录

- 2026-08-06: 全文重写（旧 REVIEW 168 行 → 本版 370+ 行）。新增：量纲矛盾、SCOPE-01 空表错配、跨 skill 死引用、check.py 零检查、dossier 核验推翻、旧 REVIEW 3 处事实错误修正。评级维持红档附近但理由重构：🔴 D(42) → 🟠 C(57)，因框架质量高于纯 D 档，核心问题集中在可补资产而非方法论。
