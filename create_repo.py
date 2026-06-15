import subprocess, sys

result = subprocess.run(
    ["/root/.picoclaw/workspace/gh", "repo", "create", "Lord1Egypt/Kesra", "--public",
     "--description", "كِسرة — Egyptian Brick-Breaker Game. 9 Worlds, 100+ Levels!",
     "--homepage", "https://github.com/Lord1Egypt/Kesra"],
    capture_output=True, text=True, timeout=15
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("RC:", result.returncode)
