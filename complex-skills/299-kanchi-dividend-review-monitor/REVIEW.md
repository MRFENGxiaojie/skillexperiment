# REVIEW — 299-kanchi-dividend-review-monitor 技能深度审查报告

- 审查日期：2026-08-06
- 审查对象目录：`D:\SkillIF\skill-experiment\complex-skills\299-kanchi-dividend-review-monitor`
- 审查基准：`complex-skills\_shared\SKILL-SPEC.md` v1.0（12 项合规清单）
- 审查方式：目录内全部 10 个文件逐文件全文通读（无抽样），并做实测验证（规则引擎冒烟、20 个单元测试逐一执行、check.py 端到端运行、YAML/JSON 解析校验、语料库交叉检索）
- 结论：整体质量良好（引擎、测试、评分链可运行且相互印证），主要问题集中在规格合规缺项（无 Scope/Limitations 节）、文档与引擎的行为不一致（T4 关键词集、ETF 分母、flat-dividend 描述、T6 口径）、以及若干测评健壮性缺陷。综合得分 74/100。

---

## 1. 目录全量清单

本目录共 10 个文件，全部经逐字通读（Read full-text），行数按含末尾换行计：

| 文件 | 行数 | 字节/备注 | 角色 |
|---|---|---|---|
| SKILL.md | 130 | 5.4 KB | 技能主文档（frontmatter 4 行 + 正文 126 行） |
| SCORING.yaml | 207 | 11.6 KB | 21 项测评标准（3 scope / 6 process / 3 decision / 4 format / 2 technical / 2 negative / 1 qa）+ 3 条 critical_failures |
| check.py | 113 | 3.6 KB | 9 项脚本化检查的实现（另有 12 项 LLM 评审项） |
| agents/openai.yaml | 3 | — | 孤立文件，SKILL.md 未引用 |
| references/input-schema.md | 72 | — | 输入 JSON schema 与样例 payload |
| references/review-ticket-template.md | 32 | — | REVIEW 人工复核工单模板 |
| references/trigger-matrix.md | 43 | — | T1-T6 触发矩阵、T2 分母映射、升级规则 |
| scripts/build_review_queue.py | 533 | — | T1-T6 确定性规则引擎 + 报告渲染 |
| scripts/tests/conftest.py | 6 | — | pytest 路径 fixture（把 scripts/ 加入 sys.path） |
| scripts/tests/test_build_review_queue.py | 294 | — | 20 个单元测试 |

语料库交叉检索结果：兄弟技能 `013-kanchi-dividend-us-tax-accounting` 存在于两套语料（complex-skills 与 complex-skills-no-trigger）中；**`kanchi-dividend-sop` 在本语料库两套集合中均不存在**，但本技能有 3 个文件（SKILL.md、input-schema.md、trigger-matrix.md）引用了它（详见 5.1、5.2、8.4、13 节）。

---

## 2. Frontmatter 审查

### 2.1 name 字段

- 值：`kanchi-dividend-review-monitor`（29 字符，小写 + 连字符，≤64 合规）。
- 与目录名 `299-kanchi-dividend-review-monitor` 的比对：按语料库既定约定（`NNN-` 为序号前缀，SKILL-SPEC §4），name 与目录去除序号后完全一致。✅

### 2.2 description 字段 — WHAT

- "Monitor dividend portfolios with Kanchi-style forced-review triggers (T1-T5) and convert anomalies into OK/WARN/REVIEW states without auto-selling."
- 第三人性陈述，动词开头的描述式写法与 SKILL-SPEC §2.6 官方"好例子"（"Generate comprehensive test plans..."）同构，不算祈使违规。✅
- 内容具体：写明了监控对象（dividend portfolios）、机制（T1-T5 forced-review triggers）、输出（OK/WARN/REVIEW states）、红线（without auto-selling）。WHAT 完整。✅
- 小问题：触发体系统称为 "T1-T5"，但引擎/矩阵/评分均含 T6（见 4.1），口径不一致。

### 2.3 description 字段 — WHEN 与触发信号（§2.4）

- "Use when users ask for dividend cut detection, 8-K governance monitoring, dividend safety monitoring, REVIEW queue automation, or periodic dividend risk checks."
- 触发场景列举充分（cut detection、8-K、safety monitoring、queue automation、periodic risk checks）。✅
- 触发信号短语为 "Use when **users** ask for..."，与 SKILL-SPEC §2.4 的规范短语列表（"Use when the user..." / "Use when the user asks to..." / "Use when the user needs to..." / "Triggers on..." / "Use for..."）存在偏差：复数 "users" + "ask for" 并非列表中任何一项的原文。功能上可识别，但本项目（SkillIF）恰是以 trigger 描述遵从度为核心测量对象，建议一字不差对齐规范短语："Use when the user asks to..."（见 13 节 🔴 修复项 F-02）。⚠️

### 2.4 description 字段 — 长度与关键词

- 实测长度：308 字符（≤1024 合规）。✅
- KEYWORDS：dividend cut detection、8-K、governance、safety monitoring、REVIEW queue、risk checks 均在列，覆盖度高。✅
- 无跨技能路由（"NOT for X, use Y"）嵌入描述；无泛化空话（非 "A useful skill"）；长度远超 40 字符下限。✅

### 2.5 Frontmatter 键集合

- 实测解析（PyYAML safe_load 通过）：仅 `name` 与 `description` 两个键，全部落在允许清单（§1.1）内，无任何 §1.3 禁键（无 metadata/license/version/tags/trigger 等）。✅
- 注意：`agents/openai.yaml` 这个文件与 §1.3 禁止的 frontmatter 键 `agents` 无关（那是 SKILL.md frontmatter 的规则），但它本身是目录内无引用的孤立文件，见 5.6 与 13 节。

---

## 3. Body 结构分析

### 3.1 必备三节

- **Workflow / Process** ✅ — "## Workflow" 四步：1) Normalize input dataset → 2) Run the rule engine（含命令）→ 3) Prioritize and deduplicate → 4) Generate human review tickets。步骤清晰、每步有输入输出指向。
- **Output Format** ✅ — "## Output Contract" 明确三条交付物：Queue JSON（summary counts + ticker 级 findings）、Markdown dashboard、REVIEW tickets 清单。与脚本输出和 SCORING FMT-01~03 一一对应。
- **Scope / Limitations** ❌ — **全篇没有名为 Scope / Limitations（或等价语义）的独立小节**。目前相关内容散落各处：Non-Negotiable Rule（32-35 行，"Never auto-sell..."，语义上是安全红线而非范围声明）、Flat-dividend cadence caveat（45-47 行，属边界行为说明）、SEC Filing Guardrail 末尾一句 "not a full governance clearance"（108 行，属局限性）。按 SKILL-SPEC §3.1，该节必须回答"本技能不做什么、何时不应当使用"，目前缺失。这是本技能最大的规格合规缺口（见 13 节 🔴 F-01）。

### 3.2 行数

- 正文 126 行（总 130 行含 frontmatter），远低于 600 行硬上限，符合 tool 型技能 ~300 行目标线（目前偏紧凑，无过度冗余）。✅

### 3.3 文件引用

- 正文内引用全部为技能内相对路径：`references/input-schema.md`、`references/trigger-matrix.md`、`references/review-ticket-template.md`、`scripts/build_review_queue.py`、`scripts/tests/test_build_review_queue.py`，均真实存在。✅
- 无 `../other-skill/` 跨技能路径。⚠️ 但 Workflow 第 2 步命令中出现了 `skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py` 这种带仓库前缀的路径（78 行），在本语料库布局（`complex-skills/299-kanchi-dividend-review-monitor/`）下不成立，照抄即失败（见 4.4 与 13 节 🔴 F-03）。
- Multi-Skill Handoff（117-121 行）以 prose 方式提及 `kanchi-dividend-sop`、`kanchi-dividend-us-tax-accounting`，符合 §3.3 "用技能名在正文中提及"的写法。⚠️ 但前者在本语料库不存在（见 5.1/5.2）。

### 3.4 内容质量（§3.4 四原则）

- 知识增量：没有铺垫模型已知的基础概念（如"什么是股息"），直接进入状态机与触发规则。✅
- 反模式优先：Non-Negotiable Rule、Flat-dividend caveat 都是"明确的不该做什么 + 理由"，符合规范。✅
- 决策树/表格化：触发规则没有在正文重复展开，而是指向 trigger-matrix.md 表格，避免双源漂移。✅
- 具体性：命令、阈值（0.99、WARN/REVIEW 状态）、示例文件名（review_queue_20260227.json）都是具体值。✅

### 3.5 结构细节

- 小节层级：H1（标题）→ H2（12 节）→ H3（Workflow 下的 1)~4) 步骤）。层级干净。
- "## State Machine" 下嵌套 "### Flat-dividend cadence caveat"，位置合理（紧邻状态定义）。
- "## Monitoring Cadence"（49-57 行）把 T1/T4 归 Daily、T3 归 Weekly、T2/T5 归 Quarterly，但**漏掉了 T6**（trigger-matrix 中 T6 为 Daily）；且整节口径为 T1-T5（见 4.1）。
- 小节排序从"是什么"（Overview）到"何时用"（When to Use）到"前提"（Prerequisites）到"规则"再到"流程"再到"输出"，阅读顺序自然。

---

## 4. 逻辑一致性

### 4.1 触发体系口径：T1-T5 还是 T1-T6

这是全技能最普遍的口径漂移，涉及 6 处：

| 位置 | 口径 |
|---|---|
| SKILL.md:3（description） | "triggers (T1-T5)" |
| SKILL.md:51-57（Monitoring Cadence） | 只列 T1-T5，无 T6 |
| SKILL.md:83（Workflow 第 2 步） | "maps each ticker to OK/WARN/REVIEW based on T1-T5" |
| SKILL.md:126（Resources） | "unit tests for T1-T5 and report rendering"（测试实际覆盖 T1-T6） |
| trigger-matrix.md:1（标题） | "Trigger Matrix (T1-T5)"，正文含 T6 行 |
| build_review_queue.py、SCORING（FMT-03/PROC-04 用 `T[1-6]`） | 均含 T6 |

T6（dividend-policy change，基于 WS-1 标志）是引擎真实实现并被 SCORING 与测试充分覆盖的功能。建议全量统一为 T1-T6（见 13 节 F-04）。

### 4.2 文档所述行为 vs 引擎实际行为

- **Flat-dividend caveat（SKILL.md:45-47）**：caveat 说"当 T6 仅由 freeze_flag / 最新常规股息等于上期常规股息驱动时，按 WARN 处理"。但引擎的 `t6_dividend_policy_change`（build_review_queue.py:312-370）**只在 WS-1 标志存在时触发**，"latest == prior 且无任何标志"的持仓不会产生任何 finding（T1 要求 `< prior * 0.99`），最终状态是 OK。也就是说：文档描述了一个引擎无法产生的 T6 场景。SCORING PROC-06 / NEG-02 的提问同样基于这个不存在的场景，评审时条件永远不成立（评审者可能因此跳过或误判）。需二选一：改文档（明确"平股息无标志 = 无机器触发，由 Agent 以说明性 note 提示，不构成 WARN"），或给引擎加"平股息 → WARN(cadence)"规则。
- **T4 关键词集**：引擎 `T4_KEYWORDS`（build_review_queue.py:26-32）只有 5 个（item 4.02、non-reliance、restatement、material weakness、sec investigation）；SKILL.md SEC Filing Guardrail（108 行）与 SCORING TEC-02（161 行）列的是 9 词族（另含 subpoena、going concern、auditor resignation、internal control）。若 Agent 按 Guardrail 抓取文本（如仅命中 "going concern"），引擎不会产出 T4 finding，文档与引擎行为脱节。
- **ETF 分母**：trigger-matrix.md:35 与 SCORING DEC-02 说 ETF 用 "holdings-level quality proxies"；引擎 `INSTRUMENT_DENOMINATOR`（build_review_queue.py:20-25）把 etf 映射为 `fcf`（基金层面现金流），从未读取任何持仓层面代理指标（输入 schema 也没有该字段）。文档描述的降级路径在引擎中不存在。
- **T5 边界**：trigger-matrix T5 行写 "2+ simultaneous negatives → WARN/REVIEW"，未界定 2 与 3+ 的区分；引擎实际是 score≥2 → WARN、score≥3 → REVIEW（build_review_queue.py:294-307），测试也验证了这一边界。建议矩阵补一句边界说明（见 13 节 🟢 F-15）。

### 4.3 文档、SCORING 与 check.py 的互相印证

- 总体自洽：SCOPE-02 的最小字段（ticker/instrument_type/dividend）与 SKILL.md Prerequisites（26-30 行）一致；PROC-02 的 dated 文件名（review_queue_YYYYMMDD.json/.md）与脚本 main() 的命名逻辑（build_review_queue.py:506,514,522，date_suffix = as_of 去连字符）一致；PROC-04 的 `- \`T[1-6]\` \`(OK|WARN|REVIEW)\`` 与 render_markdown 的 Findings 行格式（build_review_queue.py:453）一致（已实测匹配）。
- **QA-01 描述与检查不一致**：SCORING QA-01 描述（189-191 行）声称校验"dated 文件名后缀与 as_of 日期一致"，但实际检查（check.py:84-88，json_field_exists + min_present=2）只验证 queue JSON 中存在 generated_at 与 as_of 两个字段，**根本未校验文件名后缀**。Agent 产出 review_queue_99999999.json 也能通过 QA-01。
- **SCOPE-02 描述与检查不一致**：SCORING SCOPE-02 描述（22 行）说输入须含 "as_of + holdings array"，但检查只校验 holdings 元素的三个键，as_of 未校验。
- **PROC-01 可被绕过**：`tool_log_contains("build_review_queue")`（check.py:48）会搜索工具日志中**任意** JSON 条目（checker.py `_log_search` 对整个条目 json.dumps 后正则匹配）。Agent 只要 Read 一下 `scripts/build_review_queue.py`（文件路径本身就含 "build_review_queue"），或 Read 包含该脚本名的 SKILL.md 行，即可在不执行脚本的情况下通过 PROC-01。建议把模式限定为 Bash/执行类工具条目，或要求更具体的命令形态（如 `--input`）。
- **PROC-02 与 FMT-01 完全重复**（check.py:49-51 与 67-69，同一 file_exists 检查），冗余但无害；建议 FMT-01 改为校验"三件套输出"中其余部分（如 tickets 列表）以增强区分度。
- check.py 硬编码 `reports/` 子目录（check.py:32-34）：若 Agent 按 SKILL.md 以外的输出习惯（如 --output 单文件）执行，即便产出正确也会失败；SKILL.md 第 2 步已用 --output-dir reports/ 约束，尚可接受，但值得在技能中显式说明"输出必须落在工作区 reports/ 下"。
- 空持仓边界：`json_array_all_have_keys` 对空数组返回 False（checker.py:171-172），空投资组合（holdings: []）会导致 SCOPE-02 与 PROC-03 双双判失败，而空组合是合法输入（测试 test_build_report_handles_empty_holdings 也支持空组合）。测评层对空输入无容错路径。

### 4.4 术语与外部引用一致性

- **WS-1 / WS-8 / MJ-10 行话泄漏**：引擎 finding reason 中输出 "WS-1 cut_flag set..."（build_review_queue.py:345,352,360,367）——这些 reason 会原样出现在交给人类复核的 queue JSON/工单里，"WS-1" 对使用者是黑话；t6 函数 docstring 的 "WS-8 slice" 与 "improvement-plan MJ-10"（build_review_queue.py:313,318）、input-schema.md:14 的 "rather than failing (MJ-10)"、trigger-matrix.md:26 的 "(schema v2+)" 均属上游计划代号泄漏到交付物。建议全部改写为自解释表述。
- **kanchi-dividend-sop 悬空引用**：SKILL.md:119-121（Multi-Skill Handoff 两处）、input-schema.md:12（"emitted by kanchi-dividend-sop build_entry_signals.py (current: 2)"）、trigger-matrix.md:22-24（"emitted by `kanchi-dividend-sop/build_entry_signals.py` (schema v2+)"）。已核实本语料库两套集合中**均无该技能**，且 `kanchi-dividend-sop/build_entry_signals.py` 属于跨技能文件路径（SKILL-SPEC §3.3 禁止形式，虽出现在 reference 文件而非 SKILL.md 正文，纪律应一致）。引擎对此做了合理降级（schema_version 容忍、最小字段输入），说明引用的是"外部上游"而非本语料内技能。建议改为中性表述："由上游 Kanchi 股息 SOP 流水线（外部系统）产出"。
- **引号风格**：SKILL.md:47 的复述短语用了弯引号（"confirm next dividend-growth cadence / pause optional adds until checked"），而 SCORING PROC-06（87 行）与 trigger-matrix 用直引号。若未来评审工具做字符串比对会误伤，建议统一为直引号。

---

## 5. 参考文件审查（全部全文通读）

### 5.1 references/input-schema.md（72 行）

- 结构：Required Top-Level（as_of、holdings）→ Optional Top-Level（schema_version）→ Holding Object 样例 JSON → Minimal Viable Input。组织良好。
- 样例 JSON 块经 `json.loads` 实测可解析，含全部 8 个业务字段组（dividend/cashflow/balance_sheet/capital_returns/filings/operations + flags 子对象），字段命名与引擎 `to_float`/`float_history` 的读取键完全对应（如 coverage_ratio_history、net_debt_history、interest_coverage_history、revenue_cagr_5y）。✅
- 与引擎的兼容性核对：T2 需要 ffo（REIT）/nii（BDC），样例已含 ffo/nii 字段（null 占位）；T3 需要 capital_returns，样例已含；T4 需要 filings.recent_text/latest_8k_text/headlines，样例已含；T5 需要 operations 四字段，样例已含。schema 与引擎字段集 100% 覆盖。✅
- 问题点：`kanchi-dividend-sop build_entry_signals.py (current: 2)` 与 `(MJ-10)`（12-14 行）为悬空/行话引用（见 4.4）。
- 未提供第二个"最小输入"JSON 样例（只有字段清单），可加一个最小样例便于 Agent 快速构造（见 13 节 🟢 F-17）。

### 5.2 references/trigger-matrix.md（43 行）

- 结构：Severity Policy（OK/WARN/REVIEW 语义）→ Trigger Definitions 表格（6 行，T1-T6）→ T6 说明段 → Denominator Mapping 表格 → Escalation Rule。核心规则密度高，是 SKILL.md 状态机/阈值的唯一权威来源，避免正文双源漂移。✅
- 表格字段完整：Core signal / Default machine rule / Frequency / Default action。阈值与引擎一致：T1 的 `latest_regular < prior_regular * 0.99`、`<= 0`、missing feed 三项与 build_review_queue.py:67-97 逐条吻合；T2 的 `denominator <= 0` with positive dividends 与 116-123 行吻合；T4 关键词 5 个与 T4_KEYWORDS 吻合；T6 的 cut/variable→REVIEW、freeze/special→WARN 与 341-370 行吻合。✅
- 问题点：①标题 "(T1-T5)" 与实际含 T6 不符（4.1）；②T2 行 Frequency 为 Quarterly，但引擎为纯无状态函数、无周期逻辑，Frequency 只是评审节奏建议，文档未说明"引擎本身不区分周期"（可接受，建议补一句）；③`kanchi-dividend-sop/build_entry_signals.py` 跨技能路径（4.4）；④T5 的 2+/3+ 边界未在矩阵写明（4.2）；⑤ETF 行写的 holdings-level proxies 与引擎 fcf 降级不符（4.2）。

### 5.3 references/review-ticket-template.md（32 行）

- 结构：REVIEW 工单模板，含 Trigger Summary、Evidence (One Line Each)、Manual Checks Required（5 项）、Decision Log。与 SKILL.md 第 4 步、SCORING PROC-05/FMT-04 的要求（trigger IDs + evidence、suspected failure mode、required manual checks）对应。
- 小问题：Evidence 清单只列 T1-T5（13-19 行），缺 T6；"## Trigger Summary" 与模板顶部 H1 "# REVIEW Ticket: [Ticker]" 之间存在 "## Trigger Summary" 但无 "##" 层级的次级内容错位（无实质问题）。建议 Evidence 补 T6 行（13 节 🟢 F-13）。
- 模板中 "Generated at:" 为空占位，由 Agent 填写，合理。

### 5.4 scripts/build_review_queue.py（533 行）

- 架构：dataclass TriggerFinding → 六个独立判定函数（t1~t6，各返回单条 finding 或 None）→ evaluate_holding（聚合、取最高严重级、生成 actions）→ build_report（汇总）→ render_markdown → main（CLI）。职责单一、可测性好。
- 健壮性细节：to_float/float_history 对 None/非数字容错；strictly_increasing 对长度不足返回 False；T6 对 `dividend.flags` 缺失时回退读 `dividend` 顶层（312-331 行）；evaluate_holding 对缺失 instrument_type 回退 "stock"（375 行）。降级设计明确。
- 实测：用 ABC(cut)/DEF(T2 双期超 1.0)/GHI(freeze) 三持仓冒烟，summary = {OK:0, WARN:1, REVIEW:2}，MD 渲染含 ## Summary / ## Queue / ## Findings 与 `- \`T1\` \`REVIEW\`` 行，符合 SCORING PROC-04/FMT-02 模式（已实测通过）。
- 问题点：①T4_KEYWORDS 5 词与 SKILL.md 9 词族不符（4.2）；②finding reason 中的 "WS-1" 黑话进入人类交付物（4.4）；③docstring 的 "WS-8 slice"、"improvement-plan MJ-10"（313、318 行）为内部计划残留；④ETF 分母映射与文档不符（4.2）；⑤main() 中 `--output` 与 `--output-dir` 并存时 filename 逻辑 OK，但若 as_of 带时间成分（如 "2026-02-27T00:00:00Z"），date_suffix 会变成 "20260227T000000Z"，文件名与文档示例不符（输入 schema 已约束为 ISO 日期字符串，低风险，🟢）。
- 整体评价：本技能质量最高的文件。规则确定性、容错、可测性俱佳。

### 5.5 scripts/tests/（conftest.py 6 行 + test_build_review_queue.py 294 行）

- conftest.py：仅把 scripts/ 插入 sys.path，使测试可 `from build_review_queue import ...`。pytest 专用机制。
- test_build_review_queue.py：20 个测试函数，覆盖 T1（cut/missing）、T2（双期超 1.0→REVIEW、单期→WARN、分母非正→REVIEW、0.8 上升→WARN）、T3（REVIEW/WARN 两分支）、T4（Item 4.02 命中）、T5（2→WARN、3→REVIEW）、T6（cut/variable/freeze/special/无标志五路）、schema_version 容忍、render_markdown 标题、build_report 汇总与空持仓、main 子进程端到端。覆盖面与引擎行为一一对应，`assert` 断言简洁。
- 实测：20/20 全部 PASS（逐函数手动执行验证）。
- **重要问题：测试与 pytest 绑定，stdlib 无法运行**。测试全部是无类裸函数 + 裸 assert（pytest 风格），`python -m unittest discover -s tests` 实测 "Ran 0 tests"（unittest 只收集 TestCase 子类；直接 `-m unittest tests.test_build_review_queue` 同样 0 项，因为 tests 目录无 __init__.py 且非包）。本机未安装 pytest（`No module named pytest`），即**当前环境无法按任何现成命令运行这套测试**。SKILL.md:126 声称的 "unit tests" 存在但不可一键执行。建议：文档注明 `pip install pytest` 与 `python -m pytest scripts/tests`，或提供不依赖 pytest 的运行方式（见 13 节 🟡 F-09）。
- 微瑕：`import json/subprocess/sys/pathlib` 在函数体内（test_main_with_output_dir，250-255 行），风格问题；`tmp_path` fixture 依赖 pytest。

### 5.6 agents/openai.yaml（3 行）

- 内容仅 `interface: {display_name, short_description}`，描述为 "Help with Kanchi Dividend Review Monitor tasks"，信息量为零。
- **全技能无任何文件引用它**（SKILL.md Resources 未列、SCORING 未涉及、目录内无消费者）。它既不属于 SKILL-SPEC 允许的目录构件（spec 未定义 agents/ 目录），也无实际功能。判断为从上游 Kanchi 仓库复制时带入的残留。建议删除，或在 Resources 中说明用途（见 13 节 🟢 F-12）。

### 5.7 SCORING.yaml（207 行）与 check.py（113 行）

- 结构：SCORING 顶部声明 ${INPUT_JSON}/${QUEUE_JSON}/${QUEUE_MD} 变量并注释了 resolved 路径，与 check.py 硬编码路径逐项对应；21 项 criterion（3 scope / 6 process / 3 decision / 4 format / 2 technical / 2 negative / 1 qa）+ 3 条 critical_failures（cap_to_0：auto-sell、伪造状态、缺三件套输出），`total_items: 21` 与实际条目数核对无误。
- 判断方式配比：9 项 script（SCOPE-02、PROC-01~04、FMT-01~03、QA-01）由 check.py 实现；12 项 llm 评审。check.py 中 9 项逐一与 SCORING 对应，函数选择正确（json_array_all_have_keys / file_exists / file_contains / json_field_exists / tool_log_contains 均存在于 checker 库）。
- 实测：以模拟工作区（monitor_input.json + reports/review_queue_20260227.json/.md + 含 build_review_queue 调用的 tool_log.jsonl）运行 `python check.py <ws> <tool_log> <agent_output>`，9 项全部 true，rc=0，输出为合法 JSON 字典。✅ 端到端链路可用。
- LLM 评审问题质量：PROC-05 带 "Answer yes if no ticker reached REVIEW." 逃逸句，DEC-01 带 "no REVIEW statuses without a rule basis" 反例约束，均属高质量提问。⚠️ 但 PROC-06/NEG-02 基于引擎不存在的"平股息 T6"场景（4.2），评审结果可能失真。
- 问题点汇总：QA-01 描述承诺 > 实际检查（4.3）；PROC-01 可被 Read 调用绕过（4.3）；SCOPE-02 空数组必败（4.3）；PROC-02/FMT-01 重复（4.3）；文件检查取 glob 第一个匹配（checker.py file_contains/file_exists），多日期报告并存时可能检查到旧文件（🟢 提示）；check.py:26 `set_agent_output(agent_output)` 传入的是路径而非内容（本技能无 output_* 检查，实际无影响，🟢 提示）。
- 编码：SCORING.yaml/check.py 含非 ASCII 装饰字符（── 28 处、— 13 处、→ 9 处，均在注释/描述中），UTF-8 合法可解析，但若下游工具按 ASCII 处理会有噪音（🟢 提示）。

---

## 6. 语法格式

### 6.1 Frontmatter YAML

PyYAML 实测解析通过，键序 name → description，值类型均为字符串，description 用双引号包裹且内含的括号/斜杠无转义问题。✅

### 6.2 Markdown 结构

标题层级 H1(1 个)→H2(12 个)→H3(4 个) 无跳级；列表、代码块（bash/json 标注）闭合正确；表格仅出现在 reference 文件（trigger-matrix），格式规范。✅

### 6.3 JSON 样例

input-schema.md 的 json 代码块 `json.loads` 实测通过，无注释残留、无尾逗号。✅

### 6.4 Python 语法与运行

build_review_queue.py 导入即编译通过（冒烟运行成功）；check.py 正常运行；test 文件导入成功（20 个函数可枚举）。类型注解（float | None、dict[str, Any]）与 Python 3.10+ 匹配。✅

### 6.5 编码

SKILL.md（弯引号 U+201C/201D 各 1，47 行）、SCORING.yaml、check.py、trigger-matrix.md（→ 2 处）含非 ASCII；其余 6 个文件纯 ASCII。UTF-8 编码合法，无乱码；纯 ASCII 工具链友好度见 5.7 提示。

### 6.6 行尾与杂项

未发现行尾混合或不可见控制字符；文件均以换行结尾；无超长行（最长行在 SKILL.md 47 行，约 220 字符，属段落长句而非代码）。

---

## 7. 规范合规（12 项清单）

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符、≤64、匹配目录 | ✅ | 29 字符；与去 NNN 前缀的目录名一致 |
| 2 | description：第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✅ | 308 字符，三要素齐全 |
| 3 | description：无祈使/一二人称开头 | ✅ | "Monitor dividend portfolios..." 与官方好例子同构 |
| 4 | description：无跨技能路由 | ✅ | 无 "NOT for X use Y" |
| 5 | description：至少一个触发信号短语 | ❌（临界） | "Use when users ask for..." 偏离规范短语清单原文（"Use when the user..." 系），建议对齐 |
| 6 | frontmatter 无允许清单外键 | ✅ | 仅 name/description |
| 7 | body ≤600 行 | ✅ | 正文 126 行 |
| 8 | body 有 Workflow/Process 节 | ✅ | ## Workflow 四步 |
| 9 | body 有 Output Format 节 | ✅ | ## Output Contract 三条 |
| 10 | body 有 Scope/Limitations 节 | ❌ | 无独立小节，相关内容散落（见 3.1） |
| 11 | body 无跨技能文件引用 | ✅（警告） | 无 `../` 路径；但 Workflow 命令含不存在的 `skills/...` 仓库路径，trigger-matrix 含 `kanchi-dividend-sop/build_entry_signals.py` |
| 12 | 目录 NNN-kebab-case 无空格大写 | ✅ | 299-kanchi-dividend-review-monitor |

合计：✅ 10 项、❌ 2 项（其中第 5 项为临界性质）、⚠️ 附注 2 处。规格合规是本次审查最集中的短板，两项缺口的修复成本都很低。

---

## 8. 人机感

### 8.1 人类读者体验

正文 126 行、结构清晰、表意直接，"Non-Negotiable Rule"、"Flat-dividend cadence caveat" 这类命名自带记忆点。README 气质浓厚，适合人工快速上手。✅

### 8.2 机器/Agent 执行体验

规则确定性极强：输入 schema 精确、命令明确、输出文件名可预期、状态机三态互斥、actions 枚举固定（pause_buy_adds / create_review_ticket / human_read_full_disclosure / pause_buy_adds_optional / append_next_earnings_checklist）。Agent 按图索骥即可产出 SCORING 全部 9 项脚本检查所期望的产物。✅

### 8.3 输出物可读性

queue JSON 含 summary + 逐 ticker findings/actions，MD dashboard 含 Summary/Queue 表/Findings 详情，工单模板含 5 项人工核查清单——三类交付物各司其职。❌ 唯一减分点是 finding reason 里的 "WS-1 cut_flag set" 等黑话直接进入人类阅读的交付物。

### 8.4 术语与行话

"Kanchi"（品牌名）、"OK/WARN/REVIEW"（自定义状态）在技能内自洽；但 WS-1/WS-8/MJ-10/schema v2+ 等上游计划代号在本技能内从未定义，对使用者不可解释（4.4）。"T1-T5/T1-T6" 口径分裂也会让读者困惑。

### 8.5 容错与降级路径

Prerequisites（21-30 行）明确给出"数据不全时的最小输入"，input-schema 有 Minimal Viable Input，引擎对缺失字段全链路容错（to_float 返回 None → 跳过对应 trigger），SEC Guardrail 对空 snippets 给了 SEC 拉取 + 窄扫描结论的降级路径。这是本技能人机感的亮点。✅

### 8.6 整体印象

"给机器看的确定性 + 给人看的安全网"设计意图清晰且实现到位；主要观感问题是行话泄漏与 78 行命令路径在真实布局下不可执行，会显著消耗使用者的信任成本。

---

## 9. 可执行性

### 9.1 引擎与测评链实测（2026-08-06 执行）

- 引擎冒烟：三持仓样例 → summary {OK:0, WARN:1, REVIEW:2}，JSON+MD 双输出正常，日期文件名生成正确。✅
- 单元测试：pytest 未安装；unittest 发现 0 项；**手动执行 20 个测试函数全部 PASS**。即测试逻辑正确、运行方式缺失（5.5）。⚠️
- check.py：模拟评测工作区端到端运行，9 项 script 检查全部 true，退出码 0。✅
- YAML/JSON：frontmatter、SCORING.yaml、openai.yaml、input-schema JSON 块全部解析通过。✅

### 9.2 文档指令可执行性

SKILL.md 第 2 步给出的命令 `python3 skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py`（78 行）在真实语料布局下路径不存在——技能实际位于 `complex-skills/299-kanchi-dividend-review-monitor/`，且该行对"技能目录如何映射"没有任何说明。Agent 照抄必失败；聪明 Agent 会改为相对路径（Resources 节 125 行已用正确相对写法，可互为参照），但指令本身是错的。这是影响第 2 步的阻塞性问题（13 节 F-03）。

### 9.3 环境依赖

- 运行时：python3 + 标准库（argparse/json/datetime/pathlib/dataclasses），无第三方依赖。✅
- 测试：依赖 pytest（未安装、未声明）；stdlib unittest 不兼容（5.5）。⚠️
- check.py：依赖 `../_shared/checker.py`（存在，已验证）；评测工作区须含 monitor_input.json 与 reports/ 子目录（check.py 硬编码）。✅
- 附注：`python3` 在 Windows 环境可能不存在（应为 `python`），命令可移植性可顺手改进。

---

## 10. SCORING 交叉参考

21 项 criterion 的满足机制与实测状态：

| ID | 类别 | 满足机制 | 状态 |
|---|---|---|---|
| SCOPE-01 | scope | Agent 识别监控任务并应用 OK/WARN/REVIEW 状态机（LLM 评审；描述与正文均给出） | ✅ 文档支撑充分 |
| SCOPE-02 | scope | 输入含 ticker/instrument_type/dividend（check.py 实测通过；注意空数组必败） | ✅（边界 ⚠️） |
| SCOPE-03 | scope | 不产出买卖指令（Non-Negotiable Rule + CF-01 兜底） | ✅ |
| PROC-01 | process | 工具日志含 "build_review_queue" | ⚠️ 可被 Read 调用绕过（4.3） |
| PROC-02 | process | reports/review_queue_* 存在（实测 ✅；FMT-01 重复） | ✅ |
| PROC-03 | process | 结果数组含 ticker/status/actions/findings 五键（引擎输出满足） | ✅ |
| PROC-04 | process | MD 含 `- \`T[1-6]\` \`(OK|WARN|REVIEW)\``（render_markdown 实测匹配） | ✅ |
| PROC-05 | process | REVIEW 工单含触发器/失败模式/人工核查（模板支撑，LLM 评审） | ✅ |
| PROC-06 | process | 平股息 T6 按 cadence WARN 处理 | ⚠️ 引擎无法产生该场景（4.2） |
| DEC-01 | decision | T1 三规则 → REVIEW（引擎 67-97 行逐条吻合，测试覆盖） | ✅ |
| DEC-02 | decision | T2 分母按 instrument 映射 | ⚠️ ETF 行与引擎 fcf 降级不符（4.2） |
| DEC-03 | decision | WARN/REVIEW 语义与 actions（引擎 actions 枚举吻合） | ✅ |
| FMT-01 | format | 三件套输出（file_exists；与 PROC-02 重复） | ✅ |
| FMT-02 | format | MD 含 ## Summary/## Queue（实测匹配） | ✅ |
| FMT-03 | format | JSON 含 "trigger": "T[1-6]"（实测匹配） | ✅ |
| FMT-04 | format | 工单含失败模式与人工核查（模板支撑） | ✅ |
| TEC-01 | technical | 实时 SEC 抓取合规（Guardrail 写明，LLM 评审） | ✅ |
| TEC-02 | technical | 空 snippets 时 SEC 枚举 8-K + 9 词族扫描 | ⚠️ 9 词族与引擎 5 词不一致（4.2） |
| NEG-01 | negative | 不自动卖出（红线 + CF-01） | ✅ |
| NEG-02 | negative | 不把平股息当减产证据 | ⚠️ 与 PROC-06 同一口径问题 |
| QA-01 | qa | generated_at + as_of 存在（实测 ✅） | ⚠️ 描述承诺的文件名校验未实现 |

critical_failures 三条（cap_to_0：自动卖出、伪造状态、缺三件套）与 Non-Negotiable Rule / Output Contract 一一对应，兜底设计合理。✅

总体：21 项中 15 项强满足、6 项存在口径或健壮性缺陷（均非致命，不触发 cap_to_0）。

---

## 11. 已知问题

按任务要求本节跳过（本次审查的重点是发现可修复的改进点，而非复述已知问题清单）。

---

## 12. 综合评分（8 维加权）

| 维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| 规格合规 | 0.15 | 7.5 | 10/12 清单项通过；缺 Scope/Limitations 节 + 触发短语临界偏离 |
| 描述质量 | 0.10 | 8.0 | WHAT/WHEN/KEYWORDS 齐备、308 字符精炼；T1-T5 口径小漏 |
| 结构组织 | 0.10 | 8.0 | 12 节层次干净、引用指向明确；缺独立 Scope 节扣分 |
| 逻辑一致性 | 0.15 | 6.5 | T4 词集、ETF 分母、平股息 T6、T1-T5/T1-T6、QA-01 描述/实现 5 处漂移 |
| 参考文件质量 | 0.10 | 7.5 | schema 与引擎 100% 字段对齐、矩阵权威清晰；悬空 SOP 引用与行话 |
| 可执行性 | 0.15 | 7.5 | 引擎/测试/检查链实测通过；78 行命令路径错误 + pytest 缺失 |
| 人机感 | 0.10 | 7.5 | 确定性设计是亮点；WS-1 黑话进入人类交付物减分 |
| 测评对接 | 0.15 | 7.0 | 21 项与检查实现对应、端到端跑通；PROC-01 绕过、QA-01 漂移、空数组边界 |

加权总分 = 7.5×0.15 + 8.0×0.10 + 8.0×0.10 + 6.5×0.15 + 7.5×0.10 + 7.5×0.15 + 7.5×0.10 + 7.0×0.15 = **74.0 / 100**（评级：B，良好但未达优秀）。

一句话结论：**引擎、测试与评分链是本技能的三块基石，全部实测可用且互相印证；拖分项集中在"文档口径统一"与"规格合规补缺"两类低成本修复上，无结构性重构需求。**

---

## 13. 修复建议

### 🔴 高优先级（阻塞或规格硬性缺口，工作量均低）

- **F-01 | 补 Scope/Limitations 节** — SKILL.md，建议在 "## Non-Negotiable Rule" 之后（35 行后）新增 "## Scope and Limitations"，明确：①不做自动卖出/自动交易（已有，可并入）；②不做税务处理、账户迁移等（指向 013-kanchi-dividend-us-tax-accounting）；③不覆盖非股息类风险监控；④不替代人工承销复核；⑤何时不要用（一次性估值查询、无股息标的、需立即执行交易时）。工作量：10 行文本，规格 §3.1 硬性要求。
- **F-02 | 对齐 description 触发短语** — SKILL.md:3。"Use when users ask for..." → "Use when the user asks to..."（或 "Use when the user needs to..."），并对齐规范短语原文；顺带把 "(T1-T5)" 改为 "(T1-T6)"（与 F-04 一并处理）。工作量：1 行，为 SkillIF 触发遵从实验消除变量。
- **F-03 | 修正 Workflow 第 2 步命令路径** — SKILL.md:78。`python3 skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py` 在语料布局下不存在；改为技能内相对路径 `python3 scripts/build_review_queue.py`（与 Resources 125 行一致），或写明"相对技能根目录"并给占位符。工作量：1 行。

### 🟡 中优先级（口径/行为/测评健壮性，工作量低-中）

- **F-04 | 全量统一 T1-T6 口径** — SKILL.md:3,51-57,83,126 + trigger-matrix.md:1。将 description、Monitoring Cadence（补 T6 Daily）、Workflow 第 2 步 "based on T1-T5"、Resources "T1-T5"、矩阵标题 "(T1-T5)" 全部改为 T1-T6。工作量：6 处文本。
- **F-05 | 统一平股息 T6 的文档与引擎行为** — SKILL.md:45-47 + SCORING PROC-06/NEG-02 + trigger-matrix.md:20。二选一：a) 改文档——"引擎只在 WS-1 标志存在时触发 T6；latest==prior 且无标志的持仓不产生机器触发，Agent 应在报告中以说明性 note 提示复核股息增长节奏，不构成 WARN"；b) 给 t6 增加"平股息→WARN(cadence)"规则并补测试。建议 a（保持引擎纯净），工作量：3 处文本。
- **F-06 | T4 关键词集对齐** — build_review_queue.py:26-32 + SKILL.md:108 + SCORING TEC-02。引擎 T4_KEYWORDS 扩为 9 词族（subpoena、going concern、auditor resignation、internal control），并给 test_t4 系列补 2 个用例。工作量：4 行 + 测试 20 行。
- **F-07 | ETF 分母口径对齐** — build_review_queue.py:20-25 + trigger-matrix.md:35 + SCORING DEC-02。二选一：a) 引擎保持 fcf，矩阵改注"脚本当前以基金层 FCF 兜底，holdings-level proxies 由 Agent 人工补充"；b) 在输入 schema 加 ETF 持仓层字段并实现。建议 a，工作量：1 行文本。
- **F-08 | 清理悬空引用与行话** — SKILL.md:119-121 + input-schema.md:12-14 + trigger-matrix.md:22-26 + build_review_queue.py:313,318,345,352,360,367。kanchi-dividend-sop 改"上游 Kanchi 股息 SOP 流水线（外部系统）"中性表述；WS-1/WS-8/MJ-10 从交付物 reason 与文档中删除或改为自解释措辞（如 reason 改 "cut_flag set: dividend rate declined year-over-year"）。工作量：约 10 处文本。
- **F-09 | 测试可运行性** — scripts/tests/ + SKILL.md:126。pytest 未安装且 unittest 发现 0 项。方案：文档写明 `pip install pytest` + `python -m pytest scripts/tests`（conftest 已就位）；或提供轻量替代（把 test 文件改造为 unittest.TestCase 或加 `if __name__ == "__main__"` 手动跑子集）。工作量：1 行文档 + 可选改造。
- **F-10 | 收紧 PROC-01 判定** — SCORING.yaml:41-45 + check.py:48。把 tool_log_contains("build_review_queue") 改为匹配执行类条目（如 tool=="Bash" 且命令含 build_review_queue + --input），避免 Read 脚本文件路径即通过。工作量：checker 侧按 tool 过滤 + SCORING 描述同步。
- **F-11 | QA-01 描述与实现对齐** — SCORING.yaml:187-193。二选一：实现文件名后缀 == as_of 的校验（json_field_matches 或新增函数）；或把描述改为"报告包含 generated_at 与 as_of 时间戳"。建议前者（描述更有价值），工作量：检查函数 5 行。

### 🟢 低优先级（锦上添花，工作量极低）

- **F-12 | 处理 agents/openai.yaml 孤儿文件** — 删除，或移入 Resources 说明用途。工作量：1 分钟。
- **F-13 | review-ticket-template Evidence 补 T6 行** — review-ticket-template.md:13-19。工作量：1 行。
- **F-14 | 统一引号风格** — SKILL.md:47 弯引号 → 直引号，与 SCORING PROC-06 一致。工作量：1 行。
- **F-15 | trigger-matrix 补 T5 边界与"引擎无周期"说明** — trigger-matrix.md:19,17。写明 2 信号→WARN、≥3 信号→REVIEW；引擎为无状态规则、Frequency 仅为评审节奏。工作量：2 行。
- **F-16 | SCOPE-02 空数组容错** — SCORING.yaml:20-28。空 holdings 视为合法（另设空组合判定），避免空组合必败。工作量：检查函数 3 行。
- **F-17 | 补充最小输入样例** — input-schema.md：在 Minimal Viable Input 后附一个 2-3 字段的最小 JSON 样例。工作量：8 行。
- **F-18 | 编码卫生** — SCORING.yaml/check.py/trigger-matrix.md 的 ─/—/→ 替换为 ASCII（可选）。工作量：低。
- **F-19 | 输出位置约束写明** — SKILL.md:78-84：注明"输出文件必须落在工作区 reports/ 目录"（check.py 硬编码该路径）。工作量：1 行。

---

## 附录：验证记录

1. 环境：Windows 11 / Python 3.14（C:\Python314）。
2. 引擎冒烟（build_review_queue.py）：3 持仓样例 → {OK:0, WARN:1, REVIEW:2}；JSON+MD 输出、日期文件名、`- \`T1\` \`REVIEW\`` 行格式均符合 SCORING 模式。✅
3. 单元测试：`python -m pytest tests -q` → No module named pytest；`python -m unittest discover -s tests -v` → Ran 0 tests（pytest 风格裸函数与 unittest 不兼容）；手动逐函数执行 20/20 PASS。✅（运行方式缺位）
4. check.py 端到端：模拟工作区（monitor_input.json、reports/review_queue_20260227.json/.md、tool_log.jsonl 含脚本调用、agent_output.md）→ 9 项全 true、rc=0。✅
5. YAML/JSON 解析：SKILL.md frontmatter（键仅 name/description）、SCORING.yaml、agents/openai.yaml、input-schema.json 块全部通过。✅
6. 语料交叉检索：`kanchi-dividend-sop` 在两套语料中均不存在；`013-kanchi-dividend-us-tax-accounting` 存在（其 SKILL.md 同样引用了 kanchi-dividend-sop，属语料级共性问题，本次不展开）。
7. 行数与编码：SKILL.md 130 行（正文 126）；非 ASCII 仅存在于 SKILL.md（弯引号 2 处）、SCORING.yaml（装饰符 50 处）、check.py（29 处）、trigger-matrix.md（→ 2 处）。
8. 本报告仅为审查产物；按任务约束，未修改 SKILL.md / SCORING.yaml / check.py 及任何技能文件。
