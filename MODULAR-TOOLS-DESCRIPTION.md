# Modus Migration MCP Tools - Modular Structure

## Overview

The component data has been reorganized into a modular structure for better performance and maintainability:

- **Before**: 2 large JSON files (811KB + 825KB = 1.6MB)
- **After**: 89 individual component files (avg 15-20KB each)

**Benefits**:
- Faster GitHub API retrieval (fetch only what you need)
- Lower n8n workflow memory usage
- Better data organization
- Easier maintenance

---

## Tool 1: get_migration_guidance

**Name:** `get_migration_guidance`

**Description:**
```
Fetch migration guidance documents that explain the migration process and best practices.

Available Files (5 markdown documents):
1. analyze - How to analyze V1 code and identify components
2. migrate - Migration process, property transformations, best practices
3. verify - Verification checklist and testing strategies
4. log - Logging guidelines and documentation standards
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
      "description": "Guidance document name (without .md extension)"
    }
  },
  "required": ["file_name"]
}
```

**GitHub Path:** `modus_migration/component_analysis/md_prompts/{file_name}.md`

---

## Tool 2: get_component_index

**Name:** `get_component_index`

**Description:**
```
Fetch the component index for V1 or V2 components. The index lists all available components with metadata.

Available Files (2 index files):
1. v1_index - Index of 43 V1 components with props/events/slots counts
2. v2_index - Index of 44 V2 components with props/events/slots counts

Each index contains:
- Total component count
- List of all components with:
  - File name (e.g., "button.json")
  - Component tag name (e.g., "modus-wc-button")
  - Props count
  - Events count
  - Slots count

When to Use:
- Start of migration: Fetch index to see all available components
- Before fetching details: Check if component exists
- For component discovery: Browse available components

How to Use:
Pass "v1" or "v2" to get the respective index. Example: {"version": "v2"}
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "enum": ["v1", "v2"],
      "description": "Component version to fetch index for"
    }
  },
  "required": ["version"]
}
```

**GitHub Paths:**
- V1: `modus_migration/component_analysis/v1_components/_index.json`
- V2: `modus_migration/component_analysis/v2_components/_index.json`

---

## Tool 3: get_component_data

**Name:** `get_component_data`

**Description:**
```
Fetch detailed data for a specific component. Returns complete API details including props, events, slots, documentation, and examples.

Input Parameters:
- version: "v1" or "v2" (which version)
- component_name: Clean component name without prefix (e.g., "button", not "modus-button" or "modus-wc-button")

Component Data Includes:
- component_name: Full tag name (e.g., "modus-wc-button")
- version: "v1" or "v2"
- props: Array of prop objects (name, type, description, default values)
- events: Array of event objects (name, description)
- slots: Array of slot names
- documentation: Component usage guide and migration notes
- storybook: Examples, variants, and prop usage patterns
- tag_name: HTML tag name

When to Use:
- After checking index: Fetch specific component details
- During migration: Get V1 and V2 component APIs for comparison
- For code generation: Get exact prop names, types, and defaults

How to Use:
Pass version and component name. 
Example: {"version": "v2", "component_name": "button"}
This fetches: component-analysis/v2_components/button.json

File sizes: 5-120KB per component (vs 811KB-825KB for full file)
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "enum": ["v1", "v2"],
      "description": "Component version: 'v1' for modus-* components, 'v2' for modus-wc-* components"
    },
    "component_name": {
      "type": "string",
      "description": "Clean component name without prefix. Examples: 'button', 'alert', 'text-input' (NOT 'modus-button' or 'modus-wc-button')"
    }
  },
  "required": ["version", "component_name"]
}
```

**GitHub Paths:**
- V1: `modus_migration/component_analysis/v1_components/{component_name}.json`
- V2: `modus_migration/component_analysis/v2_components/{component_name}.json`

**Example Calls:**
```json
// Get V2 button component
{"version": "v2", "component_name": "button"}

// Get V1 alert component
{"version": "v1", "component_name": "alert"}

// Get V2 text-input component
{"version": "v2", "component_name": "text-input"}

// Get V1 textarea component
{"version": "v1", "component_name": "textarea-input"}
```

---

## Tool 4: get_component_mapping

**Name:** `get_component_mapping`

**Description:**
```
Fetch the component mapping file containing v1→v2 mappings and property transformation rules.

Content:
- 44 component name mappings (modus-button → modus-wc-button)
- Property transformation rules (buttonStyle → variant)
- Verification rules
- Migration plan

When to Use:
- Start of migration: Get v1→v2 component mappings
- Property transformation: Look up prop name changes
- Validation: Check migration rules

How to Use:
No parameters needed. Returns the complete mapping file.
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

**GitHub Path:** `modus_migration/component_analysis/component_mapping.json`

---

## Tool 5: get_framework_data

**Name:** `get_framework_data`

**Description:**
```
Fetch framework-specific examples and documentation for Angular or React.

Available Files (4 framework files):
1. v1_angular - 33 Angular V1 component examples with full code
2. v1_react - 34 React V1 component examples with full code
3. v2_angular - Angular V2 framework documentation
4. v2_react - 3 React V2 component examples

When to Use:
- Migrating Angular apps: Fetch v1_angular and v2_angular
- Migrating React apps: Fetch v1_react and v2_react
- Framework integration: Get framework-specific patterns

How to Use:
Pass version and framework.
Example: {"version": "v2", "framework": "react"}
```

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "enum": ["v1", "v2"],
      "description": "Component version"
    },
    "framework": {
      "type": "string",
      "enum": ["angular", "react"],
      "description": "Framework type"
    }
  },
  "required": ["version", "framework"]
}
```

**GitHub Path:** `modus_migration/component_analysis/{version}_{framework}_framework_data.json`

---

## Typical AI Workflow (Updated for Modular Structure)

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
│ Tool: get_component_mapping              │
│ Input: {}                                │
│ → AI learns: modus-button → modus-wc-button│
│ → AI learns: buttonStyle → variant       │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│ Step 3: Get V2 Component Details         │
│ Tool: get_component_data                 │
│ Input: {                                 │
│   "version": "v2",                       │
│   "component_name": "button"             │
│ }                                        │
│ → Fetches only button.json (14KB)       │
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

## Component Name Mapping Table

| V1 Component | Clean Name | V2 Component |
|--------------|------------|--------------|
| modus-button | button | modus-wc-button |
| modus-alert | alert | modus-wc-alert |
| modus-text-input | text-input | modus-wc-text-input |
| modus-textarea-input | textarea-input | modus-wc-textarea |
| modus-checkbox | checkbox | modus-wc-checkbox |
| modus-radio-group | radio-group | modus-wc-radio |
| modus-select | select | modus-wc-select |
| modus-switch | switch | modus-wc-switch |
| modus-slider | slider | modus-wc-slider |
| modus-date-picker | date-picker | modus-wc-date |
| modus-time-picker | time-picker | modus-wc-time-input |
| modus-autocomplete | autocomplete | modus-wc-autocomplete |
| modus-breadcrumb | breadcrumb | modus-wc-breadcrumbs |
| modus-badge | badge | modus-wc-badge |
| modus-toast | toast | modus-wc-toast |
| modus-table | table | modus-wc-table |
| modus-modal | modal | modus-wc-modal |
| modus-navbar | navbar | modus-wc-navbar |
| modus-side-navigation | side-navigation | modus-wc-side-navigation |
| modus-tabs | tabs | modus-wc-tabs |
| modus-accordion | accordion | modus-wc-accordion |
| modus-card | card | modus-wc-card |
| modus-chip | chip | modus-wc-chip |
| modus-pagination | pagination | modus-wc-pagination |
| modus-progress-bar | progress-bar | modus-wc-progress |
| modus-spinner | spinner | modus-wc-loader |
| modus-tooltip | tooltip | modus-wc-tooltip |
| modus-list | list | modus-wc-menu |
| modus-list-item | list-item | modus-wc-menu-item |
| modus-toolbar | toolbar | modus-wc-toolbar |
| modus-number-input | number-input | modus-wc-number-input |

---

## Summary Table

| Tool | Purpose | Input | GitHub Path | Size |
|------|---------|-------|-------------|------|
| **get_migration_guidance** | Migration docs | file_name | md_prompts/{file_name}.md | ~10KB |
| **get_component_index** | Component list | version | {version}_components/_index.json | ~7KB |
| **get_component_data** | Component API | version, component_name | {version}_components/{component_name}.json | 5-120KB |
| **get_component_mapping** | v1→v2 mappings | (none) | component_mapping.json | 11KB |
| **get_framework_data** | Framework examples | version, framework | {version}_{framework}_framework_data.json | 10-80KB |

---

## Performance Improvements

**Before Modular Structure**:
- Fetch v2_components.json: 825KB
- Parse entire JSON to find one component
- High memory usage in n8n workflows

**After Modular Structure**:
- Fetch button.json: 14KB (59x smaller!)
- No parsing needed - file contains only what you need
- Low memory usage, faster retrieval

**Example**:
- Old: Fetch 825KB to get button component
- New: Fetch 14KB to get button component
- **Improvement: 98% reduction in data transfer**

---

## Directory Structure

```
modus_migration/component_analysis/
├── v1_components/
│   ├── _index.json (7KB) - List of all 43 v1 components
│   ├── button.json (21KB)
│   ├── alert.json (11KB)
│   ├── text-input.json (61KB)
│   └── ... (43 total components)
├── v2_components/
│   ├── _index.json (7KB) - List of all 44 v2 components
│   ├── button.json (14KB)
│   ├── alert.json (10KB)
│   ├── text-input.json (42KB)
│   └── ... (44 total components)
├── component_mapping.json (11KB)
├── v1_angular_framework_data.json (80KB)
├── v1_react_framework_data.json (43KB)
├── v2_angular_framework_data.json (10KB)
└── v2_react_framework_data.json (9KB)
```

---

## Migration from Old Structure

**Backwards Compatibility**:
- Old files (v1_components.json, v2_components.json) still exist
- Can be deprecated after tools are updated
- Gradual migration path

**Next Steps**:
1. ✅ Split component files
2. ✅ Create index files
3. Update n8n workflows to use new structure
4. Update component_extractor.py to save modular files
5. Test GitHub API retrieval with smaller files

---

This modular structure follows best practices from projects like FigmaToCode and improves data management, performance, and maintainability!

