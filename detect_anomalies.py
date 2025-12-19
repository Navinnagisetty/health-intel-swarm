import pandas as pd
import numpy as np
import os

# --- 1. STATE DICTIONARY (For Decoding) ---
fips_to_state = {
    '01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas', '06': 'California',
    '08': 'Colorado', '09': 'Connecticut', '10': 'Delaware', '12': 'Florida', '13': 'Georgia',
    '15': 'Hawaii', '16': 'Idaho', '17': 'Illinois', '18': 'Indiana', '19': 'Iowa',
    '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana', '23': 'Maine', '24': 'Maryland',
    '25': 'Massachusetts', '26': 'Michigan', '27': 'Minnesota', '28': 'Mississippi', '29': 'Missouri',
    '30': 'Montana', '31': 'Nebraska', '32': 'Nevada', '33': 'New Hampshire', '34': 'New Jersey',
    '35': 'New Mexico', '36': 'New York', '37': 'North Carolina', '38': 'North Dakota', '39': 'Ohio',
    '40': 'Oklahoma', '41': 'Oregon', '42': 'Pennsylvania', '44': 'Rhode Island', '45': 'South Carolina',
    '46': 'South Dakota', '47': 'Tennessee', '48': 'Texas', '49': 'Utah', '50': 'Vermont',
    '51': 'Virginia', '53': 'Washington', '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming'
}

print("🕵️‍♂️ Starting Fraud Hunt (with Simulation)...")

file_path = 'outpatient.csv'
if not os.path.exists(file_path):
    print("❌ Error: outpatient.csv not found!")
    exit()

# --- 2. LOAD DATA ---
# We ONLY load what exists. We do NOT load 'Provider_State' because it's missing.
cols_to_load = ['Provider_ID', 'Billed_Amount']
df = pd.read_csv(file_path, usecols=cols_to_load)
print(f"   - Loaded {len(df):,} transactions.")

# --- 3. SIMULATE GEOGRAPHY ---
print("   - ⚠️ Missing State Data in Source: Simulating locations for demo...")
unique_providers = df['Provider_ID'].unique()
valid_fips = list(fips_to_state.keys())

# Randomly assign a state to each provider (Deterministic using seed 42)
np.random.seed(42)
provider_state_map = {pid: np.random.choice(valid_fips) for pid in unique_providers}

# Map the new fake states to the dataframe
df['State_Code'] = df['Provider_ID'].map(provider_state_map)

# --- 4. AGGREGATE ---
provider_stats = df.groupby('Provider_ID').agg({
    'Billed_Amount': ['mean', 'count', 'sum'],
    'State_Code': 'first'
})
# Flatten the multi-level columns
provider_stats.columns = ['Avg_Bill', 'Transaction_Count', 'Total_Revenue', 'State_Code']

# --- 5. DECODE STATES ---
# Turn '06' into 'California'
provider_stats['State_Full'] = provider_stats['State_Code'].map(fips_to_state)

# --- 6. STATISTICAL SCORING ---
active_providers = provider_stats[provider_stats['Transaction_Count'] > 10].copy()

global_mean = active_providers['Avg_Bill'].mean()
global_std = active_providers['Avg_Bill'].std()
active_providers['Z_Score'] = (active_providers['Avg_Bill'] - global_mean) / global_std

# --- 7. SAVE ---
output_file = 'enriched_providers.csv'
active_providers.to_csv(output_file)

print(f"\n✅ DATA SUCCESS.")
print(f"   - Created file: {output_file}")
print(f"   - Columns: {active_providers.columns.tolist()}")