# REVIEW: 199-invention-intake

**审查日期**: 2026-08-06
**Skill 类型**: process — 发明披露 (invention disclosure) 首轮筛查与三档结论 (PURSUE/INVESTIGATE/DECLINE) 工作流
**Body 行数**: 462 行
**参考文件数**: references/0, scripts/0, 其他/0
**审查范围**: 目录内全部 3 个文件已全文读取 (SKILL.md / SCORING.yaml / check.py)

---

## 1. 目录全量清单

```
199-invention-intake/
├── SKILL.md       (468 行, frontmatter 5 + 空行 1 + body 462)
├── SCORING.yaml   (183 行)
└── check.py       (77 行)
```

- 文件总数: 3
- references/: 0 个文件 — 完全自包含
- scripts/: 0 个文件
- 其他子目录: 无
- 结构说明: 属于 claude-for-legal 插件生态 (依赖插件配置 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`), 与 201-policy-diff 同构。**注意**: body 462 行对 process 模式 (~200 行目标) 已超 2.3 倍, 是全 corpus 中 body 较长的 process skill 之一, 见 §3.5 与 §13。

## 2. Frontmatter 逐字段审查

### 2.1 name — matches directory, lowercase+hyphens, ≤64 chars

| 检查项 | 结果 |
|---|---|
| 与目录名匹配 (剥离 NNN-) | ✅ `invention-intake` = `199-invention-intake` 去前缀 |
| 小写 + 连字符 | ✅ |
| 长度 | ✅ 15 字符 ≤ 64 |

**结论: 通过。**

### 2.2 description — sentence analysis, third-person, trigger phrase, ≤1024 chars

原文字段:

> Invention disclosure first-pass screen — novelty, obviousness, §101 eligibility, bar dates, detectability, and strategic value. Use when an invention disclosure comes in and needs triage on whether to pursue a prior-art search and patent counsel review, investigate further, or decline.

| 检查项 | 结果 |
|---|---|
| 长度 | ✅ ≈300 字符 ≤ 1024 |
| WHAT | ✅ 六项筛查维度枚举 (novelty / obviousness / §101 / bar dates / detectability / strategic value) — 具体到维度清单 |
| WHEN | ✅ "when an invention disclosure comes in and needs triage" |
| KEYWORDS | ✅ invention disclosure / prior-art search / patent counsel / §101 |
| 第三人称 | ✅ "an invention disclosure comes in and needs triage" — 无第一/第二人称, 无祈使 |
| 触发信号短语 | ⚠️ "Use when an invention disclosure comes in" — 以 "Use when..." 开头且为第三人称主语, 与 SKILL-SPEC §2.4 列出的标准信号 ("Use when the user...", "Triggers on...", "Use for...") 形式不完全一致, 但语义完全等同且无违规成分, 判边缘合规 |
| 无跨 skill 路由 | ✅ 无 |

**结论: 通过 (边缘: 触发信号措辞)。** description 是四件中人称最干净的之一 (唯一无任何人称问题的描述)。

### 2.3 allowed-tools — format, necessity per tool

- **声明情况**: 未声明。
- **必要性分析**: 本 skill 需要 Read (读披露/配置文件)、Write (写筛查备忘)、WebSearch (可选, 且被严格限制为"可信度核查"而非现有技术检索, 见 Guardrails)。全部为默认工具, 不声明合理。
- 注意: body 对 WebSearch 有严格的行为约束 ("Never do a prior-art search in this skill"), 未在 frontmatter 层面限制工具是该约束以行为纪律而非权限纪律实现, 二者自洽。

### 2.4 其他 frontmatter 字段 — allowed/forbidden per SKILL-SPEC v1.0

| 字段 | 是否出现 | 判定 |
|---|---|---|
| name / description | ✅ | 必需字段 |
| argument-hint | ✅ | 可选字段 (§1.2 允许), `"[paste or describe the invention disclosure — or just the title and I'll ask]"` |
| allowed-tools / user-invocable / model / paths / disable-model-invocation | ❌ | 可选字段, 无必要 |
| 违禁字段 (35 个清单) | ❌ 均未出现 | ✅ |

**结论: 通过。** argument-hint 语义贴合本 skill 的输入形态 (粘贴/描述披露文本)。

### 2.5 Frontmatter 语法

- 有效 YAML。description 未加引号, 内含 § 与逗号, 无 YAML 冲突字符。
- argument-hint 含单引号 (I'll) 与破折号, 未包裹引号, 在 YAML 流式标量中安全。
- `---` 定界符配对 (1/5 行)。

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行范围 | 节标题 | 层级 |
|---|---|---|
| 6 | # Invention Intake | H1 |
| 8-13 | (首屏免责声明引言) | 加粗段 |
| 15-40 | ## Instructions | H2 (8 步编号清单) |
| 43-55 | ## Examples | H2 (2 个调用示例) |
| 59-78 | ## THIS IS A FIRST-PASS SCREEN, NOT A PATENTABILITY OPINION | H2 (全大写, 强制免责声明 + 单向门说明) |
| 82-98 | ## Matter context | H2 (matter 切换 + 保密级说明) |
| 102-123 | ## Load the practice profile first | H2 (配置文件读取 + 4 类档案信息) |
| 126-422 | ## Workflow | H2 |
| 128-154 | ### Step 1: Intake the disclosure | H3 (7 问批处理) |
| 156-346 | ### Step 2: Screen against the checklist | H3 (6 屏) |
| 162-185 | #### Screen 1: Novelty signals | H4 |
| 187-208 | #### Screen 2: Obviousness flags | H4 |
| 210-247 | #### Screen 3: Subject-matter eligibility (§ 101) | H4 |
| 249-289 | #### Screen 4: Public disclosure / bar dates | H4 |
| 291-317 | #### Screen 5: Detectability | H4 |
| 319-346 | #### Screen 6: Strategic value | H4 |
| 348-402 | ### Step 3: Assemble the invention screen memo | H3 (完整 memo 模板) |
| 404-422 | ### Step 4: Recommend the bottom-line verdict | H3 (三档结论定义) |
| 424-454 | ## Guardrails | H2 (5 条行为红线) |
| 456-467 | ## Non-lawyer gate | H2 (非律师角色收尾模板) |

### 3.2 必需章节检查

| SKILL-SPEC §3.1 必需章节 | 是否存在 | 说明 |
|---|---|---|
| Workflow / Process | ✅ | ## Workflow + Step 1-4 + 6 屏 |
| Output Format | ✅ | Step 3 给出完整 memo 模板 (Bottom line / Screen results 表 / Open questions / Next steps 决策树) |
| Scope / Limitations | ⚠️ **边缘通过** | 无正式的 ## Scope / ## Limitations / ## What this skill does not do 标题; 但 `## Guardrails` (5 条红线: 禁说 patentable、禁做现有技术检索、§101 移交、detectability 优先、时间敏感旗标) + 首屏免责声明共同承担了 scope/limitations 的实质功能。按实质判读通过, 严格标题判读为不通过 |

**与 201 的对比**: 201 有显式的 "## What this skill does not do" 标题, 199 依赖 Guardrails 隐式承担。建议补一个显式标题 (见 §13)。

### 3.3 内容委托分析

- 委托率 0%。462 行全部内联。
- **重复性冗余**: 免责声明概念出现 3 处 (8-13 行引言、59-78 行全大写节、456-467 行 non-lawyer gate 模板)、"读配置文件→冷启动"指引出现 2 处 (17-18 行 Instructions 第 1 步、102-123 行 Load the practice profile first 节)、Matter context 也同时出现在 Instructions 与独立节。法律 skill 中免责声明的重复有合规理由 (强制宣示), 但 Instructions 与后文各节的重复说明 (2 处读取配置指引、7 问清单的要点重复) 可压缩约 30-40 行。
- 6 屏细则 (162-346 行, ~185 行) 是 body 最大单一内容块, 若继续扩写 (每屏增加判例/更多 red flag), 应外置 `references/screens-guide.md`。

### 3.4 节编号/标题层级

- H1 → H2 → H3 → H4 四级结构严格一致, 无跳级: 6 屏全部为 H4 且统一嵌套于 Step 2 之下, 是四件中层级最深但最规整的。
- Instructions 的 8 步编号 (1-8) 与 Workflow 的 Step 1-4 + 6 屏编号相互对应 (Instructions 第 3 步→Step 1, 第 4 步→Step 2, 第 5 步→Step 3, 第 6 步→Step 4), 映射无错位。
- Examples 节位于 Instructions 之后, 位置合理。

### 3.5 Body 长度合规

- Body 462 行 ≤ 600 硬上限 ✅ (占上限 77%)。
- process 模式目标 ~200 行, **超出 131%** — 是四件中超出目标最多的。虽然内容密度高、无注水, 但已明显偏离模式行数约定; 若再扩写将触及 600 上限。建议结构性瘦身 (重复压缩) + 部分细则外置 (见 §13)。

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接

- **主链闭环**: Step 1 (采集) → Step 2 (6 屏筛查) → Step 3 (memo 组装) → Step 4 (三档结论), 每一步产物清晰:
  - Step 1 输出: 7 问答案或 IDF 字段 → Step 2 输入
  - Step 2 输出: 6 个 ✓/🟡/🔴 判定 → Step 3 表格输入
  - Step 3 输出: memo → Step 4 结论 + Guardrails 约束 + 决策树
- Instructions 8 步与 Workflow 4 步 + Guardrails + Non-lawyer gate 一一对应, 无脱节。
- 时间敏感路径: Instructions 第 8 步 → Guardrails "Urgent cases get urgent flagging" → TEC-01, 三处一致。

### 4.2 内部矛盾

**发现一处确凿内部矛盾 (dossier 未记录):**

| 位置 | 原文 | 判定 |
|---|---|---|
| SKILL.md 158 行 (Step 2 开头) | "**Walk the five screens in order.** Each produces a per-screen verdict..." | ❌ **应为 "six"** |
| SKILL.md 25 行 (Instructions 第 4 步) | "Run the **six** screens: novelty signals, obviousness flags, § 101 eligibility, public disclosure / bar dates, detectability, strategic value" | ✅ |
| SKILL.md 162-346 行 | #### Screen 1 至 #### Screen 6 (共 6 个屏) | ✅ |
| SCORING PROC-02 | "All **six** screens are walked in order..." | ✅ |
| Step 3 memo 表格 | 6 行屏幕结果行 | ✅ |

Step 2 的引言句 "five screens" 与全部其他出处 (Instructions、6 个 Screen 小节、memo 表、SCORING) 的 "six" 直接冲突。这是全目录中最明确的文本错误, 属错别字级 (fiv→six), 但会造成 agent 在 Step 2 开头的屏数预期错乱。**必须修复。**

其余一致性核对:

| 位置 | 描述 | 判定 |
|---|---|---|
| 7 问清单 (Instructions 第 3 步 vs Step 1) | 两处枚举一致 (what/problem/differences/inventors/public disclosure/status/technology area) | ✅ |
| 判定符号体系 | ✓ / 🟡 / 🔴 在 6 屏、memo 表、SCORING PROC-03 中一致 | ✅ |
| PURSUE/INVESTIGATE/DECLINE | Instructions 第 6 步、Step 4、Guardrails、SCORING PROC-04 四处一致 | ✅ |
| §101 美国标准说明 | Screen 3 块引用 + TEC-03 | ✅ |
| 时间敏感旗标 | Instructions 第 8 步 + Guardrails + TEC-01 + CF-03 | ✅ |

### 4.3 示例/代码正确性

- Examples 节 (43-55 行): 两个调用示例 (`/ip-legal:invention-intake "..."` 与无参形式) 语法正确, 与 argument-hint 的输入描述一致。
- Step 1 的 7 问批处理块引用 (134-149 行) 结构完整, 编号 1-7。
- Step 3 memo 模板: 表格列 (Screen | Verdict | Notes) 6 行数据行与 6 屏对应; 决策树 5 个分支与 SCORING FMT-02 的枚举 (prior-art search / inventor follow-up / specialist review / decline / trade secret) 一致。
- **NEG-02 正则陷阱分析 (重要, 非错误但需知晓)**: 脚本检查为 `output_not_contains('is patentable|not patentable')`。而 body 强制要求的免责声明文本中包含 "never concludes that something is \"patentable\"" (72 行)。经逐字符核对: 正则 'is patentable' 要求 "is patentable" 连续, 而声明文本为 `is "patentable"` (is + 空格 + 引号 + patentable), 引号插入使正则**不匹配** — 作者精心规避了免责声明与检查正则的冲突。唯一理论风险: 若 agent 在输出中引用 "'Not patentable' is not an acceptable decline reason" (421 行 的指导句) 则触发 'not patentable' 匹配; 该句是给 agent 的指导而非输出内容, 被引用的概率极低。结论: 正则设计安全, 但属于"踩线设计", 建议在 SCORING 注释中记录该兼容性理由。

### 4.4 条件完整性

| 条件 | 处理 | 完整性 |
|---|---|---|
| 无披露文本 (用户仅给标题/空调用) | 7 问批处理 + 等待 | ✅ (对应 PROC-01) |
| 半披露 (不完整信息) | 明令不筛查半披露 | ✅ (对应 QA-02) |
| IDF 表单 | 提取字段, 只问缺失项 | ✅ (对应 ERR-01) |
| 配置缺失/占位符 | 停止并路由 cold-start-interview | ✅ (对应 SCOPE-02) |
| 商标/版权-only 档案 | 声明错误工具并路由 | ✅ |
| 一年内美国公开披露 / 外国权属风险 | 顶部 time-sensitive 旗标 | ✅ (对应 TEC-01/CF-03) |
| §101 边缘 | 移交专家, 不作自信裁决 | ✅ (对应 TEC-02) |
| 不可检测发明 | detectability 先于 strategic value + 商业秘密替代方案 | ✅ (对应 PROC-05) |
| 非律师角色 | 收尾 gate 模板 | ✅ (对应 QA-01) |

条件覆盖是四件中最全面的 (20 个测评点覆盖上述全部场景), 无缺口。

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

- 无 references/ 文件。
- body 引用的外部路径: `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`、`matters/<matter-slug>/` — 插件配置/运行时产物, 均有 fallback 处理 (placeholders 检测、matter disabled 默认分支)。
- 示例中的 "NeurIPS 2023"、"December 2024" (421 行) 为说明性示例, 非资源引用。
- SCORING 无文件路径型脚本检查 (唯一脚本项为文本检查 NEG-02)。

### 5.2 不可见资源审计

- 隐性依赖: ip-legal 配置 CLAUDE.md 中的 Matter workspaces / practice profile / role / approval chain — 全部有缺失与占位检测 (102-123 行), 无幽灵资源。
- 与 201 相同, 依赖被显式管理。

### 5.3 文件全文审查

- 不适用 (references/ = 0 文件)。

### 5.4 跨 Skill 引用

- 引用组件: `/ip-legal:cold-start-interview` (配置初始化, 3 处)、`/ip-legal:matter-workspace` (切换命令)、非律师 gate 中提及的执业监管机构列表 (state bar / SRA / Law Society 等, 属外部权威引用, 用法正确)。全部为插件内具名引用, 符合 SKILL-SPEC §3.3。
- 无 `../` 跨目录引用 ✅。

### 5.5 嵌套重复/死文件

- 无重复文件、无死文件。目录干净。
- 唯一"重复"是 body 内免责声明的多重出现 (见 §3.3), 属内容层冗余而非文件层问题。

## 6. 语法与格式质量

### 6.1 拼写

- 全文无拼写错误。法律/专利术语准确 (Alice/Mayo、POSA、§ 102(b)、grace period、on-sale bar、IDF、FTO)。
- **一处缩写未展开**: 153 行 "IPMS" (IP Management System) 首次出现未给出全称, 对非专利背景用户可能费解 (轻微)。

### 6.2 语法

- 语法正确。长复合句 (如 245-247 行 EPO/JP/CN 块引用) 结构完整。
- 421 行 "barred by your paper at NeurIPS 2023 — the US one-year bar ran in December 2024" 破折号用法正确。

### 6.3 中英/葡英混杂

- 纯英文, 无混杂 ✅。

### 6.4 Markdown 格式破损

- 代码围栏配对正确 (Examples 2 对、memo 模板 1 对)。
- 块引用 (`>`) 用于 7 问清单、免责声明、§101 国际差异说明、non-lawyer gate — 使用一致且语义正确。
- 表格 (memo Screen results) 对齐正确。
- 无标题层级破损; H4 使用 (6 屏) 是四件中唯一用到 H4 的, 使用正确。

### 6.5 占位符

- memo 模板中的 `[invention title]`、`[✓ / 🟡 / 🔴]`、`[one-line reasoning]`、`[question]`、`[outside counsel / search vendor]` 等均为有意输出占位符 ✅。
- 无 TODO/TBD/XXX。

### 6.6 截断

- 全文 468 行完整, 以 non-lawyer gate 的块引用收尾, 无截断。

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 备注 |
|---|---|---|---|
| 1 | name lowercase+hyphens ≤64 匹配目录 | ✅ | `invention-intake`, 15 字符 |
| 2 | description 第三人称 WHAT+WHEN+KEYWORDS ≤1024 | ✅ | ≈300 字符, 六维度 WHAT 具体 |
| 3 | 无祈使/第一/第二人称开头 | ✅ | 四件中唯一完全干净 |
| 4 | 无跨 skill 路由 | ✅ | 插件内具名引用为生态引用, 非路由 |
| 5 | 触发信号 | ⚠️ | "Use when an invention disclosure comes in" — 语义达标, 形式非标准模板 (边缘) |
| 6 | 无违禁 frontmatter 键 | ✅ | name/description/argument-hint 全为允许字段 |
| 7 | body ≤600 行 | ✅ | 462 行 |
| 8 | 有 workflow 章节 | ✅ | ## Workflow + Step 1-4 |
| 9 | 有 output format 章节 | ✅ | Step 3 memo 模板 |
| 10 | 有 scope/limitations 章节 | ⚠️ | 无正式标题, Guardrails + 免责声明实质承担 (边缘) |
| 11 | 无 ../ 跨目录引用 | ✅ | 无 |
| 12 | 目录 NNN-kebab-case | ✅ | `199-invention-intake` |

**合规结果: 10/12 明确通过, 2 项边缘 (触发信号措辞、Scope 标题形式)。** 若两项边缘均从严判读, 为 10/12; 宽松判读 12/12。body 结构完整性显著强于 203 (缺 Scope) 与 202 (三节齐缺)。

## 8. 人机感评估

### 8.1 Emoji 审计

- body 使用 ✓ / 🟡 / 🔴 三符号判定体系 (6 屏 + memo 表 + Guardrails), 使用位置与语义全程一致 — 这是法律筛查类 skill 的旗标惯例 (与 201 的 ⚠️ 同族), 属功能性符号而非装饰。✅
- 无其他 emoji。

### 8.2 全大写/喊叫

- `## THIS IS A FIRST-PASS SCREEN, NOT A PATENTABILITY OPINION` (59 行) — 全大写 H2, 且内容为"在每份输出顶部宣示、不可省略不可软化"的强制声明。全大写在此语境是法律警示惯例 (同 201 的 banner), 属有意设计 ✅。提示: 若 corpus 对标题全大写有统一审查口径, 可改为加粗正文或保持现状并在本审查中记录为有意设计。

### 8.3 Persona 语气

- 无 persona 扮演。语气为"专利律师助理的首轮筛查工具", 专业、克制、无营销腔。

### 8.4 人机边界

- **本 skill 的最大亮点**: "Under-flagging an invention that should have been filed is a one-way door... Over-flagging just means a prior-art search that comes back empty. Stay on the two-way door side." (75-78 行) — 用非对称风险框架解释筛查偏向, 是优秀的人机决策边界设计。
- "A prior-art search is a separate step; this skill does not do one." (12-13 行) — 边界声明清晰。
- "If uncertain, flag — a registered patent attorney or agent decides." (40-41 行) — 最终判定权明确归于注册执业者。
- 非律师 gate (456-467 行) 把"屏幕说 PURSUE 也不等于你可以去申请"的人机边界落实为可复制的输出模板。

### 8.5 人称分析

- body 以祈使句指示 agent (Instructions "Read...", "Follow...", "Run intake...") — body 惯例, 合规 (人称约束仅限 description)。
- 无对用户的第二人称叙述 (7 问清单对用户发问的部分使用 "What is the invention?" 等中性问句, 恰当)。

### 8.6 表格太多

- body 2 张表 (memo 模板 2 张: Screen results + 无表; 实际 1 张 Screen results 表)。使用克制 ✅。

## 9. 可执行性评估

### 9.1 独立可执行性

- 独立可执行 ✅。执行前提 (ip-legal 配置) 有占位检测与路由; 无工具依赖场景也有完整路径 (7 问交互式采集)。无卡死场景。
- 6 屏的每条判定标准都给出 🔴/🟡/✓ 三档的具体判据清单, agent 可逐条对照, 独立性最强。

### 9.2 步骤可操作性

- 每步均有模板或清单: 7 问清单原文、6 屏 red/green flag 清单、memo 完整模板、三档结论的定义与反例 ("barred by your paper at NeurIPS 2023" 而非 "not patentable")。
- 示例 (43-55 行) 演示了带参数与无参数两种调用方式, 降低入口歧义。

### 9.3 工具依赖

- 依赖工具: Read、Write、WebSearch (受限用途)。全部默认可用。
- SCORING 脚本项仅 1 个 (NEG-02, output_not_contains), 且为负向检查 — 本 skill 的测评 95% 依赖 llm 判官 (19/20), 自动化覆盖是四件中最低的 (与其主观性筛查主题匹配, 但成本高, 见 §10.1)。

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

- `total_items: 20`: SCOPE 3 + PROC 5 + FMT 4 + TEC 3 + NEG 2 + QA 2 + ERR 1 = 20 ✅ 一致。
- 判官分布: script 1 项 (NEG-02), llm 19 项 (llm 占比 95%, 四件最高)。
- check.py 实现与 SCORING 一致: `output_not_contains('is patentable|not patentable')` — 正则与 SCORING 描述逐字相同 ✅。
- check.py 质量: 含 `_is_path` 保护分支 (新版本模式, 同 201); main() 读文件后以内容 set_agent_output, 逻辑正确。
- 类别体系观察: 本 skill 是四件中唯一使用 `error_handling` 类别 (ERR-01, IDF 表单场景) 的; 201/202/203 无 error_handling 类。类别命名无规范强制 (corpus 惯例为 scope/process/format/technical/negative/qa), error_handling 的加入合理但口径需 corpus 层面确认一致。
- 覆盖质量: 20 项覆盖 8 类场景 (见 §4.4), 是三件 process 型中测评点最多、场景覆盖最全的。测评问题措辞均内置条件化 ("If the profile includes non-US jurisdictions..."、"For a non-lawyer role..."), 避免误判。

### 10.2 Critical Failures 分析

| CF | 内容 | 与 body 的对应 | 判定 |
|---|---|---|---|
| CF-01 | 结论为/非 "patentable" | 对应 Guardrails "Never say 'patentable'" + NEG-02 脚本 | ✅ 双保险 (行为 + 文本检查) |
| CF-02 | 执行现有技术检索并作为筛查组成部分 | 对应 Guardrails "Never do a prior-art search" + NEG-01 | ✅ |
| CF-03 | 漏标时间敏感条期 | 对应 Instructions 第 8 步 + Guardrails + TEC-01 | ✅ |

三个 CF 均与 body 红线直接对应; CF-01 同时有脚本兜底 (NEG-02), 是四件中唯一"行为 + 文本"双保险的 CF。

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier 记录: "总评: 🟢"

| dossier 断言 | 核实结果 |
|---|---|
| 总评 🟢 | ✅ 核实通过 — 本审查亦判 🟢 A- (见 §12)。整体质量确实为四件中第二、且接近 201 |

**dossier 遗漏 (本次审查新增发现):**

1. **"five screens" 内部矛盾** (158 行, 应为 "six") — 与 Instructions 第 4 步、6 个 Screen 小节、memo 表、SCORING PROC-02 全部冲突。这是本 skill 唯一确凿的文本错误, 也是四件中唯一被 dossier 遗漏的逻辑错误。
2. **argument-hint 内第一人称** ("I'll ask") — 元数据字段中的第一人称, 虽不属 description 人称约束范围, 但 corpus 若将人称审查扩展到全部 frontmatter 则会被捕获。
3. **无正式 Scope/Limitations 标题** — Guardrails 实质承担但无规范标题 (与 201 的显式 "What this skill does not do" 形成对比)。
4. **body 462 行超 process 目标 2.3 倍** — 接近 600 上限的 77%, 若继续扩写需外置 references/。
5. **"IPMS" 缩写未展开** — 153 行。
6. **NEG-02 正则与强制免责声明的踩线兼容** (72 行 `is "patentable"` vs 正则 'is patentable') — 当前安全, 但属于一旦编辑免责声明文案就会误伤的脆弱设计, 建议在 SCORING 注释中固化兼容性理由。

## 12. 综合评分 — 8 dimensions weighted table

| 维度 | 权重 | 得分 (5 分制) | 加权 |
|---|---|---|---|
| 1. 目录结构完整性 | 0.10 | 4.0 | 0.40 |
| 2. Frontmatter 合规 | 0.15 | 4.5 | 0.675 |
| 3. Body 结构 | 0.15 | 4.5 | 0.675 |
| 4. 逻辑一致性 | 0.20 | 4.0 | 0.80 |
| 5. 参考文件质量 | 0.10 | 4.0 | 0.40 |
| 6. 语法格式质量 | 0.05 | 4.5 | 0.225 |
| 7. SKILL-SPEC 12 项合规 | 0.20 | 4.8 | 0.96 |
| 8. 可执行性 | 0.05 | 5.0 | 0.25 |
| **合计** | 1.00 | — | **4.39 / 5 ≈ 87.7%** |

**总评: 🟢 A-** — 六屏筛查体系、三档结论纪律、人机边界设计 (one-way door 框架、非律师 gate) 均为 corpus 级优秀示范; 合规 12 项近乎全满。唯一实质扣分: "five screens" 文本错误 + 无正式 Scope 标题 + body 长度超目标。

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷

1. **修正 "five screens" → "six screens" (158 行)** — 唯一确凿文本错误, 与 5 处其他出处冲突。一行修改, 10 秒。修复后建议全局搜索 "five" 确认无其他同类错误 (本次审查已确认仅此一处)。

### 🟡 重要缺陷

2. **补正式 Scope/Limitations 标题** — 在 Guardrails 之前或之后新增 `## What this skill does not do` 节 (5-8 行), 内容直接引用现有 Guardrails 的 5 条红线的负面陈述:
   - 不做现有技术检索 (那是一个独立步骤)
   - 不给出专利性结论 ("patentable" 是禁用词)
   - 不裁决边缘 §101 (Alice/Mayo 属专家)
   - 不替代商标/版权场景 (档案非专利实践时路由)
   - 不替注册执业者做申请决定
   - 纯标题补丁, 把边缘合规 (checklist 第 10 项) 转为明确通过, 并与 201 保持结构对仗。

3. **description 触发信号措辞标准化** — "Use when an invention disclosure comes in and needs triage..." 改为 "Use when the user submits an invention disclosure that needs triage on whether to pursue a prior-art search and patent counsel review..." (保留全部信息, 采用标准 "Use when the user..." 模板), 消除边缘判定。

4. **argument-hint 去第一人称** — `"[paste or describe the invention disclosure — or just the title and I'll ask]"` → "...or just the title, and the missing details will be asked for" 或更简洁的 "[paste or describe the invention disclosure, or just the title]"。消除 frontmatter 中唯一的第一人称。

### 🟢 优化建议

5. **压缩重复段 (目标 -30 行)** — 合并 Instructions 第 1 步与 "Load the practice profile first" 节的配置读取说明 (后者保留, 前者改为一句指引); 免责声明保留 2 处 (59 行强制宣示 + 非律师 gate), 删去引言段 (8-13 行) 的第三次重复或改为一句话版本。

6. **"IPMS" 展开为 "IP management system (IPMS)"** (153 行)。

7. **SCORING 注释固化 NEG-02 兼容性** — 在 SCORING.yaml 的 NEG-02 描述旁加注释: "正则有意避开强制免责声明中的 `is \"patentable\"` 引号形式; 修改免责声明文案前需复核本正则"。

8. **为扩写预留 references/** — 若后续要增加每屏的判例/案例库, 外置 `references/screens-guide.md` (6 屏细则约 185 行可整体迁移), body 保留判定矩阵摘要; 同时将 body 收敛至 ~300 行内。

### 修复工作量估计

| 项目 | 工作量 |
|---|---|
| five→six 修正 | ~5 分钟 |
| Scope 标题补丁 | ~15 分钟 |
| description + argument-hint 措辞 | ~10 分钟 |
| 重复压缩 + IPMS + SCORING 注释 | ~30 分钟 |
| (可选) 细则外置 references/ | ~1 小时 |
| **合计** | **~1-1.5 小时 (1 人)** |

---

## 附录: 审查过程记录

1. **2026-08-06 13:30** — Glob 递归扫描 `199-invention-intake/`, 确认 3 个文件, 无 references/scripts。
2. **13:33** — 全文读取 SKILL.md (468 行)、SCORING.yaml (183 行)、check.py (77 行)。读取覆盖率 100%。
3. **13:37** — 调取 `_shared/SKILL-SPEC.md` 核对: argument-hint 属 §1.2 允许字段; description 触发信号标准模板 (§2.4) — 据此判定 199 的 "Use when an invention disclosure comes in" 为边缘形式。
4. **13:40** — 逐字符核对 NEG-02 正则 ('is patentable|not patentable') 与强制免责声明 (72 行 `is "patentable"`) 的兼容性 — 确认引号插入使正则不匹配, 判定为踩线但安全的设计。
5. **13:42** — 全局核对 "five/six" 计数 (Instructions/6 屏/memo 表/SCORING vs 158 行) — 确认唯一矛盾点。
6. **13:45** — 撰写本 REVIEW.md。

**审查结论摘要**: 🟢 A- (87.7%)。六屏筛查与三档结论纪律优秀、人机边界设计 (one-way door、非律师 gate) 为 corpus 示范级。必须修复: "five screens"→"six screens" (唯一逻辑错误); 建议修复: 正式 Scope 标题、description/argument-hint 措辞。修复总量 ~1-1.5 小时。
