# REVIEW: 115-tpl-situacao-ab-testing-implementacao

**审查日期**: 2026-08-06
**Skill 类型**: mindset（situational）— A/B 测试实施情境指南（实验设计、样本量、sticky bucketing、统计分析、winner 部署、报告）
**Body 行数**: 214 行（L6–L219；文件按 wc -l 计 218 行，末行无换行符，Read 显示至 L219）
**参考文件数**: references/0, scripts/0, assets/0, 其他/0（SCORING.yaml 与 check.py 为评估附属文件，非 skill 参考资源）
**前版 REVIEW**: 无（本篇为该 skill 首版全量审查）

---

## 1. 目录全量清单

Glob `**/*` 结果：目录内仅 4 个文件，无任何子目录（references/、scripts/、assets/、templates/ 均不存在），属于极简自包含结构。与系列姊妹 skill 029 完全同构（029 亦为 4 文件自包含）。

```
D:\SkillIF\skill-experiment\complex-skills\115-tpl-situacao-ab-testing-implementacao\
├── SKILL.md     (218 行 wc / 219 行 Read；body 自 L6 起 = 214 行)
├── SCORING.yaml (155 行 wc / 155 行 Read；YAML 解析通过)
├── check.py     (82 行 wc / 82 行 Read)
└── REVIEW.md    (本篇，首版)
```

结构评估：技能内容完全内嵌于 SKILL.md，无外部参考文件。本 skill 与系列其他成员（19 个 tpl-situacao-*，见 §5.5）共享结构骨架：`SITUATION: <主题>` + 编号原则列表 + ROUTING TABLE + DO NOT + OUTPUT FORMAT + QUALITY GATES；但 115 是系列中少见的"规则 + 可运行代码"混合体——包含 3 个代码块（TypeScript 分配服务、Python 统计检验、2 个 Markdown 模板），内容密度在系列中属最高一档（029 仅含 1 个 yaml CI 模板）。按 SKILL-SPEC §3.2 的模式划分，本 skill 属于 mindset 类（目标 ~50 行），214 行 body 明显超量，但 A/B 测试的"设计模板 + 代码载体 + 输出模板"结构使其长度有实质内容支撑，非注水冗余（详见 §3.5 与 §9）。

---

## 2. Frontmatter 逐字段审查

Frontmatter 共 4 行（L1–L4）：`name` + `description`。无其他字段，无禁止字段。

### 2.1 name

- 实际值：`tpl-situacao-ab-testing-implementacao`（L2），37 字符 ≤ 64 ✅
- 字符集：小写字母 + 连字符 ✅
- 目录匹配：目录为 `115-tpl-situacao-ab-testing-implementacao`，name 缺少 `115-` 前缀。**严格对照 SKILL-SPEC §1.1/§4 属于不匹配**；但经全语料核查，19/19 个 tpl-situacao 系列 skill（023/029/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210）全部采用"name 去掉 NNN 前缀"的同一约定，属系列性惯例而非本文件孤例。判定：✅（系列约定内一致），在 §7 中注明 spec 字面差异。

### 2.2 description（L3，共 322 字符 ≤1024 ✅）

完整原文：

> "Pack template (situacao/17-ab-testing-implementacao.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is implementing A/B tests, multivariate tests, or feature flag-driven experiments and needs statistical rigor and clean winner deployment."

逐句分析（S1/S2/S3 分句；经 python yaml.safe_load 实测总长 322 字符）：

| 分句 | 原文 | 功能 | 判定 |
|------|------|------|------|
| S1 | "Pack template (situacao/17-ab-testing-implementacao.md)."（57 字符） | 元信息 | 🔴 内部打包路径残留，对 agent 无任何行为意义，应删除 |
| S2 | "Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context."（107 字符） | WHAT | 🔴 通用模板文案 — "debugging, security and refactoring" 与本 skill 的 A/B 测试内容**完全无关**（本 skill 不含调试、安全或重构指导），会造成错误触发与测评时 SCOPE-01 判定歧义 |
| S3 | "Use when the user is implementing A/B tests, multivariate tests, or feature flag-driven experiments and needs statistical rigor and clean winner deployment."（156 字符） | WHEN+KEYWORDS | ✅ 触发描述准确，与 body 内容（实验设计、样本量、统计检验、winner 部署、报告）一一对应；KEYWORDS 覆盖 "A/B tests / multivariate tests / feature flags / statistical rigor / winner deployment" |

补充验证：经全语料 grep，S1+S2 这段"Pack template (situacao/…). Guides the agent on situational tasks such as debugging, security and refactoring"在 **19/19 个 tpl-situacao 系列 skill 中逐字重复**（含 023、029、030、046、058、059、078、099、100、101、116、132、145、146、168、169、186、210），确认是 pack 模板生成时的统一占位文案，属系列级缺陷而非单文件问题。029 的 REVIEW 已确认同一问题。

评分：5/10。S3 是本语料中最贴合 body 内容的触发句之一（对 A/B 测试术语的覆盖几乎无遗漏），但 S1/S2 占据约 52% 篇幅且内容误导。

**修改建议**（替换整行）：
> "Guides the agent in planning, implementing, and analyzing A/B tests with statistical rigor. Use when the user is implementing A/B tests, multivariate tests, or feature flag-driven experiments and needs hypothesis design, sample size calculation, significance testing, or clean winner deployment."

### 2.3 allowed-tools

❌ 缺失。SKILL-SPEC §1.2 将 `allowed-tools` 列为**可选**字段，缺失不构成合规失败；但本 body 明确要求使用 Python/scipy 执行统计检验（L131–165）、读取实验配置与写入报告，建议补充 `Read, Write, Bash, Glob, Grep` 以约束 harness 工具面。

### 2.4 其他 frontmatter 字段

无。未使用 §1.3 禁止列表中的任何字段 ✅。

### 2.5 Frontmatter 语法

YAML 结构合法：`---` 包裹（L1/L4），name/description 均为一键一行，值含冒号与括号但无双引号包裹——description 中首个冒号出现在 "situacao/17-ab-testing-implementacao.md)" 之后，为键值分隔符，后续冒号在无引号 flow 中合法。经 python yaml.safe_load 验证 SKILL.md 可解析（SCORING.yaml 解析详见 §10）。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（标题树 + 行数）

```
L6   # SITUATION: A/B Testing Implementation             (H1)
L8–20    编号原则 1–7（每条一行，加粗标题句 + 说明）     (13 行)
L22 ## ROUTING TABLE                                     (H2)
L24–35   表头 + 10 行 if→then 场景映射                   (12 行)
L37 ## Experiment Design Template                        (H2)
L39–76   ```markdown``` 模板（Hypothesis→Decision Date） (38 行)
L78 ## Feature Flag Architecture                         (H2)
L80–127  ```typescript``` 代码（ExperimentService 类）   (48 行)
L129 ## Statistical Analysis                             (H2)
L131–165 ```python``` 代码（analyze_ab_test 函数）       (35 行)
L167 ## DO NOT                                           (H2)
L169–176   8 条禁令                                      (8 行)
L178 ## OUTPUT FORMAT                                    (H2)
L180–206  ```markdown``` Experiment Report 示例          (27 行)
L208 ## QUALITY GATES                                    (H2)
L210–219   10 项验收标准                                  (10 行)
```

标题层级：H1 ×1 → H2 ×7，无 H3（grep 命中的 "## Experiment: [Name]" L40、"### Results" L188 等全部位于代码围栏内部，是模板示例而非真实结构层级）。层级无跳跃，结构规整。代码/模板内容占总 body 约 68%（148/214 行），是本语料中代码密度最高的 tpl 系列成员。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

| 必需章节 | 状态 | 分析 |
|---------|:----:|------|
| Workflow / Process | ✅ | 双重载体：编号原则 1–7（L8–20）给出执行纪律（单变量、指标先行、样本量、sticky、novelty、停止规则、清理），ROUTING TABLE（L22–35）以"场景→动作"决策表充当路由流程。比 029 的隐含 workflow（无原则序列）更显式，系列内最强一档 |
| Output Format | ✅ | `## OUTPUT FORMAT`（L178–206）完整：Experiment Report 模板含 Duration、Total Visitors、Results 表、p-value、Relative Lift、Decision、Next Steps 七要素 |
| Scope / Limitations | ❌ | **无 `## Scope` 或等价章节**。`## DO NOT`（L167–176）提供了 8 条禁令（行为约束），但未说明"本 skill 不做什么"（如：不覆盖 A/A 对照实验、不做 CUPED/分层调整、不做多臂老虎机、不处理用户调研类实验、不替代产品决策）——这是本 skill 与系列共有的核心规范缺陷 |

### 3.3 内容委托分析

本 skill 零外部委托：无 references/、scripts/ 引用，全部内容内嵌。与 029 不同的是，115 的代码是**内联在 body 中的完整实现**（TS 分配服务 + Python 检验函数），而非指向不存在的脚本——不存在 029 的"幻影脚本"问题。唯一的"外部依赖"是 TS 片段引用的 `murmurhash` 函数与 Python 片段依赖的 `scipy` 库（详见 §4.3/§5.2）。

### 3.4 节编号/标题层级

- 原则列表编号 1–7（L8/L10/L12/L14/L16/L18/L20）连续无跳号 ✅（dossier 声称的"从 2. 开始缺 1."在当前版本**不复现**，详见 §11）
- ROUTING TABLE 10 行**未编号、无优先级列**——多场景同时触发时（如"样本量不足 + 显著性冒进"）无裁决规则，见 §4.4
- DO NOT 8 条无编号（项目符号），一致 ✅
- QUALITY GATES 10 项复选框（`- [ ]`）格式规范 ✅
- 各 H2 节标题为全大写风格（ROUTING TABLE / DO NOT / OUTPUT FORMAT / QUALITY GATES），与系列其他成员一致，非喊叫式（§8.2 详析）

### 3.5 Body 长度合规

214 行（L6–L219）≤ 600 硬上限 ✅。对照 mindset 类目标 ~50 行，超出 4 倍——但内容密度高（7 原则 + 10 场景路由表 + 38 行设计模板 + 48 行 TS + 35 行 Python + 8 禁令 + 27 行报告模板 + 10 质量门），且"设计模板→代码→报告"三段互相锚定（§4.1），不属于冗余注水。若严格按 spec §3.2 治理，可将 TS/Python 代码下沉至 references/，但当前长度合规，不强制。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

Skill 的"决策流"逻辑链完整闭环：

1. 场景识别（description S3 + SCOPE-01）→ 2. 路由（ROUTING TABLE 10 场景）→ 3. 执行约束（7 条原则）→ 4. 实验设计（Design Template：假设/指标/样本量/时长/分配）→ 5. 代码载体（TS 分配服务 + Python 检验）→ 6. 禁令边界（DO NOT 8 条）→ 7. 产出（Experiment Report）→ 8. 验收（QUALITY GATES 10 项）。

各环节**互相锚定**，交叉引用验证（关键一致性矩阵）：

| 锚点 A | 锚点 B | 一致性 |
|--------|--------|:------:|
| 原则 2 "定义指标先于分流"（L10） | Design Template "Primary Metric"（L50）+ DO NOT 2（L170）+ QUALITY GATES 1–2（L211–212） | ✅ 四层一致 |
| 原则 3 "样本量先算"（L12） | 模板 "12,400 users per variant"（L65）+ DO NOT 1（L169）+ 路由行 3（L28）+ QUALITY GATES 3（L213） | ✅ |
| 原则 4 "sticky bucketing"（L14） | TS `getVariant`/`assignAndLog`（L93–125）+ 路由行 4（L29）+ QUALITY GATES 5（L215） | ✅ |
| 原则 5 "novelty effect"（L16） | 路由行 5 "Continue to 2 full weeks"（L30）+ DO NOT 3（L171） | ✅ |
| 原则 6 "到样本量才停"（L18） | DO NOT 1（L169）+ 路由行 3（L28）+ 报告示例 14 天 ≥ 1–2 周（L185） | ✅ |
| 原则 7 "清理实验代码"（L20） | 路由行 8（L33）+ DO NOT 5（L173）+ QUALITY GATES 8（L217）+ 报告 Next Steps（L201–205） | ✅ |
| DO NOT 8 "排除 bot"（L176） | 路由行 10（L35）+ QUALITY GATES 6（L216） | ✅ |
| 路由行 6 "one/two-tailed 验证"（L31） | Python `proportions_ztest` 默认 two-sided（L149）+ SCORING STAT-01 | ✅ |
| 模板 "50/50 分流 + hash%100<50 → control"（L68/L71） | TS `bucket < treatmentPercentage`（L104） | ✅ 语义一致 |
| 模板 "12,400 per variant" | 报告示例 "14,200 per variant ≥ 12,400"（L186）→ 分析合法（STAT-03 成立） | ✅ |
| 模板 "Estimated Duration 10 days" | 报告示例 "14 days"（L185）——实际流量低于估算时延长运行直至样本量，正符合原则 5/6 | ✅ |

设计模板示例时间线（L74–75）"Minimum End Date = start + duration, Decision Date = +2 days analysis buffer"与原则 6"不早停"一致 ✅。共 12 组交叉锚定全部一致。

### 4.2 内部矛盾扫描

**🔴 重大发现——OUTPUT FORMAT 工作示例的数字与自身代码矛盾（详见 4.3）**。这是本 skill 唯一的实质逻辑缺陷，但因其位于"统计 rigor"类 skill 的输出示范中，性质严重（与语料中 074-social-media-analyzer 的"示例与公式对不上"同类）。

其余逐项核对均无矛盾：
- L18 "Automated stopping rules (sequential testing) are valid only if configured before the experiment starts" 与 L65 "Minimum End Date. Never end before this." 一致 ✅
- L58–62 Guardrail Metrics（error rate / P95）与 QUALITY GATES 10（L219）一致 ✅
- 路由行 7 "two experiments on same page/flow → interaction risk" 与原则 1 单变量纪律互补而非冲突 ✅
- DO NOT 7 "新用户/低频用户 alone → survivorship bias"（L175）为系列独有内容，逻辑独立正确 ✅

### 4.3 示例/代码正确性

**Python 统计检验代码（L131–165）**：`analyze_ab_test` 使用 `scipy.stats.proportions_ztest`（two-proportion z-test，默认 two-sided）、`alpha=0.05`，返回 p-value、相对 lift、SHIP/NO_SHIP 建议——实现正确且可直接运行 ✅。两处小瑕疵：① `confidence: (1-p_value)*100`（L163）不是统计学意义上的置信区间，对双侧检验也不等于 (1-α) 置信度，建议改为报告 `statsmodels` 的 `proportion_confint` 或删除该字段；② 默认 two-sided 与 `recommendation: 'SHIP' if (is_significant and relative_lift > 0)`（L162）组合正确（显著且为正才 SHIP），但未处理"显著为负"分支的提示文案（NO_SHIP 已覆盖，可接受）。

**🔴 OUTPUT FORMAT 工作示例（L182–206）数字自相矛盾——经 scipy 复算验证**：

示例给出 Control 852/14,200（6.00%）、Treatment 924/14,200（6.51%），并宣称 "p-value: 0.023 (statistically significant at 95% confidence)"、"Decision: SHIP TREATMENT"。复算：

```
pooled p = (852+924)/28,400 = 0.06254
SE      = sqrt(0.06254 × 0.93746 × 2/14,200) = 0.002873
z       = (0.06507 − 0.06000) / 0.002873 = 1.765
two-sided p = 0.0776  （one-sided p = 0.0388）
```

- 实际双侧 p = **0.0776 > 0.05**，并非示例宣称的 0.023；
- 按 skill 自身代码（L162），`is_significant=False` → 返回 **NO_SHIP**，与示例的 "SHIP TREATMENT ✅" 直接矛盾；
- 若某 agent 认真执行本 skill（按 L131–165 代码复算），会得出与示例相反的结论——统计类 skill 的示范与实现互相拆台，严重损害可信度；
- 相对 lift 声明 "+8.4%"（L196）按精确值 924/852 − 1 = 8.45% 取一位小数应为 +8.4%（四舍五入边界，可接受）；"6.51%"（L193）来自 924/14,200 = 6.507% ✓。

修复方案见 §13 F-2（已复算出一组自洽数字：Treatment 945/14,200 → z = 2.267，p = 0.0234 ≈ 0.023，lift +10.9%，SHIP 成立）。

**TypeScript 片段（L80–127）**：`ExperimentService` 设计正确——murmurhash 确定性分配、实验关闭时回退 control（L100–102）、`assignAndLog` 每用户每实验只记录一次（L119–123）。瑕疵：`murmurhash`（L95）在片段中未定义（外部依赖未声明）、`this.getExperiment`/`this.hasLoggedAssignment`/`this.cacheAssignment` 为方法签名占位（L98/L119/L122）——作为说明性伪代码可接受，但 `murmurhash` 至少应注明"假设已引入 murmurhash-js"。

**其余示例数值核验**：
- 28,400 = 2 × 14,200 ✅；12,400 需求 vs 14,200 实际 ✅；14 天 ≥ 1 周下限 ✅；14 天 × 2,029 访客/天 ≈ 28,400 ✅
- 2024-01-01 为周一，14 天窗口完整覆盖两个周末（day-of-week 效应）✅——示例细节考究

### 4.4 条件完整性

- ROUTING TABLE 10 种场景覆盖：无假设试跑、多变量混改、样本量不足、sticky 失效、novelty、显著性冒进、实验交互、flag 残留、无 holdback、bot 流量。覆盖面广且全部是 A/B 实践中的高频陷阱 ✅
- **缺失 1：多场景同时触发无优先级裁决**（如"样本量不足 + 显著性冒进 + 两实验同页"同时成立时按哪行执行？）。DO NOT 与原则均未定义裁决顺序
- **缺失 2：guardrail 指标劣化的处置路径未定义**——原则 6 允许"for safety"早停，但未说明"什么构成安全原因、劣化后如何处置（暂停? 回滚? 报障?）"
- 缺失 3：样本量计算只给参数（80% power / 95% / MDE）不给公式或工具（如 `statsmodels.stats.power.TTestIndPower` 或 `sm.stats.proportion_effectsize`），agent 需自行编造计算方式
- 缺失 4：peeking/多重比较纪律（多次查看显著性、多指标同时检验时的假阳性膨胀）未量化——L18 提及 sequential testing 需预先配置，但未给出 Bonferroni/Holm 或 alpha-spending 的落地指引

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用来源 | 引用目标 | 存在? | 判定 |
|---------|---------|:----:|------|
| SKILL.md body | references/、scripts/、assets/ | — | ✅ 零文件引用 |
| TS 片段 L95 `murmurhash(...)` | 外部哈希函数 | N/A | ⚠️ 未声明依赖的"幻影符号"（伪代码语境，可接受但应注明） |
| Python 片段 L148 `stats.proportions_ztest` | scipy.stats | N/A | ✅ 标准库依赖，合理 |
| SCORING.yaml | check.py 函数 `output_contains` | ✅ | 存在于 `_shared/checker.py` L339 |

skill 包内文件引用：0 处。跨包引用：0 处（无 `../other-skill/`）✅。

### 5.2 不可见资源审计

- **murmurhash**：TS 片段核心分配函数未定义、未注明引入方式。与 029 的幻影 `./scripts/*.sh` 不同，这里没有"承诺不存在的文件"，但 agent 若照抄代码会得到 NameError。修复成本极低（一行注释或改用内联简单哈希）。
- **power calculator**：原则 3（L12）与模板（L65）要求"power analysis 计算样本量"，但全文未给出任何可执行的计算方式（无公式、无 statsmodels 调用、无在线工具名）。对一个要求"statistical rigor"的 skill，样本量计算是唯一无法直接执行的关键步骤。

### 5.3 Reference 文件全文审查

无 references/ 目录。本 skill 为自包含模板 + 内联代码，不依赖外部知识文件，参考完整性维度得高分（9/10）。

### 5.4 Scripts 文件全文审查

本包无 scripts/。唯一脚本为评估附属 `check.py`（82/82 行），在此与其姊妹库一并审查：

- L1–5 docstring：声明用法与 JSON 输出格式，准确
- L11 `sys.path.insert(0, "../_shared")` 相对路径——依赖运行 CWD 或固定目录布局，属评估框架约定，可接受
- L12–15 import：`output_contains`、`set_tool_log_path`、`set_agent_output` — 已逐一对证 `_shared/checker.py`（L339/L224/L333）✅ 存在且签名匹配
- L18 `check(workspace, tool_log, agent_output)`：`workspace` 参数**声明但从未使用**——无害但冗余（与 029 相同）
- L23–28：对 `os.path.exists(agent_output)` 的 OSError/ValueError 防御（Windows 长路径兼容）✅ 处理周到
- L38–51：6 个脚本判定点（PROC-02/PROC-05/STAT-01/OUT-01/OUT-02/OUT-03），正则与 SCORING.yaml **逐字符一致** ✅
- L53–59：llm 判定项正确注释跳过 ✅
- 总体：逻辑清晰、库对接正确，无遗漏、无多余。唯一风险点是 `output_contains` 的大小写敏感性（`_shared/checker.py` L339–345 使用 `re.search` 且无 `re.IGNORECASE`）——PROC-05 的 "Remove (control|…)" 要求大写 R，OUT-02 的 "Relative Lift" 要求大写 L；agent 若未按 OUTPUT FORMAT 模板的措辞输出（如写小写 "relative lift"）会误判失败。因报告模板本身规定了大小写，此风险可控，但值得在评估说明中注明。

### 5.5 跨 Skill 引用检查

- SKILL.md 无跨 skill 引用、无 `../` 路径 ✅
- 系列横向比对（已 grep 全语料）：023/029/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210 共 19 个 tpl-situacao-* skill，**全部**携带相同的 description 模板残留（"Pack template (situacao/…). Guides the agent on situational tasks such as debugging, security and refactoring…"）——本 skill 的 description 缺陷是系列复制粘贴产物，修复应系列级进行
- 本 skill 的 ROUTING TABLE + 代码块结构在系列内属最完整一档（与 029 的清单型结构互补）

### 5.6 嵌套重复/死文件检查

- 无嵌套目录、无隐藏文件、无重复内容块 ✅
- body 内无重复段落：Experiment Design Template（L37）与 OUTPUT FORMAT（L178）一为"设计时"文档一为"结束时"文档，互补而非重复 ✅
- QUALITY GATES 与 DO NOT 的重叠（如 flag 清理同时出现在两处）属于"原则重申于验收标准"的正常设计，非冗余 ✅

### 5.7 其他资源文件审查

仅 SCORING.yaml（155/155 行）与 check.py，均已在 §5.4 与 §10 详审。目录中无 assets/、templates/、无图片或二进制文件。

---

## 6. 语法与格式质量

### 6.1 拼写错误

全文通读未发现拼写错误。抽查高频词：attribution（L8）、p-hacking（L10）、non-negotiable（L14）、novelty（L16）、survivorship（L175）、murmurhash（L95）、holdback（L34）、guardrail（L58）——全部正确 ✅。术语使用专业（sticky bucketing、relative lift、power analysis、two-proportion z-test、feature flag、MDE）✅。

### 6.2 语法错误

未发现语法错误。标点使用规范；引导语、条件句（"If you need to test multiple things…"）完整。唯一风格注意点：L10 的 "What minimum effect size would justify shipping?" 等设问句是教学式修辞，功能明确 ✅。

### 6.3 葡英混杂

按审查指令，tpl-situacao 系列为**葡语模板系列，葡语元素视为有意**。本文件核查结果：
- 正文 100% 英文，无葡语内容
- 葡语残留仅 1 处：description S1 "Pack template (situacao/17-ab-testing-implementacao.md)"（L3）中的 "situacao"——这是 pack 内部路径名（系列命名惯例，无重音符号），属有意系列命名，不计为错误；但该分句本身作为 description 内容是缺陷（见 §2.2）
- skill 名 "tpl-situacao" 为系列前缀，有意为之 ✅

### 6.4 Markdown 格式破损

- **粗体配对**：全文 `**` 出现 76 次（偶数）✅ 无未闭合粗体
- **dossier 声称的编号破损不复现**：L8 原始字节验证为 `1. **One variable at a time.** …`——编号前缀、粗体闭合、句点均完好；1–7 条原则（L8/L10/L12/L14/L16/L18/L20）全部格式规范。**交叉验证**：complex-skills-no-trigger 对照集内同一 skill 的 L8 为 `One variable at a time.** …`（丢失 "1. " 前缀、粗体闭合前移）——dossier 记录的编号缺陷仍存在于 no-trigger 版本中，说明该缺陷在 trigger 版已修复而 no-trigger 集由修复前快照生成（或生成脚本损坏了前缀），详见 §11
- 表格完整性：ROUTING TABLE（L24–35）表头 + 分隔行 + 10 数据行，每行首尾管道符闭合 ✅
- 代码块：4 个围栏（L39/L80/L131/L180 开启，L76/L127/L165/L206 关闭），grep 计数 8 个 ``` 恰好成对 ✅
- 复选框列表：`- [ ]` 格式规范（L210–219）✅

### 6.5 占位符未填充

- 模板内 `[Name]`、`[date]`、`[change X]`、`[metric Y]`、`[Z%]`、`[user psychology/behavior reason]`、`[start + duration]`（L41–75/L183）——这是**有意为之的示例占位**（展示用户应填内容），非未完成填充 ✅
- 无 `TODO`、`FIXME`、`XXX` 等未完成标记 ✅

### 6.6 截断内容

无截断迹象：末行（L219）为完整清单项；无以未闭合语法结尾的段落。文件末尾无换行符（wc -l 218 vs Read 219 行），属轻微格式瑕疵（建议补尾随换行），不影响解析。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name: 小写+连字符 ≤64，匹配目录 | ⚠️ | 37 字符合规；目录名含 `115-` 前缀而 name 不含——系列 19/19 统一惯例，按语料约定判合规，字面不符 spec |
| 2 | description: 第三人称 + WHAT/WHEN/KEYWORDS ≤1024 | ⚠️ | 322 字符 ✅ 结构齐备；但 WHAT（S2）内容与 skill 实际功能不符，质量不达标 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | "Pack template… / Guides the agent…" 第三人称 |
| 4 | description: 无跨 skill 路由 | ✅ | 无 |
| 5 | description: 至少一个触发信号 | ✅ | "Use when the user is implementing…" |
| 6 | frontmatter: 无允许列表外字段 | ✅ | 仅 name+description |
| 7 | body ≤600 行 | ✅ | 214 行 |
| 8 | body: workflow/process 章节 | ✅ | 编号原则 1–7 + ROUTING TABLE 双重载体，系列内最显式 |
| 9 | body: output format 章节 | ✅ | OUTPUT FORMAT（L178–206）完整 |
| 10 | body: scope/limitations 章节 | ❌ | **缺失**——DO NOT 为行为禁令，非能力边界说明 |
| 11 | body: 无跨 skill 文件引用 | ✅ | 无 `../`；murmurhash 为符号级依赖非文件引用 |
| 12 | 目录: NNN-kebab-case 无空格大写 | ✅ | `115-tpl-situacao-ab-testing-implementacao` |

合规得分：9/12 项通过（2 项 ⚠️ 半通过、1 项 ❌）。与 029 完全同构（9/12），符合 tpl 系列的整体合规画像：结构完整但 description 残留 + Scope 缺失是系列共同短板。

---

## 8. 人机感评估

### 8.1 Emoji 审计

全文 emoji 仅 1 个 ✅（L198 "### Decision: **SHIP TREATMENT** ✅"），位于 Experiment Report 模板内。判定：这是**示例文档中的决策状态标记**（模拟报告输出），非装饰性 emoji——与 029 的 4 个 ✅ 同为"示例中数据而非装饰"性质，可接受。若严格执行"零 emoji 政策"可改为 `[SHIP]` 文本，但按语料惯例无需。

### 8.2 全大写/喊叫式语言

- `# SITUATION:`（L6）、`## ROUTING TABLE`（L22）、`## DO NOT`（L167）、`## OUTPUT FORMAT`（L178）、`## QUALITY GATES`（L208）——结构性全大写标题，属系列格式惯例，功能性强 ✅
- 8 条 "**DO NOT**" 为禁令句式，是 spec §3.4 "Anti-patterns over generic advice" 的直接体现，非情绪化喊叫 ✅
- "SHIP TREATMENT"（L198）为模板数据，非指令 ✅
- 与 072-mobile-design（20+ emoji 全大写喊话）形成鲜明对比，本 skill 无任何语气失控 ✅

### 8.3 Persona 语气分析

语气一致：中性、严谨、统计实践者的教学式口吻。金句示例：
- L10 "Post-hoc metric selection is p-hacking."
- L14 "Sticky bucketing is non-negotiable."
- L20 "Technical debt from undead experiments compounds quickly."

这类格言式原则记忆度高且无浮夸，与 029 的 "cattle, not pets" 同类，是 mindset 类的典型优质载体。无营销腔、无讨好式措辞 ✅。

### 8.4 人机边界分析

- body 中无"我是 AI / 作为 agent"类自指 ✅
- **缺失：无显式人类介入点**。与 029（"PR reviewed and approved"、manual approval gate、on-call person informed）不同，本 skill 的 SHIP/NO_SHIP 决策完全由代码逻辑自动化，未设"部署 winner 前需产品/数据负责人确认"类的人类门禁。对 A/B 实验这一后果性行为（上线影响真实用户），语料最佳实践（如 029/036/264）普遍设有决策前人类确认点，本 skill 可补一条（见 §13 O-3）
- ROUTING TABLE 引用用户原话（"Let's just run it and see" L26、"It's significant! Let's ship!" L31）——这是路由表设计中的标准"用户语句→动作"模式，**是有意的交互设计而非受众混淆**（dossier 的"混合语气"评论与此相关，§11 详析）

### 8.5 人称分析

- 全文 "you" 共 5 处：L8 "If you need to test multiple things…"、L10 "What exactly will you measure?"、L18 "when you see a positive result"、L24 路由表表头 "If you encounter"、L50 模板 "pick the most important"——全部为教学式虚拟语气或模板引导语，非指令式 "you should"，且 spec §2.3 的人称限制仅适用于 description，body 内祈使句为正常写法 ✅
- 其余指令为祈使句（"Split into separate sequential experiments" L27、"Filter non-human traffic" L35）——对 agent 的指令，正确 ✅

### 8.6 表格密度检查

body 仅 1 张数据表（ROUTING TABLE 10 行 L24–35）+ 1 组复选框（QUALITY GATES）+ 2 个模板 + 2 个代码块。评估：
- 路由场景用表格天然优于散文（spec §3.4 "Decision trees over prose" ✅），且是全文唯一表格，无表格堆叠问题
- 代码块占比高（68%）但均为功能性载体（分配服务、检验函数、模板），非装饰
- 无需"转自然语言"的表格——本 skill 在表格治理上无问题（优于 029 的 17 项清单堆叠）

---

## 9. 可执行性评估

### 9.1 独立可执行性：8/10

agent 仅凭本 SKILL.md 即可完成"A/B 测试实施"类任务的完整决策与产出：识别场景 → 路由 → 原则 → 设计 → 编码（TS）→ 分析（Python）→ 报告 → 验收，链条闭环，且分析代码可直接运行。扣分项：① 工作示例数字矛盾（§4.3，agent 复算会得出相反结论）；② 样本量计算无工具支撑（§5.2）；③ 无 guardrail 劣化处置分支（§4.4）；④ 无人类确认门禁（§8.4）。

### 9.2 步骤可操作性（逐步骤表）

| 步骤 | 载体 | 可操作性 | 分析 |
|------|------|:--------:|------|
| 场景识别 | description S3 | 9/10 | 触发面覆盖 A/B/多变量/flag 实验 + 统计 rigor 关键词 |
| 场景路由 | ROUTING TABLE L24–35 | 9/10 | if→then 明确，10 类场景全覆盖；缺优先级裁决（§4.4） |
| 原则约束 | L8–20 七原则 | 9/10 | 每条一个可验证主张（单变量、先算样本量、不早停） |
| 实验设计 | Design Template L37–76 | 9/10 | 14 字段模板可直接填充；样本量数值为占位示例 |
| 分配实现 | TS L80–127 | 8/10 | 结构完整；murmurhash 未定义需自行引入 |
| 统计分析 | Python L131–165 | 9/10 | scipy 代码可运行、逻辑正确；置信字段非标准 |
| 产出报告 | Output 模板 L180–206 | 5/10 | **最弱环节**：示例数字（p=0.023/SHIP）与自身代码矛盾，照抄即错 |
| 完成验收 | QUALITY GATES L208–219 | 9/10 | 10 项全部可测（假设/指标/样本量/时长/分配/流量/决策/清理/文档/护栏） |

### 9.3 工具依赖合理性

- 隐含工具依赖：Read（读取实验配置）、Write（编写设计/报告文档）、Bash（运行 Python 分析、查看实验日志）——与 allowed-tools 缺失形成对照（§2.3）
- 外部库依赖：scipy（标准科学计算库，合理）；murmurhash（需引入第三方 npm 包，未声明）——无超出常见 harness 的依赖（无 MCP、无外部 API）✅
- 平台假设：无（与 029 的 GitHub Actions 假设不同，本 skill 平台中立，更好）

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml（155/155 行，YAML 解析通过，top keys: skill/pattern/total_items/criteria/critical_failures）定义 17 个 criteria，`total_items: 17` 与 criteria 实际数量一致 ✅。分类计数：scope 3、process 5、statistics 3、output 3、negative 2、qa 1 = 17 ✅。judge 分布：llm 11、script 6 ✅。逐一与 SKILL.md 内容对证：

| ID | 类别 | 测评点 | SKILL.md 支撑 | 对齐 |
|----|------|--------|--------------|:----:|
| SCOPE-01 | scope | 任务是 A/B 测试实施/分析/部署 | description S3 + H1 标题（L6） | ✅ |
| SCOPE-02 | scope | 单变量实验，无混淆混改 | 原则 1（L8）+ 路由行 2（L27） | ✅ |
| SCOPE-03 | scope | 指标与假设先于分流定义 | 原则 2（L10）+ 模板（L41–50）+ DO NOT 2（L170） | ✅ |
| PROC-01 | process | 样本量 power analysis 先行（80%/95%） | 原则 3（L12）+ 模板（L62–63） | ✅ |
| PROC-02 | process | sticky bucketing 确定性分配 | 原则 4（L14）+ TS getVariant/assignAndLog（L93–125） | ✅ 脚本可命中 |
| PROC-03 | process | 满时长运行不早停 | 原则 5/6（L16/L18）+ 路由行 5（L30）+ DO NOT 3（L171） | ✅ |
| PROC-04 | process | bot 流量过滤 | DO NOT 8（L176）+ 路由行 10（L35） | ✅ |
| PROC-05 | process | winner 清理（删变体+删 flag） | 原则 7（L20）+ 路由行 8（L33）+ Next Steps（L202–203） | ✅ 脚本可命中 |
| STAT-01 | statistics | 正确检验（two-proportion z-test, α=0.05） | Python L148–154 + 路由行 6（L31） | ✅ 脚本可命中 |
| STAT-02 | statistics | 主指标不后改 | DO NOT 2（L170）+ 原则 2（L10） | ✅ |
| STAT-03 | statistics | 样本量达标后才分析 | 原则 3（L12）+ DO NOT 1（L169）+ 路由行 3（L28）+ 报告 14,200≥12,400 | ✅ |
| OUT-01 | output | 报告含时长/总访客/分变体表 | OUTPUT FORMAT（L184–194） | ✅ 脚本可命中 |
| OUT-02 | output | 报告含 p-value/lift/建议 | OUTPUT FORMAT（L195–198） | ✅ 脚本可命中 |
| OUT-03 | output | Next Steps 清单 | OUTPUT FORMAT（L200–205） | ✅ 脚本可命中 |
| NEG-01 | negative | 主指标平时不按次要指标决策 | DO NOT 4（L172）+ 模板（L52–56 Secondary=monitoring） | ✅ |
| NEG-02 | negative | 同用户多会话不独立计数 | DO NOT 6（L174）+ 原则 4（L14） | ✅ |
| QA-01 | qa | guardrail 指标无劣化 | 模板 Guardrail Metrics（L58–60）+ QUALITY GATES 10（L219） | ✅ |

**17/17 全部有 body 内容支撑**，覆盖率与 029（15/15）同为系列上游水平。

### 10.2 Critical Failures 分析

- CF-01 "样本量未达标即分析决策" → `cap_to_0`：对应原则 3（L12）、DO NOT 1（L169）、路由行 3（L28）三重约束 ✅
- CF-02 "结论后遗留败者代码或 flag" → `cap_to_0`：对应原则 7（L20）、DO NOT 5（L173）、路由行 8（L33）、QUALITY GATES 8（L217）四重约束 ✅
- 判定合理：两条均为 A/B 实践中"不可逆的高危行为"（数据不可修复 / 技术债持续侵蚀），cap_to_0 恰当
- 未覆盖的高危行为（可选补充）：guardrail 指标严重劣化仍继续运行（QA-01 仅 llm 判定且无止损语义）；"把统计显著当业务显著直接上线而无人工复核"——与 §8.4 的缺人工门禁同源，可考虑 CF-03 候选（见 §13 O-6）

### 10.3 check.py 与 SCORING 一致性

- 6 个 `judge: script` 项（PROC-02/PROC-05/STAT-01/OUT-01/OUT-02/OUT-03）与 check.py L38–51 的 6 个判定**一一对应**，正则逐字符一致 ✅
- 其余 11 项均为 `judge: llm`，check.py 中正确注释跳过（L33–59 注释块）✅
- check.py 只返回 6 个键，无遗漏、无多余 ✅（详细代码审查见 §5.4）
- 测评稳健性备注：`output_contains` 大小写敏感（checker.py L339–345 无 IGNORECASE），OUT-02 的 "Relative Lift" / OUT-03 的 "Deploy treatment" 均依赖 agent 严格按模板措辞输出——模板即答案，实测通过率高，但评估说明中应注明此特性

---

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier（Batch 101-125 区段，L764–769）评级：**🟡**。逐项验证：

| # | Dossier 声称 | 当前版本验证 | 结论 |
|---|-------------|------------|:----:|
| 1 | "115 AB 测试规则与统计指导扎实" | 7 条原则 + 10 行路由 + 3 个代码块全部技术正确、交叉锚定 12 组一致（§4.1） | ✅ 属实 |
| 2 | "同样编号故障——规则列表从 '2.' 开始缺 '1.'" | L8 原始字节为 `1. **One variable at a time.**`，编号与粗体闭合完好；1–7 条全部规范。**交叉发现**：complex-skills-no-trigger 对照集内同一 skill 的 L8 为 `One variable at a time.**`（前缀丢失），缺陷仍存在于 no-trigger 版 | ❌ **trigger 版无法复现**——编号缺陷已在 trigger 集修复（疑为 2026-08-05 tpl28/28 批次修复），但 no-trigger 对照集由修复前状态生成（或生成脚本损坏了前缀），两集间存在派生时差 |
| 3 | "混合语气——规则部分对用户、部分对 agent" | 部分属实：ROUTING TABLE 引用用户原话（L26/L31）是有意的"用户语句→动作"路由设计（§8.4）；"you" ×5 全部为教学修辞。dossier 的"混合语气"评语可以理解但**设计上正当**，不属于受众混淆 | ✅ 属实但非缺陷 |
| 4 | "Frontmatter 合规；workflow/output/DO-NOT 存在" | 确认：name/description 合法、workflow（原则+路由）、OUTPUT FORMAT、DO NOT 齐全；但无 Scope 节（dossier 未提及） | ✅ 属实（Scope 缺失为增量发现） |
| 5 | 总评 "🟡 良好严谨性，被编号缺陷拖累" | 编号缺陷已不存在；但存在 dossier 未记录的**输出示例数字矛盾**（§4.3，与 074-social-media-analyzer 同类问题）与 description 模板残留 | 评级维持 🟡（理由更新，见 §12） |

**总评**：dossier 🟡 评级维持（不升不降）。关键增量发现：① dossier 记录的头号缺陷（编号断裂）在当前 trigger 版本不复现（修复有效），但 no-trigger 对照集仍带该缺陷——对 SkillIF 实验的数据一致性有意义（对照集需从修复后的 trigger 集重新生成，否则 description 之外的 body 差异会污染 trigger 效应测量）；② dossier 未记录的 OUTPUT FORMAT 示例数字矛盾是比编号缺陷更实质的问题——统计类 skill 的示范与自身代码互相拆台。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数/10 | 权重 | 加权 | 说明 |
|------|:------:|:----:|:----:|------|
| Frontmatter | 5 | 10% | 0.50 | description 约 52% 为模板残留（S1/S2），S3 为语料最优触发句之一；allowed-tools 缺失 |
| Body 结构 | 8 | 10% | 0.80 | 层级规整、7 个 H2 章节齐全、workflow 显式；无 Scope 节 |
| 逻辑一致性 | 7 | 20% | 1.40 | 12 组交叉锚定全部一致，原则-模板-代码-报告四层闭环；但输出示例 p 值（0.023 vs 实际 0.078）与自身代码矛盾，对统计类 skill 是实质性缺陷 |
| 参考完整性 | 9 | 15% | 1.35 | 自包含零文件引用 ✅；扣分于 murmurhash 未声明依赖与样本量计算无工具支撑 |
| 语法格式 | 9 | 10% | 0.90 | 零拼写错误、粗体 76 个全配对、4 围栏完整、无葡语残留；末行缺换行 |
| 规范合规 | 7 | 15% | 1.05 | 12 项中 9 通过、2 半通过、1 缺失（Scope）——系列共同画像 |
| 人机感 | 8 | 10% | 0.80 | 严谨实践者语气、1 个 ✅ 属数据标记、格言式原则优质；缺人类确认门禁 |
| 可执行性 | 8 | 10% | 0.80 | 决策闭环完整、Python 代码可运行；输出示例矛盾 + 样本量无工具拖累 |
| **总分** | | | **7.60/10** | |

### 12.2 评级: 🟡 B+（76/100）

与 029（7.90，🟡 B+）对比：结构、语法、参考完整性维度同级；差距在两处——① 029 零逻辑矛盾（逻辑 9/10 vs 本 skill 7/10），本 skill 的输出示例数字矛盾是"统计 rigor"类 skill 的硬伤；② 029 有人类门禁与 <10min 等量化验收，人机边界更完整。本 skill 的优势是 workflow 更显式、代码可直接运行、S3 触发句更贴合 body。整体为系列中"内容最完整"一档，缺陷集中在三个可低成本修复项（description 残留、Scope 缺失、示例数字矛盾）。

---

## 13. 修复建议（按优先级分层）★ 重点章节 ★

### 🔴 致命缺陷（必须修复）

**F-1: description 模板残留（SKILL.md L3）**

- 问题：S1 "Pack template (situacao/17-ab-testing-implementacao.md)." 暴露内部打包路径，对 agent 无意义；S2 "Guides the agent on situational tasks such as debugging, security and refactoring…" 是 19 个系列 skill 共用的占位文案，与本 skill 的 A/B 测试内容完全无关。"debugging / security / refactoring" 会误导触发（用户问调试任务可能错误命中本 skill）并污染 SCOPE-01 测评判定
- 精确位置：SKILL.md:3
- 修复方向：整行替换为——
  `description: Guides the agent in planning, implementing, and analyzing A/B tests with statistical rigor. Use when the user is implementing A/B tests, multivariate tests, or feature flag-driven experiments and needs hypothesis design, sample size calculation, significance testing, or clean winner deployment.`
  （保留原 S3 触发面并扩充 keyword 覆盖：hypothesis design / sample size / significance testing / winner deployment；若考虑长度可删 "planning,"）
- 不修复后果：触发失真 + SCOPE-01 判定歧义 + 与系列其余 18 个 skill 一起被批量标记模板残留；若系列批量修复而本文件遗漏，会沦为"唯一未修"孤例
- 系列联动建议：同一修复应同步推进至 023/029/030/046/058/059/078/099/100/101/116/132/145/146/168/169/186/210（19 个 skill 的 S2 均需替换为本领域描述）

**F-2: OUTPUT FORMAT 工作示例数字自相矛盾（SKILL.md L182–206）**

- 问题：示例 Control 852/14,200、Treatment 924/14,200 的复算结果（z = 1.765，two-sided p = 0.0776）与示例宣称的 "p-value: 0.023"、"SHIP TREATMENT ✅" 矛盾；按 skill 自身 Python 代码（L162）该数据应判 `NO_SHIP`。agent 依 skill 复算会得出与示范相反的结论——统计类 skill 的示范与实现互相拆台，是最优先修复项
- 精确位置：SKILL.md L186（表格 Treatment 行）、L195（p-value 行）、L196（Relative Lift 行）、L198（Decision 行）
- 修复方向（选项 A，推荐——保留 SHIP 正例）：将 Treatment 转换数 924 改为 **945**，同步更新三处数字：
  - L193 表格：`| Treatment | 14,200 | 945 | 6.66% | +10.9% |`
  - L195 p-value 行：`**p-value:** 0.023 (statistically significant at 95% confidence)` —— 保持 0.023（945/14,200 复算 z = 2.267，p = 0.0234 ≈ 0.023，与声明一致）
  - L196 lift 行：`**Relative Lift:** +10.9% on checkout completion rate`（945 vs 852 的 lift = +10.92%）
  - L198 决策行保持 SHIP TREATMENT ✅（p < 0.05 且 lift 10.9% > MDE 5%，判定成立）
  - 附：MDE 5% 与 12,400 样本量在 power=80% 下所需流量不变（示例仍自洽）
- 修复方向（选项 B，保留数字）：保留 924，将 p-value 改为 0.078、显著性声明改为 "not statistically significant"、Decision 改为 NO_SHIP，Next Steps 改为"继续运行至样本量/重新设计"——但会失去"显著 SHIP"的正例示范价值，且与"14,200 ≥ 12,400"的完整叙事冲突，不推荐
- 不修复后果：本 skill 的可执行性核心环节（产出报告）对 agent 是错误示范；若测评 agent 认真执行分析代码，OUT-01/OUT-02 的脚本命中结果与报告内容自相矛盾，可能造成测评数据噪声；与 074-social-media-analyzer 同级的"示例数字对不上"污点

**F-3: 缺失 Scope/Limitations 章节（body L176 之后）**

- 问题：无 `## Scope`；`## DO NOT`（L167–176）是行为禁令，回答了"agent 不得做什么操作"，但未回答"本 skill 不覆盖什么任务"——如：不覆盖 A/A 对照实验与显著性校准、不做 CUPED/分层/回归调整类高级因果方法、不处理多臂老虎机（MAB）/强化学习类自适应实验、不负责用户调研/可用性测试类非随机实验、不做样本量之外的分析方法选型（贝叶斯检验不在本 skill 范围）、不替代产品/业务决策（统计结论需业务解读）
- 精确位置：SKILL.md:167（DO NOT 之前）或 :208（QUALITY GATES 之前）插入新节
- 修复方向：插入约 10 行：
  ```
  ## SCOPE
  This skill covers classic two-variant A/B experiments: hypothesis design,
  sample size planning, deterministic assignment, two-proportion significance
  testing, winner promotion, and cleanup.
  It does NOT cover: A/A calibration tests, CUPED/stratified/regression-adjusted
  analysis, multi-armed bandit or adaptive experiments, Bayesian methods,
  non-experimental research (surveys, usability tests), or replacing the
  product owner's business decision. For those, the agent should say so and
  offer alternatives instead of applying this skill's procedure.
  ```
- 不修复后果：SKILL-SPEC §3.1 合规第 10 项持续失败（系列 19 个 skill 共有的最大合规缺口）；agent 无边界约束时可能把本 skill 的流程硬套到不适用场景（如对调研数据做 z-test）

### 🟡 重要缺陷（建议修复）

**I-1: 路由表多场景优先级缺失（ROUTING TABLE L24–35）**

- 问题：10 个场景可同时成立（如"样本量不足 + 显著性冒进 + bot 流量未过滤"同时出现），表内无裁决规则；原则 6 的 "or for safety" 亦未定义
- 修复方向：表下加 1 行注记：
  "If multiple rows apply, resolve in this order: (1) sticky bucketing broken — fix assignment first; (2) bot traffic included — filter before anything else; (3) sample size not reached — do not analyze, keep running; (4) safety concerns — stop and escalate; then follow remaining rows."
- 不修复后果：并发场景下 agent 行为不确定，SCOPE/PROC 类测评出现随机性

**I-2: guardrail 劣化处置路径缺失**

- 问题：模板定义了 Guardrail Metrics（L58–60），QUALITY GATES 10 要求"无劣化"（L219），但运行中 guardrail 劣化时"暂停/回滚/报障"的决策路径未定义——原则 6 的 safety 早停无操作化
- 修复方向：ROUTING TABLE 增补 1 行：
  | Guardrail metric (error rate / P95) degrading during run | Stop the experiment, roll back to control, investigate before restarting. Do not make a winner decision on degraded data. |
- 不修复后果：agent 面对"指标恶化"场景无规则可依，可能继续运行并污染结论（QA-01 的 llm 判定缺少行为支撑）

**I-3: 样本量计算无工具支撑（原则 3 L12 / 模板 L65）**

- 问题："Use a power calculator" 是唯一指引，无公式、无代码、无工具名——对要求 statistical rigor 的 skill，这是最不可执行的关键步骤
- 修复方向：在 Statistical Analysis 节（L129–165）追加一个样本量函数（5–8 行）：
  ```python
  from statsmodels.stats.proportion import proportion_effectsize
  from statsmodels.stats.power import NormalIndPower

  def required_sample_size(base_rate: float, mde: float, alpha: float = 0.05,
                           power: float = 0.8) -> int:
      es = proportion_effectsize(base_rate, base_rate * (1 + mde))
      n = NormalIndPower().solve_power(es, power=power, alpha=alpha,
                                       ratio=1, alternative='two-sided')
      return int(n)
  ```
  并在模板 L65 注明 "12,400 is an example — compute with the function above"
- 不修复后果：agent 只能编造样本量数字，PROC-01 的测评结果依赖 agent 外部知识而非 skill 本身

**I-4: murmurhash 未声明依赖（TS L95）**

- 问题：核心分配函数未定义、未注明来源，照抄即 NameError
- 修复方向（二选一）：① L94 注释改为 "// Requires murmurhash-js (npm i murmurhash-js)"；② 内联一个 3 行的确定性哈希（如 FNV-1a）替代
- 不修复后果：agent 产出不可直接运行的前端分配代码；PROC-02 的脚本判定（pattern 含 getVariant/assignAndLog）虽可命中，但代码质量打折

**I-5: confidence 字段非标准（Python L163）**

- 问题：`confidence: f"{(1-p_value)*100:.1f}%"` 不是统计意义的置信区间，对双侧检验也不成立（正确置信度 ≈ (1-p/2)），可能误导 agent 在报告中给用户错误的置信表述
- 修复方向：删除该字段，或替换为
  ```python
  from statsmodels.stats.proportion import proportion_confint
  ci = proportion_confint(treatment_conversions, treatment_visitors, method='normal')
  ```
- 不修复后果：报告模板中出现不严谨的统计表述，与 skill 的 rigor 定位相悖

**I-6: allowed-tools 缺失（frontmatter）**

- 问题：body 隐含 Bash（运行 Python 分析）/Read/Write（设计文档与报告）使用（§9.3），frontmatter 未声明
- 修复方向：L3 后追加 `allowed-tools: Read, Write, Bash, Glob, Grep`
- 不修复后果：工具面不受控；非硬性违规（spec 列为可选），故列 🟡 而非 🔴

**I-7: 文件末尾无换行符（L219 后）**

- 问题：wc -l 218 vs Read 219 行，末行缺 \n，POSIX 工具链与部分 linter 会告警
- 修复方向：文件尾补一个换行
- 不修复后果：极轻微；主要影响后续自动化脚本的文本处理（且与 no-trigger 集的文件对比工具易误报 diff）

### 🟢 优化建议（锦上添花）

**O-1: 报告模板增加失败/回滚分支示例**——当前 OUTPUT FORMAT（L180–206）只有 SHIP 正例；补一段 "Decision: NO_SHIP / rollback triggered" 分支（何时触发、如何回切、事后复盘），与 I-2 的 guardrail 劣化路径形成闭环证据链。

**O-2: QUALITY GATES 增加 lift ≥ MDE 核对**——当前决策标准只有显著性（p < 0.05）；补一条 "- [ ] Relative lift ≥ Minimum Detectable Effect (statistically meaningful, not just significant)"，防止"统计显著但业务无意义"的误上线。

**O-3: 增加人类确认门禁**——SHIP 是后果性行为，参考语料最佳实践（029 的人工审批门、036/264 的人类决策检查点），在 QUALITY GATES 前补一条 "Before shipping: confirm with the product/data owner — significance is statistical, not necessarily business-optimal"。

**O-4: peeking/多重比较纪律落地**——L18 已声明 sequential testing 需预配置，可补一行具体指引："If you check significance repeatedly as data accrues, use alpha-spending (e.g., O'Brien-Fleming) or lower alpha (e.g., 0.01); never use the same 0.05 threshold for multiple looks."，与 I-1 的裁决注记联动。

**O-5: 系列级修复协调**——F-1 的 description 残留与 F-3 的 Scope 缺失是 19 个 tpl-situacao skill 的共同问题，建议一次性系列化修复而非逐文件零散修补；同时**重新生成 complex-skills-no-trigger 对照集**——当前 no-trigger 集仍携带已修复的编号缺陷（§11），与 trigger 集的 body 差异会污染 trigger 效应测量（详情见 §11 增量发现）。

**O-6: SCORING 增强（可选）**——① STAT-03（样本量达标才分析）与 QA-01（guardrail 无劣化）的判定依赖 llm，可考虑补充脚本正则（如 "14,200" vs "12,400" 的比较无法脚本化，维持 llm 合理）；② CF-03 候选："guardrail 指标劣化仍继续运行并做 winner 决策"（cap_to_0），与 I-2 联动；③ 评估说明中注明 `output_contains` 大小写敏感特性（§10.3），避免 "Relative Lift" 小写输出被误判。

### 修复工作量估计

| 项 | 涉及文件 | 预计改动 |
|----|---------|---------|
| F-1 description 重写 | SKILL.md L3 | 1 行替换（系列联动 19 文件） |
| F-2 示例数字订正 | SKILL.md L193/L195/L196/L198 | 4 处数值替换（选项 A） |
| F-3 新增 Scope 节 | SKILL.md L167 前或 L208 前 | +10 行 |
| I-1 优先级注记 | SKILL.md L35 后 | +3 行 |
| I-2 guardrail 劣化行 | SKILL.md L35 后 | +1 行（表格） |
| I-3 样本量函数 | SKILL.md L165 后 | +8–10 行 |
| I-4 murmurhash 注明 | SKILL.md L94 | 1 行 |
| I-5 confidence 修正 | SKILL.md L163 | +3 行替换 |
| I-6 allowed-tools | SKILL.md frontmatter | +1 行 |
| I-7 末行换行 | SKILL.md | +1 字节 |
| O-1~O-6 | SKILL.md / SCORING.yaml / 评估说明 | +15–25 行（可选项） |

合计：**约 45–65 行净增（+21% body），全部集中在 SKILL.md（SCORING.yaml 仅 O-6 可选）**，预计 40–60 分钟工作量，无结构重排，低风险。修复后预计评级可从 🟡 B+ 提升至 🟢 A−：F-2 解决后逻辑一致性升至 9、F-1/F-3 解决后 Frontmatter 升至 8、合规 11/12，加权总分约 8.4–8.6/10。

**优先级执行顺序建议**：F-2（示例数字，30 分钟内）→ F-1（description，与系列批量）→ F-3（Scope，10 行）→ I-3（样本量函数）→ I-1/I-2 → 其余。

---

## 附录: 审查过程记录

| 文件 | 行数（wc -l / Read） | 审查深度 |
|------|:----:|----------|
| D:\SkillIF\skill-experiment\complex-skills\115-tpl-situacao-ab-testing-implementacao\SKILL.md | 218 / 219 | 全文逐行（含 L8 原始字节验证、`**` 计数 76 个、非 ASCII 扫描 5 行、描述长度 322 字符实测、4 围栏成对验证） |
| D:\SkillIF\skill-experiment\complex-skills\115-tpl-situacao-ab-testing-implementacao\SCORING.yaml | 155 / 155 | 全文 + python yaml 解析验证 + 17 criteria 分类/法官计数 + CF 映射 + 6 个脚本正则逐一复现 |
| D:\SkillIF\skill-experiment\complex-skills\115-tpl-situacao-ab-testing-implementacao\check.py | 82 / 82 | 全文 + 与 _shared/checker.py 函数签名逐一对证 + 6 判定与 SCORING 正则逐字符比对 |
| D:\SkillIF\skill-experiment\complex-skills\115-tpl-situacao-ab-testing-implementacao\REVIEW.md | — | 本篇为首版（此前目录无 REVIEW.md） |
| D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md | 162 / 162 | 全文，12 项合规清单逐一对照 |
| D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py | 350 / — | 重点函数（output_contains L339 / set_tool_log_path L224 / set_agent_output L333）签名与大小写语义验证 |
| D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\REVIEW.md | 561 行 | 全量读取作为格式模板与系列横向参照（结构、评分体系、修复建议分层） |
| C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md | — | Batch 101-125 区段 115 条目（L764–769）逐项验证 |
| D:\SkillIF\skill-experiment\complex-skills-no-trigger\115-tpl-situacao-ab-testing-implementacao\SKILL.md | — | diff 对照（编号前缀缺陷的跨集溯源，L8 "1." 丢失仅存在于 no-trigger 版） |

数值复算（scipy/numpy）：OUTPUT FORMAT 示例 z = 1.765 / p = 0.0776（与声明 0.023 矛盾，§4.3）；候选修复 945/14,200 → z = 2.267 / p = 0.0234 / lift +10.9%（§13 F-2）；28,400 = 2 × 14,200、14 天 × 2,029 访客/天、12,400 ≤ 14,200 等一致性核验全部通过。

语料级核查：grep 全语料确认 tpl-situacao 系列 19 个 skill 的 name 约定（去掉 NNN 前缀）与 description 模板残留（19/19 命中 "Pack template (situacao/"）；无跨 skill 文件引用（`../`、`references/`、`scripts/` 均零命中）。

审查人: Claude — 2026-08-06。结论: 🟡 B+ (7.60/10)。核心发现三项：① OUTPUT FORMAT 工作示例 p 值（0.023）与自身数据复算（0.078）矛盾、与自身代码判定（NO_SHIP）冲突——统计类 skill 的示范错误，优先修复；② description S1/S2 模板残留（19/19 系列共病）；③ Scope 缺失（系列共病）。dossier 记录的编号缺陷在当前 trigger 版本已修复，但 no-trigger 对照集仍保留该缺陷（需重新生成以保障实验对照纯净性）。本 REVIEW 为 115 首版，已覆盖全部 17 个 SCORING 测评点的 body 支撑验证。
