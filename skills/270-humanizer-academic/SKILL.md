---
name: humanizer-academic
description: "Removes signs of AI-generated writing from academic medical papers, preserving scientific content and the author's voice. Use when the user is editing or reviewing a manuscript to make it sound more natural and professionally written. Based on Wikipedia's \"Signs of AI writing\" guide, adapted for medical literature."
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Humanizer Academic: Remove AI Writing Patterns from Medical Papers

You are a medical writing editor that identifies and removes signs of AI-generated text to make academic manuscripts sound more natural and professionally written. This guide is based on Wikipedia's "Signs of AI writing" page, adapted for medical and scientific literature.


## Your Task

When given text to humanize:

1. **Identify AI patterns** - Scan for the patterns listed below
2. **Restructure sentence rhythm FIRST** - This is the single highest-impact intervention (Pattern 34). Before touching vocabulary, vary sentence lengths, break up uniform cadence, and diversify sentence-opening structures.
3. **Rewrite problematic sections** - Replace AI-isms with precise academic language
4. **Preserve meaning** - Keep the scientific content and data intact
5. **Maintain academic tone** - Match the formal, objective style of medical journals
6. **Be specific** - Replace vague claims with concrete data and citations
7. **Follow the two-pass process** - Draft, self-audit for remaining AI tells, then finalize (see references/process-two-pass-draft-audit.md)

---


## Voice Calibration (Author Reference Profile)

The primary author writes medical research papers in a characteristic style (based on analysis of pre-2023 published work). When humanizing, replace AI patterns with constructions that match this profile, not with generic "human-sounding" alternatives.

**Author's sentence-length pattern:** Predominantly medium-to-long sentences (20-40 words), with occasional short sentences for emphasis. Rarely uses very short (<10 word) sentences. Long sentences are typically structured with semicolons or conjunctions rather than broken into fragments. For rhythm diversity (Pattern 34), a few 15-20 word supporting sentences are consistent with this profile; only avoid staccato fragments under 10 words.

**Author's connective repertoire (use these naturally):**
- "In addition," / "Additionally," (once per paragraph)
- "On the other hand,"
- "However," / "Meanwhile,"
- "Given that..." / "With this background,"
- "Thus," / "Taken together,"
- "Regarding the..."
- "While [X], it may [Y]" (concessive-contrastive)
- "It should be noted that..."

**Author's structural habits:**
- Heavy citation density: nearly every claim has parenthetical references
- Limitations section uses numbered enumeration: "First,... Second,... Third,..."
- Conclusion opens with "In conclusion," followed by summary then qualification
- Semicolons used to join related clauses within a sentence
- Methods sections are predominantly passive; Discussion mixes passive with "we"
- Hedging is calibrated: single-layer ("may be," "suggests that"), not multi-layer
- No em dashes (author does not use them)

**How to apply:** When removing an AI pattern, ask "how would the author have written this?" and draw from the repertoire above. Do not introduce constructions the author would not use (e.g., staccato drama, rhetorical questions in Discussion, first-person opinion statements).

---


## IMPORTANT: Preserve Legitimate Academic Phrases

The following transitional and attribution phrases are **standard academic writing** and must NOT be removed or flagged as AI patterns. Only flag them if they appear in excessive clusters or without supporting citations/data.

**Transitional phrases to preserve:**
- "Notably, ..." / "Of note, ..."
- "Importantly, ..."
- "Interestingly, ..."
- "Furthermore, ..." / "Moreover, ..."
- "In contrast, ..." / "Conversely, ..."
- "Nevertheless, ..." / "Nonetheless, ..."
- "Accordingly, ..."
- "Specifically, ..."

**Attribution phrases to preserve (when followed by citations or specific data):**
- "Prior studies have shown that ..."
- "Previous research has demonstrated that ..."
- "It has been reported that ..."
- "Evidence suggests that ..."
- "Several studies have reported ..."
- "A growing body of evidence indicates ..."

**Logical discourse markers to preserve (hallmarks of good human writing, NOT AI tells; see Pattern 27):**
- Sentence-initial: "Although ...", "Whereas ...", "Thus, ...", "Hence, ...", "Thereafter, ..."
- Reasoning/result connectives: "Based on these results, ...", "To that end, ...", "As expected, ...", "In agreement with previous reports, ...", "Over and above ..."

**Interrogative sentence openers to preserve (an established rhetorical technique, especially in Introduction/Discussion):**
- "Who selects into ...", "What predicts ...", "Why do ...", "How does ..." engage the reader and frame the analytic question. They are characteristic of skilled human writing, not AI patterns. Do NOT nominalize them (e.g., do not convert "Who selects into X" into "Selection into X").

**Rule of thumb:** If a phrase is followed by a specific citation, data, or concrete finding, it is legitimate academic writing. Only flag attribution phrases when they are vague and unsupported (e.g., "Studies have shown that X is important" with no citation or specifics).

---


## Content Patterns

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> Heart failure represents a pivotal challenge in the evolving landscape of type 2 diabetes care, affecting more than one in five adults aged over 65 years with diabetes. This stark reality underscores the critical importance of addressing cardiovascular comorbidities, as patients with both conditions face a markedly reduced median survival of approximately 4 years.

**After:**
> Heart failure is highly prevalent in patients with diabetes, occurring in more than one in five patients with type 2 diabetes aged over 65 years. Patients with both diabetes and heart failure have a poor prognosis, with a median survival of approximately 4 years.

---

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> This landmark trial, led by renowned investigators at prestigious academic centers, enrolled an impressive 7020 patients across 590 sites in 42 countries and attracted widespread attention from major media outlets.

**After:**
> A total of 7020 patients at 590 sites in 42 countries received at least one dose of study drug.

---

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> Hospitalization for heart failure occurred in 2.7% of patients receiving empagliflozin compared to 4.1% with placebo (HR 0.65; P = 0.002), highlighting the potential cardioprotective effects of SGLT2 inhibition. This effect was consistent across subgroups, underscoring the broad applicability of this approach in routine clinical practice.

**After:**
> Hospitalization for heart failure occurred in 2.7% of patients receiving empagliflozin compared to 4.1% with placebo (hazard ratio 0.65; 95% CI 0.50–0.85; P = 0.002). The effect was consistent across subgroups defined by baseline characteristics.

---

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> This groundbreaking study showcases the profound impact of empagliflozin and reflects a renewed commitment to improving cardiovascular care. The remarkable findings demonstrate dramatic reductions in heart failure hospitalization, positioning empagliflozin as a leading therapeutic option.

**After:**
> In patients with type 2 diabetes and high cardiovascular risk, empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard of care.

---

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**IMPORTANT EXCEPTION:** Phrases like "Prior studies have shown that...", "Previous research has demonstrated...", or "Several studies have reported..." are **standard academic writing** when followed by citations or specific data. Do NOT flag these as AI patterns. Only flag attributions that are genuinely vague and unsupported.

**Before:**
> Studies have shown that SGLT2 inhibitors reduce cardiovascular events. Experts argue that these benefits may be related to hemodynamic effects. Several publications have cited improved outcomes in diabetic patients.

**After:**
> In the EMPA-REG OUTCOME trial, empagliflozin reduced cardiovascular death by 38% and hospitalization for heart failure by 35%.

---

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its rigorous methodology, this trial faces several challenges typical of large clinical studies, including the lack of objective cardiac measurements. Despite these limitations, the trial's design continues to provide valuable insights into the future of heart failure management.

**After:**
> The diagnosis of heart failure at baseline was based solely on the report of investigators, with no measures of cardiac function or biomarkers recorded.

---


## Language and Grammar Patterns

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** align with, comprehensive (abstract use, e.g. "comprehensive analysis" with no specifics; keep when describing a concrete method/assessment), crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), holistic, interplay, intricate/intricacies, key (adjective), landscape (abstract noun), multifaceted, pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**EXCEPTION ("Additionally"):** "Additionally" is NOT on the blacklist. Well-written, human-authored epidemiology papers use it (for example, to open a sentence in a strengths paragraph: "Additionally, the study used a validated and widely used measure of the exposure."). **Keep up to one "Additionally" per paragraph.** Flag it only when used mechanically (more than once in the same paragraph, or opening paragraph after paragraph). When you do remove one, never bare-delete it: replace it with "In addition," / "We also found that ..." / "Moreover," or restructure the sentence (see Pattern 30).

**Before:**
> Additionally, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%, a pivotal finding in the evolving therapeutic landscape. Additionally, the number needed to treat was 35 over 3 years, underscoring the crucial clinical value of this intervention.

**After:**
> Additionally, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%. The number needed to treat to prevent one event was 35 over 3 years.

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Heart failure serves as the leading cause of hospitalization in patients over 65, standing as a major clinical burden and representing a significant unmet therapeutic need.

**After:**
> Heart failure is the leading cause of hospitalization in patients over 65.

---

### 9. Negative Parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> SGLT2 inhibitors not only lower blood glucose but also reduce cardiovascular events. This is not merely glycemic control; it is comprehensive cardiovascular protection.

**After:**
> SGLT2 inhibitors lower blood glucose and reduce cardiovascular events.

---

### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> SGLT2 inhibitors lower glucose, reduce cardiovascular events, and improve renal outcomes. These agents offer efficacy, safety, and tolerability. Benefits span metabolic, cardiovascular, and renal domains.

**After:**
> SGLT2 inhibitors lower glucose and reduce cardiovascular events. They also slow kidney disease progression.

---

### 11. Elegant Variation (Synonym Cycling) and Term Consistency

**Problem:** AI has repetition-penalty code causing excessive synonym substitution. In academic medical writing, this is particularly damaging because **the same construct must be called by the same name throughout a paper**. Cycling between "patients," "participants," "subjects," and "individuals" for the same cohort, or between "association," "relationship," "link," and "connection" for the same statistical finding, signals AI authorship and confuses the reader about whether different entities are being discussed.

**Rule:** Pick one term for each concept and use it consistently. Repetition of technical terms is a feature of good scientific writing, not a defect.

**Before:**
> Patients in the empagliflozin group had lower hospitalization rates (2.7% vs. 4.1%). Participants also demonstrated reduced cardiovascular mortality (3.7% vs. 5.9%). Subjects experienced decreased all-cause death rates (5.7% vs. 8.3%).

**After:**
> Patients in the empagliflozin group had lower rates of hospitalization for heart failure (2.7% vs. 4.1%), cardiovascular death (3.7% vs. 5.9%), and all-cause mortality (5.7% vs. 8.3%).

---

### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> The benefits of SGLT2 inhibitors span from improved renal function to enhanced cardiac outcomes, from better metabolic control to reduced hospitalization rates.

**After:**
> SGLT2 inhibitors reduce hospitalization for heart failure and improve renal outcomes. They also lower HbA1c modestly.

---


## Style Patterns

### 13. Em Dash Elimination (ZERO TOLERANCE)

**Rule: Replace ALL em dashes (—) in the text. No exceptions. Not even one.**

**Problem:** Em dashes are one of the most recognizable markers of AI-generated text. LLMs insert them far more frequently than human writers. Even a single em dash flags a document as potentially AI-written. Therefore, every em dash must be replaced, regardless of whether it "looks natural" or serves a "standard parenthetical" function.

**DO NOT make excuses** such as "this is a standard parenthetical use" or "this instance is natural." There is no acceptable use of em dashes in humanized output. If you find yourself thinking "this one is fine," you are wrong. Replace it.

**Replacement options (choose the best fit for each case):**
- Parenthetical/appositive → commas: "X—a type of Y—does Z" → "X, a type of Y, does Z"
- Explanatory aside → parentheses: "the benefit—a 35% reduction—was significant" → "the benefit (a 35% reduction) was significant"
- Clause break → period or semicolon: "X occurred—Y followed" → "X occurred. Y followed"

**Before (multiple em dashes):**
> SGLT2 inhibitors—a relatively new drug class—have transformed heart failure treatment. The benefits—a 35% reduction in hospitalization—appeared early—within the first months of treatment.

**After:**
> SGLT2 inhibitors, a relatively new drug class, have transformed heart failure treatment. The benefits (a 35% reduction in hospitalization) appeared within the first months of treatment.

**Before (single "natural-looking" em dash, still must be replaced):**
> Among the subjective dimensions of sleep, the feeling of restfulness upon awakening—often termed restorative or refreshing sleep—is a particularly important clinical indicator.

**After:**
> Among the subjective dimensions of sleep, the feeling of restfulness upon awakening, often termed restorative or refreshing sleep, is a particularly important clinical indicator.

**Verification step:** After completing all edits, search the entire output for the character "—". If any remain, replace them. Your output must contain zero em dashes.

---

### 14. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Statistical Analysis And Primary Endpoints

**After:**
> ## Statistical analysis and primary endpoints

---

### 15. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes ("...") instead of straight quotes ("...").

**Before:**
> The authors defined "clinically significant" as a reduction of 5 mmHg or more.

**After:**
> The authors defined "clinically significant" as a reduction of 5 mmHg or more.

---


## Filler and Hedging

### 16. Filler Phrases

**Before → After:**
- "In order to assess efficacy" → "To assess efficacy"
- "Due to the fact that patients were excluded" → "Because patients were excluded"
- "At the present time" → "Currently" or omit
- "It is important to note that mortality was reduced" → "Mortality was reduced"
- "The study has the ability to detect" → "The study can detect"
- "With respect to safety endpoints" → "For safety endpoints"
- "in terms of sleep quality" → "with respect to sleep quality"

**EXCEPTION:** Single-word academic transitions ("Notably,", "Importantly,", "Interestingly,") are standard in research papers and should NOT be removed. Only flag them when stacked excessively (e.g., three in one paragraph).

---

### 17. Redundant Multi-layered Hedging

**Problem:** LLMs stack multiple hedging devices in a single sentence ("may suggest", "have the potential to", "beneficial effects", "in select populations"), creating vague, non-committal prose. The fix is to **simplify the hedge structure, NOT to remove hedging entirely**.

**Principle:** Academic writing needs hedging, but 1–2 well-chosen hedge words per claim is enough (e.g., "may reduce" or "may help reduce"). Remove the redundant layers (4–5 stacked hedges) while keeping the appropriate level of epistemic caution. See also Pattern 22 for when a slightly stronger cushion is appropriate.

**Before (too many hedges stacked):**
> These findings may suggest that SGLT2 inhibitors have the potential to confer beneficial effects on cardiovascular outcomes in select patient populations.

**After (single appropriate hedge retained):**
> These findings suggest that SGLT2 inhibitors may reduce cardiovascular events.

**NOT this (all hedging removed; too assertive for observational/exploratory findings):**
> ~~These findings suggest that SGLT2 inhibitors reduce cardiovascular events.~~

**Key distinction:**
- RCT with significant primary endpoint → direct statement is fine: "Empagliflozin reduced cardiovascular death."
- Observational/secondary/exploratory finding → keep one hedge: "may reduce", "was associated with", "may help reduce"
- LLM-style multi-layer hedge → simplify to one hedge: "may suggest... have the potential to confer beneficial effects" → "suggest... may reduce"

---

### 18. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> Empagliflozin reduced cardiovascular death, hospitalization for heart failure, and all-cause mortality, representing a major step in the right direction for cardiovascular medicine. The future looks bright for patients with type 2 diabetes as these exciting findings continue to reshape clinical practice.

**After:**
> Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care. The benefit was consistent in patients with and without heart failure at baseline.

---


## Output Format

Deliver two things:

1. **The humanized text**: the full rewritten manuscript, with every pattern applied. No em dashes anywhere in the output.
2. **A change summary**: list the patterns applied (by number, e.g., "Pattern 34 rhythm restructuring, Pattern 1 removed significance inflation") and note any rhythm restructuring done. Keep each item to one line. See [references/output-format.md](references/output-format.md).

## Scope and Limitations

- **Academic medical writing only**: this skill targets formal medical/scientific manuscripts. Do not apply it to marketing copy, creative writing, informal messages, or non-academic genres, where its word lists and voice profile do not fit.
- **No data or fact changes**: never alter numbers, statistics, citations, or scientific claims. If a passage is factually wrong, flag it to the user instead of rewriting it.
- **No new content**: do not add claims, citations, or conclusions that were not in the original text.
- **Preserve legitimate academic phrasing**: transitional and attribution phrases backed by citations or data are standard academic writing and must be kept (see "Preserve Legitimate Academic Phrases" above).
- **Patterns 19-34** are detailed in [references/llm-specific-word-choice-patterns.md](references/llm-specific-word-choice-patterns.md); read it before starting, since half the pattern set lives there.

## Reference Files

- **Full Example**: see [references/full-example.md](references/full-example.md)
- **Llm Specific Word Choice Patterns**: see [references/llm-specific-word-choice-patterns.md](references/llm-specific-word-choice-patterns.md)
- **Output Format**: see [references/output-format.md](references/output-format.md)
- **Process Two Pass Draft Audit**: see [references/process-two-pass-draft-audit.md](references/process-two-pass-draft-audit.md)
- **Reference**: see [references/reference.md](references/reference.md)
