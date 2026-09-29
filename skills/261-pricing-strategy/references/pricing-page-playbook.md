# Pricing Page Playbook

Design specifications and copy templates for SaaS pricing pages. Use with the `Pricing Page Design` chapter in SKILL.md — this file provides the depth that chapter summarizes.

---

## 1. Above the Fold

The first screen must answer, in order: what am I buying, what does it cost, and can I switch easily. Anything below the fold is for people who are already leaning yes.

### Layout Specification

- **Plan cards:** 3 cards side by side on desktop (or a comparison table for feature-heavy plans). Middle card is the recommended tier, visually elevated: stronger border, slight scale-up, or accent background. Never elevate more than one card.
- **Card width:** minimum 300px per card on desktop; single-column stacking under 768px. Cards must not compress text at smaller widths.
- **Billing toggle:** placed above the cards, centered. Two options, annual default (pre-selected and labeled "Save 20%"). The toggle must switch prices on the cards without a page reload.
- **Price display:** large number, two decimals where prices are non-round, per-period label underneath ("per user / month"). If usage-based, show "starting at" and the formula.
- **CTA buttons:** one per card, full-width, 48px min height. Primary style on the recommended tier, secondary style on others. Do not use "Contact us" on more than one card.
- **Microcopy under the CTA:** one line that removes the last objection, e.g., "No credit card required" or "30-day free trial".

### The 5-Second Test

A first-time visitor should be able to answer all five in five seconds:
1. How many plans are there?
2. Which one should I pick?
3. What does it cost?
4. What do I get?
5. What happens if I exceed a limit?

If any answer takes longer, the section fails the test.

---

## 2. Below the Fold

### Feature Comparison Table

- Full table: all plans as columns, all features as rows, grouped by category (Core, Usage, Integrations, Security, Support).
- Use ✅/❌ and text values, not walls of "included" prose. "—" for not available.
- The recommended tier column highlighted with the same accent as the card above.
- Rows ordered by decision weight: limits and seats first, integrations next, support last.

### FAQ Section

Address the 5 objections that stop people from buying. Templates:

**1. Can I cancel anytime?**
> Yes. Cancel from your billing settings in one click — no emails, no retention calls. You'll keep access until the end of your billing period. [For annual: You can downgrade to monthly anytime, or cancel with a prorated refund within the first 30 days.]

**2. What happens when I hit limits?**
> Nothing breaks. You can keep using the product with [read-only / restricted access] until you upgrade or reduce usage. We'll email you at 80% and 100% so it never surprises you.

**3. Do you offer refunds?**
> [Plan X] comes with a 30-day money-back guarantee. Beyond that, we don't prorate refunds mid-cycle, but we'll always credit you if a service issue caused the problem.

**4. Is my data secure?**
> Yes. Data is encrypted in transit and at rest, [SOC 2 Type II / ISO 27001] certified, with [region]-based hosting. See our security page for the full list.

**5. What if I need to upgrade or downgrade?**
> Upgrades apply immediately and you're billed the prorated difference. Downgrades apply at the next billing cycle. You can switch plans from settings anytime.

Each FAQ needs the objection + a concrete policy answer + a proof detail. Never answer with "it depends."

### Social Proof Placement Rules

- Logos: above the fold, greyscale, 5-10 names from the visitor's industry if possible.
- Quotes: one per plan card region, relevant to the segment that plan targets (startup quote on entry tier, enterprise quote on top tier).
- Case studies: below the comparison table, one per tier, with a number in the headline ("cut time-to-value by 60%").
- Badges: security badges (SOC2, ISO 27001) only when the plan targets B2B enterprise — never on every card.

---

## 3. CTA Copy Templates

| Context | Copy | Notes |
|---------|------|-------|
| Free trial | "Start free trial" | Never "Sign up" — the action is the value |
| Freemium | "Get started free" | Works when entry tier is free |
| Sales-led | "Talk to sales" | Only on the enterprise card; pair with "or start free" elsewhere |
| Demo-heavy | "Book a demo" | Use when the product needs showing before buying |
| Returning visitor | "Continue with your plan" | For logged-in state |
| Microcopy | "No credit card required" | Under the CTA on the entry tier only |

Rules: one CTA verb per card, imperative mood, no "Learn more" as the primary CTA, no exclamation marks.

---

## 4. Copy Voice

- Plan names: simple segment names (Starter / Pro / Enterprise) or job-title names (Founder / Team / Company). Never puns as the only identifier.
- Bullets: 3-5 per plan, verb-first ("Collaborate with unlimited guests"), each bullet one benefit, no feature soup.
- Annually vs monthly: show the annual price first with savings highlighted ("$24/mo billed annually — save 20%"). Never hide the monthly price; hiding creates distrust.
- Localization: prices in the visitor's currency and format where the product sells internationally.

---

## 5. Review Checklist

Before a page ships, confirm:

- [ ] 5-Second Test passes (see section 1)
- [ ] Toggle updates all cards, annual is default
- [ ] One elevated "recommended" tier only
- [ ] Comparison table grouped by category with ✅/❌
- [ ] All 5 objection FAQs answered with concrete policy
- [ ] CTA copy from the template table, one per card
- [ ] Social proof matched to each tier's segment
- [ ] Security badges only where the segment demands them
- [ ] No hidden monthly price, no "Learn more" primary CTAs
