---
name: web-games
description: Web browser game development principles. Framework selection, WebGPU, optimization, PWA. Use when the user asks to build a browser game, choose a web game framework (Phaser, PixiJS, Three.js, Babylon.js), use WebGPU or WebGL, or optimize game performance, assets, and audio in the browser.
allowed-tools: Read, Write, Edit, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Web Browser Game Development

> Framework selection and browser-specific principles.

---

## 1. Framework Selection

### Decision Tree

### What type of game?
- 2D Game
  - Full engine features? - Phaser
  - Raw rendering power? - PixiJS
- 3D Game
  - Full engine (physics, XR)? - Babylon.js
  - Rendering focused? - Three.js
- Hybrid / Canvas
  - Custom - Raw Canvas/WebGL

### Comparison (2025)

- **Phaser 4** is a 2D framework best for full game features.
- **PixiJS 8** is a 2D framework best for rendering and UI.
- **Three.js** is a 3D framework best for visualizations and lightweight use.
- **Babylon.js 7** is a 3D framework best for a full engine and XR.

---

## 2. WebGPU Adoption

### Browser Support (2025)

- Chrome supports it since v113.
- Edge supports it since v113.
- Firefox supports it since v131.
- Safari supports it since 18.0.
- Total support is ~73% globally.

### Decision

- **New projects**: Use WebGPU with WebGL fallback
- **Legacy support**: Start with WebGL
- **Feature detection**: Check `navigator.gpu`

---

## 3. Performance Principles

### Browser Constraints

- No local file access: use asset bundling and a CDN.
- Tab throttling: pause when hidden.
- Mobile data limits: compress assets.
- Audio autoplay: requires user interaction.

### Optimization Priority

1. **Asset compression** - KTX2, Draco, WebP
2. **Lazy loading** - Load on demand
3. **Object pooling** - Avoid GC
4. **Draw call batching** - Reduce state changes
5. **Web Workers** - Offload heavy computation

---

## 4. Asset Strategy

### Compression Formats

- Textures use KTX2 + Basis Universal.
- Audio uses WebM/Opus, with MP3 as fallback.
- 3D models use glTF with Draco/Meshopt.

### Loading Strategy

- Startup: load core assets, under 2MB.
- Gameplay: stream on demand.
- Background: prefetch the next level.

---

## 5. PWA for Games

### Benefits

- Offline play
- Install to home screen
- Fullscreen mode
- Push notifications

### Requirements

- Service worker for caching
- Web app manifest
- HTTPS

---

## 6. Audio Handling

### Browser Requirements

- Audio context requires user interaction
- Create AudioContext on first click/tap
- Resume context if suspended

### Best Practices

- Use Web Audio API
- Audio source pooling
- Pre-load common sounds
- Compress with WebM/Opus

---

## 7. Anti-Patterns

- Don't load all assets upfront; use progressive loading.
- Don't ignore tab visibility; pause when hidden.
- Don't block on audio loading; lazy load audio.
- Don't skip compression; compress everything.
- Don't assume a fast connection; handle slow networks.

---

> **Remember:** The browser is the most accessible platform. Respect its constraints.

## Scope and Limitations

This skill covers browser game development principles only — framework selection, WebGPU/WebGL, performance, assets, audio, and PWA behavior. It does NOT cover:

- Game design, mechanics, and level design
- Monetization, IAP, and ad integration
- Backend services, multiplayer servers, and real-time networking
- Native game engines (Unity, Godot, Unreal) or native mobile development
- WebXR content creation beyond rendering API choice
- Packaging for app stores

Do not use this skill when the user asks for native-only games, server-side game logic, or game design consulting without any browser implementation.

## Output Format

Deliver a runnable browser game:

- A single `index.html` (or `game.html`) that runs standalone in a browser — no build step required
- An `assets/` directory containing every asset the code references (textures, audio, models)
- No console errors on load; the game loop pauses when the tab is hidden
- Explain the framework choice vs. alternatives in one or two sentences (e.g., why Phaser over PixiJS)

