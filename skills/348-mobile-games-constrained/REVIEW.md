# REVIEW — 082-mobile-games

> 审查对象：`D:\SkillIF\skill-experiment\complex-skills\082-mobile-games\`
> 审查基准：`_shared/SKILL-SPEC.md` (v1.0) + Skill Dossier 档案（2026-08-05 批次审查）
> 审查日期：2026-08-06

---

## §1 审查概述

### 1.1 审查范围与方法

本次审查对 skill 082-mobile-games 的完整包进行逐文件审读，包括：

1. **SKILL.md** — 技能主体，对照 SKILL-SPEC v1.0 的 Frontmatter 规则（§1）、Description 规范（§2）、Body 结构规范（§3）、目录命名规范（§4）与合规清单（§5）逐项核对。
2. **SCORING.yaml** — 15 条评测准则的完整性、可判性、与 SKILL.md 内容的可溯源性，以及 critical_failures 的设计合理性。
3. **check.py** — 脚本校验实现与 runner 约定的兼容性（`python check.py <workspace> <tool_log> <agent_output>`）。
4. **`_shared/checker.py` / `_shared/CHECKER-LIBRARY.md`** — 校验函数库，用于评估 check.py 是否充分利用了可用的脚本校验能力。
5. **Skill Dossier** — 对照既有审查结论（082 条目评级 🟡），验证本审查的独立结论是否一致，并补充更细粒度的证据。

审查采用五维框架（与 Dossier 一致）：逻辑一致性、语法与可读性、人机感、规范合规性、整体评价。

### 1.2 总体结论预览

- **内容正确性**：主体知识表（触控、电池、热管理、商店要求、变现模式）技术事实基本准确，无硬伤。
- **规范合规性**：Description 完全合规；但 **Body 缺失全部三个必需节（Workflow/Output/Scope）**，是 SKILL-SPEC §3.1 的硬性缺口。
- **评测体系**：SCORING.yaml 准则与正文内容 1:1 可溯源；check.py 为全 LLM 判定（0 条脚本校验），与 mindset pattern 匹配，可接受。
- **综合评级**：🟡（与 Dossier 一致）。但需指出：若严格执行 SKILL-SPEC §3.1 的 MUST 条款，缺三节应视为 🟠；鉴于修复成本低（纯新增三个小节），本审查按 🟡 归档并给出完整修复方案（见 §13）。

---

## §2 文件清单与规模统计

| 文件 | 行数 | 字节 | 作用 | 备注 |
|------|:----:|:----:|------|------|
| `SKILL.md` | 108 | 2,593 | 技能主体（frontmatter 5 行 + 正文约 101 行） | 正文 6 个编号小节，全部为表格 |
| `SCORING.yaml` | 141 | 7,002 | 评测准则（15 条 llm 判定 + 2 条 critical_failures） | pattern: mindset |
| `check.py` | 77 | 2,430 | runner 调用入口，返回空 dict `{}` | 0 条脚本可校验项 |
| `_shared/checker.py` | 351 | — | 共享校验函数库 | 本 skill 未使用其中任何函数 |
| `_shared/SKILL-SPEC.md` | 162 | — | 规范基准 | 见 §1.1 |

目录内无 `references/`、`scripts/` 子目录，无外部文件引用——本 skill 是完全自包含的单一文件知识型 skill。

**规模对照**：mindset pattern 的目标体量约 50 行（SKILL-SPEC §3.2），本正文约 101 行，约为目标的 2 倍，但仍远低于 600 行硬上限。对 mindset 类技能而言略偏长，属于"轻微超标的可接受范围"（详见 §13 的 I11）。

---

## §3 SKILL.md Frontmatter 审查

### 3.1 name 字段

```yaml
name: mobile-games
```

| 规则 (SKILL-SPEC §1.1) | 结果 |
|------------------------|:----:|
| 小写 + 连字符 | ✅ |
| ≤64 字符 | ✅ |
| 与目录名 `082-mobile-games` 匹配 | ✅ |

**结论：通过。**

### 3.2 description 字段

```yaml
description: Mobile game development principles. Touch input, battery, performance, app stores. Use when the user asks to build or optimize a mobile game, design touch controls, manage battery and thermal constraints, choose a monetization model, or prepare for App Store or Google Play release.
```

- 长度约 265 字符，≤1024 ✅
- 第三人称 ✅，无祈使/第一/第二人称开头 ✅
- 无跨技能路由（无 "NOT for X, use Y instead"）✅
- 无违禁关键词 ✅

**结论：通过。** 详细的结构分析见 §4。

### 3.3 allowed-tools 字段

```yaml
allowed-tools: Read, Write, Edit, Glob, Grep
```

- 属 SKILL-SPEC §1.2 允许的可选字段 ✅
- 逗号分隔格式 ✅
- 不含 `Bash`：对本技能合理——mindset 类技能只产出建议/文档，不执行构建命令；与"纯知识表"的定位一致。唯一张力：description 声称支持"build a mobile game"场景，而受限工具集不支持运行构建/测试命令。由于正文本身不含任何构建流程（见 §5/I1），实际不存在执行缺口；但若按 §13 方案补充 workflow，应保持"给出建议、不执行构建"的边界并在 Scope 节明示。

### 3.4 违禁字段检查

遍历 frontmatter，未发现 `metadata`、`license`、`version`、`tags`、`category`、`trigger(s)`、`tools` 等任何 SKILL-SPEC §1.3 列出的违禁键。**结论：通过。**

### 3.5 小结

| 项目 | 状态 |
|------|:----:|
| name | ✅ |
| description | ✅ |
| allowed-tools | ✅ |
| 无违禁字段 | ✅ |

**Frontmatter 整体合规，是干净的两字段 + 工具白名单最小结构。**

---

## §4 Description 规范审查（SKILL-SPEC §2）

### 4.1 三要素检查（WHAT / WHEN / KEYWORDS）

| 要素 | 内容 | 评价 |
|------|------|------|
| **WHAT** | "Mobile game development principles. Touch input, battery, performance, app stores." | ✅ 明确说明技能性质是"移动游戏开发原则"，并点出四个核心领域。 |
| **WHEN** | "Use when the user asks to build or optimize a mobile game, design touch controls, manage battery and thermal constraints, choose a monetization model, or prepare for App Store or Google Play release." | ✅ 5 个具体触发场景：构建/优化、触控设计、电池热约束、变现选型、商店上架。 |
| **KEYWORDS** | touch input, battery, performance, app stores, monetization, App Store, Google Play | ✅ 域名术语与动作动词齐备，利于意图匹配。 |

### 4.2 触发信号检查（§2.4）

- 含 `"Use when the user asks to..."` ✅（规范列出的标准触发信号，至少一个即通过）

### 4.3 语音与文风检查（§2.3）

- 第三人称 ✅；无 "Use this skill to..." 式祈使开头 ✅；无 "I can help..." / "You can use..." ✅。

### 4.4 规避项检查（§2.5）

- 无跨技能路由 ✅；非通用含糊描述（"A useful skill" 类）✅；长度 265 字符远大于 40 字符下限 ✅。

### 4.5 与正例模板的贴合度

对照 SKILL-SPEC §2.6 的 Good 示例（"Generate comprehensive test plans... Use when the user asks to..."），本 description 的句式结构与规范正例完全同构——**在全部 322 个 skill 的 description 中属于中上水平**。

**结论：Description 完全合规，无需修改。**

---

## §5 Body 结构与必需节审查（SKILL-SPEC §3.1）

### 5.1 现有结构盘点

正文共 6 个编号小节 + 1 个结尾块引用：

| 小节 | 内容 | 对应 SCORING 准则 |
|------|------|-------------------|
| §1 Platform Considerations | 5 行约束表（触控/电池/热/屏幕/中断） | SCOPE-01, OUT-02, PROC-06 |
| §2 Touch Input Principles | 触控 vs 手柄对照表 + 4 条最佳实践 | PROC-01, PROC-02, PROC-03, NEG-01 |
| §3 Performance Targets | 热管理分级表 + 电池优化 4 条 | PROC-04, PROC-05, NEG-02 |
| §4 App Store Requirements | iOS 3 项 / Android 3 项 | PROC-07 |
| §5 Monetization Models | 4 种模型"Best For"表 | PROC-08 |
| §6 Anti-Patterns | ❌/✅ 4 行对照表 | NEG-01, NEG-02, QA-01, CF-01, CF-02 |

结构特点：**100% 表格化**，零流程叙述、零示例、零决策树。这是本 skill 最核心的结构问题（见下）。

### 5.2 必需节检查（§3.1 —— MUST）

| 必需节 | 是否存在 | 说明 |
|--------|:--------:|------|
| **Workflow / Process** | ❌ **缺失** | 全文没有任何"先做什么、再做什么"的过程指令。无步骤、无输入、无输出、无决策分支。 |
| **Output Format** | ❌ **缺失** | 未定义 agent 交付什么：无建议清单模板、无交付物结构、无格式要求。 |
| **Scope / Limitations** | ❌ **缺失** | 未声明"何时不使用"、边界（web/桌面游戏？引擎教程？商店法务审查？）。 |

**这是本次审查的核心发现：三个必需节全部缺失。** 该技能在严格规范意义上不符合 SKILL-SPEC §3.1。与 Dossier 记录一致（"body 缺全部三必需节"）。

### 5.3 缺失三节的后果分析

1. **可执行性受损**：agent 加载该 skill 后只能获得"知识表格"，没有"使用这套知识的程序"。对 mindset pattern 而言，表格是素材而非方法论——缺少"在什么条件下选择哪条约束、如何把约束落到具体游戏上"的决策逻辑。
2. **description 承诺落空**：description 声称覆盖 "build a mobile game" 场景，但正文没有任何构建流程内容；"choose a monetization model" 也只有一张表，没有选型决策依据。
3. **评测失真风险**：SCORING.yaml 的 15 条准则全部针对"agent 输出"判定，而 skill 本身未教给 agent 如何产出这些输出，导致准则评估的更多是 agent 先验知识而非技能遵从度——这一点在 §10/§13 (I9) 详述。

### 5.4 体量检查（§3.2）

- 正文约 101 行，远低于 600 行硬上限 ✅
- mindset 目标约 50 行：超 2 倍 ⚠️（轻微，见 §13 I11）

### 5.5 文件引用检查（§3.3）

- 无任何 `references/`、`scripts/` 相对路径引用，也无跨 skill 路径（`../other-skill/`）✅。
- 未用 prose 提及姊妹技能（如 mobile-design）——不违规，但见 §12 的语料重叠讨论与 §13 I12。

### 5.6 小结

| 检查项 | 状态 |
|--------|:----:|
| workflow/process 节 | ❌ |
| output format 节 | ❌ |
| scope/limitations 节 | ❌ |
| ≤600 行 | ✅ |
| 无跨 skill 路径 | ✅ |

---

## §6 内容质量与知识准确性审查

### 6.1 事实准确项（正确，予以确认）

| 内容 | 判定 | 依据 |
|------|:----:|------|
| 最小触控目标 44×44 pt | ✅ | 与 Apple HIG 一致（Material Design 为 48×48 dp，见 6.2 微调项） |
| 触控不精确、遮挡屏幕、手势可用 | ✅ | 行业共识 |
| 热分级策略（warm→降质、hot→限帧、critical→停特效） | ✅ | 业界标准三档降级思路 |
| 30 FPS 往往足够 | ✅ | 对休闲/卡牌类成立（竞技类需 60/120，见 6.3） |
| 暂停时休眠 | ✅ | 移动 OS 生命周期标准做法 |
| 深色模式省 OLED 电量 | ✅ | OLED 黑像素关闭，节电成立（对 LCD 无效——细节见 6.2） |
| iOS 隐私标签必需 | ✅ | App Privacy 声明为强制 |
| iOS 账号删除要求 | ✅ | 2022-06 起有账号创建即需提供删除 |
| Android 64 位必需 | ✅ | 2019-08（新应用）/ 2021-08（更新）强制 |
| 反模式表（桌面控制/无视电量/强制横屏/常驻联网） | ✅ | 均为真实高频坑 |

### 6.2 精度微调项（正确但表述可更精确）

1. **"Screenshots: For all device sizes"**（§4 iOS 表）：App Store Connect 实际要求提供最大（6.7"）与最小（6.1"）支持显示尺寸的截图，并非"所有尺寸"。建议改为 "Largest and smallest supported display sizes"。
2. **"App bundles: Recommended"**（§4 Android 表）：低估了强制力——自 2021-08 起新应用**必须**提交 AAB，并非"推荐"。建议改为 "Required for new apps (since Aug 2021)"。
3. **"Target API: Current year SDK"**（§4 Android 表）：Google Play 政策为"距最新 API 一年内"（2025-08 后新应用需 target API 35+），并非严格按"当前年份"。建议改为 "Within one year of the latest API level"。
4. **"Dark mode saves OLED battery"**：仅在 OLED 屏成立，LCD 背光常亮不省电。建议加注 "OLED only"。
5. **44×44 pt**：iOS 口径；Android Material 为 48×48 dp。技能面向双平台时建议并列表述。

### 6.3 缺失项（影响完整性与可信度）

按 SKILL-SPEC §3.4"knowledge delta over redundancy / concrete over abstract"要求，下列内容属于该领域**关键且非冗余**的知识增量：

| # | 缺失内容 | 重要性 | 说明 |
|---|----------|:------:|------|
| A | **商店变现规则红线**：Apple 3.1.1 数字商品必须走 IAP | 高 | §5 变现表给出 4 种模型但完全未提规则约束——这是变现建议中最容易误导用户的点（数字内容绕过 IAP 会被拒审/下架）。 |
| B | **Google Play Data Safety 表单** | 中 | 2022-07 起强制，与 iOS App Privacy 对等，§4 未提。 |
| C | **App Tracking Transparency (iOS 14.5+)** | 中 | 广告变现模式（§5 Ads 行）的直接影响项——IDFA 权限弹窗会显著影响 eCPM。 |
| D | **订阅替代支付要求（欧盟 DMA 等地区）** | 中 | §5 Subscription 行的合规注脚。 |
| E | **帧预算具体数字**（60fps→16.7ms、30fps→33.3ms） | 中 | §3 热管理只有抽象动作无量化基准，违反"concrete over abstract"。 |
| F | **输入延迟目标（感知 ≤100ms）** | 低 | 触控手感的关键量化指标。 |
| G | **可访问性**：Dynamic Type、VoiceOver/TalkBack、触控辅助 | 中 | 平台约束型 skill 完全未提无障碍，对"最受约束平台"主题是明显空白。 |
| H | **内存压力处理**（iOS memory warning / Android low-memory killer） | 中 | §3 性能节只讲热与电，缺内存维度。 |
| I | **商店拒审常见原因**（最小功能要求、审核恢复流程） | 低 | §4 只有静态清单，无"准备上架"的过程性指导。 |

> 注：A/C/D 属于"变现 + 商店"两个 description 承诺场景（choose monetization model / prepare for release）的核心支撑知识，缺失后这两大场景的可信度明显下降。

### 6.4 小结

- 现有内容**零事实硬伤**（无 050 类 OWASP 式错误、无 074 类数字矛盾、无 039 类算错数），全部 20+ 条陈述均可核实为正确或基本正确。
- 主要问题集中在**覆盖完整性**（6.3 缺失项）与**表述精度**（6.2 微调项）。

---

## §7 逻辑一致性与内部交叉引用审查

### 7.1 内部一致性核查

逐条核查正文内部、正文与 SCORING.yaml 的对应关系：

| 核查点 | 结论 |
|--------|:----:|
| §1 "Interruptions → Pause in background" ↔ §3 "Sleep when paused" | ✅ 一致 |
| §2 触控对照表 ↔ §6 反模式 "Desktop controls on mobile → Design for touch" | ✅ 一致 |
| §3 "Minimize GPS/network" ↔ §6 "Always-on networking → Cache and sync" | ✅ 一致 |
| §6 "Force landscape → Support player preference" ↔ PROC-03（允许强制方向的唯一理由是玩家偏好/玩法需要） | ✅ 一致 |
| §1 五约束表 ↔ OUT-02 准则（要求把五约束应用到具体游戏） | ✅ 对齐 |
| §2 最佳实践 ↔ PROC-01/02/03（44pt、视觉反馈、避免精确计时、横竖屏） | ✅ 逐条对齐 |
| §3 ↔ PROC-04/05（热分级、30FPS、睡眠、GPS/网络、深色模式） | ✅ 逐条对齐 |
| §4 ↔ PROC-07（iOS 三项、Android 三项） | ✅ 对齐 |
| §5 ↔ PROC-08（4 模型） | ✅ 对齐 |
| §6 ↔ NEG-01/02、CF-01/02、QA-01 | ✅ 对齐 |

**正文与评测准则达到 1:1 可溯源，这是本 skill 评测设计上的显著优点**（见 §10）。

### 7.2 未发现矛盾

- 无编号断裂（区别于 tpl 系列 029/030 的 "1." 缺失、266 的重复编号）。
- 无数字矛盾（区别于 268 的 +3/+5、074 的示例与公式对不上）。
- 无截断（区别于 081/271 的文件中停）。
- 无未解析占位符（区别于 055 的 "`..` skill"、280 的占位符）。

### 7.3 逻辑层面的不足

唯一的逻辑缺陷是**结构性**的：无 workflow = 无过程逻辑可核查。表格各自正确，但彼此之间没有"决策链"把它们串起来。例如：

- 某 agent 面对"休闲放置游戏，双平台"时，§5 该选 Ads 还是 IAP？表格没有给判定条件（留给了 agent 先验）。
- 某 agent 面对"竞速游戏"时，§3 的 30 FPS 建议与"60fps 竞速手感"冲突，skill 未给出按类型选择 FPS 的规则。

这正是 SKILL-SPEC §3.4"decision trees over prose"所针对的缺口：**有知识点，无决策程序**。

---

## §8 语法与可读性审查

### 8.1 拼写与文法

- 全篇无拼写错误、无病句、无中文/葡语混入（区别于 262/276/319 的语言污染）。
- 英文为规范的简明技术文体，术语使用正确（thermal throttling、monetization、touch target 等）。

### 8.2 Markdown 结构

| 检查项 | 结果 |
|--------|:----:|
| 标题层级（H1→H2→H3） | ✅ 规范，无跳级（区别于 061 的并列标题瑕疵） |
| 表格渲染 | ✅ 5 张表均闭合、列对齐 |
| 编号连续性 | ✅ 1-6 连续无断裂 |
| 列表格式 | ✅ 无破损加粗/丢失编号（区别于 tpl 系列） |
| 引用块 | ✅ 结尾 "Remember" 块引用格式正确 |
| frontmatter YAML | ✅ 可解析，无截断（区别于 047/314） |

### 8.3 可读性评价

- 表格密度高、扫描性好，一个屏幕内可概览全 skill——对"快速加载、即时生效"的 mindset 使用场景是优点。
- 反面：零 prose 叙述导致"为什么"缺失。例如 "Minimize GPS/network" 未解释原因（电量 + 隐私 + 流量），agent 无法向用户解释建议的动机。建议在补节时附带每条的"原因"（见 §13 补丁草案）。

**结论：语法零缺陷，结构干净；唯一的可读性改进空间是"原因缺失"。**

---

## §9 人机感审查

### 9.1 语气与情绪

| 维度 | 评价 |
|------|------|
| 对话填充语 | 无（无 "Let's"、"Hey" 类）✅ |
| 全大写喊话 | 无（区别于 072-mobile-design 的 "STOP!"/"GO BACK AND READ"）✅ |
| 营销腔 | 无（区别于 032 的 "Nano Banana Pro will..."）✅ |
| emoji | 仅 §6 反模式表的 ❌/✅，属功能性标记（与 Dossier 判断一致）✅ |
| 人格化称呼 | 无（区别于 006 的 "Ed" 私设）✅ |
| 格言收尾 | "Mobile is the most constrained platform. Respect battery and attention." 与 061-web-games 的收尾风格同源，简洁克制，可接受 ✅ |

### 9.2 与同类 mindset skill 的对比

- 072-mobile-design（同为移动领域）：20+ 装饰性 emoji + 全大写命令式，🟡 人机感偏机械——082 与之形成鲜明对照，语气干净。
- 061-web-games：同样中性技术语气 + 格言收尾，082 与之同风格。

### 9.3 改进空间（非必改）

1. 全文无任何面向用户的话术示例——agent 如何向用户呈现建议（如"先说结论、再给量化指标"）未定义。这与缺 Output Format 节直接相关。
2. "Remember" 块引用内容略鸡汤（"Respect battery and attention"），若补节时可换成更可操作的收尾（如"给每个建议配一个可测量目标"）。

**结论：人机感合格，无 emoji 滥用、无喊叫腔，是全语料库中语气最干净的 skill 之一。**

---

## §10 SCORING.yaml 审查

### 10.1 结构完整性

```yaml
skill: mobile-games
pattern: mindset
total_items: 15
```

- `total_items: 15` 与实际条目数一致：2 (scope) + 8 (process) + 2 (output) + 2 (negative) + 1 (qa) = 15 ✅
- `pattern: mindset` 与技能性质匹配 ✅（SKILL-SPEC §3.2 mindset ≈ 50 行创意判断类——尽管本 skill 更像"知识表"，见 §5）
- 无 `judge: script` 条目，全部 15 条 `judge: llm` ——与 check.py 空返回一致（见 §11）✅

### 10.2 准则可溯源矩阵

| 准则 | 正文证据源 | 判定 |
|------|-----------|:----:|
| SCOPE-01 | description + §1 | ✅ 证据明确 |
| SCOPE-02 | description（平台/类型要求） | ✅ |
| PROC-01 | §2 44×44pt | ✅ |
| PROC-02 | §2 视觉反馈/避免精确计时 | ✅ |
| PROC-03 | §2 横竖屏 + §6 反模式 | ✅ |
| PROC-04 | §3 热分级表 | ✅ |
| PROC-05 | §3 电池 4 条 | ✅ |
| PROC-06 | §1 仅一行 "Pause in background" | ⚠️ **证据薄弱**（见 10.3） |
| PROC-07 | §4 iOS/Android 各 3 项 | ⚠️ **复合双筒问题**（见 10.3） |
| PROC-08 | §5 4 模型表 | ✅ |
| OUT-01 | 建议的具体性 | ⚠️ 与 OUT-02 部分重叠（见 10.3） |
| OUT-02 | 五约束应用 | ⚠️ 同上 |
| NEG-01 | §2/§6 | ✅ |
| NEG-02 | §3/§6 | ✅ |
| QA-01 | 条件性（如涉代码） | ✅ 条件设计合理 |

### 10.3 准则设计问题

1. **PROC-07 复合双筒**：iOS（隐私标签/账号删除/截图）+ Android（target API/64 位/AAB）合并为一条。若 agent 只针对 iOS 给出完整正确建议，Android 部分如何判定？问题文本用 "as applicable to the chosen platform" 做了对冲，但双筒问题天然增加 LLM judge 的噪声。建议拆为 PROC-07a/07b，或明确"覆盖所选平台的适用项即通过"。
2. **PROC-06 证据地基薄弱**：准则要求 agent 处理后台中断，但正文对中断的指导只有 §1 表格中的一格 "Pause in background"。该准则测量的更多是 agent 先验知识。**修复正文（补节时扩充中断处理）比修改准则更根本**——两者建议联动（见 §13 I9）。
3. **OUT-01 与 OUT-02 语义重叠**：一条问"建议是否具体（44pt、FPS 目标、商店清单）"，一条问"是否把五约束应用到具体游戏"——判定边界模糊，建议合并或差异化（如 OUT-01 专查量化指标，OUT-02 专查针对性应用）。
4. **缺少商店规则红线准则**：§6.3 的 A 项（数字商品必须走 IAP）等规则性知识未反映在任何准则中——若正文补入，可考虑在 PROC-07/08 中增加"变现与商店规则合规"要点。

### 10.4 critical_failures 审查

| ID | 描述 | 判定 |
|----|------|:----:|
| CF-01 | 给移动游戏设计了桌面式控制（精确输入、hover、小目标） | ✅ 与 NEG-01/§2/§6 一致，cap_to_0 合理 |
| CF-02 | 完全无视平台约束（电池/热/商店） | ✅ 与 NEG-02 一致，cap_to_0 合理 |

CF 设计克制、语义清晰，无过度惩罚。可选增强：增加 CF-03"建议违反商店变现规则（如数字内容绕过 IAP）"——若 §6.3 补丁采纳，建议同步添加。

### 10.5 小结

SCORING.yaml 是本 skill 包中**质量最高的组件**：结构完整、与正文 1:1 可溯源、CF 设计合理。问题集中在 3 处准则设计细节（10.3），均属可优化而非错误。

---

## §11 check.py 审查

### 11.1 行为验证

```python
def check(workspace, tool_log, agent_output) -> dict[str, bool]:
    ...
    return result   # 恒为空 dict {}
```

- 与 SCORING.yaml 一致：0 条 `judge: script`，因此返回空 dict 是**正确行为**，非缺陷。
- `main()` 契约（4 个 argv、agent_output 支持文件路径或原文）与 docstring 及 runner 约定一致 ✅。
- `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))` 基于 `__file__` 解析，不依赖 CWD，路径稳健 ✅。
- 导入的 `set_tool_log_path` / `set_agent_output` 均有实际调用，无死导入 ✅（区别于 316 类导虚拟模块的问题）。
- 各准则位点均有注释说明"llm judge (not checked here)"，结构清晰、便于后续把任意准则升级为脚本校验 ✅。

### 11.2 设计评价

**全 LLM 判定对该 skill 是否合理？**

- 合理一面：mindset 类技能输出的本质是"建议的质量与针对性"，难以用正则/文件检查做硬验证；强制硬编码 44/30 FPS 关键词校验反而会催生 agent 机械复读。
- 可议一面：15 条准则零脚本兜底，意味着评测完全依赖 LLM judge 的一致性。本 skill 的准则问题均为可判定性较好的 yes/no 问题（区别于 074 那种需要复算数字的场景），风险可控。
- **结论：维持全 LLM 判定是可接受的设计，不建议为加而加脚本校验。** 唯一可选的低成本脚本项：`output_not_contains` 检查输出是否包含典型桌面术语（hover/right-click）作为 CF-01 的粗糙先行信号——但误报风险高，本审查不推荐。

### 11.3 潜在改进（低优先级）

1. `set_tool_log_path(tool_log)` 被调用但本 skill 无任何 tool-log 校验——无害，保留即可（保持模板一致性）。
2. 可在文件头 docstring 中补充一句"本 skill 刻意全 LLM 判定，原因见 REVIEW §11"（可选，非必需）。

---

## §12 与 Skill Dossier 及姊妹技能对照

### 12.1 Dossier 结论复核

Dossier 082 条目原文要点：

> **逻辑**: 表格原则内部一致，但无 workflow、无输出格式——纯参考表。
> **语法**: 干净可读。
> **人机感**: 中性技术语气；反模式表中的 ❌/✅ 是功能性。
> **合规**: Description 第三人称含触发，但 body 缺全部三必需节，仅 ~108 行。
> **总评**: 🟡 内容正确但结构上是静态备忘单。

**本审查独立复核结论：完全一致**，并补充了三个 Dossier 未覆盖的维度：

1. Dossier 未审 check.py / SCORING.yaml —— 本审查确认评测组件质量高于 SKILL.md 本身（§10/§11）。
2. Dossier 未做事实逐条核验 —— 本审查确认正文零硬伤（§6.1），并发现 5 处精度微调项（§6.2）与 9 项缺失（§6.3）。
3. Dossier 未提语料重叠 —— 见 12.2。

### 12.2 姊妹技能对照（游戏/移动领域）

| Skill | pattern | 评级 | 与 082 的关系 |
|-------|---------|:----:|---------------|
| 061-web-games | mindset | 🟢 | 同 style：表格 + 格言收尾。061 有决策树（框架选择），082 无。061 是"更完整的 082"的参照模板。 |
| 072-mobile-design | tool | 🟡 | React Native UI 细节（组件、API），与 082 在"触控/性能"主题上部分重叠，但粒度不同。 |
| 183-game-art | mindset | 🟡 | 知识清单式、缺三节——与 082 同病相怜，但 183 连决策元素都少。 |
| 276-game-design | mindset | 🟡 | 词典条目式、混入葡语——082 的语言干净度优于它。 |

**重叠分析**：082 与 072 在"触控目标、电池、性能"上存在主题重叠。虽因 pattern 不同（mindset vs tool）不至于需要合并，但建议：

- 在 082 的补节中用 prose 提及姊妹技能（"see also: mobile-design"），符合 SKILL-SPEC §3.3 的允许方式（技能名引用），帮助 agent 在需要 RN 实现细节时转场。
- 保持 082 定位为"平台原则层"，072 为"框架实现层"，避免 082 补节时向实现细节膨胀（否则会与 072 产生真正的内容冗余）。

### 12.3 语料库层面定位

按 Dossier 汇总统计：缺 Scope 节 ~220/322（68%）、缺 Output 节 ~180/322（56%）——082 属"同时缺全部三节"的少数派（该群体主要为知识清单类 mindset skill，如 041、080、183、206）。修复 082 将把该统计样本向合规方向移动一格。

---

## §13 问题清单与修复建议（最长章节）

### 13.1 问题清单总览

| ID | 严重度 | 类别 | 位置 | 问题摘要 |
|----|:------:|------|------|----------|
| I1 | 高 | 规范/逻辑 | SKILL.md 全文 | 缺 Workflow 节：无过程指令，description "build" 场景无正文支撑 |
| I2 | 高 | 规范 | SKILL.md 全文 | 缺 Output Format 节：未定义交付物形态 |
| I3 | 高 | 规范 | SKILL.md 全文 | 缺 Scope/Limitations 节：无边界声明 |
| I4 | 中 | 逻辑 | §2/§3/§5 | 无决策树：变现选型、FPS 选型、热分级判定均无分支条件 |
| I5 | 中 | 准确性 | §4 | 3 处表述精度：截图尺寸、AAB 强制力、target API 口径 |
| I6 | 中 | 内容 | §4/§5 | 缺商店规则红线（IAP 3.1.1、Data Safety、ATT、订阅替代支付） |
| I7 | 低 | 内容 | §3 | 缺帧预算/输入延迟/内存/可访问性等量化与空白维度 |
| I8 | 低 | 内容 | §3/§4 | 2 处精度注脚：OLED 限定、44pt vs 48dp 双口径 |
| I9 | 中 | 评测 | SCORING.yaml | PROC-07 双筒、PROC-06 证据薄弱、OUT-01/02 重叠、可加商店规则准则 |
| I10 | 低 | 评测 | check.py | 维持全 LLM 判定合理；可选补充注释（无必改项） |
| I11 | 低 | 规范 | SKILL.md 体量 | 正文 101 行 ≈ mindset 目标 2 倍；补节时注意总行数控制 |
| I12 | 低 | 语料 | 跨技能 | 与 072-mobile-design 主题重叠；建议 prose 互引、分层定位 |

### 13.2 分项修复建议

#### I1+I2+I3（高优先，可一次完成）— 补三必需节

**推荐插入位置**：§6 反模式之后、"Remember" 块引用之前。新增三个 H2 小节，将原"Remember"移为 §9 或并入新 Output 节尾部。

**I1 — `## 7. Workflow`（过程节）**，内容骨架：

1. **Step 1 — Pin the platform and genre**：先确认目标平台（iOS / Android / 双平台）与游戏类型（休闲/竞技/叙事/放置等），未明确时先询问或声明假设。平台决定 §4 清单，类型决定 §3 FPS 档位与 §5 变现模型。
2. **Step 2 — Apply the five constraints**：按 §1 表格逐项过一遍触控/电池/热/屏幕/中断对当前游戏的落点，每项给出量化建议（触控 ≥44pt、帧预算、休眠策略等）。
3. **Step 3 — Choose the monetization model**：按 §5 表 + 决策条件（见 I4 决策树）选择并给出理由。
4. **Step 4 — Run the store checklist**：按目标平台执行 §4 清单（含 I6 补充的 Data Safety/ATT 项）。
5. **Step 5 — Anti-pattern sweep**：按 §6 表核查输出，确认无桌面化控制、无强制横屏、无常驻联网。

每步一行说明 + 明确的"完成标志"，保持 mindset 的轻量（每步 1-2 行，勿膨胀为 process 的 200 行）。

**I2 — `## 8. Output Format`（输出节）**，内容骨架：

- 交付物 = 三件套：(a) **约束落点表**——五约束 × 当前游戏的具体建议与量化目标；(b) **决策说明**——变现模型选择及理由、FPS 档位及理由；(c) **商店就绪清单**——按平台勾选（隐私声明、账号删除、截图尺寸、target API、64 位、AAB、Data Safety/ATT）。
- 格式要求：每条建议必须带量化指标或具体配置项（"降低特效质量"不合格，"目标 30fps、热时降至 24fps 并关闭粒子"合格）——呼应 OUT-01 准则。
- 可选附一个 1 个平台 × 1 个游戏类型的迷你示例（5-8 行），示范约束落点表的写法。

**I3 — `## 9. Scope & Limitations`（边界节）**，内容骨架：

- **本技能覆盖**：平台原则与发布准备的决策级建议。
- **本技能不覆盖**：Web/桌面/主机游戏（见 061-web-games）；React Native/Unity/Unreal 实现细节（见 mobile-design）；ASO 与买量投放；游戏数值/经济设计；商店条款的法律解读（法务边界）；xcode/android-studio 构建操作（工具受限，不执行构建）。
- **何时不使用**：用户目标是桌面/网页游戏、用户要的是引擎教程或具体 API 代码、用户要求法律条款裁决时。

#### I4（中优先）— 补 3 张决策树

**变现决策树**（插入 §5 表下方，遵循 §3.4 "decision trees over prose"）：

| 条件 | 模型 |
|------|------|
| 数字内容/增值服务直接销售 | 免费+IAP（注意：iOS 数字商品必须走 IAP，见 I6） |
| 高频复玩 + 大用户量 | 免费 + 广告（注意 ATT 对 eCPM 的影响） |
| 内容持续更新 / 多人服务型 | 订阅（注意部分地区替代支付义务） |
| 口碑型单次购买、低复玩 | 付费买断 |

**FPS 选型**（插入 §3）：休闲/卡牌/放置 → 30fps；动作/竞速/竞技 → 60fps（或 120 高刷）；帧预算 16.7ms/33.3ms 对应给到具体数字。

**热分级判定**（插入 §3）：从 OS 温度 API（iOS `ProcessInfo.thermalState` / Android `PowerManager` 温度回调）读取状态 → 按 §3 表降级；何时恢复（温度回落）也需一行说明。

#### I5（中优先）— §4 三处精度修正

| 原文 | 修正 |
|------|------|
| Screenshots: For all device sizes | Screenshots: largest + smallest supported display sizes |
| App bundles: Recommended | App bundles: Required for new apps (since Aug 2021) |
| Target API: Current year SDK | Target API: Within one year of latest API level (API 35/36 as of 2025-26) |

#### I6（中优先）— §4/§5 补商店规则红线

在 §4 增加第 3 行或脚注：

- iOS：App Privacy（声明）+ App Tracking Transparency（广告场景必配）+ 数字商品必须 IAP（Guideline 3.1.1）。
- Android：Play Data Safety 表单 + 订阅替代支付（欧盟 DMA 等地区）。
- 通用：说明"变现模型建议不得与商店规则冲突"是 §5 的前置约束。

#### I7（低优先）— 空白维度补充

- §3 增加"Memory"行：iOS memory warning / Android LMK，缓存清理策略。
- §3 增加帧预算数字与输入延迟目标（≤100ms 感知）。
- 新增（或并入 §2）可访问性要点：Dynamic Type 支持、VoiceOver/TalkBack 语义标注、触控辅助兼容。

#### I8（低优先）— 精度注脚

- "Dark mode saves OLED battery" → 加注 "(OLED only)"。
- §2 最佳实践加注 "44×44 pt (iOS) / 48×48 dp (Material)"。

#### I9（中优先）— SCORING.yaml 联动修改

| 动作 | 内容 |
|------|------|
| 拆分 PROC-07 | 拆为 PROC-07a（iOS：隐私标签/账号删除/截图）/ PROC-07b（Android：target API/64 位/AAB），`total_items` 15→16 |
| 强化 PROC-06 地基 | 先补正文（I1 的 Step 2 含中断落点），再维持准则不变；若正文不补，则在准则 question 中弱化到"提及暂停行为即可" |
| 合并或差异化 OUT-01/02 | 建议：OUT-01 专查量化指标（44pt/FPS/清单），OUT-02 专查针对性（是否落到具体游戏），在 question 文本中显式划界 |
| 新增准则（可选） | PROC-09：变现建议不与商店规则冲突（数字内容走 IAP 等）——依赖 I6 补丁落地 |
| 新增 CF-03（可选） | "建议规避商店支付规则（如数字内容绕开 IAP）" → cap_to_0。注意：CF 过多会降低评测区分度，本审查建议仅当 I6 落地且实测 judge 区分度不足时再加 |

#### I10（低）— check.py

无必改项。可选：在文件头 docstring 注明"全 LLM 判定的设计理由（mindset 输出难以脚本硬验）"，帮助后续维护者理解。若采纳 I9 新增脚本可验项（本审查不推荐），此处再行补充。

#### I11（低）— 体量控制

补节后预计正文 ~180-220 行，仍 ≤600 硬上限 ✅，且维持 mindset 的"轻量加载"特性（061-web-games 为 145 行、077-takedown 为 387 行的 process——082 补节后仍处于 mindset 合理区间）。**约束**：Workflow 每步 ≤2 行、决策树一律表格化、不引入 references/ 子目录（当前自包含结构是优点）。

#### I12（低）— 语料协同

- 在 I3 的 Scope 节中以 prose 引用："see also: mobile-design (React Native UI implementation)"。
- 不在 082 中展开任何 RN/Unity 实现细节，把实现层留给 072。
- 反向：可在 072 的 Scope 中互提（跨 skill 动作，超出本次审查范围，仅建议）。

### 13.3 修复补丁草案（可直接采用）

以下为按 I1-I3 + I4 + I5 生成的英文补丁文本，插入于 §6 反模式表之后、"Remember" 之前：

```markdown
## 7. Workflow

1. **Pin the platform and genre.** Confirm iOS, Android, or both, and the game type
   (casual, action, narrative, idle, ...). State assumptions when unspecified.
2. **Apply the five constraints.** Walk the §1 table against this specific game and
   produce quantified guidance for each constraint (touch targets, frame budget,
   sleep behavior, memory policy, orientation).
3. **Choose the monetization model.** Use the §5 decision table, and verify the choice
   against store rules (§4) — e.g., digital goods must use IAP on iOS.
4. **Run the store checklist.** Execute the §4 list for the target platform, including
   App Privacy / Data Safety, account deletion, screenshots, target API, 64-bit, AAB.
5. **Anti-pattern sweep.** Re-check §6: no desktop-style controls, no forced
   orientation, no always-on networking.

## 8. Output Format

Deliver three artifacts:

- **Constraint map** — one row per constraint (touch, battery, thermal, screen,
  interruptions), each with a concrete target: "44 pt touch targets, 30 FPS,
  sleep after 5 s in background" (not vague advice).
- **Decision notes** — monetization model chosen from §5 with a one-line reason;
  FPS tier chosen from §3 with the frame budget (16.7 ms @ 60 FPS, 33.3 ms @ 30 FPS).
- **Store readiness checklist** — platform-specific, checked off, with the
  blocking items flagged (privacy declarations, account deletion, target API
  level, 64-bit, AAB).

## 9. Scope & Limitations

- **Covers**: decision-level guidance on platform constraints, touch input,
  performance, monetization, and store release preparation.
- **Does not cover**: web/desktop/console games (see also: web-games); React
  Native or engine implementation details (see also: mobile-design); ASO or
  user acquisition; game economy design; legal interpretation of store terms.
- **When not to use**: the target is a desktop or web game; the user wants an
  engine tutorial or specific API code; the question requires legal judgment.
```

以及 §3 插入的量化补充（在 Battery Optimization 列表尾部追加两行）：

```markdown
- Frame budget: 16.7 ms @ 60 FPS, 33.3 ms @ 30 FPS; pick the tier by genre
- Input latency target: ≤100 ms perceived; measure on real devices, not emulators
- Memory: respond to iOS memory warnings / Android low-memory kills by trimming
  caches and lowering texture resolution (adds the missing memory dimension)
```

### 13.4 修复后验证清单

补丁落地后按 SKILL-SPEC §5 合规清单复验：

- [ ] body ≤600 行（预计 180-220）
- [ ] 存在 workflow/process 节（新 §7）
- [ ] 存在 output format 节（新 §8）
- [ ] 存在 scope/limitations 节（新 §9）
- [ ] 无跨 skill 文件路径（"see also" 为 prose 技能名引用，合规）
- [ ] description 无需改动（已合规）
- [ ] SCORING.yaml `total_items` 与准则数一致（若采纳拆分，15→16）
- [ ] 决策树全部表格化，无 prose 长段落膨胀
- [ ] 原 6 小节内容零删改（本方案为纯增量修复）

### 13.5 优先级与排期建议

| 批次 | 内容 | 预期效果 |
|------|------|----------|
| **P0（1 次提交）** | I1+I2+I3 补三节 + I4 决策树 + I5 精度修正 | 硬性规范缺口清零，评级 🟡→🟢 |
| **P1（同日）** | I6 商店规则红线 + I7 量化/可访问性 + I8 注脚 | 内容完整性达标，评测可信度提升 |
| **P2（随评审周期）** | I9 SCORING.yaml 联动 + I12 语料互引 | 评测体系与语料协同优化 |
| **不改** | I10 check.py（维持全 LLM 判定） | 避免为加而加 |

### 13.6 修复完成后的预期评级

- **修复前**：🟡（内容正确、描述合规、评测完整，但三必需节全缺——严格按 §3.1 应判 🟠）
- **修复后**：🟢（参照 061-web-games 🟢 的标准：结构化、可执行、决策链完整、保持轻量）

---

## 附：审查结论摘要

| 维度 | 结论 | 关键依据 |
|------|:----:|----------|
| Frontmatter 合规 | ✅ | name/description/allowed-tools 全过，无违禁字段 |
| Description 合规 | ✅ | 三要素齐备 + 标准触发信号 + 第三人称 |
| Body 必需节 | ❌ | Workflow/Output/Scope 三节全缺（本审查核心发现） |
| 内容准确性 | ✅ | 零硬伤；5 处精度微调 + 9 项缺失 |
| 逻辑一致性 | ✅ | 表内自洽、与 SCORING 1:1 可溯源；缺决策链 |
| 语法可读性 | ✅ | 零拼写/格式缺陷 |
| 人机感 | ✅ | 语气干净，语料库最佳之一 |
| SCORING.yaml | ✅ | 结构完整；3 处准则设计细节可优化 |
| check.py | ✅ | 空返回正确；全 LLM 判定对 mindset 合理 |
| 与 Dossier 对照 | ✅ | 结论一致；本审查新增评测组件与语料维度 |
| **总评** | **🟡** | **需补三节后回 🟢；修复为纯增量、低风险** |
