import subprocess, json, sys, os

GH = "/root/.picoclaw/workspace/gh"
REPO = "Lord1Egypt/Kesra"

def gh(args, data=None):
    cmd = [GH] + args
    kwargs = {"capture_output": True, "text": True, "timeout": 30}
    if data:
        kwargs["input"] = json.dumps(data)
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"⚠️  {result.stderr.strip()[:200]}")
        return None
    try:
        return json.loads(result.stdout) if result.stdout else {}
    except:
        return result.stdout.strip()

# Get milestone IDs
milestones_raw = gh(["api", f"repos/{REPO}/milestones", "--jq", ".[] | {title: .title, number: .number}"])
milestones_raw = gh(["api", f"repos/{REPO}/milestones", "--jq", ".[] | {title: .title, number: .number}"])
if isinstance(milestones_raw, str) and milestones_raw:
    milestones_list = [json.loads(line) for line in milestones_raw.strip().split('\n') if line]
else:
    milestones_list = []
print(f"📋 Found {len(milestones_list)} milestones")

# Map milestone titles to numbers
milestone_map = {m["title"]: m["number"] for m in milestones_list}

# ─────────────────────────────────────────────────
# Create Issues
# ─────────────────────────────────────────────────
issues = [
    # Phase 1: Foundation
    {
        "title": "🏏 Core Paddle Implementation",
        "body": "**Objective:** Implement the paddle (Solar Barque) with:\n- [ ] Movement (A/D or arrow keys)\n- [ ] Screen clamping (stay within bounds)\n- [ ] Collision detection\n- [ ] Size adjustment for power-ups\n- [ ] Sticky mode (magnet power-up)\n- [ ] Fire effect visual",
        "labels": ["type: feature", "priority: critical", "difficulty: medium"],
        "milestone": "v0.1 — Foundation"
    },
    {
        "title": "⚡ Core Ball Physics",
        "body": "**Objective:** Implement the ball (Sun Disc) with:\n- [ ] Launch from paddle\n- [ ] Constant speed physics\n- [ ] Bounce reflection angles (based on paddle hit position)\n- [ ] Speed increment/decrement\n- [ ] Trail particle effect\n- [ ] Ball type system (stone→fire→lightning→explosive→void→solar)\n- [ ] Screen exit detection → lose life",
        "labels": ["type: feature", "priority: critical", "difficulty: medium"],
        "milestone": "v0.1 — Foundation"
    },
    {
        "title": "🧱 Brick System & Grid Layout",
        "body": "**Objective:** Implement bricks with:\n- [ ] Grid-based placement from JSON level data\n- [ ] 10 brick types (mud, stone, marble, granite, obsidian, gold, glass, mystery, shielded, cursed, gift)\n- [ ] Hit points system (1-10 HP)\n- [ ] Destruction animations (sand particles)\n- [ ] Points on destruction\n- [ ] Drop spawning on destruction\n- [ ] Brick type colors and visuals",
        "labels": ["type: feature", "priority: critical", "difficulty: medium"],
        "milestone": "v0.1 — Foundation"
    },
    {
        "title": "📄 JSON Level Loader",
        "body": "**Objective:** Load levels from JSON files:\n- [ ] File format specification\n- [ ] Parser for grid layout\n- [ ] Theme/background loading\n- [ ] Music reference loading\n- [ ] Fact display system\n- [ ] Fallback for missing files\n- [ ] Level progress tracking",
        "labels": ["type: feature", "priority: high", "difficulty: hard"],
        "milestone": "v0.1 — Foundation"
    },
    {
        "title": "🎮 CI/CD Pipeline Setup",
        "body": "**Objective:** Automated build pipeline:\n- [ ] GDScript linting\n- [ ] Godot export for Linux\n- [ ] Godot export for Windows\n- [ ] Godot export for Web\n- [ ] Godot export for Android\n- [ ] GitHub Pages deployment for web version\n- [ ] Release automation",
        "labels": ["type: ci/cd", "priority: high", "difficulty: medium"],
        "milestone": "v0.1 — Foundation"
    },
    
    # Phase 2: Drops
    {
        "title": "💎 Drop System — Common & Rare",
        "body": "**Objective:** Implement drops from bricks:\n### Common\n- [ ] Bronze Coin (+10 pts)\n- [ ] Heart (+1 life)\n- [ ] Shield (protect 1 life)\n- [ ] Speed+ (paddle speed boost)\n### Rare\n- [ ] Fireball (1-hit any brick)\n- [ ] Wide Paddle (2x width, 10s)\n- [ ] Multi-ball x2\n- [ ] Magnet (attract coins)\n- [ ] Slow (ball slow, 8s)",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "powerup"],
        "milestone": "v0.2 — Power-ups & Drops"
    },
    {
        "title": "💎♦️ Epic & Legendary Drops",
        "body": "**Objective:** Epic and Legendary drops:\n### Epic\n- [ ] Gold Coin (+200 pts)\n- [ ] Rocket (launch missiles)\n- [ ] Laser (piercing beam)\n- [ ] Star (2x points, 15s)\n- [ ] Bomb (explode nearby bricks)\n- [ ] Chaos (random effect)\n- [ ] Paddle Swap\n### Legendary\n- [ ] Diamond (+1000 pts)\n- [ ] Ankh (+1 max life)\n- [ ] Whirlwind (clear spiral path)\n- [ ] Eye of Horus (reveal hidden bricks)\n- [ ] Menat (collect all coins)\n- [ ] Canopic (reset brick layout)\n- [ ] Aten (clear all normal bricks)",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "powerup"],
        "milestone": "v0.2 — Power-ups & Drops"
    },
    {
        "title": "🚀 Rocket System",
        "body": "**Objective:** 5 rocket types:\n- [ ] Scarab Rocket — straight line, 1 brick\n- [ ] Khopesh Rocket — curved path, 3 bricks\n- [ ] Neith Arrow — splits into 3\n- [ ] Sobek Trident — 3 parallel rockets\n- [ ] Ra's Spear — destroys everything in path\n- [ ] Rocket power-up drops\n- [ ] Rocket aiming and firing animation",
        "labels": ["type: feature", "priority: medium", "difficulty: hard", "powerup"],
        "milestone": "v0.2 — Power-ups & Drops"
    },
    
    # Worlds
    {
        "title": "🧪 World 1: Scientific — All Levels",
        "body": "**Create all 8 levels for World 1:**\n- [ ] Level 1-1: Astronomy\n- [ ] Level 1-2: Mathematics\n- [ ] Level 1-3: Medicine\n- [ ] Level 1-4: Engineering\n- [ ] Level 1-5: Chemistry\n- [ ] Level 1-6: Botany\n- [ ] Level 1-7: Zoology\n- [ ] Level 1-8: **Boss: Imhotep**\n\nEach level needs:\n- Brick layout JSON\n- Educational facts\n- Themed background colors\n- Appropriate drops",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "world: science"],
        "milestone": "v0.3 — Worlds 1-3"
    },
    {
        "title": "🎨 World 2: Artistic — All Levels",
        "body": "**Create all 6 levels for World 2:**\n- [ ] Level 2-1: Hieroglyphics\n- [ ] Level 2-2: Sculpture\n- [ ] Level 2-3: Painting\n- [ ] Level 2-4: Jewelry\n- [ ] Level 2-5: Music\n- [ ] Level 2-6: **Boss: Thoth**",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "world: art"],
        "milestone": "v0.3 — Worlds 1-3"
    },
    {
        "title": "📜 World 3: Historical — All Levels",
        "body": "**Create all 8 levels for World 3:**\n- [ ] Level 3-1: Predynastic\n- [ ] Level 3-2: Old Kingdom\n- [ ] Level 3-3: Middle Kingdom\n- [ ] Level 3-4: New Kingdom\n- [ ] Level 3-5: Foreign Rule\n- [ ] Level 3-6: Islamic Era\n- [ ] Level 3-7: Modern Egypt\n- [ ] Level 3-8: **Boss: Ramesses II**",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "world: history"],
        "milestone": "v0.3 — Worlds 1-3"
    },
    
    # Progression
    {
        "title": "🏪 Shop & Upgrade System",
        "body": "**Objective:** Shop where players spend coins:\n- [ ] 7 Paddle tiers (Papyrus→Anubis)\n- [ ] 6 Ball types (Stone→Solar)\n- [ ] 5 Rocket types\n- [ ] Currency display\n- [ ] Purchase confirmation\n- [ ] Equip/unequip system\n- [ ] Visual upgrades on paddle/ball",
        "labels": ["type: feature", "priority: medium", "difficulty: hard"],
        "milestone": "v0.6 — Progression"
    },
    {
        "title": "🏅 Achievement System",
        "body": "**Objective:** 50+ achievements:\n### Beginner\n- [ ] Welcome to Egypt (first level)\n- [ ] First Coin\n- [ ] First Death 😂\n- [ ] Rocket Man\n- [ ] Student (complete World 1)\n### Intermediate\n- [ ] Archaeologist (all 9 worlds)\n- [ ] Pharaoh (50 levels)\n- [ ] Diamond Hands (10k gems)\n- [ ] Space Program (World 9)\n- [ ] Speed Runner\n- [ ] Combo King\n### Advanced\n- [ ] Collector (all drops)\n- [ ] Perfectionist (no misses)\n- [ ] Nightmare (Nightmare mode)\n- [ ] Legend (Level 100 endless)\n- [ ] Imhotep (all achievements)\n### Secret\n- [ ] 6 secret achievements (Easter eggs)",
        "labels": ["type: feature", "priority: medium", "difficulty: hard", "achievement"],
        "milestone": "v0.6 — Progression"
    },
    
    # Boss
    {
        "title": "👾 Boss Fight Engine",
        "body": "**Objective:** Reusable boss fight system:\n- [ ] Multi-phase boss state machine\n- [ ] Boss health bar UI\n- [ ] Weak point system (specific colored bricks)\n- [ ] Healing bricks (restore if hit slowly)\n- [ ] Boss attack patterns (projectiles, speed changes)\n- [ ] Victory/detection animations\n- [ ] Loot drops from bosses\n- [ ] 12 unique boss configurations",
        "labels": ["type: feature", "priority: high", "difficulty: hard", "boss"],
        "milestone": "v0.3 — Worlds 1-3"
    },
    
    # Endless
    {
        "title": "♾️ Endless Mode",
        "body": "**Objective:** Infinite procedural levels:\n- [ ] Procedural level generation algorithm\n- [ ] Difficulty scaling (speed, brick HP, density)\n- [ ] Score multiplier per level\n- [ ] Special endless-only drops\n- [ ] Leaderboard integration\n- [ ] Daily challenge generation",
        "labels": ["type: feature", "priority: medium", "difficulty: hard"],
        "milestone": "v0.6 — Progression"
    },
    
    # Polish
    {
        "title": "🎨 Egyptian UI Theme",
        "body": "**Objective:** Complete visual identity:\n- [ ] Papyrus scroll menus\n- [ ] Scarab beetle buttons\n- [ ] Ankh cross for lives\n- [ ] Sun disc for ball\n- [ ] Solar barque for paddle\n- [ ] Hieroglyphic font\n- [ ] Sand/gold color palette\n- [ ] Particle backgrounds (stars, sand, fire)",
        "labels": ["type: design", "priority: medium", "difficulty: medium"],
        "milestone": "v0.7 — Polish"
    },
    {
        "title": "🎵 Music & SFX System",
        "body": "**Objective:** Audio experience:\n### Music (9 soundtracks)\n- [ ] Scientific — Ambient+Electronic\n- [ ] Artistic — Harp+Flute\n- [ ] Historical — Epic Orchestral\n- [ ] Geographical — Nature Sounds\n- [ ] Architectural — Rhythmic\n- [ ] Religious — Mystical Chants\n- [ ] National — Patriotic\n- [ ] Logistical — Work Rhythms\n- [ ] Space — Synthwave 🚀\n### SFX\n- [ ] Brick break sounds\n- [ ] Drop collection\n- [ ] Combo pitch increase\n- [ ] Rocket whoosh+boom\n- [ ] Life loss\n- [ ] Boss roar\n- [ ] Level complete fanfare",
        "labels": ["type: feature", "priority: medium", "difficulty: hard"],
        "milestone": "v0.7 — Polish"
    },
    
    # Secret
    {
        "title": "🥚 Easter Eggs & Secret Content",
        "body": "**Objective:** Hidden surprises:\n- [ ] Konami Code → God Mode\n- [ ] \"Mo Salah\" hieroglyphs → Speed Boost\n- [ ] \"Lord1Egypt\" in menu → Pyramid Ship\n- [ ] Perfect level (ball never hits paddle) → Atlantis\n- [ ] 777 bricks in Level 9-7 → UFO steals ball\n- [ ] World 10: Underworld (Duat)\n- [ ] World 11: Future Egypt\n- [ ] World 12: Mini Mode",
        "labels": ["type: feature", "priority: low", "difficulty: hard", "easter egg"],
        "milestone": "v1.1 — Content Update"
    },
]

print(f"📝 Creating {len(issues)} issues...\n")
for i, issue in enumerate(issues, 1):
    # Build labels list
    labels = issue["labels"]
    
    # Get milestone number
    ms_num = milestone_map.get(issue.get("milestone", ""), None)
    
    # Create the issue
    data = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": labels
    }
    if ms_num:
        data["milestone"] = ms_num
    
    result = gh(["api", f"repos/{REPO}/issues", "--method", "POST", "--input", "-"], data)
    
    if result and isinstance(result, dict) and result.get("number"):
        print(f"  ✅ #{result['number']}: {issue['title'][:50]}...")
    else:
        print(f"  ❌ {issue['title'][:50]}...")

print(f"\n🎉 Done! Created issues!")
