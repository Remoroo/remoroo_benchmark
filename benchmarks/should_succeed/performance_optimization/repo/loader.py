import time

def load_data(n=100000):
    """
    Simulates loading a large dataset.
    INEFFICIENT: Creates a massive list in memory immediately.
    """
    print(f"Loading {n} records...")
    # Simulate slow IO and memory pressure
    time.sleep(0.5) 
    
    # Create a large list of string data
    # Each string is ~100 bytes, 100k items = ~10MB raw, plus list overhead
    data = []
    for i in range(n):
        data.append(f"record_{i}_" + "x" * 80)
        
    return data
