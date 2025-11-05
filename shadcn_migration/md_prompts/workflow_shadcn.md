# shadcn/ui to Modus Component Migration Workflow

## Overview
This document outlines the end-to-end workflow for migrating shadcn/ui components to Modus V2 components. shadcn/ui is a collection of re-usable components built with Radix UI and Tailwind CSS.

## Phase 1: Analyze

*   **Objective**: Examine source code, identify shadcn components, and propose Modus V2 migration strategies.
*   **Key Characteristics of shadcn/ui**:
    *   React-based components using Radix UI primitives
    *   Styled with Tailwind CSS utility classes
    *   Copy-paste component model (components live in your codebase)
    *   Uses `class-variance-authority` (cva) for variants
*   **Agent Action**:
    1.  Use `analyze_shadcn.md` guidance
    2.  Reference `shadcn_to_modus_mapping.json` for component mapping
    3.  Identify Tailwind classes that need conversion
*   **Key Outputs**:
    *   `[filename].shadcn-analysis.md` in `analysis_reports/shadcn/` directory
    *   Identified shadcn components with migration strategies
    *   Tailwind class conversion requirements
    *   Property mapping strategies
*   **User Prompt**: "shadcn analysis complete. Review reports and reply 'proceed to migrate' or specify changes."

## Phase 2: Migrate

*   **Objective**: Transform shadcn components to Modus V2 based on analysis.
*   **Special Considerations**:
    *   Import statement transformation
    *   JSX syntax adaptation for web components
    *   Tailwind class conversion to Modus CSS/props
    *   Event handler updates
    *   Variant mapping (cva variants → Modus props)
*   **Agent Action**:
    1.  Execute migration using `migrate_shadcn.md` guidance
    2.  Apply component and property mappings
    3.  Convert Tailwind classes appropriately
    4.  Handle composition patterns (Card, Form, etc.)
*   **Key Outputs**:
    *   `[filename].migrated.[ext]` files
    *   `migration.log` with detailed transformation record
    *   TODO comments for manual review items
*   **User Prompt**: "shadcn migration complete. Review migrated files and logs. Reply 'proceed to verify' or specify changes."

## Phase 3: Verify

*   **Objective**: Ensure migrated code is correct and follows Modus best practices.
*   **Verification Focus**:
    *   Web component integration in React
    *   Event handling correctness
    *   Tailwind conversion completeness
    *   Functionality preservation
    *   No remaining shadcn dependencies
*   **Agent Action**:
    1.  Run verification using `verify_shadcn.md` guidance
    2.  Check component validity against `v2_components.json`
    3.  Validate patterns against gold standard
    4.  Review Tailwind conversions
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
    *   Tailwind conversion summary
*   **Agent Action**:
    1.  Consolidate using `log_shadcn.md` guidance
    2.  Generate summary statistics
    3.  Create action item lists
    4.  Document Tailwind conversion patterns
*   **Key Outputs**:
    *   `overall_migration_summary.md`
    *   `action_items.md`
    *   `migration_metrics.json`
*   **User Prompt**: "shadcn migration process complete. Summary and action items available."

## Key Differences from Other Migrations

### Component Nature
- **Modus V1**: Web components → Web components
- **MUI**: React library → Web components
- **shadcn**: Copy-paste React components → Web components

### Styling Approach
- **Modus V1**: CSS/attributes
- **MUI**: Theme system, sx prop
- **shadcn**: Tailwind utility classes

### Common Challenges

1. **Tailwind CSS Conversion**:
   - Utility classes need conversion to Modus CSS
   - Responsive classes require media queries
   - Custom Tailwind config needs mapping

2. **Radix UI Primitives**:
   - shadcn components wrap Radix UI
   - Modus components are standalone
   - Behavioral differences may exist

3. **Copy-Paste Nature**:
   - shadcn components live in user's codebase
   - Each project may have customized components
   - Variants may be project-specific

4. **No Direct Mappings**:
   - Command (command palette)
   - Carousel
   - Form (composition helper)
   - ScrollArea
   - AspectRatio

5. **Composition Patterns**:
   - Card with CardHeader, CardContent, CardFooter
   - Form with FormField, FormItem, FormLabel
   - Dialog with DialogTrigger, DialogContent
   - Need restructuring for Modus

## Migration Readiness Checklist

Before starting:
- [ ] Inventory shadcn components used
- [ ] Identify custom shadcn modifications
- [ ] Review Tailwind configuration
- [ ] Plan for components without Modus equivalent
- [ ] Set up Modus web components in project

## Best Practices

1. **Incremental Migration**: Migrate component by component
2. **Test Continuously**: Verify functionality after each component
3. **Document Conversions**: Record Tailwind → Modus CSS patterns
4. **Maintain Consistency**: Use same patterns across codebase
5. **Preserve Accessibility**: Ensure ARIA attributes are maintained

## Support Resources

- Modus V2 Documentation
- Web Components integration guides
- shadcn to Modus mapping reference
- Tailwind conversion patterns
- Community examples and solutions
