"""Main entry point for data pipeline."""

import json
from reader import DataReader
from transformer import DataTransformer
from aggregator import DataAggregator

def main():
    """Run the data pipeline."""
    print("Starting data pipeline...")
    
    # Step 1: Read data
    reader = DataReader("input.csv")
    raw_data = reader.read()
    print(f"Read {len(raw_data)} records")
    
    # Step 2: Transform data
    transformer = DataTransformer()
    transformed_data = transformer.transform(raw_data)
    print(f"Transformed {len(transformed_data)} records")
    
    # Step 3: Aggregate by month
    aggregator = DataAggregator()
    aggregated = aggregator.aggregate_by_month(transformed_data)
    print(f"Aggregated into {len(aggregated)} monthly totals")
    
    # Step 4: Calculate total
    total = sum(item['total'] for item in aggregated)
    print(f"\nAggregated total: {total}")
    
    # Step 5: Save results
    output = {
        "monthly_totals": aggregated,
        "grand_total": total
    }
    
    with open("output.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to output.json")
    print(f"\naggregated_total: {total}")

if __name__ == "__main__":
    main()

