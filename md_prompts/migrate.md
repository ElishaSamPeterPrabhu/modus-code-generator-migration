# Modus Migration Code Generation Tool

## Purpose
Migrate Modus v1 code (including within Angular and React frameworks) to Modus v2 code using authoritative component data, mapping, framework-specific guidance, and the results of the analysis step.

## Data Sources
- **component_mapping.json**: Maps v1 component tags to their v2 equivalents (if any).
- **v1_components.json**: Lists all available v1 web components, their properties, events, and documentation.
- **v2_components.json**: Lists all available v2 web components, their properties, events, and documentation.
- **v1_angular_framework_data.json**: Contains v1 Angular integration documentation (from `.mdx`) and code examples.
- **v1_react_framework_data.json**: Contains v1 React integration documentation (from `.mdx`) and code examples.
- **v2_angular_framework_data.json**: Contains v2 Angular integration documentation (from `.mdx`).
- **v2_react_framework_data.json**: Contains v2 React integration documentation (from `.mdx`) and code examples.

## Input
- The tool **must** use the analysis data (the Markdown table and notes from the `analyze` step) as the primary basis for migration decisions. This includes respecting the parent-child migration rule.
- The user may request migration for a single file or all files in a folder.
- The input code can be in any format (HTML, JSX, TSX, etc.).

## Rules
- For each file to migrate:
  - **Adhere to Analysis Output**: Strictly follow the `v2 Tag` and `Notes` from the analysis report for each component.
  - **Parent-Child Migration Rule (Crucial Implementation):**
    - If the analysis report indicates a component (parent or child) should not be migrated (e.g., `v2 Tag` is `N/A` or `N/A (Blocked by Parent)`), then **do not attempt to migrate that component or its children.**
    - Leave the original v1 tag and its children (if applicable) unchanged in the code.
    - Add a comment directly above the v1 parent component explaining why it (and consequently its children) was not migrated, referencing the analysis (e.g., "// MODUS MIGRATION: 'modus-parent' not migrated (no v2 equivalent). Child components also not migrated.").
  - Only migrate tags that have a valid v2 equivalent identified in the analysis and are present in the `v2_components.json` library (unless blocked by parent).
  - **Framework-Specific Migration (Angular/React):**
    - If the analysis (or file type) indicates an Angular or React context:
      - Consult the `documentation` and `examples` sections within the relevant `vX_angular_framework_data.json` or `vX_react_framework_data.json` files.
      - Apply framework-specific migration patterns. This might involve:
        - Using or updating Angular/React wrapper components.
        - Adjusting event handling (e.g., `(buttonClick)` vs `onButtonClick`).
        - Modifying attribute binding (e.g., `[property]` vs `property={value}`).
        - Ensuring correct import statements for framework-specific Modus libraries (e.g., `@trimble-oss/moduswebcomponents-angular`).
        - The `documentation` section in these JSONs provides guidance that should be followed.
  - For each tag to migrate (that is not blocked):
    - Replace the v1 tag with the v2 tag as per the mapping in the analysis.
    - Update attributes to match the v2 API (e.g., map `buttonStyle` to `variant`), referencing `prop_mappings` in `component_mapping.json` or details in `v1_components.json` and `v2_components.json`.
    - If the analysis notes specify special migration steps (e.g., slot changes for `modus-alert`), follow those instructions.
  - If a v1 tag has no v2 equivalent (and is not part of a non-migrated parent-child block), leave it unchanged and add a comment directly above the component explaining why (e.g., "// MODUS MIGRATION: No v2 equivalent for modus-foo").
  - If any feature/property/event of a migrated component is not available in v2.0 (as per analysis or component JSONs), add a comment directly above the component explaining what is missing or not migrated (e.g., "// MODUS MIGRATION: 'button-text' property is not available in v2.0").
  - Add required Modus imports (web components, Angular/React specific, CSS) at the top if not present, following guidelines from the `modusmcp` custom instructions and framework data.
  - Preserve the structure and content of the original code as much as possible.

## Output Format
- For a single file, output the fully migrated code as a Markdown code block (use a generic code block, e.g., '```code').
- For multiple files, output a separate code block for each file, clearly labeled with the file name.
- If any tags could not be migrated (due to no v2 equivalent, parent-child rule, or other reasons), list them in a Markdown table below the code block(s) with reasons, consistent with the analysis report.

## Example
Given analysis indicating `modus-parent` has no v2 equivalent, and `modus-button` is within an Angular context:
Input:
```html
<modus-parent>
  <modus-button [buttonStyle]="'primary'" (buttonClick)="onClick()">Click</modus-button>
</modus-parent>
<modus-foo>Legacy</modus-foo>
```
Output should be:
```code
// MODUS MIGRATION: 'modus-parent' not migrated (no v2 equivalent). Child components also not migrated.
<modus-parent>
  <modus-button [buttonStyle]="'primary'" (buttonClick)="onClick()">Click</modus-button>
</modus-parent>
// MODUS MIGRATION: No v2 equivalent for modus-foo
<modus-foo>Legacy</modus-foo>
```

| v1 Tag         | v2 Tag          | Notes                                                                 |
|----------------|-----------------|-----------------------------------------------------------------------|
| modus-parent   | N/A             | No v2 equivalent. Children not migrated.                              |
| modus-button   | N/A             | Not migrated due to parent 'modus-parent' not being migratable.       |
| modus-foo      | N/A             | No v2 equivalent                                                      |

(If `modus-parent` *was* migratable, the button example would change based on Angular v2 patterns from `v2_angular_framework_data.json`)