# Complete Modus Migration Systems Overview

## Four Migration Systems in One Server

This MCP server provides comprehensive migration assistance for **all major UI libraries** migrating to Modus V2 web components.

---

## 1. Shadcn/UI → Modus V2

### Overview
Migrate shadcn/ui (React + Radix UI + Tailwind CSS) components to Modus V2 web components.

### Component Coverage
**42+ shadcn components** with direct Modus equivalents:
- Button, Input, Card, Alert, Dialog, Select, Tabs
- Accordion, Badge, Breadcrumb, Checkbox, Chip
- And more...

### Key Challenges
1. **Tailwind CSS Conversion** - Utility classes → Modus design tokens/CSS
2. **Radix UI Primitives** - Primitive behaviors → Modus standalone components
3. **Copy-Paste Model** - Components live in codebase (may be customized)
4. **Composition Patterns** - Card/Form/Dialog with sub-components

### Components Without Mapping
- Command (command palette)
- Carousel
- Form (composition helper)
- ScrollArea
- AspectRatio
- InputOTP
- ToggleGroup

### Available MCP Tools
- `get_shadcn_component_mapping()` - Bidirectional mappings
- `get_migration_workflow_guide()` - Complete workflow
- `get_migration_phase_guide(phase)` - Phase-specific guides
- `get_shadcn_to_modus_migration_data(component)` - Component migration data

---

## 2. Material UI (MUI) → Modus V2

### Overview
Migrate Material UI React component library to Modus V2 web components.

### Component Coverage
**40+ MUI components** mapped to Modus:
- TextField → modus-wc-text-input
- Button → modus-wc-button
- AppBar → modus-wc-navbar
- Dialog → modus-wc-modal
- Drawer → modus-wc-side-navigation
- And more...

### Key Challenges
1. **Theme System** - MUI theme → Modus design tokens
2. **sx Prop** - Inline styles → Modus props/CSS
3. **Style Overrides** - Theme overrides → Modus custom CSS
4. **Component Variants** - MUI variants → Modus variants

### Example Mappings
```
TextField → modus-wc-text-input
CircularProgress → modus-wc-progress
Snackbar → modus-wc-toast
Rating → modus-wc-rating
Stepper → modus-wc-stepper
```

### Available MCP Tools
- `get_mui_component_mapping()` - Bidirectional mappings
- `get_mui_migration_guide(phase)` - MUI-specific migration guides

---

## 3. Connect UI → Modus V2

### Overview
Migrate Connect UI (Trimble internal UI library) components to Modus V2.

### Component Coverage
**50+ Connect UI components** with detailed migration data:
- Button, CustomInput, CustomSelect, CustomCheckbox
- Accordion, Alert, Cards, Chips, Tabs
- Popup, ConfirmPopup, Rightpanel
- DropDownMenu, Icon, Spinner
- And more...

### Key Challenges
1. **Custom Component Patterns** - Internal patterns → Modus patterns
2. **Internal Dependencies** - Connect-specific features
3. **Event Handler Mapping** - Custom events → Modus events
4. **Slot-Based Composition** - Complex slot structures

### Detailed Migration Data
Each component mapping includes:
- Property mappings (exact transformations)
- Event mappings
- Migration notes and strategies
- Modus components used
- Structural changes required

### Example Detailed Mapping
```json
{
  "CustomInput": {
    "modus_equivalent": "modus-wc-text-input",
    "property_mappings": {
      "label": "label",
      "error": "feedback.message with feedback.level='error'",
      "readonly": "readonly"
    },
    "event_mappings": {
      "onInput": "inputChange event"
    }
  }
}
```

### Available MCP Tools
- `get_connect_ui_component_mapping()` - Comprehensive detailed mappings
- `get_connect_migration_guide(phase)` - Connect-specific guides

---

## 4. Modus V1 → Modus V2

### Overview
Upgrade from Modus V1 web components to Modus V2.

### Component Coverage
**All Modus V1 components** with V2 upgrade paths.

### Key Challenges
1. **Breaking API Changes** - Property/event renames
2. **Deprecated Components** - Components removed in V2
3. **Property Renames** - Updated naming conventions
4. **Event Updates** - New event names/signatures

### Migration Data Includes
- Component mappings (V1 tag → V2 tag)
- Deprecated components list
- Verification rules
- Migration plan

### Example Mappings
```
modus-button → modus-wc-button
modus-alert → modus-wc-alert
modus-modal → modus-wc-modal
modus-accordion-item → Not Found (deprecated)
modus-data-table → Not Found (use new approach)
```

### Available MCP Tools
- `get_modus_v1_to_v2_mapping()` - V1 to V2 mappings
- `get_modus_v1_component_data(component)` - V1 component specs

---

## Common Tools (All Systems)

### Modus V2 Component Data
- `get_modus_component_data(component)` - Get Modus V2 specs
- `list_all_modus_components()` - List all V2 components

### System Overview
- `get_migration_system_overview()` - Overview of all four systems

---

## Migration Workflow (Universal)

All four migration systems follow the same 4-phase workflow:

### Phase 1: Analyze
- Scan codebase
- Identify components
- Assess complexity
- Propose migration strategies

### Phase 2: Migrate
- Transform components
- Apply property mappings
- Convert styles/themes
- Update event handlers

### Phase 3: Verify
- Validate mappings
- Test functionality
- Check best practices
- Review edge cases

### Phase 4: Log
- Generate reports
- Consolidate results
- Create action items
- Document patterns

---

## Data Structure

```
modus-code-generator-migration/
├── shadcn_mcp_server_local.py      # Main MCP server (13 tools)
│
├── shadcn_migration/               # Shadcn migration data
│   ├── mapping/component_mappings.json
│   └── md_prompts/
│       ├── workflow_shadcn.md
│       ├── analyze_shadcn.md
│       ├── migrate_shadcn.md
│       ├── verify_shadcn.md
│       └── log_shadcn.md
│
├── mui_migration/                  # MUI migration data
│   ├── mapping/component_mappings.json
│   └── md_prompts/
│       ├── workflow_mui.md
│       ├── analyze_mui.md
│       ├── migrate_mui.md
│       ├── verify_mui.md
│       └── log_mui.md
│
├── connect_migration/              # Connect UI migration data
│   ├── component_analysis/
│   │   ├── connect_ui_to_modus_mapping.json
│   │   ├── connect_ui_components.json
│   │   └── component_mappings.json
│   └── docs/
│       ├── workflow_connect.md
│       ├── analyze_connect.md
│       ├── migrate_connect.md
│       ├── verify_connect.md
│       └── log_connect.md
│
└── modus_migration/                # Modus V1→V2 and V2 data
    └── component_analysis/
        ├── component_mapping.json   # V1 to V2 mappings
        ├── v1_components.json       # V1 specs
        ├── v2_components.json       # V2 specs
        ├── v1_react_framework_data.json
        └── v2_react_framework_data.json
```

---

## Quick Reference

### Shadcn Migration
```python
# Get shadcn mappings
get_shadcn_component_mapping()

# Get workflow
get_migration_workflow_guide()

# Get specific component migration
get_shadcn_to_modus_migration_data("Button")
```

### MUI Migration
```python
# Get MUI mappings
get_mui_component_mapping()

# Get migration guide
get_mui_migration_guide("migrate")
```

### Connect UI Migration
```python
# Get Connect mappings (detailed)
get_connect_ui_component_mapping()

# Get migration guide
get_connect_migration_guide("analyze")
```

### Modus V1 to V2
```python
# Get V1 to V2 mappings
get_modus_v1_to_v2_mapping()

# Get V1 component data
get_modus_v1_component_data("button")
```

### Common
```python
# Get V2 component specs
get_modus_component_data("button")

# List all V2 components
list_all_modus_components()

# Get overview of all systems
get_migration_system_overview()
```

---

## Statistics

- **Total MCP Tools**: 13
- **Total Components Covered**: 170+
- **Migration Systems**: 4
- **Migration Phases**: 4 per system
- **Lines of Code**: 650+ (server)
- **Documentation Files**: 20+

---

## Benefits

### One Server, All Migrations
- Single MCP server for all UI library migrations
- Consistent workflow across all systems
- Common tools reduce learning curve

### Comprehensive Coverage
- 170+ components mapped
- Detailed migration guidance
- Property/event mappings
- Best practices included

### AI-Powered Assistance
- Works with Claude Desktop, Cursor, etc.
- Intelligent migration suggestions
- Context-aware recommendations

### Production-Ready
- Complete test coverage
- Comprehensive documentation
- Local deployment
- No cloud dependencies

---

## Use Cases

1. **Shadcn Project Migration** - React app using shadcn/ui + Tailwind
2. **MUI Application Upgrade** - Legacy MUI app → modern Modus V2
3. **Connect UI Modernization** - Internal Trimble apps → Modus V2
4. **Modus V1 Maintenance** - Upgrade existing Modus V1 apps to V2
5. **Mixed Library Projects** - Apps using multiple UI libraries

---

## Next Steps

1. **Install**: Follow `SETUP_LOCAL.md`
2. **Configure**: Set up MCP client (Claude, Cursor)
3. **Migrate**: Start with `get_migration_system_overview()`
4. **Verify**: Use phase guides for each migration type

---

**Branch:** master-local  
**Version:** 2.0 (Complete Migration Coverage)  
**Last Updated:** February 2026
