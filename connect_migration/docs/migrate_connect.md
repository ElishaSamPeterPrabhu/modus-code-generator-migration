# Connect-UI to Modus Migration Guide

## Purpose
Migrate Connect-UI components to Modus Web Components based on the analysis report.

## Prerequisites
1. Analysis report from `analyze_connect.md`
2. MCP Tools configured:
   - **Tool 1**: Mapping Lookup (quick availability check)
   - **Tool 2**: Connect Component Details (detailed migration info)
   - **Tool 3**: Modus Documentation (Modus component details)
3. Connect CSS loaded (temporarily, for visual verification)
4. Modus Web Components installed

## Using MCP Tools During Migration

### Step 1: Check Availability
```
MCP Tool 1 Input: "mapping"
Output: component_mappings.json
Check: Does component have Modus equivalent?
```

### Step 2: Get Connect Migration Details
```
MCP Tool 2 Input: "ComponentName"
Output: Complete migration data
- Connect properties
- Property mappings
- Migration notes
- Migration type
```

### Step 3: Get Modus Component Info
```
MCP Tool 3 Input: "modus-wc-component-name"
Output: Modus documentation
- Properties, events, slots
- Usage examples
```

## Connect UI Styling During Migration

**Keep Connect CSS temporarily:**
```html
<!-- Keep these during migration for visual reference -->
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.11.0/css/style.min.css">
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">
```

**After migration complete**, remove Connect CSS and use Modus design tokens.

## Migration Patterns by Type

### 1. Direct Migration (`migration_type: "direct"`)

Simple 1:1 component and property mapping.

**Example: Spinner → modus-wc-loader**

Connect:
```jsx
<Spinner show={true} message="Loading..." />
```

Modus:
```html
<modus-wc-loader variant="spinner" size="md" aria-label="Loading...">
</modus-wc-loader>
<!-- Note: Loader doesn't support text, place message separately -->
<modus-wc-typography>Loading...</modus-wc-typography>
```

### 2. Direct with Slots (`migration_type: "direct_with_slots"`)

Component uses Modus slots for content.

**Example: Alert**

Connect:
```jsx
<Alert 
  type="error" 
  content="Error message"
  buttonText="Retry"
  onButtonClick={handleRetry}
/>
```

Modus:
```html
<modus-wc-alert variant="error" alert-description="Error message">
  <modus-wc-button slot="button" color="tertiary" @buttonClick={handleRetry}>
    Retry
  </modus-wc-button>
</modus-wc-alert>
```

### 3. Custom CSS Required (`migration_type: "custom_css_required"`)

Needs additional CSS for styling/positioning.

**Example: FabButton**

Connect:
```jsx
<FabButton icon="tc-icon-add" />
```

Modus:
```html
<modus-wc-button 
  variant="filled" 
  shape="circle"
  style="position:fixed; bottom:16px; right:16px; z-index:1000;"
  aria-label="Add"
>
  <modus-wc-icon custom-class="icon-font tc-icon-add" name=""></modus-wc-icon>
</modus-wc-button>
```

### 4. Direct with Icon Slot (`migration_type: "direct_with_icon_slot"`)

Icons placed in default slot.

**Example: Button**

Connect:
```jsx
<Button icon="tc-icon-settings" type="solid" color="primary">
  Settings
</Button>
```

Modus:
```html
<modus-wc-button variant="filled" color="primary">
  <modus-wc-icon custom-class="icon-font tc-icon-settings" name=""></modus-wc-icon>
  Settings
</modus-wc-button>
```

### 5. Native HTML (`migration_type: "native_html"`)

Use standard HTML elements.

**Example: Image**

Connect:
```jsx
<Image src="photo.jpg" errImg="fallback.jpg" />
```

HTML:
```html
<img src="photo.jpg" onerror="this.src='fallback.jpg'" alt="Photo" />
```

### 6. Custom Implementation (`migration_type: "custom_implementation"`)

No direct equivalent - build custom component.

**Example: Empty**

Connect:
```jsx
<Empty title="No Data" description="No items found" icon="tc-icon-inbox" />
```

Custom Implementation:
```html
<div style="text-align: center; padding: 3rem;">
  <modus-wc-icon custom-class="icon-font tc-icon-inbox" size="lg"></modus-wc-icon>
  <modus-wc-typography variant="h3">No Data</modus-wc-typography>
  <modus-wc-typography>No items found</modus-wc-typography>
</div>
```

## Icon Migration

### Modus Icons (Built-in)
```html
<modus-wc-icon name="alert" variant="solid" size="md"></modus-wc-icon>
<modus-wc-icon name="settings" variant="outlined" size="lg"></modus-wc-icon>
```

### Connect Icons (Require CDN)
```html
<!-- Include Connect icon font -->
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">

<!-- Use with custom-class -->
<modus-wc-icon custom-class="icon-font tc-icon-cloud-queue" name="" size="lg"></modus-wc-icon>
<modus-wc-icon custom-class="icon-font tc-icon-delete" name="" size="md"></modus-wc-icon>
```

**Note**: Set `name=""` (empty) when using Connect icons via `custom-class`.

## Form Components

### Input, Select, Textarea, Checkbox, Switch

All follow similar pattern:
- `error` prop → `feedback.message` with `feedback.level='error'`
- Events: `onChange` → `inputChange`, `onBlur` → `inputBlur`, `onFocus` → `inputFocus`
- Size: `small/medium/large` → `sm/md/lg`
- `id` → `input-id`

**Example: CustomInput**

Connect:
```jsx
<CustomInput 
  label="Name"
  value={name}
  error="Required"
  onChange={handleChange}
/>
```

Modus:
```html
<modus-wc-text-input
  label="Name"
  value={name}
  .feedback={{level: 'error', message: 'Required'}}
  @inputChange={handleChange}
></modus-wc-text-input>
```

## Complex Components

### DropDownMenu → modus-wc-dropdown-menu

Connect:
```jsx
<DropDownMenu
  anchorText="Actions"
  dropDownOptions={['Edit', 'Delete']}
/>
```

Modus:
```html
<modus-wc-dropdown-menu button-aria-label="Actions">
  <div slot="button">Actions</div>
  <div slot="menu">
    <modus-wc-menu-item label="Edit" value="edit"></modus-wc-menu-item>
    <modus-wc-menu-item label="Delete" value="delete"></modus-wc-menu-item>
  </div>
</modus-wc-dropdown-menu>
```

### Rightpanel → modus-wc-utility-panel

Connect:
```jsx
<Rightpanel
  panelVisible={visible}
  headerTitle="Details"
  content={<div>Panel content</div>}
  onClose={handleClose}
/>
```

Modus:
```html
<modus-wc-utility-panel expanded={visible} @panelClosed={handleClose}>
  <div slot="header">Details</div>
  <div slot="body">Panel content</div>
</modus-wc-utility-panel>
```

## Migration Checklist

1. ✅ Identify all Connect-UI components
2. ✅ Look up Modus equivalent in mapping JSON
3. ✅ Check migration_type and follow appropriate pattern
4. ✅ Map all properties using property_mappings
5. ✅ Handle icons (Connect icons need CDN link)
6. ✅ Update event handlers
7. ✅ Test with Connect CSS first
8. ✅ Replace Connect CSS with Modus design tokens
9. ✅ Verify functionality

## Components Without Modus Equivalent

These require custom implementation:
- **AuthImage**: Custom auth image loading
- **LimitVisibleItems**: Custom show more/less logic
- **PanelLayout**: Compose from multiple Modus components
- **Popup**: Use modus-wc-tooltip or custom positioning
- **ProgressWidget**: Combine modus-wc-progress + modus-wc-card
- **RestrictedAccessSplashScreen**: Custom page component
- **TagEditor**: Complex tag management UI

## Testing After Migration

1. Visual comparison with original
2. Functional testing (clicks, inputs, etc.)
3. Accessibility testing
4. Cross-browser verification
5. Replace Connect CSS with Modus tokens
6. Final visual verification

