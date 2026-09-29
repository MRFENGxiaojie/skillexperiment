# REVIEW: 185-privilege-log-review

**审查日期**: 2026-08-06 | **Skill 类型**: review — 法律特权日志一审（三态分类 + 律师复核门 + 引用纪律）
**Body 行数**: 224 行（frontmatter 5 行；wc -l 计 229 行，末行为空行，body 实际内容 223 行）
**参考文件数**: refs/0, scripts/0, other/0（无 references/、scripts/、assets/ 目录；配套仅 SCORING.yaml + check.py）

---

## 1. 目录全量清单 (every file + line counts, tree format)

```
D:\SkillIF\skill-experiment\complex-skills\185-privilege-log-review\
├── SKILL.md           229 行（wc -l；CRLF 行尾；末行空行——byte 级实测以 \r\n\r\n 收尾）
├── SCORING.yaml       179 行
├── check.py            78 行
└── REVIEW.md          本次审查产物（新增）
```

- 共 3 个内容文件、486 行（wc -l 口径）。无隐藏文件、无 `.gitkeep`、无嵌套目录。
- 结构特征：**零参考文件、完全自包含** —— 全部判定规则（三态分类、in-house 法域矩阵、引用纪律、输出模板）内联于 body 224 行内。无 references/、无 scripts/、无 assets/。
- SKILL.md 与 SCORING.yaml 修改时间不同（SKILL.md 7-31，SCORING.yaml/check.py 8-05），说明 SKILL.md 先于测评配套定稿——两轮产物之间需做一致性核对（见 §10，核对结果一致）。
- 三文件均 UTF-8 无 BOM；SKILL.md/SCORING.yaml/check.py 全部 CRLF 行尾，无混合。

---

## 2. Frontmatter 逐字段审查

### 2.1 name — 匹配目录名/全小写连字符/≤64字符

- 值：`privilege-log-review`（19 字符）
- 目录名：`185-privilege-log-review` — 去除序号后完全一致 ✅
- 格式：全小写 + 连字符，无空格/大写 ✅
- 长度：19 ≤ 64 ✅
- PyYAML 实测解析成功，值类型 str ✅

### 2.2 description — 逐句分析

实际值（L3，271 字符 ≤1024 ✅）：

> "First-pass privilege log review — make the obvious privilege calls and flag the hard ones for attorney review without making close calls. Use when the user says "review the privilege log", "priv log", "check privilege on these docs", or has a log to QA before production."

| 句段 | 分类 | 评价 |
|------|------|------|
| S1 "First-pass privilege log review — make the obvious privilege calls and flag the hard ones for attorney review without making close calls." | WHAT | ✅ 名词短语开头 + 破折号引出行为界定。WHAT 非常具体：一审（first-pass）、只做明显判定（obvious calls）、困难项移交律师（attorney review）、不做接近判定（close calls）。"close calls" 与 body 三态规则（§4.1）精确呼应——描述与正文术语一致，语料库少见的高一致性。 |
| S2 "Use when the user says ... or has a log to QA before production." | WHEN + KEYWORDS | ✅ 四条触发信号（"review the privilege log"、"priv log"、"check privilege on these docs"、QA 场景）+ "the user" 显式主语。触发短语逐字可检索，满足 §7 第 5 项。 |

规范要点：
- 第三人称：S1/S2 均以名词短语和 "the user" 表述，无第一/第二人称 ✅。
- 无 imperative 开头（S1 为名词短语，S2 "Use when" 为语料库标准触发句式）✅。
- 无跨 skill 路由、无模糊表述 ✅。
- 长度 271 ≤ 1024 ✅。
- YAML 语法：plain scalar 内含 4 个字面双引号（"review the privilege log" 等）。plain scalar 中段引号合法，PyYAML 解析成功 ✅；但该写法与 102-ai-slop-detector 同类脆弱——若未来在引号后加入 `: ` 会破坏解析（属 🟢 级建议，见 §13）。

### 2.3 allowed-tools

- 未声明。SKILL-SPEC 中 allowed-tools 为可选字段，未声明 = 默认全量工具集，合规 ✅。
- 功能性评估：本 skill 的执行依赖法律研究连接器（Westlaw/CourtListener/Trellis/Descrybe，见 §5.2）。未收紧 allowed-tools 与该依赖相容——若强行限定 Read/Glob/Grep 反而会阻断 SCOPE-03 的 tool_log 命中。**不声明是当前正确选择**。

### 2.4 其他 frontmatter 字段

- 仅 name + description + argument-hint 三字段。
- `argument-hint: "[log file, or document set]"` —— SKILL-SPEC 允许字段，格式为方括号包裹的占位提示，内容与功能匹配（输入是日志文件或文档集）✅。
- 逐项核对 SKILL-SPEC §1.1 允许字段清单（name/description/allowed-tools/argument-hint/user-invocable/model/paths/disable-model-invocation）：无 metadata/license/version/tags/related-skills 等任何 forbidden keys ✅。

### 2.5 Frontmatter 语法

`---` 定界、L4 关闭、三字段齐全。全文 `yaml.safe_load` 在 L13 的 `---`（正文水平线）处会报 multi-document 错误——与 102-ai-slop-detector 相同模式：标准 frontmatter 感知解析器（取首对 `---`）不受影响，属 🟢 级已知脆弱性，非本 skill 特有。

---

## 3. Body 逐段结构分析

### 3.1 段落清单 — 目录树+行数

```
# Privilege Log Review                            L6（H1 #1 — quick-start 区标题）
  [4 条编号指令 quick-start]                      L8-11
--- （水平线）                                     L13
# Privilege Log Review                            L15（H1 #2 — 正文标题，重复！）
## Disclosed-document use restrictions            L17-25（CPR 31.22/US 保护令/其他法域）
## Matter context                                 L27-29（matter workspace 路由）
---                                               L31
## Purpose                                        L33-37（三态目的 + "first pass" 声明）
## Record fidelity — pinpoints and citation coverage  L39-51（pinpoint 纪律 + 5 步核查）
## Load context                                   L53-61（config 加载 + conflicts gate + 法域声明）
## Step 0: Research the forum's privilege-log rules   L63-76（研究步 + no silent supplement + 归因）
## The calls                                      L78-92（三态总则 + in-house 法域矩阵）
### Confidently privileged (✅)                    L94-99（4 类）
### Uncertain — keep designation AND flag (✅ + ⚠️)  L101-112（6 类 + flag 记录要求）
### Confidently not privileged (❌)                L114-124（5 类 + close 兜底）
## Workflow                                       L126-162
### Step 1: Format check                          L128-141（6 字段表 + 缺失→补全）
### Step 2: Entry-by-entry                        L143-154（输出格式 + 禁止静默剥离）
### Step 3: Pattern flags                         L156-162（重复/过度标记/描述不足）
## Output                                         L164-217（gate + 模板 + 免责声明）
## What this skill emphatically does not do       L219-224（4 条负向边界）
## Close with the next-steps decision tree        L226-228（决策树收尾）
```

共 12 个 H2 节 + 11 个 H3 节 + 2 个重复 H1。结构是一条清晰的执法流水线：**前置检查（disclosure 限制 → matter 上下文）→ 目的与纪律 → 加载上下文与冲突门 → Step 0 法域研究 → 三态判定标准 → 三步工作流 → 输出模板 → 负向边界 → 决策树收尾**。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

| 必需章节 | 状态 | 依据 |
|---|---|---|
| Workflow / Process | ✅ 显式 | "## Workflow"（L126）含 Step 1/2/3 三步；另有独立 "## Step 0"（L63）作前置研究步 |
| Output Format | ✅ 显式 | "## Output"（L164）含完整 markdown 输出模板（结果统计、三张表、marker discipline、来源声明） |
| Scope / Limitations | ✅ 变体 | "## What this skill emphatically does not do"（L219）命中 SKILL-SPEC L108 接受的变体清单（"What This Skill Does NOT Do"）；另有 "## Disclosed-document use restrictions" 与 "## Matter context" 两个前置边界节 |

**三节齐备**。注意：Scope 节未使用字面 "## Scope" 标题，而是"负向边界节 + 两个前置限制节"三处共同承担——按 SKILL-SPEC 变体规则判定合规，但 dossier 未记录此判断依据（§11）。

### 3.3 内容委托分析

- 委托对象（全部指向目录外）：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`（协议/格式/`## Outputs`/`## Who's using this`）、`matters/_log.yaml`（冲突门）、`matter.md`（matter 上下文）、`/litigation-legal:matter-intake` 与 `matter-workspace` 命令。
- 委托风险评估：**所有判定规则本体（三态、法域矩阵、引用纪律、模板）均在 body 内联**——即使外部 config 缺失，skill 的核心判定逻辑仍完整可执行。外部 config 只提供协议细节（日志格式、输出页眉、角色判定）与门控数据（matter 清单）。
- 但注意：`## Output` 的 gate 依赖读取 `## Who's using this` 中的 Role——若 config 缺失，agent 无法判定 Role，gate 行为未定义（§5.2/§9.3）。这是委托结构唯一的执行盲点。
- 结论：**高韧性委托** —— 委托的是格式细节而非判定能力，属优秀设计。

### 3.4 标题层级

- H1（×2）→ H2（12）→ H3（11），层级连续无跳级 ✅。
- 两个 H1 重复（L6 与 L15 内容完全一致）——quick-start 区标题与正文标题重复，属结构冗余（🟢，见 §13）。quick-start 的 4 条编号指令（L8-11）是"执行摘要"，正文才是完整指令——二者信息重叠但无矛盾。
- H3 全部挂在正确的 H2 之下（三态子节 ∈ ## The calls；Step 1-3 ∈ ## Workflow）✅。
- 无裸 H4、无错位层级 ✅。

### 3.5 vs 600 行硬限制

- body 224 行（wc 口径 229，含末尾空行 1）远低于 600 行上限，余量 376 行（63%）。
- 内容密度评估：224 行承载了法域矩阵、三态规则、5 步引用核查、输出模板、gate——密度极高但无堆砌感。未触发"内容下沉 references/"的需求，**零参考文件是合理选择**。

---

## 4. 逻辑一致性

### 4.1 步骤衔接

- **主流程自洽**：Disclosed-document 限制 → matter 上下文 → conflicts gate（Load context）→ Step 0 研究 → 三态判定（The calls）→ 三步工作流 → 输出 gate → 决策树。前置检查全部发生在判定之前，顺序正确。
- **quick-start 与正文编号不对应**：L8-11 的 4 条指令（1 Load / 2 Follow workflow / 3 For each entry / 4 Output）与正文 Step 0-3（0 研究 / 1 格式 / 2 逐条 / 3 模式）是两套编号体系。quick-start "2. Follow the workflow below" 所指的 workflow 在 L126 才出现，而 Step 0（L63）独立于 "## Workflow" 之外——**Step 0 在结构上不属于 Workflow 节**，但编号上属于（Step 0 → Step 1/2/3）。这是本 skill 唯一的结构性编号瑕疵（🟡，见 §13）。
- **三态体系全程一致**：✅（无 flag）/ ✅+⚠️（保号+flag）/ ❌（推荐移除）三态在 Purpose、The calls、Workflow Step 2、Output 模板（Results 计数三档）、"does not do" 五处表述完全一致，无第四种静默状态。dossier 所述"三态判定全程一致"**确认属实**（§11）。
- Step 2 输出格式（L147-152）与 Output 模板的三张表（L185-200）一一对应——条目级输出与汇总级输出的衔接闭环 ✓。

### 4.2 矛盾检查

- **"Attorney reviews every flag. No exceptions."（L37）vs ✅ 层无 flag 直接通过**：L92 明确说 ✅ 层"是设计来绕过律师审查的层级"。字面上"no exceptions"与 ✅ 层存在张力——但正文 L37 上下文是"首次审查 + 每个 flag 都经律师"，而 ✅ 的定义就是"明显到无需 flag"（L94-99 限定 4 类 + 法域例外）。可解，但措辞 "No exceptions" 建议弱化为 "Attorney reviews every ⚠️ and ❌ flag"（🟡，见 §13）。
- **in-house ✅ 示例 vs "never classify confidently privileged without stating regime"（L90）**：L97 的 ✅ 示例含"in-house counsel, clearly legal advice"，而 L90 要求声明法域体制。二者靠"规则在示例之上 + L92 非 US 法域无 ✅ 层"消解——逻辑自洽，但示例表未内嵌法域条件，依赖阅读顺序（🟢 提示级）。
- **"Produce or withhold documents. It advises"（L223）vs L174 "First-pass review ... do not require the gate"**：无矛盾——L174 明确区分"审查（无门）"与"服务/标注（有门）"，边界清晰，是本 skill 人机边界的最佳实践。
- **"SCOPE-03 要求 Westlaw/CourtListener/Trellis/Descrybe 之一** vs body L67 多列了一个 "firm platform"（公司平台）**：body 允许的第四种研究渠道不在 SCORING 判定词表中——使用 firm platform 的合规 agent 会漏过 SCOPE-03（🟡 评分缺口，见 §10.1）。
- 其余：waiver 双类型（L73-74）与 PROC-06 一致；"No silent supplement"（L67）与 QA-01 一致；marker 体系（L208-210）与 OUT-01 的 "Marker discipline" 模式一致。未发现实质逻辑矛盾。

### 4.3 代码正确性（check.py 78 行全文）

- **结构**：`check()` 执行 7 项 script 检查，注释与 SCORING 的 judge: script 声明一一对应（SCOPE-01/03、PROC-01/07/10、OUT-01/02）✅；llm 项全部注释说明，无遗漏 ✅。
- **正则一致性**（SCORING.yaml 与 check.py 交叉核对）：
  - SCOPE-01 `matters/_log\.yaml|_log\.yaml` —— YAML 双引号 `\\.` → 反斜杠转义为 `\.`，与 check.py 单引号 'matters/_log\\.yaml|_log\\.yaml' 产生的正则 `matters/_log\.yaml|_log\.yaml` 一致 ✅。
  - PROC-10 `Checked \d+ of \d+ citations` —— 与 body 模板 "Checked [N] of [M] citations" 句式对齐 ✅。
  - OUT-01 `Applicable rule|Entries reviewed|Pattern observations|Marker discipline` —— 前三个是模板加粗行首词，第四个是模板小节名，均可命中 ✅。
  - 其余 4 条逐条核对无转义漂移 ✅。
- **运行语义**：`main()` 对 agent_output 先 `os.path.exists` 判定文件/原文双路径——与 `_shared/checker.py` 的 `output_contains`（对 `_agent_output` 做 MULTILINE re.search）兼容 ✅。`check()` 内 try/except 包裹 `os.path.exists` 属冗余防御（该函数不抛 OSError），无害。
- **已知边界**：`tool_log_contains` 是对**整条 tool log 条目的 JSON 序列化**做正则匹配（checker.py `_log_search`）——意味着 SCOPE-01 要求 agent 真的发生一次含 "_log.yaml" 路径的读写工具调用，而非口头提及。这是评分可行性问题（§10.2），不是代码 bug。

### 4.4 条件完整性

- 三态穷尽性：✅ / ✅+⚠️ / ❌ 覆盖全部条目，且 L124 "If any of these is *close* ... it's uncertain, not ❌" 提供了 ❌→⚠️ 的唯一迁移路径，无遗漏状态 ✅。
- 法域条件完整：in-house 判定按 US/EU/Germany/UK/France-Belgium 五档给出（L84-88），非 US 时 ✅ 层禁用（L92）✅。
- waiver 条件：按 A/C 与 work-product 分型，[UNCERTAIN] 标记常驻直到律师确认（L76）✅。
- gate 条件：非律师角色 + 服务/标注行为 → 必须显式 yes（L166-174）✅；审查本身无门（L174）✅。
- 条件**缺失**处：Role 读取依赖外部 config（§3.3）；"其他法域"（L23）只给 "Check the local rule" 一句，无操作化步骤——对多法域 matter 是执行空洞（🟢）。

---

## 5. 参考文件内容级审查

### 5.1 引用矩阵（SKILL.md 目录外引用全量清单）

| 引用对象 | 位置 | 用途 | 目录内存在？ |
|---|---|---|---|
| `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` | L8/L55/L166/L177/L228 | 协议、priv log 格式、`## Outputs`、`## Who's using this`、决策树 | ❌ 目录外 |
| `matters/_log.yaml` | L57 | 冲突门数据源（SCOPE-01 判定依赖） | ❌ 目录外 |
| `matters/<matter-slug>/matter.md` | L29 | matter 上下文与覆盖项 | ❌ 目录外 |
| `/litigation-legal:matter-intake`、`matter-workspace` 命令 | L29/L59 | 冲突门路由与 workspace 切换 | ❌ 目录外（插件命令） |
| Westlaw / CourtListener / Trellis / Descrybe / firm platform | L67/L69 | 法域规则研究（SCOPE-03 判定依赖） | ❌ 外部工具 |

SKILL.md 对**目录内文件零引用**（无 references/ 可引）——引用面 100% 指向插件生态与外部工具。参考文件计数：refs/0, scripts/0, other/0。

### 5.2 不可见资源（body 假设存在、但不在 skill 包内的资源）

1. **litigation-legal 插件 CLAUDE.md** —— 被 6 处引用，承载协议/格式/角色/输出页眉。评估环境若不预置，gate 行为（L166）与工作产品页眉（L177）无法执行。
2. **matters/_log.yaml** —— SCOPE-01 的 tool_log 判定要求 agent 实际读取该文件。**评估环境必须预置此文件**，否则 SCOPE-01 恒败（评分可达性问题，见 §10.2）。
3. **法律研究 MCP 连接器**（Westlaw 等）—— SCOPE-03 要求 tool_log 中出现其一。若 harness 未挂载任何研究连接器，agent 无法通过任何合法手段命中该正则（除非在工具参数中字面提及，属无意义绕行）。**SCOPE-03 的可达性完全取决于环境装配**，这是本 skill 评分设计最大的外部依赖。
4. `matter.md`、`/litigation-legal:matter-intake` —— 冲突门流程（L57-59）与 CF-02 判定依赖。

以上 4 类不可见资源均不在 skill 目录内——审查结论：**skill 自身逻辑完备，但 2 项 script 评分（SCOPE-01/03）在缺装配环境下不可达**（见 §13 修复建议 I-1）。

### 5.3 文件全文审查（目录内 3 文件）

- **SKILL.md**（229 行）：全文已逐段审查（§2-§4）。内嵌内容载体共 3 个代码块/表组：L132-140 格式检查表（6 字段）、L147-152 逐条输出模板、L176-217 输出模板（含三表）——全部语法正确、占位符语义一致。
- **SCORING.yaml**（179 行）：全文逐条核对（§10）。
- **check.py**（78 行）：全文逐行核对（§4.3）。

### 5.4 跨 Skill 引用

- SKILL.md 无任何指向其他 complex-skills 的引用 ✅。
- L59 引用 `/litigation-legal:matter-intake` 与 L29 引用 `matter-workspace` —— 均为**同插件内部命令**（插件工作流的一部分），非跨 skill 任务路由，判定合规（与 184-pia-generation 引用插件内 reg-gap-analysis 同类，见 184 的 §5.4）。

### 5.5 死文件

- 无。目录内 3 文件全部被 runner/评估使用（SKILL.md 主文件、SCORING.yaml 规则、check.py 执行）。无 `.gitkeep`、无备份残留、无未引用模板。

---

## 6. 语法与格式

### 6.1 拼写

- 全文英文无拼写错误（抽查：privileged/waiver/anticipation/designation 等高频词均正确）。法律术语（implied undertaking、dominant purpose、Akzo Nobel）拼写与惯例一致 ✅。

### 6.2 语法

- 句式工整，无残缺句。长句集中在 gate 引用块（L166-172），主语-谓宾结构完整。列表项全部以名词短语或完整句构成，无混杂 ✅。

### 6.3 混杂

- 全英文 skill（法律类语料库惯例），无中英混杂、无其他语言残留 ✅。

### 6.4 Markdown 破损

- 表格 4 组全部对齐、分隔行完整；代码块 3 个全部闭合；引用块 2 个闭合 ✅。
- **重复 H1**：L6 与 L15 两处 `# Privilege Log Review`（唯一真实结构瑕疵，🟢）。
- 无孤立 `---` 造成的渲染异常（L13/L31/L212 的水平线均起分隔作用，合法）。

### 6.5 占位符

- 输出模板中的 `[N]`/`[Bates]`/`[Matter]`/`[date]` 等为**交付模板占位**，符合用途 ✅。
- `[UNCERTAIN — verify currency]`/`[VERIFY: ...]`/`[CITE NEEDED: ...]`/`[web search — verify]` 等为**标记体系占位**，是功能的组成部分而非未完成标记 ✅——设计正确，不属于占位符残留。

### 6.6 截断

- 无内容截断。文件以完整句 "The tree is the output; the lawyer picks." 结束 ✅。
- **805 字符超长行**（`file` 工具报告 very long lines）——为 L166-172 的 gate 引用块，属单行长文本而非断行错误（🟢 可读性优化项）。
- **行尾细节**：全文件 CRLF 一致；**文件末尾多一个空行**（byte 级实测 `\r\n\r\n` 收尾，即 229 行外还有第 230 个空行）——git 风格上与同类 skill 不一致，无害但建议清理（🟢）。

---

## 7. 规范合规性 12-item checklist

| # | 规则（SKILL-SPEC） | 判定 | 依据 |
|---|---|---|---|
| 1 | name ≤64、匹配目录名 | ✅ | privilege-log-review（19 字符），与 185- 后缀一致 |
| 2 | description 第三人称 WHAT+WHEN、≤1024 | ✅ | 271 字符；S1 WHAT / S2 WHEN；第三人称 |
| 3 | 无 imperative/第一/第二人称 | ✅ | description 零违规（body 内 "you" 为对 agent 的指令人称，见 §8.5） |
| 4 | 无跨 skill 路由 | ✅ | 仅插件内部命令，无指向其他 complex-skills 的引用 |
| 5 | 触发信号（trigger phrase） | ✅ | "Use when the user says ..." + 4 条可检索短语 |
| 6 | 无 forbidden keys | ✅ | 仅 name/description/argument-hint |
| 7 | body ≤600 行 | ✅ | 224 行（wc 229） |
| 8 | workflow 存在 | ✅ | ## Workflow（Step 1-3）+ ## Step 0 |
| 9 | output 存在 | ✅ | ## Output（含完整模板） |
| 10 | scope 存在 | ✅ | ## What this skill emphatically does not do（SKILL-SPEC 变体标题命中）+ 两个前置限制节 |
| 11 | 无 `../` 引用 | ✅ | SKILL.md 零 `../`；check.py 的 `.. /_shared` 为 runner 引导路径，非 skill 内容引用 |
| 12 | 目录 NNN-kebab | ✅ | 185-privilege-log-review |

**12/12 全合规**。语料库中少见的零违规记录（与 dossier 🟢 评级一致）。

---

## 8. 人机感

### 8.1 Emoji

- body 使用 ✅⚠️❌（三态符号）与 🟡（不确定标记）。**均为功能符号**——SCORING PROC-01 正则 `✅|⚠️|❌` 直接依赖这些符号判定，属于测评协议的一部分而非装饰 ✅。无装饰性 emoji。

### 8.2 喊叫

- 无全大写喊叫。`**No silent supplement.**`、`**Conflicts gate — unbypassable.**` 为加粗强调，语气克制 ✅。

### 8.3 Persona

- 无 persona。全文以中立法律助理口吻，不模拟律师、不扮演法官 ✅。

### 8.4 人机边界

- **语料库最佳实践**：律师复核门（L37/L214）、non-lawyer 服务门（L166-174）、❌ 仅推荐不执行（L151/L196）、工作产品保密声明（L216）、"a lawyer decides; the skill does not decide for them"（L67）。人机分工表述完整且反复强化 ✅。

### 8.5 人称

- body 中 "you" 出现于对 **agent** 的指令（"you may only use them..."）与给 agent 的引用话术（"If not confirmed, flag it"）；人类一律称 "the attorney"/"the lawyer"/"counsel"。人称区分清晰——agent 与律师的分工用词从未混淆，是本 skill 人机边界文本设计的核心支撑 ✅。

### 8.6 表格→自然语言

- 3 组表格均为数据呈现（格式检查字段、flag 记录表、❌ 推荐表），表格承载结构化输出合理；叙事段落负责规则与边界——无"表格中写散文"或"段落中藏数据"的错配 ✅。

---

## 9. 可执行性

### 9.1 独立可执行性：9/10

- 判定规则、输出模板、门控条件全部内联，**脱离插件 config 仍可完成核心三态审查**（8 分基础）。
- 扣 1 分：gate（L166）与工作产品页眉（L177）依赖外部 config 的 `## Who's using this`/`## Outputs`——config 缺失时这两步只能降级执行。

### 9.2 步骤可操作性

- Step 1 格式检查有明确字段清单（6 项）+ 缺失处理；Step 2 有逐条输出格式模板（3 分支）；Step 3 有 3 类模式信号。每步都有可判定输入与明确输出 ✅。
- 三态判定给出正反例清单（✅ 4 类 / ⚠️ 6 类 / ❌ 5 类）——agent 可对照分类 ✅。
- "The calls" 的 in-house 法域矩阵给到国别级条件（US/EU/DE/UK/FR-BE）——可操作 ✅。
- 唯一操作空洞：L23 "Other jurisdictions: Check the local rule" 无操作化（🟢）。

### 9.3 工具依赖

- 必要工具：Read（读取日志/文档/config）、法律研究连接器（Step 0）、以及任何可写文档集输出的环境。无 Bash/脚本依赖 ✅。
- 环境敏感依赖（评分可达性）：`matters/_log.yaml` 预置（SCOPE-01）、研究连接器装配（SCOPE-03）——**两项目前不可由 skill 自身保证**（见 §13 I-1）。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖（20 项 = SCOPE 3 + PROC 10 + OUT 3 + NEG 2 + QA 2，与 total_items: 20 一致）

| 维度 | 项数 | script | llm | 覆盖的 body 内容 | 覆盖判定 |
|---|---|---|---|---|---|
| scope | 3 | 2 | 1 | 冲突门（SCOPE-01）、disclosure 限制（SCOPE-02）、法域规则研究（SCOPE-03） | ✅ 齐 |
| process | 10 | 4 | 6 | 三态（PROC-01）、不确定保号（PROC-02）、in-house 法域（PROC-03）、❌ 限定（PROC-04）、禁静默剥离（PROC-05）、waiver 分型（PROC-06）、格式检查（PROC-07）、逐条输出（PROC-08）、模式 flags（PROC-09）、引用纪律（PROC-10） | ✅ 齐 |
| output | 3 | 2 | 1 | 模板结构（OUT-01）、复核声明+保密声明（OUT-02）、非律师门（OUT-03） | ✅ 齐 |
| negative | 2 | 0 | 2 | 不做接近判定（NEG-01）、不剥离/不产出/不服务（NEG-02） | ✅ 齐 |
| qa | 2 | 0 | 2 | 无静默补充（QA-01）、could not check 纪律（QA-02） | ✅ 齐 |

- **覆盖缺口 1**：`## Close with the next-steps decision tree`（L226-228）无任何准则覆盖——唯一无测点的章节（影响小，但作为 600 行内的收尾指令，建议补一条 llm 项，🟢）。
- **覆盖缺口 2**：SCOPE-03 判定词表缺 body L67 的 "firm platform"（§4.2）——使用公司平台的研究渠道无法命中（🟡）。
- **覆盖缺口 3**：PROC-10 正则 `Checked \d+ of \d+ citations` 要求字面句式——agent 若用 "We verified 5 of 7 citations" 等自然变体即漏报。script 检查的固有表达依赖，非设计缺陷，但建议在 question 层放宽（🟢）。
- 覆盖与 body 的对应度是本语料库最高档之一：**几乎每一段实质规则都有对应测评点**。

### 10.2 CF（Critical Failure）分析

- **CF-01**（凭主观判定剥离特权标注，cap_to_0）：与 PROC-05、NEG-02 三重重叠（同一行为被 3 条准则 + 1 条 CF 监控）。冗余度高——CF 的独立价值仅在于 cap_to_0 的惩罚力度（一条 CF 归零全分）。判定合理，因"剥离设计"是此类 skill 最致命的行为（单向门，不可逆 waiver）✅。建议：可考虑将 PROC-05 与 NEG-02 合并以降低判定冗余（🟢）。
- **CF-02**（未经冲突门审查日志，cap_to_0）：与 SCOPE-01 重叠。CF 的附加价值同样是惩罚力度。判定合理 ✅。
- **CF 判定机制**：SCORING 未声明 CF 由 script 还是 llm 判定、触发后的计分规则（cap_to_0 语义）——与 093 等同类 skill 的共性问题（🟢）。
- **评分可行性风险（本 skill 特有，重要）**：SCOPE-01（需 `_log.yaml` 可读）与 SCOPE-03（需研究连接器可用）是**环境依赖型 script 检查**。评估工作区若未装配 `matters/_log.yaml` 与任一研究连接器，则无论 agent 表现多好这两项恒败，且 CF-02 同源失效。**建议在 SCORING 或 harness 文档中明确预置要求**（🟡，见 §13 I-1）。

---

## 11. 已知问题汇总

**Dossier 记录**：`🟢 三态判定全程一致,法律类标杆`

**逐条核验**：
- "三态判定全程一致" —— **确认属实**（§4.1 五处交叉验证，零矛盾）。
- "法律类标杆" —— **确认属实**：12/12 合规、三节齐备、人机边界最佳实践、测评覆盖度最高档。本审查维持 🟢 评级。

**Dossier 未记录的问题（本次审查新发现）**：

| # | 问题 | 级别 | 详见 |
|---|---|---|---|
| D1 | "## Step 0" 在结构上位于 "## Workflow" 之外，编号与所在节不一致 | 🟡 | §3.2/§4.1 |
| D2 | "Attorney reviews every flag. No exceptions." 与 ✅ 层设计（绕过审查）措辞张力 | 🟡 | §4.2 |
| D3 | 重复 H1（L6/L15）——quick-start 区与正文区 | 🟢 | §3.4/§6.4 |
| D4 | SCOPE-01/SCOPE-03 的评分可达性依赖评估环境预置（`_log.yaml` + 研究连接器） | 🟡 | §10.2 |
| D5 | Scope 节以变体标题承担（无字面 "## Scope"），dossier 未记录该判定依据 | 🟢 | §3.2 |
| D6 | 805 字符超长行 + 文件末尾多余空行 + CRLF | 🟢 | §6.6 |
| D7 | SCOPE-03 词表缺 "firm platform"（body 自列渠道） | 🟡 | §4.2/§10.1 |

---

## 12. 综合评分（8 维加权）

**Frontmatter 合规 (10/10, 权重 10%)**: name 19 字符全合规；description 271 字符、第三人称、WHAT/WHEN 齐全、触发短语与 body 术语精确呼应；argument-hint 允许字段且语义匹配；YAML 实测解析通过。零扣分。

**Body 结构完整 (9/10, 权重 10%)**: 三节齐备（Workflow/Output/Scope 全部命中）；14 个 H2/H3 结构连续；224 行在 600 行内且密度高。扣 1 分：Step 0 游离于 Workflow 节外 + 重复 H1。

**逻辑一致性 (9/10, 权重 20%)**: 三态体系五处交叉一致（语料库标杆）；waiver/in-house/gate 条件完整；check.py 7 项正则与 SCORING 全对齐。扣 1 分："No exceptions" 措辞张力 + quick-start 与正文双编号体系。

**脚本/参考完整性 (8/10, 权重 15%)**: check.py 结构清晰、注释精确、正则无漂移；SCORING 20 项与 body 覆盖度最高档。扣 2 分：SCOPE-01/03 环境依赖型检查的可达性风险（评分可行性）与 "firm platform" 词表缺口。零参考文件对自包含 skill 是合理选择。

**语法格式 (8/10, 权重 10%)**: 拼写/语法/表格/代码块全干净。扣 2 分：重复 H1、805 字符超长行、末尾多余空行。

**规范合规 (10/10, 权重 15%)**: 12/12 全合规——本批次唯一全绿清单。

**人机感 (9/10, 权重 10%)**: 功能符号、零喊叫、律师复核门与 non-lawyer 门为语料库最佳实践、人称区分清晰。扣 1 分：gate 外部依赖使 Role 判定在缺 config 时无定义。

**可执行性 (9/10, 权重 10%)**: 核心逻辑零外部依赖可执行；步骤全部可操作；唯一扣分是 gate/页眉两处 config 依赖。

**加权总分: 10×0.10 + 9×0.10 + 9×0.20 + 8×0.15 + 8×0.10 + 10×0.15 + 9×0.10 + 9×0.10 = 9.00 → 90/100**

### 评级: 🟢 A (90/100)

与 dossier 🟢 完全一致，且经独立核验确认其两项主张（三态一致、法律类标杆）全部属实。本 skill 是语料库第一梯队：12/12 规范合规、三态规则五处零矛盾、人机边界文本为最佳实践。问题全部集中在**结构性小事**（Step 0 位置、H1 重复）与**评分环境依赖**（SCOPE-01/03 可达性）——后者是唯一有实际影响的缺陷，修复成本极低（§13 I-1）。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命问题

- **无**。本 skill 无致命问题。唯一接近"致命"级的是 **I-1（评分可达性）**——它不损 skill 质量，但若评估 harness 不装配 `matters/_log.yaml` 与法律研究连接器，SCOPE-01/03 与 CF-02 将系统性误判，导致测评结果失真。**工作量：0.5 小时**（在 SCORING.yaml 头部注释或 harness 文档中写明预置要求；若 harness 无法预置，将 SCOPE-01/03 降级为 llm 判定）。

### 🟡 重要问题（修复总工作量约 2 小时）

1. **I-2 将 "## Step 0" 并入 Workflow 节或重命名为 "## Workflow — Step 0"**（§3.2/§4.1，D1）。当前 Step 0 在编号上属于 Workflow（Step 0→1→2→3）但结构上独立成节。修复：把 L63 的 `## Step 0` 改为 `### Step 0` 并移入 L126 的 `## Workflow` 之下（或把 Workflow 标题上移覆盖 L63）。**工作量：10 分钟**。
2. **I-3 弱化 "No exceptions" 措辞**（§4.2，D2）。L37 `Attorney reviews every flag. No exceptions.` 与 ✅ 层（L92 明言设计为绕过审查）字面冲突。修复：改为 `Attorney reviews every ⚠️ and ❌ flag. The ✅ tier is limited to the unambiguous categories listed below.` **工作量：5 分钟**。
3. **I-4 SCOPE-03 词表补 "firm platform"**（§4.2/§10.1，D7）。body L67 明列 firm platform 为第四种研究渠道，SCORING/check.py 只覆盖 4 个 MCP 工具名。修复：SCORING.yaml SCOPE-03 pattern 与 check.py L36 同步增加 `firm platform`。**工作量：5 分钟**（需同步改两处，注意 184-pia-generation 同型问题见其 §13）。
4. **I-5 明确评估环境预置要求**（§10.2，D4）：在 SCORING.yaml 文件头注释写明 "SCOPE-01 需工作区含 matters/_log.yaml；SCOPE-03 需装配 Westlaw/CourtListener/Trellis/Descrybe 之一连接器"，并在 harness 文档登记。**工作量：0.5 小时**。
5. **I-6 输出模板与 gate 的 config 缺失降级路径**（§3.3/§5.2）：在 L166 与 L177 各加一句降级句："If the plugin config is unavailable, treat the role as attorney-reviewed-by-default and prepend a standard work-product header." 使 gate 在缺 config 时行为有定义。**工作量：15 分钟**。

### 🟢 优化建议（修复总工作量约 1.5 小时）

1. **I-7 删除重复 H1**（§3.4/§6.4，D3）：L6 与 L15 两个 `# Privilege Log Review` 保留其一，quick-start 区改用无 H1 的标题行（如 `**Quick start**`）。**工作量：2 分钟**。
2. **I-8 清理行尾细节**（§6.6，D6）：删除文件末尾多余空行（`\r\n\r\n` → `\r\n`）；保留 CRLF（与全目录一致）或统一 LF（与 183 等一致即可，避免混用）。**工作量：1 分钟**。
3. **I-9 拆分 805 字符超长行**（§6.6，D6）：L166-172 的 gate 引用块按句子分行，提升可读性与 diff 友好度。**工作量：5 分钟**。
4. **I-10 quick-start 与正文编号对齐**（§4.1）：L8-11 的 4 条改为引用正文步骤号（"Run Step 0-3 below"），消除两套编号。**工作量：10 分钟**。
5. **I-11 SCORING 补 "decision tree" 准则**（§10.1）：为 `## Close with the next-steps decision tree` 增加一条 llm 项（"does the output end with a next-steps decision tree customized to the review?"）。**工作量：10 分钟**。
6. **I-12 合并 CF-01/PROC-05/NEG-02 冗余**（§10.2）：保留 CF-01（惩罚力）+ 一条 llm 行为准则，删除第三处重复。**工作量：15 分钟**。
7. **I-13 操作化 "Other jurisdictions"**（§4.4）：L23 补一句操作步骤（"Identify the jurisdiction; if the local rule is not retrievable, flag [UNCERTAIN] and ask"）。**工作量：10 分钟**。
8. **I-14 description 外层引号**（§2.2）：给 description 加外层双引号（内部引号转义）以消除 plain scalar 脆弱性。**工作量：5 分钟**。

**优先级排序建议**：I-1（环境/评分）→ I-2/I-3（结构一致性）→ I-4（评分词表）→ I-5/I-6（健壮性）→ I-7 至 I-14（打磨）。全部完成后预计维持 🟢 A，主要收益在测评可信度与可维护性。

---

## 附录: 审查过程记录

### 读取的文件列表

1. `SKILL.md` — 229 行（wc -l），全文精读；byte 级核查行尾（CRLF×229、末行空行、UTF-8 无 BOM）
2. `SCORING.yaml` — 179 行，全文逐条核对（20 项准则 + 2 CF）
3. `check.py` — 78 行，全文逐行核对（7 项 script 检查、正则与 SCORING 交叉比对）
4. `_shared/checker.py` — 重点阅读 `_log_search`（L249-256）与 `output_contains`（L339-343）确认 tool_log 整条 JSON 匹配与输出正则语义
5. `_shared/SKILL-SPEC.md` — 关键规则（name ≤64、description ≤1024、允许字段清单 L13-29、三节变体标题 L106-108、600 行硬限 L120、12 项 checklist L149-155）
6. `_shared/CHECKER-LIBRARY.md` — 未读取（checker.py 源码已覆盖语义）
7. `102-ai-slop-detector/REVIEW.md` 与 `093-data-privacy-compliance/REVIEW.md` — 作为 REVIEW.md 结构与评分体系参照
8. `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` — 185 条目（🟢 三态判定全程一致,法律类标杆）

### 读取统计

- 总文件数：8（skill 3 + shared 2 + 参照 REVIEW 2 + memory 1）
- 总行数：约 1,450 行
- 验证实验：PyYAML frontmatter 解析 ×3（通过）；CRLF/EOF byte 级实测（`od -c` + Python bytes）；正则一致性人工比对 7 组；描述长度/最长行/标题计数（Python 实测：desc 271 字符、最长行 805、H2×12/H3×11）

### 审查方法说明

- 三态一致性验证采用"五处交叉定位法"（Purpose / The calls / Workflow Step 2 / Output 模板 / does-not-do 各取三态表述比对）。
- 评分可达性分析基于 `_log_search` 的整条 JSON 匹配语义（tool_log 条目必须真实包含路径/工具名）。
