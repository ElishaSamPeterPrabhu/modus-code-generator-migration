# Modus Migration Agentic Workflow Tool

## Purpose
Guide the user or agent through the Modus Web Components migration process (including Angular and React contexts) step by step, ensuring confirmation at each stage and using authoritative standards and outputs.

## Core Principles
- **Authoritative Data**: All decisions and actions must be based on the provided JSON data files and the `gold_standard.md`.
- **Framework Awareness**: The workflow must account for Angular and React specific migration patterns using the `*_framework_data.json` files.
- **Parent-Child Integrity**: The Parent-Child Migration Rule (if a parent isn't migrated, children aren't either) is paramount and must be enforced throughout.
- **User Confirmation**: Each major step (Analysis, Migration, Verification, Logging) requires user confirmation before proceeding.

## Data Sources to be Used Throughout
- **JSON Data Files**: `component_mapping.json`, `v1_components.json`, `v2_components.json`, `v1_angular_framework_data.json`, `v1_react_framework_data.json`, `v2_angular_framework_data.json`, `v2_react_framework_data.json`.
- **Markdown Guides**: `analyze.md`, `migrate.md`, `verify.md`, `log.md` for step-specific instructions.
- **Gold Standard**: `migration/gold_standard.md` for verification criteria.

## Workflow Steps

### 1. Initial Setup & Analysis (`analyze.md`)
- **Action**: Load all JSON data sources listed above.
- **Action**: Perform analysis as per `analyze.md`. This includes:
    - Identifying v1 components.
    - Detecting Angular/React context and flagging for use of framework data.
    - Applying the Parent-Child Migration Rule to determine migratability.
    - Suggesting v2 equivalents or marking as N/A / Blocked by Parent.
    - Generating the `.analysis.md` file for each input file.
- **Output**: Present the summary analysis table (as per `analyze.md` example) for each analyzed file. Highlight any framework-specific considerations noted and the impact of the Parent-Child Migration Rule.
- **User Prompt**: "Analysis complete. Review the generated `.analysis.md` files. Reply 'proceed to migrate' to continue to the migration step, or specify changes/concerns."

### 2. Code Migration (`migrate.md`)
- **Pre-condition**: User confirms to proceed.
- **Action**: Perform code migration based *strictly* on the `.analysis.md` output and rules in `migrate.md`. This includes:
    - Replacing migratable v1 tags with v2 tags.
    - Applying attribute mappings.
    - **NOT migrating components marked N/A or N/A (Blocked by Parent) in the analysis.** Add comments explaining why.
    - Implementing framework-specific changes (wrappers, event handling, imports) using `*_framework_data.json` for Angular/React files.
    - Adding comments for unmigrated features/properties.
- **Output**: Present the migrated code block for each file. Below it, list any components that were not migrated and why (consistent with analysis and parent-child rule).
- **User Prompt**: "Migration attempt complete. Review the modified code. Reply 'proceed to verify' to continue to the verification step, or specify changes/concerns."

### 3. Verification (`verify.md`)
- **Pre-condition**: User confirms to proceed.
- **Action**: Verify the migrated code against `gold_standard.md` and framework-specific criteria (from `v2_*_framework_data.json`) as per `verify.md`. This involves:
    - Confirming adherence to the Parent-Child Migration Rule (i.e., blocked components correctly remained v1).
    - Checking for correct application of framework-specific patterns for Angular/React.
    - Validating imports, properties, naming, accessibility, etc.
- **Output**: Present the detailed verification summary table, list of issues, compliant points, and overall pass/fail status for each file.
- **User Prompt**: "Verification complete. Review the verification reports. Reply 'proceed to log' to continue to the logging step, or specify changes/concerns."

### 4. Logging (`log.md`)
- **Pre-condition**: User confirms to proceed.
- **Action**: Generate a comprehensive migration log as per `log.md`. This log should consolidate:
    - Analysis summary (including parent-child rule impacts and framework context).
    - Migration actions (what was changed, what wasn't and why, framework adaptations).
    - Full verification report.
    - Final status and actionable recommendations for each file.
- **Output**: Present the generated consolidated `migration_log.md` (or a snippet if too long, with instructions on where to find the full log).
- **User Prompt**: "Logging complete. The full migration log has been generated. Review `migration_log.md`. The migration workflow for the selected file(s) is now finished."

## General Rules for the Agent
- At each step, explicitly state which markdown guide (`analyze.md`, `migrate.md`, etc.) is being followed.
- When presenting information for multiple files, clearly label each file's section.
- Ensure all outputs (tables, code blocks, summaries) are well-formatted in Markdown.
- If the user raises concerns or asks for changes at any step, address them before re-prompting for confirmation to proceed.

## Example Snippet (Illustrating a mid-workflow point)

Currently at: **Step 2: Code Migration** (following `migrate.md`)

**File: `src/components/my-button.jsx`** (React context identified)

Analysis from `my-button.jsx.analysis.md` indicated:
| v1 Tag         | v2 Tag                     | Count | Notes                                         |
|----------------|----------------------------|-------|-----------------------------------------------|
| modus-button   | modus-wc-button            | 1     | Direct replacement. Use React wrapper.        |

Migrated code for `src/components/my-button.jsx`:
```javascript
import { ModusWcButton } from '@trimble-oss/moduswebcomponents-react'; // Added based on v2_react_framework_data.json

export const MyButton = ({ onClick, children }) => {
  return (
    <ModusWcButton buttonStyle="primary" onButtonClick={onClick}>
      {children}
    </ModusWcButton>
  );
};
```

**Migration Notes for `src/components/my-button.jsx`:**
- `modus-button` replaced with `ModusWcButton` React component.
- `buttonStyle="primary"` used as per v2 component properties.
- Event handling `onButtonClick` used as per React wrapper conventions.
- Import for `ModusWcButton` added.

---
Migration attempt complete. Review the modified code. Reply 'proceed to verify' to continue to the verification step, or specify changes/concerns.