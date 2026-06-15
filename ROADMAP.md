# 🗺️ كِسرة — Development Roadmap

> "اللي جاي هيبقى نار" 🔥

---

## 🎯 Vision

**كِسرة** aims to be the most content-rich brick-breaker game ever made — an interactive encyclopedia of Egyptian civilization wrapped in addictive gameplay. **9 worlds, 100+ levels, 50+ power-ups, 12 bosses, 5 game modes, and infinite replayability.**

---

## 📅 Phases

### Phase 1: 🏗️ Foundation (v0.1) — ETA: Week 1-2

**Goal:** Core gameplay loop working

- [ ] Godot project setup with mobile-friendly config
- [ ] **Paddle** — movement, screen clamping, base physics
- [ ] **Ball** — launch, bounce physics, constant speed, trail effect
- [ ] **Bricks** — grid placement, hit detection, destruction
- [ ] **Collision** — all collision scenarios (ball↔brick, ball↔paddle, ball↔wall)
- [ ] **Level loading** from JSON files
- [ ] **Basic HUD** — score, lives, level number
- [ ] **1 playable level** (World 1-1: Astronomy)
- [ ] **.gitignore**, **LICENSE**, **README**
- [ ] **CI/CD pipeline** — Godot export for Linux/Windows/Web
- [ ] **Milestone:** `v0.1-alpha`

---

### Phase 2: 💎 Drops & Power-ups (v0.2) — ETA: Week 3-4

**Goal:** All items, power-ups, and rockets work

- [ ] **Drop system** — Common/Rare/Epic/Legendary drops from bricks
- [ ] **Drop collection** — magnet, auto-collect
- [ ] **Common drops**: Bronze Coin, Heart, Shield, Speed+
- [ ] **Rare drops**: Fireball, Wide Paddle, Multi-ball, Slow, Magnet
- [ ] **Epic drops**: Rocket, Laser, Star, Bomb, Chaos
- [ ] **Legendary drops**: Diamond, Ankh, Whirlwind, Eye of Horus, Aten
- [ ] **Rocket system**: Scarab → Khopesh → Neith Arrow → Sobek Trident → Ra's Spear
- [ ] **Power-up duration timers**
- [ ] **Stacking logic** for multiple active power-ups
- [ ] **5 levels** with increasing difficulty
- [ ] **Milestone:** `v0.2-alpha`

---

### Phase 3: 🌎 Worlds 1-3 (v0.3) — ETA: Month 2

**Goal:** Science, Art, and History worlds complete

#### 🧪 World 1: Scientific (8 levels)
- [ ] Level 1-1: Astronomy — Stars & Constellations
- [ ] Level 1-2: Mathematics — Numbers & Geometry
- [ ] Level 1-3: Medicine — Ancient Egyptian Medicine
- [ ] Level 1-4: Engineering — Building the Pyramids
- [ ] Level 1-5: Chemistry — Mummification
- [ ] Level 1-6: Botany — Papyrus & Farming
- [ ] Level 1-7: Zoology — Sacred Animals
- [ ] Level 1-8: **Boss: Imhotep** 🏆

#### 🎨 World 2: Artistic (6 levels)
- [ ] Level 2-1: Hieroglyphics — Writing System
- [ ] Level 2-2: Sculpture — Sphinx & Statues
- [ ] Level 2-3: Painting — Tomb Paintings
- [ ] Level 2-4: Jewelry — Gold & Gemstones
- [ ] Level 2-5: Music — Ancient Instruments
- [ ] Level 2-6: **Boss: Thoth** 🎨

#### 📜 World 3: Historical (8 levels)
- [ ] Level 3-1: Predynastic — Before the Pharaohs
- [ ] Level 3-2: Old Kingdom — Pyramids Era
- [ ] Level 3-3: Middle Kingdom — Renaissance
- [ ] Level 3-4: New Kingdom — Empire
- [ ] Level 3-5: Foreign Rule — Persians, Greeks, Romans
- [ ] Level 3-6: Islamic Era — Conquest & Civilization
- [ ] Level 3-7: Modern Egypt — Revolutions & Republic
- [ ] Level 3-8: **Boss: Ramesses II** 👑

- [ ] **Boss fight engine** — multi-phase bosses, weak points
- [ ] **Milestone:** `v0.3-alpha`

---

### Phase 4: 🌍 Worlds 4-6 (v0.4) — ETA: Month 3

#### 🌍 World 4: Geographical (6 levels)
- [ ] Level 4-1: The Nile — River of Life
- [ ] Level 4-2: Deserts — Eastern & Western
- [ ] Level 4-3: Oases — Siwa, Kharga, Dakhla
- [ ] Level 4-4: Red Sea — Coral Reefs
- [ ] Level 4-5: Cities — Governorates & Landmarks
- [ ] Level 4-6: **Boss: Hapi** 🌊

#### 🏛️ World 5: Architectural (8 levels)
- [ ] Level 5-1: Pyramids — The Great Three
- [ ] Level 5-2: Temples — Karnak, Luxor, Abu Simbel
- [ ] Level 5-3: Obelisks — Standing Stones
- [ ] Level 5-4: Tombs — Valley of the Kings
- [ ] Level 5-5: Fortresses — Saladin, Qaitbay
- [ ] Level 5-6: Mosques — Ibn Tulun, Muhammad Ali
- [ ] Level 5-7: Churches — Hanging Church
- [ ] Level 5-8: **Boss: Seshat** 🏛️

#### ☀️ World 6: Religious (8 levels)
- [ ] Level 6-1: Creation Myth — Nun & Atum
- [ ] Level 6-2: The Ennead — Nine Great Gods
- [ ] Level 6-3: Afterlife — Book of the Dead
- [ ] Level 6-4: Pharaoh as God — Divine Kingship
- [ ] Level 6-5: Monotheism — Akhenaten's Aten
- [ ] Level 6-6: Abrahamic Religions — Egypt in the Bible & Quran
- [ ] Level 6-7: Mysticism — Sufism
- [ ] Level 6-8: **Boss: Ra** ☀️

- [ ] **Milestone:** `v0.4-alpha`

---

### Phase 5: 🇪🇬 Worlds 7-9 (v0.5) — ETA: Month 4

#### 🇪🇬 World 7: National (8 levels)
- [ ] Level 7-1: Flag & Anthem
- [ ] Level 7-2: Revolution
- [ ] Level 7-3: Army
- [ ] Level 7-4: Suez Canal
- [ ] Level 7-5: Aswan Dam
- [ ] Level 7-6: Sports
- [ ] Level 7-7: Folk Culture
- [ ] Level 7-8: **Boss: Unity** 🇪🇬

#### 📦 World 8: Logistical (8 levels)
- [ ] Level 8-1: Quarrying
- [ ] Level 8-2: Transport on the Nile
- [ ] Level 8-3: Workforce Organization
- [ ] Level 8-4: Supply Chain
- [ ] Level 8-5: Ramp Systems
- [ ] Level 8-6: Irrigation
- [ ] Level 8-7: Trade Routes
- [ ] Level 8-8: **Boss: The Great Pyramid** 🏗️

#### 🚀 World 9: Space & Rockets (8 levels)
- [ ] Level 9-1: Early Flight — Abbas ibn Firnas
- [ ] Level 9-2: Rocket Science Basics
- [ ] Level 9-3: NARSS — Egyptian Space Agency
- [ ] Level 9-4: EgyptSat — Satellites
- [ ] Level 9-5: TIBA — Communications
- [ ] Level 9-6: Space Race
- [ ] Level 9-7: Mars Mission
- [ ] Level 9-8: **Boss: Falcon Heavy** 🚀

- [ ] **Milestone:** `v0.5-alpha`

---

### Phase 6: 🏆 Progression (v0.6) — ETA: Month 5

- [ ] **Shop system** — Paddle, Ball, Rocket upgrades
- [ ] **Currency system** — Bronze, Silver, Gold, Gems
- [ ] **Achievement system** — 50+ achievements
- [ ] **Save/Load** — persistent profile
- [ ] **Endless Mode** — procedurally generated levels
- [ ] **Challenge Mode** — daily/weekly challenges
- [ ] **Puzzle Mode** — strategic brick-breaking
- [ ] **Milestone:** `v0.6-beta`

---

### Phase 7: 🎨 Polish (v0.7) — ETA: Month 6

- [ ] **Music** — 9 world-specific soundtracks
- [ ] **SFX** — All sound effects
- [ ] **Animations** — Brick destruction, drops, boss attacks
- [ ] **Particle systems** — Sand, fire, gold, stardust
- [ ] **UI overhaul** — Egyptian-themed menus
- [ ] **Fonts** — Custom hieroglyphic-inspired font
- [ ] **Tutorial** — Interactive first-time experience
- [ ] **Difficulty balancing** — Full playtest
- [ ] **Milestone:** `v0.7-rc`

---

### Phase 8: 🚀 Launch (v1.0) — ETA: Month 7

- [ ] **Android build** — APK + Play Store ready
- [ ] **iOS build** — App Store ready
- [ ] **Desktop builds** — Windows, Linux, macOS
- [ ] **Web build** — itch.io / GitHub Pages
- [ ] **Leaderboards** — Global high scores
- [ ] **Cloud save** — Sync across devices
- [ ] **Marketing** — Trailer, screenshots, store pages
- [ ] **v1.0 Release!** 🎉

---

### Post-Launch (v1.1+)

- [ ] **World 10: Underworld** — Duat (afterlife world)
- [ ] **World 11: Future Egypt** — Cyberpunk 3000
- [ ] **World 12: Mini Mode** — 100×100 brick grid
- [ ] **Level Editor** — Players create their own levels
- [ ] **Community Workshop** — Share levels online
- [ ] **Multiplayer** — 2-player co-op / versus
- [ ] **Seasonal events** — Ramadan, Christmas, etc.
- [ ] **More languages** — French, German, Spanish

---

## 📊 Progress Tracker

```
Phase 1 🏗️  [          ] 0%
Phase 2 💎  [          ] 0%
Phase 3 🌍  [          ] 0%
Phase 4 🏛️  [          ] 0%
Phase 5 🚀  [          ] 0%
Phase 6 🏆  [          ] 0%
Phase 7 🎨  [          ] 0%
Phase 8 🚀  [          ] 0%
```

**Total: 0%** 🏁

---

## 🏅 Milestone Labels

- `v0.1` — Foundation (Weeks 1-2)
- `v0.2` — Power-ups (Weeks 3-4)
- `v0.3` — Worlds 1-3 (Month 2)
- `v0.4` — Worlds 4-6 (Month 3)
- `v0.5` — Worlds 7-9 (Month 4)
- `v0.6` — Progression (Month 5)
- `v0.7` — Polish (Month 6)
- `v1.0` — Launch (Month 7)

---

*Last updated: 2026-06-15*
