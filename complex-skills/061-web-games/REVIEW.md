# REVIEW: 061-web-games

**审查日期**: 2026-08-06
**Skill 类型**: mindset — 浏览器游戏开发原则（框架选型 / WebGPU / 性能 / 资产 / PWA / 音频）
**Body 行数**: 145 行（wc -l 实测；文件 3,147 字节）
**参考文件数**: references/0, scripts/0, assets/0, 其他/0 — 完全自包含
**Dossier 评级**: 🟢（"简洁准确"）—— 本次复核：**需下修为 🟡**（三必需节全部缺失，dossier 未验证该项；详见第 11 节）
**综合评分**: 🟡 **B (77/100)**

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\061-web-games\
├── SKILL.md      145 行 / 3,147 B / 2026-08-05 17:24   (评测入口)
├── SCORING.yaml  162 行 / 7,518 B / 2026-08-05 15:46   (18 项 criteria + 2 项 critical_failures)
├── check.py       77 行 / 2,729 B / 2026-08-05 16:36   (6 项脚本判定)
└── REVIEW.md       4 行 /   167 B / 2026-08-05 21:07   (旧 stub — 本次审查重写)
```

极简四文件结构。无 `references/`、`scripts/`、`assets/` 子目录，无嵌套 SKILL.md（对比 306-campaign-analytics 的孪生文件问题，本 skill 不存在目录卫生风险）。`SCORING.yaml` 声明 `pattern: mindset`。

145 行 body 承载 7 个原则节（框架选型 → WebGPU → 性能 → 资产 → PWA → 音频 → 反模式）+ 1 条格言式收尾。结构上是一个典型的知识参考型 / 原则备忘单式 skill。

---

## 2. Frontmatter 逐字段审查

### 2.1 `name` 字段（L2）

`name: web-games`。小写 + 连字符，9 字符，远低于 64 字符上限。与目录名 `061-web-games` 的对应关系符合本语料库约定（NNN- 为序列号前缀，spec §4 示例 `281-wcag-accessibility-audit` 即此模式）。**合规**。

### 2.2 `description` 字段（L3）

实测 302 字符（含尾部换行 303），远低于 1024 上限。按 spec §2.1 三问拆解：

- **WHAT**："Web browser game development principles. Framework selection, WebGPU, optimization, PWA." —— 点明技能性质（浏览器游戏开发原则）与四个核心主题（框架选型、WebGPU、优化、PWA），以名词短语开头，符合第三人称要求。
- **WHEN**："Use when the user asks to build a browser game, choose a web game framework (Phaser, PixiJS, Three.js, Babylon.js), use WebGPU or WebGL, or optimize game performance, assets, and audio in the browser." —— 四个具体触发场景（建游戏 / 选框架 / 用 WebGPU 或 WebGL / 优化性能、资产、音频），全部与正文 7 节一一对应。
- **KEYWORDS**：browser game、Phaser、PixiJS、Three.js、Babylon.js、WebGPU、WebGL、performance、assets、audio、PWA —— 领域词密集，四个框架名直接点名，意图匹配能力强。

未出现 imperative / first-person / second-person 开头，无 cross-skill routing 痕迹。触发信号 **"Use when the user asks to..."** 精确命中 spec §2.4 允许句式清单，无 306 那种"Use when analyzing"缺主语的擦边问题。**description 质量在语料库中属上乘，无可修之处。**

### 2.3 `allowed-tools` 字段（L4）

`Read, Write, Edit, Glob, Grep` —— 逗号分隔，属 spec §1.2 允许字段，格式正确。**但缺 Bash**：这是一个需要"做出能在浏览器里跑的游戏"的 skill，`OUT-01` 判定描述为 "Delivered game code runs in the browser without console errors **(executed/verified)**"，`CF-02` 以"游戏在浏览器中运行失败"为清零条件——而允许工具里没有任何运行/验证手段（无 Bash、无 WebFetch）。agent 写完代码无法起本地服务器实测，验证环节只能靠自省。这不是规范违规（allowed-tools 为可选字段），但是**执行语义与评分语义的矛盾**，详见 §9.3 与修复项 F-9。

### 2.4 其他字段

frontmatter 仅 `name` / `description` / `allowed-tools` 三键，无任何 spec §1.3 禁用键。PyYAML 解析通过。**合规**。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Web Browser Game Development                          (L7, 1 行)
> Framework selection and browser-specific principles.  (L9, 引言)
## 1. Framework Selection                               (L13-35)
    ### Decision Tree / ### What type of game? / ### Comparison (2025)
## 2. WebGPU Adoption                                   (L38-56)
    ### Browser Support (2025) / ### Decision
## 3. Performance Principles                            (L58-77)
    ### Browser Constraints / ### Optimization Priority
## 4. Asset Strategy                                    (L79-97)
    ### Compression Formats / ### Loading Strategy
## 5. PWA for Games                                     (L99-114)
    ### Benefits / ### Requirements
## 6. Audio Handling                                    (L116-131)
    ### Browser Requirements / ### Best Practices
## 7. Anti-Patterns                                     (L133-143)
> **Remember:** ...                                     (L145, 收尾格言)
```

### 3.2 必需节映射（spec §3.1）—— 本次审查的核心结论

| 必需节 | 状态 | 判定依据 |
|--------|:----:|---------|
| **Workflow / Process** | ❌ **缺失** | 全文无任何执行序列。决策树是"选型判断辅助"而非"做事流程"；7 节全是原则与表格，没有任何"先做什么、再做什么、最后交付什么"的步骤链 |
| **Output Format** | ❌ **缺失** | 全文从未描述交付物形态：不要求 HTML 文件、不描述工程结构、不说输出长什么样。评分体系（OUT-01 要求 `*.html` 存在、OUT-03 要求 `assets/**/*` 存在）对交付物有明确预期，正文却只字未提 |
| **Scope / Limitations** | ❌ **缺失** | `## 7. Anti-Patterns` 表（L133-143）是"领域实现反模式"（不要全量加载资产等），属于行为禁令，**不是**边界声明——它没有回答"本 skill 不覆盖什么（游戏设计、变现、后端多人、原生引擎、WebXR 等）"与"何时不该用" |

**三必需节全部缺席。** 这正是旧 REVIEW stub 中"需验证三必需节完整性"的验证结论：dossier 评级 🟢 时未检查此项，复核结果为全缺。对比语料库数据，这是最常见的规范缺口（~68% 缺 Scope）的**极端形态**——不是缺一节，而是三节全缺（语料库中约 12 个 skill 属此类：031/041/080/082/183 等，dossier 均判 🟡）。

### 3.3 §1 Framework Selection（L13-35）—— 内容最扎实的一节

决策树（L17-25）四分支：2D 全引擎 → Phaser、2D 纯渲染 → PixiJS、3D 全引擎（物理/XR）→ Babylon.js、3D 纯渲染 → Three.js、Hybrid/Custom → 裸 Canvas/WebGL。"Comparison (2025)" 表（L30-35）给出 Phaser 4 / PixiJS 8 / Three.js / Babylon.js 7 的定位。树与表相互印证，判据可裁决（"要物理和 XR → Babylon"），是语料库中少见的"真决策树"。与 SCORING 的 SCOPE-02 精确对应。仅两处小问题：标题层级并列（L15/L17，见 §4.3）；Hybrid 分支漏 raw WebGPU（见 §4.2）。

### 3.4 §2 WebGPU Adoption（L38-56）—— 事实准确的判断原则

浏览器支持表（L43-49）：Chrome/Edge v113（2023-04 起）、Firefox v131（2024-10 起）、Safari 18.0（2024-09 起）、全球 ~73%——逐一核验与官方支持时间线相符（Firefox 131 于 2024 年 10 月启用 WebGPU，Safari 18 于 2024 年 9 月推出），"~73% 全球覆盖"为 2025 年合理估计值。决策规则三条（L52-54）：新项目 WebGPU + WebGL fallback、旧项目 WebGL 起步、特性检测 `navigator.gpu`——与 DEC-01 判定完全一致，也是 CF-01 的唯一防误触机制。

### 3.5 §3 Performance Principles（L58-77）—— 显式排序是本 skill 最强的执行锚点

浏览器约束表（L62-68）五条：无本地文件访问→打包/CDN、标签页节流→隐藏时暂停、移动数据→压缩资产、音频自动播放→需用户交互。优化优先级（L72-76）显式 1-5 排序：资产压缩 → 懒加载 → 对象池 → 绘制调用批处理 → Web Worker。**这个排序是全文唯一带硬序号的执行指令**，与 DEC-02 判定的顺序要求逐字对应，agent 无需自行推断。

### 3.6 §4 Asset Strategy（L79-97）

压缩格式表（L83-87）：纹理 KTX2+Basis Universal、音频 WebM/Opus（MP3 兜底）、3D 模型 glTF+Draco/Meshopt——与 DEC-03 判定对应。加载阶段表（L91-95）：启动核心资产 <2MB、游戏流式加载、后台预取下一关——与 PROC-02 对应。缺憾：正文从未说明交付物应包含 `assets/` 目录（OUT-03 判定的前置条件），见 §9.2。

### 3.7 §5 PWA for Games（L99-114）

收益 4 项（离线、安装到主屏、全屏、推送）+ 需求 3 项（service worker 缓存、web app manifest、HTTPS）。与 PROC-03 判定对应。**但正文用的是口语词**："Service worker for caching"（带空格）、"Web app manifest"——而 PROC-03 的正则要求 `serviceWorker`（无空格）或 `manifest.json` 字面量。正文与判据之间隔着一次"agent 联想到 API 名"的推断，见 §9.2。

### 3.8 §6 Audio Handling（L116-131）

浏览器要求 3 条（L119-121）：音频上下文需用户交互、首次点击/触摸时创建 AudioContext、挂起时恢复。与 DEC-04 判定对应。同样无代码示例——"Create AudioContext" 与 `new AudioContext()` 之间靠 agent 的 API 常识补齐。对 mindset skill 而言"知识增量优先于复述"（spec §3.4）是可辩护的，但代价是脚本判定的稳定性（见 F-5/F-13）。

### 3.9 §7 Anti-Patterns（L133-143）

5 行 Don't→Do 表：全量加载资产→渐进加载、无视标签页可见性→隐藏时暂停、阻塞音频→懒加载音频、跳过压缩→全部压缩、假设高速连接→处理慢网络。全部可执行，与 NEG-01/NEG-02 一一对应，是"Anti-patterns over generic advice"原则的正面范例。**注意**：本节的"隐藏时暂停"与 §3 的"Pause when hidden"一样，都没有点名 Visibility API（`visibilitychange`/`document.hidden`），PROC-05 判定完全依赖 agent 自行联想。

### 3.10 收尾格言（L145）

"> **Remember:** The browser is the most accessible platform. Respect its constraints." —— 略带格言腔但语义准确（浏览器约束是全篇主线），dossier 判"可接受"，本次复核维持该判定。

---

## 4. 逻辑一致性深度审查

### 4.1 正文 ↔ SCORING ↔ check.py 三链一致性

本 skill 的写作是自觉的：7 个原则节与 18 条判据的映射近乎一一对应（详见 §10.1 全表）。决策树 → SCOPE-02、优化优先级 → DEC-02、格式表 → DEC-03、音频要求 → DEC-04、约束表 → PROC-01、加载阶段 → PROC-02、PWA 需求 → PROC-03、反模式表 → NEG-01/02——映射覆盖率 100%，链条上无自相矛盾。这是"正文能指导评测"的正面案例，与 306 的结论类似但更干净。

链条衰减仅发生在**脚本判定与正文的锚点强度**上（§9.2），而非事实层面。

### 4.2 决策树与 §2 的张力：Hybrid/Custom 分支漏掉 raw WebGPU

L24-25 的第三分支 "Hybrid / Canvas → Custom → **Raw Canvas/WebGL**" 只给了 WebGL 一个选项；而 §2（L52）明确"新项目：WebGPU with WebGL fallback"。若 agent 走自定义渲染路线，按决策树选 "Raw WebGL" 与 §2 的 WebGPU-first 原则存在轻微冲突——树没有说明自定义渲染场景下的 WebGPU/WebGL 取舍规则（其实可以直接复用 §2 的 fallback 规则）。小逻辑缺口，修复见 F-8。

### 4.3 标题层级并列（L15/L17）

"### Decision Tree" 与 "### What type of game?" 同级并列，后者是前者的子问题，应为 `####`。dossier 已记录此排版瑕疵，复核确认原样保留。纯格式问题，无内容影响。

### 4.4 技术事实核验

- WebGPU 支持表：Chrome/Edge v113 ✅、Firefox v131 ✅、Safari 18.0 ✅、~73% 全球 ✅（2025 年口径合理）
- 框架版本：Phaser 4 / PixiJS 8 / Three.js / Babylon.js 7 —— 与 2025 年发布状态相符 ✅
- 音频自动播放限制、AudioContext 需用户交互恢复 ✅（浏览器平台常识，正确）
- PWA 三需求（service worker / manifest / HTTPS）✅
- 压缩格式（KTX2/Basis、WebM/Opus、glTF+Draco/Meshopt）✅ 均为 2025 年主流实践
- **无任何事实错误**——对比 050 的虚构 OWASP 分类法、074 的自相矛盾数字，本 skill 的事实面是干净的

### 4.5 知识增量评估（spec §3.4）

145 行内容全部是"模型可能知道但容易忽略/记错"的浏览器平台约束（浏览器支持时间线、压缩格式选型、PWA 要求、音频策略），冗余度低。"知识增量"达标。唯一偏薄处：§6 音频节与 §4 慢网络处理只给了概念未给形态（见 F-12/F-13）。

---

## 5. 参考文件内容级审查

目录内共 4 个文件，全部通读完毕（无抽样）。

### 5.1 SKILL.md（145 行）—— 全文分析

逐段要点已在 §3 展开。行级事实补充：L3 description 302 字符；L17-25 决策树（5 分支 10 行）；L30-35 框架比较表；L43-49 浏览器支持表；L62-68 约束表；L72-76 优化优先级（唯一带编号的执行指令）；L83-87 格式表；L91-95 加载阶段表；L119-121 音频要求；L135-141 反模式表。**无 TODO、无占位符、无悬空引用、无跨技能路径、无 emoji**。145 行 ≤600 硬上限；相对 mindset 模式 ~50 行目标超 2.9 倍（目标值为引导性而非硬性，但体量确实偏"参考手册"而非"心态框架"——若未来收紧体量纪律，可下沉 §4/§5 表格到 references/，见 F-15）。

### 5.2 SCORING.yaml（162 行）—— 全文分析

结构：`skill: web-games`、`pattern: mindset`、`total_items: 18`、18 条 criteria（scope 3 / decision 4 / process 5 / negative 2 / output 2 / qa 2）、2 条 critical_failures（均 cap_to_0）。**total_items 与实际 criteria 数一致（3+4+5+2+2+2=18）**，无计数错位。script 判定 6 项（DEC-04、PROC-03、PROC-05、OUT-01、OUT-02、OUT-03），llm 判定 12 项，分工清晰。critical_failures 两条语义合理且互不重叠：CF-01（无特性检测/回退直接用 WebGPU → cap_to_0）、CF-02（游戏在浏览器中运行失败 → cap_to_0）。

**重大缺陷：四条 pattern 的转义层级错误**（`\\.` 而非 `\.`，文件字节级确认），解析后正则语义错误甚至无法编译——详见 §6.4，修复见 F-4。

### 5.3 check.py（77 行）—— 全文分析

L11 向 `..\_shared` 注入路径，L12-16 导入 checker 四个函数（`file_exists` / `output_contains` / `set_tool_log_path` / `set_agent_output`）——已核实 `_shared/checker.py` 存在且签名完全匹配，导入链可解析。L38/42/44/51-52 实现 6 项脚本判定，与 SCORING 的 script 项**一一对应、无错位**（L19 docstring "Run all 6 script checks" 与实现数一致）。main()（L58-73）CLI 契约（三参数、输出 JSON）符合 runner 约定；check() 内对 agent 输出入参做了 path/内容双模式防护（L24-29），与 059 同款健壮处理。

两个观察点：其一，**工具日志参数虽传入 `set_tool_log_path` 但从未被任何判定读取**——6 项检查全部是 `output_contains` + `file_exists`，不依赖 tool_log。这意味着 OUT-01 描述中的 "executed/verified"（执行并验证）没有任何日志佐证，"游戏真的在浏览器里跑过"无从核实，只有"文件存在"这一个代理信号（见 §9.2）。其二，无"空日志虚过"路径（对比 306 的 NEG-01 空转问题）——本 skill 不用日志判定，反而躲开了该类退化路径。

### 5.4 _shared/checker.py（351 行）—— 外围验证通读

本文件在 skill 目录外，但 check.py 的全部行为由它决定，通读以支撑 5.3 的结论。关键语义确认：

- `file_exists(path)`（L20-23）：`glob.glob(path, recursive=True)` 后检查任一匹配存在。**已实测** `assets/**/*` 能匹配 `assets/` 顶层文件（如 `assets/sprite.png`），也能匹配嵌套文件——递归语义正常，不是坑。
- `output_contains`（L339-343）：`_agent_output` 为空时返回 False（严格模式）；`re.MULTILINE` 下全文搜索。
- `tool_log_contains` 系函数（L259-268）存在且签名与 check.py 的用法兼容，但本 skill 未使用。
- 无异常防护：`output_contains` 对非法正则直接抛 `re.error`——这与 §6.4 发现的 SCORING pattern 转义缺陷叠加后，若 runner 直接以 SCORING 的 pattern 驱动判定，PROC-03 会**崩溃**而非优雅失败。

### 5.5 _shared/SKILL-SPEC.md（162 行）—— 规范锚点通读

v1.0 规范全文已通读，本 REVIEW 所有合规判定均以它为准。本 skill 触发的条款：§2.4 触发信号（命中 "Use when the user asks to..."）；§3.1 三必需结构（**全部未满足**）；§3.2 mindset 目标 ~50 行（145 行超量，非硬性）；§1.2 allowed-tools 可选字段（已用，格式正确）；§1.3 禁用键（无）。

### 5.6 悬空引用台账

**零悬空引用**：SKILL.md 全文未引用任何外部文件（无 `references/`、无 `scripts/`、无 `../` 跨技能路径、无裸文件名引用）。对比 306 的 8 个悬空引用点，本 skill 的"完全自包含"是其最大的工程优点之一——不存在打包遗漏风险。

---

## 6. 语法与格式质量

### 6.1 Markdown 结构

两级标题体系（## 7 节 + ### 12 个小组），无跳级；表格全部对齐（5 张表）；列表层级规范（决策树为嵌套列表）；代码块无（全文无代码示例——这是内容选择而非格式缺陷）。唯一排版缺陷：L15/L17 标题层级并列（§4.3）。

### 6.2 YAML 有效性

frontmatter 与 SCORING.yaml 均 PyYAML 解析通过，无语法错误。SCORING 的 criteria 结构（id/category/description/judge/check）逐条一致，无字段缺失或错位。

### 6.3 语言与术语

英文干净流畅，无错字、无病句、无葡语残留（对比 093/262/276 的葡语泄漏，本 skill 干净）。术语使用一致：WebGPU/WebGL 不混用，PWA/Service Worker/manifest 命名规范。无 emoji、无全大写喊话（对比 072 的 emoji 泛滥）。"The browser is the most accessible platform" 格言腔见 §3.10。

### 6.4 正则与转义一致性 —— 重点发现（评测体系缺陷）

SCORING.yaml 四条 pattern 与 check.py 对应正则存在**转义层级不一致**，逐字核验如下：

| 判据 | SCORING.yaml 文件字节 | PyYAML 解析后（正则语义） | check.py 运行时（正则语义） | 是否一致 |
|------|----------------------|--------------------------|---------------------------|:--------:|
| DEC-04 | `audioContext\\.resume` | 字面反斜杠+任意字符+resume（**错**） | `audioContext.resume` 字面（**对**） | ❌ |
| PROC-03 | `register\\(` 等 | **re.compile 直接报错**（未终止子组） | `register\(`（**对**） | ❌ |
| PROC-05 | `document\\.hidden` | 字面反斜杠+任意字符+hidden（**错**） | `document.hidden` 字面（**对**） | ❌ |
| OUT-02 | `navigator\\.gpu` | 字面反斜杠+任意字符+gpu（**错**） | `navigator.gpu` 字面（**对**） | ❌ |

原因：SCORING.yaml 的单引号标量中写了双反斜杠 `\\.`，PyYAML 单引号不处理转义，解析后得到**双反斜杠**正则；而 check.py 源码中的 `\\.` 经 Python 字符串字面量解析后得到**单反斜杠**正则。**实测**：解析 SCORING.yaml 的 PROC-03 pattern 后 `re.compile` 抛出 "missing ), unterminated subpattern"（编译失败）；DEC-04/PROC-05/OUT-02 解析后语义错乱（要求匹配字面反斜杠）。

影响取决于 runner 的判定驱动方式：
- 若 runner 执行 check.py（本 skill 的 docstring 即此模式）→ 运行时正确，SCORING 的 pattern 退化为文档，**不炸**；
- 若 runner 按 `_shared/checker.py` docstring（"runner resolves ${VARIABLES} before calling these functions"）以 SCORING.yaml 的 `fn`+`pattern` 通用驱动 → 3 条语义错乱、1 条编译崩溃（且 `output_contains` 无异常防护，可能拖垮整轮检查）。

无论哪种模式，两份文件的正则**解析后语义不相等**，都是评测一致性的硬伤。正确写法是 SCORING.yaml 内用单反斜杠 `\.`（YAML 原样保留），与 306 的"YAML 单 / Python 双"等价模式对齐。修复见 F-4。

### 6.5 编码与排版

四文件均为 UTF-8 无 BOM，行尾统一（无 \r\n 混排），行宽正常。检查结论：编码与排版无故障。

---

## 7. 规范合规性（12-item checklist，按 spec §5）

对 SKILL.md 逐项判定：

1. `name` 小写+连字符、≤64 字符、与目录匹配（NNN 前缀约定）—— ✅
2. description 第三人称、含 WHAT+WHEN+KEYWORDS、302 字符 ≤1024—— ✅
3. description 无 imperative/first-person/second-person 开头—— ✅
4. description 无 cross-skill routing—— ✅
5. description 含至少一个触发信号句式—— ✅（"Use when the user asks to..."，spec §2.4 精确命中）
6. frontmatter 无 allowed 清单外键—— ✅（仅 name/description/allowed-tools 三键）
7. body ≤600 行—— ✅（145 行）
8. body 有 workflow/process 节—— ❌ **缺失**（§3.2）
9. body 有 output format 节—— ❌ **缺失**（§3.2）
10. body 有 scope/limitations 节—— ❌ **缺失**（Anti-Patterns 为行为禁令，非边界声明）
11. body 无跨 skill 文件引用（../other-skill/）—— ✅（零引用）
12. 目录 NNN-kebab-case、无空格大写—— ✅

**12 项中 9 项通过、3 项失败，失败项恰为 spec §3.1 的三必需节。** 这是本 skill 唯一的合规败项，但也是最常见的语料库缺陷（~68% 缺 Scope）的极端形态——三节全缺而非缺一节，修复成本不高但必须修（见 §13 F-1/F-2/F-3）。

---

## 8. 人机感评估

### 8.1 可读性

结构顺序（框架 → 渲染 → 性能 → 资产 → PWA → 音频 → 反模式）符合"先选型、后实现、再收尾"的认知顺序，一个首次接触的 agent 可以在 30 秒内建立完整的决策模型。表格密度高（5 张表承载大部分信息），无冗余段落，读起来不费力。

### 8.2 指令清晰度

最优处：决策树的可裁决性（"2D 全功能 → Phaser"直接给答案）与优化优先级 1-5 的显式排序。agent 不需要自行推断任何选型判据。对比 031/041 等同型参考 skill 的纯知识罗列，本 skill 的决策结构是显著加分项。

### 8.3 输出可预期性

最大负分项。全文没有一句话告诉 agent"你最后要交付什么"：是一个单文件 HTML？一个带 assets/ 的工程目录？一段说明？评分体系（OUT-01/OUT-03）对交付物有明确预期，正文却完全沉默。agent 拿到这个 skill 后最自然的产出是"一段原则摘要"，而这恰恰过不了 OUT-01。**指令清晰，但交付盲区**。

### 8.4 错误路径指引

零指引。无验证步骤、无自查清单、无错误处理建议（对比 059 的 QUALITY GATES）。CF-02（游戏运行失败 → 清零）没有任何正文防线。

### 8.5 语气

零 emoji、零全大写喊话、零营销腔（对比 072/121）。格言收尾（L145）略带格言腔但语义恰是全文主线（浏览器约束），可接受。dossier 判定"可接受"，复核维持。

### 8.6 人机协作边界

无"向用户澄清"步骤（平台、性能预算、离线需求、多人等前置问题）。对 mindset skill 而言不致命，但加一步澄清问题可显著提升 SCOPE-01/02 的判定稳健性（见 F-11）。

---

## 9. 可执行性评估

### 9.1 形态匹配

`pattern: mindset`（创意任务需品味与判断）——正文形态（原则 + 决策树 + 反模式）与 mindset 定义吻合：它指导 agent 在浏览器游戏开发中做"判断"（选框架、选渲染路径、选优化顺序），而非执行固定工序。形态匹配成立。145 行相对 ~50 行目标偏厚（§5.1），但内容密度高，不是 083-085 那种空白模板。

### 9.2 六项脚本判定的传导分析（核心风险表）

| 判据 | 检查内容 | 正文锚点 | 风险 |
|------|---------|---------|:----:|
| DEC-04 | `new AudioContext\|audioContext.resume\|createAudioContext` | L120-121 概念完整（创建于交互时/挂起则恢复） | 🟢 **稳**——agent 自然写出 `new AudioContext()` |
| OUT-02 | `navigator.gpu\|WebGLRenderer\|WebGPU.*fallback` | L54 明确点名 "Check `navigator.gpu`" | 🟢 **稳** |
| PROC-03 | `serviceWorker\|manifest.json\|register(` | L110-111 口语词 "Service worker"（带空格）/ "Web app manifest" **均不命中正则** | 🟡 **中**——依赖 agent 联想 `navigator.serviceWorker.register('sw.js')` |
| PROC-05 | `visibilitychange\|document.hidden\|visibilityState` | 仅有 "Pause when hidden"（L64/L137），**未点名任何 API** | 🔴 **高**——agent 可能用 blur/focus 事件或 rAF 跳过实现暂停，判定失败 |
| OUT-01 | `*.html` 文件存在 | **零锚点**——正文从未说交付 HTML 文件 | 🔴 **高**——mindset 型 agent 可能只给原则/代码片段不建文件 |
| OUT-03 | `assets/**/*` 存在 | **零锚点**——正文从未要求 assets/ 目录；程序化/内联资产的游戏（Canvas 纯代码绘制）天然无 assets 目录 | 🔴 **高**——误判失败风险 |

结论：6 项中 2 项稳、1 项中、**3 项高风险**。高风险项的共性是把"agent 的 API 常识"当成了"正文指令"——修复成本极低（每项一行字），收益却直接决定评测得分（见 F-5）。

### 9.3 CF 传导与验证盲区

- CF-01（无特性检测直接 WebGPU → 清零）：正文 §2 三条决策规则直接覆盖，**防线完整** ✅。
- CF-02（游戏在浏览器中运行失败 → 清零）：正文**零验证指引**，且 allowed-tools 无 Bash 无法实测——唯一的防线是 LLM 目测代码质量。作为"清零级"判据，它的防误触设计明显弱于 CF-01。修复见 F-6。

### 9.4 恢复成本

修复成本在语料库中属于最低档：正文加 3 节（约 40 行）+ 点 API 名（约 5 行）+ SCORING 转义修正（4 行改动）+ allowed-tools 补 Bash（1 行）。总工作量约 2-3 小时，远低于 306 的 11-13 小时。可执行性从"3 项高风险"到"6 项全稳"的边际成本极低。

---

## 10. SCORING.yaml 交叉参考

### 10.1 criteria 与正文的映射完整性

18 条 criteria 逐一溯源：

| 判据 | 正文锚点 | 强度 |
|------|---------|:----:|
| SCOPE-01 | L9 引言 + description | 强 |
| SCOPE-02 | L17-25 决策树 | 强 |
| SCOPE-03 | L18-25（决策树无原生方案分支，隐含） | 中 |
| DEC-01 | L51-55 WebGPU 决策 | 强 |
| DEC-02 | L70-76 优化优先级（顺序逐字一致） | 强 |
| DEC-03 | L83-87 压缩格式表 | 强 |
| DEC-04 | L117-121 音频要求 | 强 |
| PROC-01 | L62-68 浏览器约束表 | 强 |
| PROC-02 | L89-95 加载阶段表 | 强 |
| PROC-03 | L100-112 PWA 需求（API 名未点名） | 中 |
| PROC-04 | L72-76 优化优先级 | 强 |
| PROC-05 | L64/L137 "Pause when hidden"（API 未点名） | 弱 |
| NEG-01 | L135-139 反模式 1-3 行 | 强 |
| NEG-02 | L141 反模式末行 | 强 |
| OUT-01 | **无锚点**（交付物形态从未定义） | 无 |
| OUT-02 | L54 "Check `navigator.gpu`" | 强 |
| OUT-03 | L79-95 资产策略（目录要求未定义） | 弱 |
| OUT-04 | L27-35 比较表（"为何选 Phaser 而非 PixiJS"未要求解释） | 弱 |

映射覆盖率为概念层 100%（每条判据都能在正文找到相关主题），但**锚点强度分化明显**：14 条强/中、4 条弱/无——弱项恰好集中在"交付物"三件套（OUT-01/03/04）与 PROC-05。这不是判据设计错误，而是正文缺 Output Format 节的连锁反应。

### 10.2 check.py 与 SCORING 的一致性及缝隙

- 6 项脚本判定与 SCORING 的 script 项**一一对应、无错位**（写了必查、查了必写）✅
- `total_items: 18` 与实际 criteria 数一致 ✅
- 2 条 critical_failures 无脚本化实现（属预期，由 runner/LLM 判定）✅
- **缝隙一**：正则转义不一致（§6.4）——SCORING 解析值 ≠ check.py 运行时值，是本次审查发现的唯一"双文件实质性分歧"。
- **缝隙二**：OUT-01 描述承诺 "runs in the browser without console errors (executed/verified)"，脚本仅查 `*.html` 存在——"运行验证"无任何可观测信号。
- **缝隙三**：OUT-03 对无资产游戏（程序化绘制）必然误判失败，判据未设条件分支（"仅当代码引用了资产文件时才要求存在"）。

### 10.3 Critical failures 评估

CF-01 ✅ 合理且防线完整（§9.3）；CF-02 ✅ 意图合理，但防误触设计弱于 CF-01（正文无验证指引）。两条均无虚构或错位。

---

## 11. 已知问题验证（来自 skill-dossier.md 与旧 REVIEW stub）

### Dossier 记录

> **061-web-games**: 🟢 评级。**逻辑**: 框架决策树、WebGPU 支持表、性能/资产/PWA 原则内部一致；仅 "### Decision Tree" 与 "### What type of game?" 标题层级并列属排版小瑕疵。**语法**: 规范清晰。**人机感**: 结尾 "The browser is the most accessible platform. Respect its constraints." 略带格言腔但可接受。**合规**: Description 第三人称含触发词，正文 145 行 ≤600，无跨技能路径。**总评**: 🟢 简洁准确。

### 逐项验证

| Dossier 判定 | 状态 | 本次验证结果 |
|--------------|:----:|-------------|
| 框架决策树/WebGPU 表/性能/资产/PWA 原则内部一致 | ✅ | 复核成立；另发现 Hybrid 分支漏 raw WebGPU 的小张力（§4.2） |
| "### Decision Tree" 与 "### What type of game?" 标题层级并列 | ❌ **仍存在** | L15/L17 原样保留，dossier 记为"排版小瑕疵"成立 |
| 结尾格言腔可接受 | ✅ | L145 保留，维持可接受判定 |
| Description 第三人称含触发词 | ✅ | L3，"Use when the user asks to..." |
| 正文 145 行 ≤600 | ✅ | wc -l 实测 145 |
| 无跨技能路径 | ✅ | 零文件引用（§5.6） |
| 三必需节完整性 | 🆕 **本次新增验证：全部缺失** | §3.2：Workflow/Output/Scope 三节全缺。dossier 审查时未检查此项，旧 REVIEW stub 已标注"需验证"——本次验证结论是**均不存在**，dossier 的 🟢 评级需据此下修 |

### Dossier 遗漏的增量问题

1. **三必需节全缺**（核心缺口，dossier 未验证）
2. **SCORING/check.py 正则转义不一致**（§6.4）——双文件解析后语义不等，3 条错乱 + 1 条编译失败
3. **脚本判定与正文锚点错位**（§9.2）——PROC-05 未点名 API、OUT-01/03 无交付形态指引、OUT-04 无"解释选型理由"要求
4. **CF-02 无验证防线 + allowed-tools 缺 Bash**（§9.3）
5. **决策树 Hybrid 分支漏 raw WebGPU**（§4.2）

### 旧 REVIEW stub 评分核验

旧 stub 记载 "**综合**: 🟢 **B+** (53/100)"。本次独立评分为 **77/100**（§12）。差异说明：stub 为占位性快评（4 行），53 分未计入两个高权重正面因素——内容逻辑一致性（20% 权重维度 8.5 分）与评测体系总体质量（映射 100%、无错位）。53 分更接近"纯规范视角"的估分，而 77 分是八维加权下的综合分。**评级符号与 dossier 同为 🟢 的"乐观"，需统一修正为 🟡**——三必需节缺失是规范硬伤，不是"可用"评级能带过的。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | description 上乘（WHAT/WHEN/KEYWORDS 齐备 + 触发句式精确命中）；仅 allowed-tools 缺 Bash 的执行语义矛盾 |
| Body 结构完整 | 4/10 | 10% | 0.40 | 7 个原则节组织良好、密度高；但三必需节全缺 |
| 逻辑一致性 | 8.5/10 | 20% | 1.70 | 决策树↔比较表↔SCORING 全链对齐，优化优先级顺序逐字一致，技术事实零错误；仅标题层级与 Hybrid 分支小瑕疵 |
| 参考完整性 | 10/10 | 15% | 1.50 | 完全自包含，零悬空引用，无打包遗漏风险 |
| 语法格式 | 8.5/10 | 10% | 0.85 | 干净规范、零 emoji、零错字；仅标题层级并列 + 正文无代码示例（内容选择） |
| 规范合规 | 6/10 | 15% | 0.90 | 9/12 通过，三必需节缺失为唯一败项（但为全缺形态） |
| 人机感 | 8/10 | 10% | 0.80 | 语气干净、判据可裁决；输出可预期性与错误路径指引为零是主要扣分 |
| 可执行性 | 6/10 | 10% | 0.60 | 6 项脚本判定 2 稳 1 中 3 高险；CF-02 无验证防线；恢复成本极低 |

**加权合计**: 0.90 + 0.40 + 1.70 + 1.50 + 0.85 + 0.90 + 0.80 + 0.60 = **7.65 → 77/100**

### 12.2 评级

**🟡 B (77/100)**。等级判定（🟢≥80 / 🟡60-79 / 🟠40-59 / 🔴<40）。

需要明确说明：这是"内容质量分与规范合规分的混合"。纯看内容，这是语料库中结构最清晰、事实最干净的知识参考型 skill 之一（决策树可裁决性、优化优先级显式排序、SCORING 映射 100%），内容分可评 88+；纯看规范，三必需节全缺是硬伤，规范分只能评 55。77 分的诚实含义是：**写得好但结构上没完工的 skill**——只差三个必需节与四处小修（合计约 2-3 小时），修复后可直接进入 🟢 85+ 区间。修复 🔴 四项后，12 项合规检查即全绿。

### 12.3 与同类对比

- vs **031-tailwind-patterns**（269 行，纯知识参考、缺三节，🟡）：061 的决策树与优先级排序使其"执行锚点"远强于 031 的纯罗列——同缺三节，061 的修复价值更高。
- vs **082-mobile-games**（~108 行，同游戏主题、缺三节，🟡）：082 是纯参考表，061 多出可裁决决策树与反模式表，且 061 与 SCORING 的联动（映射 100%）优于 082。
- vs **041-nextjs-best-practices**（197 行，缺三节 + 版本过时，🟡）：041 带过时建议（Edge runtime 等），061 无任何过时内容——061 是同类中最干净的一员。
- vs **306-campaign-analytics**（61 分 🟡）：306 的问题是"包装完整内胆抽走"（8 个引用全悬空），061 完全自包含——061 的缺陷是"结构欠账"而非"实物欠账"，性质轻得多。

---

## 13. 修复建议（按优先级分层）

修复原则：不动 skill 的整体框架（7 个原则节、决策树、SCORING 体系全部保留），只补三个必需节、修正转义与锚点、加一个验证步。所有改动均可在一个文件（SKILL.md）加一个文件（SCORING.yaml）内完成。

### 🔴 致命（不修复则合规不达标 / 评测判定不稳）

#### F-1 补 Workflow/Process 节（新增）—— 三必需节之第一块

- **位置**: 建议插在 `## 1. Framework Selection` 之前，标题 `## Workflow`
- **现状**: 全文无执行序列，agent 无"从拿到需求到交付"的步骤链（§3.2）
- **修复方向**（8 步显式序列草稿）:

  ```
  ## Workflow

  1. Clarify scope: game type (2D/3D), target devices, performance budget, offline needs
  2. Select the framework via the decision tree in Section 1
  3. Decide the rendering path: WebGPU with WebGL fallback for new projects (Section 2)
  4. Implement the game loop, input, and rendering with the optimization priority in Section 3
  5. Load assets per the phased strategy in Section 4 (core <2MB at startup)
  6. Set up audio per Section 6 (create AudioContext on first user interaction)
  7. Apply PWA requirements in Section 5 when offline play is requested
  8. Verify the game in the browser: no console errors, assets load, visibility pause works
  ```

- **附带收益**: 步骤 8 直接覆盖 CF-02 的验证盲区（§9.3）；步骤 1 顺带解决 §8.6 的澄清问题缺口
- **不修复的后果**: 12 项合规检查中 workflow 一项永久失败；agent 无执行入口，产出质量方差大

#### F-2 补 Output Format 节（新增）—— 三必需节之第二块，直接决定 OUT-01/OUT-03 的通过率

- **位置**: 建议插在 `## 7. Anti-Patterns` 之前，标题 `## Output Format`
- **现状**: 交付物形态从未定义（§8.3），OUT-01（`*.html`）与 OUT-03（`assets/**/*`）两个脚本判据在正文中零锚点（§9.2）
- **修复方向**（草稿）:

  ```
  ## Output Format

  Deliver a runnable browser game:
  - A single `index.html` (or `game.html`) that runs standalone in a browser — no build step required
  - An `assets/` directory containing every asset the code references (textures, audio, models)
  - No console errors on load; the game loop pauses when the tab is hidden
  - Explain the framework choice vs. alternatives in one or two sentences (e.g., why Phaser over PixiJS)
  ```

  最后一行"Explain the framework choice"顺带把 OUT-04（LLM 判据）从弱锚点变强锚点
- **不修复的后果**: OUT-01/OUT-03 大概率误判失败（mindset 型 agent 不建文件、程序化游戏无 assets 目录）；OUT-04 依赖 agent 自发解释

#### F-3 补 Scope/Limitations 节（新增）—— 三必需节之第三块

- **位置**: 建议插在 `## 7. Anti-Patterns` 之后，标题 `## Scope`
- **现状**: Anti-Patterns 是行为禁令，非边界声明（§3.2）
- **修复方向**（草稿）:

  ```
  ## Scope

  This skill covers browser game development principles only. It does NOT cover:
  - Game design, mechanics, and level design
  - Monetization, IAP, ad integration
  - Backend services, multiplayer servers, real-time networking
  - Native game engines (Unity, Godot, Unreal) or native mobile development
  - WebXR content creation beyond rendering API choice
  - Packaging for app stores

  Do not use this skill when the user asks for native-only games, server-side game
  logic, or game design consulting without any browser implementation.
  ```

- **不修复的后果**: agent 会被要求做"游戏设计/后端/原生"时强行套用本 skill，产出范围错位；SCOPE-03 判定（不推荐原生方案）无边界支撑

#### F-4 修复 SCORING.yaml 正则转义（SCORING.yaml L61/L86/L102/L136）—— 评测一致性硬伤

- **现状**: 四条 pattern 文件内为双反斜杠 `\\.`，PyYAML 解析后得到双反斜杠正则——3 条语义错乱（匹配"字面反斜杠+任意字符"而非字面点号）、1 条（PROC-03）`re.compile` 直接报错（§6.4 实测）
- **修复方向**: 将 SCORING.yaml 中的 `\\.` 改为 `\.`（YAML 单引号标量原样保留单反斜杠），与 check.py 运行时值对齐:

  ```
  DEC-04: '(?i)(new AudioContext|audioContext\.resume|createAudioContext)'
  PROC-03: '(?i)(serviceWorker|manifest\.json|navigator\.serviceWorker|register\()'
  PROC-05: '(?i)(visibilitychange|document\.hidden|visibilityState)'
  OUT-02: '(?i)(navigator\.gpu|WebGLRenderer|WebGPU.*fallback|fallback.*WebGL)'
  ```

- **注意**: check.py 保持不变（其运行时值已正确）；不要两头都改
- **不修复的后果**: 若 runner 以 SCORING pattern 通用驱动判定（checker.py docstring 描述的模式），DEC-04/PROC-05/OUT-02 全部错乱、PROC-03 抛异常拖垮整轮检查；即使 runner 只跑 check.py，SCORING 作为"判据元数据"也是错误的，误导后续维护与 LLM 判定

### 🟡 重要（影响判定稳健性或执行闭环）

#### F-5 正文点名脚本判定所需的 API（SKILL.md L64/L110-112/L137 附近）—— 消除 3 项高风险判定

- **位置**: §3 Browser Constraints 表、§5 PWA Requirements、§6 Audio 节
- **修复方向**: 在各节补一行"API 形态"，例如:

  ```
  - Pause the game loop on hidden tabs: document.addEventListener('visibilitychange', ...)
    and check document.hidden — do not rely on requestAnimationFrame skipping alone
  ```
  （§3 或 §7 一行，直接命中 PROC-05）;

  ```
  - Register the service worker with navigator.serviceWorker.register('sw.js') and
    reference the manifest as manifest.json
  ```
  （§5 一行，直接命中 PROC-03）;

  ```
  - const audioCtx = new AudioContext(); created inside the first click/tap handler;
    call audioCtx.resume() if it is suspended
  ```
  （§6 一行，DEC-04 从"2/3 备选"变"3/3 全稳"）

- **不修复的后果**: PROC-05 高概率失败（agent 用 blur/focus 或 rAF 跳过实现暂停是常见选择）；PROC-03 依赖联想
- **工作量**: 3 行，5 分钟

#### F-6 补验证/QA 步骤（SKILL.md Workflow 内）—— CF-02 的唯一防线

- **修复方向**: 在 F-1 的 Workflow 步骤 8 之外，再在 §3 或新 Output Format 节补一段:

  ```
  Before delivering: open the page in a browser (or self-review the code as if running),
  confirm zero console errors, confirm all referenced assets resolve, and confirm the
  loop pauses on tab switch.
  ```

- **不修复的后果**: CF-02（清零判据）完全靠 LLM 目测，无正文防线
- **工作量**: 3 行，5 分钟

#### F-7 修正标题层级（SKILL.md L17）

- "### What type of game?" → "#### What type of game?"（Decision Tree 的子问题）。dossier 已标记，本次复核仍存，顺手修掉
- **工作量**: 1 个字符层级，1 分钟

#### F-8 决策树 Hybrid 分支补 raw WebGPU 并统一渲染规则（SKILL.md L24-25）

- **现状**: "Hybrid / Canvas → Custom → Raw Canvas/WebGL" 只有 WebGL，与 §2 的 WebGPU-first 原则存在小张力（§4.2）
- **修复方向**: 改为 "Custom → Raw WebGPU (new, with WebGL fallback) or Raw WebGL (legacy)"，并加一句"自定义渲染也遵守 §2 的 fallback 规则"
- **工作量**: 1 行，2 分钟

#### F-9 allowed-tools 补 Bash（SKILL.md L4）

- **修复方向**: `allowed-tools: Read, Write, Edit, Glob, Grep, Bash`
- **说明**: 规范 §1.2 中为可选字段，但 OUT-01 描述承诺 "executed/verified"、CF-02 要求游戏可运行——无 Bash 则验证环节无工具支撑。补上后 agent 可以 `python -m http.server` 起本地服务或用无头浏览器自检
- **不修复的后果**: 验证环节永远停留在"自省"，与评分描述（executed/verified）脱节
- **工作量**: 1 行

#### F-10 处理 OUT-03 假阴性风险（SCORING.yaml L139-145）

- **现状**: `file_exists("assets/**/*")` 对无资产游戏（纯 Canvas 程序化绘制）必然失败——判据未区分"有资产引用"与"无资产"
- **修复方向 A（推荐，改正文）**: 配合 F-2 的 Output Format 要求"交付物必须含 assets/ 目录"——程序化游戏可放一个 `assets/README.md` 或实际用到的音频位图，让判据稳定可过
- **修复方向 B（改判据）**: 将 OUT-03 改为 llm 判定"代码引用的资产文件存在或已生成"（条件性判定），避免误伤；或在 SCORING 中注明"仅当代码引用资产文件时生效"
- **不修复的后果**: 合法交付（程序化游戏）被判失败，评测噪音
- **工作量**: A 5 分钟 / B 15 分钟

### 🟢 优化（锦上添花）

#### F-11 加澄清问题步骤（SKILL.md Workflow 步骤 1 扩展）

- 在 F-1 的步骤 1 中显式列出一组前置问题（2D/3D、目标设备、性能预算、是否离线、是否多人），提升 SCOPE-01/02 判定稳健性与人机协作质量（§8.6）
- **工作量**: 2 行

#### F-12 慢网络处理具体化（SKILL.md §4 或 §7）

- NEG-02 判定"显式处理慢网络"——正文目前只有反模式表一行 "Assume fast connection → Handle slow networks"（概念级）
- 补一行具体形态: "degraded experience（降级画质/降采样）、loading states、progress indicators、adaptive asset quality based on navigator.connection"
- **工作量**: 2 行

#### F-13 Audio 节补最小代码骨架（SKILL.md §6）

- 与 F-5 的音频行合并为一小节（创建于 click/keydown、挂起时 resume、懒加载），给 DEC-04/PROC-05 双覆盖的完整形态
- **工作量**: 4 行

#### F-14 数据时效声明（SKILL.md §2）

- "Browser Support (2025)" 与 "Comparison (2025)" 是静态标注——补一句 "verify against current browser release notes before relying on support percentages"（浏览器支持表半年内可能过时）
- **工作量**: 1 行

#### F-15 体量治理（可选）

- 145 行 vs mindset 目标 ~50 行（超 2.9 倍）。若语料库未来收紧体量纪律，把 §4（资产格式/加载策略表）与 §2（支持表）下沉到 `references/` 并按 F-2 的 Output Format 引用——当前非必需，仅作预案
- **工作量**: 30 分钟（若执行）

### 修复工作量估计

- **修改行数**: ~60-70 行（F-1 ~16 行、F-2 ~10 行、F-3 ~12 行、F-4 4 行、F-5 3 行、F-6 3 行、F-7/F-8/F-9/F-10 各 1-5 行、F-11~F-15 ~10 行）
- **修改文件数**: 2（SKILL.md 为主，SCORING.yaml 仅 F-4/F-10）
- **优先级路线**: 🔴 四项（约 2 小时）修复后，12 项合规检查全绿（9/12 → 12/12），脚本判定风险从"3 高险"降至"全稳"，预计得分 82-88 → 🟢；🟡 六项（约 45 分钟）修复后稳定性满格；🟢 五项视需要

---

## 附录: 审查过程记录

### 读取的文件

1. **SKILL.md** (145 行 / 3,147 字节) — 逐行精读 + 行号级复读 + grep 全标题枚举
2. **SCORING.yaml** (162 行 / 7,518 字节) — 全文，18 criteria + 2 critical_failures，逐项与正文映射 + PyYAML 解析 + pattern 字节级核验
3. **check.py** (77 行 / 2,729 字节) — 全文，6 个脚本检查，核对 _shared/checker.py 函数签名与正则运行时值
4. **REVIEW.md** (4 行 / 167 字节) — 旧 stub，本次重写
5. **_shared/SKILL-SPEC.md** (162 行) — v1.0 规范全文，逐条对照
6. **_shared/checker.py** (351 行) — 通读全部检查函数语义（file_exists 的 glob 递归行为、output_contains 的空值严格性、tool_log 系列未使用确认）
7. **skill-dossier.md** — 061 条目 + 全库 322 条背景 + 同类对比条目（031/041/082/183）

### 实测验证记录

| 验证项 | 方法 | 结果 |
|--------|------|------|
| description 长度 | L3 `wc -c` | 302 字符 ≤1024 ✅ |
| 触发信号 | 文本检索 | "Use when the user asks to" 精确命中 spec §2.4 ✅ |
| total_items 一致性 | PyYAML 计数 | 18 = 18（scope 3 / decision 4 / process 5 / negative 2 / output 2 / qa 2）✅ |
| 脚本判定项对应 | 逐项比对 | check.py 6 项 = SCORING script 6 项，无错位 ✅ |
| SCORING pattern 转义 | 文件字节 repr + PyYAML 解析 + re.compile | 双反斜杠确认；PROC-03 解析后编译报错 "missing ), unterminated subpattern"；check.py 运行时值为正确单反斜杠 ❌ |
| `assets/**/*` glob 语义 | 临时目录实测 | 能匹配 assets/ 顶层文件与嵌套文件 ✅（file_exists 无此坑） |
| 正文 API 锚点 | 正则检索正文 | 正文含 `navigator.gpu`/AudioContext（口语）/Service worker（带空格）；不含 visibilitychange/document.hidden/manifest.json ❌（F-5 依据） |
| 行数 | wc -l | SKILL.md 145 ✅（与 dossier 一致） |
| 编码 | 字节检查 | 四文件 UTF-8 无 BOM，行尾统一 ✅ |

### 读取行数统计

总计: ~980 行（SKILL.md 145 + SCORING.yaml 162 + check.py 77 + REVIEW.md 4 + SKILL-SPEC.md 162 + checker.py 351 + dossier 相关条目 ~80）

### 审查方法

- 全文阅读（非抽样）: ✅（skill 目录内 4/4 全部通读；外围 2 文件通读）
- 交叉验证: SKILL.md ↔ SCORING.yaml ↔ check.py ↔ SKILL-SPEC.md v1.0 ↔ skill-dossier.md ↔ 同类 REVIEW（031/041/082/183 条目）
- 实证验证: 正则转义问题用字节级 repr + PyYAML 解析 + re.compile 三重复核；glob 语义临时目录实测；浏览器支持数据对照官方发布时间线
- 未执行项: 未运行 check.py（依赖评测 runner 提供的 workspace/tool_log/agent_output，非本审查范畴）

### 审查人

Claude (SkillIF quality audit) — 2026-08-06

### 审查备注

本 skill 是知识参考型 mindset skill 中内容质量的第一梯队成员: 145 行承载 7 个原则节 + 5 张表 + 1 棵可裁决决策树，事实面零错误，SCORING 映射 100%，完全自包含。它的全部缺陷都集中在"结构欠账"而非"内容欠账": 三必需节全缺（dossier 未验证、本次确认）、SCORING 正则转义层级错误（双文件解析后语义不等，若 runner 通用驱动则 3 错 1 崩）、三处脚本判定无正文锚点。修复成本是语料库中最低档之一（🔴 四项约 2 小时），完成后合规 12/12、判定全稳、预期 85+。审查中重点关注了三件事: 必需节完整性对 dossier 🟢 评级的修正、正则转义不一致在两种 runner 模式下的真实影响、以及正文锚点与脚本判据之间的传导风险。综合 77/100 的构成中，逻辑一致性与内容密度贡献了主要得分；本 skill 距离 🟢 只差"补三节 + 改四个反斜杠"。
