# Modus Migration Code Generation Tool

## Purpose
Migrate Modus v1 code to Modus v2 code using authoritative component data, mapping, and the results of the analysis step.

## Data Sources
- **component_mapping.json**: Maps v1 component tags to their v2 equivalents (if any).
- **v1_components.json**: Lists all available v1 components, their properties, events, and documentation.
- **v2_components.json**: Lists all available v2 components, their properties, events, and documentation.


## Input
- The tool should use the analysis data (the Markdown table and notes from the analyze step) as the basis for migration.
- The user may request migration for a single file or all files in a folder.
- The input code can be in any format (HTML, JSX, TSX, etc.).

## Rules
- For each file to migrate:
  - Only migrate tags that have a v2 equivalent present in the v2 library, as indicated by the analysis data and authoritative JSONs.
  - For each tag to migrate:
    - Replace the v1 tag with the v2 tag as per the mapping.
    - Update attributes to match the v2 API (e.g., map `buttonStyle` to `variant`).
    - If the analysis notes specify special migration steps (e.g., slot changes for `modus-alert`), follow those instructions.
  - If a v1 tag has no v2 equivalent, leave it unchanged and add a comment directly above the component explaining why (e.g., "// No v2 equivalent for modus-foo").
  - If any feature/property/event of a migrated component is not available in v2.0, add a comment directly above the component explaining what is missing or not migrated (e.g., "// 'button-text' property is not available in v2.0").
  - Add required Modus imports at the top if not present (for HTML/JSX/TSX files).
  - Preserve the structure and content of the original code as much as possible.

## Output Format
- For a single file, output the fully migrated code as a Markdown code block (use a generic code block, e.g., '```code').
- For multiple files, output a separate code block for each file, clearly labeled with the file name.
- If any tags could not be migrated, list them in a Markdown table below the code block(s) with reasons.

## Example
Given this input:
```code
<modus-button buttonStyle="primary">Click</modus-button>
<modus-foo>Legacy</modus-foo>
<modus-alert button-text="Action">Alert</modus-alert>
```
And this analysis:
```markdown
| v1 Tag      | v2 Tag          | Count | Notes                                  |
|-------------|-----------------|-------|----------------------------------------|
| modus-button| modus-wc-button | 1     | Direct replacement                     |
| modus-foo   | N/A             | 1     | No v2 equivalent                       |
| modus-alert | modus-wc-alert  | 1     | 'button-text' not available in v2.0    |
```
The output should be:
```code
// Import Modus Web Components and styles here if required
<modus-wc-button variant="primary">Click</modus-wc-button>
// No v2 equivalent for modus-foo
<modus-foo>Legacy</modus-foo>
// 'button-text' property is not available in v2.0
<modus-wc-alert>Alert</modus-wc-alert>
```

| v1 Tag      | v2 Tag          | Notes                                  |
|-------------|-----------------|----------------------------------------|
| modus-foo   | N/A             | No v2 equivalent                       |
| modus-alert | modus-wc-alert  | 'button-text' not available in v2.0    |
