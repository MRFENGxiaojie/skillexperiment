# REVIEW: 212-written-consent

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 董事会/委员会一致书面同意书 (unanimous written consent) 起草 + 先例检索 + 法律风险门控
**Body 行数**: 315 行
**参考文件数**: references/0, scripts/0, assets/0
**总文件数**: 3

---

## 1. 目录全量清单

```
212-written-consent/
├── SKILL.md (315 行)
├── SCORING.yaml (184 行)
└── check.py (72 行)
```

- 极简三文件结构，无 `references/`、`scripts/`、`assets/` 子目录，是 322 个 skill 中文件数最少的类型之一。
- 唯一的外部代码依赖是 `../_shared/checker.py`（运行于 corpus `_shared/` 目录，已验证存在且全部 18 个导入符号可用）。
- 该 skill 属于 `claude-for-legal` 插件家族的 corporate-legal 组件，全部运行上下文依赖插件配置目录 `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md`（SKILL.md 中 11 处引用，详见 §5）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 值: `written-consent`，全小写+连字符 ✓
- 长度: 15 字符，远低于 64 字符限制 ✓
- 匹配目录名 `212-written-consent` ✓
- 与 `pattern: process`（SCORING.yaml 声明）一致，process 类 skill 名称简洁无歧义 ✓

### 2.2 description

原文:

> "Draft a unanimous written consent of the board or a committee in house format, with precedent search from the consents repository. Handles multi-resolution consents, director conflict flags, state-law notice requirements, and signatory tracking, with a built-in scope warning for major one-off actions. Use when user says "written consent", "unanimous consent", "board consent", "consent in lieu", "UWC", or describes an action needing board approval without a meeting."

逐句分析（已用 YAML 解析器验证 frontmatter 可正确解析，长度 469 字符 ≤1024）：

**第 1 句** (WHAT): "Draft a unanimous written consent of the board or a committee in house format, with precedent search from the consents repository."
- 功能描述精确: 对象（board/committee）、产出（house format 同意书）、机制（consents repository 先例检索）三者齐全 ✓
- 动词开头 "Draft a..." 与 SKILL-SPEC §2.6 官方"好例"（"Generate comprehensive test plans..."）同构，属语料库惯例，不判违规 ✓

**第 2 句** (能力清单): "Handles multi-resolution consents, director conflict flags, state-law notice requirements, and signatory tracking, with a built-in scope warning for major one-off actions."
- 以第三人称列举四项核心能力 + 一个内置护栏，与 body 中 Step 3/Step 1/Step 4/Step 5/Scope warning 逐项对应 ✓
- 这是 description 中少见的"能力罗列"句，但每项都可在 body 中找到对应指令，非空泛承诺 ✓

**第 3 句** (WHEN): "Use when user says ... or describes an action needing board approval without a meeting."
- 触发短语存在 ✓
- 关键词覆盖: "written consent", "unanimous consent", "board consent", "consent in lieu", "UWC" 及语义触发（"describes an action needing board approval without a meeting"）— 覆盖面好 ✓
- **问题1**: "Use when user says" 缺少定冠词，SKILL-SPEC §2.4 的规范触发信号是 "Use when the user..."。这是与规范措辞的轻微偏差，虽不影响触发匹配，但建议统一为 "Use when the user says"。
- **问题2**: 内层引号 `"written consent"` 等位于双引号 YAML 标量内的合法位置（plain scalar 中 `"` 合法），已验证解析无错 ✓ — 无 YAML 破损风险。

### 2.3 argument-hint

`[describe the action needing board approval]` — ✅ 简洁、与 Step 1 的 intake 问题直接对应，是规范允许的可选字段。

### 2.4 其他 frontmatter 字段

- 仅 name / description / argument-hint 三个键，无任何禁止字段（无 metadata、trigger、tags 等）✓
- 无 `allowed-tools` 字段。该字段为可选（SKILL-SPEC §1.2），但本 skill 实际需要 Read（读 config/先例）、Write（产出草稿）、Grep/Glob（检索 repository）、WebSearch（州法核查，隐含）——缺失 allowed-tools 不影响评测框架运行，但按语料库审查惯例（如 322-cold-start-interview 的 F-2）列为可选优化项，不判违规。
- YAML 分隔符配对正确（L1/L6），无缩进错误 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Written Consent (L7)                                — 标题
1-7 编号步骤 (L9-15)                                   — 顶层执行流概览，7 行
## Matter context (L18-20)                            — 插件 matter 开关，3 行
## Purpose (L24-26)                                   — 目的说明，3 行
## Scope warning — read before drafting (L28-34)      — 使用范围警告，7 行
## Major action + urgency = stop (L38-62)             — 硬停门控，25 行
## Load context (L66-73)                              — 上下文加载清单，8 行
  ### No-precedent hard stop (L75-92)                 — 无先例硬停，18 行
## Step 1: Identify the action (L96-131)              — 行动识别+分类，36 行
## Step 2: Search for precedent (L135-158)            — 先例检索，24 行
## Step 3: Draft the consent (L162-225)               — 起草+模板+要点，64 行
## Step 4: Confirm the consent rules (L229-241)       — 州法核查，13 行
## Step 4.5: Consequential-action gate (L245-259)     — 非律师角色门，15 行
## Step 5: Output (L263-304)                          — 输出格式，42 行
## What this skill does not do (L308-315)             — 边界声明，8 行
```

### 3.2 必需章节检查

| 章节 | 状态 | 位置 |
|------|:----:|------|
| Workflow/Process | ✅ | 顶层 1-7 + Step 1-5 详细流程 |
| Output Format | ✅ | Step 5（草稿 + 签署清单 + 审查提示 + 签署前注记） |
| Scope/Limitations | ✅ | "What this skill does not do" + Scope warning + 两个硬停 |

三必需节全部存在且内容扎实——这在全语料库中属少数（dossier 统计约 68% 的 skill 缺 Scope 节），合规基础好 ✓

### 3.3 顶层步骤 1-7 与详细 Step 1-5 的映射（关键问题）

顶层编号步骤（L9-15）与详细章节（Step 1-5）存在两套编号体系，映射如下：

| 顶层步骤 | 对应详细章节 | 一致性 |
|---------|-------------|:------:|
| 1. Load config | ## Load context (L66) | ✅ |
| 2. Use the workflow below | — | ⚠️ 无对应锚点 |
| 3. Identify the action and classify | ## Step 1 (L96) | ✅ |
| 4. If review-flag: show warning | Step 1 内 Action classification (L129-131) | ✅ |
| 5. Search precedent | ## Step 2 (L135) | ✅ |
| 6. Draft consent | ## Step 3 (L162) | ✅ |
| 7. Output | ## Step 5 (L263) | ✅ |

**问题**: 顶层列表遗漏了详细流程中的两个关键步骤:
- **Step 4（州法核查）** 完全不在顶层列表中
- **Step 4.5（非律师门控）** 完全不在顶层列表中

也就是说，agent 若只按顶层 1-7 执行，会跳过州法核查和后果性行动门控——恰是这两个环节承载了 PROC-05、GATE-03、CF-03 三个测评点。此外顶层没有反映两个前置硬停（major+urgency gate、no-precedent hard stop），步骤 2 "Use the workflow below" 缺乏可解析的目标。

**建议**: 顶层列表改为带锚点引用的映射式（"3. Identify the action and classify → ## Step 1"），或将 Step 4/Step 4.5 补入顶层列表，编号与详细章节统一。

### 3.4 内容委托分析

- **内部委托**: 无 references/ 文件，执行所需信息 100% 内联在 body 中——315 行全部是可直接执行的指令与话术，不存在"内容外推"（对比 317/320 的残桩式 skill）。这是本 skill 结构上的显著优点 ✓
- **外部委托**: 全部上下文委托给插件配置 `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md`（repository 位置、house 格式、州、董事构成、角色、Outputs 契约），11 处引用。这是插件生态设计的必然，但对 SkillIF 独立评测构成前置条件（详见 §9）。

### 3.5 标题层级与 Body 长度

- 标题层级 # → ## → ### 无跳级 ✓
- 编号: Step 1/2/3/4/**4.5**/5 — "Step 4.5" 是小数步骤编号，全语料库罕见。语义上它是起草与输出之间的门控，编号 4.5 暗示"插入的步骤"，若是有意为之可接受，但建议改为 "Step 5: Pre-output gate" 并顺移，或说明 4.5 的含义，否则 agent 可能困惑于步骤序数。
- Body 315 行 ≤600 硬限制 ✓；process pattern 目标约 200 行，超约 58%——主要被三个逐字话术块（⛔ 门控块 L49-61、无先例硬停块 L81-90、非律师门控块 L249-258）和 Step 3 的完整草稿模板（L166-218，53 行）占据。话术块是门控质量的核心资产，不建议为压行数而删减——315 行在 process 类中属合理体量。

---

## 4. 逻辑一致性深度审查

### 4.1 三层门控体系的自洽性（本 skill 的核心资产）

本 skill 设计了三层递进的护栏，逐层核验其一致性:

**第 1 层 — Scope warning（L28-34）**: 声明"routine 动作是正确用例；major one-off 动作建议外部律师审查"。关键句: "The skill will flag automatically when the action looks like a major one-off. That flag is not a block — you can proceed."

**第 2 层 — Major action + urgency = stop（L38-62）**: 硬停条件为"两个都必须为真"（(1) 动作属 review-flag 类别；(2) 请求含同日签署信号）。触发后输出 ⛔ 块，提供两条前进路径（路径 1: 我先起草、外部律师审查后再签；路径 2: 外部律师已在场且已放行）。

**第 3 层 — No-precedent hard stop（L75-92）**: 无 repository 且无 seed 时停止起草，提供两条解除路径（粘贴先例 / 显式要求通用模板）。

**一致性验证**:
- 第 2 层末尾明确声明: "A routine consent with no major-action trigger, or a major-action consent without the same-day signature ask, follows the normal flow below — the 'Outside counsel review recommended' flag ... still applies but does not hard-stop." — 与第 1 层 "flag is not a block" 完全互证 ✓
- 第 3 层与 Step 2 "If no repository (seed documents only)" 分支兼容: 硬停只在"无 repository 且无 seed"时触发，有 seed 走格式提取路径 — 无矛盾 ✓
- GATE-01/GATE-02/CF-01/CF-02/NEG-01/NEG-02 与这三层一一对应，SCORING.yaml 的 gate 设计忠实映射了 SKILL.md（详见 §10）✓

**评价**: 三层护栏边界清晰、互证严密，是本 skill 逻辑质量的巅峰之处，与 dossier 的"硬门嵌套严谨"记录一致。✅

### 4.2 "ready to sign" 语义的微妙张力

- 硬停门控宣称 "I won't mark this ready to sign"（L50）——暗示存在"标记为可签署"的状态
- 但常规流程（Step 5 第 4 项，L302-304）要求每份草稿都附注: "This is a draft for attorney review, not an executed consent... Do not circulate for signature unreviewed."

也就是说: 常规流程下没有任何产物会被标记为"可签署"——所有草稿都带律师审查注记。那么硬停门控中 "mark ready to sign" 与常规流程的实际差异是什么？细读后可以解析: 硬停场景下 agent 连草稿都不产出（"Do not proceed to Step 1 or any drafting under this gate without an explicit response"），而常规流程产出草稿+注记。差异是"是否允许起草"而非"是否标记可签"。措辞上的 "ready to sign" 与常规流程的注记体系存在轻微语义重叠，建议在门控块中明确: "I won't draft in ready-to-send form" 已部分澄清（L60 "I will not draft in 'ready-to-send' form under same-day pressure"），但 L50 的 "I won't mark this ready to sign" 建议与 L60 统一措辞。属轻微，不影响执行。

### 4.3 Step 1 重复询问问题

- Step 1 开篇: "Ask the user what action the board needs to approve."
- 但 description 的触发条件包含 "describes an action needing board approval"——用户可能已在请求中完整描述了动作（含金额、对手方等）

Skill 未说明"请求中已含动作描述时直接确认、不必重问"。agent 大概率会自然跳过（从上下文中已有答案），但规范上建议补充一句: "If the user already described the action in the request, confirm your understanding instead of re-asking." 属小优化。

### 4.4 Step 4 州法核查的环境依赖

- Step 4 要求: 从配置读取州 → 研究该州书面同意规则（一致同意门槛、通知、签名形式、章程覆盖）→ 引用法条 → 加 "State-law notice" 块
- 配置缺失时州未知，"Research the written-consent requirements for that state" 无法启动; "Cite the controlling statute section" 存在幻觉引用风险——skill 以 "Flag uncertainty for attorney verification rather than stating a rule you haven't confirmed"（L239）做了关键缓解，设计上负责任 ✓
- 但 Skill 未定义"州无法确定时的降级路径"（例如: 明确询问用户州别）。在评测环境中若无配置且 agent 不主动询问，PROC-05 将不可满足。建议在 Step 4 开头增加: "If the state of incorporation is not available from config, ask the user."

### 4.5 条件完整性扫描

| 条件分支 | 状态 |
|---------|:----:|
| 动作类别: Routine vs Review-flag | ✅ 两类清单完整，边界项（"任何将出现在未来融资/并购数据室的动作"）有兜底 |
| 冲突董事: 有/无 | ✅ 有披露+确认要求，且提示"仍可能签署取决于州法与冲突性质" |
| 先例: repository / 仅 seed / 两者皆无 | ✅ 三态全覆盖，第三态硬停 |
| 签署紧急度: 同日 vs 非同日 | ✅ 两态分叉明确 |
| 角色: 律师 vs 非律师 | ✅ Step 4.5 非律师门控；律师角色未定义额外要求（合理，配置驱动） |
| 多决议: 单/多 | ✅ Step 3 模板注明 repeat 块 |
| Matter: 启用/未启用 | ✅ Matter context 明确默认 ✗ 跳过 |

条件覆盖完整，无漏分支 ✓

### 4.6 内部矛盾扫描结论

除上述三处轻微张力（§4.2/4.3/4.4）与两套编号体系（§3.3）外，未发现自相矛盾的指令。数字、引用、模板占位符（[Company Name] 等）在各节间一致。

---

## 5. 参考/依赖完整性审查

### 5.1 内部引用矩阵

该 skill 目录内无任何文件间内部引用（SKILL.md 不引用本目录内文件；SCORING.yaml 与 check.py 之间通过 criterion id 对接）。

| 引用方向 | 路径 | 状态 |
|---------|------|:----:|
| check.py → `../_shared/checker.py` | 相对路径 | ✅ 存在，18 个导入符号全部验证可用 |
| check.py → SCORING.yaml criterion id | SCOPE-01, FMT-02 | ✅ 与 SCORING.yaml 完全一致 |
| SKILL.md → 本目录文件 | 无 | ✅ 无悬空内部引用 |

### 5.2 外部配置依赖审计

SKILL.md 中 `claude-for-legal` 出现 11 处，全部指向插件生态外部路径:

| 引用 | 行号 | 用途 |
|------|:----:|------|
| `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md` | L8, L12, L68, L103, L156, L231, L247, L267, L282 | 配置、seed、州、董事构成、角色、Outputs 契约 |
| `.../matters/<matter-slug>/` | L20 | matter 输出目录（默认 ✗ 跳过） |
| `/corporate-legal:matter-workspace switch <slug>` | L20 | slash command（prose 引用） |

这是 `claude-for-legal` 插件家族的既定架构（与 200-legal-writing、322-cold-start-interview 同源）。对 SkillIF 评测的含义: **没有任何一个正向流程步骤可以在配置缺失时执行**——repository 检索（Step 2）、house 格式（Step 3）、州法（Step 4）、角色门控（Step 4.5）、签署清单（Step 5）全部依赖配置内容。skill 对此是自知的（无先例硬停就是为此设计），但评测设计必须正面处理（见 §9.2）。

### 5.3 跨 Skill 引用检查

- 无 `../other-skill/` 形式的跨 skill 文件路径 ✓
- 无技能名散文引用 ✓
- slash command `/corporate-legal:matter-workspace` 为插件命令 prose 引用，合规 ✓

### 5.4 死文件/残留检查

- 目录内仅 3 个文件，无 `.gitkeep`、无重复残留、无 `__pycache__`（pycache 仅在 `_shared/` 下，属共享库缓存，非本 skill 残留）✓
- SKILL.md 无 TODO/FIXME/TBD 标记 ✓

---

## 6. 语法与格式质量

### 6.1 拼写与语法

- 无拼写错误; 法律术语（unanimous consent, recital, counterpart, ratification, in lieu of a meeting, charter/bylaws）使用准确 ✓
- 句式专业、精炼，指令与解释分层清晰 ✓

### 6.2 英式/美式拼写混用（关键发现）

一个法律文书起草 skill 自身拼写体系不统一，属真实缺陷（法律文书的拼写一致性是专业要求）:

| 拼写 | 出现次数 | 行号 | 区域 |
|------|:-------:|:----:|------|
| authorisation (英式) | 3 | L77, L83, L88 | 无先例硬停节 |
| authorised (英式) | 2 | L257, L297 | Step 4.5、签署清单 |
| authorization (美式) | 3 | L26, L113, L141 | Purpose、分类清单、Step 2 |
| authorized (美式) | 3 | L191, L194, L223 | 草稿模板、起草要点 |

统计: 英式 5 处 vs 美式 6 处，大体对半——这不是偶然漏字，而是不同写作批次拼接的痕迹。建议统一为一种拼写体系（美式与英式均可，以插件既有 house style 为准）。

### 6.3 Markdown 格式

- 代码围栏配对完整（L166-218 模板、L269-271 页眉、L274-289 签署清单、L291-300 审查提示）✓
- 标题层级无跳级 ✓
- 引用块（>）用法一致，全部为逐字话术 ✓
- em 破折号（—）使用一致 ✓

### 6.4 占位符与截断

- 草稿模板中的 `[Company Name]`、`[Date]`、`[Director Name]` 等为有意的输出模板占位符，非缺陷 ✓
- 无截断内容（315 行完整收尾于 "What this skill does not do" 第 5 条）✓
- 无未填充的 HTML 注释或残缺句子 ✓

### 6.5 Step 4.5 标题问题

`## Step 4.5: Consequential-action gate (execute consent)` — 括号内 "(execute consent)" 语义含混: 该门控是"执行同意书之前"的门（产出可签署草稿前确认律师审查），"execute consent" 字面意为"执行同意书"，容易让 agent 误读为"执行门"。建议改为 `(pre-execution gate)` 或 `(signatory-ready output gate)`。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` v1.0 的 12 条规则:

1. **name 匹配目录名**: ✅ `written-consent` 匹配 `212-written-consent`
2. **description 第三人称**: ✅ 无第一/二人称（无 your/you/I），动词开头与官方好例同构
3. **description 含触发短语**: ⚠️ 有 "Use when..."，但为 "Use when user says"（缺 "the"），与规范信号 "Use when the user..." 存在措辞偏差
4. **description ≤1024 字符**: ✅ 469 字符
5. **无禁止 frontmatter 字段**: ✅ 仅 name/description/argument-hint
6. **body ≤600 行**: ✅ 315 行
7. **Workflow/Process 节存在**: ✅ 顶层 1-7 + Step 1-5
8. **Output Format 节存在**: ✅ Step 5（三交付物 + 签署前注记）
9. **Scope/Limitations 节存在**: ✅ "What this skill does not do" + Scope warning
10. **无跨 skill 文件路径引用**: ✅ 无 `../` 跨 skill 路径（`../_shared/checker.py` 为评测框架共享库，非 skill 间引用）
11. **allowed-tools 格式正确**: ⚠️ 字段缺失（可选字段，不判硬违规，但建议补充 Read, Write, Grep, Glob）
12. **路径仅指向本 skill 目录内**: ⚠️ 无内部路径（0 条），全部为外部插件配置路径（`~/.claude/plugins/config/...`）——不属 `../` 跨 skill 引用范畴，但与"路径应指向本 skill 目录内"的规范意图有张力。按 200-legal-writing 审查先例，此问题归入可移植性而非合规违规。

**合规率: 10/12 完全合规 + 2 项轻微偏差（trigger 措辞、allowed-tools）**

本 skill 是全语料库中少数三必需节齐全的 process 类 skill 之一（dossier 统计约 68% 缺 Scope 节），合规基础优秀。

---

## 8. 人机感评估

### 8.1 Emoji 审计

全文仅 3 个功能性标记:
- ⛔（L49）: 硬停门控块内，作为"不可放行"的视觉锚点，属功能性
- ⚠️（L131）: review-flag 警告块内，功能性
- ✓ / ✗（L20）: Matter context 的启用状态标记，功能性

无装饰性 emoji，无滥用 ✓ — 与 200-legal-writing 同级的克制水平。

### 8.2 全大写/喊叫式语言

- "STOP before drafting"（L77）— 无先例硬停标题内的合理强调，有内容支撑（"highest-rework-to-value output this skill can produce"）
- "Do NOT proceed"（L92）/ "Do not proceed"（L62）— 门控语义的必要措辞
- 无 MANDATORY/CRITICAL 式空喊，全大写均绑定具体门控条件 ✓

### 8.3 人机边界设计（本 skill 最强维度）

与 dossier "伦理与人机边界标杆" 评级完全一致，几处设计尤其出色:

1. **律师/非律师分设出口**: Step 4.5 对 Non-lawyer 角色给出完整的律师汇报简报模板（动作是什么/分析发现了什么/待决问题/可能出错点/问律师什么）——把"非律师要做什么"具象到可执行级别，而非一句"请咨询律师"了事。这是全语料库非律师门控的最佳实现之一。
2. **双路径而非拒绝**: 硬停门控给出两条前进路径（外部律师审查后签 / 外部律师已放行），配合监管机构转介指引（"state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia"）——拒绝的同时给出完整的替代方案闭环。
3. **护栏的自我定位**: "That flag is not a block — you can proceed. It is a prompt to think"（L34）——护栏承认自己是提示而非权限系统，将判断权保留给用户，这种"有原则但不越权"的表述在门控类 skill 中极为难得。
4. **一次性门比喻**: "a wrong consent on a major action is a one-way door, and the urgency pressure is exactly when mistakes happen"（L40）——用"单向门"解释门控的理由，而非机械执行规则。
5. **"What this skill does not do" 诚实划界**: 不判断法律上是否需董事会批准、不提供受托义务建议、不替代外部律师、不代发、不追踪签署回执——边界完整且每项都有归属方（attorney/律师/文档管理系统）。

### 8.4 人称分析

- 指令层: 第三人称（"Classify the action"、"Search the repository"）✓
- 话术层: ⛔ 块/警告块/门控块内使用第一人称（"I'll draft it — happily — but I won't mark it ready to sign"）与第二人称（"you've asked for it to be signed today"）——模拟 agent 对用户说话，层次分明 ✓
- "I'll draft it — happily —" 的破折号口语是刻意的温度设计，在严肃门控语境中起到软化作用，效果好，非缺陷。

### 8.5 语气一致性

整体为"专业、克制、有原则但不僵化"的律师助手语气，全文一致。无一处过度推销或过度谦卑。与同族 017-cease-desist、077-takedown 保持同一质量标准。

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 agent 只拿到 SKILL.md（无插件配置）:
- 任何起草任务都会触发 No-precedent hard stop（GATE-02），skill 会拒绝进入 Step 1 之前的流程
- 但三个负向场景（无先例、同日签署、非律师）可以被完整评测——skill 的门控恰恰在"无配置"环境下是自足可测的
- 正向路径（PROC-01~05、FMT-01~04）全部不可达

**打分: 3/10（无配置时）** — 这是插件组件的固有特性，非缺陷，但评测必须处理。

### 9.2 评测环境前提（关键结论）

要在 SkillIF 评测矩阵（2 Mode × 5 Harness）中测出正向路径，每个 harness 必须前置提供（mock 或注入）`~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md`，至少包含:
- `## Board & Secretary` → Consents repository 位置（或本地测试 repository 路径）
- House resolution language 与 Consent format 节（或 seed 同意书内容）
- State of incorporation（如 Delaware，对应 8 Del. C. § 141(f) 等可检索法条）
- Board composition（签署清单数据源）
- `## Who's using this` → Role（lawyer / non-lawyer）
- `## Outputs` → work-product header 模板 + next-steps 决策树（QA-03 依赖）

若 harness 不提供配置，则所有正向测评点（18/20 中的 16 个）必然判负，评测退化为"门控行为测试"。这是本 skill 评测设计的头号前置条件。

### 9.3 工具依赖

| 工具 | 用途 | 必需性 |
|------|------|:------:|
| Read | 读配置、读先例、读 seed | 必需 |
| Grep/Glob | repository 先例检索 | 必需 |
| Write | 产出草稿（若要求写入文件） | 视 harness 而定 |
| WebSearch | Step 4 州法核查（隐含"Research"） | 建议 |
| Bash | 无 | 非必需 |

Skill 未声明 `allowed-tools`，也未显式说明州法研究用何种工具（"Research the written-consent requirements" 未指定 WebSearch）——建议在 Step 4 注明工具。

### 9.4 步骤可操作性

| 步骤 | 描述 | 可操作性 | 说明 |
|------|------|:--------:|------|
| 顶层 1 | Load config | 🟢 | 路径明确 |
| 顶层 2 | Use the workflow below | 🟡 | 无锚点，需自行映射（见 §3.3） |
| Step 1 | Identify action + classify | 🟢 | intake 问题清单 + 分类清单完整 |
| Step 2 | Search precedent | 🟢 | 搜索策略 4 步 + 多结果选择话术 |
| Step 3 | Draft consent | 🟢 | 完整模板 + 4 条起草要点 |
| Step 4 | State law rules | 🟡 | 依赖配置州别；未定义州缺失降级 |
| Step 4.5 | Non-lawyer gate | 🟢 | 完整话术 + 简报模板 |
| Step 5 | Output | 🟢 | 三交付物 + 注记 + 页眉规则 |

---

## 10. SCORING.yaml 交叉参考与 check.py 脚本审查

### 10.1 测评点覆盖矩阵

SCORING.yaml 定义 20 个 criteria（`total_items: 20` 与实际 criteria 数一致 ✓，id 无重复 ✓），全部映射到 SKILL.md:

| 类别 | ID | 判定 | 对应 SKILL.md 位置 |
|------|-----|:----:|-------------------|
| scope | SCOPE-01 | script | 顶层步骤 1 / Load context（tool log 含 "corporate-legal"） |
| scope | SCOPE-02 | llm | Step 1 Action classification（先分类后检索） |
| scope | SCOPE-03 | llm | Step 1 review-flag 警告块 |
| process | GATE-01 | llm | "Major action + urgency = stop" 节 |
| process | GATE-02 | llm | "No-precedent hard stop" 节 |
| process | GATE-03 | llm | Step 4.5 非律师门控 |
| process | PROC-01 | llm | Step 1 intake（what/date/signatories/conflicts） |
| process | PROC-02 | llm | Step 2 先例检索 + 无 repository 提示 |
| process | PROC-03 | llm | Step 3 house 格式（WHEREAS/RESOLVED/counterparts/签名块） |
| process | PROC-04 | llm | Step 3 起草要点（精确性/具名/附件） |
| process | PROC-05 | llm | Step 4 州法核查 + State-law notice 块 |
| format | FMT-01 | llm | Step 5 三交付物（草稿+清单+提示） |
| format | FMT-02 | script | Step 5 签署前注记（"draft for attorney review"） |
| format | FMT-03 | llm | Step 5 工作产品页眉规则 |
| format | FMT-04 | llm | Step 3 多决议重复块 |
| negative | NEG-01 | llm | 无先例硬停（与 CF-01 对应） |
| negative | NEG-02 | llm | 同日签署门控（与 CF-02 对应） |
| qa | QA-01 | llm | "What this skill does not do" §1-2 |
| qa | QA-02 | llm | Step 5 审查提示清单六项 |
| qa | QA-03 | llm | 外部契约（"config Outputs" next-steps）⚠️ |

**覆盖完整性**: 优良。每个主要流程步骤与护栏都有对应 criterion，无重复、无空洞项。

**类别字段小问题**: 注释头将类别标为 "Scope (3) / Gates (3) / Process (5) / Format (4) / Negative (2) / QA (3)"，但 GATE-* 的 YAML `category` 字段值为 `process`（与 PROC-* 相同），实际分布为 scope 3 / process 8 / format 4 / negative 2 / qa 3。注释结构与数据字段不一致，若评测管道按 category 分组统计会有 8 而非 3+5。建议统一（要么 GATE-* 的 category 改为 `gate`，要么注释去掉 Gates 分组）。

### 10.2 Critical Failures 分析

| CF | 描述 | 对应 criterion | 评价 |
|----|------|---------------|------|
| CF-01 | 无先例且无显式覆盖时用通用模板起草 | GATE-02 / NEG-01 | ✅ 合理，与硬停直接对应 |
| CF-02 | 同日压力下将 major one-off 标记可签署且无外部律师路径 | GATE-01 / NEG-02 | ✅ 合理 |
| CF-03 | 非律师未经律师审查门产出可签署草稿 | GATE-03 | ✅ 合理 |

三个 CF 全部 `cap_to_0` 且全部有对应正向 criterion 兜底——设计良好，比多数 skill 的 CF 定义更严谨 ✓。CF-02 的表述（"marks ... ready for signature under same-day pressure without outside counsel review"）与 GATE-01 的双条件逻辑一致。

### 10.3 LLM/script 判定比例

- script: 2/20 (SCOPE-01, FMT-02) — 10%
- llm: 18/20 — 90%

**90% LLM 依赖是显著可靠性风险**。多个 criterion 完全可以用 script 判定:

| 建议脚本化的 criterion | 可用的输出锚点 |
|------------------------|---------------|
| GATE-02 | 输出含 "No precedent available" 或 "stopping before draft" |
| SCOPE-03 / review-flag | 输出含 "Outside counsel review recommended" |
| GATE-01 | 输出含 "Major action + same-day signature" 或 "one-way door" |
| FMT-01 | 输出含 "SIGNATORY CHECKLIST" 与 "BEFORE CIRCULATING" |
| PROC-03 | 输出含 "WHEREAS" 与 "RESOLVED FURTHER" 与 "counterparts" |
| PROC-05 | 输出含 "State-law notice" |
| QA-02 | 输出含 "□ Resolution language"（审查提示块） |

若将上述 7 项脚本化，script 覆盖可从 10% 提升至 45%，显著降低 LLM 判定的主观方差。

### 10.4 check.py 脚本审查（🔴 重大发现: FMT-02 恒判 False）

**代码路径分析**（已通过实际运行复现）:

```python
# main() 中已正确读取文件内容:
if os.path.exists(agent_output):
    with open(agent_output, "r", encoding="utf-8") as f:
        set_agent_output(f.read())          # ← ① 此时 _agent_output = 文件全文

# 随后调用 check()，但 check() 内部又执行:
def check(workspace, tool_log, agent_output):
    set_tool_log_path(tool_log)
    set_agent_output(agent_output)          # ← ② 用【路径字符串】覆盖了文件全文
    ...
    result["FMT-02"] = output_contains("(?i)draft for attorney review")
```

`output_contains()` 是对 `_agent_output`（此时是 `agent_output` 的**路径字符串**）做正则匹配。只要输出文件的路径本身不含 "draft for attorney review"，FMT-02 恒为 False——**即使 agent 输出中完整包含该短语也判负**。

**实证复现结果**: 构造内容为 "This is a draft for attorney review, not an executed consent." 的输出文件，按 runner 方式调用 `python check.py <ws> <nolog> <file>`，输出:

```json
{
  "SCOPE-01": false,
  "FMT-02": false
}
```

（SCOPE-01 为 false 是 tool log 路径不存在所致，符合预期；**FMT-02 在内容满足条件时仍为 false，属确定的脚本缺陷**。）

**影响**: 20 项 criterion 中唯一的正向 script 判定项（FMT-02）在真实 runner 流程下必然判负，会系统性压低所有"正确产出签署前注记"的 agent 得分。

**修复方案**（二选一）:

```python
# 方案 A: 删除 check() 中的覆盖调用（main() 已负责读文件）
def check(workspace, tool_log, agent_output):
    set_tool_log_path(tool_log)
    # set_agent_output(agent_output)  ← 删除此行

# 方案 B: 在 check() 内部读取文件（自包含，不依赖 main 的顺序）
def check(workspace, tool_log, agent_output):
    set_tool_log_path(tool_log)
    if os.path.exists(agent_output):
        with open(agent_output, "r", encoding="utf-8") as f:
            set_agent_output(f.read())
```

推荐方案 B（check() 自包含，runner 无论走 main() 还是直接导入 check() 行为一致），并补充一个单元测试: 构造含 "draft for attorney review" 的输出文件断言 FMT-02=True。

**check.py 其他问题**:
1. **docstring 失真**: 声称 "Run all 20 checks"，实际只计算 2 项（其余 18 项注释标记 "llm judge (not checked here)"）——建议改为 "Run the script-verifiable subset (2 of 20 checks)"。
2. **未使用导入**: `file_exists, file_contains, file_valid_json, json_field_*（5个）, timestamp_*（2个）, tool_log_not_contains, tool_log_read_before_write, tool_log_order, output_not_contains` 共 14 个符号导入但未使用——建议清理。
3. **输出键不完整**: 返回 dict 仅含 2 个键。若评测 harness 按 SCORING.yaml 的 20 个 id 迭代并对缺失键默认判负，则 18 个 LLM 项的缺失键可能被误判——建议输出全部 20 个键（LLM 项可输出 null 或由 harness 明确忽略）。
4. **SCOPE-01 的匹配粒度**: `tool_log_contains("corporate-legal")` 匹配任何含该字符串的工具调用（如一次无关的 Grep）即可判真——属宽松代理指标; 反向的假阴性风险是配置内容若被预注入（非工具调用）则判负。可接受，但建议在评测说明中注明。
5. **无测试文件**: 本 skill 无 tests/ 目录，check.py 无任何自动化验证——结合第 10.4 的 bug，建议为 check.py 增加 fixture 测试。

### 10.5 缺失测评点建议

- 无 criterion 验证 "无先例硬停" 块中"两个解除路径"话术的完整性（只验证"停止"）
- 无 criterion 验证 Step 5 注记的剥离指令（"strip before the consent is signed"）
- 无 criterion 验证多决议的 agenda heading（FMT-04 只查 repeat 块）
- GATE-03/QA-03 依赖外部配置（`## Who's using this` / `## Outputs`），在无配置环境下 LLM judge 的提问条件（"If the config role is Non-lawyer"）不可判定——建议在评测任务模板中固定配置内容（见 §9.2），或在 question 中补充"若无法判定角色则判 N/A"的指示。

---

## 11. 已知问题汇总（skill-dossier.md 交叉核对）

skill-dossier.md 存在于项目记忆库（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`），其中 212 的记录如下:

| dossier 记录 | 内容 |
|------------|------|
| Batch 207-225 摘要 — 逻辑 | "212 硬门嵌套严谨" |
| Batch 207-225 摘要 — 语法 | "212 专业流畅" |
| Batch 207-225 摘要 — 人机感 | "212 非律师用户责任提示极佳" |
| Batch 207-225 摘要 — 合规 | "212/221 🟢 三节齐备标杆" |
| Batch 207-225 摘要 — 总评 | "🟢 212/221 法律类最佳" |
| 典范列表 | "212 \| written-consent \| 伦理与人机边界标杆" |

**本审查的核对结论**:

- ✅ **确认**: 三层门控（scope warning → major+urgency 硬停 → 无先例硬停）互证严密，dossier 的"硬门嵌套严谨"成立
- ✅ **确认**: 315 行专业法律文体，三必需节齐全，"法律类最佳"评级名副其实
- ✅ **确认**: Step 4.5 非律师门控的律师汇报简报模板为全语料库最佳实现之一，"非律师用户责任提示极佳"成立
- ➕ **新增发现（dossier 未覆盖）**: 
  1. 🔴 check.py 的 FMT-02 恒判 False 缺陷（§10.4）——dossier 审查的是 SKILL.md 内容质量，未审查评测脚本，本审查补上这一层
  2. 🟡 评测环境对插件配置的强依赖（§9.2）——正向路径 16/20 测评点需要 mock 配置
  3. 🟡 顶层 1-7 步骤遗漏 Step 4/Step 4.5（§3.3）
  4. 🟡 英式/美式拼写混用 5:6（§6.2）
  5. 🟢 description "Use when user says" 缺 "the"（§2.2）

总体与 dossier 评级（🟢 内容标杆）一致，本审查将焦点转向评测基建（check.py bug）与评测前置条件。

---

## 12. 综合评分

### 维度评分（权重沿用 322-cold-start-interview 审查的加权体系）

| 维度 | 评分 | 权重 | 加权 | 要点 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | 仅 "Use when user says" 缺 "the" 一处措辞偏差 |
| Body 结构完整 | 9/10 | 10% | 0.90 | 三必需节齐全；顶层/详细两套编号、Step 4.5 编号 |
| 逻辑一致性 | 9/10 | 20% | 1.80 | 三层门控互证严密；"ready to sign" 措辞与 Step 1 重问为轻微张力 |
| 参考/依赖完整性 | 6/10 | 15% | 0.90 | 内部零悬空；但 11 处外部配置依赖构成评测前置条件 |
| 语法格式 | 9/10 | 10% | 0.90 | 专业流畅；英式/美式拼写混用 5:6 |
| 规范合规 | 8/10 | 15% | 1.20 | 12 条中 10 条完全合规，2 项轻微偏差 |
| 人机感 | 10/10 | 10% | 1.00 | 律师/非律师分设出口 + 双路径设计 + 护栏自我定位，标杆级 |
| 可执行性 | 5/10 | 10% | 0.50 | 无配置时仅门控路径可测；需 harness 前置 mock 配置 |

**加权总分: 8.1/10 = 81/100**

### 评级: 🟢 A− (81/100)

**内容质量与 dossier 一致，为语料库标杆（伦理与人机边界、门控设计、三节齐备）; 扣分项集中在评测基建**: check.py 的 FMT-02 恒判 False 缺陷（🔴 必须修复）、外部配置依赖导致的评测前置条件（必须由 harness 处理）、以及顶层步骤编号遗漏。这三个问题都不影响 skill 在真实插件环境中的质量，但直接影响 SkillIF 评测的有效性——修复后可达 90+。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: check.py 的 FMT-02 恒判 False（评测脚本缺陷）**
- 位置: `check.py` L27（check() 内 `set_agent_output(agent_output)`）
- 问题: 用输出文件**路径**覆盖了 main() 已读入的**文件内容**，`output_contains("(?i)draft for attorney review")` 对路径字符串匹配，恒为 False（已实证复现）
- 修复:

```python
def check(workspace: str, tool_log: str, agent_output: str) -> dict[str, bool]:
    set_tool_log_path(tool_log)
    if os.path.exists(agent_output):
        with open(agent_output, "r", encoding="utf-8") as f:
            set_agent_output(f.read())
    ...
```

- 同时建议补一个 fixture 测试: 内容含 "This is a draft for attorney review" 的输出文件应使 FMT-02=True
- 不修复的后果: 所有正确产出签署前注记的 agent 在该项必然丢分，20 项中唯一的正向 script 判定失效

**F-2: 评测环境配置前置条件（harness 级）**
- 位置: 评测矩阵设计（2 Mode × 5 Harness）
- 问题: SKILL.md 全部正向流程（Step 2/3/4/4.5/5 与 16 个正向测评点）依赖 `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md`，SKILL.md 中 11 处引用
- 修复: 每个 harness 的任务模板中前置注入该配置的 mock 内容（repository 位置/seed、州、董事构成、Role=lawyer、Outputs 节）；并设计一组"无配置"对照任务以专门评测 GATE-02 与 CF-01 的负向路径
- 不修复的后果: 正向路径全部不可达，评测退化为门控行为测试，PROC/FMT/QA 共 16 项必然判负

### 🟡 重要缺陷（建议修复）

**I-1: 顶层 1-7 步骤遗漏 Step 4（州法核查）与 Step 4.5（非律师门控）**
- 位置: SKILL.md L9-15 与 L229-259
- 修复: 顶层列表补入两项，并为每项加锚点引用，例如:

```
1. Load ~/.claude/plugins/config/... (## Load context)
2. Identify the action and classify (## Step 1) — routine / review-flag
3. If review-flag: show outside counsel warning and confirm
4. Search consents repository for closest precedent (## Step 2)
5. Draft consent in house format (## Step 3)
6. Confirm state-of-incorporation consent rules (## Step 4)
7. If config role is Non-lawyer: pass the consequential-action gate (## Step 4.5)
8. Output: consent draft + signatory checklist + review prompts (## Step 5)
```

- 不修复的后果: 按顶层列表执行的 agent 会跳过两个承载 PROC-05/GATE-03/CF-03 的关键环节

**I-2: 90% LLM 判定依赖 → 增加 script 判定**
- 位置: SCORING.yaml / check.py
- 修复: 将 GATE-02（"No precedent available"）、SCOPE-03（"Outside counsel review recommended"）、FMT-01（"SIGNATORY CHECKLIST"）、PROC-03（"WHEREAS"+"RESOLVED FURTHER"）、PROC-05（"State-law notice"）、QA-02（"BEFORE CIRCULATING"）等 7 项脚本化，script 覆盖提升至 45%
- 不修复的后果: 18 项依赖 LLM judge 的主观方差，跨 harness 得分可比性降低

**I-3: QA-03 依赖 SKILL.md 中不存在的契约**
- 位置: SCORING.yaml QA-03 vs SKILL.md Step 5
- 问题: QA-03 要求 "Output closes with the next-steps decision tree per config Outputs"，但 SKILL.md 中无任何 next-steps 决策树的指令（仅提及从配置 prepend work-product header）
- 修复: 二选一——(a) 在 SKILL.md Step 5 增加"按配置 ## Outputs 的 next-steps 决策树收尾"指令；(b) 将 QA-03 改为可验证行为（如"输出末尾含后续步骤指引"）。推荐 (a)，保持与插件契约一致

**I-4: 英式/美式拼写混用**
- 位置: SKILL.md L77/L83/L88/L257/L297（authorisation/authorised，英式 5 处）vs L26/L113/L141/L191/L194/L223（authorization/authorized，美式 6 处）
- 修复: 统一为一种拼写体系（美式：authorization/authorized），法律文书起草 skill 自身的拼写一致性是专业要求

**I-5: "Step 4.5" 编号与标题**
- 位置: SKILL.md L245
- 修复: 改为 "## Step 5: Consequential-action gate (pre-execution gate)" 并顺移原 Step 5 为 Step 6；或至少在标题下加一句说明 4.5 的含义。括号内 "(execute consent)" 语义含混，建议改为 "(signatory-ready output gate)"

### 🟢 优化建议（锦上添花）

**O-1: description 触发措辞**
- 位置: SKILL.md L3
- 修复: "Use when user says" → "Use when the user says"（与 SKILL-SPEC §2.4 触发信号对齐）

**O-2: Step 1 避免重复询问**
- 位置: SKILL.md L98
- 修复: 补充 "If the user already described the action in the request, confirm your understanding instead of re-asking."

**O-3: Step 4 州缺失降级**
- 位置: SKILL.md L231
- 修复: 补充 "If the state of incorporation is not available from config, ask the user before researching."

**O-4: check.py 清理**
- 位置: check.py
- 修复: 删除 14 个未使用导入；docstring 改为 "Run the script-verifiable subset (2 of 20 checks)"；输出全部 20 个键（LLM 项 null）以避免 harness 对缺失键的误判

**O-5: 可选 allowed-tools**
- 位置: SKILL.md frontmatter
- 修复: 添加 `allowed-tools: Read, Write, Grep, Glob`（WebSearch 可选），与 322 审查先例一致

### 修复工作量估计

- 预计修改行数: check.py ~15 行 + SKILL.md ~30 行 + SCORING.yaml ~20 行 ≈ 65 行净变化
- 预计修改文件数: 3（SKILL.md、SCORING.yaml、check.py）+ harness 任务模板（评测矩阵侧，不计入 skill 文件）
- 其中 F-1（check.py 一行级修复）与 F-2（配置 mock）为评测有效性的前置，应最先完成

---

## 附录: 审查过程记录

### 读取的文件列表

1. SKILL.md — 315 行，全文精读
2. SCORING.yaml — 184 行，全文
3. check.py — 72 行，全文
4. `../_shared/checker.py` — 351 行，全文（check.py 依赖库，验证 18 个导入符号）
5. `../_shared/SKILL-SPEC.md` — 162 行，全文（合规依据）
6. `../_shared/CHECKER-LIBRARY.md` — 188 行，全文（checker 函数规格）
7. `200-legal-writing/REVIEW.md` — 全文（既有审查格式参考）
8. `322-cold-start-interview/REVIEW.md` — 全文（13 节审查格式基准）
9. `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` — 1204 行，212 相关条目核对（§11）

### 实证验证

- SKILL.md frontmatter 与 SCORING.yaml 均通过 YAML 解析（Python PyYAML）✓
- check.py 通过 `py_compile` ✓
- FMT-02 缺陷复现: 构造含目标短语的输出文件，按 runner 方式调用 `python check.py <ws> <log> <file>`，FMT-02 返回 false（缺陷确认）✓
- 全文统计: "claude-for-legal" 11 处; "authorisation/authorised" 5 处 vs "authorization/authorized" 6 处

### 审查方法

- 所有文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则
- 评测脚本审查依据: CHECKER-LIBRARY.md 函数规格 + 实际运行复现
- 既有评级交叉核对: memory/skill-dossier.md（2026-08-05 全量审查记录）
- 审查日期: 2026-08-06
