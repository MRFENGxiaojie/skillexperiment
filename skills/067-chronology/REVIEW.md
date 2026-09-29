# REVIEW: 067-chronology

**审查日期**: 2026-08-06 | **Skill 类型**: process — 诉讼时间线构建（文档提取、去重、显著性标注与特权纪律协议） | **Body 行数**: 274 | **参考文件数**: 0（外部插件契约 7 处）

---

## 1. 目录全量清单

目录 `D:\SkillIF\skill-experiment\complex-skills\067-chronology\` 共 4 个文件（1 个 Body + 2 个评测附属文件 + 1 个本审查文档）：

| # | 文件路径 | 行数 | 类型 | 说明 |
|---|---|---|---|---|
| 1 | `SKILL.md` | 279 | Body | Frontmatter 5 行 + Body 274 行（L6–L279）+ 尾空行 |
| 2 | `SCORING.yaml` | 207 | 评测标准 | 23 条 criteria（4 scope + 4 process-gate + 7 process + 5 output + 2 negative + 1 qa）+ 3 条 critical_failures |
| 3 | `check.py` | 73 | 评测脚本 | 3 个 script 检查（OUT-01 / OUT-02 / OUT-03），依赖 `_shared/checker.py` |
| 4 | `REVIEW.md` | 4 | 审查文档 | 旧版 stub（本文件即为其替换物，原文见附录） |

要点：

- 目录结构与 corpus 标准一致：`NNN-kebab-case-name/` + `SCORING.yaml` + `check.py`，**无 `references/`、无 `scripts/` 子目录**——SKILL.md 自含全部内容，零内部文件依赖（与 037-brief-section-drafter 同为"全量内联"设计，但本 skill 体量更大、章节更多）。
- 无触发对照集存在：`complex-skills-no-trigger\067-chronology\`（同一 corpus 的对照组）含 SKILL.md / SCORING.yaml / check.py。`diff` 结果显示：**SCORING.yaml 与触发版逐字节相同**；SKILL.md 仅 description 差异（对照版删去全部 WHEN 触发句，仅保留 WHAT 句，见 §2.2）；check.py 差异仅为触发版多一段 `is_path` 防御分支（见 §5.3）。该对照组由 `create_no_trigger_set.py` 生成，与 2 Mode × 5 Harness 测评矩阵设计一致。
- 旧 REVIEW.md 为 stub（内容见附录），已被本文替换。

---

## 2. Frontmatter 逐字段审查

### 2.1 字段清单

| 字段 | 值 | 判定 | 依据 |
|---|---|---|---|
| `name` | `chronology` | ✅ | 小写 + 连字符，≤64 字符；与目录 `067-chronology` 的 kebab 部分完全一致（NNN 前缀属目录命名规范，不进入 name 字段，符合 corpus 惯例） |
| `description` | 见 2.2 逐句分析 | ✅ | ≤1024 字符（实测 376 字符） |
| `argument-hint` | `"[slug] [--format=working\|sof\|witness-[name]]"` | ⚠️ | SPEC §1.2 允许字段；YAML 引号解析合法；但 **flag 词汇与正文不一致**——正文定义的是模式 flag `--matter`/`--documents`（L39/41），而 hint 给出的 `--format=` 三值（working/sof/witness-[name]）在正文中从未显式定义（详见 §4.1-#3、§13 P3） |

无任何 SPEC §1.3 禁用键（无 `metadata`/`version`/`tags`/`trigger`/`model` 等）。YAML 语法合法：description 为未加引号的 plain scalar，内含两个双引号（`says "chron from the production" or "what happened when"`）——plain scalar 中段嵌双引号合法（仅句首双引号需转义），实测可解析；内含 em dash（`—`）与冒号后跟空格（`[slug] [--format=...]` 在 argument-hint 值内），argument-hint 为双引号包裹字符串，均无解析问题。

### 2.2 description 逐句分析

原句（L3）：

> Build or update a chronology from declared document sources and uploads — dated events extracted, de-duped, and tagged by significance per the matter theory. Use when the user asks to build a chronology or timeline from a production or matter file, says "chron from the production" or "what happened when", or needs a working, statement-of-facts, or witness-specific timeline.

| 句 | 内容 | 三问定位 | 判定 |
|---|---|---|---|
| 句 1 | Build or update a chronology from declared document sources and uploads；后接三步过程（dated events extracted / de-duped / tagged by significance per the matter theory） | WHAT（动作 + 核心过程链） | ✅ 具体不空洞，三步过程与 Body 的 Step 2（提取）/Step 4（去重）/Step 5（显著性标注）逐一对应——description 与 body 的契约对齐清晰 |
| 句 2 | Use when the user asks to build a chronology or timeline from a production or matter file / says "chron from the production" or "what happened when" / needs a working, statement-of-facts, or witness-specific timeline | WHEN（三个触发场景 + 两个用户口语触发词 + 三种变体需求） | ✅ 触发覆盖面完整：动作动词（build/update）、口语触发（"chron from the production"、"what happened when"）、变体名（working / statement-of-facts / witness-specific）与 Body Output formats 节三变体完全对应 |

**Voice**：动词开头（"Build or update..."）描述 skill 的功能，与 SPEC §2.6 的 Good 示例同一句式——描述 WHAT 的动词开头不构成 imperative 违规（§2.3 禁止的是 "Use this skill to..." 式与第一/二人称）；全文第三人称，无 "I/you/we"。**无跨 skill 路由**嵌入，符合 §2.5。

**触发信号**（§2.4 要求至少一条）：句 2 以 "Use when the user asks to build..." 开头——**字面命中标准信号** `"Use when the user asks to..."`，无 037/034 的"变体句式带注通过"问题，本字段合规性无瑕疵。

**KEYWORDS**：chronology、timeline、production、matter file、statement-of-facts、witness-specific——领域词齐全；口语触发词（"chron from the production"、"what happened when"）是该家族 skill 中少见的"真实用户话术"式关键词设计，对触发匹配质量是明显加分。

**对照版（no-trigger）**：description 截为仅句 1（约 173 字符）。保留 WHAT 与 KEYWORDS、删除全部 WHEN 触发句——符合无触发对照集的设计目的，对照版语义仍完整可读。

### 2.3 语法

- description 内嵌双引号是唯一潜在脆弱点：现行 plain scalar 写法实测合法，但后续若在句首引入引号可能破解析；可考虑整体双引号包裹并转义内层引号（§13 P6 附带提及）。
- `argument-hint` 中 `|` 为字面量（flag 值分隔符），`[slug]`/`[--format=...]` 为占位符写法，符合 hint 惯例。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（L6–L279）

| 行号 | 标题 | 级别 | 功能 | 备注 |
|---|---|---|---|---|
| L6 | `# Chronology` | H1 | 标题 #1 | **与 L21 重复**（见下） |
| L7–17 | 10 条编号 TL;DR + 过程链 | — | 极简总览 | 与正文各节重复（见 §4.1-#1）；**未覆盖两道 gate**（L7–17 无特权 gate、无冲突 gate） |
| L19 | `---` | — | 分隔线 | 残片性质（TL;DR 区块的收尾线） |
| L21 | `# Chronology` | H1 | 正文标题 | 重复的第二个 H1 |
| L23–31 | `## Disclosed-document use restrictions` | H2 | 合规护栏：disclosure/发现所得文档的使用限制（CPR 31.22 隐含承诺 / US Rule 26(c) / 其他法域） | 前置护栏，含确认话术与 ⚠️ 旗标模板 |
| L33–35 | `## Purpose` | H2 | 动机 + "garbage-in, garbage-out" 边界声明 | 简洁得体 |
| L37–46 | `## Modes` | H2 | 双模式：`--matter`（in-house）/ `--documents`（firm associate / paralegal），按 `## Role` 选默认、flag 可覆盖 | 对应 SCOPE-02；solo/other 回退分支明确 |
| L48–56 | `## Side framing (significance tags)` | H2 | 攻防双框架：plaintiff（offensive）/ defense（defensive）显著性判定 | 对应 PROC-11 的"per case theory"语义细化；输出头部须注明所用框架 |
| L58–77 | `## Load context` | H2 | 加载插件 CLAUDE.md / 先前 chronology.md / 会话内上传 + **冲突 gate（不可绕过，`--matter` 模式）** | 冲突 gate 在 L73–77（正文加粗段落），对应 PROC-02/CF-03 |
| L79–169 | `## Workflow` | H2 | 6 步工作流（Step 0–6） | 详见 3.2 |
| L171–251 | `## Output formats` | H2 | 三变体：working（默认，含完整模板）/ SoF / witness-specific | 详见 3.2 |
| L253–261 | `## Incremental builds` | H2 | 增量构建：读旧版→重建→diff（新增/修改/移除）→版本号递增→变更摘要 | 对应 OUT-05 |
| L263–271 | `## Integration with matter.md / history.md` | H2 | 与 history.md 有意分离：hold 进 history、breach notice 进 chronology | 边界声明自洽 |
| L273–278 | `## What this skill does not do` | H2 | 边界（4 条） | 对应 SPEC 必需"Scope"节 |

### 3.2 必需章节（SPEC §3.1）

| 必需章节 | 位置 | 判定 |
|---|---|---|
| Workflow / Process | `## Workflow`（L79–169），6 个 `### Step N`（Step 0 特权 gate → Step 6 write） | ✅ 完整、有序、每步可执行；Step 0 是全程最重的门（A/B/C 三姿态），Step 2 含 no silent supplement 四选项升级话术 |
| Output Format | `## Output formats`（L171–251） | ✅ **独立成节且是三节中内容最厚的**：working 模板完整内联（L177–241，含特权继承横幅、头部 8 字段、时间线表、Key events、Gaps、Marker discipline、Version 五子节）+ SoF 变体（特权过滤默认 + `--include-flagged` 显式确认）+ witness 变体——corpus 中输出规格最完备的 skill 之一 |
| Scope / Limitations | `## What this skill does not do`（L273–278） | ✅ 4 条显式边界（不解决矛盾/不发明事件/不保证完备/不代决特权），另有 4 处功能式边界：disclosed-doc 限制（L23–31）、冲突 gate（L73–77）、特权 gate（L81–97）、no silent supplement（L125） |

### 3.3 委托结构

- **本目录内委托**：无——不引用任何 `references/` 或 `scripts/` 文件，全部内容内联（与 037 同款零悬空引用设计；若继续扩展建议下沉到 references/，见 §13 P6）。
- **外部插件委托**（关键）：`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 被 7 处引用，承担：插件 CLAUDE.md（`## Role`/`## Landscape`/`## Case theory`/`## Document review`/`## Outputs`/`## Decision posture`/`## Side`/`## Who's using this` 小节）、`matters/[slug]/matter.md`（theory/pivot fact/key facts）、`matters/_log.yaml`（冲突 gate 实体）、`matters/[slug]/chronology.md`（输出路径）。**无回退**——这是本 skill 最大的可移植性风险（详见 §4/§5/§9/§13 P0）。
- 跨 skill 引用均为散文式命名（`matter-intake` L75、`deadlines` 提及于 L273 家族语境、eDiscovery 平台名），无 `../other-skill/` 文件级引用，符合 SPEC §3.3。

### 3.4 层级健康度

- **H1 出现两次**（L6/L21）——同一文件内两个 `# Chronology`，与 034-client-intake（L6/L20）、037-brief-section-drafter（L6/L15）同源同款，是该插件家族模板的共同特征（§13 P2）。
- H2 为主干（10 个），H3 用于 6 个 Step + 3 个输出变体（10 个），层级 2–3 级、单调递增，无跳级。
- 段落长度：最长为 Step 2 的 no silent supplement 段（L125，四选项话术完整引用）；L129 的"标签纪律覆盖法律结论"段是全程信息密度峰值（tag 覆盖 timeline/Gaps/Key events/Theory tie lines/时效窗口）。整体段落节奏良好。
- 章节顺序的叙事弧合理：护栏前置（disclosed-doc → Purpose → Modes → Side → Load context + 冲突 gate）→ 执行（Workflow Step 0–6）→ 输出三变体 → 增量构建 → 集成边界 → Scope。与 037 同为"先立规矩后干活"的成熟法律类组织方式。

### 3.5 长度

- Body 274 行（L6–L279），文件总计 279 行。process 模式目标 ~200 行，本 skill 超出约 35%——体量偏大但信息密度高（双 gate + 三态特权 + 完整输出模板），无明显注水；再扩展建议下沉（§13 P6）。
- dossier 记"正文 279 行"——实测 279 为文件总行数（含 frontmatter），正文 274 行，无实质分歧。

---

## 4. 逻辑一致性深度审查

### 4.1 衔接与指代

| # | 发现 | 严重度 |
|---|---|---|
| 1 | **10 步 TL;DR 与正文重复，且遗漏两道 gate**：L7–17 的总览与正文各节重复（1=Load matter.md ↔ Load context；2=Load CLAUDE.md ↔ Load context；3=workflow ↔ 全篇；4=sources ↔ Step 1；5=extract ↔ Step 2；6=dedupe ↔ Step 4；7=tag ↔ Step 5；8=write ↔ Step 6；9=version ↔ Incremental builds；10=confirm ↔ QA-01）。**但全 skill 最重要的两道 gate（冲突 gate L73–77、特权 gate L81–97）在 TL;DR 中完全缺席**——快速阅读者会误以为时间线构建没有前置审批门槛。另：TL;DR 10 步 vs Workflow 7 步（Step 0–6）编号体系不一致，心智映射有额外开销。 | 🟡 |
| 2 | **"reference below" 无明确指代**（L9）："Follow the workflow and reference below"——正文即工作流本身，"reference" 指代下方详述章节（非独立文件），语义可通但含混；与 037 的 L9 同源同款措辞。 | 🟢 |
| 3 | **argument-hint 与正文 flag 词汇不一致**：hint 定义 `--format=working\|sof\|witness-[name]` 三值，正文仅在 L15 出现 "format variant per flag"、L169 "Variants on request"——`--format` 的具体语法与三值语义在正文**从未定义**；反之正文的模式 flag `--matter`/`--documents`（L39/41）也未进入 hint。单一词汇表原则被破坏，agent 收到 hint 后无法在正文找到 `--format=sof` 的展开说明（只能靠输出格式节的"on request"理解）。 | 🟡 |
| 4 | 双 gate 的时序自洽：冲突 gate（Load context L73–77，`--matter` 模式）→ Step 0 特权 gate（L81–97，每次必跑）→ 提取（Step 2）。NEG-01（提取前必须过特权 gate）与 CF-02/CF-03 的判定路径与 body 时序完全一致；`--documents` 模式的 gate 豁免（L77）也明确了"pre-matter research"输出定位，无自相矛盾。 | ✅ |
| 5 | 特权三态规则（L143–149）的语义闭环完整：`ok`（无可信特权理论）→ `flag`（默认项，dominant-purpose 边缘/诉讼预期边缘/内容混杂均入此）→ `review`（元数据缺失无法判断）；并给出"单向门 vs 双向门"的偏好论证（under-flagging 失特权不可逆 → 倾向 flag）。这是 corpus 中最精细的特权分类逻辑之一。 | ✅ |
| 6 | 三处话术模板双向一致：特权 gate A/B/C 选项（L87–93）、no silent supplement 四选项（L125）、确认话术（L17/L176"Scan the 🔴 entries — anything I miscalled?"）——agent 行为确定性高，与 SCORING 的 QA-01 逐字对齐。 | ✅ |
| 7 | SoF 特权过滤（L247）与 B-mixed 姿态的衔接：默认排除 🔒 条目、`--include-flagged` 需显式确认并写入头部——与 Step 0 的姿态记录（L95）形成闭环，无缝隙。 | ✅ |
| 8 | L129 的"标签纪律覆盖法律结论"与 L127 的来源标注规则互补而非冲突：来源标签管"事件从哪里来"，结论标签管"法律分析由什么支撑"——两族标签的分工在 §13 P6 建议集中定义（正文目前散落于 Step 2/L129/模板 Marker discipline 三处）。 | 🟢 |

### 4.2 矛盾检查

- 无自我矛盾声明。六重护栏（disclosed-doc 限制 / 冲突 gate / 特权 gate / no silent supplement / 显著性纪律 / 来源标签纪律）相互独立、无优先级冲突——与 037 并列为 corpus 护栏密度最高的两个 skill。
- 法条/规则引用准确：CPR 31.22（L27）隐含承诺（collateral use restriction）表述正确——"you may only use them for the purpose of the proceedings... unless the court grants permission, the disclosing party consents, or the document has been read in open court" 与英国实务一致；US Rule 26(c)（L28）protective order 引用正确；Kovel / common-interest / joint-defense / work-product 术语（L83）使用准确。
- 模式差异的边界声明自洽：`--matter` 读 matter.md（pivot fact 供显著性标注）、`--documents` 读 eDiscovery 导出（Bates 引用）——L42–44 明示两模式"converge on the same output structure"，差异只在 source profile 与 significance frame，无隐藏分叉。
- history.md 分离规则（L263–271）与 Load context（L58–77 仅读"Prior chronology.md"）一致：hold→history、breach notice→chronology 的示例判定清晰，不存在"既读又不读 history"的矛盾。
- `_log.yaml` 的契约语义（L73–77）：intake 写入、本 skill 读取——"Intake is what runs conflicts and writes the `_log.yaml` row this skill reads from" 是完整闭环；拒绝话术（L74–75）引用块完整可直接复述。

### 4.3 代码与条件

- 无伪代码、无未定义的代码实体；唯一的"代码"是输出模板围栏块（L177–241）与标记占位符。
- 条件分支全部给出明确行为：privilege_posture 三态（A/B/C，C 中止并重跑 L93）、模式选择（Role=solo/other → 默认 matter + 首轮双模式介绍 L46）、来源覆盖薄（四选项 L125）、特权判定三态（ok/flag/review L145–147）、显著性边界（borderline 降级 + `[SME VERIFY — borderline significance call]` L165）、SoF 是否含 🔒（`--include-flagged` L247）、增量 vs 首建（L253–261）。**无悬挂条件**。
- 结论断言克制：L273–278 四条 "does not" 全部是强否定 + 替代指引（"Resolution is counsel's call"、"it's not in the chronology — but Gaps might call it out as missing"），无半吊子承诺。

---

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用（位置） | 目标 | 类型 | 存在性 | 判定 |
|---|---|---|---|---|
| L8/58/61/65/67/73/95/129/175/180/247 等 7+ 处 | `~/.claude/plugins/config/claude-for-legal/litigation-legal/`（插件 CLAUDE.md 及其 `## Role`/`## Side`/`## Landscape`/`## Outputs`/`## Who's using this` 小节） | 外部插件配置 | **本机实测不可达**：`~/.claude/plugins/config/claude-for-legal/` 目录存在，但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**（见 5.2-#1） | 🔴 高依赖、无回退 |
| L73–77/95 | `.../matters/_log.yaml`（matter 登记） | 外部文件 | 不可验证（litigation-legal 不存在则无） | ⚠️ 冲突 gate 与 PROC-02 判定的实体依赖 |
| L8/65–67/175 | `.../matters/[slug]/matter.md`、`.../matters/[slug]/chronology.md` | 外部文件 | 不可验证 | ⚠️ 输入（theory/pivot fact）与输出路径依赖 |
| L201/234 | `[YYYY-MM-DD]` / `[VERIFY: ...]` 等占位符与标记 | 自含模板 | ✅ 内联 | ✅ |
| check.py L11 | `_shared/checker.py`（`sys.path.insert(0, "..", "_shared")`） | 共享库 | ✅ 存在，函数签名完全匹配（见 5.3） | ✅ |

### 5.2 不可见资源（风险清单）

1. **插件配置（7+ 处）+ `matters/` 三个文件实体**：**实测验证**——本机 `~/.claude/plugins/config/` 下存在 `claude-for-legal/` 与 `ai-governance-legal/` 两个目录，但 `claude-for-legal/` 内**仅有 `ai-governance-legal/` 子目录**，`litigation-legal/` 不存在（与 037 审查时的"整个 claude-for-legal 缺失"相比，本机已部分安装 AI 治理插件但未安装 litigation 插件）。故 `litigation-legal/CLAUDE.md`、`matters/_log.yaml`、`matters/[slug]/matter.md` 全部不可达。若评测沙箱未挂载该插件，则：`## Role` 模式默认值无来源（L39）、`## Side` 显著性框架无来源（L50）、conflicts gate 无实体（L73–77）、输出路径写不进去（L175）——**PROC-02/OUT-01 两条 criteria 直接不可达**。
2. **`_log.yaml`（3 处）**：冲突 gate 的实体。拒绝话术完整（L74–75），但"该文件存在"是 PROC-02 通过的前提；无插件环境下 agent 只能读到空/不存在的文件——此时按 skill 语义应拒绝执行（保守、合规），但评测任务将无法产出工作产品。
3. **`~` 用户主目录路径**：硬编码相对用户主目录的绝对路径，跨机器不可移植——与 017/018/028/034/036/037/040/077/127/139/144/160/170/185/200/212/258/279/304 等全部 claude-for-legal 系 skill 同款问题（家族级 P0，见 §13 P0）。

### 5.3 共享库验证

`D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py`（350 行）提供 `file_exists`、`output_contains`、`set_tool_log_path`、`set_agent_output` 等函数，与 check.py 的 import 和调用签名逐一匹配；`file_exists` 经 `_resolve_glob` 支持 `**` glob（`**/matters/**/chronology.md`），`output_contains` 的 MULTILINE 正则与 OUT-02（`(?i)(Matter:|Mode:|Privilege posture|Pivot fact|Entries:)`）和 OUT-03（`\| \d{4}-\d{2}-\d{2} \|`）兼容。check.py L24–29 的"路径 vs 原始文本"二分支逻辑与 main()（L61–63）的读文件逻辑有轻微重复（no-trigger 版 check.py 无此块，直接 `set_agent_output(agent_output)`），行为正确、无害。OUT-01 的 glob 语义与 skill 规定输出路径的匹配问题见 §10.3-#1 与 §13 P1。

### 5.4 嵌套与跨 Skill

无嵌套 skill；跨 skill 仅散文式命名与插件命令空间引用（`matter-intake` L75、Everlaw/Relativity/DISCO/Aurora L111/121 为外部服务名），无 `../other-skill/` 文件级引用——完全符合 SPEC §3.3 的禁止条款。

---

## 6. 语法与格式质量

| 检查项 | 结果 | 说明 |
|---|---|---|
| 拼写 | ✅ | 全文无拼写错误（抽查 279 行）；法律术语（implied undertaking / protective order / work product / common interest / joint defense / Kovel / Bates / pivot fact）拼写与大小写统一 |
| 术语一致性 | ✅ | `chronology` / `matter` / `production` / `pivot fact` / `significance` / `privilege posture` / `priv` 用法稳定；`--matter`/`--documents` 模式名前后一致（唯一词汇缝隙是 argument-hint 的 `--format=`，见 §4.1-#3） |
| Markdown 结构 | ✅ | 表格 1 处（输出模板时间线表 L199–201）、代码围栏 1 处（working 模板 L177–241）、引用块 5 处（A/B/C 特权姿态、冲突 gate 话术、disclosed-doc 确认话术等），语法全部合法 |
| 占位符 | ✅ | `[slug]` / `[YYYY-MM-DD]` / `[file paths or Bates]` / `[N]` / `[VERIFY: ...]` 等统一方括号风格，无残留未替换的真实数据 |
| 截断 | ✅ | 无中途截断迹象；L278 收尾完整（"Actual privilege determinations are counsel's call per `[SME VERIFY]` flags." 收束干脆） |
| 混杂 | ✅ | 全英文、无中英混杂、无乱码、无葡语残留 |
| 标点 | ⚠️ | em dash（—）**75 处 / 274 行**，密度 corpus 前列——作风格元素高度统一（description、标题、并列短语、括号说明），但高频出现使长句断句节奏单一；建议在关键判定处混用冒号/分号（§13 P7） |
| 小瑕疵 | ⚠️ | (1) L6/L21 双 H1；(2) L7–17 TL;DR 与正文重复且遗漏两道 gate（§4.1-#1）；(3) L9 "reference below" 指代含混；(4) `[SME VERIFY: privilege status]` 与 `[SME VERIFY — borderline significance call]` 两种分隔符（冒号 vs em dash）并存（L149/L165）——语义同族、格式微差 |

无 TODO/FIXME/lorem 文本、无被截断的半句。整体为 corpus 中语法质量最高梯队之一（与 dossier 评价"专业规范，法律术语使用准确"一致；L129 的标签纪律段与 L125 的四选项话术是全文语言质量峰值）。

---

## 7. 规范合规性（SKILL-SPEC.md 12 项清单）

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符，≤64，匹配目录 | ✅ | `chronology` 与目录 kebab 部分一致 |
| 2 | description：第三人称，WHAT+WHEN+KEYWORDS，≤1024 | ✅ | 376 字符，三问齐备，WHAT 带三步过程链 |
| 3 | description：无 imperative/第一/二人称开头 | ✅ | 动词开头描述 WHAT（同 SPEC §2.6 Good 示例句式），无 "Use this skill to"、无 I/you/we |
| 4 | description：无跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 结构 |
| 5 | description：≥1 触发信号 | ✅ | "Use when the user asks to..." **字面命中**标准信号，无 037/034 的带注问题 |
| 6 | frontmatter：无允许列表外键 | ✅ | 仅 name/description/argument-hint |
| 7 | body ≤600 行 | ✅ | 274 行 |
| 8 | body 有 workflow/process 节 | ✅ | `## Workflow` Step 0–6，全程门控 |
| 9 | body 有 output format 节 | ✅ | `## Output formats` 独立成节，三变体 + 完整模板（corpus 最完备之一） |
| 10 | body 有 scope/limitations 节 | ✅ | `## What this skill does not do` 4 条 + 4 处功能式边界 |
| 11 | body 无跨 skill 文件引用 | ✅ | 无 `../` 引用；插件路径属外部配置契约（§5.2） |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✅ | `067-chronology` |

**结果：12/12 通过，且全部为无注通过**（对比 037 的 #5 带注）。合规性与 034/037 并列 corpus 顶尖水平——三必需节齐全、质量高，描述合规无瑕疵。

---

## 8. 人机感评估

| 维度 | 结果 | 说明 |
|---|---|---|
| Emoji | ✅ 46 处全部功能性 | 🔴14 / 🟡13 / ⚪9 / 🔒9 / ⚠️1——显著性标签、特权旗标、disclosed-doc 警告均为流程数据与模板词汇，零装饰性使用（dossier"🔴🟡⚪🔒 为功能性标记"复核成立） |
| 全大写 | ✅ 零语气性使用 | 无 "STOP!"/"DO NOT" 喊话式指令（对比 072 的教训）；全大写仅出现在标记体系（`VERIFY`/`UNCERTAIN`/`CITE NEEDED`）与模板字段（`[WORK-PRODUCT HEADER...]`），属数据而非语气 |
| 语气 | ✅ 律师助理角色、克制专业 | "Facts happen in order. The chronology is the spine every narrative hangs on"（L35）——有专业人格但不说教；"A chronology of 300 entries with 300 🔴 tags has no tags"（L163）克制的警告方式；无填充语 |
| 人机边界 | ✅ corpus 最清晰之一 | 五处"律师决定"声明：privilege posture 由用户选（L85–93）、privilege 判定归 counsel（L278）、矛盾裁决归 counsel（L275）、低置信来源由律师接受（L125）、显著性边界降级待复核（L165）；SoF 特权过滤的 `--include-flagged` 显式确认（L247）将"默认安全 + 显式解除"原则落地 |
| 人称 | ✅ | description 与 body 均第三人称；L87–93/L125/L176 引用块是 agent 对用户的交互话术（属模板内容而非 agent 语气），用法恰当 |
| 表格密度 | ⚠️ 低 | 1 张表 / 274 行——时间线模板表是决策树化的正确用例；Step 1 的来源优先级（L101–106）、Step 3 的事件类型（L135–139）、特权三态（L145–147）均为"列表式可执行"，本可表格式呈现，但列表已足够清晰，非缺陷 |
| 场景温度 | ✅ | 特权 waive 风险（L83）、失特权单向门（L149）、disclosed 文档 contempt 风险（L27）均以专业风险语言处理，无恐吓腔；"Prefer the recoverable error"（L149）是成熟的风险权衡表述 |

评价：律师助理式克制、边界感强、门控设计有温度（A/B/C 姿态让用户在提取前做出可记录的决定）。dossier 的"律师助理角色语气克制专业"评价在复核中成立。六重护栏 + 五处交互话术的密度在 322 个 skill 中仅次于 037。

---

## 9. 可执行性评估

**独立可执行性评分：7.0 / 10**（分环境差异极大，见下）

| 子项 | 得分 | 说明 |
|---|---|---|
| 步骤操作性 | 9.5/10 | Step 0–6 每步都有具体指令与话术模板：A/B/C 姿态选项、来源四序、四选项升级话术、三态特权规则（默认 flag）、去重规则（一事件多来源）、显著性纪律（若迟疑 🟡）、输出三变体。agent 几乎不需要自行推断行为 |
| 交付物明确性 | 9.5/10 | 交付物 = `matters/[slug]/chronology.md` + 变体；模板 8 字段头部（Matter/Mode/Built/Sources/Entries/Pivot fact/Privilege posture/Flagged）+ Timeline 表 + Key events + Gaps + Marker discipline + Version 全部预定义——corpus 中最精确的输出契约之一 |
| 工具依赖 | 3.5/10 | 关键路径依赖插件配置（7+ 处，含 `## Role`/`## Side`/`## Outputs` 小节）+ `matters/` 三文件实体；`~` 绝对路径在沙箱大概率不可解析（本机实测 litigation-legal 子目录即不存在） |
| 独立运行（无插件环境） | 6.0/10 | Load context 失败 → 模式默认值与显著性框架无来源（agent 只能询问或推断）；冲突 gate 读不到 `_log.yaml` → 按语义应拒绝（合规但评测零产出）；特权 gate A/B/C 自足可执行（话术在 body 内）；输出模板完整可复制 |
| 独立运行（插件环境） | 9.5/10 | 按设计用途（claude-for-legal 插件已安装）运行时近乎满分：模式选择、matter.md 读取、冲突 gate、特权门控、增量构建全链路可执行 |

结论：skill 自身的可执行性设计是 corpus 顶尖（步骤 9.5 / 交付物 9.5），瓶颈完全在外部依赖契约——与 037 同构（家族级问题）。修复 P0（含 fixture 方案）后独立可执行性可升至 8.5–9/10；OUT-01 的路径/glob 匹配需评测侧验证（§13 P1）。

---

## 10. SCORING.yaml 交叉参考

### 10.1 23 条 criteria 溯源

| ID | 类别 | 检查点摘要 | Body 对应位置 | 判定方式 | 一致性 |
|---|---|---|---|---|---|
| SCOPE-01 | scope | 识别为 chronology 构建任务而非文档摘要 | Purpose（L33–35）、Step 3（L131–149） | llm | ✅ 任务框架明确 |
| SCOPE-02 | scope | 按角色选模式或双模式让用户挑 | Modes（L37–46） | llm | ✅ solo/other 分支与 criterion 逐字对应 |
| SCOPE-03 | scope | 不发明来源中不存在的事件 | What it does not do #2（L276）、Gaps（L216–227） | llm | ✅ "not in the chronology — but Gaps might call it out" |
| SCOPE-04 | scope | 不裁决文档间矛盾，双方条目带旗标 | What it does not do #1（L275） | llm | ✅ "Resolution is counsel's call" |
| PROC-01 | process | Step 0 特权 gate 先于提取（A/B/C） | Step 0（L81–97） | llm | ✅ "The skill will not extract until the user picks a privilege posture"（L85） |
| PROC-02 | process | 冲突 gate：未 intake 拒绝并路由 matter-intake | Load context（L73–77） | llm | ✅ 拒绝话术完整引用块 |
| PROC-03 | process | 姿态记录于头部（privilege_posture 字段） | L95 + 模板 L192 | llm | ✅ 模板字段 `**Privilege posture:**` 预置 |
| PROC-04 | process | B 姿态下三态 priv 旗标 + SME VERIFY，不确定默认 flag | Step 3（L143–149） | llm | ✅ 三态规则 + "Default for anything uncertain" |
| PROC-05 | process | 来源按声明顺序识别，薄则询问 | Step 1（L101–106） | llm | ✅ 四序 + 询问话术 |
| PROC-06 | process | 不可达来源显式列入 Gaps（不静默跳过） | Step 2（L123） | llm | ✅ "name it explicitly in the output's Gaps section" |
| PROC-07 | process | 覆盖薄时不静默补充，提供选项 | Step 2（L125） | llm | ✅ 四选项话术逐字对应 |
| PROC-08 | process | 每条目来源标注（路径/Bates/连接器/内联标签） | Step 2（L127） | llm | ✅ 含三标签清单 |
| PROC-09 | process | 法律结论（时效/期限/特权判定）带来源标签 | Step 2（L129） | llm | ✅ 本 skill 标志性规则——"tagging reaches every section that states a legal conclusion" |
| PROC-10 | process | 去重：同事件多来源合并为一条 | Step 4（L151–153） | llm | ✅ "one event with four sources" 逐字对应 |
| PROC-11 | process | 显著性纪律：非全 🔴，边界降级 + SME VERIFY | Step 5（L155–165） | llm | ✅ "300 entries with 300 🔴 tags has no tags" |
| OUT-01 | output | chronology.md 写入 matters/[slug] 路径 | Step 6（L175） | script | ✅ glob 语义见 10.3-#1 |
| OUT-02 | output | 头部含 Matter/Mode/Built/Sources/Entries/Pivot fact/Privilege posture | 模板 L184–192 | script | ✅ 五字段正则全部预置 |
| OUT-03 | output | Timeline 表含至少一条真实日期条目 | 模板 L199–201 | script | ✅ 模板占位符陷阱见 10.3-#2 |
| OUT-04 | output | Gaps 节覆盖三类（空窗/应有缺失/不可读来源） | 模板 L216–227 | llm | ✅ 三子节与 criterion 逐字对应 |
| OUT-05 | output | 有先前版本则递增 v[N+1] 并给 diff 摘要 | Incremental builds（L253–261） | llm | ✅ 新增/修改/移除三类 diff 定义明确 |
| NEG-01 | negative | 未跑特权 gate 前不提取 | Step 0（L85） | llm | ✅ "will not extract until..." 硬性语义 |
| NEG-02 | negative | 不剥离/不折叠 verify 来源标签 | Step 2（L127"Never strip or collapse the tags"） | llm | ✅ 字面对应 |
| QA-01 | qa | 定稿前请用户复核 🔴 条目（"anything I miscalled?"） | TL;DR L17 + 输出说明 L176 | llm | ✅ 话术逐字对应 |

### 10.2 critical_failures

| ID | 触发条件 | Body 对应 | 判定 |
|---|---|---|---|
| CF-01 | 发明来源中不存在的事件 | What it does not do #2（L276） | ✅ 合理 cap_to_0——与 SCOPE-03 的行为要求互补而非冗余（行为要求 vs 后果封顶） |
| CF-02 | 未经特权 gate 即提取（无姿态记录） | Step 0（L85） | ✅ 合理 cap_to_0——"will not extract until" 的否定形态 |
| CF-03 | `--matter` 模式为未 intake matter 构建（绕过冲突 gate） | Load context（L73–77） | ✅ 合理 cap_to_0——"unbypassable" 表述与 CF 语义一致 |

### 10.3 发现的缝隙

1. **OUT-01 路径语义与 glob 的匹配风险（条件性）**：skill 规定输出为 `~/.claude/plugins/config/claude-for-legal/litigation-legal/matters/[slug]/chronology.md`（绝对路径、home 之外的位置），check.py 实现为 `file_exists(os.path.join(workspace, "**/matters/**/chronology.md"))`（workspace 相对 glob）。若评测沙箱的 workspace ≠ home、或 glob 默认排除 `.claude` 等点目录，则 agent 按 skill 字面写入的合规输出**找不到**，OUT-01 误判失败。这是 037 未暴露的 067 特有缝隙（037 的 PROC-01 是工具日志检查，无路径 glob）。需在 fixture 方案中验证（§13 P1）。
2. **OUT-03 模板占位符陷阱**：模板时间线表的日期列是 `[YYYY-MM-DD]`（L201），**不匹配**正则 `\| \d{4}-\d{2}-\d{2} \|`——若 agent 逐字复制模板不改日期，OUT-03 自检失败。设计上正确（要求真实数据），但 SCORING 描述"at least one dated entry"未提示 agent 必须替换占位符；风险低（正常 agent 必填真实日期），可接受。
3. **PROC-03 可脚本化未脚本化**：`Privilege posture` 头部字段可用 `output_contains("Privilege posture")` 直接脚本化（同 OUT-02 的机制），当前留作 llm judge——非错误，属效率性优化（§13 P4）。
4. **NEG-02 语义**：criterion 是"不剥离"的否定语义，llm judge 判定——无脚本近似（对比 037 的 NEG-02 用存在性检查近似）。llm judge 对"剥离"行为的判定依赖评委对 agent 全程轨迹的观察，语义精确性更高但成本更高；可接受。
5. 23 条 criteria 与 3 条 CF 无冗余、无遗漏；categories 占比（scope 4 / process 11 / output 5 / negative 2 / qa 1）与 process 模式匹配；`total_items: 23` 计数正确（4+11+5+2+1）。check.py 仅实现 OUT-01/02/03 三个 script 检查，其余 20 条为 llm judge——与 SCORING.yaml 标注一致，无错配。

---

## 11. 已知问题汇总（skill-dossier.md 引用）

Dossier 条目（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` L539–544）：

> - **逻辑**: 特权门槛→来源识别→提取→去重→显著性标注→输出的全链条严谨自洽，模式差异、增量构建、边界声明相互印证。
> - **语法**: 专业规范，法律术语使用准确。
> - **人机感**: 律师助理角色语气克制专业，🔴🟡⚪🔒 为功能性标记。
> - **合规**: Description 第三人称，Workflow/Output 格式/质量检查完整，正文 279 行 ≤600。
> - **总评**: 🟢 结构设计堪称范本。

对照评估：

| dossier 论断 | 本次审查 | 一致性 |
|---|---|---|
| 全链条严谨自洽（特权门槛→来源→提取→去重→标注→输出） | 六步链条复核成立 ✅；本审查补充新发现：TL;DR 遗漏两道 gate、argument-hint 与正文 flag 词汇不一致、双 H1、OUT-01 glob 缝隙 | 基本一致，本审查更细 |
| 模式差异/增量构建/边界声明相互印证 | ✅ 确认（§4.2：`--matter`/`--documents` 汇聚结构、history.md 分离规则、增量 diff 三类） | 一致 |
| 专业规范，法律术语准确 | ✅ 确认（§6：CPR 31.22 / Rule 26(c) / Kovel / common-interest 均准确） | 一致 |
| 律师助理角色克制专业，🔴🟡⚪🔒 功能性 | ✅ 确认（§8：46 处 emoji 全部功能性） | 一致 |
| 🟢 完全合规 | ✅ 12/12 全部无注通过（§7） | 一致 |
| 正文 279 行 | 实测文件总计 279 行 / 正文 274 行——dossier 计全文件行数，无实质分歧 | 无实质分歧 |
| 总评 🟢 结构设计堪称范本 | 本审查给 🟢 A−（88/100，§12）——与 037（A− 89/100）同为家族顶尖区间；扣分集中在外部依赖契约（本机实测 litigation-legal 子目录不存在）与 TL;DR/词汇缝隙，均不推翻"范本级"定位 | 方向一致 |

旧 REVIEW.md stub（4 行）给出的结论：

> **2026-08-05** | Claude | Dossier: 🟢 典范
> Dossier: "范式级结构设计"、"律师助理角色语气克制专业"。279 行。硬编码路径可能需验证。
> **综合**: 🟢 **A** (60/100)

逐项核对：
1. **🟢 A 评级**：与本审查同区间（本审查 A− 88/100）。stub 的 60/100 为旧版标尺（037 等新标尺为 85–89/100 对应 A−），与旧标尺的 A 档（55–65）对应，无实质矛盾。
2. **"硬编码路径可能需验证"——本次完成验证**：`~/.claude/plugins/config/claude-for-legal/` 目录**存在**但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**（与 037 审查时"claude-for-legal 整体缺失"的机器状态不同，但结论相同：skill 引用的插件路径不可达）。stub 的谨慎措辞是准确的。
3. **"范式级结构设计"**：复核成立——六步门控工作流、三态特权规则、三变体输出模板、标签纪律覆盖法律结论（L129）均为 corpus 领先设计；本审查额外发现 4 处 dossier 未记录的小问题（§4.1），不影响总评方向。

---

## 12. 综合评分（8 维度加权）

| 维度 | 权重 | 得分 | 依据 |
|---|---|---|---|
| 逻辑一致性 | 15% | 9.5 | 六步链条 + 双 gate + 三态特权 + 增量构建全自洽、法条引用准确、无悬挂条件；扣分：TL;DR 遗漏两道 gate、argument-hint/正文 flag 词汇不一致 |
| 参考文件与资源 | 15% | 6.5 | 零悬空内部引用、纯内联结构；扣分：外部插件契约 7+ 处无回退，本机实测 litigation-legal 子目录不存在 |
| 语法与格式 | 10% | 9.5 | 全净、法律术语准确；仅双 H1、em dash 高频、TL;DR 冗余为微瑕 |
| 规范合规性 | 20% | 9.5 | 12/12 全部无注通过；argument-hint 词汇缝隙扣 0.5 |
| 人机感 | 10% | 9.5 | 46 处 emoji 全功能性、律师助理克制语气、五处"律师决定"边界、门控交互有温度 |
| 可执行性 | 10% | 7.0 | 步骤/交付物各 9.5，但关键路径外部依赖无回退、OUT-01 路径/glob 匹配待验证 |
| SCORING 对齐 | 10% | 9.0 | 23+3 全部可溯源；OUT-01 glob 缝隙与 OUT-03 占位符陷阱各扣 0.5 |
| 法律适切性 | 10% | 9.5 | CPR 31.22 隐含承诺、三态特权单向门论证、冲突 gate、waiver 分析、SoF 特权过滤——corpus 最强法律护栏群之一 |

**加权总分 = 1.425 + 0.975 + 0.950 + 1.900 + 0.950 + 0.700 + 0.900 + 0.950 = 8.75 ≈ 8.8 / 10**

### 总评：🟢 A−（88/100）

法律类 process skill 的范本级作品，与 037-brief-section-drafter 并列为 claude-for-legal 家族双标杆。合规 12/12 全部无注通过、六重护栏零矛盾、输出契约 corpus 最完备（独立 Output formats 节 + 完整模板）、L129 的"标签纪律覆盖法律结论"是全语料库罕见的精细设计；扣分集中在**外部依赖契约**（7+ 处硬编码插件路径无回退，本机实测 `litigation-legal/` 子目录不存在——与 037 同款家族级 P0）与 **OUT-01 路径/glob 匹配缝隙**（067 特有的评测暴露面）。修复 §13 的 P0–P1 后可达 9.4（🟢 A）。

---

## 13. 修复建议（按优先级分层）★重点★

### 🔴 P0 — 致命（条件性）：外部插件契约无回退（7+ 处硬编码路径）

**问题**：`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 被 7+ 处引用（L8/58/65/67/73/95/129/175/180/247 等），承担六类内容：插件 CLAUDE.md 的 `## Role`（模式默认值 L39）、`## Side`（显著性框架 L50）、`## Landscape`（文档来源 L61）、`## Outputs`（工作产品头与 reviewer note 约定 L129/178）、`## Decision posture`（特权旗标规则 L62）、`## Who's using this`（角色判定 L41/179）；`matters/[slug]/matter.md`（theory/pivot fact，显著性标注输入 L8/65）；`matters/_log.yaml`（冲突 gate 实体 L73–77）；`matters/[slug]/chronology.md`（输出路径 L175）。**全 skill 没有一处 fallback**。本机实测：`~/.claude/plugins/config/claude-for-legal/` **存在**但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**；`D:\SkillIF\skill-experiment\` 全树亦无 fixture 生成逻辑。若评测沙箱未挂载该插件（`~` 相对绝对路径在隔离工作区大概率不可解析），则：模式默认值无来源（agent 只能询问）、显著性框架无来源、冲突 gate 与 PROC-02 失去实体、输出路径写不进去（OUT-01 不可达）——三条 criteria 直接不可达，且 agent 的合规行为（拒绝）将导致评测任务零产出。这是全 skill 唯一没有兜底的关键路径。

**修复**（工作量 ~45–60 分钟，分两部分）：

**方案 A — Skill 侧回退分支**（推荐，~30 分钟）：
1. `## Load context`（L58–77）加条件分支："If the plugin configuration at `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` exists, load it and follow its `## Role`, `## Side`, and document-source declarations. If it does not exist (no firm config mounted), proceed with the session's stated role and side, note at the top of the chronology header: 'Firm config not loaded — mode/framing defaults per this skill applied.'"——把模式默认与显著性框架的默认值从插件引用改为本文显式列出（消除循环依赖）。
2. 为 Modes 节（L39）追加回退："if `## Role` is absent, default to `--matter` and mention both modes on the first run"（与 solo/other 分支同逻辑，消除 §13 P5 的缝隙）。
3. 为冲突 gate（L73–77）追加回退："if `_log.yaml` does not exist, treat the matter as unintaken — the refusal message above still applies"（拒绝话术已存在，缺的只是"文件不存在时也走同一分支"的明确性）。
4. 为输出路径（L175）追加回退："if the plugin matters directory is unreachable, write to `./matters/[slug]/chronology.md` in the workspace and note the relocation in the header"——这一步同时缓解 §13 P1 的 OUT-01 glob 缝隙。

**方案 B — 评测侧 fixture**（条件性，与 A 互补，~15 分钟）：在 SkillIF 评测工作区为每个 claude-for-legal 系 skill（017/018/028/034/036/037/040/067/077/127/139/144/160/170/185/200/212/258/279/304 等，凡引用该插件路径者）提供最小 fixture：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`（含 `## Role: in-house litigation counsel`、`## Side: plaintiff`、`## Landscape` 文档来源表、`## Outputs` 工作产品约定）+ `matters/_log.yaml`（含一个已 intake 的示例 matter slug，如 `acme-v-us-2026`）+ 该 matter 的 `matter.md`（含 theory/pivot fact/key facts 示例）+ 1–2 个源文档（供提取）。可脚本化生成（复用 `create_no_trigger_set.py` 的 corpus 遍历模式）。这同时解决全部 20+ 个同家族 skill 的同一问题，而非逐个补丁。

### 🟡 P1 — 重要：OUT-01 输出路径与评测 glob 的匹配缝隙（条件性）

**问题**：skill 规定输出为 `~/.claude/plugins/config/claude-for-legal/litigation-legal/matters/[slug]/chronology.md`（home 绝对路径），check.py 实现为 `file_exists(os.path.join(workspace, "**/matters/**/chronology.md"))`（workspace 相对 glob）。两个风险点：(1) 若评测 workspace ≠ home，agent 的合规写入位于 workspace 之外，glob 无法命中——OUT-01 误判失败；(2) 即使 workspace = home，glob 的 `**` 默认不匹配 `.claude` 等点目录（`_resolve_glob` 行为需实测确认），同样无法命中。这是 037 未暴露的 067 特有缝隙（037 的脚本检查基于工具日志，无路径 glob），必须在评测前实测。

**修复**（工作量 ~20 分钟）：
1. 实测 `_shared/checker.py` 的 `_resolve_glob` 对点目录与 home 路径的行为（写一个最小验证：在 home 下写 `.claude/plugins/config/.../matters/x/chronology.md`，跑 `file_exists("**/matters/**/chronology.md")` 看是否命中）。
2. 若不可命中：优先采用 §13 P0 方案 A 第 4 条（skill 侧回退写到 workspace 内 `./matters/[slug]/`），或方案 B 将 fixture 的 `matters/` 目录直接挂在 workspace 下，使 agent 的合规输出落在 glob 可命中范围内。
3. 同步验证 OUT-02/OUT-03 的 `output_contains` 对模板逐字复制与真实填写两种输出都按预期判定（§10.3-#2 的占位符陷阱）。

### 🟡 P2 — 重要：双 H1 + 10 步 TL;DR 冗余，且 TL;DR 遗漏两道 gate

**问题**：SKILL.md 顶部保留着插件家族模板的公共残片——`# Chronology` H1 出现两次（L6/L21），L7–17 的 10 步 TL;DR 与正文各节逐一重复（1↔Load context、2↔Load context、3↔全篇、4↔Step 1、5↔Step 2、6↔Step 4、7↔Step 5、8↔Step 6、9↔Incremental builds、10↔QA-01），**但全 skill 最重要的两道 gate（冲突 gate L73–77、特权 gate L81–97）在 TL;DR 中完全缺席**——快速阅读者会误以为时间线构建无前置审批门槛；且 TL;DR 编号（10 步）与 Workflow 编号（Step 0–6 共 7 步）不一致，心智映射有额外开销。与 034-client-intake（L6/L20 双 H1）、037-brief-section-drafter（L6/L15 双 H1 + TL;DR）同源同款，属该插件家族模板的公共缺陷。

**修复**（工作量 ~15 分钟）：删除 L6 的第一个 H1（保留 L21 起正文）并清理 L19 的残片分隔线；TL;DR 若保留，改写为与正文节一一对应的交叉引用表格（比编号列表防漂移），**并在表格上方加一行醒目注记：'⚠️ Two gates run before extraction: the conflicts gate (§ Load context) and the privilege gate (§ Workflow Step 0).'**——把 gate 从"正文才见"提升为"总览即见"，同时消除双 H1。

### 🟡 P3 — 重要：argument-hint 与正文 flag 词汇不一致

**问题**：frontmatter 的 `argument-hint` 定义 `--format=working|sof|witness-[name]` 三个 flag 值，但正文从未定义 `--format` 的语法——L15 仅出现 "format variant per flag"、L169 仅说 "Variants on request"，agent 收到 hint 后无法在正文找到 `--format=sof`/`--format=witness-[name]` 的展开说明（只能从输出格式节的三变体标题推断）。反向亦然：正文的模式 flag `--matter`/`--documents`（L39/41）未进入 hint。单一词汇表原则被破坏，且 hint 与正文两套 flag 名并存会稀释 agent 对参数系统的确定性。

**修复**（二选一，工作量 ~10 分钟）：
- 方案 A：在 `## Output formats` 节（L171）开头加一段显式参数契约："Invocation flags: `--matter` / `--documents` select the mode (default per `## Role`); `--format=working|sof|witness-[name]` selects the output variant (default `working`). Variants are also available on request."——hint 与正文由此对齐。
- 方案 B：简化 hint 为 `[slug] [--mode=matter|documents] [--format=working|sof|witness-[name]]`，把模式 flag 补进 hint 并在正文补同款参数契约段。
推荐方案 A（正文为契约主体，hint 是索引；补正文比扩 hint 更防漂移）。注意触发版与 no-trigger 对照版共享同一 frontmatter 规则——若改 hint，两版需同步（对照版只删 description 的 WHEN 句，hint 不受影响，天然同步）。

### 🟡 P4 — 重要：privilege_posture 与标签纪律可脚本化未脚本化（SCORING 优化）

**问题**：check.py 仅实现 OUT-01/02/03 三个 script 检查，其余 20 条为 llm judge。其中 PROC-03（姿态记录于头部）可用 `output_contains("(?i)Privilege posture|A-cleared|B-mixed")` 直接脚本化（与 OUT-02 同机制）；NEG-02（不剥离来源标签）可用存在性近似 `output_contains("\[web search — verify\]|\[model knowledge — verify\]|\[user provided\]")`（同 037 的 NEG-02 方案）——两者均零成本、可减少 llm judge 负担并提升判定稳定性。非错误，属效率性优化。

**修复**（工作量 ~15 分钟）：在 SCORING.yaml 将 PROC-03 的 `judge` 改为 `script`（`fn: output_contains`，pattern `(?i)Privilege posture|A-cleared|B-mixed`），NEG-02 增加一条 script 近似检查（保留 llm judge 作主判定或作为双通道）；同步更新 check.py 与 SCORING.yaml 的 `total_items` 计数（不增删 criteria 则计数不变，只改判定方式）。**注意**：判定方式变更需与 2 Mode × 5 Harness 矩阵的评分聚合逻辑兼容，改动前确认 runner 对 `judge: script` 的依赖。

### 🟢 P5 — 优化：`## Role` 缺失时的回退行为未定义

**问题**：Modes 节（L39）说 "Pick a default from the user's `## Role` in the plugin's configuration CLAUDE.md"——但若该小节缺失（无插件环境、或插件配置简版），回退行为未定义；L46 只覆盖了 "`## Role` is `solo` or `other`" 的值分支，未覆盖"小节整体缺失"分支。`## Side`（L50）同理。这使无插件环境下的模式/框架选择成为 agent 自由裁量，与 P0 的回退方案直接相关。

**修复**（工作量 ~5 分钟）：在 L39 补一句 "If the config has no `## Role` section, default to `--matter` and mention both modes on the first run"；在 L50 补 "If `## Side` is absent, ask the user per-chronology which side's framing to apply"（与 Both/varies 分支同逻辑）。两处各一行，消除全部未定义分支。

### 🟢 P6 — 优化：标记/标签词汇表集中化 + 体量预留

**问题**：正文实际存在三族标记：(1) 来源标签 `[web search — verify]` / `[model knowledge — verify]` / `[user provided]`（L127）；(2) 结论标签 `[computed from: ...]` 等（L129）；(3) marker discipline `[VERIFY: ...]` / `[UNCERTAIN: ...]` / `[CITE NEEDED: ...]` / `[SME VERIFY: ...]`（模板 L229–234）——但定义散落于 Step 2（L127/129）、Step 3（L149）、Step 5（L165）、输出模板 Marker discipline（L229–234）四处，无一处集中定义全部标记的语义与适用域；且 `[SME VERIFY: privilege status]` 与 `[SME VERIFY — borderline significance call]` 两种分隔符（冒号 vs em dash）并存。另：正文 274 行已超出 process 目标带（~200）约 35%，继续扩展有逼近 600 硬上限的趋势。

**修复**（工作量 ~15 分钟）：在 `## Output formats` 节之前新增一节 `## Marker glossary`（或并入现有 Marker discipline 概念），以表格集中列出三族标记的语义/适用域/示例——正文各处的使用点改为引用该表，消除散落定义；顺手统一 `[SME VERIFY: ...]` 的分隔符；若此后 body 超过 ~350 行，将输出模板整体下沉至 `references/output-template.md`（引用路径相对本目录，符合 SPEC §3.3），为将来扩展留余量。

### 🟢 P7 — 优化：em dash 高频的节奏调整（纯风格）

**问题**：em dash（—）75 处 / 274 行，密度 corpus 前列（对比：037 约 30 处/185 行）。风格高度统一是优点，但高频使用使长句断句节奏单一——尤其 L35/L125/L129 等长段，连续 3–4 个 em dash 并列让扫描性下降。

**修复**（工作量 ~10 分钟）：保留 description 与标记体系中的 em dash（功能性），对正文长段中的并列类 em dash 约 1/3 改为冒号（引出解释）或分号（并列分句），以 L125/L129/L263 三处最长段为试点。纯风格项，不影响合规与逻辑；不改动模板内嵌文案（模板是输出契约，与正文散文不同）。

### 修复工作量汇总

| 优先级 | 项数 | 工作量 | 修复后预期 |
|---|---|---|---|
| 🔴 P0 | 1（含 A/B 两方案） | ~45–60 分钟 | 可执行性 7.0 → 8.5+；PROC-02/OUT-01 可达 |
| 🟡 P1–P4 | 4 | ~60–90 分钟 | 评测缝隙消除、SCORING 判定更稳、词汇统一；合规仍 12/12 |
| 🟢 P5–P7 | 3 | ~30 分钟 | 细节无瑕、体量预留、风格优化，达 🟢 A（9.4/10） |
| **合计** | **8** | **约 2.5–3 小时** | 推荐全部执行；P0 必须（对 20+ 个同家族 skill 可规模化复用，建议与 037 的 P0 方案合并执行） |

---

## 附录: 审查过程记录

- **审查日期**: 2026-08-06。
- **被替换文件**: 旧 `REVIEW.md`（stub），原文：

```
# REVIEW: 067-chronology

**2026-08-05** | Claude | Dossier: 🟢 典范

Dossier: "范式级结构设计"、"律师助理角色语气克制专业"。279 行。硬编码路径可能需验证。

**综合**: 🟢 **A** (60/100)
```

- **过程时间线**:
  1. `Glob D:\SkillIF\skill-experiment\complex-skills\067-chronology\**` → 得 4 文件清单；`Glob` 定位 SKILL-SPEC.md（`complex-skills\_shared\` 与 `complex-skills-no-trigger\_shared\` 两处，取前者）与 skill-dossier.md；
  2. `Read` SKILL.md（279 行，全文）→ SCORING.yaml（207 行）→ check.py（73 行）→ 旧 REVIEW.md（stub）；
  3. `Read` SKILL-SPEC.md（162 行）→ 逐项比对 12 项合规清单；
  4. `Read` skill-dossier.md（全文）→ 定位 067 条目（L539–544）+ 037 条目（L325–330，家族对比基准）+ 汇总统计；
  5. `Read` 037-brief-section-drafter/REVIEW.md（450 行）——同域同款 13 节模板的完整样例，作为本审查的结构基准；`grep` 035/057/060 的 REVIEW.md 节标题确认 13 节模板在 corpus 中一致；
  6. `diff` 触发版 vs no-trigger 版 SKILL.md / SCORING.yaml / check.py → SCORING 逐字节相同、description 仅 WHEN 句差异（保留 WHAT 句约 173 字符）、check.py 仅 `is_path` 防御块差异；
  7. `Read _shared\checker.py`（350 行）验证 check.py 的 import 与函数签名匹配、`_resolve_glob`/`output_contains` 与 OUT-01/02/03 正则兼容性；
  8. `Bash ls ~/.claude/plugins/config/...` → **实测** `claude-for-legal/` 存在但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**（与 037 审查时的机器状态不同但结论相同）；
  9. `Python` 计算 metrics：description 376 字符、body 274 行、em dash 75 处、emoji 46 处（🔴14/🟡13/⚪9/🔒9/⚠️1）、H2 10 个/H3 10 个、表格 1 处、围栏 1 处、插件路径引用 7+ 处、`_log.yaml` 3 处、`matter.md` 6 处、`history.md` 6 处、`[SME VERIFY` 5 处、`priv:` 5 处；
  10. 交叉核对：SCORING 23+3 条 ↔ Body 行号 ↔ check.py 实现；dossier/旧 stub 结论 ↔ 本次审查结论；
  11. 写作本 REVIEW.md（替换旧 stub）。
- **验证记录**: description 长度 376 字符（≤1024 ✅）；Body 行数 274（≤600 ✅）；目录共 4 文件、无 references/scripts/；no-trigger 对照版存在于 `complex-skills-no-trigger\067-chronology\`；`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 实测不存在（父目录存在但子目录缺失）；SCORING `total_items: 23` 与分类求和一致（4+11+5+2+1）。
- **方法论备注**: 本审查独立于 dossier 结论重新走查全部文件；dossier 的 🟢 范本级评价在复核中成立（合规 12/12 全部无注通过、输出契约 corpus 最完备、L129 标签纪律为标志性设计），但本次新发现 5 处 dossier 未记录的问题（TL;DR 遗漏两道 gate、argument-hint/正文 flag 词汇不一致、双 H1、OUT-01 路径/glob 缝隙、`## Role`/`## Side` 缺失分支未定义），并**实测确认了 stub 所称硬编码路径的不可达性**（证据与 037 审查时的机器状态不同：claude-for-legal 父目录已部分安装、litigation-legal 子目录缺失）。故维持 🟢 A− 评级（88/100）——与 037（A− 89/100）同区间，突出该家族共性 P0（外部插件契约无回退）；P0–P1 修复完成后评级可上调至 🟢 A。
