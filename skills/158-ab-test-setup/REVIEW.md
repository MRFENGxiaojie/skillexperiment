# REVIEW: 158-ab-test-setup

**审查日期**: 2026-08-06
**Skill 类型**: workflow — A/B 测试实验设计全流程（假设 → 指标 → 样本量 → 变体 → 运行 → 分析 → 文档化）
**Body 行数**: 465 行（frontmatter 4 行，总 469 行）
**参考文件数**: references/6, scripts/0, assets/0, 其他: ab-test-setup/ 嵌套副本目录 1（含 304 行 SKILL.md 副本）
**审查范围**: 全目录 11 个文件全部通读（1150 行）

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\
├── SKILL.md                          (469 行, 主技能文件)
├── SCORING.yaml                      (191 行, 评分标准, pattern: workflow)
├── check.py                          (84 行, 脚本检查, 11 项)
├── REVIEW.md                         (51 行, 旧版审查——本次重写)
├── ab-test-setup\                    (嵌套子目录——异常存在, 见 §5.6)
│   └── SKILL.md                      (304 行, 完整副本, 另一版本)
└── references\
    ├── analysis-plan.md              (11 行)
    ├── common-mistakes.md            (20 行)
    ├── implementation.md             (3 行)
    ├── metrics.md                    (3 行)
    ├── questions-to-ask.md           (10 行)
    └── related-skills.md             (4 行)
```

目录合计 11 个文件、1150 行。无 scripts/、assets/、templates/、examples/、docs/ 等子目录。**重要发现**: 存在一个嵌套子目录 `ab-test-setup/`，内含一份完整的、与顶层 SKILL.md 内容不同的另一版 SKILL.md（304 行）——这是重复残留文件，详见 §5.6 与 §13。

---

## 2. Frontmatter 逐字段审查

顶层 `SKILL.md` frontmatter 仅 2 个字段（第 1-4 行）：

### 2.1 name

- 值: `ab-test-setup`。小写 + 连字符 ✓；长度 14 字符 ≤ 64 ✓；与目录名 `158-ab-test-setup` 匹配（NNN 前缀为语料库编号，按惯例 name 不含 NNN）✓。
- **无问题发现**。

### 2.2 description — 逐句分析

完整原文（367 字符，含引号）："A/B testing and experimentation design with statistical validity. Covers hypothesis formation, metric selection, variant design, sample size calculation, and results interpretation. Use when the user wants to plan, design, or implement an A/B test or experiment, mentions "A/B test", "split test", "experiment", "test this change", or wants to set up variant testing."

- **句 1** "A/B testing and experimentation design with statistical validity." — WHAT 定位明确，第三人称名词短语 ✓。小瑕疵：无动词的省略式表达（"design" 是名词），可接受但略显电报体。
- **句 2** "Covers hypothesis formation, metric selection, variant design, sample size calculation, and results interpretation." — WHAT 展开，覆盖技能全部 5 个核心环节，与 Body 章节一一对应 ✓。
- **句 3** "Use when the user wants to ... mentions ... or wants to set up variant testing." — WHEN + KEYWORDS ✓。包含规范 §2.4 认可的触发信号句式 "Use when the user wants to..."，且列出 6 个关键词触发词（"A/B test"、"split test"、"experiment"、"test this change"、"variant testing"）✓。
- 人称检查：第三人称描述技能 + "the user"，无第一/第二人称 ✓。句 3 的 "Use when" 是规范模板句（§2.2/§2.4 明确列出的触发句式），不构成 §2.3 禁止的命令式开头（禁止的是 "Use this skill to..." 型）。
- 无跨技能路由 ✓（与嵌套副本的 description 形成对比，见 §5.5）。
- 长度 367 ≤ 1024 ✓。非内部实现细节、无冗余 ✓。
- **结论: 合规**。仅有一处可优化：句 1 补动词（如 "Provides A/B testing and experimentation design..."）。

### 2.3 allowed-tools

- **缺失**。顶层 frontmatter 无 `allowed-tools` 字段。按 SKILL-SPEC v1.0 §1.2 该字段为可选（不构成规范违规），但按 SkillIF 语料库惯例与评测清单要求应存在。
- 本技能是纯知识/咨询型技能：agent 不运行命令、不写文件，工作产物直接输出为对话内容。建议值: `Read, Write, Glob, Grep`（仅为读取 references/ 与可能的工作区文件）。
- 嵌套副本同样无此字段。

### 2.4 其他 frontmatter 字段

- 顶层: 除 name/description 外**无其他字段** ✓ 合规。
- 嵌套副本 `ab-test-setup/SKILL.md`（第 1-12 行）含 `license: MIT`、`metadata: {version, author, category, updated}`、`agents: [claude-code]` — 全部属于规范 §1.3 **禁止字段**。该副本不合规（且为残留文件，应删除，见 §5.6/§13）。

### 2.5 Frontmatter 语法

- 顶层: `---` 分隔符成对（第 1、4 行），`name: ab-test-setup` 无引号合法，`description:` 为 YAML plain scalar（内含双引号字面量但不含冒号+空格序列，解析合法）✓。缩进 0 级 ✓。
- 嵌套副本: name 带双引号合法；description 带引号包裹合法；metadata 块缩进 2 空格合法。语法本身无错 ✓。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
## Initial Assessment                    (L11)
## Core Principles                       (L33)
  ### 1. Start with a Hypothesis
  ### 2. Test One Thing
  ### 3. Statistical Rigor
  ### 4. Measure What Matters
## Hypothesis Framework                  (L58)
  ### Structure
  ### Examples
  ### Good Hypotheses Include
## Test Types                            (L89)
## Sample Size Calculation                (L115)
  ### Required Inputs
  ### Quick Reference
  ### Formula Resources
  ### Test Duration
## Metric Selection                      (L151)
  ### Primary Metric
  ### Secondary Metrics
  ### Guardrail Metrics
  ### Metric Examples by Test Type
## Designing Variants                    (L187)
  ### Control (A)
  ### Variant (B+)
  ### Documenting Variants
## Traffic Allocation                    (L242)
  ### Standard Split
  ### Conservative Rollout
  ### Ramping
  ### Considerations
## Implementation Approaches              (L266)
  ### Client-Side Testing
  ### Server-Side Testing
  ### Feature Flags
## Running the Test                      (L305)
  ### Pre-Launch Checklist
  ### During the Test
  ### The Peeking Problem
## Analyzing Results                      (L346)
  ### Statistical Significance
  ### Practical Significance
  ### What to Look For
  ### Interpreting Results
## Documenting and Learning              (L400)
  ### Test Documentation
  ### Building a Learning Repository
## Output Format                         (L440)
  ### Test Plan Document
[模板代码块内嵌标题: ## Hypothesis / ## Test Design / ## Variants / ## Reference Files]
```

共 13 个顶层 `##` 节 + 30 个 `###` 子节 + 4 个代码块内模板标题。章节顺序构成完整生命周期（评估→设计→实施→运行→分析→沉淀→产出），结构优秀。

### 3.2 必需章节检查

- **Workflow/Process**: ✅ — Initial Assessment → Core Principles → Hypothesis → Sample Size → Metrics → Variants → Allocation → Implementation → Run → Analyze → Document 构成完整分步流程。
- **Output Format**: ✅（部分破损）— "## Output Format"（L440）含 Test Plan Document 模板；**但模板代码围栏未闭合**（见 §6.4），且模板内缺 "## Metrics"、"## Implementation"、"## Analysis Plan" 三个标题（SCORING FMT-01 要求输出含此三者，见 §10.1）。
- **Scope/Limitations**: ❌ **缺失** — 全文无 Scope、Limitations、"What This Skill Does NOT Do" 类章节。技能不做什么（不做因果推断、不做 MVT 小流量、不替代 analytics-tracking 等）没有边界说明。违反规范 §3.1，必须补。

### 3.3 内容委托分析

- 委托比例: body 465 行 vs references 合计 51 行 → 委托率约 9.9%。**主体自足度极高**：核心知识全部在 body，references 只是模板碎片与提示清单。
- 反向依赖检查: SCORING FMT-01 期望输出含 "## Analysis Plan" 标题，该标题在 body 中不存在、只存在于 references/analysis-plan.md 碎片中 → body 对参考文件存在弱依赖，但影响有限。
- 评估: 委托模式合理，但参考文件内容质量差（见 §5.3），属于"委托了但没委托好"。

### 3.4 节编号/标题层级

- 仅 Core Principles 使用数字编号（### 1-4），连续无跳号 ✓。
- 标题层级: `##` → `###` 严格两级，无跳级（无直接 `####`）✓。
- "### Test Duration"（L137）与 "### Quick Reference"（L124）位置合理，但 Test Duration 内容格式破损（§6.4）。

### 3.5 Body 长度合规

- 469 总行 − 4 frontmatter = **465 行** ≤ 600 上限 ✓。距上限余 135 行，有余量可补充 Scope 节。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- Initial Assessment（L11-29）采集的 baseline conversion rate、traffic volume、constraints 三个输入，被后续 Sample Size Calculation（Required Inputs: baseline、MDE、significance、power）与 Test Duration 直接消费 ✓ 衔接闭合。
- Hypothesis Framework → Metric Selection（"Primary Metric ... Directly tied to the hypothesis"）→ Designing Variants（"True to the hypothesis"）→ Analyzing Results（"Compare against your MDE"、"Check confidence intervals"）—— 假设贯穿全流程 ✓。
- Pre-Launch Checklist（L307-316）逐项回溯前面各节决策（hypothesis、metric、sample size、duration、variants、tracking、QA、stakeholders）✓。
- Analyzing Results 的 6 步 What to Look For 与 Guardrail/MDE/segment 概念闭环 ✓。
- **结论: 步骤衔接良好，无断裂**。唯一断点：Test Duration 公式区域格式破损（内容仍在，衔接概念完整）。

### 4.2 内部矛盾扫描

- "Test One Thing"（L40-43）vs Test Types 中的 MVT —— 无矛盾："Leave MVT for later" 明确排序。
- "Don't peek ... stop early"（L326）vs "Use sequential testing if you must peek"（L340）—— 无矛盾：后者是有条件的替代方案，且明确了条件。
- "Maximum: Avoid running too long"（L146）vs 无最短时长设定 —— 无矛盾。
- **无内部矛盾发现**。

### 4.3 示例/代码正确性

- **Hypothesis 模板**（L62-68）: 5 行模板结构完整、可复用 ✓。
- **Strong hypothesis 示例**（L76）: "Because users report difficulty finding the CTA (per heatmaps and feedback), we believe that increasing button size and using contrasting color will increase CTA clicks by 15%+ for new visitors. We will measure click-through rate from page view to signup start." — 符合模板结构（Observation/Change/Effect/Audience/Metric 五要素齐全）✓。
- **样本量速查表**（L126-131）数值核验（95% 显著性、80% 功效、双侧检验、对每个 baseline 按 lift 计算 MDE）：
  - 1% baseline：10% lift ≈ 147k（表 150k，四舍五入偏大 2%）；20% lift ≈ 39k（表 39k ✓）；50% lift ≈ 6.3k（表 6k ✓）。
  - 3% baseline：10% ≈ 47k ✓；20% ≈ 12k ✓；50% ≈ 2.1k（表 2k ✓）。
  - 5% baseline：10% ≈ 27k ✓；20% ≈ 7.3k（表 7k ✓）；50% ≈ 1.3k（表 1.2k ✓）。
  - 10% baseline：10% ≈ 12.5k（表 12k，略偏小）；20% ≈ 3.4k（表 3k ✓）；50% ≈ 647（表 **550，偏小约 18%**）。
  - 结论: 12 行中 11 行误差 ≤5% 可接受；**10%/50% 行 550 与精确值 ~647 偏差最大**，且整表未标注"近似值"。作为 Quick Reference 可用，建议加近似标注。
- **Test Duration 公式**（L139-143）: 语义上"Duration = n × variants / (daily traffic × conversion rate)"正确，但格式破损（分子分母被 `---` 分隔线切断，见 §6.4）——内容对、渲染错。
- **95% confidence = p-value < 0.05**（L350-351）✓；"Means: <5% chance result is random" 属常见通俗化表述（严格讲是 P(数据|无效假设)，非 P(假设为真)），作为营销语境简化可接受，建议 🟢 精确化。
- **变体文档模板**（L228-237）与**测试文档模板**（L404-428）: 结构完整、闭合围栏 ✓。
- **Output Format 模板**（L444-469）: 内容最完整（含决策字段），但围栏未闭合（§6.4）。

### 4.4 条件完整性

- "If you must peek" → 有解法（sequential testing）✓。
- "If not [hit sample size], result is preliminary"（L365）✓。
- "No significant difference" → 两个出路（more traffic / bolder test）✓。
- Guardrail "Stop the test if significantly negative"（L166）✓。
- Interpreting Results 表 4 分支全覆盖 ✓。
- **无未闭合条件**。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

顶层 SKILL.md "## Reference Files"（L463-469，位于未闭合代码块内）列出 6 个引用，逐一核验：

| SKILL.md 引用 | 实际文件 | 存在性 |
|---------------|---------|--------|
| references/analysis-plan.md | references/analysis-plan.md (11 行) | ✅ 存在 |
| references/common-mistakes.md | references/common-mistakes.md (20 行) | ✅ 存在 |
| references/implementation.md | references/implementation.md (3 行) | ✅ 存在 |
| references/metrics.md | references/metrics.md (3 行) | ✅ 存在 |
| references/questions-to-ask.md | references/questions-to-ask.md (10 行) | ✅ 存在 |
| references/related-skills.md | references/related-skills.md (4 行) | ✅ 存在 |

6/6 全部存在 ✓。但**引用链接位于未闭合代码块内，Markdown 渲染下不会成为可点击链接**——功能上等于失效（见 §6.4）。

嵌套副本的引用核验：`references/sample-size-guide.md`（L100）与 `references/test-templates.md`（L234）**均不存在**（顶层 references/ 与副本相对路径下皆无）→ 副本内 2 处坏引用。

### 5.2 不可见资源审计

- 存在的文件中未被 SKILL.md 提及的：仅 **ab-test-setup/SKILL.md**（嵌套副本）——顶层 SKILL.md 全文未提及该目录/文件，属不可见残留。
- 6 个 references 文件均在 Reference Files 列表中提及 ✓（虽然渲染失效）。

### 5.3 Reference 文件全文审查

- **references/analysis-plan.md**（11 行）: 以 "## Analysis Plan" 开头（疑为从 body Output Format 节剪出的碎片），第 4 行有**孤立围栏 ```**（未闭合，吞掉其后全部内容）。"### Results Summary"、"### Recommendations" 为 1 行空壳。质量: 差——围栏破损 + 内容截断。
- **references/common-mistakes.md**（20 行）: 4 类 × 4 条（Test Design/Execution/Analysis），内容与 SCORING QA-02 精确对应 ✓。质量: 好。尾行孤立 `---`（装饰性，无害）。
- **references/implementation.md**（3 行）: 仅 3 条占位符（Method/Tool/Development requirements）。质量: 可用的极简模板，但信息量接近零，建议并入 body 或补全。
- **references/metrics.md**（3 行）: 仅 3 条占位符（Primary/Secondary/Guardrail）。质量: 同上，且与 body "Metric Selection" 节高度重叠，存在性价值存疑。
- **references/questions-to-ask.md**（10 行）: 6 个问题，与 body Initial Assessment 互补不重复 ✓。质量: 好。尾行 `---` 装饰性。
- **references/related-skills.md**（4 行）: 3 个跨技能 prose 引用（page-cro、analytics-tracking、copywriting），符合规范 §3.3 的 prose 引用要求 ✓。质量: 好。

### 5.4 Scripts 文件全文审查

- **scripts/ 目录不存在**（无脚本文件）。
- 根目录 `check.py`（84 行）承担脚本检查职责，全文审查如下：
  - 功能: 实现 11 个 script 判定（PROC-01/03/04/05/07、FMT-01/02/03、NEG-01/02、QA-01），返回 {criterion_id: bool}；LLM 判定的 10 项不在此运行。
  - 与 SCORING.yaml 模式串逐一比对: **11 个模式串全部一致** ✓。
  - 质量: 结构清晰（分区注释）、docstring 准确（"all 11 script checks" 与 11 项一致 ✓）。`os.path.exists(agent_output)` 的异常捕获（L24-28）处理了超长文本参数，考虑周全。依赖 `../_shared/checker.py` 的 output_contains 等函数——存在对外部共享库的合理依赖 ✓。
  - 小瑕疵: check() 中 tool_log 传入 set_tool_log_path 但未使用（可能输出函数内部使用），可忽略。
  - **结论: check.py 与 SCORING.yaml 完全对齐，无质量问题**。

### 5.5 跨 Skill 引用检查

- 顶层 SKILL.md: 无 `../` 路径引用 ✓；body 无跨技能 prose 引用（analytics-tracking 出现 0 次）✓ 合规。
- 顶层 references/related-skills.md: 3 个 prose 技能名引用（page-cro/analytics-tracking/copywriting）✓ 合规。
- 嵌套副本: description 含 "For tracking implementation, see analytics-tracking." —— **description 内跨技能路由，违反规范 §2.5**；body 含 5 个技能 prose 引用（page-cro、analytics-tracking、campaign-analytics、pricing-strategy、marketing-context）✓ 合规；另引用 `.claude/product-marketing-context.md` 与 "Reference marketing-context"——环境路径引用，非跨技能文件引用，可接受。

### 5.6 嵌套重复/死文件检查

- **ab-test-setup/ 嵌套目录**: 含一份完整 SKILL.md（304 行），与顶层版本同技能不同内容（frontmatter 不同、章节结构不同、参考文件不同），作者信息 "Ric Neves - Flowgrammers / v1.0.0 / 2026-03-06" 表明是**源注册表原始版**，而顶层 469 行版为规范化扩展版。属于**版本残留重复文件**——危险点: (1) 递归扫描的评测/加载工具可能读到两份 SKILL.md 造成歧义；(2) 副本自身含 2 处坏引用（sample-size-guide.md、test-templates.md 不存在）与 description 跨技能路由；(3) 未来维护者可能改错副本。**建议直接删除整个目录**。
- 无 .gitkeep、无隐藏死文件 ✓。

### 5.7 其他资源文件审查

- 无 assets/、templates/、examples/、docs/、tests/、agents/、resources/ 目录——无其他资源可审查。

---

## 6. 语法与格式质量（逐问题列举）

### 6.1 拼写错误

- **无问题发现**（全目录逐词扫描，无拼写错误）。

### 6.2 语法错误

- L351 "Means: <5% chance result is random" — 省略主语的电报式表述（应为 "This means there is <5% chance..."），表意可懂，属风格问题（🟢 级）。
- L356 "Statistical ≠ Practical" — 符号式短句，宣传风格可接受。
- **无实质语法错误**。

### 6.3 中英/葡英混杂

- 全文纯英文，无中英混杂、无葡萄牙语残留。**无问题发现**（嵌套副本同）。

### 6.4 Markdown 格式破损（3 处）

1. **L139-148 Test Duration 公式区**（🔴 严重）: "Duration = Required sample size per variant × Number of variants"（L139）与分母 "Daily traffic to test page × Conversion rate"（L143）被 `---`（L141）与多余空行切断，且无代码围栏——分子、分母、Minimum/Maximum 三块漂浮在页面中间，视觉上完全断裂。疑为原公式（分子/分母/分隔线 的 fenced block）丢失了围栏标记 ``` 与 `─────` 分隔线。
2. **L444 代码围栏未闭合**（🔴 严重）: Output Format 模板的 ``` 开在 L444，**文件在第 469 行结束仍未闭合**。后果: 从 L444 到 EOF 的全部内容（Test Plan Document 模板 + 6 个 Reference Files 链接）在渲染时全部成为代码块；L463 的 "## Reference Files" 不再作为章节标题；6 个 references 链接不会渲染为链接。
3. **references/analysis-plan.md L4 孤立围栏**（🟡 中等）: 单个 ``` 打开代码块后再未闭合，吞掉该文件其余内容（### Results Summary、### Recommendations）。

### 6.5 占位符未填充

- references 模板中的 `[What constitutes a win]`、`[If any]`、`[list]`、`[metric and definition]`、`[Name]`、`[ID in testing tool]` 等方括号占位符——均为**有意设计的模板占位符**（供 agent 填写），非未完成标记 ✓ 可接受。
- 无 TODO/FIXME/TBD/{{PLACEHOLDER}} ✓。

### 6.6 截断内容

- **references/analysis-plan.md**: 以孤立围栏和空壳小节结尾，疑为从 body 剪出时被截断（"### Results Summary / When the test is concluded" 等 1 行占位）——实质截断。
- references/implementation.md、metrics.md: 仅 3 行——极简截断（有意为之但价值过低）。
- 顶层 SKILL.md 与嵌套副本本身无截断（结尾完整）✓。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规范条目 | 结果 | 说明 |
|---|---------|:----:|------|
| 1 | name: 小写+连字符, ≤64 字符, 匹配目录 | ✅ | `ab-test-setup`，14 字符，匹配目录（不含 NNN 前缀） |
| 2 | description: 第三人称, WHAT+WHEN+KEYWORDS, ≤1024 | ✅ | 367 字符，三句分别覆盖 WHAT/WHAT 展开/WHEN+KEYWORDS |
| 3 | description: 无命令式/第一/第二人称 | ✅ | 名词短语开头；"Use when the user" 为规范 §2.4 认可的触发句式 |
| 4 | description: 无跨技能路由 | ✅ | 顶层合规；⚠️ 嵌套副本违规（"see analytics-tracking"） |
| 5 | description: 至少一个触发信号 | ✅ | "Use when the user wants to..." + 6 个关键词 |
| 6 | frontmatter: 无禁止键 | ✅ | 顶层仅 name/description；⚠️ 嵌套副本含 license/metadata/agents（禁止键） |
| 7 | body ≤ 600 行 | ✅ | 465 行 |
| 8 | body 有 workflow/process 节 | ✅ | 13 节流程完整 |
| 9 | body 有 output format 节 | ✅ | 有（渲染破损） |
| 10 | body 有 scope/limitations 节 | ❌ | **缺失**——唯一硬性违规 |
| 11 | body 无跨技能文件引用 | ✅ | 无 `../` 路径 |
| 12 | 目录 NNN-kebab-case 无空格大写 | ✅ | `158-ab-test-setup` |

**结论: 12 项中 11 项通过，1 项违规（Scope/Limitations 缺失）。** 另附注：嵌套副本独立违反第 4、6 项（若副本也被计入评估范围）。

---

## 8. 人机感评估

### 8.1 Emoji 审计

- SKILL.md、SCORING.yaml、check.py、references/ 全部文件: **0 emoji**。SCORING.yaml 注释中使用的 `──` 为制表符线字符，非 emoji ✓。
- **无问题发现**。

### 8.2 全大写/喊叫式语言

- 全大写词统计: CTA(5)、MVT(3)、MDE(2)、URL(1)、VWO(1) —— 全部为领域缩写 ✓ 合理。
- 喊叫式结构: "**DO:**"(1) 与 "**DON'T:**"(1) —— 成对出现的清单对照标题，功能性（Pre-Launch Checklist 的 DO/DON'T 对照），虽有命令语气但服务于防错目的，属可接受边界。
- STOP!/MANDATORY/CRITICAL/NEVER/ALWAYS: **0 次** ✓。
- **总体温和，无过度喊叫**。

### 8.3 Persona 语气分析

语气为"专家导师"型：直接、务实、以原则清单与模板驱动，不居高临下。代表引文：

1. "You are an experimentation and A/B testing expert."（L8）— 角色设定，第二人称（见 §8.5）。
2. "Not just 'let's see what happens'"（L36）— 口语化反例教学。
3. "Don't peek at results and stop early"（L326）— 禁令式但具体。
4. "Because [observation/data], we believe that [change] will cause [expected outcome] for [audience]."（L63-67）— 模板化、易复用。
5. "Statistical ≠ Practical"（L356）— 简洁金句式。
6. "Trust the process"（L341）— 口语化收尾，略显随意但亲切。
7. "Pre-commit to sample size and stick to it"（L339）— 行动导向。

整体: 专业、具体、无废话，与"workflow"型技能定位匹配 ✓。

### 8.4 人机边界分析

- **Agent 职责**: 采集测试上下文、构造假设、选指标、算样本量、设计变体、分配流量、选实施方式、出 Test Plan 文档、解释显著性。
- **人类职责**: 提供 baseline 转化率/流量/工具数据；MDE 的业务判断；实现 QA；批准上线；做最终业务决策（Practical Significance 判断）；补充 stakeholders 信息。
- 边界划分明确: L362-386 的 6 步检查表显式把"决策"留给业务方（"Is it worth the implementation cost?"），Pre-Launch Checklist 中"Stakeholders informed"隐式要求人工参与 ✓。
- 评估: **边界清晰合理**，无越界要求 agent 代替人做业务决策。

### 8.5 人称分析

- 顶层 SKILL.md body: "you" 11 次、"your" 3 次（集中在 L8 角色设定、假设模板说明、分析检查表提问"Did you hit sample size?"等）；"I" 0 次；"we" 6 次（全部出现在假设模板例句 "we believe that..." / "We will know..." 内——是假设框架模板的标准第一人称复数，属有意设计，非叙述人称）。
- 规范 §2.3 的人称禁令仅约束 description（description 完全合规，见 §2.2）；body 第二人称是 Claude Code 技能语料库通行的角色扮演规范，**不构成违规**。旧版 REVIEW 将 L8 "You are..." 判为"违反 SKILL-SPEC §2.3"属规范误用（见 §11）。

### 8.6 表格太多检查

- body 共 2 张表: 样本量速查表（L126-131）、结果解读表（L390-395）。另 1 张类表结构（Required Inputs 编号列表）。总数适中，均服务于数据对照，无表格堆砌 ✓。
- **无问题发现**。

---

## 9. 可执行性评估

### 9.1 独立可执行性 — 8/10

- 加分: 465 行自足内容、完整生命周期流程、2 张决策表、3 个可填模板、检查清单、明确输入清单。
- 扣分: (1) Test Duration 公式破损，agent 需自行重建公式推导；(2) Output Format 模板围栏未闭合，模板边界在原文中不清晰；(3) 无 Scope 节，agent 无法判断不适用场景；(4) SCORING FMT-01 要求的 3 个标题（## Metrics/## Implementation/## Analysis Plan）在模板中缺失，agent 严格照模板输出会漏项。
- 结论: 主体可执行性高，破损点均可由有经验的 agent 自行修复，但不应依赖 agent 猜测。

### 9.2 步骤可操作性（分步评分）

| 步骤（章节） | 行号 | 可操作性 | 问题 |
|-------------|------|:--------:|------|
| Initial Assessment | 11-29 | 4.5/5 | 问题清单清晰，输入字段明确 |
| Core Principles | 33-55 | 4.5/5 | 原则简明，可直接应用 |
| Hypothesis Framework | 58-86 | 5/5 | 模板+强弱例对比，最佳段落 |
| Test Types | 89-111 | 4/5 | 分类描述，无选择决策表（🟢 可补） |
| Sample Size Calculation | 115-148 | 3/5 | 速查表好，**公式区破损** |
| Metric Selection | 151-184 | 4.5/5 | 三类指标 + 3 个示例场景 |
| Designing Variants | 187-237 | 4.5/5 | 变体清单 + 文档模板 |
| Traffic Allocation | 242-262 | 4/5 | 三种策略 + 注意事项 |
| Implementation Approaches | 266-301 | 4/5 | 客户端/服务端对照，工具列举 |
| Running the Test | 305-341 | 5/5 | 清单 + DO/DON'T + peeking 解法 |
| Analyzing Results | 346-396 | 4.5/5 | 6 步检查 + 解读表 |
| Documenting and Learning | 400-437 | 4.5/5 | 完整文档模板 |
| Output Format | 440-469 | 2/5 | **围栏未闭合**，模板边界不明 |

### 9.3 工具依赖合理性

- frontmatter 无 allowed-tools（§2.3）；本技能运行不需要任何外部工具——无命令执行、无文件读写需求（仅可选读取 references/ 与用户工作区）。若补 allowed-tools，建议 `Read, Write, Glob, Grep` 即可。
- 外部 URL 依赖: L134-135 的 Evan Miller 与 Optimizely 计算器链接——评测环境若离线则失效。内容上公式本身未内联（速查表为近似值），建议 🟢 在 references 内置精确计算说明（或内联公式）作为离线兜底。
- **工具依赖: 极低，合理**。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

- **结构一致性**: total_items=21 = SCOPE 3 + PROC 8 + FMT 3 + NEG 4 + QA 2 + ERR 1 ✓；script 判定 11 项与 check.py 11 项逐一对应 ✓；LLM 判定 10 项均在 SCORING.yaml 有 judge: llm 标记 ✓。
- **与 SKILL.md 内容一致性**（重点核对 pattern 匹配的关键词是否存在于技能文本）:
  - PROC-03（evanmiller.org|optimizely.com）: L134-135 有 ✓。
  - PROC-04（Duration...weeks|days）: L139/L145 有 ✓（尽管渲染破损，原文文本存在）。
  - PROC-05（Primary|Secondary|Guardrail）: L153-166 有 ✓。
  - PROC-07（50/50|90/10|80/20|ramping）: L245-256 有 ✓。
  - NEG-01（peek|peeking|stop early）: L326-341 有 ✓。
  - NEG-02（mid-test|mid test）: **SKILL.md 全文无 "mid-test" 字样**——技能文本以 "Make changes to variants"、"Add traffic from new sources"（L327-328）表达同义约束，无该短语。agent 照技能措辞输出时可能不命中该 pattern（属宽松判定风险，🟡）。
  - QA-01（p-value|confidence interval|MDE|guardrail|segment）: L350-386 全命中 ✓。
  - FMT-01（## Hypothesis|## Test Design|## Variants|## Metrics|## Implementation|## Analysis Plan）: 模板含前 3 个标题，**缺后 3 个**（## Metrics、## Implementation、## Analysis Plan）——若 agent 严格照模板产出则 FMT-01 判定失败。模板与判据不一致（🟡）。其中 "## Analysis Plan" 仅存在于 references/analysis-plan.md 碎片。
  - **SCOPE-03（指向 analytics-tracking）**: 顶层 SKILL.md **全文无 analytics-tracking**（0 次）；该技能名仅出现在 references/related-skills.md 与嵌套副本中。判据要求的行为了解技能文本的 agent 无法自发执行——**判据与技能内容脱节（🟡，重大一致性缺口）**。
  - ERR-01、SCOPE-01/02、PROC-02/06/08、NEG-03/04、QA-02: 与技能内容均对齐 ✓。

### 10.2 Critical Failures 分析

- **CF-01**（无预定样本量 + peeking 建议）: 合理。技能 L47、L326-341 明确反对，判定可复现 ✓。
- **CF-02**（多变量当 A/B 卖）: 合理。技能 L40-43 "Test One Thing" + L96-99 A/B/n 需更多流量，判定可复现 ✓。
- **CF-03**（无主指标或只看统计显著性）: 合理。技能 L151-156 + L354-360 有直接依据，判定可复现 ✓。
- 三个 CF 全部 cap_to_0，力度适中，与技能强调的"统计严谨性"精神一致 ✓。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 记录（第 1148 行）: "| 158 | ab-test-setup | 重复段落+代码围栏破损 |"，任务描述补充的完整记录为 "🔴 Metric Selection 节重复两次、代码围栏破损。总评: 🟠 需修复重复与破损。"

逐项核验:

1. **"Metric Selection 节重复两次"** — **未复现/已修复**。grep 确认顶层 SKILL.md 与嵌套副本中 "## Metric Selection" 均只出现 1 次（顶层 L151）。当前文件无重复节。判定: 已修复（或档案基于旧版本）。
2. **"代码围栏破损"** — **仍存在（部分）**。顶层 SKILL.md 有 2 处（L139-148 公式区无围栏、L444 围栏未闭合至 EOF），references/analysis-plan.md 另有 1 处（L4 孤立围栏）。判定: 仍存在，且实际比档案记录的更严重。
3. **档案遗漏的问题**（本次审查新发现）:
   - **嵌套副本目录 ab-test-setup/** 整份重复 SKILL.md（304 行），含禁止 frontmatter 键与 2 处坏引用（§5.6）——档案未提及。
   - 顶层 frontmatter 缺 allowed-tools（§2.3）——档案未提及。
   - **Scope/Limitations 节缺失**（§3.2）——档案未提及。
   - **SCORING SCOPE-03 判据与技能内容脱节**（analytics-tracking 在技能文本中 0 出现，§10.1）——档案未提及。
   - FMT-01 模板缺 3 个标题、NEG-02 短语与技能文本不一致（§10.1）——档案未提及。
   - 样本量速查表 10%/50% 行 550 与精确值 ~647 偏差 18%（§4.3）——档案未提及。
   - 旧版 REVIEW.md 自身的问题: Skill 类型标为 "process" 与 SCORING.yaml 的 pattern: workflow 矛盾；L8 "You are..." 被判为违反规范 §2.3，但 §2.3 仅约束 description，属规范误用（§8.5）。

---

## 12. 综合评分

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | name/description 全合规；allowed-tools 缺失 |
| Body 结构完整 | 6/10 | 10% | 0.60 | 13 节流程完整；Scope 节缺失；Output 模板破损 |
| 逻辑一致性 | 8/10 | 20% | 1.60 | 步骤衔接闭合、无矛盾；公式格式破损但内容正确；速查表 1 行偏差 |
| 参考完整性 | 6/10 | 15% | 0.90 | 6/6 引用存在且被列出；analysis-plan.md 围栏破损；嵌套副本 2 处坏引用；3 个参考文件过薄 |
| 语法格式 | 6/10 | 10% | 0.60 | 无拼写错误；3 处围栏破损（含 1 处至 EOF 未闭合） |
| 规范合规 | 9/15 折算 9/10 | 15% | 1.35 | 12 项中 11 项通过，仅 Scope/Limitations 违规 |
| 人机感 | 9/10 | 10% | 0.90 | 0 emoji、语气专业、人称边界清晰；DO/DON'T 轻微喊叫 |
| 可执行性 | 8/10 | 10% | 0.80 | 13 步中 11 步 ≥4/5；公式区与模板区 2 处 2-3/5 |
| **加权总分** | | | **75.5/100** | **🟡 B** |

**Rating: 🟡 B（75.5/100）** — 内容质量实质优良（统计知识正确、流程完整、模板实用），主要失分集中在格式破损与结构缺口（可修复项），无内容性缺陷。旧版 REVIEW 评分 C+（45/100）偏低，主要因为只看了破损没看内容深度，且存在 2 处判断失误（技能类型、人称违规）。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

1. **Output Format 模板代码围栏未闭合（SKILL.md L444）**
   - 位置: SKILL.md 第 444 行 ``` 至文件末尾（L469）。
   - 问题: 开围栏后无闭合，L444-L469 全部内容（Test Plan Document 模板 + Reference Files 列表）渲染为代码块，"## Reference Files" 标题与 6 个链接全部失效。
   - 修复方向: 在文件末行（L469 之后）补一行 ``` 闭合围栏。
   - 后果若不修: 技能最重要的产出模板与全部参考链接对用户不可见；SCORING FMT-01 依赖的模板输出完整性受损。

2. **Test Duration 公式区格式破损（SKILL.md L137-148）**
   - 位置: "### Test Duration" 小节。
   - 问题: 分子（L139）与分母（L143）被 `---`（L141）切断、无围栏，Minimum/Maximum 悬浮。
   - 修复方向: 用 fenced block 重写为一行内联公式并配说明，例如：
     ```
     Duration = (Sample size per variant × Number of variants) ÷ (Daily traffic × Conversion rate)
     ```
     再以表格或列表给出 Minimum: 1-2 business cycles / Maximum: 避免过长（novelty effects、external factors）。
   - 后果若不修: 核心计算逻辑无法被 agent 直接引用，样本量→时长推导链断裂。

3. **references/analysis-plan.md 孤立围栏（L4）**
   - 位置: references/analysis-plan.md 第 4 行 ```。
   - 问题: 打开后未闭合，吞掉 ### Results Summary / ### Recommendations。
   - 修复方向: 删除 L4 围栏，并补全两个空壳小节内容（Results Summary 填写模板、Recommendations 决策模板各 2-3 行）。
   - 后果若不修: agent 读取该参考文件时得到残缺模板，输出 Analysis Plan 质量受损。

4. **嵌套副本目录 ab-test-setup/ 整目录删除**
   - 位置: D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\ab-test-setup\。
   - 问题: 含另一完整版本 SKILL.md（304 行），与顶层版本不一致；副本含禁止 frontmatter 键（license/metadata/agents）、description 跨技能路由、2 处坏引用（sample-size-guide.md、test-templates.md 不存在）。
   - 修复方向: 删除整个 ab-test-setup/ 目录（顶层版本为规范化权威版）。若需保留原始版权信息，按规范 §1.3 建议移入 body 末尾 "## Metadata" 节。
   - 后果若不修: 递归扫描的评测/加载工具可能命中错误版本；内容双源漂移；语料库完整性检查（如 196-cold-email 曾因"目录含重复残留"被记档）再次标记该技能。

### 🟡 重要缺陷（建议修复）

5. **补充 Scope / Limitations 节（body 缺失，规范第 10 项违规）**
   - 位置: SKILL.md 末尾（Output Format 之前或之后均可）。
   - 修复方向: 3-5 行清单: 不做因果推断/归因（工具外因素）；流量不足时不硬跑（引用 ERR-01 精神）；MVT 仅在流量充足时使用；不替代 analytics-tracking（测量实现）；不做贝叶斯/序贯方法的完整教程。
   - 后果: 修复后 12/12 规范项全通过。

6. **补 allowed-tools 字段（frontmatter）**
   - 位置: SKILL.md frontmatter。
   - 修复方向: 加 `allowed-tools: Read, Write, Glob, Grep`，理由: 技能仅需读取 references/ 与用户工作区上下文，无命令执行需求。
   - 后果: 与语料库惯例对齐，避免工具权限策略误判。

7. **SCORING.yaml SCOPE-03 判据与技能内容脱节**
   - 位置: SCORING.yaml L23-29 + SKILL.md body。
   - 修复方向（二选一）: (a) 在 SKILL.md Implementation Approaches 节末尾加一句 prose 引用——"For tracking/measurement implementation, see also: analytics-tracking"（符合规范 §3.3 prose 引用）；(b) 删除或改写 SCOPE-03。
   - 建议 (a): 既补判据依据又增加技能可用性。注意引用名须用 prose（"see also: analytics-tracking"），不可用 ../ 路径。

8. **FMT-01 判据与 Output 模板不一致**
   - 位置: SCORING.yaml FMT-01（L99-103）+ SKILL.md L444-469 模板。
   - 修复方向: 在 Test Plan Document 模板中补 "## Metrics"（主/次/护栏）、"## Implementation"（方式/工具）、"## Analysis Plan"（成功标准/分段）三个标题小节，与判据模式串对齐。
   - 后果: 消除"严格照模板输出却判不过"的陷阱。

9. **NEG-02 模式串与技能文本不同步**
   - 位置: SCORING.yaml NEG-02（L130-136）。
   - 修复方向: 模式串加宽为 '(mid-test|mid test|make changes to variants|add traffic)'，或在 SKILL.md DON'T 清单中补 "Changing things mid-test" 短语（与 common-mistakes.md 措辞一致）。
   - 后果: 消除宽松判定/漏判风险。

10. **样本量速查表标注近似值并修正 10%/50% 行**
    - 位置: SKILL.md L126-131。
    - 修复方向: 表头下加注 "近似值，基于 95% 显著性/80% 功效双侧检验"；10%/50% 行 550 改为约 650（精确 ~647）。
    - 后果: 防止 agent 按表给出偏小的样本量建议。

### 🟢 优化建议（锦上添花）

11. **Test Types 增加选择决策表** — L89-111 目前为纯列表，可按"变体数量 × 流量水平 × 变更类型"3 条件给一行决策表，提升可执行性（符合规范 §3.4 "decision trees over prose"）。
12. **Description 句 1 补动词** — "A/B testing and experimentation design..." 改为 "Provides A/B testing and experimentation design with statistical validity."，消除电报感。
13. **references/implementation.md 与 metrics.md 并回 body 或补全** — 各 3 行的占位符模板信息量近零；建议将 metrics 模板并入 Metric Selection 节，implementation 并入 Implementation Approaches 节，references/ 瘦身。
14. **外部计算器 URL 离线兜底** — L134-135 链接在离线评测环境不可达；建议在 Sample Size Calculation 节内联精确公式（或新增 references/sample-size-formula.md）。
15. **"p-value < 5% chance result is random" 措辞精确化** — 改为 "小于 5% 概率在无效假设下观察到该结果"，避免统计误读传播。
16. **清理尾行装饰性 `---`** — common-mistakes.md L20 与 questions-to-ask.md L10 尾部孤立 `---` 删除。
17. **旧版 REVIEW 遗留项复核** — 旧版指出的"外部 URL 可能失效"与"样本量近似"两项已并入本清单 14/10；旧版"第二人称违规"判定为误判，无需修复（但若语料库统一要求 body 第三人称，可将 L8 改为 "The agent is an experimentation and A/B testing expert."——非必需）。

### 修复工作量估计

- 改动文件: SKILL.md（约 +35/−10 行: 闭合围栏 1 行、公式区重写 8 行、Scope 节 6 行、模板补 3 小节 12 行、allowed-tools 1 行、速查表注记 2 行）、references/analysis-plan.md（约 +5 行: 删围栏、补内容）、SCORING.yaml（约 2 行: NEG-02 模式串，可选）、references/common-mistakes.md + questions-to-ask.md（各 −1 行）。
- 删除文件: 整个 ab-test-setup/ 目录（304 行副本）。
- 合计: 约 50-60 行增删改 + 1 个目录删除；预计 30-45 分钟人工工作量。优先做 🔴 四项（约 20 分钟），即可将评分提升至 85+（🟢A 区）。

---

## 附录: 审查过程记录

- 审查方式: 全目录递归 Glob + 逐文件全文 Read（无抽样）+ 程序化校验（grep/fence 审计/YAML 解析/样本量数值复核）。
- 读取文件清单（行数）:
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\SKILL.md（469 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\ab-test-setup\SKILL.md（304 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\SCORING.yaml（191 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\check.py（84 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\REVIEW.md（51 行, 旧版）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\analysis-plan.md（11 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\common-mistakes.md（20 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\implementation.md（3 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\metrics.md（3 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\questions-to-ask.md（10 行）
  - D:\SkillIF\skill-experiment\complex-skills\158-ab-test-setup\references\related-skills.md（4 行）
- 外部依据: D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md（162 行, v1.0.0 全条对照）; C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md（第 1148 行条目核验）。
- 程序化校验项: 描述字符数（367）、人称统计（you 11 / your 3 / we 6 / I 0）、emoji 扫描（0）、全大写词、代码围栏配对审计（顶层 7 处围栏 3 对 + 1 未闭合）、'## Metric Selection' 计数（各 1）、cross-skill 引用扫描（../ 为 0）、样本量 12 行数值复核（Evan Miller 公式, 95%/80% 双侧）。
- 本次审查仅写入 REVIEW.md，未修改任何其他文件。
