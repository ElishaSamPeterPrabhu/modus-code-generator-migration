# shadcn/ui to Modus Migration Tool

## Purpose
Transform shadcn/ui components to Modus V2 web components based on the analysis report. This tool performs the actual code transformation while preserving functionality.

## Data Sources
- **Analysis Report**: The `.shadcn-analysis.md` file from the analyze phase
- `shadcn_to_modus_mapping.json`: Component mapping reference
- `v2_components.json`: Modus V2 web component specifications
- `v2_react_framework_data.json`: React integration patterns for Modus web components

## Migration Strategy

### 1. Import Transformation
- **Remove shadcn imports**: Remove all `@/components/ui/*` imports
- **Add Modus imports**: 
  ```javascript
  import { defineCustomElements } from '@trimble-oss/modus-web-components/loader';
  
  // Call once in app initialization
  defineCustomElements();
  ```

### 2. Component Transformation Rules

#### Basic Components
- **shadcn Component** → **Modus Web Component**
- Apply property mappings from analysis report
- Transform event handlers to Modus format

#### Complex Patterns

**Tailwind Classes**:
- Convert Tailwind utility classes to:
  - Modus component props where available
  - CSS classes using Modus design tokens
  - Custom CSS when necessary

**Variants**:
- shadcn: `<Button variant="outline" size="sm">Click</Button>`
- Modus: `<modus-wc-button variant="outlined" size="sm">Click</modus-wc-button>`

**Form Components**:
- shadcn uses composition (Label + Input)
  ```tsx
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
  ```
- Modus structure:
  ```tsx
  <modus-wc-input-label for="email">Email</modus-wc-input-label>
  <modus-wc-text-input id="email" type="email"></modus-wc-text-input>
  ```

### 3. Property Mapping Examples

| shadcn Prop | Modus Prop | Transformation |
|-------------|------------|----------------|
| `variant="default"` | `variant="filled"` | Value map |
| `variant="outline"` | `variant="outlined"` | Value map |
| `variant="destructive"` | `color="danger"` | Prop rename + value map |
| `size="sm"` | `size="sm"` | Direct |
| `className="w-full"` | `full-width={true}` | Tailwind → prop |
| `asChild` | N/A | Not supported |

### 4. Event Handler Transformation

```tsx
// shadcn
<Button onClick={handleClick}>Click</Button>

// Modus in React
<modus-wc-button onButtonClick={handleClick}>Click</modus-wc-button>
```

### 5. Styling Migration
- Remove Tailwind utility classes
- Use Modus design tokens
- Apply custom CSS for unique styling
- Use `custom-class` prop for additional styling

## Migration Process

1. **Parse Source File**: Read the original file and its analysis report
2. **Transform Imports**: Update import statements
3. **Component Migration**:
   - For each identified shadcn component:
     - Replace with Modus equivalent
     - Transform properties
     - Convert Tailwind classes
     - Update event handlers
4. **Style Migration**:
   - Convert Tailwind classes to Modus CSS
   - Update theme references
5. **Generate Output**:
   - Save as `[original_filename].migrated.[ext]`
   - Preserve original file

## Special Considerations

### No Direct Mapping Components
For components with no Modus equivalent:
- Add comment: `// TODO: No direct Modus equivalent for shadcn [Component]`
- Suggest alternatives or custom implementation
- Common patterns:
  - Command → Custom implementation
  - Carousel → Custom slider or manual implementation
  - AspectRatio → CSS aspect-ratio property

### Radix UI Primitives
If code uses Radix UI directly (not through shadcn):
- Note that Modus components are standalone
- May need significant restructuring
- Add manual review comments

## Output Format

The migrated file should:
1. Maintain the same functionality as the original
2. Use Modus V2 web components correctly
3. Include TODO comments for manual review items
4. Preserve code structure and formatting where possible

## Migration Log
Generate a `migration.log` documenting:
- Components successfully migrated
- Properties transformed
- Tailwind classes converted
- Manual interventions required
- Warnings or potential issues
- Components skipped (no mapping)
