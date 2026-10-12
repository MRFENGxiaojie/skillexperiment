# REVIEW: 219-transaction-trace-analysis

- **审查日期**: 2026-08-06
- **审查对象**: `D:\SkillIF\skill-experiment\complex-skills\219-transaction-trace-analysis\`
- **审查范围**: 目录下全部 10 个文件（SKILL.md、SCORING.yaml、check.py、references/ 下 7 个参考文件），全部逐行通读
- **参照标准**: `_shared/SKILL-SPEC.md` v1.0（规范合规）、`_shared/checker.py` 库接口（脚本校验一致性）
- **参考档案**: 项目 memory `skill-dossier.md`（2026-08-05 全语料 322 skill 审查记录）
- **总行数统计**: SKILL.md 69 行 + SCORING.yaml 167 行 + check.py 77 行 + references 404 行 = **717 行**

---

## 1. 目录全量清单

| # | 文件 | 行数 | 类型 | 职责 |
|---|------|:----:|------|------|
| 1 | `SKILL.md` | 69 | 主文件 | 技能入口：导航表、双 Ledger 构建、6 步工作流、常见陷阱 |
| 2 | `SCORING.yaml` | 167 | 评估规范 | 18 项 criteria（scope 3 / process 5 / format 3 / technical 3 / negative 2 / qa 2）+ 3 项 critical_failures |
| 3 | `check.py` | 77 | 评测脚本 | 脚本可查项执行（实际只查 SCOPE-02 与 FMT-02 两项），其余 16 项委托 LLM judge |
| 4 | `references/trace-schema-normalization.md` | 61 | 参考 | 列名规范化 → 数据字典 → 健全性检查 |
| 5 | `references/transaction-history-reconstruction.md` | 41 | 参考 | 按事务分组重建行为；区分逻辑事务与 attempt；处理残缺记录 |
| 6 | `references/object-version-history.md` | 46 | 参考 | 按对象/键重建版本时间线；版本区间 `[w, n)`；写记录交叉核对 |
| 7 | `references/timestamp-and-ordering-fields.md` | 40 | 参考 | 逻辑时间/物理时间/行序/计数器作用域/版本标识的排序语义 |
| 8 | `references/validation-and-abort-records.md` | 82 | 参考 | 失败谓词交付物；保守校验；"必要中止 vs 保守中止 vs 未知"决策树 |
| 9 | `references/evidence-quality-and-uncertainty.md` | 51 | 参考 | 证据分级（直接/派生/假设/无支撑）；防过度声明；缺失数据提问清单 |
| 10 | `references/output-classification-patterns.md` | 83 | 参考 | 内部分类记录 vs 外部输出投影；去重；ID-only JSON 模式；最终健全性检查 |

**观察**:
- 目录结构与引用关系完全闭合：SKILL.md 的 Quick Reference 表列出的 7 个 references 文件全部存在，文件名与表格逐字对应。
- 无 scripts/ 目录、无其他资源文件；不引用任何跨 skill 路径；不引用任何本目录之外的文件。
- `check.py` 顶部 `sys.path.insert` 指向 `../_shared`，实测 `_shared/checker.py` 与 `CHECKER-LIBRARY.md`、`SKILL-SPEC.md` 均存在，依赖可解析。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 值: `transaction-trace-analysis`
- 规则: 小写字母 + 连字符，≤64 字符，必须与目录名一致。
- 判定: 与目录 `219-transaction-trace-analysis` 完全一致，**通过**。

### 2.2 description（逐句分析）

原始文本（SKILL.md L2-3）:

> Teaches evidence-based analysis of transaction logs and traces. Use when reconstructing transaction behavior from tables, TSV/CSV files, timestamps, counters, object histories, validation records, abort records, retries, partial logs, or when producing classified transaction outputs from trace evidence.

逐句拆解:

| 片段 | 功能 | 合规性 |
|------|------|--------|
| "Teaches evidence-based analysis of transaction logs and traces." | **WHAT** — 第三人称陈述技能职能 | ✅ 第三人称，非祈使 |
| "Use when reconstructing transaction behavior from tables, TSV/CSV files, timestamps, counters, object histories, validation records, abort records, retries, partial logs" | **WHEN + KEYWORDS** — 触发场景枚举 | ⚠️ 见下方触发信号讨论 |
| "or when producing classified transaction outputs from trace evidence." | **WHEN（输出侧）** — 覆盖"分类输出"场景 | ✅ 与 FMT-01/02 三判定输出要求呼应 |

- 长度约 273 字符，远低于 1024 上限，**通过**。
- 无跨技能路由、无 "NOT for X, use Y" 句式、无语义空泛（非 "A useful skill"），**通过**。
- **触发信号判定（有争议点）**: SKILL-SPEC §2.4 要求至少出现下列信号之一: `"Use when the user..."`、`"Use when the user asks to..."`、`"Use when the user needs to..."`、`"Triggers on..."`、`"Use for..."`。本 description 使用 **"Use when reconstructing..."**（"Use when" + 动名词），属于规范列举模板之外的变体。语义上与 "Use when the user asks to reconstruct..." 等价，触发意图明确、可匹配度高，但字面不在模板清单内。参考项目 memory 中 [Trigger 设计决策] 的讨论（触发时机描述的取舍），此类动名词变体是语料中常见的第二档写法。**判定为: 轻微偏差，建议按模板补 "the user" 主语，但不构成硬违规。**
- 关键词覆盖: tables / TSV/CSV / timestamps / counters / object histories / validation / abort / retries / partial logs — 与 references 的七个主题一一对应，无失配关键词。

### 2.3 其他 frontmatter 字段

- 本 skill 只有 `name` 与 `description` 两个字段，未使用 `allowed-tools`、`argument-hint` 等可选字段。
- 可选字段缺失不违规（SKILL-SPEC §1.2 为 allowed list）。
- 无任何禁用字段（§1.3 清单逐项核对: 无 metadata/license/version/triggers/use-cases 等），**通过**。

### 2.4 Frontmatter 语法

- YAML 结构合法: `name:` 与 `description:` 缩进一致，description 为单行双引号包裹字符串，无截断、无尾部逗号、无未闭合引号。
- 与语料中 🔴 级问题（如 047/314 的 description 截断）对照，本文件 YAML 干净。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行号 | 段落 | 性质 |
|------|------|------|
| L6 | `# Transaction Trace Analysis`（H1） | 标题 |
| L8 | "Use this skill when the task provides concrete logs, tables, counters, timestamps, or partial records and asks you to infer transaction behavior." | 触发重述（body 内，允许祈使） |
| L10 | "This skill is about *reconstruction under partial evidence*:" | 核心定位 |
| L12-15 | 4 条要点（normalize / reconstruct per-txn + per-key / join by explicit fields / produce minimal auditable classification） | 原则声明 |
| L17 | `## Quick Reference (pick the next file to read)` | 导航表 |
| L18-28 | 7 行路由表（需求 → 参考文件） | 导航 |
| L29 | `## Trace Ledger (what you build first)` | 方法论 |
| L31 | "Build two tiny ledgers before doing any deep inference:" | 方法论 |
| L33-43 | 交易账本伪代码（txn_id → seen_keys / read-evidence / write-evidence / validation-abort-evidence / candidate_commit_fields） | 方法论 |
| L44-52 | 对象账本伪代码（key → timeline，含 event / txn_id / version_fields / counter_fields） | 方法论 |
| L54 | "Only after both exist should you attempt joins..." | 执行顺序门禁 |
| L56 | `## Workflow (operational)` | **工作流节** |
| L58-63 | 6 步工作流（Schema normalization → Per-txn reconstruction → Per-key reconstruction → Decision modeling → Classification → Output） | 工作流 |
| L65 | `## Common Pitfalls` | 反模式 |
| L67-69 | 3 条陷阱（per-key counter 当全局序 / 行序当时间序 / 无证据宣称 unnecessary） | 反模式 |

### 3.2 必需章节检查（对照 SKILL-SPEC §3.1）

| 必需章节 | 是否存在 | 证据 | 判定 |
|----------|:------:|------|------|
| **Workflow / Process** | ✅ | `## Workflow (operational)`（L56-63），6 步编号流程 | 通过 |
| **Output Format** | ❌ | 无独立输出节；仅工作流第 6 步一句 "dedupe ids, sort if required, write exact format"（L63），详细输出规范全部下沉到 `output-classification-patterns.md` | **缺失（主要缺口之一）** |
| **Scope / Limitations** | ❌ | 无独立 Scope 节；`## Common Pitfalls` 只覆盖"不该做什么"中的 3 个技术反模式，未回答"何时不应使用本 skill"（如: 无日志证据的纯代码审查、行数巨大的流式日志是否需要抽样、与 222 之类相邻技能的分工） | **缺失（主要缺口之一）** |

- 该缺口与全语料统计高度吻合（skill-dossier: ~68% 的 skill 缺 Scope 节，~56% 缺 Output Format 节），219 属于最常见的那一类结构缺口。
- 缓解因素: 输出格式虽然无专节，但 `output-classification-patterns.md` 提供了完整的"内部记录 vs 外部投影"、"ID-only JSON"、"排序与格式"、"最终健全性检查"四层规范，且 Quick Reference 表将"Emitting deduped/sorted ids and minimal justifications"路由到该文件——**功能上覆盖了 Output Format，结构上未显式声明**。Scope 则完全没有等价替代物。

### 3.3 内容委托分析

- Body 69 行，其中约 40 行为导航与方法论骨架，具体推理规则 404 行全部在 references/。这是典型的 **hub-and-spoke** 结构。
- 委托评估: 每个参考文件都有 Quick Reference 表入口，路由条件以"需求"（need）而非以"数据类型"定义，符合 SKILL-SPEC §3.4 决策表优于散文的要求。
- 与语料中 🟠 级"空壳型" skill（032/045/317/320）的差异: 那些 skill 的 body 没有可执行骨架、核心步骤全部外推；本 skill 的 body 有真实的工作流步骤、双账本伪代码和前置门禁（"build ledgers FIRST"），**委托是结构性的而非逃避性的**。委托质量合格。

### 3.4 节编号/标题层级

- 层级: H1（1 个）→ H2（4 个: Quick Reference / Trace Ledger / Workflow / Common Pitfalls）。无 H3。无编号错乱、无跳跃（对比语料中 2.5→4 类问题）。
- 标题命名均为英文动词短语，风格统一；无 "New!" 等脚手架标记。
- 表格列头 "If you need… / Read" 语义清晰；7 行表格无重复行。

### 3.5 Body 长度合规

- Body 69 行（含 frontmatter 5 行），远低于 process 模式目标 ~200 行与硬上限 600 行。
- **判定**: 数量上合规；但从 process 模式的可执行性看偏薄——若将 output 节与 scope 节补上并追加一个微型工作示例（见 §9、§13），body 约 120-150 行为宜。当前 69 行不是违规，是"偏瘦的合规"。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

6 步工作流与 references 及 SCORING 的映射（全闭合）:

| 工作流步骤 | 对应参考文件 | 对应 SCORING |
|-----------|-------------|--------------|
| 1. Schema normalization（L58） | trace-schema-normalization.md | PROC-02 |
| 2. Per-txn reconstruction（L59） | transaction-history-reconstruction.md | PROC-03 |
| 3. Per-key reconstruction（L60） | object-version-history.md | PROC-04 |
| 4. Decision modeling（L61） | timestamp-and-ordering-fields.md | PROC-05 |
| 5. Classification（L62） | validation-and-abort-records.md + evidence-quality-and-uncertainty.md | FMT-01, TEC-02, TEC-03 |
| 6. Output（L63） | output-classification-patterns.md | FMT-02, QA-02 |

- 步骤 2 与步骤 3 的顺序（先按事务、后按键）与 L54 的"两个账本都建好后才能做 join 类推断"完全一致；SCORING PROC-01 的"Trace Ledger built FIRST"与 L31 "Build two tiny ledgers before doing any deep inference"逐字呼应。
- 步骤 4 "re-express the protocol's decision rule in terms of trace fields" 是步骤 5 分类的输入；validation-and-abort-records.md 的"failed predicate"交付物（`txn T aborted because predicate P(trace_fields) was false`）正是步骤 4 的输出形式。衔接无断裂。
- **衔接上的一个隐含前提**: 步骤 4 假定任务中"协议"已知（如时间戳认证协议、read-validate-write 协议）。若任务只给日志而无协议说明，步骤 4 缺乏降级路径；evidence-quality-and-uncertainty.md 的"缺失数据问题清单"部分弥补了这一缺口（第 5 问 "can row order be trusted?"、第 6 问 "are all shards included?"），但 body 未显式指示"协议未知时跳到证据质量清单"。属轻微的可操作性断层。

### 4.2 内部矛盾扫描

| 位置 | 检查 | 结论 |
|------|------|------|
| L14 "join them through explicit fields (not through row order guesses)" vs L68 陷阱 2 "Using file row order as time order without justification" | 前后一致 | ✅ 无矛盾 |
| L31 "Build two tiny ledgers **before**" vs L54 "**Only after both exist** should you attempt joins" | 同一门禁的两次表述，语义严格一致 | ✅ 无矛盾 |
| L67 陷阱 1 "Treating per-key counters as global order" vs timestamp-and-ordering-fields.md "A per-object counter cannot order events on different objects" vs SCORING TEC-01/NEG-01 | 三处完全同构 | ✅ 无矛盾 |
| L69 陷阱 3 "Calling something 'unnecessary' without exhibiting a safe order" vs validation-and-abort-records.md 决策树第 1 步 "Can you exhibit a safe order?" | 决策树的否定形式即陷阱表述 | ✅ 无矛盾 |
| L12 "normalize columns into a stable event vocabulary" vs trace-schema-normalization.md 全篇 | 主题一致 | ✅ 无矛盾 |
| body 说输出 "minimal, auditable classification"（L15）vs output-classification-patterns.md "internal record 保留 reason/confidence，外部只投影所需字段" | 一致：minimal 指外部投影，auditable 指内部记录 | ✅ 无矛盾（且参考文件把这一区分讲透了） |

- 结论: **全文未发现任何实质性逻辑矛盾**。与语料中 🔴 级矛盾（如 208 规则与示例打架、268 +3/+5 不一致、153 描述与正文冲突）对照，219 的一致性属于上乘。

### 4.3 示例/伪代码正确性

- 交易账本伪代码（L35-43）与对象账本伪代码（L45-52）为 `text` 代码块内的示意结构，非可执行代码；字段命名（seen_keys / read-evidence / write-evidence / candidate_commit_fields / version_fields / counter_fields）与 references 中使用的术语（observed_version_fields / installed_version_fields）一致。
- object-version-history.md 的版本区间 `[w, n)`（L25）为数学上正确的半开区间：版本在写时间 w 生效、被下一次写时间 n 取代、候选有效区间 [w, n)。无数值/公式错误。
- validation-and-abort-records.md 的谓词示例 `current_wts(key) != local_wts(key) and commit_ts > local_rts(key)`（L15）——时间戳认证协议的标准校验表达式，语义正确（比较对象不同域但同为该协议内时间戳域）。
- 唯一可挑剔处: 全文没有任何"输入样本 → 账本 → 判定"的完整走查示例（见 §9），属示例缺失而非示例错误。

### 4.4 条件完整性

- 决策树（validation-and-abort-records.md L64-72）三分支完备: 能展示安全序 → 保守中止；不能展示安全序但可证不可能 → 必要中止；其余 → unknown。覆盖了所有可判定结果。
- 判定输出三分词（must abort / could commit / unknown from evidence）与决策树三分支一一对应，SCORING FMT-01 的三种判决词与决策树无未覆盖情形。
- "How to exhibit a safe order"（L74-82）给了三条最小证据路径（version-interval / ordering / protocol-specific extension），为"could commit"设置了取证门槛，条件完整。
- 缺失数据问题清单（evidence-quality-and-uncertainty.md L32-40）6 问覆盖读记录缺失、校验记录缺失、时间戳更新缺失、计数器作用域、行序可信度、分片完整性——对"trace 不完整"的边界条件枚举充分。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| SKILL.md 引用（Quick Reference 表 + 正文） | 目标文件 | 存在 | 标题一致 |
|--------------------------------------------|----------|:----:|:--------:|
| trace-schema-normalization.md | `references/trace-schema-normalization.md` | ✅ | ✅ |
| transaction-history-reconstruction.md | `references/transaction-history-reconstruction.md` | ✅ | ✅ |
| object-version-history.md | `references/object-version-history.md` | ✅ | ✅ |
| timestamp-and-ordering-fields.md | `references/timestamp-and-ordering-fields.md` | ✅ | ✅ |
| validation-and-abort-records.md | `references/validation-and-abort-records.md` | ✅ | ✅ |
| evidence-quality-and-uncertainty.md | `references/evidence-quality-and-uncertainty.md` | ✅ | ✅ |
| output-classification-patterns.md | `references/output-classification-patterns.md` | ✅ | ✅ |

- **7/7 引用全部命中**，且均为相对路径、不出本目录（符合 SKILL-SPEC §3.3）。对比语料中 195/196 类"引用全部指向错误路径"的 🟠 问题，本 skill 引用卫生状况优秀。

### 5.2 不可见资源审计

- 目录内无未在 SKILL.md/SCORING.yaml 中出现的孤立文件。
- 目录内无 scripts/、无模板、无二进制约定；`check.py` 对 `_shared/checker.py` 的导入路径有效（已验证 `_shared/` 存在 checker.py）。
- **无不可见依赖**。

### 5.3 Reference 文件全文审查

#### 5.3.1 trace-schema-normalization.md（61 行）

- 交付物定义清晰：数据字典（source column → normalized meaning → scope → ordering semantics）直接可执行。
- "Preserve Raw Values"（不覆盖原始字段）与"正常化后再 join"（L17 "Do not start 'joining' until this exists"）两条纪律是防幻觉的关键机制。
- "No Header Assumption"节针对无表头 TSV 的常见坑，给出了可验证的健全性检查（逐键单调、commit-ts 配对、作用域隔离、扇出检查）。
- "When a check fails, do not 'patch' it with assumptions; revisit the dictionary" 是正确的归因纪律。
- **质量: 高**。唯一小遗憾: 未给出一个完整的数据字典示例（SKILL.md L35-43 的账本伪代码部分代偿）。

#### 5.3.2 transaction-history-reconstruction.md（41 行）

- 最短的参考文件之一，但内容聚焦: 逐事务记录收集项 6 类、逻辑事务 vs attempt 的判别问题、残缺记录 4 种解释、约束式重建（constraints safer than storytelling）。
- "constraints ... can be checked against object histories" 与 object-version-history.md 的交叉核对直接联动，两文件间无重复。
- **质量: 中高**。缺点: "用任务的 schema description 决定残缺记录解释"这条指引需要任务本身有 schema 说明，对无说明任务缺乏兜底（可引用 evidence-quality-and-uncertainty.md 的 unknown 兜底，但未交叉引用）。

#### 5.3.3 object-version-history.md（46 行）

- 按对象建时间线的收集项 7 类；"Sort only by fields that truly order the object history" 与 timestamp-and-ordering-fields.md 的作用域纪律呼应。
- 版本区间推导、跨写记录核对 4 条、对象中心四问（读到什么版本 / 校验时有什么新版本 / 旧版本在候选串行点是否仍有效 / trace 是证明无效、证明安全、还是仅缺证明）——四问把"证据强度"问题显式化了。
- **质量: 高**。

#### 5.3.4 timestamp-and-ordering-fields.md（40 行）

- 五种排序字段（逻辑时间/物理时间/行序/计数器/版本标识）逐一定义了"能排什么、不能排什么"。
- "A per-object counter can compare two events on the same object, but it cannot order events on different objects" 是全文最关键的禁令，对应 TEC-01/NEG-01。
- 比较检查表 4 问（同钟源？协议定义？严格/非严格？排序对象？）可直接用作判断前 checklist。
- **质量: 高**。最薄之处是未给出"时钟偏移/批处理使物理时间不可靠"的量化示例，但方向正确即可。

#### 5.3.5 validation-and-abort-records.md（82 行，最实质的参考文件）

- "failed predicate"交付物是本 skill 最有价值的原创设计——把"中止原因"从叙事降格为可检验的谓词，直接防止"把每个中止当真实异常"的常见误读。
- 校验失败类型 5 类、中止原因粒度 3 档（exact / coarse / policy-based），并明确"coarse 原因不得推断精确冲突"。
- 保守校验三要素对比（协议条件失败 / 可用 trace 证据 / 存在合法串行序或时间戳指派）与决策树（necessary vs conservative vs unknown）逻辑严密，是 references 中唯一完整的决策结构。
- "How to exhibit a safe order" 的 3 条最小证据路径把"证明可能提交"的举证责任具体化。
- **质量: 极高**，全语料同主题文件中也属上乘。微小问题: "local_rts" 等缩写无注释，依赖读者协议背景（对专业受众可接受）。

#### 5.3.6 evidence-quality-and-uncertainty.md（51 行）

- 证据四分级（direct / derived / assumed / unsupported claim）是完整的证据强度谱系。
- "Avoid Overclaiming"的 4 个推荐标签（proven safe / proven unsafe / aborted by protocol condition, safety unknown / insufficient evidence）比 SCORING 的三分词多一个"aborted by protocol condition, safety unknown"——**两套词汇并存是评估时需要注意的映射点**（详见 §10.3）。
- 缺失数据 6 问与可复现推理 3 件套（逐事务摘要/逐对象时间线/分类理由）设计到位。
- **质量: 高**。

#### 5.3.7 output-classification-patterns.md（83 行）

- "外部输出是内部分类表的投影"原则 + 分类记录 6 字段（id/label/supporting fields/reason/confidence）→ 补上了 body 缺失的 Output Format 职能。
- ID-only JSON 四步模式（取集合→去重→按需排序→写整数数组）与"不把格式化烘进分类逻辑"的告诫直接服务 FMT-02 这类脚本校验。
- 最终健全性检查（去重前后计数、等值边界、每 id 有证据、每排除 id 有失败条件）与稳定性/等值边界/类型安全三条附加检查，是语料中少见的对"机器校验输出"的完备防护。
- **质量: 高**。唯一缺憾: 未给出一段"输入分类表 → 输出 JSON"的逐行示例（口头描述了流程，未展示成品），若补 3-5 行示例，对 agent 的格式遵从率会明显提升。

---

## 6. 语法与格式质量（逐问题列举）

逐文件扫描结果:

1. **拼写**: 未发现拼写错误（对照语料中 070 "which servers as"、262 葡语混入、307 叠词等典型问题，219 零命中）。
2. **病句/断句**: 未发现残缺句子或悬垂片段（对照 070 末句残缺、297 乱码）。
3. **标点**: 全篇英文标点规范；SKILL.md L18 表格中 "If you need…" 用省略号，风格统一；无全角/半角混排。
4. **中英混杂**: 无（本 skill 为纯英文编写，符合其目标受众）。
5. **Markdown 结构**: 围栏代码块全部闭合；表格 7 行均对齐（Quick Reference 表与审查用表均列数一致）；无 "1." 编号断裂类 tpl 缺陷；无孤立标题层级。
6. **YAML**: SCORING.yaml 缩进一致，`judge: llm|script` 枚举值合法，`pattern:` 均为合法字符串；`description:` 字段内部引号转义正确。
7. **Python**: check.py 语法合法（可通过 `python -m py_compile`）；docstring 与 main 的 argv 约定（3 个位置参数）一致。
8. **术语拼写一致性**: "abort" / "aborted" 统一；"wts" / "rts" / "commit_ts" 缩写全篇一致；"txn_id" / "transaction id" 两种写法并存但在各自语境中含义等价，不构成混淆。
9. **代码块语言标注**: 账本伪代码标注为 `text`（诚实标注，未冒充 Python）；其余均无代码块（references 无代码示例，纯规则文体，与其定位一致）。

**结论: 语法与格式质量 9/9 项零问题。** 这是全语料中语法最干净的一档（与 127/154/164 同级）。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

按 SKILL-SPEC §5 的 12 项 Compliance Checklist 逐条判定:

| # | 检查项 | 结果 | 说明 |
|---|--------|:----:|------|
| 1 | name: 小写+连字符、≤64、与目录一致 | ✅ | `transaction-trace-analysis` = 目录名 |
| 2 | description: 第三人称 + WHAT + WHEN + KEYWORDS、≤1024 | ✅ | 三段结构完整，~273 字符 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | "Teaches..." 第三人称 |
| 4 | description: 无内嵌跨技能路由 | ✅ | 无 "use Y instead" 类句式 |
| 5 | description: 至少一个触发信号短语 | ⚠️ | "Use when reconstructing..." 为 "Use when"+动名词变体，语义成立但不在模板清单内；建议补 "the user" |
| 6 | frontmatter: 无禁用字段 | ✅ | 仅 name + description |
| 7 | body ≤600 行 | ✅ | 69 行 |
| 8 | body 有 workflow/process 节 | ✅ | `## Workflow (operational)` 6 步 |
| 9 | body 有 output format 节 | ❌ | 无独立节；职能由 references/output-classification-patterns.md 代偿 |
| 10 | body 有 scope/limitations 节 | ❌ | 无；Common Pitfalls 只覆盖 3 条技术反模式，未声明"何时不使用" |
| 11 | body 无跨技能文件引用 | ✅ | 仅 references/ 相对路径 |
| 12 | 目录: NNN-kebab-case、无空格大写 | ✅ | `219-transaction-trace-analysis` |

- **合规项 12 中 10 项通过、2 项缺失（Output Format 节、Scope 节）、1 项轻微偏差（触发信号变体）**。
- 与全语料横向对比: 219 的合规成绩属"最常见缺口型"——缺两节的数量与语料 68%/56% 的普遍情况一致，但没有任何 🔴 级硬违规（无截断、无跨技能路径、无空壳、无事实错误），整体合规度位居中上。

---

## 8. 人机感评估

1. **语气**: 专业、克制、确定性的工程语气。全文无一句填充语、无口头禅、无营销腔（对照 083-085 的 "world-class" 自我膨胀、007 的 K-Dense 推销）。
2. **emoji 扫描**: 0 处。正文、表格、代码块均无装饰性 emoji（对照 072 的 20+ 图标、042 的 📄📁）。语料中最干净的一档。
3. **全大写喊话**: 0 处。无 "STOP!" / "DO NOT" / "MANDATORY" 类强命令（对照 072/153）。
4. **称呼与受众**: 正文用 "you"（"Before using `a < b`..."、"If the trace cannot show any of these"），为 agent 指令标准第二人称，无对用户直接说话的双重受众问题（对照 101/115 的受众混淆）。
5. **语气的"人"**: 少量人性化点缀（L31 "Build two **tiny** ledgers"、L17 表格副题 "pick the next file to read"、"storytelling" 这类反例词），尺度恰当——克制但不机械，比纯清单文体更有指导温度。
6. **协作观**: 参考文件明确"保守、宁可 unknown 不过度声明"（evidence-quality-and-uncertainty.md）、"人类可审计"（output-classification-patterns.md 的 reason/confidence 字段）——体现对下游判断者的尊重，与语料中 185/279 类"机器执行、人做裁决"的边界意识同级。

**人机感评级: 🟢 优秀（语料前 10% 档）。**

---

## 9. 可执行性评估

1. **入口清晰度**: Quick Reference 表用"需要什么 → 读哪个文件"路由，7 个需求与 7 个文件一一对应，agent 第一步动作明确（对照 SCOPE-02 的脚本检查，读任一参考文件即得分，门槛合理）。
2. **前置产物**: 双账本（交易账本 + 对象账本）有字段级伪代码，且 L54 明确"账本未齐禁止 join"——这是全文最可执行的指令，直接把 PROC-01 的"FIRST"要求落地为可检查的状态门。
3. **流程闭环**: 6 步工作流从解析到输出全链路覆盖；每一步都有对应的参考文件展开细节；决策树（necessary/conservative/unknown）是可机械执行的判定逻辑。
4. **输出可校验**: ID-only JSON 模式 + 排序/去重/类型安全三条检查，直接面向 FMT-02 类脚本校验场景，落地性强。
5. **执行阻力点**:
   - (a) **无完整工作示例**: 全文没有"一段样本 trace → 数据字典 → 账本 → 判定"的走查。agent 对"账本长什么样"有伪代码参照，但对"判定的推理过程长什么样"只有抽象规则。建议在 body 或 validation-and-abort-records.md 中补一个 8-12 行的小示例（两笔事务、一个键、一次校验失败），可执行性会上一个台阶。
   - (b) **协议未知任务无降级路径**: 步骤 4 依赖协议已知，任务无协议说明时缺显式兜底（见 §4.1）。
   - (c) **判定词表未显式映射**: skill 内部词汇（necessary abort / conservative abort / unknown）与 SCORING 判分词汇（must abort / could commit / unknown from evidence）的对应关系未在任何文件里写出来（详见 §10.3）。agent 若严格照 skill 词汇输出，可能过不了 FMT-02 脚本——这是当前最大的可执行性隐患。
6. **navigation 模式适配度**: body 作为导航枢纽的定位与其 "pattern: process" 的声名匹配；参考文献总量 404 行使整体内容规模（473 行）处于 process 模式合理区间。

**可执行性评级: 🟡 良好但三处可改进（示例缺失、协议降级、词表映射）。**

---

## 10. SCORING.yaml 交叉参考

### 10.1 18 项 criteria ↔ 出处映射表

| ID | 类别 | 检查要点 | 出处（skill/reference） | 对应 |
|----|------|---------|------------------------|------|
| SCOPE-01 | scope | 识别为 trace 重建任务 | description + L8 | — |
| SCOPE-02 | scope | 读取任一参考文件 | Quick Reference 表 | check.py 脚本 |
| SCOPE-03 | scope | 仅凭提供证据工作 | L8 "provides concrete logs..." + evidence-quality | — |
| PROC-01 | process | 双账本先建 | L31/L54 | — |
| PROC-02 | process | 列名与作用域规范化 | 步骤 1 + trace-schema-normalization | — |
| PROC-03 | process | 逐事务重建 + 候选串行化点字段 | 步骤 2 + transaction-history-reconstruction | — |
| PROC-04 | process | 逐键时间线 + 排序依据验证 | 步骤 3 + object-version-history | — |
| PROC-05 | process | 决策规则转写为 trace 字段 | 步骤 4 + validation-and-abort（failed predicate） | — |
| FMT-01 | format | 三判定词之一且证据支撑 | 步骤 5 | — |
| FMT-02 | format | 输出含三分词之一 | 步骤 6 + output-classification-patterns | check.py 脚本 |
| FMT-03 | format | 显式字段 join、非行序猜测 | L14 + L68 | — |
| TEC-01 | technical | 时间戳/计数器作用域正确 | timestamp-and-ordering-fields | — |
| TEC-02 | technical | 校验失败/中止按参考保守解释 | validation-and-abort（保守校验节） | — |
| TEC-03 | technical | 残缺 trace 输出 unknown | evidence-quality（Avoid Overclaiming） | — |
| NEG-01 | negative | 不把 per-key counter 当全局序 | 陷阱 1 + timestamp-and-ordering | — |
| NEG-02 | negative | 不用行序当时间序、不无证据判 unnecessary | 陷阱 2/3 | — |
| QA-01 | qa | 证据不足时显式标注不确定性 | evidence-quality | — |
| QA-02 | qa | 每个判定带最小可追溯理由 | output-classification（reason 字段） | — |

- **18 项全部能在 skill 文本中找到直接出处，无一悬空**；categories 分布（scope 3 / process 5 / format 3 / technical 3 / negative 2 / qa 2）与 pattern: process 的定位吻合；`total_items: 18` 与实际条目数一致。
- 3 项 critical_failures（CF-01 行序 join、CF-02 证据不足却自信判定、CF-03 计数器当全局序）分别对应 NEG-02、QA-01/TEC-03、NEG-01，与 Common Pitfalls 三重对应，设计自洽。

### 10.2 脚本可查项与 check.py 一致性

- SCORING.yaml 中 `judge: script` 的条目为 SCOPE-02 与 FMT-02；check.py 恰好只实现这两项（其余 16 项注释 "llm judge (not checked here)"），**脚本覆盖面与规范声明完全一致**。
- 两处正则逐字一致:
  - SCOPE-02: `trace-schema-normalization|transaction-history-reconstruction|object-version-history|timestamp-and-ordering|validation-and-abort|evidence-quality|output-classification`
  - FMT-02: `(must abort|could commit|unknown from evidence)`
- check.py 问题（均为轻微）:
  - 14 个未使用的 import（file_exists / file_valid_json / json_* / timestamp_* / tool_log_* / output_not_contains 等），来自 _shared/checker 库的通用模板，无功能影响但属死代码。
  - `check()` 的 `workspace` 参数未使用。
  - `main()` 中先由 `check()` 内 `set_agent_output(agent_output)` 传入路径字符串、随后又用文件内容覆盖，两次调用略冗余但结果正确（文件内容生效）。
  - 纯脚本可查的其余维度（如输出 JSON 的纯整数性、去重性）未加脚本检查——FMT-02 只验"三个词出现"，对"输出本身是合法 id 数组"无校验。若任务的最终产物是 id 数组，建议未来追加脚本检查（如 `json_valid` + `json_array_all_int`）。

### 10.3 判定词表映射缺口（本审查最重要的发现）

两套词汇并存且**无任何文件显式桥接**:

| skill/参考词汇（决策树） | SCORING/FMT-02 判分词汇 |
|--------------------------|------------------------|
| necessary abort | must abort |
| conservative abort（unnecessary for correctness） | could commit |
| unknown / insufficient evidence | unknown from evidence |
| （evidence-quality 额外）proven safe / proven unsafe / aborted by protocol condition, safety unknown | （无对应，超集） |

风险场景: agent 严格按 validation-and-abort-records.md 决策树得出 "conservative abort (unnecessary for correctness)"，这是一个**语义正确、完全符合 skill 方法**的结论，但字面上不含 "could commit"，FMT-02 脚本判否 → 该 agent 即便推理全对也会丢分。反之，agent 若只输出三分词而不展示决策树术语，LLM judge 的 PROC-05/FMT-01 又可能认为未按参考执行。

修复方向（见 §13 P1-3）: 在 SKILL.md 步骤 5 或 output-classification-patterns.md 的 Common Labels 节加一行显式映射表（"决策树结论 → 输出判定词"），或在 SCORING.yaml 的 FMT-02 pattern 中放宽为 `must abort|could commit|conservative abort|necessary abort|unknown`。

### 10.4 评分结构评价

- 无权重、无总分配置（与语料其余 SCORING.yaml 一致），18 项等权 + 3 项 cap_to_0，结构简单可复现。
- LLM 16 项占 88.9%，对评测成本不友好但符合本语料的统一设计；且 LLM 问题的 evidence 字段都标注了取证位置（working notes / final output），可审计性好。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier 2026-08-05 全语料审查记录中 219 的条目（Batch 201-225 摘要）:

> "219 证据纪律贯穿" — 批次总评 "其余 🟡 缺章节或需修复"，202 与 216 等条目分别标注过重叠与引用问题，**219 未列入 🔴/🟠 清单**。

即: dossier 对 219 的定性为 **🟡（可用但有小问题）**，具体问题指向"缺章节"（与本次审查 §3.2 的两节缺失结论一致）。本次深度审查在 dossier 结论基础上新增的发现:

1. FMT-02 判分词汇与 skill 决策树词汇未桥接（§10.3）—— dossier 按 5 维度审查时未涉及 SCORING 与 skill 的词汇级交叉，这是本次审查独有发现，属**评估健壮性**问题而非 skill 内容问题。
2. 缺输出/范围两节的具体影响面分析（§3.2、§9.6）。
3. 工作示例缺失（§9.5）。
4. references 质量分级（§5.3）: 7 个文件全部中高以上，validation-and-abort-records 为全篇最佳。

---

## 12. 综合评分

| 维度 | 权重 | 得分(5) | 依据 |
|------|:----:|:------:|------|
| 逻辑一致性 | 25% | 4.8 | 双账本门禁、6 步闭环、决策树完备、零矛盾；唯一小缺口是协议未知任务的降级路径 |
| 语法与格式 | 15% | 5.0 | 9/9 项零问题，YAML/Python/Markdown 全部干净 |
| 人机感 | 15% | 4.8 | 零 emoji、零喊话、克制有温度；"tiny ledgers" 与 "pick the next file" 恰到好处 |
| 规范合规 | 25% | 3.7 | 10/12 项通过；缺 Output Format 节与 Scope 节（语料最常见缺口）；触发信号为变体写法 |
| 可执行性 | 20% | 4.0 | 账本伪代码 + 决策树 + ID-only JSON 落地性强；扣分于示例缺失与词表映射缺口 |

**加权总分**: 0.25×4.8 + 0.15×5.0 + 0.15×4.8 + 0.25×3.7 + 0.20×4.0 = 1.20 + 0.75 + 0.72 + 0.925 + 0.80 = **4.40 / 5.0**

**总体评级: 🟡 可用但有小问题（接近 🟢）**

- **优点**: 主题聚焦、方法论原创性强（双账本、"failed predicate"交付物、证据分级）、7 个参考文件质量全部中高以上、引用零断裂、语法零问题、人机感语料顶级。作为"重建型推理"类技能的范例候选。
- **缺点**: 全部集中在"结构补全"与"评估对接"两个层面，无任何内容性硬伤。修复成本低（估计 1-2 小时），修复后可达 🟢。

---

## 13. 修复建议（按优先级分层）

### P0（阻断级，无）

当前无任何必须立即修复的问题。无截断、无死链、无矛盾、无事实错误。

### P1（高优先级，直接影响评估正确性或规范合规）

1. **补 `## Scope / Limitations` 节**（SKILL.md，插入 Common Pitfalls 之前或之后）:
   - 声明不适用场景: 无任何日志/表格/计数器的纯代码级事务审查；任务明确给出完整事务列表要求逐条翻译而非推断时；需要实时监控而非事后重建时。
   - 声明与相邻技能的分工（用技能名散文引用，如 "see also: 同语料事务类技能"），避免 description 级路由（SKILL-SPEC §2.5 禁止 description 内路由，body 内允许）。
   - 可将 Common Pitfalls 并入或保留，两节职能不同（Scope=何时不用；Pitfalls=用的时候别犯哪些错）。

2. **补 `## Output Format` 节**（SKILL.md，工作流第 6 步之后）:
   - 3-5 行即可: 外部输出形态（id 数组 / 三判定词 / 任务指定格式）、投影原则（"外部输出是内部分类表的投影，见 output-classification-patterns.md"）、必查项（去重、排序、纯整数、无散文）。
   - 目的: 满足 SKILL-SPEC §3.1 的结构要求，而非新增内容（内容已在参考文件中）。

3. **桥接判定词表**（P1-3，评估健壮性）:
   - 首选方案: 在 SKILL.md 步骤 5 或 output-classification-patterns.md "Common Labels" 节加显式映射表:
     `necessary abort → must abort; conservative abort (safe order exhibited) → could commit; insufficient evidence → unknown from evidence`
   - 备选方案: SCORING.yaml FMT-02 pattern 放宽为 `(must abort|could commit|conservative abort|necessary abort|unknown)`，并同步 check.py 的正则，避免脚本与规范再次漂移。

### P2（中优先级，可执行性与体验）

4. **补一个微型工作示例**: 在 body（约 90 行处）或 validation-and-abort-records.md 末尾加 8-12 行走查——两笔事务、同一键、一次校验失败，展示"数据字典 → 账本 → 失败谓词 → 三分词"完整链路。对 agent 的推理模式匹配收益显著。

5. **协议未知任务降级路径**: 步骤 4 加一句 "若任务未声明协议，跳至 evidence-quality-and-uncertainty.md 的 Missing Data Questions，按 unknown 兜底"。

6. **description 触发信号微调**: 将 "Use when reconstructing..." 改为 "Use when the user needs to reconstruct..." 或 "Use when the user asks to reconstruct..."，完全对齐 SKILL-SPEC §2.4 模板清单（低风险、零语义损失）。

### P3（低优先级，工程卫生）

7. check.py 清理: 移除 14 个未使用 import；`workspace` 参数标注 `_` 或删除。
8. （可选）为 FMT-02 追加"输出为合法整数 id 数组"的脚本检查（`json_valid` + 数组元素类型），覆盖"三分词出现但输出格式错误"的中间态。
9. transaction-history-reconstruction.md 与 evidence-quality-and-uncertainty.md 之间补一行交叉引用（残缺记录 4 种解释 → 缺失数据 6 问），收拢两文件的互补关系。

### 修复后预期

- 完成 P1 三项后: 规范合规 12/12 通过，评级可达 🟢。
- 完成 P2 三项后: 可执行性评分预计从 4.0 升至 4.5+，FMT-02 误判风险消除。
- 总工作量估算: 2 小时以内，不涉及任何重写。

---

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-08-06 | 首次完整审查（10 文件逐行通读），产出本 REVIEW.md；评级 🟡 4.40/5 |

---

## 附录: 审查过程记录

1. **读取范围**: 目录下全部 10 个文件逐行通读（SKILL.md 69 行、SCORING.yaml 167 行、check.py 77 行、references 7 文件 404 行），无抽样。
2. **对照读取**: `_shared/SKILL-SPEC.md` v1.0（12 项合规清单）、`_shared/` 目录存在性（checker.py / CHECKER-LIBRARY.md 验证 check.py 依赖）、同语料 REVIEW.md 模板（001-skill-tuning，13 节结构）、项目 memory `skill-dossier.md`（219 的 batch 定性）。
3. **验证动作**: `wc -l` 统计全部文件行数；目录清单 `ls`/`find` 确认无隐藏资源与孤立文件；正则逐字比对 SCORING.yaml 与 check.py 的两处 `pattern`。
4. **审查方法**: 五维评估（逻辑/语法/人机感/合规/可执行）+ SCORING 交叉映射 + 词表桥接分析（§10.3 为本次审查新增发现，dossier 未覆盖）。
5. **未执行项**: 未对 check.py 做实际运行测试（无评测环境数据）；未对照其他事务类 skill（202/216 等）做内容重叠分析——如需去重审计，可另立专题。
