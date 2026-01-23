import time

def process_data(data):
    """
    INEFFICIENT: O(N^2) processing logic.
    """
    print(f"Processing {len(data)} records...")
    
    unique_ids = []
    
    # Simulate work
    # Inefficient way to find unique items (O(N^2))
    # We'll validly just scan a subset to keep the baseline runnable but slow
    # Scanning 100k * 100k is too slow (10^10), let's just do a heavy loop on a subset
    # or simulate the inefficiency with a sleep if the N^2 is too brutal for a test.
    # Let's do a real O(N^2) but only on a slice to control the time to ~1.5s
    
    subset = data[:5000] # Check first 5000 against each other
    
    for item in subset:
        is_dup = False
        for existing in unique_ids:
            if item == existing:
                is_dup = True
                break
        if not is_dup:
            unique_ids.append(item)
            
    # Add artificial delay to represent the "rest" of the processing
    # that would be slow with the bad algorithm
    time.sleep(1.0)
    
    return len(unique_ids)
