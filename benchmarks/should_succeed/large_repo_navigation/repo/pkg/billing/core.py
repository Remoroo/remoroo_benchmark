
class InvoiceCalculator:
    def __init__(self, tax_rate=0.08):
        self.tax_rate = tax_rate
        
    def calculate_invoice_total(self, items):
        total = 0.0
        for item in items:
            price = item.get('price', 0)
            qty = item.get('qty', 1)
            
            # BUG: Negative quantity allows for negative total invoice (refund exploit)
            # Should raise ValueError if qty < 0
            
            total += price * qty
            
        total_with_tax = total * (1 + self.tax_rate)
        return round(total_with_tax, 2)
