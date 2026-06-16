# Changelog

All notable changes to **كِسرة (Kesra)** will be documented here.

---

## [Unreleased] — v0.3 (Web + Art)

### 🔄 In Progress
- Pygbag CI → GitHub Pages auto-deploy (workflow running, verifying live URL)
- Gemini Imagen 4 biome backgrounds (needs ai.dev billing enabled)

---

## [v0.2.0] — 2026-06-17 — Python + Pygame Rewrite

### 🚀 Added
- Complete rewrite in Python + Pygame-CE replacing Godot 4.3 prototype
- Beautiful programmatic visuals: rainbow HSV ball trail, pre-baked glow surfaces, 3D bricks
- Particle system: burst explosions, ambient floating sparkles, expanding ring shockwaves
- Cairo.ttf bundled — correct Arabic rendering of كِسرة in all fonts
- `pygbag.ini` + `.github/workflows/web-deploy.yml` — automatic GitHub Pages deploy on push
- All 9 biomes with procedural backgrounds, accent colors, atmospheric center glow
- Screen shake on 8× combo multiples
- `assets/ui/kesra_logo.svg` — SVG logo with pyramids, Eye of Horus, Arabic كِسرة title

### 🐛 Fixed
- `GameOverScene.draw()` TypeError: `tuple(int,) * 3` → `(v, v, v)` literal (PR #23)
- `pygbag.ini` crash: `ignore_dirs`/`ignore_files` in `[pygbag]` section caused
  `AttributeError: 'Config' object has no attribute 'DEPENDENCIES'` (PR #24)
- README release badge showed "unable to select next github token from pool" (shields.io
  rate limit on dynamic endpoint) — replaced with static badge (PR #25)

---

## [v0.1.0] — 2026-06-16 — Godot Prototype

### 🚀 Added
- Godot 4.3 project initialization (now superseded by Python rewrite)
- Infinite core: 9 biomes cycling forever, procedural round generator
- Ball boundary walls + elastic physics (bounce=1.0) — fixed "ball stops" bug
- Windows Desktop export: `Kesra.exe` (PE32+, ~84MB, self-contained)
- Web export: Pygbag-compatible HTML5 build
- GitHub Release `v0.1-infinite-core` with Windows + Web attachments
- GitHub Actions CI/CD pipeline

### 🐛 Fixed
- Ball stops and disappears: missing boundary walls + Godot's default `bounce=0.0` fully
  inelastic physics — added `spawn_walls()` + `physics_material_override` (bounce=1.0)

---

*"كل حاجة بتتبني بلبنة لبنة."* 🧱
