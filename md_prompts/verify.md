# Modus Migration Verification Tool

## Purpose
Verify that the migrated code fully complies with the Modus Web Components gold standard and migration rules.

## Rules
- Check that all v1 tags have been replaced with v2 tags (modus-wc-*).
- Ensure all required attributes and imports are present.
- Check for accessibility (e.g., aria-labels).
- List any issues or non-compliance found.

## Output Format
- Output a Markdown checklist of verification points.
- List any issues in a Markdown table with details.
- Provide a summary status: Compliant / Non-Compliant.

## Example
Given this migrated code:
```html
<modus-wc-button variant="primary">Click</modus-wc-button>
<modus-foo>Legacy</modus-foo>
```
The output should be:
- [x] All v1 tags replaced
- [x] Required attributes present
- [ ] All tags have v2 equivalents
- [x] Required imports present
- [ ] Accessibility: aria-label missing

| Issue         | Details                        |
|--------------|---------------------------------|
| No v2 tag    | modus-foo has no v2 equivalent  |
| Accessibility| aria-label missing on button    |

**Status:** Non-Compliant 