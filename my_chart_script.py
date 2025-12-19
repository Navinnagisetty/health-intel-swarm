import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Define the input and output
input_file = 'final_top_providers.csv'
output_file = 'final_chart.png'

print(f"📂 Reading {input_file}...")

try:
    # 2. Read the CSV
    df = pd.read_csv(input_file)
    
    # 3. Robust Data Extraction (Using Column Positions 0 and 1)
    # This prevents errors if column names change slightly
    x_data = df.iloc[:, 0].astype(str)  # 1st Column (Provider ID)
    y_data = df.iloc[:, 1]              # 2nd Column (Money)
    
    # Get the actual names for the chart title
    x_name = df.columns[0]
    y_name = df.columns[1]

    print(f"   - Found {len(df)} rows.")
    print(f"   - X-Axis: {x_name}")
    print(f"   - Y-Axis: {y_name}")

    # 4. Create the Chart
    plt.figure(figsize=(10, 6))
    plt.bar(x_data, y_data, color='skyblue', edgecolor='navy')
    
    # Formatting
    plt.xlabel('Provider ID')
    plt.ylabel('Billed Amount ($)')
    plt.title(f'Top 5 Providers by {y_name}')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Format Y-axis with dollar signs (optional but nice)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['${:,.0f}'.format(x) for x in current_values])

    # 5. Save
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
    
    print(f"\n✅ SUCCESS! Chart saved to: {os.path.abspath(output_file)}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")