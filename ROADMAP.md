# 🗺️ كِسرة — Development Roadmap

> "اللي جاي هيبقى نار" 🔥

---

## 🎯 Vision (updated 2026-06-16)

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

### Phase 0 — Infinite Core Foundation
- [x] Repo made private
- [x] Redesign docs for infinite-first structure (this file + GAME_DESIGN + CLAUDE.md)
- [x] `project.godot` fixed: GameManager autoload registered, broken texture/icon preloads removed
- [x] `game_manager.gd` converted from finite world/level to infinite round/cycle/biome model
- [x] `level_generator.gd` — procedural infinite round generator (scaling HP/density/drops, recurring scaled bosses)
- [x] `brick.gd` + `brick.tscn` — primitive-rendered (no art assets yet), hp/points/drop-roll
- [x] `drop.gd` + `drop.tscn` — falling pickup, magnet support, rarity color coding
- [x] `paddle.tscn`, `ball.tscn` — wired to existing scripts, primitive shapes instead of missing sprites
- [x] `game.gd` + `game.tscn` — wires everything, spawns rounds back-to-back forever
- [x] `hud.gd` + `hud.tscn` — score / lives / round / biome / combo
- [x] `main_menu.gd` + `main_menu.tscn` — entry point
- [x] Juice pass 1: brick-break particle burst, combo screen shake, score popups
- [x] Playable in a real browser engine — verified 2026-06-16 via Playwright + headless Chromium loading the exported build: main menu renders (Start button works) and clicking Start loads the gameplay scene with a real generated brick grid + HUD, zero console errors. Still want a human to actually play it for feel — automated check only proves it *runs*, not that it's *fun*.

### Phase 1 — Web Playable Loop
- [x] Export templates installed + headless Web (HTML5/WASM) export validated in CI sandbox
- [x] Fixed export hosting blocker: `export_presets.cfg` had `variant/thread_support=true`, which requires Cross-Origin-Isolation/SharedArrayBuffer headers most static hosts don't send — caught via the Playwright check above. Switched to `thread_support=false` (single-threaded WASM) for broad host compatibility; re-verified clean.
- [ ] Fix CI workflow (`ci-cd.yml`) missing export-template install step
- [ ] Deploy web build somewhere reachable without GitHub Pages (private repo ⇒ Pages needs paid plan) — candidate: Vercel static hosting or itch.io
- [ ] Touch input for paddle (mobile browsers) alongside keyboard
- [x] Windows Desktop export preset added + validated (2026-06-16): self-contained `Kesra.exe` (PE32+ GUI, ~84MB, embedded `.pck`) exports cleanly headlessly via `--export-debug "Windows Desktop"`. Published as a downloadable GitHub Release asset alongside the Web build.

### Phase 2 — Feel & Content Depth
- [ ] All power-up/drop effects from `GAME_DESIGN.md` actually wired to gameplay (currently only a subset)
- [ ] Rocket system (Scarab → Ra's Spear)
- [ ] Combo-based dynamic music intensity
- [ ] Per-biome particle theme (sand/fire/gold/stardust) instead of generic burst
- [ ] Boss telegraphing + multi-phase weak points

### Phase 3 — Meta-progression
- [ ] Shop (paddle/ball/rocket tiers) wired to persistent currency
- [ ] Achievements (including secret ones)
- [ ] Daily/weekly challenge modifiers layered on the infinite core (not a separate finite mode)
- [ ] Cloud save (so progress isn't tied to one browser)

### Phase 4 — Mobile
- [ ] Android export validated (APK installs + runs)
- [ ] iOS export validated (needs macOS/Xcode toolchain — likely cloud CI, not this sandbox)
- [ ] Store listing assets

### Ongoing — "Seasons" (post-Phase 1, runs forever)
This replaces the old "v1.0 Launch then done" milestone. Once the infinite core is solid and
playable in a browser, work proceeds as small recurring content drops:
- New brick types / drop types
- New recurring boss variants
- Cosmetic skins for paddle/ball
- Leaderboard refresh, seasonal modifiers (Ramadan, holidays, etc.)

---

## 🏅 Version Tags (informational, not "finish lines")

- `v0.1-infinite-core` — Phase 0 complete, runs in Godot editor
- `v0.2-web` — Phase 1 complete, playable in a browser tab via shared link
- `v0.3-feel` — Phase 2 complete
- `v0.4-meta` — Phase 3 complete
- `v0.5-mobile` — Phase 4 complete
- Everything after is a Season, not a version number that implies "done"

---

*Last updated: 2026-06-16 — rewritten for infinite-mode-first design.*
