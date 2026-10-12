## Additional Context

- Related to: [Feature/ticket]
- Regression: [Yes/No]
- Figma Design: [Link if UI bug]

### Severity Definitions

| Level | Criterion | Examples |
|-------|----------|----------|
| **Critical (P0)** | System crash, data loss, security | Payment fails, login broken |
| **High (P1)** | Core functionality broken, no workaround | Search doesn't work |
| **Medium (P2)** | Partial functionality, workaround exists | Filter missing an option |
| **Low (P3)** | Cosmetic, rare edge cases | Typo, minor alignment |

<details>
<summary><strong>Deep Dive: Figma MCP Integration</strong></summary>

### Design Validation Workflow

**Prerequisites:**
- Figma MCP server configured
- Access to Figma design files
- Figma URLs for components/pages

**Process:**

1. **Get Design Specs from Figma**
```
"Get the button specifications from Figma file [URL]"

Response includes:
- Dimensions (width, height)
- Colors (background, text, border)
- Typography (font, size, weight)
- Spacing (padding, margin)
- Border radius
- States (default, hover, active, disabled)
```

2. **Compare Implementation**
```
TC: Primary Button Visual Validation
1. Inspect primary button in developer tools
2. Compare against Figma specs:
   - Dimensions: 120x40px
   - Border-radius: 8px
   - Background color: #0066FF
   - Font: 16px Medium #FFFFFF
3. Document discrepancies
```

3. **Create Bug if Mismatched**
```
BUG: Primary button color doesn't match design
Severity: Medium
Expected (Figma): #0066FF
Actual (Implementation): #0052CC
Screenshot: [attached]
Figma Link: [specific component]
```

### What to Validate

| Element | What to Check | Tool |
|----------|-----------------|------------|
| Colors | Exact hex values | Browser color picker |
| Spacing | Padding/margin px | DevTools computed styles |
| Typography | Font, size, weight | DevTools font panel |
| Layout | Width, height, position | DevTools box model |
| States | Hover, active, focus | Manual interaction |
| Responsive | Breakpoint behavior | DevTools device mode |

### Query Examples
```
"Get button specs from Figma design [URL]"
"Compare navigation menu implementation against Figma design"
"Extract spacing values from the Figma dashboard layout"
"List all color tokens used in Figma design system"
```

</details>

<details>
<summary><strong>Deep Dive: Regression Testing</strong></summary>

### Suite Structure

| Suite Type | Duration | Frequency | Coverage |
|---------------|---------|-----------|-----------|
| Smoke | 15-30 min | Daily | Critical paths only |
| Targeted | 30-60 min | Per change | Affected areas |
| Full | 2-4 hours | Weekly/Release | Comprehensive |
| Sanity | 10-15 min | After hotfix | Quick validation |

### Building a Regression Suite

**Step 1: Identify Critical Paths**
- What can users NOT live without?
- What generates revenue?
- What handles sensitive data?
- What is used most frequently?

**Step 2: Prioritize Test Cases**

| Priority | Description | Must Run |
|------------|-----------|---------------|
| P0 | Business-critical, security | Always |
| P1 | Core features, common flows | Weekly+ |
| P2 | Minor features, edge cases | Releases |

**Step 3: Execution Order**
1. Smoke first - if it fails, stop and fix build
2. P0 tests next - must pass before proceeding
3. P1 then P2 - track all failures
4. Exploratory - find unexpected issues

### Pass/Fail Criteria

**PASS:**
- All P0 tests pass
- 90%+ of P1 tests pass
- No open critical bugs

**FAIL (Blocks Release):**
- Any P0 test fails
- Critical bug discovered
- Security vulnerability
- Data loss scenario

**CONDITIONAL:**
- P1 failures with workarounds
- Known issues documented
- Fix plan in place

</details>

<details>
<summary><strong>Deep Dive: Test Execution Tracking</strong></summary>

### Test Execution Report Template

```markdown
# Test Execution: [Release Version]

**Date:** 2024-01-15
**Build:** v2.5.0-rc1
**Tester:** [Name]
**Environment:** Staging
**OS:** [Operating system]
**Browser:** [Browser and version]

## Summary

| Total | Executed | Passed | Failed | Blocked |
|-------|----------|--------|--------|---------|
| 0 | 0 | 0 | 0 | 0 |

## Failures

- [BUG-ID]: [Issue and impact]

## Recommendations

- [Recommended next actions]

## Notes

- [Blockers, risks, follow-ups]
```

</details>