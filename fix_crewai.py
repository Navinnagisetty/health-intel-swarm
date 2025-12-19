import os

# Path to the broken file inside your virtual environment
file_path = r"venv\Lib\site-packages\crewai\events\types\system_events.py"

print(f"🔍 Looking for file at: {file_path}")

if not os.path.exists(file_path):
    print("❌ ERROR: Could not find the file.")
    print("Make sure you are running this from the 'data-intel-swarm' folder")
    exit()

# Read the file
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The broken line is trying to access signal.SIGHUP
broken_text = "SIGHUP = signal.SIGHUP"
# We replace it with a dummy value (1) so Windows doesn't crash
fixed_text = "SIGHUP = 1 # signal.SIGHUP (Patched for Windows)"

if broken_text in content:
    new_content = content.replace(broken_text, fixed_text)
    
    # Write the fix back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("✅ SUCCESS: Patched 'crewai' for Windows compatibility.")
    print("You can now run your agents!")
else:
    print("⚠️ INFO: The text 'SIGHUP = signal.SIGHUP' was not found.")
    print("It might interpret indentation differently or be already fixed.")
    print("Try running the test script again.")