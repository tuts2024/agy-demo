"""
Unit tests for DiscountService.
"""

import unittest
from src.models import Customer, CustomerTier, Item, Voucher
from src.discount_service import DiscountService


class TestDiscountService(unittest.TestCase):

    def setUp(self):
        self.service = DiscountService()
        self.standard_cust = Customer("c-01", "Alice Smith", "alice@example.com", CustomerTier.STANDARD)
        self.silver_cust = Customer("c-02", "Bob Jones", "bob@example.com", CustomerTier.SILVER)
        self.gold_cust = Customer("c-03", "Carol White", "carol@example.com", CustomerTier.GOLD)
        
        self.cart_items = [
            Item("item-1", "Cloud Architecture Guide", 60.0, 1),
            Item("item-2", "Developer Mechanical Keyboard", 40.0, 1),
        ]

    def test_standard_customer_no_tier_discount(self):
        result = self.service.calculate_discount(self.standard_cust, self.cart_items)
        self.assertEqual(result.original_amount, 100.00)
        self.assertEqual(result.discount_amount, 0.00)
        self.assertEqual(result.final_amount, 100.00)

    def test_silver_customer_discount(self):
        result = self.service.calculate_discount(self.silver_cust, self.cart_items)
        self.assertEqual(result.original_amount, 100.00)
        self.assertEqual(result.discount_amount, 5.00)
        self.assertEqual(result.final_amount, 95.00)


if __name__ == "__main__":
    unittest.main()
