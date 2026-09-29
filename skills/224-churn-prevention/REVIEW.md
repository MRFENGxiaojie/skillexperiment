# REVIEW: 224-churn-prevention

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: tool — SaaS 客户流失预防（取消流程设计 + 留存挽留 + dunning 欠费追回）
**Body 行数**: 232 行
**参考文件数**: references/0, scripts/0, assets/0, 其他/0
**总文件数**: 3

---

## 1. 目录全量清单

```
224-churn-prevention/
├── SKILL.md (232 行)
├── SCORING.yaml (183 行)
└── check.py (73 行)
```

该 skill 是**纯三文件结构**（SKILL.md + SCORING.yaml + check.py），无 `references/`、`scripts/`、`assets/` 任何子目录。这与 SKILL.md body 中引用的两个资产文件形成强烈反差——详见 §5。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 值: `churn-prevention`，全小写+连字符 ✓
- 长度: 16 字符，远低于 64 字符限制 ✓
- 匹配目录名 `224-churn-prevention`（去数字前缀后一致）✓

### 2.2 description

原文:

> "Reduce voluntary and involuntary customer churn through cancel flow design, retention offers, exit surveys, and dunning sequences. Use when the user wants to analyze churn patterns, design retention strategies, optimize cancellation experiences, or reduce involuntary churn from payment failures."

逐句分析:

**第 1 句** (WHAT): "Reduce voluntary and involuntary customer churn through cancel flow design, retention offers, exit surveys, and dunning sequences."
- 内容上准确概括了 skill 的全部四块能力：取消流程、挽留 offer、退出调研、dunning 序列 ✓
- **但以祈使动词 "Reduce" 开头，缺少主语**——严格按 SKILL-SPEC §2.3，description 必须是第三人称、不得用祈使句开头。对照 §2.6 的 bad example（"Use this skill whenever..."），本句属于同类问题（程度较轻：没有 "use this skill" 字样，但动词原形开头的祈使结构是确定的）
- 参考 322 号审查的先例，祈使式 WHAT 开头曾被标记为"可接受但需注意"。此处给出明确判定：⚠️ 轻微违规，建议改为第三人称（见修复 I-4）

**第 2 句** (WHEN): "Use when the user wants to analyze churn patterns, design retention strategies, optimize cancellation experiences, or reduce involuntary churn from payment failures."
- 含标准触发短语 `"Use when the user..."` ✓（SKILL-SPEC §2.4 要求至少一个触发信号）
- 触发场景具体：分析流失模式、设计挽留策略、优化取消体验、减少支付失败流失 ✓
- 第三人称 ✓

**KEYWORDS 覆盖**: churn、retention、cancel/cancellation、exit survey、dunning、payment failure——全部为领域关键术语，可被意图匹配命中 ✓

**长度**: 约 340 字符，≤1024 ✓

**跨 skill 路由**: description 中无 "NOT for X, use Y instead" 式路由 ✓（该内容放在 body 的 Related Skills 节，合规）

### 2.3 其他 frontmatter 字段

- 仅有 `name` + `description` 两个字段，无 `allowed-tools`、无 `argument-hint` ⚠️
- 本 skill 执行过程实际需要的工具：Read（读 marketing-context.md）、Bash（运行 churn_impact_calculator.py——虽然脚本缺失）、Glob/Read（查找用户环境中的取消流程、支付处理器配置）。虽然 `allowed-tools` 在 SKILL-SPEC §1.2 中是可选字段，但缺失意味着评测时无法约束工具使用。轻微问题（修复 O-4）
- 无任何禁止字段（§1.3 列表全部未出现）✓

### 2.4 Frontmatter 语法

- YAML 分隔符 `---` 配对正确（L1、L4）✓
- description 为单行双引号字符串，无转义问题 ✓
- 无缩进错误 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Churn Prevention (L6)                                — 标题
persona 引言 (L8-10)                                    — 角色声明 + 商业价值论证，~3 行
## Before You Start (L12-34)                            — 上下文收集清单，~23 行
## How This Skill Works (L36-46)                        — 三种模式（build/optimize/dunning），~11 行
## Cancel Flow Design (L49-83)                          — 5 阶段取消流程，~35 行
## Exit Survey Design (L86-102)                         — 退出调研设计 + 原因分类表，~17 行
## Retention Offer Playbook (L106-124)                  — 挽留 offer 打法表 + 展示规则，~19 行
## Involuntary Churn: Dunning Setup (L127-160)          — 重试逻辑 + 卡片更新 + 邮件序列，~34 行
## Metrics and Benchmarks (L164-186)                    — 指标表 + 红旗信号 + 计算器调用，~23 行
## Proactive Triggers (L190-200)                        — 6 个主动触发信号，~11 行
## Output Artifacts (L203-212)                          — 输入→输出映射表，~10 行
## Communication (L216-222)                             — 输出沟通模式，~7 行
## Related Skills (L226-231)                            — 5 个关联 skill 路由，~6 行
```

### 3.2 必需章节检查（对照 SKILL-SPEC §3.1）

| 必需章节 | 状态 | 说明 |
|----------|:----:|------|
| Workflow / Process | ⚠️ | 无显式 `## Workflow` 标题。流程内容分散在 Cancel Flow Design（5 阶段）、Dunning Setup（重试/邮件）等节中，**但缺少三模式选择逻辑**——Mode 1/2/3 只描述了各自场景，没有"用户输入 → 模式选择"的判定规则 |
| Output Format | ✓ | `## Output Artifacts`（L203-212）以"请求 → 交付物"映射表的形式覆盖了全部三种模式 + 附加交付物 |
| Scope / Limitations | ❌ | **完全缺失**。没有任何"本 skill 不做什么/何时不适用"的说明（详见 §3.2.1） |

#### 3.2.1 Scope/Limitations 缺失详情

搜索全文，找不到任何接近 scope 的内容。以下限制性信息散落但均非 Scope 语义：

- L51 "A cancel flow is not a dark pattern — it's a structured conversation" → 这是设计原则，不是范围边界
- L194 "Churn prevention alone won't fix it — flag for product/ICP review" → 这是触发信号，不是范围说明

缺失的范围边界应至少包括：

1. **不做支付处理集成**——不配置 Stripe/Braintree 账户、不写代码，只给出设计
2. **不做价格战略本身**——定价重构属于 pricing-strategy skill 的范畴（Related Skills 有提到但未在 Scope 中正式声明）
3. **不实际发送邮件**——只产出邮件文案与序列，不调用发送工具
4. **不保证挽回率数字**——benchmark 是行业参考值，需结合用户自身数据校准
5. **数据门槛**——没有历史流失数据的公司只能得到定性建议而非量化模型输出

缺少 Scope 节是本次审查发现的第二大结构性问题（仅次于引用失效）。

### 3.3 内容委托分析

Body 只有两处内容委托：

| 委托 | 位置 | 目标文件 | 状态 |
|------|------|----------|:----:|
| "See references/dunning-guide.md for complete email sequences and retry setup examples" | L160 | references/dunning-guide.md | 🔴 不存在 |
| "python3 scripts/churn_impact_calculator.py" | L185、L211 | scripts/churn_impact_calculator.py | 🔴 不存在 |

委托比例：2 行委托 / 232 行 body ≈ 0.9%。委托内容本身是**合理的**（完整邮件文案 40+ 行、计算器脚本 60+ 行确实应该外置），但两个目标文件均未创建——委托指向虚空。

### 3.4 节编号/标题层级

- 标题层级：`#` → `##`，无 `###` 以下的层级（整份 body 没有二级以上小节标题），结构扁平但清晰 ✓
- 无跳级 ✓
- 全文 13 个 `##` 节 + 1 个 `#` 标题，信息密度高、导航性好 ✓

### 3.5 Body 长度合规

- 实际 232 行。pattern=tool（SCORING.yaml L2），tool pattern 目标约 300 行，硬限制 600 行
- 232 行**低于** tool pattern 目标——考虑到两个委托文件缺失，如果 dunning-guide（~40 行）和计算器说明（~20 行）并入 body，约 290 行，正好贴合 tool pattern 目标。当前偏短实质是"资产缺失导致的短"，而非精炼
- 判定：长度合规，但短得有些空心——精华内容（完整邮件文案）被委托给了不存在的文件

---

## 4. 逻辑一致性深度审查

### 4.1 三模式与内容结构的一致性

Mode 1（Build Cancel Flow）↔ Cancel Flow Design 节 ✓
Mode 2（Optimize Existing Flow）↔ 无对应专节 ⚠️——优化模式只提了一句"audit what exists, identify gaps, and rebuild what's underperforming"，但没有对应的审计清单、差距评估维度、或评分卡结构。Output Artifacts 中的 "Audit my cancel flow → Scorecard (0-100)" 是唯一支撑，但 body 中没有定义评分卡的维度。QA-02 的测评点要求 agent 产出 "scorecard (0-100) with gaps, save rate benchmarks, and prioritized fixes"——**测评点存在而 skill 内容无支撑**，这是 SKILL.md 与 SCORING.yaml 之间的一处脱节
Mode 3（Set Up Dunning）↔ Dunning Setup 节 ✓

### 4.2 重试时间表与邮件序列不同步（重要矛盾）

**重试逻辑**（L134-138）：
- Retry 1: 失败后第 3 天
- Retry 2: retry 1 后 5 天 → 第 8 天
- Retry 3: retry 2 后 7 天 → 第 15 天
- Final: retry 3 后 3 天 → 第 18 天，然后取消

**邮件序列**（L147-153）：Day 0 / Day 3 / Day 7 / Day 12 / **Day 15（"Account paused/canceled"，CTA: Reactivate）**

矛盾点：

1. **Day 15 冲突**：邮件序列在第 15 天就发出 "Account paused/canceled"（账户已暂停/已取消），但重试逻辑的 Final retry 在第 18 天才执行、之后才取消。账户在第 15 天就已"paused/canceled"，第 18 天的最后一次扣款重试在逻辑上不成立——账户都取消了还重试什么？
2. **无交叉指引**：skill 从未说明"重试与邮件如何交错"。Day 0 邮件对应失败当天，Day 3 邮件与 Retry 1 同一天（第 3 天），Day 7 邮件介于 Retry 1 和 Retry 2 之间，Day 12 邮件在 Retry 2（第 8 天）之后。读者只能推测"先重试、后发邮件"的隐含时序，但 skill 没有明说

修复方向见 F-4。这是本 skill 逻辑层面最实质的问题。

### 4.3 "一因一 offer"规则与映射表的轻微矛盾

L102 的 Implementation rule 规定："Each reason must map to exactly one retention offer type. Ambiguous mapping = generic offer = low save rate."

但 L93 的映射表第一行：

| 原因 | 挽留 Offer |
|------|-----------|
| Too expensive / pricing | **Discount or downgrade** |

"Too expensive" 映射了**两个** offer 类型（Discount 和 Downgrade），与"exactly one"规则直接冲突。虽然 L112-114 的 Offer Playbook 对两者做了"使用时机"区分（Discount→price objection，Downgrade→too expensive/light usage），区分度仍然存在——但表内同时给出两个选项，agent 需要额外推理才能选出唯一 offer。轻微矛盾 ⚠️

### 4.4 商业数据无出处

- L10: "A 20% save rate on voluntary cancellations and a 30% recovery rate on involuntary churn can recover 5-8% of monthly lost MRR. That compounds." ——"5-8%"的来源未说明，且数学上存疑（20% × 自愿流失部分 + 30% × 非自愿流失部分如何加权到 5-8% 的月 MRR 恢复？依赖流失结构假设）
- L129: "Failed payments cause 20-40% of total churn in most SaaS companies." ——行业常识区间，无引用
- L170-175 的 benchmark 表（save rate 10-15% good、recovery 25-35% good 等）与 SCORING.yaml FMT-04 完全一致 ✓，但同样无出处

Skill 要求**输出**必须带置信度标记（🟢 verified benchmark / 🟡 estimated / 🔴 assumed，L222），但 skill 自身的 benchmark 未标注来源与置信度——"要求别人标注，自己不标注"的不对称。

### 4.5 阶段间衔接检查

- 5 阶段流程内部：Stage 2 明确要求"exit reason collected before showing the offer"（L67），与 Stage 3 "Match the offer to the reason"（L70）衔接正确 ✓
- Stage 5 的 7 天 re-engagement / 30 天 win-back 与 QA-03 测评点一致 ✓
- Proactive Triggers 的 6 个信号与 skill 各节内容一一对应（即时取消流程↔Stage 1、单一 offer↔映射规则、无 dunning↔Dunning Setup、可选调研↔Stage 2、无复活邮件↔Stage 5、流失率>5%↔Metrics）✓
- Output Artifacts 表中 "Model churn impact → Run churn_impact_calculator.py with your inputs" ——调用不存在的脚本，见 §5

### 4.6 Related Skills 表述问题

L229: "**email-sequence**: Use for lifecycle nurture and onboarding emails. NOT for dunning (use this skill for dunning)."

括号内 "use this skill for dunning" 中的 "this skill" 指代自身（churn-prevention）——措辞容易让 agent 混淆"this skill"是 email-sequence 还是当前 skill。建议改为 "NOT for dunning (use churn-prevention for dunning)"。轻微 ⚠️

### 4.7 条件完整性

- 本文档几乎没有条件分支结构——SKILL-SPEC §3.4 要求"Decision trees over prose: When there are branches, use a table or decision tree"。本 skill 最大的分支点（Mode 1/2/3 选择）恰恰没有决策表。三模式只有散文描述（L38-46），无 "用户说 X → 选 Mode Y" 的判定表。这是 §3.4 合规的最弱项
- 有分支处反而用了表格：原因→offer 映射表 ✓、Offer 使用时机表 ✓、指标表 ✓——"表该用而未用、表可用而处少用"的不平衡

---

## 5. 参考文件内容级审查（引用完整性矩阵）

### 5.1 引用清单与状态

| 引用 | SKILL.md 行号 | 目标路径 | 是否存在 | 后果 |
|------|:------------:|----------|:--------:|------|
| `references/dunning-guide.md` | L160 | references/ | 🔴 不存在（无 references/ 目录） | Agent 按指引去读完整邮件序列和重试示例时会失败 |
| `scripts/churn_impact_calculator.py` | L185 | scripts/ | 🔴 不存在（无 scripts/ 目录） | `python3 scripts/churn_impact_calculator.py` 会直接报文件不存在 |
| `scripts/churn_impact_calculator.py`（二次引用） | L211 | scripts/ | 🔴 同上 | Output Artifacts 中 "Model churn impact" 交付物无法实现 |

**目录实际内容确认**：仅有 `SKILL.md`、`SCORING.yaml`、`check.py` 三个文件。无 `references/`、无 `scripts/` 子目录。两处引用 100% 失效。

### 5.2 失效引用的影响分析

**dunning-guide.md（L160）**：这是最可惜的缺失。Dunning 邮件序列表（L147-153）只给了 5 行摘要（Day/Email/Tone/CTA），完整邮件正文（每个 subject line + body copy + 重试设置示例）被委托给该文件。Agent 按 L160 去读时：
- 若遵循指引 → Read 失败，流程中断
- 若忽略指引 → 只能凭摘要列产出邮件，缺失 40+ 行精华内容

**churn_impact_calculator.py（L185、L211）**：Metrics 节的"Use the churn impact calculator to model what improving each metric is worth" + Output Artifacts 的 "Model churn impact" 交付物都依赖此脚本。Agent 若真执行 `python3 scripts/churn_impact_calculator.py` 会得到 "No such file or directory"。这直接破坏了一个完整交付物（MRR 影响模型）。

### 5.3 marketing-context.md 引用（合规，非缺陷）

L15: "If `marketing-context.md` exists, read it before asking questions."

- 这是**输入文件**而非 skill 资产——由评测环境按需提供（对应 SCOPE-02 测评点）
- "If ... exists" 的条件式表述正确，不构成死引用 ✓
- 与 check.py 的 `tool_log_contains("marketing-context")` 检查配套，设计自洽 ✓

### 5.4 跨 Skill 引用检查

- Related Skills 节（L226-231）引用 customer-success-manager、email-sequence、pricing-strategy、campaign-analytics、signup-flow-cro——全部为散文式名称引用（"see also: <skill-name>"），无 `../` 文件路径 ✓ 符合 SKILL-SPEC §3.3
- 每条都带 "NOT for X（用本 skill）" 的边界说明，是 §2.5 要求的正确位置（body 而非 description）✓
- 无 `../` 跨 skill 路径引用 ✓

### 5.5 嵌套重复/死文件检查

- 无 self-nested 目录 ✓
- 无 `.gitkeep` ✓
- 无冗余文件 ✓
- **反向问题**：不是有死文件，而是"引用了不存在的文件"——见 5.1

---

## 6. 语法与格式质量

### 6.1 拼写错误

无。领域术语（dunning、churn、retention、win-back、Account Updater、Braintree）拼写全部正确 ✓

### 6.2 语法与句式

- 全文英文流畅，短句为主、信息密度高。代表性佳句：
  - "Churn is a revenue leak you can plug."（L10）——主题句有力
  - "No blame. No shame. Card failures happen — treat customers like adults."（L157）——排比 + 人文态度
  - "A cancel flow is not a dark pattern — it's a structured conversation."（L51）——立论清晰
- L229 的 Related Skills 括号句（"NOT for dunning (use this skill for dunning)"）是唯一读起来别扭的地方——"this skill"指代不清（见 §4.6）

### 6.3 中英混杂

全程英文，无中英/其他语种混杂 ✓

### 6.4 Markdown 格式破损

- 代码围栏：L55-57（5 阶段流程图）、L184-186（bash 命令）两处均配对完整 ✓
- 表格：6 张表（原因映射、offer 时机、邮件序列、指标、输出映射、proactive triggers 隐含）+ 2 处列表，分隔线行数正确、无错列 ✓
- 粗体/反引号配对 ✓
- 无孤立围栏、无错位引用块 ✓

### 6.5 占位符未填充

- 无 `TODO`、`FIXME`、`TBD` ✓
- 无空表（对比 297 号的三张空表，本 skill 表格全部有内容）✓

### 6.6 截断内容

- L231 以 Related Skills 最后一条结束，文件完整 ✓
- 无截断迹象 ✓

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` 的 12 条合规清单:

1. **name 小写+连字符、≤64、匹配目录**: ✅ `churn-prevention` 匹配 `224-churn-prevention`
2. **description 第三人称、WHAT+WHEN+KEYWORDS、≤1024**: ⚠️ WHAT 以祈使动词 "Reduce" 开头（无主语），其余合规，约 340 字符
3. **description 无祈使/第一/第二人称开头**: ⚠️ "Reduce voluntary and involuntary customer churn..." 是祈使结构
4. **description 无跨 skill 路由**: ✅
5. **description 含触发信号短语**: ✅ "Use when the user wants to..."
6. **frontmatter 无禁止字段**: ✅ 仅 name + description
7. **body ≤600 行**: ✅ 232 行
8. **body 含 workflow/process 节**: ⚠️ 无显式 Workflow 标题；流程内容存在但三模式选择逻辑缺失
9. **body 含 output format 节**: ✅ "## Output Artifacts"
10. **body 含 scope/limitations 节**: ❌ 完全缺失
11. **body 无跨 skill 文件路径引用**: ✅ 全部散文式引用
12. **目录 NNN-kebab-case**: ✅

**合规率: 9.5/12 ✅，1 项硬违规（规则 10），2 项软违规（规则 2/3、规则 8）**

### 违规详情

**违规 1 — 缺少 Scope/Limitations 节（规则 10，硬违规）**: 同 §3.2.1。SKILL-SPEC §3.1 的三必需节中唯一缺失。

**违规 2 — Workflow 节不完整（规则 8，软违规）**: 流程内容散落于业务章节，无统一 Workflow 节，且三模式（最大的流程分支）无选择逻辑。

**违规 3 — description 祈使开头（规则 2/3，软违规）**: "Reduce..." 无主语。影响面小（内容准确、触发明确），但严格逐条对照不合格。

### 对照 SKILL-SPEC §3.4 内容准则

| 准则 | 表现 | 判定 |
|------|------|:----:|
| Knowledge delta over redundancy（知识增量） | 未解释"什么是流失/什么是 SaaS"等基础概念，直接进入流程设计 ✓ | ✅ |
| Anti-patterns over generic advice（反模式） | "No pre-checked boxes, no confusing language"、"No countdown timers unless genuinely expiring"、"No blame. No shame."——NEVER 规则具体且带理由 ✓ | ✅ |
| Decision trees over prose（决策表） | 原因→offer、offer 时机、指标 benchmark 均用表 ✓；但**模式选择**这个最大的分支用散文 ⚠️ | ⚠️ |
| Concrete over abstract（具体化） | 具体天数（3/5/7/3）、具体文案（"Before you go — [offer]"）、具体 CTA（"Yes, cancel my account"）、具体百分比 ✓ | ✅ |

总体：§3.4 四项准则三项优秀、一项部分达标。内容质量准则层面表现突出，结构层面（Scope 缺失）是主要拖累。

---

## 8. 人机感评估

### 8.1 Emoji 审计

- 全文出现 3 个 emoji：🟢 🟡 🔴（L222，Communication 节的置信度标记定义）
- **属于功能性使用**：为输出的置信度分级提供视觉锚点（verified / estimated / assumed），非装饰性 emoji
- 与 322 号"零 emoji"的克制风格不同，但这里 emoji 承担语义功能且有明确定义，判定：可接受 ✓。唯一风险是 agent 可能过度使用（输出每段都贴 emoji），skill 未限制使用频次——轻微建议

### 8.2 全大写/喊叫式语言

- 无 `STOP!`、`MANDATORY`、`CRITICAL` ✓
- "Never" 出现 3 次（"don't hide it — dark patterns destroy trust"、"No pre-checked boxes"、"Never" 未直接出现但否定式高频），均为具体禁令带理由，非空洞强调 ✓
- 全大写仅用于 CTA 示例文案（"Yes, cancel my account"）——那是交付物示例，合理 ✓

### 8.3 Persona 语气分析

- L8: "You are a SaaS churn prevention and retention specialist."——第二人称角色声明，属于 skill 对执行 agent 的角色设定，符合此类 tool 型 skill 惯例
- 整体语气：**专家式务实 + 强人文关怀**。这是本 skill 人机感最突出的地方：
  - "A cancel flow is not a dark pattern — it's a structured conversation"（L51）——正面立场的行业价值观
  - "If they still want to cancel, let them"（L51）——尊重用户意愿，反强制
  - "No blame. No shame. Card failures happen — treat customers like adults"（L157）——对用户尊严的强调
  - "Don't show a generic discount — it signals your pricing was fake"（L71）——对商业诚信的坚持
  - "Subject lines: specific over vague"（L156）——实操细节到位

### 8.4 人机边界分析

- 本 skill 是"设计咨询型"skill，agent 不接触用户真实支付数据、不操作真实系统，边界风险天然较低
- 隐含边界：所有输出均为**设计/建议**（流程、文案、序列），不包含执行动作（不发邮件、不配置 Stripe）——但该边界未像 322 号那样显式声明（"This isn't a disclaimer..."），与 Scope 缺失呼应
- 缺一处好的边界声明：对"无流失数据的公司"应说明模型/指标均为假设校准（L222 的置信度标记部分承担此功能）

### 8.5 人称分析

- 第二人称 "you/your"：出现在角色声明（L8）、对用户的提问清单（L19-33 "Do you have a cancel flow today?"）、Offer 展示文案（L120-123 "Before you go — [offer]"）——前两处是 skill 对 agent 的指令（代理第二人称，惯例可接受），后一处是交付物模板文案（面向用户，合理）✓
- 第一人称：无（L120 的 "your pricing was fake" 中的 your 指用户）✓
- 第三人称：无（本 skill 不描述自身行为）——tool 型 skill 常见风格
- 判定：人称使用符合 tool 型 skill 惯例 ✓

### 8.6 表格使用评估

6 张表格全部承担结构化决策数据（映射、时机、时序、benchmark、交付物映射），无装饰性表格 ✓。表格是此类 skill 的正确载体，与 SKILL-SPEC §3.4 "决策表优于散文"一致。

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 agent 只拿到 SKILL.md：

- **能启动**：Before You Start 给出了完整的上下文收集清单（L19-33），流程设计部分（5 阶段、原因映射、offer 打法）自足可执行 ✓
- **能交付**：Output Artifacts 表定义了 6 类交付物的形态 ✓
- **会碰壁两处**：
  1. L160 读取 dunning-guide.md → 文件不存在（dunning 交付物只能靠摘要表产出）
  2. L185/L211 运行 churn_impact_calculator.py → 脚本不存在（"Model churn impact" 交付物直接失败）
- 打分: **6/10** — 主体可执行，但两个交付物受损

### 9.2 步骤可操作性

| 环节 | 可操作性 | 说明 |
|------|:--------:|------|
| 上下文收集 | 🟢 | 三组问题清单（当前状态/业务/目标）具体可问 |
| 模式选择 | 🟡 | 无决策表；agent 需自行推断（用户说"取消太多"→Mode 1/2；说"扣款失败"→Mode 3） |
| 5 阶段流程 | 🟢 | 每阶段有明确动作 + 反模式禁令 + 文案示例 |
| 退出调研 | 🟢 | 1 题必答 + 6-8 选项 + 选项表全量给出 |
| 挽留 offer | 🟢 | 6 类 offer × 使用/不使用时机 + 展示规则 4 条 |
| Dunning 序列 | 🟡 | 重试时间表 + 邮件序列表可用，但两者不同步（§4.2），且完整文案缺失 |
| 指标计算 | 🟡 | benchmark 表完整，但 MRR 影响模型依赖缺失脚本 |
| 主动触发 | 🟢 | 6 个信号 + 每种的处理动作 |
| 输出沟通 | 🟢 | 4 条模式（结论先行/What-Why-How/owner+deadline/置信度） |

### 9.3 工具依赖合理性

- 依赖工具：Read（marketing-context.md）、Bash（churn_impact_calculator.py——脚本缺失）、Glob（查找用户流程/处理器信息）
- 外部依赖：无硬编码第三方服务 ✓
- 无网络调用需求 ✓
- 唯一工具性问题：Bash 调用的目标脚本不存在

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 定义 20 个 criteria（SCOPE-01~03, PROC-01~04, FMT-01~04, PRI-01~03, NEG-01~02, QA-01~04）+ 3 个 critical failures，pattern 声明为 `tool`（L2）。

**SCOPE（3 项）**：
- SCOPE-01（llm）: 识别流失预防任务 + 选择正确模式——与 "## How This Skill Works" 一致 ✓
- SCOPE-02（script）: `tool_log_contains("marketing-context")`——与 L15 的输入约定配套 ✓
- SCOPE-03（llm）: 设计前收集上下文——与 "## Before You Start" 一致 ✓

**PROCESS（4 项）**：5 阶段结构 ✓ / 单题必答调研 + 先采集原因后展示 offer ✓ / 一因一 offer ✓ / dunning 含重试 + 卡片更新 ✓——全部能在 body 中找到对应内容 ✓

**FORMAT（4 项）**：5 阶段交付物含文案 + 映射表 + 确认邮件模板 ✓ / dunning 交付物含重试表 + 5 邮件 + 卡片更新清单 ✓ / 调研交付物含映射表 ✓ / 指标绑定 benchmark 值 ✓——FMT-04 的 benchmark 数字（10-15% good / 20%+ excellent / 25-35% / <2% / <1%）与 L170-175 完全一致 ✓

**PRINCIPLES（3 项）**：无暗黑模式 ✓ / offer 展示规则 ✓ / 邮件无责备 + 主题行具体 + 直链更新页 ✓——与 L51-51、L119-123、L155-158 一致 ✓

**NEGATIVE（2 项）**：不隐藏取消按钮 ✓ / 不推荐全员通用折扣 ✓——与 L51、L71 一致 ✓

**QA（4 项）**：主动触发信号 ✓（与 L190-200 的 6 信号一致）/ 审计模式评分卡（QA-02，注意 L153 的豁免条款 "Answer yes if the task was not an audit"）/ 取消后生命周期 ✓（与 L80-82 一致）/ 沟通模式 ✓（与 L216-222 一致）

**Critical Failures（3 项）**：
- CF-01（隐藏取消按钮/暗黑模式 → cap_to_0）: 与 L51 的明文禁令一致 ✓ 合理
- CF-02（全员通用折扣 → cap_to_0）: 与 L71、L102 的映射规则一致 ✓ 合理
- CF-03（支付失败问题却不给 dunning 方案 → cap_to_0）: 与 L127-160 的 Dunning 节一致 ✓ 合理

覆盖完整性：**优秀**。20 个测评点全部能在 SKILL.md 中找到明确支撑内容，无凭空测评点。

### 10.2 覆盖缺口建议

1. **QA-02 与 body 脱节**：QA-02 要求审计模式产出 "scorecard (0-100) with gaps, save rate benchmarks, and prioritized fixes"，但 body 未定义评分卡结构（§4.1 已述）——测评点依赖 agent 的领域常识而非 skill 内容
2. **无模式选择测评点**：SCOPE-01 只问"识别为流失预防 + 选模式"，没有 criterion 验证模式选择逻辑的正确性（用户说"扣款失败"却选了 Mode 1 也能通过？）
3. **无 Related Skills 路由测评点**：agent 是否正确地"不调用 pricing-strategy 处理挽留 offer"未被检验
4. **无失效引用防御**：无任何 criterion 检查 agent 是否被 dunning-guide.md / churn_impact_calculator.py 的缺失绊住——一旦 19 个 llm 项都通过而 1 个 script 项也通过，评测将完全掩盖引用失效问题

### 10.3 评测设计的结构性观察

20 项中 **19 项为 LLM judge，仅 1 项（SCOPE-02）为 script judge**。这不是错误——check.py 的 docstring 明确"llm items excluded"——但意味着：
- 客观性依赖 LLM judge 的一致性和 prompt 质量
- check.py 对评测结果的信息量贡献极低（仅 1 个布尔值）
- 若评测框架要求"script 可验证项 ≥ 一定比例"，本 skill 不达标（建议至少为 SCOPE-03 的上下文收集、QA-01 的触发信号输出增加 script 检查）

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 存在于 `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`，其中 224 号的相关记录（Batch 207-225 摘要）:

> **逻辑**: "224 三种模式与指标表一致但引用文件缺失"——与本次审查 §4.1（模式与结构一致）和 §5（引用失效）**完全吻合**。dossier 已确认"三模式与指标表一致"是正面项，"引用文件缺失"是负面项。
>
> **合规**: "206/223/224 🟠 需不同程度修复"——224 号被归入合规需修复档位，与本次审查 §7（9.5/12 合规率，Scope 缺失）一致。

dossier 对 224 的整体评级为 **🟠**（需修复），与本 REVIEW 的 §12 结论（🟡 B，结构缺陷集中在引用与 Scope）方向一致，但本审查发现的具体问题比 dossier 摘要更细：

1. dossier 未指出的问题：重试/邮件序列不同步（§4.2）、description 祈使开头（§7）、QA-02 与 body 脱节（§10.2）、SCORING 19/20 LLM judge 的客观性依赖（§10.3）
2. dossier 已指出、本次详细展开的问题：两个引用文件缺失（§5）

---

## 12. 综合评分

### 维度评分

**Frontmatter 合规 (9/10, 权重 10%)**: name/触发信号/字段白名单全部合规。description 祈使式开头轻微违规（"Reduce..." 无主语）。

**Body 结构完整 (6/10, 权重 10%)**: Output Artifacts 合格。三必需节中 Scope/Limitations 完全缺失。Workflow 节无显式标题、模式选择逻辑缺失。无空表（优于 297 号）、无死文件（但反向地有两处死引用）。

**逻辑一致性 (7/10, 权重 20%)**: 三模式与内容结构一致、5 阶段衔接正确、指标与 SCORING 完全对齐。主要扣分：重试时间表与邮件序列在 Day 15/Day 18 冲突且无交叉时序说明（§4.2）；"Discount or downgrade" 违反"一因一 offer"规则（§4.3）；5-8% MRR 恢复率无推导（§4.4）。

**参考完整性 (3/10, 权重 15%)**: **两处引用 100% 失效**——references/dunning-guide.md（L160）与 scripts/churn_impact_calculator.py（L185/L211）均不存在，且无对应目录。dunning 完整文案与 MRR 影响计算器两个核心资产缺失。marketing-context.md 引用（输入约定）合规。

**语法格式 (9/10, 权重 10%)**: 英文质量高、无拼写错误、Markdown 完全规整、无占位符残留。唯一瑕疵是 Related Skills 的 "this skill" 指代不清（§4.6）。

**规范合规 (8/10, 权重 15%)**: 12 条中 9.5 条达标。硬违规：Scope/Limitations 缺失（规则 10）。软违规：description 祈使开头（规则 2/3）、Workflow 节不完整（规则 8）。§3.4 内容准则三项优秀一项部分达标。

**人机感 (9/10, 权重 10%)**: 行业价值观端正（反暗黑模式、尊重用户、无责备文化），具体禁令带理由，emoji 仅功能性使用。边界声明偏少（与 Scope 缺失联动），扣 1 分。

**可执行性 (6/10, 权重 10%)**: 主体可执行、交付物定义清晰。两个交付物（dunning 完整序列、MRR 影响模型）因资产缺失受损；模式选择需 agent 自行推断。

**加权总分**: 9×0.10 + 6×0.10 + 7×0.20 + 3×0.15 + 9×0.10 + 8×0.15 + 9×0.10 + 6×0.10 = 0.9 + 0.6 + 1.4 + 0.45 + 0.9 + 1.2 + 0.9 + 0.6 = **6.95 → 70/100**

### 评级: 🟡 B (70/100)

内容质量与结构设计（三模式、5 阶段、映射表、benchmark）属于 corpus 中游偏上水平，主要扣分集中在**资产缺失**（两个引用文件）与**结构缺项**（Scope/Limitations）。与 dossier 的 🟠 评级一致。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: 创建 `references/dunning-guide.md`（或移除 L160 引用）**
- 位置: SKILL.md L160；新文件 `references/dunning-guide.md`
- 内容应至少包含: 5 封邮件的完整 subject line + body copy 模板、重试设置示例（Stripe/Braintree 的配置步骤或伪代码）、卡片更新服务启用检查清单
- 不做修复的后果: Agent 按指引读取必失败；dunning 交付物只能输出摘要表级别的信息，FMT-02/PROC-04 质量受损

**F-2: 创建 `scripts/churn_impact_calculator.py`（或移除 L184-185、L211 引用）**
- 位置: SKILL.md L184-185（Metrics 节调用）、L211（Output Artifacts 表）
- 脚本应: 接受当前 MRR、自愿/非自愿流失率、save rate、recovery rate 输入，输出月度/年度 MRR 恢复额（30-60 行纯 Python，无需依赖）
- 备选方案: 若不想维护脚本，将 L211 改为 "Model churn impact → 按 Metrics 节公式手算，输出 MRR 恢复表"，并删除 L184-185 的 bash 调用块
- 不做修复的后果: "Model churn impact" 交付物直接失败；agent 执行 `python3` 时报文件不存在，浪费评测轮次

**F-3: 新增 `## Scope / Limitations` 节**
- 位置: SKILL.md，建议放在 "## Output Artifacts" 之后、body 末尾
- 内容建议:

```markdown
## Scope and Limitations

This skill does NOT:

- **Configure payment systems or send emails.** It designs flows, sequences, and copy. Stripe/Braintree setup, email delivery, and A/B testing execution are out of scope.
- **Redefine pricing strategy.** Pricing/packaging restructuring belongs to the pricing-strategy skill; this skill only maps offers to exit reasons within the current pricing.
- **Guarantee save/recovery rates.** Benchmarks are industry references, not promises. Without the user's own churn data, all impact figures are estimates (see Confidence Marking).
- **Run without user context.** Cancel flow design requires the current state, business context, and goals from Before You Start; the skill refuses to design on assumptions.
- **Work as a replacement for churn rate reduction at scale.** If monthly churn exceeds 5%, flag product/ICP review (see Proactive Triggers) rather than claiming retention fixes alone suffice.
```

- 不做修复的后果: 违反 SKILL-SPEC §3.1 规则 10（硬违规）；agent 可能越界承诺挽回率或误入定价领域

### 🟡 重要缺陷（建议修复）

**I-1: 同步重试时间表与邮件序列（修复 §4.2 矛盾）**
- 位置: SKILL.md L134-138 与 L147-153
- 修复方案（二选一）:
  - 方案 A（推荐）: 统一为单一时间轴，邮件在重试前触发。如: Day 0 失败邮件 → Day 3 Retry 1（同日 Day 3 邮件）→ Day 7 邮件 → Day 8 Retry 2 → Day 12 邮件 → Day 15 Retry 3 → Day 18 Final retry + 取消邮件
  - 方案 B: 将邮件序列的 Day 15 "Account paused/canceled" 移到 Day 18/19，并显式加一句 "Retries run independently of the email cadence; emails are sent after each failed retry."
- 不做修复的后果: agent 按两个表分别产出交付物时自相矛盾——账户第 15 天已取消、第 18 天仍在重试

**I-2: 增加三模式选择决策表**
- 位置: SKILL.md L36-46（"## How This Skill Works"）
- 修复: 在三种模式描述后加判定表:

```
| User says...                                      | Mode |
|---------------------------------------------------|------|
| "No cancel flow" / "cancellation is instant"      | 1: Build Cancel Flow |
| "Save rate is low" / "audit my cancel flow"       | 2: Optimize Existing Flow |
| "Payment failures" / "involuntary churn"          | 3: Set Up Dunning |
| Multiple problems                                 | Start with the dominant one, then apply the others |
```

- 不做修复的后果: 模式选择依赖 agent 推断，SCOPE-01 结果不稳定；SKILL-SPEC §3.4"决策表优于散文"不达标

**I-3: 消除 "Discount or downgrade" 的映射歧义（修复 §4.3）**
- 位置: SKILL.md L93
- 修复: 明确主次。如: "Too expensive / pricing → Discount (if one tier below fits) else Downgrade"——保留一个主 offer、一个条件分支，并加一行实现注: "The mapping table must yield exactly one primary offer per reason; the Playbook below resolves ties."
- 不做修复的后果: 违反 L102 自己声明的"exactly one offer type per reason"规则，NEG-02/PROC-03 的判定出现歧义

**I-4: description 改为第三人称**
- 位置: SKILL.md L3
- 当前: "Reduce voluntary and involuntary customer churn through..."
- 修复: "Designs cancel flows, retention offers, exit surveys, and dunning sequences to reduce voluntary and involuntary customer churn. Use when the user wants to analyze churn patterns, design retention strategies, optimize cancellation experiences, or reduce involuntary churn from payment failures."
- 不做修复的后果: 违反 SKILL-SPEC §2.3（严格逐条时判不合规）

**I-5: 为 SCORING.yaml 补充 2-3 个 script 可验证项**
- 位置: SCORING.yaml
- 建议:
  - SCOPE-03 可加 script 变体: 检查 agent 输出中含问句（收集上下文）或在提问前先输出 "current state" 关键词
  - QA-01 可加 script 变体: `output_contains("dunning|recovery|retry")`（触发信号输出）
  - 新增: `output_not_contains("hide|cancel button")` 作为 NEG-01 的 script 变体
- 不做修复的后果: 20 项中 19 项依赖 LLM judge，评测客观性风险集中

### 🟢 优化建议（锦上添花）

**O-1: 为商业数据补出处或置信度标注**
- 位置: L10（5-8% MRR）、L129（20-40% 流失占比）、L170-175（benchmark 表）
- 修复: 在 Metrics 节 benchmark 表下方加一行来源注（如 "Benchmarks: industry compilations (e.g., Recurly, ProfitWell public benchmarks); treat as 🟡 estimates"），或将 Communication 节的置信度标记（L222）前移到 benchmark 定义处

**O-2: 修正 Related Skills 的 "this skill" 指代**
- 位置: L229
- 当前: "NOT for dunning (use this skill for dunning)"
- 修复: "NOT for dunning (use churn-prevention for dunning)"

**O-3: QA-02 的评分卡结构下沉到 body**
- 位置: SCORING.yaml QA-02 + SKILL.md
- 修复: 在 "## Output Artifacts" 的 "Audit my cancel flow" 行下补一行: "Scorecard: 100 分按 5 阶段 × 每阶段 20 分计，附差距清单、benchmark 对照、按影响排序的修复清单"——使测评点有技能内支撑

**O-4: 补充 `allowed-tools` 字段**
- 位置: SKILL.md frontmatter
- 修复: `allowed-tools: Read, Bash, Glob`（对应 marketing-context.md 读取与计算器运行）

**O-5: check.py 清理未使用导入**
- 位置: check.py L12-20
- 现状: 导入 15 个 checker 函数，实际使用 3 个（set_tool_log_path、set_agent_output、tool_log_contains），且 `file_exists`、`file_contains` 等 12 个未使用
- 修复: 仅导入实际使用的函数；若未来计划扩展 script 检查（见 I-5），再按需导入

### 修复工作量估计

- 预计修改行数: SKILL.md 新增 ~45 行（Scope 节 + 模式表 + 时序修正）± 修改 ~10 行；新文件 2 个（dunning-guide.md ~60 行、churn_impact_calculator.py ~50 行）；SCORING.yaml 修改 ~15 行；check.py 修改 ~5 行
- 预计修改文件数: 4-5 个（SKILL.md、SCORING.yaml、check.py、新建 references/、新建 scripts/）
- 优先级建议: F-1/F-2 先做（资产缺失直接影响评测），F-3 次之（合规硬伤），I 系列随后

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 232 行，全文精读
2. SCORING.yaml — 183 行，全文
3. check.py — 73 行，全文
4. _shared/SKILL-SPEC.md — 161 行，全文（合规依据）
5. _shared/checker.py — 351 行，全文（check.py 依赖库验证）
6. _shared/CHECKER-LIBRARY.md — 存在（未精读，功能与 checker.py 重复）

### 辅助核验
- `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` — 224 号条目（Batch 207-225 摘要），用于 §11
- 目录清单 `D:\SkillIF\skill-experiment\complex-skills\224-churn-prevention\` — 确认仅 3 文件、无 references/ 与 scripts/

### 读取统计
- 总文件数: 5（3 skill 文件 + 2 shared 文件）
- 总行数: 约 1,000 行

### 审查方法
- 所有 skill 文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条清单 + §3.4 内容准则
- 引用完整性: 以 SKILL.md 中全部 `references/`、`scripts/`、`data/` 路径对目录实际内容逐一核对
- SCORING.yaml 交叉: 20 个 criteria + 3 个 critical failures 逐一与 body 对应内容比对
- 评分口径: 与 297/322 号审查相同的 8 维加权体系

### 审查发现的摘要

| 类别 | 数量 | 明细 |
|------|:----:|------|
| 🔴 致命 | 3 | F-1 死引用 dunning-guide.md；F-2 死引用 churn_impact_calculator.py；F-3 缺 Scope/Limitations 节 |
| 🟡 重要 | 5 | I-1 重试/邮件时序矛盾；I-2 模式选择无决策表；I-3 "Discount or downgrade" 映射歧义；I-4 description 祈使开头；I-5 SCORING 客观性 |
| 🟢 优化 | 5 | O-1 数据出处；O-2 "this skill" 指代；O-3 QA-02 支撑；O-4 allowed-tools；O-5 未用导入 |

---

## 变更记录
- 2026-08-06: 初始深度审查。三个文件全部精读。确认 dossier 🟠 评级（引用缺失）；新发现重试/邮件时序矛盾与 Scope 缺失。评级 🟡 B (70/100)。
