## TC-UI-045: Mobile Navigation Menu

**Priority:** P1 (High)
**Type:** UI/Visual
**Devices:** Mobile (iPhone, Android)

### Objective
Verify that the navigation menu works correctly on mobile devices

### Pre-conditions
- Access on mobile device or responsive mode
- Viewport width: 375px (iPhone SE) to 428px (iPhone Pro Max)

### Test Steps
1. Open homepage on mobile device
   **Expected:** Hamburger menu icon visible (top right corner)

2. Tap hamburger icon
   **Expected:**
   - Menu slides in from the right
   - Overlay appears over content
   - Close button (X) visible

3. Tap on menu item
   **Expected:** Navigates to section, menu closes

4. Compare against Figma mobile design [link]
   **Expected:**
   - Menu width: 280px
   - Slide animation: 300ms ease-out
   - Overlay opacity: 0.5, color #000000
   - Font size: 16px, line-height 24px

### Breakpoints to Test
- 375px (iPhone SE)
- 390px (iPhone 14)
- 428px (iPhone 14 Pro Max)
- 360px (Galaxy S21)
```

</details>

---

**"Testing shows the presence, not the absence of bugs." - Edsger Dijkstra**

**"Quality is not an act, it is a habit." - Aristotle**