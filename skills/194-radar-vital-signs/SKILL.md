---
name: radar-vital-signs
description: End-to-end pipeline for extracting heart rate (HR) and breathing rate (BR) from raw short-range radar I/Q captures — both continuous-wave (CW, 24 GHz clinical boards) and FMCW mmWave (60/77 GHz, TI IWR/AWR). Use when Claude needs to parse interleaved I/Q binary, do a Range FFT on FMCW chirps, remove static clutter, pick a subject range bin, extract phase with unwrapping, design HR/BR bandpass filters, pick a peak frequency via PSD, reject the HR second harmonic that often dominates the fundamental, or handle respiration-harmonic leakage on slow breathers. Not for pulse/UWB range gating, MIMO beamforming, Doppler-only gesture radar, arrhythmia detection, or multi-subject source separation.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Radar Vital-Sign Extraction

End-to-end pipeline: raw radar I/Q → cleaned phase signal → HR and BR in bpm.

## Full pipeline (every step, in order)

1. **Parse binary I/Q** into a complex 1-D array (CW) or 2-D range matrix (FMCW). Use the JSON/YAML sidecar to determine format — never assume. If no sidecar exists, infer the sample rate and format from the file naming convention and state the assumption; ask only if genuinely un-inferable. See [references/iq-formats.md](references/iq-formats.md).
2. **(FMCW only) Range FFT** across fast-time samples of each chirp → range matrix `R[n_chirp, n_range_bin]`. CW skips this step.
3. **Remove static clutter.** Subtract the temporal mean:
   - CW: `iq -= iq.mean()`
   - FMCW: `R -= R.mean(axis=0, keepdims=True)`
4. **(FMCW only) Pick the subject range bin** within a physical prior window (e.g., 0.3–1.5 m for a seated subject). See [references/range-bin.md](references/range-bin.md).
5. **Extract phase with unwrap:**
   ```python
   phase = np.unwrap(np.angle(iq_or_bin))
   phase -= phase.mean()
   ```
6. **Decimate to ~50 Hz** if `fs >= 500 Hz` (sub-Hz filtering at kHz is numerically unstable):
   ```python
   from scipy.signal import decimate
   if fs >= 500:
       phase_ds = decimate(phase, q=int(fs/50), ftype='iir', zero_phase=True)
       fs_new = fs / int(fs/50)
   else:
       phase_ds = phase
       fs_new = fs
   ```
7. **Two separate bandpasses** — BR and HR:
   ```python
   b_br, a_br = butter(4, [0.08, 0.5], btype='band', fs=fs_new)
   b_hr, a_hr = butter(4, [0.7, 3.0],  btype='band', fs=fs_new)
   br_sig = filtfilt(b_br, a_br, phase_ds)
   hr_sig = filtfilt(b_hr, a_hr, phase_ds)
   ```
8. **Peak frequency via zero-padded Welch PSD** (each band):
   ```python
   nperseg = min(len(x), int(fs_new * 25))
   f, p = welch(x, fs=fs_new, nperseg=nperseg, noverlap=nperseg//2,
                nfft=8*nperseg, detrend='constant')
   mask = (f >= lo) & (f <= hi)
   peak_hz = f[mask][np.argmax(p[mask])]
   ```
9. **HR harmonic rejection — always run:**
   ```python
   f_sub = f_peak_hr / 2.0
   if 0.7 <= f_sub <= 3.0:
       p_sub = np.interp(f_sub, f, p)
       p_top = np.interp(f_peak_hr, f, p)
       if p_sub > 0.5 * p_top:
           f_peak_hr = f_sub   # peak was the 2nd harmonic
   hr_bpm = f_peak_hr * 60
   ```
   See [references/harmonic-pitfalls.md](references/harmonic-pitfalls.md) for why this matters and mitigations for slow-breather respiration harmonics leaking into the HR band.

10. **Cross-check with autocorrelation** — required; use it as the primary method for clips < 15 s:
    ```python
    # f_lo, f_hi = band edges of the band being cross-checked (HR: 0.7, 3.0; BR: 0.08, 0.5)
    ac = np.correlate(x - x.mean(), x - x.mean(), mode='full')
    ac = ac[len(ac)//2:] / ac[len(ac)//2]
    lag = int(fs_new/f_hi) + np.argmax(ac[int(fs_new/f_hi):int(fs_new/f_lo)])
    bpm_ac = 60 * fs_new / lag
    ```
    If `abs(bpm_ac - bpm_psd) > 5`, flag as low confidence.

## Critical rules

- Use phase, not magnitude: 1 mm motion at 24 GHz ≈ 1 rad; magnitude costs ~40 dB of SNR; `np.abs(iq)` is almost always wrong for mm-scale motion.
- Remove clutter before `np.angle`: the DC offset anchors phase off zero and eats the ±π unwrap budget.
- Decimate before sub-Hz bandpass: the SciPy biquad silently NaNs at very-low normalized cutoffs.
- Use two separate BR / HR bandpasses: HR is 10×–100× smaller than BR; a single wide filter can't separate them.
- Zero-pad the Welch PSD (`nfft=8*nperseg`): the raw bin spacing `fs/nperseg` is often coarser than tolerance.
- Always run the HR sub-harmonic check: the 2nd harmonic of the cardiac pulse frequently dominates the fundamental.
- Never `argmax(magnitude)` across all range bins (FMCW): the DC bin and static reflectors dominate; restrict to the subject-range window.

## Band edges: use these, not textbook 0.1–0.5 / 0.8–2.5

- BR lower: use **0.08 Hz (4.8 bpm)**, not the textbook 0.1 Hz (6 bpm), because slow breathers (supine, meditation, sleep) routinely fall below 6 bpm.
- HR lower: use **0.7 Hz (42 bpm)**, not the textbook 0.8 Hz (48 bpm), because bradycardia (athletes, post-tilt-down, β-blockers) falls below 48 bpm.
- HR upper: use **3.0 Hz (180 bpm)**, not the textbook 2.5 Hz (150 bpm), because post-exercise and children exceed 150 bpm.

Widen only with specific justification. See [references/band-rationale.md](references/band-rationale.md).

## Decision rules

- If `f_peak/2` is in the HR band and `p_sub > 0.5 × p_top`, pick the sub-harmonic (fundamental).
- If the PSD and autocorrelation disagree by more than 5 bpm, flag low confidence and don't commit to one value.
- If the BR estimate is below 10 bpm (slow breather), expect HR-band contamination — notch `2·BR` and `3·BR`; see [references/harmonic-pitfalls.md](references/harmonic-pitfalls.md).
- If HR > 150 bpm (tachycardia), widen the HR band upper edge to 3.3 Hz and re-estimate.
- If the subject is known to be exercising, use the 3.3 Hz upper edge from the start.
- If the clip is shorter than 15 s, PSD resolution exceeds tolerance — prefer autocorrelation, or flag inconclusive.

## Sanity checks before reporting

- **BR < HR** always for a live adult at rest. Violated ⇒ swapped bands.
- **HR × duration_minutes ≈ peak count in `find_peaks(bandpassed_hr)`.** Off by 2× ⇒ harmonic error slipped through.
- Resting adult plausibility: HR 50–90 bpm, BR 10–20 bpm. Way outside ⇒ re-check band edges, decimation, and harmonic rejection.

## Output Format

Report the results as:

- **HR: {N} bpm | BR: {N} bpm**
- **Parameters:** fs (post-decimation), band edges used per band, PSD window (nperseg/nfft), peak-selection method (PSD/autocorrelation/both)
- **Confidence:** for each rate, one of `high` (PSD and autocorrelation agree ≤5 bpm), `low` (disagree >5 bpm or clip <15 s — report the autocorrelation value and mark low), `inconclusive` (no reliable peak — state why)
- **Checks:** state the sanity checks passed (BR<HR; peak count vs HR×duration; plausibility bands)

If any result is low-confidence, say so in the same breath as the number — never present a flagged value as final.

## When things go wrong

If output looks like garbage, walk through [references/debugging.md](references/debugging.md) — fast checks that catch most ingestion and SNR bugs.

## Not in scope

- Pulse / UWB range-gated radar (different pipeline entirely).
- MIMO angle-of-arrival — needs beamforming first.
- Doppler-only gesture radar — use slow-time FFT, not bin phase.
- Arrhythmia / irregular rhythms — use R-peak / foot detection + RR-interval analysis, not PSD.
- Multiple subjects in one signal — run source separation first.
- Rapidly non-stationary rate (exercise ramp) — use a spectrogram, not single-window PSD.

