# Kesra — Engineering Memory (for AI assistants resuming this repo)

This file is auto-loaded by Claude Code whenever working in this directory. It records the
**current engineering state** so a new session doesn't have to re-derive it. Content/design
lives in `GAME_DESIGN.md`; phase tracking lives in `ROADMAP.md`; this file is "what's actually
built and how to keep going."

## Non-negotiable design constraint
**The game has no level cap.** Worlds 1-9 are biomes that cycle forever (`round → biome →
cycle`), difficulty and drop rarity scale with the cycle number, bosses recur scaled instead of
being beaten once. Do not reintroduce a finite "v1.0 launch" ending — see `ROADMAP.md`'s
"Vision" section for the reasoning.

## Repo facts
- **Private** GitHub repo: `Lord1Egypt/Kesra` (was public, made private 2026-06-16 at owner's
  request so dev can happen in the open-source-but-not-public sense — fine to push freely).
- Default branch: `main`. **Workflow: always branch → PR → merge, never push directly to main**
  (this is a standing rule across all of Lord1Egypt's repos, not specific to Kesra).
- Engine: Godot **4.3+**, GDScript. No external runtime dependencies.
- **Zero art/audio assets exist in this repo.** Every visual is currently primitive shapes
  (`ColorRect`/`Polygon2D`/`CPUParticles2D`) colored via the palette in `GAME_DESIGN.md`. This is
  intentional — it keeps the game buildable/exportable with zero asset pipeline while the loop is
  being proven out. Swap in real art later without touching gameplay code.

## What's actually implemented (as of 2026-06-16)
Check off against `ROADMAP.md`'s checkpoints — that's the authoritative live list. As of this
writing, Phase 0 (Infinite Core Foundation) scaffolding is being built in this session on branch
`feature/infinite-mode-foundation`.

Key files once Phase 0 lands:
- `src/core/game_manager.gd` — autoload singleton (`/root/GameManager`). Tracks score/lives/
  combo/coins/round/cycle/biome. **No `current_level`/`current_world` finite fields** — replaced
  by `round` (monotonic, never resets except on new run) and derived `biome`/`cycle`.
- `src/core/level_generator.gd` — pure function-style generator: given a round number, returns a
  brick grid dict (reusing the JSON schema shape from `levels/world_1/level_1_astronomy.json` so
  hand-authored "flavor" levels could still be mixed in later if wanted, but nothing requires a
  JSON file to exist — generation is procedural by default).
- `src/gameplay/{paddle,ball,brick,drop}.gd` + matching `.tscn` scenes — primitive-rendered.
- `src/core/game.gd` + `game.tscn` — the actual play scene; spawns rounds back-to-back forever,
  has no "you win" path, only "you lose all lives → game over → restart."
- `src/ui/{main_menu,hud}.gd` + `.tscn`.

## How to run / verify locally
There is no Godot GUI in the sandbox this was built in. Verification done via headless CLI:
```bash
# Godot binary + export templates were downloaded to a scratch dir during development —
# re-download if not present:
wget -q https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip
unzip -q Godot_v4.3-stable_linux.x86_64.zip && chmod +x Godot_v4.3-stable_linux.x86_64

# Headless sanity check (parses the whole project, fails loudly on broken scene/script refs):
./Godot_v4.3-stable_linux.x86_64 --headless --path . --check-only

# Export to web (needs export templates installed + export_presets.cfg present):
./Godot_v4.3-stable_linux.x86_64 --headless --path . --export-debug "Web" build/web/index.html
```
A human with the Godot editor installed should open the project and actually click around — CLI
checks only prove "it parses and exports," not "it's fun" or "the physics feel right."

## Bugs found and fixed while validating headlessly
- `project.godot`'s original `[input]` section used invalid syntax (`ui_left=[keyboard:A]`) —
  not valid Godot 4 config, and it was **fatal**: it broke parsing of the entire project file, so
  nothing could load at all. Fixed by deleting that section; Godot's built-in `ui_left`/`ui_right`/
  `ui_accept` actions already default to arrow keys + Space/Enter, which is enough for paddle
  control. If WASD support is wanted later, add it properly through the Godot editor's Input Map
  UI (Project Settings → Input Map) rather than hand-writing the `InputEventKey` resource syntax —
  it's easy to get the keycode integers subtly wrong by hand.
- `ball.gd` referenced a `Trail2D` node type that doesn't exist anywhere in core Godot — it was
  presumably aspirational/copy-pasted. Implemented `src/gameplay/trail2d.gd` (a `Line2D` subclass
  with `top_level = true` recording the parent's position history) so the reference resolves.
- `ball.gd`/`paddle.gd` `preload()`d texture files (`res://assets/textures/ball_fire.png` etc.)
  that don't exist on disk — this is fatal at parse time, not just a runtime warning. Replaced
  with `ProceduralTexture` (generates flat-color circle/rect `ImageTexture`s at runtime) so the
  scripts have zero file dependencies until real art exists.
- `paddle.gd` never called `add_to_group("paddle")`, but `ball.gd`'s paddle-bounce logic checked
  `body.is_in_group("paddle")` — the ball would never have bounced correctly off the paddle. Fixed.
- **"Ball stops and disappears" (reported by owner 2026-06-16, fixed same day)** — two real bugs:
  (1) `game.tscn`/`game.gd` had **zero boundary colliders** on the left/right/top edges of the play
  area, so the ball could fly off-camera and never come back (the "disappears" — it didn't actually
  vanish, it just left the visible/playable area forever with nothing to bounce it back). Fixed by
  adding `spawn_walls()` in `game.gd`, which builds 3 `StaticBody2D` boundaries at runtime (no new
  scene files needed). (2) The ball had no `physics_material_override`, so Godot's default
  `bounce=0.0` made every collision fully inelastic — a square corner hit could zero out
  `linear_velocity` permanently (the "stops"), and the existing speed-renormalization in
  `_integrate_forces` only re-applied `current_speed` when `linear_velocity.length() > 0`, so a
  true zero vector stayed zero forever. Fixed by giving the ball `bounce=1.0, friction=0.0` and
  `can_sleep = false`, plus a defensive fallback in `_integrate_forces`: if speed ever drops below
  1.0 px/s, relaunch it on a slightly randomized upward vector instead of leaving it dead. Verified
  via Playwright screenshots taken a few seconds apart showing the ball's trail actually moving and
  staying on-screen, through a full life-loss → game-over → main-menu cycle.

## Known gaps / honest limitations
- `.github/workflows/ci-cd.yml` downloads the Godot editor but **never installs export templates**
  before calling `--export-debug` — that step will fail in CI as written. Needs a template-install
  step mirroring whatever was done locally (see `ROADMAP.md` Phase 1).
- GitHub Pages deploy in that same workflow won't work on a **private** repo without a paid GitHub
  plan. Until that's resolved, treat the `deploy-web`/`deploy-pages` jobs as aspirational; the
  practical web-hosting answer is likely Vercel (owner already has a Vercel account — see the
  owner's cross-project memory) or itch.io.
- Most of `GAME_DESIGN.md`'s power-ups/drops/rockets are **designed but not wired to gameplay
  yet** — only enough is implemented to prove the infinite loop works end-to-end.
- No save/cloud-save, no shop, no achievements yet — Phase 3 in `ROADMAP.md`.

## Working agreement for future sessions
- Update `ROADMAP.md` checkboxes as you complete items — don't let this file and that file say
  different things about status.
- Keep the "no art assets" constraint in mind: don't add `preload("res://assets/...")` calls for
  files that don't exist — it breaks parsing for everyone, not just at runtime.
- Branch + PR for all changes, per the standing rule above.
