# REVIEW: 194-radar-vital-signs

**审查日期**: 2026-08-06
**Skill 类型**: process — 雷达生命体征提取管道（I/Q 解析 → Range FFT → 相位解缠 → 滤波 → PSD → 谐波抑制 → 交叉验证）
**Body 行数**: 114 行 | **参考文件数**: references/5, scripts/0, 其他/0
**SCORING pattern**: process | **SCORING total_items**: 20 | **check.py 脚本检查数**: 13（SCOPE-01, PROC-01~09, PROC-11, OUT-01, QA-01）

---

## 1. 目录全量清单

```
194-radar-vital-signs/
├── SKILL.md                   114 行  ← 正文（10 步管道 + 规则/决策/自检）
├── SCORING.yaml               179 行  ← 20 个测评点 + 2 个 critical failure
├── check.py                    82 行  ← 13 项脚本检查，其余 7 项为 llm judge
└── references/
    ├── band-rationale.md       55 行  ← 频带边界理由（0.08/0.7/3.0 的临床依据）
    ├── debugging.md            75 行  ← 8 步排错清单
    ├── harmonic-pitfalls.md    67 行  ← HR 二次谐波 + 呼吸谐波泄漏两大陷阱
    ├── iq-formats.md           42 行  ← I/Q 二进制布局与解析代码
    └── range-bin.md            40 行  ← FMCW 距离门选择启发式
```

- **目录总数**: 8 个文件（3 核心 + 5 参考）；scripts/ 0、其他子目录 0。
- **结构评述**: 本批三个 skill 中**唯一携带 references/ 的**，且 5 个参考文件全部被正文显式引用（引用矩阵见 §5.1）——参考体系完整，无死文件。正文 114 行非常精炼（三个 skill 中最短），把深度知识放在 references 是正确的外置策略。
- **行数对比**: SKILL.md 114 行 + references 279 行 = 393 行总知识量，与 197（240 行全内联）体量相近但组织方式更优；check.py 承载 13 项脚本检查（三个 skill 中最多），正文-脚本的映射关系需要逐条核对（§10.1）。

---

## 2. Frontmatter 逐字段审查

### 2.1 name
- 值: `radar-vital-signs`。
- **格式**: 全小写 + 连字符 ✅；与目录名 `194-radar-vital-signs`（NNN-kebab-case）剥离编号后一致 ✅；长度 16 字符 ≤ 64 ✅。
- **结论**: ✅ 通过。

### 2.2 description
原文:
> End-to-end pipeline for extracting heart rate (HR) and breathing rate (BR) from raw short-range radar I/Q captures — both continuous-wave (CW, 24 GHz clinical boards) and FMCW mmWave (60/77 GHz, TI IWR/AWR). Use when Claude needs to parse interleaved I/Q binary, do a Range FFT on FMCW chirps, remove static clutter, pick a subject range bin, extract phase with unwrapping, design HR/BR bandpass filters, pick a peak frequency via PSD, reject the HR second harmonic that often dominates the fundamental, or handle respiration-harmonic leakage on slow breathers. Not for pulse/UWB range gating, MIMO beamforming, Doppler-only gesture radar, arrhythmia detection, or multi-subject source separation.

- **WHAT**: "End-to-end pipeline for extracting heart rate (HR) and breathing rate (BR) from raw short-range radar I/Q captures"——动作 + 输入形态 + 输出定义齐备；技术范围（CW 24 GHz / FMCW 60/77 GHz TI IWR/AWR）精确。
- **WHEN / 触发信号**: "Use when Claude needs to parse interleaved I/Q binary, do a Range FFT…"——触发短语 + **10 个动词短语关键词**（parse/FFT/clutter/range bin/unwrap/bandpass/PSD/harmonic/leakage），覆盖正文管道的每一步动作，触发面极广且具体 ✅。
- **人称**: 全第三人称（"Claude needs to"）✅，无 you/I/we。
- **负面范围**: "Not for pulse/UWB range gating, MIMO beamforming, Doppler-only gesture radar, arrhythmia detection, or multi-subject source separation."——description 自带排除清单（5 类），与正文 `## Not in scope`（6 条）呼应。**这是本批三个 skill 中唯一在 description 就写明负边界的**，触发精度极高 ✅。
- **长度**: 约 640 字符 < 1024 ✅。
- **跨 skill 路由**: 无 ✅。
- **结论**: ✅ **通过，且为全库 description 最佳实践样板**（WHAT/WHEN/负面清单三段式）。

### 2.3 allowed-tools
- **字段不存在**。
- **必要性分析**: 该 skill 的输出是 numpy/scipy 代码（QA-01 要求 `import numpy|from scipy`），执行代码需要 Bash/Python 环境；正文未要求任何特殊工具，默认工具集（Read/Bash）即可满足。allowed-tools 非必需，**不声明不构成问题** ✅。
- 唯一依赖: 读取 sidecar（JSON/YAML）用 Read 工具 + 文件解析（fromfile）用 Python——均在默认集内 ✅。

### 2.4 其他字段
- 无 argument-hint（本 skill 输入是文件/数据路径，由用户消息给出，不需要 hint）✅。
- 无 user-invocable、model、paths、disable-model-invocation；无禁止字段 ✅。

### 2.5 YAML语法
- frontmatter 为单行长 plain scalar，无内嵌引号/冒号歧义（"60/77 GHz" 中的斜杠与逗号在 plain scalar 中合法）✅。YAML 解析正常。
- 与 198/197 相同的 `---` 分隔 ✅。

---

## 3. Body 逐段结构分析

### 3.1 段落清单

| 行号范围 | 标题/段落 | 行数 | 内容摘要 |
|---|---|---|---|
| 1-4 | frontmatter | 4 | name + description |
| 6 | `# Radar Vital-Sign Extraction` (H1) | 1 | 页标题 |
| 8 | 简介行 | 1 | 管道总览（raw I/Q → cleaned phase → HR/BR in bpm） |
| 10-63 | `## Full pipeline (every step, in order)` | 54 | 10 个编号步骤（含 7 段 Python 代码块） |
| 65-75 | `## Critical rules` | 11 | 7 条规则表（rule \| why） |
| 77-85 | `## Band edges: use these, not textbook 0.1–0.5 / 0.8–2.5` | 9 | 频带边界表（use \| textbook \| why） |
| 87-95 | `## Decision rules` | 9 | 5 行 If/Then 决策表 |
| 97-101 | `## Sanity checks before reporting` | 5 | 3 条输出前自检 |
| 103-105 | `## When things go wrong` | 3 | 指向 debugging.md |
| 107-114 | `## Not in scope` | 8 | 6 条排除项 |

合计 114 行，其中代码块约 30 行（步骤 5-10 的 Python 片段）。

### 3.2 必需章节
- **Workflow/Process**: ✅ `## Full pipeline (every step, in order)`——10 个编号步骤、含条件分支（FMCW only ×2、fs≥500 条件）、代码随步骤内联，是全库最标准的工作流章节之一。
- **Output Format**: ❌ **缺失**。全篇没有 Output Format / 输出模板章节。最近的替代物是 `## Sanity checks before reporting`（:97-101，3 条自检）与 `## Decision rules` 中的置信度规则——它们规定了"上报前必须满足什么"，但**没有定义"以什么格式上报"**: HR/BR 是否必须带 fs/band/window/method 参数（SCORING OUT-01 要求）、低置信度如何标注（OUT-02 要求）、结果如何呈现。SCORING 的输出要求（OUT-01/02/03）在正文中没有对应章节——agent 只能靠解读评测点来猜输出形态。这是 194 最明确的规范缺口（§7 第 9 项 ❌）。
- **Scope/Limitations**: ✅ `## Not in scope`（6 条，含技术替代方案的指引——如"Arrhythmia → use R-peak/foot detection + RR-interval analysis"），边界清晰且给出正确的替代技术，质量优秀。

### 3.3 内容委托
- 无 `@skill` 委托 ✅。
- 5 个 references 文件是**知识委托**（技术细节外置）: iq-formats（步骤 1）、range-bin（步骤 4）、harmonic-pitfalls（步骤 9 + 决策表）、band-rationale（频带边界）、debugging（排错）——全部由正文显式链接（`[references/xxx.md](references/xxx.md)` 相对链接形式）✅。唯一例外: 决策表 :93 用反引号裸名 "See `harmonic-pitfalls.md`"（非链接），风格不一致（§4.3 与 §13-🟡-3）。

### 3.4 标题层级连续性
- 标题链: H1(1) → H2(6) → 无 H3。层级连续、无跳级 ✅。
- 10 个编号步骤全部在 `## Full pipeline` 内，无悬浮步骤 ✅。
- 无 197 的双 H1 问题 ✅。

### 3.5 vs 600行限制
- 114 行，为上限的 19% ✅。若计入 references（279 行）总知识量为 393 行，仍远低于 600。当前正文密度高、无冗余；即使补 Output Format 章节（约 15-20 行），仍在安全区。

---

## 4. 逻辑一致性深度审查

### 4.1 步骤衔接（N→N+1）
- **步骤 1 → 2**: 解析（CW→1-D / FMCW→2-D）后，FMCW 才有 Range FFT——步骤 2 明确标注 "(FMCW only)"，与步骤 1 的输出形态衔接 ✅。
- **步骤 2 → 3**: Range 矩阵 R 与 CW 的 iq 都被步骤 3 的"减时域均值"覆盖（两行代码分别给出）✅。
- **步骤 3 → 4**: 去杂波后的 R 才有意义做距离门选择——顺序正确 ✅（Critical rules 第 7 条 "Never argmax(magnitude) across all range bins" 与 range-bin.md 的 Don'ts 呼应）。
- **步骤 4 → 5**: 选定 bin 后取相位解缠——✅。
- **步骤 5 → 6**: "Decimate to ~50 Hz **if fs >= 500 Hz**"——相位降采样后才滤波（规则表第 3 条 "Decimate before sub-Hz bandpass"）✅。注意代码块未含条件语句，条件只在散文中（🟡，见 4.4）。
- **步骤 6 → 7**: 降采样后的 fs_new 传入 butter——两个 bandpass 都使用 fs=fs_new ✅。
- **步骤 7 → 8**: 对每个 band 信号做 Welch PSD——✅。
- **步骤 8 → 9**: "HR harmonic rejection — always run"——PSD 峰值之后立刻做子谐波检查 ✅。
- **步骤 9 → 10**: 交叉验证（autocorrelation，optional）——✅。
- **10 步全覆盖闭环**: 步骤 10 之后没有"汇总输出"步骤——衔接在"输出"处断裂（与 §3.2 的 Output Format 缺失同根因）。

### 4.2 内部矛盾
- **3.3 Hz 的两个触发条件**（🟡 轻微）: 决策表 :94 "HR > 150 bpm (tachycardia) | Widen HR band upper to 3.3 Hz"，band-rationale.md:37 "Widen to 3.3 Hz if you know the subject is exercising"——同一动作（上限 3.3 Hz）有两个触发源，均文档化、不相悖（一个是测量驱动、一个是先验知识驱动），但决策表未提 exercising 分支、band-rationale 未提 tachycardia 分支，agent 遇到"正在运动的人 HR 130"时会执行哪个？建议决策表合并（§13-🟡-4）。
- **频带边界表与步骤 7 代码一致**: 步骤 7 代码 `[0.08, 0.5]` / `[0.7, 3.0]` 与频带表 use 列完全一致 ✅。
- **决策表 "PSD 与 autocorr 差 >5 bpm → 低置信度"** 与步骤 10 代码 `abs(bpm_ac - bpm_psd) > 5` 一致 ✅。
- **"BR < 10 bpm → notch 2·BR, 3·BR"**（:93）与 harmonic-pitfalls.md:45-46 "for k in [2, 3]（cap at 3）" 一致 ✅。
- **谐波检查的阈值 0.5**: 步骤 9 代码 `p_sub > 0.5 * p_top`、决策表 :91 "p_sub > 0.5 × p_top"、harmonic-pitfalls.md:18 "tune 0.3-0.6 depending on SNR"——默认值一致，调参说明在参考文件 ✅。
- **"BR < HR always for live adult at rest"**（:99）与频带边界（BR 0.08-0.5 Hz < HR 0.7-3.0 Hz）数值自洽 ✅。
- **15 秒规则**: 决策表 "Clip < 15 s → PSD resolution > tolerance"——15 s @ 50 Hz 降采样后 nperseg=750，分辨率 0.067 Hz ≈ 4 bpm < 5 bpm 容差……实际计算: 若 clip=15 s、fs_new=50，nperseg=750，Δf=50/750≈0.067 Hz≈4 bpm，恰在 5 bpm 容差内偏紧——"PSD resolution > tolerance"的表述在该边界值与容差接近的情况下成立性存疑，但保守地"prefer autocorrelation"无危害。🟢 可注明计算依据。

### 4.3 示例/代码正确性
逐段验证代码（数值与 API 正确性）:
- **步骤 3** `iq -= iq.mean()` / `R -= R.mean(axis=0, keepdims=True)`: 正确 ✅（对 2-D 按 fast-time 轴减均值）。
- **步骤 5** `np.unwrap(np.angle(iq_or_bin)); phase -= phase.mean()`: 正确 ✅（解缠后去均值，保留交流分量）。
- **步骤 6** `scipy.signal.decimate(phase, q=int(fs/50), ftype='iir', zero_phase=True); fs_new = fs / int(fs/50)`: 正确 ✅（zero_phase 需 scipy≥1.1；q 与 fs_new 计算自洽；fs=500→q=10→fs_new=50）。**条件缺失**: "if fs >= 500" 只在散文，代码无守卫——若 agent 照抄代码于 fs=250 会得到 q=5 而非跳过。🟡（与 4.4 同源）。
- **步骤 7** `butter(4, [0.08,0.5], btype='band', fs=fs_new)`（fs 参数需 scipy≥1.2）: 正确 ✅；BR/HR 双滤波 ✅。
- **步骤 8** `nperseg = min(len(x), int(fs_new*25)); welch(x, fs=fs_new, nperseg=nperseg, noverlap=nperseg//2, nfft=8*nperseg, detrend='constant'); peak_hz = f[mask][np.argmax(p[mask])]`: 正确 ✅（零填充 8×；band mask 内取峰）。注意: 对短 clip，nfft=8×nperseg 只是插值，不提高真实分辨率——决策表 :95 已正确处理（prefer autocorrelation）✅，正文与代码自洽。
- **步骤 9** 谐波检查: `f_sub = f_peak_hr / 2.0; if 0.7 <= f_sub <= 3.0: … if p_sub > 0.5 * p_top: f_peak_hr = f_sub`——正确 ✅；与 harmonic-pitfalls.md 的代码一致（该文件用 f_peak 通名，正文用 f_peak_hr，等价）。
- **步骤 10** `ac = np.correlate(x - x.mean(), x - x.mean(), mode='full'); ac = ac[len(ac)//2:] / ac[len(ac)//2]; lag = int(fs_new/f_hi) + np.argmax(ac[int(fs_new/f_hi):int(fs_new/f_lo)]); bpm_ac = 60 * fs_new / lag`:
  - 自相关归一化正确 ✅（full 模式长度 2n-1；ac[len//2:] 从 lag=0 起 ✅）。
  - **🟡 变量缺口**: `f_lo`/`f_hi` 在该片段内**未定义**——需引用步骤 7 的 band 边界（HR 0.7/3.0），但片段单独出现时 agent 无从得知该从何处取值（尤其 BR 交叉验证时 f_lo/f_hi 应是 0.08/0.5 而非 0.7/3.0）。建议片段补注释 `# f_lo, f_hi: band edges of the band being cross-checked (HR: 0.7, 3.0)`。
  - lag 索引边界: `int(fs_new/f_hi)` 对 HR=3.0 上限时 int(50/3.0)=16；`int(fs_new/f_lo)`=int(50/0.7)=71——片段截取 [16:71] 再 argmax，逻辑正确 ✅。
- **References 代码核验**: iq-formats.md 的 fromfile/rfft 片段（:17-34）正确 ✅；range-bin.md 的 `R_k = c·k·(fs/N)/(2·k_chirp)` 量纲正确 ✅；harmonic-pitfalls.md 的 iirnotch 片段（Q=20, k≤3）正确 ✅；debugging.md 的 welch 片段正确 ✅。

### 4.4 条件完整性
- **fs ≥ 500 的条件只有散文没有代码守卫**（🟡）: 步骤 6 "Decimate to ~50 Hz **if fs >= 500 Hz**"——条件明确，但紧跟的代码块无条件包裹。agent 若机械照抄会在低采样率数据上误降采样。建议把条件写进代码或加注释（`if fs >= 500:` 前缀）。
- **CW/FMCW 分支完整**: 步骤 2、4 均标 "(FMCW only)"，CW 路径明确"skips this step" ✅。
- **谐波检查的强制语义**: 步骤 9 标题 "always run"，决策表/CF-01 三重锁定 ✅。
- **低置信度分支**: 步骤 10 "flag as low confidence" + 决策表 :92、:95 + OUT-02（LLM）——完整 ✅。
- **降级选项**: 决策表 :95 "prefer autocorrelation, or flag inconclusive" ✅。
- **缺失**: "输出格式"分支（§3.2）与"sidecar 缺失时怎么办"（步骤 1 "Use the JSON/YAML sidecar to determine format — never assume"，但 sidecar 不存在时无分支——SCOPE-01 脚本要求读到 sidecar，若工作区无 sidecar 该检查失败且 agent 无指令可依）。🟡。

---

## 5. 参考文件内容级审查

### 5.1 引用完整性矩阵

| 参考文件 | 正文引用位置 | 引用形式 | 状态 |
|---|---|---|---|
| references/iq-formats.md | 步骤 1（:12） | `[references/iq-formats.md](references/iq-formats.md)` | ✅ 已引用 |
| references/range-bin.md | 步骤 4（:17） | `[references/range-bin.md](references/range-bin.md)` | ✅ 已引用 |
| references/harmonic-pitfalls.md | 步骤 9（:54）+ 决策表（:93） | 链接 + 裸名反引号 | ✅ 已引用（风格不一，🟡） |
| references/band-rationale.md | 频带边界节（:85） | `[references/band-rationale.md](references/band-rationale.md)` | ✅ 已引用 |
| references/debugging.md | When things go wrong（:105） | `[references/debugging.md](references/debugging.md)` | ✅ 已引用 |

- **5/5 全部被正文引用**——无孤儿文件、无未引用参考。引用矩阵为全绿 ✅（本批唯一达到 100% 引用覆盖的 skill）。
- 反向检查（正文提到的知识是否都落在 references 中）: 频带理由→band-rationale ✅、排错→debugging ✅、谐波→harmonic-pitfalls ✅、格式→iq-formats ✅、距离门→range-bin ✅。**无"正文提了但无出处"的知识点**。

### 5.2 不可见资源审计
- **sidecar 文件（JSON/YAML）**: 步骤 1 与 SCOPE-01 要求 agent 读取 sidecar 确定格式（如 sample_rate_hz、range_per_bin_m、format 字段）。sidecar 是**评测工作区必须预置的资产**，不在 skill 目录内——评估方需确保样例数据自带 sidecar，否则 SCOPE-01（脚本检查 Read 侧 JSON/YAML）直接失败。**风险: 中-高**（评测依赖，但 skill 本身无法打包数据，属正常设计；缺的是"无 sidecar 的提示分支"，见 4.4）。
- 样例数据文件: 同样依赖评测提供（iq-formats 的 fs×duration 校验需要真实数据）——属评测资产而非 skill 缺陷 ✅。
- 外部文献引用: harmonic-pitfalls.md:65-67 与 range-bin.md:36 引用 "Vilesov et al. 2022, ACM TOG"——外部学术引用，标注了出处与适用性说明（"their fix (a trained CNN) is out of scope here"），正当 ✅。

### 5.3 文件全文审查（5 个参考文件逐一审查）

**5.3.1 references/iq-formats.md（42 行）—— I/Q 二进制格式**
- 内容: 4 种常见布局表（complex64_le_interleaved / int16_le_interleaved_complex / int16_le_real_only / complex128，各含 bytes/complex 与来源）、3 段解析代码（interleaved float32 / interleaved int16 / real-only rfft）、首步校验（len == fs×duration）、端序说明。
- 质量: **高**。每种格式都给了"来源"列（TI DCA1000/Xethru/板载 ADC 模式），agent 能按板卡溯源；real-only 模式的 rfft 处理（:31-34）与 FMCW 场景衔接正确；2×/0.5× 校验口诀与 debugging.md 步骤 3 一致（跨文件一致性 ✅）。
- 问题: 无实质问题。细微点: "complex128" 行标注 "rare; only in post-processed Python pickles" 但未给解析代码（fromfile 读 float64 即可，属可推断操作）——🟢。
- 与正文一致性: 步骤 1 "never assume" ↔ 文件首行 "always check, never assume" ✅。

**5.3.2 references/range-bin.md（40 行）—— FMCW 距离门选择**
- 内容: 3 种选择启发式（prior-window 幅度峰 / 生命体征带能量 / 组合分）按鲁棒性排序、2 条 Don'ts（原始相位方差、全局 argmax）、prior window 计算（含 R_k 公式与 sidecar 直取 range_per_bin_m）、相邻 bin 相干求和、选后 sanity check。
- 质量: **高**。启发式按适用场景区分（"rejects bright-but-static reflectors; use when (1) is ambiguous"），不是简单列表；"combined score = mean_magnitude × sqrt(vital_band_power)" 有明确公式；相干求和（:31-34）给出完整代码且解释了"为什么"（chest spans 2-3 bins、peak bin jitters）。
- 问题: "Do not use raw phase variance" 的机理说明（"random uniform noise on a ±π circle unwraps to a random walk"）专业且正确 ✅。无实质问题。
- 与正文一致性: 步骤 4 "physical prior window (e.g., 0.3–1.5 m for a seated subject)" ↔ 文件 :9 同值 ✅；Critical rules 第 7 条 ↔ 文件 Don'ts 第 2 条 ✅。

**5.3.3 references/band-rationale.md（55 行）—— 频带边界理由**
- 内容: BR 下界 0.08 Hz（表: 坐位 12-20 / 卧位 5-10 / 睡眠 6-14 / 冥想 4-8 bpm）、HR 下界 0.7 Hz（表: 运动员 40-55 / post-tilt 45-60 / 睡眠 45-65 / β 阻滞剂 50-65）、HR 上界 3.0 Hz（表: 运动后 120-180 / 儿童 70-120 / 发热 100-160）、为何不再加宽（0.02-0.05 Hz 体动伪迹、4-12 Hz 震颤）、覆盖表（5 场景 → 5 组频带）。
- 质量: **极高**。每个边界都有"临床场景 × 典型值"证据表和"切错会漏掉谁"的后果句（"Cutting at 0.8 Hz silently fails bradycardia and anyone on HR-lowering medication"）；"Why not go wider" 给出反向约束；"When to override" 表把教科书频带也纳入（"Known-healthy adult, resting, short clip → 0.1-0.5 / 0.8-2.5"），**避免了"我的频带永远正确"的教条**。
- 问题: 唯一可议点——"since the 5th–6th BR harmonics for normal 12–20 bpm breathing are at 1.0–2.0 Hz, not 0.7"（:26）: 12-20 bpm = 0.2-0.33 Hz，5-6 次谐波 = 1.0-2.0 Hz ✅ 正确；而 0.7 Hz 处是 2-3.5 次谐波——叙述准确。无实质问题。
- 与正文一致性: 频带表 use 列 = 正文 `## Band edges` use 列 ✅；3.3 Hz 加宽建议 = 决策表 :94 ✅；睡眠 0.05-0.5 与决策表/正文默认（0.08）不冲突（是专门场景覆盖表）✅。

**5.3.4 references/harmonic-pitfalls.md（67 行）—— 谐波陷阱**
- 内容: Pitfall 1（HR 二次谐波压制基波——机理: 机械脉冲非正弦、肩部结构、Fourier 分解二次谐波≈基波；后果: 60 bpm 被报成 120 bpm；缓解代码 + 阈值调参 0.3-0.6 + 交叉检查技巧"unfiltered PSD 中看 2f/3f"）；Pitfall 2（呼吸谐波泄漏入 HR 带——机理: 慢呼吸 7-10 bpm 的 5-8 次谐波落在 0.6-1.4 Hz；典型失败签名: supine 慢呼吸者 argmax 落在呼吸谐波；3 级缓解: iirnotch k≤3 / Chebyshev-II 锐下裙 / harmonic-support 评分）；硬案例（HR ≈ k×BR 时的诚实处理: 接受 3-5 bpm 误差并标记）；文献引用（Vilesov et al. 2022 §5.2 原文引用）。
- 质量: **极高**。这是三个 skill 全部参考文件里知识深度最高的一个: 两个陷阱的机理、信号特征、失败签名、按 SNR 调参、无法分离的硬案例及"don't pretend to produce a precise answer"的诚实原则，构成完整的决策知识包。特别加分: 明确指出 Pitfall 2 失败发生在 Pitfall 1 修复**之后**（"happen independently of and after the Pitfall-1 fix"），防止 agent 误以为一次修复双杀。
- 问题: 无实质问题。细微点: 阈值方向说明（"Tighten to 0.3 in high-SNR…; loosen to 0.6 for noisy radar"）逻辑与直觉相反（噪声高应更保守地接受子谐波——实际上噪声高时二次谐波假峰更常见故 0.6 更宽松 ✓ 方向正确）✅。
- 与正文一致性: 步骤 9 代码 = 文件代码（变量名 f_peak vs f_peak_hr 等价）✅；决策表 :93 "notch 2·BR, 3·BR" = 文件 k∈{2,3} ✅。

**5.3.5 references/debugging.md（75 行）—— 排错清单**
- 内容: 8 步按序排错（文件大小 sanity → 散点 I vs Q → 长度 vs 时长 → 平均距离剖面 FMCW → 原始包裹相位 → 解缠相位 → 解缠相位 PSD → fs 假设复核），每步含"期望信号特征"与"异常模式→根因"对照。
- 质量: **高**。每步都是"检查什么 → 期望什么 → 每类异常意味着什么"三段式（如 "Tight blob: DC-dominated — clutter removal missing"、"Exact-2π step discontinuities after unwrap mean unwrap failed"）；修复步骤（低通滤波后再解缠、换 bin）具体可执行。fs 复核（步骤 8: "A 2× error in fs turns real 1 Hz HR into a spurious 2 Hz peak"）是很多人忽略的关键兜底。
- 问题: 无实质问题。步骤 2 的散点图四种形态（arc/blob/off-center circle/uniform）分类清晰。与 iq-formats 的 2×/0.5× 校验重复出现（有意的一致性，非冗余）✅。
- 与正文一致性: :105 "walk through references/debugging.md" ↔ OUT-03（LLM）✅。

### 5.4 跨Skill引用
- 全文无 `../` 相对路径、无其他 skill 目录引用 ✅。
- description 无跨 skill 路由 ✅。
- 外部引用仅限学术文献（Vilesov et al. 2022 ×2）——规范 ✅。

### 5.5 嵌套重复/死文件
- 无死文件（5/5 被引用）✅。
- 跨文件知识重复检查: "len == fs×duration" 校验出现在 iq-formats.md:37-38 与 debugging.md:27-30——两处语境不同（一个是解析后首查、一个是排错清单步骤 3），**有意且有益的重复**，非冗余 ✅。
- 阈值 0.5 出现于正文（:51）、决策表（:91）、harmonic-pitfalls（:18）——三处为同一规则的传播，数值一致 ✅。

---

## 6. 语法与格式质量

### 6.1 拼写错误
- 通读正文 + 5 参考文件未发现拼写错误。抽查高风险词: "interleaved"（:3）、"unwrapping"（:3）、"decimate/decimation"（多次）、"autocorrelation"（:56,63）、"tachycardia"（:94）、"bradycardia"（:82, band-rationale:26）、"plethysmography"（harmonic-pitfalls:67）——全部正确 ✅。
- "IQ" vs "I/Q" 混用（正文 :3 "I/Q captures"、:12 "complex 1-D array"、iq-formats 标题 "I/Q Binary Formats"）——拼写一致（I/Q 为主）✅。

### 6.2 语法错误
- 未发现语法错误。句子以祈使句 + 条件句为主（管道说明书风格）✅。
- 决策表 "BR estimate < 10 bpm (slow breather)" 语法精炼 ✅。

### 6.3 中英/葡英混杂
- 全英文，无中文/葡萄牙语混入 ✅。单位标注（Hz/bpm/m/GHz）规范 ✅。

### 6.4 Markdown破损
- 表格管道对齐正确（Critical rules :67-74、Band edges :79-83、Decision rules :89-94、参考文件各表）✅。
- 代码块: 7 段 Python 围栏（:19-22, :24-27, :31-34, :37-43, :46-53, :57-61）+ 决策表内的裸行——围栏全部成对 ✅。
- 相对链接 `[references/xxx.md](references/xxx.md)` 格式正确，路径与真实文件一致（可点击验证）✅。
- 内联代码反引号使用一致 ✅。

### 6.5 占位符未填充
- 正文无方括号占位符（无输出模板，因此也无模板占位）✅。
- 代码片段中的 `x`、`f_peak_hr`、`f_lo/f_hi` 是变量名而非占位符 ✅（f_lo/f_hi 未定义问题属 §4.3 的代码完备性，非占位符问题）。

### 6.6 截断
- 正文以完整句收尾（:114 "use a spectrogram, not single-window PSD."），5 个参考文件均以完整句收尾——无截断 ✅。

---

## 7. 规范合规性 — 12-item checklist vs SKILL-SPEC v1.0

| # | 检查项 | 判定 | 说明 |
|---|---|---|---|
| 1 | name 小写+连字符 ≤64 且匹配目录 | ✅ | `radar-vital-signs`，16 字符 |
| 2 | description 第三人称 WHAT+WHEN+关键词 ≤1024 | ✅ | 640 字符；三段式（WHAT/WHEN 10 关键词/Not-for 负面清单），本批最佳 |
| 3 | description 无祈使/第一/第二人称 | ✅ | "Claude needs to" 全第三人称 |
| 4 | description 无跨 skill 路由 | ✅ | 无 |
| 5 | 至少一个触发信号 | ✅ | "Use when Claude needs to…" + 10 个动作关键词 |
| 6 | 无禁止 frontmatter 键 | ✅ | 仅 name/description |
| 7 | body ≤ 600 行 | ✅ | 114 行（+references 279 行） |
| 8 | 存在 workflow/process 章节 | ✅ | `## Full pipeline (every step, in order)` + 10 编号步骤 |
| 9 | 存在 output format 章节 | ❌ | **缺失**；`Sanity checks before reporting` 只约束"报什么"不定义"怎么报"；SCORING OUT-01/02/03 在正文无对应章节 |
| 10 | 存在 scope/limitations 章节 | ✅ | `## Not in scope`（6 条 + 替代技术指引） |
| 11 | 无跨 skill 文件路径（../） | ✅ | 全文无 |
| 12 | 目录 NNN-kebab-case | ✅ | `194-radar-vital-signs` |

**合规小结**: 12 项中 11 项过、1 项 ❌（output format）。这是全库最"干净"的合规画像之一——唯一硬缺口恰是本批三个 skill 中另一个（198）反向缺失的章节，说明该目录下的 skill 存在"结构部分互补、各自不完整"的模式。

---

## 8. 人机感评估

### 8.1 Emoji审计
- SKILL.md **全文 0 个 emoji**（grep 验证: 🟢🟡🟠🔴✗✅❌⚠️ 计数均为 0）✅。
- 5 个参考文件同样 0 emoji（harmonic-pitfalls 用 ≈/×/± 数学符号，非 emoji）✅。
- 风格: 纯技术文档，无任何装饰性符号——本批三人机感最干净的 skill ✅。

### 8.2 全大写/喊叫
- 全文无全大写单词（grep 大写词检查: 最高为 "FMCW only"、"ALWAYS"? —— 步骤 9 为 "**HR harmonic rejection — always run**"（:44），"always" 小写加粗而非全大写）。**0 处喊叫** ✅。
- 强调手段统一为 markdown 加粗（**Parse**/**FMCW only**/**always run**）——克制且有效 ✅。

### 8.3 Persona语气
- 整体 persona: **懂雷达信号处理的资深工程师**——代码、数学、物理机理精确，用"为什么"支撑每条规则（Critical rules 的 why 列是 persona 的核心载体）。
- 代表性引语（5-8 条）:
  1. "1 mm motion at 24 GHz ≈ 1 rad; magnitude costs ~40 dB of SNR." (SKILL.md:69)
  2. "DC offset anchors phase off zero, eats the ±π unwrap budget." (:70)
  3. "HR is 10×–100× smaller than BR; single wide filter can't separate them." (:72)
  4. "SciPy biquad silently NaNs at very-low normalized cutoffs." (:71)
  5. "Raw bin spacing `fs/nperseg` is often coarser than tolerance." (:73)
  6. "the 5th–8th harmonics of respiration land in the 0.6–1.4 Hz range" (harmonic-pitfalls.md:30)
  7. "a reader who verifies everything verifies nothing" 属于 197——194 的风格是 "Widen only with specific justification." (SKILL.md:85)
  8. "When in doubt, use the slightly-wider defaults — it's safer to admit extra noise and reject it than to silently clip real signal." (band-rationale.md:55)
- 评估: persona 高度一致（工程师风格），每条规则都有可验证的物理/数值理由，无教条化语气——"always"与"never"的每次使用都有对应的机理说明，**专业可信度是本批最高** ✅。

### 8.4 人机边界
- 边界清晰: 机器负责全部信号处理（10 步管道），人类负责提供数据/sidecar 与最终判断（"flag as low confidence" 而非替人下结论）✅。
- 诚实原则: "don't commit to one value"（:92）、"accept higher error (3-5 bpm) and flag"（harmonic-pitfalls:63）、"Don't pretend to produce a precise answer you can't justify"（:64）——机器对自身不确定性的诚实表达是本批最佳 ✅。

### 8.5 人称分析（grep 实测）
| 词 | 出现次数 | 位置/性质 |
|---|---|---|
| you / your | 0 | — |
| I | 4 | **全部为 "I/Q" 中的 "I"**（:3 ×2、:12、:76 及 iq-formats 等处），非第一人称代词 |
| we / us / our | 0 | — |

- **分析**: 实质人称代词使用次数为 **0**——正文、参考文件全部采用无主祈使句（"Remove static clutter."、"Pick the subject range bin"）与代码直陈。这是全库最严格的第三人称/无主语风格，规范 item 3 完全达标 ✅。
- 对比: 198 有 5 you + 2 I（自查清单），197 有 35 we/us/our——194 的人称纪律遥遥领先。

### 8.6 表格太多 → 转换为自然语言
- 正文 3 张表（Critical rules 7 行、Band edges 4 行、Decision rules 5 行）+ 参考文件 6 张表——全部是"规则/条件-原因/动作"型对照表，是工程规范的标准载体，**表格优于自然语言** ✅。
- 表内语言密度高且列设计合理（rule | why 两列即可表达完整逻辑），无冗余列 ✅。
- 无需要转换的叙事性表格 ✅。

---

## 9. 可执行性评估

### 9.1 独立可执行性（0-10）: **8/10**
- 扣分点: (1) 无输出格式章节——agent 完成管道后"怎么交付"只能靠猜（-1）；(2) f_lo/f_hi 等片段变量未定义 + fs≥500 条件无代码守卫，机械照抄会出错（-1）。
- 得分理由: 10 步管道每一步都有代码或可执行的指令；7 段代码可直接复制运行（numpy/scipy API 全部正确）；5 个参考文件在需要时被显式引导；决策表把"异常分支"全部钉死。**在本批三个 skill 中可执行性最高**。

### 9.2 步骤可操作性
- 每步可操作性评级: 高。步骤 1-10 均以"动词 + 对象 + 产出"定义（"Parse binary I/Q into a complex 1-D array"），关键步骤附代码。**独特性**: 大部分 skill 靠文字描述让 agent 自由实现，本 skill 直接给出可运行的片段，agent 的执行方差被压到最低 ✅。
- 决策表 5 行全部可布尔判定（"f_peak/2 in HR band and p_sub > 0.5 × p_top → Pick sub-harmonic"）✅。
- Sanity checks 3 条可执行且带数值判据（"Off by 2× ⇒ harmonic error slipped through"）✅。
- 唯一低可操作点: "Output"环节（§3.2）与 debugging 的触发条件（"If output looks like garbage" 依赖 agent 自评"看起来像垃圾"，:103——建议给量化触发（如 sanity check 不通过））。

### 9.3 工具依赖
| 工具 | 用途 | 依赖类型 | 风险 |
|---|---|---|---|
| Read | 读 sidecar（JSON/YAML）与数据文件 | 必备（SCOPE-01 计分） | 中：sidecar 由评测预置 |
| Bash/Python | 执行 numpy/scipy 代码 | 必备（QA-01 计分） | 低：标准环境 |
| 无其他工具 | — | — | — |
- 依赖面窄、均为标准工具 ✅。不依赖任何外部配置/插件（对比 197 的插件配置依赖，194 的独立性极佳）。

---

## 10. SCORING.yaml 交叉参考

### 10.1 测评点覆盖
- **total_items: 20**，实际计数: SCOPE 3 + PROC 11 + OUT 3 + NEG 2 + QA 1 = **20** ✅ 一致。
- **脚本 vs LLM 分工**: 脚本 13 项（SCOPE-01, PROC-01~09, PROC-11, OUT-01, QA-01），LLM 7 项（SCOPE-02/03, PROC-10, OUT-02/03, NEG-01/02）。check.py:82 运行 13 项，docstring "Run all 13 script checks" 与实现一致 ✅。
- 13 项脚本检查逐条与正文/参考文件核对:
  - `SCOPE-01` `"tool": "Read"[^}]*\.(json|ya?ml)`（tool log 中 Read 调用了 sidecar）: 与步骤 1 "Use the JSON/YAML sidecar" 对应 ✅。**脆弱点**: 正则依赖 tool log 条目内 `"tool": "Read"` 与路径同处一个 JSON 对象且路径含 .json/.yml/.yaml——若 runner 日志格式不同（如用 "name" 字段）或 sidecar 名无扩展名，检查失效。建议 runner 侧确认格式。
  - `PROC-01` `fromfile|frombuffer`: 与 iq-formats.md:17-30 解析代码对应 ✅（agent 输出含 np.fromfile 即过）。
  - `PROC-02` `fft\(`: 对应步骤 2 Range FFT ✅——注意 "rfft(" 也包含 "fft("，real-only 路径同样通过，设计自洽 ✅。
  - `PROC-03` `\.mean\(`: 对应步骤 3 杂波去除 ✅——弱代理（任何 .mean( 都过，包括数据标准化），但结合 NEG-01（LLM，检查是否 angle 前去除）可接受。
  - `PROC-04` `unwrap\(`: 对应步骤 5 ✅。
  - `PROC-05` `decimate\(`: 对应步骤 6 ✅——**弱代理**: 只查调用不查条件（fs≥500），照抄误用也不拦截（与 §4.4 同源）。
  - `PROC-06` `0\.08`: 对应频带边界 ✅——弱代理（出现 "0.08" 即过，哪怕在注释中），与 NEG-02（LLM 检查教科书频带是否无理由使用）互补，可接受。
  - `PROC-07` `welch\(`: 对应步骤 8 ✅。
  - `PROC-08` `p_sub`: 对应步骤 9 谐波检查 ✅——**选择极好**: 检查唯一标识符而非泛化模式，误报率最低。
  - `PROC-09` `correlate\(`: 对应步骤 10（optional）✅——注意 "np.correlate" 是可选步骤，测评将其列为必须出现，与正文 "optional but recommended" 存在张力: 若 agent 合理跳过（如超短 clip 用其他方法），脚本检查会判失败。🟡 建议 SCORING 注明"步骤 10 为 recommended——脚本检查通过为加分而非必须"，或正文去掉 optional 表述。
  - `PROC-11` `br < hr|BR < HR|br_bpm < hr_bpm`: 对应 sanity check 1 ✅——大小写覆盖了三段代码命名习惯，设计贴心 ✅。
  - `OUT-01` `bpm`: 对应输出报告 ✅——弱代理（任何 bpm 字样即过），配合 OUT-02（LLM）可接受。
  - `QA-01` `import numpy|from scipy`: 对应"可执行代码"✅——弱代理但方向正确。
- **覆盖缺口**: (a) 输出格式（OUT-01/02/03）全部无正文支撑（§3.2 核心缺口）；(b) 决策表 "BR < 10 bpm → notch 2·BR/3·BR" 只有 LLM 项 PROC-10；(c) 频带"加宽需理由"（:85 "Widen only with specific justification"）只由 NEG-02（LLM）覆盖。
- **脚本/LLM 配比评价**: 13 脚本 : 7 LLM，是本批三个 skill 中客观化程度最高、评测方差最小的 ✅。

### 10.2 Critical Failures分析
- CF-01（跳过谐波抑制，把二次谐波当心率上报 → cap_to_0）: 与步骤 9 "always run" + Critical rules 第 6 条 + 决策表第 1 行三重一致 ✅。这是本 skill 最有价值的 CF——命中最常见的专业错误。
- CF-02（用幅度而非相位 / 在 angle 之后才去杂波 → cap_to_0）: 与 Critical rules 第 1、2 条一致 ✅。将两条最容易犯的"管道级"错误设为 cap_to_0，惩罚力度与危害（SNR 损失 40 dB / 解缠预算被 DC 吃光）匹配 ✅。
- **评估**: 2 个 CF 全部是"信号处理正确性"型硬约束，且都给出机理（dB 数字、unwrap 预算），不是空泛警告。无虚设 CF ✅。
- **潜在执行问题**: CF-02 的判定（LLM）需要 judge 理解"clutter removal before angle"的代码语义——建议 evidence 明确要求引用代码行的顺序证据。

---

## 11. 已知问题汇总（来自 skill-dossier.md）

**Dossier 记录**: `194-radar-vital-signs: "总评: 🟡"`

**本次复核结论**: 🟡 判定**部分成立**——需区分"内容质量"与"规范完整性"两个维度:
- **内容质量维度**: 194 实际是本批最强（管道代码可执行、参考文件 5/5 高深度、人称为零、无 emoji/喊叫、description 最佳实践）。若仅按内容评分，194 应高于 197。
- **规范完整性维度**: 🟡 成立的理由:
  1. **Output Format 章节缺失**（§7 第 9 项 ❌）——规范硬缺口，且 SCORING 的 OUT-01/02/03 无正文支撑。
  2. 代码片段变量缺口（f_lo/f_hi 未定义，§4.3）+ fs≥500 条件无代码守卫（§4.4）。
  3. PROC-09 与正文 "optional" 表述的张力（§10.1）。
  4. 决策表 :93 引用风格不统一（裸名 vs 链接）。
- **Dossier 未记录、本次新发现**:
  - PROC-09（optional 步骤被脚本强制）的测评语义冲突。
  - SCOPE-01 对 tool log 格式的依赖（§10.1）。
  - sidecar 缺失分支未定义（§4.4）。
  - "Clip < 15 s" 的 PSD 分辨率边界值论证可补充（§4.2 末）。
- **结论**: dossier 🟡 在"规范完整性"意义上成立；建议 dossier 追加内容质量维度的正面记录（description 样板、参考体系 100% 覆盖、代码可执行性），避免总评被规范缺口单因素拉低。

---

## 12. 综合评分 — 8 dimensions weighted

| 维度 | /10 | 权重 | 加权 |
|------|:---:|:----:|:----:|
| Frontmatter合规 | 10 | 10% | 1.00 |
| Body结构完整 | 8 | 10% | 0.80 |
| 逻辑一致性 | 9 | 20% | 1.80 |
| 参考完整性 | 9 | 15% | 1.35 |
| 语法格式 | 10 | 10% | 1.00 |
| 规范合规 | 8 | 15% | 1.20 |
| 人机感 | 10 | 10% | 1.00 |
| 可执行性 | 8 | 10% | 0.80 |
| **加权总分** | | | **8.95 → 89.5/100** |

**Rating: 🟢 A（80-100）** — 与 dossier 总评 🟡 存在分歧（见 §11 分析；若严格执行规范 item 9 一票降档，则为 🟡 B-）。

各维度评分理由:
- Frontmatter 10: description 三段式（WHAT/WHEN/Not-for）为全库样板，人称、长度、触发全绿。
- Body 结构 8: 无 Output Format 章节（-1）；Sanity checks 部分补偿（-1 不给满分理由: 该缺口与 §7 第 9 项联动，此处仅因"自检+决策表部分覆盖输出语义"而未给更低分）。
- 逻辑一致性 9: 仅 f_lo/f_hi 变量缺口与 3.3 Hz 双触发（-1）；10 步衔接、代码 API、跨文件数值全部自洽。
- 参考完整性 9: 5/5 引用覆盖、深度极高；扣 1 因引用风格不一（:93）与文献引用无链接（可点击性）。
- 语法格式 10: 零拼写/语法/markdown 问题，代码可复制运行。
- 规范合规 8: 12 项中 11 项过、item 9 ❌。
- 人机感 10: 零 emoji、零喊叫、零人称代词、工程师 persona 一致、诚实原则突出。
- 可执行性 8: 管道级可执行性最高；输出环节与片段变量守卫缺失各扣 1。

---

## 13. 修复建议（按优先级分层）

### 🔴 致命缺陷

本 skill **无致命缺陷**（无死锁、无违规性硬伤、无外部硬依赖）。以下 🟡 第一项（Output Format）因与规范 item 9 硬绑定，建议按"准致命"优先级处理。

**🔴-1（准致命）. 缺失 Output Format 章节（规范 item 9 ❌，SCORING OUT-01/02/03 无正文支撑）**
- 位置: SKILL.md 全文（建议插入 `## Sanity checks before reporting` 之后、`## When things go wrong` 之前）
- 问题: 完成 10 步管道后，"怎么上报"没有定义: HR/BR 的单位与格式、必须附带的处理参数（fs、band、window、method——OUT-01 明确要求）、低置信度/不明确的标注方式（OUT-02 要求）、结果表格或文本形态。agent 只能从 SCORING 反推输出要求——这是"测评驱动正文"的倒挂。
- 修复方案: 新增章节（约 15-20 行）:
  > "## Output Format
  > Report the results as:
  > - **HR: {N} bpm | BR: {N} bpm**
  > - **Parameters:** fs (post-decimation), band edges used per band, PSD window (nperseg/nfft), peak-selection method (PSD/autocorrelation/both)
  > - **Confidence:** for each rate, one of `high` (PSD and autocorrelation agree ≤5 bpm), `low` (disagree >5 bpm or clip <15 s — report the autocorrelation value and mark low), `inconclusive` (no reliable peak — state why)
  > - **Checks:** state the sanity checks passed (BR<HR; peak count vs HR×duration; plausibility bands)
  > If any result is low-confidence, say so in the same breath as the number — never present a flagged value as final."
- 后果: 规范 item 9 转 ✅；OUT-01/02/03 从"测评倒挂"变为正文可执行指令；agent 输出方差大幅下降。

### 🟡 重要缺陷

**🟡-1. 步骤 10 代码片段变量 f_lo/f_hi 未定义**
- 位置: SKILL.md:60（`lag = int(fs_new/f_hi) + np.argmax(ac[int(fs_new/f_hi):int(fs_new/f_lo)])`）
- 问题: 片段脱离上下文时无从取值——且交叉验证哪个 band（HR 用 0.7/3.0，BR 用 0.08/0.5）只能靠推断。
- 修复: 片段前加一行注释 `# f_lo, f_hi = band edges of the band being cross-checked (e.g., HR: 0.7, 3.0)`，或改写为带参数定义的完整函数。
- 后果: 机械照抄不会出错；PROC-09 的"correlate(" 检查与实际代码一致性提高。

**🟡-2. fs ≥ 500 条件无代码守卫**
- 位置: SKILL.md:23-27（步骤 6）
- 问题: "if fs >= 500 Hz" 只存在于散文；低采样率数据照抄代码即误降采样。
- 修复: 代码改为 `if fs >= 500: phase_ds = decimate(...); fs_new = fs / int(fs/50) else: phase_ds = phase; fs_new = fs`——或至少加注释 "guard: only decimate when fs >= 500"。
- 后果: 代码与规则零歧义；PROC-05 弱代理问题部分缓解（见 🟡-4）。

**🟡-3. PROC-09 与正文 "optional" 的语义冲突**
- 位置: SKILL.md:56（"Cross-check with autocorrelation (optional but recommended)"）vs SCORING.yaml:97-103（PROC-09 脚本强制 `correlate\(`）
- 问题: 正文允许合理跳过（如超短 clip 优先 autocorrelation 反而该用——实际上短 clip 情形下 autocorrelation 是首选，无冲突；但"可选"措辞仍与"脚本必须出现"矛盾: agent 若以其他方法替代且解释合理，脚本仍判失败）。
- 修复: 二选一——(a) 正文将 "optional but recommended" 改为 "required: run the autocorrelation cross-check (use it as the primary method for clips < 15 s)"；(b) SCORING 将 PROC-09 降为提示性（judge: llm 或 note）。
- 后果: 消除"正文说可选、测评说必须"的指令冲突；短 clip 场景的执行路径更清晰。

**🟡-4. 脚本检查弱代理项集中说明**
- 位置: SCORING.yaml PROC-03（`.mean\(`）、PROC-05（`decimate\(`）、PROC-06（`0\.08`）、OUT-01（`bpm`）、QA-01（`import numpy|from scipy`）
- 问题: 均为"出现即过"的弱代理，无法验证"在正确位置、正确条件下使用"。
- 修复: 不强制全改（成本高），建议: (a) 对 PROC-05 增加条件模式（`decimate\s*\(` 与 `fs\s*>\s*=\s*500|fs\s*>=\s*500` 组合）；(b) 其余弱代理在 SCORING 中加 note 说明"与 NEG-01/02（LLM）互补判定"；(c) 明确 PROC-08 为最强检查样板，后续 skill 参照。
- 后果: 测评语义透明化，避免"伪高分"。

**🟡-5. sidecar 缺失时无分支 + SCOPE-01 对日志格式的依赖**
- 位置: SKILL.md:12（步骤 1）、SCORING.yaml:10-13
- 问题: 无 sidecar 时 agent 无指令（"never assume" 的规则反而让它无法启动）；SCOPE-01 正则依赖 `"tool": "Read"` 的 JSONL 字段名。
- 修复: 步骤 1 补一句 "If no sidecar exists, ask the user for the sample rate and format, or infer from the file naming convention and state the assumption."；SCOPE-01 建议改用 `file_exists` 或与 runner 确认日志 schema。
- 后果: 评测与真实场景都有确定路径；SCOPE-01 不再依赖日志格式巧合。

**🟡-6. 3.3 Hz 双触发条件未合并 + 决策表引用风格不一**
- 位置: SKILL.md:94（"HR > 150 bpm → 3.3 Hz"）、band-rationale.md:37（"exercising → 3.3 Hz"）、SKILL.md:93（裸名 "See `harmonic-pitfalls.md`"）
- 修复: 决策表增加一行 "Subject known to be exercising | Use 3.3 Hz upper edge from the start"；:93 改为与其余四处一致的 `[references/harmonic-pitfalls.md](references/harmonic-pitfalls.md)` 链接。
- 后果: 触发条件单一化；引用风格统一（§5.1 矩阵全绿升级为全链接）。

### 🟢 优化建议（非必需）

**🟢-1.** `## Sanity checks before reporting` 的 "If output looks like garbage"（:103）补量化触发: "If any sanity check fails, walk through references/debugging.md"——把主观触发改为客观触发。
**🟢-2.** "Clip < 15 s" 规则（:95）补充一行论证: "15 s @ 50 Hz → PSD resolution ≈ 4-8 bpm, at or above the 5 bpm tolerance"——让数值决策可被读者验证（§4.2 末的存疑点即由此解决）。
**🟢-3.** 步骤 4 的示例窗口 "0.3–1.5 m" 在正文与 range-bin.md 出现两次——可加注 "scaled by `range_per_bin_m` from the sidecar"（range-bin.md:23-25 已给出代码，正文只需一句指引）。
**🟢-4.** harmonic-pitfalls.md:65-67 与 range-bin.md:36 的文献引用可加 URL/DOI（若团队政策允许）——增强可核查性。
**🟢-5.** 考虑在 description 尾部追加 "Handles CW and FMCW; returns HR and BR in bpm with confidence flags."——输出契约提前到触发层（非必需，当前 description 已很好）。

### 修复工作量估计
- 🔴-1（Output Format 章节）: 30-45 分钟（写 15-20 行模板，与 OUT-01/02/03 对齐）。
- 🟡-1/-2（代码守卫与变量注释）: 各 10 分钟。
- 🟡-3（optional vs 强制）: 15 分钟（改正文一句或改 SCORING 一行）。
- 🟡-4（弱代理说明）: 30-60 分钟（SCORING note + 与 runner 验证）。
- 🟡-5: 30 分钟（正文分支 + 与 runner 确认日志 schema）。
- 🟡-6: 10 分钟。
- 总计: 约 2-3 小时完成全部 🟡 项；仅修 🔴-1 约 45 分钟。
- 优先级建议: 🔴-1（规范硬缺口 + 测评倒挂，必改）→ 🟡-1/-2（代码正确性，照抄即受益）→ 🟡-3/-5（测评语义，需与 runner 协同）→ 🟡-4/-6 → 🟢 项。

---

## 附录: 审查过程记录

- **审查时间**: 2026-08-06
- **审查顺序**: 198 → 197 → 194（按任务指定逆序）
- **工具链**: Glob（目录清单）→ Read（全部 8 个文件全文）→ Bash `wc -l`（行数核验）→ Bash grep 正则（人称/emoji 计数，验证 194 的 "I" 均为 I/Q 字样）→ 人工逐行分析 + 代码数值验算
- **已读文件（8/8，全文）**:
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\SKILL.md（114 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\SCORING.yaml（179 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\check.py（82 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\references\band-rationale.md（55 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\references\debugging.md（75 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\references\harmonic-pitfalls.md（67 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\references\iq-formats.md（42 行）
  - D:\SkillIF\skill-experiment\complex-skills\194-radar-vital-signs\references\range-bin.md（40 行）
- **辅助参考**: 同级 `_shared/checker.py`（351 行）——确认 `output_contains`/`tool_log_contains` 的正则语义，支撑 §10.1 弱代理与 SCOPE-01 格式依赖分析。
- **代码核验**: 步骤 3-10 全部代码片段做了 API/数值逐行验算（decimate q/fs_new、welch nperseg/nfft、自相关 lag 边界、谐波阈值 0.5 传播），结果见 §4.3。
- **未修改任何文件**: SKILL.md、SCORING.yaml、check.py 及 5 个 references 文件均未改动；仅新建本 REVIEW.md。
- **评分一致性**: 加权总分 89.5 → 🟢 A，与 dossier "总评: 🟡" 存在分歧；§11 已列出分歧原因（规范完整性 vs 内容质量双维度）与 dossier 未记录的 4 项发现。
