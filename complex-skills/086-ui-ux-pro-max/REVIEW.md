# REVIEW — 086-ui-ux-pro-max

- 审查日期: 2026-08-06
- 审查人: SkillIF 复审 Agent（全文件级审查）
- 审查对象: `D:\SkillIF\skill-experiment\complex-skills\086-ui-ux-pro-max\` 全部 28 个文件
- 审查依据: `_shared/SKILL-SPEC.md` v1.0、技能目录内 `SCORING.yaml`、`check.py`、dossier（`skill-dossier.md` 中 086 条目）
- 总体评级: 🟡 可用但有小问题（与 dossier 086 条目一致；但本复审发现的新问题比 dossier 记录的更严重，见 §13）

---

## 1. 审查概述

### 1.1 审查范围

本 REVIEW 覆盖技能目录下的全部文件：

| 类别 | 文件数 | 内容 |
|------|:----:|------|
| 主文档 | 2 | SKILL.md、SCORING.yaml |
| 校验脚本 | 1 | check.py |
| 运行脚本 | 3 | scripts/core.py、scripts/search.py、scripts/design_system.py |
| 数据文件 | 12 | data/ 下 12 个 CSV（含 ui-reasoning.csv） |
| Stack 数据 | 11 | data/stacks/ 下 11 个 CSV |

### 1.2 审查方法

1. **静态审查**: 逐文件通读 SKILL.md、SCORING.yaml、check.py、3 个 Python 脚本和全部 23 个 CSV（1335 行数据记录）。
2. **规范对照**: 逐条对照 SKILL-SPEC.md v1.0 的五章要求（frontmatter、description、body 结构、目录命名、合规清单）。
3. **评分对齐**: 核对 SCORING.yaml 的 21 条 criteria 与 check.py 中 5 条脚本判定的实现一致性。
4. **运行时验证**: 对 3 个 Python 脚本执行 `py_compile` 编译检查，并实际运行 `search.py` 的域搜索与 `--design-system` 两种模式，复现了 Windows 控制台下的崩溃缺陷（见 §8、§13 的 I-01）。

### 1.3 与 dossier 的关系

dossier 中 086 条目（🟡）记录了两个问题："frontmatter 数字与 body 矛盾（21 vs 97 调色板、50 vs 57 字体配对）"、"硬编码 CLI 路径不可移植"。本复审确认这两点成立，并**新增发现**了 3 个 dossier 未记录的问题：

- **I-01（P0）**: `search.py` 在 Windows 默认 GBK 控制台直接崩溃（UnicodeEncodeError），而 SKILL.md 明确把 Windows 列为受支持平台——"MANDATORY" 的 `--design-system` 命令开箱即崩。
- **I-05（P1）**: `ui-reasoning.csv` 的 `Decision_Rules` JSON 大量存在重复 `"must_have"` 键，`json.loads` 静默保留末值，约束被悄悄丢弃。
- **I-07（P1）**: `colors.csv` 95 个调色板中约 60 个是同一组默认蓝色十六进制值，Notes 与 Hex 内容不匹配（如"Dark + Status indicator colors"配浅蓝 hex）。

---

## 2. 目录全量清单与文件盘点

### 2.1 文件清单（28 个）

```
086-ui-ux-pro-max/
├── SKILL.md                    (350 行)
├── SCORING.yaml                (21 criteria + 3 critical_failures)
├── check.py                    (85 行)
├── scripts/
│   ├── core.py                 (258 行)
│   ├── search.py               (77 行)
│   └── design_system.py        (488 行)
└── data/
    ├── styles.csv              (58 行数据记录)
    ├── colors.csv              (95)
    ├── icons.csv               (100)
    ├── landing.csv             (29)
    ├── products.csv            (95)
    ├── prompts.csv             (23)
    ├── react-performance.csv   (44)
    ├── typography.csv          (56)
    ├── ui-reasoning.csv        (100)
    ├── ux-guidelines.csv       (98)
    ├── web-interface.csv       (30)
    ├── charts.csv              (24)
    └── stacks/                 (11 个文件, 共 583 行记录)
        ├── html-tailwind.csv   (55)   ├── react.csv      (53)
        ├── nextjs.csv          (52)   ├── vue.csv        (49)
        ├── nuxtjs.csv          (58)   ├── nuxt-ui.csv    (50)
        ├── svelte.csv          (53)   ├── swiftui.csv    (50)
        ├── react-native.csv    (51)   ├── flutter.csv    (52)
        └── shadcn.csv          (60)
```

数据记录合计：主域 CSV 752 条 + stack CSV 583 条 = **1335 条设计规则记录**。

### 2.2 结构评价

- 目录名 `086-ui-ux-pro-max`：小写 + 连字符 + 三位序号，符合 SKILL-SPEC §4。✅
- 目录内无跨技能引用（无 `../other-skill/` 路径）；`check.py` 引用 `../_shared/checker.py` 属评估基础设施，不算技能运行时依赖。✅
- 数据、脚本、文档三层职责划分清晰，是本次审查中"工具型 skill"里组织最完整的目录之一。

---

## 3. Frontmatter 逐字段审查

### 3.1 字段清单

```yaml
---
name: ui-ux-pro-max
description: UI/UX design intelligence covering 50 design styles, 21 color palettes,
  50 font pairings, 20 chart types, and 9 technology stacks (React, Next.js, Vue,
  Svelte, SwiftUI, Flutter, and more). Use when the user needs UI/UX design guidance,
  design system recommendations, component design patterns, or visual design decision
  support.
---
```

### 3.2 逐项合规结论

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| `name` 小写字母+连字符 | ✅ | `ui-ux-pro-max` |
| `name` ≤ 64 字符 | ✅ | 15 字符 |
| `name` 与目录名一致 | ✅ | `086-ui-ux-pro-max` |
| `description` 第三人称 | ✅ | "UI/UX design intelligence..."，非祈使/第一/第二人称开头 |
| `description` ≤ 1024 字符 | ✅ | 约 360 字符 |
| 含触发信号短语 | ✅ | "Use when the user needs..."（满足 §2.4） |
| WHAT 具体性 | ✅ | 列出了覆盖范围（styles/palettes/fonts/charts/stacks） |
| WHEN 触发场景 | ✅ | design guidance / design system recommendations / component patterns / visual decision support |
| KEYWORDS 密度 | ✅ | 含 UI/UX、design、component、visual 等匹配词 |
| 无跨技能路由 | ✅ | 未出现 "NOT for X, use Y" |
| 无禁止字段 | ✅ | 仅有 name + description 两个键，无 `metadata/version/tags/trigger` 等 |

### 3.3 事实性问题（重点缺陷）

description 中的数字与正文、与数据层三方不一致（详见 §10.1 和 §13 的 I-03）：

- **"50 design styles"** — 实际 `styles.csv` 有 **58** 条样式记录（STT 1-58）。
- **"21 color palettes"** — 实际 `colors.csv` 有 **95** 条调色板；正文又声称 **97**。
- **"50 font pairings"** — 实际 `typography.csv` 有 **56** 条；正文声称 **57**。
- **"20 chart types"** — 实际 `charts.csv` 有 **24** 条；正文声称 **25**。
- **"9 technology stacks"** — SKILL.md 正文列出 9 个栈，但 `core.py` 的 `STACK_CONFIG` 和数据目录实际有 **11** 个栈（`nuxtjs`、`nuxt-ui` 未被正文收录）。

dossier 记录为"21 vs 97、50 vs 57"的矛盾，本复审确认并扩展为 5 组数字、三处来源（description/body/data）全部对不齐。

---

## 4. Description 专项审查

### 4.1 结构模板对照（SKILL-SPEC §2.2）

`<what> + Use when the user <trigger scenarios>` 模板命中：✅

### 4.2 人称与语气（§2.3）

- 第三人称 ✅，无 "I can help / We provide / You can use"。
- 无祈使句开头 ✅。

### 4.3 触发信号（§2.4）

"Use when the user needs..." 是规范列举的合法信号之一。✅

### 4.4 避免项（§2.5）

- 无跨技能路由 ✅
- 非空泛描述（"A useful skill" 类）✅
- 长度 > 40 字符 ✅

### 4.5 结论

Description 的**结构完全合规**，但**内容数字全部失实**（见 3.3）。由于 description 是触发匹配与前端展示的核心字段，数字失实会直接误导调用方对技能能力的预期（例如调用方以为只有 21 个调色板，实际 95 个；或正文声称 97 个实际 95 个——少报 2 个）。这属于"可用但有明显瑕疵"，评级 🟡 的依据之一。

---

## 5. Body 结构审查

### 5.1 行数与节结构

- 全文 **350 行** ≤ 600 硬上限 ✅（tool pattern 目标 ~300 行，实际 350，合理）
- 标题结构（H1 + 11 个 H2）：
  1. When to Apply
  2. Rule Categories by Priority
  3. Quick Reference（8 大规则类，含优先级表）
  4. How to Use（过渡段）
  5. Prerequisites
  6. How to Use This Skill（Step 1-4 工作流）
  7. Search Reference（Domains 表 / Stacks 表）
  8. Example Workflow
  9. Output Formats
  10. Tips for Better Results
  11. Common Rules for Professional UI（4 组 Do/Don't 表）
  12. Pre-Delivery Checklist

### 5.2 三必需节对照（SKILL-SPEC §3.1）

| 必需节 | 存在? | 说明 |
|--------|:----:|------|
| Workflow / Process | ✅ | "How to Use This Skill" 四步：分析需求 → `--design-system`（MANDATORY）→ 域搜索补充 → stack 指南 |
| Output Format | ✅ | "Output Formats" 节描述 ASCII box / Markdown 两种输出；"Pre-Delivery Checklist" 补充交付要求 |
| Scope / Limitations | ❌ | **全文无 Scope、Limitations、"What This Skill Does NOT Do" 类章节**。"Do Not Use For" 仅存在于 styles.csv 数据列，未上提到文档层 |

Scope 缺失是 SKILL-SPEC 合规清单中明确列出的检查项（"body: has scope/limitations section"），也是本语料库 322 个技能中 ~68% 的共同缺口（dossier 统计）。**I-02（P1）**。

### 5.3 路径与命令引用

- 所有 CLI 命令硬编码 `python3 .claude/skills/ui-ux-pro-max/scripts/search.py`。该路径只对"已安装到 `~/.claude/skills/` 的 Claude Code 插件布局"成立；对 SkillIF 语料库布局（`complex-skills/086-ui-ux-pro-max/scripts/search.py`）失效。**I-04（P1，dossier 已记录）**。建议改为"以技能目录为基准的相对路径"或给出两种布局的指引。
- 命令统一用 `python3`，而 Prerequisites 中 Windows 安装指引（`winget install Python.Python.3.12`）安装的是 `python`/`py`，Windows 上未必有 `python3` 命令。`python3 --version || python --version` 的容错只出现在版本检查，后续所有搜索命令仍写死 `python3`。与 I-01 叠加后，Windows 上该技能"开箱即不可用"。

### 5.4 内容密度

- "Common Rules for Professional UI" 四张 Do/Don't 表（Icons、Interaction、Light/Dark Contrast、Layout）是**全 skill 知识增量最高**的部分，给出了具体值（`bg-white/80`、`#0F172A`、`#475569`、`border-gray-200`、`top-4 left-4 right-4`、`max-w-6xl/7xl`），符合 §3.4"Concrete over abstract"。
- Quick Reference 8 类规则与优先级表一一对应，无冗余重复。
- 无明显重复段、无脚手架残留（对比 004 的 "(New!)"、055 的 "the `..` skill" 占位符，本技能干净）。

---

## 6. 数据层审查（23 个 CSV）

### 6.1 数据量核对（对照 SKILL.md 正文声明）

| 声明（正文） | 实际数据行数 | 差值 |
|--------------|:----:|:----:|
| "50+ styles" | 58 | ✅ 成立 |
| "97 color palettes" | 95 | 差 2（**I-03**） |
| "57 font combinations" | 56 | 差 1（**I-03**） |
| "99 UX guidelines" | 98 | 差 1（**I-03**） |
| "25 chart types" | 24 | 差 1（**I-03**） |
| "9 technology stacks" | 11 个 CSV | 差 2（nuxtjs/nuxt-ui 未入正文，**I-06**） |

差值呈稳定的"少 1~2"，疑似正文数字直接从 STT 序号最大值抄录但数据行数在之后有过删改，未同步。

### 6.2 各文件内容质量

**styles.csv（58 条）— 质量中等**
- 18 列 schema 完整；每行含 Primary/Secondary Colors、Effects & Animation、Performance、Accessibility、Framework Compatibility、Era/Origin、Complexity，信息密度高。
- **重复**: "Neubrutalism" 出现两次（STT 38 与 STT 54）；"Bento Box Grid"（STT 39）与 "Bento Grids"（STT 53）为近似重复概念（**I-07**）。
- **schema 不一致**: STT 21-37（Landing Page / BI-Analytics 类型共 16 行）只写到 `Conversion-Focused` 列为止，缺少末尾的 `Framework Compatibility`、`Era/Origin`、`Complexity` 三列。CSV 按行解析不报错，但搜索结果中这些行的对应字段会静默为空（**I-07**）。
- `Prompts.csv` 只覆盖 23/58 个样式，覆盖缺口 ~60%（**I-08**）。

**colors.csv（95 条）— 质量偏差（I-07）**
- 约 60+ 行的 Hex 值完全相同（Primary #3B82F6 / Secondary #60A5FA / CTA #F97316 / BG #F8FAFC / Text #1E293B / Border #E2E8F0 的"默认蓝"组），仅 Notes 不同。
- Notes 与 Hex 不匹配的典型行：
  - "Smart Home/IoT Dashboard"：Notes 写 "Dark + Status indicator colors"，Hex 却是浅蓝亮底；
  - "Sustainability/ESG Platform"：Notes 写 "Green (#228B22) + Earth tones"，Hex 是紫色 #7C3AED 组；
  - "Airline"：Notes 写 "Sky Blue + Brand colors"，Hex 是紫色 #7C3AED 组；
  - "Cybersecurity"：CTA (#00FF41) 与 Primary (#00FF41) 相同，且 Secondary #0D0D0D 用作按钮色风险存疑。
- 后果：BM25 检索不同产品类型时大概率返回同一组"默认蓝"，design-system 输出丧失差异化——直接削弱本技能的核心卖点。

**typography.csv（56 条）— 质量良好**
- Google Fonts URL、CSS Import、Tailwind Config 三列齐全且格式统一，可直接复制。
- 4 行（STT 20/39/50/52 等）的 Heading/Body 字体名是 Fontshare 字体（Satoshi、General Sans、Clash Display），URL/CSS 列却给的是 Google 替代字体，仅靠 Notes 标注——agent 若直接复制 CSS Import 会得到与字体名不同的字体（低危，已自证，**I-09**）。

**charts.csv（24 条）— 质量高**
- 每行含 Color Guidance、Performance Impact、Accessibility Notes、Library Recommendation、Interactive Level 五列，彩色盲/可访问性提示（pattern overlay、data table alternative）贯穿全文，是本技能数据层最扎实的文件。
- STT 8 "Performance vs Target" 与 STT 18 "Performance vs Target (Compact)" 概念重复（低危）。

**ux-guidelines.csv（98 条）— 质量高**
- 10 列规范，覆盖 Navigation/Animation/Layout/Touch/Interaction/Accessibility/Performance/Forms/Responsive/Typography/Feedback/Content/Onboarding/Search/Data Entry/AI Interaction/Spatial UI/Sustainability 18 类，每行 Do/Don't/Code Good/Code Bad 四件套，是本文件集里执行度最高的规则库。

**web-interface.csv（30 条）/ react-performance.csv（44 条）— 质量良好**
- web-interface 含 Critical 级聚焦要点（focus-visible、never disable zoom、outline replacement）。
- react-performance **I-10（P2）**: STT 4 "Dependency Parallelization" 推荐使用 `better-all` 库（`await all({ user() {}, ... })`）——`better-all` 并非广为人知的 npm 包，疑似虚构/幻觉依赖。若 agent 按此生成代码，交付物会引用不存在的库。

**icons.csv（100 条）— 质量良好但单一**
- 全部来自 Lucide，Import Code 可直接粘贴。SKILL.md 提到 Heroicons/Simple Icons，数据层却只有 Lucide——与 SKILL.md 正文轻微不一致（低危）。

**ui-reasoning.csv（100 条）— 结构优秀，数据缺陷（I-05）**
- 100 个产品类别 × (Recommended_Pattern / Style_Priority / Color_Mood / Typography_Mood / Key_Effects / Decision_Rules / Anti_Patterns / Severity)，是 design-system 生成器的推理核心。
- **JSON 重复键**: 约 40+ 行的 `Decision_Rules` 含多个重复的 `"must_have"` 键（如 STT 10 `{"must_have": "wcag-aaa", "must_have": "keyboard-navigation"}`、STT 19 双 `"must_have"` 等）。`json.loads` 遇重复键保留**末值**，前一个约束被静默丢弃——`wcag-aaa` 这类关键约束会消失（**I-05，P1**）。
- Anti_Patterns 列大量出现 "AI purple/pink gradients"，与"AI-Native UI"风格行（STT 48 推荐 AI Purple #6366F1）自相矛盾（低危，**I-11**）。

**landing.csv（29 条）— 质量良好**
- STT 27-30（Horizontal Scroll Journey / Bento Grid Showcase / Interactive 3D Configurator / AI-Driven Dynamic Landing）末字段缺闭合引号、Conversion Optimization 信息被截断（如 "Keep navigation visible." 戛然而止）——CSV 解析不报错但内容不完整（低危）。

**stack CSV（11 个）— 整体质量高**
- 统一 9 列 schema（Category/Guideline/Description/Do/Don't/Code Good/Code Bad/Severity/Docs URL），Do/Don't/代码三件套齐全；shadcn.csv（60 条）与 react.csv（53 条）覆盖度最高；nuxt-ui.csv 的 U 前缀组件约定与 v-model:open 用法准确。

### 6.3 数据层小结

数据量级（1335 条）是本技能最大的资产，且 ux/web/charts/stacks 四类文件质量显著高于 colors/styles 两类。**主要风险集中在 colors.csv 的"默认蓝"复制、ui-reasoning.csv 的 JSON 重复键、styles.csv 的重复条目与缺列**。

---

## 7. 脚本实现审查

### 7.1 core.py（258 行）— 质量良好

- BM25 实现正确：IDF 用平滑 `log((N-f+0.5)/(f+0.5)+1)`，k1/b 参数标准，`score > 0` 过滤合理，tokenize 会过滤 ≤2 字符的停用词。
- `CSV_CONFIG` 11 域 / `STACK_CONFIG` 11 栈与数据文件一一对应，无悬空引用。
- `detect_domain` 用子串命中计数选择域，兜底 `style`——测试 `"accessibility keyboard"` 正确落到 `ux` 域。
- 小缺陷：
  - `search_stack` 的友好报错（"Unknown stack..."）在 CLI 下是**死代码**——argparse 的 `choices` 先行拦截，非法栈名直接打 usage（运行时已验证，见 §8）；
  - `_search_csv` 对结果 `score > 0` 过滤后可能返回 0 条且无提示，`Found: 0 results` 需要调用方自行理解。

### 7.2 search.py（77 行）— 存在缺陷

- **I-01（P0）**: 两种输出路径（`print(format_output(result))` 与 `print(result)`）在 Windows 默认 GBK 控制台下均抛 `UnicodeEncodeError`（数据中的 ⚡/⚠/✓/❌ 字符无法编码）。SKILL.md 把 Windows 列为受支持平台且给出了 winget 安装指引，但没有任何关于 `PYTHONIOENCODING` 或 `chcp 65001` 的说明——"MANDATORY" 的第一步命令在 Windows 上开箱即崩。见 §8 复现。
- **I-06（P2）**: 文档字符串与 `--stack` help 均写死 "Stacks: html-tailwind, react, nextjs"，实际支持 11 个栈；"Domains: style, prompt, color, chart, landing, product, ux, typography" 同样漏掉 icons/react/web 三域。
- `--json` 与 `--design-system` 同时传入时，`--json` 被静默忽略（design-system 分支优先且只支持文本输出）——未在 help 中说明。

### 7.3 design_system.py（488 行）— 质量良好，两处隐患

- 生成器逻辑正确：product 检索定类别 → `_apply_reasoning` 取推理规则 → 5 域并行检索（与 SKILL.md "Searches 5 domains in parallel" 声明一致）→ 按 style_priority 择优 → 输出含 anti-patterns 与 pre-delivery checklist。
- `_find_reasoning_rule` 的 exact/partial/keyword 三级匹配设计稳健；无规则时返回合理兜底（Minimalism + Flat Design）。
- 隐患 1：`Decision_Rules` 的重复键问题（I-05）在 `_apply_reasoning` 的 `json.loads` 处爆发，且**静默**。
- 隐患 2：`format_ascii_box` 将 styles.csv 的 `✓/⚡/⚠` 字符原样带进输出（`perf_a11y` 一行），这就是 I-01 崩溃的直接来源；`format_markdown` 同样泄漏这些字符。
- 亮点：ASCII box 的宽度计算（90+1）自洽；markdown 输出含 Colors 表、Typography CSS Import 代码块、Pre-Delivery Checklist，可直接转交实现。

### 7.4 check.py（85 行）— 与 SCORING.yaml 对齐良好

- `sys.path.insert(0, "../_shared")` 并 `from checker import tool_log_contains, tool_log_order`——`_shared/checker.py` 确实存在（已核实）。✅
- 实现 5 条脚本判定：SCOPE-03、SCOPE-04、OUT-01、OUT-04、NEG-02，与 SCORING.yaml 中 `judge: script` 的条目完全一一对应（见 §9）。✅
- 代码注释中逐条标注了 16 条 LLM 判定项"not checked here"，评审可审计。✅

---

## 8. 运行验证（实测）

### 8.1 编译检查

```
python -m py_compile scripts/core.py scripts/search.py scripts/design_system.py check.py
→ COMPILE_OK（四个脚本语法全部通过）
```

### 8.2 崩溃复现（I-01）

在 Windows 默认控制台（GBK 代码页）下：

```
$ python scripts/search.py "saas dashboard" --domain style
Traceback ... UnicodeEncodeError: 'gbk' codec can't encode character '\u26a1'
in position 672: illegal multibyte sequence

$ python scripts/search.py "fintech crypto dashboard" --design-system -f markdown
Traceback ... UnicodeEncodeError: 'gbk' codec can't encode character '\u26a0'
in position 466: illegal multibyte sequence
```

- `\u26a1`（⚡）来自 styles.csv 的 Performance 列，`\u26a0`（⚠）来自其 Accessibility 列。
- **两种模式全部崩溃**，包括 SKILL.md 标注为 MANDATORY 的 `--design-system`。这是本技能当前最严重的运行时缺陷。
- 若评估 Runner 在 Windows 上以默认代码页运行 agent，SCOPE-03/CF-01 依赖的 `--design-system` 命令必然失败。

### 8.3 绕过验证（证明功能本身正常）

```
$ PYTHONIOENCODING=utf-8 python scripts/search.py "fintech crypto dashboard" --design-system -f markdown
→ 正常输出：Pattern=Conversion-Optimized；Style=Glassmorphism；
  Colors: #F59E0B/#FBBF24/#8B5CF6/#0F172A/#F8FAFC；
  Typography: Orbitron/Exo 2（带 Google Fonts URL 与 CSS Import）
```

输出内容与 ui-reasoning.csv STT 6（Fintech/Crypto）的规则完全对应，端到端管线（product → reasoning → style/color/typography 择优）工作正常。

### 8.4 其他行为验证

| 场景 | 结果 |
|------|------|
| `--stack bogus` | argparse usage 报错（友好报错为死代码，见 §7.1） |
| 自动域检测 `"accessibility keyboard"` | 正确落到 `ux` 域，返回 Keyboard Navigation 等 2 条 |
| `--domain` choices | 列出全部 11 域（含未入正文的 icons/react/web） |
| `--stack` choices | 列出全部 11 栈（含未入正文的 nuxtjs/nuxt-ui） |

---

## 9. SCORING.yaml 与 check.py 一致性审查

### 9.1 总数核对

- SCORING.yaml `total_items: 21` = 4 scope + 7 process + 4 output + 2 negative + 4 qa。✅
- 21 条中 `judge: script` 的恰为 5 条：SCOPE-03、SCOPE-04、OUT-01、OUT-04、NEG-02；`check.py` 恰好实现这 5 条且无多余/缺失。✅ 其余 16 条 `judge: llm` 由 `check.py` 注释明确标注为 "not checked here"。✅

### 9.2 关键判定逻辑审查

| 条目 | 逻辑 | 评估 |
|------|------|------|
| SCOPE-03 | `tool_log_order('search\.py.*--design-system', 'Write')` — design-system 搜索必须先于任何 Write | 严格但合理，与正文 "MANDATORY" 一致；与 CF-01 同源 |
| SCOPE-04 | `search\.py.*(--domain\|--stack)` | 要求至少一次域/栈搜索；注意若 agent 只用 design-system 不补搜，此项不通过 |
| OUT-01 | `heroicons\|lucide\|simple-icons\|simpleIcons` | 只匹配工具日志中出现图标库名；icons.csv 数据只有 Lucide，无 Heroicons/Simple Icons 数据支撑，agent 若照数据实现只能命中 lucide |
| OUT-04 | `375px\|768px\|1024px\|1440px\|sm:\|md:\|lg:\|xl:\|viewport` | 与 Pre-Delivery Checklist 的断点列表一致 ✅ |
| NEG-02 | `--design-system` 必须出现 | 与 CF-01 重复设防，可接受 |
| CF-01/02/03 | 三种 `cap_to_0` | 语义合理：跳过强制步骤、重大 a11y 失败、emoji 当图标，都值得一票否决 |

### 9.3 潜在盲区

- SCOPE-01/02 与 PROC 系列完全依赖 LLM 判定，但判定问题没有引用"证据字段"之外的强约束（如设计系统输出必须被复用），QA-01 已覆盖"输出被忽略"的检查，链条基本闭合。
- 没有一条脚本判定直接验证"设计系统输出被实际采用"（QA-01 是 LLM 判定），考虑到 QA-01 是失分高频项，可接受。

---

## 10. 逻辑一致性深度审查

### 10.1 数字三方矛盾（I-03，P1）

| 项目 | description | 正文 | 实际数据 |
|------|:----:|:----:|:----:|
| 设计样式 | 50 | 50+ | 58 |
| 调色板 | 21 | 97 | 95 |
| 字体配对 | 50 | 57 | 56 |
| 图表类型 | 20 | 25 | 24 |
| UX 指南 | 未提 | 99 | 98 |
| 技术栈 | 9 | 9 | 11（数据/CLI） |

dossier 记录的"21 vs 97"、"50 vs 57"被确认；本复审进一步确认**描述层、正文层、数据层三方都无法互相印证**。对调用方而言，description 少报能力（21 调色板），正文多报（97），数据居中（95）——任何一个数字被引用都会失真。

### 10.2 域/栈清单三层不一致（I-06，P2）

| 来源 | 域数量 | 栈数量 |
|------|:----:|:----:|
| SKILL.md Search Reference | 10（缺 icons） | 9（缺 nuxtjs、nuxt-ui） |
| search.py docstring / help | 8 | 3 |
| core.py 实际支持 | 11 | 11 |

- `--domain icons` 实际可用且有 100 条数据支撑，但 SKILL.md 完全未提 icons 域；
- `nuxtjs`/`nuxt-ui` 各有 58/50 条高质量数据，但正文栈表未收录，SKILL.md 声称的 "9 stacks" 与数据层 11 栈矛盾。

### 10.3 工作流自洽性

- Step 1（分析需求）→ Step 2（design-system MANDATORY）→ Step 3（域搜索补充）→ Step 4（默认 html-tailwind 栈）逻辑闭环，与 SCORING 的 SCOPE-02/03/04 一一对应。
- 示例工作流（Serenity Spa 皮肤护理）的四个步骤与正文表格、CLI 用法完全一致。
- 优先级表（P1-P8）与 Quick Reference 8 类规则、以及 SKILL.md 声称的域集合（ux/typography/color/style/product/chart）自洽。
- 正文唯一内部矛盾点：`prompt` 域出现在 Search Reference 域表，但 Step 3 的"何时用哪种搜索"表没有 `prompt`，也未说明其 23 条数据的覆盖局限。

### 10.4 输出与交付一致性

- design_system.py 输出的 Pre-Delivery Checklist 与 SKILL.md 末尾的 Pre-Delivery Checklist 条目一一对应（emoji 图标、cursor-pointer、150-300ms、4.5:1、focus、reduced-motion、375/768/1024/1440）——工具与文档闭环，是本技能少有的"文档-实现-评分"三层互锁，值得肯定。

---

## 11. 语法与可读性审查

### 11.1 SKILL.md

- 全文英文，拼写/断句抽查未发现错别字或病句。
- 表格化程度高（11 张表），优先级表、域表、栈表、Do/Don't 表格式统一，对齐良好。
- 命令块、代码块围栏完整无破损。
- 行内强调克制（MANDATORY 仅出现 2 次），无全大写喊话。
- 唯一小瑕疵：Step 2 的命令块与 4.5 节讨论的硬编码路径（I-04）会使示例命令在语料库布局中直接失败。

### 11.2 脚本与数据

- Python 三件套风格统一（docstring、类型标注、命名规范），无死 imports（`json` 在 search.py 中按需 import，OK）。
- CSV 文本整体干净；少数行存在格式性瑕疵：landing.csv STT 27-30 末字段缺闭合引号且内容截断；styles.csv STT 21-37 缺列；styles.csv 的 "Bento Grids"/"Bento Box Grid" 命名重复。
- 无中英混杂、无葡语泄漏（对比 038/262/306 的同类问题，本技能干净）。

---

## 12. 人机感评估

### 12.1 正文语气

- SKILL.md 采用中性、专业、命令式的工具文档语气，无 emoji、无对话填充语、无 persona 表演。✅
- "Common Rules for Professional UI" 的 Don't 示例用 🎨🚀⚙️ 作反例插图为功能性用途（展示"用 emoji 当图标"是错误做法），不是装饰。dossier 对此的判定成立。
- 人机分工清晰：skill 负责检索与规则输出，实现决策交给 agent，未出现越权指令或对用户的亲昵称呼。

### 12.2 数据层

- 数据中大量使用 ✓/⚡/⚠/❌/◐ 作为**功能性状态标记**（Light Mode ✓ Full、Performance ⚡ Excellent 等），阅读效率高，符合数据文件语境。但正是这些字符导致了 I-01 的编码崩溃——"数据设计"与"运行环境"的碰撞是本技能最值得吸取的教训。
- ux-guidelines.csv 的 AI Interaction / Spatial UI / Sustainability 三类（共 11 条）是面向 2025+ 前沿场景的补充，说明数据作者对"AI 生成内容标注""动态类型""能耗"等人机议题有意识，整体人机感良好。

### 12.3 结论

人机感维度 🟢，无任何需修复项。唯一建议是：在 README 或脚本内对非 UTF-8 终端给出 `PYTHONIOENCODING=utf-8` 提示（属于 I-01 的修复一部分）。

---

## 13. 问题清单与修复建议（本报告最长章节）

### 13.1 问题总表（按严重度排序）

| ID | 严重度 | 位置 | 问题 | 证据 | 影响 |
|----|:----:|------|------|------|------|
| **I-01** | **P0** | scripts/search.py L63/76 + design_system.py ASCII/Markdown 输出 | Windows 默认 GBK 控制台下，域搜索与 `--design-system` 均抛 `UnicodeEncodeError`（⚡/⚠ 无法编码） | §8.2 实测复现，两个 traceback | 评分链依赖的 MANDATORY 命令在 Windows 开箱即崩；SKILL.md 明确支持 Windows |
| **I-02** | P1 | SKILL.md 全文 | 缺 Scope/Limitations 节（SKILL-SPEC §3.1 必需项） | §5.2 逐节检索无 scope/limitations/DO-NOT 章节 | 违反规范；agent 无"何时不用本技能"的边界，可能与同类 UX skill 过度竞争 |
| **I-03** | P1 | description / 正文 / 数据 | 六组数字三方矛盾（21 vs 97 vs 95 调色板等） | §10.1 对照表 | 触发匹配与用户预期失真；正文 97/57/99/25 均比实际多 1-2 |
| **I-04** | P1 | SKILL.md 全部命令块 | 硬编码 `.claude/skills/ui-ux-pro-max/scripts/search.py`，语料库布局不可用 | §5.3 | 语料库内直接复制命令失败；dossier 已记录 |
| **I-05** | P1 | data/ui-reasoning.csv ~40 行 Decision_Rules | JSON 重复 `"must_have"` 键，`json.loads` 静默保留末值，前约束（如 wcag-aaa）被丢弃 | §6.2 / §7.3；Python 语义确认 | 设计系统决策输出失真，且无任何报错 |
| **I-06** | P2 | SKILL.md Search Reference / search.py 文档 | 域清单 10 vs 11（icons 缺失）、栈清单 9 vs 11（nuxtjs/nuxt-ui 缺失）、search.py help 仅列 3 栈 | §10.2 | 文档与 CLI 能力脱节，用户不知道 3 个可用域/栈 |
| **I-07** | P2 | data/colors.csv、data/styles.csv | colors 约 60 行同值"默认蓝"且 Notes 与 Hex 不匹配；styles 重复条目（Neubrutalism×2、Bento 家族）与 STT 21-37 缺 3 列 | §6.2 | design-system 输出差异化失效；部分检索字段静默为空 |
| **I-08** | P2 | data/prompts.csv | 仅 23/58 样式有 AI prompt 条目 | §6.2 | `prompt` 域覆盖率 ~40%，SKILL.md 未声明局限 |
| **I-09** | P3 | data/typography.csv STT 20/39/50/52 | Fontshare 字体名与 Google Fonts URL/CSS Import 不一致（仅 Notes 自证） | §6.2 | agent 复制 CSS 得到替代字体，与字体名不符 |
| **I-10** | P3 | data/react-performance.csv STT 4 | 推荐 `better-all` 库（`await all({...})`），无知名 npm 包佐证，疑似幻觉依赖 | §6.2 | agent 生成代码引用不存在库 |
| **I-11** | P3 | data/ui-reasoning.csv | Anti_Patterns 大量"AI purple/pink gradients"与 STT 48（AI-Native UI 推荐 AI Purple）自相矛盾 | §6.2 | 推理规则自相打架 |
| **I-12** | P3 | data/landing.csv STT 27-30 | 末字段缺闭合引号、Conversion Optimization 截断 | §6.2 | 检索内容不完整 |
| **I-13** | P3 | scripts/core.py search_stack | CLI 下友好报错为死代码（argparse choices 先行拦截） | §8.4 实测 | 无效栈名体验降级 |
| **I-14** | P3 | scripts/search.py | `--json` 与 `--design-system` 同传时静默忽略 `--json` | §7.2 | 无文档说明的静默行为 |

### 13.2 分级修复路线图

**第一批（P0，必须先行，影响任何 Windows 运行）：**

1. **修复 I-01 的三种方案（择一或组合）：**
   - 方案 A（最小改动）：在 `search.py` 的 `main()` 顶部与 `format_output` 前统一做 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`（Python 3.7+ 可用）。两行代码解决全部崩溃点。
   - 方案 B（数据层）：将数据 CSV 中的 ✓/⚡/⚠/❌/◐ 替换为 ASCII 标记（OK/Excellent/Warn/N/A），从源头消除非 ASCII 字符——但这会损失数据可读性，不推荐。
   - 方案 C（文档层）：在 Prerequisites 与 Step 2 增加 Windows 提示：`set PYTHONIOENCODING=utf-8` 或 `chcp 65001`。作为 A/B 的补充而非替代。
   - **推荐 A + C 组合**：脚本自愈 + 文档提示，双保险。验证方式：Windows 默认控制台执行 §8.2 两条命令，预期无 traceback。

**第二批（P1，规范与数据可信度）：**

2. **补 Scope/Limitations 节（I-02）**：建议在 "How to Use This Skill" 之后新增 `## Scope & Limitations`，内容至少覆盖：
   - 本技能提供**设计规则与推荐**，不产出完整设计评审方法论（对比 011-ui-design-review 的 10 维度框架）；
   - `prompt` 域数据仅覆盖 23 个样式；`colors.csv` 部分产品类型为默认调色板（在数据修复前先声明）；
   - 不替代 a11y 审计技能与代码审查技能；
   - 何时不应使用：纯代码调试、后端架构、品牌 VI 系统设计等。
3. **统一数字（I-03）**：以数据层为准，description 与正文改为实际值（58 styles / 95 palettes / 56 fonts / 24 charts / 11 stacks），或删除精确数字改用"50+ styles / 90+ palettes / 50+ font pairings / 20+ chart types / 9-11 stacks"。推荐后一种表述，避免未来数据增删再失配。
4. **修复 ui-reasoning.json 重复键（I-05）**：用脚本扫描 `Decision_Rules` 列，将重复 `"must_have"` 合并为数组或改键名（`must_have_1/must_have_2`），并在 `_apply_reasoning` 中增加解析失败/重复键的显式告警（当前 json 解析失败被 `except JSONDecodeError: pass` 静默吞掉——这也应改为输出 warning）。
5. **路径可移植（I-04）**：SKILL.md 命令改为以技能目录为基准的相对路径写法并注明两种布局，或提供一行环境变量说明。评分脚本 SCOPE-03 的正则 `search\.py.*--design-system` 对两种路径均兼容，无需改动 check.py。

**第三批（P2/P3，数据与体验打磨）：**

6. **colors.csv 去默认化（I-07）**：至少为 Notes 明确标注"占位调色板"或按 Notes 主题补配真实 hex；对 Smart Home/ESG/Airline 等 3-5 行高风险"主题不符"条目优先修复。styles.csv 合并重复 Neubrutalism、统一 Bento 命名、为 STT 21-37 补全三列。
7. **文档与 CLI 对齐（I-06）**：SKILL.md 域表补 `icons`（100 条数据是亮点，应展示），栈表补 `nuxtjs`/`nuxt-ui`，修正 search.py 的 docstring 与 help 文本，正文"9 stacks"改为"11 stacks"。
8. **prompts.csv 补齐或声明（I-08）**：为剩余 35 个样式补 prompt 条目，或至少在文档中声明覆盖范围。
9. **数据小修（I-09/10/11/12）**：typography 四行的字体名与 URL 对齐（或明确写"替代字体"）；react-performance STT 4 改写为标准库方案（`Promise.all` + 依赖拆分）或删除；ui-reasoning 的 AI-Native 行 Anti_Patterns 去重逻辑；landing STT 27-30 补全闭合引号。
10. **体验细节（I-13/14）**：search.py 对非法栈名给友好提示（argparse 前先校验），`--json` 与 `--design-system` 互斥说明或支持 JSON 输出。

### 13.3 修复后的验证计划

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 编码自愈 | 默认 GBK 控制台跑 §8.2 两条命令 | 无 traceback，正常输出 |
| 数字一致性 | grep description/body 中的数字，与 `wc -l data/*.csv` 核对 | 三方一致或全部改用范围表述 |
| Scope 节 | 检索 "Scope"/"Limitations" | 命中章节 |
| 重复键清零 | `python -c "import csv,json; [json.loads(r['Decision_Rules']) for r in csv.DictReader(open('data/ui-reasoning.csv',encoding='utf-8'))]"` | 无异常，且无重复键告警 |
| 评分链回归 | 模拟工具日志跑 check.py | SCOPE-03/04、OUT-01/04、NEG-02 五项判定可稳定通过 |
| 全量搜索冒烟 | 对 11 域 × 3 典型 query 各跑一次 search.py | 全部返回 >0 结果 |

### 13.4 问题对 SCORING 判定链的影响映射

| 问题 | 受影响 criterion / critical failure | 机理 | 修复后影响 |
|------|-------------------------------------|------|-----------|
| I-01（编码崩溃） | SCOPE-03、SCOPE-04、NEG-02、CF-01 | `--design-system` 命令在 Windows 崩溃 → 工具日志无 `search.py --design-system` 记录 → 脚本判定必失败；LLM 判定项因拿不到输出也会连锁失分 | 修复后四条目恢复可通过 |
| I-02（缺 Scope 节） | 规范合规（SKILL-SPEC §3.1） | 合规清单硬性检查项不通过；agent 无边界约束，PROC/QA 系列 LLM 判定缺少"不该做什么"的锚点 | 补节后合规项通过 |
| I-03（数字矛盾） | description 触发匹配质量（SCOPE-01 的前置） | 调用方按 description 预期 21 调色板/9 栈，实际 95/11，能力认知偏差 | 统一数字后触发准确 |
| I-04（硬编码路径） | SCOPE-03/04 正则匹配 | 正则 `search\.py.*--design-system` 对两种路径都兼容，**不直接影响评分**；但语料库内人工复现命令会失败 | 文档级修复即可 |
| I-05（JSON 重复键） | PROC-07、QA-01（LLM 判定） | design-system 输出缺 wcag-aaa 等约束 → agent 拿到不完整的 anti-patterns/decision rules → "设计系统被一致应用"证据不足 | 修复后决策规则完整 |
| I-06（域/栈清单） | SCOPE-02/04 | 文档 9 栈 vs 实际 11 栈：agent 若按文档选栈，`nuxtjs`/`nuxt-ui` 数据无法被触达；无碍判定通过，但浪费 108 条数据资产 | 对齐后可加分 |
| I-07（默认蓝/重复样式） | QA-01 | 不同产品类型返回同组蓝色 → 设计系统看起来"未按搜索输出实现"的风险增大（LLM 判定视角） | 去默认化后差异化恢复 |
| I-10（better-all 幻觉库） | OUT-01（脚本） | 若 agent 照数据实现 import 幻觉库，交付代码不可运行；OUT-01 只查 lucide/heroicons 字样，**查不出此问题**（评分盲区，建议数据层修复） | 数据修复后消除 |

结论：I-01 是唯一可能造成 **cap_to_0（CF-01）** 的问题，其余 P1/P2 问题主要侵蚀 LLM 判定项的得分质量。按此优先级修复，评分链可恢复完整。

### 13.5 修复工作量估计与验收标准

| 问题 | 修复方式 | 估计工作量 | 验收标准 |
|------|----------|:----:|----------|
| I-01 | `search.py` 顶部加 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` | 10 分钟 | 默认 GBK 控制台无 traceback |
| I-02 | 新增 `## Scope & Limitations` 节（约 20 行） | 20 分钟 | 检索到章节，覆盖 4 个要点 |
| I-03 | description/正文数字改为数据实际值或范围表述 | 15 分钟 | 三处数字与 `wc -l` 一致 |
| I-04 | 命令块改用相对路径并注明布局 | 15 分钟 | 语料库内直接复制可运行 |
| I-05 | 数据去重键脚本 + `_apply_reasoning` 加告警 | 1 小时 | JSON 无重复键、解析失败有输出 |
| I-06 | 补全域/栈两表 + search.py docstring | 20 分钟 | 三处清单一致为 11 域/11 栈 |
| I-07 | colors 补真实 hex / 标注占位；styles 去重、补列 | 2 小时 | 抽样 10 行 Notes 与 Hex 主题相符 |
| I-08 | 补齐 35 个 prompt 条目或声明范围 | 1-2 小时 | prompt 域可检索全部样式或文档声明 |
| I-09 ~ I-12 | 逐文件小修 | 每项 15-30 分钟 | 数据行无截断、无矛盾 |
| I-13 / I-14 | search.py 参数校验与提示 | 20 分钟 | 非法参数有友好输出 |

合计约 **0.5 人日**即可完成全部修复——性价比极高，修复后评级可提升两级（🟡 → 🟢）。

### 13.6 总结论

086-ui-ux-pro-max 是 SkillIF 语料库中**架构最完整、数据资产最重**的工具型技能之一：1335 条规则数据、BM25 检索、5 域设计系统聚合、文档-工具-评分三层互锁（Pre-Delivery Checklist 同时存在于 SKILL.md、design_system.py 输出与 OUT-04 判定中）——这些设计在 322 个技能里属于上游水准。

但当前状态**不能直接进入评测**，P0 的 Windows 编码崩溃会使评分链（SCOPE-03/CF-01 依赖的 `--design-system` 命令）在 Windows Runner 上必然失败，这与 SKILL.md 自身宣称的 Windows 支持直接冲突。按 §13.2 第一批修复（约 2 行代码）即可解除致命风险；第二批修复（Scope 节 + 数字统一 + JSON 重复键）后可达 🟢 水平。

评级：**🟡（修复 I-01 后即可测；修复 I-01/02/03/05 后达 🟢）**，与 dossier 判定一致并补充了 4 项新发现。
