# REVIEW: 127-policy-redraft

**审查日期**: 2026-08-06
**Skill 类型**: process — 对监管 gap 产出带标记的政策重起草提案（marked-up redraft proposal），上游输入来自 policy-diff / gap-surfacer，输出为政策所有者审阅用的第一稿备忘录
**Body 行数**: 199 行（SKILL.md，远低于 600 行硬上限）
**参考文件数**: references/0, scripts/0, assets/0, 其他/0（目录仅含核心三文件，无任何子目录；该 skill 的配置与政策库索引全部读取自插件级 CLAUDE.md，本地无资产依赖，结构上自洽）

---

## 1. 目录全量清单 (tree, every file + line count)

```
D:\SkillIF\skill-experiment\complex-skills\127-policy-redraft\
├── SKILL.md         199 行   (14,262 B)
├── SCORING.yaml     143 行   ( 6,183 B)
└── check.py          75 行   ( 2,400 B)
```

- 目录共 3 个文件、417 行，无隐藏文件、无子目录（已用 `ls -laR` 与 find 双重确认）。
- 参考文件统计：references/0、scripts/0、assets/0。该 skill 的全部运行上下文（政策库索引、practice profile、gap tracker、matter 工作区）来自 `~/.claude/plugins/config/claude-for-legal/regulatory-legal/CLAUDE.md` 及同目录 yaml 文件，产出物是纯 markdown 备忘录，因此零本地引用文件是合理的，不属于引用缺失。
- 三个文件均被完整阅读（SKILL.md、SCORING.yaml、check.py 全文），并交叉比对了 `_shared/checker.py`（check.py 的导入依赖）、`_shared/CHECKER-LIBRARY.md`（函数语义）、`_shared/SKILL-SPEC.md`（合规基线）以及同族上游技能 201-policy-diff 的 check.py/SCORING.yaml 约定。

各文件结构一览（便于定位）：

**SKILL.md（199 行）**：frontmatter（1-5 行）→ 顶部摘要步骤 1-7（8-14 行）→ proposal 性质 callout（18 行）→ Matter context（20-22 行）→ Purpose（26-28 行）→ 六条硬护栏（30-39 行）→ Step 1 Gather inputs 三输入（41-66 行）→ Step 2 规则时效核验与 UNVERIFIED banner（68-80 行）→ Step 3 重起草约定：粒度/Change 注释/标签词汇/scope discipline（82-108 行）→ Step 4 备忘录模板（110-161 行）→ Filename 约定（163-171 行）→ Config-dependent fallbacks（173-180 行）→ Interactions with other skills（182-186 行）→ 决策树说明（188-190 行）→ What this skill does not do（192-198 行）。

**SCORING.yaml（143 行）**：`pattern: process`、`total_items: 15`；criteria 按 5 类分布——SCOPE 3 项（6-29 行）、PROC 5 项（31-70 行）、OUT 3 项（72-95 行）、NEG 3 项（97-120 行）、QA 1 项（122-129 行）；其中脚本判据 5 个（SCOPE-03、PROC-03、OUT-01/02/03），LLM 判据 10 个；critical_failures 3 项（131-142 行），effect 均为 cap_to_0。

**check.py（75 行）**：导入 `_shared/checker.py`（10-15 行）→ check() 内 5 个 tool_log_contains 判据（18-52 行）→ main() 处理 4 参数并读 agent_output 文件（55-71 行）。全部判据基于 tool log，未使用 output_contains。

---

## 2. 逻辑一致性

整体逻辑链条极严密：gap 输入（1a）→ 当前政策文本（1b）→ 规则文本（1c）→ 规则时效核验（Step 2）→ 最小编辑重起草（Step 3）→ 备忘录输出（Step 4）→ 明确"不关闭 gap"（guardrail 2 / 顶部 step 7 / 185 行三处呼应）。"proposal 而非 edit"这一核心立场贯穿 description、顶部 callout（18 行）、六条硬护栏、文件名约定（163-171 行）、"What this skill does not do"（192-198 行），无一处走样。上游接缝（policy-diff 的 source tags、severity floor 于 184-186 行）也衔接干净。

发现一处真实的内容矛盾（🟡）：

- SKILL.md:159 输出模板的选项 4 写着 "**Watch and wait** — if the rule's status is uncertain or the policy owner is unavailable, **I'll add a revisit note to the gap tracker**"（"我来往 gap tracker 里加一条 revisit note"）。
- 但 SKILL.md:185 明文规定 "**Gap tracker state:** this skill does NOT change the tracker. It doesn't mark the gap closed, doesn't mark it in-progress, doesn't touch `notified`."
- SCORING.yaml:100 的 NEG-01 同样要求 "Agent refrains from **closing or updating** the gap in the tracker"。
- 三者冲突：向 tracker 写入 revisit note 就是对 tracker 的更新，与"绝不改动 tracker"的绝对表述、以及与测评项 NEG-01 的判定口径直接矛盾。若 revisit note 机制确实允许，则 185 行的绝对化表述需收窄；若不允许（按 185 行，纸面记录由 policy owner/user 在 apply+approve 后自行更新），则 159 行措辞必须改为 "I'll draft a revisit note **for you to add** to the gap tracker"。

其余次要逻辑点（不构成缺陷，仅记录）：

- 顶部摘要步骤 1-7（8-14 行）与正文 "Step 1: Gather inputs"（41 行）～"Step 4: Output"（110 行）存在编号错位：摘要 step 3/4/5/6 对应正文 Step 1/2/3/4，摘要 step 1（加载配置）与 step 7（不关闭 gap）在正文无对应分节。第 9 行 "Use the workflow below" 已声明摘要性质，读者可映射，但两套平行编号相差一位仍是小认知税（详见第 13 节 🟢-1）。
- 模板选项 2 "Get more info on [X]" 与 Step 2 的核验动作存在轻微重叠（都是补全证据），但选项是面向用户的后续交互菜单，不算矛盾。
- 模板选项 1（156 行）"When approved, tell me and I'll mark the gap closed" 与护栏 2 的拒绝话术（35 行）措辞互补：前者是正常闭环路径，后者是用户试图跳过审阅时的拦截，两者语义不冲突，设计意图正确。
- 模板选项 4（159 行）"if the rule's status is uncertain or the policy owner is unavailable" 的两个触发条件分别对应 Step 2 的 UNVERIFIED 场景与 Config-dependent fallbacks 的 owner 缺失场景（177 行），条件来源清晰；唯一的（也是真实的）问题是"add a revisit note"与 185 行的绝对禁令冲突，见上文。

关于矛盾本身的修复方向再展开一点：把 159 行改为 "I'll **draft** a revisit note for you to add to the gap tracker" 是代价最小的方案（一个字之差），且与 185 行"the policy owner or the user can update the gap entry"的纸面记录机制完全对齐；若反向允许 agent 写 tracker，则需要同时修改 185 行、NEG-01 的 question 措辞（SCORING.yaml:100-104）以及"Interactions"节对 `notified` 字段的绝对保护，改动面更大、风险更高，故推荐前者。

---

## 3. 语法与可读性

SKILL.md 全文 199 行无错别字、无病句、无断裂的 markdown 结构，是审查过的语料库中文字最干净的一批之一。重点核查过的易错点均未出问题：markdown 围栏（模板块 112-161 行）闭合正确；inline code 与 backtick 配对无误；引用块、表格（change summary 表 139-142 行）、复选框清单（146-150 行）排版全部规范；`⚠️`、`✗`、`🔴/🟠` 等符号在 banner/配置/severity 场景中均为功能性使用，无装饰性 emoji。

两处措辞层面的小问题（🟢 级）：

- SKILL.md:142 change summary 表第 2 行的 Verify 列写作 `` `[verify — model knowledge]` ``——带反引号、且词序为 "verify — model knowledge"；而 Step 3 约定（102 行）定义的源标签词汇是 `[model knowledge — verify]`、`[web search — verify]`（无反引号包裹，与 141 行 `[Federal Register]` 格式一致）。模板示例与规则词汇表不一致，agent 照抄模板会产出与自身规则不符的标签。建议改为 `` `[model knowledge — verify]` `` 或去掉反引号。
- SKILL.md:186 "Silent demotion is a contradiction a reviewing lawyer cannot see."——语义成立（静默降级造成的矛盾是审阅律师看不见的），但句式容易被读成"律师看不见矛盾"，建议改写为 "Silent demotion hides a severity contradiction from the reviewing lawyer."
- 标点与破折号风格全篇统一（em-dash 间隔是法律家族约定文体，与 201-policy-diff 一致），无中英混排、无冗余空格；第 113 行模板头 "WORK-PRODUCT HEADER — per plugin config ## Outputs" 使用全大写+破折号的家族标记法，属惯例而非错误。
- 模板中占位符方括号的使用（`[policy name]`、`[GAP-ID or short description]`、`[N items marked [review] inline | none]`）在 112-161 行内格式自洽，且 Step 1-3 已定义过这些占位符的取值来源（GAP-ID 来自 1a、日期来自 167 行约定、sections 来自 1b），不存在悬空占位符——这一点优于语料库中大量"模板里出现未定义占位符"的 skill（对比 076-investor-brief-writer 的 `{{EXEC_SUMMARY_CARDS}}` 未定义问题）。

---

## 4. 人机感

本 skill 的人机感是最大亮点，与 dossier 中"127 典范"的评价一致：

- 六条硬护栏（30-39 行）全部带用户可直接引用的拒绝话术（35、36 行的完整对话脚本），且话术分场景（"close the gap now" 与 "apply this for me" 是两种拒绝理由），不是同一句车轱辘话复用。
- 输入缺失时"ask, don't infer"（43 行）、"Do not guess at the policy text from the gap tracker or from web search"（57 行）——把"不猜测"落到具体可执行的行为，而不是空泛口号。
- 1b 分支（54-57 行）对文件与粘贴文本给出不同处理（文件路径→读后确认版本；粘贴→trust but flag in reviewer note），人机职责切分细致。
- "Scope discipline"（104-108 行）对"发现第二个 gap 怎么办"给出明确行为（不静默修复、记入 reviewer note、建议 follow-on gap），是同类 skill 中少见的成熟设计。
- 模板末尾的 "What next? Pick one"（154-160 行）给出五个可选后续动作，交互上尊重用户决策权。

无需修改。唯一注意点：66 行的 "no silent supplement" 规则指向插件级 CLAUDE.md 的原文引用（28-subpoena-triage 家族同款），依赖该配置实际存在，本目录内无法验证（详见第 8 节）。

从交互细节再举两个正面证据，说明"人机边界成熟"不是空话：

- 35 行与 36 行的两段拒绝话术刻意使用不同句型——前者以 "I produce the proposal." 起句（先亮身份），后者以 "I don't apply policy changes" 起句（先给否定理由）。同一个"我是提案者不是执行者"的信息，按用户请求类型（关闭 tracker vs 应用改动）调整了强调点，这是针对 agent 的语境化输出设计，而非静态模板。
- 22 行 Matter context 的启用检查（`Enabled` 为 `✗` 时静默跳过）避免了"配置未启用却每次都向用户解释 matter 机制"的噪音；178 行的 "Say nothing about config when the values are populated" 是同族策略的又一实例——配置正常时不打扰、配置缺失时才暴露，交互负担控制得体。
- 187 行附近的 severity floor 以 "a contradiction a reviewing lawyer cannot see" 为理由解释为什么禁止静默降级——把法律审查的可见性作为设计约束，是法律家族 skill 特有的、且正确的人机分工意识。

---

## 5. 规范合规性（SKILL-SPEC v1.0）

逐条对照 SKILL-SPEC v1.0 核查：

- **Frontmatter 必需字段**：name、description 齐备。description（3 行）为第三人称、含 WHAT（produce a marked-up policy redraft）+ WHEN（"Use when the user says 'redraft the policy', 'draft the policy fix', 'mark up the policy'"），长度约 380 字符，远低于 1024 上限，触发信号满足 §2.4。argument-hint 属 §1.2 允许字段，使用正确。
- **§2.5 description 规避项**：description 中出现 `/regulatory-legal:gaps`、`/regulatory-legal:policy-diff`、`gap-surfacer` 三个外部名称。严格按 §2.5 字面，跨技能路由（"NOT for X, use Y instead"）禁止进 description；此处引用是描述 gap 输入的来源（input provenance）而非路由指令，且均为同一插件（claude-for-legal/regulatory-legal）的子命令，与同族 skill 约定一致。结论：可辩护的边界情形，建议保留，但值得在审查文档中显式记录这一先例（见第 13 节 🟢-3）。
- **§3.1 三个必需节**：workflow（顶部步骤 + Step 1-4 + 六护栏）、output format（Step 4 模板 + Filename 节 + Before applying 清单）、scope/limitations（"What this skill does not do" + 护栏 2/3/5）。三节齐全。
- **§3.2 行数**：199 行 ≤ 600。✓
- **§3.3 文件引用**：全部路径引用为插件配置路径（8、22、48 行）或相对文件名（167 行），无跨技能文件路径、无 `../_shared/` 式目录穿越。✓
- **§3.4 知识增量**：body 给出可执行过程与判定规则，不是知识罗列。✓
- **`model` / 非标 frontmatter 字段**：无违规字段。

合规结论：🟢 完全合规，无硬性违规。唯一建议是把 description 中外部技能名称的处理方式作为家族先例写入共享规范说明（如 CHECKER-LIBRARY 或 family conventions 文档），避免后续审查标准摇摆。

与 skill-dossier 档案的对照：dossier（2026-08-05 批次 126-150 摘要）对本 skill 的记录为 "127 🟢 三节齐全；逻辑：从 gap 输入到草案输出的流程环环相扣、护栏完备；语法：精炼规范；人机感：对越权请求给出明确拒绝话术、人机边界成熟；合规：🟢 三节齐全"，并列入 🟢 典范 Skills 表（"写作类典范"）。本次逐行复审与档案结论一致，仅档案未覆盖的两个新发现：一是 159 行 revisit note 与 185 行/NEG-01 的措辞矛盾（档案未记录，属本次新增发现）；二是测评层（SCORING/check.py）的 4 项精细度问题。两者都不推翻 🟢 评级，只说明档案的"典范"判断需要小幅修正说明而非降级。

---

## 6. 可执行性（步骤与依赖）

- 每一步都有明确的输入/输出/判定门：Step 1 三输入缺一即问（43 行）；Step 2 给出一组可操作的红旗（适用日期超 30 天、规则年龄超 12 个月、政治上争议的最终规则）与核验渠道（research MCP、web search、Federal Register docket），并给出无法核验时的标准 banner 文本（78 行）供直接照抄；Step 3 的红线粒度阶梯（86-92 行）与 Change 注释模板（99 行）可复制；Step 4 的完整备忘录模板（112-161 行）含占位符说明，agent 只需填空。
- 文件名约定（163-171 行）给出正例（`[policy-name]-proposed-redraft-[YYYY-MM-DD].md`）和反例（`[policy-name].md`、`[policy-name]-v2.md`），并解释 "proposed-redraft" 与日期是 load-bearing 的，防呆设计到位。
- Config-dependent fallbacks（173-180 行）覆盖了配置缺失的两个分支（owner 缺失仍出稿并在 reviewer note 中提示、library 为空则停下询问），且明确 "Say nothing about config when the values are populated"——避免 agent 把配置细节泄入正常输出。
- 依赖外部插件配置是本家族设计使然（同 028、034、201），不作为缺陷。

一个可执行性盲点（🟢 级）：Step 1a 的 gap 输入分支提到 "load the entry from ... gap-tracker.yaml"，但 Step 4 与 reviewer note 模板没有给"gap entry 里的字段应如何体现到备忘录"的映射指引（例如 GAP-ID 的 🔴/🟠 severity 如何带入 Bottom line——186 行有 severity floor 规则，但没有演示如何把 tracker 字段翻译成 memo 字段）。对完全照章执行的 agent，这是一处可补的映射说明，非必须。

另外三处执行细节的一致性核验（全部通过，仅记录）：

- 80 行 "Emit that banner above the work-product header" 与 78 行 banner 文本、119 行 reviewer note 的 Currency 行（"unverified — see banner above"）三者互相指向，banner 的放置位置在三个地方被一致描述，无歧义。
- 171 行 "Do not write to the policy library source directory" 与 34 行 "The output goes to a new file ... Not `[policy-name].md`"、167 行文件名约定三处共同构成"写入位置安全网"，且与 CF-01（cap_to_0）的判定目标一致。
- 66 行的 "offer the user the options (paste full text, point at primary source, web-search-with-verify-tag, or stop), and wait" 给出了完整的选项枚举，agent 无需自行发明处理路径；"and wait" 明确禁止自行继续，是可执行的闸门而非原则性表述。

---

## 7. 护栏与防御性

本维度近乎满分，逐条核对六条硬护栏的执行一致性：

- 护栏 1（proposal 非 edit）：与顶部 step 6、Filename 节、模板 Status 行（127 行 "PROPOSAL — not yet reviewed or approved"）四重呼应。✓
- 护栏 2（不关闭 gap）：与顶部 step 7、185 行、模板选项 1（156 行 "When approved, tell me and I'll mark the gap closed"）呼应；唯一的裂缝即第 2 节所述 159 行 revisit note 矛盾。✓（除该裂缝外）
- 护栏 3（"Apply this for me" 拒绝）：仅出现一次（36 行），无内部矛盾。✓
- 护栏 4（版本确认）：37 行（护栏）、55 行（1b 文件分支）、146 行（checklist）三处重复同一问句，属有意强化，但三处逐字重复是语料库中少见的冗余度（见 🟢-4）。
- 护栏 5（最小编辑）：38 行与 87-90 行逐字重复同一条粒度阶梯，同样属有意强化。
- 护栏 6（[verify] 标签穿透）：39 行定义、80 行（banner 场景）、101 行（Step 3 约定）、102 行（源标签穿透）、141-142 行（模板示例）共五处呼应，是全文纪律性最强的规则。✓

防御设计超出同族平均水平的两点：186 行的 cross-skill severity floor（上游 🔴/🟠 不得静默降级）与 66 行的 no silent supplement 闸门（规则文本不完整时给用户四个选项并等待）。这两处说明设计者清楚"AI 起草法律文书"场景下的静默偏差风险，值得其他 legal 类 skill 借鉴。

---

## 8. 引用与文件完整性

- 本目录内引用：SKILL.md 未引用任何本地 references/scripts/assets 文件（前文已述，符合设计）。✓
- 外部配置依赖（本目录无法验证、需插件侧确认）：`~/.claude/plugins/config/claude-for-legal/regulatory-legal/CLAUDE.md`（8、22、175 行）、`gap-tracker.yaml`（48 行）、`matters/<slug>/matter.md`（22 行）、`## Outputs` / `## Who's using this` / `## Cross-skill severity floor` 三个配置节（113、186 行）。这些与 017、018、028、034、201 等法律家族 skill 的引用模式完全一致，且 201-policy-diff 的 check.py:34 用 `regulatory-legal/CLAUDE\.md` 作脚本检查佐证了该路径是家族约定，认定可信；但 REVIEW 职责范围内应记录"插件侧文件存在性未在此次审查中验证"。
- check.py:11 的 `sys.path.insert(0, ... "..", "_shared")` 依赖 `complex-skills/_shared/checker.py` 存在——已实际验证该文件存在（143 行 docstring 与 5 个文件检查、9 个 JSON 检查、2 个时间戳检查、4 个 tool-log 检查、2 个 output 检查函数齐全），且 201-policy-diff 的 check.py:11 使用完全相同的路径。✓ 运行 runner 时必须挂载 `_shared` 目录，这属于共享基础设置。
- SCORING.yaml 中 6 个脚本判据（SCOPE-03、PROC-03、OUT-01、OUT-02、OUT-03）的 regex 转义在 YAML 双引号语义下正确落地（`\\d` → `\d`、`\\[` → `\[`），与 checker.py 的 `re.search` 语义（对 json.dumps 后的整条 tool-log 记录做正则）匹配。✓

---

## 9. 测评设计（SCORING.yaml）

`total_items: 15` 与 criteria 实际数量（SCOPE 3 + PROC 5 + OUT 3 + NEG 3 + QA 1 = 15）一致；三个 critical_failures 独立计数，均为 cap_to_0 语义，与 family 惯例一致。判据结构与 SKILL.md 的规则一一对应（每条 guardrail、每个模板元素都有测评项覆盖），覆盖度是语料库中较好的。

对 6 个脚本判据的逐条执行语义验证（对照 checker.py 实现）：

- SCOPE-03（SCORING.yaml:27-29，`proposed-redraft-\d{4}`）：YAML 双引号将 `\\d` 还原为 `\d`，checker.py:259 `tool_log_contains` 对每条 JSONL 记录 `json.dumps` 后 `re.search`——会命中 Write 工具 file_path 参数或 Bash 命令中含该模式的任何记录。语义成立，但如前述存在假阳性与冗余两个问题。
- PROC-03（SCORING.yaml:52-54，`\[verify\]`）：转义正确，匹配含 `[verify]` 的记录；SKILL.md 要求标签进 redraft 文件本身（39、101 行），而 tool log 只在 Write 内容字段可见——若 tool log 不含 Write 内容字段则该判据可能假阴性，取决于 runner 的日志详细程度，建议在 runner 文档中确认 Write 内容是否入 log。
- OUT-01（SCORING.yaml:77-79，`proposed-redraft-\d{4}-\d{2}-\d{2}`）：与文件名约定（167 行）逐字对应，是本组最可靠的判据；与 SCOPE-03 的从属关系见下文。
- OUT-02（SCORING.yaml:86-88）：`|` 在正则中为交替，YAML 双引号下原样传递，语义为"任一个标题出现即通过"，见下文问题。
- OUT-03（SCORING.yaml:93-95，`Before applying`）：SKILL.md 第 144 行标题为 "### Before applying — checklist"，子串匹配命中，可靠。
- 六个判据均无正则书写错误、无 YAML 转义错误；pattern 与 SKILL.md 内容的对应关系全部核验通过（对比 201-policy-diff 的 check.py:34 用 `regulatory-legal/CLAUDE\.md` 检查配置加载，本 skill 未检查"读取插件 CLAUDE.md"这一 step 1 动作——若团队想把该前置步骤纳入脚本验证，可参照 201 的做法补一条 `regulatory-legal/CLAUDE\.md` 的 tool_log_contains，当前该动作仅由 LLM 判据间接覆盖）。

测评设计上四个问题（均不致命，但值得修）：

- **SCOPE-03 与 OUT-01 完全冗余（🟡）**：SCOPE-03 的 pattern 是 `proposed-redraft-\d{4}`，OUT-01 是 `proposed-redraft-\d{4}-\d{2}-\d{2}`。任何命中 OUT-01 的日志记录必然命中 SCOPE-03（年份是完整日期的子串），反之不成立。两条判据在同一个 tool log 上跑，SCOPE-03 恒为 OUT-01 的弱化副本，零信息增益——15 项里有 1 项是无效测评。
- **OUT-02 存在部分命中即通过的问题（🟡）**：pattern `"### Bottom line|### Change summary"` 是正则交替，命中任一个标题即通过，而 description（82 行）承诺的是"bottom line + marked-up policy section(s) + change summary table"三要素。缺 bottom line 只写 change summary 的备忘录照样过 OUT-02。建议拆成两个独立判据（或用一个正向环视/两个子模式 AND）。
- **PROC-01 与 NEG-01 本可脚本化却走了 LLM judge（🟢）**：PROC-01 的验证对象是 SKILL.md:78 的固定文本 "RULE STATUS UNVERIFIED"，NEG-01 的拒绝话术也是固定脚本（35-36 行的 "I produce the proposal"）。固定字面量用 `tool_log_contains` 判定比 LLM judge 更便宜、更稳定。
- **critical_failures 无任何脚本检测（🟡，需 runner 侧确认）**：CF-01（写入源政策文档）、CF-02（关闭 gap）、CF-03（缺输入直接起草）在 SCORING.yaml:131-142 声明，但既无 judge/check 字段，check.py 也完全不处理。CF-02 与 CF-03 是可脚本化的（CF-02：tool log 中出现对 gap-tracker.yaml 的 Write/Edit；CF-03：Write redraft 之前无对政策文本的 Read）。若 runner 对 critical_failures 有默认的 LLM 兜底判定则无碍，但本目录三文件均无证据，建议在 runner 文档中显式确认，或把 CF-02/CF-03 脚本化（CF-01 因源文件名随任务变化，保持 LLM 判定合理）。

一个补充观察（记录不修改）：SCOPE-03/OUT-01 检查的是"tool log 中出现该文件名模式"，而非"工作区里确实存在该输出文件"。agent 若只在对话里提到正确的文件名而未实际写文件，检查仍会通过（假阳性）。配合 `file_exists('${WORKSPACE}/**/proposed-redraft-*.md')` 可消除此盲区。

---

## 10. check.py 实现

check.py（75 行）结构干净、与 SCORING.yaml 的 5 个脚本判据完全对齐（SCOPE-03、PROC-03、OUT-01、OUT-02、OUT-03），且与同族 201-policy-diff 的 check.py 骨架一致（相同的 `_shared` 导入、相同的 main() 参数约定、相同的 `os.path.exists` 防御式判断）。逐行核查：

- 22-28 行：对 `agent_output` 做 `os.path.exists` 探测并 try/except 包裹，处理"参数可能是原始文本"与 Windows 长字符串路径异常两种情况，防御到位。
- 34 行 SCOPE-03 与 42 行 OUT-01 的 pattern 与 SCORING.yaml 逐字一致。
- 一个死代码问题（🟢）：本 skill 的 5 个检查全部基于 tool_log，但 24-28 行与 main() 63-65 行仍把 agent_output 读入并通过 `set_agent_output` 注入——checker.py:333 有 `output_contains`，但本 check.py 从未调用它（对比 201-policy-diff 的 check.py:50 确实用了 `output_contains`）。这段接线在本 skill 中是无用代码，可删或留作模板一致性（若团队模板统一保留，建议加注释说明"当前无 output 判据"）。
- 一个维护性风险（🟢）：SCORING.yaml 与 check.py 双份维护同一组 pattern（SCOPE-03/OUT-01/OUT-02/OUT-03 四处重复）。本次审查验证了当前两处一致，但任何单侧修改都会造成静默分叉。若 runner 能直接从 SCORING.yaml 派生脚本检查则更优；否则建议在 check.py 头部注释中声明"与 SCORING.yaml 对应判据同步"的维护契约。
- 运行时行为：`_log_search` 对每条 JSONL 记录做 `json.dumps` 后 `re.search`（checker.py:249-256），因此 pattern 会匹配到 Write 的 file_path/content、Bash 命令、Read 路径等一切字段，与设计意图一致；无需修改。

结论：check.py 功能正确、无 bug，问题仅在第 9 节所述的判据设计层面与其自身两处小瑕疵。

---

## 11. 与上游/下游技能的一致性

- **上游 policy-diff（201）**：Step 2 明确复用其 rule-status check 模式（69 行），source tags 与 `[verify]` 标记要求从 diff 携带到 redraft（102 行），severity floor 承接其 gap 分级（186 行）。方向一致，无冲突。201 的 check.py:34 用 `regulatory-legal/CLAUDE\.md` 佐证了本 skill 配置路径的家族约定。
- **上游 gap-surfacer**：GAP-ID 入口（48 行）、"gap closes when applied AND approved"的生命周期定义与 guardrail 2、185 行一致。
- **下游 cold-start-interview**：177 行引用 `/regulatory-legal:cold-start-interview --redo` 作为 owner 指派工具，与 322 号 skill 的家族角色一致。
- **未来技能预告**：197-198 行声明 `:package`（多政策批处理）与 `:apply`（带审批闸门的应用流程）为 future skill，把当前边界外的能力显式划出，避免误触发，是良好的边界管理。
- **测评骨架**：check.py 与 201-policy-diff 的 check.py 结构、_shared 依赖、main() 约定完全同构，家族一致性优秀。

唯一跨技能一致性问题仍是第 2 节的 revisit note 矛盾（159 行 vs 185 行 vs NEG-01），不涉及其他 skill。

---

## 12. 综合评分

| 维度 | 权重 | 得分 | 说明 |
|---|:---:|:---:|---|
| 逻辑一致性 | 15% | 9.0 | 全链条自洽，唯一裂缝：159 行 revisit note vs 185 行"绝不改 tracker" |
| 语法与可读性 | 10% | 9.5 | 全文干净无错字；142 行标签词汇与 102 行定义不一致 |
| 人机感 | 10% | 10.0 | 拒绝话术、ask-don't-infer、scope discipline 均为家族标杆 |
| 规范合规性 | 20% | 9.5 | 三节齐全、199 行、description 合规；外部技能名进 description 属可辩护边界 |
| 可执行性 | 15% | 9.5 | 每步有输入/输出/判定门与可复制模板；唯一盲点：tracker 字段→memo 映射指引缺位 |
| 护栏与防御性 | 15% | 10.0 | 六护栏四重呼应、severity floor、no silent supplement 闸门 |
| 引用与文件完整性 | 5% | 10.0 | 目录内引用零缺失；外部配置路径与家族约定一致（插件侧未验证，已记录） |
| 测评完备性 | 10% | 7.5 | 判据覆盖好但 SCOPE-03 冗余、OUT-02 部分命中即过、CF 无脚本检测、check.py 有死代码 |
| **加权总分** | 100% | **9.4** | 🟢 好 — 可用无重大问题，建议按第 13 节做小幅清理 |

---

## 13. 修复建议

### 🔴 致命

无。该 skill 无需重写或重大修复，与 dossier 中"127 典范"评级一致。

### 🟡 重要（建议修复，工作量 0.5-1 天）

1. **解决 revisit note 矛盾（SKILL.md:159 + SCORING.yaml NEG-01）**：三处口径必须统一。推荐方案：保留"绝不改 tracker"的绝对立场（这是本 skill 最重要的安全属性），把 159 行选项 4 改为 "I'll **draft** a revisit note for you to add to the gap tracker when you're ready"，并在 185 行补一句"revisit note 的书面记录同样由 owner/user 写入"。若产品意图是允许 agent 写 revisit note，则反过来收窄 185 行并同步 NEG-01 的 question 措辞（"closing or updating" 需改为 "closing or changing status"）。改一处，三处同步，工作量约 0.5 小时。
2. **SCOPE-03 与 OUT-01 去重（SCORING.yaml:23-29 vs 73-79）**：二选一——删除 SCOPE-03（OUT-01 是它的严格超集），或把 SCOPE-03 改为独立信号（如 `file_exists` 检查 `${WORKSPACE}/**/proposed-redraft-*.md`，同时消除第 9 节提到的"只提文件名不写文件"假阳性）。推荐后者：既去重又补了真阳性。工作量约 0.5 小时。
3. **OUT-02 拆分为双判据（SCORING.yaml:82-87）**：把 "### Bottom line|### Change summary" 交替 pattern 拆成 OUT-02a（`### Bottom line`）与 OUT-02b（`### Change summary`）两条，或改用同时匹配两者的正则（如 `(?s)` 组合或分两次调用 AND）。否则"只写一半模板"的备忘录可通过。工作量约 0.5 小时，注意同步 check.py:43 与 total_items。
4. **确认或补上 critical_failures 的检测路径（SCORING.yaml:131-142）**：向 runner 侧确认 CF 是否有 LLM 兜底判定；若没有，为 CF-02（tool log 中 `gap-tracker` 相关 Write/Edit）与 CF-03（redraft 写入前无任何政策文本 Read）补脚本判据。这是本 skill 三个 cap_to_0 项，是测评体系里最不该留白的地方。工作量约 1 天（含 runner 改动）。

### 🟢 优化（可选，工作量 0.5 天以内）

1. **摘要步骤与正文步骤的编号错位（SKILL.md:8-14）**：两个方案——把摘要步骤改名为 "0." 或字母序（A-G），或在摘要 step 后加映射注释 "Step 1-4 below"；更激进的做法是删除摘要列表（其内容已被顶部 callout、六护栏、详细步骤完全覆盖），保留 7 条反而引入编号税。
2. **统一 verify 标签词汇（SKILL.md:142）**：将 `` `[verify — model knowledge]` `` 改为 `[model knowledge — verify]`（与 102 行定义的 `[model knowledge — verify]` 一致，去掉反引号与 141 行 `[Federal Register]` 同格式）。
3. **把 description 中的跨技能名称处理记为家族先例**：`/regulatory-legal:gaps`、`policy-diff`、`gap-surfacer` 出现在 description（3 行）属于输入来源描述而非 §2.5 禁止的路由，建议在共享规范（SKILL-SPEC 或 family conventions）中补一条"插件子命令与上游输入来源允许进 description，路由指令禁止"的判定标准，避免后续审查标准摇摆。
4. **去处三处逐字重复（SKILL.md:37/55/146 与 38/86-92）**：版本确认问句保留护栏 4 与 checklist 两处即可，1b 文件分支可改为 "ask the version-confirmation question from guardrail 4 and note the answer"；粒度阶梯同理。若团队认可"护栏+操作节重复是法律家族的有意设计"，则保留并在文档注明。
5. **PROC-01 与 NEG-01 转脚本判据（SCORING.yaml:34-39、98-104）**："RULE STATUS UNVERIFIED" 与 "I produce the proposal" 是固定字面量，`tool_log_contains` 即可覆盖，降低 LLM judge 成本与抖动。
6. **check.py 清理（check.py:24-28、63-65）**：删除未使用的 agent_output 注入接线，或加注释说明"本 skill 无 output 判据，代码保留以保持家族模板一致"；并在文件头补一行"patterns 须与 SCORING.yaml 同步"的维护契约。
7. **改写 186 行**："Silent demotion is a contradiction a reviewing lawyer cannot see." → "Silent demotion hides a severity contradiction from the reviewing lawyer."（消除歧义）。
8. **补 tracker→memo 字段映射指引（SKILL.md Step 4 或 1a 附近）**：给一行示例说明 GAP-ID 的 severity/status 如何落入备忘录的 Gap 行与 Bottom line，方便完全照章执行的 agent。

### 关键修复的具体改法示例

**🟡-1 矛盾消除（SKILL.md:159）**：将模板选项 4 改为——

```
4. **Watch and wait** — if the rule's status is uncertain or the policy owner is
   unavailable, I'll draft a revisit note **for you to add** to the gap tracker.
```

同时无需改动 185 行与 NEG-01（保持"绝不改 tracker"的绝对立场）。

**🟡-2 SCOPE-03 改造（SCORING.yaml:23-29）**：删除 tool_log_contains 判据，改为——

```yaml
  - id: SCOPE-03
    category: scope
    description: "Output is a PROPOSAL written to a new '[policy-name]-proposed-redraft-[YYYY-MM-DD].md' file — the source policy document is never modified"
    judge: script
    check:
      fn: file_exists
      pattern: '${WORKSPACE}/**/proposed-redraft-*.md'
```

保留 OUT-01 的 tool-log 判据，形成"文件名出现在日志（OUT-01）+ 文件确实存在（SCOPE-03）"的双重验证，并需在 check.py 中同步（改用 `file_exists` 并传入 workspace 参数）。

**🟡-3 OUT-02 拆分（SCORING.yaml:82-87）**：拆为两条或改为双模式——

```yaml
  - id: OUT-02
    category: output
    description: "Memo includes bottom line, marked-up policy section(s), and change summary table (provision, current, proposed, why, verify)"
    judge: script
    check:
      fn: tool_log_contains
      pattern: '### Bottom line'
    # 配套：OUT-02b 使用 pattern: '### Change summary'，两条 AND 后计入 total_items=16
```

**🟡-4 CF-02/CF-03 脚本化（check.py 新增）**：CF-02 可用 `tool_log_not_contains('gap-tracker\\.yaml')` 且要求 Write 记录中不含 gap-tracker 路径；CF-03 可用 `tool_log_read_before_write(['policy.*\\.(md|docx|pdf)'], require_all=False)` 的否定形态（先有 Write 无 Read 即失败）。若 runner 已对 critical_failures 做 LLM 兜底，此两项可作为加强而非必需。

### 工作量评估

| 级别 | 项数 | 预估 |
|---|:---:|---|
| 🔴 致命 | 0 | — |
| 🟡 重要 | 4 | 0.5-1 人天（含 runner 侧 CF 确认） |
| 🟢 优化 | 8 | 0.5 人天 |
| **合计** | 12 | **1-1.5 人天** |

### 复审清单（修复后回看）

- [ ] SKILL.md:159 与 185 行、SCORING.yaml NEG-01 三处口径一致；
- [ ] SCORING.yaml 的 SCOPE-03 与 OUT-01 不再是子串从属关系；
- [ ] OUT-02 的"三要素"判据不再单标题通过；
- [ ] check.py 与 SCORING.yaml 的 pattern 双份同步（或已改为单一来源）；
- [ ] CF-01/02/03 有确定的判定路径（脚本或 runner LLM 兜底）；
- [ ] SKILL.md:142 标签词汇与 102 行定义一致；
- [ ] description 跨技能名称的处理已作为先例记录到共享规范。

### 总结论

127-policy-redraft 是法律家族 process 类 skill 的标杆——逻辑链条完整、护栏设计与拒绝话术成熟、人机边界清晰、三节合规无缺。所列问题全部是测评基建（SCORING/check.py）层面的精细度问题和一处措辞矛盾，不触及 skill 本体质量。修复后可作为家族模板参照。
