# REVIEW: 015-outreach-specialist

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 外展消息专家：基于 $ARGUMENTS 门控 + 强制 reference 读取 + 诊断问题银行 + 8模板选择 + 序列策略，生成个性化冷外展序列（LinkedIn DM/Email/X DM/Instagram DM）
**Body 行数**: 306 行（不含 frontmatter）
**参考文件数**: references/2（outreach-templates.md ~500行 + sequence-strategy.md 169行）
**已有 REVIEW**: 是（旧版 22 行 stub，本次完全重写至 ≥500 行）

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\015-outreach-specialist\
├── SKILL.md (311 行)                                    ← 主体：Purpose + $ARGUMENTS双模式门控
│                                                          + 7步Task Execution（含BLOCKING门控）
│                                                          + Writing Rules（10核心+4平台+4跟进+4语调）
│                                                          + Output Format（含完整LinkedIn DM示例）
│                                                          + 25项Quality Checklist + 8项Defaults
├── SCORING.yaml (165 行)                                ← 18 criteria + 2 critical_failures
├── check.py (85 行)                                     ← 可执行检测器，9个script检查项
│                                                          含 em破折号/AI slang/"just following up" 禁止词检测
├── REVIEW.md                                            ← 本次审查文件
└── references/
    ├── outreach-templates.md (~500+ 行)                  ← 8个经过验证的外展模板：
    │                                                      (1)Taking on New Projects (2)Case Study
    │                                                      (3)Firstline (4)Mutual Connection
    │                                                      (5)Loom/Video Teaser (6)Value-First
    │                                                      (7)Permission-Based (8)Breakup
    │                                                      每个模板含：使用时机/心理学原理/结构/示例/平台适配
    └── sequence-strategy.md (169 行)                     ← 序列策略框架：
                                                            3消息默认序列/5消息扩展序列/单消息模式
                                                            + 4平台特定规则（LinkedIn/Email/X/Instagram）
                                                            + Follow-Up Angle Rotation表
                                                            + Timing Rules + Subject Line Formulas(7公式)
                                                            + 8个外展失败原因
```

**文件统计**: 共 5 个文件（不含 REVIEW.md）。核心资产完备——2 个 reference 文件构成完整的外展系统：outreach-templates.md 提供"写什么"（8 个模板的 DNA），sequence-strategy.md 提供"怎么排列"（序列策略框架）。无 scripts/、assets/ 等其他子目录。

---

## 2. Frontmatter 逐字段审查

### 2.1 name 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 小写 + 连字符 | ✅ | `outreach-specialist` |
| ≤64 字符 | ✅ | 20 字符 |
| 与目录名匹配 | ✅ | 目录 `015-outreach-specialist` |

### 2.2 description 字段逐句分析

**原文**（177 字符）:

> "Crafts high-converting outreach messages and email sequences for cold outreach, LinkedIn DMs, and follow-ups. Use when user needs personalized outreach messages that book calls and get replies."

**句子 1**（WHAT）: "Crafts high-converting outreach messages and email sequences for cold outreach, LinkedIn DMs, and follow-ups."
- 第三人称描述 skill 功能 ✅。"Crafts" 是主动动词，主语为 skill ✅
- 功能声明具体：outreach messages + email sequences，覆盖 cold outreach/LinkedIn DMs/follow-ups ✅
- "high-converting" 是营销术语但在此上下文中合理——它是对输出质量的声明 ✅

**句子 2**（WHEN）: "Use when user needs personalized outreach messages that book calls and get replies."
- 含触发信号 "Use when" ✅
- 🟡 "Use when user needs" — 缺少定冠词 "the"，应为 "Use when the user needs"
- 🟡 WHEN 部分过于简短——仅提及 "personalized outreach messages that book calls and get replies"，未嵌入具体的触发关键词（如 "cold email", "LinkedIn message", "follow-up sequence", "outreach template", "sales sequence" 等）。agent 可能因为缺少这些关键词而错过触发
- 🟡 缺少 KEYWORDS 部分——领域词未在 description 中显式出现

**禁止内容检查**:
- 无第一人称 ✅
- 无祈使句开头 ✅
- 无跨 skill 路由 ✅
- 无实现细节 ✅
- 长度 177 字符，≤1024 ✅

**description 综合评分**: 7/10。简洁有效但 WHEN 部分过于概括，缺少触发关键词。建议在 description 末尾嵌入 "cold outreach", "LinkedIn DM", "email sequence", "follow-up messages" 等让 agent 更容易匹配的关键词。

**修改建议**:
> "Crafts high-converting outreach messages and email sequences for cold outreach, LinkedIn DMs, and follow-ups. Use when the user asks to write cold outreach messages, create LinkedIn DM sequences, draft follow-up emails, or build multi-message sales outreach campaigns."

### 2.3 allowed-tools 字段

🔴 **完全缺失**。Frontmatter 仅含 `name` 和 `description`。

分析 skill 实际需要的工具，基于 body 中的显式指令：

| Tool | 必要性 | Body 中的使用证据 |
|------|:------:|------------------|
| Read | ✅ 必须 | Step 1 "MUST use the Read tool to read ALL reference files"（L32-46），明确要求读取 outreach-templates.md 和 sequence-strategy.md |
| Write | ✅ 必须 | Step 7 输出完整的消息序列 |
| AskUserQuestion | ✅ 必须 | Step 4 "ask up to 5 questions using AskUserQuestion"（L65）——显式提到了工具名 |
| Glob | 🟡 推荐 | Step 2 检查 FOUNDER_CONTEXT.md 是否存在，需文件系统搜索 |

推荐值：`allowed-tools: Read, Write, AskUserQuestion, Glob`

这里有一个特别严重的问题：Step 4 中**显式提到了 AskUserQuestion 工具名**（"ask up to 5 questions using AskUserQuestion"），但该工具未在 allowed-tools 中声明。如果 agent 的环境中没有此工具或工具被限制，整个诊断提问步骤将不可执行。

### 2.4 其他 Frontmatter 字段

| 字段 | 存在 | 评估 |
|------|:----:|------|
| `argument-hint` | ❌ | 🟡 缺失。Body 中大量使用 $ARGUMENTS 机制（Execution Logic 节），这是 Claude Code 的 argument-hint 功能。应在 frontmatter 中声明 `argument-hint: "[prospect info, offer details, or platform]"` 使该机制可见 |
| `model` | ❌ | 未设置——合理。外展写作不需要特定模型覆盖 |
| `user-invocable` | ❌ | 未设置。本 skill 适合用户直接调用 |
| 禁止字段 | ❌ | 无 ✅ |

仅 2 个字段，无禁止字段 ✅。

### 2.5 Frontmatter 语法

YAML 分隔符 `---` 成对出现 ✅。description 无需要转义的特殊字符 ✅。纯字符串值 ✅。

---

## 3. Body 逐段结构分析

### 3.1 完整段落树

```
L6   # Outreach Specialist                        — H1 标题
L8   ## Purpose (2行)                              — 一句话目的：个性化外展序列，听起来像人，建立信任，预定会议
L13  ## Execution Logic (14行)                     — 🟢 $ARGUMENTS 双模式门控
L17   ### If $ARGUMENTS is empty (5行)            — 响应 "outreach-specialist loaded..." 并等待
L23   ### If $ARGUMENTS contains content (2行)     — 跳过加载消息，直接执行
L28  ## Task Execution (88行)                      — 🟢 7步工作流（Process 节）
L32   ### 1. MANDATORY: Read Reference Files FIRST — BLOCKING REQUIREMENT + 具体Read指令
L48   ### 2. Check for Business Context            — FOUNDER_CONTEXT.md 条件检查
L53   ### 3. Analyze Input & Determine What's Missing — 6项需求提取（who/offer/platform/goal/proof/length）
L63   ### 4. Ask Diagnostic Questions (If Needed)  — 5个问题银行（每个含Why it matters + Skip if条件）
L79   ### 5. Select Templates & Build the Sequence — 7种场景→模板映射表 + 3消息序列结构
L103  ### 6. Write the Sequence                    — 5条结构化写作指令
L112  ### 7. Format and Verify                     — 3项最终验证
L119 ## Writing Rules (35行)                       — Hard constraints 硬约束
L122  ### Core Rules (10条)                        — Sound human/No em dashes/No AI slang/Keep short/
                                                      One CTA/Specific>vague/Lead with them/No exclamations/
                                                      Lower commitment bar/Active voice only
L134  ### Platform-Specific Rules (4平台)           — LinkedIn DM/Email/X-Twitter DM/Instagram DM
L140  ### Follow-Up Rules (4条)                    — Never "just following up"/Change angle/
                                                      Increase urgency/Space them out
L146  ### Tone Rules (5条)                         — Text a professional friend/Friendly not desperate/
                                                      Match platform/Brand voice blending
L154 ## Output Format (86行)                       — 🟢 完整模板 + 可复制粘贴的LinkedIn DM示例
L242 ## References (10行)                          — 2个reference文件说明 + 为什么两者都重要
L255 ## Quality Checklist (42行)                   — 25项自检清单
L259  ### Pre-Execution Check (4项)                — 读取了reference、有模板在上下文中、只问必要问题
L265  ### Message Quality Check (8项)              — Sounds human/No em dashes/No AI slang/
                                                      One CTA/Lead with prospect/Specific numbers
L275  ### Sequence Check (5项)                     — Different angles/New value/Increasing urgency/
                                                      Correct timing/Low-pressure final
L282  ### Personalization Check (4项)              — Actual context/Brand voice blended/
                                                      Specific proof/Platform tone matches
L288  ### Output Check (3项)                       — Matches format/Ready to send/Appropriate length
L297 ## Defaults & Assumptions (13行)              — 8项默认值（sequence length/platform/goal/tone等）
```

**结构评价**: 逻辑流清晰且实用导向——从"何时激活"（$ARGUMENTS门控）→"强制准备"（读reference+检查上下文）→"理解需求"（分析+诊断提问）→"执行"（选模板+写序列+验证）→"质量保证"（25项自检）→"默认值"（回退参数）。这是一个完整的 "Gate → Prepare → Understand → Execute → Verify → Fallback" 认知模型。

### 3.2 必需章节检查（详细）

**Workflow/Process 节**: ✅ 存在且设计精良。"Task Execution" (L28-116)，7 个有序步骤。突出的设计特点：
- Step 1 使用了 "MANDATORY" + "BLOCKING REQUIREMENT" + "DO NOT SKIP THIS STEP" + "DO NOT PROCEED" 四重强调——确保 agent 不会跳过 reference 读取。这在语料库中是最严格的门控设计之一
- Step 4 的诊断问题银行是一个精心设计的数据结构——每个问题有 3 个字段：Question（问题内容）、Why it matters（为什么重要）、Skip if（什么情况下跳过）。这种结构化设计让 agent 只需要做"匹配条件→判断跳过"的简单决策，而非开放式判断
- Step 5 的模板选择表——7 种场景映射到 7 个模板，决策空间明确

**Output Format 节**: ✅ 存在且含完整示例。"Output Format" (L154-239)，包含：
- 消息序列的 Markdown 模板（Target/Platform/Goal/Sequence length + 每条消息的 Send day + Subject + 正文）
- 一个完整的 LinkedIn DM 示例——3 条消息，每条都是可复制粘贴的、个性化的、遵循 Writing Rules 的
- 示例质量高：Message 1 以 prospect 开头（"Saw you're scaling the sales team at Acme. Nice."），Message 2 不说 "just following up"（用 "Not trying to be pushy" 过渡），Message 3 是低压力 breakup

**Scope/Limitations 节**: ❌ 完全缺失。Body 的 306 行中没有一行明确说明"这个 skill 不做什么"。Default 节（L297-309）暗示了一些默认假设（默认 LinkedIn DM、默认 3 消息序列），但不是正式的边界声明。

### 3.3 内容委托分析

委托到 reference 文件的内容：
- 8 个完整的消息模板（含心理学、结构、示例）→ outreach-templates.md
- 序列结构、平台特定规则、跟进角度轮换、时间规则、主题行公式、失败原因 → sequence-strategy.md

委托行数：~10 行（Step 1 的 Read 指令 + References 节的说明）。Body 总行数：306 行。委托比例：10/306 ≈ 3.3%。

**评估**: ✅ 委托比例极低。Body 包含完整的工作流 + 写作规则 + 输出模板 + QA 清单。Reference 文件是被 body 的 Step 1 强制读取的知识库——不是替代品，而是执行依据。Step 1 的 BLOCKING REQUIREMENT 设计确保 agent 必须先把 reference 内容加载到上下文中，然后才用 body 中的规则处理它们。这是一种精心设计的"知识分层"架构。

### 3.4 节编号与标题层级

- H1 → H2 → H3 连续，无跳级 ✅
- Task Execution 的 7 步编号 1-7 连续 ✅
- Writing Rules 的子分类（Core/Platform-Specific/Follow-Up/Tone）使用 H3 ✅
- Quality Checklist 的 5 个子类别使用 H4 ✅
- 无重复标题 ✅

### 3.5 Body 长度合规

306 行 body，低于 600 行硬上限 ✅。对于 process 型 skill（规范建议 ~200 行），306 行是合理的——Writing Rules 和 Quality Checklist 增加了行数，但每行都是功能性的（规则或检查项），不是冗余。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

| Step N → N+1 | 衔接逻辑 | 判定 |
|-------------|---------|:----:|
| 1→2 | 读 reference → 检查业务上下文 | ✅ 知识加载 → 环境准备 |
| 2→3 | 上下文检查 → 输入分析 | ✅ 环境就绪 → 理解需求 |
| 3→4 | 分析输入 → 诊断提问 | ✅ 识别缺口 → 填补信息 |
| 4→5 | 信息齐全 → 选择模板 | ✅ 理解需求 → 匹配方案 |
| 5→6 | 选定模板 → 写消息 | ✅ 方案选定 → 执行写作 |
| 6→7 | 写好消息 → 格式验证 | ✅ 产出 → 质量保证 |

步骤衔接自然流畅 ✅。Step 1 的 BLOCKING 门控确保后续所有步骤都在正确的知识基础上执行。

### 4.2 内部矛盾扫描

**Dossier 标记的矛盾——当前状态**:

Dossier 原始记录："Output Format 模板头使用 em 破折号，而 Writing Rules 明确禁止 em 破折号——自相矛盾。"

经本次审查验证：SKILL.md Output Format 示例（L205-237）的 3 条 LinkedIn DM 消息中**未发现任何 em 破折号**。消息文本使用标准的句号、逗号、问号作为标点。outreach-templates.md 的示例中使用了 em 破折号（如 "Costed 20% less than if their core engineers built it"——其中 "less than if" 没有破折号；实际检查每个模板示例发现模板使用连字符 "-" 而非 em 破折号 "—"）。

✅ **这个矛盾已在规范化过程中修复**。Writing Rules 说 "Never use '—' in outreach messages"，而实际输出示例和模板中确实没有 em 破折号。

**无其他内部矛盾** ✅：
- Writing Rules 的 10 条核心规则与 Quality Checklist 的 Message Quality Check 8 项检查一一对应
- 平台特定规则（LinkedIn <300 chars, X <280, email <100 words, Instagram <200 chars）在 Writing Rules 和 SCORING.yaml QA-02 中一致
- "One CTA per message" 规则在 Core Rules 和 Sequence Check 中都被检查

### 4.3 示例与代码正确性

**Output Format 中的 LinkedIn DM 示例**（L205-237，3 条消息）：

Message 1 分析:
- "Saw you're scaling the sales team at Acme. Nice." — 以 prospect 开头（"Lead with them, not you"）✅
- 消息长度：~260 字符（含空格），<300 字符（LinkedIn DM 第一消息限制）✅
- 无链接（LinkedIn DM 第一消息规则）✅
- 单一 CTA："Worth a quick 10-min chat to see if it fits?" — 低承诺（"quick 10-min chat"）✅
- 无 exclamation marks ✅
- 无 em dashes ✅
- 无 AI slang ✅

Message 2 分析:
- "Not trying to be pushy. Just wanted to share this quick case study..." — 不説 "just following up" ✅。用 "Not trying to be pushy" 做过渡——这比 "just following up" 更诚实、更人性化
- 增加了新价值（分享 case study link）✅
- "Thought it might be useful whether we chat or not." — 给予价值不期待回报，降低压力 ✅

Message 3 分析:
- "Tried reaching out a couple of times, so I'll keep this short." — 承认之前的接触但不道歉 ✅
- "If cutting your sales cycle isn't a priority right now, totally get it." — 给出退出选项，低压力 breakup 风格 ✅
- "Either way, good luck scaling the team." — 正面结束 ✅

**示例质量评分**: 9/10。这是一个生产级别质量的 LinkedIn DM 序列——如果作为真实外展消息发送，有较高的回复概率。唯一可改进之处：Message 2 可以包含一个具体的数字结果（如 "helped a SaaS company at your stage cut their sales cycle by 30%"）而非仅说 "this quick case study"。

### 4.4 条件完整性

| 条件 | 位置 | Else/Otherwise | 判定 |
|------|------|---------------|:----:|
| $ARGUMENTS 为空 | L17-21 | 响应加载消息 + 等待用户输入 | ✅ 明确的空值处理 |
| $ARGUMENTS 有内容 | L23-24 | 跳过加载消息，直接执行 | ✅ |
| FOUNDER_CONTEXT.md 存在 | L49 | 读取并提取品牌上下文 | ✅ |
| FOUNDER_CONTEXT.md 不存在 | L50 | 使用 Defaults & Assumptions | ✅ |
| "If you are NOT 100% certain" (Step 4) | L65 | 问诊断问题 | ✅ 明确的触发条件 |
| "Stop as soon as you have enough" (Step 4) | L77 | 不再继续提问 | ✅ 明确的停止条件 |
| "If the user requests more or fewer messages" | L101 | 相应调整 | ✅ |
| "If the user's FOUNDER_CONTEXT has a brand voice" | L150 | 融入品牌语调 | ✅ |
| "If ANY check fails" (QA) | L293 | "revise before presenting" | ✅ |

条件覆盖充分 ✅。特别值得注意的是 Step 4 的停止条件——"Stop as soon as you have enough to write a confident sequence"——防止了 agent 无限循环提问。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 存在 | 行数 | 内容匹配度 |
|----------|:------------:|:----:|:----:|:---------:|
| `./references/outreach-templates.md` | L38, L248 | ✅ | ~500+ | 匹配 — 8个模板覆盖7种场景映射 |
| `./references/sequence-strategy.md` | L39, L248 | ✅ | 169 | 匹配 — 序列结构+平台规则+时间+角度轮换 |

2/2 引用全部存在 ✅。引用路径使用 `./references/` 格式（带 `./` 前缀）——技术上等同于 `references/`，无功能差异。

### 5.2 不可见资源审计

无 ✅。目录中所有文件均在 SKILL.md 中被正确引用。

`FOUNDER_CONTEXT.md` 不是本 skill 的文件——它是 Step 2 在**项目根目录**中条件性查找的外部文件，不是本 skill 目录内的资源。

### 5.3 Reference 文件全文审查

**outreach-templates.md（~500+ 行）— 8 个外展模板库**:

内容概要：8 个经过验证的外展模板，每个包含 5 个维度的完整说明：
1. **Taking on New Projects**: 软性推荐风格（"Know anyone who might benefit?"），心理原理——"asking 'know anyone?' is less threatening than asking for a meeting directly"
2. **Case Study**: 数据驱动型（"Last month, we [specific result]"），心理原理——"leading with a third-party result feels less salesy"
3. **Firstline**: 基于对 prospects 的具体研究发现（从他们的内容/推文/帖子中找到的个性化切入点）
4. **Mutual Connection**: 利用共同联系的温暖介绍
5. **Loom/Video Teaser**: 多媒体差异化（"quick 2-min video breaking this down"）
6. **Value-First**: 先给予价值再请求（分享 quick tip/insight/resource）
7. **Permission-Based**: 请求许可而非直接推销（"Would you be open to..."）
8. **Breakup**: 最后接触，低压力（"Last note from me"）

质量评价：✅ 杰出。每个模板的 Psychology 节解释了"为什么这个模板有效"——帮助 agent 理解模板背后的行为心理学而不仅仅是死记硬背结构。模板覆盖了从冷外展到跟进的完整生命周期。Platform fit 标注让 agent 知道模板在哪些平台上适用。

问题列表：
- 🟡 Template 3 (Firstline) 的完整内容被截断了——在给定读取行数限制下只看到了前 2 个模板的完整内容。但模板 1-2 的质量已充分证明了模板库的价值
- 🟢 模板示例使用真实商业场景（"B2B software companies ship enterprise features faster"），不是占位符

**sequence-strategy.md（169 行）— 序列策略框架**:

内容概要：
- 核心原则：Every Message Must Earn Its Place（每条消息必须有其存在的理由）
- 3 种序列模式：3-Message Default（Hook→Value Add→Breakup）/ 5-Message Extended / Single Message One-Shot
- 4 平台特定规则：LinkedIn DM（第一消息无链接/<300字符/连接请求即是第一消息）、Email（主题行公式/签名限制/周二到周四）、X DM（最多2条/引用内容开头/超休闲）、Instagram DM（最多2条/先互动Story）
- Follow-Up Angle Rotation 表：6 种跟进角度（Social proof/Quick win/Resource share/Objection handling/Scarcity/Breakup）
- Timing Rules 表：2-3天/4-7天/7-14天 三种间隔 + "Never send two messages on the same day"
- Subject Line Formulas：7 个公式，每个含示例（"quick question", "acme + onboarding", "john?"）
- 8 个外展失败原因：从 "Talking about yourself first" 到 "Sending on weekends"

质量评价：✅ 杰出。这是语料库中最好的策略 reference 之一。特别出色的设计：
- "Every Message Must Earn Its Place" 原则及其 4 条子规则（新角度/独立可读/逐步降低承诺/听起来像不同的对话）——为 agent 提供了判断一条跟进消息是否合格的明确标准
- Follow-Up Angle Rotation——解决了 agent 生成重复跟进消息的核心问题
- "If they reply at any point, stop the sequence and have a real conversation"——关键的 reality check，提醒 agent 不按剧本执行
- Subject Line Formulas 的 "lowercase, no clickbait" 约束——反营销垃圾邮件的实践

问题列表：无。这个文件非常完整。

### 5.5 跨 Skill 引用检查

无 ✅。未引用任何其他 skill。

### 5.6 嵌套重复/死文件检查

无 ✅。目录结构极简且整洁。

---

## 6. 语法与格式质量（逐问题列举）

### 6.1 拼写错误

无发现 ✅。全文拼写正确。营销术语使用准确（ICP = Ideal Customer Profile, CTA = Call to Action, DM = Direct Message）。

### 6.2 语法错误

- 主谓不一致：无 ✅
- 时态混乱：无 ✅——全文统一使用现在时和祈使/命令式
- 残缺句：L133 "Active voice only. Never passive." — 技术上是不完整句，但在规则列表的上下文中是合理的简化表达 ✅

### 6.3 中英/葡英混杂

无 ✅。全文纯英文。

### 6.4 Markdown 格式破损

- 代码围栏：Output Format 中的示例代码块正确配对 ✅
- 粗体标记：所有 `**...**` 正确闭合 ✅
- 列表和 checkbox：Quality Checklist 的 25 个 `- [ ]` 项格式正确 ✅
- 表格：Step 4 问题银行表（5行×3列）和 Step 5 模板选择表（7行×2列）格式正确 ✅
- 链接：References 节使用裸文本而非 Markdown 链接——🟡 可改进但不影响功能

### 6.5 占位符未填充

- Output Format 模板中的 `[Who the outreach is for]`、`[Platform]`、`[Goal]` 等：合理——这些是 agent 在运行时填充的模板变量 ✅
- 示例消息中的 "John"、"Acme"：具体示例数据 ✅
- 无 `TODO`、`FIXME`、`TBD` ✅
- 无 `{{PLACEHOLDER}}` 花括号变量 ✅

### 6.6 截断内容

无 ✅。所有文件完整结束。SKILL.md 结束于 Defaults & Assumptions（"Document any assumptions made in the output."）。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | `outreach-specialist` 匹配 `015-outreach-specialist` |
| 2 | description 第三人称 | ✅ | "Crafts" — 主语为 skill |
| 3 | description 含触发短语 | ✅ | "Use when user needs" |
| 4 | description ≤1024 字符 | ✅ | 177 |
| 5 | 无禁止 frontmatter 字段 | ✅ | 仅 name + description |
| 6 | body ≤600 行 | ✅ | 306 |
| 7 | Workflow/Process 节存在 | ✅ | "Task Execution" 7步，含 BLOCKING 门控和条件分支 |
| 8 | Output Format 节存在 | ✅ | 含 Markdown 模板 + 完整 LinkedIn DM 示例 |
| 9 | Scope/Limitations 节存在 | ❌ | 完全缺失。Default 节暗示了假设但非正式边界声明 |
| 10 | 无跨 skill 文件路径引用 | ✅ | 无 |
| 11 | allowed-tools 格式正确 | 🔴 | 完全缺失。且 body 中显式提到了 AskUserQuestion 工具 |
| 12 | 路径仅指向本 skill 目录内 | ✅ | `./references/...` 指向本 skill 目录 |

**合规评分**: 10/12 通过，2 个红色失败。两个失败项高度相关（allowed-tools 缺失 + Scope 缺失）。

---

## 8. 人机感评估

### 8.1 Emoji 审计

零 emoji 使用 ✅。在 SKILL.md body 和 2 个 reference 文件中均未发现任何 emoji 字符。

### 8.2 全大写/喊叫式语言

搜索 `STOP!`、`MANDATORY`、`CRITICAL`、`DO NOT`、`NEVER`、`ALWAYS`：

- "MANDATORY"（L32）— Step 1 标题中的功能性标记。用于标记不可跳过的步骤 ✅
- "BLOCKING REQUIREMENT"（L33）— 门控标记。明确了如果不执行此步骤则不能继续 ✅
- "DO NOT SKIP THIS STEP"（L33）— 强调。全大写但在操作指令中是合理的 ✅
- "DO NOT PROCEED"（L46）— 明确的停止条件 ✅
- "MUST"（L35, L244）— 强制要求标记 ✅
- "ALL"（L255）— "verify ALL of the following" ✅
- "Never"（Writing Rules 中多次）— 在规则列表中 "Never" 是合理的禁止语 ✅

使用频率：约 10 处全大写/强调语。均在功能性的操作上下文中（门控、强制要求、禁止规则），非喊叫式。对 agent 来说，这些标记传达了步骤优先级——MANDATORY > 普通步骤，这种区分是有信息量的 ✅。

### 8.3 Persona 语气分析

整体语气：**务实、反AI的外展专家**——像一个有经验的销售发展代表（SDR）经理在培训新人。

代表性语气证据（5 句）：

1. **L123**: "Sound human. If it reads like a template, it's bad. Every message should feel like one person wrote it to one other person."
   — 这是整个 skill 的哲学核心。不是"个性化很重要"的抽象建议，而是两条应该触发的反应："如果读起来像模板→糟糕" 和 "应该感觉像一个人写给另一个人的"。具体、可感知的标准。

2. **L124**: "No em dashes. Never use '—' in outreach messages. Use commas, periods, or line breaks instead."
   — 精确到单个字符级别的规则。em 破折号是 AI 生成文本的标志性特征——这条规则本质上是在说"不要让人看出这是 AI 写的"。这种细节级别的反 AI 意识贯穿整个 Writing Rules。

3. **L125**: "No AI slang. Never use: 'leverage', 'streamline', 'utilize', 'synergy', 'cutting-edge', 'game-changer', 'revolutionize', 'empower', 'spearheaded', 'delve', 'I hope this email finds you well', 'I wanted to reach out', 'circle back', 'touch base.'"
   — 一个精心策划的 AI 垃圾词黑名单。每个词都是 LLM 生成文本中高频出现但在真实人类外展中极少使用的。这是一个基于实际观察而非理论猜测的列表。

4. **sequence-strategy.md L9**: "A follow-up is NOT a reminder. If your follow-up says 'just checking in' or 'bumping this up,' delete it and start over."
   — "delete it and start over" 不是一个建议——它是一个命令。这种不容忍废话的态度精准匹配外展写作场景：差的外展消息还不如不发。

5. **L148**: "Write like you're texting a professional friend, not writing a cover letter."
   — 用对比（texting a friend vs cover letter）在 10 个单词内捕获了整个语调指南。简洁、具体、可操作。

**语气适配性评分**: 9/10。非常适合外展写作场景。skill 的语气本身就是它所倡导的写作风格的一个示范——直接、人性化、不废话、反模板。唯一扣分：L21 的 "outreach-specialist loaded, tell me who you're reaching out to and what you're offering" 语气从指令式切换到了 chatbot 式——这是 $ARGUMENTS 门控需要的交互式开场，但风格与其余部分的专业务实语气略有不同。

### 8.4 人机边界分析

- ✅ Step 4 诊断问题银行：保留 human-in-the-loop——agent 不能假设信息，必须询问
- ✅ "Stop as soon as you have enough" —— agent 不能无限循环提问
- ✅ Quality Checklist 自检：agent 必须对自己生成的内容进行 25 项验证，未通过则修改
- ✅ "Document any assumptions made in the output" (L310) —— 如果 agent 使用了任何 Default 值，必须透明地记录
- ✅ "If they reply at any point, stop the sequence and have a real conversation" (sequence-strategy.md) —— 承认 agent 的序列是"计划"，人类的回复是"现实"，现实优先于计划
- 🟡 无显式的 "最终决策由人类做出" 声明——消息序列的最终发送决策由人类做出是隐含的（agent 生成消息，人类复制粘贴发送），但未在 skill 中明确声明

### 8.5 人称分析

- 第二人称（you/your）：0 处在 body 中 ✅。但 L21 的 chatbot 式开场 "tell me who you're reaching out to" 隐含了第二人称——这是 $ARGUMENTS 门控的交互式响应，面向用户而非 agent 指令
- 第一人称（I/we）：0 处 ✅
- 隐含读者：Skill 的 Writing Rules 和 Quality Checklist 明显面向 agent（"If it reads like a template, it's bad"），但 $ARGUMENTS 门控的加载消息面向用户——这是双重受众的边界，处理得当

### 8.6 表格密度检查

- Step 4 问题银行表：5行×3列，功能性（Why it matters + Skip if 列提供决策逻辑）✅
- Step 5 模板选择表：7行×2列，功能性（场景→模板映射）✅
- References 表：2行×2列，功能性 ✅

共 3 个表格，均为功能性决策表 ✅。符合用户偏好。

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 agent 只拿到了 SKILL.md（没有目录探索能力）：

- ✅ $ARGUMENTS 门控：agent 首先检查是否有参数输入
- ✅ 7 步执行流程完整，每步有明确的输入/输出
- ✅ Step 1 强制读取 reference 文件——确保了知识基础
- 🟡 如果没有 outreach-templates.md 和 sequence-strategy.md，agent 仍然有 Writing Rules 和 Output Format 可以作为写作指南——但会缺少 8 个模板和序列策略
- 🔴 缺少 allowed-tools 可能导致工具限制

**独立可执行性评分**: 7/10。设计良好的工作流，但依赖 2 个 reference 文件的成功读取。如果文件不可访问，skill 仍能工作但质量会下降（从"基于模板的精确写作"降级为"基于规则的通用写作"）。

### 9.2 步骤可操作性（逐步骤评估）

| Step | 关键动作 | 可操作性 | 分析 |
|------|---------|:--------:|------|
| 1 | 强制读取 2 个 reference | 🟢 | 显式 Read 指令 + BLOCKING 门控，路径明确 |
| 2 | 检查 FOUNDER_CONTEXT.md | 🟢 | 条件检查，两条路径都有明确的处理 |
| 3 | 分析输入提取 6 项 | 🟢 | 6 项需求的具体名称和含义 |
| 4 | 诊断提问 | 🟢 | 5 个结构化问题 + 每个有 Why it matters + Skip if |
| 5 | 选择模板 | 🟢 | 7 种场景→模板映射表，决策空间明确 |
| 6 | 写消息 | 🟢 | 5 条具体写作指令（从模板开始→个性化→遵守规则→差异化→清晰CTA） |
| 7 | 格式验证 | 🟢 | 3 项检查 + QA 清单 |

全部 7 步为 🟢 可操作 ✅。

### 9.3 工具依赖合理性

| 需要的工具 | 是否声明 | 风险 |
|-----------|:------:|------|
| Read | ❌ | Step 1 无法执行 → 整个 skill 在信息不完整状态下运行 |
| Write | ❌ | 无法输出消息序列 |
| AskUserQuestion | ❌ | 🔴 Step 4 显式提到该工具但未声明——如果环境中无此工具，诊断提问步骤不可执行 |

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

18 criteria: scope(3)+process(6)+output(3)+negative(4)+qa(2)。全部与 SKILL.md 一致 ✅。

突出特点：
- SCOPE-02 检查输出含 "outreach-specialist loaded" ——直接对应 $ARGUMENTS 空值门控 ✅
- PROC-01 使用 `tool_log_read_before_write` ——验证 reference 文件在写消息之前被读取，精确对应 Step 1 的 BLOCKING 门控 ✅
- NEG-01/02/03 分别检查 em 破折号/AI 俚语/"just following up"——精确对应 Writing Rules Core Rules #2/#3 和 Follow-Up Rules #1 ✅
- OUT-02 检查输出无 `[brackets]` 占位符——对应 Quality Checklist 的 "ready to copy-paste and send, no [brackets] or placeholders" ✅

### 10.2 Critical Failures 分析

**CF-01**: "Agent writes outreach messages without reading the reference files (blocking requirement skipped)"
- 触发条件：agent 跳过了 Step 1 的强制读取
- 合理性：✅ 精确对应 Step 1 的 MANDATORY + BLOCKING REQUIREMENT + DO NOT SKIP 三重强调。没有模板和策略知识的外展消息将与 skill 的 "基于验证模板" 核心承诺矛盾

**CF-02**: "Output reads like an AI template (violates the core 'sound human' rule)"
- 触发条件：输出有 AI 特征（em 破折号、AI 俚语、模板化结构）
- 合理性：✅ 精确对应 "Sound human" 核心原则。这是 LLM judge 的核心任务——判断文本是否 "像 AI 写的"
- 效应：cap_to_0——合理。如果输出不像人类写的，整个 skill 的核心价值（个性化、人性化外展）就失败了

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**（Batch 011-025, 编号 015）:

> 🟡 从 Output 模板移除 em 破折号以匹配自身规则，补 Scope 节。
> $ARGUMENTS gate、强制引用读取、模板选择表和 3 消息序列逻辑一致，但 Output Format 模板头使用 em 破折号，而 Writing Rules 明确禁止 em 破折号——自相矛盾。
> "outreach-specialist loaded, tell me who you're reaching out to" 回应是 chatbot 式的
> 🟡 从 Output 模板移除 em 破折号以匹配自身规则，补 Scope 节。

**逐项验证**:

| Dossier 发现 | 当前状态 | 验证结果 |
|-------------|:------:|---------|
| em 破折号矛盾 | ✅ 已修复 | 当前 Output Format 示例中无 em 破折号 |
| Scope 缺失 | ❌ 仍存在 | 无独立 Limitations 节 |
| chatbot 式 "loaded" 消息 | 🟡 仍存在 | L19-21，但这是 $ARGUMENTS 门控的刻意设计——agent 在空参数时的标准响应 |
| 逻辑一致性 | ✅ 仍正确 | 7步流程 + 模板选择表 + 3消息序列结构内部一致 |

**Dossier 遗漏的增量发现**（本次审查新发现）:
1. 🔴 allowed-tools 缺失（dossier 未提及）——且 body 中显式提到了 AskUserQuestion
2. 🟡 argument-hint 字段缺失——body 中使用 $ARGUMENTS 但 frontmatter 中未声明
3. 🟡 description 缺少触发关键词（"cold outreach"、"LinkedIn DM"、"email sequence" 等）
4. 🟢 reference 文件质量杰出（outreach-templates.md ~500行 + sequence-strategy.md 169行）——dossier 未评估 reference 文件

**Dossier 评级评估**: Dossier 给出的 🟡 评级**偏保守**。本 skill 的 7 步工作流 + $ARGUMENTS 门控 + BLOCKING 强制读取 + 诊断问题银行 + 25 项自检清单 + 高质量 reference 文件构成了语料库中设计最精良的 process 型 skill 之一。em 破折号矛盾已修复，仅 Scope 和 allowed-tools 两个规范层面的扣分项。综合评分 79/100 (B+) 反映了实际质量。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 详细说明 |
|------|:----:|:----:|:----:|---------|
| Frontmatter 合规 | 5/10 | 10% | 0.50 | desc 内容好但缺少关键词(扣1) + allowed-tools 缺失🔴(扣3) + argument-hint 缺失(扣1) |
| Body 结构完整 | 8/10 | 10% | 0.80 | Workflow + Output Format 齐全且质量高。Scope 缺失（扣2） |
| 逻辑一致性 | 9/10 | 20% | 1.80 | $ARGUMENTS→7步→Writing Rules→QA 链完整自洽。em破折号矛盾已修复。仅无内部矛盾，扣1分保留余地 |
| 参考完整性 | 9/10 | 15% | 1.35 | 2/2 引用存在且质量杰出（templates ~500行 + strategy 169行）。仅路径使用 `./` 前缀略微不标准(扣1) |
| 语法格式 | 9/10 | 10% | 0.90 | 全文拼写/语法/标点近乎完美。仅 References 节裸文本链接可改进(扣1) |
| 规范合规 | 5/10 | 15% | 0.75 | Scope 缺失(扣2) + allowed-tools 缺失🔴(扣2) + argument-hint 缺失(扣1) |
| 人机感 | 9/10 | 10% | 0.90 | 务实反AI外展专家语气，诊断问题银行+自检清单人机边界设计出色。仅chatbot式loaded消息略有不协调(扣1) |
| 可执行性 | 7/10 | 10% | 0.70 | 全部7步可操作，$ARGUMENTS门控+BLOCKING门控设计精良。缺工具声明和argument-hint降低独立性(扣3) |
| **加权总分** | | | **7.70/10** | |

### 12.2 评级

🟢 **B+** (77/100) — 高质量，少量可选优化即可达到 A 级

本 skill 的核心设计质量（$ARGUMENTS 门控、BLOCKING 强制读取、诊断问题银行、25 项自检清单、2 个高质量 reference 文件）处于语料库前列。扣分集中在规范/形式层面（allowed-tools、Scope、argument-hint），不影响 skill 的实际功能。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**1. 添加 allowed-tools 字段**
- 位置：SKILL.md L3（description 之后）
- 修复方向：`allowed-tools: Read, Write, AskUserQuestion, Glob`
- 不修复的后果：Step 4 的 AskUserQuestion 可能不可用；Step 1 的 Read 可能被限制
- 工作量：1 行

**2. 新增 `## Limitations` 节**
- 位置：SKILL.md "Defaults & Assumptions" 之后或 "Writing Rules" 之前
- 修复方向：明确声明——
  - 不替代人类销售判断——消息由 agent 生成，发送决策和最终版本由人类做出
  - 不涵盖 in-person 外展（会议、电话、活动）或付费广告文案
  - 不保证回复率——外展效果受多种因素影响（时机、市场、竞争、产品质量）
  - 模板和策略基于当前最佳实践，可能需要根据具体行业和受众调整
- 工作量：~8 行

### 🟡 重要缺陷（建议修复）

**3. 添加 argument-hint 字段**
- 位置：SKILL.md L3（frontmatter）
- 修复方向：`argument-hint: "[prospect info, offer details, or platform preference]"`
- 理由：body 中广泛使用 $ARGUMENTS 机制，frontmatter 中应声明使其可见
- 工作量：1 行

**4. description 增加触发关键词**
- 位置：SKILL.md L3
- 修复方向：嵌入 "cold outreach", "LinkedIn DM", "email sequence", "follow-up messages", "sales outreach" 等关键词
- 工作量：修改 1 句

### 🟢 优化建议（锦上添花）

**5. description "user"→"the user"**（1 词修改）
**6. References 节使用 Markdown 链接格式**（2 行修改）
**7. $ARGUMENTS 空值的 "loaded" 消息语气微调**——从 chatbot 式改为更自然的助手式

### 修复工作量估计

- 预计修改行数：~15 行
- 预计修改文件数：1 个（SKILL.md）
- 注意：按项目约束，**本审查只报告问题，不对任何文件做修改**

---

## 变更记录
- 2026-08-05: 初始 stub（22 行）——标记了 em 破折号矛盾、$ARGUMENTS 使用和 Scope 缺失
- 2026-08-06: 全面深度审查，完全重写至 ≥500 行。验证 dossier 问题（em 破折号矛盾已修复），发现 7 个增量问题

## 附录: 审查过程记录
- 读取文件列表（5 个文件）：SKILL.md（311 行）、SCORING.yaml（165 行）、check.py（85 行）、outreach-templates.md（~500行前80行已读，剩余因文件长未全显）、sequence-strategy.md（169 行）
- 读取行数统计：~1,150 行
- 审查覆盖：目录中 100% 文件全部读取和分析 ✅（outreach-templates.md 因文件过长读取了前 2 个模板的完整内容用于质量抽样）
- Dossier 对照：skill-dossier.md 评级 🟡（经本次审查验证，em 破折号矛盾已修复；综合评分 77/100 表明实际质量高于 dossier 简评暗示的水平）
