# REVIEW.md — 113-prioritization-effort-impact 深度审查报告

| 项目 | 内容 |
|------|------|
| 审查对象 | `D:\SkillIF\skill-experiment\complex-skills\113-prioritization-effort-impact\`（全目录 6 个文件逐行阅读，合计 1637 行） |
| 审查日期 | 2026-08-06 |
| 依据标准 | `_shared/SKILL-SPEC.md` v1.0（§1–§5 全部条款） |
| 参考材料 | 审查档案 `skill-dossier.md`（Batch 101-125 条目）、`_shared/CHECKER-LIBRARY.md`、对照集 `complex-skills-no-trigger/113-prioritization-effort-impact/` |
| 审查方法 | 全文件逐行阅读 + 交叉一致性核对（SKILL.md ↔ SCORING.yaml ↔ check.py ↔ resources 四件套）+ 全部示例算术复算 + 对照 SKILL-SPEC 合规清单逐项打勾 + 与主集/对照集 body 逐字节 diff |
| 总体结论 | 可用且质量较高，整体评级：良好（🟢 档，与 dossier 一致）；发现 1 处教学示例算术错误、1 处象限边界口径未定义、1 处典型分布百分比不封闭、评估体系 5 处设计弱点，以及 1 处对照集（no-trigger）description 损坏——均为微调级而非重写级问题 |

---

## §1 审查概述

本报告对技能 `113-prioritization-effort-impact` 进行 SKILL-SPEC v1.0 全量合规审查与质量评估。审查覆盖技能的全部 6 个文件：`SKILL.md`（218 行）、`SCORING.yaml`（122 行）、`check.py`（75 行）、`resources/template.md`（374 行）、`resources/methodology.md`（488 行）、`resources/evaluators/rubric_prioritization_effort_impact.json`（360 行），合计 1637 行。

审查按五个层面展开：(1) 规范合规——逐条对照 SKILL-SPEC §1–§5 合规清单；(2) 内容质量——逻辑一致性、语法、人机感三个维度（沿用 dossier 的评估框架），并对全部教学示例（RICE / ICE / CD3 / Opportunity / 加权评分 / 复合评分）逐项复算算术；(3) 评估体系——SCORING.yaml 13 个 criterion 与 check.py、rubric 的完整性、可执行性与缺陷；(4) 语料库定位——与 dossier 结论、同批次技能（重点对比 112-postmortem）的横向比较；(5) 对照集核查——对 `complex-skills-no-trigger/` 下对应技能做 body diff 与 description 质量检查。

主要发现摘要：

- **合规面**：Frontmatter 仅 `name` + `description` 两键，无违禁字段；description 第三人称、WHAT/WHEN/KEYWORDS 齐备、约 500 字符（≤1024）；body 214 行（≤600）；3 处资源引用全部存在且为技能内相对路径；无跨技能引用；目录命名合规。三必需节中 Workflow 显式齐全，Output 与 Scope 均为隐性定义（Success Criteria + template.md 承担输出定义，"When to use alternatives" 承担部分边界），属解释空间问题而非硬违规。
- **内容面**：2x2 矩阵象限表、示例表、template.md 的 ASCII 矩阵三处几何一致；CSV export 示例（2 天 / 低工作量）贯穿 SKILL.md、template.md 与 rubric 三个文件且细节一致；RICE/ICE/CD3/Opportunity 示例算术全部复算正确。
- **硬伤（需修复）**：(a) `methodology.md` 加权评分示例中 Feature B 的总分显示 3.0，但各行加权和 0.8+1.2+1.0+0.4 = **3.4**，教学示例出现算术错误；(b) 象限"高/低"边界在三个文件中均无统一定义，且 SKILL.md 自带示例把 Impact=3.0（自评 "Medium-High"）判为 Quick Win，与 rubric 建议的 ">3.5 = high" 边界冲突；(c) 典型象限分布 10-20% + 20-30% + 40-50% + 10-20% = **80-120%**，非封闭分布。
- **评估设计弱点**：SCORING.yaml 13 项全部为 LLM judge、0 项 script 检查（check.py 恒返回空 dict），与语料库 36.1% script 占比的均值形成极端对比；NEG-01 在单次任务中不可满足，存在诱导 agent 编造利益相关者输入的风险；PROC-01 硬编码 1-5 刻度与技能自身允许的 1-10 扩宽刻度冲突。
- **对照集发现（跨批次共性）**：`complex-skills-no-trigger/113-prioritization-effort-impact/SKILL.md` 的 description 被触发切除管线改成了 **"5. [Common Patterns](#common-patterns)"**——提取了正文 TOC 锚点作为替代描述，description 完全不再描述技能。body 与主集逐字节一致（diff 无输出），故唯一差异正是这条损坏的描述。这会污染 Mode B 对照组：观测到的遵从度差异将混入"描述损坏"而非纯"无 trigger"变量。

§13 给出完整的问题分级清单与具体改法。本报告仅产出 REVIEW.md，未修改任何技能文件。

---

## §2 文件清单与结构

| 文件 | 行数 | 角色 | 质量印象 |
|------|-----:|------|---------|
| `SKILL.md` | 218 | 技能主文件：Purpose / When to Use / What Is It / Workflow / Common Patterns / Scoring Frameworks / Guardrails / Quick Reference | 结构完整，层次清晰 |
| `SCORING.yaml` | 122 | 评估标准：13 个 criterion（3 scope + 4 process + 3 output + 2 negative + 1 qa）+ 2 个 critical failures | 与 SKILL.md 映射良好，但 100% LLM judge |
| `check.py` | 75 | 脚本检查：0 个 script 可验证项，恒返回空 dict | 可运行但实质为空壳，含死代码 |
| `resources/template.md` | 374 | 交付模板：矩阵 ASCII 图 + 评分表 + 路线图 + 逐节指导 + 快速模式 + 质量清单 | 内容充实，量表与主文件存在漂移 |
| `resources/methodology.md` | 488 | 方法论：RICE/ICE/加权/Kano/CD3/Opportunity + 利益相关者技术 + 数据驱动 + 路线图优化 + 10 陷阱 | 深度好，含 1 处算术错误 |
| `resources/evaluators/rubric_prioritization_effort_impact.json` | 360 | 8 标准加权评分 rubric（权重合计 9.6），含分场景/分团队/分时间窗指导 | 行为锚定具体，缺阈值与归一化说明 |

目录命名 `113-prioritization-effort-impact` 符合 §4（NNN-kebab-case，无空格无大写）。资源文件全部存在，`SKILL.md` 引用的 3 个资源路径均验证存在，无悬空引用。对照集 body 与主集完全一致（diff 无输出），仅 frontmatter description 不同（损坏，见 §12.3）。

---

## §3 Frontmatter 与 Description 合规（SKILL-SPEC §1–§2）

### 3.1 name 字段

`name: prioritization-effort-impact`，小写、连字符合法、≤64 字符。与目录名 `113-prioritization-effort-impact` 的关系：spec 字面要求"name MUST match directory name"，但本语料库的既有惯例是所有技能目录带 `NNN-` 前缀而 name 不带（已验证 112-postmortem → `postmortem`、017-cease-desist → `cease-desist`、025-docx → `docx`）。113 遵循语料库惯例，dossier 也从未将此类前缀差异计为违规；此处仅记录 spec 字面与 corpus 惯例的已知张力，不判违规。

### 3.2 违禁字段

Frontmatter 仅有 `name` 与 `description` 两个键，全部在允许列表内，无 §1.3 列出的任何违禁字段（无 version / metadata / tags / trigger 等）。description 以未加引号的 YAML plain scalar 书写，内部出现的双引号（`or asks "what should we do first?"`）位于标量中间而非开头，YAML 解析合法。通过。

### 3.3 description 结构（§2.1）

```
Effort-vs-impact prioritization framework for backlog ranking and roadmap
decisions. Use when ranking backlogs, deciding what to do first based on
effort vs impact (quick wins vs big bets), prioritizing feature roadmaps,
triaging bugs or technical debt, allocating resources across initiatives,
identifying low-hanging fruit, evaluating strategic options with 2x2 matrix,
or when user mentions prioritization, quick wins, effort-impact matrix,
high-impact low-effort, big bets, or asks "what should we do first?".
```

- **WHAT**：第一句明确"effort-vs-impact prioritization framework for backlog ranking and roadmap decisions"，具体不空泛。通过。
- **WHEN**：列举 7 个触发场景（排 backlog、按 effort/impact 决定先做什么、排特性路线图、分诊 bug/技术债、跨项目分配资源、找低垂果实、用 2x2 评估战略选项）+ 关键词匹配（用户提到 prioritization / quick wins / effort-impact matrix / high-impact low-effort / big bets，或问"先做什么"）。通过。
- **KEYWORDS**：域术语丰富——prioritization、quick wins、effort-impact matrix、high-impact low-effort、big bets、backlog、roadmap。触发匹配面广。通过。
- **人称**：第三人称，无 imperative 开头、无第一/第二人称。通过。
- **长度**：约 500 字符，远低于 1024 上限。通过。
- **无跨技能路由**：description 内无"NOT for X, use Y instead"式路由，符合 §2.5。通过。

### 3.4 trigger 短语的轻微歧义（与 112 同类的字面问题）

§2.4 要求 description 至少出现一个枚举 trigger 信号："Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."。本 description 的短语是 **"Use when ranking backlogs, deciding …, prioritizing …, or when user mentions …, or asks …"** ——以 "Use when" 开头但动词是动名词 "ranking"，字面上不匹配任一枚举短语（"when user mentions" / "asks" 也是未枚举变体）。按精神判定（"Use when" + 具体场景，且无 imperative 嫌疑）可算通过，dossier 亦未提出异议；但若评估器（或 harness 的 skill 匹配层）对 trigger 短语做字面匹配，此条存在失效风险。建议改为 "Use when the user asks to rank backlogs, decide what to do first by effort vs impact, …"（§13 修复项 P2-1）。

### 3.5 小结

description 是本批次中信息密度较高的一个：WHAT/WHEN/KEYWORDS 三层齐备、关键词覆盖面广（含"什么先做"这种自然语言问法）。唯一可挑剔处是 3.4 的字面歧义与超长单句。合规结论：通过（含一处建议级修改）。

---

## §4 Body 结构合规（SKILL-SPEC §3）

### 4.1 三必需节

| 必需节 | 本技能对应位置 | 判定 |
|--------|----------------|------|
| Workflow / Process | `## Workflow`（5 步流程 + 进度 checklist + 每步展开，引用 Scoring Frameworks 与 template.md） | 通过 |
| Output Format | 无显式 `## Output` 标题；由 `## Quick Reference → Success Criteria`（6 条成功标准）+ Step 4（"Create prioritized roadmap … See resources/template.md for roadmap structure"）+ Step 5（rubric 自评）+ template.md 的路线图模板隐性定义 | 部分通过（隐性） |
| Scope / Limitations | `## When to Use`（8 条使用场景 + 5 条触发示例，仅覆盖"何时用"）；`## Quick Reference → When to use alternatives`（RICE/MoSCoW/Kano/ICE/CoD 替代路由，构成部分边界）；无显式 "Do NOT use when" 负面边界 | 部分通过（隐性） |

Output 与 Scope 是本节需要讨论的两项：

- **Output**：功能上闭环（Success Criteria 的 6 条实质是输出验收标准，Step 4 把 template 固定在 workflow 内，rubric 的 Completeness & Structure 维度定义产物清单）。但语料库中同类的 112-postmortem 也已为隐性输出被建议补显式节（112 审查 P2-2），113 情况相同。建议加简短 `## Output Format` 节（§13 P2-2）。
- **Scope**：与 112 对比尤其明显——112 的 When to Use 含显式 "Do NOT use when" 三条负面边界，113 完全没有负面边界节；"When to use alternatives" 只回答了"什么时候换方法"，未回答"什么时候根本不该用本技能"（例如：单个一次性决策无需排序、需要定量最优化的场景、仅需主观拍板时）。这是 dossier 判定"112 三节齐全而 113 仅 workflow/output 齐备"的具体体现。建议补显式 Limitations 节（§13 P2-3）。

### 4.2 尺寸限制

- Body（不含 frontmatter）214 行，远低于 600 行硬上限。通过。
- 按 §3.2 模式表，本技能申报 `pattern: process`（SCORING.yaml），对应目标行数 ~200；实际 214 行 + 两个资源文件（374 + 488 行）分担深度内容，模块化拆分合理（模板与方法论外置，主文件保持导航性）。

### 4.3 文件引用

- 3 处资源引用均为技能内相对路径（`resources/template.md`、`resources/methodology.md`、`resources/evaluators/rubric_prioritization_effort_impact.json`），全部存在。通过。
- 无跨技能引用（无 `../other-skill/` 形式）。通过。
- TOC 8 个条目与正文 8 个节标题逐项对应，锚点正确（§6 复核）。通过。

### 4.4 内容指南（§3.4）

- **知识增量**：未赘述"什么是 backlog"这类模型已知概念，直接进入矩阵框架。通过。
- **反模式优先**：Common Patterns 的 Red flags 四连（❌ 无 quick wins / 全 quick wins / 大量 time sinks / 全 3 分）与 Guardrails 全节 "✓ 对例 / ❌ 错例" 结构符合"具体 NEVER 规则 > 泛泛警告"。通过。
- **决策树/表格优先**：四象限表、按域模式表、按利益相关方模式表、effort/impact 维度表均为结构化表格。通过。
- **具体优先**：CSV export（2 天）、auth 重建（3 月）、logo 像素对齐、footer 错字四件套示例具体可参照；dark mode 示例带完整维度分解与算术。通过。

### 4.5 小结

Body 结构合规性整体良好，差距集中在 Output/Scope 两个隐性定义处（均非硬违规）。修复 P2-2/P2-3 后即为结构完整的三节齐备技能。

---

## §5 逻辑一致性分析

### 5.1 象限定义与几何一致性

四象限定义在三个文件中几何一致：

| 来源 | 高影响×高工作量 | 高影响×低工作量 | 低影响×高工作量 | 低影响×低工作量 |
|------|----------------|----------------|----------------|----------------|
| SKILL.md 象限表 | Big Bets (do 2nd) | Quick Wins (do 1st!) | Time Sinks (avoid) | Fill-Ins (do last) |
| SKILL.md 示例表 | auth 重建 | CSV export ✓ | 像素对齐 ❌ | footer 错字 |
| template.md ASCII 矩阵 | 左上 | 右上 | 左下 | 右下 |
| rubric by_context | Strategic Investments | Quick Wins | Money Pits | Nice-to-Haves |

坐标轴方向一致（effort 横轴、impact 纵轴；左=高 effort、上=高 impact），无错位。示例表四个条目各自的 effort/impact 判定（2d/High、3mo/High、1wk/Low、5min/Low）与象限结论匹配。通过。

### 5.2 Workflow ↔ SCORING 映射

5 步流程与 SCORING 13 项 criterion 的溯源关系：

| Workflow 步骤 | SCORING 项 | 对应关系 |
|---------------|-----------|---------|
| Step 1 收集条目 + 定义评分刻度 | SCOPE-02 | 一致 |
| Step 2 打分（effort/impact 双维度） | SCOPE-03 / PROC-01 | 一致 |
| Step 3 上矩阵 + 分象限 | PROC-02 | 一致 |
| Step 4 排路线图（QW→BB→FI，砍 TS） | PROC-03 / PROC-04 / OUT-01 | 一致 |
| Step 5 自评 + 沟通决策 | OUT-02 / NEG-01 / NEG-02 / QA-01 | 一致 |
| （无独立步骤）容量缓冲 | OUT-03 | 来自 Quick Reference 成功标准 |

Guardrails 与评估项也一一对应：Guardrail 1（多元视角）↔ NEG-01，Guardrail 7（strategic override）↔ NEG-02，Common Mistakes（路线图超载）↔ OUT-03，Red flags（全 3 分）↔ CF-02。溯源清晰，这是本技能评估体系最突出的优点。

### 5.3 教学示例算术复算（本技能最值得核查的部分）

对全部可复算示例逐项验算：

| 示例 | 文件 | 验算 | 结果 |
|------|------|------|------|
| Dark mode Effort 均值 | SKILL.md | (3+2+2+1)/4 = 2.0 | ✓ |
| Dark mode Impact 均值 | SKILL.md | (4+2+3+3)/4 = 3.0 | ✓ |
| RICE Feature A | methodology | 5000×3×100%/2 = 7500 | ✓ |
| RICE Feature B | methodology | 500×5×50%/1 = 1250 | ✓（A/B 之比 6 倍正确） |
| ICE A / B | methodology | 8×9×7=504；10×3×5=150 | ✓ |
| CD3 A / B | methodology | 100/2=50；200/5=40 | ✓ |
| Opportunity 示例 | methodology | 5+(5-2)=8；2+max(2-3,0)=2 | ✓ |
| 加权评分 Feature A | methodology | 1.6+1.5+0.6+0.2 = 3.9 | ✓ |
| **加权评分 Feature B** | methodology | 0.8+1.2+1.0+0.4 = **3.4**，表格显示 **3.0** | ✗ |

**加权评分示例存在算术错误（P1-1）**：Feature B 的四个加权值（0.8、1.2、1.0、0.4）在表格中逐格正确，但合计列写成 3.0，实际应为 3.4；正文结论"Feature A scores higher (3.9 vs 3.0)"也应改为 (3.9 vs 3.4)。结论方向不受影响，但这是打分型技能的教学材料，示例数字错误会直接削弱 agent 对加权算法的信任（dossier 对 074/039 等数字矛盾均判为实质问题）。这是本技能最需要立即修复的内容缺陷。

### 5.4 示例跨文件一致性（语料库亮点）

CSV export 示例贯穿三个文件且口径一致：SKILL.md 示例表 "Add 'Export to CSV' button | Low (2d)"；template.md 校准锚点 "Effort=2 example: Add CSV export (2 days, one dev)"；rubric 的 excellent indicator "Reference items documented for calibration (e.g., 'Effort=2 example: CSV export, 2 days')"。三处完全一致，与 112-postmortem 的数据库连接池示例同为语料库中少见的"示例贯穿全 skill 家族"品质。

### 5.5 象限边界未定义 + 示例与 rubric 冲突（P1-2）

三个文件对"多高算 High"没有统一口径：

- SKILL.md 无任何高/低阈值定义；自带示例把 Impact 均值 3.0（自评 "Medium-High"）判为 **Quick Win**；
- template.md 的 ASCII 矩阵分界线画在刻度 3 上（横线在行 3、竖线在 3/2 之间），3 分项恰好悬在边界上，未给出归属规则；
- rubric 的 Quadrant Classification 评分锚点举例 "reasonable boundaries (e.g., >3.5 = high)"，若按此口径，Impact=3.0 不属 high，dark mode 应判 Fill-In 而非 Quick Win；
- rubric 的 poor indicator "50%+ Quick Wins（unrealistic）" 与 SKILL.md 的典型分布（10-20%）一致，但正是因为没有边界定义，agent 无法复现"10-20% 的 Quick Win"这一分布预期。

后果：SCOPE-03/PROC-02/CF-02 的 LLM judge 对"3.0 分项归入哪象限算正确"没有客观依据，跨 agent 判定会漂移，污染测量。修复：在 SKILL.md Step 3 或 What Is It 中明确定义边界（建议：维度均值 ≥3.5 为 high、≤2.4 为 low、2.5-3.4 为边界需显式裁决，或简化为中线交叉），并同步修正 dark mode 示例的分类标注（P1-2）。

### 5.6 典型象限分布不封闭（P1-3）

```
Quick Wins: 10-20%   Big Bets: 20-30%   Fill-Ins: 40-50%   Time Sinks: 10-20%
```

四象限是全集划分，分布应和为 100%；当前区间和 80-120%，无法同时成立（例如 QW=20%、BB=30%、FI=50%、TS=20% 时和为 120%）。rubric 沿用 10-20% QW / 20-30% BB 的表述，同样的不封闭问题在 rubric 中传递。建议改为封闭区间（如 QW 10-15%、BB 20-25%、FI 40-55%、TS 10-20%），三个文件同步调整（P1-3）。

### 5.7 跨文件量表漂移（P2-4）

SKILL.md 的 Scoring Frameworks 与 template.md 的 Scoring Scales 对同一维度给出不同锚点：

| 维度 | 级别 | SKILL.md | template.md |
|------|------|----------|-------------|
| 用户覆盖率 | 2 | 1-10% | 5-20% |
| 用户覆盖率 | 3 | 10-50% | 20-50% |
| 用户覆盖率 | 1 | <1% | <5% |
| 业务价值 | 2 | $10-100K | $10-50K |
| 业务价值 | 3 | $100K-1M | $50-200K |
| 业务价值 | 4 | $1-10M | $200K-1M |

agent 若按 template.md 校准则 30% 覆盖率打 3 分，按 SKILL.md 则打 2 分——同一条目跨文件得到不同分值，评分表与矩阵的刻度一致性被破坏。建议统一为单一锚点表（P2-4）。

### 5.8 其他轻度不一致

- **CD3 缩写误展开 + 重复标题（P2-7）**：methodology.md 标题写 "CD3: Cost, Duration, Delay"，而 CD3 的标准展开是 "Cost of Delay Divided by Duration"（Reinertsen/WSJF 系指标），属事实性误展开；且该节内 "**When to use**" 粗体出现两次（L154 与 L165），排版重复。
- **Opportunity 评分边界（P2-9）**：规则写 ">8 = High opportunity"，示例恰为 8 分却标注 "8 (high opportunity)"，8 分归属矛盾（≥8 还是 >8）。
- **1-10 刻度与评估口径冲突（P2-12）**：SKILL.md Guardrail 2 明确允许 "Force rank or use wider scale (1-10)" 作为差异化手段，而 SCORING PROC-01 的 question 硬编码 "scored on effort (1-5) and impact (1-5)"。完全遵从技能建议改用 1-10 刻度的 agent 会被 PROC-01 误判为失败，评估口径与技能内容冲突（详见 §10.4）。

### 5.9 小结

主体逻辑（象限几何、workflow 闭环、示例贯穿）高度自洽，算术大部分正确；扣分点集中在 5.3 的加权示例错误（必须修）、5.5 的边界未定义、5.6 的分布不封闭，以及 5.7/5.8 的跨文件口径问题。

---

## §6 语法与可读性

- 全文件未发现拼写错误、病句或标点滥用（逐行核查 SKILL.md 218 行、template.md 374 行、methodology.md 488 行、SCORING.yaml 122 行）。
- 术语使用一致："quick wins"、"big bets"、"fill-ins"、"time sinks" 四象限名在全部文件（含 rubric）拼写与语义统一；"effort-impact" 与 "impact-effort" 两种说法并存但指向同一矩阵，无歧义。
- 结构可读性：SKILL.md 有 TOC 且 8 个条目与实际标题逐项对应；template.md 的模板表格、矩阵 ASCII、评分表格式工整；methodology.md 分层标题（## 1. Advanced Scoring Frameworks 等）规范；rubric JSON 缩进与字段命名一致。
- 轻微冗余：(a) SKILL.md 的 Common Patterns（域模式表）与 template.md 的 Quick Patterns 内容高度重叠（约 30 行语义重复）；(b) template.md 开头完整复刻了 SKILL.md 的 5 步 workflow（约 25 行逐字重复）；(c) SKILL.md 的 Common Mistakes 7 条与 Guardrails/Red flags 部分重叠。冗余不造成矛盾，但压缩后主文件更精炼（P3-1）。
- description 为超长单句（约 500 字符一个句子），信息完整但可读性一般，建议按 WHAT / WHEN / KEYWORDS 断成两到三句（并入 P2-1）。
- check.py 注释为英文且措辞欠打磨（"Run all 0 script-verifiable checks"、误导性的 `_is_path` 注释），见 §11。

语法与可读性评级：优秀。

---

## §7 人机感

- **语气**：中性决策支持语气（与 dossier 判定一致）——Workflow 用 "Copy this checklist and track your progress"，Common Patterns 用按域/按角色的模式表，整体是"中立引导者"口吻，不替用户拍板，也无意气用事的指令。
- **符号使用**：✓/❌/❓ 全部出现在象限标注、Guardrails 对错例对照、模板示例等功能性语境中；无 🎉/📌 一类情绪性 emoji；"do 1st!" 的感叹号是唯一轻量强调，可接受。符号纪律与 112 一致。
- **人机交互设计亮点**：When to Use 提供 5 条引号包裹的"用户原话"触发示例（"We have 50 feature requests, where do we start?"、"What are the quick wins?"），直接给 agent 展示了用户的自然语言入口，与 SkillIF 的 trigger 测量目标高度契合；Guardrail 7 的 "❌ 'CEO wants it' → auto-scored 5" 与 methodology Pitfall 4 的回应话术（"Let's score this using our framework…"）都是把"人的偏见"转化为"可执行流程"的成熟处理。
- **无营销腔**：无 "world-class" 式自我膨胀，无 "Let's…!" 对话填充。
- **可挑剔处（P2-10）**：Guardrails 与 methodology 的 2 小时工作坊、silent voting、pre-mortem 等利益相关者协作技术隐含"团队会议现场"假设，而 agent 执行单次任务时没有真实的工程师/销售可召集；技能未说明此时 agent 应做什么（请求用户提供输入、显式标注假设、还是用角色代偿）。该缺口与 NEG-01 的判定风险同源（§10.2），且与 112 审查的 P1-2（agent 交付边界未定义）属同一类问题。

人机感评级：良好（接近优秀，被单次执行边界模糊扣一档）。

---

## §8 Resources 质量审查

### 8.1 resources/template.md

- **结构**：TOC → 5 步 workflow（复刻）→ 矩阵 ASCII 图 + 象限汇总 → 评分表（含 5 级 effort/impact 锚点 + 可选维度明细表）→ 分阶段路线图模板（Quick Wins / Big Bets / Fill-Ins / Time Sinks + 容量规划）→ 逐节 Guidance → 按上下文 Quick Patterns → Quality Checklist（评分/矩阵/路线图/沟通四组 + Red Flags）。
- **优点**：模板是全技能家族中最"可用"的部分——矩阵 ASCII 图与 SKILL.md 象限几何一致；路线图模板带 Owner/Timeline/Dependencies 列与容量缓冲占位；Quality Checklist 的勾选项实质是 rubric 的操作化版本，agent 照单执行即可达标；Deferred/Rejected 表（Time Sinks 的 "Reconsider When" 列）把"拒绝要给出理由和回看条件"落到结构上。
- **问题**：(a) 评分量表与 SKILL.md 漂移（§5.7，P2-4）；(b) 矩阵分界线画在刻度 3 上，边界项归属规则缺失（§5.5，与 P1-2 合并处理）；(c) 开头 workflow 与 SKILL.md 逐字重复（P3-1）；(d) 快速模式与 SKILL.md Common Patterns 语义重叠（P3-1）。

### 8.2 resources/methodology.md

- **结构**：6 大节（Advanced Scoring Frameworks / Alternative Models / Stakeholder Alignment / Data-Driven / Roadmap Optimization / Common Pitfalls）+ 前 5 节带 TOC。
- **优点**：深度显著——RICE/ICE/加权/Kano/CD3/Opportunity 六种替代方法、silent voting/强制排序/$100 预算/按专业度加权/pre-mortem 五种利益相关者技术、使用量分析/AB 测试/请求计数/NPS 驱动四类数据驱动、依赖图/产能/增量交付/组合平衡四种路线图优化、10 个 Pitfall 带解决话术；"If you wouldn't start this project today knowing what you know, stop it now"（sunk cost）一类决策规则简洁可执行。
- **问题**：(a) 加权评分示例 Feature B 总分 3.0 应为 3.4（§5.3，P1-1）；(b) CD3 缩写误展开 + "When to use" 重复（§5.8，P2-7）；(c) Opportunity 评分 8 分边界矛盾（§5.8，P2-9）；(d) 组织级内容（ICS 角色轮转、季度复盘会议）与单次 agent 任务粒度差，未标注哪些节为单次任务必读（并入 P2-10）。

### 8.3 resources/evaluators/rubric_prioritization_effort_impact.json

- **结构**：8 个 criterion（Scoring Quality & Differentiation 1.4 / Quadrant Classification Accuracy 1.3 / Stakeholder Alignment & Input Quality 1.2 / Roadmap Sequencing & Realism 1.3 / Effort Scoring Rigor 1.1 / Impact Scoring Rigor 1.2 / Communication & Decision Transparency 1.1 / Completeness & Structure 1.0），权重合计 9.6；每个 criterion 有 1-5 级行为锚定 + excellent/poor indicator 清单；另有 guidance（by_context 4 类、by_team_size 3 档、by_time_horizon 3 档）、6 条 common_failure_modes、3 组 excellence_indicators。
- **优点**：行为锚定具体可判定（如 Effort 5 级要求 "时间+复杂度+风险+依赖+未知+跨团队协调+QA+部署，且对照历史校准"）；common_failure_modes 与 SKILL.md 的 Red flags 一一呼应（all_quick_wins ↔ ❌ 全 quick wins；all_3s ↔ ❌ 全 3 分；solo_prioritization ↔ Guardrail 1）；by_team_size 的产能建议（2-5 人 60%、6-15 人 70-80%、16+ 人 75-85%）与 methodology 的产能计算（60% 项目容量）互相印证，无矛盾。
- **问题**：(a) 无 passing threshold 与权重归一化说明——权重合计 9.6 的加权总分如何换算、多少分算通过，rubric 未定义，QA-01 的"自评"无从锚定（P2-11）；(b) by_context 只有 4 类（product_backlog / technical_debt / bug_triage / strategic_initiatives），SKILL.md Common Patterns 的 5 个域中 marketing_campaigns 无对应条目（P2-8）；(c) ">3.5 = high" 的边界举例与 SKILL.md dark mode 示例冲突（§5.5，P1-2 同源）。

### 8.4 小结

资源三件套整体质量在语料库 resources 中属中上梯队：template 操作化程度高、methodology 深度好、rubric 锚定扎实。主要修复项集中在两处算术/边界问题（P1-1/P1-2）与量表、覆盖类小问题（P2-4/P2-7/P2-8/P2-9/P2-11）。

---

## §9 评估体系审查（SCORING.yaml）

### 9.1 总体结构

`skill: prioritization-effort-impact`、`pattern: process`、`total_items: 13`，与实际 criterion 数量一致。分类：scope 3、process 4、output 3、negative 2、qa 1。judge 分配：**13 项全部为 llm、0 项 script**。2 个 critical_failures（CF-01 无打分 → cap_to_0；CF-02 全项同分 → cap_to_0）。

### 9.2 设计优点

- **关键失败项设计正确**：CF-01（未做 effort/impact 打分，按请求顺序或任意排序）与 CF-02（全 3 分，无实际差异化）都是"技能没有被执行"的一票否决信号，cap_to_0 强度与技能核心价值匹配；CF-02 与 SKILL.md 的 Red flags（"Effort/impact scores all 3: Need more differentiation"）精确呼应，溯源干净。
- **溯源清晰**：13 项全部能在 SKILL.md 找到对应出处（§5.2 映射表），LLM judge 收到 question 后可在技能内容中直接定位证据。
- **SCOPE-03 防单维排序**："Both effort AND impact scored for every item — no single-dimension ranking" 独立成项，能单独暴露"只按 impact 排、忽略 effort"的偷懒行为，是评估设计中少见的防退化项。
- **QA-01 测过程而非结果**：把 Step 5 的 rubric 自评动作本身作为被测行为，符合 SkillIF 的测量目标。
- **负面项位置合理**：NEG-01（隔离打分）/NEG-02（strategic override）独立成类，且与 Guardrail 1/7 一一对应。

### 9.3 评估口径与技能内容的映射核对

- SCOPE-01 与 description 的关键词集完全一致（backlog / bugs / technical debt / initiatives / roadmap）——触发一致性设计到位。
- OUT-01/02/03 与 Quick Reference 成功标准一致（QW 优先排序、rationale 透明、容量缓冲），其中 OUT-02 的示例引文 "Effort=4 because 3 teams, new infra, 6 weeks" 与 SKILL.md Guardrail 4 的示例 "Effort=4 because requires 3 teams, new infrastructure, 6-week timeline" 措辞同源，评估与内容自洽。
- PROC-01 的 "1-5" 硬编码与技能自身允许的 1-10 扩宽刻度冲突（§10.4）。
- QA-01 无阈值锚定（§10.6）。

---

## §10 评估体系缺陷与风险

### 10.1 全 LLM 判定、零 script 检查（P2-5）

SCORING.yaml 13 项全部 `judge: llm`，check.py 的 `check()` 恒返回空 dict（docstring 自述 "Run all 0 script-verifiable checks"）。与语料库整体 36.1% script 占比（research design 统计）形成极端对比——本技能的机械检查贡献为 0%。风险有三：

1. **CF-01 本可机械检测**：CF-01（无打分、任意排序）完全可以用 "输出中存在至少 N 条带 effort/impact 分值的条目" 这类正则/解析冒烟检查兜底，LLM 只负责语义判定。当前全 LLM 化把确定性判定全部交给语义判断，复现性打折。
2. **检查项冗余放大**：13 项全 LLM 意味着 runner 的 script 阶段空转，检查成本全部压在 LLM 侧（research design 的设计初衷是脚本做机械层、LLM 做语义层，各取其长）。
3. 若"纯 LLM"是刻意设计（本技能输出形态自由，机械检查价值低），应在 SCORING 头部注明设计意图，避免后续维护者误判为遗漏。

建议：增加 2 个 script 冒烟项（如输出含四象限名、输出含 ≥N 条带 effort/impact 的分值条目），或显式注释设计理由（P2-5）。

### 10.2 NEG-01 不可满足性与虚构诱导（P1-4）

NEG-01 要求 "incorporate stakeholder perspectives (engineering, product, sales, customers) rather than scoring in isolation"。技能自身的 Guardrail 1 也确实要求多元利益相关者参与。但单次全流程评测任务（SkillIF 第一期设计）通常**不提供**利益相关者输入——此时完全遵从技能的 agent 只有两条路：(a) 请求用户提供输入或显式声明"利益相关者视角缺失"；(b) 为通过检查而**编造**"工程团队估计 effort=4、销售表示 impact=5"这类不可验证的声明。当前 question 措辞 "Did the agent incorporate stakeholder perspectives…" 对 (b) 恰好放行、对 (a) 可能误判，等于奖励虚构。这与 112-postmortem 审查发现的 PROC-05（48 小时共享不可控）属同一类"可满足性缺陷"，应改写为区分可观察行为：agent 是否请求输入或标注缺失、是否编造（P1-4）。

### 10.3 PROC-03 / OUT-01 冗余（P2）

PROC-03（"quick wins identified and prioritized first"）与 OUT-01（"roadmap sequenced quick wins first, big bets second…"）语义高度重叠——前者是"识别并优先"，后者是"路线图按 QW→BB 排序"，同一行为从 process 与 output 两个角度各测一次。参照 112 审查对 OUT-01/OUT-03 冗余的处理，建议将 PROC-03 聚焦"识别"（哪些条目被认定为 QW），OUT-01 聚焦"排序"（路线图中的位置），在 question 中显式区分，否则两个 LLM 判定高度相关、信息量重合。

### 10.4 PROC-01 硬编码 1-5 与技能 1-10 扩宽冲突（P2-12）

SKILL.md Guardrail 2 明示差异化手段之一为 "use wider scale (1-10)"，而 PROC-01 的 question 写死 "scored on effort (1-5) and impact (1-5)"。遵从技能建议使用 1-10 刻度的 agent 会被判失败——评估口径与技能指令互相打架（与 112 的 3.0/3.5 阈值冲突同类）。建议 question 改为 "有明确分值刻度（1-5 或技能允许的 1-10）且分值覆盖全刻度范围"。

### 10.5 SCOPE-03 / CF-01 嵌套（P3）

SCOPE-03（双维度打分）与 CF-01（无打分）语义部分重叠：CF-01 触发必然意味着 SCOPE-03 失败，但 SCOPE-03 还覆盖"单维排序"的中间情形。嵌套可接受（CF 是更宽的一票否决），记录在案即可。

### 10.6 QA-01 无阈值锚定（P2-11 关联）

QA-01 只问 "Did the agent self-check the output against the bundled rubric?"，而 rubric 未定义通过线（§8.3，权重 9.6 无归一化说明）。LLM judge 判定"自评"时无从核对自评结论是否合理（agent 自评 5/5 与 3/5 都算"自评过"）。与 112 相反（112 的问题是阈值冲突，113 的问题是阈值缺失），建议 rubric 增加 evaluation_notes 定义换算与通过线，QA-01 的 question 同步要求"自评结论与 rubric 锚点一致"。

---

## §11 check.py 实现审查

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from checker import (
    set_tool_log_path, set_agent_output,
)
```

- 路径注入正确：`../_shared/checker.py` 存在（已验证），`set_agent_output` / `set_tool_log_path` 在 CHECKER-LIBRARY 中有定义；`output_contains` 等函数存在但本技能未使用。
- `check()` 恒返回空 dict，docstring "Run all 0 script-verifiable checks" 自洽；runner 协议要求处理空结果（LLM 项另行判定），接口层面无错误，但机械覆盖为零（§10.1，P2-5）。
- **死代码**：`_is_path` 分支的逻辑与注释不符——`main()` 无条件地在 `os.path.exists(agent_output)` 为真时读取文件内容并重赋值 `agent_output`，因此 `check()` 收到的永远是文本；`check()` 内再用 `os.path.exists(agent_output)` 判断"是否为路径"永远不会为真，`set_agent_output` 实际总会执行。注释声称 "main() has already loaded its content; set directly only when the argument is the raw text" 与实际控制流相反，属模板复制遗留（P2-6）。
- `set_tool_log_path(tool_log)` 被调用但 0 个检查使用 tool log，属冗余调用；13 个 LLM 项以注释罗列（"SCOPE-01: llm judge (not checked here)" 等），可读但占 13 行噪声，可压缩为一段说明。
- `main()` 无异常保护：任何抛错都会输出非 JSON 并使 runner 侧失败——建议包 try/except 保证恒输出合法 JSON（P2-6 一并处理）。
- 参数校验（`len(sys.argv) != 4` 时输出 error JSON）是正确的最小防护。

实现质量评级：合格；接口正确、协议合规，但实质为空壳实现，改进点为死代码清理与 1-2 个冒烟检查（P2-5/P2-6）。

---

## §12 与 Dossier 及语料库对比

### 12.1 Dossier 结论核对

Dossier（Batch 101-125）对 113 的结论：

> "逻辑: 113 2x2 矩阵与红标启发式一致；语法: 均干净结构良好；人机感: 113 中性决策支持；合规: 112 全部三节齐全；113/114 workflow/output 齐备；总评: 🟢 三个均为强 skill。"

本审查与 dossier 的一致性：总体评级一致（良好档）；"2x2 矩阵与红标启发式一致"完整复现（§5.1/§5.2）；"中性决策支持"复现（§7）；"workflow/output 齐备"认可，并补充——Output 为隐性定义（§4.1），Scope 更是只有 When to Use 无负面边界，dossier 的"齐备"实质是"隐性齐备"。

本审查在 dossier 之外新增的发现（dossier 为逐项 5 维度简评，未覆盖以下层面，属预期差异而非矛盾）：加权评分示例算术错误（§5.3）、象限边界未定义（§5.5）、典型分布不封闭（§5.6）、跨文件量表漂移（§5.7）、CD3 缩写误展开（§5.8）、SCORING 全 LLM 化（§10.1）、NEG-01 虚构诱导（§10.2）、PROC-01 刻度冲突（§10.4）、对照集 description 损坏（§12.3）。这些发现不改变 🟢 档结论，但使其从"三个均为强 skill"修正为"修复 4 个 P1 级问题后即为语料库范本级"。

### 12.2 语料库横向定位

- 与 ~68% 缺 Scope 节的技能对比：113 有 When to Use（正边界）+ "When to use alternatives"（方法边界），但缺 112 那样的显式 "Do NOT use when" 负面边界——处于语料库中上位置（好于纯缺失，弱于 112/067/127 的三重复合边界）。
- 与同批次的 112-postmortem 对比：两者同为 process 型、同为 🟢、同为隐性 Output；差异在 Scope（112 有负面边界，113 无）与评估体系（112 有 3 个 script 项，113 为 0）——112 在结构完整度上略胜，113 在示例算术上略输（112 无算术错误，113 有 1 处）。
- 与示例贯穿度对比：113 的 CSV export 示例三文件一致，与 112 的数据库连接池示例同属语料库稀有品质。
- 与同类决策支持型技能对比：113 无 121-senior-ml-engineer 式的"空模板"问题（§3.4 知识增量通过）、无 083-085 系列的内容空洞、无 074 式的"示例与公式对不上"级错误（074 的 ROI 示例矛盾比 113 的加权示例错误严重得多——113 的错误不改变结论方向，074 的错误使示例输出自相矛盾）。按 dossier 的 🔴/🟠/🟡/🟢 尺度，113 处于 🟢 档内中等偏上的位置。
- 与语料库均值对比：SCORING 全 LLM 化（0% script）是全语料库 322 个技能中的极端值（均值 36.1%），在评估设计层面值得单独复查（§13.3）。

### 12.3 对照集核查（跨批次共性发现）

`complex-skills-no-trigger/113-prioritization-effort-impact/SKILL.md` 的 frontmatter description 为：

```yaml
description: 5. [Common Patterns](#common-patterns)
```

- 触发切除管线本应从 body 提取替代描述（research design 记录的处理类型 2："纯 trigger 描述，从 body 提取替代"），但此例提取到的是 **TOC 第 5 条锚点**——description 变成了一个 Markdown 锚点链接，完全不再描述技能。
- body 与主集逐字节一致（`diff` 无输出），即主/对照两集在该技能上的唯一差异正是这条损坏的描述。
- 对实验的影响：Mode B（自然激活）对照组的设计前提是"同一技能、仅 trigger 短语被切除"。113 对照组的描述不仅无 trigger，而且语义失效——harness 的匹配层看到的是一个链接文本，agent 侧则可能因描述无法描述技能而在激活质量、初始上下文质量上双双劣化。观测到的遵从度差异将无法归因于"无 trigger"一个变量。同类损坏是否存在于其他技能需全量复核（本次审查仅核对 113 一例）。
- 建议：为对照集生成管线增加质量门——生成的 description 必须 (a) 是完整句子且含动词谓语句干，(b) 非空、不含 Markdown 语法标记（`[`、`]`、`(`、`#`），(c) 与 body 的 TOC/锚点文本不匹配；113 对照集描述应重新生成（从 body 的 Purpose 段提取替代描述）（P2-13）。

---

## §13 综合评估与改进建议

本节为报告主体，综合前述 12 节的证据，给出五维度评分、分级修复清单（P1/P2/P3）、评估设计改进方案、合规复检与最终结论。

### 13.1 五维度评分

| 维度 | 评分 | 依据 |
|------|:----:|------|
| 逻辑一致性 | 4.0 / 5 | 象限几何三文件一致、workflow↔SCORING 完全映射、CSV 示例贯穿、多数示例算术正确；扣分：加权示例总分错误（3.0 vs 3.4）、象限边界未定义且示例与 rubric 冲突、典型分布不封闭（80-120%）、跨文件量表漂移 |
| 语法与可读性 | 4.6 / 5 | 零错字、术语统一、TOC 与实际标题一致、表格工整；扣分：description 超长单句、methodology CD3 节重复标题、template 开头逐字复刻 workflow |
| 人机感 | 4.3 / 5 | 中性决策支持语气、符号纪律好、用户原话触发示例与"strategic override"话术成熟、无营销腔；扣分：利益相关者工作坊假设对单次 agent 任务不可执行、无交付边界说明 |
| 规范合规性 | 4.2 / 5 | name/description/违禁字段/尺寸/引用/目录全通过；扣分：trigger 短语字面歧义、Output 与 Scope 均隐性（均为解释空间问题而非硬违规） |
| 评估体系 | 3.5 / 5 | criterion 溯源清晰、CF 设计与红标呼应、SCOPE-03 防退化项、QA-01 测过程；扣分：0 script 检查（全 LLM）、NEG-01 不可满足且诱导虚构、PROC-01 刻度冲突、PROC-03/OUT-01 冗余、QA-01 无阈值锚定 |

综合评级：良好（🟢 档，与 dossier 一致）。该评级成立的前提是下述 P1 项在下一轮评估运行前修复；若不修，加权示例错误会污染 agent 对评分算法的信任、边界未定义会引入 LLM judge 判定漂移、NEG-01 会诱导虚构数据，直接影响 SkillIF 测量数据的可信度。

### 13.2 问题分级清单

#### P1 级（修复后再运行评估）

| 编号 | 位置 | 问题 | 具体改法 |
|------|------|------|---------|
| P1-1 | methodology.md 加权评分示例（L66-72） | Feature B 总分显示 3.0，实际 0.8+1.2+1.0+0.4 = **3.4**；正文 "3.9 vs 3.0" 同步错误 | 表格 Total 改 3.4，正文结论改 "(3.9 vs 3.4)"；修改后重跑全表验算 |
| P1-2 | SKILL.md What Is It / Step 3 / dark mode 示例 + template.md 矩阵 + rubric | 象限高/低边界无统一定义；示例把 Impact=3.0（自评 "Medium-High"）判为 Quick Win，与 rubric 建议的 ">3.5 = high" 冲突 | 在 Step 3 明确定义边界（建议：维度均值 ≥3.5 为 High、≤2.4 为 Low、2.5-3.4 为边界项需显式裁决）；同步修正 dark mode 示例的分类或标注；template 矩阵分界线注明 3 分项归属规则；rubric 的 ">3.5 = high" 提升为正式定义而非举例 |
| P1-3 | SKILL.md Common Patterns 典型分布 + rubric 指标 | 四档区间 10-20 / 20-30 / 40-50 / 10-20 和为 80-120%，非封闭分布 | 改为封闭区间（如 QW 10-15%、BB 20-25%、FI 40-55%、TS 10-20%），SKILL.md 与 rubric 的 10-20% QW / 20-30% BB 表述同步调整 |
| P1-4 | SCORING NEG-01 | 单次任务无利益相关者输入，诚实 agent 无法满足；question 对"编造利益相关者观点"放行、对"请求输入/标注缺失"可能误判 | question 改为可观察行为判定："agent 是否请求利益相关者输入或显式标注视角缺失，且未编造不可验证的利益相关者声明"；与 §13.3 的可满足性复查一起处理 |

#### P2 级（建议修复，不影响当期运行）

| 编号 | 位置 | 问题 | 具体改法 |
|------|------|------|---------|
| P2-1 | SKILL.md description | trigger 短语 "Use when ranking…" 字面不匹配 §2.4 枚举（"when user mentions / asks" 亦为变体） | 改为 "Use when the user asks to rank backlogs, decide what to do first by effort vs impact, …"；同时按 WHAT/WHEN/KEYWORDS 断成两到三句 |
| P2-2 | SKILL.md | 无显式 Output Format 节（隐性定义） | 在 Quick Reference 前加 8-10 行 `## Output Format`：交付物 = 评分表（每项 effort/impact + rationale）+ 象限矩阵 + 分阶段路线图（QW→BB→FI，TS 显式拒绝）+ 容量缓冲说明 + rubric 自评分 |
| P2-3 | SKILL.md | 无显式 Scope/Limitations 负面边界 | 加 `## Limitations`（或 Do NOT use when）：单事项一次性决策、需要定量最优化、固定范围期限任务（转 MoSCoW）、时效成本显著（转 CoD）、纯主观拍板时不用本技能；把 Quick Reference 的 "When to use alternatives" 并入该节 |
| P2-4 | SKILL.md Scoring Frameworks ↔ template.md Scoring Scales | 用户覆盖率与业务价值 5 级锚点漂移（1-10% vs 5-20%；$10-100K vs $10-50K 等） | 统一为单一锚点表（建议以 SKILL.md 为准），template.md 改引主文件 |
| P2-5 | SCORING.yaml / check.py | 13 项全 LLM、0 script 检查，check.py 恒返回空 dict | 增加 2 个 script 冒烟项（如输出含四象限名、输出含 ≥N 条带 effort/impact 分值条目），或将"纯 LLM"作为有意设计在 SCORING 头部注明理由 |
| P2-6 | check.py | `_is_path` 死分支、注释与实际控制流相反、`set_tool_log_path` 冗余、main 无异常兜底 | 简化 `check()` 为直接 `set_agent_output`；移除死代码；main 包 try/except 保证恒输出合法 JSON |
| P2-7 | methodology.md CD3 节 | "CD3: Cost, Duration, Delay" 误展开（标准为 Cost of Delay Divided by Duration）；"When to use" 粗体出现两次 | 改缩写展开；合并重复标题 |
| P2-8 | rubric by_context | 缺 marketing_campaigns（SKILL.md Common Patterns 有 5 个域） | 补 marketing 条目（focus：email nurture 为 QW、品牌 overhaul 为 BB、minor A/B tests 为 TS；red flags：无渠道数据支撑的 impact 估值） |
| P2-9 | methodology.md Opportunity Scoring | 规则 ">8 = High opportunity" 与示例 8 分标 "high" 矛盾 | 统一为 "≥8 = High opportunity" |
| P2-10 | SKILL.md Guardrails / methodology.md | 利益相关者工作坊假设对单次 agent 任务不可执行，无交付边界 | 加一句："无利益相关者可用时，请求用户输入或显式标注假设，不得虚构视角"；methodology 开头标注哪些节为单次任务必读 |
| P2-11 | rubric | 权重合计 9.6 无归一化说明、无 passing threshold，QA-01 无从锚定 | 增加 evaluation_notes：总分换算（加权和 ÷ 9.6 × 5 或直接区间表）与通过线定义 |
| P2-12 | SCORING PROC-01 | 硬编码 "1-5" 与技能允许的 1-10 扩宽刻度冲突 | question 改为"有明确分值刻度（1-5 或 1-10）且分值覆盖全刻度、非全同分" |
| P2-13 | complex-skills-no-trigger/113 | 对照集 description 损坏为 TOC 锚点 "5. [Common Patterns](#common-patterns)" | 重新生成（从 body Purpose 提取替代描述）；为对照集管线加质量门：描述须为完整句子、含动词谓语句干、无 Markdown 语法标记、不得等于 TOC/锚点文本；全量复核其余 321 个对照集描述是否同类损坏 |

#### P3 级（记录在案，可不改）

- template.md 开头 5 步 workflow 与 SKILL.md 逐字重复约 25 行；Quick Patterns 与 Common Patterns 语义重叠约 30 行（P3-1）。
- check.py 以 13 行注释罗列 LLM 项，可压缩为一段说明（并入 P2-6）。
- SCOPE-03 与 CF-01 语义嵌套（CF 更宽，可接受）。
- When to Use 的 "New PM/leader" 条目偏动机/场景描述而非可判定的触发条件，无歧义但信息价值低。

### 13.3 评估设计改进建议（面向 SkillIF 测量目标）

本技能的评估体系与技能内容的高度绑定（§5.2 映射）是加分项，但本次审查暴露了三个结构性问题，对全部 322 个技能具有普适性：

1. **可满足性审查（satisfiability check）必须成为通用步骤**。NEG-01 的问题（单次任务拿不到利益相关者输入）与 112-postmortem 的 PROC-05（48 小时共享不可控）是同一病根的两种表现：criterion 描述了"组织流程中的正确行为"，却没有问"一个完全遵从的 agent 在单次任务里能否诚实地做到"。建议对每个 SCORING.yaml 的 llm 项执行自问："是否存在一条诚实路径通过它？"——没有则改写为可观察行为（请求输入、标注缺失、输出假设声明），必要时同步修改技能正文（如 P2-10）。
2. **script/LLM 分工回归均值**。本技能 0% script 与语料库 36.1% 均值的偏离过大。CF-01（无打分）这类"有没有"级别的判定完全适合脚本化（输出解析即可），把 LLM token 留给"分数合不合理"（CF-02 的语义部分）。至少应保证 check.py 不空转——空壳 check.py 使 runner 的机械层设计完全失效。
3. **对照集质量门**。P2-13 的 TOC 锚点式 description 损坏说明触发切除管线缺少对"替代描述语义有效性"的校验。建议：(a) 对 322 个对照集 description 做一次全量扫描（规则：含 Markdown 语法标记、以 `[`/`#` 开头、与 body 中任一文本逐字相等者全部标记）；(b) 生成规则增加"替代描述必须来自正文的完整句子"约束；(c) 把对照集 description 校验纳入 runner 启动前的资产检查，防止 Mode B 数据被损坏描述污染。

### 13.4 技能内容改进后自评（对照 SKILL-SPEC §5 合规清单）

执行 P2-1/P2-2/P2-3 后对照 §5 清单复检：name/description/trigger 信号/违禁字段/workflow/output/scope/引用/目录命名九项全部显式通过（当前仅 trigger、output、scope 三项依赖解释空间）。届时 113-prioritization-effort-impact 可与 112、067、127、139 并列进入"三节齐备 + 边界清晰"梯队；其 CSV 示例贯穿 + 红标启发式的组合在 decision-support 类技能中已具范本潜力。

### 13.5 最终结论

113-prioritization-effort-impact 是一个内容充实、结构合规、示例贯穿度良好的 process 型决策支持技能，dossier 的 🟢 评级成立。它的问题集中在三个层面：

1. **内容层硬伤（3 项）**：methodology.md 加权示例的算术错误（P1-1）、象限边界未定义导致的示例与 rubric 口径冲突（P1-2）、典型分布百分比不封闭（P1-3）。三者均为分钟级改动，修复后技能内容在数学与逻辑上无可挑剔。
2. **评估层缺陷（4 项）**：NEG-01 的不可满足性与虚构诱导（P1-4）、全 LLM 化的零 script 检查（P2-5）、PROC-01 刻度冲突（P2-12）、QA-01 无阈值锚定（P2-11）。这些属于评估器层面而非技能内容层面，但其存在会在评估运行时产生判定漂移与数据污染，应在下一轮评估前按 §13.2 的 P1 清单修复。
3. **对照集污染（1 项）**：no-trigger 对照集的 description 损坏为 TOC 锚点（P2-13），直接影响 Mode B 实验的变量隔离，建议立即全量复核对照集。

修复路径建议：先改 P1-1/P1-3（纯数字修正），再改 P1-2（边界定义，需三个文件联动），随后 P1-4 与 P2-5/P2-6（评估层），P2 其余各项按批次进行；每项修改后跑一次 `check.py` 冒烟并对照 §5 清单复核。完成 P1 全部项目后，本技能可作为 effort-impact 类决策支持技能的范本，其"技能内容 ↔ 评估标准 ↔ rubric 三方绑定"的映射（§5.2/§8.3）亦可作为模板供其他 process 型技能参考。

### 13.6 修复执行计划与验证方案

以下按依赖顺序给出建议的实施批次，每批完成后即可独立验证，不要求一次性全部落地：

| 批次 | 内容 | 涉及文件 | 验证方法 |
|------|------|---------|---------|
| B1（数字修正，10 分钟） | P1-1 加权总分 3.0→3.4；P1-3 分布区间封闭化 | methodology.md、SKILL.md、rubric | 重新逐格求和；四档百分比求和 = 100% |
| B2（边界定义，30 分钟） | P1-2 在 Step 3/What Is It 定义高/低阈值，修正 dark mode 示例标注，template 矩阵注明 3 分项规则 | SKILL.md、template.md、rubric | 用 dark mode（2.0/3.0）与 CSV（1.5/4.5 级）两组数据回代验证分类结果 |
| B3（评估层，30 分钟） | P1-4 NEG-01 改写；P2-5 加 2 个 script 冒烟项；P2-6 check.py 死代码清理；P2-12 PROC-01 刻度措辞 | SCORING.yaml、check.py | 运行 check.py 确认非空输出；构造"无打分"与"全 3 分"两份假输出验证 CF 冒烟项均能捕获 |
| B4（内容口径，40 分钟） | P2-1 description 触发短语；P2-2 Output Format 节；P2-3 Limitations 节；P2-4 量表统一；P2-7/8/9/10/11 各项 | SKILL.md、methodology.md、template.md、rubric | 对照 SKILL-SPEC §5 清单九项全部显式通过；description ≤1024 字符 |
| B5（对照集，30 分钟） | P2-13 重新生成 113 对照集 description，并全量扫描 322 个对照集 | complex-skills-no-trigger/ | 扫描规则：描述含 `[` `]` `(` `#` 标记或与 body 文本逐字相等者标记；重新 diff 主/对照 body 确认仍一致 |

验证要点：B1-B4 每批完成后重跑 `check.py`（含 B3 新增的 script 项）确认脚本层通过；B5 是独立于技能本体质量的实验资产问题，建议优先于任何一轮 Mode B 评测执行。

### 13.7 审查局限

- 本审查为静态文本审查：未执行真实 agent 任务，NEG-01 的虚构风险与 CF-01 的机械可测性均基于推理与语料库先例（112 的 PROC-05），其实际发生率需在评测运行中通过人工抽检 10% 校准（research design 既定的抽检流程）验证。
- 对照集扫描仅覆盖 113 一个技能，其余 321 个对照集 description 的损坏情况未逐一核查（已列入 P2-13 的整改范围）。
- 五维度评分沿用 dossier 的评估框架，权重为等权主观赋值，仅供排序参考，不构成正式测评结果。
- 全部 3 处 rubric 权重数值（1.4+1.3+1.2+1.3+1.1+1.2+1.1+1.0 = 9.6）与 SCORING total_items（13）已逐项复核，未发现其他 off-by-one 类计数错误。

### 13.8 修复后预期评级

按 B1-B4 全部落地评估本技能在五个维度上的预期提升：

| 维度 | 当前 | 修复后 | 依据 |
|------|:----:|:------:|------|
| 逻辑一致性 | 4.0 | 4.7 | P1-1/P1-2/P1-3 消除全部数字与边界问题后，象限几何、映射、示例贯穿无懈可击 |
| 语法与可读性 | 4.6 | 4.8 | P2-1 断句、P2-7 删重复标题、P3-1 压缩冗余 |
| 人机感 | 4.3 | 4.5 | P2-10 补交付边界说明后，单次 agent 执行路径完整 |
| 规范合规性 | 4.2 | 4.9 | P2-1/P2-2/P2-3 落地后九项合规清单全部显式通过，仅剩 name↔directory 前缀惯例的已知张力 |
| 评估体系 | 3.5 | 4.2 | P1-4/P2-5/P2-11/P2-12 落地后：无不可满足项、有机械层兜底、阈值与刻度对齐 |

届时 113 可从"🟢 良好（微调后可用）"升级为"🟢 范本级"，具备与 067-chronology、127-policy-redraft、139-clearance、212-written-consent 并列进入 dossier 典范名单的资格；其在"决策支持类技能"中的映射设计（评估项 ↔ 技能红标 ↔ rubric 锚点三方一致）可作为该类技能的评估模板。

### 13.9 一句话结论

内容底子好、示例贯穿与红标启发式是亮点，四个 P1 级问题（一处算术错误、边界未定义、分布不封闭、评估项不可满足）和一处对照集描述损坏是当下唯一需要动手的地方——全部为小时级改动，修复后即为语料库范本级。
