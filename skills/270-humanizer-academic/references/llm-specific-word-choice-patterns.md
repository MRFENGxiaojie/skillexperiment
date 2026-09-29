## LLM-SPECIFIC WORD CHOICE PATTERNS

### 19. Informal "linked to" Instead of Academic "associated with"

**Problem:** LLMs prefer the casual verb "linked to" over the more precise academic phrasing "associated with" or "reported to be associated with."

**Before:**
> EDS has been linked to shorter sleep duration, insomnia symptoms, depressive symptoms, and fatigue.

**After:**
> EDS has been reported to be associated with shorter sleep duration, insomnia symptoms, depressive symptoms, and fatigue.

**IMPORTANT — do NOT blanket-swap every "link" to "associated with".** Choose the verb that fits the context:
- **Noun "link"** (e.g., "the link between vulnerability and distress") — leave unchanged.
- **Data linkage** — use "merge"/"combine": "successfully linked with T2 data" → "successfully merged with T2 data".
- **Downstream consequence** ("leads to / results in") — use "lead to": "has been linked to reduced productivity" → "can lead to reduced productivity".
- **Reframe the whole clause** when more natural: "has been linked to reductions in patient experience and continuity of care" → "can compromise patient experience and continuity of care".

Use "associated with" only when the relationship is genuinely a statistical/observational association.

---

### 20. Overuse of "Beyond" as a Transition

**Problem:** LLMs frequently use "Beyond" to introduce additional points, which sounds informal and journalistic. In academic writing, "In addition to" is more standard.

**Before:**
> Beyond the association with sleep disturbances, EDS was also related to impaired daytime functioning.

**After:**
> In addition to the association with sleep disturbances, EDS was also related to impaired daytime functioning.

---

### 21. Overuse of "via" Instead of "through"

**Problem:** LLMs prefer the Latin shorthand "via" where "through" or "by means of" is more natural in academic prose.

**Before:**
> Informed consent was obtained via the online form.

**After:**
> Informed consent was obtained through an online form.

---

### 22. Overly Assertive Causal Claims (Insufficient Hedging)

**Problem:** LLMs tend to state causal or interventional implications too strongly, dropping hedging words that academic writing requires. In observational studies especially, appropriate epistemic caution is essential.

**Before:**
> Among young adults, addressing fatigue may reduce the risk of developing depressive symptoms.

**After:**
> Among young adults, addressing fatigue may help reduce the risk of developing depressive symptoms.

**Key principle:** For observational or speculative claims, soften the causal phrasing with an additional cushion word ("may help reduce", "could potentially contribute to") rather than stating it as near-direct causation ("may reduce", "can prevent"). This is NOT the same as the redundant multi-layer hedging in Pattern 17 — here, a two-word softening ("may help") is intentional and appropriate, whereas Pattern 17 targets excessive 4–5 layer stacking ("may suggest... have the potential to confer beneficial effects").

---

### 23. Artificially Condensed Expressions

**Problem:** LLMs compress complex ideas into unnaturally compact forms — either by packing nouns into dash-compounds or by substituting abstract shorthand for concrete explanations. Academic writing should be expanded and readable.

**Type A — Compressed noun-dash phrases:**

**Before:**
> a reinforcing fatigue–sleepiness cycle

**After:**
> a reinforcing cycle of fatigue and sleepiness

**Before:**
> the sleep–mood–cognition pathway

**After:**
> the pathway linking sleep, mood, and cognition

**Type B — Abstract shorthand without elaboration:**

**Before:**
> Bidirectional associations between screen use before sleep and weekday sleep duration suggest mutual reinforcement.

**After:**
> Bidirectional associations between screen use before sleep and weekday sleep duration suggest a potentially self-reinforcing cycle, with each behavior possibly exacerbating the other.

**Key principle:** When you encounter condensed expressions — whether dash-compounds or abstract terms like "mutual reinforcement," "bidirectional relationship," or "complex interplay" — expand them into readable phrasing that makes the meaning explicit.

---

### 24. Avoid "where" as a Non-locative Connector

**Problem:** LLMs frequently use "where" to tack on elaborating clauses (especially after a comma), even when no location or setting is involved. In academic medical writing, this reads as awkward and informal. Rewrite the sentence so the additional information is presented as an independent clause, a parenthetical, or a prepositional phrase instead.

**Before:**
> Interestingly, although men reported higher rates of generative AI use than women, women were overrepresented among those who used LLMs for emotional support, particularly at the most intensive level, where almost daily use was more than twice as common in women as in men.

**After:**
> Interestingly, although men reported higher rates of generative AI use than women, women were overrepresented among those who used LLMs for emotional support, with almost daily use more than twice as common in women as in men.

**Key principle:** Only keep "where" when it truly refers to a physical location, a dataset/cohort, or a well-defined conditional context (e.g., "in trials where blinding was not feasible"). When "where" is used simply as a loose connector to add detail, **prefer "with"** or restructure into a new clause. Avoid substituting "in which" as the default replacement — "in which" also reads as an LLM tell in academic prose, and a simple "with"-phrase, prepositional phrase, or new sentence is almost always more natural. Reserve "in which" for cases where no other construction works.

---

### 25. Avoid "yield" as a Result Verb

**Problem:** LLMs overuse "yield" (e.g., "yielded results", "did not yield estimates") to describe analytic outputs. In academic medical writing, more specific verbs such as "produce", "provide", "generate", or "fail to produce" read more naturally and precisely.

**Before:**
> RI-CLPM analyses did not yield stable, interpretable within-person cross-lagged estimates due to sparse transitions in ordinal predictors.

**After:**
> RI-CLPM analyses failed to produce stable, interpretable within-person cross-lagged estimates due to sparse transitions in ordinal predictors.

**Key principle:** Replace "yield/yielded" with a more precise verb that matches the context: "produce/produced", "provide/provided", "generate/generated", or "fail to produce" for negative results. Reserve "yield" for contexts where it is genuinely standard (e.g., chemical/biochemical yields).

---

### 26. Minor word-choice refinements (remain, given)

**"remain" → a be-verb** (more natural in most contexts):
- Before: However, these interpretations remain speculative.
- After: However, these interpretations are still speculative.

**"Given" → "due to"** when it introduces a reason:
- Before: ...are still speculative given the small sizes of the subgroup samples.
- After: ...are still speculative due to the small sizes of the subgroup samples.

---

### 27. Preserve logical discourse markers (do NOT over-trim connectives)

**Problem:** Aggressive AI-pattern removal can strip the connectives that carry a paper's logic, leaving choppy, hard-to-read prose. This is a common failure mode of automated humanizing. Logical discourse markers are NOT AI tells; they are hallmarks of good human academic writing, and removing them is itself a defect.

**Preserve (do not delete):** Although / Whereas / Thus / Hence / Thereafter / In contrast / Conversely / Based on these results / To that end / As expected / In agreement with previous reports / Over and above. A measured "not only ... but also ..." (about once per paragraph) is also natural and should be kept — this refines Pattern 9, which targets only its *overuse*, not a single natural instance.

**Distinguishing rule:** ask whether the phrase *inflates meaning* (delete) or *makes logic explicit* (keep).
- "underscores the pivotal importance of ..." → inflates meaning → delete (Patterns 1, 7).
- "Based on these results, we examined ..." → makes logic explicit → keep.

**Benchmark — the "sweet spot":** Well-written, pre-AI human papers chain discourse markers densely and naturally ("Based on these initial observations ... To that end ... As expected ... In agreement with previous reports ... Over and above the impact of [the main exposure] ...") while using ZERO inflated AI vocabulary. Aim for that profile: trim inflated vocabulary and significance puffery, but keep the logical connectives that make the argument easy to follow.

**Vary connectives by logical relation — but only to avoid near repetition, never for decoration.** When you add or rewrite a connective (per Pattern 30), first identify the logical relation the sentence actually needs, then choose a marker that fits it. If the same marker was just used nearby, substitute another from the *same* relation group so the prose does not repeat mechanically. Common groups:
- **Result / consequence:** thus, hence, therefore, consequently, accordingly
- **Addition:** moreover, furthermore, in addition (and "additionally" once per paragraph, per Pattern 7)
- **Contrast:** however, in contrast, conversely, on the other hand
- **Concession:** although, albeit, nonetheless, nevertheless, even though
- **Reason / grounds:** because, since, as, given that
- **Sequence / enumeration:** first / second, to begin with

**Guardrail (this is NOT an exception to Pattern 11):** vary connectives only when the relation is genuinely present and a near-repeat would otherwise occur. Do NOT sprinkle uncommon connectives (albeit, thereby, whereby, heretofore) to "sound human" — that is decoration, and it reads as artificial. Each connective must be earned by the logic of the sentence. Skilled human writers reach for "thus", "hence", "moreover", or "albeit" because the relation calls for it, not to diversify their vocabulary.

---

### 28. Re-contextualize over-condensed semantic links

**Problem:** LLMs compress a relation into an over-direct phrasing. Expand it into natural, contextualized wording.

- Before: These males may carry substantial unmet needs to discuss their difficulties.
- After: These males may carry substantial unmet needs when it comes to discussing their difficulties.

(See also Pattern 23 on artificially condensed expressions; Pattern 28 specifically targets over-direct *semantic* links rather than noun-dash compounds.)

---

### 29. Ornamental -ly intensifier adverbs

**Problem:** LLMs dress up sentences with -ly intensifiers that add emphasis but no information ("markedly reduced", "critically important", "remarkably consistent"). Human-written epidemiology papers use -ly adverbs almost exclusively *functionally*: to convey magnitude, frequency, direction, or calibration.

**Words to watch (ornamental — delete or downgrade):** markedly, remarkably, strikingly, dramatically, profoundly, critically, fundamentally, notably (as a mid-sentence adverb, e.g. "a notably higher rate"), significantly (with no statistical test behind it), increasingly, rapidly (figurative), uniquely, vastly, deeply, exceptionally, substantially (with no quantitative backing)

**Functional adverbs to KEEP (these carry information):** approximately, slightly, modestly, consistently, almost, only, largely, generally, relatively, "statistically significantly" / "differed significantly" (when an actual test result is being reported), substantially (when it refers to a real, stated effect-size difference)

**Decision rule:** Delete the adverb mentally and ask whether any information was lost. If nothing was lost, it was ornamental — delete it or replace the emphasis with the concrete number or comparison it was gesturing at. If it conveyed magnitude, frequency, direction, or calibration, it is functional — keep it.

**Before:**
> Patients with both conditions face a markedly reduced survival, and adherence is critically important. The effect was remarkably consistent across subgroups, and rates of heart failure are increasingly rising in this population.

**After:**
> Patients with both conditions have a median survival of approximately 4 years, and poor adherence worsens prognosis. The effect was consistent across subgroups, and the prevalence of heart failure in this population is rising.

**Benchmark — how well-written human papers use -ly adverbs:** In strong epidemiology writing, the -ly adverbs almost always quantify or calibrate rather than decorate. Typical examples read like "the highest-exposure group consistently had lower mortality risk", "the exposure slightly decreases along the gradient", or "the study showed a modest association between the exposure and better self-rated health". Each adverb ("consistently", "slightly", "modest") carries information about frequency, magnitude, or calibration; none merely decorates. Aim for that profile.

(Note: Pattern 1's example "markedly reduced median survival" is the same defect viewed as significance inflation; Pattern 29 generalizes it to all ornamental intensifiers.)

---

### 30. Connective-preserving edits (never bare-delete a transition)

**Problem:** When an AI-pattern sentence opener is removed (an "Additionally," beyond the once-per-paragraph allowance, an "-ing" tail per Pattern 3, significance inflation per Pattern 1), the logical relation it marked — addition, contrast, consequence — still exists between the sentences. Deleting the marker without replacing it produces bare, disconnected sentences (asyndeton). **Choppy, connective-stripped prose is itself a tell of automated AI cleanup**, and a known failure mode of humanizing passes.

**Rule: edit, don't excise.** Whenever you remove a sentence-initial transition or a clause that carried the link to the previous sentence, restore the link by one of:
1. Substituting a natural connective: "In addition," / "Moreover," / "However," / "By contrast," / "We also found that ..."
2. Echoing a key noun from the previous sentence at the start of the new sentence (old-to-new information flow): "... was associated with nonrestorative sleep. Nonrestorative sleep, in turn, ..."
3. Restructuring the two sentences into one with an explicit conjunction.

**Before (the AI text):**
> Additionally, empagliflozin reduced cardiovascular death, highlighting its cardioprotective effects. Additionally, the benefit appeared within months.

**Wrong fix (bare deletion — creates choppy asyndeton):**
> Empagliflozin reduced cardiovascular death. The benefit appeared within months.

**Right fix (connective preserved):**
> Empagliflozin also reduced cardiovascular death, and this benefit appeared within months of treatment initiation.

**Division of labor with Pattern 27:** Pattern 27 lists the discourse markers you must not *remove*; Pattern 30 governs what you must do when an edit *would otherwise leave a gap* — replace or restructure, never just cut.

---

### 31. Paragraph cohesion (old-to-new flow and paragraph-opening markers)

**Problem:** Sentence-level edits accumulate into paragraph-level damage: topic sentences get blunted, the chain from one sentence to the next breaks, and the contrast/continuity markers that tie paragraphs together disappear. Well-written human papers are tightly chained.

**What well-written human papers do:**
- **Within a paragraph**, each sentence picks up a key word from the previous one (old-to-new flow), e.g. "the exposure was associated with a higher functional score. The functional index used here consists of ... To perform these activities, ...". The repeated key term ("functional") chains the sentences so the reader is never dropped.
- **Between paragraphs**, the opening sentence names what the paragraph is about and, where the logic requires it, carries an explicit marker: "However, ...", "On the other hand, ...", "In addition to the differential effects described above, it is worth noting that ...", or "Taken together, the results suggest ...".

**Checklist (apply to every paragraph after editing):**
1. Does the first sentence state what the paragraph claims or covers?
2. From the second sentence on, is each sentence linked to the previous one by either a connective or an echoed key word? If a link was broken by an edit, restore it (Pattern 30).
3. Across paragraphs, are the contrast/continuity openers (However / In contrast / On the other hand / Overall / Taken together / In addition to X) still present where the argument needs them? Add one if a paragraph now starts abruptly.

---

### 32. Paraphrastic Repetition of the Same Claim

**Problem:** LLMs restate the same claim 2–3 times using different words within the same paragraph or across adjacent sentences, often joined by "In other words," "That is," "Put differently," or "Essentially,". Each sentence should advance the argument, not rephrase the previous one.

**Words to watch:** In other words, That is, Put differently, Essentially, To put it another way, Simply put, This means that (when followed by a near-verbatim restatement)

**Before:**
> These findings suggest that sleep disturbance is associated with depressive symptoms. In other words, poor sleep quality may contribute to the development of depression. That is, disrupted sleep patterns appear to play a role in mood disorders.

**After:**
> These findings suggest that sleep disturbance is associated with depressive symptoms.

**Before:**
> Empagliflozin reduced the risk of cardiovascular death. Put differently, patients treated with empagliflozin had a lower likelihood of dying from cardiovascular causes. Essentially, the drug conferred a survival benefit.

**After:**
> Empagliflozin reduced the risk of cardiovascular death.

**Key principle:** State each claim once. If a second sentence follows, it should add new information (a mechanism, a comparison, a qualification), not repackage the same assertion in different vocabulary. When removing paraphrastic repetitions, keep the version that is most specific or most precisely worded and delete the rest. Apply Pattern 30 (connective-preserving edits) if deletion would break the logical flow to the next sentence.

**EXCEPTION:** Genuine clarification of a technical term is not paraphrastic repetition. "The hazard ratio was 0.65, meaning that empagliflozin reduced the event rate by 35% relative to placebo" adds information by translating a statistical metric into a clinical interpretation. The problem is when the "clarification" says the same thing in equally vague terms.

---

### 33. Content-free Evaluation Sentences

**Problem:** LLMs insert standalone sentences that evaluate a finding's importance without adding any information — no data, no mechanism, no comparison, just a verdict of significance. These are distinct from Pattern 1 (significance inflation embedded within data-bearing sentences) and Pattern 3 (-ing tails appended to factual sentences); Pattern 33 targets freestanding evaluation sentences that contain nothing but the evaluation itself.

**Words to watch:** This is an important/significant/noteworthy finding. These results are of clinical/public health significance. This observation is clinically relevant. This finding has important implications. This is a meaningful/notable result. This deserves attention.

**Before:**
> Empagliflozin reduced cardiovascular death by 38%. This is a noteworthy finding. The benefit was consistent across subgroups. This observation is of clinical significance.

**After:**
> Empagliflozin reduced cardiovascular death by 38%, and the benefit was consistent across subgroups.

**Key principle:** If the finding is genuinely significant, show why: state the mechanism, the clinical consequence, or the contrast with prior evidence. A sentence that merely labels a finding as "important" without explaining what makes it important adds no information and should be deleted. When deleting, apply Pattern 30 (connective-preserving edits) to maintain flow.

**EXCEPTION:** An evaluation sentence is acceptable when it immediately follows up with a specific reason: "This finding is clinically relevant because it identifies patients who may benefit from earlier intervention." Here, the evaluation carries forward into a concrete implication. The standalone, terminal evaluation ("This is important." Full stop.) is the problem.

---

### 34. Sentence Rhythm and Structural Diversity (Burstiness)

**This is the single highest-impact intervention for reducing AI-detection scores.** Experimental testing (desklib logit 5.54→2.47, a 55% reduction) showed that restructuring sentence rhythm alone accounts for ~90% of the achievable improvement, more than all vocabulary-level edits combined. Apply this pattern BEFORE vocabulary-level fixes.

**Problem:** AI-generated text converges on a narrow band of sentence lengths (typically 15-25 words) with uniform sentence-opening structures (Subject-Verb-Object repeating). Human writing has "burstiness": a mix of short and long sentences, with varied openings. AI detection models (both classifier-based and perplexity-based) key on this uniformity as a primary signal.

**What to change (structure only, not vocabulary):**
1. **Vary sentence length.** Break one long sentence into two shorter ones. Combine two short sentences into one longer one with a conjunction or semicolon. Aim for a mix: some sentences under 15 words, some over 30.
2. **Diversify sentence openings.** If three consecutive sentences start with a noun-phrase subject, restructure one to open with a prepositional phrase ("In this meta-analysis,"), a subordinate clause ("Although the sample was small,"), a connective ("However,"), or an adverbial ("Importantly,").
3. **Relocate clause elements.** Move a qualifying phrase from the end to the beginning, or vice versa: "In patients over 65, the risk was elevated" vs. "The risk was elevated in patients over 65."
4. **Use semicolons to join related clauses** instead of always using periods or conjunctions. This is a characteristic of skilled human academic writing.

**What NOT to change:**
- Do not alter technical vocabulary, data, or meaning
- Do not introduce staccato drama (multiple very short sentences in a row for rhetorical effect)
- Do not break the connective structure (Pattern 27/30/31 still apply)
- Do not change the voice (active/passive) of the original unless Pattern 9 applies

**CRITICAL INTERACTION with Pattern 29 (ornamental adverbs):** Deleting an adverb like "markedly" without restructuring the sentence was experimentally shown to INCREASE AI-detection scores (logit +0.72 worse). The adverb removal creates a shorter, more uniform sentence that fits the AI cadence better. **Always restructure the sentence when removing an ornamental adverb** — e.g., split it, merge it with the next sentence, or reposition clauses.

**Before (uniform rhythm, all sentences 18-22 words):**
> All three DACS had elevated PRRs for pantry overflow compared with comparator services. PRRs for bean hoarding were markedly higher for DACS than for comparators. Four of eight comparator services had no bean hoarding reports whatsoever. The remaining four comparator services had PRRs that were below one.

**After (varied rhythm: 15, 28, 18 words):**
> All three DACS had elevated PRRs for pantry overflow compared with comparator services (PRR <= 2.07). PRRs for bean hoarding were higher (MorningHarbor 77.89, CopperKettle 3.92, DailyGrind 3.24). Four of eight comparator services had no bean hoarding reports, and the remaining four had PRRs below 1.

**Benchmark:** In well-written human medical papers, sentence lengths within a single paragraph range from 12 to 55 words, with standard deviations of 10-15 words. AI-generated paragraphs typically have standard deviations under 5 words. After humanizing, check that the paragraph contains at least one sentence notably shorter and one notably longer than the average.

---