"""Data aggregator module."""

from typing import List, Dict
from collections import defaultdict

class DataAggregator:
    """Aggregates data by various dimensions."""
    
    def aggregate_by_month(self, data: List[Dict]) -> List[Dict]:
        """Aggregate data by month.
        
        BUG: This function has a subtle bug in how it calculates totals.
        It's summing amounts but not accounting for quantity correctly.
        The total should be amount * quantity for each record, then sum by month.
        """
        monthly_data = defaultdict(lambda: {'total': 0.0, 'count': 0})
        
        for record in data:
            date = record['date']
            month_key = f"{date.year}-{date.month:02d}"
            
            # BUG: Only summing amount, not amount * quantity
            # Should be: record['amount'] * record['quantity']
            monthly_data[month_key]['total'] += record['amount']
            monthly_data[month_key]['count'] += 1
        
        # Convert to list format
        result = []
        for month, stats in sorted(monthly_data.items()):
            result.append({
                'month': month,
                'total': stats['total'],
                'count': stats['count']
            })
        
        return result

