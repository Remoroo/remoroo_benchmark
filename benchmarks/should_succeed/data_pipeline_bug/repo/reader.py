"""Data reader module."""

import csv
from typing import List, Dict

class DataReader:
    """Reads data from CSV files."""
    
    def __init__(self, filename: str):
        self.filename = filename
    
    def read(self) -> List[Dict]:
        """Read CSV file and return list of dictionaries."""
        data = []
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Error: File {self.filename} not found")
            return []
        
        return data

