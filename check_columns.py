import pandas as pd
import glob
import os

print("🔍 DATASET COLUMN AUDIT\n")

# Find all CSV files in the current folder
csv_files = glob.glob("*.csv")

if not csv_files:
    print("❌ No CSV files found in this folder.")
else:
    for file in csv_files:
        try:
            # Read only the header (fast)
            df = pd.read_csv(file, nrows=0)
            columns = df.columns.tolist()
            
            print(f"📄 FILE: {file}")
            print(f"   Columns: {columns}")
            
            # Check for any column that looks like "State"
            state_matches = [col for col in columns if 'state' in col.lower()]
            
            if state_matches:
                print(f"   ✅ STATE DETECTED: {state_matches}")
            else:
                print("   ⚠️ No 'State' column found.")
                
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
            print("-" * 50)