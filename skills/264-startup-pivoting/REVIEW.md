# REVIEW: 264-startup-pivoting

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 初创公司/产品 Pivot 决策与执行（Pivot Decision & Execution Pack）
**判定基准**: SKILL-SPEC.md（编写规范）、skillif-research-design 的脚本/LLM 混合评分规范、全语料交叉引用核查

---

## 1. 审查概述

### 1.1 元信息

| 项目 | 内容 |
|------|------|
| 目录 | `264-startup-pivoting/` |
| 文件总数 | 10（1 个 SKILL.md + 1 个 SCORING.yaml + 1 个 check.py + 7 个 references） |
| 总行数 | 658 行 |
| Frontmatter name | `startup-pivoting`（小写+连字符，与目录名一致） |
| pattern | `process` |
| total_items | 17（4 scope + 7 process + 3 output + 2 negative + 1 qa + 3 critical_failures） |
| 内容主题 | 决定 pivot vs persevere vs shut down，产出 8 部分决策包 |
| 方法论来源 | Butterfield "exhaustion check" + Todd Jackson "10% vs 200% pivot"（见 SOURCE_SUMMARY.md） |

### 1.2 审查方法

1. 通读全部 10 个文件（无遗漏）；
2. 逐条核验 SKILL.md 中所有内部引用（`references/*.md`）与跨 skill 引用的存在性；
3. 逐项审查 SCORING.yaml 的 17 个检查项与 SKILL.md/WORKFLOW/CHECKLISTS/TEMPLATES 的内容映射；
4. 审查 check.py 的脚本可验证性与项目"脚本 ~36% / LLM ~64%"规范的符合度；
5. 全文检索 322 个 skill 语料，核查跨 skill 引用是否悬空。

### 1.3 总体结论

**🟢 A-（86/100）**。这是 322 个 skill 中规范化质量最高的样本之一：Scope/Inputs/Outputs/Workflow/Quality gate 五大章节齐备，7 步工作流与 7 个 PROC 评分项一一映射，所有内部引用有效，模板/清单/评分表三件套完整且互相咬合。主要扣分点集中在**可评测性**：check.py 是纯空壳（0 个 script 检查项，所有 17 项全推给 LLM 裁判），与项目"脚本 ~36%"的混合评分规范明显偏离；另有 1 处模板陷阱（选项表只有 3 行 vs 评分要求 4-8 项）、1 处复合评分问题、3 个悬空跨 skill 引用。

---

## 2. Frontmatter 分析

### 2.1 name

`startup-pivoting` — 小写+连字符、无空格、无大写，匹配目录名。✅ 符合 SKILL-SPEC 命名规范。

### 2.2 description（第 3 行，全文 340 字）

```
Decide whether/how to pivot a startup or product and produce a Pivot Decision &
Execution Pack (diagnosis, exhaustion check, pivot options map, pivot thesis +
metrics, validation plan, execution plan, decision memo). Use for "should we
pivot?", "stuck pre-PMF", "growth stalled", "change ICP", "reposition",
"major strategy reset".
```

| 规范要求 | 判定 | 说明 |
|----------|:----:|------|
| WHAT 明确 | ✅ | 第一句点明任务：决定是否/如何 pivot + 产出 Pivot Decision & Execution Pack |
| WHEN / trigger 信号 | ✅ | `Use for` + 6 个引号触发短语（"should we pivot?"、"stuck pre-PMF" 等），覆盖典型用户措辞，利于 Claude Code 等 harness 的触发匹配 |
| 第三人称 | ✅ | 祈使句已消除（"Decide..." 为动词开头但非指令式劝诱，属描述性表述） |
| 无跨 skill 路由 | ✅ | 未在 description 中做路由分发 |

**问题 1（轻微）**：括号内交付物清单与 SKILL.md 正文的 8 个交付物**不完全一致**——description 写的是 "diagnosis, exhaustion check, pivot options map, pivot thesis + metrics, validation plan, execution plan, decision memo"（7 项），而正文 8 项为 "context snapshot, stuck diagnosis, exhaustion check, pivot options map, pivot thesis + metrics, validation plan, execution plan, risks/open questions/next steps"。description 缺 **context snapshot**、多了 **decision memo**（decision memo 实际是 TEMPLATES.md 的第 9 号模板，不属于 8 个交付物之一）。语义偏差不大，但作为触发匹配文本，术语不齐会影响评分项证据对照。

**问题 2（轻微）**：description 偏长（340 字符）。对 Claude Code 这类按 description 匹配的 harness，长度本身不是缺陷（触发短语丰富是优点），但"交付物罗列"部分可以精简为 "produces a Pivot Decision & Execution Pack (8 sections)"。

---

## 3. 结构完整性分析

### 3.1 必需章节检查（对照 SKILL-SPEC）

| 章节 | 状态 | 说明 |
|------|:----:|------|
| Scope（Covers / When to use / When NOT to use） | ✅ | 三件套齐全，另有专门 "Human checkpoint (required)" 小节 |
| Inputs（Minimum required + Missing-info strategy） | ✅ | 5 项最小输入 + 缺失信息策略（≤5 个 intake 问题 + 2 个 scope 选项） |
| Outputs（deliverables） | ✅ | 8 个交付物逐条列出，附模板/工作流链接 |
| Workflow（步骤） | ✅ | 7 步，每步带 Inputs/Actions/Outputs/Checks 四要素 |
| Quality gate | ✅ | 单独成节（L104-106），与 Step 7 呼应 |
| Examples | ✅ | 2 个正向示例 + 1 个 boundary 示例 |

### 3.2 目录结构

```
264-startup-pivoting/
├── SKILL.md                       119 行
├── SCORING.yaml                   159 行
├── check.py                        59 行
└── references/
    ├── INTAKE.md                   31 行
    ├── WORKFLOW.md                 63 行
    ├── TEMPLATES.md               116 行
    ├── CHECKLISTS.md               42 行
    ├── RUBRIC.md                   40 行
    ├── EXAMPLES.md                 11 行
    └── SOURCE_SUMMARY.md           18 行
```

主文件 119 行，远低于 500 行拆分阈值；复杂内容正确下沉到 references/（7 个引用文件），SKILL.md 保持"导览 + 骨架"定位。这是规范化后 skill 的标准架构，符合项目"按需加载"的设计意图。

### 3.3 空表/占位检查

全文件扫描未发现空表。TEMPLATES.md 中所有表格均有表头且带示例行（`| A | | | | ... |` 之类占位行符合模板定位）。无 "TODO"、"TBD"、无占位符。

---

## 4. 引用完整性分析

### 4.1 内部引用（SKILL.md → references/）

| 引用位置 | 引用目标 | 存在性 |
|----------|----------|:------:|
| L41, L63 | `references/INTAKE.md` | ✅ |
| L57 | `references/TEMPLATES.md` | ✅ |
| L58 | `references/WORKFLOW.md` | ✅ |
| L100, L105 | `references/CHECKLISTS.md` | ✅ |
| L100, L105 | `references/RUBRIC.md` | ✅ |

5 处引用、2 个文件对象，全部有效。路径前缀统一（均带 `references/`），无 297-startup-idea-validation 那样的裸文件名引用问题。

### 4.2 孤立文件检查

| 文件 | 是否被任何文件引用 | 判定 |
|------|:----:|------|
| INTAKE.md | ✅ SKILL.md L41/L63 | 正常 |
| WORKFLOW.md | ✅ SKILL.md L58 | 正常 |
| TEMPLATES.md | ✅ SKILL.md L57、WORKFLOW 无 | 正常 |
| CHECKLISTS.md | ✅ SKILL.md L100/L105 | 正常 |
| RUBRIC.md | ✅ SKILL.md L100/L105 | 正常 |
| SOURCE_SUMMARY.md | ⚠️ 无直接引用 | 溯源文档，可接受 |
| **EXAMPLES.md** | ⚠️ **无任何文件引用** | **孤立文件**（见 4.4） |

### 4.3 跨 skill 引用（悬空检测）

SKILL.md "When NOT to use"（L23-26）以反引号引用 3 个其他 skill：

| 引用 | 全语料检索结果（322 skill 目录 + 全文 grep） |
|------|------|
| `problem-definition` | 🔴 不存在——全语料仅此一处提及 |
| `prioritizing-roadmap` | 🔴 不存在——全语料仅此一处提及 |
| `startup-ideation` | 🔴 不存在——全语料仅此一处提及 |

按 SKILL-SPEC §2.5，跨 skill 引用应采用散文式名称引用（本文件做到了），但**被引用的 skill 在语料中不存在**。agent 被指引"use `problem-definition`"时会找不到目标（这些 skill 可能存在于 Refound 原始包的更大语料中，但在本实验的 322 集内是死链）。参考规范化阶段"cross-skill ref 修复——agent 看到死链接"的处理先例，此处应标记为待修。

### 4.4 EXAMPLES.md 孤立 + 逐字重复

EXAMPLES.md（11 行）内容与 SKILL.md L110-117 的内联示例**逐字重复**（Example 1、Example 2、Boundary example 三例文本完全一致）。且 SKILL.md 未链接 EXAMPLES.md。后果：

- 双份维护源——修改一侧必然失同步；
- SKILL.md 加载时示例已内联，EXAMPLES.md 作为按需加载文件永远不会被引用，浪费一个文件槽位。

建议：SKILL.md 保留精简版示例（对 agent 主流程有提示价值），EXAMPLES.md 扩展为完整示例区并加引用链接，或删除 EXAMPLES.md。

---

## 5. 逐文件审查

### 5.1 SKILL.md（119 行）——主文件

质量很高，逐节点评：

| 小节 | 评价 |
|------|------|
| Scope/Covers | 3 个覆盖点准确概括技能能力边界 |
| When to use | 5 条，全部是真实用户原话，可直接作为 trigger 语料 |
| When NOT to use | 4 条排除边界，且每条都给了替代 skill 名（问题见 4.3）——这是防止 scope creep 的关键设计 |
| Human checkpoint | L28-29 单列"高利害决策必须人拍板"——对 pivot 类高利害决策是负责任的设计 |
| Inputs/Minimum required | 5 项最小输入定义清晰（产品、症状+证据、runway、约束、获胜理论） |
| Missing-info strategy | "≤5 个问题 + 2 个 scope 选项（60-90 分钟精简分析 vs 1-2 天完整包）"——有兜底不卡死 |
| Outputs | 8 个交付物逐条编号，与 TEMPLATES.md 9 个模板大体对应 |
| Workflow | 7 步，每步 Inputs/Actions/Outputs/Checks 四要素——规范化范本级写法 |
| Quality gate | 明确要求跑 CHECKLISTS + RUBRIC，强制 Risks/Open questions/Next steps |

**唯一语气瑕疵**：L116 boundary 示例说 "ask 3–5 intake questions"，而 L41 说 "up to 5"——同一技能内问题数上限表述不一致（3-5 vs 1-5）。

### 5.2 references/INTAKE.md（31 行）

12 个编号问题 + 4 条 optional 深潜项，分 5 组（快速 intake / 约束 / 已尝试（供 exhaustion check）/ 决策框架 / 深潜）。设计亮点：

- 明确"答不上就答 unknown，以显式假设继续"——缺失信息兜底与 SKILL.md 一致；
- 问题 8-9（已试过什么、剩下哪些非 pivot 杠杆）**直接喂给 Exhaustion Check**——intake → workflow 的数据流清晰；
- 问题 10（8-12 周内成功的定义）直接对接 Step 5 的 North Star + kill criteria。

**问题**：SKILL.md 说 "Ask up to 5 questions from INTAKE.md"，但 INTAKE.md 没有标记哪 5 个优先（Fast intake 组是 5 个，但文件内未显式写"缺信息时只问前 5 个"）。agent 可能任意挑 5 个，导致 exhaustion check 所需的"已尝试记录"（问题 8-9）被漏掉。建议在文件头加一行优先级说明。

### 5.3 references/WORKFLOW.md（63 行）

7 步扩展版，补充了 SKILL.md 没有的判定启发式。最有价值的 3 条：

1. **Demand vs execution 信号分离**（Step 2）——低留存=需求问题、高留存但获客难=执行问题，并有 "small cohort loves it → ICP/positioning/channel problem" 的速判规则；
2. **200% pivot 操作化定义**（Step 4）——"changes at least two of: problem, persona, product, positioning/package"，把模糊的 "meaningfully different" 变成可判定的标准；
3. **时间盒规则**（Step 3）——"非 pivot 杠杆能行就给它 2-3 周 + 可测目标，失败就停止争论"。

这些启发式恰好把评分项（PROC-02、PROC-04）从"怎么判"变成"怎么执行"——这是 WORKFLOW 文件存在的正确姿势。

### 5.4 references/TEMPLATES.md（116 行）

9 个模板覆盖 SKILL.md 的 8 个交付物 + 1 个决策备忘（template 9）。模板结构完整（选项表 9 列、验证计划表 7 列、exhaustion 表 5 列）。**关键缺陷（模板陷阱）**：

- **Template 4（Pivot options map）只有 3 行示例（A/B/C）**，而 SKILL.md Step 4 与 PROC-04 要求 **4-8 个选项**。模板跟随者大概率照抄 3 行 → 直接触发 PROC-04 失败。模板是最强的行为锚点，示例行数与硬性要求冲突是必须修的。

### 5.5 references/CHECKLISTS.md（42 行）

A-F 六张清单，与 SKILL.md 步骤 1:1 对应（A=intake、B=exhaustion、C=options、D=thesis+metrics、E=validation+execution、F=finalization）。质量高，其中：

- B 清单 "非 pivot 尝试按尝试质量而非'我们试过'评判" —— 对应 NEG-01 的判定锚点；
- E 清单 "至少一个 hard truth 测试（pre-sell/LOI/付费 waitlist）" —— 直接支撑 PROC-07。

**唯一不一致**：C 清单要求每个选项包含 "why it could win + what must be true + **biggest risks**" 三要素，而评分项 PROC-05 只查前两项（见 8.3）。

### 5.6 references/RUBRIC.md（40 行）

10 个维度 × 0/1/2 分，满分 20，及格线 ≥16/20。维度划分合理（决策框架/证据/诊断/Exhaustion 完整性/选项集/论题/指标门/验证计划/执行现实性/可分享性+安全）。与 SCORING.yaml 是**两套并行评分体系**：RUBRIC 供 agent 生成时自我评分（Step 7 要求），SCORING 供实验 runner 外部评测。机制自洽，但文件中未说明分工与换算关系——agent 自我评分 16/20 与外部 17 项二元分并无对应公式，若实验需要对齐会出偏差（轻微问题）。

### 5.7 references/EXAMPLES.md（11 行）

见 4.4——孤立 + 与 SKILL.md 逐字重复。且**只有文字性期望，没有一份填好的完整 Pivot Decision & Execution Pack 样例**。对 8 个交付物的复杂包，agent 需要的不是"期望列表"而是"完整成品长什么样"。这是示例资产最实质的缺口。

### 5.8 references/SOURCE_SUMMARY.md（18 行）

溯源文档，诚实标注假设：原技能引用 "The Four Ps" 但**未列举四 P 内容**，本包自行选取 Problem/Persona/Product/Positioning-Package 作为操作化分解。这种"来源模糊处显式声明"的做法符合规范化阶段对溯源的要求，避免把自选框架冒充原文献出处。内容上还需注意：经典 4P（Price/Product/Place/Promotion）与本包的 4P 不同源，若评测时对照原文可能被质疑，但文档已声明，无责。

### 5.9 SCORING.yaml（159 行）——见第 8 节

### 5.10 check.py（59 行）——见第 9 节

---

## 6. Workflow 逻辑一致性分析

### 6.1 步骤 ↔ 评分项映射

| SKILL.md 步骤 | 对应评分项 | 映射质量 |
|---------------|-----------|:-------:|
| Step 1 Frame the decision | PROC-01（二元+时间受限+owner+日期） | ✅ 1:1 |
| Step 2 Diagnose | PROC-02（signal vs execution + 1-3 瓶颈 + 证伪数据） | ✅ 1:1 |
| Step 3 Exhaustion check | PROC-03（杠杆清单+尝试质量+time-boxed 最后尝试） | ✅ 1:1 |
| Step 4 Generate options | PROC-04（4-8 选项 + 4P + 10%/200% + ≥1 个 200%） | ✅ 1:1 |
| Step 4 附带 | PROC-05（why win + what must be true） | ⚠️ 见 8.3 |
| Step 5 Select thesis | PROC-06（North Star + 2-5 领先指标 + 真 kill criteria + 日期） | ✅ 1:1 |
| Step 6 Validation + execution | PROC-07（sprint + 学习计划 + cut list + comms + 回滚 + hard-truth） | ⚠️ 复合项，见 8.2 |
| Step 7 Quality gate | OUT-01/02/03 | ✅ |
| Human checkpoint | SCOPE-04 | ✅ 三层布置（Scope L28 + Step 7 L100 + Checklist F） |

**7 步 ↔ 7 个 PROC 项一一对应**——这是全套语料中最干净的流程评分映射之一（对比 297-startup-idea-validation：步骤引用不存在的文件，评分项无对应）。

### 6.2 数据流完整性

```
INTAKE（12 问，含已尝试记录）
  → Step 1 上下文快照（owner + 决策日）
  → Step 2 诊断（信号/执行分离 + 证据缺口）
  → Step 3 Exhaustion Check（非 pivot 杠杆 × 尝试质量）
  → Step 4 4P 选项表（4-8 个 × 10%/200%）
  → Step 5 Thesis Card（可证伪信念陈述）
  → Step 6 验证+执行（硬事实测试 + cut list + 回滚）
  → Step 7 CHECKLISTS + RUBRIC + 风险/开放问题/下一步
```

每一步的输出恰好是下一步的输入，无断链、无循环依赖。WORKFLOW.md 的启发式在每个关键判定点提供判据（demand/execution 信号、200% 定义、时间盒规则、hard-truth 测试形式）。

### 6.3 决策框架完备性

- 决策空间显式包含三态：**pivot vs persevere vs shut down**（shut down 常被 pivot 类 skill 遗漏，此处覆盖）；
- 每个 pivot 选项必须可证伪（"what would have to be true"）；
- 指标体系分层：North Star（1）+ 领先指标（2-5）+ guardrails + kill criteria（带日期+行动）——层级完整；
- "10% pivot 陷阱"（Todd Jackson：换个壳不改变结果的伪 pivot）通过"至少 1 个 200% 选项"机制强制打破。

---

## 7. 交付物与模板体系审查

### 7.1 8 交付物 ↔ 9 模板对照

| # | SKILL.md 交付物 | TEMPLATES.md 模板 | 对应 |
|---|-----------------|-------------------|:----:|
| 1 | Context snapshot | 1) Context snapshot | ✅ |
| 2 | Stuck diagnosis | 2) Stuck diagnosis | ✅ |
| 3 | Exhaustion check | 3) Exhaustion Check | ✅ |
| 4 | Pivot options map | 4) Pivot options map (4P grid) | ✅ |
| 5 | Pivot thesis + metrics + kill criteria | 5) Thesis Card + 6) Metrics & kill criteria | ✅（1 个交付物拆 2 个模板） |
| 6 | Validation plan | 7) Validation plan | ✅ |
| 7 | Execution plan | 8) Pivot sprint execution plan | ✅ |
| 8 | Risks / Open questions / Next steps | 9) Decision memo 末尾小节 | ✅ |

结构上无缺口。TEMPLATES.md 的模板 9（决策备忘）把交付物 8 作为其收尾小节，逻辑自洽。

### 7.2 模板陷阱（已确认）

**Template 4 只有 3 个选项行（A/B/C），硬性要求是 4-8 个。** 机制分析：agent 复读模板时，"选项 A/B/C" 的三行结构是最强的格式锚点；SKILL.md Step 4 的 "Create 4–8 options" 是弱约束（散文指令）。弱约束 vs 强锚点冲突时，agent 大概率输出 3 个选项 → PROC-04 判失败。修复成本极低（模板加 2 行 + 表头加注），但影响一个完整评分项。

### 7.3 缺失：填好的完整示例 Pack

EXAMPLES.md 三例都是 "expected: ..." 式文字期望。对 8 个交付物的复杂产物，即使模板齐全，agent 对 "Exhaustion Check 表格填到什么颗粒度"、"kill criteria 怎么写才算 'real'" 仍缺乏体感参照。建议至少补一份覆盖 Example 1（B2B SaaS stuck pre-PMF）的完整成品样例（可直接放 EXAMPLES.md，并让 SKILL.md 链接过去）。

---

## 8. SCORING.yaml 评分体系审查

### 8.1 结构核查

| 项 | 值 | 核查 |
|----|----|:----:|
| total_items | 17 | ✅ 与实际条目一致（4+7+3+2+1，无 off-by-one） |
| 类别分布 | scope 4 / process 7 / output 3 / negative 2 / qa 1 | 符合 process 型 skill 的主流分布（process 占比 41%，项目均值 36.5%） |
| judge 分布 | llm 17 / script 0 | ⚠️ **全 LLM**，项目整体均值 script 36.1%——严重偏离（见第 9 节） |
| critical_failures | 3 个，全部 cap_to_0 | ✅ 数量在主流区间（2-3 个） |

### 8.2 检查项问题清单

| 检查项 | 问题 | 严重度 |
|--------|------|:------:|
| PROC-07 | **复合问题**：question 用 "and" 捆绑 6 个要求（时间盒 sprint、客户学习计划、cut list、comms 计划、回滚/退出计划、≥1 hard-truth 测试）。二元判定下，LLM 看到满足 5/6 大概率判 pass，任何单点缺失都会被吞掉；反之严格判 fail 又过于苛刻。判定不稳定 | 🔴 |
| SCOPE-02 | 双管问题："steer away from X... and instead treat it as Y (or redirect if...)"——"or redirect" 分支让否定情形也有通过路径，判定模糊 | 🟡 |
| PROC-05 | 只查 "why this could win" + "what would have to be true" 两项，而 CHECKLIST C 与模板要求每选项含 "biggest risks"（第三项）。评分项与质量门不一致——带 risks 的选项与不带 risks 的选项同样得分 | 🟡 |
| NEG-01 | 与 CF-01 行为高度重叠（无 exhaustion check 就推荐 pivot）。设计上可接受（同行为双重惩罚：NEG-01 扣一项分，CF-01 总分归零），但建议在注释中说明这是有意分层，避免审查时误判为冗余 | 🟢 |

### 8.3 检查项质量亮点

- 绝大多数 question 是**具体锚点式 yes/no**，无 weasel words（对照项目升级前的模糊描述，这批 question 是标杆）；
- evidence 字段指明判读位置（"Agent's first response"、"Agent's exhaustion check section"）——LLM 裁判不需要自行找证据；
- CF-01/02/03 均能从 SKILL.md 找到直接条款对应（Step 3/NEG-01、Step 1 Checks、Step 5 Checks），不是编造的禁止项；
- QA-01 的 boundary 场景在 SKILL.md L116-117 有明确的行为规定（"ask 3–5 intake questions, propose a discovery sprint, only then produce a thesis"）——评分项与内容条款对得上。

---

## 9. check.py 实现审查

### 9.1 现状：纯空壳

```python
def check(workspace, tool_log, agent_output) -> dict[str, bool]:
    """Run all 0 script checks. Returns {id: bool}. True = pass."""
    set_tool_log_path(tool_log)
    set_agent_output(agent_output)
    result = {}
    # ── SCOPE ──  # SCOPE-01..04: llm judge (not checked here)
    # ── PROCESS ──  # PROC-01..07: llm judge (not checked here)
    # ── OUTPUT ──  # OUT-01..03: llm judge (not checked here)
    # ── NEGATIVE ──  # NEG-01..02: llm judge (not checked here)
    # ── QA ──  # QA-01: llm judge (not checked here)
    return result
```

- `result` 恒为 `{}`，**17 项全部 0 script 可验证**，任何一次运行都输出空 JSON；
- `_shared/checker.py` 存在（import 不会崩），但 20 个公用函数一个未用（dead import）；
- `main()` 的用法分支（读 agent_output 文件）逻辑正确，但空结果让 runner 拿不到任何确定性证据。

### 9.2 与项目规范的偏离

按 skillif-research-design 的评分设计：脚本负责机械检查（~40% 分值）、LLM 负责语义判断（~60%）；322 个 skill 整体 judge 分布 script 36.1% / llm 63.9%。本 skill **0% script**，是所有 process 型 skill 中的异常值（008-tdd-workflow 为 14/20 script；典型 process skill 通常 5-8 项 script）。

后果有三：

1. **成本**：17 项全部走 LLM 裁判，同一输出评分成本 ≈ 全 script 型 skill 的 2-3 倍；
2. **方差**：无机械锚点，跨 harness 对比（2 Mode × 5 Harness 矩阵）时，差异将混入 LLM 裁判自身的不稳定性——违背"变量隔离"的实验原则；
3. **可复现性**：二元制设计（0/1 完全一致可复现）是本项目的方法论卖点，空壳 check.py 让 264 号 skill 完全放弃这一卖点。

### 9.3 可脚本化的候选检查项（4-6 项）

| 检查项 | 候选脚本逻辑 | 公共函数 |
|--------|--------------|----------|
| OUT-01 | agent 输出（或工作区文件）包含 "Risks"、"Open questions"、"Next steps" 三个标题 | `output_contains` ×3 |
| OUT-03 | 工具日志包含对 CHECKLISTS.md / RUBRIC.md 的 Read | `tool_log_contains` ×2 |
| PROC-01 | 输出包含日期模式（`\d{4}-\d{2}-\d{2}`）与 "decision owner/owner" 字样 | `output_contains` |
| PROC-04 | 输出中 "200%" 出现 ≥1 次 | `output_contains` |
| NEG-02 | 输出包含 "kill criteria" 与 "validation" 字样 | `output_contains` ×2 |

保守估计可把 judge 分布拉到 script 5-6 / llm 11-12（~30-35%），与项目均值对齐。需注意：脚本项只做"存在性"验证，语义质量仍由 LLM 把关——符合项目"脚本查有没有、LLM 评好不好"的分工。

---

## 10. 语言质量与人机感

### 10.1 语言质量

- 全英文书写，专业、精炼，无拼写/语法错误；
- 概念命名清晰且全文统一：Pivot Decision & Execution Pack、Exhaustion Check、4P pivot grid、Pivot Thesis Card、kill criteria、hard-truth test、cut list；
- 规则条文措辞可执行："Metrics are computable; kill criteria are real (not 'keep going until it works')"（L90）——既是检查项又是质量标准的写法；
- 表格全部格式正确（管道对齐、无断裂行），跨平台渲染无问题。

### 10.2 人机感（agent 视角）

| 维度 | 评价 |
|------|------|
| 指令清晰度 | 每步有 Actions + Checks，"Checks" 就是自评判据，agent 无需猜"做到什么程度算完成" |
| 决策压力管理 | 明确 "no vibes"、"no 'let's think about it'"、"not 'keep going until it works'"——把反模式显式化，agent 更容易避开 |
| 高利害处理 | Human checkpoint 三层布置（Scope/Step 7/Checklist F），SCOPE-04 单独验证——负责任 |
| 边界识别 | When NOT to use 4 条 + boundary 示例，防止 agent 越界硬上 |
| 术语一致性 | description 与正文 99% 一致（唯一出入见 2.2 问题 1） |

### 10.3 与相邻 skill 的关系定位

- 与 `206-lean-startup`（mindset，教科书式）形成鲜明对比——本 skill 是"知识 → 决策 → 交付物"的完整可执行链；
- 与 `297-startup-idea-validation`（GO/NO-GO 验证框架）在方法论上互补（验证阶梯 vs pivot 决策），本 skill 的引用策略（When NOT to use 指向 idea 验证类 skill）思路正确，但目标名悬空（见 4.3）。

---

## 11. 问题清单（按严重度）

### 🔴 严重（3 项——影响评测有效性的硬伤）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| 1 | **check.py 纯空壳**：0 个 script 检查项，result 恒为 {}，17 项全推 LLM | check.py | 评分成本高、跨 harness 对比混入裁判方差、放弃二元可复现设计 |
| 2 | **模板陷阱**：Pivot options map 模板仅 3 行（A/B/C），硬性要求 4-8 个选项 | TEMPLATES.md L44-46 vs SKILL.md L82 / PROC-04 | 模板跟随者输出不足 4 个选项 → PROC-04 必然失败，评分分不清"agent 不遵从"还是"模板误导" |
| 3 | **PROC-07 复合问题**：一个 yes/no 捆绑 6 个要求 | SCORING.yaml L93 | 二元判定不可靠，任何子项缺失都会被吞 |

### 🟡 中等（5 项——影响资产质量与判定精度）

| # | 问题 | 位置 |
|---|------|------|
| 4 | 跨 skill 引用悬空 ×3：`problem-definition` / `prioritizing-roadmap` / `startup-ideation` 在 322 集语料中不存在 | SKILL.md L23-26 |
| 5 | EXAMPLES.md 孤立且与 SKILL.md 内联示例逐字重复（双维护源） | EXAMPLES.md vs SKILL.md L110-117 |
| 6 | 无填好的完整示例 Pack（只有文字期望） | EXAMPLES.md |
| 7 | PROC-05 只查 "why win + what must be true"，漏模板/CHECKLIST C 要求的 "biggest risks" | SCORING.yaml L77 |
| 8 | description 交付物清单与正文 8 项不一致（缺 context snapshot、多 decision memo） | SKILL.md L3 |

### 🟢 轻微（4 项）

| # | 问题 | 位置 |
|---|------|------|
| 9 | intake 问题数上限表述不一致："up to 5" vs "3–5" | SKILL.md L41 vs L117 |
| 10 | NEG-01 与 CF-01 行为重叠，未注明分层设计意图 | SCORING.yaml L127/L149 |
| 11 | RUBRIC（连续 0-2 分，≥16/20）与 SCORING（二元 0/1）两套体系并行，分工与换算未说明 | RUBRIC.md vs SCORING.yaml |
| 12 | INTAKE.md 未标记"缺信息时优先问哪 5 个"（Fast intake 组未显式对接 L41 的 up to 5） | INTAKE.md |
| 13 | check.py 的 `_shared.checker` import 未使用（dead import，无实害） | check.py L11 |

---

## 12. 总体评分

| 维度 | 评分 | 说明 |
|------|:----:|------|
| Frontmatter 合规 | 9/10 | name/description 规范；交付物清单与正文小出入 |
| 结构完整度 | 10/10 | Scope/Inputs/Outputs/Workflow/Quality gate/Examples 全部齐备，无空表无占位 |
| 引用完整性 | 7/10 | 内部引用 5/5 有效；EXAMPLES.md 孤立；3 个跨 skill 引用悬空 |
| 逻辑一致性 | 9/10 | 7 步 ↔ 7 个 PROC 项 1:1 映射，数据流无断链 |
| 模板体系 | 8/10 | 9 个模板完整；选项表 3 行 vs 4-8 项要求的模板陷阱 |
| 示例资产 | 5/10 | 孤立 + 重复 + 无完整成品样例 |
| 评分体系设计 | 8/10 | 17 项结构与 CF 设计优秀；PROC-07 复合、PROC-05 覆盖缺口 |
| 检测器实现 | 4/10 | check.py 纯空壳，0 script 项，偏离项目混合规范 |
| 语言质量 | 9/10 | 专业精炼，术语统一，反模式显式化 |
| 可执行性（agent 遵从视角） | 9/10 | 模板+清单+启发式齐全，agent 可直接执行全流程 |

**综合：🟢 A-（86/100）**

结论：内容资产属于 322 集中最顶级的 10%——几乎每一条评分项都能回溯到 SKILL.md 的明确条款，内部引用零失效，方法论（Butterfield/Todd Jackson）溯源诚实。**唯一实质短板在评测基础设施**：check.py 空壳使本 skill 在 5 harness × 2 mode 实验中的测量可信度低于其内容质量。修复严重问题 1-3 后可升至 A+。

---

## 13. 修复建议（按优先级）

### P0（跑评测前必须修）

1. **实现 check.py 的 4-6 个 script 检查项**（按 9.3 候选表）：OUT-01 三标题存在性、OUT-03 工具日志 Read 记录、PROC-01 日期/owner 模式、PROC-04 "200%" 出现、NEG-02 关键词。目标 judge 分布 script 5-6 / llm 11-12（~30-35%），对齐项目均值。注意：修改后 SCORING.yaml 的 judge 字段需同步翻转，保证 322 集审计口径（result key ↔ SCORING 全匹配）不被破坏。
2. **修模板陷阱**：TEMPLATES.md 选项表扩为 5 行（A-E），表头下加注 "至少 4 个选项，其中 ≥1 个为 200% pivot"——把硬性要求写进模板本身。
3. **拆 PROC-07**：拆为 PROC-07（sprint + 学习计划 + cut list + comms + 回滚的包结构完整）与 PROC-07b（至少 1 个 hard-truth 测试），total_items 改为 18，或在 question 中改为分句判定（"包含 A 且 B 且 C..."按子句分别回答）。

### P1（本轮打磨）

4. **修悬空跨 skill 引用**：确认 `problem-definition` / `prioritizing-roadmap` / `startup-ideation` 是否在 Refound 原始包存在——存在则补路径说明，不存在则改为散文描述（"另一套问题定义类 skill"）或删除反引号引用，避免 agent 死链。
5. **单一化示例**：SKILL.md 保留精简示例，EXAMPLES.md 扩展为完整版并加 `Examples: [references/EXAMPLES.md](references/EXAMPLES.md)` 链接。
6. **补一份完整示例 Pack**：以 Example 1 场景生成填好的 8 部分决策包，放入 EXAMPLES.md——这是对 agent 遵从度提升最直接的资产。
7. **PROC-05 补 risks 项**：question 增加 "以及 biggest risks"，与 CHECKLIST C、模板第 9 列对齐。
8. **description 与正文对齐**：8 项交付物按 SKILL.md 原样列入 description（或精简为 "produces a Pivot Decision & Execution Pack (8 sections)"）。

### P2（可选优化）

9. 统一 intake 问题数表述（up to 5）；INTAKE.md 加"缺信息时优先 Fast intake 5 问"的注释。
10. SCORING.yaml 加注释说明 NEG-01/CF-01 的分层设计。
11. 在 RUBRIC.md 或 SKILL.md 补一句两套评分体系的分工说明（RUBRIC 用于生成期自我质量门，SCORING 用于实验期外部评测）。
12. 清理 check.py dead import（若不实现脚本项则一并处理）。

---

## 变更记录
- 2026-08-06: 初始深度审查（10 文件全读）。结论 🟢 A- (86/100)。内容资产顶级，评测基础设施（check.py）是唯一硬伤；发现 1 处模板陷阱与 3 处悬空跨 skill 引用。
