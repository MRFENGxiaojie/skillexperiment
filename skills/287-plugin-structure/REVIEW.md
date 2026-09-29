# 287-plugin-structure 深度审查报告

- **审查对象**: `D:\SkillIF\skill-experiment\complex-skills\287-plugin-structure\`
- **审查日期**: 2026-08-06
- **审查方式**: 全部 9 个文件逐字全文通读（SKILL.md、README.md、SCORING.yaml、check.py、examples/×3、references/×2），未抽样
- **总体结论**: 🟡 **可用但存在结构性缺口** — 内容领域深度与内部一致性出色，示例与参考文件体系完整；但按 SKILL-SPEC v1.0 硬性要求，body 缺少 Workflow/Process、Output Format、Scope/Limitations 三必需节，description 触发语非规范短语，SCORING 与技能自身内容存在两处互相矛盾。补齐后可升 🟢。
- **综合评分**: **77 / 100**（8 维加权，详见第 12 节）

---

## 1. 目录清单

本 skill 目录共 9 个文件，3352 行（wc -l 实测，CRLF 换行）：

| # | 文件 | 行数 | 角色 |
|---|------|-----:|------|
| 1 | `SKILL.md` | 459 | 技能主文件（frontmatter 4 行 + body ~455 行） |
| 2 | `README.md` | 109 | 技能说明/维护文档（非运行时内容） |
| 3 | `SCORING.yaml` | 144 | 测评标准（15 项 criterion + 3 项 critical failure） |
| 4 | `check.py` | 86 | 脚本检查器（6 项 script judge 落地） |
| 5 | `examples/minimal-plugin.md` | 83 | 最小插件示例（单命令） |
| 6 | `examples/standard-plugin.md` | 587 | 标准生产插件示例（全组件） |
| 7 | `examples/advanced-plugin.md` | 765 | 企业级插件示例（MCP + 分层） |
| 8 | `references/manifest-reference.md` | 552 | plugin.json 字段完整参考 |
| 9 | `references/component-patterns.md` | 567 | 组件组织模式进阶参考 |

目录命名 `287-plugin-structure` 符合 `NNN-kebab-case` 约定（§4）。文件层次（SKILL.md + 3 examples + 2 references + 测评三件套）与 README 所述 progressive disclosure 结构一致。`_shared/` 为跨 skill 共享测评库，不属于本 skill 内容，不在此审查范围。

---

## 2. Frontmatter

### 2.1 字段与值

frontmatter 仅含两个字段，干净无冗余：

```yaml
name: plugin-structure
description: "This skill should be used when the user requests \"create a plugin\", \"structure a plugin\", ..."
```

### 2.2 name 字段（通过）

- 小写 + 连字符，≤64 字符，与目录名 `287-plugin-structure` 去除 NNN 前缀后一致（§1.1、§4）✓

### 2.3 description 字段（部分通过，两处偏差）

**长度**: 实测 438 字符（YAML 解析后的未转义值），远低于 1024 上限 ✓。

**WHAT + WHEN + KEYWORDS（§2.1）**:
- WHEN：非常充分 — 9 个带引号的用户请求短语（"create a plugin"、"structure a plugin"、"understand plugin structure"、"organize plugin components"、"configure plugin.json"、"use ${CLAUDE_PLUGIN_ROOT}"、"add commands/agents/skills/hooks"、"configure auto-discovery"）+ 4 个需求场景（directory layout、manifest configuration、component organization、file naming conventions）。
- KEYWORDS：充分 — plugin、plugin.json、commands/agents/skills/hooks、CLAUDE_PLUGIN_ROOT、auto-discovery 均出现。
- WHAT：**隐式缺失**。description 通篇是"什么时候该用"，没有一句陈述"这个 skill 做什么"（如 "Provides guidance on Claude Code plugin architecture..."）。"or needs guidance on plugin directory layout..." 仍是 WHEN 从句。§2.1 要求三问齐答，此处 WHAT 只能从 WHEN 反推，属轻微合规偏差。

**人称（§2.3）**: "This skill should be used when the user requests..." — 第三人称被动式，无祈使/第一/第二人称，通过 ✓。

**触发信号（§2.4）**: **偏差**。"This skill should be used when the user requests" 不属于 §2.4 允许的五种短语（"Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."）。语义上最接近 "Use when the user asks to"，但字面不匹配。dossier 中 303-marp-slide 的 "Use when users request" 已被判定为偏离规范，此处同型。触发信号是描述匹配机制的关键部件，建议改为规范短语。

**禁止项（§2.5）**: 无跨 skill 路由、无空泛描述、长度 >40 字符 ✓。

---

## 3. Body 结构

### 3.1 章节总览

SKILL.md body（~455 行）共 11 个二级章节，按"结构→清单→组件→路径→命名→发现→实践→模式→排障"的知识顺序编排：

| 章节 | 行范围 | 性质 |
|------|--------|------|
| Overview | 8-17 | 关键概念列表 |
| Directory Structure | 19-41 | 目录树 + 4 条 critical rules |
| Plugin Manifest | 43-103 | 必需字段/推荐元数据/自定义路径 |
| Component Organization | 105-243 | Commands/Agents/Skills/Hooks/MCP 五类 |
| Portable Path References | 245-290 | ${CLAUDE_PLUGIN_ROOT} 规则 |
| File Naming Conventions | 292-326 | 组件/支持文件命名 |
| Auto-Discovery Mechanism | 328-344 | 加载流程 + 时机 |
| Best Practices | 346-391 | 组织/命名/可移植/维护 |
| Common Patterns | 393-429 | 最小/完整/纯技能三模式 |
| Troubleshooting | 431-455 | 四类常见问题排查 |

### 3.2 必需三节检查（§3.1）

- **Workflow/Process：缺失**。没有任何章节指导 agent "当用户请求创建插件时应做什么、按什么步骤做"。最接近的是 Auto-Discovery Mechanism（328-344），但那是描述 Claude Code 平台自身的加载流程，不是本 skill 的执行流程。Directory Structure→Manifest→Components 的顺序隐含"先建目录、再写清单、再放组件"的次序，但从未显式声明为步骤，没有 Step 1/2/3，没有每步输入输出。
- **Output Format：缺失**。全文没有章节说明"交付物长什么样"——是否要给出目录树、每个文件的完整内容、加载行为说明、验证清单。deliverables 完全靠 example 文件暗示。
- **Scope/Limitations：缺失**。Troubleshooting（431-455）不是 Scope——它不回答"这个 skill 不做什么、何时不该用它"。例如：本 skill 不涉及插件打包/发布（marketplace）、不涉及 hooks 具体编写逻辑、不涉及 MCP server 内部实现——这些边界均未声明。

这是本 skill 最核心的结构缺陷：**内容上是"参考手册"而非"可执行技能"**。值得注意的是 SKILL.md 本身行数 459 ≤ 600（硬限通过），但超出 tool 模式 ~300 行目标约 50%；Best Practices 与 Troubleshooting 大量内容与 references/ 重叠，若补三节，行数会逼近上限，需要同步瘦身（详见第 13 节）。

### 3.3 渐进披露

README 声称 SKILL.md ~1600 词、references ~6000 词、examples ~8000 词，按需加载。实际编排符合该宣称：核心规则在 body，细节在 references/，完整落地在 examples/。三层次之间内容衔接良好（例如自定义路径规则在 body 97 行、manifest-reference 332-351 行、component-patterns 93-131 行、advanced-plugin 131-142 行四处出现且口径一致）。这是本 skill 最出色的设计点之一。

---

## 4. 逻辑一致性

### 4.1 全局一致（通过项）

- **目录布局规则全文件统一**: `.claude-plugin/plugin.json` 必须在插件根（SKILL.md:38、manifest-reference.md:7-9、三个示例的目录树），组件目录必须在插件根层而非 `.claude-plugin/` 内（SKILL.md:39、SCORING PROC-02、CF-02）——四处口径一致。
- **自定义路径"补充而非替换"默认目录**: SKILL.md:97、manifest-reference.md:237/344、component-patterns.md:344 统一。
- **路径规则（相对 + `./` 前缀 + 禁止绝对路径）**: SKILL.md:99-103、manifest-reference.md:336-350、SCORING PROC-06 统一。
- **${CLAUDE_PLUGIN_ROOT} 用于 hooks/MCP/脚本**: SKILL.md:247-271、standard-plugin.md:81/448、advanced-plugin.md:152-172/639-695、SCORING PROC-05 统一。
- **hooks 事件清单**（SKILL.md:218）: PreToolUse、PostToolUse、Stop、SubagentStop、SessionStart、SessionEnd、UserPromptSubmit、PreCompact、Notification —— 与 Claude Code 现行事件集吻合，advanced-plugin 的 hooks.json 也只使用其中 PreToolUse/PostToolUse/Stop/SessionStart 四个合法事件。
- **嵌套命令需自定义路径**: component-patterns.md:111 明确声明 "Claude Code doesn't support nested command discovery automatically. Use custom paths"，与 advanced-plugin.md:131-142 的 `commands: ["./commands/ci", ...]` 严格互证。
- **manifest 三种形态（最小/推荐/完整）** 在 SKILL.md:393-429、manifest-reference.md:449-519、三个 examples 之间数字字段（如 enterprise-devops 版本 2.3.1）完全对得上。

### 4.2 局部矛盾与缺陷（问题项）

1. **"No restart required" 措辞自相矛盾（SKILL.md:339-342）**。标题句 "No restart required" 紧跟正文 "Changes take effect on next Claude Code session"——若需下一会话才生效，实质就要求重开会话。两句并列读起来互相否定。SCORING OUT-03 的问题文本原样复制了这对矛盾（"changes apply on the next session without restart"），是同一个瑕疵的一体两面。

2. **JS 中使用 ${CLAUDE_PLUGIN_ROOT} 的示例不可运行（advanced-plugin.md:293, 301）**。`const { DatadogClient } = require('${CLAUDE_PLUGIN_ROOT}/lib/integrations/datadog')` — 在 shell 上下文（hook command、bash 脚本）中 `${CLAUDE_PLUGIN_ROOT}` 会被环境变量展开，但 Node.js 的 `require()` 不会做任何展开，该字符串在运行时是字面量，文件必然找不到。SKILL.md:257-271 把 "${CLAUDE_PLUGIN_ROOT} for all intra-plugin path references" 讲成通用规则，但未说明该变量的展开机制（shell 层展开）及 JS 场景应改用 `process.env.CLAUDE_PLUGIN_ROOT`。示例本身是高级插件示例，agent 照抄必然踩坑。

3. **示例内层 skill 的 frontmatter 违反命名与字段规范（standard-plugin.md:228-230、advanced-plugin.md:314-316）**。`name: Code Standards`、`name: Kubernetes Operations` 含空格非 kebab-case（SKILL.md:41 自己声明 "Use kebab-case for all directory and file names"），且带 `version: 1.0.0/2.0.0` 字段——SKILL-SPEC §1.3 明令禁止 version 字段。虽然这是"示例中的插件内 skill"，agent 从 examples 复制 frontmatter 时会学到错误模板。SKILL.md:176-185 的 "SKILL.md format" 模板同样带 `version: 1.0.0`，且 name 复用本技能自己的 `plugin-structure`（第 179 行），属于把自身元数据抄进模板的复制粘贴痕迹——同文件的 commands 模板（SKILL.md:120-127，name: plugin-structure 出现在第 122 行）也是同一问题。

4. **SCORING PROC-01 与 manifest-reference 的 name 校验正则互相矛盾（详见第 10 节）**。SCORING 允许数字开头（`^[a-z0-9]+(-[a-z0-9]+)*$`），reference 要求字母开头（`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`）。

5. **SCORING PROC-08 与本 skill 自述的 minimal pattern 冲突（详见第 10 节）**。

6. **advanced-plugin 存在"未被任何文件引用的空组件"**：`hooks/scripts/quality/verify-tests.sh`（树 63 行，hooks.json 未引用）、`skills/kubernetes-ops/scripts/health-check.sh`（树 44 行，SKILL.md body 只提 validate-manifest.sh）、`lib/integrations/pagerduty.js`（树 86 行，仅 Slack/Datadog 被引用）。而 SKILL.md:40 明确 "Only create directories for components the plugin actually uses"、PROC-03 也考核此项——示例自身即违反技能规则（反例级矛盾，虽然只影响示例完整性不影响执行）。

7. **standard-plugin 的 style-guide.md 悬空引用（standard-plugin.md:420-423）**。正文 "See language-specific guides for: Go: `references/go-style.md`, Rust: `references/rust-style.md`, Ruby: `references/ruby-style.md`" — 这三个文件在示例目录树（7-35 行）中不存在，只有 style-guide.md。若作为内部路径是断链；若指外部文档则未说明。同为示例内断链。

8. **"prompt" 型 hook 未在任何正文/参考中说明（standard-plugin.md:435-437）**。hooks.json 中 `"type": "prompt"` 是一个 body（SKILL.md:204-216）与 manifest-reference 均未记载的 hook 类型。示例引入了技能未传授的概念。

9. **description 的 WHAT 缺失**（见 2.3），不再重复。

---

## 5. 参考文件（全文逐文件分析）

本节对全部 9 个文件逐一给出内容分析。SKILL.md 已在第 2-4 节详析，此处只作补充定位。

### 5.1 SKILL.md（459 行）— 内容主文件

领域内容覆盖面完整：目录布局 → manifest → 五类组件 → 路径 → 命名 → 自动发现 → 实践 → 模式 → 排障，闭环无遗漏。4 条 critical rules（38-41）是全文质量最高的部分——精确、可机检（全部被 SCORING 化为脚本或 llm judge 检查项）。Directory Structure 树（23-35）与 example 目录树一致。Troubleshooting（431-455）四组问答（组件不加载/路径错误/自动发现失效/插件冲突）均可直接操作。缺陷集中于第 3、4 节所列：三必需节缺失、模板示例复用自身 name、version 字段入模板、"No restart required" 矛盾。行数 459 ≤600 硬限通过。

### 5.2 README.md（109 行）— 元文档

结构清晰的技能说明书：功能列表、SKILL.md 内容索引、references/examples 深度摘要、触发场景、渐进披露层级、维护指南。两处值得注意：
- 95-100 行 Related Skills 以散文点名 `hook-development`、`mcp-integration`、`marketplace-publishing`（后两者标注 "(when available)"）。以名称引用其他 skill 是 §3.3 允许的形式，不构成违规。
- 维护清单第 5 条 "Ensure all documentation uses imperative/infinitive form" 与 description 必须第三人称的规则（§2.3）容易让人误读为"描述也用祈使句"——实际仅指正文文档风格，但措辞未区分，属轻微表述风险。
- 17 行声称 SKILL.md "1,619 words"、87-92 行声称 references ~6000 词/examples ~8000 词，与实际字数（references 两文件共 ~5,400 词量级）为约数，可接受。

### 5.3 SCORING.yaml（144 行）— 测评标准

结构规范：`pattern: tool`、`total_items: 15`（scope 2 + process 8 + output 3 + negative 1 + qa 1 = 15，计数自洽）。judge 分配：6 项 script + 9 项 llm，与 check.py 实际执行的 6 项一一对应（SCOPE-02、PROC-01、PROC-02、PROC-08、OUT-01、NEG-01）。criterion 描述与 SKILL.md 内容高度对齐（PROC-05 的 `${CLAUDE_PLUGIN_ROOT}`、PROC-06 的 `./` 前缀、PROC-07 的 frontmatter 要求、OUT-03 的自动发现解释）。3 条 critical_failures（manifest 缺失/组件嵌套/硬编码路径）都是能真正导致插件不可用的硬失败，`cap_to_0` 语义合理。**主要问题见第 10 节**（PROC-01 正则、PROC-08 与 minimal pattern 冲突、NEG-01 误报面、CF-02 的 "wrong file names" 判定标准模糊）。

### 5.4 check.py（86 行）— 脚本检查器

实现与 SCORING 严格对应：6 个 script judge 全部落地，docstring "Run all 6 script checks" 与实际一致。技术质量良好：
- `sys.path.insert` 引入 `../_shared/checker`（11 行），属于测评基建跨目录依赖，不违反技能正文的跨 skill 路径禁令；
- json_field_matches 校验 name 的 kebab 正则（39-43 行）与 SCORING 逐字一致；
- NEG-01 的 `tool_log_not_contains("claude-plugin/(commands|agents|skills|hooks)")`（57-59 行）逻辑与 SCORING 一致；
- main() 读取 agent output 文件（75-77 行）供 output 类检查使用，参数校验完整（68-70 行）。
小瑕疵：`import re`（第 4 行）未使用；PROC-08 用 glob `skills/*/SKILL.md`（49 行）要求至少一个 skill，语义问题同 SCORING（见 10 节）；无单元测试。

### 5.5 examples/minimal-plugin.md（83 行）— 最小插件示例

与 SKILL.md:395-402 的 Minimal Plugin 模式完全同构：`hello-world` 插件（kebab-case ✓）、只有 name 的 manifest、单命令 `commands/hello.md`（frontmatter name/description ✓）、Usage 展示 `/hello` 的交互输出、Key Points 总结 4 条、When to Use 与 Extending 收尾。质量高、无冗余。唯一可挑剔处：Usage 示例输出 "Executed at: 2025-01-15 14:30:22 UTC" 中时间戳写法会让 agent 误以为要加时间戳（命令文件正文也确实要求 "Include the current timestamp"），而该命令实际无脚本支撑——小细节，但说明示例输出与 hello.md 的指令是自洽的，无问题。

### 5.6 examples/standard-plugin.md（587 行）— 标准插件示例

内容最完整的一个示例：目录树（7-35 行）含 commands/agents/skills/hooks/scripts 五类组件；plugin.json 元数据齐全（41-55 行）；lint.md/test.md 两个命令文件含 Process 步骤与 ${CLAUDE_PLUGIN_ROOT} 调用（81 行）；code-reviewer/test-generator 两个 agent 文件（130-222 行）frontmatter 规范且与技能互引（"Automatically loads `code-standards` skill"）；code-standards skill 带 references/style-guide.md（224-424 行）且文件在树中存在 ✓；hooks.json 用 PreToolUse(prompt 型)/Stop(command 型) 双类型（426-454 行）；validate-commit.sh 是完整的可运行 bash 脚本（457-504 行），`set -e`、JSON systemMessage 输出、exit code 契约均正确；Usage Examples 展示 /lint、/test 与 agent 自动选中场景（506-572 行）。**问题**：转义围栏 ×6（80/293/336/360/389/410 行，见第 6 节）；内层 skill name 含空格 + version 字段（228-230 行）；style-guide.md 引用不存在的 go/rust/ruby 文件（420-423 行）；prompt 型 hook 无文档支撑（435 行）。

### 5.7 examples/advanced-plugin.md（765 行）— 企业级插件示例

工程度最高的示例：目录树（7-99 行）体现多级组织（commands/ci、agents/orchestration、hooks/scripts/security 等）；plugin.json（105-143 行）同时使用 commands/agents/hooks/mcpServers 四个自定义路径字段，与 manifest-reference 的"补充而非替换"语义一致；.mcp.json（145-176 行）三个 MCP server 全部用 `${CLAUDE_PLUGIN_ROOT}` 指路且 env 支持 `${VAR:-default}` 语法（155 行）；build.md（178-223 行）展示了经 MCP server 触发 workflow 的调用形态；deployment-orchestrator agent（225-308 行）五阶段编排 + MCP/监控/通知三线集成；kubernetes-ops skill（310-627 行）内容量大且内部全部引用真实存在的 references/examples/scripts 文件（610-625 行）；hooks.json（629-697 行）四个事件、六个脚本全部在目录树中 ✓。**问题**：转义围栏 ×16（198/292/301/383/396/429/444/458/471/518/531/567/593/597/604/624 行）；JS 中误用 ${CLAUDE_PLUGIN_ROOT}（292-293/301 行）；内层 skill name 含空格 + version（314/316 行）；三个未被引用的组件文件（63/44/86 行）。库与 server 代码文件仅列名不给内容，属合理取舍（示例定位是结构而非实现）。

### 5.8 references/manifest-reference.md（552 行）— manifest 字段完整参考

字段级百科全书：core fields（name/version/description）→ metadata fields（author/homepage/repository/license/keywords）→ component path fields（commands/agents/hooks/mcpServers）→ path resolution → validation → 三个完整示例 → best practices。每个字段有类型、格式、示例、正反例。可圈可点处：name 校验正则（35 行）与 SCORING 不一致（见 10 节）；version 支持 pre-release 语法（54-57 行）合理；author 支持对象/字符串两种格式（87-107 行）；license 支持 SPDX 与复合表达式（164-187 行）；路径规则给出 4 条反例（348-351 行）含 Windows 反斜杠反例（351 行）体现跨平台意识；validation 节区分语法/字段/组件三层校验（373-393 行）。缺陷：无文档性错误，仅与 SCORING 的正则分歧。

### 5.9 references/component-patterns.md（567 行）— 组件组织模式参考

模式库：lifecycle（discovery 5 步 + activation 5 类，7-27 行，与 SKILL.md:328-344 自动发现机制互相印证）、commands 三模式（flat/categorized/hierarchical，29-131 行）、agents 三模式（133-184 行）、skills 五模式（186-289 行，含 "Skill with Rich Resources" 的 5 资源目录约定）、hooks 三模式（291-379 行）、scripts 三模式（381-446 行）、cross-component 三模式（448-535 行，shared resources/layered/plugin-within-plugin，后者的 custom paths manifest 与前文规则一致）。质量高，其中：
- 111 行嵌套命令需要 custom paths 的说明与 advanced-plugin 严格互证（见 4.1）；
- 342-348 行 hook 文件合并示例使用 `${file:./...}` 语法并诚实标注 "Claude Code doesn't support file references. Use build script to combine files"——示例自带免责说明，处理得体；
- 264-282 行 "Skill with Rich Resources" 与 standard/advanced 示例的资源结构对应。
无独立缺陷，是全 skill 最干净的参考文件。

---

## 6. 语法格式

### 6.1 Markdown 围栏

- **SKILL.md 自身格式良好**：全部 13 个代码块（JSON×5、markdown×3、bash×1、目录树×4）闭合正确，无悬空围栏。
- **examples 的转义围栏（主要语法缺陷）**：standard-plugin.md 6 处、advanced-plugin.md 16 处出现 `\`\`\`bash` 形式的转义反引号（如 standard-plugin.md:80、293、336、360、389、410；advanced-plugin.md:198、292、301、383、396、429、444、458、471、518、531、567、593、597、604、624）。成因：外层用 ```markdown 围栏包裹"内层文件的全文"，内层文件自身含代码块，作者把内层围栏转义。效果：渲染后 `\`\`\`bash` 作为字面文本（含反斜杠）显示，agent 阅读示例时看到的不是可复制的代码块标记；若 agent 不假思索复制，会把 `\`\`\` 连同反斜杠写进文件。**推荐修复**：外层改用四反引号围栏（````markdown ... ````），内层三反引号即可原样保留。这是 examples 类文件最标准的做法。

### 6.2 伪标题

SKILL.md 中 `### commands/`、`### agents/`、`### skills/`、`### hooks/`、`### my-plugin/`、`### plugin-name/`（113-117、137-141、163-174、197-202、398、405、422 等行）用三级标题充当目录路径标识。渲染无碍，但语义上标题层级被当作路径标签使用，且与 "**Example structure**:" 之间缺空行（113-114 行），属排版小瑕疵。更规范的做法是全部用代码块目录树（与 Common Patterns 三例一致）。

### 6.3 JSON / YAML 有效性

- SKILL.md 中 5 个 JSON 示例（49-53、63-78、87-95、205-216、229-241 行）逐字节校验均合法；转义引号、数组、嵌套对象无误。
- standard-plugin.md 的 plugin.json（41-55）、hooks.json（426-454）合法；advanced-plugin.md 的 plugin.json（105-143）、.mcp.json（145-176）、hooks.json（629-697）合法；manifest-reference 的全部 JSON 片段合法。
- 各示例的命令/agent 文件 YAML frontmatter（name/description/capabilities）语法合法；list 缩进一致。
- SCORING.yaml 本身 YAML 合法，`pattern: "^[a-z0-9]+(-[a-z0-9]+)*$"` 等正则字符串无转义问题。

### 6.4 文字质量

全文英文规范，无拼写错误、无病句、无中英混杂；标题层级一致（H1 仅一个 "# Plugin Structure for Claude Code"，其余 H2/H3/H4 正确）；列表编号连续（SKILL.md 三处 numbered list 均从 1 开始，无 tpl 系列那种首项编号丢失的问题）。检查 check.py 中 `import re` 未使用属 Python 层面小洁癖。

---

## 7. 规范合规（12-item 清单）

依据 SKILL-SPEC v1.0 第 5 节逐项核对：

| # | 检查项 | 结果 | 说明 |
|---|--------|:----:|------|
| 1 | name 小写+连字符、≤64、与目录匹配 | ✅ | `plugin-structure` = `287-plugin-structure` 去前缀 |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ⚠️ | 438 字符 ✓、WHEN/KEYWORDS 充分；**WHAT 隐式缺失** |
| 3 | description 无祈使/第一/第二人称 | ✅ | "This skill should be used when..." 第三人称被动 |
| 4 | description 无跨 skill 路由 | ✅ | |
| 5 | description 至少一个触发信号短语 | ❌ | "This skill should be used when the user requests" 不在 §2.4 五种短语之列（近似但不达标） |
| 6 | frontmatter 无禁字段 | ✅ | 仅 name + description |
| 7 | body ≤600 行 | ✅ | 459 行 |
| 8 | body 有 workflow/process 节 | ❌ | 无任何显式执行流程节（Auto-Discovery 描述的是平台机制） |
| 9 | body 有 output format 节 | ❌ | 无交付物/输出规格说明 |
| 10 | body 有 scope/limitations 节 | ❌ | Troubleshooting 不构成范围声明 |
| 11 | body 无跨 skill 文件引用 | ✅ | 仅 references/、examples/ 相对路径；README 按名称点名 |
| 12 | 目录 NNN-kebab-case | ✅ | |

**小结：12 项中 9 项通过、1 项部分通过（#2）、3 项不通过（#5/#8/#9/#10 中 4 项——即 #5 触发语 + 三必需节）**。若按"三必需节齐全"判总，本 skill 属"tool 型参考手册"的典型合规缺口——这正是 dossier 统计中占比最大的问题类型（缺 Scope ~68%、缺 Output ~56%）。单项全查的合规率 9/12 = 75%，但缺的是影响"技能可执行性"的核心三项，不是边角项。

---

## 8. 人机感

- **语气**: 全文中性技术参考语气，无 emoji、无网络用语、无填充词、无营销腔。与 083-085 senior 系列那种自我膨胀模板形成鲜明对比。
- **指令强度**: 恰到好处。critical rules 用粗体 + 编号明确"必须"，Troubleshooting 用条件句引导排查，没有全大写喊话（"STOP!"、"DO NOT" 在本 skill 中仅出现于 examples 的示例内容里，且属插件业务文案而非本 skill 说教，可接受）。
- **称呼**: 无第二人称说教（正文没有"you must"堆砌）；"**Why it matters**"（257-261 行）这类短解释句平实可读。
- **示例中的交互**: minimal/standard 示例的 `$ claude` → `/hello`、`> /lint` 输出块是给 agent 展示"用户视角"，符合技能主题（插件是给用户用的），不构成面向用户的越界。
- **欠缺的人机触点**: 由于没有 Scope 节，agent 面对"不确定该不该用本 skill"的场景（如用户只想发布插件、只想写单个 hook 脚本）没有明确的分流指引；由于没有 Workflow 节，agent 不知道何时该向用户确认（例如：插件名、组件范围）——交互协议缺失是人机感层面最实际的短板，但属于"结构缺口的衍生"，非语气问题。

**人机感单项评价：90/100。** 语气干净专业，无一处需要删改；短板全在结构层。

---

## 9. 可执行性

**总体判断：知识充分、流程缺席，agent 能产出正确产物但无法保证过程一致。**

### 可执行的部分

- **规则可机检**: 4 条 critical rules、路径三规则、命名约定都是"如果 X 则必须 Y"的确定性指令，agent 可逐条对照执行；SCORING 也将其中大部分转化成了检查项（PROC-01/02/05/06、NEG-01）。
- **示例可复制**: 三个 examples 提供了从最小到企业级的完整落地文件，agent 按需求粒度挑选即可。
- **排障清单可操作**: 431-455 行的四组问答给出"检查什么→确认什么"的具体动作。

### 不可执行/含糊的部分

- **无主流程**: 没有 Step 1..N 的创建流程。agent 拿到 "create a plugin" 请求后，行为完全依赖其对 body 章节顺序的自行解读。不同 agent 可能产出"先写 manifest"或"先建目录"的不同次序——SCORING 未考核顺序，所以这不影响评分，但影响产出一致性。
- **无模式选择规则**: Common Patterns（393-429）给了三档模板（minimal/full/skills-focused），但没有"何时选哪档"的决策规则（如：单命令→minimal；多组件+团队→full；纯知识→skills-focused）。agent 只能猜用户意图，或一律产出 full——与 PROC-03 "只建实际用到的组件目录"直接冲突。
- **无输出规格**: 没有定义交付物集合（目录树+文件内容+说明文字）。OUT-02/OUT-03 的 llm judge 事实上代偿了这部分（问"结构是否完整一致""是否解释了自动发现机制"），等于评分标准替技能内容补了缺。
- **无范围边界**: 见 8 节。

**可执行性单项评价：66/100。** 内容本身可靠（不会教错东西），但缺少把内容变成"过程"的组织层。

---

## 10. SCORING 交叉参考

SCORING.yaml + check.py 与技能内容做交叉核对，发现 5 项问题：

1. **PROC-01 正则与 manifest-reference 冲突（SCORING.yaml:32 vs manifest-reference.md:35）**。SCORING 的 `^[a-z0-9]+(-[a-z0-9]+)*$` 允许插件名以数字开头（如 `123abc` 可通过）；manifest-reference 的 `/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/` 要求字母开头，且 SKILL.md:56-59 也举例 "No spaces or special characters" 未明确首位约束。评分标准与技能自述的校验规则不一致——被测 agent 按 reference 生成 `1plugin` 会被判错，按 SCORING 生成 `1plugin` 会得到"该通过却没通过"的分歧。**必须统一**（建议以 reference 的字母开头为准并同步两处）。

2. **PROC-08 与本 skill 的 minimal pattern 冲突（SCORING.yaml:87-88）**。`file_exists skills/*/SKILL.md` 要求产物中必须存在 skills/ 下的 SKILL.md。但 SKILL.md:395-402 与 examples/minimal-plugin.md 明确定义 minimal 模式只有 commands/ + plugin.json、无 skills/；且 PROC-03 要求"只创建实际用到的组件目录"——一个合法的最小插件请求天然无法通过 PROC-08。**评分标准反向惩罚了技能自身传授的最小路径**。这是本 skill 测评设计中最实质的缺陷。建议：改为 llm judge，或按插件类型条件化（plugin.json 未声明 skills 自定义路径时不要求）。

3. **NEG-01 的误报面（SCORING.yaml:121-122 + check.py:57-59）**。`tool_log_not_contains("claude-plugin/(commands|agents|skills|hooks)")` 扫描整个 tool log 的 JSON 序列化文本（含文件内容与 bash 命令）。以下合法行为会误触：agent 在插件 README 中按 Best Practices 写目录说明、agent 先 mkdir `.claude-plugin/commands` 再按排障指引删除、Write 路径恰好为 `./plugin/.claude-plugin/commands/` 的中间态。它与 PROC-02（检查最终文件系统）语义重叠但检查介质不同（log vs fs），存在"中间态违规、终态合规"仍被判负的不一致。建议改为检查最终工作区文件系统，或限定匹配 Write/Edit 工具的最终路径。

4. **SCOPE-02 假定任务是"创建"型（SCORING.yaml:17-21）**。description 明列 "understand plugin structure"、"organize plugin components" 等非创建型触发场景，但 SCOPE-02 要求 `.claude-plugin/plugin.json` 真实存在，纯讲解类请求必然全组低分。测评 prompt 设计时应只使用创建/搭建类任务，或为非创建任务设独立评分路径。属测评使用说明缺口，非评分逻辑缺陷。

5. **CF-02 判定标准模糊（SCORING.yaml:138-141）**。"wrong file names — auto-discovery fails silently" 未定义何为 "wrong"（大小写？扩展名？kebab 违规？），而 PROC-04 的 kebab-case 检查是 llm judge 而非 cap_to_0——两条标准对"命名错误"的处置力度不一致（一次命名违规即归零 vs 仅扣单项）。建议 CF-02 明确指向"文件扩展名错误或目录名非组件标准名"并举例。

**正面项**：15 项 criterion 与 6 个 script judge 的映射关系在 SCORING 与 check.py 之间逐字一致；PROC-05/06/07 的 llm 问题文本把技能规则（${CLAUDE_PLUGIN_ROOT}、`./` 前缀、frontmatter 结构）完整嵌入，judge 可对照技能正文裁决；3 条 critical_failures 均为真实致命场景。

---

## 11. 已知问题（跳过）

按任务规则，本节不做独立已知问题清单——所有发现的问题已在前述各节完整分析，并将在第 13 节给出带定位与工作量的修复建议。

---

## 12. 综合评分（8 维 → /100）

| 维度 | 得分 | 依据摘要 |
|------|:----:|----------|
| 1. 领域内容完整性与准确性 | 92 | 覆盖 Claude Code 插件结构全貌，事实基本正确；仅 JS 中 ${CLAUDE_PLUGIN_ROOT} 一处运行时错误示例 |
| 2. 逻辑一致性 | 84 | 全局规则五处互证、无核心矛盾；存在 restart 措辞、PROC-01 正则、内层 skill 命名、示例悬空引用等 6 处局部问题 |
| 3. 规范合规（12-item） | 58 | 9/12 通过；缺三必需节 + 触发语偏差 + WHAT 隐式 |
| 4. 结构与渐进披露 | 88 | 三层次披露是本 skill 最佳设计；body 略超 tool 目标行数 |
| 5. 人机感 | 90 | 干净中性，无一处需删改；交互协议因结构缺失而不完整 |
| 6. 可执行性 | 66 | 规则/示例/排障可执行，但无主流程、无模式选择规则、无输出规格 |
| 7. 参考文件与示例质量 | 86 | 两 references 质量上乘；三示例内部一致性强；转义围栏、悬空引用、未引用组件拖分 |
| 8. SCORING/check.py 设计一致性 | 72 | 映射逐字一致；PROC-08 惩罚 minimal 模式、PROC-01 正则分歧、NEG-01 误报面为实质缺陷 |

**加权计算**（合规 1.5、可执行 1.5、逻辑 1.0、内容 1.0、参考 1.0、评分 0.9、结构 0.8、人机感 0.8，总权重 8.5）：
(92×1.0 + 84×1.0 + 58×1.5 + 88×0.8 + 90×0.8 + 66×1.5 + 86×1.0 + 72×0.9) / 8.5
= (92 + 84 + 87 + 70.4 + 72 + 99 + 86 + 64.8) / 8.5
= 655.2 / 8.5
= **77.1 → 77 / 100**

**评级：🟡 可用但存在结构性缺口。** 若完成第 13 节的 🟠 项（补三节）与 🟡 项主体（description、SCORING 修复），预期可达 88-92 / 🟢。对照记忆档案（skill-dossier，2026-08-05）：287 在 281-300 批次摘要中被记为 "目录结构到最佳实践一致"，落于该批 🟡（缺节）组——本报告与档案评级一致，但档案未捕获三必需节缺失与 SCORING 内部矛盾这两类更深问题，本报告作为该条目的展开与修正。

---

## 13. 修复建议

按严重度分级，均含文件定位与工作量估计（🟢 <30 分钟，🟡 0.5-2 小时，🟠 2-4 小时）。

### 🔴 无

本 skill 无内容性致命缺陷（无截断、无错误分类法、无空壳），无需重写。

### 🟠 结构性（2 项）

1. **补 Workflow/Process 节**（SKILL.md，建议插在 "## Plugin Manifest" 之前或 "## Overview" 之后）
   - 内容：创建插件的 6 步主流程——① 确认插件名与组件范围（minimal/full/skills-focused 三档选择规则：何时选哪档）；② 建立目录树（按 Critical Rules 只建实际需要的目录）；③ 写 `.claude-plugin/plugin.json`（必需字段 + 按需元数据 + 自定义路径）；④ 逐个创建组件文件（commands/agents 带 frontmatter，skills 带 SKILL.md，hooks 用 hooks.json wrapper，MCP 用 .mcp.json）；⑤ 全部路径用 `${CLAUDE_PLUGIN_ROOT}` 并校验 `./` 前缀；⑥ 按 Troubleshooting 四组问答自检。每步给出输入/动作/输出。
   - 工作量：2-3 小时。注意行数：459 + 新增 ~60 行会逼近 600，需同步执行第 3 项瘦身。

2. **补 Output Format 与 Scope/Limitations 节**（SKILL.md，可合成一节 "## Output" 与一节 "## Scope and Limitations" 置于 Best Practices 之前）
   - Output：交付物 = 完整目录树（代码块）+ 每个文件的内容 + 对自动发现机制与生效时机的说明（覆盖 OUT-02/OUT-03 的检查口径）。
   - Scope：声明本 skill 不做的事——插件打包发布（marketplace）、hook 脚本具体逻辑设计、MCP server 内部实现、插件依赖管理；"用户只问架构原理时"与"用户只要发布指导时"应不触发本 skill。
   - 工作量：1.5-2 小时。

### 🟡 内容与一致性（8 项）

3. **修复 description 触发语与 WHAT**（SKILL.md:3）
   - 开头改为 "Provides guidance on Claude Code plugin directory structure, plugin.json manifest configuration, and component organization. Use when the user asks to..."，WHEN 部分照旧。438 → ~500 字符，仍 ≤1024。
   - 工作量：30 分钟。

4. **统一 "No restart required" 措辞**（SKILL.md:342）
   - 改为 "Restart not required for installation; changes take effect when Claude Code starts the next session." 或直接删掉 "No restart required" 短语。SCORING.yaml OUT-03 问题文本同步（SCORING.yaml:112）。
   - 工作量：15 分钟。

5. **修正模板示例中的自身 name 复用与 version 字段**（SKILL.md:120-127、176-185）
   - commands 模板 name 改为泛化示例（如 `my-command` 或 `example-command`）；SKILL.md format 模板删 `version: 1.0.0` 行（§1.3 禁字段），name 用 `example-skill-name`。
   - 工作量：20 分钟。

6. **examples 转义围栏改四反引号外层**（standard-plugin.md:80、293、336、360、389、410；advanced-plugin.md:198、292、301、383、396、429、444、458、471、518、531、567、593、597、604、624）
   - 外层 ```markdown 与 ```javascript/bash 全部改为 ````markdown/```` 形式，内层三反引号原样保留，删除全部反斜杠。
   - 工作量：1 小时（机械替换，但需逐块验证渲染）。

7. **修正示例内层 skill 的 frontmatter**（standard-plugin.md:228-230；advanced-plugin.md:314-316）
   - `name: Code Standards` → `name: code-standards`；`name: Kubernetes Operations` → `name: kubernetes-ops`；删除 `version` 字段（或改为非 frontmatter 的正文标注）。
   - 工作量：15 分钟。

8. **修正 JS 中的 ${CLAUDE_PLUGIN_ROOT} 用法**（advanced-plugin.md:292-293、301）
   - `require('${CLAUDE_PLUGIN_ROOT}/lib/...')` → `require(path.join(process.env.CLAUDE_PLUGIN_ROOT, 'lib/integrations/datadog'))`，并在示例旁加一行注释说明 shell 展开 vs process.env 的区别；建议 SKILL.md:257-271 补一句"该变量由 shell 展开，脚本语言内需经 process.env 读取"。
   - 工作量：30 分钟。

9. **消除 advanced-plugin 的未引用组件**（advanced-plugin.md:63、44、86）
   - 删除 `verify-tests.sh`、`health-check.sh`、`pagerduty.js` 或让 hooks.json/agent 正文引用它们（与 SKILL.md:40、PROC-03 对齐）。
   - 工作量：15 分钟。

10. **清理 standard-plugin 的 style-guide 悬空引用**（standard-plugin.md:420-423）
    - 将 go/rust/ruby 三行标注为"外部文档，非本插件内容"，或删除该小节。
    - 工作量：10 分钟。

### 🟢 打磨（4 项）

11. **统一 SCORING 与 reference 的 name 正则**（SCORING.yaml:32 / manifest-reference.md:35）——建议按 `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` 统一（字母开头更接近 Claude Code 实际校验），check.py:42 同步。工作量：15 分钟。
12. **PROC-08 条件化或转 llm judge**（SCORING.yaml:87-88、check.py:48-50）——按 plugin.json 是否声明 skills 相关自定义路径（或产品含 skill 组件）决定是否要求 `skills/*/SKILL.md`；至少应在 criterion 描述中注明"适用于含技能组件的插件"。工作量：45 分钟。
13. **NEG-01 收窄匹配面**（SCORING.yaml:121-122、check.py:57-59）——改为检查工作区文件系统（复用 PROC-02 语义）或限定 tool=Write/Edit 且路径匹配。工作量：30 分钟。
14. **SKILL.md 瘦身与伪标题清理**（SKILL.md:113-117 等）——`### commands/` 等伪标题改为代码块目录树；Best Practices/Troubleshooting 中与 references 重复的内容（如命名约定 296-326 与 component-patterns 命名节）压缩为要点+指针，为新增三节腾行数。工作量：1.5 小时。

**建议实施顺序**：3 → 4 → 5 → 7 → 8 → 9 → 10（零风险内容修正）→ 6（格式）→ 11-13（测评一致性）→ 1-2（结构补全）→ 14（瘦身收尾）。

---

## 附录 A — 12-item 合规清单速查

```
[x] name: lowercase + hyphens, ≤64 chars, matches directory        (plugin-structure)
[~] description: third-person, WHAT+WHEN+KEYWORDS, ≤1024 chars     (438 chars, WHAT 隐式)
[x] description: no imperative/first/second-person openings
[x] description: no cross-skill routing embedded
[ ] description: at least one trigger signal phrase                 ("This skill should be used when..." 非 §2.4 短语)
[x] frontmatter: no keys outside the allowed list
[x] body: ≤600 lines                                                (459)
[ ] body: has workflow/process section
[ ] body: has output format section
[ ] body: has scope/limitations section
[x] body: no cross-skill file references (../other-skill/)
[x] directory: NNN-kebab-case, no spaces or uppercase
```

## 附录 B — 8 维评分表

| 维度 | 权重 | 得分 | 加权 |
|------|:----:|:----:|:----:|
| 领域内容完整性与准确性 | 1.0 | 92 | 92.0 |
| 逻辑一致性 | 1.0 | 84 | 84.0 |
| 规范合规（12-item） | 1.5 | 58 | 87.0 |
| 结构与渐进披露 | 0.8 | 88 | 70.4 |
| 人机感 | 0.8 | 90 | 72.0 |
| 可执行性 | 1.5 | 66 | 99.0 |
| 参考文件与示例质量 | 1.0 | 86 | 86.0 |
| SCORING/check.py 设计一致性 | 0.9 | 72 | 64.8 |
| **合计** | **8.5** | — | **655.2 → 77/100** |

## 附录 C — 关键行号索引

- SKILL.md:3 description；:38-41 critical rules；:120-127/176-185 模板 name/version 问题；:218 hooks 事件；:339-342 生效时机；:393-429 三模式
- SCORING.yaml:24-32 PROC-01；:83-88 PROC-08；:116-122 NEG-01；:133-146 CF-01/02/03
- check.py:39-43 PROC-01；:48-50 PROC-08；:57-59 NEG-01
- examples/standard-plugin.md:80 等 转义围栏；:228-230 内层 skill frontmatter；:420-423 悬空引用；:435 prompt 型 hook
- examples/advanced-plugin.md:44/63/86 未引用组件；:292-293/301 JS 路径；:314-316 内层 frontmatter
- references/manifest-reference.md:35 name 正则；:332-351 路径规则
- references/component-patterns.md:111 嵌套命令说明；:342-348 hook 文件引用免责
