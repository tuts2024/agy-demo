---
name: code-architect-reviewer
trigger: automatic
description: Performs rigorous Senior Technical Architect review of PR diffs against Jira Acceptance Criteria, detecting logic bugs, missing tests, and security risks.
---

# Skill: Code Architect Reviewer

## Purpose
Performs an automated, in-depth architectural and specification compliance code review. Compares git changes line-by-line against Jira Acceptance Criteria, flags code defects, verifies test coverage, and outputs executive Markdown summaries and CI/CD remediation signals.

## Trigger
- Handoff from `skill-1-pr-spec-inspector`

## Instructions

1. **Acceptance Criteria Verification**:
   - Compare modified code against each specific Jira Acceptance Criterion (`AC-1` to `AC-4`).
   - Flag any divergence where code does not fulfill the stated business requirement.

2. **Code Robustness & Security Analysis**:
   - Check for defensive programming (handling of `None`, empty collections, null pointer risks).
   - Check for boundary condition violations (e.g. discount exceeding max caps).
   - Check for security standards (hardcoded credentials, injection vulnerabilities).
   - Check for auditability (structured logging, tracing identifiers).

3. **Test Suite Integrity Check**:
   - Verify that unit tests were added or updated to cover all new branches and logic.
   - Flag obsolete test assertions that mask regressions.

4. **Generate Structured Markdown Report**:
   - Format clear findings using emoji indicators (✅ PASS, ❌ VIOLATION, ⚠️ WARNING).
   - Provide concrete code suggestions with diff examples.
   - Include Jira status commentary.

5. **Emit CI/CD Remediation Directive**:
   - If ANY Acceptance Criteria are unmet or tests fail, conclude the review with the exact string:
     `REMEDIATION_REQUIRED: [Detailed bulleted list of fixes needed]`
   - If all criteria pass, conclude with:
     `APPROVAL_GRANTED: All acceptance criteria satisfied.`

## Output Files
- Save full markdown report to `reports/review-report-PR[number].md`
- Output to `$GITHUB_STEP_SUMMARY` in CI/CD runners
- Output telemetry JSON to `reports/review-telemetry-PR[number].json`
