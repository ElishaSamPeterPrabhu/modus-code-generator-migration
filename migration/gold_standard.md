# Modus Web Components Gold Standard

## Introduction

This document defines the gold standard for Modus Web Components development and migration. It combines:
- Best practices and standards from the entire team's PR reviews and comments
- The official project code guidelines
- Actual patterns and conventions used in the Modus WC 2.0 repository

Use this as the primary reference for migration, verification, and code quality.

> **📖 For detailed technical guidelines:** See the comprehensive [CODE-GUIDELINES.md](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md) for in-depth technical specifications, examples, and implementation details.

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
- Components are organized in a flat directory structure (not atomic design hierarchy).

## 2. Coding Standards

> **💡 Detailed Reference:** For comprehensive coding standards with examples, see [CODE-GUIDELINES.md - Coding Standards](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md#coding-standards)

### TypeScript & Code Structure
- **TypeScript:**
  - Prefer TypeScript over JavaScript.
  - Define types/interfaces for all props and events.
  - Use `@Prop` for properties, with `!` for required and `?` for optional.
  - Interface naming convention: `IModusWc...` (e.g., `IModusWcButton`).
- **Events:**
  - Use `@Event` for custom events, named in camelCase.
  - Emit events with `this.emit`.
- **Import Organization:**
  - Alphabetically sort imports within groups.
  - Use ESLint import sorting rules for consistent grouping.
  - Remove unused imports before committing.

### CSS & Styling
> **💡 Detailed Reference:** See [CODE-GUIDELINES.md - CSS Styling](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md#coding-standards) for CSS variable usage and styling patterns.

- **CSS Variables & Classes:**
  - Use CSS variables for repeated values.
  - Prefix all CSS classes with `modus-wc-`.
  - Use BEM naming when creating custom classes: `modus-wc-loader--big`.
  - Prefer Tailwind/DaisyUI classes over custom SCSS when possible.
  - Place dynamic Tailwind classes in `<component>.tailwind.ts`.
- **Styling Best Practices:**
  - Use logical properties (e.g., `margin-inline-start`) for RTL support.
  - Add blank lines between styling blocks for readability.
  - Add blank lines between attributes and pseudo selectors.
  - Let code breathe - use appropriate spacing (it gets minified during compilation).
  - No scoped CSS - rely on strict class naming conventions.

### Code Formatting & Style
- **Alphabetical Sorting:**
  - Alphabetically sort properties in components, interfaces, and Storybook args.
  - Alphabetically sort HTML attributes on all elements.
  - Keep imports, exports, and object properties alpha sorted.
- **Blank Lines & Spacing:**
  - Add blank lines after conditional blocks for readability.
  - Add blank lines before interfaces and type definitions.
  - Add blank lines between major code sections.
  - Maintain blank lines at the end of files (helps with future additions).
- **Code Style:**
  - Enforce with Prettier and ESLint.
  - Use single quotes, proper indentation.
  - Use descriptive variable names that clearly indicate their type/purpose.

### Error Handling & Performance
- Use try-catch where needed, with meaningful error messages.
- Avoid unnecessary logging.
- Consider performance implications of CSS and JavaScript.

## 3. Accessibility (A11y)

> **💡 Detailed Reference:** See [CODE-GUIDELINES.md - Accessibility](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md#coding-standards) for WCAG standards and `inheritedAttributes` usage.

### WCAG Compliance
- All components must be accessible and WCAG 2.2 compliant.
- Fully operable via keyboard navigation.
- Use ARIA attributes and `inheritedAttributes` utilities.
- Use `aria-label` and other ARIA props as required.

### Accessibility Best Practices
- Set `tabindex="-1"` on non-interactive elements as an accessibility best practice.
- Ensure proper contrast ratios meet WCAG 2 AA minimum standards.
- Use semantic HTML elements when possible.
- Test with screen readers and keyboard-only navigation.
- Consider accessibility in icon usage (proper aria-labels for icon elements).

## 4. Testing & Quality Assurance

> **💡 Detailed Reference:** See [CODE-GUIDELINES.md - Testing and Quality Assurance](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md#testing-and-quality-assurance) for detailed testing examples and Jest patterns.

### Test Coverage & Standards
- **Coverage Goals:**
  - 100% unit test coverage is the goal; prioritize meaningful tests.
  - Use Jest and Stencil's `newSpecPage` for component tests.
  - Use snapshot testing for rendering consistency.
- **Test Naming & Structure:**
  - Use descriptive test names: `should do something when condition`.
  - Update snapshots when intentional changes are made (`npm run test:update-snapshot`).
  - Test all UI states, including RTL and theme variations.
- **CI/CD Requirements:**
  - CI pipelines must pass for all PRs.
  - Address merge-gate failures promptly.
  - Ensure all build processes (Angular, React integrations) pass.

## 5. Documentation & Comments

> **💡 Detailed Reference:** See [CODE-GUIDELINES.md - Documentation and Comments](../modus_migration/repos/modus-wc-2.0/CODE-GUIDELINES.md#documentation-and-comments) for Storybook documentation patterns and auto-generated README requirements.

### Code Documentation
- **JSDoc Standards:**
  - Use JSDoc for all props, methods, and events.
  - Provide inline comments for complex logic.
  - Document migration steps and rationale in PRs.
- **Component Documentation:**
  - Each component must have an auto-generated README and Storybook docs.
  - Document all events and properties in Storybook stories.
  - Include usage examples for different frameworks (React, Angular).
  - Keep configuration files well-documented.

### Storybook Standards
- Center all components in Storybook for consistent presentation.
- Include comprehensive stories covering all component states.
- Document component APIs thoroughly.
- Provide framework-specific usage examples.

## 6. Version Control & Collaboration

### Commit & PR Standards
- **Commit Messages:**
  - Use semantic commit messages (e.g., `feat:`, `fix:`, `docs:`).
  - Be descriptive about what changed and why.
- **Pull Request Requirements:**
  - PRs must have clear descriptions and rationale.
  - Fill out all PR template items completely.
  - Address review comments promptly and thoroughly.
  - Use GitHub Issues and Project Boards for tracking.

### Code Review Standards
- **Review Practices:**
  - Use "Nit" or "[Nitpick]" for minor style suggestions.
  - Provide constructive feedback with explanations.
  - Suggest specific improvements rather than just pointing out issues.
  - Consider both current functionality and future maintainability.

## 7. Framework Integration & Build Standards

### Multi-Framework Support
- **React Integration:**
  - Support multiple React versions (17, 18).
  - Ensure proper wrapper component generation.
  - Test React components in dedicated test applications.
- **Angular Integration:**
  - Support multiple Angular versions (17, 18).
  - Use proper Angular wrapper patterns.
  - Include value accessor bindings for form controls.
- **Build & Publishing:**
  - Use streamlined publishing workflows for all packages.
  - Maintain version synchronization across packages.
  - Use proper npm caching in CI/CD pipelines.

## 8. Migration & Development Best Practices

### Component Development
- **Design System Alignment:**
  - Follow Figma-approved designs when available.
  - Use Modus design tokens and color variables.
  - Maintain consistency with existing component patterns.
- **Code Quality:**
  - Never use inline styles; encapsulate styling logic.
  - Prefer existing patterns and directory structures.
  - Refactor for code reuse and DRYness.
  - Ensure all new/changed code is clean, readable, and follows conventions.

### Migration Guidelines
- **Legacy Component Handling:**
  - Replace legacy tags with `modus-wc-*` tags (if available in 2.0).
  - If a 2.0 tag or behavior does not exist, do not force migration—add a code comment explaining why.
  - Map all properties and events to new API.
  - Update all styles and layouts to 2.0 standards.
- **Verification Requirements:**
  - Verify slot structure matches 2.0 exactly for content projection.
  - Check ARIA and keyboard navigation for accessibility.
  - Ensure new layouts match the design system and are consistent across components.
  - Test all framework integrations (React, Angular).

---

## Example Migration Checklist
- [ ] All legacy tags replaced with `modus-wc-*` tags (if available in 2.0)
- [ ] All properties mapped to new API and alphabetically sorted
- [ ] All events updated to new API
- [ ] All styles and layouts updated to 2.0 standards
- [ ] All accessibility requirements met (WCAG 2.2 compliance)
- [ ] All tests updated and passing with proper coverage
- [ ] All documentation updated (JSDoc, Storybook, README)
- [ ] Code follows formatting standards (alpha sorting, blank lines, etc.)
- [ ] PR reviewed and all comments addressed
- [ ] Framework integrations tested (React, Angular)
- [ ] CI/CD pipelines passing

---

**This gold standard must be followed for all Modus Web Components migration and development.** 

*Last updated: Based on comprehensive analysis of team PR comments and practices from the Modus WC 2.0 repository.* 