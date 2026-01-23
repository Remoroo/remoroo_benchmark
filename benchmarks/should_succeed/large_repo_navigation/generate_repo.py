import os
import random

REPO_ROOT = "repo"
MODULES = [
    "auth", "inventory", "users", "notifications", "shipping",
    "catalog", "search", "recommendations", "payments", "orders",
    "returns", "analytics", "support", "content", "localization",
    "infrastructure", "monitoring", "logging", "config", "utils"
]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        f.write(content)

def generate_noise_file(module, name):
    return f"""
import time
import random

class {module.capitalize()}{name.capitalize()}Manager:
    def __init__(self):
        self.status = "active"
        self.last_update = time.time()
        
    def process(self, data):
        # Simulation of {module} logic
        if not data:
            return False
        return True
        
    def get_status(self):
        return self.status
"""

def generate_repo():
    ensure_dir(REPO_ROOT)
    
    # 1. Generate Noise Modules
    for mod in MODULES:
        write_file(f"{REPO_ROOT}/pkg/{mod}/__init__.py", "")
        # Create 3-5 files per module
        for i in range(random.randint(3, 5)):
            name = f"service_{i}"
            content = generate_noise_file(mod, name)
            write_file(f"{REPO_ROOT}/pkg/{mod}/{name}.py", content)
            
    # 2. Generate Target Module (Billing)
    write_file(f"{REPO_ROOT}/pkg/billing/__init__.py", "")
    
    # Target File
    billing_core = """
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
"""
    write_file(f"{REPO_ROOT}/pkg/billing/core.py", billing_core)
    
    # Test File
    billing_test = """
import unittest
from pkg.billing.core import InvoiceCalculator

class TestInvoiceCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = InvoiceCalculator(tax_rate=0.1) # 10% tax for simple math

    def test_calculate_normal(self):
        items = [{'price': 100, 'qty': 2}]
        # 100*2 = 200 + 10% = 220
        self.assertEqual(self.calc.calculate_invoice_total(items), 220.0)

    def test_negative_quantity_raises_error(self):
        items = [{'price': 100, 'qty': -1}]
        # Should raise ValueError, currently just returns negative
        with self.assertRaises(ValueError):
            self.calc.calculate_invoice_total(items)

if __name__ == '__main__':
    unittest.main()
"""
    write_file(f"{REPO_ROOT}/pkg/billing/test_billing.py", billing_test)
    
    # Root entry
    write_file(f"{REPO_ROOT}/main.py", "print('Enterprise ERP System v1.0')")

if __name__ == "__main__":
    generate_repo()
    print(f"Generated large repo in {os.path.abspath(REPO_ROOT)}")
