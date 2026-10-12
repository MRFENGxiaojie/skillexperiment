# REVIEW — 243-ai-inventory（EU AI Act 人工智能系统清单管理 Skill）

- 审查日期：2026-08-06
- 审查范围：D:\SkillIF\skill-experiment\complex-skills\243-ai-inventory\ 目录下全部 3 个文件，并对照阅读共享依赖 _shared\ 下 3 个文件（checker.py、CHECKER-LIBRARY.md、SKILL-SPEC.md）以核实脚本检查语义。
- 审查方法：Glob 枚举全部文件 → 逐一完整 Read → 逐条对照 SKILL-SPEC v1.0、CHECKER-LIBRARY 与 EU AI Act 知识库核查。
- 评级摘要：SKILL.md 本体 [优]；SCORING.yaml [良]；check.py [中]（含一个确定性缺陷）；综合评级 [良]（详见第十三节）。

---

## 一、概述与文件清单

本 Skill 面向法律实务场景：在 EU AI Act 框架下维护"每系统"粒度的 AI 系统清单（inventory）。核心设计主张是 **role（角色）与 tier（风险等级）按系统而非按公司评定**——同一机构可同时是系统 A 的 provider、系统 B 的 deployer、系统 C 的 importer，各自触发不同义务组合。Skill 只做登记与分类引导，明确拒绝从硬编码的 role x tier 表派生义务，义务分析留给对话内进行并以 `[verify]` 标签交还律师核验。

| # | 文件 | 行数 | 角色 |
|---|------|------|------|
| 1 | SKILL.md | 246 | 技能主体：流程、清单格式、分类工作流、记录格式、护栏 |
| 2 | SCORING.yaml | 139 | 评测标准：14 项 criteria + 3 项 critical_failures |
| 3 | check.py | 70 | 脚本检查：4 项 script judge 的确定性实现 |
| 4 | _shared/checker.py（上下文） | 351 | check.py 依赖的检查函数库（已核实语义） |
| 5 | _shared/CHECKER-LIBRARY.md（上下文） | 187 | 函数库文档（已核实与实现一致） |
| 6 | _shared/SKILL-SPEC.md（上下文） | 162 | 语料规范 v1.0（合规性判据） |

目录结构极简（3 个文件），无 references/ 或 scripts/ 子目录。SKILL.md 体量 246 行，符合 process 模式 ~200 行的目标区间，远低于 600 行硬上限。

---

## 二、元数据（Frontmatter）审查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| `name: ai-inventory` | [通过] | 小写 + 连字符，<=64 字符；与目录名 243-ai-inventory 的 NNN- 前缀剥离后一致 |
| `description` 存在 | [通过] | 第三人格陈述，见第三节详析 |
| `argument-hint` | [通过] | `[list \| add \| edit <id> \| classify <id> \| show <id>]`，属允许的可选字段，且与正文 dispatch 分支一一对应 |
| 禁止字段 | [通过] | 无 metadata/license/version/trigger 等任何 §1.3 禁止键，仅有 name/description/argument-hint 三个白名单字段 |
| 目录命名 | [通过] | NNN-kebab-case，无空格、无大写 |

Frontmatter 干净合规。唯一可挑剔之处：`argument-hint` 中 `edit <id>` 的 `edit` 含义（单字段修改）在正文中有说明，提示本身不携带该语义，但这是可选字段，无碍。

---

## 三、描述与触发词审查

描述原文（L3）：

> EU AI Act per-system inventory — track each AI system's role (provider, deployer, importer, distributor, authorized representative, product manufacturer) and risk tier (prohibited, high-risk, limited, minimal, GPAI, GPAI+systemic). Role and tier are assessed per system, not per company. Use when the user says "ai inventory", "add an ai system", "what systems do we have", "classify this ai system", "eu ai act register", or "ai system registry".

| 检查项 | 结果 | 说明 |
|--------|------|------|
| WHAT | [通过] | 明确说明"维护 EU AI Act 下的按系统粒度清单（角色 + 风险等级）" |
| WHEN | [通过] | 6 组带引号的用户触发短语，覆盖 list / add / classify / register / registry 场景 |
| KEYWORDS | [通过] | ai inventory、eu ai act register、ai system registry、provider/deployer/classify 等 |
| 第三人称 | [通过] | 无 imperative / first-person / second-person 开头 |
| 触发信号 | [通过] | "Use when the user says ..."，含规范 §2.4 要求的 "Use when the user" 触发前缀 |
| 长度 | [通过] | 约 420 字符，<=1024 |
| 交叉路由 | [通过] | 描述内无 "NOT for X, use Y instead" 式路由 |

说明两点：
1. 触发信号采用 "Use when the user says" 变体，规范 §2.4 清单中列的是 "Use when the user..." 系，该写法以 "Use when the user" 开头，应判通过，但严格比对时属边界写法，可在触发词列表里再补一个 "Triggers on" 或 "Use when the user asks to" 更稳妥。
2. 描述中 role 的 6 个枚举与 tier 的 6 个枚举与正文 Step 1/Step 2 及记录格式注释完全一致，描述与正文高度自洽。

---

## 四、正文结构与流程审查

### 4.1 章节构成

| 章节 | 行号 | 职能 |
|------|------|------|
| ## When this runs | L8-16 | 触发场景与核心主张（按系统评定） |
| ## What to do | L18-49 | 主流程：读配置 → 读清单 → 参数分发 → 仪表盘邀约 → 收尾钩子 |
| ## List format | L51-61 | 表格渲染规范 |
| ## Add flow (interview) | L63-81 | 新增访谈流程 |
| ## Classification walk-through | L83-194 | 角色/等级分类工作流（三步） |
| ## Record format | L196-216 | YAML 记录格式（16 字段示例） |
| ## Why this skill does NOT auto-derive obligations | L218-232 | 不自动派生义务的设计理由 |
| ## Guardrails | L234-245 | 四条负面护栏 |

### 4.2 流程评价

- **分发逻辑清晰**：L30-38 的 dispatch 覆盖无参/list、add、edit <id>、classify <id>、show <id> 五种分支，与 argument-hint 完全对应；每个分支指向明确的子流程。
- **前置读取有明确顺序**：L20-23 先读 `~/.claude/plugins/config/claude-for-legal/ai-governance-legal/CLAUDE.md`，缺失或含 `[PLACEHOLDER]` 时转 cold-start-interview；L25-28 再读 ai-systems.yaml，缺失时在首次 add 时以空 `systems:` 创建。与 SCORING SCOPE-02 的语义吻合。
- **EU nexus 判定**：L75-77 给出三分支判定（部署于 EU/EEA、面向 EU/EEA 用户、输出影响 EU/EEA 人群），正确。
- **收尾钩子**：L44-49 规定每次写入后输出固定话术，含"不查表、对话内走义务分析、标注需律师核验"三要素。

### 4.3 流程层问题（详见第十三节）

1. **边界用例未覆盖**：对不存在的 id 执行 edit/classify/show、清单文件缺失时执行 list、重复 add 同名系统等均未定义行为；L26-28 只规定了"首次 add 时创建文件"，list 在文件缺失时的行为是隐式的。
2. **新增记录的可选字段默认值未定义**：Add flow 只收集 5 个必填字段（L65-67），role/tier/obligations_assessed 等其余字段在"稍后补充"语义下应写入何种默认值（缺省不写？null？）未说明，可能导致 OUT-01 字段完整性检查的误判。
3. **"Close every action" 与 "After any write" 的边界**：L44 说 "Close every action with a hook"，L45 紧跟 "After any write, say:"，纯 list（无写入）时是否必须出钩子话术存在二义，直接影响 OUT-02 的 LLM 判定。

---

## 五、分类工作流与领域知识审查（EU AI Act 准确性）

这是本 Skill 的知识核心，逐项对照 EU AI Act（Reg (EU) 2024/1689）现行文本核查：

### 5.1 角色判定（Step 1, L90-117）

| 角色 | L96-108 给出的判据 | 对照 Art. 3 定义 | 结论 |
|------|--------------------|------------------|------|
| Provider | 开发（或委托开发）并以自己名义投放市场/投入使用 | Art. 3(3) | 一致 |
| Deployer | 在自己权限下使用，排除个人非专业使用 | Art. 3(4) | 一致 |
| Importer | 将非 EU 提供者的系统引入 EU | Art. 3(6) | 一致 |
| Distributor | 不属提供者/进口者的市场供应 | Art. 3(7) | 一致 |
| Authorized representative | 代表非 EU 提供者在 EU 设立 | Art. 3(8) | 一致 |
| Product manufacturer | 将 GPAI/其他 AI 系统嵌入产品并以自己名义投放 | Art. 25(1)(b) 之产品制造者规则 | 一致 |

双角色标记（L110-115）：微调、改用途、贴牌即可触发 provider 身份转换的提示，正确引用 Art. 25 与 substantial modification 概念，并带 `[verify]` 标签——处理得当。

### 5.2 等级判定（Step 2, L119-185）

判定顺序（A 禁止 → B 高风险 → C GPAI → D 有限 → E 最低）与 AI Act 义务结构的适用顺序一致，也与此 Skill 自己的 SCORING PROC-05 一致。

- **A. Art. 5 禁止实践（L126-145）**：8 条清单逐条对照 Art. 5(1)(a)-(h)：潜意识/欺骗性技术、利用脆弱性、社会评分、执法场景实时远程生物识别（注明狭窄例外）、敏感特征生物识别分类、工作场所/教育场景情绪识别（注明医疗与安全例外）、面部图像抓取、仅凭人格特征的预测性警务——**8 条全部对应正确**，且明确注明"summaries, not definitive text"并带 `[verify]` 标签，规避了法条转述漂移风险。
- **B. Annex III 高风险领域（L147-168）**：8 大领域（生物识别、关键基础设施、教育、就业、必要公共服务、执法、移民庇护、司法与民主进程）与 Annex III 第 1-8 点对应正确，且示例记录（L209）引用了 Annex III(4)(a) 就业/招聘筛选，引用精确。注意 Annex III 第 1 点生物识别类目存在分阶段生效调整，Skill 以 verify 标签兜底，合理。
- **C. GPAI（L170-176）**：累计算力 10^25 FLOPs 阈值与 Art. 51 及 (EU) 2024/1779 实施细则一致。
- **D. 有限风险（L178-180）**：聊天机器人、深度伪造、Art. 5 范围外的情绪识别/生物识别分类，对应透明义务，正确。
- **E. 最低风险（L182）**：兜底，正确。

### 5.3 时间线表述

L229 "the AI Act is phasing in through 2027" 准确：一般适用 2026-08-02 已生效，Annex III 高风险义务延续至 2027-08-02。审查日恰为 2026-08-06，该表述仍成立。

### 5.4 领域知识层发现

1. **tier 枚举 token 未在 walk-through 中显式定义**：记录格式注释（L208）给出 `gpai` / `gpai_systemic` 两个枚举值，但 Step 2C（L170-176）只用自然语言说 "GPAI" 与 "GPAI + systemic risk"，未明确要求写入 `gpai` / `gpai_systemic` token。agent 可能写出 `gpai_plus_systemic` 之类的变体，导致后续查询与评分不稳定。建议在 Step 2 补一行"write the exact token: `gpai` 或 `gpai_systemic`"。
2. **role 枚举 token 同理**：L206 注释给出 `authorized_rep`，Step 1 选项写作 "Authorized representative"，未显式对应 token。两处建议统一给出"写出字段时使用的精确枚举值"清单。

---

## 六、输出格式与记录格式审查

### 6.1 List 输出（L51-61）

紧凑表格列定义（ID/Name/Owner/Status/EU nexus/Role/Tier/Next review）与 SCORING PROC-07 完全一致；表下要求等级计数与 "N systems flagged for review within 30 days" 行，可操作性明确（由 next_review 日期与当日差值计算）。表格示例数据（L57-58）两个系统字段完整、值符合枚举。示例中 sys-001 的 next_review 为 2026-08-01，处于审查日之前，作为示例数据无问题。

### 6.2 记录格式（L198-215）

- 16 个字段齐全：id/name/owner/description/status/eu_nexus/role/role_basis/tier/tier_basis/obligations_assessed/obligations_note/next_review/review_trigger/created/updated，与 SCORING OUT-01 的描述一致。
- status 与 role 与 tier 的枚举注释齐全（L204/206/208），role_basis/tier_basis 的 verify 标签示例（L207/209）示范了正确写法。
- `obligations_note`（L211）示例直接给出 deployer + high_risk 的 Art. 26 义务摘要并带 verify 标签，示范性良好。

### 6.3 输出层问题

1. **Add flow 与记录格式的字段衔接缺失**：Add flow（L65-67）收集 5 个必填字段后，role/tier/obligations_assessed 等 11 个可选字段在暂不分类时如何写入（缺省、null 或不写）未定义（见第四节问题 2）。
2. **"Verify" 标签的语法一致性**：SKILL.md 正文统一使用 `[verify against current AI Act text]`（L114、L126 等），但 L207/209/211 的记录示例中该标签嵌入带引号字符串内部，agent 抄写时若落到字符串外或双引号转义不全会破坏 YAML 可解析性——建议在 Record format 中加一句"标签写在字符串值内，保持双引号包裹"的提示。

---

## 七、范围、限制与护栏审查

- **"Why this skill does NOT auto-derive obligations"（L218-232）**：清晰声明"清单不含硬编码 role x tier 义务表；义务在对话内分析并带 [verify]；正式记录路由到 aia-generation"，并给出三条设计理由（映射复杂且在变、错而无信会进董事会备忘录、清单是给律师的登记簿）。这是本 Skill 最鲜明的设计立场，理由成立。
- **Guardrails（L234-245）**：四条护栏均为"NEVER"式负面规则且附理由——不静默分类、verify 标签不许删、实质修改必提示重分类、不许查表宣示义务——符合规范 §3.4 的 anti-patterns over generic advice 要求。

### 范围层问题

1. **缺少显式 Scope/Limitations 标题**：规范 §3.1 要求三类必备章节（Workflow / Output / Scope）。本 Skill 的 Workflow（## What to do）与 Output（## List format / ## Record format）均显式存在，但 Scope 章节是隐式的——"Why this skill does NOT auto-derive obligations"与 Guardrails 覆盖了主要的"不做"内容，但没有一句"本 Skill 不做：法律意见、义务的最终判定、提交监管机构或备案"之类的显式范围声明。建议补一个 ## Scope / Limitations 小节，把"不做什么"集中陈述。
2. **命令名不一致**：L192 写作 `/ai-governance-legal:aia-generation`，L244 写作 `/aia-generation`；L68 写作 `/ai-governance-legal:ai-inventory classify <id>`，L241 写作 `/ai-inventory classify`。同一命令两种前缀写法并存，agent 按字面复述时会输出不一致的路由。建议统一为全限定名。
3. **外部绝对路径依赖**：配置与清单路径硬编码为 `~/.claude/plugins/config/claude-for-legal/...`（L21、L26）。这是"注册表存于技能目录之外"的设计决策（数据由用户侧插件配置目录管理，属合理），且对缺失场景有兜底（转 cold-start-interview）。但需注意：评测沙箱若未铺设该插件配置，SCOPE-02 / PROC-06 / OUT-01 三类脚本检查将因文件缺失而全数失败。建议在 SKILL.md 中加一句"若配置目录不存在，明确告知用户这是 claude-for-legal 插件环境"。

---

## 八、SCORING.yaml 评分标准审查

### 8.1 结构统计

- `pattern: process`、`total_items: 14`；criteria 分类：scope 2 + process 7 + output 2 + negative 3 = 14，**计数准确**。
- critical_failures 3 项（CF-01 静默分类、CF-02 查表宣示义务、CF-03 缺 EU nexus 或未带 verify 基准确认），effect 均为 cap_to_0，且三者与 Guardrails 一一对应，是"负面护栏→临界失败"的直接映射，设计逻辑闭环。

### 8.2 逐项质量

| ID | 判定 | 评价 |
|----|------|------|
| SCOPE-01 | LLM | 问题聚焦于"开场是否定位为清单管理"，可判性良好 |
| SCOPE-02 | 脚本 | 见 8.3-1 |
| PROC-01 | LLM | 五个分支行为捆绑在一个问题里，任一分支偏差即整项不通过；建议拆分或注明"任一分支按规范执行即可" |
| PROC-02 | LLM | 五个必填字段 + ID 格式 + 可延迟说明捆绑，同 PROC-01 的捆绑问题 |
| PROC-03 | LLM | 精确对应 Step 1 判据，好 |
| PROC-04 | LLM | 精确对应双角色标记，好 |
| PROC-05 | LLM | 等级判定顺序与 SKILL.md 逐字一致，好 |
| PROC-06 | 脚本 | 见 8.3-2 |
| PROC-07 | LLM | 列名清单与 SKILL.md L55 完全一致，好 |
| OUT-01 | 脚本 | 见 8.3-3 |
| OUT-02 | LLM | 与 L44-49 收尾钩子对应；注意 4.3-3 的"无写入动作"歧义 |
| NEG-01 | LLM | 对应 Guardrails 第一条，问题构造得当 |
| NEG-02 | LLM | 对应 Guardrails 第三、四条，好 |
| NEG-03 | 脚本 | 见 8.3-4 |

### 8.3 脚本检查项缺陷

1. **SCOPE-02（L19-25 + check.py L33）**：`tool_log_contains('ai-governance-legal')` 是子串匹配，命中任何包含该串的工具调用（哪怕是 grep 一下路径、列出目录）即通过；既不验证"先读配置再读清单"的顺序，也不验证 [PLACEHOLDER] 分支与 cold-start-interview 指引（描述中明明写了这一要求）。属弱代理检查。可用 `tool_log_read_before_write` 或更精确的路径正则（如 `config/claude-for-legal/ai-governance-legal/CLAUDE\.md`）增强。
2. **PROC-06（L68-75）**：`pattern: 'role_basis:.*\\[verify'` 是 **YAML 单引号字符串，反斜杠为字面量**，实际正则等价于"role_basis: + 任意字符 + 字面反斜杠 + [verify"，要求记录里在 [verify 前存在一个反斜杠，**永远不会命中**（正常记录是 `role_basis: "..." [verify ...]`）。若评测器直接按 SCORING.yaml 的 pattern 调用 checker，本项恒失败；只有执行 check.py 时（其中 Python 字符串字面量 `'role_basis:.*\\[verify'` 正确转义为 `\[`）才能通过。两份文件的 pattern 语义不一致，是真实缺陷（详见第十节）。
3. **OUT-01（L87-94）**：描述声称检查全部 16 个字段，实现却只查 `review_trigger:` 一个键（check.py L41）。一条缺了 15 个字段、只含 review_trigger 的记录也能通过；且 `review_trigger` 出现在注释里也会误判通过。建议改为逐一检查关键字段（如 obligations_assessed、updated、tier_basis）或多个 pattern。
4. **NEG-03（L120-126）**："不剥离 verify 标签"是负面准则，实现却是正向断言"输出必须包含 [verify] 文本"。纯 list 场景（无分类、无义务分析）的输出天然不含该标签，会误判失败。且存在 8.3-2 的同款转义问题（YAML 里 `'\\[verify ...\\]'` 要求字面反斜杠）。加上 check.py 的覆盖 bug（见第九节），本项在脚本路径上**恒为 False**。

### 8.4 其他

- L6 注释定义 `${PRACTICE_CFG}` 但全文件从未使用，属死变量；L7 的 `${INVENTORY}` 在 PROC-06/OUT-01 的 path 中使用。
- 14 项中 10 项依赖 LLM judge，脚本只覆盖 4 项，LLM judge 的 prompt 质量总体良好，但 PROC-01/PROC-02 的捆绑问题会放大 judge 主观性。

---

## 九、check.py 脚本审查

### 9.1 结构

70 行，结构清晰：imports → check() → main()。docstring 标注调用方式 `python check.py <workspace> <tool_log> <agent_output>`，main 正确处理了 agent_output 文件读取（L59-61）并输出 JSON 结果（L66）。文件读取均带 encoding="utf-8"。

### 9.2 缺陷清单

1. **[P0] NEG-03 恒 False 的覆盖性 bug（L21-22 + L59-61）**：
   - main() 先读取 agent_output 文件内容并 `set_agent_output(f.read())`（L59-61）；
   - 随后调用 check(workspace, tool_log, agent_output)，而 check() 第一行就执行 `set_agent_output(agent_output)`（L22）——这里的 agent_output 是**第三个 CLI 参数（文件路径字符串）**，把刚设置的文件内容覆盖掉了；
   - 于是 NEG-03 的 `output_contains('\[verify against current AI Act text\]')`（L46）在"文件路径"上做正则搜索，路径中不含该文本，**恒为 False**。
   - 修复：删掉 check() 内的 `set_agent_output(agent_output)`，或由 main 在 check 之后不再重复设置；更稳妥的做法是 check() 只负责逻辑，路径由 main 读取内容后传入内容字符串。
2. **[P1] workspace 参数未使用（L20）**：check() 签名收 workspace 但函数体从未引用，属于未完成的设计（可能原本打算用 workspace 定位配置文件路径）。若评测沙箱中 `~` 目录与 workspace 不同，检查文件将找不到——建议改为基于 workspace 解析或从环境变量读取。
3. **[P2] 硬编码用户主目录路径（L27）**：`os.path.expanduser("~/.claude/plugins/config/...")` 在 Windows 上展开为 C:\Users\f50058303\...，依赖评测时该路径确实存在；若评测器在隔离沙箱运行且未铺设插件配置，SCOPE-02/PROC-06/OUT-01 三脚本项会因文件不存在而全部失败（file_contains 对不存在路径返回 False）。
4. **[P3] main() 仅在有文件时设置输出**：若 runner 以其他方式传递 agent 输出（不走文件路径），NEG-03 仍恒 False。建议文档化"必须传文件路径"这一约定。
5. **注释与实现一致**：L32-46 的注释准确标注了 4 项脚本检查及其 LLM 对应项，无夸大。

### 9.3 与 checker 库语义的核对

- `file_contains`（checker.py L31-43）：`re.search(pattern, content, re.MULTILINE)`。注意 `.*` 不跨行——PROC-06 的 `role_basis:.*\[verify` 仅在 role_basis 值与 [verify 标签**同一行**时才命中。SKILL.md 的示例记录是单行内嵌标签（L207），正常实现会命中；但若 agent 用 YAML 块标量（`role_basis: >-`）换行书写，则漏检。属边缘缺陷。
- `tool_log_contains`（L259-262）对整行 JSON 序列化做正则，子串匹配宽松（8.3-1 已述）。
- `output_contains`（L339-343）对 `_agent_output` 做 re.MULTILINE 搜索——受 9.2-1 影响恒 False。

---

## 十、跨文件一致性审查

| 一致性维度 | 结论 | 说明 |
|-----------|------|------|
| SKILL.md dispatch ↔ SCORING PROC-01 | [一致] | 五分支一一对应 |
| SKILL.md 等级判定顺序 ↔ PROC-05 | [一致] | A→B→C→D→E 顺序逐字对应 |
| SKILL.md 记录 16 字段 ↔ OUT-01 描述 | [一致] | 字段名完全一致 |
| SKILL.md List 列定义 ↔ PROC-07 | [一致] | 8 列逐列一致 |
| SKILL.md 收尾钩子 ↔ OUT-02 | [基本一致] | 见 4.3-3 的"write vs every action"歧义 |
| SKILL.md 角色/等级判据 ↔ PROC-03/PROC-05 | [一致] | 判据文本对齐 |
| **SCORING.yaml pattern ↔ check.py pattern** | **[不一致]** | PROC-06：YAML `'role_basis:.*\\[verify'`（字面双反斜杠，正则要求反斜杠前缀，恒不命中）vs check.py `'role_basis:.*\\[verify'`（Python 转义为 `\[`，正确）。NEG-03 同理。若评测器按 SCORING.yaml 直接调用 checker 函数则两项恒失败；按 check.py 则 NEG-03 又受 9.2-1 覆盖 bug 影响恒失败。**两条路径都有缺陷** |
| 路径解析方式 | [不一致] | SCORING.yaml 用 `${INVENTORY}` 变量（由 runner 解析），check.py 硬编码 expanduser 路径——两套解析并存，可能指向不同文件 |
| SKILL.md 内部命令名 | [不一致] | `/ai-governance-legal:aia-generation`（L192）vs `/aia-generation`（L244）；`/ai-governance-legal:ai-inventory classify`（L68）vs `/ai-inventory classify`（L241） |
| SKILL.md 标题 vs name | [轻微不一致] | L6 标题 "Ai Inventory"（首字母大写拼写）vs name `ai-inventory`，仅显示差异 |
| SKILL.md tier token ↔ 记录格式枚举 | [部分不一致] | Step 2C 未显式给出 `gpai`/`gpai_systemic` token（见 5.4-1） |
| SCORING total_items | [一致] | 14 = 2+7+2+3，计数正确 |
| SCORING 变量 | [不一致] | `${PRACTICE_CFG}` 定义但从未使用；`${INVENTORY}` 使用 |

结论：**SKILL.md 与 SCORING 的语义层高度对齐（该 Skill 的最大优点之一），但评测实现层（SCORING.yaml 转义、check.py 覆盖 bug、路径解析双轨）存在三处真实缺陷，且集中在 PROC-06 / OUT-01 / NEG-03 三个脚本项上。**

---

## 十一、规范符合性核对表（对照 SKILL-SPEC v1.0）

| 规范条目 | 结果 | 备注 |
|----------|------|------|
| name：小写+连字符，<=64，匹配目录 | [通过] | ai-inventory |
| description：第三人称，WHAT+WHEN+KEYWORDS，<=1024 | [通过] | 约 420 字符 |
| description：无祈使/一/二人称开头 | [通过] | |
| description：无交叉路由 | [通过] | |
| description：至少一个触发信号 | [通过] | "Use when the user says"（见第三节边界说明） |
| frontmatter：无白名单外键 | [通过] | 仅 name/description/argument-hint |
| 正文 <=600 行 | [通过] | 246 行 |
| 正文含 workflow 章节 | [通过] | ## What to do |
| 正文含 output format 章节 | [通过] | ## List format / ## Record format |
| 正文含 scope/limitations 章节 | [部分通过] | 仅隐式覆盖（Why-not + Guardrails），无显式 ## Scope |
| 无跨技能文件引用（../other-skill/） | [通过] | 引用为插件配置绝对路径（设计决策，见 7-3）与命令名（非文件引用） |
| 目录命名 NNN-kebab-case | [通过] | 243-ai-inventory |

12 项中 10 项通过、1 项部分通过（Scope 章节）、1 项为设计性说明项，**规范符合性良好**。

---

## 十二、优点与亮点

1. **核心主张清晰且贯穿始终**："role/tier 按系统评定、不按公司"在描述（L3）、When this runs（L11-15）、Step 1 判据（L96-108）三层反复强化，是整个 Skill 的灵魂，无一处漂移。
2. **领域知识准确度高**：Art. 5 八项禁止实践、Annex III 八大领域、GPAI 10^25 FLOPs 阈值、六种角色定义均与 EU AI Act 现行文本对照无误（第五节逐项核实）。
3. **诚实的知识边界管理**：`[verify against current AI Act text]` 标签机制贯穿分类与义务分析，并明确解释"不是犹豫，而是设计"（L87、L238），把法条核验责任正确地交给律师——这是法律领域 Skill 的最佳实践，规避了"自信且错误地写进董事会备忘录"（L230）的致命风险。
4. **负面护栏→临界失败的闭环设计**：Guardrails 四条（L236-245）与 CF-01/02/03 一一对应，负面约束在评测层可执行化。
5. **分类工作流可操作性极强**：每个角色给出"判定测试"（distinguishing test）而非定义复述；等级判定给出带顺序的检查清单（A→E）并要求注明命中的法条条目（L184-185），agent 无需猜测。
6. **交互路径完整**：Add 后显式告知"可以稍后回来分类"（L67-68）、列表后邀约仪表盘（L40-42）、分类后提供三步推荐（L190-194）——用户旅程无断点。
7. **记录格式示范完整**：16 字段的 YAML 示例含枚举注释、verify 标签用法、义务笔记示例（L211），是"输出即规范"的教科书式写法。
8. **与 SCORING 语义对齐度高**：dispatch、判定顺序、列定义、字段清单在 SKILL.md 与 SCORING.yaml 之间逐字一致，评测可追溯性极好。
9. **结构克制**：246 行覆盖 8 个章节，无冗余概念铺垫，符合"knowledge delta over redundancy"要求。
10. **设计立场鲜明**："清单是给律师的登记簿，义务分析归律师"（L231-232）一句话讲清了工具与人的边界。

---

## 十三、问题汇总、改进建议与总体评级

### 13.1 问题清单（按严重度排序）

| 编号 | 严重度 | 位置 | 问题 | 修复建议 |
|------|--------|------|------|----------|
| P0-1 | 高 | check.py L21-22 / L59-61 | check() 内 `set_agent_output(agent_output)` 用路径字符串覆盖 main() 刚写入的文件内容，NEG-03 恒 False | 删除 check() 内的 set_agent_output 调用，由 main 传入内容；或改传内容参数 |
| P0-2 | 高 | SCORING.yaml L75、L126 | 单引号 YAML 中 `\\[` 是字面双反斜杠，正则要求 [verify 前有反斜杠，恒不命中；与 check.py 的正确转义不一致 | YAML 改为 `'role_basis:.*\[verify'`（单反斜杠）或双引号 `"role_basis:.*\\\\[verify"`；并统一"以 check.py 为准"或"以 SCORING.yaml 为准"的单一事实来源 |
| P1-1 | 中 | SCORING.yaml L19-25、check.py L33 | SCOPE-02 子串匹配过宽，不验证读取顺序与 cold-start 分支 | 改用精确路径正则 + tool_log_read_before_write |
| P1-2 | 中 | SCORING.yaml L87-94、check.py L41 | OUT-01 描述 16 字段，仅查 review_trigger 一个键 | 增加多字段 pattern 或校验 YAML 结构 |
| P1-3 | 中 | SCORING.yaml L120-126 | NEG-03 用"输出含标签"实现"不剥离标签"，纯 list 场景误判 | 改为条件式：仅当输出涉及分类/义务话题时要求含标签；或降级为 CF 层面人工复核 |
| P1-4 | 中 | check.py L27 | 硬编码 expanduser 主目录，依赖沙箱铺设插件配置 | 用 ${WORKSPACE} 或环境变量解析配置根目录 |
| P2-1 | 低 | SKILL.md L192 vs L244、L68 vs L241 | 命令名前缀不一致 | 统一为 `/ai-governance-legal:...` 全限定名 |
| P2-2 | 低 | SKILL.md 正文 | 无显式 ## Scope/Limitations 章节 | 补一节集中陈述"不做什么" |
| P2-3 | 低 | SKILL.md L26-28、L63-81 | 边界用例（不存在 id、文件缺失时 list、可选字段默认值）未定义 | 各补一行规则 |
| P2-4 | 低 | SKILL.md Step 2C / L206-208 | tier/role 的精确枚举 token 未在 walk-through 中显式给出 | 补"写出字段时使用精确 token"清单 |
| P3-1 | 低 | check.py L20 | workspace 参数未使用 | 实现或删除 |
| P3-2 | 低 | SCORING.yaml L6 | ${PRACTICE_CFG} 死变量 | 删除或接入某个检查 |
| P3-3 | 低 | checker 语义 | PROC-06 的 `.*` 不跨行，块标量换行写法漏检 | 记录格式强制单行 role_basis/tier_basis，或 pattern 改用 `[\s\S]*` |

### 13.2 评测影响评估

按当前实现运行 `python check.py`：SCOPE-02 通过与否取决于工具日志（可达）；PROC-06 可通过（check.py 转义正确 + 单行记录）；OUT-01 可通过（仅查一个键，宽进）；**NEG-03 恒失败（P0-1 覆盖 bug）**。若评测器改为直接解释 SCORING.yaml 的 pattern（P0-2），则 PROC-06 与 NEG-03 同时恒失败。即：**无论走哪条执行路径，NEG-03 均无法获得真实通过；P0-1 与 P0-2 必须修其一（最好是都修），并补一条针对该 Skill 的最小冒烟测试（构造一次含 verify 标签的 classify 输出，断言 NEG-03 为 True）**。

### 13.3 总体评级

| 维度 | 评级 | 一句话结论 |
|------|------|-----------|
| SKILL.md 内容质量 | 优 | 流程完整、领域知识准确、护栏有力，法律领域 Skill 的范本 |
| 规范符合性（SKILL-SPEC） | 良 | 10/12 通过，仅 Scope 章节显式化欠缺 |
| SCORING.yaml 设计 | 良 | 语义对齐出色、LLM 问题质量高；两处 YAML 转义缺陷 + 三项弱代理检查 |
| check.py 实现 | 中 | 结构清晰但含一个确定性 P0 bug（NEG-03 恒 False）与路径依赖问题 |
| 综合 | 良（修复后可达优） | 内容层接近满分，评测实现层需按 13.1 修复后投入使用 |

审查结论：243-ai-inventory 是本次 322 个 complex skills 中"法律实务 × 流程"类型的高质量样本。其知识正确性、负面约束设计、SKILL.md 与 SCORING 的语义对齐均属上乘；主要缺陷集中在评测脚手架层（check.py 覆盖 bug、SCORING.yaml 转义与弱代理检查）。建议以 P0-1/P0-2 为优先完成修复并重跑冒烟验证后再纳入正式测评矩阵。
