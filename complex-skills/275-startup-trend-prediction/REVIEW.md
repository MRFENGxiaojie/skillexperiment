# REVIEW.md — 275-startup-trend-prediction 技能审计报告

- 审计日期：2026-08-06
- 审计对象：`D:\SkillIF\skill-experiment\complex-skills\275-startup-trend-prediction\`
- 审计范围：SKILL.md、SCORING.yaml、check.py 共 3 个文件，全部全文精读（本技能无 references/ 与 scripts/ 目录）
- 审计基准：`_shared/SKILL-SPEC.md`（v1.0）第 5 节 12 项合规清单、`_shared/checker.py` 源码、SCORING.yaml 与 check.py 的交叉对照
- 验证手段：除静态阅读外，对 frontmatter 与 SCORING.yaml 做了 PyYAML 实际解析，对 check.py 做了 py_compile 编译验证与 checker 库源码核对，对 Bass 扩散模型"达到 50% 采用所需时间"列做了公式手工复算，对 ROI 算例做了复算，对 Integration Points 提到的 5 个技能在语料库中的存在性做了逐一检索

---

## 1. 目录清单

本技能目录共 3 个文件，无任何子目录：

- `SKILL.md`（377 行，技能主体，全部知识内聚于单一文件）
- `SCORING.yaml`（150 行，16 条测评标准 + 3 条致命失败项）
- `check.py`（64 行，评测脚本，仅实现 1 条脚本判定）

目录命名 `275-startup-trend-prediction` 符合 `NNN-kebab-case` 规范，与 frontmatter 的 `name: startup-trend-prediction` 一致（NNN 前缀按既有审计口径不计入 name 匹配），无空格无大写。

目录结构层面的第一个显著事实是：**本技能没有任何参考文件**。SKILL.md 第 232-249 行的 "Navigation" 一节却以 "Resources (Deep Dives)"（第 234-237 行）、"Templates (Outputs)"（第 239-243 行）、"Data"（第 245-249 行）三个分组列出了子文件的导航位，其中 Data 分组明确给出一个链接 `[sources.json](data/sources.json)`（第 249 行），但目录中不存在 `data/` 目录，也不存在任何被导航的子文件。这是明显的脚手架残留：技能在设计时预留了参考文件与模板的挂载点，最终打包时没有填充，也没有把空壳导航删掉。该问题在第 3、4、5、9 节展开。

第二个事实：技能主体 377 行、约 12.5KB 的知识全部塞在主文件里，属于典型的"单体式"技能。考虑到 pattern 是 process（规范建议 ~200 行、硬上限 600），377 行在合法范围内，但其中存在若干空壳小节与冗余段落（详见第 3、4 节），实际有效行数约 340 行。

---

## 2. Frontmatter

### 2.1 name 字段

`name: startup-trend-prediction`。小写字母加连字符，长度 24 字符，远低于 64 字符上限，与目录名（除 NNN 前缀外）逐字一致。通过。

### 2.2 description 字段（长度 / WHAT / WHEN / KEYWORDS）

description 位于 SKILL.md 第 3 行，实测长度 272 字符（PyYAML 解析实测），远低于 1024 上限，通过。

从内容结构看，它被分号拆成两个句子。第一句 "Predict market/tech/business-model trends and market-entry timing (enter/wait/avoid) by analyzing 2-3 years of signals to forecast 1-2 years ahead." 回答了 WHAT：预测市场/技术/商业模式趋势并给出入场时机（enter/wait/avoid 三态决策），方法侧写明"分析 2-3 年信号、预测 1-2 年前景"，语义密度高，且与 body 第 8 行的 "Look back 2-3 years to predict 1-2 years ahead" 完全互文。第二句 "use for questions like market timing, trend trajectory (rising/peaking/declining), adoption curve stage, or what comes next." 回答了 WHEN：market timing、trend trajectory、adoption curve stage、what comes next 四个触发场景，句首 "use for" 正是规范 2.4 节允许的触发信号句式之一。KEYWORDS 方面，"market timing""trend trajectory""adoption curve""market-entry"都是领域检索词，检索友好度充足。

这是本项目语料中 description 写得最干净的一批之一：WHAT/WHEN/KEYWORDS 三要素齐备、无冗余触发短语堆叠、272 字符把字符预算花得恰到好处。通过，无扣分点。

### 2.3 人称与语气

整体为第三人称。开头 "Predict ..." 是描述技能的第三人称陈述，与规范 good example 同构；第二句 "use for questions like ..." 是规范 2.4 节明确允许的触发句式（"Use for..."），不是祈使句 "Use this skill to..."，也不是禁止的 "Use this skill whenever..."。无第一/第二人称。通过。

### 2.4 触发信号

"use for" 属于规范 2.4 节列举的五种允许句式之一，且后接具体触发场景短语，信号明确可操作。通过。

### 2.5 可选字段与禁止字段

frontmatter 只含 `name` 和 `description` 两个键（PyYAML 解析实测），无任何规范 1.3 节禁止的字段。六个允许的可选字段一个都没有使用——不违规。但本技能的核心执行依赖 WebSearch 工具（Trend Awareness Protocol 第 329 行强制要求），声明 `allowed-tools: WebSearch` 能让 harness 侧的权限与工具预授权更顺（详见第 9 节），属于建议而非必需。

---

## 3. Body 结构

### 3.1 总体布局

SKILL.md 的 body 从第 6 行 H1 标题 "# Startup Trend Prediction" 开始，共 14 个二级小节，顺序为：Quick Reference（第 16 行）→ Adoption Curve Framework（第 47 行）→ Cycle Pattern Library（第 99 行）→ Signal vs Noise Framework（第 127 行）→ Prediction Methodology（第 167 行）→ Navigation（第 232 行）→ Key Principles（第 253 行）→ Do / Avoid（第 303 行）→ What Good Looks Like（第 317 行）→ Trend Awareness Protocol（第 327 行）→ Integration Points（第 366 行）。

结构的核心张力在于：真正的执行流程（Prediction Methodology 的 Step 1-5，第 167-228 行）被放在了三个框架库（Adoption Curve、Cycle Pattern Library、Signal vs Noise）之后。对一个 agent 而言，"先看什么"的入口其实在文件最前面的 Quick Reference（第 16-43 行），而 Quick Reference 又与后面的方法论存在大面积内容重叠（见 3.3）。换句话说，这个文件同时存在"入门速查"与"完整方法论"两套讲法，读者（agent）要么读两遍，要么只读其一而漏掉另一套里的独有信息（例如 Quick Reference 的"信号表"在 Signal vs Noise Framework 中有更完整的 14 行版本；Reference Class Forecast 只存在于 Step 3）。

### 3.2 空壳小节（三处）

结构上有三处明显的"占位符残留"：

1. **`### Rogers Diffusion Model`（第 49 行）完全为空**。标题下方直接是两个空行，然后是下一个标题 `### Bass Diffusion Model (Quantitative)`。Rogers 模型的内容实际上以 "Position Identification"（第 77-85 行，Innovators/Early Adopters/Early Majority/Late Majority/Laggards 五段表）的形式存在于同一大节之下，但空标题的存在让读者在"Rogers 模型"和"位置判定"之间产生认知断裂——标题承诺了内容却直接跳过了。
2. **Navigation 的 Resources（Deep Dives）表（第 234-237 行）为空**：只有 `| Resource | Purpose |` 表头，零行数据。
3. **Navigation 的 Templates（Outputs）表（第 239-243 行）为空**：同样只有表头。这两个空表加上第 245-249 行 Data 表中指向不存在文件的链接，构成"导航指向虚空"的整体印象。

### 3.3 内容重叠与日期戳冗余

文件里存在三处带日期戳的"当前最佳实践"块：第 10-14 行 "**Modern Best Practices (Jan 2026)**"、第 16 行 "Quick Reference: Building a Trend View (Dec 2025)"、第 303 行 "## Do / Avoid (Dec 2025)"。三块内容互相重叠且口径不齐：

- "Modern Best Practices (Jan 2026)" 的四条（三角验证、领先/滞后指标、炒作周期防御、绑定决策）与 Quick Reference 的第 2/3/4 步、Do/Avoid 的条目、Web Search Safety（第 331-337 行）几乎逐条重复。例如"三角验证 3+ 独立信号"在 Modern Best Practices、Quick Reference 信号表、"Multiple Signals Required"（第 286-291 行）、Web Search Safety（第 337 行）出现至少四次。
- 三块使用了两个不同日期（Dec 2025、Jan 2026），且没有任何说明哪块是当前权威版本。对读者而言，"Dec 2025 版"与"Jan 2026 版"并存只能被解释为作者迭代后没有清理旧块。

这种"日期戳 + 逐次追加"的编辑方式在单文件技能里会随时间持续恶化：审计日 2026-08-06 距两个日期戳已 7-8 个月，文件内部的"最新版"标记已经过时。建议统一为一个版本标记并合并重复内容（详见第 13 节）。

### 3.4 Workflow/Process

Prediction Methodology（第 167-228 行）是本技能的执行主干：Step 1 Define Scope（代码块模板）、Step 2 Gather Historical Data（四行年度表，{{YEAR-3}}/{{YEAR-2}}/{{YEAR-1}}/{{NOW}} 占位符）、Step 3 Identify Patterns（六种模式清单 + Reference Class Forecast 小节，第 197-209 行，含 5-10 个类比、base rate、p10/p50/p90 时机表）、Step 4 Generate Prediction（Thesis/Confidence/Timing/Evidence/Counter-evidence 五字段 markdown 模板）、Step 5 Identify Opportunities（时机窗口/竞争/动作三列表）。五步顺序合理、每步有明确产出，是符合规范 3.1 节"step by step"要求的流程章节。其中 Reference Class Forecast 是难得的方法论增量——把"参考类比 + 基准率 + 概率区间"这一套业界做预测的严肃工具写进了流程，而不是停留在"多找几个信号"的泛泛之谈。

### 3.5 Output Format（边界通过，附两个缺陷）

规范 3.1 节要求 body 回答"用户最终拿到什么、结果长什么样"。本技能没有独立的 Output Format 章节，但存在两处输出契约：

- Step 4 的 `## Prediction: [TOPIC]` 模板（第 213-221 行）定义了预测本身的五字段结构；
- Trend Awareness Protocol 的 "What to Report"（第 346-353 行）定义了搜索后汇报的四要素（Current state / Trajectory / Timing window / Evidence quality）。

缺陷有二：其一，两处输出契约并行且互不提及，agent 不知道该以哪份为准——Step 4 的预测模板不包含"当前状态/轨迹/时机窗口/证据质量"四要素，What to Report 又完全没有机会表、市场容量、假设清单等 Step 5 与 SCORING 要求的输出；其二，SCORING 的 OUT-01/OUT-02/OUT-03 要求的输出（轨迹、时机窗口、机会表、假设与敏感性区间、证伪标准）分散在 Step 3/4/5、What to Report、What Good Looks Like 三处，没有一处把它们汇总成一个完整的交付物结构。对单次测评对话而言，agent 输出"预测模板 + 四要素汇报 + 机会表"时已经足够覆盖 16 条标准，所以这里判定为"边界通过"而非"不通过"，但建议补一个统一的 Output Format 小节（详见第 13 节第 4 条）。

### 3.6 Scope/Limitations（缺失）

全篇没有 Scope / Limitations 章节，没有任何"本技能不做什么、什么时候不该用"的反向约束。结合 description 2.5 节"跨技能路由禁止写入 description，必须放在 body 的 Scope 节"的规则，以下边界本应写在 body 里：

- 本技能做的是"趋势判断 + 时机决策"，不替代财务建模、竞品尽调或投资决策；
- 硬性依赖 WebSearch 工具与网络环境，离线环境下无法满足 Trend Awareness Protocol 的强制搜索要求；
- 对没有任何信号数据的完全虚构题材（如纯假设性问题），框架的可执行性会下降；
- enter/wait/avoid 中的 avoid 也是一种有效结论，不存在"必须给出入场建议"的倾向。

缺了这一节，agent 在遇到边界场景（如用户只是闲聊趋势、没有给出任何数据）时缺乏明确的降级指引，会机械地跑完五步流程。这是 12 项合规清单中唯一明确失分项（见第 7 节第 10 项）。

### 3.7 行数与体积

SKILL.md 实测 377 行，低于 600 行硬上限，通过。但注意：由于没有参考文件，377 行里混着框架库（Adoption Curve/Cycle Pattern/Signal-Noise 三个大节，约 120 行）、执行流程、原则宣言、协议与导航，层级是扁平的。若按 Navigation 的设计意图把三个框架库下沉到 references/，主文件可以压到 250 行以内，但这是重构建议而非合规问题。

---

## 4. 逻辑一致性

### 4.1 Bass 扩散模型"Time to 50%"列三处数学错误（实测复算）

这是本技能最实质的硬伤。第 56-69 行给出 Bass 模型公式：

```
F(t) = [1 - e^(-(p+q)*t)] / [1 + (q/p) * e^(-(p+q)*t)]
```

第 71-75 行的场景表给出三组 (p, q) 及其"Time to 50%"：Viral consumer (0.05, 0.5) → ~3 年；B2B SaaS (0.02, 0.3) → ~5 年；Enterprise (0.01, 0.15) → ~8 年。我用公式手工求解 F(t)=0.5（推导：令 x=e^(-(p+q)t)，则 (1-x)/(1+(q/p)x)=0.5，得 x=1/(2+q/p)，故 t = ln(2+q/p)/(p+q)），三行全部对不上：

- Viral consumer (0.05, 0.5)：t = ln(2+10)/0.55 = 4.5 年，表格写 ~3 年，差 1.5 年；
- B2B SaaS (0.02, 0.3)：t = ln(17)/0.32 = 8.9 年，表格写 ~5 年，差约 4 年；
- Enterprise (0.01, 0.15)：t = ln(17)/0.16 = 17.7 年，表格写 ~8 年，差约 10 年。

三行全部错误且错误方向一致（声称值约为公式值的 55%-60%），说明不是笔误而是作者用了错误的近似（或没有复算）。更值得注意的是第 65-68 行的"Typical values"（Consumer products p=0.03/q=0.38、B2B software p=0.01/q=0.25、Enterprise tech p=0.005/q=0.15）按公式算出的 t50 分别为 6.6、12.7、22.4 年——比场景表的声称值更大。对一个"教 agent 做采用预测"的技能而言，公式与示例互相矛盾的后果是：agent 无论用哪组参数都会得到一个与自己行为不一致的教学示范。这是第 13 节 🔴 第 1 条的修复对象。

### 4.2 两组 p/q 参数表互相冲突

第 65-68 行的"Typical values"与第 71-75 行的场景表描述了近乎同名、取值却不同的类别：Consumer products (0.03, 0.38) 对 Viral consumer (0.05, 0.5)；B2B software (0.01, 0.25) 对 B2B SaaS (0.02, 0.3)；Enterprise tech (0.005, 0.15) 对 Enterprise (0.01, 0.15)。若作者本意是"典型值"与"快/中/慢场景"两套口径，应在表中注明映射关系；现在两表并列、分类名几乎同义，agent 无法判断该用哪组。建议合并为一张表（每行给类别、p、q、t50 计算值、备注），同时消除 4.1 的数学错误。

### 4.3 Bass 模型的"典型值"与常识偏差（补充观察）

第 65-68 行 Enterprise tech p=0.005 意味着"外部影响系数"低到几乎完全依赖口碑传播，配合 q=0.15，按公式 t50 达 22.4 年——这个数字本身对"企业级技术"的直觉（通常 5-10 年）明显偏高，是参数组合不当的又一佐证。修复 4.1 时应一并重审参数值，而不是只改表格里声称的时间。

### 4.4 占位符语法不统一

Step 1 模板（第 172-176 行）使用方括号 `[Technology / Market / Business Model]` 式占位，Step 3 的参考类比表（第 205-209 行）也用方括号（`[e.g., 10% enterprise adoption...]`）；而 Quick Reference（第 21-22 行 {{HORIZON}}/{{BUYER}}/{{MARKET}}）、Step 2 年度表（第 183-186 行 {{YEAR-3}}/{{YEAR-2}}/{{YEAR-1}}/{{NOW}}）、Step 5 机会表（第 227-228 行 {{OPP_1}}/{{WINDOW}}）使用双花括号。两种占位约定在同一文件内并存，且 `{{NOW}}` 语义含糊（agent 应填入实际当前年份，但占位符名更像"当前时刻"）。对需要解析模板的 agent 来说，统一的占位符语法能显著降低歧义。

### 4.5 Integration Points 引用了 4 个不存在的技能

第 366-377 行的 Integration Points 提到 5 个其他技能：Feeds Into 的 `startup-idea-validation`、`router-startup`、`product-management`，Receives From 的 `startup-review-mining`、`startup-competitive-analysis`。我在 `complex-skills/` 与 `complex-skills-no-trigger/` 两个语料集中逐一检索这 5 个 name：

- `startup-idea-validation`：存在（297-startup-idea-validation）；
- `router-startup`：不存在；
- `product-management`：不存在（语料中仅有 105-product-manager-toolkit、253-product-audit、254-product-marketing 等相近但不同名技能）；
- `startup-review-mining`：不存在；
- `startup-competitive-analysis`：不存在（最近的 256-competitive-landscape 不同名）。

5 个引用中 4 个指向虚空。规范 3.3 节允许以散文方式引用其他技能名，但引用的前提是目标存在；对测评语料而言，agent 若顺着 Integration Points 去检索这些技能会得到空结果，且这些名字暗示了一个并不存在的技能生态（router-startup 等）。建议逐一核实并改为实际存在的技能名，或删除无法落地的条目。

### 4.6 其余一致性观察

- **死链 data/sources.json**：第 249 行链接指向 `data/sources.json`，目录中无 `data/`。这是全技能唯一的文件链接，直接断裂（详见第 5、9 节）。
- **"Very High" 超出量纲**：Strong Signals 表的 Weight 列（第 137 行）出现 "Very High"，而该列在 Strong/Moderate/Weak 三张表（第 131-155 行）的取值域是 High/Medium/Low，"Very High" 是域外值。
- **ROI 算例复算正确**：第 280-284 行的示例，Early Majority CAC=$100 对应表中 1.0x 基准（第 275 行），Late Majority CAC=$250 对应 2-3x 区间（第 276 行）；ROI factor = (100/100)×0.15 = 0.15、 (100/250)×0.05 = 0.02，比值 7.5 与第 284 行 "**7.5x better outcome**" 完全吻合。唯一小瑕疵是示例的 bullet 把 Early Majority 简写为 "Early"（第 282 行），与表中 "Early (Innovators) 0.5x" 的 "Early" 指代不同对象，字面上易混。
- **流程口径自洽**：Lookback 2-3 年 / Horizon 1-2 年在第 8 行、第 173-174 行、description 中三处一致；Rogers 五段百分比（<2.5% / 2.5-16% / 16-50% / 50-84% / 84-100%，第 79-85 行）是标准口径；Gartner Hype Cycle 五阶段与 Action 列（第 89-95 行）内部自洽。信号表（Quick Reference 第 26-32 行）与 Signal vs Noise Framework（第 127-163 行）的领先/滞后归类一致（Regulation/Platform/Buyer 为 Leading，Usage/Revenue 为 Lagging，Media 为 Weak）。
- **日期戳内部矛盾**：第 10 行 "Modern Best Practices (Jan 2026)" 与第 16、303 行 "(Dec 2025)" 并存，见 3.3。另注意 Trend Awareness Protocol 的 Required Searches（第 339-344 行）硬编码年份 "2026"（"trends 2026" 等四条），2027 年后这些模板将系统性过时，属于"需要按年维护"的隐性依赖。

---

## 5. 参考文件（全文精读）

按审计要求，本目录 3 个文件（SKILL.md、SCORING.yaml、check.py）均全文逐行精读完毕，结论如下。

### 5.1 技能本体不含任何参考文件

`275-startup-trend-prediction/` 下没有 `references/` 目录、没有 `data/` 目录、没有 `scripts/` 目录。这是本项目语料中少见的"零参考文件"技能——全部知识内聚于 SKILL.md 的 377 行内。

这一事实本身不是违规（规范对参考文件是"超出 600 行才必须下沉"的要求，没有强制"必须使用参考文件"），但与本技能 Navigation 节的脚手架形成了尖锐对比：

- 第 234-237 行 "Resources (Deep Dives)" 表：空表，承诺了深度资料但没有目标文件；
- 第 239-243 行 "Templates (Outputs)" 表：空表，承诺了输出模板但没有目标文件（Step 4 的预测模板其实就内联在 body 第 213-221 行，说明作者原本打算把它拆出去）；
- 第 245-249 行 "Data" 表：唯一一行 `[sources.json](data/sources.json) | Trend data sources (analyst reports, market data, filings, etc.)`，链接目标不存在。

对按"参考文件要全文阅读"惯例工作的 agent 而言，读到 Navigation 后会去打开 data/sources.json——得到的是文件不存在错误。这是比"没有参考文件"更糟的状态：索引存在、索引指向虚空。三处要么填充、要么删除（修复见第 13 节 🔴 第 2 条）。

### 5.2 缺失文件的内容预期（按 SKILL.md 的自我描述推断）

第 249 行对 sources.json 的描述是 "Trend data sources (analyst reports, market data, filings, etc.)"。结合 Signal vs Noise Framework 的检测方法列（第 131-155 行：VC 季度投资跟踪、M&A 监控、LinkedIn/Indeed 职位数据、GitHub 活跃度、Gartner/Forrester 报告、Algolia/HN/Reddit/ProductHunt 追踪），sources.json 应是一份"趋势数据源清单"，把 Strong/Moderate/Weak 三层信号的 14 个数据源以结构化 JSON 落盘。这个文件若补齐，能显著增强技能的可执行性（agent 无需每次重新发明数据源清单）；现在缺位，数据源知识只能靠 agent 从三张表格里自行检索。

### 5.3 SCORING.yaml 与 check.py（按参考文件口径审阅）

按审计惯例，评测配套文件（SCORING.yaml、check.py）也作为"文件全集"的一部分全文精读（其深度分析见第 6、10 节）。此处给出结论性评价：两者与 SKILL.md 的互文关系是本技能质量最高的部分——16 条标准全部能在 body 中找到逐字级支撑（映射明细见第 10 节），check.py 的 1 条脚本判定与 SCORING 的 SCOPE-02 完全一致。作为"评测文件-技能内容"的对照样本，这两个文件堪称模板级。

### 5.4 参考文件小结

本技能参考文件层的总体印象是"结构设计存在、内容全部缺失"：Navigation 的分组导航（Deep Dives / Templates / Data）暗示作者原本规划了三类子文件，但交付时只留下了三个空壳。这与 291 号技能"一半参考文件是空壳"的问题同源但更极端——291 是文件存在而内容残缺，本技能是索引存在而文件全无。好消息是：由于主文件自包含且质量尚可（见第 4、8 节），参考文件缺失不直接损害主流程可执行性，损失的是"深潜资料"与"数据源清单"两个增强层。

---

## 6. 语法与格式

### 6.1 Frontmatter YAML

用 PyYAML 实测解析通过。frontmatter 只含 `name`、`description` 两个键。description 内嵌括号、斜杠、分号与连字符，作为 plain scalar 全部安全，实测无解析错误。

### 6.2 SCORING.yaml 与 check.py 语法

SCORING.yaml 用 PyYAML 实测解析通过。顶层键为 skill/pattern/total_items/criteria/critical_failures 五项；criteria 恰为 16 条（scope 3 + process 7 + output 3 + negative 2 + qa 1），与 `total_items: 16` 一致；critical_failures 3 条，与 CF-01 至 CF-03 一一对应。`judge: script` 的条目仅 SCOPE-02 一条，其 `check.fn: tool_log_contains` 与 `pattern: '"WebSearch"'` 与 check.py 第 27 行的 `tool_log_contains('"WebSearch"')` 逐字符一致，SCORING 与 check.py 无遗漏、无多余。

check.py 通过 py_compile 编译；第 10-15 行的 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))` 解析目标 `complex-skills/_shared/checker.py` 实测存在，导入链畅通；docstring "Run all 1 script checks"（第 19 行）与实现一致（确实只有 1 条脚本判定），注释准确。两处小问题：其一，check() 第 22 行 `set_agent_output(agent_output)` 把**路径字符串**传给了需要**文本内容**的 setter，随后 main() 第 53-55 行又把文件内容读出来传入——由于本技能没有任何 output_* 检查，当前功能上无害，但与 291 号技能 check.py 相同的这段"注定无用的代码"会误导后续维护者以为输出检查在这里被处理了；其二，`workspace` 参数全程未使用，属预留接口，可接受。

### 6.3 Markdown 围栏与表格

SKILL.md 的代码围栏共 3 处（Bass 公式块第 56-69 行、Step 1 模板第 171-177 行、Step 4 模板第 213-221 行），全部配对闭合，围栏内的嵌套反引号（Step 4 模板无嵌套）无转义问题。全部表格（约 12 张）分隔行格式规范，无管道符缺失、无行数错位。第 272-276 行 ROI 表的表头分隔行 `| ------------ | ...` 带空格，Markdown 解析正常，风格略不统一，可忽略。

### 6.4 链接

全文件只有一个文件链接：第 249 行 `[sources.json](data/sources.json)`，目标不存在（死链）。除此之外无其他链接。Integration Points 的 5 个技能引用（第 370-372、375-377 行）以反引号散文形式出现，不是文件链接，但其中 4 个目标技能在语料库中不存在（见 4.5）。

### 6.5 其他格式细节

- 空行使用规范，节间分隔线 `---` 一致（第 45、97、125、165、230、251、301、364 行）。
- H1 标题（第 6 行 "# Startup Trend Prediction"）后无 frontmatter 余赘，直接进入正文。
- `{{YEAR-3}}`、`{{NOW}}` 等占位符在表格单元格内格式正常，无 Markdown 解析问题。
- 全文无全角字符混入、无控制字符；文件编码 UTF-8 实测正常。

---

## 7. 规范合规（12 项清单）

按 SKILL-SPEC v1.0 第 5 节合规清单逐项核对：

1. name 小写+连字符、≤64、与目录一致——通过（`startup-trend-prediction`，目录 `275-startup-trend-prediction`）。
2. description 第三人称、含 WHAT+WHEN+KEYWORDS、≤1024——通过（272 字符，三要素齐备，见 2.2）。
3. description 无祈使/第一/第二人称开头——通过。以第三人称 "Predict ..." 开头，"use for ..." 是允许的触发句式而非祈使句。
4. description 无跨技能路由——通过。
5. description 至少一个触发信号句式——通过（"use for questions like ..."）。
6. frontmatter 无允许列表之外的键——通过（仅 name + description，实测解析）。
7. body ≤600 行——通过（377 行）。
8. body 含 Workflow/Process 章节——通过（Prediction Methodology 五步流程 + Quick Reference，质量良好）。
9. body 含 Output Format 章节——**边界通过**。无独立章节，但 Step 4 模板（第 213-221 行）与 What to Report（第 346-353 行）构成两处并行输出契约，未统一、互不提及，详见 3.5。
10. body 含 Scope/Limitations 章节——**不通过**。全篇无任何反向边界声明，详见 3.6。
11. body 无跨技能文件引用——通过。文件引用仅 `data/sources.json`（内部相对路径，格式合规、目标缺失属内容问题）；5 个技能引用均为散文形式（规范允许），但 4 个目标技能不存在（内容问题，见 4.5）。check.py 引用 `..\_shared\checker` 属评测 harness 标准约定，不计入技能内容违规。
12. 目录 NNN-kebab-case、无空格大写——通过（275-startup-trend-prediction）。

结论：12 项中 10 项明确通过、1 项边界通过（第 9 项 Output Format）、1 项明确不通过（第 10 项 Scope/Limitations）。换成分数口径约 10.5/12。与 291 号技能相比，本技能在 description 合规上零瑕疵，失分集中在 body 的两个结构性缺项（Output Format 未统一、Scope/Limitations 完全缺失）——而 Scope/Limitations 的缺失在"流程类技能"上的影响尤其明显：流程技能的适用边界就是它的准入契约。

---

## 8. 人机感

### 8.1 阅读体验

本技能的可读性总体良好，是"讲人话"的写法：Quick Reference 的四步从"决策→信号→防御→容量核对"串成一条人类可懂的思维链；Key Principles 里 "Timing Beats Being Right"、"History Rhymes" 这类标题有记忆点；Do / Avoid 与 What Good Looks Like 直接给出行为契约，agent 读完后能立刻知道"合规输出长什么样"。三张框架库表格（Rogers 五段、Gartner 五阶段、Cycle Pattern 三库）的信息密度高、一眼可扫，作为参考库是合格的。

### 8.2 空壳对体验的伤害

三处空壳（空标题 Rogers、空表 Resources/Templates、死链 sources.json）与整体文风的工整形成反差。对真人读者，空表是"没做完"的信号；对 agent 读者，死链会触发一次失败的文件操作，打断流程。这是打包时未做最终质检的痕迹。

### 8.3 日期戳带来的"时效焦虑"

"(Dec 2025)"、"(Jan 2026)" 的日期戳原本是为了表达"本节已更新"，但三块并存、互不声明权威性，反而制造了"哪条规则还有效"的困惑。真人读者会怀疑 Dec 2025 的 Quick Reference 是否已被 Jan 2026 的 Best Practices 取代；agent 则可能把两套近似重复的指令都执行一遍（例如把三角验证写成四条而不仅是三条）。

### 8.4 占位符的可用性

`{{HORIZON}}`、`{{BUYER}}`、`{{MARKET}}`、`{{OPP_1}}`、`{{WINDOW}}`、`{{YEAR-3}}` 等占位符对 agent 是自然可替换的模板语法，比纯文本提示更利于结构化填充；但方括号式占位（Step 1/3）与双花括号式占位混用（见 4.4）会让"替换规则"变得不明确。统一为一种语法后体验会更好。

### 8.5 措辞与受众

技能面向创始人/产品人/投资人视角，术语（Rogers、Bass、Gartner Hype Cycle、p10/p50/p90、TAM/SAM/SOM、CAC）与其目标受众匹配，未出现行话滥用。What Good Looks Like 第 323 行 "Pragmatic scalability: capital efficiency and break-even path documented (2026 investor priority)" 甚至带上了 2026 年投资人关注点的时间感——这是优点，但也与 8.3 的日期戳问题同源：时间敏感表述需要维护。

---

## 9. 可执行性

### 9.1 执行链路分析

本技能无脚本、无外部命令依赖，执行完全由 agent 完成，链路为：识别请求（description）→ 强制 WebSearch（Trend Awareness Protocol 第 329 行）→ 按 Quick Reference/五步流程产出预测 → 按 SCORING 16 条标准被测评。这条链路上有两个关键点：

其一，WebSearch 是硬性前提。Trend Awareness Protocol 第 329 行用 "**IMPORTANT**: ... you MUST use WebSearch" 和 "Web Search Safety (REQUIRED)" 双层强调，SCORING 的 SCOPE-02（脚本判定）与 CF-01（致命失败）双重把关（见第 10 节）。这条强制条款与工具日志判定（checker 的 tool_log_contains 对日志 JSON 全文执行 re.search，模式 `"WebSearch"` 与工具调用记录 `"tool": "WebSearch"` 的序列化字符串匹配）实测语义正确，判定链路可用。需要留意的边界是：若测试环境将 WebSearch 工具改名或 agent 换用 WebFetch 完成搜索，SCOPE-02 会误判为未执行——严格说这是测评设计对工具名的硬编码依赖（见第 10 节），在当前 harness 下成立。

其二，data/sources.json 死链是唯一的执行级故障点。若 agent 遵循 Navigation 的指引去读取数据源文件，会得到"文件不存在"错误；幸好 body 其他部分（Signal vs Noise Framework 三张表）自包含信号来源信息，一个谨慎的 agent 会从表格自行检索数据源而不依赖该文件，但"跟着导航走"的 agent 会白跑一趟。修复见第 13 节 🔴 第 2 条。

### 9.2 测评链可执行性（实测）

- check.py 通过 `python -m py_compile` 编译，无语法错误；
- `sys.path` 插入点 `complex-skills/_shared` 实测存在，checker 库的 tool_log_contains/set_tool_log_path/set_agent_output 均可导入；
- SCORING 的 16 条标准中仅 SCOPE-02 走脚本判定，其余 15 条走 llm 判定——llm 判定条目占比 93.75%，是本语料中 llm 依赖度最高的技能之一（对比 291 号技能 17 条中 4 条脚本判定）。这意味着测评结果对 llm 判定器的稳定性与判定问题的可操作性高度敏感，见第 10 节对判定问题的逐条评估；
- check.py 第 22 行向 set_agent_output 传入路径字符串的问题（见 6.2）对当前 1 条脚本判定无影响，但属于待清理的维护性债。

### 9.3 环境与前置条件

技能执行仅依赖 WebSearch 工具与网络环境，无 bash/平台依赖，跨 harness 可移植性高于脚本类技能。未声明 allowed-tools 意味着 WebSearch 的可用性完全依赖 harness 默认权限；在权限受限环境（如未授权 WebSearch）下，agent 将无法满足 SCOPE-02/CF-01 的硬性要求，建议在 frontmatter 声明 `allowed-tools: WebSearch` 以显式化该依赖（见第 13 节 🟢 第 11 条）。

---

## 10. SCORING 交叉参考

SCORING.yaml 的 16 条标准与技能内容逐条对照如下：

**Scope（3 条）**：SCOPE-01（识别趋势预测/入场时机请求）与 description 的 "Predict market/tech/business-model trends and market-entry timing (enter/wait/avoid)" 逐字对应，llm 判定问题具体、证据指向 "Agent's first response"，可测性好。SCOPE-02（必须执行 WebSearch）对应 Trend Awareness Protocol 第 329 行，走脚本判定，与 check.py 第 27 行一致，是本技能唯一一条确定性判定。SCOPE-03（搜索结果视为不可信输入、只提取事实/日期/引用、关键主张 2+ 独立来源三角验证）对应 Web Search Safety 第 333-337 行，四要素（untrusted/prompt injection/primary sources/triangulate 2+ sources）在判定问题中完整复现，互文质量高。

**Process（7 条）**：PROC-01（先定义 enter/wait/avoid 决策、horizon、buyer、market）对应 Quick Reference 第 1 步（第 18-22 行），判定问题与该步四要素逐字吻合；PROC-02（3+ 独立信号、至少 1 个一手来源、领先/滞后分离）对应 Quick Reference 第 2 步信号表 + Web Search Safety 的 primary sources 条款，双支撑；PROC-03（证伪标准 + 5-10 个参考类比基准率 + p10/p50/p90 + 采用约束）对应 Step 3 的 Reference Class Forecast（第 197-209 行）与 Quick Reference 第 3 步，是 16 条中判定门槛最高的一条——"5-10 个类比 + 基准率 + p10/p50/p90"对单次测评对话而言是重负（见下文总评）；PROC-04（自底向上容量测算 + 显式假设 + 自顶向下交叉验证）对应 Quick Reference 第 4 步（第 40-43 行）与 What Good Looks Like 第 325 行（"both bottom-up and top-down calculations cross-checked"），互文精确；PROC-05（Rogers 位置判定 + 策略含义）对应 Position Identification 表（第 79-85 行），五段名称在判定问题中逐字列出；PROC-06（预测含 thesis/confidence/timing/3-5 证据/反证）对应 Step 4 模板（第 213-221 行），五字段与模板字段一一对应，是映射最严丝合缝的一条；PROC-07（季度复核节奏 + what-changed + 准确率追踪）对应 Key Principles 的 Update Predictions（第 293-299 行），"Revisit quarterly/Track accuracy/Document what changed" 与判定问题逐条对应。

**Output（3 条）**：OUT-01（报告当前状态/轨迹/时机窗口/证据质量）对应 What to Report 四要素（第 346-353 行），判定问题与四要素逐字吻合；OUT-02（机会表：时机窗口/竞争/动作）对应 Step 5 表格（第 225-228 行）三列，映射完整；OUT-03（显式假设 + 敏感性区间 + 证伪标准）对应 What Good Looks Like 第 321 行（"TAM/SAM/SOM with assumptions + sensitivity ranges; falsification criteria documented"），互文精确。

**Negative（2 条）**：NEG-01（不得基于单一信号外推、不得把注意力当采用）对应 Noise Filters（第 157-163 行）与 Do/Avoid 第 313 行（"Extrapolating from a single platform, influencer, or funding headline"），且判定问题中 "treating media attention as adoption" 与 Do/Avoid 第 314 行 "Treating 'attention' as 'adoption'" 逐字互文；NEG-02（不得无假设、无自底向上地做容量测算）对应 Do/Avoid 第 315 行。负向标准采用 "Does the agent avoid ..." 的判定句式，适合 llm 判定。

**QA（1 条）**：QA-01（关键定量主张带日期与来源、无未标日期的主张）对应 Web Search Safety 第 336 行（"Capture dates/versions for quantitative claims; avoid undated trend claims"），互文精确，判定问题可操作。

**Critical Failures（3 条）**：CF-01（未做任何 WebSearch → 0 分）与 SCOPE-02 语义完全重叠——SCOPE-02 是确定性脚本判定，CF-01 是 llm 复核，构成"双重闸门"：工具日志层面未搜索即 SCOPE-02 失败，同时 llm 层面复核结论仍会触发 CF-01 归零。这种重叠在 CF 设计语义下是合理的（致命失败独立于常规标准存在），但建议在 SCORING 注释中写明二者关系，避免维护者误以为冗余。CF-02（单一信号/纯炒作外推无三角验证 → 0 分）对应 NEG-01 的加重版，惩罚梯度合理。CF-03（无明确 enter/wait/avoid 决策、只有趋势闲聊 → 0 分）对应 PROC-01 的加重版，对"只会复述趋势不会做决策"的 agent 形成有效拦截，是三条 CF 中设计最好的一条。

**总评**：本技能是"标准-内容"映射密度的范本级——16 条标准几乎每一条都能在 body 中找到逐字级原文支撑，且多数判定问题把技能原文的要素直接搬进问题文本（PROC-05 的五段名、OUT-01 的四要素、NEG-01 的引号短语），极大降低了 llm 判定的歧义空间。主要扣分点有三：其一，llm 判定占比 93.75%，其中 PROC-03 的"5-10 个参考类比 + 基准率 + p10/p50/p90"在单次测评对话中是异常沉重的负担，agent 即使按技能执行也常只能给出 3-4 个类比，判定问题应允许"类比数量不足时按过程质量给分"或明确 5-10 为理想值；其二，SCOPE-02 硬编码工具名 "WebSearch"，对换用其他搜索工具的 harness 不兼容；其三，CF-01 与 SCOPE-02 的双重闸门应在注释中显式化。整体测评设计质量：良好偏优。

---

## 11. 已知问题

（按任务要求本节跳过。本审计发现的全部问题已并入第 3、4、5、6、8、9、10 节及第 13 节修复建议，不单独列章。）

---

## 12. 综合评分（8 维 → /100）

按 8 个维度评分（各维 10 分制，权重合计 100%）：

1. **规范合规性（权重 15%，得分 8.5）**：12 项清单 10 项通过、1 项边界（Output Format 未统一）、1 项不通过（Scope/Limitations 缺失）。description 合规是全场零瑕疵水准（272 字符、三要素、合规触发句式），失分集中在 body 结构缺项。
2. **内容质量（权重 15%，得分 7.0）**：方法论骨架扎实——Bass 公式、Rogers 五段、Gartner 五阶段、三库循环模式、14 信号分层框架、Reference Class Forecast、ROI 时机模型，都是具体、可执行、有行业依据的内容，在"趋势预测"类技能中属于第一梯队。但 Bass "Time to 50%" 列三处数学错误（实测复算 4.5/8.9/17.7 对声称的 3/5/8 年）、两组 p/q 参数表冲突，使"教 agent 做定量预测"的内容出现了定量错误，摊薄了整体。
3. **结构组织（权重 10%，得分 7.5）**：章节顺序清晰、表格密度高、Quick Reference 入口设计得当；扣分来自空标题、两个空表、死链、三块带日期戳的重复"最佳实践"段落、占位符语法不统一。
4. **逻辑一致性（权重 15%，得分 5.8）**：Bass 数学错误三连、参数表冲突、5 个跨技能引用 4 个不存在、sources.json 死链、日期戳版本混乱、"Very High" 域外值。作为对照，ROI 算例复算正确、Rogers/Gartner 口径正确、流程参数三处自洽，说明作者"会算的部分算对了、没算的部分错了"——教训是教学型内容必须全量复算。
5. **可执行性（权重 15%，得分 7.5）**：无脚本依赖、纯 agent 执行链路畅通，WebSearch 强制条款与工具日志判定（实测语义正确）形成确定性闭环；死链是唯一执行级故障点；93.75% 的 llm 判定占比使测评结果依赖判定器质量（见第 10 节）。
6. **人机感（权重 10%，得分 7.5）**：文风亲切、行为契约明确（Do/Avoid、What Good Looks Like）、术语与受众匹配；空壳小节与日期戳焦虑是主要扣分项。
7. **参考文件质量（权重 10%，得分 4.5）**：零参考文件 + 导航指向虚空的组合是全场最低分维度。主文件自包含缓解了实质损失，但 Resources/Templates 空表与 sources.json 死链说明"设计过、没交付"。
8. **测评可测性（权重 10%，得分 8.0）**：16 条标准全部有原文逐字支撑，判定问题普遍把技能原文要素直接嵌入问题，llm 判定歧义空间小；SCOPE-02 与 check.py 一致、CF 梯度合理。扣分：PROC-03 判定门槛过重、SCOPE-02 工具名硬编码、CF-01 与 SCOPE-02 重叠未注释。

加权合计：0.15×8.5 + 0.15×7.0 + 0.10×7.5 + 0.15×5.8 + 0.15×7.5 + 0.10×7.5 + 0.10×4.5 + 0.10×8.0 = 1.275 + 1.050 + 0.750 + 0.870 + 1.125 + 0.750 + 0.450 + 0.800 = 7.07。

**综合评分：71 / 100（需修复后可用）**。技能的 description 合规、SCORING 设计与方法论骨架达到优秀水平，但被三类问题拖累：一组教学级数学错误（Bass 时间列）、一处索引指向虚空的死链与两个空表、以及 Scope/Limitations 结构性缺项。修复第 13 节的 🔴 与 🟡 项后预计可到 80-84 分区间。

---

## 13. 修复建议

### 🔴 严重（影响可用性/正确性）

1. **修正 Bass 模型 "Time to 50%" 列并合并两组 p/q 参数**——`SKILL.md` 第 71-75 行场景表：按公式 F(t)=0.5 ⇒ t = ln(2+q/p)/(p+q) 复算，三行声称值全部错误（Viral consumer 0.05/0.5 → 应为 4.5 年而非 ~3 年；B2B SaaS 0.02/0.3 → 8.9 年而非 ~5 年；Enterprise 0.01/0.15 → 17.7 年而非 ~8 年）。同时将第 65-68 行 "Typical values" 与第 71-75 行场景表合并为一张表（类别 / p / q / t50 计算值 / 备注），消除 Consumer products (0.03,0.38) 对 Viral consumer (0.05,0.5)、B2B software (0.01,0.25) 对 B2B SaaS (0.02,0.3)、Enterprise tech (0.005,0.15) 对 Enterprise (0.01,0.15) 三组近似同名参数冲突；Enterprise 参数（p=0.005, q=0.15 → t50 22.4 年）与常识偏差过大，一并重审。工作量：S。

2. **修复 sources.json 死链与两个空表**——`SKILL.md` 第 245-249 行 Data 表：二选一——(a) 创建 `data/sources.json`，按第 249 行自我描述（Trend data sources: analyst reports, market data, filings）和第 131-155 行三张信号表的 14 个数据源（VC 投资数据、M&A 监控、LinkedIn/Indeed 职位、GitHub、Gartner/Forrester、Algolia、Reddit、ProductHunt、TechCrunch/Wired 等）结构化落盘；(b) 若暂不创建，删除该行并同步删除第 234-243 行 Resources (Deep Dives) 与 Templates (Outputs) 两个空表。建议取 (a)，因为数据源清单是本技能最该外置的参考资产。工作量：M（方案 a）或 S（方案 b）。

3. **补齐 Scope/Limitations 章节**——`SKILL.md`：在 Trend Awareness Protocol 前（或 Do/Avoid 附近）新增一节，至少写明：不替代财务建模/竞品尽调/投资决策；硬性依赖 WebSearch 与网络（离线不可用）；无信号数据的虚构题材可降级为定性判断；avoid 是合法结论而非失败。这是 12 项合规清单中唯一明确失分项，修复即合规达标。工作量：S。

### 🟡 中等（影响质量/一致性）

4. **统一 Output Format 契约**——`SKILL.md`：新增 "## Output Format" 小节，把 Step 4 预测模板（第 213-221 行）、What to Report 四要素（第 346-353 行）、Step 5 机会表（第 225-228 行）合并为一份完整交付物结构（预测模板 + 现状/轨迹/时机/证据质量 + 机会表 + 假设与敏感性区间 + 证伪标准），并注明各要素在 SCORING 中对应的标准。工作量：S。

5. **填补或删除空标题 "Rogers Diffusion Model"**——`SKILL.md` 第 49 行：要么给一段简要内容（Rogers 扩散的 S 曲线属性与五段划分的出处），要么删除标题并让 Position Identification（第 77-85 行）直接承接。工作量：S。

6. **清理日期戳与重复内容**——`SKILL.md`：删除第 10-14 行 "Modern Best Practices (Jan 2026)" 与 Quick Reference/Do/Avoid/Web Search Safety 的重复条目（三角验证出现至少 4 次、领先/滞后指标出现 3 次、采用约束出现 3 次），将 "Do / Avoid (Dec 2025)" 的日期戳移除，保留单一权威表述；若需保留版本信息，统一为 body 末尾一个 `## Metadata` 小节。工作量：S-M。

7. **修复 Integration Points 的 4 个不存在技能引用**——`SKILL.md` 第 366-377 行：`router-startup`、`product-management`、`startup-review-mining`、`startup-competitive-analysis` 在 complex-skills 与 complex-skills-no-trigger 两个语料集中均不存在（实测检索），仅 `startup-idea-validation`（297）存在。逐一替换为实际存在的技能名（如 105-product-manager-toolkit、254-product-marketing、256-competitive-landscape、065-startup-analyst 等候选），或删除无法落地的条目。工作量：S。

8. **统一占位符语法**——`SKILL.md`：把 Step 1 模板（第 172-176 行）与 Reference Class Forecast 表（第 205-209 行）的方括号占位统一为双花括号（如 {{DOMAIN}}、{{MILESTONE}}），与 Quick Reference/Step 2/Step 5 一致；把 {{NOW}}（第 186 行）改为 {{CURRENT_YEAR}} 消除歧义。工作量：S。

9. **修正 "Very High" 域外值**——`SKILL.md` 第 137 行：Strong Signals 表的 Weight 列取值域为 High/Medium/Low，"Very High" 应改为 "High" 或把三层信号统一改为含 Very High 的量纲。工作量：S（顺手项）。

### 🟢 轻微（体验/健壮性增强）

10. **ROI 示例措辞防混**——`SKILL.md` 第 282-283 行：bullet 的 "Early: $100 CAC" 指的是 Early Majority，与第 274 行表中 "Early (Innovators) 0.5x" 的 "Early" 指代不同对象，建议改为 "Early Majority: $100 CAC" 与 "Late Majority: $250 CAC"。工作量：S。

11. **frontmatter 声明 allowed-tools**——`SKILL.md` frontmatter：追加 `allowed-tools: WebSearch`，显式化 Trend Awareness Protocol 的强制工具依赖，避免权限受限环境下的执行短路。工作量：S。

12. **Required Searches 年份动态化**——`SKILL.md` 第 339-344 行：把硬编码的 "2026" 改为 "current year"（如 `"[technology/market] trends {current year}"`），消除 2027 年后的系统性过时。工作量：S。

13. **SCORING 注释 CF-01 与 SCOPE-02 的关系**——`SCORING.yaml` 第 139-142 行：在 CF-01 的 description 或注释中写明"与 SCOPE-02 构成双重闸门：工具日志层面已由脚本判定拦截，此处为 llm 复核"，防止维护者误删其一。工作量：S。

14. **SCORING PROC-03 放宽类比数量门槛**——`SCORING.yaml` 第 48-54 行：判定问题明确"5-10 个类比为理想值，3 个以上且过程完整（基准率、概率区间、调整因素）可给部分分"，避免单次测评对话中 agent 因无法凑足类比数而被整体判负。工作量：S。

15. **check.py 清理**——`check.py` 第 22 行：删除 check() 内 `set_agent_output(agent_output)`（传入的是路径非内容，功能恒空），只保留 main() 第 53-55 行的内容读取，避免误导维护者；同步在 docstring 注明 workspace 参数为预留。工作量：S。

---

## 附录 A：文件清单与行数

| 文件 | 行数 | 状态 |
|------|------|------|
| SKILL.md | 377 | 主体；Bass 数学错误、死链、空壳小节、缺 Scope/Limitations |
| SCORING.yaml | 150 | 16 条标准 + 3 CF，解析通过，映射密度高 |
| check.py | 64 | 1 条判定，编译通过，1 处冗余调用 |

（本技能无 references/、scripts/、data/ 子目录；SKILL.md 第 249 行引用的 data/sources.json 不存在。）

## 附录 B：实证验证记录

1. `python -m py_compile check.py` → 通过；`sys.path` 目标 `complex-skills/_shared/checker.py` 实测存在，tool_log_contains/set_agent_output 可导入。
2. PyYAML 解析 SKILL.md frontmatter → 仅 name/description 两键，description 长度 272 字符；解析 SCORING.yaml → 16 条标准（scope 3 + process 7 + output 3 + negative 2 + qa 1）+ 3 条 CF，与 total_items: 16 一致。
3. Bass 复算：t = ln(2+q/p)/(p+q) → Viral consumer 4.5 年（表称 ~3）、B2B SaaS 8.9 年（表称 ~5）、Enterprise 17.7 年（表称 ~8）；Typical values 表对应值 6.6/12.7/22.4 年。
4. ROI 算例复算：(100/100)×0.15 = 0.15、(100/250)×0.05 = 0.02、比值 7.5 → 与文档一致。
5. 跨技能引用检索：`startup-idea-validation` 存在（297）；`router-startup`、`product-management`、`startup-review-mining`、`startup-competitive-analysis` 在 complex-skills 与 complex-skills-no-trigger 两个语料集中均不存在。
6. `data/` 目录不存在（ls 实测），确认 data/sources.json 为死链。

## 附录 C：方法说明

- 本技能目录 3 个文件全部全文精读，无抽样；`_shared/SKILL-SPEC.md` 与 `_shared/checker.py` 全文精读作为审计基准。
- 评分口径：8 维加权（规范 15% / 内容 15% / 结构 10% / 逻辑 15% / 可执行 15% / 人机感 10% / 参考文件 10% / 测评 10%），与既有技能档案的审计口径保持一致。
- 严重度分级：🔴 影响技能可用性或产生错误结果；🟡 影响质量与一致性；🟢 体验与健壮性增强。
- 行号以本审计时文件为准；修复后行号可能位移。
