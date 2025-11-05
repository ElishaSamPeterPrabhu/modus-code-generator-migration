# shadcn/ui to Modus Migration Analyze Tool

## Purpose
Analyze provided code for shadcn/ui components. For each shadcn component, identify its Modus V2 web component equivalent and outline the migration approach. This analysis will serve as the blueprint for the `migrate_shadcn.md` phase.

## Data Sources
- `shadcn_to_modus_mapping.json`: Maps shadcn component names to their Modus V2 **web component** equivalents (e.g., `Button` maps to `modus-wc-button`).
- `v2_components.json`: Details about Modus V2 **web components** (e.g., `modus-wc-button`, `modus-wc-alert`). This is the source of truth for existing V2 web components, their properties, and events.
- `v2_react_framework_data.json`: **How-to guide** for using Modus V2 **web components** within React.

## Core Analysis Objective
For each source file, produce an `analysis_report.md` detailing:
*   **Framework Identification**: shadcn/ui is React-based (using Radix UI primitives with Tailwind CSS).
*   **shadcn Components Found**: List each shadcn component, its props, and context.
*   **Proposed Modus V2 Migration Strategy**:
    *   **Identify V2 Web Component**: Use `shadcn_to_modus_mapping.json` to find the Modus V2 **web component** tag (e.g., `modus-wc-button` for shadcn `Button`).
    *   **Migration Approach**:
        *   Target is the Modus V2 **web component tag** directly in JSX (e.g., `<modus-wc-button>`).
        *   Note that `v2_react_framework_data.json` will be consulted for:
            *   Ensuring `defineCustomElements()` is called.
            *   Correctly passing attributes/properties to the web component in JSX.
            *   Handling events on the web component in JSX.
*   **Migration Feasibility**: Based on component availability in Modus.
*   **Potential Issues/Notes**:
    *   If no Modus equivalent exists: "**No Modus V2 equivalent found for shadcn `[Component Name]`.** This component will require custom implementation."
    *   Tailwind classes: "shadcn components use Tailwind CSS styling which needs conversion to Modus design tokens and CSS."
    *   Radix UI primitives: "shadcn is built on Radix UI primitives - migration to Modus requires understanding of the underlying primitive behavior."
    *   Variants and styling: "shadcn uses `class-variance-authority` (cva) for variants - these need mapping to Modus component properties."

## shadcn-Specific Analysis Rules:

1.  **Import Analysis**: 
    *   Identify shadcn imports (e.g., `import { Button } from "@/components/ui/button"`).
    *   Track component file locations (shadcn components are typically in `components/ui/` directory).
    *   Note cn() utility usage for className merging.

2.  **Component Identification**:
    *   shadcn components are typically PascalCase (e.g., `<Button>`, `<Input>`).
    *   Identify component props and their values.
    *   Note className props with Tailwind classes.
    *   Track variant props.

3.  **Special shadcn Patterns**:
    *   **className with Tailwind**: Needs conversion to Modus CSS or component props.
    *   **Variant props**: Map to Modus component variants where available.
    *   **Composition patterns**: Components like Form, Card with sub-components need special handling.
    *   **Radix primitives**: Direct use of Radix UI primitives needs custom migration strategy.

4.  **Property Analysis**:
    *   Map shadcn props to Modus props.
    *   Identify props with no direct equivalent.
    *   Note Tailwind classes that control appearance.

5.  **Event Mapping**:
    *   shadcn events are standard React events (onClick, onChange, etc.).
    *   Map to Modus web component events.

## Output Generation

1.  **Report Content**: For each input source file, compile an analysis report including:
    *   List of shadcn imports and their usage.
    *   Detailed component analysis with:
        *   shadcn component name and location in code.
        *   Props used and their values.
        *   Proposed Modus component.
        *   Property mapping strategy.
        *   Required structural changes.
        *   Tailwind class conversions needed.
    *   Overall migration complexity assessment.
    *   Step-by-step migration recommendations.

2.  **Saving the Report**:
    *   Save as `[original_filename].shadcn-analysis.md`.
    *   Create `analysis_reports/shadcn/` subdirectory structure mirroring source files.

## Example Analysis Output

```markdown
# shadcn/ui Migration Analysis Report
**Source File**: src/components/LoginForm.tsx
**Framework**: React (shadcn/ui)

## Components Found

### 1. Button (Line 25)
- **shadcn Usage**: `<Button variant="default" size="lg" onClick={handleSubmit}>Login</Button>`
- **Target Modus Component**: `modus-wc-button`
- **Property Mappings**:
  - `variant="default"` → `variant="filled"`
  - `size="lg"` → `size="lg"`
  - `onClick` → `@buttonClick` (event rename)
- **Notes**: Direct mapping available with property transformations needed

### 2. Input (Line 18)
- **shadcn Usage**: `<Input type="email" placeholder="Email" className="w-full" />`
- **Target Modus Component**: `modus-wc-text-input`
- **Property Mappings**:
  - `type="email"` → `type="email"`
  - `placeholder` → `placeholder`
  - `className="w-full"` → `full-width` attribute or CSS
- **Notes**: Tailwind width class needs conversion

## Migration Summary
- **Overall Complexity**: Medium
- **Components with no mapping**: 0
- **Manual interventions needed**: Tailwind class conversions
```
