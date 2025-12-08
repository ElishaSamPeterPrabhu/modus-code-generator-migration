# Connect-UI to Modus Migration Verification

## Purpose
Verify that Connect-UI components have been correctly migrated to Modus Web Components.

## Verification Checklist

### 1. Component Replacement Verification

✅ **Check all Connect-UI components replaced**
- No imports from `@tcweb/connect-ui`
- No `tc-*` web component tags (except icons)
- All replaced with `modus-wc-*` components

### 2. Property Mapping Verification

For each migrated component, verify:

✅ **Direct Properties**
- All Connect props mapped to Modus equivalents
- Size mappings: `icon-small/medium/large` → `sm/md/lg`
- Type mappings: `solid/hollow/outline` → `filled/outlined/borderless`

✅ **Slot Usage**
- Icons placed in correct slots
- Button content in default slots
- Header/body/footer slots used correctly

✅ **Event Handlers**
- `onClick` → `@buttonClick` or `onclick`
- `onChange` → `@inputChange`
- `onBlur` → `@inputBlur`, `onFocus` → `@inputFocus`

### 3. Icon Verification

✅ **Modus Icons**
```html
<modus-wc-icon name="alert" variant="solid" size="md"></modus-wc-icon>
```

✅ **Connect Icons**
- CDN link present in HTML
- Using `custom-class="icon-font tc-icon-*"`
- `name=""` (empty when using custom-class)

```html
<link rel="stylesheet" href="https://resources.connect.trimble.com/1.12.0/fonts/icon-font.min.css">
<modus-wc-icon custom-class="icon-font tc-icon-add" name="" size="lg"></modus-wc-icon>
```

### 4. Styling Verification

✅ **During Migration (Temporary)**
- Connect CSS still loaded for reference
- Visual appearance matches original

✅ **After Migration Complete**
- Connect CSS removed
- Modus design tokens applied
- Custom CSS for special cases (FAB positioning, etc.)

### 5. Form Component Verification

✅ **Error Handling**
```html
<!-- Verify error prop converted to feedback -->
<modus-wc-text-input
  .feedback={{level: 'error', message: 'Error message'}}
></modus-wc-text-input>
```

✅ **Value Binding**
- Checkbox/Switch: `checked` → `value`
- All inputs: controlled component pattern

### 6. Complex Component Verification

✅ **Dropdown Menu**
- Button slot has trigger content
- Menu slot has menu-item children
- Menu visibility controlled via `menu-visible`

✅ **Utility Panel (Rightpanel)**
- `panelVisible` → `expanded`
- Header/body/footer slots populated
- Panel closes properly

✅ **Toast (ConnectSnackbar)**
- Alert component inside toast
- Correct variant (success/error/warning)
- Auto-dismiss timing works

✅ **Modal (DeleteConfirmationModal, ConfirmPopup)**
- Header/content/footer slots
- Modal ID set
- showModal()/close() methods work

### 7. Custom Implementation Verification

For components without Modus equivalents:

✅ **Empty State**
- Centered layout
- Icon + typography components
- Maintains visual appearance

✅ **Image**
- Standard `<img>` tag
- Error handling with `onerror`
- Styling preserved

### 8. Accessibility Verification

✅ **ARIA Labels**
- All icon-only buttons have `aria-label`
- Form inputs properly labeled
- Modal/dialog roles correct

✅ **Keyboard Navigation**
- Tab order correct
- Enter/Space activate buttons
- Escape closes modals/tooltips

✅ **Screen Reader**
- Decorative icons have `decorative="true"`
- Meaningful icons have `aria-label`
- Form errors announced

## Testing Scenarios

### Functional Testing
1. **Buttons**: Click events fire correctly
2. **Forms**: Input, validation, submission work
3. **Modals**: Open, close, backdrop behavior
4. **Dropdowns**: Open menu, select item, close
5. **Tabs**: Switch tabs, content updates
6. **Toast**: Appears, auto-dismisses
7. **Tooltips**: Show on hover, position correctly

### Visual Testing
1. Component sizing matches
2. Colors/variants correct
3. Icons display properly (both Modus and Connect)
4. Layout/spacing maintained
5. Responsive behavior works

### Browser Testing
- Chrome
- Firefox
- Safari
- Edge

## Common Issues & Solutions

### Issue: Icons not showing
**Solution**: 
- For Modus icons: Check icon name is correct
- For Connect icons: Verify CDN link is included

### Issue: FAB button not positioned
**Solution**: Add CSS:
```css
position: fixed;
bottom: 16px;
right: 16px;
z-index: 1000;
```

### Issue: Form errors not displaying
**Solution**: Use feedback object:
```javascript
.feedback={{level: 'error', message: 'Error text'}}
```

### Issue: Dropdown menu items not showing
**Solution**: Place menu-items in menu slot:
```html
<div slot="menu">
  <modus-wc-menu-item label="Item" value="1"></modus-wc-menu-item>
</div>
```

## Final Verification Steps

1. ✅ All Connect-UI components removed
2. ✅ All Modus components working
3. ✅ Icons displaying (Modus + Connect)
4. ✅ Events firing correctly
5. ✅ Forms submitting/validating
6. ✅ Styling matches original
7. ✅ Accessibility passes
8. ✅ Cross-browser tested
9. ✅ Connect CSS removed (optional)
10. ✅ Modus design tokens applied

## Sign-off

Migration complete when:
- ✅ All verification items passed
- ✅ No Connect-UI dependencies remain
- ✅ Visual/functional parity achieved
- ✅ Code review approved

