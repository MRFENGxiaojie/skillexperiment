# 077-takedown 技能质量审查报告

- 审查对象：`D:\SkillIF\skill-experiment\complex-skills\077-takedown`
- 审查日期：2026-08-06
- 审查标准：`_shared/SKILL-SPEC.md` v1.0（12 项合规清单）+ SCORING.yaml 22 项测评标准 + 目录内全部文件全文阅读 + 正则/字数/符号实测验证
- 审查方式：目录内 3 个文件（SKILL.md 386 行 / check.py 81 行 / SCORING.yaml 200 行）全部逐行阅读；对 check.py 的 7 项脚本检查逐个用 SKILL.md 实际文本做正则命中实测；对 SCORING.yaml 的 22 项 criterion 与 LLM 判定问题逐一做可追溯性核对；调取 skill-dossier.md 中 077 条目与「典范 Skills」表（见 §11）
- 结论：综合得分 93.0/100，质量评级 A+（语料第一梯队）。与 dossier 🟢 评级一致——三模式分发、法定要素清单、gate 设计均无可挑剔，合规度 12/12（两项带轻微保留意见）。本报告发现的问题全部集中在「测评检查层」（QA-01 正则与模板错配、PROC-14 语义不可满足、SCOPE-02 对外部 profile 的强耦合）与「打磨层」（description 触发短语、输出节分散、冗余重复），SKILL.md 正文本体零结构性缺陷。

---

## 1. 目录全量清单

目录共 3 个文件，本次全部全文阅读：

- `SKILL.md`（386 行）— 技能主体（frontmatter 4 行 + body 382 行）
- `check.py`（81 行）— 脚本检查器入口（7 项脚本检查）
- `SCORING.yaml`（200 行）— 22 项测评标准（15 项 LLM 判定 + 7 项脚本判定 + 3 项 critical_failures）

此外读取了共享基础设施 `_shared/SKILL-SPEC.md`（合规判定基准）与 `_shared/checker.py`（检查器函数库，用于核对 check.py 的映射正确性），以及 skill-dossier.md 的 077 条目（行 613-619）、「典范 Skills」表（行 1171）、076-100 批次记录——均为共享审查输入，不计入本技能文件评分。

目录特点：**无 `references/`、无 `assets/`、无 `scripts/` 目录**。作为三模式（send / respond / counter）× 八步骤的法律过程型技能，全部内容自包含在 386 行正文中。该取舍合理（详见 §5.1），符合 dossier 对「body ~387 行」的记录（wc 实测 386 行，差异为末行换行符统计口径）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name 字段

`name: takedown`。小写 + 连字符，8 字符，远小于 64 上限。目录名为 `077-takedown`（NNN-kebab-case），按语料惯例 name 不含 NNN 前缀（已抽查 301-trade-performance-coach 等相邻技能确认），与 SKILL-SPEC §1.1/§4 的歧义处理方式一致，判定合规。

**一个可选观察**：`takedown` 一词不带任何法律/领域信号——「takedown」在非法律语境（网站下线、体育、金融）同样高频。技能匹配完全依赖 description 兜底。语料内相邻法律技能（`017-cease-desist`）同样使用短名，属于语料惯例而非缺陷；若未来做意图匹配实验可考虑 `dmca-takedown`（见 §13 🟡-9，可选）。

### 2.2 description 字段

共 **453 字符**（实测），符合 ≤1024 字符限制。逐项检查：

- **人称**：以 "Draft a DMCA takedown notice, triage one you received, or draft a §512(g) counter-notice." 开头——动词罗列式开头与 SKILL-SPEC §2.6 的 Good 示例（"Generate comprehensive test plans, ..."）同型，第三人称描述成立，无第一/第二人称，符合 §2.3。
- **WHAT**：三模式职能（draft takedown / triage received / draft counter-notice）一句讲清。
- **WHEN**：三个 "when" 条件从句（"when asserting copyright through a §512(c)(3) takedown..."、"when an incoming takedown needs triage..."、"when drafting a §512(g)(3) counter-notice..."），触发场景具体到法条编号。
- **KEYWORDS**：DMCA、§512(c)(3)、§512(g)(3)、takedown、counter-notice、fair-use、perjury gates、triage、comply/counter/engage/ignore——覆盖充分，且 "fair-use and perjury gates" 与 "consent-to-federal-jurisdiction gate" 直接点名了技能的差异化安全设计。
- **无跨技能路由**：无 "NOT for X, use Y instead" 句式。
- **触发信号（⚠️ 一处保留意见）**：SKILL-SPEC §2.4 列出的五个逐字信号为 "Use when the user..."（三变体）、"Triggers on..."、"Use for..."。本 description 用的是 "Use when asserting copyright..." ——以 "Use when" 开头但**没有逐字命中五个信号中的任何一个**。规范字面判读为「六不合一」，但语义上是标准 "Use when" 结构的合法变体。语料内抽查（如 301-trade-performance-coach 的 "Use when the user wants..."）多为逐字命中。建议改为 "Use when the user asserts copyright through..." 以零成本消除合规争议（见 §13 🟡-4）。此项为合规判定中唯一值得记录的瑕疵。

### 2.3 可选字段与违禁字段

Frontmatter 共 3 个键：`name`、`description`、`argument-hint`。`argument-hint` 是 §1.2 允许的可选字段，内容 `"<--send | --respond | --counter> [context or path to incoming notice]"` 与正文三分发模式逐字对应，设计良好。未使用其余可选字段（allowed-tools 等），**绝无任何违禁字段**（metadata/license/tags/trigger 等均无）。完全合规。

### 2.4 Frontmatter 小结

Frontmatter 整体合规，结构零问题；唯一打磨点是 description 触发短语非逐字命中 §2.4 信号清单（🟡-4），以及 name 的领域信号偏弱（🟡-9，可选）。

---

## 3. Body 逐段结构分析

### 3.1 总体结构

正文 382 行（body），远低于 600 行硬上限。单一 H1 `# Takedown` + 12 个 H2 章节，H3 严格用于模式内 Step 编号，层级无跳跃。章节清单与职责：

| 章节 | 行号 | 职责 |
|---|---|---|
| `## Instructions` | L8-30 | 6 条全局执行指令（profile 加载 → matter 检查 → 模式分发 → gate 纪律 → 司法辖区 → 移交） |
| `## Examples` | L32-39 | 4 个调用示例（含 --respond 带 PDF 路径） |
| `## Notes` | L41-46 | 4 条全局注意（work-product 头部规则、要素完备性、联邦管辖、非律师简报） |
| `## Purpose` | L50-62 | 三模式总述 + 外部交付物头部规则 |
| `## Jurisdiction assumption` | L64-66 | 美国联邦法假设 + 非美辖区切换 |
| `## Load context` | L68-71 | 实践 profile / matter workspaces 加载点 |
| `## Send mode ...` | L73-197 | 8 步：识别作品 → 识别侵权材料 → 合理使用门 → 善意信念 → 准确性与授权 → 起草 → 大声门 → 输出 |
| `## Respond mode ...` | L199-306 | 4 步：读取通知 → 评估 → 四选项 → 写 triage 备忘 |
| `## Counter mode ...` | L308-372 | 4 步：确认前提 → 起草 → 大声门 → 输出 |
| `## Decision posture` | L374-376 | 不确定即上报的主观法律判断原则 |
| `## What this skill does not do` | L378-386 | 7 条不做清单 |

结构呈「全局指令 + 三模式分治」的完美放射形：Instructions 负责路由，各模式章节是自包含的线性流程，符合 process 型技能（SCORING `pattern: process`）的最佳实践。

### 3.2 Workflow / Process（必备项 ✅）

三层递进的工作流设计：

1. **全局层**（Instructions 6 步）：Step 1 profile 加载与 `[PLACEHOLDER]`/缺失检测（L16，含冷启动路由话术）→ Step 2 matter workspaces 检查（L18，含 ✗ 停用判定与切换话术）→ Step 3 按 `$ARGUMENTS` 分发（L20-24）→ Step 4 gate 纪律总纲（L26）→ Step 5 司法辖区注记（L28）→ Step 6 移交规则（L30）。
2. **模式层**（Send 8 步 / Respond 4 步 / Counter 4 步）：每步都有明确产出或检查点。
3. **门层**：合理使用门（send Step 3）+ 大声门（send Step 7 / counter Step 3）两级，后详 §4.4。

`$ARGUMENTS` 分发逻辑是完整决策树：`--send` / `--respond` / `--counter` / 无 flag 一次澄清提问，与 `argument-hint` 呼应。

### 3.3 Output Format（必备项 ✅，带一处保留意见）

输出约定**分散在三处模式级 Step** 而非独立顶层章节：

- send Step 8（L185-197）：主产物 `takedown/<slug>/notice-v<N>.md`（可 .docx）、in-chat 明文预览、审查者结语、citation 验证规则（L195，来源标签五枚举）、post-send 记录 `submission.md`（L197）。
- respond Step 4（L247-306）：主产物 `takedown/inbound/<slug>/triage.md` + 完整模板（L251-302，含 work-product 头部、特权继承声明、评估字段、四选项、期限、即时行动清单）。
- counter Step 4（L362-372）：主产物 `takedown/<slug>/counter-notice-v<N>.md` + 审查者结语 + post-submission 记录 `counter-submission.md`（L372）。

SKILL-SPEC §3.1 允许三必需节「any heading name」存在——Output Format 内容完备且具体到文件名、路径、头部规则，**判定合规**。但就结构可读性而言，三处输出约定的「模式 → 产物 → 路径 → 头部规则 → 记录文件」映射缺少一张统一汇总表，读者需要读完三节才能拼出完整输出契约。建议在 Notes 或新设顶层章节加映射表（见 §13 🟡-5）。

### 3.4 Scope / Limitations（必备项 ✅）

由 `## What this skill does not do`（L378-386，7 条）+ `## Decision posture`（L374-376）+ `## Jurisdiction assumption`（L64-66）三重承担。7 条不做清单全部是**具体反模式**（不提交通知、不代选 intake 表单、不裁决合理使用、不验证对方主张、不绕过门、不编造引用、不处理非美制度），且每一条都与正文/SCORING 有锚点对应（如「不提交」↔ SCOPE-04，「不绕过门」↔ NEG-01）。边界声明的颗粒度是本技能亮点之一。

### 3.5 引用与路径规范

- 正文无跨技能文件路径引用（无 `../other-skill/`），符合 §3.3。
- 对插件命令 `/ip-legal:takedown`、`/ip-legal:cold-start-interview`、`/ip-legal:matter-workspace` 的引用属于**散文式命令名引用**（同技能家族），符合 §3.3 "referencing another skill, use its name in prose" 精神。
- 唯一绝对路径 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`（L16/70）是**外部配置路径**而非跨技能引用，属技能运行依赖，合规但构成测评环境耦合（见 §10.4、§13 🔴-1）。
- `## Load context` 中 `takedown/<slug>/` 等输出路径均为技能内部相对约定，无绝对化问题。

---

## 4. 逻辑一致性深度审查

### 4.1 三模式分发的一致性

模式清单在正文出现三处：开篇速览块（L8-12）、Instructions Step 3 分发（L20-24）、Purpose（L54-60）——三处模式集合完全一致（send / respond / counter）。无 flag 的澄清提问脚本出现**两处且逐字相同**：L24（"Are we sending a DMCA takedown, triaging one we received, or drafting a counter-notice?"）与 L60。功能上无矛盾（同话术重复是刻意的执行确定性），但属冗余文案，建议二选一（见 §13 🟡-6）。

### 4.2 法定要素与法条逐项对照（本次审查的核心正确性验证）

**§512(c)(3)(A) 六要素**（send Step 6，L137-145）逐项对照 17 U.S.C. §512(c)(3)(A)(i)-(vi)：

| 法条要素 | SKILL.md 条目 | 核对 |
|---|---|---|
| (i) 签名（物理或电子） | 要素 1 | ✅ 逐字一致 |
| (ii) 作品识别 | 要素 2 | ✅ |
| (iii) 侵权材料识别 + 定位信息 | 要素 3（URL + 描述 + 侵权方式） | ✅ 且呼应 L95 "information reasonably sufficient to permit the service provider to locate" |
| (iv) 联系信息 | 要素 4 | ✅ |
| (v) 善意信念声明 | 要素 5 | ✅ 提供逐字可改编文案（L143） |
| (vi) 准确性 + 伪证声明 + 授权声明 | 要素 6 | ✅ 提供逐字可改编文案（L144），且 L129-133 明确该声明覆盖范围与 §512(f) 的关系 |

**§512(g)(3) 四要素**（counter Step 2，L321-326）逐项对照 17 U.S.C. §512(g)(3)(A)-(D)：签名 / 被移除材料识别及移除前位置 / 伪证下的善意错误或误认声明 / 姓名地址电话 + 联邦地区法院管辖同意 + 送达接受。四要素齐备，管辖同意条款（L326）准确覆盖「美国境内地址 → 所在司法辖区；境外 → 服务提供者可被诉的任何地区」两种情形，与法条一致。

**时间窗口一致性**：10–14 个工作日窗口在 L197（watch date）、L233（respond 选项 B 权衡）、L292（triage 模板期限节）、L310/342-343（counter 前提与门）共五处出现，全部一致且准确（§512(g)(2)(C)：提交反通知后 10–14 个工作日为诉权窗口；未起诉则服务商须在 14 个工作日内恢复）。无一处数字漂移。

**判例引用准确性**（send Step 7 大声门，L162）三处全部核对无误：

- *Lenz v. Universal Music Corp.*, 801 F.3d 1126 (9th Cir. 2015) ✅（合理使用考虑义务）
- *Online Policy Group v. Diebold*, 337 F. Supp. 2d 1195 (N.D. Cal. 2004) ✅（§512(f) 责任判例）
- *Stephens v. Clash*, 796 F.3d 281 (3d Cir. 2015) ✅（§512(f) 责任判例）

L195 的 citation 验证规则要求 agent 输出中的任何引用均来源标签化（[Westlaw]/[CourtListener]/[user provided]/[model knowledge — verify]/[web search — verify]）——规则本身适用于 agent 输出；SKILL.md 内嵌判例未带标签属正常（技能文本非 agent 输出），但建议定期在法研工具上复核（见 §13 🟢-17）。

### 4.3 逻辑链条检查点

- **合理使用门 → 大声门顺序**（Instruction 4 明示，L26）：send 中 fair-use gate（Step 3）先于 draft，loud gate（Step 7）先于 output。「debatable/likely → 不起草 → 路由律师」与「loud gate 确认清单 → 显式参与后才输出」两层分置，无交叉矛盾。
- **善意信念四要件**（Step 4，L118-124）：拥有权/授权、无许可、已考虑合理使用、直接复核被控内容——四要件与 Step 1（识别作品）与 Step 3（合理使用门）的输出严格互锁，形成闭环。
- **respond → counter 移交**（L30 + L234 + L249-250 附近）：respond 选项 B 的下一步指向 `/ip-legal:takedown --counter`，但以「triage 备忘经审查 + 决策有意作出」为前提；counter Step 1 的前提确认（L312-317）又要求「并非反应式、须经律师参与」——移交链条每个环节都有独立闸门，无短路路径。
- **外部交付物头部规则**：L43（Notes）、L62（Purpose 块引用）、L252-254（triage 模板特权继承声明）三处一致——对外通知/反通知**不带** work-product 头部（法定程序声明），内部草稿/分析/备忘**带**。与 OUT-01 判定逐字咬合。
- **matter workspaces 双轨**：L18 与 L70-71 两处一致（Enabled ✗ 则跳过；启用且无活跃 matter 则询问切换）。
- **非律师路径**：L177-181（send 大声门内）与 L356-358（counter 大声门内）均提供一页律师简报 + 转介资源（州律师协会/SRA/法学院 IP 诊所等），两处话术结构同源，无缺失分支。

### 4.4 文档 ↔ 测评的一致性（发现 3 处偏差，详见 §10）

1. **QA-01 正则与模板错配**（实测确认）：`1\.\s*Signature` 与 `2\.\s*Identification` 无法命中 `1. **Signature**` 与 `2. **Identification of the copyrighted work**`（粗体标记阻断）——见 §10.3。
2. **PROC-14 语义不可满足**：评测中通知/反通知按 SCOPE-04 只起草不提交，`submission.md`/`counter-submission.md` 物理上不可能被写出，PROC-14 只能靠 agent 在聊天输出中提及来通过——见 §10.4。
3. **SCOPE-02 的环境耦合**：`~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md` 若未在评测环境预置，合规 agent 会在 Step 1 正确停机，导致除 SCOPE-02 外的全部脚本检查落空——见 §10.5、§13 🔴-1。

---

## 5. 辅助文件内容级审查（check.py 全文 + SCORING.yaml 全文；无 references/）

### 5.1 无 `references/` 目录的评估

本技能无任何参考文件目录。对该取舍的评估：SKILL.md 正文 382 行、远低于 600 行上限，三模式 + 法定要素 + 模板均可容纳；statutory-element 型技能的知识本质上是「要素清单 + 门流程」，不像 trade-performance-coach 那样需要五轴模型/输出契约/schema 等外围资产。**自包含设计成立，无需拆分**。唯一候选外置物是 respond 的 triage 模板（L251-302，52 行），留在正文使读者无需跳转即可核对输出契约，合理。dossier 对此无异议（🟢 评级下无此维度问题）。

### 5.2 check.py（81 行）全文审查

入口契约 `python check.py <workspace> <tool_log> <agent_output>` 与 _shared 检查器库一致。docstring 声称「7 项脚本检查」，实际输出键恰好 7 个（SCOPE-02 / PROC-05 / PROC-10 / PROC-12 / PROC-14 / OUT-01 / QA-01），数目自洽。

**映射正确性**（逐一核对 check.py 调用与 checker.py 函数签名）：

| 检查 | 函数 | 参数形式 | 核对 |
|---|---|---|---|
| SCOPE-02 | tool_log_contains | 三选正则 | ✅ |
| PROC-05 | output_contains | 四选正则 | ✅ |
| PROC-10 | file_exists | `os.path.join(workspace, "**/takedown/**/triage.md")` | ✅ 与 L249 输出路径匹配 |
| PROC-12 | output_contains | 五选正则 | ✅ |
| PROC-14 | output_contains | 四选正则 | ✅ |
| OUT-01 | output_contains | 四选正则 | ✅ |
| QA-01 | output_contains | 五选正则 | ⚠️ 见 §10.3 正则缺陷 |

**正则命中实测**（以 SKILL.md 实际文本为语料，`re.search` 验证）：

- PROC-05 的 `17 U.S.C. §512\(c\)`：能命中 L129 的 "17 U.S.C. §512(c)(3)"（子串匹配）✅
- PROC-12 五个短语：`mistake or misidentification`（L325）、`good faith belief`（L325）、`federal district court`（L326）、`consent to the jurisdiction`（L326）、`17 U.S.C. §512\(g\)`（L333）全部命中 ✅
- PROC-14 的 `10.?14 business days`：能命中 en dash 版 "10–14 business days"（`.` 匹配 `–`）✅；`submission\.md`/`counter-submission`/`watch window` 全部命中（L197/233/292/310/342/372）✅
- OUT-01 四个短语：`not.*privileged`（L62 "not privileged"）、`no work-product header`（未逐字出现，但 L62 "Do NOT include the PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT header" 命中第二条 `statement made in a statutory process` 前无…——实测：第二条候选是 `statement made in a statutory process`，L62 "it's a statement made in a statutory process" 命中 ✅；第三条 `internal drafts` 命中 L43/L62 ✅）——四选一即可，实测至少两条可命中 ✅
- QA-01：`good faith belief` / `penalty of perjury` / `authorized to act` 三个短语候选在 L143-144 逐字命中 ✅；但**编号候选 `1\.\s*Signature` / `2\.\s*Identification` 对模板粗体格式全部落空**（实测 False）——检查实际只靠短语候选通过，详见 §10.3。

**代码质量**：唯一瑕疵是 L22-30 的 `_is_path` 判定逻辑——`main()` 已经读取并传入了文件内容，`check()` 又要再 `os.path.exists(agent_output)` 判断是否是路径。正常路径下（内容非路径）多一次无谓的 `set_agent_output`；极端路径下（输出文本恰好等于某个存在的文件路径字符串）会跳过 set，导致 output_contains 检查空指针级失效。属防御过度 + 冗余的混合体，建议简化（见 §13 🟡-8）。

### 5.3 SCORING.yaml（200 行）全文审查

`skill: takedown` / `pattern: process` / `total_items: 22` 三者与目录名、技能体量一致。结构：scope 4 + process 14（send 6 / respond 4 / counter 4）+ output 2 + negative 1 + qa 1 = 22，无重复 ID、无编号断层（SCOPE-01..04 / PROC-01..14 / OUT-01..02 / NEG-01 / QA-01 连续）。critical_failures 3 项（CF-01 跳过合理使用门或大声门即起草通知 → cap_to_0；CF-02 未确认联邦管辖同意与律师审查即起草反通知 → cap_to_0；CF-03 编造判例引用 → cap_to_0），与 SKILL.md 的 gate 设计、L195 引用规则一一对应，归零惩罚语义恰当。

**15 项 LLM 判定的可追溯性**（问题文本 → SKILL.md 锚点）逐一核对：SCOPE-01↔L20-24+L60；SCOPE-03↔L64-66；SCOPE-04↔L154+L380-381；PROC-01↔L75-84；PROC-02↔L86-95；PROC-03↔L97-112；PROC-04↔L114-125；PROC-06↔L156-183；PROC-07↔L203-212；PROC-08↔L214-220；PROC-09↔L222-245；PROC-11↔L312-317；PROC-13↔L336-360；OUT-02↔L195；NEG-01↔L26+L183+L360。15/15 全部可指向具体段落，无悬空问题。这是本语料中 LLM 问题可追溯性最好的 SCORING 文件之一。

---

## 6. 语法与格式质量

### 6.1 YAML

Frontmatter 为单行 plain scalar（L3），`yaml.safe_load` 实测解析成功；SCORING.yaml 同样解析成功（22 项 criteria + 3 项 critical_failures 字段完整）。无引号转义问题。en dash（–）与 § 符号在 YAML plain scalar 中无需转义，解析无误。

### 6.2 Markdown 结构

H1 仅 1 个（`# Takedown`），H2 ×12，H3 ×27（Step 标题 + 门横幅）。triage 模板（L251-302）整体包在 ```markdown 围栏内，其内部 `# DMCA Takedown Received — Triage` 等标题为**模板字面内容**而非文档大纲，围栏隔离正确，未污染标题层级。门横幅 `### BEFORE THIS TAKEDOWN GOES ANYWHERE`（L158）与 `### BEFORE THIS COUNTER-NOTICE GOES ANYWHERE`（L338）用 H3 + 全大写构成视觉隔离，是法律高风险的恰当格式手段。无嵌套列表缩进错误，代码围栏语言标注齐全（markdown 一处）。

### 6.3 拼写与语言

通篇为专业法律文体：无错字、无病句、无中英混杂。术语统一（"good faith belief"、"penalty of perjury"、"§512(f) exposure" 等固定搭配一致）。唯一生僻用词是 L372 的 "calendared"（"watch window end date calendared"）——法律事务语境下为可接受用法，非错误。句读完整，无悬垂句。

### 6.4 符号与字符

符号扫描（Unicode category S/C 过滤 § – — 后）：正文含 `✗`（U+2717，L18 "if `Enabled` is `✗`"）与 `→`（U+2192，L203 或 L308 附近节标题箭头）各一处，均为功能性符号（状态标记、节标题箭头）而非装饰性 emoji。dossier 记载「无 emoji」——严格说存在一个 ✗，但属功能标记，不构成人机感问题（§8 详述）。无 box-drawing 字符、无多余空白。

### 6.5 编码与行尾

UTF-8 无 BOM（实测读取正常）。行尾 Windows 环境下 CRLF/LF 混合属常态，不影响解析器。

---

## 7. 规范合规（SKILL-SPEC v1.0 十二项清单）

1. ✅ **name 小写+连字符 ≤64 且匹配目录**：`takedown` 8 字符；目录 `077-takedown` 为 NNN-kebab 格式；按语料惯例 name 不含 NNN 前缀。
2. ✅ **description 第三人称、含 WHAT+WHEN+KEYWORDS、≤1024 字符**：453 字符，三者齐备。
3. ✅ **description 无命令式/第一/第二人称开头**：动词罗列式开头与 §2.6 Good 示例同型。
4. ✅ **description 无跨技能路由**。
5. ⚠️ **description 含至少一个触发信号**：`"Use when asserting copyright..."` 为 "Use when" 变体，**未逐字命中 §2.4 五个信号短语**（"Use when the user..." 三变体 / "Triggers on..." / "Use for..."）。语义合规、字面存疑——判合规但带保留意见（🟡-4）。
6. ✅ **frontmatter 无违禁键**：仅 name + description + argument-hint（后者为允许的可选字段）。
7. ✅ **正文 ≤600 行**：382 行。
8. ✅ **正文含 Workflow/Process 章节**：`## Instructions` 6 步全局流程 + 三模式 Step 分治。
9. ✅ **正文含 Output Format 章节**：分布在各模式 Step 8/4（§3.3），§3.1 "any heading name" 下成立；建议增统一映射表（🟡-5）。
10. ✅ **正文含 Scope/Limitations 章节**：`## What this skill does not do` 7 条 + `## Decision posture` + `## Jurisdiction assumption`。
11. ✅ **正文无跨技能文件引用**：仅插件命令名散文引用与外部配置绝对路径（后者为运行依赖非引用）。
12. ✅ **目录 NNN-kebab-case、无空格无大写**。

结论：12 项中 10 项完全合规，第 5 项（触发短语）与第 9 项（输出节分散）合规但带保留意见。整体规范遵从度为语料第一梯队，与 dossier 🟢「完全合规——三必需节齐全」的记载一致（dossier 未细察触发短语字面差异，本报告补记）。

---

## 8. 人机感评估

### 8.1 语言基调

中性、克制、正式的法律语调贯穿全文。无 filler、无口语化、无装饰性 emoji（✗/→ 为功能符号，见 §6.4）。`Do not write the final output without explicit engagement`（L183/L360）这类短促祈使句构成门纪律的仪式感，与法律高风险场景匹配。

### 8.2 用户引导脚本（引号内对话）

Step 1-3 的块引用（L77-83/L88-94/L101-111）是结构良好的用户面向提问脚本：「What is the copyrighted work?」→ 四个子问题列表；「Where is the infringing material?」→ 平台/URL/描述/证据；合理使用门 → 四因素 + "Your read on each?"。语料惯例（dossier 对 076 的评语「引用的用户面向脚本赋予了恰当的第一人称」）同型。三处脚本均为「问题 → 选项 → 结论判定」闭环，无开放式废话。

### 8.3 高风险边界的设计（本技能人机感的核心成就）

- **大声门**：`### BEFORE THIS TAKEDOWN GOES ANYWHERE` 全大写横幅 + 4 项确认清单 + 审批人占位 + 自动升级占位；非律师追加一页律师简报话术（L177-181）与转介资源（州律师协会 / SRA / BSB / 法学院 IP 诊所 / ABA IP 名册）。「几千美元的律师时间比 §512(f) 诉讼便宜得多」这类话术把风险量级讲到了钱上，是语料内少见的、直接有效的非律师风险沟通。
- **反通知门**：L338-360 明确「这是诉讼前一步」，联邦管辖同意「不是形式主义」（L45），非律师被明确告知「这不是 Claude 审查层；这是需要持牌专业判断的步骤」（L357-358）——人机边界划得最清楚的一段文字。
- **审查者结语**：send/counter 的 in-chat 结尾均附「此为律师审查草稿，未审勿发」声明（L191-193/L368-370），respond 附「triage 非意见」声明（L304-306）。

### 8.4 决策姿态

`## Decision posture`（L374-376）把「不确定即上报、不静默决定」立为全局原则，并以「one-way door」类比（L376）解释为何不能靠假设推进。合理使用被明确点名为「范式性的不确定判断」（L376）。与 017-cease-desist 的 gate 设计同源，符合 dossier 对法律类标杆的描述。

### 8.5 小结

人机感维度无可指摘。唯一可议点是门横幅的全大写风格——对法律受众恰当，不属过度；保留。

---

## 9. 可执行性评估

### 9.1 Agent 执行路径可运行性

从 `$ARGUMENTS` 到最终产物的每一步都有确定性出口：profile 缺失 → 停机话术；matter 未选 → 询问话术；无 flag → 单次澄清；三模式的每一步 → 具体问题/清单/模板；最终产物 → 带路径的文件 + in-chat 预览 + 审查者结语 + 记录文件。不存在「无路可走」的死循环分支。非律师分支、美国境外分支、门阻断分支均有显式路径，决策树完备性在语料中属于最高一档。

### 9.2 产物路径与测评 glob 的咬合

- send 产物 `takedown/<slug>/notice-v<N>.md`、respond 产物 `takedown/inbound/<slug>/triage.md`、counter 产物 `takedown/<slug>/counter-notice-v<N>.md`——与 PROC-10 的 glob `**/takedown/**/triage.md` 匹配（Python glob 的 `**` 递归语义下，`takedown/inbound/<slug>/triage.md` 必然命中）。
- post 记录 `submission.md` / `counter-submission.md` 为 PROC-14 的文本候选提供锚点。

### 9.3 check.py 独立性

`python check.py <workspace> <tool_log> <agent_output>` 三参契约自洽，import `_shared.checker` 成功（依赖存在，实测 import 无异常）。7 项检查中 6 项有可命中的正路径（§5.2 正则实测），QA-01 仅靠短语候选通过（§10.3）。独立运行无需任何外部服务。

### 9.4 外部依赖与测评环境的耦合（本技能最大的执行风险）

Step 1 要求加载 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`，缺失或含 `[PLACEHOLDER]` 即停机转冷启动。这是**正确的产品行为**（律师技能绝不能在无 profile 时盲目起草），但对评测而言构成强环境耦合：若 harness 未预置该文件，合规 agent 会正确停机，SCOPE-02 靠 tool_log 命中（agent 会读路径或提到 cold-start）通过，而 PROC-05/10/12/14/OUT-01/QA-01 全部落空，最终得分被系统性压低——**表现越合规，得分越低**。runner 必须在工作区预置一份已完成（无占位符）的 profile（含 Approval matrix → DMCA takedown (ordinary) 行、Outputs、Who's using this），或为评测提供专门说明。详见 §13 🔴-1。

### 9.5 PROC-14 的不可满足性

按 SCOPE-04「只起草不提交」，评测中 `submission.md` 永远不会被写出；PROC-14 是 output_contains 检查，只能靠 agent 在聊天输出中提及「post-send 记录将写入 submission.md」来通过——判定名义与判定实际脱节。详见 §13 🔴-3。

---

## 10. SCORING 交叉参考

### 10.1 结构与编号

22 项 criterion 编号连续无断层（SCOPE-01..04 / PROC-01..14 / OUT-01..02 / NEG-01 / QA-01），`total_items: 22` 与实际一致，category 无错配（send 6 / respond 4 / counter 4 的 PROC 分段与 SKILL.md 三模式章节完全对应）。`pattern: process` 与技能实际形态一致。

### 10.2 检查-实现-测评三方咬合度

15 项 LLM 判定全部可追溯（§5.3 表格），7 项脚本判定 6 项与实现精确咬合（§5.2），剩余 1 项（QA-01）存在正则缺陷。CCF-01/02/03 三个归零项全部对应 SKILL.md 的硬性保障（合理使用门 + 大声门 / 联邦管辖 + 律师审查 / 引用验证），语义正确。

### 10.3 QA-01 正则与模板错配（本次审查确认的唯一 check 层缺陷）

SCORING QA-01 的判定模式 `(1\.\s*Signature|2\.\s*Identification|good faith belief|penalty of perjury|authorized to act)` 中，前两个编号候选以「数字 + 点 + 可选空白 + 单词」匹配模板。但 SKILL.md Step 6 模板的条目格式是 `1. **Signature** (physical or electronic)`——数字与单词之间有 `**` 粗体标记。实测 `re.search(r'(?i)1\.\s*Signature', '1. **Signature**')` 返回 **False**（`\s*` 只匹配空白，`Signature` 之前是 `**`）。同理 `2\.\s*Identification` 对 `2. **Identification of the copyrighted work**` 也返回 False。

后果：QA-01 实际只靠后三个短语候选通过（L143-144 的 `good faith belief` / `penalty of perjury` / `authorized to act` 逐字命中）。若未来模板修改措辞使短语候选漂移，或 agent 输出采用编号列表但非逐字短语，检查将静默失准。**修复**：模式改为 `1\.\s*\**Signature`（容忍粗体）或删除编号候选只保留短语候选。详见 §13 🔴-2。

### 10.4 PROC-14 语义脱节

判定描述为「Post-send/counter records written (submission.md / counter-submission.md) with watch window and legal hold refreshed」，检查为 output_contains。在 SCOPE-04「不提交」的约束下，产物文件物理不可达，检查退化为「聊天输出里提到过」。建议二选一：(a) 描述改为「post-send record 计划被提及」并注明评测语义；(b) 增加模拟提交步骤（如 agent 写出 submission.md 占位记录），使检查成为真实文件检查（file_exists）。详见 §13 🔴-3。

### 10.5 SCOPE-02 环境耦合

SCOPE-02 判定「practice profile loaded; if [PLACEHOLDER] or missing, agent stops and routes to cold-start-interview」，检查为 tool_log 正则。如 §9.4 所述，未预置 profile 时该检查通过但其余 6 项脚本检查全部落空。该问题不在 SCORING 本身（判定正确），而在 runner 的 provisioning——但 SCORING 文件应在注释中提示运行方预置要求（建议在 SCOPE-02 或文件头注明「评测需预置已完成配置的 ip-legal profile」）。详见 §13 🔴-1。

### 10.6 综合评价

SCORING 设计的最大优点与 301 相同：问题问的是「门是否运行、要素是否齐备、产物是否满足契约」而非「是否完成了任务」，把测评锚定在可验证的法定要素与门纪律上。22 项中 15 项 LLM 判定的提问质量高（问题文本本身就是要素清单），是语料中测评设计最好的法律类 SCORING 之一。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier（`skill-dossier.md`）中 077-takedown 条目（行 613-619）原文要点：

- **逻辑**：三模式清晰分发，法定要素清单与 10-14 工作日窗口正确。
- **语法**：优秀专业法律文体，结构清晰，无错字或断句。
- **人机感**：中性，恰当正式的法律语调，引用的用户面向脚本无 filler 或 emoji。
- **合规**：🟢 完全合规——三必需节齐全，body ~387 行。
- **总评**：🟢 顶级法律 skill：彻底、gate-driven、完全合规。

另有两条关联记录：

- 「典范 Skills」表（行 1171）：| 077 | takedown | 顶级法律过程 skill |——与 017-cease-desist、170-worker-classification、185-privilege-log-review、258-termination-review 并列法律类标杆。
- 批次记录（076-100 批）：🔴 0 个 / 🟠 4 个需修复 / 🟢 8 个优秀——077 属于 🟢 优秀批次，非 🟠 名单。

**本报告与 dossier 的分歧/增补**：dossier 零问题记载与本次审查的正文结论一致（正文本体零缺陷）；但 dossier 未覆盖测评检查层——本报告新发现 QA-01 正则错配（🔴-2）、PROC-14 语义脱节（🔴-3）、SCOPE-02 环境耦合（🔴-1）三项，以及 description 触发短语字面差异（🟡-4，dossier 的「完全合规」未细察 §2.4 逐字信号）。这些是 dossier 粒度之外的增量发现，不推翻 🟢 评级。

---

## 12. 综合评分（八维加权）

| 维度 | 权重 | 得分 | 说明 |
|---|---|---|---|
| 1. Frontmatter 与描述 | 10 | 9.5 | 完全合规结构；触发短语非逐字命中 §2.4（🟡-4）；name 领域信号弱（🟡-9） |
| 2. Body 结构与完整性 | 10 | 9.5 | 12 章节三模式分治，382 行精炼自包含；输出节分散缺汇总表（🟡-5） |
| 3. 文档-实现逻辑一致性 | 15 | 14.5 | 法定要素/时间窗口/判例全部实测正确；仅 3 处冗余重复（🟡-6） |
| 4. SCORING 与 check.py 质量 | 10 | 9.0 | 22 项结构完整、15 项 LLM 问题全可追溯；QA-01 正则缺陷（🔴-2）与 PROC-14 语义（🔴-3） |
| 5. 脚本正确性与可执行性 | 20 | 18.0 | 7 项检查映射正确、6 项正则实测命中；check.py `_is_path` 冗余（🟡-8）；环境耦合属 runner 侧（🔴-1） |
| 6. 规范合规 | 10 | 9.5 | 12 项中 10 项全过，第 5/9 项合规带保留意见 |
| 7. 人机感 | 10 | 10.0 | 大声门 + 律师简报 + 审查者结语 + one-way door 原则，语料最佳之一 |
| 8. 可执行性与测评对接 | 15 | 13.0 | 决策树完备、路径与 glob 咬合；profile 预置依赖 + PROC-14 不可满足 |

加权合计：9.5 + 9.5 + 14.5 + 9.0 + 18.0 + 9.5 + 10.0 + 13.0 = **93.0 / 100**。

评级：A+（语料第一梯队）。结论判语：与 dossier 🟢「顶级法律 skill」完全互证——正文本体（法定要素、门纪律、人机边界）无可挑剔；全部失分集中在测评检查层与打磨层，且三项高优先级修复（🔴-1/2/3）全部在 30 分钟内可完成，正文一个字都不用改。就「文档-测评」协同而言，本技能是语料中法律类的最佳样本。

---

## 13. 修复建议（按优先级分层）

### 修复清单总览

| ID | 严重度 | 位置 | 问题 | 工作量 |
|---|---|---|---|---|
| 🔴-1 | 高 | runner / SCORING | 外部 profile 未预置时合规 agent 停机导致 6/7 脚本检查落空 | S |
| 🔴-2 | 高 | SCORING.yaml QA-01 | 编号正则 `1\.\s*Signature` 无法命中粗体模板 `1. **Signature**` | XS |
| 🔴-3 | 高 | SCORING.yaml PROC-14 | 「记录已写出」语义在只起草不提交约束下不可满足 | S |
| 🟡-4 | 中 | SKILL.md L3 | 触发短语非逐字命中 §2.4 五个信号 | XS |
| 🟡-5 | 中 | SKILL.md 正文 | 输出契约分散三处，缺「模式→产物→路径→头部规则」汇总表 | S |
| 🟡-6 | 中 | SKILL.md L8-60 | 模式罗列三处、无 flag 提问脚本两处逐字重复 | XS |
| 🟡-7 | 中 | SCORING.yaml PROC-10 | triage.md 仅查存在性，未校验 work-product 头部/特权声明内容 | S |
| 🟡-8 | 中 | check.py L22-30 | `_is_path` 防御逻辑冗余且极端路径下失效 | XS |
| 🟡-9 | 低 | SKILL.md L3 | `takedown` 名无领域信号，可考虑 `dmca-takedown`（语料级决策） | XS |
| 🟢-10 | 低 | SKILL.md L18 | ✗ 符号与 dossier「无 emoji」记载的字面差异，可选改文字 | XS |
| 🟢-11 | 低 | SKILL.md L372 | "calendared" 生僻但合法，可选改为平实表达 | XS |
| 🟢-12 | 低 | SKILL.md L20-24 | Examples 可补 --send/--counter 带上下文参数的示例 | XS |

### 🔴 高优先级（影响测评结果或核心语义）

1. **评测环境预置 ip-legal 实践 profile（或改造停机语义）** — runner 侧。问题链：SKILL.md Step 1（L16）要求加载 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`，缺失或含 `[PLACEHOLDER]` 即停机转 `/ip-legal:cold-start-interview`。在未预置的评测环境中，表现完全合规的 agent 会在 Step 1 正确停机，SCOPE-02 通过（tool_log 命中 cold-start 路径），而 PROC-05/10/12/14/OUT-01/QA-01 六项脚本检查全部落空——**合规行为反而拿到最低分**，且 LLM 判定项（SCOPE-01/03/04、PROC-01..09/11/13、OUT-02、NEG-01）也会因没有产物而失去可评材料，实质上把一次有效测评变成冷启动路由测试。修复：runner 在任务工作区预置一份已完成配置的 profile，使 agent 能走完 send/respond/counter 全流程；并在 SCORING.yaml 文件头加注释注明该预置要求，防止未来运行方漏配。**预置 profile 的最小字段清单**（对照 SKILL.md L70-71 的 Load context 依赖）：

| profile 章节 | 必须包含的内容 | 缺失后果 |
|---|---|---|
| `## IP practice profile` | 版权注册信息（可为 "none"） | 仅影响识别作品步骤的填充质量 |
| `## Enforcement posture` → Approval matrix → DMCA takedown (ordinary) 行 | 审批人姓名/角色 | send Step 7 的审批人占位无法填充 |
| `## Outputs` | work-product 头部文本、角色 | OUT-01 对照缺失，输出头部规则不可用 |
| `## Who's using this` | 律师 / 非律师 | 非律师简报分支（L177-181）不触发 |
| `## Matter workspaces` | `Enabled: ✗`（或提供切换能力） | 若未提供该节，L18 的 ✗ 判定无依据 |

其中 Approval matrix 行、Outputs、Who's using this 三项是硬依赖（缺失直接导致 Step 1 停机或下游分支不可达）；Matter workspaces 用 `Enabled: ✗` 是最低成本配置（默认跳过 matter 机制，L18 与 L71 均支持此默认）。另注意：profile 路径在 `~/.claude/plugins/...` 用户主目录下，评测沙箱若为独立 HOME 需在启动前写入该路径，这是 runner 侧最容易漏的环节。工作量：S。
2. **修复 QA-01 编号正则** — `SCORING.yaml:180-187`。`1\.\s*Signature` 与 `2\.\s*Identification` 无法命中 SKILL.md Step 6 模板的 `1. **Signature**` / `2. **Identification of the copyrighted work**`（`\s*` 不匹配 `**`，实测 re.search 返回 False）。当前检查靠后三个短语候选（`good faith belief` / `penalty of perjury` / `authorized to act`）通过，编号候选形同虚设。修复：模式改为 `(?i)(1\.\s*\**Signature|2\.\s*\**Identification|good faith belief|penalty of perjury|authorized to act)`（在 `\s*` 后加 `\**` 容忍粗体标记），或直接删除编号候选、保留短语候选。验证方法：修复后对 SKILL.md Step 6 模板文本（L137-145）与三份产物模板（send 通知 / counter 反通知 / triage 备忘）各跑一次 `re.search`，确认编号候选命中。现模式与建议模式对比：

```
# 现状（编号候选实测不命中）
(?i)(1\.\s*Signature|2\.\s*Identification|good faith belief|penalty of perjury|authorized to act)
# 建议（\** 容忍 ** 粗体标记）
(?i)(1\.\s*\**Signature|2\.\s*\**Identification|good faith belief|penalty of perjury|authorized to act)
```

注意 `\**` 也会命中无粗体的纯文本 `1. Signature`（`\*` 量词为 0 次即合法），向后兼容。工作量：XS。
3. **修正 PROC-14 的判定语义** — `SCORING.yaml:146-152`。判定描述「Post-send/counter records written (submission.md / counter-submission.md) with watch window and legal hold refreshed」要求记录文件已写出，但 SCOPE-04（L380-381）与 Step 8 输出说明（L197/L372 的 "After submission, write..."）明确通知/反通知只起草、由用户提交——评测环境中 `submission.md`/`counter-submission.md` 物理不可达，检查退化为「agent 在聊天输出中提及」。修复二选一：(a) 描述改写为「post-send record 计划被明确提及（文件名 + watch window + legal hold）」，与可满足语义对齐；(b) 场景设计加一步「用户确认已提交，agent 写出 submission.md 占位记录」，此时可升级为 file_exists 真文件检查。工作量：S。
4. **description 触发短语对齐 §2.4** — `SKILL.md:3`。现为 "Use when asserting copyright through..."，未逐字命中 §2.4 的五个信号（"Use when the user..." 三变体 / "Triggers on..." / "Use for..."）。修复：改为 "Use when the user asserts copyright through a §512(c)(3) takedown..."，零语义损失、零成本消除字面合规争议。工作量：XS。
5. **新增「输出契约」汇总表** — 正文建议位置：`## Notes` 之后或新设 `## Outputs` 章节。现状：三模式输出约定分散于 send Step 8（L185-197）、respond Step 4（L247-306）、counter Step 4（L362-372），读者需读完全部三节才能拼出完整映射。建议新增顶层 `## Outputs` 章节，内容全部已有，纯收拢，不新增知识点。建议表格形态：

| 模式 | 主产物 | 头部规则 | 记录文件 | in-chat 呈现 |
|---|---|---|---|---|
| `--send` | `takedown/<slug>/notice-v<N>.md`（或 .docx） | **不带** work-product 头部 | `submission.md` | 明文预览 + 审查者结语 |
| `--respond` | `takedown/inbound/<slug>/triage.md` | **带** work-product 头部 | （无独立记录文件） | 四选项 + 推荐 + 声明 |
| `--counter` | `takedown/<slug>/counter-notice-v<N>.md` | **不带** work-product 头部 | `counter-submission.md` | 明文预览 + 审查者结语 |

表内每格均可从现有正文逐字取源（L187/L197/L249/L364/L372），且与 OUT-01 的判定口径（外部文档不带头部、内部草稿带）天然呼应。顺带满足 §3.1「Output Format」作为单一可见章节的字面可读性（现判合规靠 "any heading name" 条款）。工作量：S。
6. **合并重复的模式罗列与无 flag 提问脚本** — `SKILL.md:8-12`（开篇速览）、`:20-24`（Instructions Step 3）、`:54-60`（Purpose）。三处模式集合一致属刻意冗余可接受，但无 flag 提问脚本在 L24 与 L60 逐字重复，违反知识增量原则。建议：开篇速览保留（快速定位价值），Purpose 的 L60 提问句删除（由 Instructions 单一持有），或反之。工作量：XS。
7. **PROC-10 增强为内容校验** — `SCORING.yaml:113-119`。现仅 `file_exists` 查 triage.md 存在性，未验证其必须携带 work-product 头部与特权继承声明（L252-254 模板明确要求）。建议在 SCORING 中为 PROC-10 增加第二段脚本检查 `file_contains`（checker.py 已提供该函数，L31-43），模式例如：

```yaml
- id: PROC-10
  check:
    fn: file_exists
    path: "**/takedown/**/triage.md"
  check2:
    fn: file_contains
    path: "**/takedown/**/triage.md"
    pattern: "(?i)(work-product|privilege|ATTORNEY)"
```

使「特权边界」这一本技能的核心人机设计进入脚本可验证层（现仅靠 LLM 项间接覆盖）。若 SCORING 结构不支持单 criterion 双 fn，则新建 PROC-10b 条目，编号保持连续。工作量：S。
8. **简化 check.py 的 `_is_path` 逻辑** — `check.py:22-30`。`main()` 已读取文件并传内容给 `check()`，`check()` 内再 `os.path.exists(agent_output)` 纯属冗余防御——正常路径多一次无谓 set；若输出文本恰好等于某个存在的路径字符串（病态输入），`set_agent_output` 被跳过，全部 output_contains 检查读陈旧状态。修复：删除 `_is_path` 分支，`check()` 无条件 `set_agent_output(agent_output)`；`main()` 的文件读取逻辑保留。替换后 `check()` 头部应为：

```python
def check(workspace: str, tool_log: str, agent_output: str) -> dict[str, bool]:
    """Run all 7 script checks. Returns {id: bool}. True = pass."""
    set_tool_log_path(tool_log)
    set_agent_output(agent_output)  # main() 已解析文件内容，直接注入
    result = {}
    ...
```

删掉 L24-30 的 `_is_path` 判定与 `except (OSError, ValueError)` 分支，共约 6 行净减。工作量：XS。
9. **name 领域信号（可选，语料级决策）** — `SKILL.md:2` 与目录名。`takedown` 一词在非法律语境同样高频，匹配阶段可能被体育/金融/通用「下线」任务误触发；description 已强力兜底，故仅为可选优化。若语料整体做意图匹配实验，可评估改为 `dmca-takedown`（需同步改目录名与 SCORING `skill:` 字段，牵动面小）。工作量：XS（评估）/ S（改名）。
10. **✗ 符号的字面口径** — `SKILL.md:18`。dossier 记载「无 emoji」，实测正文含 ✗（U+2717，`if `Enabled` is `✗``）与 →（U+2192，节标题箭头）。两者均为功能符号，不构成问题；若追求与档案口径逐字一致，可将 ✗ 改为文字（如 "if matter workspaces are disabled"）——纯可选。工作量：XS。
11. **"calendared" 用词（可选）** — `SKILL.md:372`。法律事务语境合法但小众，若面向非律师用户可改为 "watch window end date entered on the calendar"。纯文风，工作量 XS。
12. **Examples 补带参数示例** — `SKILL.md:34-39`。现有 4 例覆盖三模式 + 无 flag，但 `--send`/`--counter` 无带上下文参数示例（`--respond` 有路径示例）。可补 `--send ~/workspace/evidence/` 类一行，帮助 agent 理解参数与模式的关系。工作量：XS。

### 建议实施顺序

以上 12 项相互独立，无前置依赖，可按「测评侧 → 文档侧 → 文风侧」分三波落地：

1. **第一波（测评侧，30 分钟内，影响评分有效性）**：🔴-1（runner 预置 profile + SCORING 头注释）→ 🔴-2（QA-01 正则加 `\**`）→ 🔴-3（PROC-14 描述对齐）→ 🟡-7（PROC-10 内容校验）。这四项完成前，任何一轮测评跑出的分数都存在系统性偏差；完成后 22 项判定的名义语义与实际语义完全一致。
2. **第二波（文档侧，一次编辑会话）**：🟡-4（触发短语）→ 🟡-5（Outputs 汇总表）→ 🟡-6（重复合并）→ 🟡-8（check.py 简化）。四项均为 SKILL.md / check.py 局部编辑，不动任何法定要素文本；改动后需回归验证：SKILL.md 仍 ≤600 行、YAML 仍可解析、check.py 7 项检查对 SKILL.md 文本的正则命中不降级（重点回归 QA-01 与 PROC-05/12/14）。
3. **第三波（可选）**：🟡-9（改名，需语料级评审）→ 🟢-10/11/12（文风与示例打磨）。

回归建议：每波完成后运行 `python check.py <ws> <log> <out>` 冒烟验证一次，并重跑 §5.2 的正则命中清单（PROC-05/12/14/OUT-01 共 19 个短语候选，全部应保持命中）。

### 修改影响面评估

| 修复 | 改动文件 | 涉及行 | 影响面 |
|---|---|---|---|
| 🔴-1 | runner 配置 + SCORING.yaml 头注释 | 新增注释（0 行代码） | 测评有效性 |
| 🔴-2 | SCORING.yaml QA-01 | L180-187 的 pattern | 1 项脚本判定 |
| 🔴-3 | SCORING.yaml PROC-14 | L146-152 的 description | 1 项脚本判定 |
| 🟡-4 | SKILL.md frontmatter | L3 description | 触发匹配 + §2.4 合规字面 |
| 🟡-5 | SKILL.md 正文 | Notes 后新增章节（~12 行） | body 382 → ~394 行，仍远低于 600 |
| 🟡-6 | SKILL.md 正文 | L60 或 L24 删一句 | 零功能影响 |
| 🟡-7 | SCORING.yaml PROC-10 | L113-119 增 check2 | 1 项脚本判定强化 |
| 🟡-8 | check.py | L24-30 删除 | 7 项检查执行路径，行为不变 |
| 🟡-9 | 目录名 + SKILL.md + SCORING | 全套更名 | 需语料级协调 |
| 🟢-10/11/12 | SKILL.md | L18 / L372 / L34-39 | 零功能影响 |

影响面评估结论：12 项修复合计新增正文不超过 15 行、删除不超过 10 行、正文字数净增小于 1%，无任何一项触及法定要素、gate 顺序或输出路径等核心语义；全部完成后本技能仍是语料中正文最小改动、测评受益最大的修复集合。

### 修复优先级总结

🔴-1 是**唯一影响测评是否成立**的问题，属于 runner 配置而非技能缺陷；🔴-2/🔴-3 是 check 层的两个精确小修，合计改动量不超过 20 个字符加一段注释。🟡-4 至 🟡-8 共 5 项为一致性/可验证性打磨，全部可在一次编辑会话内完成。正文本体（法定要素、门纪律、人机边界）**零修改建议**——本技能的正文质量经得起 dossie 的 🟢 评级，修复建议全部落在 SKILL.md 的打磨层与测评检查层，不触及任何核心语义。

---

## 附录：审查执行验证记录

1. **行数与规模**：SKILL.md 386 行（frontmatter 4 + body 382）、check.py 81 行、SCORING.yaml 200 行（wc 实测），与 dossier「~387 行」一致。
2. **YAML 解析**：frontmatter 与 SCORING.yaml 均 `yaml.safe_load` 解析通过；description 实测 453 字符（≤1024 ✅）。
3. **正则命中实测**：以 SKILL.md 实际文本为语料，对 check.py 全部 7 个模式逐一 `re.search` 验证——PROC-05/10/12/14/OUT-01 命中确认；QA-01 编号候选 `1\.\s*Signature` / `2\.\s*Identification` 对 `1. **Signature**` / `2. **Identification...**` 返回 False，短语候选命中（🔴-2 依据）。
4. **符号扫描**：Unicode category S/C 全量扫描，正文含 ✗（U+2717）与 →（U+2192）两个功能符号，无 emoji、无 box-drawing 字符。
5. **判例与法条核验**：Lenz 801 F.3d 1126 (9th Cir. 2015)、Diebold 337 F. Supp. 2d 1195 (N.D. Cal. 2004)、Stephens 796 F.3d 281 (3d Cir. 2015) 三处引用核对无误；§512(c)(3)(A) 六要素与 §512(g)(3) 四要素逐项对照法条通过；10–14 工作日窗口五处出现全部一致。
6. **dossier 交叉**：skill-dossier.md 行 613-619（077 条目）、行 1171（典范 Skills 表）、076-100 批次记录（🟢 8 个优秀）三处记录与本次审查互证。
