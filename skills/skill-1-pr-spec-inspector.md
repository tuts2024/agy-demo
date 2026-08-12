---
name: pr-spec-inspector
trigger: automatic
description: Inspects GitHub Pull Requests, extracts linked Jira issue keys, and retrieves Acceptance Criteria specifications for automated architectural review.
---

# Skill: PR & Jira Spec Inspector

## Purpose
Acts as the initial intake step for CI/CD automated review. Analyzes incoming Pull Request metadata, identifies linked Jira issues or product specifications, and compiles a unified context mapping PR diffs against declared Acceptance Criteria.

## Trigger
- GitHub `pull_request` event (opened, synchronized)
- Manual workflow dispatch with `pr_number`

## Instructions

1. **Extract PR Context**:
   - Parse PR title, branch name, author, and description.
   - Extract Jira issue keys matching standard regex: `[A-Z]{2,10}-[0-9]{1,6}` (e.g. `PAY-204`).
   - Extract list of modified and added files.

2. **Retrieve Requirements & Acceptance Criteria**:
   - Query Jira API / MCP tool for the referenced ticket.
   - Extract summary, description, and list of discrete Acceptance Criteria (`AC-1`, `AC-2`, etc.).
   - If no Jira ticket is referenced, flag PR for standalone code quality analysis.

3. **Construct Specification Matrix**:
   - Map each file in the PR diff to the corresponding Acceptance Criteria.
   - Identify missing requirements or unaddressed criteria before code inspection.

## Output Format
Generates a structured context object:

```json
{
  "pr_number": 104,
  "jira_key": "PAY-204",
  "jira_summary": "Implement Tiered Loyalty Discounts & Defensive Voucher Validation",
  "acceptance_criteria": [
    {"id": "AC-1", "title": "VIP Platinum 20% Discount Rate", "target_files": ["src/discount_service.py"]},
    {"id": "AC-2", "title": "Defensive Voucher Validation & Cap", "target_files": ["src/discount_service.py"]},
    {"id": "AC-3", "title": "Unit Test Coverage", "target_files": ["tests/test_discount_service.py"]},
    {"id": "AC-4", "title": "Structured Audit Logging", "target_files": ["src/discount_service.py"]}
  ],
  "handoff_to": "skill-2-code-architect-reviewer"
}
```
