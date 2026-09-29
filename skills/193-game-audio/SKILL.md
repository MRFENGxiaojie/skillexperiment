---
name: game-audio
description: Game audio principles. Sound design, music integration, adaptive audio systems. Use when the user asks about game sound design, music integration, adaptive or dynamic audio, 3D audio, audio mixing, or audio formats and budgets for games.
allowed-tools: Read, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Game Audio Principles

> Sound design and music integration for immersive gaming experiences.

---

## Workflow / Process

Answer game audio questions in this order:

1. **Classify the sound** — identify the audio category (Music, SFX, Ambience, UI, Voice) and its behavior implications.
2. **Apply category behavior** — loop vs one-shot, 3D positioning, priority, ducking behavior per category.
3. **Resolve channel competition** — if sounds compete for channels, apply the Priority Hierarchy (Voice > Player SFX > Enemy SFX > Music > Ambience).
4. **Apply platform constraints** — when platform or budget is involved, apply the Format Selection and Memory Budget tables.
5. **Set mix levels** — when mixing is involved, apply the Volume Balance Reference and Ducking Rules.
6. **Check anti-patterns** — if the design matches an Anti-patterns entry, flag it.

---

## Scope / Limitations

This skill provides game audio principles and decision tables. It does not cover:

- **Audio middleware** — Wwise/FMOD project configuration, event setup, or bus routing.
- **Sound production** — recording, mixing, mastering, or choosing specific tools (e.g., which synthesizer to use).
- **Music composition** — writing music; only music integration decisions are covered.
- **Voice synthesis** — TTS or voice generation.

It applies to game audio only, not film scoring, podcasts, or voice chat. If the user targets a specific middleware or engine project (e.g., a Unity AudioMixer setup), follow that engine's documentation.

---

## 1. Audio Category System

### Category Definitions

- **Music** category: loops, crossfades, and can be ducked; examples include BGM and combat music.
- **SFX** category: one-shot, 3D positioned; examples include footsteps and impacts.
- **Ambience** category: loops as a background layer; examples include wind, crowd, and forest.
- **UI** category: immediate, non-3D; examples include button clicks and notifications.
- **Voice** category: has priority and acts as a ducking trigger; examples include dialogue and narrator.

### Priority Hierarchy

```
When sounds compete for channels:

1. Voice (highest - always audible)
2. Player SFX (critical feedback)
3. Enemy SFX (important for gameplay)
4. Music (mood, but duckable)
5. Ambience (lowest - can be dropped)
```

---

## 2. Sound Design Decisions

### SFX Creation Approach

- Use **Recording** when realism is needed; it yields high quality but is time intensive.
- Use **Synthesis** for sci-fi, retro, and UI sounds; it is unique but requires skill.
- Use **Library samples** for fast production; they give common sounds but have licensing considerations.
- Use **Layering** for complex sounds; it gives the best results but requires more work.

### Layering Structure

- The **Attack** layer provides the initial transient; example: click, snap.
- The **Body** layer provides the main character; example: boom, blast.
- The **Tail** layer provides decay and ambience; example: reverb, echo.
- The **Sweetener** layer adds a special touch; example: shell casing, mechanical.

---

## 3. Music Integration

### Game State → Music Response
- Menu -> Calm, loopable theme
- Exploration -> Atmospheric, ambient
- Combat detected -> Transition to tension
- Active combat -> Full battle music
- Victory -> Stinger + calm transition
- Defeat -> Dark stinger
- Boss -> Unique track, multi-phase

### Transition Techniques

- Use **Crossfade** for a smooth mood change, giving a gradual feel.
- Use **Stinger** for an immediate event, giving a dramatic feel.
- Use **Stem mixing** for dynamic intensity, giving a seamless feel.
- Use **Beat-synced** for rhythmic gameplay, giving a musical feel.
- Use **Queue point** at the next natural break, giving a clean feel.

---

## 4. Adaptive Audio Decisions

### Intensity Parameters

- **Threat level** affects music intensity; example: enemy count.
- **Health** affects filter and reverb; example: low health = muffled.
- **Speed** affects tempo and energy; example: running speed.
- **Environment** affects reverb and EQ; example: cave vs outdoors.
- **Time of day** affects mood and volume; example: night = quieter.

### Vertical vs Horizontal

- **Vertical (layers)** adds/removes instrument layers; best for intensity scaling.
- **Horizontal (segments)** uses different music sections; best for state changes.
- **Combined** changes both; best for AAA adaptive soundtracks.

---

## 5. 3D Audio Decisions

### Spatialization

- Player footsteps are not 3D positioned (or only subtle) so they are always audible.
- Enemy footsteps are 3D positioned for directional awareness.
- Gunfire is 3D positioned for combat awareness.
- Music is not 3D positioned because it is mood/non-diegetic.
- Ambience zones are 3D positioned (as an area) for environmental effect.
- UI sounds are not 3D positioned because they are interface feedback.

### Distance Behavior

- **Near**: full volume, full frequency.
- **Mid**: volume falloff, high frequency rolloff.
- **Distant**: low volume, low-pass filter.
- **Max**: silent or ambient hint.

---

## 6. Platform Considerations

### Format Selection

- PC: recommended format is OGG Vorbis or WAV, for quality and no license.
- Console: recommended format is platform-specific, for certification.
- Mobile: recommended format is MP3 or AAC, for size and compatibility.
- Web: recommended format is WebM/Opus with MP3 fallback, for browser support.

### Memory Budget

- Casual mobile: audio budget 10-50 MB; strategy is compressed, fewer variants.
- Indie PC: audio budget 100-500 MB; strategy is quality focus.
- AAA: audio budget 1+ GB; strategy is full quality, many variants.

---

## 7. Mix Hierarchy

### Volume Balance Reference

- **Voice**: relative level 0 dB (reference); always clear.
- **Player SFX**: relative level -3 to -6 dB; prominent but not harsh.
- **Enemy SFX**: relative level -6 to -9 dB; important but not dominant.
- **Music**: relative level -6 to -12 dB; foundation, ducks for voice.
- **Ambience**: relative level -12 to -18 dB; subtle background.

### Ducking Rules

- When voice plays, duck Music and Ambience by -6 to -9 dB.
- When an explosion occurs, duck everything except the explosion (brief duck).
- When a menu opens, duck gameplay audio by -3 to -6 dB.

---

## 8. Anti-patterns

- Don't play the same sound repeatedly; use variations (3-5 per sound).
- Don't use max volume on everything; use a proper mix hierarchy.
- Don't ignore silence; silence creates contrast.
- Don't use one infinite loop of music; provide variety and transitions.
- Don't skip audio in prototype; placeholder audio matters.

---

## Output Format

Structure every answer as follows:

1. **Category declaration** — state which audio category (Music, SFX, Ambience, UI, Voice) the sound belongs to and what its behavior implies.
2. **Decision chain** — present recommendations in order: priority, creation approach, mix level, ducking.
3. **Specific values** — cite concrete numbers from this skill's tables: formats, memory budgets, dB ranges.
4. **Anti-pattern check** — if the design contains any Anti-patterns entry, call it out explicitly.

---

> **Remember:** 50% of the game experience is audio. A muted game loses half its soul.

