# Modus Migration Logging Tool

## Purpose
Log a comprehensive summary of the entire migration process, including analysis, migration, verification, and any issues or recommendations, following the latest workflow and gold standard.

## Rules
- Summarize each step: analysis, migration, verification, using the actual outputs from those steps.
- For analysis, include the authoritative v1/v2 mapping table and any notes.
- For migration, list all replacements, unmigrated tags, and any comments added for missing features or properties.
- For verification, include the compliance table, list of issues, compliant points, and overall pass/fail status (as per verify.md).
- For multiple files, output a separate summary for each file, clearly labeled with the file name.
- Use Markdown headings, bullet points, and tables for clarity.
- End with a final status and actionable recommendations based on verification issues.

## Output Format
- Use Markdown headings and bullet points for clarity.
- Include tables for issues, changes, and compliance as needed.
- For multiple files, repeat the full summary for each file, labeled with the file name.

## Example
```
# Migration Summary

## File: example.html

### Analysis
| v1 Tag      | v2 Tag          | Count | Notes                |
|-------------|-----------------|-------|----------------------|
| modus-button| modus-wc-button | 1     | Direct replacement   |
| modus-foo   | N/A             | 1     | No v2 equivalent     |

**Notes:**
- All v1 tags analyzed using authoritative mapping.

### Migration
- Replaced modus-button with modus-wc-button
- // No v2 equivalent for modus-foo (comment added above component)
- All required Modus imports added

### Verification Summary
| Section                | Status   | Notes                                      |
|------------------------|----------|--------------------------------------------|
| Component Naming       | Pass     | Uses modus-wc-* tags                       |
| Imports                | Pass     | All required imports present                |
| Properties/Attributes  | Pass     | Uses 'variant' as per v2 API               |
| Unmigrated Components  | Pass     | Comment explains missing v2 equivalent      |
| Accessibility          | Warning  | aria-label missing on button                |
| Testing                | N/A      | Not applicable for this snippet            |
| Documentation          | N/A      | Not applicable for this snippet            |

**Issues:**
- Accessibility: Add aria-label to all buttons

**Compliant:**
- All tags use the correct modus-wc-* naming.
- Properties are mapped to the v2 API.
- Unmigrated components are commented as required.

**Overall Status:**
- **Fail** (due to missing aria-label)

### Recommendations
- Add aria-label to all buttons
- Review tags with no v2 equivalent 