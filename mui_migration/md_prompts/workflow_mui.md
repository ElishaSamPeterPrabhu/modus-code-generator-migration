# MUI to Modus Component Migration Workflow

## Overview
This document outlines the end-to-end workflow for migrating Material-UI (MUI) v7 components to Modus V2 components within a codebase. The process follows the same phase structure as Modus V1 migration but with MUI-specific considerations.

## Phase 1: Analyze

*   **Objective**: Examine source code, identify MUI components, determine framework context, and propose Modus V2 migration strategies.
*   **Key Differences from V1 Migration**:
    *   MUI components are typically PascalCase in JSX/TSX
    *   Need to handle MUI imports and theme usage
    *   Must address sx prop and styled components
    *   Icon library migration required
*   **Agent Action**:
    1.  **Primary**: Call MUI analysis tool with `analyze_mui.md` guidance
    2.  Use `mui_to_modus_mapping.json` for component mapping
    3.  Reference `mui_v7_components.json` for MUI specifications
*   **Key Outputs**:
    *   `[filename].mui-analysis.md` in `analysis_reports/mui/` directory
    *   Identified MUI components with confidence levels
    *   Property mapping strategies
    *   Structural changes required
*   **User Prompt**: "MUI analysis complete. Review reports and reply 'proceed to migrate' or specify changes."

## Phase 2: Migrate

*   **Objective**: Transform MUI components to Modus V2 based on analysis.
*   **Special Considerations**:
    *   Import statement transformation
    *   JSX syntax adaptation for web components
    *   Event handler updates
    *   Style system migration
    *   Icon component replacement
*   **Agent Action**:
    1.  Execute migration using `migrate_mui.md` guidance
    2.  Apply component and property mappings
    3.  Handle special patterns (forms, icons, layouts)
*   **Key Outputs**:
    *   `[filename].migrated.[ext]` files
    *   `migration.log` with detailed transformation record
    *   TODO comments for manual review items
*   **User Prompt**: "MUI migration complete. Review migrated files and logs. Reply 'proceed to verify' or specify changes."

## Phase 3: Verify

*   **Objective**: Ensure migrated code is correct and follows Modus best practices.
*   **Verification Focus**:
    *   Web component integration in React/Angular
    *   Event handling correctness
    *   Style migration completeness
    *   Functionality preservation
    *   No remaining MUI dependencies
*   **Agent Action**:
    1.  Run verification using `verify_mui.md` guidance
    2.  Check component validity against `v2_components.json`
    3.  Validate patterns against gold standard
*   **Key Outputs**:
    *   `[filename].verification.md` reports
    *   Pass/fail status with detailed findings
    *   Manual review recommendations
*   **User Prompt**: "Verification complete. Review reports. Reply 'finish' or 'log results' or specify changes."

## Phase 4: Log

*   **Objective**: Consolidate all migration artifacts and provide actionable insights.
*   **Aggregation includes**:
    *   Component migration statistics
    *   Success rates by component type
    *   Common patterns and issues
    *   Framework-specific findings
*   **Agent Action**:
    1.  Consolidate using `log_mui.md` guidance
    2.  Generate summary statistics
    3.  Create action item lists
*   **Key Outputs**:
    *   `overall_migration_summary.md`
    *   `action_items.md`
    *   `migration_metrics.json`
*   **User Prompt**: "MUI migration process complete. Summary and action items available."

## Key Differences from Modus V1 Migration

### Component Identification
- **V1**: Look for `modus-*` tags
- **MUI**: Look for PascalCase components and MUI imports

### Mapping Complexity
- **V1**: Usually 1:1 mapping to V2
- **MUI**: May require structural changes, no equivalent for some components

### Framework Integration
- **V1**: Already web components
- **MUI**: React components need conversion to web component usage

### Styling System
- **V1**: Basic CSS/attributes
- **MUI**: Complex theme system, sx prop, styled components

### Common Challenges

1. **No Direct Mappings**:
   - Layout components (Grid, Box, Stack)
   - Typography component
   - Transition/animation components
   - Form helper components

2. **Structural Changes**:
   - TextField → Input + Label + Feedback
   - Icon components → modus-wc-icon with name mapping
   - Composite components need decomposition

3. **Event Handling**:
   - Synthetic events → Native events
   - Event name changes
   - Parameter differences

4. **Theme Migration**:
   - MUI theme → Modus design tokens
   - Dynamic styles → CSS classes
   - Responsive helpers → Media queries

## Migration Readiness Checklist

Before starting:
- [ ] Inventory MUI components used
- [ ] Review available Modus components
- [ ] Plan for no-mapping components
- [ ] Prepare theme migration strategy
- [ ] Set up Modus web components in project

## Best Practices

1. **Incremental Migration**: Migrate component by component
2. **Test Continuously**: Verify functionality after each component
3. **Document Decisions**: Record custom solutions for no-mapping cases
4. **Maintain Consistency**: Use same patterns across the codebase
5. **Performance Monitoring**: Check bundle size impact

## Support Resources

- Modus V2 Documentation
- Web Components integration guides
- MUI to Modus mapping reference
- Migration pattern library
- Community examples and solutions
