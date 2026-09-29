# REVIEW: 062-plugin-settings

**审查日期**: 2026-08-06
**Skill 类型**: tool — `.claude/plugin-name.local.md` 插件配置模式（YAML frontmatter + markdown body），含读取/解析/创建/安全全链路
**Body 行数**: 487 行
**参考文件数**: references/5, examples/3, scripts/2, assets/0, 其他/0
**总文件数**: 13
**旧 stub 评分**: 🟢 B (50/100) — 本次深度审查后修订（见 §11、§12）

---

## 1. 目录全量清单

```
062-plugin-settings/
├── SKILL.md (487 行)
├── SCORING.yaml (178 行)
├── check.py (83 行)
├── examples/ (3 个文件，共 322 行)
│   ├── create-settings-command.md (98 行)        ← 从未被 SKILL.md 引用
│   ├── example-settings.md (159 行)              ← 从未被 SKILL.md 引用
│   └── read-settings-hook.sh (65 行)             ← SKILL.md L99 唯一引用的 examples 文件
├── references/ (5 个文件，共 1,009 行)
│   ├── additional-resources.md (22 行)           ← 二级索引（藏了另两个大文件）
│   ├── implementation-workflow.md (12 行)
│   ├── parsing-techniques.md (549 行)            ← 全库最大参考文件，SKILL.md 未直接索引
│   ├── quick-reference.md (31 行)
│   └── real-world-examples.md (395 行)           ← SKILL.md 未直接索引
└── scripts/ (2 个文件，共 160 行)                ← 从未被 SKILL.md 引用
    ├── parse-frontmatter.sh (59 行)
    └── validate-settings.sh (101 行)
```

- 全目录 13 个文件，总计约 2,239 行
- 该 skill 属"完整教学型工具参考"：SKILL.md 自身 487 行已承载全部核心模式（无需打开参考文件即可执行），references/ 提供深度补充，scripts/ 提供校验工具 —— 模块化结构本身合理
- 但存在一个结构性问题：**references/ 中体量最大的两个文件（parsing-techniques.md 549 行、real-world-examples.md 395 行）以及全部 scripts/、2 个 examples/ 文件无法从 SKILL.md 直达**（详见 §4.3、§5.1）

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `plugin-settings`，全小写 + 连字符 ✓
- 长度: 14 字符，远低于 64 字符限制 ✓
- 匹配目录名 `062-plugin-settings` ✓
- 语义: 描述性命名，与内容一致 ✓

### 2.2 description

原文（L3）:
> "This skill should be used when the user asks about "plugin settings", "store plugin configuration", "user-configurable plugin", ".local.md files", "plugin state files", "read YAML frontmatter", "per-project plugin settings", or wants to make plugin behavior configurable. Documents the .claude/plugin-name.local.md pattern for storing plugin-specific configuration with YAML frontmatter and markdown content."

逐句分析:

**第 1 句** (WHEN/触发): "This skill should be used when the user asks about X, Y, Z..."
- 内嵌 7 个带引号关键词 + 1 个动词短语（"make plugin behavior configurable"）— 关键词覆盖面极好，几乎穷尽该领域用户可能的说法 ✓
- 但开头结构是 "This skill should be used when..." — 这是 §2.2 模板（"<what it does, third-person>. Use when the user <triggers>."）之外的被动结构。stub 已认定违反 §2.3；严格字面看，该句无第一/第二人称、无祈使句（"should be used" 是第三人称被动），§2.3 的明文禁令（imperative / first-person / second-person）并未被逐字触发，但 §2.4 的判定更关键（见下）
- 触发场景清单具体、可操作，均为该领域真实用户说法 ✓

**第 2 句** (WHAT): "Documents the .claude/plugin-name.local.md pattern for storing plugin-specific configuration with YAML frontmatter and markdown content."
- 定义了 WHAT：文档化 `.claude/plugin-name.local.md` 模式，含 YAML frontmatter + markdown body 两个关键结构词 ✓
- 第三人称 ✓

**§2.4 触发信号检查（关键问题）**:
SKILL-SPEC §2.4 列出的五种标准触发短语 —— "Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..." —— 本 description **一个都没有出现**。最接近的是 "should be used when the user asks about"，但缺少标准短语必需的 "Use when" 引导词。这是 description 规范性的实质缺口。

**总体评价**: 内容层面（WHAT + WHEN + 9 个关键词）完整且优秀，是本语料库中关键词密度最高的 description 之一；结构层面不合规 —— 无 §2.4 标准触发短语，且与 §2.2 模板结构不符（stub 判定成立，方向正确，详见 §11.2 的边界讨论）。

### 2.3 allowed-tools
- frontmatter 中**没有** `allowed-tools` 字段
- SKILL-SPEC §1.2 中该字段为可选，不构成违规
- 但该 skill 的执行需要: Read（读取 .local.md）、Write（创建配置文件）、Bash（运行解析/校验脚本）、Glob（定位 .local.md 文件）。缺字段虽不违规，但建议补充（O-1）

### 2.4 其他 frontmatter 字段
- 无 `argument-hint`、`user-invocable` 等其他可选字段 — 该 skill 无参数输入，可接受 ✓
- 无任何禁止字段 ✓

### 2.5 Frontmatter 语法
- YAML 分隔符 `---` 配对正确（L1/L4）✓
- description 中的内层引号使用了 `\"` 转义（字节级验证: `\"plugin settings\"`），YAML 解析合法，description 不会被截断 ✓
- 无缩进问题、无其他转义错误 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Plugin Settings Pattern for Claude Code Plugins (L6)   — H1 标题
## Overview (L9-18)                                      — 定位 + 5 个 Key features
## File Structure (L21-59)                               — 基础模板 + 状态文件示例
## Reading Configuration Files (L62-136)                 — hooks/commands/agents 三种读取方式
## Parsing Techniques (L139-174)                         — frontmatter/字段/body 提取
## Common Patterns (L177-274)                            — 3 个模式（临时 hook/agent 状态/配置驱动）
## Creating Configuration Files (L277-317)               — 命令创建 + 模板生成
## Best Practices (L320-391)                             — 命名/ gitignore / 默认值 / 校验 / 重启
## Security Considerations (L394-430)                    — 输入消毒 / 路径穿越 / 权限
## Real-World Examples (L434-482)                        — multi-agent-swarm + ralph-wiggum
## Reference Files (L484-488)                            — 仅 3 个文件索引
```

### 3.2 必需章节检查

#### Workflow/Process 节
- **body 内无显式 Workflow/Process 节** ⚠️
- 过程性内容由三个功能区块隐含承担: "Reading Configuration Files"（读侧流程）、"Creating Configuration Files"（写侧流程）、"Common Patterns"（三类应用场景）。对 tool 型参考 skill 而言功能上够用，但形式上无统一步骤节
- references/implementation-workflow.md 提供了 7 步实现流程（schema → template → gitignore → parsing → quick exit → docs → restart），与 SCORING.yaml PROC-07 严格对应 — 实现流程在参考文件里，不在 body 里

#### Output Format 节
- **无显式 Output Format 节** ⚠️
- "File Structure → Basic Template"（L25-41）实质上定义了交付物格式（YAML frontmatter 各类型值 + markdown body），可视为输出格式的弱化版 — 因为该 skill 的"输出"就是 `.local.md` 文件本身，格式定义即输出定义
- 但缺少对整体交付物组合（配置文件 + 解析代码 + README 文档）的声明（见 I-5）

#### Scope/Limitations 节
- **不存在** ❌ — 最直接的规范缺口（SKILL-SPEC §3.1 规则 9）
- "Best Practices → File Naming" 的 DON'T 列表（L329-333）只覆盖命名反模式，不含"何时不使用本 skill / 本模式不适用于什么场景"
- 全库没有任何"本 skill 不做什么"声明（如: 不用于全局/共享配置、不用于密钥存储、不用于 settings.json/hooks.json 管理）

### 3.3 内容委托分析

- Body 487 行承载全部核心模式，执行逻辑**不依赖**参考文件即可运转 — 委托比例低（约 5%），这是优点（可独立执行，见 §9.1）
- 参考文件是"深度补充"而非"必要依赖": parsing-techniques.md（549 行）是 SKILL.md Parsing Techniques 节的扩展版；real-world-examples.md 是 Real-World Examples 节的完整实现
- **结构缺陷**: "## Reference Files"（L484-488）只列出 3 个文件（additional-resources.md / implementation-workflow.md / quick-reference.md），而体量最大的 parsing-techniques.md 与 real-world-examples.md 藏在 additional-resources.md（22 行）的二级索引里；scripts/ 与 2 个 examples/ 文件完全不可达（见 §4.3、§5.2）

### 3.4 节编号/标题层级
- 标题层级: # → ## → ###，无跳级 ✓
- Pattern 1/2/3 编号连续 ✓
- 无孤立标题 ✓

### 3.5 Body 长度合规
- 实际 487 行 ≤ 600 行硬限制 ✓
- pattern=tool 目标 ~300 行 — 487 行超出目标约 62%，但该 skill 的核心价值就是大量可复制的 bash 代码片段，行数偏高是内容形态使然，且未触上限，判定合规但偏重

### 3.6 结构亮点（值得肯定）
- **Security Considerations 独立成章（L394-430）**: 输入消毒（SAFE_VALUE 转义）、路径穿越拦截（`..` 检查）、权限（chmod 600 / 不入 git / 不共享）三件套齐全，与本语料库大部分 tool 型 skill 相比是明显加分项，与 QA-02 严格对应
- **Best Practices 的 DO/DON'T 双列表（L320-333）**: 具体反模式带原因，符合 SKILL-SPEC §3.4"anti-patterns over generic advice"
- **示例代码全部可直接复制**: 每个模式都配完整 bash 片段，无"此处省略"式占位
- **gitignore 指引（L334-343）**: 给出精确的 `.claude/*.local.md` 与 `.claude/*.local.json` 模式，与 OUT-03 直接对应

---

## 4. 逻辑一致性深度审查

### 4.1 Pattern 1 引号剥离缺失 — 与自身 hook 脚本和参考文件不一致（本 skill 最实质的逻辑缺陷）

SKILL.md "Common Patterns → Pattern 1"（L193-194）:
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi
```

对比同一 skill 的其他材料:
- examples/read-settings-hook.sh L20-21: `sed 's/^"\(.*\)"$/\1/'` 剥离引号 ✓
- references/real-world-examples.md L65-69: 同样带引号剥离 ✓
- references/parsing-techniques.md L313-317: 明确说明 `field2: "value"` 与 `field2: value` 等价，并给出 "Handle both" 的引号剥离写法

**问题**: YAML 允许带引号布尔值（`enabled: "true"`）。Pattern 1 照抄的 agent 遇到带引号文件时，ENABLED 值为 `"true"`（含引号），`[[ "$ENABLED" != "true" ]]` 判定成立 → **已启用的插件被当作禁用**。而 SKILL.md 自己的参考材料（及其自带的 example hook）都做了引号剥离。三份同源材料行为不一致，SKILL.md 主体反而是最薄弱的一份。

### 4.2 Restart 要求与运行时读取机制的张力（6 处出现）

- "restart" 在 SKILL.md 中出现 6 次: L291（"Remind user to restart Claude Code for hooks to recognize changes"）、L316、L376（"**Important:** Configuration changes require Claude Code restart"）、L383-389（"Changing Settings" 4 步）、L391（"Hooks cannot be hot-swapped within a session"）、以及 Overview 之外的多处
- **张力所在**: 该 skill 自己演示的机制是 hook 每次触发时重新读取 `.local.md`（L74-97 的脚本、examples/read-settings-hook.sh 均如此）—— 数据文件修改后，下次 hook 触发即生效，**无需重启**。重启要求对"hook 定义变更"（settings.json / hooks.json 的修改）成立，对"hook 脚本运行时读取的数据文件"不成立
- 即: 技能一边演示无需重启的运行时读取，一边 6 次强制"必须重启"。该声明被评估侧采纳（SCORING PROC-06 问题: "changes require a Claude Code restart because hooks cannot be hot-swapped"），所以本 review 不要求删除，只要求收敛与精确化（I-4）

### 4.3 Reference Files 索引断层

- "## Reference Files"（L484-488）只索引 3 个小文件; parsing-techniques.md（549 行，SKILL.md 自己的 Parsing Techniques 节的完整版）与 real-world-examples.md（395 行）经 additional-resources.md 二级跳转才可达
- scripts/parse-frontmatter.sh、scripts/validate-settings.sh、examples/create-settings-command.md、examples/example-settings.md 在 SKILL.md 中**零提及**
- 后果链: SKILL.md 是 agent 的执行入口，索引断层意味着四个有用文件（含 QA-01 依赖的两个脚本）只在 agent 主动探索目录时才被发现（§9.1、§10.4）

### 4.4 转义反引号围栏 — Template Generation 示例渲染破损（dossier 与 stub 均已点名）

- 位置: SKILL.md L304（`\`\`\`markdown`）与 L314（`\`\`\``）
- 字节级验证: 两行内容是**反斜杠 + 反引号**（`\`\`\``），而非真实反引号围栏。markdown 渲染时以字面文本 `\`\`\`markdown` 呈现，内层"模板文件"代码块不成立；外层围栏（L298 打开、L317 闭合）虽然闭合，但内部展示的是转义字面量
- 结果: "Template Generation"（L294-317）是整个 SKILL.md 中唯一的破损代码块 —— 而这恰是 QA-04（"向用户提供配置模板"）依赖的交付物模板
- 注意: 该节意图是"在插件文档里演示嵌套 markdown 代码块"，作者用 `\`\`\`` 想避免与外围栏冲突，但 markdown 没有"转义反引号"语法，正确做法是真实反引号或换用不同长度的围栏

### 4.5 sed 解析边界与 CF-02 的关系

- SKILL.md 主推的 sed/grep 解析（L139-165）对"扁平的、单行标量值"成立；对以下情况失效: 多行值、值中含 `:` 后带引号内容、注释行、嵌套结构。SKILL.md 未声明该边界，但 references/parsing-techniques.md L453-484 提供了 yq 替代方案并明确 "Use sed/grep for simple fields, yq for complex structures"
- 更隐蔽的问题: `grep '^field_name:'` + `sed 's/field_name: *//'` 对**值中含冒号**的字段（如 `completion_promise: "All tests passing and build successful"` —— 见 SKILL.md L469）—— sed 只删第一个前缀匹配，值本身保留，正确；但若字段名是另一字段名的前缀（如 `enabled` 与 `enabled_something`），`grep '^enabled:'` 不会误匹配 `enabled_something:`（因要求紧跟冒号）— 边界设计总体安全
- 引号处理不一致是唯一真实风险点（§4.1），与 CF-02（"fail on quoted values" → cap_to_0）的判定标准直接相关: **照抄 SKILL.md Pattern 1 的 agent 会产出"对带引号值解析失败"的实现 —— 技能亲手提供了触发 CF-02 的路径**（详见 §10.2）

### 4.6 不可验证的行号引用

- SKILL.md L457 "Checks if file exists (lines 15-18: quick exit if not)"、L477 "Checks if file exists (lines 15-18: quick exit if not active)" — 引用的 `agent-stop-notification.sh` / `stop-hook.sh` 位于外部插件（multi-agent-swarm、ralph-wiggum）而非本 skill 目录，行号无从核对；且两处**相同行号**（15-18）却指向两个不同脚本，暗示复制痕迹
- 引用的脚本在 references/real-world-examples.md 中确实存在（L44-86、L156-219），本 skill 内无副本 — 行号精确性不可验证

### 4.7 其他一致性核对
- 文件命名规则（`.claude/plugin-name.local.md`）在 Overview、Best Practices、全部示例间完全一致 ✓
- 三个 Common Patterns 与 QA-03 对应关系清晰 ✓
- 安全三件套（消毒/穿越/权限）与 QA-02 对应关系清晰 ✓
- gitignore 模式（`.claude/*.local.md` + `.claude/*.local.json`）在各文件间一致 ✓
- "enabled 快速退出" 模式（quick exit）在 SKILL.md、examples、real-world-examples、quick-reference 四处一致 ✓
- SCORING.yaml PROC-07 的 7 步流程与 references/implementation-workflow.md 的 7 步**逐字对应**（schema → template → gitignore → parsing → quick exit → docs → restart）✓ 这是评估-内容映射最精确的一处

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

SKILL.md 直接引用的文件:

| 引用路径 | SKILL.md 行号 | 是否存在 | 文件行数 | 内容匹配度 |
|----------|:------------:|:--------:|:--------:|:---------:|
| examples/read-settings-hook.sh | L99 | ✅ | 65 | ✅ 完整可运行 |
| references/additional-resources.md | L486 | ✅ | 22 | ✅ 二级索引 |
| references/implementation-workflow.md | L487 | ✅ | 12 | ✅ 7 步流程 |
| references/quick-reference.md | L488 | ✅ | 31 | ✅ 速查卡 |

**存在但 SKILL.md 未引用（引用断层）**:

| 文件 | 行数 | 可达性 | 后果 |
|------|:----:|:------:|------|
| references/parsing-techniques.md | 549 | 经 additional-resources.md 二级跳转 | 解析技术全集对 agent 不可直达 |
| references/real-world-examples.md | 395 | 经 additional-resources.md 二级跳转 | 生产实现细节不可直达 |
| scripts/parse-frontmatter.sh | 59 | 仅 additional-resources.md 提及 | QA-01 依赖脚本不可发现 |
| scripts/validate-settings.sh | 101 | 仅 additional-resources.md 提及 | QA-01 依赖脚本不可发现 |
| examples/create-settings-command.md | 98 | 无任何引用 | 死资源 |
| examples/example-settings.md | 159 | 无任何引用 | 死资源（QA-04 模板的最全版本） |

无悬空引用（所有被引用文件均存在）✓，但存在**6 个不可达文件**（SKILL.md 视角）。

### 5.2 不可见资源审计
- 全目录 13 个文件中，6 个无法从 SKILL.md 直达（见上表）— 对"打开即用"的评测场景构成真实影响
- 无 assets/ 目录、无隐藏文件 ✓

### 5.3 Reference 文件全文审查

**parsing-techniques.md (549 行) — 全库最佳参考文件之一**:
- 内容: frontmatter 提取（sed 范围匹配原理逐行解释）、字段提取（string/boolean/numeric/list 四类 + jq 列表处理）、body 提取（awk 计数器法 + `---` 在 body 中出现的边界处理）、原子更新（tmp + mv 模式，含单字段/多字段）、验证技术（文件存在/围栏计数/枚举校验/数值范围）、边缘情况（引号、`---` in body、空值、特殊字符）、性能优化（缓存解析、惰性加载）、调试（set -x、解析值打印）、yq 替代方案（附优缺点与建议）、549 行完整示例
- 亮点: "Handle both" 引号剥离（L313-317）; 原子更新的 tmp.$$ 模式（L194-209）; "--- in Markdown Body" 边界处理（L319-336）; 完整示例（L488-547）含默认值 + 校验 + 快速退出，是全库最可复制的 bash 参考
- 问题: 无。与其说问题，不如说 SKILL.md 的 Parsing Techniques 节是它的缩略版 —— 这正是索引断层（§4.3）的遗憾所在

**real-world-examples.md (395 行)**:
- 内容: multi-agent-swarm（agent-stop-notification.sh 完整实现 L51-86 + 创建 L100-116 + 更新 L122-127）与 ralph-wiggum（stop-hook.sh 完整实现 L157-219 + 创建 L233-252）两插件深度剖析; 模式对比表（L256-264）; 5 条 Best Practices（快速退出/启用标志/原子更新/引号处理/错误处理）; 反模式清单（硬编码路径、未引用变量、非原子更新、无默认值、忽略边缘情况）
- 亮点: 反模式清单每个都附 BAD/GOOD 对照（L331-384），符合 §3.4; 行号标注与脚本实际内容一致（本文件内部自洽）
- 问题: 与 SKILL.md 的 Real-World Examples 节（L434-482）内容重叠约 60%（同两个插件、同文件结构）— SKILL.md 版本是压缩版，重复可接受但不经济; "### 5.5 跨 Skill 引用检查"无跨 skill 路径 ✓

**additional-resources.md (22 行)**: 纯索引文件，指向 parsing-techniques/real-world-examples/三个 examples/两个 scripts。文件本身没问题，问题是它承担了 SKILL.md Reference Files 节应承担的职责（§4.3）

**implementation-workflow.md (12 行)**: 7 步实现流程，与 PROC-07 逐字对应，干净 ✓

**quick-reference.md (31 行)**: 文件位置、frontmatter/body 解析、快速退出三块速查，干净 ✓。一处格式小瑕: "### File Location" 后直接接代码块，无过渡文字

### 5.4 Scripts 文件全文审查

**parse-frontmatter.sh (59 行)**: 参数校验、文件存在检查、frontmatter 提取、字段提取（含双引号与单引号剥离）— 功能完整可运行 ✓
- 小问题: `grep "^${FIELD}:"` 将用户输入直接拼入正则，FIELD 含正则元字符时异常（低风险）; 字段存在但为空值时误报 "Field not found"（L53-56）; 使用 `[ ]`/`$0` 而非 `[[ ]]` 风格 — 与 skill 其他材料的 bash 风格不一致（可接受，POSIX 兼容性更好）

**validate-settings.sh (101 行)**: 8 项检查 — 文件存在、可读、围栏计数 ≥2、frontmatter 非空、含 `:`、字段清单、布尔字段校验（enabled/strict_mode）、body 存在性。带 ✅/⚠️ 输出与重启提醒，可运行 ✓
- 小问题: Check 5 的 `grep -q ':'` 检查过于宽松（frontmatter 里任意冒号即过）; `grep -c '^---$'` 计数含 body 中的 `---`（若 body 有 `---` 分隔线而 frontmatter 缺围栏，会被误判合法）— 均为轻微
- 亮点: 明确的退出码约定（1 = 失败）、中英混合输出友好、重启提醒收尾

### 5.5 跨 Skill 引用检查
- SKILL.md 无 `../` 跨 skill 文件路径 ✓
- L434-482 的 real-world 示例以 prose 方式提及插件名（multi-agent-swarm、ralph-wiggum），无文件路径引用 — 符合 SKILL-SPEC §3.3 ✓
- references/real-world-examples.md 同样只有 prose 插件名 ✓

### 5.6 嵌套重复/死文件检查
- 无 self-nested 目录、无 `.gitkeep` 等垃圾文件 ✓
- 重复对: SKILL.md Real-World Examples 节 ↔ real-world-examples.md（~60% 重叠，压缩版关系）; SKILL.md Parsing Techniques 节 ↔ parsing-techniques.md（缩略版关系）; 无逐字重复
- 6 个"死资源"（SKILL.md 视角不可达）见 §5.1 — 不是文件多余，而是索引缺失

---

## 6. 语法与格式质量

### 6.1 拼写错误
- SKILL.md 与全部参考文件无拼写错误。领域术语（frontmatter、gitignore、traversal、sanitize）拼写正确 ✓

### 6.2 语法错误
- 无明显语法错误。bash 片段语法正确（set -euo pipefail、[[ ]] 条件、heredoc 均规范）✓

### 6.3 中英/葡英混杂
- 全库纯英文，无中英/葡英混杂 ✓（scripts/validate-settings.sh 输出含中文 emoji 但文字为英文）

### 6.4 Markdown 格式破损（1 处实质 + 2 处轻微）

| # | 位置 | 问题 | 严重度 |
|---|------|------|:------:|
| M-1 | SKILL.md L304/L314 | 转义反引号围栏（`\`\`\``），代码块不渲染 | **实质** |
| M-2 | SKILL.md L298/L317 | 外层围栏为 ```markdown 但内容含 H2 标题与非代码文本，语义混用（可接受的教学演示写法，但配合 M-1 整体失效） | 轻微 |
| M-3 | quick-reference.md L3 | "### File Location" 后无过渡直接接代码块 | 轻微 |

### 6.5 占位符未填充
- 无 `TODO`、`FIXME`、`[PLACEHOLDER]` 等未填充标记 ✓

### 6.6 截断内容
- 全部 13 个文件以合理内容收尾，无截断 ✓（SKILL.md 以 Reference Files 列表收尾，完整）

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` 的 12 条规则:

1. **name 匹配目录名**: ✅ `plugin-settings` 匹配 `062-plugin-settings`
2. **description 第三人称/结构**: ⚠️ 无第一/第二人称、无祈使句（"should be used" 为第三人称被动），但 "This skill should be used when" 非 §2.2 模板结构（stub 认定为 §2.3 违规）
3. **description 含触发短语**: ❌ §2.4 五种标准短语（"Use when the user..." / "Triggers on..." / "Use for..." 等）无一出现
4. **description ≤1024 字符**: ✅ 约 400 字符
5. **无禁止 frontmatter 字段**: ✅ 仅 name、description
6. **body ≤600 行**: ✅ 487 行（tool pattern 目标 ~300，超出但合规）
7. **Workflow/Process 节存在**: ⚠️ 无显式节，过程内容分散在 Reading/Creating/Common Patterns 三区块
8. **Output Format 节存在**: ⚠️ File Structure 隐含输出格式（.local.md 即交付物），无显式节
9. **Scope/Limitations 节存在**: ❌ 无任何"何时不使用"声明
10. **无跨 skill 文件路径引用**: ✅
11. **allowed-tools 格式正确**: ➖ 字段缺失（可选字段，非违规，建议补充）
12. **路径仅指向本 skill 目录内**: ✅ 全部为相对路径

**合规率: 7 条完全合规 + 3 条部分合规 + 2 条违规**（≈8.5/12）

### 违规详情

**违规 1 — description 无 §2.4 标准触发短语（规则 3）**: SKILL-SPEC §2.4 要求至少出现一个标准触发信号短语。本 description 的 "should be used when the user asks about" 是标准短语的变体，但无一个标准短语逐字出现。对 SkillIF 这类以 description 触发为核心的测评语料库，这是必须修的（修复见 §13 F-1）。

**违规 2 — 缺少 Scope/Limitations 节（规则 9）**: 全库最常见缺口（~220/322，68%），本 skill 亦未幸免。修复见 §13 F-2。

### 与同 corpus 的横向对比
- description 关键词密度: 9 个触发词/短语，全库最高档之一 —— 内容层面远超多数 tool 型 skill
- 三必需节形态: 与本批 061（🟢）/063（🟢）同属"功能完备但无显式 Scope/Output 节"的 tool 型常态 —— 本 skill 的缺口不是特例，但 description 触发短语问题是本批 5 个（061-065）中唯一一例

---

## 8. 人机感评估

### 8.1 Emoji 审计
- SKILL.md body 仅 2 处 emoji（⚠️），均在 bash 校验脚本代码片段的 stderr 输出中（L369 "⚠️ Invalid max_value... "、L421 "⚠️ Invalid path..."）— **功能性使用**（脚本运行时面向用户的警告符号），非装饰 ✓
- references/real-world-examples.md 的 ✅/❌ 标记用于 BAD/GOOD 对照 —— 教学功能性 ✓
- scripts/validate-settings.sh 的 ✅/❌/🔍 为脚本输出 —— 功能性 ✓
- 无装饰性 emoji 滥用 ✓

### 8.2 全大写/喊叫式语言
- 仅 "**Important:**"（L376）与 Best Practices 的 "DO:"/"DON'T:" 列表头 —— 适度强调，无 STOP!/MANDATORY/CRITICAL 式喊叫 ✓

### 8.3 Persona 语气分析
整体语气: **实用工程手册 + 模式速查**。代表性证据:
- "Quick exit if file does not exist"（L75-77）— 直给结论，无铺垫
- "Use case: Enable/disable hooks without editing hooks.json (requires restart)."（L204）— 一句话点明场景价值
- Best Practices 的 DO/DON'T — 决策表式，agent 可直接消费

语气评价: 与"给 agent 提供可复制模式"的定位高度适配，中性、无填充语、无营销腔。

### 8.4 人机边界分析
- Security Considerations 明确 agent 在写入配置时的消毒/校验责任（SAFE_VALUE、`..` 拦截）✓
- "Default Patterns"（L345-358）定义了文件不存在时的降级行为 —— 人机协作场景下的默认值约定清晰 ✓
- 缺一层显式边界: 未说明"配置变更这类影响 hook 行为的操作，agent 应提示用户重启并确认"的交互节点 —— 虽有 restart 提示，但全部为文档声明而非交互协议（O 级）

### 8.5 人称分析
- 指令层全部第三人称（"This skill should be used...", "Plugins can store..."）✓
- 无面向用户话术（该 skill 不产出对话，只产出文件与代码）— 人称结构干净 ✓

### 8.6 表格使用评估
- SKILL.md body 无表格 —— 全部以代码块 + 列表呈现，对 bash 教学是正确选择 ✓
- real-world-examples.md 的模式对比表（L256-264）使用恰当 ✓
- 无"为表格而表格"的滥用 ✓

---

## 9. 可执行性评估

### 9.1 独立可执行性
- 假设 agent 只拿到 SKILL.md（无目录探索）: **可执行** —— 快速退出、frontmatter 提取、字段读取、body 解析、默认值、校验回退、gitignore、安全转义、模板，全部内联且代码可直接复制
- 丢失的能力: 仅当 agent 主动探索目录才能发现 scripts/validate-settings.sh（QA-01 的判定路径）与 parsing-techniques.md 的 yq 深度方案
- 打分: **8/10** —— 核心任务零依赖可完成；QA-01 依赖的脚本调用属"碰运气"式行为

### 9.2 步骤可操作性

| 模式 | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| 快速退出 | `if [[ ! -f ... ]]` + enabled 检查 | 🟢 | 代码完整可复制 |
| frontmatter 提取 | sed 范围提取 | 🟢 | 原理逐行解释 |
| 字段读取 | grep + sed | 🟡 | Pattern 1 缺引号剥离（§4.1） |
| body 提取 | awk 计数器法 | 🟢 | 边界处理正确 |
| 默认值 | 文件缺失时回退 | 🟢 | Default Patterns 完整 |
| 校验 | 数值范围/枚举回退 | 🟢 | 带错误消息与回退值 |
| gitignore | `.claude/*.local.md` | 🟢 | 双模式全覆盖 |
| 安全 | 消毒/穿越/权限 | 🟢 | 三件套齐全 |
| 模板生成 | Template Generation | 🟡 | **围栏破损，渲染不可读（§4.4）** |

### 9.3 工具依赖合理性
- 核心: bash coreutils（sed/grep/awk）— 所有主流环境预装 ✓
- hook 输入解析: jq（examples/read-settings-hook.sh L31-32 使用）— macOS/Linux 常见，Windows 需手动安装（脚本有 jq 依赖但未声明）
- 可选: yq（parsing-techniques.md 的复杂 YAML 方案，注明 "brew install yq"）— 有降级路径 ✓
- 无硬编码第三方服务依赖 ✓

### 9.4 时间预算
- 无时间预算声明 — tool 型参考 skill 不需要，可接受 ✓

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml（178 行）定义 20 个 criteria: SCOPE-01~03（3）、PROC-01~07（7）、OUT-01~03（3）、NEG-01~03（3）、QA-01~04（4），与 `total_items: 20` 一致 ✓。评估覆盖度:

| 类别 | 评分项 | 与 SKILL/references 对应 | 覆盖评价 |
|------|--------|--------------------------|:--------:|
| SCOPE-01 | 识别为插件配置任务 + .local.md 模式 | SKILL.md Overview L9-19 | 🟢 直接对应 |
| SCOPE-02 | YAML frontmatter + markdown body | File Structure L25-59 | 🟢 |
| SCOPE-03 | `.claude/*.local.md` 文件存在 | file_exists glob 检查 | 🟢（checker 支持 glob） |
| PROC-01 | frontmatter 提取 + 字段读取 | Parsing Techniques L139-174 | 🟢 |
| PROC-02 | 快速退出模式 | Pattern 1 + read-settings-hook.sh | 🟢（Pattern 1 引号缺陷见 §4.1） |
| PROC-03 | 无文件时默认值 | Default Patterns L345-358 | 🟢 |
| PROC-04 | 数值校验 + 回退 | Validation L360-372 | 🟢 |
| PROC-05 | markdown body 解析 | Parsing Techniques L167-174 | 🟢 |
| PROC-06 | 告知重启要求 | Restart Requirement L374-391（6 处） | 🟢（声明冗余但充分） |
| PROC-07 | 7 步实现流程 | implementation-workflow.md | 🟢 **映射逐字精确** |
| OUT-01 | 类型化值 frontmatter | 各处模板（string/bool/number/list） | 🟢 |
| OUT-02 | bash 片段语法有效 | read-settings-hook.sh + 全部片段 | 🟢 |
| OUT-03 | gitignore 条目 | Best Practices L334-343 | 🟢 |
| NEG-01 | 不使用错误目录/命名 | DO/DON'T L320-333 | 🟢 |
| NEG-02 | 输入转义 | Security L396-410 | 🟢 |
| NEG-03 | 路径穿越防护 | Security L412-424 | 🟢 |
| QA-01 | 运行 validate-settings/parse-frontmatter | scripts/（存在但不可发现） | 🟡 依赖 agent 主动探索 |
| QA-02 | 安全三件套 | Security Considerations | 🟢 |
| QA-03 | 匹配真实世界模式 | Common Patterns 3 模式 | 🟢 |
| QA-04 | 提供模板 + 创建说明 | Template Generation + example-settings.md | 🟡 模板节围栏破损 |

**覆盖评价**: 20 项评分设计精良、与 skill 内容映射清晰，PROC-07 的 7 步映射是本语料库评估-内容对齐最精确的样本之一。两个 🟡 均源于 skill 侧缺陷（QA-01 的可发现性、QA-04 的围栏破损），非评估设计问题。

### 10.2 Critical Failures 分析

- **CF-01**（配置存入会被提交的位置/破坏命名的位置 → cap_to_0）: 合理 —— NEG-01 的致命版，与 Best Practices 的 DON'T 直接对应 ✓
- **CF-02**（解析代码破损——提取字段与 frontmatter 不符或带引号值解析失败 → cap_to_0）: 方向合理，但**触发路径被 skill 自己提供** —— SKILL.md Pattern 1（§4.1）正是"对带引号值解析失败"的实现，照抄 Pattern 1 的 agent 会产出被 CF-02 判定为零分的解析代码。这是 060-ux-audit-rethink 的 §4.4 同类问题（模板教 agent 做被判定为致命的事），但程度较轻: 正确示例（read-settings-hook.sh、real-world-examples.md）存在且完整，agent 有更大概率照抄正确版本

### 10.3 缺失的测评点建议
- 无检查"输出是否包含 markdown body 的使用场景（作为 prompt/context）"的 criterion —— PROC-05 只验证提取，不验证使用
- 无检查"agent 是否实际写入 .gitignore 条目"的 criterion —— OUT-03 只查输出文本含 gitignore 行
- 无检查"配置文件权限（chmod 600）"的 criterion —— QA-02 为 llm judge，覆盖了权限建议但无脚本化判定（低优先）

### 10.4 check.py 审查（83 行）
- 实现 14 项脚本检查（SCOPE-02/03, PROC-01~05, OUT-01~03, NEG-01~03, QA-01），与 SCORING.yaml 的 judge: script 标注一致 ✓（docstring "14 script checks" 属实）
- SCOPE-03 的 `file_exists` 支持 glob（checker.py L20-23 确认）✓
- 正则与 SKILL.md 内容命中验证: PROC-03 的 `ENABLED=true|MODE=standard` 命中 L351-352 ✓; PROC-04 的 `invalid .*in settings` 命中 L369 ✓; OUT-01 的 `enabled: (true|false)` 命中多处模板 ✓; OUT-03 的 `\.claude/\*\.local\.md` 命中 L339 ✓
- 两个观察:
  1. **SCORING.yaml 与 check.py 的正则转义语义不一致（低严重度）**: SCORING.yaml 用 YAML 单引号字符串（`'...'`），其中 `\\` 是字面两个反斜杠; check.py 用 Python 字符串，`\\` 经 Python 解析为一个反斜杠。例如 PROC-02 的 `! -f \\$STATE_FILE` — 在 check.py 中正确（`\$` = 字面 `$`，可匹配 `! -f "$STATE_FILE"`）; 若 runner 直接按 CHECKER-LIBRARY.md 约定从 SCORING.yaml 取 pattern 传给 output_contains，`\\` 会变成"字面反斜杠 + 行尾锚点"，永不匹配。check.py 是权威实现（runner 调用 check.py），YAML 侧应视为参考 — 但任何人用通用 runner 复用 SCORING.yaml 时需注意
  2. **NEG-01 以正向断言实现**: `tool_log_contains('(?i)\.claude/\S*\.local\.md')` — "negative" 项实为检查 agent 的工具调用中出现正确命名（正向证据），语义合理但命名易误导（若 runner 误用 tool_log_not_contains 则判定反转）

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 位于 `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`，062 条目原文:

> ### 062-plugin-settings
> - **逻辑**: 文件结构、读取/解析/创建模式、最佳实践与安全注意项全部自洽；"Template Generation" 示例使用转义反引号，代码块不会渲染为围栏。
> - **语法**: 除上述转义围栏外规范流畅。
> - **人机感**: 实用专业，⚠️ 仅出现在校验脚本输出中，属功能性使用。
> - **合规**: Description 第三人称含触发短语，有 Workflow/示例/最佳实践结构，正文 491 行 ≤600。
> - **总评**: 🟢 内容完备、逻辑一致。

### 11.1 档案评分与本次深度审查的差异

| 维度 | Dossier 判定 | 本次深审发现 | 差异原因 |
|------|:---:|:---:|------|
| 模式自洽性 | "全部自洽" | 主体自洽，但 Pattern 1 引号剥离与自身 hook 脚本/参考文件不一致 | Dossier 未跨文件比对解析代码 |
| 转义反引号 | "代码块不会渲染为围栏" | 确认属实（L304/L314 字节级验证） | 一致 ✓ |
| "正文 491 行" | 491 | **实际 487 行**（wc -l） | Dossier 行数统计偏差 4 行 |
| "Description 含触发短语" | ✅ | §2.4 五种标准短语无一出现；仅有变体 "should be used when the user asks about" | Dossier 对触发短语采用宽松判定（含 "when the user asks" 即算） |
| "有 Workflow 结构" | ✅ | 无显式 Workflow/Output/Scope 节（功能区块隐含承担） | Dossier 以内容覆盖代替形式判定 |
| 未提及 | — | Reference Files 索引断层、restart 张力、6 个不可达文件 | Dossier 未核对引用可达性 |

结论: Dossier 的 🟢 针对"SKILL.md 单文件内容质量"成立 —— 内容层面确实完备自洽; 本深审将范围扩大到引用图谱与跨文件一致性后，评级维持 🟢 档下限、调整评分（见 §12）。

### 11.2 旧 stub REVIEW 复核
- 原 stub 判定 "Description 以 'This skill should be used when' 开头——违反 §2.3" — **方向确认，边界澄清**: §2.3 明文禁令（imperative / first-person / second-person）未被逐字触发（"should be used" 为第三人称被动），但 §2.2 模板结构偏离 + §2.4 触发短语缺失成立，该问题升级为规则 3 违规（§7 违规 1）
- 原 stub 判定 "模板生成示例使用转义反引号——代码块渲染破损" — **确认属实**（字节级验证 L304/L314）
- 原 stub 评分 🟢 B (50/100) — 分数尺度过紧（与 061 B+ 53 / 063 A− 56 同级压缩）；本深审在完整 0-100 尺度上评 71/100，差异主要来自: stub 未计入参考库质量与可执行性（二者实际为上乘），也未计入触发短语/Scope/Output 三项合规缺口（互相抵消后净上修）

### 11.3 全库横向背景
Dossier 汇总（322 个 skill）: 🟢46% / 🟡45% / 🟠7.5% / 🔴1.5%; "缺 Scope 节"（~220 个，68%）与"缺 Output 节"（~180 个，56%）是全库最普遍缺口 — 062 的 Scope/Output 缺失属共性问题; 但 description 触发短语缺失（~35 个，11%）中，062 是少数"内容完整但触发结构不合规"的样本，比同批 047/314 的截断型 description 问题轻得多

---

## 12. 综合评分

### 维度评分

**Frontmatter 合规 (7/10, 权重 10%)**: name/字段/YAML 语法零瑕疵; description 内容完整（WHAT + WHEN + 9 关键词，全库关键词密度最高档），但 §2.4 触发短语缺失 + §2.2 模板结构偏离（stub 已点名）; 缺 allowed-tools（可选）。

**Body 结构完整 (6/10, 权重 10%)**: 487 行结构清晰、分区合理、示例全覆盖; 无显式 Workflow/Output/Scope 节（前两者有功能区块隐含，Scope 完全缺失）; Reference Files 索引断层。

**逻辑一致性 (7/10, 权重 20%)**: 模式体系自洽、示例代码可运行、安全/最佳实践/评分项三方对齐; 扣分点: Pattern 1 引号剥离不一致（§4.1）、restart 声明 6 处冗余且与自身机制张力（§4.2）、转义围栏（§4.4）、不可验证行号引用（§4.6）。

**参考完整性 (8/10, 权重 15%)**: 12 个附属文件全部存在且质量上乘（parsing-techniques.md 549 行为全库最佳 bash 参考之一）; 无悬空引用; 扣分: 6 个文件无法从 SKILL.md 直达（索引断层）。

**语法格式 (7/10, 权重 10%)**: 全库无拼写错误、无截断、bash 语法规范; 1 处实质围栏破损（L304/L314）+ 2 处轻微格式问题。

**规范合规 (6/10, 权重 15%)**: 12 条规则 7 条完全合规 + 3 条部分 + 2 条违规（触发短语、Scope 节）。

**人机感 (8/10, 权重 10%)**: 中性实用工程语气; emoji 仅功能性（2 处脚本警告符号）; DO/DON'T 决策表式; 无喊叫、无填充语。

**可执行性 (8/10, 权重 10%)**: 核心任务仅凭 SKILL.md 零依赖可完成（9 个模式全部内联可复制）; 扣分: QA-01 依赖脚本不可发现、模板节渲染破损。

### 加权计算

| 维度 | 得分 | 权重 | 加权 |
|------|:----:|:----:|:----:|
| Frontmatter 合规 | 7 | 10% | 0.70 |
| Body 结构完整 | 6 | 10% | 0.60 |
| 逻辑一致性 | 7 | 20% | 1.40 |
| 参考完整性 | 8 | 15% | 1.20 |
| 语法格式 | 7 | 10% | 0.70 |
| 规范合规 | 6 | 15% | 0.90 |
| 人机感 | 8 | 10% | 0.80 |
| 可执行性 | 8 | 10% | 0.80 |
| **合计** | | | **7.10 → 71/100** |

### 评级: 🟡 B+ (71/100)

可用，有需要修复的问题。内容质量（模式体系、参考库、安全三件套、可复制性）达到 tool 型 skill 的上乘水准，评估-内容映射（PROC-07 逐字对齐）是全库范例; 扣分集中在结构合规层: description 触发短语缺失、缺 Scope 节、缺显式 Output 节、模板围栏破损、引用索引断层。修复集中在 2 个致命项 + 7 个重要项（§13），总工作量约 0.5-1 个工作日，修复后可达 🟢 A− (80+)。

---

## 13. 修复建议（按优先级分层）

本节按 🔴 致命 → 🟡 重要 → 🟢 优化三级给出全部修复项。修复遵循两个总原则: (1) description 必须含 §2.4 标准触发短语且保持现有 9 个关键词不丢; (2) 任何"SKILL.md 承诺给 agent 的能力"必须能从 SKILL.md 直达（打开即用），不允许藏在二级索引之后。

### 🔴 致命缺陷（必须修复，不修则评估结果失真）

**F-1: description 无 §2.4 标准触发短语 — 触发匹配的生命线缺陷**

- 位置: SKILL.md L3
- 现状: "This skill should be used when the user asks about X, Y, Z..." — §2.2 模板要求 "<what it does, third-person>. Use when the user <triggers>."; §2.4 的五种标准短语（"Use when the user..." / "Use when the user asks to..." / "Use when the user needs to..." / "Triggers on..." / "Use for..."）**无一出现**。stub 已认定 §2.3 违规（方向正确，边界见 §11.2）。在 SkillIF 的 2 Mode × 5 Harness 测评矩阵中，description 是自动触发判定的唯一依据 —— 非标准触发结构直接削弱该 skill 在"无触发对照集"实验中的可发现性
- 修复: 按 §2.2 模板重写（WHAT 在前、标准触发在后、保留全部 9 个关键词）:

```yaml
description: "Documents the .claude/plugin-name.local.md pattern for storing
plugin-specific configuration with YAML frontmatter and markdown content, and
shows how to read it from hooks, commands, and agents. Use when the user asks
about plugin settings, wants to store plugin configuration or make a plugin
user-configurable, mentions .local.md state files, or needs to read YAML
frontmatter from per-project plugin settings files."
```

- 若一行式书写: `description: "Documents the .claude/plugin-name.local.md pattern for storing plugin-specific configuration with YAML frontmatter and markdown content, and shows how to read it from hooks, commands, and agents. Use when the user asks about plugin settings, wants to store plugin configuration, make a plugin user-configurable, or needs to read YAML frontmatter from per-project plugin settings files."`（约 420 字符，≤1024 ✓）
- 修复验收标准: description 中出现 §2.4 标准短语 "Use when the user"（逐字）; 关键词清单（plugin settings / store plugin configuration / user-configurable / .local.md / YAML frontmatter / per-project）全部保留
- 不修复的后果: 触发判定依赖非标准结构; 测评矩阵中命中率不可控; 已在 stub 中登记的违规持续存在

**F-2: body 缺 Scope/Limitations 节（SKILL-SPEC §3.1 规则 9 违规）**

- 位置: SKILL.md — 需新增章节
- 现状: Best Practices 的 DO/DON'T 只覆盖文件命名规范，全库无任何"何时不使用本 skill / 本模式不适用于什么"的声明。agent 可能在全局配置、密钥存储、多用户管理等场景错误套用 `.local.md` 模式
- 修复: 在 "## Security Considerations"（L394）之前插入:

```markdown
## Scope and Limitations

Use this skill when the task involves per-project plugin configuration stored
in `.claude/plugin-name.local.md` files (YAML frontmatter + markdown body),
read from hooks, commands, or agents.

Do NOT use this skill when:
- The configuration must be shared across users or machines — `.local.md`
  files are per-project and user-local by design.
- The settings contain secrets or credentials — use the OS secret store or
  environment variables instead; `.local.md` files are plain text (chmod 600
  is a mild protection, not encryption).
- The task is about Claude Code's own configuration (settings.json,
  hooks.json) — that is managed by the harness, not by the plugin pattern.
- The plugin needs a settings UI or multi-user management — this skill
  documents a plain-text convention, not a configuration service.

Limitations:
- The sed/grep parsing snippets handle flat, single-line scalar values.
  For nested or complex YAML, use yq (see references/parsing-techniques.md).
- Hook definitions cannot be hot-swapped within a session; settings file
  changes are picked up on the next hook trigger (see Best Practices).
```

- 不修复的后果: 规则 9 违规持续; agent 无"何时不触发"判据，可能在不适配场景下错误套用本模式

### 🟡 重要缺陷（建议修复，影响可用性但不阻断）

**I-1: 转义反引号围栏 — Template Generation 示例渲染破损**

- 位置: SKILL.md L304（`\`\`\`markdown`）与 L314（`\`\`\``）
- 现状: 两行为反斜杠 + 反引号字面量，markdown 渲染为 `\`\`\`markdown` 文本，内层代码块不成立。该节是 QA-04（提供模板）依赖的交付物展示，破损后 agent 看到的是一串转义符号
- 修复: 将 L304 改为真实反引号 ```markdown、L314 改为真实反引号 ```（外层围栏 L298/L317 保持不动即可; 若担心嵌套渲染歧义，可把内层改为 4 空格缩进代码块或加语言标注）。修改后的渲染效果应为:

```
## Configuration

Create `.claude/my-plugin.local.md` in your project:

```markdown
---
enabled: true
mode: standard
max_retries: 3
---

# Plugin Configuration

Your settings are active.
```
```

（实际编辑时直接替换 L304/L314 的反斜杠反引号为纯反引号; 修复后对 L294-317 整体做一次 markdown 渲染验证）
- 不修复的后果: dossier 与 stub 均已点名的缺陷持续; 模板节对 agent 不可读，QA-04 依赖的交付物展示失效

**I-2: Reference Files 索引断层 — 6 个文件无法从 SKILL.md 直达**

- 位置: SKILL.md L484-488
- 现状: "## Reference Files" 只索引 3 个文件; parsing-techniques.md（549 行）与 real-world-examples.md（395 行）经 additional-resources.md 二级跳转; scripts/parse-frontmatter.sh、scripts/validate-settings.sh、examples/create-settings-command.md、examples/example-settings.md 零提及
- 修复: 扩展 Reference Files 节为全量索引:

```markdown
## Reference Files

- **Parsing Techniques**: see [references/parsing-techniques.md](references/parsing-techniques.md) — complete parsing guide (quotes, lists, edge cases, yq)
- **Real-World Examples**: see [references/real-world-examples.md](references/real-world-examples.md) — multi-agent-swarm and ralph-wiggum implementations
- **Implementation Workflow**: see [references/implementation-workflow.md](references/implementation-workflow.md)
- **Quick Reference**: see [references/quick-reference.md](references/quick-reference.md)
- **Additional Resources**: see [references/additional-resources.md](references/additional-resources.md)
- **Example Hook**: see [examples/read-settings-hook.sh](examples/read-settings-hook.sh)
- **Example Templates**: see [examples/example-settings.md](examples/example-settings.md)
- **Create Command**: see [examples/create-settings-command.md](examples/create-settings-command.md)
- **Utilities**: validate settings with `scripts/validate-settings.sh` and parse fields with `scripts/parse-frontmatter.sh` (see [scripts/](scripts/))
```

- 或最小方案: 在节首加一句执行引导: "**Execution order**: read `references/parsing-techniques.md` for parsing details, `references/real-world-examples.md` for production implementations, and run `scripts/validate-settings.sh` to validate any settings file you create."
- 不修复的后果: agent 按 SKILL.md 执行时永远接触不到解析深度方案与校验工具; **QA-01 的通过路径（tool log 中出现 validate-settings/parse-frontmatter）变成依赖 agent 自发探索目录的行为** —— 评测判定与 skill 指引脱钩

**I-3: Pattern 1 引号剥离缺失 — 与自身参考材料不一致，且与 CF-02 直接冲突**

- 位置: SKILL.md L193-194（"Common Patterns → Pattern 1"）
- 现状: Pattern 1 提取 enabled 后不带引号剥离; YAML 合法的 `enabled: "true"` 会被判定为禁用。同一 skill 的 examples/read-settings-hook.sh L20-21 与 real-world-examples.md L65-69 均带 `sed 's/^"\(.*\)"$/\1/'`。SKILL.md 主体是其全部材料中引号处理最弱的一份
- 修复: 两处（L193-194 与 SKILL.md 内所有不带剥离的字段提取）统一为:

```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
```

- 同时建议在 Parsing Techniques 节（L139）开头加一行边界声明: "The snippets below handle flat, single-line scalar values. For quoted or complex values, always strip surrounding quotes (see 'Read Individual Fields'); for nested YAML use yq."
- 不修复的后果: 照抄 Pattern 1 的 agent 产出"对带引号值解析失败"的实现 —— **与 CF-02（cap_to_0）判定标准直接冲突**（§10.2），skill 亲手提供触发致命判定的路径

**I-4: Restart 要求收敛 — 6 处冗余声明与自身机制张力**

- 位置: SKILL.md L291、L316、L376、L383-391; examples/example-settings.md L159
- 现状: 技能演示的机制（hook 每次触发重新读取 .local.md）意味着数据文件修改下次触发即生效，无需重启; 但技能 6 次强制"必须重启"。声明对"hook 定义变更"成立，对"hook 运行时读取的数据文件"不成立
- 修复: 保留一句保守声明（评估 PROC-06 依赖"告知重启"），删除其余重复:

```markdown
### Restart Requirement

**Important**: After editing `.claude/plugin-name.local.md`, restart Claude Code
to guarantee the new settings are picked up. Hooks re-read the file on each
trigger, so changes may take effect without a restart — but the documented,
deterministic behavior is to restart. Hook definitions themselves cannot be
hot-swapped within a session.
```

- 不修复的后果: 6 处冗余且部分失真的提示削弱文档可信度; 与技能自证机制（L74-97 运行时读取）的矛盾持续

**I-5: body 补显式 Output Format 节（规则 8 部分合规的完整化）**

- 位置: SKILL.md — 在 "## Overview"（L9）之后新增
- 修复:

```markdown
## Output

This skill delivers:
1. A `.claude/<plugin-name>.local.md` settings file — YAML frontmatter with
   typed values (string/boolean/numeric/list) plus a markdown body for
   prompts or context (see File Structure).
2. Parsing code for hooks, commands, and agents that reads the settings at
   runtime (see Reading Configuration Files and Parsing Techniques).
3. Plugin documentation: configuration template, .gitignore entry, and the
   restart note for the plugin README (see Best Practices).
```

- 不修复的后果: 规则 8 部分合规状态持续; agent 对"完成"的定义不统一（交付 1 个文件还是 3 件套）

**I-6: 不可验证的行号引用 — 删除或改为行为描述**

- 位置: SKILL.md L457（"lines 15-18"）、L477（"lines 15-18"）
- 现状: 引用的脚本位于外部插件，本 skill 内无副本，行号无从核对; 两处相同行号（15-18）指向不同脚本，暗示复制痕迹
- 修复: L457 改为 "- Checks if file exists (quick exit if not present)"; L477 改为 "- Checks if file exists (quick exit if not active)"
- 不修复的后果: 无法验证的精确引用属于无效信息; 两处相同行号削弱可信度

**I-7: examples/create-settings-command.md 的 allowed-tools 格式与 SKILL-SPEC 不一致**

- 位置: examples/create-settings-command.md L3 `allowed-tools: ["Write", "AskUserQuestion"]`
- 现状: SKILL-SPEC §1.2 要求逗号分隔字符串（`Read, Write, Bash`）; 示例文件使用 YAML 数组。虽非 SKILL.md frontmatter，但作为 corpus 教学材料会传播错误格式。另: AskUserQuestion 工具在部分环境不可用（与 053-go-to-market-plan 同类问题）
- 修复: 改为 `allowed-tools: Write, AskUserQuestion`; 或在该文件 Implementation Notes 注明 AskUserQuestion 不可用时的回退（AskUserQuestion 不可用时用文本问题列表）
- 不修复的后果: 示例与规范格式不一致被 agent 复制到自己的 command frontmatter

### 🟢 优化建议（锦上添花）

**O-1: 补充 allowed-tools 字段**
- SKILL.md frontmatter 增加 `allowed-tools: Read, Write, Bash, Glob` — 该技能执行需要读状态文件、写 .local.md、运行 bash 解析/校验脚本、定位文件

**O-2: sed 解析局限的一行免责声明**
- 在 "## Parsing Techniques"（L139）开头加: "The sed/grep snippets below handle flat, single-line scalar values. For nested YAML, quoted-complex values, or lists, use yq — see references/parsing-techniques.md §Alternative: Using yq."

**O-3: examples/example-settings.md 的 vim 编辑示例加跨平台替代**
- L150-157 的 `vim .claude/my-plugin.local.md` 对 Windows 用户不友好 — 补充 `code .claude/my-plugin.local.md`（VS Code）或任意文本编辑器说明

**O-4: 数值校验错误文案统一**
- SKILL.md L368-369（"Invalid max_value in settings (must be 1-100)"）与 references/parsing-techniques.md L289-297（"max_size must be a number"）文案不同 — 无矛盾，但统一可减少 agent 输出差异

**O-5: Quick Reference 的格式小修**
- references/quick-reference.md L3 "### File Location" 后直接接代码块 — 加一句过渡说明（"The pattern lives in the project's .claude/ directory:"）

**O-6: 评估侧加固（配合 I-3）**
- SCORING.yaml 的 PROC-02/OUT-02 依赖的示例统一为带引号剥离版本后，可在 check.py 的 PROC-02 正则中追加 `sed 's/\\^"\\(.*\\)"\\$/\\1/'` 备选匹配，使"agent 输出含引号剥离"成为额外加分信号（可选）

**O-7: real-world 示例的重复节合并**
- SKILL.md Real-World Examples 节（L434-482）与 references/real-world-examples.md 约 60% 重叠 — 保留 SKILL.md 压缩版（当前形态合理），仅在 I-2 的全量索引中标注 reference 版为"完整实现"，维持压缩版/完整版分工

### 修复工作量估计

| 级别 | 项数 | 预计耗时 | 涉及文件 |
|------|:----:|:--------:|----------|
| 🔴 致命 | 2 | 30-40 分钟 | SKILL.md（description 重写 + Scope 节插入） |
| 🟡 重要 | 7 | 1-1.5 小时 | SKILL.md（L304/L314、L193-194、L291/316/376/383-391、L457/477、L484-488、Overview 后）、examples/create-settings-command.md |
| 🟢 优化 | 7 | 30-45 分钟 | SKILL.md、examples/example-settings.md、references/quick-reference.md、references/parsing-techniques.md |

- 净变化: 约 +60 行新增 / -15 行删除（主要来自 F-2 Scope 节、I-2 全量索引、I-4 收敛）
- 优先级执行顺序: F-1 → F-2 → I-1 → I-2 → I-3 → I-4 → I-5 → I-6/I-7 → 其余
- 修复完成标准: (1) description 含逐字 "Use when the user"; (2) body 含 Scope/Limitations 与 Output 两节; (3) SKILL.md 全部 10 个附属文件可直达; (4) 全库代码块围栏渲染验证通过（L294-317 修复后正常显示）; (5) Pattern 1 与 read-settings-hook.sh 的引号处理行为一致

### 修复后预期评级

F-1/F-2 + I-1/I-2/I-3/I-5 落地后: Frontmatter 合规 7→9、规范合规 6→9、语法格式 7→9、Body 结构 6→8 → 加权约 **8.1/10 ≈ 81/100**，达 🟢 A−。该 skill 的内容底子（模式完整性、参考库质量、安全三件套、评估-内容对齐）是 tool 型 skill 的上乘水准 — 全部缺口集中在描述结构、必需节与引用索引三个可低成本的表述层面，无任何内容性重写需求。

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 487 行，全文精读（字节级验证 L3 description 转义、L304/L314 围栏）
2. SCORING.yaml — 178 行，全文（含全部 20 项 criteria 与 2 项 critical failures）
3. check.py — 83 行，全文（14 项脚本检查逐一核对正则）
4. examples/create-settings-command.md — 98 行，全文
5. examples/example-settings.md — 159 行，全文
6. examples/read-settings-hook.sh — 65 行，全文
7. references/additional-resources.md — 22 行，全文
8. references/implementation-workflow.md — 12 行，全文
9. references/parsing-techniques.md — 549 行，全文
10. references/quick-reference.md — 31 行，全文
11. references/real-world-examples.md — 395 行，全文
12. scripts/parse-frontmatter.sh — 59 行，全文
13. scripts/validate-settings.sh — 101 行，全文
14. _shared/SKILL-SPEC.md — 162 行，全文（合规依据）
15. _shared/checker.py — 351 行，全文（验证 file_exists glob / tool_log_contains / output_contains 语义）
16. _shared/CHECKER-LIBRARY.md — 187 行，全文（验证 runner 变量解析约定）
17. skill-dossier.md — 1204 行，062 条目及其汇总统计（档案对比依据）
18. 参考模板: 060-ux-audit-rethink/REVIEW.md — 881 行、322-cold-start-interview/REVIEW.md — 625 行（13 节模板出处与评分尺度对齐）

### 读取统计
- 总文件数: 18（13 skill 文件 + 3 shared + 1 dossier + 1 模板参照）
- 总行数: 约 4,900 行

### 审查方法
- 全部文件全文阅读，未使用抽样; 关键字节用 `cat -A` 级验证（description 转义、围栏内容、文件行数）
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则
- 评分方法: 8 维度加权（权重与 060/322 的 REVIEW.md 一致），总评修正原 stub 的 50/100
- 引用图谱验证: SKILL.md 全部 4 处直接引用逐一核对存在性 + 目录内 9 个未被直接引用的文件逐一确认引用状态（6 个不可达）
- 评估侧核对: SCORING.yaml 20 项 criteria 与 check.py 14 项实现逐项对应，正则与 SKILL.md 内容命中验证（PROC-03/PROC-04/OUT-01/OUT-03 均命中）
