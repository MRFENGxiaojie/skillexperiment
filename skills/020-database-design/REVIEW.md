# REVIEW: 020-database-design

**审查日期**: 2026-08-06 | **审查人**: Claude (SkillIF quality auditor)
**审查范围**: 全目录文件逐一全文读取 —— SKILL.md (52 行)、SCORING.yaml (99 行)、check.py (73 行)、原 REVIEW.md 存根 (10 行)、database-selection.md (45 行)、indexing.md (40 行)、migrations.md (49 行)、optimization.md (38 行)、orm-selection.md (31 行)、schema-design.md (57 行)、scripts/schema_validator.py (173 行)
**对照基准**: D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md v1.0、_shared/CHECKER-LIBRARY.md、_shared/checker.py、memory/skill-dossier.md

---

## 1. Directory Full Inventory

| # | 文件 | 行数 | 类型 | 审查状态 |
|---|------|------|------|---------|
| 1 | `SKILL.md` | 52 行 | 主体 | ✅ 全文读取 |
| 2 | `SCORING.yaml` | 99 行 | 评分标准 | ✅ 全文读取 |
| 3 | `check.py` | 73 行 | 评测脚本 | ✅ 全文读取 |
| 4 | `REVIEW.md` | 10 行 | 审查文件（存根） | ✅ 全文读取，本次重写 |
| 5 | `database-selection.md` | 45 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 6 | `indexing.md` | 40 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 7 | `migrations.md` | 49 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 8 | `optimization.md` | 38 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 9 | `orm-selection.md` | 31 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 10 | `schema-design.md` | 57 行 | 主题文件（技能根目录） | ✅ 全文读取 |
| 11 | `scripts/schema_validator.py` | 173 行 | 脚本 | ✅ 全文读取 |

**子目录检查**:

| 子目录 | 是否存在 | 内容 | 备注 |
|--------|:-------:|------|------|
| `references/` | ❌ | 主题文件散落在技能根目录 | **结构偏离**（见 §3.4） |
| `scripts/` | ✅ | schema_validator.py | **孤儿脚本**（SKILL.md 从未引用，见 §5.5） |
| `assets/` / `docs/` / `examples/` | ❌ | — | — |

**要点**: 本技能是"导航型"（pattern: navigation）技能——SKILL.md 是内容地图 + 清单，实质知识在 6 个主题文件。两个结构性问题：① 主题文件不在 `references/` 而在根目录；② schema_validator.py 存在但无任何引用（包括 SCORING 与 check.py 均未引用）。

---

## 2. Frontmatter Field-by-Field Review

### 2.1 原始 Frontmatter

```yaml
---
name: database-design
description: Database design principles and decision making. Schema design, indexing strategy, ORM selection, serverless databases. Use when the user asks to design a database schema, choose a database or ORM, optimize indexing or queries, or plan migrations.
allowed-tools: Read, Write, Edit, Glob, Grep
---
```

### 2.2 `name` 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 小写 + 连字符 | ✅ | `database-design` |
| ≤64 字符 | ✅ | 15 字符 |
| 与目录名匹配 | ✅ | `020-database-design` |

### 2.3 `description` 字段逐句分析

**句子 1**: "Database design principles and decision making."

- WHAT 部分。声明技能提供数据库设计原则与决策框架。抽象但准确（导航型技能的 WHAT 是"知识域导航"）。

**句子 2**: "Schema design, indexing strategy, ORM selection, serverless databases."

- 知识域枚举。4 个主题与内容地图 6 文件的关系：
  - schema design ↔ `schema-design.md` ✅
  - indexing strategy ↔ `indexing.md` + `optimization.md`（部分） ✅
  - ORM selection ↔ `orm-selection.md` ✅
  - serverless databases ↔ `database-selection.md` + `migrations.md`（Neon/Turso 节） ✅
  - 未枚举的：database selection（主体）、query optimization、migrations——description 未覆盖全部 6 个主题，但覆盖面已足够触发（详见句子 3）。

**句子 3**: "Use when the user asks to design a database schema, choose a database or ORM, optimize indexing or queries, or plan migrations."

- WHEN 部分。4 个触发场景：设计 schema、选择数据库/ORM、优化索引/查询、规划迁移。
- 触发信号检查（规范 §2.4）：**"Use when the user asks to..." 为规范五个形式中的第二个，字面完全匹配** ✅（与 018 同级的规范表达）。
- KEYWORDS：database、schema、ORM、indexing、queries、migrations——充分 ✅。
- 无跨技能路由 ✅。
- 长度：约 228 字符 ≤1024 ✅。

**description 综合判定**: **完全合规**——WHAT/WHEN/KEYWORDS 三要素齐备、触发信号字面规范。评级: 🟢 满分。4 个技能中 description 质量并列最佳（与 018 同）。

### 2.4 `allowed-tools` 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 是否允许字段 | ✅ | 规范 §1.2 允许 |
| 格式 | ✅ | 逗号分隔字符串：Read, Write, Edit, Glob, Grep（规范 §1.2 示例格式） |
| 内容合理性 | ✅ | 与导航型技能匹配（读主题文件 + 写交付物 + 搜索定位） |
| 一致性检查 | ⚠️ | **缺 Bash**：技能目录含 `scripts/schema_validator.py`（Python 脚本），运行它需要 Bash——但该脚本未被 SKILL.md 引用（孤儿），若将来接线则需补 Bash 到 allowed-tools。当前无实际冲突 |
| 对比检查 | ✅ | 与技能实际动作匹配（对比 021 的空 allowed-tools 值，本技能为规范填写） |

### 2.5 其他字段检查

- `argument-hint` 未声明（可选 ✅）。
- 规范 §1.3 禁止字段清单 37 项逐项核对：**全部未出现** ✅。
- 无 body 末尾 Metadata 节（不强制）。

### 2.6 YAML 语法检查

- 三个标量字段，无引号包裹需求，无冒号+空格风险 ✅。可正常解析。

---

## 3. Body Section-by-Section Analysis

### 3.1 段落/章节清单（SKILL.md 全文 52 行）

| # | 行号 | 章节 | 类型 | 功能 |
|---|------|------|------|------|
| 1 | 7 | `# Database Design` | H1 | 总标题 |
| 2 | 9 | 引用块 "Learn to THINK, not copy SQL patterns." | 哲学宣言 | 技能气质声明 |
| 3 | 11-23 | `## 🎯 Selective Reading Rule` | **内容地图（导航核心）** | 6 文件路由表：File/Description/When to Read 三列 |
| 4 | 26-31 | `## ⚠️ Core Principle` | 核心原则 | 3 条：不确定就问/按上下文选择/不默认 PostgreSQL |
| 5 | 34-43 | `## Decision Checklist` | 预设计清单 | 5 项复选框 |
| 6 | 46-52 | `## Anti-Patterns` | 反模式 | 5 条 ❌ |

### 3.2 必需章节检查（规范 §3.1）

| 必需节 | 现状 | 是否满足 | 说明 |
|--------|------|:--------:|------|
| Workflow / Process | 仅 `## Decision Checklist`（5 项预设计复选框） | ❌ **缺失** | 没有"设计 schema 的实际步骤"——没有需求收集→实体识别→关系定义→字段设计→索引规划→迁移计划的流程；没有决策树；没有验证门。dossier 判定："'workflow' 仅是 5 项预设计清单——无实际 schema 设计步骤、决策树或过程，使 skill 成为大纲而非过程"——**确认成立**。Decision Checklist 的 5 项是"设计前检查"而非"设计流程"：4/5 项是提问动作（问偏好/选库/考虑部署/规划索引/定义关系），真正进入设计后没有任何步骤 |
| Output Format | 无任何输出节 | ❌ **缺失** | 未定义交付物：schema 输出成什么（DDL？Prisma schema？ERD？SQL 迁移文件？文档？）没有任何格式/结构/路径说明。SCORING OUT-01/OUT-02 是 LLM 判定（"schema design includes indexing strategy/relationship types"），但 SKILL.md 从未声明这些是必须输出的要素 |
| Scope / Limitations | 无任何 Scope 节 | ❌ **缺失** | 未声明不做的事：不写生产 DDL？不负责数据建模培训？不覆盖 NoSQL？不替代迁移执行工具？`Anti-Patterns` 是"不要这样做"的知识清单而非"技能边界" |

**发现 3.2-1（🔴）: 三个必需节全部缺失。** 这是 4 个技能中唯一的"三缺"技能（017/018 三节齐全、019 缺 1 节）。规范 §3.1 的 3 条规则全部不满足，直接影响评级（见 §7、§12）。

### 3.3 内容委托分析

- 委托结构：SKILL.md（52 行导航壳）→ 6 个主题文件（共 260 行知识）。
- 委托比例：52 : 260 ≈ 1 : 5，符合导航型技能比例（规范 §3.2 导航模式 ~30 行 + 子文件路由）。
- 但与"导航型"的范本（如 152-plugin-forge、310-edge-candidate-agent）对比，本技能缺了导航型技能的关键部件：**子文件路由存在（内容地图 ✅），但"进入子文件后如何产出"的流程契约缺失**。导航型技能应当回答"读完 database-selection.md 之后做什么"——本技能在内容地图后直接跳到检查清单，然后结束。
- 委托本身合理，委托后的执行契约缺失——这是本技能结构问题的本质。

### 3.4 节编号 / 标题层级检查

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 标题层级 | ✅ | H1 → H2 两级，一致 |
| 节编号 | ✅ | 无编号，无断裂 |
| **文件组织** | ⚠️ | 主题文件散落在技能根目录（`database-selection.md` 与 `SKILL.md` 同级），未归入 `references/`。SKILL.md 内容地图以裸文件名引用（`` `database-selection.md` ``）——**相对路径可解析**（文件确实在根目录），技术上无断链；但违背 corpus 的组织惯例（知识文件应收于 references/），且与规范 §3.3 的 "references/foo.md" 示例格式不一致。若未来加入更多主题文件，根目录会继续膨胀 |

**发现 3.4-1（🟡）: 主题文件未归入 references/ 子目录。** 裸文件名引用在"文件确实位于技能根目录"的前提下能正确解析（对比 195-backend-dev-guidelines 的路径全错案例，本技能无断链），但：① 与 corpus 322 技能的组织惯例不一致；② 内容地图表格中无路径列，读者无法一眼区分"文件在根目录还是子目录"。建议：将 6 个主题文件移入 `references/` 并更新内容地图引用（工作量 30 分钟，含全局链接检查）。

---

## 4. Logical Consistency

### 4.1 内部一致性扫描

| 检查点 | 位置 | 结果 |
|--------|------|:----:|
| "Learn to THINK, not copy SQL patterns" ↔ Core Principle "Do not default to PostgreSQL" | L9 vs L30 | ✅ 哲学与原则一致：思考先行、不套默认 |
| Core Principle 3 条 ↔ Anti-Patterns 第 1 条（默认 PostgreSQL） | L28-30 vs L48 | ✅ 一致（原则与反模式互证） |
| 内容地图 6 文件 ↔ 磁盘 6 文件 | L17-22 vs 目录 | ✅ 一一对应，全部存在，无孤儿文件（主题文件层） |
| Decision Checklist 5 项 ↔ SCORING PROC-03 的 5 要素枚举 | L37-41 vs SCORING L44-47 | ✅ 逐项一致（偏好询问/上下文选择/部署环境/索引规划/关系类型） |
| Anti-Patterns 5 条 ↔ SCORING NEG-01/NEG-02 | L48-52 vs SCORING L66-81 | ✅ 对应（PostgreSQL 默认 → NEG-01；索引跳过/N+1 → NEG-02） |
| "serverless databases"（description）↔ migrations.md 的 Neon/Turso 节 | description vs migrations.md L30-49 | ✅ 一致 |
| database-selection.md 决策树 ↔ 比较表 | database-selection.md L7-25 vs L29-35 | ⚠️ 决策树含 Supabase（serverless PG 分支）、CockroachDB（global 分支），比较表只有 5 行（PostgreSQL/Neon/Turso/SQLite/PlanetScale）——**Supabase 与 CockroachDB 在树中有、在表中无**，覆盖不对称（见 4.2-1） |

### 4.2 知识文件间的一致性

| 检查点 | 位置 | 结果 |
|--------|------|:----:|
| schema-design.md 的 ON DELETE 四选项 | schema-design.md L49-56 | ✅ CASCADE/SET NULL/RESTRICT/SET DEFAULT 全部为真实 SQL 语义 |
| schema-design.md 的 PK 类型（UUID/ULID/auto-increment/natural key） | L22-28 | ✅ 技术准确；ULID 描述 "UUID + sortable by time" 正确 |
| TIMESTAMPTZ 建议 | L38 | ✅ 与 PostgreSQL 官方建议一致 |
| indexing.md 的索引类型（B-tree/Hash/GIN/GiST/HNSW/IVFFlat） | indexing.md L23-29 | ✅ 技术准确（PG 生态术语正确） |
| indexing.md 的复合索引顺序（equality 先/range 后/selective 先） | L34-38 | ✅ 与通用 B-tree 复合索引理论一致 |
| migrations.md 的零停机策略 | L7-21 | ✅ 正确（add nullable→backfill→NOT NULL；CREATE INDEX CONCURRENTLY；加新列→迁移→部署→删旧列） |
| optimization.md 的 N+1 解法（JOIN/eager loading/DataLoader/subquery） | L13-17 | ✅ 技术准确 |
| orm-selection.md 决策树（edge→Drizzle、DX→Prisma、控制→raw、Python→SQLAlchemy 2.0） | L7-21 | ✅ 合理；SQLAlchemy 2.0 async 提法正确 |
| **"Storing JSON when structured data is better"（Anti-Pattern 第 4 条）** | SKILL.md L51 | ⚠️ 绝对化表述——JSONB 在 PostgreSQL 中有合法用途（半结构化数据、灵活 schema、全文检索），且 schema-design.md 自己讨论的是结构化设计场景。反模式表若指"能用规范表时不要偷懒用 JSON"则应限定语境。轻微过度简化，非错误 |

**发现 4.2-1（🟢 minor）: database-selection.md 内部覆盖不对称。** 决策树列出 Supabase 与 CockroachDB，比较表未收录；内容地图的 "When to Read" 描述写 "PostgreSQL vs Neon vs Turso vs SQLite" 也未提及 Supabase。三个位置对"可选数据库集合"的陈述不一致。修复：比较表补 Supabase/CockroachDB 行，或决策树收敛到比较表集合（10 分钟）。

**发现 4.2-2（🟢 minor）: "workflow" 语义缺失的连带效应。** 由于无工作流步骤，Decision Checklist 的 5 项完成后没有"下一步"指引——agent 检查完 5 项后需要自己发明设计流程。这是 §3.2 缺 Workflow 节在逻辑层面上的体现（不是独立缺陷，是同一缺陷的后果）。

### 4.3 示例正确性

| 示例 | 位置 | 正确性 |
|------|------|:------:|
| 决策树示例（要求→关系型→自托管→PostgreSQL） | database-selection.md L7-25 | ✅ 分支逻辑正确 |
| "PlanetScale: No foreign keys" 权衡列 | database-selection.md L35 | ✅ 事实准确（PlanetScale 历史上禁止外键约束） |
| N+1 示意图（1+N 查询） | optimization.md L7-12 | ✅ 正确 |
| CREATE INDEX CONCURRENTLY 示例 | migrations.md L17 | ✅ 正确（PG 非阻塞建索引） |

### 4.4 条件完整性

| 条件分支 | 完整性 |
|----------|:------:|
| 数据库选择（关系型/边缘/向量/简单/全球分布） | ✅ 5 分支覆盖（database-selection.md） |
| ORM 选择（edge/DX/控制/Python） | ✅ 4 分支覆盖（orm-selection.md） |
| 索引（何时建/何时不建） | ✅ 双向覆盖（indexing.md） |
| 迁移（加列/删列/加索引/改名） | ✅ 4 分支覆盖（migrations.md） |
| 反模式 5 条 | ✅ 覆盖（SKILL.md） |
| **设计流程条件（如：单表 vs 多表？3NF vs 反范式？读重 vs 写重？）** | ❌ **无**——schema-design.md 只列原则无选择逻辑 | 条件决策缺口（对应缺 Workflow 节） |

---

## 5. Reference File Content-Level Review

### 5.1 引用完整性矩阵

| 引用（SKILL.md 内容地图） | 文件存在？ | 路径解析 | 备注 |
|---------------------------|:---------:|:--------:|------|
| `database-selection.md` | ✅ | ✅（根目录同名） | 裸文件名引用，解析成功 |
| `orm-selection.md` | ✅ | ✅ | 同上 |
| `schema-design.md` | ✅ | ✅ | 同上 |
| `indexing.md` | ✅ | ✅ | 同上 |
| `optimization.md` | ✅ | ✅ | 同上 |
| `migrations.md` | ✅ | ✅ | 同上 |
| `scripts/schema_validator.py` | ✅ 存在 | — | **SKILL.md / SCORING / check.py 三处均未引用（孤儿脚本）** |

**引用统计**: 内容地图 6 项全部可解析、无断链 ✅。但存在 1 个孤儿文件（scripts/schema_validator.py）——"存在的资产未被引用"与 019 的"引用的资产全部存在"形成对照。

### 5.2 不可见资源

- 无不可见资源（技能自包含）。无插件/外部档案依赖（对比 017/018 的强外部依赖——本技能评测无需任何 fixture）✅。

### 5.3 跨 skill 引用检查

- 无跨技能文件引用、无 `../` 路径 ✅。
- 无按名称引用的兄弟技能（本技能完全独立）✅。

### 5.4 嵌套检查

- 唯一嵌套：`scripts/` 子目录。无嵌套 skill 文件 ✅。

### 5.5 scripts 审查 — scripts/schema_validator.py（173 行）

**引用状态**: 孤儿。SKILL.md 内容地图未列、SCORING 无对应 criterion、check.py 未调用。唯一的存在痕迹是脚本自身的 docstring。

**功能审查**:
- 用途：扫描项目目录（`**/prisma/schema.prisma`、`**/drizzle/*.ts`、`**/schema/*.ts`），对 Prisma schema 做启发式检查（PascalCase 模型名、@id 存在性、createdAt/updatedAt 建议、外键字段 @@index 建议、enum PascalCase）。
- 命令行接口：`python schema_validator.py <project_path>`，输出人读摘要 + JSON 汇总，退出码恒为 0。
- Windows 兼容性：含 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` 的 Windows 控制台编码处理（带 try/except 保护）——考虑到 corpus 中多处脚本未做此处理，这是加分项 ✅。

**代码质量逐项**:

| 检查点 | 结果 | 说明 |
|--------|:----:|------|
| `find_schema_files` glob 模式 | ✅ | 覆盖常见 Prisma/Drizzle 布局；`schemas[:10]` 上限合理（防扫描爆炸） |
| `validate_prisma_schema` 的 model 正则 `model\s+(\w+)\s*{([^}]+)}` | ⚠️ | 非贪婪 `[^}]+` 在字段含 `}` 注释/默认值时截断（如 `@default(dbgenerated("...}"))`）；对启发式工具可接受，但注释含 `{`/`}` 时会误报 |
| `if '@id' not in model_body and 'id' not in model_body.lower()` | ⚠️ | `id` 子串会命中 `grid`、`identity` 等字段名——误报风险（如字段名 `identity` 会让缺失 @id 的模型漏报） |
| `@relation` 检查循环 | 🔴 **死代码** | L71-74：对每个 relation 检查 `fields:`/`references:`，但无论结果如何都执行 `pass`——**不产生任何 issue，代码块整体无作用**。要么删掉，要么实现隐式/显式 relation 检查 |
| Drizzle 校验 | ⚠️ 未实现 | L129：`issues = []  # Drizzle validation could be added`——检测到 Drizzle schema 但不校验，输出 "Validating: x.ts (drizzle)" 后直接无结果。半成品痕迹 |
| `passed` 恒为 True | ✅ 设计意图明确 | L155 注释 "Schema issues are warnings, not failures"——校验器定位为"提示器"而非"门禁"，与脚本语义一致（但若未来用作评测 gate 需注意） |
| `except:` 裸异常（L24） | ⚠️ | 裸 except 捕获一切，编码处理中可接受，但 PEP8 建议 `except Exception` |
| 输出 JSON | ✅ | 结构完整（script/project/schemas_checked/issues_found/passed/issues） |
| 退出码 | ✅ | 恒 0（无失败语义），与"warnings"定位一致 |

**发现 5.5-1（🟡）: schema_validator.py 是未接线资产。** 三个问题叠加：① 孤儿状态（无任何引用）；② 死代码循环（relations 检查不产出）；③ Drizzle 分支未实现。处置建议（择一）：a) 在 SKILL.md 内容地图增加脚本条目并在 SCORING 增加 script 判定（如 tool_log 含 schema_validator）；b) 删除脚本（若无意维护）；c) 完成 Drizzle 分支与死代码清理后接线。推荐 a（脚本有真实价值）。

### 5.6 主题文件全文审查（6 个）

#### 5.6.1 database-selection.md（45 行）

| 元素 | 质量 | 问题 |
|------|:----:|------|
| 决策树（5 分支） | ✅ 分支合理 | Supabase/CockroachDB 与比较表不对称（4.2-1） |
| 比较表 5 行 | ✅ 权衡列如实（Neon "PG complexity"、Turso "SQLite limitations"、PlanetScale "No foreign keys"） | 缺 Supabase/CockroachDB |
| Questions to Ask 5 问 | ✅ 与 SKILL.md Core Principle 的"问用户偏好"呼应 | 无 |
| 标题 "(2025)" | ⚠️ | 版本标签会过时（2025 年知识），建议去掉或改为滚动更新说明 |

#### 5.6.2 indexing.md（40 行）

- 何时建索引（5 类）✅ / 何时不建（3 类：写重表/低基数列/少查列）✅——双向覆盖是亮点。
- 索引类型表 6 行 ✅ 技术准确。
- 复合索引原则 4 条 ✅ 正确。
- **无问题**。

#### 5.6.3 migrations.md（49 行）

- 零停机四策略 ✅ 全部正确（加列/删列/建索引/改名）。
- 迁移哲学 4 条（单步不做破坏性变更/数据副本测试/回滚计划/事务内执行）✅。
- Neon/Turso 服务化表 ✅ 准确（scale to zero/instant branching/edge/免费档）。
- **无问题**。

#### 5.6.4 optimization.md（38 行）

- N+1 问题示意图与 4 解法 ✅ 准确。
- EXPLAIN ANALYZE 检查清单 4 项 ✅ 准确。
- 优化优先级 5 项 ✅ 合理（先索引→选列→JOIN→limit 早期→缓存）。
- **无问题**。

#### 5.6.5 orm-selection.md（31 行）

- 决策树 4 分支 ✅ 合理。
- 比较表 4 行（Drizzle/Prisma/Kysely/Raw SQL）✅。
- **发现 5.6.5-1（🟢 minor）**: "Prisma ... not edge-ready"（L28）——Prisma 自 2023 年起提供边缘适配器（@prisma/adapter-*），"not edge-ready" 在 2025 语境下**过时**。建议改为 "edge support newer/less battle-tested"。
- **发现 5.6.5-2（🟢 minor）**: 内容地图写 "Drizzle vs Prisma vs Kysely"，比较表实际还含 Raw SQL 行——三方 vs 四方陈述轻微不一致。

#### 5.6.6 schema-design.md（57 行）

- 规范化决策（何时规范化 4 条/何时反范式 4 条）✅ 双向覆盖好。
- PK 类型表 4 行 ✅。
- 时间戳策略 ✅（TIMESTAMPTZ 建议正确）。
- 关系类型表 3 行 ✅（含实现列：FK on child/junction table）。
- ON DELETE 四选项 ✅。
- **无问题**。6 个主题文件中内容最完整的一个。

### 5.7 check.py 与 SCORING 路径一致性核验

- 本技能无路径变量（SCORING 无 Variables 注释——对比 017/018 有变量定义）。SCORING 的 2 个 script 判定均为 tool_log 正则，无文件路径依赖 ✅。
- check.py 实现与 SCORING 声明一致（SCOPE-02、PROC-02）✅。

---

## 6. Grammar & Format Quality

### 6.1 拼写与语法

- SKILL.md：52 行零错字。句式简短、命令式（导航型风格一致）✅。
- 6 个主题文件：零错字。ASCII 决策树格式工整（对齐正确，对比 147 号技能的错位 ASCII 流程图，本技能树形缩进一致）✅。
- schema_validator.py：注释与 docstring 英文规范 ✅。

### 6.2 中英混杂检查

- 全部纯英文 ✅（对比 corpus 中 306/319 等葡语混入案例，本技能干净）。

### 6.3 Markdown 破损检查

| 检查项 | 结果 |
|--------|:----:|
| 围栏代码块 | ✅ 全部闭合（决策树均为 ASCII 围栏） |
| 引用块 | ✅ 三处主题文件的引言引用块闭合 |
| 表格 | ✅ 内容地图表 3 列 + 各主题比较表均格式正确 |
| 粗体/列表 | ✅ 无未闭合标记 |
| 标题层级 | ✅ H1 → H2 |

### 6.4 占位符检查

- 无任何占位符（本技能无模板类内容）✅。无 `..` 残留、无 "TODO" 痕迹（schema_validator.py 的 "Drizzle validation could be added" 注释是唯一"未完成"标记——属于代码级注释，非文档占位符，但见 §5.5 处置建议）。

### 6.5 截断检查

- 全部 8 个文本文件完整收尾 ✅。无截断（对比 081/271 的截断案例）。

---

## 7. Spec Compliance（对照 SKILL-SPEC.md v1.0 的 12 条规则清单）

| # | 规则 | 检查 | 结果 |
|---|------|------|:----:|
| 1 | name 小写+连字符，≤64 字符，匹配目录 | `database-design` / `020-database-design` | ✅ |
| 2 | description 第三人称，WHAT+WHEN+KEYWORDS，≤1024 字符 | 约 228 字符，三要素齐备 | ✅ |
| 3 | description 无祈使/第一/第二人称开头 | 第三人称开头 | ✅ |
| 4 | description 无跨技能路由 | 无 | ✅ |
| 5 | description 至少一个触发信号短语 | **"Use when the user asks to..." 字面匹配规范形式二** | ✅ |
| 6 | frontmatter 无允许列表外键 | 仅 name/description/allowed-tools（三者均在允许列表） | ✅ |
| 7 | body ≤600 行 | 52 行 | ✅ |
| 8 | body 有 workflow/process 节 | 仅 5 项 Decision Checklist，无流程步骤 | ❌ **未通过** |
| 9 | body 有 output format 节 | 无任何输出节 | ❌ **未通过** |
| 10 | body 有 scope/limitations 节 | 无任何 Scope 节（Anti-Patterns 非边界声明） | ❌ **未通过** |
| 11 | body 无跨技能文件引用 | 无 ../ 路径 | ✅ |
| 12 | 目录 NNN-kebab-case | `020-database-design` | ✅ |

**合规判定**: 8/12 通过，**3 条必需节规则（8/9/10）全部未通过**——这是 4 个技能中最严重的规范缺口，也是本批次唯一"三缺"技能。Frontmatter 侧（规则 1-6）全部通过，description 质量甚至名列前茅；问题全部集中在 body 结构。**合规性: 🟠（需结构性修复）**。

---

## 8. Human-Like Feeling

### 8.1 Emoji 审计

| 位置 | Emoji | 判定 |
|------|-------|:----:|
| `## 🎯 Selective Reading Rule` | 🎯 标题 | ⚠️ **装饰性**——标题含义不依赖图标；corpus 惯例（如 072 被点名的滥用案例）与 dossier 判定均认为标题 emoji 偏装饰 |
| `## ⚠️ Core Principle` | ⚠️ 标题 | ⚠️ 同上（但 ⚠️ 勉强有"注意"语义，弱功能性） |
| Anti-Patterns 5 条 | ❌ × 5 | ✅ 功能性偏装饰——与 019 的 ❌ 前缀同类：作否定标记有语义功能，可接受 |

**Emoji 判定**: 2 个标题 emoji 为装饰性（建议移除），5 个 ❌ 为功能性（可保留）。

### 8.2 全大写审计

| 位置 | 文本 | 判定 |
|------|------|:----:|
| L13 | "**Read ONLY files relevant to the request!**" | ⚠️ 轻度喊叫——ONLY 全大写 + 感叹号。功能上是强调"选择性阅读"（导航型技能的核心纪律），但语气偏机械。可改为 "Read only the files relevant to the request"（加粗即可） |

### 8.3 Persona 语气分析

- 角色：数据库设计教练。语气：简短、命令式、面向 agent 的指令风格。
- 亮点："Learn to THINK, not copy SQL patterns." —— 一句话哲学宣言，有记忆点且与后续原则一致（对比 206-lean-startup 的书摘式无灵魂复述，本宣言短小有力）。
- 无 filler、无 pep-talk、无 marketing 腔 ✅。
- 语气与内容深度不匹配的问题：宣言承诺"教你思考"，但 body 52 行 + 主题文件 260 行只是**知识点清单**，没有"思考过程"的示范（决策树算是最接近的思考结构，但仅在 database-selection 与 orm-selection 两个文件中有）。宣言 > 兑现，是轻微的语气-内容错位。

### 8.4 人机边界

- 本技能无高后果操作（非法律/非金融类），无强制人机门控需求 ✅。
- Core Principle 第 1 条 "ASK the user about database preferences when uncertain" 是恰当的人机交互点 ✅（对应 SCORING PROC-01）。
- 无边界问题。

### 8.5 人称统计（定性）

- "you"：约 5 处（"Read ONLY files relevant to the request!"、"Asked the user about..."）。agent 指令为祈使句，人称使用一致 ✅。
- 无第一人称、无双重受众混淆 ✅。

**人机感评级**: 8.0/10 —— 干净直接，但装饰性标题 emoji、轻度喊叫、宣言与兑现的轻微错位各扣分。

---

## 9. Executability

### 9.1 独立可执行性评分

| 维度 | 评分 (0-10) | 说明 |
|------|:----------:|------|
| 步骤可操作性 | 5.5 | Decision Checklist 5 项可执行，但**进入设计后无流程**——"design a schema" 任务只有原则可依，无步骤可循；agent 必须自行发明设计流程 |
| 决策门完备性 | 4.0 | 无任何质量门（无验证步骤、无输出检查、schema_validator.py 未接线） |
| 环境独立性 | 10 | 完全自包含，无外部依赖（4 个技能中最佳） |
| 工具依赖合理性 | 8.0 | 内容地图读文件路由清晰；allowed-tools 与动作匹配；孤儿脚本未接线 |
| 评测可复现性 | 8.5 | 除 SCOPE-02 正则问题（见 9.3）外可直接评测 |

**独立可执行性总评**: "能导航，不能执行"。agent 可以正确完成"选数据库/选 ORM"（这两个主题有决策树），但"设计 schema/规划迁移/优化查询"只有原则清单，没有过程。对导航型技能而言，选择性阅读机制本身执行良好，但**缺工作流使技能的"执行半程"失效**。

### 9.2 步骤可操作性表

| 动作 | 可操作？ | 需要的用户输入 | 完成判据 |
|------|:-------:|---------------|---------|
| 选择性阅读（内容地图路由） | ✅ | 无 | 按请求读取对应主题文件 |
| Decision Checklist 5 项 | ✅ | 数据库偏好（若不确定） | 5 项全部勾选 |
| 数据库选择 | ✅ | 需求信息 | database-selection.md 决策树落地 |
| ORM 选择 | ✅ | 部署/DX 偏好 | orm-selection.md 决策树落地 |
| **Schema 设计** | ❌ | — | 无流程定义——只能产出"基于原则的任意结构" |
| **索引规划** | ❌ | — | 只有原则（何时建/不建），无"为这张表规划索引"的步骤 |
| **迁移规划** | ❌ | — | 只有策略模式，无"从 schema diff 到迁移文件"的步骤 |
| **查询优化** | ❌ | — | 只有检查清单，无"定位慢查询→诊断→修复→复测"循环 |
| Schema 验证 | ❌ | — | schema_validator.py 存在但未接线，无验证动作 |

**表注**: 后 5 行 ❌ 是 §3.2 缺 Workflow 节的具体化——"design a database schema"（description 的触发场景 1）在本技能中**没有对应执行路径**。这是可执行性的核心缺口。

### 9.3 工具依赖合理性

**发现 9.3-1（🟡）: SCOPE-02 的判定正则与技能文本不匹配。** SCORING SCOPE-02 声明 `tool_log_contains("content-map|content_map")`，check.py L34 同样实现。但 SKILL.md L13 的原文是 "**Check the content map, find what you need.**"——文本中 "content map"（空格分隔），**无 "content-map" 或 "content_map"（连字符/下划线）形式**。agent 按技能文本执行时，工具日志中出现的是 Read 主题文件调用（如 `database-selection.md`），**不会自然产生 "content-map" 字样** → SCOPE-02 结构性失败（除非 agent 恰好发明该词）。修复：pattern 改为 `content map|content-map|content_map`，或改为 `tool_log_contains("database-selection|orm-selection")` 之类与文件读取相关的判定。

- 其余依赖（Read/Write/Edit/Glob/Grep）均为标准工具 ✅。
- schema_validator.py 如需运行需 Bash——当前未接线无冲突（见 §5.5）。

---

## 10. SCORING.yaml Cross-Reference

### 10.1 结构总览

- `pattern: navigation`、`total_items: 10`。实际条目：2 scope + 3 process + 2 output + 2 negative + 1 QA = 10 ✅ 计数一致。
- judge 类型：script 2 项、llm 8 项。check.py 注释 "Run all 2 script checks" ✅ 与实现一致。

### 10.2 逐项映射矩阵

| ID | 类别 | judge | 检查方式 | 对应 SKILL.md 内容 | 可判定性 |
|----|------|:-----:|----------|--------------------|:--------:|
| SCOPE-01 | scope | llm | 首响应框定数据库设计任务 | 内容地图/标题 | ✅ |
| SCOPE-02 | scope | script | tool_log 含 content-map/content_map | 内容地图节 | ❌ **正则与文本不匹配**（9.3-1）——按技能文本执行必然失败 |
| PROC-01 | process | llm | 不确定时询问偏好 | Core Principle 1 | ✅ |
| PROC-02 | process | script | tool_log 含 database-selection\|orm-selection | 内容地图读取 | ✅ agent 读主题文件时 tool log 自然含文件名 |
| PROC-03 | process | llm | Decision Checklist 5 要素走查 | Decision Checklist | ✅ 与清单逐项对应 |
| OUT-01 | output | llm | 设计含索引策略（哪些列/为什么） | **无正文依据** | ⚠️ SKILL.md 未定义"输出必须含索引策略"——LLM judge 只能按常识判定，技能自身无契约 |
| OUT-02 | output | llm | 关系类型定义（1:1/1:N/M:N） | **无正文依据** | ⚠️ 同上（schema-design.md 有关系类型知识，但"输出必须包含"无声明） |
| NEG-01 | negative | llm | 不默认 PostgreSQL | Core Principle 3 + Anti-Patterns 1 | ✅ |
| NEG-02 | negative | llm | 不跳过索引/N+1 | Anti-Patterns 2/5 | ✅ |
| QA-01 | qa | llm | 考虑部署环境 | Decision Checklist 3 | ✅ |

**发现 10.2-1（🟡）: OUT-01/OUT-02 是"无契约输出检查"。** 两个 output 类判定要求 agent 的 schema 设计包含索引策略与关系类型，但 SKILL.md 从未声明输出必须包含这些要素（§3.2 缺 Output 节的直接后果）。LLM judge 依据常识判定会使：① 合格的 agent 若按技能文本执行（无输出契约），产出可能不含索引策略而被误判；② 判定标准悬空，不可复现。修复：补 Output 节（定义交付物结构与必含要素），OUT-01/OUT-02 即自然落地。

### 10.3 Critical Failures 分析

| ID | 描述 | effect | 与 SKILL.md 一致性 |
|----|------|:------:|--------------------|
| CF-01 | 未询问/无上下文即默认推荐 PostgreSQL | cap_to_0 | ✅ 对应 Core Principle 3 + Anti-Patterns 1（技能最核心纪律） |
| CF-02 | 无索引/关系规划即设计 schema | cap_to_0 | ⚠️ 对应 Anti-Patterns 2 + OUT-01/OUT-02，但**无正文流程强制**——技能文本没有任何"设计 schema 前必须规划索引与关系"的显式命令（Decision Checklist 第 4-5 项最接近）。CF-02 判定依赖 LLM judge 对"未规划"的解读 |

**CF 分析**: CF-01 有强正文支撑；CF-02 支撑较弱（技能自身未把"索引/关系规划"设为强制流程）。若按 §13 补 Workflow 节（含索引/关系规划步骤），CF-02 将获得正文依据。

### 10.4 SCORING 质量评价

- 结构上 10 项计数正确、类别分布合理（navigation 模式 + LLM 侧重可接受）。
- 三个实质问题：① SCOPE-02 正则不匹配（9.3-1，结构性失败）；② OUT-01/OUT-02 无契约（10.2-1）；③ CF-02 正文支撑弱。
- 亮点：CF-01 精准对准技能核心纪律；PROC-02 的判定与文件读取自然耦合 ✅。

---

## 11. Known Issues from skill-dossier.md

Dossier 原文（020-database-design 条目）：

> **逻辑**: 选择清单和反模式一致，但 "workflow" 仅是 5 项预设计清单——无实际 schema 设计步骤、决策树或过程，使 skill 成为大纲而非过程。
> **语法**: 干净简约；无错字。
> **人机感**: 有力的 "Learn to THINK" 框架，但节标题中的 emoji（🎯, ⚠️）和反模式列表（❌）偏装饰。
> **合规**: Description 第三人称含触发，body 52 行，引用是裸文件名无相对前缀，无 workflow（超出清单）、无 Output Format 节、无 Scope 节。
> **总评**: 🟡 补具体 workflow、Output 和 Scope 节，给文件引用加目录前缀。

**本次审查与 dossier 对照结论**:

| Dossier 声明 | 本次验证 | 结论 |
|--------------|---------|:----:|
| workflow 仅 5 项预设计清单 | ✅ **确认**——Decision Checklist 是"设计前检查"非设计流程 | 确认 |
| 无实际 schema 设计步骤/决策树/过程 | ✅ 确认（schema-design.md 只有原则无决策逻辑） | 确认 |
| 无错字 | ✅ 8 文件扫描零错字 | 确认 |
| 标题 emoji（🎯, ⚠️）偏装饰 | ✅ 确认（❌ 反模式前缀判定为功能性，微调 dossier） | 确认 |
| 裸文件名引用无目录前缀 | ✅ 确认——但**解析无断链**（文件在根目录），问题是组织惯例而非失效引用；dossier 的"加目录前缀"建议应改为"移入 references/ 并加前缀" | 确认（措辞修正） |
| 无 workflow/Output/Scope 三节 | ✅ 确认——**4 个技能中唯一"三缺"** | 确认 |
| 🟡 评级 | ⚠️ 本次评级 C+（6.58/10）低于 dossier 的 🟡——原因：3 条必需节规则全缺（规范 §3.1 三连败）在 322 语料中属于"需修复"档位（对标 082/092 等 🟡 缺节技能的严重度），加上 SCOPE-02 结构性失败与孤儿脚本，综合权重后落至 C+。dossier 的 🟡 与本次 C+ 的差距主要来自：① 本次将 SCOPE-02 正则不匹配计入；② 本次将 OUT-01/OUT-02 无契约计入；③ 本次将孤儿脚本计入 | 评级下调 |

**新发现（dossier 未覆盖）**:
1. SCOPE-02 判定正则与技能文本不匹配（9.3-1）——结构性评测缺陷。
2. OUT-01/OUT-02 无输出契约（10.2-1）。
3. schema_validator.py 孤儿状态 + 死代码循环 + Drizzle 未实现（5.5-1）。
4. database-selection.md 决策树与比较表覆盖不对称（4.2-1）。
5. orm-selection.md 的 "Prisma not edge-ready" 过时（5.6.5-1）。
6. Anti-Patterns 的 JSON 反模式绝对化（4.2）。

---

## 12. Comprehensive Scoring

### 12.1 八维度加权评分表

| 维度 | 权重 | 得分 | 加权 | 主要依据 |
|------|:----:|:----:|:----:|---------|
| 逻辑一致性 | 15% | 6.5 | 0.975 | 原则/反模式/checklist 互证一致；但流程缺失导致"执行逻辑"整体缺位 + 决策树/比较表不对称 |
| 语法与格式 | 10% | 8.5 | 0.850 | 8 文件零错字零破损；ASCII 决策树工整 |
| 人机感 | 10% | 8.0 | 0.800 | 宣言有力；标题 emoji 装饰 + ONLY 喊叫 + 宣言/兑现错位 |
| 规范合规 | 20% | 5.0 | 1.000 | 8/12 通过；§3.1 三必需节全缺（本批次最差） |
| 可执行性 | 15% | 6.0 | 0.900 | 导航机制好、环境独立满分；schema 设计/索引/迁移/优化无执行路径 |
| 引用完整性 | 10% | 7.0 | 0.700 | 6 主题文件全存在全引用无断链；但 1 个孤儿脚本 + 文件未归 references/ + 脚本半成品 |
| SCORING 质量 | 10% | 6.5 | 0.650 | 10 项计数正确、CF-01 精准；SCOPE-02 结构性失败、OUT 无契约、CF-02 支撑弱 |
| 内容深度 | 10% | 7.0 | 0.700 | 6 主题文件知识准确（索引双向覆盖/零停机策略/关系类型为亮点）；但总量 260 行偏薄，无 schema 示例/DDL 样例 |
| **合计** | 100% | — | **6.58** | — |

### 12.2 评级

**评级: C+（6.58/10）—— 知识准确但结构不完整，需补齐三必需节后方可使用。**

与 stub REVIEW 的 D+（35/100）对比：stub 的发现（三节缺失、emoji 装饰、裸文件名）本次全部验证成立；stub 未发现的：description 完全合规（stub 未提，实际是 4 技能中最佳之一）、SCOPE-02 正则问题、孤儿脚本、决策树不对称。本次加权 6.58（C+）高于 stub 的 35/100——差异来自：① description 与 frontmatter 侧的强合规表现被计入；② 主题文件知识准确性与零错字被计入；③ 6.58 的落点仍低于 dossier 的 🟡（dossier 未计入评测基础设施问题，详见 §11 对照表）。

---

## 13. Fix Recommendations

### 13.1 🔴 致命问题

| # | 问题 | 位置 | 修复建议 | 工作量 |
|---|------|------|---------|:------:|
| 1 | **三个必需节（Workflow/Output/Scope）全缺** | SKILL.md | 新增三节：
  - `## Workflow`：定义"从需求到 schema 交付"的流程——Step 1 收集需求（数据实体/关系/读写模式/规模）→ Step 2 按内容地图选库选 ORM → Step 3 实体建模（实体识别→关系类型定义→规范化/反范式决策，引用 schema-design.md）→ Step 4 字段设计（PK 策略/时间戳/ON DELETE）→ Step 5 索引规划（引用 indexing.md，产出"每表索引清单"）→ Step 6 迁移规划（引用 migrations.md）→ Step 7 验证（运行 schema_validator.py 或人工走查清单）。每步定义输入/输出/判据。
  - `## Output`：定义交付物格式——schema 设计文档（或 DDL/Prisma schema 文件）的必含要素：表清单、每表字段/PK/FK、关系类型表、索引策略表、部署环境记录。
  - `## Scope & Limitations`：不做清单（不写生产 DDL 部署、不执行真实迁移、不替代容量规划/备份策略设计、不覆盖 NoSQL 详细设计等） + 何时不用（与数据库性能无关的架构任务）。 | 2-4 小时 |

### 13.2 🟡 重要问题

| # | 问题 | 位置 | 修复建议 | 工作量 |
|---|------|------|---------|:------:|
| 1 | SCOPE-02 正则与技能文本不匹配 | SCORING L19-21 / check.py L34 | pattern 改为 `content map|content-map|content_map`；或改为与文件读取耦合的判定（`tool_log_contains("database-selection|orm-selection|schema-design|indexing|optimization|migrations")`） | 10 分钟 |
| 2 | schema_validator.py 孤儿 + 死代码 + 半成品 | scripts/ | 三选一：① 接线（内容地图加脚本条目 + SCORING 加 tool_log 判定 + allowed-tools 补 Bash）；② 删除；③ 先清理（删除 L71-74 死代码循环、补 Drizzle 校验或注明暂不支持）再接线。推荐 ③→① | 30-60 分钟 |
| 3 | 主题文件未归 references/ | 根目录 6 文件 | 移入 `references/`，内容地图引用改为 `references/database-selection.md` 等，全链路检查 | 30 分钟 |
| 4 | OUT-01/OUT-02 无输出契约 | SCORING L49-64 | 与 13.1-1 的 Output 节同步落地——输出契约定义后两个判定即获正文依据 | 随 13.1-1 |

### 13.3 🟢 优化建议

| # | 问题 | 位置 | 建议 | 工作量 |
|---|------|------|------|:------:|
| 1 | 标题 emoji（🎯/⚠️）装饰 | SKILL.md L11/L26 | 移除 emoji，保留文字（"Selective Reading Rule"、"Core Principle"） | 2 分钟 |
| 2 | "Read ONLY files..." 喊叫 | SKILL.md L13 | 去全大写与感叹号："Read only the files relevant to the request."（粗体保留） | 1 分钟 |
| 3 | orm-selection.md "Prisma not edge-ready" 过时 | orm-selection.md L28 | 改为 "edge support newer/less battle-tested" | 5 分钟 |
| 4 | database-selection.md 树/表不对称 | database-selection.md | 比较表补 Supabase、CockroachDB 行，或决策树收敛 | 10 分钟 |
| 5 | "Storing JSON" 反模式绝对化 | SKILL.md L51 | 加限定："Storing JSON when a normalized table fits the data (JSONB is fine for genuinely flexible/semi-structured data)" | 5 分钟 |
| 6 | 内容地图 "Drizzle vs Prisma vs Kysely" vs 表含 Raw SQL | SKILL.md L18 / orm-selection.md | 统一为 4 方或注明 "and raw SQL" | 2 分钟 |
| 7 | 主题文件 "(2025)" 版本标签 | database-selection.md / orm-selection.md 标题 | 移除或改滚动更新说明 | 2 分钟 |

### 13.4 总体结论

**020-database-design 是"有知识、无过程"的技能**：6 个主题文件的知识准确可靠（索引双向覆盖、零停机迁移策略、关系类型实现列是亮点），description 完全合规（4 技能中并列最佳），环境完全自包含。但 body 是 4 个技能中唯一"三必需节全缺"的——没有 workflow（"design a database schema" 触发场景无执行路径）、没有 output 契约（OUT-01/OUT-02 判定悬空）、没有 scope 边界；叠加 SCOPE-02 评测正则结构性失败与孤儿半成品脚本，综合评级落至 C+。**修复方向明确（§13.1 的 Workflow/Output/Scope 三节是核心），按建议补齐后预计可达 B+/A− 档。评级: C+。**
