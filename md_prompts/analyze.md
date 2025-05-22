# Modus Migration Analyze Tool

## Purpose
Analyze the provided code for Modus v1 components and suggest Modus v2 replacements.

## Rules
- Identify all Modus v1 tags in the input code.
- Suggest the correct Modus v2 tag for each v1 tag found.
- Count the number of occurrences for each v1 tag.
- Output a Markdown table with columns: v1 Tag, v2 Tag, Count, Notes.
- If a v1 tag has no v2 equivalent, note it in the table.

## Output Format
```markdown
| v1 Tag         | v2 Tag            | Count | Notes                |
|----------------|-------------------|-------|----------------------|
| modus-button   | modus-wc-button   | 2     | Direct replacement   |
| modus-alert    | modus-wc-alert    | 1     | Direct replacement   |
| modus-foo      | N/A               | 1     | No v2 equivalent     |
```

## Example
Given this input:
```html
<modus-button>Click</modus-button>
<modus-alert>Alert</modus-alert>
<modus-foo>Legacy</modus-foo>
```
The output should be:
```markdown
| v1 Tag         | v2 Tag            | Count | Notes                |
|----------------|-------------------|-------|----------------------|
| modus-button   | modus-wc-button   | 1     | Direct replacement   |
| modus-alert    | modus-wc-alert    | 1     | Direct replacement   |
| modus-foo      | N/A               | 1     | No v2 equivalent     |
``` 