# REVIEW: 182-memo

**审查日期**: 2026-08-06 | **Skill 类型**: generation — IRAC 案例备忘录脚手架(骨架生成,分析留白给学生)
**Body 行数**: 204 | **参考文件数**: refs/0, scripts/0, other/0

---

## 1. 目录全量清单

```
182-memo/
├── SKILL.md      204 行  — 主文件(Frontmatter + Body)
├── SCORING.yaml  170 行  — 19 测评项(4 scope + 6 process + 4 output + 3 negative + 2 qa)+ 2 CF
├── check.py       78 行  — 7 项 script 检查(12 项交由 llm judge)
└── references/     — 不存在(无 refs/scripts/assets 目录)
```

- 合计 3 个文件,452 行。参考文件数 0。
- 注:Read 工具显示 SKILL.md 为 205 行、SCORING 171 行、check.py 79 行,与 wc -l 差 1 行,系文件末尾无换行符所致,不影响内容完整性。
- 本 Skill 无任何参考资料文件,全部指令内联于 Body;外部依赖见 §5.2。

## 2. Frontmatter 逐字段审查

### 2.1 name

- `name: memo` — 4 字符,远小于 64 上限 ✓;与目录 `182-memo` 的语义段完全一致(kebab 单单词,无连字符需求)✓

### 2.2 description

原文: "IRAC-scaffolded case analysis memo with research gaps flagged — the scaffold, not the analysis. Rule blocks are RESEARCH NEEDED, Application is STUDENT ANALYSIS prompts, Conclusion is blank. Use when a student needs to scaffold a case analysis memo, write up their analysis, or build an IRAC memo for a case."

- 长度约 300 字符,远小于 1024 上限 ✓
- **WHAT**: "IRAC-scaffolded case analysis memo with research gaps flagged — the scaffold, not the analysis" — 功能定位清晰 ✓
- **WHEN / trigger**: "Use when a student needs to scaffold a case analysis memo, write up their analysis, or build an IRAC memo for a case" — 三组触发场景明确 ✓
- 第三人称 ✓,无第一/第二人称,无祈使(使用约定触发句式 "Use when...")✓
- 内部细节("Rule blocks are RESEARCH NEEDED, Application is STUDENT ANALYSIS prompts, Conclusion is blank")为电报体缩写,与 Body L10 一致;属可接受的描述压缩,但略占描述空间
- 注意:description 中 "the scaffold, not the analysis" 与 Body 核心立场(L24-26)"This skill structures; it doesn't conclude." 完全一致 ✓

### 2.3 allowed-tools

- 未声明 allowed-tools(可选字段)。运行时工具无白名单约束,与 Body "No silent supplement" 的交互要求(需要询问用户)搭配合理。

### 2.4 其他字段

- 仅有 `argument-hint: "[optional: specific issue to focus]"` — 在允许字段清单内(name/description/allowed-tools/argument-hint/user-invocable/model/paths/disable-model-invocation)✓
- 无任何禁止字段(如 triggers/instructions 等)✓

### 2.5 YAML

- 解析正常。description 为纯量标量,不含冒号空格序列;argument-hint 为双引号标量,内部 `:` 安全。无格式问题 ✓

## 3. Body 逐段结构分析

### 3.1 段落清单

| 段 | 行 | 类型 | 内容 |
|---|---|---|---|
| Frontmatter | L1-5 | 元数据 | name / description / argument-hint |
| # Memo | L6 | H1 | 文档级标题(第一次) |
| 快速开始 | L8-12 | 编号清单 | 5 步 TL;DR(加载配置→用流程→框架化议题→强弱项→带标签输出) |
| 命令块 | L14-16 | 代码块 | `/legal-clinic:memo` 自引用命令 |
| # Memo: Internal Case Analysis | L20 | H1 | 文档级标题(第二次) |
| ## Purpose | L22-26 | 段落 | 核心立场:"This skill structures; it doesn't conclude." |
| ## Load context | L28-31 | 段落 | 外部配置加载(practice areas / jurisdiction / facts) |
| ## Pedagogy check | L33-43 | 列表+段落 | guide/assist/teach 三姿态定义、缺省规则、输出标签 |
| ## Workflow | L45-106 | 流程 | Step 1 框架化议题(L47-53)、Step 2 IRAC 脚手架(L55-90)、Step 3 强弱项与开放问题(L92-106) |
| ## Output | L108-204 | 输出 | 横幅(L110-117)→ 完整备忘录模板(L119-187)→ 引用核验(L189)→ 来源标注(L191)→ 禁止静默补充(L193)→ 本 Skill 不做之事(L195-200)→ 收尾决策树(L202-204) |

### 3.2 必需章节(Workflow / Output / Scope)

- **Workflow** ✓ — `## Workflow`(L45),Step 1-3 编号清晰,每步有明确产出与示例
- **Output** ✓ — `## Output`(L108),含完整输出模板(标题、日期行、Bottom line、Issues Presented、逐议题 IRAC、Strengths/Weaknesses/Open Questions、Research gaps summary、NOT 声明)
- **Scope** △ — 无显式 "Scope" 标题;由 `## What this skill does NOT do`(L195-200,四条不做清单)承担边界功能,模板内另有 `## What this memo is NOT`(L181-185)双重声明。边界内容充分,但缺少一个统摄性的 "Scope" 节标题,是三个 Skill 中唯一没有显式 Scope 标题的一个

### 3.3 内容委托

- 零参考文件,零委托;所有方法论内容内联
- 存在**外部委托**:`~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md`(L8/L30)与 `guides/<practice-area>.md`(L35)均不在 Skill 目录内,属运行时外部资源(详见 §5.2)

### 3.4 标题层级

- 文档级 H1 出现 **3 次**:`# Memo`(L6)、`# Memo: Internal Case Analysis`(L20)、以及输出模板内的 `# Case Analysis Memo: [Client] — [Matter]`(L119)
- 前两个 H1 为同级重复标题(一个应降为 H2 或合并);第三个虽位于代码/模板语境,仍是 H1 级标题,阅读时层级感知混乱
- 其余层级规范:H2 节 6 个、H3 子节(Step 1-3、横幅)、引用块与代码块使用得当 ✓

### 3.5 vs 600 行

- 204 / 600 = **34%**,远低于上限,余量 396 行。无超限风险;从内容密度看,该长度与"脚手架"定位匹配,不显单薄 ✓

## 4. 逻辑一致性

### 4.1 步骤衔接

- 快速开始(L8-12)→ 详细 Workflow(L47-106)→ 输出模板(L119 起),三层链条完整无断点
- Step 2 的三种块([RESEARCH NEEDED] / [STUDENT ANALYSIS] / [STUDENT CONCLUSION])与输出模板的 `### Rule` / `### Application` / `### Conclusion`(L140/144/148)一一对应 ✓
- "Research gaps summary"(L174-177)与 Step 2 的 RESEARCH NEEDED 块互相咬合,闭环成立 ✓

### 4.2 矛盾

- **表面张力 1**:guide 姿态(L37)要求 "rather than giving them a framework"(不给框架),而 Step 2(L68-74)允许高置信时给出框架起点。二者以 "explicitly mark it as unverified" 自洽,但 guide 段未交叉引用 Step 2 的例外,读者可能困惑。建议在 L37 末尾加一句 "See Step 2 for the unverified-framework exception."
- **表面张力 2**:assist 姿态定义中夹带整段括号注(L38)解释本 Skill 特殊性 — 属自我修补,处理得当,但行内长注影响可读性(见 §13 优化项)
- 无真正的逻辑矛盾。

### 4.3 代码正确性

- 无真实可执行代码;代码块均为路径、命令(`/legal-clinic:memo`)与模板占位
- 跨行反引号代码 span(L63-66 等)在 CommonMark 中合法(代码 span 可含换行)✓
- 路径写法 `~/.claude/plugins/config/...` 一致(L8/L30/L35)✓

### 4.4 条件完整性

- 姿态缺省规则完备: "If no guide exists, use `guide`. If the guide exists but doesn't set a posture, use `guide`."(L41)✓
- "No silent supplement"(L193)分支完整:4 个选项 + 询问句式 + 主管决定权 ✓
- 多议题场景已覆盖("If there are multiple issues, each gets its own IRAC block."L53)✓
- 未覆盖:单学生无 supervisor 场景、超长案例的分块策略 — 属 🟢 级缺口,不影响主流程

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用目标 | 类型 | 位置 | 状态 |
|---|---|---|---|
| `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` | 外部配置 | L8, L30 | 运行时依赖,目录内不可见 |
| `.../legal-clinic/guides/<practice-area>.md` | 外部配置 | L35 | 运行时依赖,目录内不可见 |
| `/legal-clinic:memo` | 自身命令 | L15 | 自引用,合法 ✓ |
| `/research-start` | 跨 Skill | L66, L169, L177 | **违规,见 5.4** |

### 5.2 不可见资源

- CLAUDE.md 与 guides/<practice-area>.md 位于用户主目录 `~/.claude/plugins/config/`,Skill 目录内不存在对应文件。测评环境中若该路径缺失,Load context 与 Pedagogy check 步骤将空转。
- 缓解:Skill 对缺省有兜底("If no guide exists, use guide"),可优雅降级;但 "Close with the next-steps decision tree per CLAUDE.md `## Outputs`"(L204)若外部 CLAUDE.md 缺失,决策树结构无定义,该步会悬空。建议在 Body 内给出决策树五分支的兜底定义。

### 5.3 全文审查

- N/A — 目录内无参考文件。三个 Skill 中唯一零参考文件的(181 亦为零,180 有 5 个)。

### 5.4 跨 Skill

- `/research-start` 共 **3 处**(L66 的 RESEARCH NEEDED 模板内、L169 "these feed /research-start"、L177 "can run /research-start on each")。
- 已核实实验集中存在 `205-research-start/SKILL.md` — 这是**真实的跨 Skill 路由**,指引用户/Agent 去运行另一个 Skill,违反规范项 4。
- 严重性说明:模板内引用(L66)会随输出复现,等于把路由指令写进产出物,双重传播;但三个 Skill 相比,182 的路由量(3 处,1 个目标)小于 180(见 180 的 REVIEW)。

### 5.5 死文件

- 无死文件(目录内仅 3 个文件,全部被读取与使用)。无 references 目录,不存在"链接了但不存在的文件"。

## 6. 语法与格式

### 6.1 拼写

- 未发现拼写错误。术语(IRAC、habitability、escrow、warranty)拼写全部正确。

### 6.2 语法

- description 电报体为有意风格;正文语法流畅,长句断句合理。L43 输出标签句式("This means I [description of what the student did vs what the skill did]")括号嵌套略绕,可接受。

### 6.3 混杂

- 全文英文,无中英混排;标点使用一致(em-dash 分隔)✓

### 6.4 Markdown

- 标题层级问题见 §3.4;`---` 分隔线在 L18/L110/L118/L130/L136/L152/L156/L172/L179/L187 使用得当
- 模板内方括号 `[STUDENT ANALYSIS: ...]` 在引用块中正确渲染为文本 ✓
- 引用块+代码 span 组合(L63-90)渲染合法 ✓

### 6.5 占位符

- `[State]` / `[Client]` / `[Matter]` / `[student]` / `[date]` / `[Professor]` / `[X]` / `[Y]` 全部为模板占位,属脚手架设计意图,不是未完成标记 ✓
- `[RESEARCH NEEDED]` / `[STUDENT ANALYSIS]` / `[STUDENT CONCLUSION]` / `[UNCERTAIN]` / `[VERIFY]` 均为功能标签,定义与使用一致 ✓

### 6.6 截断

- 正文以 "Close with the next-steps decision tree" 段(L202-204)完整收尾,无截断 ✓

## 7. 规范合规性 12-item

| # | 规范项 | 结果 | 说明 |
|---|---|---|---|
| 1 | name ≤64 且匹配目录 | ✓ | `memo` / `182-memo` |
| 2 | description 第三人称 WHAT+WHEN,≤1024 | ✓ | ~300 字符,双要素齐全 |
| 3 | 无祈使/第一二人称 | ✓ | 触发句式 "Use when..." 为约定写法 |
| 4 | 无跨 Skill 路由 | **✗** | `/research-start` ×3(L66/169/177),目标 205-research-start 真实存在 |
| 5 | 触发信号 | ✓ | 三组使用场景 |
| 6 | 无禁止字段 | ✓ | 仅 name/description/argument-hint |
| 7 | Body ≤600 行 | ✓ | 204 行 |
| 8 | Workflow 节 | ✓ | L45,Step 1-3 |
| 9 | Output 节 | ✓ | L108,含完整模板 |
| 10 | Scope 节 | ✓ | L195 What this skill does NOT do(无显式 Scope 标题,弱满足) |
| 11 | 无 `../` | ✓ | 无相对路径逃逸 |
| 12 | 目录 NNN-kebab | ✓ | `182-memo` |

**违例数: 1 / 12(项 4)**

## 8. 人机感

### 8.1 Emoji

- 0 个 emoji ✓

### 8.2 喊叫

- 全大写仅出现在输出横幅 "AI-ASSISTED SCAFFOLD — THE ANALYSIS IS YOURS TO WRITE"(L112)与功能标签中 — 属刻意强调与标签设计,克制得体 ✓

### 8.3 Persona

- 无人格化、无角色扮演 ✓

### 8.4 人机边界

- 人机边界是全 Skill 最强点: "The analysis is the student's. This skill structures; it doesn't conclude."(L26)、"A memo where those blocks are still empty is a memo that hasn't been written yet."(L184-185)、"The tree is the output; the lawyer picks."(L204) — 三次明示边界 ✓

### 8.5 人称

- 描述与正文均为第三人称;第一人称("I")与第二人称("your supervisor's guide")仅出现在输出模板脚本台词中(L43),属 agent 输出角色语言,规范

### 8.6 表格→自然语言

- 全文零表格,全自然语言 — 人机感最佳实践 ✓

## 9. 可执行性

### 9.1 独立性

- **6.5 / 10**。核心流程(Step 1-3 + 模板)可完全独立执行,不依赖任何工具;但 Load context(L28-31)、Pedagogy check(L33-43)、收尾决策树(L202-204)依赖外部 CLAUDE.md/guides 文件,文件缺失时以上步骤降级为空转或悬空(有默认姿态兜底,但决策树无兜底)。

### 9.2 步骤

- 快速开始 5 步 + Workflow 3 步,全部编号化;每步有明确产出样例(问题句示例、RESEARCH NEEDED 示例、STUDENT ANALYSIS 示例、空白 CONCLUSION 示例)✓

### 9.3 工具

- 无强制工具;模板提及 CourtListener/Westlaw/MCP 仅为引用来源标注体系(L191),不要求调用;研究工具查询由外部配置决定 ✓

## 10. SCORING 交叉参考

### 10.1 测评点(19 项:脚本 7 + LLM 12)

| ID | judge | 检查内容 | Body 支撑 | 结论 |
|---|---|---|---|---|
| SCOPE-01 | script | tool_log 含 `legal-clinic/CLAUDE\.md` | L8/L30 明确要求读取 | ✓ |
| SCOPE-02 | llm | 输出声明 "Pedagogy mode: [posture]" 及姿态行为 | L43 给出精确标签句式,三姿态行为 L35-39 | ✓ |
| SCOPE-03 | llm | 议题以问句呈现 | L51 明确 "State each as a question" 并给出反例 | ✓ |
| SCOPE-04 | llm | 只搭骨架不结论 | L26/L197-199 | ✓ |
| PROC-01 | script | 输出含 `### Rule\|### Application\|### Conclusion` | 模板 L140/144/148 | ✓ |
| PROC-02 | llm | Rule 块为 RESEARCH NEEDED 而非已核验规则 | L61-66 | ✓ |
| PROC-03 | llm | 框架起点标注 unverified + [VERIFY] | L68-74 | ✓ |
| PROC-04 | llm | Application 为 [STUDENT ANALYSIS] 提示 | L78-83 | ✓ |
| PROC-05 | script | 输出含 `\[STUDENT CONCLUSION` | L89-90 / L150 | ✓ |
| PROC-06 | llm | 强弱项分离 + UNCERTAIN 标记 + 三类开放问题 | L96-106 | ✓ |
| OUT-01 | script | 横幅 "THE ANALYSIS IS YOURS TO WRITE" | L112 | ✓ |
| OUT-02 | script | `## Bottom line\|## Issues Presented` | L125/131 | ✓ |
| OUT-03 | script | `## Research gaps summary` | L174 | ✓ |
| OUT-04 | llm | 引用核验 + 来源标签 + "What this memo is NOT" | L189/191/181-185 | ✓ |
| NEG-01 | llm | 不代写分析/规则/结论 | L197-199 | ✓ |
| NEG-02 | llm | 不静默补充薄弱检索结果 | L193 完整脚本 | ✓ |
| NEG-03 | llm | teach 模式遵守两次尝试门槛 | L39 | ✓ |
| QA-01 | script | 5 类来源标签正则 | L191 五类标签齐全 | ✓ |
| QA-02 | llm | 收尾决策树定制 | L202-204 | ✓ |

- check.py 与 SCORING 一致性:docstring 称 "Run all 7 script checks",实际实现恰为 7 项(SCOPE-01、PROC-01、PROC-05、OUT-01/02/03、QA-01),逐项对应 ✓;`_shared/checker.py` 的 `output_contains` 为全输出正则 search(MULTILINE),正则均可在 Body 模板中找到对应字面量 ✓

### 10.2 CF

- CF-01(代写学生分析/结论 → cap_to_0):与 L26/L197 直接对应,判断标准清晰 ✓
- CF-02(无三种块 → cap_to_0):与 L10/L119-150 模板对应 ✓
- 两条 CF 与该 Skill 的核心立场同源,逻辑上不可能与 Body 冲突 ✓

## 11. 已知问题汇总

### Dossier 核实

- Dossier 原句: "三种教学模式与核心立场一致。总评: 🟢"
- 核实 **属实**:guide(不代拟框架,L37)/ assist(明示 [STUDENT ANALYSIS]/[STUDENT CONCLUSION] 恒空,L38)/ teach(两次尝试门槛,L39)三种姿态均以"学生自主完成分析"为核心,与 "the scaffold, not the analysis" 立场零冲突。该论断成立。

### Dossier 遗漏项

1. **规范项 4 违例**:`/research-start` 跨 Skill 路由 ×3(实验集内 205-research-start 真实存在)— 档案完全未提
2. **H1 三次重复**(L6/L20/L119)的标题层级问题未提
3. **外部配置依赖**(CLAUDE.md / guides)的测评环境风险未提
4. assist 姿态行内括号注(L38)的冗长性未提
5. 快速开始(L8-12)与 Load context(L28-31)内容重复未提

## 12. 综合评分 8 维加权

评分维度(权重)+ 分值:

| 维度 | 权重 | 分 | 依据 |
|---|---|---|---|
| 内容结构 | 12.5% | 88 | 三节齐备、模板完整;H1 重复、无显式 Scope 标题 |
| 逻辑一致性 | 15% | 92 | 姿态自洽;guide 与 Step 2 框架起点有轻微表面张力 |
| 参考文件 | 10% | 80 | 零 refs 不扣分;外部配置依赖压低执行环境确定性 |
| 语法格式 | 10% | 96 | 无拼写/语法错误,占位符均为设计意图 |
| 规范合规 | 20% | 90 | 12 项中 1 项违例(项 4) |
| 人机感 | 5% | 95 | 零 emoji、零表格、边界声明×3 |
| 可执行性 | 15% | 85 | 核心独立可运行;外部文件缺失时决策树步骤悬空 |
| 测评对齐 | 12.5% | 100 | 19 项 + 2 CF 全覆盖,check.py 与 SCORING 完全一致 |

**加权得分 = 88×0.125 + 92×0.15 + 80×0.10 + 96×0.10 + 90×0.20 + 95×0.05 + 85×0.15 + 100×0.125 = 90.4**

定级规则(以 12 项规范违例数为第一杠杆,加权分为佐证):0 违例且加权 ≥85 → A;1 违例 → B;≥2 违例 → C;CF 级缺陷 → D。

**综合评分: 🟡B(加权 90.4,规范项 4 违例)**

与 Dossier 🟢 的差异说明:档案的正面论断(三姿态一致)核实属实;差异完全来自档案未执行的规范项 4 核对。若以"12 项全过"为 🟢 标准,本 Skill 需修正 3 处 /research-start 引用后方可回到 🟢。

## 13. 修复建议

### 🔴 致命

- 无。无 CF 级缺陷,无虚假内容,无安全性问题。

### 🟡 重要

1. **移除/改写 `/research-start` 跨 Skill 引用(3 处,最重要)**
   - L66(RESEARCH NEEDED 模板内)、L169(Legal 开放问题)、L177(Research gaps summary 模板)
   - 建议改写为中性表述,如 "a research roadmap should be established separately" / 直接删除 "See /research-start for a roadmap" 一句;输出模板中的引用必须一并清理,否则 Agent 会照抄进产出物,造成路由二次传播
   - 工作量: 约 0.3h(3 处替换 + 一致性复查)
2. **标题层级归一(H1 ×3)**
   - `# Memo`(L6)与 `# Memo: Internal Case Analysis`(L20)合并为单一 H1,后者降为 H2 或删除;模板内 `# Case Analysis Memo: [Client] — [Matter]`(L119)保留为输出标题,但建议在正文注明 "以下为输出模板" 并在模板内改为文档语境标题
   - 工作量: 0.2h
3. **补全收尾决策树的兜底定义**
   - L204 仅说 "per CLAUDE.md `## Outputs`",外部文件缺失时该步悬空;建议在 Body 内给出五默认分支(draft the X / escalate / get more facts / watch and wait / something else)的兜底清单,使 Skill 独立可用
   - 工作量: 0.3h
4. **显式 Scope 标题**
   - 将 `## What this skill does NOT do`(L195)升级为带显式 Scope 的节结构(如 `## Scope` + 子节),或保留现状并在文档中说明弱满足 — 属规范观感问题
   - 工作量: 0.1h

### 🟢 优化

5. **assist 姿态行内括号注外置**(L38):把 "(Note: this memo skill always leaves ...)" 独立为一行 Note,提升可读性 — 0.1h
6. **guide 姿态与 Step 2 交叉引用**(L37):加一句 "See Step 2 for the unverified-framework exception" — 0.05h
7. **合并快速开始与 Load context 的重复内容**(L8 vs L30) — 0.1h
8. **description 精简**:删除内部细节("Rule blocks are RESEARCH NEEDED...")或压缩,保留 WHEN 触发即可 — 0.05h
9. **单学生/无 supervisor 场景补一句**:如 "If no supervisor guide exists and no supervisor is assigned, use guide posture and note it in the output" — 0.05h

**合计工作量: 约 1.2 - 1.5h(不含评审,仅修改)**

## 附录

- **审查方法**:2026-08-06 全文件通读 — SKILL.md(204 行)/ SCORING.yaml(170 行)/ check.py(78 行)逐行阅读;对照规范 12 项逐条判定;将 19 个测评项逐一映射到 Body 行号;核对 `_shared/checker.py` 语义(正则全输出/工具日志 search);核实实验集中 205-research-start 存在与否以判定跨 Skill 路由。
- **变更声明**:本次审查仅生成 REVIEW.md,未修改 SKILL.md、SCORING.yaml、check.py 中的任何内容。
- **行数说明**:wc -l 与 Read 显示差 1 行,系文件末尾无换行符;本报告行数统一采用 wc -l 口径。
