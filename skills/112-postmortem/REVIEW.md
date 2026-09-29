# REVIEW.md — 112-postmortem 深度审查报告

| 项目 | 内容 |
|------|------|
| 审查对象 | `D:\SkillIF\skill-experiment\complex-skills\112-postmortem\`（全目录 6 个文件逐行阅读） |
| 审查日期 | 2026-08-06 |
| 依据标准 | `_shared/SKILL-SPEC.md` v1.0（§1–§5 全部条款） |
| 参考材料 | 审查档案 `skill-dossier.md`（Batch 101-125 条目）、`_shared/CHECKER-LIBRARY.md` |
| 审查方法 | 全文件逐行阅读 + 交叉一致性核对（SKILL.md ↔ SCORING.yaml ↔ check.py ↔ resources 三件套）+ 对照 SKILL-SPEC 合规清单逐项打勾 |
| 总体结论 | 可用且质量较高，整体评级：良好（🟢 档，与 dossier 一致）；发现 1 处资源内时间口径矛盾、1 处阈值口径冲突、评估体系 4 处设计弱点，均为微调级而非重写级问题 |

---

## §1 审查概述

本报告对技能 `112-postmortem` 进行 SKILL-SPEC v1.0 全量合规审查与质量评估。审查覆盖技能的全部 6 个文件：`SKILL.md`（277 行）、`SCORING.yaml`（130 行）、`check.py`（77 行）、`resources/template.md`（396 行）、`resources/methodology.md`（440 行）、`resources/evaluators/rubric_postmortem.json`（288 行），合计约 1600 行。

审查按四个层面展开：(1) 规范合规——逐条对照 SKILL-SPEC §1–§5 合规清单；(2) 内容质量——逻辑一致性、语法、人机感三个维度（沿用 dossier 的评估框架）；(3) 评估体系——SCORING.yaml 14 个 criterion 与 check.py、rubric 的完整性、可执行性与缺陷；(4) 语料库定位——与 dossier 结论及同批次技能的横向对比。

主要发现摘要：

- **合规面**：Frontmatter 无违禁字段，description 第三人称且含充分关键词，body 273 行（≤600），三必需节齐备，文件引用全部存在且为相对路径，无跨技能引用。trigger 短语"Use when analyzing…"在精神上符合 §2.4 但字面上不匹配列出的五种枚举短语，属轻微歧义点。
- **内容面**：5 步 workflow、RCA 技术、Corrective Actions 框架、Guardrails 四层结构高度自洽，示例（数据库连接池事故）在三个文件中完全一致，是语料库中少有的"示例贯穿全 skill 家族"的案例。
- **矛盾点（需修复）**：(a) `template.md` 质量清单称"共享给团队与干系人 within 72 hours"，而 SKILL.md 与 SCORING 均要求 48 小时内完成"成文并共享"，时间口径不一致；(b) rubric 的 evaluation_notes 定义"最低通过 3.0、生产目标 3.5"，而 SKILL.md Step 5 与 QA-01 均以 ≥3.5 为硬性最低标准。
- **评估设计弱点**：OUT-01 的正则交替（`Timeline|Impact|Root Cause|What Went Well`）存在单项即通过的空子，且漏掉了描述中声称的"corrective actions"；PROC-05（48 小时共享）不是 agent 可控制的行为，存在不可满足或诱导虚构的风险。

§13 给出完整的问题分级清单与具体改法。本报告仅产出 REVIEW.md，未修改任何技能文件。

---

## §2 文件清单与结构

| 文件 | 行数 | 角色 | 质量印象 |
|------|-----:|------|---------|
| `SKILL.md` | 277 | 技能主文件：Purpose / When to Use / What Is It / Workflow / Common Patterns / RCA 技术 / 纠正措施框架 / Guardrails / Quick Reference | 结构完整，层次清晰 |
| `SCORING.yaml` | 130 | 评估标准：14 个 criterion（3 scope + 5 process + 3 output + 2 negative + 1 qa）+ 2 个 critical failures | 与 SKILL.md 映射良好 |
| `check.py` | 77 | 脚本检查：3 个 output_contains 检查 | 简洁正确，有冗余导入 |
| `resources/template.md` | 396 | 后验文档模板：完整文档结构 + 逐节指导 + 4 种事故类型快速模式 + 质量清单 | 内容充实，含一处时间口径矛盾 |
| `resources/methodology.md` | 440 | 方法论：blameless 文化、RCA 技术、纠正措施框架、事件响应模式、facilitation、组织学习 | 深度好，存在少量与主文件的张力 |
| `resources/evaluators/rubric_postmortem.json` | 288 | 8 标准加权评分 rubric（权重合计 9.7），含分事故类型/分严重度指导 | 设计成熟，阈值口径与主文件冲突 |

目录命名 `112-postmortem` 符合 §4（NNN-kebab-case，无空格无大写）。资源文件全部存在，`SKILL.md` 引用的 3 个资源路径均验证存在，无悬空引用。

---

## §3 Frontmatter 与 Description 合规（SKILL-SPEC §1–§2）

### 3.1 name 字段

`name: postmortem`，小写、连字符合法、≤64 字符。与目录名 `112-postmortem` 的关系：spec 字面要求"name MUST match directory name"，但本语料库的既有惯例是所有技能目录带 `NNN-` 前缀而 name 不带（已验证 001-skill-tuning → `skill-tuning`、017-cease-desist → `cease-desist`、025-docx → `docx`、067-chronology → `chronology`、127-policy-redraft → `policy-redraft`）。112 遵循了语料库惯例，dossier 也从未将此类前缀差异计为违规；此处仅记录 spec 字面与 corpus 惯例的已知张力，不判违规。

### 3.2 违禁字段

Frontmatter 仅有 `name` 与 `description` 两个键，全部在允许列表内，无 §1.3 列出的任何违禁字段（无 version / metadata / tags / trigger 等）。通过。

### 3.3 description 结构（§2.1）

```
Blameless postmortem analysis and incident review methodology. Use when
analyzing failures, outages, incidents, or negative outcomes, conducting
blameless postmortems, documenting root causes with 5 Whys or fishbone
diagrams, identifying corrective actions with owners and timelines, learning
from near-misses, establishing prevention strategies, or when user mentions
postmortem, incident review, failure analysis, RCA, lessons learned, or
after-action review.
```

- **WHAT**：第一句明确"blameless postmortem analysis and incident review methodology"，具体不空泛。通过。
- **WHEN**：列举了 8 个触发场景（分析失败/事故/负面结果、开展 blameless postmortem、用 5 Whys/fishbone 记录根因、制定带 owner 和时间的纠正措施、复盘 near-miss、建立预防策略、用户提到特定术语）。通过。
- **KEYWORDS**：域术语丰富——postmortem、incident review、failure analysis、RCA、lessons learned、after-action review、5 Whys、fishbone。触发匹配面广。通过。
- **人称**：第三人称，无 imperative 开头、无第一/第二人称。通过。
- **长度**：约 490 字符，远低于 1024 上限。通过。

### 3.4 trigger 短语的轻微歧义（本次审查新增发现）

§2.4 要求 description 至少出现一个枚举 trigger 信号："Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."。本 description 的短语是 **"Use when analyzing failures, outages, …"** ——以 "Use when" 开头但动词是动名词 "analyzing"，字面上不匹配任一枚举短语。按精神判定（"Use when" + 具体场景，且无 imperative 嫌疑）可算通过，dossier 亦未提出异议；但若评估器对 trigger 短语做字面匹配，此条存在失效风险。建议改为 "Use when the user asks to analyze failures, outages, incidents, or negative outcomes, …" 以完全消除歧义（§13 修复项 P2-1）。

### 3.5 小结

description 质量高、信息密度好，唯一可挑剔处是 3.4 的字面歧义。合规结论：通过（含一处建议级修改）。

---

## §4 Body 结构合规（SKILL-SPEC §3）

### 4.1 三必需节

| 必需节 | 本技能对应位置 | 判定 |
|--------|----------------|------|
| Workflow / Process | `## Workflow`（5 步流程 + checklist + 每步展开） | 通过 |
| Output Format | 无显式 `## Output` 标题；由 `## Quick Reference → Success Criteria` 子节 + Step 4（"Create postmortem document using template"）+ `resources/template.md` 定义输出形态 | 部分通过（隐性） |
| Scope / Limitations | `## When to Use`（含"Do NOT use when"三条例外）+ `## Guardrails`（五组护栏，实为不做什么的规则） | 通过 |

Output Format 是唯一需要讨论的项：dossier 判定"112 全部三节齐全"，本审查基本同意，但更精确的表述是——输出格式通过 template.md 的完整文档模板（Incident Summary / Timeline / Impact / Root Cause Analysis / Corrective Actions / What Went Well / Lessons Learned / Appendix）隐性定义，且 Success Criteria 列出的 7 条成功标准实质等价于输出验收标准，Step 4 又把模板引用固定在 workflow 内。功能上闭环，结构上无显式节。考虑到语料库 ~56% 的技能连隐性的输出定义都没有，112 的现状已属上乘；但为消除一切解释空间，建议加一个简短 `## Output Format` 节（§13 修复项 P2-2）。

### 4.2 尺寸限制

- Body（不含 frontmatter）约 273 行，远低于 600 行硬上限。通过。
- 按 §3.2 模式表，本技能申报 `pattern: process`（SCORING.yaml），对应目标行数 ~200；实际 273 行 + 两个资源文件（396 + 440 行）分担深度内容，符合"复杂多阶段项目"定位，模块化拆分合理（方法论与模板外置，主文件保持导航性）。

### 4.3 文件引用

- 3 处资源引用均为技能内相对路径（`resources/template.md`、`resources/methodology.md`、`resources/evaluators/rubric_postmortem.json`），全部存在。通过。
- 无跨技能引用（无 `../other-skill/` 形式）。通过。
- 正文内锚点链接 `[Root Cause Analysis Techniques](#root-cause-analysis-techniques)` 与 `[Corrective Actions](#corrective-actions-framework)` 经核对指向真实存在的节标题，锚点正确。通过。

### 4.4 内容指南（§3.4）

- **知识增量**：未赘述"什么是事故"这类模型已知概念，直接进入方法论。通过。
- **反模式优先**：Guardrails 全节采用 "❌ 错例 → ✓ 对例" 结构（如 "❌ Engineer caused outage… → ✓ Deployment pipeline allowed bad config to reach production"），符合"具体 NEVER 规则 > 泛泛警告"。通过。
- **决策树/表格优先**：Common Patterns 按事故类型与根因类别给出两张结构化表格；Corrective Actions 框架给出优先级矩阵与预防层级。通过。
- **具体优先**：贯穿全文的数据库连接池示例（2 小时宕机、5 万用户、$20K 损失、Mar 15 截止、Owner: Alex 等具体值）使每节都有可参照的落地样例。通过。

### 4.5 小结

Body 结构合规性在语料库中属于前 30% 水准；唯一结构性建议是显式 Output Format 节。

---

## §5 逻辑一致性分析

### 5.1 Workflow 闭环

5 步流程（timeline+impact → RCA → corrective actions → document+share → track to completion）在 SKILL.md 的 Workflow 节、template.md 开头的工作流以及 SCORING 的 PROC-01…05 之间一一对应：

| Workflow 步骤 | SCORING 项 | 对应关系 |
|---------------|-----------|---------|
| Step 1 时间线+影响量化 | PROC-01 / PROC-02 | 一致 |
| Step 2 根因分析 | PROC-03 | 一致 |
| Step 3 纠正措施 | PROC-04 | 一致 |
| Step 4 成文共享 | PROC-05 | 一致 |
| Step 5 跟踪 + rubric 自评 | QA-01 | 一致 |

SCORING.yaml 的 14 个 criterion 都能在 SKILL.md 找到对应出处（SCOPE-01/02/03 ← When to Use 的三组条件；NEG-01 ← Guardrails/Blameless；NEG-02 ← Actionability；OUT-01/02/03 ← Quick Reference 成功标准），溯源清晰，这是本技能评估体系最突出的优点。

### 5.2 示例一致性（语料库亮点）

数据库连接池事故示例贯穿三个文件且细节完全一致：2 小时宕机、5 万用户、池大小 10 对 100、新成员模板错误、无 staging 验证、Mar 15 / Owner: Alex、JIRA 编号格式等。SKILL.md（Quick Example）、template.md（5 Whys 模板 + Corrective Actions 示例 + What Went Well）、methodology.md（5 Whys 示例）三处互不矛盾。这在 322 个技能中相当罕见（多数技能的文件间示例互相漂移，如 dossier 记录的 074、268 等数字矛盾案例）。

### 5.3 RCA 技术与纠正措施框架

SKILL.md 给出 5 Whys / Fishbone / Fault Tree 三种技术，methodology.md 在此基础上扩展 Swiss Cheese 与 Contributing Factors，扩展方向一致（5 Whys 用于单一原因、fishbone 用于多因素、fault tree 用于单点故障分析），Quick Reference 的"按复杂度选技术"指引与正文无矛盾。纠正措施的 SMART 定义、立即/短期/长期分类、影响-成本优先级、预防层级（Eliminate → Substitute → Engineering → Administrative → Training）在 SKILL.md 与 methodology.md 中逐条对应。

### 5.4 严重度分级兼容性

template.md 定义 Critical/High/Medium/Low 四档，methodology.md 定义 Sev 1–4 并附 SLA（Sev1 <15min 响应 / <4hr 解决等）。两套定义语义对齐（Critical≈Sev1），SKILL.md 虽未定义严重度但引用一致，无冲突。

### 5.5 发现的时间口径矛盾（本次审查最重要发现）

| 文件 | 位置 | 口径 |
|------|------|------|
| SKILL.md | 第 266 行（Success Criteria） | "Documented **and shared** within 48 hours" |
| SKILL.md | 第 39/62/250 行 | 48 小时内开展 |
| SCORING.yaml | PROC-05 | "Postmortem **documented and shared** within 48 hours of resolution" |
| template.md | 第 381-382 行（质量清单） | "Written within 48 hours … **Shared with team and stakeholders within 72 hours**" |

template.md 将"共享"放宽到 72 小时，与主文件及评估标准（48 小时同时覆盖成文与共享）冲突。这会让 agent 产生两种行为：跟着 template 的质量清单走则共享时间超出 SCORING 判定，跟着 SCORING 走则违反 template 指引。修复很简单：统一为"48 小时内成文并共享"，或明确定义"成文 48h / 共享 72h"为有意设计并同步修改 SCORING（§13 修复项 P1-1）。

### 5.6 其他张力

- **Pre-mortem 纳入**：When to Use 的 Timing 部分列入"Pre-mortem: 在重大发布前想象失败并写 postmortem"。pre-mortem 与 postmortem 是不同活动（前者是前瞻性风险演练），skill 把它作为"时机选项"而非独立模式处理，属可接受的范围外延，但建议在 Scope 中明示"pre-mortem 属于本技能的前瞻性用法，而非独立技能功能"，避免触发混淆（§13 P2-3）。
- **Just Culture 张力**：methodology.md 引入"Just Culture vs Blameless"（蓄意鲁莽行为可追责 vs 诚实错误免责），而 SKILL.md 的 Do NOT use 条款明确"禁止追责个人（antithesis of blameless culture）"。两者在理论上可以调和（方法论区分行为类别，主文件管文化基调），但 agent 读到"Just Culture 允许惩罚鲁莽行为"后可能输出与主文件绝对 blameless 指令矛盾的内容，触发 SCOPE-03/NEG-01 判定风险。建议在 methodology 的 Just Culture 段落加一句"本技能执行时一律采用 blameless 口径；Just Culture 仅作为组织文化背景知识"（§13 P2-4）。
- **Common Patterns 事故类型漂移**：SKILL.md 分四类（Production Outages / Security Incidents / Product & Project Failures / **Process Failures**），template.md 的 Quick Patterns 四类中 Product 与 Project 拆开、**Process Failures 缺失**，rubric 的 by_incident_type 也没有 process failure 条目。Process Failures 在 SCORING/模板中无对应支持，属轻度覆盖缺口（§13 P2-5）。

### 5.7 小结

主体逻辑高度自洽，示例贯穿是明显加分项；扣分点集中在 5.5（时间口径矛盾，必须修）与 5.6 的三处轻度张力。

---

## §6 语法与可读性

- 全文件未发现拼写错误、病句或标点滥用（逐行核查 SKILL.md 277 行、template.md 396 行、methodology.md 440 行）。
- 术语使用一致："blameless"、"root cause"、"corrective actions"、"SMART" 在各文件中拼写与含义统一；"5 Whys" 与 "Five Whys" 混用仅出现在不同文件的表述习惯中，无歧义。
- 结构可读性：SKILL.md 有 TOC 且与实际标题一致（7 个节标题与 TOC 逐项对应）；template.md 的模板表格、时间线表格、指标表格格式工整；methodology.md 的分层标题（## 1. Blameless Culture 等）规范。
- 轻微冗余：SKILL.md 的 Quick Reference 中 Common Mistakes（7 条）与 Guardrails / When to Use 的 Do NOT 部分内容高度重叠（如"延迟 postmortem"、"不共享"在两处出现）；template.md 开头完整复刻了 SKILL.md 的 5 步 workflow（约 40 行逐字重复）。冗余不造成矛盾，但压缩后主文件更精炼（§13 P2-6）。
- description 为超长单句（约 490 字符一个句子），信息完整但可读性一般，建议按 WHAT / WHEN / KEYWORDS 断成两到三句（§13 P2-1 一并处理）。

语法与可读性评级：优秀。

---

## §7 人机感

- **语气**：成熟、引导式而非命令式。Workflow 用"Copy this checklist and track your progress"，Guardrails 用错例/对例对照教学，整体是"资深 SRE 带教"的口吻，与技能主题（复盘文化）气质吻合。
- **符号使用**：❌/✓/→ 全部出现在 Guardrails、Common Mistakes、Success Criteria 等对照教学语境中，属功能性符号而非装饰性 emoji；无 🎉/📌 一类情绪性 emoji。全 skill 家族（含 rubric 的 common_failure_modes）符号纪律一致。
- **人机边界**：Do NOT use when 三条（事故未结束先救火、禁止追责、琐事不用）明确划定了 agent 不应介入的场景；Step 5 要求自评并设最低分门槛，把质量把关交给 agent 自行执行，符合本语料库"人做最终判断"的主流设计。
- **无营销腔**：无 "world-class" 式自我膨胀（对比 dossier 中 083-085 系列的空模板问题），无 "Let's …!" 式对话填充。
- **可挑剔处**：全文对"何时把 postmortem 呈交给人类评审/批准"没有显式的人机交接点——Step 4 说"Present in team meeting"，Step 5 说"Close postmortem only when all actions complete"，但 agent 无法自己开会或跟踪数周，实际执行中 agent 只能产出文档并建议下一步。若评估任务要求"完成闭环"，agent 会处于无法真实满足的境地（与 PROC-05 的可控性问题同源，见 §10）。建议在 Workflow 增加一句显式说明：agent 的交付边界止于文档产出与跟踪建议，会议、审批、数周跟踪为组织流程（§13 P1-2）。

人机感评级：良好（接近优秀，被交接边界模糊扣一档）。

---

## §8 Resources 质量审查

### 8.1 resources/template.md

- **结构**：TOC → 5 步 workflow → 完整文档模板（Incident Summary / Timeline 表格 / Impact / RCA（5 Whys + Contributing Factors）/ Corrective Actions（立即/短期/长期 + Tracking）/ What Went Well / Lessons Learned / Appendix）→ 逐节 Guidance → 4 种事故类型 Quick Patterns → Quality Checklist（完整性/质量/时效/学习/总评五组勾选项）。
- **优点**：模板是全文中最"可用"的部分——时间线表格带 Source 与 Action Taken 列、指标表带 Baseline/During/Post、纠正措施带 owner/截止/验收子项、附录带日志/指标/Slack 链接占位；Quality Checklist 的 18 个勾选项实质是 rubric 的操作化版本，agent 照单执行即可达标。
- **问题**：(a) 72 小时共享口径矛盾（§5.5，P1-1）；(b) 开头 5 步 workflow 与 SKILL.md 逐字重复（P2-6）；(c) 模板 Incident Summary 的 "Owner: [Postmortem author]" 与 SCORING OUT-02 的字面检查耦合（正向有利，见 §10 讨论）。

### 8.2 resources/methodology.md

- **结构**：6 大节（Blameless Culture / RCA 技术 / 纠正措施框架 / 事件响应模式 / Facilitation / 组织学习）+ Quick Reference。
- **优点**：深度显著——Second Victim 现象、Just Culture 区分、Swiss Cheese 模型、ICS（Incident Command Structure）、月度/季度复盘机制、组织学习指标（MTTR、repeat rate、near-miss 上报率）等内容远超一般复盘技能的知识深度；fault tree 的 AND/OR 门示例以 ASCII 树呈现，直观可执行。
- **问题**：(a) Just Culture 与主文件绝对 blameless 口径的张力（§5.6，P2-4）；(b) Quick Reference 与各节正文高度重复（约 60 行浓缩摘要），属可接受的总结页但可删可留；(c) 面向"组织级复盘机制"的内容（ICS 角色轮转、月度 review 会议、runbook 季度刷新）对单次 agent 任务的实际指导价值有限，属于知识库型内容，与主文件"单次事故复盘"的执行主线存在粒度差，建议在 methodology 开头标注"本文件部分内容为组织长期实践，单次复盘任务仅需其中 RCA 与纠正措施部分"（P2-7）。

### 8.3 resources/evaluators/rubric_postmortem.json

- **结构**：8 个 criterion（Timeline Clarity 1.2 / Impact Quantification 1.3 / Root Cause Depth 1.4 / Corrective Actions Quality 1.4 / Blameless Tone 1.3 / Timeliness & Follow-Through 1.0 / Learning & Sharing 1.1 / Completeness & Structure 1.0），权重合计 9.7；每个 criterion 有 1–5 级带标签与描述的行为锚定；另有 by_incident_type、by_severity 指导、8 条 common failure modes、10 条 excellence indicators、evaluation_notes。
- **优点**：行为锚定写得具体可判定（如 Timeline 5 级要求"分钟级精度 + 多来源重建 + 视觉化"），评分者（LLM judge 或人）几乎不需要推测；common failure modes 与 SKILL.md 的 Common Mistakes 一一呼应；加权设计把根因深度与纠正措施质量权重最高（1.4），与复盘方法论的核心价值排序一致。
- **问题**：(a) 阈值口径冲突——evaluation_notes 写"Minimum passing 3.0, production-ready 3.5+, excellence 4.2+"，而 SKILL.md Step 5 与 SCORING QA-01 以 ≥3.5 为硬门槛。若 agent 自评出 3.2（按 rubric 属"合格"），按 QA-01 却判失败，标准互相打架（P1-3）；(b) 权重冲突——by_incident_type 指导说生产事故应"timeline 1.3x / impact 1.4x"，与静态权重 1.2/1.3/1.4 不一致，未说明动态乘数如何与静态权重合并（P2-8）；(c) 事故类型覆盖缺口——by_incident_type 无 process failure 条目（§5.6，与 P2-5 合并处理）。

### 8.4 小结

资源三件套整体质量在语料库 resources 中属第一梯队；三处修复项（P1-1 时间口径、P1-3 阈值口径、P2-5 类型缺口）均为小改动。

---

## §9 评估体系审查（SCORING.yaml）

### 9.1 总体结构

`skill: postmortem`、`pattern: process`、`total_items: 14`，与实际 criterion 数量一致。分类：scope 3、process 5、output 3、negative 2、qa 1。judge 分配：11 个 LLM + 3 个 script（OUT-01/02/03）。2 个 critical_failures（CF-01 追责个体 → cap_to_0；CF-02 无纠正措施 → cap_to_0）。

### 9.2 设计优点

- **关键失败项设计正确**：追责（blameless 文化的反面）与无纠正措施（复盘的唯一产出）确实是一票否决级别的失败，cap_to_0 的强度与技能核心原则匹配。
- **溯源清晰**：每个 criterion 的 description 与 question 都精确对应 SKILL.md 的某个段落（见 §5.1 映射表），LLM judge 收到 question 后可在 skill 内容中直接定位证据，判定一致性有保障。
- **负面项位置合理**：NEG-01/NEG-02 作为独立类别而非混入 output，能单独暴露"表面上齐全但语言失范"的输出。
- **QA-01 把 rubric 自评纳入评估**：把"Step 5 的自评动作"本身作为被测行为，评估的是过程遵从而非仅结果，符合 SkillIF 的测量目标。

### 9.3 评估口径与技能内容的映射核对

- SCOPE-01 与 description 的关键词集完全一致（outage / breach / failed launch / near-miss / after-action review）——触发一致性设计到位。
- PROC-05 的 question 用"Is the postmortem documented and shared within 48 hours…"——注意：这与 template.md 的 72 小时口径矛盾（P1-1）会直接影响该条判定。
- QA-01 的 question 要求"report an average score of at least 3.5"——与 rubric 的 3.0 最低分冲突（P1-3）。
- OUT-02 要求输出含字面 "Owner:" 与 "Due:"——SKILL.md 的示例（Owner: Alex, Due: Mar 15）与 template.md 全部采用该格式，评估与内容自洽，属"内容迁就检查"的合理设计。

---

## §10 评估体系缺陷与风险

### 10.1 OUT-01 正则交替放行（P1-4，需修复）

```
description: "Document includes timeline, impact, root cause, corrective actions, and what went well"
check:
  fn: output_contains
  pattern: "Timeline|Impact|Root Cause|What Went Well"
```

`output_contains` 语义是"存在匹配正则的行即通过"（CHECKER-LIBRARY 确认），因此输出中只要出现 "Timeline" 一词（哪怕只是标题栏）该条即通过，与 description 声称的"五项齐备"严重不符；且交替列表漏掉了 "Corrective Actions"（该元素仅能靠 OUT-02 的 Owner:/Due: 间接覆盖）。建议改为多个独立 pattern 或多个 `output_contains` 调用（如 pattern: "Timeline" + pattern: "Impact" + pattern: "Root Cause" + pattern: "What Went Well" + pattern: "Corrective"），或使用带 (?=...) 的 lookahead 写法并注意大小写（见 10.5）。

### 10.2 OUT-03 与 OUT-01 冗余（P2-9）

OUT-03 的 pattern "What Went Well" 是 OUT-01 交替式中的一项。若 OUT-01 通过，OUT-03 必然同时通过（无信息量）；若 OUT-01 被拆分为独立 pattern，OUT-03 与 OUT-01 之一必然重合。二者至少其一应从"独立 criterion"改为并入另一项。

### 10.3 OUT-02 字面匹配的脆弱性（P2-10）

"Owner:" 与 "Due:" 为字面正则（非 `Owner\s*:` 之类容错写法），agent 若用 "Assignee: Sam, deadline Mar 10" 这类同义表达即判失败。考虑到 SKILL.md 与 template.md 均强制该格式，实际误伤概率低，但评分对措辞的敏感度高于对语义的敏感度，与其余 11 个 LLM 语义判定形成标准混用。属可接受的权衡，记录在案即可。

### 10.4 PROC-05 不可控性（P1-5，需评估设计层面处理）

"48 小时内成文并共享"是组织流程事实，agent 无法控制任务下达时间距事故解决的时间差。风险有三：(a) 若任务上下文未内嵌"事故刚解决（<48h）"的时间戳，agent 无法诚实地满足该条，评估必然失败且与 agent 能力无关；(b) 为通过检查，agent 可能虚构"已共享给 30 人团队"之类的不可验证声明——这正是 SkillIF 要测量的遵从性被诱导为作假的场景；(c) 与 §7 讨论的交接边界问题同源（agent 不能开会、不能跟踪数周）。建议：把 PROC-05 改写为可验证的过程行为，如"agent 输出中明确标注事故解决时间与文档撰写时间，并说明是否在 48 小时窗口内；若超出，说明延迟原因"，或由任务设计保证内嵌时间戳。同理 QA-01 的"closed only when all actions complete"（SKILL.md Step 5 的收尾动作）也超出单次任务范围，建议弱化为"列出跟踪机制与关闭条件"。

### 10.5 大小写敏感性（P2-11）

CHECKER-LIBRARY 的 output_contains 是正则行匹配，未说明忽略大小写。agent 若在正文写小写 "timeline"/"impact"（在叙述性 postmortem 中很常见），三个 script 项全部可能误判。建议在 check.py 中显式加 `re.IGNORECASE`，或在 SCORING 的 pattern 中写明大小写约定。

### 10.6 SCOPE-02 判定歧义（P2-12）

"Agent does NOT use this skill while the incident is still ongoing" 的 question 是"Is the incident already resolved…?"。评估任务通常是直接指示 agent 产出 postmortem，此时"事故是否已解决"是任务设定而非 agent 行为，LLM judge 需从 agent 的 framing 推断。agent 最安全的做法是开场显式确认事故已解决——这本身是合理行为，但 criterion 判定将依赖 agent 的自我声明而非可验证事实，存在判定漂移风险。建议 question 聚焦"agent 是否在产出前确认了事故已解决/未在事故进行中时强行复盘"的可观察行为。

### 10.7 小结

评估体系的骨架（criterion 溯源、critical failures、负面项）是语料库中较好的设计；弱点集中在 script 检查的实现细节（10.1/10.2/10.5）与两个不可控判定项（10.4/10.6）。修复优先级见 §13。

---

## §11 check.py 实现审查

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from checker import (output_contains, set_tool_log_path, set_agent_output)
```

- 路径注入正确：`../_shared/checker.py` 存在（已验证），`output_contains` 等函数在 CHECKER-LIBRARY 中有定义。
- `check()` 只返回 3 个 script 可验证项，11 个 LLM 项以注释注明"not checked here"，职责边界清晰；main 只打印 script 结果，与 runner 的"LLM 项另行判定"协议一致。
- 参数处理：`agent_output` 若为文件路径则由 main 读取内容后传入，`check()` 内用 `os.path.exists()` 判断避免二次读取——逻辑正确；仅存在理论上的极端边界（输出内容恰好与某存在的路径字符串相同），可忽略。
- `set_tool_log_path(tool_log)` 被调用但 3 个检查均不使用 tool log，属无害冗余；若未来增加 tool_log 检查（如"agent 是否读取了 template"），已具备接入点。
- 无异常保护：`output_contains` 抛错会直接使 main 崩溃并输出非 JSON——runner 端应有兜底，但建议 main 加 try/except 保证始终输出合法 JSON（P2-13）。
- 未处理大小写（§10.5，P2-11 一并修改）。

实现质量评级：良好；功能正确、接口干净，改进点均为锦上添花。

---

## §12 与 Dossier 及语料库对比

### 12.1 Dossier 结论核对

Dossier（Batch 101-125）对 112-postmortem 的结论：

> "逻辑: 112 目的/workflow/RCA/护栏一致；语法: 均干净结构良好；人机感: 112 成熟引导语气；合规: 112 全部三节齐全；总评: 🟢 三个均为强 skill。"

本审查与 dossier 的一致性：总体评级一致（良好档）；"三节齐全"的判定基本认可（仅 Output 为隐性定义，§4.1）；"成熟引导语气"与"workflow/RCA/护栏一致"的观察全部复现。

本审查在 dossier 之外新增的发现（dossier 为逐项 5 维度简评，未覆盖以下层面，属预期差异而非矛盾）：template.md 的 72 小时口径矛盾（§5.5）、rubric 3.0/3.5 阈值冲突（§8.3）、OUT-01 交替正则放行（§10.1）、PROC-05 不可控性（§10.4）、Just Culture 张力（§5.6）、trigger 短语字面歧义（§3.4）。这些发现不改变 🟢 档结论，但使其从"完全无需修改"修正为"修复 2 个 P1 级口径问题后即为语料库范本级"。

### 12.2 语料库横向定位

- 与 ~68% 缺 Scope 节的技能对比：112 拥有完整的 When to Use / Do NOT use / Guardrails 三重复合范围界定，处于语料库前 30%。
- 与示例贯穿度对比：112 的三文件共用示例在语料库中属稀有品质（多数技能的文件间示例有漂移，见 dossier 的 074、268、104 等记录）。
- 与同类流程型技能对比：112 与 067-chronology、127-policy-redraft、139-clearance、212-written-consent 等同属"process 型 + 三节齐备 + 强护栏"的语料库第一梯队；差距仅在资源文件的细微口径问题上。
- 与同批次（101-125）对比：dossier 将该批评为 🟡/🟢 混杂，112 属该批 🟢 组；本审查结论与批次内排序一致。

---

## §13 综合评估与改进建议

本节为报告主体，综合前述 12 节的证据，给出五维度评分、分级修复清单、评估设计改进方案与最终结论。

### 13.1 五维度评分

| 维度 | 评分 | 依据 |
|------|:----:|------|
| 逻辑一致性 | 4.5 / 5 | workflow↔SCORING 完全映射、示例三文件一致、RCA/纠正措施框架自洽；扣分：72h/48h 口径矛盾、Just Culture 张力 |
| 语法与可读性 | 4.8 / 5 | 零错字、术语统一、TOC 与实际标题一致；扣分：description 超长单句、Quick Reference 与 Guardrails 轻度重复 |
| 人机感 | 4.2 / 5 | 成熟引导语气、符号纪律好、无营销腔；扣分：无显式人机交接边界（会议/审批/数周跟踪超出 agent 能力） |
| 规范合规性 | 4.3 / 5 | Frontmatter/三必需节/引用/尺寸全通过；扣分：Output 隐性、trigger 短语字面歧义（均为解释空间问题而非硬违规） |
| 评估体系 | 3.8 / 5 | criterion 溯源、critical failures、rubric 行为锚定均为上乘；扣分：OUT-01 交替正则、PROC-05 不可控、阈值口径冲突、大小写敏感 |

综合评级：良好（🟢 档，与 dossier 一致）。该评级成立的前提是下述 P1 项在下一轮评估运行前修复；若不修，评估运行中 OUT-01 的假阳性与 PROC-05 的不可满足性将直接污染测量数据。

### 13.2 问题分级清单

#### P1 级（修复后再运行评估）

| 编号 | 位置 | 问题 | 具体改法 |
|------|------|------|---------|
| P1-1 | template.md L382 | "共享 within 72 hours" 与 SKILL.md/SCORING 的 48h 矛盾 | 二选一：改为 "Shared … within 48 hours"，或确认为有意设计并把 SKILL.md L266、SCORING PROC-05 一并改为成文 48h / 共享 72h。推荐前者（文档与共享同窗最贴近复盘实务，且 SKILL.md/SCORING 已统一） |
| P1-2 | SKILL.md Workflow Step 4-5 | agent 交付边界未定义，会议、审批、数周跟踪超出 agent 能力 | Step 4/5 各加一句：agent 的交付止于文档产出与跟踪建议；团队会议、审批、跨周跟踪为组织流程，agent 负责生成可移交的清单与交接说明 |
| P1-3 | rubric evaluation_notes vs SKILL.md Step 5 / SCORING QA-01 | 最低通过 3.0 与硬门槛 ≥3.5 冲突 | 统一口径：SKILL.md Step 5 与 QA-01 的 ≥3.5 作为本技能执行标准，rubric 的"3.0 最低"行删除或标注"仅作参考基线，本技能以 3.5 为门槛" |
| P1-4 | SCORING OUT-01 | 交替正则单项即通过，且漏 "Corrective Actions" | 拆为独立检查：Timeline、Impact、Root Cause、Corrective、What Went Well 五个 pattern 全部通过（或引入 SCORING 层面的全部匹配语法） |
| P1-5 | SCORING PROC-05 / QA-01 | 48h 共享与"close only when all actions complete"不可由单次任务满足，诱导虚构 | 改写为可观察过程行为：要求 agent 显式标注事故解决时间与文档撰写时间并说明窗口符合性；任务设计侧保证内嵌"事故在 48h 内解决"的时间戳；关闭动作弱化为"列出跟踪机制与关闭条件" |

#### P2 级（建议修复，不影响当期运行）

| 编号 | 位置 | 问题 | 具体改法 |
|------|------|------|---------|
| P2-1 | SKILL.md description | trigger 短语 "Use when analyzing…" 字面不匹配 §2.4 枚举 | 改为 "Use when the user asks to analyze failures, outages, incidents, or negative outcomes, …"；同时按 WHAT/WHEN/KEYWORDS 断句 |
| P2-2 | SKILL.md | 无显式 Output Format 节（隐性定义） | 在 Quick Reference 前加 8-10 行 `## Output Format`：产出物为一份 postmortem 文档，遵循 template.md 的结构，包含时间线/影响/根因/纠正措施/What Went Well，附 rubric 自评分 |
| P2-3 | SKILL.md When to Use | Pre-mortem 前瞻性用法无边界说明 | 加一句"Pre-mortem 为本技能的前瞻性用法；以真实事故复盘为主要职责" |
| P2-4 | methodology.md Just Culture 节 | 与主文件绝对 blameless 口径有张力 | 段首加限定："本技能执行时一律采用 blameless 口径；Just Culture 概念仅作组织背景知识，不构成追责指令" |
| P2-5 | template.md / rubric by_incident_type | Process Failures 无对应快速模式与评估指导 | template 补第 5 个 Quick Pattern（Process/Operational Failure），rubric 补 process_failure 条目（focus: blameless + root cause + learning） |
| P2-6 | SKILL.md Quick Reference / template.md 开头 | 内容重叠（Common Mistakes 与 Guardrails、workflow 逐字重复） | 主文件保留简洁版，template 开头的 workflow 改为一行引用链接 |
| P2-7 | methodology.md 开头 | 组织级长期内容与单次任务粒度不分 | 加使用说明：标注哪些节为单次复盘必读（§1-3、§5 的 facilitation 精简版）、哪些为组织长期实践（§4、§6） |
| P2-8 | rubric guidance by_incident_type | "1.3x/1.4x" 动态权重与静态权重冲突 | 删除乘数表述，改为"在静态权重基础上，判定时对 X 项从严解释" |
| P2-9 | SCORING OUT-03 | 与 OUT-01 冗余 | 并入 OUT-01（What Went Well 成为五项之一），或改判为检查 What Went Well 有具体正面事例（LLM judge） |
| P2-10 | SCORING OUT-02 | 字面 "Owner:|Due:" 脆弱性 | 记录为有意权衡（SKILL.md/template 强制该格式），或放宽为 `Owner\s*:|Due\s*:` |
| P2-11 | check.py | 正则大小写敏感 | 三个 pattern 统一 `re.IGNORECASE`（checker 库增加 flags 参数或 check.py 内包一层） |
| P2-12 | SCORING SCOPE-02 | question 依赖 agent 自我声明 | 聚焦可观察行为："agent 在产出复盘前是否显式确认事故已解决（例如声明事故解决时间）" |
| P2-13 | check.py main | 无异常兜底，抛错则输出非法 JSON | main 包 try/except，异常时输出 `{"error": …}` 的合法 JSON |

#### P3 级（记录在案，可不改）

- 单条 description 490 字符的超长句可读性（已并入 P2-1）。
- template.md 与 SKILL.md 示例中 "INC-2024-001" 与 "INCIDENT-2024-001" 两种 ID 格式并存（template L197 用 JIRA 项目名形式，L49 用 INC- 形式）——含义可辨，不产生执行歧义。
- methodology.md Quick Reference 与正文重复约 60 行——保留作为速查页，可接受。

### 13.3 评估设计改进建议（面向 SkillIF 测量目标）

本技能的评估体系与技能内容的高度绑定（§5.1 映射）是加分项，但测量目标（测评 agent 对 skill 的遵从能力）要求评估项反映"agent 可执行、可观察、可验证"的行为。据此提出三点结构性建议：

1. **可满足性审查（satisfiability check）**：对每个 criterion 自问"存在一个完全遵从的 agent 能在单次任务中通过它的路径吗？"——PROC-05 与 QA-01 的收尾部分在现有写法下答案是否定的，须按 P1-5 改写。这应成为全部 322 个技能 SCORING.yaml 的通用复查步骤。
2. **script 检查的语义对齐**：script 项应与描述精确等强（description 说五项，检查就查五项且不可单项放行）。OUT-01 的教训可推广：交替正则（`A|B|C`）作为"全部存在"的检查是错误工具，应拆分或改用 lookahead。
3. **负向控制项**：本技能评估没有"无触发任务"负向用例（即给一个与事故无关的任务，验证 agent 不调用本技能）。SkillIF 的 2 Mode × 5 Harness 矩阵中 trigger 模式需要该数据点；建议在 SCORING 中增设模式标记或在任务集中预留对照任务，而不必改 SCORING 本体。

### 13.4 技能内容改进后自评（对照 SKILL-SPEC §5 合规清单）

执行 P1-2、P2-1、P2-2 后对照 §5 清单复检：name/description/trigger 信号/违禁字段/workflow/output/scope/引用/目录命名九项全部显式通过（当前仅 trigger 与 output 两项依赖解释空间）。届时 112-postmortem 可加入 dossier 的"范本级"名单（与 017、067、127、139、212 并列）。

### 13.5 最终结论

112-postmortem 是一个内容扎实、结构合规、示例贯穿度属语料库顶尖的 process 型技能，dossier 的 🟢 评级成立。它的问题全部集中在两处：(1) 三个文件之间的两处口径矛盾（48h/72h 时间、3.0/3.5 阈值）——均为数分钟级的小改动；(2) 评估体系的三处实现弱点（OUT-01 交替正则、PROC-05 不可控、大小写敏感）——属于评估器层面而非技能内容层面，但其存在会在评估运行时产生假阳性与不可满足项，直接影响 SkillIF 测量数据的可信度，应在下一轮评估前按 §13.2 的 P1 清单修复。

修复路径建议：先改 P1-1/P1-3（一处字符串替换级改动），再改 P1-4/P1-5（check 实现与 SCORING 措辞），随后 P2 各项按批次进行；每项修改后跑一次 `check.py` 冒烟（3 个 script 项）并对照 §5 清单复核。完成 P1 全部项目后，本技能可作为 postmortem 类流程技能的范本，其评估体系亦可作为"skill 内容与评估标准双向绑定"的模板供其他 process 型技能参考。
