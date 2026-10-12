# REVIEW — 154-iso-42001-ai-governance

- 审查日期: 2026-08-06
- 审查对象: `D:\SkillIF\skill-experiment\complex-skills\154-iso-42001-ai-governance\`
- 审查方式: 全文读取全部 5 个文件（SKILL.md、SCORING.yaml、check.py、references 下 2 个参考文件），逐项对照 `_shared/SKILL-SPEC.md` v1.0 规范与 `_shared/CHECKER-LIBRARY.md` 检查器库
- 只写 REVIEW.md；未修改 SKILL.md / SCORING.yaml / check.py 任何内容
- 审查顺序依据: 154 → 152 → 151 → 150（本文件为第一个）

---

## 1. 目录清单

```
154-iso-42001-ai-governance/
├── SKILL.md                        (202 行)
├── SCORING.yaml                    (184 行, 20 项判据 + 3 项致命失败)
├── check.py                        (80 行, 6 项脚本检查)
└── references/
    ├── audit-procedure.md          (817 行, 七步审计程序逐控制点检查表)
    └── report-template.md          (279 行, 报告模板 + 合规自查清单)
```

- 文件总数: 5（SKILL.md 1 + SCORING 1 + check.py 1 + references 2）
- 无 `scripts/`、无 `README.md`、无 `assets/`。对 154 这类"知识型审计"技能，references 承载全部细节是规范允许的形态；缺少 README 不影响规范合规（规范未强制要求 README）。
- 所有文件均已全文读取（SKILL.md 202 行、SCORING.yaml 184 行、check.py 80 行、audit-procedure.md 817 行、report-template.md 279 行），合计 1562 行。

---

## 2. Frontmatter（name / description / 工具 / 字段 / YAML）

### 2.1 name

- `name: iso-42001-ai-governance`
- 小写 + 连字符，长度 23 字符 ≤ 64，与目录名 `154-iso-42001-ai-governance` 的后缀完全一致，与 `NNN-kebab-case-name/` 规范匹配。
- ✅ 通过。

### 2.2 description

原文：

```yaml
description: AI governance readiness and gap assessment using ISO/IEC 42001:2023. Evaluate AI management-system practices for risk management, accountability, transparency, security, and continuous improvement. Use when the user asks to assess AI governance readiness or gaps, prepare for ISO/IEC 42001 compliance, audit AI management systems, or respond to AI regulatory requirements (EU AI Act).
```

逐项核验（对照 SKILL-SPEC §2）：

| 检查项 | 结果 |
|--------|------|
| WHAT（做什么） | ✅ "AI governance readiness and gap assessment using ISO/IEC 42001:2023"，具体明确，非泛化描述 |
| WHEN（何时用） | ✅ "Use when the user asks to ..." 列举 4 类触发场景（readiness/gaps、compliance 准备、audit、监管应对） |
| KEYWORDS | ✅ 含 governance、readiness、gap assessment、ISO/IEC 42001、compliance、audit、EU AI Act |
| 人称 | ✅ 纯第三人称，无 imperative / first-person / second-person 开头 |
| 触发信号 | ✅ 含规范要求的 "Use when the user asks to" 信号短语 |
| 长度 | 约 340 字符 ≤ 1024 字符上限 |
| 跨技能路由 | ✅ 无 "NOT for X, use Y instead" 式内嵌路由（与 150 号技能形成对照，详见第 11 节） |
| 结构 | ✅ 完全符合 "`<what>`. Use when the user <triggers>`." 模板 |

- 无缺陷。description 是该语料库中可作范本的写法之一。

### 2.3 工具（allowed-tools 等可选字段）

- Frontmatter 未声明 `allowed-tools`、`argument-hint`、`user-invocable`、`paths` 等可选字段。
- SKILL-SPEC §1.2 将这类字段标为 "Allowed Optional"，即不要求必填。154 的技能流程全部通过 Read（参考文件）+ 文本输出完成，不依赖任何受限工具，省略 allowed-tools 合理。
- ✅ 无合规问题。

### 2.4 字段与 YAML 合法性

- Frontmatter 仅含 `name`、`description` 两个键，均属允许列表，无任何禁止字段（无 version、license、metadata、tags、triggers 等）。
- YAML 语法: 用 `---` 包裹，description 为单行双引号内含逗号无特殊字符，解析无歧义；文件头无 BOM、无尾随错误缩进。
- ✅ 通过。规范 §1.3 的禁止字段列表逐项比对，零命中。

---

## 3. Body（段落 / 必需章节 / 委托 / 层级 / vs600）

### 3.1 段落概况

SKILL.md 正文共 202 行（H1 标题 + 10 个 H2 小节 + 收尾段落），结构：

1. 引言（4 段: 技能定位、标准背景、使用价值、认证边界声明）
2. `## When to Use This Skill`（9 条触发清单）
3. `## Inputs Required`（7 个输入项，标注 REQUIRED / OPTIONAL）
4. `## ISO 42001 Framework Overview`（10 条款 + 4 项原则 + 相关标准）
5. `## Audit Procedure`（7 步表，映射条款 4–10）
6. `## Output Format`（报告 8 个组成部分）
7. `## Best Practices`（10 条）
8. `## Regulatory Alignment`（EU AI Act / GDPR / NIST AI RMF / ISO 42005 / 行业）
9. `## Common Pitfalls`（10 条）
10. `## Version`（1.0）
11. 收尾 "**Remember**" 段落

段落间过渡自然：引言 → 触发 → 输入 → 框架 → 流程 → 输出 → 最佳实践 → 监管对齐 → 常见坑 → 版本。每节有 `---` 分隔线，可读性好。

### 3.2 必需章节（对照 SKILL-SPEC §3.1 三项）

| 必需章节 | 判定 | 定位 |
|----------|------|------|
| Workflow / Process | ✅ 满足 | `## Audit Procedure` 给出 7 步流程、每步条款映射与预计耗时 |
| Output Format | ✅ 满足 | `## Output Format` 列出报告 8 节结构，且委托给模板文件 |
| Scope / Limitations | ⚠️ 有条件满足 | 无独立标题。`Certification boundary` 以**加粗段落**形式内嵌于引言（第 14 行）:"This skill can prepare evidence and identify gaps, but it is not a certification audit. Do not claim ISO/IEC 42001 conformance unless a qualified auditor or certification process verifies it."——内容上完整覆盖了"本技能不做什么 + 何时不应使用"的语义，但形式上缺少 `## Scope` / `## Limitations` 标题。若按"逐字标题匹配"的严格口径，该项算部分达标；按语义口径达标。dossier 记为"三节齐备"，采纳语义口径。详见 13 节 🟡-1。 |

- 另有一处补充边界: 第 142 行 Best Practices 第 10 条 "this skill only supports readiness and evidence preparation"，与认证边界声明呼应，边界意识贯穿全文。

### 3.3 委托（Delegation）

本技能采用"SKILL.md 做导航 + references 做细节"的典型委托模式，且委托书写质量高:

- 第 92–95 行: "The full control-by-control checklists — evaluation questions, scoring rubrics, example risks, and the seven AI lifecycle stages — live in **[`references/audit-procedure.md`](references/audit-procedure.md)**. **Read the section for the step you are on rather than loading the whole file at once.**" —— 不仅委托，还给出读取策略（按步分段读取），防 context 浪费。
- 第 114–116 行: "The copy-ready template and a clause-by-clause self-assessment checklist are in **[`references/report-template.md`](references/report-template.md)**."
- 委托边界清晰: SKILL.md 保留决策层（步骤表、输入要求、边界、监管映射），references 承担执行层（检查表、评分细则、模板占位符）。两者通过 `SKILL.md → "Audit Procedure"` 反向指针闭环。
- ✅ 委托模式为全语料库优等水平。

### 3.4 层级（Heading 结构）

- SKILL.md: 1 个 H1 + 10 个 H2，无 H3。正文内容每节自洽，未出现跳级（无 H1→H3 情况）。
- audit-procedure.md: H1 + `## Contents` + 7 个 H3（每步一节）+ 每步内用 `####`（如 `**5.2 AI Policy**` 实为加粗标题 + 列表，部分 `#### Clause 5`）。层级递增 1 级，合理。
- report-template.md: H1 + H2（Contents / 报告模板 / 自查清单）+ 模板内 H3/H4 仅在 markdown 代码块中出现（属于模板内容而非文档结构，正确做法）。
- ✅ 层级结构整体清晰；唯一小瑕疵是 audit-procedure.md 中 `#### Clause 5: Leadership` 与实际小标题 `**5.1 ...**` 混用两种风格（`####` 与加粗），一致性一般，属 🟢 级微调。

### 3.5 vs600（600 行上限对比）

- SKILL.md 正文 202 行，远低于 600 行硬上限（占 34%）。
- 总内容量 1562 行中 70% 在 references（1096 行），符合"细节下沉 references"的规范导向。
- 按 SKILL-SPEC §3.2 的规模画像，该技能属 Process 型（~200 行目标）与 Tool 型（~300 行）之间，202 行完全落在 Process 型目标区间。
- ✅ 规模合规。

---

## 4. 逻辑（衔接 / 矛盾 / 代码 / 条件）

### 4.1 衔接（SKILL.md ↔ references ↔ SCORING）

- **步骤表 ↔ 参考文件**: SKILL.md 第 97–105 行 7 步表（Step 1–7, Focus, Clause 4–10, Est. 15/20/30/20/40/20/15 分钟）与 audit-procedure.md 的 7 个章节（Step 1–7，耗时 15/20/30/20/40/20/15）**一一对应，名称、条款号、耗时完全一致**。
- **输出结构 ↔ 模板**: SKILL.md Output Format 列 8 节（Executive Summary / Detailed Findings / Risk Assessment Summary / Compliance Roadmap / Documentation Requirements / Recommendations by Stakeholder / Next Steps / Appendices），report-template.md 的模板恰好含这 8 节且顺序一致。
- **SCORING ↔ 文档**: FMT-01 查 "Executive Summary"、FMT-03 查 "Risk Assessment Summary"、PROC-08 查 "Compliance Roadmap"、PROC-05 查 "decommission|lifecycle"——这些字符串全部存在于 report-template.md 模板文本中，判定字符串与技能内容互相印证，无"判据引用技能内不存在概念"的情况。
- ✅ 三段式衔接（正文 ↔ 参考 ↔ 评分）闭环完整，是合规最佳实践。

### 4.2 矛盾与不一致

逐项比对全文后发现以下不一致:

| # | 位置 | 不一致描述 | 级别 |
|---|------|-----------|------|
| C1 | SKILL.md 第 75 行 vs 第 103 行 vs audit-procedure.md 第 386–390 行 | 生命周期阶段数存在 5/7/7 三处口径: (a) 原则节写 "Design → Development → Deployment → Monitoring → Decommissioning"（5 阶段）; (b) 步骤表 Step 5 写 "Design → data → development → validation → deployment → monitoring → decommissioning"（7 阶段，其中第 2 阶段叫 "data"）; (c) 参考文件写 "Design → Development → Validation → Deployment → Monitoring → Maintenance → Decommissioning"（7 阶段，第 2 阶段叫 Data Management、第 6 阶段叫 Maintenance）。(a) 与 (b)(c) 阶段数不一致，(b) 的 "data" 与 (c) 的 "Data Management" 命名不一致。 | 🟡 |
| C2 | SKILL.md 第 86 行 | "reference **ISO/IEC 42005:2025** as a companion standard"——与 Regulatory Alignment 节第 167 行再次提到 ISO/IEC 42005:2025，两处一致（非矛盾）；但与 PROC-07 判据中同时要求 ISO/IEC 23894 略有不对称: 正文仅在 "Related ISO AI Standards" 一句提 "consider ISO/IEC 23894 as supporting guidance"，监管映射节未展开 23894。属轻微的信息分布不均，非矛盾。 | 🟢 |
| C3 | SKILL.md 第 90 行 "Work through seven steps" 与第 99 行起 7 行表格 | 七步说法与表格行数一致 ✅（此条为确认项，无问题） | — |

### 4.3 代码（check.py）

- 入口签名 `check(workspace, tool_log, agent_output) -> dict[str, bool]`，与 runner 约定一致；`main()` 校验参数个数为 4（argv 含脚本名），错误时输出 JSON error 并 exit 1。
- 导入 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))` 引入 `checker` 库——`_shared/checker.py` 已确认存在（含 tool_log_contains / output_contains / set_tool_log_path / set_agent_output），依赖可解析。
- 6 项脚本检查与 SCORING.yaml 中 6 个 `judge: script` 判据完全对齐（SCOPE-03、PROC-05、PROC-08、FMT-01、FMT-02、FMT-03），注释中逐一标注 LLM 判据不在此处检查，注释与实际一一对应，无漂移。
- 小瑕疵: `check()` 内对 `agent_output` 的路径判定逻辑（`os.path.exists` 为 False 时把原始文本 `set_agent_output`）与 `main()` 的文件读取逻辑存在职责重叠——若传入不存在的路径字符串，会误把路径当正文写入。实际 runner 流程中不影响（main 已先读取），但防御性可改进（🟢）。
- 正则: FMT-02 用 `references/audit-procedure\.md|references/report-template\.md`，转义正确；因未加分组，逻辑等价于 `(a)|(b)`，符合意图。✅
- ✅ 代码层面无致命问题。

### 4.4 条件（流程分支）

- 审计流程按 7 步线性执行 + 每步内条件分支（风险级别 → 沟通要求分级: High/Limited/Minimal 三档，见 audit-procedure.md 第 313–327 行; 审计频率分级: 高险季度 / 中险半年 / 低险年度，第 734–737 行）。
- 分支均以表格/清单呈现，符合"决策树优先于散文"的规范导向。
- 输入侧条件: Inputs Required 标注 REQUIRED/OPTIONAL 两级，SCORING 中 ERR-01 与 CF-02 覆盖"缺 REQUIRED 输入时须追问、不得臆测"的条件路径——正文、评分、致命失败三层对同一条件有一致表述。✅

---

## 5. 参考文件（引用矩阵 / 不可见资源 / 全文审查 / 跨 Skill / 死文件）

### 5.1 引用矩阵

| 源文件 | 引用目标 | 形式 | 存在性 | 用途 |
|--------|----------|------|--------|------|
| SKILL.md L92–95 | `references/audit-procedure.md` | 相对路径 markdown 链接 | ✅ 存在 (817 行) | 七步逐控制点检查表、评分细则、风险示例、七阶段生命周期 |
| SKILL.md L114–116 | `references/report-template.md` | 相对路径 markdown 链接 | ✅ 存在 (279 行) | 报告模板 + 条款自查清单 |
| audit-procedure.md L5 | `SKILL.md → "Audit Procedure"` | 反向指针（正文引用） | ✅ | 说明本文件与正文的挂接点 |
| report-template.md L5 | `SKILL.md → "Output Format"` | 反向指针（正文引用） | ✅ | 说明本文件与正文的挂接点 |
| SCORING.yaml FMT-02 | `references/audit-procedure.md`、`references/report-template.md` | 判据文本（tool_log 正则） | ✅ | 强制 agent 实际读取参考文件 |

- 引用全部为技能目录内相对路径，符合 SKILL-SPEC §3.3。

### 5.2 不可见资源（Invisible Resources）

- 无。凡被引用的文件均真实存在；凡存在的文件均被引用或承担 runner 职责（SCORING.yaml / check.py 由评测框架调用，属框架约定文件）。
- 不存在"正文承诺了 X 文件但目录里没有"的悬空引用。

### 5.3 全文审查结论

- **audit-procedure.md（817 行）**: 7 步检查表内容密度高。含逐条 checkbox（Step 2 约 16 条、Step 5 各阶段 5–8 条）、评分字段（Policy Score 0-10 / Resource Assessment 5 维 / Documentation Maturity 5 级）、风险登记模板（markdown 代码块）、示例风险 2 个、沟通分级、KPIs 四类、维护节奏（日/周/月/季/年）、非符合项 5 例、PDCA。覆盖度与 ISO 42001 条款 4–10 对齐，无缺失步骤。
- **report-template.md（279 行）**: 完整报告骨架 8 节 + 附录 4 项；自查清单按 Clause 4–10 七组列示，与 SKILL.md 框架节一一呼应。模板占位符风格统一（`[X]` / `[Name]` / `[List...]`）。
- 两个参考文件均"被正文真实引用且内容与正文承诺一致"，全文审查通过。

### 5.4 跨 Skill 引用

- 无 `../other-skill/` 形式引用；正文也未在散文里提及具体其他技能名（仅泛称 "Combine with security audits, code reviews, or ethical AI assessments"，属组合建议而非路由，符合规范）。
- ✅ 通过。

### 5.5 死文件

- 无。全部 5 个文件均有明确用途（见目录清单）。

---

## 6. 语法格式（拼写 / 语法 / 混杂 / Markdown / 占位符 / 截断）

### 6.1 拼写

- 全文未发现明显拼写错误。唯一候选: audit-procedure.md 第 258 行 `Tools: [State-of-art/Basic/Lacking]` —— "State-of-art" 应为 "State-of-the-art"。属微瑕疵（🟢/🟡 边界，计入修复建议）。
- 其余术语（ISO/IEC 42001:2023、AIMS、PDCA、EU AI Act、NIST AI RMF、ISO/IEC 23894、ISO/IEC 42005:2025）拼写一致，全文统一用 "ISO/IEC 42001:2023"（无一处漏斜杠或漏年份）。

### 6.2 语法

- SKILL.md 与 references 的句子均为完整句，无碎片化表达；列表项风格统一（短语或短句，动宾结构一致）。
- 标点: SKILL.md 第 139、200 行使用 em-dash（"problems—proactive"、"innovation—it's"），其余处用连字符；属风格混用而非错误，英文母语写作者的常见习惯，可接受。

### 6.3 中英混杂

- 全文为纯英文，无中英混排。符合该语料库（评测面为英文 prompt）的一贯做法。

### 6.4 Markdown

- 表格渲染正确（步骤表 4 列、报告表 5 列、自查表 2 列），表头分隔行齐全。
- 代码块: audit-procedure.md 第 168–195 行 ` ```markdown ` 风险登记模板闭合正确；第 388–390 行行内代码块闭合正确；report-template.md 第 16–219 行大代码块闭合正确。
- 链接 `[`...`](references/...)` 语法正确。
- 复选框 `- [ ]` 使用一致。
- ✅ Markdown 质量良好。

### 6.5 占位符

- report-template.md 占位符体系统一: `[X]`（分数）、`[Name]` / `[Date]` / `[List]` / `[Continue...]` / `[Action 1] - Owner: [Name] - Due: [Date]`。文件头已声明 "Copy-ready output structure"，占位符为预期形态。
- audit-procedure.md 中 `Findings: - ✅ Good: [Examples of strong leadership] - ❌ Gaps: [Missing elements]` 等占位式填写格，同样统一。
- ✅ 占位符不会与真实内容混淆（均用方括号包裹）。

### 6.6 截断

- 无。所有文件结尾完整（audit-procedure.md 以 PDCA 循环和 "Apply continuously..." 收束; report-template.md 以 Clause 10 清单收束; SKILL.md 以 "Remember" 段收束），无中途截断痕迹。

---

## 7. 规范合规 12-item（对照 `_shared/SKILL-SPEC.md` §5）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | name: 小写+连字符, ≤64, 匹配目录 | ✅ | `iso-42001-ai-governance`，匹配 `154-iso-42001-ai-governance` |
| 2 | description: 第三人称, WHAT+WHEN+KEYWORDS, ≤1024 | ✅ | 见 §2.2，约 340 字符 |
| 3 | description: 无 imperative/first/second-person 开头 | ✅ | 以 "AI governance readiness..." 客观陈述开头 |
| 4 | description: 无跨技能路由内嵌 | ✅ | 无 "NOT for X" 内容 |
| 5 | description: 至少一个触发信号短语 | ✅ | "Use when the user asks to" |
| 6 | frontmatter: 无允许列表之外的键 | ✅ | 仅 name + description |
| 7 | body: ≤600 行 | ✅ | 202 行 |
| 8 | body: 有 workflow/process 节 | ✅ | `## Audit Procedure` 7 步表 |
| 9 | body: 有 output format 节 | ✅ | `## Output Format` 8 节结构 |
| 10 | body: 有 scope/limitations 节 | ⚠️ | 语义完整（Certification boundary 加粗段 + Best Practices 第 10 条），但无独立标题，详见 §3.2 |
| 11 | body: 无跨技能文件引用 | ✅ | 仅相对路径引用自身 references/ |
| 12 | 目录: NNN-kebab-case, 无空格大写 | ✅ | `154-iso-42001-ai-governance` |

- 12 项中 11 项完全通过，1 项（第 10 项）为语义通过/形式存疑。整体为该语料库合规最优梯队（与 dossier 评价"合规最佳之一"一致）。

---

## 8. 人机感（Emoji / 喊叫 / Persona / 边界 / 人称 / 表格）

### 8.1 Emoji

- SKILL.md 正文: **零 Emoji**。✅
- references: 使用 ✅/❌/⚠️/✓ 均出现在**模板占位语境**（`- ✅ Good: [Examples]`、`✅ / ⚠️ / ❌` 状态列、`### Clause 4: Context ✓`），作为填写符号而非装饰表情，属合理用途。
- ✅ 判定: Emoji 使用克制且用途正确。

### 8.2 喊叫（SHOUTING）

- 全文无全大写喊叫句；大写均为合法缩写（AIMS、ISO、GDPR、KPIs、DPIA、PDCA、UAT、SHAP、LIME、XAI、ROI）。
- ✅ 通过。

### 8.3 Persona

- 正文几乎无人格化语气，以程序化指令与清单为主。
- 唯一 Persona 性收尾: 第 200 行 "**Remember**: ISO 42001 is about building trustworthy AI systems through systematic risk management and governance. It's not a barrier to innovation—it's a framework for responsible innovation that protects both organizations and the people affected by AI." —— 带轻微"说教/激励"色彩。对审计型技能属可接受的最小化 Persona（dossier 未将其列为问题），可保留或删减（🟢）。
- ✅ 整体无过度人格化。

### 8.4 边界

- 边界意识突出且贯穿三层: 正文（Certification boundary）→ 最佳实践（第 10 条 "this skill only supports readiness and evidence preparation"）→ SCORING（NEG-01/02/03 + CF-01 将越界行为 cap_to_0）。
- "不承诺认证"的边界以显式、无歧义的语言书写，且被评分体系强化。
- ✅ 边界处理为全语料库范本级。

### 8.5 人称

- description 第三人称 ✅；正文指令多为无主句/祈使句（面向 agent 的流程指令，符合技能正文惯例）；references 亦为指令/清单体。
- 无向用户喊话的第二人称段落（"You should..." 式表述未出现）。
- ✅ 人称一致。

### 8.6 表格

- SKILL.md 步骤表（Step/Focus/Clause/Est. 四列）为决策型表格，信息密度高。
- report-template.md 符合度表（Clause/Title/Status/Score/Critical Gaps 五列）结构完整。
- audit-procedure.md 中"沟通要求分级"、"审计频率分级"、"维护节奏"均用表格或分档清单呈现。
- ✅ 表格使用符合"决策树/表格优先于散文"导向。

---

## 9. 可执行性

逐环节评估"agent 拿到该技能后能否直接执行":

1. **入口**: description 触发场景明确，When to Use 列出 9 种场景，覆盖"何时该用"的判定。
2. **输入采集**: Inputs Required 明确 REQUIRED（ai_system_description、use_case）与 OPTIONAL（6 项）——agent 第一步该问什么都写死了；ERR-01 + CF-02 确保缺输入时不臆测。
3. **流程执行**: Audit Procedure 7 步表给出每步条款号与预计耗时；每步细节在 audit-procedure.md 中以 checkbox 清单 + 评分字段给出——agent 只需"读对应小节 → 逐条勾选 → 记录证据/差距 → 打 0-10 分"。
4. **输出组装**: Output Format 8 节 + report-template.md 的 copy-ready 模板——agent 按模板填坑即可，且模板内含风险登记格式、路线图三阶段、责任矩阵（Owner/Due）。
5. **质量红线**: 评分细则（0-10）、证据/差距区分（NEG-02 要求不把"写了文档"当"已落地"）、占位符体系——降低幻觉产出风险。
6. **反馈闭环**: 报告要求含行动项、负责人、期限、路线图——结果可直接由组织落地执行。

- 结论: 可执行性极高。SKILL.md 202 行中无一句"空话"，references 提供的是可直接照做的检查表而非背景读物。
- 唯一执行侧提醒: 步骤表建议"Read the section for the step you are on rather than loading the whole file at once"（分段读取），对 817 行参考文件是必要的 context 管理提示——该提示本身已写入正文，执行层面无缺口。

---

## 10. SCORING

### 10.1 结构统计

- total_items: 20
- 分布: scope 3 / process 8 / format 3 / negative 3 / qa 2 / error_handling 1（3+8+3+3+2+1 = 20 ✅ 与 total_items 一致）
- judge 分布: script 6（SCOPE-03, PROC-05, PROC-08, FMT-01, FMT-02, FMT-03）/ llm 14
- critical_failures: 3（CF-01 认证越界、CF-02 缺输入臆测、CF-03 跳过七步流程），全部 cap_to_0

### 10.2 判据与技能内容的一致性

| 判据 | 对应技能内落点 | 一致性 |
|------|----------------|--------|
| SCOPE-01/02 | description + Inputs Required | ✅ |
| SCOPE-03 | 引言 Certification boundary | ✅ |
| PROC-01 | Audit Procedure 7 步表 | ✅ |
| PROC-02 | audit-procedure.md 评分字段（0-10） | ✅ |
| PROC-03/04/05/06 | Framework 原则节 + 生命周期 + 利益相关者 | ✅ |
| PROC-07 | Regulatory Alignment 节 | ✅ |
| PROC-08 | report-template.md Compliance Roadmap 节 | ✅ |
| FMT-01/03 | report-template.md Executive Summary / Risk Assessment Summary | ✅ |
| FMT-02 | 正文 references 链接 + 强制读取 | ✅ |
| NEG-01/02/03 | Common Pitfalls 第 1/3/4 条、audit-procedure 文档成熟度 | ✅ |
| QA-01/02 | 每步评分要求 + Best Practices 第 5/7/8 条 | ✅ |
| ERR-01 / CF-02 | Inputs Required REQUIRED 标注 | ✅ |

- 每条判据都能在技能文本中找到可检验的落点，无"凭空判据"。
- 脚本正则与 check.py 完全一致（逐字符比对: "readiness|gap assessment|not a certification"、 "decommission|lifecycle"、 "Compliance Roadmap"、 "Executive Summary"、 "Risk Assessment Summary"、 转义后的 references 双正则）✅。

### 10.3 已知观察

- 🟢 观察 1: SCOPE-03 的正则 `readiness|gap assessment|not a certification` 是 OR 语义，任一关键词命中即通过——粒度较粗，但配合 llm 判据可接受。
- 🟢 观察 2: 14/20 判据依赖 LLM judge（yes/no question + evidence 字段），question 均写成可作答的是非题，evidence 字段指明检查位置（"Report"、"Agent's first response text"），格式符合 CHECKER-LIBRARY §LLM Judge 约定。
- 🟢 观察 3: 无 category 为 `negative` 的脚本判据（3 个 negative 均为 llm），若未来想硬约束可增加 script 型负面判据。
- ✅ SCORING 质量高，与技能正文、check.py 三方对齐，无悬空项。

---

## 11. 已知问题（dossier 对照）

dossier 记录（2026-08-05 技能质量档案）:

> **154: 🟢 三节齐备合规最佳之一**

本次审查结论与 dossier 一致:

- "三节齐备": Workflow（Audit Procedure）/ Output（Output Format）/ Scope-Limitations（Certification boundary 段）三项语义齐全——第 10 项形式标题问题轻微。
- "合规最佳之一": 12-item 合规 11 项全通过 + 1 项语义通过; 无跨技能引用; description 无路由内嵌; body 202 行远低于 600。
- 补充确认: 本次全文审查未发现 dossier 未记录的新致命问题；发现 3 项低级别问题（生命周期阶段数口径不一致 C1、State-of-art 拼写、无显式 Scope 标题），均不改变 🟢 评级。

---

## 12. 综合评分（8 维加权）

评分口径: 每维 0–10，加权汇总（满分 100）。

| 维度 | 权重 | 得分 | 评述 |
|------|------|------|------|
| 内容完整性 | 20% | 9.5 | 条款 4–10 全覆盖、输入/输出/风险/路线图/文档要求齐备，仅生命周期阶段数口径不一致 |
| 结构层次 | 15% | 9.0 | 正文-参考-模板三层职责清晰，委托策略明确；minor: references 内标题风格混用 |
| 规范合规（12-item） | 15% | 9.5 | 11/12 全过，1 项语义过；无跨技能引用、无路由、无禁止字段 |
| 逻辑一致性 | 10% | 8.5 | 步骤表↔参考文件↔SCORING 三方对齐；扣分点: 5/7 阶段数口径不一（C1） |
| 参考文件质量 | 10% | 9.5 | 817 行 + 279 行，无死文件、无悬空引用、双向指针闭环 |
| 人机感与语言 | 10% | 9.0 | 零装饰 Emoji、边界意识范本级、无喊叫；扣分点: Remember 段轻微 Persona、em-dash 混用 |
| 可执行性 | 10% | 9.5 | 七步流程 + 逐条 checkbox + 评分细则 + copy-ready 模板，可直接落地 |
| SCORING 质量 | 10% | 9.0 | 20 项三方对齐、3 致命失败设计合理；正则粒度粗、负面判据全 llm 为可改进点 |

**加权总分: 92.5 / 100（S 级 / 🟢 合规最佳梯队）**

排名语境: 在已审 4 技能中（154/152/151/150），154 得分最高，符合 dossier "合规最佳之一" 定位。

---

## 13. 修复建议（WRITE EXTENSIVELY）

### 🔴 致命问题

- **无。** 本次全文审查未发现致命问题。
- 说明: 唯一接近"高风险"的项是 C1（生命周期阶段数口径不一致），但它只影响内部一致性，不导致流程断裂或评分误判，按 🟡 处理。

### 🟡 重要问题

#### 🟡-1 无显式 Scope/Limitations 标题（定位: SKILL.md 第 14 行）

- 定位: 引言第 14 行 "**Certification boundary**: ..."，加粗段落形式，未使用 `## Scope` 或 `## Limitations` 标题。
- 修复: 新增 `## Scope & Limitations` 小节（放在 When to Use 之后、Inputs Required 之前），把 Certification boundary 段原样移入，并补 1–2 条边界句（如 "This skill does not perform certification audits, issue ISO 42001 certificates, or provide legal advice"）。Best Practices 第 10 条可保留或精简（移除重复的边界句）。
- 后果（若不修）: 严格脚本化审查工具若按标题匹配检查"三节齐备"，第 10 项合规会判 fail; 且边界声明藏于引言中，快速浏览正文的 agent 可能错过边界信息，增加 CF-01（越界声称认证）触发风险。
- 工作量: 10 行内改动，零风险。

#### 🟡-2 生命周期阶段数口径不一致（定位: SKILL.md 第 75 / 103 行 vs audit-procedure.md 第 386–390 行）

- 定位: 三处出现三套阶段口径（详见 §4.2 C1）: 原则节 5 阶段、步骤表 7 阶段（含 "data"）、参考文件 7 阶段（含 Data Management / Maintenance）。
- 修复: 统一为参考文件的 7 阶段口径 "Design → Data Management → Development → Validation → Deployment → Monitoring → Decommissioning"（与步骤表 Step 5 的 7 项一一对应）; 原则节 Lifecycle Management 改为同一 7 阶段链或加注 "see Step 5"; 步骤表第 103 行的 "data" 改为 "Data Management"。
- 后果（若不修）: 评测 agent 在不同章节读到不同阶段数，输出报告时可能漏掉 Validation/Maintenance 阶段; 若评测员按 PROC-05（decommission|lifecycle）外的隐含阶段数核对，存在评分口径漂移风险; 且这是"内容扎实"标签下的第一处可被挑刺的硬伤。
- 工作量: 3 处文本替换，< 5 分钟。

#### 🟡-3 "State-of-art" 拼写（定位: audit-procedure.md 第 258 行）

- 定位: `Tools: [State-of-art/Basic/Lacking]`。
- 修复: 改为 `State-of-the-art`。
- 后果（若不修）: 低烈度——不影响执行，但作为 "合规最佳之一" 的技能，模板中的拼写瑕疵会被语言级评测抓到; 且该处位于资源评估模板，agent 照抄时会把错误拼写带进用户报告。
- 工作量: 1 字符级改动。

### 🟢 优化建议

| # | 建议 | 定位 | 工作量 | 收益 |
|---|------|------|--------|------|
| 🟢-1 | description 可追加 2–3 个关键词（GDPR、NIST AI RMF、model card），提高意图匹配召回率 | SKILL.md L3 | 1 行 | 触发准确度 |
| 🟢-2 | Remember 收尾段可删减至一句或移除（当前带轻微 Persona 说教味） | SKILL.md L200 | 1 行 | 语感中性化 |
| 🟢-3 | check.py 中 agent_output 的路径/文本双路判断可简化（当前 main 与 check 职责重叠，存在把路径误当文本的边缘情形） | check.py L24–29 | 3 行 | 代码健壮性 |
| 🟢-4 | audit-procedure.md 中 `####` 标题与加粗小标题两种风格统一为一种 | 全文件 | 低 | 层级一致性 |
| 🟢-5 | SCORING 可为 negative 类别增加 1 个 script 判据（如 output_not_contains "we'll add governance later"），增强硬约束 | SCORING.yaml | 2 行 | 评分鲁棒性 |

---

## 附录

### A. 审查方法说明

- 本 REVIEW 依据 `_shared/SKILL-SPEC.md`（SKILL.md 规范 v1.0，12-item 合规清单来源）与 `_shared/CHECKER-LIBRARY.md`（checker 函数库约定）进行。
- 全部 5 个文件逐行通读（1562 行），未抽样。
- 未执行 check.py 实际运行（本审查为静态审查，不修改任何被评文件）。

### B. 文件规模汇总

| 文件 | 行数 | 占比 |
|------|------|------|
| SKILL.md | 202 | 12.9% |
| SCORING.yaml | 184 | 11.8% |
| check.py | 80 | 5.1% |
| references/audit-procedure.md | 817 | 52.3% |
| references/report-template.md | 279 | 17.9% |
| 合计 | 1562 | 100% |

### C. 结论

- 总体评级: 🟢（合规最佳梯队，加权 92.5/100）
- 关键优势: 三层委托结构、边界声明范本级、正文-参考-SCORING-代码四方对齐、零死文件零悬空引用
- 关键改进: 🟡 3 项（Scope 标题、生命周期口径、拼写）+ 🟢 5 项，均为低风险小改动，修复后可达 95+ 水平
