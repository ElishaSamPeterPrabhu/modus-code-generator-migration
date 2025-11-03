# MUI to Modus Migration Verification Tool

## Purpose
Verify the correctness and completeness of the MUI to Modus migration performed by `migrate_mui.md`. This tool validates that the migrated code maintains functionality, follows Modus best practices, and properly handles all edge cases.

## Data Sources
- **Original Source File**: The original MUI implementation
- **Migrated File**: The `.migrated.[ext]` file from migrate phase
- **Analysis Report**: The `.mui-analysis.md` file
- **Migration Log**: The `migration.log` from migrate phase
- `mui_to_modus_mapping.json`: For reference
- `v2_components.json`: Modus component specifications
- `gold_standard.md`: Best practices and patterns for Modus V2

## Verification Checklist

### 1. Import Verification
- [ ] All MUI imports removed
- [ ] Modus web components loader imported (if React/Angular)
- [ ] `defineCustomElements()` called appropriately
- [ ] No orphaned MUI dependencies

### 2. Component Migration Verification

For each migrated component, verify:

#### Structural Integrity
- [ ] Modus component tag name is correct
- [ ] Component hierarchy preserved
- [ ] Parent-child relationships maintained
- [ ] Slotted content properly placed

#### Property Validation
- [ ] All critical props migrated or addressed
- [ ] Property values correctly transformed
- [ ] Boolean props handled correctly (presence vs value)
- [ ] Required props not missing

#### Event Handling
- [ ] Event listeners properly attached
- [ ] Event names correctly mapped
- [ ] Event handlers receive correct parameters
- [ ] No broken event chains

### 3. Special Pattern Verification

#### Icons
- [ ] MUI icon components replaced with `modus-wc-icon`
- [ ] Icon names correctly mapped
- [ ] Icon positioning preserved

#### Forms
- [ ] Form structure follows Modus patterns
- [ ] Labels properly associated with inputs
- [ ] Error states correctly implemented
- [ ] Helper text appropriately placed

#### Layout
- [ ] Grid/Box/Stack replaced with appropriate CSS
- [ ] Responsive behavior maintained
- [ ] Spacing follows Modus design system

### 4. Style and Theme Verification
- [ ] sx props converted to valid CSS
- [ ] Theme colors mapped to Modus tokens
- [ ] Custom styles preserved where appropriate
- [ ] No MUI-specific CSS classes remaining

### 5. Functionality Preservation
- [ ] User interactions work as expected
- [ ] Form validations still function
- [ ] State management unaffected
- [ ] API integrations maintained

## Verification Process

### Automated Checks

1. **Syntax Validation**:
   - Valid JSX/TSX/HTML syntax
   - No undefined components
   - Proper attribute naming (kebab-case for web components)

2. **Component Existence**:
   ```javascript
   // Verify all Modus components exist in v2_components.json
   const usedComponents = extractModusComponents(migratedFile);
   const invalidComponents = usedComponents.filter(comp => 
     !v2Components.includes(comp)
   );
   ```

3. **Property Validation**:
   - Check props against component specifications
   - Flag unknown or deprecated props
   - Verify required props are present

4. **Pattern Detection**:
   - Identify incomplete migrations
   - Find TODO comments
   - Detect potential anti-patterns

### Manual Review Items

Flag for manual review:
- Complex event handler transformations
- Custom styling requirements
- Accessibility implications
- Performance considerations
- Framework-specific integrations

## Verification Report Format

```markdown
# MUI to Modus Migration Verification Report
**Source File**: [filename]
**Migration Date**: [date]
**Verification Status**: [PASSED with warnings | FAILED | REQUIRES REVIEW]

## Summary
- Total Components Migrated: X
- Successful Migrations: Y
- Issues Found: Z

## Component Verification

### ✅ Successful Migrations
1. **Button (Line 45)**
   - Correctly mapped to modus-wc-button
   - All props validated
   - Events properly connected

### ⚠️ Warnings
1. **TextField (Line 75)**
   - Manual review needed for custom validation
   - Helper text positioning may need CSS adjustment

### ❌ Failed Migrations
1. **DataGrid (Line 120)**
   - No Modus equivalent
   - Requires custom implementation

## Style Verification
- Theme migration: [COMPLETE | PARTIAL | FAILED]
- CSS conversion: [Valid | Issues found]

## Functionality Tests
- [ ] Form submission works
- [ ] Validation triggers correctly
- [ ] Modal opens/closes properly

## Recommendations
1. Review and test custom event handlers
2. Verify responsive behavior
3. Check accessibility compliance

## Code Quality
- ESLint/TSLint compliance: [PASSED | X issues]
- Best practices adherence: [Score]
```

## Gold Standard Compliance

Verify against Modus best practices:
1. **Component Usage**:
   - Using semantic HTML where appropriate
   - Proper ARIA attributes
   - Keyboard navigation support

2. **Performance**:
   - No unnecessary re-renders
   - Efficient event delegation
   - Optimized bundle size

3. **Maintainability**:
   - Clear component structure
   - Consistent naming conventions
   - Adequate documentation

## Output

Save verification report as:
- `[original_filename].verification.md`
- In `verification_reports/mui/` directory structure

Include:
- Detailed verification results
- Action items for developers
- Risk assessment
- Migration confidence score
