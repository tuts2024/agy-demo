"""
Discount & Pricing Engine Service.
Contains pricing calculation, tiered customer loyalty discounts, and voucher validation.
REMEDIATED BY ANTIGRAVITY 2.0 AGENT - Compliant with JIRA PAY-204 Acceptance Criteria.
"""

from typing import Optional, List
from src.models import Customer, CustomerTier, Item, Voucher, DiscountResult
import logging
import uuid

logger = logging.getLogger("discount_service")


class DiscountService:
    """
    Handles customer discount calculations and voucher redemptions.
    """

    # ✅ FIXED (AC-1): VIP Platinum tier upgraded to 20% (0.20 multiplier) per PAY-204
    TIER_DISCOUNTS = {
        CustomerTier.STANDARD: 0.0,
        CustomerTier.SILVER: 0.05,
        CustomerTier.GOLD: 0.10,
        CustomerTier.VIP_PLATINUM: 0.20,  # ✅ 20% discount rate
    }

    def calculate_cart_subtotal(self, items: List[Item]) -> float:
        """Calculate total amount before discounts."""
        if not items:
            return 0.0
        return round(sum(item.subtotal for item in items if item and item.quantity > 0), 2)

    def calculate_discount(
        self,
        customer: Customer,
        items: List[Item],
        voucher: Optional[Voucher] = None
    ) -> DiscountResult:
        """
        Calculate total discount for a customer cart with defensive validations.
        """
        subtotal = self.calculate_cart_subtotal(items)
        applied_rules = []
        audit_id = str(uuid.uuid4())

        if subtotal <= 0.0 or not customer:
            logger.info(f"[AUDIT {audit_id}] Empty cart calculation for customer={getattr(customer, 'customer_id', 'anon')}")
            return DiscountResult(
                original_amount=0.0,
                discount_rate=0.0,
                discount_amount=0.0,
                final_amount=0.0,
                applied_tier=getattr(customer, 'tier', CustomerTier.STANDARD).value if customer else "UNKNOWN",
                applied_rules=["EMPTY_CART"],
                audit_event_id=audit_id
            )

        # 1. Customer Tier Discount (AC-1)
        tier_rate = self.TIER_DISCOUNTS.get(customer.tier, 0.0)
        tier_discount = round(subtotal * tier_rate, 2)
        
        if tier_rate > 0:
            applied_rules.append(f"TIER_{customer.tier.value}_{int(tier_rate*100)}%")

        # 2. Defensive Voucher Validation & Cap Enforcement (AC-2)
        voucher_discount = 0.0
        voucher_code_applied = None

        if voucher is not None:
            if voucher.is_active:
                raw_voucher_disc = subtotal * (voucher.discount_percentage / 100.0)
                # Enforce max discount cap
                if voucher.max_discount_amount > 0:
                    voucher_discount = round(min(raw_voucher_disc, voucher.max_discount_amount), 2)
                    applied_rules.append(f"VOUCHER_{voucher.code}_CAPPED")
                else:
                    voucher_discount = round(raw_voucher_disc, 2)
                    applied_rules.append(f"VOUCHER_{voucher.code}")
                voucher_code_applied = voucher.code
            else:
                logger.warning(f"[AUDIT {audit_id}] Inactive voucher '{voucher.code}' rejected for customer {customer.customer_id}")
                applied_rules.append(f"VOUCHER_{voucher.code}_REJECTED_INACTIVE")

        total_discount = min(subtotal, round(tier_discount + voucher_discount, 2))
        final_amount = round(subtotal - total_discount, 2)
        effective_rate = round(total_discount / subtotal, 4) if subtotal > 0 else 0.0

        # ✅ Structured Audit Log Emission (AC-4)
        logger.info(
            f"[AUDIT {audit_id}] Discount computed: customer_id={customer.customer_id}, "
            f"tier={customer.tier.value}, subtotal=${subtotal:.2f}, "
            f"tier_discount=${tier_discount:.2f}, voucher_discount=${voucher_discount:.2f}, "
            f"total_discount=${total_discount:.2f}, final_amount=${final_amount:.2f}"
        )

        return DiscountResult(
            original_amount=subtotal,
            discount_rate=effective_rate,
            discount_amount=total_discount,
            final_amount=final_amount,
            applied_tier=customer.tier.value,
            voucher_code=voucher_code_applied,
            applied_rules=applied_rules,
            audit_event_id=audit_id
        )
