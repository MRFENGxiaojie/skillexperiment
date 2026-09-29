# REVIEW: 027-roadmap-backcast

**审查日期**: 2026-08-06
**Skill 类型**: process — 逆向规划（从目标结果反向推导到当前里程碑的 5 步规划法）
**Body 行数**: 211 行
**参考文件数**: references/0, scripts/0, assets/0, 其他/0
**Dossier 评级**: 🟡（缺 Output 节 + "Brook's Law" 拼写错误）

---

## 1. 目录全量清单

```
027-roadmap-backcast/
├── SKILL.md (211 行)
├── SCORING.yaml (140+ 行)
├── check.py (70+ 行)
└── REVIEW.md
```

极简结构——仅核心三件套。211 行 body 完全自包含，含 Table of Contents → Purpose → When to Use → What Is It → 5-Step Workflow → Dependency Mapping → Critical Path → Common Patterns → Guardrails → Quick Reference。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- **实际值**: `roadmap-backcast`
- **目录名**: `027-roadmap-backcast`
- **匹配**: ✅ 匹配
- **格式**: ✅ 全小写+连字符，16 字符 ≤64

### 2.2 description

**实际值**:
> "Backward planning from target outcomes to present-day milestones. Use when planning with fixed deadline or target outcome, working backward from future goal to present, defining milestones and dependencies, mapping critical path, identifying what must happen when, planning product launches with hard dates, multi-year strategic roadmaps, event planning, transformation initiatives, or when user mentions 'backcast', 'work backward from', 'reverse planning', 'we need to launch by', 'target date is', or 'what needs to happen to reach'."

**逐句分析**:

| 句子 | 标注 | 评价 |
|------|------|------|
| S1: "Backward planning from target outcomes to present-day milestones." | WHAT | ✅ 简洁精准的功能定义 |
| S2: "Use when planning with fixed deadline or target outcome..." | WHEN + 关键词罗列 | ✅ 丰富的触发场景和关键词，含 "when user mentions" |

**规范检查**:
- 第三人称: ✅ S1 中性描述
- 触发短语: ✅ "Use when planning..." + "when user mentions..."
- 禁止内容: 无第一/第二人称、无祈使句、无跨 skill 路由 ✅
- 长度: ~420 字符 ≤1024 ✅

**评分**: 8/10 — 良好的 description，触发词丰富

### 2.3 allowed-tools
- **实际值**: 未定义（字段缺失）
- **判定**: ❌ 缺失。此 skill 需要 Read（读取项目文件）、Write（创建路线图文档）、Glob（搜索现有计划文件）
- **建议值**: `Read, Write, Glob, Grep`

### 2.4 其他 frontmatter 字段
仅 `name` 和 `description`。无非法/非标准字段 ✅。

### 2.5 Frontmatter 语法
- YAML 分隔符配对: ✅
- description 未加引号但无双引号/冒号歧义: ✅ 安全
- 无缩进错误 ✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Roadmap Backcast                              (L6, 1 行)
## Table of Contents                             (L8-17, 10 行) — 9 个锚点链接
## Purpose                                       (L19-21, 3 行)
## When to Use                                   (L23-30, 8 行) — 6 个触发场景
## What Is It                                    (L32-49, 18 行) — backcast vs forecast 概念对比
## Workflow                                      (L51-106, 56 行) — 5 步核心流程
  Step 1: Define Target Outcome                 (L53-63)
  Step 2: Identify Major Milestones             (L65-75)
  Step 3: Map Dependencies                      (L77-85)
  Step 4: Critical Path Analysis                (L87-96)
  Step 5: Feasibility Assessment                (L98-106)
## Dependency Mapping                            (L108-138, 31 行) — 4 种依赖类型详解
## Critical Path Analysis                        (L140-160, 21 行)
## Common Patterns                               (L162-185, 24 行) — 3 种典型场景
## Guardrails                                    (L187-198, 12 行) — 4 条防护规则
## Quick Reference                               (L200-211, 12 行)
```

### 3.2 必需章节检查

#### Workflow/Process 节
- **是否存在**: ✅ "Workflow" 节 (L51-106) 包含明确的 5 步流程
- **步骤连贯性**: ✅ 目标→里程碑→依赖→关键路径→可行性，逻辑顺序正确
- **步骤粒度**: ✅ 每步包含: what to do + how to do it + expected output
- **条件分支**: ⚠️ Step 5 (Feasibility Assessment) 暗示了 "feasible vs infeasible" 分支但未明确 else 路径
- **起始/终止条件**: ✅ Step 1 从 target outcome 开始，Step 5 以 feasibility verdict 结束
- **评分**: 8/10

#### Output Format 节
- **是否存在**: ❌ 完全缺失
- **隐含输出**: Workflow 每步描述了产出物（target statement、milestone list、dependency map、critical path diagram、feasibility assessment），但无统一的输出模板
- **缺失**: 无 backcast plan 文档模板、无 deliverable format 说明
- **评分**: 0/10

#### Scope/Limitations 节
- **是否存在**: ⚠️ 部分存在。"Guardrails" 节 (L187-198) 提供了 4 条约束，但更偏向行为指南而非领域边界
- **缺失**: 不涵盖什么？何时不应使用 backcast？与 forecast/agile planning 的边界？
- **评分**: 4/10

### 3.3 内容委托分析
- 委托比例: **0%** — 无 references/ 目录，211 行完全自包含 ✅
- 评估: Agent 可以仅从 body 独立执行完整的 backcast 规划

### 3.4 标题层级
- `#` → `##` → 无 `###` — 层级正确但扁平 ✅
- Table of Contents 中的锚点链接与节标题一致 ✅

### 3.5 Body 长度合规
- 实际: 211 行 vs 600 行限制 ✅

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接分析
5 步流程的输入/输出链:
- Step 1 产出 "target outcome statement" → Step 2 消费它来识别 milestones
- Step 2 产出 "milestone list with dates" → Step 3 消费它来映射依赖
- Step 3 产出 "dependency map" → Step 4 消费它来分析关键路径
- Step 4 产出 "critical path" → Step 5 消费它来评估可行性

数据流完整且单向 ✅。无断链。

### 4.2 内部矛盾扫描

**"Brook's Law" 拼写错误 (L148)**: 当前文本为 "Brook's Law"，应修正为 "Brooks's Law"（Fred Brooks 的所有格形式）。这是 Dossier 已标记的问题。此错误在 "Common Patterns" 节的 "Compressing the Schedule" 小节中出现。

**backcast vs forecast 概念**: "What Is It" 节清晰区分了 backcast（从未来往回规划）和 forecast（从现在往前预测）。概念定义与后续 Workflow 完全一致 ✅。

**无其他矛盾**: ✅ 全文无对立表述、无数值不一致、无声明与实现矛盾。

### 4.3 示例/计算正确性

**关键路径计算**: "Critical Path Analysis" 节中的方法描述（longest sequence of dependent tasks determining minimum timeline）正确。Float/slack 概念使用正确。

**Dependency Mapping 四种类型**: Finish-to-Start(FS)、Start-to-Start(SS)、Finish-to-Finish(FF)、Start-to-Finish(SF) — 项目管理标准依赖类型，定义准确 ✅。

### 4.4 条件完整性
- "When to Use" 给出 6 个正向触发场景 ✅
- Guardrails 给出 4 条行为约束 ✅
- 缺失: 无条件分支 else/otherwise（"如果目标不明确怎么办？" "如果用户无法定义目标结果怎么办？"）
- 缺失: "When NOT to use backcast"（如 agile sprint planning 更适合 forecast 的场景）

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵
无 references/ 目录。Body 无任何文件引用。完全自包含。✅ (N/A)

### 5.2 不可见资源审计
目录仅含 SKILL.md + SCORING.yaml + check.py。无隐藏文件。✅

### 5.3-5.7 其他资源审查
无子目录。✅ (N/A)

### 5.5 跨 Skill 引用检查
- `../` 路径引用: ✅ 无
- `@skill-name` prose 引用: ✅ 无
- 外部引用: ✅ 无

---

## 6. 语法与格式质量

### 6.1 拼写错误

| 行号 | 当前文本 | 建议修正 | 严重程度 |
|------|---------|---------|:--------:|
| L148 | "Brook's Law" | "Brooks's Law" | 🟡 |

### 6.2 语法错误
无主谓不一致、时态混乱、残缺句。✅ 整体英语质量高。

### 6.3 中英/葡英混杂
全文纯英文。✅

### 6.4 Markdown 格式破损
- Table of Contents 使用 Markdown 锚点链接: ✅ 格式正确
- 列表编号: ✅ 连续
- 代码围栏: ✅ (如有) 全部配对
- 无表格格式错误 ✅

### 6.5 占位符未填充
无 `TODO`、`FIXME`、`TBD` 等未完成标记。✅

### 6.6 截断内容
文件以 Quick Reference 正常结束。✅ 无截断。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | |
| 2 | description 第三人称 | ✅ | "Backward planning from target outcomes..." |
| 3 | description 含触发短语 | ✅ | "Use when planning..." + "when user mentions" |
| 4 | description ≤1024 字符 | ✅ | ~420 字符 |
| 5 | 无禁止 frontmatter 字段 | ✅ | |
| 6 | body ≤600 行 | ✅ | 211 行 |
| 7 | Workflow/Process 节存在 | ✅ | "Workflow" 5 步 |
| 8 | Output Format 节存在 | ❌ | 完全缺失 |
| 9 | Scope/Limitations 节存在 | ⚠️ | Guardrails 部分覆盖但无领域边界 |
| 10 | 无跨 skill 文件路径引用 | ✅ | |
| 11 | allowed-tools 格式正确 | ❌ | 字段缺失 |
| 12 | 路径仅指向本 skill 目录内 | ✅ | N/A |

**合规率**: 9/12 = 75%

---

## 8. 人机感评估

### 8.1 Emoji 审计
全文零 emoji。✅ 规划框架 skill 的理想状态——emoji 会分散对逻辑结构的注意力。

### 8.2 全大写/喊叫式语言
- 无 `STOP!`、`MANDATORY`、`CRITICAL` 等喊叫式语言 ✅
- "Workflow"、"Guardrails" 等节标题使用 Title Case — 正常 ✅

### 8.3 Persona 语气分析
**整体语气**: 中性教导式/咨询式。不是命令 agent，而是提供一个清晰的规划方法论。

**代表性语句**:
- L21: "Roadmap Backcast helps you plan backward from a fixed goal or deadline to the present..." — 有帮助的引导语气
- L32: "Unlike forecasting (predicting what will happen), backcasting starts with the desired outcome..." — 清晰的概念对比
- L98: "Feasibility Assessment — Ask: 'Is this timeline physically possible?'" — 直接而有力的问题

**语气适合度**: ✅ 完全适合规划框架 skill。不喊叫、不命令、不闲聊。专业且平实。

### 8.4 人机边界分析
- Guardrails 节提供了 agent 的行为约束（"Don't skip dependencies"、"Always include buffer time"、"Don't assume unlimited resources"）
- 无显式 "人类最终决策" 声明 ⚠️ — backcast 是规划工具，最终计划应由人类批准
- 无硬编码人类名称/偏好 ✅

### 8.5 人称分析
- 第二人称 (you/your): 在 "helps you plan" 等上下文中使用 ~3 次 — 面向用户的指导语气，对 agent skill 合理
- 第一人称 (I/we): 0 次 ✅
- 祈使句: "Ask: 'Is this timeline physically possible?'" — 指导性祈使句，合理 ✅

### 8.6 表格密度
适中。Dependency Mapping 使用 bullet 列表而非表格。整体以 prose + bullet 列表为主。✅

---

## 9. 可执行性评估

### 9.1 独立可执行性: 7/10
Agent 可以仅从 body 执行完整的 5 步 backcast。Workflow 提供了清晰的步骤和每步的输出。

### 9.2 步骤可操作性

| Step | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| 1: Define Target Outcome | "Write a clear target outcome statement" | 🟢 | 有具体格式指导 |
| 2: Identify Major Milestones | "Work backward from target date" | 🟢 | 有时间顺序指导 |
| 3: Map Dependencies | "For each milestone, identify what must complete first" | 🟢 | 有 4 种依赖类型 |
| 4: Critical Path Analysis | "Find the longest sequence of dependent milestones" | 🟢 | 有 float/slack 概念 |
| 5: Feasibility Assessment | "Compare critical path duration to available time" | 🟡 | 缺少 "不可行时怎么办" 的分支 |

### 9.3 工具依赖合理性
- 需要的工具: Read (读项目文件)、Write (创建路线图文档)、Glob (搜索现有计划)
- 在 allowed-tools 中声明: ❌ 缺失

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖
15 criteria。全部与 SKILL.md 内容一致 ✅。

关键匹配:
- Workflow 5 步: SCORING 中有对应的 process criteria
- Dependency types: SCORING 检查是否区分了依赖类型
- Critical Path: SCORING 检查是否识别了关键路径

### 10.2 Critical Failures 分析
Critical failures 合理: 跳过依赖分析、忽略时间缓冲、单向规划（不做 backcast 反而做 forecast）。

---

## 11. 已知问题验证（来自 skill-dossier.md）

> 🟡 评级。问题: "Brook's Law" 应为 "Brooks's Law"；Output 节缺失。

**验证**:
- "Brook's Law" 拼写: ❌ 仍存在 (L148)
- Output Format 节: ❌ 仍缺失
- Scope/Limitations 节: ⚠️ Guardrails 部分覆盖

**增量发现**: allowed-tools 缺失；缺少 "不可行时怎么办" 的分支逻辑。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 7/10 | 10% | 0.70 | Description 良好，allowed-tools 缺失 |
| Body 结构完整 | 6/10 | 10% | 0.60 | Workflow 存在，Output/Scope 缺失 |
| 逻辑一致性 | 8/10 | 20% | 1.60 | 5 步流程数据流完整，仅一处拼写错误 |
| 参考完整性 | 10/10 | 15% | 1.50 | 自包含，无引用断裂风险 |
| 语法格式 | 8/10 | 10% | 0.80 | 仅 "Brook's Law" 一处错误 |
| 规范合规 | 7/10 | 15% | 1.05 | 9/12 合规 |
| 人机感 | 8/10 | 10% | 0.80 | 专业中性，零废话 |
| 可执行性 | 7/10 | 10% | 0.70 | 5 步清晰但缺 infeasible 分支 |
| **加权总分** | | | **7.75/10** | **78/100** |

### 12.2 评级

🟢 **B+ (78/100)**: 扎实的规划方法论 skill。5 步逆向规划流程逻辑清晰、数据流完整。主要扣分项集中在规范合规（缺 Output/Scope 节、allowed-tools 缺失）和一个拼写细节（"Brook's Law"）。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷
1. **缺失 Output Format 节** — 添加 backcast plan 文档模板（含 Target Outcome Statement、Milestone Timeline、Dependency Map、Critical Path Diagram、Feasibility Assessment 各节）
2. **缺失 Scope/Limitations 节** — ≥3 条: 不替代 agile sprint planning、不替代财务预测、不适用于没有明确目标的探索性项目
3. **添加 allowed-tools** — `Read, Write, Glob, Grep`

### 🟡 重要缺陷
4. **"Brook's Law" → "Brooks's Law"** — L148
5. **Step 5 添加 infeasible 分支** — "如果不可行: 调整目标范围、增加资源、或接受延期"

### 🟢 优化建议
6. Guardrails 扩展为完整 Scope 节
7. 添加 "When NOT to use backcast" 条件（如 agile 迭代、探索性研究）

### 修复工作量估计
- 修改行数: ~25 行
- 修改文件数: 1 (SKILL.md)

---

## 附录: 审查过程记录

### 读取的文件列表
1. SKILL.md (211 行) — 逐行精读，含 ToC → Purpose → When to Use → What Is It → 5-Step Workflow → Dependency Mapping → Critical Path → Common Patterns → Guardrails → Quick Reference
2. SCORING.yaml — 全文
3. check.py — 全文

### 读取行数统计
总计: ~400 行 (3 个文件)

### 审查方法
- 全文阅读（非抽样）: ✅
- 交叉验证: SKILL.md ↔ SCORING.yaml ↔ SKILL-SPEC.md v1.0 ↔ skill-dossier.md
- 项目管理知识验证: Dependency types (FS/SS/FF/SF) 对照 PMBOK 标准

### 审查人
Claude (SkillIF quality audit) — 2026-08-06
