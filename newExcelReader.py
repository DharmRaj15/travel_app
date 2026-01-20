import pandas as pd
import re

def clean_excel_dynamic(file_path, output_path):
    # 1. Load the data
    df = pd.read_excel(file_path)
    
    # 2. Identify all "name" columns using Regex
    # This looks for any column starting with 'index column name' followed by a number
    all_columns = df.columns.tolist()
    name_cols = [c for c in all_columns if re.search(r'index column name \d+', c)]
    
    pairs_processed = 0

    # 3. Iterate through found name columns and find their matching value columns
    for name_col in name_cols:
        # Extract the number from the name column (e.g., "1" from "name 1")
        suffix = re.search(r'\d+', name_col).group()
        value_col = f'index column value {suffix}'
        
        # Check if the matching value column actually exists in this specific file
        if value_col in df.columns:
            # Logic: If Name is empty OR Value is empty, set both to "Not Applicable"
            mask = df[name_col].isna() | df[value_col].isna()
            
            df.loc[mask, name_col] = "Not Applicable"
            df.loc[mask, value_col] = "Not Applicable"
            pairs_processed += 1
            
    # 4. Save the result
    df.to_excel(output_path, index=False)
    print(f"Processed {len(df)} rows and {pairs_processed} column pairs in {file_path}")

# Example Usage:
file_path = r'C:\Users\Dharmaraj\Favorites\Downloads\pyTest.xlsx'
output_path = r'C:\Users\Dharmaraj\Favorites\Downloads\cleaned_output.xlsx'
clean_excel_dynamic(file_path, output_path)