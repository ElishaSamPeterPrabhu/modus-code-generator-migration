# Modus Migration Code Generation Tool

## Purpose
Migrate Modus v1 code to Modus v2 code using the provided mapping and best practices.

## Rules
- Replace all Modus v1 tags with their Modus v2 equivalents, if available.
- Update attributes to match the v2 API (e.g., map `buttonStyle` to `variant`).
- If a v1 tag has no v2 equivalent, leave it unchanged and add a comment explaining why.
- Add required Modus imports at the top of the HTML if not present.
- Preserve the structure and content of the original code as much as possible.

## Output Format
- Output the fully migrated code as a Markdown code block (specify the language, e.g., `html`).
- If any tags could not be migrated, list them in a Markdown table below the code block with reasons.

## Example
Given this input:
```html
<modus-button buttonStyle="primary">Click</modus-button>
<modus-foo>Legacy</modus-foo>
```
The output should be:
```html
<!-- Import Modus Web Components and styles here -->
<modus-wc-button variant="primary">Click</modus-wc-button>
<!-- No v2 equivalent for modus-foo -->
<modus-foo>Legacy</modus-foo>
```

| v1 Tag      | v2 Tag          | Notes                |
|-------------|-----------------|----------------------|
| modus-foo   | N/A             | No v2 equivalent     |

</rewritten_file> 