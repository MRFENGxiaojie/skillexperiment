# Mobile Platform Guidelines (Spec)

> Mandatory reading before writing any game code or recommendation. These
> guidelines are the concrete thresholds behind the principles in SKILL.md.
> Verify against current official store documentation when specifics change.

## 1. Touch input

- Minimum touch target: **44 × 44 points** (Apple HIG) / **48 × 48 dp**
  (Material) — use the larger when both apply.
- All interactive elements must show visual feedback on touch.
- No action may require two simultaneous precise taps to trigger.
- Support both portrait and landscape unless the game is single-orientation
  by design (state the rationale in the design doc).

## 2. Performance and thermal

- Target 60 FPS for active gameplay, but **30 FPS is acceptable** for
  turn-based or slow-paced play — do not render at full rate when the content
  does not change.
- Thermal escalation ladder (record the chosen step in the design doc):
  1. Device warm → reduce quality settings (shadows, post-processing)
  2. Device hot → cap frame rate
  3. Critical → pause effects / enter low-power mode
- Background behavior: pause the game loop, stop networking, release
  GPU-heavy resources on `OnApplicationPause` / `onStop`.

## 3. Battery

- Minimize GPS, background network sync, and wake-ups.
- Dark scenes save OLED power — use them where thematically acceptable.
- Report battery use honestly in store privacy disclosures.

## 4. App Store (iOS)

- Privacy labels: complete and accurate (data collected / linked / used to
  track).
- Account deletion: if the game offers account creation, it must offer in-app
  account deletion.
- Screenshots: all required device sizes; updated for current iPhone/iPad
  lineup.

## 5. Google Play (Android)

- Target API level: current-year Android SDK (per Play policy).
- 64-bit native code required (if native libs exist).
- App bundle (AAB) preferred over APK.
- Data safety form completed and consistent with actual data usage.

## 6. Monetization decision criteria

| Model | Choose when |
|-------|-------------|
| Premium | Short core loop, high polish, established brand |
| Free + IAP | Progression-based gameplay, repeat sessions |
| Ads | Hyper-casual, high volume, short sessions |
| Subscription | Regular content updates, multiplayer, retention-driven |

Do not recommend multiple models without a clear primary; state the rationale
in the design doc.
