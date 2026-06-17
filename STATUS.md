# 📊 كِسرة (Kesra) — Project Status Snapshot

> A single-page "where are we" view. **Canonical sources of truth:** `ROADMAP.md` (phases),
> `GAME_DESIGN.md` (content bible), `FUTURE_IMPROVEMENTS.md` (110-item backlog), `CLAUDE.md`
> (engineering memory). This file just consolidates **what's done** and **what remains** so you
> don't have to cross-reference all four. Last updated: **2026-06-17**.

---

## 🎮 What the game is, right now
An **infinite** Egyptian brick-breaker in **Python + Pygame-CE**, playable in the browser
(Pygbag/WASM) at **https://lord1egypt.github.io/Kesra/** and on desktop (`python main.py`).
No level cap — 9 biomes cycle forever, difficulty + bosses scale per cycle.

- **CI:** both GitHub workflows green on `main` — `🎮 Kesra CI` (headless smoke test, 11 checks)
  and `Build & Deploy Web` (Pygbag → GitHub Pages on every push).
- **Tests:** `python tools/test_smoke.py` → `ALL SMOKE TESTS PASSED (11 checks)`, exit 0.

---

## ✅ SHIPPED (this session — PRs #30–#37, all merged)

### Modes & control
- **AUTO PLAY** mode — AI tracks the lowest descending ball, auto-launches (#30)
- **Speed control** — ½× / 1× / 1.5× / 2× tabs on the menu, multiplies all physics (#30)
- **Pause menu** — ESC/P → Resume / Restart / Menu, keyboard + clickable (#31)
- Keyboard + mouse + **touch** (FINGERDOWN/FINGERMOTION) paddle control

### Power-ups / drops
- Coins (bronze/silver/gold), **diamond** (+1,000), heart, shield, wide, slow, fireball
- **Multi-ball** ×2 split (cap 6 balls; life lost only when ALL fall) (#31)
- **Star** — ×2 score for 15s (#31)
- **Bomb** — 3×3 cluster destroy · **Rocket** — bottom-row buster (#31)
- **Sticky magnet** — paddle catches the ball, re-launch on SPACE/click/touch (#31)

### Bricks & juice
- 6 brick tiers + **special bricks**: explosive (chain, capped), gift (guaranteed good drop),
  cursed (shrinks paddle) — geometric badges (#33)
- **Victory fountain** + "ROUND CLEAR" on every round clear (#33)
- Combo meter bar, brick HP numbers, aim-guide dotted line, bigger 500+ score popups (#31, #33)
- Egyptian-themed Pygbag **loading screen** (`tools/patch_web.py`, applied in CI) (#30)

### Systems
- **Persistent save** (`storage.py`) — localStorage (web) → JSON file (desktop) → memory;
  best score/round + settings survive refresh; corruption-safe (#32)
- **Achievements** — 14 unlockable (`achievements.py`), in-game toasts, menu panel (press **A**),
  persisted lifetime stats (#34)
- **Procedural audio** (`audio.py`) — zero-dependency synth: paddle, brick (combo-pitched),
  coin, power-up, combo, bomb, life-lost, round-clear, game-over; **M** mutes (persisted);
  silent no-op where the mixer is unavailable (WASM pre-gesture) (#36)
- **First-run tutorial** overlay (persisted) + **Konami code → 👑 God Mode** easter egg (#37)
- **CI fixed** — replaced the dead Godot workflow with a Python smoke test (#35)

---

## 🚧 WHAT REMAINS

### 🔴 Blocked / needs your input
- **Biome background art** — 9 Gemini Imagen 4 images. *Blocked:* needs API billing enabled at
  ai.dev. Tooling ready: `python3 ~/.claude/tools/gemini_image.py --kesra-biomes --out-dir assets/bg/`.
- **Per-biome music** — 9 looping themes. Needs either audio assets or a longer procedural
  composer; bigger lift than the SFX already shipped.

### 🟡 Phase 3 — Meta-progression (next big feature)
- **Shop / economy** — spend coins between rounds on paddle/ball upgrades (the largest remaining
  feature; coin drops already exist, just not yet bankable/spendable)
- Daily / weekly challenge modifiers (fixed-seed runs)
- Cosmetic unlocks (paddle/ball skins)

### 🟢 Gameplay backlog (asset-free, pickable any time — see FUTURE_IMPROVEMENTS.md)
- **More power-ups:** ghost ball, laser ball, lightning strike, meteor rain, row/column buster
  variants, multi-ball "storm" fan spawn, coin magnet, shield wall
- **More brick types:** armored, healing, moving, mirror, multiplier, glass/reveal, boss-core
- **Boss mechanics:** HP bar, multi-phase, attacks (heal/redirect/shrink), intro/defeat cutscenes
- **Visual polish:** ball skins (fire/ice/galaxy/Ra), parallax stars, depth shadows, rainbow
  paddle, biome transition fade, screen-warp at high combo

### 🔵 Phase 4 — Platforms
- Android APK (Pygbag/Buildozer), iOS (needs macOS toolchain)
- Gamepad support, gyroscope tilt control, PWA installable (manifest + service worker)

### ⚙️ Tech / UX
- Full settings screen (colorblind palette, language toggle) — *mute + speed already done*
- FPS counter (F3), per-round autosave, global leaderboard, replay/ghost

---

## 🗂️ File map (current)
```
main.py          async entry (Pygbag-compatible), audio.init(), save hooks
settings.py      constants: screen, speeds, palette, biomes, brick tiers, drops
state.py         GameState: score/lives/combo, persistence, achievements, stats
storage.py       cross-platform save: localStorage → JSON file → memory
achievements.py  14 achievement defs (id/name/desc/check predicate)
audio.py         procedural SFX synth (array + pygame.mixer), play()/play_brick()/set_muted()
levelgen.py      generate_round(n) → procedural grid (drops + special bricks)
entities.py      Ball, Paddle, Brick (special types), Drop
gfx.py           glow, gradients, 3D bricks, hearts, special-brick badges
particles.py     ParticleSystem, FloatTextSystem, RingSystem, AmbientSystem
scenes.py        MenuScene (achievements/Konami), PlayScene (everything), GameOverScene
rtl.py           Arabic reshaping (arabic_reshaper + bidi) for كِسرة
tools/
  patch_web.py   post-processes Pygbag index.html → Egyptian loading screen
  test_smoke.py  headless smoke test (11 checks) — run before every PR
.github/workflows/
  ci-cd.yml      compileall + smoke test (Python 3.12)
  web-deploy.yml Pygbag build + patch + GitHub Pages deploy
```

---

## 🔑 Standing rules (don't forget)
- **Branch → PR → merge**, never push directly to `main`.
- **Run `python tools/test_smoke.py` before every PR** (CI runs it too).
- **Never commit** `build/`, `kesra_save.json`, or the Gemini API key
  (`~/.config/gemini/api_key`, chmod 600 — repo is PUBLIC).
- The game has **no level cap** — biomes cycle forever; don't reintroduce an "ending".
