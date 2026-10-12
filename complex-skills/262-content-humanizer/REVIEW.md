# Skill 262-content-humanizer 审查报告（REVIEW）

> 审查日期：2026-08-06
> 审查对象：`D:\SkillIF\skill-experiment\complex-skills\262-content-humanizer\`
> 审查人：SkillIF 质量审计（Agent 审计流程）
> 审查依据：`_shared/SKILL-SPEC.md` v1.0、SkillIF 科研设计（2 Mode × 5 Harness 测评矩阵）、322 技能语料库审查惯例（Dossier 五维评估法：逻辑、语法、人机感、合规、总评）
> 评级预案：🟢 好 / 🟡 可用但有小问题 / 🟠 需修复 / 🔴 严重问题

---

## 一、概览与元信息

### 1.1 技能定位

本 skill 是一个**内容改写型（process 型）**技能：将 AI 生成的文本改写为"听起来像真人写的"内容。核心方法论是**三模式管线**：

| 模式 | 名称 | 职责 |
|------|------|------|
| Mode 1 | Detect — AI Pattern Analysis | 对文本做 AI 指纹审计，按类别命名问题并打严重度 |
| Mode 2 | Humanize — Pattern Removal and Rhythm Repair | 移除 AI 模式、修复句律、以具体替换笼统 |
| Mode 3 | Voice Injection — Brand Character | 注入品牌性格，完成从"人"到"这家品牌的人"的转换 |

三模式与 SKILL.md 开头的 "How This Skill Works"（L29-40）声明一致，且 SCORING.yaml 的评分点（SCOPE-01、PROC-01~09）逐条映射到三个模式，形成 skill 正文 → 评分点的完整链路。这是本 skill 最大的结构优点。

### 1.2 文件资产清单

| 文件 | 大小/行数 | 状态 |
|------|-----------|------|
| SKILL.md | 254 行 | 存在，正文完整，无截断 |
| SCORING.yaml | 153 行 | 存在，YAML 合法，16 个检查项 |
| check.py | 63 行 | 存在，Python 可编译，1 个脚本检查项 |
| references/（目录） | — | **不存在**（SKILL.md L174 引用了 `references/voice-techniques.md`） |
| scripts/（目录） | — | **不存在**（SKILL.md L232 与 SCORING.yaml QA-01 引用了 `scripts/humanizer_scorer.py`） |
| marketing-context.md | — | 不存在（属于工作区可选输入，非 skill 自带资产，合规） |
| EVAL.md / README.md | — | 不存在（语料库中多数 skill 亦无，不视为缺陷） |

### 1.3 评级速览（先行结论）

**总评：🟡 可用但有小问题。** 核心三模式逻辑自洽、description 合规、评分点与正文对应良好、正文自身"人机感"水准高（一个教人写得更像人的 skill 自己读起来就像人写的）。但存在**两个悬空引用**（references/voice-techniques.md 与 scripts/humanizer_scorer.py 均不存在）、**一处葡萄牙语泄漏**、**评分项 QA-01 依赖不存在的脚本而必然失真**、以及**缺 Scope/Limitations 节**等实质性问题。修复 F-01~F-04 后可达到 🟢 水准。

---

## 二、审查范围与方法

### 2.1 审查对象

对 `262-content-humanizer` 目录下**全部 3 个文件**逐一完整阅读：

1. `SKILL.md`（254 行，逐行审查）
2. `SCORING.yaml`（153 行，逐项审查，重点核对 total_items 计数、judge 类型、check 字段质量、critical_failures 与正文规则的对应关系）
3. `check.py`（63 行，逐行审查，核对与 _shared/checker.py 的接口契约、result key 与 SCORING.yaml 的一致性）

### 2.2 审查维度

沿用 Dossier 五维评估法并扩展为适用于"skill + 评分系统"的审查框架：

| # | 维度 | 检查内容 |
|---|------|---------|
| 1 | 逻辑一致性 | 三模式步骤自洽、正文规则与 SCORING/check.py 对应、无内部矛盾 |
| 2 | 语法与可读性 | 拼写、病句、语言混杂、标点滥用 |
| 3 | 人机感 | 语气是否自然、emoji 是否功能性、是否过度口语化或机械 |
| 4 | 规范合规性 | SKILL-SPEC.md v1.0：description 第三人称+触发、必需节、行数限制、跨 skill 引用规则 |
| 5 | 引用完整性 | references/、scripts/ 引用是否真实存在 |
| 6 | 评分系统质量 | SCORING.yaml 检查项可判定性、judge 类型匹配、CF 设计、check.py 可执行性 |
| 7 | 测评可用性 | 在 2 Mode × 5 Harness 矩阵下检查项是否可通过、依赖哪些工作区前提 |

### 2.3 审查限制

- 本审查不评估 skill 实际执行效果（未运行评测），只做静态审计。
- `_shared/checker.py` 未在本目录内，其函数签名以 `CHECKER-LIBRARY.md` 记录的契约为准；check.py 与库的接口调用方式（`set_tool_log_path` / `set_agent_output` / `tool_log_contains`）与语料库 322 个 check.py 的通用模式一致，视为符合契约。

---

## 三、文件清单与资产完整性

### 3.1 资产完整性结论

目录中只有 3 个文件，**没有任何 external 资产目录**。SKILL.md 引用了两个外部文件，均不存在：

| 引用位置 | 引用内容 | 实际存在？ |
|---------|---------|:--------:|
| SKILL.md L174 | `references/voice-techniques.md`（Mode 3 引导"See references/voice-techniques.md"） | ❌ 不存在 |
| SKILL.md L232 | `scripts/humanizer_scorer.py`（Output Artifacts 表："Humanity score \| Run `scripts/humanizer_scorer.py`"） | ❌ 不存在 |
| SCORING.yaml L139 | QA-01 检查 `scripts/humanizer_scorer\.py` 出现在工具日志 | ❌ 依赖同一缺失脚本 |

### 3.2 缺失引用的影响评估

**F-02（中）：`references/voice-techniques.md` 缺失。**
Mode 3 是"Voice Injection"，其方法论核心之一是"See references/voice-techniques.md for specific techniques for each voice type"（L174）。文件不存在时：
- agent 若尝试读取会得到不存在提示，可能自行发挥——与"品牌蓝图为准"的约束产生冲突；
- 该引用是 Mode 3 的唯一深化入口，缺失使 Mode 3 的"每种 voice type 的具体技法"悬空，PROC-08（提取并一致应用 voice 模式）的判定失去权威参照。
- 语料库中同类问题被标记为 🟠（如 195-backend-dev-guidelines 参考链接全部指向错误路径、196-cold-email 引用文件全部缺失、188-free-tool-strategy 脚本缺失），本 skill 因 body 主体内容完整、该引用仅属补充深化，严重度降为"中"。

**F-03（高）：`scripts/humanizer_scorer.py` 缺失。**
这是本 skill 最严重的单项问题，且影响超出 skill 自身：
- SKILL.md L232 明确要求 agent 在用户索要 Humanity score 时运行该脚本（"score 0-100 with breakdown by signal type"）；
- SCORING.yaml QA-01（L135-139）正是以"工具日志中出现 `scripts/humanizer_scorer.py`"作为唯一的脚本可判定检查项；
- 脚本不存在 → **QA-01 在评测中要么必然失败（agent 诚实检查文件后发现不存在而放弃执行），要么被"硬跑"并报错（污染工具日志）**。无论哪种，该检查项都无法公平测出技能遵从度；
- 修复选项：① 编写真实可运行的 `scripts/humanizer_scorer.py`（按信号类型输出 0-100 分）；② 将 QA-01 改为可机械判定的替代检查（如要求 agent 输出数字分数，用 `output_contains` 匹配）；③ 从 SKILL.md 与 SCORING.yaml 同步移除该能力。**必须三文件联动修改**，否则测评结果系统性失真。

### 3.3 不存在即合规的项

- `marketing-context.md`：SKILL.md 将其定位为**工作区可选输入**（"If `marketing-context.md` exists, read it"，L15），属于测评时由任务 prompt 提供的工作区文件，不是 skill 自带资产，不构成缺失。但需注意：**测评任务必须提供该文件**，SCOPE-02 才能通过（详见第十一节 F-09）。

---

## 四、Frontmatter 与 Description 审查

### 4.1 结构合规

```yaml
---
name: content-humanizer
description: Rewrites AI-generated content to sound genuinely human with natural voice,
  varied sentence rhythm, and authentic personality. Use when content feels robotic,
  uses too many clichés, has uniform sentence length, or needs to pass as human-written.
---
```

- **name**：`content-humanizer`，小写连字符格式，与目录名 `262-content-humanizer` 的 slug 部分一致，无空格、无大写，符合规范。
- **frontmatter**：仅含 name 与 description 两个标准 key，无 `trigger: explicit`、`model: inherit` 等非标准字段（对比 065-startup-analyst 的 `model: inherit` 违规，本 skill 干净）。
- **description 人称**：第三人称开头（"Rewrites..."），符合 §2.3 要求。
- **description 触发词**：含 `Use when...` 触发结构（"Use when content feels robotic, uses too many clichés, has uniform sentence length..."），符合 trigger 设计规范（统一格式 `<WHAT>. Use when the user <TRIGGERS>.`）。与无 trigger 对照集的切除逻辑兼容（可切除 "Use when..." 部分）。
- **description 长度**：适中（约 35 词），无截断、无尾部悬挂（对比 047/314 的截断 description，本 skill 无此问题）。

### 4.2 Description 内容审查

**优点：** WHAT（重写 AI 文本使其像真人书写）+ WHEN（内容机械感强、套话多、句长均匀）双要素齐全，且"内容机械化"的触发信号具体可感，有利于 Claude Code Skill tool 的 description 匹配激活。四个触发信号（robotic / clichés / uniform sentence length / needs to pass as human-written）覆盖了 Mode 1 的核心指纹类别，与正文呼应良好。

**F-06（低-中，伦理定位）：** 最后一个触发短语 "or needs to pass as human-written"（L3）将技能明确定位为"让 AI 文本通过人工审查"。在学术诚信、作者身份披露（authorship disclosure）等场景下，该表述可能被解读为协助欺骗（deception facilitation）：
- 正文 Mode 2 的示例与技法本身都在训练"AI 痕迹清除"，方向一致；
- 建议在 Scope/Limitations 节（见 F-04）中显式声明边界，如："本技能用于改善文字质量与品牌一致性；不得用于需要披露 AI 生成身份的学术、法律或监管场景"，并给出拒绝话术（对比 127-policy-redraft 的拒绝话术设计，语料库已有成熟先例）；
- 此问题不阻断使用，但作为面向大众分发的 skill，定位表述值得收紧。

### 4.3 小结

Description 合规性在 322 技能中属前 30% 水平：无语法违规、无跨 skill 路由（对比 148/251 的 description 路由违规）、无截断。仅伦理定位一项建议补强。

---

## 五、SKILL.md 正文结构合规性

### 5.1 结构总览

| 节 | 位置 | 行数占比 | 评价 |
|----|------|:--------:|------|
| 角色定位声明 | L8-10 | ~3 | 有力，直接建立 persona |
| Before You Begin（上下文检查+输入清单） | L12-25 | ~10 | 良好，对应 SCOPE-02/03 |
| How This Skill Works（三模式总览） | L27-40 | ~12 | 良好，总览先行 |
| Mode 1: Detect | L44-88 | ~45 | 7 类 AI 指纹，带严重度 |
| Mode 2: Humanize | L92-155 | ~64 | 4 个子技法（替换/句律/具体化/段落结构/不完美） |
| Mode 3: Voice Injection | L159-208 | ~50 | 蓝图读取+5 种注入技法+Before/After 示例 |
| Proactive Triggers | L212-220 | ~9 | 5 个主动触发场景 |
| Output Artifacts | L224-232 | ~9 | 输出物表 |
| Communication | L236-244 | ~9 | 输出沟通规范 |
| Related Skills | L248-254 | ~7 | 4 个关联技能（仅名称引用） |
| **Scope / Limitations 节** | **—** | **0%** | **缺失（F-04）** |

### 5.2 必需节合规分析（对照 SKILL-SPEC）

- **Workflow 节**：✅ 以三模式展开，每一步都有明确动作指令，非清单堆砌，有实质过程描述。
- **Output 节**：🟡 部分覆盖。"Output Artifacts"表（L224-232）以"用户要什么→得到什么"的形式列出 5 类交付物，但没有**输出模板/结构定义**（如审计报告应包含哪些字段、注释格式如何标记），也没有输出自检清单。对比 158/197 等有严格模板的 skill，本 skill 交付物自由度高，OUT-01/OUT-02 的判定将依赖 LLM 主观判断（详见第十一节）。
- **Scope / Limitations 节**：❌ **缺失**。这是语料库最常见的规范缺口（约 68% 的 skill 缺此节），本 skill 亦未豁免：
  - 无"何时不适用"声明（如：不需要披露 AI 身份的场合、纯事实核查任务、非英文内容、短文案——Related Skills 中 copywriting 暗示了长文/短文分工，但未在自身边界中显式声明）；
  - 无能力边界（不能编造数据——该约束散落在 Mode 2 与 CF-02 中，未在正文显式集中声明为边界）；
  - 无输入格式边界（接受什么格式的输入文本）；
  - 建议补一节，内容可包括：不用于需要披露 AI 身份的场合（呼应 F-06）、不编造事实数据（呼应 CF-02）、不适用于极短文案（<50 词）、输入输出语言一致性等。

### 5.3 行数合规

正文 254 行，远低于 600 行上限；无截断、无残留模板脚手架、无 "tpl-situacao" 类模板缺陷（编号断裂、杂散 `**` 等在本 skill 中均未出现）。按语料库惯例，"体量偏小但完整"优于"超长注水"，此处是加分项。

### 5.4 跨 skill 引用合规

Related Skills 节（L248-254）以**纯名称**引用 content-production / copywriting / content-strategy / ai-seo，无路径引用、无 `../` 跨技能路径（对比 003/013 的路径违规），符合 §2.5。且每条引用都给出了"何时用哪个"的说明（"Run content-humanizer after drafting, before the SEO optimization pass"），路由信息清晰。

---

## 六、逻辑一致性审查

### 6.1 三模式管线自洽性

- **顺序依赖成立**：Detect（诊断）→ Humanize（清除）→ Voice Injection（注入）的递进关系清晰；L40 "Run all three in one pass when you have enough context. Separate them when the client needs to review the audit before you edit." 给出了串行/并行两种执行模式，与 SCOPE-01 "as needed" 的措辞对齐。
- **模式间不重叠**：Mode 1 只诊断不改写（"This is diagnosis — not editorial"，L32）；Mode 2 只做通用化修复不注入品牌；Mode 3 才动品牌性格。职责边界干净，无循环依赖。
- **内部计数一致**：Mode 1 列 7 类指纹、Mode 2 列 5 个子技法（替换/句律/具体化/段落结构/不完美）、Mode 3 列 5 种注入技法，正文标题、内容、示例三者互不矛盾。

### 6.2 正文规则 ↔ SCORING.yaml ↔ CF 的对应链

| 正文规则 | 评分点 | 一致性 |
|---------|--------|:------:|
| L15 读 marketing-context.md 作蓝图 | SCOPE-02 | ✅ |
| L21-23 收集内容/品牌/受众/目标 | SCOPE-03 | ✅ |
| L46 按类别+严重度审计 | PROC-01 | ✅ |
| L216 10+ tells/500 词 → 全重写 | PROC-02 | ✅ |
| L218 5+ 笼统声明 → 上报 | PROC-03 | ✅ |
| L98 "Never just delete — always replace" | PROC-04 + CF-03 | ✅ |
| L113-119 句长变化 | PROC-05 | ✅ |
| L126-136 具体化/诚实不确定，不编数据 | PROC-06 + CF-02 | ✅ |
| L140-146 段落结构变化 | PROC-07 | ✅ |
| L167-172 从蓝图提取 voice 模式 | PROC-08 | ✅ |
| L178-191 五种注入技法 | PROC-09 | ✅ |
| L220-221 保留好段落/一致性 | NEG-01 | ✅ |
| L232 运行 humanizer_scorer.py | QA-01 | ⚠️ 依赖缺失脚本（F-03） |

对应链完整度在语料库中属上游水平（15 个 LLM 项全部有正文锚点），无"评分点无出处"或"正文无评分点覆盖"的孤儿项。这是本 skill 逻辑设计最强的部分。

### 6.3 内部张力检查

- **CF-02 vs Mode 2 示例（F-05，中）**：CF-02 规定"编造具体事实/研究/统计 → 总分归零"，但 Mode 2 的 Before/After 示例（L130-133）给出的"After"版本引用了高度具体的数据："HubSpot published their onboarding funnel data in 2023 — companies that hit their first moment of value within 7 days showed 40% higher retention at 90 days. That's not margin of error." 该数据**无出处、无法在 skill 内验证**，与 CF-02 惩罚的行为高度同构。影响：
  1. 语义层面：skill 以疑似虚构的具体数字示范"具体化"，自身就是 CF-02 的反例示范——agent 若模仿示例写法（堆具体数字）会触发 cap_to_0；
  2. 评测层面：CF-02 判定依赖 LLM 判断"agent 是否编造"，而 skill 示例提供了"看起来像编造但正当"的模棱两可模板，加大判定噪音；
  3. 建议：将该示例改为"显式标注为示意性数字"（如添加"示例数据，非真实引用"），或替换为可验证的真实案例，使示例与规则严格一致。
- **Em-dash 教授者自身使用偏多（F-08，低）**：Mode 1 将"em-dash 每段出现"标记为 AI 指纹（🟡，L70-71），但 skill 正文自身使用了约 10 处 em-dash（如 L23、L85、L105、L217-221 等，不含小标题分隔用法），密度约每 20 行 1 处。虽然远未到"每段一个"的红线，但作为专门教人克制 em-dash 的技能，自身示例偏多略显讽刺。建议将正文中的 em-dash 部分改写为逗号/冒号/句号，以身作则。
- **"Actions have owners and deadlines" 语境错位（F-07，低）**：Communication 节（L241）要求"Actions have owners and deadlines — no 'you might want to consider'"。这是一套项目管理/咨询框架的输出规范，对**写作交付物**而言"owner 和 deadline"没有定义载体（谁是有 owner？deadline 是何时？）。正文从未解释该条在改写场景中如何落地，属从其他框架搬运的残留。建议改为写作场景可落地的等价约束（如"给出可直接粘贴的替换句"），或删除该条。
- **未定义最终验证步骤（F-11，低）**：三模式跑完后没有任何"重扫验证"步骤（如：对改写稿再跑一遍 Mode 1 的 7 类指纹检查确认密度下降、核对未引入新的事实错误）。语料库中高质量的 process 型 skill 普遍带验证闭环（如 008-tdd 的测试门、279 的证据通道）。补一个"Mode 4: Verify（可选）"或 Output 自检清单即可，同时可缓解 OUT-01/02 判定主观性问题。

---

## 七、内容质量与示例审查

### 7.1 方法论深度

- **7 类 AI 指纹分类**（L50-88）：filler 词清单具体到词（delve/landscape/crucial/leverage/furthermore...）、hedging 链给出句式原文、"具体性缺失"给出"笼统说法 → 该问什么"的对应（"Many companies → which companies?"）。这是本 skill 内容最扎实的部分，训练数据驱动的措辞识别具备实操价值。
- **替换表**（L100-109）：8 行 AI 短语 → 人类替代，替换建议质量高（"furthermore → nothing (just start the next sentence)" 尤其好）。
- **句律模式**（L121-124）："Long. Short. Long, long. Short."、"Question? Answer. Proof." 等模式可作为可执行指令，对 agent 而言可操作性高于抽象描述。
- **"诚实的不确定"范式**（L134-135）："I haven't seen controlled studies on this, but in my experience..." 为 CF-02 提供了正面的行为样本，是罕见的"用正面示范约束负面行为"的设计。

### 7.2 示例质量

- **Before/After 完整示例**（L195-207）：Before 文本集中了 crucial/leverage/navigate/robust/ensure/significantly/furthermore 七个指纹词，After 文本示范了直接称呼、短句收尾、具体指涉，且"What changed"逐项列出，教学价值高。
- 细节核对：L207 "Removed: ... 'significantly' ..." 与 Before 文本中 "reduce churn significantly" 吻合，无张冠李戴（对比 074 的示例数字矛盾，此处无此问题）。
- 唯一瑕疵即 7.1 提到的 F-05（HubSpot 数字疑似虚构），其余示例自洽。

### 7.3 缺失内容盘点

| 缺失项 | 影响 | 优先级 |
|--------|------|:------:|
| 每种 voice type 的具体技法（references/voice-techniques.md） | Mode 3 深化不足 | 高（F-02） |
| Humanity score 的"signal type"定义（scripts/humanizer_scorer.py） | 分数不可解释 | 高（F-03） |
| 输出模板（审计注释格式、交付结构） | 交付物不稳定 | 中 |
| 最终验证/自检清单 | 质量闭环缺失 | 中（F-11） |

---

## 八、语法与语言质量审查

### 8.1 语言整体评价

正文英语整体流畅、地道，写作风格本身即是"humanized"的示范：短句、fragment（"Like this."、"Too complete."）、设问（"According to what?"）、括号补注——对"教人写人话"的技能而言，语气与内容高度统一，是加分项。

### 8.2 具体缺陷

**F-01（中，葡萄牙语泄漏）：L105 替换表单元格混入葡萄牙语**

```
| "crucial" / "vital" | "the part that actually matters", "the one thing", or just
  state the thing — deixe que seja autoevidentemente importante |
```

`deixe que seja autoevidentemente importante`（葡萄牙语，意为"让它不言自明地重要"）突兀地出现在英语替换表中。问题：
- 该格是"crucial/vital 的替代方案"，葡萄牙语短语与上下文语义脱节，agent 无法执行；
- 一个以"语言质量"为核心卖点的 skill 混入外语，讽刺且损害可信度；
- 语料库中存在同类问题（276 混入葡语标题 "Exemplos de Loops"、306 混入葡语参考文件名），Dossier 已将 262 的此问题记录在案（batch 251-275）；
- 修复建议：删除该短语，改为 "or just state the thing — let it be self-evidently important" 或直接以"cut it"收尾。

### 8.3 其他语法检查

- 无拼写错误、无病句、无标点滥用（正文中未出现 `、、`、`,,` 类双标点）；
- 无截断、无占位符残留（对比 055 的 "the `..` skill" 占位符、280 的未解析占位符，本 skill 无）；
- 无编号断裂、无杂散 `**`（对比 029/030/058 等 tpl 家族缺陷，本 skill 无）；
- 美式/英式拼写一致；
- 表格格式规范（L100-109 替换表、L224-232 输出物表均对齐）。

---

## 九、人机感与语气审查

### 9.1 语气基调

本 skill 的人机感在语料库中属**上乘**：以"一个有观点、有脾气、有经验的真人作者"的语气写指令（"This is not a cleanup service. You are not just removing 'delve' and calling it a day."，L10），与技能主旨（教 agent 写人话）高度自洽——"教什么就示范什么"。这比 083-085 系列自我膨胀的模板语气和 072 的全大写喊话式语气高出一个层次。

### 9.2 emoji 使用审查

正文 emoji 仅出现在三处，均为**功能性**使用，无装饰性滥用（对比 072 的 20+ 个装饰 emoji）：
- L46：🔴🟡🟢 严重度分级（诊断输出规范）；
- L242：🟢🟡🔴 置信度标记（Communication 节，与输出规范一致）；
- 无其他 emoji。✅ 符合语料库"emoji 须功能性"的惯例。

### 9.3 称呼语与口语化

- 全程对 agent 使用第二人称指令（"You are an expert..."、"Read it."），无对终端用户的花哨称呼（对比 101 的受众混淆）；
- 口语化表达（"the ear goes numb"、"the raised-eyebrow equivalent mid-sentence"）服务于内容示范，不是填充语；
- 无"Let's"引导的闲聊式互动（对比 042 的聊天式框架），指令密度高。

### 9.4 人机边界

- 主动触发场景（L212-220）设计清晰：高密度 AI 指纹 → 建议全重写而非修补；缺 voice 蓝图 → 暂停注入、向用户索要示例（与 SCOPE-03 呼应）；5+ 笼统声明 → 上报用户提供数据而非编造（与 CF-02 呼应）；保留好段落（与 NEG-01 呼应）。这 5 个触发点本身就是"agent 何时该停手问人"的边界定义，人机分工成熟。
- 唯一不足：没有"改写完成后请用户复核品牌声音"的确认点（Mode 3 注入品牌后无人类确认门）。对比 264/273 的强制人类检查点设计，此处可补一个轻量确认步骤。

---

## 十、引用与依赖完整性审查

### 10.1 引用盘点（全量）

| 引用 | 位置 | 类型 | 状态 |
|------|------|------|:----:|
| `marketing-context.md` | L15, L165, L217 | 工作区可选输入 | ✅ 合规（需测评任务提供） |
| `references/voice-techniques.md` | L174 | skill 内部引用 | ❌ 缺失（F-02） |
| `scripts/humanizer_scorer.py` | L232 | skill 内部引用 | ❌ 缺失（F-03） |
| content-production / copywriting / content-strategy / ai-seo | L248-254 | 跨 skill 名称引用 | ✅ 合规（§2.5） |
| `_shared/checker.py`（check.py 侧） | check.py L12 | 评测系统内部依赖 | ✅ 合规（语料库公共库） |

### 10.2 引用完整性结论

两个 skill 内部引用（references/ 与 scripts/）均悬空。语料库中"引用文件缺失"被列为 Top 问题类型之一（约 15 个 skill 受影响，其中 188/195/196 被定为 🟠）。本 skill 的严重度略低，因为：
- body 主体内容完整（对比 032 空壳、045 全委托 references），缺失引用只是深化材料；
- 但 F-03 的特殊之处在于它同时污染了**评分系统**（QA-01 依赖同一文件），使其从"内容瑕疵"升级为"测评系统性失真源"，是本次审查的最高优先级修复项。

---

## 十一、SCORING.yaml 评分点审查

### 11.1 元数据

| 字段 | 值 | 核对结果 |
|------|----|:--------:|
| skill | content-humanizer | ✅ |
| pattern | process | ✅（三模式流程型） |
| total_items | 16 | ✅ 与 criteria 实际条目数一致（3+9+2+1+1=16），无 off-by-one（语料库曾修复 5 处此类错误） |
| 类别分布 | scope 3 / process 9 / output 2 / negative 1 / qa 1 | 与语料库通用分布（process 占 36.5% 最高）一致，process 占 56% 属合理偏高（改写技能的语义工作量集中） |

### 11.2 judge 类型分布

| judge | 数量 | 占比 | 语料库平均 |
|-------|:----:|:----:|:---------:|
| llm | 15 | 93.75% | 63.9% |
| script | 1 | 6.25% | 36.1% |

**F-09（中）：LLM 判定占比严重失衡。** 93.75% 的检查项依赖 LLM 评委，是语料库中最极端的 skill 之一（平均 63.9%）。影响：
- **可复现性**：全部核心判定（scope 3 项 + process 9 项）都靠 LLM 评委的 yes/no，评委模型的不稳定性直接放大为评分噪音——这正是研究设计中"二元 0/1 + 尽量脚本化"要避免的（"纯 LLM 不稳定、不一致"）；
- **可脚本化检查的错配**：至少两类检查本可脚本化却被标为 llm：
  1. **SCOPE-02**（读 marketing-context.md）：evidence 字段写的正是 "Tool call log (Read marketing-context.md)" —— 工具日志是可机械验证的，`tool_log_contains('marketing-context')` 即可判定"是否读了蓝图"，却被标为 llm 并让评委再读一遍日志，浪费 token 且引入主观性；
  2. **PROC-04**（filler 词替换）：可脚本检查 agent 输出中不再出现 delve/leverage/furthermore/moreover 等（`output_not_contains`），与"是否替换为更优表达"的语义部分分层：机械层用脚本、语义层用 LLM；
  3. **PROC-05**（句长变化）：句长方差/长短句交替是可计算的（分割句子 → 统计长度分布），可做脚本冒烟检查；
  4. **PROC-06**（不编造数据）：CF-02 本身由 LLM 判，但可先用脚本检查输出中是否出现"数字 + 无单位上下文"的疑似编造信号做预筛。
- **改进方向**：不必追求 36% 的语料库均值，但把 SCOPE-02 与 QA-01 之外的 1-2 个机械可判项切为 script，可将 LLM 占比降到 ~80%，显著提升跨 harness 对比稳定性。

### 11.3 检查项质量问题

- **question 措辞**：绝大多数为可回答的 yes/no 问句，且带判定锚点（如 PROC-06 的 "no fabricated studies or statistics invented by the agent"、OUT-02 的 "quoting the offending sentence and the replacement"），优于语料库平均的 weasel-word 描述。
- **evidence 字段**：全部 15 个 LLM 项都给了明确的证据位置（"Agent's first response"、"Tool call log"、"Rewritten draft content"），可操作性好。
- **F-10（低）：捆绑问题导致粒度不足**。PROC-05 捆绑了"句长变化 + fragment 强调 + 问-答模式"三个子要求，PROC-09 捆绑了五种注入技法——任一子项未达成，该检查项整体判 0（二元制下无 0.5）。agent 做到 4/5 技法与 1/5 技法得分相同，区分度受损。建议按技法拆分（或改为"至少使用 X 种技法"的计数式 question，让 LLM 判定标准可量化）。
- **覆盖缺口**：
  - Communication 节的"Conclusion first / What+Why+How / Confidence marking（🟢🟡🔴 标记）"仅 OUT-02 部分覆盖（what+why+how），"结论先行"与"置信度标记"无对应检查项；
  - Proactive Triggers 的"tone mismatch after humanizing"（L219）无对应检查项（NEG-01 的"tone matches the brand"部分重叠但未要求 agent 主动 flag 不一致）；
  - 建议补 1-2 项：OUT-03（输出结论先行 + 置信度标记）与 PROC-10（识别并上报品牌 tone 不一致）。

### 11.4 critical_failures 审查

| CF | 描述 | 与正文对应 | 评价 |
|----|------|:---------:|------|
| CF-01 | 输出仍以 AI 模式为主，无实质改造 | ✅ L98 替换规则 / L216 全重写触发 | 合理，与 PROC-04 形成双保险 |
| CF-02 | 编造事实/研究/统计 | ✅ L134-135 诚实不确定范式 | 合理，但与 L130-133 示例张力（F-05） |
| CF-03 | 裸删内容产生破碎文 | ✅ L98 "never just delete" | 合理，防"过度激进"方向 |

三个 CF 覆盖"不改、乱改（编造）、改坏（破碎）"三个失败方向，设计完整。CF 数量 3 个属语料库主流（176 个 skill 为 3 CF）。唯一建议：CF-02 的判定提示中应注明"与 skill 自带示例的可信度区分"（示例数字被 agent 原样引用不算编造，agent 新增未提供数据才算），以减少 F-05 造成的判定歧义。

### 11.5 测评前提条件（Mode A 单次全流程 prompt 依赖）

- **SCOPE-02 前提**：任务 prompt 的工作区**必须提供 marketing-context.md**，否则"读蓝图"无从发生，该检查项在所有 harness 下必然失败。任务设计时应与技能目录一致地放置该文件；
- **QA-01 前提**：任务 prompt 必须**显式索要 humanity score**（"When asked for a humanity score"，L135）——若单次全流程 prompt 未要求该交付物，agent 不会运行脚本，QA-01 在全部 harness 下同分失败，失去区分度。且脚本本身缺失（F-03），此检查项当前**在任何条件下都无法公平通过**；
- 以上两条说明：SCORING.yaml 的可用性不只看文件本身，还依赖任务 prompt 与工作区构造，建议在评测 runner 中把这两个前提做成显式检查（任务模板校验）。

---

## 十二、check.py 检测器审查

### 12.1 实现审查

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from checker import (tool_log_contains, set_tool_log_path, set_agent_output)

def check(workspace: str, tool_log: str, agent_output: str) -> dict[str, bool]:
    set_tool_log_path(tool_log)
    set_agent_output(agent_output)
    result = {}
    # ... 15 个 llm judge 项注释说明（不在此检查）
    result['QA-01'] = tool_log_contains('scripts/humanizer_scorer\\.py')
    return result
```

| 检查项 | 结果 |
|--------|:----:|
| 与 _shared/checker.py 接口契约（set_* 函数） | ✅ 与语料库 322 个 check.py 的通用模式一致 |
| 函数签名 `check(workspace, tool_log, agent_output) -> dict[str, bool]` | ✅ 符合 runner 契约 |
| result key 与 SCORING.yaml 条目对应 | ✅ 唯一 key QA-01 与 SCORING.yaml QA-01 精确匹配，无遗漏、无多余（语料库审计项：result key vs SCORING.yaml 全部匹配） |
| main() 参数契约（3 个 argv）+ agent_output 文件读取 | ✅ 与 runner 调用约定 `python check.py <workspace> <tool_log> <agent_output>` 一致 |
| 输出 JSON 格式 | ✅ `json.dumps(results, indent=2)` |
| 注释说明 15 个 LLM 项不在此检查 | ✅ 明确，避免误读 |

### 12.2 问题

- **F-03 在检测器层的表现**：QA-01 的判定模式 `scripts/humanizer_scorer\.py` 是纯字符串匹配——即使脚本不存在，只要工具日志中出现该字符串（包括 agent 尝试运行但失败的记录，甚至 `ls scripts/` 的输出）即判通过。这说明该检查项是"痕迹检查"而非"行为验证"，配合缺失的脚本，QA-01 的判定结果将完全失真：诚实 agent 失败、碰运气的 agent 通过；
- **弱信号问题**：正则未锚定命令形态（如 `python scripts/humanizer_scorer.py`），任何包含该路径的日志行都会命中。若保留该检查项，建议改为匹配 `(python|python3|uv run|poetry run).*humanizer_scorer` 形态；
- **单一脚本检查项过于单薄**：16 个检查项中只有 1 个脚本项，check.py 实际上退化为"一个正则"。结合 11.2 的 F-09，建议把 SCOPE-02（读蓝图）、PROC-04 机械层（filler 词消失）、PROC-05 机械层（句长方差）纳入 check.py，使脚本检查覆盖 4-5 项；
- 无 workspace 参数使用：当前实现完全不读 workspace 目录（例如无法检查输出文件是否存在），对写作类 skill 可接受（交付物是对话输出而非文件），但若未来输出要求落盘（如 before/after 对比文件），需扩展。

### 12.3 编译与质量

- Python 语法编译通过（文件结构完整、缩进一致）；
- 文件规模 63 行，处于语料库正常区间（1673-4073 字节的经验值之外略小，但功能对应简单场景，可接受）。

---

## 十三、总评、评级与修复建议

### 13.1 五维评估汇总

| 维度 | 评分 | 要点 |
|------|:----:|------|
| 逻辑一致性 | 🟢 4.5/5 | 三模式自洽，正文 ↔ SCORING ↔ CF 对应链完整；扣分：示例与 CF-02 的张力（F-05） |
| 语法与可读性 | 🟡 3.5/5 | 整体优秀；扣分：葡萄牙语泄漏（F-01） |
| 人机感 | 🟢 4.5/5 | 语气与主旨自洽，emoji 功能性使用；扣分：正文 em-dash 偏多（F-08）、无品牌确认点 |
| 规范合规性 | 🟡 3.5/5 | description/name/跨 skill 引用/行数全合规；扣分：缺 Scope 节（F-04）、缺显式 Output 模板 |
| 引用完整性 | 🟠 2/5 | 两个 skill 内部引用悬空（F-02/F-03），其中一个污染评分系统 |
| 评分系统质量 | 🟡 3/5 | 检查项措辞好、CF 设计完整；扣分：LLM 占比 93.75% 失衡（F-09）、QA-01 不可通过（F-03）、捆绑粒度（F-10） |
| 测评可用性 | 🟡 3/5 | 依赖任务 prompt 提供 marketing-context.md 与 humanity score 请求；QA-01 当前无法公平通过 |

### 13.2 总体评级

**🟡 可用但有小问题 — 建议微调。** 评级理由：
- 不评为 🟠 的理由：核心内容（三模式方法论、替换表、指纹清单、示例）质量高且自洽，description 合规，无截断/无模板残迹，评分点与正文逐条锚定——整体处于语料库中游偏上；
- 不评为 🟢 的理由：两处悬空引用（其中 F-03 直接影响评测公平性）、葡语泄漏、缺 Scope 节、LLM 判定占比极端——这些问题不修，"规范化后变量隔离"的测评目标会受影响（agent 面对一个无法运行的脚本指令时，行为无法归因）。

### 13.3 修复建议清单（按优先级）

| 优先级 | 编号 | 问题 | 修复动作 | 涉及文件 |
|:------:|------|------|---------|---------|
| P0 | F-03 | scripts/humanizer_scorer.py 缺失，QA-01 必然失真 | 三选一：① 编写真实可运行脚本（0-100 分 + signal type 明细）；② QA-01 改为 `output_contains` 匹配输出中的分数；③ 删除该能力并从 SKILL.md L232 移除对应行 | SKILL.md + SCORING.yaml + check.py |
| P1 | F-01 | L105 葡萄牙语泄漏 | 删除 `deixe que seja autoevidentemente importante`，补英语替代 | SKILL.md |
| P1 | F-02 | references/voice-techniques.md 缺失 | 补写该文件（每种 voice type 的具体技法，约 100-200 行），或删除 L174 引用 | SKILL.md（+ 新文件） |
| P1 | F-04 | 缺 Scope/Limitations 节 | 补节：不用于需披露 AI 身份的场景（呼应 F-06）、不编造数据边界、输入长度/语言边界 | SKILL.md |
| P2 | F-05 | Mode 2 示例疑似虚构数据 | 示例数字标注"示意"或替换为可验证案例 | SKILL.md |
| P2 | F-09 | LLM 判定占比 93.75% | SCOPE-02 改 script（tool_log_contains('marketing-context')）；PROC-04/05 加机械层检查；check.py 相应扩展 | SCORING.yaml + check.py |
| P3 | F-10 | PROC-05/09 捆绑子项 | 拆分或改为"至少 N 项"计数式 question | SCORING.yaml |
| P3 | F-06 | description 伦理定位 | 加边界声明与拒绝话术 | SKILL.md |
| P3 | F-07/F-08/F-11 | Communication 语境错位 / 自身 em-dash 偏多 / 缺验证步骤 | 删除"owners and deadlines"或改写；正文 em-dash 收敛；补"Mode 4: Verify"或自检清单 | SKILL.md |
| P3 | — | 覆盖缺口 | 补 OUT-03（结论先行+置信度标记）、PROC-10（tone 不一致上报） | SCORING.yaml |

### 13.4 评测前的强制前提

在跑 2 Mode × 5 Harness 评测之前，必须满足：
1. 修复 F-03（否则 QA-01 在所有 harness 下系统性失真，污染跨 harness 对比）；
2. 任务 prompt 工作区提供 `marketing-context.md`（SCOPE-02 前提）；
3. 任务 prompt 显式要求 humanity score 交付物（QA-01 前提）；
4. 无 trigger 对照集（complex-skills-no-trigger/）需同步应用上述修复——主集与对照集除 description 外必须保持一致。

### 13.5 修复后预期

完成 P0+P1 后，本 skill 可评级至 **🟢**：它具备成为语料库"写作类 skill 标杆"的底子——三模式管线在 322 个 skill 中独树一帜（其余写作类多为单流程或模板型），评分点锚定度属上游，正文人机感在写作类中与 240-design-doc、322-cold-start-interview 同档。届时它可作为 process 型内容改写 skill 的合规范本，与 127-policy-redraft、264-startup-pivoting 并列。

---

*（审查结束。全文共 13 节，覆盖 SKILL.md / SCORING.yaml / check.py 全部 3 个文件的逐行审计。问题编号 F-01 ~ F-11 均可在文中定位到具体行号与修复动作。）*
