import glob

print("🕵️‍♂️ SECURITY SCAN: Checking for hidden keys...")
files = glob.glob("*.py")
clean = True

for file in files:
    # Skip the scanner itself
    if file == "security_scan.py": continue
    
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        # Look for the pattern "AIza" (Google Key Start)
        if "AIza" in content and "GOOGLE_API_KEY" not in content:
            print(f"❌ DANGER: Hardcoded key found in: {file}")
            print("   -> DELETE this file or remove the key inside it.")
            clean = False

if clean:
    print("\n✅ SECURE: No exposed keys found. Ready for GitHub.")
else:
    print("\n⚠️ DO NOT UPLOAD YET. Fix the files listed above.")