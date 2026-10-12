# REVIEW: 019-discovery-interviews-surveys

**审查日期**: 2026-08-06 | **审查人**: Claude (SkillIF quality auditor)
**审查范围**: 全目录文件逐一全文读取 —— SKILL.md (211 行)、SCORING.yaml (163 行)、check.py (73 行)、原 REVIEW.md 存根 (10 行)、resources/methodology.md (270 行)、resources/template.md (301 行)、resources/evaluators/rubric_discovery_interviews_surveys.json (265 行)
**对照基准**: D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md v1.0、_shared/CHECKER-LIBRARY.md、_shared/checker.py、memory/skill-dossier.md

---

## 1. Directory Full Inventory

| # | 文件 | 行数 | 类型 | 审查状态 |
|---|------|------|------|---------|
| 1 | `SKILL.md` | 211 行 | 主体 | ✅ 全文读取 |
| 2 | `SCORING.yaml` | 163 行 | 评分标准 | ✅ 全文读取 |
| 3 | `check.py` | 73 行 | 评测脚本 | ✅ 全文读取 |
| 4 | `REVIEW.md` | 10 行 | 审查文件（存根） | ✅ 全文读取，本次重写 |
| 5 | `resources/methodology.md` | 270 行 | 引用文件 | ✅ 全文读取 |
| 6 | `resources/template.md` | 301 行 | 引用文件 | ✅ 全文读取 |
| 7 | `resources/evaluators/rubric_discovery_interviews_surveys.json` | 265 行 | 引用文件 | ✅ 全文读取 |

**子目录检查**:

| 子目录 | 是否存在 | 内容 | 备注 |
|--------|:-------:|------|------|
| `resources/` | ✅ | methodology.md、template.md | 引用文件 |
| `resources/evaluators/` | ✅ | rubric JSON（嵌套一层） | 引用文件 |
| `scripts/` | ❌ | — | — |
| `assets/` | ❌ | — | — |
| `docs/` | ❌ | — | — |
| `examples/` | ❌ | — | — |

**要点**: 这是 4 个技能中唯一带引用文件树的技能（3 个资源文件）。引用文件全部存在于磁盘、全部被 SKILL.md 引用（无孤儿文件）。

---

## 2. Frontmatter Field-by-Field Review

### 2.1 原始 Frontmatter

```yaml
---
name: discovery-interviews-surveys
description: Discovery interviews and survey methodology for product validation. Use when validating product assumptions before building, discovering unmet user needs, understanding customer problems and workflows, testing concepts or positioning, researching target markets, identifying jobs-to-be-done and hiring triggers, uncovering pain points and workarounds, or when users mention user research, customer interviews, surveys, discovery interviews, validation studies, or voice of customer.
---
```

### 2.2 `name` 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 小写 + 连字符 | ✅ | `discovery-interviews-surveys` |
| ≤64 字符 | ✅ | 29 字符 |
| 与目录名匹配 | ✅ | `019-discovery-interviews-surveys` |

### 2.3 `description` 字段逐句分析

**句子 1**: "Discovery interviews and survey methodology for product validation."

- WHAT 部分。声明技能提供"发现式访谈与问卷调查方法论"，服务于产品验证。
- 第三人称 ✅。但 WHAT 略抽象——"methodology for product validation" 未直接说明"产出的交付物"（研究计划 + 访谈指南/问卷 + 洞察文档），对比 corpus 优秀 description（如 017 明确双模式产出），WHAT 的产出性稍弱。可接受，非缺陷。

**句子 2**: "Use when validating product assumptions before building, discovering unmet user needs, understanding customer problems and workflows, testing concepts or positioning, researching target markets, identifying jobs-to-be-done and hiring triggers, uncovering pain points and workarounds, or when users mention user research, customer interviews, surveys, discovery interviews, validation studies, or voice of customer."

- WHEN 部分。7 个触发场景（验证假设/发现需求/理解问题与工作流/测试概念/研究市场/JTBD/痛点） + 7 个用户提及关键词（user research/customer interviews/surveys/discovery interviews/validation studies/voice of customer）。
- 触发信号检查（规范 §2.4）：本句以 **"Use when validating..."** 开头——"Use when" + 动名词，**不是**规范五个形式中的 "Use when the user..."（缺 "the user" 主语）。句尾另有 "or when users mention..."——"when users mention" 同样不是五个规范形式之一。
- 与 017 的判定一致：按宽口径（"Use when" 家族）视为含触发短语，dossier 亦判定 "Description 第三人称含触发"；按严格字面，两个信号均为变体。原 REVIEW 存根同样标记了 "缺少 'the user asks to' 触发短语"。
- 人称：无第一/第二人称 ✅（第三人的 "users mention" 完全合规）。
- KEYWORDS：17 个领域词/短语，匹配面极广 ✅——这是本 description 的强项。
- 无跨技能路由 ✅。
- 长度：约 510 字符 ≤1024 ✅。

**description 综合判定**: WHAT 达标、WHEN 场景充分、KEYWORDS 顶级。唯一偏差是触发短语为 "Use when validating..." 变体而非规范 "Use when the user..."。**评级: 🟢（附 1 个规范形式润色项）**

### 2.4 其他字段检查

- `argument-hint`、`allowed-tools` 均未声明（可选 ✅）。
- 规范 §1.3 禁止字段清单逐项核对：**全部未出现** ✅。
- 无 body 末尾 Metadata 节（不强制）。

### 2.5 YAML 语法检查

- 两个标量字段，description 为无引号 plain scalar。检查冒号风险："Use when validating..." 内无 `word: word` 模式（无冒号+空格）；逗号、连字符、破折号在 plain scalar 中安全 ✅。
- 可正常解析 ✅。

---

## 3. Body Section-by-Section Analysis

### 3.1 段落/章节清单

| # | 行号 | 章节 | 类型 | 功能 |
|---|------|------|------|------|
| 1 | 5 | `# Discovery Interviews & Surveys` | H1 | 总标题 |
| 2 | 7-14 | `## Table of Contents` | 导航 | 7 节锚点列表 |
| 3 | 16-27 | `## Purpose` | 背景目的 | 6 项学习目标 |
| 4 | 29-43 | `## When to Use` | 触发条件 | 9 场景 + 8 触发短语 |
| 5 | 45-67 | `## What Is It?` | 概念定义 | 5 组件 + 坏/好问题对比示例 |
| 6 | 69-109 | `## Workflow` | **Workflow 节** | 6 步清单 + 每步详述 |
| 7 | 111-146 | `## Common Patterns` | 模式库 | 5 种研究模式 |
| 8 | 148-174 | `## Guardrails` | 护栏 | 8 项关键要求 + 5 项常见陷阱 |
| 9 | 176-210 | `## Quick Reference` | 速查 | 资源链接/时间估算/升级/输入输出 |

**TOC 完整性**: TOC 列 7 节（Purpose/When to Use/What Is It?/Workflow/Common Patterns/Guardrails/Quick Reference），正文 7 节全部存在且顺序一致 ✅。

### 3.2 必需章节检查（规范 §3.1）

| 必需节 | 对应章节 | 是否满足 | 说明 |
|--------|---------|:--------:|------|
| Workflow / Process | `## Workflow`（Step 1-6 详述） | ✅ | 目标定义→参与者→方法选择→工具设计→执行→分析，6 步闭环，每步有方法选择路由 |
| Output Format | Quick Reference 的 "Outputs produced" + Step 6 分析输出 | ⚠️ 部分满足 | 声明交付物为 `discovery-interviews-surveys.md`（研究计划+访谈指南/问卷+招募标准+分析计划+洞察模板），但**未在 SKILL.md 内定义该文件的章节结构**——结构存在于 resources/template.md 的 Insights Document Template 中。作为导航型技能，输出格式"下沉到引用文件"可接受，但严格按 §3.1 的"output format 节必须回答 '用户得到什么、结果长什么样'"要求，本技能在正文只回答了"文件名"未回答"结构"。判为"部分满足" |
| Scope / Limitations | 无显式节 | ❌ **缺失** | 最接近的是 Quick Reference 的 "When to escalate"（1000+ 参与者/统计建模/纵向研究/民族志→转专家），以及 When to Use 的"何时使用"。但规范 §3.1 要求"此技能不做的事、何时不应使用"，本技能**无任何"何时不该用/不做"的显式声明**（例如：不代替实际访谈执行、不适合替代 AI 生成的问卷盲用等）。dossier 已标记此缺口 |

**发现 3.2-1（🟡，dossier 确认）: 缺显式 Scope/Limitations 节。** "When to escalate" 承担了部分边界功能（4 类研究超出本技能范围），但：① 位于 Quick Reference 内部，无独立章节；② 语义是"升级路径"而非"不做清单"；③ 缺少"本技能不做什么"的否定式边界（如"不执行实际访谈"、"不做市场调研报告撰写"）。建议增加独立 `## Scope & Limitations` 节。

### 3.3 内容委托分析

- 委托结构合理：SKILL.md（211 行）为导航/流程骨架，三个引用文件承载方法细节：
  - `resources/methodology.md`：11 节高级方法论（JTBD 转换访谈、Kano、主题编码、统计分析、偏差缓解、招募、访谈促进、问卷设计、连续发现、混合方法、伦理）。
  - `resources/template.md`：访谈指南模板、问卷模板、JTBD 访谈模板、问题设计原则、筛选问题、分析模板、洞察文档模板。
  - `resources/evaluators/rubric_...json`：10 项评分标准 + 5 类研究指导 + 8 类失败模式。
- 委托比例：SKILL.md 211 行 vs 引用文件 836 行——符合导航型技能（~30 行规格的导航模式在此为 211 行，属"导航+模式库"混合体）✅。
- 关键问题：**SKILL.md 是否充分覆盖核心执行逻辑？** 是——6 步工作流每步在正文有实质内容，引用文件提供深化。无"空壳委托"（对比 045/317/320 的残桩式委托）✅。

### 3.4 节编号 / 标题层级检查

- H1 → H2 两级结构，无 H3，层级一致 ✅。
- Workflow 的 6 步以 "**Step N: ...**" 粗体段落呈现（非标题），与"复制清单跟踪进度"的设计一致 ✅。
- 无编号断裂、无跳级 ✅。

---

## 4. Logical Consistency

### 4.1 步骤衔接分析

| 步骤 | 内容 | 输出 | 下游衔接 |
|------|------|------|---------|
| Step 1 定义目标 | 学习目标/假设/成功标准/决策 | 目标声明 | → Step 3 方法选择依据 |
| Step 2 识别参与者 | 标准/样本量/招募/筛选 | 参与者画像 | → Step 4 筛选问题、Step 5 执行 |
| Step 3 选择方法 | 访谈(5-15)/问卷(50-200+)/JTBD/混合 | 方法决策 | → Step 4 工具类型 |
| Step 4 设计工具 | 访谈指南/问卷 + 偏差规避 | 工具草稿 | → Step 5 执行 |
| Step 5 执行 | 访谈(录音许可)/问卷(先试点) | 数据 | → Step 6 分析 |
| Step 6 分析 | 主题编码/统计 + rubric 自评 ≥3.5 | 洞察文档 | 交付 |

衔接质量：6 步闭环无断链 ✅。每步的输出被下一步消费，Step 6 的 rubric 自评形成质量门。

### 4.2 内部矛盾扫描

**发现 4.2-1（🟡）: 样本量数字在文件内不一致。**

| 来源 | 访谈样本量 | 问卷样本量 |
|------|-----------|-----------|
| SKILL.md Step 3 | 5-15 | **50-200+**（概念测试） |
| SKILL.md Pattern 4 | — | **100-500** |
| SKILL.md Guardrails 第 5 条 | 5-15 | **100+** |
| methodology.md §1/§6 | 5-15（saturation 12-15） | 100+（±5% 需 400+） |
| template.md | 5-15 | — |
| rubric（Quantitative Surveys） | — | **100+ 总，30+/分段** |
| rubric（Problem Discovery） | 8-15 | — |
| SKILL.md Pattern 1 | **8-12** | — |

问题分解：
- 问卷下限："50-200+"（Step 3）vs "100+"（Guardrails/rubric/methodology）——**Step 3 是唯一的 50 起档**，与其余 4 处 100+ 冲突。50 份样本声称"concept testing at scale"与统计显著性下限矛盾（本技能自身反复强调"interviews = themes, surveys = statistics"）。
- 访谈范围："5-15"（Step 3/Guardrails/methodology/template）vs "8-12"（Pattern 1）vs "8-15"（rubric Problem Discovery）——三组数字并存，虽均可辩护（不同模式配不同规模），但无桥接说明。

**修复建议**: Step 3 的 "50-200+" 改为 "100+（探索性概念测试可 50+ 起步，但统计性结论需 100+）"，或将全篇统一为 100+；访谈统一为 5-15（base）+ 模式特化说明。

**发现 4.2-2（🟢 minor）: "When to escalate" 与 Step 3 的方法覆盖边界略重叠。** Step 3 未提及"何时不做调查"，而 escalate 节列出 4 类超出范围的研究——两处边界信息分散，合并入 Scope 节更佳（与 3.2-1 同一修复）。

**发现 4.2-3（🟢 minor）: 伦理要求未在 SKILL.md 正文浮现。** rubric 有 "Ethics & Consent" 标准（10 项标准之一）、methodology.md §11 有完整伦理节（知情同意/隐私/补偿/弱势群体），但 SKILL.md 的 Guardrails 只提 "record with permission"（Step 5 一句）——按 SKILL.md 正文执行的 agent 不会主动覆盖知情同意、匿名化、补偿。建议在 Guardrails 增加一条伦理要求并指向 methodology.md §11。

### 4.3 其余一致性检查

| 检查点 | 位置 | 结果 |
|--------|------|:----:|
| 5 种 Common Patterns ↔ rubric guidance_by_research_type 5 类 | SKILL.md L111-146 vs rubric | ✅ 一一对应（Problem Discovery / JTBD / Concept Testing / Quantitative Surveys / Continuous Discovery） |
| Guardrails 第 2 条（past behavior）↔ rubric Question Quality ↔ methodology 偏差缓解 | 三文件 | ✅ 一致 |
| "Minimum standard: Average score ≥ 3.5" ↔ rubric `minimum_score: 3.5` | SKILL.md L109 vs rubric L94 | ✅ 完全一致 |
| 触发短语 ↔ When to Use ↔ description 关键词 | 三处 | ✅ 一致（描述/正文/触发互证） |
| 输出 `discovery-interviews-surveys.md` ↔ template.md Insights Document Template | SKILL.md L210 vs template.md L256-300 | ⚠️ 文件名唯一出现一次且无模板锚点对应；Insights Template 的标题是 "Research Insights: [Study Name]"，两者命名不同但语义同源，可接受 |
| JTBD 时间窗（3-6 个月） | SKILL.md L122 vs methodology.md L8 vs rubric JTBD L126 | ✅ 三处一致 |
| 招募策略引用锚点 | SKILL.md L89 指向 methodology.md#participant-recruitment | ⚠️ 锚点失效（见 §5.2） |
| 问题设计引用锚点 | SKILL.md L101 指向 methodology.md#question-design-principles | ⚠️ 锚点失效且文件错误（见 §5.2） |

### 4.4 示例正确性

| 示例 | 位置 | 正确性 |
|------|------|:------:|
| 坏/好访谈问题对比（"Would you pay $49/month..." vs 4 步行为导向追问） | SKILL.md L56-67 | ✅ 与 Guardrails 第 1-2 条完全一致，且 4 步追问分别演示 past-behavior/show me/current solution/willingness to change |
| 反例 "Don't you think our UI is confusing?" | Guardrails 1 | ✅ 教科书式诱导问题反例 |
| B2B SaaS 发现访谈示例 | Pattern 1 | ✅ |
| SaaS churn 研究示例 | Pattern 2 | ✅ |
| 落地页验证示例 | Pattern 3 | ✅ |
| 路线图优先排序问卷示例 | Pattern 4 | ✅ |
| 每周客户对话示例 | Pattern 5 | ✅ |
| 混合方法示例（"65% of users find pricing page confusing"） | methodology.md §10 | ✅ 正确演示访谈主题 → 问卷验证的桥接，且**不**声称访谈得出统计结论（与 NEG-03 一致） |
| Kano 双问题模板 | methodology.md §2 | ✅ 功能/反功能双问法正确 |
| NPS 计算（%Promoters(9-10) − %Detractors(0-6)） | template.md L250 | ✅ 标准 NPS 定义正确 |

### 4.5 条件完整性

| 条件分支 | 完整性 |
|----------|:------:|
| 方法选择：深度发现/规模概念测试/JTBD/混合 | ✅ 4 分支全覆盖（Step 3） |
| 5 种研究模式 | ✅ 全覆盖（Common Patterns） |
| 样本量：访谈/问卷/分段 | ⚠️ 数字不一致（4.2-1） |
| 偏差规避：6 类常见偏差 | ✅ 全覆盖（methodology §5） |
| 招募：现有用户/潜在用户两条路径 | ✅ 全覆盖（methodology §6） |
| 分析：访谈 6 步/问卷 6 步 | ✅ 全覆盖（template.md Analysis Templates） |
| 超出范围研究（1000+/统计建模/纵向/民族志） | ✅ escalate 路径（但非 Scope 语义） |

---

## 5. Reference File Content-Level Review

### 5.1 引用完整性矩阵

| 引用（SKILL.md 内） | 目标文件存在？ | 目标锚点存在？ | 备注 |
|---------------------|:-------------:|:-------------:|------|
| `resources/methodology.md` | ✅ | —（无锚点引用） | — |
| `resources/methodology.md#participant-recruitment`（L89） | ✅ | ❌ | methodology.md 实际标题为 `## 6. Participant Recruitment Strategies`，GitHub 风格锚点为 `#6-participant-recruitment-strategies`。**锚点失效** |
| `resources/template.md#interview-guide-template`（L94） | ✅ | ✅ | template.md `## Interview Guide Template` → `#interview-guide-template` ✅ |
| `resources/template.md#survey-template`（L95） | ✅ | ✅ | `## Survey Template` → `#survey-template` ✅ |
| `resources/methodology.md#jobs-to-be-done-interviews`（L96） | ✅ | ❌ | methodology.md 实际标题为 `## 1. Jobs-to-be-Done (JTBD) Switch Interviews` → `#1-jobs-to-be-done-jtbd-switch-interviews`。**锚点失效** |
| `resources/methodology.md#question-design-principles`（L101） | ✅ 文件存在 | ❌ 文件错误 | **"Question Design Principles" 标题在 template.md（L175）而非 methodology.md**。引用指向了错误文件 |
| `resources/evaluators/rubric_discovery_interviews_surveys.json`（L109、L182） | ✅ | — | — |

**锚点统计**: 5 个锚点引用中 2 个有效（interview-guide-template、survey-template）、3 个失效（participant-recruitment、jobs-to-be-done-interviews、question-design-principles）。失效锚点在渲染器（GitHub/VS Code）中表现为"跳转无效但仍显示链接"，agent 阅读时若依赖锚点定位会找不到目标节。**修复工作量小（10 分钟），但影响阅读体验与 agent 定位效率。**

### 5.2 不可见资源

- 无。3 个引用文件全部存在于磁盘，无幽灵引用 ✅。rubric JSON 经 `json.loads` 验证为合法 JSON ✅。

### 5.3 跨 skill 引用检查

- 无跨 skill 文件引用、无 `../` 路径 ✅。引用全部限定在技能目录内（resources/ 下）✅。
- 按名称的兄弟技能引用：无（本技能独立，不依赖任何其他 skill）✅。

### 5.4 嵌套检查

- 唯一嵌套层：`resources/evaluators/`（rubric JSON 位于二级子目录）。SKILL.md 中该文件的两处引用（L109、L182）路径完整（`resources/evaluators/rubric_discovery_interviews_surveys.json`）✅。

### 5.5 scripts / assets / docs / examples 审查

- 无脚本、无资产文件。rubric JSON 是唯一的结构化数据文件。

### 5.6 引用文件全文审查

#### 5.6.1 resources/methodology.md（270 行，11 节）逐节审查

| 节 | 内容 | 质量 | 问题 |
|----|------|:----:|------|
| 1. JTBD Switch Interviews | 招募 3-6 个月转换者、时间线重建、forces of progress（push/pull/anxiety/habit）四力框架、5 个关键问题 | ✅ 方法论准确（经典 JTBD 转换访谈框架） | 无 |
| 2. Kano Analysis | 5 类别（must-have/performance/delight/indifferent/reverse）+ 功能/反功能双问 + 分类矩阵 + 优先级 | ✅ 标准 Kano 正确 | 未提"reverse"与"questionable"组合的分类细节，可接受 |
| 3. Thematic Coding | 熟悉→开放编码→轴心→选择→频次→饱和 6 步 + 4 项严谨技术 | ✅ 标准主题分析流程正确 | 无 |
| 4. Statistical Analysis | 描述/推断统计清单 + 样本量（n≥30、±5% 需 n≈400、有限总体修正）+ 分段 | ✅ 统计规则正确 | "n ≈ 400" 为经验法则，标注了条件（population > 10K）✅ |
| 5. Bias Mitigation | 6 偏差 + 6 策略（含盲分析、预注册假设） | ✅ 全面 | 无 |
| 6. Participant Recruitment | 现有用户/潜在用户两路径 + 筛选 + 超额招募 20-30% + 样本量指导 | ✅ 实用 | 无 |
| 7. Interview Facilitation | 前/中/后三段完整（镜像、3-5 秒静默、why 少用） | ✅ 专业 | 无 |
| 8. Survey Design | 7 问题类型 + 顺序效应 + 量表设计（奇偶点、全标注）+ 试点 5-10 人 | ✅ 标准正确 | 无 |
| 9. Continuous Discovery | 每周 3-5 次对话节奏 + 4 步流程 + 工具 | ✅ | 无 |
| 10. Mixed Methods | 顺序/并发/三角验证 | ✅ | "65%"示例正确（见 4.4） |
| 11. Ethical Considerations | 知情同意/隐私/补偿（$50-150/60min、$10-25/问卷）/弱势群体/IRB | ✅ 全面 | 该节质量高但与 SKILL.md 正文脱节（见 4.2-3） |

**methodology.md 评级**: 内容专业、事实准确、结构清晰。✅ 无错字、无破损。

#### 5.6.2 resources/template.md（301 行）逐节审查

| 节 | 内容 | 质量 | 问题 |
|----|------|:----:|------|
| Workflow 清单 | 5 项模板进度清单 | ✅ | 与 SKILL.md 6 步工作流编号不同（5 vs 6 项）——模板清单合并了 SKILL 的 Step 1-2，轻微不一致但语义兼容 |
| Interview Guide Template | 研究目标/参与者标准/脚本（引言 2min/热身 3min/发现 20-30min/概念测试 10min/收尾 5min） | ✅ 结构专业，时间预算合理 | 无 |
| Survey Template | 筛选器 + 5 节主体（行为/满意度/优先级/概念测试/人口）+ 感谢 | ✅ | 概念测试的价格锚点题 "$X-$Y" 为区间占位符，合理 |
| JTBD Interview Template | 9 阶段时间线重建（首次想法→触发→考虑→焦虑→决定→首次使用→习惯→结果→权衡） | ✅ 与 methodology §1 一致 | 无 |
| Question Design Principles | DO 6 条（✅）/ DON'T 6 条（❌） | ✅ 与 Guardrails 一致 | 无 |
| Screening Questions | B2B SaaS 5 题 / Consumer 4 题 / 排除标准 3 条 | ✅ | 无 |
| Analysis Templates | 访谈主题编码 6 步 + 输出格式（Theme/Frequency/Quotes/Insight/Recommendation）+ 问卷统计 6 步 + 关键指标（CSAT/NPS/2x2 矩阵/样本量） | ✅ | NPS 定义正确（见 4.4） |
| Insights Document Template | 9 节（摘要/目标/方法/发现/惊喜与矛盾/建议/置信度与局限/下一步） | ✅ 结构完整，含 Surprises & Contradictions 节（对应 NEG-04 反证据要求） | 无 |

**template.md 评级**: 内容完整、模板即用。✅ 唯一小瑕疵是模板 Workflow 清单与 SKILL.md 步骤数不一致（5 vs 6）。

#### 5.6.3 resources/evaluators/rubric_discovery_interviews_surveys.json（265 行）审查

| 元素 | 内容 | 质量 |
|------|------|:----:|
| `criteria` | 10 项标准：Objective Clarity / Participant Targeting / Question Quality / Guide Structure / JTBD Focus / Sample Size & Statistical Rigor / Analysis Plan / Facilitation / Ethics & Consent / Insights Documentation | ✅ 覆盖 SKILL.md 全部 Guardrails + Step 6 要求 |
| 评分锚点 | 每项 1/3/5 三档行为锚定（非仅数字） | ✅ 行为锚定设计优秀，利于 LLM 判定 |
| `minimum_score` | 3.5 | ✅ 与 SKILL.md "Average score ≥ 3.5" 一致 |
| `guidance_by_research_type` | 5 类研究（Problem Discovery/JTBD/Concept Testing/Quantitative Surveys/Continuous Discovery），每类含 target_score、focus_criteria、sample_size、key_requirements、common_pitfalls | ✅ 与 Common Patterns 5 模式一一对应；每类 target_score 不同（4.0/4.2/3.8/4.1/3.7），体现按方法差异化 |
| `common_failure_modes` | 8 类失败模式（假设性问题/诱导问题/样本量不足/错误参与者/无系统分析/浅层追问/功能导向/无伦理），每类含 failure/symptom/detection/fix 四字段 | ✅ 自查-修复闭环设计优秀 |

**rubric 评级**: corpus 中设计最完整的自评 rubric 之一。✅ 无 JSON 语法错误。

### 5.7 check.py 与 SCORING 路径一致性核验

**发现 5.7-1（🟡）: PROC-06 的文件路径判定脆弱。** SCORING PROC-06（judge: script）声明 `file_exists("rubric_discovery_interviews_surveys.json")`，check.py L38 实现为 `file_exists(os.path.join(workspace, "rubric_discovery_interviews_surveys.json"))`——**在 workspace 根目录查找**。而 rubric 实际位于技能的 `resources/evaluators/` 子目录：
- 若评测 workspace = 技能目录：glob `rubric_discovery_interviews_surveys.json`（无递归）**不会匹配** `resources/evaluators/...` → PROC-06 结构性失败。
- 若评测 workspace = agent 任务目录：agent 必须已把 rubric 复制到工作区根目录才会匹配——SKILL.md 并未指示 agent 复制 rubric。

两种解释下，PROC-06 都依赖未文档化的前提。**修复建议**: 改为在 skill 目录解析（`${SKILL_DIR}/resources/evaluators/rubric_...json`），或改为 `output_contains` 判定（agent 报告自评分数），或在 SKILL.md 中明确"将 rubric 复制到工作区"。

---

## 6. Grammar & Format Quality

### 6.1 拼写与语法

- SKILL.md 全文扫描：**无拼写错误**。句式完整，无残缺句。
- methodology.md / template.md：**无错字**（对比 corpus 中 262/276 等存在葡语混杂的案例，本技能三文件全英文干净 ✅）。
- 术语一致性：JTBD（jobs-to-be-done）拼写在 description 与正文中一致；"voice of customer" 与 "VOC" 用法一致（SKILL.md 用全称，无缩写混乱）✅。

### 6.2 中英混杂检查

- 无 ✅。

### 6.3 Markdown 破损检查

| 检查项 | 结果 |
|--------|:----:|
| TOC 锚点与标题匹配 | ✅ 7 节全部匹配（#purpose/#when-to-use/#what-is-it/#workflow/#common-patterns/#guardrails/#quick-reference） |
| 围栏代码块 | ✅ 工作流清单、访谈脚本等全部闭合 |
| 粗体/列表 | ✅ 无未闭合标记 |
| 表格 | ✅ 本技能正文无表格；模板文件中的格式正确 |
| 复选框 | ✅ `- [ ]` 正确 |

### 6.4 占位符检查

- 占位符均为模板占位符：`[Specific learning goal]`、`[Hypothesis 1]`、`[Criterion 1]`、`[Option 1]`、`$X/$Y/$Z`、`[Study Name]`——全部有填充语义 ✅。
- 无未定义占位符、无 `..` 残留 ✅。

### 6.5 截断检查

- SKILL.md 211 行完整收尾（Outputs produced 条目）✅。
- methodology.md 270 行完整（IRB 条款收尾）✅。
- template.md 301 行完整（Next Steps 收尾）✅。
- rubric JSON 完整闭合 ✅。

---

## 7. Spec Compliance（对照 SKILL-SPEC.md v1.0 的 12 条规则清单）

| # | 规则 | 检查 | 结果 |
|---|------|------|:----:|
| 1 | name 小写+连字符，≤64 字符，匹配目录 | `discovery-interviews-surveys` / `019-discovery-interviews-surveys` | ✅ |
| 2 | description 第三人称，WHAT+WHEN+KEYWORDS，≤1024 字符 | 约 510 字符，三要素齐备，关键词 17 个 | ✅ |
| 3 | description 无祈使/第一/第二人称开头 | 第三人称开头，无 you/I | ✅ |
| 4 | description 无跨技能路由 | 无 | ✅ |
| 5 | description 至少一个触发信号短语 | "Use when validating..." / "when users mention..."——"Use when" 家族变体，非规范五形式字面 | ⚠️ 通过（宽口径；dossier 同判） |
| 6 | frontmatter 无允许列表外键 | 仅 name/description | ✅ |
| 7 | body ≤600 行 | 211 行 | ✅ |
| 8 | body 有 workflow/process 节 | `## Workflow` 6 步 | ✅ |
| 9 | body 有 output format 节 | "Outputs produced" + Step 6 + 模板引用 | ⚠️ 部分满足（结构定义在引用文件，正文仅声明文件名） |
| 10 | body 有 scope/limitations 节 | **无显式节**；仅 "When to escalate" | ❌ **未通过**（dossier 同判） |
| 11 | body 无跨技能文件引用 | 无 | ✅ |
| 12 | 目录 NNN-kebab-case | `019-discovery-interviews-surveys` | ✅ |

**合规判定**: 10/12 通过，1 项部分通过（output），1 项未通过（scope）。**基本合规，缺 Scope 节是主要缺口** —— 与 dossier 🟡 判定一致。

---

## 8. Human-Like Feeling

### 8.1 Emoji 审计

| 位置 | Emoji | 判定 |
|------|-------|:----:|
| SKILL.md Guardrails 常见陷阱 | ❌ × 4（列表项前缀） | ⚠️ 功能性偏装饰——作为"陷阱"的否定标记，语义功能明确（对比其他 corpus 技能用文字 "-"），属轻度装饰但可接受 |
| template.md Question Design Principles | ✅ × 6 / ❌ × 6 | ✅ 功能性（DO/DON'T 双向对照的视觉锚点） |
| template.md 筛选排除 | ❌ 无（用文字"Disqualifiers"标题） | — |
| methodology.md / rubric | 无 | ✅ |

### 8.2 全大写审计

- SKILL.md：无全大写喊叫（"**Critical requirements:**" 为粗体强调）✅。
- template.md：`DO:` / `DON'T:` 为功能性标签 ✅。
- 无滥用 ✅。

### 8.3 Persona 语气分析

- 角色：产品研究方法论顾问，语气专业、实用、经验导向。
- 亮点：Guardrails 的 "What people did reveals truth; what they say they'd do is often wrong" —— 经验性洞察而非机械规则 ✅。
- 语气无 marketing 腔、无 pep-talk（对比 038/083-085 的营销 persona）✅。
- 面向 agent 的指令明确（"Copy this checklist and track your progress" 是 checklist 的交付形式设计，可接受）。

### 8.4 人机边界

- 本技能方法论属性强，人机边界体现在：① Step 5 "record with permission" 明确人类访谈者的伦理义务；② rubric 自评把质量判断交给 agent 但设定客观门槛（≥3.5）；③ "When to escalate" 明确 4 类研究应交给专业研究者。
- 无 017/018 式的高后果门控（本技能非法律类，无需）——边界与技能性质匹配 ✅。

### 8.5 人称统计（定性）

- "you"：约 15 处，集中在**模板内容**（访谈脚本 "Tell me about your role"、"What's the most frustrating part of [workflow]?"）——这些是交付物（访谈指南）中的人类访谈者话术，属于**数据**而非对用户的指令，用法正确 ✅。
- agent 指令为第三人称祈使 ✅。
- 无双重受众混淆（对比 101 的"面向用户 vs 面向 agent"混杂）✅。

**人机感评级**: 9.0/10 —— 专业、可读、无噪音；仅 4 个 ❌ 装饰性前缀为可选项。

---

## 9. Executability

### 9.1 独立可执行性评分

| 维度 | 评分 (0-10) | 说明 |
|------|:----------:|------|
| 步骤可操作性 | 9.0 | 6 步工作流每步有具体指令与路由；Step 3 方法选择表直接可用 |
| 决策门完备性 | 7.5 | 仅 Step 6 rubric ≥3.5 一个质量门；无前置确认门（方法论类技能可接受） |
| 环境独立性 | 9.5 | **完全自包含**——不依赖任何外部插件/档案（对比 017/018 的 6.0） |
| 工具依赖合理性 | 9.0 | 仅 Read/Write/Glob 等标准工具；无脚本依赖 |
| 评测可复现性 | 8.5 | 除 PROC-06 路径问题外（见 5.7-1），评测可直接进行 |

**独立可执行性总评**: 4 个技能中环境独立性最强。agent 只需 SKILL.md + 3 个引用文件即可完整执行"设计访谈/问卷研究计划"流程。

### 9.2 步骤可操作性表

| 步骤 | 可操作？ | 需要的用户输入 | 依赖 | 完成判据 |
|------|:-------:|---------------|------|---------|
| Step 1 定义目标 | ✅ | 产品假设/目标 | 无 | 目标+假设+成功标准+决策声明 |
| Step 2 识别参与者 | ✅ | 目标人群 | methodology.md §6 | 标准+样本量+招募+筛选 |
| Step 3 选择方法 | ✅ | 约束（时间/预算） | 内容地图路由 | 方法决策+理由 |
| Step 4 设计工具 | ✅ | 无 | template.md | 访谈指南/问卷草稿 |
| Step 5 执行计划 | ✅ | 无 | 无 | 录音许可/试点计划 |
| Step 6 分析 | ✅ | 无 | rubric JSON | 洞察文档 + 自评 ≥3.5 |

### 9.3 工具依赖合理性

- 无 Bash/脚本依赖；rubric 自评可由 agent 直接对照 JSON 判定 ✅。
- 唯一工具性注意点：锚点链接失效不影响执行（agent 读全文而非跳转），影响定位效率（见 §5.1）。

---

## 10. SCORING.yaml Cross-Reference

### 10.1 结构总览

- `pattern: process`、`total_items: 18`。实际条目：3 scope + 7 process（含 PROC-03b）+ 2 output + 4 negative + 2 QA = 18 ✅ 计数一致。
- judge 类型：script 2 项、llm 16 项。check.py 注释 "Run all 2 script checks" ✅ 与实现一致。

**观察**: 16/18 为 LLM 判定——本技能评测高度依赖 LLM judge 质量。这是方法论类技能的结构特征（内容质量难以机械判定），但相比 017/018（script:llm ≈ 8:12 / 10:10），本技能更极端。

### 10.2 逐项映射矩阵

| ID | 类别 | judge | 检查方式 | 对应 SKILL.md 内容 | 可判定性 |
|----|------|:-----:|----------|--------------------|:--------:|
| SCOPE-01 | scope | llm | 首响应框定发现研究 | Purpose/When to Use | ✅ |
| SCOPE-02 | scope | llm | 目标/假设/成功标准/决策 | Step 1 | ✅ |
| SCOPE-03 | scope | llm | 方法匹配目标（5-15 访谈 / 50-200+ 问卷） | Step 3 | ⚠️ 问题文本沿用 "50-200+"（与正文一致但见 4.2-1 的数字冲突） |
| PROC-01 | process | llm | 参与者 4 要素 | Step 2 | ✅ |
| PROC-02 | process | llm | 偏差规避设计 | Step 4/Guardrails 1-3 | ✅ |
| PROC-03 | process | llm | 录音许可/试点 | Step 5 | ✅ |
| PROC-03b | process | llm | 访谈技巧 | methodology.md §7 | ✅ 两个 PROC-03 变体并存（03 与 03b）——ID 命名合法但略违反递增惯例，可接受 |
| PROC-04 | process | llm | 系统化分析 | Step 6 | ✅ |
| PROC-05 | process | llm | 证据化洞察（不摘樱桃） | Step 6/Guardrails 8 | ✅ |
| PROC-06 | process | script | rubric 文件存在 | Step 6 自评 | ⚠️ 路径脆弱（5.7-1） |
| OUT-01 | output | script | output 含 Research Plan/Interview Guide/recruitment/analysis plan | Outputs produced | ✅ |
| OUT-02 | output | llm | 洞察模板含主题+证据 | template.md Insights Template | ✅ |
| NEG-01 | negative | llm | 无诱导问题 | Guardrails 1 | ✅ |
| NEG-02 | negative | llm | 无假设性问题 | Guardrails 2 | ✅ |
| NEG-03 | negative | llm | 不从访谈样本做统计声明 | Guardrails 陷阱 2/methodology §10 | ✅ |
| NEG-04 | negative | llm | 不摘樱桃引语 | Guardrails 8 | ✅ |
| QA-01 | qa | llm | 样本量匹配方法 | Guardrails 5 | ⚠️ 判定依赖的样本量数字自身不一致（4.2-1），LLM judge 可能无所适从 |
| QA-02 | qa | llm | 反证积极寻找 | Guardrails 6 | ✅ |

### 10.3 Critical Failures 分析

| ID | 描述 | effect | 与 SKILL.md 一致性 |
|----|------|:------:|--------------------|
| CF-01 | 诱导/假设性问题工具 | cap_to_0 | ✅ 对应 Guardrails 1-2（技能的最核心纪律） |
| CF-02 | 从访谈样本做统计显著性声明 | cap_to_0 | ✅ 对应 Guardrails 陷阱 2 + NEG-03 |

CF 设计质量：两个 CF 对准方法论类技能的两条职业道德红线（问题质量与统计诚实），语义明确 ✅。但注意 CF-01 的触发面较宽——LLM judge 需区分"轻微诱导"与"系统性诱导"，判定边界描述（"telegraph the expected answer"）可接受。

### 10.4 SCORING 质量评价

- 覆盖面与 Guardrails/工作流严格对应，无悬空条目 ✅。
- 问题：① PROC-06 路径脆弱（5.7-1）；② 16/18 LLM 判定带来的可复现性风险；③ SCOPE-03/QA-01 的问题文本嵌入了有争议的样本量数字（"50-200+"/"100+"），若正文统一数字需同步 SCORING。
- 亮点：QA-02（反证寻找）是本技能方法论灵魂（confirmation bias 防护）的正确测评化。

---

## 11. Known Issues from skill-dossier.md

Dossier 原文（019-discovery-interviews-surveys 条目）：

> **逻辑**: 6 步工作流、5 种模式、护栏和 rubric 自评一致实用。
> **语法**: 干净，结构良好；无错字。
> **人机感**: Helpful 顾问语气；清单格式引人入胜而无填充或 emoji。
> **合规**: Description 第三人称含触发，body 211 行，workflow 和 outputs 节存在，但 scope 仅部分覆盖——"When to escalate" 暗示限制但无显式 Scope 节。
> **总评**: 🟡 补显式 Scope 节。

**本次审查与 dossier 对照结论**:

| Dossier 声明 | 本次验证 | 结论 |
|--------------|---------|:----:|
| 6 步工作流/5 模式/护栏/rubric 一致 | ✅ 验证一致（含 rubric 10 项标准与 5 类指导的对应） | 确认 |
| 无错字 | ✅ 三文件扫描无错字 | 确认 |
| 无填充或 emoji | ⚠️ SKILL.md 有 4 个 ❌ 装饰前缀（Guardrails 陷阱列表）——dossier 判"无 emoji"不精确，但 ❌ 属功能性前缀，不影响结论 | 微调 |
| 缺显式 Scope 节 | ✅ **确认缺失** | 确认 |
| 🟡 评级 | ✅ 与本次 B+（8.23/10）一致 | 确认 |

**新发现（dossier 未覆盖）**:
1. 3 个失效锚点链接（5.1）。
2. 样本量数字多文件不一致（4.2-1）。
3. 伦理要求未在 SKILL.md 正文浮现（4.2-3）。
4. PROC-06 判定路径脆弱（5.7-1）。
5. Output 节仅为"部分满足"（3.2）。

---

## 12. Comprehensive Scoring

### 12.1 八维度加权评分表

| 维度 | 权重 | 得分 | 加权 | 主要依据 |
|------|:----:|:----:|:----:|---------|
| 逻辑一致性 | 15% | 8.0 | 1.200 | 6 步闭环无断链；样本量数字多文件冲突为实质问题 |
| 语法与格式 | 10% | 9.0 | 0.900 | 三文件零错字、零破损 |
| 人机感 | 10% | 9.0 | 0.900 | 顾问语气、无喊叫、模板人称用法正确；4 个 ❌ 装饰前缀 |
| 规范合规 | 20% | 7.5 | 1.500 | 10/12 通过；缺 Scope 节（❌），Output 部分满足 |
| 可执行性 | 15% | 8.5 | 1.275 | 自包含、无环境依赖、步骤可操作性强 |
| 引用完整性 | 10% | 8.0 | 0.800 | 3 文件全存在全引用（无孤儿）；但 5 锚点中 3 个失效 |
| SCORING 质量 | 10% | 8.0 | 0.800 | 覆盖严丝合缝；PROC-06 路径脆弱、16/18 LLM 判定、数字冲突传染 |
| 内容深度 | 10% | 8.5 | 0.850 | 方法论覆盖面广且准确；11 节高级方法与 10 项 rubric 是实质深度 |
| **合计** | 100% | — | **8.23** | — |

### 12.2 评级

**评级: B+（8.23/10）—— 内容扎实、可立即使用的方法论技能，需补 Scope 节与一致性修整。**

与 stub REVIEW 的 B−（50/100）对比：stub 的核心发现（触发短语变体、缺 Scope 节）本次均验证成立；但 stub 未发现锚点失效与数字冲突问题，且 50/100 未反映本技能引用体系（836 行高质量资源文件）的实质价值。本次加权为 8.23（B+）。

---

## 13. Fix Recommendations

### 13.1 🔴 致命问题

**无。**

### 13.2 🟡 重要问题

| # | 问题 | 位置 | 修复建议 | 工作量 |
|---|------|------|---------|:------:|
| 1 | 缺显式 Scope/Limitations 节 | SKILL.md Quick Reference 之前 | 新增 `## Scope & Limitations`：本技能不做（不实际执行访谈/不代替统计建模/不撰写完整市场报告等）+ 将 "When to escalate" 移入或并入 | 20 分钟 |
| 2 | 样本量数字不一致（50-200+ vs 100+；5-15 vs 8-12 vs 8-15） | Step 3 / Pattern 1/4 / Guardrails 5 | 统一：问卷下限统一 100+（探索性概念测试注明 50+ 起步但不作统计声明）；访谈统一 5-15 为基准、模式特化处注明"因模式而异"；同步修订 SCORING SCOPE-03 文本 | 15 分钟 |
| 3 | 3 个失效锚点 | SKILL.md L89/L96/L101 | `#participant-recruitment` → `#6-participant-recruitment-strategies`；`#jobs-to-be-done-interviews` → `#1-jobs-to-be-done-jtbd-switch-interviews`；`methodology.md#question-design-principles` → 改为 `template.md#question-design-principles` | 10 分钟 |
| 4 | PROC-06 判定路径脆弱 | SCORING L84-86 / check.py L38 | 改为 skill 目录解析 `${SKILL_DIR}/resources/evaluators/...` 或改 output_contains 判定（agent 报告自评分数 ≥3.5） | 15 分钟 |

### 13.3 🟢 优化建议

| # | 问题 | 位置 | 建议 | 工作量 |
|---|------|------|------|:------:|
| 1 | 触发短语变体 | description | "Use when validating..." → "Use when the user validates..."（规范形式） | 2 分钟 |
| 2 | 伦理要求未在正文浮现 | Guardrails | 增加第 9 条：伦理要求（知情同意/匿名化/补偿）并指向 methodology.md §11 | 10 分钟 |
| 3 | Output 结构正文缺定义 | Outputs produced | 简述 `discovery-interviews-surveys.md` 的 6 个组成块（研究目标/方法/工具/招募/分析计划/洞察模板）并指向 template.md | 10 分钟 |
| 4 | 4 个 ❌ 装饰前缀 | Guardrails 陷阱 | 保留（功能性）或改纯文本标记 | 1 分钟（可选） |
| 5 | template.md 模板清单 5 项 vs SKILL.md 6 步 | template.md L6-12 | 对齐为 6 步或注明"模板视角" | 5 分钟 |
| 6 | 5.7-1 之外：SCOPE-03/QA-01 的 SCORING 文本与正文数字联动修订 | SCORING | 与修复 2 同步 | 5 分钟 |

### 13.4 总体结论

**019-discovery-interviews-surveys 是 4 个技能中唯一带完整引用体系（836 行高质量资源）的技能**：方法论内容专业准确（JTBD/Kano/主题编码/统计/伦理全覆盖）、rubric 自评设计在 corpus 中属上乘（10 项行为锚定标准 + 5 类研究指导 + 8 类失败模式自查闭环）、6 步工作流自包含可立即执行。主要缺口是 dossier 已标记的显式 Scope 节，以及本次新发现的 3 个失效锚点与样本量数字冲突。修复后可达 A−。**评级: B+。**
