# REVIEW: 058-tpl-situacao-data-pipeline（深度复评）

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: mindset / template — 数据管道场景模板（ETL/ELT、数据摄入、转换流、流式消费、批处理作业）；tpl-situacao 家族（葡萄牙语模板系列，situacao = "situation"）
**审查范围**: 目录内全部 4 个文件 + `_shared/SKILL-SPEC.md` + memory `skill-dossier.md`
**上一版状态**: 2026-08-05 stub（4 行，🟡 B− 46/100）——本版全面展开并更正其核心结论
**本版结论**: 🟡 **B（84/100）** — 编号/粗体缺陷已随 2026-08-05 家族修复落地；核心残留为 description 与正文的承诺断裂（WHAT 声称 debugging/security/refactoring，正文为零覆盖）与 Scope 节缺失

---

## 1. 目录清单

| # | 文件 | 行数 | 角色 |
|---|------|:----:|------|
| 1 | `SKILL.md` | 191 | 主技能文件（frontmatter + 8 个一级节正文） |
| 2 | `SCORING.yaml` | 183 | 评估标准：20 项 criteria + 3 项 critical failures |
| 3 | `check.py` | 81 | 评估执行器：8 项 script 检查（SCOPE-02、PROC-02/03/06、OUT-04、NEG-01/02/03） |
| 4 | `REVIEW.md` | 4 | 本文件（旧版 stub，2026-08-05，待覆盖） |

**外部参照文件**（不在技能目录内，但为本审查依据）：
- `D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md`（162 行，合规基准，下称 SP）
- `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`（1203 行，dossier 档案，下称 D）
- `_shared/checker.py`（存在，`check.py` 的导入依赖，位于 `complex-skills/_shared/`）

**行号约定**：下文以 `S:` 指 SKILL.md、`Y:` 指 SCORING.yaml、`K:` 指 check.py、`R:` 指旧版 REVIEW.md stub、`SP:` 指 SKILL-SPEC.md、`D:` 指 skill-dossier.md。

**家族背景**：本技能属 tpl-situacao 模板系列（第 15 号模板，源文件 `situacao/15-data-pipeline.md`，葡萄牙语打包模板）。系列成员包括 023/029/030/046/059/078/101/115/116/131/132/145/146/166-169 等，共享 "SITUATION:" 标题、路由表、DO NOT、OUTPUT FORMAT、QUALITY GATES 骨架。按审查约定，葡萄牙语系列命名与模板骨架属**有意保留**，不计为缺陷；但描述文案与技能内容的匹配问题仍属实质缺陷（详见 §4、§13）。

---

## 2. Frontmatter 审查

### 2.1 name（S:2）
`tpl-situacao-data-pipeline` — 小写+连字符、≤64 字符、与目录名 `058-tpl-situacao-data-pipeline` 完全一致（SP:13、SP:160）。✅

### 2.2 description（S:3）
```
Pack template (situacao/15-data-pipeline.md). Guides the agent on situational tasks such as
debugging, security and refactoring aligned with this context. Use when the user is building
ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers,
or batch processing jobs.
```
逐项对照 SP §2（SP:36-73）：
- **WHAT** ⚠️ 具体但**错位**：`Pack template (situacao/15-data-pipeline.md)` 是模板内部书签（打包源文件路径），不应出现在面向用户的描述中；`Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context` 声称覆盖 debugging/security/refactoring，但正文**完全没有**这三类内容（§4.1 详析）
- **WHEN** ✅ 五个触发场景列举完整且与正文完全对应（ETL/ELT、数据摄入、转换流、流式消费、批处理作业）
- **KEYWORDS** ✅ ETL/ELT、ingestion、transformation、streaming、batch 等域词齐全
- **人称** ✅ 第三人称，无祈使/第一/第二人称开头（SP:54-58）
- **触发短语** ✅ 含 "Use when the user"（SP:63）
- **无跨技能路由** ✅（SP:70）
- **长度** ✅ 约 330 字符，≤1024（SP:14）

### 2.3 禁止字段检查（SP:29-30）
仅含 `name`/`description` 两个允许字段，无 `metadata`/`version`/`tags`/`trigger` 等任何禁止键。✅

**Frontmatter 小结**：格式完全合规，无违规键；但 description 的 WHAT 子句与正文内容断裂是本技能**最核心的缺陷**——触发匹配时，声称的 "debugging, security and refactoring" 能力会引导 agent 在无关任务上调用本技能（详见 §4.1、§13 P0-1）。

---

## 3. Body 结构

### 3.1 一级节序列
SKILL.md 共 1 个 H1 + 8 个 H2 节，无编号、顺序如下：

| 行 | 节 | 内容 |
|:--:|----|------|
| S:6 | `# SITUATION: Building a Data Pipeline` | H1，7 条设计原则（S:8-20） |
| S:22 | `## ROUTING TABLE` | 10 行诊断→对策表（S:24-35） |
| S:37 | `## Pipeline Architecture Patterns` | 批/流/lambda 三模式图（S:39-49） |
| S:51 | `## Checkpoint Template` | Python 类：save/load/reset（S:53-74） |
| S:76 | `## Data Validation Gates` | ValidationResult + validate_payment_record（S:78-109） |
| S:111 | `## Dead Letter Queue Pattern` | process_record 失败路由示例（S:113-130） |
| S:132 | `## DO NOT` | 8 条反模式禁令（S:134-141） |
| S:143 | `## OUTPUT FORMAT` | Pipeline Specification 模板（S:147-178） |
| S:180 | `## QUALITY GATES` | 10 项验收清单（S:182-191） |

### 3.2 三必需节检查（SP:102-108）
| 必需节 | 状态 | 依据 |
|--------|:----:|------|
| Workflow/Process | ⚠️ 部分 | 无显式 Workflow 节；7 条原则（S:8-20）+ 路由表（S:24-35）+ 架构模式（S:37-49）承担流程功能。对 mindset 型可接受，但无步骤链与"输入→动作→输出"的流程化表达 |
| Output Format | ✅ | `## OUTPUT FORMAT`（S:143-178），含 Source/Transformations/Destination/Validation Gates/Failure Handling 五小节模板，具体值完整（系统名、调度周期、SLO 数字） |
| Scope/Limitations | ⚠️ 部分 | `## DO NOT`（S:132-141）8 条禁令覆盖"不可为"，但无显式"本技能不做什么/何时不用"声明（SP 示例要求"when it should NOT be used"） |

### 3.3 体量
191 行，≤600 硬上限（SP:120）。按 SP:114-118 模式量级：SCORING 标记为 mindset（Y:2），mindset 目标 ~50 行——当前 191 行是目标值的近 4 倍，且含 3 段代码模板与完整输出模板，形态上更接近 process 型（~200 行目标）。**pattern 标记与正文形态不完全匹配**（详见 §10.3、§13 P2-1）。

### 3.4 文件引用
正文零文件引用（无 scripts/、无 references/、无 `../`），完全自包含。✅（SP:123-126）

**Body 小结**：骨架完整、输出节强、范围节部分覆盖。结构问题集中在"流程无显式化"与"范围无显式声明"两处，属家族通病（与 029/030/046/059 同源），非本技能独有。

---

## 4. 逻辑一致性（核心审查）

### 4.1 description ↔ body 承诺断裂【本技能首要缺陷】

S:3 的 WHAT 子句声称：
> "Guides the agent on situational tasks such as **debugging, security and refactoring** aligned with this context"

对正文做穷举核查：
- **debugging**：正文无任何调试指导。最接近的条目是路由表 S:30 "Pipeline taking too long"（性能剖析）与 S:34 "Transformation failure on 1 bad record"（单条失败处理），但这些都是**构建期设计对策**，不是调试方法论；"debugging" 声称无支撑。
- **security**：正文零安全内容（无权限、加密、审计、CWE 等条目）。"security" 声称无支撑。
- **refactoring**：正文零重构内容。声称无支撑。
- **"aligned with this context"**：无信息量填充语（"this context" 指代不明）。
- **"Pack template (situacao/15-data-pipeline.md)"**：模板内部书签，向用户泄露打包路径，且无功能语义。

对照 SP §2.1：WHAT 必须是 "what this skill does, be specific"——当前 WHAT 描述的是一个**通用模板**而非本技能实际交付的数据管道设计指导。触发层面：用户在"调试管道性能"或"重构管道代码"时会命中 description 声称，而技能正文给不出对应指导；用户在"构建管道"时命中 WHEN 子句（正确的），WHAT 子句却不描述管道。**承诺-交付双向断裂**。

### 4.2 内部一致性（强项）

7 条原则、路由表 10 行、3 段代码模板、DO NOT 8 条、QUALITY GATES 10 项、OUTPUT FORMAT 5 小节之间交叉一致，无矛盾。以"幂等"为例的同链贯通：

| 环节 | 位置 | 表述 |
|------|------|------|
| 原则 2 | S:10 | "unique keys on destination inserts, upsert semantics, checkpointing" |
| 路由表 | S:26 | "Add idempotency key. Use upsert (INSERT ... ON CONFLICT DO UPDATE) or deduplication step" |
| Checkpoint 模板 | S:61-73 | save/load/reset 三方法，resume-on-failure |
| 输出模板 | S:166 | "Load method: UPSERT on transaction_id" |
| 质量门 | S:182 | "Pipeline is idempotent: running twice produces identical destination state" |

同理，原则 5（失败要响）↔ 路由表 S:35（freshness 告警）↔ DLQ 示例 S:118（alert on DLQ growth）↔ 输出模板 S:176-177（PagerDuty 阈值）；原则 7（UTC）↔ S:65（utcnow）↔ S:139（DO NOT 第 7 条）↔ S:159（转换步骤 2）↔ S:188（质量门）。**五层互证，无一处矛盾**——这是本技能在 20 个评估项上全部有直接支撑的基础（见 §10.2）。

### 4.3 代码示例逻辑核查

- **Checkpoint 模板（S:53-74）**：save 记录 `last_processed_id`/`processed_count`/`updated_at`，load/reset 语义正确；`datetime.utcnow().isoformat()` 在 Python 3.12+ 已弃用（DeprecationWarning，技术时新性小问题，见 §4.4）。`CheckpointStorage` 与 `Optional` 未定义——模板式接口草图，见 §9.2。
- **验证函数（S:78-109）**：字段守卫正确——`if 'amount' in record and ...`（S:96、S:100）防止缺失字段叠加报错；required/type/range/enum 四类检查与 SCORING PROC-02 的"null checks, value range checks"逐词对应。唯一瑕疵：enum 检查（S:105）未守卫缺失——currency 缺失时 S:93 已报 "Missing required field"，S:106 会再叠加一条 "Invalid currency: None"，产生冗余双报（见 §13 P2-3）。
- **DLQ 示例（S:113-130）**：失败路由（校验失败→DLQ 带 reason+pipeline_version；处理异常→DLQ 带 exception_type）、成功计数、日志事件结构均正确，与 PROC-03/CF-03 口径一致。`validate_record`/`transform`/`destination`/`metrics`/`logger` 未定义——同属模板式草图。

### 4.4 技术正确性

- "INSERT ... ON CONFLICT DO UPDATE"（S:26）— PostgreSQL UPSERT 语法正确；
- watermark 轮询抽取（S:154）、ISO 4217 货币规范（S:158）、BigQuery DATE 分区（S:167）、lambda 架构（S:46-48）— 均准确；
- 无 EPSS/CVSS 类外部事实引用，**未发现事实性错误**；
- 唯一技术时新性问题：`datetime.utcnow()`（S:65）自 Python 3.12 弃用，新代码应使用 `datetime.now(timezone.utc)`（见 §13 P1-3）。

### 4.5 一致性结论

1. 内部逻辑高度一致（五层互证、20/20 评估项有支撑）——本技能最大优点；
2. 核心断裂在**描述层**：WHAT 子句与正文内容零重叠（§4.1）；
3. 次要问题：enum 双报（S:105）、utcnow 弃用（S:65）、pattern 标记与形态不符（Y:2）；
4. 无跨文件口径分裂（SCORING/check.py/SKILL.md 三方一致，与 050 的分类法错版问题性质完全不同）。

---

## 5. 参考文件审查

### 5.1 无 references/scripts 子目录
技能目录仅 4 个文件（§1），正文零外部引用。自包含设计对 mindset 型模板属合理——191 行无超限压力，SP 的"600 行外内容进 references/"规则（SP:120）不触发。✅

### 5.2 SCORING.yaml（183 行）
- `total_items: 20`（Y:3）与实际一致：SCOPE 3 + PROC 7 + OUT 4 + NEG 3 + QA 3 ✅；judge 分配：script 8 项、llm 12 项；
- 正则与正文词面匹配核查（逐一验证正文包含）：
  - SCOPE-02/NEG-01 `write to source|modify source|...`（Y:21、Y:128）— S:134 "DO NOT write to source tables"、S:8 "Never write to" ✅
  - PROC-02 `row count|validation gate|null check|required field|value range|referential integrity`（Y:46）— S:14 逐词命中 ✅
  - PROC-03 `dead[- ]letter|dlq|pipeline_version|pipeline version`（Y:54）— S:34/137/175、S:118 ✅
  - PROC-06 `utc|utcnow|timezone`（Y:78）— S:20/65/139 ✅
  - OUT-04 `checkpoint|last_processed_id|resume`（Y:119）— S:61/62/55 ✅
  - NEG-02 `chunk|stream|chunksize|iter_|generator`（Y:136）— S:33/136 ✅
  - NEG-03 `datetime\.now\(\)|strftime...`（Y:144）— 正文仅用 `utcnow()`，**负向检查设计精巧**：技能自带的 UTC 模板不会误伤 ✅
- 3 项 critical_failures（Y:171-182）cap_to_0 设置合理：写源数据、非幂等、静默吞错——均与原则 1/2/5 直接对应；
- 无缺陷。

### 5.3 check.py（81 行）
- `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))`（K:10）→ 解析到 `complex-skills/_shared/`，`checker.py` 已核证存在，导入可成功 ✅；
- 8 项 script 检查（K:35-53）与 SCORING 正则逐字一致，注释标明 llm 判定项不在此处 ✅；
- main() 对 agent_output 做路径/内容双态处理（K:61-76），`os.path.exists` 双保险，稳健 ✅；
- 轻微冗余：K:25-29 的 `_is_path` 检测与 main() 的文件预读职责重叠（main 已读入内容后 check() 再判一次路径），无害但可简化（见 §13 P3）。

### 5.4 参考完整性总评
三件套（SKILL.md / SCORING.yaml / check.py）**完全同口径**，无悬空引用、无口径分裂、无缺失依赖。这是本技能评估链路健康的决定性证据——agent 按 SKILL.md 执行、按 SCORING 打分、由 check.py 判定，三方互不打架。

---

## 6. 语法格式

### 6.1 编号与粗体【已修复】
dossier（D:477-478）与旧版 stub（R:3）均记录"首条原则编号丢失、粗体断裂（列表从 2 开始）"。对当前文件逐字节核验（`cat -A`）：
- S:8 = `1. **Immutability of source is sacred.** Never write to, modify, or delete source data...` — **编号 1 存在、粗体标记闭合**；
- S:10-20 编号 2-7 连续完整；
- **该缺陷已随 2026-08-05 的 tpl 家族修复（memory 记录 "tpl28/28"）清除**。D:1122 统计表中"tpl 模板编号断裂 ~18"项应随家族修复更新（见 §11.3）。

### 6.2 其他格式
- 英文文体干净，无拼写错误、无病句、无中英混杂（正文为英文；"SITUATION:" 前缀与 `situacao` 系列命名为葡萄牙语家族惯例，按审查约定属有意保留）；
- 表格 1 张（路由表 S:24-35）：表头/分隔行/10 行数据对齐规范 ✅；
- 代码围栏 5 段全部闭合（S:39-49、S:53-74、S:78-109、S:113-130、S:148-178）✅；
- DO NOT 列表破折号使用一致（—）✅；QUALITY GATES 复选框 `- [ ]` 格式统一 ✅；
- 无装饰性 emoji（与家族其他成员一致，优于 072 等 emoji 泛滥案例）。

**语法格式小结**：9/10。编号/粗体问题已修复，当前版本无可挑剔；唯一可议处是 "Pack template (situacao/15-data-pipeline.md)" 书签残留在描述中（属 §2/§4 内容问题而非格式问题）。

---

## 7. SKILL-SPEC 合规 12 项

按 SP:148-161 的合规清单逐项核验：

| # | 检查项（SP 行） | 结果 | 依据 |
|---|----------------|:----:|------|
| 1 | name 小写+连字符、≤64、匹配目录（SP:149） | ✅ | S:2 |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024（SP:150） | ✅ | S:3（WHAT 错位属内容问题，格式合规） |
| 3 | description 无祈使/第一/第二人称开头（SP:151） | ✅ | S:3 |
| 4 | description 无跨技能路由（SP:152） | ✅ | S:3 |
| 5 | 至少一个触发短语（SP:153） | ✅ | "Use when the user"（S:3） |
| 6 | frontmatter 无允许列表外字段（SP:154） | ✅ | S:1-4（详见 §2.3） |
| 7 | body ≤600 行（SP:155） | ✅ | 191 行 |
| 8 | 有 workflow/process 节（SP:156） | ⚠️ 部分 | 无显式 Workflow 节；原则+路由表承担（见 §3.2） |
| 9 | 有 output format 节（SP:157） | ✅ | `## OUTPUT FORMAT`（S:143-178） |
| 10 | 有 scope/limitations 节（SP:158） | ⚠️ 部分 | `## DO NOT` 部分覆盖（见 §3.2） |
| 11 | 无跨技能文件引用（SP:159） | ✅ | 正文零引用（见 §3.4） |
| 12 | 目录 NNN-kebab-case 无空格大写（SP:160） | ✅ | `058-tpl-situacao-data-pipeline` |

**合规判定**：12 项中 **10 项通过、2 项部分（#8 workflow、#10 scope）**。
附加审查：
- 知识增量原则（SP:129-133）：7 条原则（幂等、UTC、回填、schema 演进）与模型通用工程常识重叠度中等——"knowledge delta" 偏薄，但路由表（10 个具体诊断→对策）与 OUTPUT FORMAT（带具体系统名与数字）显著弥补；决策表化（SP:132）执行出色，路由表正是 SP 推崇的决策表形态 ✅；
- 反模式优先（SP:131）：DO NOT 8 条均为"具体禁令+理由"（如 "DO NOT run backfill during peak traffic hours — it will compete with production workloads"），符合 SP 要求 ✅；
- 非 frontmatter 元数据（SP:32）：无版本/作者等元数据，n/a。

合规问题均为结构性小缺口（workflow/scope 显式化），无硬性违规。

---

## 8. 人机感

### 8.1 语气基调
- 祈使式、直接、简洁："Immutability of source is sacred."（S:8）、"Data pipeline failures must be loud."（S:16）——强断言有实操支撑，非口号；
- 全文无 emoji、无填充语、无第一人称包装、无喊叫式大写（与 072 等反例形成对照）；
- 路由表是"if-you-encounter → then"的机器可执行格式，agent 可直接照单处置；
- DO NOT 列表语气坚定但不粗暴，理由与代价显式（SP:131 反模式写法范本）。

### 8.2 扣分项
1. description 的 "aligned with this context"（S:3）是无信息量填充语，读感模糊（内容问题，见 §4.1）；
2. "Pack template (situacao/15-data-pipeline.md)"（S:3）给用户"这是模板残件"的观感，削弱技能的成品感。

**人机感小结**：9/10。家族系列中最克制的语气之一，无装饰性元素；扣分仅来自 description 的两处模板残迹。

---

## 9. 可执行性

### 9.1 主流程可执行性
agent 可按闭环执行：**原则（设计约束）→ 路由表（问题诊断）→ 代码模板（实现参照）→ OUTPUT FORMAT（交付规格）→ QUALITY GATES（验收）**。五环节每步都有具体可操作内容，无"按上下文行事"式空转。路由表 10 行的对策全部可直接实施（指定了 upsert 语义、DLQ 行为、分区回填策略、chunked 读取等）。✅

### 9.2 代码模板可执行性（边界）
3 段代码均为**接口草图**而非可运行脚本：
- Checkpoint 模板（S:53-74）依赖未定义的 `CheckpointStorage`，且 `Optional`/`datetime` 无 import——需按环境实现存储后端；
- DLQ 示例（S:113-130）依赖未定义的 `validate_record`/`transform`/`destination`/`metrics`/`logger`/`PIPELINE_VERSION`/`DeadLetterQueue`——是模式示意；
- 验证函数段（S:78-109）**自足可运行**（imports 齐全、函数完整）✅。
对 mindset 型模板而言，"接口草图 + 自足示例"混合是可接受风格；但建议在节首标注"以下为模式示意，需按项目适配实现"以免 agent 原样照抄（见 §13 P1-3）。

### 9.3 评估链路可执行性
`python check.py <workspace> <tool_log> <agent_output>` 可直接运行：8 项 script 检查全部有正文支撑（§5.2 逐词验证），12 项 llm 判定有明确证据字段。**不存在 050 式的"评估工具与技能交付物互相矛盾"问题**——本技能评估链路健康。

**可执行性小结**：9/10。主流程与评估链路完全可执行；扣分仅来自代码草图的未标注属性。

---

## 10. SCORING 交叉参考

### 10.1 结构核对
Y:3 `total_items: 20` 与实际一致（SCOPE 3 + PROC 7 + OUT 4 + NEG 3 + QA 3）；judge 分配：script 8 项（Y:19、Y:44、Y:52、Y:76、Y:117、Y:126、Y:134、Y:142）、llm 12 项；K:35-53 的脚本端实现与 YAML 完全对应。✅

### 10.2 与 SKILL.md 的一致性映射

| SCORING 项 | 对应 SKILL.md 依据 | 一致性 |
|-----------|--------------------|:----:|
| SCOPE-01（Y:7-13） | description WHEN 子句（S:3） | ✅（但 WHAT 子句误导，见 §4.1） |
| SCOPE-02（Y:15-21） | 原则 1（S:8）+ DO NOT 第 1 条（S:134） | ✅ |
| SCOPE-03（Y:23-29） | 原则 2（S:10） | ✅ |
| PROC-01（Y:33-39） | 原则 3（S:12） | ✅ |
| PROC-02（Y:41-46） | 原则 4（S:14）+ 验证函数（S:87-108） | ✅ |
| PROC-03（Y:48-54） | DLQ 节（S:111-130）+ DO NOT 第 4 条（S:137） | ✅ |
| PROC-04（Y:56-63） | 原则 5（S:16） | ✅ |
| PROC-05（Y:65-71） | 原则 6（S:18）+ 路由表 S:31 | ✅ |
| PROC-06（Y:74-78） | 原则 7（S:20）+ 模板代码（S:65） | ✅ |
| PROC-07（Y:80-85） | 路由表 10 行（S:26-35） | ✅ |
| OUT-01（Y:89-95） | 输出模板 Source/Transformations/Destination（S:151-167） | ✅ |
| OUT-02（Y:97-103） | 输出模板 Validation Gates（S:169-172） | ✅ |
| OUT-03（Y:105-111） | 输出模板 Failure Handling（S:174-177） | ✅ |
| OUT-04（Y:113-119） | Checkpoint 模板（S:61-73） | ✅ |
| NEG-01（Y:123-128） | DO NOT 第 1 条（S:134） | ✅ |
| NEG-02（Y:130-136） | 路由表 S:33 + DO NOT 第 3 条（S:136） | ✅ |
| NEG-03（Y:138-144） | DO NOT 第 7 条（S:139）；正文无 datetime.now() | ✅ |
| QA-01（Y:147-153） | QUALITY GATES 10 项（S:182-191） | ✅ |
| QA-02（Y:155-161） | 架构模式三选（S:39-49） | ✅ |
| QA-03（Y:163-169） | 路由表 S:31 + DO NOT 第 8 条（S:140） | ✅ |
| CF-01/02/03（Y:171-182） | 原则 1/2/5 与 DO NOT/DLQ 节 | ✅ 合理（cap_to_0 恰当） |

### 10.3 判定
- **20/20 项 + 3 项 CF 全部有直接正文支撑**——在已审查语料中属罕见的高对齐度（对比 050 的 PROC-01 结构性矛盾、003 的跨技能路径）；
- SCORING 设计质量高：证据字段明确、critical failures 语义精确；
- 次要问题：Y:2 `pattern: mindset` 与正文形态（191 行、含代码模板与输出模板，接近 process 型）不完全匹配；description（Y:9）若按 §13 P0-1 重写，SCOPE-01 的触发匹配将更纯净（消除 debugging/security/refactoring 误导项）。

---

## 11. dossier 汇总

### 11.1 dossier 对 058 的原始记录（D:476-481）
> - **逻辑**: 路由表、检查点、验证门、死信队列等模式完整一致，但编号列表首项丢失（列表从 2 开始），description 声称覆盖 "debugging, security and refactoring" 与实际数据管道内容不符。
> - **语法**: 开篇 "Immutability of source is sacred.**" 粗体标记断裂，编号 1 丢失导致 markdown 渲染破损。
> - **人机感**: 祈使语气简洁专业，无 emoji。
> - **合规**: Description 为第三人称但属打包模板通用文案，与技能内容匹配度低；正文 191 行 ≤600。
> - **总评**: 🟡 技术内容实用，但编号丢失与 description 失配需修复。

### 11.2 dossier 判定与当前文件的一致性
- **D:477/D:478 的编号与粗体缺陷已过期**：当前文件 S:8 为 `1. **Immutability of source is sacred.**`，编号与粗体完整（§6.1 逐字节核验）。dossier 记录的是 2026-08-05 家族修复前的版本；memory 状态字段（"fixed — ... tpl28/28"）已记录该修复，但 D:477-478 与 D:1122 统计表（"tpl 模板编号断裂 ~18"）未同步更新；
- **D:479 人机感判定维持** ✅：当前文件语气与记录一致；
- **D:480 行数"191 行"与当前一致** ✅（wc 190 为末行无换行的计数差，实际 191 行）；
- **D:480 的 description 失配判定维持** ✅：S:3 至今未改，WHAT 子句仍与正文断裂（§4.1）。

### 11.3 本复评对 dossier 的处置建议
- 维持 🟡 评级，但**更正问题定性**：剩余缺陷不是"编号丢失"（已修复），而是 description WHAT 错位 + Scope 节缺失两项结构性缺口；
- 建议勘误：D:477-478 更新为"编号缺陷已于 2026-08-05 家族修复中清除"；D:1122 统计表的"tpl 模板编号断裂 ~18"项更新为已清零（经家族修复后）；
- 家族级视角：058 是 tpl-situacao 系列中**结构最完整、代码模板最具体**的成员之一（对比 059 的 96 行、023 的 148 行），其剩余问题代表家族共性缺口（description 通用文案、缺显式 Scope），可作家族批量修复的样板。

### 11.4 旧版 REVIEW.md stub 的同源问题（R:1-4）
- R:3 "首条编号破损——'Immutability of source is sacred.**' 粗体标记断裂"——**过期记录**，当前文件已修复；
- R:3 "Description 声称覆盖 'debugging, security and refactoring' 与实际数据管道内容不符"——**正确判定**，维持；
- R:4 "**综合**: 🟡 **B−** (46/100)"——**自相矛盾**：46/100 按本审查等级带（§12.2）落在 D 区间（<55），与 B− 标签不符；本复评重算为 84/100 → B（§12）。

---

## 12. 综合评分（8 维加权 + 等级）

### 12.1 评分维度与权重

| # | 维度 | 权重 | 得分 | 加权 | 核心理由 |
|---|------|:----:|:----:|:----:|----------|
| 1 | **事实准确性** | 30% | 9/10 | 2.70 | 无事实错误；UPSERT/watermark/ISO 4217/lambda 均正确；仅 utcnow() 弃用属时新性小问题 |
| 2 | **逻辑一致性** | 20% | 7/10 | 1.40 | 内部五层互证高度一致；description WHAT 与正文零重叠为唯一显著断裂 |
| 3 | SKILL-SPEC 合规 | 10% | 8/10 | 0.80 | 12 项中 10 过、2 部分（workflow/scope 显式化） |
| 4 | 可执行性 | 10% | 9/10 | 0.90 | 闭环可执行、评估链路健康；代码草图未标注为唯一扣分 |
| 5 | 语法格式 | 10% | 9/10 | 0.90 | 编号/粗体已修复；围栏/表格/清单规范 |
| 6 | 人机感 | 10% | 9/10 | 0.90 | 家族最克制语气之一；description 模板残迹微扣 |
| 7 | 参考文件完整性 | 5% | 9/10 | 0.45 | 自包含、无悬空引用；SCORING/check.py 同口径（无独立参考文件，按 n/a 满分处理） |
| 8 | 输出/范围完整性 | 5% | 7/10 | 0.35 | 输出节强（含模板）；范围节仅 DO NOT 部分覆盖 |
| | **合计** | **100%** | | **8.40** | **84/100** |

### 12.2 等级判定
| 等级 | 区间 | 判定 |
|------|------|------|
| A | 85-100 | 可用，无需修改 |
| **B** | **70-84** | **可用，小修** |
| C | 55-69 | 需明显修复 |
| D | <55 | 需重大修复/重写 |

**综合评级：🟡 B（84/100）**——位于 B 档上沿，距 A 档仅 1 分。相比旧版 stub 的 46/100：差异主要来自（a）编号/粗体缺陷已修复（语法维度 4→9）；（b）上版把"B−"标签配在 46 分上，等级-分数错配（§11.4）；（c）本版全面核验了 SCORING/check.py 链路的 20/20 对齐，确认评估侧无缺陷。

### 12.3 修复后预估
按 §13 P0-1（description 重写）+ P1-1（补 Scope 节）+ P1-2（补 Workflow 节）执行后：逻辑一致性 7→9（+0.40）、合规 8→10（+0.20）、输出/范围 7→9（+0.10）、人机感 9→10（+0.10）≈ **90/100 → B+ / A−**。即：全部扣分集中于描述层与两个结构性缺口，修复成本低、收益确定——这是整个 tpl-situacao 家族中最值得优先修复的样板件。

---

## 13. 修复建议 ★重点★

> 本章为全文重点。按优先级 P0（必须，阻断性）→ P1（应当，一版内完成）→ P2（建议）→ P3（可选）排列，每条给出文件、行号、具体改法与可直接采用的替换文本。

### 13.1 P0-1：重写 description——消除 WHAT 承诺断裂【阻断性】

**问题**：S:3 的 WHAT 子句声称 "debugging, security and refactoring"（正文零覆盖）且含模板书签 "Pack template (situacao/15-data-pipeline.md)" 与填充语 "aligned with this context"（§4.1）。description 是触发匹配的第一入口，承诺与交付断裂会让 agent 在无关任务上误触发、在相关任务上信心不足。

**做法**：保留 WHEN 子句（已与正文精确对应），重写 WHAT 子句为数据管道设计指导的实际内容；删除模板书签与填充语。

**替换文本（直接替换 S:3 整行）**：

```yaml
description: Guides the design and operation of production-grade data pipelines: ETL/ELT ingestion, transformation flows, event streaming consumers, and batch processing, with source immutability, idempotent re-runs, schema evolution handling, validation gates, dead-letter queues, checkpointing, and backfill strategy. Use when the user is building ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers, or batch processing jobs.
```

**新旧对照**：

| 片段 | 旧（S:3） | 新 | 理由 |
|------|-----------|-----|------|
| 开头 | Pack template (situacao/15-data-pipeline.md). | （删除） | 模板书签，泄露内部路径 |
| WHAT | Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context | Guides the design and operation of production-grade data pipelines: ...（枚举正文 7 原则） | 与正文实际能力对齐（§4.1） |
| WHEN | Use when the user is building ETL/ELT pipelines, ... batch processing jobs | 保留原样 | 已精确对应正文 |

**验证**：改后 description 仍第三人称 ✅、含触发短语 "Use when the user" ✅、约 400 字符 ≤1024 ✅、无跨技能路由 ✅；SCOPE-01（Y:7-13）的 LLM 判定将更纯净——"recognizes this as a data pipeline task" 由新旧两句同时支撑。

### 13.2 P1-1：新增显式 Scope/Limitations 节【应当】

**问题**：SP:158 要求 scope/limitations 节回答"本技能不做什么、何时不用"；当前仅 DO NOT（S:132-141）覆盖"不可为"禁令，无边界声明（§3.2）。对 mindset 型模板，明确边界能防止 agent 在管道之外的场景（如数据库调优、实时框架源码修改）越界使用。

**做法**：在 S:141（DO NOT 之后）与 S:143（OUTPUT FORMAT 之前）之间插入一节。**建议文本**：

```markdown
## Scope and Limitations

**What this skill covers:**
- Pipeline architecture decisions (batch / streaming / lambda), design principles,
  failure handling, and operational practices for ETL/ELT, ingestion, transformation,
  streaming consumption, and batch jobs
- Diagnosis of common pipeline failure modes via the routing table
- Deliverable: Pipeline Specification with Source / Transformations / Destination /
  Validation Gates / Failure Handling

**What this skill does NOT do:**
- No implementation of specific frameworks (Airflow, dbt, Spark, Kafka Streams) —
  code templates are interface sketches to adapt, not ready-to-run code
- No database administration, data modeling, or SQL tuning
- No real-time system internals (e.g., exactly-once semantics of a specific broker)
- No debugging methodology, security audits, or code refactoring guidance —
  use dedicated skills for those tasks
- Do NOT use when the user asks about pipeline tool installation/administration
  or when the task is a one-off data transformation script (use a scripting skill)
```

**说明**：末条 "No debugging methodology, security audits, or code refactoring guidance" 与 P0-1 的 description 重写形成呼应——描述不再承诺、正文边界明示，承诺-交付双向对齐。

### 13.3 P1-2：将 7 条原则显式化为 Workflow 节【应当】

**问题**：SP:156 要求 workflow/process 节回答"技能实际做什么、步骤如何"；当前 7 条原则（S:8-20）是设计约束清单，无"先做什么后做什么"的流程化表达（§3.2）。

**做法**：在 S:6（H1 标题）之后插入 Workflow 节，将原则重新组织为 5 步执行链，原则保留为各步的约束依据。**建议文本**：

```markdown
## Workflow

1. **Scope the pipeline** — identify source (system, extraction method, schedule),
   transformations, destination (load method, partitioning). Design for the pattern
   that fits: batch pull, streaming push, or lambda (see Architecture Patterns).
2. **Lock the invariants** — apply the seven principles: source is read-only,
   idempotent re-runs, schema evolution tolerance, validation gates, loud failures,
   backfill strategy, UTC timestamps.
3. **Implement with the templates** — checkpointing (resume-on-failure), validation
   gates (reject early), dead-letter queue (never swallow bad records).
4. **Produce the Pipeline Specification** — follow OUTPUT FORMAT; every section
   needs concrete values (system names, thresholds, SLOs).
5. **Verify against QUALITY GATES** — run the checklist; test idempotent re-run,
   backfill on staging, schema-evolution case, freshness alert.
```

**说明**：步骤 2 显式引用七条原则（S:8-20），步骤 4/5 引用 OUTPUT FORMAT（S:143）与 QUALITY GATES（S:180）——纯内部交叉引用，不新增内容，零风险；workflow 合规项（SP:156）从"部分"转"通过"。

### 13.4 P1-3：代码模板可移植性标注【应当】

**问题**：S:53-74 与 S:113-130 两段代码为接口草图，依赖未定义的 `CheckpointStorage`/`Optional`/`datetime`/`validate_record`/`transform`/`destination`/`metrics`/`logger`/`PIPELINE_VERSION`/`DeadLetterQueue`，且 S:65 使用已弃用的 `datetime.utcnow()`（§4.4、§9.2）。agent 照抄会出现 NameError 与 DeprecationWarning。

**做法**（三选一，建议全部）：
1. 在 S:51 与 S:111 节标题下各加一行：`> 以下为模式示意（interface sketch）——需按项目环境实现存储/日志/指标依赖后运行。`
2. S:65 `datetime.utcnow().isoformat()` → `datetime.now(timezone.utc).isoformat()`（Python 3.12+ 推荐写法，且不违反 PROC-06 的 `utc|utcnow|timezone` 正则——`timezone` 词面仍命中）;
3. S:68 `Optional[dict]` 前补 `from typing import Optional`，或改为 `dict | None`（Python 3.10+ 内建联合类型，无需 import）。

**验证**：修改后 NEG-03 正则（Y:144 `datetime\.now\(\)|strftime...`）仍通过——`datetime.now(timezone.utc)` 与 `datetime.now()` 词面不同，负向检查不受影响。

### 13.5 P2-1：SCORING.yaml pattern 字段校正【建议】

**问题**：Y:2 `pattern: mindset` 与正文形态不符——191 行、含 3 段代码模板、完整输出模板与质量门清单，形态上更接近 process 型（SP:118 目标 ~200 行）而非 mindset 型（SP:114 目标 ~50 行）（§3.3、§10.3）。

**做法**：Y:2 `pattern: mindset` → `pattern: process`。**注意**：此改动仅影响语料分类统计，不影响 20 项 criteria 的执行（judge/check 逻辑与 pattern 字段无关），但使 dossier 的"按 Pattern 分类质量"（D:1193-1197）统计更准确。

### 13.6 P2-2：家族格式收敛——description 模板书签清理【建议】

**问题**：S:3 的 "Pack template (situacao/15-data-pipeline.md)" 与 S:6 的 "SITUATION:" 前缀为 tpl-situacao 家族模板残迹。按审查约定，葡萄牙语系列命名与 "SITUATION:" 骨架属**有意保留**，但文件路径书签不属于系列惯例，属于打包残留。

**做法**：
- "Pack template (situacao/15-data-pipeline.md)"：随 P0-1 一并删除（见 §13.1 替换文本）；
- "SITUATION:" 前缀：**保留**（家族一致性与系列识别需要）；
- 家族批量建议：对 023/029/030/046/059/078/101/115/116/131/132/145/146/166-169 逐一排查 description 中的 "Pack template (...)" 书签与 "debugging, security and refactoring" 通用文案，按各技能实际内容重写 WHAT（058 作为样板先做，其余照 §13.1 模式批量处理）。

### 13.7 P2-3：验证函数 enum 双报修复【建议】

**问题**：S:105 `if record.get('currency') not in valid_currencies:` 未守卫缺失字段——currency 缺失时 S:93 已报 "Missing required field: currency"，S:106 再叠加 "Invalid currency: None"，双报冗余且信息重复（§4.3）。

**做法**：S:104-106 替换为：

```python
    # Enum checks
    valid_currencies = {'USD', 'EUR', 'BRL'}
    currency = record.get('currency')
    if currency is not None and currency not in valid_currencies:
        errors.append(f"Invalid currency: {currency}")
```

**验证**：修改后缺失 currency 仅报一次（required field 检查），存在但非法时仍精确报错；PROC-02 正则（Y:46 "required field|value range" 等）不受影响。

### 13.8 P3：可选打磨【可选】

| # | 位置 | 建议 | 理由 |
|---|------|------|------|
| 1 | K:25-29 | 简化 `_is_path` 双态检测（main() 已预读文件内容后，check() 内的路径检测冗余） | 代码清洁度，无害改动 |
| 2 | S:26 | 路由表 "Duplicate records" 行补充去重示例的幂等键选取建议（如 business key 而非 surrogate key） | 强化决策表的可操作性（SP:132） |
| 3 | S:169-172 | Validation Gates 小节补充 "referential integrity" 的具体检查示例（当前模板只有 required fields/reconciliation/SLO） | 与原则 4（S:14）的 referential integrity 承诺对齐 |
| 4 | S:176-177 | 输出模板的告警阈值可补充"阈值来源"（如 p95 延迟基线推导），避免硬编码任意值 | 增强"具体值"的可辩护性 |

### 13.9 修复验收清单

- [ ] S:3 description = §13.1 替换文本（无 "Pack template"、无 "debugging, security and refactoring"、WHEN 子句原样保留）
- [ ] 新增 `## Scope and Limitations` 节（§13.2 文本，含 "What this skill does NOT do" 与 "Do NOT use when"）
- [ ] 新增 `## Workflow` 节（§13.3 文本，5 步链，交叉引用原则/OUTPUT FORMAT/QUALITY GATES）
- [ ] S:65 `datetime.utcnow()` → `datetime.now(timezone.utc)`；S:68 补 `Optional` import 或改 `dict | None`
- [ ] S:51/S:111 节首标注 "interface sketch — adapt to environment"
- [ ] S:105-106 enum 检查守卫缺失（§13.7 替换文本）
- [ ] Y:2 `pattern: mindset` → `process`
- [ ] 回归验证：`python check.py <workspace> <tool_log> <output>` 8 项 script 检查全部通过（PROC-06 的 `utc|utcnow|timezone` 与 NEG-03 的负向检查均不受 P1-3 影响）
- [ ] dossier 勘误回写：D:477-478 编号缺陷标记为已修复；D:1122 "tpl 模板编号断裂 ~18" 更新为已清零；058 条目总评维持 🟡 但理由更新为"description 已对齐、Scope/Workflow 已补"（修复验收后）
- [ ] 家族批量：以 058 为样板，对 23 个 tpl 系列成员执行 §13.6 P2-2 的 description 排查

### 13.10 附录 A：description 修改前后对照

**修改前（S:3）**：
```
Pack template (situacao/15-data-pipeline.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is building ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers, or batch processing jobs.
```

**修改后（§13.1）**：
```
Guides the design and operation of production-grade data pipelines: ETL/ELT ingestion, transformation flows, event streaming consumers, and batch processing, with source immutability, idempotent re-runs, schema evolution handling, validation gates, dead-letter queues, checkpointing, and backfill strategy. Use when the user is building ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers, or batch processing jobs.
```

**逐段影响**：

| 检查项 | 修改前 | 修改后 |
|--------|:----:|:----:|
| 第三人称（SP:54-58） | ✅ | ✅ |
| 触发短语 "Use when the user"（SP:63） | ✅ | ✅ |
| WHAT 与正文对齐（§4.1） | ❌ 零覆盖 | ✅ 7 原则逐条枚举 |
| 无模板书签（§4.1） | ❌ "Pack template (...)" | ✅ |
| 无填充语（§8.2） | ❌ "aligned with this context" | ✅ |
| ≤1024 字符（SP:14） | ✅ ~330 | ✅ ~400 |
| SCOPE-01 判定支撑（Y:7-13） | ⚠️ 仅 WHEN 子句 | ✅ WHAT+WHEN 双重支撑 |

### 13.11 附录 B：tpl-situacao 家族缺陷对照

| 家族成员 | 编号/粗体缺陷（2026-08-05 已修复） | description 通用文案 | 缺显式 Scope 节 |
|----------|:----:|:----:|:----:|
| 023-tpl-situacao-documentacao-tecnica | 已修复（D:225 记录） | ⚠️ 需排查 | ⚠️ |
| 029-tpl-situacao-deployment-devops | 已修复（D:270 记录） | ⚠️ 需排查 | ⚠️（DO NOT 覆盖） |
| 030-tpl-situacao-setup-inicial-projeto | 已修复（D:279 记录） | ⚠️ 需排查 | ⚠️ |
| 046-tpl-situacao-code-review-assistant | 已修复（D:390 记录） | ⚠️ 需排查 | ⚠️ |
| 058-tpl-situacao-data-pipeline | **已修复（本复评 §6.1 核验）** | **❌ 未修复（P0-1）** | ⚠️（DO NOT 覆盖） |
| 059-tpl-situacao-security-audit | 已修复（D:486 记录） | ⚠️ 需排查（主题尚匹配） | ⚠️ |
| 078-tpl-situacao-onboarding-novo-dev | 已修复（D:622 记录） | ⚠️ 需排查 | ✅（D:624 三节齐备） |
| 101/115/116/131/132/145/146/166-169 | 已修复（D:709/766/846/868/930 记录） | ⚠️ 需排查 | ⚠️ |

**家族结论**：编号断裂为同源缺陷、已随 2026-08-05 家族修复清零；description 通用文案（WHAT 子句与正文失配）与缺显式 Scope 节是家族**现存**的两大共性缺口。058 结构最完整，修复 058 后其 P0-1/P1-1 文本可直接作为家族批量修复模板。

### 13.12 附录 C：dossier 与旧版 REVIEW 勘误对照

| # | 原文 | 出处 | 勘误结论 |
|---|------|------|----------|
| 1 | "编号列表首项丢失（列表从 2 开始）" | D:477 | ❌ 已过期——当前 S:8 编号 1 完整（§6.1） |
| 2 | "开篇 'Immutability of source is sacred.**' 粗体标记断裂" | D:478 | ❌ 已过期——当前粗体闭合（§6.1） |
| 3 | "description 声称覆盖 'debugging, security and refactoring' 与实际数据管道内容不符" | D:477、R:3 | ✅ 维持——S:3 至今未改（§4.1） |
| 4 | "正文 191 行 ≤600" | D:480 | ✅ 与当前一致（wc 190 为末行无换行计数差） |
| 5 | "首条编号破损——粗体标记断裂" | R:3 | ❌ 已过期（同 #1/#2） |
| 6 | "🟡 **B−** (46/100)" | R:4 | ⚠️ 等级-分数错配：46/100 落 D 区间（§12.2）；本复评重算 84/100 → B |
| 7 | "tpl 模板编号断裂 ~18" | D:1122 | ⚠️ 经 2026-08-05 家族修复后应更新为已清零 |
| 8 | "按 Pattern 分类质量：mindset (35个) 🟡" | D:1193-1197 | ⚠️ 058 按 §13.5 改 `process` 后，mindset 组剔除 058（191 行/含代码模板更贴近 process 形态） |

### 13.13 附录 D：复评结论摘要

1. **定性更正**：058 的核心问题不是编号/粗体（已修复），而是 description WHAT 子句与正文的承诺断裂 + 两个结构性缺口（无显式 Scope/Workflow 节）。
2. **等级**：🟡 B（84/100）；修复后预估 ≈90 → B+ / A−。
3. **强项保留**：五层互证内部一致性、20/20 SCORING 对齐、评估链路健康（SCORING/check.py 同口径）、输出模板具体、人机感克制——修复后完全具备 A 档资质。
4. **阻断项**：P0-1 description 重写（唯一必须项）；P1-1/P1-2 补两节；其余为建议与可选。
5. **对 corpus 层面的建议**：058 可作 tpl-situacao 家族 description 批量修复的样板（§13.6）；dossier D:477-478/D:1122 勘误随家族修复同步更新。

---

**变更记录**
- 2026-08-06：深度复评（v2，覆盖 4 行 stub）。核验编号/粗体缺陷已随家族修复清除（§6.1）；确认 description WHAT 断裂为现存核心缺陷（§4.1）；确认 SCORING 20/20 与 check.py 8/8 完全对齐（§5、§10）；重算评分为 🟡 B（84/100）并勘误旧版 B−（46/100）的等级-分数错配（§11.4、§13.12）；给出 P0-1 description 全文替换、P1-1/P1-2 两节完整文本与验收清单（§13）。
