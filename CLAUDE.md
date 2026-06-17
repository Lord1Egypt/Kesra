# Kesra — Engineering Memory (for AI assistants resuming this repo)

This file is auto-loaded by Claude Code whenever working in this directory. It records the
**current engineering state** so a new session doesn't have to re-derive it. Content/design
lives in `GAME_DESIGN.md`; phase tracking lives in `ROADMAP.md`; this file is "what's actually
built and how to keep going."

> **Start here:** `STATUS.md` is the consolidated "what's done / what remains" snapshot —
> read it first when resuming.

## Non-negotiable design constraint
**The game has no level cap.** Worlds 1-9 are biomes that cycle forever (`round → biome →
cycle`), difficulty and drop rarity scale with the cycle number, bosses recur scaled instead of
being beaten once. Do not reintroduce a finite "v1.0 launch" ending — see `ROADMAP.md`'s
"Vision" section for the reasoning.

## Repo facts
- **Public** GitHub repo: `Lord1Egypt/Kesra`
- Default branch: `main`. **Workflow: always branch → PR → merge, never push directly to main**
  (this is a standing rule across all of Lord1Egypt's repos, not specific to Kesra).
- Engine: **Python + Pygame-CE 2.5.7**. Zero external dependencies beyond `pygame-ce`.
- Web export: **Pygbag** — `python -m pygbag --build main.py` → `build/web/index.html`
  CI workflow at `.github/workflows/web-deploy.yml` builds and deploys to GitHub Pages on every
  push to `main`. Live URL: `https://lord1egypt.github.io/Kesra/`

## File map — what each module does
```
main.py        async entry (Pygbag-compatible: has await asyncio.sleep(0))
settings.py    all constants: screen size, speeds, colours, biome/brick/drop definitions
gfx.py         drawing primitives: glow surfaces, gradient backgrounds, 3D bricks, hearts
particles.py   ParticleSystem, FloatTextSystem, RingSystem, AmbientSystem
levelgen.py    generate_round(n) → procedural brick grid dict (no JSON files needed)
entities.py    Ball, Paddle, Brick, Drop classes
scenes.py      MenuScene, PlayScene, GameOverScene
state.py       GameState: score/lives/combo/coins/powerups; add_score(), lose_life(), etc.
storage.py     cross-platform persistence: browser localStorage → JSON file → in-memory
achievements.py  ACHIEVEMENTS list (id/name/desc/check); GameState tracks stats + unlocks
audio.py       procedural SFX (zero-dep array+mixer synth); init()/play()/play_brick()/set_muted()
assets/fonts/Cairo.ttf   Arabic TTF — loaded by scenes._fonts() for proper كِسرة rendering
```

## How to run / verify locally
```bash
pip install pygame-ce
python main.py            # desktop run
python tools/test_smoke.py   # headless smoke test (10 checks, exits 0 on success)
```

CI (`.github/workflows/ci-cd.yml`) runs `compileall` + `tools/test_smoke.py` on every
push/PR. **Run the smoke test before every PR** — it covers menu, every drop type, pause,
bomb/rocket, multi-ball cap, special bricks, achievements+persistence, boss round, a 6k-frame
auto-play soak, and game-over. (The old Godot `ci-cd.yml` was deleted in the engine switch's
cleanup — it was failing every push trying to export Godot presets.)

### Headless simulation (no display — for CI / testing)
```python
import os; os.environ["SDL_VIDEODRIVER"] = "dummy"; os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame; pygame.init()
# then import scenes, state, etc. as normal
```

### Web build
```bash
pip install pygbag
python -m pygbag --build --app_name kesra main.py
# output → build/web/index.html + WASM
```

## What's implemented (as of 2026-06-17)
- Full infinite game loop: menu → play → game_over → restart, cycling forever
- Procedural round generator: 9 biomes × N cycles, boss every 8th round, difficulty scales
- Ball physics: wall bounces, paddle angle-based launch, brick overlap side-detection
- Particle system: burst, sparks, ambient floating sparkles, rising float-text, ring shockwaves
- 6 brick tiers (mud → obsidian), rainbow HSV trail on ball, per-biome atmospheric glow
- Special bricks (data-driven via levelgen `special` field): explosive (chain-capped 3 deep),
  cursed (shrinks paddle), gift (guaranteed good drop) — geometric badge drawn by gfx.draw_special_mark
- Round-clear victory fountain + "ROUND CLEAR" float; 500+ point bricks use the larger popup font
- Achievements: 14 unlockable (achievements.py), toast on unlock in-game, menu panel via 'A' key;
  lifetime stats (bricks/drops/best_combo/boss_clears/max_balls) + unlock set persisted in save
- First-run tutorial overlay (persisted `tut_done`); Konami code on the menu enables session-only
  God Mode (gs.god_mode) — balls spawn as slow permanent fireballs
- Drops: bronze/silver/gold coins, diamond(+1k), heart, shield, wide, fireball, magnet,
  slow, multi_ball, star(×2 score), bomb(3×3), rocket(row buster)
- Multi-ball: `PlayScene.balls` is a list (cap `MAX_BALLS=6`); life lost only when ALL balls fall
- Sticky magnet: paddle catches the ball while magnet active; re-launch on SPACE/click/touch
- AUTO PLAY AI (`_run_ai`) tracks lowest descending ball; speed control via `gs.speed` (½×–2×)
- Pause menu (ESC/P → Resume/Restart/Menu), aim-guide dotted line, combo meter bar, brick HP numbers
- HUD: score (top-left), combo+meter, lives (hearts), active-effect stack, speed/auto pill,
  round/cycle/biome (bottom)
- Screen shake on 8x combo multiples + bomb/rocket
- Cairo TTF font for correct Arabic rendering of كِسرة
- All scenes verified by headless simulation (normal + boss + 20k-frame auto-play soak) without crash

## Known gaps / honest limitations
- Magnet is now a sticky-catch paddle (no mid-air attraction physics — that's a separate future item)
- No shop yet (Phase 3 in ROADMAP.md); save + achievements are done
- Audio is procedural SFX only — no music tracks yet; mixer may be silent in WASM until a
  user gesture, by design it no-ops rather than crashing (`audio.enabled` stays False)
- Web deploy is set up but Pygbag WASM requires the game to `await asyncio.sleep(0)` every frame
  — already in main.py so this is satisfied
- Mobile (Android/iOS) not started yet (Phase 4)

## Working agreement for future sessions
- Update `ROADMAP.md` checkboxes as you complete items
- Branch + PR for all changes (standing rule)
- Never commit `build/` directory — it's in `.gitignore` and rebuilt by CI
- The Gemini API key is at `~/.config/gemini/api_key` (chmod 600) — never commit it; repo is PUBLIC
- To generate game art (biome backgrounds, bosses): `python3 ~/.claude/tools/gemini_image.py`
  — requires API billing enabled at ai.dev first

## Bug history (for context)
- **GameOver TypeError** (fixed 2026-06-17, PR #23): `tuple(int,) * 3` raised
  `TypeError: 'int' object is not iterable` — fixed to `(v, v, v)` literal
- **Pygbag.ini crash** (fixed 2026-06-17, PR #24): `ignore_dirs`/`ignore_files` in `[pygbag]`
  section caused `AttributeError: 'Config' object has no attribute 'DEPENDENCIES'` — removed those keys
- **Ball stops/disappears** (Godot prototype, 2026-06-16): fixed in Godot prototype before the
  Python rewrite — root causes were no boundary walls + inelastic bounce default. Now moot since
  ball.py implements its own wall-bounce and speed-clamping in pure Python
