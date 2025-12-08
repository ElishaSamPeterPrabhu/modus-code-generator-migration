# Connect-UI to Modus Migration Analyze Tool

## Purpose
Analyze provided code for Connect-UI components. For each Connect-UI component, identify its Modus web component equivalent and outline the migration approach based on the detected framework (React, SolidJS, or Vanilla JS). This analysis will serve as the blueprint for the migration phase.

## Data Sources

### MCP Tools Available
1. **Mapping Lookup Tool**: Get simple bidirectional mappings
   - Input: "mapping" → Returns `component_mappings.json`
   
2. **Connect Component Details Tool**: Get detailed migration info
   - Input: Component name → Returns complete migration data for that component
   
3. **Modus Documentation Tool**: Get Modus component details
   - Input: Modus component name → Returns Modus properties, events, slots

### JSON Files
- `component_mappings.json`: Simple bidirectional mapping (connect_to_modus + modus_to_connect)
- `connect_ui_to_modus_mapping.json`: Complete detailed mappings (source for Tool 2)
- `connect_ui_components.json`: Connect component catalog with all properties

## Connect UI Styling
Connect-UI components use Trimble Connect design system. To maintain styling during migration:

**Include Connect UI CSS:**
```html
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.11.0/css/style.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800">
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">
```

**After migrating to Modus**, replace with Modus design tokens and CSS.

## Core Analysis Objective
For each source file, produce an `analysis_report.md` detailing:

### Framework Identification
Clearly state the detected framework:
- **SolidJS**: Connect-UI components are built with SolidJS
- **React**: May use Connect-UI via React wrappers
- **Vanilla JS**: Direct web component usage

### Connect-UI Components Found
List each Connect-UI component with:
- Component name (e.g., `Button`, `Alert`, `Spinner`)
- Props used
- Connect-specific patterns (SolidJS reactivity, web component wrappers)

### Proposed Modus Migration Strategy

For each Connect-UI component:

1. **Identify Modus Equivalent**: From `connect_ui_to_modus_mapping.json`
2. **Migration Type**: 
   - `direct`: Simple 1:1 mapping
   - `direct_with_slots`: Uses Modus slots
   - `custom_css_required`: Needs additional CSS
   - `native_html`: Use standard HTML
   - `custom_implementation`: No equivalent, custom needed
   - `not available`: No Modus equivalent

3. **Property Mapping**: Map Connect props to Modus props
4. **Migration Notes**: Follow guidance from mapping JSON

### Special Cases

#### Icon Handling
Connect-UI uses both Connect icons (`tc-icon-*`) and Modus icons:

**For Modus icons:**
```html
<modus-wc-icon name="icon-name" size="md"></modus-wc-icon>
```

**For Connect icons:**
```html
<modus-wc-icon custom-class="icon-font tc-icon-name" name="" size="lg"></modus-wc-icon>
```
*Requires Connect icon font CDN link*

#### Button with Icons
Connect Button has `icon` prop. Modus uses slots:

**Connect:**
```jsx
<Button icon="tc-icon-add" />
```

**Modus:**
```html
<modus-wc-button>
  <modus-wc-icon custom-class="icon-font tc-icon-add" name=""></modus-wc-icon>
</modus-wc-button>
```

#### FAB Button
Connect FabButton needs custom CSS in Modus:

**Migration:**
```html
<modus-wc-button variant="filled" shape="circle" style="position:fixed; bottom:16px; right:16px; z-index:1000;">
  <modus-wc-icon name="add"></modus-wc-icon>
</modus-wc-button>
```

#### Toast/Snackbar
ConnectSnackbar message object maps to modus-wc-toast + modus-wc-alert:

**Connect:**
```jsx
<ConnectSnackbar message={{text: "Success!", type: "success"}} />
```

**Modus:**
```html
<modus-wc-toast delay="5000" position="top-end">
  <modus-wc-alert variant="success" alert-title="Success!"></modus-wc-alert>
</modus-wc-toast>
```

## Analysis Rules & Steps

1. **Load Data**: Parse `connect_ui_to_modus_mapping.json` and `connect_ui_components.json`

2. **For Each File**:
   a. **Framework Detection**: Identify SolidJS, React, or Vanilla JS
   b. **Connect-UI Component Identification**: Find all Connect-UI component usage
   c. **Modus Mapping**: Look up equivalent in mapping JSON
   d. **Property Analysis**: Map each Connect prop to Modus equivalent
   e. **Migration Strategy**: Based on `migration_type` from mapping

3. **Output Generation**:
   - Save as `<original-filename>.connect-analysis.md`
   - Include framework, components found, Modus equivalents
   - List property mappings and migration notes
   - Note any components without equivalents

## Migration Feasibility Levels

- **High**: Direct mapping with clear migration notes
- **Medium**: Requires custom CSS or slot usage
- **Low**: No Modus equivalent, custom implementation needed

## Output Format

```markdown
# Analysis Report for <filename>

**Framework**: SolidJS/React/VanillaJS
**Connect-UI Components Found**: X components

## Component Analysis

### 1. ComponentName

**Connect Component**: ComponentName
**Modus Equivalent**: modus-wc-component
**Migration Type**: direct/custom_css_required/etc
**Feasibility**: High/Medium/Low

**Property Mappings**:
- connectProp → modusProp
- icon → Place <modus-wc-icon> in slot

**Migration Notes**:
[Detailed migration guidance from JSON]

**Connect Styling**:
- Uses Connect CSS classes
- After migration, replace with Modus design tokens
```

## Important Notes

- All Connect-UI components use SolidJS internally
- Connect icons require CDN link
- Maintain Connect CSS during migration, then replace
- Test thoroughly after migration

