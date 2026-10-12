# REVIEW: 124-customer-feedback-analyzer

**审查日期**: 2026-08-06
**Skill 类型**: process — 多渠道用户反馈的收集、分类、优先级评分与闭环工作流
**Body 行数**: 466 行（SKILL.md 共 470 行，frontmatter 4 行）
**参考文件数**: references/0, scripts/0, assets/0, 其他 4（SKILL.md, SCORING.yaml, check.py, manifest.yaml）

---

## 1. 目录全量清单

本技能目录共 4 个文件、717 行，**没有任何子目录**（无 references/、scripts/、assets/、resources/、templates/、examples/、specs/、phases/、docs/ 等）。所有内容全部内联在 SKILL.md 正文中，属于完全自包含的知识型 process skill。

```
D:\SkillIF\skill-experiment\complex-skills\124-customer-feedback-analyzer\
├── SKILL.md        (470 行)   — 主文件：原理 + 6 渠道 + 4 维分类 + 评分公式 + 闭环 + 模式 + 周报模板 + 工具 + 节奏 + 清单
├── SCORING.yaml    (123 行)   — 13 项测评标准：scope 3 / process 4 / output 3 / negative 2 / qa 1，含 2 条 critical_failures
├── check.py        (74 行)    — 脚本评测器：4 项 script judge 检查（PROC-02, OUT-01, OUT-02, OUT-03），依赖 ../_shared/checker.py
└── manifest.yaml   (50 行)    — 技能元数据清单（与 SKILL.md frontmatter 基本一致）
```

逐文件行数分布：SKILL.md 470 行（占 65.6%）、SCORING.yaml 123 行（17.2%）、check.py 74 行（10.3%）、manifest.yaml 50 行（7.0%）。文件规模合理，无超大文件也无残桩文件。

---

## 2. Frontmatter 逐字段审查

frontmatter 仅 3 个字段，紧凑且全部合格。

**name**: `customer-feedback-analyzer` — 与目录编号 124 对应，kebab-case 规范，与 SCORING.yaml 的 `skill:` 字段、manifest.yaml 的 `name:` 字段完全一致，无命名漂移。

**description**（1 行，无换行折叠）："Synthesize user feedback from multiple channels and identify patterns to inform product decisions. Use when analyzing feedback, prioritizing feature requests, conducting NPS surveys, or understanding user sentiment. Covers feedback collection, categorization, prioritization frameworks, and closing the feedback loop."

逐要素核验：
- 第三人称 ✓ — "Synthesize user feedback..." 是描述性第三人称，无第一/第二人称、无祈使句。
- WHAT ✓ — "Synthesize user feedback from multiple channels and identify patterns to inform product decisions" 明确定义功能范围。
- WHEN/触发条件 ✓ — "Use when analyzing feedback, prioritizing feature requests, conducting NPS surveys, or understanding user sentiment" 给出 4 类触发场景，符合规范要求的 trigger 信号短语结构。
- KEYWORDS 覆盖 ✓ — "collection, categorization, prioritization frameworks, and closing the feedback loop" 覆盖正文全部四大模块（渠道收集、分类、优先级、闭环）。
- 无跨技能路由、无 "@" 交叉引用、无截断或语法破损 ✓ — 与 corpus 中 047/314 等截断 description 形成鲜明对比。

**结论**: frontmatter 是规范的正面样例，10/10 无保留。唯一可挑剔的是 description 与 manifest.yaml 中同一文本在 manifest 中被 YAML 折叠换行书写（`description: Synthesize user feedback...patterns\n  to inform...`），两者内容逐字一致，无分叉。

---

## 3. Body 逐段结构分析

Body 共 466 行，15 个章节。逐段分析如下：

**# Customer Feedback Analyzer（H1 + 1 行简介, 行 6-8）**：标题正确、单句简介 "Collect, analyze, and prioritize user feedback to inform product decisions." 与 description 呼应。

**## Core Principle（行 10-12）**：全篇锚点 — "Never collect feedback you won't act on." 一句话加一段解释（收集反馈即产生行动预期，不承诺行动就不要索取）。该原则贯穿全文，并在 SCORING.yaml 的 SCOPE-03、NEG-01、NEG-02 三处化为测评标准，是 skill 设计中最亮眼的一笔。

**## Feedback Channels（行 14-111）**：6 个子节，每个渠道统一采用 "Best for → 代码/结构化示例 → Pros/Cons 或要点" 的模板化结构：
1. In-App Feedback Widget（行 16-33）— JSX 代码示例带 context 对象
2. NPS Surveys（行 35-56）— 0-10 量表、Promoter/Passive/Detractor 分档、NPS 公式、基准线（Excellent ≥50 / Good 30-49 / Needs Work <30）
3. Support Tickets（行 58-67）— 3 条模式识别启发式（5+ 次同类问题、单票超 10 分钟、票量尖峰）
4. User Interviews（行 69-81）— 30 分钟访谈结构（5+10+10+5）、样本量 5-10 人
5. Feature Request Voting（行 83-99）— 工具列举（Canny/ProductBoard/Upvoty）+ 收益/避免清单
6. Exit Interviews（行 101-111）— 4 个关键流失问题

结构一致性好，每个渠道的示例都是"可用于生产"的（模板、评分档位、访谈脚本），不是空泛描述。

**## Feedback Categorization（行 113-189）**：4 个维度，各为一张 YAML 结构表：
- By Type（行 115-137）— Bug/Feature Request/Enhancement/Usability/Performance 五类，每类带示例 quote 和优先级
- By Severity（行 139-157）— Critical/High/Medium/Low 四档，各带行动时限（Hotfix immediately / Fix this sprint / Fix next quarter / Backlog）
- By Frequency（行 159-173）— 四档频段（50+ / 10-50 / 5-10 / <5）映射到优先级
- By User Segment（行 175-189）— Power/New/Churned/Enterprise 四类用户，标注每类的反馈特征

四维分类正交、无重叠冲突，是分析阶段的核心操作框架。

**## Prioritization Framework（行 191-221）**：评分公式 `Score = Impact (1-5) × Frequency (1-5) × Strategic Alignment (1-5)`，三档阈值（≥40 High / 20-39 Medium / <20 Low），后接正反两个算例（Slack integration 4×5×4=80 → HIGH；button color 1×1×1=1 → LOW）。算例算术全部正确（4×5×4=80、1×1×1=1）。

**## Close the Feedback Loop（行 223-301）**：闭环 4 步 — Acknowledge（感谢邮件模板）、Act（决策树）、Notify Users Who Requested It（上线通知邮件模板）、Public Changelog（变更日志模板）。决策树（10+ 次→上路线图、战略对齐→优先、2 周可发→快赢）与评分公式互补。两个邮件模板均可直接复制使用，P.S. 引导用户回复的设计有真实产品运营功力。

**## Common Feedback Patterns（行 303-344）**：3 个常见认知陷阱 — Squeaky Wheel Syndrome（少数活跃者≠真实需求，用数据验证）、Silent Churn（无投诉流失，主动排查）、Feature Bloat Risk（Excel/CSV/JSON/PDF 导出四连例子生动且准确传达"建通用方案而非逐变体"）。该节为 SCORING.yaml 的 PROC-03 提供直接素材。

**## Synthesis & Reporting（行 346-398）**：Weekly Feedback Summary 完整 YAML 模板，包含 period、total_items、top_themes（theme/frequency/severity/example_quotes/recommended_action 五要素）、nps（score + detractor_reasons）、prioritized_backlog（feedback/score/priority 三要素）。该节直接对应 SCORING.yaml 的 OUT-01/OUT-02/OUT-03 三项 script 检查，模板字段名与测评 pattern 逐字匹配（详见第 10 节）。

**## Tools & Software（行 400-416）**：按收集/分析/路线图透明三组列举第三方工具。纯参考性内容，无推销、无评测色彩，信息中性准确。

**## Feedback Cadence（行 418-439）**：Daily/Weekly/Monthly/Quarterly 四层运营节奏表，将分析工作落到可排期的频率上。

**## Quick Start Checklist（行 441-450）**：8 项可勾选清单，全部具体可执行（"Set up in-app feedback widget"、"Schedule NPS survey (monthly)"）。

**## Common Pitfalls（行 452-458）**：5 条 ❌ 反模式清单，均为真实产品失误（收集不行动、全建全要、不验证数据、忽视沉默多数、无跟进）。

**## Summary（行 460-469）**：6 条 ✅ 总结要点，回收正文全部模块。

总体结构评价：管线完整（收集→分类→评分→闭环→节奏→清单），段落密度均匀，无空节、无残桩、无重复粘贴。唯一的结构性缺口是**没有显式命名的 Workflow、Scope/Limitations、Output Format 三个章节**——管线逻辑隐含在章节顺序中，Synthesis & Reporting 充当输出格式，Core Principle + Common Pitfalls 部分充当边界声明，但都不是规范要求的显式节名。这一点与 SKILL-SPEC 的"三必需节"要求存在形式差距（详见第 7 节）。

---

## 4. 逻辑一致性深度审查

整体自洽性良好（管线、公式、阈值在各节之间互相呼应），但深入比对后发现 **1 处确定的内部矛盾 + 2 处跨章节数值张力**。

### 4.1 确定性矛盾：score 45 标注为 medium，违反公式阈值（🔴 需修复）

Prioritization Framework 明确写道：

```
Score ≥ 40: High Priority (next sprint)
Score 20-39: Medium Priority (next quarter)
Score < 20: Low Priority (backlog or never)
```

而 Synthesis & Reporting 的 prioritized_backlog 示例：

```yaml
- feedback: "Optimize dashboard performance"
  score: 45
  priority: medium
```

45 ≥ 40，按公式应判 **High Priority**，示例却标 **medium**。而同一 backlog 中 score 16（<20）标 low 是正确归类的，score 80（≥40）标 high 也是正确的——唯独中间这行错了。这要么是分数写错（应为 35-39 区间的值才匹配 medium），要么是 priority 标错（应为 high）。这是**本 skill 最严重的逻辑缺陷**：测评场景下若 agent 直接照抄该示例做输出模板，会产出与技能自身规则矛盾的结论。SCORING.yaml 的 OUT-03 只检查字段名不检查数值一致性，所以这类错误不会被自动化评测捕获，但会被 LLM judge 和下游人工审查发现。

另外注意：top_themes 中 "Slow Dashboard Load" 的 severity 标为 medium，而 Slack Integration（23 次提及）标 high——severity 标注与 backlog 的 medium 自洽，但与公式阈值不自洽。修复方向应该是把 score 改成 35（3×5×3 或 3×3×4 等落在 20-39 的组合），或把 priority 改成 high 并同步 severity 说明。

### 4.2 数值张力：Slack 集成在两个示例中频次不一致（🟡）

Prioritization 示例对 "Add Slack integration" 标注 `Frequency: 5 (50+ requests)`，而 Synthesis & Reporting 中同一主题（主题名同为 "Slack Integration"，且是 weekly summary 的头号主题）标注 `frequency: 23`。同一反馈项在两个示例中频次从 50+ 变成 23，且 summary 里 score 80 = 4×5×4 需要 Frequency=5（即 50+），与自报的 23 次不一致——按技能自己的 By Frequency 频段表，10-50 次属 "Common" 档，应映射到中优先级。即：**示例内部的 frequency 字段（23）与 score 反推的 frequency（5）互相矛盾**。若 agent 照模板填周报，可能填出 frequency 23 但 score 80 这种自相矛盾的条目。

### 4.3 频段表与评分公式之间缺少映射定义（🟢 优化级）

By Frequency 的档位（50+/10-50/5-10/<5）与公式的 Frequency 轴（1-5）没有给出换算规则："50+ 次→5 分？10-50 次→3-4 分？"未定义。同理 Act 决策树的 "10+ times → Add to roadmap" 与频段表 "Common: 10-50 → Medium priority" 的阈值口径不一致（一个看绝对次数、一个走分档+战略对齐）。三者各自内部成立，但拼起来时 agent 需要自行推断映射，存在解释空间。建议在公式后加一行换算表：50+ → 5, 20-49 → 4, 10-19 → 3, 5-9 → 2, <5 → 1（示例值）。

### 4.4 其余一致性核验（通过）

- NPS 基准自洽：summary 中 NPS 42 → "Good: 30-49" ✓。
- By Frequency 与 backlog 一致：Mobile App 8 次 → "Occasional: 5-10 → Low priority, monitor"，backlog 标 score 16 / low ✓。
- 评分算例算术：4×5×4=80、1×1×1=1 ✓。
- 访谈结构 5+10+10+5=30 分钟，与 "User Interviews" 渠道节的样本量 5-10 人一致 ✓。
- Common Pitfalls 的 5 条与 Core Principle、NEG-01/NEG-02、Squeaky Wheel/Feature Bloat 三模式全部互相对应，无漂移 ✓。
- Quick Start Checklist 的 8 项与正文各节一一对应（widget→1、NPS→2、tracking spreadsheet→分类节、tickets weekly→节奏表、interviews→渠道 4、public roadmap→渠道 5、email templates→闭环 1/3、categorization process→分类节）✓。

**逻辑一致性小结**: 骨架完整、设计自洽，但 4.1 是会在实际使用中显形（agent 直接照抄示例输出）的硬伤，4.2 是示例间的口径漂移，两处都应优先修复。修复后此维度可达 9/10。

---

## 5. 参考文件内容级审查

本技能**没有 references/、scripts/、assets/ 等任何子目录**，这是设计决策而非缺失：SKILL.md 将所有示例、模板、公式内联，440+ 行正文足以自给，不引用任何外部文件，也不存在跨 skill 路径（corpus 中常见的 `../_shared/` 引用、指向其他 skill 脚本的悬空引用在此均不存在）。

按 SOP 要求逐文件审查全部 4 个文件（目录内无遗漏）：

**manifest.yaml（50 行）**：
- name/kind/description 与 SKILL.md frontmatter 逐字一致（description 在 manifest 中以 YAML 折叠形式书写，内容相同）✓。
- preconditions 仅一条通用检查 `project_initialized`（"Project environment is set up"），对反馈分析类技能偏形式化——真实前置条件应是"存在反馈数据源（tickets/NPS 结果/访谈记录）"，建议补充。
- domains 列表 8 项（ai/frontend/security/testing/product/design/data/orchestration）经 `&id001` 锚点复用 tags，明显是模板化通用列表而非技能特异（反馈分析的核心 domain 只有 product/design/data），有套模板痕迹。
- side_effects 声明 `modifies_files` + `creates_artifacts`：分析类技能通常产出摘要文档（creates_artifacts 合理），但"modifies_files"与本技能正文（纯分析输出，无修改既有文件的操作）不匹配，建议去掉 modifies_files。
- risk_level: low ✓（无敏感操作，符合正文定位）。
- idempotent: false ✓；success_signal/failure_signals/observability 为通用模板文本，无错误但无信息增量。
- metadata: version 1.0.0、created_at 2025-10-30；`examples: []` 为空——manifest 规范允许但此处留空略可惜，可补一条示例调用。

**SCORING.yaml（123 行）**：详见第 10 节交叉参考。此处要点：13 项标准结构完整、注释分节清晰（scope/process/output/negative/qa）、judge 类型标注准确（9 项 llm + 4 项 script）、2 条 critical_failures 语义正确且与正文原则（Squeaky Wheel 数据验证、不捏造）对应。

**check.py（74 行）**：
- 实现与 SCORING.yaml 的 script judge 完全对齐：4 项（PROC-02 检查 "Strategic Alignment" 字符串、OUT-01 检查 top_themes|recommended_action|example_quotes、OUT-02 检查 detractor_reasons|nps、OUT-03 检查 prioritized_backlog|priority: (high|medium|low)），SCORING.yaml 中恰好也是这 4 项标 judge: script，其余 9 项 judge: llm 在 check.py 中正确注释跳过 ✓。
- 依赖 `../_shared/checker.py`，已确认该文件存在于 D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py，import 路径可解析 ✓（注意：这是测评 harness 的共享库引用，属于评测基础设施，与 SKILL.md 正文无关，不违反"无跨 skill 路径"规范）。
- 参数与协议：`python check.py <workspace> <tool_log> <agent_output>`，输出 JSON {criterion_id: bool}，与 SCORING.yaml 的检查协议一致；main() 中 agent_output 若是文件路径则读取内容，check() 中再做一次存在性判断避免重复设置，逻辑健壮。
- 小瑕疵：`try: _is_path = os.path.exists(agent_output) except (OSError, ValueError)` 中 os.path.exists 对超长路径会抛 OSError，捕获是防御性写法，可接受；check() 返回 dict 的键顺序与 SCORING.yaml 无关紧要。整体无功能性问题。
- 可执行性实测要点：`output_contains` 接收 `"top_themes|recommended_action|example_quotes"` 这类以 `|` 连接的 pattern，语义应是"至少命中其一"，与 SKILL.md 示例输出（同时含三者）兼容 ✓。

---

## 6. 语法与格式质量

**英文质量**: 全文为规范、地道的产品英语，无拼写错误、无病句、无中英混杂、无葡萄牙语残留（corpus 中其他技能常见的葡语泄漏在此完全不存在）。术语统一（feedback/priority/promoter/detractor/churn/close the loop 等全部在全文保持同一译法与拼写）。

**标点与排版**: 无 em 破折号滥用、无乱码、无 markdown 渲染破损（对比 corpus 中 tpl 系列首条编号丢失、杂散 `**` 等格式缺陷，本文件格式干净）。代码块围栏语言标注正确（javascript/yaml/markdown 均与实际内容匹配）。

**结构一致性**: 渠道 6 子节、分类 4 子节、闭环 4 子节均采用统一模板，缩进与层级（### 二级子节）一致。

**YAML 示例的可解析性问题（🟡）**: 正文中的多个 YAML 块是"结构化的伪代码"而非严格可解析的 YAML，存在两处典型模式：
1. 标量值后跟嵌套映射——如 `Bug: Something broken` 下一行缩进的 `- "Export fails with >100 rows"`，严格解析时列表挂在标量值下会报错；Prioritization 算例中 `Feedback: "Add Slack integration"` 下缩进的 `Impact: 4` 同理（标量后不能跟映射）。
2. `- "Too expensive" (12 mentions)` 这种括号注释尾巴不属于标准 YAML 列表项语法。
这些块若被 agent 当作字面 YAML 解析（例如用工具 parse 后回填）会失败，但目前形态作为"示例格式"可读性很好。建议要么全部规范成合法 YAML（标量改映射、注释移出行内），要么在块开头注明"illustrative, not parseable"。考虑到 check.py 的 pattern 匹配是字符串级而非 YAML 级，此问题不影响自动化评测，评级为优化级。

**行数**: 466 行 body，远低于 600 行上限，且信息密度高——没有凑数内容。

---

## 7. 规范合规性

对照 SKILL-SPEC v1.0 逐条核验：

**Description 合规（§2.3）**: ✓ 通过。第三人称、WHAT/WHEN/KEYWORDS 三段结构完整、含 4 组触发短语。这是 corpus 322 个技能中 description 写得最规范的一类。

**三必需节（workflow / output / scope）**: 🟡 部分通过。正文存在完整的工作流管线（渠道→分类→评分→闭环→节奏）和明确的输出模板（Weekly Feedback Summary），但**均未以显式节名出现**——没有 "## Workflow"、"## Output Format"、"## Scope / Limitations" 标题。dossier 判定 "Workflow/output/scope 存在" 应理解为内容级存在而非节名级存在。对 LLM 读取而言，内容存在通常已足够，但规范字面要求是显式节。Core Principle + Common Pitfalls 部分承担 scope 职能（何时不该收集、不该全建），但没有"何时不使用本技能"（如：无反馈数据时不应编造、单条反馈不足以决策）的明确边界声明。

**无跨 skill 路径**: ✓ 通过。正文未引用任何其他技能或 `../` 路径；SCORING/check 的 `_shared` 引用属于评测基础设施，不违规。

**长度与结构**: ✓ body 466 ≤ 600；章节层级规整。

**emoji 使用**: 🟡 边缘合规。Common Pitfalls 5 条 ❌ 和 Summary 6 条 ✅ 为装饰性符号——与 corpus 中判"功能性使用可接受"的先例（如 054、064 的严重度标记）相比，这里的 ❌/✅ 纯粹是列表前缀，删除后语义不变。未达"泛滥"程度（全文仅 11 个），但属于可收敛项。

**allowed-tools**: 未声明，合理（纯知识型技能无需工具白名单）。

**合规小结**: 描述、长度、路径三类硬规则全过；缺口集中在三必需节的显式化。若按最严格字面解释为 🟡，考虑到正文内容已实质覆盖，评级 8/10 合理。

---

## 8. 人机感评估

**语气**: 全篇为"资深产品经理向 agent 传授方法论"的中性专业语气，无 chatbot 腔、无营销腔、无机械感。核心原则 "Never collect feedback you won't act on. ... Destroys trust." 是全文最佳的一句话——简短、有立场、有后果，具备真实产品经验背书，不是空话。dossier 的"产品敏锐语气，以 ... 为锚"评价准确。

**称呼与视角**: 无第一人称叙事、无对用户的直呼、无 "You are a..." persona 模板腔（对比 083-085 系列的空洞 persona）。指令式祈使句（"Fix immediately"、"Add to roadmap"）用在 YAML 值里，是结构化数据而非喊话。

**无 filler、无冗余警告**: 全文没有 "Please"、"Important: remember..." 式填充，也没有 corpus 中常见的重复警告块。

**适度的人性化细节**: 邮件模板中的 "P.S. Have more ideas? Reply to this email."、"Thanks for the feedback that made this happen." 是真实运营场景的细节，增强了模板的可用性而非装饰性。Changelog 模板 "Requested by 47 users" 直接呼应了"通知请求者"的闭环原则。

**评分**: 9/10。唯一扣分点是 ❌/✅ 装饰符号可收敛（见第 7 节），语气本身无可挑剔。

---

## 9. 可执行性评估

**Agent 执行路径**: agent 拿到本 skill 后，可沿 6 渠道→4 维分类→评分公式→Act 决策树→闭环 4 步→周报模板的完整管线执行，无任何需要外部文件或脚本才能启动的步骤。相比 corpus 中"body 是导航壳、核心委托给 references"的 045 类技能，本技能是真正自包含可立即执行的。

**模板即交付物**: 邮件模板 ×2、访谈脚本、周报 YAML schema、changelog 模板均为"复制即用"，Checklist 8 项全部有对应正文内容，无悬空承诺（对比 092 的 "FINAL AUDIT REPORT 从未定义" 类问题）。

**算例正确性**: 算术全部正确（4.1 节的标签矛盾除外），agent 照抄公式可得出正确分数。

**与 SCORING 的适配**: 技能自带示例输出（Weekly Feedback Summary）恰好覆盖 SCORING.yaml 全部 4 项 script 检查的 pattern 字符串——即 agent 按正文模板输出即可通过自动化检查，这是"skill 内容与测评标准对齐"的最佳实践。

**检查器可运行性**: check.py 依赖的 _shared/checker.py 已确认存在；Python 3.9+ 的类型标注 `dict[str, bool]` 与运行环境兼容；命令行协议清晰。

**扣分项**: 4.1 的 score-45-as-medium 矛盾若被 agent 直接模仿，会产出违反自身规则的结果；无显式 Workflow 节意味着不同 agent 对"管线起点/终点"的理解可能略有差异（对自包含知识型技能影响小）。综合 8/10。

---

## 10. SCORING.yaml 交叉参考

SCORING.yaml 与 SKILL.md、check.py 三方对齐程度是本 skill 的另一亮点，逐项核验：

**SCOPE-01 / SCOPE-02 / SCOPE-03（llm）**: 分别对应正文的"功能范围"（收集/分类/优先级/合成/闭环）、6 渠道、Core Principle。其中 SCOPE-03 的问题 "Does the agent avoid recommending feedback collection without a plan to review and act?" 是核心原则的直接评测化，问题措辞精确可判。

**PROC-01（llm）**: 要求"至少两类分类维度"，正文有 4 维，判定宽松合理（避免过度要求 agent 全做）。

**PROC-02（script）**: 检查输出含 "Strategic Alignment" 字符串。正文公式与算例均含该词，agent 照抄即通过。注意该检查的脆弱性——字符串级匹配可被无意义提及绕过，但这是 corpus 通用评测设计，非本技能缺陷。

**PROC-03（llm）**: 三模式（Squeaky Wheel/Silent Churn/Feature Bloat）正文各成一节，"where relevant to the data" 的限定词给了 agent 合理豁免空间，设计成熟。

**PROC-04（llm）**: Act 决策树三问逐字取自正文，一一对应。

**OUT-01/02/03（script）**: 三个 pattern 与正文 Weekly Feedback Summary 的字段名逐字匹配（top_themes/recommended_action/example_quotes、detractor_reasons/nps、prioritized_backlog/priority: (high|medium|low)）。**技能示例输出 = 评测通过的充分条件**，这是全 corpus 少见的强对齐。

**NEG-01 / NEG-02（llm）**: 与 Common Patterns 的 Feature Bloat、Squeaky Wheel 两节直接对应，negative 项与正文反模式一一咬合。

**QA-01（llm）**: 闭环三要素（acknowledge/notify/changelog）与正文闭环 4 步一致（QA 描述缺了第 2 步 "Act"，但 Act 已由 PROC-04 覆盖，无遗漏）。

**critical_failures**: CF-01（单声量驱动决策）与 CF-02（捏造主题/引文）语义正确，cap_to_0 惩罚合理。CF-02 特别值得肯定——反馈分析场景捏造用户引文是真实风险，该条与正文"example_quotes"模板共同构成防捏造的双保险。

**改进建议**: 4.1 的数值矛盾若想在 SCORING 层防御，可在 OUT-03 之外加一条 script/llm 检查（如 "priority tier matches score threshold"），或至少修正示例数值以免评测样例自身矛盾。另外 PROC-02 的 pattern 可扩展为 `Strategic Alignment|Impact|Frequency` 增加鲁棒性（当前仅查一个词）。

---

## 11. 已知问题汇总

1. **🔴 score 45 标注 medium**（SKILL.md 行 391-393）：优先级的 priority 标签与公式阈值（≥40 为 High）矛盾，是唯一需要数值修复的硬伤。
2. **🟡 Slack 集成频次口径漂移**（行 205-210 vs 行 357-362）：先例 50+ requests，周报示例 23 次；score 80 反推 Frequency=5 与 23 次自报不符。
3. **🟡 缺显式三必需节**：无 "## Workflow"、"## Output Format"、"## Scope/Limitations" 标题，内容存在但节名缺失；Scope 未覆盖"何时不使用本技能"。
4. **🟡 YAML 示例非严格可解析**：标量后嵌套映射、括号注释（行 121-131、205-221、382-384），如被工具解析会失败。
5. **🟢 ❌/✅ 装饰符号**：Pitfalls/Summary 共 11 个，语义无增量。
6. **🟢 manifest.yaml 通用化**：domains 8 项为模板锚点复用；side_effects 含 modifies_files 与技能行为不符；examples 为空。
7. **🟢 频段表→Frequency 分值的映射未定义**（行 161-173 vs 行 196）：agent 需自行推断换算规则。
8. **🟢 manifest preconditions 形式化**：`project_initialized` 对反馈分析场景无实际约束力。

不存在的问题（明确排除）：文件截断、引用文件缺失、跨 skill 路径、description 违规、拼写错误、葡语泄漏、重复段落、模板占位符（"the `..` skill" 类）、商业推销。以上在 corpus 其他技能中高频出现的问题，本技能全部免疫。

---

## 12. 综合评分

本 skill 是"内容自包含、示例可执行、测评强对齐"的知识型 process skill，dossier 判定 🟢 完整实用整体成立。但 4.1 的示例内部矛盾是实际使用中会显形的硬伤，三必需节缺显式节名是规范字面差距，因此综合评级落在 🟡B 上沿——修复 4.1/4.2 两处数值问题后即可稳定进入 🟢A 区。

| 维度 | 分数 | 权重 | 加权 |
|------|:----:|:----:|:----:|
| Frontmatter 合规 | 10/10 | 10% | 1.00 |
| Body 结构完整 | 7/10 | 10% | 0.70 |
| 逻辑一致性 | 7/10 | 20% | 1.40 |
| 参考完整性 | 10/10 | 15% | 1.50 |
| 语法格式 | 9/10 | 10% | 0.90 |
| 规范合规 | 8/10 | 15% | 1.20 |
| 人机感 | 9/10 | 10% | 0.90 |
| 可执行性 | 8/10 | 10% | 0.80 |
| **加权总分** | | | **84.0/100** |

评级: 🟡B（上沿，接近 🟢A）

分维度评述：Frontmatter 满分（description 为 corpus 最佳梯队）；Body 结构扣分在缺显式三节；逻辑扣分在 4.1/4.2 两处示例问题；参考完整性满分（自包含、零悬空引用）；语法仅扣 YAML 可解析性；合规扣显式节名与装饰符号；人机感近满分；可执行性扣"照抄示例会产出矛盾结论"的风险。

---

## 13. 修复建议（重点章节）

### 🔴 致命缺陷

严格说本 skill 无"需重写"级缺陷，唯一一处被列为本节头号问题的数值矛盾建议在下次编辑时优先处理：

**1. 修正 prioritized_backlog 中 "Optimize dashboard performance" 的 score 或 priority（SKILL.md 行 391-393）**
- 方案 A（改分数，推荐）：将 score: 45 改为 score: 35（落在 20-39 区间，与 priority: medium 自洽；35 = Impact 5 × Frequency 4 × Alignment 1.75 不整，可换 36 = 3×3×4 或 40 以下任意合法组合，最简为 35 = 5×7×1 也不行——注意三因子都须 1-5，因此 20-39 区间内的可分解组合如 3×3×4=36 或 2×5×3=30）。建议直接写 36 或 30，并保持 Impact/Frequency/Alignment 三因子 1-5 的约束成立。
- 方案 B（改标签）：priority: medium 改为 priority: high，并同步将 top_themes 中该主题的 severity: medium 改为 high（行 366）。
- 方案 A 改动最小且不牵连 severity，优先推荐。修完后请复核：Slack 80/high ✓、Dashboard 36/medium ✓、Mobile 16/low ✓，三个示例与公式全对齐。

**2. 统一 Slack 集成的频次口径（行 205-210 与行 357-362）**
- 将 Prioritization 算例的注释 "(50+ requests)" 改为 "(23 requests, this week)" 并说明 Frequency=5 的换算依据（若采纳下面的频段映射表，23 次应映射为 Frequency 4 而非 5，此时 score = 4×4×4 = 64，仍 ≥40 保持 high）；或反过来将周报示例的 frequency: 23 改为 frequency: 50+（但 50+ 与 top_themes 里其他主题的个位数量级不协调）。推荐前者，并让两个示例共用同一组数字。

### 🟡 重要缺陷

**3. 补显式三必需节**（规范合规的核心动作）
- 在 Core Principle 之后新增 `## Workflow`（6 步管线：收集 → 分类 → 评分 → 决策 → 闭环 → 复盘，每步一行说明 + 指向正文对应章节的引用），将隐含管线显式化，同时为 agent 提供确定的执行起点。
- 在 Common Pitfalls 之后新增 `## Scope & Limitations`，至少声明三点：何时不使用（无真实反馈数据时不得编造主题/引文——与 CF-02 呼应；单条反馈不足以支撑产品决策）；不涵盖什么（本技能不执行问卷设计平台搭建、不代替用户访谈的现场执行）；数据前提（分析基于提供的反馈数据，不自行虚构渠道数据）。
- Synthesis & Reporting 节可改名为 `## Output Format — Weekly Feedback Summary`，直接满足 Output Format 必需节。
- 改动量约 30-40 行，对 466 行的 body 无压力，且能把合规评级直接拉到 10/10。

**4. 将频段表与 Frequency 分值显式绑定（行 161-173 与行 196）**
- 在 Priority Score Formula 后加一行映射：`Frequency: 50+ → 5, 20-49 → 4, 10-19 → 3, 5-9 → 2, <5 → 1`，并注明与 By Frequency 分档的对应关系；同时在 Act 决策树（行 248-258）补一句"10+ 次 = Frequency ≥ 3，需结合战略对齐与可交付性综合判断"，消解三处阈值的口径差。

### 🟢 优化建议

**5. 规范化 YAML 示例**（行 121-131、205-221、382-384 等处）
- 将 `Bug: Something broken` 类标量+嵌套结构改为合法 YAML（如 `Bug: { description: "Something broken", priority: ... }`），括号注释（`(12 mentions)`）移入注释 `#` 或改为 `count: 12` 字段；或在文件头注明"示例块为伪 YAML 结构，仅供阅读"。

**6. 收敛装饰符号**
- Common Pitfalls 与 Summary 的 ❌/✅ 前缀可删除，改为 "**Bad**: Collecting feedback without acting" 式纯文本，或保留但明确其为格式标记。此为风格选择，非必须。

**7. manifest.yaml 修订**
- domains 去掉 ai/frontend/security/testing/orchestration，收敛为 product/design/data；side_effects 移除 modifies_files 仅保留 creates_artifacts；preconditions 补充"反馈数据可用"；examples 补一条（如 `analyze Q2 support ticket export for top themes`）。

**8. SCORING.yaml 增强（可选）**
- 新增一条 script 检查防御 4.1 类回归，如 pattern `"score: (4[0-9]|5[0-9])|priority: high"` 类数值-标签一致性检查（pattern 设计需谨慎避免误伤）；PROC-02 的 pattern 扩为 `Strategic Alignment|Impact|Frequency`。

### 修复工作量估计

| 优先级 | 项 | 工作量 | 说明 |
|:---:|---|---|---|
| 🔴 | 修正 score 45 与频次口径 | ~10 分钟 | 两处数字替换 + 复核 |
| 🟡 | 补三必需节 + 频段映射 | ~40 分钟 | 30-40 行新增，无结构性风险 |
| 🟢 | YAML 规范化 / 符号收敛 / manifest / SCORING 增强 | ~1 小时 | 均为低风险润色 |

总计约 1.5-2 小时可由一次编辑会话完成；优先级上先做 🔴 两处（数值正确性 > 结构形式），再做 🟡 三节（合规评级跃升），最后视需要做 🟢 项。修复后该技能预计可评为 🟢A（88-92 分区间），有望列入 corpus 的"自包含知识型 process skill"范本。

---

## 附：与 Dossier 的一致性说明

Dossier（skill-dossier.md, 行 813-818）判定：逻辑一致（收集渠道、分类、优先级评分、闭环互相一致）、语法干净示例丰富、人机感产品敏锐语气、合规 Workflow/output/scope 存在、总评 🟢 完整实用。本 REVIEW 与 dossier 在语气、语法、人机感、内容完整性四个维度完全一致；唯一分歧在两点：(1) 合规维度 dossier 认为三节"存在"，本 REVIEW 细读后确认其以内容形式存在但无显式节名，按规范字面要求判为部分通过；(2) 逻辑维度本 REVIEW 发现 score 45/medium 标签矛盾与频次口径漂移两处 dossier 未记录的问题。结论：dossier 的 🟢 判断整体成立，但建议在修复第 13 节 🔴 两项后维持 🟢，否则按本 REVIEW 标准应为 🟡B 上沿（84/100）。
