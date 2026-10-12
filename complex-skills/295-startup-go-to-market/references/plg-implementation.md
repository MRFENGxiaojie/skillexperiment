# PLG Implementation Guide

Use when the chosen motion is PLG or hybrid (PLG + sales-assist). The goal is a self-serve path from signup to activation that does not depend on a human touch.

## What PLG requires

1. A self-serve onboarding flow that reaches "first value" without sales or CS intervention.
2. A clear activation definition, instrumented as an event (not a belief).
3. Pricing and a free tier (or trial) that let users start without talking to anyone.
4. Product-qualified signals (usage events, fit data) that can route users to sales when expansion justifies it.

## Build order

- [ ] Define activation as a concrete event (e.g., "created first project + invited teammate")
- [ ] Instrument the funnel: signup -> activation -> retained -> paid
- [ ] Ship the shortest possible path to activation; remove any step a user can skip
- [ ] Decide free tier limits (what free users can do, where the limit sits)
- [ ] Add upgrade triggers (limit reached, feature unlocked, paywall moment)
- [ ] Add PQL events and thresholds (e.g., 3 key actions in 7 days)
- [ ] Define PQL-to-SQL routing rules and SLA (see the checklist in SKILL.md)
- [ ] Set up weekly review of the funnel by stage and channel

## Free tier decisions

- Free tier exists to demonstrate value, not to be a charity tier. The limit must sit where the pain of upgrading exceeds the effort.
- If free users never upgrade and never churn, the tier is too generous.
- Track free-to-paid conversion per activation path and per ICP.

## PLG metrics

- Activation rate (signup -> activation)
- Time to activation
- Free-to-paid conversion
- PQL rate and PQL-to-SQL conversion
- Expansion (upsell/cross-sell) rate
- Net revenue retention

## Common pitfalls

- Optimizing signups instead of activation
- Building onboarding for the demo, not the daily user
- Making the free tier so generous that expansion revenue disappears
- Routing every user to sales too early (kills the self-serve loop)
