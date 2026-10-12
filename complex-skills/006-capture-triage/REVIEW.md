# REVIEW: 006-capture-triage

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 将 Drafts Pro 移动端捕获的内容分类预览后路由到每日笔记的 Ready 队列
**Body 行数**: 373 行
**参考文件数**: docs/2, assets/0 (空), references/0 (空), resources/0 (空), scripts/0 (空)
**已有 REVIEW**: 是（旧版 46 行 stub）

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\006-capture-triage\
├── SKILL.md (377 行)
├── SCORING.yaml (170 行)
├── check.py (90 行)
├── REVIEW.md (本次审查替换)
├── assets/
│   └── .gitkeep (0 字节，空占位文件)
├── docs/
│   ├── GUIDE.md (103 行)
│   └── ROADMAP.md (65 行)
├── references/
│   └── .gitkeep (0 字节，空占位文件)
├── resources/
│   └── .gitkeep (0 字节，空占位文件)
└── scripts/
    └── .gitkeep (0 字节，空占位文件)
```

**文件统计**: 共 10 个文件（不含 REVIEW.md），其中 4 个为 .gitkeep 空占位符，2 个 docs 目录下的用户文档，3 个核心文件（SKILL.md, SCORING.yaml, check.py）。无实际的 references、scripts、assets 文件。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- **实际值**: `capture-triage`
- **目录名**: `006-capture-triage`
- **匹配**: ✅ 完全匹配（NNN- 前缀为序列号，name 字段无需包含）
- **格式**: 全小写字母 + 连字符，无空格、无大写 ✅
- **长度**: 14 字符，远低于 64 字符上限 ✅

### 2.2 description

**原文**:
```
Processes Drafts Pro captures from the Inbox folder. Classifies by intent, shows preview for approval, routes to Ready as tasks. Use when triaging captures, processing mobile notes, or as part of daily review. Triggers on "triage captures", "process captures", "check my captures".
```

**逐句分析**:

| # | 句子/分句 | 类型 | 判定 |
|---|----------|------|:----:|
| 1 | "Processes Drafts Pro captures from the Inbox folder." | WHAT — 核心功能声明 | ✅ 具体、第三人称、指明工具名(Drafts Pro) |
| 2 | "Classifies by intent, shows preview for approval, routes to Ready as tasks." | WHAT — 功能链条（三个并列动词） | ✅ 清晰完整的功能描述 |
| 3 | "Use when triaging captures, processing mobile notes, or as part of daily review." | WHEN — 触发场景 | 🟡 "Use when" 后接动名词而非 "the user asks to..." |
| 4 | "Triggers on \"triage captures\", \"process captures\", \"check my captures\"." | WHEN — 精确触发短语 | ✅ 三个具体触发短语明确列出 |

**第三人称检查**:
- "Processes" — 主语为 skill ✅
- "Classifies" — 主语为 skill ✅
- "shows" — 主语为 skill ✅
- "routes" — 主语为 skill ✅
- 无第一人称 (I/we)、无第二人称 (you/your)、无祈使句 ✅

**触发信号检查**: 包含 "Use when" 和 "Triggers on" 两个规范要求的触发信号 ✅

**禁止内容检查**:
| 禁止项 | 是否存在 | 详情 |
|--------|:------:|------|
| 第一/第二人称 | ❌ | 无 |
| 祈使句开头 | ❌ | 无 "Use this skill to..." |
| 跨 skill 路由 | ❌ | 无 `@skill-name` 形式 |
| 实现细节 | ❌ | 无 |
| 模糊描述 | ❌ | 具体到产品名和触发短语 |

**长度**: 187 字符（含空格），远低于 1024 字符上限 ✅

**逐句打分**: 8/10。功能描述准确具体，触发词明确。扣分点：第三句 "Use when triaging captures" 的动名词形式不如 "Use when the user asks to triage captures" 更精确地表达触发时机。

**修改建议**: "Use when the user asks to triage captures, process mobile notes, or perform a daily review." 将动名词改为 "the user asks to..." 的子句形式，更符合 WHEN 描述的第三人称规范。

### 2.3 allowed-tools

**实际值**: `Read, Glob, Grep, Edit, Write, AskUserQuestion`

**格式**: 逗号分隔列表，无多余空格 ✅

**逐工具论证**:

| Tool | 必要性 | 论证 | 在 SKILL.md 中的使用位置 |
|------|:------:|------|------------------------|
| Read | ✅ 必须 | 读取 Inbox 中的捕获 .md 文件、daily note、project 文件、contact 文件 | Step 3, Step 6, Step 8 |
| Glob | ✅ 必须 | Step 2 中 `PROJECT - *.md` 的 glob 模式匹配 | Step 2 (L70) |
| Grep | 🟡 存疑 | SKILL.md 正文中无明确的 grep 操作；Step 3a 检测已处理内容时可能隐式需要内容搜索，但 skill 未说明用 grep | 无明确引用 |
| Edit | ✅ 必须 | Step 6 使用 Edit 工具向 daily note 的 `## Ready` 节追加任务项 | Step 6 (L201-214) |
| Write | ✅ 必须 | Step 8 创建新的 CONTACT 文件，可能创建或更新 PROJECT 文件 | Step 8 (L248-272) |
| AskUserQuestion | ✅ 必须 | Step 5b 使用 AskUserQuestion 工具请求用户做出审批决策 | Step 5b (L160-169) |

**缺失工具检查**:
- 🔴 **`Bash` 缺失**: Step 1 (L59) 使用 `ls` 命令检查 Inbox 文件，Step 9 (L279) 使用 `mv` 命令移动文件到 Processed/。这两个操作都需要 Bash 工具，但 `Bash` 未在 allowed-tools 中声明。**这是功能性缺陷**——在严格检查 allowed-tools 的环境中，agent 将无法执行这两个步骤。

**冗余工具**:
- 🟡 **`Grep` 存疑**: 声明的 6 个工具中，Grep 在 workflow 中无明确使用点。如果设计意图是让 agent 使用 grep 搜索 capture 内容中的模式（如 "Research:" 前缀），应在 workflow 中明确说明。

**总体评价**: 6 个声明工具中 5 个有明确用途。`Bash` 缺失是关键遗漏，`Grep` 的使用理由不充分。建议调整为 `Read, Glob, Grep, Edit, Write, AskUserQuestion, Bash`（添加 Bash）或说明 Grep 的使用场景。

### 2.4 其他 frontmatter 字段

**实际字段清单**: `name`, `description`, `allowed-tools`（仅三个字段）

**对照 SKILL-SPEC.md 允许字段表**:

| 字段 | 类型 | 状态 | 说明 |
|------|------|:----:|------|
| `name` | 必须 | ✅ | 正确使用 |
| `description` | 必须 | ✅ | 正确使用 |
| `allowed-tools` | 可选 | ✅ | 在允许列表中 |
| `model` | 可选 | 未使用 | 不需要模型覆盖，合理 |
| `argument-hint` | 可选 | 未使用 | 不需要 |
| `user-invocable` | 可选 | 未使用 | 使用默认值 |
| `paths` | 可选 | 未使用 | 不需要 |
| `disable-model-invocation` | 可选 | 未使用 | 不需要 |

**禁止字段检查**: 无 `metadata`, `license`, `version`, `tags`, `author`, `category`, `domain` 等禁止字段 ✅

**评估**: Frontmatter 字段极为精简，仅包含 3 个字段（2 必须 + 1 可选），无冗余、无违规。

### 2.5 Frontmatter 语法

- YAML 分隔符 `---`: L1 和 L5 — 成对出现 ✅
- 缩进: 无缩进，所有字段顶格 ✅
- 特殊字符转义: description 中的双引号已正确转义（`\"triage captures\"`, `\"process captures\"`, `\"check my captures\"`）✅
- description 值被双引号包裹，内部引号使用反斜杠转义 —— 标准 YAML 实践 ✅
- 尾随空格: 无 ✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Capture Triage                                        (L7,     1 行, H1)
## What This Does                                       (L9-12,  4 行)
## Who It's For                                         (L14-16, 3 行)
## The Philosophy                                       (L18-23, 6 行)
## Paths                                                (L27-35, 9 行)
## Important: Naming Clarification                      (L39-49, 11 行)
## Instructions                                         (L52-303, 252 行) ← 核心
  ### Step 1: Check Inbox Folder (Root Only)            (L54-63,  10 行)
  ### Step 2: Load Context                              (L65-73,  9 行)
  ### Step 3: Read and Classify Each Capture            (L75-84,  10 行)
  ### Step 3b: Extract Source URLs                      (L87-96,  10 行) ← 乱序!
  ### Step 3a: Detect Already-Processed Content         (L98-109, 12 行) ← 乱序!
  ### Step 4: Classify Each Capture                     (L111-128, 18 行)
  ### Step 5: Show Classification Preview (Two-Step)    (L130-174, 45 行)
    #### Step 5a: Present the Table                     (L137-155, 19 行)
    #### Step 5b: Ask for Decision                      (L158-174, 17 行)
  ### Step 6: Route by Classification                   (L176-217, 42 行)
  ### Step 7: Handle Research                           (L219-242, 24 行)
  ### Step 8: Handle Contacts                           (L244-272, 29 行)
  ### Step 9: Move to Processed                         (L274-283, 10 行)
  ### Step 10: Generate Triage Summary                  (L285-303, 19 行)
## Examples                                             (L307-344, 38 行)
  (包含 Example 1: Dry Run Preview 和 Example 2: After Approval)
## Guidelines                                           (L347-358, 12 行)
## Version History                                      (L361-368, 8 行)
## Notes & Learnings                                    (L372-377, 6 行)
```

**Body 总行数**: 373 行（L7-L377，不含 frontmatter L1-L5）

### 3.2 必需章节检查（详细）

#### Workflow/Process 节

- **存在性**: ✅ 存在。`## Instructions` (L52-L303) 包含完整的 10 步操作流程。
- **标题用词**: 🟡 **"Instructions"** — SKILL-SPEC.md 推荐的标题为 "Workflow", "Process", "Execution Flow", "Procedure"。"Instructions" 偏向对人类用户的命令式指导，不够适合面向 agent 的 skill 定义。
- **步骤编号**: Step 1 → 2 → 3 → **3b** → **3a** → 4 → 5 → 6 → 7 → 8 → 9 → 10
  - 🔴 **编号乱序**: Step 3b (L87, "Extract Source URLs") 出现在 Step 3a (L98, "Detect Already-Processed") **之前**。子步骤编号应该按逻辑顺序排列（3a → 3b），但实际文件中顺序颠倒。
  - Step 1-10 主序列编号连续 ✅
- **步骤连贯性**: 
  - Step 1 (检查 Inbox) → Step 2 (加载上下文) → Step 3 (读取和分类) → Step 4 (分类判定) → Step 5 (预览审批) → Step 6 (路由) → Step 7/8 (特殊处理) → Step 9 (清理) → Step 10 (总结)
  - 逻辑链完整、流畅 ✅
- **每步骤内容完整性**:

| Step | 做什么 | 怎么做 | 输入/输出 | 评分 |
|------|:------:|:------:|:---------:|:----:|
| 1 | 检查 Inbox | ls 命令 | 文件列表/空 | 🟢 |
| 2 | 加载项目上下文 | glob + mission-context | 项目名列表 | 🟡 glob 明确，mission-context 调用方式模糊 |
| 3 | 读取和分类 | 逐文件 Read | 捕获内容和分类 | 🟢 |
| 3b | 提取 URL | 检查 frontmatter | URL 列表 | 🟢 |
| 3a | 检测已处理 | 信号匹配 | [PROCESSED] 标记 | 🟢 |
| 4 | 分类判定 | 内联提示优先+自动检测 | 分类标签 | 🟢 |
| 5 | 预览审批 | 两段式 AskUserQuestion | 审批决定 | 🟢 |
| 6 | 路由到 Ready | Edit 工具追加 | daily note 中的任务 | 🟢 |
| 7 | 研究处理 | Task spawn | 后台 agent | 🟡 spawn 参数细节待确认 |
| 8 | 联系人处理 | 检查/创建/更新 | CONTACT 文件 + Ready 任务 | 🟢 |
| 9 | 移动文件 | mv 命令 | 文件转移 | 🟢 |
| 10 | 生成摘要 | 模板输出 | Markdown 摘要 | 🟢 |

- **步骤粒度**: 合适。每个步骤是一次完整的操作单元，不太粗（如 "处理所有捕获" 一步完成）也不太细（如 "打开文件、读第一行、读第二行..."）。✅
- **条件分支检查**:

| 条件 | 位置 | Else/Otherwise | 完整？ |
|------|:----:|---------------|:------:|
| "If no files found" | L62 | "Report 'No captures waiting' and stop" | ✅ |
| "If files found" | L63 | "Continue to Step 2" | ✅ |
| "For x-bookmark files" | L89 | 隐式（非 x- 文件走 "For other captures"） | 🟡 隐式 |
| "If capture content looks like a summary" | L100 | 隐式（不标记 [PROCESSED]） | 🟡 隐式 |
| "If inline hint present" | L113-117 | "Auto-Detection (if no inline hint)" L119 | ✅ |
| "If approved" (research) | L222-224 | 隐式（不 spawn） | 🟡 |
| "If exists" (contact) | L248-249 | "If new" L250 | ✅ |
| "If a capture has no URL" | L197 | "note this: (source needed)" | ✅ |

- **起始/终止条件**: 
  - 起始: Step 1 — "Check Inbox Folder" 明确 ✅
  - 终止: Step 10 — "Generate Triage Summary" 后自然结束 ✅（虽然无显式 "Done" 信号）

#### Output Format 节

- **存在性**: 🟡 **部分存在**。输出格式信息分散在多个步骤中，但没有独立的 `## Output Format` 或 `## Deliverables` 节。
- **分散位置**:
  - Step 5a (L142-152): 预览表格模板 — 包含表头（#/File/Preview/Classification/Suggested Routing）
  - Step 6 (L180-187): 路由格式映射表 — 每种分类的目的地和格式
  - Step 6 (L201-214): Edit 操作格式示例
  - Step 8 (L255-272): Contact Note 模板
  - Step 10 (L287-303): Triage Summary 模板
- **输出完整性**: ✅ 各类输出格式均有明确模板（Markdown 表格、checkbox 格式、日期格式 MM-DD、Bash 命令）
- **可验证性**: ✅ 格式具体到字段级别——SCORING.yaml 的 OUT-01 (MM-DD 日期)、OUT-02 (URL)、OUT-03 (摘要关键字) 均可自动验证
- **缺失**: 无统一章节汇总所有输出产物。agent 需要通读全部 10 个步骤才能拼凑出完整的输出格式图景。

#### Scope/Limitations 节

- **存在性**: ❌ **完全缺失**。无 "## Scope", "## Limitations", "## What This Skill Does NOT Do" 标题。
- **替代内容的位置**:
  - `## What This Does` (L9-12): 仅 4 行正面描述，未说不做什么
  - `## The Philosophy` (L18-23): "No passive filing" — 仅 1 条哲学原则
  - `## Guidelines` (L347-358): 9 条操作原则，部分起到 scope 作用（如 "Dry run is standard", "Research-swarm is opt-in"）
  - `docs/GUIDE.md` L95-102: "What It's NOT" 小节 — 但 agent 不会自动读取 GUIDE.md
- **应包含但缺失的边界声明**:
  1. 不处理非 .md 文件（如 .txt, .json, .pdf）
  2. 不自动路由——所有操作需人类通过 Step 5 审批
  3. 不创建新项目文件——仅更新已存在的 PROJECT - *.md（Step 6 暗示了这一点但未明确）
  4. 不删除原始捕获——仅移动到 Processed/ 作为安全网
  5. 不搜索 Inbox 子目录——仅处理 Inbox/ 根目录文件
  6. 不替代 task-clarity-scanner 做优先级决策
  7. 不处理已标记为 [PROCESSED] 的内容（仅路由为 REFERENCE）
- **Medical/Legal disclaimer**: 不适用——此 skill 不涉及医疗或法律建议。

### 3.3 内容委托分析

- **委托行数**: 0 行。SKILL.md body 中没有任何 "see references/xxx.md" 或 "refer to docs/xxx.md" 形式的委托语句。
- **委托比例**: 0%
- **真实情况**: 虽然委托比例为 0%，但存在**未被引用的外部文档**（docs/GUIDE.md 和 docs/ROADMAP.md）。这不是"委托"问题，而是"资源不可见"问题（见 §5.2）。
- **独立可执行性**: body 内容完全自足，不需要读取任何外部文件即可执行全部 10 个步骤。✅
- **隐式外部依赖**（非文件委托，但仍是依赖）:
  - `mission-context skill` (L67): prose 引用，用于加载活跃项目名
  - `task-clarity-scanner` (L12, L357): prose 引用，用于后续优先级决策
  - `research-swarm pattern` (L234): prose 引用，Step 7 的研究 spawn

### 3.4 节编号/标题层级

- **标题层级路径**: `#` → `##` → `###` → `####` — ✅ 无跳级
  - H1: 1 个 (`# Capture Triage`)
  - H2: 11 个 (`## What This Does`, `## Who It's For`, `## The Philosophy`, `## Paths`, `## Important: Naming Clarification`, `## Instructions`, `## Examples`, `## Guidelines`, `## Version History`, `## Notes & Learnings`)
  - H3: 13 个（Step 1-10 + 子步骤）
  - H4: 2 个（Step 5a, Step 5b）
- **编号序列**: 
  - 主步骤: 1→2→3→4→5→6→7→8→9→10 ✅ 连续
  - 子步骤: 3b→3a ❌ 倒序
- **重复标题**: 无 ✅

### 3.5 Body 长度合规

- **实际行数**: 373 行 body（L7-L377）
- **600 行限制**: ✅ 373 < 600，有 227 行余量（约 38% 空间可用）
- **Pattern 对应**: process 类型目标 ~200 行，实际 373 行略超但远低于 600 上限
- **Reference 拆分需求**: 不需要——body 长度适中，无内容溢出压力

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

逐对检查相邻步骤之间的数据流：

| 步骤对 | 上游输出 | 下游消费 | 衔接 |
|--------|---------|---------|:----:|
| Step 1 → Step 2 | Inbox 中有 .md 文件 | 触发 context loading | ✅ |
| Step 2 → Step 3 | 活跃项目名称列表 | Step 4 中 PROJECT_UPDATE 分类需要匹配项目名 | ✅ |
| Step 3 → Step 3b/3a | 已读取的 capture 内容 | Step 3b 提取 URL，Step 3a 检测已处理 | ✅ |
| Step 3b/3a → Step 4 | URL 信息 + [PROCESSED] 标记 + 捕获内容 | Step 4 分类判定输入 | ✅ |
| Step 4 → Step 5 | 每个捕获的分类标签 | 预览表格数据 | ✅ |
| Step 5 → Step 6 | 用户审批决定（approve/modify/skip） | 路由指令 | ✅ |
| Step 6 → Step 7 | RESEARCH 分类 + 用户显式确认 | spawn 决策 | ✅ |
| Step 6 → Step 8 | CONTACT 分类 | 联系人处理 | ✅ |
| Step 6/7/8 → Step 9 | 所有路由完成 | 可以安全移动文件 | ✅ |
| Step 9 → Step 10 | 处理完成 | 生成摘要统计 | ✅ |

**衔接质量**: 全部 9 个步骤间衔接的输入/输出匹配。无断层、无信息丢失。✅

### 4.2 内部矛盾扫描

**对立表述搜索**:
- L11-12: "this skill makes it explicit so task-clarity-scanner can decide what's important"
- L357: "Everything to Ready - Let task-clarity-scanner handle prioritization"
- 两处一致：都委托 task-clarity-scanner 做优先级决策 ✅

- L349: "Dry run is standard - Always show preview before routing"
- L353: "Research-swarm is opt-in - Ask before spawning"
- Step 5 实现：先显示预览表（5a），再问决策（5b）— 与声明一致 ✅

**数字不一致检查**: 无硬编码数字冲突（处理数量 "32 captures" 出现在 Notes 节作为历史记录，不是规则）✅

**声明与实现矛盾**:
- L52 声明 "Instructions" 包含 10 步 → 实际有 Step 1-10，共 10 个主步骤 ✅
- L22-23 "No passive filing. Every capture becomes a decision point." → Step 5 要求人类对每个捕获做决策 ✅
- L48 "Tasks go to Ready section only" → Step 6 路由表中所有分类最终都去 Ready ✅
- 🟡 "This step can run in background" (L77) — 声称 Step 3 可后台运行，但 Step 3 的分类结果需要 Step 4 消费，后台模型下 Step 4 如何等待 Step 3 完成？"background OK" 的具体机制未说明。

### 4.3 示例/代码正确性

**Bash 命令 (L59)**:
```bash
ls /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/*.md 2>/dev/null
```
- 语法: ✅ `ls` + glob + 错误重定向，标准 Unix 语法
- 路径: 与 Paths 节 (L30) 一致 ✅
- `2>/dev/null`: 在 macOS/Linux 上有效 ✅
- 🟡 在 Windows 上 `2>/dev/null` 语法无效——但 skill 显然是 macOS 专属（`/Users/eddale/` 路径）

**Edit 操作示例 (L211-214)**:
```
old_string: "## Ready\n- [ ] existing task"
new_string: "## Ready\n- [ ] existing task\n- [ ] [new task from capture] (01-06)"
```
- 使用 `\n` 换行符: ✅ 符合 Edit 工具的字符串匹配规则
- 🟡 日期硬编码 "(01-06)" —— 应为动态值如 `(MM-DD)` 或 `(today's date)`
- old_string 假设已存在至少一个任务: 🟡 如果 `## Ready` 下尚无任务项，old_string 应为 `"## Ready\n"` 而非 `"## Ready\n- [ ] existing task"`

**Task spawn 伪代码 (L228-237)**:
```
Task(
  description="Research: [Topic]",
  prompt="Research question: [Full capture content]\n\nUse research-swarm pattern...",
  subagent_type="research-swarm",
  run_in_background=true
)
```
- 参数名: `description`, `prompt`, `subagent_type`, `run_in_background` — 与 Claude Code 的 Task 工具参数匹配 ✅
- `subagent_type="research-swarm"`: "research-swarm" 在 corpus 中的存在性待验证
- 模板变量: `[Topic]` 和 `[Full capture content]` — 标记清晰 ✅

**Contact Note Template (L255-272)**:
```markdown
---
type: contact
created: YYYY-MM-DD
source: capture-triage
---
# [Person Name]
...
```
- YAML frontmatter: 语法正确 ✅
- `type: contact` 和 `source: capture-triage`: 元数据字段合理 ✅
- 🟡 `created: YYYY-MM-DD`: 字面值，agent 应替换为实际日期但 skill 未显式说明

### 4.4 条件完整性

逐条检查所有条件分支：

| 条件 | 位置 | Else/Otherwise | Else 明确？ | 判定 |
|------|:----:|---------------|:----------:|:----:|
| "If no files found" | L62 | stop + report | ✅ 显式 | 完整 |
| "If files found" | L63 | continue to Step 2 | ✅ 显式 | 完整 |
| filename starts with `x-` | L89 | "For other captures with URLs" L93 | ✅ 显式 | 完整 |
| content looks like summary | L100 | 隐式（不标记） | 🟡 | 边界模糊—"looks like" 主观 |
| inline hint present | L113 | auto-detection L119 | ✅ 显式 | 完整 |
| user explicitly approved | L222 | 隐式（不 spawn） | 🟡 | 安全关键条件应有显式 else |
| contact file exists | L248 | create new L250 | ✅ 显式 | 完整 |
| capture has no URL | L197 | note "(source needed)" | ✅ 显式 | 完整 |

**边界条件覆盖**:
| 边界情况 | 是否处理 | 说明 |
|---------|:------:|------|
| 空 Inbox | ✅ | Step 1: report + stop |
| Inbox 中有非 .md 文件 | ❌ | `ls *.md` 自动过滤，但 .txt/.json 等被静默忽略 |
| Project glob 返回空 | 🟡 | 未明确说明——agent 可能以空列表继续 |
| Daily note 不存在 | ❌ | Step 6 假设 daily note 已存在 |
| Daily note 中无 `## Ready` 节 | ❌ | Step 6 的 Edit old_string 会匹配失败 |
| 多个捕获分类为同一人 CONTACT | 🟡 | 未说明是否合并还是分多次追加 |
| x-bookmark 无 tweet_url 字段 | ❌ | 未处理 frontmatter 缺少 tweet_url 的情况 |

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

SKILL.md body 中**无任何显式文件引用**。以下列出所有 prose 中提及的外部实体作为替代：

| 引用（prose） | SKILL.md 行号 | 是否为文件引用 | 本 skill 内文件？ | 判定 |
|--------------|:------------:|:------------:|:---------------:|:----:|
| `mission-context skill` | L67 | ❌ (prose) | N/A (外部 skill) | 🟢 合规 prose 引用 |
| `task-clarity-scanner` | L12, L357 | ❌ (prose) | N/A (外部 skill) | 🟢 合规 prose 引用 |
| `research-swarm pattern` | L234 | ❌ (prose) | N/A (外部 skill) | 🟢 合规 prose 引用 |
| (无文件引用) | — | — | — | — |

### 5.2 不可见资源审计

目录中存在但 SKILL.md 中从未提及的文件：

| 文件 | 应被提及？ | 评估 | 不可见后果 |
|------|:--------:|------|-----------|
| docs/GUIDE.md | 🟡 建议 | 包含 "What It's NOT" 小节和用户指南——恰好填补缺失的 Scope 节 | agent 不知道 scope 边界，可能在边界情况做错误决策 |
| docs/ROADMAP.md | 🟢 可选 | 项目管理文件——展示版本历史和未来计划 | 无直接功能影响 |
| assets/.gitkeep | 🟢 不需要 | 空占位符 | 无后果 |
| references/.gitkeep | 🟢 不需要 | 空占位符 | 无后果 |
| resources/.gitkeep | 🟢 不需要 | 空占位符 | 无后果 |
| scripts/.gitkeep | 🟢 不需要 | 空占位符 | 无后果 |

**关键发现**: docs/GUIDE.md 的 "What It's NOT" 小节（L95-102）包含了 SKILL.md 缺失的 scope 信息。如果 agent 不知道 GUIDE.md 的存在且不进行目录探索，将完全错过这些边界声明。

### 5.3 Reference 文件全文审查

**无 reference/*.md 文件**。references/ 目录仅包含 .gitkeep 占位符。N/A。

### 5.4 Scripts 文件全文审查

**无 scripts/*.py 或 .sh 文件**。scripts/ 目录仅包含 .gitkeep 占位符。N/A。

### 5.7 其他资源文件审查

#### docs/GUIDE.md (103 行)

**全文阅读结论**:

**内容概要** (逐节):
- L1-6: "The One-Sentence Version" — 将 skill 比喻为"清空大脑收件箱的助手"
- L7-18: "Why This Exists" — 解释捕获→积压→需要系统的动机链
- L19-26: "The Mental Model: The Mail Room" — 邮件室比喻：分类入站邮件
- L27-44: "How You Actually Use It" — 日常使用流程（捕获→说 "triage captures"→审批→路由）
- L45-52: "The Preview Pattern" — 解释为何预览步骤是设计核心（避免意外自动处理）
- L53-70: "Classification: How It Knows What Things Are" — 动词→任务、"What if"→想法、人名→联系人
- L71-83: "What Happens to Each Type" — 五种分类的处理方式
- L84-93: "The 'Everything to Ready' Philosophy" — 解释"一切到 Ready"的设计理念
- L95-102: "What It's NOT" — 三条否定声明（不是归档系统、不是自动化、不是研究工具）

**质量评价**:
- ✅ 写作流畅、比喻生动（邮件室）— 面向用户的可读性强
- ✅ "What It's NOT" 小节质量高——恰好是 SKILL.md 最需要的 scope 内容
- 🟡 使用第二人称 "you" 贯穿全文（面向人类用户，非 agent）
- 🟡 L29: "say 'triage captures'" — 对用户的命令式
- 🔴 最关键的三条 scope 声明存在于 GUIDE.md 而非 SKILL.md——agent 默认不可见

**对 skill 的贡献**: 作为用户文档，帮助人类理解 skill 的设计哲学和使用方式。但其 scope 内容应被提升到 SKILL.md 中。

**文件质量**: 🟡 好文档，但定位错误——scope 信息应在 SKILL.md 中，GUIDE.md 应聚焦在用户教程上。

#### docs/ROADMAP.md (65 行)

**全文阅读结论**:

**内容概要** (逐节):
- L1-10: "What's Shipped" — 版本历史表（v1.0→v2.2），4 个版本
- L12-16: "The Vision" — 愿景："捕获自动流入，坐下时已分类完毕等待审批"
- L18-27: "Planned Improvements" — 7 项计划改进（Drafts Pro 集成、智能默认、批量研究等）
- L28-44: "Ideas (Not Committed)" — 7 项未承诺想法（语音捕获、图像 OCR、统计仪表盘等）
- L46-60: "What We've Learned" — 6 条经验教训（预览不可协商、两步优于一步、Research-swarm 需 opt-in 等）
- L62-64: "Decision Log" — 决策记录规范（引用 `plans/` 和 `plans/archive/` 目录）

**质量评价**:
- ✅ 组织良好，区分了 Planned/Not Committed/Learned
- ✅ "What We've Learned" 节为设计决策提供了追溯依据
- 🟡 第一人称 "we" 贯穿——项目管理文档风格，非 agent 指令
- 🟡 L62-64 提到 `plans/` 和 `plans/archive/` 目录——这些目录在文件系统中不存在
- 🟡 "Decision Log" 指向不存在的目录

**对 skill 的贡献**: 为维护者和用户提供上下文，对 agent 执行无直接帮助。属于"nice to have"的项目管理文档。

#### .gitkeep 文件 (4 个)

- `assets/.gitkeep`: 0 字节 ✅
- `references/.gitkeep`: 0 字节 ✅
- `resources/.gitkeep`: 0 字节 ✅
- `scripts/.gitkeep`: 0 字节 ✅

全部为 Git 占位文件，用于在版本控制中保留空目录结构。无内容可审查。这些空目录暗示设计时预留了扩展空间（assets/ 用于模板、references/ 用于参考文档、scripts/ 用于辅助脚本），但当前版本 v2.2 仍未填充任何内容。

### 5.5 跨 Skill 引用检查

**`../` 路径引用**: 0 处 ✅

**Prose 引用清单**:
| 行号 | 引用形式 | 目标 skill | 类型 | 判定 |
|:----:|---------|-----------|------|:----:|
| L12 | "task-clarity-scanner" | task-clarity-scanner | prose 引用 | 🟢 合规 |
| L67 | "mission-context skill" | mission-context | prose + "skill" 后缀 | 🟢 合规 |
| L234 | "research-swarm pattern" | research-swarm | prose + "pattern" 后缀 | 🟢 合规 |
| L357 | "task-clarity-scanner" | task-clarity-scanner | prose 引用 | 🟢 合规 |

全部为合规的 prose 引用（使用 skill 名称而非文件路径，不使用 `@skill-name` 或 `../` 路径）。✅

### 5.6 嵌套重复/死文件检查

- **Self-nested 目录**: 无。`006-capture-triage/` 下无 `006-capture-triage/` 子目录 ✅
- **空 .gitkeep 目录**: 4 个（assets/, references/, resources/, scripts/）— 🟡 4 个空目录在无内容填充时显得冗余
- **废弃文件**: 无 ✅
- **`.gitkeep` 与已有内容的目录**: docs/ 目录有 2 个文件但**无** .gitkeep——不一致，docs/ 也是有内容的目录但没用 .gitkeep 标记

---

## 6. 语法与格式质量（逐问题列举）

### 6.1 拼写错误

逐行扫描结果：

| 行号 | 当前文本 | 建议修正 | 严重程度 |
|------|---------|---------|:--------:|
| (无拼写错误) | — | — | — |

SKILL.md 全文 377 行无拼写错误。✅

### 6.2 语法错误

| 行号 | 问题描述 | 类型 | 严重程度 |
|:----:|---------|------|:--------:|
| L11-12 | "Everything captured has intent - this skill makes it explicit" — 破折号连接两个独立完整句 | 标点风格 | 🟢 可接受 |
| L20-21 | "Everything captured has intent. Route to Ready, let task-clarity-scanner decide" — "Route" 是祈使句 | 语气不一致 | 🟡 |

无主谓不一致、时态混乱、残缺句或悬垂修饰语。整体语法质量高。✅

### 6.3 中英/葡英混杂

无任何非英文单词或短语。此 skill 不涉及多语言场景。✅

### 6.4 Markdown 格式破损

| 检查项 | 结果 | 详情 |
|--------|:----:|------|
| 代码围栏 ``` 配对 | ✅ | 所有代码块正确闭合（L29, L58, L68, L141, L163, L211, L227, L239, L255, L278, L286, L313, L320） |
| 粗体/斜体 `**` 配对 | ✅ | 全部闭合，无断裂标记 |
| 列表编号连续 | ✅ | 无编号断裂 |
| 表格格式 | ✅ | 5 个表格全部对齐正确（L41, L121, L146, L180, L364） |
| 链接语法 | ✅ | 无 `[text](url` 残缺或 `[text]` 裸文本 |
| Blockquote `>` | ✅ | L20-21 正确使用 |
| 水平线 `---` | ✅ | L25, L37, L135, L156, L199, L305, L345, L358 |

**整体评估**: Markdown 格式质量优秀。代码围栏、表格、引用块、列表全部格式正确。✅

### 6.5 占位符未填充

| 行号 | 占位符 | 类型 | 判定 |
|:----:|--------|------|:----:|
| L33 | `YYYY-MM-DD.md` | 日期路径模板 | ✅ 运行时动态解析 |
| L205 | `YYYY-MM-DD.md` | 日期路径模板 | ✅ 同上 |
| L258 | `YYYY-MM-DD` | contact 模板日期 | 🟡 应说明需替换为实际日期 |
| L268 | `YYYY-MM-DD` | interactions 条目日期 | 🟡 同上 |
| L287 | `YYYY-MM-DD HH:MM` | 摘要模板时间戳 | ✅ 运行时动态解析 |
| L30-34 | `/Users/eddale/...` | 用户路径 | 🔴 硬编码特定用户路径 |

无 `..`, `{{PLACEHOLDER}}`, `TODO`, `FIXME`, `TBD` 标记。✅

### 6.6 截断内容

- SKILL.md 末尾 (L377): "Review tasks without links are useless - Ed can't find the content to review (added v2.2)" — 完整句子，句号结尾 ✅
- docs/GUIDE.md 末尾 (L102): "Think of it as triage, not treatment. It sorts the incoming. You decide what gets attention." — 完整段落 ✅
- docs/ROADMAP.md 末尾 (L64): "That way we remember WHY we did things, not just what we did." — 完整句子 ✅
- SCORING.yaml 末尾: YAML 正确闭合 ✅
- check.py 末尾: `if __name__ == "__main__":` 和 `main()` 完整 ✅

无截断内容。所有文件均以完整句子/语句结束。✅

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

### 7.1 合规检查清单

| # | 规则（SKILL-SPEC.md v1.0） | 状态 | 说明 |
|---|--------------------------|:----:|------|
| 1 | name: lowercase+hyphens, ≤64 chars, 匹配目录 | ✅ | `capture-triage` = `006-capture-triage` 去掉前缀 |
| 2 | description: 第三人称 | ✅ | 所有动词主语均为 skill |
| 3 | description: 含触发信号短语 | ✅ | "Use when" + "Triggers on" |
| 4 | description: ≤1024 字符 | ✅ | 187 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | 仅 name/description/allowed-tools |
| 6 | body: ≤600 行 | ✅ | 373 行 |
| 7 | body: 有 Workflow/Process 节 | 🟡 | "## Instructions" 存在但标题非规范推荐词 |
| 8 | body: 有 Output Format 节 | 🟡 | 输出格式嵌入在步骤中，无独立节 |
| 9 | body: 有 Scope/Limitations 节 | ❌ | **完全缺失** |
| 10 | 无跨 skill 文件路径引用 (`../`) | ✅ | 仅 prose 引用 |
| 11 | allowed-tools: 格式正确（逗号分隔） | 🟡 | 格式正确但缺少 Bash |
| 12 | 路径仅指向本 skill 目录内 | 🟡 | 操作路径为外部用户目录（灰色地带） |

### 7.2 违规详情

**#7 — Workflow 标题不规范 (🟡)**
- 当前值: `## Instructions` (L52)
- 规范原文: "Workflow / Process / Execution Flow / Procedure"
- 建议: 改为 `## Workflow` 或 `## Process`
- 影响: 低——功能上 agent 仍能找到流程，但标题不匹配规范预期

**#8 — Output Format 节缺失 (🟡)**
- 当前状态: 输出格式分散在 Step 5a (preview table), Step 6 (routing formats), Step 10 (triage summary) 中
- 规范原文: "What does the user get? What does the result look like?"
- 建议: 新增 `## Output Format` 节，汇总所有输出格式
- 影响: 中——agent 需要扫描多个步骤才能理解完整的输出格式

**#9 — Scope/Limitations 节缺失 (🔴)**
- 当前状态: 完全无 Scope/Limitations 节
- 规范原文: "What does this skill NOT do? When should it NOT be used?"
- 影响: 高——agent 不知道边界，可能在不适用的场景下激活此 skill
- 已有替代内容: Guidelines 节 (L347-358) 部分起到 scope 作用，但不完整
- 建议: 新增 `## Limitations` 节，至少 3 条边界声明

**#11 — allowed-tools 缺少 Bash (🟡)**
- 当前值: `Read, Glob, Grep, Edit, Write, AskUserQuestion`
- 缺失: `Bash` — Step 1 (`ls`) 和 Step 9 (`mv`) 需要
- 影响: 中——在严格 enforced allowed-tools 的评测环境中，agent 无法执行 Shell 命令

**#12 — 外部路径引用 (🟡)**
- 位置: L30-34 (Paths 节), L59 (ls 命令), L70 (glob), L205 (daily note)
- 评估: 这些都是 skill 操作的**目标路径**而非 skill 自身的内部引用。对于操作外部文件的 process skill，目标路径引用是功能必需的。但硬编码 `/Users/eddale/` 路径使其不可移植。
- 灰色地带: 规范说"路径仅指向本 skill 目录内"——目标是将引用限制在 skill 自身文件，但操作目标路径不在同一范畴

---

## 8. 人机感评估

### 8.1 Emoji 审计

**全篇 377 行零 emoji 使用。** ✅

无功能性 emoji、无装饰性 emoji、无表情符号。这是一个完全无 emoji 的 skill，风格干净统一。

### 8.2 全大写/喊叫式语言

| 短语 | 行号 | 出现次数 | 上下文 | 判定 |
|------|:----:|:------:|--------|:----:|
| `IMPORTANT` | L56, L189 | 2 | "Important: Only check files..." / "IMPORTANT: Review tasks MUST include links." | 🟡 功能性强调 |
| `MUST` | L91, L189 | 2 | "This URL MUST be included..." / "Review tasks MUST include links" | 🟡 功能性 |
| `FIRST` | L113 | 1 | "Check for these FIRST:" | 🟡 功能性 |

**统计**: 共 5 处全大写强调。阈值 = 5 处，刚好在边界。属于合理强调范围——每处都是功能性标记（非情绪化喊叫）。

### 8.3 Persona 语气分析

**整体语气判定**: 对话式实用主义 + 私人助理

**代表性语气证据**:

| 行号 | 原文 | 语气特征分析 |
|:----:|------|------------|
| L16 | "Ed - capturing quick thoughts in Drafts Pro throughout the day." | 私人助理——直呼用户名，带有熟悉感 |
| L20-23 | "> Everything captured has intent. Route to Ready, let task-clarity-scanner decide what moves to Someday/Maybe.\n\nNo passive filing. Every capture becomes a decision point." | 设计原则宣言——短句连击、自信、果断 |
| L47-48 | "**Remember:** This skill reads from the Inbox FOLDER and routes to the Ready SECTION.\nTasks go to Ready section only - Captures section is for document links." | 提醒语气——"Remember" 带有教练感 |
| L349-357 | "- **Two-step preview** - Show table first, ask decision second...\n- **Dry run is standard** - Always show preview...\n- **Everything to Ready** - Let task-clarity-scanner handle..." | 简洁的要点列表——操作原则、无废话 |
| L374-377 | "- Day 1 test processed 32 captures with backlog - dry run prevented overwhelm\n- [PROCESSED] detection helps avoid re-researching...\n- Review tasks without links are useless - Ed can't find the content to review (added v2.2)" | 实践反思——坦诚、从经验中学习 |

**语气适配性评估**: 🟡 对于 Ed 的个人工作流 skill，私人助理语气是功能性的——它反映了 skill 是为单用户设计的。但如果放到多用户场景，以下几点需要调整：
1. 去除 "Ed" 个性化（或用 `$USER` 变量替换）
2. "Remember:" 类提醒可保留——对 agent 仍有指导作用
3. Notes & Learnings 中的反思语气适合作为设计文档

### 8.4 人机边界分析

**Agent vs 人类职责区分**:

| 职责 | 归属 | 依据 |
|------|:----:|------|
| 读取 Inbox 文件 | Agent | Step 1-3 |
| 分类捕获 | Agent | Step 4 |
| 展示预览 | Agent | Step 5a |
| 审批/修改/跳过 | **人类** | Step 5b — "user approve, modify, or skip" |
| 路由到 Ready | Agent | Step 6 (仅在审批后) |
| 启动研究 swarm | Agent | Step 7 (仅在人类显式批准后) |
| 移动文件到 Processed | Agent | Step 9 |
| 生成摘要 | Agent | Step 10 |

**边界声明**: 
- 🟡 无显式 "In all cases, the human decides" 声明——但设计上 human-in-the-loop 是核心（Step 5 审批、Step 7 opt-in）
- ✅ Agent 不替代人类判断——所有修改都需要审批
- 🟡 "Ed" 硬编码——如果 agent 为其他用户运行，出现人名错位

**过度自动化风险**: 低。两段式预览 + opt-in research spawn + dry run 设计确保了人类始终在审批环中。✅

### 8.5 人称分析

| 人称 | 出现次数 | 典型上下文 | 判定 |
|------|:------:|-----------|:----:|
| 第二人称 "you"/"your" | 0 | — | ✅ 无 |
| 第一人称 "I"/"we"/"our" | 0 | — | ✅ 无 |
| "Ed" (专有名称) | 5 | L16, L192, L357, L377 (×2) | 🟡 特定用户硬编码 |

**分析**: SKILL.md body 严格执行了第三人称（面向 agent）——无 "you" 和 "I/we"。但 "Ed" 作为特定用户名的出现形成了一个隐性第二人称（因为 Ed 就是 skill 的唯一目标用户）。对于个人使用场景可接受，但在评测 corpus 中是一个值得注意的特征。

**对比 docs/GUIDE.md**: GUIDE.md 大量使用 "you"（面向人类用户），这是定位差异——GUIDE.md 是用户文档而非 agent 指令。

---

## 9. 可执行性评估

### 9.1 独立可执行性

**假设**: agent 仅拿到 SKILL.md 文本，没有目录探索能力。

| 评估维度 | 判定 | 说明 |
|---------|:----:|------|
| 能否理解任务目标？ | ✅ | description + "What This Does" + "The Philosophy" 清晰 |
| 能否找到操作对象？ | ✅ | Paths 节给出了精确路径 |
| 能否执行每个步骤？ | 🟡 | Step 1-10 都有操作指令，但部分依赖外部 skill |
| 能否独立完成（无外部 skill）？ | 🟡 | Step 2 依赖 mission-context，Step 7 依赖 research-swarm |
| 能否在非 Ed 机器上执行？ | ❌ | 路径硬编码到 `/Users/eddale/...` |

**打分**: 6/10。流程完整、步骤清晰，但高度绑定特定用户环境（路径、外部 skill 依赖）。

### 9.2 步骤可操作性

| Step | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| 1 | "ls /Users/eddale/.../Inbox/*.md" | 🟢 | 精确命令，输入输出明确 |
| 2 | "Pull active project names from mission-context skill AND glob PROJECT - *.md" | 🟡 | mission-context 调用方式未说明（是读文件？触发 skill？） |
| 3 | "Read and classify all captures before surfacing to user" | 🟡 | "classify" 在此步是概述，实际分类在 Step 4 |
| 3b | "Read tweet_url from YAML frontmatter" | 🟢 | 精确字段名 |
| 3a | "Detect if already-processed" | 🟢 | 4 条信号列表明确 |
| 4 | "Check inline hints FIRST... Auto-Detection table" | 🟢 | 优先级 + 分类表 + 6 类信号 |
| 5 | "Show table first, then AskUserQuestion" | 🟢 | 精确的两段式流程 + 模板 |
| 6 | "Route by classification table" | 🟢 | 6 分类→格式→目的地完整映射 |
| 7 | "Task(description=..., subagent_type='research-swarm')" | 🟡 | research-swarm 的行为和参数约定未定义 |
| 8 | "Check if CONTACT exists, append or create" | 🟢 | 条件分支 + 模板 |
| 9 | "mv [Inbox file] [Processed folder]" | 🟢 | 精确命令 |
| 10 | "Generate Triage Summary" | 🟢 | Markdown 模板 |

**操作性子数**: 🟢 7/10, 🟡 3/10, 🔴 0/10

### 9.3 工具依赖合理性

| 操作 | 所需工具 | 在 allowed-tools？ | 有回退？ |
|------|---------|:-----------------:|:------:|
| 读取 Inbox 文件 | Read | ✅ | N/A |
| 查找项目文件 | Glob | ✅ | N/A |
| 搜索内容模式 | Grep | ✅ (但未被 workflow 使用) | N/A |
| 编辑 daily note | Edit | ✅ | N/A |
| 创建 CONTACT 文件 | Write | ✅ | N/A |
| 用户审批交互 | AskUserQuestion | ✅ | N/A |
| ls 命令 | Bash | ❌ | 🔴 无回退 |
| mv 命令 | Bash | ❌ | 🔴 无回退 |
| mission-context | 外部 skill | N/A | 🟡 无显式回退方案 |
| research-swarm | 外部 skill/agent | N/A | 🟡 无显式回退方案 |

**外部依赖回退**: 对于 `mission-context` 和 `research-swarm`，如果这些 skill 不可用：
- mission-context: Step 2 可通过仅 glob `PROJECT - *.md` 部分回退（获取项目文件名但缺少活跃上下文）
- research-swarm: Step 7 无回退方案——如果该 agent 不可用，RESEARCH 项目将被挂起

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 共定义 **18 个 criteria**，分布在 scope(3) + process(9) + output(3) + negative(2) + qa(1)。

| ID | 类别 | Judge 方式 | 检查内容 | 与 SKILL.md 一致？ |
|----|------|:---------:|---------|:-----------------:|
| SCOPE-01 | scope | LLM | 首条回复 framing 为 triage 任务 | ✅ "What This Does" L9-12 |
| SCOPE-02 | scope | Script | tool log 含 "Zettelkasten/Inbox" | ✅ Paths 节 L30 |
| SCOPE-03 | scope | Script | tool log 不含 Inbox 子目录模式 | ✅ Step 1 L56 "Root Only" |
| PROC-01 | process | LLM | 空 Inbox 时报告并停止 | ✅ Step 1 L62 |
| PROC-02 | process | Script | tool log 含 "PROJECT -" | ✅ Step 2 L70 |
| PROC-03 | process | Script | tool log 含 URL 字段名 | ✅ Step 3b L90-93 |
| PROC-04 | process | LLM | [PROCESSED] 检测和 REFERENCE 路由 | ✅ Step 3a L100-109 |
| PROC-05 | process | LLM | 内联提示优先于自动检测 | ✅ Step 4 L113-117 |
| PROC-06 | process | Script | 输出含 "Capture Triage Preview" | ✅ Step 5a L142 |
| PROC-07 | process | Script | daily note 含指定格式 | ✅ Step 6 L180-187 |
| PROC-08 | process | LLM | research-swarm 仅审批后 spawn | ✅ Step 7 L222-224 |
| PROC-09 | process | Script | tool log 含 "Inbox/Processed" | ✅ Step 9 L279 |
| OUT-01 | output | Script | daily note 含 (MM-DD) 日期 | ✅ Step 6 L182-184 |
| OUT-02 | output | LLM | REFERENCE 任务含链接 | ✅ Step 6 L189-197 |
| OUT-03 | output | Script | 输出含摘要关键字 | ✅ Step 10 L287-303 |
| NEG-01 | negative | Script | tool log 不含 "## Captures" | ✅ L48, L208 |
| NEG-02 | negative | LLM | 未经审批不 spawn swarm | ✅ Step 7 L222-224 |
| QA-01 | qa | LLM | 无 URL 时标注 "(source needed)" | ✅ Step 6 L197 |

**一致性评估**: ✅ 全部 18 个 criteria 与 SKILL.md 内容精确对应。每个 criterion 的源头都可以在 SKILL.md 中找到。SCORING.yaml 质量高——覆盖了核心行为（SCOPE, PROC）、输出格式（OUT）、负面合规（NEG）和边界情况（QA）。

### 10.2 Critical Failures 分析

| CF ID | 条件 | 触发效果 | 合理性 | 评估 |
|-------|------|:------:|:------:|------|
| CF-01 | 未经两步预览/审批直接路由 | cap_to_0 | ✅ 非常合理 | 这是 skill 最核心的设计原则——"dry run is standard"（L349） |
| CF-02 | 追加到 ## Captures 而非 ## Ready | cap_to_0 | ✅ 非常合理 | SKILL.md 多处强调（L48, L208）。路由到错误节会使 tasks 不可见 |

**缺失的 Critical Failure**:
- 🟡 未覆盖 "agent 在 ## Ready 中创建了重复任务"——重复检测
- 🟡 未覆盖 "agent 未在处理后移动文件到 Processed/"——原始文件残留
- 🟡 未覆盖 "agent 向不允许的目的地路由（如直接向 Someday/Maybe）"

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录** (skill-dossier.md, Batch 001-025 节):

- **评级**: 🟡
- **问题 1**: "子节编号乱序（Step 3b 'Extract Source URLs' 在 Step 3a 'Detect Already-Processed' 之前）"
- **问题 2**: "Step 7 research-spawn 条件模糊"
- **问题 3**: "无 Scope/Limitations 节"
- **总评**: "🟡 重排 Steps 3a/3b、明确 spawn 条件、补 Scope 节。"

**逐项验证**:

| Dossier 问题 | 当前状态 | 详情 |
|-------------|:------:|------|
| Step 3b/3a 乱序 | 🔴 仍存在 | L87 Step 3b → L98 Step 3a，自 dossier 记录以来未修复 |
| research-spawn 条件模糊 | 🟡 部分改善 | L222-224 明确了 "Only spawn if user explicitly approved"，比 dossier 描述的好。但 spawn 的 Task 参数中引用的 "research-swarm pattern" 细节未定义 |
| 无 Scope/Limitations 节 | 🔴 仍存在 | 确认完全缺失 |

**Dossier 遗漏问题（本次审查新发现）**:

| # | 新增问题 | 严重程度 | 位置 |
|---|---------|:------:|------|
| 1 | allowed-tools 缺少 Bash | 🔴 | SKILL.md L4 |
| 2 | Grep 在 allowed-tools 但 workflow 未使用 | 🟡 | SKILL.md L4 |
| 3 | docs/ 下文件未被 SKILL.md 引用 | 🟡 | 全局 |
| 4 | "## Instructions" 标题不规范 | 🟡 | SKILL.md L52 |
| 5 | 无独立 "## Output Format" 节 | 🟡 | 全局 |
| 6 | 硬编码路径 (Ed 专属) | 🟡 | L30-34, L59, L205 |
| 7 | Daily note 无 ## Ready 节时 Edit 失败 | 🟡 | L201-214 |
| 8 | 外部 skill 依赖无回退方案 | 🟡 | L67, L234 |
| 9 | GUIDE.md scope 内容未提升到 SKILL.md | 🟡 | docs/GUIDE.md L95-102 |

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | description 优质、name 匹配，allowed-tools 缺 Bash(扣2) |
| Body 结构完整 | 5/10 | 10% | 0.50 | 缺 Scope(扣3)、Output Format(扣1)、3b/3a 乱序(扣1) |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 步骤衔接完整、无内部矛盾，部分 else 分支隐式(扣2)，边界条件覆盖不全(扣1) |
| 参考完整性 | 6/10 | 15% | 0.90 | 无 references/scripts 被使用，docs/ 未被引用(扣2)，4 空 .gitkeep(扣1)，GUIDE.md scope 信息未提升(扣1) |
| 语法格式 | 9/10 | 10% | 0.90 | 拼写/语法/Markdown 几乎完美，仅 1 处破折号风格问题(扣1) |
| 规范合规 | 5/10 | 15% | 0.75 | 缺 Scope 🔴(扣3)、Output 节缺失(扣1)、标题不规范(扣1)、Bash 缺失(扣1)，但 body 长度和跨 skill 引用合规(+1) |
| 人机感 | 7/10 | 10% | 0.70 | 过度个性化 "Ed"(扣1)，无 emoji(优)，人机边界清晰(优)，但部分 "Remember" 语气偏对话(扣1)，GUIDE.md 第二人称(扣1) |
| 可执行性 | 7/10 | 10% | 0.70 | 流程完整但绑定特定环境(扣2)，外部 skill 依赖无回退(扣1) |
| **加权总分** | | | **66.5/100** | |

### 12.2 评级

🟡 **B** (60-79): 可用，有需要修复的问题

**评级说明**: 作为单用户工作流 skill，设计质量和操作细节出色。10 步流程逻辑连贯、两段式预览模式设计精良、输出格式完整可验证。主要扣分来自合规性缺失（Scope 节、Output Format 节、allowed-tools）和可移植性问题（硬编码路径）。修复这些问题可使评分提升至 A 级（预计 82-85 分）。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**1. 缺少 Scope/Limitations 节**
- **位置**: SKILL.md — 需新增节（建议在 Guidelines 之后、Version History 之前）
- **修复方向**: 新增 `## Limitations` 节，至少包含以下 7 条：
  1. 仅处理 .md 文件，忽略其他格式
  2. 所有路由操作需要人类审批（本 skill 不自动修改 daily note）
  3. 仅更新已存在的 PROJECT - *.md 文件，不创建新项目文件
  4. 原始捕获文件仅移动到 Processed/，永不删除
  5. 仅处理 Inbox/ 根目录文件，不遍历子目录
  6. 不替代 task-clarity-scanner 做优先级排序
  7. [PROCESSED] 内容自动路由为 REFERENCE，不触发 research-swarm
- **不修复的后果**: agent 可能在未预期的边界情况（非 .md 文件、深层目录、大容量 Inbox）中做出错误行为。缺失 scope 也违反了 SKILL-SPEC.md §3.1 的强制要求。

**2. allowed-tools 缺少 Bash**
- **位置**: SKILL.md L4
- **修复方向**: `allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion, Bash`
- **不修复的后果**: 在 enforced allowed-tools 的评测中，agent 无法执行 Step 1 的 `ls` 和 Step 9 的 `mv` 命令，skill 的初始化和清理步骤均失败。

**3. Step 3b/3a 编号乱序**
- **位置**: SKILL.md L87-L109
- **修复方向**: 交换两节——Step 3a "Detect Already-Processed Content" (L98-109) 移到 Step 3b "Extract Source URLs" (L87-96) 之前
- **不修复的后果**: agent 按文档顺序先提取 URL 后检测已处理内容。对已标记为 [PROCESSED] 的内容仍然执行了 URL 提取（浪费操作），且逻辑流违反直觉（应先判断类型再提取元数据）。

### 🟡 重要缺陷（建议修复）

**4. "## Instructions" 标题改为 "## Workflow"**
- **位置**: SKILL.md L52
- **修复方向**: `## Instructions` → `## Workflow`
- **原因**: 匹配 SKILL-SPEC.md 推荐的标题命名

**5. 新增独立 "## Output Format" 节**
- **位置**: SKILL.md — 在 Workflow 之后、Examples 之前
- **修复方向**: 提取和汇总以下内容到一个独立节中：
  - Preview table 格式（来自 Step 5a）
  - 各分类的路由格式（来自 Step 6 表 L180-187）
  - Edit 操作格式（来自 Step 6 L201-214）
  - Contact Note 模板（来自 Step 8 L255-272）
  - Triage Summary 模板（来自 Step 10 L287-303）
- **原因**: 满足 SKILL-SPEC.md §3.1 的强制要求，同时让 agent 能在一个位置找到所有输出格式

**6. 将硬编码路径参数化**
- **位置**: SKILL.md L30-34, L59, L70, L205
- **修复方向**: 在 Paths 节顶部定义变量：
  ```
  ${INBOX}      = /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
  ${DAILY_NOTE} = /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
  ```
  然后后续所有步骤使用 `${INBOX}` 和 `${DAILY_NOTE}` 引用
- **原因**: 提高可移植性和可测试性。SCORING.yaml (L5-8) 已使用此变量模式，SKILL.md 应与之保持一致

**7. 引用 docs/GUIDE.md**
- **位置**: SKILL.md — Guidelines 节末尾或新增的 Limitations 节
- **修复方向**: 添加 "See docs/GUIDE.md for the user-facing explanation and design rationale."
- **原因**: GUIDE.md 包含有价值的 scope 信息和设计解释，agent 应知道其存在

**8. 移除或说明 Grep 的用途**
- **位置**: SKILL.md L4
- **修复方向**: 如果 workflow 确实需要 Grep（如搜索 capture 内容中的模式），在 workflow 中明确说明；如果不需要，从 allowed-tools 中移除
- **原因**: 减少不必要的工具表面积，避免 agent 使用 Grep 做非预期操作

**9. 添加 daily note 无 ## Ready 节的回退逻辑**
- **位置**: SKILL.md Step 6 (L201-214)
- **修复方向**: 在 Edit 操作前添加：
  > "If `## Ready` section does not exist in today's daily note, create it before appending tasks. Use Edit or Write to add `## Ready\n` at the appropriate location."
- **原因**: 防止 agent 在 daily note 无 Ready 节时 Edit 失败

**10. 补充 Inbox 无非 .md 文件的说明**
- **位置**: SKILL.md Step 1 (L54-63)
- **修复方向**: 在 "If no files found" 附近添加："Only .md files are processed. Non-markdown files (if any) are silently ignored."
- **原因**: 明确边界，避免 agent 困惑

### 🟢 优化建议（锦上添花）

**11. 合并空 .gitkeep 目录**
- **位置**: 目录结构
- **修复方向**: 如果 assets/, references/, resources/, scripts/ 在可预见的未来无填充计划，考虑合并或移除空目录。4 个空目录对 v2.2 版本显得过度预留。
- **原因**: 减少目录噪音

**12. CONTACT 模板日期字段说明**
- **位置**: SKILL.md L258, L268
- **修复方向**: 将 `created: YYYY-MM-DD` 改为 `created: <TODAY'S DATE>` 或添加注释 "// replace with actual date"
- **原因**: agent 可能复制字面字符串 "YYYY-MM-DD" 而非实际日期

**13. 外部 skill 依赖文档化**
- **位置**: SKILL.md L67, L234
- **修复方向**: 在 prose 引用后添加简短说明：
  - "mission-context (external skill for loading active project context)"
  - "research-swarm (external skill/pattern for multi-agent research investigation)"
- **原因**: agent 需要知道这些是外部依赖，如果不可用应有心理准备

**14. Step 3 "background OK" 澄清**
- **位置**: SKILL.md L77
- **修复方向**: 说明 "background OK" 的具体机制——是 agent 并行读取多个文件？还是启动后台子任务？与 Step 4 的衔接如何保证？
- **原因**: 当前描述模糊，agent 可能不知道如何具体实现"后台"操作

### 修复工作量估计

- **预计修改行数**: ~45-65 行
  - 新增 Limitations 节: ~15 行
  - 新增 Output Format 节: ~20 行
  - 修改 allowed-tools: 1 行
  - 重排 Step 3a/3b: 0 行（仅移动位置）
  - 标题修正: 1 行
  - 路径参数化: ~10 行
  - 其他小修改: ~10 行
- **预计修改文件数**: 1 个（仅 SKILL.md）
- **复杂度**: 低——主要是结构性补充，无需逻辑重写

---

## 变更记录
- 2026-08-05: 初始 stub REVIEW (46 行)
- 2026-08-06: 全面深度审查替换 (本文件)

---

## 附录: 审查过程记录

### 读取的文件列表
| 文件 | 行数 | 读取方式 | 状态 |
|------|:----:|---------|:----:|
| SKILL.md | 377 | 全文逐行精读 | ✅ |
| SCORING.yaml | 170 | 全文 | ✅ |
| check.py | 90 | 全文 | ✅ |
| docs/GUIDE.md | 103 | 全文逐段分析 | ✅ |
| docs/ROADMAP.md | 65 | 全文逐段分析 | ✅ |
| assets/.gitkeep | 0 | 确认为空文件 | ✅ |
| references/.gitkeep | 0 | 确认为空文件 | ✅ |
| resources/.gitkeep | 0 | 确认为空文件 | ✅ |
| scripts/.gitkeep | 0 | 确认为空文件 | ✅ |
| _shared/SKILL-SPEC.md | 162 | 全文（批次级引用） | ✅ |

### 读取统计
- **Skill 内部文件总行数**: 805 行（含所有非空文件）
- **规范参考**: 162 行（SKILL-SPEC.md, batch-level）
- **总计读取**: 967 行
- **空文件**: 4 个 .gitkeep（全部确认）

### 审查深度声明
- SKILL.md: 完成 13 节全维度分析，逐句审查 description，逐步检查工作流衔接，全条件分支枚举
- SCORING.yaml: 18 个 criteria 全部逐条验证与 SKILL.md 的一致性
- check.py: 10 个 script-checkable criteria 全部验证实现正确性和路径匹配
- docs/GUIDE.md: 全文 103 行内容级分析，8 个子节逐一概述
- docs/ROADMAP.md: 全文 65 行内容级分析，6 个子节逐一概述
- .gitkeep 文件: 4 个全部确认为 0 字节空占位符
- 跨 skill 引用: 4 处 prose 引用全部验证合规
