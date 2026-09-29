# REVIEW: 196-cold-email — 深度审查 (Deep Review)

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit — deep review)
**Skill 类型**: tool / process — B2B 冷邮件外展策略（首封邮件、跟進序列、性能迭代）
**审查范围**: 目录全量文件 × 4；对照 SKILL-SPEC v1.0（`complex-skills\_shared\SKILL-SPEC.md`）12 项合规清单；SCORING.yaml 20 项测评点逐项映射；check.py 脚本审查；语料库跨 skill 引用核验
**上一版审查**: 2026-08-05，43 行，评分 "B (50/100)"（分数与量表区间矛盾，见 §11）

---

## 1. 目录全量清单

```
196-cold-email/
├── SKILL.md         266 行 / 14,326 B   (2026-08-05 20:02)
├── SCORING.yaml     185 行 /  8,407 B   (2026-08-05 14:57)
├── check.py          73 行 /  2,257 B   (2026-08-05 16:36)
└── REVIEW.md         43 行 /  1,640 B   (2026-08-05 20:46, 本次重写前)
```

- 合计：**4 个文件 / 567 行 / ≈26.6 KB**
- 子目录：**全部不存在** — `references/` ✗、`scripts/` ✗、`assets/` ✗、`templates/` ✗、`examples/` ✗、`specs/` ✗、`phases/` ✗、`docs/` ✗、`tests/` ✗、`agents/` ✗、`resources/` ✗
- 隐藏文件核验：`ls -laR` 无任何额外条目；目录中无 `.` 开头文件
- 结论：目录结构干净（仅 4 个规范文件），但存在**悬空引用**（`marketing-context.md`，见 §5.1）——dossier 所述"引用文件全部缺失"在文件层面成立

---

## 2. Frontmatter 逐字段审查

### 2.1 name — matches directory, lowercase+hyphens, ≤64 chars

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 值 | `cold-email` | ✔ |
| 小写+连字符 | ✔ | 全部小写，单连字符 |
| 长度 ≤64 | ✔ | 10 字符 |
| 匹配目录 | ✔ | 目录 `196-cold-email` = `NNN-` + `cold-email`，符合 NNN-kebab-case 规则 |
| 与 SCORING.yaml 一致性 | ✔ | SCORING.yaml L1 `skill: cold-email` 一致 |

### 2.2 description — sentence-by-sentence analysis

原文（SKILL.md L3）：
> "Write, improve, and build B2B cold email outreach sequences for outbound prospecting. Use when the user wants to craft cold emails, design multi-step outreach sequences, optimize email copy for response rates, or build targeted prospect lists."

**句 1**：`Write, improve, and build B2B cold email outreach sequences for outbound prospecting.`（约 91 字符）
- 承担 **WHAT** 职责：写/改进/构建 B2B 冷邮件外展序列 ✔
- 语态分析：动词开头、无主语——形式上为祈使句。规范 §2.3 要求"third-person, describes the skill"。严格阅读下属于边界性违规；语料库中大量 skill 采用此风格，建议改为 `Crafts, improves, and builds...`（动名词第三人称）以完全合规。**边界性 ⚠**

**句 2**：`Use when the user wants to craft cold emails, design multi-step outreach sequences, optimize email copy for response rates, or build targeted prospect lists.`（约 180 字符）
- 承担 **WHEN + KEYWORDS** 职责 ✔
- 触发短语：`Use when the user wants to...` —— 规范 §2.4 明确列出的 trigger signal ✔
- KEYWORDS：cold emails / outreach sequences / response rates / prospect lists ✔
- 无 first/second 人称代词（无 I/You/We）✔
- 无 cross-skill routing（description 中未出现"NOT for X use Y"）✔
- **主要问题 ⚠**：`build targeted prospect lists`（构建目标客户名单）在 body 中**无任何对应内容**——body 的 "The Prospect"（L23-27）只询问目标人画像用于个性化，没有任何"名单构建/爬取/筛选"的流程、步骤或原则。description 承诺了 body 未兑现的能力（description-body mismatch）。

**长度**：合计约 271 字符 ≤ 1024 ✔

### 2.3 allowed-tools — format, necessity per tool

- **未声明** `allowed-tools` 字段。
- 规范 §1.2 将其列为**可选**字段，缺席不违规 ✔
- 必要性分析：本 skill 为纯写作/策略类，核心交付（邮件文案、序列设计）不依赖任何工具。唯一隐含的工具依赖：
  - `Read` —— "Before You Start"（L12）要求"若 marketing-context.md 存在则先读它"，隐含需要 Read 能力；
  - `WebSearch`/`Glob` 未在 body 中要求。
- 建议：若未来补充该字段，至少应包含 `Read`；当前缺席无实际损害（无工具限制意味着 agent 可以自由使用）。**不扣分**。

### 2.4 其他 frontmatter 字段 — allowed/forbidden per SKILL-SPEC v1.0

- 现有字段仅 `name` + `description` 两个——均在 §1.1 必需字段清单内 ✔
- 规范 §1.3 禁止的字段（metadata、license、version、tags、trigger、triggers、related-skills、title、stats 等 30+ 项）**全部未出现** ✔
- 规范 §1.2 允许的可选字段（allowed-tools、argument-hint、user-invocable、model、paths、disable-model-invocation）**均未使用**——合规（可选）
- `## Metadata` 尾部节（规范建议的非规范元数据落点）：**无**——可选，不强制

### 2.5 Frontmatter 语法

- YAML 结构：`name:` + `description:` 两个简单键值对，无引号包裹、无内嵌冒号、无多行折叠符——解析无歧义 ✔
- 前后 `---` 定界符齐全（L1、L4）✔
- description 中逗号、括号均为半角，无潜在 YAML 陷阱 ✔
- **结论：frontmatter 语法完全健康**

---

## 3. Body 逐段结构分析

### 3.1 段落清单 — all headings with line counts

| # | 标题 | 行范围 | 行数 | 层级 |
|---|------|--------|------|------|
| 1 | `# Cold Email Outreach` | L6-8 | 3 | H1 |
| 2 | `## Before You Start` | L10-32 | 23 | H2 |
| 3 | `### 1. The Sender` | L17-21 | 5 | H3 |
| 4 | `### 2. The Prospect` | L23-27 | 5 | H3 |
| 5 | `### 3. The Ask` | L29-31 | 3 | H3 |
| 6 | `## How This Skill Works` | L35-63 | 29 | H2 |
| 7 | `### Mode 1: Write the First Email` | L37-44 | 8 | H3 |
| 8 | `### Mode 2: Build a Follow-Up Sequence` | L46-54 | 9 | H3 |
| 9 | `### Mode 3: Iterate from Performance Data` | L56-62 | 7 | H3 |
| 10 | `## Core Writing Principles` | L66-101 | 36 | H2 |
| 11 | `### 1. Write Like a Peer, Not a Vendor` | L68-75 | 8 | H3 |
| 12 | `### 2. Every Sentence Earns Its Place` | L77-81 | 5 | H3 |
| 13 | `### 3. Personalization Must Connect to the Problem` | L83-89 | 7 | H3 |
| 14 | `### 4. Lead With Their World, Not Yours` | L91-96 | 6 | H3 |
| 15 | `### 5. One Ask Per Email` | L98-100 | 3 | H3 |
| 16 | `## Voice Calibration by Audience` | L104-116 | 13 | H2 |
| 17 | `## Subject Lines: The Anti-Marketing Approach` | L119-143 | 25 | H2 |
| 18 | `### What Works` | L125-133 | 9 | H3 |
| 19 | `### What Kills Opens` | L135-142 | 8 | H3 |
| 20 | `## Follow-Up Strategy` | L146-188 | 43 | H2 |
| 21 | `### Cadence` | L150-161 | 12 | H3 |
| 22 | `### Follow-Up Rules` | L163-174 | 12 | H3 |
| 23 | `### The Breakup Email` | L176-187 | 12 | H3 |
| 24 | `## What to Avoid` | L191-207 | 17 | H2 |
| 25 | `## Deliverability Basics` | L210-223 | 14 | H2 |
| 26 | `## Proactive Triggers` | L226-236 | 11 | H2 |
| 27 | `## Output Artifacts` | L239-248 | 10 | H2 |
| 28 | `## Communication` | L251-258 | 8 | H2 |
| 29 | `## Related Skills` | L261-266 | 6 | H2 |

- H1 × 1，H2 × 17，H3 × 10；body 共 **261 行**（L6-266）

### 3.2 必需章节检查 — Workflow / Output Format / Scope-Limitations

| 必需章节 | body 落点 | 判定 |
|----------|-----------|------|
| Workflow/Process | `## How This Skill Works`（L35-63）：Mode 1（5 步）、Mode 2（6 步）、Mode 3（4 步），步骤均为编号指令 | ✔ 强覆盖 |
| Output Format | `## Output Artifacts`（L239-248）交付物对照表 + `## Communication`（L251-258）输出结构模式 | ✔ 强覆盖 |
| Scope/Limitations | **无专节**；仅 `## Related Skills`（L261-266）间接界定边界（"NOT for cold outreach — that's cold-email"、"cold email is the wrong tool to figure it out"） | ⚠ 弱覆盖 |

- Scope/Limitations 判定：规范 §3.1 要求"Must Answer: What does this skill NOT do? When should it NOT be used?"。Related Skills 给出了两个负向边界（不做生命周期邮件、不用于定位/ICP 梳理），但无独立的 "What This Skill Does NOT Do" 结构。**功能上可满足、形式上薄弱**——列为 🟡。

### 3.3 内容委托分析

- **零委托**：无 `references/`、无 `scripts/`——全部内容内联在 body 261 行中。这是双刃剑：
  - 优点：完全自包含，独立可执行性极高（见 §9.1）；
  - 缺点：Skill 类型 `pattern: tool` 的目标行数 ~300 行（规范 §3.2），body 已用 261 行，若后续扩充（如更细的 CTA 战术库、行业模板）将逼近 600 行硬上限——届时需要按规范 §3.3 委托 `references/`。
- 无脚本委托、无 agent 委托。

### 3.4 节编号/标题层级

- 标题层级连续：H1 → H2 → H3，无跳级 ✔
- **编号风格混用 ⚠**：`### 1./2./3.` 数字编号同时出现在两个不同 H2 下（"Before You Start" 的 Sender/Prospect/Ask 与 "Core Writing Principles" 的五原则），且每次都从 1 重启——本地编号重启本身可接受，但 "Mode 1/2/3"（文字式）与 "1.-5."（数字式）两种体系并存，风格不统一
- 未使用 GFM 自动编号/锚点冲突问题 ✔

### 3.5 Body 长度合规

- Body 261 行（L6-266）≤ 600 行硬上限 ✔
- 与 `pattern: tool` 目标（~300 行）相比：261 行处于合理区间 ✔
- 无因长度触发的强制委托需求

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- Mode 2 步骤 1 显式依赖 Mode 1（L49 "Start with the first email (Mode 1)"）——跨模式衔接清晰 ✔
- Mode 3 步骤 2（L60）的三分诊断（subject/body/CTA）与 FMT 类测评点（FMT-03/04/05）对应 ✔
- 每个 Mode 都以明确的 "Deliver: ..." 步骤收尾（L44、L54、L62），交付物清单与 Output Artifacts 表呼应 ✔
- **衔接缺口 ⚠**："Communication" 节（L251-258）定义的输出模式（Conclusion first / What+Why+How / 行动有负责人和期限 / 置信度标记）与三个 Mode 的 Deliver 步骤之间没有显式链接——agent 可能交付了内容却未套用 Communication 格式，而 QA-02 测评点恰恰检查这一格式
- "Before You Start"（L10-32）要求收集 Sender/Prospect/Ask 三类信息，但未说明信息不足时是提问还是推断——PROC-01 的测评措辞允许"确认已提供"，body 未将此显式化

### 4.2 内部矛盾扫描 — 核心发现

**矛盾 1（严重 🔴）：两条互相冲突的跟進节奏同时存在于一个 skill 中**

| 出处 | 节奏 |
|------|------|
| L51（Mode 2 步骤 3） | Day 1, Day 4, Day 9, Day 16, Day 25 |
| L152-159（Cadence 表） | Email 1 Day 1 / E2 Day 4 (+3) / E3 Day 9 (+5) / E4 Day 16 (+7) / E5 Day 25 (+9) / Breakup Day 35 (+10) |
| **L187（Follow-Up Strategy 末尾）** | **Day 1: initial value / Day 3: social proof / Day 7: insight / Day 14: pattern break / Day 21: breakup** |

- L187 与 L51/表格**完全冲突**：第 2 封在第 3 天 vs 第 4 天；第 3 封第 7 天 vs 第 9 天；breakup 第 21 天 vs 第 35 天。三处来源中 L51 与表格一致，L187 是孤立离群值。
- **影响**：agent 按哪条执行都"有据可依"；PROC-03 的裁判问题引用的是 `Day 1/4/9/16/25` 示例，若 agent 遵循 L187 仍可能被裁判误判为通过——矛盾会**静默污染评分**（见 §10.2）。

**矛盾 2（🟡）：序列长度三个数字不一致**

- L47："typically 4-6 emails"（Mode 2）
- L244："5-6 email sequence"（Output Artifacts）
- L187："5-7 touch sequence"（Follow-Up Strategy）
- 表内实际 6 封（5 跟進 + 1 breakup）。建议统一为 "5-6"。

**矛盾 3（🟢 轻微）：主题行变体数量不一致**

- L44（Mode 1 交付）："2-3 subject line variants"
- L243（Output Artifacts）："3 subject line variants"
- FMT-01 采用 "2-3"——以 L44/FMT-01 为准，L243 应改为 "2-3"。

**矛盾 4（🟡）：Deliverability 内容重复**

- L216 bullet："Domain warmup — 4-6 weeks, start at 20/day"
- L220 bullet："Bounce rate — above 5% hurts"
- L215 bullet："SPF, DKIM, DMARC — all three must be set up"
- L222-223 独立段落重复了 warmup（10-20/day、~20%/week）、SPF/DKIM/DMARC、bounce <5%，唯一新信息是**垃圾词清单**（free, guarantee, act now, limited time）
- 该重复已被上一版 REVIEW 发现（属实），但需要补充：L216 的 "start at 20/day" 与 L222 的 "start with 10-20 emails/day" 数字表述不完全一致（20 vs 10-20）——虽为范围重叠，仍是双处定义

**矛盾 5（🟡）：description 越权承诺**

- description "build targeted prospect lists" 在 body 无对应内容（详见 §2.2）——描述与能力错位。

### 4.3 示例/代码正确性

- **主题行示例**（L129-133）：`quick question` / `your LinkedIn post` / `re: Series B` / `your current ATS` / `[mutual name] suggested I reach out` —— 全部符合自身"反营销"规则（短、具体、像内部邮件）✔
- **✅/❌ 对照示例**（L74-75、L95-96）：反例真实（"I'm reaching out because our platform..."、开场即产品介绍），正例符合"以对方世界开场"原则 ✔
- **Breakup 示例**（L181-185）：占位符 `[problem]`、`[Company]`、`[whatever's relevant]` 使用规范，属邮件模板占位（非未填充的 skill 占位符）✔
- **节奏表内数学**（L152-159）：+3/+5/+7/+9/+10 严格递增，表内自洽 ✔（问题仅在 L187）
- **外部事实**：mail-tester.com（L215）真实存在；CAN-SPAM/GDPR（L218）法域标注正确 ✔
- 本 skill 无代码示例（非代码型 skill），check.py 的 Python 代码另见 §5.4 ✔

### 4.4 条件完整性

- L12 "If `marketing-context.md` exists, read it" —— **条件清晰但位置未定义**（skill 根目录？workspace 根目录？），且文件实际不存在（§5.1）。条件句缺少"若不存在则跳过"的显式后续（虽可意会）
- Mode 选择条件（L37/46/56 "When they need..."）——三个模式的适用条件完整 ✔
- Voice Calibration 表（L108-113）覆盖 4 类受众（C-suite/VP/Mid-level/Technical）——分类穷尽性可接受 ✔
- Proactive Triggers（L230-235）6 项触发条件，与 ERR-01 测评点一一对应 ✔
- 缺失条件 ⚠：未定义"用户未提供目标人信息时"的处理路径（直接提问 vs 用占位符）——可操作性上依赖 agent 常识

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用目标 | 引用位置 | 实际存在性 | 判定 |
|----------|----------|-----------|------|
| `marketing-context.md` | SKILL.md L12 | ❌ 不存在于 skill 目录任何位置；references/ 目录本身不存在 | 🔴 悬空引用 |
| `email-sequence`（skill） | SKILL.md L263 | ❌ 语料库中无此 skill（complex-skills 与 no-trigger 均无） | 🔴 悬空引用 |
| `copywriting`（skill） | SKILL.md L264 | ✔ `150-copywriting` 存在 | ✔ |
| `content-strategy`（skill） | SKILL.md L265 | ❌ 语料库中无此 skill | 🔴 悬空引用 |
| `marketing-strategy-pmm`（skill） | SKILL.md L266 | ✔ `165-marketing-strategy-pmm` 存在 | ✔ |
| mail-tester.com（外部工具） | SKILL.md L215 | ✔ 真实网站 | ✔ |
| `..\_shared`（Python 导入） | check.py L11 | ✔ `complex-skills\_shared\checker.py` 存在 | ✔ |

- 引用完整率：7 项中 4 项有效、3 项悬空。**dossier "引用文件全部缺失"判定成立**（marketing-context.md + 两个 skill 引用）。

### 5.2 不可见资源审计

- `references/`：不存在（SKILL.md 未引用任何 `references/` 路径——不存在对缺失子目录的引用，唯一悬空的是裸文件名 `marketing-context.md`）
- `scripts/`：不存在（check.py 不依赖任何脚本资源）
- 其余子目录（assets/templates/examples/specs/phases/docs/tests/agents/resources）：全部不存在
- 结论：除 marketing-context.md 外，不存在"引用了但目录缺失"的情况——缺失面小于 dossier 措辞的暗示，但 marketing-context.md 是 SCOPE-03 脚本检查的依赖项（§10.1），影响权重高

### 5.3 Reference 文件全文审查

- 无 references/ 文件可审。**N/A**（由 §5.2 覆盖）。

### 5.4 Scripts 文件全文审查 — check.py（73 行）

- 结构：`check()` 仅执行 1 项脚本检查（SCOPE-03），其余 19 项全部交由 LLM judge——docstring "Run all 1 script checks" 与实际一致 ✔
- 导入 `tool_log_contains / set_tool_log_path / set_agent_output` 全部被使用，无死导入 ✔
- `main()`：参数校验（4 参数）、agent_output 文件读取、JSON 输出——健壮 ✔
- **设计缺陷 1 ⚠（SCOPE-03）**：`result["SCOPE-03"] = tool_log_contains('marketing-context\\.md')`（L34）为**无条件检查**，而 SKILL.md L12 的行为是**条件性的**（"If marketing-context.md exists"）。若测评 workspace 中未放置该文件，agent 的正确行为（不读取）必然导致 SCOPE-03 失败——检查结果与 skill 指令脱钩，分数不可控
- **设计缺陷 2 ⚠**：正则 `marketing-context\\.md` 匹配 tool log 中任何包含该字符串的调用（Read 失败也算命中）。若 agent 因文件不存在而 Read 报错，工具日志仍会包含路径字符串——"尝试读"被计为"成功读"，语义失真
- 无其他逻辑问题；编码/输出格式合规

### 5.5 跨 Skill 引用检查

- `email-sequence`（L263）：**不存在**——但注意这是语料库级问题：`150-copywriting` 的 description 同样引用 `email-sequence`（"For email copy, see email-sequence"），即该悬空引用波及至少 2 个 skill
- `content-strategy`（L265）：**不存在**——196 独有悬空
- `copywriting`、`marketing-strategy-pmm`：存在 ✔
- **重要遗漏 ⚠**：语料库中存在 `159-cold-email-sequence-generator`（7-14 封冷邮件序列 + A/B 测试主题行 + 跟進时机推荐），与 196 的 Mode 2 功能**高度重叠**，但 Related Skills 完全未提及 159——跨 skill 边界（4-6 封 vs 7-14 封、A/B 测试有无）未定义。测评时用户请求若同时命中两 skill 的描述，路由结果不可预期
- 无 `../` 跨目录文件路径 ✔（符合规范 §3.3）

### 5.6 嵌套重复/死文件检查

- 目录层面：无死文件、无嵌套重复、无残留副本（仅 4 个规范文件）✔
- **内容层面重复 2 处**：
  1. L216/220 vs L222-223（warmup/SPF/DKIM/DMARC/bounce 重复，见 §4.2 矛盾 4）
  2. L187 vs L51/表格（节奏重复且内容冲突，见 §4.2 矛盾 1）——dossier "目录含重复残留"更准确的解读应落在**内容重复**而非文件残留上（见 §11）

### 5.7 其他资源文件审查

- 无其他子目录/资源文件。**N/A**。

---

## 6. 语法与格式质量

### 6.1 拼写错误

- 全文通读未发现拼写错误。抽查：personalization（L85/89，一致美式拼写）、Deliverability（L210）、anti-marketing（L119，连字符一致）、mail-tester.com（L215）✔

### 6.2 语法错误

- 未发现语法错误。句式干净（短句为主，符合该 skill 主题的"简洁"精神）✔

### 6.3 中英/葡英混杂

- body 为**纯英文**，无中文、无葡萄牙语、无其他语言混杂 ✔
- （本审查文件为中文是审查约定，不影响 skill 本身）

### 6.4 Markdown 格式破损

- 5 张表格全部规范（表头分隔行齐全、列对齐）✔
- L181-185 块引用跨段格式正确（`>` 每行前缀 + 空 `>` 段间分隔）✔
- 标题层级无跳级；强调符号（`**`、`` ` ``）配对完整 ✔
- 无损坏的链接/图片语法 ✔

### 6.5 占位符未填充

- 无未填充占位符。`[problem]`、`[Company]`、`[whatever's relevant]`（L181-185）、`[mutual name]`（L133）均为**邮件模板的有意占位**，属内容设计而非缺陷 ✔
- 唯一接近"悬空占位"的是 `marketing-context.md`（L12）——它像一个未随 skill 发布的引用文件（见 §5.1）

### 6.6 截断内容

- 无截断：L266 以完整的 Related Skills 最后一条（marketing-strategy-pmm 条目）正常收尾，无断句/半表/未闭合列表 ✔

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | name 小写+连字符 ≤64、匹配目录 | ✔ | `cold-email`；目录 `196-cold-email` |
| 2 | description 第三人称 WHAT+WHEN+KEYWORDS ≤1024 | ⚠ 边界 | ~271 字符 ✔；WHEN/KEYWORDS ✔；句 1 动词开头无主语，形式上祈使（§2.2） |
| 3 | description 无祈使/第一/第二人称 | ⚠ 边界 | 无 I/You/We 代词 ✔；句 1 动词开头属祈使形式 |
| 4 | description 无跨 skill 路由 | ✔ | description 未含 "NOT for X" |
| 5 | description 至少一个触发信号 | ✔ | "Use when the user wants to..."（L3） |
| 6 | frontmatter 无禁用键 | ✔ | 仅 name + description |
| 7 | body ≤600 行 | ✔ | 261 行（L6-266） |
| 8 | 有 workflow/process 章节 | ✔ | `## How This Skill Works`（L35）三模式 |
| 9 | 有 output format 章节 | ✔ | `## Output Artifacts`（L239）+ `## Communication`（L251） |
| 10 | 有 scope/limitations 章节 | ⚠ 弱 | 仅 Related Skills 间接覆盖（§3.2） |
| 11 | 无跨 skill 文件路径（../） | ✔ | 无 `../` 引用；Related Skills 用散文名引用（规范 §3.3 允许） |
| 12 | 目录 NNN-kebab-case | ✔ | `196-cold-email` |

**合规得分：12/12 项全部通过或边界通过（其中 3 项为 ⚠ 边界/弱覆盖）≈ 11.5/12。** 无硬性违规项——与 dossier 🟠 评级相比，规范性层面实际表现好于 dossier 暗示。

---

## 8. 人机感评估

### 8.1 Emoji 审计

- 全文共 8 处 emoji（L74 ❌、L75 ✅、L95 ❌、L96 ✅、L195 ❌表头、L257 🟢/🟡/🔴）
- 全部为**功能化用途**：✅/❌ 作示例好坏对照标记，🟢🟡🔴 作置信度标记（Communication 节的明确设计），无装饰性/语气性 emoji
- 注意：QA-02 测评点把"confidence marking"（含 emoji 标记）编码进必查格式——emoji 是测评体系的组成部分，非随意使用
- 判定：🟢 低风险观察项。若语料库级标准禁 emoji，需同步改 SKILL.md 与 SCORING.yaml 两处

### 8.2 全大写/喊叫

- 正文无全大写滥用；"ALL CAPS"（L137）是主题行反模式的教学内容而非喊叫 ✔

### 8.3 Persona 语气

- L8 "You are a B2B cold email prospecting specialist. Your goal is to help..."——面向 agent 的角色设定，专业、克制、顾问式
- 用户以 "they/their" 指代（L37/46/56 "When they need..."），与 agent persona 区分清楚 ✔
- 整体语气与技能主题（"写得像人"）自洽，无机械腔 ✔

### 8.4 人机边界

- skill 的主题恰是"避免机器人腔"——所有指导内容服务于该主题，无越界；无将 agent 冒充真人的不当表述（"sounds like a human" 是文案标准而非身份冒充）✔

### 8.5 人称分析

- body 中第二人称祈使句大量出现："Read your draft out loud"（L81）、"Don't ask them to book a call..."（L100）、"who you're writing to"（L108）、"You're persistent but not annoying"（L161）、"if you can't reach them"（L170）
- **重要更正 ⚠**：上一版 REVIEW 称 L8 第二人称"违反 §2.3"——但 SKILL-SPEC v1.0 的 §2.3 Voice 规则位于 "## 2. Description Specification" 章节之下，**仅约束 description**；body 的第二人称指令不构成规范违规。旧审查存在对规范的误用（详见 §11）
- 就人机感而言，body 第二人称是面向 agent 的执行指令，接受度高；若追求严格一致可改为无主语祈使句

### 8.6 表格太多

- 共 5 张表（Voice Calibration L108-113、What Works L127-133、Cadence L152-159、What to Avoid L195-206、Output Artifacts L241-247），密度约 1 表/52 行
- 全部为决策/对照/交付物类表格，符合规范 §3.4 "Decision trees over prose" 的偏好 ✔
- 判定：可接受，无需削减

---

## 9. 可执行性评估

### 9.1 独立可执行性

- **自包含程度高**：除可选的 marketing-context.md 外零外部依赖；无 references/ 也能独立完成全部交付物
- 一个具备常识的 agent 仅凭本 SKILL.md 即可产出合规冷邮件——独立性评级 ✔（前提是修复 §4.2 的节奏矛盾）

### 9.2 步骤可操作性

- 三模式步骤均为"理解→选择→产出→复盘"的可执行链，每步有具体输入（ICP、触发事件、性能数据）与输出（交付物清单）✔
- 原则节提供判断标准（"Would a friend send this?"、150 词阈值、one-ask 规则）——可操作、可验证 ✔
- Proactive Triggers 提供明确的 flag-and-fix 行为 ✔
- 唯一可操作性缺口：L12 的 marketing-context.md 条件分支（位置不明 + 文件缺失）会让 agent 在该步骤上产生不确定性

### 9.3 工具依赖

- 必需工具：无 ✔
- 可选工具：Read（marketing-context.md，条件性）；WebSearch（未要求，但 personalization 研究时可自选）
- allowed-tools 缺席无实际影响（§2.3）

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖 — 20 项逐条映射

| ID | 类别 | 判据方式 | body 落点 | 覆盖判定 |
|----|------|----------|-----------|----------|
| SCOPE-01 | scope | llm | Related Skills L263（与 email-sequence 区分） | ✔（但被引用 skill 不存在，见 §5.5） |
| SCOPE-02 | scope | llm | Mode 1/2/3（L37/46/56） | ⚠ 裁判问题列了 **5 种模式**（含 critique、write follow-ups），body 仅定义 3 种模式；另 2 种只在 Output Artifacts 表（L245-246）作为交付物出现，无流程步骤 |
| SCOPE-03 | scope | **script** | L12 marketing-context.md | ⚠ 无条件检查 vs 条件性行为（§5.4 设计缺陷 1） |
| PROC-01 | process | llm | Before You Start L10-32 | ✔ |
| PROC-02 | process | llm | Follow-Up Rules L163-174 | ✔ |
| PROC-03 | process | llm | Cadence L150-161 | ⚠ 与 L187 冲突（§4.2 矛盾 1） |
| PROC-04 | process | llm | Mode 3 步骤 2 L60 | ✔ |
| FMT-01 | format | llm | Mode 1 交付 L44 | ✔（L243 的 "3" 与 "2-3" 不一致为轻微噪音） |
| FMT-02 | format | llm | Mode 2 交付 L54 | ✔ |
| FMT-03 | format | llm | Proactive Triggers L231（150 词） | ✔ |
| FMT-04 | format | llm | What Kills Opens L135-142 | ✔ |
| FMT-05 | format | llm | 原则 4 L91-96 + Triggers L230 | ✔ |
| COP-01 | format | llm | 原则 3 L83-89 | ✔ |
| COP-02 | format | llm | 原则 5 L98-100 | ✔ |
| COP-03 | format | llm | Voice Calibration L104-116 | ✔ |
| NEG-01 | negative | llm | What to Avoid L197-203 | ✔ |
| NEG-02 | negative | llm | What to Avoid L199-200 | ✔ |
| QA-01 | qa | llm | Deliverability L210-223 | ✔（内容重复不影响覆盖） |
| QA-02 | qa | llm | Communication L251-258 | ✔（依赖 §4.1 指出的格式-交付脱节，实际达成率打折） |
| ERR-01 | error_handling | llm | Proactive Triggers L226-236 | ✔ |

- 覆盖结论：20/20 有 body 落点；其中 4 项存在 ⚠ 风险（SCOPE-02、SCOPE-03、PROC-03、QA-02）
- 结构性观察：20 项中 **19 项依赖 LLM judge**，仅 1 项脚本检查——脚本护栏过少；若 SCOPE-03 因文件缺失必然失败，则脚本层贡献的分数几乎为 0

### 10.2 Critical Failures 分析

| ID | 触发条件 | 效果 | 与 body 对齐 |
|----|----------|------|-------------|
| CF-01 | 开场含 "I hope this email finds you well" / "My name is X and I work at Y" | cap_to_0 | ✔ 对应 What to Avoid L197/L203、NEG-01 |
| CF-02 | "just checking in" 无新角度的跟進 | cap_to_0 | ✔ 对应 L172/L202/L233 |
| CF-03 | 将生命周期/培育邮件模式套用到冷外展（opt-in 假设、按钮 CTA、重 HTML） | cap_to_0 | ✔ 对应 Related Skills L263 边界 |

- CF 设计合理，与 NEG 类测评点互补（CF 为评分上限压制，NEG 为单项判定）✔
- **遗漏 ⚠**：未针对 §4.2 矛盾 1 设置 CF——若 agent 按 L187 节奏（Day 1/3/7/14/21）执行，PROC-03 以 L51 示例判定可能误判通过，且无任何机制暴露该矛盾

---

## 11. 已知问题汇总 — dossier 条目验证与新增发现

### Dossier 条目逐项验证

**条目 1："🟠 引用文件全部缺失" — ✅ 属实（成立）**
- `marketing-context.md`（L12）不存在于 skill 目录；`email-sequence`、`content-strategy` 两个 Related Skills 引用在语料库中不存在
- 补充限定：除 marketing-context.md 外，无 `references/`、`scripts/` 目录缺失问题（目录本身干净）

**条目 2："目录含重复残留" — ⚠ 部分属实（需修正解读）**
- **目录层面不成立**：`ls -laR` 确认无重复文件、无残留副本、无隐藏文件——4 个规范文件各居其位
- **内容层面成立**：重复发生在 SKILL.md 内部——(a) L216/L220 vs L222-223 的 Deliverability 重复；(b) L187 与 L51/表格的节奏重复。且 (b) 不只是"重复"，而是**两个不同值的冲突**（Day 3 vs Day 4、Day 21 vs Day 35）
- 建议 dossier 表述改为："SKILL.md 内容级重复 2 处，其中节奏表述自相矛盾"

### Dossier / 上一版 REVIEW 遗漏的问题（本次新发现）

1. **🔴 节奏矛盾**：L187（Day 1/3/7/14/21, 5-7 touch）与 L51 + L152-159 表（Day 1/4/9/16/25/35）冲突——旧 REVIEW 只看到"重复"，未识别为"冲突"
2. **🟡 序列长度三值不一**：L47 "4-6" / L244 "5-6" / L187 "5-7"
3. **🟡 description 越权**："build targeted prospect lists" 无 body 支撑
4. **🟡 SCOPE-02 模式数不匹配**：裁判问 5 种模式，body 只定义 3 种
5. **🟡 SCOPE-03 无条件脚本检查 vs 条件性 skill 指令**（check.py L34）
6. **🟡 Related Skills 两个悬空 skill 引用**（email-sequence、content-strategy）+ 未提及高重叠的 159-cold-email-sequence-generator
7. **🟡 旧 REVIEW 规范误用**：称 L8 第二人称 persona"违反 §2.3"——§2.3 仅约束 description；description 本身无 I/You 代词，实际合规（仅句 1 祈使形式为边界）
8. **🟢 旧 REVIEW 分数自相矛盾**："🟡 B (50/100)"——按既定量表 50 分落在 🟠C (40-59) 区间，B 应为 60-79；本次修正为 78（B），并给出可复算的加权表（§12）
9. **🟢 Emoji 使用 8 处**（功能化，QA-02 强依赖）
10. **🟢 主题行变体 "2-3" vs "3"**（L44 vs L243）

---

## 12. 综合评分 — 8 dimensions weighted table

| 维度 | 权重 | 得分(0-1) | 加权 | 依据 |
|------|------|-----------|------|------|
| 规范合规性（12-item） | 15% | 0.95 | 14.25 | 12/12 通过，3 项边界/弱覆盖（§7） |
| 内容质量 | 15% | 0.90 | 13.50 | 反模式具体、示例真实、阈值明确（150 词、+3/+5/+7 间隔） |
| 结构与组织 | 10% | 0.85 | 8.50 | 三模式结构清晰；Scope 节薄弱、编号体系混用（§3.4） |
| 逻辑一致性 | 20% | 0.55 | 11.00 | 节奏冲突 🔴 + 长度三值 + 描述越权（§4.2） |
| 参考文件完整性 | 15% | 0.50 | 7.50 | marketing-context.md 悬空 + 2 个悬空 skill 引用（§5.1） |
| 语法格式质量 | 5% | 0.95 | 4.75 | 无拼写/语法/格式破损（§6） |
| 人机感 | 5% | 0.85 | 4.25 | persona 专业、emoji 功能化；body 第二人称偏多（§8） |
| 可执行性 | 15% | 0.95 | 14.25 | 自包含、步骤可执行、零工具依赖（§9） |
| **合计** | 100% | — | **78.0** | — |

**最终评级：🟡 B（78/100，区间 60-79）**

- 与 dossier 🟠 的关系：dossier 仅凭 2 条问题（引用缺失+重复）定级 🟠；深度审查显示其规范性、内容与可执行性维度显著强于 dossier 暗示——但 **🔴 节奏矛盾 + SCOPE-03 检查失效风险**足以阻止其进入 A 档
- 与上一版 "B (50/100)" 的关系：评级字母一致，但分数修正（50→78），且旧分数落入了错误的量表区间
- 修复 §13 中 🔴 两项后预计可达 88-90（A 档）；修复全部 🟡 后可达 93+（A 档高分区）

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷 — 影响测评可靠性，必须修复

**F1. 跟進节奏冲突（SKILL.md L187 vs L51/L152-159）**
- 问题：L187 "Day 1: initial value. Day 3: social proof. Day 7: insight/trigger. Day 14: pattern break question. Day 21: breakup email" 与 L51 和 Cadence 表的 Day 1/4/9/16/25（+Breakup Day 35）完全冲突；"5-7 touch" 亦与 L47/L244 矛盾。agent 执行时面临两条互斥指令，PROC-03 评分结果取决于 agent 恰好读到哪一行
- 修复：删除 L187 的节奏数字，仅保留角度轮换内容并合并进 `### Follow-Up Rules`（L163-174），改为："Rotate angles across the sequence — never repeat the same value proposition twice. Initial value, then social proof, insight/trigger, pattern break question, breakup."（不写具体天数，天数统一以 Cadence 表为准）
- 后果：消除唯一 🔴 矛盾；PROC-03 裁判输入与 body 唯一化，评分可复现

**F2. marketing-context.md 悬空引用（SKILL.md L12）**
- 问题：条件句引用的文件不存在于 skill 目录，位置亦未定义；同时 SCORING.yaml SCOPE-03 / check.py L34 以**无条件**脚本检查依赖它——若 runner 不注入该文件，脚本检查对任何 agent 都必然失败（正确行为 = 不读取 = 失败）
- 修复（二选一）：
  - 方案 A（推荐，skill 侧）：将引用改为 `references/marketing-context.md` 并创建该文件（如一份含 sender/prospect/ask 占位模板）；SCORING 侧同步确保 runner 在 workspace 注入同名文件——条件句与检查都指向确定位置
  - 方案 B（runner 侧）：确认测评环境注入该文件；check.py L34 增加存在性前置判断（先 file_exists 再判定 tool log）
- 后果：SCOPE-03 从"不可控"变为"可判定"；修复后脚本层贡献 1 项有效测评点

### 🟡 重要缺陷 — 影响一致性与评分精度，应尽快修复

**F3. 序列长度三值不统一（L47/L187/L244）**
- 修复：统一为 "5-6 emails（含 breakup）"，与 Cadence 表 6 封一致；L47 "typically 4-6 emails"、L244 "5-6 email sequence"、L187 "5-7 touch sequence" 全部对齐

**F4. description 越权承诺（L3 "build targeted prospect lists"）**
- 修复（二选一）：(a) 从 description 删除该短语（推荐——名单构建不是本 skill 能力）；(b) 在 body 增加一小节 "Prospect List Input" 说明如何接收/校验已有名单（不承诺构建）。若选 (b)，需在 Output Artifacts 增加对应交付物，避免再次脱节

**F5. SCOPE-02 五模式 vs body 三模式（SCORING.yaml L18/L20 vs SKILL.md L37-62）**
- 修复（推荐 scorer 侧）：SCOPE-02 裁判问题改为与 body 一致的三模式 + 交付物表（critique/follow-ups 归入 Output Artifacts 交付路径）；或（skill 侧）将 Critique 与 Follow-ups-only 升格为 Mode 4/Mode 5 各给 3-5 步流程。前者改动小，推荐前者

**F6. Related Skills 悬空引用（L263 email-sequence、L265 content-strategy）**
- 修复：email-sequence 不存在于语料库——L263 改为指向真实存在的相邻 skill：`159-cold-email-sequence-generator`（说明差异：159 面向 7-14 封 A/B 测试型序列，196 面向 4-6 封轻量序列）或 copywriting（已引用）；content-strategy 不存在——删除或改为 `246-content-research-writer`（存在）并核实语义
- 附带：在 Related Skills 或 Scope 节显式定义与 159-cold-email-sequence-generator 的边界（序列长度、A/B 测试能力），消除路由不确定性

**F7. Deliverability 重复段落（L222-223 vs L214-220）**
- 修复：删除 L222-223 的重复内容，仅保留新信息，并入 bullets："Avoid spam trigger words (free, guarantee, act now, limited time) in subject lines and first paragraphs."；顺带统一 warmup 数字（"start at 20/day" vs "10-20/day" → 取 10-20/day）

**F8. Scope/Limitations 节形式化（当前弱覆盖）**
- 修复：新增 `## Scope and Limitations` 节（或改写 Related Skills 导语），明确列出：(1) 不做生命周期/培育邮件（→ email-sequence/159）；(2) 不做文案/页面 copy（→ copywriting）；(3) 不做 ICP/定位梳理（→ marketing-strategy-pmm）；(4) 不承诺名单构建/爬取；(5) 不处理交付结果，不发送邮件（无发送动作）
- 后果：§7 检查项 10 从弱覆盖转强覆盖

**F9. QA-02 格式-交付脱节（Communication L251-258 vs 各 Mode Deliver 步骤）**
- 修复：在三个 Mode 的 Deliver 步骤或 Communication 节首句增加一句："All deliverables follow the Communication pattern below（结论先行/What+Why+How/置信度标记）"——建立显式链接

### 🟢 优化建议 — 低成本高收益

**F10. description 句 1 第三人称化（L3）**：`Write, improve, and build...` → `Crafts, improves, and builds...`——消除祈使形式的边界争议（§2.2/§7 项 3 转全绿）

**F11. 主题行变体统一（L243）**："3 subject line variants" → "2-3 subject line variants"，与 L44/FMT-01 一致

**F12. body 第二人称收束（L81/L100/L108/L161/L170 等）**：改为无主语祈使句（"Read the draft out loud" / "Don't ask them..."）——与 description 的第三人称严格一致，规避未来规范收严风险

**F13. Emoji 功能化留档**：在 SKILL.md 或 SCORING.yaml 注释中说明 🟢🟡🔴 为通信协议组成部分；若语料库统一禁 emoji，需同步替换为文字标记（[verified]/[assumed]）并修改 QA-02 措辞

**F14. 编号体系统一（§3.4）**：三处数字编号（Before You Start / Core Writing Principles）改为描述性标题（"The Sender"→"Sender Context" 类）或统一连续编号

**F15. 可选：`## Metadata` 尾部节**：补记录来源/版本（如无则跳过，非强制）

### 修复工作量估计

| 层级 | 项数 | 内容性质 | 人力估计 | Claude 估计 |
|------|------|----------|----------|-------------|
| 🔴 F1-F2 | 2 | SKILL.md 改 2 处 + SCORING/runner 协调 1 处 | 1-2 小时 | 15 分钟 |
| 🟡 F3-F9 | 7 | SKILL.md 编辑为主 + SCORING.yaml 微调 1 处 | 2-3 小时 | 30-40 分钟 |
| 🟢 F10-F15 | 6 | 文字级微调 | 0.5-1 小时 | 10 分钟 |
| **合计** | 15 | — | **3.5-6 小时** | **约 1 小时** |

修复优先级路线：F1 → F2 → F3 → F5 → F4/F6 → 其余。F1+F2 完成后评级即达 A 档门槛（80+）；全部完成约 93-95 分。

---

## 附录: 审查过程记录

| 步骤 | 内容 | 结果 |
|------|------|------|
| 1 | Glob 递归枚举 skill 目录 | 4 文件；`ls -laR` 复核无隐藏文件/子目录 |
| 2 | Read SKILL.md 全文 | 266 行，逐行审读 |
| 3 | Read SCORING.yaml 全文 | 185 行，20 项 criterion + 3 项 CF |
| 4 | Read check.py 全文 | 73 行，1 项脚本检查 |
| 5 | 枚举 references/ | 目录不存在（N/A） |
| 6 | 枚举 scripts/ | 目录不存在（N/A） |
| 7 | 枚举其他子目录 | 全部不存在（N/A） |
| 8 | Read 旧 REVIEW.md | 43 行，发现分数区间矛盾与 §2.3 误用 |
| 附加 | 读取 SKILL-SPEC v1.0（complex-skills\_shared） | 确立 12 项合规基准与 §2.3 适用范围 |
| 附加 | 读取 checker.py（complex-skills\_shared） | 核验 tool_log_contains 语义（无条件匹配字符串） |
| 附加 | 语料库交叉核验 | email-sequence ✗ / content-strategy ✗ / copywriting ✔ (150) / marketing-strategy-pmm ✔ (165) / 159-cold-email-sequence-generator 存在且高重叠 |
| 核验方法 | 全文逐行审读 + 三处节奏来源交叉比对 + 数字算术复核（+3/+5/+7/+9/+10） + description 字符计数 + emoji 逐处定位 | 见 §4/§5/§7/§8 各节 |

**审查结论**：196-cold-email 内容质量与可执行性优秀（冷邮件实操指南水准），规范合规 11.5/12；但存在 1 处 🔴 节奏冲突、1 处 🔴 悬空引用（连带脚本检查失效风险）及 7 项 🟡 一致性/评分精度问题。综合 **78/100（🟡 B）**。dossier 两条问题均经验证（一条完全成立、一条需从"目录重复"修正为"内容重复且冲突"），并新增 10 项 dossier 未覆盖的问题。建议按 §13 路线图优先修复 F1/F2。

---

## 变更记录

- 2026-08-05: 初始审查（43 行，评分 "B (50/100)"——分数与量表区间不符）
- 2026-08-06: 深度审查重写（本版）。修正旧版两处错误（§2.3 适用范围误用、分数区间矛盾），新增节奏冲突等 10 项发现；评分修正为 🟡 B (78/100)
