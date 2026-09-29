# REVIEW: 267-azure-bgp

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 类型**: process — Azure Virtual WAN 风格 hub-and-spoke 拓扑中的 BGP 振荡与路由泄漏分析
**Body 行数**: 235 行（SKILL.md）
**参考文件数**: 0（无 references/ 目录，body 自包含）
**已有 REVIEW**: 否（本文件为首次审查）
**审查范围**: 目录内全部 3 个文件（SKILL.md 235 行 + SCORING.yaml 151 行 + check.py 60 行，共 446 行）

---

## 1. 目录全量清单

```
267-azure-bgp/
├── SKILL.md (235 行)
├── SCORING.yaml (151 行)
└── check.py (60 行)
```

- 目录仅 3 个文件，无 `references/`、`scripts/`、`templates/` 子目录。
- 无 REVIEW.md 历史版本（本次为初始审查）。
- 无冗余文件、无 `.gitkeep` 占位、无嵌套目录。✅

**结构评价**: 该 skill 采用"全内联"模式——所有知识（检测规则、修复层级、禁用清单、陷阱清单）全部内联在 SKILL.md body 中，无外部参考文件。对 235 行的 process 型 skill 而言这是合理选择：内容规模不需要拆分，且避免了 001-skill-tuning 中发现的"参考文件不可见"类问题（category-mappings.json 事件）。代价是 body 相对密集（后文第 9 节评估其可执行性）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name

```
name: azure-bgp
```

- 匹配目录名 `267-azure-bgp` 的后缀部分：✅（SKILL-SPEC.md §1.1 要求 name 匹配目录名，`azure-bgp` 匹配 `267-azure-bgp` 的 slug）
- 全小写+连字符：✅
- ≤64 字符：✅（9 字符）
- 无大写、无空格、无下划线：✅

### 2.2 description（逐句拆解）

原文（SKILL.md L3，单行约 545 字符）：

```
Analyze and resolve BGP oscillation and BGP route leaks in Azure Virtual
WAN–style hub-and-spoke topologies (and similar cloud-managed BGP
environments). Detect preference cycles, identify valley-free violations,
and propose allowed policy-level mitigations while rejecting prohibited
fixes. Use when the user reports Azure Virtual WAN BGP route flapping or
unstable path selection, suspects route leaks or valley-free violations,
or asks which fix (routing intent, UDR, export policy) is valid in Azure.
```

逐句拆解：

| 句子 | 类型 | 判定 |
|------|------|:----:|
| "Analyze and resolve BGP oscillation and BGP route leaks in Azure Virtual WAN–style hub-and-spoke topologies (and similar cloud-managed BGP environments)." | WHAT | ✅ 明确描述核心功能与适用环境，且范围限定（Azure VWAN 风格 + 类似云托管 BGP 环境）|
| "Detect preference cycles, identify valley-free violations, and propose allowed policy-level mitigations while rejecting prohibited fixes." | WHAT（展开）| ✅ 具体化了三件核心动作（检测偏好环、识别谷底违规、提出受允许的策略级缓解）|
| "Use when the user reports Azure Virtual WAN BGP route flapping or unstable path selection, suspects route leaks or valley-free violations, or asks which fix (routing intent, UDR, export policy) is valid in Azure." | WHEN | ✅ 三个具体触发场景：路由抖动/路径不稳、怀疑泄漏、询问修复方案合法性 |

**判定汇总**:

- **WHAT**: ✅ 明确且具体，直接对应 body 的三大检测任务与三级修复体系
- **WHEN**: ✅ 使用规范触发短语 "Use when the user..."（SKILL-SPEC §2.4 允许的信号之一）
- **KEYWORDS**: ✅ 覆盖 BGP、Virtual WAN、route flapping、route leak、valley-free、routing intent、UDR、export policy 等全部关键域词
- **第三人称**: ✅ 全文无第一/第二人称，动词主语为隐含第三人称（"reports"、"suspects"、"asks" 主语均为 the user）
- **字符数**: 约 545 字符，≤1024。✅
- **触发短语**: "Use when the user..." 存在。✅

**问题 1（🟡 轻微）**: "while rejecting prohibited fixes" 将否定性边界嵌入了 description。按 SKILL-SPEC §2.5，否定性边界声明（what NOT to do）原则上应放在 body 的 Scope 节。此处与 200-legal-writing 的 "NEVER rewrites the draft" 类似但不完全相同——本句是作为 skill 的**正向功能**（"拒绝非法修复"本身就是本 skill 的输出要求，SCORING OUT-03 明确要求"同时推荐与拒绝"）来描述的，并非跨 skill 路由声明，因此可接受。但更干净的做法是改为 "evaluate proposed fixes against Azure policy constraints" 之类的正向表述。

**问题 2（✅ 无问题）**: "Azure Virtual WAN–style" 使用了 en-dash（–），为排版正确用法，无格式问题。

### 2.3 其他 frontmatter 字段

仅 `name`、`description` 两个字段。均属 SKILL-SPEC.md §1.1-1.2 允许范围，无禁止字段（无 `tools`、`metadata`、`tags` 等）。✅

未声明 `allowed-tools`：本 skill 为纯推理型（无文件操作、无 Bash、无外部工具），不声明 allowed-tools 完全合理。✅

### 2.4 Frontmatter 语法

YAML 分隔符 `---` 配对正确；description 中无未转义冒号（"routing intent, UDR, export policy" 使用逗号而非冒号，避开了 YAML 陷阱）；无缩进错误。✅

---

## 3. Body 逐段结构分析

### 3.1 段落清单

```
# Azure BGP Oscillation & Route Leak Analysis (L6)
## When to Use This Skill (L19-27)
## Core Invariants (Must Never Be Violated) (L29-38)
## Expected Inputs (L40-51)
## Reasoning Workflow (Executable Checklist) (L53-108)
  ### Step 1 — Sanity-Check Inputs (L55-61)
  ### Step 2 — Detect BGP Oscillation (Preference Cycle) (L63-91)
  ### Step 3 — Detect BGP Route Leak (Valley-Free Violation) (L93-108)
## Fix Selection Logic (Ranked) (L110-185)
  ### Tier 1 — Virtual WAN Routing Intent (Preferred) (L112-134)
  ### Tier 2 — Export / Route Policy (Protocol-Correct) (L136-157)
  ### Tier 3 — User Defined Routes (UDR) (L159-185)
## Prohibited Fixes (Must Be Rejected) (L187-211)
## Common Pitfalls (L213-220)
## Output Expectations (L222-229)
## References (L231-235)
```

共 11 个 `##` 节 + 6 个 `###` 子节。结构为"触发条件 → 硬性不变量 → 输入定义 → 检测工作流（3 步）→ 修复选择（3 层）→ 禁用修复 → 陷阱 → 输出期望 → 文献"。这是教科书式的 process skill 布局：**检测-修复分离、层级分明**，与 SCORING.yaml 的 PROCESS/OUTPUT 分类一一对应。

### 3.2 必需章节检查

| 章节 | 状态 | 位置与评价 |
|------|:----:|-----------|
| Workflow/Process | ✅ | `## Reasoning Workflow (Executable Checklist)`（L53-108）——Step 1-3 编号连续、每步含检测规则+判定标准+伪代码，是全语料中较扎实的工作流之一 |
| Output Format | ⚠️ | `## Output Expectations`（L222-229）——仅 4 条编号期望，共 8 行。无输出模板、无示例格式、未要求"逐项分类 possible_solutions.json"（见问题 4）|
| Scope/Limitations | 🟡 | 无显式 Limitations 节。`## When to Use This Skill`（L19-27）只给出**正向**触发场景；`## Core Invariants`（L29-38）与 `## Prohibited Fixes`（L187-211）约束的是"解决方案的合法性"，而非"skill 的适用边界"。SKILL-SPEC §3.1 要求回答"此 skill 不做什么、何时不该用"，此处缺失 |

**问题 3（🟡 重要）**: Scope/Limitations 节缺失/不足。应补充至少以下内容：
- 不处理 on-prem（本地）路由器配置（"The focus is cloud-correct reasoning, not on-prem router manipulation" L17 虽有提及，但属单句声明，未成节）
- 不处理非 BGP 层问题（物理链路、光模块、QoS）
- 不处理非 Azure 环境的传统 BGP 调优（timer、dampening 等属陷阱而非本 skill 主题，已在 Common Pitfalls 反向覆盖）
- 不保证修复在 Azure 门户/CLI 中的实际落地验证

### 3.3 必需章节检查（Workflow 细节）

#### Workflow/Process 节（L53-108）
- 标题明确：✅ "Executable Checklist" 一词明确定位
- 步骤连贯：✅ Step 1（输入校验）→ Step 2（振荡）→ Step 3（泄漏），顺序合理——先校验输入再分析，符合 SCORING PROC-01→02→03 的顺序
- 每步含输入/输出：⚠️ 每步有检测规则与结论判定，但 Step 1 的"输入无效时怎么办"未定义（见问题 6）；Step 2 伪代码的起点选取未说明（见问题 7）
- 条件分支：🟡 Step 2 与 Step 3 之间、检测与修复之间无显式分支（如"仅振荡→Tier 1/2 组合"、"仅泄漏→Tier 2 侧重导出过滤"），依赖 agent 自行组合。可接受但可更显式
- 起始/终止条件：✅ Step 1 为起点，Output Expectations 隐含终止

#### Output Format 节（L222-229）
- 存在：✅
- 输出模板：❌ 无任何模板或示例
- 与 workflow 对应：⚠️ 第 1-2 条对应检测结果（问题类型+成因），第 3-4 条对应修复建议与禁用修复拒绝——与 SCORING OUT-01/02/03 对应良好，但见问题 4
- 可验证性：⚠️ "Recommend allowed policy-level fixes" 未要求**逐项**评判 `possible_solutions.json` 中的每个候选方案（SCORING OUT-02 的硬性要求，见问题 4）

### 3.4 内容委托分析

- 无 references/ 目录，body 未委托任何内部文件。✅
- `## References`（L231-235）仅列出 2 条外部文献：RFC 4271 与 Gao-Rexford 模型。二者均为 BGP 领域公认权威来源，引用恰当且克制（未堆砌无关文献）。✅
- 委托比例：0%。body 完全自包含——这是本 skill 相比 001-skill-tuning（委托比例 ~24%）的重大优点。

### 3.5 节编号/标题层级

- 标题层级：`#` → `##` → `###`，无跳级。✅
- 编号序列：Step 1-3 连续无跳跃；Tier 1-3 连续无跳跃。✅
- 重复标题：无。✅

### 3.6 Body 长度合规

235 行，远低于 600 行硬上限。✅（process 模式建议 ~200 行，235 行略超但属正常波动）

---

## 4. 逻辑一致性深度审查

### 4.1 检测-修复链条衔接

**链条完整**: Step 2（振荡检测：偏好环）→ Tier 1 振荡修复（routing intent 打破偏好环）+ Tier 2 振荡修复（过滤 peer-learned 路由打断环的一条边）；Step 3（泄漏检测：谷底违规）→ Tier 1 泄漏修复（intent 强制谷底转发）+ Tier 2 泄漏修复（谷底导出规则）+ Tier 3（UDR 覆盖泄漏路由的下一跳）。四条映射均成立，无"检测了却无对应修复"或"修复了却无对应检测"的悬空。✅

### 4.2 内部矛盾/张力扫描

**张力 A — "possible" 与 "conclude" 的强度不一致（L72-74）**:
- L72: "If the graph contains a cycle, oscillation is **possible**"
- L74: "A 2-node cycle is **sufficient to conclude** oscillation"
- 同一检测规则内，"可能"与"足以断定"两种措辞并存。这是为评测服务的刻意简化（SCORING PROC-02 同样要求 2-node cycle → 判定振荡），逻辑上自洽，但从 BGP 收敛理论看，振荡还取决于决策规则（如 MED 比较、多链路）与路由重播次序。建议统一措辞为"sufficient to conclude oscillation **for the purposes of this analysis**"，明确简化假设。

**张力 B — Tier 2 泄漏修复混淆"出口侧"与"接收侧"（L149-157 vs L216）**:
- Step 3 定义的泄漏条件（L105-108）是**出口违规**：本网络把 provider/peer-learned 路由导出给 peer/provider
- Tier 2 的泄漏修复菜单却同时列出：谷底导出规则（L151，出口侧 ✅）、no-export communities（L152，出口侧 ✅）、**ingress filtering**（L153，接收侧 ❌ 错位）、**RPKI 起源验证**（L154，接收侧 ❌ 错位）
- ingress filtering 与 RPKI 解决的是**接收侧**问题（防止外部泄漏路由进入本网络），不能阻止本网络将 peer-learned 路由再导出给 peer——这正是 Common Pitfalls L216 自己承认的："Ingress filtering alone doesn't stop export of other leaked routes"
- **结论**: Tier 2 的泄漏修复菜单与 Common Pitfalls 存在自我矛盾——同一文件内既把 ingress/RPKI 列为"泄漏修复"，又声明它们不足以阻止泄漏。修复方向：将 Tier 2 泄漏修复拆为"出口侧（谷底导出规则、no-export）"与"接收侧防护（ingress filtering、RPKI，作为纵深防御而非直接修复）"两组，消除错位。

**张力 C — "Virtual WAN (ASN 65001)" 的领域事实存疑（L130）**:
- L130: "When intent mandates hub-to-hub traffic goes through Virtual WAN (ASN 65001), leaked routes cannot be used"
- Azure Virtual WAN hub 的 BGP ASN **默认为 65515**（与虚拟网络网关、VPN 网关、ExpressRoute 网关一致），65001 并非 Azure 的默认 hub ASN（它是常见示例性私有 ASN，多出现于 Cisco/社区文档）
- 若评测数据刻意采用 65001 作为 hub ASN，则本 skill 与评测数据内部自洽、无碍打分；但作为**通用领域知识**嵌入推理示例，存在事实性错误风险，可能诱导 agent 在非评测场景输出错误信息
- 修复方向：改为 "Virtual WAN (ASN 65515)"，或中性表述 "the hub's ASN" 并在示例中注明"以实际配置为准"

**张力 D — 不变量与禁用表的范围口径不统一（L33 vs L193）**:
- Core Invariants L33: "BGP sessions **between hubs** cannot be administratively disabled"
- Prohibited Fixes L193: "Disable BGP — **Not customer-controllable**"（未限定 hub 间）
- 后者把"hub 间 BGP 不可禁用"泛化为"所有 BGP 不可禁用"。对 Azure 场景（ExpressRoute/VPN 网关的 BGP 会话均为 Azure 托管）大体成立，但 on-prem 侧会话并非如此。作为 Azure 场景的简化立场可接受，但建议统一口径："在 Azure 托管侧不可禁用"。

**张力 E — 泄漏条件的正反覆盖不对称（L105-108）**:
- 泄漏条件只列出"**是**泄漏"的两条（provider→peer/provider、peer→peer/provider），未显式声明"customer-learned → anyone **不是**泄漏"
- 表格（L97-101）隐含了这一点（Customer 行 = Anyone），但 SCORING PROC-03 明确要求"without misclassifying customer-exported routes"——若 agent 仅读到条件清单而未消化表格，存在误报风险。建议在 Leak Conditions 后加一句正向声明："Routes learned from a customer may be exported to anyone; this is never a leak."

### 4.3 示例/伪代码正确性

**Step 2 伪代码（L77-90）——算法正确，两点边界缺失**:

```python
pref = {asn: prefer_via_asn, ...}

def find_cycle(start):
    path = []
    seen = {}
    cur = start
    while cur in pref:
        if cur in seen:
            return path[seen[cur]:]  # cycle found
        seen[cur] = len(path)
        path.append(cur)
        cur = pref[cur]
    return None
```

- 核心逻辑（路径游走 + 访问标记，找到重复节点即切出环）正确，标准且可读。✅
- **边界 1（🟡）**: 未处理 `pref[asn] == asn` 的自环。若某 ASN 的偏好下一跳是自身（数据异常，Step 1 未定义此校验），`find_cycle` 会返回单元素环 `[asn]`，被解读为振荡。单节点自环不是 BGP 振荡环，应作为输入非法处理（在 Step 1 拒绝）或在伪代码中排除。
- **边界 2（🟡）**: 只从单个 `start` 出发，且未说明 `start` 如何选取。正确用法是对每个 ASN 都运行一次（或对偏好图每个入度为 0 的节点运行），文本未交代，agent 可能只跑一个起点而漏检环。建议在伪代码后加一句："Run find_cycle from every ASN in preferences.json."
- 环的返回形式 `path[seen[cur]:]` 正确切出闭环。✅

**Tier 2 振荡修复推理（L140-147）——玩具模型成立，一般性说明不足**:
- "过滤 peer-learned 路由打断一环 → 环崩塌"：对 2 节点环成立（删一条边即无环），对更长环（A→B→C→A）删任意一条边同样成立。逻辑正确。✅
- 但示例（L147）假设了"被争议前缀仅经由 peer 学到"的特定模型；对"前缀经第三方（客户/提供商）学到、偏好环仅体现在选路偏好上"的情形，过滤 peer-learned 路由未必打断环。文本未声明该假设边界。建议加一句适用范围说明。

### 4.4 条件完整性

- 谷底规则表（L97-101）覆盖 Customer/Peer/Provider 三行，无遗漏。✅
- 泄漏条件两条覆盖 provider→{peer,provider} 与 peer→{peer,provider} 全部组合。✅
- 修复层级 Tier 1-3 各有适用对象表（振荡/泄漏），无空档。✅
- Tier 2 振荡修复的"why it works"链式论证（L141-143）完整（过滤→对方不再收到→不再偏好→环崩塌）。✅
- Prohibited Fixes 表 4 行均有理由列。✅
- Common Pitfalls 4 条均以 "— False." 结尾 + 总括 "All are false."（L220）。✅

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

SKILL.md 内无任何相对路径文件引用（无 `references/`、`scripts/` 引用），不存在悬空引用问题。目录内全部 3 个文件均被本审查读取并核实：

| 文件 | 角色 | 一致性 |
|------|------|:------:|
| SKILL.md (235 行) | 技能本体 | ✅ |
| SCORING.yaml (151 行) | 评测标准（16 criteria + 3 CF）| ✅ 与 body 高度对齐（详见第 10 节）|
| check.py (60 行) | 评测脚本 | ✅ 语法正确、导入成功，但为空实现（详见 5.4）|

### 5.2 外部引用审查

| 引用 | 位置 | 评价 |
|------|------|------|
| RFC 4271 — Border Gateway Protocol 4 | L233 | ✅ BGP 本体标准，恰当 |
| Gao–Rexford model — Valley-free routing economics | L234 | ✅ 谷底规则的理论基础，与本 skill 的 Valley-Free Rule 直接对应 |

两条引用均为领域公认权威，无拼写错误（"Gao–Rexford" en-dash 正确），未堆砌无关文献。✅

### 5.3 Expected Inputs 审计（L40-51）

6 个 JSON 输入文件（topology.json、relationships.json、preferences.json、route.json、route_leaks.json、possible_solutions.json）为**任务注入输入**而非 skill 资源——评测时由 runner 提供到 workspace，设计合理。

**问题 5（🟢 优化）**: 目录内无输入文件的示例/schema。agent 无法预演数据结构（如 relationships.json 的边方向表示法、preferences.json 的键名）。虽依赖评测注入可接受，但若在 SKILL.md 的 Expected Inputs 表中补充各文件的关键字段示例，将显著降低 agent 的解析变异性。

### 5.4 check.py 审查（60 行）

- 导入 `_shared/checker` 成功（已验证 `_shared/checker.py` 存在，`set_tool_log_path`/`set_agent_output` 均可用）。✅
- `check()` 函数体全部为注释（"SCOPE-01, SCOPE-02: llm judge (not checked here)"），**返回空 dict `{}`**——0 项脚本检查。与 SCORING.yaml 全部 16 项 `judge: llm` 的声明一致，属"全 LLM 评测"skill 的标准脚手架，但无任何功能价值。
- **冗余逻辑**: `main()` 先以**路径字符串**调用 `check()`（其中 `set_agent_output(agent_output)` 会把路径误设为输出内容），随后再读文件、用真实内容覆盖设置。最终状态正确（后写覆盖前写），但这是无意的双重设置，若未来在 `check()` 与 `main()` 之间插入读取逻辑会产生错误结果。
- **结果形态风险**: 对全 LLM skill 输出 `{}` 空 dict——runner 需要正确解释"空结果 = 全部交由 judge"；若 runner 将空 dict 误读为"无 criteria 可评"或"全部失败"，将系统性影响该 skill 的评分。建议确认 runner 对空 dict 的处理约定。

**问题 6（🟡 重要）**: 本 skill 的 3 个 critical_failures（CF-01/02/03）全部依赖 LLM judge 主观判定，check.py 未提供任何脚本级辅助验证。例如 NEG-01（不提出禁用 BGP/关闭 peering）完全可以用脚本粗筛 agent_output 中是否出现 "disable BGP"/"shutdown" 等建议性语句作为辅助信号。全 LLM 评测在高风险 CF 上缺少可复现的机器锚点，建议为至少 1 个 criteria 增加 script 检查（详见第 10 节与第 13 节）。

### 5.5 跨 Skill 引用检查

- `../` 路径引用：无。✅
- `@other-skill-name` 引用：无。✅
- 外部 URL 引用：无。✅
- 硬编码外部 CLI 依赖：无（本 skill 无任何命令行/工具依赖，纯推理）。✅

### 5.6 嵌套重复/死文件检查

- Self-nested 目录：无。✅
- 冗余/废弃文件：无。✅
- 隐藏文件：无。✅

---

## 6. 语法与格式质量（逐问题列举）

**总评**: skill-dossier.md 记录"267 多处语法瑕疵"，本审查确认属实。瑕疵集中在 L33-35（Core Invariants 节）与 L194（Prohibited Fixes 表），均为可快速修复的英文语法问题。Markdown 结构本身无破损。

### 6.1 拼写错误

| 行号 | 文件 | 当前文本 | 建议修正 | 严重程度 |
|:----:|------|---------|---------|:--------:|
| — | — | 未发现拼写错误（Virtual WAN、hub-and-spoke、valley-free、oscillation 均拼写正确）| — | — |

### 6.2 语法错误

| 行号 | 文件 | 当前文本 | 问题 | 建议修正 |
|:----:|------|---------|------|---------|
| L33 | SKILL.md | "as it's **owned by azure**" | ① "azure" 首字母小写（专有名词应大写为 Azure）；② 正式规范文中使用口语缩写 "it's" | "as it is owned by Azure" |
| L34 | SKILL.md | "as it **break** all other traffic running on the connections" | ① 主谓不一致——主语 it（第三人称单数）应配 breaks；② "traffic running" 后接 "on the connections" 尚可，但与 L35 语义重复 | "as it breaks all other traffic running on the connections" |
| L35 | SKILL.md | "as it **break** all other traffic running" | ① 主谓不一致（同 L34）；② 句末 "running" 悬垂——"running" 什么？无宾语 | "as it breaks all other traffic running over the same connections" 或直接与 L34 合并（见问题 7）|
| L130 | SKILL.md | "When intent mandates hub-to-hub traffic **goes** through Virtual WAN" | 缺引导词 "that"——"mandates that traffic goes" | "When intent mandates **that** hub-to-hub traffic goes through..." |
| L194 | SKILL.md | "**prohibited operation** and cannot solve the issue" | 无主语句子碎片（表内理由列）——"Disable peering" 是主语，此处两个谓词并列缺主语 | "A prohibited operation; cannot solve the issue" 或 "Prohibited in Azure; does not solve the issue" |

### 6.3 中英/葡英混杂

无。全部文件为英文。✅（对照 262-content-humanizer 的葡语混入问题，本 skill 无此问题）

### 6.4 Markdown 格式破损

- 表格（L44-51、L97-101、L191-196）：分隔线、列对齐正确。✅
- 代码块（L77-90）：```python 开闭配对正确。✅
- 粗体/列表嵌套：正确。✅
- 无破损。✅

### 6.5 占位符未填充

无 `[TODO]`、`[X]`、`<placeholder>` 类残留。✅

### 6.6 截断内容

- L235 以 References 最后一行结束，无截断。✅
- SCORING.yaml L151 以 CF-03 描述结束，无截断。✅
- check.py L59 以 `main()` 调用结束，无截断。✅

### 6.7 冗余重复

**问题 7（🟡 轻微）**: Core Invariants L34 与 L35 语义几乎完全重复——"Peering connections cannot be shut down as it break all other traffic running on the connections" 与 "Removing connectivity is not a valid solution as it break all other traffic running" 表达的是同一件事（破坏既有流量）。两条可合并为一条："Peering connections cannot be shut down and connectivity cannot be removed — doing so breaks all other traffic on the connection." 同时消除一处语法错误的重复来源。

---

## 7. 规范合规性（逐条对照 SKILL-SPEC.md v1.0）

| # | 规则 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | name 匹配目录名 | ✅ | `azure-bgp` ↔ `267-azure-bgp` |
| 2 | description 第三人称 | ✅ | 全第三人称，无 you/I/we |
| 3 | description 含 WHAT + WHEN + KEYWORDS | ✅ | 三要素齐备（见 2.2）|
| 4 | description ≤1024 字符 | ✅ | 约 545 字符 |
| 5 | description 含触发短语 | ✅ | "Use when the user reports..." |
| 6 | 无禁止 frontmatter 字段 | ✅ | 仅 name/description |
| 7 | body ≤600 行 | ✅ | 235 行 |
| 8 | Workflow/Process 节存在 | ✅ | L53-108 Reasoning Workflow |
| 9 | Output Format 节存在 | ⚠️ | L222-229 存在但仅 8 行、无模板（问题 4）|
| 10 | Scope/Limitations 节存在 | 🟡 | 无显式节，仅正向 When-to-Use + 约束性边界（问题 3）|
| 11 | 无跨 skill 文件路径引用 | ✅ | 无 `../` 引用 |
| 12 | 目录名 NNN-kebab-case | ✅ | `267-azure-bgp`，无空格无大写 |

### 7.1 违规详情

**违规 1（🟡 部分合规）— Scope/Limitations 节不足**: SKILL-SPEC §3.1 要求 body 必须回答"此 skill 不做什么、何时不该用"。本 skill 的 `## When to Use This Skill` 只覆盖"何时该用"，`## Core Invariants` 与 `## Prohibited Fixes` 约束的是**解决方案的合法性**而非 **skill 的适用边界**。严格判定为部分缺失。这是本 skill 最大的规范合规缺陷。

**违规 2（🟢 可接受边缘）— description 含否定边界**: "while rejecting prohibited fixes" 属 §2.5 建议避免的否定性表述混入（详见问题 1）。不构成违规，但建议调整。

### 7.2 合规亮点

- description 是本批次（251-275）中最规范的之一：WHAT/WHEN 分离清晰、触发场景具体到"route flapping / unstable path selection / suspects route leaks / asks which fix is valid"，与评测意图（SCORING SCOPE-01）高度一致
- 无任何跨 skill 路由、无内部实现细节泄露、无工具依赖声明残留

---

## 8. 人机感评估

### 8.1 Emoji 审计

| 位置 | Emoji | 用途 | 判定 |
|------|:-----:|------|:----:|
| L33-36（Core Invariants）| ❌ | 标注"禁止"的不变量 | ✅ 功能性 |
| L36（Core Invariants）| ✅ | 标注"必须"的规则 | ✅ 功能性 |
| L114-115、L161-162（Tier 适用表）| ✔ | 标注适用对象（振荡/泄漏）| ✅ 功能性 |
| L215-218（Common Pitfalls）| ❌ | 标注错误命题 | ✅ 功能性 |

全部 emoji 均为功能性语义标记（允许/禁止/适用），无装饰性 emoji、无颜文字。✅（与 001-skill-tuning 的判定标准一致：功能性 emoji 可接受）

### 8.2 全大写/喊叫式语言

- "Must Never Be Violated"（L29）、"Must Be Rejected"（L187）：结构性强调标题，合理不刺耳 ✅
- "**Any solution violating these rules is invalid.**"（L38）：加粗强调，规范 ✅
- "All are false."（L220）：简短直接——见 8.3
- 无过度喊叫。✅

### 8.3 Persona 语气分析

整体语气：**中性技术文档风**。以规则、表格、条件句为主，无营销腔、无夸张承诺。

代表性例句：
- "The focus is cloud-correct reasoning, not on-prem router manipulation."（L17）——一句话划定立场，清晰有力
- "**Correct approach**: Fix BGP issues through **policy changes** (route filters, preferences, export controls, communities) rather than disabling connectivity."（L211）——正面引导，指令明确
- "All are false."（L220）——过于简短，略显突兀；建议 "None of these are valid fixes; all are false." 以保持句子完整性

### 8.4 人机边界分析

- 本 skill 为**纯分析型**任务（读输入 JSON → 判定 → 输出解决方案），无文件写入、无外部操作、无人工检查点
- 无"询问用户澄清"步骤——对评测场景（一次性输入 6 个 JSON）合理；对真实使用场景，若输入不完整（Step 1 校验失败），agent 无退路（见问题 8）
- 决策权边界：skill 将所有"是否合法"的判定权交给规则（Tier 体系 + 禁用清单），agent 无自由裁量空间——符合评测的可判定性需求
- 硬编码人类名称：无

### 8.5 人称分析

- 第二人称（you/your）：无。✅
- 第一人称（I/we）：无。✅
- 用户称呼：description 用 "the user"（第三人称）✅；body 用 "an agent"（L10）——规范

---

## 9. 可执行性评估

### 9.1 独立可执行性

假设 agent 只拿到 SKILL.md（无目录探索能力）：
- 它知道 3 个检测步骤 + 各自判定规则 ✅
- 它知道 3 个修复层级 + 排序逻辑 ✅
- 它知道 4 类禁用修复 + 拒绝理由 ✅
- 它知道 4 类常见陷阱（避免误答）✅
- 它知道 4 条输出期望 ✅

**可执行性评分**: 8/10——body 完全自包含、无外部参考依赖，是 322 个 skill 中可独立执行性最好的一类。扣分项：Step 1 无效输入无处理路径、Step 2 伪代码起点未定义、修复层级选择缺少"routing intent 可用性如何判定"的说明、输出无模板。

### 9.2 步骤可操作性

| Step | 描述 | 可操作性 | 问题 |
|------|------|:--------:|------|
| Step 1 | 输入校验（ASN 存在性 + 关系对称性）| 🟡 | 校验规则明确（L57-61），但校验失败后的行为未定义——报告并继续？中止？降级？（问题 8）|
| Step 2 | 振荡检测（偏好图 + 环检测）| 🟡 | 伪代码正确，但未说明对所有 ASN 起点迭代、未排除自环（问题 7/边界 1-2）|
| Step 3 | 泄漏检测（谷底规则）| 🟢 | 表格 + 两条条件，直接可执行，无歧义 |
| 修复选择 | Tier 1 → 2 → 3 | 🟡 | 层级排序明确，但 "If routing intent is available"（L134）——可用性从何判定？预期是从 possible_solutions.json 读取，文本未指明 |
| 输出 | Output Expectations | 🟡 | 4 条期望无模板；未要求逐项分类 possible_solutions.json（问题 4）|

### 9.3 工具依赖合理性

- 需要的工具：无（纯推理，仅 Read 输入文件）。✅
- 外部 CLI 依赖：无。✅
- 运行时风险：零——这是本 skill 相对 001-skill-tuning（Gemini CLI 硬依赖）、259/260（截断模板）等 skill 的显著优势。

### 9.4 评测可判定性

- SCORING 16 项 criteria 均可由 LLM judge 依据 SKILL.md 的明确规则判定（规则足够具体，judge 无需猜测"正确解"）✅
- CF-01/02/03 的触发条件在 SKILL.md 中有直接对应文本（Core Invariants / Step 2 / Step 3 / Prohibited Fixes）✅
- 唯一风险：全 LLM judge 无脚本锚点（见问题 6）

---

## 10. SCORING.yaml 交叉参考

### 10.1 文件结构核对

| 字段 | 值 | 核对 |
|------|-----|:----:|
| skill | azure-bgp | ✅ 与 frontmatter name 一致 |
| pattern | process | ✅ 与 body 类型一致 |
| total_items | 16 | ✅ 实际 criteria 数：SCOPE 2 + PROC 7 + OUT 3 + NEG 3 + QA 1 = 16 |
| criteria 全部 judge: llm | 16/16 | ✅ 与 check.py 空实现一致（0 script）|
| critical_failures | 3（全部 cap_to_0）| ✅ |

### 10.2 Criteria ↔ SKILL.md 映射表（16 项全查）

| # | Criterion | SKILL.md 对应 | 对齐度 |
|---|-----------|--------------|:------:|
| 1 | SCOPE-01 识别为 Azure VWAN BGP 振荡/泄漏任务 | When to Use（L19-27）+ description | ✅ 强对齐 |
| 2 | SCOPE-02 云正确推理（策略级修复）| Core Invariants（L29-38）+ L17 | ✅ 强对齐 |
| 3 | PROC-01 输入校验（ASN 存在性、关系对称）| Step 1（L55-61）| ✅ 逐条对应 |
| 4 | PROC-02 偏好图 + 环检测 + 2-node 判定 | Step 2（L63-91）| ✅ 逐条对应 |
| 5 | PROC-03 谷底规则 + 不误报 customer-export | Step 3（L93-108）| ⚠️ SKILL.md 未显式声明 customer-export 合法（问题 4.2 张力 E）|
| 6 | PROC-04 Tier 1 routing intent 优先 | Tier 1（L112-134）| ✅ |
| 7 | PROC-05 Tier 2 政策修复（过滤/community/ingress/RPKI）+ 机制解释 | Tier 2（L136-157）| ✅ |
| 8 | PROC-06 Tier 3 UDR 仅当 intent 不可用/需立即遏制 + trade-off | Tier 3（L159-185）| ✅ 含 trade-off 陈述（L185）|
| 9 | PROC-07 禁用修复 + Azure 理由 | Prohibited Fixes（L187-211）| ✅ |
| 10 | OUT-01 问题类型 + 成因 | Output Expectations 1-2（L224-225）| ✅ |
| 11 | OUT-02 逐项分类 possible_solutions.json | Output Expectations 3-4 | ⚠️ **缺口**：SKILL.md 未显式要求"逐项分类候选修复为 valid/invalid"（问题 4）。Expected Inputs 虽列出该文件，但无对应处理指令——agent 可能只推荐修复而不逐项评判 |
| 12 | OUT-03 推荐 + 拒绝缺一不可 | Output Expectations 3-4（L226-227）| ✅ |
| 13 | NEG-01 不提出禁用 BGP/关 peering/删连接 | Core Invariants + Prohibited Fixes | ✅ 双重覆盖 |
| 14 | NEG-02 不声称 timer/dampening 可修复振荡 | Common Pitfalls 1（L215）| ✅ |
| 15 | NEG-03 不声称少收前缀可防泄漏 | Common Pitfalls 2（L216）| ✅ |
| 16 | QA-01 结论点名 tier + 具体 ASN/偏好边 | Tier 2 示例（L147）+ Output Expectations | ⚠️ **缺口**：SKILL.md 的示例（vhubvnet1 ASN 65002 / vhubvnet2 ASN 65003）示范了"点名 ASN"，但 Output Expectations 未要求结论必须点名具体 ASN/边——agent 可能给出泛化结论而丢 QA-01 分 |

**结论**: 14/16 项强对齐，2 项存在显式性缺口（OUT-02、QA-01）——缺口不在评测标准，而在 SKILL.md 未将评测要求写进输出指令。修复成本极低（见第 13 节第 4 项）。

### 10.3 Critical Failures 分析

| CF | 条件 | 合理性 | 补充 |
|----|------|:----:|------|
| CF-01 | 建议禁用 BGP/关 peering/删连接 | ✅ 合理——与 Core Invariants 完全对应 | 建议加脚本辅助（问题 6）|
| CF-02 | 误诊：漏检偏好环或谷底规则用错（如 customer-export 算泄漏）| ✅ 合理 | 覆盖过宽——"valley-free rule 应用错误"的任何形态都直接 cap_to_0，未区分轻微误用与根本性误诊；可考虑按严重度分级（如仅计算错误扣分 vs 完全漏检 cap_to_0）|
| CF-03 | 按 on-prem 路由器思路操作（拓扑破坏式修复）| ✅ 合理——与 SCOPE-02 呼应 | — |

**建议新增 CF（🟢 可选）**: Agent 在 routing intent 可用时仍推荐 UDR 为第一选择（层级倒置）——已有 PROC-06 以 process 项覆盖，是否升级为 critical 取决于评测者对层级倒置严重性的判断。

### 10.4 测评可行性

- 16 项 criteria 全部可由 judge 依据 SKILL.md 明确规则判定，无"猜标准答案"问题。✅
- 3 项 CF 的判定边界清晰（是否出现禁用类建议、是否误用规则、是否 on-prem 思路）。✅
- 无脚本检查的可靠性风险：见问题 6。全 LLM 评测的 judge 间一致性（inter-rater reliability）是本 skill 评分最大的系统性风险。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

skill-dossier.md 对 267-azure-bgp 的记录：

> **逻辑**: "267 技术推理严密"（Batch 251-275 摘要）
> **语法**: "267 多处语法瑕疵"（Batch 251-275 摘要）

**本审查验证**:

- ✅ **"技术推理严密"确认**: Tier 1-3 修复体系（intent 优先 → 导出策略 → UDR 兜底）逻辑链条完整、谷底规则表与泄漏条件自洽、检测-修复映射无悬空、Common Pitfalls 与 NEG criteria 一一对应。这是本 skill 的最大优点。
- ✅ **"多处语法瑕疵"确认**: L33（"azure" 小写 + "it's" 口语化）、L34-35（"as it break" 主谓不一致 ×2 + 语义重复）、L130（缺 "that"）、L194（句子碎片）——共 5 处，集中在 2 个区域，修复成本极低（见第 13 节第 3 项）。

**dossier 未记录、本审查新增发现的问题**:

1. **ASN 65001 领域事实存疑**（L130）——Azure VWAN hub 默认 ASN 为 65515
2. **Scope/Limitations 节不足**（问题 3）
3. **Tier 2 泄漏修复出口/接收侧错位**（问题 4.2 张力 B）
4. **OUT-02 / QA-01 显式性缺口**——SCORING 要求与 Output Expectations 不完全对应（问题 4）
5. **check.py 空实现**——全 LLM 评测无脚本锚点（问题 6）
6. **Step 2 伪代码边界缺失**——自环未排除、起点未定义（问题 4.3）

dossier 中该 skill 未被列入"🟠 需修复"名单（259/260/268/269/271 在列），与本审查"无致命缺陷"的结论一致。

---

## 12. 综合评分

### 12.1 维度评分表

| 维度 | 分数 | 权重 | 加权 | 说明 |
|------|:----:|:----:|:----:|------|
| Frontmatter 合规 | 9/10 | 10% | 0.90 | description 为全语料优秀水平；唯一小瑕是 "while rejecting prohibited fixes" 否定边界混入 |
| Body 结构完整 | 6/10 | 15% | 0.90 | 工作流扎实（3 步 + 3 层 + 禁用 + 陷阱），但 Output 仅 8 行无模板、Scope/Limitations 无显式节 |
| 逻辑一致性 | 7/10 | 20% | 1.40 | 检测-修复链条完整、谷底规则自洽；扣分：ASN 65001 存疑、Tier 2 出口/接收侧错位、自环边界缺失 |
| 语法格式 | 6/10 | 10% | 0.60 | 5 处语法错误（dossier 已标记），Markdown 结构完好 |
| 规范合规 | 7/10 | 15% | 1.05 | 12 项清单 10 项通过；Scope 部分缺失、Output 偏弱 |
| 人机感 | 8/10 | 10% | 0.80 | 中性专业、功能 emoji、无人称问题；"All are false." 略突兀 |
| 可执行性 | 8/10 | 10% | 0.80 | 自包含无依赖、规则可直接执行；输入无效处理与输出模板缺失 |
| SCORING 配套 | 8/10 | 10% | 0.80 | 16 项 criteria 与 body 强对齐、total_items 精确；2 项显式性缺口、check.py 空实现 |
| **加权总分** | | | **7.25** | **73/100** |

### 12.2 评级

🟢 **B (73/100)** — 良好。技术推理严密、评测配套一致、可独立执行性强，是本批次（251-275）中综合质量靠前的 skill。主要扣分集中在语法瑕疵与边界声明不足，均为低成本可修复项。修复第 13 节 🟡 各项后可达 A-（85+）。

> 对比参考：001-skill-tuning（C+ 56/100，Scope 完全缺失 + 硬依赖）；本 skill 无致命缺陷、无工具依赖、无死文件，结构性优点显著。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷（必须修复）

**无。** 本 skill 未发现 cap 级缺陷（无内部矛盾、无缺失引用、无运行时依赖、无评测结构性风险）。以下按重要度排序。

### 🟡 重要缺陷（建议修复）

1. **核实并修正 "Virtual WAN (ASN 65001)"**（SKILL.md L130）
   - 当前: "When intent mandates hub-to-hub traffic goes through Virtual WAN (ASN 65001)..."
   - 修复方向: Azure Virtual WAN hub 的 BGP ASN 默认为 65515。改为 "Virtual WAN (ASN 65515)"，或中性表述 "the hub's BGP ASN" 并注明以实际配置为准；若评测数据刻意采用 65001，则至少加注"示例 ASN"
   - 不修复后果: 作为通用 skill 传播错误领域事实；评测数据若使用 65515 而 skill 示例用 65001，agent 可能产生困惑

2. **补充 Scope/Limitations 节**（SKILL.md）
   - 位置: Output Expectations 之前（L229 与 L231 之间）
   - 修复方向: 新增 `## Scope / Limitations` 节，至少包含：① 不处理 on-prem 路由器配置（L17 已有单句，成节强化）；② 不处理物理链路/非 BGP 层问题（光模块、线缆、QoS）；③ 不适用于非 Azure 云托管的传统 BGP 环境；④ 修复方案为分析性建议，不保证在 Azure 门户/CLI 的落地验证
   - 不修复后果: 违反 SKILL-SPEC §3.1 必需章节要求（部分合规状态），且真实使用中 agent 可能越界执行 on-prem 操作

3. **修正语法错误（5 处）**（SKILL.md L33-35、L130、L194）
   - L33: "it's owned by azure" → "it is owned by Azure"
   - L34: "as it break" → "as it breaks"
   - L35: 与 L34 合并（见第 7 项）或改为 "as it breaks all other traffic running"
   - L130: "mandates hub-to-hub traffic goes" → "mandates that hub-to-hub traffic goes"
   - L194: "prohibited operation and cannot solve the issue" → "A prohibited operation; does not solve the issue"
   - 不修复后果: dossier 已标记的"多处语法瑕疵"持续存在，影响语料整体质量声誉

4. **Output Expectations 与 SCORING 对齐**（SKILL.md L222-229）
   - 新增第 5 条: "Classify **every** candidate fix from `possible_solutions.json` as valid or invalid, referencing the tier logic"——对应 SCORING OUT-02
   - 修改第 1 条: 补充 "and name the specific ASN / preference edge that must be filtered or overridden"——对应 SCORING QA-01（示例已在 Tier 2 L147 演示：vhubvnet1 ASN 65002 过滤来自 vhubvnet2 的路由）
   - 可附加一个简单输出模板（如: 问题诊断 → 修复推荐（Tier + 具体 ASN/边）→ 禁用方案拒绝 → possible_solutions 分类表）
   - 不修复后果: 即使 agent 全部推理正确，OUT-02/QA-01 两项（占 16 项中的 2 项）可能因输出未显式覆盖而丢分——这是与评测分数的直接相关性最高的修复

5. **厘清 Tier 2 泄漏修复的出口/接收侧语义**（SKILL.md L149-157）
   - 将泄漏修复拆为两组: **出口侧**（谷底导出规则、no-export communities——直接修复本网络导出的泄漏）与 **接收侧防护**（ingress filtering、RPKI——纵深防御，防止外部泄漏进入，不直接修复本网络的出口泄漏）
   - 与 Common Pitfalls L216 的口径统一（"Ingress filtering alone doesn't stop export of other leaked routes"）
   - 不修复后果: Tier 2 修复菜单与 Common Pitfalls 自相矛盾，agent 可能误以为 ingress/RPKI 已解决泄漏问题

6. **完善 Step 2 伪代码边界**（SKILL.md L77-90）
   - 补充: "Run `find_cycle` from every ASN in preferences.json"（遍历所有起点）
   - 在 Step 1 增加自环校验: 若 `preferences.json` 中某 ASN 的偏好下一跳是其自身，判为输入非法
   - 不修复后果: 起点选取不当可能漏检环；自环数据会被误判为振荡

7. **定义 Step 1 校验失败后的行为**（SKILL.md L55-61）
   - 当前: "If this fails, the input is invalid."（L61）——然后呢？
   - 修复方向: "Report the invalid input and stop analysis, or proceed with only the valid subset, flagging the issue"——与评测场景（runner 注入的输入应合法）配合，明确 agent 不得在无效输入上强行推理
   - 不修复后果: agent 行为不确定（可能继续分析并产出基于非法输入的结论，污染 OUT/QA 评分）

8. **明确"routing intent 可用性"的判定来源**（SKILL.md L134）
   - 当前: "If routing intent is available, recommend it first."——从何获知可用性？
   - 修复方向: 注明 "Routing intent availability is given in the task inputs (e.g., `possible_solutions.json` or the scenario description); if the input does not state it, assume it is unavailable and proceed to Tier 2"
   - 不修复后果: agent 可能在意图不可用时仍推荐 intent，或在可用时跳过它，影响 PROC-04/PROC-06 判定

9. **统一 BGP 禁用范围口径**（SKILL.md L33 vs L193）
   - 将 L193 "Disable BGP — Not customer-controllable" 与 L33 统一为 "BGP sessions (hub-to-hub and Azure-managed sessions) cannot be administratively disabled by customers"
   - 不修复后果: 口径不一致给 agent 的拒绝理由模板造成轻微混乱

10. **显式声明 customer-export 合法**（SKILL.md L105-108 之后）
    - 新增: "Routes learned from a customer may be exported to anyone; this is never a leak."
    - 不修复后果: SCORING PROC-03 的"不误报 customer-export"要求缺乏 body 直接支撑，judge 判定时缺少文本依据

### 🟢 优化建议（锦上添花）

11. **合并 Core Invariants L34-35 重复条目**
    - 两条语义重复（关 peering 与删连接都会破坏既有流量），合并为一条，同时消除一处语法错误来源

12. **为 SCORING 增加 1-2 个脚本检查**（check.py）
    - 例: NEG-01 辅助检查——agent_output 中若出现 "disable BGP" / "shut down the peering" / "remove connectivity" 且上下文为建议（非拒绝），触发脚本级警告（脚本只能辅助，最终仍需 judge 判定）
    - 理由: 3 个 CF 全凭 LLM judge 主观判定，脚本锚点可提高评分可复现性（当前 check.py 返回空 dict，无任何机器验证）

13. **在 Expected Inputs 中补充 JSON 字段示例**（SKILL.md L44-51）
    - 为 6 个输入文件各给出 1-2 行示例字段（如 `preferences.json`: `{"65002": 65003, ...}`），降低 agent 解析变异性

14. **修正 "All are false." 措辞**（SKILL.md L220）
    - 改为 "None of these are valid fixes."——句子完整、语气一致

### 修复工作量估计
- 预计修改文件数：1-2 个（SKILL.md 必改；check.py 可选）
- 预计新增行数：~25-40 行（Scope/Limitations 节 + Output 扩充 + 泄漏修复分组 + Step 2 补充说明）
- 预计修改行数：~12-18 行（语法 5 处 + ASN + 口径统一 + 伪代码注释）
- 预计耗时：1 小时内可完成全部 🟡 项

---

## 变更记录
- 2026-08-06: 初始深度审查。阅读目录内全部 3 个文件（SKILL.md 235 行 + SCORING.yaml 151 行 + check.py 60 行，共 446 行）。结论: 🟢 B (73/100)。确认 dossier 的两条记录（技术推理严密 ✅ / 多处语法瑕疵 ✅），并新增 6 项 dossier 未记录的问题。

---

## 附录: 审查过程记录
- 读取文件数：3（SKILL.md + SCORING.yaml + check.py，目录内全部文件）
- 读取总行数：446 行
- 辅助参考：`_shared/SKILL-SPEC.md`（v1.0 合规标准）、`_shared/CHECKER-LIBRARY.md`（checker 库文档，确认 `set_tool_log_path`/`set_agent_output` 存在）、`_shared/checker.py`（导入验证）、skill-dossier.md（Batch 251-275 记录）、001-skill-tuning/REVIEW.md 与 322-cold-start-interview/REVIEW.md（13 节审查格式基准）
- 重点深度审查内容：Step 2 伪代码（自环/起点边界）、Tier 2 泄漏修复的出口/接收侧语义、ASN 65001 领域事实、SCORING 16 项 criteria 与 body 的逐条映射、check.py 空实现
- 领域事实核查：Azure Virtual WAN hub 默认 BGP ASN 为 65515（非 65001）——基于 Azure 文档公开默认值
