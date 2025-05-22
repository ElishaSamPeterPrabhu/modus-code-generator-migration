# Modus Web Components Gold Standard

## Introduction

This document defines the gold standard for Modus Web Components development and migration. It combines:
- Best practices and standards from Gabriel Piltzer's PR reviews
- The official project code guidelines

Use this as the primary reference for migration, verification, and code quality.

---

## 1. Component Structure & Organization
- Each component must be self-contained in its own directory, with:
  - Component file (e.g., `modus-wc-button.tsx`)
  - Styles file (e.g., `modus-wc-button.scss`)
  - Test file (e.g., `modus-wc-button.spec.ts`)
  - Storybook file (e.g., `modus-wc-button.stories.ts`)
  - Auto-generated README
- Use meaningful, descriptive, and kebab-case names for files and components.
- Tag names must follow the `modus-wc-*` pattern.

## 2. Coding Standards
- **TypeScript:**
  - Prefer TypeScript over JavaScript.
  - Define types/interfaces for all props and events.
  - Use `@Prop` for properties, with `!` for required and `?` for optional.
- **Events:**
  - Use `@Event` for custom events, named in camelCase.
  - Emit events with `this.emit`.
- **CSS & Styling:**
  - Use CSS variables for repeated values.
  - Prefix all CSS classes with `modus-wc-`.
  - Prefer Tailwind/DaisyUI classes over custom SCSS.
  - Place dynamic Tailwind classes in `<component>.tailwind.ts`.
  - Use logical properties (e.g., `margin-inline-start`) for RTL support.
- **Code Style:**
  - Enforce with Prettier and ESLint.
  - Use single quotes, proper indentation, and blank lines for readability.
- **Error Handling:**
  - Use try-catch where needed, with meaningful error messages.
  - Avoid unnecessary logging.

## 3. Accessibility (A11y)
- All components must be accessible and WCAG 2.2 compliant.
- Fully operable via keyboard.
- Use ARIA attributes and `inheritedAttributes` utilities.
- Use `aria-label` and other ARIA props as required.

## 4. Testing & Quality Assurance
- 100% unit test coverage is the goal; prioritize meaningful tests.
- Use Jest and Stencil's `newSpecPage` for component tests.
- Use descriptive test names: `should do something when condition`.
- Use snapshot testing for rendering consistency.
- CI pipelines must pass for all PRs.

## 5. Documentation & Comments
- Use JSDoc for all props, methods, and events.
- Provide inline comments for complex logic.
- Each component must have an auto-generated README and Storybook docs.
- Document all events and properties in Storybook stories.
- Keep configuration files well-documented.

## 6. Version Control & Collaboration
- Use semantic commit messages (e.g., `feat:`, `fix:`).
- No unused imports in commits.
- PRs must have clear descriptions and rationale.
- Address review comments promptly and thoroughly.
- Fill out all PR template items.
- Use GitHub Issues and Project Boards for tracking.

## 7. Review & Migration Best Practices (from Gabriel Piltzer's PRs)
- Always follow atomic design principles and Figma-approved designs.
- Never use inline styles; encapsulate styling logic.
- Prefer existing patterns and directory structures.
- Refactor for code reuse and DRYness.
- Ensure all new/changed code is clean, readable, and follows conventions.
- Test all UI states, including RTL and theme variations.
- Document migration steps and rationale in PRs.
- If a 2.0 tag or behavior does not exist, do not force migration—add a code comment explaining why.
- For slots and content projection, verify slot structure matches 2.0 exactly.
- For accessibility, always check ARIA and keyboard navigation.
- For styling, ensure new layouts match the design system and are consistent across components.

---

## Example Migration Checklist
- [ ] All legacy tags replaced with `modus-wc-*` tags (if available in 2.0)
- [ ] All properties mapped to new API
- [ ] All events updated to new API
- [ ] All styles and layouts updated to 2.0 standards
- [ ] All accessibility requirements met
- [ ] All tests updated and passing
- [ ] All documentation updated
- [ ] PR reviewed and all comments addressed

---

**This gold standard must be followed for all Modus Web Components migration and development.** 