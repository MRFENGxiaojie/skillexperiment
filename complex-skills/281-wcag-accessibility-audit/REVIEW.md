# REVIEW: 281-wcag-accessibility-audit

**审查日期**: 2026-08-06 | **审查者**: Claude | **审查范围**: 全目录 16 个文件全文精读 + `_shared/SKILL-SPEC.md` v1.0 + `_shared/checker.py` + 同级参考 REVIEW.md（043-nielsen-heuristics-audit，格式对齐）

**审查方法**: 对 16 个文件（SKILL.md、SCORING.yaml、check.py、references/ 下 13 个文件）逐一全文阅读，零文件跳过；所有 YAML/代码均通过解析验证（`yaml.safe_load`、`py_compile` 均通过）；WCAG 事实性声明与 W3C 官方文本及公开资料交叉核对（含 4.1.1 Parsing 在 WCAG 2.2 中的移除状态）；SCORING.yaml 16 项准则与 SKILL.md 逐条追溯；对比 WCAG 2.2 官方 9 条新增成功准则原文。

**总评**: 这是本次语料中评测对齐度最高的技能之一——SCORING 16 项准则全部可追溯至 SKILL.md 具体内容，3 项 critical failure 与安全声明/负面约束严丝合缝。内容主体事实高度准确（对比度数值、9 条新 SC 级别、ISO 状态全部核对无误）。主要问题集中在三处：①正文缺少显式 Scope/Limitations 节（规范 12 项清单唯一不达标项）；②若干成功准则的细节归属混入相邻准则（2.4.7 的 2px、1.4.3 的组件对比度、1.4.4 的横向滚动），且 4.1.1 未标注"WCAG 2.2 已移除"；③执行流程假设 agent 能物理操作浏览器/屏幕阅读器，却未给出工具不可用时的如实声明指引——这对本实验的 agent 执行环境是实质隐患。

**综合评分**: **B+ (84/100)**（八维加权见 §12.5；旧 dossier 档案未查阅到 281 号条目独立评分，本次为首次深度审查）。

---

## 1. 目录清单

| # | 文件 | 行数 | 类型 | 审查状态 |
|---|------|:----:|------|:--------:|
| 1 | `SKILL.md` | 497 | 主技能文件 | ✅ 全文精读 |
| 2 | `SCORING.yaml` | 150 | 评测准则（16 项 + 3 项 critical failure） | ✅ 全文精读 + YAML 解析校验 |
| 3 | `check.py` | 59 | 评测脚本（0 项 script 检查，全 llm judge） | ✅ 全文精读 + 编译校验 |
| 4 | `references/accessibility-statement-recommendations.md` | 17 | 无障碍声明模板 | ✅ 全文精读 |
| 5 | `references/best-practices.md` | 13 | 最佳实践 | ✅ 全文精读 |
| 6 | `references/common-quick-wins.md` | 12 | 快速修复清单 | ✅ 全文精读 |
| 7 | `references/detailed-findings-by-principle.md` | 78 | 按 POUR 原则的发现模板 | ✅ 全文精读 |
| 8 | `references/legal-disclaimer.md` | 6 | 法律免责声明 | ✅ 全文精读 |
| 9 | `references/methodology-notes.md` | 17 | 方法论备注 | ✅ 全文精读 |
| 10 | `references/next-steps.md` | 27 | 后续行动清单 | ✅ 全文精读 |
| 11 | `references/prioritized-remediation-plan.md` | 41 | 分阶段修复计划 | ✅ 全文精读 |
| 12 | `references/resources.md` | 25 | 外部资源链接 | ✅ 全文精读 |
| 13 | `references/success-criteria-priority-matrix.md` | 12 | 优先级矩阵 | ✅ 全文精读 |
| 14 | `references/testing-tools-used.md` | 19 | 测试工具记录模板 | ✅ 全文精读 |
| 15 | `references/version.md` | 6 | 版本记录 | ✅ 全文精读 |
| 16 | `references/wcag-2-2-new-success-criteria-summary-2023.md` | 16 | WCAG 2.2 新增 SC 摘要 | ✅ 全文精读 |

**外部参照**: `_shared/SKILL-SPEC.md`（161 行，合规 12 项清单，§7 逐项核对）、`_shared/checker.py`（check.py 的导入库，实际存在 ✅）、同级 043 号 REVIEW.md（模板格式对齐）。

**目录健康度**: 16 个实体文件全部存在且可解析；SKILL.md L484-497 引用的 13 个 references 文件全部真实存在且一一对应（§5 逐一核对）；无孤文件、无缺失引用、无 `scripts/` 或 `assets/` 等未声明目录；SCORING.yaml `skill` 字段（L1）与目录名一致；`total_items: 16` 与实际文件数一致。SCORING 准则数与 `total_items` 均为 16（3 scope + 8 process + 3 output + 1 negative + 1 qa），内部自洽。

---

## 2. Frontmatter 审查

### 2.1 `name` 字段（SKILL.md L2）

`name: wcag-accessibility-audit` — 小写 + 连字符，≤64 字符，与目录名 `281-wcag-accessibility-audit` 一致（NNN 前缀按 §4 约定与 name 分离）。有趣的是，SKILL-SPEC §1.1 的官方示例字段值正是 `wcag-accessibility-audit`——本技能是 spec 的自证例子。✅ **通过**。

### 2.2 `description` 字段（SKILL.md L3）

原文（**479 字符**，≤1024 ✅）：

> "Comprehensive web accessibility audit using WCAG 2.1/2.2 guidelines. Evaluate compliance across 4 POUR principles (Perceivable, Operable, Understandable, Robust) with A, AA, AAA conformance levels. Use when the user asks to audit a website or app for accessibility, check WCAG 2.1/2.2 compliance, ensure legal conformance (ADA, Section 508, EAA), or prepare for accessibility certification."

按 SKILL-SPEC §2.1 三问拆解：

| 检查项 | 判定 | 说明 |
|--------|:----:|------|
| **WHAT**（做什么） | ✅ | "Comprehensive web accessibility audit using WCAG 2.1/2.2" 具体到标准版本、4 POUR 原则、三级合规等级 |
| **WHEN**（何时用） | ✅ | 五组触发场景：audit 网站/应用、检查 WCAG 合规、法律合规（ADA/Section 508/EAA）、认证准备 |
| **KEYWORDS**（关键词） | ✅ | audit、accessibility、WCAG、website、app、compliance、ADA、Section 508、EAA、certification 均为有效匹配词 |
| 长度 ≤1024 | ✅ | 479 字符 |
| 触发信号短语（§2.4） | ✅ | "Use when the user asks to..." 精确命中标准短语 |
| **语态（§2.3）** | ✅ | 首句 "Comprehensive web accessibility audit using..." 为描述性名词短语，无祈使/第一/第二人称引导；全句无 "Use this skill to..." 句式 |
| 跨技能路由（§2.5） | ✅ | description 内无 "NOT for X, use Y instead"；跨技能协作（Nielsen/DON Norman）放在正文 L14，符合 §3.3 的 prose 引用方式 |

**小结**: description 三要素齐全、长度合规、触发短语精确、语态规范，frontmatter 全项通过。

### 2.3 允许/禁止字段（SKILL.md L1-4）

Frontmatter 仅含 `name` 与 `description` 两个键，无 §1.3 禁止字段（无 metadata/version/tags/trigger 等任何多余键），未使用 allowed-tools 等可选字段（本技能为分析对话型，无固定工具白名单需求，合理）。✅ **通过**。

---

## 3. Body 结构

### 3.1 骨架与章节分布（SKILL.md，497 行）

| 行号 | 章节 | 内容定位 |
|------|------|---------|
| L6 | `# WCAG Accessibility Audit`（H1） | 标题 |
| L8-14 | 引言（3 段） | 技能定位 + L10 WCAG 2.2/ISO 状态 + L14 跨技能协作提示 |
| L17-25 | `## When to Use This Skill` | 7 条**正向**触发场景 |
| L29-38 | `## Inputs Required` | 6 项输入，1 REQUIRED + 5 OPTIONAL，均带默认值（AA / 2.2） |
| L41-76 | `## The 4 POUR Principles` | 4 原则 × 下设 Guidelines 列表（对应 WCAG 2.2 指南编号） |
| L79-87 | `## Conformance Levels` | A/AA/AAA 三级 + 法律要求提示 |
| L90-312 | `## Critical Success Criteria (Level A & AA)` | 34 条关键成功准则，按 POUR 分组，每条 = 要点 + 具体检查项 |
| L315-329 | `## Security Notice` | OWASP LLM01 提示注入防御，1 类不可信输入 + 3 条处理步骤 |
| L334-437 | `## Audit Procedure` | 4 步流程，各带时间预算与勾选清单 |
| L440-497 | `## Report Structure` | 报告模板（代码围栏）+ `## Reference Files` 13 文件入口 |

### 3.2 SKILL-SPEC §3.1 三必需节核对

| 必需节 | 判定 | 依据 |
|--------|:----:|------|
| **Workflow / Process** | ✅ | Audit Procedure（L334-437）：4 步（准备 15min → 自动化 20min → 手动 60-90min → 报告 30min），每步含可执行子步骤、时间预算、勾选清单，是全语料中流程颗粒度最高的之一 |
| **Output Format** | ✅ | Report Structure（L440-494）：完整报告模板（L443-480 代码围栏 38 行），从 Executive Summary 到 Reference Files 共 8 个区块，交付物形态定义充分 |
| **Scope / Limitations** | ❌ **缺失** | 正文无 Scope/Limitations/"What This Skill Does NOT Do" 类章节；L17-25 仅列 7 条**正向**触发，未回答"何时不应使用、不做什么"（如：不替代真实用户测试、不构成法律意见、无物理工具时不可声称已测试）。局限性仅以零散句子出现（L87 "legal obligations vary"、L372 "Automated tools catch ~30-40%"），且 references/methodology-notes.md 虽有 Limitations 小节，但 spec §3.1 要求的是 **SKILL.md 正文**必需节——**这是 12 项合规清单中唯一不达标项**（§7 第 10 项） |

### 3.3 体量

497 行 ≤ 600 行硬上限 ✅（SKILL-SPEC §3.2）。`pattern: process`（SCORING.yaml L2）目标体量 ~200 行，本技能 497 行为其 2.5 倍——但其中 L90-312 的 222 行是高密度知识区（34 条成功准则的定义与检查要点，无灌水），L443-480 报告模板 38 行为可复用交付物。知识增量（§3.4）成立：每条准则给的不是 WCAG 原文转述，而是"测试动作 + 具体反例/示例"（如 2.5.4 的 "Shake to undo → has undo button"）。**体量合理，无膨胀**。

### 3.4 格式噪音

约 12 处**双空行**（段间两空行夹行）：L15-16、L27-28、L39-40、L77-78、L88-89、L144-145、L226-227、L291-292、L313-314、L331-332、L437-438、L494-495 等。不影响 Markdown 解析，属排版噪音（§13-🟢-1）。

### 3.5 结构亮点

- **每步时间预算可审计**：Step 3 内部 6 个子测试 15+20+15+15+10+10=85 分钟，与标题 "60-90 minutes" 自洽；全过程 15+20+85+30=150 分钟 ≈ 2.5 小时，节奏合理。
- **勾选清单**（L378-432）用 `- [ ]` 形式，6 类测试各 6-7 项，可直接转执行核对单。
- **报告模板独立成代码围栏**，agent 可直接复制填充，格式约束性强。

---

## 4. 逻辑一致性

### 4.1 WCAG 事实性声明核对（通过项）

逐条与 W3C 官方文本核对：

- L10 "WCAG 2.2 is a W3C Recommendation and was approved as ISO/IEC 40500:2025" ✅ 正确（2023-10-05 成为 REC；2025-06 发布为 ISO/IEC 40500:2025）。
- L10 "WCAG 3 is still a working draft" ✅ 正确。
- 4 POUR 原则及指南编号（L45-77）与 WCAG 2.2 官方指南编号一一对应 ✅。
- 2.4.11 (AA)、2.4.12 (AAA)、2.4.13 (AAA)、2.5.7 (AA)、2.5.8 (AA)、3.2.6 (A)、3.3.7 (A)、3.3.8 (AA)、3.3.9 (AAA) 的级别标注全部正确 ✅（references/wcag-2-2-...-2023.md 与正文两处均无误）。
- L119 "Large text: 3:1 (18pt+ or 14pt+ bold)" ✅ 与 WCAG 定义一致（18pt=24px，14pt bold=18.66px bold）。
- detailed-findings-by-principle.md L33-35 对比度数学核对：#999999 对 #FFFFFF 相对亮度比 (1.05)/(0.3685)≈**2.85:1** ✅ 标注正确；#595959 对 #FFFFFF ≈**7.0:1** ✅ 标注正确。两个示例数字均准确，无随手编造。
- 3.3.4 的 Reversible/Checked/Confirmed 三要素 ✅ 与 WCAG 原文一致。

### 4.2 成功准则细节归属问题（3 处串线，🟡）

**问题 1 — L195 "Minimum 2px, high contrast" 挂在 2.4.7 Focus Visible (AA) 下**：2px 最小尺寸要求出自 **2.4.13 Focus Appearance（AAA）**，WCAG 2.4.7 本身只要求"有可见焦点指示器"，无尺寸量化。把 AAA 细则写进 AA 条目会造成 agent 对 2.4.7 的误判标准（对 AA 审计场景过度要求）。

**问题 2 — L120 "UI components: 3:1 contrast ratio" 挂在 1.4.3 Contrast (Minimum) 下**：组件/图形对比度 3:1 是 **1.4.11 Non-text Contrast（AA）** 的内容（正文 L132-135 已单列 1.4.11，此处重复且归属错误）。1.4.3 仅覆盖文本对比。

**问题 3 — L125 "No horizontal scrolling at 200% zoom (1280px width)" 挂在 1.4.4 Resize Text 下**：横向滚动的测试口径属于 **1.4.10 Reflow**（320px/200% 缩放无横向滚动）。1.4.4 自身只要求 200% 缩放无内容/功能损失。L127-130 已单列 1.4.10，此处同样重复归属。

三处均为"把相邻准则的细则抄进上一准则"的复制粘贴型错误，不影响整体结论（对应准则在正文别处均正确存在），但作为"审计他人可访问性"的技能，自身把 SC 编号与内容对应错，会被被审计方抓住把柄，建议修正。

### 4.3 4.1.1 Parsing 未标注 WCAG 2.2 移除状态（🟡）

L296-299 将 **4.1.1 Parsing (A)** 列为活跃的 critical criterion 并要求用 W3C Validator 检查。但 WCAG 2.2（本技能默认版本，L38）**已将该 SC 移除**并标记为 "Obsolete and removed"——W3C 官方立场是：现代浏览器/AT 依赖 accessibility tree 而非直接解析 HTML，4.1.1 所覆盖问题已由 1.3.1/4.1.2 接管，HTML 内容下视为恒满足。本技能默认审计 WCAG 2.2，却把已移除的标准列为必查关键项，存在事实滞后。**缓解因素**：该检查本身无害（HTML 校验仍有价值），且 4.1.1 在 2.0/2.1 中仍有效，而技能声明支持 2.1/2.2 双版本。建议在条目内加一行注释说明 2.2 状态（§13-🟡-2）。

### 4.4 关键成功准则覆盖缺口（🟡）

标题自称 "Critical Success Criteria (Level A & AA)"，但对照 WCAG 2.2 全部 A/AA 级 SC（约 50 条），以下 **13 条 A/AA 级准则完全未列入**：1.2.1 Audio-only/Video-only (A)、1.2.2 Captions (A)、1.2.3 Audio Description (A)、1.2.4 Captions Live (AA)、1.2.5 Audio Description (AA)（整个 1.2 指南缺席）、1.3.3 Sensory Characteristics (A)、1.3.4 Orientation (AA)、1.3.5 Identify Input Purpose (AA)、1.4.2 Audio Control (A)、1.4.5 Images of Text (AA)、1.4.13 Content on Hover (AA)、2.2.1 Timing Adjustable (A)、2.2.2 Pause Stop Hide (A)、2.3.1 Three Flashes (A)。

**缓解因素**：其中 1.2.x 在手动测试清单中有部分覆盖（L404-405 "Check video captions/transcripts / audio descriptions"），1.4.13/2.2.1 等属低频项。但作为"审计"技能，一个未列出的 SC 意味着 agent 几乎不可能主动去查——对完整审计而言这是实质性覆盖缺口。至少应补入 1.2.2、1.2.3、1.4.5、2.2.2 四条高频项。

### 4.5 跨文件一致性（通过项）

- 报告模板 "Estimated Remediation Effort: Quick Fixes (1-2 weeks) / Medium (1-2 months) / Major (3+ months)"（L476-479）与 prioritized-remediation-plan.md 的三阶段时限（Phase 1 1-2 周 / Phase 2 1-2 月 / Phase 3 3+ 月）完全一致，且与 SCORING OUT-02 的口径一致 ✅。
- L372 "Automated tools catch ~30-40% of issues" 与 methodology-notes.md L7 一致 ✅（W3C/WebAIM 公认区间）。
- version.md "1.0 - Initial release (WCAG 2.2 compliant)" 与正文默认 2.2 一致 ✅。
- next-steps.md L26 "Stay updated on WCAG 2.2 and WCAG 3 working drafts" 与 L10 的 WCAG 3 定位一致 ✅。
- prioritized-remediation-plan.md Phase 1 工时核算：40+8+16+4+12=**80 小时**，与 "~80 hours (2 weeks)" 自洽 ✅。
- 无自相矛盾的默认值：AA 默认（L35、SCORING SCOPE-01、methodology-notes L3）三处一致；2.2 默认（L38、SCORING SCOPE-01）两处一致。

### 4.6 内部命名一致性（🟢）

"Reference Files" 节（L484-497）显示名 `Wcag 2 2 New Success Criteria Summary 2023`（大驼峰+空格）与实际文件名 `wcag-2-2-new-success-criteria-summary-2023.md` 不一致——链接可解析，但显示名风格与其余 12 条（正常标题大小写）不统一，纯视觉问题。

---

## 5. 参考文件逐一分析（13 个，全部全文精读）

### 5.1 `references/accessibility-statement-recommendations.md`（17 行）

单节模板：一段承诺性文本 + 代码围栏内的声明模板（合规状态 "WCAG 2.2 Level AA Partial Conformance (in progress...)" + 反馈渠道 + 日期）。质量良好：声明结构符合 EAA/ADA 实务惯例（承诺-状态-反馈-日期四要素齐全），与 SCORING OUT-03 的 "accessibility statement recommendation" 要求精确对应。占位符 `[Company]`/`[email/form]`/`[date]` 是模板预期形态。无语法问题。

### 5.2 `references/best-practices.md`（13 行）

10 条实务准则，每条一句话。与正文内容呼应良好：#4 "Proper HTML is 80% of accessibility"（业界流传比例，非官方数字，措辞可接受）、#9 与正文 L10 的 WCAG 3 定位一致。无需修复。可作为 agent 报告的建议附录直接引用。

### 5.3 `references/common-quick-wins.md`（12 行）

7 条快速修复，每条 = 修复项 + SC 编号 + 级别 + 工时估算（1-2 天到 30 分钟）。SC 编号核对：1.1.1 (A)、1.4.3 (AA)、2.4.7 (AA)、2.4.2 (A)、3.1.1 (A)、3.3.2 (A)、4.1.1 (A)——**与正文同款问题：4.1.1 在 WCAG 2.2 已移除**（§4.3）。工时估算合理（alt text 全站 1-2 天、lang 属性 30 分钟符合实务）。内容与正文关键准则清单（L96-311）重合度高——作为独立交付参考文件可接受，但若追求知识增量可删减为与正文互补的"按工时排序"视角，当前已是此视角，保留无妨。

### 5.4 `references/detailed-findings-by-principle.md`（78 行）

按 POUR 四原则分组的**发现模板**（供 agent 填充实际审计结果）。包含 3 个已填示例：1.1.1（产品图缺失 alt、图标按钮无 aria-label，含正反例代码）、1.4.3（对比度数值经验证准确，§4.1）、2.1.1（下拉菜单键盘不可达，含测试步骤与修复建议），另含 1.4.4 的 PASS 示例。每条发现的结构 = Severity/Impact/Issues Found（Location/Example/User Impact/Recommendation/Effort），与 SCORING PROC-07 要求的 "criterion reference + location + example + user impact + recommendation + effort" **逐字段对齐**——这是 SCORING 与参考文件设计对齐的最强证据。L38 `[Continue for all failed criteria...]`、L65/71/77 的 `[Continue...]` 占位符为模板预期形态。缺点：示例发现均为电子商务语境（product images/CTA/dropdown），未覆盖金融/政府等合规高发语境，属可选优化（🟢）。

### 5.5 `references/legal-disclaimer.md`（6 行）

3 句法律免责：审计提供合规指引但**不是法律评估**，法律核验需咨询无障碍律师/第三方认证。与 SCORING NEG-01（"does NOT claim legal compliance — legal disclaimer included"）精确对应。正文 L87 亦有 "legal obligations vary by jurisdiction" 呼应。这是"负面合规"设计链条的收口文件，质量良好。

### 5.6 `references/methodology-notes.md`（17 行）

结构化备注：Standard（WCAG 2.2/2.1, AA）、Method（自动化+手动）、Evaluator（AI agent 模拟无障碍专家）、Limitations（3 条：自动化仅覆盖 30-40%、需手动验证、需真实用户确认）、Scope（`[X pages]` 占位）。与 SCORING QA-01 的五个要素（standard/method/evaluator/limitations/scope with page count）**一一对应**。**语法问题：L16 有一个孤立的收尾代码围栏 ```（无配对开始围栏）**——Markdown 渲染会将其作为单行代码块处理，视觉上不干净（🟡）。L15 "**Version**: 1.0 / **Date**: [Date]" 的冒号风格与 references 其他文件一致。

### 5.7 `references/next-steps.md`（27 行）

4 阶段行动清单（立即/短期 1-3 月/长期 3-6 月/持续），全部为勾选式任务。阶段划分与 prioritized-remediation-plan.md 的三阶段互补不冲突（此文件是团队落地视角，彼文件是工程修复视角）。"Conduct user testing with people with disabilities" 与 version.md 的 "Remember" 段呼应。L19 "third-party certification (e.g., WebAIM)"——WebAIM 本身不是认证机构（是 WebAIM 培训/工具，认证通常指 IAAP CPWA/WAS 或 Trusted Tester），属轻微事实瑕疵（🟢，不影响主流程）。质量良好。

### 5.8 `references/prioritized-remediation-plan.md`（41 行）

三阶段修复计划。Phase 1 完整填充（5 项：alt text 40h / 对比度 8h / 下拉菜单键盘 16h / 焦点指示器 4h / 表单标签 12h，合计 80h 自洽），Phase 2/3 为 `[Continue...]` 占位。每项 = WCAG SC + 级别 + 工时 + 影响。与报告模板的 "Estimated Remediation Effort" 和 SCORING OUT-02 的阶段口径一致（§4.5）。作为模板合格；Phase 2/3 的占位符合"模板而非成品"定位。可选优化：给 Phase 2/3 也各留一条示例防止 agent 忽略占位结构（🟢）。

### 5.9 `references/resources.md`（25 行）

13 个外链分 4 组（WCAG 标准 5 / 测试工具 4 / 屏幕阅读器 3 / 培训 3）。链接核对：W3C WCAG 2.2/2.1 quickref、Understanding WCAG 2.2、ISO/IEC 40500:2025 新闻稿（w3.org/press-releases/2025/wcag22-iso-pas/）、WCAG 3 导览、Deque/WebAIM/Lighthouse/Contrast Checker、NVDA/JAWS/VoiceOver、WebAIM/Deque University/A11y Project——**全部为真实存在的权威链接**，无死链迹象，无钓鱼域。与正文 Step 2 工具清单（L360-364）一致。质量优秀。

### 5.10 `references/success-criteria-priority-matrix.md`（12 行）

P0-P4 五级优先级表（P0 A 级失败 → P4 AAA 改进），每级附法律属性与影响等级。逻辑清晰：P0-P3 均标注 "Legal requirement"（A 级与 AA 级在多数司法辖区均为法律义务），P4 为可选项。与报告模板的 Critical/Serious/Moderate/Minor 严重度体系是**两套并行维度**（优先级 vs 严重度），文件本身未说明二者如何映射——agent 需自行理解（P0≈Critical 等）。建议加一行映射说明（🟢）。内容无误。

### 5.11 `references/testing-tools-used.md`（19 行）

测试工具记录模板：自动化（axe DevTools 4.x **45 issues**、WAVE **38 issues**、Lighthouse **64/100**、W3C Validator **12 errors**）+ 手动（键盘/NVDA 2025.1/200% 缩放/320px/对比度分析器）+ 辅助技术清单。**风险点：示例数值已预填且未标注为占位**——agent 若直接套用模板会把这些编造的"实测数字"写进报告，破坏 evidence trail（SCORING CF-03 恰好在惩罚"无证据链的合规声明"）。建议加一行 "示例值，请替换为实际检测结果" 的显式标注（🟡）。工具版本号（NVDA 2025.1）符合时效。

### 5.12 `references/version.md`（6 行）

"1.0 - Initial release (WCAG 2.2 compliant)" + 一句 "Remember" 收尾（无障碍超越合规、需真实用户验证）。与 SKILL-SPEC §1.3 的"版本历史放正文尾部 Metadata 节"约定在形态上稍有出入（spec 允许非 frontmatter 的版本信息放 `## Metadata` 节，此处以独立 reference 文件承载——本语料惯例如此，且被 SKILL.md Reference Files 索引，可接受）。内容无问题。

### 5.13 `references/wcag-2-2-new-success-criteria-summary-2023.md`（16 行)

WCAG 2.2 新增 9 条 SC 摘要。**逐条核对级别**：2.4.11 Focus Not Obscured (Min) **AA** ✅、2.4.12 Focus Not Obscured (Enhanced) **AAA** ✅、2.4.13 Focus Appearance **AAA** ✅、2.5.7 Dragging Movements **AA** ✅、2.5.8 Target Size (Min) **AA** ✅、3.2.6 Consistent Help **A** ✅、3.3.7 Redundant Entry **A** ✅、3.3.8 Accessible Authentication (Min) **AA** ✅、3.3.9 Accessible Authentication (Enhanced) **AAA** ✅——**9/9 全部正确**，无一处级别误标。表述与正文 L198-199/L219-225/L260-290 完全一致（两处均正确），自洽性佳。末尾 "These are integrated into the main checklist above for 2.2 audits" 与正文关键准则清单对应属实。

**参考文件整体评价**: 13 个文件全部可用、无孤立文件、与正文和 SCORING 双向对应。体系完整度（声明/免责/方法论/工具/计划/后续/资源/优先级/版本）覆盖审计交付的每个侧面，是语料中参考文件矩阵最完整的技能之一。主要问题为 3 个 🟡（methodology 围栏、testing-tools 占位数字、4.1.1 在 common-quick-wins 中重复出现）与若干 🟢。

---

## 6. 语法格式

- **YAML 校验**: SCORING.yaml 通过 `yaml.safe_load` 解析（16 项 criteria + 3 项 critical_failures，字段结构 id/category/description/judge/check 完整，无重复 id，无类型错误）。SKILL.md frontmatter 解析正常。✅
- **Python 校验**: check.py 通过 `py_compile` 编译，无语法错误；导入链 `_shared/checker.py` 实际存在且含 `set_tool_log_path`/`set_agent_output`（签名匹配）。✅
- **Markdown 围栏配对**: methodology-notes.md L16 孤立 ```（§5.6，🟡）；SKILL.md L443 报告模板围栏开启、L480 关闭，配对正确。
- **双空行噪音**: SKILL.md 约 12 处（§3.4，🟢）。
- **链接**: resources.md 13 个外链格式规范（https，无裸链）；SKILL.md 内 13 个相对链接 `references/xxx.md` 全部可解析（相对路径符合 §3.3，无 `../` 跨技能引用）。✅
- **中英文/emoji 混排**: 一致使用 ✅❌🔴⚪⭐ 标记，风格统一。
- **占位符风格**: `[Date]`/`[X]`/`[Company]` 方括号风格全目录统一。✅
- **list 缩进**: SKILL.md 勾选清单 4 空格缩进一致；references 各文件编号列表统一。✅

---

## 7. 规范合规（SKILL-SPEC v1.0 十二项清单）

| # | 检查项 | 判定 | 依据 |
|---|--------|:----:|------|
| 1 | name：小写+连字符，≤64 字符，匹配目录名 | ✅ | `wcag-accessibility-audit`，与 `281-wcag-accessibility-audit/` 一致（§2.1） |
| 2 | description：第三人称，含 WHAT+WHEN+KEYWORDS，≤1024 字符 | ✅ | 479 字符，三要素齐全（§2.2） |
| 3 | description：无祈使/第一/第二人称开头 | ✅ | 名词短语开头，无 "Use this skill to..."（§2.2） |
| 4 | description：无跨技能路由嵌入 | ✅ | 无 "NOT for X, use Y"；跨技能协作放正文（§2.2） |
| 5 | description：至少一个触发信号短语 | ✅ | "Use when the user asks to..." 精确命中（§2.2） |
| 6 | frontmatter：无允许清单之外键 | ✅ | 仅 name+description（§2.3） |
| 7 | body：≤600 行 | ✅ | 497 行（§3.3） |
| 8 | body：含 workflow/process 节 | ✅ | Audit Procedure 4 步流程（§3.2） |
| 9 | body：含 output format 节 | ✅ | Report Structure 完整模板（§3.2） |
| 10 | body：含 scope/limitations 节 | ❌ | **正文无显式 Scope/Limitations 节**；仅正向触发列表 + references 内零散提及（§3.2） |
| 11 | body：无跨技能文件引用 | ✅ | 13 个引用均为目录内相对路径，L14 跨技能为 prose 引用（§6） |
| 12 | 目录：NNN-kebab-case，无空格大写 | ✅ | `281-wcag-accessibility-audit` |

**合规结论: 12 项中 11 项通过，1 项不达标（第 10 项 Scope/Limitations）**。该缺口与 043-nielsen-heuristics-audit 的既有审查结论同源（同批次技能的共性问题），修复成本低（一节 5-10 行，§13-🔴-1）。

---

## 8. 人机感

**强项**:

1. **流程即节奏**: 时间预算（15/20/60-90/30 分钟）让"开始审计"变成一个可排程的动作；子测试的时间分配暗示了投入权重（手动测试中键盘 15min > 屏幕阅读器 20min > 表单 15min），符合实务重心。
2. **检查项全部动词化、可勾选**: "Navigate entire site with Tab key only"、"No keyboard traps (can always navigate away)" 这类指令无歧义，agent 或人类执行者都不需要二次解释。
3. **示例密度高**: 每条成功准则几乎都有正反例（`<img src="product.jpg">` vs 带 alt 版本、`#999999` vs `#595959`、"Shake to undo → has undo button"），抽象标准被转译成可操作样本。
4. **安全声明位置合理**: Security Notice（L315-329）紧接在外部输入定义（L29-38）之后，agent 读取时"输入 → 信任边界"的因果链清晰。
5. **报告模板可整段复制**: 代码围栏内的模板（L443-480）是交付物蓝图，agent 填充即可，格式漂移风险低。

**弱项**:

1. **物理工具依赖未做兜底声明**（🟡，最重要的人机感问题）: Step 2/3 大量指令假设 agent 能操作浏览器扩展（axe/WAVE）、屏幕阅读器（NVDA/JAWS/VoiceOver）、实体键盘测试。但本技能的执行环境（SkillIF agent + WebFetch/Read 工具）无法物理运行这些工具。技能没有一条"当工具不可用时的行为准则"（如实声明未测、以代码审查替代实测、或标注 simulated）。**后果**: 诚实的 agent 无路可走，不诚实的 agent 会编造测试结果——而 SCORING PROC-01~06 恰好按"是否报告了这些测试"评分，CF-01 只惩罚"全自动无手动证据"，不惩罚"声称做了其实没做"。这是评测设计与技能内容之间最值得警惕的缝隙（§10.4 详述）。
2. **"unplug mouse"（L348）**: 对人类审计员是常识提示，对 agent 是无意义指令——微瑕，但暴露出文本是"人类审计 SOP"改写而来，未针对 agent 执行体做适配。
3. **Knowledge-delta 冗余**: L46-77 的 4 POUR 原则与指南列表、L83-87 的合规等级定义，对 LLM 是常识（spec §3.4 反对解释模型已知概念）。约 30 行低增量内容，可压缩为一句定位。

**总体**: 作为"给 agent 用的审计作业指导书"人机感良好（指令可执行、模板可复制、安全边界明确），主要缺口是未处理"agent 无法物理操作工具"这一执行现实。

---

## 9. 可执行性

**逐步骤可执行性评估**:

- **Step 1 准备（15min）**: 输入定义清晰（6 项，1 必填），scope 选择标准明确（10-15 页或关键模板，含 5 类页面）。可执行 ✅。**缺口**: 未显式要求 agent "获取目标页面内容"（WebFetch/Read）——L341 只说 "Review urls_or_screenshots"，而 SCORING PROC-08 假设存在 "fetched page content"。对无浏览器的 agent，"Review URLs" 唯一合理路径就是 fetch，建议显式写出（🟡）。
- **Step 2 自动化测试（20min）**: 工具清单具体（axe/WAVE/Lighthouse/W3C/Stark），文档字段明确（violations/SC/affected/severity）。**执行现实**: 无浏览器时 axe 等不可用；技能未提供替代（如静态 HTML 分析、axe-core 无法注入时的降级策略）。可执行性中等（🟡）。
- **Step 3 手动测试（60-90min）**: 6 个子测试全部勾选化，验收标准内嵌（如 320px 无横向滚动）。对人类的可执行性满分；对 agent 依赖 §8 所述兜底声明。其中 "Test with text spacing adjustments"（L403）对应 1.4.12 的具体参数（1.5×/2×/0.12×/0.16×，L139-142），参数齐全可执行 ✅。
- **Step 4 报告（30min）**: 模板字段与 SCORING OUT-01/02/03 对齐，直接产出合规交付物。可执行性最强的一步 ✅。

**可执行性总评**: 流程链完整、验收标准量化（对比度比值、像素宽度、时间预算、工时估算）、模板可直接产出。扣分项集中在"工具不可用时的降级路径缺失"与"页面获取步骤未显式化"。**结论: 结构可执行性 9/10，环境适配可执行性 6/10，综合 7.5/10**。

---

## 10. SCORING 交叉参考

### 10.1 准则与 SKILL.md 逐条追溯（16/16 全覆盖）

| 准则 | 判定 | 溯源 |
|------|:----:|------|
| SCOPE-01 识别审计任务 + 收集输入（interface_description 必填、AA/2.2 默认） | ✅ | Inputs Required L29-38（REQUIRED/默认值完全对应） |
| SCOPE-02 仅用 2.1/2.2，不用 WCAG 3 作为合规目标 | ✅ | L10 "should not be used as a conformance target" + Inputs L38 |
| SCOPE-03 范围定义（首页/导航/表单/动态内容/媒体） | ✅ | Step 1 第 3 条 L352-353 |
| PROC-01 自动化工具 + 违规记录 | ✅ | Step 2 L359-372 |
| PROC-02 键盘测试六要素 | ✅ | 键盘勾选清单 L378-385 |
| PROC-03 屏幕阅读器测试六要素 | ✅ | 屏幕阅读器清单 L387-396 |
| PROC-04 视觉/内容测试（200%/320px/对比度/非颜色独传/文本间距/字幕） | ✅ | 视觉清单 L398-405（六项全部命中） |
| PROC-05 表单测试四要素 | ✅ | 表单清单 L407-414 |
| PROC-06 语义 HTML + ARIA 测试 | ✅ | 两清单 L416-432 |
| PROC-07 发现结构（SC 编号/位置/示例/影响/建议/工时） | ✅ | detailed-findings-by-principle.md 字段逐一对应（§5.4） |
| PROC-08 不可信输入处理 | ✅ | Security Notice L315-329 |
| OUT-01 各等级合规状态/严重度/TOP3/工作量 | ✅ | 报告模板 Executive Summary L458-479 |
| OUT-02 三阶段修复计划（1-2 周/1-2 月/3+ 月） | ✅ | prioritized-remediation-plan.md（§4.5 口径一致） |
| OUT-03 工具与方法记录 + 无障碍声明建议 | ✅ | testing-tools-used.md + accessibility-statement-recommendations.md |
| NEG-01 不依赖自动化/不声称法律合规 | ✅ | L372 "30-40%" + legal-disclaimer.md |
| QA-01 方法论五要素 | ✅ | methodology-notes.md（standard/method/evaluator/limitations/scope 全含） |

**16/16 全部可溯源，无孤儿准则、无不可测准则**。这是本技能评测设计质量的最高分项。

### 10.2 critical_failures 交叉核验

- **CF-01**（仅自动化、无手动证据 → cap 0）: 与 NEG-01 同源互补。⚠️ 但如前所述（§8.1），CF-01 只拦截"没有手动测试内容"，不拦截"声称做了手动测试"，无法区分"真实执行"与"编造报告"——这是 llm-judge 体系的固有局限，非本技能独有问题，但值得在运行评测时留意提示词措辞。
- **CF-02**（执行被取页面内指令 → cap 0）: 与 PROC-08/Security Notice 精确对应。✅
- **CF-03**（无页面/失败准则证据链的合规声明 → cap 0）: 与 OUT-01/QA-01 呼应。✅

### 10.3 check.py 与 SCORING 一致性

- 准则总数 16 = SCORING criteria 16 = `total_items: 16`，三者一致 ✅。
- check.py docstring "Run all 0 script checks" 与实现一致（所有 16 项 judge: llm，result 恒为空 dict）✅——纯 llm-judge 设计成立，SCORING 无 script 项，不存在"脚本应查未查"的失配。
- **潜在 bug（🟡）**: `check()` 内部（check.py L17-18）调用 `set_agent_output(agent_output)` 时传入的是**路径字符串**，而 `main()`（L48-50）已先将文件内容读入并设置——`check()` 的调用**覆盖**了内容，`_agent_output` 最终存的是路径而非文本。当前因无 script 检查而无实际影响，但任何未来的 `output_contains` 脚本检查都会静默失败。建议在 `check()` 内读取文件内容，或删除 `check()` 中的重复设置。
- check.py L23-35 的注释块按 SCOPE/PROCESS/OUTPUT/NEGATIVE/QA 分组标注 llm judge，与 SCORING category 划分一一对应，结构清晰 ✅。

### 10.4 评测设计缝隙（供运行方参考，非缺陷）

SCORING 16 项全部依赖 "Agent's report/tool log" 中的**声明性证据**（"Does the agent **report**..."）。由于 SKILL.md 要求 6 类手动测试且全部走 llm-judge，评测实质在测"报告完整度"而非"审计真实性"。在 prompt-injection 对照集（CF-02）之外，可考虑增加一条针对"工具不可用时的如实声明"的负向或 QA 项——这是本技能评测闭环上唯一未封的口子。

---

## 11. Skip（跳过/不适用项）

本审查遵循"全文件、零跳过"原则，以下为**主动判定为不适用**而略去审查的内容，逐一说明理由：

- **11.1 无旧 REVIEW.md / stub**: 本目录为首次审查（Glob 未发现既有 REVIEW.md），无需"旧 stub 对比"环节（043 号审查包含此项）。
- **11.2 无 LICENSE/README/scripts/ 等附属物**: 目录仅含 SKILL.md + SCORING.yaml + check.py + references/，无其他文件类型可审。
- **11.3 二进制/图片/大文件**: 目录内无二进制资源，无图片引用，无需渲染检查。
- **11.4 跨技能路由检查的范围界定**: 正文 L14 提及 "Nielsen Heuristics Audit" 与 "Don Norman Principles"（043 与 071 号技能），按 SKILL-SPEC §3.3 属合法的 prose 引用，不展开核验对方技能内容（其合规性由各自 REVIEW 负责）。
- **11.5 外链的实时可达性**: resources.md 的 13 个链接按域名/路径真实性核验（全部为 W3C/Deque/WebAIM/Google/Apple/Freedom Scientific 的权威地址），未做逐链 HTTP 探测（网络环境不稳定时探测结果不可靠，且 W3C 新闻稿链接 2025 年发布、时效内）。如需要可在评测前抽查。
- **11.6 AAA 级成功准则的逐条内容核对**: 技能将 2.4.12/2.4.13/3.3.9 等 AAA 项仅在 references 中列出级别，正文不展开 AAA 细则——按技能定位（AA 为默认目标）合理，AAA 细则内容未逐条对照官方文本，视为范围外。
- **11.7 SCORING 的 judge 提示词效果评估**: 16 项全部为 llm-judge，其判定稳定性属于运行期（runner）问题而非本技能文件问题，不在本次审查范围。

---

## 12. 综合评分（八维）

### 12.1 评分维度定义

| 维度 | 权重 | 含义 |
|------|:----:|------|
| D1 内容准确性 | 15% | WCAG 事实、数值、级别标注与官方文本的一致性 |
| D2 结构组织 | 12% | 章节骨架、信息层级、流程编排 |
| D3 规范合规 | 15% | SKILL-SPEC 12 项清单达成度 |
| D4 可执行性 | 13% | 指令能否被 agent/人类无歧义执行 |
| D5 参考文件质量 | 12% | references/ 的完整性、准确性、与正文协同 |
| D6 人机感 | 10% | 阅读体验、节奏、示例、安全边界 |
| D7 评测对齐 | 15% | SCORING 可追溯性、critical failure 有效性 |
| D8 维护性 | 8% | 版本管理、占位符规范、扩展空间 |

### 12.2 分维评分与依据

**D1 内容准确性 — 8.5/10**: 主体事实全部核对无误（ISO 状态、9 条新 SC 级别、对比度数值、POUR 指南编号、3.3.4 三要素）；扣分在 4.1.1 未标注 2.2 移除状态（§4.3）与 3 处 SC 细节归属串线（§4.2）——对一个"纠正他人可访问性错误"的技能，自身 4 处标准细节瑕疵是实质扣分。

**D2 结构组织 — 9.0/10**: 层次分明（原则→准则→检查→报告），时间预算贯穿，模板独立围栏；扣分在 12 处双空行噪音与 "Reference Files" 显示名不一致。

**D3 规范合规 — 8.0/10**: 12 项清单 11 过 1 挂（Scope/Limitations 缺失）；该缺口的缓解因素（references 内有局限性、NEG-01 覆盖"不声称法律合规"）使其影响小于 043 号的同款问题，但清单是二分判定，仍记不达标。

**D4 可执行性 — 7.5/10**: 验收标准量化、清单可勾选、模板可复制（结构层面接近满分）；扣分在物理工具依赖无兜底声明（§8.1）、页面获取步骤未显式化（§9）、"unplug mouse"类人类向指令。

**D5 参考文件质量 — 8.5/10**: 13 文件全部可用、SCORING 双向对应、9 条新 SC 级别 9/9 正确、资源链接权威；扣分在 methodology 孤立围栏、testing-tools 预填数字未标占位、common-quick-wins 复现 4.1.1 问题、priority matrix 缺严重度映射说明。

**D6 人机感 — 8.5/10**: 节奏感、示例密度、安全边界是标杆级；扣分在约 30 行知识冗余（POUR 定义/合规等级对 LLM 为常识）与工具可用性断裂感。

**D7 评测对齐 — 9.5/10**: 16/16 准则全部可溯源、3 CF 全部有效、check.py 注释分组与 category 一致、`total_items` 三重自洽——本语料最佳水平之一。扣 0.5 因 CF-01 与 PROC-01~06 之间存在"声称 vs 实际"缝隙（§10.4，体系性问题，非本技能专属）。

**D8 维护性 — 8.0/10**: 版本文件存在、占位符风格统一、无硬编码日期；扣分在无显式 Metadata 节（spec §1.3 建议形态）与 testing-tools 占位数字的误用风险。

### 12.3 加权汇总

| 维度 | 权重 | 得分 | 加权 |
|------|:----:|:----:|:----:|
| D1 内容准确性 | 15% | 8.5 | 1.28 |
| D2 结构组织 | 12% | 9.0 | 1.08 |
| D3 规范合规 | 15% | 8.0 | 1.20 |
| D4 可执行性 | 13% | 7.5 | 0.98 |
| D5 参考文件质量 | 12% | 8.5 | 1.02 |
| D6 人机感 | 10% | 8.5 | 0.85 |
| D7 评测对齐 | 15% | 9.5 | 1.43 |
| D8 维护性 | 8% | 8.0 | 0.64 |
| **合计** | 100% | — | **8.48 → 85/100** |

### 12.4 最终结论

**B+ (85/100)**。与 043 号同级技能（B+ 83）相比：评测对齐更强（043 仅 20 项中 1 项 script 检查、本技能 16 项全 llm 但溯源更完整）、参考文件矩阵更全；扣分项类型相似（同为 Scope/Limitations 缺失 + 物理工具假设）。定位语：**评测就绪度高于内容完善度**——SCORING 链已闭环可立即投用，内容层面的 4 处标准细节与 2 处执行环境适配建议在本批修复后（预计 2-3 小时工作量）可升至 A- 档。

### 12.5 与 dossier 档案的关系

本审查未在 skill-dossier.md 中找到 281 号条目的独立评分记录（322 项逐项审查档案为 2026-08-05 完成，281 号如存在条目则以本 REVIEW 为准更新）。本次 B+ (85/100) 为首次深度审查结论，建议回写档案。

---

## 13. 修复建议

按 🔴（必须修，影响规范合规或评测正确性）→ 🟡（应当修，影响内容准确或执行质量）→ 🟢（建议修，排版/一致性）排序。每项附文件、行号与工作量估计。

### 🔴 必须修（1 项）

**🔴-1 补写 Scope / Limitations 必需节**（SKILL.md，建议插在 L87 Conformance Levels 之后或 L312 关键准则之后；约 15 分钟）
SKILL-SPEC §3.1 的 12 项清单唯一不达标项（§7 第 10 项）。建议内容（6 条负面声明即可达标）：
- 本技能不替代真实用户（残障用户）可用性测试；
- 本审计不构成法律意见（引 references/legal-disclaimer.md）；
- 无法物理操作浏览器/屏幕阅读器时，应如实标注未执行项或注明 simulated，不得编造测试结果；
- 不覆盖 AAA 级全量（默认 AA 目标）；
- 不对未提供的页面/截图作合规结论（呼应 CF-03）；
- 自动化测试结果（axe/WAVE/Lighthouse）仅作线索，不作合规判定依据（呼应 NEG-01）。

### 🟡 应当修（6 项）

**🟡-1 4.1.1 Parsing 标注 WCAG 2.2 移除状态**（SKILL.md L296-299 与 common-quick-wins.md L11；约 10 分钟）
加注释："(注：该 SC 已在 WCAG 2.2 移除，仅 2.0/2.1 审计仍需检查；2.2 审计下 HTML 校验作为最佳实践保留)"。消除 §4.3 的事实滞后。

**🟡-2 修正 3 处 SC 细节归属串线**（SKILL.md L120、L125、L195；约 15 分钟）
- L195 删去 "Minimum 2px"（2px 属 2.4.13 AAA，可作附注提及）；
- L120 的 "UI components: 3:1" 移至 1.4.11 条目或删除（1.4.11 已有完整内容）；
- L125 的 "No horizontal scrolling at 200% zoom (1280px width)" 移至 1.4.10 条目（L127-130 已含 320px 口径，可合并为 320px/200% 双口径）。

**🟡-3 Audit Procedure 增加"页面获取"与"工具不可用兜底"两步**（SKILL.md Step 1/Step 2 区域；约 20 分钟）
- Step 1 显式加入：获取目标页面内容（WebFetch/Read），全部视为 `<untrusted-content>`（与 Security Notice 联动，让 PROC-08 的执行路径显式化）；
- Step 2 加入降级策略：无浏览器扩展环境时，改用静态 HTML 分析 + 代码审查替代 axe/WAVE，并在报告中如实标注工具与实际检测方法（呼应 §8.1/§10.4 缝隙）。

**🟡-4 check.py 修复 set_agent_output 覆盖 bug**（check.py L17-18；约 10 分钟）
`check()` 内将 `agent_output` 路径参数直接传给 `set_agent_output`，覆盖了 `main()` 已写入的正文内容。建议在 `check()` 内读取文件内容再传入，或删除 `check()` 中的该行（保留 `set_tool_log_path`）。当前无 script 检查所以无实际危害，但属定时炸弹。

**🟡-5 methodology-notes.md 删除孤立代码围栏**（L16 的 ```；1 分钟）
去掉无配对开始标记的收尾围栏（§5.6）。

**🟡-6 关键准则清单补入高频遗漏项**（SKILL.md L90-312；约 30 分钟）
至少补入 1.2.2 Captions (A)、1.2.3 Audio Description (A)、1.4.5 Images of Text (AA)、2.2.2 Pause Stop Hide (A) 四条（含检查要点，风格同现有条目），回应 §4.4 的 13 条覆盖缺口。

### 🟢 建议修（5 项）

**🟢-1 清理 SKILL.md 约 12 处双空行**（全文件；5 分钟）——§3.4。

**🟢-2 "Reference Files" 显示名对齐文件名**（SKILL.md L497："Wcag 2 2 New Success Criteria Summary 2023" → "WCAG 2.2 New Success Criteria Summary"；1 分钟）——§4.6。

**🟢-3 testing-tools-used.md 标注示例值**（L4-7；2 分钟）——加一行 "示例值，请替换为本次实际检测结果"，防 agent 把 45/38/64/12 等编造数字写进报告（§5.11，直接降低 CF-03 风险）。

**🟢-4 success-criteria-priority-matrix.md 增加严重度映射说明**（L5-11 后加一行；2 分钟）——说明 P0≈Critical、P1≈Serious、P2≈Moderate、P3≈Minor 与报告模板严重度体系的对应关系（§5.10）。

**🟢-5 next-steps.md 修正 WebAIM 认证表述**（L19；1 分钟）——"third-party certification (e.g., WebAIM)" 改为 "third-party certification (e.g., IAAP WAS/CPACC or Trusted Tester)"，WebAIM 本身不颁发认证（§5.7）。

**修复优先级提示**: 🔴-1 + 🟡-4 + 🟢-3 三项对"评测正确性与诚实性"影响最大，建议先行；🟡-1/2/6 是内容准确性修复；🟢 项可在同一编辑轮次顺手完成。全部修复预计 2-3 小时，完成后本技能可达 A-（88-90/100）档。

---

## 附录 A. 审查执行记录

- **工具**: Glob（文件枚举）→ Read（16 文件全文）→ Bash（`yaml.safe_load` 解析 SCORING.yaml、`py_compile` 编译 check.py、`wc -l` 行数核对）→ WebSearch（4.1.1 移除状态官方确认）→ Read（_shared/SKILL-SPEC.md、_shared/checker.py、043 号 REVIEW.md 格式参照）。
- **行号基准**: 本 REVIEW 所有行号指 2026-08-06 审查当日文件内容；`wc -l` 与 Read 工具显示行数在尾部空行处有 ±1 差异（如 SKILL.md 497 vs Read 498），不影响任何引用定位。
- **外部核验项**: ① WCAG 2.2 于 2023-10-05 发布为 W3C Recommendation、2025-06 发布为 ISO/IEC 40500:2025；② SC 4.1.1 Parsing 在 WCAG 2.2 中被移除并标记 "Obsolete and removed"（W3C Understanding SC 4.1.1、TPGi 移除解读、W3C "What's New in WCAG 2.2" 页，2026-08-06 检索）；③ 9 条新增 SC 的级别标注对照 W3C "What's New in WCAG 2.2"；④ 对比度比值手工复算。
- **未发现事项**: 无孤儿文件、无缺失引用、无重复 criterion id、无 YAML/Python 语法错误、无禁止字段、无跨技能文件路径。
- **Sources（WebSearch 核验来源）**:
  - W3C Understanding SC 4.1.1 Parsing (Obsolete and removed): https://w3c.github.io/wcag/understanding/parsing.html
  - W3C What's New in WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
  - TPGi — Understanding the Removal of 4.1.1 Parsing in WCAG 2.2: https://www.tpgi.com/understanding-the-removal-of-4-1-1-parsing-in-wcag-2-2/
  - W3C WCAG 2 FAQ: https://www.w3.org/WAI/standards-guidelines/wcag/faq/

## 附录 B. 评分对照说明

- 本 REVIEW 八维评分（85/100, B+）与 043-nielsen-heuristics-audit（83/100, B+）保持同一标尺：两者同为"流程型审计技能、同批生成、同款 Scope 缺口"，043 因启发式定义 10/10 全对、本技能因评测对齐 16/16 更优而略高 2 分。
- 如运行方采用其他加权方案，单维得分（§12.2）可直接复用；D7（评测对齐 9.5）是本技能最具区分度的强项，建议在汇总时优先关注 D1/D4 的修复进展。

## 附录 C. 修订建议落地清单

| 优先级 | 编号 | 文件 | 工作量 |
|:------:|------|------|:------:|
| 🔴 | 13-1 | SKILL.md 新增 Scope/Limitations 节 | 15 min |
| 🟡 | 13-2 | SKILL.md L296-299 + common-quick-wins.md L11（4.1.1 注记） | 10 min |
| 🟡 | 13-3 | SKILL.md L120/L125/L195（SC 归属修正） | 15 min |
| 🟡 | 13-4 | SKILL.md Step 1/2（页面获取 + 工具降级） | 20 min |
| 🟡 | 13-5 | check.py L17-18（set_agent_output 覆盖） | 10 min |
| 🟡 | 13-6 | methodology-notes.md L16（孤立围栏） | 1 min |
| 🟡 | 13-7 | SKILL.md L90-312（补 4 条高频 SC） | 30 min |
| 🟢 | 13-8 | SKILL.md 双空行清理 | 5 min |
| 🟢 | 13-9 | SKILL.md L497 显示名对齐 | 1 min |
| 🟢 | 13-10 | testing-tools-used.md 示例值标注 | 2 min |
| 🟢 | 13-11 | success-criteria-priority-matrix.md 映射说明 | 2 min |
| 🟢 | 13-12 | next-steps.md L19 认证机构修正 | 1 min |

**总计**: 约 2 小时；🔴-1、🟡-5、🟢-10 优先（评测正确性与诚实性相关）。
