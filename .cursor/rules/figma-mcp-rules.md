Figma to Modus Web Components MCP Specification
Purpose: This specification defines the exact process for converting Figma designs into Modus Web Components using the Figma MCP Server. For: Developers using AI assistants (Claude, ChatGPT, Cursor) with the Figma MCP Server Requirement: Attach this file to your AI conversation for accurate Figma-to-code conversion
Core Task Definition
Create a new page called [PAGE_NAME].[extension] along with a corresponding CSS file. Use the analyze_figma tool to retrieve the layout for this page from the connected Figma file.
Step-by-Step TODO List
Phase 1: Initial Analysis
Get the Figma URL from the user
Call analyze_figma("[FIGMA_URL]") for the main page
Document the page dimensions and layout type
List all major components found in hierarchical order
Identify which components need deep analysis
Phase 2: Component Deep Dive
For each major component identified:

Extract the component's node ID from the initial analysis
Call analyze_figma("[FIGMA_URL]", node_id="[NODE_ID]")
Document the component's:
Exact dimensions (width x height)
Layout method (flex/grid/absolute)
Spacing values (gap, padding, margins)
Position (if absolute)
Child components
Repeat recursively for nested components
Phase 3: Modus Component Mapping
Create a list of all unique component types found
For each component type:
Identify the corresponding Modus component
Call get_modus_component_data("[modus-component-name]")
Document required props
Document optional props that match Figma
Note any components that cannot be mapped
Phase 4: Documentation
Create the layout analysis document with:
Page overview section
Component hierarchy visualization
Individual component analysis for each major component
Modus component mapping table
List of custom components needed (if any)
Phase 5: Implementation Code Generation
Generate the main page file with:
All necessary Modus component imports
Exact layout structure from Figma
Components with proper props from analysis
Inline styles matching Figma dimensions/positioning
Generate the CSS file with:
Layout styles for containers
Any custom styling needed
Exact spacing and dimensions
Phase 6: Validation
Verify every Figma component is represented
Check all dimensions match exactly
Ensure component hierarchy is preserved
Confirm no extra features were added
Validate all Modus components are properly configured
⚠️ CRITICAL GUIDELINES
You MUST:
Work with the Web Components version of the Modus code
Stay 100% accurate and faithful to the Figma layout
Use exact pixel values from Figma (no rounding or approximations)
Preserve the exact component hierarchy as shown in Figma
Document any components that cannot be mapped to Modus
You MUST NOT:
Add ANYTHING that isn't present in the Figma design
Make creative interpretations of the design
Add features, functionality, or enhancements not shown
Optimize or simplify the component structure
Change spacing, dimensions, or layout properties
Required Analysis Format
1. Page Overview
# [PAGE_NAME] Layout Analysis

## Page Information
- Name: [From Figma]
- Dimensions: [WIDTH]x[HEIGHT]px
- Layout Type: [sidebar-layout/header-content-footer/etc]
- Background: [Color/Image]

## Component Hierarchy
[Indented list showing parent-child relationships]
2. Component Analysis
For EACH component, document:

## Component: [COMPONENT_NAME]
- Figma Node ID: [NODE_ID]
- Type: [FRAME/GROUP/INSTANCE/etc]
- Dimensions: [WIDTH]x[HEIGHT]px
- Position: [X, Y coordinates if absolute]
- Layout: [flex/grid/absolute]
  - Direction: [horizontal/vertical]
  - Gap: [VALUE]px
  - Padding: [TOP]px [RIGHT]px [BOTTOM]px [LEFT]px
  - Alignment: [main axis] / [cross axis]

### Modus Mapping
- Modus Component: modus-wc-[component-name]
- Props Required: [List exact props needed]
- Layout CSS: [Exact CSS properties from Figma]

### Children
[List all child components with their mappings]
MCP Tool Usage
Primary Analysis Tool
analyze_figma(figma_url: str, node_id: Optional[str] = None)

Purpose: Analyzes Figma designs and returns component mappings
Returns: Layout structure, component detection, dimensions, CSS properties, undetected components
Usage: Start with full page, then analyze each component with its node_id
N8N Workflow Integration
For n8n implementations, use the MCP webhook endpoint:

POST https://flows-webhook.stage.trimble-ai.com/mcp/agentic/n8n-server/v1/modus

Request Body:

{
  "tool": "analyze_figma",
  "parameters": {
    "figma_url": "https://figma.com/design/...",
    "node_id": "optional-node-id"
  }
}

Headers:

Authorization: Bearer {AUTH_TOKEN}
Content-Type: application/json
New: Undetected Components Tracking
The tool now provides visibility into elements that couldn't be mapped to Modus components:

undetected_components: Section showing elements that need manual implementation
mapping_summary: Statistics about detection rates and analysis coverage
possible_reasons: Explanations for why elements weren't matched (e.g., "Generic Figma element", "Layout container", "Decorative element")
🔍 Getting More Details When Needed
The output is optimized for context efficiency. If you need more details about specific elements:

Use Node IDs: Every element in the layout structure includes an id field
Call with Specific Node:

analyze_figma(figma_url, node_id="2100:44186")  # Analyze specific node

When to Use:
Need full details about a collapsed group (e.g., "Pattern/Fingerprint (×4)")
Want to see all children of a truncated section
Investigating specific undetected components
Need deeper nesting levels for complex layouts

Example: If the concise output shows collapsed elements and you need details:

Find the node ID from the layout structure
Call analyze_figma with that specific node_id
Get complete details for just that section
Component Documentation Tool
get_modus_component_data(component_name: str)

Purpose: Gets documentation for Modus Web Components
Returns: Props, events, slots, methods, usage examples
Usage: Call for each unique Modus component type found

N8N Usage:

{
  "tool": "get_modus_component_data",
  "parameters": {
    "component_name": "modus-wc-table"
  }
}
Layout Fidelity Rules
Spacing & Dimensions
Use exact pixel values (e.g., 24px not 25px or 1.5rem)
Preserve all padding values exactly as specified
Maintain exact gaps between elements
Keep precise positioning for absolute elements
Component Hierarchy
Maintain exact nesting as shown in Figma
Don't flatten or optimize structure
Keep all wrapper elements even if they seem unnecessary
Preserve component groupings
Styling
Extract exact colors (use hex values from Figma)
Match border radius precisely
Apply shadows exactly as defined
Preserve opacity values
💡 Pro Tip: Drilling Down for Details
When the initial analysis shows collapsed or summarized elements (to manage context size):

// Initial call shows collapsed pattern
const result = await analyze_figma("https://figma.com/...");
// Output shows: "Pattern/Fingerprint (×83)" - 83 elements collapsed

// Get full details for that specific node
const details = await analyze_figma("https://figma.com/...", "I2100:43169;5684:55307");
// Now you see all 83 individual fingerprint elements with their properties

This two-step approach keeps the initial analysis manageable while allowing deep dives when needed.
Common Pitfalls to Avoid
Adding Helper Text: Don't add tooltips, placeholders, or helper text not in Figma
Inferring Behavior: Don't add hover states, animations, or interactions not shown
Improving Layout: Don't "fix" spacing or alignment that looks odd
Adding Accessibility: Don't add ARIA labels or roles unless specified in Figma
Responsive Behavior: Don't add media queries or responsive behavior not defined
Handling Undetected Components
When analyze_figma reports undetected components, follow these guidelines:
Understanding the Report
The tool provides:

Count: Total number of unmatched elements
Reasons: Why elements weren't matched (grouped by category)
Examples: Specific elements in each category
Developer Notes: Suggestions for implementation
Common Undetected Elements
Layout Containers: Frames/Groups used for spacing

Implement as <div> with appropriate CSS
Preserve exact spacing and layout properties

Decorative Elements: Vectors, shapes, lines

Implement with CSS or inline SVG
Maintain exact visual appearance

Standalone Text: Text not part of a component

Use appropriate HTML tags (<p>, <h1>, etc.)
Apply Modus typography classes

Images: Rectangle elements with fills

Implement as <img> tags
Request actual image assets from design team
Validation Checklist
Before delivering the implementation, verify:

Every component in Figma is represented in the code
All dimensions match Figma exactly (no rounding)
Component hierarchy is preserved exactly
All Modus components are properly imported
CSS properties match Figma's layout properties
No additional features or enhancements added
Node IDs are documented for traceability
Layout type (flex/grid/absolute) matches Figma
Resources
When You Need React Implementation
If you encounter any issues or need to follow the React implementation of a component, refer to this documentation and apply its guidance accordingly:

Modus Web Components for React – Documentation
When You Need Angular Implementation
When You Need Angular Implementation
If you encounter any issues or need to follow the Angular implementation of a component, refer to this documentation and apply its guidance accordingly:

Modus Web Components for Angular – Documentation
Component Documentation
Always use get_modus_component_data("[component-name]") for accurate props
Component names follow pattern: modus-wc-[component-name]
Check for required vs optional props
Example Usage
Direct MCP Usage
Task: Create a new page called `dashboard-new.tsx` along with a corresponding CSS file.

Figma Link: https://www.figma.com/design/kLKbrIfRJA7IutXoutdS3w/test-mcp?node-id=2100-70772

Following the TODO list:

Phase 1: Initial Analysis ✓
> analyze_figma("https://www.figma.com/design/kLKbrIfRJA7IutXoutdS3w/test-mcp?node-id=2100-70772")
- Found: Sidebar navigation, header, main content area, data table

Phase 2: Component Deep Dive
> For sidebar (node-id="2100-70773"):
> analyze_figma("https://www.figma.com/design/kLKbrIfRJA7IutXoutdS3w/test-mcp", node_id="2100-70773")

> For header (node-id="2100-70774"):
> analyze_figma("https://www.figma.com/design/kLKbrIfRJA7IutXoutdS3w/test-mcp", node_id="2100-70774")

Phase 3: Modus Component Mapping
> get_modus_component_data("modus-wc-side-navigation")
> get_modus_component_data("modus-wc-navbar")
> get_modus_component_data("modus-wc-table")

[Continue through all phases...]
N8N Workflow Usage
For n8n implementations, create workflows that call the MCP webhook:

Step 1: Initial Analysis

{
  "method": "POST",
  "url": "https://flows-webhook.stage.trimble-ai.com/mcp/agentic/n8n-server/v1/modus",
  "headers": {
    "Authorization": "Bearer {{$env.AUTH_TOKEN}}",
    "Content-Type": "application/json"
  },
  "body": {
    "tool": "analyze_figma",
    "parameters": {
      "figma_url": "https://www.figma.com/design/kLKbrIfRJA7IutXoutdS3w/test-mcp?node-id=2100-70772"
    }
  }
}

Step 2: Component Documentation

{
  "tool": "get_modus_component_data",
  "parameters": {
    "component_name": "modus-wc-navbar"
  }
}

Available Workflow Files:

n8n-workflows/analyze-figma-modular-complete.built.json: Complete Figma analysis pipeline
n8n-workflows/get-modus-component-github.json: Component documentation fetcher

See N8N_FIGMA_MCP_IMPLEMENTATION_GUIDE.md for detailed n8n implementation patterns and examples.



Remember: The goal is 100% fidelity to the Figma design. When in doubt, match Figma exactly rather than making assumptions or improvements.

