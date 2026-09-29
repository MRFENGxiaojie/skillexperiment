# REVIEW: 029-tpl-situacao-deployment-devops

**审查日期**: 2026-08-06
**Skill 类型**: mindset — 部署管道/DevOps 情境路由指南（CI/CD、环境一致性、密钥管理、健康检查、零停机策略、回滚）
**Body 行数**: 165 行（L6–L170；文件按 wc -l 计 169 行，末行无换行符，Read 显示至 L170）
**参考文件数**: references/0, scripts/0, assets/0, 其他/0（SCORING.yaml 与 check.py 为评估附属文件，非 skill 参考资源）
**前版 REVIEW**: 161 行部分审查（2026-08-06），本文为其全量重写，保留有效发现并修正其事实错误

---

## 1. 目录全量清单

Glob `**/*` 结果：目录内仅 4 个文件，无任何子目录（references/、scripts/、assets/、templates/ 均不存在），属于极简自包含结构。

```
D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\
├── SKILL.md     (169 行 wc / 170 行 Read；body 自 L6 起 = 165 行)
├── SCORING.yaml (139 行 wc / 140 行 Read；YAML 解析通过)
├── check.py     (73 行 wc / 74 行 Read)
└── REVIEW.md    (161 行；本文件将覆盖)
```

结构评估：技能内容完全内嵌于 SKILL.md，无外部参考文件。对于 mindset 类（规范目标 ~50 行）而言，165 行 body 偏长但未超 600 行硬上限，属于"内容自足型"写法。与 tpl-situacao-* 系列（19 个 skill，见 §5.5）共享结构骨架：`SITUATION: <主题>` + 编号原则列表 + ROUTING TABLE + DO NOT + OUTPUT FORMAT + QUALITY GATES。

---

## 2. Frontmatter 逐字段审查

Frontmatter 共 4 行（L1–L4）：`name` + `description`。无其他字段，无禁止字段。

### 2.1 name

- 实际值：`tpl-situacao-deployment-devops`（L2），30 字符 ≤ 64 ✅
- 字符集：小写字母 + 连字符 ✅
- 目录匹配：目录为 `029-tpl-situacao-deployment-devops`，name 缺少 `029-` 前缀。**严格对照 SKILL-SPEC §1.1/§4 属于不匹配**；但经全语料核查，19/19 个 tpl-situacao 系列 skill（023/029/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210）全部采用"name 去掉 NNN 前缀"的同一约定，属系列性惯例而非本文件孤例。判定：✅（系列约定内一致），在 §7 中注明 spec 字面差异。

### 2.2 description（L3，共 319 字符 ≤1024 ✅）

完整原文：

> "Pack template (situacao/10-deployment-devops.md). Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context. Use when the user is setting up or improving a deployment pipeline — CI/CD, environments, secrets management, health checks, rollbacks, or a production go-live."

逐句分析（S1/S2/S3 分句）：

| 分句 | 原文 | 功能 | 判定 |
|------|------|------|------|
| S1 | "Pack template (situacao/10-deployment-devops.md)." | 元信息 | 🔴 内部打包路径残留，对 agent 无任何行为意义，应删除 |
| S2 | "Guides the agent on situational tasks such as debugging, security and refactoring aligned with this context." | WHAT | 🔴 通用模板文案 — "debugging, security and refactoring" 与本 skill 的部署/DevOps 内容**完全无关**（本 skill 不含任何调试、安全审计或重构指导），会造成错误触发与测评时 SCOPE-01 判定歧义 |
| S3 | "Use when the user is setting up or improving a deployment pipeline — CI/CD, environments, secrets management, health checks, rollbacks, or a production go-live." | WHEN+KEYWORDS | ✅ 触发描述准确，与 body 内容（CI/CD 模板、环境、密钥、健康检查、回滚）一一对应 |

补充验证：经全语料 grep，S1+S2 这段"Pack template (situacao/…). Guides the agent on situational tasks such as debugging, security and refactoring"在 **19/19 个 tpl-situacao 系列 skill 中逐字重复**（含 023、030、046、059 等），确认是 pack 模板生成时的统一占位文案，属系列级缺陷而非单文件问题。

评分：5/10。S3 正确且 KEYWORDS 覆盖良好，但 S1/S2 占据 2/3 篇幅且内容误导。

**修改建议**（替换整行）：
> "Guides the agent in setting up and improving deployment pipelines. Use when the user is configuring CI/CD, environments, secrets management, health checks, rollbacks, or preparing for a production go-live."

### 2.3 allowed-tools

❌ 缺失。SKILL-SPEC §1.2 将 `allowed-tools` 列为**可选**字段，缺失不构成合规失败；但本 body 多处指示执行 shell 命令（L88 `npm ci`、L165 `node --version`、L98/L108 `./scripts/deploy.sh`）以及 CI 配置编写（Read/Write），建议补充 `Read, Write, Bash, Glob, Grep` 以约束 harness 工具面。

### 2.4 其他 frontmatter 字段

无。未使用 §1.3 禁止列表中的任何字段 ✅。

### 2.5 Frontmatter 语法

YAML 结构合法：`---` 包裹（L1/L4），name/description 均为一键一行，值含冒号与破折号但无双引号包裹——YAML 解析无冲突（description 中首个冒号出现在 "situacao/10-deployment-devops.md)" 之后，为键值分隔符，后续冒号在无引号 flow 中合法）。经 python yaml.safe_load 验证 SKILL.md 可解析（SCORING.yaml 解析详见 §10）。

---

## 3. Body 逐段结构分析

### 3.1 段落清单（标题树 + 行数）

```
L6   # SITUATION: Deployment & DevOps Pipeline Setup        (H1)
L8–21   编号原则 1–7（每条一行，加粗标题句 + 解释句）        (14 行)
L22 ## ROUTING TABLE                                        (1 行标题)
L24–35   表头 + 10 行 if→then 场景映射                       (12 行)
L37 ## Deployment Checklist (Pre-Deploy)                    (1 行标题)
L39–44   ### Code Readiness    5 项                          (6 行)
L46–50   ### Environment Readiness  4 项                     (5 行)
L52–56   ### Monitoring Readiness  4 项                      (5 行)
L58–62   ### Rollback Readiness  4 项                        (5 行)
L64 ## Zero-Downtime Deployment Strategies                  (1 行标题)
L66–71   4 行策略表（Strategy/Use When/Complexity/Rollback Speed）(6 行)
L73 ## CI/CD Pipeline Template (GitHub Actions)             (1 行标题)
L75–111  ```yaml``` 代码块（37 行）                          (37 行)
L113 ## DO NOT                                              (1 行标题)
L115–122   8 条禁令                                         (8 行)
L124 ## OUTPUT FORMAT                                       (1 行标题)
L128–157  Deployment Record 模板示例（```markdown``` 块）   (30 行)
L159 ## QUALITY GATES                                       (1 行标题)
L161–170   10 项验收标准                                     (10 行)
```

标题层级：H1 ×1 → H2 ×7 → H3 ×4（仅 Checklist 内部）。层级无跳跃（无 H1 直接到 H3 的情况），结构规整。

### 3.2 必需章节检查（SKILL-SPEC §3.1）

| 必需章节 | 状态 | 分析 |
|---------|:----:|------|
| Workflow / Process | ⚠️ | 无显式 `## Workflow` 或步骤序列；ROUTING TABLE（L22–35）以"场景→动作"决策表形式充当隐含 workflow，Deployment Checklist（L37–62）提供执行顺序。对 mindset 类可接受，但严格按 spec 属"隐含存在" |
| Output Format | ✅ | `## OUTPUT FORMAT`（L124–157）完整：Deployment Record 模板 + Pre-Deploy Checklist + Timeline + Post-Deploy Metrics + Status |
| Scope / Limitations | ❌ | **无 `## Scope` 或等价章节**。`## DO NOT`（L113–122）提供了 8 条禁令（行为约束），但未说明"本 skill 不做什么"（如：不做基础设施 provisioning、不做安全渗透测试、不做成本优化）——这是本 skill 与 dossier 评级相关的核心缺陷 |

### 3.3 内容委托分析

本 skill 零外部委托：无 references/、scripts/ 引用，全部内容内嵌。唯一"委托"是 CI/CD 模板中的 `./scripts/deploy.sh` 与 `./scripts/verify-health.sh`（L98/L100/L108/L110）——这是**模板面向用户仓库的占位脚本**，并非指向本 skill 包内文件（本包无 scripts/ 目录），因此不构成 SKILL-SPEC §3.3 的引用违规，但属于"承诺不存在的资源"，需在 §5.2/§9 中警示。

### 3.4 节编号/标题层级

- 原则列表编号 1–7（L8/L10/L12/L14/L16/L18/L20）连续无跳号 ✅
- ROUTING TABLE 10 行**未编号、无优先级列**——多场景同时触发时（如"密钥泄露 + 周五"）无裁决规则，见 §4.4
- DO NOT 8 条无编号（项目符号），一致 ✅
- 各 H2 节标题为全大写风格（ROUTING TABLE / DO NOT / OUTPUT FORMAT / QUALITY GATES），与系列其他成员一致，非喊叫式（§8.2 详析）

### 3.5 Body 长度合规

165 行（L6–L170）≤ 600 硬上限 ✅。对照 mindset 类目标 ~50 行，超出 3 倍——但内容密度高（7 原则 + 10 场景路由表 + 17 项清单 + 4 策略表 + 37 行 CI 模板 + 30 行输出模板 + 10 项质量门），并非注水冗余，长度可接受。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

Skill 的"决策流"逻辑链完整：

1. 场景识别（description S3 + SCOPE-01）→ 2. 路由（ROUTING TABLE 10 场景）→ 3. 执行约束（7 条原则 + DO NOT 8 条）→ 4. 部署前验证（Checklist 17 项）→ 5. 零停机策略选择（4 策略表）→ 6. 产出（Deployment Record 模板）→ 7. 验收（QUALITY GATES 10 项）。

各环节**互相锚定**，交叉引用验证（关键一致性矩阵）：

| 锚点 A | 锚点 B | 一致性 |
|--------|--------|:------:|
| 原则 5 "/health 返回 200 即健康"（L16） | QUALITY GATES "200 健康 / 503 不健康"（L162） | ✅ 数值一致 |
| 原则 7 "回滚演练 <10 分钟"（L20） | QUALITY GATES "Recovery time < 10 minutes"（L168） | ✅ |
| 路由行 4 "expand-contract 先迁移"（L29） | DO NOT 第 8 条 "迁移与代码部署同步骤禁止"（L122） | ✅ 互补无矛盾 |
| 路由行 3 "无 staging 先建"（L28） | DO NOT "skip staging — ever"（L118） | ✅ |
| 原则 3 "从 artifact 部署"（L12） | QUALITY GATES "immutable artifact tagged with git SHA"（L169） | ✅ |
| 路由行 2 "npm install 出现在生产=错误模式"（L27） | CI 模板在 CI 侧执行 `npm ci`（L87） | ✅ 模板与原则自洽 |
| 原则 6 "监控先行"（L18） | Checklist Monitoring Readiness（L52–56）+ QA-01 | ✅ |

Deployment Record 示例时间线（L144–149）"14:30 Migration started → 14:33 Rolling update started"与"迁移先于代码部署"原则一致 ✅。

### 4.2 内部矛盾扫描

未发现实质性矛盾。逐项核对：
- L14 "Dark launch → canary → full rollout"与策略表（L68–71）的 Feature Flag / Canary 行一致
- L16 "负载均衡器停止路由到不健康实例"与 L162 "503 on unhealthy"一致（健康检查返回 503 使 LB 摘除，是标准实践）
- 原则 1 "cattle, not pets"（L8）与 DO NOT "manually modify production servers"（L119）同源 ✅
- 旧 REVIEW 声称路由表覆盖"database backups"——**不准确**：10 行路由中无备份行，备份仅出现在 Checklist（L50/L61）。旧文描述有误，不影响结论。

### 4.3 示例/代码正确性

CI/CD 模板（L75–111）技术核查：
- `on: push branches [main]` ✅；`actions/checkout@v4` 固定主版本 ✅（未锁 SHA，模板级可接受）
- `npm ci`（L87）比 `npm install` 更优且与原则 3 呼应 ✅
- `environment: staging / production`（L94/L104）+ 注释 "Requires manual approval"（L104）与路由行 5 "受保护环境人工审批"（L30）呼应 ✅
- `${{ github.sha }}` 注入 artifact 标识（L98/L108）与 QUALITY GATES "tagged with git SHA"（L169）呼应 ✅
- 缺陷：① 无 `concurrency` 控制（并发 push 可互相覆盖部署）② 无回滚 job（原则 7 要求回滚 <10 分钟，模板却无 rollback 步骤或 `workflow_dispatch` 回滚入口）③ `./scripts/deploy.sh` / `./scripts/verify-health.sh` 为幻影引用（本包无 scripts/，也未内联其内容）

Deployment Record 示例（L128–157）：字段完整（Version/Environment/Date/Deployer/Changes/Pre-Deploy Checklist/Timeline/Metrics/Status），符合 OUT-01 脚本判定的正则 `[Dd]eployment [Rr]ecord|Deployer|pre-deploy`（SCORING.yaml L96 / check.py L42）——示例本身即可命中 ✅。

### 4.4 条件完整性

- ROUTING TABLE 10 种场景已覆盖：secrets→构建反模式→无 staging→迁移→审批门→环境漂移→无回滚→零停机需求→长时停机→新人首部署。覆盖面广 ✅
- **缺失 1：多场景同时触发无优先级裁决**（如"迁移 + 密钥泄露"或"周五 + 新人部署"）。DO NOT 第 1 条隐含"紧急热修复除外"，但未成规则
- 缺失 2：部分失败（如 rolling update 中途健康检查失败）的处理路径未定义——只有成功时间线示例，无失败分支示例
- 缺失 3：策略表的 "Complexity: High"（Canary）无配套实施门槛说明

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 引用来源 | 引用目标 | 存在? | 判定 |
|---------|---------|:----:|------|
| L98/L100/L108/L110 `./scripts/deploy.sh` | 用户仓库脚本 | N/A | ⚠️ 模板占位，面向用户项目而非本包 |
| L98/L100/L108/L110 `./scripts/verify-health.sh` | 用户仓库脚本 | N/A | ⚠️ 同上 |
| SKILL.md body | references/、scripts/、assets/ | — | ✅ 零引用 |
| SCORING.yaml | check.py 函数 `output_contains` | ✅ | 存在于 `_shared/checker.py` L339 |

skill 包内引用：0 处。跨包引用：0 处（无 `../other-skill/`）✅。

### 5.2 不可见资源审计

最大的不可见资源问题即 §4.3 所述幻影脚本：CI 模板（L98/L100/L108/L110）假设用户仓库存在 `./scripts/deploy.sh` 与 `./scripts/verify-health.sh` 且参数为 `staging|production <sha>`，但 skill 包内**没有**这两个脚本的参考实现，也未在模板旁注明"假定仓库已有这些脚本"。agent 按模板产出后，用户照抄会得到无法运行的 pipeline。修复方向见 §13。

### 5.3 Reference 文件全文审查

无 references/ 目录。本 skill 为自包含模板，不依赖外部知识文件，参考完整性维度得高分（9/10）——但请注意"自包含"与"模板可运行"是两回事（见 §5.2）。

### 5.4 Scripts 文件全文审查

本包无 scripts/。唯一脚本为评估附属 `check.py`（73/74 行），在此与其姊妹库一并审查：

- L1–5 docstring：声明用法与 JSON 输出格式，准确
- L11 `sys.path.insert(0, "../_shared")` 相对路径——**依赖运行 CWD 或固定目录布局**，若从其他目录调用需调整；属评估框架约定，可接受
- L12–15 import：`output_contains`、`set_tool_log_path`、`set_agent_output` — 已逐一对证 `_shared/checker.py`（L339/L224/L333）✅ 存在且签名匹配
- L18 `check(workspace, tool_log, agent_output)`：`workspace` 参数**声明但从未使用**（L20/L59）——无害但冗余
- L23–28：对 `os.path.exists(agent_output)` 的 OSError/ValueError 防御（Windows 长路径兼容）✅ 处理周到
- L42：`result["OUT-01"] = output_contains(r"[Dd]eployment [Rr]ecord|Deployer|pre-deploy")` — 与 SCORING.yaml L96 正则**逐字符一致** ✅
- L54–73 main()：4 参数校验、文件读取、JSON 输出；若 `agent_output` 为文件路径，L64 直接读取并 set，check() 内因 exists=True 跳过重复设置 ✅ 无双重赋值 bug
- 总体：逻辑清晰、库对接正确，唯一脚本化测评点（OUT-01）实现无瑕疵。

### 5.5 跨 Skill 引用检查

- SKILL.md 无跨 skill 引用、无 `../` 路径 ✅
- 系列横向比对（已 grep 全语料）：023/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210 共 19 个 tpl-situacao-* skill，**全部**携带相同的 description 模板残留（"Pack template (situacao/…). Guides the agent on situational tasks such as debugging, security and refactoring…"）——本 skill 的 description 缺陷是系列复制粘贴产物，修复应系列级进行
- 本 skill 的 QUALITY GATES 与 ROUTING TABLE 结构在系列内属最完整一档（与 030 同级）

### 5.6 嵌套重复/死文件检查

- 无嵌套目录、无隐藏文件、无重复内容块 ✅
- body 内无重复段落：ROUTING TABLE 行 8 "Zero-downtime deployment needed" 与策略表（L64–71）内容互补而非重复（一行是路由，一段是选择标准）✅
- 唯一轻微重复：原则 5（L16）与 QUALITY GATES L162 都写 "/health 200/503"——属于"原则重申于验收标准"的正常设计，非冗余

### 5.7 其他资源文件审查

仅 SCORING.yaml（139/140 行）与 check.py，均已在 §5.4 与 §10 详审。目录中无 assets/、templates/、无图片或二进制文件。

---

## 6. 语法与格式质量

### 6.1 拼写错误

全文通读未发现拼写错误。抽查高频词：cattle（L8）、parity（L10）、non-negotiable（L10）、artifact（L12/L169）、canary（L14/L70）、prerequisite（L18）、rollback（L20/L32/L58–62）、readiness（L39–62）、draining（L34）、immutable（L169）——全部正确 ✅。术语使用专业（expand-contract、graceful shutdown、readiness probes、protected environments、dark launch）✅。

### 6.2 语法错误

未发现语法错误。标点使用规范（英文句点、冒号、破折号统一）。唯一风格注意点：L117 "— choose low-traffic windows"、L118 "— ever" 的破折号用法统一，无不完整句 ✅。

### 6.3 葡英混杂

按审查指令，tpl-situacao 系列为**葡语模板系列，葡语元素视为有意**。本文件核查结果：
- 正文 100% 英文，无葡语内容
- 葡语残留仅 1 处：description S1 "Pack template (situacao/10-deployment-devops.md)"（L3）中的 "situacao"——这是 pack 内部路径名（系列命名惯例，无重音符号），属有意系列命名，不计为错误；但该分句本身作为 description 内容是缺陷（见 §2.2）
- skill 名 `tpl-situacao-deployment-devops` 中的 "tpl-situacao" 为系列前缀，有意为之 ✅

### 6.4 Markdown 格式破损

- **粗体配对**：全文 `**` 出现 44 次（偶数）✅ 无未闭合粗体
- **dossier 声称的编号破损不复现**：L8 原始字节验证为 `1. **Every environment is cattle, not pets.** …`——编号前缀、粗体闭合、句点均完好。7 条原则（L8/L10/L12/L14/L16/L18/L20）全部格式规范。该 dossier 缺陷（2026-08-05 记录）要么在记录后已被修复，要么为误报；**当前版本无此问题**
- 表格完整性：ROUTING TABLE（L24–35）表头 + 分隔行 + 10 数据行，每行首尾管道符闭合（含 L34 长行）✅；策略表（L66–71）4 行闭合 ✅
- 代码块：yaml 块 L75–111、markdown 块 L128–157 均正确开闭 ✅
- 复选框列表：`- [ ]` / `- [x]` 格式规范（L40–44 等）✅

### 6.5 占位符未填充

- L131–134 Output 示例中 `**Deployer:** [name]`、`**Changes:** [link to CHANGELOG / PR list]` —— 这是**有意为之的示例占位**（展示用户应填内容），非未完成填充 ✅
- 无 `TODO`、`FIXME`、`XXX` 等未完成标记 ✅

### 6.6 截断内容

无截断迹象：末行（L170）为完整清单项；无以未闭合语法结尾的段落。文件末尾无换行符（wc -l 169 vs Read 170 行），属轻微格式瑕疵（建议补尾随换行），不影响解析。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name: 小写+连字符 ≤64，匹配目录 | ⚠️ | 30 字符合规；目录名含 `029-` 前缀而 name 不含——系列 19/19 统一惯例，按语料约定判合规，字面不符 spec |
| 2 | description: 第三人称 + WHAT/WHEN/KEYWORDS ≤1024 | ⚠️ | 319 字符 ✅ 结构齐备；但 WHAT（S2）内容与 skill 实际功能不符，质量不达标 |
| 3 | description: 无祈使/第一/第二人称开头 | ✅ | "Guides the agent…" 第三人称 |
| 4 | description: 无跨 skill 路由 | ✅ | 无 |
| 5 | description: 至少一个触发信号 | ✅ | "Use when the user is setting up or improving…" |
| 6 | frontmatter: 无允许列表外字段 | ✅ | 仅 name+description |
| 7 | body ≤600 行 | ✅ | 165 行 |
| 8 | body: workflow/process 章节 | ⚠️ | 无显式 Workflow 节，ROUTING TABLE + Checklist 构成隐含流程（dossier 亦认可"workflow 存在"） |
| 9 | body: output format 章节 | ✅ | OUTPUT FORMAT（L124–157）完整 |
| 10 | body: scope/limitations 章节 | ❌ | **缺失**——DO NOT 为行为禁令，非能力边界说明 |
| 11 | body: 无跨 skill 文件引用 | ✅ | 无 `../`；幻影 `./scripts/*.sh` 为模板占位不违规 |
| 12 | 目录: NNN-kebab-case 无空格大写 | ✅ | `029-tpl-situacao-deployment-devops` |

合规得分：9/12 项通过（2 项 ⚠️ 半通过、1 项 ❌）。与旧 REVIEW 的 "8/12 = 67%" 相比，本次将 #1 按系列惯例从 ❌ 调整为 ⚠️、#8 维持 ⚠️，更符合语料实况。

---

## 8. 人机感评估

### 8.1 Emoji 审计

全文 emoji 仅 4 个 ✅，全部位于 Deployment Record 示例内（L152、L153、L154 行尾 "✅" 及 L156 "**Status: Successful ✅**"）。判定：这些 ✅ 是**示例文档中的状态数据标记**（模拟 checklist 勾选结果），非装饰性 emoji——与 dossier "✅ 标记在示例中是数据而非装饰" 的结论一致。⚠️ 注意：旧 REVIEW 声称"零 emoji"，**事实错误**（有 4 个）。若严格执行"零 emoji 政策"仍建议改为 `[PASS]` 文本，但按语料惯例可接受。

### 8.2 全大写/喊叫式语言

- `# SITUATION:`（L6）、`## ROUTING TABLE`（L22）、`## DO NOT`（L113）、`## OUTPUT FORMAT`（L124）、`## QUALITY GATES`（L159）——结构性全大写标题，属系列格式惯例，功能性强，非情绪化喊叫 ✅
- "Stop everything."（L26）、"Wrong pattern."（L27）、"exploratory surgery without anesthesia"（L28）——修辞性强调，贴合运维实践者的果断语气，符合 Anti-patterns over generic advice（spec §3.4）精神 ✅
- SCORING.yaml 内 "BEFORE"（L75）为对比强调，评估文件不计入人机感。

### 8.3 Persona 语气分析

语气一致：直接、果断、技术密度高的 DevOps 实践者口吻。金句示例：
- L8 "Every environment is cattle, not pets."
- L18 "If you cannot observe the service after deployment, you cannot safely deploy."
- L28 "Deployments without staging are exploratory surgery without anesthesia."
- L33 "Rollback must be practiced."

这类格言式原则（meme-style principles）是 mindset 类的典型载体，记忆度高且无浮夸。无营销腔、无讨好式措辞 ✅。

### 8.4 人机边界分析

- body 中无"我是 AI / 作为 agent"类自指（description 的 "Guides the agent" 是模板元描述，非自指）✅
- 人类介入点清晰：PR reviewed and approved（L41）、manual approval gate（L30）、on-call person informed（L55/L121）、pair program 首次部署（L35）、Deployer: [name]（L133）——human-in-the-loop 边界健康 ✅
- 无将 agent 拟人化或把人类排除在决策外的表述 ✅

### 8.5 人称分析

- 全文仅 1 处第二人称：L18 "If **you** cannot observe the service…"——修辞性虚拟语气，非指令式"you should"，风格可接受 ✅
- 其余为祈使句指令（"Move to secrets manager" L26、"Create one before continuing" L28）——对 agent 的指令用祈使句是 skill body 的正常写法（spec §2.3 的人称限制仅适用于 description）
- ⚠️ 旧 REVIEW 声称"零 you/your"，**事实错误**（L18 有 you）。修正：1 处，且为格言式修辞，不扣分。

### 8.6 表格密度检查

body 含 2 张数据表（ROUTING TABLE 10 行 L24–35、策略表 4 行 L66–71）+ 4 组复选框清单 + 1 组指标列表 + 1 组质量门列表。评估：
- 密度合理：路由场景用表格天然优于散文（spec §3.4 "Decision trees over prose" ✅）
- 可优化点：Deployment Checklist 4 个子节（L39–62）共 17 项，其中 Monitoring Readiness（L52–56）与 Environment Readiness（L46–50）条目数少（各 4 项），可考虑合并为 2 节以减表格堆叠——按审查指令"表格过多处建议转自然语言"给 🟢 级建议（详见 §13）
- QUALITY GATES 10 项为清单非表格，无堆叠问题

---

## 9. 可执行性评估

### 9.1 独立可执行性：8/10

agent 仅凭本 SKILL.md 即可完成"部署管道设置/改进"类任务的完整决策与产出：识别场景 → 路由 → 约束 → 清单 → 策略 → 模板 → 记录 → 验收，链条闭环。扣分项：① CI 模板依赖不存在的 `./scripts/*.sh`（§5.2）；② 无具体命令示例（docker build / kubectl rollout / curl /health 均未出现）；③ 失败分支与回滚执行无示例。比旧 REVIEW 的 7/10 高 1 分，因为确认了模板-原则-验收三者的锚定关系与 OUT-01 可命中性。

### 9.2 步骤可操作性（逐步骤表）

| 步骤 | 载体 | 可操作性 | 分析 |
|------|------|:--------:|------|
| 场景识别 | description S3 | 8/10 | 触发面覆盖 CI/CD/环境/密钥/健康检查/回滚/上线 |
| 场景路由 | ROUTING TABLE L24–35 | 9/10 | if→then 明确，10 类场景全覆盖；缺优先级裁决（§4.4） |
| 原则约束 | L8–21 七原则 | 9/10 | 每条一个可验证主张（如 /health、<10min、artifact） |
| 部署前检查 | Checklist L37–62 | 8/10 | 17 项可勾选；"if applicable"（L43）等条件已标注 |
| 策略选择 | 策略表 L64–71 | 8/10 | Use When 列给出选择条件；缺实施细节（Complexity: High 无门槛） |
| 模板落地 | CI 模板 L75–111 | 5/10 | **最弱环节**：幻影脚本 + 无 concurrency + 无回滚 job |
| 产出记录 | Output 模板 L124–157 | 9/10 | 字段齐全，可直接填充 |
| 完成验收 | QUALITY GATES L159–170 | 9/10 | 10 项全部可测（数值阈值明确：1%/2s/10min） |

### 9.3 工具依赖合理性

- 隐含工具依赖：Read（读取仓库 CI 配置）、Write（编写 pipeline 文件）、Bash（`npm ci`/`node --version`/部署脚本执行验证）、Glob/Grep（查找 secrets 与配置）——与 allowed-tools 缺失形成对照（§2.3）
- 无超出常见 harness 的依赖（无 MCP、无外部 API）✅
- GitHub Actions 模板依赖用户仓库在 GitHub 上——description 未限定平台，若用户用 GitLab CI/Jenkins，模板不可复用，需 agent 自行转换；可作为 Scope 补充说明（见 §13）

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

SCORING.yaml（139/140 行，YAML 解析通过，top keys: skill/pattern/total_items/criteria/critical_failures）定义 15 个 criteria，`total_items: 15` 与 criteria 实际数量一致 ✅。分类计数：scope 3、principles 4、decision 3、output 2、negative 2、qa 1。逐一与 SKILL.md 内容对证：

| ID | 类别 | 测评点 | SKILL.md 支撑 | 对齐 |
|----|------|--------|--------------|:----:|
| SCOPE-01 | scope | 首响应识别部署任务 | description S3 + SITUATION 标题（L6） | ✅ |
| SCOPE-02 | scope | 经路由表路由 | ROUTING TABLE L24–35（6 类场景全部有行） | ✅ |
| SCOPE-03 | scope | 环境一致性 | 原则 2（L10） | ✅ |
| PRI-01 | principles | artifact 部署 | 原则 3（L12）+ DO NOT L120 | ✅ |
| PRI-02 | principles | LB 就绪健康检查 | 原则 5（L16）+ GATE L162 | ✅ |
| PRI-03 | principles | 监控前置 | 原则 6（L18）+ Checklist L52–56 | ✅ |
| PRI-04 | principles | 回滚演练 | 原则 7（L20）+ Checklist L58–62 | ✅ |
| DEC-01 | decision | 零停机策略匹配 | 策略表 L66–71 | ✅ |
| DEC-02 | decision | 迁移 expand-contract 先行 | 路由行 4（L29）+ DO NOT L122 | ✅ |
| DEC-03 | decision | 密钥处理 | 路由行 1（L26） | ✅ |
| OUT-01 | output | Deployment Record 产出 | Output 模板 L128–157 | ✅ 且脚本可命中 |
| OUT-02 | output | 部署前清单完成 | Checklist L37–62 | ✅ |
| NEG-01 | negative | 不周五/高峰部署、通知 on-call | DO NOT L115/L117/L121 | ✅ |
| NEG-02 | negative | 不手动改生产、不烤密钥进镜像 | DO NOT L119/L120 | ✅ |
| QA-01 | qa | 质量门全过 | QUALITY GATES L159–170 | ✅ |

**15/15 全部有 body 内容支撑**，覆盖率为系列上游水平。

### 10.2 Critical Failures 分析

- CF-01 "部署跳过 staging" → `cap_to_0`：对应 DO NOT L118 "DO NOT skip staging — ever" 与路由行 3（L28），body 侧有强约束 ✅
- CF-02 "迁移与代码同步骤/高峰迁移" → `cap_to_0`：对应 DO NOT L122 与路由行 4（L29）✅
- 判定合理：两条均为"可一次性破坏生产"的高危行为，cap_to_0 恰当
- 未覆盖的高危行为（可选补充）：直接在容器镜像中烤入环境变量中的密钥（NEG-02 已部分覆盖）；无健康检查直接接流量（PRI-02 覆盖）。CF 集与 DO NOT 8 条映射完整，无需新增。

### 10.3 check.py 与 SCORING 一致性

- OUT-01 是唯一 `judge: script` 项（SCORING L92–96），check.py L42 正则与其逐字符一致 ✅
- 其余 14 项均为 `judge: llm`，check.py 中正确注释跳过（L33–49 注释块）✅
- check.py 只返回 OUT-01，无遗漏、无多余 ✅（详细代码审查见 §5.4）

---

## 11. 已知问题汇总（来自 skill-dossier.md）

dossier（Batch 026-050 区段，L269–274）评级：**🟡**。逐项验证：

| # | Dossier 声称 | 当前版本验证 | 结论 |
|---|-------------|------------|:----:|
| 1 | "编号原则列表破损——第 1 条丢失 '1.' 前缀并以杂散 `**` 结尾" | L8 原始字节为 `1. **Every environment is cattle, not pets.**`，编号与粗体闭合完好；1–7 条全部规范 | ❌ **无法复现**（疑已被修复，或原记录有误） |
| 2 | "无 Scope 节（DO NOT 部分覆盖）" | 确认：无 `## Scope`，DO NOT（L113–122）为禁令非边界说明 | ✅ 属实 |
| 3 | "workflow 和 output 存在" | ROUTING TABLE 隐含 workflow + OUTPUT FORMAT 完整 | ✅ 属实 |
| 4 | "Description 第三人称含触发" | S3 触发句第三人称 ✅（但 S1/S2 残留未在 dossier 中提及） | ✅ 属实 |
| 5 | "169 行 ≤600" | wc -l 169 行 ✅（body 165 行） | ✅ 属实 |
| 6 | "内容强且可操作" | §9 可执行性 8/10，原则-清单-门禁锚定完整 | ✅ 认同 |
| 7 | "✅ 标记在示例中是数据而非装饰" | L152–156 的 4 个 ✅ 确为示例状态数据 | ✅ 认同 |

**总评**：dossier 🟡 评级维持（不升不降）。关键增量发现：dossier 记录的头号缺陷（编号破损）在当前版本不复现——若修复发生在 2026-08-05 之后，本 REVIEW 确认修复有效；同时 dossier 未记录的 description 模板残留（§2.2）与幻影脚本（§5.2）为新增问题。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数/10 | 权重 | 加权 | 说明 |
|------|:------:|:----:|:----:|------|
| Frontmatter | 5 | 10% | 0.50 | description 2/3 为模板残留（S1/S2），S3 正确；allowed-tools 缺失 |
| Body 结构 | 7 | 10% | 0.70 | 层级规整、章节齐全；无显式 Workflow、无 Scope |
| 逻辑一致性 | 9 | 20% | 1.80 | 原则-路由-清单-门禁四层锚定，8 组交叉验证全部一致，零矛盾 |
| 参考完整性 | 9 | 15% | 1.35 | 自包含零引用 ✅；扣分于幻影 scripts 引用 |
| 语法格式 | 9 | 10% | 0.90 | 零拼写错误、粗体 44 个全配对、表格完整；末行缺换行 |
| 规范合规 | 7 | 15% | 1.05 | 12 项中 9 通过、2 半通过、1 缺失（Scope） |
| 人机感 | 8 | 10% | 0.80 | 果断实践者语气、人类介入点清晰；4 个 ✅ 属数据标记可接受 |
| 可执行性 | 8 | 10% | 0.80 | 决策闭环完整；CI 模板幻影脚本与命令示例缺失拖累 |
| **总分** | | | **7.90/10** | |

### 12.2 评级: 🟡 B+（79/100）

与旧 REVIEW（7.55，B+）差异说明：上调 0.35 分，主因是①dossier 编号缺陷经字节级验证**不复现**（修复有效），②参考完整性/语法格式经全量核查高于旧评；旧 REVIEW 的三处事实错误（DO NOT 6 条实为 8 条、零 emoji 实有 4 个、零 you 实有 1 处）已在本次修正。技术内容为系列上游水准，缺陷集中在 description 模板残留与 Scope 缺失两项结构性问题，均属可低成本修复项。

---

## 13. 修复建议（按优先级分层）★ 重点章节 ★

### 🔴 致命缺陷（必须修复）

**F-1: description 模板残留（SKILL.md L3）**

- 问题：S1 "Pack template (situacao/10-deployment-devops.md)." 暴露内部打包路径，对 agent 无意义；S2 "Guides the agent on situational tasks such as debugging, security and refactoring…" 是 19 个系列 skill 共用的占位文案，与本 skill 的部署/DevOps 内容完全无关。"debugging / security / refactoring" 会误导触发（用户问调试任务可能错误命中本 skill）并污染 SCOPE-01 测评判定
- 精确位置：SKILL.md:3
- 修复方向：整行替换为——
  `description: Guides the agent in setting up and improving deployment pipelines. Use when the user is configuring CI/CD, environments, secrets management, health checks, rollbacks, or preparing for a production go-live.`
  （保留原 S3 触发面，新增 WHAT；若考虑 keyword 覆盖可追加 "Triggers on 'deploy', 'CI/CD pipeline', 'release', 'rollback'"）
- 不修复后果：触发失真 + SCOPE-01 判定歧义 + 与系列其余 18 个 skill 一起被批量标记模板残留；若系列批量修复而本文件遗漏，会沦为"唯一未修"孤例
- 系列联动建议：同一修复应同步推进至 023/030/046/058/059/078/099/100/101/115/116/132/145/146/168/169/186/210

**F-2: 缺失 Scope/Limitations 章节（body L113 之后）**

- 问题：无 `## Scope`；`## DO NOT`（L113–122）是行为禁令，回答了"agent 不得做什么操作"，但未回答"本 skill 不覆盖什么任务"——如：不负责基础设施 provisioning（Terraform 云资源创建）、不做安全渗透/漏洞利用、不做成本优化/FinOps、不处理 GitLab CI/Jenkins 等非 GitHub 平台（description 与模板均假设 GitHub Actions）、不替代 on-call 值班流程
- 精确位置：SKILL.md:113（DO NOT 之前或之后插入新节）
- 修复方向：在 QUALITY GATES 之前插入约 8–10 行 `## SCOPE`：
  ```
  ## SCOPE
  This skill covers deployment pipeline setup and improvement: CI/CD,
  environments, secrets, health checks, zero-downtime strategies, and rollback.
  It does NOT cover: infrastructure provisioning (Terraform/cloud resource
  creation), security penetration testing, cost optimization, or CI platforms
  other than GitHub Actions (adapt the template for GitLab CI/Jenkins).
  ```
- 不修复后果：SKILL-SPEC §3.1 合规第 10 项持续失败；agent 无边界约束时可能越界行动（如擅自改云基础设施或重排值班），测评中 Scope 类问题扣分

### 🟡 重要缺陷（建议修复）

**I-1: 幻影脚本引用（SKILL.md L98/L100/L108/L110）**

- 问题：CI 模板引用 `./scripts/deploy.sh` 与 `./scripts/verify-health.sh`，本包无 scripts/ 目录，模板照抄即失败
- 修复方向（三选一）：① 在 L73 标题下加一行说明 "Assumes the repo contains scripts/deploy.sh and scripts/verify-health.sh (deploy: env + git SHA; verify: env + curl /health)";② 将两个脚本的 5–10 行参考实现内联在模板注释中;③ 在 references/ 下补充 deploy-example.sh
- 不修复后果：agent 产出的 pipeline 对用户不可运行，可执行性维度的最大失分点；真实使用中用户需自行补脚本，信任损耗

**I-2: 多场景触发优先级缺失（ROUTING TABLE L24–35）**

- 问题：10 个场景可同时成立（如"密钥泄露 + 周五 + 新人部署"），表内无裁决规则；DO NOT L115 的"emergency hotfix 除外"缺少定义
- 修复方向：表下加 1 行优先级注记：
  "If multiple rows apply, resolve in this order: (1) secrets in code — stop everything; (2) missing staging — create first; (3) rollback missing — document before deploy; then follow remaining rows."
- 不修复后果：并发场景下 agent 行为不确定，DEC/NEG 类测评出现随机性

**I-3: CI 模板缺 concurrency 控制与回滚入口（L75–111）**

- 问题：无 `concurrency`（并发 push 互相覆盖）；无 rollback job 或 `workflow_dispatch` 回滚工作流——与原则 7"回滚 <10 分钟"（L20）的强承诺不对称
- 修复方向：yaml 顶部加
  ```yaml
  concurrency:
    group: production-deploy
    cancel-in-progress: false
  ```
  并在 deploy-production 后追加一个 `rollback` job（或注明"另配 rollback.yml，用 workflow_dispatch 触发前一版本镜像重部署"）
- 不修复后果：模板级实践不完整，agent 给出的"回滚演练"建议缺乏落地载体

**I-4: 缺失具体命令示例**

- 问题：全文无一条可执行命令——`/health` 如何验证（L16/L162 只给状态码）、artifact 如何构建、canary 如何切量均无命令支撑
- 修复方向：在策略表（L66–71）后补 3–5 行命令示例：
  ```bash
  docker build -t app:$SHA .
  kubectl rollout status deploy/app --timeout=5m
  curl -sf http://host/health && echo healthy
  ```
- 不修复后果：可执行性停留在"原则级"，agent 需自行编造命令细节

**I-5: allowed-tools 缺失（frontmatter）**

- 问题：body 隐含 Bash/Read/Write/Glob/Grep 使用（§9.3），frontmatter 未声明
- 修复方向：L3 后追加 `allowed-tools: Read, Write, Bash, Glob, Grep`
- 不修复后果：工具面不受控；非硬性违规（spec 列为可选），故列 🟡 而非 🔴

**I-6: 文件末尾无换行符（L170 后）**

- 问题：wc -l 169 vs Read 170 行，末行缺 \n，POSIX 工具链与部分 linter 会告警
- 修复方向：文件尾补一个换行
- 不修复后果：极轻微；主要影响后续自动化脚本的文本处理

### 🟢 优化建议（锦上添花）

**O-1: Deployment Record 增加失败分支模板**——当前 Output 模板（L128–157）只有成功时间线；补一段"Rollback triggered"分支示例（何时触发、如何回切、事后复盘），与 QUALITY GATES L168 的 <10min 目标形成闭环证据链。

**O-2: 清单条目反向锚定原则编号**——17 项 Checklist（L40–62）可加溯源标注，如 "Feature flags configured — Principle 4"，提升可追溯性（纯文档增益，无行为影响）。

**O-3: 合并小清单减表格堆叠**——Monitoring Readiness（L52–56）与 Environment Readiness（L46–50）各仅 4 项，可合并为一节或转为自然语言段落（响应审查指令"表格过多处转自然语言"）；保留 ROUTING TABLE 与策略表（决策表形式合理）。

**O-4: CF-03 候选**——SCORING.yaml 可考虑新增 CF："无健康检查将流量切入新版本"（cap_to_0），当前 PRI-02 仅 llm 判定，高危行为无硬性止损；非必须，视测评数据而定。

**O-5: 模板加跨平台提示**——L73 标题或 Scope 中注明"模板面向 GitHub Actions；GitLab CI/Jenkins 用户需由 agent 转换"（与 F-2 的 Scope 联动，F-2 落地后可合并）。

**O-6: SCORING OUT-02 可脚本化**——OUT-02 目前为 llm 判定，其正则（如 `Pre-Deploy|Code Readiness|Monitoring`）简单可靠，转为 script judge 可降低测评成本；低优先级。

### 修复工作量估计

| 项 | 涉及文件 | 预计改动 |
|----|---------|---------|
| F-1 description 重写 | SKILL.md L3 | 1 行替换 |
| F-2 新增 Scope 节 | SKILL.md | +8–10 行 |
| I-1 幻影脚本说明/示例 | SKILL.md L73–111 | +5–10 行 |
| I-2 优先级注记 | SKILL.md L35 后 | +3 行 |
| I-3 concurrency + rollback | SKILL.md L75–111 | +6–10 行 |
| I-4 命令示例 | SKILL.md L71 后 | +5 行 |
| I-5 allowed-tools | SKILL.md frontmatter | +1 行 |
| I-6 末行换行 | SKILL.md | +1 字节 |
| O-1~O-6 | SKILL.md / SCORING.yaml | +10–20 行（可选项） |

合计：**约 40–60 行净增，全部集中在 SKILL.md（SCORING.yaml 仅 O-4/O-6 可选）**，预计 30–60 分钟工作量，无结构重排，低风险。修复后预计评级可从 🟡 B+ 提升至 🟢 A−（description 与 Scope 两项 🔴 修复后，规范合规可达 11/12，Frontmatter 升至 8/10）。

---

## 附录: 审查过程记录

| 文件 | 行数（wc -l / Read） | 审查深度 |
|------|:----:|----------|
| D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\SKILL.md | 169 / 170 | 全文逐行（含 L8 原始字节 od 验证、`**` 计数 44 个、非 ASCII 扫描、描述长度 319 字符实测） |
| D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\SCORING.yaml | 139 / 140 | 全文 + python yaml 解析验证 + 15 criteria 分类计数 + CF 映射 |
| D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\check.py | 73 / 74 | 全文 + 与 _shared/checker.py 函数签名逐一对证 |
| D:\SkillIF\skill-experiment\complex-skills\029-tpl-situacao-deployment-devops\REVIEW.md | 161 / 161 | 全文读取，提炼有效发现（description 残留、allowed-tools、优先级列），修正 3 处事实错误 |
| D:\SkillIF\skill-experiment\complex-skills\_shared\SKILL-SPEC.md | 162 行 | 全文，12 项合规清单逐一对照 |
| D:\SkillIF\skill-experiment\complex-skills\_shared\checker.py | 351 行 | 全文（核对 output_contains / set_tool_log_path / set_agent_output 签名） |
| C:\Users\f50058303\.claude\projects\C--Users-f50058303\memory\skill-dossier.md | — | Batch 026-050 区段 029-tpl 条目（L269–274）逐项验证 |

语料级核查：grep 全语料确认 tpl-situacao 系列 19 个 skill 的 name 约定（去掉 NNN 前缀）与 description 模板残留（19/19 命中 "Pack template (situacao/"）。

审查人: Claude — 2026-08-06。结论: 🟡 B+ (7.90/10)。核心缺陷两项（description 模板残留、Scope 缺失）均为结构性小改；dossier 记录的编号破损经字节级验证已不存在（修复确认或记录误差）。本 REVIEW 已全量覆盖旧 REVIEW 的有效发现并修正其全部事实错误。
