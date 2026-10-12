# REVIEW — 099-tpl-situacao-acessibilidade-a11y

## §1 审查概要

| 项目 | 内容 |
|------|------|
| Skill | `099-tpl-situacao-acessibilidade-a11y` |
| 目录 | `D:\SkillIF\skill-experiment\complex-skills\099-tpl-situacao-acessibilidade-a11y\` |
| 审查日期 | 2026-08-06 |
| 依据 | `SKILL-SPEC.md` v1.0、`skill-dossier.md`、本目录 `SCORING.yaml` / `check.py` |
| 文件体量 | `SKILL.md` 202 行 / 9,563 字节（含 frontmatter 7 行） |
| Pattern | process（SCORING.yaml 声明），实际形态为"模板 + 清单 + 决策表"混合体 |
| 评分项 | SCORING.yaml 共 17 项（scope 3 / process 4 / technical 4 / output 3 / negative 2 / qa 1）+ 3 条 critical failures |
| 总评 | 🟡 可用但有小问题 —— 内容质量在 tpl-situacao 家族中属上乘，主要缺口为缺 Scope 节与显式 Workflow 节 |

### 审查结论（一句话）

本技能是 tpl-situacao 模板家族中内容最厚实的成员之一：7 条原则、11 行路由表、24 项 POUR 清单、CSS/TSX 示例、输出模板与 10 条质量门俱全，领域事实经核实全部正确；但缺少 SKILL-SPEC §3.1 要求的两类必备节（Scope / 显式 Workflow），description 携带与内容无关的家族模板套话（"debugging, security and refactoring"），且 React Modal 示例声明了 `aria-modal` 却未实现它所声称的焦点陷阱——修复上述问题后可达 🟢。

### 与档案的衔接

`skill-dossier.md` 中 099 未被单独审查：批注 076-100 只给出汇总统计（🔴0 / 🟠4 / 🟢8），条目 "093-data-privacy-compliance — 100 系列" 的内容（GDPR 罚款、数据主体权利、DPIA）实际只对应 093，与 099 完全无关。本 REVIEW.md 补上这一缺口。另注意语料库存在多个 a11y 主题技能（281-wcag-accessibility-audit、242-auditor-de-acessibilidade、234-ux-audit 及 286-captions-media-accessibility），本技能与它们的边界在 §11 单独讨论。

## §2 审查文件与角色

| 文件 | 角色 | 要点 |
|------|------|------|
| `SKILL.md` | 被审对象 | 202 行，frontmatter 2 个键，正文含 8 个子节 |
| `SCORING.yaml` | 评分契约 | 17 项 criteria + 3 项 critical failures；8 项 judge: script、9 项 judge: llm |
| `check.py` | 脚本评分实现 | 与 SCORING.yaml 的 8 项 script 检查一一对应 |
| `_shared/SKILL-SPEC.md` | 合规基准 | v1.0 规范，共 5 章（frontmatter / description / body / 命名 / 清单） |
| `skill-dossier.md` | 语料库档案 | 322 技能总体统计；099 仅有占位性合并记录 |
| `complex-skills-no-trigger/099-tpl-situacao-acessibilidade-a11y/SKILL.md` | 对照物 | 与触发版 diff 仅 2 处：description 去触发、首条原则 "1. " 前缀被剥离 |
| `281-wcag-accessibility-audit/SKILL.md`、`242-auditor-de-acessibilidade/SKILL.md` | 兄弟技能 | 同主题重叠对比（详见 §11） |

审查方法：逐行阅读 SKILL.md；对照 SKILL-SPEC §1-§5 逐条打勾；逐项核验 SCORING.yaml 17 项 criteria 与本技能文本的支撑关系；对文中数值型断言（对比度比值、字号阈值）做独立复算；对 React 示例代码做逻辑走查。

## §3 Frontmatter 合规审查（SKILL-SPEC §1）

| 检查项 | 结果 | 证据 |
|--------|------|------|
| `name` 小写 + 连字符 | ✅ | `tpl-situacao-acessibilidade-a11y` |
| `name` ≤64 字符 | ✅ | 34 字符 |
| `name` 与目录名一致 | ✅ | 与 `099-tpl-situacao-acessibilidade-a11y` 完全一致 |
| 仅允许的字段 | ✅ | 只有 `name` 与 `description`，无任何禁用键 |
| 禁用键清单（§1.3） | ✅ | 未出现 metadata/version/tags/trigger 等 32 个禁用键 |

结论：frontmatter 完全合规。与家族其他成员（029/030/046/058/059/078 等）一样保持极简双键，无违规字段，亦无 `allowed-tools` 空值等家族内曾出现的次级缺陷（对比 021-react-native 的空 `allowed-tools:`）。

## §4 Description 合规审查（SKILL-SPEC §2）

原文（SKILL.md 第 3 行）：

> Pack template (situacao/19-acessibilidade-a11y.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is auditing an application for accessibility (a11y) compliance, implementing WCAG 2.1 AA requirements, or fixing accessibility issues.

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 第三人称（§2.3） | ✅ | "Guides the agent..." 为第三人称描述技能自身 |
| 触发信号短语（§2.4） | ✅ | "Use when the user..." 命中规范模板 |
| ≤1024 字符 | ✅ | 约 296 字符 |
| WHAT + WHEN + KEYWORDS（§2.1） | 🟡 | WHEN 充分（auditing/implementing/fixing 三场景）；KEYWORDS 有 a11y/WCAG 2.1 AA；但 WHAT 被家族模板套话取代 |
| 无祈使/第一/第二人称开头 | ✅ | 不以 "Use this skill..." / "I..." / "You..." 开头 |
| 无跨技能路由（§2.5） | ✅ | 无 "NOT for X, use Y" 结构 |
| ≥40 字符 | ✅ | 远大于 40 |

问题点（详见 §13 之 A4、B4）：

1. 开头 "Pack template (situacao/19-acessibilidade-a11y.md)." 是来源溯源而非功能描述——违反"WHAT 优先"结构；且该路径 `situacao/19-acessibilidade-a11y.md` 在语料库中不存在（它是上游模板包的路径）。
2. "Guides the agent on situational tasks such as debugging, security and refactoring" 是家族复制的套话，与本技能的实际内容（无障碍审计与修复）毫无关系——058 在档案中被指出同一缺陷，099 未幸免。

## §5 Body 结构合规审查（SKILL-SPEC §3）

### §5.1 必备节检查（§3.1）

| 必备节 | 结果 | 说明 |
|--------|------|------|
| Workflow / Process | ❌ | 无任何逐步执行流程。7 条原则是知识断言，路由表是决策表，清单是核查项，但"先做什么、后做什么"的排序从未出现 |
| Output Format | ✅ | `## OUTPUT FORMAT`（第 150–189 行）：严重度汇总表、关键问题条目模板、键盘导航核查、对比度失败表，结构完整 |
| Scope / Limitations | ❌ | 无独立 Scope 节。`## DO NOT`（第 139–148 行）是反模式禁令而非范围声明，未说明"本技能不做什么 / 何时不应使用" |

结论：3 项必备节仅满足 1 项。这是全语料库最普遍的合规缺口（档案统计约 68% 缺 Scope 节、56% 缺 Output 节），本技能 Output 齐备但其余两项缺席。

### §5.2 体量与参考（§3.2 / §3.3）

| 检查项 | 结果 | 说明 |
|--------|------|------|
| ≤600 行硬上限 | ✅ | 202 行（process pattern 目标 ~200 行，恰好达标） |
| 引用相对路径 | ✅（无引用） | 无 `references/` 目录、无脚本引用，技能完全自包含 |
| 无跨技能文件路径 | ✅ | 无 `../other-skill/` 类引用；但按 §3.3 应"在正文中以名称提及兄弟技能"——本技能未提及（见 §13 B3） |

### §5.3 内容组织盘点

| 子节 | 位置 | 体量 | 评价 |
|------|------|------|------|
| 7 条原则 | 第 8–20 行 | 13 行 | 编号完整（家族缺陷"1. **"断裂在此不出现，见 §12） |
| ROUTING TABLE | 第 22–35 行 | 11 行 | 11 个典型情境，决策表化，符合 §3.4 |
| WCAG 2.1 AA Checklist | 第 37–68 行 | 24 项 | Perceivable 8 / Operable 8 / Understandable 5 / Robust 3 |
| Focus Indicator CSS | 第 70–97 行 | ✅/❌ 对照 | 好/坏双示例 + .sr-only 工具类 |
| Modal 示例（React/TSX） | 第 99–137 行 | 完整组件 | 逻辑走查见 §7.3 与 §13 A3 |
| DO NOT | 第 139–148 行 | 8 条 | 全部为"具体反模式 + 理由"，符合 §3.4 要求 |
| OUTPUT FORMAT | 第 150–189 行 | 报告模板 | 含数值正确的对比度示例（见 §7.2） |
| QUALITY GATES | 第 191–202 行 | 10 条 | 与 SCORING.yaml 的 critical failures 语义对齐（见 §10） |

## §6 目录命名合规审查（SKILL-SPEC §4）

| 检查项 | 结果 |
|--------|------|
| `NNN-kebab-case/` | ✅ `099-tpl-situacao-acessibilidade-a11y/` |
| 无空格、无大写 | ✅ |
| 与 `name` 一致 | ✅ |

无问题。家族成员命名风格统一（tpl-situacao-*），本技能是序列 099。

## §7 领域正确性审查（WCAG 2.1 AA 事实核验）

### §7.1 原则与清单的事实准确性

逐条核验 7 条原则与 24 项清单的领域断言，全部正确：

- 语义 HTML 优先于 ARIA（1.1）：标准实践，"Incorrect ARIA is worse than no ARIA" 是无争议的领域共识。
- 键盘可达性与焦点指示（2.1.1 / 2.4.7）：正确。
- 焦点管理（2.4.3）：模态开/关的焦点进出规则正确。
- 颜色非唯一信息载体（1.4.1）：正确。
- alt 文本规则（1.1.1）：`alt=""` 装饰图、信息图描述、图标按钮 `aria-label`，三分类正确。
- 对比度阈值（1.4.3 / 1.4.11）："4.5:1 正文、3:1 大字（18pt+ 或 14pt+ 粗体）、3:1 UI 组件"——与 WCAG 2.1 定义精确一致（大字即 24px 或 18.66px 粗体；非文本对比度 3:1）。
- 自动工具覆盖率 ~30%：与 WebAIM 等广泛引用的估计一致，属合理经验值。
- 清单 24 项：200% 缩放（1.4.4）、320px 视口回流（1.4.10）、每秒 3 次闪光（2.3.1）、页面标题（2.4.2）、焦点顺序（2.4.3）、lang 声明（3.1.1）、语言切换标记（3.1.2）、可见标签（3.3.2）、错误识别（3.3.1）、无意外上下文变化（3.2.2）、aria-live 状态消息（4.1.3）——全部映射到真实准则且分级正确。
- "Valid HTML"（Robust 首项）对应 2.1 的 4.1.1 Parsing（Level A）：本技能明确目标为 WCAG 2.1 AA，故保留该项是正确的；但需注意 4.1.1 已从 WCAG 2.2 移除，若未来升级目标版本须删除（见 §13 C4）。

### §7.2 数值断言复算（全部通过）

输出模板中的对比度示例是自证正确的关键证据，独立复算结果：

| 断言 | 复算 | 结果 |
|------|------|------|
| #999999 对 #FFFFFF = 2.85:1 | (1.05)/(0.318+0.05) ≈ 2.85 | ✅ 正确 |
| #AAAAAA 对 #EEEEEE = 1.9:1 | (0.883)/(0.452) ≈ 1.95 | ✅ 正确 |

两个示例均低于对应阈值（2.85<4.5、1.95<3），与"失败示例"的角色一致——数值与语义双重正确。此类可复算示例在全语料库中并不常见（对比 039-db-seed 的价格范围算错、074-social-media-analyzer 的 ROI 矛盾），应记为本技能亮点。

### §7.3 React Modal 示例代码走查（问题所在）

```tsx
useEffect(() => {
  if (isOpen) {
    triggerRef.current = document.activeElement as HTMLElement
    const firstFocusable = modalRef.current?.querySelector<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    firstFocusable?.focus()
  } else {
    triggerRef.current?.focus()
  }
}, [isOpen])
```

走查发现三个问题：

1. **声明与实现矛盾（主要）**：示例输出 `aria-modal="true"`，且路由表第一行明确要求 "Trap focus within"，但组件未实现任何 Tab 键焦点陷阱（无 keydown 处理器）。`aria-modal="true"` 向辅助技术宣称模态外内容不可交互，而实际键盘用户可 Tab 到背景元素——这是无障碍语义与实现行为的直接矛盾。要么补 Tab 陷阱，要么去掉 `aria-modal`。
2. **无 Escape 关闭**：键盘用户无法用 Esc 关闭模态；路由表也未提。属于模态键盘可用性（2.1.1）的常规要求。
3. **triggerRef 依赖时序**：通过 `document.activeElement` 捕获触发器而非 `ref` 绑定；若从模态内打开第二层模态，`triggerRef` 会被覆盖，关闭时焦点回到内层模态而非最初触发元素（多层模态边缘场景）。

### §7.4 结论

领域知识主体准确、数值自洽、示例贴近实战（checkout 流程报告模板非常具体）。除 Modal 示例的陷阱缺失外，无事实性错误。

## §8 路由表 / 清单 / DO NOT / 质量门审查

### §8.1 路由表（第 22–35 行）

11 个情境覆盖了高频实战场景：div 点击元素、缺 label、图标按钮、对比度失败、模态焦点、skip link、自动播放、错误关联、表格头、自定义下拉。行内建议具体到代码片段级（如 `<th scope="col">`、`<span lang="fr">`），符合 §3.4 "具体优于抽象"。与 SCORING.yaml 的 PROC-01 正则（`<button\b|<label[ >]|role="button"|tabIndex{0}|tabindex="0"|<a [^>]*href`）高度同构——技能文本驱动的行为恰好就是检查项，映射质量好。

### §8.2 清单（24 项）

POUR 四象限分布均衡（8/8/5/3）。微瑕：绝大多数项未附准则编号（如 "[ ] Text can be resized to 200%" 未标 1.4.4），对输出报告需引用准则的场景（OUT-02）略少赋能——输出模板中的问题条目示例是唯一给出编号的地方（见 §13 C1）。

### §8.3 DO NOT（8 条）

全部为带理由的具体禁令，无一条是空泛警告："outline: none"、placeholder 冒充 label、只跑自动工具、div role="button" 缺键盘、颜色传达错误、aria-label 覆盖可见文本、页面加载自动聚焦、tabIndex>0——其中 "aria-label 覆盖可见文本" 一条属高阶内容，多数同类技能未覆盖，是知识增量亮点。

### §8.4 QUALITY GATES（10 条）

覆盖自动工具归零、全键盘走查、持久标签、模态焦点、对比度、alt、lang、skip link、屏幕阅读器实测、prefers-reduced-motion。与 SCORING.yaml 的 CF-03（无验证证据不得声称合规）直接咬合：第 1、2、9 条门禁即为 CF-03 的行为化表达。NEG-02（不依赖纯自动工具）对应第 9 条门禁与第 7 条原则，双保险。

## §9 人机感审查

| 维度 | 评价 |
|------|------|
| 语气 | 专业、指令式、无 chatbot 腔；无 "Let's"、无问候语、无推销 |
| emoji | 仅 ✅/❌ 出现在 CSS 代码注释与报告模板中，属功能性标记（好/坏对照、通过/失败），非装饰 |
| 称呼 | 无第二人称对用户喊话；DO NOT 与原则均以 agent 为执行主体（与家族 101/115/116 的"双重受众混淆"不同，本技能受众单一清晰） |
| 冗余度 | 紧凑；无重复节（对比 003 的 120 行逐字重复、294 的重复章节） |
| 亮点 | 输出模板与清单的复选框风格让 agent 可以逐项勾选交付，人机协同顺畅 |

人机感无实质问题，在全语料库中属于干净的第一梯队。

## §10 SCORING.yaml / check.py 映射审查

### §10.1 数量与一致性

SCORING.yaml 17 项 = 8 项 script + 9 项 llm；check.py 恰好实现 8 项 script 检查，数量一致、id 一一对应（PROC-01/PROC-04/TEC-01/TEC-02/TEC-04/OUT-01/NEG-01/QA-01），无遗漏无多余。check.py 通过 `sys.path` 引入 `_shared/checker`，依赖 `tool_log_contains` / `tool_log_not_contains` / `output_contains` 三个函数，与 CHECKER-LIBRARY.md 的接口一致。

### §10.2 技能文本对 17 项 criteria 的支撑度

| Criteria | 支撑来源 | 支撑度 |
|----------|----------|--------|
| SCOPE-01 识别 a11y 任务 | description 触发 + H1 情境标题 | 强 |
| SCOPE-02 不越界 | 无文本支撑（无 Scope 节） | 弱 —— 靠 agent 自觉 |
| SCOPE-03 先声明审计范围 | 仅输出模板中的 "**Scope:**" 行 | 弱 —— 技能从不说"开始前先声明范围" |
| PROC-01 语义 HTML | 原则 1 + 路由表行 1 | 强 |
| PROC-02 模态焦点管理 | 原则 3 + 路由表行 5 + 示例代码 | 强（但示例陷阱缺失，见 A3） |
| PROC-03 颜色非唯一载体 | 原则 4 + DO NOT 行 5 | 强 |
| PROC-04 prefers-reduced-motion | 路由表行 7 + 质量门 10 | 中（无 CSS 示例，见 C2） |
| TEC-01 alt 文本 | 原则 5 + 质量门 6 | 强 |
| TEC-02 对比度验证 | 原则 6 + 质量门 5 | 强 |
| TEC-03 键盘导航验证 | 清单 Operable + 质量门 2 | 强 |
| TEC-04 lang + skip link | 清单 Understandable 行 1 + 路由表行 6 + 质量门 7/8 | 强 |
| OUT-01 严重度汇总表 | 输出模板 Summary 表 | 强 |
| OUT-02 问题条目五要素 | 输出模板 Critical Issues 条目 | 强 |
| OUT-03 质量门报告 | 输出模板 + 质量门 | 强 |
| NEG-01 不删焦点指示 | DO NOT 行 1 | 强（但存在误报风险，见 B2） |
| NEG-02 不纯靠自动工具 | 原则 7 + DO NOT 行 3 + 质量门 9 | 强 |
| QA-01 自动工具证据 | 质量门 1 | 强 |

结论：15/17 有明确文本支撑；SCOPE-02 与 SCOPE-03 两项缺乏驱动文本，是本技能与评分契约之间仅有的两个"空档"。

### §10.3 检查实现的风险点

1. **NEG-01 误报风险（值得关注）**：检查为 `tool_log_not_contains('outline:\s*none|...')`，作用于工具调用日志。技能自身第 80–83 行就给出了 `* { outline: none; }` 的 ❌ 反例——若 agent 忠实示范"好/坏对照"（把反例写进工作区文件），Write 调用即污染工具日志，NEG-01 判负，尽管 agent 行为完全正确。评分器无法区分"引入反模式"与"演示反模式"。缓解：检查改为针对最终交付文件而非工具日志，或至少将反例写法限定为注释形式。
2. **NEG-01 正则冗余**：`outline:\s*0|outline: 0` 中第二项已被第一项覆盖（SCORING.yaml 与 check.py 同源），属无害冗余。
3. **OUT-01 弱匹配**：`Critical|Serious|Moderate|Minor` 是单词级匹配，报告正文任意一处出现即通过；在无障碍语境下误报概率低，可接受。
4. **CF 与技能的语义一致性**：CF-01（div 无 role/tabIndex/键盘处理器）、CF-02（全局 outline:none 或键盘陷阱）、CF-03（无证据声称合规）——三条 cap_to_0 的门槛都与技能文本的禁令一一对应，无冲突。技能路由表允许"div + role + tabIndex + 处理器"的例外与 CF-01 的豁免条件完全一致，设计上相互印证。

## §11 兄弟技能与语料库定位

语料库中与 a11y 直接相关的技能至少有 5 个：

| 技能 | 主题 | 档案评级 |
|------|------|---------|
| 099-tpl-situacao-acessibilidade-a11y | 情境模板：审计 + 实施 | 本次审查 🟡 |
| 234-ux-audit | UX 审计，含 `references/a11y-automation.md` | 未单列 |
| 242-auditor-de-acessibilidade | WCAG/ARIA 专家型审计 | 未单列 |
| 281-wcag-accessibility-audit | 完整 WCAG 2.1/2.2 POUR 审计 + 合规等级 | 🟢 三节齐备 |
| 286-captions-media-accessibility | 字幕/媒体无障碍 | 🟢 无障碍范本 |

问题：099 与 281 的任务边界几乎重合（都是"审计应用 + 修复 + 输出报告"），与 242 的领域也重叠；三者无任何相互引用。SKILL-SPEC §3.3 明确要求"提及另一技能时使用其名称"——本技能正文零提及。对 agent 而言，同一请求可命中三个重叠技能，触发歧义直接损害评估可复现性（测评矩阵 2 Mode × 5 Harness 下尤其敏感）。建议：099 在 Scope 节声明"完整准则级审计见 wcag-accessibility-audit；本技能定位为情境化快检 + 修复执行"，形成分工而不是重复（见 §13 B3）。

## §12 模板家族共性分析（tpl-situacao）

家族 17 个 tpl-situacao-* 技能（029/030/046/058/059/078/099/101/115/116/131/132/145/146/166-169/259-260 等）共享三处同源缺陷，逐项对照 099：

| 家族缺陷 | 家族典型 | 099 状态 |
|----------|----------|----------|
| 首条原则编号断裂（"1. **" 前缀丢失） | 029/030/046/058/059/078/131/132/145/146/166-169 | ✅ 幸免 —— 第 8 行 "1. **Semantic HTML first..." 编号完整 |
| description 模板套话失配（"debugging, security and refactoring"） | 058/059 等 | ❌ 同样存在（A4） |
| 缺 Scope / 显式 Workflow 节 | 全家 | ❌ 同样存在（A1/A2） |

额外发现：**无触发变体的编号断裂是管线产生的**。对 `complex-skills-no-trigger/` 对照物做 diff，唯一内容差异除 description 去触发外，就是把首条原则的 "1. " 前缀也剥离了（"Semantic HTML first, ARIA second.**"），制造出家族同款断编号。说明触发剥离管线对编号前缀的处理有副作用，建议在 `create_no_trigger_set.py` 侧修复（该缺陷影响全部 17 个家族成员的无触发副本）。

家族质量排序：099 属上乘组（有路由表 + 清单 + 代码示例 + 输出模板 + 质量门的只有 029/046/099/078 等少数成员，多数家族成员只有"原则 + DO NOT"两层）。修复 §13 的 A 级问题后，099 可成为家族标杆。

## §13 问题清单与修复建议（最重篇幅）

### 13.1 问题总表

按严重度分三档。A = 高（影响合规或正确性，必须修复）；B = 中（影响评分映射或使用体验，应当修复）；C = 低（打磨项，可选）。

### 13.2 A 级问题

**A1 — 缺 Scope / Limitations 节（SKILL-SPEC §3.1 硬性要求）**

- 严重度：高
- 证据：正文 202 行内无任何 "Scope" / "Limitations" / "What This Skill Does NOT Do" 标题；`## DO NOT` 是反模式禁令，不是范围声明。
- 影响：直接违反规范 §3.1 三条必备节之一；且 SCOPE-02（不得把本技能用到无关工作）无文本驱动，评估中"agent 是否越界"全靠自由发挥。语料库 ~68% 技能有同一缺口，但这不降低本技能的合规责任。
- 修复：在 QUALITY GATES 之后新增一节，至少覆盖：(a) 不做完整的准则逐项合规审计（那是 wcag-accessibility-audit 的职责）；(b) 不处理后端逻辑、全站重设计、新功能开发等无关范围；(c) 不适用于非 Web 应用（桌面/原生 App 需调整清单）；(d) 屏幕阅读器实测依赖本机环境，无法替代时须显式报告降级；(e) 何时不应使用——用户只要求快速视觉检查、或明确排除了键盘/AT 场景时。

**A2 — 缺显式 Workflow / Process 节（SKILL-SPEC §3.1 硬性要求）**

- 严重度：高
- 证据：全文无逐步流程。原则 1–7 是知识、路由表是决策、清单是核查、质量门是验收，唯独没有"按什么顺序执行"。
- 影响：技能实际运行时的行为序列完全未定义——agent 可能从"读页面源码"开始、也可能从"跑 axe"开始、也可能从"直接改写代码"开始。评估的 PROC-01/04、TEC-01/02/04、QA-01 都是"是否出现"型检查，掩盖了顺序缺失，但真实任务的产出质量（先审计后修复、先证据后结论）会分化。这也是 CF-03（无证据声称合规）的温床：没有流程约束的 agent 容易直接给结论。
- 修复：在 ROUTING TABLE 之前新增 `## WORKFLOW`，定义 5 步审计执行流：① 声明范围（页面/流程清单、WCAG 目标 2.1 AA、工具集）→ ② 自动扫描（axe/Lighthouse 全页面，导出原始结果）→ ③ 手动核查（键盘全流程走查、模态焦点、对比度抽样实测）→ ④ 屏幕阅读器验证（NVDA/VoiceOver 完成关键流程，记录实际步骤）→ ⑤ 汇编报告 + 质量门自检。每步写明输入/输出，与既有路由表和清单形成闭环。第 ① 步同时补上 SCOPE-03 的文本支撑。

**A3 — React Modal 示例声明与实现矛盾（无焦点陷阱、无 Escape）**

- 严重度：高
- 证据：第 124–136 行示例包含 `aria-modal="true"`；路由表第 30 行明确要求 "Trap focus within"；但组件内没有任何 keydown/Tab 处理，焦点可自由 Tab 到模态外背景内容。此外无 Escape 关闭处理器。
- 影响：这是本技能唯一一处领域事实性瑕疵，且位于最显眼的示例代码位置。`aria-modal="true"` 而无法陷阱 = 语义宣称与真实行为矛盾，恰恰违反了技能自己第 1 条原则（"Incorrect ARIA is worse than no ARIA"）。照抄示例的 agent 会复刻一个有缺陷的模态。
- 修复：二选一——(a) 在组件内补 Tab 陷阱（keydown 处理、循环 `querySelectorAll` 焦点元素）+ Escape 关闭 + `aria-describedby` 关联描述；(b) 若要保持示例简短，则删除 `aria-modal` 并注明"真实生产模态必须实现焦点陷阱，此处省略"并在路由表处给引用。建议 (a)，因为本技能面向实战修复，示例应可直接复制。

**A4 — description 家族套话失配（"debugging, security and refactoring"）**

- 严重度：高
- 证据：第 3 行 "Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context."
- 影响：三个列举场景与本技能内容（审计/实施/修复无障碍）零交集。该 description 同时用于 17 个家族成员，语义槽位完全相同——对触发匹配（SkillIF 测评的核心变量）而言，这段文字是噪音：检索/嵌入匹配时会把 a11y 查询与 "debugging/security/refactoring" 错误关联。档案对 058 标注了同一缺陷但 099 未被修复（因为 099 从未被单独审查）。
- 修复：替换为真实内容，例如 "Provides accessibility (a11y) audit and remediation guidance — semantic HTML, keyboard access, focus management, color contrast, and screen-reader testing against WCAG 2.1 AA. Use when the user is auditing an application for accessibility compliance, implementing WCAG 2.1 AA requirements, or fixing accessibility issues."

### 13.3 B 级问题

**B1 — 技能从不要求"先声明审计范围"（SCOPE-03 无支撑）**

- 严重度：中
- 证据：全文检索 "scope" 仅出现在输出模板的 "**Scope:** Checkout flow (5 pages)" 一行；没有任何文本指示 agent 在动手前声明范围。
- 影响：SCOPE-03 是 LLM 判定项，脚本不查，但评估中该题稳定性差——agent 报不报范围全凭运气。修复随 A2 的 Workflow 第 ① 步一并完成。

**B2 — NEG-01 评分器与技能自身 ❌ 示例的误报风险**

- 严重度：中
- 证据：check.py 第 55 行 `tool_log_not_contains('outline:\s*none|...')`；技能第 80–83 行主动给出 `* { outline: none; }` 反例。
- 影响：agent 若把好/坏 CSS 对照写进项目文件（本技能的教学设计恰好鼓励对照演示），工具日志即含 `outline: none`，NEG-01 判负。此误报路径不是假设——输出模板与 CSS 节的双示例结构就在诱导这种写法。
- 修复建议：(a) 评分侧——把 NEG-01 改为对最终交付文件检查，或把反例写法规范化为注释（`/* DO NOT: * { outline: none } */`）再落盘；(b) 技能侧——无需改，反例教学价值高，问题在评分器粒度。

**B3 — 未按 §3.3 以名称引用兄弟技能，语料库重叠未界定**

- 严重度：中
- 证据：正文无任何 "wcag-accessibility-audit" / "auditor-de-acessibilidade" 字样；281 与 242 亦无反向引用。
- 影响：3 个技能任务边界重合，同一 prompt 可触发多个，评估归因（哪个技能生效）不可复现。测评矩阵 2 Mode × 5 Harness 下，重叠技能会稀释 trigger 测量的效度。
- 修复：随 A1 的 Scope 节加入一行 "see also: wcag-accessibility-audit（准则级完整审计）、auditor-de-acessibilidade"，并各自声明分工。

**B4 — description 以来源路径开头而非 WHAT**

- 严重度：中
- 证据："Pack template (situacao/19-acessibilidade-a11y.md)." 是上游模板包路径，语料库中不存在该文件。
- 影响：a) 违反 §2.1"WHAT 优先"；b) 对 agent 是无效承诺（agent 可能尝试读取该路径）；c) 泄漏数据来源，削弱测评"盲测"属性。修复随 A4 一并完成。

**B5 — Modal 示例 triggerRef 依赖运行时时序，多层模态失效**

- 严重度：中
- 证据：第 110 行 `triggerRef.current = document.activeElement as HTMLElement`，无 ref 属性绑定；从模态内打开第二层模态时触发器被覆盖。
- 影响：边缘场景（嵌套对话框）下焦点归还错误；对示例级代码可接受，但作为"可直接复制"的教材应说明限制或改 ref 绑定。修复随 A3 一并处理。

### 13.4 C 级问题

**C1 — 清单 24 项几乎未附 WCAG 准则编号**：仅输出模板的条目示例给编号。建议给每项附编号（如 "[ ] Text can be resized to 200% without loss (1.4.4)"），直接提升 OUT-02 的产出质量。低优先级，可批量完成。

**C2 — prefers-reduced-motion 仅文字提及，无 CSS 示例**：路由表行 7 与质量门 10 提及，但没有 `@media (prefers-reduced-motion)` 代码块。鉴于 CSS 节已存在，补一个 5 行示例成本极低。

**C3 — 大字阈值只给 pt 不给 px**：原则 6 的 "18pt+ or 14pt+ bold" 正确，但前端语境 px 更常用（24px / 18.66px 粗体）。补括号换算即可。

**C4 — 无 WCAG 2.2 前瞻说明**：目标 2.1 AA 内部一致，不构成错误；但清单 Robust 首项 "Valid HTML"（4.1.1）在 2.2 中已废弃，若未来升级版本需删除/替换为 4.1.3 项。建议在清单头部加一行版本说明。

**C5 — 无触发变体的首条编号断裂（管线缺陷外溢）**：`complex-skills-no-trigger/` 版本首条原则丢失 "1. " 前缀，产生家族同款渲染破损。缺陷源在触发剥离管线（`create_no_trigger_set.py`），应修管线而非修文档；但为保测评集完整性，两处都该修。

**C6 — NEG-01 正则冗余**：`outline:\s*0|outline: 0` 中第二备选被第一备选包含。无害，清理即可。

**C7 — Dossier 对 099 的占位性合并记录**：档案将 099 归入 "093-data-privacy-compliance — 100 系列" 条目，内容却是 GDPR 描述，与 099 无关；批次统计也未单列。建议档案补一条 099 单独记录（本 REVIEW.md 可作底稿）。

**C8 — 家族 description 套话的批量修复**：A4 不只影响 099——17 个家族成员的 description 都带 "debugging, security and refactoring" 槽位。建议对家族做一次批量替换（各成员换成各自领域词），成本低于逐个审查。

### 13.5 修复优先级与工作量

| 优先级 | 问题 | 工作量 | 建议批次 |
|--------|------|--------|----------|
| P0 | A1 Scope 节、A2 Workflow 节 | 各 20–30 行文本 | 本次立即修 |
| P0 | A4 + B4 description 重写 | 1 行 frontmatter | 本次立即修 |
| P0 | A3 Modal 焦点陷阱 + Escape | 示例 +15 行 | 本次立即修 |
| P1 | B1 范围声明（随 A2） | 含在 A2 内 | 与 P0 同步 |
| P1 | B2 NEG-01 评分粒度 | check.py 改动 | 与测评管线同步 |
| P1 | B3 兄弟技能引用 | Scope 内 1 行 | 与 A1 同步 |
| P1 | B5 嵌套模态注释 | 注释 2 行 | 随 A3 |
| P2 | C1–C6 | 各 5–15 分钟 | 下轮迭代 |
| P2 | C7 档案补录 | 档案 +10 行 | 下轮迭代 |
| P2 | C8 家族批量描述 | 17 文件批量脚本 | 需协调 |

### 13.6 修复后的预期效果

若 P0 全部落地：合规面从"3 必备节只满足 1 项"变为 3/3；description 从家族模板套话变为领域精准；Modal 示例从"自相矛盾"变为"可直接复制"。评分面：SCOPE-02/03 从"无支撑"变为"文本驱动"，17 项 criteria 的支撑度从 15/17 升为 17/17；NEG-01 误报路径关闭。届时 099 可进入档案 🟢 名单，并成为 tpl-situacao 家族的结构标杆（其余 16 个成员可参照其 Workflow + Scope 结构补齐）。

### 13.7 明确不做的事（审查边界）

本次审查不涉及：a) 评估运行结果数据（outputs/ 目录的 SCORING.yaml 副本与检查器一致，未复跑）；b) 其他语言 harness 适配（AGENTS.md / toml / mdc 转换的正确性）；c) 屏幕阅读器工具链本身的实证验证（NVDA/VoiceOver 操作步骤属领域常识，未超出核验范围）。这些如需审查，另行立项。

### 13.8 最终评级

| 维度 | 得分（5 分制） | 一句话 |
|------|:----:|--------|
| 逻辑一致性 | 4.0 | 主体自洽，仅 Modal 示例陷阱缺失一处矛盾 |
| 语法与可读性 | 4.5 | 干净无错字，表格结构优 |
| 人机感 | 4.5 | 专业克制，无 emoji 滥用，受众单一 |
| 规范合规性 | 2.5 | 缺 Scope + 显式 Workflow 两节，description 套话失配 |
| 领域正确性 | 4.5 | 对比度数值复算全对，WCAG 2.1 AA 映射准确 |

**总评：🟡 可用但有小问题。** 内容质量在 tpl-situacao 家族中居首（路由表/清单/示例/输出模板/质量门五件套齐全，数值自证正确），核心短板是结构合规——Scope 与显式 Workflow 两节缺失、description 家族套话与内容失配、Modal 示例声明与实现矛盾。完成 §13.5 的 P0 批次（预计 1 小时内）即可达 🟢，并可作为家族其余成员的结构修复模板。
