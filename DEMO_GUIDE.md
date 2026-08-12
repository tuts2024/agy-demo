# 🚀 Presenter's Guide: Autonomous SDLC Review & Self-Healing Remediation Demo

## 🌟 Executive Overview & Value Proposition
In standard CI/CD pipelines, automated checks are limited to syntax linting, static type checking, and unit test execution. They **cannot understand business intent** or verify if code changes satisfy **product acceptance criteria**.

**This demo showcases Next-Generation Agentic SDLC Governance:**
1. **Intelligent Intake & Context Fusion:** An autonomous agent ingests Pull Request diffs and pulls linked Jira stories & Acceptance Criteria via MCP (Model Context Protocol).
2. **Deep Semantic & Specification Review:** The agent acts as a Senior Technical Architect, auditing the code line-by-line against business rules, edge cases, null safety, and audit standards.
3. **Autonomous Self-Healing Loop:** If regressions or unfulfilled criteria are detected, a specialized auto-remediator agent generates targeted code patches, updates unit tests, and verifies 100% test passing before merge approval.

---

## 📂 Demo Artifacts & Architecture

| Component | Path | Description |
| :--- | :--- | :--- |
| **Interactive Dashboard** | [sdlc-review-dashboard.html](file:///usr/local/google/home/ntuteja/demo/sdlc/sdlc-review-dashboard.html) | High-fidelity live visual UI with pipeline stepper, diff viewer & AC matrix. |
| **Orchestration Engine** | [orchestrate_review.py](file:///usr/local/google/home/ntuteja/demo/sdlc/orchestrate_review.py) | Python engine supporting CLI stages and REST API backend. |
| **Launcher Script** | [run_demo.sh](file:///usr/local/google/home/ntuteja/demo/sdlc/run_demo.sh) | One-command launcher (`./run_demo.sh [port]`). |
| **CI/CD Script** | [demo-cli-prompt.sh](file:///usr/local/google/home/ntuteja/demo/sdlc/demo-cli-prompt.sh) | Terminal runner emulating GitHub Actions runner execution. |
| **GitHub Actions** | [.github/workflows/jetski-pr-review.yml](file:///usr/local/google/home/ntuteja/demo/sdlc/.github/workflows/jetski-pr-review.yml) | Production CI/CD workflow definition. |
| **Jira Issue Context** | [jira/PAY-204-ticket.json](file:///usr/local/google/home/ntuteja/demo/sdlc/jira/PAY-204-ticket.json) | Mock Jira ticket specification with 4 Acceptance Criteria. |
| **Skill 1: PR Inspector** | [skills/skill-1-pr-spec-inspector.md](file:///usr/local/google/home/ntuteja/demo/sdlc/skills/skill-1-pr-spec-inspector.md) | Ingestion & Jira context extraction skill. |
| **Skill 2: Architect Reviewer** | [skills/skill-2-code-architect-reviewer.md](file:///usr/local/google/home/ntuteja/demo/sdlc/skills/skill-2-code-architect-reviewer.md) | Senior Architect code analysis & AC verification skill. |
| **Skill 3: Auto-Remediator** | [skills/skill-3-auto-remediator.md](file:///usr/local/google/home/ntuteja/demo/sdlc/skills/skill-3-auto-remediator.md) | Self-healing code patcher and test expander skill. |

---

## 🎬 Live Presentation Flow (Step-by-Step)

### Preparation Before the Meeting:
1. Open a terminal in `/usr/local/google/home/ntuteja/demo/sdlc`.
2. Run:
   ```bash
   ./run_demo.sh
   ```
3. Open `http://localhost:8085/` in your browser.
4. Position your screen with the **Browser Dashboard on the left** and the **Terminal on the right**.

---

### Step 1: The Context & The Problem (1 minute)
- **Show the Dashboard:** Point to **Pull Request #104** (`feat: Loyalty Discounts`) and linked **Jira Ticket PAY-204**.
- **Talking Point:** 
  > *"Here we have a typical developer pull request modifying our checkout discount engine. Standard unit tests pass, but did the developer actually satisfy the product requirements in Jira PAY-204? Usually, a human senior engineer has to manually read both and cross-reference. Let's see what happens when we let our autonomous agent review this."*

---

### Step 2: Trigger Autonomous Architect Review (1 minute)
- **Action:** Click the **"Run Architect Review"** button in the dashboard top navigation (or run `./demo-cli-prompt.sh` in the terminal).
- **Watch the UI Live:**
  - Pipeline Stepper updates from **1. PR Intake** → **2. Jira Spec MCP** → **3. Architect Review** → **4. AC Audit (Warning / Remediation Required)**.
  - The **Jira Acceptance Criteria Matrix** dynamically flags all 4 criteria as ❌ **FAIL**!
  - 4 finding cards appear explaining the exact code flaws:
    1. `AC-1`: VIP Platinum rate set to 10% instead of 20%.
    2. `AC-2`: Missing voucher defensive checks (`is_active` & discount cap).
    3. `AC-3`: Test suite contains obsolete assertions ($90 vs $80).
    4. `AC-4`: Missing financial audit trail logging.
- **Talking Point:**
  > *"In seconds, the agent cross-referenced the git diff against Jira PAY-204. It caught that VIP customers were about to be under-discounted, vouchers were unvalidated, and tests were masking regressions. The review outputs a structured directive: `REMEDIATION_REQUIRED`."*

---

### Step 3: Trigger Autonomous Self-Healing Remediation (1 minute)
- **Action:** Click the green **"Autonomous Remediate"** button.
- **Watch the UI Live:**
  - Stepper moves to **5. Auto-Remediate** and **6. Verified Merge**.
  - Status pill glows emerald: **`VERIFIED & APPROVED`**.
  - All 4 Acceptance Criteria switch to **`PASS`**.
  - Test suite count jumps from **3 to 7 tests (100% Green)**.
- **Switch to the "Code Diff & Patches" Tab:**
  - Show the side-by-side comparison:
    - `VIP_PLATINUM` rate updated to `0.20`.
    - Defensive voucher validation & cap enforcement implemented.
    - Structured audit logging added.
- **Talking Point:**
  > *"Rather than kicking this back to a backlog queue and waiting days for another developer cycle, the Autonomous Remediator agent took the directives, patched the source code, expanded unit test coverage to 7 comprehensive tests, and proved that 100% of tests pass cleanly. The PR is verified and ready for instant merge."*

---

## 🛠️ CLI Quick Commands Cheat Sheet

| Command | Action |
| :--- | :--- |
| `./run_demo.sh` | Starts live dashboard on port 8085 and resets demo state |
| `./demo-cli-prompt.sh` | Runs end-to-end review and remediation directly in the terminal |
| `python3 orchestrate_review.py --stage review` | Runs only the Architect Review stage |
| `python3 orchestrate_review.py --stage remediate` | Runs only the Autonomous Remediation stage |
| `python3 orchestrate_review.py --reset` | Resets code and state back to initial buggy PR |
| `python3 -m unittest discover tests -v` | Executes test suite |
