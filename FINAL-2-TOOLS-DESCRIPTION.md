# Final MCP Tools - 2 Tools for Migration

## Tool 1: get_migration_guidance

**Name:** `get_migration_guidance`

**Description:**
```
Fetch migration guidance documents that explain the migration process and best practices.

Available Files (5 markdown documents):
1. analyze - How to analyze V1 code and identify components that need migration
2. migrate - Step-by-step migration process, property transformations, and best practices
3. verify - Verification checklist and testing strategies for migrated code
4. log - Migration logging guidelines and documentation standards
5. workflow - Overall migration workflow and process orchestration

When to Use:
- For migration: Fetch "migrate" to understand the migration process
- For analyzing code: Fetch "analyze" to learn code analysis techniques
- After migration: Fetch "verify" to validate the migrated code
- For documentation: Fetch "log" to learn logging standards
- For overview: Fetch "workflow" to understand the complete process

How to Use:
Pass the file name (without .md extension) as input. Example: {"file_name": "migrate"}
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "file_name": {
      "type": "string",
      "enum": ["analyze", "migrate", "verify", "log", "workflow"],
      "description": "Name of the guidance document to fetch (without .md extension). Options: 'analyze', 'migrate', 'verify', 'log', 'workflow'"
    }
  },
  "required": ["file_name"]
}
```

**GitHub Path:** `md_prompts/{file_name}.md`

**Example Calls:**
```json
// Get migration process guide
{"file_name": "migrate"}

// Get analysis guide
{"file_name": "analyze"}

// Get verification checklist
{"file_name": "verify"}

// Get workflow overview
{"file_name": "workflow"}

// Get logging guidelines
{"file_name": "log"}
```

---

## Tool 2: get_component_details

**Name:** `get_component_details`

**Description:**
```
Fetch component data including mappings, API details, and framework examples for Modus v1 and v2 components.

Available Files (7 JSON files):

1. component_mapping
   - 44 component name mappings (v1 → v2)
   - Property transformation rules (e.g., buttonStyle → variant)
   - Verification rules and migration plan
   Use when: Need to map v1 component names to v2 or transform properties

2. v1_components
   - Complete API details for 43 V1 components
   - Props, events, slots, default values
   - Documentation and storybook examples
   Use when: Need V1 component API details or usage examples

3. v2_components
   - Complete API details for 44 V2 components
   - Props, events, slots, default values
   - Documentation, migration notes, and storybook examples
   Use when: Need V2 component API details or migration guidance

4. v1_angular_framework_data
   - 33 Angular V1 component examples with full code
   - Angular-specific usage patterns and template syntax
   Use when: Migrating Angular applications from V1

5. v1_react_framework_data
   - 34 React V1 component examples with full code
   - JSX usage patterns and React hooks
   Use when: Migrating React applications from V1

6. v2_angular_framework_data
   - Angular V2 framework documentation
   - Integration guidelines for Angular with V2 components
   Use when: Need Angular V2 integration examples

7. v2_react_framework_data
   - 3 React V2 component examples
   - Modern React patterns with V2 components
   Use when: Need React V2 integration examples

How to Use:
Pass the file name (without .json extension) as input. Example: {"file_name": "component_mapping"}
The tool returns the full JSON content. Parse it to extract the specific component or data you need.

Typical Workflow:
1. Fetch "component_mapping" to get v1→v2 mappings
2. Fetch "v2_components" to get target component API details
3. Fetch framework examples if needed for Angular or React
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "file_name": {
      "type": "string",
      "enum": [
        "component_mapping",
        "v1_components",
        "v2_components",
        "v1_angular_framework_data",
        "v1_react_framework_data",
        "v2_angular_framework_data",
        "v2_react_framework_data"
      ],
      "description": "Name of the data file to fetch (without .json extension)"
    }
  },
  "required": ["file_name"]
}
```

**GitHub Path:** `component-analysis/{file_name}.json`

**Example Calls:**
```json
// Get component mappings
{"file_name": "component_mapping"}

// Get all V1 component details
{"file_name": "v1_components"}

// Get all V2 component details
{"file_name": "v2_components"}

// Get Angular V1 examples
{"file_name": "v1_angular_framework_data"}

// Get React V2 examples
{"file_name": "v2_react_framework_data"}
```


---

## Component Lists

### V1 Components (43 total):
```
modus-button, modus-alert, modus-text-input, modus-textarea-input, 
modus-checkbox, modus-radio-group, modus-select, modus-switch, 
modus-slider, modus-date-picker, modus-time-picker, modus-autocomplete, 
modus-breadcrumb, modus-badge, modus-toast, modus-table, modus-modal, 
modus-navbar, modus-side-navigation, modus-tabs, modus-accordion, 
modus-card, modus-chip, modus-pagination, modus-progress-bar, 
modus-spinner, modus-tooltip, modus-dropdown, modus-list, modus-message, 
modus-toolbar, modus-number-input, modus-file-dropzone, modus-data-table, 
modus-content-tree, modus-button-group, modus-utility-panel, 
modus-action-bar, modus-list-item, modus-accordion-item, modus-date-input, 
modus-icons, modus-sentiment-scale
```

### V2 Components (44 total):
```
modus-wc-button, modus-wc-alert, modus-wc-text-input, modus-wc-textarea, 
modus-wc-checkbox, modus-wc-radio, modus-wc-select, modus-wc-switch, 
modus-wc-slider, modus-wc-date, modus-wc-time-input, modus-wc-autocomplete, 
modus-wc-breadcrumbs, modus-wc-badge, modus-wc-toast, modus-wc-table, 
modus-wc-modal, modus-wc-navbar, modus-wc-side-navigation, modus-wc-tabs, 
modus-wc-accordion, modus-wc-card, modus-wc-chip, modus-wc-pagination, 
modus-wc-progress, modus-wc-loader, modus-wc-tooltip, modus-wc-dropdown-menu, 
modus-wc-menu, modus-wc-menu-item, modus-wc-toolbar, modus-wc-number-input, 
modus-wc-icon, modus-wc-avatar, modus-wc-collapse, modus-wc-input-feedback, 
modus-wc-input-label, modus-wc-typography, modus-wc-skeleton, modus-wc-stepper, 
modus-wc-rating, modus-wc-divider, modus-wc-theme-switcher, modus-wc-utility-panel
```

---

## Typical AI Workflow

```
User: "Migrate this V1 code to V2"
<modus-button buttonStyle="primary">Click</modus-button>

AI Agent:
┌──────────────────────────────────────────┐
│ Step 1: Get Migration Process            │
│ Tool: get_migration_guidance             │
│ Input: {"file_name": "migrate"}          │
│ → AI reads migration guide               │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Step 2: Get Component Mappings           │
│ Tool: get_component_details              │
│ Input: {"file_name": "component_mapping"}│
│ → AI learns: modus-button → modus-wc-button│
│ → AI learns: buttonStyle → variant       │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Step 3: Get V2 Component Details         │
│ Tool: get_component_details              │
│ Input: {"file_name": "v2_components"}    │
│ → AI parses JSON for "modus-wc-button"  │
│ → AI learns V2 props, events, slots     │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Step 4: AI Performs Migration            │
│ - Detects: modus-button                  │
│ - Maps to: modus-wc-button               │
│ - Transforms: buttonStyle → variant      │
│ - Adds: aria-label="Click"               │
│ - Generates V2 code                      │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Step 5: Return Migrated Code             │
│ <modus-wc-button variant="primary"       │
│   aria-label="Click">Click              │
│ </modus-wc-button>                       │
└──────────────────────────────────────────┘
```

---

## Summary Table

| Tool | Purpose | Files | Size | Use When |
|------|---------|-------|------|----------|
| **get_migration_guidance** | Migration process docs | 5 markdown files | ~50KB | Need to understand HOW to migrate |
| **get_component_details** | Mappings, component API, examples | 7 JSON files | ~1.8MB | Need mappings, component details, or framework examples |

---

## GitHub Repository Structure

```
ElishaSamPeterPrabhu/modus-document-code/
├── md_prompts/
│   ├── analyze.md
│   ├── migrate.md
│   ├── verify.md
│   ├── log.md
│   └── workflow.md
└── component-analysis/
    ├── component_mapping.json (44 v1→v2 mappings)
    ├── v1_components.json (43 components)
    ├── v2_components.json (44 components)
    ├── v1_angular_framework_data.json (33 examples)
    ├── v1_react_framework_data.json (34 examples)
    ├── v2_angular_framework_data.json (docs)
    └── v2_react_framework_data.json (3 examples)
```

---

## Key Component Mappings (from component_mapping.json)

```json
{
  "modus-button": "modus-wc-button",
  "modus-alert": "modus-wc-alert",
  "modus-text-input": "modus-wc-text-input",
  "modus-textarea-input": "modus-wc-textarea",
  "modus-checkbox": "modus-wc-checkbox",
  "modus-radio-group": "modus-wc-radio",
  "modus-select": "modus-wc-select",
  "modus-switch": "modus-wc-switch",
  "modus-slider": "modus-wc-slider",
  "modus-date-picker": "modus-wc-date",
  "modus-time-picker": "modus-wc-time-input",
  "modus-autocomplete": "modus-wc-autocomplete",
  "modus-breadcrumb": "modus-wc-breadcrumbs",
  "modus-badge": "modus-wc-badge",
  "modus-toast": "modus-wc-toast",
  "modus-table": "modus-wc-table",
  "modus-modal": "modus-wc-modal",
  "modus-navbar": "modus-wc-navbar",
  "modus-side-navigation": "modus-wc-side-navigation",
  "modus-tabs": "modus-wc-tabs",
  "modus-accordion": "modus-wc-accordion",
  "modus-card": "modus-wc-card",
  "modus-chip": "modus-wc-chip",
  "modus-pagination": "modus-wc-pagination",
  "modus-progress-bar": "modus-wc-progress",
  "modus-spinner": "modus-wc-loader",
  "modus-tooltip": "modus-wc-tooltip",
  "modus-list": "modus-wc-menu",
  "modus-list-item": "modus-wc-menu-item",
  "modus-toolbar": "modus-wc-toolbar",
  "modus-number-input": "modus-wc-number-input",
  "modus-utility-panel": "modus-wc-utility-panel"
}
```

---

## Property Mappings (from component_mapping.json)

### modus-button → modus-wc-button
```json
{
  "buttonStyle": "variant",
  "buttonSize": "size",
  "buttonType": "type"
}
```

### modus-alert → modus-wc-alert
```json
{
  "message": "alert-description",
  "button-text": "alert-button-text"
}
```

### modus-text-input → modus-wc-text-input
```json
{
  "inputSize": "size",
  "errorText": "error-text",
  "helperText": "helper-text"
}
```

---

## Total Data Available

- **5 Guidance Documents** (~50KB total)
- **7 Data Files** (~1.8MB total)
- **87 Components Documented** (43 V1 + 44 V2)
- **44 Component Mappings**
- **67 Framework Examples** (33 Angular V1 + 34 React V1 + 3 React V2)

---

This architecture allows the AI to efficiently fetch guidance documents separately from component data, with all component-related information consolidated in one tool!
