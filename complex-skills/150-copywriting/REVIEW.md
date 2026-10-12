# REVIEW: 150-copywriting

**审查日期**: 2026-08-06
**Skill 类型**: workflow — 转化文案写作（web 页面营销文案：首页/落地页/定价页/功能页/关于页）
**Body 行数**: 282 行（SKILL.md 共 288 行内容；wc -l 计 287，末行无结尾换行符）
**参考文件数**: references/0（但正文引用 2 个不存在的 references/ 文件——悬空引用，见 §5）
**Dossier 评级**: 🟡（写作原则与输出物表相互印证；description 中内嵌跨技能路由需移入正文）
**总文件数**: 3（SKILL.md + SCORING.yaml + check.py）

---

## 1. 目录全量清单

```
150-copywriting/
├── SKILL.md       (288 行内容；wc -l 计 287，末行无结尾换行符)
├── SCORING.yaml   (175 行，19 项判据 + 3 项致命失败)
├── check.py       (79 行，4 项脚本检查)
└── REVIEW.md      (本文件)
```

全部文件为 CRLF 行尾（Windows 风格）。**关键事实**: 目录中不存在 `references/` 目录，但 SKILL.md 正文两次引用其中的文件——`references/natural-transitions.md`（L119）与 `references/copy-frameworks.md`（L141）。这是本审查的最高优先级发现（§5.2 与 §13 🔴-1）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- `name: copywriting` — 小写 + 连字符 ✅
- 长度: 10 字符 ≤64 ✅
- 与目录名 `150-copywriting`（去掉 NNN- 前缀后）一致 ✅

### 2.2 description

**实际值**:

> When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about us, or product pages. Also use when the user says 'write copy for', 'improve this copy', 'rewrite this page', 'marketing copy', 'help with headline', or 'CTA copy'. For email copy, see email-sequence. For popup copy, see popup-cro.

**逐句分析**:

| 检查项 | 结果 |
|--------|------|
| WHAT | ✅ "write, rewrite, or improve marketing copy for any page" + 6 类页面枚举（homepage/landing/pricing/feature/about us/product pages），具体明确——WHAT 内嵌于 WHEN 句，虽无独立 WHAT 句但语义完整 |
| WHEN | ✅ 双段触发: 场景描述 + 用户原话引号触发词（'write copy for'、'improve this copy'、'rewrite this page'、'marketing copy'、'help with headline'、'CTA copy' 共 6 个）——这是全语料库少见的"原话触发词"设计，匹配意图极强 |
| KEYWORDS | ✅ marketing copy、homepage、landing pages、pricing、headline、CTA copy |
| 人称 | ✅ 以 "When the user wants to..." 条件句开头，非祈使、非第一/第二人称 |
| 触发信号 | ⚠️ "Also use when the user says..." 含 "use when the user" 子串（变体形式），"When the user wants to..." 语义上是触发条件——两者均非 SKILL-SPEC §2.4 列出的标准句式（"Use when the user asks to..." 等），语义达标、字面部分达标 |
| 长度 | 约 460 字符 ≤1024 ✅ |
| 跨技能路由 | ❌ **违规**——"For email copy, see email-sequence. For popup copy, see popup-cro." 将跨技能路由内嵌在 description 中。SKILL-SPEC §2.5 明文规定: 跨技能路由（"NOT for X, use Y instead"）属于正文 Scope 节的职责，不得放 description。这正是 dossier 标记的问题，本次审查确认 |

**总体评价**: 触发设计是全语料库最强者之一（场景 + 原话双段），但路由句混在其中稀释了触发纯度，且违反规范。

**修改建议**:

> "Writes conversion-focused marketing copy for web pages — homepage, landing pages, pricing pages, feature pages, about us, or product pages. Use when the user wants to write, rewrite, or improve marketing copy, or says 'write copy for', 'improve this copy', 'rewrite this page', 'marketing copy', 'help with headline', or 'CTA copy'."

（路由句移入正文 Related Skills——email-sequence 已有条目，补 popup-cro 一条即可，见 §13 🟡-1。）

### 2.3 allowed-tools

未声明。✅ 纯写作型技能（读上下文 + 输出文本），不依赖受限工具，省略可接受（与 146 的工程型技能不同——写作型对工具的依赖极低）。

### 2.4 其他字段

仅 `name` + `description` 两个键，无禁止字段 ✅。YAML 单行双引号，内含撇号（'write copy for'）与破折号（—），均在双引号字符串内，无解析问题 ✅。无 BOM ✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

SKILL.md 正文 282 行，13 个 H2 小节，按"写前 → 写中 → 写后 → 协作"编排:

```
# Copywriting                                  (L6)    — 标题
Persona 声明                                    (L8)    — "You are an expert conversion copywriter."
## Before Writing                              (L10-36) — 上下文采集 4 组 + 产品营销上下文文件约定
## Copywriting Principles                      (L39-56) — 5 条原则
## Writing Style Rules                         (L59-80) — 6 条风格规则 + 快速质检 5 问
## Best Practices                              (L82-101) — 直白/反问/类比/幽默
## Page Structure Framework                    (L104-141) — Above the Fold + 主区块表（引用 2 个不存在文件）
## CTA Copy Guidelines                         (L145-162) — 强弱对照 + 公式 + 示例
## Page-Specific Guidance                      (L166-191) — 5 类页面
## Voice and Tone                              (L195-212) — 正式度 + 品牌人格 + 强度调节
## Output Format                               (L216-238) — Page Copy / Annotations / Alternatives / Meta
## Proactive Triggers                          (L242-250) — 5 项主动标记
## Output Artifacts                            (L254-262) — 请求类型 → 交付物对照表
## Communication                               (L266-275) — 结论先行 / What+Why+How / 置信度标记
## Related Skills                              (L279-287) — 8 个关联技能的 USE/NOT 路由
```

内容密度高，原则 → 规则 → 结构 → 示例 → 交付 → 协作的链条完整，正文写作质量在语料库中属于信息量最大的之一。

### 3.2 必需章节检查

| 必需章节 | 判定 | 定位 |
|----------|------|------|
| Workflow / Process | ⚠️ 部分满足 | 无 `## Workflow` 标题，但 "Before Writing"（采集上下文）→ 各写作章节 → "Output Format"（交付）→ "Output Artifacts"（验收对照）构成隐式流程链，起点与终点明确，中间缺显式步骤编排 |
| Output Format | ✅ 满足 | `## Output Format`（L216-238）明确交付形态: Page Copy / Annotations / Alternatives（Option A/B + rationale）/ Meta Content；`## Output Artifacts`（L254-262）补充按请求类型的交付物对照表——**本 skill 是显式 Output Format 节最完整的写作类 skill** |
| Scope / Limitations | ⚠️ 部分满足 | 无 `## Scope` / `## Limitations` 标题。边界语义由两处承担: description 路由句（"For email copy, see email-sequence..."——位置错误，见 §11）与 `## Related Skills` 的 USE/NOT 双句（"USE for X. NOT for Y"）。Related Skills 形式合规，但缺技能自身能力边界的独立声明（如: 不做品牌策略、不做视觉设计、不生成图片） |

**评分**: Workflow 6/10, Output 10/10, Scope 6/10

### 3.3 内容委托分析

委托结构存在但**执行不完整**:
- L119: "**For natural transition phrases**: See references/natural-transitions.md"——委托目标文件**不存在**（🔴）
- L141: "**For detailed section types and page templates**: See references/copy-frameworks.md"——委托目标文件**不存在**（🔴）
- L78: "For thorough line-by-line review, use the **copy-editing** skill after your draft."——委托给外部技能（正文内路由，合规位置 ✅）

委托意图清晰（正文放原则、参考放素材），但两处承诺未兑现。这是"委托模式"最坏的形态: **委托了，但受托方不存在**。修复方向: 补建两个参考文件（正文已给出内容定位），或删除两处引用并内联素材（见 §13 🔴-1）。

### 3.4 标题层级

- H1 + 13 个 H2 + 少量 `###`（Before Writing 的 1-4 组、Writing Style Rules 的 Core Principles、Page Structure Framework 的 Headline/Subheadline/CTA、Output Format 的 4 项）——层级递增正常，无跳级 ✅
- 表格 2 张（主区块用途表、Output Artifacts 对照表），与列表交错，节奏好 ✅

### 3.5 Body 长度

282 行，占 600 上限的 47%，合规 ✅。`pattern: workflow` 在 SKILL-SPEC §3.2 的目标行数约 200 行——实际 282 行略超目标但远低于硬上限；若按"删引用内联"方案（🔴-1 方案 B），正文将增至约 330 行，仍合规。

---

## 4. 逻辑一致性深度审查

### 4.1 隐含工作流衔接

```
读取 .claude/product-marketing-context.md（存在时）   (L13)
  → 按 Before Writing 4 组问题补齐上下文，缺则问     (L15-35)
  → 确立 Voice and Tone                              (L195-212)
  → 按 Page Structure Framework + 页面类型写作        (L104-191)
  → 逐节应用 Proactive Triggers 自查                  (L242-250)
  → 按 Output Format / Output Artifacts 交付          (L216-262)
  → 按 Communication 模式输出（结论先行+标注+备选）   (L266-275)
```

这条链完整自洽，起点（读上下文）与终点（交付形态）都明确，中间缺显式编号编排——与 151 同型的"隐式 workflow"问题。

### 4.2 内部矛盾深度扫描

1. **变体数量矛盾（🟡 本审查新增发现，dossier 与既往审查均未记载）**:
   - `## Output Format` 的 Alternatives 节（L230）: "For headlines and CTAs, provide **2-3 options**"
   - `## Output Artifacts` 表（L259）: "Headline options | **5** headline variants using different formulas"
   - `## Output Artifacts` 表（L260）: "CTA copy | **3-5** CTA options with formula and rationale for each"
   - 同一 skill 内，headline 备选数一处说 2-3、一处说 5；CTA 备选数一处说 2-3、一处说 3-5。且 Alternatives 节只示范了 Option A/B 两行——三处数值互相打架。
   - 更微妙的是 SCORING.yaml 的 FMT-03 采用 5 / 3-5 版本（"5 headline variants, 3-5 CTA options"）——**评测层与 Output Artifacts 表一致，与 Output Format 的 "2-3 options" 不一致**。agent 按正文 Alternatives 节交 2 个选项，FMT-03 的 llm 判定可能不认（"3-5 CTA options"）；agent 按 Output Artifacts 交 5 个，又违背正文 Alternatives 的 "2-3 options"。
   - 修复: 统一为 "3-5 options"（对齐 Output Artifacts 与 FMT-03），Alternatives 节示例扩为 Option A/B/C 三行。

2. **description ↔ Related Skills 的路由对象不一致（🟡）**: description 路由到 "popup-cro"，但正文 Related Skills 列表（8 个: marketing-context / copy-editing / content-strategy / social-content / marketing-ideas / content-humanizer / ab-test-setup / email-sequence）**没有 popup-cro**；description 的 email-sequence 则在列表中 ✅。路由对象与正文清单不一致——若按 description 去找 popup-cro 的协作说明，正文里没有。

3. **"Clarity Over Creativity" vs Best Practices 的修辞手法（🟡 轻微）**: 原则 1 说"清楚优先于创意"，而 Best Practices 节积极推广 Rhetorical Questions / Analogies / Humor 等修辞手法——表面张力，实际可自洽（"清晰优先，创造辅助"：手法受"不伤清晰"约束），但正文未显式声明主从关系，agent 可能在"加个双关语"时越界。建议加一句"Creative devices are allowed only when they don't reduce clarity"。

4. **行内委托与 Related Skills 条目重复（🟢）**: L78 "use the copy-editing skill after your draft" 与 L282 "copy-editing: USE after your first draft is complete" 重复表达同一委托——非矛盾，是冗余，可保留其一。

**其余一致性核验（✅）**:
- 原则 6 "Honest over sensational — Never fabricate statistics or testimonials" ↔ NEG-01/CF-01: 一致 ✅
- Proactive Triggers 第 1 条 "Copy opens with 'We' → Flag immediately" ↔ NEG-02 "Copy does not open with We": 触发→修正闭环 ✅
- Proactive Triggers 第 2/3 条（模糊价值主张、feature 无 benefit）↔ NEG-03: 一致 ✅
- "Primary CTA: 'Start Free Trial' > 'Sign Up'" ↔ CTA 弱名单（Sign Up 在列）: 一致 ✅
- 置信度标记 🟢🟡🔴 ↔ QA-02 "confidence marking": 唯一有文本体系支撑的判据 ✅
- "Meta Content (if relevant)" ↔ FMT-02（完整页面才需要 meta）: 口径一致 ✅
- "Annotations are mandatory" ↔ Communication 第 3 条: 一致 ✅
- Page Structure Framework 的 Main Sections 表（Social Proof/Problem/Solution/How It Works/Objection/Final CTA）↔ Output Artifacts 的 Homepage 交付物清单（headline, subheadline, CTA, social proof, benefits, how it works, objection handling, final CTA）: 一一对应 ✅

### 4.3 模板/示例正确性验证

- 弱/强 CTA 对照（Submit / Sign Up / Learn More / Click Here / Get Started 弱 vs Start Free Trial / Get [Specific Thing] / See [Product] in Action / Create My First [Item] / Download the Guide 强）: 行业标准 ✅
- CTA 公式 "[Action Verb] + [What They Get] + [Qualifier if needed]": 标准 ✅，示例 3 条（"Start My Free Trial"、"Download the Complete Checklist"、"See Pricing for My Team"）质量高 ✅
- Headline 公式 4 个（"{Achieve result} without {pain point}"、"The {category} for {audience}"、"Never {unpleasant event} again"、"{Question highlighting the main pain point}"）: 常见公式库 ✅
- 坏/好示例对比（L87-89）: "Slack allows you to share files instantly, from documents to images, right inside your conversations" ❌ vs "Need to share a screenshot? Send as many documents, images, and audio files as you want." ✅——经典"特性陈述 vs 客户场景"对比，教学价值高 ✅
- Main Sections 表 6 节: 标准落地页结构 ✅
- 5 种页面类型指导（Homepage/Landing/Pricing/Feature/About Us），每类 3 条具体建议: ✅
- 反问句示例（"Hate returning purchases?"、"Tired of chasing approvals?"）: 符合主题 ✅

### 4.4 条件完整性

**正向覆盖**: 5 原则 + 6 风格规则 + 5 页面类型 + CTA 公式 + 5 主动触发 + 5 类交付物 = 26 个指导点，覆盖面在写作类 skill 中领先 ✅

**反向覆盖**: NEG 3 项（编造数据 / We 开头 / 无 benefit 桥）✅。但 DO NOT 风格禁令散落在 Principles（"Honest over sensational"）与 Quick Quality Check（"Exclamation points? (remove them)"），无集中 DO NOT 节——可接受但不如 146 的集中式清晰。

**缺失的条件处理**:
- 上下文缺失时的降级路径（ERR-01 只说"ask if not provided"，未说用户拒绝提供/催促开写时怎么办）
- 伦理边界（用户要求误导性文案、编造 testimonial 时是否拒绝——NEG-01 只禁止编造，未定义 agent 的应对动作）🟡
- 品牌风格指南与本 skill 原则冲突时的优先级
- 多语言/本地化指导
- 字数/篇幅指导

---

## 5. 参考文件审查

### 5.1 引用完整性矩阵

| 源文件 | 引用目标 | 形式 | 存在性 | 用途 |
|--------|----------|------|--------|------|
| SKILL.md L119 | `references/natural-transitions.md` | 行内 "See" | ❌ **不存在** | 自然过渡短语 |
| SKILL.md L141 | `references/copy-frameworks.md` | 行内 "See" | ❌ **不存在** | 详细区块类型与页面模板 |
| SKILL.md L78 | copy-editing（外部技能） | 行内路由 | N/A（外部） | 草稿精修 |
| SKILL.md L279-287 | 8 个外部技能 | Related Skills 表 | N/A（外部） | 协作路由 |
| SCORING SCOPE-02 | `.claude/product-marketing-context.md`（工作区文件） | 判据正则 | 视任务环境而定 | 上下文前置读取 |
| check.py | 同上 | 代码 | 同上 | 同上 |

技能目录内引用: **2 处指向不存在文件**（悬空引用）——经 Glob（目录仅 3 文件命中）+ 正文引用比对双重确认；工作区文件引用属任务约定，非技能资源。

### 5.2 不可见资源（幽灵引用）

- **确认存在不可见资源问题**: 正文承诺的 2 个参考文件不存在，属于"承诺资源缺失"。这是本 skill 最严重的问题——**全语料库 322 个 skill 中罕见的悬空引用案例**（与 154/152/151"引用必存在"的水准形成鲜明落差）。
- 影响链: agent 按正文指示 Read `references/natural-transitions.md` → Read 失败 → (a) 自行发挥补过渡短语（质量漂移）；(b) 跳过该细节（交付缺项）；(c) 询问用户（流程卡顿）。三种结果都偏离技能预设。同时正文 L119/L141 的 "See" 指引成为死指令。
- 推测成因: 该 skill 源 pack 中本有 references/ 素材，规范化/拆分迁移时文件未随正文引用一并拷贝——与项目规范化记录"54 处交叉引用修复"对照，这两处是漏网之鱼。

### 5.3 跨 Skill 引用

- 无 `../other-skill/` 文件路径引用 ✅
- 技能名散文引用 8 处（Related Skills）+ 1 处行内（copy-editing, L78）——规范 §3.3 允许以名称引用；Related Skills 的 "USE for X. NOT for Y" 双句式位置合规 ✅
- **违规点只在 description 的 2 处路由**（email-sequence / popup-cro），正文侧路由全部合规

### 5.4 死文件检查

技能目录内无死文件（仅 3 个文件，全部有职责）。反向的死引用（C1）: 2 个"应存在但不存在"的文件——从死文件审查角度，这是比死文件更需要注意的"幽灵引用"。

---

## 6. 语法与格式质量

### 6.1 拼写

全文未发现拼写错误。术语（copywriting、CTA、ICP、SEO、landing page、About Us）拼写一致 ✅。

### 6.2 语法

- 正文以短句、指令句、断言句为主（广告文案型节奏，符合技能主题）✅
- "Never deliver one option and call it done." 等祈使句为技能正文惯例，合法 ✅
- em dash（—）在全文作为分隔与强调统一使用，风格一致 ✅
- 列表动宾结构统一 ✅

### 6.3 中英混杂

全英文，无混杂 ✅。

### 6.4 Markdown

- 表格 2 张渲染正确（主区块 2 列、Output Artifacts 2 列），管道对齐 ✅
- 无代码块（纯写作型技能，合理）✅
- 加粗、列表语法均正确 ✅
- 占位符使用规范: 公式占位（"{Achieve result} without {pain point}"、"[Action Verb] + [What They Get]"）、备选格式（"Option A: [copy] — [rationale]"）——花括号/方括号包裹清晰，与真实内容无混淆 ✅

**行尾细节（本次审查新增发现）**: 三个文件均为 CRLF 行尾；SKILL.md 末行（"NOT for page or landing page copy."）**无结尾换行符**（wc -l 287 vs 内容行 288）。属无害细节，但 git diff 与 Unix 拼接工具下会产生告警，建议顺手补上。

### 6.5 截断内容

全文结尾完整（Related Skills 以 email-sequence 条目收束），无截断 ✅。

---

## 7. 规范合规 12 项（对照 `_shared/SKILL-SPEC.md` §5）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name: 小写+连字符, ≤64, 匹配目录 | ✅ | `copywriting`，10 字符 |
| 2 | description: 第三人称 + WHAT + WHEN + KEYWORDS + ≤1024 | ✅ | 约 460 字符；WHAT 内嵌于 WHEN 句但语义完整 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | "When the user wants to..." 条件句开头 |
| 4 | description: 无内嵌跨技能路由 | ❌ | "For email copy, see email-sequence. For popup copy, see popup-cro."——明文路由，违反 §2.5 |
| 5 | description: 至少一个触发信号短语 | ⚠️ | "When the user wants to..." / "Also use when the user says..." 为变体句式，语义达标、非 §2.4 标准句式 |
| 6 | frontmatter: 无允许列表之外的键 | ✅ | 仅 name + description |
| 7 | body: ≤600 行 | ✅ | 282 行 |
| 8 | body: 有 workflow/process 节 | ⚠️ | 无显式 Workflow 标题；"Before Writing → 写作 → Output" 为隐式链 |
| 9 | body: 有 output format 节 | ✅ | `## Output Format` + `## Output Artifacts` 双节，语料库最完整 |
| 10 | body: 有 scope/limitations 节 | ⚠️ | Related Skills 的 NOT 句承担协作边界；无技能自身能力边界声明 |
| 11 | body: 无跨 skill 文件引用 | ✅ | 无 `../other-skill/`；悬空的是本地 references（属 §5 问题，不计入本项） |
| 12 | 目录: NNN-kebab-case, 无空格大写 | ✅ | `150-copywriting` |

**合规率**: 8 × 1 + 3 × 0.5 + 1 × 0 = **9.5/12 (79.2%)**——8 项全合规、3 项部分合规（规则 5/8/10）、1 项违规（规则 4，即 dossier 标记项）。

### 违规详情

**违规 1 — description 内嵌跨技能路由（规则 4）**: 见 §2.2。这是本 skill 唯一的 12-item 硬违规，也是 dossier 已标记的问题。

**部分合规 — 触发信号变体句式（规则 5）**: "Also use when the user says..." 含规范 §2.4 的 "use when the user" 子串（变体形式），语义达标但字面部分达标；"When the user wants to..." 不在 §2.4 标准清单中，但属触发语义明确的条件句。修复难度极低（改为 "Use when the user asks to..." 即可）。

---

## 8. 人机感评估

### 8.1 Emoji 审计

- L87-89: ❌/✅ 用于 Slack 例子对照（差例/好例标记）——语义化使用 ✅
- L273: 🟢 strong recommendation / 🟡 test this / 🔴 needs proof to land——置信度标记体系，语义化且被 QA-02 判据引用 ✅
- 其余小节零 emoji ✅

**评价**: 全部 emoji 均为功能性（示例对照 + 置信度体系），非装饰。其中置信度标记是刻意设计——要求 agent 在输出中对每条建议标注 🟢/🟡/🔴。⚠️ 需留意跨 harness 渲染一致性（cursor/plain 输出中 emoji 可能丢失，但 plain 拼接场景不影响语义标记）。

### 8.2 全大写/喊叫式语言

无全大写喊叫。CTA 强弱列表中的 "Submit, Sign Up, Learn More" 为引号枚举，非喊叫 ✅。

### 8.3 Persona 语气分析

- L8: "You are an expert conversion copywriter."——明确 Persona 指令。这是**面向 agent 的角色设定**（正文设定 agent 扮演角色），属于技能设计惯例（role prompting），不是对用户的讨好式人格化 ✅ 合规且贴合写作型技能需求
- **整体语气**: 自信、专业、带教式的资深文案总监口吻

**代表性语句**:
- L42: "If you have to choose between clear and creative, choose clear." — 原则一句话讲透
- L52: "Use the words your customers use." — 客户语言的命令式表达
- L63: "'Use' not 'utilize', 'help' not 'facilitate'" — 具体词对对比
- L275: "Never deliver one option and call it done." — 有态度的收尾，与 CF-02 红线呼应
- L244: "Flag these issues WITHOUT being asked" — 主动性要求明确

**语气适合度**: ✅ 优秀——像资深文案总监带教，每条规则都有理由和例子。

### 8.4 人机边界分析

**优势**:
- L13: "If `.claude/product-marketing-context.md` exists, read it before asking questions"——具体的文件级指令 ✅
- ERR-01 对应"缺信息时先问" ✅
- Proactive Triggers 5 项给 agent 明确干预点（We 开头、价值主张模糊、feature 无 benefit、缺 social proof、弱 CTA 动词）✅
- Related Skills 的 "USE for X. NOT for Y" 双句式路由——8 组边界清晰，如 "copy-editing: ... NOT for writing new copy from scratch"、"email-sequence: USE for email copywriting specifically. NOT for page or landing page copy" ✅ 全语料库系统性使用 NOT 句式的少数 skill 之一

**不足**:
- 无"最终交付需人工确认"步骤（文案发布前品牌方审阅）
- 无伦理边界（误导性文案/编造 testimonial 的拒绝机制——NEG-01 只禁止编造，未定义应对动作）🟡
- 无"何时停下问用户"的交互点（上下文缺失但用户催促时）

### 8.5 人称分析

- description 第三人称 ✅
- 正文指令体 + agent 角色句（"You are..."）——面向 agent 的扮演指令，符合技能惯例 ✅
- 无对用户的第二人称讨好式表述 ✅

### 8.6 表格使用评估

- 2 张表（主区块用途、Output Artifacts 对照）均承载决策/映射信息，是最优格式 ✅
- 页面类型（5 类）用分节而非表格——信息量与粒度合适，不算缺陷 ✅
- 信息密度高但节奏良好 ✅

---

## 9. 可执行性评估

### 9.1 独立可执行性: 8/10

1. **入口**: description 双段触发（场景 + 用户原话）是全语料库少见的强触发设计——但 2 句路由混在其中稀释了触发纯度（§13 🟡-1 修复后触发更聚焦）
2. **上下文采集**: Before Writing 的 4 组问题清单（页面目的/受众/产品/流量）可直接照问；`.claude/product-marketing-context.md` 前置读取约定明确 ✅
3. **写作执行**: 五原则 + 六规则 + 质检清单（5 问）为写作过程提供即时自检 ✅；Proactive Triggers 5 项让 agent 主动标记问题 ✅
4. **交付**: Output Format（结构/标注/备选/meta）+ Output Artifacts（按请求类型的交付物对照表）闭环——交付形态定义最明确的写作类 skill ✅
5. **破坏点**: 🔴 两处悬空引用——agent 在 Above the Fold 与主区块处按指示去读不存在的文件。若 agent 是"严格按文档执行"型，会在交付前卡住；若 agent 是"跳过并发挥"型，会产出与技能设计不符的过渡短语/框架内容
6. **协作链**: Related Skills 8 技能路由（USE/NOT）可执行性好，前提是这些技能在评测环境中真实存在（跨技能依赖，任务设计时需确保）

### 9.2 步骤可操作性

| 元素 | 可操作性 | 评估 |
|------|:--------:|------|
| Before Writing | 🟢 | 4 组问题清单可直接照问 |
| 原则 + 风格规则 | 🟢 | 5+6 条全部可执行，词对示例具体 |
| 页面框架 | 🟢 | 结构明确，公式库 4 个 |
| CTA 公式 | 🟢 | 公式 + 正反例 |
| Output Format | 🟢 | 交付物结构完整 |
| references 引用 | 🔴 | 2 处悬空，agent 读取必失败 |

### 9.3 可执行性盲点

- 悬空引用使 "natural transitions" 与 "section types" 两个环节成为死指令
- 无降级路径（用户拒绝提供上下文时怎么办——ERR-01 只说问，没说不给时的回退）
- meta content 的 SEO 具体性不足（只提 page title/meta description，未给长度/格式规范）
- PROC-03 脚本判定（见 §10.4）对"仅 headline 变体"类子任务有误判风险

---

## 10. SCORING.yaml 交叉参考

### 10.1 结构核查

- `total_items: 19` ✅ 实际 19（SCOPE 3 + PROC 7 + FMT 3 + NEG 3 + QA 2 + ERR 1），计数正确
- `pattern: workflow` ✅ 与 Skill 类型一致
- judge 分布: script 4 / llm 15——llm 占比 79%，写作文本类技能的合理选择（主观质量判定多，机械断言少）
- critical_failures: 3 个 cap_to_0 ✅
- `check.py` 头注释 "Run all 4 script checks" ✅ 实际返回 4 项（SCOPE-02、PROC-03、PROC-07、FMT-01），注释与实际一致

### 10.2 检查项 ↔ SKILL.md 全量映射

| 检查项 | SKILL.md 落点 | 一致性 |
|--------|---------------|:------:|
| SCOPE-01 | description 页面类型枚举（homepage/landing/pricing/feature/about） | ✅ |
| SCOPE-02 | L13 "If `.claude/product-marketing-context.md` exists, read it..." | ✅ 脚本正则与正文字面匹配 |
| SCOPE-03 | Before Writing 4 组问题（页面目的+主行动/受众/产品/流量） | ✅ |
| PROC-01 | Copywriting Principles 5 条 | ✅ |
| PROC-02 | Writing Style Rules 6 条 | ✅ |
| PROC-03 | Output Format 的 Page Copy 结构（Headline/Subheadline/CTA 等） | ⚠️ 见 10.4 |
| PROC-04 | CTA Copy Guidelines 强弱对照 + 公式 | ✅ |
| PROC-05 | Page-Specific Guidance 5 类页面 | ✅ |
| PROC-06 | Voice and Tone 节 | ✅ |
| PROC-07 | Output Format 的 Alternatives 节（"Option A: ... — rationale"） | ✅ 脚本正则与正文格式字面匹配 |
| FMT-01 | Output Format 的 Headline 结构 | ✅ |
| FMT-02 | Output Format 的 Meta Content 项（"(if relevant)" 口径一致） | ✅ |
| FMT-03 | Output Artifacts 表 5 类请求 | ✅ 与 5/3-5 版本一致（但见 §4.2-1 数值矛盾） |
| NEG-01 | Style Rules 第 6 条 "Never fabricate statistics or testimonials" | ✅ |
| NEG-02 | Proactive Triggers 第 1 条 | ✅ |
| NEG-03 | Proactive Triggers 第 2/3 条 | ✅ |
| QA-01 | Proactive Triggers 全节 5 项 | ✅ |
| QA-02 | Communication 节 4 项（含置信度 🟢🟡🔴） | ✅ |
| ERR-01 | Before Writing 采集逻辑（"ask if not provided"） | ✅ |

**19/19 全部可追溯到 SKILL.md 原文**，无凭空检查项。SCORING 设计与正文的匹配度为语料库前列。

### 10.3 脚本检查细节

| Criterion | 检查模式 (check.py) | SKILL.md 对应文本 | 一致性 |
|-----------|--------------------|------------------|:------:|
| SCOPE-02 | `tool_log_contains('product-marketing-context\\.md')` | L13 上下文文件约定 | ✅ |
| PROC-03 | `output_contains("Subheadline")` | L121-124 Subheadline 小节 + L258 交付物 | ✅ 字面匹配 |
| PROC-07 | `output_contains("Option A")` | L233-234 "Option A: [copy] — [rationale]" | ✅ 字面匹配 |
| FMT-01 | `output_contains("Headline")` | L108-117 Headline 小节 | ✅ 字面匹配 |

### 10.4 评分架构观察（含一个设计缺陷）

- **PROC-03 的条件化问题（🟡）**: 脚本无条件要求输出含 "Subheadline"，但 Output Artifacts 表明确定义了"Headline options"与"CTA copy"两类子任务——此类交付物天然不含 Subheadline 一词。对"只写 5 条 headline 变体"或"写 3-5 个 CTA"的合法子任务，PROC-03 会误判失败（假阳性）。FMT-03 承认交付物随请求类型而变，PROC-03 却不带条件——**评测层内部口径不一致**。修复: PROC-03 改 llm judge，或脚本加条件（任务为完整页面时才要求 Subheadline），或换一个所有交付类型都含的词（如 "CTA"）。
- FMT-01 "Headline" 检查无此问题（headline 变体任务也含 "Headline"）✅
- SCOPE-02 依赖工作区存在 `.claude/product-marketing-context.md`——若任务环境不提供该文件，判据无法通过。设计上合理（测的是"有文件就读取"的行为），但任务设计者需知悉
- 无判据检查"是否读取了 references 文件"——若按 🔴-1 方案 A 补建参考文件，建议加一条 tool_log 判据对应（参照 154 的 FMT-02 模式）

### 10.5 Critical Failures 分析

- CF-01（编造 statistics/testimonials/proof points → cap 0）: 对应 Style Rule 6 "Never fabricate" ✅
- CF-02（单一 headline/CTA 选项、无备选无标注 → cap 0）: 对应 Communication "Always provide alternatives... Never deliver one option and call it done" ✅
- CF-03（feature 堆砌无 benefit / "We" 开头不修正 → cap 0）: 对应 NEG-02/03 + Proactive Triggers 1/3 条 ✅

三个 CF 全部与正文规则一一咬合，设置恰当。

---

## 11. 已知问题验证（来自 skill-dossier.md）

### Dossier 记录

> **148-signup-flow-cro — 150-copywriting**: "逻辑: ...150 写作原则与输出物表相互印证。语法: 均规范流畅。人机感: 150 结论先行沟通到位。合规: 🟡 description 中内嵌跨技能路由（违反 §2.5），需移入正文。"

### 逐项验证

| Dossier 记载 | 本次审查验证 | 状态 |
|-------------|------------|:----:|
| 写作原则与输出物表相互印证 | 5 条原则 ↔ Output Artifacts 5 类交付物大体对应（Benefits→Solution/Benefits 区块、Specificity→headline 公式变体、One Idea Per Section→按区块组织）——**大体成立**，但发现一处例外：Output Format 说 "2-3 options"、Output Artifacts 表说 "5 headline variants / 3-5 CTA options"（§4.2-1），数值不印证 | ⚠️ 大体确认 + 一处例外 |
| 语法规范流畅 | 全文无拼写/语法错误，Markdown 干净 | ✅ 确认 |
| 结论先行沟通到位 | Communication 节 4 条模式（结论先行 / What+Why+How / 标注强制 / 置信度）明确，QA-02 有文本体系支撑 | ✅ 确认 |
| description 中内嵌跨技能路由 | L3 "For email copy, see email-sequence. For popup copy, see popup-cro." **仍存在**，12-item 规则 4 失败 | ❌ 确认仍存在 |

### Dossier 未记载的新问题（本次审查发现）

1. 🔴 **两处悬空引用**（references/natural-transitions.md、references/copy-frameworks.md）——正文承诺不存在的文件，Glob + 引用比对双重确认。这是本 skill 最严重的问题，dossier 未记载
2. 🟡 **变体数量矛盾**（2-3 vs 5 vs 3-5）——Output Format 与 Output Artifacts 两节数值打架，SCORING FMT-03 站在 Output Artifacts 一边（§4.2-1）
3. 🟡 **description ↔ Related Skills 路由对象不一致**——description 路由到 popup-cro，正文 Related Skills 列表无 popup-cro 条目（§4.2-2）
4. 🟡 **PROC-03 无条件 "Subheadline" 判定**——与 Output Artifacts 的子任务类型冲突，对 headline-only 任务误判（§10.4）
5. 🟢 触发信号为变体句式、无显式 Workflow 标题、无自身能力边界声明
6. 🟢 CRLF + 末行无换行符细节

**综合评级**: 维持 🟡 但问题清单扩容——dossier 记了 2 项，本次审查实查 8 项（1 红 + 3 黄 + 4 绿）。**dossier 需在下次审查中更新该条目**（追加"🔴 references 双悬空引用"）。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 6/10 | 10% | 0.60 | description 内嵌路由（12-item 唯一硬违规）+ 触发信号变体句式 |
| Body 结构完整 | 8/10 | 10% | 0.80 | 13 节丰富自洽，Output 双节语料库最佳；Workflow 隐含、Scope 部分 |
| 逻辑一致性 | 7.5/10 | 20% | 1.50 | 原则↔输出物表大体互证（dossier 确认）；变体数矛盾 + popup-cro 不一致 |
| 参考完整性 | 6/10 | 15% | 0.90 | **2 处悬空引用**——正文承诺不存在的文件，全语料库罕见 |
| 语法格式 | 9/10 | 10% | 0.90 | 规范流畅，零错字；CRLF + 末行无换行为无害细节 |
| 规范合规 | 7/10 | 15% | 1.05 | 9.5/12（8 全合规 + 3 部分 + 1 违规） |
| 人机感 | 9/10 | 10% | 0.90 | 带教式文案总监语气 + 置信度标记体系 + USE/NOT 路由 |
| 可执行性 | 8/10 | 10% | 0.80 | 上下文→写作→交付→协作闭环完整、Output 定义最佳；悬空引用打断执行流 |
| **加权总分** | | | **7.45/10** | **74.5 ≈ 75/100** |

计算: 0.10×6 + 0.10×8 + 0.20×7.5 + 0.15×6 + 0.10×9 + 0.15×7 + 0.10×9 + 0.10×8 = 7.45

### 12.2 评级

🟡 **B (75/100)**: 内容质量在写作类 skill 中属于优秀（13 节信息量大、交付定义最完整、触发设计最强），但 2 处悬空引用（参考完整性 6.0）与 description 路由违规（合规 7.0）构成实质性扣分。若 🔴-1 与 🟡-1 修复，预计回升至 85+。

### 12.3 与同族对比

写作族 skill（298-writing-skills、024-content-creator、038-content-production 等）中，150 的差异化定位清晰：专精"web 页面营销文案"，与内容策略、社交分发、邮件序列等相邻技能划清边界（Related Skills 的 USE/NOT 双句式）。与同批审查的 146 相比：146 参考完整性 10/10、150 仅 6/10——**146 是"完全自包含"的正面教材，150 是"委托未兑现"的反面教材**，两者对照鲜明。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**🔴-1 两处悬空引用: references/natural-transitions.md 与 references/copy-frameworks.md**
- **定位**: SKILL.md L119 "**For natural transition phrases**: See references/natural-transitions.md"、L141 "**For detailed section types and page templates**: See references/copy-frameworks.md"——目录中无 references/，两个文件均不存在（Glob 双重确认）
- **修复（二选一，推荐方案 A）**:
  - **方案 A（补建文件）**: 创建 `references/natural-transitions.md`（自然过渡短语: 从价值主张→痛点、痛点→解决方案、解决方案→社会证明的桥接短语清单，各 10-15 例，含上下文与语气标注）与 `references/copy-frameworks.md`（主区块详细类型定义: Social Proof / Problem-Pain / Solution-Benefits / How It Works / Objection Handling / Final CTA 每类 2-3 个页面模板 + 区块写作要点，承接正文 L132-139 表格的扩展）。两份文件均为 80-120 行的素材型文档，正文无需改动，只补建即可闭合
  - **方案 B（删引用内联）**: 删除 L119 与 L141 两行，将过渡短语公式与区块模板要点直接内联进正文相应小节（正文预计 282 → 330 行，仍 < 600）
- **后果（若不修）**: agent 执行时 Read 失败——严格执行型 agent 流程中断（询问/停滞），弹性 agent 自行发挥导致交付漂移；任何"链接完整性"类静态检查直接判负；与语料库"引用必存在"的水准形成明显落差，拖累整体评测一致性
- **工作量**: 方案 A 约 40-60 分钟（2 个新文件）；方案 B 约 15 分钟

### 🟡 重要缺陷（建议修复）

**🟡-1 description 内嵌跨技能路由移入正文**
- **定位**: SKILL.md L3 "For email copy, see email-sequence. For popup copy, see popup-cro."
- **修复**: 从 description 删除该两句；将 email-sequence 与 popup-cro 的 USE/NOT 路由句补入 `## Related Skills`（email-sequence 已有条目，补 popup-cro 新条目: "**popup-cro**: USE for popup copy conversion optimization. NOT for page or email copy."——顺带修复 §4.2-2 的"路由对象与正文清单不一致"）。同时将 description 改以标准触发句式收尾（"Use when the user wants to write, rewrite, or improve marketing copy..."，顺带修复第 5 项 ⚠️）
- **后果（若不修）**: 12-item 第 4 项持续失败；路由语义与正文清单不一致持续；description 承担路由职责使触发匹配被稀释（"For email copy" 与 "write copy for" 两类意图混淆）
- **工作量**: description 2 句删除 + Related Skills 1 条目新增，约 5 分钟

**🟡-2 统一变体数量（2-3 vs 5 vs 3-5）**
- **定位**: L230（Alternatives "2-3 options"）vs L259-260（Output Artifacts "5 headline variants" / "3-5 CTA options"）
- **修复**: 统一为 "3-5 options"（对齐 Output Artifacts 与 SCORING FMT-03）；Alternatives 节示例扩为 Option A/B/C 三行
- **后果（若不修）**: agent 按任一版本交付都可能被 FMT-03 的 llm 判定认为"备选数不符"；内部口径不一致会让评测结果依赖 judge 的随机取信版本

**🟡-3 补建正文自身的 Scope 小节**
- **定位**: 无 `## Scope & Limitations`；Related Skills 只覆盖"协作边界"，不覆盖"能力边界"
- **修复**: 新增 `## Scope & Limitations`（可放在 Communication 之后）: "本技能输出页面文案与标注，不制定品牌策略、不进行视觉/排版设计、不生成图片、不做 A/B 实验设计（见 ab-test-setup）"；并注明 "相关参考素材见 references/ 两文件"（与 🔴-1 联动）；补充伦理边界: "Refuse to fabricate proof or write deliberately misleading copy."
- **后果（若不修）**: 12-item 第 10 项持续部分达标；agent 对跨界请求（"顺便帮我设计个 banner"）缺拒绝依据
- **工作量**: 8-10 行

**🟡-4 补显式 Workflow 节**
- **定位**: 隐式流程链无标题编排
- **修复**: 新增 `## Workflow` 5 步: 1. 读取 `.claude/product-marketing-context.md`（存在时）→ 2. 按 Before Writing 四组问题补齐上下文（缺则追问，ERR-01 依据）→ 3. 确立 Voice and Tone → 4. 按 Page Structure Framework + 页面类型写作，逐节应用 Proactive Triggers 自查 → 5. 按 Output Format/Output Artifacts 交付（备选 + 标注 + 置信度）。每步给对应小节指针
- **后果（若不修）**: 12-item 第 8 项持续部分达标；执行顺序靠 agent 推断
- **工作量**: 约 15 行

**🟡-5 PROC-03 脚本判定条件化**
- **定位**: check.py PROC-03 `output_contains("Subheadline")` 无条件要求
- **修复**: 改 llm judge，或脚本加条件（仅当任务为完整页面时要求 Subheadline），或改用所有交付类型都含的词（如 "CTA"）
- **后果（若不修）**: "只写 headline 变体/CTA 文案"的合法子任务被脚本误判失败，污染 Mode A/B 对比数据

### 🟢 优化建议（锦上添花）

| # | 建议 | 定位 | 工作量 | 收益 |
|---|------|------|--------|------|
| 🟢-1 | description 触发信号改为规范标准句式 "Use when the user wants to..."（与 🟡-1 合并改） | SKILL.md L3 | 1 行 | 第 5 项全达标 |
| 🟢-2 | Related Skills 由列表改表格（Skill / When to use / When NOT to use 三列），路由信息更紧凑 | SKILL.md L279-287 | 低 | 可读性 |
| 🟢-3 | 补建参考文件后（🔴-1 方案 A），SCORING 增加 1 条 tool_log 判据检查 agent 读取了 references 文件（参照 154 的 FMT-02 模式） | SCORING.yaml | 2 行 | 强制素材使用 |
| 🟢-4 | Before Writing 的 (a) 分支补一句"文件不存在时直接进入提问清单" | SKILL.md L13 | 1 行 | 执行缺口闭合 |
| 🟢-5 | L78 行内 copy-editing 路由与 Related Skills 条目保留其一，避免重复 | SKILL.md L78 | 1 行 | 减冗余 |
| 🟢-6 | 补末尾换行符 + 统一 LF | 全部文件 | 低 | git diff 友好度 |

### 修复工作量估计
- 🔴 1 项: 方案 A 约 40-60 分钟（2 个新文件）或方案 B 约 15 分钟
- 🟡 5 项: 约 30 行 + check.py 1 处
- 合计约 1-2 小时，修复后预期评分 85-88

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md — 288 行内容，全文精读（含 13 节逐节分析 + 2 处引用行核验）
2. SCORING.yaml — 175 行，全文（19 criteria + 3 critical_failures）
3. check.py — 79 行，全文（4 项 script check）
4. _shared/SKILL-SPEC.md — 161 行，全文（合规依据）
5. skill-dossier.md — 148/150 相关条目（已知问题对照）

### 读取统计
- 总文件数: 5（3 skill 文件 + 1 规范 + 1 dossier 摘录）
- 总行数: 约 710 行

### 审查方法
- 所有文件全文阅读，未使用抽样 ✅
- 悬空引用双重确认: Glob（仅 3 文件命中）+ 正文引用比对
- 字节级验证: 末行换行符（tail -c）、行尾风格（grep -c $'\r'）
- 数值一致性: Output Format Alternatives vs Output Artifacts vs SCORING FMT-03（发现 2-3/5/3-5 三方矛盾）
- 交叉验证: SKILL.md ↔ SCORING.yaml ↔ check.py ↔ SKILL-SPEC.md v1.0 ↔ skill-dossier.md
- 家族对比: 146（同批审查，自包含正面教材）与写作族其他 skill

### 审查人
Claude (SkillIF quality audit) — 2026-08-06

### 审查备注
本 skill 是写作类中"内容优秀但引用失信"的典型案例：13 节正文信息量大且自洽，触发设计与交付定义是语料库最强之一，Related Skills 的 USE/NOT 双句式值得推广；但 2 处悬空引用（正文承诺不存在的 references 文件）是全语料库罕见的硬伤，会直接打断 agent 执行流。dossier 标记的"description 内嵌路由"确认仍存在；"写作原则与输出物表相互印证"大体成立，但审查新发现一处数值矛盾（2-3 vs 5 vs 3-5 变体数）使印证不完整。另发现 PROC-03 脚本判定对 headline-only 子任务存在误判风险——该问题若带入评测，会直接污染 Mode A/B 对比数据，建议优先于正文问题处理。修复路径清晰（补建/删除引用 + 路由移正文 + 数值统一），修复后此 skill 可作为写作类 workflow 型的参考标准。
