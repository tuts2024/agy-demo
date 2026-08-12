# 🎙️ Speaker Script: Autonomous SDLC Review & Remediation Demo

**Total Duration:** ~3 to 5 Minutes  
**Audience:** Technical Leaders, Engineering Directors, DevOps & Product Teams  

---

## ⏱️ Minute 0:00 – 1:00 | Setting the Stage & The Core Problem

**[Screen: Show Browser on `http://localhost:8085` with initial state]**

> **Speaker:**  
> *"Good morning / afternoon everyone! Today, I want to show you how autonomous AI agents transform the Software Development Life Cycle (SDLC) from slow, manual code reviews into real-time, specification-driven quality governance."*
>
> *"In every engineering organization, developers submit pull requests like this one—PR #104. In standard CI pipelines, basic linters check code syntax, and unit tests run. But linters and standard tests have a huge blind spot: **they cannot read Jira stories or understand product acceptance criteria.**"*
>
> *"Here, our team is delivering **JIRA PAY-204**: an upgrade to our E-Commerce Checkout loyalty tiers and voucher safety rules. A developer submitted their PR. Tests are green, but are the business requirements actually met? Let's find out."*

---

## ⏱️ Minute 1:00 – 2:30 | The Autonomous Review in Action

**[Action: Click 'Run Architect Review' or execute `./demo-cli-prompt.sh`]**

> **Speaker:**  
> *"When a PR is opened, our agent pipeline triggers automatically in non-interactive CI mode."*
>
> *"First, **Skill 1: PR & Spec Inspector** pulls the git diff and queries Jira via MCP to extract the exact Acceptance Criteria.*
> *Next, **Skill 2: Senior Architect Reviewer** performs a deep semantic code review, cross-referencing every line of code against the requirements."*
>
> **[Point to the AC Matrix & Finding Cards on the screen]**
>
> *"Look at what the agent caught in seconds:*
> 1. *In **AC-1**, VIP Platinum customers were supposed to get a **20% discount**, but the developer mistakenly hardcoded 10%.*
> 2. *In **AC-2**, vouchers were being applied without checking if they were active or expired, and without enforcing maximum discount caps.*
> 3. *In **AC-3**, the existing unit test had an obsolete assertion that was masking the bug!*
> 4. *In **AC-4**, required financial audit logging was omitted.*
>
> *"Instead of a generic comment, the agent produces a structured, actionable signal: **`REMEDIATION_REQUIRED`**."*

---

## ⏱️ Minute 2:30 – 4:00 | The Self-Healing Remediation Loop

**[Action: Click 'Autonomous Remediate']**

> **Speaker:**  
> *"Now, here is the real superpower: **The Self-Healing Loop**.*
>
> *"Instead of kicking this ticket back to a developer's backlog and waiting three days for revisions, our **Auto-Remediator Agent** immediately consumes the review findings."*
>
> **[Point to the Stepper moving to Verified Merge & Status changing to Approved]**
>
> *"In just a few seconds, the agent:*
> - *Patched `discount_service.py` with the correct 20% rate, active voucher defenses, and audit telemetry.*
> - *Expanded `test_discount_service.py` from 3 tests to 7 comprehensive test cases covering edge cases.*
> - *Executed the full test suite to guarantee 100% green builds.*
>
> **[Switch to the 'Code Diff & Patches' tab]**
>
> *"You can see the exact diff right here: clean, defensive, production-ready code."*

---

## ⏱️ Minute 4:00 – 4:30 | Wrap-up & Takeaways

> **Speaker:**  
> *"To summarize: By pairing autonomous Gemini agents with CI/CD and MCP tools, we achieve:*
> 1. ***Zero Requirement Drift:** Code is mathematically aligned with Jira Acceptance Criteria.*
> 2. ***Instant Feedback:** Architectural reviews happen in seconds, not days.*
> 3. ***Autonomous Self-Healing:** Buggy PRs are fixed and verified automatically before human sign-off.*
>
> *"Thank you, and I'd love to take any questions!"*
