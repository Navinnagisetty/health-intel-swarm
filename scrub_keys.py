import os
import glob
import re

# The pattern for a Google API Key (starts with AIza, followed by random chars)
key_pattern = re.compile(r'AIza[0-9A-Za-z\-_]{35}')

print("🧼 STARTING CLEANUP: Scrubbing keys from portfolio files...")

# Get all Python files
files = glob.glob("*.py")
cleaned_count = 0

for file in files:
    # Skip our utility scripts
    if file in ["scrub_keys.py", "security_scan.py", "detect_anomalies.py", "dashboard.py"]:
        continue
        
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Check if key exists
    if key_pattern.search(content):
        print(f"   ... Scrubbing key from: {file}")
        
        # Replace the hardcoded key with a secure environment variable fetch
        # It changes "AIzaSy..." to os.getenv("GOOGLE_API_KEY")
        new_content = key_pattern.sub('os.getenv("GOOGLE_API_KEY")', content)
        
        # Ensure 'import os' is present if we added os.getenv
        if "import os" not in new_content:
            new_content = "import os\n" + new_content
            
        # Overwrite the file with the clean version
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        cleaned_count += 1

print(f"\n✨ DONE! Cleaned {cleaned_count} files.")
print("   Your code logic is safe. The API keys are gone.")