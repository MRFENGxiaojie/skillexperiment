# REVIEW: 097-portfolio

**审查日期**: 2026-08-06 | **Skill 类型**: process — IP 资产组合台账管理（五模式：初始化/报告/新增/更新/审计，围绕 `portfolio.yaml` 登记簿维护续展、年费、使用声明等期限） | **Body 行数**: 442 行

## 1. 目录全量清单

本 skill 目录共 7 个文件（4 个顶层文件 + 4 个 reference 文件，无隐藏文件、无 assets/templates/examples/phases/specs/docs 子目录）。全部文件均已完整读取（总计 812 行）。

```
D:\SkillIF\skill-experiment\complex-skills\097-portfolio\
├── SKILL.md                                 442 行 (17,842 B)  主体：frontmatter + 8 步指令 + 5 模式 + 登记簿 YAML 规格
├── SCORING.yaml                             183 行             20 条测评标准 + 3 条 critical_failures
├── check.py                                  85 行             4 项脚本检查，其余 16 项交 LLM judge
└── references\
    ├── handoffs.md                            6 行             与 prosecution/clearance 技能的交接说明
    ├── integration-ip-renewal-watcher-agent.md  5 行           定时巡检 agent 的集成说明
    ├── mode-5-audit.md                       73 行             Mode 5 审计的完整规格（正文外置）
    └── what-this-skill-does-not-do.md        18 行             Scope：五条边界
```

同一技能的对照集副本位于 `D:\SkillIF\skill-experiment\complex-skills-no-trigger\097-portfolio\`，与主版本唯一差异是 description 仅保留首句（无触发语），其余文件逐字节相同——符合无 trigger 对照集的设计意图（见第 11 节）。

## 2. Frontmatter 逐字段审查

### 2.1 name

`name: portfolio`（第 2 行）。小写+连字符、8 字符、≤64 字符，合规。与目录名 `097-portfolio` 的关系：目录前缀 `097-` 是语料序号约定，name 与去掉序号后的部分完全一致。按语料惯例判定 ✅（与 304-tabular-review 同款附注：若评测器做严格字符串比对则不等，建议按"目录名去序号后匹配"处理）。

### 2.2 description 逐句审查

description 在第 3 行，共 314 字符（≤1024 ✅）。逐句分析：

- **"Track the IP portfolio — registrations, renewals, maintenance fees, and use declarations."** — WHAT：覆盖范围明确（登记/续展/年费/使用声明）。**⚠️ 缺陷一**：以祈使动词 "Track" 开头，是命令式而非第三人称描述。§2.3 明令禁止祈使开头（"Use this skill to..."），虽然禁令列举的是 "Use this skill" 型句式，但 "Track the IP portfolio" 同样是对 agent 的直接命令——按第三人称应写 "Tracks the IP portfolio"。同类先例：dossier 中 177-auto-updater 因 description 以祈使句开头被记为"略偏离 §2.3"（🟡）。
- **"Use when checking what's renewing, adding or updating an asset, recording a maintenance filing, or auditing the register for gaps, lapses, and use-in-commerce questions."** — WHEN：四个触发场景（查续展/增改资产/记录申报/审计登记簿）覆盖全部五模式。**⚠️ 缺陷二**：§2.4 规定的触发信号是 "Use when **the user**..." / "Triggers on..." / "Use for..." 之一，此处写为 "Use when checking..."（动名词短语，缺 "the user"）。严格按短语匹配会落空；宽松匹配（含 "Use when"）可过。与 304-tabular-review 的 "Use when **user** says" 属同类一词之差缺陷。此外场景动词与主句不平行（checking / adding / updating / recording / auditing 全部为动名词，主语指代模糊）。
- **"Receives handoffs from prosecution and clearance work."** — 数据流声明：接收来自 prosecution/clearance 技能（本插件内其他技能）的交接。§2.5 禁止的是"NOT for X, use Y instead"型路由，此句为关系陈述而非路由指令，且用类别名而非技能名（符合"跨 skill 引用用散文名"惯例）。判定 ✅ 附注：严格审查器若按"description 不得提及其他 skill"执行则可能判违规，移入正文 Handoffs 章节（内容已在 references/handoffs.md）可零成本规避。

其余检查：无第一/第二人称（全文第三人称，未出现 "you/I/we"）✅；含 "renewals/maintenance fees/registrations/use declarations" 等检索关键词 ✅。

### 2.3 argument-hint

`argument-hint: "[--report [--days N] | --add | --update | --audit]"`（第 4 行）。规范 §1.2 白名单允许字段 ✅。⚠️ 与正文的小出入：正文 Mode 1（L249）还定义了 `--rebuild` 旗标，argument-hint 未列出（见 13 节第 9 条，🟢）。

### 2.4 其他字段

frontmatter 仅含 name、description、argument-hint 三个键，无任何规范禁止的键。✅

### 2.5 YAML 语法

frontmatter 为合法的三个键值对，description 内含一个 `—`（em 破折号）和一个撇号（`what's`），均不在 YAML 引号内、无转义问题，解析无碍；闭合 `---` 在第 5 行。description 314 字符中 `'` 正常。✅

## 3. Body 逐段结构分析

### 3.1 标题树

```
# Portfolio                                (L7)
## Instructions                            (L12-48)   8 步指令（含模式路由与护栏提醒）
## Examples                                (L50-70)   5 条命令示例（含 1 条带 --days 参数）
## Works better connected                  (L75-92)   与 IPMS/USPTO 直连的能力边界说明
## Purpose                                 (L95-103)  动机陈述（"This skill maintains that calendar."）
## Important: deadline reference caveat    (L106-120) 期限仅为参考的强免责声明
## Jurisdiction and type assumptions       (L123-153) 8 类法域/资产类型的维护机制规则
## The register                            (L158-243) portfolio.yaml 位置、结构、6 值状态枚举
## Mode 1: Initialise                      (L247-291)
   ### Step 1: Determine the source       (L251)
   ### Step 2: For each asset, compute deadlines (L258)
   ### Step 3: Write the register          (L272)
## Mode 2: Report                          (L296-341)
## Mode 3: Add                             (L346-383)
   ### Custom rules capture                (L369)
## Mode 4: Update                          (L388-433)
   ### Consequential-action gate           (L394)
   ### Sub-modes                           (L419)
## Reference Files                         (L438-442) 4 个 reference 的索引
```

### 3.2 必需章节检查

- **Workflow/Process** ✅：`## Instructions`（8 步）+ Mode 1–4 全量过程 + Mode 5 外置到 `references/mode-5-audit.md`。步骤链从数据源确定（Mode 1）→ 期限计算（规则表 + 状态枚举）→ 输出（报告模板）→ 增改（Mode 3/4）→ 审计（Mode 5），闭环完整。
- **Output Format** ✅（实质性满足）：无字面标题 `## Output Format`，但 Mode 1 初始化摘要模板（L276-291）、Mode 2 报告模板（L307-339，含五个分组与 SUMMARY 块）、Mode 5 审计模板（reference L56-72）完整覆盖三种输出；`## The register` 给出登记簿文件的完整 YAML 结构（L163-234）。若评测器要求字面章节名，属唯一风险点。
- **Scope/Limitations** ⚠️：正文无显式 Scope 节——边界内容分散在 `## Works better connected`（L75-92，能力边界）、`## Important: deadline reference caveat`（L106-120，风险边界）、`## Jurisdiction and type assumptions`（L123-153，法域适用边界）三处，**完整边界清单外置**到 `references/what-this-skill-does-not-do.md`（五条）。规范 §3.1 要求"Every SKILL.md body MUST include these three sections"——reference 文件的内容不满足 body 内必需节的形式要求。这是语料最普遍的规范缺口（dossier 统计约 68% 技能缺 Scope 节）在本技能的具体形态：内容有、位置不对。🟡（修复见 13 节第 2 条）。

### 3.3 委派比例

Mode 5（审计）全文外置（73 行 reference），正文仅保留指令第 6 步一句描述 + Reference Files 索引。审计是五模式之一，约占 skill 功能的 1/5，body 内对应内容约 3 行——委派比例偏高但可接受：body 442 行本身已接近 600 行上限的 74%，Mode 5 是最适合独立成文件的"低频、模板化"模式，且 Instructions 第 6 步（L35-36）已给出六维审计摘要。若评测中 agent 未按索引打开 reference，审计功能会退化为指令摘要——建议在指令第 6 步内联引用文件名（13 节第 8 条，🟢）。

### 3.4 标题层级

H1 → H2 → H3 三级清晰，无跳级。Mode 章节以 `---` 分隔线切分（L72/L155/L244/L293/L344/L385），结构工整。唯一小瑕疵：`## Instructions` 与 `## Examples` 之间的 `---`（L72）与 `## Works better connected` 前无分隔线（L75 直接接 L74 空行），分隔线使用略有不对称（🟢，可忽略）。

### 3.5 600 行上限

442 行 ≤ 600。✅ 余量 26%。若将 Mode 5 迁回正文会逼近上限，维持外置是合理取舍。

## 4. 逻辑一致性深度审查

### 4.1 步骤链

顶层指令（L12-48，8 步）与模式章节的映射：

| 指令项 | 对应章节 | 一致性 |
|---|---|---|
| 1. 读取 plugin CLAUDE.md + 工作流 | Instructions 起头 | ✅ |
| 2. 默认 = --report（90 天窗口、五分组） | Mode 2（L296-341） | ✅ 分组一致（🔴⏰🟡🌐❓） |
| 3. --report [--days N] + 工作产品表头 + 验证收尾 | Mode 2 | ✅ |
| 4. --add 交互式录入 + 自定义规则 | Mode 3（L346-383） | ✅ |
| 5. --update + 后果性行动门槛 | Mode 4（L388-433） | ✅ |
| 6. --audit 六维健康检查 | references/mode-5-audit.md | ✅ 六维与 reference 完全对应 |
| 7. 空登记簿 + IPMS 连接 → Mode 1 | Mode 1（L247-291） | ✅ |
| 8. 护栏提醒（期限仅供参考） | L106-120 caveat | ✅ |

无前向引用、无跳步。SCORING SCOPE-01 的"无旗标即默认报告模式"与指令第 2 步严格一致。

### 4.2 内部矛盾（重点）

**问题一（真实缺陷）：`overdue` 状态在报告分组中无归属。** L237-242 定义 6 值状态枚举（upcoming / due_soon / overdue / grace / lapsed / filed），但 Mode 2 报告模板（L311-337）的分组只覆盖：🔴 LAPSED/IN GRACE、⏰ DUE WITHIN N DAYS、🟡 UPCOMING、🌐 AGENT-MANAGED、❓ UNKNOWN。`overdue`（"past the primary due date, within grace window"）既不属于 🔴（标题仅写 lapsed/grace）也不属于 ⏰（"due" 语义不含已逾期）。同时 `overdue` 与 `grace`（"in the grace period (explicit flag — carries surcharge)"）两个定义几乎重合——同一时间段的资产可被记为两种状态，报告模板又只对 grace 给出归位。后果：PROC-04（状态值使用正确）与 PROC-06（按紧迫度分组）的 LLM judge 遇到 overdue 资产时没有唯一正确行为可判。🟡（修复见 13 节第 3 条）。

**问题二（真实缺陷）：可变报告窗口与固定 90 天状态边界冲突。** L237 定义 `upcoming` = "more than 90 days out"、L238 定义 `due_soon` = "due within 90 days"——状态语义钉死在 90 天上；但 Mode 2（L302）允许窗口取 30/60/90/180。当 `--days 180` 时，一个 150 天后到期的资产：状态是 `upcoming`（>90 天），却在 ⏰ "DUE WITHIN 180 DAYS" 分组里（若分组按到期日与窗口比较）。技能未说明分组依据是"存储的状态值"还是"窗口内的到期日"，agent 与 judge 都会产生歧义。🟡（修复并入 13 节第 3 条）。

**问题三（轻微）：L200 状态注释漏列 `lapsed`。** L200 的 YAML 示例注释写 `# upcoming / due_soon / overdue / grace / filed`（5 值），而 L236-242 的枚举定义是 6 值（含 `lapsed`）。示例注释与权威定义不一致，agent 按注释记忆会漏掉 lapsed 状态。🟢（修复见 13 节第 6 条）。

**问题四（轻微）：Mode 4 无总结要求 vs OUT-04 判分要求。** OUT-04 的问法是"After init **or update**, does the agent show a summary"。Mode 1 有总结模板（L276-291），Mode 4 的 Sub-modes（L419-433）未要求任何总结——更新后 agent 按正文执行不会主动给总结，LLM judge 可能据此扣分。🟢（修复见 13 节第 7 条）。

**问题五（轻微）：`--rebuild` 旗标仅在 Mode 1 正文出现。** L249 "Run when no register exists, or with `--rebuild`"——但 Instructions 8 步与 argument-hint 均未列出，agent 只在进入 Mode 1 场景后才知道该旗标存在。🟢（修复见 13 节第 9 条）。

其余交叉一致性核验通过：Mode 1 Step 2"只存最近两三个期限，远期期限按需计算"（L261-263）与 Mode 2"报告前刷新全部资产期限"（L302-303）不矛盾（存储策略 vs 报告时计算策略）；Mode 3 自定义规则捕获四问（L376-381）与 L150-153"非内置法域 → custom_rules + agent_managed"及 `## The register` 的 `custom_rules:` 块（L177）三处一致；Mode 4 门槛"非律师角色才触发"（L397）与 NEG-01 判分口径一致；handoffs.md 与 description 末句一致。

### 4.3 代码块正确性

- **登记簿 YAML 示例（L163-234）**：结构合法。`metadata`（4 键）、`custom_rules: []`、两个资产示例（TM/PAT）字段齐全，缩进一致，`#` 注释与字段语义匹配。TM 示例的 `next_deadlines` 含 `basis`（"5th-6th anniversary of registration"）与 `action`——与 PROC-01 口径一致；PAT 示例的 `entity_size: "large"` 注释（drives USPTO fees）正确。⚠️ 小瑕疵：L200 状态注释漏 `lapsed`（见 4.2 问题三）；L197 `grace_end: "[YYYY-MM-DD or null]"` 对 TM §8 正确（有 6 个月宽限），PAT 示例 L224 `grace_end: "[YYYY-MM-DD]"` 无 null 备选——与 L139"6-month grace window with surcharge"一致，无问题。
- **命令示例（L52-68）**：5 条 `/ip-legal:portfolio [flags]` 与 argument-hint 及五模式一一对应；`/ip-legal:` 为插件命名空间约定（与 304 同款插件语境）。`--report --days 180` 示例合法。
- **报告模板（L307-339）**：五个分组标题与 L18-19 的简介分组逐一对应；SUMMARY 三行（资产总数/窗口内期限/上次审计）与 L336-338 一致。
- **SCORING.yaml**：YAML 合法；`total_items: 20` 与实际条数核对一致（见第 10 节）；正则 pattern 均为合法 PCRE。

### 4.4 条件完备性（每个 if 都有 else）

- L251-256 Mode 1 数据源三分支（IPMS 连接 / 有表格导出 / 两手空空）：三分支互斥且覆盖全。✅
- L265-270 无法排期资产的二分（未知法域 → custom_rules+agent_managed；缺日期 → unknown+notes）：else 完整。✅
- L396-417 后果性行动门槛（非律师 → 确认后才能 filed；律师/已确认 → 放行）：else 分支完整。✅
- L341 仪表盘 offer（资产 >10 或用户要求时）：有条件无 else——≤10 时静默跳过，合理省略。✅
- **缺失的 else（重要）**：L253、L305、L397、L341 四处无条件引用 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`——工作产品表头（L22-23/L305）、门槛角色判定（L397）、仪表盘 offer 指引（L341）、审计 watch list（mode-5-audit.md L51-54）全部依赖该插件配置文件，且均无"文件不存在时怎么办"的分支。在 SkillIF 评测环境中该路径大概率不存在：工作产品表头无从得知、角色无法判定（门槛静默失效或默认跳过）、watch list 缺数据。这是本技能可执行性最大的单一风险点。🟡（修复见 13 节第 4 条）。

## 5. 参考文件内容级审查

### 5.1 参考完整性矩阵

| SKILL.md 中的承诺 | 对应文件 | 兑现 |
|---|---|---|
| Reference Files 索引（L438-442） | 4 个文件全部 | ✅ |
| "see references/handoffs.md"（L440） | references/handoffs.md | ✅ |
| "see references/integration-ip-renewal-watcher-agent.md"（L441） | references/integration-ip-renewal-watcher-agent.md | ✅ |
| "see references/mode-5-audit.md"（L442） | references/mode-5-audit.md | ✅ |
| "see references/what-this-skill-does-not-do.md"（L443） | references/what-this-skill-does-not-do.md | ✅ |

所有被引用文件都存在，无悬空引用；所有文件都被正文引用，无死文件。

### 5.2 隐形资源审计

skill 目录内无 assets/templates/examples/phases/specs/docs 子目录，无未被正文引用的资源，无隐藏文件（find 确认）。目录外的隐性依赖：① `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`（L253/L305/L397/L341，见 4.4）；② `CONNECTORS.md`（L85/L89，"at the repo root"——插件仓库根目录，正文未说明其在本 skill 目录之外，agent 若在 skill 目录内查找会落空，🟢）；③ `_shared/checker.py`（check.py 的导入，属评测框架文件非本 skill 资源）。均属环境依赖，建议在正文声明（见 13 节第 10 条）。

### 5.3 参考文件逐文件全文审查

**references/mode-5-audit.md（73 行）** — 全文结构：六维审计（deadline hygiene L14-20 / registration gaps L23-30 / use-in-commerce L32-36 / ownership L38-43 / expiration horizon L45-49 / unwatched assets L51-54）+ 输出模板（L56-72）。与 SCORING PROC-10 的问法逐项对应（TM pending >18 个月、专利 pending >4 年、§8 approaching + use_in_commerce: false、owner 不一致、24 个月到期专利、watch list 缺口），与正文 L150-153 的 agent_managed/unknown 语义一致。质量评价：六维结构严谨、每维给出具体检查信号与触发阈值，输出模板的 RECOMMENDED ACTIONS 块给审计收尾以行动出口。**问题**：① L51-54 依赖 CLAUDE.md 的 Brand protection watch list——与 4.4 同源的插件配置依赖；② 无"审计频率建议"（何时该跑审计、与 --report 的差异定位），对 judge 判定 PROC-10 的"audit covers all sections"无影响，但执行层面缺少触发指导（🟢）。

**references/what-this-skill-does-not-do.md（18 行）** — 五条边界：不代写申报、不核验注册局状态、不决定是否续展、不替代多资产 IPMS、不读官方记录。与正文 caveat（L106-120）互为表里，语言克制精准（"A §8 shown as 'filed' here means someone told it so — not that the USPTO accepted it."）。质量高。唯一遗憾是该内容未进正文（见 3.2 与 13 节第 2 条）。

**references/handoffs.md（6 行）** — 接收（prosecution/clearance/assignment recordals）+ 发送（"file §8 now" 触发器给律师）。与 description 末句、SCORING SCOPE-02 的"不代任何动作"口径一致。极简但完整。

**references/integration-ip-renewal-watcher-agent.md（5 行）** — 定时 agent 每周跑 Mode 2 报告并推送频道；🔴 项（grace/lapsed）即时推送。与 Mode 2 分组语义一致。

### 5.4 脚本全文审查

**check.py（85 行）** — 全文功能：`check(workspace, tool_log, agent_output)` 返回 4 项脚本检查——SCOPE-03（output_contains 验证 caveat 相关词）、OUT-01（file_exists `**/portfolio.yaml`）、OUT-02（output_contains 报告头/工作产品/来源短语）、QA-01（tool_log_contains 日期字段与期限基准词）；其余 16 项标注 llm judge、不在此检查。main() 校验 4 参数、读 agent_output 文件、输出 JSON。代码质量：结构清晰、docstring 与实际项数一致（"Run all 4 script-verifiable checks"）、职责单一。**问题**：① **OUT-01 的工作区路径摩擦**（L51）：技能正文 L160/L274 规定登记簿写入 `~/.claude/plugins/config/claude-for-legal/ip-legal/portfolio.yaml`（用户主目录插件配置），而 OUT-01 检查 workspace 下的 `**/portfolio.yaml`——若评测框架不把该配置路径映射进工作区，agent 忠实执行正文必然导致 OUT-01 假阴性失败；若 agent 为迎合检查改写入工作区，则违背技能指令。这是评分设计与技能设计的直接冲突，🟡（修复见 13 节第 5 条）。② **QA-01 的纯报告场景假阴性风险**（L61）：检查 tool_log 含 `registration_date|grant_date|...|next_deadlines`——若 agent 在无现有登记簿时只跑 `--report`（不写文件、日志无日期字段），QA-01 失败；虽有条件性但值得备忘（🟢）。③ `set_agent_output` 在 check() 与 main() 中各调一次（L29-30 与 L77），第二次覆盖第一次，无害但冗余（🟢）。④ 依赖 `../_shared/checker.py`，其 `file_exists` 是否支持 `**` glob 通配在本目录内无法验证——若按字面路径匹配则 OUT-01 恒失败，建议确认（🟢，备注性）。⑤ 无单元测试（🟢，备注性）。

### 5.5 跨 skill 引用

正文以散文名提及 prosecution/clearance 技能（description L3、handoffs.md L3-4），无 `../` 路径，符合"跨 skill 引用用散文名"规范。✅ 引用 `~/.claude/plugins/config/.../CLAUDE.md` 与 `CONNECTORS.md` 为环境/仓库文档，非 skill 文件引用。

### 5.6 死文件

无。四个 reference 全部被正文 Reference Files 节引用，check.py 与 SCORING.yaml 相互一致（4 项脚本检查 ↔ 4 个 script 型 criterion）。

### 5.7 其他资源

无 assets/templates/examples/phases/specs/docs 目录，无其他资源文件。

## 6. 语法与格式质量

### 6.1 拼写

七个文件逐词扫描未发现拼写错误。术语拼写一致：`agent_managed`、`custom_rules`、`next_deadlines`、`use_in_commerce` 在 SKILL.md/SCORING.yaml/check.py/references 中全部一致；`initialise`（英式）在正文与检查中一致使用（Initialise/initialised/initialization），无英美混用。

### 6.2 语法

正文英文语法干净。重点句抽查：L118-120 "A docketed-but-wrong deadline is worse than an undocketed one: it creates false confidence."（冒号递进正确）；L47-48 "do not let the user treat this as the system of record unless the IP management system is sync-integrated."（条件句完整）；L414-417 门槛收尾句无语法问题。未发现病句。

### 6.3 语言混用

七个文件均为纯英文，无中英混排、无中文字符（含全角标点）混入。✅（对照：语料中 306/307 等存在葡语残留，本技能干净。）

### 6.4 Markdown 损坏

无。反引号配对全部为偶数（SKILL.md 154、mode-5-audit.md 30、integration 2，其余 0），无控制字符（逐字节扫描确认无 TAB/CR 混入——304 的公式注入段缺陷在这里不存在），Markdown 表格与代码块围栏完整。`---` 分隔线（6 处）与 em 破折号（正文大量使用 U+2014）风格统一。

### 6.5 未填充占位符

全部占位符均为"有意占位"：`[date]`/`[N]`/`[Company Name]`/`[Asset ID]`（报告与登记簿模板）、`[--report [--days N] | ...]`（argument-hint 语法说明）、`# [comment]`（YAML 示例注释）。无"忘填的空白"型占位符。✅

### 6.6 截断

七个文件均完整收尾，无截断。SKILL.md 以 Reference Files 清单（L442）结束；mode-5-audit.md 以 `---` 收尾（L73）；SCORING.yaml 以 CF-03 的 `cap_to_0` 收尾（L183）。✅

## 7. 规范合规性（SKILL-SPEC v1.0 十二项清单）

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | name：小写+连字符、≤64 字符、匹配目录 | ✅ | `portfolio`，目录前缀 `097-` 为语料序号约定（见 2.1） |
| 2 | description：第三人称 WHAT+WHEN+关键词 | ⚠️ | 三要素齐全（WHAT/WHEN/关键词），但以祈使句 "Track the..." 开头，违反 §2.3 语态 |
| 3 | description 含规定触发信号（五选一） | ⚠️ | 含 "Use when" 但缺 "the user"（"Use when checking..."）；宽松匹配可过，严格匹配落空 |
| 4 | description ≤1024 字符 | ✅ | 314 字符 |
| 5 | 可选字段仅限白名单 | ✅ | name + description + argument-hint（白名单内） |
| 6 | description 无跨 skill 路由 | ✅ | "Receives handoffs from..." 为数据流陈述非路由（附注见 2.2） |
| 7 | Body 含 Workflow/Process | ✅ | Instructions 8 步 + Mode 1-4（L12-433），Mode 5 在 reference |
| 8 | Body 含 Output Format | ✅ | 报告模板/初始化摘要/登记簿 YAML 规格实质性覆盖（无字面标题，附注） |
| 9 | Body 含 Scope/Limitations | ❌ | 边界内容分散于三处 + 完整清单外置 reference，正文无显式 Scope 节 |
| 10 | Body ≤600 行 | ✅ | 442 行 |
| 11 | 文件引用仅限 skill 目录内相对路径 | ✅ | `references/*` 相对路径；插件配置/仓库文档为环境依赖 |
| 12 | 无跨 skill 文件路径（`../`） | ✅ | 跨 skill 引用均为散文名 |

结论：12 项中 10 项通过，2 项为"一词之差/位置问题"级：触发信号短语缺定冠词、Scope 节内容在 reference 而未进正文。整体合规性良好，两项修复合计不到 10 分钟（见第 13 节）。

## 8. 人机感评估

### 8.1 Emoji 审计

全文符号类字符共 6 种、全部功能性：🔴/⏰/🟡/🌐/❓ 五个紧迫度分组标记（各 2 处，仅出现在 L18-19 简介与 L311-329 报告模板中，纯输出规格用途）+ 5 处 `→`（"per CLAUDE.md → Outputs"、"unknown rules → add a stub" 等流程箭头）。零装饰性 emoji、零花哨符号。✅ 在 IP 法律这一高严肃度场景下保持克制，正确（dossier 对 010/043 等功能性标记的处理口径一致）。

### 8.2 全大写喊叫审计

全文零全大写强调：MUST/NEVER/DO NOT 出现次数均为 0。唯一接近强调的是 L415 "Do not set a deadline's `status` to `filed` past this gate without an explicit yes."（句首大写 + 常规长度）。与语料中 153/223 等"喊叫式"技能形成鲜明对比。✅

### 8.3 人设与语气

语气统一：沉稳的 IP 律师助理口吻，行业密度高、金句克制——"A docketed-but-wrong deadline is worse than an undocketed one: it creates false confidence."（L118-119）、"The right deadline is on someone's calendar, tied to the right registration number, in the right jurisdiction."（L100-101）、"This skill maintains that calendar."（L103）。没有空洞客套、没有营销腔。`## Works better connected` 一节诚实说明能力边界（"the register being whatever the lawyer remembers to paste"），而非夸大。

### 8.4 人机边界

边界设计是本技能最强项，五层清晰：
- **不代申报**：L40-46 "it doesn't file anything; it tells the attorney the deadline"（与 what-this-skill-does-not-do.md 呼应）；
- **不核验注册局**：L110-116 caveat 强制 "Always confirm computed deadlines against the USPTO TSDR / Patent Center..."；
- **不决定续展**：L17 与 reference L8-10 "Renewal is a business call"；
- **后果性行动门槛**（L394-417）：非律师角色记录"已申报"前必须与申报律师/注册局确认，否则给出"带什么材料去见律师"的清单（L407-410）——这是语料中 258/212 同级的成熟 gate 设计；
- **状态降级**：L150-153 非内置法域标记 `agent_managed`、"confirm with the foreign associate rather than computing a date this skill doesn't understand"——"宁可承认不知道"的纪律。
第 8 步护栏提醒（L42-48）把"假期限制造假信心"的风险写进了每次输出。✅

### 8.5 代词分析

- description：第二人称 0 次、第一人称 0 次、祈使 1 处（"Track"，见 2.2）。合规关键点通过但语态有小瑕疵。
- Body：`You/you` ×14，全部集中在两类语境——指令语域（"do not let the user treat this..."）与**用户面向脚本**（Mode 3 自定义规则捕获对话 L374-381 "> Let me capture them so we can track this going forward"、Mode 4 门槛对话 L400-413 "> Have you confirmed this with the attorney..."）。用户脚本中的第一人称（I 2 次、we 1 次）是对话引语，符合正文允许的语域（dossier 对 139/144 的用户脚本处理口径一致）。
- references：what-this-skill-does-not-do.md 有 1 处 "someone told it so"（第三人称，无问题）。

### 8.6 表格使用评估

正文 0 张 Markdown 表格——本技能的信息载体是 YAML 规格（登记簿）、输出模板（报告）与编号列表（法域规则），全部是"格式即内容"的场景，不需要表格。SCORING.yaml 的判分结构是唯一"表格化"数据。无任何为装饰而设的表格，符合"知识增量而非冗余"原则。✅

## 9. 可执行性评估

### 9.1 独立可执行性：8.0/10

技能指令本身完备、零歧义：报告/新增/更新/初始化四模式可完全脱离外部系统执行（录入即算期限）。扣分项：① 插件配置 CLAUDE.md 无 fallback（4.4，影响工作产品表头、门槛角色、watch list 三处行为）；② Mode 1 的 IPMS 拉取依赖 MCP 连接（L254，技能已给两分支，降级得当）；③ OUT-01 工作区路径摩擦（5.4 ①，评分层问题）；④ `--rebuild` 旗标传播不完整（4.2 问题五）。

### 9.2 分步可操作性

- Instructions 8 步：🟢 全部可操作，模式路由信号清晰。
- Mode 1：🟢 数据源三分支 + 无法排期资产二分完备；总结模板（L276-291）可直接照抄。
- Mode 2：🟡 五分组模板完整，但分组依据（状态值 vs 窗口到期日）未定义（4.2 问题二），且工作产品表头依赖外部文件（4.4）。
- Mode 3：🟢 十项录入问题清单 + 自定义规则四问脚本，全部可操作。
- Mode 4：🟢 门槛对话脚本完整（含"确认了才放行/未确认带去见律师"两分支），Sub-modes 三例具体。
- Mode 5：🟡 六维检查全在 reference，正文指令第 6 步只有一行摘要——agent 不打开文件则只能输出摘要级审计。

### 9.3 工具依赖

硬依赖：无（核心操作是读写一个 YAML 文件）。软依赖（均有降级分支）：IPMS MCP（Anaqua/CPA Global 等，L80-89）、USPTO 直连（L87-89，尚无 MCP 属 wish list）。环境依赖（无 fallback）：插件 CLAUDE.md ×4 处（L253/L305/L397/L341）、CONNECTORS.md（L85/L89）。整体依赖设计优于多数技能——核心台账功能零硬依赖，问题集中在那个可能不存在的插件配置上。

## 10. SCORING.yaml 交叉参考

### 10.1 标准覆盖度

20 条标准（`total_items: 20` 与实际条数核对一致；类别分布 scope 3 / process 10 / output 4 / negative 2 / qa 1 = 20 ✅；judge 分布 16 llm + 4 script ✅，与 check.py 的 4 项一致）全部能在 SKILL.md 中找到对应内容源：

- SCOPE-01 → Instructions 第 2-6 步 + argument-hint（模式路由）；SCOPE-02 → what-this-skill-does-not-do.md + L106-120 caveat；SCOPE-03（脚本）→ L339 收尾句（含 USPTO/WIPO）。
- PROC-01 → L126-153 法域规则表（TM §8 五至六年、§8/§9 十年、专利 3.5/7.5/11.5 年、Madrid/EUIPO 十年、域名年续）；PROC-02 → L130-137 宽限期规则 + `grace` 状态定义；PROC-03 → L150-153 + Mode 1 Step 2 + Mode 3 custom rules 捕获流；PROC-04 → L236-242 六值状态枚举；PROC-05 → Mode 1 三步 + L276-291 摘要模板；PROC-06 → Mode 2 L302-339；PROC-07 → Mode 3 L352-363 十项；PROC-08 → Mode 4 L394-417 门槛；PROC-09 → Mode 4 Sub-modes "From IP management system sync"（L426-430，"system of record wins" 与 L254 一致）；PROC-10 → references/mode-5-audit.md 六维。
- OUT-01（脚本）→ L160/L274 登记簿路径 ⚠️（工作区摩擦，见 5.4）；OUT-02（脚本）→ L305 表头 + L339 收尾句（pattern 与模板措辞兼容）；OUT-03 → L318-320 basis/agent/docket 行；OUT-04 → 仅 Mode 1 有总结（Mode 4 缺失，见 4.2 问题四）。
- NEG-01 → L415-417；NEG-02 → L126-143 期限基准（grant/registration）。
- QA-01（脚本）→ L186-233 登记簿日期字段 + L222 "3.5-year maintenance fee"（pattern 词可命中）。
- CF-01 → L394-417（门槛绕过 → 封顶 0）；CF-02 → 期限基准错误（L126-143）；CF-03 → 无验证收尾（L339/L106-120）。

LLM judge 问题措辞（如 PROC-10 的 "TM applications pending over 18 months, patents over 4 years"）与 reference 阈值逐字一致，设计良好。**覆盖缝隙**：① OUT-04 的 update 场景无正文依据（4.2 问题四）；② 没有任何标准检查 `overdue` 状态的分组归位（4.2 问题一），PROC-04/06 判分遇 overdue 无唯一解；③ OUT-01 路径摩擦（5.4 ①）——三处缝隙全部是"正文/评分设计"层而非技能内容层。

### 10.2 关键失败分析

CF-01（未过门槛记录 filed → 封顶 0）是整套测评的命门，与技能最重的设计投资（后果性行动门槛）互为表里——测评把最大权重放在技能最强调的安全规则上，这是正确的测评设计。CF-02（期限基准错误）与 CF-03（无验证收尾呈现权威期限）同样对应技能的核心护栏。三处 critical_failures 均有明确的正文依据，且与 SCOPE-02/NEG-01/NEG-02 形成"负面标准 + 关键失败"的双层防护。**执行风险**：CF-01 依赖 LLM judge 判断"agent 是否在非律师角色下未经确认即记录 filed"——若 judge 不实际检查 agent 是否读取了插件 CLAUDE.md（评测环境中该文件不存在，角色判定本身就是问题），CF-01 的判定会漂移——这是插件配置依赖（4.4）在评分层的连锁效应。

## 11. 已知问题汇总

**Dossier 交叉核对**：全局质量档案（`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`）中 097 无独立条目——批组 076-100 以组条目 "093-data-privacy-compliance — 100 系列" 合并记录，评级 🟢 "整体为坚实合规内容"，且批组统计为 "🔴 0 / 🟠 4 / 🟢 8"。组条目主要反映的是该批数据合规/模板类技能，对 097 仅能提供组级参考。本审查的独立评级为 **🟡 B+（85.5/100）**——与组级 🟢 方向一致（内容扎实、无致命问题），但按 SKILL-SPEC 十二项清单逐项核对时，正文缺显式 Scope 节与 description 两处措辞偏差使其达不到"完全合规"档（组条目"大部分三节齐全或接近齐全"的表述与本结论吻合）。

**No-trigger 对照集**：`complex-skills-no-trigger\097-portfolio\SKILL.md` 与主版本仅 description 不同（删去触发句，保留 "Track the IP portfolio — registrations, renewals, maintenance fees, and use declarations."）——对照集 description 恰好规避了主版本的两处缺陷（无祈使冲突？不——对照集同样以 "Track" 祈使开头，且完全无触发信号），属于有意的触发对照设计；主版本修复描述时需注意保持对照集的可比性。

**本审查发现的问题**已在本报告 2.2、3.2、4.2、4.4、5.4、9、10 各节完整记录，第 13 节按优先级汇总。

## 12. 综合评分

八维加权评分如下（每维先给 10 分制小分，再按权重折算）：

| 维度 | 权重 | 得分 /10 | 加权 | 核心理由 |
|---|---|---|---|---|
| Frontmatter | 10% | 8.5 | 0.85 | 结构合法、314 字符；祈使开头 + 触发短语缺 "the user" 两处措辞偏差 |
| Body | 10% | 8.5 | 0.85 | 五模式结构完整、模板详尽；正文缺显式 Scope 节、Mode 5 全文外置 |
| Logic | 20% | 8.0 | 1.60 | 无硬矛盾；overdue 分组无归属、状态/窗口语义分歧、L200 注释漏 lapsed |
| References | 15% | 9.0 | 1.35 | 4/4 存在且被引用；mode-5-audit 覆盖 PROC-10 六维；无死文件无控制字符 |
| Grammar | 10% | 9.5 | 0.95 | 零拼写错误、零 Markdown 损坏、英式拼写一致 |
| Compliance | 15% | 8.3 | 1.25 | 12 项过 10 项；触发短语与正文 Scope 节两项均为"一词/位置"级偏差 |
| Human-feel | 10% | 9.5 | 0.95 | 语域克制、emoji 全功能、五层人机边界是语料顶级设计 |
| Executability | 10% | 7.5 | 0.75 | 指令完备；插件配置 ×4 无 fallback + OUT-01 路径摩擦是主要扣分点 |

**总分：85.5 / 100 → 🟡 B+**

评级解读：B+ 级属于"高质量、接近语料一线水准、有明确改进空间"档位。所有扣分点均为措辞级或评分设计级，可在 1 小时内修复完毕（见第 13 节）：修复后预计可达 92+ 进入 A 档，与 dossier 中 068-deadlines（同 IP 期限域技能）同属"逻辑闭环完整"档位。本技能的核心设计——五层人机边界（不代申报/不核验/不决定/后果性门槛/状态降级）配以"期限仅供参考"的强免责纪律——是 process 型法律技能中少见的成熟设计，caveat 一句 "A docketed-but-wrong deadline is worse than an undocketed one" 的准确性甚至超出多数同类商用工具。

## 13. 修复建议（重点章节）

### 🔴 致命问题

**无。** 未发现会导致测评失败、产线事故或严重事实错误的缺陷。最接近致命的是下述第 1-2 条（description 两项措辞，会导致严格合规检查 ❌），但均为分钟级修复；第 5 条（OUT-01 路径摩擦）是评分设计层问题，属最高优先级的结构性修复。

### 🟡 重要问题（建议全部修复，合计约 40 分钟）

**1. description 祈使开头 + 触发短语缺定冠词** — `SKILL.md:3`。改为第三人称且与规范触发信号对齐：

> Tracks the IP portfolio — registrations, renewals, maintenance fees, and use declarations. Use when the user checks what's renewing, adds or updates an asset, records a maintenance filing, or audits the register for gaps, lapses, and use-in-commerce questions. Receives handoffs from prosecution and clearance work.

- 改动要点：① "Track the IP portfolio" → "Tracks the IP portfolio"（§2.3 语态，与语料多数技能的名词短语/第三人称开头对齐）；② "Use when checking what's renewing, adding or updating..." → "Use when the user checks..., adds..., records..., or audits..."（§2.4 规范信号 + 动词平行）。
- 影响：合规十二项清单第 2、3 项从 ⚠️ 转 ✅，消除严格匹配器判负的唯二 description 风险。
- 副作用提示：对照集 `complex-skills-no-trigger\097-portfolio` 的 description 需同步更新首句（否则对照集与主版本失去可比性——见第 11 节）。
- 工作量：5 分钟。

**2. 正文补 Scope 节** — `SKILL.md:92`（`## Works better connected` 之后，或 `## Reference Files` 之前）。将 references/what-this-skill-does-not-do.md 五条浓缩为正文小节：

```
## What this skill does not do

- Does not file anything — surfaces deadlines for the attorney to execute.
- Does not verify deadlines against any registry — computes them from dates
  you provide; the registry is the source of truth.
- Does not decide whether to renew — that is a business call.
- Does not replace an IP management system for large portfolios.
- Does not read office records to confirm status.

Full list with rationale: see references/what-this-skill-does-not-do.md.
```

- 影响：满足 §3.1 第三必需节"body 内"的形式要求，合规十二项清单第 9 项从 ❌ 转 ✅；同时消除"评测器只扫正文不扫 reference"的 Scope 判负风险。reference 全文保留（详细版仍在那里）。
- 工作量：5 分钟。

**3. `overdue` 状态归位 + 报告分组依据澄清** — `SKILL.md:237-242` vs `311-337`。二选一，推荐方案 A：
- **方案 A（推荐）**：Mode 2 报告模板 🔴 组标题改为 `🔴 LAPSED / OVERDUE / IN GRACE ([N])`，并在模板前的分组说明（L302-303 附近）加一句："Group by each asset's due date relative to the report window, not by its stored status; `filed` and assets outside the window are not listed."——同时把 4.2 问题二的窗口歧义一并解决（分组依据显式化：按窗口比较，而非按固定 90 天的存储状态）。
- **方案 B**：合并 `overdue` 与 `grace` 为一个状态（`grace`，保留 surcharge 旗标字段），枚举缩为 5 值。改动面更大（SCORING PROC-04 问法含 overdue，需同步），不推荐。
- 影响：PROC-04/PROC-06 的 LLM judge 获得唯一正确行为依据；消除状态枚举与报告分组之间的逻辑缺口。
- 工作量：10 分钟。

**4. 插件配置缺失的降级分支** — `SKILL.md:253`、`L305`、`L397`、`L341`。在 Instructions 第 1 步（L14-15）后加降级句：

> If `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md` does not exist: skip the work-product header and the dashboard/watch-list offers, and apply the consequential-action gate as if the role were non-lawyer (default to the cautious path).

- 影响：消除 4 处环境依赖的静默降级——工作产品表头（OUT-02 受影响）、门槛角色判定（PROC-08/CF-01 受影响）、仪表盘 offer、审计 watch list（PROC-10 受影响）全部获得确定行为。独立可执行性 8.0 → 9.3。
- 工作量：5 分钟。

**5. OUT-01 工作区路径摩擦** — `SCORING.yaml:120`（`path: "**/portfolio.yaml"`）+ `check.py:51` + 正文 `SKILL.md:160/L274`。技能规定登记簿写入插件配置路径（用户主目录），检查器却在工作区找文件。三选一，推荐 ①：
- ① 评测框架将 `~/.claude/plugins/config/claude-for-legal/ip-legal/` 映射为 workspace 子路径（如 `workspace/.plugin-config/`），并在技能正文 Mode 1 Step 3（L274）注明"评测环境下登记簿写入工作区 `.plugin-config/` 镜像"——保持正文单一路径，由框架负责映射。
- ② check.py 的 OUT-01 改为宽匹配（同时在 workspace 与配置路径查找）。
- ③ 正文 Mode 1 Step 3 加"同时在工作区保存一份镜像副本"——改动最小但让 agent 写两份文件，与"系统权威单一"理念略冲突。
- 影响：消除 20 项标准中唯一可能因路径设计而假阴性的脚本检查（OUT-01 占 5% 权重，且属 output 类最易判的硬检查）。
- 工作量：10 分钟（需与评测框架协调，属评分设计层）。

### 🟢 优化问题（按性价比排序，合计约 20 分钟）

**6. L200 状态注释补 `lapsed`** — `SKILL.md:200`。`# upcoming / due_soon / overdue / grace / filed` → `# upcoming / due_soon / overdue / grace / lapsed / filed`，与 L236-242 六值定义一致。影响：消除示例注释与权威枚举的偏差（4.2 问题三）。工作量：1 分钟。

**7. Mode 4 补更新总结** — `SKILL.md:433`（Sub-modes 末尾）。加一行："After each update, show a one-line summary — asset ID, what changed, and the next deadline in that asset's lifecycle."影响：OUT-04 的 update 场景获得正文依据（4.2 问题四）。工作量：3 分钟。

**8. Instructions 第 6 步内联指向审计文件** — `SKILL.md:35-36`。在 "--audit: Mode 5" 一句后补 "（详见 references/mode-5-audit.md）"。影响：降低 agent 漏开审计 reference 的概率（3.3）。工作量：1 分钟。

**9. argument-hint 补 `--rebuild`** — `SKILL.md:4`。`"[--report [--days N] | --add | --update | --audit]"` → 追加 `| --rebuild`（与 Mode 1 L249 对齐）。影响：消除旗标传播缺口（4.2 问题五）。工作量：1 分钟。

**10. CONNECTORS.md 位置说明** — `SKILL.md:85/L89`。"see CONNECTORS.md at the repo root" → "see `CONNECTORS.md` at the plugin repository root (outside this skill directory)"。影响：防止 agent 在 skill 目录内空找（5.2）。工作量：1 分钟。

**11. description 的 handoff 句评估器兼容** — `SKILL.md:3`。保留原句即可，但建议在评测说明中注明该句为数据流陈述、非 §2.5 禁止的路由；若严格审查器不接受，删去该句并依赖 references/handoffs.md（内容已完整，零信息损失）。工作量：1 分钟（决策）。

**12. 报告模板分组标题措辞统一** — `SKILL.md:316`。"⏰ DUE WITHIN [N] DAYS" 与 L18 简介 "due within window" 统一（可保留现状，L18 的 "window" 指代上一行的 90 天窗口）。属于可改可不改项，列此仅为完整。工作量：1 分钟。

**13. check.py 备忘注释** — `check.py:51`。在 OUT-01 检查前补一行注释说明 `**/portfolio.yaml` 的 glob 语义假设（依赖 `_shared/checker.py` 的 file_exists 实现，若为字面匹配则恒失败）与 workspace 映射约定（联动修复 5）。影响：可审计性。工作量：5 分钟。

**工作量汇总**：🟡 5 项约 35 分钟 + 🟢 8 项约 15 分钟 ≈ **50 分钟**。若只修 🟡 1-4 项（约 25 分钟），合规十二项清单即可全绿、执行性 8.0 → 9.3；连同第 5 项（评分设计层）一起修，综合评分预计从 85.5 提升至 92+ 进入 A 档。按语料惯例（dossier：322 技能中约 68% 缺 Scope 节、35 个 description 语法违规），本技能两项合规偏差均属语料中"最普遍、最易修"的类型，修复后可作为 IP 期限管理类 process 技能的参照样本。

## 附录: 审查过程记录

**读取文件清单**（全部完整读取，无抽样）：

1. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\SKILL.md` — 442 行
2. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\SCORING.yaml` — 183 行
3. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\check.py` — 85 行
4. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\references\handoffs.md` — 6 行
5. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\references\integration-ip-renewal-watcher-agent.md` — 5 行
6. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\references\mode-5-audit.md` — 73 行
7. `D:\SkillIF\skill-experiment\complex-skills\097-portfolio\references\what-this-skill-does-not-do.md` — 18 行

**合计读取 812 行**（目录全量 7/7 文件，含隐藏文件检查确认无遗漏）。

**辅助核验文件**：`_shared\SKILL-SPEC.md`（161 行，规范全文）；`C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`（1203 行，dossier 全文，重点核对批组 076-100 与汇总统计）；`complex-skills-no-trigger\097-portfolio\SKILL.md`（diff 比对，确认仅 description 差异）。

**辅助核验命令**：wc -l 行数统计（7 文件 812 行）；Python yaml.safe_load 验证 frontmatter 与 SCORING.yaml 结构（20 条 = total_items 20、judge 分布 16 llm + 4 script、CF 3 条）；description 长度计算（314 字符）；控制字符逐字节扫描（0 处）；反引号配对奇偶检查（全部偶数）；emoji/符号审计（6 种符号 × 2 处，全部功能性）；代词/全大写统计（You 0、you 14、MUST/NEVER 0）；grep -n 定位全部标题与关键句行号。

**审查范围边界**：本审查仅限 skill 目录内 7 个文件 + 上述辅助文件；`_shared/checker.py` 位于 skill 目录之外，其 `file_exists`/`output_contains` 的 pattern 语义（glob/正则）无法在目录内验证，已在 5.4/13 节以备注形式标注。插件配置路径 `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md` 在本机是否存在未验证（评测环境判定为大概率不存在，见 4.4）。
