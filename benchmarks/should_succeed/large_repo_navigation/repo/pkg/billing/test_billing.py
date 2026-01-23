
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
