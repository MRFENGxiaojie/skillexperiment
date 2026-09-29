# REVIEW: 268-us-market-bubble-detector

**审查日期**: 2026-08-06
**审查人**: Claude (SkillIF quality audit, 深度审查)
**审查方式**: 逐文件全文阅读（共 13 个文件，约 2,900 行），对照 `_shared/SKILL-SPEC.md` 规范与
`_shared/checker.py` 检查库，逐条验证 SCORING.yaml 的 16 项测评标准与技能正文的一致性
**审查对象文件清单**:
- `SKILL.md`（493 行，技能主体）
- `SCORING.yaml`（153 行，测评标准）
- `check.py`（64 行，脚本化检查入口）
- `scripts/bubble_scorer.py`（310 行，评分脚本）
- `references/bubble_framework.md`（337 行，理论框架）
- `references/historical_cases.md`（329 行，历史案例）
- `references/implementation_guide.md`（474 行，实施指南）
- `references/quick_reference.md`（355 行，快速参考，索引标注为日文）
- `references/quick_reference_en.md`（343 行，快速参考英文版）
- `references/reference-documents.md`（33 行，参考文件索引）
- `references/summary-essence-of-v2-1-revision.md`（38 行，v2.1 修订摘要）
- `CHANGELOG.md`（119 行，变更记录）
- `REVIEW.md`（旧版 39 行存根，本次重写）

---

## 一、审查概况与方法

本次审查取代了此前 39 行的存根 REVIEW.md。存根基于 Dossier 标记提出了三个问题——+3/+5 阈值
不一致、双语重复、缺少 Scope 章节——其中第一个问题经本次全文核实属实，且严重程度高于存根判断：
+5 的残留不止一处，而是横跨 SKILL.md 正文、implementation_guide.md 自检清单与报告模板等多个
位置，构成一个系统性的"版本腐烂"问题，其影响范围远超单一文件。与此同时，存根对输出格式的判断
是错的：它声称 Output Format "隐含在评分表中"，但实际上 SKILL.md 第 411 行起存在完整的
"## Output Format" 章节，包含 v2.1 报告模板全文。这一正一反的事实，恰好说明了为什么浅层审查
会误判这个技能——它的主体文本质量并不低，真正的病灶藏在"主干是 v2.1、枝叶仍是 v2.0 甚至
v1.x"的版本断层里。

本次审查逐字通读了全部 13 个文件，并额外核对了评测侧的两份基础设施文件（`_shared/SKILL-SPEC.md`
与 `_shared/checker.py`），目的是验证三个层面的自洽性。第一，SKILL.md 自身内部的逻辑自洽——
阈值、上限、阶段划分在不同章节之间是否互相矛盾；第二，SKILL.md 与六个参考文件、一个脚本之间的
横向自洽——同一概念在不同文件里是否有不同口径；第三，技能文本与 SCORING.yaml 十六项测评标准
之间的纵向自洽——测评所问的问题，技能正文是否真的给出了可执行的答案。审查过程中对每一处阈值
做了边界推演（例如 VIX 13 且距高点 8% 时该得几分），对每一条版本声明做了全文搜索核对（例如
"+5""+3""16""15" 在全部文件中的出现位置），以确保本章每一句判断都有文件内证据支撑。

结论可以概括为一句话：这是一个核心设计出色、但版本治理失败的技能。v2.1 的骨架——强制数据收集、
机械评分、严格定性调整、确认偏误防护、颗粒化风险阶段——是本次审查所见的优秀设计之一，但围绕
这副骨架，至少有五个文件停留在 v2.0 甚至 v1.x 的状态，导致同一个技能内部并存着两套互相矛盾的
评分体系（15 分制与 16 分制）、两套冲突的阈值（3x 与 5x、20 与 +30%）、以及一处连 CLI 参数
都不存在的演示脚本。下文按 13 个章节展开，从定位与合规开始，逐层深入，最后给出评分与修复优先级。

## 二、技能定位、触发条件与描述合规性

frontmatter 的 `name` 为 "us-market-bubble-detector"，小写加连字符、长度合规，与目录名
`268-us-market-bubble-detector` 的 kebab-case 约定一致。description 长度约 470 字符，未超
1024 字符上限，采用第三人称，完整回答了 SKILL-SPEC 要求的三个问题：WHAT（"Evaluates market
bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger
framework v2.1"）、WHEN（"Use when user asks about bubble risk, valuation concerns, or
profit-taking timing"）、KEYWORDS（Put/Call、VIX、margin debt、breadth、IPO 等）。触发短语
明确，无命令式开头、无跨技能路由，frontmatter 也只用了 name 和 description 两个允许字段。
这一项在语料中属于合规标杆，无可挑剔。

但触发设计有一个值得注意的错位：description 与技能名称都锚定 "US market"，而正文第 259-273
行的 "Data Sources" 章节却并列给出了美国市场和日本市场两套数据源，第 313 行的 "Common
Failures" 示例里还出现了 "Takaichi Trade" 这样的日本政治事件（2025 年日本股市的网红股行情）。
也就是说，技能的执行范围实际上被设计为"美股 + 日股"，而触发面与命名只覆盖了美股。一个用户问
"日经是不是泡沫"，按 description 的触发词（bubble risk、valuation、profit-taking）大概率会
命中本技能，但 Phase 1 的数据收集程序只写了美股数据源（CBOE、FINRA、Renaissance），日股路径
在 SKILL.md 正文中没有任何操作化描述——数据源表格里只有链接，没有收集步骤、没有评分阈值适配。
比如日经期货期权 P/C 的正常水平与美股股票 P/C 完全不同，直接套用 <0.70 的阈值在方法上存疑；
JNIVE（日经波动率指数）的历史分布也与 VIX 不同。这是范围声明（Scope）缺失的直接后果，详见
第三章与第十三章的修复清单。

"When to Use This Skill" 章节用英文和日文各写了一遍五个触发场景，内容几乎逐字对应。这一做法在
存根中被点名为"双语维护成本高"，本次审查同意这个判断，但要补充两点。其一，这是本技能唯一的日文
内容，其余所有参考文件都是英文，SKILL-SPEC 也没有要求双语，这五条日文既没有服务任何下游文件，
也没有对应的双语输出格式，属于孤立资产——它在日本用户场景下甚至是有害的，因为用户读到日文触发
条件后会预期日文流程，而实际技能流程全部是英文。其二，reference-documents.md 把 bubble_
framework.md、historical_cases.md、quick_reference.md 三份文件标注为 "(Japanese)"，但实际
阅读后确认这三份文件全部是英文写成——语言标注本身就是错的，详见第九章。技能的语言策略整体上是
"宣称双语、实为英文"，要么补齐日文参考文件，要么删掉孤立日文段落并修正索引标注，两者必居其一。

## 三、总体结构与文件组织

技能目录共 13 个文件：SKILL.md 位于根目录，六个参考文件在 references/ 下，一个脚本在
scripts/ 下，加上 SCORING.yaml、check.py、CHANGELOG.md、REVIEW.md，以及一份专为测评环境
准备的 summary-essence-of-v2-1-revision.md。目录布局符合语料约定，相对路径引用（references/、
scripts/）正确，无跨技能引用，SKILL-SPEC 的文件引用规范合规。CHANGELOG.md 是这份语料中少见
的正式版本管理文件，其结构（问题复盘 → 修订条款 → 影响重算 → 经验教训 → 版本时间线）值得其他
技能效仿，这部分在第八章展开。

SKILL.md 正文 493 行，未超过 600 行硬上限，但已相当接近；对照 SKILL-SPEC 的 pattern 规模表，
"process" 类型的目标体量是约 200 行，493 行超出两倍多。膨胀的主要来源有三处：英文/日文重复的
When-to-Use（约 17 行）、每个指标自带 Rationale 与示例的重复式展开、以及 Output Format 中
嵌入的完整报告模板（约 70 行）。需要指出的是，这个技能的冗长并非纯粹浪费——指标 Rationale 与
无效/有效示例对是技能可用性的关键，模板嵌入也让 agent 可以直接套用。真正值得压缩的是与其他文件
重复的部分（见第十二章），以及四章旧版本残留的声明（见第八章）。

SKILL-SPEC 要求正文必须包含三个必需章节：Workflow/Process、Output Format、Scope/Limitations。
本技能有 "Evaluation Process (Strict Order)"（第 43 行起，四阶段流程完整覆盖）和
"## Output Format"（第 411 行起，完整报告模板），但**没有任何 Scope/Limitations 章节**——
既没有"本技能不做什么"，也没有"何时不应使用"。这是对规范第三项必需章节的明确缺失，同时它正是
第二章所述"美国/日本范围模糊""是否覆盖加密货币、债券、单只个股"等问题的根源。historical_
cases.md 明明详细分析了加密货币泡沫（2017 年案例、100x 杠杆、ICO 泛滥），但技能正文从未声明
自己是否适用于加密资产：适用则需在 Data Sources 中加入加密市场数据源并适配其指标口径，不适用
则需明确排除，现在两者皆无。修复成本很低：加一节 "## Scope and Limitations"，写明适用范围
（美股/日股指数与大盘，不覆盖单票择时）、数据时效前提（见第十一章）、做空建议仅为框架输出而非
独立投资建议等边界声明。

## 四、核心评估流程评审：四阶段设计

v2.1 的流程设计是"Phase 1 数据收集 → Phase 2 量化评分 → Phase 3 定性调整 → Phase 4 最终
判定"的严格顺序四阶段。这个设计的优点在于：它把"先入为主的空头结论"这一金融分析中最常见的偏差，
拆解成了必须按序执行的机械步骤，并在 Phase 3 入口处设置了强制确认偏误清单。相比直接给意见的
通用回答模式，这是一个有真实方法论价值的框架，也解释了为什么 Dossier 会把它归类为复杂技能。
SCORING.yaml 的 SCOPE-02 专门检验"严格阶段顺序"，与正文的 "Evaluation Process (Strict
Order)" 标题一一对应，测评与文本在此处协同良好。

Phase 1 要求强制收集六类数据：P/C 比率（5 日均线）、VIX（当前值 + 3 个月百分位）、21 天已实现
波动率、FINRA 保证金余额（同比）、S&P 500 广度（50 日均线上方占比）、IPO 数量与首日收益中位数，
并明确标注 "Do NOT proceed with evaluation without Phase 1 data collection"。这一强制性与
SCORING.yaml 的 CF-01（无 Phase 1 数据即给出泡沫判定 → 总分清零）完全对应，是技能文本与测评
标准协同最好的部分。数据来源要求（CBOE、Yahoo Finance、FINRA、Barchart、Renaissance Capital）
在 PROC-02 中被逐字复述，agent 只要按正文执行就能通过测评，这种"正文即答案"的一致性值得肯定。

但流程存在一处数据流断裂，需要在本章直接指出：Phase 1 收集的"21 天已实现波动率"和"VIX 过去
3 个月百分位"两项数据，在 Phase 2 的六个量化指标中没有任何一项被使用——指标 2（波动率抑制）
用的是 VIX 绝对水平阈值（<12、12-15、>15）和距 52 周高点距离，与"3 个月百分位"和"21 天已
实现波动率"毫无关系。反过来，指标 6（价格加速度）要求"过去 3 个月收益超过过去 10 年 95 分位"，
这是一个需要十年日频收益序列的分位数计算，而 Phase 1 的收集清单里根本没有价格历史数据这一项。
结果是：收集的数据有三成无用，评分需要的数据又有一项未纳入收集清单。这不影响测评标准的可执行性
（PROC-01 只检查是否发生了 WebSearch），但会直接影响 agent 的实际产出质量——一个严格遵守
Phase 1 清单的 agent，到了指标 6 会发现自己没有评分依据。修复建议是把 Phase 1 的收集清单改为
与六个指标逐一对应：删除或重定位 21 天已实现波动率，加入"近 3 个月与近 10 年收益分位数"的计算
方法与数据来源说明。

Phase 4 的判定矩阵（0-4 Normal / 5-7 Caution / 8-9 Elevated / 10-12 Euphoria / 13-15
Critical）五段连续无重叠，比 v2.0 的四段式更细，"Elevated Risk" 新阶段的定位（保持警惕但不
极端防御、50-70% 风险预算）在 CHANGELOG 里有完整的决策复盘支撑，是 v2.1 最有价值的修订——
v2.0 把 9 分直接判为 Euphoria 意味着 40% 的极端防御仓位，而 v2.1 认识到 8-9 分区间只是警告
信号而非崩塌前兆，仓位管理从"是否离场"细化为"如何渐进降仓"。需要提醒的是风险预算区间的边界
处理：Caution 的 70-80% 与 Elevated 的 50-70% 在 70% 处重叠，Euphoria 的 40-50% 与
Elevated 的 50-70% 在 50% 处重叠，而 Normal 的 100% 与 Caution 的 70-80% 之间、Critical
的 20-30% 与 Euphoria 的 40-50% 之间存在 80-100% 与 30-40% 的空白带。这属于区间设计的
模糊性，在"风险预算"这类本就用于指导性而非精确性的参数上可以接受，但既然技能标榜机械执行，
建议在矩阵下方加一句"区间边界取较低值（保守侧）"的规则，避免 agent 在 70% 或 50% 处产生分歧。

## 五、量化评分体系逐条评审：六指标阈值、边界与空白区间

六个量化指标各 0-2 分，总 12 分，每个指标都有明确阈值与 Rationale，这一设计在同类技能中属于
少见的"真量化"。但逐条推演后发现，六个指标中有四个存在边界重叠或空白区间，属于机械评分落地时
的真实风险点，逐一说明如下。

指标 1（P/C 比率）：<0.70 得 2 分、0.70-0.85 得 1 分、>0.85 得 0 分。边界问题在 0.85 本身
——"0.70-0.85"与">0.85"在 0.85 处重叠，且恰好是 P/C 等于 0.85 时 1 分与 0 分归属不明。
同时该指标的 2 分条件只有单一绝对阈值（<0.70），没有历史分位参照，而 P/C 的市场常态水平会随
期权结构与交易机制变化，一个固定阈值在不同市场环境下可能对应完全不同的情绪状态——这是本指标
可改进的方向，但不属于错误。Rationale 中"P/C < 0.7 是泡沫期的历史特征"的说法与 bubble_
framework.md 第 187 行的警戒线（P/C < 0.5 为极端乐观）存在口径差异，两份文件对同一个指标给出
了 0.5 与 0.7 两个不同参考值，见第九章。

指标 2（VIX + 新高）：VIX<12 且指数距 52 周高点 5% 以内得 2 分、VIX 12-15 且接近高点得
1 分、VIX>15 或距高点 10% 以上得 0 分。这里存在一个真实的空白区间：假设 VIX=13（落在 12-15
区间）但指数距高点 8%（超过 5% 但不到 10%），则 2 分条件不满足（距高点超 5%）、1 分条件不
满足（"接近高点"未定义，若按 5% 理解则 8% 不算接近）、0 分条件也不满足（VIX 未超 15，距高点
未超 10%）——三个分值全部落空，机械执行到此卡壳。修复很简单：把 1 分的 "near highs" 明确为
"距高点 5-10%"，把 0 分的第二条件改为"距高点 10% 以上"，区间即闭合。此外该指标的 1 分条件
只写 "AND near highs" 而未给出数值，是六个指标中表述最含糊的一处。

指标 3（保证金杠杆）：同比 +20% 且创新高得 2 分、+10-20% 得 1 分、+10% 以下或负值得 0 分。
同样存在空白：同比 +25% 但未创新高时，2 分条件不满足（缺创新高）、1 分条件不满足（超 20%）、
0 分条件也不满足（未小于 +10%）——"高增速但未创新高"这种在真实市场很常见的情形没有任何分值
归属。最可能的本意是"同比 +20% 以上但未创新高 → 1 分"，但文本未写。顺带指出，FINRA 保证金
数据是月度发布且滞后约三周，指标 3 的数据新鲜度天然受限，这在第十一章展开。

指标 4（IPO 过热）：季度 IPO 数超 5 年均值 2 倍且首日收益中位数 +20% 以上得 2 分、超 1.5 倍
得 1 分、正常水平得 0 分。这个指标逻辑自洽：超过 2 倍但首日收益不达标的，回落到 1 分条件
（超 1.5 倍）仍有归属，没有空白区间。唯一的小问题是"正常水平"没有数值定义，且"首日收益中位数"
在部分市场（如日股）的数据可得性差，见第十一章。

指标 5（广度异常）：创新高且 50 日均线上方占比 <45% 得 2 分、45-60% 得 1 分、>60% 得 0 分。
边界在 45% 与 60% 两点重叠，与指标 1 同类，属于文字表述精度问题，加 "≥""≤" 即可闭合。这个
指标的设计逻辑（"少数股票推动的创新高是脆弱行情"）与 bubble_framework.md 的广度理论一致，
是六指标中概念与操作最贴合的一个。

指标 6（价格加速度）：3 个月收益超 10 年 95 分位得 2 分、85-95 分位得 1 分、85 分位以下得
0 分。边界在 85 与 95 两点重叠，且如前所述，该指标所需的十年收益分布数据不在 Phase 1 收集
清单内，是六指标中落地阻力最大的一个——agent 在无价格数据库的情况下，仅靠 web_search 很难
可靠取得十年 3 个月滚动收益的 95 分位值。建议在 Phase 1 中为指标 6 单独写明数据来源（如历史
指数收盘序列的公开来源）与计算口径（滚动窗口、年化方式）。

总体评价：阈值体系的设计意图（越接近历史极值越高分）方向正确，六个指标覆盖了情绪、波动、杠杆、
发行、广度、动量六个维度，覆盖面优于绝大多数同类技能；但"机械执行"的承诺需要闭环的区间定义来
兑现，目前四个指标在边界处的模糊会迫使 agent 现场发挥，而这恰好违背了 v2.1 打击主观性的初衷。
修复成本不高（全部是表述闭合问题），收益却直接体现在测评稳定性上。

## 六、定性调整与确认偏误防护评审

Phase 3 是 v2.1 修订的核心战场，其设计质量值得单独成章。三个调整项（社会渗透、媒体/搜索趋势、
估值脱钩）各 0-1 分、合计上限 +3 分，相比 v2.0 的 +5 大幅收紧；每项都要求"全部条件满足才给分"
的严格合取逻辑，并配有有效/无效示例对。特别是 Adjustment A 的无效示例（"AI narrative is
prevalent"）与有效示例（理发师、牙医、Uber 司机带日期的人名级证据）对比，把"可直接观察、可独立
核验"的证据标准讲得很清楚；Adjustment B 给出的验证三步法（搜索 Google Trends 数字、Time 封面
日期、CNBC 特辑期数）也可操作。CHANGELOG 里记录的 2025-11-03 真实复盘（v2.0 下 11/16 分
Euphoria、40% 风险预算的过度防御，v2.1 下 9/15 分 Elevated、50-70% 风险预算的平衡判断）是
这个技能最珍贵的资产——它用一次真实的确认偏误事故解释了每条修订条款的由来，这种"案例驱动的修订
文档"在其他技能中极为罕见。summary-essence-of-v2-1-revision.md 把这次复盘压缩成 38 行，
作为测评者快速入门材料是称职的。

但有三处与 v2.1 精神相抵触的残留需要指出。其一，Adjustment C 的 "P/E >25 (if NOT already
counted in Phase 2 quantitative)" 条件在 v2.1 体系下永远不可能触发——六个量化指标中根本没有
P/E 或估值项，"已在 Phase 2 计分"是 v1.x 八指标体系（其中包含 Valuation Disconnect 指标）的
遗留逻辑。这个条件子句的存在本身无害，但它暴露了 Adjustment C 的评分标准实际依赖的是一套不存在
的参照系，应当改写为"P/E 不属于 Phase 2 计分项，无需检查重复计分，但需检查叙事依赖"。其二，
SKILL.md 第 320 行 "Common Failures and Solutions" 的 Failure 4 示例写着 "❌ P/E 17 →
Valuation disconnect 2 points"，而 v2.1 的估值调整只有 0-1 分且要求 P/E>25——这个 2 分示例是
旧体系的直接残留，且 P/E 17 在 v2.1 任何口径下都不该得分，示例与现行规则完全脱节。其三，
Adjustment B 的有效示例存在数据机制问题：Google Trends 输出的是 0-100 的相对搜索指数，示例中
"AI stocks 780、baseline 150、5.2x"的绝对数值不符合该产品的实际输出机制，正确的做法应是同窗口、
同比较基准下的相对倍率（例如"当前 100 vs 去年同期 19"）。推理方向对、示例数字不现实，这会让
agent 在核验时产生困惑。

确认偏误防护清单（四条自问：有无可测数据、独立观察者是否同意、是否与 Phase 2 重复计分、是否记录
了带来源的证据）在 SKILL.md、implementation_guide.md、SCORING.yaml 的 PROC-07 三处出现且
内容一致，并在 NEG-01 与 CF-02、CF-03 中得到测评侧强制背书——这是"技能文本 — 参考文件 — 测评
标准"三者协同的正面样板。CF-03 专门惩罚"Phase 2 与 Phase 3 之间估值重复计分导致泡沫分虚高"，
与 Adjustment C 的自查问题（"Is P/E already in Phase 2 quantitative scoring?"）相互呼应。
总体而言，Phase 3 的设计思想是本次审查所见最优秀的定性控制机制之一，扣分项全部来自版本残留与
示例失真，而非设计本身。

## 七、输出格式与行动建议评审

这里需要先纠正存根 REVIEW.md 的一个事实错误：存根声称 Output Format "隐含在评分表中"，但
SKILL.md 第 411 行起存在完整的 "## Output Format" 章节，给出了 v2.1 报告模板的全文——总体
评估块（分数、阶段、风险等级、日期）、Phase 2 六指标表格（实测值/得分/理由）、Phase 3 逐项
证据与自检、按阶段对应的行动建议、做空评估（X/7 综合条件），以及 v2.1 关键变化摘要。模板与
四阶段流程一一对应，结构完整，是满足 SKILL-SPEC 输出格式要求的合格实现。此前 39 行存根在这个
问题上的误判，是本次深度审查重写 REVIEW.md 的直接动机之一——如果一个技能仅凭 39 行的浅层阅读
就被判"缺少输出格式"，那么存根式审查对复杂技能的伤害可想而知。

模板的几个细节值得肯定：Phase 2 表格要求 "Measured Value" 列，把"数据驱动"落到了格式层面；
Phase 3 每项要求 "Evidence" 字段并内置确认偏误勾选；做空部分要求明确写出 "Composite
conditions: X/7 met" 与当前阶段的最低门槛（0/2/3/5），与 SCORING.yaml 的 OUT-03 逐字对应。
这些设计让"机械性"不只停留在原则层面，而是嵌入了产出物的结构。输出中的"风险等级"五档映射
（Low/Medium/Medium-High/High/Extremely High）与五阶段一一对应，也与 bubble_scorer.py 的
四档风险等级（Low/Medium/High/Extremely High）形成对照——脚本没有 Medium-High 档，再次印证
脚本与正文的脱节（见第十章）。

同样需要指出的问题是模板与正文的两处不一致。第一，模板整体评估块写 "Final Score: X/15 points
(v2.1: max reduced from 16)"，把版本历史塞进了用户可交付物——对最终用户而言 16 这个数字毫无
意义，建议只保留 "X/15"，把版本说明放进 CHANGELOG。第二，模板中 "Phase 3 Total: +X/3 points"
与正文 Implementation Checklist 的 "+5 point limit" 直接矛盾——agent 若按正文清单自检，会用
一个 v2.0 的约束去核对自己的 v2.1 产出（详见第八章）。行动建议矩阵（按阶段给出止盈比例、ATR
系数、仓位纪律、做空门槛）内容扎实：从 Normal 的 ATR 2.0x、Caution 的 1.8x、Elevated 的
1.6x、Euphoria 的 1.5x 到 Critical 的 1.2x，各阶段做空仓位规模（10-15%、20-25%、分批建仓）
都有具体数字，与 quick_reference.md 的动作矩阵和 bubble_framework.md 的风险预算表相互印证，
是技能内跨文件一致性最好的部分。但做空综合条件存在跨文件的数量分歧：SKILL.md 与两个 quick_
reference 是 7 条，bubble_framework.md 第 286-293 行只列了 5 条且建议"至少 3 条满足即考虑
做空"，与 SKILL.md 的分阶段门槛（Elevated 2/7、Euphoria 3/7、Critical 5/7）无法对应；另外
第 6 条条件 "VIX surges" 在 SKILL.md 写作 "spike above 20"、在 quick_reference 写作
"+30%+"，同一条件两种量化口径。这些需要在统一文档修订中一并闭合。此外，做空门槛与阶段分档的
对应关系（0/2/3/5）在 SKILL.md 中散落在 "Recommended Actions by Bubble Stage" 各段里，没有
汇总表，建议在 Output Format 模板附近补一张对照行，降低 agent 拼装时的出错概率。

## 八、版本一致性审计：v2.1 声明的实际落实情况

本章是本次审查的核心章节。v2.1 在 2025-11-03 发布，核心变更三条：定性调整上限 +5 → +3、
新增 8-9 分 Elevated Risk 阶段、总分上限 16 → 15。对全部 13 个文件逐一核对后，版本一致性状态
如下：SKILL.md 主干、SCORING.yaml、CHANGELOG.md、summary-essence-of-v2-1-revision.md 四个
文件基本落实 v2.1；bubble_framework.md 的风险预算表与动作矩阵已更新但保留了八指标清单；
implementation_guide.md、quick_reference_en.md 停留在 v2.0；quick_reference.md 的动作矩阵
已更新但八指标速评分仍为 v1.x；historical_cases.md 的案例评分与 bubble_scorer.py 整个脚本
停留在 v1.x 的 16 分制。具体证据逐条列出如下。

第一处也是最严重的一处，就在 SKILL.md 自身内部。第 285 行 Implementation Checklist 写作
"Did you keep qualitative evaluation within +5 point limit?"，第 301-302 行 Important
Principles 第 3 条写作 "Qualitative adjustment has a total limit of +5 points"，而同一文件
第 17 行、第 154 行、第 232 行、第 465 行四处都明确写着 +3。存根 Dossier 标记的"+3/+5 不
一致"经核实为真，且不是笔误而是结构性残留——两处 +5 都位于"原则/自检"性质的章节，属于 agent
最容易直接照抄执行的位置。更要命的是，SCORING.yaml 的 PROC-06 与 NEG-01 明确按 +3 上限评判、
CF-02 规定超限即总分清零：一个老老实实按 SKILL.md 自检清单执行 +5 的 agent，会被测评体系判定
为严重违规。技能文本亲手教出了测评要惩罚的行为，这是本次审查认定的第一优先修复项。修复后还应
全文搜索 "+5""+3""16""15" 等关键词做一遍回归核对，并把这一核对动作写入 CHANGELOG 的后续
修订流程。

第二处是 quick_reference_en.md 整体停留在 v2.0。其动作矩阵（第 45-53 行）仍是 Caution 5-8 /
Euphoria 9-12 / Critical 13-16，风险预算 70%/40%/20%，无 Elevated Risk 阶段，满分 16——与
v2.1 的 5-7/8-9/10-12/13-15、70-80%/50-70%/40-50%/20-30%、满分 15 全面冲突。有趣的是，
同为快速参考的 quick_reference.md 动作矩阵已更新到 v2.1（含 Elevated Risk、注明 "Maximum
score reduced from 16 to 15"），两份姊妹文件一旧一新，说明 v2.1 发布时漏改了英文版。而英文版
恰恰是最可能被 agent 在英语会话中加载的文件——后果是同一技能同一问题，中英两种语言路径会产出
不同分数体系下的判定。这是第二优先修复项。

第三处是双评分体系并存。v1.x 的"八指标 Bubble-O-Meter"（大众渗透、媒体饱和、新入市者、发行潮、
杠杆、价格加速、估值脱钩、广度相关，各 0-2 分，总分 16）完整保留在 bubble_scorer.py 的全部
逻辑、historical_cases.md 的三个案例评分（2000 年 3 月 15/16、2017 年 12 月 16/16、2021 年
11 月 14/16）、quick_reference 两个版本的八指标速评分章节，以及 bubble_framework.md 每日清单
的 "Update Bubble-O-Meter (score 8 indicators)" 中。这套体系与 v2.1 的"六量化 + 三定性"完全
异构：指标集不同（八指标含"新入市者""估值脱钩"两个 v2.1 六指标里没有的项）、满分不同（16 vs
15）、阶段切分不同（无 Elevated）。CHANGELOG 明确写着 "v1.x: Original framework
(deprecated)"，但被弃用的框架在五个文件中仍然存活。历史案例的 15/16、16/16 分数在新体系下
无法复现——比如 2000 年 3 月的估值脱钩 2 分，在 v2.1 里估值调整最多 1 分且要求 P/E>25，评分
路径完全不同。这不是"参考文档未同步"的轻度问题，而是同一个技能目录里并存两套可操作的方法论，
agent 装载不同文件就会走向不同流程。

第四处是 implementation_guide.md 的版本混装。该文件标题为 "Revised v2.0"，但 Step 5 的标题
写着 "Upper limit +3 points, STRICT CRITERIA"（v2.1 的措辞），Step 6 的示例报告写 "Final
Score: 0/16 points"（v1.x/v2.0 口径），报告模板写 "X/16 points"，文末自检清单写 "Did you
keep qualitative adjustment within +5 point limit?" 与 "Total ≤ 5 points?"（v2.0 口径），而
NG 示例 1 中 Google Trends 的判定线写的是 "below 3x"（v2.1 是 5x）。同一份"首次使用推荐装载"
的实施指南里，v2.0 与 v2.1 交错出现，且 3x 这个阈值在整个语料中仅此一处。这份文件被 reference-
documents.md 标注为 "RECOMMENDED FOR FIRST USE"，是 agent 首次执行时最可能依赖的文档——
它的版本混乱会直接传导为 agent 产出的混乱。

综上，版本一致性维度在本审查的八个维度中得分最低。根因是 v2.1 修订只更新了"主干文件"（SKILL.md、
SCORING、CHANGELOG）而未建立"参考文件必须同步修订"的纪律，且目录中缺少一份版本对照表（如
"八指标速评分已弃用，以 SKILL.md 六指标 + 三调整为准；各参考文件版本状态见下表"）。修复路径
建议：将 quick_reference_en.md 的动作矩阵与阈值对齐 v2.1；在 implementation_guide.md 与
historical_cases.md 中增加 v2.1 迁移说明或直接更新案例评分；对 bubble_scorer.py 做 v2.1 化
改造或标注弃用（详见第十章）；在 reference-documents.md 中加入版本状态列。值得注意的是，
CHANGELOG.md 的"Documentation Updates"段落声称 SKILL.md、implementation_guide.md、
quick_reference.md、bubble_framework.md 四个文件已更新到 v2.1——对 implementation_guide.md
而言这个声明与文件实际内容不符，说明变更记录本身也没有被核对过。

## 九、参考文件体系逐文件评审

六个参考文件按内容可分为三层：理论层（bubble_framework.md）、案例层（historical_cases.md）、
操作层（implementation_guide.md、quick_reference.md、quick_reference_en.md），外加索引
（reference-documents.md）与修订摘要（summary-essence-of-v2-1-revision.md）。层级设计合理，
操作层内部有"首用装指南、日常装速查"的装载指引，这是加分项。

bubble_framework.md 的学术内容是六份参考文件中质量最高的：Minsky/Kindleberger 五阶段模型
（位移、繁荣、狂热、获利、恐慌）配真实年份例证；行为心理学四要素（FOMO、确认偏误、过度自信、
损失厌恶 × 遗憾厌恶的危险组合）解释到位，特别是"止盈后快速上涨 → 遗憾 → 高位重进 → 亏损不止损
→ 上涨强化错觉 → 错过反转离场"的链路推演，把四个心理机制串成了一个完整的故事；"出租车司机信号"
作为信息瀑布完成度的代理指标有清晰的理论链条；文末六条 Golden Rules（"See process, not
price"、"When taxi drivers talk stocks, exit"）有格言质感。扣分点有三。其一，第 172-213 行
的五类检测指标阈值表与 SKILL.md 的评分阈值存在系统性出入——例如 P/C 的警戒线此处写 <0.5、
SKILL.md 写 <0.70，IPO 此处写同比 +100%、SKILL.md 写超 5 年均值 2 倍，新开户此处写 +200%
而六指标体系根本不含开户数据——理论文档的"检测阈值"与操作文档的"评分阈值"两套数字并存，agent
引用时会拿到不同的警戒水平。其二，做空条件此处只有 5 条（见第七章）。其三，每日清单仍引用已弃用
的八指标 Bubble-O-Meter。第二层的 historical_cases.md 是三份案例（科网、加密、疫情）中事实
细节最扎实的：IPO 首日 +70%、Bitcoin 从 3k 到 19.8k 的逐级价格、GME/SPAC/NFT 的复合泡沫，
时间线可查证；"阶段化社会渗透"模式（专家 → 白领 → 出租车司机，第三阶段后仅剩 1-3 个月）与
"政策转向即触发器"模式的归纳有实战价值；文末比特币案例的三种应对情景（完美择时幻觉 vs 阶梯止盈
vs ATR 追踪止损）用 $1,000 本金做了可复现的算术演示，Scenario B 的 $8,250 与 Scenario C 的
$16,550 对比直观说明"次优但可执行"优于"最优但不可达"。它的问题只在评分口径（16 分制）与 v2.1
脱节，以及"杠杆 1 分"等主观评分的依据未交代——比如 2021 年保证金余额实际处于历史高位，案例却
只给 1 分，理由 "not excessive mortgage levels" 略显牵强。

操作层三份文件的问题在第八章已述，此处补充两点正面结论：implementation_guide.md 的"NG 示例
vs OK 示例"对照（"Many Takaichi Trade reports → 媒体饱和 2 分"的错误路径 vs 搜索后 1.8x →
0 分的正确路径）和"红旗下重做"清单（P/C>1.0 却得分 10+、无来源无日期等八条红旗）是很好的执行
防错机制，四级质量评判（Failed/Pass/Good/Excellent）把自评落到了可操作层面；quick_reference.md
的三问应急评估（非投资者在推荐吗、叙事成为常识了吗、"这次不一样"成为口头禅了吗）是优秀的低延迟
筛选工具，All-3-YES → Critical 的口诀与 historical_cases 的"当怀疑有社会成本时就是尾声"呼应。
reference-documents.md 的问题已在第二章点明：三处 "(Japanese)" 标注全部错误，且它完全没提
scripts/bubble_scorer.py——作为索引文件，既标错了语言，又漏掉了目录里最大的一个文件；它把
implementation_guide.md 标注为 "RECOMMENDED FOR FIRST USE" 的决策本身没问题，但推荐装载的
恰恰是版本最混乱的文件，见第八章。summary-essence-of-v2-1-revision.md 内容与 CHANGELOG
高度重合，但作为给测评者快速入门的 38 行摘要，存在价值可以接受。

## 十、脚本与自动检查评审

scripts/bubble_scorer.py 是本次审查发现的问题最集中的文件，需要逐条说明。第一，它与 v2.1 的
整体设计完全脱节：docstring 与 calculate_score 中的阶段映射是 0-4 Normal / 5-8 Caution /
9-12 Euphoria / 13-16 Critical 的 16 分制，没有 Elevated Risk 阶段，风险预算沿用旧口径
（如 Euphoria 推荐语中的 "reduce total risk budget by 30-50%"），八指标集（mass_
penetration、media_saturation、new_accounts、new_issuance、leverage、price_acceleration、
valuation_disconnect、breadth_expansion）是已弃用的 v1.x 体系。也就是说，脚本输出的任何分数
都无法映射到 SKILL.md 的 Phase 2/3/4 判定——脚本给出的 "9 分 Euphoria" 在 SKILL.md 里是
"Elevated Risk"。第二，脚本没有任何数据收集能力——它只接受手工输入的分数或 JSON，与 v2.1 的
"强制数据收集"原则无关，甚至没有任何关于数据来源的提示，运行脚本本身就构成一种"凭印象打分"的
诱惑；manual_assessment 模式的交互提示会直接把用户引向凭感觉打分。第三，docstring 宣称的用法
"python bubble_scorer.py --ticker SPY --period 1y" 在实际 CLI 中不存在——argparse 只定义了
--manual、--scores、--output 三个参数，按 docstring 运行会直接报 unrecognized arguments，
这是文档与实现不符的确定性 bug。第四，SKILL.md 与 reference-documents.md 均未引用该脚本，它
是个既矛盾又孤立的文件。处理建议二选一：要么将其改造为 v2.1 的 6+3 计算器并接入 Phase 4 判定
（六量化 + 三调整输入、15 分上限、五阶段映射、做空门槛输出），要么在 docstring 顶部标注
DEPRECATED 并从目录移除或移入 archive——在当前状态下，任何 agent 或用户运行它都会得到与技能
主体矛盾的结论。此外，脚本中 indicators 字典的 weight 字段恒为 2，实际是冗余参数；_estimate_
minsky_phase 的四段映射与 SKILL.md 的五阶段 Minsky 模型也不完全对应（Profit Taking 阶段在
脚本映射中与 Peak Euphoria 合并），说明脚本演进停在旧版。

check.py 与 checker.py 的配合基本正常：check.py 通过 sys.path 注入加载 _shared/checker.py，
调用 tool_log_contains('WebSearch|web_search') 检查工具日志中是否出现 WebSearch 调用，正则
同时覆盖了工具名大小写两种形态，思路正确。但存在两个问题。其一，check.py 中 set_agent_output
的调用顺序有隐患：main() 先读取 agent_output 文件内容并 set_agent_output(内容)，随后 check()
内部又调用 set_agent_output(agent_output) 把全局值覆盖成文件路径字符串——由于当前 check.py
只使用 tool_log_contains、不使用 output_contains，这个覆盖不产生实际影响，但任何未来新增的
output 类检查都会因此拿到路径字符串而非内容，属于潜伏 bug，应在 check() 内删除该行或改为仅在
需要时传入内容。其二，SCORING.yaml 的 16 项标准中 15 项为 LLM 判定、仅 PROC-01 一项脚本判定，
且 PROC-01 只验证"工具日志中出现过至少一次 WebSearch"，无法验证"Phase 1 的六项数据是否在评估
前收集、是否每项都有来源与日期"。这是测评设计对"数据收集"承诺的弱化——CF-01 的强制力理论上很
强，但实际触发它需要的只是"发生过搜索"这一个布尔值。考虑到 LLM 判定是语料的标准做法，此项不作
为缺陷处理，但值得记录其局限。SCORING.yaml 本身的质量是测评侧亮点：16 项标准与 SKILL.md 的
流程逐条对应（数量核对：2 scope + 9 process + 3 output + 1 negative + 1 qa = 16，与
total_items: 16 一致），PROC-03 把六个阈值完整嵌入提问文本，PROC-08 将三个定性调整的合取条件
逐字复述，CF-01/02/03 的 cap_to_0 威慑设计得当，OUT-01 覆盖了含 Elevated Risk 的完整五段映射，
QA-01 要求展示自检清单结果——整套标准比多数技能更贴合正文。唯一的刺是它比 SKILL.md 的正文更
"v2.1"：测评按 +3 判，正文还留着 +5，这在第八章已述，且会直接影响本技能的实测得分。

## 十一、数据源与实操可行性评审

技能承诺"强制数据收集、机械评分"，那么数据可得性与时效就是它的生命线。逐项核对后，可行性评价
是"方向对、细节糙"。P/C 比率与 VIX 可以即时取得（CBOE/Yahoo，网络搜索可达），广度数据
（Barchart）与 IPO 数据（Renaissance Capital）也可得，这四项没问题。但有三处现实障碍。第一，
FINRA 保证金余额是月度统计且官方发布滞后约三周——implementation_guide.md 第 82 行却要求
"Data is recent (within 1 week)"，对保证金这一项这是不可能达成的标准；同一个文件第 72 行示例
却给了 "Margin YoY +8% | FINRA | 2025-09" 这种明显超期的数据且未作任何说明。要么把时效规则
改为"按数据源实际发布周期"，要么给保证金数据单独标注滞后容忍度。第二，指标 6 的十年分位数计算
需要历史收益序列，SKILL.md 未给出任何数据来源；Renaissance 的 IPO 季度数据同样有自然滞后，
"收集：季度数量 + 首日收益中位数"在实际中经常要引用上一季度的数据。第三，Adjustment B 的
Google Trends 核验路径在真实 agent 环境中只有 web_search 可用，而 Google Trends 的绝对数值
（示例中的 780/150）不符合其 0-100 相对指数机制，agent 很可能搜不到与示例格式一致的数据。
建议为三个调整项各补充"搜索失败时的降级规则"（例如"无法取得 Trends 数值 → 该调整记 0 分"），
把数据不可得的情形显式纳入流程——目前 SKILL.md 只说了 "Do NOT proceed without Phase 1
data"，没说"部分数据不可得时怎么办"，这会让 agent 在真实执行时要么卡住要么放弃流程。另外，
Phase 1 提到的 "CBOE DataShop" 需要账号与 API 权限，普通网络搜索无法访问，应改为 CBOE 公开
页面或直接说明该来源为可选。最后，Phase 1 要求收集"VIX 过去 3 个月百分位"但 Phase 2 不用百分位
（用绝对阈值），本章与第四章、第五章的观察一致指向同一个修复方向：让收集清单、评分指标、数据
可得性三者闭环对齐。

## 十二、重复与冗余分析

这个技能存在两层冗余。第一层是 SKILL.md 内部的，已在第二章与第三章提及：When-to-Use 的英日
双写（17 行）、v2.1 变更声明的四次重复（第 9-17 行的 Key Revisions、第 250-254 行的 Key
Change、第 363-366 行的 Rationale 段落、第 480-484 行模板内的 Key Changes 共出现四次）、
以及 Common Failures 章节与 quick_reference 的 Failure 章节内容高度重叠。第二层是跨文件的：
Golden Rules 十条在 bubble_framework.md、quick_reference.md、quick_reference_en.md 三处各
出现一次（合计约 30 行）；阶梯止盈模板（$10,000 起始、+20% 卖 25% 的算术）出现三次；ATR 追踪
止损的 Python 函数在两份 quick_reference 中各出现一次（同一函数、同一注释，仅缩进风格不同）；
确认偏误清单出现三次（SKILL.md、implementation_guide.md、SCORING PROC-07——测评侧重复是
合理的，因为测评标准需要自含）；做空 7 条件清单出现三次；"Market can remain irrational
longer than you can remain solvent" 格言出现四次。合计保守估计，冗余内容超过 250 行，占全
语料近一成。冗余的代价不只是 token 消耗：三份文件各写一遍的同一内容，在版本迭代时必然出现只有
一份被更新的局面——第八章的所有版本问题，本质上都是重复维护的必然结果。修复建议是确立"单一
事实来源"原则：SKILL.md 保留流程与阈值（它是唯一被测评直接引用、必须自含的文件）；Golden
Rules 归入 bubble_framework.md；动作矩阵归入 quick_reference.md（quick_reference_en.md
改为同步更新或仅保留链接与差异说明）；报告模板归入 implementation_guide.md；其他文件以引用
代替复制。在修复完成前，任何对阈值的修改都必须做全文 grep 核对——本次审查对每一处"+5/+3/
16/15/3x/5x"的核对即是这一原则的示范。

## 十三、综合评分、修复优先级与结论

综合八个维度的评价，最终评分为 **60/100（🟡 C）**。维度分项如下：触发条件与描述质量 8/10
（描述合规、触发明确，但范围声明缺失与日股路径未操作化牵连此项）；核心评估流程设计 15/20
（四阶段结构优秀、数据流断裂与阈值空白扣分）；量化评分阈值设计 10/15（六指标覆盖好、四指标
边界缺陷）；定性调整与确认偏误防护 8/10（设计一流、两处旧体系残留与示例数字失真）；输出格式
与行动建议 7/10（模板完整、做空条件跨文件不一致）；版本一致性 3/15（五处文件版本错位，SKILL.md
自身 +5/+3 并存）；参考文件体系 5/10（内容质量高、语言标注错误与阈值体系出入）；脚本与测评配套
4/10（SCORING 出色、脚本整体失配且含 CLI 文档 bug）。相比存根的 46 分，本次评分上调主要因为：
存根误判了 Output Format 的存在，且未读到正文之外的 12 个文件——它看到的"草率"有一半是"只
看了主干"造成的，而真正的病灶（版本腐烂）比存根描写的更广，但病灶的可修复性也更高。

按修复优先级排列，需要做的事依次是：第一优先级（高影响、低成本），修复 SKILL.md 第 285 行与
第 301-302 行的两处 +5 残留，全文 grep 核对 "+5/+3/16/15" 一致性，因为 SCORING.yaml 会按
+3 惩罚照章执行 +5 的 agent；第二优先级，将 quick_reference_en.md 的动作矩阵与阈值对齐 v2.1
（或删除该文件改为单一英文速查）；第三优先级，处理 bubble_scorer.py 的失配——改造为 v2.1 六
指标计算器或标注 DEPRECATED；第四优先级，重写 implementation_guide.md 的版本（标题、模板、
自检清单、3x 阈值）并补充指标 6 的数据来源与"数据不可得降级规则"；第五优先级，修正 reference-
documents.md 的三处日文标注、补上脚本条目，并新增 Scope/Limitations 章节；第六优先级，统一
做空条件的数量与 VIX 阈值（7 条 vs 5 条、"spike above 20" vs "+30%"）、闭合四个量化指标的
边界区间、删除 Adjustment C 的不可触发条件、修正 Google Trends 示例的数值机制、修正 check.py
的 set_agent_output 覆盖顺序。

最终结论：这个技能的"内胆"值得保留——机械评分、严格定性、偏误防护、颗粒化阶段的设计在语料中
属于第一梯队，CHANGELOG 的案例驱动修订方式更是值得其他技能效仿的范例；它的"外壳"需要一次系统
性的版本治理。如果上述六项优先级全部落地，本技能有望进入 A- 区间。在修复完成前，测评时需要
注意一个现实风险：由于 SKILL.md 自检清单残留 +5，agent 遵循正文的行为可能被 SCORING.yaml 的
CF-02 判定为违规——这会让本技能的实测分数系统性低估，建议在修复版本一致性之前，对 PROC-06/
NEG-01/CF-02 的判定结果标注"受文本版本残留干扰"。这一观察也再次印证了本次审查的核心方法论：
对复杂技能的审查必须全文通读、交叉核对，任何"看主干即下结论"的做法，无论结论是褒是贬，都可能
与文件的实际状态相去甚远。

---

**变更记录**
- 2026-08-06: 深度审查（全文 13 文件 + 2 份基础设施文件），取代 2026-08-05 的 39 行存根审查。
  存根三问的核实结论：+3/+5 不一致属实且为多处系统性残留（SKILL.md 第 285、301-302 行）；
  双语重复属实但非主要冗余来源（跨文件重复约 250 行更严重）；Scope 缺失属实（SKILL-SPEC 三项
  必需章节缺一项）。存根关于 Output Format 缺失的判断经核实为误判（SKILL.md 第 411 行起存在
  完整模板）。
