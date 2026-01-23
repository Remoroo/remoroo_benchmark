"""Data pipeline with multiple validation requirements.

BUGS TO FIX:
1. Doesn't handle missing values (nulls) - should skip or fill them
2. Includes extra_field in output (schema violation)
3. Doesn't validate required fields before outputting
4. Output JSON structure is wrong (should be array of objects)

REQUIREMENTS (all must be met):
- records_processed >= 100
- null_count == 0 (no null/empty values in output)
- schema_valid == true (exactly these fields: id, name, email, score, category)

The Judge will inspect:
- output.json for correct structure
- artifacts/validation.json for metrics
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional


REQUIRED_FIELDS = ["id", "name", "email", "score", "category"]


def read_csv(filepath: str) -> List[Dict[str, Any]]:
    """Read CSV file into list of dictionaries."""
    records = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))
    return records


def transform_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a single record.
    
    BUG: Doesn't filter out extra fields!
    BUG: Doesn't handle empty/null values!
    """
    # BUG: Just returns the record as-is, including extra_field
    # Should only include REQUIRED_FIELDS
    transformed = {}
    for key, value in record.items():
        # BUG: Converts empty strings to None but still includes them
        if value == "":
            transformed[key] = None  # BUG: Should skip record instead
        else:
            transformed[key] = value
    return transformed


def validate_record(record: Dict[str, Any]) -> bool:
    """Check if record is valid.
    
    BUG: Validation is too permissive!
    """
    # BUG: Only checks if record is not empty
    # Should check all required fields exist and are non-null
    return len(record) > 0


def process_pipeline(input_file: str, output_file: str) -> Dict[str, Any]:
    """Process the data pipeline.
    
    BUGS:
    1. Includes records with null values
    2. Includes extra fields in output
    3. Doesn't properly count nulls
    """
    print(f"Reading from {input_file}...")
    raw_records = read_csv(input_file)
    print(f"  Read {len(raw_records)} raw records")
    
    print("Transforming records...")
    transformed = []
    null_count = 0
    
    for record in raw_records:
        t = transform_record(record)
        
        # BUG: This doesn't actually detect nulls properly
        # because transform_record includes None values
        if validate_record(t):
            transformed.append(t)
    
    print(f"  Transformed {len(transformed)} records")
    
    # BUG: Count nulls incorrectly (always 0)
    # Should count None values in transformed records
    for record in transformed:
        for value in record.values():
            if value is None:
                null_count += 1
    
    print("Writing output...")
    # BUG: Writing as dict with "data" key instead of just array
    output = {
        "data": transformed,  # BUG: Should just be the array
        "metadata": {
            "total": len(transformed)
        }
    }
    
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"  Wrote to {output_file}")
    
    # Check schema validity
    # BUG: Doesn't actually check if extra fields are present
    schema_valid = True
    for record in transformed[:5]:  # BUG: Only checking first 5
        for field in REQUIRED_FIELDS:
            if field not in record:
                schema_valid = False
                break
    
    # Prepare validation report
    validation = {
        "records_processed": len(transformed),
        "null_count": null_count,
        "schema_valid": schema_valid,
        "input_file": input_file,
        "output_file": output_file
    }
    
    # Save validation report
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/validation.json", "w") as f:
        json.dump(validation, f, indent=2)
    
    print(f"\nValidation Report:")
    print(f"  records_processed: {validation['records_processed']}")
    print(f"  null_count: {validation['null_count']}")
    print(f"  schema_valid: {validation['schema_valid']}")
    
    # Check requirements
    success = (
        validation["records_processed"] >= 100 and
        validation["null_count"] == 0 and
        validation["schema_valid"] == True
    )
    
    if success:
        print("\n✅ All requirements met!")
    else:
        print("\n❌ Requirements NOT met:")
        if validation["records_processed"] < 100:
            print(f"   - records_processed {validation['records_processed']} < 100")
        if validation["null_count"] != 0:
            print(f"   - null_count {validation['null_count']} != 0")
        if not validation["schema_valid"]:
            print(f"   - schema_valid is False")
    
    return validation


def main():
    """Run the pipeline."""
    print("=" * 60)
    print("DATA PIPELINE")
    print("=" * 60)
    print()
    
    validation = process_pipeline("input.csv", "output.json")
    
    print(f"\nMetrics saved to artifacts/validation.json")


if __name__ == "__main__":
    main()

