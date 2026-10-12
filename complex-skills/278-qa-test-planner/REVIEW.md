# REVIEW: 278-qa-test-planner

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: tool — QA 测试文档生成工具（test plan / test case / regression suite / Figma validation / bug report 五类交付物）
**Body 行数**: 400 行（SKILL.md）
**参考文件数**: 15 个（references/），其中 4 个正式指南 + 11 个切分碎片
**脚本数**: 2 个（scripts/，均为 bash）
**总行数**: 21 个文件，约 3,500 行
**已有 REVIEW**: 无（本文件为首次审查）

---

## 1. 目录全量清单

```
278-qa-test-planner/
├── SKILL.md                                    (400 行, 2026-08-05 18:15 修改)
├── README.md                                   (355 行, 2026-07-31)
├── SCORING.yaml                                (160 行, 2026-08-05 14:50)
├── check.py                                    ( 56 行, 2026-08-05 16:38)
├── references/                                 (目录时间戳 2026-08-05 18:15)
│   ├── test_case_templates.md                  (430 行, 2026-07-31) ← 正式指南
│   ├── bug_report_templates.md                 (423 行, 2026-07-31) ← 正式指南
│   ├── regression_testing.md                   (371 行, 2026-07-31) ← 正式指南
│   ├── figma_validation.md                     (345 行, 2026-07-31) ← 正式指南
│   ├── additional-context.md                   (150 行, 2026-08-05 18:15) ← 碎片
│   ├── coverage-matrix.md                      ( 96 行, 2026-08-05 18:15) ← 碎片
│   ├── tc-login-001-valid-user-login.md        ( 49 行, 2026-08-05 18:15) ← 碎片
│   ├── tc-ui-045-mobile-navigation-menu.md     ( 46 行, 2026-08-05 18:15) ← 碎片
│   ├── next-steps.md                           (  8 行, 2026-08-05 18:15) ← 碎片
│   ├── test-cases-by-priority.md               (  7 行, 2026-08-05 18:15) ← 碎片
│   ├── summary.md                              (  7 行, 2026-08-05 18:15) ← 碎片
│   ├── examples.md                             (  5 行, 2026-08-05 18:15) ← 碎片
│   ├── critical-failures.md                    (  3 行, 2026-08-05 18:15) ← 碎片
│   ├── risks.md                                (  2 行, 2026-08-05 18:15) ← 碎片
│   └── blocked-tests.md                        (  1 行, 2026-08-05 18:15) ← 碎片
└── scripts/
    ├── generate_test_cases.sh                  (302 行, 2026-07-31)
    └── create_bug_report.sh                    (276 行, 2026-07-31)
```

文件时间戳是本次审查最重要的线索之一：README、四个正式指南、两个脚本均为 2026-07-31（语料原始版本）；而 SKILL.md 的修改时间与 references/ 目录下 11 个小文件的创建时间完全一致（2026-08-05 18:15），这与项目记忆中"body-too-long 已由 converter 自动拆分"的记录吻合。换言之，这 11 个小文件不是作者有意编写的参考文档，而是规范化时从原 SKILL.md 尾部机械切分出来的碎片（详见第 5 节）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

```
name: qa-test-planner
```

- 全小写 + 连字符：✅
- ≤64 字符：✅（14 字符）
- 匹配目录名 `278-qa-test-planner` 的 slug 部分：✅（SKILL-SPEC.md 要求 name 匹配目录名）

### 2.2 description（逐句分析）

原文：

```
Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers. Includes Figma MCP integration for design validation. Use when the user asks to create a test plan, generate manual test cases, build a regression or smoke test suite, validate a page against a Figma design, or write a bug report.
```

逐句拆解：

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers." | WHAT | ✅ 具体列举了四类交付物与目标用户 |
| "Includes Figma MCP integration for design validation." | 能力陈述（含实现细节倾向） | 🟡 边界情况——"Figma MCP integration" 提及了内部工具依赖（MCP server），与 001-skill-tuning 审查中 "Supports Gemini CLI" 被判定为内部实现细节的先例同型。但此处程度较轻：Figma 校验本身是该 skill 面向用户的核心能力，MCP 只是实现途径，且 body 与参考指南中都有实质的 Figma 校验方法学支撑。可移入 body，非强制 |
| "Use when the user asks to create a test plan, generate manual test cases, build a regression or smoke test suite, validate a page against a Figma design, or write a bug report." | WHEN + KEYWORDS | ✅ 五个触发场景，覆盖五类交付物，含 trigger 信号短语 "Use when the user asks to..." |

**第三人称检查**：全文无第一/第二人称代词，动词为无主语的第三人称描述句式。✅

**触发短语**：含 "Use when the user asks to..." 标准信号。✅

**字符数**：约 380 字符，≤1024。✅

**特别说明**：SKILL-SPEC.md §2.6 的 "Good" 示例所引用的 description 正是本 skill 的这一段。也就是说，本 description 是规范作者钦定的正面范例——按规范自身标准，这是完全合规的（也是 322 个 skill 中 description 最标准化的样本之一）。

**激活机制自洽性**：description 含完整触发短语，意味着在 Claude Code 的 Mode B（自然激活）下该 skill 会被自动匹配；而 SKILL.md body 第 10 行声明 "This skill is triggered only when explicitly called by name"。两者并不矛盾——description 负责"何时可用"，body 声明"需要显式指名才会真正启用"。与 SCORING.yaml 的 SCOPE-02（仅在显式请求时激活，不主动应用于一般功能讨论）一致。

### 2.3 其他 frontmatter 字段

仅有 `name` 和 `description` 两个字段，均为 SKILL-SPEC.md §1 允许的字段。无禁止字段（无 `trigger: explicit` 等非标准键——记忆显示规范化已将所有非标准键清零）。✅

### 2.4 Frontmatter 语法

YAML 分隔符 `---` 配对正确，description 为带引号的单行字符串，无未转义特殊字符。✅

---

## 3. Body 结构审查

### 3.1 章节地图

SKILL.md 正文共 400 行，结构如下：

1. **Quick Start**（15-42 行）— 五种请求的一句话示例，全部是自然语言 prompt 示例，用户可照抄。
2. **Quick Reference**（45-54 行）— 任务→交付物→耗时映射表。
3. **How It Works**（58-82 行）— 三阶段工作流（ANALYZE / GENERATE / VALIDATE）。这是全 skill 唯一的工作流节，但极其精简：每阶段只有三个要点短语，没有任何分支条件、决策规则或"何时走哪条路径"的说明。对一个"tool"型 skill 而言，工作流部分偏弱——如何从用户的一句话需求判断该产出哪类交付物（这正是 SCORING SCOPE-01/03 测的）在 body 中缺乏显式决策指引。
4. **Commands**（86-104 行）— 脚本用法表 + 自然语言请求→结果映射表。
5. **Core Deliverables**（108-142 行）— 五类交付物（Test Plans / Manual Test Cases / Regression Suites / Figma Validation / Bug Reports）的内容要点清单。这是"输出格式"节的实体，覆盖了全部五类交付物。
6. **Patterns to Avoid**（146-155 行）— 五条反模式表（含原因与替代做法）。
7. **Verification Checklist**（159-178 行）— 三类交付物的自查清单。
8. **References**（182-188 行）— 仅列 4 个正式指南。
9. **三个 Deep Dive**（191-401 行，`<details>` 折叠）— 标准测试用例格式、测试计划模板、Bug 报告模板，均含完整可复制的 markdown 模板。这是 body 最有价值的部分。

### 3.2 结构性缺陷

**缺陷一：Scope/Limitations 节缺失（规范违规，详见第 7 节）**。全 body 没有任何"本 skill 不做什么"的说明。"Patterns to Avoid" 讲的是测试文档的质量反模式（模糊步骤、缺前置条件等），不是 skill 的边界（例如：不做自动化测试执行、不做 CI 集成、Figma 校验依赖 MCP server 可用性等）。SKILL-SPEC.md §3.1 明确要求 body 必须有 scope/limitations 节。

**缺陷二：How It Works 的流程图是残破的**。第 60-62 行：

```
Your Request

-
```

"Your Request" 与三阶段之间只有一个孤立的 "-"，应有的箭头/流程符号缺失，读起来像排版事故。79 行 "QA-Ready Deliverable" 之前同样是一个孤立 "-"。这个图原本大概是一个 ASCII 流程图，被规范化工具弄坏后没有修复。

**缺陷三：body 以脚手架残留收尾**。Deep Dive: Bug Report 之后（389-401 行）是一个"## Reference Files"列表，罗列 11 个参考文件（文件名被机器式地大写为 "Tc Login 001 Valid User Login" 等），整个 SKILL.md 就结束在这个列表上，没有任何收束。这个列表显然是为 2026-08-05 的自动切分服务的注释性残留，不是有意的文档设计（切分证据见第 5 节）。

**缺陷四：体量超出 tool pattern 目标**。SKILL-SPEC §3.2 规定 tool pattern 目标 ~300 行、硬上限 600 行。本 body 400 行，未超硬上限但超出目标 1/3，且这正是被切分过的结果——切分后仍有 400 行，说明原文显著超出硬上限（这也是它被 converter 拆分的直接原因）。

### 3.3 结构优点

- 三个 Deep Dive 使用 `<details>`/`<summary>` 折叠，主 body 保持清爽，符合"把细节折叠、把主干突出"的良好实践。
- Quick Start 提供了五种可直接照抄的用户话术，降低了 agent 理解触发场景的成本。
- Verification Checklist 与 SCORING 的 OUT-01/NEG-01 高度呼应，是"检查项"与"测评点"对得上的少数 skill 之一。

---

## 4. 逻辑一致性审查

本 skill 的逻辑一致性总体良好（核心流程无自相矛盾），但存在若干尺度/枚举不一致与残留错误，按严重度排列：

### 4.1 优先级标尺冲突（中等）

SKILL.md Deep Dive: Test Case Structure 的标准模板写的是：

```
**Priority:** High | Medium | Low
```

而 references/test_case_templates.md 的标准模板与命名表用的是：

```
**Priority:** P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
```

SCORING.yaml 的 PROC-10 也按 "Critical P0 = crash/data loss/security, down to Low P3 = cosmetic" 检查。三处两套标尺。若 agent 照 SKILL.md 模板产出 "High/Medium/Low" 优先级，而 SCORING 期望 P0-P3，会产生评分误判；更重要的是 team 内部文档会同时出现两种标尺。同源问题：SKILL.md Deep Dive 的 Status 枚举 "Not Executed | Passed | Failed | Blocked" 与 test_case_templates.md 的 "Not Run | Pass | Fail | Blocked | Skipped" 不一致；bug 报告 Status "Open | In Progress | Fixed | Closed" 与 bug_report_templates.md 的 "Open | In Progress | In Review | Fixed | Verified | Closed" 不一致。类型枚举同样如此：SKILL.md 模板 "Functional | UI | Integration | Regression"，test_case_templates.md 是六类（含 Performance/Security），而示例文件 tc-ui-045 用了模板体系之外的 "UI/Responsive"。

### 4.2 create_bug_report.sh 的 Type 字段恒为 Functional（真 bug）

`scripts/create_bug_report.sh` 第 158 行：

```bash
**Type:** ${TEST_TYPE:-Functional}
```

但 `TEST_TYPE` 在该脚本中从未被赋值——它是从 `generate_test_cases.sh` 复制过来的残留变量（generate_test_cases.sh 中 TEST_TYPE 由第 8 步的 case 语句赋值）。结果：这个脚本生成的所有 bug 报告 Type 恒为 "Functional"，即使用户报告的是性能或 UI bug。这不是文档措辞问题，是可复现的逻辑缺陷。

### 4.3 README 结构树与实际文件不符（中等）

README.md "Skill Structure" 节（297-311 行）只列出 4 个 references 文件 + 2 个脚本，而实际存在 15 个 references 文件。SKILL.md 的 "References" 节同样只列 4 个。11 个碎片文件只在 SKILL.md 末尾的 Bug Report 模板 Reference Files 列表中隐现。三处对文件系统的描述互相不一致，会让 agent（和人类）对 skill 的真实体积产生错误预期。

### 4.4 回归套件层级不一致（轻微）

SKILL.md Core Deliverables 只列三层：Smoke（15-30 min）、Full（2-4 hours）、Targeted（30-60 min）。README（74-77 行）和 regression_testing.md 都是四层，含 Sanity（10-15 min, after hotfix）。SCORING PROC-08 只要求三层。SKILL.md 与 SCORING 一致，但作为"主入口"漏掉了 README/参考指南都有的 Sanity 层——agent 只读 SKILL.md 时会遗漏 hotfix 快速验证场景。

### 4.5 脚本提示文本与逻辑不符（轻微）

generate_test_cases.sh 前置条件输入提示 "press Enter twice when done"，但循环逻辑是读到第一个空行即 break——实际只需一次回车；第二次回车多余且提示误导。同文件步骤输入用 `ACTION false`（非必填）+ 空值即终止，与提示 "Type 'done' when finished" 双重语义并存，行为正确但措辞含糊。

### 4.6 其余一致性核查（通过项）

- 五类交付物的 Quick Start / Quick Reference / Commands / Core Deliverables 四处描述互相一致，无冲突。
- 耗时估算（10-15 min test plan、5-10 min/case、15-20 min regression suite、5 min bug report）在 SKILL.md 与 README 间一致。
- 测试计划退出标准（90%+ pass rate、无未修复 critical bug）在 SKILL.md、regression_testing.md、SCORING PROC-03 三处一致。
- 严重度定义（Critical/High/Medium/Low 与 P0-P3 的映射）在 bug_report_templates.md、additional-context.md、SCORING PROC-10 三处一致。
- 执行顺序（smoke first → stop on P0 failure）在 regression_testing.md 与 SCORING PROC-08 间一致。
- 示例文件 tc-login-001 与 tc-ui-045 的字段结构与正式模板吻合（除 Type 枚举问题外）。

---

## 5. 参考文件逐一全文分析

本 skill 有 15 个参考文件，分两类：4 个正式指南（语料原始内容，质量高）与 11 个切分碎片（规范化副产物，存在严重格式断裂）。逐一分析如下。

### 5.1 test_case_templates.md（430 行，正式指南）

内容最丰富的参考文件。包含：标准测试用例模板（TC-ID、优先级、类型、状态、预计耗时、创建/更新日期、目标、前置条件、测试步骤（每步含输入与 Expected）、测试数据表、后置条件、边界与变体表、相关用例、执行历史表、备注）、以及按类型的五个专项模板（Functional / UI/Visual / Integration / Regression / Security / Performance），每类模板都针对该类型定制了字段（如 UI 模板有视觉规格表——布局/字体/颜色/交互状态，Performance 模板有指标目标表——响应时间/吞吐量/错误率/CPU/内存）。末尾附命名规则表（TC-FUNC-/TC-UI-/TC-INT-/TC-REG-/TC-SEC-/TC-PERF-/TC-API-/SMOKE-）与优先级定义表（P0-P3 与执行频率映射）。这份文件是 skill 的核心资产：模板字段齐全、每步强制 Expected、覆盖六类测试，对 agent 生成结构化测试用例的约束力很强。缺陷：长度 430 行，作为"模板参考"偏长，且与 SKILL.md Deep Dive 的简化模板构成双源（见第 4.1 节的标尺冲突）。

### 5.2 bug_report_templates.md（423 行，正式指南）

同样高密度。标准 bug 模板字段极全：严重度/优先级/类型/状态/经办人/报告人/日期、环境表（OS/浏览器/设备/构建/环境/URL）、描述、复现步骤（含前置条件与复现率）、期望/实际行为、视觉证据（前后截图/录像/控制台错误/网络错误）、影响评估表（受影响用户/频率/数据影响/业务影响/变通方案）、附加上下文（关联项/回归信息）、开发者区块（根因/修复方案/改动文件/PR）、QA 验证清单。另附四个专项模板：Quick（简版）、UI/Visual（设计差异对照表，含 Expected vs Actual vs Match）、Performance（指标期望 vs 实际 vs 差异百分比）、Security（OWASP 类别/机密标记/影响/修复建议/披露时间线）、Crash/Error（错误消息/堆栈/日志）。末尾是严重度定义表（含响应时限）、优先级×影响矩阵（Rare/Often/Always × Low/Critical Impact）、标题最佳实践（好标题 3 例、坏标题 4 例）、提交前检查清单。这份文件把"可复现 bug 报告"的所有要素都固化了，且与 SCORING PROC-09/PROC-10 的检查点一一对应。缺陷与 5.1 相同：与 SKILL.md Deep Dive 简化模板构成双源。

### 5.3 regression_testing.md（371 行，正式指南）

覆盖回归测试全流程：定义与触发时机、三层套件结构（Smoke 15-30min 每日 / Full 2-4h 发布前 / Targeted 30-60min 变更后，外加 Sanity 10-15min）、构建套件的三步法（识别关键路径→按 P0/P1/P2 排优先级→按功能域分组，含 Auth/Payment/User Management 分组示例树）、电商回归套件完整示例（按模块列执行时长）、执行策略（smoke first → stop on failure → P0 → P1/P2 → exploratory；PASS/FAIL/CONDITIONAL PASS 判据）、套件维护节奏（月度评审/发布后更新）、自动化取舍清单、执行报告模板（含汇总表与 BUG 关联格式）、常见陷阱（❌/✅ 对照）、执行前中后检查清单、速查表。质量高，与 SCORING PROC-08 完全对应。独特价值：提供了唯一完整的"回归测试执行报告"模板——SKILL.md 主体没有这一交付物。

### 5.4 figma_validation.md（345 行，正式指南）

设计校验方法学指南：前置条件（Figma MCP server 配置/设计文件访问权限/组件 URL）、三步工作流（MCP 取规格 → DevTools 检查实现 → 记录差异，含 TC-UI-001 差异记录示例）、校验维度清单（布局与间距/排版/颜色/组件/交互状态，每维度带示例查询语句）、常见差异分类（排版不匹配/间距问题/颜色差异/响应式行为）、测试用例模板（桌面/平板/移动三个断点 + 状态机）、MCP 查询语料库（组件规格/颜色系统/间距/断点四组示例 prompt）、UI 差异 bug 报告模板、自动化想法（Percy/Chromatic/BackstopJS 视觉回归、设计令牌校验）、最佳实践 DO/DON'T、逐组件检查清单、速查表。与 SCORING PROC-11/PROC-12 精确对应（hex 颜色、字号、间距、圆角、状态，差异→bug+Figma 链接）。这份指南是"Figma MCP 集成"声称的实质支撑——若没有它，description 里的 Figma 能力就是空话。

### 5.5 additional-context.md（150 行，碎片 1）

碎片特征最明显的一个文件。开头就是孤立的 ```（一个没有配对的关闭围栏，第 5 行），紧接着是 "### Severity Definitions" 表——这显然是某处被切断后残留的围栏尾巴。随后是三个 `<details>` 块：Figma MCP Integration deep dive、Regression Testing deep dive、Test Execution Tracking deep dive。前两个内容完整但与 5.3/5.4 高度重复（Figma 的规格提取/DevTools 对比流程、回归的三层套件/执行顺序/PASS-FAIL 判据在正式指南中都有且更详细）。第三个 "Deep Dive: Test Execution Tracking" 在第 150 行戛然而止——内容只到 "**Environment:** Staging" 一行，测试执行报告模板的其余部分（汇总表、失败项、建议等）被直接截断，且 `<details>` 从未闭合。这个文件是"切分把完整文档拦腰截断"的铁证。

### 5.6 coverage-matrix.md（96 行，碎片 2）

前 8 行是一个覆盖矩阵表（Login/Checkout/Dashboard 的特性-需求-用例-状态-缺口），第 8 行有一个孤立 ``` 围栏——说明该表原本是代码块的一部分。之后是两个 `<details>` 块：QA Process Workflow（Planning/Test Design/Execution/Reporting 四阶段清单）与 Best Practices（测试用例编写/缺陷报告/回归测试的 DO-DON'T）。这两块内容结构完整、质量尚可（与正式指南的 Best Practices 部分重复）。孤立围栏 + 与 5.1-5.4 的重复内容使其作为独立文档价值低。

### 5.7 tc-login-001-valid-user-login.md（49 行，碎片 3）

一个完整度较高的测试用例示例：TC-LOGIN-001（P0，Functional，2 分钟），含目标、前置条件（测试账号、清 cookie）、四步测试步骤（每步含 Expected，第 4 步含三个断言）、后置条件、待扩展边界用例清单（TC-LOGIN-002 到 005）。作为示例本身质量不错——具体 URL、具体断言（"Welcome back, Test User"）、可执行的边界用例列表。但文件末尾三行是 "```"、"\</details\>"、"\</details\>"——一个孤立围栏和两个无配对的 details 闭合标签（本文件内从未打开任何 details）。它是某个更大的 `<details>` 示例块被切开后剩下的部分。

### 5.8 tc-ui-045-mobile-navigation-menu.md（46 行，碎片 4）

同理是"响应式测试用例"示例的残段：TC-UI-045（P1，UI/Responsive，移动端），含目标、前置条件（视口 375-428px）、四步测试（汉堡菜单可见→滑入动画→点击导航→对比 Figma 设计，含具体数值断言：宽度 280px、动画 300ms ease-out、遮罩透明度 0.5 色值 #000000、字号 16px 行高 24px）、断点清单（四款设备）。示例质量好，但文件末尾包含文档级收尾内容——Dijkstra 与亚里士多德引言（与 README 结尾的引言完全相同）。引言属于"文档尾部"内容，出现在一个测试用例文件中，进一步证明这些碎片原本是一份连续文档的不同段落。

### 5.9 六个微型碎片（碎片 5-10）

- **blocked-tests.md**（1 行）：`## Blocked Tests` + 一条示例 "TC-112: Dashboard widget (API endpoint down)"。语义完整但只有一条假数据，是原文档中一个示例块的残留。
- **critical-failures.md**（3 行）：`## Critical Failures` + 一条示例（TC-045 失败，关联 BUG-234，状态 Open）。
- **risks.md**（2 行）：两条发布风险示例（2 个 critical bug 阻塞发布、支付集成需关注）。
- **summary.md**（7 行）：测试汇总示例（150 总数/145 执行/130 通过/10 失败/5 阻塞/90% 通过率）。
- **test-cases-by-priority.md**（7 行）：按优先级统计示例表（P0 25 项 23 通过 / P1 50 项 45 通过 / P2 50 项 / P3 25 项）。
- **next-steps.md**（8 行）：`## Next Steps` 三条示例 + 第 5 行孤立 ``` + 第 7 行未闭合的 "```markdown"。同样是被拦腰切断的证据。

这六个文件的内容（除 risks 外）在其他碎片中能找到同源数据（summary 的 130 通过 vs critical-failures 的 2 个 critical bug 与 next-steps 的 BUG-234 修复，互相自洽，说明它们出自同一份虚构的执行报告文档片段）。每个文件体量都只有 1-8 行，作为"参考文档"没有独立价值。

### 5.10 碎片成因重建

将时间戳（全部创建于 2026-08-05 18:15，与 SKILL.md 同一分钟）、格式断裂点（孤立围栏、未闭合 details、句子截断）与内容连续性（Figma/Regression deep dive 与正式指南重复；尾部引言与 README 重复）三者合起来，可以重建原文档的顺序：

> …（bug 报告 deep dive）→ Additional Context → Severity Definitions → Figma MCP deep dive → Regression deep dive → Test Execution Tracking（截断于此）→ Blocked Tests → Coverage Matrix → QA Process Workflow → Best Practices → Examples（截断于 "```markdown"）→ Next Steps → Risks → Summary → Test Cases by Priority → TC-LOGIN-001 → TC-UI-045 → 结尾引言

即：原 SKILL.md 是一份超过 600 行硬上限的巨文档，规范化时 converter 将尾部约 500 行切分为 11 个文件，并在 SKILL.md 的 bug 报告 deep dive 末尾机械追加了 "## Reference Files" 清单。切分点是按标题盲切的，没有检查围栏配对与 details 配对，导致碎片链上至少 6 个文件（additional-context、coverage-matrix、examples、next-steps、tc-login-001、tc-ui-045）出现格式断裂，且大量内容（Figma/Regression 两个 deep dive、QA 流程、最佳实践、示例）与 4 个正式指南重复。

### 5.11 碎片对 skill 的影响评估

- 对 agent 执行的影响：中性偏负。SKILL.md 自身完整覆盖五类交付物，4 个正式指南质量足够，碎片不承载核心信息；但 agent 若按 SKILL.md 末尾的 Reference Files 列表逐一阅读，会在断裂的 markdown 上浪费时间与 token，且 additional-context.md 末尾截断的 details 可能让 agent 误以为存在未读完的内容。
- 对评测的影响：中性。SCORING 17 项检查的证据全部存在于 SKILL.md 与 4 个正式指南中，碎片不参与评分依据。
- 对仓库卫生的影响：显著为负。11 个碎片（合计约 380 行）中至少有 9 个不具备独立文档价值，是规范化过程留下的技术债。

---

## 6. 语法格式审查

### 6.1 主体文件（SKILL.md / README / SCORING.yaml / check.py / 4 个正式指南 / 2 个脚本）

- Markdown 语法整体干净：标题层级正确、表格结构完整、代码围栏配对无误（SKILL.md 的 5 个 markdown 模板围栏全部闭合）、`<details>` 全部配对。
- YAML（SCORING.yaml）可解析：结构缩进一致，160 行无语法问题（17 个 criteria + 3 个 critical_failures 均为合法的 question/evidence 结构）。
- Python（check.py）语法正确，可独立运行（`python check.py a b c` 输出 `{}`）。
- 脚本（bash）：语法正确，`set -e` + case 语句 + here-doc 结构完整；UTF-8 编码下的 emoji（✅⚠️）与 box-drawing 字符（╔═╗）在现代终端正常，但注意语料库存在 `fix_box_chars.py` 先例——box 字符在其他 skill 中曾被当作问题处理过，脚本中保留此类字符在旧终端/Windows 传统编码下可能乱码（风险低，建议保持）。
- 拼写：正文未发现明显拼写错误；英文大小写使用规范。

### 6.2 碎片文件（11 个）

- additional-context.md 第 5 行孤立 ```；coverage-matrix.md 第 8 行孤立 ```；next-steps.md 第 5 行孤立 ``` 且第 7 行有未闭合的 "```markdown"；examples.md 整体（5 行）就是一个未闭合的 details + 未闭合的围栏开头；tc-login-001 末尾 3 行孤立 ``` 与两个无配对 </details>。
- additional-context.md 末尾截断于列表项半行（"**Environment:** Staging" 后无内容）；examples.md 截断于 "```markdown"；test-cases-by-priority.md、summary.md 等微型文件以表格/列表裸结尾。
- 结论：11 个碎片中有 6 个存在明确的语法断裂，其余 5 个虽语法自洽但内容残缺。这些文件作为 markdown 文档在渲染器与阅读者（agent）面前都是"半成品"。

### 6.3 其他格式问题

- SKILL.md "How It Works" 的孤立 "-"（见 3.2 缺陷二）。
- 术语不统一：SKILL.md 用 "Pre-conditions"，test_case_templates.md 用 "Preconditions"，README 两种混用。
- 文件行尾：LF，无 BOM，符合规范。

---

## 7. 规范合规审查（SKILL-SPEC.md §5 十二项检查表）

| # | 检查项 | 判定 | 依据 |
|---|--------|:----:|------|
| 1 | name：小写+连字符，≤64 字符，匹配目录 | ✅ | `qa-test-planner` 匹配 `278-qa-test-planner` |
| 2 | description：第三人称，含 WHAT+WHEN+KEYWORDS，≤1024 字符 | ✅ | 约 380 字符，三类要素齐全；SKILL-SPEC §2.6 将其列为 Good 示例 |
| 3 | description：无祈使/第一/第二人称开头 | ✅ | "Generate comprehensive test plans..." 虽为动词开头，但属无主语的 WHAT 陈述句式，与规范自身的 Good 示例完全一致 |
| 4 | description：无内嵌跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 表述 |
| 5 | description：至少一个 trigger 信号短语 | ✅ | "Use when the user asks to..." |
| 6 | frontmatter：无允许列表之外的键 | ✅ | 仅 name + description |
| 7 | body ≤600 行 | ✅ | 400 行（tool pattern 目标 ~300 行，超出目标但合规） |
| 8 | body 含 workflow/process 节 | ✅ | "How It Works"（ANALYZE/GENERATE/VALIDATE）——但内容单薄，见 3.1 |
| 9 | body 含 output format 节 | ✅ | "Core Deliverables" 五类交付物清单 + 三个 deep dive 模板 |
| 10 | body 含 scope/limitations 节 | ❌ | **缺失**。全 body 无"本 skill 不做什么/何时不该用"的说明；"Patterns to Avoid" 是内容质量反模式，不构成 scope |
| 11 | body 无跨 skill 文件引用 | ✅ | 所有引用均为 skill 内相对路径 |
| 12 | 目录命名 NNN-kebab-case，无空格大写 | ✅ | `278-qa-test-planner` |

**合规结果：11/12 通过，1 项失败（第 10 项 Scope/Limitations 缺失）。** 这是 12 项中唯一的硬性违规。另有两个灰色地带（不构成合规失败但值得记录）：body 400 行超出 tool pattern 目标行数约 1/3；How It Works 作为 workflow 节内容过薄，几乎不携带流程决策信息。

---

## 8. 人机感审查

### 8.1 语气与表达

- 全文专业中性，无说教口吻，无过度拟人化。README 结尾的 Dijkstra 与亚里士多德引言（"Testing shows the presence, not the absence of bugs." / "Quality is not an act, it is a habit."）给工程文档增添了一点人文温度，位置得体。
- 无 emoji 滥用：SKILL.md/README/参考指南均无 emoji；脚本内的 ✅⚠️ 属于交互终端 UX 的一部分，可接受。
- 无第一/第二人称的越界（body 全部为客观陈述），人机边界清晰——skill 是"给 agent 的指令"而非"替用户发言"。

### 8.2 用户视角体验

- 正面：Quick Start 的五句话术、README 的五个完整示例（输入→输出预期）让用户对"能得到什么"有清晰预期；脚本的彩色分步向导（Step 1-7 明确编号）+ 完成后的 "Next steps" 提示是良好的 CLI 交互设计；脚本对必填/选填输入有区分并循环校验，用户不会因为误回车丢失输入。
- 负面：How It Works 的残破流程图是第一眼就能看到的"做工粗糙"信号；SKILL.md 以机器生成风格的文件名列表（"Tc Login 001 Valid User Login"）收尾，阅读体验突兀；术语 Pre-conditions/Preconditions 混用会削弱文档的权威感。

### 8.3 Agent 视角体验

- 正面：三阶段工作流 + 折叠 deep dive + 四份高质量指南的分层设计清晰，agent 可按需加载；Verification Checklist 提供了明确的输出自查标准。
- 负面：11 个碎片文件是"假参考文档"——agent 按 References 线索打开它们时得到的是断裂的 markdown 和与正式指南重复的内容；"## Reference Files" 列表暗示这些碎片是重要文档，实际不是。这属于对 agent 的误导性信号。

### 8.4 评价

整体人机感中上：专业、克制、有温度，交互脚本体验良好；扣分项集中在残破流程图、脚手架残留列表与碎片文件的误导性上。

---

## 9. 可执行性审查

### 9.1 脚本可执行性

- **generate_test_cases.sh**：功能完整。交互收集 10 项输入（ID/标题/优先级/类型/耗时/目标/前置条件/步骤/测试数据/Figura 与边界信息），生成结构完整的测试用例 markdown（含 Execution History 表与 Attachments 清单）；必填校验、优先级与类型的 case 默认值兜底、文件名清理（`${FILENAME//[^a-zA-Z0-9_-]/}`）、输出目录参数、UI 类型的条件式 Figma 区块——脚本逻辑经逐行推演可正常运行。`set -e` 在 `read` 非交互场景（无 stdin）下会直接退出，可接受。
- **create_bug_report.sh**：结构同上，自动生成 BUG-ID（`date +%Y%m%d%H%M%S`）、环境信息五连问、复现步骤循环、期望/实际行为必填。**缺陷**：Type 字段恒为 Functional（见 4.2）。另有 **eval 注入风险**：两个脚本都用 `eval "$var_name=\"$input\""` 实现变量赋值——用户输入如果包含 shell 元字符（如 `"; rm -rf ...; "` 或 `$(...)`），eval 会执行它。交互式场景下风险有限（使用者是自己），但作为面向团队的 skill 这是应避免的写法（用 `declare` 或关联数组即可替代）。此外脚本通过 `read` 收集多行输入（前置条件/复现步骤）时无提示符前缀，用户连续输入时看不到"当前在第几行"的反馈，属轻微 UX 问题。
- **Windows 环境**：两脚本为 bash，在 Claude Code 默认的 Git Bash 下可直接运行；`./scripts/...` 的 README 用法在 Windows 上需 bash 环境，与实测环境一致。

### 9.2 检查器可执行性

- check.py 可独立运行且输出合法 JSON（空对象 `{}`）。SCORING.yaml 的 17 个检查项全部为 `judge: llm`，与 check.py 的 "0 script checks" 一致——结构自洽，无"SCORING 声明了 script check 而 check.py 未实现"的断裂（这是其他 skill 常见的问题，本 skill 没有）。
- 代价：全部 17 项依赖 LLM 判断，没有任何可自动验证的硬性检查（如产物文件存在性、模板字段存在性）。对 QA 类 skill，至少可加 1-2 项 `file_contains` 类检查（如测试用例文件包含 "**Expected:**"、bug 报告包含 "## Steps to Reproduce"），提升评分的客观性。

### 9.3 交付物可执行性

- SKILL.md 的模板全部可直接复制使用：测试用例模板（步骤含 Expected 断言）、测试计划模板（含退出标准）、bug 报告模板（含环境/复现/证据/影响）。agent 照模板产出即可交付，无"不可执行的伪代码"或虚构工具调用。
- Figma 校验流程依赖 Figma MCP server 可用性——指南已写明前提条件与 DevTools 降级路径（不依赖 MCP 也能手测），降级路径存在，可执行性不悬空。
- 唯一的"执行盲区"：How It Works 没有给 agent 提供"从用户请求判定交付物类型"的决策规则（SCORING SCOPE-01/03 的考察点），只能靠 agent 的常识判断。这不阻塞执行，但把本该由 skill 承担的判定责任外包给了模型。

---

## 10. SCORING 交叉参考

SCORING.yaml 共 17 个 criteria（total_items: 17 与文件内计数一致）+ 3 个 critical_failures，pattern 分类为 tool。逐一将检查点与 skill 文件中的证据位置对应如下：

| 检查项 | 类别 | 证据位置 | 覆盖判定 |
|--------|------|----------|:--------:|
| SCOPE-01 识别交付物类型 | scope | SKILL.md Quick Start / Commands / Core Deliverables | ✅ |
| SCOPE-02 仅显式请求时激活 | scope | SKILL.md L10 Activation 声明 + description 触发短语 | ✅ |
| SCOPE-03 先分析后产出 | scope | SKILL.md How It Works 阶段 1 (ANALYZE) | ✅（内容薄，仅三个要点） |
| PROC-01 测试计划七要素 | process | SKILL.md Deep Dive: Test Plan Template + Core Deliverables #1 | ✅ |
| PROC-02 测试方法四件套 | process | Deep Dive 的 Test Approach（黑盒/正负/边界值/等价类） | ✅ |
| PROC-03 量化退出标准 | process | Deep Dive Exit Criteria（90%+、无 critical） | ✅ |
| PROC-04 测试用例标准格式 | process | Deep Dive: Test Case Structure + test_case_templates.md | ✅（标尺与模板双源，见 4.1） |
| PROC-05 边界用例 | process | test_case_templates.md Edge Cases 表 | ✅ |
| PROC-06 测试数据提供 | process | 模板 Test Data 节 + 脚本 Test Data 步骤 | ✅ |
| PROC-07 每步含 Expected | process | 两处模板 + 两示例用例 | ✅ |
| PROC-08 回归三层结构 | process | Core Deliverables #3 + regression_testing.md | ✅ |
| PROC-09 bug 报告模板 | process | Deep Dive: Bug Report + bug_report_templates.md | ✅ |
| PROC-10 严重度/优先级定义 | process | bug_report_templates.md 严重度表 + additional-context.md（碎片） | ✅（注意：一处证据在碎片文件中，若碎片被删除需迁移） |
| PROC-11 Figma 规格对比 | process | figma_validation.md 全篇 | ✅ |
| PROC-12 差异→bug+Figma 链接 | process | figma_validation.md 差异记录节 | ✅ |
| OUT-01 交付物无占位/模糊 | output | Verification Checklist | ✅ |
| NEG-01 无模糊步骤等反模式 | negative | Patterns to Avoid 表 | ✅ |
| CF-01/02/03 三类 cap_to_0 | critical | 与 NEG-01/OUT-01 重叠，语义强化，合理 | ✅ |

**交叉结论**：17 + 3 项检查全部能在 SKILL.md 与 4 个正式指南中找到支撑证据，SCORING 与 skill 内容整体吻合，没有"检查点要求了但 skill 完全没有"的空洞项，也没有"skill 核心能力但 SCORING 未测"的重大遗漏（性能/安全模板、脚本、报告模板属于 SCORING 之外的丰富化内容，不要求覆盖）。需要记录的三点：

1. PROC-04 与 PROC-09 的检查描述使用 "TC-ID, priority..." 与 "specific title..." 等措辞，与 SKILL.md Deep Dive 的模板措辞略有出入，但语义一致；而 Deep Dive 的 Priority 标尺（High/Medium/Low）与 SCORING 期望的 P0-P3 不一致（见 4.1）——这是 SCORING 与 SKILL.md 之间唯一的实质性语义偏差，修复 SKILL.md 模板即可消除。
2. PROC-10 的严重度定义一处证据（additional-context.md）位于碎片文件中——若执行第 13 节的碎片清理，需确认 bug_report_templates.md 已覆盖该定义（已覆盖：Severity Definitions 表在 bug_report_templates.md 中存在）。
3. check.py 与 SCORING 自洽（全部 llm），但零 script check 意味着评测完全依赖 LLM 主观判断——对 17 个检查项中的模板结构类项目（PROC-04/07/09 的字段存在性）本可脚本化。

---

## 11. 预留章节（跳过）

（本审查按任务模板预留第 11 节编号，无既定内容，跳过。）

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | name/description 双字段均合规；description 是 SKILL-SPEC 官方 Good 示例；"Includes Figma MCP integration" 属轻微的实现细节倾向，可移入 body |
| Body 结构完整 | 7/10 | 10% | 0.70 | 主要章节齐全（Quick Start/工作流/交付物/反模式/检查清单/3 deep dive），但 Scope/Limitations 缺失、How It Works 图残破、400 行超出 tool 目标 |
| 逻辑一致性 | 6/10 | 20% | 1.20 | 核心流程一致；但优先级/状态/类型三套枚举双源、create_bug_report.sh Type 恒为 Functional、README 结构树滞后 11 个文件 |
| 参考完整性 | 5/10 | 15% | 0.75 | 4 个正式指南质量高（合计 1,569 行）；11 个碎片中 6 个格式断裂、9 个无独立价值、内容与指南大量重复 |
| 语法格式 | 6/10 | 10% | 0.60 | 主体文件干净；碎片文件孤立围栏/未闭合 details/截断句共 6 处以上；术语混用 |
| 规范合规 | 8/10 | 15% | 1.20 | 12 项检查 11 过 1 挂（Scope/Limitations 缺失）；灰色地带：workflow 节过薄、行数超 target |
| 人机感 | 7/10 | 10% | 0.70 | 专业克制有温度、脚本交互体验好；残破流程图、机器风文件名列表、碎片误导性拉低印象 |
| 可执行性 | 7/10 | 10% | 0.70 | 两脚本功能完整可跑、check.py 自洽可跑、模板即拷即用；Type 恒 Functional bug、eval 注入风险、零 script check |
| **加权总分** | | | **67.5/100** | |

### 12.2 评级

**B- (67.5/100)** — 功能完整、核心资产（4 个正式指南 + 3 个 deep dive 模板）质量高，SCORING 与内容吻合度高；扣分集中于规范化副产物（11 个碎片文件、脚手架残留列表）与若干标尺/枚举不一致。修复第 13 节的 🔴 项后可升至 B+/A- 区间。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**1. 补充 Scope/Limitations 节（SKILL.md 缺失，规范 12 项中唯一失败项）**
- 位置：SKILL.md 中 "Patterns to Avoid" 之后、Verification Checklist 之前。
- 修复方向：新增 `## Scope / Limitations` 节，至少声明：本 skill 生成测试文档而非执行测试或管理测试环境；Figma 校验依赖 Figma MCP server 可用（无 MCP 时按 figma_validation.md 的 DevTools 手动降级路径）；自动化测试（CI/框架脚本）不在范围内；测试执行与缺陷生命周期管理（指派/关闭/验证）由团队工具（Jira/TestRail 等）承担。
- 不修复后果：SKILL-SPEC §3.1 合规检查不合格，且 agent 会在无 MCP 或无 Figma 权限的环境里对 Figma 校验能力产生错误预期。

**2. 处理 11 个切分碎片文件（推荐的单一方案：清理而非修复）**
- 位置：references/ 下 additional-context.md、coverage-matrix.md、tc-login-001-valid-user-login.md、tc-ui-045-mobile-navigation-menu.md、next-steps.md、test-cases-by-priority.md、summary.md、examples.md、critical-failures.md、risks.md、blocked-tests.md。
- 修复方向（二选一）：
  - 方案 A（推荐）：删除全部 11 个碎片，同步移除 SKILL.md 末尾的 "## Reference Files" 脚手架列表，并把 README 的 Skill Structure 树更新为实际的 4 个指南 + 2 个脚本。碎片中的独有内容仅两处有保留价值：regression_testing.md 已含执行报告模板（无需迁移）；若想保留测试用例示例，可将 tc-login-001 / tc-ui-045 各约 45 行合并进 examples 性质的位置或直接删除（SKILL.md 模板已自带示例）。
  - 方案 B（保留碎片）：逐文件修复格式断裂（additional-context 第 5 行孤立 ```、examples.md 截断于 "```markdown"、next-steps 的孤立/未闭合围栏、tc-login-001 末尾孤立 ``` 与无配对 </details>、coverage-matrix 第 8 行孤立 ```、additional-context 截断的 Test Execution Tracking），并在 SKILL.md References 节正式列出全部文件。此方案成本高且碎片内容与正式指南重复，仅当碎片承载独有信息时才值得。
- 不修复后果：仓库携带 6 个以上 markdown 语法断裂文件；agent 按 References 线索读到半成品文档，浪费 token 并可能误以为存在未读内容；评测输出目录（outputs/）会把这些碎片原样转换到 5 种 harness 格式，放大问题面。

**3. 修复 create_bug_report.sh 的 Type 字段（真 bug）**
- 位置：scripts/create_bug_report.sh 第 158 行。
- 修复方向：删除 `${TEST_TYPE:-Functional}` 这行 Type 输出，或在脚本中增加类型选择的交互步骤（与 generate_test_cases.sh 的 6 类 case 一致）。若走删除路线，建议同时在 `## Environment` 之后保持模板与 bug_report_templates.md 对齐。
- 不修复后果：所有脚本生成的 bug 报告 Type 恒为 Functional，性能/UI bug 被错误归类，测评中 PROC-09 若抽样脚本产物将直接失分。

### 🟡 重要缺陷（建议修复）

**4. 统一优先级/状态/类型三套标尺（SKILL.md vs test_case_templates.md）**
- 位置：SKILL.md Deep Dive: Test Case Structure（约 200-202 行）与 Deep Dive: Bug Report（约 344-347 行）。
- 修复方向：以 references/test_case_templates.md 为准，将 SKILL.md 的 "Priority: High | Medium | Low" 改为 "P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)"；Status 改为 "Not Run | Pass | Fail | Blocked | Skipped"；bug Status 与 Type 枚举同步对齐。
- 理由：消除与 SCORING PROC-10、正式指南、示例用例（P0/P1）的三方冲突。

**5. 修复 "How It Works" 残破流程图**
- 位置：SKILL.md 60-62、79 行。
- 修复方向：将两个孤立 "-" 替换为实际的流程示意（如 "Your Request → [1. ANALYZE → 2. GENERATE → 3. VALIDATE] → QA-Ready Deliverable" 的单行流程，或删除图示只保留编号列表）。
- 理由：这是用户/agent 第一眼看到的章节，残破图直接影响对 skill 质量的观感。

**6. 移除或转正 SKILL.md 末尾的 "## Reference Files" 脚手架列表**
- 位置：SKILL.md 389-401 行。
- 修复方向：若采纳修复建议 2 方案 A，直接删除该列表；若保留部分碎片，则把列表改造成正式的 References 小节（放入第 8 节 References 中统一管理），并用正常大小写文件名。
- 理由：当前列表是切分工具的机械产物，文件名大写化（"Tc Login 001 Valid User Login"）与全文档风格冲突。

**7. 消除脚本中的 eval 注入风险**
- 位置：两个脚本的 prompt_input 函数（约 33 行）。
- 修复方向：用 `declare -- "$var_name=$input"` 或 `read -r "$var_name"` 直接读取替代 `eval`；或在赋值前过滤 shell 元字符。
- 理由：面向团队的 skill 不应内置命令注入通道；`eval` 也是代码评审必然被挑战的写法。

**8. 更新 README 的 Skill Structure 树与 SKILL.md References 节**
- 位置：README.md 297-311 行、SKILL.md 182-188 行。
- 修复方向：与实际的 15 个 references 文件（或修复后的数量）保持一致；References 节按"正式指南 + 示例/数据文件"分组列出。
- 理由：三处文件清单不一致会误导 agent 的资源规划。

**9. 修正脚本提示文本与术语**
- 位置：generate_test_cases.sh 前置条件提示（"press Enter twice when done"→"press Enter once when done"）、两个脚本的 Type 缺失提示（见修复 3）、SKILL.md 的 "Pre-conditions" 统一为 "Preconditions"（与指南一致）。
- 理由：细节一致性成本低、收益直接。

**10. 为 SCORING 增加 1-2 项 script check（可选但推荐）**
- 位置：check.py 与 SCORING.yaml 的 check 字段。
- 修复方向：给 PROC-04/07/09 增加 `file_contains` 类检查（如产物含 "**Expected:**"、含 "## Steps to Reproduce"），使 17 项 llm judge 中至少有 2-3 项可自动验证。
- 理由：当前评测 100% 依赖 LLM 判断，模板结构类检查完全可以脚本化，提升评分稳定性与可复现性。

### 🟢 优化建议（锦上添花）

**11. description 中 "Includes Figma MCP integration" 移入 body**
- 与 001-skill-tuning 的 Gemini CLI 先例对齐；Figma 能力已在 Core Deliverables #4 与 figma_validation.md 中充分体现，description 保留纯 WHAT+WHEN 更干净。非强制。

**12. SKILL.md 回归套件补充 Sanity 层 + Bug 报告验证清单补充 Impact 项**
- 使 SKILL.md 与 README/regression_testing.md 的四层结构一致；使 Verification Checklist 与 SCORING PROC-09 的 impact 要求对齐。

**13. 示例文件类型标签统一**
- tc-ui-045 的 "UI/Responsive" 改为命名表中的 "UI/Visual"（若保留该碎片），保持类型枚举唯一。

**14. 碎片数据文件的迁移（若采方案 B）**
- blocked-tests/critical-failures/risks/summary/test-cases-by-priority 六个微型文件若保留，建议合并为一个 `references/example-execution-data.md`，避免 1-8 行的"文件碎片"继续存在。

### 修复工作量估计
- 方案 A（推荐）：修改 3 个文件（SKILL.md 删列表 + 补 Scope + 修标尺与流程图；README 更新结构树；create_bug_report.sh 删 Type 行），删除 11 个文件，预计净减少约 400 行，改动风险低。
- 方案 B：修复 6 个文件的格式断裂 + 迁移 6 个微型文件，预计耗时约为方案 A 的 3 倍且收益更低。

---

## 附录: 审查过程记录

- 读取文件数：21（SKILL.md + README.md + SCORING.yaml + check.py + 15 references + 2 scripts）
- 读取总行数：约 3,500 行（全部全文读取，无抽样）
- 重点深度审查：SKILL.md 全文逐节、11 个碎片文件的格式断裂逐处定位、两个脚本的变量流逐行推演、SCORING 17 项检查点逐项映射证据位置
- 关键证据：文件时间戳（SKILL.md 与 11 个碎片同为 2026-08-05 18:15 修改；README/脚本/4 指南为 2026-07-31）；SKILL.md 末尾机械风格 Reference Files 列表；碎片间内容顺序可重建（尾部引言与 README 重复）
- 对照基准：`_shared/SKILL-SPEC.md`（12 项合规检查表）、`_shared/checker.py`（check.py 依赖库）、001-skill-tuning/REVIEW.md（审查格式先例）、项目记忆 skillif-project.md / skillif-trigger-design.md（规范化与 trigger 决策上下文）
- 变更记录：2026-08-06 初始深度审查，产出本文件
