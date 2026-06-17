# 🗺️ كِسرة — Development Roadmap

> "اللي جاي هيبقى نار" 🔥

---

## 🎯 Vision (updated 2026-06-17)

**كِسرة** is an **infinite** Egyptian-themed brick-breaker. There is **no level cap and no ending** —
the 9 knowledge worlds (Science, Art, History, Geography, Architecture, Religion, National,
Logistics, Space) are **biomes that cycle forever**, getting harder and richer every loop. The
"100+ levels / v1.0 launch" framing from the original design is retired: the game is a **live
product** that keeps receiving new bricks, drops, bosses, and effects in small updates
indefinitely, the same way a live-service arcade game would.

Core invariants:
- **No win screen.** The run only ends when the player loses all lives.
- **Biome cycling, not biome completion.** Round `N` → biome `((N-1) % 9) + 1` → cycle `floor((N-1)/9)+1`.
- **Recurring, scaling bosses.** Every 8th round in a cycle is a boss round; boss stats scale with
  the cycle number so the same 9 bosses stay relevant forever instead of being "beaten once."
- **Everything is data-driven** so new content (bricks, drops, biomes, bosses) can be added without
  touching engine code — this is what makes "update every while" sustainable.

---

## 🧭 How to resume this project in a new session

1. Read this file (`ROADMAP.md`) top to bottom — `## Checkpoints` below is the live status.
2. Read `GAME_DESIGN.md` for the full content bible (drops, bricks, bosses, economy, audio, visuals).
3. Read the repo-root `CLAUDE.md` for the current engineering state (what's implemented vs stubbed,
   how to run/export, known gaps).
4. Pick up the next unchecked item in `## Checkpoints`.

---

## ✅ Checkpoints (live status — update as you go)

### Phase 0 — Infinite Core Foundation (Python + Pygame)
- [x] Repo made public
- [x] Engine switched from Godot 4.3 → **Python + Pygame-CE** for beautiful programmatic visuals
- [x] `settings.py` — all constants: screen, speeds, biome palette, brick tiers, drop types
- [x] `state.py` — GameState: score/lives/combo/coins/powerups, add_score(), lose_life()
- [x] `levelgen.py` — procedural infinite round generator (scaling HP/density/drops, recurring scaled bosses)
- [x] `entities.py` — Ball (rainbow HSV trail, wall bounces, brick overlap), Paddle, Brick, Drop
- [x] `gfx.py` — drawing primitives: pre-baked glow surfaces, gradient backgrounds, 3D bricks, hearts
- [x] `particles.py` — ParticleSystem (burst/sparks), FloatTextSystem, RingSystem, AmbientSystem
- [x] `scenes.py` — MenuScene (animated pyramids, Arabic title, pulsing PLAY), PlayScene, GameOverScene
- [x] `main.py` — async entry point (Pygbag-compatible: `await asyncio.sleep(0)`)
- [x] Cairo.ttf bundled — correct Arabic rendering of كِسرة verified
- [x] All 3 scenes pass 180-frame headless simulation without crash
- [x] `v0.1-infinite-core` GitHub Release published (Godot prototype + Windows exe)

### Phase 1 — Web Deploy
- [x] `pygbag.ini` config added (480×720 canvas, metadata)
- [x] `.github/workflows/web-deploy.yml` — Pygbag WASM build + GitHub Pages deploy on every push
- [x] GitHub Pages enabled at `https://lord1egypt.github.io/Kesra/`
- [ ] Verify live URL loads and game runs in browser after CI succeeds
- [x] Touch input for paddle (mobile browsers) alongside keyboard — FINGERMOTION/FINGERDOWN
- [x] AUTO PLAY mode + speed control (½×–2×) + Egyptian themed loading screen
- [x] Pause menu (ESC/P → Resume/Restart/Menu), aim guide, combo meter, brick HP numbers

### Phase 2 — Art & Feel
- [ ] Gemini Imagen 4 backgrounds for all 9 biomes (unlock: enable API billing at ai.dev)
  - Use: `python3 ~/.claude/tools/gemini_image.py --kesra-biomes --out-dir assets/bg/`
- [~] Power-up/drop effects wired to gameplay — **done:** multi-ball, star (×2), bomb,
  rocket (row buster), diamond, sticky-magnet, fireball, wide, slow, shield, coins, heart.
  **TODO:** laser, ghost-ball, lightning, meteor, whirlwind, eye-of-horus (see FUTURE_IMPROVEMENTS.md)
- [ ] Per-biome particle theme (sand/fire/gold/stardust)
- [ ] Boss telegraphing + multi-phase weak points
- [x] Sound effects — procedural zero-dep synth (`audio.py`): paddle / brick (combo-pitched) /
  coin / power-up / combo / bomb / life-lost / round-clear / game-over; M to mute (persisted).
  Degrades to silent no-op where the mixer is unavailable (WASM pre-gesture).
- [ ] Per-biome music (looping themes) — still TODO

### Phase 3 — Meta-progression
- [ ] Shop (paddle/ball skins) wired to persistent coins
- [x] Achievements — 14 unlockable, toast on unlock, menu panel (A); stats persisted in save
- [ ] Daily/weekly challenge modifiers
- [x] Save to localStorage (web) / file (desktop) — `storage.py`; persists best score/round + settings

### Phase 4 — Mobile
- [ ] Android APK via Pygbag or Buildozer
- [ ] iOS (needs macOS toolchain)
- [ ] Store listing assets

### Ongoing — "Seasons" (post-Phase 1, runs forever)
Once the infinite core is solid and playable in a browser, work proceeds as small recurring content:
- New brick types / drop types
- New recurring boss variants
- Cosmetic skins for paddle/ball
- Leaderboard refresh, seasonal modifiers (Ramadan, holidays, etc.)

---

## 🏅 Version Tags (informational, not "finish lines")

- `v0.1-infinite-core` — Godot prototype shipped 2026-06-16
- `v0.2-python` — Python + Pygame rewrite, beautiful visuals, CI web deploy
- `v0.3-feel` — Phase 2 complete: art + full power-ups + sound
- `v0.4-meta` — Phase 3 complete: shop + save
- `v0.5-mobile` — Phase 4 complete
- Everything after is a Season, not a version number that implies "done"

---

*Last updated: 2026-06-17 — Python/Pygame rewrite complete, web deploy CI live.*
