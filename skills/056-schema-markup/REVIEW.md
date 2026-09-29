# REVIEW: 056-schema-markup

**审查日期**: 2026-08-06
**Skill 类型**: tool — structured data / schema.org markup（JSON-LD 实施、审计、验证）
**Body 行数**: 227 行
**参考文件数**: references/0, scripts/0（SKILL.md 引用的 3 个文件全部缺失，详见 §5）
**总文件数**: 4

---

## 1. 目录全量清单

```
056-schema-markup/
├── SKILL.md     (227 行)
├── SCORING.yaml (76 行)
├── check.py     (77 行)
└── REVIEW.md    (旧版 4 行 stub，本次重写)
```

该 skill 是**最小文件集**（仅 4 个文件），无 `references/`、`scripts/`、`assets/` 目录。但 SKILL.md 正文引用了 3 个不存在的文件：

| 引用路径 | 引用位置 | 是否存在 |
|---------|---------|:-------:|
| `scripts/schema_validator.py` | L39, L174, L178 | ❌ |
| `references/schema-types-guide.md` | L41, L131 | ❌ |
| `references/implementation-patterns.md` | L48, L120 | ❌ |

这是本次审查发现的**最重大缺陷**（详见 §5 与 §13 F-1/F-2/F-3）。skill-dossier.md（L466）声称"路径均为技能内 scripts/、references/"，该判断只核验了路径格式、未核验文件存在性，与实际情况不符（详见 §11）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `schema-markup`，全小写+连字符 ✓
- 长度: 13 字符，远低于 64 字符限制 ✓
- 匹配目录名 `056-schema-markup` ✓

### 2.2 description

原文（L3，共 256 字符）：

> "Implement, audit, and validate structured data (schema markup) for websites. Use when the user wants to add JSON-LD schema to pages, audit existing structured data for errors, validate against schema.org specifications, or optimize rich result eligibility."

逐句分析：

**第 1 句** (WHAT): "Implement, audit, and validate structured data (schema markup) for websites."
- 动词短语开头描述 skill 的 WHAT 功能。SKILL-SPEC §2.2 的 "Good" 范例本身就以裸动词开头（"Generate comprehensive test plans..."），故此写法合规 ✓
- "for websites" 限定了适用范围 ✓
- 隐含主语为 the skill，第三人称 ✓

**第 2 句** (WHEN): "Use when the user wants to add JSON-LD schema to pages, audit existing structured data for errors, validate against schema.org specifications, or optimize rich result eligibility."
- 使用规范触发短语 verbatim 模式 "Use when the user..." ✓
- 枚举了 4 个触发场景（添加 schema / 审计错误 / 对照 schema.org 验证 / 优化富结果资格）✓
- 场景与 body 的三 Mode（实施/审计/验证）一一对应 ✓

**KEYWORDS 检查**: 含 JSON-LD、schema、structured data、rich result 等领域术语与动作动词 ✓

**负面检查**:
- 无跨技能路由（"NOT for X, use Y"）✓
- 无第一/第二人称 ✓
- 无祈使式 "Use this skill to..." ✓
- 长度 256 字符 ≤ 1024 ✓
- 无通用/空洞表述 ✓

**结论**: description 完全合规，为语料库中描述质量较好的之一。可选的微调建议见 §13 O-1。

### 2.3 allowed-tools
- **缺失** ⚠️ — 属于 SKILL-SPEC §1.2 的可选字段，缺失不构成合规违规
- 但该 skill 的执行需要: Read（读取页面 HTML、marketing-context.md）、Bash（运行 `scripts/schema_validator.py`）、WebFetch（访问 Rich Results Test / validator.schema.org）
- 建议值: `allowed-tools: Read, Write, Bash, WebFetch`（详见 §13 O-2）

### 2.4 其他 frontmatter 字段
- 仅有 `name` 与 `description` 两个字段，无任何 SKILL-SPEC §1.3 禁止的字段（无 metadata、license、trigger、tags 等）✓

### 2.5 Frontmatter 语法
- YAML 分隔符 `---` 配对正确（L1/L4）✓
- description 为单行双引号字符串，无转义问题 ✓
- 无缩进错误 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Schema Markup Implementation (L6)                    — 标题
## Before You Start (L10-30)                           — 上下文检查 + 3 组采集问题，~21 行
## How This Skill Works (L34-60)                       — 三 Mode 并行，~27 行
  ### Mode 1: Audit Existing Markup (L36-42)           — 审计工作流，~7 行
  ### Mode 2: Implement New Schema (L44-51)            — 实施工作流，~8 行
  ### Mode 3: Validate & Fix (L53-59)                  — 验证修复工作流，~7 行
## Schema Type Selection (L63-82)                       — 选型表 + 堆叠规则，~20 行
## Implementation Patterns (L86-120)                    — JSON-LD 格式/放置/CMS/参考模式，~35 行
## Common Errors (L124-137)                             — 8 行错误表，~14 行
## Schema and AI Search (L141-157)                      — AI 搜索可见性，~17 行
## Testing & Validation (L160-183)                      — 4 项验证手段，~24 行
## Proactive Triggers (L187-196)                        — 6 个主动触发，~10 行
## Output Artifacts (L200-208)                          — 输出对照表，~9 行
## Communication (L212-218)                             — 沟通规范，~7 行
## Related Skills (L222-227)                            — 4 个关联技能，~6 行
```

结构总览: 13 个节，围绕"审计→实施→验证"三 Mode 主循环组织，前后呼应良好（选型表 → 错误表 → 验证节 → 主动触发 → 输出 → 沟通），是一个组织有序的 tool pattern skill。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

#### Workflow/Process 节
- 存在，形式为 `## How This Skill Works` 下的三 Mode ✓
- 每个 Mode 有明确的触发条件从句:
  - Mode 1: "When they have a site and want to know what schema exists and what's broken."（L36）
  - Mode 2: "When they need to add structured data to pages"（L44）
  - Mode 3: "When schema exists but rich results aren't showing or GSC reports errors."（L53）
- 三 Mode 的步骤编号各自连续（1-4 / 1-5 / 1-4）✓
- 有输入（采集问题三组）、处理（三 Mode）、输出（Output Artifacts 表）的完整闭环 ✓
- 有条件分支: Mode 选择、CMS 类型（L113-117）、页面类型（选型表）✓

#### Output Format 节
- 存在，形式为 `## Output Artifacts`（L200-208）✓
- 5 行对照表覆盖 5 种请求类型对应的交付物: 审计报告（含 completeness score per page）、完整 JSON-LD、修复后的 JSON-LD + 变更日志、AI 搜索可见性审查、实施计划 ✓
- 审计报告字段（schemas found / required fields / errors / score / priority fixes）与 SCORING.yaml 的 TEC-03 一致 ✓
- 不足: 审计报告的**具体模板结构**未给出（只有字段名列表），可执行性略低于给出的空间（见 §9.2 与 §13 O-8）

#### Scope/Limitations 节
- **不存在专门的 Scope/Limitations 节** ❌ — 这是 SKILL-SPEC §3.1 三条必需节的唯一缺口
- 现有边界性内容散落: 选型表附注 "don't add schema that doesn't match the page content"（L65）、堆叠规则 "Never add Product to a page that doesn't sell a product"（L82）、Related Skills 的路由说明（L222-227，部分含 "NOT for schema-specific work"）
- 缺少明确的"本 skill 不做什么": 不替代完整 SEO 审计、不做内容创作、不处理 Microdata/RDFa 迁移以外的格式、不保证富结果展示（Google 展示与否受多种因素影响）
- 修复方案见 §13 I-3

### 3.3 内容委托分析

Body 将两类核心内容委托给 reference 文件:
- **L41, L131**: `references/schema-types-guide.md` — 每种 schema 类型的 required vs recommended 字段（Mode 1 第 3 步和 Common Errors 表都依赖它）
- **L48, L120**: `references/implementation-patterns.md` — 每种类型的 copy/paste JSON-LD 模式（Mode 2 第 2 步的直接执行依据）

**两个被委托的文件都不存在**，委托链断裂。这意味着:
- Mode 2 的核心指令 "Pull the JSON-LD pattern from references/implementation-patterns.md"（L48）指向空处
- Common Errors 表的修复指引 "Check required vs. recommended in references/schema-types-guide.md"（L131）同样失效

委托比例: 3 处委托声明 / 227 行 body。比例不高，但委托的都是**核心执行资源**而非锦上添花的补充内容（详见 §5.3 与 §13 F-2/F-3）。

### 3.4 节编号/标题层级
- 标题层级: # → ## → ###，无跳级 ✓
- 三 Mode 用 ### 子节组织在 ## 之下，层级正确 ✓
- 无孤立标题、无标题下无内容 ✓

### 3.5 Body 长度合规
- 实际 227 行。pattern=tool 的目标行数约 300 行，硬限制 600 行
- 227 行略低于 tool pattern 目标，但考虑到 references 缺失使本应外置的内容无处安放，实际"内容总量"是符合 tool pattern 预期的——补齐引用文件后（见 §13 F-1/F-2/F-3）总信息量将恢复到 ~500 行当量 ✓

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- **三 Mode 闭环**: 审计（Mode 1）→ 实施（Mode 2）→ 验证修复（Mode 3）覆盖了 schema 的生命周期，且 Mode 3 的错误修复结果会反馈到 Mode 1 的审计项，逻辑闭环成立 ✓
- Mode 1 第 1 步 "Run scripts/schema_validator.py on the page HTML（or paste URL for manual check）"（L39）→ Mode 3 第 1 步 "Test on rich-results.google.com and validator.schema.org"（L56）→ Testing 节 4 项验证（L160-183）三处验证手段互相印证，无矛盾 ✓
- 采集问题三组（Current State / Site Details / Goals，L17-30）与三 Mode 的输入需求对应: 已有 schema → Mode 1；新页面类型 → Mode 2；报错/不展示 → Mode 3 ✓

**关键断点**: Mode 2 步骤 2 依赖 `references/implementation-patterns.md`、Mode 1 步骤 1 依赖 `scripts/schema_validator.py`，两个文件均缺失——agent 按文档执行必然失败或被迫自行发挥。这不是步骤间逻辑矛盾，而是**执行资源断链**（见 §5.3）。

### 4.2 事实准确性/过时扫描

1. **HowTo 富结果建议过时（dossier 已指出，本审查确认）** — L28 把 "HowTo steps" 列为富结果目标、L71 把 HowTo 列为 How-to 指南页的 primary schema、L114 提到 WordPress 加 HowTo schema、L147 "HowTo schema 让 AI 系统识别教程内容"。事实: Google 于 2023 年 8 月 29 日起停止展示 HowTo 富结果（2023 年 9 月官方公告弃用）。该建议对 Google 渠道已失效，对 AI 搜索渠道的表述（L147）勉强成立但无区分。**dossier 已标记，本审查确认。**

2. **FAQPage 富结果建议过时（dossier 未发现，本审查新发现）** — L153 明确建议 "Add FAQPage schema to any page with Q&A content — **even if it's just 3 questions**"，L191 主动触发 "any page with Q&A format and no FAQPage schema is leaving easy rich results on the table"。事实: Google 自 2023 年 8 月起将 FAQ 富结果限制为**权威政府/健康类站点**，普通站点不再获得 FAQ 富结果展示。L153/L191 对绝大多数站点是过度承诺。FAQPage 对 AI 搜索引用（QA-02 的意图）仍有一定价值，但 skill 未区分"Google 富结果价值"与"AI 搜索价值"两个语境。

3. **"Nesting Product inside Article — Invalid type combination"（L135）过度简化** — schema.org 的语法层面允许类型嵌套（Article 内嵌 Product 是产品评测文章的合法模式），Google 的 review snippet 文档也展示过 Article + Product 组合。真正的风险是**策略层**的（给非产品页加 Product 标记违反 Google 政策），而非"invalid type combination"。该行的措辞会让 agent 对合法的产品评测文章做出错误判断。建议改为策略风险表述（见 §13 I-6）。

4. **validator URL 不统一** — L56 写 `rich-results.google.com`，L164 写 `search.google.com/test/rich-results`。前者是旧域名（会重定向），两者指向同一工具，但同一 skill 内两处不一致，且 L56 的旧域名是"官方弃用迁移"的目标（见 §13 I-5）。

5. **GTM 风险提示位置滞后** — Mode 2 第 4 步把 "GTM injection" 作为 placement 选项之一直接列出（L50），未附带任何风险提示；而风险警告（"schema injected via GTM often isn't indexed by Google... Recommend server-side injection"）要到 Proactive Triggers（L193）才出现。技能内部信息一致（警告确实存在），但呈现顺序上，implement 模式的 agent 可能在无警告的情况下提供 GTM 方案。SCORING 的 NEG-02 检查此点，但 skill 应前置（见 §13 I-7）。

### 4.3 示例/代码正确性

- Placement 示例（L93-100）: `<head>` 内嵌 `<script type="application/ld+json">` — 正确 ✓
- 日期示例（L137）: `"2024-01-15"` / `"2024-01-15T10:30:00Z"` — ISO 8601 正确 ✓
- URL 示例（L133）: `https://example.com/image.jpg` not `/image.jpg` — 正确 ✓
- `"@context": "https://schema.org"`（L130）— 正确 ✓
- 常用类型组合（L67-77 选型表）: Organization+WebSite/SearchAction、Article+BreadcrumbList+Person、Product+Offer+AggregateRating、LocalBusiness+OpeningHoursSpecification — 均为业界标准组合 ✓
- 无完整的 JSON-LD 整块示例（正文只有一个空的 placement 骨架）— 完整模式委托给缺失的 implementation-patterns.md，这是 Mode 2 可执行性的实际缺口

### 4.4 条件完整性

- Mode 选择条件: 三个 Mode 各有 When 从句，条件互斥清晰（有没有 schema / 要不要新 schema / 报错不展示）✓
- CMS 分支（L113-117）: WordPress / Webflow / Shopify / 自定义 — 覆盖主流 ✓
- 富结果类型选择: 选型表按页面类型映射 ✓
- **缺失回退**: 当 reference 文件不存在或 validator 无法访问（离线环境）时，skill 无任何降级说明。对依赖外部网络的 Rich Results Test 与 validator.schema.org（L164-172），离线评测环境下 agent 会卡死（见 §9.3 与 §13 O-5）

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 缺失影响 |
|---------|:------------:|:-------:|---------|
| `scripts/schema_validator.py` | L39, L174, L178 | ❌ | Mode 1 第 1 步的执行工具；Testing 节第 3 项；`python3 scripts/schema_validator.py page.html` 命令直接失败 |
| `references/schema-types-guide.md` | L41, L131 | ❌ | Mode 1 第 3 步的字段核对依据；Common Errors 表 "required vs. recommended" 的指向 |
| `references/implementation-patterns.md` | L48, L120 | ❌ | Mode 2 第 2 步的 JSON-LD 模式库（skill 的核心交付物来源） |
| `marketing-context.md` | L13 | ⚠️ 条件性 | 属于"用户提供的上下文文件"模式（"If marketing-context.md exists, read it"），非 skill 自有资源，缺失不算缺陷 ✓ |

**引用存在率: 0/3 必存文件**。这是全语料库中引用缺失最严重的一类情况之一（dossier 统计约 15 个 skill 存在引用文件缺失，其中 188/195/196 因同类问题被评为 🟠）。本 skill 的降级因素: body 自身的选型表与错误表能支撑大部分实施任务，缺失文件不使 skill 完全不可用（详见 §5.3 与 §13 F-1/F-2/F-3 的修复方案）。

### 5.2 不可见资源审计

目录 `ls -laR` 确认: 无隐藏文件、无 .gitkeep、无空目录、无嵌套 skill。4 个文件全部可见且被 SKILL.md 或 SCORING.yaml 覆盖 ✓。

### 5.3 缺失文件的逐项影响分析

**schema-types-guide.md（影响 Mode 1 与 Common Errors）**:
- 该文件应包含各 schema 类型的 required vs recommended 字段清单（Google 官方标准）
- 缺失后果: 审计任务中 agent 无法准确判断字段缺口；Common Errors 表的 "Check required vs. recommended in references/schema-types-guide.md"（L131）变成死链
- 关键要求速查（修复时需覆盖）: Article（headline, image, datePublished, author）、Product（name, image, offers 或 aggregateRating/review）、FAQPage（mainEntity 数组）、Organization（name, logo）、LocalBusiness（name, image, telephone, address 等）、VideoObject（name, thumbnailUrl, uploadDate 等）、Event（name, startDate, location）— 详见 §13 F-3

**implementation-patterns.md（影响 Mode 2，最重）**:
- 该文件是 Mode 2 的核心: "Pull the JSON-LD pattern" 的唯一来源；Output Artifacts 承诺的 "copy/paste ready JSON-LD" 也依赖它
- 缺失后果: 实施任务中 agent 需要自行编写全部 JSON-LD 模式，容易遗漏 Google 必填字段或引入格式错误——恰是 CF-01（交付无效 JSON-LD）的诱发条件
- 修复方案见 §13 F-2（提供 10 类类型的完整 JSON-LD 模式清单与示例）

**schema_validator.py（影响 Mode 1 与 QA-01/PROC-07）**:
- 该脚本被引用 3 次（L39, L174, L178），是审计模式的主工具，被描述为具备: 提取页面 JSON-LD、按类型校验必填字段、输出 0-100 完备度评分
- 缺失后果: 审计任务的主工具不可用；SCORING.yaml 的 PROC-07 的脚本模式（`schema_validator\.py`）永远无法由工具日志命中
- 修复方案见 §13 F-1（提供最小可运行实现约 40 行）

### 5.4 Scripts 文件全文审查

无 scripts/ 目录。唯一被引用的 `scripts/schema_validator.py` 缺失（见 §5.3）。无其他脚本依赖 ✓。

### 5.5 跨 Skill 引用检查

- L222-227 引用 4 个技能: **seo-audit**、**site-architecture**、**content-strategy**、**programmatic-seo**
- 全部为**纯 prose 名称引用**（"see also: <skill-name>" 形式），无 `../other-skill/` 文件路径 ✓ — 完全符合 SKILL-SPEC §3.3
- L224 "NOT for schema-specific work — use schema-markup" 是 body 内的跨技能路由，属 SKILL-SPEC §2.5 允许的位置（description 禁止，body 允许）✓
- 引用关系合理: seo-audit（超出 structured data 的全面 SEO）、site-architecture（架构问题优先）、content-strategy（决定写什么内容）、programmatic-seo（规模化模板）— 四者的边界划分清晰且与 073-programmatic-seo 技能（dossier 🟢）的实际内容吻合 ✓

### 5.6 嵌套重复/死文件检查

- 无 self-nested 目录 ✓
- 无 .gitkeep / 空占位文件 ✓
- 无冗余文件 ✓
- REVIEW.md 旧 stub 仅 4 行，属待重写的审查文件而非 skill 内容 ✓

---

## 6. 语法与格式质量

### 6.1 拼写错误
全文无拼写错误。领域术语（BreadcrumbList、OpeningHoursSpecification、aggregateRating、datePublished、SameAs）拼写正确 ✓。

### 6.2 语法错误
- 无病句、无残缺句、无中英/葡英混杂 ✓
- 唯一风格性表述: L90 "Use JSON-LD. End of story." — 口语化断言，符合"果断专家"语气设定，可保留（见 §13 O-6 供可选软化）
- L102 "Multiple schema blocks per page are OK — use separate `<script>` tags or nest them in an array." — 表意清楚 ✓

### 6.3 中英/葡英混杂
全程英文，无中英混杂、无葡萄牙语残留（对照语料库中 262/276 等技能的葡语泄漏，本技能干净）✓

### 6.4 Markdown 格式破损
- 5 张表格（选型表 L67-77、Scope 表 L104-111、错误表 L126-138、输出表 L200-208、AI 搜索无表格）列对齐正确，表头/分隔行完整 ✓
- 代码围栏成对（L93-100 的 HTML 示例）✓
- 列表缩进一致，无编号断裂（对照 tpl 模板家族的 "1. **" 缺失缺陷，本技能无此问题）✓
- 无孤立 `**` 或杂散标记 ✓

### 6.5 占位符未填充
- 无 TODO / FIXME / TBD ✓
- L93 的 `{ ... your schema here ... }` 是有意的教学占位符（不是遗漏）✓
- 无未填充的模板变量 ✓

### 6.6 截断内容
- SKILL.md L227 以 programmatic-seo 引用完整收尾，无截断 ✓
- 所有表格、节均完整 ✓

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` 的 12 条规则:

| # | 规则 | 结果 | 说明 |
|---|------|:----:|------|
| 1 | name 小写+连字符，≤64 字符，匹配目录名 | ✅ | `schema-markup` 匹配 `056-schema-markup` |
| 2 | description 第三人称，WHAT+WHEN+KEYWORDS，≤1024 字符 | ✅ | 256 字符，四要素齐全 |
| 3 | description 无祈使/第一/第二人称开头 | ✅ | 裸动词 WHAT 句式（与规范 Good 范例一致） |
| 4 | description 无跨技能路由 | ✅ | 路由仅存在于 body Related Skills 节 |
| 5 | description 含触发信号短语 | ✅ | "Use when the user wants to..." |
| 6 | frontmatter 无禁止字段 | ✅ | 仅 name + description |
| 7 | body ≤600 行 | ✅ | 227 行 |
| 8 | 有 workflow/process 节 | ✅ | `## How This Skill Works`（三 Mode） |
| 9 | 有 scope/limitations 节 | ❌ | **无专门节**（见 §3.2 与 §13 I-3） |
| 10 | 无跨技能文件路径（../other-skill/） | ✅ | 仅 prose 名称引用 |
| 11 | allowed-tools 格式正确 | ⚠️ | 字段缺失（可选字段，非强制） |
| 12 | 路径仅指向本 skill 目录内 | ⚠️ | 路径格式正确（`references/`、`scripts/`），但**目标文件不存在** |

**合规率: 10/12 完全合规，2 项部分违规**

### 违规详情

**违规 1 — 缺少 Scope/Limitations 节（规则 9）**: SKILL-SPEC §3.1 要求 body 必须包含 scope/limitations 节（"under any heading name"）。本 skill 的边界性内容（"don't add schema that doesn't match the page content" L65、"Never add Product..." L82、Related Skills 的路由 L222-227）散落多处，无集中落点。该问题影响全语料库约 68% 的 skill，属最常见缺口。修复方案见 §13 I-3。

**违规 2 — 引用文件存在性（规则 12 的精神）**: 规则 12 的条文是"路径格式正确、指向本目录内"，本 skill 字面上满足；但 §5 已证实 3 个被引用文件不存在。这属于 §3.3 文件引用规则的精神要求（引用必须可解析）。dossier 将同类问题（引用文件缺失）列为语料库 Top-5 问题类型（~15 个 skill）。

**附注**: 规则 11（allowed-tools）按 SKILL-SPEC §1.2 属于可选字段，缺失不构成违规，仅作增强建议（§13 O-2）。

---

## 8. 人机感评估

### 8.1 Emoji 审计
全文仅 3 个 emoji，全部位于 L218 的 Communication 节: 🟢（verified）/ 🟡（medium）/ 🔴（assumed）— 作为置信度标记，属**功能性使用**，与 §8.5 的沟通规范自洽 ✓。无装饰性 emoji 滥用（对照 072-mobile-design 的 20+ 个 emoji 问题，本技能为零）✓。

### 8.2 全大写/喊叫式语言
无 `STOP!`、`MANDATORY`、`CRITICAL` 等喊叫式表述（对照 032-clinical-reports 的 "⚠️ MANDATORY" 问题）✓。"Never" 出现 3 次（L82 "Never add Product"、L133/134），均在合理强调范围内 ✓。

### 8.3 Persona 语气分析
- 开场 L8: "You are a structured data and schema.org markup specialist." — 第二人称 persona 开场，属语料库惯例（约半数技能使用），位于 body 而非 description，不构成规范违规
- 整体为**专业顾问语气**: "Conclusion first — answer before explanation"（L215）、"Actions have owners and deadlines — no 'we should consider'"（L217），简洁有力
- 唯一口语化点: L90 "Use JSON-LD. End of story." — 果断专家腔，在该语境下（反驳 Microdata/RDFa 遗产格式）有效且不失专业，可接受
- 无营销腔、无 pep-talk、无外部品牌推销（对照 007 的 K-Dense 广告问题，本技能干净）✓

### 8.4 人机边界分析
- 本技能是纯技术工具型 skill，风险等级低于法律/医疗类技能，因此**无强制人类审批点**是合理设计（对比 258/279 等技能）
- 存在的边界意识:
  - L193 对 GTM 注入的索引风险给出明确警告并推荐 server-side ✓
  - L134/L82 对"标记与页面内容不符"的 Google 政策风险给出硬规则 ✓
  - Communication 节要求 findings 带置信度标注（🟢/🟡/🔴），把"已验证"与"假设"分开 ✓
- 弱点: L50 在 Mode 2 的 placement 选项中直接提供 GTM 而未同步风险（见 §4.2-5 与 §13 I-7）

### 8.5 人称分析
- description: 纯第三人称 ✓
- body 指令层: 第二人称 persona（"You are..."）+ 祈使句（"Run...", "Pull...", "Advise..."），为语料库工具型技能的常规写法 ✓
- 人称使用与技能类型匹配，无层次混乱 ✓

### 8.6 表格使用评估
5 张表格全部为**数据型表格**（类型映射、作用域、错误、输出、富结果映射），是决策表的最优形式，无冗余表格（对照 055-paid-ads 的平台表重复问题，本技能无重复表）✓。

---

## 9. 可执行性评估

### 9.1 独立可执行性
假设 agent 只拿到 SKILL.md（无目录探索），能否开工:
- **Mode 2（实施）**: 部分可行 — 选型表（L67-77）+ 放置示例（L93-100）+ 错误表（L126-138）可支撑基础类型（Organization/Article/BreadcrumbList/Product）的 JSON-LD 编写；但 L48 强制要求 "Pull the JSON-LD pattern from references/implementation-patterns.md" 指向空处，agent 需自行补全模式
- **Mode 1（审计）**: 受挫 — 主工具 `schema_validator.py` 不存在，L39 步骤必然失败；agent 只能靠备选的 "paste URL for manual check" 路径
- **Mode 3（验证修复）**: 可行 — rich-results.google.com 与 validator.schema.org 均为公开 URL，错误映射逻辑（错误表）完整 ✓
- 打分: **6/10** — Mode 3 完全可行，Mode 2 基础可行、深度受阻，Mode 1 主路径失败

### 9.2 步骤可操作性

| Mode | 步骤 | 可操作性 | 问题 |
|------|------|:--------:|------|
| Mode 1 | 1. 运行 schema_validator.py | 🔴 | 脚本不存在，命令必失败 |
| Mode 1 | 2. 审阅 GSC Enhancements | 🟢 | 具体入口明确 |
| Mode 1 | 3. 对照 schema-types-guide.md | 🔴 | 文件不存在 |
| Mode 1 | 4. 交付审计报告 | 🟡 | 字段有清单（TEC-03），无报告模板 |
| Mode 2 | 1. 识别页面类型 | 🟢 | 选型表完整 |
| Mode 2 | 2. 提取 JSON-LD 模式 | 🔴 | 模式库不存在 |
| Mode 2 | 3-5. 填充/放置/交付 | 🟡 | 放置指导在 L50，交付约定在 Output Artifacts |
| Mode 3 | 1-4. 验证/映射/修复/解释 | 🟢 | 完整闭环，唯一完全可执行 Mode |

### 9.3 工具依赖合理性
- 无第三方 API 密钥依赖 ✓
- 网络依赖: Rich Results Test 与 validator.schema.org（L164-172）需要外网；本地脚本 `schema_validator.py`（缺失）本应提供离线降级路径 — **修复该脚本后离线可执行性将显著提升**（见 §13 F-1）
- 评测相关性: SCORING 的 PROC-07 依赖工具日志命中 `schema_validator\.py|rich-results|validator\.schema\.org` — 由于脚本缺失，评测中 agent 只能走 web validator 路径命中；修复脚本后两条路径均可命中

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 共 20 个 criteria（SCOPE-01~03 / PROC-01~07 / TEC-01~04 / NEG-01~02 / QA-01~04）+ 2 个 critical failure。与 SKILL.md 的对应关系:

| 测评点 | 类别 | judge | 对应 SKILL.md 内容 | 一致 |
|--------|------|:-----:|-------------------|:----:|
| SCOPE-01 | scope | llm | description L3 + 三 Mode 定位 | ✅ |
| SCOPE-02 | scope | llm | L36/L44/L53 的 Mode 条件从句 | ✅ |
| SCOPE-03 | scope | llm | 选型表 L67-77 | ✅ |
| PROC-01 | process | script | L90 "Use JSON-LD" | ✅ |
| PROC-02 | process | script | L130 `"@context": "https://schema.org"` | ✅ 有假阴性风险（见 10.3） |
| PROC-03 | process | script | L132 name 非空规则 | ✅ |
| PROC-04 | process | llm | L50/L93-100 放置指导 | ✅ |
| PROC-05 | process | llm | L82/L134 内容匹配规则 | ✅ |
| PROC-06 | process | script | L133/L137 URL 与日期 | ⚠️ 只查 URL 不查日期（见 10.3） |
| PROC-07 | process | script | L39 审计工具 | ⚠️ 目标脚本缺失（见 10.3） |
| TEC-01 | technical | script | Output Artifacts 的完整 JSON-LD | ⚠️ 模式过松（见 10.3） |
| TEC-02 | technical | llm | 堆叠规则 L79-82 | ✅ |
| TEC-03 | output | llm | Output Artifacts 审计报告行 L204 | ✅ |
| TEC-04 | output | llm | L59 "Explain why the fix works" | ✅ |
| NEG-01 | negative | llm | L82/L134/L196 反滥用规则 | ✅ |
| NEG-02 | negative | llm | L193 GTM 风险警告 | ✅ |
| QA-01 | qa | script | Testing 节 L160-183 | ✅ |
| QA-02 | qa | llm | Schema and AI Search 节 L141-157 | ✅ |
| QA-03 | qa | llm | Proactive Triggers 节 L187-196 | ✅ |
| QA-04 | qa | llm | Communication 节 L212-218 | ✅ |

覆盖完整性: 良好。20 个测评点全部能在 SKILL.md 中找到明确出处，抽取忠实、无虚构测评点。

### 10.2 Script vs LLM 分布
- script judge: 7 项（PROC-01/02/03/06/07, TEC-01, QA-01）— check.py 恰好实现这 7 项，与 SCORING.yaml 完全一致 ✓
- llm judge: 13 项
- check.py docstring "Run all 7 script checks" 与实际 7 项一致 ✓（对照 026 的 docstring 10 vs 9 计数错误，本 skill 无此问题）

### 10.3 check.py 实现问题

1. **PROC-06 只执行了一半承诺**: criterion description 承诺 "URLs in schema are absolute...; **dates use ISO 8601 format**"，但 check 只测 `(?i)https?://`（任何含 http 的输出都通过，包括与日期无关的文本）。日期一半完全未执行。建议双正则或拆分为两个 criterion（见 §13 I-4）。
2. **PROC-02 尾斜杠假阴性风险**: 正则 `"@context"\s*:\s*"https://schema.org"` 要求精确匹配无尾斜杠。schema.org 的官方 @context 有 `https://schema.org` 与 `https://schema.org/` 两种合法写法（带尾斜杠同样可解析）。agent 输出带尾斜杠版本时该检查误判失败。建议 `https://schema\.org/?`（见 §13 O-3）。
3. **TEC-01 过松**: 模式 `(?i)(```json|valid json|parses|```{0,2}json)` 中单独出现单词 "parses" 即可通过——任何解释性文本都可能误命中，区分度低。建议收紧为 ```` ```json ```` 围栏或 "valid JSON" 完整短语（见 §13 O-4）。
4. **PROC-07 依赖缺失脚本**: 模式允许 `schema_validator\.py|rich-results|validator\.schema\.org` 三选一，其中主选项指向不存在的脚本。若评测 agent 尝试运行脚本（按 skill 指示）将失败；只能靠后两个 web validator 选项命中。修复 schema_validator.py 后此问题自然消失（见 §13 F-1）。
5. **PROC-06 判定力弱**: `(?i)https?://` 对"audit 报告中附上客户官网链接"这类无关输出也会放行，无法证明 schema 内 URL 绝对。属于宽松检查，不会产生假阴性，风险低，可接受。
6. **check.py 边界情况（微小）**: `_is_path` 分支在 agent 输出恰好是存在的文件路径字符串时跳过 `set_agent_output`，理论上有状态污染风险；实际评测中 agent 输出为长文本，不会命中，风险极低。

### 10.4 Critical Failures 分析

- **CF-01（交付无法通过验证的 JSON-LD 且声称就绪）→ cap_to_0**: 合理且必要 — 这是本 skill 最核心的失败模式；skill 自身的 Testing 节（L160-183）与 CF-01 互相印证 ✓
- **CF-02（为页面不可见内容添加 schema）→ cap_to_0**: 合理 — 对应 L82/L134 的政策红线与 NEG-01；与 Google 反富结果操纵立场一致 ✓
- 两个 CF 均为"行为底线"型，判定标准客观（LLM judge 可依据交付物文本判定），无过度惩罚风险 ✓

### 10.5 缺失测评点建议

- 无 `marketing-context.md` 预检（L13）的 criterion — 该步骤被描述为 "Check context first"，属流程第一步，可考虑加入（低优先）
- 无 ISO 8601 日期独立 criterion（PROC-06 仅覆盖 URL，见 10.3-1）
- 无 CMS 特定建议（L113-117）的 criterion — 可选
- 无 "Multiple conflicting @type on same entity"（L195 主动触发之一）独立 criterion — QA-03 泛化覆盖，可接受
- 无产品评测文章场景（Article + Product 合法嵌套）的正向 criterion — 与 §4.2-3 的过度简化相关联

---

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier（skill-dossier.md L462-467）记录：

> - **逻辑**: 三种 Mode 覆盖审计/实施/修复闭环，堆叠规则和错误表一致；仅 HowTo schema 建议过时（Google 已于 2023 年弃用 HowTo 富结果）。
> - **语法**: 规范清晰，无错别字。
> - **人机感**: 专业语气，🟢🟡🔴 为沟通规范的置信度标记，使用得当。
> - **合规**: Description 第三人称，含 Workflow/Output Artifacts/触发条件，路径均为技能内 scripts/、references/，正文 227 行 ≤600。
> - **总评**: 🟢 逻辑与合规良好，仅需更新 HowTo 富结果建议。

逐条验证:

- **逻辑判定** ✅ 本审查 §4.1 复核无误（三 Mode 闭环、堆叠规则一致）。
- **"仅 HowTo 建议过时"** ⚠️ 部分成立但不完整 — 本审查确认 HowTo 过时（§4.2-1），但**遗漏了两项**: ①FAQPage 富结果建议同样过时（§4.2-2）；②三处引用文件缺失（§5）。dossier 的结论"仅需更新 HowTo 富结果建议"低估了修复工作量。
- **语法判定** ✅ §6 复核无误。
- **人机感判定** ✅ §8 复核无误。
- **合规判定** ⚠️ "路径均为技能内 scripts/、references/" — 该判断只核验了路径**格式**（相对路径、无 `../`），未核验文件**存在性**。实际 `ls -laR` 证实 3 个引用文件全部不存在（§5.1）。路径格式合规 ✅，但引用完整性是硬缺口。
- **总评 🟢** ⚠️ 与本次深度审查存在分歧 — 本审查将评级**下调为 🟡**（见 §12.2）：核心原因不是逻辑或格式问题（这两项确实好），而是"Mode 1 主工具与 Mode 2 模式库双双缺失"对可执行性的实质影响。dossier 自身将"引用文件/脚本缺失"列为语料库 Top-5 问题类型，188/195/196 等技能均因此被评为 🟠——本 skill 因 body 自足性较好而维持 🟡（未至 🟠）。

**结论**: dossier 的 🟢 评级在其未核验引用文件的前提下成立；本审查补上该核验后，评级调整为 🟡 B（74/100），但认同 dossier 对逻辑、语法、人机感三项的判定。

---

## 12. 综合评分

### 12.1 维度评分表（8 维度加权）

| 维度 | 分数 | 权重 | 加权 | 主要扣分点 |
|------|:----:|:----:|:----:|------|
| Frontmatter | 9/10 | 10% | 0.90 | description 完全合规；allowed-tools 缺失（可选字段） |
| Body 结构 | 8/10 | 10% | 0.80 | 无显式 Scope/Limitations 节；审计报告无模板 |
| 逻辑一致性 | 7/10 | 15% | 1.05 | HowTo/FAQPage 富结果建议过时；Product-in-Article 过度简化；URL 不统一 |
| 参考完整性 | 4/10 | 15% | 0.60 | 3 个引用文件全部缺失（0/3 存在率） |
| 语法格式 | 9/10 | 10% | 0.90 | 零错字、零破损、零占位符 |
| 规范合规 | 9/10 | 15% | 1.35 | 条文 10/12 完全合规（scope 节缺失 + 引用存在性） |
| 人机感 | 9/10 | 10% | 0.90 | 功能性 emoji、专业语气、无喊叫无推销 |
| 可执行性 | 6/10 | 15% | 0.90 | Mode 3 完全可行、Mode 2 基础可行、Mode 1 主路径失败 |
| **加权总分** | | **100%** | **7.40/10** | |

### 12.2 评级

**🟡 B（74/100）** — 较 dossier 的 🟢 下调一档。理由: ①Mode 1 主工具 `schema_validator.py` 与 Mode 2 模式库 `implementation-patterns.md` 缺失，直接破坏 skill 自述的两个核心工作流（§5.3）；②HowTo 之外还存在 FAQPage 富结果建议过时（§4.2-2）。同时，本 skill 在逻辑自洽、语法质量、人机感、description 合规方面均属语料库中上水平，且缺失文件修复成本低（3 个文件，详见 §13 修复工作量），故维持 🟡 而非 🟠。

与旧版 REVIEW stub（2026-08-05，🟢 B 52/100）的对比: 旧版 52 分口径偏严且未核验引用文件（其摘要仅提及 HowTo 过时与第二人称开场）。本审查重新校准为 74/100，维度更完整、扣分项均有文件级证据。旧版两项判断（HowTo 过时 ✓、第二人称开场 ✓ 即 L8 persona）均保留并纳入 §4.2/§8.3。

---

## 13. 修复建议（按优先级分层）★ 重点 ★

### 🔴 致命缺陷（必须修复）

**F-1: 创建缺失的 `scripts/schema_validator.py`（影响 Mode 1 与 PROC-07）**

- **位置**: 新建 `scripts/schema_validator.py`（SKILL.md L39/L174/L178 引用）
- **现状**: Mode 1 第 1 步与 Testing 节第 3 项的执行工具不存在；`python3 scripts/schema_validator.py page.html` 命令必然失败；SCORING PROC-07 的主命中模式永远落空
- **修复**: 按 SKILL.md 描述的功能契约实现（提取 JSON-LD 块 → 按类型校验必填字段 → 输出 0-100 完备度评分）。最小可用实现参考（约 40 行）:

```python
#!/usr/bin/env python3
"""Extract and validate JSON-LD from an HTML file. Score 0-100 by completeness.
Usage: python3 scripts/schema_validator.py page.html
"""
import json, re, sys
from html.parser import HTMLParser

REQUIRED = {  # per Google structured data documentation
    "Article": ["headline", "image", "datePublished", "author"],
    "Product": ["name", "image", "offers"],
    "FAQPage": ["mainEntity"],
    "Organization": ["name", "logo"],
    "LocalBusiness": ["name", "image", "telephone", "address"],
    "VideoObject": ["name", "thumbnailUrl", "uploadDate"],
    "Event": ["name", "startDate", "location"],
    "BreadcrumbList": ["itemListElement"],
}

class JSONLDExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks, self.in_jsonld, self.buf = [], False, []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "script" and d.get("type") == "application/ld+json":
            self.in_jsonld, self.buf = True, []
    def handle_data(self, data):
        if self.in_jsonld:
            self.buf.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            self.blocks.append("".join(self.buf))

def validate(html):
    p = JSONLDExtractor(); p.feed(html)
    if not p.blocks:
        return [("no-jsonld", "No JSON-LD blocks found", 0)]
    results = []
    for i, raw in enumerate(p.blocks, 1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            results.append((f"block-{i}", f"Invalid JSON: {e}", 0)); continue
        types = data.get("@type", [])
        types = types if isinstance(types, list) else [types]
        if not types:
            results.append((f"block-{i}", "Missing @type", 0)); continue
        missing = sorted({f for t in types for f in REQUIRED.get(t, []) if not data.get(f)})
        score = max(0, 100 - 20 * len(missing))  # each missing required field -20
        results.append((f"block-{i}", f"{','.join(types)} missing={missing or 'none'}", score))
    return results

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        for block_id, note, score in validate(f.read()):
            print(f"{block_id}: {note} — score {score}/100")
```

- 影响面: 新增 1 个文件 ~40 行；修复后 Mode 1 全流程可执行，PROC-07 两条命中路径（脚本 + web validator）齐全
- 不修复的后果: 审计模式（skill 的第一 Mode）无法按文档执行；评测中 agent 被迫偏离 skill 指令

**F-2: 创建缺失的 `references/implementation-patterns.md`（影响 Mode 2，最重）**

- **位置**: 新建 `references/implementation-patterns.md`（SKILL.md L48/L120 引用）
- **现状**: Mode 2 第 2 步 "Pull the JSON-LD pattern" 的唯一来源不存在；Output Artifacts 承诺的 "copy/paste ready JSON-LD" 无实现支撑
- **修复**: 按选型表（L67-77）的 10 种页面类型提供完整 JSON-LD 模式。文件结构建议:

```markdown
# Implementation Patterns — copy/paste JSON-LD per page type

## Organization (site-wide, template header)
{ "@context": "https://schema.org", "@type": "Organization",
  "name": "Example Corp", "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": ["https://twitter.com/example", "https://www.linkedin.com/company/example"] }

## WebSite + SearchAction (homepage)
{ "@context": "https://schema.org", "@type": "WebSite", "name": "...",
  "url": "...", "potentialAction": { "@type": "SearchAction",
  "target": "https://example.com/search?q={search_term_string}",
  "query-input": "required name=search_term_string" } }

## Article + BreadcrumbList + Person (blog post)
{ "@context": "https://schema.org", "@type": "Article", "headline": "...",
  "image": "https://example.com/hero.jpg", "datePublished": "2026-01-15",
  "dateModified": "2026-01-15", "author": { "@type": "Person", "name": "...",
  "sameAs": ["https://linkedin.com/in/..."] } }
{ "@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [ { "@type": "ListItem", "position": 1, "name": "Home", "item": "/" },
  { "@type": "ListItem", "position": 2, "name": "Category", "item": "/category" } ] }

## FAQPage (Q&A content; NOTE: since 2023-08 Google limits FAQ rich
## results to authoritative government/health sites — value is now mostly AI search)
{ "@context": "https://schema.org", "@type": "FAQPage",
  "mainEntity": [ { "@type": "Question", "name": "Q1",
  "acceptedAnswer": { "@type": "Answer", "text": "A1" } } ] }

## Product + Offer (product page)
{ "@context": "https://schema.org", "@type": "Product", "name": "...",
  "image": "...", "offers": { "@type": "Offer", "price": "19.99",
  "priceCurrency": "USD", "availability": "https://schema.org/InStock" } }

## LocalBusiness, VideoObject, Event, CollectionPage, HowTo
## (same pattern per type; include required fields from schema-types-guide.md)
```

- 每类附: 完整 JSON-LD + 必填字段批注 + 常见错误提示
- 影响面: 新增 1 个文件 ~150-200 行（可在 600 行 body 限制外安全承载）
- 不修复的后果: 实施模式的核心输出（copy/paste JSON-LD）质量无保障，直接诱发 CF-01（交付无效 JSON-LD）

**F-3: 创建缺失的 `references/schema-types-guide.md`（影响 Mode 1 与 Common Errors）**

- **位置**: 新建 `references/schema-types-guide.md`（SKILL.md L41/L131 引用）
- **现状**: Mode 1 第 3 步的字段核对依据不存在；Common Errors 表 "Check required vs. recommended"（L131）成为死链
- **修复**: 提供每种类型的 required / recommended 字段表（基于 Google 官方文档），结构建议:

```markdown
# Schema Types Guide — required vs recommended fields (Google standard)

| Type | Required | Recommended |
|------|----------|-------------|
| Article | headline, image, datePublished, author | dateModified, publisher |
| Product | name, image, offers 或 aggregateRating/review | brand, sku, review |
| FAQPage | mainEntity (Question[]/Answer[]) | — |
| Organization | name, logo | sameAs, url, contactPoint |
| LocalBusiness | name, image, telephone, address | openingHours, geo |
| VideoObject | name, thumbnailUrl, uploadDate | contentUrl, duration |
| Event | name, startDate, location | endDate, offers, image |
| BreadcrumbList | itemListElement (position, name, item) | — |
| HowTo (Google rich result deprecated 2023-08; keep only for other engines) | — | step, totalTime |

Note: "required" below means Google-required for the corresponding rich result,
not schema.org spec requirements.
```

- 影响面: 新增 1 个文件 ~60-80 行
- 不修复的后果: 审计报告（Mode 1 交付物）的"required fields present/missing"判定缺乏权威依据

### 🟡 重要缺陷（建议修复）

**I-1: 更新 HowTo 富结果建议（dossier 已标记，给出具体改法）**
- 位置: L28（Goals 富结果目标）、L71（选型表）、L114（WordPress 段）、L147（AI 搜索段）
- 修复: L71 表格行改为 "How-to guide | Article（含 Step 结构）| BreadcrumbList"，或保留 HowTo 但加注: "HowTo 富结果已于 2023-08 被 Google 弃用；保留 HowTo 标记仅对非 Google 引擎与 AI 搜索有意义"。L28 的 "HowTo steps" 从富结果目标列表移除
- 不修复的后果: agent 承诺用户无法获得的 HowTo 富结果，损害交付可信度

**I-2: 更新 FAQPage 建议（dossier 未发现，本审查新发现）**
- 位置: L153（"even if it's just 3 questions"）、L191（主动触发）
- 修复: 改为区分语境 — "FAQPage 自 2023-08 起仅在权威政府/健康站点展示 Google FAQ 富结果；对普通站点，FAQPage 的价值在 AI 搜索引用（Perplexity/AI Overviews 可直接抽取 Q&A）。若有 Q&A 内容仍建议添加，但向用户说明收益渠道"。
- 不修复的后果: 与 I-1 相同的过度承诺问题

**I-3: 新增 `## Scope and Limitations` 节（SKILL-SPEC §3.1 规则 9）**
- 位置: 建议置于 "## Related Skills"（L222）之前
- 修复: 新增约 8-10 行:

```markdown
## Scope and Limitations

This skill handles structured data only — not full SEO. For technical/content SEO
spanning more than markup, use **seo-audit**. This skill does NOT:

- Guarantee rich results. Google decides eligibility; markup only removes
  technical blockers (and since 2023-08, HowTo/FAQ rich results are largely
  unavailable — see Schema and AI Search).
- Rewrite page content or decide what content to create (use content-strategy).
- Diagnose URL architecture, internal linking, or crawl issues (use site-architecture).
- Generate schema at scale for thousands of pages (use programmatic-seo).
- Convert legacy Microdata/RDFa automatically — it recommends JSON-LD and
  provides guidance, not automated migration scripts.
```

- 不修复的后果: agent 可能把不属于本 skill 范围的任务（架构问题、内容策略）误收进来，或对富结果做出保证性承诺

**I-4: PROC-06 增加日期校验（criterion 承诺的一半未执行）**
- 位置: SCORING.yaml PROC-06 的 check + check.py L41
- 修复: 拆分两个脚本检查:

```python
result["PROC-06"] = output_contains("(?i)https?://")                       # URLs absolute
result["PROC-06b"] = output_contains(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?")  # ISO 8601 dates
```

- 并在 SCORING.yaml 中相应补充 PROC-06b 条目（description: "Dates use ISO 8601 format"）
- 不修复的后果: 日期格式错误（agent 输出 "January 15, 2026"）在评测中不被发现

**I-5: 统一 validator URL**
- 位置: L56 `rich-results.google.com` vs L164 `search.google.com/test/rich-results`
- 修复: L56 改为与 L164 一致的 `https://search.google.com/test/rich-results`（旧域名现已重定向，统一可避免 agent 困惑）

**I-6: 修正 "Nesting Product inside Article" 的错误表述**
- 位置: L135
- 修复: "Nesting Product inside Article — Invalid type combination" 改为 "Adding Product markup to a page without a purchasable product — policy violation"。schema.org 语法允许嵌套（产品评测文章是合法场景），真实风险是内容与标记不符的 Google 政策，而非语法非法
- 不修复的后果: agent 会对合法的产品评测文章（Article 内嵌 Product）做出错误否决

**I-7: GTM 风险提示前置到 Mode 2**
- 位置: L50（Mode 2 第 4 步）
- 修复: 在 "Advise on placement（inline script in head, CMS plugin, GTM injection）" 后追加: "If GTM injection is chosen, flag that client-side rendered schema may not be indexed by Google — recommend server-side injection（见 Proactive Triggers）"
- 不修复的后果: implement 模式的 agent 可能无警告地推荐 GTM 方案，与 NEG-02 测评点的精神冲突

### 🟢 优化建议（锦上添花）

**O-1: description 关键词补充**
- 位置: L3
- 修复: 可在 WHEN 从句追加 "GSC structured data errors, rich snippets" 等触发词，提升匹配度。可选，当前 description 已合规

**O-2: 声明 allowed-tools**
- 建议值: `allowed-tools: Read, Write, Bash, WebFetch`（Bash 用于运行修复后的 schema_validator.py；WebFetch 用于访问两个在线 validator）
- 属可选字段，不修不构成合规问题，但在 harness 权限预配置场景下有价值

**O-3: PROC-02 容忍尾斜杠**
- check.py L38: `"@context"\s*:\s*"https://schema\.org/?` — 1 字符改动，消除合法变体的假阴性

**O-4: TEC-01 收紧**
- check.py L45: 移除单独匹配的 `parses`，改为 `(?i)(```json|valid json|```{0,2}json)` 或要求 "parses" 需与其他关键词共现。提高判别力

**O-5: 离线降级说明**
- Testing 节（L160-183）补一句: "若无法访问在线 validator，使用 scripts/schema_validator.py 的本地评分（0-100）作为替代" — 与 F-1 修复联动，提升离线评测环境可执行性

**O-6: "End of story." 语气（可选）**
- L90 可保留（果断专家腔在该语境有效）；若追求语料库统一中性，可改为 "Use JSON-LD. Microdata and RDFa are legacy formats."。低优先，纯风格选择

**O-7: AI 搜索声明标注依据**
- L145-150（"FAQPage schema boosts citation likelihood" 等 4 条断言）加一句免责: "这些机制尚无公开基准，为实践经验推断" — 避免 agent 向用户转述为已证实结论（与 Communication 节 🟢/🟡/🔴 置信度体系呼应）

**O-8: 审计报告模板化**
- Output Artifacts 的审计行（L204）补一个 6 字段报告骨架（Schema Type / Found / Required Missing / Errors / Score 0-100 / Priority），与 TEC-03 测评点对齐，降低审计交付物方差

### 修复工作量估计

| 层级 | 项数 | 涉及文件 | 预计改动行数 | 风险 |
|------|:----:|---------|:----------:|------|
| 🔴 致命 | 3 | scripts/schema_validator.py（新建 ~40 行）、references/implementation-patterns.md（新建 ~180 行）、references/schema-types-guide.md（新建 ~70 行） | ~290 行新增 | 低（均为新增文件，不触碰现有内容） |
| 🟡 重要 | 7 | SKILL.md ×6 处 + SCORING.yaml + check.py | ~35 行 | 低-中（I-4 涉及评测逻辑，改后需重跑一次评测验证） |
| 🟢 优化 | 8 | SKILL.md ×5 处 + check.py ×2 处 | ~20 行 | 低 |
| **合计** | 18 | 6 个文件（3 新建 + 3 修改） | **~345 行** | |

优先序建议: F-1 → F-2 → F-3（补齐引用完整性，直接修复 Mode 1/2 主工作流与 PROC-07 命中）→ I-1 → I-2（事实准确性，涉及交付承诺）→ I-3（规范合规）→ I-4（评测完整性）→ 其余按成本排序。全部完成预计 2-3 小时内，完成后本 skill 可恢复至 🟢 级（body 质量本身过硬，缺陷集中在缺失资源与两处过时建议）。

---

## 附录: 审查过程记录

### 读取的文件列表

| 文件 | 行数 | 读取方式 | 状态 |
|------|:----:|---------|:----:|
| SKILL.md | 227 | 全文逐行精读 + 正则扫描（emoji/引用/行号定位） | ✅ |
| SCORING.yaml | 76 | 全文，20 criteria + 2 CF 逐条对照 | ✅ |
| check.py | 77 | 全文，7 项脚本检查逐条验证 | ✅ |
| REVIEW.md（旧 stub） | 4 | 全文，重写前核验 | ✅ |
| _shared/SKILL-SPEC.md | 162 | 全文（12 条合规清单） | ✅ |
| _shared/checker.py | — | 存在性确认（check.py import 依赖） | ✅ |
| skill-dossier.md | 1203 | L462-467（056 条目）定位核验 | ✅ |

### 读取统计
- Skill 内部文件总行数: 384 行（4 文件）
- 规范参考: SKILL-SPEC.md 162 行 + dossier 相关条目
- 目录核验: `ls -laR` 全量（确认无 references/、scripts/、隐藏文件）

### 审查方法
- 全部文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条规则
- 引用完整性: 对 SKILL.md 中全部 `scripts/`、`references/` 引用做存在性矩阵核验（发现 3 个缺失文件）
- 事实核查: HowTo/FAQPage 富结果政策以 Google 2023-08 变更公告为准；schema.org 类型嵌套规则以规范语义为准
- 与旧版 stub（4 行）的关系: 保留其两个正确判断（HowTo 过时、第二人称开场）；52/100 评分因口径偏差（未核验引用文件、缺维度加权）重校准为 74/100
- 与 dossier 🟢 评级的分歧处理: §11 逐条验证后下调一档（引用文件缺失 + FAQPage 遗漏），分歧原因与依据已文档化
- 未验证事项: 未实跑任何 JSON-LD 校验（无真实页面样本）；check.py 未在评测 harness 中实跑；修复后的 schema_validator.py 实现为静态设计稿，落地后应补充一次冒烟测试
