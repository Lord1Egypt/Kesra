<p align="center">
  <img src="assets/ui/kesra_logo.png" alt="كِسرة Logo" width="300"/>
</p>

<h1 align="center">🏛️ كِسرة — Egyptian Brick-Breaker 🚀</h1>

<p align="center">
  <b>9 Worlds • 100+ Levels • 50+ Power-ups • 12 Bosses • ∞ Replayability</b>
</p>

<p align="center">
  <i>"محصلتش قبل كده ولا هتحصل"</i>
</p>

<p align="center">
  <a href="https://github.com/Lord1Egypt/Kesra/releases"><img src="https://img.shields.io/github/v/release/Lord1Egypt/Kesra?color=FFD700&label=Release&style=flat-square" alt="Release"/></a>
  <a href="https://github.com/Lord1Egypt/Kesra/actions"><img src="https://img.shields.io/github/actions/workflow/status/Lord1Egypt/Kesra/ci-cd.yml?style=flat-square&logo=github" alt="CI/CD"/></a>
  <a href="https://github.com/Lord1Egypt/Kesra/issues"><img src="https://img.shields.io/github/issues/Lord1Egypt/Kesra?style=flat-square&color=red" alt="Issues"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Lord1Egypt/Kesra?style=flat-square" alt="License"/></a>
  <img src="https://img.shields.io/badge/Engine-Godot%204.x-%23478cbf?style=flat-square&logo=godotengine" alt="Godot"/>
  <img src="https://img.shields.io/badge/Platform-Android%20%7C%20iOS%20%7C%20Desktop%20%7C%20Web-blue?style=flat-square" alt="Platform"/>
</p>

---

## 🌟 Overview

**كِسرة (Kesra)** is not just a brick-breaker game — it's an **interactive journey through Egyptian civilization**, from the pyramids to space exploration.

Built with **Godot 4.x**, Kesra combines classic **Arkanoid/Breakout** gameplay with an **educational RPG-like progression system** that spans **9 knowledge domains**:

| # | World (Biome) | Theme | Rounds/Cycle | Recurring Boss |
|---|-------|-------|--------|------|
| 🧪 | **Scientific** | Astronomy, Math, Medicine | 8 | Imhotep |
| 🎨 | **Artistic** | Hieroglyphics, Sculpture, Music | 6 | Thoth |
| 📜 | **Historical** | Kingdoms, Conquests, Revolutions | 8 | Ramesses II |
| 🌍 | **Geographical** | Nile, Deserts, Red Sea | 6 | Hapi |
| 🏛️ | **Architectural** | Pyramids, Temples, Mosques | 8 | Seshat |
| ☀️ | **Religious** | Mythology, Monotheism, Mysticism | 8 | Ra |
| 🇪🇬 | **National** | Flag, Army, Suez Canal | 8 | Nebty |
| 📦 | **Logistical** | Quarrying, Transport, Trade | 8 | Khufu |
| 🚀 | **Space & Rockets** | Satellite, Mars, NARSS | 8 | NARSS Director |

Biomes **cycle forever** — after World 9 it loops back to World 1, harder than before. There is
no final world and no ending.

### 🏆 Super Boss: **The Great Sphinx** 🪦
1000-brick boss that returns every few cycles to test your knowledge of ALL Egyptian civilization!

---

## 🎮 Features

### 🕹️ Gameplay
- **♾️ Infinite by design** — no level cap, no ending. The 9 worlds are biomes that cycle
  forever, getting harder and rewarding rarer drops every cycle.
- **Classic brick-breaking** with **50+ power-ups & drops**
- **Combo system** — chain hits for massive score multipliers
- **Endless core + Challenge, Tournament, Puzzle modifiers** layered on top
- **9 recurring boss fights** that come back stronger every cycle instead of being beaten once
- **Rocket system**: 5 types from Scarab to Ra's Spear

### 📚 Educational
- Every level teaches **real history, science, art & culture**
- **Hieroglyphic translations**, **architectural facts**, **astronomical data**
- Built-in **encyclopedia** of Egyptian civilization

### 🎯 Progression
- **Shop system** with 7 paddle tiers, 6 ball types, 5 rocket types
- **50+ achievements** (including secret ones 🥚)
- **4 currencies**: Bronze, Silver, Gold, Gems
- **Save/load** across devices

### 🎨 Visual & Audio
- **Egyptian-themed art**: Papyrus scrolls, scarab beetles, ankh crosses
- **Dynamic music** that changes per world (orchestral → synthwave)
- **Particle effects**: sand, fire, gold, stardust
- **9 color palettes** matching each world's theme

---

## 📱 Platforms

| Platform | Status |
|----------|--------|
| 🌐 **Web (HTML5)** | 🟡 In progress — primary target right now |
| 🖥️ **Windows / Linux / macOS** | 🔴 Planned (export config exists, untested) |
| 🤖 **Android** | 🔄 Planned next after web |
| 🍏 **iOS** | 🔄 Planned after Android |

---

## 🚀 Quick Start

### Play Now
1. Go to **[Releases](https://github.com/Lord1Egypt/Kesra/releases)**
2. Download your platform's build
3. Extract and run!

### Build from Source

```bash
# Clone
git clone https://github.com/Lord1Egypt/Kesra.git
cd Kesra

# Open with Godot 4.x
# File → Import → Select project.godot
# Run ▶️
```

### Requirements
- **[Godot 4.3+](https://godotengine.org/download/)** (for development)
- **Android**: JDK 17, Android SDK (for mobile builds)

---

## 🏗️ Architecture

```
kesra/
├── assets/              # Game assets
│   ├── audio/           # Music & SFX
│   ├── fonts/           # Egyptian-themed fonts
│   ├── textures/        # Bricks, backgrounds, items
│   └── ui/              # UI elements
├── src/                 # Source code
│   ├── core/            # Core game systems
│   ├── gameplay/        # Paddle, ball, bricks, drops
│   ├── systems/         # Combo, shop, achievements
│   ├── worlds/          # World-specific content
│   ├── bosses/          # Boss fight scripts
│   └── ui/              # Menus, HUD, shop UI
├── levels/              # Level data (JSON)
├── .github/             # CI/CD, templates
├── project.godot        # Godot project file
└── README.md            # You are here!
```

---

## 🤝 Contributing

**Kesra is open-source!** We welcome all contributions:

- 🐛 **Report bugs** — [Open an issue](https://github.com/Lord1Egypt/Kesra/issues/new?template=bug_report.md)
- ✨ **Suggest features** — [Feature request](https://github.com/Lord1Egypt/Kesra/issues/new?template=feature_request.md)
- 🌍 **Propose worlds** — [World request](https://github.com/Lord1Egypt/Kesra/issues/new?template=world_request.md)
- 💎 **Design power-ups** — [Power-up idea](https://github.com/Lord1Egypt/Kesra/issues/new?template=powerup_request.md)
- 🎨 **Create assets** — Art, music, UI
- 💻 **Write code** — GDScript, Godot
- 📝 **Translate** — Arabic, English, and more!

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 🗺️ Roadmap

The game has **no "launch and done" milestone** — it's built as an infinite, continuously
updated core loop. See [ROADMAP.md](ROADMAP.md) for the live phase checklist:

| Phase | Milestone | Status |
|-------|-----------|--------|
| 🏗️ v0.1-infinite-core | Infinite core loop (paddle, ball, procedural rounds, bricks, drops) | 🟡 In progress |
| 🌐 v0.2-web | Playable in a browser tab | 🔴 Not started |
| 🎨 v0.3-feel | Full power-up/rocket/particle pass | 🔴 Not started |
| 🏆 v0.4-meta | Shop, achievements, cloud save | 🔴 Not started |
| 📱 v0.5-mobile | Android + iOS builds | 🔴 Not started |
| ♾️ Seasons | Ongoing content drops, forever | 🔴 Not started |

---

## 📜 License

**Kesra** is open-source under the **MIT License**.

Built with ❤️ by **Mohamed (Lord1Egypt)** 🇪🇬

---

<p align="center">
  <img src="https://img.shields.io/badge/مصر-أم_الدنيا-red?style=for-the-badge" />
  <br>
  <i>"العلم نور، والجهل ظلام — والتكسير أحلى ما في الدنيا"</i>
</p>
