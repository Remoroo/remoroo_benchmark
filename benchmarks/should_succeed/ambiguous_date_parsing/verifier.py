
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
            
    expected = 20500.0
    if abs(val - expected) < 0.01:
        print("metric_name=accuracy_score value=1.0")
        print(f"Success: {val} matches expected {expected}")
    else:
        print("metric_name=accuracy_score value=0.0")
        print(f"Failure: {val} != expected {expected}")

if __name__ == "__main__":
    verify()
