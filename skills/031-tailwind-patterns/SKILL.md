---
name: tailwind-patterns
description: Tailwind CSS v4 principles. CSS-based configuration, container queries, modern patterns, design token architecture. Use when the user asks to style with Tailwind CSS, set up v4 CSS-first configuration, use container queries, dark mode, or design tokens, or build responsive layouts.
allowed-tools: Read, Write, Edit, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Tailwind CSS Patterns (v4 - 2025)

> Modern utility-first CSS with native CSS configuration.

---

## 1. Tailwind v4 Architecture

### What Changed from v3

- `tailwind.config.js` (v3) replaced by CSS-based `@theme` directive (v4)
- PostCSS Plugin (v3) replaced by Oxide engine, which is 10x faster (v4)
- JIT Mode (v3) replaced by native, always-on mode (v4)
- Plugin system (v3) replaced by native CSS features (v4)
- `@apply` directive still works in v4 but is discouraged

### v4 Core Concepts

- **CSS-first**: configuration lives in CSS, not JavaScript
- **Oxide Engine**: Rust-based compiler, much faster
- **Native Nesting**: CSS nesting without PostCSS
- **CSS Variables**: all tokens exposed as `--*` variables

---

## 2. CSS-Based Configuration

### Theme Definition

```
@theme {
  /* Colors - use semantic names */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);
  
  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### When to Extend vs Override

- **Extend**: use when adding new values alongside defaults
- **Override**: use when replacing the default scale completely
- **Semantic tokens**: use for project-specific naming (primary, surface)

---

## 3. Container Queries (Native v4)

### Breakpoint vs Container

- **Breakpoint** (`md:`): responds to viewport width
- **Container** (`@container`): responds to parent element width

### Container Query Usage

- Define container: put `@container` on the parent
- Container breakpoint: use `@sm:`, `@md:`, `@lg:` on children
- Named containers: use `@container/card` for specificity

### When to Use

- Page-level layouts: use viewport breakpoints
- Component-level responsive design: use container queries
- Reusable components: use container queries (context-independent)

---

## 4. Responsive Design

### Breakpoint System

- (none) prefix: minimum width 0px, mobile-first base
- `sm:` prefix: minimum width 640px, targets large phone / small tablet
- `md:` prefix: minimum width 768px, targets tablet
- `lg:` prefix: minimum width 1024px, targets laptop
- `xl:` prefix: minimum width 1280px, targets desktop
- `2xl:` prefix: minimum width 1536px, targets large desktop

### Mobile-First Principle

1. Write mobile styles first (no prefix)
2. Add overrides for larger screens with prefixes
3. Example: `w-full md:w-1/2 lg:w-1/3`

---

## 5. Dark Mode

### Configuration Strategies

- `class` strategy: `.dark` class toggles; use for manual theme switcher
- `media` strategy: follows system preference; use when there is no user control
- `selector` strategy: custom selector (v4); use for complex themes

### Dark Mode Pattern

- Background: `bg-white` in light, `dark:bg-zinc-900` in dark
- Text: `text-zinc-900` in light, `dark:text-zinc-100` in dark
- Borders: `border-zinc-200` in light, `dark:border-zinc-700` in dark

---

## 6. Modern Layout Patterns

### Flexbox Patterns

- Center (both axes): `flex items-center justify-center`
- Vertical stack: `flex flex-col gap-4`
- Horizontal row: `flex gap-4`
- Space between: `flex justify-between items-center`
- Wrapping grid: `flex flex-wrap gap-4`

### Grid Patterns

- Responsive auto-fit: `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]`
- Asymmetric (Bento): `grid grid-cols-3 grid-rows-2` with spans
- Sidebar layout: `grid grid-cols-[auto_1fr]`

> **Note:** Prefer asymmetric/Bento layouts over symmetric 3-column grids.

---

## 7. Modern Color System

### OKLCH vs RGB/HSL

- **OKLCH**: perceptually uniform, better for design
- **HSL**: intuitive hue/saturation
- **RGB**: legacy compatibility

### Color Token Architecture

- **Primitive** layer: e.g. `--blue-500`, holds raw color values
- **Semantic** layer: e.g. `--color-primary`, purpose-based naming
- **Component** layer: e.g. `--button-bg`, component-specific

---

## 8. Typography System

### Font Stack Pattern

- Sans: `'Inter', 'SF Pro', system-ui, sans-serif`
- Mono: `'JetBrains Mono', 'Fira Code', monospace`
- Display: `'Outfit', 'Poppins', sans-serif`

### Type Scale

- `text-xs`: 0.75rem, for labels, captions
- `text-sm`: 0.875rem, for secondary text
- `text-base`: 1rem, for body text
- `text-lg`: 1.125rem, for highlight text
- `text-xl`+: 1.25rem+, for headings

---

## 9. Animations and Transitions

### Native Animations

- `animate-spin`: continuous rotation
- `animate-ping`: attention pulse
- `animate-pulse`: subtle opacity pulse
- `animate-bounce`: bounce effect

### Transition Patterns

- All properties: `transition-all duration-200`
- Specific: `transition-colors duration-150`
- With easing: `ease-out` or `ease-in-out`
- Hover effect: `hover:scale-105 transition-transform`

---

## 10. Component Extraction

### When to Extract

- Same class combination 3+ times: extract component
- Complex state variants: extract component
- Design system element: extract + document

### Extraction Methods

- **React/Vue Component**: use when dynamic, JS needed
- **`@apply` in CSS**: use when static, JS not needed
- **Design tokens**: use for reusable values

---

## 11. Anti-patterns

- Don't use arbitrary values everywhere; use design system scale
- Don't use `!important`; fix specificity properly
- Don't use inline `style=`; use utilities
- Don't duplicate long class lists; extract component
- Don't mix v3 config with v4; migrate fully to CSS-first
- Don't use `@apply` heavily; prefer components

---

## 12. Performance Principles

- **Purge unused**: automatic in v4
- **Avoid dynamic**: no template string classes
- **Use Oxide**: default in v4, 10x faster
- **Cache builds**: CI/CD caching

---

## Scope and Limitations

This skill covers styling with Tailwind CSS v4: CSS-first configuration, design tokens, responsive layouts, container queries, dark mode, and component extraction.

It does NOT cover:
- **Tailwind v3 projects** — this skill documents v4. A v3 project must migrate to CSS-first configuration before these patterns apply.
- **Non-Tailwind CSS frameworks** — the class names, `@theme` syntax, and token architecture are Tailwind-specific.
- **JavaScript interaction logic** — state, event handlers, and component behavior live in the framework layer (React, Vue, etc.), not in utility classes.
- **Build tool installation** — setting up Vite, PostCSS, or the Tailwind CLI is outside this skill; it assumes a working Tailwind v4 build.

## Output Format

Deliver styling changes as concrete, copy-pasteable artifacts:

1. **Class strings** — the final class attribute for each element, showing the exact utility classes to apply.
2. **CSS configuration** — the `@theme` tokens, `@custom-variant` rules, or custom utilities required to support those classes, as a complete CSS block.
3. **Extracted components** — when a class combination repeats 3+ times, deliver the extracted component (JSX, Vue template, or `@apply` CSS), not the repeated list.
4. **Pattern rationale** — one line stating which pattern from this skill was applied (container query vs breakpoint, token vs arbitrary value) so the choice is reviewable.

Example:

```jsx
<button class="rounded-lg bg-primary px-4 py-2 text-white transition-colors hover:opacity-90">Sign up</button>
```

```css
@theme {
  --color-primary: oklch(0.7 0.15 250);
}
```

The class string is complete; the `@theme` block defines the one non-default token it references.

---

> **Remember:** Tailwind v4 is CSS-first. Embrace CSS variables, container queries, and native features. The config file is now optional.

