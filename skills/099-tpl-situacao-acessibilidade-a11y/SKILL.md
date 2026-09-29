---
name: tpl-situacao-acessibilidade-a11y
description: Provides accessibility (a11y) audit and remediation guidance — semantic HTML, keyboard access, focus management, color contrast, and screen-reader testing against WCAG 2.1 AA. Use when the user is auditing an application for accessibility compliance, implementing WCAG 2.1 AA requirements, or fixing accessibility issues.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: Accessibility Audit & Implementation

## WORKFLOW

1. **Declare scope.** List the pages and flows to audit, state the WCAG target (2.1 AA), and note the toolset — this becomes the report's Scope section.
2. **Automated scan.** Run axe/Lighthouse across every page in scope and export the raw results before touching anything.
3. **Manual verification.** Full keyboard walk-through of all critical flows, modal focus behavior, and sampled contrast measurements on real elements.
4. **Screen reader validation.** Complete the critical flows with NVDA (Windows) or VoiceOver (macOS/iOS), recording each step.
5. **Compile the report.** Assemble the OUTPUT FORMAT report — severity summary, per-issue entries, keyboard and contrast tables — and self-check the QUALITY GATES as evidence.

1. **Semantic HTML first, ARIA second.** The most reliable way to convey meaning to assistive technology is semantic HTML: `<button>`, `<nav>`, `<main>`, `<h1>`…`<h6>`, `<label>`, `<table>`. Add ARIA only when HTML semantics are insufficient. Incorrect ARIA is worse than no ARIA.

2. **Every interactive element must be keyboard accessible.** Tab focus must reach all buttons, links, form fields, and interactive controls. Every focusable element must have a visible focus indicator. No keyboard traps (users can always navigate away).

3. **Focus management is mandatory for dynamic UI.** When a modal opens, focus moves into it. When it closes, focus returns to the trigger. When a new section loads (SPA navigation), focus moves to the content. Unmanaged focus makes screen readers disorienting.

4. **No information conveyed by color alone.** Error states need text labels, not just red borders. Status indicators need text or icons, not just colors. Add at least one non-color indicator for every color-coded meaning.

5. **All images need descriptive alt text.** Decorative images: `alt=""`. Informative images: `alt="A bar chart showing sales growth from 2023 to 2024"`. Never `alt="image"` or `alt="photo"`. Icon buttons: `aria-label="Close dialog"`.

6. **WCAG 2.1 AA minimum color contrast:** 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold), 3:1 for UI components (borders of form inputs, focus indicators). Test with real tools, not your eyes.

7. **Screen reader testing is required — automated tools find only ~30% of issues.** Test with: NVDA + Firefox (Windows), VoiceOver + Safari (macOS/iOS), TalkBack (Android). The goal: can a screen reader user complete all critical flows independently?

## ROUTING TABLE

- When you encounter a `<div onClick={...}>` used as an interactive element, replace it with `<button>` or `<a>`; if a `<div>` must be used, add `role="button"`, `tabIndex={0}`, and keyboard handlers (`onKeyDown` for Enter/Space).
- When a form field is missing a label, add `<label htmlFor="fieldId">` or `aria-label`; `placeholder` is NOT a label substitute.
- For an icon-only button without text, add `aria-label="[action]"` or `<span className="sr-only">Close</span>`.
- On a color contrast failure, darken the text or lighten the background, and use a contrast ratio tool to verify a ratio of ≥ 4.5:1.
- For a popup/modal with no focus management, call `focus()` on the first interactive element inside on open, `focus()` on the trigger element on close, and trap focus within the modal.
- When a skip link is missing, add `<a href="#main-content" className="skip-link">Skip to main content</a>` as the first focusable element.
- For auto-playing animated content, add a pause/stop control and respect the `prefers-reduced-motion` media query.
- When error messages are not associated with their field, add `role="alert"` to the error container or use `aria-describedby` to link the field to the error.
- For a data table without headers, add `<th scope="col">` for column headers and `<th scope="row">` for row headers.
- A custom dropdown/select component is complex: either use a native `<select>` (accessible by default) or implement the full combobox ARIA pattern.

## WCAG 2.1 AA Checklist

### Perceivable
- [ ] All images have descriptive alt text (or `alt=""` for decorative)
- [ ] All audio/video has captions and/or transcripts
- [ ] Color is not the only way to convey information
- [ ] Text contrast ratio: ≥ 4.5:1 (normal), ≥ 3:1 (large text ≥18pt)
- [ ] UI component contrast ratio: ≥ 3:1 for borders, focus indicators
- [ ] Text can be resized to 200% without loss of content or functionality
- [ ] Content is not blocked by horizontal scrolling at 320px viewport width

### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Skip navigation link present and functional
- [ ] Visible focus indicator on all focusable elements (not removed with `outline: none` without replacement)
- [ ] No content flashes more than 3 times per second (seizure risk)
- [ ] Page titles are descriptive and unique per page
- [ ] Link text describes destination (no "click here", "read more")
- [ ] Focus order is logical (matches visual reading order)

### Understandable
- [ ] Language of page set: `<html lang="en">`
- [ ] Language changes marked: `<span lang="fr">Bonjour</span>`
- [ ] Form inputs have labels visible at all times
- [ ] Error messages identify: what went wrong + how to fix it
- [ ] No unexpected context changes on focus or input

### Robust
- [ ] Valid HTML (no duplicate IDs, properly nested elements)
- [ ] Custom components have correct ARIA roles, states, and properties
- [ ] Status messages (`role="alert"`, `aria-live`) announced to screen readers without receiving focus

## Focus Indicator (CSS)

```css
/* ✅ Good: visible focus indicator */
:focus-visible {
  outline: 2px solid #0066CC;
  outline-offset: 2px;
  border-radius: 2px;
}

/* ❌ Bad: removes all focus indicators */
* {
  outline: none;
}

/* Screen reader only utility class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Modal Focus Management (React)

```tsx
import { useEffect, useRef } from 'react'

function Modal({ isOpen, onClose, title, children }) {
  const modalRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      triggerRef.current = document.activeElement as HTMLElement
      // Note: opening a second modal from inside this one overwrites triggerRef —
      // for nested dialogs, track the trigger per modal level.
      // Move focus to first interactive element in modal
      const firstFocusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      firstFocusable?.focus()
    } else {
      // Return focus to trigger when modal closes
      triggerRef.current?.focus()
    }
  }, [isOpen])

  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
        return
      }
      if (event.key !== 'Tab') return

      // Trap focus within the modal — aria-modal="true" claims the background is inert
      const focusable = Array.from(
        modalRef.current?.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        ) ?? []
      )
      if (focusable.length === 0) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      const active = document.activeElement

      if (event.shiftKey && (active === first || !modalRef.current?.contains(active))) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && active === last) {
        event.preventDefault()
        first.focus()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
    >
      <h2 id="modal-title">{title}</h2>
      <div id="modal-description">{children}</div>
      <button onClick={onClose} aria-label="Close dialog">×</button>
    </div>
  )
}
```

## DO NOT

- **DO NOT** use `outline: none` or `outline: 0` without providing an alternative visible focus indicator
- **DO NOT** use `placeholder` as a label — it disappears when the user types
- **DO NOT** rely only on automated tools (axe, Lighthouse) — they find ~30% of real issues
- **DO NOT** add `role="button"` to a `<div>` without also adding `tabIndex={0}` and keyboard handlers
- **DO NOT** convey error state through color alone — add an error message or icon
- **DO NOT** use `aria-label` to override visible text — confuses users who can both see and use a screen reader
- **DO NOT** auto-focus a form field on page load in a way that skips past important page context
- **DO NOT** use `tabIndex` > 0 (e.g., `tabIndex={3}`) — it creates confusing non-linear tab order

## OUTPUT FORMAT

For each accessibility audit, produce:

**Accessibility Audit Report:**
```markdown
## Accessibility Audit Report

**Date:** 2024-01-15
**Scope:** Checkout flow (5 pages)
**WCAG Level:** 2.1 AA
**Tools Used:** axe DevTools + manual keyboard testing + VoiceOver

### Summary
- Critical: 3
- Serious: 7
- Moderate: 12
- Minor: 5

### Critical Issues (Must Fix)
#### 1. Missing form labels on checkout address form
- WCAG Criterion: 1.3.1 Info and Relationships (Level A)
- Element: `<input id="street-address">` (no associated label)
- Impact: Screen reader users hear "edit text" with no context
- Fix: Add `<label for="street-address">Street Address</label>`
- Files: CheckoutAddressForm.tsx:34

### Keyboard Navigation
- [x] Tab through checkout: All fields reachable ✅
- [ ] Modal focus: Focus not trapped in order confirmation modal ❌
- [ ] Skip link: Missing ❌

### Color Contrast Failures
- Help text has a foreground of #999999 and background of #FFFFFF with an actual contrast ratio of 2.85:1 against a required 4.5:1.
- Disabled button text has a foreground of #AAAAAA and background of #EEEEEE with an actual contrast ratio of 1.9:1 against a required 3:1.
```

## QUALITY GATES

- [ ] Automated tool (axe or Lighthouse) shows zero Critical and zero Serious violations
- [ ] Full tab navigation through all critical user flows completed without mouse
- [ ] All form fields have visible, persistent labels (not just placeholder)
- [ ] Modal/dialog focus management tested: open → focus in, close → focus returns
- [ ] Color contrast verified for all text elements (≥ 4.5:1 normal, ≥ 3:1 large)
- [ ] All images have appropriate alt text (not "image" or filename)
- [ ] `<html lang="...">` set correctly on all pages
- [ ] Skip link present and navigates to `<main>` correctly
- [ ] Screen reader test (VoiceOver or NVDA) completed on checkout flow
- [ ] `prefers-reduced-motion` respected for all animations

## SCOPE AND LIMITATIONS

This skill covers accessibility auditing and remediation for web applications: semantic HTML, keyboard access, focus management, color contrast, and screen-reader verification against WCAG 2.1 AA.

It does NOT cover:
- **Criterion-level full compliance audits** — that is the job of `wcag-accessibility-audit`; this skill is a situational quick check plus fix execution (see also `auditor-de-acessibilidade`)
- **Backend logic, full-site redesigns, or new feature development** — only the accessibility of existing interfaces
- **Non-web applications** — desktop or native apps need a different checklist; the WCAG framing here assumes the browser
- **Screen-reader verification** — it requires a local environment (NVDA/VoiceOver); if it cannot be run, say so explicitly and mark the report as degraded on that axis

When not to use: the user only wants a quick visual check, or has explicitly excluded keyboard and assistive-technology scenarios.

