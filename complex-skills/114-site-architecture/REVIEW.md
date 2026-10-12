# REVIEW.md — 114-site-architecture 深度审查报告

| 项目 | 内容 |
|------|------|
| 审查对象 | `D:\SkillIF\skill-experiment\complex-skills\114-site-architecture\`（全部 4 个文件逐行阅读 + diff 比对） |
| 审查日期 | 2026-08-06 |
| 依据标准 | `_shared/SKILL-SPEC.md` v1.0（§1–§5 全部条款） |
| 参考材料 | 审查档案 `skill-dossier.md`（Batch 101-125 条目、汇总统计、状态行）、`_shared/CHECKER-LIBRARY.md`、对照集 `complex-skills-no-trigger/114-site-architecture/` |
| 审查方法 | 全文件逐行阅读 + 嵌套/顶层正文 diff 比对 + 交叉一致性核对（SKILL.md ↔ SCORING.yaml ↔ check.py）+ 对照 SKILL-SPEC 合规清单逐项打勾 + 目录存在性验证（scripts/、references/ 引用路径逐个检查） |
| 总体结论 | 内容质量高、三模式工作流设计扎实（dossier 🟢 结论在内容面成立）；但发现 1 处**嵌套 SKILL.md 残留**（含 §1.3 违禁 frontmatter 字段）、**4 处悬空文件引用**（含评测脚本 `scripts/sitemap_analyzer.py` 缺失，直接影响 SCORING PROC-01 的确定性判定）、**缺 Scope/Limitations 必需节**。整体定级 🟡（完成 P0/P1 修复后回 🟢），与 dossier 的 🟢 存在"内容强、结构有缺口"的认知差异，详见 §12 |

---

## §1 审查概述

本报告对技能 `114-site-architecture` 进行 SKILL-SPEC v1.0 全量合规审查与质量评估。审查覆盖目录下全部 4 个文件：`SKILL.md`（279 行，顶层规范化版）、`site-architecture/SKILL.md`（288 行，**嵌套残留版**）、`SCORING.yaml`（155 行）、`check.py`（82 行），合计约 804 行；另对对照集 `complex-skills-no-trigger/114-site-architecture/` 做了结构比对。

审查按五个层面展开：(1) 规范合规——逐条对照 SKILL-SPEC §1–§5 合规清单；(2) 内容质量——逻辑一致性、语法、人机感三个维度（沿用 dossier 的评估框架）；(3) 引用完整性——正文出现的全部文件路径逐一做存在性验证；(4) 评估体系——SCORING.yaml 17 个 criterion 与 check.py 的完整性、可执行性与缺陷；(5) 语料库定位——与 dossier 结论、同批次技能及语料库统计的横向对比。

### 主要发现摘要

- **🚩 嵌套 SKILL.md（必须处理）**：`site-architecture/SKILL.md` 与顶层 `SKILL.md` 共存。diff 验证（忽略行尾空格后）两者正文**逐字一致**——嵌套文件是规范化前的旧版本残留：frontmatter 含 `license`、`metadata`（version/author/category/updated）、`agents` 共 5 个 §1.3 明令禁止的字段；description 含跨技能路由（§2.5 违规）。dossier 状态行声称已完成"14 nested cleanups (2026-08-05)"，但当前语料库仍有 15 个嵌套 SKILL.md（114 为其一），114 的残留未被清理（详见 §2、§3、§12、§13-P0）。
- **合规面**：顶层 frontmatter 仅 `name` + `description` 两键，无违禁字段；description 第三人称、含标准触发短语、WHAT/WHEN/KEYWORDS 齐全；body 279 行（≤600）。三必需节中 **Workflow（三模式）与 Output（Output Artifacts）齐备，Scope/Limitations 缺失**——语料库最常见缺口（~68%），dossier 只记录了 workflow/output 而未标记此缺失。
- **引用面（影响评测）**：正文 4 处文件引用全部悬空——`scripts/sitemap_analyzer.py`（正文第 40、203 行，**且是 SCORING PROC-01 的脚本判定对象**）、`references/url-design-guide.md`（第 104 行）、`references/internal-linking-playbook.md`（第 220 行）。目录中不存在 `scripts/` 与 `references/` 任何文件。Mode 1 第一步"Run `scripts/sitemap_analyzer.py`"按字面无法执行，评测中 PROC-01 将确定性失败（详见 §8、§10）。
- **内容面**：三模式（审计/规划/内链策略）工作流与 6 个知识小节（URL 原则、导航、Silo、内链、常见错误、主动触发）高度自洽，交叉引用一致；`Communication` 节的"结论先行 / What+Why+How / 带 owner 与 deadline 的行动 / 置信度标记"直接支撑 SCORING 的 OUT-01、OUT-03、QA-01 三个判定项，是"评估体系与技能正文互相咬合"的良好案例。
- **事实性小瑕疵**：Common Architecture Mistakes 表末行"Dynamic URLs … Canonicalize or block with robots.txt"——robots.txt 只控制爬取、不解决重复内容，且 Google 明确不建议用 robots.txt 做 noindex；正确做法是 canonical 或 GSC URL 参数处理（详见 §5）。
- **评估设计弱点**：PROC-01 正则锁定字面文件名 `sitemap_analyzer\.py`，正文又提供了"粘贴 sitemap 内容"的兜底路径——按兜底路径执行的 agent 必然不匹配正则，判定设计把"合理的降级行为"判为失败；TEC-03（301 映射）在正文中只有错误表和交付物行两处隐含支持，无 workflow 级指令，映射偏弱（详见 §10）。

§13 给出完整的问题分级清单（P0–P3）、每个问题的具体改法与修复后合规自检表。本报告仅产出 REVIEW.md，未修改任何技能文件。

---

## §2 文件清单与结构

### 2.1 目录结构

```
114-site-architecture/
├── SKILL.md                     ← 顶层技能主文件（279 行，规范化版）
├── site-architecture/
│   └── SKILL.md                 ← 🚩 嵌套 SKILL.md（288 行，规范化前残留版）
├── SCORING.yaml                 ← 评估标准（155 行）
└── check.py                     ← 脚本检查器（82 行）
```

目录中**不存在** `scripts/`、`references/`、`resources/` 任何子目录——但正文引用了这 3 个路径下的 4 个文件（详见 §8）。

### 2.2 文件角色一览

| 文件 | 行数 | 角色 | 质量印象 |
|------|-----:|------|---------|
| `SKILL.md` | 279 | 技能主文件：Before You Begin / How This Skill Works（3 模式）/ URL 原则 / 导航设计 / Silo 结构 / 内链策略 / 常见错误 / 主动触发 / Output Artifacts / Communication / Related Skills | 内容扎实、结构清晰；缺 Scope 节 |
| `site-architecture/SKILL.md` | 288 | **嵌套残留**：正文与顶层逐字一致（仅行尾空格差异），frontmatter 含 5 个违禁字段 | 应删除或归档（P0） |
| `SCORING.yaml` | 155 | 评估标准：17 个 criterion（3 scope + 4 process + 4 technical + 3 output + 2 negative + 1 qa）+ 2 个 critical failures | 与 SKILL.md 映射总体良好，1 处判定对象缺失（PROC-01） |
| `check.py` | 82 | 脚本检查：实现 PROC-01（全 skill 唯一 script 判定项） | 简洁正确，存在评估风险（见 §10） |

### 2.3 嵌套 SKILL.md 标记（本报告首要发现）

`site-architecture/SKILL.md` 与顶层文件并存构成嵌套结构，具体事实如下：

1. **正文完全重复**：`diff -w <(tail -n +14 site-architecture/SKILL.md) <(tail -n +6 SKILL.md)` 输出为空（忽略行尾空格后逐字节一致，275 行正文完全相同）。嵌套文件是规范化流程之前的旧版本，顶层文件即其规范化产物。
2. **违禁 frontmatter**：嵌套文件含 `license: MIT`、`metadata:`（`version: 1.0.0`、`author: Ric Neves - Flowgrammers`、`category: marketing`、`updated: 2026-03-06`）、`agents: [claude-code]`——§1.3 明确列名的 `license`、`version`、`category`、`agents`、`metadata` 全部命中，共 5 处违规（详见 §3.4）。
3. **description 违规**：嵌套文件 description 以 WHEN 从句开头（无 WHAT 前置）、含跨技能路由 "NOT for content strategy decisions … (use content-strategy) or for schema markup (use schema-markup)"（违反 §2.5），长度约 700 字符虽在 ≤1024 内但结构不符合 §2.2 模板。
4. **残留波及对照集**：`complex-skills-no-trigger/114-site-architecture/site-architecture/SKILL.md` 同样存在，删除时须同步（见 §13-P0）。
5. **语料库范围**：主集当前仍有 15 个嵌套 SKILL.md（12 个位于 `NNN-name/name/` 直接子目录，3 个位于 `311-legacy-to-ai-ready/assets/` 下），114 是 12 个直接子目录型之一——嵌套问题非 114 独有，但 dossier 的"14 nested cleanups 已完成"状态声明与现状不符，114 的残留应视作清理遗漏（详见 §12）。

---

## §3 Frontmatter 与 Description 合规（SKILL-SPEC §1–§2）

### 3.1 name 字段（顶层）

`name: site-architecture`，小写、连字符合法、≤64 字符。与目录名 `114-site-architecture` 的关系：spec 字面要求"name MUST match directory name"，但语料库既有惯例是目录带 `NNN-` 前缀而 name 不带（已验证 112-postmortem → `postmortem`、113-prioritization-effort-impact → `prioritization-effort-impact` 等）。114 遵循语料库惯例，dossier 从未将此类前缀差异计为违规；此处仅记录 spec 字面与 corpus 惯例的已知张力，不判违规。

### 3.2 违禁字段（顶层）

顶层 frontmatter 仅有 `name` 与 `description` 两个键，全部在允许列表内，无 §1.3 列出的任何违禁字段（无 version / metadata / tags / trigger / license / agents 等）。**通过。**

### 3.3 description 结构（顶层，§2.1–§2.4）

```
Audit, redesign, and plan website structure, URL hierarchy, navigation design,
and internal linking. Use when the user wants to improve site architecture for
SEO, user experience, or content discoverability.
```

| §2 要求 | 判定 | 说明 |
|---------|:----:|------|
| WHAT（具体做什么） | ✅ | "Audit, redesign, and plan website structure, URL hierarchy, navigation design, and internal linking"——具体且列举了 5 个领域动词 |
| WHEN（触发场景） | ✅ | "Use when the user wants to improve site architecture for SEO, user experience, or content discoverability" |
| KEYWORDS | ✅ | 隐含 site architecture / URL hierarchy / navigation / internal linking / SEO / UX / discoverability |
| 第三人称（§2.3） | ✅ | 无 imperative / 第一人称 / 第二人称开头 |
| 触发信号短语（§2.4） | ✅ | "Use when the user wants to…" 命中枚举短语 |
| 无跨技能路由（§2.5） | ✅ | description 内无 "NOT for X, use Y" |
| 长度 ≤1024 字符 | ✅ | 约 220 字符，远低于上限 |
| ≥40 字符（§2.5） | ✅ | 达标 |

顶层 description 是**规范的 §2.2 模板示范**：WHAT 在前、WHEN 在后、无路由、无语气违规。

### 3.4 嵌套文件 frontmatter 与 description（🚩 违规模板样例）

`site-architecture/SKILL.md` 的 frontmatter 是规范化前旧形态，逐项违规如下：

| 字段 | 值 | §1.3 判定 |
|------|-----|:---------:|
| `name: "site-architecture"` | 带引号标量（合法但非常规） | 合规 |
| `license: MIT` | — | ❌ 违禁字段 |
| `metadata: {version, author, category, updated}` | 1.0.0 / Ric Neves - Flowgrammers / marketing / 2026-03-06 | ❌ 违禁字段（且内嵌 version / category 两个单独违禁键） |
| `agents: [claude-code]` | — | ❌ 违禁字段 |

description 违规点：**(a)** 以 "When the user wants to…" WHEN 从句开头，无 WHAT 前置，不符合 §2.2 模板顺序；**(b)** 中段 "NOT for content strategy decisions about what to write (use content-strategy) or for schema markup (use schema-markup)" 是 §2.5 明令禁止的 description 内跨技能路由（这类路由按 spec 应放正文 Scope 节）；**(c)** 关键词列举（9 个短语）偏堆砌，但仍在可接受范围。触发短语 "Use when the user mentions…" 合法。

该文件的非合规内容全部保留在旧的嵌套副本中，顶层已规范化——**处理方式应是删除/归档嵌套副本而非修改它**（见 §13-P0）。

---

## §4 Body 结构合规（SKILL-SPEC §3）

### 4.1 三必需节核查

| 必需节 | 顶层正文对应 | 判定 |
|--------|--------------|:----:|
| **Workflow / Process** | `## How This Skill Works`（Mode 1 审计 / Mode 2 规划 / Mode 3 内链，各 5 步） | ✅ 齐备 |
| **Output Format** | `## Output Artifacts`（5 种请求 → 交付物映射表） | ✅ 齐备 |
| **Scope / Limitations** | **无任何独立节**；`Common Architecture Mistakes` 是知识表而非范围声明；`Related Skills` 内含路由但非 Scope 语义 | ❌ **缺失** |

Scope 缺失是 §3.1 的硬性要求（MUST），也是语料库最普遍的缺口（dossier 统计 ~220 个，~68%）。对 114 而言还带来一个次生影响：正文唯一一处跨技能路由（"NOT for deep structural redesign — use site-architecture"，见 Related Skills 第一条）因此无处安放，§2.5 的合规性也连带受损。§13-P1 给出补写方案。

### 4.2 行数

body 274 行（总 279 行减 5 行 frontmatter），远低于 600 行硬上限；对照 §3.2 模式基准，"tool" 型目标约 300 行，114 正好落在 tool 模式量级，体量控制合理。

### 4.3 文件引用规则（§3.3）

- 引用形式全部为相对路径风格（`scripts/…`、`references/…`），无跨技能路径（无 `../other-skill/`），形式上符合 §3.3——**但 4 处引用目标全部不存在**（详见 §8），属于"形式合规、内容悬空"。
- 跨技能引用均以散文名引用（`seo-audit`、`schema-markup`、`content-strategy`、`programmatic-seo`），符合 §3.3"用名称而非路径引用"。
- `marketing-context.md`（"Before You Begin" 条件读取）未指定路径前缀，按惯例应为 workspace 根目录，属条件可选文件，不算悬空引用，但建议显式注明（§13-P3）。

### 4.4 内容指南（§3.4）

- **知识增量**：正文 6 个知识小节（URL 深度/构造、导航分区、hub-and-spoke、锚文本、错误表、主动触发）均为领域高增量内容，非通用建议复述，符合 §3.4。
- **反模式优先**：`Common Architecture Mistakes` 表 9 行全部带"为什么有害 + 修法"，符合"NEVER 规则带理由"要求。
- **决策表优先**：Flat vs Layered、Do/Don't、Navigation Zones、Anchor Text、Mistakes 共 5 张决策表，分支信息全部表化，符合 §3.4。
- **具体优先**：URL 示例（`/how-to-write-cold-emails` vs `/how_to_write_cold_emails`）真实可执行。

### 4.5 合规清单速览

`name` ✅ / description 第三人称+触发 ✅ / 无违禁键 ✅ / body ≤600 ✅ / workflow ✅ / output ✅ / **scope ❌** / 无跨技能文件路径 ✅ / 目录命名 ✅。**12 项中 11 项通过，1 项（scope）未通过**——这正是 §13 中 P1-1 的修复对象。

---

## §5 逻辑一致性分析

### 5.1 三模式与交付物的闭环

- Mode 1（审计）5 步：跑 sitemap 分析 → 深度/URL 模式/孤儿/重复路径审查 → 导航评估 → 按 SEO 影响排序 → 交付优先级审计。与 Output Artifacts 第 1 行"Structural scorecard…+ prioritized fix list"一一对应。
- Mode 2（规划）5 步：目标映射 → URL 层级设计 → 内容 silo → 导航分区 → 交付文本站点树 + URL 规格表。与第 2 行对应，且与 URL Structure Principles、Navigation Design、Silo 三个知识节互相引用。
- Mode 3（内链）5 步：hub 识别 → spoke 映射 → 孤儿查找 → 锚文本审查 → 交付内链计划。与第 3 行、Internal Linking Strategy 节对应。
- 第 4、5 行（URL redesign / Silo strategy）是 Mode 2/3 的衍生交付，逻辑上衔接无矛盾。

### 5.2 知识小节内部一致性（交叉核对无矛盾）

- URL 深度表（Flat ≤3 层、4+ 层 ❌）↔ PROC-02 判定口径一致；NEG-01 口径一致。
- 锚文本规则表（exact/partial/branded/generic/naked 五档）↔ TEC-04 判定口径一致。
- Silo 链接规则（hub→spokes、spokes→hub、deep→spoke+hub、跨 silo 允许）↔ PROC-04 判定口径一致，且与"Linking Priority Stack"排序（in-content > hub > nav > footer > sidebar）无冲突。
- 孤儿页查找（GSC/Screaming Frog 导出做集合差 + 脚本兜底）↔ TEC-02 判定口径一致；两条路径内部一致。
- 主动触发 6 条全部源自前面知识节的推论（3 点击即风险 ↔ 深度表；浅层 hub ↔ Silo 节；无面包屑 ↔ Navigation 节；noindex 进 sitemap ↔ 常识性 SEO 规则），无自相矛盾。
- 3 点击表述："Pages more than 3 clicks from the homepage → flag"与"click 4+ times to reach needs a shortcut"——"多于 3 次点击"即"第 4 次点击"，两处口径自洽，无数字冲突。

### 5.3 轻微事实性问题（非逻辑矛盾）

1. **Mistakes 表末行**："Dynamic URLs with parameters … Canonicalize or block with robots.txt"。两个技术瑕疵：(a) robots.txt 控制的是**爬取**而非索引，对"重复内容"（duplicate content）无效——参数页若已被收录，robots.txt 不阻止其出现在索引中；(b) Google 官方明确不建议用 robots.txt 阻止 noindex（无内容页面场景），正确修法是 canonical 或 Google Search Console 的 URL 参数处理，必要时 noindex meta。该行"Canonicalize"前半句正确，后半句"block with robots.txt"技术表述不准确。影响面：仅一处知识表措辞，不影响 SCORING 判定（NEG-01 判定的是推荐 URL 形态，不受此影响）。
2. **"The keyword in the URL is a minor signal"**：表述与主流 SEO 共识一致，无问题。
3. **Sitemap 分析脚本缺失**（Mode 1 第 1 步、孤儿查找第 4 步）——严格说属"步骤引用的工具不存在"，归入 §8 引用完整性处理，不在此列为逻辑缺陷。

### 5.4 逻辑一致性总评

正文内部无步骤矛盾、无数字冲突、无模式间口径漂移，三模式 × 五交付物 × 六知识节形成闭合的知识—执行体系。除 robots.txt 一处措辞瑕疵外，逻辑层质量在语料库 tool 型技能中属上游水平。

---

## §6 语法与可读性

- **拼写与错字**：全文未发现拼写错误、错别字或断句问题。术语（equity、pillar、spoke、orphan、silo）全篇统一。
- **标点与格式**：标题层级规整（H1 → H2 → H3），5 张表格列对齐一致，分隔线分隔节结构整齐；反引号包裹的 URL 示例格式统一。全文无 em 破折号滥用——按语料库惯例（015-outreach-specialist 曾出现 em 破折号与自身规则冲突的先例）核查，此处未发现问题。
- **重复与冗余**：正文无整段重复。唯一可挑剔处是"Flat vs Layered"与"Do/Don't"两张表在"避免 4+ 层/动态参数"上概念重叠，但角度不同（深度策略 vs 构造规则），不算冗余。
- **行尾空格**：顶层文件干净；嵌套文件 `site-architecture/SKILL.md` 几乎每行带行尾空格（diff 时全文件行级差异均源于此），进一步佐证其为规范化前旧版本。
- **可读性**：长段落少、表格为主（约 45% 行数为表格），扫描性好；每节以一句"原则性论断"开头（如"Navigation serves two masters"），符合参考型工具技能的阅读体验。

---

## §7 人机感

- **语气**：自信的领域专家口吻（"You are a specialist in site information architecture and technical SEO structure"），是语料库中 tool 型技能的常见 persona 框架，与技能定位匹配；全文无 chatbot 式寒暄、无过度口号。
- **emoji 使用**：仅两处——置信度标记（🟢/🟡/🔴，Communication 节，功能性）与表格内的 ✅/❌（URL 示例与深度表，功能性）。无装饰性 emoji 堆砌（对比 072-mobile-design 的 20+ emoji 先例，本技能克制）。
- **人机协作边界**：Before You Begin 先收集 current state / goals / constraints 再动手（支撑 SCOPE-03）；"If `marketing-context.md` exists, read it before asking questions" 体现上下文优先；主动触发节"Surface these without being asked"把建议行为显式化，不给 agent 留"可选做不做"的模糊空间；Communication 节"Actions have owners and deadlines — no 'we should consider'"直接把交付标准写进行为规则。
- **可接受性**：persona 化开场与结论先行的沟通模式在 tool 型技能中属行业惯例，非越界；整体人机感与 112-postmortem 同批次水平，属"专业、不机械、不油滑"的中上档。

---

## §8 文件引用与资源完整性（含悬空引用清单）

### 8.1 正文全部文件引用逐一验证

| # | 引用（正文行号） | 路径形式 | 目标是否存在 | 判定 |
|---|------------------|----------|:----------:|:----:|
| 1 | 第 40 行：`Run `scripts/sitemap_analyzer.py`` | `scripts/` 相对路径 | ❌ 目录不存在 | **悬空** |
| 2 | 第 104 行：`See `references/url-design-guide.md`` | `references/` 相对路径 | ❌ 目录不存在 | **悬空** |
| 3 | 第 203 行：`run `scripts/sitemap_analyzer.py`` | `scripts/` 相对路径 | ❌ 目录不存在 | **悬空** |
| 4 | 第 220 行：`See `references/internal-linking-playbook.md`` | `references/` 相对路径 | ❌ 目录不存在 | **悬空** |
| 5 | 第 12 行：`marketing-context.md` | 裸文件名（条件读取） | 条件可选（workspace 提供） | 非悬空，建议注明位置 |

### 8.2 悬空引用的影响分析

- **对技能可执行性**：Mode 1 第 1 步"Run `scripts/sitemap_analyzer.py`"是审计模式的**第一步**。脚本缺失时 agent 只能走括号内兜底"or paste the sitemap content"（手动/自写解析），工作流仍可完成，但技能承诺的工具化能力（深度分布、孤儿候选标记）无法兑现。孤儿查找第 4 步同样依赖该脚本。
- **对评测（最严重）**：SCORING.yaml 的 PROC-01 是脚本判定项 `tool_log_contains('sitemap_analyzer\.py')`，即**要求工具日志中出现对该脚本的调用**。脚本不存在 → agent 无法真实调用 → 唯一匹配方式是 agent 自行伪造调用记录（诱导虚构）或评测方在 workspace 预置该脚本。两种情况都不是正常评测应有的状态（详见 §10-A）。
- **对参考文件**：`references/url-design-guide.md`（博客/SaaS/电商/本地四种站点类型模式）与 `references/internal-linking-playbook.md`（模式与脚本）是正文承诺的深度材料，缺失使"See references/…"成为死链接。由于正文自身已自足（279 行内容覆盖引用点声称的主题），删除引用行或补文件皆可（见 §13-P2）。

### 8.3 语料库横向背景

dossier 统计"引用文件/脚本缺失"类问题影响约 15 个 skills；114 的 4 处悬空引用属该已知问题族。但 114 的特殊性在于：**悬空引用中有一个是评测判定项的直接对象**（PROC-01 → 脚本），把"内容瑕疵"升级为"评测基础设施缺口"，处置优先级应高于同类技能（P1）。

---

## §9 评估体系审查（SCORING.yaml）

### 9.1 结构总览

- `pattern: tool`，`total_items: 17`——与 criteria 列表实际数量一致（3+4+4+3+2+1 = 17）✅。
- 分布：scope 3 / process 4 / technical 4 / output 3 / negative 2 / qa 1；script 判定 1 项（PROC-01），其余 16 项 LLM 判定。
- critical_failures 2 项：CF-01（无任何上下文收集即交付 → cap_to_0）、CF-02（推荐无 301 映射的 URL 变更 → cap_to_0）。两条都是"可客观判断的硬错误"，设计合理。
- 判定 prompt 全部为"question + evidence"结构，符合 CHECKER-LIBRARY 的 LLM judge 规范。

### 9.2 SCORING ↔ SKILL.md 逐项映射

| Criterion | 判定方式 | 正文支撑点 | 映射强度 |
|-----------|:-------:|-----------|:-------:|
| SCOPE-01 任务属站点架构域 | llm | description + 三模式标题 | 强 |
| SCOPE-02 正确选择模式 | llm | 三模式各 5 步，入口清晰 | 强 |
| SCOPE-03 先收集上下文 | llm | Before You Begin（current state/goals/constraints + marketing-context.md） | 强 |
| PROC-01 调用 sitemap_analyzer.py | **script** | Mode 1 第 1 步（**脚本缺失**） | **弱（对象缺失）** |
| PROC-02 URL 深度扁平 ≤3 层 | llm | Flat vs Layered 表 + "Rule of thumb" | 强 |
| PROC-03 导航分区规划 | llm | Navigation Zones 表 + 主导航 ≤5-8 条规则 | 强 |
| PROC-04 hub-and-spoke 链接规则 | llm | Silo 节 5 条链接规则 | 强 |
| TEC-01 URL 构造规则 | llm | Do/Don't 表（连字符/无冗余后缀/无动态参数/无关键词堆砌） | 强 |
| TEC-02 孤儿页识别 | llm | 孤儿查找 4 步 + 修复 3 步 | 强 |
| TEC-03 URL 变更配 301 映射 | llm | 仅 Mistakes 表"Always 301 redirect"行 + Output Artifacts"URL redesign"行 | **偏弱** |
| TEC-04 锚文本指导 | llm | Anchor Text Rules 表（禁 generic/naked） | 强 |
| OUT-01 优先级修复清单带 owner/deadline | llm | Communication"Actions have owners and deadlines" | 中强 |
| OUT-02 文本站点树/URL 规格表 | llm | Output Artifacts 第 2 行 | 强 |
| OUT-03 置信度标记 | llm | Communication"Confidence marking" | 强 |
| NEG-01 不推荐关键词堆砌/4+ 层 URL | llm | Keywords in URLs + 深度表 | 强 |
| NEG-02 不建议全站 footer 链 | llm | Mistakes 表 footer 行 + Navigation"use carefully" | 强 |
| QA-01 结论先行 + What+Why+How | llm | Communication 前两条 | 强 |

### 9.3 正面评价

- 17 项中 15 项在正文有直接且充分的支撑，映射强度为语料库上游水平。
- 2 条 critical_failures 与技能的设计意图（先问再答、禁止断链式改动）精确对应，权重设置（cap_to_0）合理。
- 判定口径与知识表一一对应（如 NEG-01 ↔ 深度表、NEG-02 ↔ footer 行），LLM judge 有明确的"参考答案"可查。

---

## §10 评估体系缺陷与风险

**A. PROC-01 的判定对象缺失（高风险，P1）**

`tool_log_contains('sitemap_analyzer\.py')` 锁定字面文件名，而该脚本在技能目录中不存在。由此产生三条失败路径：agent 按正文执行（找不到脚本 → 走"粘贴 sitemap"兜底）→ 工具日志无该字符串 → **确定性失败**；agent 为满足指令自行编写同名脚本（合理但超出技能交付范围）→ 行为不可复现；agent 伪造调用 → 评测污染。无论哪条路径，PROC-01 在当前状态下测的不是"遵从技能"而是"是否存在同名文件"。**修复选项**（详见 §13-P1-2）：(a) 在技能目录补齐 `scripts/sitemap_analyzer.py` 并把正则放宽为 `sitemap|sitemap.*analy`；(b) 将 PROC-01 改为 LLM 判定"是否对 sitemap 内容做了结构化分析（含兜底路径）"；(c) 保留脚本判定但改为 `tool_log_contains('sitemap')` 语义变体。推荐 (a)，保持"工具调用"这一可验证行为。

**B. TEC-03 映射偏弱（中风险，P2）**

301 映射在正文中仅以错误表一行（"Always 301 redirect old URLs to new ones"）和交付物表一行（"Before/after URL table + 301 redirect mapping"）存在，无 workflow 步骤级指令。Mode 2/3 的步骤列表（各 5 步）均未提及"为每条 URL 变更产出 old→new 映射"。LLM judge 判定 TEC-03 时可能因"正文未将其设为流程组成部分"而得到不一致结果——部分 agent 从交付物表推断出该行为，部分不推断。建议在 Mode 2 增加一步或在 URL Structure 节加一句显式指令。

**C. SCOPE-03 的 marketing-context.md 位置未定义（低风险，P3）**

判定问句引用 "marketing-context.md if present"，但正文未说明该文件应位于 workspace 根目录还是技能目录。不同 agent 会去不同位置查找，导致判定噪声。建议正文补注"（workspace 根目录）"。

**D. OUT-01 的 owner/deadline 判定依赖单句（低风险）**

正文支撑仅 Communication 一节一句，无模板示范（如"每个行动项含 Owner: X / Due: Y"的具体样例）。LLM judge 面对"无 owner/deadline 但其余完整"的输出时，判定标准模糊。建议在 Output Artifacts 或 Communication 节给一行行动项模板。

**E. 无 format 类检查项（可接受，不作缺陷）**

语料库全局有 format 类检查 279 项，但本 skill 0 项（输出是自由文本建议而非结构化文件），合理，不判问题。

**F. 检查项覆盖密度（可接受）**

17 项/技能与语料库平均（10–22 项）匹配；1 个脚本判定在 tool 型技能中偏少但合法（判定内容本身主要由 LLM 承担）。

---

## §11 check.py 实现审查

- **实现范围**：仅实现 PROC-01 一个脚本判定（`tool_log_contains('sitemap_analyzer\.py')`），与 SCORING.yaml 中唯一 script 项一一对应，其余 16 项按注释明确标注"llm judge (not checked here)"——**与 SCORING 无口径漂移，无漏项/多出项**。
- **正确性**：正则写法正确（转义 `.`）；`tool_log_contains` 对 JSONL 每行做匹配，与 CHECKER-LIBRARY 定义一致；返回 `{id: bool}` 结构符合 runner 约定。
- **健壮性**：`agent_output` 参数用 `os.path.exists` 判路径/内容，包 OSError/ValueError——对超长字符串的 `os.path.exists` 可能抛错的情形有防御；`set_agent_output` 仅在非路径时调用，避免与 main() 的读文件逻辑重复调用。逻辑无缺陷。
- **小问题**：(1) `workspace` 参数接收后未使用（无害，保持签名一致即可）；(2) `set_agent_output` 导入后实际仅条件调用，import 行无冗余问题；(3) **与 §10-A 相同的风险**：check.py 本身实现无误，但 PROC-01 的判定对象（脚本文件）缺失，检查器会稳定输出 `PROC-01: false`——修复应落在 SCORING/脚本补全层面，check.py 无需改动（若采用 §13 选项 b 改为 LLM 判定，则需同步删除 check.py 中该项）。
- **总评**：实现质量良好（对照 112-postmortem 的 check.py 同样为简洁风格），风险不在代码而在其依赖的文件。

---

## §12 与 Dossier 及语料库对比

### 12.1 dossier 条目原文（Batch 101-125）

> "112 目的/workflow/RCA/护栏一致；113 2x2 矩阵与红标启发式一致；114 三模式加规则连贯。…合规: 112 全部三节齐全；113/114 workflow/output 齐备。总评: 🟢 三个均为强 skill。"

### 12.2 一致点

- 内容面完全一致：三模式（审计/规划/内链）加规则体系的连贯性，本报告 §5 结论与 dossier 相同。
- "workflow/output 齐备"成立：§4.1 确认两者存在且质量高。
- 总体"强 skill"判断在内容层面成立，本报告不推翻。

### 12.3 差异点（dossier 未覆盖，本报告补充）

| # | dossier 状态 | 本报告发现 | 意义 |
|---|--------------|-----------|------|
| 1 | 未标记 114 缺 Scope 节（条目只记"workflow/output 齐备"） | §4.1：Scope/Limitations 必需节缺失 | 114 属语料库 ~68% 缺 Scope 群体，dossier 的批次摘要口径漏记 |
| 2 | 未标记文件引用缺失 | §8：4 处引用全部悬空，含 PROC-01 判定对象 | 内容问题升级为评测基础设施问题 |
| 3 | 状态行声称"14 nested cleanups (2026-08-05)"已完成 | §2.3：主集仍有 15 个嵌套 SKILL.md，114 为直接子目录型之一 | 清理声明与现状不符，或清理未覆盖这些目录 |
| 4 | 批次条目未区分顶层/嵌套文件 | diff 验证嵌套正文与顶层逐字一致 | 114 的嵌套是"旧版本残留"而非"独立技能" |

### 12.4 语料库定位

- 与同批次（112-114）：112 三节齐全，114 缺 Scope——同为"强内容"但合规完成度不同；114 的修复路径清晰（补节 + 删嵌套 + 补/改引用），比 113、114 之外本批次的 115-116（编号断裂）更接近 🟢。
- 与 tool 型技能（61 个）：114 体量（279 行）、决策表密度、三模式结构均属 tool 型中上游；其缺 Scope 是 tool 型典型问题（dossier 表：tool 型平均 🟡，常见缺 output/scope）。
- 与"引用缺失"问题族（~15 个）：114 是其中唯一（就本报告核查范围而言）引用缺失直接命中 SCORING 脚本判定项的案例。
- 与嵌套问题族（15 个残留）：114 属同族，但其余 14 个不在本次审查范围，不逐一断言其性质。

---

## §13 综合评估与改进建议（问题分级清单）

### 13.1 分级总表

| 优先级 | 编号 | 问题 | 影响面 | 处置动作 |
|:------:|:----:|------|--------|---------|
| **P0** | N-01 | 嵌套 `site-architecture/SKILL.md` 残留（正文与顶层重复，frontmatter 5 处违禁字段） | 合规 / 评测 / 语料库整洁度 | 删除或归档（13.2） |
| **P1** | S-01 | 缺 Scope/Limitations 必需节（§3.1 硬性要求） | 合规（12 项清单中唯一未通过项） | 补节（13.3） |
| **P1** | R-01 | `scripts/sitemap_analyzer.py` 缺失 → PROC-01 确定性失败 | 评测有效性 | 补脚本或改判定（13.4） |
| **P2** | R-02 | `references/url-design-guide.md`、`references/internal-linking-playbook.md` 缺失 | 引用完整性 | 补文件或删引用行（13.5） |
| **P2** | L-01 | Mistakes 表"block with robots.txt"措辞不准确 | 知识准确性（低） | 改措辞（13.6） |
| **P2** | L-02 | TEC-03 正文映射偏弱（301 映射无 workflow 级指令） | 评测判定一致性 | 加显式步骤（13.6） |
| **P3** | L-03 | `marketing-context.md` 位置未注明 | 判定噪声（低） | 补路径说明（13.6） |
| **P3** | L-04 | OUT-01 缺行动项模板示例 | 判定标准模糊（低） | 加一行模板（13.6） |
| **P3** | N-02 | 嵌套残留波及对照集（no-trigger 副本） | 语料库同步 | 随 N-01 同步删除（13.2） |

### 13.2 N-01：删除嵌套 SKILL.md（P0，唯一必须动刀项）

**理由**：(a) 正文与顶层逐字重复，无独立信息价值；(b) frontmatter 含 `license` / `metadata` / `agents` 等 5 处 §1.3 违禁键，若被任何工具按文件名递归发现（`find -name SKILL.md` 类扫描、harness 的递归加载），将引入"非规范化文件"进评测管线的风险；(c) dossier 声称嵌套清理已完成，此残留属遗漏，应归位。

**具体操作**：
1. 删除 `D:\SkillIF\skill-experiment\complex-skills\114-site-architecture\site-architecture\` 整个目录。
2. 同步删除 `D:\SkillIF\skill-experiment\complex-skills-no-trigger\114-site-architecture\site-architecture\`。
3. 若项目有历史归档需求，可将旧版移至 `_shared/archive/` 或 skill 内 `references/legacy/`（归档则需同步改顶层"See references"行的目录语义——**建议直接删除，归档价值为零**，因为正文 100% 重复）。
4. 复核语料库其余 14 个嵌套 SKILL.md 是否应纳入同批清理（超出本 skill 范围，仅提示）。

**验收**：`find complex-skills -name SKILL.md` 下 114 目录只剩顶层 1 个；`grep -c "^name:" site-architecture/SKILL.md` 报文件不存在。

### 13.3 S-01：补 Scope/Limitations 节（P1）

在 `## How This Skill Works` 之前或 `## Common Architecture Mistakes` 之后插入独立节（建议置于 `Common Architecture Mistakes` 之后、`Proactive Triggers` 之前，逻辑流为"错误清单 → 边界 → 触发"）。**建议文本（可直接采用）**：

```markdown
## Scope & Limitations

**What this skill DOES:**
- Site structure, URL hierarchy, navigation design, internal linking, and content silo architecture
- Audits, redesigns, and structural planning for new and existing sites

**What this skill does NOT do:**
- NOT keyword research or content strategy — decide WHAT to create with
  `content-strategy`, then use this skill to decide WHERE it lives
- NOT on-page copywriting, meta-tag writing, or content production
- NOT schema markup implementation — use `schema-markup` after the structure is set
- NOT a full SEO audit — use `seo-audit` when architecture is one of several problem areas
- NOT a crawling/indexing debugger (robots.txt, log analysis) — structural decisions only
- NOT a CMS migration tool — it designs the target structure and redirect map, it does not
  implement the migration

**When NOT to use:**
- When the user only needs content recommendations without structural changes
- When the site is a single-page/landing-page with no hierarchy to design
- When the request is about individual page on-page SEO, not the site's overall structure

**Hard limits:**
- All URL-change recommendations MUST include a 301 redirect map (old → new)
- Never recommend keyword-stuffed URLs or 4+ level nesting (see URL Structure Principles)
- No site-wide footer links to every post (see Common Architecture Mistakes)
```

该节同时解决三个问题：满足 §3.1 必需节；把 Related Skills 中的"NOT for …"路由迁入正确位置（§2.5 合规）；把 TEC-03 的 301 映射要求显式化（缓解 §10-B）。**若采用本节，"Hard limits"三行与 SCORING 的 TEC-03 / NEG-01 / NEG-02 判定口径完全对齐。**

### 13.4 R-01：补脚本或改判定（P1，二选一）

**选项 A（推荐）——补齐脚本**：新增 `scripts/sitemap_analyzer.py`（XML sitemap 解析：URL 列表、深度分布、重复路径标记、孤儿候选启发式；CLI 接受 sitemap 文件路径或粘贴内容；输出结构化文本）。正文第 40 行兜底"or paste the sitemap content"可保留（脚本应同样接受 stdin）。同时将 SCORING PROC-01 正则放宽为 `sitemap`（覆盖脚本调用与"分析 sitemap 内容"两种行为），或保持 `sitemap_analyzer\.py` 不动（脚本补全后即可真实命中）。check.py 无需改动。
**选项 B——改判定**：PROC-01 改为 LLM judge，question 改为"Did the agent perform a structured analysis of the sitemap (depth distribution, URL patterns, orphan candidates) — via the provided script or equivalent analysis?"，同步从 check.py 删除该项。代价：失去一个可验证的机械检查点。
**不建议**：保留脚本判定 + 不补脚本（现状）——PROC-01 将稳定判负或诱导虚构。

### 13.5 R-02：补 references 或删引用行（P2）

正文两处 "See `references/…`" 指向不存在文件。二选一：
- **最小成本（推荐）**：删除第 104 行 "See `references/url-design-guide.md` for patterns by site type" 与第 220 行 "See `references/internal-linking-playbook.md` for patterns and scripts."——正文已自足覆盖这些主题，删除不损失内容，直接消除死链接。
- **增值**：若保留引用，补两份文件（url-design-guide.md：博客/SaaS/电商/本地四类站点 URL 模式表；internal-linking-playbook.md：hub 发现启发式、锚文本批量改写示例）。体量各 ~50-80 行即可，属锦上添花。
- **验收**：`grep -n "references/" SKILL.md` 结果对应的文件全部 `ls` 可查。

### 13.6 低优先级措辞与一致性修复（P2–P3）

- **L-01（P2）**：Mistakes 表末行 Fix 改为"Consolidate with canonical or use Search Console URL parameter handling — do not rely on robots.txt (it controls crawling, not indexing)"。一行改动，消除技术表述错误。
- **L-02（P2）**：Mode 2 步骤列表插入一步（如步骤 5 前）"Produce a redirect map for every URL change (old → new) when restructuring an existing site"，使 TEC-03 从"交付物行"升级为"流程步骤"。若采用 13.3 的 Scope 节 Hard limits，两处互相印证更佳。
- **L-03（P3）**：第 12 行改为 "If `marketing-context.md` exists **in the workspace root**, read it before asking questions."
- **L-04（P3）**：Communication 节补一行行动项格式示例："Every action item: `Action: <what> | Owner: <person> | Due: <date>`"。

### 13.7 修复后合规自检表（对照 SKILL-SPEC §5 清单）

| 检查项 | 现状 | 修复后 |
|--------|:----:|:------:|
| name 小写+连字符、≤64、匹配目录 | ✅ | ✅ |
| description 第三人称 WHAT+WHEN+KEYWORDS、≤1024 | ✅ | ✅ |
| description 无祈使/一二人称开头 | ✅ | ✅ |
| description 无跨技能路由 | ✅（顶层） | ✅ |
| 至少一个触发信号短语 | ✅ | ✅ |
| frontmatter 无违禁键 | ✅（顶层） | ✅（含删除嵌套后全目录） |
| body ≤600 行 | ✅（274） | ✅ |
| workflow/process 节 | ✅ | ✅ |
| output 节 | ✅ | ✅ |
| **scope/limitations 节** | **❌** | ✅（13.3） |
| 无跨技能文件路径 | ✅ | ✅ |
| 目录命名规范 | ✅ | ✅（嵌套目录删除后） |
| 文件引用均存在 | ❌（4/4 悬空） | ✅（13.4 + 13.5） |
| 评测判定对象可执行 | ❌（PROC-01 脚本缺失） | ✅（13.4） |

### 13.8 最终评级与结论

- **内容质量评级**：🟢——三模式 × 五交付物 × 六知识节闭合自洽，决策表密度与具体性是 tool 型技能上游水平，Communication 节与 SCORING 三个判定项精确咬合是本技能亮点。
- **综合评级**：🟡——P0 嵌套残留（违禁 frontmatter 入评测管线风险）+ P1 缺 Scope 必需节 + P1 评测脚本缺失 3 项叠加，按 dossier 定级标准"可用但有小问题，建议微调"恰如其分；完成 P0/P1 四项动作（13.2 / 13.3 / 13.4 / 13.5）后即回 🟢。
- **与 dossier 的关系**：dossier 的 🟢 在内容维度成立，本报告不推翻，但补充了其批次摘要未覆盖的三个结构性发现（Scope 缺失、悬空引用、嵌套残留）；同时指出 dossier 状态行"14 nested cleanups 已完成"与语料库现状（15 个残留）不符，建议对清理结果做一次全库复核。
- **评测影响提示**：在 R-01 未修复前，任何基于当前 SCORING.yaml 运行的 114 评测，PROC-01 将确定性判负——**建议将 114 的评测排期安排在脚本补全或判定修改之后**。
- **改动范围声明**：本报告仅产出 REVIEW.md，未修改任何技能文件；上述所有改动建议均需另行确认后执行。
