# REVIEW: 146-tpl-situacao-testes-codigo-sem-testes

**审查日期**: 2026-08-06
**Skill 类型**: template（tpl-situacao 情境模板家族）— 为"零测试/极少测试"的现有代码库补充测试：特征化测试、seam 识别、风险分级覆盖率
**Body 行数**: 108 行（SKILL.md 共 114 行内容；wc -l 计 113，末行无结尾换行符）
**参考文件数**: references/0, scripts/0, assets/0, 其他/0（完全自包含）
**Dossier 评级**: 🟡（tpl 模板首条编号丢失，同源缺陷）
**总文件数**: 3（SKILL.md + SCORING.yaml + check.py）

---

## 1. 目录全量清单

```
146-tpl-situacao-testes-codigo-sem-testes/
├── SKILL.md       (114 行内容；wc -l 计 113，末行无结尾换行符)
├── SCORING.yaml   (190 行，21 项判据 + 3 项致命失败)
├── check.py       (73 行，2 项脚本检查)
└── REVIEW.md      (本文件)
```

极简三件套结构，无 references/、无 scripts/、无 assets/。全部文件为 CRLF 行尾（Windows 风格）。该 skill 属于 tpl-situacao（情境模板）家族——源材料为葡萄牙语模板包（situacao/08-testes-codigo-sem-testes.md），正文已英文化。108 行 body 以"7 条原则 + 路由表 + 测试金字塔 + 命名规范 + DO NOT + 输出格式 + 质量门禁"构成完整闭环，参考完整性无问题。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 值: `tpl-situacao-testes-codigo-sem-testes` — 全小写 + 连字符 ✅
- 长度: 37 字符 ≤64 ✅
- 匹配目录名 `146-tpl-situacao-testes-codigo-sem-testes`（去掉 NNN- 前缀后完全一致）✅

### 2.2 description

**实际值**:

> Pack template (situacao/08-testes-codigo-sem-testes.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user needs to add tests to a codebase with zero or very few tests — characterization tests, identifying seams, and risk-based coverage.

**逐句分析**:

| 句子 | 角色 | 评价 |
|------|------|------|
| "Pack template (situacao/08-testes-codigo-sem-testes.md)." | 元信息 | ⚠️ 模板包元数据泄露——"这是来自 pack 的模板，源文件是 situacao/08-...md"是模板生成过程的内部信息，对触发匹配零价值，且把葡语文件路径暴露在英语 description 中。用户/agent 不需要知道 "Pack template" 或源文件名 |
| "Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context." | WHAT | ⚠️ **WHAT 与实际内容严重不符**——这是模板包的通用文案（家族内每个情境模板共享此句）。本 skill 的实际内容是"为无测试/极少测试的代码库补测试"（characterization tests、seams、risk-based coverage），与 "debugging、security、refactoring" 毫不相关。后果：用户说"帮我调试这个问题"时可能错误触发本 skill；用户说"给这段老代码补测试"时，本句却无法辅助匹配（幸好第 3 句兜底）。与 023/058 的 description 模板残留同源，属 tpl 家族通用缺陷 |
| "Use when the user needs to add tests to a codebase with zero or very few tests — characterization tests, identifying seams, and risk-based coverage." | WHEN + KEYWORDS | ✅ 真正与内容匹配的触发句——"Use when the user needs to..."标准触发信号 ✅，第三人称 ✅，触发场景具体（补测试），且把三个核心方法（characterization、seams、risk-based coverage）直接作为关键词带出，利于 description 匹配 |

**字符数**: 约 335 字符 ≤1024 ✅

**总体评价**: 触发句合格且准确，但前两句是模板包残留——"Pack template" 元数据 + 牛头不对马嘴的通用句，必须重写。

**修改建议**:

> "Adds tests to codebases with zero or very few existing tests — writing characterization tests first, identifying seams, and prioritizing coverage by risk tier. Use when the user needs to add tests to an untested or barely-tested codebase, or mentions characterization tests, test seams, or risk-based test coverage."

### 2.3 allowed-tools

未定义。❌ 缺失（可选字段，非强制，但强烈建议）。实际执行需要: Read（读代码）、Bash（跑测试）、Write/Edit（写测试文件）、Glob/Grep（找被测文件）。与 tpl 家族其余成员一致缺失——建议系列统一补充: `allowed-tools: Read, Write, Edit, Bash, Glob, Grep`。

### 2.4 其他字段

仅 `name` + `description` 两个键，无禁止字段 ✅。

### 2.5 YAML 语法

- 分隔符配对正确（L1/L4）✅
- description 含 em dash（—）与括号，无双引号包裹，无转义问题 ✅
- 无 BOM ✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# SITUATION: Writing Tests for Untested Code   (L6)    — 标题（全大写 SITUATION 为模板家族标记）
7 条核心原则（编号 1-7）                       (L8-24)  — 17 行
## ROUTING TABLE                               (L26-39) — 10 种情境→处置，14 行
## Test Pyramid Strategy                       (L41-57) — 测试金字塔 70/25/5，17 行
## Test Naming Convention                      (L59-71) — 命名规范 + JS/Jest 示例，13 行
## DO NOT                                      (L73-82) — 8 条禁令，10 行
## OUTPUT FORMAT                               (L84-102) — 5 项交付物 + 特征化测试注释模板，19 行
## QUALITY GATES                               (L104-114) — 9 项质量门，11 行
```

结构骨架与同家族 023/029/030/145 一致（原则 → 路由表 → DO NOT → 输出格式 → 质量门禁），146 在此骨架上补充了领域专属资产：测试金字塔、命名规范、特征化测试注释模板——属于家族内定制较深的一员。

### 3.2 必需章节检查

#### Workflow/Process 节

- ⚠️ 存在但隐含：七条原则（L8-24）定义了执行顺序（先特征化 → 按风险排序 → 测边界 → 找 seams → 一次一个失败测试 → 最外层 mock → 风险分层覆盖率目标），ROUTING TABLE（L26-39）提供情境化处置规则。原则 + 路由表构成完整工作流，但无 `## Workflow` 显式标题与编号步骤
- 原则编号 1-7 连续，无跳跃 ✅

#### Output Format 节

- ✅ 存在: "## OUTPUT FORMAT"（L84-102），5 项交付物（Coverage Report / Test inventory / Seams identified / Characterization tests list / Skipped paths）+ 特征化测试注释模板（含日期、issue 链接、防误改警告）
- 输出与 SCORING PROC-09 的 5 交付物逐一对应 ✅

#### Scope/Limitations 节

- ❌ 不存在独立节。"## DO NOT"（L73-82）是行为否定规则（不 mock 自有代码、不测私有方法、不留 console.log 等），不是 scope 声明。skill 未说明：何时不应使用本 skill（如全新项目从零写测试、纯 E2E 场景、无测试框架的代码库怎么办——OUTPUT FORMAT 假设测试框架已存在）、语言/框架边界（示例全是 JS/Jest，但原则宣称普适）

**评分**: Workflow 7/10, Output 9/10, Scope 6/10

### 3.3 内容委托分析

0% 委托——108 行全部内联，无 reference 依赖 ✅。作为 template 家族 skill，这是最自包含的形态，不存在悬空引用风险（对比 150-copywriting 的两处幽灵引用，146 的参考完整性是其突出优势）。

### 3.4 标题层级与编号

- 标题层级: `#` → `##` 两级，无跳级 ✅
- 原则 7 的嵌套子列表（L20-24）缩进一致 ✅
- "SITUATION"、"ROUTING TABLE"、"OUTPUT FORMAT"、"QUALITY GATES" 全大写节名——模板家族标记，功能性大于喊叫，可接受 ✅
- **编号专项验证**（字节级，od -c）: L8 实际字节为 `1 . SPACE * * C h a r a c t e r i z a t i o n ...`，即 `1. **Characterization tests first.**`——**前缀完整，编号 1-7 连续，dossier 记载的"首条编号丢失"在当前文件中不复现**（详见 §11）

### 3.5 Body 长度

108 行 ≤600 ✅。template 型 skill 精炼得当，信息密度高，无冗余模板脚手架。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

7 条原则构成一条完整的隐含执行链，从"为什么"递进到"怎么验收"：

```
原则 1 特征化测试优先     → 先捕获现状（动机）
原则 2 风险优先           → 决定先测什么（排序）
原则 3 测边界不测实现     → 决定测什么粒度（对象）
原则 4 识别 seam           → 决定怎么测（可测性改造）
原则 5 一次一个失败测试    → 决定执行节奏（反馈回路）
原则 6 最外层 mock         → 决定 mock 策略（边界）
原则 7 风险分级覆盖率      → 决定验收标准（达标线）
```

链条逻辑递进、无跳步，且与 ROUTING TABLE 一一呼应：

- 原则 4"没有 seam 就加最小 seam" ↔ 路由表 "new SomeService() inside a function → Pass it as a parameter with a default" ✅
- 原则 6"mock 最外层边界" ↔ 路由表 DB / HTTP / fs 三行 ✅
- 原则 1"先写记录现状的测试" ↔ 路由表 "Untestable legacy function → characterization test at the top level + TODO + separate PR" ✅
- 原则 2"风险优先" ↔ 路由表覆盖 money/auth/data mutation 等高风险条目 ✅

路由表 10 行覆盖: 全局可变状态、硬编码依赖、DB 调用、HTTP 调用、定时器、文件系统、不可测遗留函数、0% 覆盖函数、async 代码、第三方库——情境覆盖全面，每个情境的处置动作具体可操作（"Extract DB calls to a Repository interface"、"Use Jest's fake timers"）。

### 4.2 内部矛盾深度扫描

1. **覆盖率目标数值矛盾（🟡 中危）**:
   - 原则 7（L21）: "Critical (payments, auth, data deletion): **100%** line + branch coverage"
   - QUALITY GATES（L106）: "Coverage of critical paths (auth, payments, data mutations) is **≥ 90%**"
   - 同一 skill 内对关键路径的覆盖率要求一处 100%、一处 ≥90%。agent 若以 90% 达标（质量门）则违反原则 7 的 100% 要求；若追求 100% 则与质量门的 "≥ 90%" 措辞张力。
   - 有趣的是 SCORING.yaml 的 PROC-05 已自行调和为 "critical paths ≥ 90-100%"——**评测层比 skill 正文先调和了**，正文应跟进
   - 修复方向: 显式区分"目标"与"最低线"——"100% line + branch as the target for critical paths; ≥90% as the acceptance floor"

2. **200ms 门槛与集成测试的张力（🟡）**:
   - QUALITY GATES（L108）: "No test takes more than 200ms (if so, investigate why)"
   - Test Pyramid（L48-51）: Integration Tests (25%) 明确要求 "Use real DB (in-memory or test DB), mock external APIs"
   - 真实 DB 集成测试（尤其含 HTTP 调用、文件 IO）普遍超过 200ms。门槛对 unit 层合理，对 integration 层过严，两者共存会使 agent 在门禁自检时困惑（是删掉 250ms 的集成测试，还是违背"用真实 DB"的要求？）
   - 修复方向: 按测试层分级——"No unit test takes more than 200ms; integration/E2E tests get separate time limits"

3. **async 改造 vs "不改生产代码"的语义边界（🟡）**:
   - 路由表（L38）: "Async code without proper async/await → **Convert to async/await first**"
   - QUALITY GATES（L109）: "No production code was changed to make tests pass (only seams added)"
   - "把异步代码改写为 async/await"是一次生产代码修改动作，是否属于"only seams added"的豁免范围？文本未明说。合理的解释是"最小可测性改造"包含在内（原则 4 的 seam 概念延伸），但 agent 可能因此犹豫，或在门禁自检时误判

4. **"DO NOT target 100% line coverage across the board"（L79）vs 原则 7 的 100%**: 其实语义一致（全局 100% 是反模式、关键路径 100% 是目标），但"100%"在正文出现三次（L21 目标、L79 反模式、L106 90%），措辞易混——建议统一术语（"target vs floor"）。

5. **示例语言单一（🟢 低危）**: 命名规范（describe/it）、路由表（nock/msw、jest.useFakeTimers、sinon、afterEach）全部是 JS/Jest 生态示例，而原则宣称普适。对 Python/Go/Java 代码库，agent 需自行翻译工具——未声明"示例以 JS/Jest 为例，其他语言用等价工具"。

6. **特征化测试模板日期硬编码（🟢 低危）**: L96 "Captures current behavior as of 2024-01-15" 写死日期；"see issue #123" 为占位符。模板注释应引导 agent 填实际日期（"as of [the date this test is written]"），避免照抄 2024 年日期。

**其余一致性核验（✅）**:
- 原则 6 ↔ DO NOT 第 1 条（"DO NOT mock what you own"）: 互为表里 ✅
- 原则 3 ↔ DO NOT 第 2 条（"DO NOT test private methods"）: 一致 ✅
- 原则 1 特征化测试 ↔ DO NOT 第 6 条（不写仅断言 mock 被调用的测试）: 特征化测试断言真实行为而非 mock 行为，不冲突 ✅
- 命名规范 "should [expected behavior] when [condition]" ↔ 特征化测试示例 "should return null when user not found (current behavior)": 示例附加 "(current behavior)" 说明符，与 PROC-07 脚本正则 `should .+ when` 兼容 ✅
- 原则 5"一次一个 + commit" ↔ 无冲突 ✅

### 4.3 示例/代码正确性验证

- 测试金字塔 5%/25%/70%: 行业标准分布 ✅；每层附"何时用/示例"，Integration 层给出具体例子（"UserService creates a user and can retrieve it"）✅
- 覆盖率分级: Critical 100% line+branch / Core 80%+ / Utility 60%+ / Glue skip — 符合业界"关键路径全测、工具代码低覆盖"主流实践 ✅
- 命名规范代码块（L63-71）: describe/it 嵌套结构正确，Jest 语法正确；4 个 it 示例覆盖正/负/边界/业务规则四种场景 ✅
- 特征化测试注释模板（L96-101）: 含日期、issue 链接、"Do not change this test without first verifying the business requirement" 警告——模板的核心价值在于"标记未来可重新验证" ✅
- 技术引用: jest.useFakeTimers()、sinon fake timers、nock、msw、afterEach 均为真实存在的 JS 生态工具 ✅

### 4.4 条件完整性

**正向覆盖**: 7 原则 + 10 场景路由表 = 17 个指导点 ✅
**反向覆盖**: DO NOT 8 条禁令 ✅

**缺失的条件处理**:
- 多场景同时触发时的优先级（timer + DB + HTTP 并存先处理哪个？路由表逐条给方案，无组合优先级——与 023 同一缺口）
- 无测试框架的代码库（应先引入哪个框架）——OUTPUT FORMAT 假设测试框架已存在
- monorepo 中部分模块已测、部分未测的边界处理
- 用户禁止修改生产代码（连最小 seam 都不允许）时的处置
- 时间紧迫时的"最小执行集"（哪些原则不可妥协、哪些可暂缓并记录）

---

## 5. 参考文件审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 状态 |
|----------|:------------:|:--------:|:----:|
| （无文件引用） | — | — | ✅ 自包含 |

SKILL.md 全文无任何 `references/` 或 `scripts/` 文件引用——参考完整性无问题 ✅。

### 5.2 不可见资源审计

实际存在的 3 个文件全部被 runner 使用，无不可见资源、无隐藏文件、无 .gitkeep ✅。

### 5.3 对比同家族模板

与 023（文档写作）、029（部署运维）、030（项目初始化）、145（CVSS 分诊）同属 tpl-situacao 家族。家族共享骨架（原则→路由表→DO NOT→输出→门禁），146 的定制点：
- 023 定制了完整 README/ADR 模板；146 定制了测试金字塔 + 命名规范 + 特征化测试注释模板——均为高价值领域资产
- 146 的 ROUTING TABLE（10 条）是家族内最长的之一，场景覆盖最细
- 146 的 DO NOT（8 条）比 023（6 条）更密集，负面约束更完整

### 5.4 跨 Skill 引用检查

- 全文无跨 skill 引用（prose 或路径均无）✅
- 无 `../` 路径 ✅
- description 中的 "situacao/08-testes-codigo-sem-testes.md" 是 pack 内部元数据标记（对 agent 是噪声，应随模板残留一并移除），不构成跨 skill 引用违规

### 5.5 死文件检查

无 self-nested 目录、无冗余文件、无死引用 ✅。

---

## 6. 语法与格式质量

### 6.1 拼写错误

无明显拼写错误。测试领域术语（characterization、seam、coverage、flaky、seams）拼写正确 ✅。

### 6.2 语法错误

- 整体英文流畅，原则表述精确（如 "Test what breaks the most when wrong"——言简意赅）✅
- "Mock at the outermost boundary" 等短句祈使式为测试指导的标准风格 ✅
- 无主谓不一致、无残缺句 ✅

### 6.3 中英/葡英混杂

- 正文全英文 ✅；description 中含葡语路径 "situacao/08-testes-codigo-sem-testes.md"（模板包残留）——tpl-situacao 家族共有的混排痕迹（058 已记载同类问题）

### 6.4 Markdown 格式破损

| 位置 | 检查项 | 结果 |
|------|--------|:----:|
| L8-24 | 编号列表 1-7 前缀完整（字节级 od -c 验证） | ✅ |
| L26-39 | ROUTING TABLE 管道对齐、10 行 2 列 | ✅ |
| L41-57 | 代码围栏内 ASCII 金字塔图 | ✅ 围栏配对完整 |
| L61-71 / L96-101 | 两个 JS 代码块围栏配对 | ✅ |
| 全文 | 无孤立 `**`、无未闭合括号 | ✅ |
| 全文 | em dash（U+2014）用于句间插入语，无乱码 | ✅ |

**行尾细节（本次审查新增发现）**: 三个文件均为 CRLF 行尾（Windows 风格）；SKILL.md 末行（"A new developer can understand what a function does by reading its tests"）**无结尾换行符**（wc -l 113 vs 内容行 114）。CRLF 在 YAML/Python 解析与 plain 拼接场景无影响，属无害细节；末行无换行符在 git diff 与部分 Unix 拼接工具下会产生告警，建议顺手补上。

### 6.5 占位符未填充

- 无 TODO/FIXME/TBD ✅
- L96 "as of 2024-01-15" 与 "see issue #123" 是有意示例（教 agent 怎么写特征化测试注释），但日期硬编码应引导 agent 用实际日期（见 §4.2-6）

### 6.6 截断内容

文件以 QUALITY GATES 第 9 项正常结束，无截断 ✅。

---

## 7. 规范合规 12 项（逐条对照 `_shared/SKILL-SPEC.md` §5）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name: 小写+连字符, ≤64, 匹配目录 | ✅ | 37 字符，匹配 146- 前缀目录 |
| 2 | description: 第三人称 + WHAT + WHEN + KEYWORDS + ≤1024 | ⚠️ | 人称/长度/触发合规，但 WHAT 句（"debugging, security and refactoring"）与实际内容不符，且含模板包元数据——按 §2.1 精神（"Be specific, not vague"）属实质不合规 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | "Pack template... Guides the agent..." 第三人称 |
| 4 | description: 无内嵌跨技能路由 | ✅ | 无 "see X" 式路由 |
| 5 | description: 含触发信号短语 | ✅ | "Use when the user needs to add tests..." |
| 6 | frontmatter: 无允许列表之外的键 | ✅ | 仅 name + description |
| 7 | body: ≤600 行 | ✅ | 108 行 |
| 8 | body: 有 workflow/process 节 | ⚠️ | 7 原则 + 路由表构成隐含流程，无显式 Workflow 标题 |
| 9 | body: 有 output format 节 | ✅ | "## OUTPUT FORMAT" 完整 |
| 10 | body: 有 scope/limitations 节 | ❌ | DO NOT 是行为规则，非 scope 声明 |
| 11 | body: 无跨 skill 文件引用 | ✅ | 无 `../` 路径 |
| 12 | 目录: NNN-kebab-case, 无空格大写 | ✅ | `146-tpl-situacao-testes-codigo-sem-testes` |

**合规率**: 9 × 1 + 2 × 0.5 + 1 × 0 = **10/12 (83.3%)**——9 项全合规、2 项部分合规（规则 2/8）、1 项违规（规则 10）。

### 违规详情

**违规 1 — 缺 Scope/Limitations 节（规则 10）**: DO NOT 覆盖"测试行为禁令"，但不回答"本 skill 不适用于什么场景"（何时不用、无测试框架怎么办、只做 E2E 怎么办、绿地项目怎么办）。

**部分合规 — description WHAT 失实（规则 2）**: 字面要求形式上满足，但 WHAT 内容与 skill 实际功能不符——"debugging, security and refactoring" 会误导触发匹配。

---

## 8. 人机感评估

### 8.1 Emoji 审计

全文**零 emoji** ✅。工程测试场景，纯文本规则风格合适。

### 8.2 全大写/喊叫式语言

- "SITUATION:"（L6）、"ROUTING TABLE"、"OUTPUT FORMAT"、"QUALITY GATES"、"DO NOT"——全大写节名是 tpl 家族统一标记，功能性大于喊叫 ✅
- "assert what DOES happen"（L8）——用大写强调"行为"vs"应该"，刻意修辞，有效 ✅
- DO NOT 8 条均为强否定（"DO NOT mock what you own"）——规则型指令的合理强度 ✅
- 无 `STOP!`/`MANDATORY`/`CRITICAL` 等过度喊叫 ✅

### 8.3 Persona 语气分析

**整体语气**: 直接、务实、有工程判断的资深测试工程师口吻。这是本 skill 的重要优势——每条规则都有理由、有取舍、有验收标准，不是干巴巴的清单。

**代表性语句**:
- L8: "This is the safety net — even if behavior is wrong, you want to know if it changes." — 先给动机再给指令，解释"为什么"而非只说"做什么"
- L10: "Test what breaks the most when wrong." — 五个词讲清风险优先的全部理由，工程箴言
- L12: "If you have to, the architecture needs to change later." — 有判断、有态度，不回避重构结论
- L16: "Don't write 50 tests then try to make them all pass — the feedback loop is too long." — 具体数字 + 具体后果，有画面感
- L36: "Write a characterization test at the top level only. Add TODO comment. Refactor in a separate PR." — 面对遗留大函数给出明确、克制的处置路径
- L82: "DO NOT skip flaky tests with `xtest` or `.skip` — fix the flakiness or delete the test." — 二选一的硬边界，不留灰色地带

**语气适合度**: ✅ 优秀——写给"会写代码但没给旧代码补过测试"的工程师，每条规则都可执行、可验证。

### 8.4 人机边界分析

**优势**:
- DO NOT 8 条提供明确行为禁区（不 mock 自己的逻辑、不测私有方法、不留 console.log、不跳 flaky 测试）
- QUALITY GATES 9 项全部可验证（覆盖率数值、独立运行、200ms、CI 干净）
- 路由表每条都是 if→then 的具体行动，agent 无歧义空间
- "Untestable legacy function → Write a characterization test at the top level only... Refactor in a separate PR"（L36）——明确限制 agent 不在补测试时顺手重构，边界清晰 ✅
- 特征化测试模板自带 "Do not change this test without first verifying the business requirement"——对未来读者（含人类同事）立了护栏 ✅

**不足**:
- 无"人工复核点"声明：风险分级（哪些代码算 Critical）本质需要产品/领域知识判断，skill 未要求 agent 在分级时确认或报告假设
- 无"何时停下来问用户"的交互点（如代码库语言不是 JS 时，是问用户还是自行迁移工具？）
- 原则 5 的 "commit" 假设 git 工作流存在，未确认用户环境

### 8.5 人称分析

- 全篇无第一/第二人称（无 "you should" 指示 agent 对用户说的话）——纯指令式 ✅
- 全部指令用祈使句或直陈句面向 agent（"Write a test that captures it"、"Extract DB calls to a Repository interface"）✅

### 8.6 表格使用评估

- ROUTING TABLE（L26-39）是情境→处置映射，表格是最优格式 ✅
- 金字塔（L41-57）用代码块 + 箭头呈现层级，比表格更直观 ✅
- QUALITY GATES 用复选框列表 ✅
- 全文仅 1 张表——信息密度高但不过度，格式选择与内容类型匹配良好 ✅

---

## 9. 可执行性评估

### 9.1 独立可执行性: 8.5/10

假设 agent 只拿到 SKILL.md: **完全可执行**。七原则给出顺序与方法，路由表给出 10 种典型情境的处置，命名规范给出格式，输出格式给出 5 项交付物，质量门给出验收标准——108 行内形成完整闭环（为什么 → 怎么办 → 怎么分配 → 怎么命名 → 什么不能做 → 交什么 → 怎么验收），无任何外部依赖。

### 9.2 步骤可操作性

| 元素 | 可操作性 | 评估 |
|------|:--------:|------|
| 7 条原则 | 🟢 | 每条都是可执行祈使句，且带动机解释 |
| ROUTING TABLE | 🟢 | 10 种情境 if→then 映射，动作具体（"Pass it as a parameter with a default"） |
| 测试金字塔 | 🟢 | 比例 + 每层用法 + 示例 |
| 命名规范 | 🟢 | 代码块可直接照抄模式 |
| DO NOT | 🟢 | 8 条禁令每条都是可判定的行为规则 |
| OUTPUT FORMAT | 🟢 | 5 项交付物 + 注释模板可直接使用 |
| QUALITY GATES | 🟢 | 9 项验收，大部分可自动验证（除 "new developer can understand" 主观项） |

### 9.3 可执行性盲点

- **JS 生态假设** 🟡: nock/msw/jest/sinon 对非 JS 用户直接失效，无迁移指引（见 §4.2-5）
- **无测试框架的启动路径缺失** 🟡: 未定义"代码库还没有测试框架"时怎么办
- **降级路径缺失** 🟡: 未定义"时间不足时的最小执行集"
- **覆盖率测量工具未指定** 🟢: 门禁要求 "Coverage report visible in CI"，但未给出产出手段（Istanbul/JaCoCo 等）
- 工具依赖: 无硬编码工具/服务依赖 ✅；隐含依赖（测试框架、覆盖率工具）属常识性实现细节，可接受

### 9.4 与测评的对接性

两条脚本检查（SCOPE-02 "CHARACTERIZATION TEST"、PROC-07 "should .+ when"）与正文模板/示例**逐字对齐**——忠实 agent 可稳定通过，假阴性风险为家族内最低。

---

## 10. SCORING.yaml 交叉参考

### 10.1 结构核查

- `total_items: 21` ✅ 实际 21（SCOPE 3 + PROC 9 + NEG 6 + QA 2 + ERR 1），计数正确
- `pattern: template` ✅ 与 Skill 类型一致（research-design 中 template 型典型 18-20 项，21 略高但合理）
- judge 分布: script 2 / llm 19——llm 占比 90.5%，家族内典型
- critical_failures: 3 个 cap_to_0 ✅
- `check.py` 头注释 "Run all 2 script checks" ✅ 实际返回 2 项（SCOPE-02、PROC-07），注释与实际一致

### 10.2 检查项 ↔ SKILL.md 全量映射

| 检查项 | 来源章节 | 一致性 |
|--------|---------|:------:|
| SCOPE-01 | description 触发条件（"adds tests to a codebase with zero or very few tests"） | ✅ |
| SCOPE-02 | OUTPUT FORMAT 特征化测试模板（tool_log 含 "CHARACTERIZATION TEST" 注释） | ✅ 脚本正则与模板注释字面匹配 |
| SCOPE-03 | 原则 2（风险优先） | ✅ |
| PROC-01 | 原则 4 + 路由表 `new SomeService()` 条目（最小 seam） | ✅ |
| PROC-02 | 路由表（reset()/Repository 接口/nock-msw/假定时器/临时目录） | ✅ 逐条对应 |
| PROC-03 | 原则 5（一次一个失败测试 + commit） | ✅ |
| PROC-04 | 原则 6（最外层 mock） | ✅ |
| PROC-05 | 原则 7（风险分级覆盖率） | ✅ 评分描述已自行调和 90%/100% 数值差（"≥ 90-100%"） |
| PROC-06 | Test Pyramid（70/25/5） | ✅ |
| PROC-07 | Test Naming Convention | ✅ 脚本正则 `should .+ when` 与模式字面匹配 |
| PROC-08 | 路由表 legacy 函数条目（顶层特征化测试 + TODO + 独立 PR） | ✅ |
| PROC-09 | OUTPUT FORMAT 5 项交付物 | ✅ |
| NEG-01 | DO NOT 第 1 条 | ✅ |
| NEG-02 | DO NOT 第 2 条 | ✅ |
| NEG-03 | DO NOT 第 3/4 条 | ✅ |
| NEG-04 | DO NOT 第 6 条 | ✅ |
| NEG-05 | DO NOT 第 7/8 条 | ✅ |
| NEG-06 | QUALITY GATES 第 4 条（only seams added） | ✅ |
| QA-01 | QUALITY GATES 汇总（覆盖、独立性、200ms、特征化标记、CI 干净） | ✅ |
| QA-02 | 命名规范 + 门禁第 9 项（测试如文档） | ✅ |
| ERR-01 | 原则 4 第二句（"If a class has no seams, you'll need to add a minimal one"） | ✅ |

**21/21 全部可追溯到 SKILL.md 原文，无凭空检查项**——这是本 skill 测评设计最扎实的部分。

### 10.3 脚本检查细节

| Criterion | 检查模式 (check.py) | SKILL.md 对应文本 | 一致性 |
|-----------|--------------------|------------------|:------:|
| SCOPE-02 | `tool_log_contains("CHARACTERIZATION TEST")` | L96 "// CHARACTERIZATION TEST: Captures current behavior as of 2024-01-15." | ✅ 逐字对齐 |
| PROC-07 | `tool_log_contains("should .+ when")` | L63-67 "it('should return JWT token when credentials are valid', ...)" | ✅ 逐字对齐 |

设计评价: 两条脚本检查检查的是 agent **实际写入测试文件**的注释/命名（tool log 而非 output），能真实捕获"agent 是否写了特征化测试"与"是否遵循命名模式"——设计得当。

### 10.4 Critical Failures 分析

- CF-01（只写断言型测试、无特征化测试 → cap 0）: 合理，对应原则 1 的核心方法论 ✅
- CF-02（mock 自有业务逻辑 / 直接测私有方法 → cap 0）: 合理，对应原则 6 + DO NOT 1/2 条 ✅
- CF-03（改生产代码让测试通过 / 留 flaky 或 skip 测试 → cap 0）: 合理，对应 DO NOT 8 + 门禁 4 条 ✅

三个 CF 全部与正文规则一一咬合，设置恰当——均为本 skill 的"灵魂红线"。

### 10.5 评分架构观察

- script 项仅 2/21（9.5%），低于研究设计中 ~40% 的脚本占比目标（023 为 1/15 即 6.7%，同属偏低）。原因可理解——补测试的遵从度大多需要语义判断（是否风险优先、是否 mock 了自家逻辑）。可考虑增加 1-2 个机械项，如："覆盖报告出现 before/after 数字"（正则 `\d+%`）或"特征化测试注释含 issue 编号"（`#\d+`）
- PROC-07 正则 `should .+ when` 用贪婪 `.+`，对长测试名无歧义（字面字符串出现在 tool log 即可），无实际风险 ✅

---

## 11. 已知问题验证（来自 skill-dossier.md）

### Dossier 记录

> **145-146 tpl 模板系列**: "逻辑: 145 CVSS 分诊与更新策略一致；146 特征化测试优先与风险分级原则链一致。语法: 均编号第 1 条丢失前缀。人机感: 路由表+质量门禁驱动，agent 可执行性强。合规: 均 OUTPUT FORMAT、DO NOT 齐备，仅编号缺陷。"

### 逐项验证

| Dossier 记载 | 本次审查验证 | 状态 |
|-------------|------------|:----:|
| 特征化测试优先与风险分级原则链一致 | 原则 1→7 链条与路由表、质量门互相咬合（§4.1 验证） | ✅ 确认 |
| 编号第 1 条丢失前缀 | **L8 字节级验证为 "1. **Characterization tests first.**"——编号 1 存在且完整，1-7 连续** | ❌ **不复现** |
| 路由表 + 质量门禁驱动、agent 可执行性强 | 10 场景路由表 + 9 项门禁，闭环完整（§9 验证） | ✅ 确认 |
| OUTPUT FORMAT、DO NOT 齐备 | L73-82 / L84-102 均存在 | ✅ 确认 |
| "仅编号缺陷"的总评 | ⚠️ 需修订 | 本审查发现 3 处增量问题（见下） |

**重要发现**: dossier 记载的"首条编号丢失"问题在当前文件状态中**不存在**（字节级验证）。可能原因：
1. 该文件在 2026-08-05 dossier 审查之后被修复过（tpl 家族其他成员如 029/046/058/166-169 确实存在此缺陷，本文件可能是修复后的状态）；
2. dossier 的 "均编号第 1 条丢失前缀" 是 145/146 的合并记载，实际只有 145 存在该问题，146 被误并入。

**据此建议**: **不要对 146 做编号修复**（无问题可修）；若维护者关注该家族缺陷，请单独核对 145 的编号状态（对照集 complex-skills-no-trigger 中对应目录也应一并核对）。

### Dossier 未记载的新问题（本次审查发现）

1. 🟠 **description 前两句为模板包残留**——"Pack template (situacao/...)" 元数据 + "debugging, security and refactoring" 通用句与内容不符（家族同源缺陷，023/058 已记载过同类问题）
2. 🟡 **覆盖率目标矛盾**: 原则 7 的 100% vs 质量门的 ≥90%（SCORING PROC-05 已调和，正文未跟进）
3. 🟡 **200ms 门槛与集成测试张力**: 真实 DB 集成测试普遍超 200ms（§4.2-2）
4. 🟡 **async 改造 vs "only seams added" 语义边界**: 未定义转换 async/await 是否属于最小 seam（§4.2-3）
5. 🟡 **无 Scope/Limitations 节**: 12-item 规则 10 违规
6. 🟡 **allowed-tools 缺失**: 家族通病
7. 🟢 **示例全部为 JS/Jest 生态**，未声明语言中立性
8. 🟢 **CRLF + 末行无换行符**: 跨平台工具链细节

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 6/10 | 10% | 0.60 | description WHAT 失实 + 模板包元数据残留 + allowed-tools 缺失 |
| Body 结构完整 | 8/10 | 10% | 0.80 | workflow（隐含）与 OUTPUT FORMAT 齐备；缺 Scope 节 |
| 逻辑一致性 | 9/10 | 20% | 1.80 | 原则链↔路由表↔DO NOT↔门禁四层自洽；3 处轻微张力（100%/90%、200ms、async） |
| 参考完整性 | 10/10 | 15% | 1.50 | 完全自包含，零断链风险 |
| 语法格式 | 9/10 | 10% | 0.90 | 字节级验证无破损；CRLF + 末行无换行为无害细节 |
| 规范合规 | 8/10 | 15% | 1.20 | 10/12（9 全合规 + 2 部分 + 1 违规） |
| 人机感 | 9/10 | 10% | 0.90 | 实战派工程师语气 + 动机解释，零 emoji |
| 可执行性 | 8/10 | 10% | 0.80 | 闭环完整、脚本检查逐字对齐；JS 生态假设与降级路径缺失 |
| **加权总分** | | | **8.50/10** | **85/100** |

计算: 0.10×6 + 0.10×8 + 0.20×9 + 0.15×10 + 0.10×9 + 0.15×8 + 0.10×9 + 0.10×8 = 8.50

### 12.2 评级

🟢 **B+ (85/100)**: 高质量的 template 型 skill。7 条原则构成家族内罕见的完整逻辑链（动机→排序→对象→手段→节奏→边界→验收），路由表与原则互为实例化，DO NOT 与门禁为行为与验收双重约束，测评点 21/21 全部可追溯。主要扣分项（description 模板残留、缺 Scope 节、allowed-tools）修复成本极低（约 15 行）。dossier 记载的编号缺陷已不复现。

### 12.3 与同系列对比

tpl-situacao 家族中，146 属于定制最深的成员之一：路由表最长（10 条）、DO NOT 最密（8 条）、持有领域专属资产（测试金字塔 + 命名规范 + 特征化测试注释模板）。家族两处通病（description 模板残留、allowed-tools 缺失）在 146 上同样存在——建议家族级统一修复。若修复完成，此 skill 可作为 template 型 skill 的系列标杆。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: 重写 description（移除模板包残留，修正 WHAT）**
- **位置**: SKILL.md L3
- **问题**: 第 1 句 "Pack template (situacao/08-testes-codigo-sem-testes.md)" 是内部元数据；第 2 句 "debugging, security and refactoring" 与实际内容（补测试）完全不符，可能误导触发匹配
- **修复**: 按 §2.2 的修改建议替换:
  ```
  description: "Adds tests to codebases with zero or very few existing tests — writing characterization tests first, identifying seams, and prioritizing coverage by risk tier. Use when the user needs to add tests to an untested or barely-tested codebase, or mentions characterization tests, test seams, or risk-based test coverage."
  ```
- **不修复的后果**: 调试/安全/重构类请求可能错误触发本 skill（资源浪费 + Mode B 实验中污染 trigger 维度数据）；补测试请求的触发匹配缺少关键词支撑

**F-2: 补 Scope/Limitations 节（违反 SKILL-SPEC §3.1 规则 10）**
- **位置**: QUALITY GATES 之前
- **修复**: 新增 "## SCOPE" 节:
  ```markdown
  ## SCOPE

  This skill adds tests to existing untested or barely-tested code. It does NOT:

  - **Write tests for greenfield projects** — for new code with no legacy
    constraints, standard TDD applies; this skill targets existing behavior.
  - **Refactor legacy code** — refactoring happens in a separate PR, after
    characterization tests lock in current behavior.
  - **Fix bugs** — a failing test reveals a bug; fixing the production code
    is a separate task outside this skill's test-adding scope.
  - **Rewrite tests wholesale** — existing passing tests stay; the skill adds
    coverage for untested paths and converts behavior-capturing tests where
    appropriate.
  - **Require a specific language or framework** — examples use JS/Jest, but
    the principles apply to any stack; substitute equivalent tools.
  ```
- **不修复的后果**: agent 可能在绿地项目误用本 skill、或在补测试时顺手重构（违反 CF-03 边界）

### 🟡 重要缺陷（建议修复）

**I-1: 统一覆盖率目标语义（100% vs ≥90%）**
- **位置**: L21（原则 7）+ L106（质量门 1）
- **修复**: 显式区分目标与最低线——原则 7 改为 "Critical (payments, auth, data deletion): target 100% line + branch coverage (acceptance floor: ≥90%)"，或质量门改为 "Coverage of critical paths reaches the rule-7 target or the agreed floor (≥90%)"
- **不修复的后果**: agent 在 90% 与 100% 之间摇摆，llm judge（PROC-05）可能判定不一致

**I-2: 明确 200ms 门槛适用域**
- **位置**: L108
- **修复**: 改为 "No unit test takes more than 200ms; integration and E2E tests get separate, higher time limits"——避免与"集成测试用真实 DB"的要求冲突

**I-3: 明确 async 改造与"不改生产代码"的关系**
- **位置**: 路由表 async 条目 + 门禁第 4 条
- **修复**: 门禁第 4 条补充限定语: "No production code was changed to make tests pass (only minimal seams and readability conversions, e.g. async/await, added)"

**I-4: 特征化测试模板日期动态化**
- **位置**: L96
- **修复**: "as of 2024-01-15" → "as of [the date this test is written]"——避免 agent 照抄硬编码日期

**I-5: 声明示例语言中立性**
- **位置**: Test Naming Convention 节首或 ROUTING TABLE 后
- **修复**: 加一句: "Examples use JavaScript/Jest; apply the same patterns with your stack's equivalents (pytest, JUnit, Go testing, etc.)."

### 🟢 优化建议（锦上添花）

**O-1: 补充"无测试框架"启动路径** — 在 ROUTING TABLE 补一行: "Codebase has no test framework yet → add the minimal framework setup (e.g., vitest/jest for JS, pytest for Python) as the first step, then proceed"

**O-2: 补充 allowed-tools** — `allowed-tools: Read, Write, Edit, Bash, Glob, Grep`（读代码、写测试、跑测试套件需要）

**O-3: 路由表添加组合场景优先级** — "若 DB + HTTP + timer 同时出现，先处理 DB（数据完整性风险最高）"

**O-4: SCORING 补充测评点** — 质量门 "No test takes more than 200ms"（L108）无对应 criterion；"new developer can understand"（L114）主观项可考虑给出可判定替代（如测试名全遵循命名规范）

**O-5: 与同家族 skill 的编号问题交叉核对** — 本文件编号完整（dossier 记载不复现）；建议核对 145 是否仍存在首条编号丢失（含对照集 complex-skills-no-trigger 对应目录）

**O-6: 补末尾换行符 + 统一 LF** — 顺手修复 CRLF/末行无换行（git diff 友好度）

### 修复工作量估计
- 修改行数: description 1 行、Scope 节 +15 行、覆盖率措辞 2 行、200ms 措辞 1 行、async 限定 1 行、日期 1 行、语言中立声明 1 行 ≈ **22 行**
- 修改文件数: 1（SKILL.md）；SCORING.yaml 可选（O-4）
- 建议同时按同一模式修复 tpl-situacao 家族其余成员（description 残留 + allowed-tools 为家族通病）

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 114 行内容，全文精读（含编号完整性逐行验证）
2. SCORING.yaml — 190 行，全文（21 criteria + 3 critical_failures）
3. check.py — 73 行，全文（2 项 script check）
4. _shared/SKILL-SPEC.md — 161 行，全文（合规依据）
5. skill-dossier.md — 145/146/148/150 相关条目（已知问题对照）

### 读取统计
- 总文件数: 5（3 skill 文件 + 1 规范 + 1 dossier 摘录）
- 总行数: 约 540 行

### 审查方法
- 所有文件全文阅读，未使用抽样 ✅
- 字节级验证: L8 编号前缀（od -c）、末行换行符（tail -c）、行尾风格（grep -c $'\r'）
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条清单
- 已知问题对照: skill-dossier.md（2026-08-05 记录）——特别注意"首条编号丢失"记载的复核
- 数值一致性: 原则 7 覆盖率分级 vs QUALITY GATES vs SCORING PROC-05
- 家族对比: 023/029/030/145（tpl-situacao 同源缺陷核验）

### 审查人
Claude (SkillIF quality audit) — 2026-08-06

### 审查备注
本 skill 是 tpl-situacao 家族中逻辑链最完整的成员：7 条原则的递进关系（动机→排序→对象→手段→节奏→边界→验收）为家族内少见的设计质量，21 个测评点全部可追溯至正文。dossier 标记的"首条编号丢失"经字节级验证在当前文件中已不存在（同 023 案例，建议交叉核对 145），但 description 模板残留与缺 Scope 节仍存在。审查新增发现：覆盖率数值未调和（100% vs ≥90%）、200ms 门槛与集成测试张力、async 改造与"不改生产代码"的语义边界、CRLF 与末行无换行符细节。修复成本极低（~22 行），修复后此 skill 可作为 template 型 skill 的家族标杆。
