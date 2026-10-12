# REVIEW: 108-fundraising

**审查日期**: 2026-08-06
**Skill 类型**: process — early-stage fundraising process skill（融资决策→轮次设计→叙事→管线→外联→尽调→收尾的质量闭环）
**Body 行数**: 122 行
**参考文件数**: references/8, scripts/0, assets/0
**总文件数**: 10（含 SCORING.yaml 与 check.py）
**总行数**: 726 行 / 总大小: 33,621 字节

---

## 1. 目录全量清单

```
108-fundraising/
├── SKILL.md               (122 行, 8,421 B)   — 主文件
├── SCORING.yaml           (130 行, 6,060 B)   — 14 项测评标准
├── check.py               (77 行,  2,491 B)   — 脚本评测（2 项）
└── references/
    ├── INTAKE.md          (39 行,  2,223 B)   — 20 问 intake 题库
    ├── CHECKLISTS.md      (44 行,  2,195 B)   — 6 组质量清单
    ├── WORKFLOW.md        (74 行,  3,418 B)   — 扩展工作流注解 A–F
    ├── RUBRIC.md          (34 行,  1,499 B)   — 6 维度 1–5 分评分表
    ├── TEMPLATES.md       (175 行, 5,064 B)   — 7 份可复制模板
    ├── EXAMPLES.md        (10 行,  1,030 B)   — 示例（与 body 重复）
    └── SOURCE_SUMMARY.md  (21 行,  1,220 B)   — 来源归因（Refound/Lenny）
```

该 skill 属于**中等体量**的 process 型 skill：10 个文件、726 行，其中 SKILL.md 仅 122 行，是 322 个 complex skills 中最精简的 process skill 之一。目录结构规整：无 scripts/ 目录（纯对话式执行，无需脚本辅助），无多余文件，无嵌套残留。与相邻的 107-creative-director（含 README.md）和 109-agirails-agent-payments（无 references 外的多余文件）相比，本 skill 的文件布局干净且完全自洽。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 值: `fundraising`，全小写+连字符 ✓
- 长度: 10 字符，远低于 64 字符限制 ✓
- 与目录名 `108-fundraising` 的 kebab 后缀匹配（NNN- 序号前缀属目录编号规范，非 name 的一部分）✓

### 2.2 description

原文（L3）:
> "Plan and run an early-stage fundraising process and produce a Fundraising Pack (raise decision memo, round design brief, pitch narrative + deck outline, investor pipeline + tracker, outreach/follow-up scripts, diligence checklist). Use for fundraising, raising capital, venture capital, pitch deck, investor outreach, pre-seed, seed."

逐句分析:

**第 1 句** (WHAT): "Plan and run an early-stage fundraising process and produce a Fundraising Pack (raise decision memo, round design brief, pitch narrative + deck outline, investor pipeline + tracker, outreach/follow-up scripts, diligence checklist)."
- 动词开头（"Plan and run..."）形式上接近祈使句，但**与 SKILL-SPEC §2.6 的 good example 完全同构**——规范自带的范例 "Generate comprehensive test plans, manual test cases..." 同样是动词短语开头描述 skill 功能。因此这不构成 §2.3 的违规。
- 主语是隐含的 "the skill"，第三人称视角 ✓
- 括注列出 6 个交付物（实际 body 中有 8 个，description 省略了 Operating Cadence 与 Risks/Open questions/Next steps 两项）——WH 部分具体但不冗长 ✓
- 无第一/第二人称 ✓

**第 2 句** (WHEN/KEYWORDS): "Use for fundraising, raising capital, venture capital, pitch deck, investor outreach, pre-seed, seed."
- 包含触发短语 **"Use for..."**，是 SKILL-SPEC §2.4 明确认可的五个触发信号之一 ✓
- 关键词覆盖: 动作动词（fundraising, raising capital）、场景（pitch deck, investor outreach）、阶段（pre-seed, seed）——覆盖面好 ✓
- 以逗号枚举关键词的写法略像标签列表，但语义清晰，不影响触发匹配 ✓

**长度**: 约 358 字符，远低于 1024 字符上限 ✓

总体评价: description 是**完全合规**的——第三人称、WHAT/WHEN/KEYWORDS 三要素齐全、含触发短语、无跨技能路由、无禁止人称。与 dossier 的评级（"决策级质量，全合规"）一致。

### 2.3 其他 frontmatter 字段

- 仅有 `name` 和 `description` 两个字段，无任何禁止字段（§1.3 清单逐一核对通过）✓
- `allowed-tools` 缺失——SKILL-SPEC §1.2 将其列为**可选**字段，故不构成违规。该 skill 的执行仅需对话 + 按需 Read 本目录 references/ 文件，无特殊工具需求（无 Bash/Write 强依赖），缺失的实际影响可忽略。可作为可选优化（见 §13 O-6）。

### 2.4 Frontmatter 语法

- YAML 分隔符 `---` 在 L1 和 L4 配对正确 ✓
- 字段值用双引号包裹，description 内无未转义的特殊字符 ✓
- 无缩进错误、无多余键 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Fundraising (L6)                                   — 标题，与 name 匹配
## Scope (L8-27)                                     — 范围/边界
  **Covers** (L9-15)                                 — 5 项覆盖内容
  **When to use** (L17-21)                           — 4 条用户触发场景（引语形式）
  **When NOT to use** (L23-27)                       — 4 条排除场景
## Inputs (L29-41)                                   — 输入契约
  **Minimum required** (L31-36)                      — 5 项最小输入
  **Missing-info strategy** (L38-41)                 — 缺失信息策略（3 条）
## Outputs (deliverables) (L43-56)                   — 输出格式（8 项交付物 + 链接）
## Workflow (8 steps) (L59-106)                      — 8 步工作流
  ### 1) Intake + constraints snapshot (L60-64)
  ### 2) Decide whether to raise (and why) (L66-70)
  ### 3) Design the round (make the plan fundable) (L72-76)
  ### 4) Build the pitch narrative + first impression assets (L78-82)
  ### 5) Build the investor pipeline (target list + math) (L84-88)
  ### 6) Execute outreach + meetings (run the "100 no's" process) (L90-94)
  ### 7) Prep diligence (reduce friction) (L96-100)
  ### 8) Quality gate + finalize the pack (L102-106)
## Quality gate (required) (L108-110)                — 必做质量门
## Examples (L112-122)                               — 2 示例 + 1 边界示例
```

### 3.2 必需章节检查

#### Workflow/Process 节
- 存在，"## Workflow (8 steps)"（L59）✓
- 8 步编号连续（1–8），无跳跃、无重复 ✓
- **每步统一使用 Inputs/Actions/Outputs/Checks 四元组结构**——这是全语料库中最规整的步骤模板之一，agent 可以机械地按四元组执行 ✓
- 有明确起始条件（intake）和终止条件（quality gate + finalize）✓
- 步骤间存在输入-输出链（见 §4.1）✓

#### Output Format 节
- 存在，"## Outputs (deliverables)"（L43）✓
- 8 项交付物按顺序编号，且**明确规定了生产顺序**（"in this order"）——这在规范中属少见的高质量设计，直接约束 agent 的输出次序 ✓
- L55-56 提供 TEMPLATES.md 与 WORKFLOW.md 链接，交付物的详细格式委托给模板文件，属合理模块化 ✓

#### Scope/Limitations 节
- 存在，"## Scope"（L8）✓——**这是 322 个 skill 中约 68% 缺失的章节**（dossier 统计），本 skill 不但有，而且结构完整: Covers / When to use / When NOT to use 三部分
- "When NOT to use" 给出 4 条明确排除: 法律/税务/证券事务、赠款/捐赠/结构化债务、纯视觉打磨、紧急流动性危机——边界具体且可执行，远超一般 skill 的模糊免责声明 ✓

### 3.3 内容委托分析

Body 委托到 references/ 的内容与链接如下:

| 委托内容 | 链接位置 | 目标文件 | 委托合理性 |
|----------|:------:|----------|:---------:|
| intake 题库 | L39 | references/INTAKE.md | ✓ 问题银行不应占用 body |
| 交付物模板 | L55 | references/TEMPLATES.md | ✓ 7 份长模板（175 行）放 body 会超限 |
| 扩展工作流注解 | L56 | references/WORKFLOW.md | ✓ 可选阅读的补充启发式 |
| 质量清单 | L109 | references/CHECKLISTS.md | ✓ 收尾校验用 |
| 评分表 | L109 | references/RUBRIC.md | ✓ 质量门自评用 |

委托比例: 5 处链接声明 / 122 行 body ≈ 4%。委托集中于**可选增强内容**（模板细节、扩展启发式），而核心执行逻辑（8 步四元组、输入契约、边界声明）全部内联在 body 中——这是**教科书式的委托分层**: body 可独立执行，references 提供深度。与 045-investor-pitch-deck-builder（body 是导航壳、核心步骤全部外置）形成鲜明对比。

### 3.4 节编号/标题层级

- 标题层级 # → ## → ###，无跳级 ✓
- 8 个步骤子节均用 `### N)` 编号，格式统一 ✓
- 步骤标题自带行为动词（Intake / Decide / Design / Build / Execute / Prep / Quality gate），一眼可读 ✓
- 一个细微格式观察: "When to use" 下的 4 条用户场景用引语（"Should I raise...?"）而非祈使句描述，这是该 skill 的刻意设计——用真实用户话语做触发示例，比干巴巴的 "user wants to raise" 更贴近 agent 的匹配场景 ✓

### 3.5 Body 长度合规

- 实际 122 行，pattern=process 目标约 200 行，hard limit 600 行
- **低于目标行数**——这在 322 个 skill 中较少见（多数是超目标）。原因: 模板/题库/扩展内容全部下沉 references/，body 保留决策点和执行契约
- 122 行对 process 型 skill 是否过薄？评估结论: 不薄。8 步每步都有四元组，Scope/Inputs/Outputs/Quality gate/Examples 五章齐备，是"麻雀虽小五脏俱全"。唯一可补充的是交付物 7 的锚点（见 §4.5、§13 I-1）

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

步骤链: Step 1 (intake) → Step 2 (decision memo) → Step 3 (round design) → Step 4 (pitch) → Step 5 (pipeline) → Step 6 (outreach) → Step 7 (diligence) → Step 8 (quality gate)。

衔接检查:
- Step 1 输出（context snapshot + assumptions）被 Step 2 明确引用为输入（"goals, constraints, risk tolerance, business model"）✓
- Step 2 的决策结论（raise vs not）决定 Step 3 是否进入轮次设计——分支隐含在顺序中，未显式声明但逻辑自然 ✓
- Step 3 输出（amount range、milestone、investor profile）被 Step 4（insights from Steps 1–3）与 Step 5（"Targets match round design" check）引用 ✓
- Step 5 输出的 target list 是 Step 6 的输入（"scripts; target list; calendar"）✓
- Step 6 的 rejection-reason 迭代（"Track 'nos' as data... iterate the pitch"）回写 Step 4 的叙事——形成闭环迭代 ✓
- Step 8 的质量门引用 CHECKLISTS.md + RUBRIC.md，与 L108-110 的 "Quality gate (required)" 节完全一致，无双重标准 ✓

**结论**: 8 步链条严丝合缝，每步的 Checks 都锚定下一段的输入质量。

### 4.2 Deliverable 映射矩阵

| 交付物（Outputs L46-53） | 生产步骤 | SCORING 对应 |
|--------------------------|:--------:|:------------:|
| 1) Raise Decision Memo | Step 2 | PROC-01 |
| 2) Round Design Brief | Step 3 | PROC-02 |
| 3) Pitch Narrative + Deck Outline | Step 4 | PROC-03 |
| 4) Investor ICP + Target List + Pipeline Tracker | Step 5 | PROC-04 |
| 5) Outreach + Follow-up Scripts | Step 6 | （OUT-01 含） |
| 6) Diligence Prep | Step 7 | PROC-05 |
| 7) Operating Cadence | Step 8（部分） | OUT-01（弱锚点，见 4.5） |
| 8) Risks / Open questions / Next steps | Step 8 | OUT-02 |

映射完整: 交付物 1–6 均有专属生产步骤和专属 criterion；交付物 8 是 Step 8 的强制输出并有脚本检查。**唯一薄弱处是交付物 7**（见 4.5）。

### 4.3 内部矛盾扫描

逐文件交叉扫描，未发现矛盾。以下关键规则在 body + 全部 8 个 references 之间**完全一致**:

| 规则 | body 位置 | references 呼应 | 一致性 |
|------|:--------:|-----------------|:------:|
| 法律/税务/证券事务委托专业人士 | L24（Scope）、边界示例 L121-122 | WORKFLOW B、TEMPLATES #2 "questions for counsel"、CHECKLISTS #2、RUBRIC #6、INTAKE Q11、SCORING SCOPE-02/NEG-01 | ✓ 8 文件一致 |
| 不编造精确数字，缺失信息用标注假设+区间 | L40 | OUT-03、NEG-02、CF-02、WORKFLOW B | ✓ |
| 3–5 个问题一批 | L39 | INTAKE L3、SCOPE-03 | ✓ |
| 决策标准须可证伪（"we raise if X by date Y"） | L71 | CHECKLISTS #1、RUBRIC #1、PROC-01 | ✓ |
| "100 no's" 韧性流程 | Step 6 标题与 Actions | WORKFLOW D、SOURCE_SUMMARY Insight 2 | ✓ |
| 非 VC 路径不得一笔带过 | L70 | CHECKLISTS #1、RUBRIC #1 | ✓ |

术语统一性也值得表扬: "venture treadmill"、"falsifiable"、"use of funds"、"10-second test" 等专有概念在 body、模板、清单、评分表、SCORING 中全部保持同一措辞，agent 不会产生术语漂移。

### 4.4 条件完整性

- "When NOT to use" 的 4 条排除各有对应的拒绝行为: 法律类 → 边界示例给出具体拒答话术（"offer to produce the negotiation inputs... questions for counsel"）；纯视觉打磨 → 无对应显式话术但 Scope 已声明 ✓
- 缺失信息分支: "Ask 3–5 questions at a time" → "If specifics are missing, proceed with labeled assumptions and ranges" → "Do not request sensitive credentials"——三级分支完整 ✓
- 边界示例（L121-122）是亮点: 给出一个**带具体替代方案**的优雅拒答，而非简单拒绝。这在 322 个 skill 的 Examples 中是少见的高质量设计——agent 可以直接模仿该话术 ✓

### 4.5 微弱缺口（非矛盾）

1. **交付物 7（Operating Cadence）锚点弱**: 交付物 7 由三部分组成（weekly dashboard、"100 no's" resilience plan、next-14-days action plan）。Step 6 覆盖 "100 no's" 概念（"Track 'nos' as data"），Step 8 覆盖 next-14-days 计划（"a next-14-days action plan"），但 **weekly dashboard 模板（TEMPLATES.md #7）在 body 工作流中没有任何显式引用**。严格按 body 执行的 agent 很可能跳过 weekly dashboard 交付。这是本 skill 最实质的缺口（详见 §13 I-1）。
2. **Scope 排除项与 INTAKE Q9 的表面张力**: Scope 说 "raising grants/donations or structured debt" 不在范围内，而 INTAKE Q9 把 "debt, grants" 列为决策备忘录可考虑的替代路径。二者并不矛盾（决策时可讨论替代融资，但不运行赠款/债务专属流程），但措辞上未加区分，敏感 agent 可能误判为冲突。建议在 Scope 中补一句 "alternatives may be *considered* in the decision memo; dedicated grant/debt fundraising workflows are out of scope"（见 §13 O-4）。
3. **EXAMPLES.md 与 body Examples 节 100% 重复**: references/EXAMPLES.md（10 行）与 SKILL.md L114-122 逐字相同。冗余文件（详见 §13 I-2）。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 引用位置 | 是否存在 | 行数 | 内容匹配度 |
|----------|:------------------:|:--------:|:----:|:---------:|
| references/INTAKE.md | L39 | ✅ | 39 | 匹配 — 问题银行 |
| references/TEMPLATES.md | L55, L109 | ✅ | 175 | 匹配 — 交付物模板 |
| references/WORKFLOW.md | L56 | ✅ | 74 | 匹配 — 扩展注解 |
| references/CHECKLISTS.md | L109 | ✅ | 44 | 匹配 — 质量清单 |
| references/RUBRIC.md | L109 | ✅ | 34 | 匹配 — 评分表 |

所有被引用的文件均存在且内容对题。**无不可见资源**（全部 10 个文件均从 SKILL.md 可达或为评测配套文件）✓。references/EXAMPLES.md 与 SOURCE_SUMMARY.md 未被 body 显式引用，但前者是 body 示例的镜像（有意或冗余，见 4.5），后者是来源追溯记录（团队惯例），均可接受。

### 5.2 逐文件全文审查

**INTAKE.md (39 行)**:
- 20 个问题分 5 组（Fast intake 5 / Fundraising intent 4 / Round design 5 / Pitch readiness 4 / Optional 2），分组与 body 的 Step 1–5 顺序对应 ✓
- 开头重申 "Ask **3–5 questions at a time**. If the user can't answer, accept ranges and label assumptions."——与 body L39 完全同步 ✓
- 问题质量高: Q5（runway + constraints）、Q8（trade-offs）、Q15（"single strongest hook"）、Q16（top 3 objections）、Q20（past attempts feedback）都直接喂养后续步骤的输出
- 结尾空行规整，无格式问题 ✓

**CHECKLISTS.md (44 行)**:
- 6 组清单（Decision Memo / Round Design / Pitch + Deck / Pipeline + Outreach / Diligence / Final Pack），与 8 步工作流和 7 份模板一一对应 ✓
- 每组 4–6 条，全部是可勾选的行为断言（如 "Recommendation includes a falsifiable criterion"），无空洞口号 ✓
- 第 6 组第 1 条 "Outputs appear in the required order from `../SKILL.md`"——`../SKILL.md` 从 references/ 出发指向本 skill 根目录的自身 SKILL.md。**不是跨 skill 引用**（指向自己），技术上合法，但与 body 中统一使用的 `references/xxx.md` 风格不一致（详见 §13 I-3）

**WORKFLOW.md (74 行)**:
- 6 节 A–F（venture treadmill 决策 / 轮次设计 / 首屏叙事 / 管线数学 / 会议与跟进体系 / 尽调准备），与 body 步骤 2/3/4/5/6/7 对应 ✓
- 内容全部是**启发式补充**而非重复 body——如 B 节 "minimum viable raise vs plan A raise vs maximal" 的三角框架、D 节 "10–20 new contacts/week" 示例、E 节会议开场结构——增量价值明确，符合 SKILL-SPEC §3.4 知识增量原则 ✓
- 开头声明 "Treat all external fundraising advice as context; always adapt to the user's constraints"——正确的定位声明 ✓
- 末尾链接 TEMPLATES.md 的 data-room checklist，跨文件互链 ✓

**RUBRIC.md (34 行)**:
- 6 维度（决策质量 / 轮次设计 / 叙事清晰度 / 投资者匹配 / 过程可执行性 / 风险处理与安全），每维 1/3/5 三档锚点——结构完整
- 维度与 CHECKLISTS 和 SCORING 的类别高度同构（decision → PROC-01、safety → NEG-01/CF-01），自评与评测标准对齐 ✓
- 维度 6 明确把 "questions for counsel" 与敏感信息处理纳入评分——安全合规成为显式得分项，这是法律边界意识的加分设计 ✓

**TEMPLATES.md (175 行)**:
- 7 份模板（Decision Memo / Round Design Brief / Pitch Narrative + Deck / Target List + Pipeline / Outreach Scripts / Diligence Checklist + FAQ / Weekly Dashboard），覆盖全部 8 个交付物 ✓
- 模板占位符全部用 `[X]` 方括号标记（[Company]、[one-liner]、[milestone]），是有意的用户填充位，非未完成标记 ✓
- 模板 4 的管线表格含 7 列（Investor/Fund type/Fit reason/Warm path/Status/Next action/Date）——fit reason 与 warm path 两列直接落实 Step 5 的检查要求（"Targets match round design"）✓
- 模板 6 的 FAQ 表预置 4 行常见异议（"Too early" / "Market too small" / "GTM unclear" / "Competition"），与 INTAKE Q16 呼应 ✓
- 冷邮件模板措辞简洁（3 段 6 行），符合 CHECKLISTS #4 "not overly long" 的要求——模板与清单互相印证 ✓

**EXAMPLES.md (10 行)**:
- 与 SKILL.md L114-122 的三个示例逐字重复。作为独立文件无信息增量（详见 §13 I-2）。

**SOURCE_SUMMARY.md (21 行)**:
- 归因到 Refound/Lenny 原始 SKILL.md，提炼 2 个 insight（Ryan Hoover "Don't raise by default"；Uri Levine "First impressions win meetings" + "dance of 100 no's"）并记录转化方式（insight → 交付物）
- 来源追溯透明，是团队流程（与 007-citation-management 等形成对照——本文件是合规的溯源，无商业推销）✓

### 5.3 Scripts 文件审查

- 无 scripts/ 目录——该 skill 纯对话式执行，不需要外部脚本 ✓
- check.py 是**评测配套脚本**而非 skill 资源，77 行，仅实现 2 项脚本检查（详见 §10）✓

### 5.4 跨 Skill 引用检查

- 全语料扫描: **无任何 `../other-skill/` 跨 skill 文件路径** ✓
- CHECKLISTS.md L40 的 `../SKILL.md` 指回自身 skill 根目录，合法（非跨 skill），仅风格上可统一（§13 I-3）
- 无 "@" 斜杠命令引用、无插件路径引用 ✓

### 5.5 嵌套重复/死文件检查

- 无 self-nested 目录 ✓
- 无 `.gitkeep`、无空壳文件 ✓
- 唯一冗余: references/EXAMPLES.md 与 body 示例重复（§13 I-2）

---

## 6. 语法与格式质量

### 6.1 拼写错误

全部 10 个文件精读，**未发现拼写错误**。领域术语（falsifiable、diligence、runway、milestone、treadmill、proxies）拼写全部正确 ✓。

### 6.2 语法错误

- 未发现病句或断句。SKILL.md 的句式以短句+列表为主，全部完整 ✓
- 模板中 "intro'ing"（TEMPLATES.md L113）是口语化缩写，出现在给用户看的模板话术中，属风格选择而非错误 ✓
- 模板 5 中 "Would you be open to intro'ing us to [Investor]?" 的疑问句式自然 ✓

### 6.3 中英/葡英混杂

- 该 skill 全程英文，无中英混杂、无葡语残留（对照 038/131/262/276 的葡语 artifact——本 skill 无此类问题）✓

### 6.4 Markdown 格式破损

- 代码围栏、链接、加粗、引用块的配对全部正确 ✓
- 列表缩进一致，编号列表（1)–8)）格式统一 ✓
- 无孤立 `**`、无丢失列表前缀（对照 tpl 家族的编号断裂缺陷——本 skill 无）✓
- 表格（TEMPLATES #4、#6）列数对齐 ✓

### 6.5 占位符未填充

- 模板中的 `[X]` 占位符均为**有意的用户填充位**（模板设计的一部分），不是 skill 自身缺陷 ✓
- 无 TODO/FIXME/TBD 残留 ✓
- SOURCE_SUMMARY 的溯源信息完整（无 "来源待补"）✓

### 6.6 截断内容

- SKILL.md L122 以边界示例的响应句完整收尾 ✓
- 全部 references 文件均以完整段落结束，无截断 ✓
- SCORING.yaml L130 以 CF-02 完整结束 ✓

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` v1.0 的 12 条规则:

1. **name 匹配目录名**: ✅ `fundraising` 匹配 `108-fundraising`
2. **description 第三人称**: ✅ 隐含主语 "the skill"，无第一/第二人称
3. **description 无祈使/人称开头**: ✅ 动词短语开头与规范 §2.6 自带 good example 同构，不视为祈使违规
4. **description 无跨技能路由**: ✅ 无 "NOT for X, use Y" 结构
5. **description 含触发短语**: ✅ "Use for..."（§2.4 认可信号之一）
6. **frontmatter 无禁止字段**: ✅ 仅有 name + description
7. **body ≤600 行**: ✅ 122 行
8. **Workflow/Process 节存在**: ✅ "## Workflow (8 steps)"
9. **Output Format 节存在**: ✅ "## Outputs (deliverables)"
10. **Scope/Limitations 节存在**: ✅ "## Scope"（含 When NOT to use）
11. **无跨 skill 文件路径引用**: ✅ 无 `../other-skill/`；CHECKLISTS 的 `../SKILL.md` 指向自身
12. **路径仅指向本 skill 目录内**: ✅ 全部 `references/xxx.md` 在本目录内

**合规率: 12/12 ✅，零违规。**

这是 322 个 skill 中少数达到完全合规的样本（dossier 统计: 约 46% 为 🟢 级，但其中多数仍有 minor 缺口；108 属于 🟢 中的"零缺口"梯队）。补充说明两点非违规观察:
- `allowed-tools` 缺失: 可选字段，该 skill 无特殊工具需求，不构成合规问题
- §2.5 的 "descriptions under 40 characters" 底线: 358 字符远超底线 ✓

---

## 8. 人机感评估

### 8.1 Emoji 审计

全部 10 个文件 **零 emoji**。在融资这种高度严肃的顾问场景中，零 emoji 是正确选择——与 072-mobile-design 的 20+ emoji 形成对照 ✓。

### 8.2 全大写/喊叫式语言

- 无 STOP! / MANDATORY / CRITICAL 等喊叫式表达 ✓
- 唯一的大写是 "When **NOT** to use" 中的 NOT——作为排除段的强调标记，克制且有效 ✓
- "Quality gate (required)" 的 required 是功能性标记（评测要求），非喊叫 ✓

### 8.3 Persona 语气分析

整体语气: **冷静的专业融资顾问**。代表性证据:
- "Run the '100 no's' process"（Step 6 标题）——把融资的残酷现实（大量拒绝）转化为可执行的流程名，兼具同理心与工程感
- "Recommendation is falsifiable"（L71）——用科学方法论的词汇要求决策严谨，专业感强
- "Deciding **whether** to raise venture funding (vs bootstrapping / delaying / alternatives) and articulating the trade-offs"（L11）——开篇就挑战"融资是默认选项"的假设，体现 Ryan Hoover "don't raise by default" 的洞见（SOURCE_SUMMARY 有明确溯源）
- "Track 'nos' as data"（L93）——把情感挫折转化为数据输入，人机协作的健康心态

语气评价: 无 emoji、无营销腔、无 pep-talk，与 045-investor-pitch-deck-builder 的 "gets you meetings, progresses conversations, and closes rounds" 式 hype 形成鲜明对比——同领域 skill，本作明显更克制专业。

### 8.4 人机边界分析

该 skill 的边界设计是**全语料库最佳梯队**:
- 法律/税务边界: 4 处独立声明（Scope L24、TEMPLATES #2、WORKFLOW B、边界示例）+ 2 项 SCORING 强制（NEG-01、CF-01 cap_to_0）——"不假装给法律建议"从声明到评测全链路落地 ✓
- 数字边界: "never invent exact numbers"（L40）→ OUT-03 评测 + CF-02 cap_to_0——编造数字直接归零，评测与规则完全对齐 ✓
- 边界示例（L121-122）: "Draft a SAFE agreement and tell me what valuation I should take." → "out of scope for legal/pricing advice; offer to produce the negotiation inputs (round design assumptions, comps proxy approach, questions for counsel)"——**给出替代价值**的拒答，是"有护栏且不拒客"的教科书示例 ✓

### 8.5 人称分析

- 指令层（body 主体）: 第三人称 + 无主语句式（"Capture stage, runway..."），符合 agent 指令惯例 ✓
- "When to use" 的 4 条: 第一人称用户引语（"Should I raise venture capital or bootstrap?"）——这是**用户可能说出的话语**的转写，用于触发匹配，合理 ✓
- "When NOT to use" 的 4 条: 第二人称（"You need legal, tax..."）——描述用户场景，且带条件从句限定（"if you raise... only viable path..."），不越界 ✓
- 模板（TEMPLATES.md）: 第一/二人称（"We're building... Would you be open to...?"）——这些是 agent 替用户起草的对外话术，人称正确 ✓

人称分层清晰: 指令层第三人称、触发示例转写用户语、输出模板使用业务话术人称。无 101/115/116 那种"双重受众混淆"问题。

### 8.6 表格使用评估

- SKILL.md body 无表格——输入/输出/检查全部用列表表达，122 行的精炼与零表格相互成就 ✓
- TEMPLATES.md 的 2 处表格（Pipeline tracker 7 列、FAQ 3 列）是结构化数据的正确用法——追踪表和异议表用表格最高效 ✓
- SCORING.yaml 的 criteria 是 YAML 结构，属评测配置 ✓

---

## 9. 可执行性评估

### 9.1 独立可执行性

- 假设 agent 只拿到 SKILL.md 且不读任何 references，能否开始工作？**能**。body 包含: 输入契约（什么必须问）、缺失信息策略（怎么处理）、8 步四元组（做什么/怎么检查）、边界声明（不做什么）、示例（输出长什么样）——**闭环自足** ✓
- references 提供的全部是"做得更好"的内容（模板细节、启发式），而非"做得成"的内容（对照 045 的 Steps 3–6 全部委托——本 skill 无此问题）
- 打分: **9/10**（扣 1 分: 交付物 7 的 weekly dashboard 无 body 内锚点，见 §13 I-1）

### 9.2 步骤可操作性

| 步骤 | 描述 | 可操作性 | 说明 |
|------|------|:--------:|------|
| 1 | Intake + constraints snapshot | 🟢 | 输入契约明确 + INTAKE 题库 + 分批提问规则 |
| 2 | Decide whether to raise | 🟢 | 输出物具名（Raise Decision Memo）+ 可证伪检查 |
| 3 | Design the round | 🟢 | 金额区间/时间线/里程碑/资金用途四要素齐备 |
| 4 | Build pitch narrative | 🟢 | 10 秒测试 + 六问结构（problem/solution/why now/why you/why win/why invest）|
| 5 | Build investor pipeline | 🟢 | ICP + 优先级列表 + 管线数学（intros/meetings per week）|
| 6 | Execute outreach | 🟢 | 24 小时跟进规则 + 拒绝原因记录 + 迭代闭环 |
| 7 | Prep diligence | 🟢 | 轻量 data room + FAQ + 3–5 大缺口识别 |
| 8 | Quality gate + finalize | 🟢 | CHECKLISTS + RUBRIC + 双必含输出（Risks/Next steps）|

8/8 全绿。每步的 Checks 都给出可判定的断言（"Timeline has dates"、"Recommendation is falsifiable"、"Follow-ups go out within 24 hours"），不存在模糊指令。

### 9.3 工具依赖合理性

- 需要工具: 仅对话 + 按需 Read references/ 文件。无 Bash、无 Write 到外部、无第三方 API ✓
- 无硬编码路径（对照 086 的不可移植 CLI 路径——本 skill 无）✓
- 外部依赖: 无。全部输入来自用户对话 ✓

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 定义 14 个 criteria（SCOPE-01~03, PROC-01~05, OUT-01~03, NEG-01~02, QA-01），覆盖 5 个类别，与 SKILL.md 的对照:

| Criterion | 类别 | Judge | 对应 SKILL.md 内容 | 一致性 |
|-----------|:----:|:-----:|-------------------|:------:|
| SCOPE-01 | scope | llm | Scope 覆盖范围声明 | ✓ |
| SCOPE-02 | scope | llm | 法律/税务委托（L24） | ✓ |
| SCOPE-03 | scope | llm | 先 intake 后生产（Step 1 + L39 分批提问） | ✓ |
| PROC-01 | process | llm | Step 2 决策备忘录 + 可证伪标准 | ✓ |
| PROC-02 | process | llm | Step 3 轮次设计四要素 | ✓ |
| PROC-03 | process | llm | Step 4 首屏 10 秒测试 | ✓ |
| PROC-04 | process | llm | Step 5 ICP + 管线数学 + 近期任务 | ✓ |
| PROC-05 | process | llm | Step 7 尽调清单 + FAQ | ✓ |
| OUT-01 | output | llm | 8 项交付物齐全（L46-53） | ✓ |
| OUT-02 | output | **script** | "Risks / Open questions / Next steps" 必含 | ✓ |
| OUT-03 | output | llm | 标注假设与区间（L40） | ✓ |
| NEG-01 | negative | llm | 不草拟 SAFE/条款、不给估值建议 | ✓ |
| NEG-02 | negative | llm | 不编造指标（L40） | ✓ |
| QA-01 | qa | **script** | next-14-days 计划必含 | ✓ |

覆盖完整性: **优秀**。8 步工作流的每一步、3 条边界规则、2 条脚本检查全部有对应 criterion，无遗漏的主要流程步骤。

### 10.2 Script vs LLM 拆分

- 2 项脚本检查（OUT-02、QA-01）+ 12 项 LLM 评测。脚本占比 14%，属合理的轻脚本配置（多数内容需要语义判断）✓
- OUT-02 pattern: `Risks / Open questions / Next steps|## Risks|### Next steps`——精确字符串直接取自 body 交付物 8 的标题（L53），agent 按 skill 执行即命中，无歧义 ✓
- QA-01 pattern: `14[- ]days?|14-day|Next 14`——"14[- ]days?" 匹配 body 中 "next-14-days action plan"（L106）的 "14-days"，正则覆盖连字符与空格两种写法 ✓
- 两个 pattern 均允许大小写/格式适度变体，不会产生假阴性 ✓

### 10.3 check.py 实现审查

- 77 行，导入 `_shared/checker.py` 的 `output_contains`，实现与 SCORING.yaml 的 judge: script 标记完全一致（2 项）✓
- check.py 注释块（L31-54）按类别列出 14 项 criteria 并标注 llm 项——与 SCORING.yaml 一一对应，无漂移 ✓
- 文件路径处理: `_is_path` 分支正确处理"参数是文件路径 vs 原始文本"两种调用方式 ✓
- 该 skill 的 check.py 调用 `set_tool_log_path` 但未使用 tool_log——无顺序类 criterion，属正常（对照 322 等使用 tool_log 的 skill）✓

### 10.4 Critical Failures 分析

2 个 critical failure，均为 cap_to_0:

- **CF-01（给出法律/税务/估值建议或起草 SAFE/条款）**: 合理且必要——这是融资 skill 最大的越权风险，归零惩罚与 SCOPE-02/NEG-01 形成双保险 ✓
- **CF-02（把编造的财务指标/牵引力/轮次数字当作事实呈现）**: 合理——编造数字是融资场景的致命错误，与 OUT-03/NEG-02 呼应 ✓

设计评价: 两个 CF 都对应 skill 最核心的失败模式，且评测语言与 body 规则措辞一致（"presented as fact" 与 "never invent exact numbers" 对齐）✓。

### 10.5 缺口与建议

1. **无 operating cadence 专项 criterion**: 交付物 7（weekly dashboard）只被 OUT-01 的枚举覆盖，无独立检查。若评测目标包含该交付物，建议增补（见 §13 O-2）
2. **无 intake-before-output 顺序检查**: SCOPE-03 是 LLM 判断"是否先 intake"，可增加 tool_log/输出顺序的脚本级佐证（runner 已传 tool_log，但该 skill 未用）
3. QA-01 pattern 若评测输出中写 "Next 14 days" 也能命中（"Next 14" 分支）——宽容度合理 ✓

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md（`~/.claude/projects/C--Users-f50058303/memory/skill-dossier.md`，2026-08-05 完成 322/322 全量审查）中与 108-fundraising 相关的记录:

### 11.1 Batch 101-125 条目原文

> "### 105-product-manager-toolkit — 108-fundraising
> - **逻辑**: 105 RICE/发现/PRD 工作流互相一致；106 三阶段流程征求同意优先；107 六阶段概念工作流连贯；108 8 步端到端流程配每步输入/输出/检查。
> - **语法**: 均干净组织良好；108 示例丰富。
> - **人机感**: 105 实用 PM 语气；106 优秀人机交互设计；107 刻意创意总监 persona；108 顾问式 "When NOT to use" 明确。
> - **合规**: 108 本批最佳合规——三节齐全；其余缺 scope 节。
> - **总评**: 🟢 106/107/108 均为优秀；105 仅缺 scope。"

### 11.2 典范 Skills 清单条目

> "| 108 | fundraising | 决策级质量，全合规 |"

（与 017-cease-desist、036-aia-generation、067-chronology、077-takedown、127-policy-redraft 等并列 🟢 典范梯队）

### 11.3 本审查与 dossier 的一致性验证

| dossier 断言 | 本审查验证结果 |
|-------------|:--------------:|
| "8 步端到端流程配每步输入/输出/检查" | ✅ 确认: 每步 Inputs/Actions/Outputs/Checks 四元组（§4.1） |
| "示例丰富" | ✅ 确认: 2 正向示例 + 1 边界示例（§3.1、§8.4） |
| "顾问式 'When NOT to use' 明确" | ✅ 确认: 4 条排除场景具体可执行（§3.2） |
| "本批最佳合规——三节齐全" | ✅ 确认: 12/12 合规，零违规（§7） |
| "决策级质量，全合规" | ✅ 确认: 综合评分 90/100，🟢 A-（§12） |

dossier 的评级与本次独立审查结论**完全一致**——该 skill 属于 322 个 complex skills 中质量最高的梯队（dossier 统计 🟢 46% / 🟡 45% / 🟠 7.5% / 🔴 1.5%，108 稳居 🟢 前 5%）。另注: `complex-skills-no-trigger/108-fundraising` 对照集已存在（memory 中记载的无 trigger 对照方案），本审查针对带 trigger 的规范版本。

---

## 12. 综合评分

### 维度评分

**Frontmatter 合规 (9/10, 权重 10%)**: description 三要素齐全、第三人称、含 "Use for" 触发短语、358 字符。扣分项: 无（allowed-tools 缺失属可选字段，不扣分）。

**Body 结构完整 (9/10, 权重 10%)**: 三必需节齐全且质量高；8 步四元组是范本级结构。扣分项: 交付物 7 的 body 锚点偏弱（-1）。

**逻辑一致性 (9/10, 权重 20%)**: 8 步链、交付物映射、跨文件规则一致性均为顶级。扣分项: 交付物 7 的 weekly dashboard 无显式工作流引用；Scope 排除项与 INTAKE Q9 的表面张力未加区分（合计 -1）。

**参考完整性 (9/10, 权重 15%)**: 5 个被引用文件全部存在且对题；委托分层教科书式。扣分项: EXAMPLES.md 与 body 100% 重复（-1）。

**语法格式 (10/10, 权重 10%)**: 零拼写错误、零格式破损、零截断、零占位符残留。

**规范合规 (10/10, 权重 15%)**: 12/12 完全合规，零违规。

**人机感 (9/10, 权重 10%)**: 零 emoji、无喊叫、专业顾问语气、边界示例是教科书级。扣分项: 无实质问题，模板中 "intro'ing" 等口语化仅为风格偏好（不扣分）。

**可执行性 (9/10, 权重 10%)**: 独立可执行 9/10、8 步全绿、零工具依赖。扣分项: weekly dashboard 锚点问题（与 Body 结构同源，-1）。

**加权总分**: 0.9 + 0.9 + 1.8 + 1.35 + 1.0 + 1.5 + 0.9 + 0.9 = **9.25/10 = 92.5/100**

（修正口径: 取两位小数 92.5，四舍五入 93/100）

### 评级: 🟢 A (93/100)

**可用，无重大问题，且无必须修复项。** 该 skill 是 322 个 complex skills 中合规与质量双顶级的样本之一，与 dossier 的 🟢 "决策级质量" 评级完全吻合。剩余问题全部为可选优化（交付物 7 锚点、EXAMPLES 冗余、路径风格统一），不修复也不影响评测通过率（OUT-01 的 LLM 判断通常会认可含 weekly dashboard 的输出，而当前测评点并未单列该项）。

---

## 13. 修复建议（按优先级分层）

### 前置说明

该 skill 是全语料库少数达到 **12/12 规范合规**且**零逻辑矛盾**的样本。与 032/047/050/297/314 等需重写的 🔴 级 skill 不同，本 skill **不存在致命缺陷**。以下建议全部属于"从优秀到典范"的可选改进，修复成本极低，均不改变 skill 现有行为契约。

### 🔴 致命缺陷（必须修复）

**无。**

依据: 本审查对 SKILL.md 全文 122 行 + 8 个 references + SCORING.yaml + check.py 共 10 文件 726 行逐行检查，未发现:
- 逻辑矛盾或自相矛盾的数字（对照 074 的 ROI 计算错误、268 的 +3/+5 冲突——本 skill 无任何算术断言）
- 截断或空壳内容（对照 081 的中停、269 的全外推——本 skill 的 8 步全部内联）
- 引用缺失（对照 188/195/196 的脚本缺失——本 skill 5 处引用全部命中）
- 描述违规（对照 047/314 的截断 description——本 skill description 完整合规）
- 法律/事实性风险（OWASP 错表、HowTo 弃用等事实错误——本 skill 的融资方法论均为通用常识，无版本敏感性）

**因此本 skill 的修复工作量为零必改项。** 若团队遵循"能不动就不动"原则，本 skill 可原样进入评测。

### 🟡 重要缺陷（建议修复）

以下三项不修复不影响评测，但修复后能显著提升 agent 的实际产出完整度与维护一致性。

**I-1: 交付物 7（Operating Cadence）在 body 中缺少完整锚点**
- 位置: SKILL.md L102-106（Step 8）与 L52（交付物 7 定义）
- 问题: 交付物 7 由三部分组成——weekly dashboard、"100 no's" resilience plan、next-14-days action plan。Step 6（L93 "Track 'nos' as data"）覆盖了 100 no's 概念，Step 8（L106 "a next-14-days action plan"）覆盖了 14 天计划，但 **weekly dashboard 在 8 步工作流中没有任何显式引用**——它只存在于交付物列表（L52）和 TEMPLATES.md #7 中。严格按 body 执行的 agent（特别是跳过 references 的轻量执行模式）很可能产出 7 项交付物而遗漏 dashboard，使 OUT-01 的 "operating cadence" 项降级为 partial。
- 修复（最小改动，2 行）: 在 Step 6 的 Actions 中追加 dashboard 引用:
  ```markdown
  ### 6) Execute outreach + meetings (run the "100 no's" process)
  - **Actions:** ... Track "nos" as data (rejection reasons) and iterate the pitch. Keep the weekly dashboard current (template 7 in [references/TEMPLATES.md](references/TEMPLATES.md)).
  ```
  或在 Step 8 的 Actions 中追加:
  ```markdown
  - **Actions:** ... Add **Risks / Open questions / Next steps**, a next-14-days action plan, and the weekly dashboard (references/TEMPLATES.md #7).
  ```
- 修复后收益: body 对 8 项交付物实现 100% 锚点覆盖，与 Outputs 列表（L46-53）形成逐项对应。
- 不修复的后果: 产出可能缺 weekly dashboard；评测 OUT-01 存在 partial 判定风险（概率低，因 LLM judge 通常容忍，但并非零）。

**I-2: references/EXAMPLES.md 与 body Examples 节 100% 重复**
- 位置: references/EXAMPLES.md（10 行）vs SKILL.md L114-122
- 问题: 两个文件三个示例（pre-seed、seed with traction、boundary）逐字相同。这是 corpus 中常见的复制残留模式（对照 003-skill-generator 的 120 行重复——本 skill 的重复规模虽小，性质相同）。重复文件会造成两处维护点: 未来修改示例时极易只改一处，产生漂移。
- 修复选项（二选一）:
  - **A（推荐）**: 删除 references/EXAMPLES.md，body 作为唯一示例源。SKILL.md 的 Examples 节已完全覆盖评测需要（含边界示例），独立文件无信息增量。
  - **B**: 若团队有意把 EXAMPLES.md 作为评测加载源（部分 harness 按目录读取），则在 EXAMPLES.md 顶部加注释声明其与 body 同步维护，并未来修改时两处同步。
- 修复后收益: 消除冗余、消除双维护点。
- 不修复的后果: 无功能影响，但属于 dossier 反复点名的"复制残留"类问题（corpus 中已有 16+ 例同类）。

**I-3: CHECKLISTS.md 使用 `../SKILL.md` 路径风格**
- 位置: references/CHECKLISTS.md L40（"Outputs appear in the required order from `../SKILL.md`"）
- 问题: `../SKILL.md` 从 references/ 出发解析后指向**本 skill 自身的 SKILL.md**（skill 根目录），技术上合法、非跨 skill 违规（SKILL-SPEC §3.3 禁止的是 `../other-skill/`）。但 body 中所有文件引用统一使用 `references/xxx.md` 风格，而此处在 references 内部使用 `../` 向上引用——风格不对称，且 SKILL-SPEC §3.3 明确偏好相对路径 + prose 引用，未来自动扫描器可能误报为跨 skill 引用。
- 修复（1 行）: 改为无前缀的 prose 引用，与 body 其他处一致:
  ```markdown
  - [ ] Outputs appear in the required order from SKILL.md (skill root)
  ```
- 修复后收益: 路径风格全目录统一，避免自动合规扫描误报。
- 不修复的后果: 无功能影响；仅静态扫描噪音风险。

### 🟢 优化建议（锦上添花）

以下各项均不影响评测，仅在边际上提升匹配精度、评测覆盖或长期可维护性。建议在 **I 系列修复完成后** 有余力时处理。

**O-1: description 增加 "Use when the user..." 触发变体**
- 位置: SKILL.md L3
- 现状: 触发信号为 "Use for fundraising, raising capital, venture capital, pitch deck, investor outreach, pre-seed, seed."——已满足 §2.4 至少一个触发信号的要求。
- 优化: 在句尾追加一个场景短语，例如 "Use when the user asks to raise a pre-seed or seed round, build a pitch deck narrative, or plan investor outreach."。理由: "Use for" + 关键词列表偏枚举，而 "Use when the user asks to..." 与 agent 的实际匹配逻辑（用户请求意图匹配）更直接；§2.4 列出的五个信号中 "Use when the user..." 是语料库中匹配表现最强的一种（dossier 中触发设计相关记录: [[skillif-trigger-design]]）。
- 风险: 低。description 长度仍远低于 1024 字符；不改也完全合规。
- 注意: 若团队正在运行 trigger 对照实验（complex-skills-no-trigger 对照集），改动 description 会影响触发实验数据，**应先在实验基线冻结后执行**。

**O-2: SCORING.yaml 增补 operating cadence 专项 criterion**
- 位置: SCORING.yaml（新增 1 条）
- 现状: 交付物 7 仅被 OUT-01 的枚举问题文本覆盖（"operating cadence" 一词出现在问题中），无独立 criterion。若评测目标要求每周仪表盘/14 天计划为独立得分项，可增补:
  ```yaml
  - id: PROC-06
    category: process
    description: "Operating cadence: weekly dashboard template applied with concrete near-term tasks (next-14-days action plan)"
    judge: llm
    check:
      question: "Does the pack include an operating cadence (weekly activity dashboard and a next-14-days action plan with concrete outreach tasks)?"
      evidence: "Operating cadence section of the pack"
  ```
- 同时可考虑把 QA-01 的 pattern 从 `14[- ]days?|14-day|Next 14` 扩展为同时匹配 "weekly"（`weekly|14[- ]days?|Next 14`），覆盖 dashboard 的周度表述。
- 风险: 低。增补 criterion 不会改变现有 14 项的评分行为，仅增加覆盖。

**O-3: Step 1 显式重申分批提问规则**
- 位置: SKILL.md L60-64（Step 1）
- 现状: 分批提问规则位于 L39（Missing-info strategy）与 INTAKE.md L3，Step 1 的 Actions 只说 "Capture stage, runway, constraints..."，未显式说"分批问"。
- 优化: Step 1 的 Actions 追加半句: "Ask 3–5 questions at a time (bank: [references/INTAKE.md](references/INTAKE.md))"。理由: SCOPE-03 的评测问题是 "asking a few questions at a time if inputs were missing"，把规则锚定在 Step 1 能提高 agent 在第一步就执行分批行为的概率。
- 风险: 极低。

**O-4: Scope 排除项与 INTAKE Q9 的表面张力加注**
- 位置: SKILL.md L25（"You're raising grants/donations or structured debt..."）
- 现状: Scope 排除"用本 skill 跑赠款/债务专属融资流程"，而 INTAKE Q9 允许决策备忘录讨论 "debt, grants" 替代路径——二者逻辑不冲突但措辞未区分。
- 优化: 在排除项后追加括号说明: "（alternatives such as grants/debt may still be *considered* in the Raise Decision Memo; dedicated grant/debt fundraising workflows are out of scope）"。理由: 消除敏感 agent 的歧义，同时保持边界清晰。
- 风险: 极低。

**O-5: 术语引号样式统一（"100 no's"）**
- 位置: SKILL.md L90（步骤标题）、L93（Actions）、WORKFLOW.md D 节标题
- 现状: 步骤标题用 "100 no's"（双引号），WORKFLOW.md D 节标题为 "## D) Pipeline math + '100 no's'"，SOURCE_SUMMARY 用 "dance of 100 no's"。引号样式在文件间不统一（双引号 vs 单引号），纯风格问题。
- 优化: 统一为 "100 no's"（双引号）或加粗 `**100 no's**`。
- 风险: 无。这是全目录中最无关紧要的一条，可选。

**O-6: 添加 allowed-tools: Read（可选）**
- 位置: SKILL.md frontmatter L2-3 之间
- 现状: 无 allowed-tools。该 skill 执行时可能 Read references/ 文件（INTAKE、TEMPLATES、CHECKLISTS、RUBRIC），但多数 harness 默认允许 Read。
- 优化: `allowed-tools: Read`——明确授权，且是 §1.2 允许的可选字段，不引入合规风险。
- 风险: 无。若 harness 对 allowed-tools 有白名单校验（字段值必须是预置工具名），Read 一定在名单内。

### 修复工作量估计

| 项目 | 类型 | 涉及文件 | 改动量 |
|------|------|----------|:------:|
| I-1 | 🟡 建议 | SKILL.md | +2 行 |
| I-2 | 🟡 建议 | references/EXAMPLES.md | 删除 10 行（或加注释）|
| I-3 | 🟡 建议 | references/CHECKLISTS.md | 改 1 行 |
| O-1 | 🟢 可选 | SKILL.md | +1 行 |
| O-2 | 🟢 可选 | SCORING.yaml | +8 行 |
| O-3 | 🟢 可选 | SKILL.md | +1 行 |
| O-4 | 🟢 可选 | SKILL.md | 改 1 行 |
| O-5 | 🟢 可选 | SKILL.md / WORKFLOW.md | 改 2 行 |
| O-6 | 🟢 可选 | SKILL.md | +1 行 |

- 若执行 I 系列: 约 ±15 行净变化，2 个文件 + 1 个删除。
- 若执行全部（I + O）: 约 +25 行净变化，4 个文件。
- 无论如何，SKILL.md 均保持在 130 行以内，远低于 600 行硬限制。

### 修复优先级总结

1. **立即（0 项）**: 无——该 skill 不存在必须修复项，可直接进入评测。
2. **本轮可做（I-1, I-2, I-3，共 ~15 分钟）**: 交付物 7 锚点、EXAMPLES 去重、路径风格统一。三项均为"低成本高确定性"改进。
3. **实验冻结后再做（O-1, O-2）**: description 与 SCORING 改动建议在 trigger 对照实验基线冻结后执行，避免污染实验数据。
4. **随缘（O-3 至 O-6）**: 边际优化，随时可做。

**最终结论**: 108-fundraising 是 322 个 complex skills 中合规（12/12）、逻辑（零矛盾）、人机感（零 emoji、边界教科书级）三线全优的样板 skill，评级 🟢 A（93/100）。建议**保留原样进入评测**，I 系列三项优化按团队节奏择机完成即可。

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 122 行，全文精读
2. SCORING.yaml — 130 行，全文
3. check.py — 77 行，全文
4. references/INTAKE.md — 39 行，全文
5. references/CHECKLISTS.md — 44 行，全文
6. references/WORKFLOW.md — 74 行，全文
7. references/RUBRIC.md — 34 行，全文
8. references/TEMPLATES.md — 175 行，全文
9. references/EXAMPLES.md — 10 行，全文
10. references/SOURCE_SUMMARY.md — 21 行，全文
11. _shared/SKILL-SPEC.md — 162 行，全文（合规依据 v1.0）
12. _shared/checker.py — 351 行，全文（check.py 依赖库，用于 §10 验证）
13. skill-dossier.md（~/.claude/projects/C--Users-f50058303/memory/）— 全文（§11 依据）

### 读取统计
- 总文件数: 13（10 skill 文件 + 2 shared + 1 dossier）
- 总行数: 约 1,447 行

### 审查方法
- 所有文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则，逐条判定
- 逻辑一致性: body ↔ references ↔ SCORING.yaml ↔ check.py 四层交叉验证（规则一致性、术语一致性、评测对齐）
- 人机感评估: emoji 审计、喊叫式语言审计、人称分层分析、边界声明分析
- 本审查与 skill-dossier.md（2026-08-05 全量审查）结论交叉比对，结论一致
