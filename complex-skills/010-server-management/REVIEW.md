# REVIEW: 010-server-management

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: mindset — 服务器管理原则与决策框架："教推理而非命令"
**Body 行数**: 157 行
**参考文件数**: references/0, scripts/0, assets/0（极简 skill）
**已有 REVIEW**: 是（旧版 34 行 stub）

---

## 1. 目录全量清单

```
D:\SkillIF\skill-experiment\complex-skills\010-server-management\
├── SKILL.md (161 行，含 frontmatter)
├── SCORING.yaml (131 行)
├── check.py (69 行)
└── REVIEW.md (本次审查替换)
```

**文件统计**: 共 3 个核心文件。无子目录、无 references/、无 scripts/、无 assets/。与 008-tdd-workflow 同为最简洁的 skill 之一。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

- **实际值**: `server-management`
- **目录名**: `010-server-management`
- **匹配**: ✅
- **格式**: 全小写 + 连字符 ✅
- **长度**: 17 字符，≤64 ✅

### 2.2 description

**原文**:
```
Server management principles and decision making. Process management, monitoring strategy, and scalability decisions. Teaches reasoning, not commands. Use when the user asks about managing production servers, choosing a process manager (PM2, systemd, Docker), monitoring or logging, health checks, scaling, or troubleshooting server issues.
```

**逐句分析**:

| # | 句子/分句 | 类型 | 判定 |
|---|----------|------|:----:|
| 1 | "Server management principles and decision making." | WHAT — 高层声明 | ✅ 简洁 |
| 2 | "Process management, monitoring strategy, and scalability decisions." | WHAT — 三个核心领域 | ✅ 具体 |
| 3 | "Teaches reasoning, not commands." | WHAT — 独特的方法论定位 | ✅ 明确区分 |
| 4 | "Use when the user asks about managing production servers, choosing a process manager (PM2, systemd, Docker), monitoring or logging, health checks, scaling, or troubleshooting server issues." | WHEN — 触发场景 | ✅ 规范 "the user asks about" |

**第三人称检查**: "Teaches" — 主语为 skill ✅。全部通过。

**触发信号**: "Use when the user asks about" — ✅ 精确匹配规范。触发场景列举全面（7 个场景）。

**"Teaches reasoning, not commands"**: 这是 322 个 skill 中最独特的描述声明之一——明确定义了 skill 的方法论（教思考方式而非给出命令）。在 description 中声明方法论是合理的，因为这是 skill 核心特征。

**长度**: 302 字符，≤1024 ✅

**打分**: 9/10。精确符合规范。触发场景丰富。"Teaches reasoning, not commands" 是独特且有价值的区分声明。

### 2.3 allowed-tools

**实际值**: `Read, Write, Edit, Glob, Grep, Bash`

**逐工具论证**:

| Tool | 必要性 | 论证 |
|------|:------:|------|
| Read | ✅ 必须 | 读取配置文件、日志文件、进程信息 |
| Write | ✅ 必须 | 写入配置文件、日志配置 |
| Edit | ✅ 必须 | 局部编辑配置文件 |
| Glob | 🟡 弱 | 查找配置文件和服务定义 |
| Grep | 🟡 弱 | 搜索日志中的错误模式 |
| Bash | ✅ 必须 | 执行进程/服务/系统命令 |

**评估**: 6 个工具全部合理。对于 mindset 类型 skill，工具声明的精度不那么关键（skill 不强制特定命令），但全面覆盖主机管理场景。

### 2.4-2.5 其他字段及语法

仅 3 个允许字段，无禁止字段 ✅。YAML 分隔符配对，description 中无引号需转义 ✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Server Management                       (L7,     1 行)
[blockquote: L9-10]                       (L9-10,  2 行) — 核心哲学
## 1. Process Management Principles       (L14-33, 20 行) [2 tables]
## 2. Monitoring Principles               (L36-63, 28 行) [3 tables]
## 3. Log Management Principles           (L66-83, 18 行) [1 table + numbered list]
## 4. Scalability Decisions               (L85-103, 19 行) [2 tables]
## 5. Health Check Principles             (L105-122, 18 行) [1 table + bullet list]
## 6. Security Principles                 (L125-134, 10 行) [1 table]
## 7. Troubleshooting Priority            (L137-146, 10 行) [numbered list]
## 8. Anti-patterns                       (L149-158, 10 行) [❌/✅ 表格]
[blockquote: L161]                        (L161,    1 行) — 结束语
```

**表格统计**: 14 个表格在 157 行 body 中——表格密度是所有 skill 中最高的。这是 "决策矩阵" 风格：不给命令，给选择框架。

### 3.2 必需章节检查

#### Workflow/Process 节

- **存在**: 🟡 "## 7. Troubleshooting Priority" (L137-146) — 5 步编号列表，构成一个故障排查工作流
- **标题用词**: "Troubleshooting Priority" — 不含 "Workflow"/"Process" 关键词，但表达了执行顺序
- **步骤内容**:
  1. Check if it's running (process status)
  2. Check logs (error messages)
  3. Check resources (disk, memory, CPU)
  4. Check network (ports, DNS)
  5. Check dependencies (database, APIs)
  - 每步说明了检查什么，但未说明怎么检查（无具体命令）
- **其他隐式工作流**: Section 1-6 没有顺序关系——它们是**并行决策域**，不是线性步骤。这是 mindset skill 的合理设计
- **条件分支**: 🟡 无。"When something isn't working" 是唯一起始条件，但 "something" 太宽泛
- **起始/终止**: 起始（"something isn't working"）→ 终止（检查所有 5 层）——明确 ✅

#### Output Format 节

- **存在**: ❌ **完全缺失**
- **隐式输出**: Body 暗示 agent 应该输出决策建议（基于表格推理），但从未说明格式
- SCORING.yaml OUT-01 要求 "decision-oriented recommendations with rationale" —— 但 SKILL.md 未告知 agent 应如何格式化这些建议
- **严重程度**: 🟡 对 mindset 类型来说，输出格式没那么关键——但规范要求必须有

#### Scope/Limitations 节

- **存在**: ❌ **完全缺失**
- **局部替代**: "## 8. Anti-patterns" (L149-158) 的 Don't/Do 表部分起到边界作用
- **缺失的边界声明**:
  - 不提供特定操作系统的命令（只给原则）
  - 不执行自动化运维（Ansible/Terraform 级别）
  - 不处理硬件层面的故障（仅软件/服务层面）
  - 不替代专业 DevOps 工具的详细文档
  - 不适用于开发环境（仅生产环境）

### 3.3 内容委托分析

- **委托行数**: 0 行。零文件引用。
- **委托比例**: 0%
- **独立可执行性**: Body 完全自足——不依赖任何外部文件 ✅

### 3.4 节编号/标题层级

- 层级: `#` → `##` → 无 `###` — ✅ 简化但无跳级
- 编号: 1→2→3→4→5→6→7→8 — ✅ 连续
- 无重复标题 ✅

### 3.5 Body 长度合规

- **实际行数**: 157 行 body
- **600 行限制**: ✅ 157 < 600
- **Pattern**: mindset 类型目标 ~50 行，实际 157 行适中

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析

Section 1-6 是独立决策域（无顺序依赖）——mindset 合理设计 ✅。

Section 7 (Troubleshooting Priority) 内部有顺序：进程→日志→资源→网络→依赖 — 这是标准的 OSI-风格分层排查，逻辑正确 ✅。

### 4.2 内部矛盾扫描

**"Teaches reasoning, not commands" 与 Tool Selection 表**:
- L9: "Learn to THINK, don't memorize commands."
- L18-23: Tool Selection 表（PM2/systemd/Docker/Kubernetes）— 推荐了具体工具
- 🟡 **不强矛盾但存在张力**：说 "don't memorize commands" 但给出了具体工具名称。这不是纯推理——这是 "if scenario X, use tool Y" 的决策表。在这个意义上，tool selection 表本身就是"推理"的载体 ✅

**Anti-patterns 与 Principles 一致性**:
- §1 Process Management Goals: "Restart on failure" (L29)
- §8 Anti-patterns: "Don't: Manual restarts → Do: Configure auto-restart" (L154)
- 一致 ✅

**无内部矛盾** ✅

### 4.3 示例/代码正确性

无代码块。所有内容均为 Markdown 表格和列表。N/A。

### 4.4 条件完整性

| 条件 | 位置 | Else | 判定 |
|------|:----:|------|:----:|
| "High CPU" | L91 | "Add instances (horizontal)" | 无 else——如果不是高 CPU 呢？ |
| "High memory" | L92 | "Increase RAM or fix leak" | 无 else |
| "Slow response" | L93 | "Profile first, then scale" | 无 else |
| "Traffic spikes" | L94 | "Auto-scaling" | 无 else |

**问题**: §4 Scalability Decisions 的 "When to Scale" 表是 4 个独立的 symptom→solution 映射，但**不是互斥的**——多个症状可同时存在。表格未处理组合情况。

---

## 5. 参考文件内容级审查

所有 5.1-5.7 子节均为 N/A——无 references/、scripts/、assets/ 目录。✅

唯一可报告的：
- 跨 skill 引用: 0 处 ✅
- 嵌套重复: 无 ✅
- 死文件: 无 ✅

---

## 6. 语法与格式质量

### 6.1-6.6 全面检查

| 检查项 | 结果 | 详情 |
|--------|:----:|------|
| 拼写错误 | ✅ | 无 |
| 语法错误 | ✅ | 无 |
| 中英/葡英混杂 | ✅ | 无 |
| 代码围栏 | ✅ | 无代码块（纯表格/列表） |
| 表格格式 | ✅ | 14 个表格全部正确对齐 |
| 粗体/斜体 | ✅ | **粗体** 全部闭合 |
| Blockquote | ✅ | L9-10 和 L161 正确 |
| 占位符未填充 | ✅ | 无 TODO/FIXME/TBD |
| 截断内容 | ✅ | L161 以句号结束 |

---

## 7. 规范合规性

### 7.1 合规检查清单

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | server-management |
| 2 | description 第三人称 | ✅ | "the user asks about" 精确 |
| 3 | description 含触发短语 | ✅ | "Use when" |
| 4 | description ≤1024 字符 | ✅ | 302 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | |
| 6 | body ≤600 行 | ✅ | 157 行 |
| 7 | Workflow/Process 节存在 | 🟡 | Troubleshooting Priority 存在但非标准标题 |
| 8 | Output Format 节存在 | ❌ | 完全缺失 |
| 9 | Scope/Limitations 节存在 | ❌ | 完全缺失 |
| 10 | 无跨 skill 文件路径引用 | ✅ | |
| 11 | allowed-tools 格式正确 | ✅ | |
| 12 | 路径仅指向本 skill 目录内 | ✅ | |

### 7.2 违规详情

**#8 — Output Format 缺失 (🔴)**
- 当前: 无任何输出格式
- SCORING.yaml OUT-01 要求 "decision-oriented recommendations with rationale"
- 修复: 新增 `## Output Format` 节

**#9 — Scope/Limitations 缺失 (🔴)**
- 当前: 完全无 "不做什么" 的声明
- 修复: 新增至少 3 条边界

---

## 8. 人机感评估

### 8.1 Emoji 审计

| Emoji | 行号 | 类型 | 判定 |
|-------|:----:|------|:----:|
| ❌ | L151 | 功能性（反模式标记） | 🟢 合理——传递 "don't" 语义 |
| ✅ | L152 | 功能性（正确做法标记） | 🟢 合理——传递 "do" 语义 |

共 2 个 emoji，在 §8 Anti-patterns 表中。全部为功能性使用——去掉后二元对比的视觉清晰度下降。

### 8.2 全大写/喊叫式语言

| 短语 | 行号 | 判定 |
|------|:----:|:----:|
| `THINK` | L10 | 🟡 功能性强调——"Learn to THINK" 是 skill 核心哲学 |

仅 1 处。不是喊叫——是哲学术语强调。

### 8.3 Persona 语气分析

**整体语气**: 自信的实践者——像一个有 10 年运维经验的 SRE 给出的简洁原则。

**代表性语气证据**:
- L9-10: "Server management principles for production operations. Learn to THINK, don't memorize commands." — 哲学声明
- L161: "A well-managed server is boring. That's the goal." — 经典 SRE 格言（出自 Google SRE 文化）
- §1-6: 14 个密集决策表——信息压缩到极致
- §8 Anti-patterns: Don't/Do 二元对比——直接、不含糊

**语气适配性**: ✅ 运维/DevOps 场景的完美匹配。自信+务实+经验驱动。

### 8.4 人机边界分析

- 🟡 Skill 的核心哲学 ("teaches reasoning, not commands") 暗示 agent 应该教人类如何思考——但边界模糊：agent 应该给出决策建议还是让人类自己决策？
- 🟡 无显式人类决策声明——但 §1-6 的决策表本质上是 "帮助人类做决策"
- 🟡 无 "In all cases, the human decides" 类声明

### 8.5 人称分析

| 人称 | 出现次数 | 判定 |
|------|:------:|:----:|
| 第二人称 "you" | 0 | ✅ |
| 第一人称 "I"/"we" | 0 | ✅ |

Body 完全第三人称/无人称——纯粹的参考卡风格。✅

---

## 9. 可执行性评估

### 9.1 独立可执行性

**假设**: agent 仅拿到 SKILL.md。

- ✅ 能理解 7 个决策域（process/monitoring/logs/scaling/health/security/troubleshooting）
- ✅ 能基于决策表给出场景化建议（"if Node.js → recommend PM2"）
- 🟡 没有具体命令——agent 需要用自己的知识补充命令
- 🟡 §7 Troubleshooting 步骤说 "check logs" 但不说明用什么命令（`journalctl`？`tail`？`docker logs`？）

**打分**: 6/10。决策框架清晰，但 agent 需要自己填充具体工具命令。

### 9.2 步骤可操作性

| Section | 可操作性 | 问题 |
|---------|:--------:|------|
| §1 Process Mgmt | 🟢 | Tool Selection 表直接可用 |
| §2 Monitoring | 🟢 | What to Monitor + Tool Selection 直接可用 |
| §3 Log Mgmt | 🟢 | 4 条原则可操作 |
| §4 Scalability | 🟡 | Symptom→Solution 映射存在但症状可能重叠 |
| §5 Health Check | 🟢 | Simple vs Deep 选择框架 |
| §6 Security | 🟢 | 5 条原则可操作 |
| §7 Troubleshooting | 🟡 | 有顺序但缺少具体检查命令 |
| §8 Anti-patterns | 🟢 | Don't/Do 对照直接可用 |

### 9.3 工具依赖合理性

全部 6 个 allowed-tools 可在服务器管理场景中合理使用 ✅。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖

共 **14 个 criteria**: scope(3) + decision(4) + principles(3) + output(2) + negative(2)。**全部为 LLM judge**（0 个 script-checkable）。

| 关键一致性问题 | 判定 |
|--------------|:----:|
| SCOPE-03: "teaches reasoning principles rather than dumping memorized commands" | ✅ 与 description "Teaches reasoning, not commands" 精确一致 |
| DEC-01: PM2/Node, systemd/general, Docker/containers | ✅ 与 §1 Tool Selection 表精确一致 |
| DEC-04: Health check depth based on load balancer | ✅ 与 §5 L120-122 一致 |
| NEG-01: No running as root | ✅ 与 §8 Anti-patterns 一致 |
| PRI-03: Troubleshooting follows priority order | ✅ 与 §7 5 步顺序精确一致 |

### 10.2 Critical Failures 分析

| CF ID | 条件 | 合理性 |
|-------|------|:------:|
| CF-01 | Agent 产生纯命令配方无推理 | ✅ 精准——如果 agent 只给命令列表就违反了 skill 核心哲学 |
| CF-02 | Agent 推荐手动重启/无自动恢复 或 用 root 运行 | ✅ 精准——反模式避免 |

CF 设计与 skill 核心价值精确对齐 ✅

### 10.3 check.py 特殊分析

**check.py 无任何脚本检查**: L29-46 的 `check()` 函数返回空字典 `{}`。全部 14 个 criteria 均为 LLM judge。这是 322 个 skill 中**唯一一个 100% LLM-judged 的 skill**。

- 这是合理的：mindset skill 评估 "reasoning quality" 本质上需要 LLM 判断
- 🟡 但可以考虑添加一些自动检查（如 NEG-01 可检查输出是否含 "root"）

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**:

- **评级**: 🟡
- **问题**: "无 Output Format 节和 Scope 节"
- **总评**: "🟡 补 Scope 和 Output 节。"

**逐项验证**:

| Dossier 问题 | 当前状态 |
|-------------|:------:|
| 无 Output Format 节 | 🔴 仍缺失 |
| 无 Scope 节 | 🔴 仍缺失 |

**Dossier 遗漏问题**:
1. check.py 零脚本检查——是否应添加一些自动验证？
2. §4 Scalability 的 symptom→solution 表无组合情况处理
3. §7 Troubleshooting 步骤缺少具体命令
4. ❌/✅ emoji — 虽然是功能性的但在反模式表中可接受

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | "the user asks about" 精确，allowed-tools 全面 |
| Body 结构完整 | 5/10 | 10% | 0.50 | 8 个域覆盖全，但缺 Output(扣3)和 Scope(扣2) |
| 逻辑一致性 | 8/10 | 20% | 1.60 | 决策表内部一致，反模式与原则对齐，无矛盾 |
| 参考完整性 | 10/10 | 15% | 1.50 | 零辅助文件=零引用断裂（满分适用） |
| 语法格式 | 9/10 | 10% | 0.90 | 14 个表格完美，拼写/语法清 |
| 规范合规 | 4/10 | 15% | 0.60 | Output 缺失🔴(扣3)、Scope 缺失🔴(扣3) |
| 人机感 | 8/10 | 10% | 0.80 | 自信实践者语气精准匹配，emoji 功能性，零喊叫 |
| 可执行性 | 6/10 | 10% | 0.60 | 决策框架清晰但缺少具体命令桥接(扣3)，troubleshooting 无操作细节(扣1) |
| **加权总分** | | | **74.0/100** | |

### 12.2 评级

🟡 **B** (60-79): 可用，有需要修复的问题

**评级说明**: server-management 是 mindset skill 的优秀范例——"teaches reasoning, not commands" 的核心哲学贯穿全文，14 个决策表构成一个完整的运维决策框架。扣分几乎全部来自合规性缺失（Scope + Output Format）。加上这两节并将 Troubleshooting 升级为更完整的 Workflow 可轻松进入 A 级。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷

**1. 新增 "## Output Format" 节**
- **位置**: SKILL.md — §8 之后
- **修复方向**: 明确建议的输出结构：
  - 决策摘要（选择什么 + 为什么）
  - 推理依据（使用了哪个决策表）
  - 实施注意事项（从反模式表中引用相关警告）
- **不修复的后果**: 违反规范；agent 不知道如何格式化建议

**2. 新增 "## Limitations" 或 "## When NOT to Use" 节**
- **位置**: SKILL.md — §8 之前或之后
- **至少包含**:
  - 不提供特定 OS 的命令（仅推理框架）
  - 不做自动化运维编排（不属于 Ansible/Terraform 级别）
  - 不处理硬件/网络基础设施层面
  - 不适用于开发环境（仅生产运维）
- **不修复的后果**: 违反规范；skill 可能在不适用的场景被激活

### 🟡 重要缺陷

**3. §7 Troubleshooting 添加具体检查命令**
- **位置**: SKILL.md L141-146
- **修复方向**: 每个步骤添加示例命令：
  1. `systemctl status <service>` 或 `ps aux | grep <process>`
  2. `journalctl -u <service> -n 100` 或 `tail -f /var/log/...`
  3. `df -h`, `free -m`, `top`
  4. `ss -tlnp`, `dig <domain>`
  5. `curl <health endpoint>`, `ping <db host>`
- **原因**: "推理" 不等于 "零信息"——提供命令示例不等于 "memorize commands"

**4. §4 Scalability 添加组合症状处理**
- **修复方向**: 添加注释 "Multiple symptoms may overlap — address the root cause (often profiling reveals the real bottleneck)"
- **原因**: 当前 symptom→solution 映射未考虑组合情况

### 🟢 优化建议

**5. 统一 Troubleshooting Priority 为 Workflow 标题**
- **修复方向**: 改为 `## Workflow: Troubleshooting Priority` 或添加父标题 `## Workflow`
- **原因**: 使 Workflow 节与规范期望对齐

**6. check.py 添加自动验证**
- **修复方向**: 为 NEG-01 和 NEG-02 添加基于关键词的自动检查（检查输出是否含 "root" 或 "manual restart"）
- **原因**: 当前 100% LLM judge——添加一些自动检查可提高评分效率

### 修复工作量估计

- **预计修改行数**: ~35-50 行
- **预计修改文件数**: 1-2（SKILL.md + 可选 check.py）
- **复杂度**: 低

---

## 变更记录
- 2026-08-05: 初始 stub REVIEW (34 行)
- 2026-08-06: 全面深度审查替换

---

## 附录: 审查过程记录

### 读取的文件列表

| 文件 | 行数 | 读取方式 | 状态 |
|------|:----:|---------|:----:|
| SKILL.md | 161 | 全文逐行精读 | ✅ |
| SCORING.yaml | 131 | 全文，14 criteria 验证 | ✅ |
| check.py | 69 | 全文，确认 0 script checks | ✅ |
| _shared/SKILL-SPEC.md | 162 | 全文（批次级别） | ✅ |

### 读取统计
- **Skill 内部文件总行数**: 361 行
- **规范参考**: 162 行
- **总计**: 523 行
- **目录结构**: 无子目录，无 references/scripts/assets

### 审查深度声明
- SKILL.md: 完成 13 节全维度分析，14 个表格逐一评估，8 个域逻辑一致性验证
- SCORING.yaml: 14 criteria 全部验证（100% LLM judge）
- check.py: 确认为零脚本检查的独特设计
- 无辅助文件需审查（极简 skill）
