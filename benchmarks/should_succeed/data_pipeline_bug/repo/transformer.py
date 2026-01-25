"""Data transformer module."""

from typing import List, Dict
from datetime import datetime

class DataTransformer:
    """Transforms raw data into structured format."""
    
    def transform(self, raw_data: List[Dict]) -> List[Dict]:
        """Transform raw CSV data into structured format."""
        transformed = []
        
        for record in raw_data:
            try:
                # Parse date
                date_str = record.get('date', '')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Parse amount (handle both int and float strings)
                amount_str = record.get('amount', '0')
                amount = float(amount_str)
                
                # Parse quantity
                quantity_str = record.get('quantity', '0')
                quantity = int(float(quantity_str))  # Handle "1.0" -> 1
                
                transformed.append({
                    'date': date_obj,
                    'amount': amount,
                    'quantity': quantity,
                    'product': record.get('product', '')
                })
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping invalid record: {record} - {e}")
                continue
        
        return transformed

