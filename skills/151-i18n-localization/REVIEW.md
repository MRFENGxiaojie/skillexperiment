# REVIEW — 151-i18n-localization

- 审查日期: 2026-08-06
- 审查对象: `D:\SkillIF\skill-experiment\complex-skills\151-i18n-localization\`
- 审查方式: 全文读取全部 4 个文件（SKILL.md、SCORING.yaml、check.py、scripts/i18n_checker.py），逐项对照 `_shared/SKILL-SPEC.md` v1.0 规范与 `_shared/CHECKER-LIBRARY.md` 检查器库
- 只写 REVIEW.md；未修改 SKILL.md / SCORING.yaml / check.py / scripts 任何内容
- 审查顺序依据: 154 → 152 → 151 → 150（本文件为第三个）

---

## 1. 目录清单

```
151-i18n-localization/
├── SKILL.md                        (153 行)
├── SCORING.yaml                    (160 行, 17 项判据 + 3 项致命失败)
├── check.py                        (82 行, 5 项脚本检查)
└── scripts/
    └── i18n_checker.py             (242 行, 硬编码字符串/缺失翻译检测器)
```

- 文件总数: 4（无 references/ 目录——本技能为自包含参考卡 + 单脚本形态，与 154/152 的"正文+多参考"形态不同）
- 全部文件已全文读取（合计 637 行），脚本做了逐行代码走读。
- 目录结构极简，无死空间; 唯一脚本已被正文引用。

---

## 2. Frontmatter（name / description / 工具 / 字段 / YAML）

### 2.1 name

- `name: i18n-localization`
- 小写 + 连字符，长度 16 字符 ≤ 64，与目录名 `151-i18n-localization` 后缀一致。
- ✅ 通过。

### 2.2 description

原文:

```yaml
description: Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. Use when the user asks to internationalize or localize an app, detect hardcoded strings, manage translation and locale files, or add RTL language support.
```

| 检查项 | 结果 |
|--------|------|
| WHAT | ✅ "Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support."——名词短语开头（规范 Good 示例同型），四类能力点明确 |
| WHEN | ✅ "Use when the user asks to internationalize or localize an app, detect hardcoded strings, manage translation and locale files, or add RTL language support" |
| KEYWORDS | ✅ i18n、localization、hardcoded strings、translations、locale files、RTL |
| 人称 | ✅ 第三人称，无 first/second-person |
| 触发信号 | ✅ 使用规范 §2.4 原文信号短语 "Use when the user asks to"——4 个被审技能中唯一逐字命中的 |
| 长度 | 约 355 字符 ≤ 1024 ✅ |
| 跨技能路由 | ✅ 无 |

- description 为 4 技能中最符合规范字面要求的写法。

### 2.3 工具（allowed-tools）

- 声明了 `allowed-tools: Read, Glob, Grep`——这是本次 4 个技能中唯一声明该字段的。
- **存在矛盾**: 正文 `## Script` 节要求运行 `python scripts/i18n_checker.py <project_path>`（执行 Python 需要 Bash 工具），但 allowed-tools 未包含 Bash。若评测环境严格按 allowed-tools 授权，agent 将无法运行检查器 → PROC-05 判据（tool_log 含 `i18n_checker\.py`）稳定失败，ERR-01/QA-01 的判定依据也缺失。详见 🟡-3。
- 字段本身在规范允许列表中（SKILL-SPEC §1.2），合规 ✅；只是清单内容与技能需求不匹配。

### 2.4 字段与 YAML

- 三个键（name、description、allowed-tools）均在允许列表，无禁止字段。
- YAML 单行双引号描述，无解析问题。
- ✅ 通过。

---

## 3. Body（段落 / 必需章节 / 委托 / 层级 / vs600）

### 3.1 段落概况

SKILL.md 正文 153 行，形态为"参考卡"（reference card）:

- H1 标题 + blockquote 摘要（"Internationalization (i18n) and Localization (L10n) best practices."）
- 8 个**编号** H2 小节: 1. Core Concepts / 2. When to Use i18n / 3. Implementation Patterns（React / Next.js / Python 三例代码）/ 4. File Structure / 5. Best Practices（DO/DON'T 双列）/ 6. Common Problems（表格）/ 7. RTL Support（CSS）/ 8. Checklist
- 未编号的 `## Script` 节: 脚本表格（Purpose + Command）

- 结构高度规整、表格密度高（4 张表）、代码示例直给（tsx/python/css 三例）。这是本技能的最强项，dossier 的"结构清晰"评价完全成立。

### 3.2 必需章节（对照 SKILL-SPEC §3.1 三项）

| 必需章节 | 判定 | 定位 |
|----------|------|------|
| Workflow / Process | ⚠️ 部分满足 | 无 `## Workflow` / `## Process` 节。最接近的执行性内容: §8 Checklist（部署前 6 项验证）与 §2 When to Use（决策表）。SCORING 的流程判据（SCOPE-02 判需求 → PROC-01..05 执行 → QA-01 清单核验 → ERR-01 修缺陷）在正文中**没有对应的步骤化描述**，agent 需自行拼装执行顺序。详见 🟡-1 |
| Output Format | ❌ 缺失 | 无 `## Output`。没有说明"完成任务后用户拿到什么"（locales/ 树 + 改写后的组件 + 检查器报告格式）。§8 Checklist 是验证清单而非交付物描述。详见 🟡-2 |
| Scope / Limitations | ⚠️ 部分满足 | 无 `## Scope` / `## Limitations`。§2 When to Use i18n 的项目类型决策表（public web app=必做 / personal=可选）提供了"何时该做"的部分边界语义，但无"本技能不做什么"（例如: 不做机器翻译、不自动迁移存量代码、不覆盖 Nuxt/Vue-i18n 之外生态）的声明 |

- 综合: 该技能是"参考卡"而非"流程技能"，三项必需章节中 Workflow 与 Scope 以替代形态部分覆盖、Output 完全空缺。SCORING.yaml 却声明 `pattern: tool`——正文形态（参考卡）与声明形态（工具/决策树型）不一致，是模式错位（🟡/🟢，见第 10 节）。

### 3.3 委托（Delegation）

- 本技能无 references/ 目录，委托结构极简: SKILL.md 内联全部知识（153 行），仅将"检测执行"委托给 `scripts/i18n_checker.py`（`## Script` 节一行表格）。
- 对 153 行的自包含参考卡而言，这种"知识内联 + 单点委托"是可接受的形态——不需要为小技能硬造 references。
- 但注意: 与 154/152 的"正文 200+ 行 + references 数百行"相比，本技能把约 8 小节知识全部放在 SKILL.md，正文即全部。若后续扩充（新增框架示例、语言包规范），应拆出 references 保持 SKILL.md ≤600 行（当前无超限风险，153 行）。

### 3.4 层级

- 编号小节（1–8）+ 未编号 Script 节——层级本身清晰，但编号不完整（Script 是第 9 节却无编号），一致性小瑕疵（🟢）。
- 代码示例与表格交替，无跳级。
- ✅ 总体层级良好（本技能最强项）。

### 3.5 vs600

- SKILL.md 153 行，占 600 硬上限的 25.5%，远低于上限，无超限风险。
- 规模画像: `pattern: tool` 目标 ~300 行，实际 153 行——约为 Tool 型目标的一半，接近"知识卡"的合理规模（约 150–250 行区间下沿）。行数不是问题，缺的是流程化内容（见 🟡-1/2）。

---

## 4. 逻辑（衔接 / 矛盾 / 代码 / 条件）

### 4.1 衔接（正文 ↔ 脚本 ↔ SCORING）

逐项核验三方的"概念↔正则"对齐:

| SCORING 判据 | SKILL.md 落点 | 脚本/check.py 落点 | 一致性 |
|--------------|---------------|--------------------|--------|
| SCOPE-03（react-i18next\|next-intl\|gettext） | §3 三个框架示例 | I18N_PATTERNS 含 t()/useTranslation/$t/_\|gettext/useTranslations | ✅ |
| PROC-02（locales/*/common.json） | §4 File Structure（en/common.json 等） | find_locale_files 扫描 `**/locales/**/*.json` | ✅ |
| PROC-03（Intl\.(DateTimeFormat\|NumberFormat)） | §6 Common Problems 表 | 无（脚本不查 Intl，靠 tool_log） | ✅ |
| PROC-04（inline-start\|inline-end\|...） | §7 RTL CSS 示例 | 无（靠 tool_log） | ✅ |
| PROC-05（i18n_checker\.py） | ## Script 节命令 | 脚本 main() 读取 sys.argv[1] | ✅ |
| TEC-01（语言键集对齐） | §8 Checklist 第 2 条 | check_locale_completeness 跨语言键比对 | ✅ |
| NEG-01（无硬编码残留） | §5 DON'T 第 1 条 + §8 | check_hardcoded_strings | ✅ |

- 六组概念全部闭环，无"判据引用正文不存在概念"的情况。整体衔接良好。

### 4.2 矛盾与不一致

| # | 位置 | 不一致描述 | 级别 |
|---|------|-----------|------|
| C1 | frontmatter L4 vs 正文 L152 vs SCORING PROC-05 | allowed-tools（Read, Glob, Grep）不含 Bash，但正文要求运行 `python scripts/i18n_checker.py`，PROC-05 要求 tool_log 出现该命令——**工具清单与执行要求矛盾**（详见 🟡-3） | 🟡 |
| C2 | SCORING `pattern: tool` vs 正文形态 | 正文是参考卡（概念/模式/清单），无决策树/工具型结构；pattern 声明与内容形态不符 | 🟡/🟢 |
| C3 | SKILL.md §3 覆盖框架 vs 脚本扫描框架 | 正文只给 React/Next.js/Python 三例；脚本还扫描 .tsx/.jsx/.ts/.js/.vue/.py 并内置 Vue 的 `$t(`、react-intl 的 FormattedMessage、i18n. 等模式——脚本覆盖面大于正文（超集方向，非矛盾，但正文未提 Vue/react-intl 可被认为遗漏） | 🟢 |

### 4.3 代码（scripts/i18n_checker.py + check.py 走读）

**i18n_checker.py**（242 行）:

- 优点:
  1. Windows 控制台编码修复（`sys.stdout.reconfigure(encoding='utf-8')`，含 Python<3.7 兜底）——本语料库脚本中的稀有细节，好评;
  2. 正则模式分类清晰（jsx/vue/python 三组硬编码模式 + 8 条 i18n 使用模式）;
  3. 输出分级（[OK]/[X]/[!]）+ 退出码 0/1 与 [X] 计数挂钩;
  4. 排除 node_modules/.git/dist/build/venv/test/spec;
  5. 扁平化嵌套键（flatten_keys）处理多级 locale JSON;
  6. 每文件读取带 errors='ignore'，健壮。
- 缺陷:
  1. **`if matches and not has_i18n`**（L174）: 只有"整文件无任何 i18n 用法"时才报告硬编码——混合文件（用了 t() 但残留若干硬编码串）被静默放过，与 NEG-01（无硬编码残留）目标相悖。这是脚本最大的检测漏洞（🟡-4）;
  2. `code_files[:50]`（L157）: 超过 50 个代码文件的工程只查前 50 个且无提示，大项目漏检（🟡-4）;
  3. `base_lang = all_langs[0]`（L99）: 基准语言依赖 glob 遍历顺序而非显式配置，检测结果顺序敏感（🟢）;
  4. 裸 `except: continue` 两处（L88、L182），吞掉 JSON 解析错误，调试困难（🟢）;
  5. I18N_PATTERNS 中 `i18n\.` 过宽，可能把含 "i18n." 注释/字符串的文件误判为已 i18n，进一步放大缺陷 1 的漏报（🟢）;
  6. 硬编码正则要求大写字母开头（`[A-Z]`），全小写文本/标签值漏检（🟢）。

**check.py**（82 行）:

- 5 项脚本检查（SCOPE-03、PROC-02、PROC-03、PROC-04、PROC-05）与 SCORING 中 5 个 `judge: script` 判据一一对应，正则逐字符一致 ✅。
- 注释 "Run all 5 script checks" 与实际数量一致 ✅（对比 152 的注释误差，此处无此问题）。
- 与 154/152 相同的 agent_output 双路判断模式，无新问题。
- ✅ 代码层面无功能性缺陷。

### 4.4 条件（流程分支）

- 正文侧分支仅 §2 项目类型决策表（必做/可能/考虑/可选）——是条件表达，但无"选型后怎么办"的流程衔接（选了 SaaS → 下一步做什么? 正文没有指引，需 agent 自行跳到 §3 模式）。
- 脚本侧分支: 无 locale 文件 / 单一语言 / 多语言键对齐 / 混合键——均有明确输出路径 ✅。
- ERR-01（检查器报告缺陷 → 修复而非忽略）在正文无对应"如何读报告/如何修"指引——判据有、正文支撑弱（与 152 同型问题）。

---

## 5. 参考文件（引用矩阵 / 不可见资源 / 全文审查 / 跨 Skill / 死文件）

### 5.1 引用矩阵

| 源文件 | 引用目标 | 形式 | 存在性 | 用途 |
|--------|----------|------|--------|------|
| SKILL.md L150–152 | `scripts/i18n_checker.py` | 表格（Purpose + Command） | ✅ 存在 (242 行) | 硬编码/缺失翻译检测 |
| SCORING PROC-05 | `i18n_checker\.py`（tool_log 正则） | 判据文本 | ✅ | 强制运行检查器 |
| check.py L45 | `scripts/i18n_checker.py`（通过 PROC-05 正则） | 代码 | ✅ | 同上 |
| SCORING PROC-02 | `locales/*/common.json` | 判据文本 | ✅（产物） | 验证 locale 结构 |

- 引用全部指向技能内相对路径或评测产物，无悬空引用。
- 无 references/ 目录——不构成违规（规范不要求必须有 references），只是形态选择。

### 5.2 不可见资源

- 无。唯一被引用的脚本真实存在，正文承诺的命令（`python scripts/i18n_checker.py <project_path>`）与脚本 argv 约定（`sys.argv[1]`，缺省 "."）一致。
- 反向检查: 脚本输出格式（[OK]/[X]/[!] 前缀）在 SKILL.md 未描述——agent 读到脚本输出时无对照说明，属轻微的信息不对称（🟢，可并入 🟡-2 的 Output 节修复）。

### 5.3 全文审查结论

- **i18n_checker.py（242 行）**: 功能完整的启发式检测器。locale 完整性比对（跨语言键集差集）逻辑正确；硬编码检测有设计漏洞（见 §4.3 缺陷 1/2）。作为评测辅助工具够用，作为生产工具会漏报——按"评测场景够用"标准判定为合格。
- SKILL.md 与 SCORING/check.py 已全文逐项核验，无遗漏内容。

### 5.4 跨 Skill 引用

- 无 `../other-skill/` 引用；正文未提及任何其他技能名。
- ✅ 通过。

### 5.5 死文件

- 无。4 个文件全部承担明确职责（SKILL.md 主体 / SCORING 评测 / check.py 评测 / script 工具）。
- ✅ 本技能是 4 个被审技能中唯一"零死文件、零冗余文档"的（152 有 README 死文件问题）。

---

## 6. 语法格式（拼写 / 语法 / 混杂 / Markdown / 占位符 / 截断）

### 6.1 拼写

- 全文未发现拼写错误。术语（i18n、L10n、react-i18next、next-intl、gettext、Intl.DateTimeFormat、ICU）拼写统一正确。
- blockquote 摘要与正文重复定义 i18n/L10n，无冲突。

### 6.2 语法

- 正文以名词短语/短句为主（参考卡风格），无碎片句; DO/DON'T 列表动宾结构统一。
- 脚本 docstring 与注释为完整句。

### 6.3 中英混杂

- 全英文，无混杂。

### 6.4 Markdown

- 4 张表格全部渲染正确（Core Concepts 3 列 / When to Use 2 列 / Common Problems 2 列 / Script 3 列），表头与分隔行齐全。
- 代码块: tsx 2 处、python 1 处、css 1 处、纯文本目录树 1 处，全部闭合 ✅。
- 缩进列表（locales/ 目录树）用 2 空格，渲染稳定。
- ✅ Markdown 质量良好。

### 6.5 占位符

- 仅 1 处占位符: `<project_path>`（脚本命令参数），语义明确。
- 代码示例中的 'welcome.title'、'Home' 等为键名示例，非占位符，无混淆风险。

### 6.6 截断

- 所有文件结尾完整（SKILL.md 以 Script 表收束; 脚本以 `__main__` 收束），无截断。

---

## 7. 规范合规 12-item（对照 `_shared/SKILL-SPEC.md` §5）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | name: 小写+连字符, ≤64, 匹配目录 | ✅ | `i18n-localization` |
| 2 | description: 第三人称, WHAT+WHEN+KEYWORDS, ≤1024 | ✅ | 约 355 字符 |
| 3 | description: 无 imperative/first/second-person 开头 | ✅ | 名词短语开头 |
| 4 | description: 无跨技能路由内嵌 | ✅ | 无 |
| 5 | description: 至少一个触发信号短语 | ✅ | "Use when the user asks to"（规范原文句式） |
| 6 | frontmatter: 无允许列表之外的键 | ✅ | name + description + allowed-tools（允许字段） |
| 7 | body: ≤600 行 | ✅ | 153 行 |
| 8 | body: 有 workflow/process 节 | ⚠️ | 无显式 Workflow 节; §8 Checklist 提供验证步骤、§2 提供需求判定，但无执行流程编排 |
| 9 | body: 有 output format 节 | ❌ | 无 Output 节 |
| 10 | body: 有 scope/limitations 节 | ⚠️ | §2 项目类型决策表覆盖"何时该做"，无"不做什么"的 limitations |
| 11 | body: 无跨技能文件引用 | ✅ | 无 |
| 12 | 目录: NNN-kebab-case, 无空格大写 | ✅ | `151-i18n-localization` |

- 结果: 8 项通过、2 项部分、2 项未过（第 9 项为硬缺失，第 8/10 项为替代形态）。
- 与 152 对比: 152 是 Workflow ✅ / Output ❌ / Scope ❌; 151 是 Workflow ⚠️ / Output ❌ / Scope ⚠️——151 在第 8/10 项有部分形态支撑（Checklist、决策表），第 5 项 description 触发信号则完胜。
- 注: 三项必需章节的"语义与标题"之间的差距是 151 与 154 之间最主要的分野（154 至少以加粗段覆盖 Scope，151 完全无集中边界声明）。

---

## 8. 人机感（Emoji / 喊叫 / Persona / 边界 / 人称 / 表格）

### 8.1 Emoji

- SKILL.md 使用 ✅/⚠️/❌: §2 项目类型表（✅ Yes / ⚠️ Maybe / ❌ Optional）、§5 DO ✅ / DON'T ❌ 双列。均为**语义化标记**（判定符号），非装饰表情，用途正确。
- 其余小节零 Emoji。
- ✅ 克制且语义化。

### 8.2 喊叫

- "DON'T ❌" 为 DO/DON'T 对照列表的既定表达（可视为列表标签而非喊叫句）; 其余无大写喊叫。
- ✅ 通过（"DON'T" 在 DO/DON'T 对照语境中属惯例，不计违规）。

### 8.3 Persona

- 正文为陈述式/清单式，无人格化。blockquote 摘要为客观陈述。
- ✅ 通过。

### 8.4 边界

- 边界意识偏弱: 无 Limitations 节（§7 RTL 与 §2 决策表只覆盖部分语义）; 未声明"不做什么"（不做机器翻译/不做存量代码自动迁移/不覆盖 Vue 生态——尽管脚本实际支持 Vue）。
- SCORING 侧边界判据 4 条（NEG-01..04）均针对"禁止事项"，正文侧无对应集中声明。边界信息呈"评分层有、正文层无"格局（与 152 同型）。见 🟡-2 修复建议。

### 8.5 人称

- description 第三人称 ✅; 正文陈述体/清单体，无用户对话式第二人称。
- ✅ 一致。

### 8.6 表格

- 4 张表承载了核心决策信息（概念对照、需求判定、问题对策、脚本入口），是"参考型"形态的正向实践——决策用表格、知识用表格，符合"决策树/表格优先于散文"导向。
- ✅ 良好。

---

## 9. 可执行性

1. **入口**: description 触发明确; §2 给出项目类型需求判定表（SCOPE-02 的支撑）✅。
2. **执行路径**: ❌ 弱项——正文没有步骤化流程。agent 的合理执行链（判需求 → 选框架模式 → 改写组件为 t() → 建 locales/ 结构 → Intl/复数 → RTL → 跑检查器 → 按报告修复 → 过 Checklist）只能从 §3→§8 的内容顺序与 SCORING 语义中自行推断。SCORING 对 agent 不可见（评测文件），正文未提供该链条的显式编排。
3. **代码示例**: §3 三框架各给一段可直接抄的代码，§7 给 CSS 逻辑属性片段——"照抄可用"粒度好 ✅。
4. **工具支撑**: i18n_checker.py 可运行、输出分级带退出码、检测维度与判据对齐 ✅; 但检测漏洞（混合文件漏报、50 文件上限）削弱了"用检查器证明无硬编码"的证据强度。
5. **验收**: §8 Checklist 6 项可直接当验收单 ✅（但属于"验证"而非"交付物描述"）。
6. **失败路径**: ERR-01 要求按检查器报告修复——正文无"报告格式说明/常见缺陷清单"支撑（脚本输出 [OK]/[X]/[!] 的语义未在任何正文位置说明）。

- 结论: 可执行性中下偏上。代码片段与检查器可用性都不错，但**执行顺序编排与交付物定义**缺失，agent 依赖自身推断; 这直接对应 12-item 第 8/9 项的失分。

---

## 10. SCORING

### 10.1 结构统计

- total_items: 17
- 分布: scope 3 / process 5 / technical 2 / negative 4 / qa 2 / error_handling 1（3+5+2+4+2+1 = 17 ✅）
- judge 分布: script 5 / llm 12——llm 占比 71%，是本次 4 个技能中**脚本硬核验最薄**的（154: 6/20、152: 9/19）
- critical_failures: 3（CF-01 宣称 i18n 但残留硬编码、CF-02 locale 缺键无 fallback、CF-03 拼接翻译串 + RTL 场景用物理 CSS），全部 cap_to_0

### 10.2 判据与技能内容一致性

| 判据 | 落点 | 一致性 |
|------|------|--------|
| SCOPE-01 | description | ✅ |
| SCOPE-02 | §2 项目类型表 | ✅ 表内四档（Yes/Maybe/Consider/Optional）与判据逐字对应 |
| SCOPE-03 | §3 三框架 | ✅ |
| PROC-01 | §5 DO 第 1 条 + §3 代码 | ✅ |
| PROC-02 | §4 File Structure | ✅ |
| PROC-03 | §6 表格 | ✅ |
| PROC-04 | §7 CSS | ✅ |
| PROC-05 | ## Script 节 | ✅ |
| TEC-01/02 | §8 Checklist 第 2 条 | ✅ |
| NEG-01/02/03/04 | §5 DON'T 四条 | ✅ 与 DON'T 列表一一对应 |
| QA-01 | §8 Checklist | ✅ 判据列举的 5 项与 Checklist 6 项基本重合 |
| QA-02 | §6 Common Problems 表 | ✅ 判据的 4 组映射与表格 5 行一致 |
| ERR-01 | 脚本报告 | ✅ 判据合理 |

- 判据与正文映射全部成立，无悬空项。
- 观察 1: 脚本可核验的判据仅 5 项，且其中 4 项是 tool_log 正则（"agent 有没有做过")，只有 PROC-02 检查产物存在性——**对产物正确性的硬核验只有 locale 文件存在这一项**。NEG-01（无硬编码残留）等关键质量判据全部依赖 llm，脚本本可支撑却未被判据利用（i18n_checker 的输出可被 file_contains/JSON 解析接入）——建议未来扩展（🟢）。
- 观察 2: `pattern: tool` 与参考卡正文错位（C2）——tool 型判据（SCOPE-03 的框架库正则等）设计得不错，但正文无 tool 型决策树支撑其"选择逻辑"。

### 10.3 潜在评测陷阱

- PROC-05 要求 tool_log 出现 `i18n_checker\.py`——若任务不涉及修改代码（纯咨询型提问），agent 合理不运行脚本，判据扣分; 取决于任务设计，非技能缺陷（记 🟢 提示）。

---

## 11. 已知问题（dossier 对照）

dossier 记录（2026-08-05）:

> **151: 🟢 结构清晰参考型**

本次审查结论:

- "结构清晰": 完全认同——编号小节 + 4 表 + 3 框架代码示例 + Checklist，是本技能最突出的优点。
- "参考型": 认同且有必要深挖——"参考型"正是其缺点的来源: 参考卡形态天然缺少 Workflow/Output/Scope 三节（12-item 第 8/9/10 项失分点），SCORING 却声明 `pattern: tool`，形态与声明不一致。
- 补充发现（dossier 未记录）: (a) allowed-tools 缺 Bash 与 PROC-05 运行要求矛盾（🟡）; (b) i18n_checker.py 两个检测漏洞（混合文件漏报、50 文件上限）; (c) Output 节缺失。
- 综合评级: 维持 🟢（内容质量与结构确实好），但建议按 🟡 项修复后向 154 看齐。

---

## 12. 综合评分（8 维加权）

评分口径: 每维 0–10，加权汇总（满分 100）。

| 维度 | 权重 | 得分 | 评述 |
|------|------|------|------|
| 内容完整性 | 20% | 8.0 | 概念/模式/结构/实践/问题/RTL/清单七类知识齐备; 缺流程编排与输出定义 |
| 结构层次 | 15% | 9.0 | 编号小节+表格密度为 4 技能之最; 唯一小瑕疵是 Script 节未编号 |
| 规范合规（12-item） | 15% | 7.5 | 8 过 2 部分 2 未过; description 触发信号为 4 技能唯一逐字合规 |
| 逻辑一致性 | 10% | 8.5 | 正文↔脚本↔判据六组概念闭环; C1 allowed-tools 矛盾、C2 pattern 错位 |
| 参考文件质量 | 10% | 8.5 | 无 references（自包含合理）; 脚本功能完整但有两处检测漏洞; 零死文件 |
| 人机感与语言 | 10% | 9.0 | Emoji 全部语义化、无喊叫无 Persona |
| 可执行性 | 10% | 7.5 | 代码片段可用、脚本可跑; 缺执行顺序编排与交付物定义，依赖 agent 推断 |
| SCORING 质量 | 10% | 8.0 | 17 项映射全部成立; script 覆盖最薄（5/17），产物核验仅 1 项 |

**加权总分: 82.25 ≈ 82 / 100（A- 级 / 🟢 结构清晰参考型）**

排名语境: 4 技能中列第 3（154=92.5 > 152=83.5 > 151≈82）。与 152 分差很小（1.5 分），主要差异: 152 脚本硬核验更强、正文有 Workflow 节; 151 结构与人机感更优、description 更合规。

---

## 13. 修复建议（WRITE EXTENSIVELY）

### 🔴 致命问题

- **无。** 本技能无致命缺陷。检测漏洞（🟡-4）不直接导致评测崩溃（llm 判据可兜底），但会削弱证据链。

### 🟡 重要问题

#### 🟡-1 缺少 Workflow/Process 流程编排（定位: SKILL.md 整体结构）

- 定位: 全文无步骤化执行流程; §8 Checklist 是验证清单，§2 是需求判定，两者之间没有"执行链"。
- 修复: 在 §2 之后新增 `## Workflow`（4–5 步）:
  1. 判定需求（§2 决策表）→ 2. 选择框架模式并改写组件为翻译键（§3+§5 DO 第 1 条）→ 3. 创建 locales/<lang>/ 与 feature 文件（§4）→ 4. 处理日期/数字/复数与 RTL（§6+§7）→ 5. 运行 `scripts/i18n_checker.py` 并按报告修复（Script 节）→ 6. 对照 §8 Checklist 验收。
  - 每一步附一行"对应小节"指针，把现有内容串成链。
- 后果（若不修）: 12-item 第 8 项持续失分; agent 执行顺序随机（先建 locales 再改代码 / 先跑检查器再写代码等组合都会出现），交付质量方差大; "参考型"标签固化为"不可执行型"的风险。
- 工作量: 约 20 行,零风险。

#### 🟡-2 缺少 Output Format 与 Scope/Limitations 两节（定位: SKILL.md 第 8 节之后）

- 定位: 无 Output 节、无 Limitations 声明; 脚本输出格式（[OK]/[X]/[!]）也无任何说明。
- 修复:
  - 新增 `## Output`（或并入 Workflow 末步）: 交付物 = 改写后的组件（翻译键）+ locales/<lang>/ 树 + 检查器报告（[OK]/[X]/[!] 前缀语义说明）; 附一个小交付物树示例;
  - 新增 `## Scope & Limitations`: "本技能不执行机器翻译"、"不自动迁移存量代码"、"覆盖 React/Next.js/Python 生态（Vue 检测由脚本支持，示例未展开）"、"检测器为启发式，50 文件上限，大工程需分批"。
- 后果（若不修）: 12-item 第 9 项失分持续; agent 无交付物对照，脚本报告读不懂; 边界缺失导致 agent 对"迁移存量代码"类请求越界硬做。
- 工作量: 约 25 行。

#### 🟡-3 allowed-tools 与运行脚本要求矛盾（定位: frontmatter L4 vs ## Script 节）

- 定位: `allowed-tools: Read, Glob, Grep` 不含 Bash，但正文与 PROC-05 都要求执行 `python scripts/i18n_checker.py`。
- 修复: 三选一——
  (a) allowed-tools 追加 `Bash`（最直接）;
  (b) 若评测环境禁止 Bash，把检查器改为"只读分析 + 输出建议"由 agent 用 Read/Glob/Grep 复现，正文改写相应命令说明;
  (c) 至少将 `python` 执行命令标注为"需要 Bash 权限"。
- 后果（若不修）: 严格授权的评测环境（按 allowed-tools 白名单执行工具）下，PROC-05 稳定失败、ERR-01/QA-01 证据缺失，实际得分被结构性压低——这是本技能最可能在评测中"莫名丢分"的一处。
- 工作量: 1 行。

#### 🟡-4 i18n_checker.py 检测漏洞（定位: scripts/i18n_checker.py L157、L174）

- 定位:
  1. L174 `if matches and not has_i18n`——混合文件（有 t() 但残留硬编码）不报告;
  2. L157 `code_files[:50]`——大工程只查前 50 个文件，静默漏检。
- 修复:
  1. 将条件改为: 始终报告硬编码命中，但按"文件已有 i18n 用法"降权（如标 `[!]` 而非 `[X]`），避免误伤; 或在报告头注明"混合文件单独列示";
  2. `[:50]` 改为配置参数（`--max-files`，默认 200），并在报告打印"仅扫描前 N 个文件"。
- 后果（若不修）: NEG-01（无硬编码残留）的脚本证据不可信; 若评测把检查器输出当证据，混合文件漏报会让"宣称已 i18n 但残留串"的行为通过——正好放走 CF-01 想抓的违规。
- 工作量: 各 2–3 行。

### 🟢 优化建议

| # | 建议 | 定位 | 工作量 | 收益 |
|---|------|------|--------|------|
| 🟢-1 | Script 节编号为 "9. Script"，保持编号体系完整 | SKILL.md L148 | 1 字符 | 结构一致性 |
| 🟢-2 | description 追加关键词: translation keys、ICU、pluralization | SKILL.md L3 | 1 行 | 意图匹配 |
| 🟢-3 | SCORING 增加 1 条 script 判据读取 i18n_checker 输出（如 file_contains 检查报告文件）以强化产物核验 | SCORING.yaml | 2 行 | script 覆盖 5→6 |
| 🟢-4 | 脚本裸 `except: continue` 改为捕获指定异常（json.JSONDecodeError 等） | i18n_checker.py L88/L182 | 2 行 | 可调试性 |
| 🟢-5 | base_lang 改为显式基准（或按 alphabet 排序取首） | i18n_checker.py L99 | 2 行 | 结果确定性 |
| 🟢-6 | pattern 由 `tool` 改为 `philosophy`/`reference`，或按 🟡-1 补 Workflow 后维持 tool | SCORING.yaml L2 | 1 行 | 形态与声明一致 |

---

## 附录

### A. 审查方法说明

- 依据 `_shared/SKILL-SPEC.md` 与 `_shared/CHECKER-LIBRARY.md` 静态审查; 全部 4 个文件逐行通读（637 行）; i18n_checker.py 按代码走读方式审查（未实际执行——不修改被评文件）。
- 正则与判据的对照通过逐字符比对完成。

### B. 文件规模汇总

| 文件 | 行数 | 类型 |
|------|------|------|
| SKILL.md | 153 | 技能主体（自包含参考卡） |
| SCORING.yaml | 160 | 评测 |
| check.py | 82 | 评测 |
| scripts/i18n_checker.py | 242 | 工具 |
| 合计 | 637 | — |

### C. 结论

- 总体评级: 🟢（结构清晰参考型，加权 82/100）
- 关键优势: 结构规整（编号+表格+示例）、description 触发信号 4 技能唯一逐字合规、零死文件、正文↔脚本↔判据六组概念闭环
- 关键改进: 🟡 4 项（Workflow 编排、Output/Scope 两节、allowed-tools 矛盾、脚本检测漏洞）+ 🟢 6 项; 优先处理 🟡-1/2/3，修复后预期 86–88 分
