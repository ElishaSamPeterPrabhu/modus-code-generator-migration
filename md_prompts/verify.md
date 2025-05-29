# Modus Migration Verification Tool

## Purpose
Verify migrated code or files (including Angular and React specific migrations) against the Modus Web Components Gold Standard (`migration/gold_standard.md`) and framework-specific best practices as outlined in the `_framework_data.json` files.

## Data Sources
- **Gold Standard**: All verification must reference the rules, best practices, and checklist in `migration/gold_standard.md`.
- **v2_angular_framework_data.json**: Contains v2 Angular integration documentation (from `.mdx`) and expected patterns.
- **v2_react_framework_data.json**: Contains v2 React integration documentation (from `.mdx`) and expected patterns/examples.
- **Analysis Report**: The `.analysis.md` file for the component/file being verified. This is crucial to understand what *should* have been migrated and why.

## Input
- The tool should support verifying:
  - A single file
  - All files in a specified folder (each file checked individually)
  - A code snippet
- The corresponding analysis report (`<filename>.analysis.md`) should be available and consulted.

## Rules
- For each file or code snippet:
  - **Consult Analysis Report**: Before verification, review the corresponding `.analysis.md` file. Pay close attention to components marked as "N/A" or "N/A (Blocked by Parent)". These components should remain as v1 in the migrated code, and this is considered correct behavior.
  - **Parent-Child Migration Rule Verification:**
    - Confirm that if a parent component was not migrated (as per analysis), its child components also remain unmigrated in the code. If child components were migrated despite a non-migrated parent, this is a failure.
  - **Framework-Specific Verification (Angular/React):**
    - If the file is an Angular or React file:
      - Consult the `documentation` and `examples` in `v2_angular_framework_data.json` or `v2_react_framework_data.json`.
      - Verify that migrated components use correct framework-specific wrappers, event handling, attribute bindings, and import statements as recommended in these data sources and the general `modusmcp` custom instructions.
      - Check for adherence to best practices mentioned in the framework `.mdx` documentation.
  - Compare the migrated code against all relevant sections of the gold standard (structure, naming, properties, events, styling, accessibility, testing, documentation, version control, migration best practices, etc.).
  - For each section/rule (from gold standard or framework data):
    - Check for both compliance and non-compliance.
    - If a rule is not met, provide a clear, actionable comment explaining what is missing or incorrect, referencing the relevant gold standard section or framework documentation.
    - If a rule is met, note the compliance.
    - If a rule is not applicable (e.g., accessibility for a non-UI utility), state so.
- Summarize the results for each file or snippet, listing all issues and all points of compliance.
- Provide an overall pass/fail status for each file or snippet. A "pass" means all applicable rules from the gold standard and relevant framework data are met, and the parent-child migration rule was correctly followed based on the analysis.

## Output Format
- For a single file or snippet, output a detailed summary with:
  - Compliance table (section/rule, status, notes referencing gold standard or framework doc)
  - List of all issues found, with actionable feedback
  - List of all points of compliance
  - Overall pass/fail status
- For multiple files, output a separate summary for each file, clearly labeled with the file name.

## Example
Given migrated code and its analysis report. Analysis showed `modus-parent` was N/A, so it and `modus-child` should remain v1. `modus-button` was migratable.
Migrated Code (React context):
```tsx
// import { ModusWcButton } from '@trimble-oss/moduswebcomponents-react'; // Missing import
// MODUS MIGRATION: 'modus-parent' not migrated (no v2 equivalent). Child components also not migrated.
<modus-parent>
  <modus-child />
</modus-parent>
<ModusWcButton color="primary" onClick={handleClick}>Click Me</ModusWcButton> // Incorrect attribute: 'color' instead of 'variant' or buttonStyle as per v2 React component. 
```
The output should be:

### Verification Summary: my-component.tsx
| Section                             | Status   | Notes                                                                                      |
|-------------------------------------|----------|--------------------------------------------------------------------------------------------|
| Gold Standard: Component Naming     | Pass     | Migrated component `ModusWcButton` uses correct naming.                                    |
| Gold Standard: Imports              | Fail     | React specific import for `ModusWcButton` is missing.                                      |
| Gold Standard: Properties/Attributes| Fail     | `ModusWcButton` uses `color="primary"`. Should be `buttonStyle="primary"` or `variant="primary"` (confirm with v2_react_framework_data.json & v2_components.json). |
| Parent-Child Rule Adherence         | Pass     | `modus-parent` and `modus-child` correctly left unmigrated as per analysis.                |
| Framework: React Best Practices   | Warning  | Review `v2_react_framework_data.json` for exact prop names for `ModusWcButton`. Example uses `buttonStyle` for `modus-wc-button` in general, but React wrapper might differ.|
| Accessibility                       | Check    | Needs manual check for ARIA attributes on `ModusWcButton`.                                   |

**Issues:**
- Imports: Add `import { ModusWcButton } from '@trimble-oss/moduswebcomponents-react';` (Verify exact import path from framework data).
- Properties: `ModusWcButton` attribute `color="primary"` is incorrect. Correct to `buttonStyle="primary"` or `variant="primary"` after checking documentation for the React wrapper.

**Compliant:**
- Unmigrated `modus-parent` and `modus-child` correctly handled based on analysis.
- Migrated `ModusWcButton` uses PascalCase, typical for React components.

**Overall Status:**
- **Fail** (due to missing imports and incorrect property usage) 