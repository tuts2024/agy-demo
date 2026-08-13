#!/usr/bin/env python3
"""
Helper script to create a fresh, open GitHub Pull Request for live presentations.
Resets the base code on main, pushes the flawed feature branch, and opens a live PR.
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

WORKSPACE_DIR = Path(__file__).parent.resolve()

INITIAL_DISCOUNT_SERVICE_CODE = '''"""
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

    TIER_DISCOUNTS = {
        CustomerTier.STANDARD: 0.0,
        CustomerTier.SILVER: 0.05,
        CustomerTier.GOLD: 0.10,
        CustomerTier.VIP_PLATINUM: 0.10,  # ❌ BUG: 10% instead of required 20%
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

        tier_rate = self.TIER_DISCOUNTS.get(customer.tier, 0.0)
        tier_discount = round(subtotal * tier_rate, 2)
        
        if tier_rate > 0:
            applied_rules.append(f"TIER_{customer.tier.value}_{int(tier_rate*100)}%")

        # ❌ GAPS: Missing voucher.is_active check and max_discount_amount cap
        voucher_discount = 0.0
        voucher_code_applied = None
        if voucher is not None:
            raw_voucher_discount = round(subtotal * (voucher.discount_percentage / 100.0), 2)
            voucher_discount = raw_voucher_discount
            applied_rules.append(f"VOUCHER_{voucher.code}_{int(voucher.discount_percentage)}%")
            voucher_code_applied = voucher.code

        total_discount = min(subtotal, round(tier_discount + voucher_discount, 2))
        final_amount = round(subtotal - total_discount, 2)
        effective_rate = round(total_discount / subtotal, 4) if subtotal > 0 else 0.0

        return DiscountResult(
            original_amount=subtotal,
            discount_rate=effective_rate,
            discount_amount=total_discount,
            final_amount=final_amount,
            applied_tier=customer.tier.value,
            voucher_code=voucher_code_applied,
            applied_rules=applied_rules
        )
'''

INITIAL_TEST_CODE = '''"""
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
        self.vip_cust = Customer("c-04", "Diana Prince", "diana@example.com", CustomerTier.VIP_PLATINUM)
        
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

    def test_vip_platinum_discount_legacy(self):
        # ❌ Developer bug assertion: expecting $90 instead of $80
        result = self.service.calculate_discount(self.vip_cust, self.cart_items)
        self.assertEqual(result.original_amount, 100.00)
        self.assertEqual(result.discount_amount, 10.00)
        self.assertEqual(result.final_amount, 90.00)


if __name__ == "__main__":
    unittest.main()
'''

BASE_DISCOUNT_SERVICE = '''"""
Discount & Pricing Engine Service.
Contains baseline pricing calculation and customer loyalty tiers.
"""

from typing import Optional, List
from src.models import Customer, CustomerTier, Item, Voucher, DiscountResult
import logging

logger = logging.getLogger("discount_service")


class DiscountService:
    """Handles basic customer discount calculations."""

    TIER_DISCOUNTS = {
        CustomerTier.STANDARD: 0.0,
        CustomerTier.SILVER: 0.05,
        CustomerTier.GOLD: 0.10,
    }

    def calculate_cart_subtotal(self, items: List[Item]) -> float:
        if not items:
            return 0.0
        return round(sum(item.subtotal for item in items), 2)

    def calculate_discount(
        self,
        customer: Customer,
        items: List[Item],
        voucher: Optional[Voucher] = None
    ) -> DiscountResult:
        subtotal = self.calculate_cart_subtotal(items)
        tier_rate = self.TIER_DISCOUNTS.get(customer.tier, 0.0)
        tier_discount = round(subtotal * tier_rate, 2)
        total_discount = min(subtotal, tier_discount)
        final_amount = round(subtotal - total_discount, 2)
        effective_rate = round(total_discount / subtotal, 4) if subtotal > 0 else 0.0

        return DiscountResult(
            original_amount=subtotal,
            discount_rate=effective_rate,
            discount_amount=total_discount,
            final_amount=final_amount,
            applied_tier=customer.tier.value,
            applied_rules=[f"TIER_{customer.tier.value}"] if tier_rate > 0 else []
        )
'''

BASE_TESTS = '''"""
Unit tests for DiscountService baseline.
"""

import unittest
from src.models import Customer, CustomerTier, Item
from src.discount_service import DiscountService


class TestDiscountService(unittest.TestCase):

    def setUp(self):
        self.service = DiscountService()
        self.standard_cust = Customer("c-01", "Alice Smith", "alice@example.com", CustomerTier.STANDARD)
        self.silver_cust = Customer("c-02", "Bob Jones", "bob@example.com", CustomerTier.SILVER)
        self.cart_items = [
            Item("item-1", "Cloud Architecture Guide", 60.0, 1),
            Item("item-2", "Developer Mechanical Keyboard", 40.0, 1),
        ]

    def test_standard_customer_no_tier_discount(self):
        result = self.service.calculate_discount(self.standard_cust, self.cart_items)
        self.assertEqual(result.final_amount, 100.00)

    def test_silver_customer_discount(self):
        result = self.service.calculate_discount(self.silver_cust, self.cart_items)
        self.assertEqual(result.final_amount, 95.00)


if __name__ == "__main__":
    unittest.main()
'''


def create_github_pr(token: str, repo: str, title: str, head: str, base: str = "main", body: str = "") -> dict:
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-2.0-SDLC-Agent/2.0"
    }
    payload = json.dumps({"title": title, "head": head, "base": base, "body": body}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"GitHub API Error: {e}")
        return {}


def main():
    print("======================================================================")
    print("🚀 Initializing Live GitHub Pull Request for Demo...")
    print("======================================================================")

    env_file = WORKSPACE_DIR / ".env"
    if not env_file.exists():
        print("❌ .env file not found!")
        sys.exit(1)

    env = dict(line.strip().split('=', 1) for line in env_file.read_text().splitlines() if '=' in line and not line.startswith('#'))
    token = env.get('GITHUB_TOKEN', '').strip('\"\'')
    repo = env.get('GITHUB_REPOSITORY', '').strip('\"\'')
    if not token or not repo:
        print("❌ GITHUB_TOKEN or GITHUB_REPOSITORY missing from .env")
        sys.exit(1)

    push_url = f"https://x-access-token:{token}@github.com/{repo}.git"
    branch_name = "feature/checkout-loyalty-discounts"

    print("📦 1. Setting up baseline code on main...")
    subprocess.run(["git", "checkout", "main"], cwd=WORKSPACE_DIR, check=True)
    (WORKSPACE_DIR / "src" / "discount_service.py").write_text(BASE_DISCOUNT_SERVICE)
    (WORKSPACE_DIR / "tests" / "test_discount_service.py").write_text(BASE_TESTS)
    subprocess.run(["git", "add", "-A"], cwd=WORKSPACE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "chore(base): baseline checkout pricing engine", "--allow-empty"], cwd=WORKSPACE_DIR, check=True)
    subprocess.run(["git", "push", push_url, "main", "--force"], cwd=WORKSPACE_DIR, check=True)

    print(f"🌿 2. Creating feature branch '{branch_name}' with initial developer implementation...")
    subprocess.run(["git", "checkout", "-B", branch_name, "main"], cwd=WORKSPACE_DIR, check=True)
    (WORKSPACE_DIR / "src" / "discount_service.py").write_text(INITIAL_DISCOUNT_SERVICE_CODE)
    (WORKSPACE_DIR / "tests" / "test_discount_service.py").write_text(INITIAL_TEST_CODE)
    subprocess.run(["git", "add", "-A"], cwd=WORKSPACE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(checkout): Support loyalty discounts and voucher redemption [KAN-8]"], cwd=WORKSPACE_DIR, check=True)
    subprocess.run(["git", "push", push_url, f"{branch_name}", "--force"], cwd=WORKSPACE_DIR, check=True)

    print("🐙 3. Opening new Pull Request on GitHub...")
    pr_data = create_github_pr(
        token=token,
        repo=repo,
        title="feat(checkout): Support loyalty discounts and voucher redemption [KAN-8]",
        head=branch_name,
        base="main",
        body="""### Pull Request Description
Implements tiered customer loyalty discounts and promotional voucher redemption in the checkout service per JIRA specification [KAN-8].

#### Changes:
- Added `CustomerTier.VIP_PLATINUM` discount support.
- Added promotional voucher discount application.
- Added unit tests for VIP discount.

#### Related Jira Issue:
- **Story:** [KAN-8](https://ntuteja.atlassian.net) (Tiered Loyalty Discounts)
"""
    )

    if pr_data and pr_data.get("html_url"):
        pr_url = pr_data.get("html_url")
        pr_number = pr_data.get("number")
        print(f"\n🎉 Successfully created open Pull Request #{pr_number}!")
        print(f"👉 Live PR URL: {pr_url}")
        print(f"👉 Actions Tab: https://github.com/{repo}/actions")
    elif pr_data and pr_data.get("errors"):
        print(f"ℹ️ Pull request status: {pr_data.get('message', '')} - {pr_data.get('errors')}")
        print(f"👉 View open PRs at: https://github.com/{repo}/pulls")
    else:
        print(f"👉 View open PRs at: https://github.com/{repo}/pulls")


if __name__ == "__main__":
    main()
