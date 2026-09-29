# REVIEW: 037-brief-section-drafter

**审查日期**: 2026-08-06 | **Skill 类型**: process — 诉讼简报章节起草（法律写作与验证协议） | **Body 行数**: 185 | **参考文件数**: 0（外部插件契约 4+ 处）

---

## 1. 目录全量清单

目录 `D:\SkillIF\skill-experiment\complex-skills\037-brief-section-drafter\` 共 4 个文件（1 个 Body + 2 个评测附属文件 + 1 个本审查文档）：

| # | 文件路径 | 行数 | 类型 | 说明 |
|---|---|---|---|---|
| 1 | `SKILL.md` | 191 | Body | Frontmatter 5 行 + Body 185 行（L6–L190）+ 尾空行 |
| 2 | `SCORING.yaml` | 182 | 评测标准 | 20 条 criteria（3 scope + 7 process + 4 output + 2 negative + 4 qa）+ 3 条 critical_failures |
| 3 | `check.py` | 76 | 评测脚本 | 3 个 script 检查（PROC-01 / PROC-04 / NEG-02），依赖 `_shared/checker.py` |
| 4 | `REVIEW.md` | 7 | 审查文档 | 旧版 7 行 stub（本文件即为其替换物） |

要点：

- 目录结构与 corpus 标准一致：`NNN-kebab-case-name/` + `SCORING.yaml` + `check.py`，**无 `references/`、无 `scripts/` 子目录**——SKILL.md 自含全部内容，不依赖任何本目录附属文件（这是与多数 process 型 skill 不同的纯内联结构）。
- 无触发对照集存在：`complex-skills-no-trigger\037-brief-section-drafter\`（同一 corpus 的对照组）含 SKILL.md / SCORING.yaml / check.py。`diff` 结果显示：**SCORING.yaml 与触发版逐字节相同**；SKILL.md 仅 description 差异（对照版删去全部 WHEN 触发句，仅保留 WHAT 句，见 §2.2）；check.py 差异仅为触发版多一段 `is_path` 防御分支（详见 §5.3）。该对照组由 `create_no_trigger_set.py` 生成，与 2 Mode × 5 Harness 测评矩阵设计一致。
- 旧 REVIEW.md 为 7 行 stub（内容见附录），已被本文替换。

---

## 2. Frontmatter 逐字段审查

### 2.1 字段清单

| 字段 | 值 | 判定 | 依据 |
|---|---|---|---|
| `name` | `brief-section-drafter` | ✅ | 小写 + 连字符，≤64 字符；与目录 `037-brief-section-drafter` 的 kebab 部分完全一致（NNN 前缀属目录命名规范，不进入 name 字段，符合 corpus 惯例） |
| `description` | 见 2.2 逐句分析 | ✅ | ≤1024 字符（实测 296 字符） |
| `argument-hint` | `"[section — e.g., 'statement of facts', 'argument II']"` | ✅ | SPEC §1.2 允许字段；YAML 双引号内 `\u2014` 转义为 em dash，解析合法；值与 Workflow Step 1 的 section 路由表（L93–97）逐项对应——提示可直接携带目标章节，agent 可跳过路由提问直接进入 Step 2 |

无任何 SPEC §1.3 禁用键（无 `metadata`/`version`/`tags`/`trigger`/`model` 等）。YAML 语法合法，引号转义正确（description 内含 `"draft the [section]"` 双引号，外层以 YAML 双引号包裹、内层双引号未转义——经解析实测合法，因为内层引号不构成 YAML 结构歧义，但严格说这是唯一一处脆弱写法，见 §13 🟢P5）。

### 2.2 description 逐句分析

原句（L3）：

> Draft a brief section in house style, consistent with the case theory — every fact cited, every case checked, every argument tied to the theory. Use when the user says "draft the [section]", "write the statement of facts", "argument section on [issue]", or needs a first draft of a brief section.

| 句 | 内容 | 三问定位 | 判定 |
|---|---|---|---|
| 句 1 | Draft a brief section in house style, consistent with the case theory；后接三项承诺（every fact cited / every case checked / every argument tied to the theory） | WHAT（动作 + 质量承诺） | ✅ 具体不空洞，三项承诺分别由 Body 的 Record fidelity（L38–50）、Citation extraction coverage（L60–68）、Theory check（L100–107）兑现——description 与 body 的契约对齐是本 skill 的突出优点 |
| 句 2 | Use when the user says "draft the [section]" / "write the statement of facts" / "argument section on [issue]" / needs a first draft | WHEN（四个触发场景，全部是用户口头语式的引语） | ✅ 触发词覆盖 section 类型与动作动词，可直接匹配用户意图；注意 "argument section on [issue]" 是引语内的占位符用法，触发时括号内容由用户填充 |

**Voice**：动词开头（"Draft a brief section..."）描述 skill 的功能，与 SPEC §2.6 的 Good 示例（"Generate comprehensive test plans..."）同一句式——描述 WHAT 的动词开头不构成 imperative 违规（§2.3 禁止的是 "Use this skill to..." 式与第一/二人称）；全文第三人称，无 "I/you/we"。**无跨 skill 路由**嵌入，符合 §2.5。

**触发信号**（§2.4 要求至少一条）：句 2 以 "Use when the user says..." 开头——含 "Use when the user" 前缀。SPEC 列出的五个标准信号为 `"Use when the user..."`、`"Use when the user asks to..."`、`"Use when the user needs to..."`、`"Triggers on..."`、`"Use for..."`；"says" 是 "asks to / needs to" 的语义变体，在清单内但非字面标准句式。与 034-client-intake（"Use when starting..."）同类，判为 ✅（含注），建议标准化（§13 🟢P5）。

**KEYWORDS**：brief section、house style、case theory、statement of facts、argument、first draft——领域词齐全；动作动词（draft/write）匹配用户意图。

**对照版（no-trigger）**：description 截为仅句 1（"Draft a brief section in house style, consistent with the case theory — every fact cited, every case checked, every argument tied to the theory."，约 150 字符）。保留 WHAT 与 KEYWORDS、删除全部 WHEN 触发句——符合无触发对照集的设计目的（测评 trigger 效果），同时语义仍完整可读，对照版自身质量良好。

### 2.3 语法

- 双引号内嵌双引号（"draft the [section]"）是唯一语法风险点：现行写法经 YAML 解析实测合法（内层引号处于值中段，不破坏引号配对），但若后续编辑在句首/句尾引入内层引号则可能破解析；建议改单引号或转义（§13 🟢P5）。
- `argument-hint` 的 `\u2014` 转义正确；方括号为字面量，无解析问题。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（L6–L190）

| 行号 | 标题 | 级别 | 功能 | 备注 |
|---|---|---|---|---|
| L6 | `# Brief Section Drafter` | H1 | 标题残片 | **与 L15 重复**（见下） |
| L8–11 | 4 条编号 TL;DR + 代码块 | — | 极简总览 | **残片**：条目与正文节重复，且声称的 "reference below" 无对应物（见 §4.1-#2） |
| L13 | `---` | — | 分隔线 | 残片的一部分，正文中段孤悬 |
| L15 | `# Brief Section Drafter` | H1 | 正文标题 | 重复的第二个 H1 |
| L17–25 | `## Witness statements for England & Wales — PD 57AC` | H2 | 合规护栏：拒写"以证人身份"叙述性声明 | 含许可替代项（问题提示、组织证词、文件清单、PD 57AC 合规清单、律师证书）与 US 声明书/宣誓书类比 |
| L27–29 | `## Purpose` | H2 | 动机 + "emphasis on draft. Partner edits." | 边界声明前置，得体 |
| L31–36 | `## Written or oral?` | H2 | 先问再写：书面 vs 口头两套深度策略 | 对应 SCOPE-02；口头场景给出"挑 3-4 个点、让步弱项"的明确策略 |
| L38–50 | `## Record fidelity — quotes and pinpoints` | H2 | 逐字引用纪律 + pinpoint 完整性纪律 | 对应 PROC-06/PROC-07/CF-01；声明 canonical 版本在插件 CLAUDE.md |
| L52–58 | `## Candor about weak arguments` | H2 | 弱论点必须显式标记（MR 3.1 依据） | 对应 PROC-05；引用块给出标准话术模板 |
| L60–68 | `## Citation extraction coverage` | H2 | 引用核对协议：全量提取→全量核对→覆盖报告 | 对应 QA-01；"could not check ≠ confirmed" 反误报规则 |
| L70–77 | `## Echo vs repeat` | H2 | 回应式复用 vs 逐句抄袭的边界 | 对应 QA-02 |
| L79–87 | `## Load context` | H2 | 加载插件 CLAUDE.md + **不可绕过的冲突 gate** | 对应 PROC-01/CF-02；gate 逻辑见 §4.2 |
| L89–168 | `## Workflow` | H2 | 5 步工作流 | 详见 3.2 |
| L170–177 | `## Statement of facts specifics` | H2 | 事实陈述节特殊规则 | 对应 OUT-02/OUT-03 |
| L179–184 | `## Argument section specifics` | H2 | 论证节特殊规则 | 对应 OUT-03/QA-04 |
| L186–190 | `## What this skill does not do` | H2 | 边界（3 条） | 对应 SPEC 必需"Scope"节 |

### 3.2 必需章节（SPEC §3.1）

| 必需章节 | 位置 | 判定 |
|---|---|---|
| Workflow / Process | `## Workflow`（L89–168），5 个 `### Step N` | ✅ 完整、有序、每步可执行，另加 Statement of facts / Argument 两个节专属规则块 |
| Output Format | Workflow Step 5 内嵌（L136–168） | ✅ 非独立标题，但内容完备度超过多数独立 Output 节：交付物定义（L148）+ 完整 drafting notes 前置模板（L150–162，含 theory tie-in / authorities / record cites / open questions / length 五字段）+ 两条格式固定的警告（L165–167） |
| Scope / Limitations | `## What this skill does not do`（L186–190）+ 分布式边界 | ✅ 3 条显式边界（不产终稿/不决定策略/永不代签），另有四处功能式边界：PD 57AC 拒稿（L21）、冲突 gate 拒绝（L83–87）、no silent supplement（L132）、non-lawyer filing gate（L138–146） |

### 3.3 委托结构

- **本目录内委托**：无——不引用任何 `references/` 或 `scripts/` 文件，全部内容内联。零悬空引用的反面是本 skill 偏"全量内联"设计，信息密度高但 Body 已达 185 行，若继续扩展建议下沉（§13 🟢P5）。
- **外部插件委托**（关键）：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` 在 4 处被引用（L8/81/113/138），承担：case theory、house style（citation format/structure/tone/length）、输出约定（`## Outputs`）、共享护栏（`## Shared guardrails` 的 canonical 引语规则）；另引用该文件的 `## Who's using this` 小节 2 处（L138/153，non-lawyer 角色判定）；`_log.yaml` 3 处（L83/85/87，冲突 gate）。**无回退**——这是本 skill 最大的可移植性风险（详见 §4/§5/§9/§13）。
- 跨 skill 引用均为散文式命名（`matter-intake`、`deadlines` 等插件命令空间），无 `../other-skill/` 文件级引用，符合 SPEC §3.3。

### 3.4 层级健康度

- H1 出现两次（L6/L15）——同一文件内两个 `# Brief Section Drafter`，是重构残留（TL;DR 残片的一部分），应合并（§13 🟡P1）。与 034-client-intake 的 L6/L20 双 H1 缺陷同源同款。
- H2 为主干（12 个），H3 用于 5 个 Step，层级 2–3 级、单调递增，无跳级。
- 段落长度：最长为 Step 4（L120–134，约 15 行，信息密度高但结构清晰——标记三件套、no silent supplement 话术、来源标签清单）；L50（pinpoint 规则）为全文件最长单段（60+ 词），逻辑完整可读。
- 章节顺序的叙事弧合理：护栏前置（PD 57AC → Purpose → Written/oral → Record fidelity → Candor → Citation coverage → Echo）→ 执行（Load context → Workflow）→ 节专属规则 → Scope。先立规矩后干活，是法律类 skill 的成熟组织方式。

### 3.5 长度

- Body 185 行（L6–L190）。process 模式目标 ~200 行，恰好落在目标带内；远低于 600 行硬上限。
- dossier 记 "190 行"——实测含 frontmatter 共 191 行（含尾空行），dossier 可能计 frontmatter + body = 190，无实质分歧。

---

## 4. 逻辑一致性深度审查

### 4.1 衔接与指代

| # | 发现 | 严重度 |
|---|---|---|
| 1 | **TL;DR 残片与全文脱节**：L8–11 的 4 条总览是草稿脚手架——条目 1（Load CLAUDE.md）与正文 `## Load context` 重复；条目 3（Draft in house format）与 Step 3 重复；条目 4（Output + flag every place）与 Step 5 重复；条目数（4）与工作流步数（5）不对应，且未覆盖 Step 1（Which section?）/Step 2（Theory check）两个前置步骤。 | 🟡 |
| 2 | **"reference below" 无指代**：L9 条目 2 "Follow the workflow and reference below"——正文即工作流本身，下方并无独立的 "reference" 文件或附录（本 skill 无 references/ 目录）。该措辞是早期"内容拆到附属文件"设计留下的残迹。 | 🟡 |
| 3 | L38 自指说明合理："The canonical statement lives in the plugin's CLAUDE.md shared guardrails; repeated here because this skill is the most common place the rule gets tested"——解释了重复声明的原因，与插件委托结构自洽。 | ✅ |
| 4 | Step 4 标记三件套（L126–128）与 Step 5 前置模板的 "Open questions" 字段（L160）双向衔接一致；L132 的四选项升级路径（broaden / other tool / web search tagged / stop）与 NEG-01 逐字对齐。 | ✅ |
| 5 | **两套标记体系并存**：L45 用 `[verify exact quote — record cite pending]`（小写 verify、`[ ]` 内短语式），L126–128 用 `[VERIFY: ...]` / `[UNCERTAIN: ...]` / `[CITE NEEDED: ...]`（大写、冒号式）——语义互补（前者专管引语、后者管事实/法理/引注），但格式族不一致，见 §13 🟡P2。 | 🟢 |
| 6 | **`[verify against record — Tr. p. __]` 与 `[verify exact quote — record cite pending]` 两个占位符风格**（L44/L45）：前者含 Tr. p. 页码占位、后者无——同段内两种颗粒度，微瑕。 | 🟢 |
| 7 | 冲突 gate 的拒绝话术（L85–86）与 `## Who's using this` 的 non-lawyer 话术（L140–144）均为"引用块内完整可直接复述"的模板——agent 行为确定性高。 | ✅ |
| 8 | L153 `[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see ## Who's using this]` 是模板内占位指令而非最终文本——agent 需自行展开，位置清楚、无歧义。 | ✅ |

### 4.2 矛盾检查

- 无自我矛盾声明。五重护栏（PD 57AC 拒稿 / 冲突 gate / no silent supplement / candor 标记 / non-lawyer filing gate）相互独立、无优先级冲突——这是 corpus 中护栏密度最高的 skill 之一（对比 034 的三重边界、028 的三重 gate）。
- 法条/规则引用准确：PD 57AC（L17–25）与官方要求一致（2021-04-06 生效于 Business & Property Courts 等 CPR 管辖程序；证人本人语言、不得含 argument、须附记忆文件清单、合规确认与律师证书——body 逐项对应且无虚构）；MR 3.1（L58，"a lawyer must have a basis in law and fact"）正确；Rule 11（L140/165）与 Rule 3.3（L167）在 filing 语境下使用正确（Rule 11 签字认证、Rule 3.3 candor toward the tribunal——L167 将两者并列于 "filing this section... carries Rule 11 / Rule 3.3 exposure" 的表述在法律上可辩护）。
- 冲突 gate 的契约语义（L83–87）：`matters/_log.yaml` 由 matter-intake 写入、agent 读取——"intake 是 gate，跳过它即绕过冲突纪律"。PROC-01 的脚本检查（工具日志出现 `_log\.yaml|matter-intake`）与 body 逐字对应。逻辑自洽，但**依赖外部文件存在**（§5.2-#1）。
- 写作/口头分支（L31–36）与 Step 3 的 tone/length 规则（L115–118）无冲突：口头分支是策略层（选点与让步），Step 3 是风格层（格式与语调），分层清晰。

### 4.3 代码与条件

- 无伪代码、无未定义的代码实体。唯一的"代码"是模板占位符（`[VERIFY]` 等）与前置模板围栏（L152–168），语法在 Markdown 围栏内合法。
- 条件分支全部给出明确行为：书面/口头（L33–36 两条策略）、guide 有无（不适用，本 skill 无 guide）、thin coverage 四选项（L132）、non-lawyer 有无（L138–146 两分支）、引语可得性（L42–48 三态：verbatim / paraphrase+placeholder / never fabricate）。无悬挂条件。
- 结论断言克制：L188–190 "does not" 三条全部是强否定+替代指引（"It produces a draft" 而非 "它可能产出草稿"），没有半吊子承诺。

---

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用（位置） | 目标 | 类型 | 存在性 | 判定 |
|---|---|---|---|---|
| L8/81/113/138 | `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` | 外部插件配置 | **本机实测不存在**（`~/.claude/plugins/config/claude-for-legal/` 目录不存在，见 5.2-#1） | 🔴 高依赖、无回退 |
| L138/153 | 插件 CLAUDE.md 的 `## Who's using this` 小节 | 外部文档内部锚点 | 不可验证 | ⚠️ non-lawyer filing gate 的角色判定依赖之 |
| L83/85/87 | `.../matters/_log.yaml`（matter 登记） | 外部文件 | 不可验证（无插件则不存在） | ⚠️ 冲突 gate 与 PROC-01 脚本检查的实体依赖 |
| L44/45/126–128 | `[verify...]` / `[VERIFY]` 等标记 | 自含模板 | ✅ 内联 | ✅ |
| check.py L11 | `_shared/checker.py`（`sys.path.insert(0, "..", "_shared")`） | 共享库 | ✅ 存在，函数签名完全匹配（见 5.3） | ✅ |

### 5.2 不可见资源（风险清单）

1. **插件 CLAUDE.md（4 处）+ `## Who's using this`（2 处）**：承担 case theory、house style、`## Outputs` 输出约定、`## Shared guardrails` canonical 引语规则、non-lawyer 角色判定共 5 类内容。**实测验证**：本机 `~/.claude/plugins/` 下仅有 `config`（空）/`installed_plugins.json`/`known_marketplaces.json`/`marketplaces`，`config/claude-for-legal/` **不存在**；`D:\SkillIF\skill-experiment\` 全树（含 research/、scripts）亦无该路径的任何 fixture 生成逻辑。若评测沙箱未挂载该插件，则 Step 1 加载失败、Step 3 "Per CLAUDE.md" 的三行风格规则（L113–118）失去定义来源、Step 5 的 non-lawyer gate 无法判定角色（L138），PROC-01/QA-03 两条 criteria 直接不可达。**这是全 skill 唯一没有兜底的关键路径**。
2. **`_log.yaml`（3 处）**：冲突 gate 的实体。body 的拒绝话术是完整的（L85–86 引用块），但"该文件存在"是 PROC-01 通过的前提；无插件环境下 agent 只能读到空/不存在的文件——此时按 skill 语义应拒绝执行（保守、合规），但评测任务将无法产出任何工作产品。
3. **`~` 用户主目录路径**：硬编码相对用户主目录的绝对路径，跨机器不可移植（作者机可用、评测沙箱大概率不可用）——与 034/036/054/067 等全部 claude-for-legal 系 skill 同款问题。

### 5.3 共享库验证

`D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py` 提供 `tool_log_contains`、`output_contains`、`set_tool_log_path`、`set_agent_output`，与 check.py 的 import 和调用签名逐一匹配；`output_contains` 的 MULTILINE 正则与 PROC-04（`\[VERIFY[^]]*\]|\[UNCERTAIN[^]]*\]|\[CITE NEEDED[^]]*\]`）和 NEG-02（六个来源标签）兼容。check.py L24–29 的"路径 vs 原始文本"二分支逻辑与 main()（L61–63）的读文件逻辑有轻微重复（no-trigger 版 check.py 无此块，直接 `set_agent_output(agent_output)`），行为正确、无害。`_shared/checker.py` 的 `tool_log_contains` 对 JSONL 逐行解析后全串匹配——`_log\.yaml|matter-intake` 对 tool 参数与工具名的扁平 JSON 均可命中，模式设计合理。

### 5.4 嵌套与跨 Skill

无嵌套 skill；跨 skill 仅散文式命名与插件命令空间引用（`matter-intake` L85、`Westlaw/CourtListener/Trellis/Descrybe` L132/134 为外部服务名），无 `../other-skill/` 文件级引用——完全符合 SPEC §3.3 的禁止条款。

---

## 6. 语法与格式质量

| 检查项 | 结果 | 说明 |
|---|---|---|
| 拼写 | ✅ | 全文无拼写错误（抽查 185 行） |
| 术语一致性 | ✅ | `theory` / `house style` / `record` / `pinpoint` / `marker` / `Shepardize` 用法一致且含义稳定 |
| Markdown 结构 | ✅ | 表格 1 处（Step 1 section 表）、代码围栏 2 处（前置模板）、引用块 5 处（拒稿话术、弱论点话术、non-lawyer 话术等），语法全部合法 |
| 占位符 | ✅ | `[VERIFY: ...]` / `[UNCERTAIN: ...]` / `[CITE NEEDED: ...]` / `[section]` / `[issue]` / `[date]` 等统一方括号风格，无残留未替换的真实数据 |
| 截断 | ✅ | 无中途截断迹象；L190 收尾完整（"File anything. Ever." 收束干脆） |
| 混杂 | ✅ | 全英文、无中英混杂、无乱码、无葡语残留（对比 262/276 的教训） |
| 标点 | ✅ | em dash（—）作为分隔符用法一致（description、argument-hint、L38 标题、L56 引用块内）；分号分隔长句（L111、L134）可读 |
| 小瑕疵 | ⚠️ | (1) L6/L15 双 H1；(2) L8–11 TL;DR 残片 + L13 孤悬分隔线；(3) 两套标记体系大小写不一（L45 vs L126–128）；(4) L9 "reference below" 无指代 |

无 TODO/FIXME/lorem 文本、无被截断的半句。整体为 corpus 中语法质量最高的梯队（与 dossier 评价"干净、锐利"一致；L50 的 pinpoint 段落与 L132 的四选项话术是全文语言质量峰值）。

---

## 7. 规范合规性（SKILL-SPEC.md 12 项清单）

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符，≤64，匹配目录 | ✅ | `brief-section-drafter` 与目录 kebab 部分一致 |
| 2 | description：第三人称，WHAT+WHEN+KEYWORDS，≤1024 | ✅ | 296 字符，三问齐备，WHAT 带三项质量承诺 |
| 3 | description：无 imperative/第一/二人称开头 | ✅ | 动词开头描述 WHAT（同 SPEC §2.6 Good 示例句式），无 "Use this skill to"、无 I/you/we |
| 4 | description：无跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 结构 |
| 5 | description：≥1 触发信号 | ✅* | "Use when the user says..." 含 "Use when the user" 前缀但非字面标准句式（同 034 的带注通过），见 §2.2 |
| 6 | frontmatter：无允许列表外键 | ✅ | 仅 name/description/argument-hint |
| 7 | body ≤600 行 | ✅ | 185 行 |
| 8 | body 有 workflow/process 节 | ✅ | `## Workflow` 5 步 + 两个节专属规则块 |
| 9 | body 有 output format 节 | ✅ | Step 5 内嵌完整输出规格与前置模板（L136–168），内容完备度超过多数独立 Output 节 |
| 10 | body 有 scope/limitations 节 | ✅ | `## What this skill does not do` 3 条 + 4 处功能式边界 |
| 11 | body 无跨 skill 文件引用 | ✅ | 无 `../` 引用；插件路径属外部配置契约（§5.2） |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✅ | `037-brief-section-drafter` |

**结果：12/12 通过**（#5 带注）。合规性与 034 并列 corpus 顶尖水平——三必需节齐全且质量高。注意 #9 的形式边界：Output Format 不以独立 `##` 标题存在（嵌于 Workflow Step 5），严格字面检查可能误报，但 SPEC §3.1 允许任意标题名，Step 5 的内容实质满足该节要求，判 ✅。

---

## 8. 人机感评估

| 维度 | 结果 | 说明 |
|---|---|---|
| Emoji | ✅ 零使用 | 全文无 emoji（对比 036 将 emoji 限于模板数据内，本 skill 完全不用，更克制；同 034 的零使用梯队） |
| 全大写 | ✅ 仅模板标记 | `VERIFY` / `UNCERTAIN` / `CITE NEEDED`（L126–128）为标记体系数据，非语气性大写；无 "STOP!"/"DO NOT" 喊话式指令（对比 072 的教训） |
| 语气 | ✅ 专业、坦率且恰当地坚定 | "If you ask me to do it, I won't."（L21）、"A quote that's almost right is worse than a paraphrase"（L42）、"The draft should make the lawyer smarter, not confident about a bad position"（L58）——有人格但不说教、无填充 |
| 人机边界 | ✅ 极清晰 | Partner edits（L29）；"A partner decides whether to accept lower-confidence sources; the skill does not decide for them"（L132）；"I help you get the witness's evidence into the statement. I don't write the evidence."（L23）；`## What this skill does not do` 3 条 |
| 人称 | ✅ | description 与 body 均第三人称；L85/L140 引用块是 agent 对用户说的交互话术（属模板内容而非 agent 语气），用法恰当 |
| 表格密度 | ⚠️ 偏低 | 1 张表 / 185 行——Step 1 section 表是"决策树化"的正确用例；Step 2 theory check（L102–106）的两条 bullet 与 Step 4 来源标签清单（L134）本可表格式呈现，但列表形式已足够清晰，非缺陷 |
| 场景温度 | ✅ | 制裁风险（Rule 11 制裁、L165）、虚构引用的纪律后果（L42–46）、证人声明伪造风险（L21）均以专业风险语言处理，无恐吓腔 |

评价：专业、克制、边界感强，是法律起草领域 skill 的理想人机感样板——dossier 的"专业、坦率且恰当地坚定"评价在复核中成立。口头/书面分支（L31–36）的"主动询问+两套策略"设计（SCOPE-02）是 322 个 skill 中少见的"策略层交互"写法，值得保留。

---

## 9. 可执行性评估

**独立可执行性评分：7.5 / 10**（分环境差异极大，见下）

| 子项 | 得分 | 说明 |
|---|---|---|
| 步骤操作性 | 9.5/10 | 5 步每步都有具体指令：Step 1 四类 section 路由表（输入列明确）；Step 3 明确"研究本地规则与法官 standing orders、引用一手来源（规则号/命令节）、核验时效"；Step 4 标记三件套 + no silent supplement 四选项升级话术；Step 5 前置模板 5 字段逐项定义 |
| 交付物明确性 | 9/10 | 交付物 = 草稿章节（markers 内联）+ drafting notes 前置 + 两条警告；QA-01 的引用覆盖报告（"Found N / Checked N of M / K 无法检索 / J 确认 / I 疑似 / H misgrounded"）是全 skill 最精确的输出契约 |
| 工具依赖 | 4/10 | 关键路径依赖插件 CLAUDE.md（4+2 处）+ `_log.yaml`（冲突 gate）；`~` 绝对路径在沙箱大概率不可解析（本机实测即不存在） |
| 独立运行（无插件环境） | 6.5/10 | Step 1 "Load CLAUDE.md" 失败 → case theory/house style 无定义来源，agent 只能询问或推断；Step 4 的来源标签体系（`[Westlaw]` 等）与标记三件套自足可执行；Step 5 的 `## Who's using this` 读取失败 → non-lawyer gate 失去角色输入（按 skill 语义的保守行为是拒绝，但评测任务将无产出）；冲突 gate 读不到 `_log.yaml` → 无 matter slug 即拒绝（合规但评测失败） |
| 独立运行（插件环境） | 9.5/10 | 按设计用途（claude-for-legal 插件已安装）运行时近乎满分：理论检查、记录保真、引用覆盖、filing gate 全链路可执行 |

结论：skill 自身的可执行性设计是 corpus 顶尖（步骤可操作性 9.5），瓶颈完全在外部依赖契约。修复 P0（§13，含 fixture 方案）后独立可执行性可升至 8.5–9/10。

---

## 10. SCORING.yaml 交叉参考

### 10.1 20 条 criteria 溯源

| ID | 类别 | 检查点摘要 | Body 对应位置 | 判定方式 | 一致性 |
|---|---|---|---|---|---|
| SCOPE-01 | scope | 识别 section 类型与所需输入 | Step 1（L91–98） | llm | ✅ 表格行与 criterion 列举的四种 section 完全一致 |
| SCOPE-02 | scope | 询问书面/口头并调整深度 | `## Written or oral?`（L31–36） | llm | ✅ 两套策略与 criterion 描述逐字对应 |
| SCOPE-03 | scope | PD 57AC 辖区拒写叙述性证人声明并提供替代 | L17–25 | llm | ✅ 拒稿 + 5 类许可替代项（L23） |
| PROC-01 | process | 起草前检查 _log.yaml，未 intake 拒绝 | `## Load context`（L83–87） | script | ✅ 拒绝话术完整；⚠️ 依赖外部文件存在（§5.2-#2） |
| PROC-02 | process | theory check——矛盾则停下标记 | Step 2（L100–107） | llm | ✅ |
| PROC-03 | process | 研究本地规则/standing orders，引一手来源，核验时效 | Step 3（L111） | llm | ✅ 逐字对齐（"don't rely on preferences"） |
| PROC-04 | process | 标记纪律（VERIFY/UNCERTAIN/CITE NEEDED） | Step 4（L126–128） | script | ✅ 正则与 body 逐字匹配 |
| PROC-05 | process | 弱论点显式标记并提供框架选项 | `## Candor`（L52–58） | llm | ✅ 引用块话术含"press/concede/drop"三选项 |
| PROC-06 | process | 无法核实时 paraphrase 不加引号 + 占位符 | L42–48 | llm | ✅ 三态规则 + 占位符样式 |
| PROC-07 | process | pinpoint 支持整个命题——拆分或收窄 | L50 | llm | ✅ 明确给出 (a)(b) 两方案 |
| OUT-01 | output | 符合 house style（引用格式/结构/语调/长度） | Step 3（L113–118） | llm | ✅ 四要素 + 本地规则核对 |
| OUT-02 | output | 事实有 record cite、法理有 case cite+pincite | Step 4（L122–124） | llm | ✅ |
| OUT-03 | output | 事实陈述：时序+全引+无 argument；论证节：先规则+回应反方 | L170–184 | llm | ✅ 两节专属规则精确 |
| OUT-04 | output | 前置 drafting notes + cite-check 警告 | Step 5（L150–167） | llm | ✅ 模板 5 字段 + 两条警告逐项对应 |
| NEG-01 | negative | 研究覆盖薄时不静默补充 | L132 | llm | ✅ 四选项话术逐字对应 |
| NEG-02 | negative | 不剥离来源标签 | L134 | script | ⚠️ 语义偏移见 10.3-#1 |
| QA-01 | qa | 引用覆盖报告（Found/Checked/confirmed/misgrounded） | `## Citation extraction coverage`（L60–68） | llm | ✅ 五类计数与 criterion 逐字对应 |
| QA-02 | qa | 回应式复用而非逐句抄 | `## Echo vs repeat`（L70–77） | llm | ✅ |
| QA-03 | qa | 非律师 filing gate——1 页律师审阅简报 | Step 5（L138–146） | llm | ✅ 简报内容清单（5 要素）与 criterion 对应 |
| QA-04 | qa | 一节一论点、parenthetical 不注水 | L181–184 | llm | ✅ |

### 10.2 critical_failures

| ID | 触发条件 | Body 对应 | 判定 |
|---|---|---|---|
| CF-01 | 虚构引用（引号内非记录原文） | Record fidelity（L42–46） | ✅ 合理 cap_to_0——与 L46 "Never fill the gap" 完全呼应 |
| CF-02 | 未经 intake 即起草实质工作产品（冲突 gate 绕过） | L83–87 | ✅ 合理 cap_to_0——gate 的"不可绕过"表述（L83）与 CF 语义一致 |
| CF-03 | PD 57AC 辖区起草"以证人身份"叙述性声明 | L17–25 | ✅ 合理 cap_to_0——拒稿是 SCOPE-03 的行为要求，CF 是后果封顶，两者互补而非冗余 |

### 10.3 发现的缝隙

1. **NEG-02 语义偏移**：criterion 描述是"does NOT strip source attribution tags"（否定语义——不剥离），脚本实现为 `output_contains`（存在性检查——输出必须含至少一个标签）。无法直接测试"未剥离"（需要与基线对比），存在性检查是合理近似；但 body L134 强制打标签——agent 若合规必含标签，存在性检查会掩盖"打了标签但剥离了部分"的中间状态。低风险，见 §13 🟡P3。
2. **PROC-01 的执行前提**：脚本检查要求工具日志出现 `_log\.yaml|matter-intake`。无插件沙箱中 `_log.yaml` 不存在，agent 行为将偏向"读取失败→拒绝"（合规但评测失分）或"跳过检查"（违规）。检查语义与 body 契约一致，但执行前提依赖环境 fixture（§13 🟡P4）。
3. **PROC-04 与 L45 小写标记无冲突**：脚本正则 `\[VERIFY[^]]*\]` 不匹配小写 `[verify exact quote...]`——body 要求 Step 4 强制使用大写三件套，L45 的小写占位符是"引语专项"提示，两者不重合，无漏检风险（但格式统一问题见 §4.1-#5）。
4. 20 条 criteria 与 3 条 CF 无冗余、无遗漏；categories 占比（scope 3 / process 7 / output 4 / negative 2 / qa 4）与 process 模式匹配；`total_items: 20` 计数正确（3+7+4+2+4）。
5. check.py 仅实现 PROC-01/PROC-04/NEG-02 三个 script 检查，其余 17 条为 llm judge——与 SCORING.yaml 标注一致，无错配。

---

## 11. 已知问题汇总（skill-dossier.md 引用）

Dossier 条目（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` L325–330）：

> - **逻辑**: 连贯且推理严密——theory check、record-fidelity rules、marker discipline、echo-vs-repeat 和不可绕过的冲突 gate 全部一致。
> - **语法**: 干净、锐利法律文体。
> - **人机感**: 专业、坦率且恰当地坚定（"If you ask me to do it, I won't."），无填充或 emoji。
> - **合规**: 🟢 完全合规——三必需节齐全，190 行 ≤600。
> - **总评**: 🟢 优秀起草 skill——连贯、有保护、合规。

对照评估：

| dossier 论断 | 本次审查 | 一致性 |
|---|---|---|
| 逻辑连贯且推理严密（theory check / record fidelity / marker / echo-vs-repeat / 冲突 gate 五要素） | 五要素全部复核成立 ✅；本审查补充新发现：TL;DR 残片（4 条 vs 5 步）、"reference below" 无指代、两套标记体系、双 H1 | 基本一致，本审查更细 |
| 干净、锐利的法律文体 | ✅ 确认（§6） | 一致 |
| 人机感专业坦率坚定 | ✅ 确认（§8） | 一致 |
| 🟢 完全合规 | ✅ 12/12（§7，#5 带注） | 一致 |
| 190 行 | 实测 body 185 行 / 总 191 行（含尾空行）——dossier 计 frontmatter+body=190，无实质分歧 | 无实质分歧 |
| 总评 🟢 优秀 | 本审查给 🟢 A−（89/100，§12）——比 dossier 更保守一级，扣分项集中在外部依赖回退（本机实测插件路径不存在）与 L6–15 草稿残片，均不推翻"优秀起草 skill"定位 | 方向一致 |

旧 REVIEW.md stub（7 行）给出的结论：

> **综合**: 🟢 **A−** (55/100)。硬编码路径（`~/.claude/plugins/config/claude-for-legal/litigation-legal/`）。Dossier: "连贯、有保护、合规"。PD 57AC witness statement 段是从另一个 skill 粘贴的（dossier 标记）。

逐项核对：
1. **A− 评级**：与本审查一致（同 A− 区间，扣分同样集中于外部依赖）。stub 的 55/100 为旧标尺，与 034 等新标尺（87/100）同为 A− 档，无矛盾。
2. **硬编码路径**：确认，且本审查进一步实测了该路径**在本机确实不存在**（§5.2-#1）。
3. **"PD 57AC 段从另一个 skill 粘贴（dossier 标记）"——需更正**：dossier 并未在 037 条目中标记粘贴关系；dossier 对 040-deposition-prep 的标记是 "PD 57AC witness-statement 块从 brief-section-drafter 逐字复制"（L347）——即复制方向为 **037 → 040，037 是源头而非受体**。且在 037 中该块是相关性高的合规护栏（证人陈述属于诉讼起草范畴，拒写"以证人身份"的叙述性声明是 PD 57AC 下的职业责任护栏），**不是缺陷**；它在 040 中"奇怪地置于 deposition-outline skill 顶部"才是被粘贴方的问题。stub 的此条注记应视为误读。

---

## 12. 综合评分（8 维度加权）

| 维度 | 权重 | 得分 | 依据 |
|---|---|---|---|
| 逻辑一致性 | 15% | 9.5 | 五重护栏零矛盾、法条引用准确、条件分支无悬挂；扣分：TL;DR 残片、双 H1、两套标记体系 |
| 参考文件与资源 | 15% | 7.0 | 零悬空引用、纯内联结构；扣分：外部插件契约 4+2 处无回退，本机实测路径不存在 |
| 语法与格式 | 10% | 9.5 | 全净、锐利；仅双 H1/残片/标记大小写微瑕 |
| 规范合规性 | 20% | 9.5 | 12/12 通过；触发句式非标准扣 0.5 |
| 人机感 | 10% | 9.5 | 零 emoji、边界极清晰、专业坦率 |
| 可执行性 | 10% | 7.5 | 步骤可操作性 9.5，但关键路径外部依赖无回退、评测前提缺 fixture |
| SCORING 对齐 | 10% | 9.0 | 20+3 全可溯源；NEG-02 语义偏移与 PROC-01 环境前提各扣 0.5 |
| 法律适切性 | 10% | 9.5 | PD 57AC 拒稿、MR 3.1/Rule 11/Rule 3.3 使用准确、filing gate、misgrounded citation 纪律——corpus 中最强的法律护栏组合之一 |

**加权总分 = 1.425 + 1.050 + 0.950 + 1.900 + 0.950 + 0.750 + 0.900 + 0.950 = 8.875 ≈ 8.9 / 10**

### 总评：🟢 A−（89/100）

法律起草 skill 家族标杆，与 034-client-intake 同属"流程型 skill 教科书"梯队。合规 12/12 全绿、逻辑零矛盾、五重护栏（PD 57AC 拒稿 / 冲突 gate / no silent supplement / candor 标记 / non-lawyer filing gate）是 corpus 中最完备的护栏群之一，SCORING 20+3 全部可溯源；扣分集中在**外部依赖契约**（硬编码插件路径在本机实测不存在、无任何回退——与 034 同款 P0）与 **L6–15 草稿残片**（双 H1 + 4 条 TL;DR）。修复 §13 的 P0–P1 后可达 9.4（🟢 A）。

---

## 13. 修复建议（按优先级分层）★重点★

### 🔴 P0 — 致命（条件性）：外部插件依赖无回退

**问题**：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` 被 4 处引用（L8/81/113/138）、`## Who's using this` 被 2 处引用（L138/153）、`_log.yaml` 被 3 处引用（L83/85/87），承担 case theory、house style 四要素、`## Outputs` 输出约定、canonical 引语规则、non-lawyer 角色判定、冲突 gate 实体共 6 类内容，但**全 skill 没有一处 fallback**。本机实测 `~/.claude/plugins/config/claude-for-legal/` 不存在（`~/.claude/plugins/` 下仅有 config 空目录与三个 JSON），`D:\SkillIF\skill-experiment\` 全树亦无 fixture 生成逻辑。若评测沙箱未挂载该插件（`~` 相对绝对路径在隔离工作区大概率不可解析），则：Step 1 加载失败、Step 3 的 house style 规则（L113–118）失去定义来源、Step 5 的 non-lawyer gate 无法判定角色、冲突 gate 与 PROC-01 脚本检查失去实体——PROC-01/QA-03 两条 criteria 直接不可达，且 agent 的合规行为（拒绝）将导致评测任务零产出。

**修复**（工作量 ~45–60 分钟，分两部分）：

**方案 A — Skill 侧回退分支**（推荐，~30 分钟）：
1. `## Load context`（L79–81）加条件分支：

```
If `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`
exists, load it and follow its case theory, house style, and guardrails.
If it does not exist (no firm config mounted), proceed with the workspace's
matter brief or the user's stated theory, note at the top of the drafting
notes: "Firm config not loaded — house style defaults per this skill applied."
```

2. 为 Step 3（L113–118）追加回退句："no config loaded → use Bluebook-compatible default citation style, CRAC argument structure, and the tone of the seed brief the user provides"——把四要素的默认值从插件引用改为本文显式列出（消除循环依赖）。
3. 为 Step 5 的 non-lawyer gate（L138）追加回退："if `## Who's using this` is unavailable, ask the user directly: 'Are you a licensed attorney?' and apply the gate accordingly"。
4. 为冲突 gate（L83–87）追加回退："if `_log.yaml` does not exist, treat the matter as unintaken — the refusal message above still applies"（拒绝话术已存在，缺的只是"文件不存在时也走同一分支"的明确性）。

**方案 B — 评测侧 fixture**（条件性，与 A 互补，~15 分钟）：在 SkillIF 评测工作区为每个 claude-for-legal 系 skill（017/018/028/034/036/037/040/067/077/127/139/144/160/170/185/200/212/258/279/304 等，凡引用该插件路径者）提供最小 fixture：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`（含 case theory 示例、house style 四要素、`## Who's using this` 的 Role=Lawyer、`## Outputs` 的 work-product 约定）+ `matters/_log.yaml`（含一个示例 matter slug）。可脚本化生成（复用 `create_no_trigger_set.py` 的 corpus 遍历模式）。这同时解决全部 20+ 个同家族 skill 的同一问题，而非逐个补丁。

### 🟡 P1 — 重要：清理 L6–15 草稿残片

**问题**：SKILL.md 顶部保留着重构前的脚手架——`# Brief Section Drafter` H1 出现两次（L6/L15），L8–11 的 4 条 TL;DR 与正文重复且条目数（4）与工作流步数（5）不对应、未覆盖 Step 1/2，L9 "Follow the workflow and reference below" 的 "reference" 无指代（本 skill 无 references/），L13 `---` 孤悬。与本文替换掉的 7 行 REVIEW stub 属于同一批"草稿残留"（034-client-intake 的 L6–17 TL;DR 残片同源同款——该批 skill 普遍存在此问题）。

**修复**（工作量 ~15 分钟）：删除 L6–13 的整个残片区块（含双 H1 之一与分隔线），保留 L15 起的正式正文；如要保留总览，改写为与 5 步一一对应的表格（比编号列表防漂移），并把 "reference below" 删除或改为指向 `## Workflow`。

### 🟡 P2 — 重要：统一两套标记体系

**问题**：L45 的 `[verify exact quote — record cite pending]`（小写、无冒号）与 L126–128 的 `[VERIFY: ...]` / `[UNCERTAIN: ...]` / `[CITE NEEDED: ...]`（大写、冒号式）并存。语义上互补（引语专项 vs 事实/法理/引注），但格式族不一致会稀释 marker 的"一眼可扫"属性——审阅律师扫描 `[VERIFY` 会漏掉小写的 `[verify exact quote]`。

**修复**（工作量 ~5 分钟）：将 L44–45 的两个占位符统一进主标记族：`[VERIFY: exact quote — record cite pending]` 与 `[VERIFY: quote against record — Tr. p. __]`。改后 L42–48 的段落仍保留"三态规则"的叙述（verbatim / paraphrase+placeholder / never fabricate），只换占位符字样。注意：`[VERIFY[^]]*]` 正则（PROC-04）对小写样式本就不匹配，统一后样式收敛、无副作用。

### 🟡 P3 — 重要：NEG-02 检查语义对齐（SCORING.yaml）

**问题**：criterion 描述（"Agent does NOT strip source attribution tags"）是"不剥离"的否定语义，脚本实现（check.py L47–49 `output_contains`）是"输出含至少一个标签"的存在性检查。语义偏移：agent 打了标签又剥离部分标签时，存在性检查仍会误报通过。

**修复**（二选一，工作量 ~10 分钟）：
- 方案 A：将 SCORING.yaml 的 NEG-02 描述改为存在性语义（"Agent includes source attribution tags ([Westlaw], [web search — verify], ...) on citations it retrieves or recalls"），与脚本实现一致；
- 方案 B：维持描述语义，脚本升级为双检查（输出含标签 AND 输出不含 "tag: none" 之类剥离痕迹）——成本高、收益低，不推荐。
推荐方案 A：评测目标是"标签纪律是否存在"，存在性代理在工程上已足够，把文档与实现对齐即可消除歧义。

### 🟡 P4 — 重要：无插件环境下的评测可运行性（与 P0 方案 B 合并）

**问题**：即使 Skill 侧加回退（P0 方案 A），PROC-01 的脚本检查（工具日志含 `_log\.yaml|matter-intake`）在无 `_log.yaml` 的沙箱中仍不可命中——agent 无法"检查一个不存在的文件"（合规行为是拒绝）。

**修复**（工作量 ~30 分钟）：采纳 P0 方案 B 的 fixture 方案，并**验证回退路径本身**：在无 fixture 的对照组（Mode 无 trigger 或 Harness 变体）中，预期 agent 行为是"拒绝 + 提示 matter-intake"——这本身是一个可评测的结果（合规拒绝），建议在 SCORING 中为 PROC-01 增加一个"文件缺失时正确拒绝"的二级判定（llm judge），把"环境不可达"从失分项转为可验证的合规行为。

### 🟢 P5 — 优化：description 触发句式标准化 + 引号安全

**问题**：(1) "Use when the user says..." 不在 SPEC §2.4 的标准信号清单内（语义无歧义，但严格比对时带注通过，见 §7-#5）；(2) description 双引号内嵌双引号（"draft the [section]"）是 YAML 脆弱写法（当前实测合法，但编辑易破）。

**修复**（工作量 ~3 分钟）：改为 `"Use when the user asks to draft the [section], write the statement of facts, argument section on [issue], or needs a first draft of a brief section."`——落入 "Use when the user asks to..." 标准信号，同时内层引号全部去除（句子结构不变，引语感由上下文保留）。注意：**触发版与 no-trigger 对照版需同步**（对照版只删 WHEN 句，本就无此问题）。

### 🟢 P6 — 优化：PD 57AC 块的版本管理注记

**问题**：该块（L17–25）已逐字复制到 040-deposition-prep 顶部（dossier 040 条目确认）。两处副本后续若独立演进会漂移（如 PD 57AC 更新、法院纪律指引变化）。

**修复**（工作量 ~5 分钟）：在 L17 标题下加一行 "This guardrail block is shared verbatim with the `deposition-prep` skill — update both copies together"（散文式跨 skill 注记，符合 SPEC §3.3，不违反跨文件引用禁令）。同时把 040 中的副本标记为"从 brief-section-drafter 复制"的源注，消除两目录间的溯源歧义（旧 REVIEW stub 的"粘贴方向"误读正是缺乏此类注记导致的）。

### 🟢 P7 — 优化：回归测试闭环

**修复**（工作量 ~20 分钟）：执行 P0–P3 后，在挂载 fixture 与不挂载 fixture 两种工作区各跑一遍 check.py（`python check.py <workspace> <tool_log> <agent_output>`），验证：(1) 挂载时 PROC-01/PROC-04/NEG-02 三条 script 检查在真实 agent 轨迹中可命中；(2) 不挂载时 agent 行为为"合规拒绝"（预期，供 P4 二级判定使用）；(3) 另跑一条 PD 57AC 拒稿轨迹确认 CF-03 判定路径（llm judge 输入完整）。

### 修复工作量汇总

| 优先级 | 项数 | 工作量 | 修复后预期 |
|---|---|---|---|
| 🔴 P0 | 1（含 A/B 两方案） | ~45–60 分钟 | 可执行性 7.5 → 8.5+；PROC-01/QA-03 可达 |
| 🟡 P1–P4 | 4 | ~60–80 分钟 | 逻辑一致性/SCORING 对齐 9.5+；合规仍 12/12 |
| 🟢 P5–P7 | 3 | ~30 分钟 | 细节无瑕、同家族 skill 的 fixture 问题一并解决，达 🟢 A（9.4/10） |
| **合计** | **8** | **约 2.5–3 小时** | 推荐全部执行；P0 必须（对 20+ 个同家族 skill 可规模化复用） |

---

## 附录: 审查过程记录

- **审查日期**: 2026-08-06。
- **被替换文件**: 旧 `REVIEW.md`（7 行 stub），原文：

```
# REVIEW: 037-brief-section-drafter

**2026-08-05** | Claude | Dossier: 🟢 典范

硬编码路径（~/.claude/plugins/config/claude-for-legal/litigation-legal/）。Dossier: "连贯、有保护、合规"。PD 57AC witness statement 段是从另一个 skill 粘贴的（dossier 标记）。

**综合**: 🟢 **A−** (55/100)
```

- **过程时间线**:
  1. `Glob D:\SkillIF\skill-experiment\complex-skills\037-brief-section-drafter\**` → 得 4 文件清单；
  2. `Glob SKILL-SPEC.md` 首查 `skill-experiment\_shared\` 失败（该层无 `_shared`）→ 重定位 `complex-skills\_shared\SKILL-SPEC.md` 与 `complex-skills-no-trigger\_shared\SKILL-SPEC.md`，取前者；
  3. `Read` SKILL.md（191 行，全文）→ SCORING.yaml（182 行）→ check.py（76 行）→ 旧 REVIEW.md（7 行）；
  4. `Bash ls ~/.claude/plugins/...` → 实测 `config/claude-for-legal/litigation-legal/` **不存在**（仅 config/installed_plugins.json/known_marketplaces.json/marketplaces）；
  5. `Read` SKILL-SPEC.md（163 行）→ 逐项比对 12 项合规清单；
  6. `Read` skill-dossier.md（全文）→ 定位 037 条目（L325–330）+ 040 条目（L346–351，PD 57AC 复制方向证据）+ 汇总统计；
  7. `Read` 034-client-intake/REVIEW.md（434 行）——同域同款 13 节模板的完整样例，作为本审查的结构基准；
  8. `diff` 触发版 vs no-trigger 版 SKILL.md / SCORING.yaml / check.py → SCORING 逐字节相同、description 仅 WHEN 句差异、check.py 仅 is_path 防御块差异；
  9. `Read _shared\checker.py`（351 行）验证 check.py 的 import 与函数签名匹配、正则兼容性；
  10. `Grep D:\SkillIF` 全树 "claude-for-legal" → 确认无 fixture 生成逻辑（命中均为 SKILL.md/REVIEW.md 内的引用文本）；`Grep research\skill-reviews` → 确认无 037 的历史审查记录可参照；
  11. `Python` 计算 metrics：description 296 字符、插件路径 4 处、`_log.yaml` 3 处、标记计数（VERIFY 2 / UNCERTAIN 2 / CITE NEEDED 3）、字数 2552；
  12. 交叉核对：SCORING 20+3 条 ↔ Body 行号 ↔ check.py 实现；dossier/旧 stub 结论 ↔ 本次审查结论；
  13. 写作本 REVIEW.md（替换旧 stub）。
- **验证记录**: description 长度 296 字符（≤1024 ✅）；Body 行数 185（≤600 ✅）；目录共 4 文件、无 references/scripts/；no-trigger 对照版存在于 `complex-skills-no-trigger\037-brief-section-drafter\`；`~/.claude/plugins/config/claude-for-legal/` 实测不存在；SCORING `total_items: 20` 与分类求和一致。
- **方法论备注**: 本审查独立于 dossier 结论重新走查全部文件；dossier 的 🟢 评价在复核中成立，但本次新发现 5 处 dossier 未记录的问题（双 H1 + TL;DR 残片、"reference below" 无指代、两套标记体系、NEG-02 语义偏移、PROC-01 环境前提），并实测确认了 stub 所称硬编码路径的缺失；同时**更正了旧 stub 的一处误读**——PD 57AC 块的复制方向是 037 → 040（037 为源头，dossier 040 条目为证），该块在 037 中是相关性高的合规护栏而非缺陷。故维持 🟢 A− 评级（89/100）而非上调；P0 修复（含 fixture 方案）完成后评级可上调至 🟢 A。
