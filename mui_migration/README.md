# MUI to Modus Migration System

## Overview
This system helps migrate Material-UI (MUI) v7 components to Trimble Modus V2 Web Components. It provides automated analysis, migration guidance, and verification tools.

## Structure

```
mui_migration/
├── component_extraction/     # MUI component data extraction
│   ├── extract_mui_components.py
│   ├── mui_v7_components.json
│   └── [component]-mui-v7.json files
├── mapping/                  # Component and property mappings
│   └── mui_to_modus_mapping.json
├── md_prompts/              # Migration workflow prompts
│   ├── analyze_mui.md
│   ├── migrate_mui.md
│   ├── verify_mui.md
│   ├── log_mui.md
│   └── workflow_mui.md
├── mcp_server_mui.py        # MCP server for migration tools
└── test/                    # Test files for migration
    └── UserForm.jsx
```

## Quick Start

1. **Extract MUI Components** (already done):
   ```bash
   cd component_extraction
   python3 extract_mui_components.py
   ```

2. **Run MCP Server**:
   ```bash
   python3 mcp_server_mui.py
   ```

3. **Use Migration Tools**:
   - `get_mui_workflow_guidance()` - Get complete workflow guide
   - `get_mui_analyze_guidance()` - Analyze MUI components
   - `get_mui_migrate_guidance()` - Migration instructions
   - `get_mui_verify_guidance()` - Verification steps
   - `get_mui_component_mapping(name)` - Get specific mapping

## Component Mapping

### High Confidence Mappings
- Button → modus-wc-button
- TextField → modus-wc-text-input
- Checkbox → modus-wc-checkbox
- Alert → modus-wc-alert
- Switch → modus-wc-switch
- Chip → modus-wc-chip

### Components Requiring Structure Changes
- TextField with labels → modus-wc-input-label + modus-wc-text-input
- IconButton → modus-wc-button with shape="circle"
- Card → modus-wc-card with different slot structure

### No Direct Mapping
- Grid, Box, Stack → Use CSS Grid/Flexbox
- Typography → HTML elements with Modus classes
- FormControl group → Manual restructuring needed

## Migration Process

### Phase 1: Analyze
1. Identify MUI components in source files
2. Check mapping availability
3. Assess migration complexity
4. Generate analysis report

### Phase 2: Migrate
1. Transform imports
2. Replace components
3. Map properties
4. Handle special patterns (icons, forms)
5. Generate migrated code

### Phase 3: Verify
1. Check component validity
2. Verify prop mappings
3. Test functionality
4. Generate verification report

### Phase 4: Log
1. Consolidate all reports
2. Generate statistics
3. Create action items
4. Provide summary

## Key Differences from V1 Migration

1. **Component Format**: MUI uses PascalCase React components vs lowercase web components
2. **Import System**: Need to handle @mui/material imports
3. **Styling**: sx prop and theme system need conversion
4. **Icons**: Separate icon library migration required
5. **Layout**: No direct equivalents for layout components

## Common Patterns

### Button with Icon
```jsx
// MUI
<Button startIcon={<DeleteIcon />}>Delete</Button>

// Modus
<modus-wc-button>
  <modus-wc-icon name="delete"></modus-wc-icon>
  Delete
</modus-wc-button>
```

### Form Field
```jsx
// MUI
<TextField 
  label="Name" 
  error={hasError}
  helperText="Enter your name"
/>

// Modus
<div>
  <modus-wc-input-label for="name">Name</modus-wc-input-label>
  <modus-wc-text-input id="name" invalid={hasError}></modus-wc-text-input>
  <modus-wc-input-feedback type="invalid">Enter your name</modus-wc-input-feedback>
</div>
```

## Testing

Use the provided test file (`test/UserForm.jsx`) to test the migration process:
1. Run analysis on the file
2. Apply migrations
3. Verify the results

## Integration with n8n

The MCP server can be integrated with n8n to provide two tools:
1. **mui-modus-guidance** - Provides mapping and guidance
2. **mui-modus-transform** - Performs code transformation

## Notes

- This system uses a hybrid approach: automated analysis with manual property mapping
- Complex components may require manual intervention
- Always verify migrated code functionality
- Consider performance implications of web components
