# Modus Migration Logging Tool

## Purpose
Log a summary of the entire migration process, including analysis, migration, verification, and any issues found.

## Rules
- Summarize each step: analysis, migration, verification.
- List all changes made and issues found.
- Output a Markdown summary with sections for each step.
- Include a final status and any recommendations.

## Output Format
- Use Markdown headings and bullet points for clarity.
- Include tables for issues or changes if needed.

## Example
```
# Migration Summary

## Analysis
- Found 2 v1 tags: modus-button, modus-foo

## Migration
- Replaced modus-button with modus-wc-button
- Could not migrate modus-foo (no v2 equivalent)

## Verification
- [x] All v1 tags replaced
- [ ] Accessibility: aria-label missing

| Issue         | Details                        |
|--------------|---------------------------------|
| No v2 tag    | modus-foo has no v2 equivalent  |
| Accessibility| aria-label missing on button    |

## Final Status
**Non-Compliant**

## Recommendations
- Add aria-label to all buttons
- Review tags with no v2 equivalent 