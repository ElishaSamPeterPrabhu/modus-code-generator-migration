# Modus Migration Analyze Tool

## Purpose
Analyze the provided code for Modus v1 components (including those within Angular and React frameworks) and suggest Modus v2 replacements using authoritative component data. The tool should support analyzing either a single file or all files in a specified folder, as requested by the user.

## Data Sources
- **component_mapping.json**: Maps v1 component tags to their v2 equivalents (if any).
- **v1_components.json**: Lists all available v1 web components, their properties, events, and documentation.
- **v2_components.json**: Lists all available v2 web components, their properties, events, and documentation.
- **v1_angular_framework_data.json**: Contains v1 Angular integration documentation (from `.mdx`) and code examples.
- **v1_react_framework_data.json**: Contains v1 React integration documentation (from `.mdx`) and code examples.
- **v2_angular_framework_data.json**: Contains v2 Angular integration documentation (from `.mdx`).
- **v2_react_framework_data.json**: Contains v2 React integration documentation (from `.mdx`) and code examples.

## Rules
- Load and parse all JSON data sources listed above before analyzing code.
- Based on user input, analyze either:
  - A single specified file, or
  - All files within a specified folder (analyzing each file individually).
- For each file analyzed:
  - Detect if the file is likely an Angular or React file (e.g., by extension `.ts`, `.tsx` with framework-specific imports or patterns). If so, make a note to consult the relevant `_framework_data.json` files for context during analysis and migration planning.
  - Identify all Modus v1 tags in the input code by matching against the list in `v1_components.json`.
  - **Parent-Child Migration Rule (Crucial):**
    - When analyzing, identify parent-child relationships between Modus components.
    - If a parent Modus v1 component cannot be migrated to v2 (e.g., no direct equivalent, or explicitly marked as not to migrate by user), then all its child Modus v1 components **must also be marked as 'Do Not Migrate' or 'Migration Blocked by Parent'**, even if they have a direct v2 equivalent. This is to maintain application integrity.
    - This rule should be clearly noted in the output for affected child components.
  - For each v1 tag found:
    - Use `component_mapping.json` to suggest the correct v2 tag, if available.
    - If a parent component is not migratable, mark the current child component's v2 Tag as 'N/A (Blocked by Parent)' and add a note.
    - If no mapping exists (and not blocked by a parent), mark as "N/A" and note there is no v2 equivalent.
    - If a mapping exists but the v2 tag is not present in `v2_components.json`, mark as "N/A" and note the v2 tag is missing from the library.
    - Count the number of occurrences for each v1 tag.
    - Optionally, add notes if there are breaking changes or special migration instructions (from mapping, `v1_components.json`/`v2_components.json` documentation, or relevant `_framework_data.json` files).
  - Output a Markdown table with columns: v1 Tag, v2 Tag, Count, Notes.
  - If a v1 tag is not in `v1_components.json`, note it as "Unknown component".

## Output Format
- The output should begin with a brief statement that the file(s) were analyzed using authoritative component data, framework integration details, and mappings.
- For a single file, output the final Markdown table as described below.
- For multiple files, output a separate Markdown table for each file, clearly labeled with the file name.
- Do not include step-by-step or process details.

### Save the Analysis as Markdown
- **Save the analysis result as a markdown (.md) file** so the user can review it later.
- The file should be named `<original-filename>.analysis.md` (e.g., `my-component.tsx.analysis.md`) and placed alongside the analyzed file or in a designated `analysis/` folder.
- The markdown file should include:
  1. **Title and Summary**: A heading with the file name and a summary of the analysis, noting if Angular/React context was considered.
  2. **Detailed Markdown Table**: As described below, listing all v1 components, v2 suggestions, counts, and notes (including parent-child migration blocks).
  3. **Additional Notes**: Any migration recommendations, breaking changes, framework-specific considerations (referencing `_framework_data.json` if applicable), or special considerations like the parent-child rule's impact.

```markdown
# Modus Migration Analysis: <filename>

This file was analyzed using authoritative Modus v1/v2 component data, framework integration details, and mappings. [Optional: Angular/React specific considerations were applied based on file content.] Below is a summary of Modus v1 components found and migration recommendations.

| v1 Tag         | v2 Tag                     | Count | Notes                                         |
|----------------|----------------------------|-------|-----------------------------------------------|
| modus-parent   | N/A                        | 1     | No v2 equivalent                              |
| modus-child    | N/A (Blocked by Parent)    | 2     | Parent 'modus-parent' cannot be migrated.     |
| modus-button   | modus-wc-button            | 2     | Direct replacement. Consider React wrapper.   |
| modus-alert    | modus-wc-alert             | 1     | Direct replacement. Check Angular form usage. |
| modus-foo      | N/A                        | 1     | No v2 equivalent                              |
| custom-xyz     | N/A                        | 1     | Unknown component                             |
```

## How to Use the Data
- Always check for the presence of a v1 tag in `v1_components.json` before suggesting a mapping.
- Use `component_mapping.json` for authoritative v1->v2 mappings.
- Consult `vX_angular_framework_data.json` or `vX_react_framework_data.json` when analyzing Angular or React files respectively, for specific integration patterns, wrapper examples, and potential issues noted in their documentation sections.
- Validate that any suggested v2 tag exists in `v2_components.json` before recommending it (unless blocked by a parent).
- Use documentation fields in all relevant JSONs for additional migration notes.
- **Strictly enforce the Parent-Child Migration Rule.**

---

**Remember:** The markdown analysis file is for user review and should be clear, detailed, and actionable for migration planning, especially highlighting any blocked migrations due to parent components or framework-specific needs. 