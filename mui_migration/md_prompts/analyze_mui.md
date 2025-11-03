# MUI to Modus Migration Analyze Tool

## Purpose
Analyze provided code for Material-UI (MUI) v7 components. For each MUI component, identify its Modus V2 web component equivalent and outline the migration approach based on the detected framework (React, Angular, or Vanilla JS). This analysis will serve as the blueprint for the `migrate_mui.md` phase.

## Data Sources
- `mui_to_modus_mapping.json`: Maps MUI component names to their Modus V2 **web component** equivalents (e.g., `Button` maps to `modus-wc-button`). Includes confidence levels, complexity ratings, and migration notes.
- `mui_v7_components.json`: Details about MUI v7 components, their properties, and events.
- `v2_components.json`: Details about Modus V2 **web components** (e.g., `modus-wc-button`, `modus-wc-alert`). This is the source of truth for existing V2 web components, their properties, and events.
- `v2_react_framework_data.json`: **How-to guide** for using Modus V2 **web components** within React.
- `v2_angular_framework_data.json`: **How-to guide** for using Modus V2 **web components** within Angular.

## Core Analysis Objective
For each source file, produce an `analysis_report.md` detailing:
*   **Framework Identification**: Clearly state the detected framework (primarily React for MUI, but could be Angular or others). This is CRITICAL.
*   **MUI Components Found**: List each MUI component, its props, and context.
*   **Proposed Modus V2 Migration Strategy**:
    *   **Identify V2 Web Component**: Use `mui_to_modus_mapping.json` to find the Modus V2 **web component** tag (e.g., `modus-wc-button` for MUI `Button`). Verify its existence and details in `v2_components.json`.
    *   **Component Complexity**: Note the complexity rating from the mapping (low, medium, high).
    *   **Confidence Level**: Note the confidence level from the mapping (high, medium, low).
    *   **Migration Approach Based on Framework**:
        *   **React** (most common for MUI):
            *   Target is the Modus V2 **web component tag** directly in JSX (e.g., `<modus-wc-button>`).
            *   Note that `v2_react_framework_data.json` will be consulted for:
                *   Ensuring `defineCustomElements()` is called.
                *   Correctly passing attributes/properties to the web component in JSX.
                *   Handling events on the web component in JSX.
        *   **Angular** (if MUI is used in Angular):
            *   Target is the Modus V2 **web component tag** directly in Angular templates.
            *   Note that `v2_angular_framework_data.json` will be consulted for proper integration.
*   **Migration Feasibility**: Based on mapping confidence and complexity.
*   **Potential Issues/Notes**:
    *   If no Modus equivalent exists (component in `no_direct_mapping` list): "**No Modus V2 equivalent found for MUI `[Component Name]`.** This component will require custom implementation or architectural changes."
    *   Theme-related props (sx, styled components): "MUI theming system needs conversion to Modus design tokens and CSS."
    *   Icon handling: "MUI icons (e.g., `<DeleteIcon />`) need replacement with `<modus-wc-icon name='delete'></modus-wc-icon>`."
    *   Composite components: Note related components that need coordinated migration.

## MUI-Specific Analysis Rules:

1.  **Import Analysis**: 
    *   Identify MUI imports (e.g., `import { Button, TextField } from '@mui/material'`).
    *   Track MUI icon imports (e.g., `import DeleteIcon from '@mui/icons-material/Delete'`).
    *   Note theme imports and styled component usage.

2.  **Component Identification**:
    *   MUI components are typically PascalCase (e.g., `<Button>`, `<TextField>`).
    *   Identify component props and their values.
    *   Note event handlers (onClick, onChange, etc.).

3.  **Special MUI Patterns**:
    *   **sx prop**: Needs conversion to CSS classes or inline styles.
    *   **theme usage**: Track theme-dependent values.
    *   **Composite patterns**: Grid, Box, Stack need CSS-based replacement.
    *   **Form controls**: FormControl, InputLabel patterns need restructuring.

4.  **Property Analysis**:
    *   Map MUI props to potential Modus props.
    *   Identify props with no direct equivalent.
    *   Note props requiring transformation (e.g., `variant="contained"` → `variant="filled"`).

5.  **Event Mapping**:
    *   MUI events often have direct Modus equivalents with different names.
    *   Note event signature differences.

## Output Generation

1.  **Report Content**: For each input source file, compile an analysis report including:
    *   List of MUI imports and their usage.
    *   Detailed component analysis with:
        *   MUI component name and location in code.
        *   Props used and their values.
        *   Proposed Modus component and confidence level.
        *   Property mapping strategy.
        *   Required structural changes.
    *   Overall migration complexity assessment.
    *   Step-by-step migration recommendations.

2.  **Saving the Report**:
    *   Follow the same directory structure rules as Modus V1 migration.
    *   Save as `[original_filename].mui-analysis.md` to distinguish from V1 migration reports.
    *   Create `analysis_reports/mui/` subdirectory structure mirroring source files.

## Example Analysis Output

```markdown
# MUI Migration Analysis Report
**Source File**: src/components/UserForm.jsx
**Framework**: React
**MUI Version**: 7.x

## Components Found

### 1. Button (Line 45)
- **MUI Usage**: `<Button variant="contained" color="primary" onClick={handleSubmit}>Submit</Button>`
- **Target Modus Component**: `modus-wc-button`
- **Confidence**: High
- **Complexity**: Medium
- **Property Mappings**:
  - `variant="contained"` → `variant="filled"`
  - `color="primary"` → `color="primary"`
  - `onClick` → `@buttonClick` (event rename)
- **Notes**: Direct mapping available with property transformations

### 2. TextField (Line 52)
- **MUI Usage**: `<TextField label="Username" value={username} onChange={handleChange} error={hasError} helperText="Enter username" />`
- **Target Modus Component**: `modus-wc-text-input`
- **Confidence**: High
- **Complexity**: Medium
- **Property Mappings**:
  - `label` → Use separate `<modus-wc-input-label>`
  - `value` → `value`
  - `onChange` → `@valueChange`
  - `error` → `invalid`
  - `helperText` → Use separate `<modus-wc-input-feedback>`
- **Notes**: Requires structural changes for label and helper text

## Migration Summary
- **Overall Complexity**: Medium
- **Components with no mapping**: 0
- **Manual interventions needed**: 2 (label/helper text structure)
```
