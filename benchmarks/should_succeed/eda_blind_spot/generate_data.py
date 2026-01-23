import numpy as np
import pandas as pd
import os

def generate_data():
    np.random.seed(42)
    n_samples = 500
    
    # Generate clean linear data: y = 3x + 5 + noise
    x = np.random.uniform(0, 100, n_samples)
    y = 3 * x + 5 + np.random.normal(0, 10, n_samples)
    
    # Introduce corruption: 10% of data has error code -999 in 'y'
    n_corrupt = int(0.1 * n_samples)
    corrupt_indices = np.random.choice(n_samples, n_corrupt, replace=False)
    y[corrupt_indices] = -999.0
    
    # Create DataFrame
    df = pd.DataFrame({'x': x, 'y': y})
    
    # Save to CSV
    os.makedirs('repo', exist_ok=True)
    df.to_csv('repo/data.csv', index=False)
    
    print(f"Generated repo/data.csv with {n_samples} samples ({n_corrupt} corrupted).")
    
    # Create empty train.py
    with open('repo/train.py', 'w') as f:
        f.write("# TODO: Implement model training here\n")

if __name__ == "__main__":
    generate_data()
