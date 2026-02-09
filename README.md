# Complete Modus Migration MCP Server

A comprehensive local MCP server for migrating from **any major UI library** to Modus V2 web components.

## Supported Migration Systems

1. **Shadcn/UI → Modus V2** (42+ components)
2. **Material UI (MUI) → Modus V2** (40+ components)
3. **Connect UI → Modus V2** (50+ components)
4. **Modus V1 → Modus V2** (all components)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test the server
python3 test_mcp_server.py

# Run the server
python3 shadcn_mcp_server_local.py
```

## Documentation

- **[SETUP_LOCAL.md](SETUP_LOCAL.md)** - Complete installation and setup guide
- **[README_LOCAL.md](README_LOCAL.md)** - Detailed tool reference and usage
- **[MIGRATION_SYSTEMS.md](MIGRATION_SYSTEMS.md)** - Overview of all four migration systems

## MCP Tools Available

### Overview
- `get_migration_system_overview()` - Overview of all four systems

### Shadcn/UI
- `get_shadcn_component_mapping()`
- `get_migration_workflow_guide()`
- `get_migration_phase_guide(phase)`
- `get_shadcn_to_modus_migration_data(component)`

### Material UI
- `get_mui_component_mapping()`
- `get_mui_migration_guide(phase)`

### Connect UI
- `get_connect_ui_component_mapping()`
- `get_connect_migration_guide(phase)`

### Modus V1 to V2
- `get_modus_v1_to_v2_mapping()`
- `get_modus_v1_component_data(component)`

### Common Tools
- `get_modus_component_data(component)` - Get Modus V2 specs
- `list_all_modus_components()` - List all Modus V2 components

## MCP Client Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "modus-migration-local": {
      "command": "python3",
      "args": ["/absolute/path/to/shadcn_mcp_server_local.py"]
    }
  }
}
```

### Cursor IDE

Configure in Cursor MCP settings with the same configuration.

## Data Structure

```
modus-code-generator-migration/
├── shadcn_mcp_server_local.py    # Main MCP server (13 tools)
├── requirements.txt               # Python dependencies
├── test_mcp_server.py            # Test suite
├── start_mcp_server.sh           # Startup script
│
├── shadcn_migration/             # Shadcn data
├── mui_migration/                # MUI data
├── connect_migration/            # Connect UI data
└── modus_migration/              # Modus V1 & V2 data
```

## Features

- **170+ components** mapped across all systems
- **13 MCP tools** for comprehensive migration support
- **4-phase workflow** (Analyze, Migrate, Verify, Log)
- **Local deployment** - No cloud dependencies
- **Complete documentation** - Setup guides and references
- **Test suite included** - Verify everything works

## License

Part of the Modus Code Generator Migration system.

---

**Branch:** master-local  
**Version:** 2.0 - Complete Migration Coverage  
**Last Updated:** February 2026
