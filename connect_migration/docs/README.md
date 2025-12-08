# Connect-UI to Modus Migration Documentation

Complete guide for migrating from Trimble Connect-UI library to Modus Web Components.

## Documentation Files

1. **[workflow_connect.md](workflow_connect.md)** - Complete migration workflow overview
2. **[analyze_connect.md](analyze_connect.md)** - Analysis phase guide
3. **[migrate_connect.md](migrate_connect.md)** - Migration patterns and examples
4. **[verify_connect.md](verify_connect.md)** - Verification checklist
5. **[log_connect.md](log_connect.md)** - Migration logging template

## Quick Start

### 1. Analyze Your Code
```bash
# Run analysis on your Connect-UI code
# See analyze_connect.md for details
```

### 2. Check Component Mappings
**Location**: `../component_analysis/connect_ui_to_modus_mapping.json`

**Key Info**:
- 36 Connect-UI components mapped
- 26 have Modus equivalents
- 10 require custom implementation or native HTML

### 3. Migrate Components
Follow patterns in `migrate_connect.md`:
- Direct migrations
- Slot-based components
- Custom CSS requirements
- Icon handling (Modus + Connect icons)

### 4. Verify Migration
Use checklist in `verify_connect.md`:
- Visual verification
- Functional testing
- Accessibility check
- Cross-browser testing

### 5. Log Progress
Document in `log_connect.md`:
- Components migrated
- Issues encountered
- Decisions made
- Time tracking

## Connect UI Styling

### During Migration (Keep Both)
```html
<!-- Connect CSS (for visual reference) -->
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.11.0/css/style.min.css">
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">

<!-- Modus CSS -->
<!-- Add Modus CSS according to Modus installation guide -->
```

### After Migration
- **Keep Connect icon font** if using Connect icons (tc-icon-*)
- **Remove Connect CSS** if fully migrated to Modus design tokens
- **Or keep both** if mixed icon usage

## Component Status

See `../component_analysis/Connect to Modus components status - Components status.csv`

**Summary**:
- ✅ Complete: 26 components
- 🔧 Native HTML: 2 components  
- ❓ Maybe Modus: 2 components
- ❌ No Equivalent: 6 components

## Migration Patterns

### Most Common (12 components)
**Direct Migration**: Simple 1:1 replacement
- Spinner, CustomInput, CustomCheckbox, etc.

### Common (7 components)
**Direct with Slots**: Use Modus slot system
- Alert, Cards, Accordion, Modal, etc.

### Special Cases
- **FAB Button**: Requires fixed positioning CSS
- **Icons**: Support both Modus and Connect icons
- **Toast**: Requires Alert component as child
- **Empty**: Custom implementation needed

## Resources

### JSON Files
- `connect_ui_to_modus_mapping.json` - Main mapping file
- `connect_ui_components.json` - Component catalog
- `connect_ui_to_modus_status.csv` - Status spreadsheet

### Demo App
- Location: `../connect-ui-demo/`
- Shows 8 components without Modus equivalents
- Runs with full Connect CSS

### External Resources
- [Modus Web Components Docs](https://modus.trimble.com/)
- [Connect UI Resources](https://resources.connect.trimble.com/)
- [Trimble Design System](https://trimble-oss.github.io/website-modus.trimble.com/)

## Getting Help

### Common Questions

**Q: How do I use Connect icons in Modus?**
A: Include CDN link and use custom-class:
```html
<modus-wc-icon custom-class="icon-font tc-icon-name" name=""></modus-wc-icon>
```

**Q: What about components without Modus equivalent?**
A: Check migration_notes in JSON for alternatives or custom implementation guidance.

**Q: Should I remove Connect CSS after migration?**
A: Optional. Keep icon font if using Connect icons. Remove main CSS if using Modus design tokens.

**Q: How to handle form errors?**
A: Use Modus feedback object:
```javascript
.feedback={{level: 'error', message: 'Error text'}}
```

## Next Steps

1. Read `workflow_connect.md` for complete process
2. Review `connect_ui_to_modus_mapping.json` for your components
3. Start with `analyze_connect.md` phase
4. Follow migration patterns in `migrate_connect.md`
5. Verify with `verify_connect.md` checklist
6. Document in `log_connect.md`

