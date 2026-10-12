# REVIEW: 257-social-content

**审查日期**: 2026-08-06
**Skill 类型**: Process — 多平台社交媒体内容技能（上下文收集 → 平台适配 → 内容支柱 → 钩子 → 复用 → 日历 → 互动 → 分析 → 排期）
**Body 行数**: 311 行（SKILL.md 全文 316 行，frontmatter 4 行 + 空行 1 行；Process 目标线 ~200，超出约 55%）

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\257-social-content\
├── SKILL.md                        316 行, 11,106 B, LF, UTF-8
├── SCORING.yaml                    131 行,  7,220 B, LF, UTF-8
└── check.py                         66 行,  1,872 B, CRLF, UTF-8
```

该目录共 3 个文件（`wc -l` 分别计 315/130/65，末行均无换行符）。**关键事实**：

- 目录下不存在 `references/`、`scripts/`、`assets/`、`templates/`、`examples/` 中任何一类子目录，而 SKILL.md 正文有 **2 处**悬空引用指向 `references/` 下的文件（SKILL.md:101 的 `references/post-templates.md` 与 :255 的 `references/reverse-engineering.md`），全部不存在（详见第 5 节）。
- 无嵌套同名副本（全语料 12 例 `name/name/SKILL.md` 残留模式中，257 不在其列），无违规 frontmatter 残留，目录级卫生在语料中属于干净的一档。
- 行尾风格：SKILL.md 与 SCORING.yaml 为 LF，check.py 为 CRLF，混用属轻微工程洁癖（见第 6.4 节）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

`name: social-content`（SKILL.md:2）。小写 + 连字符，14 字符，符合 ≤64 限制。目录名为 `257-social-content`，按 SKILL-SPEC.md v1.0 §4 的 `NNN-kebab-case-name/` 约定，name 与目录名在去掉序号前缀后完全一致，判定合规。内容含义与技能功能（社交媒体内容）完全对应，无异议。

### 2.2 description（SKILL.md:3）

实测 **398 字符**（yaml 解析后取值），远低于 1024 上限。逐句拆解：

- **句 1**："When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms." — WHAT+WHEN 合并表述，第三人称，无祈使/第一/第二人称。句首不是标准触发句式 "Use when the user..."，而是 "When the user wants..."，省略了 "Use"（详见 §2.5 与第 7 节第 5 项）。
- **句 2**："Also use when the user mentions 'LinkedIn post', 'Twitter thread', 'social media', 'editorial calendar', 'social scheduling', 'engagement', or 'viral content'." — WHEN，含 "use when the user mentions" 触发短语，列出 7 个具体触发关键词，关键词密度良好。
- **句 3**："This skill covers content creation, repurposing, and platform-specific strategies." — WHAT 的职能归纳（创作/复用/平台策略），与正文 14 个 H2 节一一对应。

**语音检查**：全程第三人称，合规。**关键词**：LinkedIn post、Twitter thread、social media、editorial calendar、social scheduling、engagement、viral content 齐备，且这些词在正文中均有对应内容（SCOPE-01 的判定词与 description 完全咬合）。**跨技能路由**：description 全文未点名任何其他技能，第 4 项合规（与 308 的 "Complements social-content..." 违规形成对照）。

**问题点**：description 是一个**未加引号的裸 YAML 标量**。经 `yaml.safe_load` 实测可正常解析（标量内无 `: `、无 `#`），且与 203/150/141/262 等营销族技能的 description 风格同源，技术性无风险；但语料主流均使用双引号包裹，若未来编辑加入冒号或 `#` 会产生静默解析风险（详见第 13 节 🟢-2）。

### 2.3 allowed-tools

未使用。本技能为纯知识型技能，正文无任何工具调用指令（无 Bash/WebSearch/Read 指令），不声明 allowed-tools 无实际影响，属可选优化项而非缺陷。

### 2.4 其他字段

frontmatter 只有 name 与 description 两个键，六个允许的可选键一个未用，**没有任何禁用键**（无 metadata/license/version/tags/author 等）。对照 308 目录内残留违规副本的问题，257 干净。

### 2.5 触发信号（第 5 项判定依据）

SKILL-SPEC §2.4 列出的标准信号为 "Use when the user..."、"Triggers on..."、"Use for..." 等。本 description 句 1 以 "When the user wants..." 开头（无 "Use"），句 2 含 "Also use when the user mentions..."——**意图完全满足**（触发场景与关键词明确），且 203/150/141/262 等语料内多个技能使用同一句式、dossier 未对此类描述判违规，故第 5 项判定为 **✅（附观察）**：严格逐字比对时 "Use when the user wants..." 未出现，建议句 1 补 "Use" 以完全对齐规范样例（详见第 13 节 🟢-1）。

### 2.6 YAML 语法

frontmatter 为 3 行简单 YAML，name 裸标量、description 裸长标量（398 字符单行，也是全文件最长行 411 字符的构成主体），无缩进层级，解析实测通过。SCORING.yaml 为 131 行规整 YAML：缩进一致（criteria 下 id/category/description/judge/check 两级、check 下 question/evidence 三级），引号成对，无裸 `: ` 冲突，`yaml.safe_load` 实测通过，13 条 criteria 与 3 条 critical_failures 全部正常解析。

---

## 3. Body 逐段结构分析

### 3.1 标题树

```
# Social Content                                  (H1, line 6)
├── ## Before Creating Content                    (H2, line 10)
│   ├── ### 1. Goals                              (H3)
│   ├── ### 2. Audience                           (H3)
│   ├── ### 3. Brand Voice                        (H3)
│   └── ### 4. Resources                          (H3)
├── ## Platform Quick Reference                   (H2, 表格 7 行)
├── ## Content Pillars Framework                  (H2, 表格 + 5 问)
│   └── ### Example for a SaaS Founder            (H3, 表格 5 行)
├── ## Hook Formulas                              (H2)
│   ├── ### Curiosity / Story / Value / Contrarian Hooks (H3 ×4)
├── ## Content Repurposing System                 (H2, 表格 5 行)
│   ├── ### Blog Post → Social Content            (H3)
│   └── ### Repurposing Workflow                  (H3, 5 步)
├── ## Content Calendar Structure                 (H2, 表格 5 行)
│   ├── ### Weekly Planning Template              (H3)
│   └── ### Batching Strategy                     (H3, 6 步)
├── ## Engagement Strategy                        (H2)
│   ├── ### Daily Engagement Routine              (H3, 4 项)
│   ├── ### Quality Comments                      (H3)
│   └── ### Building Relationships                (H3)
├── ## Analytics & Optimization                   (H2)
│   ├── ### Metrics That Matter / Weekly Review / Optimization Actions (H3 ×3)
├── ## Content Ideas by Situation                 (H2)
│   ├── ### When You're Starting Out / Stuck      (H3 ×2)
├── ## Scheduling Best Practices                  (H2)
│   ├── ### When to Schedule vs. Post Live        (H3)
│   └── ### Queue Management                      (H3)
├── ## Reverse Engineering Viral Content          (H2, 6 步)
├── ## Task-Specific Questions                    (H2, 6 问)
├── ## Proactive Triggers                         (H2, 5 条)
├── ## Output Artifacts                           (H2, 表格 5 行)
├── ## Communication                              (H2, 4 条 + 收尾段)
└── ## Related Skills                             (H2, 8 条)
```

标题层级为 H1→H2→H3，无跳级、无孤儿标题。14 个 H2 覆盖"调研→平台→内容→钩子→复用→日历→互动→分析→排期→逆向工程→触发→交付→沟通→路由"全链路，是 Process 模式典型的"参考手册式"组织方式。

### 3.2 必需三节检查（SKILL-SPEC §3.1）

- **Workflow/Process**：**满足**。虽然没有名为 "Workflow" 的节，但全 body 以清晰的处理链路推进：Before Creating Content（收集上下文，含 `.claude/product-marketing-context.md` 条件读取）→ Content Pillars（定支柱）→ Hook Formulas（写钩子）→ Content Repurposing System（复用）→ Content Calendar Structure（排期）→ Engagement（互动）→ Analytics（优化）→ Scheduling（发布节奏），每一步都有"做什么 + 怎么做"（清单/表格/步骤号）。规范允许"under any heading name"，dossier 亦判定其链路"调研→平台→内容→钩子→排期→数据完整"，此处判定**满足**。
- **Output Format**：**满足**。`## Output Artifacts`（:282-290）以表格形式明确给出 5 类交付物（社交帖子/编辑日历/复用计划/钩子选项/LinkedIn 串推）的形态定义，直接回答"用户最终得到什么"，是语料中较规范的 Output 节。唯一瑕疵是该表的"LinkedIn 串推"行与"钩子 5 变体"行存在内容不一致（详见第 4.2 节问题 1、2）。
- **Scope/Limitations**：**部分满足（⚠）**。`## Related Skills`（:307-316）以 "USE when... / NOT for..." 的路由句式给出 8 个技能的分工边界（如 "copywriting: NOT for short social posts"、"content-production: NOT for one-off post creation"），形式上承担了 Scope 职能，符合规范 §2.5"routing belongs in body Scope section"的导向；但**缺少对技能自身能力边界的直接陈述**（如"本技能不代发内容、不接入平台 API、不管理账号"），也没有"何时不应使用本技能"的独立小节。12 项清单第 10 项判定为**部分满足（⚠）**，与 308 对同类结构的处理一致。

### 3.3 委派比例

正文无任何子代理委派指令，不涉及委派。技能也没有把重活推给外部脚本或文件的倾向——除 2 处 references/ 指针外，全部知识内联在正文，独立性是语料中最好的之一（详见第 9 节）。

### 3.4 标题层级

如上，H1→H2→H3 无跳级。唯一风格瑕疵：Hook Formulas 下 4 个 H3（Curiosity/Story/Value/Contrarian）与 Pillars 下的 H3 平行，层级深度一致，无不对称问题。`## Output Artifacts`、`## Communication`、`## Related Skills` 三个 H2 位于 Proactive Triggers 之后，作为交付与边界附录合理。

### 3.5 ≤600 行合规

Body 311 行（第 6 行起至第 316 行），远低于 600 行硬上限，合规。但 **Process 模式目标线为 ~200 行，311 行超出约 55%**（111 行），是语料中 Process 类偏长的样本。超出的主体是 5 张信息表格与 4 组 H3 清单（Context 四类、Hook 四类、优化动作两组、Content Ideas 两组），密度尚可、冗余有限；若严格对齐目标线需合并 Task-Specific Questions 等重复节（详见第 4.2 节问题 4 与第 13 节 🟡-6）。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤链

知识链总体自洽且完整：先收集上下文（Goals/Audience/Brand Voice/Resources 四类）→ 平台速查表定格式基线 → 内容支柱定配比 → 钩子公式定首行 → 复用系统扩产量 → 日历与批处理定节奏 → 互动策略建社区 → 分析优化闭环 → 排期实践区分"定时 vs 实时"→ 逆向工程借势 → 最后以 Proactive Triggers 兜底防错。链条内交叉引用一致：支柱示例促销占比 5%（:64）与 Proactive Triggers 的 ">20% 预警"（:277）自洽；Twitter/X 频率 3-10x/day（:44）与"3x/day 跨 4 平台不可持续"（:276）在"单平台 vs 跨平台"维度上兼容（该区分是隐含的，未显式说明，见 4.2 问题 5）；"hook 永远第一行"在 Hook Formulas（:79）、Communication（:303）、CF-02 三处一致。

### 4.2 内部矛盾与张力

逐项核对后共发现以下问题，按严重度排列：

- **"data" 钩子变体悬空（技能正文 vs 交付承诺 vs 评测标准三处不一致）**：Output Artifacts 承诺 "Hook options | 5 hook variants (curiosity, story, value, contrarian, **data**)"（:289），但 Hook Formulas 节只定义了 4 类公式（Curiosity/Story/Value/Contrarian，:81-99），**没有任何 "data" 类钩子的定义或示例**。更严重的是 SCORING.yaml 的 HOO-01（:53-57）判定问题同样写 "curiosity/story/value/contrarian/data formulas"——即评测标准要求 agent 产出技能自身从未定义的东西。三处不一致中最轻的修法是把 "5 variants" 改为 "4 variants" 并同步 SCORING；更好的修法是补一个 "Data Hooks" 类别（如 "X% of [audience] do [behavior] — here's the data"）并给 1-2 个示例（详见第 13 节 🔴-2）。
- **"LinkedIn 串推"的 X 术语错配**：Output Artifacts 承诺 "A LinkedIn thread | Full thread structure: hook **tweet**, 5-8 body **tweets**, CTA **tweet**, with formatting notes"（:290），THR-01 判定问题同文。LinkedIn 没有 tweets/threads 的原生形态（其平台原生形态是帖子、轮播、文章、文档），把 X 术语直接套到 LinkedIn 上会误导 agent 产出形态。同时 "formatting notes" 这一概念在技能全文中从未定义（正文无任何一处解释什么是 formatting notes），判定项依赖一个未定义概念。应改为 "hook post / body posts / CTA post" 并给出 LinkedIn 形态说明（详见第 13 节 🟡-1）。
- **日历模板与交付承诺字段不一致**：Output Artifacts 承诺编辑日历含 "topic, platform, format, pillar, and posting day"（:287），CAL-01 判定问题同文；但正文唯一的日历模板 `## Weekly Planning Template`（:133-139）只有 Day | LinkedIn | Twitter/X | Instagram 三平台列，单元格值是 format 类别（"Industry insight"、"Thread"、"Carousel"），**既没有 topic 列、也没有 pillar 列**。即评测标准 CAL-01 所要求的两字段（topic、pillar）在技能自己的模板中缺席，agent 只能自行扩展模板才能达标——评测项与技能内容存在倒挂（详见第 13 节 🟡-3 与第 10 节）。
- **Task-Specific Questions 与上下文收集节大面积重复**：`:259-266` 的 6 个问题中有 3 个与 `## Before Creating Content`（:10-36）重复——"Do you have existing content to repurpose?"（:263 vs :33）、"How much time can you dedicate weekly?"（:265 vs :31）、"Are you building personal brand, company brand, or both?"（:266 vs :20）。两节间存在约 50% 的信息重复，且 Task-Specific Questions 未提供任何新增信息，属于冗余节，可合并或删除（详见第 13 节 🟡-4）。
- **跨平台频率的隐含前提未显式化**：速查表推荐 Twitter/X 3-10x/day（:44），而 Proactive Triggers 把 "3x/day across 4 platforms" 判为不可持续（:276）。两者在"频率是单平台标准、不可跨平台相乘"的读法下自洽，但技能未用一句话点破这个前提，agent 可能同时采用两个表面冲突的规则。补一句说明即可消解（详见第 13 节 🟢-4）。
- **WhatsApp 孤儿行**：速查表含 WhatsApp 行（:48，"B2C communities, support | As needed | Messages, groups"），但全正文再无任何 WhatsApp 相关内容（无格式、无钩子、无排期建议），description 也未提 WhatsApp（"or other platforms" 兜底）。该行信息孤悬，要么删、要么在 Output 或排期节补一句落地（详见第 13 节 🟡-5）。
- **复用表格重复行**：`### Blog Post → Social Content` 表格（:111-117）中 LinkedIn 出现两行（"Key insight + link in comments" 与 "Carousel of main points"）、Instagram 出现两行（"Carousel with visuals" 与 "Reel summarizing the post"）。不是数据错误，但同一 Platform 值重复出现两行、且与"每周排期表"的平台列布局习惯不一致，属表格组织瑕疵，合并为"LinkedIn（2 种形态）"式表达更清晰（详见第 13 节 🟡-7）。

其余交叉项核对均一致：支柱百分比合计 100%（30+25+25+15+5，:58-64）；"5-8 derivative formats"（REP-01 与 :288）与复用表 5 行、工作流 5 步自洽；Engagement 30 分钟日常（:154-159）与 ENG-01 四要素一致；Analytics 三分层指标与 OPT-01 一致；Queue Management 1-2 周前瞻（:237）与 SCH-01 一致；Proactive Triggers 5 条与 TRG-01 逐一对应；Communication 4 条（结论先行/What+Why+How/平台原生/置信度标注）与 COM-01 一致。

### 4.3 代码块正确性

正文**零个围栏代码块**——本技能没有任何可执行代码、命令或模板代码，所有内容均为散文、列表与表格。不存在代码块闭合问题，也不存在"命令指向缺失脚本"这一 308 式的技术债。对纯知识型 Process 技能而言，无代码块是合理的（见第 9 节）。

### 4.4 条件完整性

技能的条件表达集中在 Proactive Triggers（:270-278）：5 条触发条件全部采用"**症状 → 立即行动**"结构（如 "User wants to post the same content across all platforms → Flag platform format mismatch immediately; adapt tone, length, and structure per platform before writing"），是全文条件逻辑最强的部分，也是语料中罕见的"主动兜底"设计。Analytics 的 Optimization Actions 同样按症状分支（低互动 → 4 项行动；触达下滑 → 4 项行动，:195-207）。这两处是 257 在条件完整性上的亮点。其余节为知识参考型内容，无分支需求。整体判定：条件完整性良好，无 308 式"清单无处置分支"的短板。

---

## 5. 参考文件内容级审查

### 5.1 参考文件完整性矩阵

| 类别 | 预期 | 实际 | 状态 |
|------|------|------|------|
| references/*.md | 2 个文件（正文引用 2 处） | 无此目录 | ❌ 缺失 |
| scripts/*.py | 无引用 | 无 | — |
| assets/ | 无明确需求 | 无 | — |
| templates/ | 无明确需求 | 无 | — |
| examples/ | 无明确需求 | 无 | — |

### 5.2 隐形资源审计

正文 2 处悬空引用，全部指向不存在的文件：

- `references/post-templates.md` — SKILL.md:101（"For post templates and more hooks: See references/post-templates.md"）
- `references/reverse-engineering.md` — SKILL.md:255（"For the full framework: See references/reverse-engineering.md"）

后果评估（与 308 的脚本全缺相比，危害显著更轻）：本技能对 references/ 的依赖是**增强性**而非**必需性**——Hook Formulas 节本身已内联 4 类 12 条钩子公式，Reverse Engineering 节本身已内联 6 步完整流程，两处指针只是"深度扩展"入口。agent 忽略指针可正常完成全部工作流；只有"post templates"（发帖模板）这一被承诺但未内联的内容是真实缺口。2 个 SCORING 判定项均不依赖这两文件，无"必然失分/虚假通过"问题。对比 308 的 5 脚本缺失（20% 判定项失真），此处属中等优先级缺陷。

### 5.3 逐参考文件审查

无任何 references/ 文件可审。全技能知识密度全部内联在 311 行 SKILL.md 中——按 SKILL-SPEC §3.2 的设计意图，超出 Process 目标线的深度内容（post 模板库、逆向工程方法论详解）本应下沉到 references/，本技能用指针做了约定、却没有落地文件。补齐这两个文件（或删除指针）是第 13 节 🔴-1 的核心。

### 5.4 逐脚本审查

scripts/ 目录不存在，正文也无任何脚本引用，无脚本可审——这在本语料中反而是干净的（无 308 式悬空工具链）。

### 5.5 跨技能引用

`## Related Skills`（:307-316）以反引号散文名形式引用 8 个技能，逐一比对全语料 322 个目录：

| 引用名 | 语料实际 | 状态 |
|--------|----------|------|
| `marketing-context` | 实际技能名为 **203-product-marketing-context** | ⚠ 名字不符 |
| `copywriting` | 150-copywriting | ✅ |
| `content-strategy` | **不存在**（全语料无此名技能） | ❌ |
| `copy-editing` | 141-copy-editing | ✅ |
| `marketing-ideas` | **不存在** | ❌ |
| `content-production` | 038-content-production | ✅ |
| `content-humanizer` | 262-content-humanizer | ✅ |
| `launch-strategy` | **不存在** | ❌ |

8 个引用中 4 个有效、1 个名字不符、3 个死引用。需要说明的是：这 3 个死名字是**语料级漂移**而非 257 独有——全语料有 20 个技能在正文中提及 "content-strategy"、4 个提及 "marketing-ideas"、4 个提及 "launch-strategy"，均无对应目录。但 257 是单个技能中死引用最多的（3/8），且其引用的 203 技能名字应为 `product-marketing-context`（该技能 description 明确声明它创建 `.claude/product-marketing-context.md`，正是 257 第 13 行要求读取的文件，两者本应互相点名）。引用形式（散文名 + 反引号）符合规范 §3.3"prose names only、无跨技能文件路径"，第 11 项合规；但 3 个死引用会让 agent 按字面路由到不存在处（详见第 13 节 🟡-2）。

### 5.6 死文件

无嵌套副本、无重复 SKILL.md、无残留原稿，无死文件。

### 5.7 其他资源

assets/、templates/、examples/、specs/、phases/、docs/ 均不存在，根目录亦无 README.md 等附加文件。目录干净，3 文件齐整。

---

## 6. 语法与格式质量

### 6.1 拼写

全文英文拼写干净，未发现拼写错误。"evergreen"（:125、:231、:303）、"repost"（:158）、"Saves"（:184）等营销惯用词拼写正确。"hook tweet"（:290）拼写无误但术语错配见 4.2 问题 2。

### 6.2 语法

句式完整、主谓一致，无残缺句。"The first line determines whether someone will read the rest."（:79）主语明确；"For post templates and more hooks: See references/post-templates.md"（:101）是规范的指引句式；"Share/repost with additional insight"（:158）为祈使清单项，正常。整体语法质量高。

### 6.3 语言混用

全文单一英语，无中英混排、无代码注释侵入正文。技能面向英语社交媒体营销场景，语言选择合理。

### 6.4 Markdown 破坏

无破坏：5 张表格列头分隔行完整且列数匹配（速查表 4 列、支柱表 3 列、复用表 2 列、周历表 4 列、交付物表 2 列）；无序列表、有序列表、加粗、行内代码均正确渲染；`<numbers>` 无。唯一工程洁癖：check.py 为 CRLF 行尾而另两个文件为 LF，混用不影响解析，但与语料主流（LF）不一致。

### 6.5 未填充占位符

钩子公式中的 `[common belief]`、`[outcome]`、`[impressive result]`、`[number]`、`[past state]`、`[current state]`（:82-99）是公式模板的示例变量，属有意设计，非缺陷。无"留白待填"性质的真实占位符残留。

### 6.6 截断

所有文件读取完整，无截断迹象。SKILL.md 结尾（:316）为 Related Skills 最后一项，收尾自然；SCORING.yaml 结尾（:131）为 CF-03 完整定义；check.py 结尾（:66）为 `main()` 守卫完整。

---

## 7. 规范合规性（12-item checklist vs SKILL-SPEC.md v1.0）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | name 小写+连字符、≤64、匹配目录 | ✅ | 14 字符，按 NNN- 前缀约定与 `257-social-content` 匹配 |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✅ | 398 字符，三要素齐备 |
| 3 | description 无祈使/第一/第二人称开头 | ✅ | 全程第三人称 |
| 4 | description 无跨技能路由内嵌 | ✅ | 全文未点名任何其他技能 |
| 5 | description 至少一个触发信号 | ✅ | 句 2 含 "use when the user mentions..."；句 1 为非标准 "When the user wants..." 句式（附观察，见 2.5） |
| 6 | frontmatter 无禁用键 | ✅ | 仅 name+description 两键 |
| 7 | body ≤600 行 | ✅ | 311 行；Process 目标线 ~200 超出 55%（🟡 见 3.5） |
| 8 | body 有 workflow/process 节 | ✅ | 上下文→支柱→钩子→复用→日历→互动→分析→排期全链路（无显式 "Workflow" 标题但规范允许任意标题名） |
| 9 | body 有 output format 节 | ✅ | `## Output Artifacts` 表格，5 类交付物形态明确 |
| 10 | body 有 scope/limitations 节 | ⚠ | 仅 Related Skills 的 NOT-for 路由承担 Scope 职能，无独立能力边界声明（见 3.2） |
| 11 | body 无跨技能文件引用 | ✅ | 全部为散文名（反引号），无 ../ 路径；references/ 指针为自目录相对路径，格式合规（文件缺失见第 5 节） |
| 12 | 目录 NNN-kebab-case、无空格大写 | ✅ | `257-social-content` |

**判定**：12 项中 0 项明确违规、2 项灰色地带（第 5、10 项）、10 项合规。根 SKILL.md 是语料 322 个技能中规范化程度最高的一档，与 dossier 的 🟢 评级一致（见第 11 节）。合规风险集中在"Related Skills 死引用"与"Scope 节不完整"两处文本级问题。

---

## 8. 人机感评估

### 8.1 Emoji 审计

全文仅 1 处 emoji（:301，"**Confidence marking** — 🟢 proven format / 🟡 test this / 🔴 depends on your audience"）。该行是本技能 Communication 协议的一部分——它**规定 agent 在输出中用交通灯 emoji 标注建议置信度**。评估：对社交媒体技能而言，emoji 置信度标注与其输出场景（社交帖子本身即 emoji 原生环境）是匹配的设计选择，且 🟢🟡🔴 是功能性符号而非装饰性表情；但按语料规范（308 等技能为零 emoji），在 SKILL.md 正文保留 emoji 仍需注意两点：其一，agent 照抄该行时会把 emoji 学进输出，需确认这是产品意图；其二，若后续评测对输出做纯文本解析，emoji 可能干扰正则判定。判定为"设计使然、可保留、需知情"（🟢-5）。

### 8.2 全大写喊叫

无全大写段落。CTAs（:93、:161、:289）为惯用缩写，不构成喊叫。全文无强调性大写滥用。

### 8.3 人格/语气

语气为专业教练式："The first line determines whether someone will read the rest."（:79）、"Stop [common mistake]. Do this instead:"（:94）、"Add new insight, not just 'Great post!'"（:163）——指令清晰、经验性强，符合 Process 技能该有的实操感。Proactive Triggers 采用"症状 → 立即行动"结构，符合规范 §3.4 "anti-patterns over generic advice"导向。首句 "You are an expert social media strategist. Your goal is to help create engaging content..."（:8）是第二人称 Persona 开场——SKILL-SPEC 的语音禁令只针对 description，body 中的角色定位句是语料常见写法（196 的旧版审查曾将此类判违规，308 的现行判例认为 body 第二人称允许且更适合执行，本文从后者），且后续正文立即转入指令式，无角色扮演失控。

### 8.4 人机边界

无拟人化、无对话性内容；技能是纯知识/流程载体，人机分工清晰——dossier 亦评价 257"人机分工清晰"（模型产出内容，用户提供品牌/受众上下文并决策）。"The algorithm loves replies" 一类的拟人口吻在本文中不存在，边界干净。

### 8.5 代词分析

正文大量使用第二人称 "you/your"（"your niche"、"your audience"、"your comment"），是社交内容技能的合理语域；description 中无任何代词问题。无第一人称（"I/we"）残留。

### 8.6 表格使用评估

body 共 5 张表格：平台速查表（:41-48）、支柱配比表（:58-64）、博客→社交复用表（:111-117）、周历模板表（:133-139）、交付物表（:284-290）。评估：5 张表格全部承载真正的结构化数据（映射关系、配比数值、格式清单、交付定义），无一装饰性表格，符合规范 §3.4 "decision trees over prose"的导向。其中平台速查表与支柱配比表是全技能信息密度最高的部分，用表格是正确的选择。唯一的组织瑕疵是复用表的两组重复平台行（4.2 问题 7）。5 表/311 行不构成过度表格化。

---

## 9. 可执行性评估

### 9.1 独立可执行性：9/10

本技能是语料中最接近"零依赖"的一档：全部知识内联在正文，无任何脚本、命令、外部工具调用指令。分项判断：

- 上下文收集（Before Creating Content）：可执行，唯一的外部依赖是**条件性**读取 `.claude/product-marketing-context.md`（若存在才读，:13），这是语料营销族技能的既有约定（203 技能专门负责创建该文件），依赖成立且有出处。
- 钩子、支柱、复用、日历、互动、分析、排期：全部为纯知识/模板，直接可用。
- 逆向工程：6 步全手工流程，直接可用。
- Output Artifacts 五类交付物：除 "LinkedIn 串推"与 "data 钩子"两个定义缺口（见 4.2 问题 1、2）外，均可直接按承诺产出。

扣 1 分的原因：2 处 references/ 指针悬空（post 模板内容真实缺失）+ 日历模板与承诺字段不一致（4.2 问题 3），agent 照承诺产出时会遇到两处"技能承诺了但技能没给"的缺口。

### 9.2 分步可操作性

每一步都有可对照的操作对象：Context 四类问题可直接提问；支柱配比表可套用；12 条钩子公式可直接填充；复用工作流 5 步编号清晰；日历模板可直接生成；互动日常按分钟标注（5/15/5/5 分钟）；分析节按症状给出行动列表。Proactive Triggers 5 条是"无须用户要求即主动触发"的指令，是可操作性最强的部分。

### 9.3 工具依赖

零工具依赖（无 Bash/WebSearch/脚本）。唯一环境依赖是用户的品牌上下文文件（可选）。对比 308（5 脚本悬空 + WebSearch 依赖），257 在可执行性上无技术债。

---

## 10. SCORING.yaml 交叉参考

### 10.1 标准覆盖 vs SKILL.md

13 条标准（SCOPE 1 + PROCESS 5 + DECISION 1 + OUTPUT 5 + NEGATIVE 1）与 `total_items: 13` 一致，全部为 `judge: llm`。逐条映射：SCOPE-01 → description 关键词（7 个触发词逐一对应）；CTX-01 → Before Creating Content（含 product-marketing-context.md 条件读取）；PLT-01 → Platform Quick Reference；PLL-01 → Content Pillars；CAL-01 → Weekly Planning Template；HOO-01 → Hook Formulas；REP-01 → Content Repurposing System；THR-01 → Output Artifacts 串推行；ENG-01 → Engagement Strategy；OPT-01 → Analytics & Optimization；SCH-01 → Scheduling Best Practices；TRG-01 → Proactive Triggers（5 条与判定问题 5 个旗标逐一对应，是全语料中技能与判定项咬合最紧的触发类标准之一）；COM-01 → Communication。**13 条标准 ↔ 13 个正文节，映射质量高**——每一条都能指到正文的具体行。

问题集中四点：

1. **HOO-01 与正文不一致**：判定问题中的 "data formulas" 在 Hook Formulas 节无定义（4.2 问题 1），agent 被要求产出技能未教的东西，判定项存在"无法按技能内容达标"的失真风险。
2. **CAL-01 与正文模板不一致**：判定要求日历含 topic/pillar 两字段，正文模板没有（4.2 问题 3），agent 必须自行扩展模板才能过项，标准与内容倒挂。
3. **全 LLM 判定、零脚本判定**：check.py 的 13 条全部走 LLM judge，无任何 `output_contains`/`tool_log_contains` 的自动化兜底。对 257 这种"输出形态高度结构化"（日历表、钩子首行、串推结构）的技能，至少 CAL-01/HOO-01/THR-01 三条可以用 `output_contains` 正则做初筛，把 LLM 判定留给语义项（COM-01/OPT-01），可显著降低评测成本与判定方差（详见第 13 节 🟢-6）。
4. **覆盖缺口**：Content Ideas by Situation、Reverse Engineering Viral Content、Task-Specific Questions、Batching Strategy 四个正文节没有任何判定项覆盖——其中 Batching 与 Reverse Engineering 是技能中较为独特的方法论内容，未被测量。属可接受的覆盖取舍（13 项已覆盖主干），但值得记录。

### 10.2 关键失败分析

- **CF-01**（跨平台雷同文案 → cap_to_0）：与正文 Platform Quick Reference + Communication 的"平台原生"要求一致，合理。
- **CF-02**（无钩子首行 → cap_to_0）：与正文 "Always include a hook as the first element. Never deliver copy body without it."（:303）及 HOO-01 一致，合理。
- **CF-03**（促销主导无支柱配比 **或** 未收集受众/声音上下文 → cap_to_0）：两个触发条件（无支柱平衡 或 无上下文）以 OR 复合在同一 CF 中，语义上"任一"即封顶。宽严设计可议（如"未收集上下文"对纯帖子创作任务是否过严），且 CF-03 的上下文部分与 CTX-01 存在判定重叠（同一行为被 CF 和常规标准双重计分）。建议拆分或明确优先序（详见第 13 节 🟢-7）。

三个 CF 均与正文规则直接对应，无"正文没写却拿来判死"的悬空标准——这一点与 308（CF 依赖缺失脚本）相比是干净的。

---

## 11. 已知问题汇总（skill-dossier）

skill-dossier.md 存在于 `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md`，257 的记录位于 Batch 251-275 摘要（:1023-1027），无单独条目、无已知缺陷登记。摘要对 257 的判定：

- **逻辑**: "257 调研→平台→内容→钩子→排期→数据链路完整" — 与本 REVIEW 第 4.1 节的链路分析一致。
- **人机感**: "257 人机分工清晰" — 与本 REVIEW 第 8.4 节一致。
- **合规**: "🟢 257/258/261 三节齐备" — 与本 REVIEW 第 3.2/7 节基本一致（dossier 将 Related Skills 计入 Scope，故为 🟢；本 REVIEW 按 12 项清单严格口径判第 10 项 ⚠，属口径差异而非实质分歧）。
- **总评**: "🟢 257/261 边界清晰" — 与本 REVIEW 的总体评级方向一致。

dossier 未登记 257 的任何 🔴/🟡 缺陷。本 REVIEW 发现的 2 处 🔴（references 悬空、data 钩子矛盾）与 3 个死路由属于 dossier 摘要粒度未覆盖的细节，本节已知问题由此 REVIEW 第 4、5、10 节自行承载。

---

## 12. 综合评分

| 维度 | 权重 | 得分(/10) | 加权 | 依据摘要 |
|------|------|-----------|------|----------|
| Frontmatter | 10% | 9.0 | 0.90 | name/description 合规优良、无跨技能路由；裸标量 + 非标准触发句式两处小瑕疵 |
| Body | 10% | 8.5 | 0.85 | 14 节知识密度高、5 表全有效；311 行超 Process 目标线 55%；复用表重复行 |
| Logic | 20% | 7.5 | 1.50 | 链路完整、触发/通信与正文咬合佳；data 钩子悬空、日历模板缺字段、问题节重复 |
| References | 15% | 4.5 | 0.675 | 零参考文件 + 2 处悬空指针；8 个相关技能引用 3 死 1 名不符（部分为语料级漂移） |
| Grammar | 10% | 9.0 | 0.90 | 拼写语法干净；LinkedIn"hook tweet"术语错配 |
| Compliance | 15% | 9.0 | 1.35 | 12 项 10✅2⚠，0 违规；无嵌套副本、无禁用键、dossier 🟢 |
| Human-feel | 10% | 9.0 | 0.90 | 教练式专业语气、人机边界清晰；1 处功能性置信度 emoji（设计使然） |
| Executability | 10% | 9.0 | 0.90 | 零工具依赖、全内联知识，语料顶级；仅 2 处增强性指针悬空 |
| **合计** | 100% | — | **7.975 → 79.8/100** | **🟡B+（上界，接近 🟢A- 门槛）** |

79.8/100，判定为 **🟡B+**。与 308（64.5/🟠C）相比，257 是"底子干净、欠债少"的一类：无目录级违规、无脚本悬空、无 12 项清单硬违规，扣分集中在 References（2 处悬空指针 + 3 死引用）与 Logic（data 钩子矛盾、日历模板缺字段）两个可快速修复的文本级问题。若补齐 2 个 references/ 文件、修正 data 钩子与 Related Skills 死引用、补显式 Scope 节，可预期升至 88-90（🟢A- 档），逼近语料第一梯队（258 法律类 90+ 档）。

---

## 13. 修复建议（重点章节）

### 🔴 致命缺陷

**F-1 references/ 两处悬空指针（最高优先级）**
- 位置：SKILL.md:101（`references/post-templates.md`）、:255（`references/reverse-engineering.md`）
- 现状：目录无 references/ 子目录，2 处指针指向不存在的文件。post-templates 内容（发帖模板库）是真实缺口——钩子公式内联了，但"完整 post 模板"从未给出；reverse-engineering 则仅差深度扩展。
- 修复：二选一。方案 A（推荐）：补建 `references/` 目录与两个文件——`post-templates.md` 写 5 类发帖模板（公告型/教育型/故事型/观点型/互动型，各含完整 post 骨架与示例，呼应 4 类钩子公式 + 交付物承诺）；`reverse-engineering.md` 把 6 步方法论展开（数据收集表、模式编码模板、playbook 文档结构）。方案 B（轻量）：若暂不补内容，删掉两处 "See references/..." 句子（:101、:255），使正文零悬空。
- 后果：方案 A 补齐技能唯一的深度缺口、交付承诺全部兑现；方案 B 至少消除悬空引用。两条路径均建议执行其一，成本 1-1.5 小时。

**F-2 "data" 钩子变体悬空（正文 vs 交付承诺 vs 评测标准三处不一致）**
- 位置：SKILL.md:289（"5 hook variants (curiosity, story, value, contrarian, data)"）；SCORING.yaml:53-57（HOO-01 question 含 "data formulas"）
- 现状：Hook Formulas 节只定义 4 类（curiosity/story/value/contrarian，:81-99），"data" 类无定义无示例；但交付物承诺 5 种变体、HOO-01 判定问题也要求 "data formulas"。agent 按技能内容产不出 data 类钩子。
- 修复：推荐在 Hook Formulas 节补 `### Data Hooks`（1-2 条公式与示例，如 "X% of [audience] do [behavior] — the data behind why"、"The numbers changed my mind: [stat] → [stat]"），使 5 变体承诺兑现；若不想扩正文，则把 :289 改为 "4 hook variants (curiosity, story, value, contrarian)" 并把 SCORING HOO-01 的 "data" 一词同步删除。
- 后果：正文、交付承诺、评测标准三处对齐，消除判定失真。

### 🟡 重要缺陷

**I-1 修正 LinkedIn 串推的 X 术语错配 + 定义 "formatting notes"**
- 位置：SKILL.md:290；SCORING.yaml:67-73（THR-01）
- 修复：改为 "Full thread structure: hook post, 5-8 body posts, CTA post, with formatting notes (carousel/document structure for LinkedIn)"；SCORING THR-01 的 question/evidence 同步；若保留 "formatting notes" 概念，在 Output Artifacts 表下补一行说明其含义（如"分段长度、换行节奏、emoji 密度、hashtag 位置"）。
- 后果：消除术语错配与未定义概念依赖，THR-01 判定有据可依。

**I-2 修正 Related Skills 死引用与名字不符（3 死 1 误）**
- 位置：SKILL.md:309、:311、:313、:316
- 修复：`marketing-context` → 改为 `product-marketing-context`（语料实际名 203-product-marketing-context，且其 description 明确创建 `.claude/product-marketing-context.md`，与 :13 的读取约定互证）；`content-strategy`、`marketing-ideas`、`launch-strategy` 三个语料中不存在的技能——若语料规划补建则保留，否则改写为散文描述（如 "topics-first planning: see the Pillar Development Questions in this skill"）或直接删除条目。注意这三个名字在语料中另有 20/4/4 处引用，属语料级漂移，若本轮不做语料级治理，至少 257 自身应消除死路由。
- 后果：agent 不再按字面路由到不存在的技能。

**I-3 日历模板补齐 topic/pillar 字段（CAL-01 倒挂修复）**
- 位置：SKILL.md:133-139（Weekly Planning Template）
- 修复：把表头从 `| Day | LinkedIn | Twitter/X | Instagram |` 扩展为 `| Day | Platform | Format | Pillar | Topic | Evergreen/Timely |`（与 Output Artifacts :287 承诺的 6 要素完全对齐），或保留平台列布局、为每格增加 pillar/topic 子标注。
- 后果：CAL-01 判定要求的字段在模板中落地，标准与内容倒挂消除。

**I-4 合并 Task-Specific Questions 与 Before Creating Content 的重复**
- 位置：SKILL.md:259-266
- 修复：删去 :263、:265、:266 三条重复问题，保留独有的 3 条（平台焦点、当前频率、历史表现），并在该节加一句 "Context questions already covered in Before Creating Content are not repeated here"。
- 后果：正文去重约 20 行（同时向 Process 目标线 200 行靠拢）。

**I-5 处理 WhatsApp 孤儿行**
- 位置：SKILL.md:48
- 修复：二选一——删除该行（description 未承诺 WhatsApp，删行最省）；或在 Output Artifacts 或 Scheduling 节补一句 WhatsApp 落地指引（如 "WhatsApp: message-based broadcasts, use Status as daily content, best for community support"）。
- 后果：消除信息孤行。

**I-6 Body 压缩至 ~200 行目标线**
- 位置：SKILL.md 整体（当前 311 行）
- 修复：执行 I-4 去重（-20 行）+ 合并复用表重复平台行（I-7，-2 行）+ 收紧 Before Creating Content 的段落措辞（-10 行），可降至 ~280 行；若坚持 Process 目标线，进一步把 Content Ideas by Situation 或 Hook 示例压入 references/（与 F-1 方案 A 联动）。
- 后果：行数合规从"超 55%"降至"超 40%"以内；深度内容迁移至 references/ 后，SKILL.md 更符合"主流程 + 引用"的结构。
- 注意：行数超目标不是硬违规（硬上限 600），此条为优化项而非强制项。

**I-7 合并复用表格的重复平台行**
- 位置：SKILL.md:111-117
- 修复：合并为 `| LinkedIn | Key insight + link in comments; Carousel of main points |`、`| Instagram | Carousel with visuals; Reel summarizing the post |`，保持 5 平台 5 行。
- 后果：表格组织与速查表/周历表风格统一。

**I-8 补显式 Scope/Limitations 节（12 项清单第 10 项 ⚠ 转 ✅）**
- 位置：建议插在 `## Related Skills`（:307）之前
- 修复：声明三件事——本技能不代发内容、不接入任何平台 API、不替代账号运营；本技能产出建议与模板，发布与投放决策由用户执行；跨技能边界以 Related Skills 的 NOT-for 路由为准（把路由信息在此以范围声明形式复述一遍，符合规范 §2.5）。
- 后果：Scope 职责归位，第 10 项合规，dossier 的 🟢 评级获得文本级支撑。

**I-9 修复 check.py 的 set_agent_output 覆盖潜伏 bug**
- 位置：check.py:18 与 :54-56
- 修复：check() 内 `set_agent_output(agent_output)` 传入的是**路径字符串**，而 main() 已在 :56 用文件内容设置过——check() 的调用会用路径覆盖内容。当前 13 条全为 llm 判定、无 output_* 检查，所以无实害，但若按 🟢-6 补充 script 判定项，此 bug 会立即生效（output_contains 将匹配路径字符串）。修复：删除 check() 内该行，或改为只在 main() 设置一次。
- 后果：消除潜伏缺陷，为 🟢-6 铺路。

### 🟢 优化建议

**G-1** description 句 1（SKILL.md:3）改为标准触发句式："**Use when** the user wants help creating, scheduling, or optimizing social media content..."，第 5 项从"附观察"变为完全逐字合规。

**G-2** description 加双引号包裹（与语料主流一致），消除未来编辑引入冒号/`#` 时的静默 YAML 解析风险。

**G-3** 平台速查表（:41-48）每行补充 "Secondary Format" 或 "Best Posting Time" 一列可增强信息密度——可选，当前表已够用。

**G-4** 在 Proactive Triggers（:274-278）附近加一句显式说明："Frequencies in the Quick Reference are per-platform maxima; they do not multiply across platforms"，把 4.2 问题 5 的隐含前提显式化。

**G-5** 置信度 emoji（:301）保持现状（功能性设计、匹配社交场景），但建议在 Communication 节加一句："Use these markers only in advice, not in the social copy itself"，防止 agent 把 🟢🟡🔴 写进交付的帖子正文。

**G-6** 为 SCORING 增加 2-3 条 `judge: script` 判定（用 `output_contains`），如 CAL-01（输出含 "Evergreen"/"Timely" 字样）、HOO-01（输出首行含 "I"/"How"/"Stop"/"Unpopular" 等钩子句式）、THR-01（输出含 "hook"/"CTA" 结构标记），把高结构化项从 LLM 判定中释放，降低评测成本与方差。注意先修 I-9。

**G-7** 拆分 CF-03 的 OR 复合（SCORING.yaml:128-130）：拆为 CF-03a（促销主导无支柱平衡）与 CF-03b（未收集受众/声音上下文），各自独立 cap_to_0 或调整为降级计分（cap 而非清零），消除与 CTX-01 的判定重叠与"任一触发即封顶"的过严风险。

**G-8** check.py 的 CRLF 行尾改为 LF，与目录内其他文件统一（一行 `sed -i 's/\r$//' check.py` 即可）。

**修复工作量估计**：文本级修复（F-2、I-1~I-5、I-8、G-1~G-5、G-7、G-8）约 1.5-2 小时；references/ 两文件写作（F-1 方案 A）约 1-1.5 小时；SCORING 增加 script 判定项（G-6，含 I-9 前置修复）约 30 分钟。总计约 3-4 小时。若只做最低限度修复（F-1 方案 B + F-2 + I-2 + I-3），约 45 分钟即可将评分从 79.8 提升至 ~86（🟢A- 下沿）。

---

## 附录: 审查过程记录

**读取文件清单（全部全文读取，无抽样）**：
1. `D:\SkillIF\skill-experiment\complex-skills\257-social-content\SKILL.md` — 316 行全部
2. `D:\SkillIF\skill-experiment\complex-skills\257-social-content\SCORING.yaml` — 131 行全部
3. `D:\SkillIF\skill-experiment\complex-skills\257-social-content\check.py` — 66 行全部

**辅助核验（非技能目录内文件）**：
- `D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py` — 351 行全部（核对 tool_log_contains/output_contains 语义与 set_agent_output 行为）
- `D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md` — 162 行全部（核对 12 项清单、禁用键、行数目标、§2.4 触发信号清单）
- `D:\SkillIF\skill-experiment\complex-skills\_shared\CHECKER-LIBRARY.md` — 存在性确认
- `C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md` — Batch 251-275 摘要中 257 的条目（:1023-1027）
- 参考格式：`308-x-twitter-growth/REVIEW.md`（417 行，13 节格式模板）、`196-cold-email/REVIEW.md`（43 行，旧版短格式）
- 全语料 322 个技能目录名逐一比对（确认 content-strategy/marketing-ideas/launch-strategy 不存在；确认 203-product-marketing-context 为 marketing-context 的实际名；确认 12 例嵌套副本中 257 无份）

**验证性命令**：`wc -l/-c` 实测三文件行数与字节数；`file` 实测行尾（SKILL.md/SCORING.yaml 为 LF，check.py 为 CRLF）；`python yaml.safe_load` 实测 SKILL.md frontmatter 与 SCORING.yaml 解析（均通过，description 实测 398 字符、裸标量无引号）；grep 统计 references/ 引用 2 处、emoji 出现 1 行（:301）、语料内 content-strategy 20 处/marketing-ideas 4 处/launch-strategy 4 处引用；grep 核对 5 个相关技能 name 字段。

**Quality Gate 自查**：目录内 3 个文件全部提及并完成内容分析 ✅；13 节结构齐全（含附录共 14 部分）✅；正文 400+ 行（远超 300 行要求）✅；修复建议含 file:line 与后果 ✅；表格仅用于清单核对与评分矩阵（必要场景）✅；仅写入 REVIEW.md，未改动任何其他文件 ✅。
