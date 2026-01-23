import numpy as np
import pandas as pd
import os

def generate_data():
    np.random.seed(42)
    
    # 3 Groups
    # Group A: Centered at (10, 80), Slope -2
    # Group B: Centered at (30, 100), Slope -2
    # Group C: Centered at (50, 120), Slope -2
    # Global Trend of Centroids: slope +1
    
    groups = ['A', 'B', 'C']
    centers = [(10, 80), (30, 100), (50, 120)]
    n_per_group = 200
    
    msg_rows = []
    
    for g, (cx, cy) in zip(groups, centers):
        # x spread around center
        x = np.random.normal(cx, 5, n_per_group)
        # y = -2*x + intercept + noise
        # at mean: cy = -2*cx + intercept => intercept = cy + 2*cx
        intercept = cy + 2 * cx
        
        noise = np.random.normal(0, 4, n_per_group) # MSE ~ 16 locally
        y = -2 * x + intercept + noise
        
        for i in range(n_per_group):
            msg_rows.append({'x': x[i], 'y': y[i], 'group': g})
            
    df = pd.DataFrame(msg_rows)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    os.makedirs('repo', exist_ok=True)
    df.to_csv('repo/data.csv', index=False)
    
    print(f"Generated repo/data.csv with {len(df)} samples.")
    print("Underlying Model MSE should be around 16.0")
    print("A naive linear model ignoring groups will have much higher MSE.")

    # Create stub train.py
    with open('repo/train.py', 'w') as f:
        f.write("# TODO: Train model to predict y from x and group\n")

if __name__ == "__main__":
    generate_data()
