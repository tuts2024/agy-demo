"""
Unit tests for DiscountService.
REMEDIATED BY ANTIGRAVITY 2.0 AGENT - Comprehensive test coverage for PAY-204 Acceptance Criteria.
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
        self.vip_cust = Customer("c-04", "Diana Prince", "diana@example.com", CustomerTier.VIP_PLATINUM)
        
        self.cart_items = [
            Item("item-1", "Cloud Architecture Guide", 60.0, 1),
            Item("item-2", "Developer Mechanical Keyboard", 40.0, 1),
        ]  # Total subtotal = $100.00

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

    def test_vip_platinum_discount_20_percent(self):
        # ✅ Verified AC-1: VIP Platinum gets 20% discount ($20 off $100)
        result = self.service.calculate_discount(self.vip_cust, self.cart_items)
        self.assertEqual(result.original_amount, 100.00)
        self.assertEqual(result.discount_amount, 20.00)
        self.assertEqual(result.final_amount, 80.00)
        self.assertIn("TIER_VIP_PLATINUM_20%", result.applied_rules)

    def test_inactive_voucher_rejected(self):
        # ✅ Verified AC-2: Inactive voucher must not apply any discount
        inactive_voucher = Voucher(code="EXPIRED50", discount_percentage=50.0, max_discount_amount=25.0, is_active=False)
        result = self.service.calculate_discount(self.standard_cust, self.cart_items, voucher=inactive_voucher)
        self.assertEqual(result.discount_amount, 0.00)
        self.assertEqual(result.final_amount, 100.00)
        self.assertIn("VOUCHER_EXPIRED50_REJECTED_INACTIVE", result.applied_rules)

    def test_voucher_max_discount_cap_enforced(self):
        # ✅ Verified AC-2: Active voucher exceeding cap gets capped at max_discount_amount
        big_voucher = Voucher(code="MEGA30", discount_percentage=30.0, max_discount_amount=15.0, is_active=True)
        result = self.service.calculate_discount(self.standard_cust, self.cart_items, voucher=big_voucher)
        self.assertEqual(result.discount_amount, 15.00)  # Capped at $15 instead of 30% of $100 ($30)
        self.assertEqual(result.final_amount, 85.00)
        self.assertIn("VOUCHER_MEGA30_CAPPED", result.applied_rules)

    def test_combined_vip_tier_and_voucher(self):
        # VIP 20% ($20) + Voucher 10% ($10) = $30 discount ($70 final)
        voucher = Voucher(code="SUMMER10", discount_percentage=10.0, max_discount_amount=50.0, is_active=True)
        result = self.service.calculate_discount(self.vip_cust, self.cart_items, voucher=voucher)
        self.assertEqual(result.discount_amount, 30.00)
        self.assertEqual(result.final_amount, 70.00)

    def test_empty_cart_safety(self):
        result = self.service.calculate_discount(self.vip_cust, [])
        self.assertEqual(result.original_amount, 0.00)
        self.assertEqual(result.discount_amount, 0.00)
        self.assertEqual(result.final_amount, 0.00)


if __name__ == "__main__":
    unittest.main()
