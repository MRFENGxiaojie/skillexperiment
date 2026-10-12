# REVIEW: 228-enterprise-artifact-search

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 多跳证据检索 + 结构化实体提取（子代理委托型检索 skill）
**Body 行数**: 248 行（SKILL.md，共 252 行）
**参考文件数**: 0（无 references/、scripts/ 子目录；配套文件仅 SCORING.yaml 与 check.py）
**已有 REVIEW**: 无（本次为首次审查）

---

## 1. 目录全量清单

```
228-enterprise-artifact-search/
├── SKILL.md      (252 行)
├── SCORING.yaml  (151 行)
└── check.py      (73 行)
```

| 文件 | 行数 | 说明 |
|------|:----:|------|
| SKILL.md | 252 | 主 skill 定义：委托式多跳检索 + 实体提取流程 |
| SCORING.yaml | 151 | 16 项测评标准（3 scope + 5 process + 2 decision + 3 output + 3 negative + 3 critical failures） |
| check.py | 73 | 脚本化检查（仅实现 OUT-01、OUT-03 两项，其余 14 项交 LLM judge） |

**结构特点**: 该 skill 无任何参考文件，全部逻辑（6 步核心流程 + 输出格式 + 推荐类型）内联在 SKILL.md 正文中。这是一个"委托式" skill：主 agent 触发后不亲自执行检索，而是通过 `Task(subagent_type="enterprise-artifact-search")` 将检索任务下发给轻量子代理，正文的 Core Procedure 实际上是写给子代理的指令。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
```
name: enterprise-artifact-search
```
- 匹配目录名 `228-enterprise-artifact-search` 的 slug 部分：✅
- 全小写 + 连字符：✅
- ≤64 字符：✅（26 字符）

### 2.2 description（逐句分析）

原文（500 字符，≤1024 上限）：
```
Multi-hop evidence search + structured extraction over enterprise artifact
datasets (docs/chats/meetings/PRs/URLs). Strong disambiguation to prevent
cross-product leakage; returns JSON-ready entities plus evidence pointers.
Use when the user asks questions whose answers must be retrieved from
enterprise documents, chat logs, meeting transcripts, PRs, or URLs, needs
structured entity extraction with evidence pointers, or wants multi-hop
evidence gathering without loading large files into context.
```

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "Multi-hop evidence search + structured extraction over enterprise artifact datasets (docs/chats/meetings/PRs/URLs)." | WHAT | ✅ 明确功能与数据域 |
| "Strong disambiguation to prevent cross-product leakage; returns JSON-ready entities plus evidence pointers." | WHAT（展开） | ✅ 描述核心价值（防串产品）与输出形态 |
| "Use when the user asks questions whose answers must be retrieved from enterprise documents, chat logs, meeting transcripts, PRs, or URLs, needs structured entity extraction with evidence pointers, or wants multi-hop evidence gathering without loading large files into context." | WHEN | ✅ 三个触发场景，含标准触发短语 |

**第三人称检查**: 全文无第一/第二人称代词。✅

**触发短语**: 含 "Use when the user" 标准信号，且落在句首位置，满足 SKILL-SPEC §2.4。✅

**字符数**: 500 字符 ≤1024。✅

**关键词覆盖**: docs/chats/meetings/PRs/URLs、multi-hop、evidence pointers、entity extraction、cross-product——领域词充分。✅

**小瑕疵**: 末尾 "without loading large files into context" 属于实现收益（上下文节省）的叙述，而非触发场景，语义上可并入 WHAT 段；但不构成违规，仅表述冗余。

### 2.3 其他 frontmatter 字段
仅 `name`、`description` 两个字段。均为 `_shared/SKILL-SPEC.md` 允许的字段。**无任何禁止字段**（无 metadata/license/version/trigger/tools 等）。✅

### 2.4 Frontmatter 语法
YAML 分隔符 `---` 配对正确（L1、L4），无缩进错误，description 为单行双引号字符串，无未转义特殊字符。✅

**Frontmatter 结论**: 完全合规，无问题。

---

## 3. Body 逐段结构分析

### 标题与前导说明 (L6-15)
```
# Enterprise Artifact Search Skill (Robust)
```
- 标题带 "(Robust)" 后缀，并有一段 "This version adds two critical upgrades: 1) Product grounding & anti-distractor filtering... 2) Key reviewer extraction rules..."——这是**版本迭代痕迹**，属于典型的评测/开发脚手架语言（详见第 8 节）。
- 前导说明交代了委托式架构（"delegates ... to a lightweight subagent, keeping the main agent's context lean"）。

### ## When to Invoke This Skill (L18-27)
5 条触发条件：多跳证据、必须从 artifact 检索、跨类型证据分散、需要精确指针、保持上下文精简。与 description 的 WHEN 部分一一对应。✅

### ## Why Use This Skill? (L30-42)
"Without this skill / With this skill" 对比段。内容合理（防漏跨链、防"first hit wins"），但措辞偏评测报告风格（"common failure: wrong product"），且 "Typical context savings: 70–95%" 是无出处数据。

### ## Invocation (L45-63)
委托协议模板：
```python
Task(subagent_type="enterprise-artifact-search", prompt="""
Dataset root: /root/DATA
Question: <paste the question verbatim>
...
""")
```
- 明确了本 skill 的使用方式：主 agent 构造 Task 调用，子代理类型即本 skill 名。
- **注意**: 模板中硬编码 `Dataset root: /root/DATA`，而 Core Procedure Step 1 又直接写死 `/root/DATA/products/<Product>.json`（详见第 4 节问题 2）。

### ## Core Procedure (Must Follow) (L67-167)
7 个子节（Step 0–6），构成完整流程链：
- Step 0 — Parse intent + target product (L69-75)
- Step 1 — Build candidate set（宽召回再过滤）(L78-89)
- Step 2 — HARD Product Grounding（2 信号防干扰门）(L92-106)
- Step 3 — Select correct report version（latest→final→date→引用频率）(L109-118)
- Step 4 — Extract author(s)（doc→PR→slack 优先级）(L121-130)
- Step 5 — Extract key reviewers（证据制，不把参会者当评审人）(L133-158)
- Step 6 — Validate IDs & de-duplicate (L161-166)

### ## Output Format (Strict, JSON-ready) (L169-203)
1) Final Answer Object（5 字段 JSON）；2) Evidence Map（artifact_type + artifact_id + snippet）。均给出完整 JSON 示例。✅

### ## Recommendation Types (L206-212)
USE_EVIDENCE / NEED_MORE_SEARCH / AMBIGUOUS 三选一。**注意**：推荐类型未纳入 Final Answer Object 的 JSON schema（详见第 4 节问题 4）。

### ## Common Failure Modes (L215-232)
4 类失败模式（跨产品泄漏、评审人过度包含、版本选择错误、schema 不匹配），均与对应 Step 的修复手段一一对应。✅

### ## Mini Example (L235-244)
"Your case" 标题下的示例（CoachForce Market Research Report）。**"(Your case)" 字样是某次具体评测实例的残留**，评测痕迹明显。

### ## Do NOT Invoke When (L248-251)
2 条不触发条件（单文件一跳查询、范围无歧义）。**该节即本 skill 的 Scope/Limitations 节**，满足 SKILL-SPEC §3.1 的三必需节要求，但篇幅偏薄（仅 2 条，未覆盖"不做什么"的完整边界，如：不做报告写作、不做跨数据集泛化推理等）。

### Body 结构结论
流程型 skill 的三必需节（Workflow/Core Procedure、Output Format、Scope/Do NOT Invoke）**全部齐备**，结构完整。主要问题集中在评测脚手架残留与少量内部不一致。

---

## 4. 逻辑一致性深度审查

### 4.1 Step 0-6 主链一致性 —— 严谨，无矛盾

| 环节 | 输出 | 下游消费 | 判定 |
|------|------|---------|:----:|
| Step 0 意图解析 | target product + 实体类型 + artifact 类型 | Step 1 搜索方向 | ✅ |
| Step 1 候选集 | 宽召回候选 | Step 2 过滤 | ✅ |
| Step 2 产品接地 | VALID / DISTRACTOR | Step 3 版本选择 | ✅ |
| Step 3 版本选择 | 最终 report_doc_id | Step 4/5 提取锚点 | ✅ |
| Step 4 作者提取 | author_employee_ids | Step 6 校验 | ✅ |
| Step 5 评审人提取 | key_reviewer_employee_ids | Step 6 校验 | ✅ |
| Step 6 校验去重 | all_employee_ids_union | Output Format | ✅ |

- Step 0 "产品名缺失时仅凭 artifact 明确支持才推断，否则 AMBIGUOUS" 与 Recommendation Types 的 AMBIGUOUS 类型一致。✅
- Step 2 的 reject rule（内容反复出现别的产品名且无目标产品接地 → DISTRACTOR）与 Step 3 "仅从 VALID 报告中选择" 闭环。✅
- Step 5 Tier 3 的排除规则（纯点赞不算；作者排除，除非题目明确要求）与 NEG-02/NEG-03 一致。✅
- Step 6 去重顺序（作者在前、评审人在后）直接产出 `all_employee_ids_union` 的语义。✅

**结论**: 主流程逻辑链条严密，未发现步骤间的矛盾或断链。这是该 skill 最大的优点。

### 4.2 问题 1 — 执行主体模糊：主 agent 还是子代理执行 Core Procedure？（轻微）

SKILL.md 开篇声明"delegates ... to a lightweight subagent"，Invocation 节也明确要求用 `Task(subagent_type="enterprise-artifact-search")` 委托。但正文 6 步 Core Procedure 是祈使句写给"执行者"的，未明确声明"主 agent 不得亲自执行 Step 0-6"。若运行环境未将本 skill 注册为可用 subagent 类型，主 agent 将面临两难：亲自执行则违背委托设计，委托则 `Task()` 调用可能在运行时失败（详见第 9 节）。应补一句明确的责任划分。

### 4.3 问题 2 — `/root/DATA` 硬编码与 Invocation 参数化不一致（轻微）

- Invocation 模板（L51）将数据集根目录参数化为 `Dataset root: /root/DATA`，暗示真实环境中根目录由调用方提供。
- 但 Step 1（L81）直接硬编码 `Search in this order: 1) Product artifact file(s): /root/DATA/products/<Product>.json`。
- 若实际数据集根目录不是 `/root/DATA`，子代理会先找错路径。应改为 `<Dataset root>/products/<Product>.json`，与 Invocation 的参数化保持一致。

### 4.4 问题 3 — "If the benchmark expects" 直呼评测框架（中等，评测痕迹核心项）

Step 5 的 Critical rule（L157）写道：
> If the benchmark expects "key reviewers" to be "the people who reviewed in the review meeting", then your evidence must cite the transcript lines/turns that contain their suggestions.

这句话把**评测基准的期望**作为指令依据写入生产 skill。其意图（用转录行证明评审贡献）本身合理，但"benchmark expects"的措辞是评测脚手架泄漏，运行中的 agent 不应知道自己在接受评测。应改为中性表述（如 "If the review meeting is the designated review venue, your evidence must cite..."）。

### 4.5 问题 4 — Recommendation Types 未并入输出 schema（轻微）

Output Format 的 Final Answer Object 只有 5 个字段，没有 `recommendation` 字段；Recommendation Types 节（L206-212）要求"Return one of"，但未说明返回载体（JSON 内？还是 JSON 外单独一行？）。SCORING 的 DEC-01 检查的是"是否返回了与证据一致的推荐类型"，载体含糊会导致 agent 输出格式漂移。建议在 JSON schema 中增加 `"recommendation": "USE_EVIDENCE | NEED_MORE_SEARCH | AMBIGUOUS"` 字段。

### 4.6 问题 5 — 接地信号独立性未定义（轻微）

Step 2 要求"at least 2 **independent** grounding signals"，但信号 A（位于产品容器内）与信号 D（id/路径含产品标识）在典型数据集中往往同源于同一个 artifact 路径：一份位于 `products/CoachForce.json` 内的报告，其 doc_id 若含 "CoachForce"，A 与 D 会同时满足，但二者并非真正独立。建议明确"独立性"的定义（如：信号不得源于同一字段/同一路径）。

### 4.7 其他一致性核对
- "70–95% context savings"（L41）无测算依据，属夸大式声称。🔸
- Step 1 的候选匹配条件（title 含 "Market Research Report" 等）与 Mini Example 一致。✅
- "Common Failure Modes" 4 条与 Step 2/3/5/Output Format 一一对应，无错配。✅

**逻辑结论**: 主链逻辑严谨（该 skill 的核心价值），但存在 1 项中等（评测措辞泄漏）与 4 项轻微问题。

---

## 5. 参考文件内容级审查

本 skill **无 references/、scripts/ 子目录**，SKILL.md 也未引用任何外部文件（这是合理的：全部流程逻辑内联）。因此本节改为对两个配套文件（SCORING.yaml、check.py）的内容级审查。

### 5.1 SCORING.yaml（151 行）

结构：`pattern: process`、`total_items: 16`、5 类共 16 项 criteria + 3 项 critical_failures。

**total_items 一致性**: SCOPE 3 + PROC 5 + DEC 2 + OUT 3 + NEG 3 = 16，与 `total_items: 16` 精确一致。✅

**类别分布**: scope 3 项（触发判定）、process 5 项（流程执行）、decision 2 项、output 3 项、negative 3 项。对"过程型" skill 而言，process 占 5/16 权重合理。

**judge 分布**: llm 14 项 + script 2 项（OUT-01、OUT-03）。该 skill 的核心行为（接地推理、评审人证据判定、去重顺序）确实无法脚本化，LLM judge 主导是合理的。但 2 项脚本检查恰好覆盖了最容易出错的两项输出契约，选点正确。

**逐项与 SKILL.md 映射**（详见第 10 节交叉参考表）: 16 项 criteria 均能在 SKILL.md 中找到对应的步骤/节，映射完整度极高。

**发现的问题**:
1. **OUT-01 检查模式缺 `report_doc_id`**（L92-96）: 描述列出的 5 个字段包括 `report_doc_id`，但 `check.pattern` 的正则只含 `target_product|author_employee_ids|key_reviewer_employee_ids|all_employee_ids_union` 四个。描述与检查不一致。
2. **CF-02 无对应的 NEG 项**（L144-146）: 关键失败 "equates meeting participants with key reviewers" 在 16 项 criteria 中没有专属的 negative 项（NEG-02 是纯点赞、NEG-03 是作者包含），只能靠 PROC-05 的 llm judge 间接覆盖。建议补一条 NEG-04。
3. **SCOPE-02 的 judge 提问措辞自相矛盾**（L20）: 问题先问"对于一跳琐碎查询，agent 是否避免调用本 skill？"，紧接着又指示 "Answer yes if the task was genuinely multi-hop"——若任务真的是多跳，则"避免调用"的前提不成立，法官会无所适从。应改为判断题面任务类型，而非让法官双向作答。

### 5.2 check.py（73 行）

**导入**: 从 `_shared/checker.py` 导入了 18 个函数，实际仅使用 `output_contains` 与 `set_tool_log_path/set_agent_output`，其余 15 个（file_*、json_*、timestamp_*、tool_log_*）均未使用——模板 boilerplate，无害但可清理。

**检查实现**: `check()` 仅返回 OUT-01、OUT-03 两项，与 SCORING.yaml 的 script judge 标记一致。✅

**发现的问题（重要）**:

4. **`set_agent_output` 被路径字符串覆盖（输出检查缺陷）** — check.py L26-27:
```python
set_tool_log_path(tool_log)
set_agent_output(agent_output)
```
   `check()` 的第三个参数是 `agent_output`（按 docstring L2 约定为**路径**）。main()（L61-63）已先读取文件内容并 `set_agent_output(f.read())`，但 `check()` 内部紧接着又用**路径字符串**调用 `set_agent_output(agent_output)`，把已加载的内容覆盖为路径。此后 `output_contains()` 检查的是**路径字符串**而非输出内容 → OUT-01/OUT-03 在正常运行路径下几乎必然返回 False（假阴性）。
   - **对比证据**: 语料库 322 个 check.py 中已有 200 个修复了此问题（如 002-software-manual/check.py L22-29 的写法：`_is_path = os.path.exists(agent_output); if not _is_path: set_agent_output(agent_output)`，并注释 "main() has already loaded its content"）。228 属于尚未修复的 122 个之一。
   - 若 runner 改为把输出**内容**直接作为第三参数传入，则 `os.path.exists(超长内容)` 在 Windows 上会抛 OSError 使 main() 崩溃——两条调用路径必有一条出问题。
   - **修复方向**: 采用 002 的 `_is_path` 防护写法（详见第 13 节修复 1）。

**可执行性补充建议（非缺陷）**:
- SCOPE-01 要求"委托给 enterprise-artifact-search 子代理"，可用 `tool_log_contains("Task")` 做部分脚本化验证（当前完全依赖 llm judge）。
- PROC-01 要求"按顺序构建候选集"，可用 `tool_log_contains("Glob|Grep")` 做弱验证。

### 5.3 参考文件结论
SCORING.yaml 与 SKILL.md 的映射质量高（16/16 全部可溯源），是本批 skill 中少见的完整对应；check.py 存在 1 项会直接破坏两项脚本检查的缺陷，必须修复。

---

## 6. 语法与格式质量（逐问题列举）

**整体**: 英文书写规范、术语一致（doc_id/message_id/meeting_id/pr_id、eid_*、grounding、DISTRACTOR），未发现拼写错误或病句。代码块与 JSON 示例格式正确（Output Format 的 JSON 可解析）。

逐问题列举：

| # | 位置 | 问题 | 严重度 |
|---|------|------|:----:|
| 1 | L6 标题 | `# Enterprise Artifact Search Skill (Robust)` — "(Robust)" 是版本标记残留，非正式标题组成部分 | 🟡 |
| 2 | L12-15 | "This version adds two critical upgrades: 1) ... 2) ..." — 变更日志口吻出现在正文开头，属开发脚手架 | 🟡 |
| 3 | L235 | `## Mini Example (Your case)` — "(Your case)" 是具体评测实例残留 | 🟡 |
| 4 | L157 | "If the benchmark expects..." — 评测措辞（详见 4.4） | 🟡 |
| 5 | L105 | "Why: Benchmarks intentionally insert same doc type across products" — 同上，评测动机解释直接入文 | 🟡 |
| 6 | L41 | "Typical context savings: 70–95%" — 无依据的数值声称 | 🟢 |
| 7 | L81 | `/root/DATA` 硬编码路径与 Invocation 参数化不一致 | 🟡 |
| 8 | L55 | "Avoid oracle/label fields (ground_truth, gold answers)" — "oracle/label" 是评测数据集术语，普通用户任务中不存在"金答案"，措辞暴露评测语境 | 🟡 |

**格式**: 标题层级（##/###）规范；Step 编号 0-6 连续无重复；列表与表格渲染无破损；Markdown 语法无误。✅

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

### 7.1 Compliance Checklist

| 检查项 | 结果 | 证据 |
|--------|:----:|------|
| name: 小写+连字符，≤64 字符，匹配目录 | ✅ | `enterprise-artifact-search` |
| description: 第三人称，WHAT+WHEN+KEYWORDS，≤1024 字符 | ✅ | 500 字符，三段式结构完整 |
| description: 无祈使/第一/第二人称开头 | ✅ | 以名词短语开头 |
| description: 无内嵌跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 内容 |
| description: 至少一个触发信号短语 | ✅ | "Use when the user" (L3) |
| frontmatter: 无允许列表外字段 | ✅ | 仅 name + description |
| body: ≤600 行 | ✅ | 248 行 |
| body: 有 workflow/process 节 | ✅ | ## Core Procedure (L67) |
| body: 有 output format 节 | ✅ | ## Output Format (L169) |
| body: 有 scope/limitations 节 | ✅ | ## Do NOT Invoke When (L248) |
| body: 无跨 skill 文件引用（../other-skill/） | ✅ | 无任何 ../ 路径；唯一路径引用是数据集路径 /root/DATA |
| 目录: NNN-kebab-case，无空格/大写 | ✅ | 228-enterprise-artifact-search |

### 7.2 合规性结论
**12/12 全项通过**，是语料库中合规度最高的形态之一（三必需节齐备 + 无禁止字段 + 无跨引用）。唯一可挑剔处：
- Scope 节以 "Do NOT Invoke When" 形式存在，仅 2 条，未声明该 skill **不**覆盖的行为（如报告写作、结果综述、跨数据集泛化），边界声明偏薄（建议补 2-3 条，见第 13 节）。
- §3.3 的"文件引用用相对路径"不适用（无文件引用），但 `/root/DATA` 绝对路径作为**数据路径**而非文件引用，不属于违规，仅属可移植性问题。

---

## 8. 人机感评估

### 8.1 语气与风格
- **无 emoji、无填充语**：全文纯指令式专业英文，与 skill 的"子代理操作手册"定位匹配。✅
- **无第一/第二人称面向用户的话术**：body 全部面向执行者（agent/subagent），不出现"我会帮您"等客服腔。✅
- **门控与防御措辞到位**："MUST enforce product grounding"、"Reject rule (very important)"、"Critical rule" 等强约束表达清晰但不喊叫。✅

### 8.2 主要问题：评测痕迹过重（dossier 已点名，本次确认并定位）

该 skill 的人机感问题不在语气，而在**面向评测的脚手架语言大面积残留**，共 6 处：

| # | 位置 | 残留内容 | 问题本质 |
|---|------|---------|---------|
| 1 | L6 | "(Robust)" 标题后缀 | 版本迭代标记 |
| 2 | L12-15 | "This version adds two critical upgrades" | 变更日志 |
| 3 | L41 | "Typical context savings: 70–95%" | 评测风格量化声称 |
| 4 | L105 | "Why: Benchmarks intentionally insert same doc type across products" | 直接解释评测设计动机 |
| 5 | L157 | "If the benchmark expects ... then ..." | 以评测期望为指令依据 |
| 6 | L235 | "Mini Example (Your case)" | 具体实例残留 |

其中 4、5 两项最刺眼：生产 skill 的正文中出现 "Benchmarks intentionally insert..." 和 "If the benchmark expects..."，等于告诉 agent"你在被评测"。即使 SkillIF 本身就是评测语料，正式化（规范化）后的 skill 也不应保留这类措辞——这正是本项目"规范化"工作要清除的对象。

### 8.3 双重受众问题
- Invocation 节（L45-63）面向**主 agent**（教你如何委托）；
- Core Procedure 节（L67-167）面向**子代理**（教你如何执行）；
- 同一文件内两个受众未做显式分隔（如"以下内容供子代理执行"的标注），读起来像是同一份指令被两方同时执行。属结构设计问题而非语气问题，建议加一句受众标注（见第 13 节）。

### 8.4 人机感结论
语气本身专业克制，无 emoji、无废话；扣分集中在评测痕迹（6 处）与双重受众未标注。修复后可达语料库中上等水平。

---

## 9. 可执行性评估

### 9.1 步骤可执行性 —— 主体良好

| 评估维度 | 结果 |
|---------|:----:|
| 步骤颗粒度（子代理可直接照做） | ✅ 6 步 + 每步明确优先级/规则 |
| 决策点明确性 | ✅ 2 信号接地门、4 级版本优先级、3 层评审人证据分级 |
| 输出契约明确性 | ✅ 双 JSON schema 示例 |
| 失败处理 | ✅ NEED_MORE_SEARCH / AMBIGUOUS 回退路径 |
| 约束的可验证性 | ✅ "eid_..." 模式、目录校验、去重顺序均有硬规则 |

子代理拿到 body 即可执行完整的"解析→召回→接地→选版→提人→校验→输出"流程，这是该 skill 可执行性的强项。

### 9.2 可执行性风险点

**风险 1（中等）— 对 `Task(subagent_type="enterprise-artifact-search")` 的环境依赖**：
- Invocation 要求主 agent 以本 skill 名为 subagent_type 调用 Task。在真实 Claude Code 环境中，subagent_type 必须对应已注册的 agent 定义（`.claude/agents/*.md`），而本 skill 目录内**没有任何 agent 定义文件**。
- 该模式仅在 SkillIF 评测 harness（skill 名即 subagent 类型）下成立。若脱离 harness 使用，Task 调用会失败。
- 缓解建议：在 Invocation 节注明"前提：运行环境已将本 skill 注册为可用 subagent 类型；否则主 agent 应携带本 body 作为 Task prompt"。

**风险 2（轻微）— `/root/DATA` 硬编码**：见第 4 节问题 2，子代理在非基准环境会先找错路径。

**风险 3（重要）— check.py 输出检查缺陷**：`set_agent_output` 被路径覆盖，OUT-01/OUT-03 在标准调用方式下会假阴性（详见 5.2 问题 4）。此缺陷不直接影响 skill 运行，但直接破坏**评测结果的有效性**——对本项目（测评 Agent 对 skill 的遵从能力）而言，评测脚本自身出错会导致该 skill 的合规分失真。

**风险 4（轻微）— 脚本覆盖不足**：16 项中 14 项靠 LLM judge。judge 间一致性依赖提问质量，其中 SCOPE-02 的提问措辞有自相矛盾风险（见 5.1 问题 3），可能引入评分噪声。

### 9.3 可执行性结论
子代理执行路径清晰完整（强项），但存在 1 项评测链路缺陷（风险 3）与 1 项环境依赖未声明（风险 1），修复成本低、收益明确。

---

## 10. SCORING.yaml 交叉参考

### 10.1 16 项 criteria 与 SKILL.md 逐项映射

| ID | 类别 | SCORING 描述要点 | SKILL.md 对应 | 一致性 |
|----|------|------------------|---------------|:----:|
| SCOPE-01 | scope | 识别为多跳检索任务并委托子代理 | When to Invoke #1-5 + Invocation (L18-63) | ✅ |
| SCOPE-02 | scope | 琐碎一跳查询不调用 | Do NOT Invoke When (L248-251) | ✅ 措辞有瑕疵* |
| SCOPE-03 | scope | Step 0 先解析目标产品/实体/artifact 类型 | Step 0 (L69-75) | ✅ |
| PROC-01 | process | 候选集按 产品文件→全局扫→链路 顺序构建 | Step 1 (L78-89) | ✅ |
| PROC-02 | process | ≥2 个独立接地信号才接受候选 | Step 2 (L92-106) | ✅ |
| PROC-03 | process | 版本选择优先级 latest→final→date→引用频率 | Step 3 (L109-118) | ✅ |
| PROC-04 | process | 作者优先级 doc→PR→slack | Step 4 (L121-130) | ✅ |
| PROC-05 | process | 评审人证据制，非参会者名单 | Step 5 (L133-158) | ✅ |
| DEC-01 | decision | 返回与证据一致的推荐类型 | Recommendation Types (L206-212) | ✅ 载体未定义** |
| DEC-02 | decision | 姓名→ID 仅在有接地证据后解析 | Step 4 末段 + Step 6 (L127-130, L161-166) | ✅ |
| OUT-01 | output | 5 字段 JSON 对象 | Output Format #1 (L173-182) | ⚠️ 正则缺 report_doc_id*** |
| OUT-02 | output | 证据地图含指针+片段 | Output Format #2 (L184-202) | ✅ |
| OUT-03 | output | eid_ 模式、去重保序 | Step 6 + Output Format (L161-166) | ✅ 去重/保序无法脚本验证 |
| NEG-01 | negative | 拒绝跨产品干扰项 | Step 2 reject rule (L102-105) | ✅ |
| NEG-02 | negative | 纯点赞不算评审证据 | Step 5 Tier 3 (L146-150) | ✅ |
| NEG-03 | negative | 作者不混入评审人 | Step 5 Tier 3 (L149-151) | ✅ |

* SCOPE-02 judge 提问含 "Answer yes if the task was genuinely multi-hop" 自相矛盾指示。
** DEC-01 的推荐类型未纳入 Final Answer Object schema，输出载体含糊。
*** OUT-01 描述含 `report_doc_id`，但 check.pattern 正则不含。

### 10.2 critical_failures 对照

| ID | 描述 | 对应机制 | 判定 |
|----|------|---------|:----:|
| CF-01 | 跨产品泄漏（最常见失败） | Step 2 双信号接地 + NEG-01 | ✅ 覆盖充分 |
| CF-02 | 参会者=评审人 | Step 5 Critical rule + PROC-05 | ⚠️ 无专属 NEG 项（见 5.1 问题 2） |
| CF-03 | 无证据指针裸返回 | Output Format #2 + OUT-02 | ✅ |

### 10.3 交叉参考结论
映射完整度 16/16，是本语料库中 SCORING.yaml 与 SKILL.md 对应关系最好的 skill 之一；需要修正的为 3 处小瑕疵（SCOPE-02 措辞、OUT-01 正则、CF-02 缺 NEG 项）。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 中 228 的记录（Batch 226-250）：
> - **逻辑**: "228 多跳检索→产品锚定→版本选择逻辑严谨"
> - **人机感**: "228 评测痕迹过重"
> - **合规**: "228/230 基本合规"
> - **总评**: "🟢 全组法律/合规类均为高质量"

**本次验证结果**:

| dossier 记录 | 验证 | 结论 |
|-------------|:----:|------|
| 逻辑严谨 | ✅ | 确认：Step 0-6 主链无矛盾（见第 4 节 4.1） |
| 评测痕迹过重 | ✅ | 确认：6 处残留（见第 8 节 8.2），其中 L105/L157 两处最重 |
| 基本合规 | ✅ | 确认：12/12 项规范检查通过（见第 7 节） |
| 🟢 高质量 | 🔄 | 主体质量确属上乘，但本次深度审查发现 dossier 未记录的 4 项新问题（见下） |

**dossier 未记录的本次新发现**:

1. **check.py 输出检查缺陷**（`set_agent_output` 被路径覆盖 → OUT-01/OUT-03 假阴性）—— 本语料库 200/322 已修复、228 未修复（见 5.2 问题 4）。
2. **Task 子代理类型环境依赖未声明**（skill 目录无 agent 定义文件，脱离 harness 会运行失败，见 9.2 风险 1）。
3. **OUT-01 检查正则缺 `report_doc_id`**、CF-02 无专属 NEG 项、SCOPE-02 judge 措辞矛盾（见 5.1）。
4. **`/root/DATA` 硬编码与 Invocation 参数化不一致**（见 4.3）。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | description 三段式完整、第三人称、含触发词；仅末尾实现收益叙述轻微冗余 |
| Body 结构完整 | 8/10 | 10% | 0.80 | 三必需节齐备；Scope 仅 2 条偏薄、Recommendation 未入输出 schema |
| 逻辑一致性 | 8/10 | 20% | 1.60 | Step 0-6 主链严谨无矛盾；4 项轻微不一致（硬编码路径、执行主体模糊、独立性未定义、schema 载体） |
| 参考完整性 | 8/10 | 15% | 1.20 | 无参考文件（合理内联）；SCORING 16/16 可溯源；但 check.py 存在输出检查缺陷 |
| 语法格式 | 9/10 | 10% | 0.90 | 英文规范无错字，JSON/代码块正确；扣分在 6 处脚手架措辞 |
| 规范合规 | 9/10 | 15% | 1.35 | 12/12 全项通过，语料库上等；Scope 节篇幅偏薄为唯一软肋 |
| 人机感 | 6/10 | 10% | 0.60 | 语气专业无 emoji；但评测痕迹 6 处、"Your case"/"benchmark expects" 直白泄漏 |
| 可执行性 | 7/10 | 10% | 0.70 | 子代理步骤可直接执行；Task 类型依赖未声明 + check.py 假阴性风险 |
| **加权总分** | | | **80.5/100** | |

### 12.2 评级

🟡 **B**（80/100）— 逻辑严谨、规范全合规、SCORING 映射完整的上乘 skill；被"评测痕迹过重"与 check.py 输出检查缺陷拖累，两者修复后可达 🟢 A 级。

> 注：dossier 评级为 🟢（"基本合规、全组高质量"）。本次深度审查阅读了全部 3 个文件并对照语料库 200/322 个已修复 check.py 模式，新增发现 1 项评测链路缺陷与 6 处评测痕迹，故评级略降为 🟡。若按"内容与规范"单维度衡量仍属 🟢 上等。

---

## 13. 修复建议（按优先级分层）

### 🔴 必修复缺陷（评测链路，1 项）

**1. 修复 check.py 的 `set_agent_output` 路径覆盖缺陷**（check.py L26-27）
- 现状：`check()` 内无条件执行 `set_agent_output(agent_output)`，把 main() 已加载的输出内容覆盖为路径字符串，导致 OUT-01/OUT-03 假阴性。
- 修复方向：采用语料库已验证模式（002-software-manual/check.py L22-29）：
```python
set_tool_log_path(tool_log)
# If the agent output argument is a file path, main() has already loaded
# its content; set directly only when the argument is the raw text.
try:
    _is_path = os.path.exists(agent_output)
except (OSError, ValueError):
    _is_path = False
if not _is_path:
    set_agent_output(agent_output)
```
- 不修复后果：该 skill 的两项脚本化检查（OUT-01/OUT-03）在标准 runner 调用方式下恒为 False，评测分数失真。

### 🟡 重要修复（评测痕迹清理，建议一次完成）

**2. 删除/改写 6 处评测脚手架措辞**（SKILL.md）
- L6：标题去掉 "(Robust)" → `# Enterprise Artifact Search Skill`
- L12-15：删除 "This version adds two critical upgrades" 段落，改为中性能力描述（"The skill enforces product grounding and evidence-based reviewer extraction."）或将之移到文末 `## Metadata` 节
- L41："Typical context savings: 70–95%" → 删除或改为定性表述（"keeps the main agent's context lean"）
- L105："Why: Benchmarks intentionally insert same doc type across products" → 改为中性原理（"Reason: reports for different products can share document types and co-occur in the same file; first-hit selection is unreliable."）
- L157："If the benchmark expects ..." → 改为中性表述（"If the review meeting is the designated review venue, cite the transcript lines containing reviewers' suggestions."）
- L235：`## Mini Example (Your case)` → `## Example`

**3. 统一数据集根目录参数化**（SKILL.md L81）
- `/root/DATA/products/<Product>.json` → `<Dataset root>/products/<Product>.json`，与 Invocation 模板的 `Dataset root:` 参数保持一致。

**4. 明确执行主体分工**（SKILL.md Invocation 节）
- 在 Invocation 节增加一句："If the environment does not provide an `enterprise-artifact-search` subagent, the main agent MUST attach this skill's Core Procedure as the Task prompt and delegate only the search execution."——消除主 agent/子代理双重受众歧义，并为脱离 harness 的运行提供降级路径。

**5. 将 Recommendation 纳入输出 schema**（SKILL.md L173-182）
- Final Answer Object 增加第 6 个字段 `"recommendation": "USE_EVIDENCE | NEED_MORE_SEARCH | AMBIGUOUS"`，消除 DEC-01 的输出载体歧义。

**6. 明确接地信号独立性定义**（SKILL.md L93）
- 在 Step 2 补充："Signals must originate from distinct sources (e.g., container location, content text, channel/meeting series, id path) — do not count two signals derived from the same artifact path."

### 🟢 优化建议（锦上添花）

**7. 补强 Scope 节**（SKILL.md L248-251）
- 增加不适用场景：报告**撰写/综述**任务、需要**人工阅读判断**的文档分析、数据集**外**的知识检索。

**8. SCORING.yaml 三处小修**
- OUT-01 正则补 `report_doc_id`；
- 新增 NEG-04："Agent does not count meeting participants as reviewers without feedback evidence"（与 CF-02 对应）；
- SCOPE-02 judge 提问删除 "Answer yes if the task was genuinely multi-hop"，改为中性的任务类型判断题面。

**9. check.py 增加弱脚本化检查**
- `SCOPE-01` 部分脚本化：`tool_log_contains("Task")` 验证委托动作发生（若 harness 的 tool_log 记录 Task 调用）；
- `PROC-01` 弱验证：`tool_log_contains("Glob|Grep")` 验证搜索动作。
- 清理 15 个未使用的导入（可选）。

**10. 删除 "Avoid oracle/label fields (ground_truth, gold answers)" 约束**（SKILL.md L55）
- 该约束是评测语料的防泄漏规则，对真实用户任务无意义且暴露评测语境；如 harness 需要保留，应移至评测侧而非 skill 正文。

### 修复工作量估计
- 预计修改文件数：3（SKILL.md + SCORING.yaml + check.py）
- 预计新增行数：~25-35 行（check.py 防护 + schema 字段 + Scope 补充）
- 预计删除/改写行数：~15 行（评测痕迹清理）
- 优先级排序：修复 1（评测链路）→ 修复 2-6（正文质量）→ 优化 7-10

---

## 变更记录
- 2026-08-06: 首次深度审查。阅读全部 3 个文件（SKILL.md 252 行 + SCORING.yaml 151 行 + check.py 73 行），并对照 `_shared/checker.py`（351 行）与 200 个已修复的同类 check.py 验证了 check.py 缺陷。总评 🟡 B（80/100），发现 1 项必修复评测链路缺陷、6 处评测痕迹、3 处 SCORING 小瑕疵。

---

## 附录: 审查过程记录
- 读取文件数：3（本 skill 全部文件）+ 2 个对照文件（`_shared/checker.py`、`001-skill-tuning/REVIEW.md` 格式基准）+ 语料库抽样对比（002/003 check.py 修复模式）
- 读取总行数：~530 行（本 skill）+ ~1,200 行（对照与抽查）
- 重点深度审查文件：check.py（输出检查缺陷定位）、SKILL.md Step 2/5（评测措辞定位）、SCORING.yaml（16 项映射核对）
- 验证手段：`wc -l` 行数核对；YAML 解析验证 frontmatter 字段与 description 长度（500 字符）；grep 统计语料库 322 个 check.py 中 `_is_path` 防护的分布（200/322 已修复，228 未修复）
