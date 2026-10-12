# REVIEW — 080-ceo-advisor

审查日期：2026-08-06
审查对象：`D:\SkillIF\skill-experiment\complex-skills\080-ceo-advisor\` 全目录 8 个文件
审查依据：`_shared/SKILL-SPEC.md` v1.0、`_shared/CHECKER-LIBRARY.md`、dossier 档案（skill-dossier.md 中 080 条目）
审查方式：全文精读 + 两个脚本的数值级复现验证（growth 复利、IRR 边界、break-even 索引均已实跑确认）

---

## 1. 审查概览（Review Overview）

### 1.1 结论摘要

| 维度 | 结论 |
|------|------|
| 总评 | 🟡 可用但需修复。与 dossier 的 🟡 一致，但严重程度需上调：dossier 只审查了 SKILL.md，本次审查覆盖全包后确认 scripts/ 存在真实正确性缺陷与数据注入缺失，属于 P1 级问题 |
| 最强项 | description 合规；引用文件齐全；参考文件单文件内部质量高；SCORING 的 critical_failures 设计精准 |
| 最弱项 | 两个脚本均无输入管道（跑出来的是硬编码示例）；脚本用默认值"生产"数据（幻觉风险直接威胁 NEG-01/CF-02）；body 缺 2/3 必需节；跨文件 5 处不一致 |

### 1.2 逐文件评级

| 文件 | 评级 | 一句话 |
|------|:----:|--------|
| SKILL.md | 🟡 | 知识正确但结构缺 2/3 必需节，是参考转储而非可执行 skill |
| SCORING.yaml | 🟡 | 17 项标准与内容锚点清晰，但 2 个 script 检查均为"提及级"弱证据 |
| check.py | 🟢 | 与 SCORING 一致，集成正确，fail-closed |
| scripts/strategy_analyzer.py | 🟠 | 无输入管道、默认值造假、输出含硬编码占位符 |
| scripts/financial_scenario_analyzer.py | 🟠 | 4 个已复现的数值错误 + 无输入管道 |
| references/executive_decision_framework.md | 🟢 | 单文件质量高，但与 SKILL.md 存在 3 处不一致 |
| references/board_governance_investor_relations.md | 🟢 | 单文件质量高，board package 与 SKILL.md 不一致 |
| references/leadership_organizational_culture.md | 🟢 | 单文件质量高，沟通日历节奏与 SKILL.md 不一致 |

### 1.3 与 dossier 的差异说明

dossier（2026-08-05）对 080 的结论为："🟡 事实正确的知识库但不是 agentic skill；补 workflow 和 output 节"，并称"资本配置范围求和正确"。本次审查的修正：

1. **资本配置范围求和在端点处并不成立**：SKILL.md 四档范围 40-50% / 25-35% / 10-15% / 10-15% 的端点极值为 85%–115%，仅中点恰好等于 100%。reference 的 4 档方案（Essential 40-50 / Strategic 30-40 / Efficiency 10-15 / Experimental 5-10）同样端点不闭合。
2. **dossier 未覆盖 scripts/**：本次实跑复现出 growth 双重复利、IRR 数学域错误、break-even 索引回绕、敏感性分析为常数表等真实缺陷，且两脚本完全无法注入用户数据。这些是比"缺节"更优先的修复项。

---

## 2. 文件清单与目录结构（File Inventory）

| 路径 | 行数 | 角色 |
|------|-----:|------|
| SKILL.md | 501（body 497） | 主 skill 定义 |
| SCORING.yaml | 158 | 评测标准：17 项 criteria + 2 项 critical_failures |
| check.py | 74 | 评测执行器（2 项 script 检查） |
| scripts/strategy_analyzer.py | 610 | 战略分析脚本 |
| scripts/financial_scenario_analyzer.py | 452 | 财务场景建模脚本 |
| references/executive_decision_framework.md | ~476 | 决策框架参考 |
| references/board_governance_investor_relations.md | ~600 | 董事会治理 + 投资者关系参考 |
| references/leadership_organizational_culture.md | ~683 | 领导力与文化参考 |

结构评价：

- **目录命名合规**：`NNN-kebab-case`、无大写无空格，`080-ceo-advisor` 与 frontmatter `name: ceo-advisor` 精确一致（§4）。
- **引用完整性**：SKILL.md 引用的 2 个脚本、3 个 reference 全部实际存在；`references/` 与 `scripts/` 内无孤儿文件、无跨 skill 路径（`../other-skill/` 未出现），符合 §3.3。
- **规模失衡**：SCORING 声明 `pattern: mindset`，而 mindset 模式的目标体量是 ~50 行（§3.2），实际 body 497 行，为目标的 10 倍。这是整个 corpus 中 mindset 类目里最重的文件之一，pattern 分类与实际形态不符（更像 process 或纯 reference）。

---

## 3. 元数据与 Frontmatter 合规性（Frontmatter）

逐项核对 SKILL-SPEC §1：

| 检查项 | 结果 |
|--------|------|
| `name` 小写 + 连字符，≤64 字符，匹配目录 | 通过（`ceo-advisor`） |
| 无违禁字段（metadata/license/version/tools/trigger 等 44 个禁项） | 通过（仅 name + description） |
| `description` ≤1024 字符 | 通过（实测 509 字符） |
| 无 `allowed-tools` 等可选字段 | 通过（未使用，属允许范围） |

结论：frontmatter 零问题，是 322 个 skill 中干净度第一梯队。与 dossier 的 080 条目（"Description 第三人称含触发"）一致。

---

## 4. Description 触发设计分析（Trigger Design）

```
"Executive leadership guidance for strategic decision-making, organizational development,
and stakeholder management. Includes strategy analyzer, financial scenario modeling,
board governance frameworks, and investor relations playbooks. Use when planning strategy,
preparing board presentations, managing investors, developing organizational culture,
making executive decisions, or when user mentions CEO, strategic planning, board meetings,
investor updates, organizational leadership, or executive strategy."
```

- **WHAT**：明确（CEO 领导力指导，含 4 类工具）。
- **WHEN**：6 个动作触发 + 8 个关键词触发，覆盖 7 个领域（strategy / financial scenarios / board / investor relations / culture / crisis / succession）。
- **KEYWORDS**：以"when user mentions"清单内嵌，另 body 有独立 `## Keywords` 行（17 个术语）。
- **人称与语态**：第三人称，无祈使/第一人称开头，含规范触发信号短语 "Use when..."（§2.3、§2.4 通过）。
- **无跨 skill 路由**：description 未出现 "NOT for X, use Y instead"（§2.5 通过）。

对 SkillIF 触发实验的评估：

- 优点：触发词密度高且领域显式，适合做"有触发 vs 无触发"对照集（对照组只需把 description 中的触发清单摘除即可，body 不依赖触发词）。
- 风险：8 个"user mentions"关键词把触发面铺得很宽，低相关请求（如仅一句 "help me with my board meeting"）也可能命中，评测时需在 task prompt 设计上控制干扰度。
- 盲点：description 未覆盖 crisis 与 succession 的显式触发（"crisis"、"succession" 不在触发清单里，只在 body Keywords 中），SCORING SCOPE-01 却把 crisis/succession 列为待识别领域——触发面与评测面之间存在一个小的错位。

---

## 5. Body 结构与 SKILL-SPEC 三节合规性（Body Structure）

### 5.1 三必需节核对（§3.1）

| 必需节 | SKILL.md 现状 | 判定 |
|--------|---------------|:----:|
| Workflow / Process | 有碎片化流程（Strategic Planning Cycle 季度循环、Go/No-Go 清单、board 准备时间线、crisis 分级），但**无统领全 skill 的顶层工作流**——没有"识别领域 → 收集数据 → 选择框架/脚本 → 产出"的执行主线 | 部分 |
| Output Format | **缺失**。无任何"交付物长什么样"的定义；body 以 Success Metrics / Red Flags 两个清单收尾 | 缺失 |
| Scope / Limitations | **缺失**。无"何时不用"、无"不做什么"、无数据前提声明、无反事实编造禁令 | 缺失 |

结论：497 行 body 缺 2/3 必需节，是 §3.1 的硬性违反，与 dossier 结论一致。

### 5.2 结构诊断

- **内容组织**：19 个二级节覆盖 Vision & Strategy / Capital & Resource / Stakeholder / Organizational / External Representation / Executive Routines / Critical Decisions / Board / IR / Performance / Succession / Personal Development / Tools / Success Metrics / Red Flags。目录学上完整，7 个领域都有锚点。
- **但它是知识目录而非执行协议**：全篇无一个"先做 A 再根据 X 做 B"的分支，无决策树（§3.4 明确要求 decision trees over prose）。例如 board 部分只是模板堆叠，没有"遇到什么信号用哪个模板"。
- **与 references 高度重复**（详见 §11）：culture 时间线、succession 时间线、board 准备时间线、decision checklist、capital allocation、stakeholder 矩阵在两处各写一遍且细节有分歧——违反 §3.4 "knowledge delta over redundancy"。
- **行数**：497 行 ≤ 600 硬限（§3.2 通过），但远超 mindset ~50 行目标。
- **知识增量问题**：书单（Good to Great 等 4 本）、网络（YPO/EO）等内容对 agent 是零增量信息，占行数但不增加能力。

### 5.3 与 SCORING 的锚点映射（正面）

17 项 criteria 在 body 中几乎都有可引用的内容锚点：PROC-01→季度循环、PROC-02→Decision Checklist（8 项）、PROC-04→Stakeholder Priority Matrix、PROC-05→Capital Allocation、PROC-06→Board 准备时间线、PROC-07→Earnings Cycle、PROC-08→Crisis 三级、OUT-02→Company Scorecard、QA-01→Red Flags。评测标准不是凭空造的，这点是设计质量的正分项。

---

## 6. SCORING.yaml 评测设计分析（Scoring Design）

### 6.1 结构核对

- `total_items: 17` 与实际 criteria 数一致（3 scope + 8 process + 3 output + 2 negative + 1 qa）。
- `pattern: mindset` 与 body 形态不匹配（见 §5.2）。
- `judge` 分布：script 2 项（SCOPE-02、PROC-03），llm 15 项。
- `critical_failures` 2 项：CF-01（泛泛而谈无框架 → cap_to_0）、CF-02（编造财务/市场/董事会数据 → cap_to_0）。这两项选得极其精准——正是本 skill 的两个真实高风险失败模式（§12 的风险画像印证）。

### 6.2 script 检查的弱证据问题

两个 script 检查都基于 `tool_log_contains`（对每条工具调用 JSON 做正则匹配）：

1. **SCOPE-02**（`(?i)(executive_decision_framework|board_governance_investor_relations|leadership_organizational_culture)`）：agent 只需 **Read** 过任一 reference 文件即通过——文件名出现在 Read 的 args 里就命中。不验证"回答是否真的用了框架"。一个读了文件但回答完全没引用内容的 agent 照样得分。
2. **PROC-03**（`financial_scenario_analyzer\.py`）：agent 只需**提及**该文件名（Read、Grep 甚至自言自语）即通过，不要求真正 Bash 执行；即使执行，由于脚本无输入管道（§8/§9），执行结果也是硬编码示例，与用户数据无关——**检查测的是一个 skill 自身文档无法有意义执行的行为**。

建议（详见 §13）：SCOPE-02 至少要求 Bash 调用或 output_contains 报告标题（"=== Financial Scenario Analysis ===" / "STRATEGIC HEALTH SCORE"）；或将两者升级为 `tool_log_order`（先 Read 后 Bash）。

### 6.3 LLM 判断项的覆盖缺口

- **无"先索取数据"项**：脚本需要公司数据字典，但没有任何 criterion 检查"agent 在数据不足时是否显式向用户索取而非自行补全"。这是 NEG-01 的前置保护，建议补一条。
- **SCOPE-03 / NEG-01 / CF-02 三者证据重叠**：都指向"不编造"，判定维度冗余。不算错误，但 judge 提示词会因此重复问同一类问题。
- **PROC-01 对 LLM judge 的信息依赖高**：季度循环在 SKILL.md 与 reference 中均有，judge 需携带全文才能判，否则容易给错分。
- **SCOPE-01 的多领域选择问题**：criteria 问"识别哪个 CEO 领域并停留其中"，但未覆盖"同时多领域相关时的优先级"（如 crisis + board 复合问题）。测试题如不规避复合场景，judge 会陷入主观。

### 6.4 对 2×5 测评矩阵的适配性

该 skill 的 NEG-01/QA-01/CF-02 是 mode 与 harness 差异最可能放大的判别器（无触发模式下 agent 不读文件时是否仍保持事实纪律、是否主动 surface red flags）。作为矩阵实验的"纪律型"样例，设计上合适。

---

## 7. check.py 与 checker 集成审查（Checker Integration）

- **职责划分正确**：check.py 只返回 2 项 script 可验证项，15 项 llm 项显式注释排除，与 SCORING 完全一致；`main()` 负责读 agent_output 文件、`check()` 负责执行。
- **路径注入**：`sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))` 相对本文件定位 `_shared`，从 skill 目录或任意 cwd 调用均可用；checker 的 `tool_log_contains` 在 tool log 缺失/损坏时返回 False（fail-closed），符合评测预期。
- **边缘细节**：
  1. `os.path.exists(agent_output)` 的 try/except 捕获 `(OSError, ValueError)`——Windows 上超长字符串路径会抛 OSError，意图明确；但若 agent 输出恰好与磁盘上某文件路径同名，会跳过 `set_agent_output`。当前 check.py 不使用任何 output_* 函数，此问题无实际影响，但作为可复用模板是隐患。
  2. `json` 导入被 `main()` 使用，无死代码；注释与行为一致（"Run all 2 script checks"）。
- **结论**：check.py 本身实现质量 🟢；其薄弱处完全继承自 SCORING 的检查模式（§6.2），非本文件过错。

---

## 8. scripts/strategy_analyzer.py 审查（Script Review A）

### 8.1 架构

- 5 支柱加权模型（market 0.25 / financial 0.25 / operational 0.20 / organizational 0.20 / growth 0.10），权重和为 1.00，正确。
- 框架库（SWOT / Porter / BCG / Ansoff）、风险计算、战略选项生成、路线图生成、建议生成构成一条完整分析管道，内部自洽。
- 输出格式化函数 `analyze_strategy` 生成文本报告。

### 8.2 关键缺陷（按严重度）

| # | 缺陷 | 严重度 | 说明 |
|---|------|:------:|------|
| A1 | **无任何输入管道** | 高 | 无 argv 解析、无 stdin 读取、无 JSON 文件加载。`__main__` 只跑硬编码的 TechCorp 示例。SKILL.md Quick Start 指示 `python scripts/strategy_analyzer.py`——照做只能得到一份与用户无关的示例报告。agent 若想用真实数据，必须自己 import 并写封装代码，而 SKILL.md 没告诉它这么做。文档化用法与实际能力脱节 |
| A2 | **默认值造假** | 高 | `_apply_frameworks` 在无输入数据时填充 "Strong brand recognition" / "Robust technology platform" 等 SWOT 默认项；Porter 力默认值（rivalry 70 等）；`_analyze_pillar` 对空数据返回 50.0、`_get_pillar_details` 默认 50。这些默认值经加权计算后输出"STRATEGIC HEALTH SCORE: 61.3/100"式的伪精确结论。**该行为直接威胁 SCORING 的 SCOPE-03 / NEG-01 / CF-02**——agent 跑脚本把默认值当分析结果转述，即构成"呈现未提供的公司数据" |
| A3 | **硬编码成功指标与占位符** | 中 | `_create_strategic_roadmap` 无视输入，固定输出 "Revenue growth: 25% YoY"、"Market share: +5pp"、"EBITDA margin: +8pp"、"NPS >70"、"Engagement >80%"；`resource_requirements` 含 `'$X million investment over 18 months'` 裸占位符。路线图因此与输入数据零关联 |
| A4 | **建议生成以输入为条件但内容模板化** | 中 | 选项（Market Leadership / Profitability Turnaround / Expansion / Digital Transformation / M&A）由阈值触发，内容全部为固定文案；`_generate_recommendations` 的薄弱分支只处理 5 支柱中的 3 个（operational_excellence、growth_potential 弱时不生成针对性建议） |
| A5 | **阈值武断** | 低 | BCG 分类用 share>50 / growth>10 的绝对阈值；M&A 触发需 cash_available>1 亿，无比例依据；框架阈值（<60/<50/>70）无来源说明 |
| A6 | **输出截断丢信息** | 低 | `analyze_strategy` 只输出每支柱前 2 个 factor、前 3 个选项、前 3 个阶段、前 5 条建议，rest 静默丢弃 |
| A7 | **输出含装饰性 emoji** | 低 | 🚨/⚠️/✓/⭐ 出现在建议文案中（"🚨 URGENT: ..."），与 SKILL.md 的 ✅/⚠️ 装饰问题同源 |

### 8.3 优点（为公允计）

- 权重体系与风险公式自洽；`_calculate_industry_attractiveness` 的"力越低越吸引"处理正确。
- 输出报告结构清晰（score / pillars / options / risk / roadmap / recommendations），是 OUT-01 想要的"结构化输出"的现成模板——只是它把这种结构封装进了脚本而不是 SKILL.md。
- 示例数据完整可运行，作为自测夹具质量尚可。

---

## 9. scripts/financial_scenario_analyzer.py 审查（Script Review B）

### 9.1 架构

- 多场景 3 年投影（4 种 growth model）+ NPV/IRR + break-even + return multiple + 敏感性 + 风险调整 + 推荐，管线完整。
- 输出报告（base case 摘要 / 场景明细 / 风险调整 / 推荐）结构清楚。

### 9.2 已复现的数值缺陷（全部实跑确认）

| # | 缺陷 | 复现结果 |
|---|------|----------|
| B1 | **增长模型双重复利**：`_project_year` 把 growth model 作用在当前状态上，而当前状态每轮被上一轮投影覆盖；exponential 模型在 year 参数 1/2/3 下逐轮放大 | base 5M、rate 0.3：y1=6.50M，y2=10.99M，y3=24.13M；y3/y1 系数 3.71，而正确 30% 复利应为 1.3²=1.69。**3 年增长被夸大约 2.2 倍**，NPV/IRR/推荐全部随之失真 |
| B2 | **IRR 数学域错误**：`math.pow(total_return/initial_investment, 1/years)` 在累计现金流为负时抛 `ValueError: math domain error` | 三条负现金流 + 正初始投资 → 直接崩溃。场景分析只要含一个全负方案即炸整个流程 |
| B3 | **break-even 索引回绕**：`projections[projection['year']-2]` 在 year=1 时取 `projections[-1]`（即第 3 年投影）；且 year=1 的 ebitda>0 分支直接返回 12 个月、跳过插值 | 实测 year-1 盈利场景返回 12；year=1 时"前一年"实际取的是第 3 年数据，插值语义全错 |
| B4 | **敏感性分析是常数表**：`_calculate_variable_impact` 使用固定 `base_value = 10000000` 与固定乘子（growth 2.5 / margin 1.8 / CAC -1.2），与输入的 base case 完全无关；且名为"recompute"实为查表 | 敏感性结果对所有输入恒为 10M×(1±0.2×2.5) 等固定值 |
| B5 | **NPV 不含初始投资**：`_calculate_npv` 只折现 FCF，推荐逻辑却用 NPV×概率 选场景，投资规模被排除在决策之外；IRR 公式实为"累计回报 CAGR"而非 IRR | 语义不一致：NPV 未减投资而 IRR 除以投资 |
| B6 | **"风险调整"计算了但从未使用**：`risk_adjusted_view`（expected value / std dev / sharpe）算完后，`_generate_recommendation` 只取 `max(NPV×prob)`，std dev/sharpe 从不出现在决策里；sharpe 用场景 NPV 的离散分布计算，概念上不成立 | 白算 + 误导性指标 |
| B7 | **推荐内容恒定**：`key_actions` 永远是同一 5 条（"Secure funding..." 等），与任何场景输入无关；10x revenue 估值倍数硬编码并声明"For SaaS"却用于所有行业 | 输出与输入脱钩 |
| B8 | **无输入管道（同 A1）** | `__main__` 硬编码 5M 收入示例；Quick Start 的 `python scripts/financial_scenario_analyzer.py` 无法分析用户场景 |
| B9 | **runway 无穷值**：burn_rate≤0 时返回 `float('inf')`，报告格式化为 "inf months" | 边界可接受但无说明 |

### 9.3 总结评

该脚本的 B1（增长夸大 2.2 倍）与 B2（崩溃）属于**正确性缺陷**，会让依赖它的 agent 输出错误的资金建议；B4/B7 属于**虚假计算**（输出看起来是模型结果，实为常数），与 SCORING 反编造精神直接冲突。修复优先级见 §13。

---

## 10. references/ 三文件审查（Reference Files）

三个 reference 均远超 SKILL.md 的使用方式（SKILL.md 只做了 3 行"去读它"的桥接），单文件质量整体高，逐一点评：

### 10.1 references/executive_decision_framework.md

- DECIDE 五步框架、growth 决策矩阵（加权表）、M&A 尽调四段、capital allocation 优先级、budget 决策树、restructuring 触发条件、leadership 评估矩阵、crisis 响应协议与**四级**决策权限表、SWOT-TOWS/BCG/Risk-Impact/Eisenhower 四矩阵、Porter 三战略、Blue Ocean 四动作、stakeholder 映射、balanced scorecard、认知偏差清单、board 演示模板、IR 框架、年度规划、退出策略。
- 亮点：决策偏差清单（confirmation/anchoring/sunk cost/overconfidence/availability + 对策）是全书最稀缺的内容，对"agent 帮 CEO 决策"场景直接有用。
- 问题：与 SKILL.md 的三处分歧（capital allocation 4 档 vs 5 档、crisis 4 级 vs 3 级、stakeholder 象限标签 Key Players vs Keep Satisfied）——详见 §11。

### 10.2 references/board_governance_investor_relations.md

- Board 构成（7-9 人、独立多数）、角色表、年度会议日历、T-4w/T-2w/T-1w/T-0 准备时间线、package 模板、月度更新邮件模板、flash report、难对话处理、机构/零售投资者细分、earnings release 模板、earnings call 脚本（CEO 5min/CFO 10min/Q&A）、investor day 6 个月时间线、股东激进防御四阶段、法规表（10-K/10-Q/8-K/DEF 14A/S-1 时间窗与实际法规一致）、FD 合规、IR 危机通信小时级响应、IR KPI、董事会评估、executive session、D&O（Side A/B/C 正确）、ESG 报告框架、board resolution / insider trading / proxy 三个模板。
- 亮点：earnings release 与 call 脚本是可直接落地的交付物模板；Reg FD / 8-K 时间窗等法规细节准确。
- 问题：board package 组件与 SKILL.md 的 6 组件清单（CEO Letter/Dashboard/Financial/Strategic/Risk register）不一致（reference 是 Cover Memo/CEO Report/Financial/Strategic/Committee Reports），见 §11。

### 10.3 references/leadership_organizational_culture.md

- 领导力五维、文化维度模型（innovation↔stability 等四轴）、4 阶段文化转型路线图（与 SKILL.md 时间线一致）、executive team charter、succession 时间线（与 SKILL.md 一致）、9-box 人才网格、领导力胜任力模型、内部沟通渠道表、CEO 沟通日历、敬业度 8 维框架、OKR 模板与示例、绩效节奏、8 步变革、组织设计原则、重组 playbook、危机领导力、创新三地平线（70/20/10）、DEI 四支柱、高管形象（PREP/STAR）。
- 亮点：OKR 示例（NPS 45→70 等）具体可执行；9-box 的开发策略按格给出；危机沟通频率（2x daily）具体。
- 问题：CEO 沟通日历节奏与 SKILL.md 版本不一致（SKILL.md 每周 board member update，reference 是每月 board touchpoint），见 §11。

---

## 11. 跨文件一致性与重复度分析（Cross-File Consistency & Redundancy）

### 11.1 不一致清单（5 处，全部位于 SKILL.md 与 references 之间）

| # | 主题 | SKILL.md | reference | 影响 |
|---|------|----------|-----------|------|
| C1 | Capital allocation | 5 档：Core Ops 40-50 / Growth 25-35 / Innovation/R&D 10-15 / Strategic Reserve 10-15 / Returns varies | 4 档：Essential 40-50 / Strategic 30-40 / Efficiency 10-15 / Experimental 5-10 | 两套完全不同的分配框架；且两组端点值域均为 85%–115% 不闭合。agent 依 skill 建议"40% 核心 + 40% 战略"时无从判断该听哪个 |
| C2 | Crisis 分级 | 3 级：L1 department / L2 company / L3 existential（CEO 直接接管） | 4 级：L1 department head / L2 C-suite / L3 CEO / L4 CEO+Board | 级数不同、决策权映射不同；SCORING PROC-08 按 SKILL.md 的 3 级措辞设计，agent 若读 reference 会按 4 级回答，与 judge 期望冲突 |
| C3 | Board package | 6 组件（CEO Letter 1-2p / Dashboard 1p / Financial 5p / Strategic 10p / Risk register 2p / Appendices） | 6 组件（Cover Memo 1p / CEO Report 3-5p / Financial 5-10p / Strategic 10-15p / Committee Reports 2-3p / Appendices） | 组件名与页码两套；SCORING PROC-06 的期望清单（CEO letter, dashboard, financial, strategic, risk register）只与 SKILL.md 匹配 |
| C4 | Stakeholder 象限标签 | Keep Informed / Manage Closely / Monitor / **Keep Satisfied** | Manage Closely / Key Players / Monitor / Keep Informed | 标签命名分歧（Keep Satisfied vs Key Players）；SCORING PROC-04 用 SKILL.md 措辞 |
| C5 | CEO 沟通节奏 | Weekly: board member update；Monthly: board report | Weekly: exec team/leadership cascade；Monthly: board touchpoint | 与董事会沟通频率矛盾（每周 vs 每月） |

一致的部分（正面）：culture 转型时间线、succession 时间线、decision checklist 主干（8 vs 9 项仅数量差，内容重叠）、earnings cycle、board 准备时间线在 SKILL.md 与 reference 间完全对齐——说明不一致不是系统性粗心，而是复制-发散。

### 11.2 重复度分析

以下内容在 SKILL.md 与 references 中**逐项重复书写**：

- Culture Transformation Timeline（§4 ↔ culture.md Phase 1-4）
- CEO Succession Timeline（§Succession ↔ culture.md 同节）
- Board 准备时间线（§Board ↔ board.md T-4w 起）
- Capital Allocation（§2 ↔ decision.md 同节）
- Stakeholder 矩阵（§3 ↔ decision.md 映射图）
- Decision Checklist（§Critical ↔ decision.md Hygiene Checklist）
- CEO Communication Calendar（§5 ↔ culture.md 同节，且细节不一致=C5）

估计重复约 120-150 行。这违反 §3.4 知识增量原则，且是 C1-C5 发散的温床（同一事实写两遍，必有一遍过期）。整改方向（§13 P2）：SKILL.md 保留"何时读哪个 reference + 一句话要点"，细节全部下沉。

### 11.3 逻辑自洽抽查（正向）

- SKILL.md 内部无矛盾：月度/季度/年度节拍表相互吻合；数字（页码、页数、百分比）自洽（除 §1.3 已修正的资本配置端点）。
- 脚本内部：strategy 权重和 = 1.0；financial 的 3 年投影环、NPV 折现年限一致。
- SCORING 与 SKILL.md 锚点映射完整（§5.3）。

---

## 12. 人机感、语气与风险画像（Tone & Risk Profile）

### 12.1 人机感

- 主体语气：正式、中性、目录式，无口语填充，符合 CEO 顾问场景的严肃预期。dossier 评价"正式中性"成立。
- 装饰性 emoji：Success Metrics 的 8 个 ✅ 与 Red Flags 的 8 个 ⚠️ 是纯装饰（不携带状态信息，每行一个），与脚本输出的 🚨/✓/⭐ 同源。占 16+ 处，建议删除或改为纯文本符号。
- 排版瑕疵：Red Flags 的 7 行（494-500 行）有**行尾双空格**（"consistently  "、"turnover  " 等），是批量粘贴痕迹，markdown 渲染会出现意外换行。
- 面向 agent 的指令密度低：全篇几乎没有祈使性执行指令（"先做 X"），读者（agent）无法从语气上判断它是可执行协议还是参考手册——这放大了 §5.1 的结构缺陷。

### 12.2 风险画像

| 风险 | 来源 | 触发场景 | 关联 criterion |
|------|------|----------|----------------|
| 数据编造（最高） | 脚本默认值造假（A2/B4/B7）+ body 无反编造禁令 | agent 无公司数据时跑脚本并把默认输出当结论转述 | SCOPE-03 / NEG-01 / CF-02（cap_to_0） |
| 领域漂移 | 7 领域无路由逻辑；description 触发面过宽 | 用户说 "board meeting" 时 agent 同时倾倒 culture 模板 | SCOPE-01 / OUT-01 |
| 参考倾倒 | references 内容丰富但 SKILL.md 无"怎么用"指令 | agent 读完全部 3 个 reference 后输出目录式长文 | OUT-01 / CF-01（cap_to_0） |
| 数值失真 | B1 增长夸大 2.2 倍、B2 崩溃、B3 回绕 | 任何财务场景建模请求 | PROC-03（check 只验提及，验不出） |
| 框架冲突 | C1-C5 双框架并存 | 资本配置/危机分级/board package 类问题 | PROC-05/06/08 判断不稳定 |

### 12.3 总评定位

SKILL.md 本体 🟡（知识正确、合规半达标、缺节）；scripts 🟠（正确性 + 数据完整性）；references 🟢。综合：**🟡，P1 修复后可转 🟢**。它仍是 322 个 skill 中少数"目录完整 + 引用齐全 + 评测标准有真实锚点"的样本，基础面好于 corpus 平均。

---

## 13. 详细整改建议（Remediation Plan，按优先级）

本节约 90 行。共 22 项整改，按 P0（正确性/数据完整性，阻止使用）→ P1（结构合规，阻止评测公平）→ P2（一致性/打磨）→ E（评测侧）四级组织，每项含动作、期望产出与验收标准。

### 13.1 P0 — 正确性与数据完整性（4 项，优先于一切）

**P0-1. 为两个脚本增加输入管道**

- 动作：`strategy_analyzer.py` 与 `financial_scenario_analyzer.py` 各支持 `python scripts/xxx.py --input company.json`（或 `-` 读 stdin）；`__main__` 示例改为仅在 `--example` 显式请求时运行。
- 期望产出：agent 可用一条命令把用户公司数据送入脚本并得到基于真实输入的报告。
- 验收：无参数运行时打印 usage 而非示例；`--example` 输出与现状一致；`--input` 输出随输入变化且不出现示例公司名。
- 关联：SKILL.md Quick Start 同步更新为 `--input` 用法。

**P0-2. 移除脚本默认值造假**

- 动作：`_apply_frameworks` 的 SWOT/ Porter 默认填充改为 `None`；`_analyze_pillar`/`_get_pillar_details` 对缺失数据不再返回 50.0 默认分，而是输出 "insufficient data" 状态；对缺失因子不足的支柱，战略健康分标注"数据不完整，分数仅供参考"。
- 期望产出：脚本永远不能"无中生有"地打印公司事实。
- 验收：空输入字典时报告出现明确缺数据标注，不再输出 50/100 伪分数或 "Strong brand recognition" 类事实。
- 关联：这是 NEG-01/CF-02 的脚本侧防线，也是 P0 中最关键的一项。

**P0-3. 修复 financial_scenario_analyzer 的 4 个数值缺陷（B1-B4）**

- 动作：
  1. B1 增长模型：改为 `revenue_y = base_revenue * (1+rate)^y`（或增量 `*(1+rate)` 逐年）单次作用，消除双重复利。
  2. B2 IRR：改为标准二分法/牛顿法求解，或对负累计回报返回 `None` 并在报告中标注"不可计算"。
  3. B3 break-even：引入显式 `prev_projection` 变量，year=1 用 base case 的 ebitda 做前值；year=1 盈利也走插值分支。
  4. B4 敏感性：改为对模型真实重算（把 growth_rate/margin 参数 ±20% 后重新投影），或删除并标注"示例乘子，非模型计算"。
- 验收：复测三个复现用例——30% 增长 3 年系数 = 1.69；负现金流场景不崩溃；year-1 盈利场景 break-even 为插值结果。
- 关联：B 类缺陷修复后，PROC-03 的"执行脚本"才算有意义的行为。

**P0-4. 参数化硬编码输出**

- 动作：roadmap 成功指标（25% YoY 等）、"$X million"占位符、10x revenue 倍数、key_actions 固定 5 条全部改为输入参数或由模型推导；无法推导的标注为示例占位。
- 验收：两份报告即使输入不同，输出不再出现相同绝对数值。

### 13.2 P1 — 结构与合规（5 项，SKILL.md 三节 + 体量 + 纪律）

**P1-1. 补 ## Output Format 节**

- 动作：在 body 增加"## Output"节，规定交付物结构：① 领域判定（strategy/financial/board/IR/culture/crisis/succession）② 使用的框架与脚本 ③ 结构化产出物（决策矩阵 / board agenda / 沟通日历 / scorecard 四选一或组合）④ 每条建议的成功度量 ⑤ red flags。每条给 1-2 行格式示例。
- 期望产出：OUT-01/OUT-03 有了可引用的正文依据。
- 验收：正文中出现显式 Output 标题且内容可判真伪。

**P1-2. 补 ## Scope / Limitations 节**

- 动作：明确四条——(a) 不替代法律/财务/证券合规意见；(b) 需要用户提供公司数据，数据缺失时必须先索取、不得编造；(c) 7 个领域的边界与"何时不用本 skill"（如纯运营执行、非 CEO 决策场景）；(d) 脚本输出为辅助分析，重大决策需人工复核。
- 期望产出：SCOPE-03/NEG-01/CF-02 有了正文级禁令锚点。
- 验收：正文出现 Scope 标题；出现显式"不得编造财务/市场数据"语句。

**P1-3. 补顶层 ## Workflow 节**

- 动作：在 Quick Start 之后增加 5 步执行主线：① 识别领域（7 选 1，多领域时定优先级）→ ② 收集数据（缺则问）→ ③ 选择工具（决策类→executive_decision_framework；场景建模→financial 脚本；战略分析→strategy 脚本；其余→对应 reference）→ ④ 执行并产出结构化交付物 → ⑤ 校验（red flags、成功度量、无编造）。
- 期望产出：§3.1 的 Workflow 节补齐，且给 SCOPE-01/PROC 系列一个可执行的分支依据。
- 验收：一个不熟悉该 skill 的 agent 读 Workflow 后能独立跑通完整任务。

**P1-4. 体量治理（pattern 匹配）**

- 二选一：把重复内容（§11.2 列出的 7 块）下沉 references 后压到 ~200-300 行并保持 `pattern: mindset`；或把 SCORING 的 `pattern` 改为 `process`（~200 行目标）。推荐前者。
- 期望产出：body 与 pattern 自洽；agent 不至于在无数据时被 497 行目录淹没。
- 验收：body 行数、pattern 字段、实际形态三者一致。

**P1-5. 反编造纪律写入 body + 修排版**

- 动作：在 Quick Start 或新 Workflow 内加一句显式纪律（"NEVER present financials, market data, valuation, or cap table as known facts unless provided by the user"）；删除 Red Flags 7 处行尾双空格；清理 16 处装饰性 emoji 或改为纯文本标记。
- 验收：文件无行尾空白；✅/⚠️ 出现次数为 0 或仅存于功能性上下文。

### 13.3 P2 — 跨文件一致性（5 项）

**P2-1. 统一资本配置框架（C1）**

- 动作：二选一，推荐保留 SKILL.md 的 5 档并删掉 reference 的 4 档（或反之）；无论留哪套，重算区间使端点闭合为 100%（如 40-50/25-35/10-15/10-15 + Returns 0-15 显式写明弹性）。
- 验收：文档中只存在一套分配框架，且任意组合值域 ⊆ 100%。

**P2-2. 统一危机分级（C2）**

- 动作：SKILL.md 3 级与 reference 4 级择一。若保留 3 级，reference 的 L4 合并进 L3 描述；SCORING PROC-08 措辞随之确认（建议 judge 提示词同时携带两处文本以防 agent 读了 reference 答 4 级）。
- 验收：全文仅一套级数与决策权映射；PROC-08 问题文本与文档一致。

**P2-3. 统一 board package（C3）**

- 动作：以 SCORING PROC-06 的期望（CEO letter, dashboard, financial review, strategic updates, risk register, appendices）为准统一两处组件与页码。
- 验收：SKILL.md 与 reference 的 package 清单逐项一致。

**P2-4. 统一 stakeholder 标签与沟通节奏（C4/C5）**

- 动作：象限标签统一为 Keep Informed / Manage Closely / Monitor / Keep Satisfied（与 PROC-04 措辞一致）；沟通日历统一为每周 exec team、每月 board touchpoint。
- 验收：两文件相关表格逐字一致。

**P2-5. 决策清单数量对齐**

- 动作：SKILL.md 8 项与 reference 9 项取一（推荐合并为 9 项，reference 的 biases 检查与 review process 有价值）。
- 验收：两处清单逐项一致。

### 13.4 E — 评测侧（4 项）

**E-1. 升级 SCOPE-02 / PROC-03 为使用级证据**

- 动作：SCOPE-02 改为 `tool_log_order(Read 某 reference, 其后出现输出/回答引用)` 或 `output_contains('framework|matrix|checklist')` 之一；PROC-03 改为要求 Bash 调用且 `output_contains('=== Financial Scenario Analysis ===')`。
- 验收：agent 只读不用的行为不再得分。
- 权衡：升级后对"正确但没用脚本"的 agent 更严格，符合评测意图。

**E-2. 新增"先索取数据"criterion**

- 动作：在 scope 类新增一项（judge: llm）："公司数据缺失时，agent 是否显式索取而非自行假设"。
- 验收：total_items 更新为 18，check.py 注释同步。

**E-3. 为 LLM judge 提供跨文件锚点**

- 动作：PROC-05/06/08 的 judge 输入拼接 reference 对应小节，避免 judge 只拿 SKILL.md 时把 reference 式回答误判（C1/C2 未修复前尤其必要）。
- 验收：judge 提示词中可见两处文本的摘录。

**E-4. 保留并强化 CF-01/CF-02**

- 动作：维持 cap_to_0 语义；在任务提示模板里为测试题补充"不提供财务数据"约束，使 CF-02 成为稳定判别器。
- 验收：无触发对照组中编造率可观测、可统计。

### 13.5 整改顺序与工作量

| 批次 | 内容 | 预计工作量 |
|------|------|:----------:|
| 第一批（P0-1 至 P0-4） | 脚本输入管道 + 反造假 + 数值修复 + 参数化 | 0.5-1 天 |
| 第二批（P1-1 至 P1-5） | 三节补齐 + 体量治理 + 纪律与排版 | 0.5 天 |
| 第三批（P2-1 至 P2-5） | 跨文件统一 | 0.5 天 |
| 第四批（E-1 至 E-4） | SCORING/check.py 调整 + 文档 | 0.5 天 |

优先执行 P0-1/P0-2 与 E-1：前者决定该 skill 是否能在实验中产生可信输出，后者决定评测是否公平。全部完成后预计评级可达 🟢，并可列入"纪律型"样本参与 2×5 测评矩阵。

### 13.6 复检清单（回归项）

- [ ] 脚本：`--input` 管道可用、空数据标注明确、B1-B4 复现用例通过
- [ ] SKILL.md：Output / Scope / Workflow 三节存在且可判真伪；无行尾空白；无装饰 emoji
- [ ] 一致性：C1-C5 复检表全绿
- [ ] SCORING：total_items 与 criteria 数一致；script 检查为使用级
- [ ] check.py：随 SCORING 更新后实测通过两个 fixture（读不用的失败 / 真用的通过）
