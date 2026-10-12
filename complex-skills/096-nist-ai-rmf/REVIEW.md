# REVIEW: 096-nist-ai-rmf

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — NIST AI RMF 1.0 四函数 AI 风险评估（GOVERN / MAP / MEASURE / MANAGE）
**Body 行数**: 498 行（SKILL.md，≤600 合规）
**参考文件数**: references/ 7 个（best-practices / critical-infrastructure-note / generative-ai-considerations / next-steps / resources / scoring-guide / version）
**已有 REVIEW**: 无（本文件为 096-nist-ai-rmf 的首份深度审查）
**Dossier 记录**: skill-dossier.md 中 096 未单独审查，仅在 "093 — 100 系列" 综述中随组判定为"🟢 整体为坚实合规内容"；本次审查为逐项验证

---

## 1. 目录全量清单

```
096-nist-ai-rmf/
├── SKILL.md (498 行)
├── SCORING.yaml (191 行)
├── check.py (83 行)
├── REVIEW.md (本文件)
└── references/
    ├── best-practices.md (13 行)
    ├── critical-infrastructure-note.md (5 行)
    ├── generative-ai-considerations.md (12 行)
    ├── next-steps.md (19 行)
    ├── resources.md (15 行)
    ├── scoring-guide.md (22 行)
    └── version.md (8 行)
```

- 无 `scripts/` 目录（本 skill 不需要脚本，全部逻辑内联在 SKILL.md 中）✅
- 无嵌套 skill 目录、无废弃/残留文件 ✅
- SKILL.md 末尾 Reference Files 表（L491-499）列出的 7 个引用文件全部实际存在 ✅

---

## 2. Frontmatter 逐字段审查

### 2.1 name
```
name: nist-ai-rmf
```
- 匹配目录名 `096-nist-ai-rmf` 的 slug 部分：✅
- 全小写+连字符：✅
- ≤64 字符：✅（12 字符）

### 2.2 description（逐句分析）

原文：
```
AI risk assessment using NIST AI RMF 1.0 framework. Evaluate AI systems across 4 core functions (Govern, Map, Measure, Manage) for trustworthy and responsible AI deployment. Use when the user asks to assess risks of an AI system before deployment, establish AI governance structures, evaluate AI trustworthiness, prepare for regulatory compliance (EU AI Act), or review third-party AI tools and vendors.
```

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "AI risk assessment using NIST AI RMF 1.0 framework." | WHAT | ✅ 具体到框架名称与版本 |
| "Evaluate AI systems across 4 core functions (Govern, Map, Measure, Manage) for trustworthy and responsible AI deployment." | WHAT（展开） | ✅ 动词短语开头与 SKILL-SPEC §2.6 的 GOOD 示例同构 |
| "Use when the user asks to assess risks of an AI system before deployment, ... review third-party AI tools and vendors." | WHEN + 触发场景 | ✅ 6 个具体触发场景 |

- **第三人称检查**: 全文无第一/第二人称代词，无 "Use this skill to" 祈使开头。✅
- **触发信号**: 含 "Use when the user asks to"（SKILL-SPEC §2.4 允许的信号之一）。✅
- **KEYWORDS**: AI risk assessment / governance / trustworthiness / EU AI Act / regulatory compliance / third-party AI tools — 覆盖充分。✅
- **字符数**: ~384 字符，≤1024。✅
- **跨技能路由**: 无（"Combine with ISO 42001..." 在 body 而非 description，合规）。✅
- **小瑕疵**: "(Govern, Map, Measure, Manage)" 首字母大写风格与框架官方全大写写法（GOVERN/MAP/MEASURE/MANAGE）不一致，纯外观问题。

### 2.3 其他 frontmatter 字段
仅 `name`、`description` 两个字段，无 allowed-tools 声明（本 skill 不依赖受限工具，可接受）。无任何禁止字段（§1.3 清单逐项比对通过）。✅

### 2.4 Frontmatter 语法
YAML 分隔符配对正确，description 无双引号内嵌引号问题，无截断。✅（对比 corpus 中 047/314 的 description 截断问题，本 skill 无此风险）

**小节结论**: Frontmatter 完全合规，是 corpus 中少数 description 零违规的技能之一。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# NIST AI Risk Management Framework (AI RMF 1.0) (L6-14)
## When to Use This Skill (L17-27)
## Inputs Required (L30-40)
## Trustworthy AI Characteristics (L43-53)
## The 4 Core Functions (L58-231)
  ### GOVERN Function (L62-108) — 6 类别 19 子类别
  ### MAP Function (L111-152) — 5 类别 18 子类别
  ### MEASURE Function (L155-196) — 4 类别 22 子类别
  ### MANAGE Function (L199-231) — 4 类别 13 子类别
## Audit Procedure (L235-319)
  ### Step 1: System Understanding (15 min) (L239-254)
  ### Step 2: GOVERN Assessment (20 min) (L256-271)
  ### Step 3: MAP Assessment (20 min) (L273-285)
  ### Step 4: MEASURE Assessment (25 min) (L287-301)
  ### Step 5: MANAGE Assessment (20 min) (L303-315)
  ### Step 6: Report Generation (20 min) (L317-319)
## Output Format (L324-499)
  ### Executive Summary (L341-367)
  ### GOVERN/MAP/MEASURE/MANAGE Function Assessment (L370-447)
  ### Risk Register (L450-457)
  ### Remediation Roadmap (L460-476)
  ### Compliance Alignment (L478-488)
  ### Reference Files (L491-499)
```

共 5 个 `##` 顶层节 + 大量 `###`/`####` 子节。层级结构完整，无跳级。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

#### Workflow/Process 节
- 存在：✅（`## Audit Procedure`，L235-319）
- 标题明确：✅
- 步骤连贯：✅ Step 1-6 编号连续，顺序为 理解系统 → GOVERN → MAP → MEASURE → MANAGE → 报告，与最佳实践 "Start with GOVERN"（best-practices.md #1）一致
- 每步骤含具体检查项：✅ 41 个 checkbox 检查项分布在 Step 2-5
- 时间预算：15+20+20+25+20+20 = 120 分钟，可执行性强
- 条件分支：⚠️ Step 1.3 "Determine which functions and categories to assess; Prioritize based on lifecycle stage and concerns" 提供了范围裁剪入口，但未定义"何时跳过某子类别"的具体规则（详见 §4 与 §13）

#### Output Format 节
- 存在：✅（`## Output Format`，L324-499）
- 输出模板完整性：✅ 本 skill 的最大优点之一——执行摘要（风险总评 + 严重度计数 + 7 特征 1-5 分表）、四函数逐类评估（Rating/Findings/Gaps/Recommendations）、风险登记表、分阶段整改路线图、法规映射表五件套齐全
- 与 SCORING 的 OUT-01..05 一一对应：✅（详见 §11）
- 可验证性：⚠️ 总评级别（Low/Medium/High/Critical）与函数评级（Not Implemented/Partial/Substantial/Full）之间**无聚合规则**——从哪几个函数评级如何推导出总评未定义（详见 §4.4）

#### Scope/Limitations 节
- 存在：❌ **完全缺失**。全文无 "Scope"、"Limitations"、"What This Skill Does NOT Do" 节。
- 关键影响：SKILL-SPEC §3.1 硬性要求缺失；同时该 skill 面向法规合规领域（EU AI Act 等），缺失"不提供法律意见/不替代正式合规审计"边界声明（详见 §4.5）。

### 3.3 内容委托分析

| 委托内容 | 目标文件 | 委托方式 | 合理性 |
|---------|---------|:--------:|:------:|
| 最佳实践 10 条 | references/best-practices.md | 仅在 Output 模板 Reference Files 表列出 | ⚠️ Audit Procedure 从未指示读取 |
| GenAI 附加评估项 | references/generative-ai-considerations.md | 同上 | ⚠️ 见 §4.6，接线缺口 |
| 评分标尺 | references/scoring-guide.md | 同上 | ⚠️ Rating 标尺实际已内联在输出模板中，参考文件为冗余备份 |
| 基础设施关键性说明 | references/critical-infrastructure-note.md | 同上 | ⚠️ 仅挂名 |
| 后续步骤/资源/版本 | next-steps / resources / version | 同上 | 🟢 辅助性内容，可接受 |

委托比例：SKILL.md 中约 10 行是引用语句（占 498 行的 ~2%）。**核心框架内容（72 子类别全文）完全内联**，agent 仅凭 SKILL.md 即可独立执行完整评估——这是与 001/045 等"导航壳"型 skill 的本质区别。✅

### 3.4 节编号/标题层级
- 标题层级 `#`→`##`→`###`→`####` 无跳级 ✅
- GOVERN 1-6 / MAP 1-5 / MEASURE 1-4 / MANAGE 1-4 编号连续 ✅
- 子类别编号：GOVERN 1.1-1.7、2.1-2.3、3.1-3.2、4.1-4.3、5.1-5.2、6.1-6.2；MAP 1.1-1.6、2.1-2.3、3.1-3.5、4.1-4.2、5.1-5.2；MEASURE 1.1-1.3、2.1-2.13、3.1-3.3、4.1-4.3；MANAGE 1.1-1.4、2.1-2.4、3.1-3.2、4.1-4.3 — 全部连续无跳号 ✅

### 3.5 Body 长度合规
498 行 ≤600 硬上限 ✅。考虑到 72 子类别全文内联，长度控制合理。

---

## 4. 逻辑一致性深度审查

### 4.1 框架内部一致性

| 检查项 | 结果 |
|--------|:----:|
| 7 信任特征（L45-53）↔ 输出模板 Trustworthiness Summary 表 7 行（L356-365） | ✅ 一一对应 |
| 7 信任特征 ↔ MEASURE 2 对应子类别（Valid&Reliable=2.5, Safe=2.6, Secure&Resilient=2.7, Accountable&Transparent=2.8, Explainable=2.9, Privacy=2.10, Fair/Bias=2.11） | ✅ 对应正确 |
| 四函数定义 ↔ Audit Procedure 步骤顺序（GOVERN 先于 MAP） | ✅ 一致 |
| 输入项（ai_system_description 等 7 项）↔ Step 1 分析内容 ↔ 输出模板头部字段 | ✅ 三者对齐 |
| 生命周期阶段（design/development/deployment/monitoring/decommissioning）↔ 输入默认值 ↔ 输出模板 Lifecycle Stage 字段 | ✅ 一致 |
| 整改路线图 Phase 0-30/30-90/90-180/持续 ↔ 执行摘要严重度时限（立即/30 天/90 天） | ✅ 一致 |
| SCORING PROC-10 的双标尺（1-5 分 + 四档评级）↔ scoring-guide.md ↔ 输出模板 | ✅ 三者一致 |

### 4.2 检查清单覆盖缺口（41/72）

Audit Procedure 的固定检查清单共 41 项（GOVERN 12 + MAP 9 + MEASURE 11 + MANAGE 9），覆盖 72 子类别中的 41 个（57%），**未覆盖 31 个子类别且未声明这是抽样**：

| 函数 | 检查清单覆盖 | 遗漏（示例） |
|------|:-----------:|-------------|
| GOVERN (19) | 12 | 1.3、1.4、1.7、2.2、3.2、4.1-4.3、5.2、6.1-6.2 |
| MAP (18) | 9 | 1.2、1.3、1.4、1.6、2.3、3.3、3.4、4.2、5.2 |
| MEASURE (22) | 11 | 1.2、1.3、2.1、2.2、**2.8**、2.12、2.13、3.2、4.1-4.3 |
| MANAGE (13) | 9 | 1.4、2.2、3.2、4.2 |

**问题 1（🟡）**: 检查清单是隐式抽样。尤其 MEASURE 2.8（Accountable & Transparent 特征对应的评估项）被遗漏——输出模板的 7 特征表要求评 "Accountable & Transparent"，但检查清单中没有任何一项指向 MEASURE 2.8，agent 严格按清单执行时会跳过该特征评估，与模板要求形成内部张力。

**问题 2（🟡）**: 检查清单的缩写记号（G、G1.1、M、ME、MA）未在文中解释——"G1" 既代表类别 GOVERN 1（检查项 "G1: Are AI risk policies in place?"），又作为子类别前缀（G1.1、G1.5、G1.6），同一列表内类别级与子类别级混排。Risk Register 模板中用 [G/M/ME/MA] 表示函数，与 MAP=M、MEASURE=ME、MANAGE=MA 的约定一致，但 "M"（MAP）与 "ME"（MEASURE）在快速阅读时极易混淆。

### 4.3 术语问题

**问题 3（🟡）**: TEVV（Test, Evaluation, Verification, and Validation）出现 3 次（MAP 2.3 L128、MEASURE 2.1 L170、MEASURE 2.13 L182）但从未展开首字母缩写。非 NIST 背景的 agent 可能不解其意。

**问题 4（🟢 轻微）**: 流程命名为 "Audit Procedure"，但 NIST AI RMF 官方语境为 "assessment"（审计是更高保证度的独立鉴证活动）。description 与全文均用 "assessment"，流程节标题用 "Audit" 属术语混用，可能给用户带来错误的保证预期。

### 4.4 聚合规则缺失

**问题 5（🟡）**: 三处评分体系之间缺少聚合/映射规则：
- 子类别四档评级（Not Implemented/Partial/Substantial/Full）→ 类别评级：如何聚合未定义；
- 类别评级 → 函数评级：未定义；
- 函数评级 → 总评（Low/Medium/High/Critical）：未定义；
- Risk Register 的 Likelihood/Impact（L/M/H）→ Priority（P0-P3）：无映射表（如 L×H→P0 之类的规则）。
不同 agent 对同一系统可能给出不同总评与优先级，直接影响 LLM judge 对 OUT-01/OUT-03/QA-01 的判定一致性（详见 §13.4）。

### 4.5 输入缺失时的回退路径

**问题 6（🟡）**: `ai_system_description` 标为 [REQUIRED]，但未定义用户未提供时的行为（追问？用假设继续？标注假设？）。Step 1 要求 "Analyze ai_system_description" 但无缺失输入处理指令。同时全文无"信息不足时声明假设"的显式规则——这与 SCORING PROC-08 / QA-01 / NEG-02 的判定强相关（见 §11）。

### 4.6 参考文件接线缺口

**问题 7（🟡）**: Audit Procedure 的 6 个步骤**从不指示读取任何 reference 文件**。GenAI 附加评估（generative-ai-considerations.md）、关键基础设施专项（critical-infrastructure-note.md）、评分标尺（scoring-guide.md）、"非所有子类别适用于每个系统"的裁剪声明（version.md）全部只出现在输出模板末尾的 Reference Files 表（L491-499）。严格按步骤执行的 agent 直到生成报告阶段才"顺带"看到这些文件，且该表位于报告模板内部——格式上是让 agent 把文件清单写进交付报告，而非执行指令。SCORING PROC-09 要求对生成式系统加入 GenAI 考量，但 SKILL.md 没有任何条件分支指示 agent 何时/如何加载该文件。

---

## 5. NIST AI RMF 1.0 事实保真度审查

### 5.1 官方结构核对（NIST AI 100-1，2023-01-26 发布）

| 核对项 | 官方 AI RMF 1.0 | SKILL.md | 判定 |
|--------|----------------|----------|:----:|
| 四函数 | GOVERN/MAP/MEASURE/MANAGE | 一致 | ✅ |
| 类别数量 | GOVERN 6 / MAP 5 / MEASURE 4 / MANAGE 4 | 一致 | ✅ |
| 子类别总数 | 19/18/22/13 = 72 | 一致 | ✅ |
| 发布信息 | "published January 2023 by NIST" | "published January 2023"（L8） | ✅ |
| 框架性质 | voluntary、technology- and sector-agnostic | 一致（L10） | ✅ |
| 7 信任特征 | 与官方列法一致 | 一致（L45-53） | ✅ |

### 5.2 子类别逐项比对结论

72 个子类别中抽样逐项比对官方文本（全部 72 项已核），**唯一实质性偏差**：

**问题 8（🟠）: GOVERN 1.3 / GOVERN 1.4 内容互换**
- SKILL.md L71 GOVERN 1.3: "Processes to determine needed risk management activity levels based on organizational risk tolerance"
- SKILL.md L72 GOVERN 1.4: "Risk management process and outcomes established through transparent policies, procedures, and controls"

官方 AI RMF 1.0 原文：
- GOVERN 1.3: "AI risk management processes and outcomes are established through transparent policies, procedures, and other controls."
- GOVERN 1.4: "Organizational risk tolerance is evaluated and reflected in AI risk management processes and practices."

即 skill 的 1.3 装的是官方 1.4 的内容，1.4 装的是官方 1.3 的内容。语义覆盖尚完整（两个概念都在），但编号错位对按编号引用框架的 agent 是事实性风险——version.md 声称 "NIST AI RMF 1.0 compliant"，此声明因此不完全成立。其余 70 个子类别与官方文本在实质上一致（若干处为压缩性改写，如 GOVERN 1.5 省略了 "with input from relevant AI actors" 后半句，属于可接受的简化）。

### 5.3 时效性声明

| 声明 | 位置 | 判定 |
|------|------|:----:|
| NIST AI 600-1 GenAI Profile, July 2024 | generative-ai-considerations.md L3 | ✅ 正确（2024-07-26 发布） |
| Critical Infrastructure Profile 概念注记 2026-04-07 | critical-infrastructure-note.md L3 | ⚠️ 时点性声明，与 NIST 公开路线图吻合但本环境无法联网核验，建议下一版更新时复核 |
| "AI RMF 1.0 (January 2023)" | SKILL.md L336 | ✅ 正确 |

### 5.4 外部 URL 审计（resources.md）

| URL | 判定 |
|-----|:----:|
| https://www.nist.gov/itl/ai-risk-management-framework | ✅ 规范 |
| https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook | ⚠️ 疑似可访问但非官方 playbook 主路径（官方 playbook 托管于 pages.nist.gov/AIRMF），建议核验 |
| **https://airc.nist.gov/Docs/1** | 🟠 路径模式异常（"Docs/1"），NIST AI 600-1 的规范引用为 doi.org/10.6028/NIST.AI.600-1；本环境 fetch 失败，**强烈建议人工验证或替换为 DOI 链接** |
| https://airc.nist.gov/ | ✅ 规范 |

### 5.5 法规映射的限定性

Compliance Alignment 表（L478-488）将 EU AI Act → GOVERN/MAP/MEASURE、NIST CSF 2.0 → GOVERN/MANAGE、州法 → GOVERN/MAP，属合理的说明性映射。但输出模板要求 agent 给出 "EU AI Act risk level"，而 SKILL.md 无任何"风险分级结论需限定、不构成法律意见"的护栏（详见 §9.4）——在法规敏感领域这是比缺失 Scope 更实质的边界缺口。

---

## 6. 参考文件内容级审查

### 6.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 内容匹配 |
|----------|:------------:|:--------:|:--------:|
| references/best-practices.md | L493 | ✅ | 匹配 |
| references/critical-infrastructure-note.md | L494 | ✅ | 匹配 |
| references/generative-ai-considerations.md | L495 | ✅ | 匹配 |
| references/next-steps.md | L496 | ✅ | 匹配 |
| references/resources.md | L497 | ✅ | 匹配 |
| references/scoring-guide.md | L498 | ✅ | 匹配 |
| references/version.md | L499 | ✅ | 匹配 |

所有引用文件均存在，无死链。✅ 目录中无 SKILL.md 未提及的隐藏文件。✅

### 6.2 逐文件质量

- **best-practices.md (13 行)**: 10 条最佳实践，简洁准确。"Start with GOVERN" 与 Audit Procedure 顺序一致。"Tailor to context"（#6）是 SCORING PROC-04 的唯一支撑文本，但它躺在参考文件里，Audit Procedure 未引用——支撑是间接的。
- **scoring-guide.md (22 行)**: 双标尺定义与输出模板完全一致。功能上冗余（标尺已内联于模板），但作为独立参考无害。
- **generative-ai-considerations.md (12 行)**: 8 项 GenAI 附加评估项（provenance/confabulation/privacy/environment/info-sec/harmful content/third-party/human-AI），与 NIST AI 600-1 对齐。内容质量高，**问题在于从未被 Audit Procedure 的条件分支调用**（§4.6 问题 7）。
- **critical-infrastructure-note.md (5 行)**: 指向 2026-04-07 概念注记（§5.3 已评）。
- **next-steps.md (19 行)**: 通用三阶段行动清单，与 Remediation Roadmap 有重叠但作为独立检查清单可接受。
- **resources.md (15 行)**: 5 个 URL，其中 1 个疑似失效（§5.4）。
- **version.md (8 行)**: 仅 4 行有效内容，但承载了全文最重要的裁剪声明："The NIST AI RMF is voluntary and risk-based. Not all subcategories apply to every system. Tailor the assessment depth..."——该声明应前移到 SKILL.md body（并成为 Scope 节的核心），而非藏在参考文件末尾。

---

## 7. 语法与格式质量（逐问题列举）

### 7.1 拼写错误
未发现拼写错误。✅

### 7.2 语法/大小写问题

| 位置 | 问题 | 严重度 |
|------|------|:------:|
| SKILL.md L495 | "**Generative Ai Considerations**" — "Ai" 大小写不一致（应为 "AI"，与文件名 generative-ai-considerations.md 及文中其他 "AI" 不一致） | 🟢 轻微 |
| SKILL.md L3 description | "Govern, Map, Measure, Manage" — 官方写法为全大写，外观不一致 | 🟢 轻微 |
| SKILL.md L15 | "Combine with 'ISO 42001 AI Governance'..." — 官方标准名称为 "ISO/IEC 42001"，斜杠被省略 | 🟢 轻微（技能名引用属规范允许方式） |

### 7.3 中英/葡英混杂
无（全文英文，无 corpus 中常见的葡语泄露）。✅

### 7.4 Markdown 格式破损
无。表格、复选框、代码块格式全部正确。✅（对比 corpus 中 029/058/297 的编号断裂与乱码问题，本 skill 零破损）

### 7.5 占位符未填充
输出模板中的 `[占位符]` 均为模板设计（方括号占位），非未填充的残留。无 "the `..` skill" 类破损占位符。✅

### 7.6 截断内容
无。498 行完整。✅

---

## 8. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | `nist-ai-rmf` ↔ `096-nist-ai-rmf` |
| 2 | description 第三人称 | ✅ | 零人称违规（corpus 中罕见） |
| 3 | description 含 WHAT+WHEN+KEYWORDS | ✅ | 三要素齐备 |
| 4 | description ≤1024 字符 | ✅ | ~384 字符 |
| 5 | description 含触发信号短语 | ✅ | "Use when the user asks to" |
| 6 | description 无跨技能路由 | ✅ | 路由仅以 prose 形式存在于 body（§3.3 允许） |
| 7 | 无禁止 frontmatter 字段 | ✅ | 仅 name/description |
| 8 | body ≤600 行 | ✅ | 498 行 |
| 9 | Workflow/Process 节存在 | ✅ | `## Audit Procedure` |
| 10 | Output Format 节存在 | ✅ | `## Output Format`（corpus 中最完整的输出模板之一） |
| 11 | **Scope/Limitations 节存在** | ❌ | **完全缺失（硬性要求违反）** |
| 12 | 无跨 skill 文件路径 | ✅ | 无 `../`，无 `@other-skill` 文件引用 |

**违规详情**: 唯一硬性违规是 Scope/Limitations 节缺失（SKILL-SPEC §3.1 三必需节之一）。本 skill 的 Workflow 与 Output 质量均为 corpus 上游水准，Scope 缺失使其整体合规无法拿到满分——且该节缺失还连带放大了 §4.5/§5.5 的边界问题（不适用于什么系统、不提供法律意见、不替代正式合规审计、GenAI 参考文件何时适用）。

---

## 9. 人机感评估

### 9.1 Emoji 审计
SKILL.md 全文无 emoji；检查清单使用 `[ ]` 原生复选框格式。✅（corpus 中 130/183 等技能为反面对照）

### 9.2 全大写/喊叫式语言
无 "MANDATORY"、"STOP" 类叫喊式指令（对比 032/153 的 "⚠️ MANDATORY" 问题）。Rating 选项 "Not Implemented / Partial / Substantial / Full" 为数据非喊叫。✅

### 9.3 Persona 语气分析
整体语气为**专业、中性的合规顾问式**。代表性例句：
- "Use this skill to identify, assess, and manage AI risks; establish governance structures; ensure trustworthy AI characteristics..."（L12）——指令清晰
- "Follow these steps systematically:"（L237）——简洁的祈使引导
- 时间盒设计（"Step 1: System Understanding (15 minutes)"）——务实的执行约束

无自我膨胀式 persona（对比 083-085 "world-class" 模板）、无商业推销（对比 007 K-Dense）。✅

### 9.4 人机边界分析

| 检查项 | 判定 |
|--------|:----:|
| 人类交互点 | ⚠️ 仅存在于交付环节——报告生成后由用户接收；无过程中的人类确认门 |
| 法律/合规边界 | ❌ 无"不构成法律意见/不替代正式审计/风险评估结论需由人类专家复核"声明——作为 EU AI Act 相关 skill，这是实质性缺失 |
| 假设披露 | ❌ 无"信息缺失时声明假设"规则（§4.5 问题 6） |
| 过度自动化倾向 | ⚠️ 输出模板直接要求给出 "EU AI Act risk level" 等强结论，无置信度标注机制（对比 273/301 的置信度机制） |

### 9.5 人称分析
- 第二人称（you/your）：body 中 "Use this skill to" 为对 agent 的祈使指令，属 body 允许的规范用法；无对用户的直接称呼 ✅
- 第一人称（I/we）：无 ✅
- "Remember" 提示仅出现在 version.md 参考文件末尾，无碍 ✅

---

## 10. 可执行性评估

### 10.1 独立可执行性

假设 agent 只拿到 SKILL.md（无目录探索）：
- 72 子类别框架全文内联 → 无需任何参考文件即可展开四函数评估 ✅
- 41 项检查清单 + 每步时间盒 → 执行路径清晰 ✅
- 输出模板五件套 → 交付物结构明确 ✅
- 无外部 CLI、无脚本、无虚构工具依赖（对比 001 的 ccw CLI 与 universal-executor）✅

**可执行性评分: 9/10**——语料库中少有的"纯 body 可执行"型 process skill。

### 10.2 步骤可操作性

| Step | 描述 | 可操作性 | 说明 |
|------|------|:--------:|------|
| 1 | System Understanding | 🟢 | 3 个子步骤明确（review/context/scope） |
| 2 | GOVERN Assessment | 🟢 | 12 项检查清单可直接执行 |
| 3 | MAP Assessment | 🟢 | 9 项检查清单 |
| 4 | MEASURE Assessment | 🟢 | 11 项检查清单 |
| 5 | MANAGE Assessment | 🟢 | 9 项检查清单 |
| 6 | Report Generation | 🟢 | 模板字段完整 |

唯一执行歧义在 Step 1.3 的范围裁剪（§4.1）与清单之外 31 个子类别的处理方式（§4.2）。

### 10.3 工具依赖合理性
无 allowed-tools 声明、无 Bash 命令、无脚本调用——纯文本推理型 skill，任何 harness 环境均可执行。✅

---

## 11. SCORING.yaml 与 check.py 交叉参考（含 dossier 记录比对）

### 11.1 测评点覆盖（21 项 criteria）

| ID | SCORING 要求 | SKILL.md 支撑 | 支撑强度 |
|----|-------------|--------------|:--------:|
| SCOPE-01 | 四函数结构而非通用清单 | 框架节 + 输出模板 | 🟢 强 |
| SCOPE-02 | 先收集系统描述 | Inputs Required + Step 1.1 | 🟢 强 |
| SCOPE-03 | 生命周期裁剪 | 输入项 + Step 1.3 + 模板字段 | 🟢 强 |
| PROC-01 | GOVERN 6 类别 | 框架节 L62-108 | 🟢 强 |
| PROC-02 | MAP 5 类别 | 框架节 L111-152 | 🟢 强 |
| PROC-03 | 风险容忍度与人类监督（MAP 1.5/2.2/3.5） | 框架节明确存在 | 🟢 强 |
| PROC-04 | 深度按风险画像裁剪 | 仅 Step 1.3 一句 + version.md 参考文件 | 🟡 弱接线 |
| PROC-05 | GOVERN 先行 | Step 2 先于 Step 3 + best-practices #1 | 🟢 强 |
| PROC-06 | MEASURE 4 类别 + 7 特征 | 框架节 + 模板 7 特征表 | 🟢 强 |
| PROC-07 | MANAGE 4 类别 | 框架节 L199-231 | 🟢 强 |
| PROC-08 | 不虚构系统细节/控制项 | 无显式禁令，仅模板 "Findings with evidence" 间接暗示 | 🟡 弱 |
| PROC-09 | 生成式系统加 GenAI 考量 | 参考文件存在但未接线到流程 | 🔴 弱（条件触发缺失） |
| PROC-10 | 双标尺评级 | scoring-guide + 模板 | 🟢 强 |
| OUT-01 | 执行摘要 + 总评 + 严重度计数 | 模板 L341-367 | 🟢 强 |
| OUT-02 | 四函数评估带 findings/gaps/recommendations | 模板 L370-447 | 🟢 强 |
| OUT-03 | 风险登记表含 likelihood/impact/priority/mitigation | 模板 L450-457 | 🟢 强 |
| OUT-04 | 分阶段整改路线图 | 模板 L460-476 | 🟢 强 |
| OUT-05 | 法规映射表 | 模板 L478-488 | 🟢 强 |
| NEG-01 | 不得少于 3 函数冒充完整 | 检查清单覆盖全部 4 函数 | 🟢 强 |
| NEG-02 | 不得虚构 | 同 PROC-08 | 🟡 弱 |
| QA-01 | 评级可追溯（证据或假设） | 模板要求证据，但无假设声明规则 | 🟡 弱 |

**小结**: 21 项中 15 项强支撑、5 项弱支撑（PROC-04/08/09、NEG-02、QA-01）、其中 PROC-09 为唯一"结构上不可能满足"风险项——SCORING 要求生成式系统附加评估，但 SKILL.md 流程无触发该行为的机制，agent 能否满足完全取决于其自身主动性。

### 11.2 Critical Failures 分析

| CF | 条件 | 风险度 | 分析 |
|----|------|:------:|------|
| CF-01 | 仅 1-2 函数冒充完整评估 | 低 | 41 项清单覆盖全部 4 函数，结构上难触发 |
| CF-02 | 虚构系统能力/控制/事件 | **中** | 输入薄场景下，输出模板的 "Findings with evidence" 可能诱导 agent 补全貌似合理的控制项（无"信息不足→声明假设"规则兜底） |
| CF-03 | 通用 AI 风险清单无框架映射 | 低 | 框架结构内联程度高，难触发 |

### 11.3 check.py 审查
- 全部 21 项 criteria 均为 llm judge；check.py 实际返回空 dict `{}`，无脚本可验证项——与本 skill 纯文本推理的性质相符，合理 ✅
- 代码瑕疵：`set_tool_log_path` / `set_agent_output` 被导入但无实际消费者（checker 库的调用点不存在于本文件），属模板残留的无效代码，无运行时影响 🟢

### 11.4 Dossier 记录比对
skill-dossier.md 对 096 的判定仅存在于 "093-data-privacy-compliance — 100 系列" 综述（"🟢 整体为坚实合规内容"）。本审查验证结果：**主体判断成立**（框架完整、语法干净、人机感好），但综述粒度无法覆盖本 skill 的两个实质缺陷——Scope 节缺失与 GOVERN 1.3/1.4 内容互换。本文件作为 096 的首份逐项深度审查补上该缺口。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9.5/10 | 10% | 0.95 | description 零违规，仅函数名大小写外观问题 |
| Body 结构完整 | 6/10 | 10% | 0.60 | Workflow/Output 上游水准；Scope 完全缺失 |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 框架自洽；清单抽样未声明、聚合规则缺失、TEVV 未展开 |
| 事实保真度 | 7.5/10 | 15% | 1.13 | 70/72 子类别准确；GOVERN 1.3/1.4 互换；1 个疑似失效 URL |
| 参考完整性 | 8/10 | 10% | 0.80 | 7 文件全存在且质量好；接线缺口（未入流程） |
| 语法格式 | 9.5/10 | 5% | 0.48 | 零拼写/零 markdown 破损；"Ai" 大小写一处 |
| 规范合规 | 7/10 | 15% | 1.05 | 12 项规则 11 过 1 失（Scope 硬性缺失） |
| 人机感 | 8/10 | 5% | 0.40 | 专业中性零 emoji；缺法律边界与假设披露 |
| 可执行性 | 9/10 | 5% | 0.45 | 纯 body 可执行，无外部依赖 |
| SCORING 对齐 | 7/10 | 5% | 0.35 | 15/21 强支撑；5 项弱支撑 1 项结构性缺口 |
| **加权总分** | | | **7.61/10** | |

### 12.2 评级

🟡 **B** (76/100) — 可用但有小问题：内容质量与合规度位于 corpus 上游（process 型 160 个技能中属于前 20%），但 Scope 缺失 + GOVERN 1.3/1.4 互换 + references 接线缺口使其与 017/054/067/077 等 🟢 标杆尚有距离。修复 §13 的 P0/P1 项（预计 ~1 小时工作量）后可达 🟢。

---

## 13. 深度评估：SkillIF 2 Mode × 5 Harness 评测矩阵下的行为预测、失败模式与优化策略

> 本节为深度专项分析，基于 SkillIF 的 2 Mode（规范化 skill 提示 vs 无 trigger 对照集）× 5 Harness 测评矩阵设计，结合 §1-12 的审查证据，预测本 skill 在各评测条件下的行为，给出可操作的优化策略。所有通过率均为基于语料库经验的估算值，用于排序而非精确预测。

### 13.1 技能在评测矩阵中的定位

096-nist-ai-rmf 属于 process 型技能中罕见的"全内联"设计：72 个子类别、41 项检查清单、完整输出模板全部位于 SKILL.md body，references 仅作辅助。这一设计决策决定了其评测画像：

- **优势**: 对提示注入方式不敏感——无论 harness 以何种方式组织任务（直接指令、角色扮演、任务包装、多轮对话、分步拆解），agent 只要读到 SKILL.md 即可获得完整方法论，不依赖任何外部文件或工具链。这在 5 Harness 间会产生最低的方差。
- **劣势**: 方法论的"装载成本"高——72 子类别 + 41 清单 + 5 件套模板约 460 行核心内容，在上下文预算受限的 harness 中，agent 可能只"读到"框架节而压缩清单与模板细节，导致输出偏离。
- **对照集风险**: 本 skill 的核心方法论（NIST AI RMF 四函数）是训练数据中的高频公开知识，无 trigger 模式下 agent 仍可能凭先验知识搭建四函数结构——**trigger 模式的增益主要不来自"框架本身"而来自"框架细节"**（子类别编号、41 项清单、五件套模板）。这一判断直接影响 Mode 间差异的解读：SCOPE-01（四函数结构）在对照组的通过率将意外地高，而 PROC-03（MAP 1.5/2.2/3.5 具体编号）、OUT-04（0-30/30-90/90-180 分阶段）等细节项将显著回落。

### 13.2 Mode 维度行为预测（有 trigger + 完整 skill vs 无 trigger 对照）

| 判据组 | Mode A（规范 skill）预期 | Mode B（无 trigger 对照）预期 | Mode 间差异来源 |
|--------|------------------------|-----------------------------|-----------------|
| SCOPE（3 项） | 0.85-0.95 | 0.5-0.6 | A 方由 "4 core functions" 文案直接锚定；B 方靠先验知识，结构存活但细节退化 |
| PROC-01/02/05/06/07（框架流程） | 0.85-0.95 | 0.5-0.65 | 四函数与 "GOVERN first" 是先验常识；类别清单准确度在 B 方下降 |
| PROC-03（具体子类别编号） | 0.7-0.8 | 0.3-0.4 | 编号细节（MAP 1.5/2.2/3.5）仅 skill 提示可保证 |
| PROC-04（裁剪深度） | 0.5-0.6 | 0.3-0.4 | 双模式同弱——裁剪规则本身在 SKILL.md 中就是弱接线（§4.1/§11.1） |
| PROC-08/NEG-02（不虚构） | 0.6-0.7 | 0.4-0.5 | 无显式禁令，依赖 agent 天性；B 方更依赖先验"风险评估模板"惯性 |
| PROC-09（GenAI 附加） | 0.4-0.5 | 0.2-0.3 | 条件触发缺失，A 方仅靠输出模板文件清单间接命中 |
| PROC-10（双标尺） | 0.9 | 0.5-0.6 | 标尺定义明确内联 |
| OUT-01..05（五件套） | 0.85-0.95 | 0.4-0.6 | 模板完整度是 A 方的最大增益项；B 方报告结构随先验波动 |
| NEG-01（完整性） | 0.95 | 0.7 | 清单结构防止偷工 |
| QA-01（可追溯） | 0.6-0.7 | 0.4 | 无假设声明规则，judge 对"证据"的期待无 skill 侧保障 |

**模式行为结论**: 该 skill 在 Mode A 属"高分稳定型"——五个判据组的通过率方差小（0.4-0.95），无系统性塌方风险；在 Mode B 属"先验依赖型"——框架级判据（SCOPE-01、PROC-01/05）顽强存活，细节级判据（PROC-03、OUT-04）显著退化。若评测报告需要展示"skill 提示的边际价值"，本 skill 是理想样本；若评测关注"无 trigger 时的安全底线"，其 CF-02 风险（虚构控制项）在输入薄场景值得专项监控。

### 13.3 Harness 维度行为预测

按 harness 对输入供给与输出约束的差异，分三档预测：

1. **厚输入 harness（提供完整系统描述 + 组织背景）**: 所有判据通过率取区间上沿。PROC-08/NEG-02/QA-01 在此档最安全——证据可取自输入。PROC-04 受益于"真实风险画像"（如低风险内部工具 vs 高风险医疗系统），agent 更容易自然裁剪而非硬套 41 项清单。
2. **薄输入 harness（仅一句系统名/用途）**: 全区间下沿。风险集中在: (a) PROC-08/QA-01——agent 为填充五件套模板而补造控制项；(b) PROC-02/06 覆盖缩水——41 项清单在上下文紧张时先被压缩的是 MEASURE（22 子类别最长）；(c) SCOPE-02——无输入可收集时 judge 对 "gather before assessing" 的判定变严。
3. **输出受限 harness（限长/限结构）**: 五件套模板与限长冲突。agent 被迫裁剪 Risk Register 或 Remediation Roadmap，直接击穿 OUT-03/OUT-04；而 judge 问题按模板逐项问询，易出现"报告未含 → 判负"的误伤。**建议评测设计时对 process 型技能明确"输出完整度 > 输出精简"的优先级，或将 OUT-03/04 的判据问题改为 '若报告超长可省略，是否仍含核心字段' 的容错表述。**

### 13.4 21 项 LLM-judge 逐项风险矩阵

| 判据 | judge 问题中的歧义/风险点 | 误判方向 | skill 侧缓解手段 |
|------|--------------------------|:--------:|------------------|
| SCOPE-01 | "rather than a generic risk checklist"——薄输入时 judge 可能把"压缩版四函数"误判为通用清单 | 假阴性 | 无（输入侧问题） |
| SCOPE-02 | "before assessing"——agent 可能在报告首段一次性补收集，顺序不可证 | 轻微 | 无 |
| PROC-03 | 三个编号要求精确命中；agent 若用全文覆盖但未显式标注编号 | 假阴性 | 建议在模板 GOVERNS 类标题下保留子类别编号（已内联，风险低） |
| PROC-04 | 主观性最强——"acknowledge when not apply" 的判定依赖 judge 对被评系统的独立判断 | 双向 | 弱接线（§11.1），需在 Step 1.3 补显式裁剪规则 |
| PROC-08 | "no invented details" 需 judge 比对输入与输出的事实差集 | 双向 | **核心缓解点：补"信息缺失→声明假设"规则** |
| PROC-09 | "For generative AI systems" 条件成立与否取决于输入系统类型 | 假阴性/NA | **核心缓解点：流程加条件分支引用 generative-ai-considerations.md** |
| PROC-10 | 双标尺混用（1-5 与四档）——agent 若在函数节误用 1-5 分 | 假阴性 | 模板已分节标注，风险低 |
| OUT-03 | "per-risk priority"——P0-P3 无映射规则（§4.4），judge 无法复现 agent 的优先级推导 | 双向不稳定 | **核心缓解点：补 L/M/H → P0-P3 映射表** |
| QA-01 | "traceable"——证据强度无标尺；judge 对"无证据的 rating"容忍度因人而异 | 双向不稳定 | **核心缓解点：同上假设规则 + 模板加 'Assumptions' 字段** |
| NEG-02 | 同 PROC-08 | 双向 | 同上 |

误判风险最高的三项为 PROC-08/NEG-02、QA-01、OUT-03——恰是 §11.1 标记为弱支撑的项，skill 侧修复与 judge 稳定性呈直接正相关。

### 13.5 失败模式推演（含 CF 触发场景）

**FM-1（中概率，CF-02 近邻）: 薄输入下补造控制项。** 推演路径: harness 仅给 "Assess our recommendation engine" → Step 1 无信息可分析 → agent 直接进入四函数评估 → 为满足模板 "Findings: [with evidence]" 而引用不存在的文档/流程。触发条件: 输入薄 + 无追问习惯 + 无假设规则。**后果**: CF-02 判负或 PROC-08/NEG-02/QA-01 三连扣。**缓解**: P0 修复（§13.7 #2/#5）。

**FM-2（低概率，CF-01 近邻）: 上下文预算挤压致函数缺失。** 触发条件: 长上下文 harness + agent 在 MEASURE 段压缩。41 项清单已把四函数绑定为必检，结构上难以滑向 1-2 函数，但可能滑向"3 函数 + 声明完整"的中间态（NEG-01 判据覆盖此态，属设计良好）。

**FM-3（中概率，判定噪声）: 总评聚合不一致。** 同一输入下不同 agent 得出 Low 与 High 两种总评（§4.4 无聚合规则）→ judge 对 OUT-01 的通过与否随被评样本漂移。这不是"技能失败"而是"评测不可复现"，在 5 Harness 交叉比对时尤其危险——**可能被误读为 harness 质量差异**。

**FM-4（低概率，合规打击）: 法规陈述越界。** agent 输出 "Your system qualifies as high-risk under EU AI Act" 一类绝对化法律结论（§5.5），judge 虽不直接判负（无对应判据），但叠加 Scope 缺失，评测报告中可能作为"合规内容风险"扣人机感/边界分。

**FM-5（低概率，引用错误）: agent 输出模板中的 Reference Files 表复制进用户报告**，暴露 skill 内部路径——无判据直接惩罚，但属交付质量噪音。

### 13.6 边界案例专项

| 边界场景 | 当前行为 | 判据影响 | 建议 |
|----------|---------|:--------:|------|
| 用户请求评估非 AI 系统（如传统规则系统） | 无拒绝/限定路径，agent 强行套用 | SCOPE-01 判定模糊化 | Scope 节补"非 AI 系统不适用" |
| 生成式系统但输入未标注（如仅说 "our chatbot"） | Step 1 无判别分支 | PROC-09 | 流程补"识别系统类型→决定是否加载 GenAI 参考" |
| 用户提及关键基础设施 | 输入项有 deployment_domain 挂钩，但无流程动作 | 无直接判据 | 接线 critical-infrastructure-note.md |
| 用户索要"欧盟合规意见" | 直接产出 risk level 无免责 | 人机感/边界 | 补免责声明 |
| 用户要求只评估 GOVERN | Step 1.3 支持范围裁剪 | PROC-04/NEG-01 | 流程补"显式声明裁剪范围"规则，与 NEG-01 判定对齐 |
| 用户提供矛盾信息（描述说无用户数据，后文又说训练集含 PII） | 无冲突检测指令 | QA-01 | 补"检测并标注输入矛盾" |

### 13.7 优化策略清单（按评分影响排序）

**P0（必做，直接影响判据通过率与 CF 防护）**

1. **新增 `## Scope / Limitations` 节**（SKILL.md 末尾，Reference Files 之前，~15 行）
   内容至少: 不适用于非 AI 系统；不构成法律意见、不替代正式合规审计（EU AI Act 风险分级结论需人类专家复核）；不替代渗透测试/安全评估（OWASP 类专项）；评估深度按风险画像裁剪且裁剪须显式声明；结论基于输入上下文，信息缺失时以假设标注。
   评分影响: 修复 §3.2 硬性违规（合规 7→9+）；降低 FM-4 风险。
2. **Audit Procedure 增加显式"信息缺口处理"步骤**（Step 1 末尾，3-5 行）
   规则: "If ai_system_description is missing or insufficient: ask the user for the missing specifics before assessing; if the user cannot provide them, proceed with explicitly stated assumptions, and mark every assumption in the report." 同步在输出模板执行摘要下加 `**Assumptions**: [...]` 字段。
   评分影响: PROC-08 / NEG-02 / QA-01 三判据的直接支撑（弱→强）；直接压降 FM-1 与 CF-02 触发率。
3. **给 Audit Procedure 接线条件分支: 生成式系统 / 关键基础设施**
   Step 1 系统类型识别后: "If the system is generative (LLM, image/audio/video generation): additionally evaluate the items in references/generative-ai-considerations.md and add a Generative AI Considerations section to the report." 关键基础设施同理（引用 critical-infrastructure-note.md）。
   评分影响: PROC-09 从"结构性缺口"变为可满足；SCOPE-01 判定也更稳。

**P1（应做，事实保真与评测一致性）**

4. **修正 GOVERN 1.3 / GOVERN 1.4 内容互换**（L71-72，两行对调）
   评分影响: 事实保真度 7.5→9；version.md "NIST AI RMF 1.0 compliant" 声明重新成立。耗时 <5 分钟，性价比最高。
5. **补充聚合规则表**（Output Format 节或 Risk Register 前，~10 行）
   - 四档→类别→函数→总评的映射（如: 任一函数 Substantial 以下 → 总评 High+；建议给出可复现的启发式而非追求完美）；
   - Risk Register: L×H→P0、L×M/M×H→P1、其余→P2/P3 的示例映射。
   评分影响: OUT-01/OUT-03 的 judge 可复现性；压降 FM-3 评测噪声。
6. **检查清单声明抽样性**（Step 2 前加一句，1 行）
   "The checklist below is a curated sample of the 72 AI RMF subcategories; assess remaining subcategories where relevant to the system's risk profile (see the framework sections above), and note subcategories you determine not applicable." 同时把 MEASURE 2.8 补入 Step 4 清单（消解 §4.2 内部张力）。
   评分影响: PROC-04 从弱接线变显式授权；NEG-01 判定更清晰。

**P2（可做，打磨）**

7. TEVV 首现展开（MAP 2.3）为 "Test, Evaluation, Verification, and Validation (TEVV)"。
8. 修正 "Generative Ai Considerations" 大小写（L495）；description 与正文函数名统一为全大写 GOVERN/MAP/MEASURE/MANAGE。
9. resources.md 核验并替换疑似失效的 airc.nist.gov/Docs/1 为 DOI 链接（doi.org/10.6028/NIST.AI.600-1）；复核 critical-infrastructure-note.md 的 2026-04-07 概念注记声明。
10. "Audit Procedure" 标题改为 "Assessment Procedure"（与 NIST 术语及 description 的 assessment 表述统一），或保留 Audit 并加一句说明评估与审计的区别。
11. version.md 的裁剪声明（"Not all subcategories apply..."）前移到 SKILL.md body（并入 #1 的 Scope 节），避免关键执行指令藏在参考文件中。

**工作量估计**: P0 三项 ~40 行新增；P1 三项 ~15 行新增/修改；P2 各项各 1-5 行。合计 ~1.5-2 小时人工可完成，无需改动 SCORING.yaml（21 项判据本身设计合理，问题在 skill 侧支撑，不在判据侧）。

### 13.8 修复后的预期评分变化

| 维度 | 当前 | 修复后 | 变化来源 |
|------|:----:|:------:|---------|
| Body 结构完整 | 6/10 | 9/10 | Scope 节补齐 |
| 事实保真度 | 7.5/10 | 9/10 | GOVERN 1.3/1.4 对调 + URL 核验 |
| 规范合规 | 7/10 | 9.5/10 | 三必需节齐备 |
| SCORING 对齐 | 7/10 | 9.5/10 | PROC-04/08/09/QA-01 全部获得显式支撑 |
| 加权总分 | 7.61/10 | ~9.0/10 | 🟡 B → 🟢 A |

评测矩阵预期: 修复后 Mode A 通过率区间整体上移（PROC-09: 0.4-0.5 → 0.75-0.85；PROC-08/QA-01: 0.6-0.7 → 0.85-0.9；OUT-03: 判定噪声消除），且 5 Harness 间方差进一步收窄——该技能有望从"高分稳定型"升级为"高分低方差型"，成为 process 型技能的标杆样本。

### 13.9 结论

096-nist-ai-rmf 是 corpus 中结构质量最高的风险评估类技能之一: 框架内联完整、检查清单可执行、输出模板五件套齐备、description 零违规、零 emoji 零乱码。其短板集中在三处: Scope 节缺失（corpus 共性缺陷，但本技能因法规属性代价更高）、references 接线缺口（GenAI 附加评估无法条件触发）、GOVERN 1.3/1.4 内容互换（唯一事实保真缺陷）。修复路径清晰且成本极低（P0+P1 约 1 小时），完成后可达到与 054/067/077 同级的 🟢 标杆水准。在 2 Mode × 5 Harness 评测矩阵中，本技能应作为"提示增益显著且稳定"的正面样本使用——其 Mode 间差异主要体现为框架细节而非框架结构，评测解读时应以细节级判据（PROC-03/OUT-04 类）而非框架级判据（SCOPE-01 类）作为 trigger 有效性证据。

---

## 变更记录
- 2026-08-06: 096-nist-ai-rmf 首份深度审查。读取全部 9 个文件（SKILL.md 498 行 + SCORING.yaml 191 行 + check.py 83 行 + references/ 7 文件 94 行，合计 ~870 行），并对 72 个子类别逐一比对 NIST AI RMF 1.0 官方文本。评级 🟡 B (76/100)。首次审查，无旧版可对比。

---

## 附录: 审查过程记录
- 读取文件数: 9（SKILL.md + SCORING.yaml + check.py + references/ 7 个）
- 读取总行数: ~870 行
- 参照标准: _shared/SKILL-SPEC.md v1.0（12 项合规清单逐条核对）；skill-dossier.md（093-100 系列综述比对）
- 事实核对: NIST AI 100-1 (AI RMF 1.0, 2023-01-26) 四函数/类别/子类别结构逐项比对；NIST AI 600-1 (GenAI Profile, 2024-07) 发布信息；resources.md 5 个 URL 逐条审计（1 个疑似失效，本环境无法联网确认，标注人工复核）
- 重点深度审查文件: SKILL.md 的 Audit Procedure 与 Output Format 节、SCORING.yaml 21 项判据与 body 的支撑映射
