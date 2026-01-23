import json
import re

class LegacyProcessor:
    def __init__(self, config):
        self.config = config
        self.processed_count = 0

    def process_data(self, data_list):
        results = []
        for item in data_list:
            # --- VALIDATION LOGIC (Mixed in) ---
            if not isinstance(item, dict):
                print(f"Skipping invalid item: {item}")
                continue
            
            if 'id' not in item or 'value' not in item:
                print(f"Skipping missing fields: {item}")
                continue
            
            if not isinstance(item['id'], int) or item['id'] < 0:
                print(f"Invalid ID: {item['id']}")
                continue

            # --- TRANSFORMATION LOGIC (Mixed in) ---
            # Normalize value
            val = str(item['value']).strip().lower()
            
            # Remove special chars
            val = re.sub(r'[^a-z0-9\s]', '', val)
            
            # Truncate if too long (legacy rule)
            if len(val) > 100:
                val = val[:100]
                
            # Enrich data
            processed_item = {
                'id': item['id'],
                'clean_value': val,
                'status': 'processed',
                'version': self.config.get('version', 1)
            }
            results.append(processed_item)
            self.processed_count += 1
            
        return results

    def get_stats(self):
        return {"count": self.processed_count}
