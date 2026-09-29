# REVIEW: 270-humanizer-academic

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit)
**Skill 名称**: humanizer-academic
**Skill 类型**: process — 学术医学论文 AI 痕迹清除（humanizer）
**源项目**: https://github.com/matsuikentaro1/humanizer_academic（基于 blader/humanizer，Wikipedia "Signs of AI writing" 指南的医学化改编）
**版本**: v2.1.0（README 版本历史自述）
**审查方式**: 全目录 Glob → 全部 12 个文件全文读取（SKILL.md 377 行、README.md 193 行、SCORING.yaml 159 行、check.py 65 行、references 5 个文件 371 行、LICENSE、.gitignore、PNG 结构校验）→ 交叉核对 SKILL-SPEC.md（12 项合规）、_shared/checker.py、邻号 skill 的 SCORING.yaml 惯例 → 撰写本报告。

---

## 执行摘要

这是一个质量相当高、作者身份特征鲜明的测评类 skill。它把 Wikipedia "Signs of AI writing" 的通用 AI 写作痕迹清单系统化改造为 34 个面向医学论文的具体模式（SKILL.md 内 1–18，references/llm-specific-word-choice-patterns.md 内 19–34），每一模式都配有"问题—Before—After—决策规则—边界条件"，并引入了罕见的"作者声音画像"（Voice Calibration）与基于本地 AI 检测器实验（desklib + Binoculars）验证的模式优先级排序（Pattern 34 节奏重构被实验标定为最高杠杆干预）。

审查发现的主要问题集中在**规范合规与测评闭环**两层，而非内容质量本身：

- **规范层**：description 以祈使句开头（违反第三人称硬性要求）、触发信号未落入规范列举的短语模式；Body 缺少规范强制要求的 "Output Format" 与 "Scope/Limitations" 两个正文章节（目前仅存在于 references 中）；`allowed-tools:` 为空值。
- **测评层**：check.py 存在一个确定性逻辑缺陷——`main()` 中读入的 agent 输出内容被 `check()` 内的 `set_agent_output(agent_output)` 用"路径字符串"二次覆盖，导致 `output_not_contains('—')` 实际检查的是文件路径而非输出文本，**PROC-02 永远恒真**，依赖它的 CF-01（em dash 零容忍，cap_to_0）事实上永远不会被脚本触发。
- **自洽层**：skill 自身正文中的说明性 prose 出现约 8 处 em dash（"every em dash must be replaced — regardless…"），与它自己宣传的零容忍规则形成反讽；full-example.md 的 After 范文第 2、3 段重复陈述同一结论（恰好违反它自己定义的 Pattern 32 同义重复）；README 第 77 行表格内残留字面量 `\u201cclinically significant\u201d` 转义文本未渲染。

综合评分 79/100（B+），定位为"内容卓越、规范与测评工程有待修缮"的优质 skill。详细八维评分见第 12 节，逐项修复建议见第 13 节。

---

## 1. 目录清单

目录共 12 个条目，其中 11 个为文本/配置，1 个为图片。逐文件角色与规模如下。

- **SKILL.md**（377 行，21.6 KB，2026-08-05 修改）——skill 主体。含 frontmatter、任务清单、Voice Calibration（作者声音画像）、需保留的学术表达清单、Pattern 1–18 详细规则、Reference Files 索引。正文只含前 18 个模式，19–34 全部外置到 references。
- **README.md**（193 行，15.4 KB）——工程文档。安装/调用方式、34 个模式的 Before/After 速查表（7 张表）、完整示例、来源文献（Fitchett 2019 Circulation；Matsui 2025、Bao 2025、Galpin 2025 三篇词频研究）、作者相关论文与图 1、从 1.0.0 到 2.1.0 的完整版本历史。文档质量高，且版本历史本身就是 skill 演进的可追溯日志。
- **SCORING.yaml**（159 行）——测评标准。17 条 criteria（scope 2 / process 9 / output 3 / negative 2 / qa 1）+ 3 条 critical_failures，全部为 llm 判分，仅 1 条脚本判分（PROC-02）。
- **check.py**（65 行）——测评执行脚本。导入 `../_shared/checker` 库，只执行 PROC-02 一条脚本检查。**存在覆盖 bug（详见第 10 节）**。
- **references/reference.md**（9 行）——知识来源声明：Wikipedia 指南 + Fitchett 2019 文献出处。
- **references/llm-specific-word-choice-patterns.md**（295 行）——Pattern 19–34 的完整细则，本 skill 内容密度最高的文件。
- **references/process-two-pass-draft-audit.md**（30 行）——两遍"草稿—自审"流程与 3 项强制终检。
- **references/output-format.md**（7 行）——输出格式约定（改写稿 + 变更摘要）。
- **references/full-example.md**（30 行）——完整 Before/After 范文与逐条变更说明。
- **2025_Matsui_Delving_into_PubMed_Records_Fig1.png**（262,647 字节，1200×757，RGBA）——作者论文图 1，仅被 README 引用，与执行路径无关。
- **LICENSE**（7 行）——MIT，Copyright (c) 2025 Kentaro Matsui，声明基于 blader/humanizer。
- **.gitignore**（3 行）——忽略 `../ai-detector-score/samples/human_baseline.md`。指向仓库外的相对路径，对 skill 本体无实际作用，属作者工作流遗留。

目录结构完全符合 "NNN-kebab-case" 约定，无大小写、空格问题；references/ 子目录职责划分清晰。唯一结构性质疑是：262 KB 的 PNG 只服务 README 展示，与测评执行无关，属于可裁剪的"展示性资产"。

---

## 2. Frontmatter

**name**: `humanizer-academic`。小写 + 连字符，长度 18，与目录名（去掉 `270-` 前缀后）完全一致，通过。

**description**（252 字符，≤1024 通过）：

> Remove signs of AI-generated writing from academic medical papers. Use when editing or reviewing manuscripts to make them sound more natural and professionally written. Based on Wikipedia's "Signs of AI writing" guide, adapted for medical literature.

逐条核验：

- **WHAT**：明确（清除 AI 写作痕迹，使其更自然专业），通过。
- **WHEN**：给出了触发场景"editing or reviewing manuscripts"，语义上成立，但**未落入 SKILL-SPEC 列举的触发信号短语模式**。规范给出的合法模式为 `"Use when the user..."`、`"Use when the user asks to..."`、`"Use when the user needs to..."`、`"Triggers on..."`、`"Use for..."`；本 description 是 `"Use when editing or reviewing…"`（Use when + 动名词，无 "the user"）。语义完整但短语形式不符，判定为**部分通过**。
- **KEYWORDS**：academic medical papers / manuscripts / natural / professionally written，领域词与动作动词齐备，通过。
- **人称与语态**：**违反第三人称硬性要求**。首句 `"Remove signs of AI-generated writing from academic medical papers."` 是裸祈使句（动词原形开头），与规范明令禁止的 `"Use this skill to..."` 属于同一语法类。应改为 "Removes signs of AI-generated writing…" 或 "A skill that removes signs of AI-generated writing…"。这是本 skill 描述中唯一实质性违规点。
- **无跨 skill 路由**：通过（"Based on Wikipedia's…" 属于来源声明而非路由）。
- **字符数**：252 ≤ 1024，通过；版本历史 2.1.0 声称"为适配 claude install-skill 的 1024 字符限制而精简"，实际占用远低于限制，声明与事实一致。

**allowed-tools**: `allowed-tools:` 后为空值（YAML null）。该键属规范允许的可选字段，但空值既无约束力也无信息量，属于录入草率。建议要么填入实际工具（本 skill 纯文本改写，实际无需任何工具），要么直接删除该键。

**禁字段检查**：无 metadata/license/version/tags 等任何规范禁止字段，通过。非 frontmatter 元数据（MIT、作者、版本历史）已按规范建议放入正文末尾与 README，处理得当。

**小结**：frontmatter 整体合规率约 80%，两个扣分点均集中在 description 的语态与触发信号短语形式；修改成本极低。

---

## 3. Body结构

### 3.1 行数与体量

SKILL.md 正文 377 行，低于 600 行硬上限，通过。但按 SKILL-SPEC 3.2 的模式体量表，skill 自报类型为 `pattern: process`（目标 ~200 行），实际 377 行超出目标约 90%——不过由于 19–34 号模式全部外置到 references，正文的实际密度是"18 个模式的详细规则 + 声音画像 + 保留清单"，这个体量对 process 型 skill 略超但可辩护，且 377 行的规模下阅读负担仍在可接受范围。

### 3.2 章节骨架

正文章节依次为：`# Humanizer Academic…`（标题）→ `## Your Task`（7 步任务清单）→ `## Voice Calibration (Author Reference Profile)` → `## IMPORTANT: Preserve Legitimate Academic Phrases` → `## CONTENT PATTERNS`（1–6）→ `## LANGUAGE AND GRAMMAR PATTERNS`（7–12）→ `## STYLE PATTERNS`（13–15）→ `## FILLER AND HEDGING`（16–18）→ `## Reference Files`。

对照 SKILL-SPEC 3.1 的三项强制章节：

- **Workflow/Process**：`## Your Task` 以 7 个编号步骤描述了完整工作流（识别→节奏重构→改写→保义→保调→具体化→两遍流程），并把两遍流程指引到 references/process-two-pass-draft-audit.md。**基本满足**。但注意两点瑕疵：其一，步骤 7 写的是"see Process section"，而 SKILL.md 正文中并不存在名为 `## Process` 的章节，该指引实际指向 references 文件，措辞有歧义；其二，步骤 2 把"节奏重构 FIRST"写进了任务清单，但 Pattern 34 的完整内容在 references 中，正文只给了摘要句——依赖 agent 主动去读 references。
- **Output Format**：**缺失**。正文没有任何描述"交付物长什么样"的章节，输出格式只存在于 references/output-format.md（7 行）。对照规范"Every SKILL.md body MUST include these three sections"，这是硬性违规。对于本 skill，输出格式（改写稿 + 变更摘要 + 零 em dash）高度可预期，应在正文中加一个简短章节（5–8 行即可）。
- **Scope/Limitations**：**缺失**。正文没有"本 skill 不做什么/何时不该用"的章节。虽然 `## IMPORTANT: Preserve Legitimate Academic Phrases` 从反面界定了"什么不该被当作 AI 痕迹清除"，但这是规则层面的反向约束，不是 scope 章节。建议补一节说明：不适用于非学术文体、不重写数据、不生成新内容、不改动作者事实判断等边界。

### 3.3 文件引用

Reference Files 一节列出 5 个 references 文件，全部为 skill 目录内相对路径，链接名与文件名一一对应（Full Example / Llm Specific Word Choice Patterns / Output Format / Process Two Pass Draft Audit / Reference），无跨 skill 引用（`../other-skill/`），通过。小瑕疵：链接文字与文件名的自然语言映射（如 "Llm Specific Word Choice Patterns" 大小写不规范）不影响解析。

### 3.4 内容组织质量

正文采用"模式编号 + Words to watch 词表 + Problem 描述 + Before/After 成对示例 + 例外条款"的统一模板，18 个模式格式高度一致，可扫读性强。三处突出的亮点结构：Voice Calibration 一节把"人味"从"通用人类风格"收窄为"作者本人的风格"（20–40 词句长、分号/连词、不用 em dash），这在同类 skill 中极为少见，直接支撑 SCOPE-02 的判分；"Preserve Legitimate Academic Phrases" 一节是防止过度修正的防呆设计（对应 NEG-01/NEG-02 两个负向判据）；Pattern 13 的"zero tolerance + DO NOT make excuses"段落是全书最有力的可执行指令。

---

## 4. 逻辑一致性

### 4.1 模式间的交叉引用与例外衔接

逐条核对 34 个模式之间的引用链，逻辑闭环总体严密：

- **Pattern 7（"Additionally" 例外）**：正文限定"每段至多一个"；references 27 号模式的连接词分组中再次注明 "additionally" 每段一次的例外；README 表格同样标注。三处口径一致。
- **Pattern 9（Not only…but also）**：正文按过用模式处理；references Pattern 27 明确修正——"一次自然的 not only…but also…（每段约一次）应保留，这是对 Pattern 9 的细化而非矛盾"。文档主动记录了对旧模式的修订关系，处理规范。
- **Pattern 17（多层 hedging 简化）与 Pattern 22（insufficient hedging 加缓冲）**：两个模式方向相反（一个去层、一个加词），references 用一整段"这不是同一回事"的区分说明把张力化解，且 Pattern 17 正文反向引用 Pattern 22（"See also Pattern 22"），交叉指认正确。
- **Pattern 1 与 Pattern 29**：references 明确标注"Pattern 1 示例中的 markedly reduced median survival 与 Pattern 29 是同一缺陷的两种视角"，防止测评 agent 把同一处改动算作两个独立违规。
- **Pattern 30 与 Pattern 27 的分工**：references 用"Division of labor"段落界定——27 管"不许删什么"，30 管"删了之后必须补什么"，边界清晰。
- **Pattern 23 与 Pattern 28**：同样有显式区分（名词压缩 vs 语义链接过密），无重叠。
- **Pattern 34 与 Pattern 29 的交互**：两个文件（SKILL.md 正文之外的 references 与 README）均记载"删 ornamental adverb 必须伴随句式重构，否则 AI 分数反而上升（logit +0.72）"，实验结论在版本历史 2.0.0 与 Pattern 34 正文中重复出现且数字一致。

### 4.2 数据一致性（EMPA-REG OUTCOME 数字）

对全部 Before/After 示例中的试验数据进行交叉核对（详见附录 D）：住院率 2.7% vs 4.1%、HR 0.65、心血管死亡 3.7% vs 5.9%、全因死亡 5.7% vs 8.3%、HHF/CV 死亡复合终点 34%、HHF 35%、CV 死亡 38%、NNT 35（3 年）、7020 例/590 中心/42 国——在各文件（SKILL.md、README、full-example.md、llm-specific-word-choice-patterns.md）中出现的位置均一致，**未发现数字打架**。35%（HHF）与 34%（复合终点）看似接近实则分属不同终点，文档区分正确，不存在虚假矛盾。

### 4.3 声音画像与节奏建议的张力

Voice Calibration 声称作者"predominantly medium-to-long sentences (20-40 words)，rarely uses <10 word sentences"，而 Pattern 34 建议"some sentences under 15 words, some over 30"。15 词与 20 词下限之间有一个未被显式调解的灰色区间：严格按画像执行（全部 20–40 词）会削弱 Pattern 34 想要的 burstiness，严格按 34 执行（插入 <15 词短句）又可能偏离画像。二者并非矛盾（<15 词仍远高于 <10 词的禁区），但这是全文档唯一一处"两个权威指令未互相引用"的校准缝隙，建议在 Voice Calibration 中补一句桥接说明。

### 4.4 自反性反讽（self-referential irony）

这是本 skill 最有趣的发现，也是"逻辑一致性"里最不该放过的一处：**文档自身违反了自己的规则**。

- **Em dash**：SKILL.md 全文件含 23 个 em dash（—）。其中约 8 个出现在**说明性 prose**而非示例文本里——最刺眼的是 Pattern 13 的规则句本身：第 269 行 "every em dash must be replaced — regardless of whether it…"、第 271 行 "you are wrong — replace it"、第 340/348 行的 Principle 与 NOT 示例句、第 79/184 行的清单行。一个"对 em dash 零容忍"的章节用 em dash 给自己划线，措辞上是反讽的（示例中的 em dash 是教学必需，可以豁免；prose 中的 8 处无此豁免）。
- **全大写标题**：Pattern 14 声称"AI 会把标题中所有主词大写"是 AI 痕迹，而正文自身四个分区标题全部全大写（`## CONTENT PATTERNS`、`## LANGUAGE AND GRAMMAR PATTERNS`、`## STYLE PATTERNS`、`## FILLER AND HEDGING`）。全大写与 Title Case 不同，不算直接违规，但与 14 号模式想表达的精神（标题要低调）不协调。
- **full-example.md 的同义重复**：范文 After 第 2 段末句 "empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%" 与第 3 段第 2 句 "Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care" 是同一结论的两次陈述——恰好踩中 Pattern 32（paraphrastic repetition）自己定义的缺陷。README 中的同名 After 范文反而没有此重复（README 版本更干净）。旗舰示例出现自身规则的漏网之鱼，应修复。

### 4.5 其他一致性

- "Your Task" 7 步与 references/process-two-pass-draft-audit.md 的两遍流程兼容（任务清单是概要，流程文件是步骤级展开），无冲突。
- README 版本历史（2.1.0 → 1.0.0）与 references 内容的时间线对应关系自洽：2.0.0 引入 Pattern 34 与 Voice Calibration，references 中二者确实存在。
- SCORING.yaml 的 SCOPE-02 对声音画像的描述（"20-40 word sentences, semicolons/conjunctions, no em dashes, no staccato drama"）与 Voice Calibration 逐字对应。

**结论**：逻辑一致性总体评分优秀（内部引用链、例外条款、实验数据三方面都做得扎实），扣分集中在 4.3 的校准缝隙与 4.4 的三处自反性反讽。

---

## 5. 参考文件（逐文件全文分析）

### 5.1 references/reference.md（9 行）

一份极简的来源声明：本 skill 基于 Wikipedia "Signs of AI writing"（WikiProject AI Cleanup 维护），医学示例改编自 Fitchett 2019 的 EMPA-REG OUTCOME Circulation 论文，并注明该文 CC-BY-4.0 授权。内容与其使命（出处追溯）完全匹配，无冗余。小瑕疵：与其他 reference 文件不同，本文件没有标题层级锚点以外的结构化信息（如"何时需要读它"的指引），但作为纯来源声明可接受。与 README 中 References 一节的文献信息完全一致，无冲突。

### 5.2 references/llm-specific-word-choice-patterns.md（295 行）——本 skill 的知识核心

全文件覆盖 Pattern 19–34，共 16 个模式，与 SKILL.md 的 1–18 无缝衔接、无重叠无断档。逐项评估：

- **19（linked to → associated with）**：罕见的"反盲换"设计——明确警告不要把所有 "link" 一律换成 "associated with"，并给出名词 link / 数据 linkage / 下游结果 / 整句重构四类情形的分派表。这是 34 个模式中最精细的决策规则之一。
- **20–21（Beyond / via）**：标准替换规则 + 例句，简洁有效。
- **22（insufficient hedging）**：与 Pattern 17 的区分说明（见 4.1）是全文最重要的防混淆设计；"may help reduce" 这类双词缓冲的语义（因果性的有意保留 vs 17 号的多层堆叠）讲得清楚。
- **23（artificially condensed expressions）**：Type A（名词连字符复合，fatigue–sleepiness cycle）与 Type B（抽象速记，mutual reinforcement）双分类，且 Type A 的示例恰好示范了 en dash 复合词的改写——注意这与 Pattern 13 的 em dash 规则不同维度，文档未混淆二者。
- **24（where 非处所连接）**：给出保留条件（物理位置/数据集/限定条件）与替换偏好（优先 "with"，明示避免以 "in which" 作为默认替代，因为 "in which" 本身也是 AI 痕迹）——这条"不要用 A 替换 A 的同类"的警告是全文档少见的深度洞见。
- **25（yield）**：替换词表 + "化学产率语境保留"的例外，精确。
- **26（remain/given）**：两条微调规则，示例即事实。
- **27（preserve discourse markers）**：全文最重要的"防过度修正"章节。核心判据是那条可操作的二分类问题——"这个词是膨胀含义（删）还是让逻辑显式化（保留）"；随后给出连接词按逻辑关系（结果/添加/对比/让步/理由/序列）分组表与"不要为装饰而撒连接词"的护栏（明确这不是 Pattern 11 的例外）。**"甜点区"基准段**（pre-AI 人类论文密集使用 discourse markers + 零膨胀词）是本文件乃至全 skill 最具洞察力的段落。
- **28（re-contextualize）**：3 行示例 + 与 23 的边界说明。
- **29（ornamental -ly adverbs）**：装饰性词表（14 个）与功能性词表（9 个）双向列示 + "删掉副词试想信息是否损失"的决策规则 + 人类论文用副词方式的基准段（"consistently/slightly/modest 都有量化或校准功能"）。与 Pattern 1 的交叉引用已在 4.1 记录。
- **30（connective-preserving edits）**：以"错误修法（裸删）vs 正确修法（补连接）"的对比对展示 asyndeton 缺陷，给出三条补链手段（换连接词/回声名词/合并重写），并以 "Division of labor" 段落与 27 号划界。
- **31（paragraph cohesion）**：给出段落内旧-新信息流与段际开头标记的两层要求，附 3 条可勾选清单——与 process 文件终检 8 一一对应。
- **32（paraphrastic repetition）**：触发词表（In other words / That is / Put differently…）+ 双示例 + 关键例外（"把 HR 0.65 翻译成降低 35% 属于信息增量，不是同义重复"）——例外的定义精确，防止误删。
- **33（content-free evaluation sentences）**：与 Pattern 1/3 的三方划界（嵌入式膨胀 vs -ing 尾巴 vs 独立裁决句）+ 带理由的例外句允许保留。
- **34（sentence rhythm）**：实验数据（desklib logit 5.54→2.47，55% 降幅；~90% 的可达改善归因于节奏）、4 条结构操作（变句长/变开头/移成分/用分号）、4 条禁止（不改术语数据义、不引入 staccato、不断连接、不改变语态）、与 29 号的交互警告（+0.72 反效果）、人类段落句长基准（12–55 词、SD 10–15）。可执行性全文件最高。

**总体评价**：该文件把"怎么改"提升到了"怎么改才不像自动清理过的"的层次——27/29/30/31 四个模式专门防御"humanizer 自身产生的 AI 痕迹"，这是同类 skill 中罕见的元认知设计。若一定要挑毛病：Pattern 34 的 "desklib logit 5.54→2.47" 数字无法在文档内复核（实验细节未附），对测评 agent 而言属于不可验证断言；且文件缺少一个"19–34 目录索引"（295 行无锚点目录），快速定位依赖滚动。

### 5.3 references/process-two-pass-draft-audit.md（30 行）

两遍流程（Pass 1 草稿改写 4 步、Pass 2 自审 2 步）+ 3 项强制终检（EM DASH CHECK / PARAGRAPH COHESION CHECK / RHYTHM CHECK）。与 SCORING.yaml 的 PROC-09、QA-01 直接对应（终检 7/8/9 分别对应 PROC-02 脚本、PROC-08 段落衔接、Pattern 34 节奏）。第 5 步的自审提问（"What makes this draft still look AI-generated?"）把自查从"查清单"升级为"攻击性找茬"，设计优于多数 skill 的 checklist 式自查。结构紧凑、无废话。唯一小缺点：文件没有落款日期或版本号，无法与 README 版本历史对应（2.0.0 声称"Upgraded Process to two-pass draft-audit loop"，此文件即该产物，但文件自身无版本标注）。

### 5.4 references/output-format.md（7 行）

两行要求：输出 = 改写文本 + 变更摘要（注明应用了哪些模式、做了什么节奏重构）。与 SCORING OUT-02 逐字对应，也与 README 中 "Full Example" 后附 "Changes made" 清单的样例格式一致。内容正确但过于简略——没有给出摘要的组织模板（如按模式编号分组、每条一句），agent 的自由发挥空间大，这也是 SKILL.md 正文缺 Output 章节的连锁后果。

### 5.5 references/full-example.md（30 行）

完整 Before（3 段，集中堆叠 1/2/3/4/5/6/7/8/13/17/18 号模式的缺陷）与 After（3 段）+ 12 条 "Changes made" 清单。Before 的缺陷密度与 After 的改写手段对应关系清晰，12 条变更说明逐条标注了模式编号与例外（"the 'Additionally' disappeared only because its whole sentence was rewritten" 这条尤其专业——它把"为什么范文里没有 Additionally"预先解释清楚，防止读者误以为范文违反 7 号模式）。主要缺陷已在 4.4 记录：**After 第 2、3 段重复同一结论，违反 Pattern 32**；且 After 第 3 段三句（HF 诊断局限→empagliflozin 获益→各亚组一致）之间存在段内跳跃，与 Pattern 31 的"段首句陈述主张"理想态略有距离。除此之外，范文质量高，是可直接对照学习的样例。

### 5.6 README.md（193 行，工程文档）

超出"参考文件"范畴的配套文档，但影响 skill 的对外呈现。亮点：34 模式速查表（7 张表）使 README 可独立充当 cheat-sheet；版本历史 1.0.0–2.1.0 完整记录了每次模式增补与修订动机；三篇词频研究文献（Matsui 2025 / Bao 2025 / Galpin 2025）+ Fitchett 2019 的引用规范。问题点：第 77 行 Pattern 15 表格的 Before 单元格内是**字面量转义文本** `\u201cclinically significant\u201d`（应渲染为弯引号"clinically significant"），这是典型的"转义序列未被解析"的复制粘贴事故；第 116–118 行的 Pattern 34 引文块与 references 的数字重复但表述略异（"~90% of the achievable improvement" 一致，无冲突）；"This is a paper I wrote… Take a look if you're curious!" 一句是作者个人口吻，对正式文档略随意，但反而强化了人机感（见第 8 节）。

### 5.7 图片与辅助文件

- **PNG**（262 KB，1200×757 RGBA）：有效 PNG（文件头/IHDR 校验通过），README 声明为 Matsui 2025 论文图 1（AI 影响词汇趋势图），CC-BY 4.0 再发布并注明出处。仅 README 引用，不进执行路径。本审查环境无法渲染 RGBA 图像，**像素内容未能目检**（列入第 11 节 Skip）。
- **LICENSE**：MIT，版权 2025 Kentaro Matsui，保留 blader/humanizer 归属。无问题。
- **.gitignore**：指向仓库外路径 `../ai-detector-score/...`，对 skill 分发无意义但无害。

---

## 6. 语法格式

- **Markdown 结构**：SKILL.md 标题层级规范（H1 唯一，H2 分区，H3 模式），代码引用用 `>` blockquote，Bold 标记使用一致。references 文件标题层级从 H2 起（作为被引用的子文档），合理。
- **README 第 77 行转义事故**：`\u201cclinically significant\u201d` 以字面量形式出现在表格中，未渲染为弯引号，读者会看到一串乱码般的转义文本。这是全 skill 唯一一处明显的"显示层面"缺陷。
- **连字符/破折号混用**：`Your Task` 清单使用 "**Label** - text" 的连字符分隔；其余正文多用全角/半角破折号；references 内使用 en dash 于区间（"1–2"、"5.54→2.47"）。风格未统一，但均不构成渲染问题。
- **Frontmatter 空值**：`allowed-tools:` 尾随空值，YAML 解析为 null，合法但草率。
- **SCORING.yaml 语法**：经 PyYAML 解析验证有效；注释用 `# ── Scope (2 items) ──` 的框线风格，与邻号 skill（269/271）格式惯例一致。`total_items: 17` 与 criteria 实际条数 17 一致（critical_failures 3 条不计入），与邻号 skill 的口径一致。
- **check.py**：语法可解析，导入路径 `../_shared/checker` 解析到实际存在的库（output_not_contains 等函数签名与调用匹配）；docstring 声明的调用方式（3 个位置参数）与 main() 实现一致。**但存在逻辑 bug，详见第 10 节**。
- **中文/英文混杂**：SKILL.md 与 references 全英文（面向英文医学写作，合理）；SCORING.yaml 注释含中文字符，编码 UTF-8 正常。
- **行尾与编码**：全部文件 UTF-8 可正常解码，无 BOM 异常；Windows 环境 CRLF/LF 混用未检出影响。

---

## 7. 规范合规（12 项）

对照 `_shared/SKILL-SPEC.md` 的 12 项合规清单逐项判定：

1. **name 小写+连字符、≤64、与目录一致** —— 通过。`humanizer-academic` 与 `270-humanizer-academic`（去 NNN 前缀）完全一致。
2. **description 第三人称、含 WHAT+WHEN+KEYWORDS、≤1024** —— **部分通过**。WHAT/WHEN/KEYWORDS/长度均达标，但首句为祈使句（见第 2 节），第三人称要求不满足。
3. **description 无祈使/第一/第二人称** —— **不通过**。"Remove signs of…" 是裸祈使句。
4. **description 无跨 skill 路由** —— 通过。
5. **description 至少一个触发信号短语** —— **部分通过**。"Use when editing or reviewing manuscripts…" 含 "Use when" 语义，但未命中规范列举的 `"Use when the user..."` / `"Triggers on..."` / `"Use for..."` 等精确模式。
6. **frontmatter 无禁字段** —— 通过。仅 name/description/allowed-tools 三键（allowed-tools 空值不违规但建议清理）。
7. **body ≤600 行** —— 通过（377 行）。
8. **body 含 workflow/process 章节** —— 通过（`## Your Task` 7 步 + references 两遍流程，满足"任何章节名均可"的弹性）。
9. **body 含 output format 章节** —— **不通过**。仅存在于 references/output-format.md。
10. **body 含 scope/limitations 章节** —— **不通过**。全文无 Scope/边界章节。
11. **body 无跨 skill 文件引用** —— 通过。5 个引用全部为 skill 内相对路径。
12. **目录 NNN-kebab-case、无空格大写** —— 通过。

**统计**：12 项中 9 项通过、2 项不通过（#9、#10）、2 项部分通过（#2、#5）。合规完成度约 75%–83% 区间（通过 9 + 部分 2 + 不通过 2）。两项不通过项均为"补章节"级别的小改，两项部分通过项合并为 description 的一次重写即可解决。

---

## 8. 人机感

本 skill 的"人味"是全语料库中辨识度最高的之一，判断依据如下：

- **作者声音真实可感**：Voice Calibration 一节不是抽象的"写自然一点"，而是具体的"作者本人怎么写"——20–40 词句长、分号连接、不用 em dash、限段一个 "Additionally"、结论以 "In conclusion" 开头。这种把"人味"参数化为可判分特征的做法，本身就是人类作者自我建模的结果。
- **指令具有人格与情绪**："Do NOT make excuses"、"If you find yourself thinking 'this one is fine,' you are wrong — replace it."、"No exceptions. Not even one."——这些句子有作者的情绪立场，不像是模板生成。README 末段的 "This is a paper I wrote… Take a look if you're curious!" 是典型的个人项目口吻。
- **经验性知识而非泛泛建议**：Pattern 29 的功能/装饰副词二分、Pattern 24 对 "in which" 的警告、Pattern 30 的"裸删也是 AI 痕迹"——这些是只有真编辑过论文才会有的经验颗粒度。实验数据（desklib logit 值）的引用进一步强化了"作者做过验证"的可信感。
- **反面证据**：全大写分区标题（`## CONTENT PATTERNS` 等）与 Pattern 14 的精神相悖；Pattern 13 的 prose 自带 em dash（4.4 已述）；"No exceptions. Not even one." 与下一段 "DO NOT make excuses" 存在修辞上的重复强调，略有冗余；SCORING.yaml 的 `# ──` 注释风格偏工程化。但这些是风格层面，不影响"文档像人写的"这一主判断。

**结论**：人机感 9/10——这是语料库中少见的"有明显人类作者指纹"的 skill，主要扣分来自全大写标题与自反性 em dash 对"专业性人设"的轻微破坏。

---

## 9. 可执行性

- **模式可操作性强**：34 个模式全部提供"触发词表（Words to watch）→ 问题说明 → Before/After → 决策规则 → 例外"，agent 无需自行推断触发条件即可机械套用。Pattern 13 甚至给出了替换选项矩阵（括号/逗号/句号/分号）与强制终检步骤，Pattern 29 给出"删词后信息是否损失"的判定程序。
- **流程可执行**：两遍流程（草稿 → 自审 → 3 项终检）步骤编号明确，终检内容可逐条执行（搜索 "—"、段落衔接清单、句长波动检查）。
- **判分可执行**：SCORING 的 17 条 criteria 全部可映射到具体技能内容，OUT-01（数据保真）与 OUT-02（输出格式）的判据与文档要求逐字对应，CF 定义明确。
- **执行风险点**：
  1. **模式分布在两个文件中**：19–34 号模式的全部细则在 references/llm-specific-word-choice-patterns.md，SKILL.md 只给一行摘要。若 agent 未读取 references，将丢失 16/34 的模式覆盖，而 SCORING 没有任何条目验证 references 是否被读取（无 tool_log_contains 类检查，见第 10 节）——这是本 skill 可执行性最大的结构漏洞。
  2. **"see Process section" 指针歧义**：SKILL.md 内无 `## Process` 章节，指引落到 references 文件，agent 需自行推断。
  3. **Pattern 34 的量化断言不可复核**：logit 值无实验附录，agent 无法验证也无从遵循具体数值（但"先做节奏、后改词汇"的排序指令是可直接执行的）。
  4. **输出格式约束薄弱**：output-format.md 只有两行，变更摘要无模板，agent 输出结构化程度依赖自觉。
- **脚本可执行**：check.py 的 CLI 契约清晰（3 参数、JSON 输出），依赖库存在，唯一问题是被覆盖 bug 使 PROC-02 失效（详见下节）。

**结论**：规则与流程层面 9/10，但"模式分布 + 无引用消费校验 + PROC-02 失效"三者叠加使端到端测评闭环存在真实裂缝，综合判定 7/10。

---

## 10. SCORING 交叉参考

### 10.1 结构与映射完整性

SCORING.yaml 与 SKILL-SPEC/邻号 skill（269-latex-posters、271-scientific-slides）的结构惯例完全一致（skill / pattern / total_items / criteria / critical_failures 五键），`total_items: 17` 与 criteria 实数一致。17 条 criteria 逐条与 skill 内容映射核查：

- SCOPE-01/02 → "Your Task" + Voice Calibration（20–40 词/分号/无 em dash/staccato 禁止），对应关系直接。
- PROC-01 → Pattern 34 优先级（节奏 FIRST），判据问题与文档指令逐字对应。
- PROC-02 → Pattern 13 零容忍，`fn: output_not_contains` + pattern "—"，与 check.py 实现一致（**但实现有 bug，见 10.2**）。
- PROC-03 → Patterns 1/7/29/19/20/21/25/24 的合并判据，问句列全了词类，无遗漏。
- PROC-04 → "Preserve Legitimate Academic Phrases" 节 + Pattern 27，对应。
- PROC-05 → Pattern 11 术语一致性，对应。
- PROC-06 → Pattern 17/22 的 hedge 校准，对应。
- PROC-07 → Pattern 30 补链规则，对应。
- PROC-08 → Pattern 31 段落衔接，对应。
- PROC-09 → references/process 两遍流程，对应。
- OUT-01 → 数据保真，判据（"numbers identical to original"）合理且无脚本化——注意 CF-02 与 OUT-01 是同一事实的两种后果（out-01 是常规判据，CF-02 是 cap_to_0 触发），这种"普通项/致命项"双轨设计正确。
- OUT-02 → output-format.md，对应。
- OUT-03 → Patterns 1/4/18 的合并判据，对应。
- NEG-01/02 → 两个"不要过度修正"的负向判据，与 Preserve 节对应——这是语料库中少见的负向合规设计，值得肯定。
- QA-01 → 终检 7/8/9 的合并判据，对应。
- CF-01/02/03 → 全部有文档依据（Pattern 13 / OUT-01 / Patterns 1+34），无"无中生有"的致命项。

**映射完整性结论**：17 条 criteria + 3 条 CF 全部有文档锚点，覆盖了 scope/process/output/negative/qa 五类，设计质量高。

### 10.2 check.py 逻辑缺陷（本审查最重要的技术发现）

`main()` 的执行顺序是：读 agent_output 文件内容 → `set_agent_output(内容)` → 调用 `check()`；而 `check()` 内第一行又执行 `set_agent_output(agent_output)`，**把刚写入的文件内容覆盖为路径字符串**（如 `D:\...\output.txt`）。随后 `output_not_contains('—')` 实际对路径字符串做正则搜索——路径中不含 em dash，于是 **PROC-02 恒真，永远无法失败**。后果链条：

1. PROC-02（唯一脚本判据）形同虚设；
2. CF-01（em dash 残留 → cap_to_0）依赖的正是这条检查，**致命降级机制永远不会被脚本触发**，只能靠 QA-01 的 llm 判分兜底；
3. 修复方式二选一：在 `check()` 内删除 `set_agent_output(agent_output)`（让 main() 读入的内容生效），或把 main() 读入的内容作为参数传入 check()。删除一行即可。

（注：无法在无 runner 环境与样例输出的条件下实测复现，但静态执行顺序分析是确定性的，该 bug 成立。）

### 10.3 测评设计缺口

- **无 references 消费校验**：19–34 号模式在 references 中，但 SCORING 没有任何 `tool_log_contains("llm-specific-word-choice-patterns")` 类判据，也没有对 agent 打开过程文件的检查。一个只读 SKILL.md 的 agent 可以靠 18 个模式混过 PROC-03/OUT-03 的部分判据，且不会被任何 criteria 发现。建议增加 1 条 process 类脚本判据（tool_log 含 references/llm-specific-word-choice-patterns.md 的 Read 调用）。
- **llm 判分占比过高**：17 条 criteria 中 16 条为 llm 判分，唯一脚本判分失效后，全部判分依赖 LLM 主观性。虽然 PROC-02 这种"输出字符级检查"本应适合脚本化，但其他条目（如 PROC-01 的"节奏先于词汇"的时序判断）确实难以脚本化——当前配比在语料库中属常态，不作扣分项，仅记录。
- **OUT-01 数据保真的判据弹性**："all numbers identical" 作为 llm 问句可判，但无脚本化的数字 diff 校验，风险可接受（医学文本改写任务中数据条目有限）。

---

## 11. Skip（跳过/不适用项）

本节登记本审查中**有意未执行或无法执行**的项目，避免与"未发现问题"混淆：

1. **PNG 像素级内容审查**：审查环境无法渲染 RGBA 图像（转换 JPEG 后仍无法读取），图 1 仅完成结构校验（有效 PNG、1200×757、262 KB、IHDR 正常）与引用核验（README 声明为 Matsui 2025 图 1、CC-BY 4.0、出处注明）。图像内容是否与论文图 1 一致未验证。
2. **check.py 端到端运行验证**：需要 runner 环境（workspace/tool_log/agent_output 三参数与样例会话）方可实测；本审查以静态执行顺序分析确证 PROC-02 覆盖 bug（10.2），未做运行时复现。
3. **与 Wikipedia "Signs of AI writing" 原始条目的逐条比对**：来源为外部页面，未逐条核验 34 个模式与维基指南的对应关系；本文仅核验了 skill 内部一致性。
4. **SCORING 判分项的实际执行效果**：16 条 llm 判分条目的真实区分度需实测会话数据，本审查只做条目-内容映射核查。
5. **README 版本历史中 1.2.x 之前条目的行为级验证**（如 "Underused Classical Academic Terms" 模式的退役声明）：仅确认了版本史自述的内部一致性，未考古更早版本源码。

---

## 12. 综合评分（8 维 → /100）

评分原则：内容质量权重高于规范性；每一维度给出评分理由与对应证据位置。

| 维度 | 满分 | 得分 | 要点 |
|---|---|---|---|
| 1. 内容质量与知识密度 | 20 | 19 | 34 个模式、成对示例、词表、决策规则、实验数据；"-1"：Pattern 34 实验数字不可复核 |
| 2. 逻辑一致性 | 20 | 16 | 交叉引用链与数据一致性极佳；"-4"：prose 自用 em dash、full-example 违反 Pattern 32、Voice 与 P34 句长口径未桥接 |
| 3. 参考文件质量 | 15 | 14 | 19–34 细则极深，"防过度修正"设计罕见；"-1"：无目录索引、无版本标注 |
| 4. Frontmatter 与描述 | 10 | 6 | name/长度/禁字段全过；祈使开头违规、触发信号短语不符、allowed-tools 空值 |
| 5. Body 结构完整性 | 10 | 6 | ≤600 行、引用规范、Workflow 达标；缺 Output Format 与 Scope 两节、指针歧义 |
| 6. 语法格式 | 10 | 8 | 整体规范；README `\u201c` 转义事故、破折号风格不统一 |
| 7. 规范合规（12 项） | 10 | 7 | 9 过 2 不过 2 部分（见第 7 节明细） |
| 8. 可执行性与测评闭环 | 5 | 3 | 模式可执行性极高；PROC-02 恒真 bug、无 references 消费校验 |
| **合计** | **100** | **79** | **B+ / 良好偏上** |

**等级解读**：79 分对应"内容卓越、需修缮规范与测评工程"的定位。内容层（维度 1+2+3 = 48/55）达到语料库顶尖水平；工程层（维度 4+5+6+7+8 = 30/45）被四类可修复问题拖累。若完成第 13 节全部 🔴 修复，预计可升至 90–92 分区间；完成 🟡 后可达 94+。

---

## 13. 修复建议（🔴🟡🟢）

按严重度排序。🔴 为影响合规判定或测评有效性的必改项，🟡 为应改项，🟢 为可选打磨项。

### 🔴 必改（4 项）

1. **修复 check.py 的 agent 输出覆盖 bug**（测评有效性）。`check()` 内第 21 行 `set_agent_output(agent_output)` 用路径覆盖了 `main()` 读入的输出内容，导致 PROC-02 恒真、CF-01 永不触发。删除该行（或改为由 main() 传入已读内容）即可。修改后建议补一条含 em dash 的负向冒烟测试。
2. **description 改为第三人称并补触发信号短语**。首句改为 "Removes signs of AI-generated writing from academic medical papers."（或 "A skill that removes…"），WHEN 句改为规范短语形式，如 "Use when the user is editing or reviewing a manuscript to make it sound more natural and professionally written."。一次重写同时解决第 2 节的两项部分通过与第 7 节第 3 项不通过。
3. **在 SKILL.md 正文补 "## Output Format" 章节**（5–8 行）：改写稿 + 变更摘要（模式编号 + 节奏重构说明），与 references/output-format.md 保持一致。满足规范第 9 项。
4. **在 SKILL.md 正文补 "## Scope and Limitations" 章节**：明确不适用于非学术文体（营销/创意/口语）、不重写数据或事实、不新增内容、对已有合法学术表达不做清除（指向 Preserve 节）。满足规范第 10 项。

### 🟡 应改（7 项）

5. **清除 SKILL.md 说明性 prose 中的 8 处 em dash**（第 79/184/269/271/340/348 行附近的规则句与清单句），改逗号/句号。示例文本中的 em dash 保留（教学必需），但在规则句上消灭自反性反讽。顺手可将四个全大写分区标题改为句首大写（Sentence case），与 Pattern 14 的精神统一。
6. **修复 full-example.md After 第 2/3 段的同义重复**：删除或改写第 3 段 "Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care"，替换为新的信息（如亚组一致性），或直接对齐 README 中更干净的范文版本。旗舰示例必须无懈可击。
7. **修复 README 第 77 行的 `\u201c` 转义事故**：将字面量 `\u201cclinically significant\u201d` 替换为真实弯引号字符，或改用描述性文字（"curly quotes"）。
8. **Voice Calibration 与 Pattern 34 的句长口径桥接**：在 Voice Calibration 补一句说明，如"20–40 词为主体句长；为节奏多样性允许 15–20 词的辅助短句，但避免 <10 词的 staccato"。消除第 4.3 节的灰色区间。
9. **"see Process section" 指针修正**：SKILL.md 第 22 行改为明确文件路径（如 "see references/process-two-pass-draft-audit.md"），消除歧义。
10. **SCORING 增加 references 消费校验**：新增 1 条 process 类脚本判据（如 tool_log 含对 references/llm-specific-word-choice-patterns.md 的 Read 调用），堵住"只读 SKILL.md 丢一半模式"的测评缺口。
11. **清理 frontmatter 空值**：删除空 `allowed-tools:` 键或填入实际工具名。

### 🟢 可选（4 项）

12. **给 llm-specific-word-choice-patterns.md 增加锚点目录**（295 行无索引，建议在文件头加 16 个模式的编号链接表）。
13. **为 references 文件补充版本/日期标注**，与 README 版本历史形成可追溯闭环。
14. **PNG 资产瘦身**：262 KB 的 README 展示图可压缩（调色板化/降采样）或外链托管，与执行路径无关。
15. **README 版本历史改为精简表格**：目前 12 行叙事型条目，可压缩为"版本—要点"两列，保留全部信息但降低维护成本。

---

## 附录

### 附录 A：逐文件清单

| 文件 | 行数/大小 | 角色 | 修改日期 |
|---|---|---|---|
| SKILL.md | 377 行 / 21.6 KB | skill 主体（Pattern 1–18） | 2026-08-05 |
| README.md | 193 行 / 15.4 KB | 工程文档与速查表 | 2026-07-31 |
| SCORING.yaml | 159 行 | 测评标准（17+3 条目） | 2026-08-05 |
| check.py | 65 行 | 脚本判分执行器 | 2026-08-05 |
| references/reference.md | 9 行 | 来源声明 | 2026-08-05 |
| references/llm-specific-word-choice-patterns.md | 295 行 / 24.1 KB | Pattern 19–34 细则 | 2026-08-05 |
| references/process-two-pass-draft-audit.md | 30 行 | 两遍流程与终检 | 2026-08-05 |
| references/output-format.md | 7 行 | 输出格式 | 2026-08-05 |
| references/full-example.md | 30 行 | 完整范文 | 2026-08-05 |
| 2025_Matsui_..._Fig1.png | 262,647 B | README 展示图 | 2026-07-31 |
| LICENSE | 7 行 | MIT | 2026-07-31 |
| .gitignore | 3 行 | 工作流遗留 | 2026-07-31 |

### 附录 B：34 个 Pattern 的分布

- SKILL.md 正文：1–18（Content 1–6 / Language-Grammar 7–12 / Style 13–15 / Filler-Hedging 16–18）。
- references/llm-specific-word-choice-patterns.md：19–34（词选 19–26 / 衔接与篇章 27–31 / 语义冗余 32–33 / 句法节奏 34）。
- 编号连续、无重叠、无断档；两个文件各自内部的子编号（Pattern 19 下再分四类替换情形）不产生编号冲突。

### 附录 C：12 项合规核对明细（含判定依据）

逐项判定结果已在第 7 节给出，此处补充证据行号：判定 2/3/5 依据为 description 全文（SKILL.md 第 3 行）；判定 8 依据为 `## Your Task`（第 12–22 行）；判定 9 依据为全文无 Output 章节、仅 Reference Files（第 371–377 行）指向 references/output-format.md；判定 10 依据为全文无 Scope/Limitations 字样；判定 11 依据为 5 个引用链接均以 `references/` 开头且文件实际存在。

### 附录 D：EMPA-REG OUTCOME 数据一致性核对

| 数据点 | 数值 | 出现文件（抽查行） | 一致性 |
|---|---|---|---|
| 试验规模 | 7020 例 / 590 中心 / 42 国 | SKILL.md P2、README 表 | 一致 |
| HHF 住院率 | 2.7% vs 4.1% | SKILL.md P3、P11 | 一致 |
| HR（HHF） | 0.65（95% CI 0.50–0.85） | SKILL.md P3 | 一致 |
| CV 死亡 | 3.7% vs 5.9% | SKILL.md P11 | 一致 |
| 全因死亡 | 5.7% vs 8.3% | SKILL.md P11 | 一致 |
| HHF/CV 死亡复合终点 | 34% | SKILL.md P7、README、full-example | 一致 |
| HHF 单独降低 | 35% | SKILL.md P5、README 表 5 行 | 一致（与 34% 分属不同终点） |
| CV 死亡降低 | 38% | SKILL.md P5 | 一致 |
| NNT | 35（3 年） | SKILL.md P7、full-example | 一致 |
| 作者声音画像 | 20–40 词/分号/无 em dash | Voice Calibration、SCOPE-02 | 一致 |

### 附录 E：审查方法与限制

- 方法：目录 Glob（12 文件）→ 全部文本文件全文读取 → 与 SKILL-SPEC.md（12 项合规）、_shared/checker.py（check.py 依赖）、269/271 号 skill 的 SCORING.yaml（惯例比对）交叉核验 → 数字与交叉引用逐项核对 → 撰写本报告。辅助脚本（_verify.py）已在使用后删除，未污染 skill 目录。
- 限制：① RGBA PNG 无法在审查环境渲染，图像内容未目检（第 11 节）；② check.py 的 bug 为静态执行顺序分析结论，未做运行时复现；③ 16 条 llm 判分的真实区分度需实测会话数据；④ 外部来源（Wikipedia 指南）未逐条比对；⑤ SKILL.md 中 23 处 em dash 的数量以字符计数程序统计，prose/示例的归类为人工判断。
