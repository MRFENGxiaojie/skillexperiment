# REVIEW: 239-crafting-effective-readmes

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**审查对象**: `D:\SkillIF\skill-experiment\complex-skills\239-crafting-effective-readmes\`
**对照规范**: `complex-skills\_shared\SKILL-SPEC.md` v1.0
**Skill 类型**: process — 面向受众/项目类型匹配的 README 撰写方法论
**Body 行数**: 77 行（SKILL.md，含 frontmatter 4 行，正文 73 行）
**参考文件数**: 10 个（references/ 5 个 + templates/ 4 个 + 根目录辅助 3 个 + README.md，不含测评件）
**已有 REVIEW**: 无（首次审查）
**本次结论**: 🟡 **B+ (84/100)** — 内容组织有创意（受众×任务矩阵 + 四套差异化模板是真正的知识增量），但存在 2 项规范硬缺口（无 Output Format 节、无 Scope/Limitations 节）与 1 处与评分逻辑冲突的设计矛盾（Essential Sections 与 Config 模板、CF-01 的互相打架），属于"结构问题拖累好内容"的类型

> 本审查通读目录下全部 16 个文件（SKILL.md / README.md / SCORING.yaml / check.py /
> section-checklist.md / style-guide.md / using-references.md / references/ 5 个 /
> templates/ 4 个），并交叉核对了 `_shared/checker.py`（`tool_log_contains` 等函数实现）、
> `_shared/SKILL-SPEC.md`、memory 中 skill-dossier.md 的批次摘要，以及与
> `complex-skills-no-trigger\239-crafting-effective-readmes\` 的对照 diff。
> 所有引用以 `SKILL.md L12`（行号）格式标注。

---

## 1. 目录全量清单

```
239-crafting-effective-readmes/
├── SKILL.md                          ( 77 行)  ← 主文件（frontmatter 4 + body 73）
├── README.md                         (176 行)  ← 面向人类的技能说明（与 SKILL.md 大量重复）
├── SCORING.yaml                      ( 93 行)  ← 测评标准（9 项：scope 2 / process 4 / output 2 / negative 1）
├── check.py                          ( 68 行)  ← 测评脚本（实现 2 条 script 判据）
├── section-checklist.md              ( 17 行)  ← 按项目类型的章节清单
├── style-guide.md                    ( 13 行)  ← 常见错误 + 指向 writing-clearly-and-concisely
├── using-references.md               ( 35 行)  ← 参考材料使用指南
├── references/
│   ├── art-of-readme.md              (536 行)  ← 第三方文章（hackergrrl，哲学向）
│   ├── make-a-readme.md              (119 行)  ← 第三方文章（Danny Guo / makeareadme.com）
│   ├── standard-readme-spec.md       (242 行)  ← 第三方规范（RichardLitt / standard-readme）
│   ├── standard-readme-example-minimal.md (21 行) ← 最小合规示例
│   └── standard-readme-example-maximal.md (68 行) ← 全功能示例
└── templates/
    ├── oss.md                        ( 77 行)  ← 开源项目模板
    ├── personal.md                   ( 51 行)  ← 个人/作品集模板
    ├── internal.md                   (106 行)  ← 内部/团队项目模板
    └── xdg-config.md                 ( 71 行)  ← 配置目录模板
```

文件结构总评：**分层设计合理**——SKILL.md 是流程编排（识别任务→提问→选模板→成稿→追问），
templates/ 是产物骨架，references/ 是深度材料，using-references.md 明确告诫"不要一次加载全部
参考"。这个 progressive disclosure 结构与 298-writing-skills 提倡的模式一致，是加分项。
但存在三个结构性问题：(a) SKILL.md 末尾的 `## References`（L74-78）只索引了 3 个根目录辅助
文件，**完全没有提及 references/ 目录**——art-of-readme.md、make-a-readme.md、
standard-readme-spec.md 只有读完 using-references.md 才能被发现，发现链多一跳；(b) README.md
与 SKILL.md 是同一内容的两个版本（详见 §4 P-2），存在双份真相漂移风险；(c) 测评件
（SCORING.yaml / check.py）与技能件混居同一目录，README.md 的 Directory Structure 清单未收录
它们（可接受，属实验约定，但 README 未加"另含测评件"说明）。

对照 `complex-skills-no-trigger\239-crafting-effective-readmes\` 存在同构目录，SKILL.md 仅
description 一行不同（详见 §11），SCORING.yaml 完全相同。

---

## 2. Frontmatter 审查

### 2.1 name

```
name: crafting-effective-readmes
```
- 全小写+连字符：✅
- ≤64 字符：✅（27 字符）
- 匹配目录名：⚠️ 目录为 `239-crafting-effective-readmes`，name 为 `crafting-effective-readmes`。
  按 SkillIF 实验约定（NNN- 为序号前缀，name 取 slug 部分，与 298-writing-skills 同款处理），
  判为可接受；若按"严格匹配目录"字面规则则不一致，需在实验说明中固定此约定。

### 2.2 description（逐句分析）

原文（约 214 字符，含 `description: ` 前缀约 228 字符）：

```
README writing methodology with audience-matched templates. Use when writing or improving README files. Not all READMEs are the same — provides templates and guidance matched to your audience and project type.
```

逐句拆解：

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "README writing methodology with audience-matched templates." | WHAT（方法+载体） | ✅ |
| "Use when writing or improving README files." | WHEN（触发场景） | ⚠️ 见下 |
| "Not all READMEs are the same — provides templates and guidance matched to your audience and project type." | WHAT 补充（受众匹配） | ⚠️ 见下 |

**问题 1（触发短语缺主语）**: SKILL-SPEC §2.4 列出的五个触发信号形式为 "Use when the user..."、
"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."。
本 description 的 "Use when writing or improving README files" 缺 "the user" 主语，按 §5 清单
第 5 项字面判为部分合规（与 054-oss-review L3 的 "Use when reviewing a manifest..." 同型偏差）。
语义上它是合格的触发信号，功能无碍，仅措辞级偏差。

**问题 2（第二句语法碎片）**: "Not all READMEs are the same — provides templates and guidance..."。
"provides" 缺主语，是悬挂式碎片句（隐含主语应为 skill 本身）。em dash 后接动词短语在英文中
不算致命，但按严格语法规范是残缺句，且这段文字恰好是 skill 面向检索系统的门面，建议补主语
（见 §13 F-12）。

**第三人称检查**: 全文无第一/第二人称代词（"your audience" 出现在"matched to your audience"，
严格说出现了第二人称物主代词 your——但此处为描述受众的泛指用法，类似 054 的判定惯例，语气
仍是第三人称描述 skill 而非对话用户，判为可接受）。✅

**字符数**: 约 214 字符 ≤1024。✅

**关键词覆盖**: README / writing / improving / templates / audience / project type——覆盖了
领域核心词与动作动词，无跨技能路由。✅

### 2.3 其他 frontmatter 字段

仅 `name`、`description` 两个字段。无 allowed-tools / argument-hint / user-invocable / model /
paths / disable-model-invocation，也无任何 §1.3 禁用字段（metadata / version / triggers 等）。
✅（可选字段不出现不违规。）

### 2.4 Frontmatter 语法

YAML 分隔符 `---` 配对正确，无缩进错误；description 内 em dash（—）与句点正常，无引号冲突。✅

---

## 3. Body 结构分析

### 3.1 段落清单（SKILL.md，共 6 个一级/二级节）

| 节 | 行号 | 内容 |
|----|------|------|
| # Crafting Effective READMEs | L6 | H1 标题 |
| ## Overview | L8-12 | 核心原则："READMEs answer questions your audience will have" + 恒问句 |
| ## Process | L14-53 | Step 1 任务识别（L16-25）→ Step 2 任务特定提问（L27-49）→ Step 3 成稿后追问（L51-53） |
| ## Project Types | L55-64 | 四类项目 × 受众 × 关键章节 × 模板路径 表格 |
| ## Essential Sections (All Types) | L66-72 | 所有类型至少三节：Name / Description / Usage |
| ## References | L74-78 | 3 个根目录辅助文件索引 |

### 3.2 必需章节检查（SKILL-SPEC §3.1：Workflow/Process + Output Format + Scope/Limitations）

| 必需项 | 状态 | 说明 |
|--------|:----:|------|
| Workflow/Process | ✅ | `## Process`（L14-53）三步骤完整：Step 1 任务识别（Create/Add/Update/Review 四分类表 L20-25）、Step 2 按任务类型给出针对性提问清单（L29-49）、Step 3 收尾追问（L53）。流程为咨询式：问清任务→问清上下文→选模板→成稿→追问遗漏 |
| Output Format | ❌ | **无任何输出格式节**。交付物（README.md 文件、写入项目根目录、文件名与位置、语言、内容结构）从未被明文定义。"输出长什么样"只能从 templates/ 四个文件反推——模板承担了隐含的输出规格，但 skill 未声明"按所选模板产出 README.md 写入项目根目录"这一最基本的交付协议。agent 可能把产物写到任意位置、用任意文件名、只返回正文而不落盘 |
| Scope/Limitations | ❌ | **无专门节**。全文仅有的范围性表述是 L64 "Don't assume OSS defaults for everything"（这属于流程约束而非范围声明）。以下边界均未成文：不适用非代码项目（数据/设计/文档仓库）、不替代完整文档站点、不负责 README 翻译与 i18n 结构、单次审查而非持续维护、不自动生成徽章/截图等资产 |

**规模**: 77 行（body 73 行）≤ 600 行硬上限 ✅；`pattern: process` 目标 ~200 行，实际 73 行，
**仅达目标的 37%**。对 process 型而言偏薄：SKILL.md 本体几乎不含"怎么写 README"的知识，
所有实质内容都在 templates/ 与 references/ 中，SKILL.md 退化为纯编排页。§3.2 的"目标行数"
是经验值而非硬限，但 73 行意味着执行代理若只加载 SKILL.md（不读任何模板/参考），产出的
README 质量将完全依赖模型先验知识——这与"skill 应携带知识增量"的 §3.4 精神存在张力。

### 3.3 内容委托分析（progressive disclosure 是否符合自己定的规则）

- 委托结构：SKILL.md（编排）→ templates/（骨架，成稿的直接依据）→ references/（深度，按需取用）。
  层级为两层，无跨文件链式委托，符合官方规范 "Keep references one level deep from SKILL.md"。
- **加载顺序明确**：Project Types 表（L59-62）直接把四类任务映射到四个模板路径，using-references.md
  又明确"Templates are your primary tool"并告诫"Don't load all references at once"。执行代理的
  路径是清晰的。
- **缺口**：SKILL.md 的 `## References`（L74-78）只列 3 个辅助文件，references/ 目录完全缺席
  （见 §1）。且 Step 2/3 之后没有任何"如何把提问答案映射进模板章节"的指导——模板里的
  `[占位符]` 就是全部桥梁。对简单 skill 可接受，但结合 Output Format 缺失，成稿环节是整个
  链路上唯一没有显式规格的环节。

---

## 4. 逻辑一致性

链条整体自洽，但存在 1 处**会影响评分的实质矛盾**与若干小错位。逐项核对：

| 检查点 | 判定 | 依据 |
|--------|:----:|------|
| 任务分类表 ↔ SCORING | ✅ | L20-25 四任务（Create/Add/Update/Review）↔ SCOPE-01（L9-13）完全对应 |
| 项目类型表 ↔ 模板路径 | ✅ | L59-62 四类型 ↔ templates/oss|personal|internal|xdg-config.md 四文件一一对应，且 PROC-03 的 script 正则（`templates/(oss\|personal\|internal\|xdg-config)\.md`）覆盖全部四个 |
| 关键章节 ↔ 模板内容 | ✅ | L59 "OSS: Installation, Usage, Contributing, License" ↔ oss.md 确有 Installation/Usage/Contributing/License；L61 "Internal: Setup, Architecture, Runbooks" ↔ internal.md 确有 Local Development Setup/Architecture/Runbooks；L62 "Config: What's here, Why, How to extend, Gotchas" ↔ xdg-config.md 节名逐字对应 |
| Review 任务流程 ↔ PROC-02/CF-03 | ✅ | L45-49（读当前 README、对照 package.json 等项目状态、标记过期节、更新 Last reviewed）↔ PROC-02（L33-38）与 CF-03（L91-93）完全呼应 |
| 收尾追问 ↔ PROC-04 | ✅ | L53 原文 ↔ PROC-04 question（L53-58）逐字一致 |
| 提问清单 ↔ PROC-01 | ✅ | L29-33（项目类型/一句话问题/最短路径/亮点）↔ PROC-01（L24-30）逐项对应 |
| Last reviewed 机制三处一致 | ✅ | L49（Review 流程提更新日期）↔ xdg-config.md L12（`> Last reviewed:` 占位行）↔ section-checklist.md L17（Config 行 "Last Reviewed: Yes"） |

**发现的实质问题**:

- **P-1（矛盾，会直接影响评分）**: `## Essential Sections (All Types)`（L66-72）宣称
  "Every README needs at minimum: Name, Description, Usage"，但 **Config 模板
  （xdg-config.md）没有任何 Usage 节**（节序：What's Here / Why This Setup / How to Extend /
  Dependencies / Gotchas / Sync/Backup / Related）。而 SCORING.yaml 的 **CF-01**
  （L83-85：README 缺 Name/Description/Usage 即 cap_to_0）以此为基准。于是出现三处互相打架：
  (a) SKILL.md 说 Usage 是所有类型的必备节；(b) section-checklist.md L10 说 Config 的
  Usage/Examples 只需 "Brief"；(c) xdg-config.md 模板干脆没有。**最坏情形**：agent 忠实遵循
  Config 模板产出 README → CF-01 触发 cap_to_0，一个合规执行被评分逻辑判死。这是本 skill
  **评测正确性层面最值得修的矛盾**（§13 F-01）。
- **P-2（双份真相）**: README.md（176 行）与 SKILL.md（77 行）描述同一技能。README.md 内容
  更多（含触发短语、对话示例、Best Practices、Common Mistakes、Directory Structure、Related
  Skills），SKILL.md 是其压缩版。两处表述存在可观测的措辞漂移：README.md L59 的收尾追问是
  "Anything else to highlight or include that I might have missed?"，SKILL.md L53 是 "Is there
  anything else to highlight or include that I might have missed?"——SCORING PROC-04 跟随
  SKILL.md 版本，而执行代理若读到 README.md 会拿到不同版本（当前仅是措辞差异，属幸运；
  长期维护下去 Step 内容、模板表都可能各自漂移）。
- **P-3（清单与模板小错位）**: section-checklist.md L11 列 Internal "Usage/Examples: Yes"，
  但 internal.md 无 Usage 节（Running Locally / Runbooks 在功能上等价，但字面无对应）；
  L8 列 OSS "Architecture: Optional"，oss.md 无 Architecture 节；L7 列 OSS "Gotchas/Notes:
  Optional"，oss.md 也无。均为"可选/等价覆盖"级别的小错位，不构成矛盾，但清单宣称的
  推荐项在模板里找不到落点，agent 对照清单选节时会落空。
- **P-4（README.md 内部不一致）**: README.md 的 Reference Materials 节（L88-94）只列 3 个
  参考文件（art-of-readme / make-a-readme / standard-readme-spec），而 Directory Structure 节
  （L164-171）列出了 5 个（含两个 example 文件）。同文件内两处对"参考材料"的计数不一致。
- **P-5（发现链多一跳）**: SKILL.md References 节（L74-78）不含 references/ 索引，深度材料
  依赖"读 using-references.md 再跳转"——若代理只读被显式链接的文件（常见行为），
  art-of-readme.md 等 5 个文件永远不会被加载。

**其余核对**: 无断裂的步骤编号（Step 1/2/3 连续）、无数字矛盾、无跨节冲突。知识量方面，
"受众×任务"矩阵与四套差异化模板是本 skill 的真实知识增量（远超"通用 README 建议"），
符合 §3.4"知识增量 > 冗余"——本段扣分完全来自 P-1。

---

## 5. 参考文件审查（每个文件全文通读）

### 5.1 references/art-of-readme.md（536 行，第三方转载）

- 来源：hackergrrl/art-of-readme，Node 社区经典长文。内容核心：cognitive funneling
  （宽→窄的信息漏斗，L244-288）、"README 是用户不进源码的最后一站"（L174-188）、六个关键
  元素扫描序（Name→One-liner→Usage→API→Installation→License，L191-242）、bonus 清单
  （L436-449）与 11 条 good practices（L313-404）。
- **价值判定**: 高。cognitive funneling 是"先写什么后写什么"的通用理论依据，与 SKILL.md 的
  四模板结构互补。using-references.md L12-14 对该文件的摘要准确（认知漏斗、简洁性）。
- **问题（死链）**: L5-8 列出 [Chinese](README-zh.md)、[Japanese](README-ja-JP.md) 等 7 个
  翻译版链接——在原仓库可解析，但本目录内这些文件**均不存在**，SkillIF 隔离环境下全部 404。
  L475 指向 catb.org 的外部链接正常（外链不在审查范围）。L472-478 的 footnotes 用 HTML
  `<a name>` 锚点，在 Markdown 渲染下可用。

### 5.2 references/make-a-readme.md（119 行，第三方转载）

- 来源：makeareadme.com（Danny Guo）。内容核心：README 101（是什么/为什么/谁/何时/何地/怎么，
  L7-31）+ 12 个建议章节逐节讲解（Name/Description/Badges/Visuals/Installation/Usage/Support/
  Roadmap/Contributing/Authors/License/Project Status，L33-87）+ FAQ + 后续文档建议。
- **价值判定**: 高。是 section-by-section 的实操指南，与 standard-readme-spec.md 互补（一个
  "讲为什么"，一个"讲强制要求"）。using-references.md L20-22 摘要准确（含 "too long is better
  than too short" 引用）。
- **问题**: 无死链。内容纯第三方，无本 skill 定制痕迹。

### 5.3 references/standard-readme-spec.md（242 行，第三方转载）

- 来源：RichardLitt/standard-readme 规范。内容核心：合规 README 的强制要求（文件名、节顺序、
  节标题、链接有效性、代码示例 lint）+ 15 个节的 Required/Optional 状态与 Requirements/
  Suggestions 细分 + Definitions。
- **价值判定**: 高，是全语料库少见的"形式化规格"级参考，与 OSS 模板的合规取向吻合。
- **问题（死链）**: L7 "it's [historically](README.md#background) made for Node and npm projects"
  ——相对路径 `README.md#background` 从 references/ 目录解析应指向
  `references/README.md`，**不存在**（技能根目录的 README.md 在上一层，该写法在原仓库成立，
  移植后失效）。

### 5.4 references/standard-readme-example-minimal.md（21 行）

- 最小合规示例：# Title + Install（空代码块）+ Usage（空代码块）+ Contributing + License。
  忠实于原 spec 仓库的示例文件。
- **价值判定**: 中。展示"合规的最小形态"（无 ToC、无 Badges），与 maximal 对照构成两个极端
  样本，对 agent 理解"合规下界"有用。
- **问题**: 空代码块（L7-8、L11-12 ```` ``` ````）在渲染时是空洞方框，属原文件固有问题；
  占位作者 "Richard McRichface" 是原仓库玩笑，保留无碍。

### 5.5 references/standard-readme-example-maximal.md（68 行）

- 全功能示例：Banner + 6 个 badge + 短/长描述 + ToC + Security/Background/Install/Usage/API/
  Contributing/License 全节 + 附属注释。
- **价值判定**: 中。是全语料库少见的完整标准 README 样本，ToC 写法、badge 组合可直接参考。
- **问题（死链）**: L34 `This module depends upon a knowledge of [Markdown]().`——空链接目标
  （原仓库依赖链接目标，移植时未填充）；L46 残留原仓库的维护者提示
  "The `license` badge image link at the top of this file should be updated with the correct
  `:user` and `:repo`"——这是写给标准仓库维护者的元文本，作为技能参考材料会误导 agent
  以为 badge URL 的 `:user`/`:repo` 写法是正确的填充方式。

### 5.6 templates/oss.md（77 行）— 开源模板

- 结构完整：badges（License/Build/npm 三个 shields 占位）→ About → Features → Installation
  （含 Requirements）→ Usage（含 More Examples）→ Documentation → Contributing（含
  Development Setup/Running Tests）→ Roadmap → Acknowledgments → License。
- **优点**: 三类 badge 覆盖许可/构建/包版本，是 OSS README 的标配；Requirements 子节符合
  make-a-readme.md L55 的建议（novice 友好）；无任何节缺 Key Sections 表中承诺的项。
- **问题（轻微）**: badge URL 中 `[user]/[repo]` 与 `[package-name]` 占位符混用两种语法
  （斜杠路径式与括号式），风格不统一；README 头部的 About 用 2-3 句而非 SKILL.md L71 要求的
  "1-2 句 Description"，小节命名（About vs Description）与 Essential Sections 的用词不一致。

### 5.7 templates/personal.md（51 行）— 个人/作品集模板

- 结构：What This Does → Demo → Tech Stack → Getting Started → How It Works → What I Learned
  → Future Ideas → License。
- **优点**: "平衡未来之你与观众"的定位写进了模板头注释（L4）；What I Learned 节是作品集
  场景的差异化设计，其他三个模板都没有。
- **问题（轻微）**: L13-14 `[Screenshot or demo GIF if visual]` 后无任何说明文字；"Getting
  Started" 承担 Installation 职能但与 section-checklist.md L9 的 "Installation: Yes" 用词
  不一致（等价覆盖，见 §4 P-3）。

### 5.8 templates/internal.md（106 行）— 内部/团队模板

- 结构：Team/On-call 头 → Overview（含 Upstream/Downstream 依赖）→ Local Development Setup
  （Prerequisites / Environment Variables 表 / Running Locally / Running Tests）→ Architecture
  （含 ASCII 图占位与 Key Files 表）→ Deployment（含 Environments 表）→ Runbooks →
  Troubleshooting（Symptom/Cause/Fix）→ Contributing → Related Docs。
- **优点**: 四个模板中信息密度最高、最专业：Environment Variables 表带 "Where to get it"
  列、Runbooks 与 Troubleshooting 的 Symptom/Cause/Fix 结构都是真实的内部运维文档形态，
  属高知识增量内容。
- **问题（轻微）**: 无 Usage 节（见 §4 P-3）；On-call 行用粗体行而非表格，与 Env 表的视觉
  风格略不统一；Deployment 无"回滚"小节（内部服务运维的常见盲点）。

### 5.9 templates/xdg-config.md（71 行）— 配置目录模板

- 结构：Last reviewed 头 → What's Here（Path/Purpose 表）→ Why This Setup → How to Extend
  （编号步骤）→ Dependencies → Gotchas → Sync/Backup → Related。
- **优点**: "The audience is future-you, probably confused."（L6）的定位句是全 skill 最好的
  一句话；Gotchas 节针对"未来之你会困惑什么"设计，How to Extend 的编号步骤是操作导向的。
- **问题（严重，见 P-1）**: **无 Usage 节**，与 SKILL.md L66-72 的"所有类型必备 Usage"矛盾，
  与 SCORING CF-01 的 cap_to_0 逻辑冲突。这是四模板中唯一直接与评分逻辑打架的模板。

### 5.10 section-checklist.md（17 行）— 章节清单

- 11 行 × 4 列的交叉矩阵，是 SKILL.md Project Types 表的细化版。
- **优点**: 一行一节的格式极适合 agent 快速查表；OSS/Personal/Internal/Config 四列的
  Yes/Optional/No/Brief 粒度合理。
- **问题**: 与模板的错位见 §4 P-3；无版本/日期信息，与 SKILL.md 表格的"双份清单"关系未声明
  （SKILL.md L57-62 的表是简化版，两者若漂移将出现四份真相：SKILL.md 表 + checklist +
  README.md L73-86 表 + 模板实际节序）。

### 5.11 style-guide.md（13 行）— 风格指南

- 5 条常见错误（无安装步骤/无示例/文字墙/内容过时/通用语气）+ 指向 writing-clearly-and-concisely。
- **优点**: 每条错误都带一句"为什么"（Never assume / Show don't just tell 等），符合
  §3.4"Anti-patterns over generic advice"。
- **问题（轻微）**: 只有 13 行，5 条错误与 README.md L137-143 的 Common Mistakes 逐条重复
  （双份真相之一）；"写作通则请用另一个 skill"的跨技能引用按 §3.3 允许（散文式名称引用）✅，
  但本 skill 自己的差异化风格规则（受众措辞示例、Config 场景的口语化建议等）完全没有沉淀。

### 5.12 using-references.md（35 行）— 参考使用指南

- 结构：一句话定位（Templates 为主，References 为深度）+ 加载告诫 + 三个参考文件的
  Why/What 摘要 + 两个 example 的用途说明。
- **优点**: "Don't load all references at once" 是 token 效率意识的最佳实践；三个 Why/What
  摘要准确（见 5.1-5.3 核验）。
- **问题（轻微）**: 两个 example 文件只给了单行说明，无"何时看 minimal vs maximal"的判定
  规则（建议：短 README 看 minimal，规范合规看 maximal）。

---

## 6. 语法与格式质量

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 拼写/错字 | ✅ | 全篇未发现拼写错误（含 16 个文件） |
| 病句/断句 | ⚠️ | description 第二句 "Not all READMEs are the same — provides templates..." 为悬挂式碎片句（§2 问题 2）；SKILL.md L10 "Different audiences need different information - an OSS..." 用连字符 `-` 而非 em dash（与 description 的 em dash 风格不一致，且 `-` 在 Markdown 中可被误解析为列表符） |
| Markdown 结构 | ✅ | 各文件表格对齐工整；围栏代码块闭合正确（含空代码块）；`- [ ]` 复选框仅出现在模板占位（合法 GFM） |
| 中英混杂 | ✅ | 全部文件纯英文，无意外语言泄漏 |
| 标点 | ✅ | 正文句号/冒号统一；description 的 em dash 使用正确（虽然紧跟碎片句） |
| 标题大小写 | ✅ | "Crafting Effective READMEs" 等标题均为规范 Title Case；模板内 "### Running Tests" 等一致 |
| 占位符残留 | ⚠️ | 模板 `[占位符]` 均为有意占位 ✅；但 maximal 示例 L46 的维护者元文本、L34 的空链接 `[Markdown]()` 属于从原仓库带进来的"半成品残留" |
| 编码 | ✅ | UTF-8 无 BOM 问题；em dash / ✅ / box-drawing 注释字符（SCORING.yaml L6 `──`）均正常 |

**结论**: 语法质量整体良好，扣分集中在 description 碎片句、L10 连字符风格、两处第三方
残留。远好于语料库中下游水平，但距 054 那种"无可挑剔"有一两处差距。

---

## 7. 规范合规性（12 项逐条对照）

按 SKILL-SPEC.md §5（L148-161）逐项核对：

| # | 检查项 | 判定 | 依据 |
|---|--------|:----:|------|
| 1 | name 小写+连字符、≤64、匹配目录 | ✅ | SKILL.md L2 `crafting-effective-readmes` ↔ 目录 `239-crafting-effective-readmes`（NNN 前缀约定，同 298 判例） |
| 2 | description 第三人称、WHAT+WHEN+KEYWORDS、≤1024 | ✅ | L3，约 214 字符；WHAT（方法论+模板）、WHEN（写作/改进 README）、KEYWORDS（README/templates/audience）齐备 |
| 3 | description 无祈使/第一/第二人称开头 | ✅ | L3 以名词短语 "README writing methodology..." 开头 |
| 4 | description 无跨技能路由 | ✅ | L3 无 "NOT for X, use Y" |
| 5 | description 含触发信号短语 | ⚠️ | "Use when writing or improving README files"——语义为触发语，但字面缺 §2.4 模板的 "the user"（同 054-oss-review L3 判例） |
| 6 | frontmatter 无禁用键 | ✅ | L1-4 仅 name/description |
| 7 | body ≤600 行 | ✅ | 77 行（body 73） |
| 8 | 有 workflow/process 节 | ✅ | L14 `## Process`（三步骤编号完整） |
| 9 | 有 output format 节 | ❌ | 无；交付物规格完全缺席，仅模板隐含（§3.2） |
| 10 | 有 scope/limitations 节 | ❌ | 无专门节；唯一范围性表述 L64 是流程约束而非边界声明（§3.2） |
| 11 | 无跨技能文件引用 | ✅ | 全文无 `../other-skill/` 路径；writing-clearly-and-concisely 仅以散文名称提及（style-guide.md L13、README.md L176） |
| 12 | 目录 NNN-kebab-case、无空格大写 | ✅ | `239-crafting-effective-readmes` |

**合计**: 8 项 ✅ / 2 项 ⚠️（5、11 中的 11 实为 ✅，故 ⚠️ 仅 5）/ **2 项 ❌（9、10）**。
即：**8 ✅ / 1 ⚠️ / 2 ❌**（第 11 项复核为 ✅，上表判定一致）。

与 dossier 批次摘要（L1015：239 🟡 "缺 scope/output 节"）**完全一致**——这证实了 dossier
的批量判断准确。本审查在 dossier 基础上新增的发现集中在：P-1 的 CF-01 评分冲突、OUT-01 的
弱判别（§9）、references 死链（§5）、description 触发短语（§2）。

---

## 8. 人机感评估

| 维度 | 评价 |
|------|------|
| 语气 | 咨询顾问式：全篇以问句驱动（L12 恒问句、L18 任务问句、L29-49 提问清单、L53 收尾追问），无营销腔、无填充语 |
| emoji | 全文无 emoji（含模板与参考），✅ 符合审查维度 3 |
| 用户交互设计 | 亮点：(a) 每个提问都有精确到词的话术，agent 可直接引用（"What README task are you working on?"）；(b) 四类任务的提问清单互不混淆（新建问项目类型/一句话问题/最短路径/亮点；更新问改了什么/读现状/给编辑建议）；(c) L64 "Ask the user if unclear. Don't assume OSS defaults" 把"受众不可得时怎么办"决策权交还用户——与 CF-02 呼应，是全 skill 人机设计最好的句子；(d) README.md L99-126 给了三段对话示例，人类读者一眼明白交互形态 |
| 人机边界 | 清晰：skill 负责提问与组织，内容取舍权在用户（L64、L53 追问）；无越界承诺（未声称"写出完美 README"，只声称"匹配受众的方法论"） |
| 机器感/死板度 | 轻微：提问清单偏"表单感"（四类任务的固定问题），对"用户答非所问时如何追问/如何判断项目类型边界（如既是 OSS 又是内部工具）"无引导。整体仍属自然 |
| 收尾交互 | L53 恒追问 "anything else to highlight or include" 是低姿态收尾，符合输出型技能惯例；但无"下一步"引导（如 Review 完成后建议更新 Last reviewed 日期、Create 完成后建议跑一次 markdownlint），收尾略单薄 |

**结论**: 人机感良好（咨询式提问 + 反假设立场 + 无 emoji 无 persona），处于语料库中上水平；
短板是"表单感"提问与单薄收尾，均不构成实质问题。

---

## 9. 可执行性评估

**评测脚本侧（check.py，68 行）**:

- 入口协议 `python check.py <workspace> <tool_log> <agent_output>`（L3）清晰；main() 正确处理
  agent_output 为文件路径的情形（L57-59），且 check() 内也做了 `os.path.exists` 的
  is_path 防御（L25-29，与 main() 职责重叠，属冗余但无害）。
- 2 条 script 判据实现与 SCORING.yaml 逐字一致：
  - PROC-03：`tool_log_contains("templates/(oss|personal|internal|xdg-config)\\.md")`
    （check.py L36 ↔ SCORING.yaml L42-46）——**模式串正确**，Python 源码中 `\\.md` 经字符串
    转义后为 `\.md`，正则匹配字面点号 ✅。
  - OUT-01：`tool_log_contains("#+ (Description|Usage)")`（check.py L40 ↔ SCORING.yaml L58-63）。
- 依赖 `_shared/checker.py` 已核实存在；用到的 3 个函数 `set_tool_log_path`（L224）、
  `tool_log_contains`（L259）、`set_agent_output`（L333）全部定义且签名匹配。**可运行性 ✅**。

**check.py 的两个实质缺陷**:

- **D-1（OUT-01 弱判别，误报方向）**: `tool_log_contains` 的实现是 `json.dumps(entry)` 后
  `re.search`（checker.py L242-250）——它搜索**整条工具日志记录的 JSON 序列化全文**，包括
  Read 调用返回的文件内容。本 skill 里存在多个"读了就满足 OUT-01"的文件：README.md L96
  `## Usage Examples`、templates/oss.md L36 `## Usage` 都命中 `#+ (Description|Usage)`。
  即 agent 只读 README.md（概率不低，它是目录里唯一的引导性文档）就通过 OUT-01，**最终产物
  完全没有 Description/Usage 章节也能得分**。CF-01 虽把"缺必需节"cap_to_0，但 CF-01 是
  llm 判据（SCORING.yaml L82-85 无 judge 字段，按惯例归 llm），脚本层没有任何防护。
- **D-2（OUT-01 漏报方向）**: 若 agent 写出的 README 用同义标题（如 "## What it does" /
  "## How to use"），OUT-01 恒 False，即便内容完全达标。正向核对时只能靠 llm 判据兜底。
- 次要项：`workspace` 参数全程未用（L24/L60）；import 了 15 个 checker 函数实际只用 3 个
  （L12-20），11 个为死导入。

**技能体侧（SKILL.md）**:

- 执行链：读 SKILL.md → 问任务类型 → 问提问清单 → 按 Project Types 表读对应模板 → 成稿 →
  追问。链条短、无外部依赖、无插件路径、无环境前置条件——**隔离评测环境可完整执行 ✅**
  （对比 054 的外部插件路径依赖，本 skill 此维度先天干净）。
- 风险点：(a) **Output Format 缺失**意味着 agent 对"交付物写哪、叫什么、什么形态"零约束，
  不同 agent 可能产出正文回复、`output.md`、任意路径的 README——产物可测性低；(b) Config
  任务 + CF-01 的评分陷阱（§4 P-1）在隔离评测中会真实发生（Config 是四类型之一，测试用例
  覆盖到它就触发）；(c) PROC-03 的正则要求 tool log 出现模板路径——若 agent 不读模板而是
  凭 SKILL.md 表格里的"关键章节"自己写（表格已给出 Key Sections），PROC-03 会失败，即使
  产物正确（评测侧将"必须读过模板文件"设为硬性过程证据，属偏严设计，对忠实遵循 L64
  "Ask the user if unclear" 的 agent 而言是额外负担）。

**结论**: check.py 可运行性 ✅；技能体隔离环境可执行性 ✅（语料库中上游）；但 OUT-01 的
误报/漏报双向缺陷 + CF-01 冲突构成评分稳定性风险，见 §13 F-01/F-02。

---

## 10. SCORING.yaml 交叉参考

SCORING.yaml 全部 9 条判据 + 3 条 critical_failures 与 SKILL.md 的对应关系逐条核对：

| ID | 行（SCORING.yaml） | judge | 对应 SKILL.md | 覆盖度 |
|----|-------------------|:-----:|---------------|:------:|
| SCOPE-01 | L7-13 | llm | L18、L20-25（任务四分类） | ✅ 完整 |
| SCOPE-02 | L15-21 | llm | L64（问清受众，勿默认 OSS） | ✅ 完整 |
| PROC-01 | L24-30 | llm | L29-49（四类任务提问清单） | ✅ 完整 |
| PROC-02 | L33-38 | llm | L45-49（Review 流程：读现状/对照状态/标记过期） | ✅ 完整 |
| PROC-03 | L42-46 | script | L59-62（模板路径表） | ✅ 一致，check.py L36 |
| PROC-04 | L51-56 | llm | L53（收尾追问，逐字对应） | ✅ 完整 |
| OUT-01 | L58-63 | script | L70-72（必需三节） | ⚠️ 弱判别（§9 D-1/D-2） |
| OUT-02 | L66-71 | llm | L59-62（Key Sections 按受众匹配） | ✅ 完整 |
| NEG-01 | L75-80 | llm | L66-72 vs L64（针对性而非一刀切） | ⚠️ 与 OUT-02 重复 |
| CF-01 | L82-85 | (llm) | L70-72（缺必需节） | ⚠️ 与 Config 模板矛盾（P-1） |
| CF-02 | L87-89 | (llm) | L64（未识别类型即默认 OSS） | ✅ 呼应 |
| CF-03 | L91-93 | (llm) | L42-43、L46-47（先读再改） | ✅ 呼应 |

- `total_items: 9`（L3）与实际判据数 9（2+4+2+1）✅ 一致。
- 判据问题均为 yes/no 可判形式，evidence 字段指向明确（"Agent's first response text"、
  "Tool call log (Read calls)"、"Final README content"）✅。
- **缺口**：
  (a) **OUT-02 与 NEG-01 实质性重复**——OUT-02 问 "Do the README sections match the
  audience's needs ... rather than a generic one-size-fits-all template?"，NEG-01 问 "Is the
  README tailored to the identified audience — not a one-size-fits-all template?"，同一问题
  的双重表述。9 条判据里约 1.5 条是冗余的，稀释了判据集的区分度；
  (b) **无计分聚合规则**——`total_items: 9` 只声明数量，pass_threshold、llm/script 判据是否
  等权、cap_to_0 与总分如何交互均未成文（与 054 F-04 同款缺口，属 runner 侧协议问题）；
  (c) SCOPE-01 与 PROC-01 有部分重叠（任务类型识别 vs 提问清单），可接受但边界未声明；
  (d) evidence 字段出现 "AskUserQuestion"（L21、L30）——该工具在 SkillIF 隔离 harness 中
  是否存在未确认，若不存在，llm judge 需要按"工具调用日志或首轮回复文本"理解这条证据；
  (e) CF-01 的判定与 Config 模板冲突（P-1），这是本 SCORING 最需要修的条目。

**结论**: SCORING.yaml 与 SKILL.md 的对齐度整体良好（9 条全部可在正文找到落点，脚本正则
逐字一致），但存在 1 处评分逻辑冲突（CF-01 vs Config 模板）、1 对重复判据（OUT-02/NEG-01）、
1 个弱脚本判据（OUT-01），交叉一致性居语料库中游。

---

## 11. dossier 汇总与对照集对比

### 11.1 dossier 记录

memory 中 skill-dossier.md 对本 skill 无独立条目，仅出现在 Batch 226-250 的合并摘要
（L1011-1016）：

> 合规: 🟢 233/237/240/241/243/248 三节齐全；232/238/239/242/244/245/246/247 🟡 缺 scope/output 节。

| 项 | dossier 记录 | 本审查结论 | 一致性 |
|----|-------------|-----------|:------:|
| 评级 | 🟡（缺 scope/output 节） | 🟡 B+ (84/100) | ✅ 一致 |
| 合规判断 | "缺 scope/output 节" | §7 第 9/10 项 ❌，完全复现 | ✅ 一致（dossier 摘要准确） |
| 逻辑/语法/人机感 | 未单独记录 | 本审查 §4/§6/§8 | —（dossier 无此维度数据） |

结论：dossier 的合并摘要对本 skill 的判断（🟡、缺两节）经得起复核；本审查新增的发现全部
集中在其未覆盖的维度（§4 P-1 评分冲突、§9 脚本缺陷、§5 死链）。

### 11.2 无 trigger 对照集对比

`complex-skills-no-trigger\239-crafting-effective-readmes\` 与本目录 diff：

```
SKILL.md 仅 L3 description 不同：
< description: README writing methodology with audience-matched templates. Use when writing
<   or improving README files. Not all READMEs are the same — provides templates and guidance
<   matched to your audience and project type.
---
> description: READMEs answer questions your audience will have.  Different audiences need
>   different information - an OSS project contributor needs different context than your future
>   self opening a config folder.
SCORING.yaml: 完全相同（diff 为空）
```

- **对照设计评价**: ✅ 两版仅 description 一行差异，SCORING 一致——这是干净的双变量设计，
  符合"2 Mode × 5 Harness"实验对 trigger 对照集的隔离要求（对照组无任何触发语，
  实验组含 "Use when..." 触发语）。
- **小瑕疵（不影响实验）**: 对照组 description 借用了 SKILL.md L10 的 Overview 句子，含
  双空格 "have.  Different"（L3 内）与连字符 `-` 的遗留格式问题；且该句是第三人称陈述句，
  无 WHEN 触发信息——对照组的 description 信息完整度低于实验组，属设计使然（无 trigger
  版本就要去掉触发语），但"删触发语的同时补一句 WHEN 信息"会在对照设计上更对等（如保留
  "Use for documentation tasks" 之外的场景描述）。记录为观察项，不建议改动（实验设计已定稿）。

---

## 12. 综合评分（8 维加权 + 等级）

评分口径：每维 0-100，权重合计 100%。权重反映 SkillIF 测评目标（逻辑正确性与规范合规优先，
可执行性与参考质量为次）。

| # | 维度 | 权重 | 得分 | 加权 | 主要扣分点 |
|---|------|:----:|:----:|:----:|-----------|
| 1 | 逻辑一致性 | 15% | 82 | 12.30 | P-1 Essential Sections 与 Config 模板/CF-01 冲突（评分级矛盾）；P-2 双份真相；P-3/P-4/P-5 小错位 |
| 2 | 语法格式 | 10% | 90 | 9.00 | description 碎片句；L10 连字符风格；两处第三方残留 |
| 3 | 人机感 | 10% | 92 | 9.20 | 咨询式提问优秀；"表单感"提问清单与单薄收尾扣分 |
| 4 | SKILL-SPEC 合规 | 15% | 80 | 12.00 | 缺 Output Format 与 Scope/Limitations 两必需节（硬缺口）；触发短语缺 "the user" |
| 5 | 可执行性 | 15% | 80 | 12.00 | OUT-01 双向缺陷（读文件即误报 / 同义标题漏报）；CF-01 评分陷阱；PROC-03 必须读模板的偏严设计；Output Format 缺失降低产物可测性 |
| 6 | SCORING 交叉 | 10% | 85 | 8.50 | OUT-02/NEG-01 重复；无聚合规则；AskUserQuestion 证据存疑 |
| 7 | 参考文件 | 10% | 82 | 8.20 | 三处死链（art-of-readme 翻译链、spec 的 README.md 链、maximal 空链）；maximal 残留维护者元文本；style-guide 过薄 |
| 8 | 内容深度/知识增量 | 15% | 85 | 12.75 | 受众×任务矩阵与四套差异化模板是高增量；SKILL.md 本体仅 73 行，知识大部分在模板侧 |
| — | **加权总分** | 100% | — | **83.95 ≈ 84** | — |

**等级**: **B+**（80-84 档）→ 🟡 需要改进。

**等级构成说明**:

- **A 档门槛（85+）未达原因**: 两处硬伤——(a) §3.1 两必需节（Output Format、Scope/
  Limitations）缺失，这是语料库最常见的规范缺口，dossier 已指出；(b) P-1 的 CF-01 评分冲突
  不是美学问题而是评测正确性问题：Config 任务下忠实执行会被 cap_to_0。两者修复成本都低
  （见 §13 F-01/F-03/F-04），修复后本 skill 有机会进入 A− 档。
- **低于 B（75）未达原因**: 无——内容组织（受众×任务矩阵）、模板质量（internal.md 的
  运维化设计）、参考选材（三个官方级来源）都是语料库中上游水平；逻辑除 P-1 外全部自洽；
  人机感干净；隔离环境可执行性先天优秀。
- **与 dossier 一致性**: 🟡 评级一致；本审查评分（84）落在 B+ 上沿，与 dossier 的
  "缺两节→🟡"判断互相印证。

**分维度等级映射**: 逻辑 B+ / 语法 A− / 人机感 A− / 合规 B / 可执行 B+ / SCORING B+ / 参考 B+ / 深度 B+。

---

## 13. 修复建议 ★重点★

本节为本次审查的核心产出。按优先级 P0（评分正确性/阻断性）→ P1（规范硬缺口）→ P2
（一致性风险）→ P3（打磨项）→ P4（观察项）排列；每条含：位置、问题、理由、建议改法、
改动量估算。

### 13.1 修复优先级总览

| 编号 | 优先级 | 主题 | 位置 | 影响 |
|------|:------:|------|------|------|
| F-01 | P0 | CF-01 与 Config 模板的评分冲突 | SKILL.md L66-72 + SCORING.yaml L82-85 | 评测正确性 |
| F-02 | P0 | OUT-01 弱判别（读文件即误报 / 同义标题漏报） | check.py L40 + SCORING.yaml L58-63 | 评分稳定性 |
| F-03 | P1 | 新增 `## Output Format` 节 | SKILL.md（body 尾部） | SKILL-SPEC §3.1 硬缺口 |
| F-04 | P1 | 新增 `## Scope & Limitations` 节 | SKILL.md（body 尾部） | SKILL-SPEC §3.1 硬缺口 |
| F-05 | P1 | description 触发短语补 "the user" | SKILL.md L3 | SKILL-SPEC §2.4 |
| F-06 | P2 | SKILL.md 与 README.md 双份真相去重 | README.md L1-176 | 长期漂移风险 |
| F-07 | P2 | references 死链清理 | references/ 三文件 | 参考可用性 |
| F-08 | P2 | SCORING.yaml 补计分聚合规则 | SCORING.yaml 头部 | 测评可复现性 |
| F-09 | P2 | OUT-02 与 NEG-01 去重 | SCORING.yaml L66-80 | 判据区分度 |
| F-10 | P2 | SKILL.md References 节补 references/ 索引 | SKILL.md L74-78 | 深度材料可发现性 |
| F-11 | P3 | section-checklist 与模板错位标注 | section-checklist.md | 清单-模板一致性 |
| F-12 | P3 | description 碎片句补主语 | SKILL.md L3 | 语法 |
| F-13 | P3 | check.py 死导入与 workspace 注释 | check.py L12-20 | 代码卫生 |
| F-14 | P4 | AskUserQuestion evidence 存疑标注 | SCORING.yaml L21/L30 | 证据可执行性 |
| F-15 | P4 | no-trigger 版 description 格式勘误 | no-trigger 对照集 SKILL.md L3 | 对照集卫生 |
| F-16 | P4 | style-guide.md 增补本 skill 差异化规则 | style-guide.md | 风格指南厚度 |

### 13.2 P0 — 评分正确性（先做）

**F-01 化解 CF-01 与 Config 模板的冲突**（SKILL.md L66-72 + SCORING.yaml L82-85）

- 问题：SKILL.md 宣称 Usage 是**所有类型**必备；xdg-config.md 模板没有 Usage 节；
  section-checklist.md L10 又说 Config 只需 "Brief"；SCORING CF-01 以"缺 Usage → cap_to_0"
  兜底。四者互相矛盾。对 Config 任务忠实执行模板的 agent 会被 CF-01 判死，而 Config 恰是
  四类项目之一，评测用例覆盖到即真实触发。
- 建议（推荐方案：改 SKILL.md 与 SCORING，模板不动）：
  1. SKILL.md L66-72 标题改为 "## Essential Sections"，正文按类型分列："Every README needs
     a name and a description. Usage is required for OSS / Personal / Internal projects; for
     config directories a short usage note (or none) suffices — see section-checklist.md."
  2. SCORING.yaml CF-01 description 追加限定："(Config 类型 README 豁免 Usage 要求，须有
     Name + Description)"。
  3. 同步把 OUT-01 的脚本判据范围与 CF-01 对齐（见 F-02）。
- 改动量：SKILL.md 改写 4~6 行；SCORING.yaml 改 1 行。收益：消除评测正确性唯一硬伤。

**F-02 OUT-01 判别加固**（check.py L40 + SCORING.yaml L58-63）

- 问题：`tool_log_contains("#+ (Description|Usage)")` 扫描整条 JSON 日志——agent 读
  README.md（L96 "## Usage Examples"）或 templates/oss.md（L36 "## Usage"）即误报通过；
  反之 agent 用 "## How to Use" 等标题则恒漏报。
- 建议（三选一，按推荐序）：
  1. **最简**：pattern 改为带 Write 工具限定（若 tool log 结构支持），如
     `"(Write|Edit)".*"#+ (Description|Usage)"`，把命中域缩小到写操作；
  2. **更稳**：改用输出文件检查——让 agent 把 README 写到 workspace 内约定路径
     （配合 F-03 的 Output Format 节定义 `README.md` 于项目根），用 `file_contains` +
     `output_contains` 系列检查最终产物；
  3. **配套**：SCORING.yaml OUT-01 的 question 加限定词
     "in the final README the agent writes"，提示 llm judge 忽略工具日志中的读取内容。
- 改动量：check.py 1 行（pattern 改写）或 3-4 行（换用文件检查）；SCORING.yaml 1 行。
  5 分钟内可完成。

### 13.3 P1 — 规范硬缺口（评估后尽快）

**F-03 新增 `## Output Format` 节**（SKILL.md body 尾部，`## References` 之前）

- 问题：§3.1 三必需节中缺失其一。交付协议（文件名、位置、语言、与模板的关系）完全未定义，
  产物可测性低（§9）。
- 建议内容（直接可用，约 10 行）：
  > ## Output Format
  > The deliverable is a `README.md` file at the project root, written in the project's primary
  > language. Structure follows the template matching the project type (see Project Types);
  > fill in every `[placeholder]` in the template. Keep the three essential sections intact
  > (see Essential Sections). For update/review tasks, edit the existing README in place
  > rather than rewriting from scratch. After drafting, ask the follow-up question in Step 3.
- 改动量：+10 行。一次编辑补上规范缺口。

**F-04 新增 `## Scope & Limitations` 节**（SKILL.md body 尾部，紧邻 F-03）

- 问题：§3.1 三必需节中缺失其二。以下边界未成文，agent 无从判断"不适用"：
  - 非代码项目（数据仓库/设计资产/纯文档仓库）——模板矩阵未覆盖；
  - README 翻译与 i18n 结构（多语言 README 的文件命名约定不在本 skill 范围）；
  - 完整文档站点/API 文档生成（README 只是入口，非替代品）；
  - 持续维护——本 skill 是单次任务型（Review 完成后由用户决定何时再跑）；
  - 徽章/截图/资产制作（本 skill 只引用，不生成）。
- 建议内容（直接可用，约 8 行）：
  > ## Scope & Limitations
  > This skill writes, extends, updates, and reviews README files for code projects of four
  > types (OSS, personal, internal, config directories). It does not translate READMEs, build
  > documentation sites or API docs, generate screenshots or badges, or cover non-code
  > repositories. Reviews are point-in-time: re-run after project changes. Templates are
  > starting points — adapt section order to the actual project when the checklist allows.
- 改动量：+8 行。两个 P1 缺口合计 +18 行，SKILL.md 仍远低于 600 行上限。

**F-05 description 触发短语补 "the user"**（SKILL.md L3）

- 问题：SKILL-SPEC §2.4 字面清单要求五种触发形式之一，"Use when writing..." 缺主语。
- 建议改法（保持 ≤1024 字符，顺手修碎片句）：
  > "README writing methodology with audience-matched templates for OSS, personal, internal,
  > and config projects. Use when the user is writing, updating, or reviewing a README file,
  > or asking which sections a README should have. Not all READMEs are the same — this skill
  > matches templates and guidance to the audience and project type."
- 改动量：L3 单行改写。注意 no-trigger 对照集版本的 description 需保持无触发语，不受影响
  （F-15 另有其格式勘误）。

### 13.4 P2 — 一致性风险（计划内）

**F-06 SKILL.md 与 README.md 双份真相去重**（README.md L1-176）

- 问题：两个文件描述同一技能，Step 内容、收尾追问措辞已出现可观测漂移（§4 P-2）。
- 建议：README.md 头部加注说明性横幅："This README describes the skill for humans browsing
  the repo; SKILL.md is the executable source of truth and may differ." 并把 README.md 中与
  SKILL.md 重复的 Step/表格改为引用 SKILL.md 的概述（保留触发短语、对话示例、Directory
  Structure 等 README 独有内容）。改动量：README.md 改写约 30 行。

**F-07 references 死链清理**（references/art-of-readme.md L5-8、standard-readme-spec.md L7、
standard-readme-example-maximal.md L34/L46）

- 问题：三处链接触发即 404/空目标（§5.1/5.3/5.5）。
- 建议：翻译版链接改为注释或删除（原仓库链接保留为外链）；spec 的 `README.md#background`
  改为指回 `../README.md#background`（技能根 README 无 Background 锚点，实际应改为删除或
  指向仓库 URL）；maximal 的 `[Markdown]()` 填充为外链或删除该句；L46 维护者元文本删除或
  移入注释。改动量：4 处共约 6 行。

**F-08 SCORING.yaml 补计分规则**（SCORING.yaml L1-5 附近）

- 问题：与 054 F-04 同款——9 条判据无聚合规则（threshold/权重/CF 交互均未成文）。
- 建议：
  ```yaml
  scoring:
    pass_threshold: 0.8
    weights: { scope: 0.2, process: 0.35, output: 0.25, negative: 0.20 }
    cap_to_0: critical_failures
  ```
  （数值为建议值，需 runner 侧协议确认。）
- 改动量：+6 行。

**F-09 OUT-02 与 NEG-01 去重**（SCORING.yaml L66-80）

- 问题：同一问题（tailored vs generic）的双重表述，稀释判据区分度。
- 建议：保留 OUT-02（正向表述），NEG-01 改为补集检查："Agent does not apply the OSS template
  to a non-OSS project（反向：未识别类型即套 OSS 模板）"——这正好与 CF-02 区分开（CF-02
  惩罚"默认 OSS"，NEG-01 惩罚"套错模板"），并把 `total_items` 维持 9（替换而非删除）。
- 改动量：1 条判据改写，共约 6 行。

**F-10 SKILL.md References 节补全索引**（SKILL.md L74-78）

- 问题：references/ 目录 5 个文件在 SKILL.md 中零索引，发现链依赖 using-references.md。
- 建议：References 节补一行：
  > - `using-references.md` - Guide to deeper reference materials (art-of-readme,
  >   make-a-readme, standard-readme-spec + two example READMEs in `references/`)
- 改动量：1 行。

### 13.5 P3 — 打磨项（顺手）

- **F-11** section-checklist.md 为三处"清单有而模板无"的条目（Internal Usage/Examples、
  OSS Architecture、OSS Gotchas/Notes）加脚注："may be covered by equivalent sections
  (Runbooks / Running Locally; Dependencies; etc.)"。改动量：表格下 +3 行。
- **F-12** description 碎片句补主语（与 F-05 一并完成）。
- **F-13** check.py L12-20 删掉 11 个未使用的 import（file_exists、file_contains、
  file_valid_json、json_*、timestamp_*、tool_log_not_contains、tool_log_read_before_write、
  tool_log_order、output_contains、output_not_contains），L24 的 workspace 参数加一行注释
  说明协议兼容用途。改动量：删 8 行、加 1 行。
- **F-14** SCORING.yaml L21/L30 的 AskUserQuestion 若确认不在隔离 harness 中，改为
  "Agent's first response text or tool call log"，避免 judge 找不到证据载体。改动量：2 行。

### 13.6 P4 — 观察项（记录不行动）

- **F-15** no-trigger 对照集 SKILL.md L3 description 内双空格 "have.  Different" 与连字符
  `-` 风格——不影响实验（对照组不参与 trigger 评分），待下次批量维护对照集时一并勘误。
- **F-16** style-guide.md 可增补 1-2 条本 skill 差异化规则（如"Config 场景对 future-you
  用口语化指引"、"Badges 仅在 OSS 场景使用"），降低纯指针感——不必须，现有内容不违规。

### 13.7 建议修复顺序

| 步骤 | 内容 | 依赖 |
|------|------|------|
| 1 | F-01（CF-01 冲突）+ F-02（OUT-01 加固） | 无，可立即做 |
| 2 | F-03 + F-04（两个必需节，一次编辑） | 无 |
| 3 | F-05 + F-12（description 单行改写） | 无 |
| 4 | F-06/07/10（一致性批次，可一次 PR） | 无 |
| 5 | F-08/09/14（SCORING 批次，需 runner 协议确认） | 依赖 runner 团队 |
| 6 | F-11/13/16（打磨批次） | 无 |

预计总改动量：SKILL.md +25~30 行、README.md ±30 行、SCORING.yaml ±15 行、check.py −7 行、
references/ −6 行。全部完成后：合规维度可升至 92+（两必需节补齐、触发短语达标）、可执行性
维度升至 88+（OUT-01 加固、CF-01 冲突消解）、加权总分约 **90 → A− 档**，进入 🟢 区间。

---

## 附录 A — 逐行勘误表（本审查所有发现点汇总）

| 位置 | 文件 | 问题 | 优先级 | 处置 |
|------|------|------|:------:|------|
| L3 | SKILL.md | 触发短语缺 "the user"；碎片句 | P1/P3 | F-05/F-12 |
| L10 | SKILL.md | 连字符 `-` 风格与 description 的 em dash 不一致 | P3 | F-12 一并 |
| L66-72 | SKILL.md | "All Types 必备 Usage" 与 Config 模板矛盾 | P0 | F-01 |
| L74-78 | SKILL.md | References 节未索引 references/ 目录 | P2 | F-10 |
| L96 | README.md | "## Usage Examples" 使 OUT-01 误报 | P0（检测侧） | F-02 |
| L88-94 vs L164-171 | README.md | Reference Materials 与 Directory Structure 对参考文件计数不一致 | P2 | F-06 |
| L1-176 | README.md | 与 SKILL.md 双份真相 | P2 | F-06 |
| L82-85 | SCORING.yaml | CF-01 与 Config 模板冲突 | P0 | F-01 |
| L58-63 | SCORING.yaml | OUT-01 弱判别 | P0 | F-02 |
| L66-80 | SCORING.yaml | OUT-02 与 NEG-01 重复 | P2 | F-09 |
| L21/L30 | SCORING.yaml | AskUserQuestion 证据载体存疑 | P3 | F-14 |
| L1-5 | SCORING.yaml | 无计分聚合规则 | P2 | F-08 |
| L40 | check.py | OUT-01 pattern 扫描全量日志 | P0 | F-02 |
| L12-20 | check.py | 11 个死 import | P3 | F-13 |
| L24 | check.py | workspace 未用 | P3 | F-13 |
| L5-8 | references/art-of-readme.md | 7 个翻译版死链 | P2 | F-07 |
| L7 | references/standard-readme-spec.md | README.md#background 相对路径失效 | P2 | F-07 |
| L34/L46 | references/standard-readme-example-maximal.md | 空链接 + 维护者元文本残留 | P2 | F-07 |
| L11/L8/L7 | section-checklist.md | 与模板的等价覆盖错位未标注 | P3 | F-11 |
| L3 | no-trigger SKILL.md | 双空格 + 连字符风格 | P4 | F-15 |
| — | style-guide.md | 13 行过薄、与 README.md Common Mistakes 重复 | P4 | F-16 |

## 附录 B — 12 项规范合规总表

| # | 检查项 | 判定 |
|---|--------|:----:|
| 1 | name 合规 | ✅ |
| 2 | description 结构与长度 | ✅ |
| 3 | description 人称 | ✅ |
| 4 | description 无跨技能路由 | ✅ |
| 5 | description 触发短语 | ⚠️ |
| 6 | frontmatter 无禁用键 | ✅ |
| 7 | body ≤600 行 | ✅ |
| 8 | workflow/process 节 | ✅ |
| 9 | output format 节 | ❌ |
| 10 | scope/limitations 节 | ❌ |
| 11 | 无跨技能文件引用 | ✅ |
| 12 | 目录命名 | ✅ |

合计：8 ✅ / 1 ⚠️ / 2 ❌（修复后预期 10 ✅ / 1 ⚠️ / 0 ❌）。

## 附录 C — 审查方法说明

- 阅读范围：239-crafting-effective-readmes 目录全部 16 个文件（SKILL.md 77 行 / README.md
  176 行 / SCORING.yaml 93 行 / check.py 68 行 / section-checklist.md 17 行 / style-guide.md
  13 行 / using-references.md 35 行 / references/ 5 文件共 986 行 / templates/ 4 文件共 305
  行）；共享件 `_shared/SKILL-SPEC.md`（161 行）、`_shared/checker.py`（`tool_log_contains`
  L259-262 等关键函数）；memory skill-dossier.md 批次摘要（L1011-1016）；与
  `complex-skills-no-trigger\239-crafting-effective-readmes\` 的 SKILL.md/SCORING.yaml diff。
- 评分口径：8 维加权（§12 表），与 dossier 5 维审查（逻辑/语法/人机感/合规/总评）的映射：
  维度 1↔逻辑、2↔语法、3↔人机感、4↔合规、7/8↔合规延伸、5↔新增（可执行性）、6↔新增
  （SCORING 交叉）。
- 限制：本审查未在隔离环境实际运行 agent 评测，check.py 的可行性为静态核对（依赖函数
  存在性、模式串转义、与 SCORING.yaml 逐字比对），未做动态执行验证；OUT-01 误报结论基于
  checker.py `_log_search` 的 `json.dumps` 全量扫描实现推导，具体 tool log 结构以 runner
  实际格式为准。
