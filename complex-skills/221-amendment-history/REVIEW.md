# Skill 221 — amendment-history 审查报告 (REVIEW)

> 审查日期: 2026-08-06
> 审查对象: `D:\SkillIF\skill-experiment\complex-skills\221-amendment-history\`
> 审查方式: 逐文件全文阅读 + 实证验证（YAML 解析、正则匹配、执行流模拟）
> 审查者: Claude (SkillIF 质量审查)

---

## 1. 审查概要

### 1.1 审查范围

本次审查覆盖技能目录内的全部 3 个文件，以及其运行所依赖的 1 个共享库文件，共 4 个文件全文阅读：

| 文件 | 行数 | 角色 |
|------|:----:|------|
| `SKILL.md` | 293 | 技能本体：frontmatter + 指令正文 |
| `SCORING.yaml` | 184 | 测评设计：20 个 0/1 检查项 + 3 个 critical failure |
| `check.py` | 74 | 可执行检测器：脚本判定项的实现 |
| `_shared/checker.py`（外部依赖） | 351 | 公用检测函数库（20 个函数） |

审查方法为：Glob 枚举 → 全文 Read → 对关键疑点做实证验证（YAML 合法性、正则可匹配性、
main()/check() 执行流模拟、跨文件一致性比对），最终产出本报告。

### 1.2 结论摘要

- **技能正文 (SKILL.md)**：逻辑自洽、语法干净、人机感专业、规范合规，质量优秀，评级 🟢。
- **测评设计 (SCORING.yaml)**：结构完整、条目与技能内容可追溯性极强，评级 🟢。
- **检测器 (check.py)**：**存在一个必然导致 FMT-02 恒为 False 的执行流缺陷**（实证复现），
  且该缺陷在 322 个技能的 check.py 中普遍存在（已确认 321/322 个文件含同一模式），评级 🟠。
- **总体评级**：🟢（技能本体）+ 🟠（测评工具链需修复一处关键 bug）。

### 1.3 审查批次定位

对照 skill-dossier 的 201-225 批次记录，该技能此前未单独建档（dossier 中 201-225 为摘要
覆盖）。本次审查补全了该技能的完整档案。技能 pattern 为 `process`，属 160 个 process 型
技能之一，该 pattern 整体质量偏高（常见问题是缺 scope 节），本技能三节齐备、无缺节问题。

---

## 2. 文件清单与职责划分

### 2.1 SKILL.md — 技能本体

- Frontmatter 三个字段：`name: amendment-history`、`description`（第三人称 + 触发短语 +
  WHAT/WHEN 结构）、`argument-hint`。
- 正文 12 个节（含标题与 frontmatter 共 293 行，正文约 288 行，远低于 600 行上限）：
  1. 引言段（技能做什么）
  2. `## Instructions`（4 步总控：取文档 → 判模式 → 跑流程 → 提供后续）
  3. `## Examples`（3 个调用示例）
  4. `## Matter context`（事务所级上下文开关）
  5. `## Purpose`（背景与动机）
  6. `## Mode detection`（双模式判定规则 + 术语映射表 + 歧义处理）
  7. `## Step 1: Load and order the documents`（文档来源与排序规则）
  8. `## Privilege inheritance`（特权继承与 work-product 头）
  9. `## Step 2: Read and index`（建索引：类型/日期/当事方/变动条款）
  10. `## Mode 1: Summary of all changes`（汇总模式输出模板）
  11. `## Mode 2: Provision trace`（条款追踪模式输出模板）
  12. `## Close with the next-steps decision tree` + `## What this skill does not do`

### 2.2 SCORING.yaml — 测评设计

- 头字段：`skill: amendment-history`、`pattern: process`、`total_items: 20`。
- 20 个 criteria 分 6 类：scope(3) + process(5) + format(5) + technical(2) + negative(2) + qa(3)。
- 3 个 critical_failures，全部 `effect: cap_to_0`。

### 2.3 check.py — 可执行检测器

- 头注释声明调用约定：`python check.py <workspace> <tool_log> <agent_output>`，输出
  `{criterion_id: true/false}` JSON。
- 导入 `_shared/checker.py` 的 18 个函数（经核验全部存在，导入可解析）。
- 实际仅执行 1 项脚本判定：FMT-02（输出含 `§\d+\.\d+` 章节引用）；其余 19 项标注
  "llm judge (not checked here)"。

### 2.4 _shared/checker.py — 公用库（依赖，非本技能文件）

- 20 个函数：文件类 5、JSON 类 8、时间戳类 3、工具日志类 5、输出类 2（重复计算）。
- 本技能只用到 `output_contains`、`set_tool_log_path`、`set_agent_output` 三个。
- `output_contains` 行为：对空 `_agent_output` 返回 False（安全失败），正则使用
  `re.MULTILINE`。

---

## 3. 总体评价与评级

### 3.1 五维评级表

| 维度 | 评级 | 一句话结论 |
|------|:----:|-----------|
| 逻辑一致性 | 🟢 | 双模式流程与全部规则自洽，仅 2 处结构小瑕疵 |
| 语法与可读性 | 🟢 | 无错字、无病句、结构清晰 |
| 人机感 | 🟢 | 专业律师口吻，零 emoji、零填充语、门控提问克制 |
| 规范合规性 | 🟢 | frontmatter 合规、正文 ≤600 行、三节齐备、无跨技能路径 |
| 整体评价 | 🟢 | 优秀的法律流程类技能；配套检测器需修复一处必现 bug |

### 3.2 评分基准对照

- 正文行数 293（上限 600，安全裕度 51%）。
- Description 为第三人称陈述 + "Use when the user says ..." 触发短语列表，
  满足 WHAT/WHEN/KEYWORDS 结构，无祈使句开头、无第一/第二人称违规、无跨技能路由。
- workflow（Instructions + Step 1/2 + 双 Mode）、output（两套 markdown 模板）、
  scope（What this skill does not do）三节齐备。

### 3.3 与语料库基准比较

- 在 322 个技能中属于"三节齐备"的少数派（约 32% 达标率），且是法律类中结构与
  术语精度俱佳的样本，与 067-chronology、139-clearance、201-policy-diff 等
  标杆技能同级。
- 唯一拉低整体评级的因素不在技能本体，而在 check.py 的 FMT-02 必现失效 bug
  （详见第 9 节与第 11 节）。

---

## 4. 逻辑一致性审查

### 4.1 总体判定

🟢 技能的执行逻辑（取文档 → 判模式 → 排序 → 建索引 → 按模式出模板 → 收尾决策树）
全程闭环、无矛盾，且"边界行为"（何时问、何时不问）定义得异常清晰。

### 4.2 指令与控制流核对

- `Instructions` 第 2 步说"有明确条款名直接进 Mode 2，无条款名跑 Mode 1，仅真正歧义才问"，
  `Mode detection` 节给出完全一致的触发短语与歧义处理模板（列出候选条款并问
  "I found [N] provisions related to [term] — [list them]. Which one?"）。前后一致 ✓。
- `Instructions` 第 1 步"无文档则问"与 `Step 1` 的"Only ask the user to confirm ordering
  if ..."三条件（文件名无序列信息 / 日期缺失 / 疑似重复版本）严格对应 ✓。
- 排序规则链：执行日期（元数据）→ 文档头部/recitals 日期 → 交叉引用确认链条；
  规则之间无冲突，且"推断而非确认时只在不确定处标注置信度"的粒度定义合理 ✓。
- `Step 2` 提取四要素（类型/日期/当事方/变动的条款）与 Mode 1、Mode 2 的输出所需
  信息完全匹配（Mode 1 需要变动清单，Mode 2 需要引用原文）✓。
- `What this skill does not do` 四条边界与正文行为一致：不做冲突裁决（只 flag 并路由
  Legal）、不起草修订、不对比 playbook（归 vendor-agreement-review）、不解读歧义条款
  （只原样引用并 flag）✓。
- `Privilege inheritance` 要求每个输出加 work-product 头、仅限特权圈内分发、外部交付
  前剥离，与 TEC-01 测评点一致 ✓。

### 4.3 结构瑕疵（轻微）

1. **`## Privilege inheritance` 插入位置打断编号流程**：该节位于 `## Step 1` 与
   `## Step 2` 之间，是一段无步骤编号的"上下文/护栏"内容夹在编号步骤中间。
   读者按 Step 1 → Step 2 阅读时会被特权说明打断。建议移到 `Matter context` 附近
   （二者同为上下文类），或与 `Close with the next-steps decision tree` 合并为
   "Guardrails" 分组。
2. **步骤编号只到 Step 2**：`Instructions` 第 3 步说"Run the workflow below"，
   但正文中 Mode 1 / Mode 2 / Decision tree 均无步骤编号，编号体系到 Step 2 中断。
   建议改为 Step 3（按模式产出）、Step 4（收尾决策树），或去掉 Step 编号改纯节标题，
   二者取一，保持体系一致。
3. **边缘场景未覆盖**：未定义"只上传了修订件没有主合同"、"主合同晚于修订件"、
   "两份文档实际是同一版本"等异常输入的处理路径（`Step 1` 只处理了"疑似重复版本
   需询问"，但没定义确认后如何继续）。属建议级补充，不影响主流程。
4. **`Purpose` 与引言段轻度重复**：引言段（L6-10）与 `Purpose`（L54-61）表达同一件事
   （合同累积修订后无人记得原文）。可保留（Purpose 偏背景、引言偏功能），仅提示。

---

## 5. 语法与可读性审查

### 5.1 总体判定

🟢 英文全文专业规范，未发现拼写错误、病句或标点滥用。

### 5.2 逐项检查

- 术语一致性：`base agreement` / `amendment` / `addendum` / `provision` / `section` 等
  词汇全篇统一，未混用 `clause` 指代不一致概念（`clause` 仅在触发短语中作为用户
  口语出现，符合语境）。
- 模板占位符风格统一：`[date]`、`[X.X]`、`[N]` 均用方括号，无花括号/双花括号混用。
- 输出模板中的格式锚点（`**Base agreement:**`、`---` 分隔线、`### Amendment N`、
  `## Net current state`、`## Watch items`）在各模式下命名一致，无重复定义。
- 箭头符号 `→` 与破折号 `—` 用法一致（时间范围用 `→`，注释性插入用 `—`）。
- 引号使用：用户话术块使用 `>` 引用块 + 英文双引号，代码示例用围栏块，层次分明。
- 无中文/葡语等其他语言混入（对照语料库中其他技能常见的混排问题，此处无）。
- 无临时脚手架残留（对照 004 的 "(New!)"、032 的 "Nano Banana Pro" 等先例，
  本技能仅有 "[CLM ID (coming soon)]" 与 "[repository link (coming soon)]" 两处
  产品路线图占位，属可接受的商业文档惯例，且被 `argument-hint` 与正文一致引用）。

### 5.3 可读性结构

- 文档以"总控（Instructions）→ 规则（Mode detection / Step 1）→ 模板（Mode 1/2）"
  的倒金字塔组织，律师用户可以只看 Mode 模板即可理解交付物形态。
- 每个 Mode 均自带"输出格式模板 + 边界行为（什么时候省略/跳过）"的成对结构，
  可读性佳。
- 唯一可读性减分项：第 4.3.1 条所述的特权节插入位置（读者流程感断裂）。

---

## 6. 人机感审查

### 6.1 总体判定

🟢 专业律师助理口吻，零 emoji、零填充语、零全大写喊叫（对照 072-mobile-design 的
20+ emoji 与 "STOP!" 命令式问题，本技能是反面典范的另一端）。

### 6.2 逐项检查

- **提问克制**：全技能只有两类提问——无文档时问要文档、真歧义时问选哪个模式/哪个
  条款，且都给出"尽量不问"的前置条件（"proceed without asking"、"genuinely
  ambiguous"）。人机边界成熟。
- **确定性输出**：Mode 2 明确"Show only what changed. Do not list amendments where
  the provision was untouched — skip them entirely."，把"该省则省"变成规则而非风格，
  避免 Agent 输出冗长。
- **法律风险意识恰如其分**：特权继承、律师做裁决 Agent 只 flag、原文引用不解读，
  三个护栏都与"法律 AI 助手"的角色定位一致，无越界承诺。
- **无推销/无营销腔**：无 K-Dense 式外部产品植入（对照 007 的问题）、无 "world-class"
  式自我标榜（对照 083-085 的问题）。
- **用户话术示例真实**：如 "What changed in this contract over time"、
  "where's the latest [clause]" 均为真实律师提问口吻，利于触发匹配与示例理解。
- **决策树收尾**：明确"树是输出，律师做选择"（"The tree is the output; the lawyer
  picks."），职责边界一句话说清，人机感上乘。

### 6.3 轻微观察

- `Instructions` 第 4 步的后续建议三连问（再追一条 / 全量审查 / 利益相关方摘要）
  略显流程化，但作为"标准后续"符合律所工作流惯例，可接受。

---

## 7. 规范合规性审查（对照 SKILL-SPEC）

### 7.1 Frontmatter

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| `name` 与目录名/技能名一致 | ✅ | `amendment-history` = 目录 `221-amendment-history` 的后缀 |
| `description` 第三人称 | ✅ | "Trace how a contract has changed..." |
| `description` 含触发信号 | ✅ | "Use when the user says..." + 5 组触发短语 |
| `description` 无跨技能路由 | ✅ | 未提及任何 `/skill-name` 或 `@skill` 引用 |
| `description` 无祈使句开头 | ✅ | 以动词 Trace 开头的陈述句 |
| `argument-hint` 存在 | ✅ | 含文件/CLM ID/repository 三来源 + `--provision` 参数 |
| 无非标准键 | ✅ | 仅 name/description/argument-hint 三键 |

### 7.2 正文结构

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 行数 ≤ 600 | ✅ | 293 行（含 frontmatter） |
| workflow 节 | ✅ | Instructions + Step 1/2 + 双 Mode 构成完整流程 |
| output 节 | ✅ | 两套完整 markdown 输出模板 |
| scope/limitations 节 | ✅ | `What this skill does not do` 四条边界 |
| 无跨 skill 文件路径 | ✅ | 仅按名称引用 vendor-agreement-review / stakeholder-summary |
| 配置路径引用合规 | ✅ | 3 处引用 `~/.claude/plugins/config/claude-for-legal/commercial-legal/CLAUDE.md`，属允许的配置路径 |
| 相对路径/自引用 | ✅ | 无对 `../` 或 `skills/...` 的跨目录引用 |
| emoji/装饰性标记 | ✅ | 全篇零 emoji |

### 7.3 与语料库常见违规对照

本技能未命中语料库 Top 问题类型中的任何一类：不缺 scope 节（~68% 技能有该问题）、
不缺 output 节（~56%）、description 无违规（~11%）、无逻辑矛盾、无引用缺失、
无截断、无编号断裂。合规性属于语料库前 1/3 水平。

---

## 8. SCORING.yaml 测评设计审查

### 8.1 结构完整性

- 20 个 criteria 与 `total_items: 20` 一致（经验证）。
- 6 类目（scope/process/format/technical/negative/qa）与检查项内容分类吻合。
- 全部条目含 `id`/`category`/`description`/`judge`/`check` 五要素，ID 无重复
  （经验证）。
- 唯一脚本项 FMT-02 声明 `judge: script`、`fn: output_contains`、
  `pattern: '§\d+\.\d+'`，与 check.py 实现完全一致（经逐字符比对）。

### 8.2 条目与技能的映射可追溯性（Traceability）

逐条验证结论：**20/20 个条目均能在 SKILL.md 中找到对应的明确指令**，无凭空条目。

| 测评点 | 对应 SKILL.md 内容 | 一致性 |
|--------|-------------------|:------:|
| SCOPE-01 | Purpose / 引言段（tracing changes across base + amendments） | ✅ |
| SCOPE-02 | Mode detection 节（判模式、仅真歧义才问） | ✅ |
| SCOPE-03 | Instructions 第 1 步（多文件接收、无文件则问） | ✅ |
| PROC-01 | Step 1 排序规则（先排序后读内容） | ✅ |
| PROC-02 | Step 1 三条件询问 + 置信度标注 | ✅ |
| PROC-03 | Step 2（按时间序读取、建索引四要素） | ✅ |
| PROC-04 | Step 2 当事方核对与 flag | ✅ |
| PROC-05 | Mode detection 歧义条款候选列表 + 询问模板 | ✅ |
| FMT-01 | Mode 1 输出模板（头部/chronological/Net table/Watch） | ✅ |
| FMT-02 | Section reference rule（每条 finding 带 § 引用） | ✅（实现有 bug，见 8.4） |
| FMT-03 | Mode 2 模板（Original/Was/Now/Current/Watch） | ✅ |
| FMT-04 | Mode 2 "skip untouched" + "original language controls" 话术 | ✅ |
| FMT-05 | Watch items 四类典型不一致 + 引用要求 | ✅ |
| TEC-01 | Privilege inheritance 节 | ✅ |
| TEC-02 | "quotes exactly and flags ambiguity" | ✅ |
| NEG-01 | What it does not do 第 1、2 条 | ✅ |
| NEG-02 | What it does not do 第 3 条 | ✅ |
| QA-01 | Instructions 第 4 步三连后续 | ✅ |
| QA-02 | Close with the next-steps decision tree 节 | ✅ |
| QA-03 | Step 2 "Build a working index ... do not show it to the user" | ✅ |

这是本技能测评设计最值得肯定的一点：20 个检查项与正文指令逐条对应，无"测了技能
没写的行为"或"技能写了但没测的行为"漂移。

### 8.3 Critical Failures 设计

- CF-01（无章节引用 → cap_to_0）：与 FMT-02 呼应，双保险设计合理。
- CF-02（引用不实 → cap_to_0）：与 TEC-02 呼应，对法律输出"引文即证据"的性质
  判定恰当。
- CF-03（追踪了未触及条款 → cap_to_0）：与 FMT-04 呼应，"show only what changed"
  是 Mode 2 的核心价值，设为致命失败合理。

### 8.4 设计缺陷与改进建议

1. **脚本判定覆盖过薄**：20 项中 19 项依赖 LLM judge，脚本仅 1 项。而 checker 库
   提供的 `tool_log_order`、`tool_log_read_before_write`、`timestamp_before` 等函数
   足以让 PROC-01（先排序后读）、PROC-03（按序读取、先建索引后输出）转为脚本判定，
   可大幅降低 LLM judge 的抖动。建议扩充。
2. **无特权泄露的致命失败**：TEC-01（work-product 头、特权圈内分发）仅是非致命
   检查项。对读取特权法律文档的技能，若 Agent 把特权输出发给圈外，后果远超
   "少写一个章节引用"。建议新增 CF：privilege header 缺失或分发范围违规 → cap_to_0。
3. **FMT-02 正则过窄**：`§\d+\.\d+` 要求"§ + 数字.数字"格式。若 Agent 输出
   "Section 9.1"、"§12"（整数节号）或合同使用非十进制编号（如 §1(a)），即使行为
   完全合规也会判失败（假阴性）。建议放宽为 `(§|Section\s+)\d+([.]\d+)?` 或
   `§\S*` 类宽松模式，并补充 no-trigger 对照集验证。
4. **QA-01 措辞笼统**：question 只说 "standard follow-ups"，未锚定技能定义的三个
   具体后续（再追踪一条 / 全量 playbook 审查 / 利益相关方摘要），LLM judge 可能
   对"任意后续"放行。建议在 question 中列出三项。

---

## 9. check.py 实现审查

### 9.1 总体判定

🟠 结构与调用约定正确，但存在一个**必现的 FMT-02 失效 bug**（经实证复现），且该 bug
为语料库系统性缺陷（321/322 个技能的 check.py 均含同一模式）。

### 9.2 已实证的缺陷：FMT-02 恒为 False

**根因（L24-27 与 L54-73 的双重 set_agent_output）：**

```python
# check() 内部（L26-27）—— 把"路径字符串"塞进 _agent_output
def check(workspace, tool_log, agent_output):
    set_tool_log_path(tool_log)
    set_agent_output(agent_output)   # ← bug：agent_output 是文件路径，不是内容

# main() 中（L62-66）—— 读取文件内容后调 check()，内容随即被上面一行覆盖
if os.path.exists(agent_output):
    with open(agent_output, "r", encoding="utf-8") as f:
        set_agent_output(f.read())   # ← 此处设置的内容在 check() 内被路径覆盖
results = check(workspace, tool_log, agent_output)
```

**执行流推演与复现结果：**

1. 按 docstring 约定 `python check.py <ws> <log> <output>` 运行 → main() 读取输出
   文件内容到 `_agent_output` → 调用 check() → check() 第一行用**路径字符串**覆盖
   `_agent_output` → FMT-02 的 `output_contains("§\d+\.\d+")` 实际在搜索文件路径。
2. 复现实验（本审查实测）：构造内容为 "Indemnification (§9.1): added." 的输出文件，
   走 main() 流程 → `{'FMT-02': False}`；即使用内容直接调用 check() 也会被路径参数
   覆盖 → `{'FMT-02': False}`；而单独用正确解析后的正则对同一内容做
   `re.search` → True（正则本身无误，是执行流把内容弄丢了）。
3. 结论：**在文档化的 runner 调用方式下，FMT-02 永远判 False**——这是脚本项的
   唯一判定，等于 20 个检查项全部实际不可自动化判定。

**修复方案（最小改动）：**

- 方案 A（推荐）：删除 check() 内 L27 的 `set_agent_output(agent_output)`，让
  main()（或 runner）设置的内容生效；同时把 main() 的读文件逻辑保留。
- 方案 B：main() 不读文件，把内容作为第三参传入 check()——但 docstring 约定的是
  路径，故方案 A 更贴合现有契约。
- 若 322 个 check.py 为批量生成，应在生成器（或批量脚本）中统一修复，而非逐个
  手改。建议修复后对全部 322 个技能回归：构造含 § 引用的假输出跑一遍 main()，
  断言 FMT-02 为 True。

### 9.3 其他实现观察（轻微）

1. **`workspace` 与 `tool_log` 参数完全未用**：check() 签名接收但从不引用，且本技能
   没有使用 `tool_log_*` 系列函数（PROC 类全部委托 LLM）。签名保留无害，但配合
   8.4-1 的建议（PROC-01/03 改脚本判定）可物尽其用。
2. **main() 对文件缺失的兜底**：`os.path.exists` 为 False 时静默跳过读取，FMT-02
   返回 False 而非报错。可接受（安全失败），但排查期易误判为"Agent 没写章节引用"。
3. **未用导入**：文件类/JSON 类/tool-log 类函数导入但未使用，属语料库统一模板的
   通用导入清单，非本技能独有问题，无害。
4. **注释与 SCORING.yaml 分类注释一致**：SCOPE/PROCESS/FORMAT/... 分段注释与
   SCORING 分类对齐，便于维护。

---

## 10. 跨文件一致性审查

### 10.1 三件套横向核对

| 核对项 | SKILL.md | SCORING.yaml | check.py | 一致? |
|--------|----------|--------------|----------|:-----:|
| 技能名 | `amendment-history` (L2) | `skill: amendment-history` (L1) | docstring `221-amendment-history` | ✅ |
| 模式数 | 双模式 (Mode 1/2) | SCOPE-02/FMT-01/FMT-03/FMT-04 | 无模式相关脚本项 | ✅ |
| 章节引用要求 | Section reference rule (L158-168) | FMT-02 + CF-01 | `output_contains` + 正则 | ✅（正则偏窄，见 8.4-3） |
| 引用忠实性 | "quotes exactly" (L292) | TEC-02 + CF-02 | 无脚本项 | ✅ |
| "只显示变化" | Mode 2 skip 规则 (L223-224) | FMT-04 + CF-03 | 无脚本项 | ✅ |
| 特权处理 | Privilege inheritance (L138-140) | TEC-01 | 无脚本项 | ✅ |
| 后续三连问 | Instructions 第 4 步 (L24-29) | QA-01 | 无脚本项 | ✅ |
| 决策树收尾 | L279-281 | QA-02 | 无脚本项 | ✅ |
| 工作索引不外显 | L152-153 | QA-03 | 无脚本项 | ✅ |

### 10.2 边界行为三方对齐

- "仅真歧义才问"：Instructions L18-20、Mode detection L65-91、SCOPE-02 三方措辞一致。
- "先排序后读"：Step 1 L127-135、PROC-01 一致。
- "不做裁决/不解读"：What it does not do L283-293、NEG-01/TEC-02 一致。
- 未发现任何"技能说 A、测评点测 B"的漂移。

### 10.3 对 no-trigger 对照集的影响（前瞻）

无 trigger 对照集将删除 description 中的触发短语。本技能 description 触发信号强
（5 组用户话术 + 2 个文件上传场景），删除后 Mode detection 仍要求 Agent 自行判
模式——对照集的判别力（无触发时是否仍被误触发/被正确拒用）设计空间充足。但注意
FMT-02 的 bug 若不修复，对照集与主集的脚本判定都会恒 False，无法区分任何差异，
修复应优先于对照集评测。

---

## 11. 发现的问题清单（按严重度分级）

### 11.1 严重（必须修复）

| # | 问题 | 位置 | 证据 | 影响 |
|---|------|------|------|------|
| S-1 | FMT-02 恒为 False：`set_agent_output` 双重设置导致内容被路径覆盖 | check.py L27 与 L62-64 | 实证复现：内容含 "§9.1" 的输出经 main() 流程判定 False；正则单独测试为 True | 唯一脚本项永远失效，20 项全部实际依赖 LLM judge |
| S-2 | S-1 为语料库系统性缺陷 | 322 个 check.py 中 321 个含 `set_agent_output(agent_output)` | grep 统计 | 全语料库脚本判定全部可能失效，需批量修复 + 回归 |

### 11.2 中等（建议修复）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| M-1 | FMT-02 正则过窄（`§\d+\.\d+` 不认 "Section 9.1" / "§12"） | SCORING.yaml L87、check.py L39 | 假阴性误判合规 Agent |
| M-2 | 无"特权泄露"致命失败（TEC-01 仅普通项） | SCORING.yaml L114-120 | 法律技能最高风险行为无 cap_to_0 兜底 |
| M-3 | 19/20 项依赖 LLM judge，PROC-01/03 可脚本化而未用 | SCORING.yaml L31-70、check.py L34-36 | LLM judge 抖动大、评测成本高 |

### 11.3 轻微（可选项）

| # | 问题 | 位置 |
|---|------|------|
| L-1 | `Privilege inheritance` 夹在 Step 1/Step 2 之间，打断编号流程 | SKILL.md L138-140 |
| L-2 | 步骤编号止于 Step 2，Mode 1/2 与收尾无编号 | SKILL.md L156/219/279 |
| L-3 | "只有修订件无主合同"等异常输入未定义处理路径 | SKILL.md L95-135 |
| L-4 | `Purpose` 与引言段轻度重复 | SKILL.md L6-10 vs L54-61 |
| L-5 | "[coming soon]" 产品路线图占位两处 | SKILL.md L3、L99-108 |
| L-6 | QA-01 question 未锚定三个具体后续项 | SCORING.yaml L150-155 |

---

## 12. 修复建议（按优先级排序）

### 12.1 P0 — 修复 FMT-02 执行流 bug（对应 S-1/S-2）

1. 在 221-amendment-history/check.py 的 `check()` 中删除
   `set_agent_output(agent_output)` 一行（L27）。
2. 若该文件由生成器批量产出，定位生成器（memory 提示为"322 个 check.py 可执行
   检测器"，工具脚本位于项目根），统一修复生成逻辑，再重新生成全部 644 个
   check.py（主集 + no-trigger 集）。
3. 批量回归：构造含 "§9.1" 的假输出文件，对每个技能执行
   `python check.py ws log output`，断言脚本项结果与预期一致。
4. 同时修复 `main()` 的可读性：文件缺失时打印显式告警而非静默 False。

### 12.2 P1 — 加固测评设计（对应 M-1/M-2/M-3）

1. 放宽 FMT-02 正则，兼容 "Section 9.1"、"§12" 变体；同步更新 SCORING.yaml 与
   check.py 两处（保持逐字符一致）。
2. 新增 critical failure：特权头缺失或特权输出分发违规 → cap_to_0。
3. 将 PROC-01（先排序后读，可用 `tool_log_order`）与 PROC-03（按序读取 + 先索引
   后输出，可用 `tool_log_order` / `timestamp_before`）转为脚本判定，降低 LLM
   judge 负担。
4. QA-01 的 question 明确列出三个标准后续项。

### 12.2 P2 — 技能正文微调（对应 L-1 至 L-6）

1. 将 `Privilege inheritance` 移到 `Matter context` 之后，或并入 Guardrails 分组。
2. 统一步骤编号体系（补 Step 3/4 或全部去编号）。
3. `Step 1` 增补异常输入处理（无主合同、日期倒挂、重复版本确认后的走向）。
4. QA-01 措辞锚定三连后续。
5. 可保留 "[coming soon]" 占位，但建议注明"作为产品路线图标记，不影响当前评测"。

---

## 13. 结论与后续行动

### 13.1 结论

**221-amendment-history 技能本体是语料库中高质量的法律流程类技能**：双模式（汇总/
条款追踪）设计精准命中真实律师工作流，模式判定、排序规则、引用纪律、边界声明
四层逻辑环环相扣，20 个测评点与正文指令 100% 可追溯，无缺节、无描述违规、无
人机感问题。技能本体评级 🟢，无需实质改动。

**测评工具链存在一处必现缺陷**：FMT-02（全技能唯一的脚本判定项）因 `set_agent_output`
双重设置而在文档化 runner 流程下恒为 False，且为 321/322 个技能共有的系统性 bug。
该缺陷不修复，主集与 no-trigger 对照集评测中的脚本判定全部失真，会直接污染后续
5 harness × 2 mode 的测评矩阵数据。修复优先级高于一切后续评测工作。

### 13.2 后续行动清单

| 序号 | 行动 | 责任人建议 | 优先级 |
|------|------|-----------|:------:|
| 1 | 修复 check.py 双重 set_agent_output（本技能 + 生成器批量） | 工具链维护 | P0 |
| 2 | 644 个 check.py 批量回归（主集 + no-trigger） | 工具链维护 | P0 |
| 3 | 放宽 FMT-02 正则 + 同步两处 | 测评设计 | P1 |
| 4 | 新增特权泄露 critical failure | 测评设计 | P1 |
| 5 | PROC-01/03 脚本化 | 测评设计 | P1 |
| 6 | 技能正文微调（特权节位置、步骤编号、异常输入） | 技能维护 | P2 |
| 7 | 技能档案回写 skill-dossier（本审查结论入档） | 档案维护 | P2 |

### 13.3 审查元信息

- 覆盖文件：SKILL.md（293 行）、SCORING.yaml（184 行）、check.py（74 行）、
  _shared/checker.py（351 行，依赖）。
- 实证验证项：YAML 合法性（两文件均解析通过）、criteria 计数与 ID 唯一性、
  FMT-02 正则可匹配性、main()/check() 执行流复现（FMT-02 恒 False）、
  系统性缺陷 grep 统计（321/322）。
- 评级汇总：逻辑 🟢 / 语法 🟢 / 人机感 🟢 / 合规 🟢 / 测评设计 🟢 / 检测器 🟠 /
  总体 🟢（含必修复工具链缺陷 1 项）。

---

*本报告由 SkillIF 质量审查流程生成，供 221-amendment-history 技能及其配套测评件*
*的后续迭代使用。报告中的代码缺陷均已实证复现，修复后建议回归验证。*
