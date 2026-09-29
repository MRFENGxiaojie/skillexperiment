# Current Implementation Notes (Unity)

## Tech Stack
- Unity 2022.3 LTS, URP rendering pipeline
- Portrait 1080×1920 fixed resolution
- Android minSdk 26; no iOS build experience (first submission)

## Input Controls (ported directly from the PC version)
- Input: `Input.mousePosition` sampled in `FixedUpdate` (a mouse click fires)
- Fire button: 32×32 px (fine with PC mouse precision, clearly too small on mobile)
- Aiming: press and drag to set the direction + release to fire; no joystick, no trajectory prediction line
- High demand for fast, precise taps: 400ms combo window; with mobile touch latency, combos frequently fail to chain

## Performance & Power Consumption
- Target frame rate: constant 60 FPS, `Application.targetFrameRate = 60`
- No frame-rate adaptation (no dynamic resolution, no thermal frame throttling)
- Particle effects: an average of 3 resident particle systems per round + explosion effects
- Switching to background: `OnApplicationPause` only pauses game logic; **the WebSocket scoring connection stays alive**, continuously syncing scores in the background (measured: about 8% battery drain over 10 minutes in the background)
- No battery/temperature detection

## Online Features
- Real-time score upload (WebSocket), reconnection without exponential backoff
- Leaderboard refreshes every round

## Other
- No anti-addiction / age-appropriateness notice implementation
- No GDPR / privacy policy page (only text embedded in the login page)
- Data reporting: self-built analytics, no third-party SDKs (except the AdMob test package)