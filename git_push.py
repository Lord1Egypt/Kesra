import subprocess, os

os.chdir("/root/.picoclaw/workspace/kesra")

cmds = [
    ["git", "init"],
    ["git", "config", "user.email", "lord1egypt@github.com"],
    ["git", "config", "user.name", "Lord1Egypt"],
    ["git", "add", "-A"],
]

for c in cmds:
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode:
        print("WARN:", r.stderr.strip()[:100])
    else:
        print("OK:", c[0], c[1] if len(c) > 1 else "")

msg = "🎮 Initial commit: Kesra - Egyptian Brick-Breaker"
r = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
print("COMMIT:", r.stdout.strip()[:200] if r.stdout else r.stderr.strip()[:200])

r = subprocess.run(["git", "remote", "add", "origin", "https://github.com/Lord1Egypt/Kesra.git"], capture_output=True, text=True)
print("REMOTE:", r.stdout.strip()[:100] if r.stdout else r.stderr.strip()[:100])

r = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True, timeout=30)
print("PUSH:", r.stdout.strip()[:500] if r.stdout else r.stderr.strip()[:500])
print("\nDONE!")
