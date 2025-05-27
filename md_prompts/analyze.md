# Modus Migration Analyze Tool

## Purpose
Analyze the provided code for Modus v1 components and suggest Modus v2 replacements using authoritative component data. The tool should support analyzing either a single file or all files in a specified folder, as requested by the user.

## Data Sources
- **component_mapping.json**: Maps v1 component tags to their v2 equivalents (if any).
- **v1_components.json**: Lists all available v1 components, their properties, events, and documentation.
- **v2_components.json**: Lists all available v2 components, their properties, events, and documentation.

## Rules
- Load and parse the three JSON files above before analyzing code.
- Based on user input, analyze either:
  - A single specified file, or
  - All files within a specified folder (analyzing each file individually).
- For each file analyzed:
  - Identify all Modus v1 tags in the input code by matching against the list in v1_components.json.
  - For each v1 tag found:
    - Use component_mapping.json to suggest the correct v2 tag, if available.
    - If no mapping exists, mark as "N/A" and note there is no v2 equivalent.
    - If a mapping exists but the v2 tag is not present in v2_components.json, mark as "N/A" and note the v2 tag is missing from the library.
    - Count the number of occurrences for each v1 tag.
    - Optionally, add notes if there are breaking changes or special migration instructions (from mapping or documentation).
  - Output a Markdown table with columns: v1 Tag, v2 Tag, Count, Notes.
  - If a v1 tag is not in v1_components.json, note it as "Unknown component".

## Output Format
- The output should begin with a brief statement that the file(s) were analyzed using authoritative component data and mappings.
- For a single file, output the final Markdown table as described below.
- For multiple files, output a separate Markdown table for each file, clearly labeled with the file name.
- Do not include step-by-step or process details.

### Save the Analysis as Markdown
- **Save the analysis result as a markdown (.md) file** so the user can review it later.
- The file should be named `<original-filename>.analysis.md` (e.g., `my-component.tsx.analysis.md`) and placed alongside the analyzed file or in a designated `analysis/` folder.
- The markdown file should include:
  1. **Title and Summary**: A heading with the file name and a summary of the analysis.
  2. **Detailed Markdown Table**: As described below, listing all v1 components, v2 suggestions, counts, and notes.
  3. **Additional Notes**: Any migration recommendations, breaking changes, or special considerations.

```markdown
# Modus Migration Analysis: <filename>

This file was analyzed using authoritative Modus v1/v2 component data and mappings. Below is a summary of Modus v1 components found and migration recommendations.

| v1 Tag         | v2 Tag            | Count | Notes                |
|----------------|-------------------|-------|----------------------|
| modus-button   | modus-wc-button   | 2     | Direct replacement   |
| modus-alert    | modus-wc-alert    | 1     | Direct replacement   |
| modus-foo      | N/A               | 1     | No v2 equivalent     |
| custom-xyz     | N/A               | 1     | Unknown component    |
```

## How to Use the Data
- Always check for the presence of a v1 tag in v1_components.json before suggesting a mapping.
- Use component_mapping.json for authoritative v1→v2 mappings.
- Validate that any suggested v2 tag exists in v2_components.json before recommending it.
- Use documentation fields in the JSONs for additional migration notes if needed. 

---

**Remember:** The markdown analysis file is for user review and should be clear, detailed, and actionable for migration planning. 