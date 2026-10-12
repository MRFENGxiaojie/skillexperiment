# REVIEW: 053-go-to-market-plan

**2026-08-06** | Claude 审查 | 对照基准: `_shared/SKILL-SPEC.md` v1.0（12 项合规清单）、既有 skill-dossier（2026-08-05 批次）、本目录 SCORING.yaml（20 项评测）
**结论**: 🟢 内容与结构质量位于语料库前列，可直接进入评测；但存在 1 项硬性规范缺失（Scope/Limitations 节）、1 项触发短语措辞偏离、1 处 AskUserQuestion 工具依赖风险、1 处 OUT-05 模板与指令脱节。综合评分 **87/100（B+）**，修复上述 4 项后可达 A 档（≥90）。

---

## 1. 目录清单

本技能目录共 4 个文件，无 `references/`、无 `scripts/` 子目录（skill 自包含，见 §5）：

| 文件 | 行数 | 角色 | 备注 |
|------|:----:|------|------|
| `SKILL.md` | 444 | 技能主体 | frontmatter 4 行 + body 440 行；全部逻辑内联 |
| `SCORING.yaml` | 179 | 评测标准 | 20 项 criteria + 2 项 critical_failures（L171-178） |
| `check.py` | 75 | 脚本检查 | 仅实现 2 项脚本检查（SCOPE-02、PROC-03） |
| `REVIEW.md` | 4 | 审查档案 | 旧版为占位 stub（本次全文覆盖） |

- 行数核对：SKILL.md 最后一行（L444）为收尾空行；dossier 中"444 行"的记载与实测一致。
- SCORING.yaml `total_items: 20`（L3）与 criteria 实际条数 3+6+5+2+4=20（L7-169）核对一致；`pattern: process`（L2）与 SKILL-SPEC §3.2 的 process 模式对应（目标 ~200 行，见 §3）。
- check.py 仅有 2 项 `judge: script`（SCORING.yaml L18、L50），其余 18 项 `judge: llm`，脚本/LLM 分工与 SCORING 标注完全一致（见 §10）。

---

## 2. Frontmatter 审查

针对 SKILL.md L1-4 逐条核对 SKILL-SPEC §1（Frontmatter）与 §2（Description）：

**2.1 name 字段（L2）**
- `name: go-to-market-plan` — 17 字符（≤64），小写 + 连字符，与目录名 `053-go-to-market-plan` 匹配（SKILL-SPEC §1.1、§4）。✅

**2.2 description 字段（L3）**
- 长度：约 400 字符（≤1024）。✅
- **WHAT**："Analyzes the founder's business context to deliver 3 best go-to-market strategies tailored to their current stage, product, and market." — 具体、非泛化，与 body Purpose（L8）措辞呼应。✅
- **WHEN/KEYWORDS**："Asks up to 10 diagnostic questions…" + "Use when user needs go-to-market strategy, launch planning, market entry strategy, or actionable GTM roadmap." — 触发场景与关键词齐备。✅
- **第三人称**：以 "Analyzes / Asks" 第三人称描述，无第一/第二人称、无祈使开头（SKILL-SPEC §2.3）。✅
- **无跨技能路由**：description 未出现 "NOT for X, use Y instead" 式路由（§2.5）。✅
- **触发信号短语（§2.4）**：⚠️ 规范列举的信号为 "Use when the user… / Use when the user asks to… / Use when the user needs to… / Triggers on… / Use for…"；本文为 **"Use when user needs…"** — 缺 "the"、缺 "to"，且非任何列举短语的精确形式。功能上等价于触发信号（与 dossier 对 303 号 "Use when users request" 的判罚同型），但严格口径下属措辞偏离，建议微调（见 §13 P1-3）。

**2.3 frontmatter 键白名单（§1.2/§1.3）**
- 仅出现 `name`、`description` 两个必需键，无任何 allowed-optional 字段，也无任何 forbidden 键（逐一核对 §1.3 列出的 40 余个禁用键，均未出现）。✅
- 可选字段（如 `allowed-tools`）未使用本身合规；但考虑到 §13 P1-2 的 AskUserQuestion 工具依赖，声明 allowed-tools 并不能解决该工具在本 harness 不存在的问题，故不作为修复必选项。

**小结**：frontmatter 仅一处 ⚠️（触发短语措辞），其余全绿。

---

## 3. Body 结构

**3.1 总体框架（SKILL.md L5-444）**

| 节 | 行号 | 角色 |
|----|------|------|
| `# Go To Market Plan`（H1） | L5 | 标题（建议连字符化，见 §6） |
| `## Purpose` | L7-9 | 一句话使命 |
| `## Execution Logic` | L12-24 | $ARGUMENTS 双模式门控 |
| `## Task Execution` | L27-122 | Steps 1-6 主工作流 |
| `## Writing Rules` | L125-169 | 硬约束写作规则 |
| `## Output Format` | L172-377 | 输出模板（L174-260）+ 完整示例（L262-377） |
| `## Quality Checklist (Self-Verification)` | L381-425 | 6 组 24 项自检 |
| `## Defaults & Assumptions` | L428-443 | 默认值与假设声明 |

**3.2 三必需节核对（SKILL-SPEC §3.1）**
- **Workflow/Process** ✅：Execution Logic（L12-24）+ Task Execution 六步（L27-122）构成完整闭环：读上下文 → 诊断就绪度 → 提问 → 分析 → 生成 3 策略 → 格式化校验。
- **Output Format** ✅：L172-377 同时提供占位模板（L174-260）与 115 行完整实例（L262-377，以 DevAnalytics 为例），是语料库中为数不多"模板 + 完整示例"双全的写法。
- **Scope/Limitations** ❌：全文无任何 Scope / Limitations / "What This Skill Does NOT Do" 节。Writing Rules（L125-169）是写作约束而非范围声明；Defaults & Assumptions（L428-443）是默认值而非不做清单；Quality Checklist 是自检而非边界。**这是本次审查唯一硬性规范缺失**，详见 §7 第 10 项与 §13 P1-1。

**3.3 体量（§3.2）**
- body 440 行 ≤ 600 行硬上限 ✅。
- 但 pattern=process 的目标体量约 200 行，当前为其 2 倍有余；膨胀主因是内置 115 行完整示例（L262-377）。补 Scope 节后会增至 ~460 行，仍合规但建议将示例下沉 `references/`（见 §13 P2-7，属可选优化而非缺陷）。

**3.4 结构优点**
- 双模式 $ARGUMENTS 门控（L14-23）与评测框架的 load/execute 两模式设计吻合（对应 SKILLIF 2 Mode 测评矩阵）。
- 每个 Step 的产出语义明确（Step 6 显式引用 Output Format 与 Quality Checklist，L119-122），交叉引用链完整。
- "Writing Rules: Hard constraints. No interpretation."（L126）以最高力度框定约束，是良好实践。

---

## 4. 逻辑一致性

**4.1 六步工作流逐项核对（L27-122）**

| 步骤 | 行号 | 内容 | 一致性结论 |
|------|------|------|-----------|
| 1. Read Business Context | L31-34 | FOUNDER_CONTEXT.md 读取 + 9 项字段提取 | 与 SCORING SCOPE-02 对齐 ✅ |
| 2. Diagnose GTM Readiness | L36-51 | 8 项必需信息清单（L39-47）+ 分支（L49-51） | 与 SCORING SCOPE-03 对齐 ✅ |
| 3. Ask Diagnostic Questions | L53-72 | "3-10 questions"（L54）+ 核心 7 问（L56-63）+ 场景定制问（L65-70）+ "只问真正需要"（L72） | 与 description "up to 10" 上限一致 ✅ |
| 4. Analyze Market Entry | L74-89 | PMF/楔子/竞争/渠道/GTM motion/时机 6 维度 + 5 条分析原则 | 与 SCORING PROC-02 对齐 ✅ |
| 5. Generate 3 Strategies | L91-117 | "exactly 3"（L92）+ 5 条选择标准（L94-100）+ A/B/C 三部分（L104-117） | 与 description/PROC-03/PROC-04 对齐 ✅ |
| 6. Format and Verify | L119-122 | 按 Output Format 输出 + Quality Checklist 自检 | 交叉引用成立 ✅ |

**4.2 示例数字自洽性验证（L264-377，逐项演算）**
- Strategy 1：outreach 20 → 5 partnerships，隐含接受率 25%，与 Metrics 目标 "25%"（L287-288）吻合 ✅；milestones（L293）与 Success Criteria（L372）口径一致。
- Strategy 2：页面 1,000 views × 15% 邮件转化 = 150 signups；150 × 10% 试用转化 = 15 trials —— 与 Milestones "150 email signups / 15 trial signups"（L323）及 Success Criteria（L373）完全咬合 ✅。
- Strategy 3：outreach 15 × 30% 接受率 ≈ 3-4 位伙伴，与 "3 active partners"（L354）吻合；3 伙伴 × 每月 2 推荐 × 2 月 ≈ 12 试用，与 "10 partner-referred trials"（L354）数量级一致 ✅。
- 三个策略的 Execution Priority 排序（L361-365）与 Success Criteria（L369-376）结构互映，无矛盾。

**4.3 发现的问题（按严重度排序）**

- **问题 A — AskUserQuestion 工具依赖（可执行性风险）**：L54 "Use the AskUserQuestion tool to gather missing information." 该工具并非 Claude Code 标准工具集成员；在 SKILLIF 的多 harness 测评矩阵（记忆中的 2 Mode × 5 Harness 设计）中，部分 harness 下该指令无法按字面执行。Quality Checklist L388（"I used AskUserQuestion to gather it"）隐含同一假设。dossier（skill-dossier.md L442）亦标注此点。→ 修复见 §13 P1-2。
- **问题 B — 必需信息与问题集覆盖差**：Step 2 必需信息含 "Distribution model (direct, channel partners, marketplace, etc.)"（L45），但 Step 3 的核心问题清单（L56-63）没有对应的渠道/分发提问，仅 L60 "How do customers currently discover solutions like yours?" 间接覆盖。轻微缺口。→ §13 P2-5。
- **问题 C — OUT-05 指令与模板脱节**：L441 要求 "Document any assumptions made at the top of the output"，但 Output Format 模板（L174-260）与完整示例（L264-377）开头均无 Assumptions 占位元素（模板以 "## Your 3 Go-to-Market Strategies" 直接起首，L175）。LLM 评测 OUT-05 时，agent 按模板输出会缺该元素而误判。→ §13 P2-6。
- **问题 D — Step 5 未显式路由 Writing Rules**：Writing Rules 自称 "Hard constraints. No interpretation."（L126），但 Step 5（L91-117）与 Step 6（L119-122）均未显式要求引用该节（Step 6 只引 Output Format 与 Quality Checklist）。约束链存在但调用点缺失，轻微。→ §13 P3-9。
- **问题 E（轻微）— Step 2→3→4 回环省略**：L49 "If you have enough context: Proceed directly to Step 4." 但提问（Step 3）之后未显式说明"重新评估就绪度再进入 Step 4"，隐含跳转。→ §13 P2-4。

**4.4 一致性亮点**
- description "3 best go-to-market strategies"（L3）与 "exactly 3"（L92）、模板 "### Strategy 1/2/3"（L181/206/225）三处口径完全一致。
- Quality Checklist 24 项（L385-422）与 Writing Rules 逐条对应（如 L402 对应 L131，L413 对应 L139-146），无自相矛盾。
- Defaults & Assumptions（L428-443）与示例设定一致：默认 post-MVP 阶段（L434）对应示例 "MVP launched, 12 beta users"（L267）。
- 未发现占位符残留、未发现前后数字打架。

---

## 5. 参考文件审查

- **本技能无 references/、无 scripts/ 目录**：全部逻辑内联于 SKILL.md，自包含、零跨技能路径（SKILL-SPEC §3.3 的 `../other-skill/` 禁令不适用）。✅
- **唯一外部文件依赖 — FOUNDER_CONTEXT.md**（L32-34）：这是项目根目录的用户侧文件，不是技能文件引用，合规。但技能未给出该文件的最小结构模板，字段提取（L33 的 9 项）依赖用户自行按约准备；若文件缺失则走提问路径（L34），逻辑闭环成立。建议补模板（→ §13 P3-8）。
- **check.py（75 行）**：L10 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))` 解析为 `complex-skills/_shared`，checker 库存在（`_shared/checker.py` 265 行），导入路径正确 ✅。L24-29 对 agent_output 的文件/文本双形态处理正确；L35/L40 两处正则转义正确（详见 §10）。
- **SCORING.yaml（179 行）**：自包含，无文件引用；`fn` 字段（L20/L52）指向 checker 库函数名，均已实现（checker.py L259/L339）。✅
- **REVIEW.md 旧占位（4 行）**：本次覆盖，其内容留档于 §11。

---

## 6. 语法格式

- **拼写与语法**：全文逐段扫读 L1-444，未发现拼写错误、病句或中英混杂（全英文）。数字、时间格式统一（"30-60 minutes"、"60/90 days"）。
- **Markdown 结构**：标题层级一致（H1×1 → H2×7 → H3 于 Writing Rules/Quality Checklist 内合理使用）；代码围栏闭合正确（模板 L174-260、示例 L264-377 两处独立围栏）；列表缩进统一；BAD/GOOD 对比（L139-146）排版清晰。
- **术语统一**："go-to-market" 连字符用法全文一致；"Do This Today" 在 Step 5 定义（L115-117）、模板（L201-202）、示例（L295-296/L325-326/L356-357）、质检清单（L409）四处一致；"Expected Milestones / Metrics to Track / Execution Priority / Success Criteria" 在模板与示例中逐字一致。
- **微小瑕疵（装饰性）**：
  1. H1 "Go To Market Plan"（L5）未使用连字符，与正文 "go-to-market" 惯例不统一（SKILL.md L3、L130 等处均带连字符）。
  2. 模板中 Strategy 2/3 使用 `[...]` 占位（L209-240），属模板常规写法，非缺陷。
- **格式亮点**：输出模板（L174-260）与完整示例（L262-377）共用同一套骨架，是"模板-实例"互验的良好实践。

---

## 7. SKILL-SPEC 合规 12 项

对照 SKILL-SPEC §5 Compliance Checklist（L146-161）逐项核验：

| # | 检查项 | 结果 | 证据（行号） |
|---|--------|:----:|--------------|
| 1 | name: 小写+连字符、≤64、匹配目录 | ✅ | SKILL.md L2；目录 `053-go-to-market-plan` |
| 2 | description: 第三人称 + WHAT/WHEN/KEYWORDS + ≤1024 字符 | ✅ | L3，约 400 字符，三要素齐备 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | L3 以 "Analyzes / Asks" 起句 |
| 4 | description: 无跨技能路由 | ✅ | L3 无 "NOT for X" |
| 5 | description: 至少一个触发信号短语 | ⚠️ | L3 "Use when user needs…" 偏离规范列举短语（缺 "the"/"to"） |
| 6 | frontmatter: 无白名单外键 | ✅ | L1-4 仅 name/description |
| 7 | body: ≤600 行 | ✅ | body 440 行 |
| 8 | body: 有 workflow/process 节 | ✅ | Execution Logic L12-24 + Task Execution L27-122 |
| 9 | body: 有 output format 节 | ✅ | L172-377 |
| 10 | body: 有 scope/limitations 节 | ❌ | 全文无；最近似者 Writing Rules（L125-169）非范围声明 |
| 11 | body: 无跨技能文件引用 | ✅ | 无 `../` 路径；FOUNDER_CONTEXT.md 为项目文件 |
| 12 | 目录: NNN-kebab-case、无空格大写 | ✅ | `053-go-to-market-plan` |

**合计：10 ✅ / 1 ⚠️ / 1 ❌**。第 10 项缺失属于语料库最大缺口族（dossier 统计约 68% 技能缺 Scope 节，skill-dossier.md L1117），但按规范字面即硬性不达标；第 5 项为措辞级偏离，功能等价。

---

## 8. 人机感

- **语气**：直接、行动导向、零废话——"No motivational fluff. Only actionable GTM strategy."（L134）自身即为示范；全文无 emoji、无全大写喊话式命令（BAD/GOOD 的大写仅为排版对比）。
- **人机分工**：agent 负责生成策略，用户负责执行与验证——"Do This Today" 交付 30-60 分钟内的用户侧动作（L115-117）；"Would I personally bet money that this will produce traction?"（L167、L415）是强烈的自我检验装置，把"可信度门槛"内化为 agent 自检，而非空洞承诺。
- **边界意识**：Quality Checklist 要求 "I assessed product-market fit status based on evidence, not assumptions"（L391）与 "didn't guess"（L388），与 SCORING NEG-02/CF-02（禁止编造业务背景）同构，防护到位。
- **加载语**："go-to-market-plan loaded, proceed with details…"（L18）带 chatbot 腔，但属 $ARGUMENTS 双模式的设计约定（评测 load 模式要求），在 SkillIF 语境下合理，不计为缺陷。
- **示例中人称**：示例内的第一人称（L280 "I'm building DevAnalytics specifically for this problem"）是给用户的文案示范，引用得当，不是对用户的称呼。
- **评分**：9.5/10——专业、克制、无过度拟人，无 emoji 滥用。

---

## 9. 可执行性

- **自包含性**：无外部脚本/参考文件依赖，全部指令内联，开箱可执行 ✅。
- **步骤可执行度**：六步均有明确动作对象（读文件、列问题、分析 6 维度、生成 3 策略、格式化、自检），无抽象口号；每条策略强制附带 step-by-step playbook（L109-113）与 30-60 分钟首日动作（L115-117），示例中均已实例化（如 L278-296 的 outreach 脚本、L307-315 的内容引擎）。
- **质检闭环**：24 项自检清单（L385-422）按"执行前/分析/策略选择/具体性/写作规则/输出"六组组织，可直接当评测运行时的 checkable 行为轨迹。
- **主要风险（问题 A）**：AskUserQuestion（L54）在无该工具的 harness 下无法按字面执行，是整个 skill 唯一"可能不可执行"的指令；回退方案见 §13 P1-2。
- **输出负担**：3 个完整策略 × 5 段结构 + Execution Priority + Success Criteria，输出体量偏大但属本 skill 核心交付物设计使然；模板对 Strategy 2/3 给 `[...]` 缩写示意，agent 可复制，负担可控。
- **评测可跑性**：check.py 两项脚本检查均可稳定判定——SCOPE-02 依赖工具日志中出现 `FOUNDER_CONTEXT.md`（L35），PROC-03 依赖输出含 "Strategy 3:" 等三选一模式（L40），与技能模板（L181 等）强制格式相符，判定条件在技能侧可满足 ✅。

---

## 10. SCORING 交叉参考

**10.1 SCORING.yaml 结构核对（L1-179）**
- `pattern: process`（L2）、`total_items: 20`（L3）✅。
- 20 项分布：scope 3（L7-29）、process 6（L33-78）、output 5（L82-119）、negative 2（L123-136）、qa 4（L140-169）；critical_failures 2（L172-178）。
- `judge: script` 恰好 2 项（SCOPE-02 L18、PROC-03 L50），与 check.py 实现一致 ✅。

**10.2 check.py 实现审查（75 行）**
- L10-16：导入路径解析正确（见 §5）。
- L24-29：`_is_path = os.path.exists(agent_output)` 处理 main() 已读入的文本（L63-65），逻辑正确。
- L35：`tool_log_contains('FOUNDER_CONTEXT\\.md')` — 源码内双反斜杠 → 正则 `FOUNDER_CONTEXT\.md`，转义正确；匹配 Read 调用 JSON dump 中的文件路径 ✅。
- L40：`output_contains("Strategy 3:|Your 3 Go-to-Market|3 (go-to-market|GTM|strateg)")` — 三路交替可命中模板/示例的输出形态 ✅。注意 `output_contains`（checker.py L339-343）用 `re.MULTILINE` 但**大小写敏感**——若 agent 将标题改写为 "Strategy three" 或 "3 GTM" 之外的形式会漏判；技能模板强制 "Strategy 3:" 格式，风险可控，可不改。
- 其余 18 项 LLM 判定依赖评测 harness 的 LLM judge，check.py 无遗漏、无越权。

**10.3 20 项评测与 SKILL.md 正文映射（覆盖度核验）**

| SCORING 项 | 对应正文（SKILL.md） | 覆盖 |
|-----------|---------------------|:----:|
| SCOPE-01 | Execution Logic L14-23 + Purpose L8 | ✅ |
| SCOPE-02 | L31-34（FOUNDER_CONTEXT.md 读取） | ✅ |
| SCOPE-03 | L36-51（就绪度 8 项评估） | ✅ |
| PROC-01 | L53-72（3-10 问、只问必要） | ✅ |
| PROC-02 | L74-89（市场进入 6 维度分析） | ✅ |
| PROC-03 | L92（exactly 3）+ 模板 L181/206/225 | ✅ |
| PROC-04 | L104-117（A/B/C 三部分） | ✅ |
| PROC-05 | L129-146（Specificity Rules + BAD/GOOD） | ✅ |
| PROC-06 | L148-159（阶段 × 业务类型适配） | ✅ |
| OUT-01 | 模板 L174-260（playbook/metrics/milestones/Do This Today） | ✅ |
| OUT-02 | L244-248（Execution Priority 排序解释） | ✅ |
| OUT-03 | L252-259（Success Criteria 分策略） | ✅ |
| OUT-04 | L193-199 / L286-296（可量化指标 + 时间线里程碑） | ✅ |
| OUT-05 | L441 指令 ✅ 但模板 L174-260 **无 Assumptions 占位** | ⚠️ |
| NEG-01 | L129、L139-146、L412（零泛化建议） | ✅ |
| NEG-02 | L72、L388（不猜测、用提问） | ✅ |
| QA-01 | L161-168（Quality Filters 5 问） | ✅ |
| QA-02 | L399（三策略不同角度、无重叠） | ✅ |
| QA-03 | L134、L414-415（无 fluff、主动语态、赌注测试） | ✅ |
| QA-04 | L136、L400（资源约束内可执行） | ✅ |
| CF-01 | L129/L412（泛化建议 cap_to_0，与技能红线同构） | ✅ |
| CF-02 | L72/L388（编造背景 cap_to_0） | ✅ |

- **覆盖度评价**：22 项（含 CF）在正文均有对应指令，覆盖度 100%；唯一薄弱点是 OUT-05 的模板侧缺口（问题 C，→ §13 P2-6）。
- **判定风险提示**：PROC-03 依赖输出字面含 "Strategy 3:"——若 agent 严格照模板执行则必过；OUT-01 的 LLM 判定依赖模板结构的精确复现，模板本身给出完整骨架，判定公平性良好。

---

## 11. dossier 汇总

**11.1 既有 dossier 条目（skill-dossier.md L441-446）**
- 评级 **🟢**；四维评语与我方结论对照：
  - 逻辑："Step 1-6 工作流闭环完整…但依赖 AskUserQuestion tool" — 与本次问题 A 完全一致 ✅。
  - 语法："规范流畅，BAD/GOOD 对比示例结构清晰" — 与 §6 一致 ✅。
  - 人机感："直接、行动导向，无 emoji、无废话" — 与 §8 一致 ✅。
  - 合规："含 Execution Logic/Workflow/Output Format/Checklist 各节，正文 444 行 ≤600" — **口径偏宽松**：将 Checklist 计入必需节，未检出 Scope 节缺失。按 SKILL-SPEC §3.1 严格口径应为 10/12（见 §7）。dossier 的 🟢 与语料库约 68% 缺 Scope 的现实一致（skill-dossier.md L1117），但严格口径下 053 存在 1 项硬性缺口。
- **总评**："🟢 结构完整、约束明确，仅 AskUserQuestion 工具依赖需按环境适配。" — 认可，附加 3 项本次新发现（触发短语、OUT-05 模板脱节、Scope 缺失）。

**11.2 旧 REVIEW.md 占位（4 行）**
- L3 "444 行、三必需节基本齐全" — "基本齐全"表述与实测不符：三必需节实际只有两节（缺 Scope）。
- L4 "综合: 🟢 B+ (54/100)" — 54/100 无任何计算依据，与 dossier 🟢 及内容质量明显不匹配（对比语料库 🟡 典型问题仅为"缺节/微调"级）。本次以 8 维加权重算为 **87/100**（§12），等级 B+ 保留，分值以证据修正。

**11.3 语料库定位**
- 按 dossier 汇总（skill-dossier.md L1102-1124）：053 属于"内容与结构质量前列、仅差规范补齐"的群体——修复 Scope 节 + 触发短语后即进入 🟢 典范组（与 054-oss-review 等 278 行三节齐全者的差距仅在结构节层面）。

---

## 12. 综合评分（8 维加权 + A/B/C/D）

**12.1 评分表（权重合计 100%）**

| 维度 | 权重 | 得分 | 加权 | 主要依据 |
|------|:----:|:----:|:----:|----------|
| D1 Frontmatter 与 Description | 10% | 9.0 | 0.90 | 仅触发短语措辞偏离（§2） |
| D2 Body 结构完整性 | 15% | 8.0 | 1.20 | 缺 Scope 节（§3/§7）；其余结构优秀 |
| D3 逻辑一致性 | 15% | 9.0 | 1.35 | 六步闭环 + 示例数字自洽；A-E 五项轻微问题（§4） |
| D4 参考文件完整性 | 5% | 9.0 | 0.45 | 自包含、零跨技能引用；FOUNDER_CONTEXT 无模板（§5） |
| D5 语法与格式 | 10% | 9.5 | 0.95 | 全文无错别字；仅 H1 连字符小瑕疵（§6） |
| D6 SKILL-SPEC 合规 12 项 | 20% | 8.5 | 1.70 | 10✅/1⚠️/1❌（§7） |
| D7 人机感 | 10% | 9.5 | 0.95 | 专业克制、边界清晰；加载语为设计约定（§8） |
| D8 可执行性 | 15% | 8.0 | 1.20 | AskUserQuestion 依赖 + OUT-05 模板缺口（§9） |
| **合计** | **100%** | — | **8.70** | **87/100** |

**12.2 等级判定**
- 档位定义：A ≥ 90 / B+ 80-89 / B 70-79 / C 60-69 / D < 60。
- **综合等级：B+（87/100）** —— B 档上限，距 A 档仅差 3 分。
- 失分集中于 D2/D6（结构合规）与 D8（可执行性风险）三处，全部为"可修复"级问题；内容质量（D3/D5/D7）已达语料库前列水平（对标 dossier 🟢 典范组）。

**12.3 修复后预期**
- 完成 P1 三项（Scope 节、AskUserQuestion 回退、触发短语）后：D2 → 9.5、D6 → 9.5、D8 → 9.0，加权约 92-94/100 → **A 档**。
- 完成 P2 三项（流程回环、问题集补全、Assumptions 占位）后可达 95+，具备进入 🟢 典范组的充分条件。

---

## 13. 修复建议 ★重点★

按优先级分组（P1 必修 → P3 可选），每条给出：问题 → 证据（行号）→ 修复方案（含可直接粘贴的文本）→ 影响（规范项/评测项）。共 10 条建议 + 3 个附录。

### P1 — 必修（影响规范达标或评测稳定性）

**P1-1 补 Scope/Limitations 节（最高优先）**
- **问题**：SKILL-SPEC §3.1 三必需节缺一（§7 第 10 项 ❌）。
- **证据**：SKILL.md 全文 444 行无 Scope/Limitations 类节；最近似者 Writing Rules（L125-169）是写作约束、Defaults & Assumptions（L428-443）是默认值，均不构成范围声明。
- **方案**：在 Writing Rules 末尾（L169 与 L172 之间）插入以下节（可直接粘贴）：

```markdown
## Scope & Limitations

**What this skill delivers:**
- 3 套按适配度排序的可执行 GTM 策略（策略、playbook、首日行动、指标、里程碑）
- 覆盖 pre-PMF（验证）、post-PMF（可复制获客）、scaling（扩张）三阶段，
  以及 B2B / B2C / marketplace / developer tools 四类业务

**What this skill does NOT do:**
- 不代替用户执行落地动作（投放、发帖、建群、签约等）
- 不提供定价精算、财务预测、融资或法务意见（如需，请转相应专业技能或顾问）
- 不保证业绩结果；所有策略假设需用户以数据验证
- 不编造用户未提供的业务背景（ICP、指标、市场地位）——缺失信息一律走提问流程

**When NOT to use:**
- 用户仅需单点答案（如单一定价问题、单一渠道问题）而非完整 GTM 方案
- 用户已具备成熟 GTM 体系、仅需执行督导
- 用户要求绕过诊断与提问直接输出——本技能必须基于真实上下文生成
```

- **影响**：合规 12 项 10→11/12（配合 P1-3 后 12/12）；同时给 CF-02/NEG-02 的 LLM 判定提供正文锚点，且为语料库最大缺口族（~68%，skill-dossier.md L1117）再消一例。
- **成本**：+14 行，正文 454 行，远低于 600 行上限。

**P1-2 AskUserQuestion 工具依赖增加回退路径（可执行性风险）**
- **问题**：唯一可能"无法按字面执行"的指令；多 harness 测评（2 Mode × 5 Harness）下部分环境无此工具 → PROC-01/NEG-02 假失败风险。
- **证据**：L54 "Use the AskUserQuestion tool to gather missing information."；L388 "I used AskUserQuestion to gather it"；description L3 "Asks up to 10 diagnostic questions when needed"。
- **方案**：
  - L54 改为：`Use the AskUserQuestion tool to gather missing information (ask between 3-10 questions based on what's needed). If AskUserQuestion is unavailable in the current environment, ask the same questions in plain text in the conversation and wait for the user's answers.`
  - L388 同步改为：`I used AskUserQuestion (or plain-text questions when the tool is unavailable) to gather missing information (and didn't guess)`
- **影响**：消除跨 harness 不可执行风险；保留工具优先、回退兜底的双轨设计，不改变 skill 语义。

**P1-3 description 触发短语对齐规范信号（合规微调）**
- **问题**："Use when user needs…" 缺 "the"/"to"，非 SKILL-SPEC §2.4 列举信号短语的精确形式（§2/§7 第 5 项 ⚠️）。
- **证据**：SKILL.md L3；对照 SKILL-SPEC L60-66 信号列表。
- **方案**（二选一）：
  - 方案一（最小改动）：`Use when the user needs a go-to-market strategy, launch plan, market entry strategy, or actionable GTM roadmap.`
  - 方案二（更贴近列举短语）：`Use when the user asks for a go-to-market strategy, launch planning, market entry strategy, or actionable GTM roadmap.`
- **影响**：合规第 5 项 ⚠️→✅；在"无 trigger 对照集"测评（记忆中的对照集设计）中提升触发区分度；对 description 语义无实质影响。

### P2 — 建议修复（结构/一致性完善）

**P2-4 Step 2→3→4 流程回环显式化**
- **证据**：L49-51（分支只写了"信息充足 → Step 4"，未写"提问后 → 重新评估"）。
- **方案**：在 L51 后补一句：`After Step 3, re-check the Step 2 required-information list; proceed to Step 4 only when the list is complete or the user explicitly overrides it.`
- **影响**：SCOPE-03/PROC-01 的 LLM 判定有明确流程参照，消除隐含跳转。

**P2-5 Step 3 问题集补 "Distribution model" 覆盖**
- **证据**：Step 2 必需信息含分发模式（L45），Step 3 核心问题（L56-63）无对应提问。
- **方案**：在 Core GTM questions 追加一条：`- How do you plan to reach customers — direct sales, channel partners, marketplace, or self-serve?`
- **影响**：8 项必需信息 → 8 项均有对应提问，SCOPE-03 判定更稳；顺带补强 PROC-02 的渠道分析输入。

**P2-6 Output Format 模板补 Assumptions 占位（OUT-05 判定锚点）**
- **证据**：L441 指令 vs L174-179 模板开头无占位、L265-267 示例开头无假设说明。
- **方案**：
  - 模板 L175（"## Your 3 Go-to-Market Strategies" 之前）插入：`**Assumptions:** [state assumptions about stage, budget, timeline, metrics here]`
  - 示例 L267 后补一行实例：`**Assumptions:** ~$2k/month budget, 2 founders (1 eng / 1 growth), 60-day initial traction window.`
- **影响**：OUT-05 LLM 判定有据可依；指令（L441）与模板脱节消除。

**P2-7 体量管理：完整示例下沉 references/（可选优化）**
- **证据**：L262-377 约 115 行示例；SKILL-SPEC §3.2 process 目标 ~200 行，当前 440 行超 2 倍。
- **方案**：将示例移至 `references/example-output.md`，正文 Output Format 保留模板（L174-260）+ 一行指引：`See references/example-output.md for a fully worked example.` 同时补 P1-1 的 Scope 节后正文约 330-350 行，回落 process 目标区间。
- **影响**：体量与可维护性改善；`references/` 内相对路径符合 SKILL-SPEC §3.3。**注意**：Quality Checklist 及 SCORING 均不引用示例具体内容，下沉不破坏任何评测项；若不愿改动（当前仍在 600 行内），此项可不做。

### P3 — 锦上添花

**P3-8 提供 FOUNDER_CONTEXT.md 最小结构模板**
- **证据**：L32-34 依赖该文件但未定义结构。
- **方案**：在正文 Step 1 后附最小字段清单（company name / industry / target audience (ICP) / value proposition / products & services / stage / competitors / pricing / distribution / resources），或下沉 `references/founder-context-template.md`。
- **影响**：SCOPE-02 字段提取稳定性提升；降低用户准备成本。

**P3-9 Step 5/6 显式路由 Writing Rules**
- **证据**：L119-122 只引 Output Format 与 Quality Checklist；L125-126 "Hard constraints" 无调用点。
- **方案**：L91（Step 5 首行）加 `All strategies must comply with the Writing Rules below (hard constraints, no interpretation).`
- **影响**：约束链闭环，NEG-01/QA-01 判定更稳。

**P3-10 check.py 可选加固（低优先）**
- **证据**：check.py L40（大小写敏感的三路交替）。
- **方案**：`output_contains("Strategy 3:|Your 3 Go-to-Market|3 (go-to-market|GTM|strateg)")` 可加 `(?i)` 前缀或补充 "Strategy 2:" 锚点；当前实现正确、模板已强制格式，仅作防误判加固，非必需。
- **影响**：降低极端改写下的漏判；保持 2 项 script 检查与 SCORING 标注一致，无需增减。

---

### 附录 A — 行级问题清单

| # | 位置（SKILL.md 行号） | 问题 | 类型 | 严重度 | 影响项 |
|---|----------------------|------|------|:------:|--------|
| A1 | 全文（无 Scope 节） | 缺 Scope/Limitations 必需节 | 规范 | 高 | 合规 12 项 #10 |
| A2 | L54 / L388 / L3 | AskUserQuestion 工具依赖无回退 | 可执行性 | 高 | PROC-01、NEG-02 |
| A3 | L3 | 触发短语缺 "the"/"to" | 规范 | 中 | 合规 12 项 #5 |
| A4 | L441 vs L174-260 | Assumptions 指令无模板占位 | 一致 | 中 | OUT-05 |
| A5 | L49-51 | 提问后无显式回环评估 | 一致 | 低 | SCOPE-03 |
| A6 | L45 vs L56-63 | 问题集缺 distribution model | 覆盖 | 低 | SCOPE-03 |
| A7 | L91-122 | Step 5/6 未路由 Writing Rules | 一致 | 低 | QA-01 |
| A8 | L5 | H1 连字符不统一（Go To vs go-to-） | 格式 | 低 | 无（装饰性） |
| A9 | L32-34 | FOUNDER_CONTEXT.md 无结构模板 | 体验 | 低 | SCOPE-02 |
| A10 | check.py L40 | 脚本判定大小写敏感 | 评测 | 低 | PROC-03（风险可控） |

### 附录 B — SKILL-SPEC 12 项合规明细（修复后预期）

| 项 | 现状 | P1 修复后 | P1+P2 修复后 |
|----|:----:|:--------:|:------------:|
| 1-4, 6-9, 11-12（10 项） | ✅ | ✅ | ✅ |
| 5 触发短语 | ⚠️ | ✅（P1-3） | ✅ |
| 10 Scope 节 | ❌ | ✅（P1-1） | ✅ |
| 达标数 | 10/12 | 12/12 | 12/12 |

### 附录 C — 修复后回归检查清单

- [ ] SKILL.md body 仍 ≤600 行（预期 450-460 行）
- [ ] Output Format 模板与新增 Assumptions 占位在示例中同步（P2-6）
- [ ] Quality Checklist L385-422 与新增 Scope 节无措辞冲突
- [ ] description 修改后仍 ≤1024 字符、第三人称、无路由
- [ ] 若执行 P2-7：`references/example-output.md` 路径为相对引用，正文留指引行
- [ ] 重新跑 check.py：SCOPE-02（工具日志含 FOUNDER_CONTEXT.md）、PROC-03（输出含 "Strategy 3:"）仍可判定
- [ ] SCORING.yaml 20 项无需改动（本审查未发现评测标准侧缺陷）

---

*审查完毕。总评：🟢 上乘之作，8 维加权 87/100（B+）；完成 P1 三项修复后即可完全达标（A 档），建议在本次测评运行前至少完成 P1-1 与 P1-2。*
