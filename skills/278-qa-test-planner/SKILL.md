---
name: qa-test-planner
description: Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers. Includes Figma MCP integration for design validation. Use when the user asks to create a test plan, generate manual test cases, build a regression or smoke test suite, validate a page against a Figma design, or write a bug report.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# QA Test Planner

A comprehensive skill for QA engineers to create test plans, generate manual test cases, build regression test suites, validate designs against Figma, and document bugs effectively.

> **Activation:** This skill is triggered only when explicitly called by name (e.g., `/qa-test-planner`, `qa-test-planner`, or `use the qa-test-planner skill`).

---


## Quick Start

**Create a test plan:**
```
"Create a test plan for the user authentication feature"
```

**Generate test cases:**
```
"Generate manual test cases for the checkout flow"
```

**Build regression suite:**
```
"Build a regression test suite for the payment module"
```

**Validate against Figma:**
```
"Compare the login page against the Figma design at [URL]"
```

**Create bug report:**
```
"Create a bug report for the form validation issue"
```

---


## Quick Reference

- Test Plan provides strategy, scope, timeline, and risks in 10-15 minutes.
- Test Cases provide step-by-step instructions and expected results, taking 5-10 minutes each.
- Regression Suite includes smoke tests, critical paths, and execution order, taking 15-20 minutes.
- Figma Validation compares design against implementation and produces a discrepancy list in 10-15 minutes.
- Bug Report includes reproducible steps, environment, and evidence in 5 minutes.

---


## How It Works

Your Request → **1. ANALYZE** → **2. GENERATE** → **3. VALIDATE** → QA-Ready Deliverable

### 1. ANALYZE
• Analyze feature/requirement
• Identify needed test types
• Determine scope and priorities

### 2. GENERATE
• Create structured deliverables
• Apply templates and best practices
• Include edge cases and variations

### 3. VALIDATE
• Verify completeness
• Check traceability
• Ensure actionable steps

---


## Commands

### Interactive Scripts

- `./scripts/generate_test_cases.sh` creates test cases interactively via step-by-step prompts.
- `./scripts/create_bug_report.sh` generates bug reports via guided input collection.

### Natural Language

- "Create test plan for {feature}" produces a complete test plan document.
- "Generate {N} test cases for {feature}" produces numbered test cases with steps.
- "Build smoke test suite" produces critical path tests.
- "Compare with Figma at {URL}" produces a visual validation checklist.
- "Document bug: {description}" produces a structured bug report.

---


## Core Deliverables

### 1. Test Plans
- Test scope and objectives
- Test approach and strategy
- Environment requirements
- Entry/exit criteria
- Risk assessment
- Timeline and milestones

### 2. Manual Test Cases
- Step-by-step instructions
- Expected vs. actual results
- Preconditions and setup
- Test data requirements
- Priority and severity

### 3. Regression Suites
- Sanity checks (10-15 min, after hotfix)
- Smoke tests (15-30 min, daily)
- Full regression (2-4 hours, pre-release)
- Targeted regression (30-60 min, after changes)
- Execution order and dependencies

### 4. Figma Validation
- Component-by-component comparison
- Spacing and typography checks
- Color and visual consistency
- Interactive state validation

### 5. Bug Reports
- Clear reproduction steps
- Environment details
- Evidence (screenshots, logs)
- Severity and priority

---


## Patterns to Avoid

- Avoid vague test steps because they cannot be reproduced; instead use specific actions plus expected results.
- Avoid missing preconditions because tests fail unexpectedly; instead document all setup requirements.
- Avoid no test data because the tester is blocked; instead provide sample data or generation.
- Avoid generic bug titles because they are hard to track; instead use the specific format "[Feature] issue when [action]".
- Avoid skipping edge cases because you miss critical bugs; instead include boundary values and nulls.

---

## Scope / Limitations

This skill generates QA documents (test plans, test cases, regression suites, Figma validation, bug reports). It does not:

- **Execute tests or manage test environments.** It produces artifacts for QA engineers to run; it does not run the tests or interpret live results.
- **Automate tests or set up CI.** Automation frameworks, CI integration, and test runner scripts are out of scope.
- **Own the defect lifecycle.** Assigning, closing, verifying, and tracking bugs happens in the team's tooling (Jira, TestRail, etc.).
- **Guarantee Figma validation without access.** Figma validation depends on Figma MCP server availability and file access; when MCP is unavailable, fall back to the manual DevTools comparison path described in [figma_validation.md](references/figma_validation.md).

---

## Verification Checklist

**Test Plan:**
- [ ] Scope clearly defined (in/out)
- [ ] Entry/exit criteria specified
- [ ] Risks identified with mitigations
- [ ] Realistic timeline

**Test Cases:**
- [ ] Every step has expected result
- [ ] Preconditions documented
- [ ] Test data available
- [ ] Priority assigned

**Bug Reports:**
- [ ] Reproducible steps
- [ ] Environment documented
- [ ] Screenshots/evidence attached
- [ ] Severity/priority defined
- [ ] Impact (users affected, frequency, workaround) assessed

---


## References

**Formal guides:**
- [Test Case Templates](references/test_case_templates.md) - Standard formats for all test types
- [Bug Report Templates](references/bug_report_templates.md) - Documentation templates
- [Regression Testing Guide](references/regression_testing.md) - Suite construction and execution
- [Figma Validation Guide](references/figma_validation.md) - Design-implementation validation

**Example artifacts** (sample QA documents you can use as reference output shapes):
- [Example: Login Flow Test Case](references/examples.md) - Sample test cases across test types
- [Example: Login Test Case](references/tc-login-001-valid-user-login.md) - Full test case document
- [Example: Mobile Navigation Test Case](references/tc-ui-045-mobile-navigation-menu.md) - UI test case document
- [Example: Test Cases by Priority](references/test-cases-by-priority.md) - Prioritization breakdown
- [Example: Coverage Matrix](references/coverage-matrix.md) - Requirements-to-tests traceability
- [Example: Summary Report](references/summary.md) - Execution summary and pass rates
- [Example: Risks](references/risks.md) - Risk assessment table
- [Example: Next Steps](references/next-steps.md) - Follow-up actions
- [Example: Blocked Tests](references/blocked-tests.md) - Blocked test documentation
- [Example: Additional Context](references/additional-context.md) - Context fields for bug reports
- [Example: Critical Failures](references/critical-failures.md) - Critical failure documentation

---

<details>
<summary><strong>Deep Dive: Test Case Structure</strong></summary>

### Standard Test Case Format

```markdown

## TC-001: [Test Case Title]

**Priority:** P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
**Type:** Functional | UI/Visual | Integration | Regression | Performance | Security
**Status:** Not Run | Pass | Fail | Blocked | Skipped

### Objective
[What we are testing and why]

### Preconditions
- [Setup requirement 1]
- [Setup requirement 2]
- [Test data needed]

### Test Steps
1. [Action to perform]
   **Expected:** [What should happen]

2. [Action to perform]
   **Expected:** [What should happen]

3. [Action to perform]
   **Expected:** [What should happen]

### Test Data
- Input: [Test data values]
- User: [Test account details]
- Configuration: [Environment settings]

### Post-conditions
- [System state after test]
- [Cleanup needed]

### Notes
- [Edge cases to consider]
- [Related test cases]
- [Known issues]
```

### Test Types

- Functional tests focus on business logic, e.g., login with valid credentials.
- UI/Visual tests focus on appearance and layout, e.g., button matches Figma design.
- Integration tests focus on component interaction, e.g., API returns data to frontend.
- Regression tests focus on existing functionality, e.g., previous features still work.
- Performance tests focus on speed and load capacity, e.g., page loads in under 3 seconds.
- Security tests focus on vulnerabilities, e.g., SQL injection prevented.

</details>

<details>
<summary><strong>Deep Dive: Test Plan Template</strong></summary>

### Test Plan Structure

```markdown
# Test Plan: [Feature/Release Name]


## Executive Summary
- Feature/product being tested
- Test objectives
- Key risks
- Timeline overview


## Test Scope

**In Scope:**
- Features to test
- Test types (functional, UI, performance)
- Platforms and environments
- User flows and scenarios

**Out of Scope:**
- Features not being tested
- Known limitations
- Third-party integrations (if applicable)


## Test Strategy

**Test Types:**
- Manual testing
- Exploratory testing
- Regression testing
- Integration testing
- User acceptance testing

**Test Approach:**
- Black-box testing
- Positive and negative testing
- Boundary value analysis
- Equivalence partitioning


## Test Environment
- Operating systems
- Browsers and versions
- Devices (mobile, tablet, desktop)
- Test data requirements
- Backend/API environments


## Entry Criteria
- [ ] Requirements documented
- [ ] Designs finalized
- [ ] Test environment ready
- [ ] Test data prepared
- [ ] Build deployed


## Exit Criteria
- [ ] All high-priority test cases executed
- [ ] 90%+ test case pass rate
- [ ] All critical bugs fixed
- [ ] No open high-severity bugs
- [ ] Regression suite passed


## Risk Assessment

- Risk [Risk 1] has likelihood H/M/L, impact H/M/L, and mitigation [Mitigation].


## Test Deliverables
- Test plan document
- Test cases
- Test execution reports
- Bug reports
- Test summary report
```

</details>

<details>
<summary><strong>Deep Dive: Bug Report</strong></summary>

### Bug Report Template

```markdown
# BUG-[ID]: [Clear and specific title]

**Severity:** Critical | High | Medium | Low
**Priority:** P0 | P1 | P2 | P3
**Type:** Functional | UI | Performance | Security | Data | Crash
**Status:** Open | In Progress | In Review | Fixed | Verified | Closed


## Environment
- **OS:** [Windows 11, macOS 14, etc.]
- **Browser:** [Chrome 120, Firefox 121, etc.]
- **Device:** [Desktop, iPhone 15, etc.]
- **Build:** [Version/commit]
- **URL:** [Page where the bug occurs]


## Description
[Clear and concise description of the issue]


## Steps to Reproduce
1. [Specific step]
2. [Specific step]
3. [Specific step]


## Expected Behavior
[What should happen]


## Current Behavior
[What actually happens]


## Visual Evidence
- Screenshot: [attached]
- Video: [link if applicable]
- Console errors: [paste errors]


## Impact
- **User Impact:** [How many users affected]
- **Frequency:** [Always, Sometimes, Rarely]
- **Workaround:** [If one exists]
```

</details>

