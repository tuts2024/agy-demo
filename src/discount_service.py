"""
Discount & Pricing Engine Service.
Contains pricing calculation, tiered customer loyalty discounts, and voucher validation.
"""

from typing import Optional, List
from src.models import Customer, CustomerTier, Item, Voucher, DiscountResult
import logging

logger = logging.getLogger("discount_service")


class DiscountService:
    """
    Handles customer discount calculations and voucher redemptions.
    """

    # Note: Developer bug in PR #104 - VIP tier set to 0.10 instead of 0.20 (20%) per JIRA PAY-204 AC #1
    TIER_DISCOUNTS = {
        CustomerTier.STANDARD: 0.0,
        CustomerTier.SILVER: 0.05,
        CustomerTier.GOLD: 0.10,
        CustomerTier.VIP_PLATINUM: 0.10,  # ❌ BUG: Should be 0.20 (20%)
    }

    def calculate_cart_subtotal(self, items: List[Item]) -> float:
        """Calculate total amount before discounts."""
        if not items:
            return 0.0
        return round(sum(item.subtotal for item in items), 2)

    def calculate_discount(
        self,
        customer: Customer,
        items: List[Item],
        voucher: Optional[Voucher] = None
    ) -> DiscountResult:
        """
        Calculate total discount for a customer cart.
        
        Rules:
        1. Base discount from customer tier.
        2. Voucher discount if valid.
        3. Cap total discount to not exceed original amount.
        """
        subtotal = self.calculate_cart_subtotal(items)
        applied_rules = []

        if subtotal <= 0.0:
            return DiscountResult(
                original_amount=0.0,
                discount_rate=0.0,
                discount_amount=0.0,
                final_amount=0.0,
                applied_tier=customer.tier.value,
                applied_rules=["EMPTY_CART"]
            )

        # 1. Customer Tier Discount
        tier_rate = self.TIER_DISCOUNTS.get(customer.tier, 0.0)
        tier_discount = round(subtotal * tier_rate, 2)
        
        if tier_rate > 0:
            applied_rules.append(f"TIER_{customer.tier.value}_{int(tier_rate*100)}%")

        # 2. Voucher Logic (❌ BUG: Missing defensive check for inactive voucher or max discount cap)
        voucher_discount = 0.0
        voucher_code_applied = None

        if voucher is not None:
            # ❌ BUG: Does not check voucher.is_active or validate expiration date
            voucher_discount = round(subtotal * (voucher.discount_percentage / 100.0), 2)
            voucher_code_applied = voucher.code
            applied_rules.append(f"VOUCHER_{voucher.code}")

        total_discount = min(subtotal, tier_discount + voucher_discount)
        final_amount = round(subtotal - total_discount, 2)
        effective_rate = round(total_discount / subtotal, 4) if subtotal > 0 else 0.0

        # ❌ BUG: Missing structured audit log event (AC #4)

        return DiscountResult(
            original_amount=subtotal,
            discount_rate=effective_rate,
            discount_amount=total_discount,
            final_amount=final_amount,
            applied_tier=customer.tier.value,
            voucher_code=voucher_code_applied,
            applied_rules=applied_rules
        )
