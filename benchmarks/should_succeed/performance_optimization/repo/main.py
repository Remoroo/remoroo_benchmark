import time
import tracemalloc
import loader
import analyzer

def run_pipeline():
    # Start tracking memory
    tracemalloc.start()
    
    start_time = time.time()
    
    # 1. Load Data
    data = loader.load_data()
    
    # 2. Process Data
    result_count = analyzer.process_data(data)
    
    end_time = time.time()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = end_time - start_time
    peak_mb = peak / (1024 * 1024)
    
    print(f"Pipeline finished. Result count: {result_count}")
    print(f"runtime_s={runtime:.4f}")
    print(f"peak_memory_mb={peak_mb:.4f}")

if __name__ == "__main__":
    run_pipeline()
