# REVIEW: 176-polars

**审查日期**: 2026-08-06 | **Skill 类型**: reference — Polars 高性能数据处理参考库（表达式 API / 惰性求值 / I/O / 迁移）
**Body 行数**: 377 | **参考文件数**: refs/6, scripts/0, other/0
**审查文件**: SKILL.md (381 行/9,820 B), SCORING.yaml (156 行/6,568 B), check.py (79 行/2,695 B),
references/ 6 个（合计 3,158 行/71,505 B）
**前置事实**: 目录下无 REVIEW.md（本次为首次生成）; SKILL.md 修改于 2026-08-04 16:14，SCORING/check 修改于
2026-08-05（测评文件晚于正文约 1 天）；references/ 全部修改于 2026-07-31 14:49（早于正文约 4 天）。

---

## 1. 目录全量清单

```
176-polars/
├── SKILL.md              381 行    9,820 B   (2026-08-04 16:14)
├── SCORING.yaml          156 行    6,568 B   (2026-08-05 15:46)
├── check.py               79 行    2,695 B   (2026-08-05 16:36)
└── references/
    ├── core_concepts.md      379 行    8,726 B   (2026-07-31 14:49)
    ├── operations.md         603 行   12,682 B   (2026-07-31 14:49)
    ├── io_guide.md           558 行   11,765 B   (2026-07-31 14:49)
    ├── transformations.md    550 行   12,770 B   (2026-07-31 14:49)
    ├── pandas_migration.md   418 行   11,732 B   (2026-07-31 14:49)
    └── best_practices.md     650 行   14,830 B   (2026-07-31 14:49)
```

- 6 个参考文件全部存在，且**全部被正文引用**（见 §5.1 引用矩阵）——无死文件。
- 无 scripts/、assets/；无 REVIEW.md 残留。references 总量 3,158 行，是 4 个待审 skill 中唯一的"正文 + 参考库"
  双层次结构（spec §3.2 "内容超过 600 行归 references" 的设计范式样本）。

## 2. Frontmatter 逐字段审查

### 2.1 name

- `name: polars` — 小写，长度 6 ≤ 64；与目录名 `176-polars`（去 `NNN-`）完全匹配 ✅。
- 目录 `NNN-kebab-case` 合规 ✅。注意：name 与生态包名相同（通用名词型），无违规。

### 2.2 description（逐句审查）

```yaml
description: "Fast DataFrame library (Apache Arrow). Select, filter, group_by, joins,
lazy evaluation, CSV/Parquet I/O, expression API, for high-performance data analysis
workflows. Use when the user works with polars or large tabular datasets, asks about
lazy evaluation, expressions, or pandas migration, or needs to process CSV/Parquet
files efficiently, optimize data pipelines, or perform high-performance data
manipulation."
```

- **YAML 格式**：✅ 双引号包裹（因内容含逗号与冒号?——实际无冒号，但逗号多；加引号是防御性正确写法，比 177 的
  裸标量更规范）。
- **WHAT**：✅ 首句定位（Fast DataFrame library, Apache Arrow）+ 能力词云（Select/filter/group_by/joins/lazy
  evaluation/CSV-Parquet I/O/expression API）。
  - 小瑕：**"expression API, for high-performance data analysis workflows" 的逗号断句**——"API, for" 用逗号
    连接两个名词短语，读起来是断裂句；应为 "expression API, and high-performance data analysis workflows"
    或改句号（§13 🟢）。
- **WHEN**：✅ 触发场景四类：处理 polars/大型表格数据、询问惰性求值/表达式/迁移、高效处理 CSV/Parquet、
  优化管道/高性能处理——覆盖度高。
- **第三人称**：✅ "the user works with polars" — 无 I/you/we。
- **Trigger 信号**：✅ "Use when the user works with…, asks about…, or needs to…"（spec §2.4 标准信号）。
- **长度**：约 430 字符 ≤ 1024 ✅。
- **无 routing**：✅ 无 "NOT for X" 句式。
- **KEYWORDS**：✅ polars / DataFrame / lazy evaluation / expressions / pandas migration / CSV / Parquet —
  领域词完备。
- **一句话缺位**：description 未提 Excel/数据库/云存储（正文 Data I/O 与 io_guide.md 都覆盖）——触发面略窄
  于能力面；建议在 WHEN 中补 "reads/writes Excel or database sources"（§13 🟢）。

### 2.3 allowed-tools

- 未声明 ✅（reference 型 skill 一般不需要工具面声明；运行代码可能需要 Bash，但那是 agent 侧决策）。

### 2.4 其他字段

- 无 argument-hint / user-invocable 等。reference 型 skill 无需参数提示 ✅。
- 可选建议：`disable-model-invocation: false` 无需显式；不做建议。

### 2.5 YAML

- 两字段（name/description）规范；description 双引号包裹、无转义问题 ✅。

## 3. Body 逐段结构分析

### 3.1 段落清单（按出现顺序）

| # | 章节 | 行区间 | 功能 |
|---|------|--------|------|
| 1 | `# Polars` + `## Overview` | 6–10 | 定位：Arrow 底座 / 表达式 API / 惰性求值 |
| 2 | `## Quick Start` | 12–42 | 安装 + 4 个基础操作代码块 |
| 3 | `## Core Concepts` | 44–91 | 表达式原理 + 惰性/急切双模式 + **加载 core_concepts.md** |
| 4 | `## Common Operations` | 93–165 | Select/Filter/With Columns/Group By + **加载 operations.md** |
| 5 | `## Aggregations and Window Functions` | 167–195 | 聚合函数清单 + over() 窗口 + mapping 策略 |
| 6 | `## Data I/O` | 197–232 | 格式清单 + CSV/Parquet/JSON 示例 + **加载 io_guide.md** |
| 7 | `## Transformations` | 234–272 | Join/Concat/Pivot/Unpivot + **加载 transformations.md** |
| 8 | `## Pandas Migration` | 274–312 | 概念差异 + 映射表 + 并行/串行对照 + **加载 pandas_migration.md** |
| 9 | `## Best Practices` | 314–367 | 5 条性能优化 + 表达式模式 + **加载 best_practices.md** |
| 10 | `## Resources` | 369–381 | 6 个 references 索引清单 |

### 3.2 必需章节（spec §3.1）

- **Workflow/Process**：⚠️ 无传统"步骤式 workflow"（reference 型 skill 的合理形态）。但存在**学习路径结构**
  （Quick Start → Core Concepts → Common Operations → 进阶 → Best Practices → Resources），且每节尾部给出
  "加载 references 明细"的分层指令。对 reference 模式，此结构即 workflow 等价物，判定 ✅（弱形态）。
  - 改进点：可在 Overview 末尾加一句"使用路径建议"（新手走 Quick Start→Core；性能调优直接跳 Best Practices；
    迁移走 Pandas Migration），把隐性导航显性化（§13 🟢）。
- **Output Format**：🔴 **缺失**（Dossier 已标注）。正文没有任何关于"本 skill 产出什么"的章节——对 reference
  型 skill，输出即"正确的 Polars 代码/建议"，但正文未显式声明（如"所有示例可直接运行；复杂场景引用
  references 后给出完整可执行代码"）。SCORING OUT-01/OUT-02（llm）判定"代码有效、迁移映射正确"，
  正文虽通过示例隐含满足，但无输出契约。
- **Scope/Limitations**：🔴 **缺失**（Dossier 已标注）。无 "What this skill does not do" / "When not to use"。
  - 讽刺点：**pandas_migration.md 的 L400–407 有 "When to Stick with Pandas"（5 条适用边界）**，但 SKILL.md
    正文从未提及——知识在参考库中，但没被主文件路由到。这是"正文缺 scope、参考库有 scope"的跨层不一致
    （§13 🟡-1）。

### 3.3 内容委托

- 6 个 references 文件的分工清晰：core_concepts（原理/类型/惰性）、operations（操作大全）、io_guide（I/O）、
  transformations（变形）、pandas_migration（迁移）、best_practices（性能/反模式）——重叠度低、命名直白 ✅。
- 委托边界合理：正文保留"常用 + 决策性"内容（379 行内联示例），"大全/纵深"内容外移——正是 spec §3.2
  的推荐形态 ✅。
- 无跨 skill 引用、无 `../` ✅。

### 3.4 标题层级

- 单一 H1 + 9 个 H2 + H3 小节（### Expressions / ### Lazy vs Eager Evaluation 等）——层级规范 ✅。
- H2 编号不连续（Quick Start / Core Concepts / Common Operations / Aggregations and Window Functions /
  Data I/O / Transformations / Pandas Migration / Best Practices / Resources）——功能分区命名，非步骤编号，
  对 reference 型正确 ✅。

### 3.5 vs 600 行

- 377 行 < 600 硬限 ✅；reference 模式目标 ~300 行，377 略超——但 377 行中约 260 行是代码示例，
  密度合理。若继续膨胀可把 Window Functions 与 Best Practices 的示例再外移（当前无需）。
- 与 references 总量 3,158 行合计 3,535 行——总知识量 corpus 前列，结构无损 ✅。

## 4. 逻辑一致性

### 4.1 步骤衔接

- 无线性步骤；衔接体现为"正文示例 → 参考库深化的引用链"：6 个加载指令（L91/L165/L232/L272/L312/L367）的
  目标文件与主题一一对应（Expressions→core_concepts、Operations→operations、I/O→io_guide、
  Transformations→transformations、Migration→pandas_migration、Best Practices→best_practices）——引用链
  无错位 ✅。
- Quick Start → Core Concepts 的教学顺序自然（先会用、再懂原理）✅。

### 4.2 矛盾排查

- **正文 vs references 术语一致性**（抽查 8 组）：
  | 主题 | 正文 | references | 一致 |
  |------|------|------------|------|
  | 多重条件 filter | 逗号分隔（L118–121） | operations.md L73–77 同式 | ✅ |
  | group_by + pl.len() | L149–152 | operations.md L138–141 同式 | ✅ |
  | over() 窗口 | L181–189 | operations.md L242–249 同式 | ✅ |
  | mapping 三策略 | L192–195 | operations.md L268–289 同式 | ✅ |
  | with_columns 并行 | L138–143 | pandas_migration L87–101 同式 | ✅ |
  | collect(streaming=True) | L331 | best_practices L84 同式 | ✅ |
  | 惰性优先场景 | L79–83 | core_concepts L232–237 同式 | ✅ |
  | 避免 map_elements | L324–327 | best_practices L51–63 同式 | ✅ |
  全部一致 ✅——Dossier "表达式API、惰性求值、窗口函数准确自洽" 属实。
- **版本敏感 API 排查（跨层一致性风险点）**：正文与 references 共用的若干 API 在较新 Polars 版本有演进，
  目前均仍可用，但需版本声明（详见 §6/§13 🟡-4）：
  - `df.write_json("output.json")`（L229 / io_guide L160）— 存在但推荐 write_ndjson，旧版默认 row-oriented 已
    弃用参数化，**示例仍可运行**；
  - `read_csv(ignore_errors=False)`（io_guide L27）— 1.15+ 弃用（改 `malformed`/`truncate_ragged_lines`）；
  - `df.unique(subset=…, keep="first")`（operations L565）— 1.12+ 弃用 keep（改 maintain_order）；
  - `pl.NUMERIC_DTYPES`（core_concepts L85 / operations L24）— 仍存在；`pl.col(pl.NUMERIC_DTYPES, pl.Boolean)`
    （best_practices L255）多 dtype 位置参数**需实测确认**（稳妥写法 `pl.col([pl.NUMERIC_DTYPES, pl.Boolean])`）；
  - `write_ipc("output.arrows")`（io_guide L343–346）"Arrow Streaming" 小节标题与实现不严格对应（write_ipc 写
    的是 IPC 文件格式；真正的流式写是 `sink_ipc`）。
- **无自相矛盾**：全文未发现同主题两处说法冲突的情况 ✅。

### 4.3 代码审查

- 正文 50+ 个代码块，逐块核对 Polars API 真实性（节选）：
  - `df.select("name", "age")` ✅；`pl.col("^.*_id$")` 正则选择 ✅（L108）
  - `df.with_columns(age_plus_10=pl.col("age") + 10)` 关键字表达式赋值 ✅（L39–41）
  - `df.group_by("city").agg(pl.col("age").mean().alias("avg_age"), pl.len().alias("count"))` ✅（L149–152）
  - `pl.col("salary").rank().over("city")` ✅（L183）
  - `df.pivot(values="sales", index="date", columns="product")` — 现代签名 ✅（L266）
  - `df.unpivot(index="id", on=["col1","col2"])` ✅（L269）
  - `pl.concat([df1, df2], how="diagonal")` ✅（L259）
  - `pl.when(condition).then(value).otherwise(other)` ✅（L352）
  - `df1.join(df2, left_on="user_id", right_on="id")` ✅（L246）
  - `lf.collect(streaming=True)` ✅（L331）
- references 代码抽查（节选）：
  - `df.filter(pl.col("city").is_between(25, 35))`… 等等——L114 `is_between(25, 35)` 对 age 列 ✅；
  - `df.group_by("category", maintain_order=True)` ✅（operations L149）；
  - `pl.col("value").rolling_mean(window_size="7d", by="date")` ✅（operations L297–301）；
  - `df.join_asof(quotes, on="timestamp", by="stock", strategy="backward")` ✅（transformations L145–151）；
  - `df.transpose(include_header=True, header_name="quarter", column_names="metric")` ✅（L384–388）；
  - `pl.coalesce(["col1","col2","col3"])` ✅ 接受列表（best_practices L220）；
  - `df.estimated_size('mb')` ✅（L418）；
  - `query.explain(optimized=True)` ✅（L459）；
  - `pl.read_database_uri("SELECT …", uri="postgresql://…")` ✅ 模块级（io_guide L213）；
  - `df.write_database("table_name", connection=engine, if_exists="replace")` ✅（L226–233）；
  - `df[0:5]` 行切片 / `df[0, "column"]` 标量索引 ✅（pandas_migration L18–20）。
- **未发现会导致 CF-01/CF-02 的 API 错误**——正确性是本 skill 的强项 ✅。

### 4.4 条件

- "When to use lazy"（L79–83）4 条件明确；"streaming for very large data"（L329–332）边界清晰 ✅。
- "Use `.map_elements()` only when necessary"（L326）— 条件表述留有判断空间，但 best_practices L65–75 给出了
  必须用时的显式写法（return_dtype + skip_nulls），条件完备 ✅。
- 无含糊条件 ✅。

## 5. 参考文件内容级审查

### 5.1 引用矩阵

| 引用点 | 正文位置 | 目标 | 存在 | 主题对应 |
|--------|----------|------|------|----------|
| `references/core_concepts.md` | L91 | core_concepts.md (379 行) | ✅ | 表达式/类型/惰性/并行 |
| `references/operations.md` | L165 | operations.md (603 行) | ✅ | 选择/过滤/分组/窗口/字符串/日期 |
| `references/io_guide.md` | L232 | io_guide.md (558 行) | ✅ | CSV/Parquet/JSON/Excel/DB/云 |
| `references/transformations.md` | L272 | transformations.md (550 行) | ✅ | join/concat/pivot/unpivot/explode |
| `references/pandas_migration.md` | L312 | pandas_migration.md (418 行) | ✅ | 迁移映射/反模式/清单 |
| `references/best_practices.md` | L367 | best_practices.md (650 行) | ✅ | 性能/表达式模式/陷阱 |
| `## Resources` 索引 | L373–379 | 全部 6 个 | ✅ | 与正文加载指令一致 |

- **6/6 全部被引用，0 死文件**；`## Resources` 的索引描述（"Detailed explanations of expressions, lazy evaluation,
  and type system" 等）与各文件实际内容一致 ✅。
- QA-01 脚本 pattern `references/(core_concepts|operations|io_guide|transformations|pandas_migration|
  best_practices)\.md` 与 6 个引用点逐字兼容 ✅。

### 5.2 不可见资源

- 无外部文件依赖（零 ~/.claude 路径、零插件配置）。所有知识在包内——**4 个待审 skill 中唯一"零外部依赖"者**
  （与 178 并列，但 178 依赖用户提供代码库，本 skill 连输入都自含）✅。

### 5.3 全文审查（6 个 references 逐文件）

**core_concepts.md（379 行）— 评级 ✅ 准确**
- 类型系统（Int8–64/UInt/Float/Utf8/Categorical/Enum/Date/Datetime/List/Array/Struct/Binary/Object/Null）
  完整且与 Arrow 对应 ✅；
- `fill_null(strategy="mean")`（L170）— 0.19.16+ 支持，版本内可用 ✅；
- 惰性/急切对照 + explain() + streaming 限制（L283–286 "Not all operations support streaming"）——诚实 ✅；
- "Random row access slower than pandas"（L316）——正确 ✅；
- 整数列可含 null 不转 float（L373–378）——正确 ✅；
- 唯一小瑕：L332 注释 "Sequential .pipe() chains" 列为"避免"，但 best_practices L614–620 又用 .pipe 组合管线
  （LazyFrame 上 pipe 组合自定义函数是推荐用法）——**两文件对 .pipe 的立场需要调和**：core_concepts 说的是
  "Python 函数塞进 pipe 破坏并行"，best_practices 说的是"纯 LazyFrame 变换的 pipe 组合"。建议在 core_concepts
  加限定语 "…with Python callables"（§13 🟡-3）。

**operations.md（603 行）— 评级 ✅ 准确**
- 分组聚合（sum/mean/median/std/var/quantile/first/last/n_unique）全覆盖 ✅；
- 条件聚合（`(pl.col("salary") > 100000).sum()`、`pl.col("value").filter(...).mean()`、when-then-otherwise.sum）
  准确 ✅；
- 窗口（rank(method="dense"/"ordinal")、rolling、cum_sum、shift over）准确 ✅；
- 字符串（to_titlecase/strip_chars/len_chars）为 0.20+ 命名，正确 ✅；
- 日期（strptime/dt.year()/duration/total_days）正确 ✅；
- 列表（list.eval(pl.element() > 10)）正确 ✅；
- `pl.col("*").name.suffix("_renamed")`（L599）— rename 命名空间正确 ✅；
- 小瑕：L505 "Filter by year: df.filter(pl.col("date").dt.year() == 2023)" ✅ 无问题。未发现实质错误。

**io_guide.md（558 行）— 评级 ✅ 准确（版本敏感 2 处）**
- CSV 参数（separator/has_header/n_rows/skip_rows/dtypes/null_values/encoding）全部真实 ✅；
- Parquet（compression 枚举 snappy/gzip/brotli/lz4/zstd、statistics、use_pyarrow、partition_by、
  `scan_parquet("output_dir/**/*.parquet")` + hive 自动分区列）全部真实 ✅；
- NDJSON 推荐（read_ndjson/scan_ndjson/write_ndjson）✅；
- Excel（read_excel(sheet_name/sheet_id/columns="A,B,C")、pl.ExcelWriter 多 sheet）✅；
- DB（read_database/read_database_uri/write_database + SQLAlchemy engine、Postgres/MySQL/SQLite URI）✅；
- 云（s3:// az:// gs:// + env 凭据）✅；
- 版本敏感：`ignore_errors=False`（L27）弃用趋势；"Arrow Streaming"（L341–347）小节名与 write_ipc 文件格式
  不完全对应——建议改 "IPC/Feather 流式变体" 或补 `sink_ipc` 示例（§13 🟡-4）。

**transformations.md（550 行）— 评级 ✅ 准确**
- 6 种 join（inner/left/outer/cross/semi/anti）+ suffix + 多键 + join_asof(by=, strategy=) 全部真实 ✅；
- concat（vertical/horizontal/diagonal + rechunk/parallel + "Horizontal concat requires same number of rows"）
  准确 ✅；
- pivot（index/columns/values/aggregate_function）与 unpivot（on 支持 `pl.col("^sales_.*$")` 选择器）准确 ✅
  （unpivot 的 on 选择器在 0.20+ 支持，版本内可用）；
- explode/transpose/多级变换（str.extract + drop + pivot 管道）准确 ✅；
- 性能建议（semi/anti 快于 inner+filter、filter before join）——符合 Polars 实践 ✅。

**pandas_migration.md（418 行）— 评级 ✅ 准确**
- 概念差异 5 条（无索引/内存格式/并行/惰性/类型严格）正确 ✅；
- 12 张映射表逐一核对（select/filter/assign/groupby→group_by/size/transform→over/rank/shift/cumsum/merge→join/
  concat 轴/排序/pivot/melt→unpivot/read_csv/to_csv/str.upper→to_uppercase/dt.year→dt.year()/dropna→drop_nulls/
  fillna→fill_null/ffill→fill_null(strategy="forward")）——**全部正确**，无一处 pandas 语法错落到 Polars 侧 ✅；
- "Unique values: `df["col"].unique()` | `df["col"].unique()`"（L194）两边同式——正确（两库方法同名同义）✅；
- 反模式 4 条 + 迁移清单 10 步 + 兼容层（from_pandas/to_pandas/from_arrow）✅；
- "When to Stick with Pandas"（L400–407）诚实边界 ✅——**但该边界未在 SKILL.md 正文出现**（§3.2 缺 scope）。

**best_practices.md（650 行）— 评级 ✅ 准确**
- 性能 7 条（lazy/early select/filter、禁 Python 函数、streaming+sink、类型优化、并行结构、rechunk）✅；
- 表达式模式（when 多条件、null 处理含 per-group fill `fill_null(pl.col("value").mean()).over("group")`、
  coalesce、正则选择、多聚合、条件聚合、组内占比 `pct_of_group`）全部真实 ✅；
- 反模式 6 条（行迭代/原地修改/字符串式 select/低效 join/不指定类型/中间 DataFrame 过多）✅；
- 内存管理（estimated_size/explain/drop/降型 cast）✅；
- 测试调试（schema 断言、eager vs lazy 计时对比、n_rows 采样）✅；
- 代码组织（可复用表达式、LazyFrame 管线函数 + .pipe 组合）✅；
- 版本检查（pl.__version__ + "Document version requirements"）✅——正文缺的版本意识在参考库有，需上提（§13 🟡-4）。

### 5.4 跨 Skill

- 无跨 skill 交互 ✅（纯生态内包，与 179/177 的插件生态无关联）。

### 5.5 死文件

- 无。6/6 references 被正文加载指令或 Resources 索引覆盖（§5.1 矩阵）✅。

## 6. 语法与格式

### 6.1 拼写

- 正文与 references 英文拼写无错（parallelization/predicate/projection/concatenation 等高频词均正确）✅。
- 变量/列名（Alice/Bob/Charlie、NY/LA/SF、age/salary/city）命名一致，示例连贯 ✅。

### 6.2 语法

- 句法正确；"Bad:"/"Good:" 对照句式统一 ✅。
- 正文 L10 "Work with Polars' expression-based API…" — 祈使式营销句，对 reference 型可接受（与 177 的
  description 祈使不同——正文中祈使动词作"用法引导"无碍）✅。

### 6.3 混杂

- 全英文 ✅。中文注释零 ✅。

### 6.4 Markdown

- 标题/列表/代码块/表格结构完整；代码块全部带 python 语言标注 ✅（优于 178 的缺标注）。
- 表格 1 处（正文 Pandas/Polars 映射表 L286–292）+ references 内 12 张表格——**表格密度 corpus 最高**
  （见 §8.6 分析）。
- `df.group_by("city").agg(...)` 等多行代码块缩进一致 ✅。

### 6.5 占位符

- 无 `[...]` 占位符（全部示例为真实代码）✅——reference 型 skill 的正确形态。

### 6.6 截断

- 无截断：正文 381 行完整；6 个 references 代码块闭合；SCORING 156 行（17 项 + 2 CF 完整）；check.py 79 行完整 ✅。

## 7. 规范合规性（SKILL-SPEC v1.0 12 项）

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | name 小写+连字符，≤64，匹配目录 | ✅ | `polars` = 目录去 `176-` 前缀 |
| 2 | description 第三人称，WHAT+WHEN+KEYWORDS，≤1024 | ✅ | ~430 字符，三要素齐备 |
| 3 | description 无祈使/一二人称 | ✅ | "Fast DataFrame library…" 名词开头，第三人称 |
| 4 | description 无跨 skill 路由 | ✅ | 无 |
| 5 | 至少一个 trigger 信号短语 | ✅ | "Use when the user works with…" |
| 6 | frontmatter 无禁用键 | ✅ | 仅 name/description |
| 7 | body ≤ 600 行 | ✅ | 377 行 |
| 8 | body 有 workflow/process 节 | ⚠️ | 无步骤式 workflow；有学习路径 + 加载指令（reference 形态） |
| 9 | body 有 output 节 | 🔴 | **缺失**（无输出契约声明） |
| 10 | body 有 scope/limitations 节 | 🔴 | **缺失**（边界知识在 pandas_migration.md 但未上提） |
| 11 | body 无 `../` 跨 skill 引用 | ✅ | 仅 references/ 相对引用 |
| 12 | 目录 NNN-kebab、无空格大写 | ✅ | `176-polars` |

**结论**：12 项中 9 项全过、1 项弱过（workflow 形态）、**2 项不通过（第 9、10 项：Output 与 Scope 缺失）**——
这是 Dossier 判定 🟡 的直接依据。合规总分是 4 个 skill 中最低者，但**缺的是章节而非内容**（scope 内容存在于
pandas_migration.md），修复成本低（§13 🟡-1/2）。

## 8. 人机感

### 8.1 Emoji

- 0 个 emoji ✅。

### 8.2 喊叫

- 0 处全大写 ✅（"Bad:"/"Good:" 标签、`pl.NUMERIC_DTYPES` 常量、`^.*_id$` 正则均为功能需要）。
- `df[df["col"] > 10]` 类 pandas 对照代码中的大写非喊叫 ✅。

### 8.3 Persona

- 无虚构人格 ✅。全部为事实陈述与代码。

### 8.4 人机边界

- 无授权/决策类边界（reference 型无此需求）✅；版本提示（best_practices L644–648 "Document version
  requirements for production code"）是合理的"交给人判断"点 ✅。

### 8.5 人称

- description 与正文均第三人称（正文无 you/I）✅——4 个 skill 中正文人称最干净（对比 178/179 的正文第二人称）。
- 唯一例外：L326 ".map_elements() only when necessary" 等无主语句式，非人称问题 ✅。

### 8.6 表格→自然语言

- **表格密度 corpus 最高**（正文 1 张 + references 12 张映射表）。评估：
  - 正文 L286–292 的 Pandas/Polars 映射表：5 行核心映射，信息密度高、表格化合理 ✅；
  - references 的 12 张表（pandas_migration 为主）是**对照参考的标准形态**——映射类内容天然表格化，人机都易读 ✅；
  - 无"把自然语言硬塞进表格"的反模式 ✅。
  - 结论：表格使用正确，无需转自然语言；唯一建议是正文映射表与 pandas_migration 的完整版建立"详表见 ref"
    的指向（现有 L312 加载指令已隐含，可显式化，🟢）。

## 9. 可执行性

### 9.1 独立

- ✅ 完全独立：零外部依赖（§5.2）。评测时 agent 可直接以任意 polars 任务执行，QA-01 的 references 加载指令
  指向包内文件，无需任何注入。

### 9.2 步骤

- 无步骤，但有清晰导航：6 个"加载 references"指令 + Resources 索引，agent 按主题取用 ✅。
- 全部示例为可运行代码（`uv pip install polars` 起步）——复制即用 ✅。

### 9.3 工具

- 所需工具：Read（references 加载）、可选 Bash（运行示例验证）。与默认工具集兼容 ✅。
- 无 Write/Edit 需求（参考型只读）✅。

## 10. SCORING 交叉参考

### 10.1 测评点（17 项）与 SKILL.md 覆盖度

| ID | 类别 | judge | check.py 脚本 | SKILL.md 覆盖点 | 一致性 |
|----|------|-------|---------------|-----------------|--------|
| SCOPE-01 | scope | llm | — | 用 Polars 非 pandas / 迁移合理性（L274–312）✅ | ✅ |
| SCOPE-02 | scope | llm | — | 惰性求值适用场景 + scan/collect（L72–83）✅ | ✅ |
| PROC-01 | process | script | output `pl\.col\(` | 全文示例 ✅ | ✅ |
| PROC-02 | process | script | output `\.filter\(` | L114–127 ✅ | ✅ |
| PROC-03 | process | script | output `\.group_by\(\|\.agg\(` | L149–163 ✅ | ✅ |
| PROC-04 | process | script | output `\.over\(` | L181–189 ✅ | ✅ |
| PROC-05 | process | script | output `read_csv\|scan_csv\|read_parquet\|write_parquet\|read_json` | L212–230 ✅ | ✅ |
| PROC-06 | process | script | output `\.join\(\|pl\.concat` | L240–260 ✅ | ✅ |
| PROC-07 | process | script | output `\.pivot\(\|\.unpivot\(` | L266–269 ✅ | ✅ |
| PROC-08 | process | script | output `pl\.when\|\.otherwise\(` | L352 ✅ | ✅ |
| PROC-09 | process | llm | — | lazy + collect(streaming=True)（L318–332）✅ | ✅ |
| PROC-10 | process | llm | — | select before filter（L334–341）✅ | ✅ |
| PROC-11 | process | llm | — | 避免 map_elements（L324–327）✅ | ✅ |
| OUT-01 | output | llm | — | 示例全部真实 API（§4.3 审查通过）✅ | ✅ |
| OUT-02 | output | llm | — | 迁移映射正确（§5.3 pandas_migration 审查通过）✅ | ✅ |
| NEG-01 | negative | llm | — | 无行级循环建议（L323–327 + refs 反模式）✅ | ✅ |
| QA-01 | qa | script | tool_log `references/(core_concepts\|operations\|io_guide\|transformations\|pandas_migration\|best_practices)\.md` | 6 个加载指令（L91/165/232/272/312/367）✅ | ✅ |

**17/17 全覆盖**。脚本项 9 个（PROC-01…08 + QA-01）在 check.py 全部实现，docstring "Run all 9 script checks"
与实际 9 项一致 ✅。8 个 llm 项证据点充分 ✅。

**脚本 pattern 语义提示**：PROC-01…08 均为"agent 输出含某 API 调用"的存在性判定，正文示例与 refs 保证了 agent
有高质量语料可用；但**存在性 ≠ 正确性**（agent 可输出 `pl.groupby()` 也能匹配 `\.agg\(`？——PROC-03 pattern
`\.group_by\(|\.agg\(` 会放过 `df.groupby("x").agg(...)` 这种 pandas 写法）——正确性由 OUT-01/CF-01（llm）把关，
分工合理 ✅。

### 10.2 CF

- **CF-01**（交付代码对真实 Polars API 无效 → cap_to_0）：正文+refs 的示例零错误（§4.3），为 agent 提供了
  正确语料，判定合理 ✅。
- **CF-02**（pandas 语义套用到 Polars 对象 → cap_to_0）：refs 的"反模式"章节（pandas_migration L303–364）直接
  教 agent 避免此类错误，判定合理 ✅。
- 注意 CF-02 与正文"迁移对照表"的共存设计：对照表**故意**展示 pandas 写法（左侧列），agent 若误抄左列即触发
  CF-02——正文 L292 映射表已明确左右分栏为 Pandas/Polars，视觉上可区分，风险可控 ✅。

### 10.3 check.py 实现审查

- 9 个脚本项与 SCORING 一致；`references/…\.md` pattern 中 alternation 与 6 文件名逐字匹配 ✅。
- `\.group_by\(|\.agg\(` 等 pattern 中的转义正确（`\.` 与 `\(`）✅。
- 无错误；唯一改进空间是 PROC 项的存在性判定强度（已由 llm 项补位）✅。

## 11. 已知问题汇总（Dossier 核对）

**Dossier 原话**: "表达式API、惰性求值、窗口函数准确自洽。缺Output与Scope。总评: 🟡"

**验证结果**:
- ✅ "表达式 API、惰性求值、窗口函数准确自洽" — 属实。§4.2 的 8 组正文-refs 对照、§4.3 的 50+ 代码块核对、
  §5.3 的 6 文件全文审查均未发现 API 错误；over()/rank/rolling/mapping 三策略与官方语义一致。
- ✅ "缺 Output 与 Scope" — 属实。正文无输出契约节（第 9 项 🔴）、无 scope 节（第 10 项 🔴）；scope 知识实际
  存在于 pandas_migration.md L400–407 但未上提正文。
- ✅ 总评 🟡 — 与本次 §12 综合评分一致（🟡 B+，规范项拖累）。

**Dossier 遗漏项（MISSED）**:
1. **版本敏感性**：全文（正文 + refs）无 Polars 版本声明；`write_json`、`read_csv(ignore_errors=)`、
   `unique(keep=)`、`pl.col(pl.NUMERIC_DTYPES, pl.Boolean)` 等 API 在 1.x 有演进/弃用趋势，示例"当前可运行"
   但无版本锚点（§13 🟡-4）。
2. io_guide "Arrow Streaming" 小节名与 write_ipc 实现不严格对应（应为 sink_ipc 或改名）。
3. core_concepts 与 best_practices 对 .pipe 的立场表面冲突（Python 函数 pipe vs 纯 LazyFrame 管道组合）——
   需加限定语。
4. description 逗号断句（"API, for"）。
5. description 触发面未覆盖 Excel/数据库/云（能力面 > 触发面）。
6. body 无"使用路径建议"（Overview 未显性化新手/调优/迁移三条导航）。
7. body 377 行略超 reference 目标 ~300 行（可继续外移窗口/最佳实践示例，当前无害）。

## 12. 综合评分（8 维加权）

| 维度 | 权重 | 得分 | 说明 |
|------|------|------|------|
| 规范合规 | 0.20 | 7.5 | 2 项硬缺失（Output/Scope 节），1 项弱过（workflow 形态） |
| 内容完整性 | 0.15 | 9.5 | 377 行正文 + 3,158 行 refs，主题全覆盖 |
| 逻辑一致性 | 0.15 | 9.5 | 8 组正文-refs 对照零矛盾；引用链无错位 |
| 技术准确性 | 0.10 | 9.0 | 50+ 代码块零错误；版本锚点缺失 -0.5 |
| 人机感 | 0.10 | 9.0 | 零 emoji、零喊叫、第三人称干净；表格使用正确 |
| 可执行性 | 0.10 | 9.5 | 零外部依赖，复制即用 |
| 测评对齐 | 0.10 | 9.0 | 17/17 覆盖，9 脚本项实现正确 |
| 参考文件 | 0.10 | 9.5 | 6/6 被引用、无死文件、准确性高 |

**加权得分 ≈ 8.9 / 10 → 🟡 B+**

- 与 Dossier 的 🟡 一致。B+ 的张力：技术内容与参考库是 A 级（9.0–9.5），被规范项（7.5，两节缺失）压到 B 档上沿。
- 修复 §13 的 🟡-1/2（补 Scope 与 Output 节）后，预估 ≈ 9.2 → 🟢 A——**修复成本与评级收益比是 4 个 skill 中
  最高的**。

## 13. 修复建议

### 🔴 致命级
- **无。** 无 API 错误、无 CF 契约矛盾；缺失的 Output/Scope 是规范级而非功能级缺陷（Dossier 亦判 🟡 而非 🟠）。

### 🟡 重要级
1. **补 `## Scope / When not to use` 节**（工作量：15 分钟）
   - 位置：`## Best Practices` 之后、`## Resources` 之前。
   - 内容：从 pandas_migration.md L400–407 提炼 5 条适用边界（复杂索引时间序列、生态依赖 pandas-only 库、
     团队无 Polars 经验、数据小且性能不敏感、需 pandas 高级特性无等价物），并加 2 条本 skill 自身边界
     （"本 skill 不评测运行时性能，示例面向 API 正确性；生产环境请按 best_practices.md 做类型与内存决策"、
     "不覆盖 Spark/DuckDB 等其他引擎迁移"）。
   - 同时把 L312 的加载指令扩展为 "…详细边界清单见 references/pandas_migration.md 的 'When to Stick with
     Pandas'"——闭合跨层不一致。
2. **补 `## Output` 节**（工作量：10 分钟）
   - 位置：Overview 之后。
   - 内容："本 skill 的产出是可直接运行的 Polars 代码与实现建议。所有正文示例均针对当前主版本 API 编写；
     复杂场景先加载对应 references 再给出完整代码；迁移类任务给出 pandas→polars 双侧对照并标注行为差异
     （无索引、类型严格、惰性执行时机）。"
   - 收益：直接补齐规范第 9 项，并为 OUT-01/OUT-02 的 llm 判定提供可引用的输出契约。
3. **调和 .pipe 立场**（工作量：5 分钟）：core_concepts.md L332 改为 "Sequential `.pipe()` chains **with Python
   callables**"，并加注"纯 LazyFrame 变换的管道组合是推荐用法（见 best_practices.md）"。
4. **版本锚点**（工作量：45 分钟，最大单项）
   - 在正文 Overview 末尾与每个 references 头部加一行："Targets Polars ≥ 1.0（2024-11 起主版本）；示例涉及
     API 演进时按最新 1.x 语义书写。"
   - 修订 3 处弃用风险示例：io_guide L27 `ignore_errors=False` → 加注 "1.15+ 建议 `malformed="error"`" 或直接
     移除该参数；operations.md L565 `keep="first"` → `maintain_order=True` 语义说明；SKILL.md L229
     `write_json("output.json")` → 保留但加注 "结构数据建议 write_ndjson（io_guide 有示例）"。
   - best_practices.md L255 `pl.col(pl.NUMERIC_DTYPES, pl.Boolean)` → 改为稳妥写法
     `pl.col([pl.NUMERIC_DTYPES, pl.Boolean])`。
   - 收益：消除本 skill 唯一的技术评分扣分点，并让"准确自洽"在时间维度上可维持。
5. **io_guide "Arrow Streaming" 小节修正**（工作量：10 分钟）：标题改 "IPC 流式写（sink）"，示例补
   `lf.sink_ipc("output.arrows")`，并把现有 write_ipc 示例归入文件格式小节。

### 🟢 优化级
6. **description 断句与触发面**（工作量：5 分钟）："expression API, for high-performance…" → "expression API,
   and high-performance data analysis workflows"；WHEN 补 "reads or writes Excel, database, or cloud
   storage sources"。
7. **Overview 使用路径建议**（工作量：5 分钟）：加 3 行导航（新手 / 性能调优 / pandas 迁移各指一条路径）。
8. **正文映射表指向详表**（工作量：2 分钟）：L292 表下加 "完整 12 张对照表见 references/pandas_migration.md"。
9. **窗口/最佳实践示例继续外移**（工作量：30 分钟，可选）：若未来正文超 400 行，把 §Aggregations and Window
   Functions 的 mapping 策略示例与 Best Practices 的模式块移入对应 references（当前 377 行无需）。

**工作量合计**：核心修复（1–5）约 1.5 小时；含优化约 2 小时。优先顺序：1/2（规范，决定 B→A）→ 4/5（版本，
决定长期准确性）→ 3（一致性）→ 6–8（优化）。

## 附录

- 评审方法：SKILL.md/SCORING.yaml/check.py 全文逐行阅读；references 6 文件全文逐行阅读（合计 3,158 行）；
  对照 `_shared/SKILL-SPEC.md` v1.0 12 项合规清单；对照 `_shared/checker.py`（11,986 B）验证 9 个脚本 pattern
  匹配语义；代码示例按 Polars 1.x 语义人工核对（未实际执行——标注"静态核对"，如需可运行验证建议
  `uv pip install polars` 后执行 §4.3 抽查样本）。
- 目录外未修改任何文件（含 references 6 文件，保持原样）；本 REVIEW.md 为唯一新增文件。
- 行数统计口径：body = SKILL.md 总行数 − frontmatter 行数（381 − 4 = 377）；references 合计 3,158 行；
  SCORING 156 行；check.py 79 行。
- 引用行号基于 2026-08-06 审查时的文件快照（SKILL.md 2026-08-04 16:14 版本，references 2026-07-31 14:49 版本）。
