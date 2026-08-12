"""
Domain data models for E-Commerce Checkout & Pricing Engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import uuid


class CustomerTier(Enum):
    STANDARD = "STANDARD"
    SILVER = "SILVER"
    GOLD = "GOLD"
    VIP_PLATINUM = "VIP_PLATINUM"


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    tier: CustomerTier = CustomerTier.STANDARD
    is_active: bool = True


@dataclass
class Item:
    item_id: str
    name: str
    unit_price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


@dataclass
class Voucher:
    code: str
    discount_percentage: float
    max_discount_amount: float
    is_active: bool = True
    expires_at: Optional[str] = None


@dataclass
class DiscountResult:
    original_amount: float
    discount_rate: float
    discount_amount: float
    final_amount: float
    applied_tier: str
    voucher_code: Optional[str] = None
    applied_rules: List[str] = field(default_factory=list)
    audit_event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
