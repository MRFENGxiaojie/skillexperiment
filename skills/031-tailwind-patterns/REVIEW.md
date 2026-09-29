# REVIEW: 031-tailwind-patterns

**审查日期**: 2026-08-06
**Skill 类型**: mindset（SCORING.yaml 声明）— 实质为 Tailwind CSS v4 知识参考/模式速查手册，无执行流程
**Body 行数**: 约 264 行（第 7–270 行；第 270 行为末尾空行，实际内容行 263 行）
**参考文件数**: references/0, scripts/0, assets/0（目录仅 4 个文件，全部内联）

---

## 1. 目录全量清单

Glob `**/*` 结果（共 4 个文件，无任何子目录）：

| 文件 | 行数 | 角色 |
|------|------|------|
| `SKILL.md` | 270 | 技能主体（frontmatter 1–5 行 + body 7–270 行） |
| `SCORING.yaml` | 131 | 测评标准（14 项声明，实际 12 criteria + 2 critical_failures） |
| `check.py` | 74 | 脚本检查器（2 个 script 检查 + llm 项占位注释） |
| `REVIEW.md` | 7 | 本审查的前身 stub（含 dossier 评级 🟡 C+ 42/100） |

要点：目录结构极简，无 `references/`、`scripts/`、`assets/`。269 行左右的 body 完全内联在 SKILL.md 中，未做任何拆分委托。stub REVIEW.md 仅 7 行，核心信息是"三必需节全缺、v4 细节过时、综合 🟡 C+ (42/100)"，本审查在此基础上展开逐行核验。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- 第 2 行：`name: tailwind-patterns` — 小写 + 连字符，≤64 字符，合法。
- 与目录名 `031-tailwind-patterns` 的关系：SKILL-SPEC §4 要求目录名"匹配 name 字段"。此处目录带 `031-` 编号前缀而 name 不带。经核对语料惯例（029、030 等同批技能均如此），`NNN-` 为语料序列编号而非 name 一部分，全语料一致执行，故记为**惯例性偏差**而非本技能独有缺陷。若严格按规范字面执行则需要全语料统一修订，超出本技能范围。

### 2.2 description

- 第 3 行全文：`Tailwind CSS v4 principles. CSS-based configuration, container queries, modern patterns, design token architecture. Use when the user asks to style with Tailwind CSS, set up v4 CSS-first configuration, use container queries, dark mode, or design tokens, or build responsive layouts.`（约 280 字符，≤1024 ✓）
- **WHAT**：前半句"Tailwind CSS v4 principles…"以第三人称陈述技能功能 ✓。
- **WHEN**：触发信号 "Use when the user asks to…" 位于句首位置 ✓（符合 §2.4 要求之一），枚举了 6 类触发场景：常规样式、v4 CSS-first 配置、容器查询、暗色模式、设计令牌、响应式布局。
- **KEYWORDS**：Tailwind CSS、CSS-first、container queries、dark mode、design tokens、responsive — 关键词充分 ✓。
- 无命令式/第一/第二人称开头（"Use when the user" 为规范规定的触发短语本身，不违规）✓。
- 无跨技能路由语句 ✓。
- 小瑕疵：触发列表以逗号分隔、句末以 "or build responsive layouts" 收尾，其中 "dark mode, or design tokens" 的 "or" 位置略显口语化，但不影响机器解析，属 🟢 级润色项。

### 2.3 allowed-tools

- 第 4 行：`Read, Write, Edit, Glob, Grep` — 5 个纯文件工具，全部在 Claude Code 白名单内，无拼写错误。
- 无 `Bash`：与纯知识参考型技能匹配（不涉及构建/运行）。但需注意：若未来按修复建议补入"验证 v4 构建"类操作步骤，则需同步扩展该字段。

### 2.4 其他字段

仅 3 个字段（name/description/allowed-tools），无 `argument-hint`、`model`、`paths` 等可选字段——知识参考型技能不需要，合理。无任何禁止字段（对照 §1.3 的 30+ 个 forbidden 键逐一核对，均未出现）✓。

### 2.5 语法

YAML 解析无问题：第 2 行无引号标量合法；第 3 行 description 双引号包裹，内容无未转义引号；第 4 行逗号分隔列表合法。frontmatter 闭合 `---`（第 5 行）与 body 分离干净（第 6 行为空行），无语法错误。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

Body（第 7–270 行）为 12 个编号知识章节 + 1 条结尾提示，全部为并列主题，无前后依赖：

| 编号 | 章节 | 行号范围 | 形态 |
|------|------|----------|------|
| 标题 | `# Tailwind CSS Patterns (v4 - 2025)` + 引言 blockquote | 7–11 | 标题 + 1 行引用 |
| 1 | Tailwind v4 Architecture | 13–33 | 2 张对比表（v3 vs v4、v4 核心概念） |
| 2 | CSS-Based Configuration | 36–66 | 1 段 CSS 代码块（@theme）+ 1 张表 |
| 3 | Container Queries (Native v4) | 69–93 | 3 张表 |
| 4 | Responsive Design | 96–113 | 1 张断点表 + 3 步移动优先列表 |
| 5 | Dark Mode | 117–133 | 2 张表（策略 + 模式示例） |
| 6 | Modern Layout Patterns | 137–158 | 2 张表 + 1 条 note |
| 7 | Modern Color System | 161–178 | 2 张表（格式对比 + 三层令牌架构） |
| 8 | Typography System | 181–200 | 2 张表（字体栈 + 字号） |
| 9 | Animations and Transitions | 203–222 | 2 张表 |
| 10 | Component Extraction | 225–242 | 2 张表（提取信号 + 方法） |
| 11 | Anti-patterns | 245–254 | 1 张 Don't/Do 表 |
| 12 | Performance Principles | 258–265 | 1 张表 |
| 结尾 | Remember blockquote | 269 | 1 行总结 |

### 3.2 必需章节

对照 SKILL-SPEC §3.1 的三必需节逐一核查：**全部缺失**。

- **Workflow/Process**：无。全文没有任何"step by step 做什么"的章节，12 节全是陈述性知识（what），无一节是过程性指导（how to do）。
- **Output Format**：无。没有描述"用户最终得到什么、产出长什么样"的内容。SCORING 中 OUT-01（组件提取 3+ 次规则）与 OUT-02（字体栈）有可评估的输出行为，但 body 没有给出任何输出形态示例（如完成的 HTML/CSS 片段）。
- **Scope/Limitations**：无。未声明"本技能不做什么、何时不该用"（例如：不覆盖 Tailwind v3 项目迁移、不适用于非 Tailwind 的 CSS 框架、不处理 JS 交互逻辑等）。

这三项是 SKILL-SPEC 的硬性要求（"All 322 skills MUST conform"），第 11 节 checklist 12 项中对应第 8/9/10 项，本技能 3 项全挂。这也是 stub 中"纯参考无 Workflow/Output/Scope"评语的直接来源，经逐行核验**属实**。

### 3.3 内容委托

零委托。全部内容内联于 SKILL.md，无任何相对路径引用（正文中不存在 `references/`、`scripts/` 字样）。对 ≤600 行硬限制而言合法，但与 §3.2 的 mindset 目标行数（~50 行）严重不符——264 行是目标值的 5 倍以上（详见 3.5）。

### 3.4 层级编号

- 编号体系为 `## 1.`–`## 12.` 连续、无跳号、无重复；每节内 `###` 子节命名一致（`### What Changed from v3`、`### Theme Definition`、`### Breakpoint vs Container` 等）。
- **结构性观察**：编号 1–12 是"主题编号"而非"流程编号"。编号章节的语义通常暗示步骤顺序，而本技能 12 节为并列参考主题，交换顺序不影响理解。编号与内容类型的语义错配是"伪流程感"来源——若补 Workflow 节（见 §13），建议将现有编号改为无编号主题组（如 `## Theme` 风格的语义标题），避免与真正的工作流编号冲突。

### 3.5 长度合规

- 硬限制：body 264 行 ≤ 600 ✓（dossier 记 269 行，差异为计行口径——dossier 可能计入 frontmatter/空行；以实际内容行 263–264 为准）。
- 模式目标：SCORING 声明 `pattern: mindset`，SKILL-SPEC §3.2 给 mindset 的目标是 ~50 行。264 行约为目标的 5.3 倍，是**声明模式与内容形态的显著失配**。12 节知识表更接近 Tool 型（~300）或参考手册形态。两条出路（详见 §13）：a) 改声明 pattern 为更匹配的类型；b) 将 §3–§12 的细节表迁入 `references/`，body 瘦身并补三必需节。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接

无步骤可衔接——12 节为并列知识主题，节间无"上一节输出作为下一节输入"的依赖链。对"参考手册"定位而言这一结构自洽；对"技能"定位而言则是缺失行为定义的直接体现（与 3.2 同源问题）。节内局部衔接良好：例如 §4 的移动优先 3 步列表（第 111–113 行）顺序正确（先写无前缀基础样式，再加前缀覆盖），第 113 行示例 `w-full md:w-1/2 lg:w-1/3` 与文字描述一一对应。

### 4.2 内部矛盾

经逐表比对，发现 4 处实质矛盾或框架错配，全部指向同一根因：**v3 心智模型被投射到 v4 内容上**（与 dossier 评语一致，此处逐一落到行号）：

1. **静态间距尺度 vs v4 动态间距**（第 48–51 行 vs 第 21 行）：§2 示例定义 `--spacing-xs: 0.25rem; --spacing-sm: 0.5rem; --spacing-md: 1rem; --spacing-lg: 2rem;`。v4 的默认间距机制是**动态乘法尺度**：单一 `--spacing: 0.25rem` 基数 + `calc(var(--spacing) * N)`，任意整数 N（`mt-13`、`gap-7`）无需配置即可用。此处展示的 xs/sm/md/lg 命名静态尺度：(a) 与默认数值完全重复（xs=mt-1、sm=mt-2、md=mt-4、lg=mt-8），是纯冗余别名；(b) 暗示"间距是离散命名刻度"的 v3 心智，与同文件 §1 第 21 行宣称的 v4 "Native, always on" 全新引擎框架自相矛盾。正确 v4 示例应为 `--spacing: 0.25rem;`（如需扩展自定义值再用 `--spacing-18: 4.5rem` 这类数值键）。
2. **Dark Mode 策略表是 v3 配置概念**（第 121–125 行）：表中 `class` / `media` / `selector` 三行正是 v3 `darkMode: 'class' | 'media' | ['selector', ...]` 配置选项的直译。v4 中这些配置项**不存在**，自定义策略的唯一机制是 CSS 级 `@custom-variant` 指令（如 `@custom-variant dark (&:where(.dark, .dark *));`）。表内第三行标注"Custom selector (v4)"尤其误导——v4 没有 `darkMode: 'selector'` 配置，该概念是 v3.4 引入的。全文 264 行未出现一次 `@custom-variant` 字样，对一份自称 "v4" 的暗色模式章节而言是最大的机制性缺漏（后续第 129–133 行示例 `dark:bg-zinc-900` 等默认 `dark:` 变体在未配置时仅跟随系统偏好，与表中"class 策略手动切换"的行为描述无法对应）。
3. **"PostCSS Plugin" 归入 v3 遗产**（第 20 行）：v4 仍官方提供 `@tailwindcss/postcss` 插件（依赖 PostCSS 的工程是 v4 支持的一等使用方式），并非被 Oxide 取代的 v3 遗留物。"Oxide engine" 是 v4 的默认编译路径（Vite 等场景）正确，但将 PostCSS 一刀切标记为 legacy 是事实性简化。
4. **"JIT Mode | Native, always on"（第 21 行）**：方向正确（v4 恒开 JIT 且无开关概念），但表头框架把 v3 的配置概念（"JIT Mode"）直接映射到 v4，属于"v3 概念应用于 v4"的框架残留——dossier 原文即指出此点。表述上应为 "Content detection | Built-in, always on" 之类，避免暗示 v4 有可开关的 JIT 模式。

另有 1 处轻微不精确：§3 标题 "Container Queries (Native v4)"（第 69 行）——容器查询自 v3.2 起已内建（无需插件），并非 v4 独有特性；"Native in v4" 的准确含义是 v4 中更彻底的原生化，建议标题改为 "Container Queries" 或加注 "built-in since v3.2"。

### 4.3 代码正确性

- 第 40–57 行 `@theme` 代码块：语法上完全合法（v4 的 `@theme` 指令、`--color-*`/`--font-*` 命名空间正确，oklch() 值合法，注释使用 `/* */` 正确）。问题仅在间距尺度的策略层面（见 4.2-1），非语法错误。该块也是全文件唯一的真实代码片段，其余均为类名表格。
- 第 153 行 `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]`：arbitrary value 语法正确（v4 对 `[]` 内空格用下划线转义——此处 repeat() 内部无空格、minmax 内部无空格，恰好不需要下划线，正确）。
- 第 155 行 `grid grid-cols-[auto_1fr]`：下划线转义空格，正确。
- 第 84 行 `@container/card`：v4 命名容器语法正确。
- 第 221 行 `hover:scale-105 transition-transform`：正确。
- 第 131–133 行暗色示例：类名本身合法，但如 4.2-2 所述，其行为依赖未给出的 `@custom-variant` 配置，示例完整度不足。
- 断点表（第 102–107 行）数值全部正确：sm 640px、md 768px、lg 1024px、xl 1280px、2xl 1536px（v4 默认为 40/48/64/80/96rem，换算一致）。
- 字号表（第 195–199 行）数值全部正确：text-xs 0.75rem、text-sm 0.875rem、text-base 1rem、text-lg 1.125rem、text-xl 1.25rem。
- 结论：**没有一条错误代码语法**，全部正确性缺陷集中在"策略/机制过时"层面，而非代码层面。

### 4.4 条件完整性

- §2 第 59–65 行 "When to Extend vs Override" 表：给出 3 行（Extend/Override/Semantic tokens），但"何时 Override"仅写 "Replace default scale completely"，缺决策判据（如"仅当需要整体替换尺度时；局部加值一律 Extend"）。条件描述完整度中等。
- §6 第 157 行 note "Prefer asymmetric/Bento layouts over symmetric 3-column grids"：未给例外条件（何时对称网格更合适），与 SCORING PRI-03 的措辞 "where appropriate" 相比，body 的条件限定反而更弱——评测量表比技能正文更严谨，属于可改进点。
- §11 反模式表全部为无例外断言（"Arbitrary values everywhere"、`!important`、Inline `style=`），符合"Specific NEVER rules"的规范偏好 ✓。
- 其余表格（断点、容器查询、动画、提取信号）条件完整度良好。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

Body 中**零引用**（无 `references/`、`scripts/`、`assets/` 相对路径），故引用矩阵为空集，无悬空引用、无路径拼写错误可查。SCORING.yaml 与 check.py 未引用任何外部文件（check.py 仅 import `_shared/checker` 库，属语料共享基础设施，路径 `../_shared` 由 runner 约定，与技能本体无关）。

### 5.2 不可见资源

无。技能不依赖任何未随目录分发的外部资源（无字体、无图片、无 CDN 链接、无网络依赖）。自包含性良好——这在纯知识型技能中是优点。

### 5.3 Reference审查

目录不存在 `references/`。评估：就当前 264 行 body 而言，若能拆分（见 §13），建议将 §3–§12 的 9 张细节表迁入 `references/patterns-cheatsheet.md` 一类文件，body 保留 v4 架构总览 + Workflow + Output + Scope。但该迁移为 🟢 优化级，非缺陷——硬限制 600 行未触发。

### 5.4 Scripts审查

目录不存在 `scripts/`。技能无自动化工件需求（知识型），合理。注意 `check.py` 位于技能根目录而非 `scripts/`，这与语料 runner 的固定约定有关（runner 调用 `<skill>/check.py`），保持现状 ✓。

### 5.5 跨Skill引用

正文中未出现任何 `../other-skill/` 相对引用，也未以 prose 形式提及其他技能名（SKILL-SPEC §3.3 允许 "see also: <skill-name>" 的散文引用，本技能连散文引用也没有）。无违规，但也没有为相邻技能（如 030 系列的 CSS 或设计系统类技能）建立上下文桥接——🟢 级增强项。

### 5.6 嵌套/死文件

目录仅 4 个文件，无嵌套目录、无孤儿文件、无 .bak/.tmp 残留、无未使用的检查文件。check.py 与 SCORING.yaml 的检查项一一对应（见 §10），无死代码。

### 5.7 其他资源

无 assets/、无二进制、无许可证文件——知识参考型技能不需要。唯一可议点是 SKILL-SPEC §1.3 建议"有价值的元信息放 body 末尾 `## Metadata` 节"，本技能无版本/作者/许可证元信息需求，缺 Metadata 节不算缺陷。

---

## 6. 语法与格式质量

### 6.1 拼写

全文扫描未发现拼写错误。类名（`grid-cols-[auto_1fr]`、`dark:border-zinc-700`）、函数名（`repeat(auto-fit,minmax(250px,1fr))`）、色值（`oklch(0.7 0.15 250)`）逐一核验无误。字体名 'JetBrains Mono'、'Outfit'、'Poppins' 拼写正确。

### 6.2 语法

- 表格语法：13 张表全部 Markdown 表格结构完整（表头分隔行、列数对齐）。抽查第 17–23 行表：表头 `| v3 (Legacy) | v4 (Current) |` 与分隔行 `|-------------|-----------|` 列数一致（2 列）；所有行 2 列无错位。第 100–107 行断点表 3 列对齐正确。**未发现任何破损表格**——这与 dossier "语法干净、良好表格化" 的评价一致。
- 代码块：第 40–57 行唯一代码块，fenced 语法（```）正确配对。
- 列表：第 111–113 行有序列表编号 1/2/3 连续 ✓（无 029/030 批次出现的列表编号破损问题——该问题不适用于本技能）。

### 6.3 混杂

中英混排自然：全英文正文，无乱码、无编码损坏、无全角/半角符号混用问题（对比批次内其他技能出现的杂散 `**` artifact，本技能全文干净）。文件编码 UTF-8 正常。

### 6.4 Markdown

- 层级结构：`#` 标题 1 个（第 7 行）、`##` 12 个、`###` 子节若干，层级单调但一致。
- blockquote 使用规范：第 9 行引言、第 157 行 note、第 269 行 Remember 均使用 `>` 且语义恰当（第 269 行是全文唯一的"行动号召"式收尾，与纯参考定位匹配）。
- 加粗使用克制且一致（表格内首列概念词加粗，如第 175–177 行 Primitive/Semantic/Component）。
- 无裸 URL、无错误嵌套的斜体/代码标记。Markdown 质量整体优秀。

### 6.5 占位符

全文无 `{placeholder}`、`<example>`、`TODO`、`XXX`、`...`（省略号滥用）类残留。所有示例均为真实可用的类名/代码。第 44 行 `oklch(0.7 0.15 250)` 与第 45–46 行 `oklch(0.98 0 0)` / `oklch(0.15 0 0)` 数值真实有效，非示意占位。

### 6.6 截断

无截断迹象：第 270 行后文件自然结束（末尾空行），第 269 行 blockquote 完整收尾（"The config file is now optional." 句末句号齐全）；所有表格在各自节内完整闭合。SCORING.yaml 与 check.py 亦无截断（SCORING 第 131 行 CF-02 完整、check.py 第 74 行 `main()` 标准入口完整）。

---

## 7. 规范合规性（SKILL-SPEC.md 12项清单）

对照 SKILL-SPEC 第 5 节 checklist 逐项核验：

| # | 检查项 | 结果 | 依据 |
|---|--------|------|------|
| 1 | name 小写+连字符、≤64、匹配目录 | ⚠️ | `tailwind-patterns` 合法；与 `031-tailwind-patterns` 差 NNN 前缀，属全语料惯例（见 2.1） |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✅ | 约 280 字符，结构完整（见 2.2） |
| 3 | description 无命令式/第一/第二人称 | ✅ | 无违规句式 |
| 4 | description 无跨技能路由 | ✅ | 无 "NOT for X" 类语句 |
| 5 | description 含触发信号短语 | ✅ | "Use when the user asks to…" |
| 6 | frontmatter 无禁止键 | ✅ | 仅 name/description/allowed-tools |
| 7 | body ≤600 行 | ✅ | 264 行 |
| 8 | body 含 workflow/process 节 | ❌ | **缺失**（全文无过程性章节） |
| 9 | body 含 output format 节 | ❌ | **缺失** |
| 10 | body 含 scope/limitations 节 | ❌ | **缺失** |
| 11 | body 无跨技能文件引用 | ✅ | 零引用 |
| 12 | 目录 NNN-kebab-case、无空格大写 | ✅ | `031-tailwind-patterns` |

**结果：12 项中 9 项通过、3 项不通过**（全部集中在三必需节）。合规性的唯一结构性缺陷就是三节全缺——这是本技能从"良好参考"降级为"不合规技能"的单一原因，其余 9 项全部干净。

---

## 8. 人机感评估

### 8.1 Emoji

全文（SKILL.md / SCORING.yaml / check.py）**零 emoji**。SCORING.yaml 第 6、31、64、89、106 行注释使用 `──` 装饰线（如 `# ── Scope (3 items) ──`），属 ASCII 分隔装饰，非 emoji，风格统一且不干扰解析。

### 8.2 全大写

正文中大写词仅技术术语：`OKLCH`（第 44、167 行）、`JIT`（第 21 行）、`PostCSS`、`Bento`（第 154、157 行）。无呐喊式 ALL CAPS 短语，无强调性大写滥用 ✓。

### 8.3 语气

通篇中性参考语气（dossier 评语"中性参考语气，无 emoji 或对话填充"经核验属实）。第 269 行 "**Remember:** …" 是唯一带指导色彩的句子，但以引用形式呈现，克制适度。无感叹号、无反问、无拟人化表达。SCORING 的 judge 问题（如第 28 行 "Does the agent apply the pattern category matching the scenario…"）为机器评估措辞，语气中性。

### 8.4 人机边界

技能以"知识速查"形式呈现，无对话性引导（无"你可以""请记住"类句式），无虚假交互。SCORING 与 body 之间无"暗示答案"的泄漏——评测量表基于行为提问而非复述正文，人机边界清晰。

### 8.5 人称

正文零第一/第二人称（无 I/we/you）。第 124 行 "No user control" 中 "user" 指应用使用者（系统偏好场景），是领域术语而非对话人称 ✓。description 中 "the user" 为规范模板要求，合规。

### 8.6 表格密度

全文 13 张表覆盖约 150 行，表格密度极高、散文密度极低（无叙事段）。对"模式速查手册"这一体裁，高表格密度是**恰当**的——速查型内容用表是正解，且所有表格都有真实功能（对照、映射、决策），无凑数表格。唯一的格式性问题是：极端的表格化导致全文没有任何一段可读的流程性叙述，这与三必需节缺失互为表里（§4.1 同源）。

---

## 9. 可执行性评估

### 9.1 独立可执行性

- 作为**知识查询资源**：独立可用。Agent 读取后可回答"v4 断点默认值""Bento 布局类名""令牌三层架构"等事实查询，正确率高（除 §4.2 的 4 处 v3 残留外，事实准确率约 90%+）。
- 作为**技能（skill）**：执行性弱。没有 Workflow 就没有"被调用后做什么"的行为契约；没有 Output Format 就无法约束产出形态——SCORING 的 OUT-01（组件提取）要求行为，而 body 只给了"何时提取"的信号表，没有"提取成什么样"的产物定义。独立可执行性评分：**中等偏弱**。

### 9.2 步骤可操作性

零步骤。全文唯一的"步骤"是第 111–113 行的移动优先 3 步，且它是设计原则而非技能执行步骤。其余均为事实陈述。若要恢复可操作性，需要新增流程节（见 §13 的 🔴-01 修复）。

### 9.3 工具依赖

allowed-tools 5 个文件工具与内容匹配（知识查询只需 Read/Glob）。无 Bash 意味着技能无法指导 agent 实际构建/编译 Tailwind 工程（如运行 `npx @tailwindcss/cli` 验证配置）——若补 Workflow 时加入验证步骤需扩展工具白名单。无 MCP/外部服务依赖，离线可用 ✓。

---

## 10. SCORING.yaml 交叉参考

### 10.1 结构与计数

- 声明 `total_items: 14`（第 3 行），实际文件包含 **12 条 criteria + 2 条 critical_failures = 16 个条目**。若口径为"仅 criteria"，12 ≠ 14；若口径为"全部条目"，16 ≠ 14。3+4+3+2+2=14 恰好等于 category 分组的行数之和，说明 `total_items` 疑似误写为"分组条数和"，与文件实际条目数（16）不符。需对照语料其他技能确认口径（建议统一为"criteria + critical_failures 总数"，即 16）。
- judge 分布：llm 10 项（SCOPE-01/03、DEC-01~04、PRI-02/03、OUT-01/02、NEG-01/02）、script 2 项（SCOPE-02、PRI-01）。**critical_failures CF-01/CF-02（第 123–130 行）无 judge 字段**——若语料惯例是 CF 默认 llm 评估，建议显式标注 `judge: llm` 以免 runner 解析歧义。

### 10.2 与 Body 的映射完整性

12 条 criteria 在 body 中**全部有对应章节**，映射良好：

| Criterion | Body 依据 | 一致性 |
|-----------|-----------|--------|
| SCOPE-02（无 tailwind.config.js） | §11 第 253 行 "Mix v3 config with v4 → Migrate fully to CSS-first" | ✅ |
| DEC-01（断点 vs 容器查询） | §3 第 73–77、86–92 行 | ✅ |
| DEC-02（暗色策略匹配） | §5 第 121–125 行 | ⚠️ 表内容本身 v3 过时（4.2-2），但策略三分法与评分意图一致 |
| DEC-03（三层令牌架构） | §7 第 173–177 行 | ✅ |
| DEC-04（移动优先） | §4 第 109–113 行 | ✅ |
| PRI-01（@theme 语义令牌） | §2 第 40–57 行 | ✅ 示例完全匹配正则 |
| PRI-02（OKLCH 优先） | §7 第 163–169 行 | ✅ |
| PRI-03（Bento 优先） | §6 第 157 行 | ✅ |
| OUT-01（3+ 次提取） | §10 第 231–241 行 | ✅ |
| OUT-02（推荐字体栈） | §8 第 185–189 行 | ✅ |
| NEG-01（禁 arbitrary+!important） | §11 第 249–250 行 | ✅ |
| NEG-02（禁混 v3/v4、禁重 @apply） | §11 第 253–254 行 | ✅ |

评分表与技能内容的高一致性是本技能少有的强项——修复 body 时只需保证新增 Workflow/Output/Scope 节不破坏上述映射即可。

### 10.3 脚本检查（check.py）审查

- 入口与运行协议（第 1–5 行 docstring、第 54–59 行 argv 校验）符合语料 runner 约定，用法说明清晰。
- 实现的 2 个 script 检查：
  - `SCOPE-02`（第 35 行）：`tool_log_not_contains(r"tailwind\.config\.js|tailwind\.config\.ts|@tailwindcss/v3")` — 正则转义正确、无锚定（搜索工具日志全文）、无大小写陷阱（v3 字样全小写出现）。合理。
  - `PRI-01`（第 42 行）：`output_contains(r"@theme|--color-|--spacing-|--font-")` — 四项交替，可匹配 §2 示例中任何令牌。
- **发现 3 个问题**：
  1. **docstring 计数不符**：第 20 行注释 "Run all 3 script checks"，实际仅 2 个 script 检查（SCOPE-02、PRI-01），第 34–49 行注释也印证其余均为 llm。注释与实现差 1，应改为 "2"。
  2. **PRI-01 与 v4 修复的耦合**（重要）：正则需要字面 `--spacing-`（连字符结尾）。若按 §13 修复建议将 §2 间距示例改为纯 v4 动态写法（仅 `--spacing: 0.25rem` 基数，无 `--spacing-*` 命名键），一个"完全正确"的 agent 输出将**无法命中该正则而误判失败**（`var(--spacing)`、`--spacing:` 均不含 `--spacing-`）。当前技能自身的示例恰好命中正则，掩盖了该问题。修复间距示例时须同步把正则放宽为 `--spacing`（去掉尾部连字符）或增加 `calc\(var\(--spacing` 分支。
  3. **重复加载逻辑冗余**（第 21–29 行 vs 第 62–64 行）：`check()` 内再次判断 `os.path.exists(agent_output)` 与 `main()` 的预加载逻辑重叠。无害但可读性可优化——建议二选一。
- **缺失项**：CF-01/CF-02 声明为 cap_to_0 的致命失败，但均无脚本检测，全依赖 llm 判断（第 49 行注释确认 NEG-01/02 不在此处检查）。CF-01（生成 tailwind.config.js）与 SCOPE-02 的正则几乎同源，若 CF 由脚本判定将大幅提升检测确定性——建议给 CF-01 增加 `judge: script` + 相同正则在输出上的检查（tool_log 与 output 双检测）。

### 10.4 分级与 effect 字段

CF 使用 `cap_to_0`（第 126、130 行），与语料中"致命失败封顶 0 分"的语义一致。无 `reduce` 等其他 effect 用法。分级粒度（14+2 项）对该技能覆盖面充分。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 第 283–288 行的 Batch 026-050 段落记录原文（关键句）：

> - **逻辑**: 内部一致但 dark-mode 策略表和 "JIT always on" 框架是 v3 概念应用于 v4，`--spacing-xs` 风格自定义比例与 v4 动态间距默认值矛盾。
> - **语法**: 干净、良好表格化、可读。
> - **人机感**: 中性参考语气，无 emoji 或对话填充。
> - **合规**: Description 第三人称含触发，但 body 是纯知识参考——无 workflow、无 output-format、无 scope 节；269 行 ≤600。
> - **总评**: 🟡 有用参考但结构不合规（缺全部三必需节），v4 细节稍有过时。

本审查逐行核验结论：dossier 四条评语**全部属实且可精确定位**——"dark-mode 策略表 v3 残留"对应第 121–125 行、"JIT always on 框架"对应第 21 行、"--spacing-xs 矛盾"对应第 48–51 行、"三必需节全缺"经 §3.2 全文件扫描确认。dossier 之外，本审查新增发现 4 处 dossier 未记录的问题：check.py docstring 计数错误（3 vs 2）、PRI-01 正则与 v4 修复的耦合风险（10.3-2）、SCORING `total_items` 计数口径歧义（10.1）、CF 缺 judge 字段（10.1）。另对 §3 标题 "Native v4"（容器查询 v3.2 已内建）与 §1 "PostCSS Plugin" 归 v3（v4 仍有官方 PostCSS 插件）两处事实性简化做了补充定位。

---

## 12. 综合评分（8维度加权+评级）

按 8 个维度加权评分（每维 0–100，权重合计 100%）：

| 维度 | 权重 | 得分 | 依据摘要 |
|------|------|------|----------|
| 规范合规性（三必需节） | 25% | 30 | 12 项 checklist 9/12 通过，但三必需节全缺是硬性缺陷；其余 9 项干净 |
| 内容准确性与时效性 | 20% | 60 | 断点/字号/语法代码全部正确；4 处 v3 概念投射 v4（间距、暗色、PostCSS、JIT），缺 @custom-variant 关键机制 |
| 逻辑一致性（内部自洽） | 10% | 60 | 12 节主题自洽、SCORING↔body 映射强；失分集中在间距策略与暗色示例的自相矛盾 |
| 语法与格式质量 | 10% | 90 | 13 张表全部结构完整、代码块规范、无占位符/截断/拼写错误，批次内上游水准 |
| 人机感 | 10% | 85 | 零 emoji、零人称、中性参考语气、术语大写克制；仅"过度表格化致无叙事"微瑕 |
| 可执行性 | 10% | 50 | 知识查询可用性高；无 Workflow/Output 行为契约，独立作为"技能"执行性弱 |
| SCORING/check 质量 | 10% | 75 | 12 criteria 全映射、CF 分级正确；扣分项：total_items 口径、CF 无 judge、docstring 计数、PRI-01 正则耦合 |
| 完整性/资源组织 | 5% | 60 | 自包含、零死文件；无 references 拆分、264 行与 mindset 目标 50 行失配 |

**加权合计**: 30×0.25 + 60×0.20 + 60×0.10 + 90×0.10 + 85×0.10 + 50×0.10 + 75×0.10 + 60×0.05 = 7.5 + 12 + 6 + 9 + 8.5 + 5 + 7.5 + 3 = **59/100**

**评级: 🟡 C+**（与 dossier 及原 stub 评级一致；stub 记 42/100，本审查重算为 59/100，差异主要源于两点：a) 本审查将"语法格式 90 分、人机感 85 分"的高质量计入权重——这批文件在 322 个技能中格式层属上游水平；b) 合规权重 25% 而非默认更高。若按"规范一票否决"的严口径将合规权重提到 40%，总分将回落到约 50 分区间。两口径评级均为 🟡，结论稳定。）

**一句话总评**: 一份内容扎实、格式优秀、但结构不合规且含 4 处 v3/v4 混淆的"半成品参考手册"——修好三必需节与 v4 机制细节后，可望升为语料中的优质参考型技能。

---

## 13. 修复建议（按优先级分层）★ 重点 ★

### 🔴 致命（必须先修，共 2 项）

**🔴-01 补齐三必需节（Workflow / Output / Scope）——结构性缺陷，规范硬性要求**
- 问题：SKILL-SPEC §3.1 的三必需节全部缺失（详见 §3.2），checklist 12 项中 3 项不通过，是降级为 C+ 的唯一主因。
- 建议在现有 12 节**之前**插入 `## Workflow`、`## Output Format`、`## Scope` 三节（或置于第 12 节之后、Remember 之前），要点：
  - **Workflow**（建议 15–25 行）：给出调用本技能后的执行序列，例如：① 确认项目 Tailwind 版本（v4 工程用 CSS-first，v3 工程明确拒绝并引导迁移）；② 按场景路由——响应式→§4、暗色→§5、容器查询→§3、令牌→§2/§7、动效→§9；③ 输出类名/配置前对照 §11 反模式自查；④ 重复 3+ 次的类组合按 §10 提取。用决策树或路由表呈现（SKILL-SPEC §3.4 偏好 decision tree）。
  - **Output Format**（建议 10 行）：定义交付物形态——修改后的 HTML 类名片段、`@theme` CSS 块、或组件提取后的 JSX/CSS 代码，并附 1 个最小完整示例（当前全文无任何完整输出示例，SCORING OUT-01/OUT-02 无对应行为锚点）。
  - **Scope**（建议 8–12 行）：声明不做什么——不覆盖 Tailwind v3 项目（要求迁移）、不覆盖 Tailwind 之外的 CSS 框架、不处理 JS 交互逻辑、不指导构建工具安装配置。
- 工作量估计：1–1.5 小时（含示例代码编写与验证）。

**🔴-02 重写 Dark Mode 章节——事实性错误（v3 配置概念冒充 v4）**
- 问题：第 121–125 行策略表是 v3 `darkMode:` 配置选项的直译，且第三行 "Custom selector (v4)" 指向 v4 中不存在的配置方式；第 129–133 行示例未说明默认 `dark:` 变体需 `@custom-variant` 才能实现表中描述的 class 切换行为。全文 264 行未出现一次 `@custom-variant`——对 v4 技能而言这是最严重的机制缺漏。
- 建议重写为：默认行为（跟随系统 `prefers-color-scheme`）→ `@custom-variant dark (&:where(.dark, .dark *));` 手动切换 → 自定义选择器（`[data-theme]`）→ 多主题变体示例。删去 `class`/`media`/`selector` 三行 v3 框架，替换为 v4 的 `@custom-variant` + 变体名语法。
- 工作量估计：30–45 分钟。

### 🟡 重要（建议修复，共 4 项）

**🟡-01 修正 §2 间距示例为 v4 动态尺度**
- 问题：第 48–51 行 `--spacing-xs/sm/md/lg` 静态命名尺度与 v4 动态乘法间距（`--spacing` 基数 + `calc`，任意整数可用）矛盾且数值冗余（等价 mt-1/2/4/8）。
- 建议：示例改为 `--spacing: 0.25rem;`（可加注释说明动态机制），如需展示自定义再写 `--spacing-18: 4.5rem` 这种数值键。
- **联动**：修复后必须同步调整 `check.py` 第 42 行 PRI-01 正则——当前 `--spacing-`（带尾部连字符）在纯动态写法下无法命中（详见 §10.3 问题 2），应放宽为 `--spacing` 或增加 `var\(--spacing` 分支，否则修复会直接制造新的评测误判。
- 工作量估计：20 分钟（含正则联动）。

**🟡-02 修正 §1 架构表中 2 处 v3 框架残留**
- 第 21 行 "JIT Mode | Native, always on"：v4 无 JIT 开关概念，建议改为 "Content detection | Built-in, always on" 之类，去掉 v3 配置模式名词。
- 第 20 行 "PostCSS Plugin" 整行归 v3 遗产系误述：v4 仍官方支持 `@tailwindcss/postcss`。建议改列为 "PostCSS via @tailwindcss/postcss | Optional, still supported"，或加注"多数新工程使用 Oxide 默认路径"。
- 工作量估计：15 分钟。

**🟡-03 补齐 v4 关键机制覆盖**
- 当前 12 节覆盖广度尚可，但缺 3 个 v4 高频机制：`@utility`（自定义工具类，v4 核心）、`@theme inline`（内联求值场景）、`@source`（内容探测源配置）。可在 §2 后新增小节或在 §1 核心概念表（第 27–32 行）中加行，每条 2–3 行即可。
- 另外 §3 标题 "Container Queries (Native v4)"（第 69 行）建议去掉 "v4" 或加注 "built-in since v3.2"，避免 v3 用户误以为需升级才可用。
- 工作量估计：30 分钟。

**🟡-04 解决 pattern 声明与内容形态失配**
- SCORING 声明 `pattern: mindset`（目标 ~50 行），实际 body 264 行、纯知识参考形态。二选一：
  - 方案 A（推荐）：body 瘦身至 ~80–120 行（架构总览 + 三必需节 + 关键示例），把 §3–§12 的 9 张细节表整体迁入 `references/patterns-cheatsheet.md`，Workflow 中引用之——同时满足 mindset 行数目标与"细节委托 references"的规范偏好；
  - 方案 B：维持单文件，但需评估是否改用更匹配的 pattern 声明（如 tool），并确认语料对 mindset 行数的宽容度。
- 工作量估计：方案 A 约 1.5 小时（含 references 文件新建与 body 重排）。

### 🟢 优化（可做可不做，共 5 项）

**🟢-01 SCORING.yaml `total_items` 口径**：第 3 行 `total_items: 14` 与文件实际条目数（12 criteria + 2 CF = 16）不符，疑似误写为分组和。按语料统一口径修正并核对 runner 是否读取该字段。工作量：10 分钟。

**🟢-02 CF 补 judge 字段**：CF-01/CF-02（第 123–130 行）无 `judge` 字段，建议显式 `judge: llm`；另可考虑将 CF-01（tailwind.config.js 生成）改为 `judge: script` 复用 SCOPE-02 同源正则，把致命失败检测从 llm 主观判断提升为确定性检测。工作量：15 分钟。

**🟢-03 check.py 文案与结构**：第 20 行 docstring "Run all 3 script checks" 改为 "2"；第 21–29 行与第 62–64 行的重复加载逻辑二选一精简。工作量：10 分钟。

**🟢-04 小处润色**：description 第 3 行 "dark mode, or design tokens" 的 "or" 位置（改 "dark mode, design tokens, or responsive layouts"）；§2 第 59–65 行 Extend/Override 表补一条 Override 判据；§6 第 157 行 note 补对称网格的例外场景（与 PRI-03 "where appropriate" 对齐）；§12 第 264 行 "10x faster" 加定性表述（如 "markedly faster in large projects"）。工作量：30 分钟。

**🟢-05 跨技能衔接**：以 prose 形式在 Scope 或结尾引用相邻技能（如 CSS 设计系统/色彩类技能）建立上下文桥接——SKILL-SPEC §3.3 允许 "see also: <skill-name>"。工作量：5 分钟。

### 修复后预期

完成 🔴 两项 + 🟡 四项后：checklist 12/12 通过、v4 机制完整、行为契约齐备，评分预计从 59 升至 75–80 区间（🟢 绿区边缘）。全部修复（含方案 A 拆分）总计工作量约 5–6 小时。

---

## 附录: 审查过程记录

- **审查时间**: 2026-08-06（stub 原审查日期 2026-08-05）
- **审查者**: Claude（人工复核流程代理）
- **执行步骤（按 SOP 严格顺序）**:
  1. Glob `**/*` 于 `D:\SkillIF\skill-experiment\complex-skills\031-tailwind-patterns\` → 4 个文件，无子目录；
  2. 全量读取 SKILL.md（270 行）、SCORING.yaml（131 行）、check.py（74 行）、REVIEW.md stub（7 行），逐一全文分析；
  3. 读取 `D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md`（162 行，12 项 checklist、三必需节、frontmatter 规则）；
  4. 检索 `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` 的 Batch 026-050 段，取得 031 条目（第 283–288 行）并逐条核验；
  5. 撰写并覆盖写入本 REVIEW.md。
- **核验方法**: 全部 13 张表逐行比对列数与内容；全部 CSS 类名与断点数值对照 Tailwind v4 文档知识校验；SCORING 12 条 criteria 逐一映射 body 行号；check.py 正则逐一手工推导匹配行为（含 PRI-01 在纯动态间距写法下的反例推演）。
- **与 stub 的差异**: stub 7 行、42/100；本审查 59/100，评级一致（🟡 C+）。差异来自权重口径与格式/人机维度加分，已在 §12 说明。
- **文件完整性**: 审查过程未修改 SKILL.md、SCORING.yaml、check.py；仅覆盖写入 REVIEW.md。
