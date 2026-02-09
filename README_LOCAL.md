# Complete Modus Migration MCP Server - Local Setup

This branch (`master-local`) contains a comprehensive local MCP server setup for migrating **all major UI libraries** to Modus V2 web components.

## Purpose

This local server provides AI assistants with access to migration data for **four different UI migration systems** through the Model Context Protocol (MCP), enabling intelligent code migration assistance for:

1. **Shadcn/UI → Modus V2** - React components with Tailwind CSS
2. **Material UI (MUI) → Modus V2** - MUI React component library
3. **Connect UI → Modus V2** - Trimble internal UI library
4. **Modus V1 → Modus V2** - Upgrade from Modus V1 to V2

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Server Locally

```bash
python shadcn_mcp_server_local.py
```

The server runs in stdio mode and can be integrated with MCP-compatible clients.

## MCP Server Configuration

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shadcn-modus-migration-local": {
      "command": "python",
      "args": ["/path/to/modus-code-generator-migration/shadcn_mcp_server_local.py"],
      "env": {}
    }
  }
}
```

### Cursor/Other MCP Clients

Configure according to your client's MCP setup documentation, pointing to the `shadcn_mcp_server_local.py` script.

## Available MCP Tools

### Overview Tool

#### `get_migration_system_overview()`
Get an overview of all four migration systems and their capabilities.

**Returns:** Information about all migration systems, their challenges, and available tools.

**Example:**
```python
get_migration_system_overview()
```

---

### Shadcn/UI Migration Tools

#### 1. `get_shadcn_component_mapping()`
Get complete bidirectional mapping between shadcn/ui and Modus V2 components.

#### 2. `get_migration_workflow_guide()`
Get complete shadcn migration workflow documentation (all phases).

#### 3. `get_migration_phase_guide(phase: str)`
Get shadcn-specific phase guide (`"analyze"`, `"migrate"`, `"verify"`, `"log"`).

#### 4. `get_shadcn_to_modus_migration_data(shadcn_component: str)`
Get complete migration data for a specific shadcn component.

---

### Material UI (MUI) Migration Tools

#### 5. `get_mui_component_mapping()`
Get complete bidirectional mapping between MUI and Modus V2 components.

**Returns:**
- `mui_to_modus`: Maps MUI components to Modus tags (e.g., `TextField` → `modus-wc-text-input`)
- `modus_to_mui`: Reverse mapping

#### 6. `get_mui_migration_guide(phase: str)`
Get MUI-specific migration guide (`"analyze"`, `"migrate"`, `"verify"`, `"log"`, `"workflow"`).

---

### Connect UI Migration Tools

#### 7. `get_connect_ui_component_mapping()`
Get comprehensive Connect UI to Modus mapping with detailed property mappings and migration notes.

**Returns:** Detailed mapping including:
- Property mappings
- Event mappings
- Migration notes
- Required structural changes

#### 8. `get_connect_migration_guide(phase: str)`
Get Connect UI-specific migration guide for each phase.

---

### Modus V1 to V2 Migration Tools

#### 9. `get_modus_v1_to_v2_mapping()`
Get mapping between Modus V1 and V2 components.

**Returns:**
- Component mappings
- Deprecated components
- Verification rules
- Migration plan

#### 10. `get_modus_v1_component_data(component_name: str)`
Get detailed Modus V1 component specifications.

---

### Common Tools (All Migration Systems)

#### 11. `get_modus_component_data(component_name: str)`
Get detailed Modus V2 component specifications.

**Parameters:**
- `component_name`: Component name with or without `modus-wc-` prefix

**Returns:** JSON with props, events, slots, and documentation.

#### 12. `list_all_modus_components()`
List all available Modus V2 web components.

## Data Structure

```
modus-code-generator-migration/
├── shadcn_mcp_server_local.py      # Main MCP server (LOCAL)
├── README_LOCAL.md                  # This file
├── requirements.txt                 # Python dependencies
│
├── shadcn_migration/               # Shadcn migration data
│   ├── mapping/
│   │   └── component_mappings.json # Component mappings
│   └── md_prompts/
│       ├── workflow_shadcn.md      # Complete workflow
│       ├── analyze_shadcn.md       # Analysis phase guide
│       ├── migrate_shadcn.md       # Migration phase guide
│       ├── verify_shadcn.md        # Verification phase guide
│       └── log_shadcn.md           # Logging phase guide
│
└── modus_migration/                # Modus component data
    └── component_analysis/
        ├── v2_components.json      # Modus V2 component specs
        └── v2_react_framework_data.json  # React integration data
```

## Migration Workflow

### Phase 1: Analyze
Examine source code, identify shadcn components, and propose migration strategies.

```python
# Get analysis guidance
get_migration_phase_guide("analyze")

# Get component mapping
get_shadcn_component_mapping()
```

### Phase 2: Migrate
Transform shadcn components to Modus V2 based on analysis.

```python
# Get migration guidance
get_migration_phase_guide("migrate")

# Get specific component migration data
get_shadcn_to_modus_migration_data("Button")
get_modus_component_data("button")
```

### Phase 3: Verify
Ensure migrated code is correct and follows Modus best practices.

```python
# Get verification guidance
get_migration_phase_guide("verify")
```

### Phase 4: Log
Consolidate migration artifacts and generate reports.

```python
# Get logging guidance
get_migration_phase_guide("log")
```

## Key Features

### Focused on Shadcn Migration
- **42+ shadcn components** with direct Modus mappings
- Tailwind CSS to Modus conversion guidance
- Radix UI primitive migration strategies
- Composition pattern handling

### Comprehensive Data
- Complete component specifications
- Property mapping strategies
- Event handler transformations
- Styling migration guidance

### Phase-by-Phase Guidance
- Structured workflow with clear phases
- Detailed instructions for each phase
- Best practices and common pitfalls
- Automated verification checks

## Components Without Direct Mapping

The following shadcn components have no direct Modus equivalent and require custom implementation:

- Command (command palette)
- Carousel
- Form (composition helper)
- ScrollArea
- AspectRatio
- InputOTP
- ToggleGroup

## Special Considerations

### Tailwind CSS Conversion
shadcn components use Tailwind utility classes extensively. The migration process includes:
- Converting utility classes to Modus design tokens
- Mapping responsive classes to media queries
- Handling custom Tailwind configurations

### Radix UI Primitives
shadcn is built on Radix UI primitives. Migration considerations:
- Modus components are standalone (no Radix dependency)
- Behavioral differences may exist
- Accessibility features need verification

### Copy-Paste Nature
shadcn components live in the user's codebase:
- Each project may have customized components
- Variants may be project-specific
- Custom styling needs preservation

## Development

### Testing the Server

```bash
# Run the server
python shadcn_mcp_server_local.py

# Test with MCP inspector (if available)
mcp dev shadcn_mcp_server_local.py
```

### Adding New Tools

1. Add new `@mcp.tool()` decorated function in `shadcn_mcp_server_local.py`
2. Update this README with tool documentation
3. Test with your MCP client

## Troubleshooting

### Server Won't Start
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check file paths in data loading code

### Data Not Loading
- Verify directory structure matches expected layout
- Check file permissions
- Ensure JSON files are valid

### MCP Client Connection Issues
- Verify client configuration points to correct script path
- Check environment variables if needed
- Review client-specific MCP setup documentation

## License

This project is part of the Modus Code Generator Migration system.

## Support

For issues or questions:
1. Check this README
2. Review the migration workflow guide
3. Examine phase-specific guides
4. Consult Modus documentation

## Version

Branch: `master-local`  
Purpose: Local MCP server for shadcn to Modus migration  
Last Updated: February 2026
