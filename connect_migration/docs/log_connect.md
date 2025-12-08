# Connect-UI to Modus Migration Logging

## Purpose
Document the migration process, decisions made, and issues encountered.

## Log Structure

### Migration Log Entry Template

```markdown
## [Component Name] - [Date]

### Source
- File: `path/to/file`
- Connect Component: `ComponentName`
- Props: `{prop1, prop2, ...}`

### Target
- Modus Component: `modus-wc-component`
- Migration Type: `direct/custom_css_required/etc`

### Changes Made
1. Replaced component tag
2. Mapped properties
3. Updated event handlers
4. Added custom CSS (if applicable)

### Issues Encountered
- Issue description
- Solution applied

### Testing
- ✅ Visual: Matches original
- ✅ Functional: Works as expected
- ✅ Accessibility: ARIA labels correct

### Notes
- Any special considerations
- Future improvements needed
```

## Example Logs

### Example 1: Spinner Migration

```markdown
## Spinner → modus-wc-loader - 2024-12-08

### Source
- File: `src/components/LoadingState.tsx`
- Connect: `<Spinner show={loading} message="Loading..." />`

### Target
- Modus: `modus-wc-loader`
- Type: `direct`

### Changes
1. Component: `Spinner` → `modus-wc-loader`
2. Props:
   - `show` → Conditional rendering
   - `message` → Separate typography (loader has no text prop)
3. Added: `variant="spinner"` `size="md"`

### Code
Before:
```jsx
<Spinner show={loading} message="Loading data..." />
```

After:
```html
{loading && (
  <>
    <modus-wc-loader variant="spinner" size="md"></modus-wc-loader>
    <modus-wc-typography>Loading data...</modus-wc-typography>
  </>
)}
```

### Testing
- ✅ Visual: Spinner animates correctly
- ✅ Functional: Shows/hides based on loading state
- ✅ Message displays below spinner

### Notes
- Loader component doesn't support text property
- Placed message separately for better flexibility
```

### Example 2: Button with Icon

```markdown
## Button → modus-wc-button - 2024-12-08

### Source
- File: `src/components/Toolbar.tsx`
- Connect: `<Button icon="tc-icon-delete" color="danger">Delete</Button>`

### Target
- Modus: `modus-wc-button`
- Type: `direct_with_icon_slot`

### Changes
1. Component tag replaced
2. Props:
   - `icon` → Place icon in default slot
   - `color="danger"` → `color="danger"`
3. Added Connect icon CDN link
4. Placed icon before text in slot

### Code
Before:
```jsx
<Button icon="tc-icon-delete" color="danger">Delete</Button>
```

After:
```html
<!-- In HTML head -->
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">

<!-- In component -->
<modus-wc-button color="danger" variant="filled">
  <modus-wc-icon custom-class="icon-font tc-icon-delete" name="" size="sm"></modus-wc-icon>
  Delete
</modus-wc-button>
```

### Testing
- ✅ Visual: Icon shows before text
- ✅ Functional: Click event works
- ✅ Icon: Connect icon displays correctly

### Notes
- Required Connect icon font CDN
- Icon placed before text in default slot
```

## Component Migration Summary Log

### Components Migrated

| Component | Modus Equivalent | Status | Date | Developer |
|-----------|-----------------|--------|------|-----------|
| Spinner | modus-wc-loader | ✅ Complete | 2024-12-08 | Name |
| Button | modus-wc-button | ✅ Complete | 2024-12-08 | Name |
| Alert | modus-wc-alert | ✅ Complete | 2024-12-08 | Name |

### Components Pending

| Component | Reason | Expected Date |
|-----------|--------|---------------|
| TagEditor | No equivalent - needs design | TBD |

## Issues Log

### Issue #1: Connect Icons Not Displaying
**Date**: 2024-12-08
**Component**: All icon usage
**Problem**: Connect icons (tc-icon-*) not rendering
**Solution**: Added CDN link to HTML head:
```html
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">
```
**Status**: ✅ Resolved

### Issue #2: FAB Button Positioning
**Date**: 2024-12-08
**Component**: FabButton
**Problem**: Button not floating in bottom-right
**Solution**: Added inline style:
```html
style="position:fixed; bottom:16px; right:16px; z-index:1000;"
```
**Status**: ✅ Resolved

## Decisions Log

### Decision #1: Keep Connect Icon Font
**Date**: 2024-12-08
**Context**: Many components use Connect icons (tc-icon-*)
**Decision**: Keep Connect icon font CDN link even after migration
**Rationale**: Easier than converting all icons to Modus equivalents
**Impact**: Small external dependency, minimal performance impact

### Decision #2: Error Handling Pattern
**Date**: 2024-12-08
**Context**: All form inputs need error display
**Decision**: Use Modus feedback object pattern
**Pattern**:
```javascript
.feedback={{level: 'error', message: 'Error text'}}
```
**Rationale**: Consistent with Modus design system
**Impact**: All form components follow same pattern

## Statistics

### Migration Progress
- Total Components: 36
- Migrated: 0/36 (Update as you go)
- In Progress: 0
- Pending: 36

### Lines Changed
- Added: 0
- Removed: 0
- Modified: 0

### Time Spent
- Analysis: 0 hours
- Migration: 0 hours
- Testing: 0 hours
- Total: 0 hours

## Notes for Future Migrations

1. **Start with simple components** (Spinner, Button, Alert)
2. **Test incrementally** - don't migrate everything at once
3. **Keep Connect CSS** during migration for visual comparison
4. **Document custom implementations** for components without equivalents
5. **Icon strategy upfront** - decide Modus vs Connect icons early
6. **Form pattern first** - establish error handling pattern early

