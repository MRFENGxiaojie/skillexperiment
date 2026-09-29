# REVIEW: 201-policy-diff

**审查日期**: 2026-08-06
**Skill 类型**: process — 法规变更与政策库索引的差距分析 (gap analysis) 门控工作流
**Body 行数**: 199 行
**参考文件数**: references/0, scripts/0, 其他/0
**审查范围**: 目录内全部 3 个文件已全文读取 (SKILL.md / SCORING.yaml / check.py)

---

## 1. 目录全量清单

```
201-policy-diff/
├── SKILL.md       (205 行, frontmatter 5 + 空行 1 + body 199)
├── SCORING.yaml   (176 行)
└── check.py       (76 行)
```

- 文件总数: 3
- references/: 0 个文件 — 完全自包含 (process 模式 ~200 行目标内, 无需外置)
- scripts/: 0 个文件
- 其他子目录: 无
- 说明: 本 skill 属于 claude-for-legal 插件生态 (依赖插件配置 `~/.claude/plugins/config/claude-for-legal/regulatory-legal/CLAUDE.md` 而非自带参考文件), 自包含结构合理。

## 2. Frontmatter 逐字段审查

### 2.1 name — matches directory, lowercase+hyphens, ≤64 chars

| 检查项 | 结果 |
|---|---|
| 与目录名匹配 (剥离 NNN-) | ✅ `policy-diff` = `201-policy-diff` 去前缀 |
| 小写 + 连字符 | ✅ |
| 长度 | ✅ 11 字符 ≤ 64 |

**结论: 通过。**

### 2.2 description — sentence analysis, third-person, trigger phrase, ≤1024 chars

原文字段:

> Diff a specific regulatory change against the indexed policy library. Use when a reg has changed and you need to know which policies it touches and what the gap is, when the user says "diff this reg against our policies", "which policy does this affect", or "gap analysis", or when reg-feed-watcher hands off a material item.

| 检查项 | 结果 |
|---|---|
| 长度 | ✅ ≈380 字符 ≤ 1024 |
| WHAT | ✅ "Diff a specific regulatory change against the indexed policy library" — 动作 + 对象明确 |
| WHEN | ✅ 3 个触发场景 + 2 个用户口语触发短语 + 1 个组件交接场景 |
| KEYWORDS | ✅ "gap analysis" / "reg" / "policy" / 组件名 "reg-feed-watcher" |
| 第三人称 | ❌ **违规 1**: 首句 "Diff a specific regulatory change..." 为祈使句 (直接命令 agent), SKILL-SPEC §2.3 明确禁止 imperative 开头 |
| 第二人称 | ❌ **违规 2**: "when a reg has changed and **you** need to know..." 出现第二人称 "you", §2.3 禁止 ("You can use this to..." 列名) |
| 触发信号短语 | ✅ 含 "Use when..." 片段 |
| 无跨 skill 路由 | ⚠️ "when reg-feed-watcher hands off a material item" 具名提及另一组件 — 属插件内生态交接描述 (描述触发场景, 非路由指令 "用 X 代替 Y"), 与 §2.5 禁止的 routing 有区别, 判边缘合规 |

**结论: 部分通过 — 这是本轮四件中 description 唯一出现明确人称违规的。** 首句祈使 + "you need to know" 第二人称, 两项均违反 SKILL-SPEC §2.3。dossier 未记录此问题 (其 🟢 评价基于 body 三节, 未覆盖 description 人称)。修复成本极低 (见 §13)。

### 2.3 allowed-tools — format, necessity per tool

- **声明情况**: 未声明。
- **必要性分析**: 本 skill 需要 Read (读政策库索引与政策文件)、research MCP / WebSearch (Step 0 规则状态核查, 可选)、Write (产出 diff 文档)。全部为默认/条件可用工具, 不声明合理。Step 0 已内置 "no tools connected" 的降级分支 (banner 模式), 不依赖特定工具可用性。
- **格式**: 不适用 (未声明)。

### 2.4 其他 frontmatter 字段 — allowed/forbidden per SKILL-SPEC v1.0

| 字段 | 是否出现 | 判定 |
|---|---|---|
| name / description | ✅ | 必需字段 |
| argument-hint | ✅ | 可选字段 (SKILL-SPEC §1.2 明确允许), `"[reg name, or paste reg text/summary]"` — 对参数化入口的 skill 是合理声明 |
| allowed-tools / user-invocable / model / paths / disable-model-invocation | ❌ | 可选字段, 无必要 |
| 违禁字段 (35 个清单) | ❌ 均未出现 | ✅ |

**结论: 通过。** argument-hint 的使用与 199-invention-intake 一致 (同为插件生态中可参数化调用的 skill), 合规。

### 2.5 Frontmatter 语法

- 有效 YAML。description 含引号触发短语, 未加外层引号但内部双引号在 YAML 流式标量中合法 (双引号在未包裹标量中属普通字符), 解析安全。
- `---` 定界符配对 (1/5 行); argument-hint 行内无冒号冲突。

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行范围 | 节标题 | 层级 |
|---|---|---|
| 6 | # Policy Diff | H1 |
| 8-11 | (入口 4 步速览) | 有序列表 1-4 |
| 15-17 | ## Matter context | H2 |
| 21-23 | ## Purpose | H2 |
| 26-27 | ## Load context | H2 |
| 29-38 | ## Scope integrity | H2 |
| 40-112 | ## Workflow | H2 |
| 42-56 | ### Step 0: Verify rule status before you diff | H3 |
| 58-70 | ### Step 1: Extract the new requirements | H3 |
| 72-78 | ### Step 2: Map to policies | H3 |
| 80-97 | ### Step 3: Diff | H3 |
| 99-112 | ### Step 4: No-match gaps | H3 |
| 114-144 | ## Branches by regulatory input type | H2 |
| 116-123 | ### Pre-rule branch (ANPR / RFI) | H3 |
| 125-140 | ### Negative-finding branch (final rule / NPRM diffed against a policy that isn't the right target) | H3 |
| 142-144 | ### Gap branch (final rule / NPRM with at least one gap against the target policy) | H3 |
| 146-182 | ## Output | H2 (含完整输出模板) |
| 184-191 | ## Config-dependent fallbacks | H2 |
| 193-195 | ## Handoff | H2 |
| 197-199 | ## Close with the next-steps decision tree | H2 |
| 201-205 | ## What this skill does not do | H2 |

### 3.2 必需章节检查

| SKILL-SPEC §3.1 必需章节 | 是否存在 | 说明 |
|---|---|---|
| Workflow / Process | ✅ | ## Workflow + Step 0-4, 含分支路由 |
| Output Format | ✅ | ## Output 给出完整输出模板 (header/bottom line/summary 表/detailed diffs/new policies/no-gap 清单/引文核查声明) |
| Scope / Limitations | ✅ | 双保险: ## Scope integrity (用户排除范围时的旗标纪律) + ## What this skill does not do (明确两条边界) |

**三节齐备 — 与 dossier "三节齐备标杆" 的定性一致。** 本 skill 是三节结构的标准示范, 特别是 scope 由两个互补节 (行为纪律 + 边界声明) 承担, 比单一 Scope 节更完整。

### 3.3 内容委托分析

- 委托率 0% (无 references/scripts)。全部 199 行内联。
- 动态上下文委托给插件配置 (policy library index、matter workspaces、## Outputs/## Who's using this 等均位于插件级 CLAUDE.md), 属于"配置即参考"模式 — 与 199 一致, 自洽。
- 入口 4 步速览 (8-11 行) 与 Workflow 5 步存在轻度内容重复 (速览是摘要, 非矛盾), 可视为 TL;DR 设计。

### 3.4 节编号/标题层级

- H1 → H2 → H3 三级层级严格一致, 无跳级。
- Workflow 的 Step 0-4 全部为 H3, 统一嵌套于 ## Workflow — 无 203 那种跨层级编号问题。
- 分支节 (## Branches by regulatory input type) 三个 H3 与 Workflow 的 Step H3 分属两个 H2 容器, 职责清晰 (步骤 vs 分支选择)。
- 长标题 (如 "Negative-finding branch (final rule / NPRM diffed against a policy that isn't the right target)") 达 20+ 词, 偏长但信息完整, 可接受。

### 3.5 Body 长度合规

- Body 199 行 ≤ 600 ✅。
- process 模式目标 ~200 行 — **几乎精确命中目标** (199 行), 是四件中与 SKILL-SPEC §3.2 行数目标最契合的。

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接

- **全链条闭环**: 入口速览 (1-4) → Step 0 (状态门控) → Step 1 (需求提取) → Step 2 (映射) → Step 3 (diff) / Step 4 (无匹配) → 分支选择 (pre-rule / negative-finding / gap) → Output 模板 → Handoff → 决策树。每一步的输出都是下一步的输入, 无跳跃、无死路。
- 分支路由逻辑自洽: 输入类型 (ANPR/RFI vs 终局规则/NPRM) × 结果 (全 no-gap vs 有 gap) 的两个维度组合出三条互斥分支, 覆盖完整:

| 输入类型 | diff 结果 | 分支 |
|---|---|---|
| ANPR/RFI | (无需求可 diff) | Pre-rule branch |
| 终局规则/NPRM | 全部 no-gap (目标策略错误) | Negative-finding branch |
| 终局规则/NPRM | ≥1 个 gap | Gap branch |

### 4.2 内部矛盾

| 位置 | 描述 | 判定 |
|---|---|---|
| Step 0 banner 文案 vs SCORING PROC-01 期望 | banner 原文 "⚠️ RULE STATUS UNVERIFIED — I could not confirm..." 与 SCORING 描述一致 | ✅ |
| Step 1 来源标签体系 vs Output 中示例 | "[Federal Register]" / "[web search — verify]" 两类标签均属 Step 1 定义的体系 | ✅ |
| 入口速览第 4 条 "Output: per-requirement gap analysis" vs 负向分支压缩输出 | 负向分支明说 "do NOT produce the full per-requirement analysis" — 速览的泛化表述被分支规则精确限定, 不构成矛盾 (速览是默认路径描述) | ✅ 边缘通过 |
| "What this skill does not do" vs Handoff | 不起草策略更新 (职责边界) 与 handoff 给 gap-surfacer (跟踪条目) 不冲突 | ✅ |
| 跨 skill 名称 | gap-surfacer / cold-start-interview / matter-workspace / reg-feed-watcher 均属 claude-for-legal 插件生态组件, 命名一致 | ✅ |

**未发现实质内部矛盾。** "门控与分支规则自洽" 的 dossier 定性核实通过。

### 4.3 示例/代码正确性

- Output 模板: markdown 围栏配对正确; 模板内表格 (Summary 表 #/Requirement/Policy affected/Gap/Owner) 列定义与 Step 2/3 的映射产出一致。
- Step 3 diff 块模板: "New rule requires / Our policy says / Gap (None|Partial|Full) / Change needed / Policy owner" 五要素与 SCORING PROC-04 的测评问题逐项对应。
- Step 4 模板: 三个选项 (draft new / add to existing / determine not needed) 与 SCORING PROC-05 对应。
- 负向分支压缩模板: 引用 "§[X] already covers [Y]" 与 rerun `/regulatory-legal:policy-diff` 路由, 语法正确。
- 引文核查声明 (181 行): 完整段落, 与 QA-01 脚本检查的字符串 'Verify citations before relying on them' 精确匹配 ✅。

### 4.4 条件完整性

| 条件 | 处理 | 完整性 |
|---|---|---|
| 规则状态无法核实 (无工具) | 专属 banner + 每条 due date 打标 + handoff 标记 status_verified: false | ✅ 三层防护 |
| 法规文本部分/模糊 | 停-问四选项, 禁止静默补充 | ✅ (对应 CF-01) |
| 政策库为空 | 全部标记 no-match + 解释文案 + 修复指引 | ✅ |
| 匹配策略缺 owner | Owner 留空 + 文案 + 修复指引 | ✅ |
| 用户排除范围 | 旗标 + 传递至 gap-surfacer + 语义说明 | ✅ |
| 规则 12 个月以上 / 有争议终局规则 | 触发核查 red flag | ✅ |

条件覆盖无缺口。Config fallback 节的 "Say nothing about config when the library is populated" 也明确了默认分支。

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

- 无 references/ 文件, 无文件间引用。
- body 引用的外部路径: `~/.claude/plugins/config/claude-for-legal/regulatory-legal/CLAUDE.md` (插件配置, 运行时存在) 与 matters/<slug>/ (运行时生成) — 均为配置/产物路径, 非 skill 自带资源。
- SCORING SCOPE-01 以 script 检查工具日志含 'regulatory-legal/CLAUDE.md' — 与 body 入口第 1 步直接对应 ✅。

### 5.2 不可见资源审计

- 唯一隐性依赖: 插件级配置 CLAUDE.md 中的 `## Matter workspaces`、`## Outputs`、`## Who's using this`、`[PLACEHOLDER]` 等标记。body 已对配置缺失/占位状态给出 fallback 处理 (Config-dependent fallbacks 节), 依赖被显式管理, 无"幽灵资源"。
- 与 199 相同, body 明确提示索引可能为 `[PLACEHOLDER]` 并给出处理路径, 无虚假承诺。

### 5.3 文件全文审查

- 不适用 (references/ = 0 文件)。自包含设计的正确示范: 199 行的体量无需外置。

### 5.4 跨 Skill 引用

- 引用组件: gap-surfacer (下游消费方)、cold-start-interview (配置初始化)、matter-workspace (切换命令)、reg-feed-watcher (上游触发方, 出现在 description)。全部为 claude-for-legal 插件内生态引用, 以具名方式 (prose) 提及, 符合 SKILL-SPEC §3.3 "使用名称在散文中引用另一 skill" 的规定。
- 无 `../` 跨目录文件引用 ✅。

### 5.5 嵌套重复/死文件

- 无重复、无死文件。目录干净。

## 6. 语法与格式质量

### 6.1 拼写

- 全文无拼写错误。法律术语使用准确 (vacatur / stays / injunctions / rescission / ANPR / RFI / NPRM / gap analysis)。

### 6.2 语法

- 语法正确。长句 (如 17 行 Matter context 段) 信息密度高但结构完整。
- "The flag is the difference between 'we scoped the review' and 'we hid the problem.'" (38 行) — 引用语内的句号处理符合美式英语惯例。

### 6.3 中英/葡英混杂

- 纯英文, 无混杂 ✅。

### 6.4 Markdown 格式破损

- 代码围栏全部配对 (Step 3 模板、负向分支模板、Output 模板各一对)。
- 表格对齐正确 (Step 1 需求表、Summary 表)。
- 引用块 (`>`) 用于 banner 文案, 使用一致。
- 无标题层级破损。

### 6.5 占位符

- 模板内 `[N]`、`[name]`、`[date]`、`[what it requires]`、`[relevant excerpt]`、`[regulator or research tool]`、`[other-policy-1]` 等均为有意的输出模板占位符 ✅。
- 无 TODO/TBD/XXX。

### 6.6 截断

- 全文 205 行完整, 以 "What this skill does not do" 收尾, 无截断。

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 备注 |
|---|---|---|---|
| 1 | name lowercase+hyphens ≤64 匹配目录 | ✅ | `policy-diff`, 11 字符 |
| 2 | description 第三人称 WHAT+WHEN+KEYWORDS ≤1024 | ⚠️ | 长度/内容 ✅, 但人称违规 (见第 3 项) |
| 3 | 无祈使/第一/第二人称开头 | ❌ | 首句祈使 "Diff a specific regulatory change..." + "you need to know" 第二人称 |
| 4 | 无跨 skill 路由 | ⚠️ | "reg-feed-watcher" 具名提及, 属生态交接触发而非路由, 边缘合规 |
| 5 | 触发信号 | ✅ | "Use when a reg has changed..." |
| 6 | 无违禁 frontmatter 键 | ✅ | name/description/argument-hint, 全为允许字段 |
| 7 | body ≤600 行 | ✅ | 199 行 |
| 8 | 有 workflow 章节 | ✅ | ## Workflow + Step 0-4 |
| 9 | 有 output format 章节 | ✅ | ## Output 完整模板 |
| 10 | 有 scope/limitations 章节 | ✅ | ## Scope integrity + ## What this skill does not do |
| 11 | 无 ../ 跨目录引用 | ✅ | 无 |
| 12 | 目录 NNN-kebab-case | ✅ | `201-policy-diff` |

**合规结果: 10/12 明确通过, 2 项边缘 (4 边缘合规), 1 项不通过 (第 3 项 description 人称)。** 即: 严格计 11/12, 宽松计 12/12 (将第 4 项判过)。**body 三节全满分** — "三节齐备标杆" 成立; 唯一失分点在 description 人称, 这也是四件中唯一确凿的 description 违规。

## 8. 人机感评估

### 8.1 Emoji 审计

- body 共 2 处 emoji, 均为 ⚠️ (34 行 SCOPE LIMITATION banner、52 行 RULE STATUS UNVERIFIED banner), 用于高风险旗标, 属**有意的合规警示符号**, 与 199 的 ✓/🟡/🔴 体系同属法律类 skill 的旗标惯例, 非装饰性用法。✅ 可接受。
- SCORING 无 emoji。

### 8.2 全大写/喊叫

- banner 内 "SCOPE LIMITATION" / "RULE STATUS UNVERIFIED" 全大写 — 法律警示惯例 (类似 "CONFIDENTIAL" 水印), 属有意设计而非喊叫 ✅。
- 其余无全大写。

### 8.3 Persona 语气

- 无 persona 扮演。语气为"内部法务顾问的合规分析助手", 专业、克制。

### 8.4 人机边界

- **杰出示范**: "A lawyer decides whether to accept lower-confidence sources; Claude does not decide for them." (60 行) — 明确把置信度决策权交给律师。
- "The tree is the output; the lawyer picks." (199 行) — 决策树是产出, 选择权在律师。
- 引用核查声明 (181 行) 明确提示 AI 生成的引用可能被编造/误引/过时 — 对 LLM 局限性的诚实披露。
- Scope integrity 节把"用户拥有范围主权"与"agent 必须旗标"结合, 人机职责分工清晰。

### 8.5 人称分析

- body 人称: 以祈使句指示 agent (Step 0 "Verify rule status before you diff" — 标题中 "you" 指 agent) 与第三人称陈述混合, 属 body 的正常写法 (SKILL-SPEC 人称约束仅限 description)。
- 无对用户的第一/第二人称叙述。

### 8.6 表格太多

- body 2 张表格 (Step 1 需求表、Summary 表), 均为数据承载必需。✅

## 9. 可执行性评估

### 9.1 独立可执行性

- 独立可执行 ✅。执行前提: 插件配置存在 (有 fallback); 工具可选 (无工具时降级为 banner 模式)。两种环境状态下均有完整路径, 无卡死场景。

### 9.2 步骤可操作性

- 每步均有具体可执行指令与输出模板: Step 0 给出 3 个 red flag 判据; Step 1 给出表格模板与"具体 vs 模糊"的正反例; Step 2 给出三类映射判据; Step 3/4 给出完整块模板; 分支节给出三套输出形态。
- 这是四件中"模板化程度最高"的 skill: agent 只需填空, 临场发挥空间最小, 可执行性最强。

### 9.3 工具依赖

- 依赖工具: Read (索引/政策文件)、可选 research MCP/WebSearch (Step 0 核查)、Write (输出)。
- SCORING 脚本项: SCOPE-01 (tool_log_contains 'regulatory-legal/CLAUDE.md') 与 QA-01 (output_contains 'Verify citations before relying on them') — 均可自动测评, 且与 body 文本精确对应。

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

- `total_items: 19`: SCOPE 3 + PROC 5 + FMT 4 + TEC 2 + NEG 2 + QA 3 = 19 ✅ 一致。
- 判官分布: script 2 项 (SCOPE-01 / QA-01), llm 17 项 (llm 占比 89.5%)。
- check.py 实现与 SCORING 一致:

| SCORING 项 | check.py 实现 | 一致性 |
|---|---|---|
| SCOPE-01 | `tool_log_contains('regulatory-legal/CLAUDE\\.md')` | ✅ 与 body 入口一致 |
| QA-01 | `output_contains('Verify citations before relying on them')` | ✅ 与 Output 模板 181 行精确匹配 |

- check.py 质量: 含 `_is_path` 保护分支 (agent_output 为路径时交给 main 加载, 为文本时直接设置), 比 203 的 check.py 更健壮 — 四件中 201/199 采用新版本模式, 203 为旧模式。
- 覆盖质量: 19 项与 body 的 5 步 + 3 分支 + 输出结构 + fallback + handoff 逐点映射; 特别地, FMT-03 (due date 打标)、TEC-02 (status_verified: false)、FMT-04 (负向分支压缩) 精准对应 body 的细节规则, 测评粒度细。
- 观察: SCOPE-03 (用户排除范围时旗标) 在无排除请求时应答 yes — 测评问题已内置条件化措辞 ("If no exclusion was requested, answer yes"), 设计合理。

### 10.2 Critical Failures 分析

| CF | 内容 | 与 body 的对应 | 判定 |
|---|---|---|---|
| CF-01 | 静默补充 (资料不完整时从 web/模型知识补缺而不问) | 对应 Step 1 "No silent supplement" 四选项流程 | ✅ 有效防线 |
| CF-02 | 未核实规则生效状态即以生效日期呈现 | 对应 Step 0 核查 + banner 流程 | ✅ 有效防线 |
| CF-03 | 对错误目标策略产出完整 per-requirement "no gap" 分析而非压缩路由 | 对应 Negative-finding branch | ✅ 有效防线 |

三个 CF 均为"法律实务层面会产生真实危害"的错误 (错误合规结论/掩盖范围问题), cap_to_0 处罚与风险等级匹配。

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier 记录: "门控与分支规则自洽。总评: 🟢 三节齐备标杆"

| dossier 断言 | 核实结果 |
|---|---|
| 门控与分支规则自洽 | ✅ 核实通过: Step 0 状态门控 → 提取 → 映射 → diff → 分支路由, 双维度三分支组合完整, 无内部矛盾 (§4.1/§4.2) |
| 三节齐备标杆 | ✅ 核实通过: Workflow / Output / Scope (双节) 齐备, 且是四件中唯一三节全满分者 (§3.2/§7) |
| 总评 🟢 | ✅ 核实通过 — 本审查亦判 🟢 A (见 §12) |

**dossier 遗漏 (本次审查新增发现):**

1. **description 人称违规** (首句祈使 + "you need to know" 第二人称) — 唯一确凿的 description 合规缺口, dossier 未记录 (其评价聚焦 body 三节)。
2. **"reg-feed-watcher" 具名提及** — 边缘性生态引用, 若严格判读可视为路由嫌疑, 建议在 description 中弱化为 "an upstream monitor hands off a material item"。
3. **入口 4 步速览与 Workflow 内容重复** (轻度, TL;DR 性质, 不构成缺陷)。
4. 对比项: 201 是四件中 body 与 SCORING 映射最精确的, 此正面事实 dossier 亦未展开。

## 12. 综合评分 — 8 dimensions weighted table

| 维度 | 权重 | 得分 (5 分制) | 加权 |
|---|---|---|---|
| 1. 目录结构完整性 | 0.10 | 4.0 | 0.40 |
| 2. Frontmatter 合规 | 0.15 | 3.5 | 0.525 |
| 3. Body 结构 | 0.15 | 5.0 | 0.75 |
| 4. 逻辑一致性 | 0.20 | 5.0 | 1.00 |
| 5. 参考文件质量 | 0.10 | 4.0 | 0.40 |
| 6. 语法格式质量 | 0.05 | 5.0 | 0.25 |
| 7. SKILL-SPEC 12 项合规 | 0.20 | 4.6 | 0.92 |
| 8. 可执行性 | 0.05 | 5.0 | 0.25 |
| **合计** | 1.00 | — | **4.50 / 5 ≈ 89.9%** |

**总评: 🟢 A** — body 三节齐备、门控/分支/输出/交接全链路自洽、模板化程度与可执行性四件之最、check.py 与 SCORING 映射精确。唯一实质扣分: description 人称违规 (祈使开头 + 第二人称)。若修复 description, 该 skill 是四件中距"满分"最近的。

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷

**未发现。** 无逻辑错误、无断链、无缺失章节、无测评映射断裂。该 skill 当前状态可直接投入使用。

### 🟡 重要缺陷

1. **改写 description 人称 (合规第 3 项, 唯一实质问题)** — 建议改为:

   > Analyzes a specific regulatory change against the indexed policy library and reports which policies it touches and the compliance gap. Use when a reg has changed and the user needs to know which policies are affected, when the user says "diff this reg against our policies", "which policy does this affect", or "gap analysis", or when an upstream monitor hands off a material item.

   变更点: 首句祈使 → 第三人称陈述 ("Analyzes..."); "you need to know" → "the user needs to know"; "reg-feed-watcher" → "an upstream monitor" (消除具名路由嫌疑, 或保留原名但确认其为插件内组件命名)。字符数 ~420, 仍 ≤1024。

2. **(可选) 弱化 reg-feed-watcher 具名** — 若 corpus 对 description 的跨组件具名有更严格判读 (见 §2.2 边缘判定), 按上条一并处理。

### 🟢 优化建议

3. **入口速览加 "default path" 标注** — 在 8-11 行的 4 步速览后加一行 "(负向分支/预规则分支按下方分支节压缩)", 消除 §4.2 中"速览 vs 分支规则"的轻微歧义 (当前靠读者自行推导)。

4. **为三节结构加目录式索引** — body 无 TOC; 199 行的单页 skill 无需 TOC, 不构成缺陷, 但若未来 body 超过 300 行可考虑。

5. **SCORING 补充 description 合规测评点** — 建议增加一项 llm/script 检查 "description 无祈使/第二人称", 使 corpus 能自动捕获同类回归 (当前 checklist 第 3 项无对应测评点)。

6. **FMT-01 可作为 script 化候选** — Output 模板中 "Bottom line" 与 Summary 表头的存在性可用 output_contains 校验, 可将部分 FMT 项从 llm 判官转为 script, 降低 89.5% 的 llm 占比。

### 修复工作量估计

| 项目 | 工作量 |
|---|---|
| description 人称改写 | ~10 分钟 |
| (可选) 组件名弱化 | ~5 分钟 |
| 入口速览标注 | ~5 分钟 |
| SCORING 补测评点 + FMT script 化 | ~30 分钟 |
| **合计** | **~30-50 分钟 (1 人)** |

---

## 附录: 审查过程记录

1. **2026-08-06 13:00** — Glob 递归扫描 `201-policy-diff/`, 确认 3 个文件, 无 references/scripts。
2. **13:03** — 全文读取 SKILL.md (205 行)、SCORING.yaml (176 行)、check.py (76 行)。读取覆盖率 100%。
3. **13:06** — 调取 `_shared/SKILL-SPEC.md` 核对 description 人称规则 (§2.3) 与允许字段 (argument-hint 属 §1.2 允许) — 依据该规则判定 201 的 description 为四件中唯一确凿人称违规。
4. **13:08** — 比对 201/199/203 的 check.py 版本差异 (201/199 含 _is_path 保护, 203 为旧版)。
5. **13:12** — 撰写本 REVIEW.md。

**审查结论摘要**: 🟢 A (89.9%)。三节齐备、门控与分支自洽、可执行性与测评映射四件最优。唯一实质问题: description 祈使开头 + 第二人称, 修复约 10 分钟。建议以本 skill 为 corpus 的 process 型标杆模板。
