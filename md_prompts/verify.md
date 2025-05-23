# Modus Migration Verification Tool

## Purpose
Verify migrated code or files against the Modus Web Components Gold Standard (`migration/gold_standard.md`).

## Data Source
- **Gold Standard**: All verification must reference the rules, best practices, and checklist in `migration/gold_standard.md`.

## Input
- The tool should support verifying:
  - A single file
  - All files in a specified folder (each file checked individually)
  - A code snippet

## Rules
- For each file or code snippet:
  - Compare the code against all relevant sections of the gold standard (structure, naming, properties, events, styling, accessibility, testing, documentation, version control, migration best practices, etc.).
  - For each section, check for both compliance and non-compliance.
  - If a rule is not met, provide a clear, actionable comment explaining what is missing or incorrect, referencing the relevant gold standard section.
  - If a rule is met, note the compliance.
  - If a rule is not applicable, state so.
- Summarize the results for each file or snippet, listing all issues and all points of compliance.
- Provide an overall pass/fail status for each file or snippet.

## Output Format
- For a single file or snippet, output a detailed summary with:
  - Compliance table (section, status, notes)
  - List of all issues found, with actionable feedback
  - List of all points of compliance
  - Overall pass/fail status
- For multiple files, output a separate summary for each file, clearly labeled with the file name.

## Example
Given this code:
```code
// Import Modus Web Components and styles here if required
<modus-wc-button variant="primary">Click</modus-wc-button>
// No v2 equivalent for modus-foo
<modus-foo>Legacy</modus-foo>
```
The output should be:

### Verification Summary
| Section                | Status   | Notes                                      |
|------------------------|----------|--------------------------------------------|
| Component Naming       | Pass     | Uses modus-wc-* tags                       |
| Imports                | Warning  | Import comment present, but not actual code |
| Properties/Attributes  | Pass     | Uses 'variant' as per v2 API               |
| Unmigrated Components  | Pass     | Comment explains missing v2 equivalent      |
| Accessibility          | N/A      | Not applicable for this snippet            |
| Testing                | N/A      | Not applicable for this snippet            |
| Documentation          | N/A      | Not applicable for this snippet            |

**Issues:**
- Imports: Add actual Modus Web Components and styles imports as per gold standard.

**Compliant:**
- All tags use the correct modus-wc-* naming.
- Properties are mapped to the v2 API.
- Unmigrated components are commented as required.

**Overall Status:**
- **Fail** (due to missing imports) 