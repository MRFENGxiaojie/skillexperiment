# REVIEW: 148-signup-flow-cro

**审查日期**: 2026-08-06
**Skill 类型**: workflow — signup/registration flow optimization: audit → recommend → experiment hypotheses
**Body 行数**: 219 行
**参考文件数**: references/0, scripts/0, assets/0, 其他/0
**总文件数**: 3

---

## 1. 目录全量清单

```
148-signup-flow-cro/
├── SKILL.md (219 行)
├── SCORING.yaml (175 行)
└── check.py (79 行)
```

该 skill 是轻量级 skill（3 个文件）。**但 SKILL.md L38 明确引用 `references/signup-cro-playbook.md`，该文件在目录中不存在**——Core Principles（核心方法框架）整体缺失，详见 §5。这也是 148 与 149 两姊妹 skill 共同的"引用缺失"缺陷模式。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `signup-flow-cro`，全小写+连字符 ✓
- 长度: 15 字符，≤64 字符 ✓
- 匹配目录名 `148-signup-flow-cro` ✓

### 2.2 description

原文:
> "When the user wants to optimize signup flows, registration, account creation, or trial activation. Also use when the user mentions \"signup conversions\", \"registration friction\", \"signup form optimization\", \"free trial signup\", \"reduce signup abandonment\", or \"account creation flow\". For post-signup onboarding, see onboarding-cro. For lead capture forms (not account creation), see form-cro."

逐句分析:

**第 1 句** (WHEN): "When the user wants to optimize signup flows, registration, account creation, or trial activation."
- 第三人称 ✓，"the user" 主语 ✓
- 触发场景具体（4 类: signup/registration/account creation/trial activation）✓

**第 2 句** (KEYWORDS): "Also use when the user mentions 'signup conversions', 'registration friction', 'signup form optimization', 'free trial signup', 'reduce signup abandonment', or 'account creation flow'."
- 6 个触发关键词，覆盖全面 ✓
- "Also use when the user mentions" — 触发信号 ✓

**第 3-4 句** (跨技能路由): "For post-signup onboarding, see onboarding-cro. For lead capture forms (not account creation), see form-cro."
- ❌ **违反 SKILL-SPEC §2.5**: description 中嵌入跨技能路由（"For X, see Y"）。该 skill 的 Related Skills 节（L176-183）已经完整承担了 onboarding-cro 与 form-cro 的 WHEN/WHEN NOT 说明，description 中的路由是冗余且违规的。
- 与 skill-dossier.md 记载完全一致（"技能边界清楚🟡description路由"）——讽刺的是，边界说明本身写得很好（Related Skills 节是全文最佳部分），却以违规形式重复出现在 description 中。

总体评价: WHAT/WHEN/KEYWORDS 齐全、人称合规，尾部跨技能路由违反 §2.5。与 149 的 description 违规同源。

修改建议:
```
description: "Optimizes signup, registration, account creation, and trial activation flows — auditing friction, recommending changes, and framing A/B test hypotheses to raise completion rates. Use when the user wants to optimize signup flows or mentions 'signup conversions', 'registration friction', 'signup form optimization', 'free trial signup', 'reduce signup abandonment', or 'account creation flow'."
```

### 2.3 allowed-tools
- frontmatter 中**没有** `allowed-tools` 字段（可选字段，非强制）
- 实际执行需要: Read（product-marketing-context.md）、可能 Bash/WebFetch（抓取 signup 页、读取 analytics）
- 建议补充: `allowed-tools: Read, Glob, Bash, Grep, WebFetch`

### 2.4 其他 frontmatter 字段
- 无禁止字段 ✓；仅有 name、description ✓

### 2.5 Frontmatter 语法
- YAML 分隔符配对正确（L1/L4）✓
- description 引号转义 `\"` 正确 ✓

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Signup Flow CRO (L6)                              — 标题
## Initial Assessment (L10-34)                      — 前置评估：营销上下文 + 3 组问题，~25 行
## Core Principles (L37-38)                         — 核心原则：仅 1 行委托，指向缺失文件，~2 行
## Output Format (L40-60)                           — 输出格式：Audit Findings / Recommended Changes / Form Redesign，~21 行
## Common Signup Flow Patterns (L63-84)             — 4 类常见流程模式（B2B/B2C/Waitlist/E-commerce），~22 行
## Experiment Ideas (L87-163)                       — 实验想法库：4 个子节，~77 行
   ### Form Design Experiments (L89-116)            — 表单设计实验（布局/字段/认证/视觉）
   ### Copy & Messaging Experiments (L119-138)      — 文案实验（标题/微文案/信任元素）
   ### Trial & Commitment Experiments (L141-153)    — 试用与承诺实验（免费试用/摩擦点）
   ### Post-Submit Experiments (L157-162)           — 提交后实验
## Task-Specific Questions (L166-172)               — 任务专项问题 5 条，~7 行
## Related Skills (L176-183)                        — 6 个相关技能 + WHEN/WHEN NOT，~8 行
## Communication (L187-195)                         — 输出质量标准，~9 行
## Proactive Triggers (L199-207)                    — 5 个主动触发场景，~9 行
## Output Artifacts (L211-219)                      — 交付物表，~9 行
```

### 3.2 必需章节检查

#### Workflow/Process 节
- ⚠️ **无显式 workflow 节**。流程是隐式的: Initial Assessment（收集上下文）→ Audit Findings（诊断）→ Recommended Changes（Quick wins → High-impact → Test hypotheses 分层建议）→ Form Redesign（可选）→ A/B 假设。这个"审计→建议→实验"链条散落在 Output Format 和 Communication 节中，逻辑成立（dossier 确认"审计→建议→实验框架一致"），但没有一个名为 Workflow/Process 的节把步骤串起来。
- "## Core Principles"（L37-38）本该承载方法框架，但只有一行委托:
  ```
  ## Core Principles
  → See references/signup-cro-playbook.md for details
  ```
  委托文件**不存在**。核心原则（如何判断摩擦点、字段取舍框架、减少摩擦的优先级思维）完全缺失。
- "## Experiment Ideas"（L87-163）是全文最重的节（77 行），一个四分类实验想法库——这是菜单/目录，不是决策流程。

#### Output Format 节
- 存在 ✓（L40-60）
- Audit Findings: Problem / Impact / Fix / Priority 四要素（注意: 与 149 的五要素不同，148 是四要素——Impact 带"estimated impact if possible"）✓ 与 SCORING PROC-01 的 "Impact" 检查一致
- Recommended Changes: 按 Quick wins → High-impact → Test hypotheses 三档组织 ✓（与 Communication 和 SCORING PROC-02 一致）
- Form Redesign（可选）: 字段集+理由、字段顺序、文案、视觉布局四要素 ✓ 与 SCORING FMT-01 对应

#### Scope/Limitations 节
- **不存在** ❌
- 与 149 同病: 何时不使用（在 Related Skills 的 WHEN NOT 中有路由层面的覆盖）、无数据分析时的降级路径（ERR-01 要求的行为在正文缺失）、付费工具限制等均无说明

### 3.3 内容委托分析

L38 委托 `references/signup-cro-playbook.md`——该文件缺失。值得注意的是，Experiment Ideas（77 行）内容充实，说明设计者在正文中保留了实验目录，却把"判断原则"（核心原则）放到了缺失的文件里——正好委托反了: 应该保留的是原则，可外置的是实验目录。委托比例按行数算约 1/219，但委托的是方法论核心。

### 3.4 节编号/标题层级
- 标题层级: # → ## → ### 连续，无跳级 ✓
- ### 子节出现在 Experiment Ideas 下，格式一致 ✓
- "### Copy & Messaging Experiments" 使用 & 符号，其余子节用 & 或 And——风格统一性可接受

### 3.5 Body 长度合规
- 实际 219 行，workflow pattern 目标约 200 行，hard limit 600 行 ✓ 接近目标行数

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

- Initial Assessment（flow type / current state / business constraints）→ 隐式审计 → Recommended Changes 分层 → （可选）Form Redesign → A/B 假设: 链条自洽 ✓
- SCORING PROC-05（post-submit experience）在正文有 "Post-Submit Experiments" 子节（L157-162）支撑 ✓
- SCORING PROC-04（SSO/auth 考虑）在正文有 "Auth Options" 子节（L105-109）与 Communication 标准（L192 "SSO options are always considered"）支撑 ✓
- SCORING PROC-07（fix vs test 区分）在正文 Communication L195 有支撑（"Experiment ideas distinguish between 'fix this' (obvious) and 'test this' (uncertain) — never recommend testing obvious improvements"）——一句话原则，支撑较薄但存在 ✓

### 4.2 内部矛盾扫描

1. **"Quick wins" 大小写不一致**（中危）: Output Format L52 写作 "1. Quick wins (same-day fixes)"（小写 w）；Communication L190 写作 "**Quick Wins → High Impact → Test Hypotheses**"（大写 W）；SCORING PROC-02 模式为 "Quick Wins"（大写）。skill 内部自身大小写混用，agent 依从哪一处都可能与脚本检查错位。
2. **FMT-02 "Success Metric" 与正文 "success metric" 不匹配**（高危，假阴性）: Output Artifacts 表 L219 写 "Hypothesis x variant description x success metric x priority"（小写 m），正文中无任何一处大写 "Success Metric"。`output_contains("Success Metric")` 大小写敏感——**严格按 skill 输出的 agent 100% 过不了 FMT-02**。这是 SCORING/check.py 与 SKILL.md 之间的系统性失配。
3. **Mobile 不是独立节**（中危）: SCORING PROC-06 要求 "Mobile optimization treated as a distinct section, not an afterthought"。正文中 mobile 只出现两处: Experiment Ideas 的 "Visual Design" 子节一条 bullet（"Mobile-optimized layout testing"）和 Proactive Trigger #5（"High mobile signup drop-off"）。没有专门的 Mobile 节——忠实 agent 若不额外发挥，llm judge 的 PROC-06 可能不通过。skill 自身标准（L194 "Mobile optimization is treated as a distinct section"）与正文结构矛盾。
4. **Task-Specific Questions 与 Initial Assessment 重复**（低危）: L166-172 的 5 个问题（完成率、字段级 analytics、必需数据、合规要求、signup 后发生什么）与 L16-34 的 Initial Assessment 问题组大面积重叠（completion rate、data needed、post-signup 均出现两次）。
5. **NEG-02 的 analytics 前置门禁未入正文**（中危）: SCORING NEG-02 要求 "No A/B test recommendations before field-level drop-off analytics are instrumented — missing analytics are flagged instead"。正文 Communication 只讲了 fix vs test，**没有**提及 analytics 门禁。忠实 agent 可能直接给 A/B 建议而违规（CF-01 边缘）。

### 4.3 示例/代码正确性

- Common Signup Flow Patterns（L63-84）4 个模式示例（B2B SaaS Trial、B2C App、Waitlist、E-commerce Account）均符合行业惯例 ✓
- 一个边界小疑点: E-commerce 模式 "Guest checkout as default"（L81-83）——guest checkout 属于购买流程而非账号创建流程，与 form-cro/paywall 的边界有轻微模糊，但作为"账号创建模式"的对照参考可接受
- Experiment Ideas 中的实验变量（SSO 选项、7/14/30 天试用、CAPTCHA 等）均为真实 CRO 实践 ✓

### 4.4 条件完整性

- Initial Assessment 3 组问题覆盖 SCOPE-03 全部要素（flow type 五选一、current state 四问、business constraints 三问）✓
- "Form Redesign (if requested)" 的条件分支明确（"if requested"）✓
- 缺少分支: 用户没有任何 analytics 数据时的降级（ERR-01，正文无）；用户只要 audit 不要 redesign 时的输出裁剪（隐含于 Output Format 的 "(if requested)"，可接受）

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用路径 | SKILL.md 行号 | 是否存在 | 状态 |
|----------|:------------:|:--------:|:----:|
| references/signup-cro-playbook.md | L38 | ❌ | **缺失 — Core Principles 文件** |

与 149 相同的缺陷模式: 唯一的跨文件引用指向不存在的文件，且承载的是方法论核心。后果:
- agent 只读 SKILL.md 时，signup CRO 的判断框架（如何识别摩擦、字段取舍的思维模型）缺失
- SCORING PROC-03（"do we need this before they can use the product?" 字段取舍测试）、PROC-07（fix vs test）依赖的原则虽在 Communication 有零星表述，但系统性框架无处可寻

### 5.2 不可见资源审计
实际存在的 3 个文件全部被 runner 使用，无不可见资源 ✓。

### 5.3 Reference 文件全文审查
无 reference 文件存在。

### 5.4 Scripts 文件全文审查
无 scripts/ 目录 ✓。

### 5.5 跨 Skill 引用检查
- Related Skills（L176-183）以纯文本名称引用 6 个技能（onboarding-cro、form-cro、page-cro、ab-test-setup、paywall-upgrade-cro、marketing-context），每个带 WHEN/WHEN NOT，边界清晰——**全文最佳部分** ✓
- 无 `../` 文件路径 ✓ 合规

### 5.6 嵌套重复/死文件检查
- 无 self-nested 目录、无 .gitkeep、无冗余文件 ✓

---

## 6. 语法与格式质量

### 6.1 拼写错误
无明显拼写错误。CRO 领域术语（abandonment、friction、microcopy、freemium）拼写正确 ✓。

### 6.2 语法错误
- "### Copy & Messaging Experiments"（L119）与其他子节标题并列，& 使用规范 ✓
- 整体英文流畅，无病句 ✓

### 6.3 中英/葡英混杂
全程英文，无混杂 ✓。

### 6.4 Markdown 格式破损
- 无破损。标题层级、表格、列表、粗体均完好 ✓
- L92-96 "Layout & Structure" 等子节内部使用 bullets 而非编号，风格统一 ✓

### 6.5 占位符未填充
- 无 TODO/FIXME/TBD ✓
- 无未填充占位符 ✓

### 6.6 截断内容
- L219 以 Output Artifacts 表格结尾，文件完整 ✓

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

逐条对照 `_shared/SKILL-SPEC.md` §5 合规清单的 12 条:

1. **name 匹配目录名**: ✅ `signup-flow-cro` 匹配 `148-signup-flow-cro`
2. **description 第三人称 + WHAT/WHEN/KEYWORDS + ≤1024**: ✅ 三要素齐全，约 470 字符
3. **description 无祈使/第一/第二人称开头**: ✅ 以 "When the user wants..." 开头
4. **description 无跨技能路由**: ❌ 尾部两处路由（"see onboarding-cro"、"see form-cro"）违反 §2.5
5. **description 含触发信号短语**: ✅ "Use when the user wants..."、"Also use when the user mentions..."
6. **frontmatter 无禁止字段**: ✅ 仅有 name、description
7. **body ≤600 行**: ✅ 219 行
8. **body 有 workflow/process 节**: ⚠️ 流程隐式存在于 Output Format/Communication，无显式 workflow 节；Core Principles 节为空壳（委托缺失文件）
9. **body 有 output format 节**: ✅ "## Output Format" 完整
10. **body 有 scope/limitations 节**: ❌ 不存在
11. **body 无跨 skill 文件路径引用**: ✅ 无 `../` 路径
12. **目录命名**: ✅ `148-signup-flow-cro` 为 NNN-kebab-case

**合规率: 9/12 ✅，1 项部分合规（规则 8），2 项违规（规则 4、规则 10）**

### 违规详情

**违规 1 — description 嵌入跨技能路由（规则 4）**: 同 149。§2.5 要求路由移入正文；Related Skills 节已完整承担路由职责。

**违规 2 — 缺少 Scope/Limitations 节（规则 10）**: 无专门 Scope 节；"Do not use form-cro for registration/account creation flows" 等边界只在 Related Skills 的 WHEN NOT 中，属于路由护栏而非 scope 声明。

**部分合规 — Workflow 节隐式 + Core Principles 空壳（规则 8）**: 审计→建议→实验链条存在但无显式节；Core Principles 委托给缺失文件。

---

## 8. 人机感评估

### 8.1 Emoji 审计
全文**零 emoji** ✓。CRO 咨询场景下保持专业纯文字风格，合理。

### 8.2 全大写/喊叫式语言
- 无 `STOP!`、`MANDATORY` 等喊叫式表达 ✓
- "never recommend testing obvious improvements"（L195）使用 never 但语气克制 ✓

### 8.3 Persona 语气分析
- 开头 "You are a signup and registration flow optimization specialist."（L8）— 第二人称 persona 开场，标准做法 ✓
- 整体为专业 CRO 顾问口吻，指令层中性
- Communication 节质量高: "Every field removal recommendation is justified against the 'do we need this before they can use the product?' test"（L191）——把判断标准写成可操作的提问，是可执行性极佳的表述

### 8.4 人机边界分析
- "Recommendations are always organized as Quick Wins → High Impact → Test Hypotheses — never a flat list"（L190）— 结构纪律 ✓
- "never recommend testing obvious improvements"（L195）— 修复与实验的边界 ✓
- 缺少: 无 analytics 数据时不得编造基线的显式边界（ERR-01 只在 SCORING）；A/B 测试前的 analytics 门禁（NEG-02 只在 SCORING）

### 8.5 人称分析
- 指令层第三人称/中性 ✓；persona 开场与话术层的 "you" 属标准用法
- 无第一人称（"I will"）✓

### 8.6 表格使用评估
- 仅 Output Artifacts 一个表格（L213-219）✓
- 其余为列表组织，对实验目录（77 行）而言列表比表格更合适 ✓

---

## 9. 可执行性评估

### 9.1 独立可执行性
- 假设 agent 只拿到 SKILL.md: 输出结构（Audit Findings 四要素、Recommended Changes 三档、Form Redesign 四要素）完整可照做；实验想法库（77 行）提供了大量可直接引用的具体假设素材；4 类流程模式提供对照参考。
- **缺失的是判断框架**: 如何发现摩擦点、如何权衡字段、如何设定优先级的原则在缺失的 playbook 中。agent 需要依靠自身 CRO 知识。
- 相比 149（5/10），148 因为实验库与模式的补充，可执行性更高。
- 打分: **6/10**

### 9.2 步骤可操作性

| 环节 | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| Initial Assessment | 3 组问题收集上下文 | 🟢 | 具体完整，与 SCOPE-03 对应 |
| Core Principles | "See references/signup-cro-playbook.md" | 🔴 | 文件缺失，判断框架空洞 |
| Output Format | 四要素 findings + 三档建议 + 可选 redesign | 🟢 | 具体可照做 |
| Common Patterns | 4 类流程模式 | 🟢 | 直接可用的对照模板 |
| Experiment Ideas | 4 类实验目录 | 🟢 | 素材丰富，但无"该推荐哪个"的选择规则 |
| Proactive Triggers | 5 个触发场景 | 🟢 | 场景 + 行动方向明确 |
| Output Artifacts | 交付物表 | 🟡 | A/B 假设表的列名 "success metric" 小写与 FMT-02 失配 |

### 9.3 工具依赖合理性
- 无硬编码工具/服务依赖 ✓
- 需要 analytics 数据（完成率、drop-off）但 skill 没有定义数据获取方式（GA/Amplitude 等）——由 agent 与用户协商，可接受

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml 定义 19 个 criteria（SCOPE-01~03, PROC-01~07, FMT-01~03, NEG-01~03, QA-01~02, ERR-01），其中 4 个由 check.py 脚本执行，15 个由 llm judge 执行。total_items: 19 = 3+7+3+3+2+1 ✓ 计数正确。

### 10.2 脚本检查模式与 SKILL.md 文本一致性矩阵

| Criterion | 检查模式 (check.py) | SKILL.md 对应文本 | 一致性 |
|-----------|--------------------|------------------|:------:|
| SCOPE-02 | `product-marketing-context\.md` | L13 `.claude/product-marketing-context.md` | ✅ 一致 |
| PROC-01 | `Impact` | L45 "**Impact**: Why it matters" | ✅ 一致 |
| PROC-02 | `Quick Wins`（大写 W） | L52 "Quick wins"（小写）vs L190 "Quick Wins"（大写） | ⚠️ **正文大小写混用** |
| FMT-02 | `Success Metric`（大写 S/M） | L219 "success metric"（小写）——正文无大写形式 | ❌ **假阴性风险高** |

**关键发现**: 两个脚本检查存在大小写失配:
1. FMT-02 "Success Metric": 正文 Output Artifacts 表写的是小写 "success metric"，全文没有任何大写 "Success Metric"。忠实 agent 必挂 FMT-02。**这是 SCORING.yaml 设计错误，不是 agent 问题**。
2. PROC-02 "Quick Wins": 正文两处大小写并存——若 agent 按 Output Format（L52）输出则挂，按 Communication（L190）输出则过。skill 自身不一致是根因。

### 10.3 llm judge 项的可用性

- SCOPE-01/03、PROC-03~07、FMT-01/03、NEG-01~03、QA-01/02、ERR-01 依赖正文支撑。其中:
  - PROC-03（字段取舍测试）: Communication L191 有支撑 ✓
  - PROC-04（SSO 考虑）: L105-109 + L192 ✓
  - PROC-05（post-submit）: L157-162 ✓
  - PROC-06（mobile 独立节）: ⚠️ 正文只有 bullet 级提及，无独立节——llm judge 严格时可能不通过
  - PROC-07（fix vs test）: L195 一句话支撑，偏薄
  - NEG-02（analytics 门禁）: ❌ 正文无依据——忠实 agent 可能直接违规
  - ERR-01（无数据不编造）: ❌ 正文无依据

### 10.4 Critical Failures 分析

- CF-01（把显然的修复当 A/B 实验）: 合理，与 Communication L195 一致 ✓
- CF-02（完全忽略 post-submit experience）: 合理，正文有 Post-Submit 子节 ✓
- CF-03（用错框架: onboarding-cro 处理表内流失 / form-cro 处理账号创建）: 合理，与 Related Skills 的 WHEN NOT 一一对应 ✓

评价: 三个 CF 与正文规则咬合良好，是本批 4 个 skill 中 CF 设计最贴合的。

### 10.5 缺失的测评点建议

- 无检查 "Form Redesign" 触发条件（仅在用户请求时产出）的 criterion——FMT-01 只查内容要素
- 无检查 Recommended Changes 三档组织（Quick→High→Test）顺序的 criterion（PROC-02 只查 "Quick Wins" 字样存在）

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 对 148 的记载:
> **148-signup-flow-cro — 150-copywriting**: "...148 审计→建议→实验框架一致、技能边界清楚；..." **合规**: "🟡 description 中内嵌跨技能路由（违反 §2.5），需移入正文。"

对照验证:

| Dossier 记载 | 本次审查验证 | 状态 |
|-------------|------------|:----:|
| 审计→建议→实验框架一致 | Output Format 三档建议 + Communication 标准 + SCORING 三层次对应 | ✅ 确认 |
| 技能边界清楚 | Related Skills 6 个 WHEN/WHEN NOT 边界精准 | ✅ 确认 |
| description 路由违规 | L3 尾部 "see onboarding-cro" / "see form-cro" | ✅ 确认 |

**Dossier 未记载的新问题（本次审查发现）**:
1. 🔴 `references/signup-cro-playbook.md` 缺失——Core Principles 核心文件不存在
2. 🔴 FMT-02 "Success Metric" 与正文 "success metric" 失配——忠实 agent 必挂的脚本检查
3. 🟡 PROC-02 "Quick Wins" 与正文大小写混用
4. 🟡 Mobile 无独立节，与自身标准（L194）及 PROC-06 矛盾
5. 🟡 NEG-02 analytics 门禁、ERR-01 无数据降级均未入正文
6. 🟡 Task-Specific Questions 与 Initial Assessment 重复

---

## 12. 综合评分

### 维度评分

**Frontmatter 合规 (6/10, 权重 10%)**: 人称、触发词、长度均合规；description 尾部跨技能路由违反 §2.5（已确认）。

**Body 结构完整 (7/10, 权重 10%)**: 有 Output Format；无 Scope 节；无显式 workflow 节（流程隐式）；Core Principles 委托缺失文件；实验目录充实是加分项。

**逻辑一致性 (9/10, 权重 20%)**: 审计→建议→实验框架一致、技能边界清楚（dossier 确认）；主要问题是大小写失配、Mobile 节缺失、问题节重复。

**参考完整性 (3/10, 权重 15%)**: 唯一引用的 playbook 文件缺失。与 149 相同的最短板。

**语法格式 (9/10, 权重 10%)**: 英文干净、格式完好、无错字。

**规范合规 (7/10, 权重 15%)**: 12 条规则 9 条全合规；2 条违规（description 路由、缺 Scope）；1 条部分合规（workflow 隐式）。

**人机感 (9/10, 权重 10%)**: 专业 CRO 口吻、零 emoji、"字段取舍测试"等可操作表述优秀；缺无数据不编造的显式边界。

**可执行性 (6/10, 权重 10%)**: 输出结构 + 实验库 + 模式库提供良好脚手架；判断框架缺失；两条脚本检查有假阴性风险。

**加权总分: 7.00/10 = 70/100**

计算: 0.10×6 + 0.10×7 + 0.20×9 + 0.15×3 + 0.10×9 + 0.15×7 + 0.10×9 + 0.10×6 = 7.00

### 评级: 🟡 B- (70/100)
内容质量高于 149（实验库与边界设计优秀），但被缺失的 playbook 文件和两条脚本失配拖累。修复后可达 80+ 分档。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**F-1: 创建缺失的 `references/signup-cro-playbook.md`（或将核心原则内联）**
- 位置: SKILL.md L38 引用的文件
- 问题: Core Principles（判断框架）完全缺失
- 修复: 创建该文件，至少包含:
  1. **摩擦识别框架**: 如何在字段层面识别摩擦（必填字段数量、字段类型、验证时机）
  2. **字段取舍测试**: "do we need this before they can use the product?" 的具体操作化（逐字段提问模板）
  3. **优先级思维模型**: 影响面 × 改动成本 × 数据可信度的排序方法
  4. **常见反模式**: 过度收集字段、验证前置过严、忽略 post-submit、社交登录缺失等
- 或者内联进 SKILL.md——推荐内联核心原则（约 40-60 行），将 Experiment Ideas 目录（77 行）外置到 reference——当前委托方向正好反了
- 不修复的后果: 判断框架缺失，PROC-03/PROC-07 依赖的原则无系统支撑

**F-2: 补 Scope/Limitations 节（违反 SKILL-SPEC §3.1 规则 10）**
- 位置: SKILL.md Communication 节之后
- 修复: 新增 "## Scope & Limitations" 节:
  ```markdown
  ## Scope & Limitations

  This skill optimizes signup/registration/account-creation flows. It does NOT:

  - **Optimize onboarding** — post-signup activation is onboarding-cro's scope;
    this skill stops at successful account creation.
  - **Optimize lead capture forms** — lead magnets, contact, demo request, and
    survey forms belong to form-cro.
  - **Convert free users to paying** — that is paywall-upgrade-cro's territory.
  - **Invent data** — when completion rate or drop-off data is unknown, ask for
    it or flag it as missing; never fabricate a baseline.
  - **Recommend A/B tests before analytics exist** — flag missing field-level
    drop-off analytics instead of proposing experiments on top of guesses.
  ```
- 不修复的后果: 边界与数据纪律无正文依据，agent 可能越界或编造数据

### 🟡 重要缺陷（建议修复）

**I-1: 移除 description 中的跨技能路由（违反 §2.5）**
- 位置: SKILL.md L3 尾部两句
- 修复: 按 §2.2 的修改建议替换 description；路由职责完全交给 Related Skills 节
- 不修复的后果: 规范审计不通过；触发阶段可能误导模型路由

**I-2: 修复 FMT-02 "Success Metric" 失配（脚本假阴性）**
- 位置: SCORING.yaml FMT-02 + check.py L45 + SKILL.md L219
- 修复方案 A（推荐）: SKILL.md Output Artifacts 表改列名为 "Success Metric"（大写），与 SCORING 对齐——成本一行
- 修复方案 B: check.py 模式改为 `[Ss]uccess [Mm]etric`，SCORING.yaml 同步——成本两处
- 注意: 按任务约束只记录建议，由维护者执行；同时确认 A/B 假设表的三列（Hypothesis x variant x metric）在交付时确实出现

**I-3: 统一 "Quick Wins" 大小写**
- 位置: SKILL.md L52（小写）、L190（大写）
- 修复: 统一为 "Quick Wins"（大写，与 Communication 标准和 SCORING 对齐）；L52 的 "1. Quick wins (same-day fixes)" 改为 "1. Quick Wins (same-day fixes)"

**I-4: 增加 Mobile 独立节**
- 位置: Experiment Ideas 之后或 Communication 附近
- 修复: 新增 "## Mobile Signup Optimization" 节（约 10 行）: 移动端字段数量建议、键盘类型、触控目标尺寸、移动端 SSO 优先、移动端 drop-off 分析清单——使正文结构与自身标准（L194）和 PROC-06 一致

**I-5: 将 NEG-02 与 ERR-01 规则写入正文**
- 位置: Communication 节
- 修复: 增加两条质量标准:
  - "Never propose A/B tests before field-level drop-off analytics are instrumented — flag the missing analytics instead."
  - "When completion rate or drop-off data is unknown, ask for it or flag it as missing; never invent a baseline."

### 🟢 优化建议（锦上添花）

**O-1: 合并 Task-Specific Questions 与 Initial Assessment**
- 删除 L166-172 的 Task-Specific Questions（5 问与 Initial Assessment 重复），或只保留差异项（competitors）

**O-2: 为 Experiment Ideas 增加选择规则**
- 77 行实验目录没有"该推荐哪个实验"的指导——在目录前加一段: 根据 Initial Assessment 的瓶颈位置（表单内流失 vs 提交后流失）选择对应子节的实验；按影响面排序 Top 3-5

**O-3: 补充 allowed-tools**
- 建议添加 `allowed-tools: Read, Glob, Bash, Grep, WebFetch`

**O-4: SCORING 补充测评点**
- 增加检查 Recommended Changes 三档组织的顺序 criterion；增加 Form Redesign 仅在请求时产出的 criterion

### 修复工作量估计
- 预计修改行数: 内联核心原则 +50 行（或新建 reference ~80 行）、Scope 节 ~15 行、Mobile 节 ~10 行、大小写修正 2 行、表格列名 1 行
- 预计修改文件数: 2 个（SKILL.md + 新建 references/signup-cro-playbook.md，或仅 SKILL.md）；SCORING.yaml/check.py 视 I-2 方案而定

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 219 行，全文精读
2. SCORING.yaml — 175 行，全文
3. check.py — 79 行，全文
4. _shared/SKILL-SPEC.md — 161 行，全文（合规依据）
5. _shared/checker.py — 351 行，全文（output_contains 大小写敏感性验证）

### 读取统计
- 总文件数: 5（3 skill 文件 + 2 shared 支持文件）
- 总行数: 约 985 行

### 审查方法
- 所有文件全文阅读，未使用抽样
- 合规检查依据: SKILL-SPEC.md v1.0 的 12 条清单
- 脚本检查一致性依据: _shared/checker.py 的 `output_contains` 实现（确认大小写敏感 regex）
- 已知问题对照: skill-dossier.md（2026-08-05 审查记录）
