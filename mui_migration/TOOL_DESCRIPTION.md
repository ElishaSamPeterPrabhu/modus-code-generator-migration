# MUI Migration Assistant Tool

This tool provides MUI to Modus migration guidance and mappings.

## Input
A string representing either:
1. The word **"mapping"** - to get component mapping information
2. A process/workflow name: **"analyze"**, **"migrate"**, **"verify"**, **"log"**, or **"workflow"**

## Output

### If input is "mapping"
Returns the unified mapping JSON file containing both directions:
- `component_mappings.json` with structure:
  ```json
  {
    "mui_to_modus": { "Button": "modus-wc-button", ... },
    "modus_to_mui": { "modus-wc-button": "Button", ... }
  }
  ```

### If input is a process name
Returns the filename of the workflow documentation:
- `"analyze"` → `"analyze_mui.md"`
- `"migrate"` → `"migrate_mui.md"`
- `"verify"` → `"verify_mui.md"`
- `"log"` → `"log_mui.md"`
- `"workflow"` → `"workflow_mui.md"`

## Examples
- Input: `"mapping"` → Output: `component_mappings.json`
- Input: `"analyze"` → Output: `"analyze_mui.md"`
- Input: `"workflow"` → Output: `"workflow_mui.md"`

## What This Tool Helps With

This tool helps developers:
- **Access component mappings** between MUI v7 and Modus V2
- **Locate workflow documentation** for each migration phase
- **Understand** which MUI components have Modus equivalents
- **Navigate** the migration process from analysis through verification

## About MUI Migration

Material-UI (MUI) v7 is a comprehensive React component library. Migration to Modus involves:
- Converting MUI React components to Modus web components
- Transforming MUI's `sx` prop and theme system to Modus design tokens
- Mapping MUI icons to Modus icons
- Handling MUI-specific patterns (Grid, Box, Stack)
- Converting form composition patterns

Use this tool to streamline the MUI to Modus migration process.
