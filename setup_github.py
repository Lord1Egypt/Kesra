import subprocess, json, sys, os

GH = "/root/.picoclaw/workspace/gh"
REPO = "Lord1Egypt/Kesra"

def gh(args, input_data=None):
    cmd = [GH] + args
    kwargs = {"capture_output": True, "text": True, "timeout": 30}
    if input_data:
        kwargs["input"] = input_data
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"⚠️  Error running {' '.join(args)}: {result.stderr.strip()}")
        return None
    return result.stdout.strip()

def gh_json(args):
    cmd = [GH] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"⚠️  Error: {result.stderr.strip()}")
        return None
    try:
        return json.loads(result.stdout)
    except:
        return result.stdout.strip()

# ─────────────────────────────────────────────
# 🏷️ 1. LABELS — Create all labels
# ─────────────────────────────────────────────
print("🏷️  Creating Labels...")

labels = [
    # Priority
    ("priority: critical", "B60205", "Must fix immediately"),
    ("priority: high", "FF0000", "High priority"),
    ("priority: medium", "FFA500", "Medium priority"),
    ("priority: low", "9C9C9C", "Low priority"),
    
    # Type
    ("type: feature", "00FF00", "New feature"),
    ("type: bug", "FF0000", "Bug report"),
    ("type: enhancement", "006B75", "Enhancement"),
    ("type: design", "1D76DB", "Design work"),
    ("type: documentation", "0E8A16", "Documentation"),
    ("type: refactor", "FEF2C0", "Code refactoring"),
    ("type: test", "E99695", "Testing"),
    ("type: ci/cd", "5319E7", "CI/CD pipeline"),
    ("type: performance", "BFD4D9", "Performance"),
    ("type: security", "000000", "Security"),
    
    # Worlds
    ("world: science", "D4C5F9", "World 1 — Scientific"),
    ("world: art", "F9D5C5", "World 2 — Artistic"),
    ("world: history", "C5F9D5", "World 3 — Historical"),
    ("world: geography", "C5D5F9", "World 4 — Geographical"),
    ("world: architecture", "F9C5D5", "World 5 — Architectural"),
    ("world: religion", "D5F9C5", "World 6 — Religious"),
    ("world: national", "F9E6C5", "World 7 — National"),
    ("world: logistics", "C5F9E6", "World 8 — Logistical"),
    ("world: space", "E6C5F9", "World 9 — Space & Rockets"),
    
    # Difficulty
    ("difficulty: easy", "C2E0C6", "Good for beginners"),
    ("difficulty: medium", "FBCA04", "Moderate difficulty"),
    ("difficulty: hard", "FF7619", "Hard task"),
    
    # Status
    ("status: blocked", "000000", "Blocked by something else"),
    ("status: in progress", "0075CA", "Currently working on it"),
    ("status: review needed", "FBBD04", "Needs code review"),
    ("status: done", "0E8A16", "Completed"),
    ("status: wontfix", "FFFFFF", "Won't do"),
    
    # Special
    ("good first issue", "7057FF", "Good for newcomers"),
    ("help wanted", "008672", "Extra attention needed"),
    ("boss", "B60205", "Boss fight related"),
    ("powerup", "1D76DB", "Power-up/drop related"),
    ("achievement", "0E8A16", "Achievement related"),
    ("easter egg", "5319E7", "Hidden content"),
]

for label_name, color, desc in labels:
    try:
        # First try to create
        result = subprocess.run(
            [GH, "api", f"repos/{REPO}/labels", "-f", f"name={label_name}", "-f", f"color={color}", "-f", f"description={desc}"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 or "already_exists" in result.stderr:
            print(f"  ✅ {label_name}")
        else:
            # Try updating color
            subprocess.run(
                [GH, "api", "--method", "PATCH", f"repos/{REPO}/labels/{label_name.replace(' ', '%20').replace(':', '%3A').replace('/', '%2F')}", "-f", f"color={color}", "-f", f"description={desc}"],
                capture_output=True, text=True, timeout=15
            )
            print(f"  ✅ {label_name} (updated)")
    except Exception as e:
        print(f"  ❌ {label_name}: {e}")

# ─────────────────────────────────────────────
# 🏁 2. MILESTONES
# ─────────────────────────────────────────────
print("\n🏁 Creating Milestones...")

milestones = [
    ("v0.1 — Foundation", "Core mechanics: paddle, ball, bricks, collisions", "2026-07-01T00:00:00Z"),
    ("v0.2 — Power-ups & Drops", "All drops, power-ups, rockets system", "2026-07-15T00:00:00Z"),
    ("v0.3 — Worlds 1-3", "Science, Art, History worlds + 3 bosses", "2026-08-01T00:00:00Z"),
    ("v0.4 — Worlds 4-6", "Geography, Architecture, Religion worlds", "2026-08-15T00:00:00Z"),
    ("v0.5 — Worlds 7-9", "National, Logistics, Space worlds", "2026-09-01T00:00:00Z"),
    ("v0.6 — Progression", "Shop, achievements, save/load, endless mode", "2026-09-15T00:00:00Z"),
    ("v0.7 — Polish", "Music, SFX, animations, UI overhaul", "2026-10-01T00:00:00Z"),
    ("v1.0 — Launch 🚀", "Android/iOS/Desktop release", "2026-10-15T00:00:00Z"),
    ("v1.1 — Content Update", "Secret worlds, new levels, community levels", "2026-11-01T00:00:00Z"),
    ("v2.0 — Godot 5", "Port to Godot 5, new engine features", ""),
]

for ms_title, ms_desc, ms_due in milestones:
    try:
        args = [GH, "api", f"repos/{REPO}/milestones",
                "-f", f"title={ms_title}",
                "-f", f"description={ms_desc}",
                "-f", "state=open"]
        if ms_due:
            args += ["-f", f"due_on={ms_due}"]
        result = subprocess.run(args, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 or "already_exists" in result.stderr:
            print(f"  ✅ {ms_title}")
        else:
            print(f"  ⚠️  {ms_title}: {result.stderr[:100]}")
    except Exception as e:
        print(f"  ❌ {ms_title}: {e}")

print("\n🎉 All done!" if True else "")
