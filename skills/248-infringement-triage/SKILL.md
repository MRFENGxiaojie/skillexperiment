---
name: infringement-triage
description: Infringement triage across trademark, copyright, patent, and trade secret — a flag list with the factors cutting each way, not a finding. Use when assessing whether someone is infringing the user's IP or whether the user might be infringing another's, when a knockoff or copycat surfaces, or when deciding whether a matter is worth pursuing and how.
allowed-tools: Read, Write, Bash, Glob
argument-hint: "[describe the facts and which right — or just the facts and I'll ask which right]"
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Infringement Triage

**This is a triage, not a finding of infringement or non-infringement.**
Infringement analysis is fact-intensive and legally complex. Acting on a
triage — sending a cease-and-desist, refusing to stop, filing suit, or
deciding not to — without attorney review is how companies end up on the
wrong side of fee awards, Rule 11 sanctions, declaratory-judgment actions,
and (for patents) treble damages.


## Instructions

1. Read the practice profile: if `claude-for-legal/ip-legal/CLAUDE.md` exists in
   the current working directory, read that one; otherwise read
   `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`. If it
   contains `[PLACEHOLDER]`, stop and direct to `/ip-legal:cold-start-interview`.
2. Follow the workflow below.
3. Ask which right is at issue — trademark / copyright / patent / trade secret
   / mixed. If mixed, run each separately; do not blend.
4. Run common intake (party posture — senior or accused, jurisdiction, timing,
   exhibits).
5. Walk the mode-specific factors:
   - **Trademark** — circuit's confusion test + dilution (if famous) +
     false advertising (if a comparative claim).
   - **Copyright** — ownership + registration + access + substantial
     similarity + fair use + DMCA safe harbor (if applicable).
   - **Patent** — claim-chart first pass (route to `/ip-legal:fto-triage` output
     structure); literal + DOE; indirect + divided; invalidity defenses to
     consider.
   - **Trade secret** — secrecy + reasonable measures + misappropriation;
     preemption + reverse-engineering flags.
6. Produce a flag list with direction — what cuts toward the senior party,
   what cuts toward the accused, what's mixed. Never conclude.
7. Write the triage memo to the matter folder or practice outputs folder. Apply
   the work-product header per role.
8. End with recommended next steps, the non-lawyer gate if the role is
   non-lawyer, and — if the practice posture supports assertion — an offer to
   draft the C&D via `/ip-legal:cease-desist` or the takedown via
   `/ip-legal:takedown`. Do not draft automatically.

This skill never concludes. If uncertain, flag — the attorney decides.


## Examples

```
/ip-legal:infringement-triage "competitor launched a tool called APEXSEED in class 9 — we have APEXLEAF registered in class 9; likely confusion?"
```

```
/ip-legal:infringement-triage "former engineer took notes on our model architecture to a competitor — possible trade secret?"
```

```
/ip-legal:infringement-triage "a competitor claims our new release infringes their patent — we don't think it does"
```

```
/ip-legal:infringement-triage
```

(And the skill will ask which right and for the facts.)

---


## THIS IS A TRIAGE, NOT A FINDING

**The loudest guardrail in the plugin. Say this at the top of every output. Do
not drop it. Do not soften it.**

> **This is a triage, not a finding of infringement or non-infringement.**
> Infringement analysis is fact-intensive and legally complex. The triage
> identifies the factors and flags the ones that matter most; it does not
> conclude. A conclusion that something does or does not infringe is a legal
> opinion that requires an attorney's judgment on the facts, the claim or
> right scope, the relevant jurisdiction's law, and the likely defenses.
> Acting on a triage — sending a cease-and-desist, refusing to stop, filing
> suit, or deciding not to — without attorney review is how companies end up
> on the wrong side of fee awards, Rule 11 sanctions, declaratory-judgment
> actions, and (for patents) treble damages.

Under-calling a conflict is a one-way door — a C&D not sent and a mark goes
generic in the market; a claim not chased and the statute of limitations runs;
a copied copyrighted work kept on the site. Over-calling is a two-way door —
the attorney narrows. Stay on the two-way door side.

---


## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/ip-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-legal/ip-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

Infringement triages often lead into cease-and-desist drafting or takedown
routing. Open a matter if one isn't active and the practice is private — the
triage, the C&D, and any downstream response belong in one workspace.

---


## Load the practice profile first

Read the practice profile (working-directory `claude-for-legal/ip-legal/CLAUDE.md`
if present, otherwise `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`). Pull:

- **Role** from `## Who's using this`.
- **Enforcement posture** from `## Enforcement posture` — the triage output
  should end with a routing suggestion consistent with the stated posture
  (aggressive / measured / conservative) and the named approver for the
  relevant letter type.
- **Registered in / enforce where** from `## IP practice profile` — determines
  which circuit / jurisdiction test to apply by default.
- **Integrations** from `## Available integrations` — CourtListener,
  Solve Intelligence each affects whether the triage can cite to case law,
  prior rulings, or prior art.
- **Decision posture** from `## Decision posture on subjective legal calls` —
  this skill never concludes on a subjective threshold.

If the config has `[PLACEHOLDER]`, surface this bounce:

> I notice you haven't configured your practice profile yet — that's how I tailor posture, jurisdictions, and approval chain to your practice.
>
> **Two choices:**
> - Run `/ip-legal:cold-start-interview` (2 minutes) to configure your profile, then I'll run this tailored to YOUR practice.
> - Say **"provisional"** and I'll run this against generic defaults — US jurisdiction, middle risk appetite, lawyer role, no playbook — and tag every output `[PROVISIONAL — configure your profile for tailored output]` so you can see what I do before committing.

### Provisional mode

If the user says "provisional," run the infringement triage normally using these generic defaults: middle risk appetite, lawyer role, US jurisdiction, no playbook (do the full analysis rather than matching against a position list). Tag the reviewer note and every finding block with `[PROVISIONAL]`. At the end of the output, append:

> "That was a generic run against default assumptions. Run `/ip-legal:cold-start-interview` to get output calibrated to YOUR practice — your playbook, your jurisdiction, your risk appetite. 2 minutes."

---


## Mode selection

Ask at the top, before anything else:

> Which right are we triaging?
>
> 1. **Trademark** — confusion, dilution, or false advertising
> 2. **Copyright** — substantial similarity, fair use, DMCA safe harbor
> 3. **Patent** — claim-chart first pass, literal read + doctrine of equivalents
> 4. **Trade secret** — secrecy, reasonable measures, misappropriation
> 5. **Mixed / not sure** — describe the facts and I'll pick

If the user picks "not sure," help them sort. The same facts can implicate
multiple rights (e.g., a competitor's product uses our logo — trademark; and
the product is a near-copy of ours — possible patent, copyright on packaging,
possible trade dress; and a former employee launched it — trade secret).

**If more than one right is in play, run the triage for each, separately.**
Don't mash them together. Each right has different factors, different
jurisdictional rules, and different remedies.

---


## Intake (common to all modes)

> Before I walk factors:
>
> 1. **Posture.** Are you the potentially senior party (they're taking
>    yours) or the potentially accused party (we're the ones being looked at)?
>    The factors are symmetric but the output differs — a "mine's being
>    copied" triage routes toward an assertion letter; a "we might be
>    exposed" triage routes toward a risk memo.
> 2. **Jurisdiction.** Which country / circuit / court? US federal default if
>    not specified. Flag if foreign law may apply.
> 3. **Timing.** Is a statute of limitations or laches clock running?
> 4. **What exhibits / evidence / source documents do you have?** A screenshot,
>    a URL, a packaging photo, a code excerpt, an ex-employee contract.

Proceed through the factors once the inputs are available; flag gaps explicitly.

---


## Trademark mode

### Confusion

Use the applicable circuit's multi-factor test. Cite the test (du Pont /
Polaroid / Sleekcraft / other — see the `/ip-legal:clearance` skill for the
case citations and pick logic). Walk each factor and flag what cuts each way.

- **Similarity of marks** — sight / sound / meaning / commercial impression.
- **Similarity of goods or services** — expected-source test, not identity.
- **Channels of trade.**
- **Consumer sophistication.**
- **Strength of the senior mark** — fanciful / arbitrary / suggestive /
  descriptive with secondary meaning / generic.
- **Intent** — evidence of copying, knock-off trade dress, near-miss mark.
- **Actual confusion** — any evidence (surveys, misdirected inquiries, social).
- **Likelihood of expansion / bridge-the-gap** — whether the zones overlap
  commercially.

### Dilution

Apply the federal TDRA (15 U.S.C. § 1125(c)) and any applicable state statute.

- **Fame threshold.** The senior mark must be famous to the general consuming
  public — a niche-famous mark is not enough. *Starbucks Corp. v. Wolfe's
  Borough Coffee, Inc.*, 588 F.3d 97 (2d Cir. 2009) is representative.
- **Blurring vs. tarnishment.** Blurring = distinctiveness harm; tarnishment
  = reputation harm.
- **Defenses** — comparative advertising, news reporting, fair use,
  non-commercial use.

If the senior mark is not plainly famous nationally, flag dilution as a
stretch.

### False advertising / comparative claims

If the triage is prompted by a competitor's comparative ad or a claim about
product attributes:

- Apply Lanham Act § 43(a) / 15 U.S.C. § 1125(a) for the materiality,
  falsity-or-misleading, deception, commercial-speech, and injury elements.
- Flag whether the statement is literally false, implicitly false, or
  puffery. Puffery is not actionable.
- Substantiation evidence the claimant has or needs.

### Output

Factors table; what cuts each way; a "not a finding" conclusion line. End with
a routing suggestion against the enforcement posture in the practice profile.

---


## Copyright mode

### Ownership

Is the claimant the owner (or exclusive licensee with standing)? Work-for-hire
issues; joint authorship; assignments; and termination rights all flag.

### Registration

17 U.S.C. § 411 requires registration (or preregistration) as a precondition
to filing an infringement action in US federal court. *Fourth Estate Public
Benefit Corp. v. Wall-Street.com, LLC*, 586 U.S. 296 (2019) — registration
means actually issued, not just applied for. Flag registration status; if
not registered, flag the practical bar on filing.

### Access + substantial similarity

Two paths to proving copying:

- **Access + probative similarity** — defendant had access and the works share
  features probative of copying.
- **Striking similarity** — even absent proof of access, the similarity is so
  striking that independent creation is unlikely.

For substantial similarity, apply the circuit's test (Second Circuit's
ordinary-observer; Ninth Circuit's extrinsic / intrinsic under *Krofft* and
*Swirsky*; Fourth / Seventh / Eleventh circuits' variations). Flag which
test applies.

### Fair use

17 U.S.C. § 107 four factors, analyzed as a whole:

1. Purpose and character of the use (transformativeness; commercial vs.
   non-commercial).
2. Nature of the copyrighted work (factual / functional vs. creative).
3. Amount and substantiality of the portion used.
4. Effect on the market for the original.

Recent touchstones: *Google LLC v. Oracle America, Inc.*, 593 U.S. 1 (2021);
*Andy Warhol Found. for the Visual Arts, Inc. v. Goldsmith*, 598 U.S. 508
(2023). Flag the transformativeness analysis carefully — *Warhol* narrowed
the scope of transformative use and is still being applied by lower courts.

### DMCA safe harbor

17 U.S.C. § 512. If the accused is a service provider hosting user content,
flag whether § 512(c) applies: designated agent, notice-and-takedown
procedure, no actual or red-flag knowledge, no financial benefit
attributable to infringement the provider could control, expeditious
takedown on valid notice. Repeat-infringer policy required. Safe harbor does
not cover direct infringement by the service provider itself.

### Output

Factors flagged; fair-use balance with "the triage does not conclude";
ownership / registration / safe-harbor threshold notes. Routing per posture.

---


## Patent mode

**Route to `/ip-legal:fto-triage` for the detailed framework.** This mode is the
mirror image of the FTO skill — same claim charts, same doctrine-of-equivalents
flag, same all-elements rule — applied to an accused product instead of one's
own.

### Design patent (D-number) — branch before the workflow

**Check the asserted patent's registration number FIRST.** If it has a `D`,
`RE`, or `PP` prefix (e.g., `D712,345`), it's not a utility patent and the
workflow below does NOT apply. Branch per prefix:

- **`D` prefix — design patent (35 U.S.C. §171).** Different test, different
  claim structure, different damages. Do NOT build a claim chart, do NOT run
  doctrine of equivalents, do NOT do element-by-element mapping. Design
  patents have a single claim defined by the drawings; charting a figure as
  if it were a utility claim element list is wrong doctrine.
- **`RE` prefix — reissue patent.** Treat as the utility patent it reissued,
  but flag reissue-specific defenses (intervening rights under §252,
  recapture rule, original-patent requirement).
- **`PP` prefix — plant patent.** Separate regime (35 U.S.C. §161). Asexually
  reproduced plant varieties. Route to plant-patent counsel; this skill does
  not analyze plant patents.

**Design patent infringement test — ordinary observer.** *Egyptian Goddess,
Inc. v. Swisa, Inc.*, 543 F.3d 665 (Fed. Cir. 2008) (en banc). The question
is whether an ordinary observer, **familiar with the prior art designs**,
would be deceived into thinking the accused design is the same as the
patented design. Compare **overall ornamental appearance**, not individual
elements. The accused product must appropriate the **novelty** that
distinguishes the patented design from the prior art (the "point of novelty"
survives as a guidepost inside the ordinary-observer test, not as a separate
test).

**Functional-vs-ornamental filter.** Design patents protect ornamental
features only; functional features are not protected. If the accused
similarity is in features dictated by function, flag that the overlap may
fall outside the patented scope.

**§289 total-profit damages flag.** Design patent damages under 35 U.S.C.
§289 are the infringer's **total profits on the "article of manufacture,"**
which can be the whole product or a component. *Samsung Electronics Co. v.
Apple Inc.*, 580 U.S. 53 (2016). This is a separate analysis from utility
patent reasonable-royalty / lost-profits and is specialist work — do not
compute.

**Trade dress cross-flag.** The same ornamental-shape facts are usually also
a **trade dress** question under Lanham Act §43(a) (15 U.S.C. §1125(a)).
Product configuration trade dress requires **secondary meaning** (*Wal-Mart
Stores, Inc. v. Samara Bros., Inc.*, 529 U.S. 205 (2000)) and must be
**non-functional** (*TrafFix Devices, Inc. v. Marketing Displays, Inc.*,
532 U.S. 23 (2001)). Flag trade dress as a parallel track; the tests are
different but the evidence overlaps.

### Design patent triage — output

Because you cannot see the patent drawings or the accused product directly,
the design patent triage is mostly a request for the materials and a frame
for the analysis:

- **Ask for the drawings.** "I can't run the ordinary-observer test without
  seeing the patent figures and the accused product. Paste or attach: (a)
  the patent drawings (all figures, including any broken-line disclaimers),
  (b) photos of the accused product from comparable angles, (c) any prior
  art designs you're aware of."
- **Prior-art landscape.** Ordinary observer is a *comparison* test — the
  observer is "familiar with the prior art," so the scope of the patented
  design narrows as the prior-art field crowds. Flag what prior art is
  known and what's missing.
- **Functional-vs-ornamental analysis.** Walk the features and flag which
  look functional (and therefore unprotected) vs. ornamental.
- **Broken lines.** Design patents use solid lines for claimed features and
  broken lines for unclaimed environmental context. Flag whether the
  alleged copying is in claimed (solid-line) or unclaimed (broken-line)
  territory.
- **§289 damages flag** as above.
- **Trade dress cross-flag** as above.

**Route to a design patent specialist for anything beyond first-pass triage.**
Design patent litigation is a subspecialty (Perkins Coie, Sterne Kessler,
Desmarais, Kirkland's design team, Gibson Dunn's design group are
representative; use your practice profile's IP litigation OC as the starting
point). This skill flags issues; it does not assess infringement.

### Utility patent workflow

The rest of this mode assumes the asserted patent is a **utility patent**
(no `D`/`RE`/`PP` prefix). If the D-number branch above applies, stop here.

> **Patent systems differ by jurisdiction.** The US claim chart (all-elements rule, doctrine of equivalents, prosecution history estoppel, §284/§289 damages) does not transfer to other systems:
> - **Germany:** Utility models (Gebrauchsmuster), the Schneidmesser/Kunststoffrohrteil questions for DOE, bifurcated validity/infringement proceedings.
> - **China:** Utility models (shiyong xinxing), CNIPA examination, different claim construction.
> - **Japan:** Utility models, JPO examination, a narrower DOE.
> - **Europe (unified patent court):** UPC procedure as of 2023.
>
> When non-US jurisdictions are in scope: "This analysis uses the US claim-charting framework. A product manufactured in China and sold in the EU needs CNIPA and EP analysis, not a US claim chart. I can flag the issues a US analysis surfaces, but the infringement and validity calls require [jurisdiction]-specific review."

### Workflow

- Accused product / process / method — described in technical detail.
- Identified patent(s) at issue.
- Claim chart for each independent claim: element-by-element mapping to the
  accused product.
- Literal infringement first. DOE as a flag.
- Indirect (induced, contributory) and divided infringement as flags.
- **Invalidity defenses to consider** — anticipation (§ 102), obviousness
  (§ 103), § 112 written-description / enablement / definiteness, § 101
  subject-matter eligibility (*Alice* / *Mayo*). Known IPR or PGR outcomes,
  known prior art, known prosecution history. Flag each; do not opine.
- **Unenforceability defenses** — inequitable conduct flag, prosecution
  laches flag, assignor / licensee estoppel flag. Each is attorney-only.
- **Damages posture** — lost profits vs. reasonable royalty (Georgia-Pacific
  factors), marking, pre-suit notice, willfulness (reading this triage may
  factor into willfulness — see the FTO skill's willfulness note).

### Output

Claim charts. Element flags. Defense flags. Routing to patent counsel. See
the `/ip-legal:fto-triage` skill for the full output structure — the
infringement-triage patent mode uses the same format with "accused product"
substituted for "own product."

### Handoff to the full claim chart

For a detailed element-by-element claim chart suitable for infringement or
invalidity contentions, run `/litigation-legal:claim-chart`. This triage's
claim chart is a first pass to identify the strongest and weakest mappings;
the litigation claim chart builds the full chart with pin cites, claim
construction flags, dependent claims, and the verification workflow that
contentions require.

---


## Trade secret mode

### Was it a secret?

Apply the Defend Trade Secrets Act (18 U.S.C. § 1836 et seq.) for federal
purposes and the applicable state UTSA (or, in New York / Massachusetts /
other non-UTSA jurisdictions, the state's common-law test). Flag:

- **Not generally known** — to the public or to others in the industry who can
  obtain economic value from disclosure.
- **Economic value from secrecy** — independent economic value actual or
  potential, derived from not being generally known.
- **Combinations and compilations** — a combination of public elements can
  be a trade secret (*Altavion v. Konica Minolta*, and the Restatement view).

### Reasonable measures

- NDAs with employees, contractors, counterparties. Scope, signed, enforced?
- Access controls — technical (role-based), physical (doors, badges),
  organizational (need-to-know).
- Marking — confidentiality legends on documents, code, data.
- Exit interviews / return of materials on termination.
- Trade-secret policy / training.

Flag what's in place and what's missing. *Reasonable* is fact-specific; the
triage does not decide whether the measures were reasonable — it lists them.

### Misappropriation

Acquisition by improper means, or disclosure / use in breach of duty.
Improper means includes theft, bribery, misrepresentation, breach or
inducement of breach of a duty to maintain secrecy, or espionage (electronic
or otherwise). 18 U.S.C. § 1839(6).

- **Former employee fact pattern:** new employer, overlapping work,
  departure timing, documents taken (and returned?), access logs, recruiting
  channels, assignment and invention-assignment agreements.
- **Inadvertent disclosure:** Was disclosure made by a person with a duty? Did
  the recipient know or have reason to know of the breach?
- **Reverse engineering** — a defense if the means were lawful. Flag whether
  reverse engineering is plausible on the facts.

### Preemption

Where state tort claims (unfair competition, conversion, breach of confidence)
might be preempted by the UTSA, flag preemption. Some jurisdictions preserve
contract claims; others preempt most tort claims addressing the same facts.

### Output

Three flag groups — secrecy, measures, misappropriation — each with what cuts
each way. Routing per posture.

---


## What this skill does not do

- **Never concludes** — no infringement / non-infringement finding, no fair-use
  call, no validity opinion, no damages computation.
- **No substitute for investigation** — evidence-gathering, experts, claim
  construction, and the full litigation chart are out of scope.
- **No outside-jurisdiction analysis** — foreign-law questions get flagged, not
  answered.
- **No automatic drafting** — a C&D or takedown is offered, never produced
  unprompted.
- **Nothing quoted back to the other side** — the triage is work product for
  the attorney's side.

Full list: see [references/what-this-skill-does-not-do.md](references/what-this-skill-does-not-do.md).


## Output format (all modes)

Prepend the work-product header from `~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md` `## Outputs`.

```markdown
[WORK-PRODUCT HEADER]

# Infringement Triage — [Trademark | Copyright | Patent | Trade Secret] (NOT A FINDING)

**This is a triage, not a finding of infringement or non-infringement.** The
triage identifies factors and flags what matters most; it does not conclude.
A conclusion requires an attorney's judgment on the facts, the right scope,
jurisdiction, and defenses. Acting on a triage without attorney review is
how companies end up on the wrong side of fee awards, Rule 11 sanctions,
declaratory-judgment actions, and enhanced damages.

**Triage result:** [GREEN / YELLOW / RED — one sentence why]
```

## Reference Files

- **Citation Verification**: see [references/citation-verification.md](references/citation-verification.md)
- **Close With The Next Steps Decision Tree**: see [references/close-with-the-next-steps-decision-tree.md](references/close-with-the-next-steps-decision-tree.md)
- **Defenses And Thresholds**: see [references/defenses-and-thresholds.md](references/defenses-and-thresholds.md)
- **Factor Analysis**: see [references/factor-analysis.md](references/factor-analysis.md)
- **Handoff To Enforcement Skills**: see [references/handoff-to-enforcement-skills.md](references/handoff-to-enforcement-skills.md)
- **Non Lawyer Gate**: see [references/non-lawyer-gate.md](references/non-lawyer-gate.md)
- **Output Location**: see [references/output-location.md](references/output-location.md)
- **Posture And Scope**: see [references/posture-and-scope.md](references/posture-and-scope.md)
- **Recommended Next Steps**: see [references/recommended-next-steps.md](references/recommended-next-steps.md)
- **Tone**: see [references/tone.md](references/tone.md)
- **What Cuts Which Way Summary**: see [references/what-cuts-which-way-summary.md](references/what-cuts-which-way-summary.md)
- **What This Skill Does Not Do**: see [references/what-this-skill-does-not-do.md](references/what-this-skill-does-not-do.md)

Some of these are output templates rather than reading material — Defenses
And Thresholds, Factor Analysis, Posture And Scope, Recommended Next Steps,
and What Cuts Which Way Summary. Fill their bracketed placeholders with the
mode's factors and flags as you walk them; they are meant to shape the memo,
not to be pasted verbatim.
