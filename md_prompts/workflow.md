# Modus Migration Agentic Workflow Tool

## Purpose
Guide the user or agent through the Modus Web Components migration process step by step, ensuring confirmation at each stage and using authoritative standards and outputs.

## Rules
- Always start with analysis using authoritative JSONs (`component_mapping.json`, `v1_components.json`, `v2_components.json`).
- At each step, the agent must reference and follow the corresponding authoritative md file for instructions, output format, and compliance:
  - **Analysis:** Use `analyze.md` for rules and output.
  - **Migration:** Use `migrate.md` for rules and output.
  - **Verification:** Use `verify.md` for rules and output.
  - **Logging:** Use `log.md` for rules and output.
- After each step, present the result and prompt the user to confirm before proceeding.
- Only proceed to migration, verification, or logging if the user explicitly confirms.
- Each step should use the latest prompt and output format from the corresponding md file:
  - **Analysis:** Outputs a v1/v2 mapping table and notes, using authoritative data.
  - **Migration:** Uses the analysis output and authoritative JSONs, migrates only what is supported, adds comments for unmigrated tags or missing features, and supports any code format.
  - **Verification:** Compares the result to `migration/gold_standard.md`, outputs a compliance table, issues, compliant points, and overall status, for one or multiple files.
  - **Logging:** Summarizes all steps, includes tables and actionable recommendations, and outputs a separate summary for each file if needed.
- Summarize the workflow in Markdown at each step.

## Output Format
- Use Markdown headings for each step.
- Present prompts and results as bullet points or tables.
- Clearly indicate the current step and next available actions.
- For multiple files, output a separate summary for each file, clearly labeled.

## Example
```
# Migration Workflow

## Step 1: Analysis
| v1 Tag      | v2 Tag          | Count | Notes                |
|-------------|-----------------|-------|----------------------|
| modus-button| modus-wc-button | 1     | Direct replacement   |
| modus-foo   | N/A             | 1     | No v2 equivalent     |

**Notes:**
- All v1 tags analyzed using authoritative mapping.
- Reply 'proceed' to continue to migration.

## Step 2: Migration
- Replaced modus-button with modus-wc-button
- // No v2 equivalent for modus-foo (comment added above component)
- All required Modus imports added
- Reply 'verify' to verify the migration.

## Step 3: Verification
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
- Reply 'log' to log the migration summary.

## Step 4: Logging
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

- Workflow complete. 