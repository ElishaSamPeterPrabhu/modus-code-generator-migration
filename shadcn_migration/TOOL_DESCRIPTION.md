# shadcn/ui Migration Assistant Tool

This tool provides shadcn/ui to Modus migration guidance and mappings.

## Input
A string representing either:
1. The word **"mapping"** - to get component mapping information
2. A process/workflow name: **"analyze"**, **"migrate"**, **"verify"**, **"log"**, or **"workflow"**

## Output

### If input is "mapping"
Returns the unified mapping JSON file containing both directions:
- `component_mappings.json` with structure:
  ```json
  {
    "shadcn_to_modus": { "Button": "modus-wc-button", ... },
    "modus_to_shadcn": { "modus-wc-button": "Button", ... }
  }
  ```

### If input is a process name
Returns the filename of the workflow documentation:
- `"analyze"` → `"analyze_shadcn.md"`
- `"migrate"` → `"migrate_shadcn.md"`
- `"verify"` → `"verify_shadcn.md"`
- `"log"` → `"log_shadcn.md"`
- `"workflow"` → `"workflow_shadcn.md"`

## Examples
- Input: `"mapping"` → Output: `component_mappings.json`
- Input: `"analyze"` → Output: `"analyze_shadcn.md"`
- Input: `"workflow"` → Output: `"workflow_shadcn.md"`

## What This Tool Helps With

This tool helps developers:
- **Access component mappings** between shadcn/ui and Modus V2
- **Locate workflow documentation** for each migration phase
- **Understand** which shadcn components have Modus equivalents
- **Navigate** the migration process from analysis through verification

## About shadcn/ui Migration

shadcn/ui is a collection of re-usable React components built with:
- **Radix UI** primitives for accessibility and behavior
- **Tailwind CSS** for styling
- **Copy-paste** model (components live in your codebase)

Migration challenges include:
- Converting Tailwind utility classes to Modus CSS/props
- Adapting Radix UI primitive behaviors to Modus web components
- Handling composition patterns (Card, Form, Dialog with sub-components)
- Components without direct Modus equivalents (Command, Carousel, etc.)

Use this tool to streamline the shadcn/ui to Modus migration process.
