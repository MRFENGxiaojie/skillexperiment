# REVIEW: 193-game-audio

**审查日期**: 2026-08-06
**Skill 类型**: reference — 游戏音频原则参考（声音设计、音乐集成、自适应音频、3D 音频、混音）
**Body 行数**: 181 行 | **参考文件数**: references/0, scripts/0, 其他/0
**对应 dossier**: 🟡（"总评: 🟡"，本审查核实后维持）
**审查范围**: SKILL.md、SCORING.yaml、check.py 全量阅读；无 references/scripts 子目录；对照 _shared/SKILL-SPEC.md v1.0 与 memory/skill-dossier.md 中 193 条目
**结论**: 🟡 **B-** (73/100)。内容准确、结构干净、无事实错误，但作为 reference 型技能缺失全部三必需节（Workflow/Output Format/Scope），check.py 为空实现，SCORING 中 NEG-01 存在跨域模板残留措辞；修复后可达 🟢。

---

## 1. 目录全量清单

```
193-game-audio/
├── SKILL.md        187 行  (frontmatter L1-5，正文 L7-187 = 181 行)
├── SCORING.yaml    155 行  (skill/pattern/total_items + 17 判据 + 2 critical_failures)
└── check.py         68 行  (0 项脚本检查的空实现)
```

全目录仅 3 个文件，无 `references/`、无 `scripts/`、无模板、无隐藏文件。全部文件均已逐行阅读：

| 文件 | 行数 | 角色 | 审查结论 |
|---|---|---|---|
| `SKILL.md` | 187 | 技能主文件（正文 181 行） | 🟡 内容准确、表格体系清晰；缺三必需节 |
| `SCORING.yaml` | 155 | 测评标准（17 项判据） | 🟡 与正文逐条对应；NEG-01 措辞异常 |
| `check.py` | 68 | 脚本检查（0 项） | 🟡 空实现，全部判据交给 llm judge |

---

## 2. Frontmatter 逐字段审查

### 2.1 name（L2）

`game-audio`。小写字母 + 连字符，10 字符 ≤64，与目录名 `193-game-audio/` 的技能名部分完全匹配（SKILL-SPEC §1.1、§4）。**通过**。

### 2.2 description（L3）

完整引用：

> "Game audio principles. Sound design, music integration, adaptive audio systems. Use when the user asks about game sound design, music integration, adaptive or dynamic audio, 3D audio, audio mixing, or audio formats and budgets for games."

逐要素分析：

- **WHAT**（§2.1）: "Game audio principles. Sound design, music integration, adaptive audio systems" — 明确的能力域声明，非泛化描述。通过。
- **WHEN**（§2.1）: "Use when the user asks about game sound design, music integration, adaptive or dynamic audio, 3D audio, audio mixing, or audio formats and budgets for games" — 6 个触发分支，具体且与正文 8 节一一对应（sound design→§2、music integration→§3、adaptive→§4、3D audio→§5、mixing→§7、formats/budgets→§6）。通过。
- **KEYWORDS**（§2.1）: sound design、music integration、adaptive audio、3D audio、audio mixing、audio formats 等术语齐备，检索性良好。通过。
- **第三人称**（§2.3）: 无 "Use this skill to..."、"I can..."、"You can..." 句式。通过。
- **触发信号短语**（§2.4）: 含标准信号 "Use when the user asks about"。通过。
- **无跨技能路由**（§2.5）: 无 "NOT for X, use Y instead" 句式。通过。
- **长度**（§1.1，≤1024）: 约 290 字符。通过。
- **小瑕疵**: "Game audio principles." 以句号结束的短句 + 名词短语堆叠，比 051-statsmodels 式完整句更凝练，可接受；"the user asks about" 分支覆盖了正文全部 8 节，无过度触发的宽泛分支（如 "asks about audio"）。无需修改。

### 2.3 allowed-tools（L4）

`allowed-tools: Read, Glob, Grep` — 逗号分隔格式符合 §1.2。

- **Read**: reference 型技能读取文件必需。必要。
- **Glob**: 查找项目音频资产/目录结构时有用。合理。
- **Grep**: 检索音频配置、代码中的播放调用时有用。合理。

本技能是纯问答参考型（SCORING 全部 17 项判据均为 llm judge，无脚本执行要求），不需要 Write/Bash；只读工具集与技能职责匹配。**通过**。

### 2.4 其他字段

frontmatter 仅 `name`、`description`、`allowed-tools` 三个键，全部在 §1.2 允许列表中；无 metadata、version、trigger、tools、category、tags 等任何禁用键（§1.3 清单逐项比对）。**通过**。

### 2.5 YAML 语法

三键均为 `key: value` 平铺格式，无引号嵌套、无列表、无多行字符串；description 中无冒号空格歧义（"adaptive or dynamic audio, 3D audio" 无 `: ` 序列）。可被标准 YAML 解析器正确解析。**通过**。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

正文 181 行（L7-187），结构树：

```
# Game Audio Principles (L7)
├── > 引言块引用 (L9)                  "Sound design and music integration for immersive gaming experiences."
├── ## 1. Audio Category System (L13)
│   ├── ### Category Definitions (L15)     5 类音频表（Music/SFX/Ambience/UI/Voice）
│   └── ### Priority Hierarchy (L25)       code block 优先级 1-5
├── ## 2. Sound Design Decisions (L39)
│   ├── ### SFX Creation Approach (L41)    4 方案表（Recording/Synthesis/Library/Layering）
│   └── ### Layering Structure (L50)       4 层表（Attack/Body/Tail/Sweetener）
├── ## 3. Music Integration (L61)
│   ├── ### Music State System (L63)       ← 空标题（缺陷，见 3.4/4.2）
│   ├── ### Game State -> Music Response (L65)  7 条游戏状态→音乐映射
│   └── ### Transition Techniques (L74)    5 技法表（Crossfade/Stinger/Stem/Beat-synced/Queue point）
├── ## 4. Adaptive Audio Decisions (L86)
│   ├── ### Intensity Parameters (L88)     5 参数表（Threat/Health/Speed/Environment/Time of day）
│   └── ### Vertical vs Horizontal (L98)   3 行系统表
├── ## 5. 3D Audio Decisions (L108)
│   ├── ### Spatialization (L110)          6 元素 3D 定位判定表
│   └── ### Distance Behavior (L121)       4 档距离行为表
├── ## 6. Platform Considerations (L132)
│   ├── ### Format Selection (L134)        4 平台格式表
│   └── ### Memory Budget (L143)           3 游戏类型预算表
├── ## 7. Mix Hierarchy (L153)
│   ├── ### Volume Balance Reference (L155)  5 类相对电平表
│   └── ### Ducking Rules (L165)           3 场景闪避表
├── ## 8. Anti-patterns (L175)             Don't/Do 5 行对照表
└── > 结尾块引用 (L187)                    "50% of the game experience is audio..."
```

### 3.2 必需章节（Workflow/Process、Output Format、Scope/Limitations）

对照 SKILL-SPEC §3.1，三必需节**全部缺失**：

1. **Workflow / Process** — **缺失**。正文没有任何步骤式过程：没有 "## Workflow"、"## Process"，也没有 Quick Start。§1-§8 全部是知识表（是什么、怎么选），没有"遇到任务后先做什么、再做什么"的执行序列。对 reference 型技能而言，判据对应的"过程感"（如"检测到声音竞争→按优先级裁决"）只隐含在 Priority Hierarchy 的代码块里，未显式化为步骤。
2. **Output Format** — **缺失**。没有任何节描述"用户拿到什么"：没有报告格式、交付物清单、回答结构约定。SCORING 的 OUT-01/OUT-02 要求 agent 给出"具体可操作的建议"并"标记反模式"，但正文没有规定输出形态。
3. **Scope / Limitations** — **缺失**。没有"不处理什么"（如：不做音色设计文件制作、不覆盖音频中间件（Wwise/FMOD）操作细节、不处理语音合成）与"何时不用"的边界声明。description 的触发分支是唯一的"何时用"，反向边界为零。

这是本技能最大的结构缺陷，与 031-tailwind-patterns、082-mobile-games 同型（dossier 对同类纯参考表技能判 🟡）。

### 3.3 内容委托

**无委托**。正文 181 行全部自含，无 `references/` 引用、无 `scripts/` 调用、无外部文件依赖。对 181 行的参考型技能，内容全部内联是可接受的（§3.2 规模目标 ~300 行内无需下沉）；但这也意味着缺失的必需节没有"由参考文件补位"的余地。

### 3.4 标题层级

- 层级总体规范：1 个 H1 + 8 个 H2（编号 1-8）+ H3 成对出现，编号连续无跳号。
- **缺陷 1（L63-65）**: `### Music State System`（L63）之后紧接 `### Game State -> Music Response`（L65）——第一个 H3 没有任何正文内容就进入第二个 H3，形成"空标题 + 连续 H3"。且第二个标题用 ASCII 箭头 `->` 而非规范措辞，与全文档其他标题风格（名词短语）不一致。应合并为 `### Music State System` 直接接状态映射列表，或去掉一个 H3。
- **缺陷 2**: 标题层级只有 H1/H2/H3 三级，无 H4，无越级。

### 3.5 vs 600 行

正文 181 行，远低于 600 行硬限（§3.2），也低于 reference 型典型规模。规模健康，无膨胀。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接

本技能无显式步骤（§3.2 已证），故"步骤衔接"维度降级为**知识表之间的引用关系**审查：

- 类别系统（§1）→ 优先级（§1.2）→ 混音电平（§7.1）→ 闪避（§7.2）：四者构成一条完整决策链，agent 可从"分类→定优先级→定电平→定闪避"顺链作答，无断链。
- SFX 创建（§2.1）→ 分层结构（§2.2）：方案与层结构配套给出，衔接自然。
- 音乐状态（§3.2）→ 过渡技法（§3.3）：状态映射与过渡表配对，无交叉引用错误。
- 自适应参数（§4.1）→ 垂直/水平系统（§4.2）：参数表引用的"强度缩放"与 Vertical 系统描述一致。
- 3D 定位（§5.1）→ 距离行为（§5.2）：定位判定表与距离衰减表互补，无矛盾。
- 平台（§6）→ 预算（§6.2）：格式选择与预算策略配套，无冲突。

**结论**: 8 节之间无指向性断链，决策链完整。

### 4.2 内部矛盾

- **优先级顺序差异（轻微）**: §1.2 Priority Hierarchy 顺序为 Voice > Player SFX > **Enemy SFX** > Music > Ambience；§7.1 混音表行序为 Voice、Player SFX、**Music**、Enemy SFX、Ambience。两处排列顺序不同。由于二者量纲不同（竞争裁决 vs 相对电平），数值不冲突（Enemy -6~-9 dB 与 Music -6~-12 dB 有重叠区间），不构成逻辑矛盾，但阅读时"优先级第二是 Enemy 还是 Music"会轻微晃眼。建议统一两表行序。
- **空标题**: L63 `### Music State System` 无正文（见 3.4），视觉上像"正文丢失"，是格式缺陷而非逻辑矛盾。
- **数值一致性核查**: 全文出现的全部数值——优先级 5 级、Attack/Body/Tail/Sweetener 4 层、3-5 个变体、PC/Mobile/Web/Console 4 平台、10-50MB/100-500MB/1+GB 3 档预算、0dB/-3~-6/-6~-12/-6~-9/-12~-18 电平、-6~-9dB 闪避量——与 SCORING.yaml 判据中出现的数值逐一比对，**全部一致**（详 §10.1）。

### 4.3 示例/代码正确性

- 唯一代码块（L27-35 Priority Hierarchy）是伪代码注释文本，无语法可验证，无错误。
- 8 张表格的 5W 结构（Category/Behavior/Examples 等列）全部填满，无空单元格。
- 事实层面抽查：MP3/AAC 用于移动端（MP3 专利已过期，无授权问题，正文未提授权细节，无误导）；WebM/Opus 用于 Web（浏览器支持面正确）；"Console 平台专有格式 + 认证"表述准确；"Near/Mid/Distant/Max 距离衰减 + low-pass"符合音频行业标准做法。**未发现事实错误**。

### 4.4 条件完整性

- 优先级代码块覆盖了"当声音竞争通道时"的唯一前置条件，条件与结果（1-5 级）完整。
- SFX 方案表的"何时使用"列 4 分支互斥完整（真实感/科幻与复古/快速生产/复杂声音）。
- 闪避表的 3 个触发条件（语音、爆炸、菜单）各自带独立闪避量，无重叠冲突。
- 距离行为的 4 档覆盖 0 到最大听距全区间。
- **缺口**: 未定义"当平台是混合平台（如 PC 同时出 Web 版）"与"预算超限时如何降级"的交叉条件——属优化级而非缺陷。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

本技能**无任何文件引用**（SKILL.md 全文无 `references/`、`scripts/`、`../` 路径），SCORING.yaml 与 check.py 亦无文件路径引用。矩阵为空——没有引用，也就没有"引用断裂"风险。

### 5.2 不可见资源审计

- SCORING.yaml 未引用任何正文之外的文件（全部 17 项判据的 evidence 都是 "Agent's answer..."），无"隐藏依赖"。
- check.py 仅依赖 `_shared/checker.py`（已验证存在于 `complex-skills/_shared/`），无其他运行时资源。
- 正文声称的知识点全部内联，无"指向未提供文件"的悬空承诺。
- **结论**: 无可访问性缺口。

### 5.3 文件全文审查

目录无 `references/`、`scripts/` 子目录，本节无对象。作为替代，本审查对"唯一知识载体"——正文 8 张表 + 2 个代码块——逐表核对完毕（§4.2 数值核查 + §4.3 事实核查），未发现死数据或与 SCORING 冲突的条目。

### 5.4 跨 Skill 引用

无 `../` 路径、无其他技能名、无跨技能资源依赖（§7 清单第 11 项通过）。**唯一异常**在 SCORING.yaml 的 NEG-01（L123-129）：

> "Agent did NOT recommend mono-purpose patterns (e.g., polling for real-time, ignoring voice priority)"

- "mono-purpose" 非标准英文（标准说法是 single-purpose / monolithic），措辞生造。
- "polling for real-time"（轮询实现实时性）在音频语境中无意义——轮询是事件/数据系统反模式，与游戏音频（实时音频由引擎回调驱动）无关。该例句疑似从其他领域（实时系统/事件架构类）技能的 NEG 判据模板复制残留，仅第二例 "ignoring voice priority" 与本技能相关。
- 影响: 判据本身仍可被 llm judge 解释执行，但语义噪音会降低评分一致性（不同 judge 对该例句的理解可能发散）。建议改写（见 §13）。

### 5.5 嵌套重复/死文件

- 无重复内容：8 节各司其职，Priority Hierarchy 与 Mix Hierarchy 是互补而非重复（§4.1 已述）。
- 无死文件：3 个文件全部被使用（check.py 由 runner 调用、SCORING 由评分调用、SKILL.md 为技能本体）。
- 无嵌套目录。

---

## 6. 语法与格式质量

### 6.1 拼写

全文英文拼写规范，无拼写错误。专业术语（crossfade、ducking、sweetener、stinger、stem mixing、beat-synced）大小写与拼法统一。SCORING.yaml 拼写亦正确（唯一异常为 "mono-purpose"，§5.4）。

### 6.2 语法

正文为名词短语 + 短句风格（表格驱动），无长难句、无病句。唯一语法层面的非标准表达是 L63-65 的标题衔接（§3.4 已述）。

### 6.3 中英/葡英混杂

全英文，无中文、无葡萄牙语混入（本语料中 306、262、038 等技能存在葡语残留，本技能无此问题）。

### 6.4 Markdown 破损

- 表格全部使用规范 `|` 分隔 + `|------|` 分隔行，8 张表无破损。
- 代码块使用 ```` ``` ```` 围栏，2 处均闭合。
- **唯一破损点**: L63 空 H3 紧跟 L65 第二个 H3（渲染后出现一个无内容标题），见 §3.4。
- L187 结尾块引用闭合正确。

### 6.5 占位符

全文无 `TODO`、`FIXME`、`...` 占位、`{{xxx}}` 模板变量残留、`<placeholder>`。SCORING.yaml 与 check.py 亦无占位符。

### 6.6 截断

- SKILL.md 以完整句 "A muted game loses half its soul." 结尾，无截断迹象。
- SCORING.yaml 以 CF-02 的 `effect: cap_to_0` 完整收尾（L155）。
- check.py 以 `main()` 块完整收尾（L68）。
- 三文件均无"文件中途停止"或"残缺句尾"。

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 结果 | 依据 |
|---|---|---|---|
| 1 | name 小写+连字符、≤64、匹配目录 | ✅ | L2 `game-audio` = 目录技能名，10 字符 |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✅ | L3 约 290 字符，三要素齐备 |
| 3 | description 无命令式/一二人称开头 | ✅ | L3 以名词短语 "Game audio principles." 开头 |
| 4 | description 无跨技能路由 | ✅ | 无 "NOT for X" 句式 |
| 5 | description 至少一个触发信号短语 | ✅ | "Use when the user asks about" |
| 6 | frontmatter 无禁用键 | ✅ | 仅 name/description/allowed-tools 三键 |
| 7 | 正文 ≤600 行 | ✅ | 正文 181 行 |
| 8 | 正文有 workflow/process 节 | ❌ | 纯知识表，无任何过程性节（§3.2） |
| 9 | 正文有 output format 节 | ❌ | 无交付物/输出形态描述 |
| 10 | 正文有 scope/limitations 节 | ❌ | 仅 description 正向触发，无反向边界 |
| 11 | 正文无跨技能文件引用 | ✅ | 全文无 `../`、无其他技能路径 |
| 12 | 目录 NNN-kebab-case 无大写无空格 | ✅ | `193-game-audio/` |

**9/12 通过，3/12 不通过**。三项不通过均属"结构缺失"而非内容违规。与其他纯参考表技能（031、082、176）同型，按规格字面判定不合规；dossier 判 🟡 与本审查一致。

其余规格条文：§3.3 文件引用（无引用项，无 `../`）；§3.4 知识增量（正文未重复基础声学常识，直接给决策表，符合"Knowledge delta over redundancy"；"Decision trees over prose" 一项以表格形式落地，比列表更优，通过）；§1.3 附注（无 Metadata 尾节需求）。

---

## 8. 人机感评估

### 8.1 Emoji

正文 0 个 emoji。SCORING.yaml 0 个 emoji。check.py 0 个。全包无装饰性图标（对比 072-mobile-design 的 20+ emoji，本技能完全干净）。

### 8.2 喊叫式语言

无全大写命令、无 "STOP!"、"MANDATORY"、"CRITICAL" 式喊叫。唯一大写是专业术语（Music/SFX/Ambience/UI/Voice、AAA、OGG、EPSG 类专名）与表格列名，属正常用法。

### 8.3 Persona 语气

**无 persona**。正文是中性技术参考文体，无 "You are a..." 角色设定、无激励式口吻、无营销腔。结尾格言 "50% of the game experience is audio. A muted game loses half its soul." 是行业名言式收束（该说法常见于游戏音频行业演讲），语气适度，不油腻。

### 8.4 人机边界

纯知识供给型技能，无与用户交互的指令（无提问、无确认、无闸门设计）——对 reference 型技能这是合理的边界设定（agent 的角色是"答"，不是"问"）。无越权指令（没有要求 agent 擅自修改音频文件或调用外部工具）。

### 8.5 人称分析

正文 0 处第一人称、0 处第二人称、0 处命令式祈使（§2.2 已证 description 同）。全文严格第三人称。这在 322 语料中属于人称最干净的一档。

### 8.6 表格太多→自然语言

正文 181 行中表格占约 150 行（8 张表 + 2 代码块），**表格密度约 83%**，是典型的"表格优先"型文档。评估：
- **优点**: 决策信息（分类、方案、电平、预算）天然适合表格，检索效率高，与 SCORING 判据的"数值对应"设计（§10.1）配合良好。
- **缺点**: 表格之间缺少自然语言"胶水"——每节只有标题 + 表格，没有 1-2 句引导语解释"何时使用本节、与其他节的关系"。例如 §7 Mix Hierarchy 没有说明"与 §1 优先级的关系"，读者（agent）第一次阅读时需自行推断。
- **建议**: 每节表格前补 1-2 句引导语（如 §7 开头："Mix hierarchy operationalizes the priority hierarchy: levels encode priority into the mix."），可将可读性从"可用"提升到"易用"。属优化级。

---

## 9. 可执行性评估

### 9.1 独立可执行性

reference 型技能不要求"运行"，其可执行性 = agent 能否仅凭正文回答 8 类问题。核查：SCORING 17 项判据的问题域（分类、优先级、SFX 方案、音乐状态、自适应、3D、平台格式、预算、电平、闪避、反模式）在正文 8 节中**全部有对应知识**，无判据落空（逐项矩阵见 §10.1）。**通过**。

### 9.2 步骤可操作性

无步骤可评估（§3.2）。对应判据 PROC-01~PROC-10 全部是"agent 输出是否正确应用知识"而非"agent 是否执行步骤"，与技能形态匹配。**无缺陷**。

### 9.3 工具依赖

- 技能运行: 仅需 Read/Glob/Grep（allowed-tools 已声明），agent 可纯对话回答，零工具依赖也可完成。
- 测评运行: check.py 依赖 `_shared/checker.py`（存在 ✓）；check.py 本身 `main()` 对 agent_output 的路径/文本双态处理（L22-27、L57-59）与 corpus 标准一致，可直接由 runner 调用。
- **缺陷**: check.py 返回 `{}`（空 dict，L46）。runner 若期望按 `{criterion_id: bool}` 逐项合并，空结果意味着 17 项全部依赖 llm judge——功能上成立（SCORING 注释已声明 "llm judge (not checked here)"），但意味着本技能**没有任何机器可验证的检查项**，评分完全依赖 judge 一致性。属设计选择，风险在于 llm judge 的波动无 script 兜底。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

- `pattern: reference`（L2）与技能形态匹配 ✓；`total_items: 17`（L3）与判据计数核对：SCOPE 2 + PROC 10 + OUT 2 + NEG 2 + QA 1 = **17** ✓，无多无漏。
- 类别分布: scope 12%、process 59%、output 12%、negative 12%、qa 6%——process 权重压倒性，符合"知识应用正确性"型测评目标。
- **17 项判据 ↔ 正文逐项对应矩阵**:

| 判据 | 对应正文 | 数值一致性 | 判定 |
|---|---|---|---|
| SCOPE-01 游戏音频原则 vs 通用音频工程 | 全正文 | — | ✅ |
| SCOPE-02 识别问题类别并对应章节 | §1-§8 结构 | — | ✅ |
| PROC-01 类别行为（循环/单发/3D/优先级/闪避） | §1.1 表 | 5 类一致 | ✅ |
| PROC-02 优先级 Voice>Player>Enemy>Music>Ambience | §1.2 块 | 5 级一致 | ✅ |
| PROC-03 SFX 方案 + 分层 | §2.1/2.2 表 | 4 方案 + 4 层一致 | ✅ |
| PROC-04 音乐状态 + 过渡技法 | §3.2/3.3 | 7 状态 + 5 技法一致 | ✅ |
| PROC-05 自适应参数 + 垂直/水平 | §4.1/4.2 | 5 参数一致 | ✅ |
| PROC-06 3D 定位 + 距离行为 | §5.1/5.2 | 6 元素 + 4 档一致 | ✅ |
| PROC-07 平台格式 | §6.1 表 | OGG/WAV/MP3/AAC/WebM 一致 | ✅ |
| PROC-08 内存预算 | §6.2 表 | 10-50/100-500/1+ GB 一致 | ✅ |
| PROC-09 混音电平 | §7.1 表 | 0/-3~-6/-6~-12/-12~-18 一致 | ✅ |
| PROC-10 闪避规则 | §7.2 表 | -6~-9/-3~-6 一致 | ✅ |
| OUT-01 建议具体可操作 | 全正文数值 | — | ✅ |
| OUT-02 标记反模式 | §8 表 | 5 条一致 | ✅ |
| NEG-01 无单一用途模式 | 无正文对应 | **措辞异常（§5.4）** | ⚠️ |
| NEG-02 不把音视频/DSP 概念当游戏音频规则 | — | — | ✅ |
| QA-01 准确引用正文数值 | 全正文 | — | ✅ |

14/17 判据与正文**数值级**一一对应（这在 322 语料中属于对应质量最高的之一）；NEG-01 措辞异常但不破坏功能；SCOPE-01/NEG-02 为定性判据，无对应缺失。

- **判据质量隐患**: 全部 17 项为 llm judge，无一项 script judge。与 192（7 项 script）对比，本技能缺"最低限度的机器校验"，llm judge 的主观波动完全无兜底——对评测工程而言是设计薄弱点（§9.3 同述）。

### 10.2 Critical Failures

- **CF-01**（L149-151）: "Advice contradicts the core system — e.g., voice given lower priority than music, or spatializing UI sounds" → cap_to_0。与正文 §1.2（Voice 最高）与 §5.1（UI 非 3D）直接绑定，抓的是"知识应用反转"型致命错误，定义准确、可判定。✅
- **CF-02**（L153-155）: "Recommendation omits category/priority thinking entirely" → cap_to_0。抓"完全不用分类/优先级框架"型失败，与 SCOPE-01 互补（SCOPE-01 管"用错框架"，CF-02 管"不用框架"）。✅
- 两条 CF 与正文核心机制（类别系统 + 优先级）绑定，无一为空转条款。**对齐良好**。
- 轻微问题: CF-01 的 example 与 NEG-01 第二例（"ignoring voice priority"）语义重叠——同一行为在两个条款中出现，llm judge 评分时可能重复扣分或混淆归属。建议 NEG-01 例句改用非优先级示例（如"把单通道混音当立体声定位处理"）。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier 176-200 批次记录（L968-973 摘要行）："192-194 内容可靠"，193 条目（skill-dossier.md 中）记：

> "总评: 🟡"

**逐维复核**:

- **"内容可靠"** — ✅ 与本审查 §4.3 一致：8 张表无事实错误，数值自洽，SCORING 与正文逐条对应（§10.1 矩阵 14/17 数值级一致）。
- **"总评 🟡"** — ✅ 维持。本审查独立评估 73/100（B-，🟡），与 dossier 评级一致。
- **dossier 遗漏项**（本次审查新增发现，dossier 未记录）:
  1. 三必需节（Workflow/Output/Scope）全缺——dossier 176-200 批次摘要仅以"内容可靠"概括，未指出结构不合规 9/12；
  2. L63 空 H3 连续标题缺陷；
  3. SCORING NEG-01 "mono-purpose/polling for real-time" 跨域模板残留措辞；
  4. check.py 全空实现、零 script 判据的设计风险；
  5. §1.2 与 §7.1 优先级行序不一致（轻微）。
- **dossier 与本文差异**: 无评级冲突；本文提供了 dossier 未覆盖的结构缺陷清单。

---

## 12. 综合评分（8 维加权 + 等级）

| 维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| 内容准确性 | 0.18 | 8.0 | 8 张表无事实错误、数值自洽；SCORING 17 判据与正文数值级对应 |
| 内容完整性 | 0.12 | 6.0 | 领域知识覆盖完整，但三必需节（workflow/output/scope）全缺 |
| 结构组织 | 0.10 | 7.5 | 8 节编号清晰、表格体系好；L63 空 H3 瑕疵 |
| 人机感/语气 | 0.10 | 9.0 | 零 emoji、零喊叫、纯第三人称，全语料最干净一档 |
| 可执行性 | 0.15 | 8.0 | reference 型：17 判据全部有正文落点，可独立作答 |
| 参考文件质量 | 0.12 | 6.5 | 无参考文件（单文件技能）；内容内联无遗漏，但无扩展体系 |
| 规范合规 | 0.13 | 6.0 | 12 项清单 9/12，frontmatter 满分，三必需节缺失 |
| 测评适配 | 0.10 | 7.5 | SCORING 结构规范、CF 与正文绑定；零 script 判据、NEG-01 措辞异常 |

**加权计算**:
0.18×8.0 + 0.12×6.0 + 0.10×7.5 + 0.10×9.0 + 0.15×8.0 + 0.12×6.5 + 0.13×6.0 + 0.10×7.5
= 1.440 + 0.720 + 0.750 + 0.900 + 1.200 + 0.780 + 0.780 + 0.750 = **7.32 → 73/100**

**等级判定**: A ≥ 85，B 70-84，C 55-69，D < 55。73 分 → **B-，对应 🟡**，与 dossier 一致。

**评级说明**:
- 若完成 §13 的 🟡 层修复（补三必需节 + 修空标题 + 改 NEG-01），预计 85-88 分 → **A- / 🟢**，即"补齐结构后进入 🟢 档"。
- 扣分集中于"结构完整性"与"规范合规"两个结构性维度；内容质量本身（准确性 + 人机感）是本技能最强项。

---

## 13. 修复建议（按优先级分层）★重点★

### 🔴 致命缺陷

本技能**无致命缺陷**——无事实错误、无崩溃代码、无引用断裂、无截断、无危险建议。以下 🟡 层是全部待办。

### 🟡 重要缺陷

**🟡-1: 补 `## Scope / Limitations` 节（最高优先）**

- **位置**: 建议插在 `## 1. Audio Category System`（L13）之前，作为第 0 节或独立节。
- **要点**（8-15 行即可）:
  1. **不处理**: 音频中间件（Wwise/FMOD）的项目级配置与事件搭建、语音合成/TTS、音乐作曲（本技能给"音乐集成"决策而不教作曲）、音频文件制作（录音/混音工程操作）；
  2. **不适用**: 非游戏音频场景（影视配乐、播客、语音聊天），以及"用户明确指定某中间件/引擎（如 Unity AudioMixer 具体项目）"的场景——此时以引擎文档为准；
  3. **边界澄清**: 本技能给"原则与决策表"，具体音效制作（如用哪款合成器）不在范围内。
- **依据**: SKILL-SPEC §3.1 第三必需节；补后合规清单 10/12。

**🟡-2: 补 `## Output Format` 节**

- **位置**: 建议放在 `## 8. Anti-patterns`（L175）之后、结尾块引用之前。
- **要点**: 规定"每次回答的交付形态"——(1) 分类声明：先说该声音属于哪类（Music/SFX/Ambience/UI/Voice）及其行为含义；(2) 决策链：按 优先级→方案→电平→闪避 顺序给出建议；(3) 具体数值：格式、预算、dB 值必须引用本技能表格（对应 QA-01）；(4) 反模式检查：若用户设计含 §8 反模式，必须指出。8-12 行。
- **依据**: SKILL-SPEC §3.1 第二必需节；同时把 OUT-01/OUT-02 判据的预期行为显式化。

**🟡-3: 补 `## Workflow / Process` 节**

- **位置**: 建议插在引言块引用（L9）之后。
- **要点**（10-15 行）: 定义标准回答流程——Step 1 识别音频类别（§1）；Step 2 按类别套行为（循环/单发/3D/优先级）；Step 3 若涉及竞争通道，套优先级层级（§1.2）；Step 4 涉及平台/预算时套 §6；Step 5 涉及混音时套电平与闪避（§7）；Step 6 检查反模式（§8）。把散落在各表的"隐性决策链"（§4.1 已识别）显式化。
- **依据**: SKILL-SPEC §3.1 第一必需节；补后合规清单 11/12。

**🟡-4: 修复 L63 空 H3 + 连续标题**

- **位置**: SKILL.md L63-65。
- **方案**: 删除空标题 `### Music State System`（L63），把 `### Game State -> Music Response`（L65）改为规范的 `### Game State → Music Response` 或直接并入 Transition Techniques 前导。若保留 `->`，至少统一全文档箭头风格（全文档仅此处用 `->`）。
- **改动量**: 1-2 行。

**🟡-5: 重写 SCORING.yaml NEG-01 的措辞**

- **位置**: SCORING.yaml L123-129。
- **问题**: "mono-purpose patterns (e.g., polling for real-time, ignoring voice priority)"——"mono-purpose" 生造词 + "polling for real-time" 跨域残留例句（§5.4）。
- **方案**: 改为 "Agent did NOT recommend anti-patterns unrelated to the audio category system (e.g., treating a one-shot SFX as a looping track, or ignoring voice priority)"——保留与本技能相关的第二例，替换第一例为音频域内的反模式。
- **附带**: 将 CF-01 的 example（"ignoring voice priority"）与 NEG-01 第二例去重——CF-01 保留优先级例句，NEG-01 只保留"单发当循环"类例句。

### 🟢 优化建议

1. **统一 §1.2 与 §7.1 的行序**: 两表按同一顺序（Voice → Player SFX → Enemy SFX → Music → Ambience）排列，消除阅读晃动（§4.2）。
2. **每节补 1-2 句自然语言引导**: 表格间加"胶水"句（§8.6），如 §7 开头说明"本节把 §1 的优先级编码为电平"。
3. **为 check.py 增加至少 1-2 项 script 判据**: 例如 PROC-07 平台格式可用 `output_contains('OGG|MP3|AAC|WebM')` 脚本化，给全 llm 的判据体系加最低机器兜底（§9.3/§10.1）。注意需同步 SCORING.yaml 的 judge 字段与 `total_items` 不变（judge 改为 script 即可）。
4. **description 可选微调**: 把 "3D audio" 改为 "3D audio spatialization" 提高检索特异性（可选，非必须）。
5. **补充混合平台与预算超限的降级规则**: §4.4 指出的条件缺口，一行表即可。

### 修复工作量估计

| 优先级 | 项数 | 预计改动行数 | 风险 |
|---|---|---|---|
| 🔴 | 0 | 0 | — |
| 🟡 | 5 | ~60（含三节新增正文 35 行 + 措辞/标题修复 5 行 + SCORING 10 行） | 极低 |
| 🟢 | 5 | ~20 | 极低 |
| 合计 | 10 | ~80 | — |

全部修复不触及 frontmatter 与目录结构；三节新增正文共约 35 行，修复后正文 ~215 行，仍远低于 600 行上限。修复后可复核（复核重点: 12 项合规清单是否全绿、NEG-01 可判读性、check.py 是否新增 script 判据）。

---

## 附录: 审查过程记录

- **审查方式**: 全量文件阅读（3/3 文件，413 行）+ 对照 SKILL-SPEC v1.0 与 skill-dossier.md 逐项复核 + 数值一致性人工比对（SCORING 17 判据 ↔ 正文 8 节）。
- **执行顺序**: 193 → 192 → 191（逆序批次）。
- **环境核查**: `complex-skills/_shared/checker.py` 存在（350 行）✓，check.py 依赖可解析。
- **时间**: 2026-08-06。
- **结论可信度**: 高——本技能无脚本可执行性验证需求（reference 型 + 全 llm 判据），人工阅读即可覆盖全部内容；唯一无法自动化验证的是 llm judge 的评分一致性，已作为风险在 §9.3/§10.1 标注。
- **审查中发现的 dossier 差异**: 见 §11（dossier 未记录结构缺失与 NEG-01 措辞问题，评级本身一致）。
