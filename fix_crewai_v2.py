import os

# Path to the broken file
file_path = r"venv\Lib\site-packages\crewai\events\types\system_events.py"

print(f"🔍 Inspecting: {file_path}")

if not os.path.exists(file_path):
    print("❌ ERROR: File not found.")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We will replace the system calls with a dummy number '1' so Windows doesn't crash
replacements = {
    "signal.SIGHUP": "1",
    "signal.SIGTSTP": "1",
    "signal.SIGCONT": "1",
    "signal.SIGQUIT": "1"
}

new_content = content
count = 0

for old, new in replacements.items():
    if old in new_content:
        new_content = new_content.replace(old, new)
        count += 1
        print(f"   - Patched {old}")

if count > 0:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"\n✅ SUCCESS: Fixed {count} Windows incompatibility issues.")
    print("Your environment should now be stable.")
else:
    print("\n⚠️ INFO: No issues found (File might already be fixed).")