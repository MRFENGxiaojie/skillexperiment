# REVIEW: 165-marketing-strategy-pmm

**审查日期**: 2026-08-06 | **Skill 类型**: process — 产品营销/GTM 战略知识手册（定位 / ICP / 竞争情报）
**Body 行数**: 504（wc -l 508 − 4 行 frontmatter；Read 显示 509 行内容，末行无换行符）| **参考文件数**: refs/6, scripts/0, assets/0, other/1（嵌套孤儿 SKILL.md 400 行）

---

## 1. 目录全量清单

```
165-marketing-strategy-pmm/                          （2026-08-05 树形快照）
├── SKILL.md                                  508 行   ← 正本（本次审查对象）
├── SCORING.yaml                              179 行   ← 20 测评点 + 2 CF（1 脚本 + 19 LLM）
├── check.py                                   70 行   ← 仅实现 1 个脚本项（SCOPE-01）
├── marketing-strategy-pmm/                    （孤儿嵌套目录，2026-08-03）
│   └── SKILL.md                              400 行   ← 旧版巴西向草稿：frontmatter 含禁用键
└── references/
    ├── 4-go-to-market-gtm-strategy.md        165 行   ← GTM 三型 / 90 天打法 / 国际市场进入
    ├── 5-product-launch-framework.md         161 行   ← 发布三档 / Tier1 周历 / 指标看板
    ├── 6-sales-enablement-collaboration.md   112 行   ← 销售赋能资产 / 培训 / 交接
    ├── 7-metrics-analytics.md                113 行   ← PMM KPI / HubSpot 报表 / QBR
    ├── 8-quick-reference.md                   77 行   ← 月度节奏 / 定位时间轴 / 交接协议
    └── resources.md                           23 行   ← 死索引：所列 10 个文件全部不存在
────────────────────────────────────────────────
共 10 文件 / 1808 行；无隐藏文件，无 scripts/、assets/ 目录
```

全部 10 个文件均已逐行通读：正本 SKILL.md 两版 + SCORING.yaml + check.py + references/ 6 个文件；另读依赖 `_shared/checker.py`（351 行）与 `_shared/SKILL-SPEC.md` 以核验判据语义与规范条款。

---

## 2. Frontmatter

### 2.1 name
`marketing-strategy-pmm`（22 字符）。小写 + 连字符，≤64，与目录 `165-marketing-strategy-pmm` 的 kebab 部分完全匹配。**✅**

### 2.2 description（SKILL.md:3，实测 492 字符 ≤1024）
分三句，逐句定位：

| 句 | 内容 | 功能定位 |
|---|---|---|
| 1 | "Product marketing, positioning, GTM strategy, and competitive intelligence." | WHAT（能力清单） |
| 2 | "Includes ICP definition, April Dunford positioning methodology, launch playbooks, competitive battlecards, and international market entry guides." | WHAT 展开（内容清单，覆盖 6 大能力域） |
| 3 | "Use when developing positioning, planning product launches, creating messaging, analyzing competitors, entering new markets, enabling sales, or when user mentions product marketing, positioning, GTM, go-to-market, competitive analysis, market entry, or sales enablement." | WHEN（8 场景动词 + 10 关键词，触发信号充足） |

- **第三人称** ✅：无 I/you/we/your；无 "Use this skill to…" 禁令句式。
- **WHAT/WHEN 完整** ✅：不是泛化描述（长度 492 字符，远超 40 字符下限）。
- **无跨技能路由** ✅：description 不出现任何其他 skill 名（SKILL-SPEC §2.5 合规）。
- **小瑕疵（2 处）**：① "Use when developing…" 为省略主语的椭圆句式，语义上是触发句，但不在 §2.4 列出的五个字面信号（"Use when the user…" 等）之内，严格口径判 ⚠️；② 句 3 "or **when user mentions**" 缺定冠词 the（"when the user mentions"）。

### 2.3 allowed-tools
未声明。SKILL-SPEC 中为可选字段，空缺合规。**✅**

### 2.4 其他字段
仅 name + description，无其他键，无 `metadata/license/version/triggers/agents` 等。**✅**

### 2.5 YAML
PyYAML `safe_load` 实测解析成功；description 为 plain scalar，内含逗号/句点但无引号嵌套风险。**✅**

**⚠️ 嵌套版 frontmatter（marketing-strategy-pmm/SKILL.md:1-18）**：name 带引号合法、description 535 字符以 "Use when the user asks about…" 开头（触发信号反而比正本规范），但多出 `triggers:`（11 项列表）与 `agents:`（claude-code）两个 SKILL-SPEC §1.3 明文禁止键（"No `triggers`、`agents`…"）。该文件若被任何递归 glob 拾取即构成违规——文件级地雷，详见 §5.5。

---

## 3. Body

### 3.1 段落清单（正本 504 行正文，L6–L509）

| 段落 | 行范围 | 行数 | 性质 |
|---|---|---|---|
| `# Marketing Strategy & Product Marketing` + 导语 | L6-8 | 3 | 定位声明（Series A+ / hybrid PLG/Sales-Led） |
| `## Keywords` | L11-12 | 2 | 30 个关键词 |
| `## Role Coverage` | L15-21 | 7 | 4 角色（PMM / Head of Mkt / Head of Growth / CMO） |
| `## Core KPIs by Role` | L24-32 | 9 | 4 角色 KPI 清单 |
| `## Tech Stack Integration` | L35-41 | 7 | HubSpot / GA / Gong / Productboard / Notion |
| `## 1. Strategic Foundation`（1.1 公司战略 / 1.2 ICP / 1.3 市场细分） | L46-169 | 124 | 知识框架 + 模板 |
| `## 2. Positioning & Messaging`（2.1 Dunford 六步 / 2.2 消息层级 L1-L4 / 2.3 测试迭代） | L174-331 | 158 | 知识框架 + 模板 |
| `## 3. Competitive Intelligence`（3.1 三层竞争 / 3.2 战卡 / 3.3 Win-Loss） | L336-497 | 162 | 知识框架 + 模板 |
| `## Reference Files` | L502-509 | 8 | 6 个 refs 扁平列表 |

### 3.2 必需章节（Workflow / Output / Scope）
**三项硬性章节全部缺失。** 全文 `## ` 级标题仅有：Keywords、Role Coverage、Core KPIs by Role、Tech Stack Integration、1.、2.、3.、Reference Files——无任何 Workflow/Process、Output Format、Scope/Limitations 类章节。这是本 skill 最核心的结构性缺陷，直接对应 §7 第 8/9/10 项 ❌，且是 SCORING CF-01 的结构性诱因（见 §10.2）。

### 3.3 委托
- 编号体系跨文件连续：正文 §1–§3 + references §4–§8（4=GTM、5=发布、6=销售赋能、7=指标、8=速查），"框架相互衔接"（dossier 语）属实。
- 但正文 §1–§3 **零"详见 ref N"使用点委托**，唯一入口是文末 L502-509 的扁平列表——只告诉 agent "有什么"，不告诉 "什么时候看哪个"。ref 6:39 "See Section 3.2 for detailed battlecard template" 反向引用正文，跨文件指针正确 ✅。

### 3.4 层级
H2/H3 两级清晰，编号 1–8 跨文件连续无跳号。`## Keywords` 等元信息章节置于知识章节之前，整体观感像"文档目录"而非"技能流程"。✅（结构性小疵见 §13-O2）

### 3.5 vs 600
正文 504 行 ≤ 600 硬限 ✅，占用 84%，余量仅 ~96 行。process 型目标行数约 ~200，实际 504（超 2.5 倍），且 504 行中约 80% 是模板/清单/知识内容、过程性内容为零——若补三必需章节需精打细算或继续外移内容。

---

## 4. 逻辑

### 4.1 步骤衔接
- 章节内容互指成立：§1.2 ICP ↔ PROC-01；§2.1 六步 ↔ PROC-02；§2.2 层级 ↔ PROC-03/04；§3.1/3.2 ↔ PROC-05；ref 4.2 90 天打法建立在 §1/§2 成果之上。**但全文没有一条可执行的步骤链**——只有静态知识，没有 "先做 X 再 Y" 的流程语句。Agent 如何组织一次任务完全依赖自身推断。

### 4.2 矛盾
1. **双版本冲突（重要）**：嵌套版 April Dunford 为 7 步（多 "Test with 10+ customer interviews"，L90-91），正本为 6 步；嵌套版全程 R$ 巴西（L291-295：Brazil 40% 首发、PIX/LGPD），正本为美元 US 优先。同名同树并存，任一处被误载即产生行为矛盾。
2. **ref 内 outbound 目标冲突**：ref 4.2 "Outbound sales blitz (top **100** accounts)"（ref4:63）vs ref 5 Launch Day "Sales outbound campaign (top **500** accounts)"（ref5:94）——同为发布期 outbound 目标，100 与 500 冲突（轻微，跨文件审计可检出）。
3. **ref 7 示例数字自相矛盾**：QBR 文字 "Improved win rate by 15%"（ref7:66）vs 表格 "Win Rate 30%→35% = +17%"（ref7:79）。
4. **Tier 1 预算跨版本差 5 倍**：正本 ref 5 $50k-$100k vs 嵌套版 R$250-500k。
5. **Nordics 悬空**：正文 §1.3 地理清单含 Nordics（L156），ref 4.3 五阶段市场进入不含——未解释。
6. **双发布时间轴并存**：ref 4.2 "90-Day Playbook"（-90~-30 → 1-30 → 31-90）与 ref 5.2 "8-Week Tier1 Playbook"（-8~-1 → 发布周 → +3-4 周）口径不同，二者关系（GTM 市场进入 vs 重大产品发布）从未说明；ref 5.2 L26 "8 Weeks Before Launch" 之后 L57 又出现 "**4 Weeks Before Launch**" 小标题（实际覆盖 -4~-1 周，是 8 周窗口的后半段），易读成两个独立阶段。
7. **ref 4.3 阶段重叠未说明**：UK(M4-9) 与 US(M1-6)、DACH(M7-12) 与 France(M10-15)、Canada(M7-12) 并行重叠，可辩护但应明示。
8. **ACV 分档重叠**：ref 4.1 PLG <$10k / Sales-Led $25k+ / Hybrid $5k-$100k，$5-10k 与 $25-100k 区间重叠属带宽语义，可接受，但无重叠时的取舍规则。

### 4.3 代码正确性（check.py 全文核验）
- 结构正确：`check()` 返回 `{"SCOPE-01": bool}`，与 docstring "Run all 1 script checks" 一致；`main()` 参数校验（argc==4）、agent_output 路径/文本双模式处理均正确。
- 依赖 `../_shared/checker.py` **已实测存在** ✅（complex-skills/_shared/checker.py 351 行）。`tool_log_contains("marketing-context")` 实际是正则子串匹配 JSON 序列化后的整条工具日志（checker.py:249-256）——agent 任何一次工具调用路径含 "marketing-context" 即通过，语义正确。
- 共享库 `output_not_contains` 在 `_agent_output=None` 时返回 True（vacuous truth），属共享库缺陷，本 skill 未使用该函数，不影响。
- 无语法错误、无死代码。**✅**（本 skill 自身无业务代码文件。）

### 4.4 条件完整性
- **零条件逻辑**：全文无 "if X → do Y" 决策规则。PROC-06 要求 "GTM motion 明确绑定 ACV 与买家画像"，ref 4.1 只给了对照表（ACV 分档 + 示例公司），无决策规则（如 "ACV>$25k 且采购者 VP/C-level → Sales-Led"）。
- 战卡中 WHEN TO WIN/LOSE 是模板占位示例，非给 agent 的分支指令。
- 评分条件侧：SCOPE-01（读 marketing-context）、OUT-01（UX spec）等判据在技能内容中无落点（见 §10）——"条件与技能脱节"。

---

## 5. 参考文件

### 5.1 引用矩阵

| 引用来源 | 引用目标 | 存在? |
|---|---|---|
| SKILL.md L504-509（6 项） | references/4~8 + resources.md | ✅ 全部存在 |
| ref 6:39 | SKILL.md §3.2（战卡模板） | ✅ 跨文件指针正确 |
| ref 6:93 | marketing-demand-acquisition skill（prose） | ✅ 允许（§3.3 prose 引用；语料 095 号存在） |
| resources.md L5-8 | positioning-frameworks / launch-checklists / international-gtm / messaging-templates .md | ❌ 4 个全不存在 |
| resources.md L12-13 | scripts/competitor_tracker.py / win_loss_analyzer.py | ❌ 不存在（scripts/ 目录本身不存在） |
| resources.md L17-20 | assets/ 4 个模板（pptx/docx/xlsx） | ❌ 不存在（assets/ 目录本身不存在） |
| 嵌套 SKILL.md L313-346 | references/positioning-frameworks 等 4 个 | ❌ 全部不存在 |

### 5.2 不可见资源
**resources.md 是死索引文件：所列 10 个资源（4 refs + 2 scripts + 4 assets）无一存在。** Agent 若按该文件尝试运行 `scripts/competitor_tracker.py` 或打开 `assets/roi-calculator.xlsx` 将直接失败；这也是"资源声称能力"与真实能力的差值。唯一真实信息是末行版本号（October 2025 | v1.0）——它更像是旧技能结构的残留 README。

### 5.3 全文审查（refs 4–8 逐文件）
**ref 4（165 行）**：三 motion 表格完整；90 天三阶段周历自洽（-90~-30 的 12 周 = Week1-12 ✅；Launch 1-30 天 = Week1-4 ✅；Post 31-90 天 = Week5-12 ✅）；国际五阶段预算 50+20+15+10+5=100% ✅、金额 $200k+$80k+$60k+$40k+$20k=$400k ✅、ARR 目标 $1M+$500k+$300k+$200k+$100k=$2.1M ✅（数字全部验算通过）。PROC-06/07/08 锚点全在此文件。问题：top-100/500 冲突（§4.2-2）、阶段重叠无说明（§4.2-7）。

**ref 5（161 行）**：三档发布分级（$50-100k / $10-25k / <$5k 自洽）；Tier1 八周逐周 checklist 颗粒度极细，Launch Day 当天 + Days 2-5 + Week 2 + Week 3-4 复盘完整；看板示例含目标对比（10,000 visitors goal 8,000 等）。问题：top-500 冲突、L57 标题歧义（§4.2-3/6）。

**ref 6（112 行）**：六类必备资产（15-20 页 deck 逐页定义是亮点、one-pager、battlecard→§3.2、30-45min demo 脚本 5 段时间分配、5 类邮件模板、ROI 计算器输入输出）；月度例会/季度半天/4 周 onboarding；MQL→SQL 与 PMM→Sales 交接含 SLA。prose 引用 marketing-demand-acquisition 合规 ✓，但该技能名未出现在任何 Related Skills 列表中，路由不闭环。

**ref 7（113 行）**：六项 PMM KPI 全带目标值（adoption >40% in 90d、velocity −20% YoY、win rate >30%、ACV +25%、ROMI 3:1、competitive win rate >35%）——与 QA-01 判据示例完全一致 ✅；三类 HubSpot 报表结构完整；QBR 四页模板。问题：15% vs +17% 冲突（§4.2-3）；**Slide 2 指标表 Markdown 破损**（§6.4，为前次审查遗漏项）；8 个 ✅⚠️ 状态符号（示例仪表盘内功能性用法）。

**ref 8（77 行）**：四周月度节奏、6 周定位时间轴（W1 研究→W2 框架→W3 消息→W4 验证→W5-6 推广）、4 类交接协议（PMM→Demand Gen/Sales/Product/CS 含 SLA）。纯清单形态，与 ref 6/7 无冲突。质量中高。

### 5.4 跨 Skill
- 有效 prose 引用：ref 6:93 → 095-marketing-demand-acquisition（语料存在 ✅）。
- SCORING NEG-01 提及 referral-program / content-strategy / launch-strategy：referral-program（语料 171 ✅）、content-strategy（**语料无此名**，近邻 024-content-creator/038-content-production）、launch-strategy（**语料无此名**，近邻 048-launch-review/291-technical-launch-planner）。
- 嵌套版 Related Skills（L395-400）：marketing-context（语料 203 ✅）、launch-strategy（✗）、competitive-intel（✗，近邻 256-competitive-landscape）、cmo-advisor（✗，近邻 080-ceo-advisor）——4 个名字 3 个不存在。
- 正本正文无任何"相关技能/何时不要用本技能"指引——NEG-01 判据在 skill 内无支撑。
- 全技能无 `../` 路径引用 ✅（§7 第 11 项）。

### 5.5 死文件
1. **`marketing-strategy-pmm/SKILL.md`（400 行）**——孤儿副本，两大危害：① frontmatter 含 `triggers`/`agents` 禁用键（SKILL-SPEC §1.3），任何递归 glob 加载即违规；② 内容为巴西向旧版，与正本行为矛盾（§4.2-1），其引用的 4 个 references 文件不存在。且该旧版反而具备正本缺失的要素（编号流程 1-8 步、Proactive Triggers、Output Artifacts、置信度输出规范）——规范化时只删了过程性内容，没删旧文件。
2. **`references/resources.md`（23 行）**——10/10 死链接索引（§5.2）。
3. 无其他死文件（check.py 依赖的 _shared/checker.py 存在）。

---

## 6. 语法格式

### 6.1 拼写
正文与 refs 未发现拼写错误（专业词 psychographics/technographics/battlecard/one-pager 均正确）。"PMM" 在 Keywords（L12）先出现、L18 才展开全称——轻微顺序问题。"**4 Go To Market Gtm Strategy**"（L504）展示名大小写混乱（Go To Market / Gtm），与文件内标题 "Go-To-Market (GTM) Strategy" 不一致。

### 6.2 语法
正文英文语法通顺，无病句。description "when user mentions" 缺冠词（§2.2）。正文引导句 "What would customers do if your product didn't exist?"（L180）为模板语境直接引语，合理。

### 6.3 混杂
- 正本 SKILL.md 全文 **0 emoji** ✅；ref 5（L141-145）与 ref 7（L76-81）各 8 个 ✅/⚠️ 状态符号——均在示例仪表盘/周报内，属数据状态功能性用法，判 🟢 可接受（从严可降 🟡）；嵌套版有 🟢🟡🔴 3 个（随孤儿文件处理）。
- 战卡模板大写段标签（KEY STRENGTHS / OUR ADVANTAGES / WHEN TO WIN / TALK TRACKS，L385-414）为模板结构标签，非指令性喊叫，可接受。
- 全大写 ≥5 字符共 15 处，均为产品名（HUBSPOT、GOOGLE ANALYTICS）或模板标签（LEVEL 1-4），无情感性喊叫 ✅。

### 6.4 Markdown 破损
**ref 7:72-81 QBR 指标表破损（前次审查遗漏项）**：
```
KPI             Q2 Target   Q2 Actual   Status

---

MQLs            800         950         ✅ +19%
```
表头行与数据行之间只有单独一行 `---`（单列分隔线），GFM 会解析为单列表格（表头 "KPI Q2 Target Q2 Actual Status" 坍缩为单单元格），4 列意图落空，并与上方 "**Slide 2: Metrics Dashboard**" 产生段落歧义。其余文件：正文 3.3 赢/丢单表（L473-477）分隔行规范 ✅；所有代码围栏成对闭合 ✅；正本末行缺换行符（wc 508 vs Read 509）——非破损，仅风格。

### 6.5 占位符
实测 0 处 TODO/FIXME/TBD/{{}}/`..` ✅。模板占位符 `[Competitor A]`（11 次）、`[Feature X]`、`[Your one-liner here]`、`[Link to competitive positioning map]` 等大量存在，属模板设计。**⚠️ 占位符与"真实感示例"混排**：L278-280 "Customer logos: [Microsoft, Shopify, Stripe]"、"Used by 10,000+ teams, 4.8/5 G2 rating"、L425 "35% win rate in competitive deals"、ref 5/7 的 "$800k pipeline" 与 "Q2-2025" 系列——全部为编造示例却无任何"示例数据"声明，存在被 agent 当作真实数据引用的风险（CF-02 暴露面，见 §10.2）。

### 6.6 截断
无截断。正文止于 L509 最后一个引用链接；refs 均以 `---` 完整收尾；resources.md 有版本落款。✅

---

## 7. 规范合规性（12-item vs SKILL-SPEC v1.0）

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | name ≤64 匹配目录 | ✅ | `marketing-strategy-pmm` 22 字符，匹配 165- kebab 部分 |
| 2 | desc 第三人称 WHAT+WHEN ≤1024 | ✅ | 492 字符；WHAT 2 句 + WHEN 1 句 + 关键词内嵌；第三人称 |
| 3 | desc 无 imp/1st/2nd | ✅ | 无 I/you/we/your，无 "Use this skill to…" |
| 4 | desc 无跨技能路由 | ✅ | 无其他 skill 名 |
| 5 | 触发信号 | ⚠️ | "Use when developing…" 语义为触发句、信号充分，但非 §2.4 五个字面信号（"Use when the user…" 等）；且 "when user mentions" 缺 the |
| 6 | 无禁用 frontmatter 键 | ✅（正本）/ ❌（嵌套版） | 正本仅 name+description；嵌套版含 `triggers`、`agents` 两个明文禁止键 |
| 7 | body ≤600 | ✅ | 504 行（84%） |
| 8 | workflow/process 章节 | ❌ | 全文无流程章节（§3.2） |
| 9 | output format 章节 | ❌ | 无交付物/输出契约 |
| 10 | scope/limitations 章节 | ❌ | 无边界、无"何时不用" |
| 11 | 无 ../ | ✅ | 0 处 |
| 12 | 目录 NNN-kebab | ✅ | `165-marketing-strategy-pmm` 无空格无大写（嵌套子目录为文件级结构异常，不属命名违规） |

**小结：8 ✅ / 2 ⚠️ / 3 ❌**（若计入嵌套版第 6 项则为 4 ❌）。文件层完全干净，但三个硬性必需章节（SKILL-SPEC §3.1）全缺——这是合规失分的全部来源，且无法靠补丁式修改解决，需要一次结构化补强。

---

## 8. 人机感

### 8.1 Emoji
正本正文 0 emoji ✅；refs 5/7 共 16 个 ✅/⚠️ 状态符号（示例仪表盘），功能性用法 🟢；嵌套版 🟢🟡🔴 随孤儿文件处理。无装饰性 emoji。

### 8.2 喊叫
无情感性全大写（15 处 ALL-CAPS 均为产品名/模板标签，§6.3）。✅

### 8.3 Persona 与引语
**无角色扮演 persona**（无 "You are a senior PMM" 开场），教科书姿态，专业克制。代表语句 6 条：
1. "Expert Product Marketing playbook for Series A+ startups expanding internationally with hybrid PLG/Sales-Led motion."（SKILL.md:8）
2. "Nail positioning - Clear, differentiated value prop"（SKILL.md:68）
3. "What would customers do if your product didn't exist?"（SKILL.md:180）
4. "That's great - many of our customers came from [Competitor A]. What prompted you to explore alternatives?"（SKILL.md:417，战卡话术示例）
5. "Why did you choose us over [Competitor]?"（SKILL.md:460，赢单访谈问题）
6. "Without clear positioning, all marketing is guesswork."（嵌套版 SKILL.md:375）
风格一致、数据导向、无营销腔。✅（策略顾问型技能可考虑补 1-2 个开场/提问话术块提升对话温度——🟢 优化项）

### 8.4 人机边界
**薄弱，几乎为零**。全文无：开场该问用户什么（intake）、信息不足时怎么办、何时停下确认、完成标准。SCORING 的 SCOPE-03（先收集产品/客户/LTV/CAC 再产出）与 CF-01（无 intake 直接套模板）都押注在 skill 应教授的对话行为上，而 skill 未教。嵌套版反而有 4 个 Proactive Triggers（无定位/信息不一致/无 ICP/竞品 repositioning）——旧版的人机边界意识优于正本，规范化时被删。**🟡**

### 8.5 人称
you/your 共 19 处，集中在模板与引导语（L180 "your product"、L193 "What do you have"、L264 "Your one-liner here"）与访谈问题脚本（L309-311、L458-469，被引内容合理）；I/we 10 处，集中在战卡 talk tracks 卖方口吻（L417 "many of our customers"、L392 "2x our price"），属角色话术。体感中等 🟡，不构成违规。

### 8.6 表格→自然语言
全文仅 1 张真表格（3.3 Win/Loss 数据跟踪表 L473-477）——典型数据记录表，用表恰当 ✅；ref 7 QBR 表本应走表格却 Markdown 破损（§6.4）；其余为列表/代码块形态，与"手册"定位匹配。

---

## 9. 可执行性

### 9.1 独立可执行性：3/10
把 SCORING.yaml 拿走、只给 SKILL.md：agent 能得到"丰富的知识"但得不到"怎么开始、按什么顺序、产出什么形态、不做什么"。无 intake、无步骤链、无输出契约、无决策规则、无工具路径。作为参考手册 9 分，作为可执行 skill 3 分——"像手册摘录"的输出风险高（CF-01 结构诱因）。

### 9.2 步骤
正本 0 条编号步骤。refs 内含周历式 checklist（ref 4.2/5.2），但那是"给公司团队的执行日历"，不是"给 agent 的任务流程"。模板类内容（battlecard、ICP 校验清单、消息层级、win/loss 问题集）可直接套用 ✅。**讽刺对照**：嵌套旧版有完整编号步骤（ICP Workflow 1-8、Positioning 1-8、Launch 1-9），正本规范化时删光了过程性内容。

### 9.3 工具
- 未声明 allowed-tools ✅（可选字段）。
- 无 scripts/ 实际文件（resources.md 声称 2 个 .py，不存在）。
- Tech Stack（L35-41）是"客户公司用的业务工具"（HubSpot/GA/Gong），非 agent 工具——信息性内容，不产生工具调用路径。
- check.py 依赖 `../_shared/checker.py` 已实测存在 ✅。

---

## 10. SCORING

### 10.1 测评点覆盖（20 项：1 脚本 + 19 LLM）

| 项 | 对齐 | 说明 |
|---|---|---|
| SCOPE-01 | ⚠️ | 脚本检查 tool_log 含 "marketing-context"。正本全文无此词（仅嵌套版 Related Skills 提及；语料 203-product-marketing-context 存在但 skill 未教授联动）——判据依赖环境恰好提供该文件，skill 侧无教学支撑 |
| SCOPE-02 | ✅ | Role Coverage（L15-21）+ 按角色 KPI（L24-32）直接支撑 |
| SCOPE-03 | ❌ | skill 无 intake 协议，agent 无从学起 |
| PROC-01~05 | ✅ | §1.2 / §2.1 / §2.2 / §3.1 / §3.2 逐项对应 |
| PROC-06 | ⚠️ | ref 4.1 有对照表但无 ACV/买家→motion 决策规则 |
| PROC-07 | ✅ | ref 4.2 90 天三阶段完整 |
| PROC-08 | ✅ | ref 4.3 分阶段+理由+本地化清单+预算 |
| PROC-09 | ✅ | §3.3 问题集+数据表+月报 |
| OUT-01 | ❌ | 判据列举 "scored idea matrix / UX spec / landing page copy / launch checklist / measurement plan / ROI model"——"scored idea matrix" 与 "UX spec" 明显是其他技能（点子筛选/UX）的复制残留，本 skill 交付物是 positioning/battlecard/launch plan/GTM 计划等，判据与技能对不上 |
| OUT-02 | ⚠️ | skill 数字密度高可支撑，但无"数字必须来自用户输入"约束 |
| OUT-03 | ⚠️ | 正本无置信度标记（verified/estimated/assumed）教学；旧版嵌套文件反而有 |
| OUT-04 | ⚠️ | 无 owner+deadline 教学；ref 8 SLA 是交接协议不是动作责任 |
| NEG-01 | ⚠️ | 判据引 referral-program / content-strategy / launch-strategy：后两者语料无此名，且正本无任何路由指引 |
| NEG-02 | ⚠️ | skill 通篇编造感示例（§6.5）却无"示例数据"声明，未教 placeholder 标注 |
| QA-01 | ✅ | ref 7.1 六项 KPI 目标值与判据示例（>30%/>40%/3:1）完全一致 |
| QA-02 | ❌ | 判据要求 "HubSpot, GA4, GSC, referring domains"——skill 只提 HubSpot/Google Analytics/Gong，GA4、GSC、referring domains 零出现 |

覆盖统计：**✅ 9 / ⚠️ 6 / ❌ 5**。5 项硬性错位中 4 项（SCOPE-03、OUT-01、QA-02 及半项 SCOPE-01）是 SCORING 与 skill 内容互相打架，不是 agent 能力问题。

### 10.2 CF（critical_failures）
- **CF-01（无 grounding 直接套模板 → cap_to_0）**：风险 **高**。skill 不教 intake，用户只给一句 "给我做个 GTM 方案" 时 agent 直接输出 handbook 内容即触发。这是技能侧最真实的失分点。
- **CF-02（编造公司/竞对指标 → cap_to_0）**：风险 **中高**。skill 嵌入大量"像真数据"的示例（Microsoft/Shopify/Stripe、10,000+ teams、4.8/5 G2、35% win rate、$800k pipeline、Q2-2025 系列），无免责声明；战卡模板本体为占位符形态（NEG-02 有共同防线），但示例区无防线。

---

## 11. 已知问题

### Dossier 复核
Dossier 原判："**逻辑**: 165 框架相互衔接但为知识手册；**总评**: 🟡"。

**核验：属实。** "框架相互衔接"已验证（正文 1-3 + refs 4-8 编号连续、互指成立，§3.3/§4.1）；"知识手册"已验证（零流程/输出/边界章节，§3.2）。合规 8✅/2⚠️/3❌（§7）与 🟡 档位一致。

### Dossier MISSED（未记录问题）
1. 🔴 **嵌套孤儿 `marketing-strategy-pmm/SKILL.md`**（400 行）：禁用键 + R$ 巴西版矛盾内容 + 4 条死引用；递归 glob 加载即破第 6 项合规。
2. 🔴 **`references/resources.md` 死索引**：10/10 列表文件不存在。
3. 🔴 **三必需章节全缺**（比"知识手册"印象更可量化——SKILL-SPEC §3.1 硬性条款）。
4. 🟡 **SCORING 脱节**：SCOPE-01 半不可达、OUT-01 "UX spec/scored idea matrix" 残留、QA-02 GA4/GSC 无落点、NEG-01 路由无锚点（§10.1）。
5. 🟡 **双版本跨文件冲突**：outbound 100/500、QBR 15%/+17%、7 步 vs 6 步、Tier1 预算差 5 倍（§4.2）。
6. 🟡 **ref 7 QBR 表 Markdown 破损**（§6.4，前次审查误判"无破损"）。
7. 🟢 Nordics 悬空、双时间轴关系未说明（§4.2-5/6）。

---

## 12. 综合评分（8 维加权 → /100）

| 维度 | 权重 | 得分 | 加权 | 依据摘要 |
|---|---|---|---|---|
| 内容深度 | 0.15 | 9 | 1.35 | 框架完整、模板可用、预算/KPI/ARR 数字全验算自洽 |
| 结构 | 0.10 | 6 | 0.60 | 编号连续层级清晰；三必需章节全缺 |
| 逻辑 | 0.15 | 7 | 1.05 | 互链成立；跨版本/跨 ref 数字冲突 7 处、零决策规则 |
| 规范合规 | 0.20 | 5 | 1.00 | 12 项中 3 硬性 ❌ + 2 ⚠️；嵌套版另含禁用键 |
| 人机感 | 0.10 | 6 | 0.60 | 无 persona/喊叫/emoji；零对话协议、19 处 you/your |
| 可执行性 | 0.15 | 3 | 0.45 | 知识手册：无步骤/输出契约/工具路径，独立执行 3/10 |
| 参考文件 | 0.10 | 4 | 0.40 | 5 个实质 ref 质量高；resources.md 死链 10 条 + 孤儿副本 |
| 测评对齐 | 0.05 | 4 | 0.20 | 5 项判据错位/污染（SCOPE-03、OUT-01、QA-02 等） |
| **合计** | 100% | — | **5.65 → 56.5/100** | **🟠 C（濒临 🟡B）** |

**最终评级：56.5/100 → 🟠C（差 3.5 分达 B）。** 与 dossier 🟡 存在约一档偏差，原因：本次为全文件级审查，新增证据（三硬性章节缺失、死资源链、孤儿副本、SCORING 污染、CF-01/02 结构诱因）把评分压到 B 下沿之下。内容资产本身值 B 档（框架质量在线），但按 SKILL-SPEC 硬性条款与测评可达性，当前档位 C 更诚实。完成 §13 的 R1-R3 三项致命修复后预期 65+ 分回 B 档。

---

## 13. 修复建议（按优先级，本节省为全文重点）

### 🔴 致命（不修则评测必失分 / 存在 cap_to_0 风险）

**R1. 补三必需章节（Workflow / Output / Scope）** — SKILL.md 结构性补强
- 位置：`## Workflow` 建议插于 L43（Tech Stack 之后）；`## Output` 与 `## Scope` 建议插于 L497（§3 之后）或合并前置。
- 内容骨架（约 60-80 行，注意 96 行行数预算）：
  - **Workflow（7 步）**：① Intake——向用户收集：产品/行业、目标客户、LTV/CAC、ARPU、当前渠道状态、目标（对齐 SCOPE-03、CF-01）；② 角色识别——从用户身份映射 Role Coverage（L15-21）与对应 KPI（L24-32）（对齐 SCOPE-02）；③ ICP 定义（§1.2 框架）；④ 定位（§2.1 六步）；⑤ 消息架构（§2.2 四层）；⑥ 竞争分析（§3.1/§3.2）；⑦ 按请求类型产出 GTM/发布/市场进入/赢丢单方案（读 ref 4/5/8），数据不足处标注 verified/estimated/assumed（对齐 OUT-03）。
  - **Output**：结论先行（Conclusion → 证据 → 行动）、交付物形态清单（定位陈述、battlecard、launch checklist、测量计划）、动作带 owner+deadline（对齐 OUT-04）。
  - **Scope**：不做推介计划（→ 171-referral-program）、不做内容日历/内容生产（→ 038-content-production）、不执行投放运营（→ 095-marketing-demand-acquisition）、不做发布执行复盘（→ 048-launch-review）；信息不足先提问后产出；不虚构竞品数据（对齐 NEG-01/02）。
- 后果：不修 → 规范第 8/9/10 项恒挂、SCOPE-03/OUT-03/04/NEG-01 大概率失分、CF-01 一触即发；修后 → 合规可达 12/12，5 项测评点从"无锚点"变"有锚点"。
- 工作量：3-4 小时（含把 1.3/3.3 部分内容下放 refs 以控制行数预算）。

**R2. 删除或归档孤儿副本 `marketing-strategy-pmm/SKILL.md`（400 行）**
- 位置：`marketing-strategy-pmm/` 全目录。frontmatter `triggers:`/`agents:` 违反 SKILL-SPEC §1.3（L4-17）；内容为巴西向旧版（L289-295：Brazil 40% 首发 + R$、PIX、LGPD）与正本冲突；引用的 4 个 references 文件不存在（L313-346）。
- 处置：优先删除；其中尚有价值的内容（编号流程 1-8 步、Proactive Triggers 4 条、置信度输出规范、Related Skills 路由）应先吸收进 R1 再删——注意 Related Skills 中 launch-strategy/competitive-intel/cmo-advisor 三个名字语料不存在，吸收时须改为真实语料名（048-launch-review/256-competitive-landscape/080-ceo-advisor）。
- 后果：不修 → 目录扫描评测可能加载错文件；agent 双读输出矛盾方案（R$ vs $）；合规扫描直接暴露禁用键；修后 → 消除双头风险。
- 工作量：0.5 小时（含内容回收评估）。

**R3. 重写或删除 `references/resources.md`（23 行）**
- 位置：`references/resources.md` 全文件 + SKILL.md:509 引用行。
- 处置：二选一——(a) 重写为真实 6 个 refs 的用途索引（0.5 小时，推荐）；(b) 真正补建 scripts/competitor_tracker.py、win_loss_analyzer.py 与 4 个 assets 模板（4-6 小时，价值更高但超出本 skill 核心范围）。
- 后果：不修 → agent 按索引 10 次 Read 失败路径；资源可信度崩坏；修后 → 资源声称与真实结构一致。
- 工作量：0.5 小时（方案 a）。

### 🟡 重要（建议本季度内修）

**R4. SCORING.yaml 对齐技能现实**（1 小时）
- OUT-01（SCORING.yaml:106-113）：删除 "scored idea matrix / UX spec" 污染项，替换为本 skill 真实交付物（positioning statement、messaging hierarchy、battlecard、GTM plan、90 天发布计划、市场进入计划、win/loss 报告）。
- QA-02（SCORING.yaml:164-170）：工具改为 "HubSpot, Google Analytics, Gong/Chorus"，或将 GA4/GSC/referring domains 补入 ref 7 测量工具清单（二选一，推荐改 SCORING 对齐 skill）。
- SCOPE-01（SCORING.yaml:7-13）：在 R1 的 Scope/Workflow 中说明 marketing-context 联动，或改判据为有落点的行为（如"产出前确认角色与上下文"）。
- NEG-01（SCORING.yaml:141-145）：skill 名改为语料真实存在者（171-referral-program / 038-content-production / 048-launch-review），并在 R1 Scope 节落锚。
- 后果：不修 → 5 项判据恒负或依赖运气，测评总分失真。

**R5. 为示例数据加免责声明（CF-02 防线）**（0.2 小时）
- 位置：SKILL.md:278-280（客户 logo/10,000+ teams/4.8/5 G2）、424-426（35% win rate）；ref 5:140-160（$800k pipeline 看板）；ref 7:63-68（Q2-2025 数字）。
- 修复：首次出现示例处加一行："文中公司名、金额、评分均为教学示例，禁止作为用户/竞对真实数据输出；用户未提供数据时以占位符或 verified/estimated/assumed 标注。"
- 后果：不修 → NEG-02/CF-02 判据无支撑，agent 照抄示例数字即 cap_to_0。

**R6. 修 ref 7 QBR 表 Markdown**（0.1 小时）
- 位置：references/7-metrics-analytics.md:72-81。补全 4 列分隔线 `|------|---------|---------|--------|` 或改代码围栏。
- 后果：不修 → 渲染为单列表格，指标对照信息丢失。

**R7. 补 GTM motion 决策规则（PROC-06）**（0.5 小时）
- 位置：references/4-go-to-market-gtm-strategy.md:3-31 末尾。追加："ACV <$10k 且采购者终端用户 → PLG；ACV ≥$25k 且采购者 VP/C-level → Sales-Led；其余 → Hybrid（Series A 默认 Hybrid）"。并为 §4.2/§5.2 双时间轴补一句关系说明（90 天 GTM 打法适用于新品市场进入，8 周 Tier1 适用于重大产品发布，可嵌套）。

**R8. 统一跨文件数字与口径**（0.3 小时）
- outbound 目标：ref 4:63 "top 100" vs ref 5:94 "top 500" 统一；QBR 示例：ref 7:66 "15%" vs :79 "+17%" 统一；Nordics：SKILL.md:156 加说明或删除；ref 4.3 阶段重叠补"并行工作流"说明。

### 🟢 优化（低优先）

- **O1.** 正文 §3.2 战卡模板（L366-436，约 70 行）外移至 references/——504 行余量 96 行，R1 三节后逼近 600 上限；战卡与 ref 6 资产清单天然同域。
- **O2.** `## Reference Files`（L502-509）改为"按需委托表"：每行补一句何时读（"GTM/90 天打法 → ref 4；发布分级/周历 → ref 5；销售赋能 → ref 6；KPI 基准/报表 → ref 7；月度节奏/交接 → ref 8"）——不补则 refs 占全 skill 60% 内容被浪费（0.5 小时）。
- **O3.** 正本补 `## Summary` 锚点目录（嵌套版 L26-34 有，导航价值高，尤其 R2 吸收后）。
- **O4.** 补文件落款：正本与 refs 均无版本/更新日期，统一加 `Last Updated` 脚注。
- **O5.** ref 5/7 的 ✅⚠️ 表情符改文字（meets/misses），规避严格 emoji 审查口径（0.1 小时）。
- **O6.** check.py 可加第二脚本检查：`output_not_contains` 验证输出不含示例公司名（Microsoft/Stripe 等）——直接服务 NEG-02/CF-02，0.3 小时，性价比高。
- **O7.** description 触发措辞规范化："Use when developing…" → "Use when the user asks about positioning, product launches, messaging, competitors, market entry, or sales enablement…"，顺手补 the（0.1 小时）。
- **O8.** L504 展示名 "**4 Go To Market Gtm Strategy**" 大小写修正；L278 示例客户加 "(示例)" 标注（0.1 小时）。

**合计工作量：🔴 约 4-5 小时 + 🟡 约 2 小时 + 🟢 约 1.5 小时 ≈ 1 个工作日内，预期 56.5 → 65+（🟡B）。**

---

## 附录：审查过程记录

- 审查时间：2026-08-06；审查者：SkillIF REVIEW Agent。
- 读取文件（全部全文）：SKILL.md（正本 509 行内容）、marketing-strategy-pmm/SKILL.md（400 行）、SCORING.yaml（179 行）、check.py（70 行）、references/4-8 六文件 + resources.md；另读 `complex-skills/_shared/checker.py`（351 行）与 `complex-skills/_shared/SKILL-SPEC.md` 核验判据语义与规范条款。
- 验证手段：`wc -l` 全量行数（10 文件 1808 行）；Python 实测 description 长度（正本 492 / 嵌套 535）、body 行数（504）、frontmatter 键（正本仅 name+description；嵌套含 triggers/agents）；PyYAML `safe_load` 验证 SCORING.yaml（20 criteria + 2 CF，ID 无重复）与两个 frontmatter；预算/ARR/ACV 数字逐项验算（§5.3 全部通过）；Grep 工具全量扫描 emoji/人称/全大写/TODO/`../`；语料邻接 skill 存在性逐一核验（095/171/203/038/048/256/080 ✅；content-strategy/launch-strategy/competitive-intel/cmo-advisor ✗）。
- 与前版 REVIEW.md（373 行，2026-08-06 19:42）差异：本次为全新通读生成——新增发现 ref 7 QBR 表 Markdown 破损（前版误判"无破损"）、ref 4.3 预算/ARR 验算通过、ref 5.2 "4 Weeks Before Launch" 标题歧义、示例数据无免责声明的 CF-02 系统性风险、NEG-01 skill 名语料核验；合规口径收紧（触发信号判 ⚠️），综合分 56.5 → 🟠C（与 dossier 🟡 差约一档，理由见 §12）。
- 本 REVIEW.md 仅写入技能目录，未修改 SKILL.md / SCORING.yaml / check.py 及任何 references 文件。
