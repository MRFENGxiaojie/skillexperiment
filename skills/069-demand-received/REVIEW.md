# REVIEW: 069-demand-received

**审查日期**: 2026-08-06 | **审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — 入站索赔函分诊（inbound demand letter triage：字段提取 → 组合交叉核对 → 价值评估 → 响应选项 → 期限分类 → 撰写 triage → 交接，7 步闭环）
**Body 行数**: 230 行（frontmatter L1–4，body L6–235；文件总计 235 行）
**参考文件数**: references/0, scripts/0, assets/0 — 全内容内联；外部插件契约 9 处（`~/.claude/plugins/config/claude-for-legal/litigation-legal/`，本机实测不可达）
**总文件数**: 4（SKILL.md, SCORING.yaml, check.py, REVIEW.md）
**已有 REVIEW**: 旧版 4 行 stub（2026-08-05，Dossier 🟢，综合 A− 55/100），本次替换为全面深度审查

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\069-demand-received\
├── SKILL.md        (235 行, 13,825 bytes)
├── SCORING.yaml    (168 行,  8,429 bytes)
├── check.py        ( 73 行,  2,305 bytes)
└── REVIEW.md       (  4 行 — 旧版 stub，本次全文覆写)
```

要点：

- **极简 4 文件结构，无任何子目录**（references/、scripts/、assets/、templates/ 均不存在），与 028/067 同款"全量内联"设计——SKILL.md 自含全部内容（含完整的输出模板），零内部文件依赖，无悬空引用。
- **无触发对照集存在**：`complex-skills-no-trigger\069-demand-received\`（同一 corpus 对照组）含 SKILL.md / SCORING.yaml / check.py。`diff` 实测：**SCORING.yaml 与触发版逐字节相同**；SKILL.md 仅 description 差异（对照版删去全部 WHEN 触发句，仅保留 WHAT 句，约 205 字符）；check.py 差异仅为触发版多一段 `is_path` 防御分支（L22–29）。与 2 Mode × 5 Harness 测评矩阵设计一致。
- **旧 REVIEW.md 为 4 行 stub**（内容见附录），已被本文替换。
- 唯一外部路径依赖：`~/.claude/plugins/config/claude-for-legal/litigation-legal/`（9 处引用）——与 017/018/028/034/036/037/040/067/077 等全部 claude-for-legal 系 skill 同款插件配置契约。**本机实测 `litigation-legal/` 子目录不存在**（详见 §5.2、§13 P0-1）。

---

## 2. Frontmatter 逐字段审查

### 2.1 字段清单

| 字段 | 值 | 判定 | 依据 |
|---|---|---|---|
| `name` | `demand-received` | ✅ | 小写 + 连字符，≤64 字符；与目录 `069-demand-received` 的 kebab 部分完全一致 |
| `description` | 见 2.2 逐句分析 | ✅ | 值 326 字符（≤1024） |
| `argument-hint` | `"[path-to-incoming] [--slug=custom-slug]"` | ✅ | SPEC §1.2 允许字段；与正文完全自洽：`[path-to-incoming]` 对应 Step 1 的读入要求（L8），`--slug=custom-slug` 对应输出路径 `inbound/[slug]/triage.md` 的 `[slug]`（L13/L119）——hint 与正文词汇单一、无缝隙（优于 067 的 argument-hint/正文 flag 不一致） |

无任何 SPEC §1.3 禁用键（无 `metadata`/`version`/`tags`/`trigger`/`model` 等）。YAML 语法合法：description 为未加引号的 plain scalar，内含两个双引号（`says "we got a demand letter"`）与 em dash——plain scalar 中段嵌双引号合法（实测可解析），与 028/067 同款写法。

### 2.2 description 逐句分析

原句（L3，值 326 字符）：

> Triage an inbound demand letter — extract fields, cross-check the portfolio, assess merit, present response options with a recommendation, and hand off to matter-intake or demand-intake if escalation is warranted. Use when the user says "we got a demand letter", "triage this demand", or shares an incoming demand to evaluate.

| 句 | 内容 | 三问定位 | 判定 |
|---|---|---|---|
| 句 1 | Triage an inbound demand letter + 五步过程链（extract fields / cross-check the portfolio / assess merit / present response options with a recommendation / hand off to matter-intake or demand-intake） | WHAT（动作 + 核心过程链） | ✅ 与 Body 的 7 步 Workflow 逐一对应（Step 1 提取 ↔ extract；Step 2 交叉核对 ↔ cross-check；Step 3 价值评估 ↔ assess merit；Step 4 选项 ↔ present options；Step 7 交接 ↔ hand off）——description 与 body 的契约对齐清晰 |
| 句 2 | Use when the user says "we got a demand letter", "triage this demand", or shares an incoming demand to evaluate | WHEN（两个用户口语触发词 + 一个行为触发场景） | ✅ 与 028-subpoena-triage 的 `"we got a subpoena"` 同款"引号内真实用户话术"设计——语料库少见的优质触发设计 |

**Voice**：动词开头（"Triage an inbound demand letter..."）描述 skill 的功能，与 SPEC §2.6 Good 示例（"Generate comprehensive test plans..."）同句式、与 028（"Triage a subpoena..."）逐字同构——描述 WHAT 的动词开头不构成 imperative 违规（§2.3 禁止的是 "Use this skill to..." 式与第一/二人称）；全文第三人称，无 I/you/we。

**触发信号**（§2.4 要求至少一条）：句 2 以 "Use when the user says..." 开头——**字面命中标准信号** `"Use when the user..."`，无注通过。

**KEYWORDS**：demand letter、triage、incoming demand、matter-intake、demand-intake——领域词齐全；口语触发词（"we got a demand letter"、"triage this demand"）是家族级最优触发设计之一（与 028 并列）。

**对照版（no-trigger）**：description 截为仅句 1（约 205 字符）。保留 WHAT 与 KEYWORDS、删除全部 WHEN 触发句——符合无触发对照集设计目的，对照版语义完整可读。

### 2.3 语法

- description 内嵌双引号是唯一潜在脆弱点：现行 plain scalar 写法实测合法（与 028 判定一致），可考虑整体双引号包裹并转义内层引号（§13 P7 附带提及）。
- `argument-hint` 中 `[path-to-incoming]`/`[--slug=custom-slug]` 为占位符写法，符合 hint 惯例。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（L6–L235）

| 行号 | 标题 | 级别 | 功能 | 备注 |
|---|---|---|---|---|
| L6 | `# Demand Received` | H1 | 标题 #1 | **与 L22 重复**（同 028/034/037/067 家族模板残片，见 §4.1-#1、§13 P1） |
| L7–19 | 7 条编号 TL;DR + 交接四分支 | — | 极简总览 | 与 Workflow 7 步编号一致（见 3.2），含 handoff 四分支（matter-intake / demand-intake / related_matters / standalone） |
| L20 | `---` | — | 分隔线 | 残片性质（TL;DR 区块收尾线） |
| L22 | `# Demand Received` | H1 | 正文标题 | 重复的第二个 H1 |
| L24–26 | `## Purpose` | H2 | 动机 + 失败模式（"treating them all alike"）| 简洁得体，定位分诊价值 |
| L28–32 | `## Load context` | H2 | 输入三件套：incoming 文档 / `_log.yaml`（组合交叉核对）/ 插件 CLAUDE.md（风险校准、landscape、demand-letter practice）| 对应 PROC-03；依赖外部插件契约 |
| L34–214 | `## Workflow` | H2 | 7 步工作流（Step 1–7）| 详见 3.2；Step 6 内含完整输出模板围栏（L121–214） |
| L225–227 | `## Close with the next-steps decision tree` | H2 | 收尾决策树（按插件 CLAUDE.md `## Outputs` 定制五默认分支）| 对应 OUT-04；依赖外部契约 |
| L229–235 | `## What this skill does not do` | H2 | 边界（4 条）| 对应 SPEC 必需"Scope"节 |

### 3.2 必需章节（SPEC §3.1）

| 必需章节 | 位置 | 判定 |
|---|---|---|
| Workflow / Process | `## Workflow`（L34–214），7 个 `### Step N`（Step 1 读取 → Step 7 交接）| ✅ 完整、有序、每步可执行；Step 5 内嵌本家族标志性的"no silent supplement"四选项升级话术与来源标注纪律 |
| Output Format | Step 6（L117–214）内的完整模板围栏（L121–214，94 行）| ✅ 实体完整：特权继承横幅、READ FOR TRIAGE 免责、头部字段、The demand/Facts/Legal basis/Threats/Portfolio cross-check/Merit/Options/Deadlines/Immediate actions 九子节——与 028/067 同为家族级完整输出契约；**注意：无独立 `## Output` 标题**，模板嵌入 Step 6 之内（dossier 判"Workflow/Output 模板/边界声明齐全"成立；§13 P5 建议可选地独立成节） |
| Scope / Limitations | `## What this skill does not do`（L229–235）| ✅ 4 条显式边界（不验证法条/不发送响应/不决定价值/不代做建件决策），另有 4 处功能式边界：no silent supplement（L113）、来源标注纪律（L115）、privilege 继承横幅（L124）、READ FOR TRIAGE 免责（L128） |

### 3.3 委托结构

- **本目录内委托**：无——不引用任何 `references/` 或 `scripts/` 文件，全部内容内联（与 028/067 同款零悬空引用设计）。
- **外部插件委托**（关键）：`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 被 **9 处**引用，承担四类内容：插件 CLAUDE.md（`## Risk calibration`/`## Landscape`/`## Demand-letter practice`/`## Outputs`/`## Who's using this`，L3/32/75/122/226）、`matters/_log.yaml`（组合交叉核对实体，L2/31）、`inbound/[slug]/triage.md`（输出路径，L13/119）、`inbound/`（standalone 留档，L223）。**无回退**——这是本 skill 最大的可移植性风险（详见 §4/§5/§9/§13 P0-1）。
- 跨 skill 引用均为散文式命名（`matter-intake` L15/220、`demand-intake` L16/86/96/221/222、`demand-draft` L232、`legal-hold` L101/209），无 `../other-skill/` 文件级引用，符合 SPEC §3.3。`demand-draft` 是 018-demand-draft 的姊妹 skill（出站函起草方），069 明确将起草职责外置（L232）——职责边界与 018 互补（详见 §4.1-#4）。

### 3.4 层级健康度

- **H1 出现两次**（L6/L22）——同一文件内两个 `# Demand Received`，与 034/037/067/028 同源同款，是该插件家族模板的公共特征（§13 P1）。
- 模板围栏内还有一个 `# Demand Received — Triage`（L126）——那是输出模板的 H1，属交付物格式，非结构缺陷。
- H2 主干 5 个（Purpose/Load context/Workflow/Close/Scope），H3 为 7 个 Step，层级 2–3 级、单调递增，无跳级。模板内另有 9 个 H2（九子节）+ 4 个 H3（选项 A–D），全部在围栏内，不参与正文层级。
- 章节顺序的叙事弧合理：动机（Purpose）→ 输入（Load context）→ 执行（Workflow Step 1–7）→ 收尾（决策树）→ 边界（Scope）。与家族同款"先立规矩后干活"组织方式。

### 3.5 长度

- Body 230 行（L6–L235），文件总计 235 行。process 模式目标 ~200 行，超出约 15%——体量合理（7 步 + 94 行完整模板，信息密度高，无明显注水）。
- dossier 记"正文 235 行"——实测 235 为文件总行数（含 frontmatter），正文 230 行，无实质分歧（与 067/068 的计数口径相同）。

---

## 4. 逻辑一致性深度审查

### 4.1 衔接与指代

| # | 发现 | 严重度 |
|---|---|---|
| 1 | **双 H1 + TL;DR 残片**（L6/L22）：与 028/034/037/067 同源同款家族模板残片。TL;DR（L7–19）与正文各节内容重复（1↔Step 1、2↔Load context、3↔Load context、4↔meta 指引、5↔Step 2–4、6↔Step 6、7↔Step 7），但**编号体系与 Workflow 的 7 步完全一致**（对比 067 的 10 步 TL;DR vs 7 步 Workflow 的编号错位，本 skill 无此问题）——TL;DR 是压缩视图而非矛盾视图。 | 🟢 |
| 2 | **"reference below" 无明确指代**（L10）："Follow the workflow and reference below"——与 037/067 同款措辞，"reference" 指代下方详述章节（非独立文件），语义可通但含混。 | 🟢 |
| 3 | **Step 2 "Update related_matters if it's a tangent" 措辞微糊**（L61）：该句位于"direct match + active"分支内——"adding incoming to the existing matter" 与 "update related_matters if it's a tangent" 并列，但"与直接匹配事项相邻的切线事项"判定标准未定义（什么构成 tangent？）；语义无害但读者需自行推断（§13 P5）。 | 🟢 |
| 4 | **三命令邻接关系的显式化缺口**：Option A 的 next step 是 `/demand-intake`（L86，"with pre-populated fields for a counter-response letter"），而 Scope 节说起草在 `demand-draft`（L232）——实际链条是 triage → demand-intake（预填充交接）→ demand-draft（起草），两个命令名邻接且职责不同，但正文从未一次性点明这条链（§13 P3）。 | 🟡 |
| 5 | **来源标注标签与输出模板的衔接缺口**：Step 5 要求进入 triage 的所有引文携带来源标签（`[Westlaw]`/`[CourtListener]`/`[Trellis]`/`[Descrybe]`/MCP 工具名/`[web search — verify]`/`[model knowledge — verify]`/`[user provided]`，L115），PROC-08 据此判定；但输出模板的 `## Legal basis cited` 节（L149–151）只规定了 `[SME VERIFY: applicability / currency / jurisdiction]` 旗标，**从未展示来源标签应落在何处**——两族标签互补（来源标签管出处、SME VERIFY 管验证）而非矛盾，但模板字面执行会遗漏来源标签（§13 P2）。 | 🟡 |
| 6 | 七步闭环自洽：读取（Step 1）→ 交叉核对（Step 2）→ 价值评估（Step 3）→ 响应选项（Step 4）→ 期限（Step 5）→ 撰写（Step 6）→ 交接（Step 7）；TL;DR、description 过程链、Workflow 三处编号/顺序完全一致，无 067 式 TL;DR 遗漏 gate 的问题。 | ✅ |
| 7 | 交接四分支双向一致：TL;DR（L14–19）↔ Step 7（L216–223）↔ description（"hand off to matter-intake or demand-intake"）三处分支集相同；"standalone → no further action"（L18）与 "leave in inbound/; no portfolio change"（L223）语义一致。 | ✅ |
| 8 | 期限逻辑闭环：Step 5（L107–109）的内部决策期限公式（stated deadline − 5 business days）与模板 `## Deadlines` 三字段（L199–203：their stated / our internal / legal）一一对应；"their stated deadline doesn't bind us" 的立场在模板中一致贯彻。 | ✅ |

### 4.2 矛盾检查

- 无自我矛盾声明。六道防护（no silent supplement / 来源标签纪律 / SME VERIFY 纪律 / READ FOR TRIAGE 免责 / 特权继承横幅 / 交接须用户确认）相互独立、无优先级冲突——与 028/037 同属护栏密度最高的家族梯队。
- **法条/规则引用准确**：FRE 408（L49/L95）"protection attaches from conduct and context, not merely from labeling" 的处理是法律上准确且精细的——settlement-communication 保护确实取决于"为和解目的、在和解过程中"的实质语境而非文件标签，且明确要求按法域查 state equivalent（L49/L95），无过界断言；L143 模板字段四值（labeled / substantively / neither / ambiguous）与 Step 1 定义一致。
- **免责与评级的边界自洽**：Step 3（L67 "Not a legal opinion — a structured read"）→ 模板 L128（"READ FOR TRIAGE, NOT OPINION"）→ L177（triage rating 附 `[SME VERIFY: counsel to confirm...]`）→ Scope #3（L233 "Decide merit definitively" 被排除）——四层措辞同一立场，无"既给意见又不给意见"的矛盾。
- **"No silent supplement"（L113）与来源标签（L115）互补而非冲突**：一个管"不静默补内容"，一个管"已有引文的出处标记"，与 028/037 家族语义完全一致；四选项话术（broaden / other tool / web search tagged / stop）与 SCORING 的 PROC-07 逐字对应。
- `demand-draft`（起草）与 `demand-intake`（交接）的职责边界：Scope #2（L232）明确 "Drafts are drafted in demand-draft; this skill stops at the triage decision"，与 NEG-02/CF-02（不代写响应函）语义闭环——069 是 018 的入站侧姊妹，边界清晰。

### 4.3 代码与条件

- 无伪代码、无未定义的代码实体；唯一的"代码"是输出模板围栏块（L121–214）。
- 条件分支全部给出明确行为：交叉核对四情形（direct+active / direct+closed / type match / no match，L61–64）、响应选项四选一（A–D 各有 When/Tradeoff/Next step，L83–102）、来源覆盖薄四选项（L113）、交接四分支（L216–223）、settlement 四值（L143）、deadline 三类（L107–109）。**无悬挂条件**。
- 结论断言克制：Scope 四条 "does not" 全部是强否定 + 替代指引（"user decides" L234、"counsel's, not this skill's" L128），无半吊子承诺。

---

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用（位置） | 目标 | 类型 | 存在性 | 判定 |
|---|---|---|---|---|
| L2/31/223 | `.../matters/_log.yaml`（组合交叉核对实体 + related_matters 更新目标）| 外部插件文件 | **本机实测不可达**（见 5.2-#1）| 🔴 高依赖、无回退 |
| L3/32/75/122/226 | `.../litigation-legal/CLAUDE.md`（`## Risk calibration`/`## Landscape`/`## Demand-letter practice`/`## Outputs`/`## Who's using this`）| 外部插件文件 | 不可达 | 🔴 高依赖、无回退 |
| L13/119/223 | `.../litigation-legal/inbound/[slug]/triage.md`、`incoming.[ext]`、`inbound/` | 外部插件路径 | 不可达 | 🔴 输出路径依赖（与 OUT-01 glob 的匹配缝隙见 §10.3-#1）|
| L130–213 | `[slug]`/`[YYYY-MM-DD]`/`[entity / person]` 等占位符 | 自含模板 | ✅ 内联 | ✅ |
| check.py L11 | `_shared/checker.py`（`sys.path.insert(0, "..", "_shared")`）| 共享库 | ✅ 存在（350 行），函数签名完全匹配（见 5.3）| ✅ |

### 5.2 不可见资源（风险清单）

1. **插件配置（9 处）+ `matters/` 实体**：**实测验证（2026-08-06）**——本机 `~/.claude/plugins/config/claude-for-legal/` 下**仅有 `ai-governance-legal/` 子目录，`litigation-legal/` 不存在**（与 067 审查时实测的机器状态一致）。故 `litigation-legal/CLAUDE.md`、`matters/_log.yaml`、`inbound/` 全部不可达。若评测沙箱未挂载该插件，则：风险校准/landscape/demand-letter practice 无来源（Step 3 的 leverage 判定失去参考）、`_log.yaml` 交叉核对无实体（**PROC-03 直接不可达**）、输出路径写不进去（**OUT-01 直接不可达**）——两条核心 criteria 依赖同一外部契约。
2. **`[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see ## Who's using this]`（L122）**：模板头依赖插件 CLAUDE.md 的两个小节；无插件环境下该占位符无法展开，agent 只能跳过或臆造。同理 L226 的决策树依赖 `## Outputs` 的默认分支定义。
3. **`~` 用户主目录路径**：硬编码相对用户主目录的绝对路径，跨机器不可移植——与 017/018/028/034/036/037/040/067/077/127/139/144/160/170/185/200/212/258/279/304 等全部 claude-for-legal 系 skill 同款问题（家族级 P0，见 §13 P0-1）。

### 5.3 共享库验证

`D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py`（350 行）提供 `file_exists`（glob 支持）、`tool_log_contains`、`set_tool_log_path`、`set_agent_output` 等函数，与 check.py 的 import 和调用签名逐一匹配。**`file_exists` 直接使用 `globmod.glob(path, recursive=True)`**——实测（Python 3.14.6）对隐藏目录（`.` 开头）**默认不匹配**（`include_hidden=False`），该行为直接决定 OUT-01 的判定结果（§10.3-#1 实证）。check.py L24–29 的"路径 vs 原始文本"二分支逻辑与 main()（L61–63）的读文件逻辑有轻微重复（no-trigger 版 check.py 无此块，直接 `set_agent_output(agent_output)`），行为正确、无害。

### 5.4 嵌套与跨 Skill

无嵌套 skill；跨 skill 仅散文式命名（`matter-intake`/`demand-intake`/`demand-draft`/`legal-hold`），无 `../other-skill/` 文件级引用——完全符合 SPEC §3.3 的禁止条款。

---

## 6. 语法与格式质量

| 检查项 | 结果 | 说明 |
|---|---|---|
| 拼写 | ✅ | 全文无拼写错误（抽查 235 行）；法律术语（settlement-communication / FRE 408 / account stated / cure period / statute of limitations / legal hold / privilege）拼写与大小写统一 |
| 术语一致性 | ✅ | `demand`/`triage`/`portfolio`/`[slug]`/`SME VERIFY`/`related_matters` 用法稳定；`matter-intake`/`demand-intake` 三处（TL;DR、Step 7、description）拼写一致 |
| Markdown 结构 | ✅ | 代码围栏 1 处（模板 L121–214，配对正确）、引用块 2 处（特权继承横幅 L124、READ FOR TRIAGE L128）、模板内 5 个复选框（L209–213），语法全部合法 |
| 占位符 | ✅ | `[slug]`/`[YYYY-MM-DD]`/`[entity / person]`/`[list]`/`[date]`/`[path]` 等统一方括号风格，无残留未替换的真实数据 |
| 截断 | ✅ | 无中途截断迹象；L235 收尾完整（"**Make the matter-creation call.** Surfaces the recommendation; user decides." 收束干脆） |
| 混杂 | ✅ | 全英文、无中英混杂、无乱码、无葡语残留 |
| 标点 | ⚠️ | em dash（—）58 处 / 235 行（含 description 1 处）——密度 corpus 前列（067 为 75/274），作风格元素高度统一，但高频使长句断句节奏单一；§13 P7 建议在关键判定处混用冒号/分号 |
| 小瑕疵 | ⚠️ | (1) L6/L22 双 H1；(2) L7–19 TL;DR 与正文重复（虽编号一致，仍是双份内容）；(3) L10 "reference below" 指代含混；(4) 模板 L143 的 `[SME VERIFY]` 与 L149 的 `[SME VERIFY: applicability / currency / jurisdiction]` 两种分隔符（裸标记 vs 冒号）并存——语义同族、格式微差 |

无 TODO/FIXME/lorem 文本、无被截断的半句。整体为 corpus 中语法质量最高梯队之一（与 dossier 评价"规范流畅"一致；L113 的四选项话术与 L124 的特权继承横幅是全文语言质量峰值）。

---

## 7. 规范合规性（SKILL-SPEC.md 12 项清单）

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符，≤64，匹配目录 | ✅ | `demand-received` 与目录 kebab 部分一致 |
| 2 | description：第三人称，WHAT+WHEN+KEYWORDS，≤1024 | ✅ | 326 字符，三问齐备，WHAT 带五步过程链 |
| 3 | description：无 imperative/第一/二人称开头 | ✅ | 动词开头描述 WHAT（同 SPEC §2.6 Good 示例句式），无 "Use this skill to"、无 I/you/we；句 2 引号内 "we" 是用户话语引用，非 skill 自称（028 同款判定） |
| 4 | description：无跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 结构 |
| 5 | description：≥1 触发信号 | ✅ | "Use when the user says..." **字面命中**标准信号 |
| 6 | frontmatter：无允许列表外键 | ✅ | 仅 name/description/argument-hint |
| 7 | body ≤600 行 | ✅ | 230 行 |
| 8 | body 有 workflow/process 节 | ✅ | `## Workflow` Step 1–7，全程门控 |
| 9 | body 有 output format 节 | ✅ | Step 6 内嵌 94 行完整模板（九子节 + 特权/免责横幅）——实体完备；**注**：无独立 `## Output` 标题（嵌入 Step 6），实体层面满足、标题层面可优化（§13 P5） |
| 10 | body 有 scope/limitations 节 | ✅ | `## What this skill does not do` 4 条 + 4 处功能式边界 |
| 11 | body 无跨 skill 文件引用 | ✅ | 无 `../` 引用；插件路径属外部配置契约（§5.2）；跨 skill 均为散文式命名 |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✅ | `069-demand-received` |

**结果：12/12 通过，且全部为无注通过**（与 028/067 同级）。三必需节齐全、质量高，描述合规无瑕疵——合规性与家族最佳梯队并列。

---

## 8. 人机感评估

| 维度 | 结果 | 说明 |
|---|---|---|
| Emoji | ✅ 0 处 | 正文与模板**零 emoji**——比家族多数 skill（028 用功能标记、067 用 46 处功能标记）更克制；复选框（L209–213）是纯 markdown 清单，无装饰 |
| 全大写 | ✅ 零语气性使用 | 无 "STOP!"/"DO NOT" 喊话式指令；全大写仅出现在标记体系（`SME VERIFY`/`READ FOR TRIAGE, NOT OPINION`）与模板字段（`[WORK-PRODUCT HEADER...]`），属数据而非语气 |
| 语气 | ✅ 律师助手角色、克制专业 | "The failure mode is treating them all alike"（L26）、"Be blunt. The user is triaging, not writing the brief."（L77）——有专业人格但不说教；无填充语 |
| 人机边界 | ✅ corpus 最清晰之一 | 六处"律师决定"声明：handoff 须用户确认（L216）、triage rating 待 counsel 确认（L177）、低置信来源由律师决定（L113）、法条验证留给用户/citator（L231）、matter-creation 由用户决定（L234）、privilege 分发决定权在律师（L124）；"A lawyer decides whether to accept lower-confidence sources; the skill does not decide for them"（L113）是家族级最佳表述之一 |
| 人称 | ✅ | description 与 body 均第三人称；L113/L124/L128 的引用块与横幅是 agent 面向用户的交互话术（属模板内容而非 agent 语气），用法恰当 |
| 表格密度 | ⚠️ 低 | 0 张表 / 230 行——Step 2 交叉核对四情形（L61–64）、Step 4 选项 A–D（L83–102）均为"列表式可执行"，本可表格式呈现（SPEC §3.4 建议决策树优先）；列表已足够清晰，非缺陷（§13 P6） |
| 场景温度 | ✅ | 特权 waive 风险（L124）、account stated 静默风险（L100）、法条臆造的职业暴露（L231）均以专业风险语言处理，无恐吓腔 |

评价：律师助理式克制、边界感强、零装饰——dossier 的"专业克制，无填充语，面向律师语气恰当"复核成立。六道防护 + 六处"律师决定"声明的密度在 322 个 skill 中居家族第一梯队。

---

## 9. 可执行性评估

**独立可执行性评分：7.0 / 10**（分环境差异极大，见下）

| 子项 | 得分 | 说明 |
|---|---|---|
| 步骤操作性 | 9.5/10 | Step 1–7 每步都有具体指令与话术模板：字段清单九项（L38–48）、settlement 四值（L143）、交叉核对四情形判定规则（L61–64）、四选项升级话术（L113）、来源标签八类（L115）、选项 A–D 的 When/Tradeoff/Next step（L83–102）、deadline 三类（L107–109）。agent 几乎不需要自行推断行为 |
| 交付物明确性 | 9.5/10 | 交付物 = `inbound/[slug]/triage.md` + `incoming.[ext]`；94 行模板九子节全部预定义（The demand/Facts/Legal basis/Threats/Portfolio cross-check/Merit/Options/Deadlines/Immediate actions）+ 特权继承横幅 + READ FOR TRIAGE 免责 + 5 项 immediate actions 复选框——corpus 中最精确的输出契约之一 |
| 工具依赖 | 3.5/10 | 关键路径依赖插件配置（9 处，含 `## Risk calibration`/`## Landscape`/`## Demand-letter practice`/`## Outputs`/`## Who's using this`）+ `_log.yaml` 实体 + `inbound/` 输出目录；`~` 绝对路径在沙箱大概率不可解析（本机实测 litigation-legal 子目录不存在）|
| 独立运行（无插件环境） | 6.0/10 | Load context 失败 → 风险校准与 leverage 判定失去参考（agent 只能询问或推断）；`_log.yaml` 读不到 → 交叉核对空转（PROC-03 判定悬空）；输出路径不存在 → agent 需自行决定落点（与 OUT-01 glob 语义冲突，§10.3-#1）；Step 1/3/4/5 的提取/评估/选项/期限逻辑自足可执行；模板完整可复制 |
| 独立运行（插件环境） | 9.5/10 | 按设计用途（litigation-legal 插件已安装）运行时近乎满分：交叉核对、风险校准、输出路径、决策树全链路可执行 |

结论：skill 自身的可执行性设计是 corpus 顶尖（步骤 9.5 / 交付物 9.5），瓶颈完全在外部依赖契约——与 028/067 同构（家族级问题）。修复 P0-1/P0-2（含 fixture 方案）后独立可执行性可升至 8.5–9/10。

---

## 10. SCORING.yaml 交叉参考

### 10.1 18 条 criteria 溯源

`total_items: 18` 实测与分类求和一致（scope 3 + process 8 + output 4 + negative 2 + qa 1 = 18）；judge 分布：script 2 + llm 16；pattern: process。

| ID | 类别 | 检查点摘要 | Body 对应位置 | 判定方式 | 一致性 |
|---|---|---|---|---|---|
| SCOPE-01 | scope | 读取传入的 demand 文档并作为分诊依据 | Step 1（L36–49）、TL;DR #1（L8）| script | ⚠️ 任意 Read 工具调用即通过，低区分度（见 10.3-#2）|
| SCOPE-02 | scope | 输出定位为 triage 而非法律意见（含 READ FOR TRIAGE 免责）| 模板 L128 | llm | ✅ 与模板横幅逐字对应 |
| SCOPE-03 | scope | 不验证法条/不终局定 merit（SME VERIFY 旗标替代）| Scope #1/#3（L231/233）、L113 | llm | ✅ "Inventing legal analysis... is malpractice exposure"（L231）|
| PROC-01 | process | 九字段提取（sender/recipient/delivery/date received vs signed/type/asks/facts/basis/threats）| Step 1（L38–48）| llm | ✅ 字段清单与 criterion 逐字对应 |
| PROC-02 | process | settlement-communication 四值捕获（labeled/substantive/neither/ambiguous）| Step 1（L49）+ 模板 L143 | llm | ✅ 四值与 criterion 逐字对应；本 skill 相对 028 的差异化能力 |
| PROC-03 | process | `_log.yaml` 交叉核对：direct/type/subject 三匹配 + 路由建议 | Step 2（L51–64）+ 模板 L159–164 | llm | ✅ 三匹配与四分支完整；**实体依赖插件环境（§13 P0-1）** |
| PROC-04 | process | merit 评估五要素 + blunt 评级（substantial/debatable/weak/frivolous）| Step 3（L66–77）+ 模板 L168–177 | llm | ✅ "Be blunt" 与四值评级逐字对应 |
| PROC-05 | process | 3–4 个响应选项带 tradeoff + 单一推荐 | Step 4（L79–103）+ 模板 L181–195 | llm | ✅ A–D 四选项 + Recommendation 字段 |
| PROC-06 | process | 期限分类三类 + 紧期限日历化 | Step 5（L105–111）+ 模板 L199–203 | llm | ✅ 三字段逐字对应 |
| PROC-07 | process | no silent supplement——薄覆盖时四选项 | Step 5（L113）| llm | ✅ 四选项话术逐字对应 |
| PROC-08 | process | 引文来源标签（8 类）不剥离 | Step 5（L115）| llm | ✅ "Never strip or collapse the tags"；模板衔接缺口见 10.3-#3 |
| OUT-01 | output | triage.md 写入 inbound/[slug]/ + incoming 复制/链接 | Step 6（L13/119）| script | ⚠️ 路径/glob 匹配缝隙（实测，见 10.3-#1）|
| OUT-02 | output | triage 含交叉核对节与推荐 | 模板 L159–164/L195 | llm | ✅ |
| OUT-03 | output | immediate actions 清单（hold/matter/counsel/insurance/escalation）| 模板 L207–213 | llm | ✅ 五项复选框逐字对应 |
| OUT-04 | output | 收尾 next-steps 决策树定制化 | L225–227 | llm | ✅ 五默认分支语义对应；依赖插件 `## Outputs` |
| NEG-01 | negative | 不臆造法律分析、不断言引文有效性 | L113/L115/L231 | llm | ✅ |
| NEG-02 | negative | 止步于分诊，不代写/代发响应函 | Scope #2（L232）、L233 | llm | ✅ "stops at the triage decision" |
| QA-01 | qa | 交接跟随用户选择而非单边行动 | Step 7（L216–223）| llm | ✅ "Based on recommendation and user confirmation" |

### 10.2 critical_failures

| ID | 触发条件 | Body 对应 | 判定 |
|---|---|---|---|
| CF-01 | 产出终局性法律意见或验证了法条（而非带旗标的分诊读）| Scope #1/#3（L231/233）、L128 | ✅ 合理 cap_to_0——与 SCOPE-02/03 行为要求互补而非冗余（行为要求 vs 后果封顶）|
| CF-02 | 薄研究覆盖时静默用模型知识/网络填充 | L113 | ✅ 合理 cap_to_0——"no silent supplement" 的否定形态，四选项话术逐字对应 |
| CF-03 | 未经用户指示即建件或发函 | Step 7（L216）、L234 | ✅ 合理 cap_to_0——"user decides" 的否定形态，与 QA-01 互补 |

### 10.3 发现的缝隙

1. **OUT-01 路径语义与 glob 的匹配风险（实证）**：skill 规定输出为 `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/[slug]/triage.md`（home 绝对路径、`.claude` 隐藏目录之下、workspace 之外），check.py 实现为 `file_exists(os.path.join(workspace, "**/inbound/**/triage.md"))`（workspace 相对 glob）。**实测（Python 3.14.6）**：`glob.glob("**/triage.md", recursive=True)` 默认不匹配隐藏目录（`include_hidden=False`）——即使 workspace = home，`.claude` 下的合规写入也无法命中；若 workspace ≠ home 则双重错位。**这是 028 审查中 🔴 R1 同类问题**（028 为三文件路径不一致，本 skill 为 skill 规定路径 vs 检查 glob 两处错位），必须评测前验证/修复（§13 P0-2）。
2. **SCOPE-01 低区分度**：`"tool"\s*:\s*"Read"` 匹配工具日志中**任何** Read 调用——agent 即使没读 demand 文档（读了别的文件）也能通过；判别力依赖 llm 项兜底。可改为检查 Read 目标路径含 `.pdf`/`.docx`/incoming 相关模式（同 028 对 PROC-01 的观察）。非错误，属判定力优化（§13 P4）。
3. **PROC-08 与模板的衔接缺口**：模板 `## Legal basis cited`（L149–151）只要求 `[SME VERIFY]` 旗标，未展示来源标签（`[Westlaw]` 等 8 类）的落点——照模板字面执行的 agent 满足 SME VERIFY 但可能丢来源标签，PROC-08 判定悬空（§13 P2）。
4. **privilege 继承横幅无独立测评点**：SCOPE-02 覆盖 READ FOR TRIAGE 免责，但 L124 的特权继承横幅（本 skill 相对 028 的差异化设计之一）未被任何 criterion 单独验证（§13 P4 附带）。
5. **script/llm 比例 2/16**：PROC-07/PROC-08 可用 `output_contains` 做近似脚本化（同 067 的 P4 建议），非错误，属效率性优化。
6. check.py docstring（L20 "Run all 2 script checks"）与实际实现数一致——**无 028 式 docstring 虚报问题**；SCORING 声明 2 条 script，check.py 实现恰好 2 条，无"声明未实现"的常见病。

---

## 11. 已知问题汇总（skill-dossier.md 引用）

Dossier 条目（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` L553–558）：

> ### 069-demand-received
> - **逻辑**: 读取→组合交叉核对→价值评估→响应选项→期限分类→撰写→交接七步闭环一致。
> - **语法**: 规范流畅。
> - **人机感**: 专业克制，无填充语，面向律师语气恰当。
> - **合规**: Description 第三人称，Workflow/Output 模板/边界声明齐全，正文 235 行 ≤600。
> - **总评**: 🟢 结构严谨、防护意识强。

对照评估：

| dossier 论断 | 本次审查 | 一致性 |
|---|---|---|
| 七步闭环一致（读取→交叉核对→价值评估→响应选项→期限分类→撰写→交接）| 复核成立 ✅（§4.1-#6）；本审查补充新发现：双 H1、来源标签/模板衔接缺口、三命令邻接未显式化、OUT-01 glob 缝隙（实证）| 基本一致，本审查更细 |
| 规范流畅 | ✅ 确认（§6：零拼写错误、零 emoji、模板与横幅语言质量高）| 一致 |
| 专业克制、面向律师语气恰当 | ✅ 确认（§8：零 emoji、六处"律师决定"边界、FRE 408 处理精细）| 一致 |
| Workflow/Output 模板/边界声明齐全 | ✅ 确认（§3.2：三必需节实体齐全；Output 为 Step 6 内嵌 94 行模板而非独立节）| 一致 |
| 🟢 完全合规（description 第三人称、正文 ≤600）| ✅ 12/12 全部无注通过（§7）| 一致 |
| 正文 235 行 | 实测文件总计 235 行 / 正文 230 行——dossier 计全文件行数，无实质分歧 | 无实质分歧 |
| 总评 🟢 结构严谨、防护意识强 | 本审查给 🟢 A−（86/100，§12）——与 028（A− 89/100）、067（A− 88/100）同区间；扣分集中在外部插件契约（本机实测 litigation-legal 不存在）与 OUT-01 评测缝隙，均不推翻"结构严谨、防护意识强"的定位 | 方向一致 |

旧 REVIEW.md stub（4 行）给出的结论：

> **2026-08-05** | Claude | Dossier: 🟢
> 硬编码路径。Dossier: "结构严谨、防护意识强"。235 行。7 步闭环：读取→交叉核对→价值评估→响应选项→期限→撰写→交接。
> **综合**: 🟢 **A−** (55/100)

逐项核对：
1. **🟢 A− 评级**：与本审查同区间（本审查 A− 86/100；stub 的 55/100 为旧版标尺，与 067 stub 的 A 60/100 同标尺系，本审查采用 8 维度加权新标尺，86/100 ≈ 旧标尺 A− 区间，无实质矛盾）。
2. **"硬编码路径"——本次完成验证**：`~/.claude/plugins/config/claude-for-legal/` 目录**存在**但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**（2026-08-06 实测，与 067 审查时的机器状态一致）。stub 的谨慎措辞是准确的，且本审查将其升级为带修复方案的 P0-1。
3. **"结构严谨、防护意识强"**：复核成立——七步闭环、六道防护、94 行完整模板、FRE 408 实质-标签二分（L49）、交接四分支均属家族级领先设计；本审查额外发现 5 处 dossier 未记录的问题（§4.1/§10.3），不影响总评方向。

---

## 12. 综合评分（8 维度加权）

| 维度 | 权重 | 得分 | 依据 |
|---|---|---|---|
| 逻辑一致性 | 15% | 9.0 | 七步闭环三处编号一致、六道防护零矛盾、FRE 408 处理准确、无悬挂条件；扣分：三命令邻接未显式化（P3）、来源标签/模板衔接缺口（P2）、related_matters tangent 措辞（P5） |
| 参考文件与资源 | 15% | 6.0 | 零悬空内部引用、全内联结构；扣分：外部插件契约 9 处无回退，本机实测 litigation-legal 子目录不存在（家族 P0-1） |
| 语法与格式 | 10% | 9.5 | 全净、零 emoji、零拼写错误；仅双 H1、em dash 58 处、TL;DR 冗余为微瑕 |
| 规范合规性 | 20% | 9.5 | 12/12 全部无注通过；Output 节为内嵌模板（实体完备、标题可优化）扣 0.5 |
| 人机感 | 10% | 9.5 | 零 emoji、律师助理克制语气、六处"律师决定"边界、settlement 四值交互设计 |
| 可执行性 | 10% | 7.0 | 步骤/交付物各 9.5，但关键路径外部依赖无回退、OUT-01 路径/glob 错位（实证） |
| SCORING 对齐 | 10% | 9.0 | 18+3 全部可溯源、check.py 与 SCORING 声明一致；OUT-01 glob 缝隙与 SCOPE-01 低区分度各扣 0.5 |
| 法律适切性 | 10% | 9.5 | FRE 408 实质-标签二分、SME VERIFY 纪律、特权继承横幅、no silent supplement、legal hold 提示——corpus 最强法律护栏群之一 |

**加权总分 = 1.350 + 0.900 + 0.950 + 1.900 + 0.950 + 0.700 + 0.900 + 0.950 = 8.60 ≈ 8.6 / 10**

### 总评：🟢 A−（86/100）

claude-for-legal litigation 家族入站分诊侧的成熟作品，与 028-subpoena-triage（A− 89/100）、067-chronology（A− 88/100）并列为家族高质量梯队。合规 12/12 全部无注通过、七步闭环三处编号一致、零 emoji、六道防护零矛盾、94 行完整输出契约、FRE 408 实质-标签二分是全文最精细的法律设计（L49）；扣分集中在**外部插件契约**（9 处硬编码路径无回退，本机实测 `litigation-legal/` 子目录不存在——与 028/037/067 同款家族级 P0）与 **OUT-01 路径/glob 匹配缝隙**（Python 3.14 实测隐藏目录不可命中，028 审查中 🔴 R1 同类问题）。修复 §13 的 P0-1/P0-2 后可达 9.3（🟢 A）。

---

## 13. 修复建议（按优先级分层）★重点★

### 🔴 P0-1 — 致命（条件性）：litigation-legal 插件契约无回退（9 处硬编码路径，PROC-03/OUT-01 依赖同一实体）

**问题**：`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 被 9 处引用（L2/3/13/31/32/75/119/122/223），承担四类内容：插件 CLAUDE.md 的 `## Risk calibration`（Step 3 leverage 判定参考 L75）、`## Landscape`（发送方是否为惯常诉讼对手 L32）、`## Demand-letter practice`（house 语气与响应默认 L32）、`## Outputs`（工作产品头与决策树默认分支 L122/226）、`## Who's using this`（角色判定 L122）；`matters/_log.yaml`（Step 2 交叉核对实体 L2/31，**PROC-03 的判定前提**）；`inbound/[slug]/triage.md`（输出路径 L13/119，**OUT-01 的判定前提**）；`inbound/`（standalone 留档 L223）。**全 skill 没有一处 fallback**。本机实测（2026-08-06）：`~/.claude/plugins/config/claude-for-legal/` **存在**但仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**；`D:\SkillIF\skill-experiment\` 全树亦无 fixture 生成逻辑。若评测沙箱未挂载该插件（`~` 相对绝对路径在隔离工作区大概率不可解析），则：风险校准/landscape 无来源（agent 只能询问或推断）、`_log.yaml` 交叉核对无实体（agent 的合规行为是声明无法核对，PROC-03 判定悬空）、输出路径写不进去（OUT-01 不可达）——**两条核心 criteria 直接不可达**，且 agent 的合规行为（拒绝/声明）将导致评测任务零产出。这是全 skill 唯一没有兜底的关键路径，也是 028/037/067 已记录、069 未单独处理的家族级 P0。

**修复**（工作量 ~45–60 分钟，分两部分；**与家族其他 skill 合并执行，勿逐个补丁**）：

**方案 A — Skill 侧回退分支**（推荐，~30 分钟）：
1. `## Load context`（L28–32）加条件分支："If the plugin configuration at `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` exists, load it and follow its `## Risk calibration`, `## Landscape`, and `## Demand-letter practice` sections. If it does not exist (no firm config mounted), proceed with the session-provided facts, note at the top of the triage: 'Firm config not loaded — risk calibration and landscape defaults per this skill applied.'"——把 Step 3 的 leverage 判定参考从插件引用改为"插件优先、会话兜底"。
2. 为 Step 2 交叉核对（L51–64）追加回退："if `_log.yaml` does not exist or is empty, state 'Portfolio log not loaded — cross-check unavailable' in the triage's Portfolio cross-check section and proceed with the direct-match/type-match analysis based on session knowledge, each finding tagged `[model knowledge — verify]`"——既保持 PROC-03 的判定结构（三匹配字段仍在输出中），又不卡死整条流程。
3. 为输出路径（L13/L119）追加回退："if the plugin inbound directory is unreachable, write to `./inbound/[slug]/triage.md` in the workspace and note the relocation in the triage header"——**这一步同时直接缓解 P0-2 的 OUT-01 glob 缝隙**（workspace 内路径可被 `**/inbound/**/triage.md` 命中）。
4. 为 `[WORK-PRODUCT HEADER]`（L122）追加回退："if the plugin `## Outputs` section is unavailable, use the header format shown in the template below and note 'house header conventions not loaded'"。

**方案 B — 评测侧 fixture**（条件性，与 A 互补，~15 分钟）：在 SkillIF 评测工作区为每个 claude-for-legal 系 skill（017/018/028/034/036/037/040/067/069/077/127/139/144/160/170/185/200/212/258/279/304 等，凡引用该插件路径者）提供最小 fixture：`~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`（含 `## Risk calibration` 风险分级表、`## Landscape` 惯常诉讼对手列表、`## Demand-letter practice` house 语气约定、`## Outputs` 工作产品约定）+ `matters/_log.yaml`（含一个与发送方同 counterparty 的已存在 matter slug，供 PROC-03 命中 direct match）+ 1–2 份入站 demand 示例文档（供 Step 1 提取）。可脚本化生成（复用 `create_no_trigger_set.py` 的 corpus 遍历模式）。这同时解决全部 20+ 个同家族 skill 的同一问题，而非逐个补丁。

### 🔴 P0-2 — 致命（条件性）：OUT-01 输出路径与评测 glob 错位（实测隐藏目录不可命中）

**问题**：skill 规定输出为 `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/[slug]/triage.md`（home 绝对路径、`.claude` 隐藏目录之下、workspace 之外），check.py 实现为 `file_exists(os.path.join(workspace, "**/inbound/**/triage.md"))`（workspace 相对 glob）。**实证（Python 3.14.6）**：`glob.glob("**/triage.md", recursive=True)` 对 `.claude` 等隐藏目录**默认不匹配**（`include_hidden=False`，Python ≥3.11 行为）——实验在临时目录下创建 `.claude/inbound/acme/triage.md` 与 `plain/triage.md`，glob 仅命中后者，`**/inbound/**/triage.md` 零命中。两个风险点叠加：(1) 评测 workspace ≠ home 时，agent 按 skill 字面写入 home 的合规输出在 workspace glob 下不可见；(2) 即使 workspace = home，`.claude` 隐藏目录同样不可命中。**这是 028 审查 🔴 R1（输出路径三文件不一致）的 069 变体**——028 因 SKILL.md/SCORING/check.py 三处路径相互矛盾被定级 🔴，069 为"skill 规定路径 vs 检查 glob"两处错位、且经实测必然失配，同属评测链路级缺陷。

**修复**（工作量 ~20 分钟）：
1. **首选**：P0-1 方案 A 第 3 条（skill 侧回退写到 workspace 内 `./inbound/[slug]/triage.md`），使 agent 的合规输出落在 glob 可命中范围内——一个修复同时闭合 P0-1 与 P0-2。
2. 备选（不改 skill）：评测任务 prompt 明确输出落点（如"将 litigation-legal 配置预置于 workspace 下，triage 输出到 workspace 内 inbound/[slug]/triage.md"），并使 fixture 的 `inbound/` 目录直接挂在工作区（方案 B 变体）。
3. 同步验证 `_shared/checker.py` 的 `file_exists` 在目标 Python 版本下的 glob 行为（若评测环境为 Python <3.11，`include_hidden` 语义不同，需重测）；`OUT-01` 检查若改为显式扫描 workspace 与 home 双位置则彻底消除此缝隙。

### 🟡 P1 — 重要：双 H1 + TL;DR 冗余（家族模板残片）

**问题**：SKILL.md 顶部保留着插件家族模板的公共残片——`# Demand Received` H1 出现两次（L6/L22），L7–19 的 7 条 TL;DR 与正文各节逐一重复（1↔Step 1、2/3↔Load context、4↔meta 指引、5↔Step 2–4、6↔Step 6、7↔Step 7）。与 028（双 H1 + 9 步 TL;DR）、034（L6/L20 双 H1）、037（L6/L15 双 H1 + TL;DR）、067（L6/L21 双 H1 + 10 步 TL;DR）同源同款。**本 skill 的 TL;DR 编号与 Workflow 7 步完全一致（优于 067 的 10 vs 7 错位），无内容遗漏问题**——缺陷限于格式重复。

**修复**（工作量 ~10 分钟）：删除 L6 的第一个 H1（保留 L22 起正文）并清理 L20 的残片分隔线；TL;DR 若保留，降级为 `## Quick Start` 标题并补一行指向正文的注记（"详情见 ## Workflow Step 1–7"）——消除双 H1、保留快速入口。触发版与 no-trigger 对照版需同步（对照版除 description 外逐字节相同，改一处两处同步）。

### 🟡 P2 — 重要：输出模板未承载来源标注标签词汇（PROC-08 判定悬空风险）

**问题**：Step 5 的来源标注纪律（L115）定义 8 类来源标签（`[Westlaw]`/`[CourtListener]`/`[Trellis]`/`[Descrybe]`/MCP 工具名/`[web search — verify]`/`[model knowledge — verify]`/`[user provided]`）并要求"Never strip or collapse the tags"，PROC-08 据此判定；但 94 行输出模板中**没有任何字段展示这些标签的落点**——`## Legal basis cited`（L149–151）只要求 `[SME VERIFY: applicability / currency / jurisdiction]`，`## Merit assessment`（L168–177）同样只有 SME VERIFY 措辞。两类标记分工明确（来源标签管出处、SME VERIFY 管验证），但模板字面执行时 agent 会自然产出"只有 SME VERIFY、没有来源标签"的 triage——PROC-08 的 llm 判定将依赖评委对模板外行为的推断，判定基础脆弱。

**修复**（工作量 ~10 分钟）：在模板 `## Legal basis cited` 节补一行示例（如 `[citation] — tagged `[user provided]`, `[SME VERIFY: applicability / currency / jurisdiction]``），并在 `## Merit assessment` 的 Legal basis 行补"每处引文先标来源、再标验证"的一句说明；同步在 Step 5 的来源标注段（L115）加一句"the template's Legal basis section carries these tags inline"。两处各 1–2 行，模板与纪律由此闭环。

### 🟡 P3 — 重要：matter-intake / demand-intake / demand-draft 三命令邻接关系未一次性显式化

**问题**：body 三处引用三个家族命令且职责各异：`matter-intake`（建件 L15/220）、`demand-intake`（出站需求 intake，L16/86/96/221/222，其中 L86 是 Option A 的 next step、L96 是 Option C 的 next step）、`demand-draft`（出站函起草，L232 仅出现一次）。实际链条是"triage → demand-intake（预填充交接）→ demand-draft（起草）"，但全文没有任何一处把这条链一次说清——agent 读 L86 会以为"下一步就是起草"（其实 next step 只是 intake），读 L232 才知道起草在别处；对入站分诊的最终落点（response letter 由谁起草）需要跨三处拼图。

**修复**（工作量 ~5 分钟）：在 Step 7 交接节（L216–223）开头补一行路由说明："Handoff pipeline: this skill ends at the triage decision → `demand-intake` pre-populates the counter-response intake (Options A/C) → letter drafting happens in `demand-draft`. `matter-intake` is only for new-matter creation."——三命令一次定位，消除拼图成本。

### 🟡 P4 — 重要：SCORING 判定力优化（SCOPE-01 低区分度 + 可脚本化项未脚本化）

**问题**：(1) SCOPE-01 的 `"tool"\s*:\s*"Read"` 匹配任何 Read 调用——agent 未读 demand 文档也可通过，判别力弱（10.3-#2）；(2) PROC-07（no silent supplement）与 PROC-08（来源标签）可做 `output_contains` 近似脚本化（同 067 的 P4 方案），当前全部为 llm judge，增加评委负担且判定稳定性依赖评委一致性；(3) 特权继承横幅（L124，本 skill 相对 028 的差异化设计）无任何 criterion 单独验证。

**修复**（工作量 ~20 分钟）：
1. SCOPE-01 加强：pattern 改为匹配 Read 且目标路径含 incoming 文档特征（如 `Read` 后跟 `.pdf|.docx|.txt|incoming`），或保留现状并接受其"弱存在性检查"定位（家族惯例，非错误）。
2. PROC-08 增加 script 近似：`output_contains("\[web search — verify\]|\[model knowledge — verify\]|\[user provided\]|\[Westlaw\]")`（存在性检查，保留 llm judge 作主判定或作为双通道）。
3. 新增 1 条 llm criterion：特权继承横幅是否出现在 triage 输出中（`Privilege inheritance|privilege circle` 模式）。
4. 同步更新 SCORING.yaml 的 `total_items` 计数与 check.py 实现。**注意**：判定方式变更需与 2 Mode × 5 Harness 矩阵的评分聚合逻辑兼容，改动前确认 runner 对 `judge: script` 的依赖。

### 🟢 P5 — 优化：Output 模板独立成节 + Step 2 tangent 措辞

**问题**：(1) 94 行输出模板内嵌于 Step 6（L121–214），正文无独立 `## Output` 标题——实体完备、标题可优化（SPEC §3.1 要求的是"回答输出长什么样的节"，当前已满足，但独立成节提升可导航性，也便于将来下沉 references/）；(2) Step 2 的 "Update `related_matters` if it's a tangent"（L61）未定义 tangent 判定标准（§4.1-#3）。

**修复**（工作量 ~10 分钟）：
1. 将 Step 6 的模板围栏提取为独立 `## Output format` 节（Step 6 改为指向该节），或仅在 Step 6 前加一行 `### Output` 小标题——二选一，前者更符合 SPEC §3.1 的命名惯例。
2. L61 补半句："...Update `related_matters` if the incoming demand is a tangent (different subject but same counterparty) rather than the same dispute"——判定标准一行说清。

### 🟢 P6 — 优化：决策结构表格式呈现（SPEC §3.4）

**问题**：Step 2 交叉核对四情形（L61–64）、Step 4 选项 A–D（L83–102）实为天然决策树结构（情形 → 推荐动作），当前以 bullet 表达——与 028 审查的 R12 同款观察。SPEC §3.4 明确"decision trees over prose"。

**修复**（工作量 ~15 分钟）：Step 2 的四情形改为一列四行的小表（Match type / Finding / Recommendation）；Step 4 的选项 A–D 加一行表头式对比表（Option / When / Tradeoff / Next step），散文保留为补充说明。body 由此从 0 张表升至 2 张表，扫描性与 agent 分支确定性双升。

### 🟢 P7 — 优化：em dash 节奏调整 + description 双引号包裹（纯风格）

**问题**：(1) em dash（—）58 处 / 235 行，密度 corpus 前列（067 为 75/274）——风格统一是优点，但长段中连续 3–4 个 em dash 并列让扫描性下降（L113/L115/L124 三处最长段尤甚）；(2) description 的 plain scalar 内嵌双引号实测可解析，但后续若在句首引入引号可能破解析。

**修复**（工作量 ~10 分钟）：保留 description 与标记体系中的 em dash（功能性），对正文长段中的并列类 em dash 约 1/3 改为冒号（引出解释）或分号（并列分句），以 L113/L115/L124 三处为试点；description 可选地整体双引号包裹并转义内层引号（`\"we got a demand letter\"`）。纯风格项，不影响合规与逻辑；不改动模板内嵌文案（模板是输出契约，与正文散文不同）。

### 修复工作量汇总

| 优先级 | 项数 | 工作量 | 修复后预期 |
|---|---|---|---|
| 🔴 P0-1 + P0-2 | 2（含 A/B 方案）| ~60–75 分钟 | 可执行性 7.0 → 8.5+；PROC-03/OUT-01 可达；评测链路缝隙闭合 |
| 🟡 P1–P4 | 4 | ~45–60 分钟 | 结构清理、模板/纪律闭环、SCORING 判定更稳 |
| 🟢 P5–P7 | 3 | ~35 分钟 | 细节无瑕、风格优化，达 🟢 A（9.3/10）|
| **合计** | **9** | **约 2.5–3 小时** | 推荐全部执行；P0-1/P0-2 必须（对 20+ 个同家族 skill 可规模化复用，建议与 028/037/067 的 P0 方案合并执行，形成统一的 litigation-legal fixture 包）|

---

## 附录: 审查过程记录

- **审查日期**: 2026-08-06。
- **被替换文件**: 旧 `REVIEW.md`（stub），原文：

```
# REVIEW: 069-demand-received

**2026-08-05** | Claude | Dossier: 🟢

硬编码路径。Dossier: "结构严谨、防护意识强"。235 行。7 步闭环：读取→交叉核对→价值评估→响应选项→期限→撰写→交接。

**综合**: 🟢 **A−** (55/100)
```

- **过程时间线**:
  1. `Bash ls` 069 目录 → 4 文件清单（SKILL.md 235 行 / SCORING.yaml 168 行 / check.py 73 行 / REVIEW.md stub 4 行）；`Glob` 定位 SKILL-SPEC.md（`complex-skills\_shared\` 与 `complex-skills-no-trigger\_shared\` 两处，取前者）与 skill-dossier.md；
  2. `Read` SKILL.md（235 行，全文）→ SCORING.yaml（168 行）→ check.py（73 行）→ 旧 REVIEW.md（stub）；
  3. `Read` SKILL-SPEC.md（162 行）→ 逐项比对 12 项合规清单；
  4. `Read` skill-dossier.md（全文）→ 定位 069 条目（L553–558）+ 028 条目（L262–267，家族对比基准）+ 汇总统计；
  5. `Read` 067-chronology/REVIEW.md（449 行）与 068-deadlines/REVIEW.md（616 行）——同款 13 节模板的完整样例，作为本审查的结构基准；`Read` 028-subpoena-triage/REVIEW.md 首 80 行 + `grep` 其评分与修复结论（A− 89/100、🔴 R1 输出路径三文件不一致）——069 的姊妹 skill，作为家族横向对比基准；
  6. `diff` 触发版 vs no-trigger 版 SKILL.md / SCORING.yaml / check.py → SCORING 逐字节相同、description 仅 WHEN 句差异（保留 WHAT 句约 205 字符）、check.py 仅 `is_path` 防御块差异（L22–29 vs L22）；
  7. `grep` `_shared/checker.py` 函数清单 + `Read` 其 `file_exists`/`glob` 实现（L20–23）→ 与 check.py 的 import 和调用签名逐一匹配；
  8. `Bash ls ~/.claude/plugins/config/claude-for-legal/` → **实测** 仅含 `ai-governance-legal/` 子目录，`litigation-legal/` **不存在**（与 067 审查时的机器状态一致）；
  9. **实证测试**：Python 3.14.6 下创建临时隐藏目录 `.claude/inbound/acme/triage.md` 与 `plain/triage.md`，`glob.glob("**/triage.md", recursive=True)` 仅命中 plain、`**/inbound/**/triage.md` 零命中 → 确认 `include_hidden=False` 默认行为，OUT-01 缝隙实证成立；
  10. `Python` 计算 metrics：description 值 326 字符、body 230 行、em dash 58 处、emoji 0 处、H2 主干 5 个/H3 7 个（模板内另有 9 H2 + 4 H3）、表格 0 处、围栏 1 对（L121/L214）、引用块 2 处（L124/L128）、插件路径引用 9 处、`_log.yaml` 4 处、`inbound` 4 处、`SME VERIFY` 5 处、verify 标签 8 处、复选框 5 处；`yaml.safe_load` 验证 SCORING 结构：total_items 18 = 3+8+4+2+1，judge 分布 script 2 + llm 16，CF 3 条；
  11. 交叉核对：SCORING 18+3 条 ↔ Body 行号 ↔ check.py 实现；dossier/旧 stub 结论 ↔ 本次审查结论；028/067 家族基准 ↔ 069；
  12. 写作本 REVIEW.md（替换旧 stub）。
- **验证记录**: description 值 326 字符（≤1024 ✅）；Body 行数 230（≤600 ✅）；目录共 4 文件、无 references/scripts/；no-trigger 对照版存在于 `complex-skills-no-trigger\069-demand-received\`；`~/.claude/plugins/config/claude-for-legal/litigation-legal/` 实测不存在（父目录存在但仅含 ai-governance-legal）；glob 隐藏目录失配实证（Python 3.14.6）；SCORING `total_items: 18` 与分类求和一致。
- **方法论备注**: 本审查独立于 dossier 结论重新走查全部文件；dossier 的 🟢 评价与 stub 的 A− 评级在复核中成立（合规 12/12 全部无注通过、七步闭环编号一致、FRE 408 实质-标签二分为家族级精细设计），但本次新发现 5 处 dossier/stub 未记录的问题（OUT-01 隐藏目录失配【实证】、来源标签/模板衔接缺口、三命令邻接未显式化、SCOPE-01 低区分度、双 H1），并**实证确认了 stub 所称硬编码路径的不可达性**（`litigation-legal/` 子目录缺失，证据链与 067 审查一致）。故维持 🟢 A− 评级（86/100）——与 028（A− 89/100）、067（A− 88/100）同区间，突出该家族共性 P0（外部插件契约无回退 + 输出路径/glob 错位）；P0-1/P0-2 修复完成后评级可上调至 🟢 A。
