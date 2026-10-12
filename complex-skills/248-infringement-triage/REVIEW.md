# REVIEW: 248-infringement-triage

**审查日期**: 2026-08-06 | **审查人**: Claude (SkillIF quality auditor)
**审查范围**: 全目录 14 个文件逐一全文读取 —— SKILL.md (517 行)、SCORING.yaml (159 行)、check.py (69 行)、references/ 12 个文件（合计约 117 行）
**对照基准**: D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md v1.0、_shared/CHECKER-LIBRARY.md、_shared/checker.py、memory/skill-dossier.md（Batch 226-250 摘要）

---

## 1. Directory Full Inventory

| # | 文件 | 行数/大小 | 类型 | 审查状态 |
|---|------|----------|------|---------|
| 1 | `SKILL.md` | 517 行 | 主体 | ✅ 全文读取 |
| 2 | `SCORING.yaml` | 159 行 | 评分标准 | ✅ 全文读取 |
| 3 | `check.py` | 69 行 | 评测脚本 | ✅ 全文读取 + 行为仿真验证 |
| 4 | `references/citation-verification.md` | 9 行 | 引用 | ✅ 全文读取 |
| 5 | `references/close-with-the-next-steps-decision-tree.md` | 3 行 | 引用 | ✅ 全文读取 |
| 6 | `references/defenses-and-thresholds.md` | 5 行 | 引用 | ✅ 全文读取 |
| 7 | `references/factor-analysis.md` | 5 行 | 引用 | ✅ 全文读取 |
| 8 | `references/handoff-to-enforcement-skills.md` | 17 行 | 引用 | ✅ 全文读取 |
| 9 | `references/non-lawyer-gate.md` | 24 行 | 引用 | ✅ 全文读取 |
| 10 | `references/output-location.md` | 11 行 | 引用 | ✅ 全文读取 |
| 11 | `references/posture-and-scope.md` | 7 行 | 引用 | ✅ 全文读取 |
| 12 | `references/recommended-next-steps.md` | 8 行 | 引用 | ✅ 全文读取 |
| 13 | `references/tone.md` | 7 行 | 引用 | ✅ 全文读取 |
| 14 | `references/what-cuts-which-way-summary.md` | 10 行 | 引用 | ✅ 全文读取 |
| 15 | `references/what-this-skill-does-not-do.md` | 16 行 | 引用 | ✅ 全文读取 |

**子目录检查**:

| 子目录 | 是否存在 | 内容 | 备注 |
|--------|:-------:|------|------|
| `references/` | ✅ 存在 | 12 个引用文件 | 本技能内容委托的主要载体 |
| `scripts/` | ❌ 不存在 | — | — |
| `assets/` | ❌ 不存在 | — | — |
| `docs/` | ❌ 不存在 | — | — |
| `examples/` | ❌ 不存在 | — | 示例内联在 SKILL.md `## Examples` 节 |

**要点**: 本技能是 claude-for-legal 插件生态的深度集成组件（模式与 017-cease-desist、028-subpoena-triage 同族）。全部输出路径、实践档案、matter 工作区、角色配置均指向插件外部环境（`~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`），技能内部零硬编码输出路径（除 Output format 节引用 reference 文件外）。12 个 reference 文件中 **5 个为占位模板骨架**（见 §5），内容深度集中在 SKILL.md 主体。

---

## 2. Frontmatter Field-by-Field Review

### 2.1 原始 Frontmatter

```yaml
---
name: infringement-triage
description: Infringement triage across trademark, copyright, patent, and trade secret — a flag list with the factors cutting each way, not a finding. Use when assessing whether someone is infringing your IP or whether you might be infringing theirs, when a knockoff or copycat surfaces, or when deciding whether a matter is worth pursuing and how.
argument-hint: "[describe the facts and which right — or just the facts and I'll ask which right]"
---
```

### 2.2 `name` 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 小写 + 连字符 | ✅ | `infringement-triage`，符合 kebab-case |
| ≤64 字符 | ✅ | 19 字符 |
| 与目录名匹配 | ✅ | 目录 `248-infringement-triage`，序列号前缀 NNN- 后与 name 完全一致 |

### 2.3 `description` 字段逐句分析

**句子 1**: "Infringement triage across trademark, copyright, patent, and trade secret — a flag list with the factors cutting each way, not a finding."

- WHAT 部分。声明四大权利类型（商标/版权/专利/商业秘密）全覆盖，并**在 description 层直接嵌入核心边界**："a flag list ... not a finding"——把技能最重要的护栏前置到触发描述里，可在意图匹配阶段就与"法律意见书/起诉状起草"类技能区分开。这是全 corpus description 中少见的边界前置设计，值得表扬。
- 第三人称 ✅，无祈使 ✅。

**句子 2**: "Use when assessing whether someone is infringing your IP or whether you might be infringing theirs, when a knockoff or copycat surfaces, or when deciding whether a matter is worth pursuing and how."

- WHEN 部分。三个触发场景：① 评估"他人在侵权我方"（senior 侧）；② 评估"我方可能侵权他人"（accused 侧）；③ 山寨品/仿冒品浮出水面或决定是否值得追诉。**双姿态（senior/accused）对称触发是法律分诊类技能的正确设计**——触发面覆盖了纠纷的两侧，与 017 的双模式设计异曲同工。
- 触发短语检查（规范 §2.4）：五个规范形式为 "Use when the user..."、"Use when the user asks to..."、"Use when the user needs to..."、"Triggers on..."、"Use for..."。本句为 "Use when assessing..."——以 "Use when" + 动名词开头，**不属于五个规范形式的字面任一种**，属 "Use when" 家族的变体。与 017-cease-desist 相同的灰区，按 corpus 先例（dossier Batch 001-025 对 017 的判定）宽口径通过。
- 人称检查（规范 §2.3）：`your IP`、`infringing theirs` 为第二人称物主代词。与 017 的 `your rights` 同类灰区——描述的是技能服务场景而非对用户发令，但规范字面禁止第二人称。**建议打磨**。
- KEYWORDS 检查：infringement / trademark / copyright / patent / trade secret / knockoff / copycat / triage——领域词充分且具体 ✅。
- 长度：约 292 字符，≤1024 ✅。
- 无跨技能路由（规范 §2.5）✅。
- 无泛化/过短问题 ✅（对比 corpus 中 "A useful skill" 类反例）。

**description 综合判定**: 结构（WHAT + WHEN + KEYWORDS）完整，四权利覆盖 + 双姿态触发 + 边界前置为亮点。仅两处灰区（第二人称、"Use when" 家族变体）。**评级: 🟢（附 2 个可选润色项）**

### 2.4 `argument-hint` 字段

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| 是否允许字段 | ✅ | 规范 §1.2 允许列表内 |
| 内容合理性 | ✅ | `[describe the facts and which right — or just the facts and I'll ask which right]` 与 body 行为一致——Example 3（无参数调用）即对应 "just the facts and I'll ask which right" 分支 |
| 格式 | ✅ | 双引号包裹的普通字符串，YAML 解析无问题（内含破折号/撇号无未转义问题） |

### 2.5 其他字段检查

- `allowed-tools`、`user-invocable`、`model`、`paths`、`disable-model-invocation`: 均未声明（可选字段，缺省合规 ✅）。
- 禁止字段检查（规范 §1.3 清单逐项核对）：metadata / license / version / agents / source / risk / date_added / category / compatibility / tags / author / domain / bundle / contributors / created / updated / dependencies / difficulty / frequency / time-saved / estimatedTime / displayName / color / featured / orchestrated-by / related-skills / related-commands / related-agents / subdomain / tech-stack / python-tools / tools / trigger / triggers / use-cases / verified / title / stats / skills —— **全部未出现** ✅。

### 2.6 YAML 语法检查

- 三个字段全部为标量值，description 为双引号包裹字符串，内含 em dash（—）与撇号（I'll）无转义问题 ✅。
- 无缩进错误、无制表符、无重复键 ✅。
- 可被标准 YAML 解析器正确解析 ✅。

---

## 3. Body Section-by-Section Analysis

### 3.1 段落/章节清单

| # | 行号 | 章节 | 类型 | 功能 |
|---|------|------|------|------|
| 1 | 9-14 | 开头护栏块 | 风险声明 | 3 行超浓缩版 "triage not finding" + 后果列举 |
| 2 | 17-45 | `## Instructions` | 执行指令 | 8 条编号指令（读档案 → 工作流 → 问权利 → 通用 intake → 模式因素 → flag 清单 → 写备忘录 → 收尾交接）|
| 3 | 48-62 | `## Examples` | 示例 | 3 条 slash command（商标/商业秘密/无参数）|
| 4 | 67-87 | `## THIS IS A TRIAGE, NOT A FINDING` | **Loudest Guardrail 节** | 护栏全文 + one-way door / two-way door 不对称风险框架 |
| 5 | 91-97 | `## Matter context` | 上下文 | matter 工作区开关逻辑 |
| 6 | 102-132 | `## Load the practice profile first` | 前置加载 | 档案 5 节映射 + [PLACEHOLDER] 弹跳 + `### Provisional mode` |
| 7 | 136-156 | `## Mode selection` | 模式分发 | 五选一提问 + 混合权利须分开跑 |
| 8 | 160-176 | `## Intake (common to all modes)` | 通用收案 | 姿态/管辖/时效/证据四项 + "Wait for the answer" |
| 9 | 180-229 | `## Trademark mode` | **模式工作流 1** | Confusion（8 因素）/ Dilution（TDRA）/ False advertising / Output |
| 10 | 233-290 | `## Copyright mode` | **模式工作流 2** | Ownership / Registration / Access+similarity / Fair use / DMCA §512 / Output |
| 11 | 294-425 | `## Patent mode` | **模式工作流 3** | D/RE/PP 前缀分支 → Design patent 全节 → Utility workflow → Output → Handoff |
| 12 | 429-481 | `## Trade secret mode` | **模式工作流 4** | Secret / Measures / Misappropriation / Preemption / Output |
| 13 | 485-517 | `## Output format (all modes)` | 输出格式 | work-product 头 + GREEN/YELLOW/RED + 12 个 Reference Files 清单 |

### 3.2 必需章节检查（规范 §3.1）

| 必需节 | 对应章节 | 是否满足 | 说明 |
|--------|---------|:--------:|------|
| Workflow / Process | `## Instructions` + 四模式工作流节 | ✅ | 每个模式有明确因素清单、测试引用、输出子节；混合权利分跑规则明确 |
| Output Format | `## Output format (all modes)` + 6 个输出型 reference 模板 | ✅ | 输出结构 + 12 个引用文件全部列出 |
| Scope / Limitations | `## THIS IS A TRIAGE, NOT A FINDING`（主体内） + `references/what-this-skill-does-not-do.md` | ✅ | 主体内护栏节承担 Scope 职责（"never concludes"），边界清单委托给 reference 文件 |

**发现 3.2-1（🟢 minor）**: 本技能主体没有独立的 `## What this skill does not do` 章节（对比 017 主体内联 6 条不做清单）；Scope 声明分散为：(a) 护栏节（结论边界）、(b) reference 文件 what-this-skill-does-not-do.md（6 条不做清单）。dossier 判定"三节齐全"成立——护栏节即为事实上的 scope 节——但若严格按规范 §3.1"body 必须有 scope/limitations 节"字面执行，主体内无同名章节是个可辩护性弱点。建议在 Output format 节前加一行内联的 Scope 小节或在护栏节补充边界列表。

### 3.3 内容委托分析

- 本技能是**重度委托型**：12 个 reference 文件构成输出结构的模板层。SKILL.md 的 `## Output format (all modes)` 节只给出护栏模板与 GREEN/YELLOW/RED 结果行，其余结构（posture/scope 块、factor analysis、defenses、what-cuts-which-way 表、next-steps 决策树、non-lawyer gate、output location）全部委托给 reference 文件。
- 委托对象分为三类（详见 §5）：实质内容型（citation-verification、non-lawyer-gate、handoff、what-this-skill-does-not-do、output-location、tone）、占位模板骨架型（defenses-and-thresholds、factor-analysis、posture-and-scope、recommended-next-steps、what-cuts-which-way-summary）、纯指针型（close-with-the-next-steps-decision-tree）。
- 跨技能引用全部为名称引用（规范 §3.3 合规）：`/ip-legal:fto-triage`、`/ip-legal:cease-desist`、`/ip-legal:takedown`、`/ip-legal:cold-start-interview`、`/ip-legal:matter-workspace`、`/litigation-legal:claim-chart`、`clearance`、`fto-triage`。**命名前缀不一致**（见发现 4.3-1）。
- 无 `../other-skill/` 形式路径 ✅。

### 3.4 节编号 / 标题层级检查

- H1 → H2（模式/流程节）→ H3（模式内因素小节）层级一致，无跳级 ✅。
- 标题命名风格统一：模式节用 `## XXX mode`，因素小节用 `###` 名词短语 ✅。
- 唯一的层级小瑕疵：`## Output format (all modes)` 与其上方的 `### Output`（每个模式内）重名——模式内 `### Output` 是"该模式输出要点"，全局 `## Output format` 是"统一输出模板"，语义可分但字面易混。纯文体问题。

---

## 4. Logical Consistency

### 4.1 步骤衔接分析（总流程）

| 步骤 | 输入 | 输出 | 下游衔接 |
|------|------|------|---------|
| Instructions 1: 读实践档案 | 档案路径 | Role/Posture/Jurisdiction/Integrations | → 2 若有 [PLACEHOLDER] 停止弹跳 |
| Instructions 3: 问权利 | 用户回答 | 模式选择（五选一/混合） | → 4 或直接进入对应模式节 |
| Instructions 4: 通用 intake | 用户回答 | 姿态/管辖/时效/证据四要素 | → 5 因素走查（Wait for the answer 硬性等待）|
| Instructions 5: 模式因素 | 四要素 + 档案 | 各模式因素 flag | → 6 |
| Instructions 6: flag 清单 | 因素分析 | 双向 flag + 混合项 | → 7 绝不结论 |
| Instructions 7: 写备忘录 | flag 清单 | matter 文件夹/输出文件夹 triage memo | → 8 |
| Instructions 8: 收尾 | memo | next steps + non-lawyer gate + C&D/takedown 提议（不自动起草）| 结束 |

衔接质量：链条完整闭环，intake → 因素 → flag → memo → 交接无断链 ✅。`This skill never concludes`（L45）与 Instructions 6、护栏节、OUT 模板结论行四处呼应，是全技能最一致的元素。

### 4.2 四模式内部衔接

| 模式 | 因素清单 | 输出 | 与 SCORING 对应 |
|------|---------|------|:--------------:|
| Trademark | 8 因素混淆测试 + TDRA 淡化 + §43(a) 虚假广告 | Factors table + not-a-finding 行 + 路由建议 | PROC-03 ✅ |
| Copyright | Ownership / §411 / Access+similarity / §107 四因素 / §512 | flag 清单 + fair-use 平衡 + 门槛注记 | PROC-04 ✅ |
| Patent | D/RE/PP 分支 → Design（ordinary observer）→ Utility（claim chart 首轮）| claim charts + defense flags + 路由 | PROC-05/PROC-06 ✅ |
| Trade secret | DTSA/UTSA 三要素 + 措施清单 + 盗用 + preemption | 三组 flag（secrecy/measures/misappropriation）| PROC-07 ✅ |

Patent 模式内部有一个非常完整的嵌套决策树：**注册号前缀检查（D/RE/PP）→ 分支 → 回退到 utility 工作流**，且分支在 workflow 之前强制执行（"Check the asserted patent's registration number FIRST"、"If the D-number branch above applies, stop here"）。这是全 corpus 中少数把"前置类型判别"做成硬分支的技能，与 028 的 grand-jury stop rule 同类防御性设计。

### 4.3 内部矛盾扫描

| 检查点 | 位置 | 结果 |
|--------|------|:----:|
| 混合权利处理 | Instructions 3 vs Mode selection | ✅ 两处一致："If mixed, run each separately; do not blend" / "Don't mash them together" |
| 护栏措辞 | L9-14 vs L72-81 vs L494-499 | ✅ 三处同源同义（"triage, not a finding"），详略不同但无冲突 |
| 永不结论 | L45 vs L82 vs L227 vs L288 vs 各 reference | ✅ 处处一致 |
| 不自动起草 | Instructions 8 vs handoff reference L15-16 vs what-this-skill-does-not-do L10 | ✅ 三处一致 |
| intake 等待 | L175 "Wait for the answer" | ✅ 唯一权威声明，无冲突 |
| matter 逻辑 | L93 vs output-location reference | ✅ 一致（启用+活跃 → matter 文件夹；否则输出文件夹）|
| [PLACEHOLDER] 处理 | Instructions 1 vs L119-125 | ✅ 一致：停止 + 弹跳 cold-start / provisional |
| provisional 标签 | L129 | ✅ 与 SCORING PROC-01 的 [PROVISIONAL] 检查点一致 |
| design patent 范围 | L303-305 vs L382 | ✅ "do NOT build a claim chart" 与 "The rest of this mode assumes utility patent" 严格互斥，无重叠执行路径 |

**发现 4.3-1（🟢 minor）**: 跨技能引用前缀不统一——`/ip-legal:fto-triage`（L296）vs `fto-triage`（L412-413，正文与输出节）、`clearance`（L185，无前缀）、`/ip-legal:cease-desist`（L42）vs `/ip-legal:takedown`（L43）、`/litigation-legal:claim-chart`（L420）。全部为合法名称引用，但混用前缀形式。建议统一为带 `/ip-legal:` / `/litigation-legal:` 前缀的完整命令形式，避免 agent 在非插件环境下解析歧义。

**发现 4.3-2（🟢 minor）**: 护栏文本存在**有意冗余**——开头块（L9-14）、Loud guardrail 节全文（L67-87）、Instructions 8（L40-43）、输出模板（L494-499）四处出现近同文。L83-86 的 one-way door / two-way door 框架是独立增量内容（不对称风险决策的精准表述），但 L11-14 与 L78-81 的 fee awards/Rule 11 后果句几乎逐字重复。这是插件族系的刻意修辞（"Say this at the top of every output. Do not drop it. Do not soften it."），判定为设计选择而非缺陷；但可在 Loud guardrail 节用"理由 + 引用"方式消重而不损失强调效果。

**结论**: 未发现实质性逻辑矛盾。仅 3.2-1、4.3-1、4.3-2 三处 🟢 级打磨点。

### 4.4 示例正确性

| 示例 | 位置 | 正确性 |
|------|------|:------:|
| 商标示例（APEXSEED vs APEXLEAF, class 9） | L51 | ✅ 与 Trademark mode 的混淆因素走查路径一致；class 9 商品类别描述具体真实 |
| 商业秘密示例（前工程师带走模型架构笔记）| L55 | ✅ 与 Trade secret mode 的 former employee 事实模式（L463-466）精确对应 |
| 无参数示例 | L59-62 | ✅ 与 argument-hint 与 Mode selection 的"会问权利"行为一致 |

**发现 4.4-1（🟢 minor）**: 两个带事实的示例均为 senior 姿态（"we have APEXLEAF registered"、"our model architecture"），无 accused 姿态示例。Intake 明确要求双姿态处理（L164-168），建议补一个 accused 侧示例（如 "competitor claims our new tool infringes their patent — we don't think it does"）以覆盖对称触发面。

### 4.5 条件完整性

| 条件分支 | 完整性 |
|----------|:------:|
| 五模式 + 混合 | ✅ 全覆盖（混合 = 各跑各的） |
| matter workspaces 启用/未启用/无活跃 matter | ✅ 全覆盖（L93 完整分支） |
| 档案 [PLACEHOLDER] / 已配置 | ✅ 全覆盖（弹跳 / provisional） |
| senior / accused 双姿态 | ✅ intake 覆盖；输出路由不同（assertion letter vs risk memo） |
| D / RE / PP / utility 四类专利 | ✅ 全覆盖 + 分支互斥 |
| 外国法域（德/中/日/UPC） | ✅ L384-390 专用块 + 输出行模板 |
| 淡化仅限著名商标 | ✅ "If the senior mark is not plainly famous nationally, flag dilution as a stretch" |
| 版权未注册 | ✅ §411 flag + "practical bar on filing" |
| 非律师角色 | ✅ non-lawyer-gate reference + OUT-04 检查 |
| DMCA 仅限服务商托管用户内容 | ✅ §512(c) 适用性判定 + "does not cover direct infringement by the service provider" |
| 设计专利"看不到图纸" | ✅ L351-359 诚实声明 + 材料请求清单（这是本技能最诚实的边界处理之一） |

---

## 5. Reference File Content-Level Review

### 5.1 引用完整性矩阵

SKILL.md `## Output format` 节列出 12 个引用文件，逐个核验：

| reference 文件 | 在技能内可验证？ | 类型 | 状态 |
|----------------|:--------------:|------|------|
| citation-verification.md | ✅ 存在 | 实质政策 | 内容正确，但见 5.2 格式缺陷 |
| close-with-the-next-steps-decision-tree.md | ✅ 存在 | 指针型 | 指向档案 `## Outputs`，3 行 |
| defenses-and-thresholds.md | ✅ 存在 | **占位骨架** | 5 行，全占位符 |
| factor-analysis.md | ✅ 存在 | **占位骨架** | 5 行，全占位符 |
| handoff-to-enforcement-skills.md | ✅ 存在 | 实质内容 | 两个 offer 模板 + 不自动起草 |
| non-lawyer-gate.md | ✅ 存在 | 实质内容 | 角色检查 + 1 页简报 + 监管机构转介 |
| output-location.md | ✅ 存在 | 实质内容 | 路径规范 + history.md 条目 |
| posture-and-scope.md | ✅ 存在 | **占位骨架** | 7 行字段模板 |
| recommended-next-steps.md | ✅ 存在 | **占位骨架** | 8 行占位 bullets |
| tone.md | ✅ 存在 | 实质内容 | 风格规范（"No hedging prose"） |
| what-cuts-which-way-summary.md | ✅ 存在 | **占位骨架** | 10 行表格模板 |
| what-this-skill-does-not-do.md | ✅ 存在 | 实质内容 | 6 条不做清单 |

**统计**: 实质内容型 6 个（含 tone/output-location 类规范型），占位模板骨架 5 个，纯指针 1 个。**无幽灵引用**（引用了不存在的文件）✅——12/12 全部真实存在。

### 5.2 引用文件逐文件审查

1. **citation-verification.md（9 行）** — 政策声明正确（每个判例/法条/注册号须核对权威来源、确认现行有效控制性权威）。**缺陷：第 7 行有一个孤立的代码围栏 `` ``` ``（无开围栏）**，见 §6.3。这在本 corpus 是真实的 Markdown 破损。

2. **close-with-the-next-steps-decision-tree.md（3 行）** — 指向档案 `## Outputs` 的决策树五分支（draft the X / escalate / get more facts / watch and wait / something else），并强调 "The tree is the output; the lawyer picks." 语义清晰；作为指针文件内容合理。

3. **defenses-and-thresholds.md（5 行）** — 纯占位符：`[Mode-specific: dilution fame threshold / registration prerequisite / § 512 safe harbor / invalidity / inequitable conduct / preemption / reverse-engineering / consent / license / laches / statute of limitations. Flag each.]`。枚举了 11 类防御/阈值，但无任何内容。作为"输出模板提示"可接受，作为"引用文件"名不副实。

4. **factor-analysis.md（5 行）** — 纯占位符：`[Mode-specific factor table — ...]`。

5. **handoff-to-enforcement-skills.md（17 行）** — 实质内容。两个 offer 脚本（C&D 经 `/ip-legal:cease-desist`、DMCA takedown 经 `/ip-legal:takedown`）+ "Do not draft the letter automatically" + "The decision to assert is the approver's, not the triage's."——与 Instructions 8、SCORING PROC-08/NEG-02 完全对齐。

6. **non-lawyer-gate.md（24 行）** — 实质内容。角色检查（读 `## Who's using this`）+ 后果警告（Rule 11 / DJ / treble damages / fee awards）+ 1 页律师简报生成 + 各国监管机构转介（US state bar / SRA / BSB / Law Society / USPTO / INTA）。监管机构名称正确。与 017 的 find-an-attorney 段同源。

7. **output-location.md（11 行）** — 实质内容。matter 启用时写 `<matter-slug>/outputs/infringe-<mode>-<subject-slug>-YYYY-MM-DD.md`，否则写 `outputs/infringe-...` + 表面化路径 + 活跃 matter 追加 history.md 一行。与 check.py OUT-03 的 `infringe-*.md` glob 精确匹配 ✅。

8. **posture-and-scope.md（7 行）** — 字段模板（party posture / right / jurisdiction / framework / SOL-laches / exhibits）。占位骨架。

9. **recommended-next-steps.md（8 行）** — 4 条占位 bullets（formal opinion / evidence hold / fact development / routing per posture）。骨架但语义方向明确。

10. **tone.md（7 行）** — 实质内容。"Factor-by-factor, flag-by-flag. No hedging prose."——全技能语气纲领，与 Loud guardrail 节的修辞哲学一致。

11. **what-cuts-which-way-summary.md（10 行）** — 表格模板 + "**Conclusion:** *This skill does not conclude.*" 结论行模板。骨架。

12. **what-this-skill-does-not-do.md（16 行）** — 实质内容。6 条不做清单（不结论 / 不替代调查证据-损害专家-claim construction / 不评估管辖范围外防御 / 不定 fair use / 不起草 C&D-takedown-complaint / 不向对方引用输出）。

**发现 5.2-1（🟡）**: 5/12 引用文件为占位骨架（defenses-and-thresholds、factor-analysis、posture-and-scope、recommended-next-steps、what-cuts-which-way-summary）。风险点：(a) 与 SKILL.md `## Output format` 节把它们标为 "Reference Files" 的定位不符——它们实际是**输出模板**而非参考资料；(b) 评测中 agent 读取这些文件获得的是占位符而非内容，LLM judge 判 OUT-02（posture/scope 块、factor table、defenses、what-cuts-which-way 表）时，判定依据完全依赖 SKILL.md 正文质量；(c) 若评测流程希望引用文件提供"知识增量"（规范 §3.4），这 5 个文件几乎无增量。建议：要么充实为真实内容（各模式因素表/防御清单/阈值数据），要么在 SKILL.md 中把该清单更名为 "Output Templates" 并说明占位符的填充规则。

### 5.3 跨 skill 引用检查

- 无 `../other-skill/` 形式的文件路径 ✅。
- 名称引用全部为插件生态内部命令/技能，合规 ✅（前缀不统一问题见 4.3-1）。

### 5.4 嵌套检查

- 单层 references/ 子目录，无更深嵌套，无嵌套 skill 文件 ✅。

### 5.5 scripts / assets / docs / examples 审查

- 无 scripts/、assets/、docs/、examples/ 目录。技能不含可执行脚本 ✅。全部检查逻辑位于 check.py（评测侧）。

### 5.6 check.py 与 SCORING 路径一致性核验

- SCORING 变量注释（L5-8）：`${PRACTICE_CFG}`、`${MATTERS_DIR}`、`${OUTPUTS_DIR}` 与 check.py 注释（L25-26）逐项一致 ✅。
- check.py L26 用 `os.path.expanduser("~/.claude/plugins/config/claude-for-legal/ip-legal/outputs")` 解析 OUTPUTS_DIR，与 output-location.md 的路径规范（`outputs/infringe-<mode>-<subject-slug>-YYYY-MM-DD.md`）一致 ✅。
- OUT-03 glob `infringe-*.md` 与 SKILL.md 输出命名 `infringe-<mode>-...` 匹配 ✅。
- **发现 5.6-1（🔴→🟡 评测管线级）**: check.py 缺少兄弟技能普遍存在的 `os.path.exists` 守卫（详见 §6.6 与 §10.4），导致经文档化调用方式（`python check.py <ws> <log> <output_path>`）运行时 PROC-05 与 OUT-01 **恒为 False**。已用行为仿真复现（见 §6.6）。

---

## 6. Grammar & Format Quality

### 6.1 拼写与语法

- 全文逐段扫描：**未发现拼写错误**。
- 法律术语使用准确：TDRA、du Pont / Polaroid / Sleekcraft、Lanham Act § 43(a)、17 U.S.C. § 107/§ 411/§ 512、35 U.S.C. § 101-103/§ 112/§ 161/§ 171/§ 252/§ 289、DTSA 18 U.S.C. § 1836/§ 1839(6)、DOE、IPR/PGR、claim chart、prosecution history estoppel、point of novelty、broken-line disclaimers——全部拼写与引用格式规范。
- 句式完整，无残缺句、无悬垂修饰。专业法律文体。

### 6.2 中英混杂检查

- 全文纯英文，无中文/其他语言混杂 ✅。

### 6.3 Markdown 破损检查

| 检查项 | 结果 |
|--------|:----:|
| 围栏代码块闭合（SKILL.md） | ✅ 全部成对（Examples 块、provisional 块、work-product 模板块） |
| **围栏代码块闭合（references/）** | ❌ **citation-verification.md 第 7 行有孤立闭围栏 ` ``` `（无开围栏）**——raw 字节验证确认，见 5.2.1 |
| 引用块（blockquote）闭合 | ✅ |
| 粗体/斜体标记 | ✅ 无未闭合 `**` |
| 标题层级 | ✅ H1/H2/H3 有序 |
| 列表缩进 | ✅ 嵌套列表缩进正确 |
| 表格 | ✅ 本技能主体无表格（what-cuts-which-way 表格在 reference 中，格式正确） |
| 转义字符 | ✅ 无异常转义 |

**发现 6.3-1（🟢）**: citation-verification.md 的孤立围栏会将文件 3-6 行的正文渲染为代码块（在部分渲染器中）。修复：删除第 7 行的 ` ``` ` 即可。

### 6.4 非 ASCII 符号审计

| 位置 | 字符 | 判定 |
|------|------|:----:|
| SKILL.md L93 | `✗`（U+2717） | ✅ 功能性——镜像插件实践档案 `## Matter workspaces` 的 `Enabled ✗` 约定标记，非装饰 |
| SCORING.yaml L11/28/93/126 | `─`（U+2500 注释分隔线）| ✅ 注释装饰，corpus 惯例 |
| check.py L30/33/38/44 | `─`（同上）| ✅ 注释装饰 |
| 全部文件 | 其他 box-drawing/emoji | ✅ 零 |

本技能零 emoji，全大写仅用于护栏标题（`THIS IS A TRIAGE, NOT A FINDING`，功能性强调）。对照 corpus 反例（072/153），无喊叫式滥用。

### 6.5 占位符检查

- 技能内出现的占位符均为**功能性模板占位符**：`[PROVISIONAL]`、`[describe the facts...]`、`[GREEN / YELLOW / RED — one sentence why]`、`[WORK-PRODUCT HEADER]`、`[matter-slug]`、`[mode]`、`[subject-slug]`、`[YYYY-MM-DD]`——全部有明确语义与填充规则 ✅。
- 5 个骨架 reference 文件内的 `[Mode-specific: ...]`、`[factor 1]`、`[senior / accused]` 等占位符是**有意设计的输出模板填充槽**，不是残留的未定义占位符——但缺少"填充规则"声明（见 5.2-1）。
- `[PLACEHOLDER]` 标记仅作为检测插件档案未配置的条件文本出现（L19-20），语义正确 ✅。

### 6.6 截断与文件完整性检查

- SKILL.md 517 行，结尾为 Reference Files 清单完整收尾，无截断 ✅。
- 全部 reference 文件结尾完整（多数以 `---` 或完整句收尾；citation-verification.md 以孤立围栏收尾——见 6.3-1）✅。

---

## 7. Spec Compliance（对照 SKILL-SPEC.md v1.0 的 12 条规则清单）

| # | 规则 | 检查 | 结果 |
|---|------|------|:----:|
| 1 | name 小写+连字符，≤64 字符，匹配目录 | `infringement-triage` / `248-infringement-triage` | ✅ |
| 2 | description 第三人称，WHAT+WHEN+KEYWORDS，≤1024 字符 | 约 292 字符，三要素齐备 | ✅ |
| 3 | description 无祈使/第一/第二人称开头 | 以 "Infringement triage across..." 第三人称开头；句中 "your IP" 为灰区 | ⚠️ 通过（附润色建议） |
| 4 | description 无跨技能路由 | 无 | ✅ |
| 5 | description 至少一个触发信号短语 | "Use when assessing..."（"Use when" 家族变体，非规范五个形式字面）| ⚠️ 通过（宽口径，与 017 同判） |
| 6 | frontmatter 无允许列表外键 | 仅 name/description/argument-hint | ✅ |
| 7 | body ≤600 行 | 517 行 | ✅ |
| 8 | body 有 workflow/process 节 | Instructions + 四模式工作流（因素清单 + 输出子节）| ✅ |
| 9 | body 有 output format 节 | `## Output format (all modes)` + 12 引用模板 | ✅ |
| 10 | body 有 scope/limitations 节 | `## THIS IS A TRIAGE, NOT A FINDING`（事实 scope 节）+ what-this-skill-does-not-do reference | ✅（见 3.2-1 命名备注） |
| 11 | body 无跨技能文件引用（../other-skill/）| 无任何 ../ 路径 | ✅ |
| 12 | 目录 NNN-kebab-case，无空格大写 | `248-infringement-triage` | ✅ |

**合规判定**: 12/12 通过（第 3、5 条为灰区变体，按 corpus 先例与 dossier 判定为通过）。**完全合规** 🟢。

---

## 8. Human-Like Feeling

### 8.1 Emoji 审计

| 位置 | Emoji | 判定 |
|------|-------|:----:|
| 全文 | 无 | ✅ 零 emoji（`✗` 为功能标记，见 6.4）|

### 8.2 全大写审计

| 位置 | 文本 | 判定 |
|------|------|:----:|
| L67 节标题 | "THIS IS A TRIAGE, NOT A FINDING" | ✅ 功能性——技能自称 "The loudest guardrail in the plugin"，全大写是该宣言的既定形式 |

无喊叫式滥用。全大写仅一处，且为该技能的标志性护栏。

### 8.3 Persona 语气分析

- 角色：律师事务所 IP 业务助理 / 法务团队分诊工具，语气专业、克制、审慎。
- **one-way door / two-way door 框架（L83-86）是本技能语气的最佳单品**："Under-calling a conflict is a one-way door — a C&D not sent and a mark goes generic in the market; ... Over-calling is a two-way door — the attorney narrows. Stay on the two-way door side."——用不对称风险决策的意象把"保守但不过度"的姿态哲学压缩成可记忆的一句话，且直接指导输出行为（不结论 = 留在两扇门都能回的一侧）。全 corpus 少见的修辞级内容。
- "This skill never concludes. If uncertain, flag — the attorney decides."（L45）——权力边界一句话收束，干净。
- 设计专利节诚实声明"you cannot see the patent drawings"并转为材料请求（L351-359）——专业助手的诚实，而非假装能看图。
- 无 filler、无 pep-talk、无 marketing 腔。

### 8.4 人机边界

| 边界机制 | 位置 | 有效性 |
|----------|------|:------:|
| 永不结论（Loudest guardrail + 双门框架） | L67-87 / L45 | ✅ 强制 |
| intake 等待（"Wait for the answer before walking factors"）| L175 | ✅ 强制 |
| [PLACEHOLDER] 停止 + 弹跳 / provisional | L119-131 | ✅ 强制 + 优雅降级 |
| 混合权利分跑（不 blend）| L22-23 / L153-155 | ✅ 强制 |
| 不自动起草 C&D/takedown（只 offer）| Instructions 8 / handoff | ✅ 强制 |
| 引证验证要求 | citation-verification reference | ✅ |
| 非律师 gate（1 页简报 + 转介）| non-lawyer-gate reference | ✅ 条件触发 |
| 法域外 flag | L384-390 | ✅ 条件触发 |

### 8.5 人称统计（定性）

- 第二人称 "you/your"：约 15+ 处，全部集中在**用户提问块、材料请求、provisional 弹跳文本**（"your practice"、"I'll ask"、"you cannot see"）——是技能定义的人机对话契约，非对 agent 发令。符合设计。
- 对 agent 的指令均为第三人称祈使（"Ask which right"、"Walk each factor"、"Produce a flag list"）——agent 指令与用户话术分离清晰 ✅。
- description 中的 "your IP" 为唯一不在对话契约语境内的第二人称（见 2.3）。

**人机感评级**: 9.5/10 —— 双门框架 + 诚实边界 + 零填充，与 dossier 的 🟢 判定一致，与 017/028 同列 corpus 法律类第一梯队。

---

## 9. Executability

### 9.1 独立可执行性评分

| 维度 | 评分 (0-10) | 说明 |
|------|:----------:|------|
| 步骤可操作性 | 9.5 | 每模式有明确因素清单与输出子节；intake 四要素 + 等待机制；五选一模式分发 |
| 决策门完备性 | 9.0 | 永不结论、[PLACEHOLDER] 停止、混合分跑、不自动起草四类硬约束均有字面依据；无 017 式显式 gate 块（本技能以"flag 不结论"替代）|
| 环境独立性 | 6.0 | 强依赖插件实践档案；[PLACEHOLDER] 时有优雅降级（停止 + provisional），但无法产出正常 triage memo |
| 工具依赖合理性 | 9.0 | Read（档案/matter.md）、Write（memo）、Glob——均为合理生态工具；无 Bash/MCP 硬依赖 |
| 评测可复现性 | 7.5 | 需 workspace 预置档案 fixture（含 Role/Posture/Jurisdiction/Outputs/Matter workspaces 五节）；**check.py 的 PROC-05/OUT-01 恒 False 缺陷（见 6.6/10.4）会进一步压低实际可复现的 script 项** |

**独立可执行性总评**: 插件生态内执行性极佳；SkillIF 裸环境内为"可控降级"状态。评测时需 fixture + check.py 修复。

### 9.2 步骤可操作性表（节选关键步骤）

| 步骤 | 可操作？ | 需要的用户输入 | 需要的工具/数据 | 完成判据 |
|------|:-------:|---------------|----------------|---------|
| Instructions 1: 读实践档案 | ✅ | 无 | Read 档案 | 档案存在且无 [PLACEHOLDER] |
| Instructions 3: 模式分发 | ✅ | 五选一回答 | 无 | 模式确定（或确认混合）|
| Instructions 4: intake | ✅ | 四项批量回答 | 无 | 姿态/管辖/时效/证据记录 |
| Trademark 因素走查 | ✅ | 证据材料 | 档案（电路测试选择）| 8 因素 flag 表 |
| Copyright 因素走查 | ✅ | 注册信息 | 无 | ownership/§411/access/fair use/§512 flags |
| Patent D/RE/PP 分支 | ✅ | 注册号 | 无 | 分支确定（设计专利 → 材料请求）|
| Patent utility claim chart | ✅ | 技术细节 | 无 | 首轮 claim chart + 防御 flags |
| Trade secret 三组 flag | ✅ | 事实 | 无 | secrecy/measures/misappropriation 三组 |
| Output 写盘 | ✅ | 无 | Write + 档案 Outputs 节 | infringe-<mode>-<slug>-date.md |
| 收尾交接 | ✅ | 确认 | 生态命令 | offer（不自动起草）|

### 9.3 工具依赖合理性

- 检索类（CourtListener、Solve Intelligence）来自档案 `## Available integrations` 的动态配置，非硬编码工具调用 ✅。
- 无 Bash 脚本依赖、无 MCP 硬依赖 ✅。

---

## 10. SCORING.yaml Cross-Reference

### 10.1 结构总览

- `pattern: process`、`total_items: 16`。实际条目：2 scope + 8 process + 4 output + 2 negative = 16 ✅ 计数一致。
- judge 类型：script 3 项（PROC-05、OUT-01、OUT-03）、llm 13 项。check.py 实现 3 项 script 检查 ✅ 与 SCORING 一致。
- 类别分布：无 QA 类目（对比 017 有 QA-01；本技能 16 项全部落在 scope/process/output/negative 四类）——覆盖面合理，缺 QA 不构成缺陷。

### 10.2 逐项映射矩阵

| ID | 类别 | judge | 检查方式 | 对应 SKILL.md 内容 | 可判定性 |
|----|------|:-----:|----------|--------------------|:--------:|
| SCOPE-01 | scope | llm | flag-list-not-finding 框架 | 开头护栏 + Instructions 6 | ✅ |
| SCOPE-02 | scope | llm | 问权利 + 混合分跑 | Mode selection | ✅ |
| PROC-01 | process | llm | 档案优先 + [PLACEHOLDER] 弹跳/provisional | Instructions 1 + L119-131 | ✅ |
| PROC-02 | process | llm | intake 四要素 + 等待 | Intake | ✅ |
| PROC-03 | process | llm | 商标混淆测试 + 淡化门槛 + 虚假广告 | Trademark mode | ✅ |
| PROC-04 | process | llm | 版权六要素 | Copyright mode | ✅ |
| PROC-05 | process | **script** | output 含 `design patent\|Egyptian Goddess` | Patent mode 设计专利分支 | ⚠️ 见 10.4 两处问题 |
| PROC-06 | process | llm | utility claim chart 首轮 | Utility patent workflow | ✅ |
| PROC-07 | process | llm | 商业秘密三组 flag | Trade secret mode | ✅ |
| PROC-08 | process | llm | next steps + 姿态路由 + offer 不自动起草 | Instructions 8 + handoff | ✅ |
| OUT-01 | output | **script** | output 含 `triage, not a finding` | 护栏模板 L494 | ⚠️ 见 10.4 两处问题 |
| OUT-02 | output | llm | 八要素输出结构 | Output format + 5 个骨架模板 | ⚠️ 判定依据依赖模板填充（见 5.2-1）|
| OUT-03 | output | **script** | `${OUTPUTS_DIR}/infringe-*.md` 存在 | output-location reference | ✅ 需 fixture 目录存在 |
| OUT-04 | output | llm | 非律师 gate | non-lawyer-gate reference | ✅ |
| NEG-01 | negative | llm | 绝不结论（fair use/损害/有效性）| 护栏 + what-this-skill-does-not-do | ✅ |
| NEG-02 | negative | llm | 不自动起草 + 引证验证 | Instructions 8 + citation-verification | ✅ |

### 10.3 Critical Failures 分析

| ID | 描述 | effect | 与 SKILL.md 一致性 |
|----|------|:------:|--------------------|
| CF-01 | 结论侵权/非侵权 | cap_to_0 | ✅ 对应 Loudest guardrail |
| CF-02 | 省略/软化/移动护栏 | cap_to_0 | ✅ 对应 "Say this at the top of every output" |
| CF-03 | 混合权利合并分析 | cap_to_0 | ✅ 对应 "run each separately; do not blend" |
| CF-04 | 无档案且无 provisional 标签 / 无姿态-管辖 intake | cap_to_0 | ✅ 对应 Instructions 1/4 + provisional 节 |

CF 设计质量：四个 CF 全部对应技能内"强制不可违反"规则，均有字面依据，cap_to_0 语义与职业责任风险严重度匹配 ✅。CF-04 是 corpus 中少见的复合 CF（档案缺失 + provisional 标签 + intake 三条件合一），覆盖了评测环境最容易发生的失败模式。

### 10.4 SCORING 质量评价与两处结构问题

- 覆盖面：16 项覆盖 scope/process/output/negative 全类别，无类别失衡 ✅。
- LLM 项问题质量：13 项问题的 evidence 指向明确（"Triage output factor table (trademark mode)"、"Tool call log"、"Triage memo conclusion sections"），LLM judge 可判定 ✅。

**问题 10.4-1（🔴 评测管线级，修复成本 2 分钟）**: **check.py 缺失 `os.path.exists` 守卫导致 PROC-05/OUT-01 恒 False**。对比 017/028/200/121 的 check.py 均在 check() 内实现：

```python
try:
    _is_path = os.path.exists(agent_output)
except (OSError, ValueError):
    _is_path = False
if not _is_path:
    set_agent_output(agent_output)
```

248 的 check.py L22 无条件 `set_agent_output(agent_output)`。由于 main()（L58-60）已先把文件**内容**载入 `_agent_output`，check() 随后用**路径字符串**覆写之——`output_contains` 检索的是路径字符串而非输出内容。已用行为仿真证实：输出文件明明含 "triage, not a finding" 与 "design patent"，经 `python check.py <ws> <log> <output_path>` 调用时 PROC-05 = False、OUT-01 = False；直接传内容时两者为 True。**效果**: 经文档化调用方式，本技能最重要的两条 script 检查（护栏字面检查 + 设计专利分支检查）恒判定失败，评测结果系统性失真。

**问题 10.4-2（🟡）**: PROC-05 是无条件注册的模式条件检查——pattern `design patent|Egyptian Goddess` 只在专利模式（且设计专利语境）成立。若评测用例是商标/版权/商业秘密场景，合规 agent 的输出不该含 "design patent"，PROC-05 必然失败且**不应**失败。建议：(a) SCORING 注释说明 PROC-05 仅对专利场景用例计分；(b) 或在 check.py 中按用例模式条件化。注意 "Egyptian Goddess" 字样在 SKILL.md 正文 L319 出现——但 output_contains 检查的是 agent 输出，无假阳性风险；反观 "design patent" 是通用词组，商标模式输出若顺带提及可能假阳性，概率低。

**问题 10.4-3（🟢）**: OUT-03 的 description 声明 "with a history.md entry when a matter is active"，但 script 检查仅验证 memo 文件存在，history.md 部分无验证——描述承诺与检查粒度不匹配（minor）。

---

## 11. Known Issues from skill-dossier.md

Dossier 原文（Batch 226-250 摘要，248-infringement-triage 条目，无独立条目、仅批组摘要）：

> **逻辑**: 248 模式选择→因素走查→红旗清单严密。
> **人机感**: 248 "triage 不是 finding"护栏极强。
> **合规**: 🟢 233/237/240/241/243/248 三节齐全；... 🟢 248 优秀。

**本次审查与 dossier 对照结论**:

| Dossier 声明 | 本次验证 | 结论 |
|--------------|---------|:----:|
| 模式选择→因素走查→红旗清单严密 | ✅ 四模式因素清单 + 混合分跑规则逐节验证一致 | 确认 |
| "triage 不是 finding"护栏极强 | ✅ 双门框架 + 四处呼应 + OUT-01/CF-01/CF-02 三道检查 | 确认（且比 dossier 所记更强）|
| 三节齐全 | ✅ workflow/output/scope 均满足（scope 借护栏节承载，见 3.2-1）| 确认（附命名备注）|
| 🟢 优秀 | ✅ 本次审查评级 A（9.03/10）| 确认 |

**dossier 未记录而本次发现的问题**: ① check.py 恒 False 缺陷（10.4-1）；② 5 个占位骨架引用文件（5.2-1）；③ citation-verification.md 孤立围栏（6.3-1）；④ 跨技能命名前缀不统一（4.3-1）；⑤ description 灰区两处（2.3）。前两项对评测有实质影响，建议在 dossier 后续更新中补记。

---

## 12. Comprehensive Scoring

### 12.1 八维度加权评分表

权重设定：合规 20%（规范性是 corpus 首要目标）、逻辑 15%、可执行 15%、语法 10%、人机感 10%、引用 10%、SCORING 质量 10%、内容深度 10%。

| 维度 | 权重 | 得分 | 加权 | 主要依据 |
|------|:----:|:----:|:----:|---------|
| 逻辑一致性 | 15% | 9.0 | 1.350 | 总流程 + 四模式闭环、D/RE/PP 硬分支互斥；仅 3 处 🟢 级打磨点（无实质矛盾）|
| 语法与格式 | 10% | 9.0 | 0.900 | 零错字、术语精准；citation-verification 孤立围栏一处 🟢 |
| 人机感 | 10% | 9.5 | 0.950 | 双门框架、诚实边界、零 emoji、无喊叫；corpus 法律类第一梯队 |
| 规范合规 | 20% | 9.5 | 1.900 | 12/12 通过（2 条灰区按宽口径）；description 边界前置为加分项 |
| 可执行性 | 15% | 8.5 | 1.275 | 生态内极强；裸环境依赖 fixture（档案五节）|
| 引用完整性 | 10% | 9.0 | 0.900 | 12/12 真实存在、无幽灵引用、路径与 glob 匹配；5 个骨架文件拖累知识增量 |
| SCORING 质量 | 10% | 8.0 | 0.800 | 16 项全覆盖、CF 与护栏严格对应；但 check.py 恒 False 缺陷 + PROC-05 无条件注册 + OUT-03 history.md 未验证 |
| 内容深度 | 10% | 9.5 | 0.950 | 设计专利全节（broken lines/§289/point of novelty/贸易外观交叉旗标）、非美法域块、双门框架、13 个判例引用全部核实真实准确 |
| **合计** | 100% | — | **9.03** | — |

### 12.2 评级

**评级: A（9.03/10）—— 典范级，与 017/028 同列 corpus 法律过程技能第一梯队。**

与 dossier 🟢 判定一致。扣分集中在评测管线层（check.py 缺陷）与引用文件的骨架化，而非技能内容本身。技能内容质量足以支撑 A 级；修复 check.py 一处 2 分钟的缺陷后，SCORING 质量维度可回升至 9.0，总分约 9.2。

---

## 13. Fix Recommendations

### 13.1 🔴 致命问题

**无（技能本体）。** 技能可直接使用。唯一接近"致命"的是评测侧缺陷（见 13.2 #1），与技能内容无关。

### 13.2 🟡 重要问题

1. **check.py 恒 False 缺陷（评测管线级，修复成本 2 分钟，优先级最高）** — `D:\SkillIF\skill-experiment\complex-skills\248-infringement-triage\check.py` L22 缺少 `os.path.exists` 守卫：main() 已载入输出内容后，check() 用路径字符串覆写 `_agent_output`，导致经 `python check.py <ws> <log> <output_path>` 文档化调用时 PROC-05 与 OUT-01 **恒为 False**（已仿真复现）。修复：按 017/028/200/121 的 check.py 模式加入：

   ```python
   try:
       _is_path = os.path.exists(agent_output)
   except (OSError, ValueError):
       _is_path = False
   if not _is_path:
       set_agent_output(agent_output)
   ```

   并补一行回归注释（"main() has already loaded its content"）。

2. **PROC-05 无条件注册的模式条件检查** — SCORING.yaml L64-67。非专利场景用例下该项恒失败且不应失败。建议：SCORING 注释声明 PROC-05 仅对专利场景计分，或在 check.py 中按用例模式条件化。

3. **5 个占位骨架引用文件** — defenses-and-thresholds.md、factor-analysis.md、posture-and-scope.md、recommended-next-steps.md、what-cuts-which-way-summary.md。建议二选一：充实为真实内容（各模式因素表/防御清单），或在 SKILL.md `## Output format` 中将清单更名为 "Output Templates" 并声明占位符填充规则（当前 "Reference Files" 命名与文件实际性质不符，且 OUT-02 的 LLM 判定完全依赖模板被正确填充）。

### 13.3 🟢 优化建议（均可选）

| # | 问题 | 位置 | 建议 | 工作量 |
|---|------|------|------|:------:|
| 1 | description 第二人称 "your IP" + "Use when assessing" 触发变体 | L3 | 改为规范形式："Use when the user assesses whether the user's IP is being infringed or whether the user might be infringing another's IP..." | 5 分钟 |
| 2 | citation-verification.md 第 7 行孤立代码围栏 | references/citation-verification.md | 删除 ` ``` ` 行 | 1 分钟 |
| 3 | 跨技能引用前缀不统一（`/ip-legal:fto-triage` vs `fto-triage` vs `clearance`）| L185/L296/L412-413 | 统一为带插件前缀的完整命令形式 | 5 分钟 |
| 4 | Examples 缺 accused 姿态示例 | L51-62 | 补一个 "competitor claims our product infringes" 类示例，覆盖对称触发面 | 3 分钟 |
| 5 | OUT-03 description 承诺 history.md 验证但 check 未实现 | SCORING.yaml L113-117 | 描述中删除 history.md 子句，或 check.py 增加 history.md glob | 2 分钟 |
| 6 | 主体无 `## What this skill does not do` 同名节 | SKILL.md 主体 | 在 Output format 节前加内联 scope 小节，或在护栏节补充边界列表，消除规范 §3.1 字面可辩护性弱点 | 10 分钟 |
| 7 | OUT-03 glob 依赖 `~/.claude/plugins/config/claude-for-legal/ip-legal/outputs` 目录预先存在 | check.py L26/L41 | 评测时预置 fixture 目录，或 file_exists 前先 mkdir（与评测 runner 约定）| 10 分钟 |

### 13.4 总体结论

**248-infringement-triage 是 claude-for-legal 插件家族中内容深度与风险设计均属顶级的技能**：双门不对称风险框架、"永不结论"的多层硬约束、D/RE/PP 专利前缀硬分支、13 个判例引用全部核实真实准确、非美法域专用块、诚实的设计专利边界声明——这些元素叠加使本技能在 322 个 corpus 技能中稳居法律类第一梯队（与 017、028 并列）。规范 12/12 通过。唯一实质问题在评测侧：check.py 的恒 False 缺陷会系统性压低两条 script 检查的实际效力，属 2 分钟可修复的机械错误，修复后评测结果方能反映技能真实水平。**评级: A（9.03/10）。**
