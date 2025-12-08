# Connect-UI to Modus Migration Workflow

## Overview
Complete workflow for migrating from Connect-UI library to Modus Web Components.

## Migration Phases

### Phase 1: Analyze
**Tool**: `analyze_connect.md`

**Steps**:
1. Identify framework (SolidJS/React/Vanilla JS)
2. Find all Connect-UI component usage
3. Look up Modus equivalents in mapping JSON
4. Generate analysis report with migration strategy
5. Review feasibility and potential issues

**Output**: `<filename>.connect-analysis.md`

### Phase 2: Migrate
**Tool**: `migrate_connect.md`

**Steps**:
1. Load Connect CSS (temporary, for visual reference)
2. Replace Connect-UI components with Modus equivalents
3. Map properties according to migration notes
4. Handle icons (Modus icons + Connect icons via CDN)
5. Update event handlers
6. Add custom CSS where needed (FAB, etc.)
7. Test functionality

**Output**: Updated source files with Modus components

### Phase 3: Verify
**Tool**: `verify_connect.md`

**Steps**:
1. Visual comparison with original
2. Functional testing (all interactions)
3. Verify icons display (both types)
4. Check accessibility (ARIA, keyboard, screen reader)
5. Cross-browser testing
6. Performance check

**Output**: Verification report

### Phase 4: Finalize
**Steps**:
1. Remove Connect CSS (optional - can keep for Connect icons)
2. Apply Modus design tokens for spacing/colors
3. Code review
4. Documentation update
5. Deployment

## Quick Reference

### Component Count
- **36 total** Connect-UI components
- **26 have** Modus equivalents
- **10 no equivalent** (custom implementation or native HTML)

### Migration Types
- `direct`: 12 components - Simple replacement
- `direct_with_slots`: 7 components - Use Modus slots
- `custom_css_required`: 2 components - Need positioning/styling
- `direct_with_icon_slot`: 1 component - Icons in slots
- `custom_implementation`: 1 component - Build custom
- `native_html`: 2 components - Use HTML tags
- `use_modal`: 1 component - Use modal alternative

### Critical Notes

#### Connect Icons
**Must include CDN link:**
```html
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">
```

**Usage:**
```html
<modus-wc-icon custom-class="icon-font tc-icon-name" name=""></modus-wc-icon>
```

#### Connect CSS
**During migration:**
```html
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.11.0/css/style.min.css">
```

**After migration:** Can remove if not using Connect icons, otherwise keep icon font CDN only.

## Tools & Resources

### MCP Tools (Three Complementary Tools)

**Tool 1: Mapping Lookup**
- Input: `"mapping"` → Quick bidirectional lookup
- Input: Process name → Workflow docs
- Fast availability check

**Tool 2: Connect Component Details** ⭐ NEW
- Input: Component name (e.g., "Button")
- Output: Complete migration info for that Connect component
- Includes: properties, mappings, migration notes, migration type

**Tool 3: Modus Documentation** (Existing Modus MCP)
- Input: Modus component name (e.g., "modus-wc-button")
- Output: Modus properties, events, slots, examples
- Official Modus documentation

### JSON Files
- `component_mappings.json`: Simple bidirectional mapping
- `connect_ui_to_modus_mapping.json`: Detailed migration info (source for Tool 2)
- `connect_ui_components.json`: Connect component catalog
- `connect_ui_to_modus_status.csv`: Migration status spreadsheet

### Documentation
- `analyze_connect.md`: Analysis phase guide
- `migrate_connect.md`: Migration patterns and examples
- `verify_connect.md`: Verification checklist
- `workflow_connect.md`: This document

### Demo
- Live demo at: `connect_migration/connect-ui-demo/`
- Shows 8 components without Modus equivalents
- URL: http://localhost:3000/ (when running)

## Migration Timeline (Estimate)

- **Small project** (< 10 components): 1-2 days
- **Medium project** (10-30 components): 3-5 days
- **Large project** (30+ components): 1-2 weeks

Add time for:
- Custom implementations
- Extensive testing
- Styling adjustments
- Team review

## Success Criteria

✅ All Connect-UI components migrated or replaced
✅ Visual parity achieved
✅ Functional parity achieved
✅ All tests passing
✅ Accessibility maintained
✅ Code reviewed and approved
✅ Documentation updated

