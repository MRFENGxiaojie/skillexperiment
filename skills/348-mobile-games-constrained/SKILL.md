---
name: mobile-games-constrained
description: Mobile game development principles. Touch input, battery, performance, app stores. Use when the user asks to build or optimize a mobile game, design touch controls, manage battery and thermal constraints, choose a monetization model, or prepare for App Store or Google Play release.
allowed-tools: Read, Write, Edit, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Mobile Game Development

> Platform constraints and optimization principles.

---

## Mandatory Workflow

Before writing any game code, you MUST:

1. **Create the design document** at `.workflow/.scratchpad/game-design-{timestamp}/design.json` with:
   ```json
   {"status": "init", "platform": "", "engine": "", "controls": [], "monetization": "", "constraints": [], "decisions": []}
   ```
2. **Read the platform guidelines** at `specs/mobile-platform-guidelines.md` — do not write any code before reading it
3. **Record architecture decisions** in `design.json` → `.decisions[]` with fields: `decision_id`, `topic`, `options_considered`, `chosen`, `rationale`
4. **After implementation**, update `design.json` → `.status` to `"complete"` and add `.verification` with build/test results
5. **Do not skip the design document** — if `.workflow/` is not writable, create it first

---

## 1. Platform Considerations

### Key Constraints

- **Touch input** constraint: use large touch areas and gestures.
- **Battery** constraint: limit CPU/GPU usage.
- **Thermal** constraint: throttle when hot.
- **Screen size** constraint: use responsive UI.
- **Interruptions** constraint: pause in background.

---

## 2. Touch Input Principles

### Touch vs Controller

- Touch input is imprecise, while desktop/console is precise.
- Touch occludes the screen, while desktop/console has no occlusion.
- Touch has limited buttons, while desktop/console has many buttons.
- Touch offers gestures, while desktop/console offers buttons/sticks.

### Best Practices

- Minimum touch target: 44x44 points
- Visual feedback on touch
- Avoid precise timing requirements
- Support portrait and landscape

---

## 3. Performance Targets

### Thermal Management

- Reduce quality when the device is warm.
- Limit FPS when the device is hot.
- Pause effects at critical temperature.

### Battery Optimization

- 30 FPS often sufficient
- Sleep when paused
- Minimize GPS/network
- Dark mode saves OLED battery

---

## 4. App Store Requirements

### iOS (App Store)

- Privacy labels: required.
- Account deletion: required if account creation exists.
- Screenshots: required for all device sizes.

### Android (Google Play)

- Target API: must use the current year SDK.
- 64-bit: required.
- App bundles: recommended.

---

## 5. Monetization Models

- **Premium** model is best for quality games with a loyal audience.
- **Free + IAP** model is best for casual, progression-based games.
- **Ads** model is best for hyper-casual, high-volume games.
- **Subscription** model is best for content updates and multiplayer.

---

## 6. Anti-Patterns

- ❌ Don't use desktop controls on mobile; ✅ do design for touch.
- ❌ Don't ignore battery drain; ✅ do monitor thermals.
- ❌ Don't force landscape; ✅ do support player preference.
- ❌ Don't rely on always-on networking; ✅ do cache and sync.

---

> **Remember:** Mobile is the most constrained platform. Respect battery and attention.

## Output Format

When providing mobile game guidance, structure the response as:

- **Recommendation summary**: What to change and why, referencing the relevant principle or guideline table from this skill
- **Rationale**: Which platform constraint (touch, battery, thermal, store, monetization) drove the recommendation
- **Concrete thresholds**: Specific values where applicable — touch target sizes (44×44 points), FPS targets, thermal triggers, target API levels
- **Verification**: How to confirm the change worked — device testing, profiling, or store checklist review

## Scope and Limitations

- Covers mobile game development specifically — does not cover desktop, console, or web game development
- Focuses on native mobile performance and design patterns; does not cover game design, narrative, or art direction
- Platform requirements (Android API levels, iOS versions, store policies) change over time — always verify against current official documentation
- Does not cover server-side game infrastructure (multiplayer networking, leaderboards, cloud save)

