# REVIEW: 042-forecast-premortem

**审查日期**: 2026-08-06 | **审查者**: Claude | **审查范围**: 全目录 7 个文件 + `_shared/SKILL-SPEC.md` v1.0 + `skill-dossier.md` 既有档案
**既有档案**: dossier 🟡（可用但有小问题）| 旧 stub 评分: C+ (44/100) | 本审查评分: **B- (70/100)**（修正说明见 §12.4）

> 本文按 13 节模板撰写，所有行号均指审查当日文件内容（SKILL.md 455 行、SCORING.yaml 171 行、check.py 72 行、premortem-principles.md 292 行、backcasting-method.md 378 行、failure-mode-taxonomy.md 497 行）。

---

## 1. 目录清单

| # | 文件 | 行数 | 类型 | 审查状态 |
|---|------|:----:|------|:--------:|
| 1 | `SKILL.md` | 455 | 主技能文件 | ✅ 全文精读 |
| 2 | `SCORING.yaml` | 171 | 评测准则（19 项） | ✅ 全文精读 |
| 3 | `check.py` | 72 | 评测脚本（3 项 script 检查） | ✅ 全文精读 |
| 4 | `resources/premortem-principles.md` | 292 | 理论参考 | ✅ 全文精读 |
| 5 | `resources/backcasting-method.md` | 378 | 方法论参考 | ✅ 全文精读 |
| 6 | `resources/failure-mode-taxonomy.md` | 497 | 分类法参考 | ✅ 全文精读 |
| 7 | `REVIEW.md` | 4 (旧) | 旧审查 stub | ✅ 已读取并整体重写 |

**外部参照**: `_shared/SKILL-SPEC.md`（161 行，合规 12 项清单）、`_shared/checker.py`（check.py 的导入库，存在 ✅）、`skill-dossier.md`（042 条目位于第 360-365 行）。

**目录健康度**: 6 个实体文件全部存在且可解析；SKILL.md 引用的 3 个 resources 文件全部真实存在（§5 逐一核对）；无孤文件、无缺失引用。

---

## 2. Frontmatter 审查

### 2.1 `name` 字段（SKILL.md L2）

`name: forecast-premortem` — 小写 + 连字符，≤64 字符，与目录名 `042-forecast-premortem` 完全一致。✅ **通过**（SKILL-SPEC §1.1 / §4）。

### 2.2 `description` 字段（SKILL.md L3）

原文（约 330 字符，≤1024 ✅）：

> "Use to stress-test predictions by assuming they failed and working backward to identify why. Invoke when confidence is high (>80% or <20%), need to identify tail risks and unknown unknowns, or want to widen overconfident intervals. Use when user mentions premortem, backcasting, what could go wrong, stress test, or black swans."

按 SKILL-SPEC §2.1 三问拆解：

| 检查项 | 判定 | 说明 |
|--------|:----:|------|
| **WHAT**（做什么） | ✅ | "stress-test predictions by assuming they failed and working backward" 具体明确 |
| **WHEN**（何时用） | ✅ | 三组触发场景：高置信度（>80%/<20%）、尾部风险与未知未知、加宽置信区间 |
| **KEYWORDS**（关键词） | ✅ | premortem、backcasting、what could go wrong、stress test、black swans 均为有效匹配词 |
| 长度 ≤1024 | ✅ | 约 330 字符 |
| 触发信号短语（§2.4） | ⚠️ 边缘通过 | "Use when user mentions..." 是 "Use when the user..." 的变体，**缺 "the"**；字面上不命中 §2.4 列出的五个标准短语之一，但语义完全等价的短语出现两次 |
| **语态（§2.3）** | ❌ **违规** | 首句 "Use to stress-test..." 与次句 "Invoke when..." 均为**祈使句**（省略了 "this skill" / "the agent"），而 §2.2 模板要求首句为第三人称陈述句；§2.3 明令禁止 "Use this skill to..." 式祈使开头 |
| 跨技能路由（§2.5） | ✅ | 无 "NOT for X, use Y instead" 内容 |

**小结**: description 的 WHAT/WHEN/KEYWORDS 三要素齐全、长度合规、无跨技能路由，但**语态开头违规**是本文件最容易被既有档案遗漏的规范缺口——dossier 记为"Description 第三人称含触发"（详见 §11 差异分析）。修复方式见 §13-1。

### 2.3 允许/禁止字段（SKILL.md L1-4）

Frontmatter 仅含 `name` 与 `description` 两个键，无 §1.3 禁止字段（无 metadata/version/tags 等），未使用 allowed-tools/argument-hint 等可选字段（本技能为纯对话交互型，不需要工具白名单，合理）。✅ **通过**。

---

## 3. Body 结构

### 3.1 骨架与章节分布（SKILL.md）

| 行号 | 章节 | 内容定位 |
|------|------|---------|
| L6 | `# Forecast Pre-Mortem`（H1） | 标题（首字母大小写风格，规范） |
| L8-13 | `## Table of Contents` | 目录（未列 6 个工作流条目，但菜单区自含链接） |
| L17-31 | `## What is a Forecast Pre-Mortem?` | 概念、核心原则（L21 反转原则）、5 条价值点、出处（L30 Gary Klein） |
| L34-47 | `## When to Use This Skill` | **正向 5 条**（L36-41）+ **Do NOT use 3 条**（L43-46） |
| L50-63 | `## Interactive Menu` | 主菜单：7 项（6 工作流 + Exit），每项带锚点链接 |
| L66-152 | `## 1. Run a Failure Premortem` | 核心工作流（5 步，L70-77 进度清单） |
| L156-199 | `## 2. Run a Success Premortem` | 悲观预测（<20%）反向前置预演（5 步） |
| L203-263 | `## 3. Dragonfly Eye Perspective` | 三视角合成（怀疑者/狂热者/旁观者，5 步） |
| L267-339 | `## 4. Identify Tail Risks` | 尾部风险：PESTLE + 影响×概率矩阵 + kill criteria（5 步） |
| L343-401 | `## 5. Adjust Confidence Intervals` | 定量调宽：评分 → 宽度乘数 → 新边界（5 步） |
| L405-417 | `## 6. Learn the Framework` | 三个资源文件入口（与 L446-451 重复，见 §4.4） |
| L421-442 | `## Quick Reference` | 7 条诫命 + 一句话总结 + 跨技能集成 |
| L446-451 | `## Resource Files` | 资源清单（📁） |
| L455 | 收尾提示 | "Ready to start? Choose a number..." |

### 3.2 SKILL-SPEC §3.1 三必需节核对

| 必需节 | 判定 | 依据 |
|--------|:----:|------|
| **Workflow / Process** | ✅ | Interactive Menu（L50-63）+ 6 个编号工作流（L66-401）均为可执行步骤，每工作流带勾选进度清单 |
| **Output Format** | ❌ **缺失** | 全文无 Output/Deliverables 类章节；最终交付物（调整后概率/区间、kill criteria、signposts、推理记录）仅散见于各工作流内部（L149-150、L395、L397-399），无统一输出契约 |
| **Scope / Limitations** | ⚠️ 部分覆盖 | L43-46 "Do NOT use when" 回答了"何时不应使用"，但无独立 Scope/Limitations 节，未覆盖"本技能不做什么"（如不替代风险登记册、不用于通用头脑风暴） |

### 3.3 体量

455 行 ≤ 600 行硬上限 ✅。但注意：SCORING.yaml L2 声明 `pattern: mindset`，而 SKILL-SPEC §3.2 中 mindset 的目标体量是 ~50 行——本技能实际是**多工作流菜单式 process 型体量**（455 行 ≈ process 目标 200 行的 2.3 倍），pattern 分类与体量明显错位（详见 §10.2 与 §13-10）。

### 3.4 重复内容

- L405-417 "Learn the Framework" 与 L446-451 "Resource Files" 列出**完全相同的三个资源文件**，一个带 📄 emoji、一个带 📁 emoji，属轻度冗余（§13-8）。
- Quick Reference（L421-431）的 7 条诫命与正文各工作流要点重复，但作为速查表属合理设计，不计问题。

---

## 4. 逻辑一致性

### 4.1 内部自洽性（通过项）

1. **触发口径一致**: description（L3）、When to Use（L37）、Workflow 2 Step 1（L162 "<20%"）、SCORING SCOPE-02（SCORING.yaml L14-21）四处统一为 **>80% 或 <20%** 的高/低置信度触发线。✅
2. **示例连续性**: L86 例子（"startup 2 年内达 $10M ARR，概率 75%，CI 60-85%"）与 L149-150 定量例子（成功 75% → 隐含失败 25%，失败模式合计 40% → 调整至 60%）复用同一预测对象，数字链条连贯。✅
3. **算术验证**:
   - L144-147: P(failure) 求和规则内部计算正确（40% > 25% → "过高"判断成立）；
   - L373-383: `Width multiplier = 1 + Score/20`，三个示例 4/20→1.2、10/20→1.5、16/20→1.8 全部正确；
   - L395: 示例 70%，CI 60-80%（宽 20），Score 12/20 → 乘数 1.6 → 新宽 32 → 新 CI **54-86%**（70±16）计算正确。
4. **跨工作流一致性**: Workflow 1 Step 5（L136-140 "5+ 模式各 >5%"）与 Workflow 5 维度 2（L366 "1-2 个模式=1 分，5+ 个=5 分"）口径一致；Workflow 3 的"三视角共识 = 稳健失败模式"（L244-261）与 Workflow 5 维度 4（L367 "全部视角一致=5 分"）方向一致（共识越强 → 应更宽，逻辑闭环成立）。
5. **kill criteria 格式统一**: SKILL.md L316 "If [event X] happens, probability drops to [Y]%" 与 taxonomy L350 完全一致；L318-322 示例与 taxonomy L356-403 模板库互不矛盾。✅
6. **PESTLE 口径统一**: SKILL.md L288-295 六类（政治/经济/社会/技术/法律/环境）与 taxonomy L290-341 完整清单一致，且 SKILL.md L299 显式指向 taxonomy。✅

### 4.2 核心定量缺陷：非互斥失败模式按可加处理（重点）

**位置**: SKILL.md L142-147

> "Quantitative Method: Sum the probabilities of failure modes: P(failure) = P(mode_1) + P(mode_2) + ... + P(mode_n). If this sum is greater than 1 - your_current_probability, your probability is too high."

**问题**: 该"定量方法"把各失败模式概率**无条件相加**，未做交集修正。失败模式之间通常**并非互斥**（监管、竞争、执行可以同时发生），相加会系统性高估失败概率。L149-150 示例即如此：监管 20% + 竞争 20% + 执行 15% 相加得 40%，但若三者有重叠（如"监管通过"与"竞争免费层"可共存），P(任一) 严格小于 40%。

**更严重的是与本技能自己的资源文件自相矛盾**:
- `backcasting-method.md` L236-239 明确给出交集修正公式 `P(A or B) = P(A) + P(B) - P(A and B)`，且 L231-233 明示"这些路径并不独立"的警惕；
- `failure-mode-taxonomy.md` L440-457 给出独立模式下的正确聚合 `P(any) = 1 - ∏(1 - P_i)`（L444-445），并附 L452-454 正确算例（0.8×0.7×0.75 → 58%），同时注明依赖情形需用 Venn/条件概率（L456-457）。

即：**主文件使用最粗糙的加法规则，而两份资源文件都给出了更准确的规则**——同一技能内出现三种不一致的聚合口径，且主文件的规则是错的最严重的一个。这在评测上还有放大效应：SCORING.yaml PROC-05（L64-70）的 script 检查模式串 `sum of failure-mode probabilit` 会**奖励**照抄该错误规则的行为（§10.4 详述）。

**严重度评估**: 该规则的方向性偏保守（高估风险 → 倾向加宽区间），对"打击过度自信"这一技能目标是安全的误错方向，因此不构成 P0 级重写，但作为以"正确量化"为卖点的技能，核心公式与自身资源冲突属**实质性缺陷**，定级 **P1**（§13-3）。

### 4.3 流程缺口：resolution date 未经采集即被使用

- Workflow 1 Step 1（L79-86）只问三件事：预测内容、当前概率、置信区间——**未问解析日期**；
- Step 2（L92）却直接使用 "It is now **[resolution date]**"。日期只能从 L86 示例的"within 2 years"间接推断。
- 对照 `backcasting-method.md` L17-19（Phase 1 Step 1.1 "Set the resolution date ... Be specific"），主文件漏掉了自己资源文件强调的第一步。建议在 Step 1 增补第 4 问（§13-4）。

### 4.4 其他逻辑瑕疵（次要）

1. **影响×概率矩阵示例不当**（L305-309）: "Recession" 被放入 **Low Impact** 格、"Key Founder Dies" 被放入 **High Probability** 格——衰退对多数预测是高影响事件，创始人去世通常是低概率事件，两个示例与常识/统计学直觉相悖，会误导使用者对照填写（§13-5）。
2. **悬空跨技能引用**（L439-442）: `scout-mindset-bias-check`（L440）与 `bayesian-reasoning-calibration`（L441）按名称引用，但经全语料检索，**这两个技能在 322 项 corpus 中均不存在**。§3.3 允许按名称引用其他技能（"see also: <skill-name>"），但引用不存在的技能名会造成交付物中的死链（§13-12）。
3. **"Learn the Framework" 与 "Resource Files" 重复**（L405-417 vs L446-451）: 同一三文件清单出现两次（§3.4）。
4. **Workflow 5 维度 4 方向未解释**（L367）: "全部视角一致=5 分 → 更宽" 依赖 Workflow 3 的"共识=稳健"逻辑，但 L367 未回指 Workflow 3，独立阅读时方向感稍显突兀（轻微）。
5. **"Feeds into: Monitoring systems and adaptive forecasting"**（L442）无具体交接对象/格式，为占位性表述（轻微）。

---

## 5. 参考文件审查

### 5.1 `resources/premortem-principles.md`（292 行）— 理论与研究基础

- **结构**: H1 + 9 个二级节（规划谬误 L7-18、后见之明 L22-41、反转之力 L44-58、有效性研究 L62-85、结果偏误 L88-107、何时有效 L110-146、何时无效 L148-171、与其他技术对比 L174-221、认知机制 L224-242、常见异议 L245-275、实践要点 L278-288），层次分明。
- **与主文件一致性**: L115 ">80% or <20%" 与 SKILL.md L37 一致；L284-285 kill criteria/signposts 与主文件 L312-337 一致；"The Rule"（L288）与主文件 L431 "Widen CIs" 呼应。✅
- **内容质量**: Munger 名言（L49）、Kahneman 名言（L79）、premortem vs red teaming/scenario planning/risk register 对比（L174-221）均为高质量方法论内容；L103 "10% events happen 10% of the time" 表述精准。
- **问题**:
  1. **研究数据无出处**: L13-16 "90% 项目超预算、70% 延期、80% 项目经理预测按时完成"（实为 Flyvbjerg 大型项目研究）；L67 "premortem 组多识别 30% 风险"（Klein 2007）；L72 "前瞻性后见之明提升记忆 30%"（Mitchell et al. 1997）；L79 Kahneman 引文——**全部无书目/链接出处**。对理论参考文件而言，缺引注削弱可验证性（P3，§13-11）。
  2. 无语法问题、无 emoji、无术语冲突。

### 5.2 `resources/backcasting-method.md`（378 行）— 方法论核心

- **结构**: 4 个阶段（未来状态 L13-31、时间线构建 L34-68、因果链 L72-103、叙事构建 L106-148）+ 叙事 vs 定量回望（L150-188）+ 多路径高级技术（L191-240）+ 时间推理技术（L243-292）+ 常见错误（L295-330）+ 预测集成（L333-347）+ 实践工作流（L351-375）。
- **亮点**: L40-51 两年/六月预测的时间块回退模板；L77-83 因果链示例；L110-118 标题线示例（含时间锚点）；L128-131 good/bad 叙事对比；L296-330 四条回望错误与修复；L343-347 "After Backcasting" 定量示例（监管 20%+执行 15%+市场 10%+黑天鹅 5% → 调整 60%/CI 45-75%）。
- **关键作用**: L236-239 与 L444-445（taxonomy）共同构成对 SKILL.md L144 加法规则的**正确替代方案**——这是本技能内唯一一处"正确公式"的完整呈现，修复时是现成素材（§13-3）。
- **问题**:
  1. L19 示例日期 "December 31, **2025**" 已过期（审查日 2026-08），宜改为中性/未来日期（P3）；
  2. L143 "82% of startups in this space fail due to regulation" 系"旁观者视角"示例中的**虚构精确数字**，无任何来源，作为教学示例易被误读为真实统计（P3，§13-11）。

### 5.3 `resources/failure-mode-taxonomy.md`（497 行）— 分类学参考

- **结构**: 两个主维度（内/外 L7-19、可预防/不可预防 L22-34）+ 四象限（L37-45）+ 内部模式 3 类（执行/资源/战略 L48-132）+ 外部模式 7 类（市场/竞争/监管/宏观/技术/社会/环境 L135-263）+ 黑天鹅（L266-287）+ PESTLE 清单（L290-341）+ kill criteria 模板库（L344-403）+ 概率估计（L407-437）+ 聚合（L440-457）+ 监测（L461-490）+ 实操九步（L493-495）。
- **亮点**: L269 "Retrospectively predictable, prospectively invisible" 精炼；L452-454 聚合算例算术正确（1-0.8×0.7×0.75=0.58 ✅）；L466-476 工程师离职的前瞻指标（commit 频率、会议参与、LinkedIn 更新等）具体可操作；L481-489 监测节奏表（按风险等级分档）与 SKILL.md L330-335 频率示例兼容。
- **与主文件一致性**: PESTLE（L290-341）↔ SKILL.md L288-295 ✅；kill criteria 模板（L356-403）↔ SKILL.md L316-322 ✅；概率分档（L413-436：1-5%/5-15%/15-35%/35-70%/>70%）与 SKILL.md L136-140 "5+ 模式各 >5%" 兼容 ✅。
- **小张力**: L44 "Premortem focus: Mostly on **preventable** failures" 与 SKILL.md 工作流 4 主打不可预防的黑天鹅/未知未知（L267-285）侧重点不同——非矛盾（不同工作流各司其职），可接受。

### 5.4 交叉文件一致性总评

| 对比项 | SKILL.md | 资源文件 | 结论 |
|--------|----------|----------|:----:|
| 失败概率聚合规则 | L144 加法求和 | backcasting L238-239 交集公式；taxonomy L444-445 独立乘积 | ❌ **冲突**（§4.2） |
| PESTLE 六类 | L288-295 | taxonomy L290-341 | ✅ |
| kill criteria 格式 | L316 | taxonomy L350 | ✅ |
| 触发置信度线 | L37 | principles L115 | ✅ |
| 资源链接 | L112/L299/L411-415/L448-451 | 三文件回链 `../SKILL.md#interactive-menu` | ✅ 双向可达 |

---

## 6. 语法格式

### 6.1 SKILL.md

- 拼写/病句: 全文未发现错别字或断句错误（455 行逐行核读）。✅
- Markdown 结构: H1 唯一（L6），二级/三级标题层级一致（## 工作流 → ### Step）；TOC 锚点（L9-13）与标题 slug 匹配；表格均闭合（L121-125、L255-259、L305-309、L330-335）；代码围栏均成对（L70-77、L143-145、L160-167、L209-216、L271-278、L347-354、L375-377、L390-393）。✅
- 标点: "—"（em dash）与 "-" 混用（如 L21 用 "-"，L112 用 "—"），但不违反任何内部规则，属风格噪音，不计问题。
- 行内代码用于公式与变量名（L144-147、L316），规范。✅

### 6.2 SCORING.yaml（171 行）

- YAML 结构合法: 顶层 `skill/pattern/total_items/criteria/critical_failures`，criteria 每项含 id/category/description/judge/check，缩进一致；注释分区清晰（Scope/Process/Output/Negative/QA）。✅
- 正则转义正确: L70 `'plausibilit|P\\(failure\\)|1 - (your_)?current_probability|sum of failure-mode probabilit'`、L103 `'Width multiplier|\\d+/20|multiplier|New CI:|widen'`、L162 `'adjusted (probability|confidence)|\\d+%\\s*(→|->)\\s*\\d+%'` — Python re 语法合法。✅
- `total_items: 19` 与实际条目数一致（3+9+4+2+1）。✅

### 6.3 check.py（72 行）

- 结构: `check()` 返回 3 个 script 项（L37 PROC-05、L39 PROC-09、L48 QA-01），与 SCORING.yaml 中 `judge: script` 的三项**一一对应**（1:1，无遗漏无多余）。✅
- 导入路径 `os.path.join(os.path.dirname(__file__), "..", "_shared")`（L10）→ `complex-skills/_shared/checker.py`，已确认文件存在，`output_contains`/`set_tool_log_path`/`set_agent_output` 均在 CHECKER-LIBRARY.md 有定义（L160-166）。✅
- 边界处理: L23-27 用 `os.path.exists` 判别"输出是路径还是内容"，对 4KB+ 输出文本误判为路径的概率可忽略；L61-63 main() 先读文件再传内容，逻辑闭环。✅
- 风格: docstring 齐全、注释标明 llm-judge 项不走脚本，可维护性好。

---

## 7. SKILL-SPEC 合规 12 项（SKILL-SPEC.md §5 清单）

| # | 检查项 | 判定 | 依据 |
|---|--------|:----:|------|
| 1 | name 小写+连字符、≤64、匹配目录 | ✅ | SKILL.md L2 ↔ 目录 `042-forecast-premortem` |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ⚠️ | 三要素齐全、330 字符，但首句为祈使语态（§2.2） |
| 3 | description 无祈使/第一/第二人称开头 | ❌ | L3 "Use to stress-test..."、"Invoke when..." 为祈使开头 |
| 4 | description 无跨技能路由 | ✅ | 无 |
| 5 | description 至少一个触发信号短语 | ⚠️ | "Use when user mentions..." 为标准短语变体（缺 "the"），语义命中但字面不完全匹配 |
| 6 | frontmatter 无允许列表外键 | ✅ | 仅 name+description 两键（§2.3） |
| 7 | body ≤600 行 | ✅ | 455 行 |
| 8 | body 有 workflow/process 节 | ✅ | Interactive Menu（L50-63）+ 6 工作流（L66-401） |
| 9 | body 有 output format 节 | ❌ | 无显式输出节（§3.2） |
| 10 | body 有 scope/limitations 节 | ⚠️ | 仅 "Do NOT use when"（L43-46）部分覆盖，无独立节 |
| 11 | body 无跨技能文件引用（../other-skill/） | ✅ | 所有引用均为 `resources/*.md` 相对路径；跨技能仅按名称（L440-441），符合 §3.3 形式 |
| 12 | 目录 NNN-kebab-case、无空格大写 | ✅ | `042-forecast-premortem` |

**统计**: 通过 8 项（1,4,6,7,8,11,12 + 5 语义通过）；部分通过 2 项（2,10）；**未通过 2 项（3,9）**。

---

## 8. 人机感

### 8.1 语气画像

本技能是**菜单驱动的用户交互型**技能，语气明显偏"引导式对话"：

| 行号 | 原文 | 风格 |
|------|------|------|
| L52 | "What would you like to do?" | 对话式开场（合理，菜单技能惯例） |
| L68 | "**Let's stress-test your prediction by imagining it has failed.**" | 第一人称复数邀请，偏聊天 |
| L81 | "**Tell me:**" | 口语化指令 |
| L94 | "How does it feel? Surprising? Expected? Shocking?" | 情绪引导提问（设计意图明确：测真实置信度） |
| L92 | "This is a certainty. Do not argue with it." | 强指令（功能性，符合 NEG-01 设计） |
| L220/228 | "Channel the harshest critic... **Be extreme**" | 角色扮演指令 |

**评估**: 这种语气对"引导用户做压力测试"的目标是**功能性的**——用户需要被拽进"失败已发生"的想象里，L92 的强制口吻和 L94 的情绪提问都是有意的设计。但作为 corpus 中 322 项技能的 SKILL.md，其闲聊密度（Let's / Tell me / How does it feel）在同类中偏高，与 dossier 判断一致。

### 8.2 emoji 普查

| 位置 | emoji | 数量 |
|------|:-----:|:----:|
| L411/413/415 | 📄（资源入口） | 3 |
| L447 | 📁（资源目录） | 1 |

共 4 处、全部为**装饰性**用途（无功能载荷——资源链接本身已可点击，emoji 不携带信息）。对比 corpus 中 🟢 标杆技能（如 067-chronology、139-clearance 的零装饰策略），此处属可消除噪音。无 ✅/❌/⚠️ 状态类 emoji 混入指令（比 072-mobile-design 的 20+ 个 emoji 好得多）。

### 8.3 称呼与对象

全文以第二人称"you/your"面向用户提问、以祈使句驱动 agent 执行——**双受众混用但分工明确**：提问句面向用户（L81-84），执行指令面向 agent（L118-119）。未出现"亲爱的用户"式称呼，无营销腔，无全大写喊叫（仅 "Do NOT" 加粗，功能性）。

### 8.4 结论

人机感 **🟡 可用但需微调**: 交互式设计本身是亮点（L92 的确定性设定、L94 的情绪校准问题都是好设计），但"Let's / Tell me"式闲聊密度 + 4 处装饰 emoji 使其在技能语料中偏"活泼"，建议收敛措辞并去 emoji（§13-6、§13-7）。

---

## 9. 可执行性

### 9.1 优点

1. **菜单驱动、路径明确**: L50-63 主菜单 → 6 个工作流 → 每个工作流 5 步进度清单（L70-77、L160-167、L209-216、L271-278、L347-354）→ 每步有 "Next: Return to menu"（L152、L199、L263、L339、L401）。agent 可完整跟踪会话状态，无断链步骤。✅
2. **每步都有具体提示词**: 如 L101-104 回望叙事四问、L190-193 悲观挑战四问、L316 kill criterion 格式。✅
3. **量化工具完整**: L375-377 宽度乘数公式、L390-393 对称加宽公式、L144-147 失败概率检查——agent 可直接代算。✅
4. **模板表可直接套用**: L121-125 失败模式表、L255-259 三视角合成表、L305-309 影响×概率矩阵、L330-335 监测表。✅
5. **无需外部脚本/工具**: 纯对话技能，无 scripts/ 依赖，无跨技能路径依赖（仅名称引用）。✅

### 9.2 缺口

1. **无输出契约（最大可执行性缺口）**: 六个工作流各自产出（调整后概率 L150、新 CI L395、kill criteria L318-322、signposts L330-335、推理记录 L397-399），但**没有统一 Output Format 定义最终交付形态**——不同 agent 可能产出"仅口头结论"或"结构化报告"，评测时 OUT-01~04 只能依赖 llm judge 的自由裁量。此缺口同时是合规项 #9 的失败原因（§13-2）。
2. **PROC-05 公式的可执行性风险**: L144 加法规则虽然"可算"，但按 §4.2 是错误的算法——"可执行"不等于"可正确地执行"，修复后才能真正可依赖（§13-3）。
3. **悬空技能名**: L440-441 引用的两个技能在 corpus 中不存在（§4.4-2），"After: 用 scout-mindset-bias-check 校验调整"这条交接路径在当前语料下无法走通（§13-12）。

### 9.3 可评测性（与 SCORING 联动）

19 项 criterion 全部能在 SKILL.md 中找到对应文本锚点（§10.3 映射表），无不可评测条目；3 项 script 检查在 check.py 中均有实现。评测基础设施完整。

---

## 10. SCORING 交叉参考

### 10.1 文件间一致性

| 检查 | 结果 |
|------|:----:|
| SCORING.yaml `skill: forecast-premortem` 与目录名 | ✅ |
| `pattern: mindset` 与技能形态 | ⚠️ 455 行多工作流技能被标为 mindset（§10.2） |
| `total_items: 19` 与实际条目数 | ✅ 3+9+4+2+1=19 |
| `judge: script` 条目（PROC-05/PROC-09/QA-01）与 check.py 三个 return | ✅ 1:1 对应 |
| `judge: llm` 条目（16 项）与 CHECKER-LIBRARY.md llm-judge 协议 | ✅ 每项含 question+evidence 字段 |
| critical_failures（CF-01/CF-02）与 NEG 项 | ✅ CF-02 与 NEG-02 互补（未运行检查即调整 → cap_to_0） |

### 10.2 pattern 分类问题

SCORING.yaml L2 `pattern: mindset`。但该技能是**菜单式六工作流、每工作流 5 步带进度清单**的 process 型结构（对照 corpus 中其他 mindset 技能如 206-lean-startup 的知识复述型）。pattern 声明影响评测时对体量/结构的预期（SKILL-SPEC §3.2 中 mindset ~50 行 vs process ~200 行）。建议改为 `process`（§13-10）。

### 10.3 19 项 ↔ SKILL.md 锚点映射

| ID | 类别 | 锚点（SKILL.md） | 判定 |
|----|------|------------------|:----:|
| SCOPE-01 | scope | L17-31（概念框架） | ✅ 可锚定 |
| SCOPE-02 | scope | L36-41（When to Use 五条） | ✅ |
| SCOPE-03 | scope | L43-46（Do NOT use 三条） | ✅ |
| PROC-01 | process | L79-86（Step 1 三问） | ✅ |
| PROC-02 | process | L88-94（水晶球练习） | ✅ |
| PROC-03 | process | L96-112（回望叙事四提示词） | ✅ |
| PROC-04 | process | L114-125（四要素失败模式表） | ✅ |
| PROC-05 | process/script | L127-150（合理性与定量检查） | ⚠️ 锚点存在但算法有缺陷（§4.2） |
| PROC-06 | process | L156-199（成功预演） | ✅ |
| PROC-07 | process | L203-263（蜻蜓眼） | ✅ |
| PROC-08 | process | L267-339（尾部风险四件套） | ✅ |
| PROC-09 | process/script | L343-401（区间调整） | ✅ |
| OUT-01 | output | L149-150、L395（调整后数值） | ✅ |
| OUT-02 | output | L121-125、L326-337（signposts/kill criteria） | ✅ |
| OUT-03 | output | L397-399（推理记录四要素） | ✅ |
| OUT-04 | output | L421-431（七诫命） | ✅ |
| NEG-01 | negative | L92（失败确定性，不辩论是否） | ✅ |
| NEG-02 | negative | L127-150（未调整也须运行检查） | ✅ |
| QA-01 | qa/script | L150、L395（调整后概率/区间表述） | ⚠️ 见 §10.4 |

**结论**: 19 项全覆盖、无孤儿条目，评测设计与正文内容高度咬合——这是本技能评测基础设施的显著优点。

### 10.4 评测设计缺陷（3 项）

1. **PROC-05 固化错误算法**（SCORING.yaml L64-70 + check.py L37）: 模式串显式匹配 `sum of failure-mode probabilit`，即**忠实照抄 SKILL.md L144 的加法规则反而得分**，而采用 taxonomy L444-445 正确乘积公式的 agent 可能因未出现 "sum of failure-mode probabilit" 字样而**丢分**——评测规则与正确方法论方向相反。修复建议见 §13-3。
2. **QA-01 名不副实**（L155-162）: 描述称"no arithmetic errors in the check"，但 script 检查仅要求输出包含 `adjusted (probability|confidence)` 或 `X% → Y%` 字样——**复读模板即可通过**，检测不到任何算术错误。建议改为要求两侧均为具体数字的强模式（§13-10）。
3. **16/19 依赖 llm judge**: 与 corpus 主流一致（process 类技能普遍如此），但 OUT-04（七诫命遵守度）这类宽泛项的问句（L133-136）容易获得宽松通过，建议拆分或明确 evidence 字段。

---

## 11. dossier 汇总

### 11.1 既有档案（skill-dossier.md L360-365）逐句核对

| dossier 条目 | 本文判定 | 一致性 |
|--------------|----------|:------:|
| "菜单驱动工作流内部一致，算术验证正确" | ✅ 同意（§4.1 已验证 L373-383、L395 算术） | 一致 |
| "sum of failure-mode probabilities 将非互斥失败模式视为可加而未加限定" | ✅ 同意，并升级为 P1（§4.2），补充了与自身资源文件冲突的新证据 | 一致且深化 |
| "干净组织良好" | ✅ 同意（§6） | 一致 |
| "活泼、面向用户的互动性……对互动工具引人入胜但对 skill body 过于闲聊" | ✅ 基本同意（§8.1），但补充了"聊天式语气对压力测试目标具功能性"的平衡判断 | 一致 |
| "装饰性 📄📁 emoji" | ✅ 同意（§8.2，共 4 处） | 一致 |
| "workflow 存在但无显式 output-format 节" | ✅ 同意（§3.2） | 一致 |
| "455 行 ≤600" | ✅ 同意 | 一致 |
| **总评 🟡 "有效技术，但互动聊天式框架和缺 output 节需收紧"** | 🟡 ↔ B-（70/100）：方向一致，本文给分更细 | 一致 |

### 11.2 既有档案遗漏/从宽项（本文新增发现）

1. **description 祈使语态违规**（SKILL.md L3 "Use to.../Invoke when..."）——dossier 记为"Description 第三人称含触发"，从宽放行；本文按 §2.3 判为违规（合规项 #2/#3 未过）。这是**本技能与 dossier 记录的最大分歧点**。
2. **核心公式与自身资源文件冲突**（SKILL.md L144 vs backcasting-method.md L238-239、failure-mode-taxonomy.md L444-445）——dossier 只提"未加限定"，未指出"同一技能内三种聚合口径并存"。
3. **SCORING.yaml pattern 分类错位**（mindset vs 455 行 process 体量）与 **PROC-05/QA-01 评测缺陷**（固化错误算法、正则可复读）——dossier 未涉及评测侧。
4. 次要新发现: resolution date 缺口（L79-92）、尾部风险矩阵示例不当（L305-309）、悬空技能引用（L440-441）、principles 缺引注（L13-16/67/72/79）、backcasting L19 过期日期与 L143 虚构统计。

### 11.3 与旧 REVIEW.md stub（4 行）对比

旧 stub 3 点结论（加法规则、聊天语气+emoji、Output Format 缺失）**全部被本文复核证实**，但旧评分 C+ (44/100) 明显偏严：其权重偏向三个负面点，未计入本技能的强项（参考文件质量、SCORING 19 项全覆盖与 1:1 实现、算术正确性、PESTLE/kill criteria 口径统一、零跨技能路径违规）。本文的 8 维加权评分见 §12。

---

## 12. 综合评分（8 维加权 + 等级）

### 12.1 评分维度与权重

| # | 维度 | 权重 | 评分 /10 | 依据摘要 |
|---|------|:----:|:-------:|----------|
| 1 | Frontmatter 与 Description | 10% | 6.5 | 三要素齐全但祈使语态开头（§2.2） |
| 2 | Body 结构三要素 | 15% | 6.0 | workflow ✅；output ✗；scope 部分（§3.2） |
| 3 | 逻辑一致性 | 20% | 6.0 | 内部自洽+算术正确，但核心聚合公式错误且与资源冲突（§4） |
| 4 | 领域内容质量 | 12% | 8.0 | Klein premortem 方法论落地充分，PESTLE/kill criteria 扎实 |
| 5 | 参考文件完整性 | 10% | 9.0 | 三文件全部存在、高质、双向链接；仅缺引注等小瑕 |
| 6 | 语法与格式 | 8% | 8.5 | 无错字、结构规范；4 处装饰 emoji |
| 7 | 人机感 | 10% | 7.0 | 交互设计功能性，但闲聊密度偏高（§8） |
| 8 | 可执行性与可评测性 | 15% | 7.0 | 菜单闭环可执行；评测 19 项全覆盖但 2 项脚本检查有缺陷（§10.4） |

### 12.2 加权计算

```
6.5×0.10 + 6.0×0.15 + 6.0×0.20 + 8.0×0.12 + 9.0×0.10 + 8.5×0.08 + 7.0×0.10 + 7.0×0.15
= 0.65 + 0.90 + 1.20 + 0.96 + 0.90 + 0.68 + 0.70 + 1.05
= 7.04 → 70.4 / 100 → 70/100
```

### 12.3 等级判定

| 等级 | 区间 | 判定 |
|------|------|:----:|
| A | ≥85 | — |
| **B-** | **70-74** | **★ 本技能: 70/100** |
| C | 55-69 | 旧 stub 44 分在此区间下限之下 |
| D | <55 | — |

**综合评语**: 方法论扎实、执行链完整、评测基础设施出色的**中上等 🟡 技能**。一个核心公式缺陷（P1）与两个结构性合规缺口（Output 节、Description 语态）是其停留在 B- 而非 A-/B+ 的原因；修复 P1 三项后预计可达 **B+（78-80）**，再补齐 P2 可冲击 **A-（82-84）**。全部修复项见 §13。

### 12.4 与旧评分（C+ 44/100）的差异说明

旧 stub 评分为 4 行概括式（非加权体系），其 44 分对应"三个负面点"的直觉加权。本文以 8 维加权重评得 70 分，差异主要来自: （1）参考文件质量（9.0）与领域内容（8.0）两个强项未在旧评分中体现；（2）评测基础设施（19 项全覆盖、check.py 1:1）被计入；（3）逻辑维度按"方向保守、可修复"而非"致命错误"处理。两评分对**问题清单**无分歧，仅总分标尺不同。

---

## 13. 修复建议 ★重点★

> 按优先级排列。P0 = 必须立即修复（暂无）；P1 = 高优先，影响正确性或合规达标；P2 = 中优先，影响质量或用户体验；P3 = 低优先，打磨项。每项给出文件、行号、问题与**具体改法**。修复顺序建议: 13-1 → 13-3 → 13-2 → 其余。

### 13-1 【P1】description 语态改写（SKILL.md L3）

**问题**: 首句 "Use to stress-test..."、次句 "Invoke when..." 为祈使语态，违反 SKILL-SPEC §2.3（合规项 #2/#3 未过）；这是本技能唯一一处"描述级"规范缺口。

**改法**（将动作主体变为第三人称、保留全部触发语义）:

```yaml
description: "Stress-tests predictions by assuming they have failed and working backward to identify why. Use when the user has high confidence (>80% or <20%), needs to identify tail risks and unknown unknowns, or wants to widen overconfident intervals. Use when the user mentions premortem, backcasting, what could go wrong, stress test, or black swans."
```

要点: ① 首句改为第三人称一般现在时（对齐 §2.2 模板）；② "Use when the user" 补回 "the"，精确命中 §2.4 标准触发短语；③ WHAT/WHEN/KEYWORDS 三要素不变。改后合规项 #2/#3/#5 全部转 ✅。

### 13-2 【P1】新增 Output Format 节（SKILL.md，建议插在 L401 与 L405 之间）

**问题**: 合规项 #9 未过（§3.2）；六个工作流产出形态无统一契约，评测 OUT-01~04 只能依赖 llm 裁量（§9.2-1）。

**改法**: 插入独立章节（约 15 行）:

```markdown
## Output Format

交付一份结构化的压力测试结论，包含以下五个部分：

1. **原始预测**: 预测陈述、当前概率、当前置信区间、解析日期
2. **失败模式表**: 每条含机制、似然、预警信号（表格式）
3. **聚合检查**: 按独立性假设聚合的失败概率（注明使用公式与重叠假设）
4. **调整后结论**: 调整后概率 + 新置信区间；若未调整，须显式写明"经合理性检查后置信度保持不变"及理由
5. **监测计划**: 每条 kill criterion 对应的 signposts 与检查频率

若任一部分不适用，须显式注明"不适用"而非省略。
```

要点: ① 第 4 部分呼应 OUT-01 与 NEG-02（未调整也必须给出检查记录）；② 第 2 部分呼应 OUT-02；③ 第 5 部分呼应 OUT-03。**注意**: 输出节只定义交付物形态，不要引入新的执行步骤，避免与六个工作流重复。

### 13-3 【P1】修复失败概率聚合公式（SKILL.md L142-150 + SCORING.yaml L64-70 + check.py L37）

**问题**: 加法求和未做交集修正，且与自身两份资源文件（backcasting-method.md L238-239、failure-mode-taxonomy.md L444-445）冲突（§4.2）；PROC-05 模式串固化错误算法，评测方向与方法论相反（§10.4-1）。

**改法 A（推荐，主文件改为引用资源）**: 将 L142-147 的"Quantitative Method"改写为:

```markdown
**Quantitative Method:** Estimate each failure mode's probability, then aggregate
with overlap explicitly accounted for. See [Failure Mode Taxonomy](resources/failure-mode-taxonomy.md)
"Aggregation" section — if modes are independent, use P(any failure) = 1 - ∏(1 - P_i);
if they may co-occur, subtract intersections (P(A or B) = P(A) + P(B) - P(A and B)).
```

**改法 B（若保留内联公式）**: 至少把 L144 改为 `P(any failure) = 1 - ∏(1 - P_i)`（独立假设）并加一行"模式间存在重叠时须扣除交集，公式见 backcasting-method.md"。

**配套修改**:
1. SCORING.yaml PROC-05（L64-70）: description 改为 "Agent applies a probability-aggregation check with overlap assumptions stated (independence product or intersection-adjusted sum)"; 模式串从 `sum of failure-mode probabilit` 扩展为 `1 - \\\\(1 -|independence|overlap|intersection|\\\\(1 - \\\\prod` 之类，使正确聚合形式同样命中，错误加法形式不再独占得分。
2. check.py L37 同步替换模式串（保持与 SCORING 1:1）。
3. L149-150 示例重算: 若用独立乘积，监管 20%/竞争 20%/执行 15% → `1 - 0.8×0.8×0.85 = 45.6%`，仍 >25%，结论"调至 ~54%"不变（方向一致，数字更新即可）。

### 13-4 【P2】Step 1 增补"解析日期"采集（SKILL.md L79-86）

**问题**: Step 2（L92）使用 `[resolution date]` 但 Step 1 未询问（§4.3），与 backcasting-method.md L17-19 的显式要求不符。

**改法**: L81-84 的 "Tell me" 列表增加第 4 项:

```markdown
4. What's the resolution date (when will you know)?
```

并同步更新 L86 示例: "Resolution: 2027-06-30"（或与预测日期一致的示例）。

### 13-5 【P2】修正尾部风险矩阵示例（SKILL.md L305-309）

**问题**: "Recession" 置于 Low Impact 格、"Key Founder Dies" 置于 High Probability 格，与直觉/统计相悖（§4.4-1），会引导用户错误填表。

**改法**（换成无歧义的示例）:

|  | Low Probability | High Probability |
|---|---|---|
| **High Impact** | Major pandemic | Key customer churn |
| **Low Impact** | Minor tax change | Competitor emerges |

或保留原四例但重排: Pandemic（低概率/高影响）、Key engineer quits（中高概率/高影响）、Recession（中概率/中高影响）、Competitor free tier（高概率/中影响）——总之**删除"Recession=Low Impact"与"Key Founder Dies=High Probability"这两个反直觉组合**。

### 13-6 【P2】去除装饰性 emoji（SKILL.md L411/413/415/447）

**问题**: 4 处 📄📁 无信息载荷（§8.2），是 corpus 中 🟢 标杆技能（如 067、139）不采用的装饰。

**改法**: 删除各处的 📄/📁，保留加粗链接:

- L411: `📄 **[Premortem Principles](...)**` → `**[Premortem Principles](...)**`
- L413/415: 同法处理
- L447: `📁 **resources/**` → `**resources/**`

### 13-7 【P2】收敛闲聊式措辞（SKILL.md L52/L68/L81/L94）

**问题**: "Let's stress-test..."、多外 "Tell me:" 使语气密度偏高（§8.1）。注意 L92 "Do not argue with it" 与 L94 情绪提问是**功能性设计，保留**。

**改法**（只替换装饰性闲聊，不伤交互性）:
- L68: "**Let's stress-test your prediction by imagining it has failed.**" → "**Stress-test the prediction by assuming it has failed.**"
- L81: "**Tell me:**" → "**State the following:**"
- L94 保留（情绪校准是方法本身）; L52 "What would you like to do?" 保留（菜单惯例）。

### 13-8 【P3】合并重复的资源清单（SKILL.md L405-417 与 L446-451）

**问题**: 同一三文件清单出现两次（§3.4）。

**改法**: "Learn the Framework"（L405-417）改为一句引导语 + 指向 Resource Files 的链接，删除重复的三行 📄 列表；或反之删除 L446-451 保留 L405-417（推荐保留 L405-417，因其含文件简介）。任选其一，避免双清单漂移。

### 13-9 【P2】补独立 Scope/Limitations 节（SKILL.md，建议紧随 L47 之后）

**问题**: 合规项 #10 部分未过（§3.2）；"Do NOT use when"（L43-46）只覆盖"何时不用"，未覆盖"不做什么"。

**改法**: 插入（约 8 行）:

```markdown
## Scope and Limitations

**This skill does NOT:**
- Replace risk registers, scenario planning, or red-team analysis (it feeds into them)
- Turn generic "what could go wrong" brainstorms into premortems without a stated prediction and confidence
- Provide calibrated probability arithmetic — it provides the stress-test frame; quantitative checks must state their independence/overlap assumptions
- Run premortems on trivial, low-stakes, or already-uncertain (~50%) predictions (see "When to Use This Skill")
```

对照: taxonomy L174-221 已有 premortem vs 其他技术的对比内容，本节约 8 行即可，不必重复展开。

### 13-10 【P3】SCORING.yaml 评测侧修补

**问题**: ① pattern 分类错位（mindset vs 455 行 process 体量，§10.2）；② QA-01 正则可复读通过（§10.4-2）；③ OUT-04 问句过宽（§10.4-3）。

**改法**:
1. SCORING.yaml L2: `pattern: mindset` → `pattern: process`（与体量和结构匹配；如 runner 依赖 pattern 决定 llm judge 提示语，此改动会影响评测一致性——**需确认 runner 无耦合后再改**，若无把握可仅改正文注释）。
2. QA-01（L155-162）: 模式串改为 `(\\d+%\\s*(→|->)\\s*\\d+%)` 强制**两侧均为数字**，并删除 `adjusted (probability|confidence)` 这个可复读分支；同步改 check.py L48。
3. OUT-04（L130-136）: 问句拆分为两条（"是否至少列出三个具体机制" + "是否给出每个模式的概率/频率"），evidence 字段指向 L121-125 表格与 L330-335 监测表。

### 13-11 【P3】资源文件引注与数字纪律（premortem-principles.md / backcasting-method.md）

**问题**: ① principles 的研究数据无出处（L13-16、L67、L72、L79，§5.1）；② backcasting L143 虚构精确统计"82%"（§5.2）；③ backcasting L19 过期日期"December 31, 2025"（§5.2）。

**改法**:
1. principles.md 在 L13-16 后追加来源行（如 "Source: Flyvbjerg, 2003, Megaprojects and Risk"）；L67 后 "Source: Klein, 2007, Harvard Business Review"；L72 后 "Mitchell, Russo & Pennington, 1989"；L79 后 "Kahneman, 2011, Thinking, Fast and Slow"。或在文件末尾加一个小节 "## Sources" 统一收编。
2. backcasting L143: "82% of startups in this space fail due to regulation" → 改为无精确数字的表述，如 "Base rates for startup failure are high, and regulatory causes are common in this space"（教学示例不应携带虚构统计）。
3. backcasting L19: "December 31, 2025" → "December 31, 2026" 或中性示例日期。

### 13-12 【P3】处理悬空技能引用（SKILL.md L439-442）

**问题**: `scout-mindset-bias-check`（L440）、`bayesian-reasoning-calibration`（L441）在 322 项 corpus 中不存在（§4.4-2）。

**改法**: 二选一——
1. 若这些技能存在于更大的技能库（corpus 外），保留引用并在括号注明 "if available"；
2. 若以当前 corpus 为基准，改为中性表述: "**After:** Re-run the plausibility and quantitative checks (see Step 5) after any adjustment" 与 "**Companion:** Works with general bias-checking and Bayesian-updating practices"，删除具体技能名，避免死链。

### 13-13 【P3】其余打磨

1. **Workflow 5 维度 4 回指**（L367）: 句末追加 "（见 Workflow 3 的稳健失败模式定义）"，独立阅读方向更清晰。
2. **L442 "Feeds into"** 改为具体交接: "Feeds into: monitoring signposts (see Output Format item 5)"——与本技能自身的输出契约闭环，而非泛指"monitoring systems"。
3. **目录加工作流锚点**（L8-13）: TOC 增补 1-6 工作流条目（当前仅菜单区可跳转），提升导航性。
4. **体量治理**（可选，P3）: 455 行已超 mindset 目标（~50 行）近 9 倍，若团队追求 pattern 体量纪律，可将 Workflow 4 的 PESTLE 明细（L288-295）与 Workflow 5 的完整示例（L379-395）下沉到 taxonomy/backcasting 资源文件，主文件瘦身至 ~350 行；**此条不强制**，455 行在 600 硬限内合规。

### 13-14 修复清单总表与预期效果

| 优先级 | 项数 | 涉及文件 | 修复后预期 |
|:------:|:----:|----------|-----------|
| P1 | 3 | SKILL.md L3/L142-150、新增节；SCORING.yaml L64-70；check.py L37 | 合规 12 项 12/12 或 11/12；逻辑评分 6.0→8.0 |
| P2 | 5 | SKILL.md L79-86/L305-309/L411-447/L43 后/新增节 | 人机感 7.0→8.0；可执行性 7.0→8.0 |
| P3 | 6 | 三份资源文件、SCORING.yaml、check.py、L405-417/L439-442 等 | 内容评分 8.0→8.5+，打磨收尾 |

**预计修复后综合分**: P1 全部 + P2 全部 → **B+ 至 A-（78-84）**；P3 全部完成 → **A-（82-84）**。该技能**无需重建**，全部问题均为外科手术式修改；其框架设计与评测基础设施是 corpus 中 process 型技能的上游水准，修复成本低、收益确定。

---

## 附录

### 附录 A: 文件清单与行数（复核）

| 文件 | 行数 | 复核方式 |
|------|:----:|----------|
| SKILL.md | 455 | wc -l + 全文精读 |
| SCORING.yaml | 171 | wc -l + 全文精读 |
| check.py | 72 | wc -l + 全文精读 |
| resources/premortem-principles.md | 292 | wc -l + 全文精读 |
| resources/backcasting-method.md | 378 | wc -l + 全文精读 |
| resources/failure-mode-taxonomy.md | 497 | wc -l + 全文精读 |
| _shared/SKILL-SPEC.md | 161 | 合规依据（§7 引用） |
| _shared/checker.py | 存在 ✅ | check.py 导入依赖验证 |

### 附录 B: 关键行号速查

| 主题 | 行号 |
|------|------|
| description 祈使语态 | SKILL.md L3 |
| Do NOT use when（部分 Scope） | SKILL.md L43-46 |
| 主菜单 | SKILL.md L50-63 |
| Workflow 1 Step 1（缺解析日期） | SKILL.md L79-86 |
| 水晶球练习（NEG-01 锚点） | SKILL.md L88-94 |
| 失败模式表 | SKILL.md L121-125 |
| **加法求和公式（缺陷）** | SKILL.md L142-150 |
| 成功预演 | SKILL.md L156-199 |
| 蜻蜓眼三视角 | SKILL.md L203-263 |
| 影响×概率矩阵（示例不当） | SKILL.md L305-309 |
| kill criteria | SKILL.md L312-324 |
| 宽度乘数公式 | SKILL.md L373-395 |
| 资源清单重复 | SKILL.md L405-417 vs L446-451 |
| 悬空技能引用 | SKILL.md L439-442 |
| 正确聚合公式（交集） | backcasting-method.md L238-239 |
| 正确聚合公式（独立乘积） | failure-mode-taxonomy.md L444-445 |
| 虚构统计 "82%" | backcasting-method.md L143 |
| 无出处研究数据 | premortem-principles.md L13-16/67/72/79 |
| PROC-05 固化错误算法 | SCORING.yaml L64-70 / check.py L37 |
| QA-01 弱正则 | SCORING.yaml L155-162 / check.py L48 |
| dossier 042 条目 | skill-dossier.md L360-365 |

### 附录 C: SCORING 19 项 ↔ SKILL.md 锚点映射表

（完整表见 §10.3，此处仅列 3 项 script 检查的对应实现位置）:

| 项 | judge | 模式串 | check.py 实现 |
|----|:-----:|--------|:-------------:|
| PROC-05 | script | `plausibilit\|P\(failure\)\|1 - (your_)?current_probability\|sum of failure-mode probabilit` | L37 |
| PROC-09 | script | `Width multiplier\|\d+/20\|multiplier\|New CI:\|widen` | L39 |
| QA-01 | script | `adjusted (probability\|confidence)\|\d+%\s*(→\|->)\s*\d+%` | L48 |

### 附录 D: 合规 12 项修复前后对照

| # | 检查项 | 修复前 | 修复后 |
|---|--------|:------:|:------:|
| 2 | description 三要素+语态 | ⚠️ 祈使开头 | ✅（13-1） |
| 3 | 无祈使/人称开头 | ❌ | ✅（13-1） |
| 5 | 触发信号短语 | ⚠️ 缺 "the" | ✅（13-1） |
| 9 | output format 节 | ❌ | ✅（13-2） |
| 10 | scope/limitations 节 | ⚠️ 部分 | ✅（13-9） |

**修复后预期**: 合规 12 项全部通过（12/12）。

---

*本审查覆盖目录内全部 7 个文件及两个 _shared 参照文件；所有行号经 wc -l 与逐行核读双重确认。审查结论与 skill-dossier.md 042 条目（🟡）方向一致，新增 4 项发现见 §11.2。*
