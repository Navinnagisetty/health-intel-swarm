import pandas as pd
import numpy as np

# We are simulating a mini-version of your healthcare data
# but with obvious errors to test the Agent's cleaning skills.
data = {
    'TransactionID': [101, 102, 103, 104, 105, 106],
    'Product': ['Laptop', 'Mouse', 'Monitor', 'Laptop', None, 'Mouse'], # None is a missing value
    'Region': ['North', 'South', 'East', 'North', 'West', 'South'],
    'Sales': [1000, 25, 300, 'MISSING', 450, 25], # 'MISSING' is a string error (dirty data)
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_filename = "messy_sales_data.csv"
df.to_csv(csv_filename, index=False)

print(f"✅ Created '{csv_filename}' successfully.")
print("   - This proves Python can WRITE to your disk.")