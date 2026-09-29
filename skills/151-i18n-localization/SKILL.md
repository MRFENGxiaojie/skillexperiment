---
name: i18n-localization
description: Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. Use when the user asks to internationalize or localize an app, detect hardcoded strings, manage translation and locale files, or add RTL language support.
allowed-tools: Read, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# i18n & Localization

> Internationalization (i18n) and Localization (L10n) best practices.

---

## 1. Core Concepts

- **i18n** means Internationalization — making the app translatable.
- **L10n** means Localization — the actual translations.
- **Locale** is a combination of Language and Region (for example, en-US, tr-TR).
- **RTL** refers to Right-to-left languages (for example, Arabic, Hebrew).

---

## 2. When to Use i18n

- Public web apps require i18n.
- SaaS products require i18n.
- Internal tools may require i18n.
- Single-region apps should consider i18n for the future.
- Personal projects treat i18n as optional.

---

## 3. Implementation Patterns

### React (react-i18next)

```tsx
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

### Next.js (next-intl)

```tsx
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('Home');
  return <h1>{t('title')}</h1>;
}
```

### Python (gettext)

```python
from gettext import gettext as _

print(_("Welcome to our app"))
```

---

## 4. File Structure

locales/
- en/
  - common.json
  - auth.json
  - errors.json
- tr/
  - common.json
  - auth.json
  - errors.json
- ar/          # RTL
  - ...

---

## 5. Best Practices

### DO ✅

- Use translation keys, not raw text
- Organize translations by feature
- Support pluralization
- Handle date/number formats by locale
- Plan RTL support from the start
- Use ICU message format for complex strings

### DON'T ❌

- Hardcode strings in components
- Concatenate translated strings
- Assume text size (German is 30% longer)
- Forget RTL layout
- Mix languages in the same file

---

## 6. Common Problems

- For missing translations, fall back to the default language.
- For hardcoded strings, use a linter or checker script.
- For date formatting, use `Intl.DateTimeFormat`.
- For number formatting, use `Intl.NumberFormat`.
- For pluralization, use the ICU message format.

---

## 7. RTL Support

```css
/* CSS Logical Properties */
.container {
  margin-inline-start: 1rem;  /* Not margin-left */
  padding-inline-end: 1rem;   /* Not padding-right */
}

[dir="rtl"] .icon {
  transform: scaleX(-1);
}
```

---

## 8. Checklist

Before deploying:

- [ ] All user-visible strings use translation keys
- [ ] Locale files exist for all supported languages
- [ ] Date/number formatting uses Intl API
- [ ] RTL layout tested (if applicable)
- [ ] Fallback language configured
- [ ] No hardcoded strings in components

---

## Script

- `scripts/i18n_checker.py` detects hardcoded strings and missing translations; run it with `python scripts/i18n_checker.py <project_path>`.

## Scope and Limitations

- Covers i18n/l10n implementation patterns — string extraction, locale files, RTL support, formatting. Does not cover translation services, translator workflow, or translation quality review
- Framework-agnostic guidance; specific library APIs (react-intl, vue-i18n, i18next) are covered at the pattern level, not as exhaustive API references
- Does not cover accessibility compliance related to language (WCAG 3.1) beyond RTL layout support
- Cultural adaptation beyond text direction and formatting (colors, imagery, gestures) is out of scope

