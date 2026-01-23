import numpy as np
import pandas as pd
import os

def generate_data():
    np.random.seed(42)
    regions = ['US', 'UK']
    data = []
    
    # Generate ambiguous dates: days 1-12
    # For day D and month M where both <= 12:
    # US (MM/DD): 01/02 means Jan 2nd
    # UK (DD/MM): 01/02 means Feb 1st
    
    # We want to sum sales for January.
    # Case 1: 01/02/2023
    # If US: Jan 2nd -> Include
    # If UK: Feb 1st -> Exclude
    
    # Case 2: 02/01/2023
    # If US: Feb 1st -> Exclude
    # If UK: Jan 2nd -> Include
    
    sales_us_jan = 0
    sales_uk_jan = 0
    
    for i in range(100):
        val = 100.0
        
        # Ambiguous Date 1: 01/02/2023
        # US: Jan 2 -> Include
        data.append({'date': '01/02/2023', 'region': 'US', 'sales': val})
        sales_us_jan += val
        
        # UK: Feb 1 -> Exclude
        data.append({'date': '01/02/2023', 'region': 'UK', 'sales': val})
        
        # Ambiguous Date 2: 02/01/2023
        # US: Feb 1 -> Exclude
        data.append({'date': '02/01/2023', 'region': 'US', 'sales': val})
        
        # UK: Jan 2 -> Include
        data.append({'date': '02/01/2023', 'region': 'UK', 'sales': val})
        sales_uk_jan += val
        
        # Unambiguous Jan Date: 13/01/2023 (UK only format) or 01/13/2023 (US only)
        # Let's stick to ambiguous ones to maximize the trap.
        
    df = pd.DataFrame(data)
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    os.makedirs('repo', exist_ok=True)
    df.to_csv('repo/data.csv', index=False)
    
    total_jan_sales = sales_us_jan + sales_uk_jan
    print(f"Generated repo/data.csv with {len(df)} samples.")
    print(f"Correct Jan Sales: {total_jan_sales}")
    print("Trap: If you parse everything as US (MM/DD):")
    print("  01/02 (Jan 2) included for both US and UK. (UK should be Feb 1 - excluded)")
    print("  02/01 (Feb 1) excluded for both US and UK. (UK should be Jan 2 - included)")
    # Note: In this specific symmetric setup, the errors might cancel out if count is equal!
    # Let's break symmetry.
    
    # Add EXTRA ambiguous US-Jan rows (01/05)
    data_extra = []
    for i in range(50):
        val = 10.0
        # 01/05/2023
        # US: Jan 5 -> Include
        data_extra.append({'date': '01/05/2023', 'region': 'US', 'sales': val})
        total_jan_sales += val
        
        # UK: May 1 -> Exclude
        data_extra.append({'date': '01/05/2023', 'region': 'UK', 'sales': val})
        
    df_final = pd.concat([df, pd.DataFrame(data_extra)]).sample(frac=1, random_state=42).reset_index(drop=True)
    df_final.to_csv('repo/data.csv', index=False)
    
    print(f"Final True Jan Sales: {total_jan_sales}")

    # Create stub main.py
    with open('repo/main.py', 'w') as f:
        f.write(f"""
import pandas as pd
import json

def main():
    # TODO: Calculate total sales for January 2023
    # Look at 'region' to decide date format!
    pass

if __name__ == "__main__":
    main()
""")

    # Create verifier script to check result.txt
    with open('verifier.py', 'w') as f:
        f.write(f"""
import sys
import os

def verify():
    if not os.path.exists('repo/result.txt'):
        print("metric_name=accuracy_score value=0.0")
        return

    with open('repo/result.txt', 'r') as f:
        try:
            val = float(f.read().strip())
        except:
            print("metric_name=accuracy_score value=0.0")
            return
            
    expected = {total_jan_sales}
    if abs(val - expected) < 0.01:
        print("metric_name=accuracy_score value=1.0")
        print(f"Success: {{val}} matches expected {{expected}}")
    else:
        print("metric_name=accuracy_score value=0.0")
        print(f"Failure: {{val}} != expected {{expected}}")

if __name__ == "__main__":
    verify()
""")

if __name__ == "__main__":
    generate_data()
