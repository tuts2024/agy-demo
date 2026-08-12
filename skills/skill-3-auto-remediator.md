---
name: auto-remediator
trigger: on-remediation-signal
description: Autonomous self-healing agent that parses REMEDIATION_REQUIRED tasks, generates code fixes, updates unit tests, executes test suites, and verifies resolution.
---

# Skill: Autonomous Code Remediator

## Purpose
Acts as the self-healing remediation loop. When the Code Architect Reviewer detects defects or incomplete criteria, the Auto-Remediator automatically implements the missing logic, writes comprehensive unit tests, executes the test suite to ensure green builds, and posts a verified remediation summary.

## Trigger
- CI/CD workflow detects `needs_remediation=true` or `REMEDIATION_REQUIRED` string in review report.

## Instructions

1. **Parse Remediation Directives**:
   - Extract the list of required fixes from `remediation_task` environment variable or review report.
   - Identify targeted source and test files.

2. **Execute Autonomous Code Fixes**:
   - Update `TIER_DISCOUNTS[CustomerTier.VIP_PLATINUM]` to `0.20` (20%).
   - Implement defensive voucher validation: check `voucher.is_active`, validate expiration, enforce `voucher.max_discount_amount` cap.
   - Add structured logging using standard library logging with `audit_event_id`, `customer_id`, `subtotal`, and `total_discount`.

3. **Update & Expand Unit Tests**:
   - Fix `test_vip_platinum_discount_legacy` to assert $20.00 discount on $100 subtotal ($80.00 final amount).
   - Add `test_inactive_voucher_rejected` verifying that inactive vouchers are skipped.
   - Add `test_voucher_max_discount_cap_enforced` verifying discount capping.
   - Add `test_null_and_empty_cart_safety` verifying zero-dollar cart resilience.

4. **Verify Test Suite**:
   - Execute `python3 -m unittest discover tests` or `pytest`.
   - Verify that 100% of test cases pass cleanly.

5. **Generate Remediation Log**:
   - Save execution results to `reports/remediation-log-PR[number].md`.
   - Update PR comment with commit details and green test run confirmation.
