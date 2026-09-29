# REVIEW: 076-investor-brief-writer

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 引导式访谈 + 内容生成型（investor one-pager / executive summary / email brief 撰写）
**Body 行数**: 493 行
**参考文件数**: references/8, scripts/0, assets/0, html-templates/0（被引用但目录不存在）
**总文件数**: 11

---

## 1. 目录全量清单

```
076-investor-brief-writer/
├── SKILL.md (493 行)
├── SCORING.yaml (199 行)
├── check.py (73 行)
└── references/
    ├── 8-critical-guidelines-for-this-skill.md (18 行)
    ├── html-editorial-template-reference.md (31 行)
    ├── html-output-verification.md (33 行)
    ├── integration-with-other-skills.md (16 行)
    ├── quality-checklist-before-finalizing.md (15 行)
    ├── step-4-generate-comprehensive-investor-brief.md (52 行)
    ├── step-5-quality-review-iteration.md (14 行)
    └── step-6-save-next-steps.md (7 行)
```

该 skill 属于中重型 skill（11 个文件，8 个 reference 文件）。Body 的 STEP 编号跨文件延续：SKILL.md 含 STEP 0-3，references/ 含 STEP 4-6，形成一条"桥接式"工作流。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `investor-brief-writer`，全小写+连字符 ✓
- 长度: 21 字符，远低于 64 字符限制 ✓
- 匹配目录名 `076-investor-brief-writer` ✓

### 2.2 description

原文:
> "Create compelling investor one-pagers and email briefs that capture attention and get meetings. Distill your pitch into scannable, high-impact documents with traction-focused cold emails and distribution strategy. Use when the user asks to write an investor one-pager or executive summary, draft cold outreach emails to investors, or create follow-up and distribution materials to get meetings."

逐句分析:

**第 1 句** (WHAT): "Create compelling investor one-pagers and email briefs that capture attention and get meetings."
- 隐含主语 "the skill"，第三人称描述，与 SKILL-SPEC §2.6 的 Good 示例风格一致 ✓
- 明确了产物类型（one-pager / email brief）和核心目标（capture attention, get meetings）✓

**第 2 句**: "Distill your pitch into scannable, high-impact documents..."
- ⚠️ **第二人称泄露** — "your pitch" 违反 SKILL-SPEC §2.3 第三人称禁令。应改为 "the user's pitch" 或直接省略。
- 该句同时承担 KEYWORDS 职责（scannable, high-impact, cold emails, distribution strategy）✓

**第 3 句** (WHEN): "Use when the user asks to write an investor one-pager or executive summary, draft cold outreach emails to investors, or create follow-up and distribution materials to get meetings."
- 含规范触发短语 "Use when the user asks to" ✓
- 触发场景具体（one-pager、executive summary、cold outreach emails、follow-up/distribution materials）✓

总体评价: WHAT/WHEN/KEYWORDS 三要素齐全，触发条件明确。唯一缺陷是第 2 句的第二人称 "your"。字符数约 430，远低于 1024 上限 ✓。

修改建议:
```
description: "Create compelling investor one-pagers and email briefs that capture attention and get meetings, distilling the pitch into scannable, high-impact documents with traction-focused cold emails and distribution strategy. Use when the user asks to write an investor one-pager or executive summary, draft cold outreach emails to investors, or create follow-up and distribution materials to get meetings."
```

### 2.3 allowed-tools
- 该 skill 未声明 `allowed-tools` 字段。SKILL-SPEC §1.2 将其列为可选字段，不构成违规。该 skill 的主要执行方式是对话式访谈 + 文本生成，对工具依赖低（Read references 即可），缺失影响不大 ⚠️（轻微）。

### 2.4 其他 frontmatter 字段
- 仅 `name` 和 `description` 两个字段，无 `argument-hint`，无禁止字段 ✓
- YAML 分隔符 `---` 配对正确（L1/L4）✓
- description 无特殊转义问题 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# investor-brief-writer (L6)                          — 标题
**Mission** (L8)                                       — 使命陈述，~2 行
## STEP 0: Pre-Generation Verification (L13-45)       — 占位符校验清单（23 个占位符，3 组）
## STEP 1: Detect Previous Context (L49-63)           — 上游上下文检测（3 档）
## STEP 2: Context-Adaptive Introduction (L67-91)     — 分档引导话术（3 套引用块）
## STEP 3: Questions (L95-481)                         — 15 个问题，~390 行
  ### Brief Format & Purpose (L97-138)                — BF1 格式 / BF2 受众
  ### Content Structure (One-Pager) (L142-266)        — CS1-CS8（elevator→ask）
  ### Content Structure (Email Brief) (L270-318)      — EB1 冷邮件
  ### Design & Formatting (L322-361)                  — DF1 设计
  ### Distribution & Follow-Up (L367-452)             — DU1 分发 / DU2 CRM
  ### Implementation Roadmap (L456-481)               — IR1 时间线
## Reference Files (L485-493)                          — 8 个 reference 的导航列表
```

### 3.2 必需章节检查

| 章节 | 状态 | 问题 |
|------|:----:|------|
| Workflow/Process | ⚠️ | STEP 0-3 在 body，STEP 4-6 在 references/，靠末尾导航列表衔接；STEP 0 的"生成前校验"实际放在生成步骤之前（逻辑倒置，详见 §4.1） |
| Output Format | ❌ | body 无任何 Output Format 节；输出规格（HTML 模板、验证清单）全部委托给 references/html-* 两个文件，而其中依赖的 html-templates/ 目录不存在（详见 §5.3） |
| Scope/Limitations | ❌ | 完全缺失——无任何"不做什么/何时不用"的章节，也无 NEG 护栏（详见 §4.4） |

### 3.3 内容委托分析

- STEP 4（生成）、STEP 5（质量复查）、STEP 6（保存）三个执行步骤整体下沉到 references/，body 只保留 STEP 0-3（验证 + 上下文 + 提问）。委托声明共 8 条（L487-493 导航列表），占 body 比例极低 ✓。
- 但委托存在结构性风险：body 的标题是 "STEP 0" 到 "STEP 3"，reference 文件又是 "STEP 4" 到 "STEP 6"——编号体系跨文件延续，agent 若不读 reference 导航列表，会以为工作流止于 STEP 3（提问）而无生成动作。
- **输出格式完全依赖缺失文件**：html-editorial-template-reference.md 要求 "MUST read" 的 3 个 html-templates/ 文件均不存在（详见 §5.3），这是本次审查发现的最高优先级问题。

### 3.4 节编号/标题层级
- 标题层级: # → ## → ### → ####（如 Email Body Structure 下的 Paragraph 1-4），无跳级 ✓
- STEP 编号: 0-6 连续（0-3 在 body，4-6 在 references）✓，但 STEP 0 的语义顺序倒置
- 问题编号体系: BF1/BF2, CS1-CS8, EB1, DF1, DU1/DU2, IR1 —— 多套前缀并存但互不冲突，可读性可接受

### 3.5 Body 长度合规
- 实际 493 行，pattern=process 目标约 200 行，hard limit 600 行
- 远超 process pattern 目标（主要被 15 个问题的示例/公式/话术占据），但低于硬限制 ✓
- 建议: DF1（设计）、IR1（时间线）两部分与简报内容生成关系较弱，可下沉 references

---

## 4. 逻辑一致性深度审查

### 4.1 STEP 0 倒置问题（dossier 已指出，确认为真实缺陷）

STEP 0 标题为 "Pre-Generation Verification"，内容是逐项勾选 23 个 `{{PLACEHOLDER}}` 是否已填充。但:

- 该步骤位于 STEP 1（上下文检测）、STEP 2（引导）、STEP 3（15 个问题）**之前**——在收集任何内容前，不可能完成"verify all placeholders are populated"
- 真正的生成动作在 references/step-4 中，STEP 0 与生成步骤之间隔着完整的访谈流程
- 正确顺序应为: STEP 1-3 收集内容 → STEP 4 生成 → **验证占位符** → STEP 5 质量复查

修复方向: 将 STEP 0 改为两阶段——访谈前仅做"占位符提醒"（告知 agent 生成时必须填满），生成后做真正的逐项校验；或整体移到 STEP 4 之后。

### 4.2 BF1 格式选择未驱动分支（dossier 已指出，确认为真实缺陷）

BF1 让用户选择 One-Pager / Executive Summary / Email Brief 三种格式，但后续 14 个问题**无条件分支**:

- 用户选 Email Brief 后，CS1-CS8（one-pager 专属内容：elevator pitch、team 等）仍被无差别询问
- 用户选 One-Pager 后，EB1（冷邮件全文）仍被询问——虽然后续 DU1 分发策略需要邮件，但 skill 未说明这种复用关系
- 唯一的分支暗示是标题 "Content Structure (One-Pager)" 与 "Content Structure (Email Brief)"，但无任何"若选择 X 则回答 Y 组"的指令

修复方向: 增加格式→问题组的映射表（决策树）:

| 用户选择 | 必答问题 | 可跳过 |
|----------|----------|--------|
| One-Pager | BF2, CS1-CS8, DF1, DU1, DU2 | EB1（仅需 subject 思路） |
| Executive Summary | BF2, CS1-CS8, DF1, DU1, DU2 | EB1 |
| Email Brief | BF2, CS2, CS3, CS5, CS8, EB1, DU2 | CS1, CS4, CS6, CS7, DF1 |

### 4.3 占位符与问题的映射缺口（dossier 指出 `{{EXEC_SUMMARY_CARDS}}`，实际缺口更大）

STEP 0 共列 23 个占位符（9 个 Score Banner + 12 个 Content Section + 2 个 Chart Data）。逐一映射到 15 个问题:

| 占位符 | 来源问题 | 状态 |
|--------|----------|:----:|
| COMPANY_NAME, ROUND_NAME, RAISE_AMOUNT | CS8（+用户自我介绍） | ✅ |
| MRR, GROWTH_RATE, CUSTOMERS | CS5 | ✅ |
| TAM | CS4 | ✅ |
| TARGET_INVESTORS | IR1（50-100 名单） | ⚠️ 间接 |
| ONEPAGER_SECTIONS | CS1-CS8 汇总 | ✅ |
| TRACTION_CARDS | CS5（2-4 指标） | ⚠️ 卡片形式未明确 |
| TEAM_CARDS | CS7（2 创始人+1 关键人） | ✅ |
| EMAIL_SUBJECT, EMAIL_BODY | EB1 | ✅ |
| DISTRIBUTION_CARDS | DU1 | ✅ |
| **EXEC_SUMMARY_CARDS** | **无任何问题覆盖**（"4 exec summary cards: format, audience, distribution, differentiators"——format/audience 有 BF1/BF2，但 differentiators 从未被询问） | 🔴 缺口 |
| **EMAIL_TEMPLATES**（3 模板） | DU1 提供 warm intro + post-meeting 示例，**follow-up 模板不存在**——而 8-critical-guidelines 第 6 条明确要求 "Send 2-3 follow-ups" | 🔴 缺口 |
| **CONTACT_INFO** | 无任何问题询问联系方式 | 🔴 缺口 |
| **REVENUE_LABELS / REVENUE_DATA** | 无任何问题询问 12 个月 MRR 历史——CS5 只取当前指标，而 QA-01 与 html-output-verification 强制要求 "MRR progression over 12 months" 折线图 | 🔴 缺口（图表数据无输入路径） |
| TAGLINE | CS1（elevator pitch 近似） | ⚠️ 间接 |
| NEXT_STEPS | IR1 时间线 | ⚠️ 间接 |

结论: 23 个占位符中 4 个无任何问题支撑（EXEC_SUMMARY_CARDS、EMAIL_TEMPLATES 的 follow-up、CONTACT_INFO、REVENUE_LABELS/DATA），3 个仅间接覆盖。**评估标准 QA-01 强制要求的营收图表，在访谈中根本没有数据采集环节**——agent 只能自行编造或向用户追加提问，前者触碰 CF-01，后者流程上无支持。

### 4.4 缺少数值护栏（NEG 规则不在 body 中）

- NEG-02 / CF-01（不得编造 traction/metrics，只能使用用户提供或明确标注的数字）只存在于 SCORING.yaml，**body 与 8 个 reference 文件均无对应指令**
- 对一个面向投资人的交付物而言，编造 MRR/市场规模是严重的信任破坏行为；skill 要求产出大量数字（CS4 市场、CS5 指标、CS8 金额）却无一字禁止虚构
- 修复方向: 在 body 增加一条显式规则——"Never invent traction metrics or market numbers. Use only figures the user provides, or clearly mark estimates as assumptions."

### 4.5 其他逻辑不一致

- **PDF vs HTML**: step-6-save-next-steps.md 说 "Save the investor brief (**PDF**) and email templates"，而 STEP 0 / html-output-verification.md / QA-01 的产物均为 HTML 报告。输出形态定义前后矛盾。
- **"One at a Time" 声称 vs 15 个问题**: STEP 3 标题为 "Questions (One at a Time, Sequential)"，但一份简报访谈要连问 15 个问题（BF1-BF2, CS1-CS8, EB1, DF1, DU1-DU2, IR1），且无中途检查点、无"何时终止访谈进入生成"的判定条件（STEP 5 的 Iterate? 是生成后而非生成前）。对目标为"快速拿到 meeting"的轻量任务偏重。
- **IR1 与 NEXT_STEPS 重叠**: IR1（Implementation Roadmap）是 Week 1-3 的执行计划，与 NEXT_STEPS 占位符（"6 prioritized next step items"）和 step-6 的内容三方重叠，职责不清。
- **"9 sections" 未定义**: html-output-verification.md 要求 "All 9 sections present"，但 step-4 的 Section 1-7 只有 7 个编号节，one-pager 又是 6-8 节——"9" 这个数字未映射到任何命名清单（勉强可对应验证清单中的 9 个内容条目，但无显式说明）。

### 4.6 示例/模板正确性
- CS1/CS2/CS3/CS6/CS8 的示例（Stripe、Figma、Notion、BuildFlow）具体且自洽，同一虚构公司 BuildFlow 贯穿 CS2-CS8 与 EB1 示例，叙事一致 ✓
- DU2 的 CRM 示例表（Jane Doe/Sequoia、John Smith/Andreessen、Alice Johnson/First Round）是**示例数据**，但 skill 未标注"这些是示例行，不得输出为真实名单"——与 OUT-03（要求 5-10 行真实名单）和 NEG-02 存在张力
- STEP 2 的 Ideal Context 话术含 `[X]`、`[$X]`、`[Z]` 未填充占位符，agent 直接引用会输出原始标记

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

SKILL.md L487-493 导航列表引用的 8 个 reference 文件**全部存在** ✓:

| 引用路径 | SKILL.md 行号 | 是否存在 | 文件行数 | 内容匹配度 |
|----------|:------------:|:--------:|:--------:|:---------:|
| references/8-critical-guidelines-for-this-skill.md | L487 | ✅ | 18 | 匹配 — 8 条军规 |
| references/html-editorial-template-reference.md | L488 | ✅ | 31 | 匹配 — HTML 模板用法 |
| references/html-output-verification.md | L489 | ✅ | 33 | 匹配 — 输出验证清单 |
| references/integration-with-other-skills.md | L490 | ✅ | 16 | 匹配 — 上下游衔接 |
| references/quality-checklist-before-finalizing.md | L491 | ✅ | 15 | 匹配 — 终检清单 |
| references/step-4-generate-comprehensive-investor-brief.md | L492 | ✅ | 52 | 匹配 — 生成大纲 |
| references/step-5-quality-review-iteration.md | L493 | ✅ | 14 | 匹配 — 复查问题 |
| references/step-6-save-next-steps.md | L494 | ✅ | 7 | 匹配 — 保存与后续 |

### 5.2 不可见资源审计

**html-editorial-template-reference.md 引用了 3 个不存在于本 skill 目录的文件**（L9/L14/L19）:

```
html-templates/VERIFICATION-CHECKLIST.md       🔴 不存在（无 html-templates/ 目录）
html-templates/base-template.html              🔴 不存在
html-templates/investor-brief-writer.html      🔴 不存在
```

该文件以 "**CRITICAL**: When generating HTML output, you MUST read and follow the skeleton template files" 开头，将模板读取设为强制动作，但目标文件整体缺失。这是 skill 中最严重的问题——**生成环节的核心依赖不存在**。agent 只有两条出路:（a）跳过 MUST read 指令自行构建 HTML（违反明确指令）；（b）按 html-output-verification.md 的验证清单手工拼装（清单本身足够详细，可作为可行回退）。无论哪条，skill 的既定执行路径都无法走通。

### 5.3 Reference 文件全文审查

**8-critical-guidelines-for-this-skill.md (18 行)**: 8 条原则质量高（"Traction gets meetings"、"The ask is a meeting, not money"、"Warm intros have 10x higher response rate"）。第 6 条 "Send 2-3 follow-ups spaced 5-7 days apart" 与 §4.3 发现的 follow-up 模板缺失直接冲突——原则要求发 follow-up，内容资产里却没有 follow-up 模板。第 4 条 "Personalize every cold email" 与 EB1 的通用模板结构之间缺少个性化指令桥接。

**step-4-generate-comprehensive-investor-brief.md (52 行)**: 定义了 7 个输出 Section（Executive Summary / One-Pager Content / Email Brief / Design & Formatting / Distribution & Follow-Up / Investor List Building / Next Steps），与 body 的问题分组一一对应 ✓。但这是"内容大纲"而非"输出格式"——未定义 HTML 结构、样式、图表配置（那些在缺失的 html-templates 中）。Section 1 的 "Distribution strategy (warm intros, cold outreach, post-meeting follow-ups)" 与 body DU1 重复列举，篇幅可压缩。

**step-5-quality-review-iteration.md (14 行)**: 6 个质量复查问题与 quality-checklist-before-finalizing.md 高度重叠（scannability、traction、ask 三处几乎逐字重复），两文件可合并。

**step-6-save-next-steps.md (7 行)**: 最短的 reference。内容与 body 的 IR1（时间线）和 NEXT_STEPS 占位符三方重叠；"Save the investor brief (PDF)" 的 PDF 表述与全 skill 的 HTML 产物矛盾（见 §4.5）。

**html-editorial-template-reference.md (31 行)**: 见 §5.2。另注意其指令 "Replace all `{{PLACEHOLDER}}` markers" 使用泛化占位符，与 body STEP 0 的 23 个具名占位符词汇表脱节。合并标记 `{{SKILL_SPECIFIC_CSS}}`、`{{CONTENT_SECTIONS}}`、`{{CHART_SCRIPTS}}` 在 body 任何位置都未定义——与 `{{EXEC_SUMMARY_CARDS}}` 同属未定义词汇（dossier 只点名了后者）。

**html-output-verification.md (33 行)**: 内容本身是可靠的输出验收清单（结构 4 项 / 图表 1 项 / 内容 9 项 / 视觉 5 项），且与 QA-01 的判定模式（#0a0a0a、#10b981、Chart.js）一致。但文件末尾 L34 的 "**End of Skill**" 是脚手架残留标记（corpus 的 clean_scaffolding.py 正是为此类残留而生），应删除。

**integration-with-other-skills.md (16 行)**: 见 §5.4。

**quality-checklist-before-finalizing.md (15 行)**: 12 项清单与 step-5 及 body 内容三方重叠，建议与 step-5 合并。

### 5.4 跨 Skill 引用检查

SKILL.md 与 references 中共提到 10 个上游/下游 skill 名称，逐一对照 corpus 实际目录:

| 引用名称 | 出现位置 | corpus 中是否存在 |
|----------|----------|:-----------------:|
| investor-pitch-deck-builder | STEP 1/2, integration | ✅ (045) |
| financial-model-architect | STEP 1/2, integration | ✅ (075) |
| customer-persona-builder | integration | ✅ (266) |
| fundraising-strategy-planner | integration | ✅ (317) |
| problem-validation-study | STEP 1/2, integration | 🔴 不存在 |
| metrics-dashboard-designer | STEP 1/2, integration | 🔴 不存在 |
| product-positioning-expert | integration | 🔴 不存在 |
| competitive-intelligence | integration | 🔴 不存在（corpus 有 256-competitive-landscape） |
| investor outreach | integration (downstream) | 🔴 不存在（近似: 015-outreach-specialist） |
| post-meeting follow-ups | integration (downstream) | 🔴 不存在 |

**10 个跨 skill 引用中 6 个指向不存在的 skill**。STEP 1 的上下文检测逻辑（Ideal/Partial/No 三档）依赖 "problem-validation-study" 和 "metrics-dashboard-designer" 两个不存在的技能——agent 按此检测将永远落在 "No Context" 档，STEP 1/2 的 Iideal/Partial 分支实际不可达。无 `../` 文件路径引用，形式上合规，但名称级引用错位使上下文复用机制失效。

### 5.5 嵌套重复/死文件检查
- 无 self-nested 目录 ✓
- 无 .gitkeep、无冗余文件 ✓
- "End of Skill" 脚手架标记 1 处（html-output-verification.md L34）

---

## 6. 语法与格式质量

### 6.1 拼写错误
- 全文无拼写错误。专业术语（scannable, due diligence, term sheet, unit economics）拼写正确 ✓

### 6.2 语法错误
- 无明显语法错误。句式以祈使/陈述混合为主，均通顺 ✓
- "Processed $50M in transactions in 12 months" 重复 "in" 属可接受的英语习惯用法，不记为错误

### 6.3 中英/葡英混杂
- 全文纯英文，无中英或葡英混杂 ✓

### 6.4 Markdown 格式破损
- 无孤立代码围栏、无断裂列表 ✓
- 8 个 reference 文件均以 `---` 正常分隔 ✓
- 唯一的格式残留是 html-output-verification.md L34 的 "**End of Skill**"

### 6.5 占位符未填充
- **STEP 2 话术中的 `[X]`、`[$X]`、`[Z]`**（L74-76）: 意为"agent 从上下文提取后填入"，但无说明文字，直接引用会输出原始标记——需加 "(fill from detected context)" 或改为 `[fill from investor-pitch-deck-builder output]`
- **`{{EXEC_SUMMARY_CARDS}}`、`{{SKILL_SPECIFIC_CSS}}`、`{{CONTENT_SECTIONS}}`、`{{CHART_SCRIPTS}}`**: 词汇表未闭合（见 §4.3、§5.3）
- 无 `TODO`/`FIXME`/`TBD` ✓
- 问卷中的 `[Your Answer]` 类占位符是**有意设计的答案槽**，不属于缺陷 ✓

### 6.6 截断内容
- SKILL.md L493 以 navigation 列表正常结束 ✓
- 所有 reference 文件以合理内容结束，无截断 ✓

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` 的 12 条规则:

1. **name 匹配目录名**: ✅ `investor-brief-writer` 匹配 `076-investor-brief-writer`
2. **description 第三人称**: ⚠️ 整体第三人称，但第 2 句 "Distill **your** pitch" 第二人称泄露
3. **description 含触发短语**: ✅ "Use when the user asks to..."
4. **description ≤1024 字符**: ✅ 约 430 字符
5. **无禁止 frontmatter 字段**: ✅ 仅 name、description
6. **body ≤600 行**: ✅ 493 行
7. **Workflow/Process 节存在**: ✅ STEP 0-3（body）+ STEP 4-6（references），编号连续
8. **Output Format 节存在**: ❌ body 无输出格式节；输出规格委托 references/html-*，其依赖的模板文件缺失（§5.2）
9. **Scope/Limitations 节存在**: ❌ 完全缺失——最常见的规范缺口，本 skill 亦未幸免
10. **无跨 skill 文件路径引用**: ✅ 无 `../` 路径；但 6/10 个名称级跨 skill 引用指向不存在的技能（§5.4，规范未禁止但功能失效）
11. **allowed-tools 格式正确**: N/A（未声明，可选字段）
12. **路径仅指向本 skill 目录内**: ⚠️ `references/xxx.md` 均在本目录内 ✓，但 html-templates/ 三个路径指向本目录内**不存在**的子目录

**合规率: 9/12 ✅，2 项明确违规 + 1 项功能失效**

### 违规详情

**违规 1 — 缺少 Scope/Limitations 节（规则 9）**: 无任何 "What This Skill Does NOT Do"。对投资材料生成类 skill，至少应声明: 不编造财务数字、不替代法务/募资顾问、不保证投资人回复、不管理已发送的邮件（CRM 仅为建议）。

**违规 2 — 缺 Output Format 节（规则 8）**: 严格说输出规格散落在 references/html-output-verification.md（足够详细），但 body 层面无输出节，且该规格依赖缺失模板。建议 body 增加 "## Output" 摘要节（HTML 报告 + 6 指标 score banner + 营收折线图 + 9 项内容清单），细节保留在 reference。

**功能失效 — 名称级跨 skill 引用**: 6 个上游/下游 skill 名称在 corpus 中不存在，STEP 1 的上下文检测分支因此不可达。

---

## 8. 人机感评估

### 8.1 Emoji 审计
- 全文（含 references）**零 emoji**。与 dossier 的评语一致——引导式采访角色，无装饰性符号 ✓

### 8.2 全大写/喊叫式语言
- 无 `STOP!`、`MANDATORY`、`CRITICAL` 等喊叫式语言 ✓（"**CRITICAL**" 仅出现在 html-editorial-template-reference.md 的模板读取指令处，属功能性强调，可接受）
- "MUST read"（html 模板）使用 1 次，属指令强度而非情绪化 ✓

### 8.3 Persona 语气分析
整体语气: **引导式内容教练 + 募资顾问**。三层语气结构清晰:

- **Skill 指令层**: 祈使式流程描述（"Verify all placeholders are populated"、"Choose one"）——中性专业
- **用户话术层**（STEP 2 引用块、EB1/DU1 邮件示例）: 第一人称的招募邮件话术（"I'm reaching out because you've invested in B2B SaaS..."）——恰当地模拟创始人语气，dossier 也肯定了这一层的第一人称使用
- **知识提示层**: 每个问题前的公式（"Elevator Pitch = 1-2 sentences..."）和示例（Stripe/Figma/Notion）——教学感强，降低用户填写门槛

代表性语气证据:
- "Traction gets meetings."（8-critical-guidelines L3）→ 干脆的领域洞察
- "If investors need to scroll, you've lost them."（L7）→ 口语化但有说服力
- "Do you have 15 minutes this week or next for a quick intro call?"（EB1 示例）→ 教科书式的 meeting ask

语气评价: 非常适合面向创始人的采访型 skill——不端着、不废话，示例具体到可以直接模仿。

### 8.4 人机边界分析
本 skill 的交互设计亮点: STEP 2 的 "**Proceed with this data?** [Yes/Start Fresh]" 把数据复用决策显式交给用户 ✓；STEP 5 的 "**Iterate?** [Yes — refine X / No — finalize]" 提供明确的迭代出口 ✓。

**但存在一个严重边界缺口**（§4.4）: skill 要求 agent 产出大量数字型内容（TAM、MRR、增长率、融资金额），却**没有一条"不得编造数据"的护栏**。投资人材料场景下，编造指标的危害被 SCORING.yaml 的 CF-01 认可（cap_to_0），但该护栏只存在于评测端，未进入 skill 本体。8 条军规里也全是"应该做"（Lead with traction...），没有一条"绝不"。

### 8.5 人称分析
- 第二人称（you/your）: 集中出现在用户话术引用块与邮件模板中——合理（这些话是 agent 替创始人说给投资人听的）✓
- 第一人称（I）: 出现在 STEP 2 脚本（"I found outputs from..."）与邮件示例（"We're BuildFlow..."）——合理的角色扮演 ✓
- 第三人称: skill 指令层 ✓
- 判定: 人称层次分明，唯一越界是 description 的 "your pitch"（§2.2）

### 8.6 表格使用评估
- body 仅 1 张表格（DU2 的 CRM 状态表），是结构化数据表的合理应用 ✓
- 其余信息用分层列表呈现，符合"用户不喜欢表格"的偏好 ✓

---

## 9. 可执行性评估

### 9.1 独立可执行性
假设 agent 只拿到 SKILL.md（不主动探索目录）:

- **内容收集阶段**: 完全可以执行——15 个问题每个都有公式、示例和答案槽，agent 可以立刻开始引导式访谈 ✓
- **上下文复用阶段**: 部分失效——STEP 1 依赖的两个上游 skill（problem-validation-study、metrics-dashboard-designer）不存在，Ideal/Partial 分支在真实环境中不可达（除非用户会话中确实存在同名 skill 产物）
- **生成阶段**: 无法按指令执行——html-editorial-template-reference.md 要求 MUST read 的 3 个模板文件缺失。agent 只能违反指令自行拼装，或退回用 html-output-verification.md 的清单手工构建（后者可行，但相当于绕开 skill 自己的执行路径）
- **打分: 5/10** — 访谈环节优秀，生成环节的依赖断裂使端到端流程不可信

### 9.2 步骤可操作性

| 步骤 | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| STEP 0 | Pre-Generation Verification | 🔴 | 在内容产生之前执行"验证占位符已填充"——无物可验 |
| STEP 1 | Detect Previous Context | 🟡 | 依赖 2 个不存在的上游 skill，Ideal/Partial 分支不可达 |
| STEP 2 | Context-Adaptive Introduction | 🟡 | 话术含 [X]/[$X]/[Z] 未填标记 |
| STEP 3 | 15 个问题 | 🟢 | 公式+示例+答案槽俱全；但无格式条件分支、无访谈终止判定 |
| STEP 4 (ref) | Generate Comprehensive Brief | 🔴 | 大纲齐全但 HTML 模板缺失 |
| STEP 5 (ref) | Quality Review & Iteration | 🟢 | 6 个问题 + 明确迭代出口 |
| STEP 6 (ref) | Save & Next Steps | 🟡 | 与 IR1/NEXT_STEPS 三方重叠；PDF 表述与 HTML 产物矛盾 |

### 9.3 工具依赖合理性
- 主要工具: Read（读 references 导航列表）、无脚本依赖、无第三方服务 ✓
- 输出为单文件 HTML（含 Chart.js CDN）——无本地构建链，合理 ✓
- 外部依赖: html-templates/*（缺失）是唯一的硬依赖，且是本次审查的核心问题

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖
SCORING.yaml 定义 22 个 criteria（SCOPE-01~03, PROC-01~12, OUT-01~04, NEG-01~02, QA-01），覆盖 7 个类别。check.py 实现其中 3 个 script 检查（SCOPE-03, PROC-09, QA-01），其余 19 个为 LLM judge——与 SCORING 的 `judge: script` 标注一致 ✓。

| 类别 | 数量 | 与 SKILL.md 的一致性 |
|------|:----:|------|
| SCOPE（3 项） | 3 | SCOPE-01（格式+受众确认）↔ BF1/BF2 ✓；SCOPE-02（上下文复用）↔ STEP 1/2 ✓；SCOPE-03（无占位符残留）↔ STEP 0 意图 ✓ |
| PROCESS（12 项） | 12 | PROC-01~08 ↔ CS1-CS8 一一对应 ✓；PROC-09~11 ↔ EB1 ✓；PROC-12 ↔ DU1/DU2 ✓ |
| OUTPUT（4 项） | 4 | OUT-01/02 ↔ DF1 ✓；OUT-03 ↔ DU2/IR1 ✓；OUT-04 ↔ step-5 ✓ |
| NEGATIVE（2 项） | 2 | NEG-01 ↔ 30 秒可扫读 ✓；NEG-02 ↔ **body 中无对应指令**（§4.4） |
| QA（1 项） | 1 | QA-01 ↔ html-output-verification.md 图表/主题 ✓ |

覆盖完整性: 良好——SKILL.md 与 references 的每个主要环节都有对应 criterion，PROC-01~08 与 CS1-CS8 的编号对齐是设计亮点。

### 10.2 Script 检查的质量问题

**PROC-09（script）**: 正则 `(?i)(200[-– ]?300 words|\bHook\b|\bTraction\b|\bAsk\b|4 paragraphs)` 是**词汇存在性启发**——agent 只要在输出里写出 "Hook"/"Traction"/"Ask" 字样（哪怕放在目录里）即通过，无需邮件真有 4 段结构。一个 500 字、无 meeting ask 的烂邮件只要提到 "Ask" 一词也能得分。建议改为 LLM judge（与 PROC-01~08 一致），或要求输出同时匹配 "meeting" + "15 minutes" 等 ask 特征。

**QA-01（script）**: 正则 `(?i)(new Chart|type:\s*['"]line['"]|#0a0a0a|#10b981|chart\.js)` 是 **5 项 OR 组合**——输出中只要出现任意一项（比如仅仅提到 "#10b981"）即通过，无法保证图表、主题、配色同时达标。建议至少要求 "new Chart"（或 chart.js）与 "#0a0a0a" 两项 AND 组合。

**SCOPE-03（script）**: `output_not_contains('\{\{\w+\}\}')` 设计合理——直接对应用户最关心的"别把占位符交给我" ✓。注意 email 模板中的 `[Your Name]`（方括号）不受影响，判定准确。

### 10.3 Critical Failures 分析
- **CF-01**（编造指标 → cap_to_0）: 合理且必要，但护栏只在评测端（§4.4）
- **CF-02**（无 traction 或无 ask → cap_to_0）: 合理，与 PROC-05/PROC-08 呼应
- **CF-03**（邮件 >300 字或缺 meeting ask → cap_to_0）: 合理，与 8 条军规第 3/5 条一致

评价: 三个 CF 都对应募资场景的核心失败模式，设计良好。缺一个与格式分支相关的 CF（如"用户选 email brief 却只给 one-pager"），但该问题更接近流程指导而非致命失败。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md（memory: `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`）中 076 条目:

> **076-investor-brief-writer**
> - **逻辑**: Workflow 内部一致，但 STEP 0 "pre-generation verification" 排序在生成步骤之前，BF1 格式选择后 CS1-CS8 问题无差别询问。
> - **语法**: 干净可读，示例丰富；占位符 `{{EXEC_SUMMARY_CARDS}}` 在任何问题节中都未定义。
> - **人机感**: 引导式采访角色，引用的 "I found outputs from investor-pitch-deck-builder..." 脚本赋予了恰当的第一人称。
> - **合规**: Description 第三人称含触发，workflow/output 存在，无跨 skill 文件路径，body ~493 行。
> - **总评**: 🟡 扎实的引导式简报 skill，但倒置的 STEP 0/占位符逻辑需理顺。

### 与本次审查的对照

| dossier 发现 | 本次审查结论 |
|--------------|--------------|
| STEP 0 排序倒置 | ✅ 确认（§4.1），并补充修复方案 |
| BF1 后 CS1-CS8 无差别询问 | ✅ 确认（§4.2），并量化（15 问题、无分支表） |
| `{{EXEC_SUMMARY_CARDS}}` 未定义 | ✅ 确认（§4.3），且扩展——实际有 4 个占位符无问题支撑（+EMAIL_TEMPLATES 的 follow-up、CONTACT_INFO、REVENUE_LABELS/DATA） |
| 引导式采访 + 恰当第一人称 | ✅ 确认（§8.3） |
| workflow/output 存在、无跨 skill 路径 | ⚠️ 部分修正——无 `../` 路径 ✓，但 **6/10 个名称级跨 skill 引用指向不存在的技能**（§5.4），且 **html-templates/ 3 个模板文件整体缺失**（§5.2，dossier 未记录，本次审查新增） |
| 🟡 总评 | 同意 🟡，但严重度上浮——生成环节依赖缺失使评级从"微调可解决"上移至"结构性修复" |

dossier 的评级方向正确，但受当时审查深度所限未发现最严重的两个问题（缺失模板目录、失效的上游 skill 引用）。本次审查将其显性化。

---

## 12. 综合评分

### 维度评分

**Frontmatter 合规 (8/10, 权重 10%)**: name/trigger/长度全部合规，唯一瑕疵是 description 第 2 句 "your pitch" 第二人称泄露。

**Body 结构完整 (6/10, 权重 10%)**: 访谈工作流完整（15 个问题的公式+示例+答案槽），但缺 Output Format 节和 Scope/Limitations 节；493 行远超 process pattern 的 200 行目标。

**逻辑一致性 (6/10, 权重 20%)**: STEP 0 倒置、格式选择无分支、23 个占位符中 4 个无采集路径、营收图表数据无输入、PDF/HTML 矛盾、follow-up 模板缺失。

**参考完整性 (5/10, 权重 15%)**: 8/8 导航引用存在，但 html-templates/ 3 个 MUST-read 文件缺失（生成环节断裂）；6/10 跨 skill 名称指向不存在的技能（上下文复用机制失效）；"End of Skill" 脚手架残留。

**语法格式 (8/10, 权重 10%)**: 纯英文、无拼写错误、markdown 干净；STEP 2 话术 [X]/[$X] 未填标记。

**规范合规 (8/10, 权重 15%)**: 12 条规则中 9 条完全合规，2 条违规（缺 Scope、缺 Output 节），1 项功能失效（跨 skill 名称）。

**人机感 (8/10, 权重 10%)**: 零 emoji、三层语气结构清晰、Proceed/Iterate 出口设计好；但缺"不得编造数据"的负向护栏，对募资材料是信任风险。

**可执行性 (6/10, 权重 10%)**: 访谈阶段 🟢 可直接执行；生成阶段因模板缺失不可按指令执行；STEP 1 分支因上游 skill 缺失而不可达。

**加权总分: 6.7/10 = 67/100**

### 评级: 🟡 B- (67/100)

可用但有明显缺陷。访谈/内容框架质量扎实（问题设计、示例、军规都专业），但生成环节依赖缺失 + 逻辑倒置 + 护栏缺失使其无法以当前形态参与严格评估。修复后可达 🟢。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复，影响端到端可用性）

**F-1: html-templates/ 目录整体缺失——生成环节的核心依赖断裂**
- 位置: references/html-editorial-template-reference.md L9/L14/L19
- 问题: 该文件以 "**CRITICAL**: ... you MUST read and follow the skeleton template files" 开头，要求按顺序读取 3 个文件（VERIFICATION-CHECKLIST.md、base-template.html、investor-brief-writer.html），但本 skill 目录下不存在 html-templates/ 子目录，3 个文件全部缺失。agent 无法遵守 MUST-read 指令，只能自行拼装 HTML。
- 修复选项（择一）:
  - **选项 A（推荐，工作量 ~150 行）**: 在 skill 目录下创建 `html-templates/`，依 html-output-verification.md 的规格自足实现——`base-template.html`（#0a0a0a 暗色底、#1a1a1a 容器、#10b981 emerald 强调、Chart.js v4.4.0 引入）、`investor-brief-writer.html`（6 指标 score banner、exec summary cards、one-pager preview、traction cards、team cards、cold email preview、3 套邮件模板、investor table、revenue chart 脚本）、`VERIFICATION-CHECKLIST.md`（即 html-output-verification.md 的 CSS 模式权威清单）。模板中的 `{{PLACEHOLDER}}` 使用 STEP 0 的 23 个具名占位符。
  - **选项 B（轻量，工作量 ~40 行）**: 删除 html-editorial-template-reference.md，将 html-output-verification.md 升级为自包含的 HTML 生成规格（内联 CSS 模式、图表配置、区块结构），使 agent 无需外部文件即可产出符合 QA-01 的 HTML。
- 不修复的后果: agent 在生成环节必然偏离指令；QA-01 只能靠运气通过；skill 端到端不可执行。

**F-2: 缺少 Scope/Limitations 节（违反 SKILL-SPEC §3.1 规则 9）**
- 位置: SKILL.md — 需在 "## Reference Files" 之前新增 section
- 修复: 新增 "## Scope & Limitations" 节，建议内容:

```markdown
## Scope & Limitations

This skill writes investor one-pagers, executive summaries, and cold outreach emails.
It does NOT:

- **Invent data.** Never create traction metrics, market sizes, or financial figures
  that the user did not provide. When a number is an estimate, label it as an
  assumption (e.g., "TAM: $40B (industry estimate, to verify)").

- **Act as legal, securities, or fundraising counsel.** It drafts marketing
  materials. Terms, cap tables, and offering details are the user's responsibility.

- **Manage the outreach pipeline.** It provides CRM templates and status
  categories, but does not send emails, schedule meetings, or track responses.

- **Replace a pitch deck.** A one-pager is a distillation; if the user has no
  deck or data room, recommend investor-pitch-deck-builder and the data-gathering
  skills before drafting.

- **Guarantee investor responses.** Meeting rates depend on fit and timing;
  the skill optimizes the materials, not the outcome.

Do not use this skill when the user needs a full business plan, a fundraising
pitch deck, or formal financial modeling — those belong to other skills.
```

- 不修复的后果: agent 无边界意识，可能在缺数据时编造数字（CF-01 触发）、越界承诺募资效果

**F-3: 修复 STEP 1 上下文检测依赖的不存在 skill**
- 位置: SKILL.md L49-63、L70-78；references/integration-with-other-skills.md
- 问题: STEP 1 的 Ideal/Partial 档依赖 problem-validation-study 与 metrics-dashboard-designer 两个不存在的 skill，实际运行永远落入 "No Context" 档，STEP 2 的两套话术成为死代码；integration-with-other-skills.md 另引用不存在的 product-positioning-expert、competitive-intelligence、"investor outreach"、"post-meeting follow-ups"。
- 修复: 名称对齐 corpus 实际目录（或改用泛指描述）:

| 当前引用 | 建议修正 |
|----------|----------|
| problem-validation-study | 删除或改为泛指 "user's prior validation work" |
| metrics-dashboard-designer | 删除或改为泛指 "user's metrics dashboards" |
| product-positioning-expert | 删除（可用 256-competitive-landscape 替代竞争分析） |
| competitive-intelligence | 改为 "competitive-landscape"（256） |
| investor outreach | 改为 "outreach-specialist"（015） |
| post-meeting follow-ups | 删除或描述为 prose（"post-meeting follow-up materials"） |

- 不修复的后果: 上下文复用机制失效，STEP 1/2 约 40 行内容形同虚设；跨 skill 名称误导 agent 寻找不存在的资源

### 🟡 重要缺陷（建议修复）

**I-1: STEP 0 顺序倒置——移回生成步骤之后**
- 位置: SKILL.md L13-45
- 当前: "Before generating HTML output, verify all placeholders are populated" 位于内容收集之前
- 修复: 拆分为两个动作:
  1. **STEP 0（保留在当前位置，改名 "STEP 0: Placeholder Registry"）**: 只声明 23 个占位符词汇表及含义，作为后续收集的路线图，不要求"验证"
  2. **新增 STEP 4b（放在 step-4 生成之后）: "Verification"** —— 对生成结果逐项检查 23 个占位符均已替换，无 `{{...}}` 残留（对应 SCOPE-03 检查）
- 不修复的后果: agent 在无内容可验的阶段执行验证，产生无意义动作；或忽视该步骤导致占位符残留

**I-2: BF1 格式选择后缺少条件分支——补映射表**
- 位置: SKILL.md L99-118（BF1）之后
- 修复: 在 BF1 答案槽后插入格式→问题组映射表（见 §4.2 的表格），并加一条指令: "Ask only the question groups for the selected format(s). If the user selects multiple formats (e.g., one-pager + email brief), ask the union, but skip DF1 unless a designed one-pager is needed."
- 不修复的后果: 15 个问题无差别轰炸，访谈冗长，且产出内容与所选格式不匹配（例如选了 email brief 却生成完整 one-pager 结构）

**I-3: 补齐 4 个无采集路径的占位符 + 修复合集缺口**
- 位置: SKILL.md STEP 3
- 修复:
  1. 新增 **Question CS9: What makes you different?**（differentiators）——喂给 `{{EXEC_SUMMARY_CARDS}}` 的第四张卡（现有 BF1 格式、BF2 受众、DU1 分发 + 新增不同化）
  2. 新增 **Question CS10: What are your contact details?**（email/website/location）——喂给 `{{CONTACT_INFO}}`
  3. 在 EB1 后新增 **follow-up email 模板**（8 条军规第 6 条要求 2-3 次 follow-up 却无模板资产）——同时补齐 `{{EMAIL_TEMPLATES}}` 三件套（warm intro ✓ 已有、post-meeting ✓ 已有、follow-up 🔴 缺失）;给出 5-7 天间隔的 follow-up 话术示例
  4. 新增 **Question CS11: What is your 12-month revenue history?**（month labels + MRR values）——`{{REVENUE_LABELS}}`/`{{REVENUE_DATA}}` 的唯一合法来源；若无历史数据，允许用户提供后 12 个月预测并标注 "projected"
- 不修复的后果: 生成时 4 个区块只能靠 agent 编造（触碰 CF-01）或留白（触碰 SCOPE-03）；强制性的 12 个月营收图无数据可用

**I-4: 统一 PDF/HTML 产物表述**
- 位置: references/step-6-save-next-steps.md L4
- 当前: "Save the investor brief (PDF)"
- 修复: 改为 "Save the investor brief as **HTML** (the skill's primary output; export to PDF if the user requests)"——与 STEP 0、html-output-verification.md、QA-01 的 HTML 定位一致
- 不修复的后果: agent 交付形态摇摆，用户与评测端对产物预期不一致

**I-5: 将"不得编造数据"护栏写入 body（NEG-02 从评测端前移到指令端）**
- 位置: SKILL.md STEP 3 开头（或新 Scope 节，见 F-2）
- 修复: 在 CS4/CS5/CS8 三个数字密集问题前加统一规则: "All numbers (TAM, MRR, growth, raise amount) must come from the user. If the user does not know a figure, ask once, then mark the field as `[assumption]` — never invent."
- 不修复的后果: 无护栏的 agent 在数据缺口下大概率编造——对投资人材料是信任灾难，CF-01 只能事后惩罚无法事前预防

**I-6: 弱化 PROC-09 与 QA-01 的词汇存在性判定**
- 位置: SCORING.yaml L101-103（PROC-09）、L183-186（QA-01）
- 修复: PROC-09 改为 LLM judge（与 PROC-01~08 同源，问题: "Is the cold email 200-300 words with 4 paragraphs (Hook → Company → Traction → Ask) and a meeting request?"）；QA-01 的正则改为 AND 语义或拆成两个 criteria（一个查 chart（`new Chart` 或 `chart\.js`），一个查主题（`#0a0a0a` 且 `#10b981`））
- 不修复的后果: 评分可被低质量输出"刷词"通过，评测区分度失真

**I-7: STEP 2 话术中的 [X]/[$X]/[Z] 未填标记**
- 位置: SKILL.md L74-76
- 修复: 改为 "Problem statement ([fill from problem-validation output or ask])" 等带来源说明的写法，或删除方括号直接写 "[values from detected context — ask user to confirm]"
- 不修复的后果: agent 原样引用话术时向用户输出原始标记

### 🟢 优化建议（锦上添花）

**O-1: 删除脚手架残留 "**End of Skill**"**
- 位置: references/html-output-verification.md L34
- corpus 的 clean_scaffolding.py 本应处理此类标记；删除即可

**O-2: 明确 "9 sections" 的数字来源**
- 位置: references/html-output-verification.md L9
- 修复: 改为 "All 9 content blocks present（score banner, exec summary, one-pager preview, traction cards, team, cold email, email templates, distribution, investor table）"——把验证清单的 9 个内容条目与数字显式挂钩，避免与 step-4 的 7 个 Section 混淆

**O-3: 合并重叠的清单资产**
- references/step-5-quality-review-iteration.md（6 项）与 quality-checklist-before-finalizing.md（12 项）近半内容重复；8-critical-guidelines 第 3/5 条与 PROC-09/CF-03 语义重复
- 修复: quality-checklist 与 step-5 合并为一个文件（"## Quality Review"），8 条军规保留为独立前置阅读

**O-4: 精简访谈长度（493 行 → ~350 行的路径）**
- DF1（设计）与 IR1（时间线）与简报内容本身弱相关——DF1 可并入 STEP 4 生成阶段（按所选格式输出布局），IR1 可并入 step-6（Next Steps 输出的一部分）
- 两个问题下沉后 body 约 -90 行，同时解决 IR1/NEXT_STEPS/step-6 三方重叠（§4.5）

**O-5: 品牌条款泛化**
- 位置: references/html-editorial-template-reference.md L4
- "StratArts brand consistency" 的命名品牌出现在一个中立的 investor-brief skill 中略显突兀（与 057 的 "Claude (StratArts)" 同源问题）。若模板家族确需统一品牌，建议在文件中加一行说明（"StratArts is the house design system; replace with the user's brand when requested"），否则改为 "the house design system"

**O-6: CRM 示例行加"示例"标注**
- 位置: SKILL.md L433-435（DU2 表格）
- 修复: 表格下加一行注释 "*(Example rows — replace with the user's real investor data)*"，防止 agent 将 Jane Doe/Sequoia 等虚构行输出为真实名单（与 NEG-02/OUT-03 的张力，见 §4.6）

**O-7: STEP 3 标题与实测数量对齐**
- "Questions (One at a Time, Sequential)" 面对 15 个问题的实际情况，建议改为 "## STEP 3: Guided Interview (15 questions, ask one at a time)" 并给出建议节奏（如每 5 个问题暂停一次确认），与 322 号 skill 的 pacing 规则（2-3 questions per turn）对齐——当前标题给人"快速一问"的印象，实际是长访谈

### 修复工作量估计
- 预计修改行数: ~200 行新增 + ~60 行删除 = ~260 行净变化
- 预计修改文件数: 7 个（SKILL.md 为主战场；html-editorial-template-reference.md 或新建 html-templates/ 三件套；step-6-save-next-steps.md；html-output-verification.md；integration-with-other-skills.md；SCORING.yaml/check.py 微调；可选合并 step-5 与 quality-checklist）
- 修复优先级: F-1 → F-2 → F-3 → I-3 → I-5 → I-1/I-2（前五项完成即可恢复端到端可执行性与基本护栏）
- 修复后预期评级: 🟢（若 I-1~I-5 一并完成，可跻身 076-100 批次优等之列；该批 dossier 评级 8 个 🟢）

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 493 行，全文精读
2. SCORING.yaml — 199 行，全文
3. check.py — 73 行，全文
4. references/8-critical-guidelines-for-this-skill.md — 18 行，全文
5. references/html-editorial-template-reference.md — 31 行，全文
6. references/html-output-verification.md — 33 行，全文
7. references/integration-with-other-skills.md — 16 行，全文
8. references/quality-checklist-before-finalizing.md — 15 行，全文
9. references/step-4-generate-comprehensive-investor-brief.md — 52 行，全文
10. references/step-5-quality-review-iteration.md — 14 行，全文
11. references/step-6-save-next-steps.md — 7 行，全文
12. _shared/SKILL-SPEC.md — 162 行，全文（合规依据）
13. _shared/checker.py — 351 行，全文（script 检查语义核验）
14. skill-dossier.md（memory）— 076 条目提取（§11 对照）

### 读取统计
- 总文件数: 14（11 skill 文件 + 2 shared 文件 + 1 memory 档案）
- 总行数: 约 1,464 行

### 辅助核验
- corpus 目录 grep: 10 个跨 skill 引用名称的存在性逐一对照（§5.4）
- `wc -l` 行数核验;目录完整性核验（确认无 html-templates/ 子目录）

### 审查方法
- 所有文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则
- 跨 skill 引用核验依据: complex-skills/ 目录 322 个技能的实际命名
- 与 dossier 076 条目逐项对照，确认/修正既有发现并新增 5 项问题

### 本次审查新增发现（dossier 未记录）
1. html-templates/ 3 个 MUST-read 模板文件整体缺失（F-1，最高优先级）
2. 6/10 个名称级跨 skill 引用指向不存在的技能，STEP 1 上下文检测分支不可达（F-3）
3. 营收图表（QA-01 强制）的 12 个月数据无采集问题支撑（I-3-4）
4. follow-up 邮件模板缺失，与 8 条军规第 6 条自相矛盾（I-3-3）
5. "不得编造数据"护栏只存在于评测端（CF-01/NEG-02），body 无对应指令（I-5）
