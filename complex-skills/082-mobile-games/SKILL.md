---
name: mobile-games
description: Mobile game development principles. Touch input, battery, performance, app stores. Use when the user asks to build or optimize a mobile game, design touch controls, manage battery and thermal constraints, choose a monetization model, or prepare for App Store or Google Play release.
allowed-tools: Read, Write, Edit, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Mobile Game Development

> Platform constraints and optimization principles.

---

## 1. Platform Considerations

### Key Constraints

- Touch input is handled with large touch areas and gestures.
- Battery is handled by limiting CPU/GPU usage.
- Thermal is handled by throttling when hot.
- Screen size is handled with a responsive UI.
- Interruptions are handled by pausing in the background.

---

## 2. Touch Input Principles

### Touch vs Controller

- Touch input is imprecise, while desktop/console input is precise.
- Touch input occludes the screen, while desktop/console has no occlusion.
- Touch has limited buttons, while desktop/console has many buttons.
- Touch has gestures available, while desktop/console has buttons/sticks.

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

- Privacy labels are required.
- Account deletion is required if account creation exists.
- Screenshots are required for all device sizes.

### Android (Google Play)

- Use the current year SDK as the target API.
- 64-bit is required.
- App bundles are recommended.

---

## 5. Monetization Models

- **Premium** is best for quality games and a loyal audience.
- **Free + IAP** is best for casual, progression-based games.
- **Ads** is best for hyper-casual, high-volume games.
- **Subscription** is best for content updates and multiplayer games.

---

## 6. Anti-Patterns

- Don't use desktop controls on mobile; design for touch.
- Don't ignore battery drain; monitor thermals.
- Don't force landscape; support player preference.
- Don't use always-on networking; cache and sync.

---

> **Remember:** Mobile is the most constrained platform. Respect battery and attention.

## Scope and Limitations

- Covers mobile game development specifically — does not cover desktop, console, or web game development
- Focuses on native mobile performance and design patterns; does not cover game design, narrative, or art direction
- Platform requirements (Android API levels, iOS versions, store policies) change over time — always verify against current official documentation
- Does not cover server-side game infrastructure (multiplayer networking, leaderboards, cloud save)

