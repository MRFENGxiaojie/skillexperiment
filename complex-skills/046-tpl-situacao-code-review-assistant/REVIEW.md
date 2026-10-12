# REVIEW: 046-tpl-situacao-code-review-assistant

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: mindset — 系统性代码审查（PR/MR review，severity 分级评论 + 分层审查 + 路由表 + 质量门）
**审查范围**: SKILL.md、SCORING.yaml、check.py、REVIEW.md（旧桩）、_shared/SKILL-SPEC.md（基准）、skill-dossier.md（既往评级）、complex-skills-no-trigger/046 副本（附录 A 对照）
**总评**: 🟡 **B−**（73.75/100，8 维加权）— 可用，建议微调：description 模板残留误指域 + 缺 Scope 节为两大扣分项；内容本体与评测设计（19/19 全支撑）质量优秀

---

## 1. 目录清单

本节列出技能目录全部文件及审查状态。本技能为**单文件自包含设计**：无 references/、无 scripts/、无 templates/ 目录（与 045 等"导航壳"类技能形成鲜明对照）。

| # | 文件 | 行数 | 角色 | 审查状态 |
|---|------|:----:|------|:--------:|
| 1 | `SKILL.md` | 120 | 主入口（原则 + 路由表 + 清单 + DO NOT + 输出格式 + 质量门） | ✅ 全文审查 |
| 2 | `SCORING.yaml` | 170 | 评测标准（19 项 criteria + 2 项 critical_failures） | ✅ 全文审查 |
| 3 | `check.py` | 74 | 脚本检查实现（2 项 script judge） | ✅ 全文审查 |
| 4 | `REVIEW.md` | 5 | 旧版审查桩（2026-08-05，已废弃） | ✅ 已读，本次全面重写 |
| 基准 | `_shared/SKILL-SPEC.md` | 161 | 合规判定标准 v1.0 | ✅ 全文参照 |
| 对照 | `skill-dossier.md` | — | 既往评级档案（046 条目位于 L388-393） | ✅ 交叉核对 |
| 对照 | `complex-skills-no-trigger/046/…` | — | 无 trigger 实验副本（SKILL.md + SCORING + check.py） | ✅ 与 trigger 版逐行 diff |

**目录结构要点**：
- 目录名 `046-tpl-situacao-code-review-assistant`，符合 SKILL-SPEC §4 的 `NNN-kebab-case` 格式 ✅。
- **⚠️ 无 references/ 子目录**：SKILL.md body 内**零文件引用**（无 `references/`、无跨 skill `../` 路径），全部知识内联于单文件。这使本技能天然免疫 045 类"引用缺失文件"的断链问题（§4、§9），但也意味着 body 行数（115 行 body）超过 mindset 模式 ~50 行的目标线（见 §3.3 讨论）。
- check.py 依赖 `_shared/checker.py`（L10-16 相对导入）——该库文件存在且导出 `tool_log_contains`（L259）/`output_contains`（L339）/`set_tool_log_path`（L224）/`set_agent_output`（L333）四个被引函数 ✅，无悬空依赖。
- **🔴 对照发现（详见 §11、附录 A）**：`complex-skills-no-trigger/046` 副本的 SKILL.md 首条原则仍为破损状态（`Review the diff, not the author.**`，缺 `1. **` 前缀）——规范化修复**未同步**到 no-trigger 副本，029 等家族成员同型破损。

---

## 2. Frontmatter 审查

SKILL.md L1-4 为 frontmatter，仅含 `name` 和 `description` 两个字段。

### 2.1 name（L2）
- `tpl-situacao-code-review-assistant`：小写 + 连字符，26 字符 ≤64，与目录名 `046-tpl-situacao-code-review-assistant` 后缀完全匹配 ✅（SKILL-SPEC §1.1、§4）。
- 系列前缀 `tpl-situacao-` 表明其出自葡萄牙语情境模板包（见 §6.3 的系列来源说明），属有意保留。

### 2.2 description（L3）

原文（326 字符）：
```
Pack template (situacao/05-code-review-assistant.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is conducting or receiving code reviews — reviewing a Pull Request, Merge Request, or any proposed change for correctness, security, and quality.
```

逐项核验（对照 SKILL-SPEC §2.1-§2.6）：

- **🟠 前半句是模板元数据，不是 WHAT**："Pack template (situacao/05-code-review-assistant.md)" 描述的是**模板包的出处**（葡萄牙语 situacao 包的第 5 号文件），不是该技能"做什么"。按 SKILL-SPEC §1.3 的规定，这类模板出处元数据应移入 body 尾部的 `## Metadata` 节，而非占据 description 的 WHAT 位置。
- **🟠 通用模板残留误指域**："Guides the agent on situational tasks such as **debugging, security and refactoring**"——debugging/security/refactoring 三个领域与本技能（code review）**并不等同**。这是 tpl-situacao 系列模板包的包级通用描述被逐技能复制粘贴的残留（对比 029/030 的 description 前两句逐字相同，见 §11.5）。风险是实打实的：agent 做调试/安全/重构任务时可能被这句误导向加载本技能；反之，description 的首屏信息不告诉读者这是 code review。
- **🟠 空话残渣**："aligned with this context" 无信息量，是模板占位措辞。
- **✅ WHAT 的实质内容在后半句**：code review、PR/MR、正确性/安全/质量三方面——后半句是合格描述。
- **✅ WHEN / 触发信号**："Use when the user is conducting or receiving code reviews — reviewing a Pull Request, Merge Request, or any proposed change..."。以 "Use when the user" 开头，符合 SKILL-SPEC §2.4 允许的触发信号模板（"Use when the user..."）✅。
- **✅ KEYWORDS**：Pull Request、Merge Request、code review、correctness/security/quality 均为领域关键词。
- **✅ 长度**：326 字符 ≤1024（§1.1）。
- **✅ 人称**：整体第三人称，无 imperative/first/second-person 开头（§2.3）。
- **✅ 跨 skill 路由**：无 "NOT for X, use Y" 结构（§2.5）。

### 2.3 禁用字段检查（SKILL-SPEC §1.3）
- frontmatter 仅 name + description，无 metadata、version、license、tags 等任何禁用键 ✅。

**Frontmatter 小结**：结构合规（无禁用字段、人称、触发、长度全过），但 description 前半句为模板元数据 + 通用误指域残留，是**本技能第一大扣分项**（详见 §13.1 修复方案）。评级：6/10。

---

## 3. Body 结构

SKILL.md 共 120 行（L6-120 为 body，115 行），远低于 600 行硬上限（SKILL-SPEC §3.2）。

### 3.1 实际内容盘点

| 章节 | 行号 | 内容 | 评价 |
|------|------|------|------|
| H1 | L6 | `# SITUATION: Systematic Code Review`（系列模板风格标题） | ✅ 有意保留（§6.3） |
| 原则 1-6 | L8-22 | 审查流程六原则：diff 而非作者、分层审查、severity 分级、PR 大小、先看测试、验收标准 | ✅ 完整编号列表（首条已修复，见 §11.2） |
| ROUTING TABLE | L24-37 | 10 行决策表：场景 → 严重级别 → 动作 | ✅ 决策树形式符合 §3.4 |
| Review Checklist | L39-67 | 18 项清单（Correctness 5 + Security 4 + Performance 3 + Readability 3 + Tests 3） | ✅ 结构完整 |
| DO NOT | L69-77 | 7 条审查者行为禁令 | ✅ 反模式清单符合 §3.4 |
| OUTPUT FORMAT | L79-110 | 评论格式 + Review Summary 模板（两个代码块示例） | ✅ 见 3.2 |
| QUALITY GATES | L112-121 | 8 项交付质量门 | ✅ 与 DO NOT 呼应 |

### 3.2 必需三节核验（SKILL-SPEC §3.1）

| 必需节 | 状态 | 说明 |
|--------|:----:|------|
| Workflow / Process | ✅ 通过 | 原则 1-6（L8-22）+ ROUTING TABLE（L24-37）构成完整流程：理解变更 → 分层审查 → 严重性分流 → 路由决策。SKILL-SPEC §3.1 允许"any heading name"，编号原则即流程节。与 045 的"导航壳"（Steps 3-6 全委托）形成鲜明对比——本技能流程**全部内联**，agent 不读任何外部文件即知全流程 |
| Output Format | ✅ 通过 | `## OUTPUT FORMAT`（L79-110）：单条评论格式（L83-89）+ PR 汇总评论格式（L93-110，含 Overall/Highlights/Blocking/Suggestions 四段），具体可执行 |
| Scope / Limitations | ❌ 缺失 | 无"不做什么"、无"何时不用"节。`DO NOT`（L69-77）是**审查者行为**禁令（如不批不懂的 PR、不重复审查），不是**技能边界**声明（如"本技能不写代码、不替代 linter/CI、非 PR 场景不用"）。dossier 亦记录此缺失（L392），与本次核实一致 |

### 3.3 行数与模式匹配

- pattern 为 mindset（SCORING.yaml L2），目标线 ~50 行（§3.2）；本技能 body 115 行，为目标线的 2.3 倍。**超过目标线但远低于硬上限**——mindset 类内容密度高（路由表 + 18 项清单 + 8 项质量门），行数合理；若追求精简可把 Checklist 拆入 references/（属 P2 可选优化，见 §13.10-4）。
- 单文件内章节顺序合理：原则 → 路由 → 清单 → 禁令 → 输出 → 质量门，构成完整审查闭环，无跳步、无倒置（对照 045 的"STEP 0 顺序倒置"缺陷，本技能无此问题）。

**Body 小结**：结构完整度在 tpl-situacao 家族中属上乘——流程与输出格式两节齐备且内容扎实，唯一硬缺口是 Scope 节。评级：6.5/10。

---

## 4. 逻辑一致性

### 4.1 ✅ 主链路自洽（全文无 🔴 级断裂）

逐层核验内部一致性：

- **分类法 ↔ 路由表**：L12-16 定义 `[BLOCKING]`/`[SUGGESTION]`/`[QUESTION]`/`[NIT]` 四级，L28-37 路由表 10 行全部落在四级的子集内（BLOCKING ×5 行、SUGGESTION ×3 行、QUESTION ×1 行、BLOCKING-or-SUGGESTION ×1 行）——无路由结果落到未定义的标签上（`[SECURITY]` 除外，见 4.3）。
- **清单 ↔ 输出**：L41-67 清单五项（正确性/安全/性能/可读性/测试）与 OUTPUT FORMAT 的 Summary 结构（L96-109）兼容——Highlights 对应清单通过项、Blocking 对应失败项。
- **DO NOT ↔ QUALITY GATES**：L71（不批不懂的 PR）↔ L115（先读 PR 描述）、L72（linter 管的不评论）↔ L119（无 linter 级评论）、L77（CI 红不批）↔ L118（CI 绿基线）、L76（不堆叠）↔ 隐含"+1 文化"。两节互为镜像，无矛盾。
- **原则 ↔ 路由表**：L18（PR >400 行分节审）↔ L29（大函数拆解）同属"规模管理"主题，口径一致；L20（先看测试）↔ L28（无测试 → BLOCKING）闭环成立。
- **BLOCKING 闭环**：L13 定义"必须修复才能合并"，L114 要求每个 BLOCKING 带修复建议（↔ PROC-06），L120 要求作者回应 BLOCKING 后才批准（↔ QA-03）——从提出到关闭的链路完整。

### 4.2 🟠 SLA 口径不一致：24 小时 vs 24 个业务小时

- L73（DO NOT）："leave a review open more than **24 hours** without at minimum a comment"
- L117（QUALITY GATES）："Review submitted within SLA (default: **24 business hours**)"

同一约束两处口径不同。SCORING.yaml NEG-03（L130-136）跟随的是 L73 的"24 hours"——即评测基准与 QUALITY GATES 之间的锚点也不统一。业务小时 vs 自然小时在跨周末/节假日的评审中结果差异可达 3-4 倍。修复见 §13.4。

### 4.3 🟠 `[SECURITY]` 标签未入分类法

- L33 路由表："Security-sensitive code (auth, crypto, user input) | **Always block. Tag as `[SECURITY]`**"
- 但 L12-16 的严重性分类法只定义 4 个标签（BLOCKING/SUGGESTION/QUESTION/NIT），**没有 `[SECURITY]`**——它既不是第 5 级，也没说明它与 `[BLOCKING]` 的关系（是替代标签还是附加修饰？"Always block"暗示安全项必属 BLOCKING 级，但分类法未写这一归属规则）。agent 执行时可能产生两套标签（`[SECURITY]` 与 `[BLOCKING]` 并存或互斥）的不一致。SCORING PROC-04（L56-62）同样要求 "[SECURITY] tag"——评测与文本同缺定义。修复见 §13.3。

### 4.4 🟡 两处可讨论的判定阈值

- **L31 硬编码值双路由**："Hardcoded values (URLs, IDs, magic numbers) | `[BLOCKING]` **or** `[SUGGESTION]` depending on production risk"——一个路由两档输出，唯一的判定辅助是"Ask: what happens when this changes?"。缺一个具体化判据（如"直接威胁数据/凭据 → BLOCKING；纯样式常量 → SUGGESTION"）。不构成矛盾，但决策树的"树"部分可以更实。
- **L35/L36 的 BLOCKING 从严**：`console.log` 与注释掉的代码都判 `[BLOCKING]`（"never merge debug artifacts to main"）。对个人仓库这偏严（`console.log` 常见于开发中未清理），但对"合并门禁"语境是自洽的——与 L13 的 BLOCKING 定义（bugs、test failures）略不同源但可辩护，属风格选择而非逻辑错误。

### 4.5 ✅ 与 SCORING 的交叉一致性（19/19，详见 §10.3）

L8 ↔ OUT-01/CF-02、L10 ↔ PROC-01、L18 ↔ SCOPE-03、L20 ↔ PROC-02、L22 ↔ PROC-05、L28 ↔ PROC-04、L33 ↔ PROC-04、L72 ↔ OUT-04、L73 ↔ NEG-03、L114 ↔ PROC-06、L118 ↔ QA-01、L120 ↔ QA-03、L121 ↔ QA-02——技能文本与评测标准**逐项互证**，无"评分标准先于技能定义"的倒挂（对照 045 的 SCOPE-03 倒挂，见 045 REVIEW §10.3）。

**逻辑一致性小结**：无 🔴；2 处 🟠（SLA 口径、SECURITY 标签）+ 2 处 🟡（阈值细化）。评分：7.5/10。

---

## 5. 参考文件审查

### 5.1 零 references 的自包含设计

本技能无 references/ 目录，SKILL.md body 内零文件引用（L1-121 中无任何 `references/...`、`scripts/...`、`../other-skill/` 路径）。这一设计带来：

- ✅ **无悬空引用风险**：不可能出现 045 的 html-templates 缺失断链（045 REVIEW §4.1）、076 类"引用文件不存在"的问题。
- ✅ **合规加分**：SKILL-SPEC §3.3"使用相对路径、禁止跨 skill 引用"——零引用天然全绿。
- ⚠️ **代价**：全部内容内联使 body 达 115 行（mindset 目标 ~50 行，§3.3）。对 mindset 类技能，这属于"以行数换自包含"的可接受取舍，且 115 行仍远低于 600 行硬限。

### 5.2 check.py 的 _shared 依赖核验

- check.py L10-11：`sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))`——相对导入 `_shared/checker.py`，该文件存在（`D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py`）✅。
- 被引用的四个函数均已核实存在：`set_tool_log_path`（L224）、`tool_log_contains`（L259）、`set_agent_output`（L333）、`output_contains`（L339）✅。
- 无其他文件依赖（不读 SCORING.yaml、不读 SKILL.md）。

**参考文件小结**：单文件自包含 + 唯一外部依赖（共享库）存在且函数齐全。评级：9/10（满分留白 1 分，因内联策略使 body 偏长，见 §3.3）。

---

## 6. 语法格式

### 6.1 拼写与病句

- 全文件英文拼写无错字、无病句。审查术语（PR/MR、off-by-one、race condition、N+1、authorization、OWASP）使用准确一致。
- 唯一病句级瑕疵在 description L3："Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context"——"aligned with this context"悬空修饰（与什么对齐？），系模板占位残渣（§2.2）。

### 6.2 Markdown 结构

- **编号列表**：L8-22 原则 1-6 编号完整连续（`1.`→`6.`），首条 `1. **Review the diff, not the author.**` 前缀完整——**dossier 记录的"首条编号破损"在 trigger 版已修复**（§11.2 详述，含 no-trigger 副本仍破损的对照发现）。
- **加粗配对**：全文件 44 处 `**`（22 对，偶数平衡），逐一抽查均为合法用法（原则句首、清单小节标题、DO NOT 强调、标签加粗），无杂散 `**` artifact——**dossier 记录的语法缺陷同样已修复**（§11.2）。
- **表格**：ROUTING TABLE（L26-37）对齐工整，列宽一致，无断行。
- **清单勾选**：Checklist（L42-67）与 QUALITY GATES（L114-121）统一使用 `- [ ]` 形式 ✅。
- **行尾**：CRLF 行尾（120 CR / 120 LF 一致）。抽样核查发现语料库混用：045 为 LF（0 CR）、029/001/046 为 CRLF——**非本技能特有缺陷**，属全库待统一项（P2，§13.10-3）。

### 6.3 ★ 葡萄牙语模板来源标记（有意保留，非缺陷）★

按项目指示与语料事实记录如下：

- **系列来源**：本技能属 `tpl-situacao` 模板系列，出自葡萄牙语情境模板包（"situacao" 即葡萄牙语 "situation"；description L3 中的 "Pack template (situacao/05-code-review-assistant.md)" 即该包第 5 号模板的原始引用）。同系列共 19 个（023、029、030、058、059、078、099、100、101、115、116、132、145、146、168、169、186、210 等，目录名保留葡语拼写如 documentacao-tecnica、setup-inicial-projeto）。
- **有意保留的语言元素**：① name 与目录名的 `tpl-situacao` 前缀；② description L3 的 "situacao/05-code-review-assistant.md" 路径引用；③ H1 的 `# SITUATION:` 标题惯例（英译保留）。**这些均判定为有意保留的系列印记，不按语言泄露/拼写错误处理**——与前几轮审查对 262/276 类"真葡语混入正文"的判定（dossier L872 等）不同，本技能正文无任何葡语 token 混入。
- **正文语言核验**：对 SKILL.md 全文件葡语词扫描（situacao/para/com/nao/uma/documentacao/qualidade/codigo 等），命中仅 L2/L3 的 "situacao" 两处；L6-L120 正文 100% 英文，无中英混杂、无葡英混杂。
- **结论**：本技能"葡萄牙语来源"合规标记为——✅ 有意保留（系列印记层），✅ 正文无泄露（语言纯净层）。description 中模板出处的**呈现位置**问题（应移入 body Metadata 节）已在 §2.2/§13.1 作为独立问题处理，与本标记不冲突。

### 6.4 排版与标点

- description 的 em-dash（"—"）用法正确；正文无全角/半角混用、无零宽字符、无 BOM（文件首字节非 EF BB BF）。
- 全文件无 emoji、无全大写喊叫（"DO NOT" 与 `[BLOCKING]` 均为功能性强调，见 §8.1）。

**语法格式小结**：干净规范；扣分项为 description 病句残渣与 CRLF 未统一（全库层面）。评级：8.5/10。

---

## 7. SKILL-SPEC 合规 12 项

逐项对照 SKILL-SPEC.md §5 的 Compliance Checklist（基准文件 L146-161）：

| # | 检查项 | 结果 | 依据 |
|---|--------|:----:|------|
| 1 | name：小写+连字符，≤64 字符，匹配目录 | ✅ | SKILL.md L2 vs 目录 `046-tpl-situacao-code-review-assistant` |
| 2 | description：第三人称，含 WHAT+WHEN+KEYWORDS，≤1024 字符 | ⚠️ | L3 全长 326 字符 ≤1024；WHEN/KEYWORDS/人称全过；**WHAT 前半句为模板元数据 + 误指 debugging/security/refactoring 域**（§2.2），严格判为部分不达标 |
| 3 | description：无 imperative/first/second-person 开头 | ✅ | 以 "Pack template..." 名词短语开头，第三人称（§2.2） |
| 4 | description：无跨 skill 路由 | ✅ | L3 无 "NOT for X, use Y" 结构 |
| 5 | description：至少一个触发信号短语 | ✅ | "Use when the user is conducting or receiving code reviews..."（L3） |
| 6 | frontmatter：无禁用键 | ✅ | 仅 name+description（L1-4），§1.3 禁用键全部未用 |
| 7 | body ≤600 行 | ✅ | 120 行 |
| 8 | body 有 workflow/process 节 | ✅ | 原则 1-6（L8-22）+ ROUTING TABLE（L24-37）构成完整流程（§3.2） |
| 9 | body 有 output format 节 | ✅ | `## OUTPUT FORMAT`（L79-110） |
| 10 | body 有 scope/limitations 节 | ❌ | 完全缺失（§3.2）；DO NOT（L69-77）是行为禁令而非技能边界声明 |
| 11 | body 无跨 skill 文件引用（../） | ✅ | 全文零文件引用（§5.1） |
| 12 | 目录 NNN-kebab-case，无空格大写 | ✅ | `046-tpl-situacao-code-review-assistant` |

**结果：10.5/12 通过（1 项硬缺失 + 1 项部分）**。若按"三必需节齐备"的门槛（§3.1），本技能差 Scope 一节不达标。dossier 判定（L392）"workflow 和 output format 存在但无 Scope 节"与本审查完全一致 ✅；本审查额外确认第 2 项（description WHAT 污染）为部分不达标。

---

## 8. 人机感

### 8.1 专业审查者语气（本技能最大优点之一）

- 全文直接、专业、克制：无 emoji、无夸张标点、无营销腔（对照 045 的 "gets meetings, progresses conversations, and closes rounds" 营销句，本技能零此类内容）。
- 大写强调全部是功能性用法：`[BLOCKING]`/`[SUGGESTION]` 等标签（L13-16）、"DO NOT"（L69-77）——均为指令语义而非情绪化喊叫。
- 术语密度高但面向 agent 恰当：OWASP、N+1、off-by-one、race condition 均未加解释——符合 SKILL-SPEC §3.4"知识增量而非冗余"（不对模型已懂的概念说教）。

### 8.2 用户尊重原则

- L8 "Review the diff, not the author"——把反馈指向代码而非人，是审查者人机感的核心原则，表述精准。
- L76 "add a '+1 on the above'"——社群协作礼貌机制写进 DO NOT，务实。
- L71 "ask questions until you do [understand]"——不装懂、诚实沟通。
- L74 "trust that the author fixed what was asked"——避免重复骚扰作者的体贴设计。

### 8.3 无受众混淆

- 全文为纯 agent 指令，无用户对话脚本、无表单式填空（对照 045 的 STEP 2 开场白脚本与 step-3 的 "Your X: [填空]" 双重受众问题，045 REVIEW §8.1）——本技能指令与话术边界清晰 ✅。
- OUTPUT FORMAT（L81-110）的示例是 agent 产出规范（给用户的评论怎么写），归属明确，无混用。

### 8.4 轻微死板面

- DO NOT 列表 7 条全部以 "DO NOT" 大写开头，语气偏命令式——对 agent 指令这是合理风格（并被评为务实），对阅读体验略机械；可接受，不入修复项。
- QUALITY GATES 的 "Review submitted within SLA (default: 24 business hours)"（L117）是组织流程语言，对个人使用场景略显官僚——不影响功能，与 4.2 的 SLA 口径问题合并处理即可。

**人机感小结**：全文最干净的一个维度——专业、克制、无填充、无营销、无受众混淆。评级：8/10（扣分仅为 8.4 的轻微死板与官僚措辞）。

---

## 9. 可执行性

按 agent 装载 SKILL.md 后的实际执行路径逐段推演：

1. **触发装载**：description（L3）触发词（code review / Pull Request / Merge Request）与任务匹配 → 装载成功。（⚠️ 但见 §2.2：若任务是 debugging/security/refactoring，agent 可能被 description 误载——这是**误触发风险**而非本步骤自身缺陷。）
2. **流程主线**：原则 1-6（L8-22）给出审查顺序（理解 → 分层 → 分流 → 规模 → 测试 → 验收）→ ROUTING TABLE（L26-37）提供遇到问题的即时决策 → Checklist（L41-67）提供核对维度 → DO NOT（L71-77）约束行为边界 → OUTPUT FORMAT（L81-110）规定产出形态 → QUALITY GATES（L114-121）验收。**闭环完整，无断点、无死代码、无缺失文件**——这是本技能可执行性最强的证据（对照 045：STEP 0 空转 + html-templates 断链，045 REVIEW §9）。
3. **每一步都可直接转化为动作**：所有指令均带具体值（400 行、40 行函数、24 小时）或具体标签（BLOCKING/SUGGESTION/...），无"视情况"式空指令。
4. **微小执行缺口**（均非阻断）：
   - **diff 获取方式未指明**：如何拿到 PR/MR 的 diff（`git diff`、`gh pr review`、浏览 workspace 文件）未写——依赖 agent 的工具常识。SCOPE-02（SCORING L15-21）要求 tool log 中出现 PR description / pull request 等痕迹，若 agent 用其他方式进入（如用户直接贴 diff 文本），该检查可能空过（§10.5）。
   - **PR description 缺失时的处理未定义**：L115 要求"PR description was read"，但若 PR 无 description 怎么办？无兜底指令（对照 L71 "ask questions until you do" 的精神，建议显式补一句）。
   - **`[SECURITY]` 归属不清**（§4.3）：执行到 L33 时 agent 需自行决定标签语义。
   - **OUTPUT FORMAT 只给了 `[BLOCKING]` 和 Suggestion 两个示例**（L84-89）：`[QUESTION]`/`[NIT]` 在分类法有定义（L15-16）但无输出示例——小缺口。
5. **可执行性风险评级：低**。本技能是 46 号段审查中少见的"开箱即跑"型：不依赖任何外部文件、无死分支、无倒置时序。

**结论**：自包含 + 闭环 + 无断链，唯一短板在四个微缺口与 description 的误触发风险。评级：8/10。

---

## 10. SCORING 交叉参考

SCORING.yaml（170 行）共 19 项 criteria（pattern: mindset, total_items: 19，L1-3 与 3+6+4+3+3=19 相符 ✅），其中 llm judge 17 项、script judge 2 项；check.py（74 行）实现了全部 2 项 script 检查。critical_failures 2 项（CF-01 L164-166、CF-02 L168-170）。

### 10.1 script 检查实现核对

| Criterion | SCORING.yaml | check.py | 实现 | 一致性 | 现实可达性 |
|-----------|:-----------:|:-------:|------|:------:|:----------:|
| SCOPE-02 PR 描述读取 | L15-21（fn: tool_log_contains, L20-21） | L35 | `tool_log_contains('PR description\|pull[_-]?request\|merge[_-]?request\|description\\.(md\|txt)')` | ✅ 逐字符一致 | 中高（依赖 agent 通过 Read/WebFetch 读 PR 描述或 diff 文本中出现关键词） |
| PROC-03 severity 标签输出 | L48-54（fn: output_contains, L52-53） | L40 | `output_contains('\\[BLOCKING\\]\\|\\[SUGGESTION\\]\\|\\[QUESTION\\]\\|\\[NIT\\]')` | ✅ 逐字符一致 | 高（OUTPUT FORMAT L84 强制 `[BLOCKING]` 前缀，只要 agent 按格式输出必命中） |

**一致性结论**：check.py 与 SCORING.yaml 完全对齐，无实现偏差 ✅。与 045 的对照（045 的 OUT-04 依赖缺失文件、QA-03 硬编码品牌色）不同，本技能两项 script 检查都建立在真实可达的行为上——**评测层无缺陷**。

### 10.2 check.py 实现质量

- L19-29 的 `check()` 对 agent_output 做"路径 vs 原文"判别（L22-29：`os.path.exists` + 捕获 OSError/ValueError 防 Windows 超长路径异常）——健壮性处理优于 no-trigger 副本（其直接 `set_agent_output(agent_output)`，见附录 A）。
- L31-51 按 SCORING 分组注释标注"llm judge（not checked here）"——脚本与 llm 的职责边界清晰，docstring（L20 "Run all 2 script checks"）与实际数量一致。
- main()（L55-71）读文件 → 传内容 → 输出 JSON，接口契约明确。
- 唯一小瑕疵：无单元测试/自测用例（可 P2 补，见 §13.10-5）。

### 10.3 llm judge 17 项与技能文本的支撑矩阵（全部有据）

| 组 | 项 | SCORING 行 | 技能文本支撑 |
|----|----|:----------:|--------------|
| SCOPE | 01 识别为 code review 且对码不对人 | L7-13 | L8（"Review the diff, not the author"）✅ |
| SCOPE | 03 大 PR（>400 行）分节审查 | L23-29 | L18（"A PR over 400 lines... review in sections"）✅ |
| PROC | 01 分层审查（理解→正确性→风格） | L32-38 | L10（"Review in layers... First/Second/Third pass"）✅ |
| PROC | 02 先看测试、缺测试为最重问题 | L40-46 | L20（"Check the tests first"）+ L28（路由表首行）✅ |
| PROC | 04 路由表应用 + [SECURITY] 标签 | L56-62 | L28-37（路由表全表）+ L33（[SECURITY]）✅（标签语义缺口见 §4.3） |
| PROC | 05 验收标准 + 人工验证路径 | L64-70 | L22（"Verify acceptance criteria... verify it manually"）✅ |
| PROC | 06 每个 BLOCKING 带修复建议 | L72-78 | L114（QUALITY GATES 首条）✅ |
| OUT | 01 反馈对码不对人、不确定用提问 | L82-87 | L8（"Use 'this function' not 'you wrote.' Frame feedback as questions"）✅ |
| OUT | 02 Summary 含总体结论/亮点/阻断/建议 | L89-95 | L93-110（OUTPUT FORMAT 的 Review Summary 四段模板）✅ |
| OUT | 03 清单五维全覆盖 | L97-103 | L41-67（Correctness/Security/Performance/Readability/Tests 18 项）✅ |
| OUT | 04 无 linter 级风格评论 | L105-111 | L72（"DO NOT request changes on style if the team has a linter"）✅ |
| NEG | 01 不盲批、CI 红不批 | L115-120 | L71 + L77（DO NOT 第 1/7 条）✅ |
| NEG | 02 不重审已处理项、不堆叠 | L122-128 | L74 + L76（DO NOT 第 4/6 条）✅ |
| NEG | 03 24h 内至少留一条评论 | L130-136 | L73（DO NOT 第 3 条）✅（口径冲突见 §4.2） |
| QA | 01 审查前确认 CI 绿基线 | L139-145 | L118（QUALITY GATES）✅ |
| QA | 02 安全/架构敏感变更要第二审阅人 | L147-153 | L121（QUALITY GATES 第 8 条）✅ |
| QA | 03 BLOCKING 回应后才批准 | L155-161 | L120（QUALITY GATES 第 7 条）✅ |

**17/17 全部有技能文本直接支撑**——这是本技能评测设计最出色之处：SCORING 不是从模板臆造，而是从 SKILL.md 内容逐条提炼（与此前 045 的 SCOPE-03 倒挂、046 家族部分成员的"评测期望无行为依据"形成对比）。

### 10.4 critical_failures 合理性

- **CF-01**（L164-166）：CI 红或未解决的安全阻断仍批准 → cap_to_0。与 L77/L33 双锚点对应，判定条件可操作 ✅。
- **CF-02**（L168-170）：对作者的人身攻击式反馈 → cap_to_0。与 L8 对应，"评审文化红线"定位准确 ✅。
- 两项均无"结构性必触发"风险（对照 045 的 CF-02 在模板缺失下必然触发，见 045 REVIEW §10.4）——在现实评测中归零只会发生在 agent 真违规时 ✅。

### 10.5 评测可达性边界（2 点提示，非缺陷）

- **SCOPE-02 的"读 PR 描述"痕迹依赖**：pattern（L20-21）要求 tool log 含 'PR description|pull[_-]?request|merge[_-]?request|description\.(md|txt)'。若评测工作区不提供真实 PR（用户直接粘贴 diff 文本），agent 可能没有任何读动作命中该 pattern——**该检查的结果更多取决于评测任务构造而非 agent 行为**。建议评测侧保证工作区含带 PR description 的仓库（P2，§13.10-6）。
- **PROC-03 的区分度**：output 含任一标签即过（L52-53），agent 只要按 OUTPUT FORMAT 正常输出必命中——该检查是"烟雾测试"而非"质量测试"，区分度靠 17 项 llm judge 承担。设计意图合理，无需改动。

**SCORING 小结**：19 项结构自洽、script/llm 分工清晰、check.py 无偏差、llm 项 17/17 有文本支撑、CF 无结构性触发——**评测层质量优秀**。评分（并入 §12 的"参考文件/自包含"维度考量）：9/10。

---

## 11. dossier 汇总

### 11.1 既往评级（skill-dossier.md L388-393）

> **046-tpl-situacao-code-review-assistant**
> - **逻辑**: 路由表、分层审查方法、blocking/non-blocking 分类法、清单和质量门一致；仅开头原则列表破损（同 029/030）。
> - **语法**: 同样杂散 `**` markdown artifact，其余干净。
> - **人机感**: 直接、专业审查者语气，务实 "DO NOT" 规则；无填充。
> - **合规**: Description 第三人称含触发；workflow 和 output format 存在但无 Scope 节；120 行 ≤600。
> - **总评**: 🟡 好实用内容，破损列表开头和缺 Scope 节反映其他 tpl-situacao 模板缺陷。

dossier 判定 🟡。旧 REVIEW.md 桩（2026-08-05）同判 🟡，并记 48/100、"B−"（其数值口径问题见 §12.3）。

### 11.2 本审查对既往记录的核实（trigger 版两项缺陷已修复）

| 既往记录 | 当前核实（trigger 版） | 结果 |
|----------|------------------------|:----:|
| "开头原则列表破损" | L8 首条为 `1. **Review the diff, not the author.**`——编号与加粗完整 | ✅ 已修复 |
| "杂散 `**` markdown artifact" | 全文件 44 处 `**` 偶数成对、逐处抽查均为合法 | ✅ 已修复 |
| "120 行 ≤600" | 当前 120 行（wc -l） | ✅ 记录准确 |
| "workflow 和 output format 存在但无 Scope 节" | §3.2 核验：流程节 ✅、输出节 ✅、Scope ❌ | ✅ 记录准确 |

即：dossier 与旧桩记录的缺陷在**触发版**已不成立（2026-08-05 的 tpl28/28 规范化修复覆盖了 trigger 副本）。

### 11.3 本审查相对 dossier 的新发现（delta）

| # | 新发现 | 级别 | 影响 |
|---|--------|:----:|------|
| 1 | **no-trigger 副本 L8 首条仍破损**（`Review the diff, not the author.**`，缺 `1. **` 前缀，加粗失衡）——tpl28/28 修复未同步到 no-trigger 集 | 🔴 | 无 trigger 实验组读到的是损坏指令：markdown 渲染下该行失去列表语义、`**` 不配对，且首条原则在正文中退化为孤行文本；029 的 no-trigger 副本（L8 同型破损）证明这是家族性未同步 |
| 2 | description 模板残留细节（"Pack template (situacao/05-code-review-assistant.md)" + 误指 debugging/security/refactoring + "aligned with this context" 空话） | 🟠 | dossier 只记"description 第三人称含触发"，未记 WHAT 污染与误指域；这是本技能实际扣分最大的单项 |
| 3 | `[SECURITY]` 标签未入分类法（L12-16 vs L33） | 🟠 | 执行歧义（§4.3） |
| 4 | SLA 口径冲突：L73 "24 hours" vs L117 "24 business hours" | 🟠 | 与 NEG-03（L130-136）的评测锚点也不一致（§4.2） |
| 5 | SCORING 19/19 全支撑（§10.3） | 🟢 正面 | dossier 未评估 SCORING 层；本审查确认评测设计与技能文本零倒挂 |
| 6 | 单文件自包含、零外部依赖（§5.1） | 🟢 正面 | 免疫 045 类断链缺陷 |

### 11.4 生态对照（同族技能在 dossier 中的记录）

- **029-tpl-situacao-deployment-devops / 030-tpl-situacao-setup-inicial-projeto**（dossier 记录同源"开头列表破损"）：已核实两技能 trigger 版 L8 首条完整（`1. **Every environment is cattle...**`）——家族修复在 trigger 版落实；但 029 的 no-trigger 副本 L8 破损依旧（§11.3-1 佐证）。
- **045-investor-pitch-deck-builder**（dossier L381-386，🟠）：同批审查对象，其"导航壳 + 引用缺失文件"与本技能"自包含 + 零引用"是同一语料的两个极端——对照阅读可直观看出本技能的相对优势。
- **023-tpl-situacao-documentacao-tecnica 等葡语名技能**：系列命名保留葡语拼写（§6.3），与本技能同属有意保留的系列印记。

### 11.5 结论

dossier 的 🟡 总评在方向上与本审查一致（"好实用内容 + 小缺陷"）；但 dossier 记录的两项具体缺陷（破损列表、杂散 `**`）已在 trigger 版修复，而**新的两级问题**（description 误指域、no-trigger 未同步）取代了它们的位置。综合评级保持 🟡（B−，73.75/100），数值依据见 §12。

---

## 12. 综合评分（8 维加权 + 等级）

### 12.1 评分模型

沿用本语料 13 节模板的权重口径：Body 结构完整度 20%、逻辑一致性 15%、参考文件质量 15%、SKILL-SPEC 合规 15% 为核心四维；Frontmatter 合规 10%、人机感 10%、可执行性 10% 次之；语法格式 5% 为最小维度。本技能无 references/ 目录，将第 4 维改标为"参考文件/自包含性"（以"零外部依赖、唯一共享库依赖存在且函数齐全"为评分对象）。

| # | 维度 | 权重 | 评分/10 | 加权 | 关键依据 |
|---|------|:----:|:------:|:----:|----------|
| 1 | Frontmatter 合规 | 10% | 6.0 | 0.60 | 结构合规、触发/人称/长度全过；description WHAT 为模板残留 + 误指域（§2.2） |
| 2 | Body 结构完整度 | 20% | 6.5 | 1.30 | 流程/输出两节齐备且闭环；**缺 Scope 节**（§3） |
| 3 | 逻辑一致性 | 15% | 7.5 | 1.125 | 主链路自洽、零 🔴；SLA 口径 + [SECURITY] 定义两处 🟠（§4） |
| 4 | 参考文件/自包含性 | 15% | 9.0 | 1.35 | 零 references、零悬空引用、_shared 依赖存在且函数齐全（§5） |
| 5 | 语法格式 | 5% | 8.5 | 0.425 | 拼写干净、markdown 平衡；description 病句残渣、CRLF 未统一（§6） |
| 6 | SKILL-SPEC 合规 | 15% | 6.5 | 0.975 | 10.5/12 通过；唯一硬缺失为 Scope 节（§7） |
| 7 | 人机感 | 10% | 8.0 | 0.80 | 专业克制、无 emoji/营销/受众混淆；轻微命令式（§8） |
| 8 | 可执行性 | 10% | 8.0 | 0.80 | 自包含闭环零断点；4 个微缺口 + 误触发风险（§9） |
| | **综合** | 100% | | **7.375** | **73.75 / 100** |

### 12.2 等级判定

| 等级 | 区间 | 含义 |
|:----:|:----:|------|
| A | ≥85 | 可用，无需修改 |
| B | 70-84 | 可用，建议微调 |
| C | 55-69 | 可用但有明显缺陷 |
| D | 40-54 | 需修复，修复后可用 |
| F | <40 | 需重写 |

**综合等级：B−（73.75/100）→ 🟡 可用，建议微调。**

对照旧 REVIEW 桩（5 行，2026-08-05）：旧桩记 "🟡 B− (48/100)"。**等级与色级完全一致**；数值 48/100 与 B− 标签自相矛盾（按本语料等级表，48 属 D 区间，D+ 是 045 的档位）——旧桩的 100 分制未校准。本审查以同口径（与 045 REVIEW 相同的 8 维加权模型）给出 73.75/100 = B−：**保留旧桩的 B− 等级结论，修正其数值标定**。与 dossier 的 🟡 也一致。

### 12.3 分数构成说明

- 给"Frontmatter"6/10 而非更低：误指域（debugging/security/refactoring）是真实路由风险，但 description 后半句（WHEN + KEYWORDS）质量高，且触发信号/人称/长度全合规——问题集中在前半句一处，可定点修复（§13.1）。
- 给"Body 完整度"6.5/10：只差 Scope 一节，其余六节全部在岗且相互咬合；若补上 Scope，该维可升至 8.5+。
- 给"可执行性"8/10 而非更高：四个微缺口（diff 获取、PR description 缺失兜底、[SECURITY] 语义、输出示例不全）都不阻断流程，但 description 误触发风险扣分较重。
- 若 §13 的 P0 两项（description 重写、Scope 补齐）+ P1 三项（no-trigger 同步、[SECURITY] 入分类法、SLA 统一）全部落地，预期重评可达 85+/100（A 级边缘）——本技能的内容基本面（路由表、清单、输出格式、质量门的品质）决定了它的上限显著高于 46 号段多数成员。

---

## 13. 修复建议（★重点★）

按优先级 P0（影响路由/合规硬项，不修则失分或误用）→ P1（重要，不修则失效或失分）→ P2（打磨）组织。所有行号引用以当前文件为准；修复需同时应用到 trigger 与 no-trigger 两个副本（P1-1 除外，其对象本就是 no-trigger 副本）。

### 13.1 P0-1 ★ 重写 description，消除模板残留与误指域 ★

**现状**：SKILL.md L3 的 description 前半句是 tpl-situacao 系列模板残留——"Pack template (situacao/05-code-review-assistant.md)"（模板元数据）+ "Guides the agent on situational tasks such as debugging, security and refactoring"（误指三个与 code review 无关的领域）+ "aligned with this context"（空话）（§2.2）。后果：① agent 做调试/安全/重构任务时可能被误导向加载本技能；② 触发匹配的首屏信息不含"code review"关键字之外的技能本体描述；③ SKILL-SPEC §1.3 明文规定非 frontmatter 元数据（如模板出处）应放 body 尾部 Metadata 节，当前写法违反该条精神。

**修复**（替换 L3 为如下文本，326 字符 → 约 330 字符，仍 ≤1024）：

```
description: "Systematic code review of Pull Requests and Merge Requests with severity-labeled comments: layered review (high-level understanding, correctness and logic, style), routing rules, checklists, and quality gates for correctness, security, performance, readability, and tests. Use when the user is conducting or receiving a code review — reviewing a Pull Request, Merge Request, or any proposed change for correctness, security, and quality."
```

- 保留原 WHEN 句（"Use when the user is conducting or receiving a code review..."）不动——它是整段里唯一完全合格的部分；
- WHAT 改为真实的技能本体（分层审查 + severity 标签 + 路由 + 清单 + 质量门）；
- 模板出处信息（situacao/05-code-review-assistant.md）移至 body 尾部新 `## Metadata` 节（与 §13.10-2 合并实施）。

**验收**：description 前三句不再出现 debugging/security/refactoring 与 "aligned with this context"；对 description 做意图匹配测试（debugging 任务不触发、code review 任务触发）。

### 13.2 P0-2 ★ 补 Scope/Limitations 节（SKILL-SPEC §3.1 硬项）★

**现状**：§7 合规 12 项第 10 项不达标——body 无 scope 节（§3.2）。`## DO NOT`（L69-77）是审查者行为禁令，不构成技能边界声明。

**修复**：在 `## DO NOT`（L69）之前插入一节（建议插在 Review Checklist 之后、DO NOT 之前，保持"正面流程 → 边界声明 → 禁令 → 输出"的递进）：

```
## SCOPE / LIMITATIONS

**What this skill does NOT do:**
- Does not write or rewrite the code under review — it reviews and suggests changes
- Does not replace linters, formatters, CI, or static analysis tools — those run first; this skill reviews what they cannot
- Does not make the merge decision — it flags `[BLOCKING]` issues and requests changes; the team and the author decide
- Does not review non-code artifacts (design docs, specs, tickets) unless they are part of the PR

**When NOT to use:**
- The user is authoring new code without a proposed change (use a coding or writing skill instead)
- The user wants a design-only review with no code or diff attached
- The user asks for a full-codebase audit outside a PR/MR context (no single change to evaluate)
```

**验收**：§7 合规 12 项全绿；SKILL-SPEC §3.1 三必需节齐备。

### 13.3 P1-1 ★ `[SECURITY]` 标签写入严重性分类法 ★

**现状**：L33 路由表要求 "Always block. Tag as `[SECURITY]`"，但 L12-16 分类法只有 4 个标签（§4.3）；SCORING PROC-04（L56-62）的判定词同样含 "[SECURITY] tag"，评测与文本同缺定义。

**修复**（L16 之后追加一条，或在 L13 的 BLOCKING 定义内补说明）：

```
   - `[SECURITY]` — modifier applied to blocking issues in auth, crypto, input handling, or other security-sensitive code. Always accompanies `[BLOCKING]`, never replaces it.
```

同时把 L33 的路由动作改为明确引用："Always block. Tag as `[BLOCKING]` + `[SECURITY]`."——一句话同时修复执行歧义与评测锚点（PROC-04 判词不变，仍检查 "[SECURITY]" 词痕）。

**验收**：分类法含 5 个标签且关系明确（4 个独立级 + 1 个修饰符）；按 L33 路由产出的评论标签与分类法一致。

### 13.4 P1-2 ★ 统一 SLA 口径（24 hours vs 24 business hours）★

**现状**：L73 "DO NOT leave a review open more than 24 hours" vs L117 "SLA (default: 24 business hours)"（§4.2）；SCORING NEG-03（L130-136）跟随 L73。

**修复**（三处对齐，建议以"业务小时"为准，因 L117 是 SLAs 的唯一正式定义处）：
- L73 改为 "more than **24 business hours**（跨周末/节假日按下一个工作日计算）"；
- L117 不变（已是业务小时）；
- SCORING.yaml NEG-03 的 description（L130-136）中的 "24 hours" 同步改为 "24 business hours"（保持评测锚点与文本一致）。

**验收**：全文 grep "24 hour" 仅剩业务小时口径一处或零处；NEG-03 判定词与 L73/L117 无冲突。

### 13.5 P1-3 ★ no-trigger 副本破损首条同步修复（家族性未同步）★

**现状**：`complex-skills-no-trigger/046-tpl-situacao-code-review-assistant/SKILL.md` L8 为 `Review the diff, not the author.** Keep all feedback...`——缺 `1. **` 前缀（§1、§11.3-1）。该行在 markdown 下失去列表语义（退化为正文段落）且 `**` 不配对（后续原则 2-6 仍编号，第 1 条游离在列表外）。029 的 no-trigger 副本（L8）同型破损——**tpl28/28 修复只覆盖 trigger 集**。

**修复**：
1. 修改 no-trigger 副本 L8，前缀补全为 `1. **Review the diff, not the author.**`（与 trigger 版逐字一致）；
2. 对 no-trigger 全集 28 个 tpl-situacao 成员（023/029/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210 等）批量核查首条编号与 `**` 平衡（`grep -c '\*\*'` 应为偶数；首行原则应含 `1. ` 前缀）；
3. 修复后用 diff 复核：no-trigger 副本与 trigger 副本除 description 触发句外逐字一致（当前 046 已满足该标准，见附录 A）。

**验收**：`diff <(trigger SKILL.md) <(no-trigger SKILL.md)` 仅显示 description 一行差异；no-trigger 副本首条原则渲染为编号列表。

### 13.6 P1-4 ★ 显式化 diff 获取与 PR description 缺失兜底 ★

**现状**：§9 的执行缺口——L8-22 全程未写"diff 从哪来"；L115 要求读 PR description 但未写"PR 无 description 怎么办"；SCOPE-02（SCORING L15-21）的 tool log 痕迹依赖评测任务构造（§10.5）。

**修复**（L6 的 H1 之后、原则 1 之前插入 2 行前置指令，或并入原则 1）：

```
0. **Establish the input.** Obtain the diff via `git diff` (local) or `gh pr review` / MR web view (remote), and read the PR description first; if the PR has no description, ask the author for intent before reviewing.
```

该行同时：① 给 SCOPE-02 的 tool log 检查一个自然入口（agent 会 Read/执行含 "pull request"/"PR description" 的指令）；② 兑现 L71 "ask questions until you do" 的精神；③ 修复后把 0-6 原则重新编号为 1-7（或编号策略保持 1-6，将本条并入原则 1——建议并入原则 1 以最小改动）。

**验收**：按文执行时 tool log 必然出现 PR description 相关读取痕迹；无 description 的 PR 有明确兜底动作。

### 13.7 P1-5 ★ OUTPUT FORMAT 补全 `[QUESTION]`/`[NIT]` 示例 ★

**现状**：分类法定义 4 标签（L12-16），OUTPUT FORMAT 只示例 `[BLOCKING]` + Suggestion（L84-89）与 Summary 四段（L93-110），`[QUESTION]`/`[NIT]` 无输出样例（§9 缺口 4）。

**修复**（在 L89 的代码块后追加）：

```
For questions and nits:

[QUESTION] What happens to the rate limiter when the Redis instance restarts?
[NIT] The variable `tmp2` could be `normalizedTotal` — author's discretion.
```

**验收**：分类法 4 个独立标签在 OUTPUT FORMAT 全部有样例；PROC-03 的区分度不受影响（任何标签命中即过）。

### 13.8 P1-6 ★ 评测层补丁：NEG-03 口径 + SCOPE-02 任务构造提示 ★

**现状**：SCORING.yaml NEG-03（L130-136）的 "24 hours" 与修复后的 L73 需要同步（§13.4 已含）；SCOPE-02（L15-21）依赖评测任务提供含 PR description 的工作区（§10.5）。

**修复**：
1. NEG-03 措辞同步（并入 13.4）；
2. SCOPE-02 的 description（L16-17）追加一句评测构造要求："The evaluation workspace should include a repository with a PR description file or metadata（保证 tool log 可产生匹配痕迹）"——把"评测可达性"责任从技能侧划到评测侧，避免误判。

**验收**：两项改动后，评测在"agent 照章办事"场景下不存在必然失败的检查项。

### 13.9 P2 打磨项（按性价比排序）

1. **路由表 L31 细化判定阈值**（§4.4）："Hardcoded values" 一行补示例判据——"secrets/credentials/URLs with production impact → `[BLOCKING]`; pure display constants → `[SUGGESTION]`"。一句话把双路由变成可决策树。
2. **body 尾部补 `## Metadata` 节**（SKILL-SPEC §1.3 建议做法）：承接 description 移除的模板出处——
   ```
   ## Metadata
   Template source: situacao/05-code-review-assistant.md (tpl-situacao series, Portuguese situational pack)
   ```
   与 13.1 的 description 重写配套实施。
3. **CRLF 统一**（§6.2）：046 为 CRLF，045 为 LF——语料库行尾混用。若全库批量统一，建议统一为 LF（git 友好）；单文件层面无需单独处理。
4. **Checklist 拆 references 的选项**（§3.3，可选）：115 行 body 超过 mindset 目标线 2.3 倍；若追求精简可将 Review Checklist（L41-67）移入 `references/review-checklist.md` 并在 body 保留引用与摘要——**注意：这是可选优化，当前自包含设计本身合理，不做也不扣分**。
5. **check.py 补自测**（§10.2）：为 check() 加 2-3 个 fixture 用例（空 tool log / 含关键词 tool log / 含标签输出），防止未来修改破坏与 SCORING.yaml 的一致性。
6. **SCOPE-02 评测构造提示**（已并入 13.8-2，此处不再重复）。
7. **DO NOT 语气微调**（§8.4，可选）：7 条 "DO NOT" 保留——命令式对 agent 是优点；不列为必改项。
8. **H1 标题保留**：`# SITUATION: Systematic Code Review`（L6）为系列惯例标题，**有意保留，不改**（§6.3）。

### 13.10 修复优先级总表

| 优先级 | 编号 | 修复项 | 对应问题 |
|:------:|:----:|--------|----------|
| P0 | 13.1 | 重写 description（去模板残留/误指域） | 2.2 误触发风险、7 合规第 2 项部分不达标 |
| P0 | 13.2 | 补 Scope/Limitations 节 | 3.2、7 合规第 10 项硬缺失 |
| P1 | 13.3 | [SECURITY] 标签入分类法 | 4.3 执行歧义、10.3 PROC-04 锚点 |
| P1 | 13.4 | SLA 统一（24h ↔ 24 business hours） | 4.2、10.3 NEG-03 |
| P1 | 13.5 | no-trigger 副本破损首条同步修复 | 11.3-1 家族性未同步 |
| P1 | 13.6 | diff 获取 + PR description 兜底 | 9 缺口 1-2、10.5 SCOPE-02 |
| P1 | 13.7 | OUTPUT FORMAT 补 QUESTION/NIT 示例 | 9 缺口 4 |
| P1 | 13.8 | 评测层 NEG-03/SCOPE-02 补丁 | 10.5 |
| P2 | 13.9 | 8 项打磨 | 4.4、6.2、6.4、8.4、10.2 |

### 13.11 修复完成判据

1. **P0 落地后**：description 首屏即"code review 技能本体"（无误指域）；SKILL-SPEC 12 项合规全绿；此时可重评，预期 Frontmatter 升至 8.5+、合规升至 9+、Body 升至 8.5+，总分约 85/100（A 级边缘）。
2. **P1 全部落地后**：执行路径零歧义（标签、SLA、diff 来源、无 description 兜底全有定义）；trigger 与 no-trigger 两副本逐字一致（description 触发句除外）；评测层无"照章办事必失败"项。
3. **P2 按性价比陆续实施**：语料库级统一（CRLF、Metadata 节惯例）建议与其他 tpl-situacao 成员批量执行，而非单技能孤改。

**一句话总结**：本技能是 tpl-situacao 家族中内容质量第一梯队的成员——路由表、清单、输出格式、质量门四件套全部在岗且互咬合，SCORING 19/19 全支撑，评测层零缺陷；扣分集中在 description 的模板残留（误指域）、缺 Scope 节、以及 no-trigger 副本的未同步破损。修完 P0+P1 五项即达 A 级候选。

---

## 附录 A：与 no-trigger 版本的差异

`complex-skills-no-trigger/046-tpl-situacao-code-review-assistant/` 与 trigger 版的逐行 diff 结果（已实测）：

| 文件 | 差异 | 性质 |
|------|------|------|
| SKILL.md L3（description） | no-trigger 版删去 "Use when the user is conducting or receiving code reviews — reviewing a Pull Request, Merge Request..." 触发句，仅剩 "Pack template (situacao/05-code-review-assistant.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context." | 实验设计（无 trigger 对照）；**但注意**：无触发句后 description 完全不含 "code review" 字样——WHAT 只剩模板残留，误指域问题在 no-trigger 版被放大（本审查 §2.2 的修复方案对两版都适用，no-trigger 版更需重写） |
| SKILL.md L8 | no-trigger 版为 `Review the diff, not the author.** Keep...`（缺 `1. **` 前缀） | 🔴 非实验设计，是修复未同步的破损（§13.5） |
| SKILL.md 其余 117 行 | 逐字一致（已 diff 核实） | — |
| SCORING.yaml | 完全相同（diff 无输出） | 两版评测口径一致 ✅ |
| check.py | trigger 版 L22-29 有 agent_output 路径/原文判别逻辑（含 OSError/ValueError 防护）；no-trigger 版直接 `set_agent_output(agent_output)` | 功能差异极小；建议以 trigger 版实现为准（更健壮，§10.2） |

**实验影响声明**：本审查的 12 项合规、逻辑、可执行性结论对两版均成立（body 仅 L8 一处差异）；但 no-trigger 版需先修 L8 破损，否则"无 trigger 实验"测到的是损坏指令，与 trigger 版的比较会被 markdown 解析差异污染。附录 B 的 SCORING 速查对两版相同。

## 附录 B：SCORING 19 项清单速查

| 组 | 项 | judge | 依赖的技能文本 | 本审查判定 |
|----|----|:-----:|----------------|:----------:|
| SCOPE | 01 任务识别/对码不对人 / 02 读 PR 描述 / 03 大 PR 分节审 | llm×2 + script×1 | L8 / L20 或 L115 / L18 | ✅ 支撑充分（02 的 tool log 痕迹依赖任务构造，§10.5） |
| PROC | 01 分层 / 02 先看测试 / 04 路由表+SECURITY / 05 验收 / 06 BLOCKING 带建议 | llm×5 | L10 / L20+L28 / L28-37 / L22 / L114 | ✅ 支撑充分（04 的 [SECURITY] 语义缺口，§13.3） |
| PROC | 03 severity 标签输出 | script×1 | L12-16 + L84 | ✅ 高可达、低区分度（烟雾测试定位） |
| OUT | 01 对码不对人 / 02 Summary 四段 / 03 清单五维 / 04 无 linter 级评论 | llm×4 | L8 / L93-110 / L41-67 / L72 | ✅ 支撑充分 |
| NEG | 01 不盲批+CI 红不批 / 02 不重审不堆叠 / 03 24h 内留评论 | llm×3 | L71+L77 / L74+L76 / L73 | ✅ 支撑充分（03 口径冲突，§13.4） |
| QA | 01 CI 绿基线 / 02 第二审阅人 / 03 BLOCKING 回应后批准 | llm×3 | L118 / L121 / L120 | ✅ 支撑充分 |
| CF | 01 CI 红/安全阻断仍批准 → 0 / 02 人身攻击 → 0 | — | L77+L33 / L8 | ✅ 合理，无结构性触发 |

合计：19 项（17 llm + 2 script），check.py 实现 2 项 script 且与 SCORING 逐字符一致；17/17 llm 项有文本支撑。

## 附录 C：本次审查关键文件与行号索引

- SKILL.md：frontmatter L1-4、H1 L6、原则 1-6 L8-22、ROUTING TABLE L24-37、Review Checklist L39-67、DO NOT L69-77、OUTPUT FORMAT L79-110、QUALITY GATES L112-121
- SCORING.yaml：元信息 L1-3、SCOPE 组 L7-29、PROC 组 L32-78、OUT 组 L82-111、NEG 组 L115-136、QA 组 L139-161、CF L163-170
- check.py：导入与 _shared 路径 L5-16、check() L19-52、SCOPE-02 实现 L35、PROC-03 实现 L40、main() L55-71
- _shared/SKILL-SPEC.md：§1.1 L11-14、§1.3 禁用键 L27-32、§2.3 人称 L53-59、§2.4 触发信号 L61-67、§3.1 必需三节 L100-108、§3.2 行数 L110-120、§3.3 文件引用 L122-126、§5 检查清单 L146-161
- skill-dossier.md：046 条目 L388-393、029/030 同源记录（家族上下文）
- complex-skills-no-trigger/046/SKILL.md：破损首条 L8、description L3（无触发句）

## 附录 D：变更记录

- 2026-08-06：全面重审（4 个技能文件 + SKILL-SPEC + dossier + no-trigger 副本 diff）。新发现：no-trigger 副本 L8 破损未同步（🔴）、description 模板残留误指域（🟠）、[SECURITY] 未入分类法（🟠）、SLA 口径冲突（🟠）；正面确认：dossier 两项缺陷已在 trigger 版修复、SCORING 19/19 全支撑、单文件自包含零断链。8 维加权 73.75/100 = B− 🟡（取代旧桩 5 行版）。
- 2026-08-05：旧桩初始审查（5 行，已废弃；其 "48/100" 数值与 "B−" 标签自相矛盾，按语料等级表 48 属 D 区间，本审查重校为 73.75/100 = B−）。
