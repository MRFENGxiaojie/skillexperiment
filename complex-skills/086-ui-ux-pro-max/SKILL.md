---
name: ui-ux-pro-max
description: UI/UX design intelligence covering 50 design styles, 21 color palettes, 50 font pairings, 20 chart types, and 9 technology stacks (React, Next.js, Vue, Svelte, SwiftUI, Flutter, and more). Use when the user needs UI/UX design guidance, design system recommendations, component design patterns, or visual design decision support.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# UI UX Pro Max

Comprehensive design guide for web and mobile applications. Contains 50+ styles, 97 color palettes, 57 font combinations, 99 UX guidelines, and 25 chart types across 9 technology stacks. Searchable database with priority-based recommendations.

## When to Apply

Consult these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

- Priority 1: Accessibility (`ux` domain, impact CRITICAL).
- Priority 2: Touch & Interaction (`ux` domain, impact CRITICAL).
- Priority 3: Performance (`ux` domain, impact HIGH).
- Priority 4: Layout & Responsive (`ux` domain, impact HIGH).
- Priority 5: Typography & Color (`typography` and `color` domains, impact MEDIUM).
- Priority 6: Animation (`ux` domain, impact MEDIUM).
- Priority 7: Style Selection (`style` and `product` domains, impact MEDIUM).
- Priority 8: Charts & Data (`chart` domain, impact LOW).

## Quick Reference

### 1. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio for normal text
- `focus-states` - Visible focus rings on interactive elements
- `alt-text` - Descriptive alt text for relevant images
- `aria-labels` - aria-label for icon-only buttons
- `keyboard-nav` - Tab order matches visual order
- `form-labels` - Use label with for attribute

### 2. Touch & Interaction (CRITICAL)

- `touch-target-size` - Minimum 44x44px touch target
- `hover-vs-tap` - Use click/tap for primary interactions
- `loading-buttons` - Disable button during async operations
- `error-feedback` - Clear error messages near the problem
- `cursor-pointer` - Add cursor-pointer to clickable elements

### 3. Performance (HIGH)

- `image-optimization` - Use WebP, srcset, lazy loading
- `reduced-motion` - Check prefers-reduced-motion
- `content-jumping` - Reserve space for async content

### 4. Layout & Responsive (HIGH)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Minimum 16px for body text on mobile
- `horizontal-scroll` - Ensure content fits viewport width
- `z-index-management` - Define z-index scale (10, 20, 30, 50)

### 5. Typography & Color (MEDIUM)

- `line-height` - Use 1.5-1.75 for body text
- `line-length` - Limit to 65-75 characters per line
- `font-pairing` - Pair heading and body fonts by personality

### 6. Animation (MEDIUM)

- `duration-timing` - Use 150-300ms for micro-interactions
- `transform-performance` - Use transform/opacity, not width/height
- `loading-states` - Skeleton screens or spinners

### 7. Style Selection (MEDIUM)

- `style-match` - Match style to product type
- `consistency` - Use the same style across all pages
- `no-emoji-icons` - Use SVG icons, not emojis

### 8. Charts & Data (LOW)

- `chart-type` - Match chart type to data type
- `color-guidance` - Use accessible color palettes
- `data-table` - Provide table alternative for accessibility

## How to Use

Search specific domains using the CLI tool below.

---

## Prerequisites

Verify Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it according to the user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This Skill

When the user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from the user's request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default `html-tailwind`

### Step 2: Generate the Design System (MANDATORY)

**Always start with `--design-system`** to get comprehensive recommendations with reasoning:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This command:
1. Searches 5 domains in parallel (product, style, color, landing, typography)
2. Applies reasoning rules from `ui-reasoning.csv` to select the best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Includes anti-patterns to avoid

**Example:**
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 3: Supplement with Detailed Searches (as needed)

After obtaining the design system, use domain searches for additional details:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

- For more style options, use domain `style`, e.g. `--domain style "glassmorphism dark"`.
- For chart recommendations, use domain `chart`, e.g. `--domain chart "real-time dashboard"`.
- For UX best practices, use domain `ux`, e.g. `--domain ux "animation accessibility"`.
- For alternative fonts, use domain `typography`, e.g. `--domain typography "elegant luxury"`.
- For landing structure, use domain `landing`, e.g. `--domain landing "hero social-proof"`.

### Step 4: Stack Guidelines (Default: html-tailwind)

Get implementation-specific best practices. If the user does not specify a stack, **default to `html-tailwind`**.

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## Search Reference

### Available Domains

- `product`: use for product type recommendations (e.g., SaaS, e-commerce, portfolio, healthcare, beauty, service).
- `style`: use for UI styles, colors, and effects (e.g., glassmorphism, minimalism, dark mode, brutalism).
- `typography`: use for font combinations and Google Fonts (e.g., elegant, playful, professional, modern).
- `color`: use for color palettes by product type (e.g., saas, ecommerce, healthcare, beauty, fintech, service).
- `landing`: use for page structure and CTA strategies (e.g., hero, hero-centric, testimonial, pricing, social-proof).
- `chart`: use for chart types and library recommendations (e.g., trend, comparison, timeline, funnel, pie).
- `ux`: use for best practices and anti-patterns (e.g., animation, accessibility, z-index, loading).
- `react`: use for React/Next.js performance (e.g., waterfall, bundle, suspense, memo, rerender, cache).
- `web`: use for web interface guidelines (e.g., aria, focus, keyboard, semantic, virtualize).
- `prompt`: use for AI prompts and CSS keywords (e.g., `(style name)`).

### Available Stacks

- `html-tailwind` stack: Tailwind utilities, responsive, a11y (DEFAULT).
- `react` stack: State, hooks, performance, patterns.
- `nextjs` stack: SSR, routing, images, API routes.
- `vue` stack: Composition API, Pinia, Vue Router.
- `svelte` stack: Runes, stores, SvelteKit.
- `swiftui` stack: Views, State, Navigation, Animation.
- `react-native` stack: Components, Navigation, Lists.
- `flutter` stack: Widgets, State, Layout, Theming.
- `shadcn` stack: shadcn/ui components, theming, forms, patterns.

---

## Example Workflow

**User request:** "Create a landing page for a professional skincare service"

### Step 1: Analyze Requirements
- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate the Design System (MANDATORY)

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** Complete design system with pattern, style, colors, typography, effects and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get UX guidelines for animation and accessibility
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Step 4: Stack Guidelines

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Then:** Synthesize the design system + detailed searches and implement the design.

---

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use the stack flag** - Get implementation-specific best practices
6. **Iterate** - If the first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make the UI look unprofessional:

### Icons & Visual Elements

- No emoji icons: use SVG icons (Heroicons, Lucide, Simple Icons); do not use emojis like 🎨 🚀 ⚙️ as UI icons.
- Stable hover states: use color/opacity transitions on hover; do not use scale transforms that shift layout.
- Correct brand logos: look up the official SVG from Simple Icons; do not guess or use incorrect logo paths.
- Consistent icon size: use a fixed viewBox (24x24) with w-6 h-6; do not mix icon sizes randomly.

### Interaction & Cursor

- Cursor pointer: add `cursor-pointer` to all clickable/hover cards; do not leave the default cursor on interactive elements.
- Hover feedback: provide visual feedback (color, shadow, border); do not leave no indication that an element is interactive.
- Smooth transitions: use `transition-colors duration-200`; do not use instant or too-slow state changes (over 500ms).

### Light/Dark Mode Contrast

- Glass card light mode: use `bg-white/80` or higher opacity; do not use `bg-white/10` (too transparent).
- Light text contrast: use `#0F172A` (slate-900) for text; do not use `#94A3B8` (slate-400) for body text.
- Light muted text: use `#475569` (slate-600) minimum; do not use gray-400 or lighter.
- Border visibility: use `border-gray-200` in light mode; do not use `border-white/10` (invisible).

### Layout & Spacing

- Floating navbar: add `top-4 left-4 right-4` spacing; do not stick the navbar to `top-0 left-0 right-0`.
- Content padding: account for fixed navbar height; do not leave content hidden behind fixed elements.
- Consistent max-width: use the same `max-w-6xl` or `max-w-7xl`; do not mix different container widths.

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Correct brand logos (verified from Simple Icons)
- [ ] Hover states do not cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout
- [ ] Floating elements have proper edge spacing
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected

## Scope and Limitations

- Covers UI implementation review (code-level patterns, component structure, design tokens) — not visual design review or brand strategy
- Tailwind CSS is the assumed framework; the patterns and rules may need adaptation for other CSS approaches
- Does not cover full WCAG compliance auditing — the accessibility checklist here is a quick sanity check, not a certification-grade audit
- Design decisions that involve subjective taste ("does this look good?") are outside scope — this skill checks consistency and correctness, not aesthetics

