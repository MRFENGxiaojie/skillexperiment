# REVIEW: 074-social-media-analyzer

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: tool — 社交媒体营销活动性能分析（engagement / ROI / 平台基准对比）
**Body 行数**: 298 行（SKILL.md）
**参考文件数**: 0（引用了 5 个文件，全部不存在）
**已有 REVIEW**: 否（本次为首版）

---

## 1. 目录全量清单

```
074-social-media-analyzer/
├── SKILL.md (298 行)
├── SCORING.yaml (176 行)
└── check.py (83 行)
```

**缺失目录/文件（SKILL.md 中声明但不存在）**：

| 声明路径 | SKILL.md 行号 | 用途 | 状态 |
|----------|:------------:|------|:----:|
| `scripts/calculate_metrics.py` | L172-176 | 计算 engagement rate / CTR / reach rate | 🔴 缺失 |
| `scripts/analyze_performance.py` | L179-191 | 全量分析（ROI、benchmark、建议） | 🔴 缺失 |
| `assets/sample_input.json` | L199 | 示例输入 | 🔴 缺失 |
| `assets/expected_output.json` | L223 | 示例输出 | 🔴 缺失 |
| `references/platform-benchmarks.md` | L164, L260-269 | 平台基准完整数据 | 🔴 缺失 |

该 skill 的 Tools 节、Examples 节、Reference Documentation 节所依赖的全部 5 个外部文件均不存在。目录中仅有 3 个文件，skill 实际以"单文件自包含"形态运行，但文档却是按"带脚本和参考文件"形态编写的。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
```
name: social-media-analyzer
```
- 匹配目录名 `074-social-media-analyzer` 的 slug 部分：✅（与语料库惯例一致，NNN 序号前缀除外）
- 全小写+连字符：✅
- ≤64 字符：✅（21 字符）

### 2.2 description（逐句分析）

原文（L3）：
```
Social media campaign analysis and performance tracking. Calculates engagement
rates, ROI, and cross-platform benchmarks. Use to analyze social media
performance, calculate engagement rate, measure campaign ROI, compare platform
metrics, or benchmark engagement against industry standards. Use when the user
asks to analyze social media campaign performance, calculate engagement rates or
ROI, compare platforms (Instagram, Facebook, TikTok, LinkedIn, Twitter), or
benchmark engagement.
```

逐句拆解：

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "Social media campaign analysis and performance tracking." | WHAT | ✅ |
| "Calculates engagement rates, ROI, and cross-platform benchmarks." | WHAT（展开） | ✅ |
| "Use to analyze social media performance, calculate engagement rate, ..." | WHEN（变体） | ⚠️ 边界——"Use to ..." 是祈使句缩略形式，SKILL-SPEC §2.3 禁止 "Use this skill to..."，§2.4 允许的触发信号是 "Use for..."，"Use to..." 不在允许清单中 |
| "Use when the user asks to analyze social media campaign performance, ..." | WHEN + 触发场景 | ✅ 标准触发短语 |

**问题 1**: "Use to analyze ..." 以祈使缩略形式开头，与 §2.3/§2.4 允许的触发信号清单不完全吻合。虽然紧随其后的 "Use when the user asks to..." 是规范触发短语（§2.4 ✅），但 "Use to..." 句应改写为 "Use for analyzing..." 或直接删除，避免歧义。

**第三人称检查**: 无第一/第二人称代词（"Calculates"、"Use when the user asks" 均为第三人称表述）。✅

**触发短语**: "Use when the user asks to..." ✅（满足 §2.4 至少一个触发信号的要求）

**字符数**: ~440 字符，≤1024。✅

**KEYWORDS**: 含 platform 名称（Instagram、Facebook、TikTok、LinkedIn、Twitter）、动作动词（analyze、calculate、compare、benchmark）、领域术语（engagement rate、ROI）。✅

### 2.3 其他 frontmatter 字段

仅 `name`、`description` 两个字段，无 allowed-tools / argument-hint 等可选字段（该 skill 不需要 allowed-tools——它引用脚本但脚本不存在，见 §5）。无禁止字段。✅

### 2.4 Frontmatter 语法

YAML 分隔符配对正确，description 为单行无转义问题。✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Social Media Analyzer (L6)
## Summary (L12-19)                      —— TOC
## Analysis Workflow (L23-59)
  ### Input Requirements (L36-49)
  ### Data Validation Checks (L51-59)
## Engagement Metrics (L63-88)
  ### Engagement Rate Calculation (L65-69)
  ### Metric Definitions (L72-80)
  ### Performance Categories (L83-88)
## ROI Calculation (L92-130)
  ### ROI Formulas (L103-110)
  ### Engagement Value Estimates (L112-120)
  ### ROI Interpretation (L123-130)
## Platform Benchmarks (L134-164)
  ### Engagement Rate by Platform (L137-144)
  ### CTR by Platform (L146-153)
  ### CPC by Platform (L155-162)
## Tools (L168-191)
## Examples (L195-254)
## Reference Documentation (L258-269)
## Proactive Triggers (L271-276)
## Output Artifacts (L278-284)
## Communication (L286-291)
## Related Skills (L293-298)
```

共 11 个 `##` 节 + 8 个 `###` 子节。结构扁平的参考手册型 body，与 `pattern: tool`（SCORING.yaml L2）匹配。

**问题 2**: Summary TOC（L12-19）只列出 6 个节（Analysis Workflow / Engagement Metrics / ROI Calculation / Platform Benchmarks / Tools / Examples），但 body 实际有 11 个 `##` 节。Reference Documentation、Proactive Triggers、Output Artifacts、Communication、Related Skills 均未列入 TOC。

### 3.2 必需章节检查

#### Workflow/Process 节
- 存在：✅（`## Analysis Workflow`，L23-59）
- 标题明确：✅
- 步骤连贯：✅（L28-35，Step 1-8 编号连续：输入校验→逐帖指标→活动级聚合→ROI（条件）→基准对比→识别 top/bottom→建议→验证）
- 条件分支：✅ Step 4 "Calculate ROI if ad spend provided" 明确标出条件；Step 8 的验证规则（engagement rate < 100%、ROI 与 spend 数据一致）是良好的闭环
- 输入/输出：⚠️ 有 Input Requirements 表（L38-49），但各步骤未标明每步的输入输出

#### Output Format 节
- 存在：⚠️ 弱存在。`## Output Artifacts`（L278-284）是一张三行的"请求→交付物"映射表（audit / what's performing / competitor analysis），`## Communication`（L286-291）描述输出结构（Conclusion → What → Why → How to Act）和置信度标记约定（🟢/🟡/🔴）
- 输出模板：❌ 无正式的输出 schema / 字段定义。Example Output（L225-246）提供了 JSON 示例，但该示例数字本身是错误的（见 §4.1），不能作为格式基准
- 可验证性：❌ 除置信度标记外，无字段级别的可验证输出规范

**问题 3**: Output Format 节以"请求→交付物"映射代替真正的输出格式规范。Agent 无从得知 `campaign_metrics` 应包含哪些必填字段、ROI 缺席时如何呈现（OUT-02 只要求"缺席或标记"）。

#### Scope/Limitations 节
- 存在：❌ **完全缺失**。body 中没有 "Scope"、"Limitations"、"What This Skill Does NOT Do" 节。最接近的是 Data Validation Checks（那是输入校验，不是范围声明）和 Related Skills（L293-298，只列出相邻 skill 名）。

**问题 4（🔴 硬性违规）**: 缺少 Scope/Limitations 节是 SKILL-SPEC.md §3.1 的硬性要求。该 skill 需要一个 Scope 节，至少说明：
- 只分析用户提供的数据，不抓取/不实时采集社交媒体数据
- 不做内容创作、广告文案、排期发布（Related Skills 中 social-content 承担该职责，但未在 body 中声明边界）
- 不做竞争对手深度调研（Output Artifacts 却承诺 "Competitor social analysis"——承诺与能力边界矛盾）
- 基准数据是行业聚合值，不保证适用于具体账号/行业/地区
- Engagement value 估值为假设值而非实际收入
- 不替代平台原生分析工具

### 3.3 内容委托分析

Body 中委托给外部文件的引用共 5 处，全部指向不存在的文件（见 §1）。委托本身属于合理设计（基准数据放 references/ 符合 §3.2 精神），但**委托目标缺失**使 Tools 节与 Examples 节空转。

### 3.4 节编号/标题层级

- 标题层级：`#` → `##` → `###`，无跳级。✅
- 编号序列：Workflow Step 1-8 连续。✅
- 重复标题：无。✅
- 一处小瑕疵：L256-258 `## Reference Documentation` 直接从 `### Examples` 子节之后出现，`##` 与 `###` 的从属关系在语义上断裂（Reference Documentation 应属独立顶级节，此处排版上像是 Examples 的子节）。属轻度排版问题。

### 3.5 Body 长度合规

298 行，低于 600 行上限。✅

---

## 4. 逻辑一致性深度审查

### 4.1 🔴 示例算术矛盾（核心缺陷）

**Example Input（L203-219）**：
```
platform: instagram, total_spend: 2500
posts[0]: likes=342, comments=28, shares=15, saves=45, reach=5200, impressions=8500, clicks=120
```

**按 skill 自身公式（L67-69, L104-110, L113-120）计算**：

| 指标 | 正确值 | 示例输出声称值 | 差异 |
|------|:------:|:------------:|:----:|
| total_engagements = 342+28+15+45 | **430** | 1521 | +1091 |
| Engagement Rate = 430/5200×100 | **8.27%** | 8.36% | +0.09pp |
| CTR = 120/8500×100 | **1.41%** | 1.55% | +0.14pp |
| CPE = 2500/430 | **5.81** | 1.64 | -4.17 |
| Engagement Value = 342×2.50+28×10+15×25+45×15+120×7.50 | **$3,085** | — | — |
| ROI = (3085−2500)/2500×100 | **23.4%** | 660.5% | +637pp |

**示例输出内部也不自洽**：
- 声称 total_engagements = 1521，同时声称 avg_engagement_rate = 8.36%——若以 reach=5200 为分母，8.36% 对应的互动数为 434.7，与 1521 相差 3.5 倍；1521/5200 = 29.25%，与 8.36% 对不上
- 声称的数值之间反而互相印证：CPE 1.64 = 2500/1521（精确等于 1.6437）；ROI 660.5% = (1521×12.5−2500)/2500×100（1521×12.5 = 19,012.5 精确成立）——说明示例输出是**从另一份更大的数据集（多帖）算出来的**，与展示的单帖输入根本不是同一份数据

**连锁错误**：
- Interpretation 节（L250-254）在错误输出之上继续推导："ROI 660% = Exceptional return"（按 L126-129 的 ROI Interpretation 表 >500% 确属 Excellent，表内自洽，但起点错了）；"CTR 1.55% vs 0.22% = 7x above average"（正确 CTR 1.41% 应为 6.4x）
- 若按正确数值运行 L123-130 的 ROI Interpretation 表：ROI 23.4% 落入 "0-100% Break-even — Review targeting and creative" 区间，而 ER 8.27% 落入 "Excellent — Scale and replicate" 区间——同一份数据会同时给出"规模扩张"和"暂停投放、检视定向"两条相反建议。即使修正数字，价值法 ROI 与 ER 分类的结论冲突也需要在 skill 中明确处理（例如声明价值法 ROI 仅为相对参考）

**违反自身校验规则**：L34 "ROI matches spend data"、L35 "Engagement rate < 100%"——示例输出本身是 skill 提供的可复现基准，Agent 若照抄示例即产出与任何公式都不匹配的数字，直接触碰 SCORING CF-01 的精神（"以错误公式/分母计算 engagement rate"）。

### 4.2 性能分类与平台基准表的矛盾

**通用分类表（L84-88）**：
| Excellent > 6% | Good 3-6% | Average 1-3% | Poor < 1% |

**平台基准表（L138-144）**：

| 平台 | 平均值 | Good | Excellent |
|------|:-----:|:----:|:---------:|
| Facebook | 0.07% | 0.5-1% | >1% |
| Twitter/X | 0.05% | 0.1-0.5% | >0.5% |
| TikTok | 5.96% | 8-15% | >15% |

**矛盾点**：Facebook 上 0.6% 的 engagement rate 按平台表（L141）是 "Good"，按通用表（L84-88，<1% 即 Poor）却是 "Poor"；TikTok 上 7% 按平台表是 "Average 以下"（Good 需 8-15%），按通用表却是 "Excellent"（>6%）。通用分类表实际是按 Instagram/TikTok 量级校准的，却未声明适用范围，与 Facebook/Twitter 平台行直接冲突。SCORING PROC-05 要求 Agent "按 >6%/3-6%/1-3%/<1% 阈值应用性能分类"——照做即会对 Facebook 数据给出荒谬评级。

**边界重叠**：>6% 与 3-6%、3-6% 与 1-3%、1-3% 与 <1% 三组阈值在 6%/3%/1% 处未定义包含/排除规则（6.0% 算 Excellent 还是 Good？）。

### 4.3 校验清单与输入 schema 不符

- L56 校验 "Date range is valid (start < end)"——但 Input Requirements（L38-49）**没有任何日期字段**（无 campaign start/end，无 posts[].date）。该校验永远无法执行
- L77 定义 "Reach Rate = Reach / Followers × 100"——但输入 schema 无 `followers` 字段。指标悬空
- L110 定义 "ROAS = Revenue / Ad Spend"——但输入 schema 无 `revenue` 字段。ROAS 无法从输入计算，只能依赖 L98 "Estimate engagement value" 的假设值
- L99 "Estimate engagement value using benchmark rates"——价值估计表（L113-120：Like $2.50 / Comment $10 / Share $25 / Save $15 / Click $7.50）**无任何来源引用**。而 L288-290 的 Communication 节明确要求 "source attribution"（来源标注）——skill 自身的价值表恰恰没有来源，自相矛盾

### 4.4 步骤衔接与条件完整性

| 检查项 | 评估 |
|--------|------|
| Step 1 输入校验 → Step 2 计算 | 衔接 OK，校验清单覆盖了除 0 分母外的多数风险 |
| Step 4 条件分支（有 spend 才算 ROI） | ✅ 与 SCORING OUT-02 的 "no spend" 分支一致 |
| Step 5 平台基准对比 | ⚠️ 未说明平台与分类表冲突时以哪个为准（见 §4.2） |
| Step 8 验证闭环 | ✅ "Engagement rate < 100% / ROI matches spend data"——但示例本身违反此规则（§4.1） |
| 名称一致性 | ⚠️ description（L3）写 "Twitter"，基准表（L142）写 "Twitter/X" |

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 后果 |
|----------|:------------:|:--------:|------|
| scripts/calculate_metrics.py | L173 | ❌ 缺失 | Tools 节无法执行 |
| scripts/analyze_performance.py | L181 | ❌ 缺失 | Tools 节无法执行 |
| assets/sample_input.json | L199 | ❌ 缺失 | Examples 节的"See assets/..."指向空 |
| assets/expected_output.json | L223 | ❌ 缺失 | Examples 节的"See assets/..."指向空 |
| references/platform-benchmarks.md | L164, L260-269 | ❌ 缺失 | 基准数据仅有 body 内表格，无完整版 |

**问题 5（🔴 致命）**: 5 个引用文件全部缺失。SKILL.md 声称的"完整基准数据"、"可运行脚本"、"示例数据文件"均不存在。对 Agent 的实际影响：
- 按 Tools 节运行 `python scripts/calculate_metrics.py ...` 会直接 FileNotFoundError
- SCORING QA-01（tool_log 需含 "calculate_metrics|analyze_performance"）在脚本缺失时无法通过——除非 Agent 自行编写同名脚本（评分设计与缺失产物耦合，见 §10）
- Example Input/Output 的 inline JSON（L203-246）成为唯一数据源，而它本身是错的（§4.1）

### 5.2 不可见资源审计

目录中无 SKILL.md 未提及的额外文件（无死文件、无冗余残留）。✅（这是目录极简的唯一"优点"）

### 5.3 跨 Skill 引用检查

- `../` 路径引用：无。✅
- `@other-skill-name` 引用：无。✅
- 外部 URL 引用：无。✅
- Related Skills 节（L293-298）：以纯名称提及 social-content / campaign-analytics / content-strategy / marketing-context——符合 SKILL-SPEC §3.3（以名称引用，不用文件路径）。✅ 但注意：这 4 个 skill 在语料库中是否实际存在未验证（campaign-analytics、marketing-context 未见序号目录，可能为虚构 skill 名，属轻度风险）。

### 5.4 Scripts 文件审查

无 scripts/ 目录。Tools 节（L170-191）描述的 `calculate_metrics.py`、`analyze_performance.py` 均为悬空引用。**没有脚本意味着检查无脚本可跑**——SCORING QA-01 的设计前提（"scripts run when available"）在现目录形态下必然失败。

---

## 6. 语法与格式质量（逐问题列举）

### 6.1 拼写错误

| 行号 | 当前文本 | 建议修正 | 严重程度 |
|:----:|---------|---------|:--------:|
| — | 未发现拼写错误 | — | — |

### 6.2 语法错误

| 行号 | 问题 |
|:----:|------|
| L3 | "Use to analyze social media performance..." — 祈使缩略句（见 §2.2 问题 1），语法上是不完整句（缺少主语），由 frontmatter 语境隐式补齐 |

### 6.3 中英/葡英混杂

无。全英文，规范。✅

### 6.4 Markdown 格式破损

| 行号 | 问题 |
|:----:|------|
| L256-258 | `## Reference Documentation` 紧随 `### Examples` 之后，标题层级断裂感（见 §3.4），不破坏渲染但破坏结构语义 |

### 6.5 占位符未填充

无 `{{...}}` 或 `..` 占位符。✅

### 6.6 截断内容

无。文件内容完整，无中途截断。✅

### 6.7 TOC 完整性

Summary（L12-19）漏列 5 个节（见 §3.1 问题 2）。🟡

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | `social-media-analyzer` 匹配 `074-social-media-analyzer`（NNN 前缀除外，语料库惯例） |
| 2 | name 全小写+连字符，≤64 字符 | ✅ | 21 字符 |
| 3 | description 第三人称 | ✅ | 无第一/第二人称 |
| 4 | description 含 WHAT + WHEN + KEYWORDS | ✅ | 结构完整 |
| 5 | description 含触发信号短语 | ✅ | "Use when the user asks to..."（§2.4 标准短语）；"Use to..." 为边界情况（§2.3） |
| 6 | description ≤1024 字符 | ✅ | ~440 字符 |
| 7 | 无禁止 frontmatter 字段 | ✅ | 仅 name/description |
| 8 | description 无跨 skill 路由 | ✅ | 无 "NOT for X, use Y" 结构 |
| 9 | body ≤600 行 | ✅ | 298 行 |
| 10 | Workflow/Process 节存在 | ✅ | `## Analysis Workflow` |
| 11 | Output Format 节存在 | ⚠️ | `## Output Artifacts` + `## Communication` 部分覆盖，无正式输出规范 |
| 12 | Scope/Limitations 节存在 | ❌ | **完全缺失**（§3.2 问题 4） |
| 13 | 无跨 skill 文件路径 | ✅ | 无 `../` 引用；Related Skills 用纯名称 |
| 14 | 文件引用仅指向本 skill 目录内 | ⚠️ | 路径均在本目录内，**但 5 个被引用文件不存在** |
| 15 | body 引用相对路径 | ✅ | 均为 `scripts/`、`assets/`、`references/` 相对前缀 |

### 7.2 违规详情

**违规 1（🔴 硬性）— Scope/Limitations 缺失**：SKILL-SPEC §3.1 的三必需节缺一。语料库中 ~68% 的 skill 存在此缺口，但对一个承诺 "Competitor social analysis" 的 tool 型 skill 而言，缺少能力边界声明还会让 Agent 误判能力范围。

**违规 2（⚠️ 边界）— description "Use to..." 祈使缩略**：§2.3 禁止 "Use this skill to..."，§2.4 允许清单中无 "Use to..." 变体。虽然后续标准触发短语弥补了 §2.4 的要求，仍建议改写。

**违规 3（⚠️ 间接）— 引用完整性**：spec §3.3 要求"使用相对路径"，路径形式上合规，但指向不存在的文件，使 §3.3 的意图（可解析的引用）落空。

---

## 8. 人机感评估

### 8.1 Emoji 审计

SKILL.md body 中 emoji 仅出现在 Communication 节（L291）：🟢 verified / 🟡 medium / 🔴 assumed——作为置信度标记的功能性使用，与 SCORING OUT-04 对齐。✅

### 8.2 全大写/喊叫式语言

- 无 "STOP!"、"DO NOT" 式喊叫。
- "**Validation:**"（L34, L101）为粗体标签而非全大写命令，可接受。✅

### 8.3 Persona 语气分析

整体语气：**中性专业参考手册**。代表性例句：
- "Campaign performance analysis with engagement metrics, ROI calculations, and platform benchmarks."（L8）——客观功能描述
- "Before analysis, verify:"（L53）——简洁指令

语气适合 tool 型 skill，无营销腔、无第一人称推销。✅

### 8.4 人机边界分析

- 人类交互点：无显式 AskUserQuestion 设计，skill 是纯分析型工具，一次性产出结果——对工具类 skill 可接受
- 置信度标记（🟢/🟡/🔴）要求 Agent 对假设（如 engagement value 估计）标注可信度——这是良好的人机透明性设计 ✅
- 但价值估计表（L113-120）本身无来源（§4.3），Agent 按 L290 "assumption audit" 自检时只能标记 🔴 assumed——skill 没有为自身假设提供来源，等于把"无来源标注"的负担转嫁给 Agent

### 8.5 人称分析

- 第二人称（you/your）：无。✅
- 第一人称（I/we）：无。✅
- 用户称呼：无直接称呼。✅

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 Agent 只拿到 SKILL.md：
- ✅ 能理解 8 步分析流程
- ✅ 能按公式手算 ER / CTR / CPE / ROI（公式完整且正确）
- ✅ 能按平台基准表做对比（表格齐全）
- ❌ 按 Tools 节执行脚本必然失败（脚本不存在）
- ❌ 参考 `assets/sample_input.json` 必然失败（文件不存在）
- ❌ 参考 `references/platform-benchmarks.md` 必然失败（文件不存在）
- ❌ 若照抄 Example Output 会产出与任何公式不符的数字（§4.1）

**可执行性评分**: 4/10——公式和表格可支撑手工计算，但脚本通道全断，且唯一的输出基准（示例）是错误数据。

### 9.2 步骤可操作性

| Step | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| 1 | 输入校验 | 🟢 | 校验清单具体（reach>0、非负、平台识别），但"日期范围"校验无字段可依（§4.3） |
| 2 | 每帖指标计算 | 🟢 | 公式明确，分母正确（reach） |
| 3 | 活动级聚合 | 🟢 | 定义明确 |
| 4 | ROI（条件） | 🟡 | 无 spend 时的行为未描述（SCORING OUT-02 要求"缺席或标记"，skill 未给 Agent 该指引） |
| 5 | 基准对比 | 🟡 | 平台表与通用分类表冲突时的取舍未说明（§4.2） |
| 6 | 识别 top/bottom | 🟢 | 排序逻辑天然可执行 |
| 7 | 生成建议 | 🟡 | 建议与分类表绑定，分类表本身与平台表冲突 |
| 8 | 验证 | 🔴 | 示例输出违反该验证规则（§4.1），"ROI matches spend data" 的基准自身不成立 |

### 9.3 工具依赖合理性

- 脚本依赖（calculate_metrics.py / analyze_performance.py）：声明存在但缺失——最大可执行性风险
- 无外部 CLI / API 依赖：✅（skill 本身不含网络依赖）
- 计算均可手工完成：✅（公式齐全），但手工计算的"正确性基准"（expected_output.json）缺失且 inline 示例错误

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

共 19 个 criteria（3 scope + 5 process 计算 + 3 process 分析 + 4 output + 2 negative + 2 QA）+ 3 个 critical_failures。`total_items: 19` 与实际 criteria 数一致。✅

### 10.2 各 criteria 与 SKILL.md / check.py 的吻合度

| Criteria | 依据（SKILL.md） | 问题 |
|----------|------------------|------|
| SCOPE-02 | L53-59 校验清单 | regex 含 `valid.*date`——但 schema 无日期字段，Agent 无"日期校验"可做，此 pattern 分支形同虚设 |
| SCOPE-03 | L138-144 平台表 | 合理，但依赖 Agent 正确理解平台表 vs 通用分类表的冲突（§4.2） |
| PROC-01 | L67-69 公式 | regex `(/\s*reach\b|reach\s*\*\s*100|...)` 能匹配正确公式 ✅；讽刺的是 skill 自己的示例输出（8.36%）无法由任何公式重现 |
| PROC-03 | L104-110 | 含 `\bCPM\b\|\bROAS\b`——ROAS 依赖不存在的 revenue 字段（§4.3），Agent 只能估或略 |
| PROC-05 | L84-88 分类表 | 与平台表冲突（§4.2），照表执行对 Facebook/Twitter 会给出错误评级 |
| OUT-02 | L95 Step 4 条件 ROI | regex 含 `no spend` 分支，设计良好 ✅ |
| OUT-03 | L34-35, L101 验证 | regex 匹配 "validation" 关键词——弱验证，Agent 仅写 "validation" 一词即通过 |
| NEG-01 | L55-57 校验 | ✅ 合理，与校验清单对应 |
| NEG-02 | — | ⚠️ **误报风险**：pattern `(fabricat|invented|assumed spend of|made[- ]up)` 是 `output_not_contains`——Agent 若诚实声明 "I did not assume spend of $X" 即被误判。且 skill 要求 Agent 用 L113-120 的**假设价值表**估算 ROI——"estimated value" 措辞可避过 regex，但 "assumed" 措辞会触发 |
| QA-01 | L173, L181 脚本 | 🔴 **不可达成**：脚本不存在，Agent 无法运行 `calculate_metrics|analyze_performance` 且让 tool_log 命中。除非 Agent 自行编写同名脚本（tool_log 中文件名命中才算过） |
| QA-02 | L164, L138-144 | regex 含 `platform-benchmarks`——文件不存在，但 `1.22%\|5.96%` 关键词可从 body 表格命中，可达成 ✅ |

### 10.3 Critical Failures 分析

| CF | 条件 | 合理性 | 备注 |
|----|------|:----:|------|
| CF-01 | 错误公式/分母计算 engagement rate | ✅ 合理 | 讽刺的是 skill 自带示例（8.36%）正是"无法由任何公式导出"的数字——**skill 自身在示范 CF-01 行为** |
| CF-02 | 无 spend 数据却报告 ROI | ✅ 合理 | 与 L49 可选 spend、L59 "Spend > 0 if ROI requested" 一致 |
| CF-03 | 无效输入（reach=0）导致除零 | ✅ 合理 | 与 L55 校验、NEG-01 对应 |

建议增加：
- **CF-04**: Agent 将通用性能分类（>6% Excellent 等）应用于 Facebook/Twitter 数据而未按平台表校准——防止 §4.2 矛盾被"照章执行"放大
- **CF-05**: Agent 报告 ROI 但未说明价值估计来源/置信度——与 Communication 节（L286-291）的来源标注要求对齐

### 10.4 check.py 审查

- 11 个 script 检查项（SCOPE-02、PROC-01~04、OUT-02/03、NEG-01/02、QA-01/02）与 SCORING.yaml 的 script judge 项一一对应，pattern 逐字一致 ✅
- `_shared/checker.py` 导入路径（L9-17）正确，checker.py 存在 ✅
- `workspace` 参数（L20）未被使用——无害冗余
- `set_agent_output` 的路径探测逻辑（L25-30）在 main() 已读文件后重复 `os.path.exists()` 于文件内容上——对超长文本内容依赖 `OSError` 异常路径兜底，逻辑晦涩但功能正常（Windows 下长路径抛 OSError 被捕获）
- 注释 "Run all 11 script checks" 与实际数量一致 ✅

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 中的记录：
> ### 074-social-media-analyzer
> - **逻辑**: 🔴 核心矛盾在示例——按所给输入计算应为 8.27% 与总互动 430，而示例输出写 8.36%、total_engagements 1521、ROI 660%，违反技能自身 "ROI matches spend data" 的校验规则，数字自相矛盾。
> - **语法**: 规范流畅。
> - **人机感**: 中性专业，🟢🟡🔴 为功能标记。
> - **合规**: Description 第三人称，有 Workflow/公式/Output 结构，正文 298 行 ≤600。
> - **总评**: 🟠 计算型技能的自带示例与公式对不上，严重削弱可信度，必须订正。

**验证**: 示例算术矛盾完全属实——本次审查独立复算确认正确值为 ER 8.27%（声称 8.36%）、total_engagements 430（声称 1521）、CTR 1.41%（声称 1.55%）、CPE 5.81（声称 1.64）、价值法 ROI 23.4%（声称 660.5%），且声称值彼此内部自洽（2500/1521=1.64、1521×12.5→ROI 660.5%），证明示例输出源于另一份未展示的数据集。✅ dossier 判断成立。

**dossier 遗漏的问题**（本次审查新增发现）：
1. 🔴 **5 个引用文件全部缺失**（scripts/×2、assets/×2、references/×1）——Tools 节不可执行、Examples 节指向空、SCORING QA-01 不可达成（§1, §5, §10）
2. 🔴 **Scope/Limitations 节完全缺失**——SKILL-SPEC §3.1 硬性违规（§3.2）
3. 🟡 **通用性能分类表与平台基准表矛盾**——Facebook 0.6% 同时是 "Good" 和 "Poor"（§4.2）
4. 🟡 **校验清单与 schema 脱节**——日期/粉丝数/收入字段均不在输入 schema 中，三处校验/指标悬空（§4.3）
5. 🟡 **Engagement value 表无来源**——违反 skill 自身 Communication 节的 "source attribution" 要求（§4.3）
6. ⚠️ 修正示例后 ROI（23.4%）落入 "Break-even" 区间，与 ER 的 "Excellent" 结论相反——价值法 ROI 的方法论张力（§4.1）

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 8/10 | 10% | 0.8 | 结构合规，仅 "Use to..." 祈使缩略边界问题 |
| Body 结构完整 | 5/10 | 10% | 0.5 | Workflow 完整、Output 弱、Scope 缺失、TOC 不完整 |
| 逻辑一致性 | 4/10 | 20% | 0.8 | 示例算术崩坏；分类表与基准表冲突；校验清单悬空；价值表无来源 |
| 参考完整性 | 2/10 | 15% | 0.3 | 5/5 引用文件缺失，评分通道 QA-01 不可达成 |
| 语法格式 | 8/10 | 10% | 0.8 | 无拼写错误，仅标题层级小瑕疵 |
| 规范合规 | 5/10 | 15% | 0.75 | Scope 缺失（硬违规）+ "Use to..." 边界 |
| 人机感 | 8/10 | 10% | 0.8 | 中性专业，emoji 仅功能性，置信度标记设计良好 |
| 可执行性 | 3/10 | 10% | 0.3 | 脚本全缺失、示例输出误导、无输出规范 |
| **加权总分** | | | **50.5/100** | |

### 12.2 评级

🟠 **C+** (50.5/100) — 有明显缺陷，修复后可用

> 与 dossier 的 🟠 评级一致。dossier 只发现示例算术问题；本次审查将其扩展为三大修复线（示例订正 + 补全引用文件 + 补 Scope 节），并额外发现分类表矛盾、schema 脱节等 5 个中等缺陷。核心公式体系（ER 分母为 reach、CPE/CPC/CPM、条件 ROI）本身正确，这是该 skill 仍有修复价值的根本原因。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**1. 订正 Examples 节的示例算术（SKILL.md L195-254）**

- 位置：Example Input（L203-219）、Example Output（L225-246）、Interpretation（L250-254）
- 现状：示例输出（8.36% / 1521 / 1.55% / 1.64 / 660.5%）无法由示例输入（342+28+15+45 互动、reach 5200、impressions 8500、clicks 120、spend 2500）按任何公式导出；声称的 avg_engagement_rate 与 total_engagements 内部矛盾（8.36%×5200=434.7 ≠ 1521）
- 修复方向（二选一）：
  - **方案 A（推荐，改动最小）**：保持单帖输入不变，将示例输出订正为按公式实算的值：`total_engagements: 430`、`avg_engagement_rate: 8.27`、`ctr: 1.41`、`cost_per_engagement: 5.81`、`roi_percentage: 23.4`（价值 $3,085）、`overall_health: excellent`（ER 8.27% > 6% 成立）。同步修正 Interpretation：CTR "6.4x above average"（1.41/0.22）、ROI 结论改为 "Break-even (23.4%) — review targeting"；同时补一句说明价值法 ROI 与 ER 分类结论相反时的处置规则（见修复 4）
  - **方案 B（信息量更大）**：将示例输入扩充为可复现 1521 / 8.36% / 660.5% 的多帖数据集（3-5 个 post 的完整表格，含每帖 likes/comments/shares/saves/reach/impressions/clicks），并补一张"手工验算表"逐帖展示 ER、CPE、价值合计，使 Agent 可全程验证
- 无论哪种方案，订正后必须通过 skill 自身校验（L34 "ROI matches spend data"、L35 "ER < 100%"）
- 不修复后果：Agent 照抄示例即产出错误数字；SCORING CF-01 与 skill 自身示例矛盾；计算型 skill 的可信度根基崩溃

**2. 补全 5 个缺失的引用文件（scripts/ assets/ references/）**

- 位置：skill 目录下新建 `scripts/`、`assets/`、`references/` 三个子目录
- 修复方向：
  - `scripts/calculate_metrics.py`：实现 L67-77 的 ER/CTR/Reach Rate/Virality/Save Rate 计算，读取 JSON 输入，输出逐帖 + 活动级指标。参数签名与 L173 示例一致（输入文件路径）
  - `scripts/analyze_performance.py`：实现 L94-101 的 ROI 全链 + L134-164 平台基准对比 + top/bottom 排序，输出与订正后的示例输出同构的 JSON
  - `assets/sample_input.json`：与订正后的 Example Input 一致；建议同时补一个无 `total_spend` 的变体输入（覆盖 OUT-02 的 "no spend" 分支）
  - `assets/expected_output.json`：与订正后的 Example Output 完全一致（脚本可复现）
  - `references/platform-benchmarks.md`：把 L138-162 三张表扩展到"行业分行业"维度（L263-268 声称含 industry 数据），补数据来源与统计年份（当前表格无出处、无年份，见修复 5）
- 不修复后果：Tools 节（L170-191）完全不可执行；SCORING QA-01 无法通过；Examples 节的 "See assets/..." 指引落空；"完整基准数据"承诺落空

**3. 补充 Scope/Limitations 节（SKILL.md 末尾，Related Skills 之前）**

- 位置：L293 Related Skills 之前插入 `## Scope / Limitations`
- 修复方向：至少包含：
  - **不做什么**：不抓取/不实时采集数据（仅分析用户提供的数据）；不做内容创作与排期（交给 social-content）；不做广告投放执行；不生成可视化报告
  - **承诺边界**：Output Artifacts（L282-283）承诺 "Competitor social analysis" 与 "Cross-platform performance analysis"——需声明竞争分析仅限"基于用户提供的对手数据"或降级为"差距分析框架"
  - **数据局限**：基准表为行业聚合值，不保证适用于具体账号/行业/地区/时段；价值估计（L113-120）为假设值，不构成财务建议
  - **不适用的场景**：实时监控、舆情分析、情感分析、NLP 文本分析不在范围内
  - **平台边界**：仅支持 Instagram / Facebook / Twitter(X) / LinkedIn / TikTok 五个平台（与 L40 一致）
- 不修复后果：违反 SKILL-SPEC §3.1；Agent 误判能力范围（尤其 "Competitor social analysis" 承诺）；合规检查不合格

### 🟡 重要缺陷（建议修复）

**4. 消解通用性能分类表与平台基准表的矛盾（L84-88 vs L138-144）**

- 位置：`## Engagement Metrics` 的 Performance Categories 表与 `## Platform Benchmarks` 的表
- 现状：Facebook 0.6% ER 按通用表（<1%）判 "Poor"，按平台表（Good 0.5-1%）判 "Good"；TikTok 7% 按通用表判 "Excellent"，按平台表未达 Good（8-15%）
- 修复方向（三选一）：
  - 将通用分类表明确标注"Instagram/TikTok 校准"，并要求 Agent 在平台表有对应行时一律以平台表为准（表头加注："When platform table exists, use it; generic table applies to Instagram/TikTok-style channels only"）
  - 或为每个平台生成独立的 4 档分类行（把 Average/Good/Excellent 映射为平台表值）
  - 或在 SCORING PROC-05 的 LLM judge 问题中补充"平台优先"判定（配合新增 CF-04）
- 同时定义边界包含规则：`>6%` 与 `3-6%` 在 6% 处重叠——明确 "Excellent: >6%"、"Good: 3% ≤ x ≤ 6%" 之类的不重叠定义
- 不修复后果：Agent 对 Facebook/Twitter 数据产出荒谬评级；SCORING PROC-05 与 SCOPE-03 的判定互相打架

**5. 为 Engagement Value 估计表补来源或降级为假设（L113-120）**

- 位置：ROI Calculation 的 Engagement Value Estimates 表
- 现状：Like $2.50 / Comment $10 / Share $25 / Save $15 / Click $7.50 无任何出处，且与 Communication 节（L290 "source attribution"）自相矛盾
- 修复方向：给表格加"数据来源 + 年份 + 地区"列（如引用行业报告），或明确标注 "🟡 medium — estimates based on industry averages; adjust per client";配合 Communication 节要求 Agent 输出时对该指标自动标记 🔴 assumed / 🟡 medium
- 不修复后果：ROI 百分比的数值可信度存疑；Agent 无法履行来源标注自检；财务向输出有误导风险

**6. 校验清单与输入 schema 对齐（L38-49 vs L53-59, L77, L110）**

- 位置：Input Requirements 表与 Data Validation Checks、Metric Definitions、ROI Formulas
- 修复方向（二选一）：
  - 在 schema 中增加 `posts[].published_date`、`campaign.start_date/end_date`（支撑 L56 日期校验）、`followers`（支撑 L77 Reach Rate）、`revenue`（支撑 L110 ROAS）
  - 或删除对应项：去掉 L56 日期校验、将 Reach Rate 标注"requires followers input, else skipped"、将 ROAS 标注"requires revenue; otherwise compute value-based ROAS with estimated value"
- 不修复后果：Agent 执行 L55-59 校验时对日期项无所适从；Reach Rate/ROAS 指标输出无输入支撑

**7. 补正式 Output Format 规范（L278-291）**

- 位置：`## Output Artifacts` 节
- 修复方向：把订正后的 Example Output JSON 升格为 schema 文档——定义 `campaign_metrics`（total_engagements / avg_engagement_rate / ctr 等必填字段）、`roi_metrics`（无 spend 时该对象缺省并注明 "no spend"）、`insights`（overall_health / benchmark_comparison / top_bottom_performers / recommendations）的字段级说明；明确每字段的类型与单位（% 为百分比数值，money 为浮点）
- 不修复后果：Agent 输出结构不稳定，SCORING OUT-01/OUT-02 的 LLM judge 依赖 Agent 自发对齐

**8. 修正 description 的 "Use to..." 句（L3）**

- 位置：frontmatter description 第 3 句
- 修复方向：改为 "Use for analyzing social media performance, calculating engagement rate..."（§2.4 允许的 "Use for..." 信号），或直接并入后句
- 不修复后果：§2.3/§2.4 的边界争议在合规复查中反复出现

**9. 修正 SCORING QA-01 与缺失脚本的耦合（SCORING.yaml L150-154）**

- 位置：QA-01 定义
- 修复方向：依赖修复 2（脚本落地）后保留现文；若脚本暂不落地，则改写为 "Agent runs analysis scripts when available, or shows full manual computation trace"（与 QA-01 description 原文一致，但 pattern 改为 `(calculate_metrics|analyze_performance|manual computation|computed)`），避免 criterion 在产物缺失时成为不可达死项
- 不修复后果：该 skill 的评分在脚本落地前恒缺 QA-01 一分

**10. 修正 NEG-02 的误报风险（SCORING.yaml L142-145）**

- 位置：NEG-02 的 pattern
- 修复方向：`output_not_contains '(?i)(fabricat|invented|assumed spend of|made[- ]up)'` 中 "assumed spend of" 会命中 Agent 的诚实声明（"I did not assume spend of $X"）。建议收紧为 `(fabricat|invented|made[- ]up.*spend|assumed spend of\s+\d)`（要求"假设了具体金额"才算违规），或在描述中注明"仅在 Agent 编造金额时判负"
- 不修复后果：诚实声明触发 NEG-02 误判，评分失真

**11. 补充无 spend 场景的示例路径（SKILL.md L195-254）**

- 位置：Examples 节
- 修复方向：增加一个"无 total_spend 输入"的迷你示例，展示 ROI 相关输出缺省 + 明确标注 "no spend data provided"（对应 OUT-02 的 `no spend` 分支）
- 不修复后果：Agent 对可选 spend 的两种分支缺乏行为基准

### 🟢 优化建议（锦上添花）

**12. 完成 TOC 与节名一致性**

- Summary（L12-19）补列 Reference Documentation / Proactive Triggers / Output Artifacts / Communication / Related Skills 五个节；"Twitter" 与 "Twitter/X"（L3 vs L142）统一为 "Twitter/X"

**13. 修正 Example Interpretation 的倍率表述**

- 订正后 "8.27% vs 1.22% = 6.8x"（8.27/1.22=6.78 仍成立）、"1.41% vs 0.22% = 6.4x"（原 7x 错）；或改为精确小数点说明，避免 Agent 反向推导出错倍率

**14. 为 check.py 增加 NEG-03（数字一致性自检）**

- 位置：check.py 新增一条 script 检查
- 修复方向：`output_contains '(?i)(8\.27|430|23\.4)'` 之类的**正向数字命中**——即 Agent 输出与订正后示例基准一致时加分。当前 check.py 全部 11 项均为关键词/格式命中，无一项验证**数值正确性**，这是计算型 skill 评分体系的最大盲区。修复 1 落地后可把示例基准值加入正向断言

**15. 简化 check.py 的 set_agent_output 路径探测**

- main()（L71-74）已读取文件内容并传入 check()，check() 内（L25-30）又对内容做 `os.path.exists` 探测（依赖 OSError 异常兜底）。可改为由 main() 直接传入内容、check() 只接收内容字符串，消除冗余逻辑

**16. 验证 Related Skills 中 4 个 skill 名在语料库中的存在性**

- social-content / campaign-analytics / content-strategy / marketing-context 若不存在，改为引用语料库中实际存在的相邻 skill 名（如 paid-ads 055、content-creator 024），或删去未验证的引用

### 修复工作量估计

- 预计修改文件数：3-8 个（SKILL.md + SCORING.yaml + check.py + 新建 5 个引用文件）
- 预计新增行数：SKILL.md ~60-80 行（Scope 节 + 输出规范 + 订正后示例与验算表）；新建文件 5 个共 ~400-600 行（两个脚本 + 两个 JSON + 一个基准文档）
- 预计修改行数：SKILL.md ~40-50 行（示例三处 + 分类表标注 + 校验清单 + TOC + description）；SCORING.yaml ~10 行（QA-01 / NEG-02 / 可选 CF-04、CF-05）；check.py ~10 行（可选 NEG-03 / 简化）
- 优先级排序：修复 1（示例订正）→ 修复 2（补文件）→ 修复 3（Scope）为一组，完成即达 🟢 基准线；修复 4-11 为第二组；修复 12-16 为第三组

---

## 变更记录

- 2026-08-06: 首版深度审查。读取全部 3 个文件（SKILL.md 298 行 + SCORING.yaml 176 行 + check.py 83 行）及 _shared/SKILL-SPEC.md、skill-dossier.md。独立复算示例算术（8.27%/430/1.41%/5.81/23.4% vs 声称 8.36%/1521/1.55%/1.64/660.5%），确认 dossier 🟠 判定成立；新增发现 5 个引用文件全缺失、Scope 节缺失、分类表矛盾、schema 脱节、价值表无来源等 6 项 dossier 遗漏问题。评级 🟠 C+ (50.5/100)。

---

## 附录: 审查过程记录

- 读取文件数：3（SKILL.md + SCORING.yaml + check.py）+ 2 外部参考（_shared/SKILL-SPEC.md、skill-dossier.md 074 条目）
- 读取总行数：~660 行
- 独立复算验证：全部示例数字按 skill 自身公式逐项重算（awk 验算：ER 8.2692%、CTR 1.4118%、CPE 5.814、价值 $3,085、ROI 23.4%；声称值内部自洽验证：2500/1521=1.6437、1521×12.5=19,012.5 → ROI 660.5%）
- 重点审查文件：SKILL.md Examples 节（L195-254）、Performance Categories 与 Platform Benchmarks（L84-162）、SCORING.yaml QA-01/NEG-02/CF-01、check.py 全套 11 项检查
