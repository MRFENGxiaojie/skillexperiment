# REVIEW: 216-command-creator

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — Claude Code 斜杠命令创建器（Slash Command Creator）
**Body 行数**: 210 行（SKILL.md，process 模式目标 ~200 行 ✅）
**参考文件数**: 3（references/patterns.md 363 行、references/examples.md 583 行、references/best-practices.md 719 行）
**全目录总量**: 7 个文件，约 2,645 行
**已有 REVIEW**: 无（本文件为首次审查）
**总评**: 🟡 C+ (67.5/100) — 流程设计完整、参考文件质量高，但存在 3 处自相矛盾的 Bash/make 指令（可执行性风险）与多处内部不一致

---

## 1. 目录全量清单

```
216-command-creator/
├── SKILL.md (210 行) — 主技能文件，6 步创建工作流
├── README.md (523 行) — 市场营销式文档（与 SKILL.md 大量重复）
├── SCORING.yaml (168 行) — 18 项评估标准（6 类）
├── check.py (79 行) — 脚本检查器（7 项脚本检查）
├── REVIEW.md (本文件)
└── references/
    ├── patterns.md (363 行) — 4 主模式 + 5 进阶模式
    ├── examples.md (583 行) — 4 个完整命令示例 + 对比表
    └── best-practices.md (719 行) — 模板、清单、反模式
```

全目录 7 个文件，总代码量约 2,645 行。这是一个中等规模的 process 型技能，核心价值载体在 3 个参考文件（合计 1,665 行，占总量 63%）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- **实际值**: `command-creator`
- **目录名**: `216-command-creator` → slug 匹配 ✅
- **格式**: 全小写 + 连字符，15 字符 ≤ 64 ✅
- **判定**: ✅ 完全合规

### 2.2 description（逐句分析）

原文（297 字符，≤1024 ✅）：
```
This skill should be used when creating a Claude Code slash command. Use when users ask to "create a command", "make a slash command", "add a command", or want to document a workflow as a reusable command. Essential for creating optimized, agent-executable slash commands following best practices.
```

逐句拆解：

| # | 句子/分句 | 类型 | 判定 | 问题 |
|---|----------|------|:----:|------|
| 1 | "This skill should be used when creating a Claude Code slash command." | WHEN | ✅ | 被动语态陈述何时使用，语义清晰 |
| 2 | "Use when users ask to 'create a command', 'make a slash command', 'add a command', or want to document a workflow as a reusable command." | WHEN（触发短语） | ⚠️ | 含触发信号 "Use when..."（§2.4 合规），但 "users" 是复数，规范模板为 "Use when the user..." |
| 3 | "Essential for creating optimized, agent-executable slash commands following best practices." | 促销语 | ⚠️ | "Essential for" 是营销式措辞，不增加 WHAT/WHEN 信息，可删除 |

**第三人称检查**: ✅ 无第一/第二人称，无祈使句开头（"This skill should be used when..." 是被动陈述，非 "Use this skill to..."）

**WHAT 充分性检查**: ⚠️ description 只说了 "when"（什么时候用），没有明确说明 skill 做什么（"创建/生成 Claude Code 斜杠命令" 隐含在 "when creating" 里）。规范 §2.1 要求 WHAT + WHEN + KEYWORDS 三要素齐全，此处 WHEN 和 KEYWORDS 有，WHAT 相对薄弱。

### 2.3 可选字段
无 `allowed-tools`、`model`、`argument-hint` 等可选字段。SKILL.md 自身不需要参数，允许缺省。✅

### 2.4 其他 frontmatter 字段
仅 2 个字段（name + description），无禁用字段（§1.3 合规）。✅

### 2.5 Frontmatter 语法
YAML 正确，`---` 配对，无多字节字符。✅

---

## 3. Body 逐段结构分析

Body 共 210 行，7 个章节。符合 process 模式 ~200 行目标（✅ 精确命中），远低于 600 行硬限。

### About Slash Commands (L10-17, ~8 行)
介绍斜杠命令的存储位置（`.claude/commands/` 项目级、`~/.claude/commands/` 全局级）和适用场景。简洁，无冗余。

### When to Use This Skill (L19-27, ~9 行)
5 条触发场景，与 frontmatter description 的触发短语一致。✅

### Included Resources (L29-37, ~9 行)
三份参考文件的 one-line 摘要 + "Load these references as needed" 指引。路径正确（`references/xxx.md`，无跨技能引用）。✅

### Command Structure Overview (L39-52, ~14 行)
展示命令文件的最小骨架（frontmatter description/argument-hint + 标题 + 指令正文）。✅ 与 SCORING FMT-02/FMT-03 对齐。

**问题（🟠）**: 此节只展示最小骨架（~10 行），而 best-practices.md 的模板（L85-161）有 8 个子章节（What This Command Does / Usage / Implementation Steps / Important Notes / Error Handling / Example Output）。两处模板规模差异极大，SKILL.md 未说明"最小骨架 vs 完整模板"何时用哪个，生成者可能在两者间摇摆。

### Command Creation Workflow (L54-180, ~127 行，核心)

**Step 1: Determine Location (L56-68)**
- 通过 `git rev-parse --is-inside-work-tree 2>/dev/null` 自动探测位置 ✅
- 项目级 vs 全局级默认规则清晰，用户显式 override 规则清晰 ✅
- 与 SCORING SCOPE-02 的脚本检查（pattern `git rev-parse`）精确耦合 ✅

**Step 2: Show Command Patterns (L70-79)**
- 加载 patterns.md，展示 4 种模式，询问用户 "Which pattern is closest to what you want to create?" ✅
- **问题（🟡）**: 依赖用户回答后才继续；若用户不回答，未定义回退策略（应默认 Workflow Automation 或让 agent 自行判断）。

**Step 3: Gather Command Information (L81-136)**
- A. 命令名 + 用途（kebab-case 强制，✅/❌ 示例齐全）✅
- B. 参数（`<angle-brackets>` 必选 / `[square-brackets]` 可选）✅ 与 SCORING PROC-04 一致
- C. 工作流步骤（分析/主操作/结果处理/成功标准/错误处理）✅
- D. 工具约束（允许/禁止/上下文文件）✅
- 信息收集维度完整，与 SCORING PROC-02 的 LLM 判定问题逐字对齐 ✅

**Step 4: Generate Optimized Command (L138-153)**
- 加载 best-practices.md，5 条关键原则（祈使句、具体、预期结果、具体示例、错误处理）✅

**Step 5: Create the Command File (L155-172)**
- 完整路径构造 → `mkdir -p` → Write 工具 → 向用户确认（位置/功能/调用方式）✅ 与 QA-01 对齐
- **问题（🟡）**: `mkdir -p` 在 Windows 原生 cmd 下不可用，但 Claude Code 在 Windows 使用 Git Bash，实际可执行。可加跨平台说明。

**Step 6: Test and Iterate (L174-180, Optional)**
- 建议用户运行 `/command-name [arguments]` 测试并迭代 ✅ 与 QA-02 对齐

### Quick Tips (L182-197, ~16 行)
**问题（🟠）**: L192 写 "Use Bash tool for `pytest`, `pyright`, `ruff`, `prettier`, `make`, `gt` commands"——与 references/best-practices.md L197/L383/L537 的 "DO NOT use Bash tool for make commands" **直接矛盾**（详见 §4-1）。

### Summary (L199-210, ~12 行)
6 步流程回顾 + "Focus on creating commands that agents can execute autonomously"。✅

---

## 4. 逻辑一致性深度审查

### 4.1 🔴 Bash/make 指令自相矛盾（跨文件，3 处，高优先级）

| 位置 | 文本 | 语义 |
|------|------|------|
| SKILL.md L192 | "Use Bash tool for `pytest`, `pyright`, `ruff`, `prettier`, `make`, `gt` commands" | 用 Bash 跑 make |
| README.md L454-456 | "**Use Bash tool for**: `pytest`, `pyright`, `ruff`, `prettier`, `make`, `npm`, `yarn`, `gt`" | 用 Bash 跑 make |
| patterns.md L261 | "**IMPORTANT:** Always use Bash tool for pytest/pyright/ruff/prettier/make/gt commands" | 用 Bash 跑 make |
| best-practices.md L190 | "**Use the Bash tool for pytest/pyright/ruff/prettier/make/gt commands:**" | 用 Bash 跑 make |
| best-practices.md L197 | "**DO NOT use Bash tool for make commands**" | ❌ 禁用 Bash 跑 make |
| best-practices.md L383 | "**DO NOT use Bash tool for make commands** - this is less efficient and provides worse output handling." | ❌ 禁用 Bash 跑 make |
| best-practices.md L537 | "DO NOT use Bash tool for make commands"（紧跟在 "Use Bash tool to run make commands" 之后） | ❌ 禁用 Bash 跑 make |

**分析**: 4 个文件主张 "用 Bash 跑 make"，而 best-practices.md 内部 3 处（L197、L383、L537）宣称 "禁用 Bash 跑 make"。L383 紧随 "ALWAYS use Bash tool for ... make/gt commands" 出现，L537 紧随 "Use Bash tool to run make commands: `make all-ci`" 出现——显然是复制粘贴时把否定对象写错了：**本意应为 "DO NOT use Task/agent tool for make commands"**（否定词错挂在 Bash 上）。这是对执行 Agent 有实际危害的指令矛盾：若生成命令时照抄 best-practices 模板，可能生成"禁用 Bash 跑 make"的错误命令。

### 4.2 🟠 argument-hint 语义矛盾（examples.md 内部）
- 本技能自己的约定（SKILL.md L111、README L426-431）：`<angle-brackets>` = 必选参数
- examples.md Example 1 submit-stack frontmatter（L12）：`argument-hint: <description>` —— 尖括号 = 必选
- 但同一示例 L33-40 展示无参数调用 `/submit-stack`（"Without argument (will analyze changes automatically)"），L164 又明确标注 "Argument handling (optional `<description>`)" —— 必选标记与可选语义直接冲突。应为 `[description]`。

### 4.3 🟠 示例 3 与"命令必须自主执行"原则矛盾
- README L463-464 "Avoid in commands: Interactive prompts (commands must be autonomous)"
- SCORING FMT-03 "Command body is instructions to the agent, not a description for the user"
- 但 examples.md Example 3 (create-implementation-plan) 的正文（L404-441）是以**用户为读者**的第一人称交互式内容（"I'll help you create an implementation plan..."、"**What would you like to plan?**"），核心价值恰是交互式逐步审批。该示例与技能自身的质量标准正面冲突，读者无法判断交互式命令是否可接受。

### 4.4 🟡 gt 命令语法不一致
- patterns.md L46: "Use gt stack submit"
- examples.md L100: "gt submit --stack --publish --no-edit"
- 同一工具（Graphite）的提交命令有两种写法，生成者可能产出语法错误的命令。

### 4.5 🟡 prettier glob 错误
- examples.md L237-238: `make prettier # Runs: prettier --write '\*_/_.md'`
- 转义后的 glob `*_/_.md` 不是合法 prettier 模式（应为 `**/*.md`）。若被原样复制进命令，prettier 不会匹配任何文件。

### 4.6 🟡 示例句病句
- best-practices.md L18 将 "Use the Task tool with Bash tool" 列为 CORRECT 示例——句子本身无意义（Task 工具与 Bash 工具是互斥的执行通道），应为 "Use the Bash tool for pytest" 之类。

### 4.7 🟡 工具命名过时
- 全技能使用 "Task tool"（现为 Agent tool）、`subagent_type="subagent"`（现为 general-purpose/Explore/Plan）、"TodoWrite"（现为 todo）——generated 命令会包含过时工具名，在新版 Claude Code 中可能无法执行。

### 4.8 一致性良好的部分
- Step 1 位置探测逻辑在 SKILL.md / README / SCORING SCOPE-02 三处一致 ✅
- kebab-case 命名规则在 SKILL.md / README / best-practices / SCORING PROC-03 四处一致 ✅
- 6 步流程在 SKILL.md 与 README 中一致（README 为扩写）✅
- 4 模式定义在 SKILL.md / README / patterns.md / examples.md 四处一致 ✅

---

## 5. 参考文件内容级审查

### 5.1 references/patterns.md (363 行) — 🟢 质量高

**内容结构**:
- 4 主模式：Workflow Automation（Analyze→Act→Report）、Iterative Fixing（Run→Parse→Fix→Repeat）、Agent Delegation（Context→Delegate→Iterate）、Simple Execution（Parse Args→Execute→Return）
- 5 进阶模式：Multi-Agent Orchestration、Context File Priority、Conditional Tool Selection、Makefile Integration、Progressive Disclosure
- 模式选择指南表（L295-307，9 行场景→模式映射）+ 组合模式分析 + 模式专属写作要素清单

**优点**:
- 每个模式都有"When to use / Example workflow / Key features / Pattern example"四段式，结构统一
- 选择指南表是真正的决策树（spec §3.4 推荐形式）✅
- 组合模式分析（submit-stack 组合 3 模式、ensure-ci 组合 3 模式）展示了模式的可组合性，超出一般参考文件水平

**问题**:
- L46 "gt stack submit" vs examples.md "gt submit --stack"（见 §4.4）
- L199 `subagent_type="Explore"` 是真实 agent 类型，但 L203/L134 `subagent_type="subagent"` 是过时命名（见 §4.7）
- 无内部矛盾，结构自洽 ✅

### 5.2 references/examples.md (583 行) — 🟠 质量高但 3 处内部不一致

**内容结构**: 4 个完整命令（submit-stack / ensure-ci / create-implementation-plan / codex-review）+ 模式对比表 + 按模式的使用指引。

**Example 1 submit-stack（Workflow Automation）**:
- 优点: .PLAN.md 上下文优先级检查、条件分支、flag 逐一解释、反模式（"NEVER run additional exploration"）、示例输出——是技能中最好的示例之一
- 问题: `argument-hint: <description>` 与"optional"标注矛盾（§4.2）

**Example 2 ensure-ci（Iterative Fixing）**:
- 优点: 10 次迭代上限、3 次同错卡死检测、按错误类别的定向修复指令、TodoWrite 进度跟踪、SUCCESS/STUCK 双报告格式、示例迭代流——迭代控制的完整范本
- 问题: prettier glob 转义错误（§4.5）；L244 提到 "Follow the coding standards in AGENTS.md (use `list[...]` not `List[...]`)"——把 AGENTS.md 当作必然存在的文件，但未给不存在时的回退路径

**Example 3 create-implementation-plan（Agent Delegation）**:
- 问题（🟠）: 用户向交互式正文与"命令必须自主"原则冲突（§4.3）；"saved as a `.md` file at the repository root" 未给出文件名规范（对比 create-implementation-plan 模式的 .PLAN.md 惯例）；"IMPORTANT AGENT INSTRUCTIONS" 与用户向正文混排，Agent 需自行分辨哪些段落是给自己的指令
- 优点: 阶段边界（planning vs implementation）清晰、用户审批触发词（"looks good" / "approved"）具体

**Example 4 codex-review（Simple Execution）**:
- 优点: 可选参数默认值逻辑（main/master 探测）完整
- 问题（🟡）: 引用 `scripts/codex-review.py` 外部脚本，但技能未说明该脚本从何而来（示例性质可接受，但生成者可能误以为脚本自动存在）

**对比表（L543-552）**: 7 个维度 × 4 示例，信息密度高，是极佳的教学工具 ✅

### 5.3 references/best-practices.md (719 行) — 🟠 模板最佳但 3 处致命矛盾

**内容结构**: 写作风格（祈使句/具体性/预期结果/具体示例）、8 子章节模板、7 个 agent 优化元素（显式文件检查/工具指引/反模式/条件逻辑/成功标准/错误处理/进度跟踪）、4 个通用模式、31 项质量清单、7 个常见陷阱、4 个进阶实践（多步验证/迭代控制/上下文收集/输出格式）、10 条总结。

**优点**:
- 模板的 8 子章节结构（What This Command Does → Usage → Implementation Steps → Important Notes → Error Handling → Example Output）是本技能对生成命令质量贡献最大的部分
- 反模式（NEVER/DO NOT）风格贯彻到位（除 4.1 的错误外）
- 31 项质量清单可操作性极强（Structure 6 项 / Content 8 项 / Writing Style 4 项 / Location 4 项 / Testing 3 项 + 杂项）
- "Stuck Reporting Format" 与 "Success Reporting Format" 是其他技能罕见的输出规范

**问题**:
- 🔴 Bash/make 矛盾 ×3（L197/L383/L537，§4.1）
- 🟡 L18 病句（§4.6）
- 🟡 模板代码块内全部使用转义反引号（\`\`\`），直接复制需手工还原；作为教学模板可接受，但应注明
- 🟡 质量清单无 "single responsibility" 与 "explicit dependencies" 项，而 SCORING QA-03 的判定问题引用这两项（§10-3）
- 🟡 L197 所在小节标题 "Tool Usage Guidance" 与 L383 所在小节 "Makefile Integration" 均把 "DO NOT use Bash for make" 作为结论，若执行 Agent 从该文件学习，会同时收到两条互斥指令

---

## 6. 语法与格式质量

### SKILL.md / README.md / references（Markdown）
- Markdown 语法正确，标题层级一致，无散落的反引号 ✅
- 无 emoji、无中文混排、无乱码 ✅
- README 目录锚点（Overview→Common Use Cases 共 11 个）与实际标题一一对应 ✅
- 代码块语言标注（bash/markdown/yaml）规范 ✅
- best-practices.md 模板块使用 `\`\`\`` 转义属于教学必需，但 L14-25、L31-43 等"✅ CORRECT / ❌ WRONG"列表未用代码块包裹，长列表可读性略降 🟡

### SCORING.yaml
- YAML 语法正确，18 个 criterion 结构统一（id/category/description/judge/check）✅
- `total_items: 18` 与实际 criterion 数一致（SCOPE 3 + PROC 5 + FMT 4 + TEC 2 + NEG 1 + QA 3 = 18）✅
- 正则 pattern 中 `[\\/]` 的双转义在 YAML 单引号与 Python 字符串中的行为不同（§10-5），但最终语义等价 ✅

### check.py
- 语法正确，可运行（imports 全部来自 _shared/checker.py，已验证存在）✅
- **问题（🟡）**: 13 个未使用的 import（file_contains, file_valid_json, json_field_*, json_array_*, timestamp_*, tool_log_read_before_write, tool_log_order, output_contains, output_not_contains）
- **问题（🟡）**: L24-27 的 docstring 声称 "Run all 18 checks"，实际只返回 7 项
- **问题（🟠）**: L26-27 `set_agent_output(agent_output)` 把 **路径字符串** 当作 agent 输出内容写入（main() L69-70 已从文件读入真实内容），覆盖了正确值。当前无脚本检查消费 agent 输出，属潜伏缺陷；未来若新增 output_* 检查将直接误判

---

## 7. 规范合规性（对照 SKILL-SPEC.md v1.0）

| 检查项 | 判定 | 说明 |
|--------|:----:|------|
| name 小写+连字符，≤64，匹配目录 | ✅ | `command-creator` = `216-command-creator` 的 slug |
| description 第三人称 + WHAT + WHEN + KEYWORDS | ⚠️ | 第三人称 ✅；WHAT 薄弱（§2.2）；触发信号 ✅（"Use when users ask to"，复数偏差） |
| description ≤1024 字符 | ✅ | 297 字符 |
| description 无祈使/一二人称开头 | ✅ | 被动陈述 "This skill should be used when..." 可接受 |
| 无跨技能路由嵌入 description | ✅ | 无 "NOT for X" |
| 至少一个触发信号短语 | ✅ | "Use when users ask to..." |
| frontmatter 无禁用字段 | ✅ | 仅 name + description |
| body ≤600 行 | ✅ | 210 行 |
| body 含 Workflow/Process 节 | ✅ | "Command Creation Workflow" 6 步 |
| body 含 Output Format 节 | ⚠️ | 仅 "Command Structure Overview" 展示命令文件骨架，无专门输出/交付物节 |
| body 含 Scope/Limitations 节 | ❌ | **缺失**——无任何 "What This Skill Does NOT Do" 内容 |
| body 无跨技能文件引用（../） | ✅ | 全部为 references/ 相对路径，无一处 `../` |
| 目录命名 NNN-kebab-case | ✅ | `216-command-creator` |

**合规得分**: 12 项中 9 项 ✅、2 项 ⚠️、1 项 ❌（Scope 缺失）。这是与 001/003/005 等已审查技能相同的常见缺口——process 型技能几乎普遍缺 Scope 节。

---

## 8. 人机感评估

### SKILL.md（引导者口吻）— 🟢
- 6 步流程以 "Ask the user..." 开头的问题驱动，交互节奏自然
- "Report the chosen location to the user before proceeding" 等步骤体现了过程透明度
- 语气中性专业，无推销腔

### README.md（营销文档口吻）— 🟡
- "A comprehensive skill...", "expert guidance", "ensures your commands are: Reliable / Maintainable / Reusable / Optimized"——促销式形容词密度偏高
- 523 行中约 60% 与 SKILL.md 内容重复（6 步流程、4 模式、命名规则、参数提示各出现 2 次）。README 作为技能入口文档（若被 Agent 读到）会显著稀释 SKILL.md 的指令密度
- "Get Started: `/command-creator`" 将 skill 描述为斜杠命令——在 Claude Code 中 skill 通过 Skill 工具触发而非 `/command-creator` 斜杠命令，轻微误导

### references（教学范本口吻）— 🟢
- 示例源自 erk 项目真实命令，命名具体（switch.py:45、PR #123），符合 "Concrete over abstract"（spec §3.4）
- ✅/❌ 对照形式降低阅读负担；对比表信息密度高
- ensure-ci 的 SUCCESS/STUCK 报告格式可直接套用

**综合**: 引导流程是 322 个技能中较成熟的之一（问题驱动 + 透明汇报 + 可选迭代），但 README 与 SKILL.md 的内容重复和促销语气拖累整体印象。

---

## 9. 可执行性评估

### 技能自身可执行性 — 🟢（主体）
- Step 1 有精确的 bash 命令（`git rev-parse --is-inside-work-tree 2>/dev/null`），无需 agent 推断 ✅
- Step 5 有目录创建（`mkdir -p`）与 Write 工具调用路径 ✅
- 每一步的输出/汇报对象明确（"Report the chosen location"、"Confirm with the user"）✅
- 7 项脚本检查与 SKILL.md 指令精确耦合（git rev-parse / commands/*.md / argument-hint / description / references 读取）✅

### 生成命令的可执行性风险 — 🟠
- **最高风险**: best-practices.md 的 Bash/make 矛盾（§4.1）——照模板生成的命令可能包含 "DO NOT use Bash tool for make commands" 这类错误约束，直接破坏生成命令的自主执行
- 示例 3 的用户向交互式正文若被原样复用，生成的命令会以 "I'll help you..." 开头向用户说话，而非执行指令（正是 CF-02 的 cap_to_0 场景）
- 过时工具名（Task/subagent/TodoWrite）在新版 harness 下可能导致生成的命令调用不存在的工具

### SCORING 脚本检查的盲区 — 🟠
- **FMT-01 只查项目级路径**: `file_exists(workspace/.claude/commands/*.md)` 无法验证全局命令（~/.claude/commands/）。若 Agent 依据规则在非 git 目录下创建全局命令，FMT-01 必然失败——该检查对"正确行为"存在系统性惩罚
- **PROC-04 无条件要求 argument-hint**: 标准文本是"当命令带参数时"添加，脚本却无条件要求工具日志中出现 "argument-hint"。对无参数命令（如 ensure-ci 示例），正确行为会被判失败
- **NEG-01 只查下划线**: 标准文本还包含 "no vague/ambiguous instructions"，脚本只查 `commands/..._....md` 模式，模糊指令完全无脚本覆盖
- **CF-01/02/03 无任何执行路径**: check.py 未实现 critical_failures 的检测，cap_to_0 机制在脚本端不存在

---

## 10. SCORING.yaml 交叉参考

### 10.1 总览
- `total_items: 18`，类别分布: scope 3 / process 5 / format 4 / technical 2 / negative 1 / qa 3 ✅ 计数正确
- 判定方式: `judge: script` 7 项 + `judge: llm` 11 项
- check.py 实现的 7 项与 SCORING 的 script 项一一对应（SCOPE-02, PROC-03, PROC-04, FMT-01, FMT-02, TEC-01, NEG-01）✅ 映射无遗漏无多余

### 10.2 逐项映射核查

| ID | 判定 | check.py 行 | 一致性 |
|----|:----:|:-----------:|:------:|
| SCOPE-02 | script | L33 `tool_log_contains("git rev-parse")` | ✅ 与 SKILL.md Step 1 指令一致 |
| SCOPE-01, SCOPE-03 | llm | 未实现（注释说明） | ✅ 合理 |
| PROC-03 | script | L38 `commands[\\/][a-z0-9-]+\.md` | ✅ 正则等价（§10-5） |
| PROC-04 | script | L39 `argument-hint` | ⚠️ 无条件检查，忽略"当命令带参数时"条件（§9） |
| PROC-01, PROC-02, PROC-05 | llm | 未实现 | ✅ |
| FMT-01 | script | L43 项目级 file_exists | ⚠️ 全局命令盲区（§9） |
| FMT-02 | script | L44 `[\n]description` | ✅ 匹配 frontmatter |
| FMT-03, FMT-04 | llm | 未实现 | ✅ |
| TEC-01 | script | L48 `(patterns\|examples\|best-practices)\.md` | ⚠️ 若工具日志含 Read 输出（含正文），读 README 即可命中，存在弱假阳性风险 |
| TEC-02 | llm | 未实现 | ✅ |
| NEG-01 | script | L52 下划线模式 | ⚠️ 标准中的"模糊指令"部分无覆盖（§9） |
| QA-01, QA-02, QA-03 | llm | 未实现 | ✅ |

### 10.3 QA-03 判定问题与清单不一致（🟡）
QA-03 的 question 引用 "single responsibility, clear description, explicit dependencies, documented arguments"——但 best-practices.md 的 31 项质量清单中没有 "single responsibility" 和 "explicit dependencies" 两项。LLM 判定时参照物不存在，判定口径会漂移。

### 10.4 Critical Failures 无脚本执行（🟠）
CF-01（文件名下划线/非法命名）、CF-02（正文写给用户）、CF-03（位置错误）均 `cap_to_0`，但 check.py 没有任何 CF 检测逻辑，SCORING 也未给 CF 指定 llm judge——CF 实际上永远不会被触发。

### 10.5 正则转义等价性（✅）
- SCORING.yaml 单引号内: `'commands[\\/][a-z0-9-]+\.md'` → 字符串 `commands[\/]...\.md` → 正则匹配 `commands/` 或 `commands\`（字符类含反斜杠与斜杠）
- check.py 双引号内: `"commands[\\\\/][a-z0-9-]+\\.md"` → 字符串 `commands[\\/]...\.md` → 正则 `[\\/]` = 反斜杠或斜杠
- 两者最终语义一致 ✅

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md（memory）对 216 的唯一专项评语（L994，逻辑维度）:

> "216 与 202 高度重叠"

**验证**: ✅ 属实。对比两技能的 description 触发短语:

| 触发短语 | 216-command-creator | 202-command-development |
|----------|:---:|:---:|
| "create a command" | ✅ | ✅ |
| "add a command" | ✅ | ✅ |
| "make a slash command" | ✅ | (近似 "create a slash command") |
| "write a custom command" | — | ✅ |
| "define command arguments" | — | ✅ |
| "use AskUserQuestion in command" | — | ✅ |

- **区分度**: 216 专注"创建流程 + 模式 + 最佳实践"（本技能独有: 4 模式分类、位置探测、3 参考文件）；202 专注"命令结构 + frontmatter + 动态参数 + bash 执行 + 交互模式"（AskUserQuestion、file references 等 216 未覆盖）
- **风险**: 用户说 "create a command" 时两个技能都可能被触发，Agent 可能加载 216 的流程指引 + 202 的结构指引造成内容混搭，或错误选择其中之一导致覆盖缺失
- **建议**: 216 的 description 中增加与 202 的边界提示（如 "for structural guidance see: command-development"），或在 body 增加 Scope 节声明不覆盖的内容（正好弥补 §7 的 Scope 缺失）

---

## 12. 综合评分

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.80 | 触发信号 ✅，WHAT 薄弱 + "Essential" 促销语 |
| Body 结构完整 | 6/10 | 10% | 0.60 | 6 步流程完整，Scope 缺失 + Output 节不完整 |
| 逻辑一致性 | 5/10 | 20% | 1.00 | Bash/make 矛盾 ×3 + argument-hint 矛盾 + 交互示例冲突 |
| 参考完整性 | 8/10 | 15% | 1.20 | 3/3 存在且结构优秀，但相互间存在语法/命名不一致 |
| 语法格式 | 7/10 | 10% | 0.70 | Markdown/YAML 规范，check.py 死 import + 潜伏 bug |
| 规范合规 | 7/10 | 15% | 1.05 | 12 项中 9 ✅，Scope 缺失为唯一 ❌ |
| 人机感 | 7/10 | 10% | 0.70 | 流程引导成熟，README 促销语气 + 与 SKILL.md 重复 |
| 可执行性 | 7/10 | 10% | 0.70 | 主体可执行，Bash/make 矛盾 + 脚本盲区（FMT-01/PROC-04） |
| **加权总分** | | | **67.5/100** | |

🟡 **C+** (67.5/100) — 设计意图优秀（4 模式 + 3 参考文件的创建器架构是 process 型技能的优质模板，examples.md 的对比表与 best-practices.md 的模板是全语料亮点），但 best-practices.md 中 3 处自相矛盾的 Bash/make 指令是必须优先修复的执行危害。修复后有望升至 B+ 区间。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷
1. **修复 best-practices.md 的 Bash/make 矛盾（L197、L383、L537）** — 将 "DO NOT use Bash tool for make commands" 改为 "DO NOT use the Task/agent tool for make commands"（与 SKILL.md L192、README L454、patterns.md L261 的统一口径一致）。这是本技能最紧急的修复。

### 🟠 重要缺陷
2. **补充 Scope/Limitations 节** — SKILL.md 增加 "## What This Skill Does NOT Do"：不覆盖命令结构/参数细节（转引 202-command-development）、不适用于非 Claude Code 环境的命令、不生成命令的测试框架
3. **修复 examples.md Example 1 的 argument-hint** — `<description>` 改为 `[description]`，消除与 "optional" 标注和 Usage 无参调用的矛盾（L12）
4. **示例 3 交互式正文与原则冲突** — 在 examples.md 增加说明：交互式命令仅在明确需要用户审批时使用（作为例外模式），或在正文前加 "以下为用户向内容，agent 应跳过" 的分隔说明
5. **check.py 修复** — (a) check() 中删除 `set_agent_output(agent_output)` 覆盖（或改为接收已读内容）；(b) 修正 docstring "Run all 18 checks" → "Run 7 script checks"；(c) 删除 13 个未使用 import
6. **FMT-01 支持全局命令** — 增加对 `~/.claude/commands/*.md` 的检查（或允许通过环境变量指定），消除对全局创建的惩罚

### 🟡 优化建议
7. **description 打磨** — 删除 "Essential for creating..."；"Use when users ask to" → "Use when the user asks to"；补充 WHAT（"Guides creation of optimized, agent-executable slash commands with patterns, templates, and best practices"）
8. **PROC-04 改为条件检查** — 当生成的命令无参数时不应强制要求 argument-hint；或由 LLM judge 兜底该条件
9. **统一 gt 语法** — patterns.md L46 "gt stack submit" 与 examples.md "gt submit --stack" 二选一
10. **修复 prettier glob** — examples.md L238 `'\*_/_.md'` → `'**/*.md'`
11. **工具名现代化** — Task tool → Agent tool；`subagent` → `general-purpose`/`Explore`/`Plan`；TodoWrite 加注
12. **QA-03 口径对齐** — 在 best-practices.md 清单中补充 "single responsibility" 与 "explicit dependencies" 两项，或改写 QA-03 的 question
13. **216/202 路由边界** — 与 202-command-development 的 description 互相引用或由评测集分配明确场景

### 修复工作量估计
- 预计修改行数: ~80-120 行
- 预计修改文件数: 5（SKILL.md + references/best-practices.md + references/examples.md + references/patterns.md + check.py）
- 最大单项工作: 修复 Bash/make 矛盾（3 处，约 10 行）+ Scope 节（~15 行）
- 无需结构性重构——问题全部为局部编辑

---

## 变更记录
- 2026-08-06: 首次审查（本文件）。通读全部 7 个文件（SKILL.md + README.md + SCORING.yaml + check.py + references/ 3 文件，约 2,645 行）。主要发现：best-practices.md 3 处 Bash/make 自相矛盾（L197/L383/L537）、Scope 节缺失、examples.md 的 argument-hint 语义矛盾、check.py 潜伏 set_agent_output bug + FMT-01/PROC-04 脚本盲区、与 202-command-development 触发重叠。评级 🟡 C+ (67.5/100)。

---

## 附录: 审查过程记录
- 读取文件数：7/7（全量读取，无采样）
  - SKILL.md (210 行) ✅
  - README.md (523 行) ✅
  - SCORING.yaml (168 行) ✅
  - check.py (79 行) ✅
  - references/patterns.md (363 行) ✅
  - references/examples.md (583 行) ✅
  - references/best-practices.md (719 行) ✅
- 辅助阅读：`_shared/SKILL-SPEC.md` v1.0（合规依据）、`_shared/checker.py`（验证 file_exists 支持 glob、tool_log_contains 正则语义）、202-command-development/SKILL.md（重叠验证）、skill-dossier.md（memory，216 条目）
- 规范依据：_shared/SKILL-SPEC.md v1.0（12 项合规清单）
- 交叉验证：description 长度 297 字符（python 实测）、正则转义等价性（YAML vs Python 字符串）、SCORING 18 项计数（3+5+4+2+1+3）
- 审查方法：逐文件全文阅读 → 跨文件一致性比对（工具名/命令语法/参数约定 3 个维度）→ SCORING 与 check.py 逐项映射 → 规范清单逐项核对
