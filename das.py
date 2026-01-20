import pandas as pd
import numpy as np

# 1. Load your Excel file
file_path = r'C:\Users\Dharmaraj\Favorites\Downloads\pyTest.xlsx'
df = pd.read_excel(file_path)

# 2. Define the column pairs
# You can list them manually or use a loop if the naming convention is strict
pairs = [
    ('index column name 1', 'index column value 1'),
    ('index column name 2', 'index column value 2'),
    # ... add all 10 pairs here
]

def clean_pairs(df, pairs):
    for name_col, value_col in pairs:
        # Check if either column is null (NaN)
        # .isna() detects empty cells in Excel/Pandas
        is_empty = df[name_col].isna() | df[value_col].isna()
        
        # Where the condition is true, fill both with "Not Applicable"
        df.loc[is_empty, name_col] = "Not Applicable"
        df.loc[is_empty, value_col] = "Not Applicable"
    
    return df

# 3. Execute cleaning
df_cleaned = clean_pairs(df, pairs)

# 4. Save the result into downloads folder
df_cleaned.to_excel(file_path, index=False)

print("Cleaning complete! Files saved as 'cleaned_data.xlsx'.")