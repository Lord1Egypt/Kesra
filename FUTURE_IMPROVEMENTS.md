# 🚀 Kesra — Future Improvements Master List

> Pick any item, branch off `main`, implement, PR. No order required.
> Items marked 🔥 are highest impact for fun. Items marked 💎 are highest visual wow.
> Items marked ✅ are already shipped.

---

## ✅ SHIPPED SO FAR
- AUTO PLAY mode + speed tabs (½× / 1× / 1.5× / 2×) + Egyptian loading screen
- Multi-Ball (×2 splitting, capped at 6 balls)  ·  Double Score star (×2 for 15s)
- Bomb (3×3 cluster destroy)  ·  Rocket / Row Buster (clears bottom row)
- Diamond (+1,000)  ·  sticky Magnet paddle (catch & re-launch)
- Pause menu (ESC/P → Resume / Restart / Menu)
- Ball aim-guide dotted line before launch
- Brick HP indicators on tough bricks  ·  Combo meter bar toward next ×8 milestone

---

## 🎮 POWER-UPS & BOOSTERS (drops from bricks)

1. ✅ 🔥 **Double Ball** — splits current ball into 2 identical balls; both stay alive *(shipped: `multi_ball`)*
2. 🔥 **Triple Ball** — splits into 3 balls at 120° spread
3. 🔶 🔥 **Multi-Ball Storm** — spawns 6 balls in a fan; chaos mode *(partial: ball cap is 6, fan spawn TODO)*
4. **Huge Ball** — ball radius ×3 for 10s; easier to hit paddle
5. **Tiny Ball** — ball radius ÷3, moves faster, fits through gaps
6. **Ghost Ball** — passes through bricks dealing damage without bouncing (1s of phase-through)
7. **Laser Ball** — ball leaves a laser trail that burns bricks it passes near
8. **Gravity Ball** — ball curves downward like a real ball, hard mode
9. ✅ **Sticky Ball (Magnet Catch)** — ball sticks to paddle on contact; re-launch manually *(shipped)*
10. 🔥 **Wide Paddle** — already exists, but add stacking (up to 3× width)
11. **Narrow Paddle** — challenge drop: paddle shrinks, score ×2 for the round
12. **Infinite Paddle** — paddle spans full width for 5s; god mode brief
13. **Speed Boost** — ball speed +40% for 8s
14. **Slow Motion** — everything slows to 50% for 6s; strategic window
15. 🔥 **Shield Wall** — a full-width barrier 100px above the bottom; ball bounces off it once
16. ✅ **Double Score** — all brick points ×2 for 15s *(shipped: `star`)*
17. **Coin Magnet** — all drops fly toward paddle for 12s
18. ✅ **Bomb** — explodes on contact, destroys a 3×3 cluster of bricks instantly *(shipped)*
19. ✅ 🔥 **Row Buster** — destroys the entire bottom row of bricks *(shipped: `rocket`)*
20. **Column Buster** — destroys a random full column top-to-bottom
21. 💎 **Lightning Strike** — bolt hits 5 random bricks, each takes 3 damage
22. 💎 **Meteor Rain** — 8 meteors fall and deal 2 damage each to random bricks
23. **Repair Kit** — restores 1 HP to the paddle shield if active
24. **Extra Life** — already exists (heart); add big golden heart collect animation
25. **Combo Freeze** — locks current combo multiplier for 20s; don't lose it on ball loss
26. **Coin Rain** — 20 gold coins rain down for 5s; collect all you can
27. **Freeze Ray** — all bricks frozen for 4s; ball passes through without triggering bounce
28. **Barrier OFF** — unbreakable wall bricks (future tier) become breakable for 10s
29. 🔥 **Rocket Barrage** — 3 rockets fire upward from paddle, each exploding on a brick
30. **Mirror Paddle** — a second ghost paddle at the top, deflecting the ball downward

---

## 🧱 BRICK TYPES & MECHANICS

31. **Armored Brick** — has a shield layer; must be hit twice before HP starts reducing
32. **Explosive Brick** — when destroyed, deals 1 damage to all 8 adjacent bricks
33. **Healing Brick** — slowly regenerates 1 HP every 5s (must kill quickly)
34. **Moving Brick** — slides left/right across its row, hard to hit
35. **Falling Brick** — drops down one row every 8s; eventually hits paddle zone
36. **Teleport Brick** — when hit, teleports ball to a random position
37. **Mirror Brick** — reflects ball at exact incoming angle (no normal bounce)
38. **Multiplier Brick** — worth 1000 pts but only 1 HP; golden shine effect
39. **Curse Brick** — when destroyed, shrinks paddle for 5s as penalty
40. **Chain Brick** — destroying it chains to adjacent bricks of same tier (domino)
41. **Ghost Brick** — invisible until ball gets within 60px; then reveals itself
42. **Boss Core Brick** — unbreakable until all normal bricks cleared; final mechanic
43. **Crystal Brick** — shatters into 4 shards that become tiny bricks scattered on screen
44. **Freeze Brick** — when destroyed, briefly freezes the ball for 0.5s
45. **Magnet Brick** — attracts the ball toward it, making it harder to avoid

---

## 👹 BOSS BATTLES

46. 🔥 **Boss Health Bar** — visible HP bar at top of screen during boss rounds
47. **Boss Phase 2** — at 50% HP boss spawns shield bricks that must be cleared first
48. **Boss Attack: Brick Repair** — boss heals 1 random brick every 3s
49. **Boss Attack: Drop Disable** — boss disables all power-up drops for 10s
50. **Boss Attack: Paddle Shrink** — boss zaps paddle to minimum width
51. **Boss Attack: Ball Redirect** — boss deflects ball with a force field once per 15s
52. **Boss Minion Bricks** — boss spawns extra indestructible bricks mid-round
53. **Super Boss (Sphinx)** — every 27th round (3rd cycle), ultra boss; multi-phase fight
54. **Boss Intro Cutscene** — 2s animated entrance: boss flies in from top with particles
55. **Boss Defeat Explosion** — 3-ring shockwave + 50 particles + screen flash on boss kill

---

## 💫 VISUAL EFFECTS

56. 💎 **Biome Background Art** — AI-generated images per biome (Gemini Imagen 4)
57. 💎 **Ball Skin: Fire** — ball wrapped in animated fire particles, orange/red trail
58. 💎 **Ball Skin: Ice** — blue crystalline ball, frost particle trail
59. 💎 **Ball Skin: Galaxy** — deep purple/blue ball with star sparkle trail
60. 💎 **Ball Skin: Ra's Sun** — golden ball with radiant sun-ray animation
61. 💎 **Brick Break Combo Animation** — at 16x combo, bricks shatter in gold slow-motion
62. **Screen Warp** — at high combo, screen edges pulse/breathe in biome color
63. **Parallax Stars** — background star layers move at different speeds (depth effect)
64. 💎 **Boss Aura** — boss bricks pulse with a halo glow that grows as boss HP drops
65. **Score Text Size** — big points popup (500+) renders larger and stays longer
66. **Biome Transition Fade** — full-screen fade through biome accent color on round change
67. **Rainbow Paddle** — paddle cycles through HSV colors at high combo
68. **Depth Shadow** — bricks cast a subtle drop shadow beneath them
69. **Sparkle Collect** — coins/drops emit sparkle burst when collected
70. 💎 **Victory Fountain** — clearing a round: gold particle fountain from all brick positions

---

## 🔊 SOUND & MUSIC

71. **Per-biome ambient track** — 9 looping musical themes (1 per biome)
72. **Brick hit SFX** — different sound per brick tier (mud=thud, gold=ding, obsidian=boom)
73. **Paddle hit SFX** — satisfying thwack; pitch shifts up on combo streak
74. **Combo voice line** — "Combo x8!" / "UNSTOPPABLE!" audio cues at milestones
75. **Ball launch SFX** — whoosh sound on Space press
76. **Power-up collect SFX** — unique sound per drop type
77. **Boss music** — intense drum/oud track replaces biome music during boss rounds
78. **Life lost SFX** — dramatic sting + brief silence
79. **Game over music** — melancholic Egyptian melody
80. **Level clear fanfare** — short triumphant horn burst on round clear

---

## 🏆 META PROGRESSION & ECONOMY

81. 🔥 **Persistent Shop** — spend bronze/silver/gold coins between rounds
82. **Paddle Upgrades** — buy wider, faster, or bouncier paddle in shop
83. **Ball Upgrades** — buy faster base speed or bigger ball permanently
84. **Starting Lives Upgrade** — spend coins to start with 4 or 5 lives
85. **Combo Shield** — buy: losing the ball doesn't reset combo (passive)
86. **Achievements System** — 30+ achievements with gold/silver/bronze badges
87. **Daily Challenge** — fixed seed round config, global leaderboard for that day
88. **Weekly Boss Rush** — survive 9 consecutive boss rounds; special reward
89. **Prestige System** — after round 99, reset for a permanent bonus multiplier
90. **Cosmetic Unlock: Paddle Skins** — gold/pharaoh/neon/obsidian paddle designs

---

## 💾 SAVE & ONLINE

91. ✅ **Local Save** — best score/round + settings to localStorage (web) / file (desktop) *(shipped: `storage.py`)*
92. 🔶 **Auto-save** — saves on game-over + play-start; per-round autosave still TODO
93. **Global Leaderboard** — top 100 scores with country flags
94. **Share Score** — "I scored 12,450 on Round 34!" copy-to-clipboard button
95. **Replay Last Run** — record ball/paddle positions, replay as ghost after game over

---

## 📱 PLATFORMS & INPUT

96. **Android APK** — Pygbag or Buildozer export; tap to control paddle
97. **iOS build** — macOS/Xcode toolchain required
98. **Gamepad support** — left stick / d-pad to move paddle, A to launch
99. **Gyroscope mode** — tilt phone to control paddle (mobile browser DeviceOrientation API)
100. **PWA (installable web app)** — manifest.json + service worker so it installs on home screen

---

## 🛠️ TECHNICAL & UX

101. ✅ **Pause menu** — ESC opens pause with Resume / Restart / Quit options *(shipped)*
102. **Settings screen** — volume, ball speed, colorblind mode, language toggle
103. **Colorblind mode** — swap brick colors to colorblind-safe palette
104. **FPS counter** — dev toggle (F3) to show FPS overlay
105. **Tutorial overlay** — first run: animated arrow shows "move paddle → press SPACE"
106. ✅ **Ball preview line** — dotted line showing ball trajectory before launch *(shipped: aim guide)*
107. **Slow-mo launch** — first 0.5s after launch runs at 30% speed (easy aim window)
108. ✅ **Brick HP indicators** — small number on each brick showing remaining HP *(shipped: tough bricks)*
109. ✅ **Combo meter UI** — visual bar that fills toward next ×8 combo milestone *(shipped)*
110. **Round preview** — show the brick grid layout before round starts (1s preview)

---

*Total: 110 items. Add more anytime — this list never closes.*
*"اللي جاي هيبقى نار" 🔥*
