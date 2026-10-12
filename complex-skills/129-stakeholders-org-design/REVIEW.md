# REVIEW: 129-stakeholders-org-design

**审查日期**: 2026-08-06
**Skill 类型**: process — 组织设计与利益相关者映射（power-interest 矩阵、Conway's Law 团队对齐、团队接口契约、能力成熟度评估、转型治理）
**Body 行数**: 256 行（≤600 上限）
**参考文件数**: references/2 (methodology.md 457 行, template.md 396 行), scripts/0, assets/0, 其他/3 (SCORING.yaml 122 行, check.py 68 行, resources/evaluators/rubric_stakeholders_org_design.json 206 行)
**文件总数**: 6 个文件，共 1505 行

---

## 1. 目录全量清单 (tree, every file + line count)

```
129-stakeholders-org-design/
├── SKILL.md                                    # 256 行 — 主体：5 步工作流 + 四框架 + 护栏
├── SCORING.yaml                                # 122 行 — 13 项评分标准 (3 scope / 4 process / 3 output / 2 negative / 1 qa) + 2 项 critical failure
├── check.py                                    # 68 行 — 评估检查脚本（全部委托 LLM judge，恒返回空 dict）
└── resources/
    ├── methodology.md                          # 457 行 — 进阶方法论：Conway's Law、Team Topologies、DDD、变革管理
    ├── template.md                             # 396 行 — 填空式交付模板（五节 + 质量清单）
    └── evaluators/
        └── rubric_stakeholders_org_design.json # 206 行 — 8 维度评估量表 + 分规模/分场景 guidance + 7 种失败模式
```

引用关系核对（全部指向真实存在文件）：
- SKILL.md:90 → `resources/template.md` ✓ 存在
- SKILL.md:90 → `resources/methodology.md` ✓ 存在
- SKILL.md:102 → `resources/evaluators/rubric_stakeholders_org_design.json` ✓ 存在
- check.py:11 → `../_shared/checker.py` ✓ 存在（`set_tool_log_path` / `set_agent_output` 均已在库中定义，import 可解析）
- 无 scripts/、assets/ 目录；无跨 skill 文件路径引用 ✓

**总体判断（先行结论）**: 这是一个内容扎实、结构完整的 process 类 skill。五步工作流（映射 → 定团队 → 接口 → 成熟度 → 转型计划）在 SKILL.md、template.md、SCORING.yaml、rubric 四层之间保持高度一致，评分体系设计认真。主要问题集中在：① 主体缺 Scope/Limitations 与 Output Format 两个必需节（与 skill-dossier 中 "129 🟡 缺 scope 或 output" 的记录吻合）；② 旗舰示例中存在一处方向性数据错误；③ SKILL.md 的护栏与 methodology.md 的推荐值存在团队规模冲突；④ 评分体系内部有 3.5 门槛与 rubric guidance 的张力。评级：🟡 可用但需小修。

---

## 2. Frontmatter 与 Description 合规性

**合规（无问题）**。description（SKILL.md:3）为第三人称叙述，包含 WHEN（"Use when designing organizational structure... assessing capability maturity..."）、WHAT（"Organizational design and stakeholder mapping methodology"）与触发关键词（"org design", "team structure", "stakeholder map", "team interfaces", "capability maturity", "Conway's Law", "RACI"），符合 SKILL-SPEC 的 description 规范：无第一人称、无祈使句、无跨 skill 路由。body 256 行远低于 600 行上限。name 与目录名一致。frontmatter 无多余字段。

唯一可吹毛求疵处：description 长度约 600 字符，触发词列表偏长，其中 "Conway's Law" 与 "RACI" 两个关键词在 When to Use 的 "User phrases that trigger this skill"（SKILL.md:36-43）中再次重复——双处维护同一份触发清单，未来增删触发词时存在失同步风险（本次审查两处一致，暂无实际错误）。

---

## 3. 必需节检查：缺 Scope/Limitations 节（🟡 主要发现 #1）

SKILL.md 有 Purpose（:20）、When to Use（:24）、Workflow（:71）等节，但**没有任何 Scope/Limitations 或 When NOT to Use 节**。与之形成对照的是，SCORING.yaml 的 SCOPE-03（SCORING.yaml:23-29）明确设定了边界："Skill not used for unrelated work (individual performance, pure product strategy)"——即评分体系知道这个 skill 不该干什么，但 skill 本身从未告诉 agent 这一点。agent 只能靠自己的判断避免把绩效评估、纯产品战略之类的话题套进组织设计框架，而这个边界恰恰是评分项。

现存最接近的替代品是 Guardrails 节（SKILL.md:198-237），但那是**设计规则**（Conway's Law 不可避免、团队规模上限、认知负载、接口归属、避免矩阵地狱、成熟度评估要有证据），不是**使用边界**（何时不调用本 skill）。两者功能不同，不能互相顶替。

修复建议（见 §13 🟡-1）：新增 "## Scope & Limitations" 节，明确排除：
- 个体绩效评估、个人发展计划、薪酬与职级设计（组织层面的职级体系不在此列）
- 纯产品战略/市场策略（不涉及团队结构的）
- 招聘计划、预算编制（可作为 transition plan 的输入，但不是主产出）
- 企业文化与价值观变革（可用 Kotter 框架，但文化本身就是主题时另用专门的 skill）
- 法律合规审查（裁员、工会、劳动法——需法务参与）

---

## 4. 必需节检查：缺显式 Output Format 节（🟡 主要发现 #2）

与第 3 节同源。SKILL.md 的 5 步工作流各步骤有动作描述，Step 5（:100-102）甚至给出了质量门槛（"Self-check using ... rubric ... Minimum standard: Average score ≥ 3.5"），但**全篇没有一句说明最终交付物是什么、长什么样**。模板文件 template.md 实质承担了输出格式职责，但 SKILL.md:90 的 Step 2 只把它路由给"straightforward restructuring"场景——复杂场景走 methodology.md（无输出模板），此时 agent 完全没有输出结构约束。这意味着：

1. 复杂场景下两个 agent 可能产出格式迥异、结构不可比的结果；
2. SCORING.yaml 的 OUT-01/02/03 与 QA-01 都在评"agent 的响应是否包含 X"，但 skill 没有显式告知 agent 必须包含 X。

修复建议（见 §13 🟡-2）：在 Workflow 之后加 "## Output Format" 节，声明交付物为"组织设计备忘录"，必须包含五个板块（stakeholder map / team structure / interface contracts / maturity assessment / transition plan），并说明简单场景按 template.md 填充、复杂场景至少按五个板块组织输出。这一行说明能把 body、template、rubric 三者的隐含契约显式化。

---

## 5. 逻辑一致性：示例数据错误与内部冲突

### 5.1 旗舰示例的方向性错误（SKILL.md:66）

"What Is It" 节的 Quick example 中，DORA 指标示例：

```
Deployment frequency: Daily → Weekly (target: Daily)
```

**当前状态是 Daily，目标也是 Daily，箭头却指向 Weekly**——这是一个向**更差**方向的迁移，与同表其余三行（Lead time 1 week → 2 days、MTTR 4h → 1h、CFR 15% → 5%，全部是改善方向）方向相反。这个示例位于 skill 最显眼的位置（正文第三个区块），是 agent 学到的第一个带数字的模式样例，示例自相矛盾会直接污染 agent 对"现状→目标"格式的理解。应为 `Weekly → Daily (target: Daily)`。属一行修复，但性质上是真实的数据/逻辑错误。

### 5.2 团队规模护栏与 methodology.md 推荐值冲突

SKILL.md Guardrails（:205-209）声明：
- 2-pizza: 5-9 人
- **太小 (<3): 脆弱，缺乏技能多样性**
- **太大 (>12): 沟通开销，子群形成**

而 methodology.md 的 Team Topologies 节推荐：
- Platform Team 尺寸 **"Larger (10-15 people)"**（methodology.md:104）——10-15 人整体超出 ">12 过大" 护栏，其中 13-15 人区间与护栏直接矛盾；
- Enabling Team 尺寸 **"Small (2-5 people)"**（methodology.md:110）——2 人团队低于 "<3 脆弱" 下限；
- Complicated-Subsystem **"Small (3-8 people)"**（methodology.md:116）——与护栏兼容，无问题。

rubric 的量表（rubric JSON:31）同样声明 "team sizes unrealistic (<3 or >15)"。于是出现三方矛盾：**方法论推荐 2 人 enabling 团队，护栏说 <3 脆弱，rubric 说 <3 不现实**——同一 skill 家族内部对"最小合理团队规模"有三种说法。platform 的 10-15 人同理。修复方向不是抹平数字，而是明确"护栏 5-9 针对 stream-aligned 主团队，enabling 2-5 与 platform 10-15 是特例且需有理由"——rubric scale-3 其实已经表达了这种宽容（"team sizes mostly 5-12"），把这条解释写进 Guardrails 即可。

### 5.3 DACI vs RAPID 只定义了一半（SKILL.md:250）

Quick Reference 写 "decision rights (DACI/RAPID)"，正文只有 DACI 的定义（:142-145），**RAPID 从未定义**。RAPID 是 Bain 的决策权框架（Recommend/Agree/Perform/Input/Decide），与 DACI 是平行的替代框架，不是同义词。既然 rubric 与 SCORING 全部基于 DACI 词汇（"exactly one Approver"），Quick Reference 里出现的裸 RAPID 只会让 agent 困惑或产出评分体系不认识的术语。建议：要么在 Decision Rights 小节补 RAPID 一句话定义，要么从 Quick Reference 删掉。

### 5.4 五步工作流的一致性（正面确认）

SKILL.md:75-82 的 5 步 checklist、Quick Reference 的 "5-Step Process"（:246）、template.md:7-14 的 5 步 checklist 三者完全一致（Map → Define → Specify → Assess → Transition），无漂移。SCORING.yaml 的 PROC-01~04、OUT-01~03 也与这五步一一对应（PROC-01=step1 映射、PROC-02=step1 RACI、PROC-03=step3 接口、PROC-04=step4 成熟度、OUT-01=step2 Conway 对齐、OUT-02=step5 转型、OUT-03=step2 规模/负载）。评分体系与工作流的咬合是本 skill 最扎实的部分。

### 5.5 双工作流的关系未显式化（小问题）

SKILL.md 的 5 步流程与 methodology.md 的 "Advanced Org Design Progress" 5 步（methodology.md:5-12：Conway 分析 → Topologies → DDD → 高级利益相关者 → 变革模式）是两套不同结构的流程。SKILL.md:90 只说"复杂场景用 methodology"，没有说明两套流程如何衔接（例如：进阶流程中并无显式的成熟度评估与转型治理步骤，而主流程第 4、5 步要求这两项）。衔接规则缺失导致复杂场景下 agent 可能跳过 SCOPE/PROC/OUT 要求的评估与治理产出。建议在 Step 2 处补一句衔接说明。

---

## 6. 内容准确性核查

### 6.1 DORA 指标表使用 2019 年版阈值（SKILL.md:151-156，template.md:249-254 同步）

SKILL.md 的 DORA 四级表：Elite 档 Lead Time `<1 hour`、CFR `0-15%`；High 档 CFR `16-30%`。经与当前 DORA 官方基准（2024 State of DevOps 报告）核对：

| 指标 | 表中 Elite（skill 用） | 2024 官方 Elite |
|------|----------------------|-----------------|
| Deployment Frequency | Multiple/day | On-demand (multiple/day) ✓ |
| Lead Time | <1 hour | **<1 day**（官方基准已放宽） |
| MTTR | <1 hour | <1 hour ✓ |
| Change Failure Rate | 0-15% | **~5%**（官方已收紧） |

skill 使用的是 2019 Accelerate 报告的阈值。对"内容准确性"要求高的测评场景（尤其 PROC-04/QA-01 会评"evidence-based maturity"），过时基准会让 agent 产出与 2024 官方口径不符的评估结论。建议二选一：更新为 2024 阈值并注明报告年份，或保留 2019 经典阈值但显式标注 "classic/2019 thresholds"。

（核查来源：2024 DORA State of DevOps 报告公开基准，如 cortex.io 的 2024→2025 playbook 解读与 taskade/datadog 的 DORA 基准总结页。）

### 6.2 CMMC 作为"成熟度模型"表述不准确（SKILL.md:30、:51，rubric JSON:57）

description 与正文多次把 CMMC（Cybersecurity Maturity Model Certification）列为成熟度模型之一（"security/CMMC"）。CMMC 是美军供应链的**合规认证体系**（要求等级 1-3 由合同强制），不是像 CMM/DORA 那样用于自我评估分级的成熟度模型——它没有 5 级渐进式评估语义（实际是 3 级认证，2024 版）。安全能力成熟度更常用的模型是 C2M2、NIST CSF 成熟度层或 SSE-CMM。把 CMMC 与 CMM 并列会让 agent 在"评估安全成熟度"时误用认证框架。建议改为 "CMM/CMMI、NIST CSF" 或保留 CMMC 但注明"如合同要求"。

### 6.3 "2-pizza 5-9 / Dunbar 5-15" 并存无矛盾（确认无问题）

护栏中 2-pizza 5-9 与 Dunbar 5-15 同时出现，两个数字区间不同但表述为不同约束（团队规模 vs 紧密工作关系上限），不构成矛盾，rubric 与 methodology 中的使用也一致。✓

---

## 7. 评分体系设计（SCORING.yaml + rubric JSON）

### 7.1 13 项标准与 2 项 critical failure 的设计质量（正面）

SCORING.yaml 的分类结构（3 scope / 4 process / 3 output / 2 negative / 1 qa）与 check.py 注释区块一一对应（check.py:31-45），`total_items: 13` 与实际标准数吻合。每项标准带 judge、question、evidence 三件套，question 可直接作为 LLM judge 的 prompt，evidence 明确指向观测来源。CF-01（无视 Conway's Law → cap_to_0）与 CF-02（无证据的成熟度自评 → cap_to_0）选得准——恰好对应本领域最常见的两个失败模式，且与 rubric 的 common_failure_modes（:145-186）中 "conways_law_ignored" 和 "unrealistic_maturity" 一一对应。评分词汇在 SCORING、rubric、SKILL.md 三层一致（"exactly one Accountable/Approver"、"2-pizza 5-9"、"cognitive load"），这是全语料库中评分体系一致性做得最好的批次之一。

### 7.2 QA-01 的 3.5 门槛与 rubric guidance 的张力（🟡 主要发现 #3）

SCORING.yaml:109-113 的 QA-01 要求 "self-check score at or above the 3.5 minimum"，SKILL.md:102 同步声明同一门槛。但 rubric JSON 的 guidance 明确写着：
- `startup_small`（<30 人）: "typical_score": **"Aim for 3.0-3.5 (functional design, not over-engineered)"**（rubric JSON:102）
- `optimization_tuning`（小幅调整）: "typical_score": **"Aim for 3.0-3.5 (incremental improvements)"**（rubric JSON:141）

也就是说：对初创公司或调优类任务，rubric 自己说"好的设计就是 3.0-3.5 分"，但 QA-01 又规定平均分 <3.5 即不过关——一个按 rubric 指引产出的、规模恰当的初创团队设计会被自己的质量门拒掉。这是评分体系内部真实的逻辑冲突，会让 agent 在两种指令（"做符合规模的简单设计" vs "自评分 ≥3.5"）间无所适从。修复见 §13 🟡-4。

### 7.3 权重与"平均分"的聚合公式未定义（🟢 级别）

rubric 8 个维度权重为 1.3/1.5/1.4/1.4/1.3/1.3/1.2/1.1（合计 10.5），但 QA-01 只说 "average score ≥ 3.5"——未定义是简单平均还是加权平均、是否除以权重和。JSON 内也没有 aggregation 字段。若 runner 端用简单平均，权重形同虚设；用加权平均则与 "3.5" 的直接可比性未说明。建议在 SCORING.yaml 或 rubric 中补一行聚合公式（如 "score = Σ(weight × rating) / Σ(weight)"）。

### 7.4 全部 13 项均为 LLM judge，零确定性检查（🟡 主要发现 #4）

SCORING.yaml 中 13 项全部 `judge: llm`，check.py 恒返回空 dict（详见 §8）。其中 QA-01 的证据是 "Tool log (Read calls)"——agent 是否读过 rubric 文件是**纯事实、可脚本验证**的（`_shared/checker.py` 的 `tool_log_contains` 即可完成），却被归为 LLM judge。13/13 全 LLM 意味着评估完全依赖 judge 模型，无法捕获"agent 根本没 consult rubric 但声称 consult 了"这类作弊情形（QA-01 恰是防这类行为的项）。建议把 QA-01 改为 hybrid：脚本侧 `tool_log_contains('rubric_stakeholders_org_design.json')` 为硬性通过条件，LLM 侧评自评分合理性。

---

## 8. check.py 审查

- **结构**: 参数校验（argc==4）、agent_output 文件路径与裸文本双处理、`sys.path` 注入 `_shared`、main 出口——整体框架与 _shared 库的约定一致，`set_tool_log_path`/`set_agent_output` 均已验证存在于 `_shared/checker.py`（分别为 :224 与相邻位置），import 不会失败。docstring（:2-3）与实际行为一致。
- **行为**: `check()` 恒返回 `{}`（:46），注释（:32-45）逐项声明 "llm judge (not checked here)"——诚实但意味着本脚本对评估结果**零信息量**。runner 端必须能处理空 dict（即"全部交由 LLM"），若 runner 把空结果误解为"全部失败/全部通过"则会系统性失真，这是本 skill 评估链上唯一的硬风险点。
- **改进机会**: 见 §7.4——至少 QA-01 的"读取 rubric"事实应进脚本。另可脚本化的是"输出是否覆盖五板块"这类弱模式（如 agent_output 中检索 'power-interest'/'RACI'/'DORA' 关键词），把 PROC 类项做成 LLM+关键词双通道。当前零脚本设计合法但浪费了 _shared 库已有的 `tool_log_contains` 能力。

---

## 9. resources/methodology.md 审查

内容深度是五个文件中最大的（457 行），覆盖 Conway's Law 与逆向 Conway、四种团队类型 + 三种交互模式、DDD 限界上下文与六种上下文映射、社会网络分析的三种中心性、联盟构建四阶段、Kotter 八步、Spotify 模型、二披萨原则、平台团队提取、四种组织重构模式、组织有效性度量——领域知识准确、结构清晰、各节自引锚点（`#1-conways-law--reverse-conway-maneuver` 等）均与标题匹配，GitHub 风格锚点计算正确。

问题汇总（按严重度）：
1. **团队规模与主护栏冲突**（:104、:110）——已在 §5.2 详述，此处不再重复。
2. **"Infrastructure tasks" 软换行**（:388-389）：原文 "**Signal 2**: Stream teams slowed by infrastructure\n tasks (>20% time)"——句子在 "infrastructure" 后硬断行。Markdown 渲染时会合成 "infrastructure tasks" 正常显示，但源码层面是排版瑕疵，且这类 mid-sentence 断行在批量工具处理（grep/翻译）时会产生噪音。
3. **第 6 节游离于流程外**（:435-457 "Measuring Organizational Effectiveness"）：正文 5 步工作流与锚点目录都不含第 6 节，该节内容质量好但属于"附录式"结构，无入口。可接受，但建议在 Step 5 处引一句。
4. **DORA 表未重复出现在 methodology 中**（中性）：methodology 只在 :164、:445 提及 DORA 词汇，详细表格由 SKILL.md 承担——单点维护，避免了重复定义漂移，这是好的设计。

---

## 10. resources/template.md 审查

396 行的填空式模板，五节结构（Stakeholder Mapping / Team Structure Design / Team Interface Contracts / Capability Maturity Assessment / Transition Plan）+ 尾部 Quality Checklist，与 SKILL.md 五步流程一一对应，可直接作为交付物骨架。

- **锚点**: Step 1-5 的引用锚（:16-24）与各节标题匹配 ✓。
- **质量清单**（:353-396）是亮点：把 SKILL.md 护栏逐条转成可勾选验收项（"RACI defined ... exactly one Accountable per decision"、"No shared ownership"、"Current state assessed with evidence (not aspirations)"），与 SCORING 的 PROC/NEG/OUT 项高度对应，是"body → 模板 → 评分"三线闭环的最后一环。
- **可复用的度量定义**（:345-347）：outcome metrics 给了基线→当前→目标的示例形态，与 rubric 的 "Actionability" 维度（rubric JSON:90）要求呼应。
- **小问题**: 模板中 DORA target 列只给了 Elite 档参照值（:251-254 "Elite: Multiple/day" 等），未提示 High/Medium 档——填模板的 agent 可能据此把一切目标都设成 Elite，与 rubric guidance 的"按组织规模设合理目标"（startup 3.0-3.5）背道而驰。建议在 DORA 表后加一行"target 选择参考 rubric by_org_size 指引"。模板本身无语法/结构缺陷。

---

## 11. 人机感与交互设计

**人机感是干净的一类**：全语料零 emoji、零全大写喊叫、零称呼语，语气为中性专业顾问体。面向 agent 的指令全部为可执行动词（Map/Define/Specify/Assess/Create），无营销腔。与 083-085 senior-* 系列的"世界级"人设、072 的 emoji 泛滥形成鲜明对比——本 skill 是"克制型"的正例。

交互设计上的可改进点（均非硬伤）：
- **无 $ARGUMENTS/输入门控**：skill 直接以框架知识开场，不先问"你面对什么组织场景"。对 process 类 skill，很多同语料库优秀样本（如 017、127）会用一句话引导 agent 先确认输入（组织规模、现状结构、目标架构），再进入流程。本 skill 的 template.md 其实有 Organization Context 区块（:30-37），但 SKILL.md 没有要求先收集这些上下文。补一个"Step 0: 收集输入"（组织规模 → 当前结构 → 目标 → 约束）能显著提升输出质量，且直接喂给 rubric 的 by_org_size guidance。
- **自评门槛的定位**（SKILL.md:102）写得清楚（"Minimum standard: Average score ≥ 3.5"），agent 知道何时算完成——这在全语料库中属少见的显式退出条件，是加分项。

---

## 12. 综合评分 (8-dimension weighted table)

| # | 维度 | 权重 | 得分 | 加权 | 核心依据 |
|---|------|:----:|:----:|:----:|---------|
| 1 | 逻辑一致性 | 0.20 | 3.5 | 0.70 | 五步流程四层一致是最大亮点；但 :66 示例方向错误、§5.2 规模冲突、§5.5 双流程未衔接 |
| 2 | 语法与可读性 | 0.10 | 4.0 | 0.40 | 三份 md 干净规范；仅 methodology:388-389 软换行一处瑕疵 |
| 3 | 人机感 | 0.10 | 4.0 | 0.40 | 零 emoji 零填充语，专业克制；缺输入门控略损交互质量 |
| 4 | 规范合规性 | 0.20 | 3.5 | 0.70 | description/workflow/行数合规；缺 Scope/Limitations 与 Output Format 两必需节 |
| 5 | 内容准确性 | 0.15 | 3.0 | 0.45 | DORA 2019 阈值过时、CMMC 误当成熟度模型、:66 数字方向错误 |
| 6 | 评分体系设计 | 0.10 | 3.5 | 0.35 | 13 项+2 CF 设计精良、词汇三层一致；QA-01 门槛与 rubric guidance 冲突、聚合公式未定义 |
| 7 | check.py 脚本质量 | 0.05 | 3.0 | 0.15 | 框架正确可运行；恒空结果，QA-01 本可脚本化却未做 |
| 8 | 引用与资源完整性 | 0.10 | 5.0 | 0.50 | 全部 4 个引用文件真实存在、路径正确、无跨 skill 引用 |
| **合计** | | 1.00 | | **3.65/5.00** | |

**最终评级: 🟡 可用但有小问题（建议微调）**。与 skill-dossier 记录（129 🟡 缺 scope 或 output）方向一致，本次深审进一步确认：内容层无硬伤，问题集中在缺失节、一处示例错误、两处领域数据过时、三处评分/护栏张力。无 🔴 级问题，无需重写。

---

## 13. 修复建议

### 🔴 紧急（无）

本 skill 无阻断性缺陷。全部引用存在、description 完整、流程自洽、评分体系可用。

### 🟡 建议优先修复（6 项）

**🟡-1 补 Scope/Limitations 节（SKILL.md，工作量：小）**
在 When to Use 之后（:43 后）插入 "## Scope & Limitations"：明确不覆盖个体绩效/薪酬/纯产品战略/法律合规审查，并说明 SCOPE-03（SCORING.yaml:23）所依凭的边界应先在 body 中告知 agent。这是合规缺口，也是评分项与正文的唯一断裂点。

**🟡-2 补 Output Format 节（SKILL.md，工作量：小）**
声明交付物为组织设计备忘录、五板块结构（与 SCORING OUT-01~03 对齐）、简单场景按 template.md 填充、复杂场景至少按五板块组织。让 body 与 rubric 的隐含契约显式化。

**🟡-3 修正示例方向错误（SKILL.md:66，工作量：极小）**
"Deployment frequency: Daily → Weekly (target: Daily)" 改为 "Weekly → Daily (target: Daily)"。同表其余三行方向均为改善，仅此一行矛盾。

**🟡-4 协调 3.5 门槛与 rubric guidance（SCORING.yaml:109-113 + rubric JSON:102/:141，工作量：小）**
三选一：① 门槛改为分场景（startup/optimization 3.0、其余 3.5）；② 把 rubric guidance 的 typical_score 上调为 3.5+；③ 门槛改为 3.0 且"低于 3.5 时给出差距说明"。推荐①，与 rubric 已有的 by_org_size/by_change_type 结构天然契合。

**🟡-5 统一团队规模口径（SKILL.md:205-209 + methodology.md:104/:110，工作量：小）**
在 Guardrails 补一句："5-9 为 stream-aligned 主团队基准；enabling 团队可 2-5 人、platform 团队可 10-15 人，均需注明偏离理由"。同时把 rubric scale-1 的 "<3 unrealistic" 改为 "<3（enabling 特例除外）" 或保持现状但明确特例判定。消除三方矛盾。

**🟡-6 更新 DORA 表并处理 CMMC 表述（SKILL.md:151-156、:30、:51，工作量：小）**
① DORA 表换 2024 基准（Elite: Lead Time <1 day、CFR ~5%）或在表头注明 "2019 经典阈值"；template.md:249-254 同步。② "CMMC" 改为 "CMMI/SSE-CMM、NIST CSF"（或保留但注明认证属性）。

### 🟢 锦上添花（5 项）

**🟢-1 QA-01 改为 hybrid 检查（SCORING.yaml + check.py，工作量：小）**：脚本侧 `tool_log_contains('rubric_stakeholders_org_design.json')` 作为硬条件，LLM 侧评自评分数合理性。利用 _shared 库已有能力，把 13/13 全 LLM 降为 12 LLM + 1 确定性。

**🟢-2 定义评分聚合公式（SCORING.yaml，工作量：极小）**：补一行 "score = Σ(weight×rating)/Σ(weight)"，消除权重与平均分的歧义。

**🟢-3 补 Step 0 输入收集（SKILL.md:71-102，工作量：小）**：进入五步前先收集组织规模/现状结构/目标架构/约束，直接喂给 rubric by_org_size 指引，提升输出与评分匹配度。

**🟢-4 明确双流程衔接（SKILL.md:90，工作量：极小）**：说明进阶流程（methodology 5 步）结束后仍需补做成熟度评估与转型治理两个板块。

**🟢-5 小修三处（工作量：极小）**：Quick Reference 删掉未定义的 RAPID 或补定义（:250）；methodology:388-389 合并断行；template.md DORA 表后加"target 按组织规模选取"提示（:251-254）。

### 工作量汇总

| 级别 | 数量 | 合计工作量 |
|------|:----:|-----------|
| 🔴 | 0 | — |
| 🟡 | 6 | 约 1 个工作日（主要为 SKILL.md 补两节 + 5 处单行修改） |
| 🟢 | 5 | 约 0.5 个工作日（含 check.py 一处增强） |

**优先序建议**：🟡-3（一分钟修掉示例错误）→ 🟡-1/🟡-2（合规缺口）→ 🟡-6（准确性）→ 🟡-4/🟡-5（内部一致性）→ 🟢 项。修复后本 skill 有望进入 🟢 档（文件级质量已接近 026/034 等范本，主要差距就在两个缺失节与三处数值口径）。
