# 🎤 Presenter's Playbook: Autonomous SDLC Governance & Self-Healing Demo

> **Target Audience:** Engineering Executives (VPs, Directors), Lead Architects, Product Managers, and Platform Engineers.  
> **Duration:** 5–7 Minutes  
> **Core Theme:** *From Passive Linting to Autonomous Semantic Governance and Self-Healing Code.*

---

## 🖥️ Pre-Demo Setup & Screen Arrangement

### 1. Terminal Preparation
In your terminal, navigate to the project root and launch the demo dashboard:
```bash
cd /usr/local/google/home/ntuteja/demo/sdlc
./run_demo.sh
```

### 2. Browser Tabs to Open:
1. **Live Dashboard:** [http://localhost:8085/](http://localhost:8085/) *(Main focus)*
2. **GitHub Pull Request #1:** [https://github.com/tuts2024/agy-demo/pull/1](https://github.com/tuts2024/agy-demo/pull/1)
3. **Jira Issue KAN-8:** [https://ntuteja.atlassian.net](https://ntuteja.atlassian.net)

---

## ⏱️ Step-by-Step Demo Script & Stage Directions

### 🎬 ACT 1: The Context & The SDLC Dilemma (1.5 Minutes)

#### 🎯 Goal:
Establish the gap in current CI/CD tools (they don't understand business requirements or product tickets).

#### 🗣️ Talking Points:
> *"Welcome everyone. Today, every engineering team uses automated CI/CD pipelines to run linters, typecheckers, and unit tests. But here is the fundamental problem: **standard CI/CD is blind to business intent**."*
>
> *"If a developer writes code that passes syntax checks and legacy unit tests, but accidentally gives VIP customers 10% instead of the 20% required by Product, standard CI/CD will green-light it. Catching this requires a senior human architect to manually read the Jira ticket, read the GitHub diff line-by-line, and catch the mismatch."*

#### 🖥️ Visual Focus:
* Point to the **GitHub Pull Request Card** (`#1` by `@ntuteja`) and the **Jira User Story Card** (`KAN-8`).
* Point out that the pipeline is currently in `PIPELINE READY` state with all 4 Acceptance Criteria `PENDING`.

---

### 🎬 ACT 2: Trigger Autonomous Architect Review (2 Minutes)

#### 🎯 Goal:
Demonstrate the AI Architect performing real-time semantic verification against Jira Acceptance Criteria.

#### 👉 Action:
Click the blue **"Run Architect Review"** button in the top navigation bar.

#### 🗣️ Talking Points:
> *"Let's watch what happens when we unleash our autonomous SDLC agent on this Pull Request."*
>
> *"In real time, the agent performs 3 key steps:*
> 1. *It ingests the Pull Request diff from GitHub.*
> 2. *It calls the Atlassian Jira Cloud API to pull ticket **KAN-8** and dynamically extracts the 4 formal Acceptance Criteria.*
> 3. *It acts as a Senior Technical Architect, cross-referencing every line of code against those criteria."*

#### 🖥️ Visual Focus:
* Watch the **Pipeline Stepper** progress across steps 1, 2, 3, and light up step 4 (**AC Audit**).
* Show the status badge turn to glowing red: **`REMEDIATION REQUIRED`**.
* Show the **Jira Acceptance Criteria Matrix** where all 4 rows switch to ❌ **`FAIL`**:
  * **AC-1:** VIP rate is hardcoded to 10% instead of 20%.
  * **AC-2:** Missing defensive voucher validation (`is_active`) and discount caps.
  * **AC-3:** Unit test expects $90 instead of $80, masking the bug.
  * **AC-4:** Missing structured audit trail logging.
* Click the **"Architect Report"** tab to highlight the full executive Markdown audit report.
* *(Optional)* Switch to GitHub PR #1 to show the automated review review posted live.

---

### 🎬 ACT 3: Autonomous Self-Healing Remediation (2 Minutes)

#### 🎯 Goal:
Showcase the self-healing loop—repairing code, expanding tests, and achieving green verification without human delay.

#### 👉 Action:
Click the green **"Autonomous Remediate"** button in the top navigation bar.

#### 🗣️ Talking Points:
> *"Normally, when a review fails, the PR is kicked back to a sprint backlog. It might take 2 to 3 days for a developer to re-contextualize, patch the code, and request another review."*
>
> *"Instead, our Autonomous Remediator agent takes the architect's exact failure directives, writes a targeted code patch for `discount_service.py`, expands the unit test suite to 7 comprehensive test cases, and runs `unittest` to verify 100% green test passes."*

#### 🖥️ Visual Focus:
* Watch the **Pipeline Stepper** complete steps 5 (**Auto-Remediate**) and 6 (**Verified Merge**).
* Status badge turns emerald: **`VERIFIED & APPROVED`**.
* All 4 rows in the AC Matrix dynamically switch to ✅ **`PASS`**.
* **Switch to the "Code Diff & Patches" Tab:**
  * Show the side-by-side code diff:
    * Left: Initial developer submission (with bugs).
    * Right: AI-remediated code (with VIP 20%, voucher guards, and audit logging).
* **Switch to Jira / GitHub:** Show the sync comment posted to **`KAN-8`** and the PR approval comment.

---

### 🎬 ACT 4: Executive Wrap-Up & Value Summary (1 Minute)

#### 🗣️ Closing Statement:
> *"In under 30 seconds, this agent eliminated a multi-day review cycle, prevented a revenue-impacting business logic regression from hitting production, and guaranteed 100% compliance with product and security specifications."*
>
> *"This is the future of enterprise software engineering: autonomous, specification-driven, self-healing governance."*

---

## ❓ Frequently Asked Questions (Presenter Cheat Sheet)

### Q1: Does this require human approval before merging?
**Answer:** Yes, the agent can be configured in two modes:
1. **Autonomous Auto-Merge:** For low-risk, internal, or staging services with 100% test verification.
2. **Architect Advisory Mode (Default):** Prepares the patch and test suite, leaving the final 1-click merge button for the lead engineer.

### Q2: How does it extract Acceptance Criteria from Jira?
**Answer:** The agent connects to Atlassian Jira Cloud v3 REST API, parses Atlassian Document Format (ADF) rich text nodes, and extracts numbered criteria using structured pattern matching (`AC-1`, `AC-2`, etc.).

### Q3: What if the code has compilation errors after remediation?
**Answer:** The self-healing loop is iterative. It executes the local test runner (`unittest`/`pytest`) and checks the exit code. If tests fail, it feeds the traceback back to the AI model to refine the patch until all tests pass.

### Q4: Can this integrate with existing GitLab, Bitbucket, or Azure DevOps pipelines?
**Answer:** Yes. The core engine is packaged as a standalone Python CLI (`orchestrate_review.py`) that runs in any standard containerized CI/CD environment (GitHub Actions, GitLab CI, Jenkins, Tekton, Cloud Build).

---

## 🔄 Resetting for Another Demo

To instantly reset the demo to the pre-review state for the next audience:
* Click **"Reset Demo"** in the top navigation of the web dashboard.
* Or run in your terminal:
  ```bash
  python3 orchestrate_review.py --reset
  ```
