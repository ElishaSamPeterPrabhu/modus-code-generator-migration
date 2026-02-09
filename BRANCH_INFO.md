# Branch Information: master-local

## Branch Purpose

The `master-local` branch is a specialized version of the repository designed specifically for running the **Shadcn to Modus Migration MCP Server locally**.

## What's Different from Master?

### Added Files

1. **shadcn_mcp_server_local.py** - Main MCP server implementation
   - Contains 6 MCP tools for shadcn migration
   - Runs in stdio mode for MCP client integration
   - Lightweight and focused on shadcn migration only

2. **README_LOCAL.md** - Complete documentation
   - Tool reference for all 6 MCP tools
   - Migration workflow documentation
   - Data structure explanation
   - Troubleshooting guide

3. **SETUP_LOCAL.md** - Installation and setup guide
   - Step-by-step installation instructions
   - MCP client configuration examples
   - Troubleshooting common issues
   - Quick reference commands

4. **test_mcp_server.py** - Test suite
   - Tests all 6 MCP tools
   - Validates data loading
   - Verifies error handling
   - Provides diagnostic information

5. **start_mcp_server.sh** - Convenience startup script
   - Creates/activates virtual environment
   - Installs dependencies
   - Starts the MCP server

6. **mcp_config_example.json** - Example MCP configuration
   - Shows how to configure Claude Desktop
   - Template for other MCP clients

7. **BRANCH_INFO.md** - This file

### Modified Files

- **.gitignore** - Updated to exclude:
  - Virtual environments
  - Migration output files
  - Local MCP configurations
  - External repository clones

## MCP Tools Available

### 1. get_shadcn_component_mapping()
Returns bidirectional mapping between shadcn and Modus components.

### 2. get_migration_workflow_guide()
Returns complete migration workflow documentation.

### 3. get_migration_phase_guide(phase: str)
Returns phase-specific guide ("analyze", "migrate", "verify", "log").

### 4. get_modus_component_data(component_name: str)
Returns detailed Modus V2 component specifications.

### 5. get_shadcn_to_modus_migration_data(shadcn_component: str)
Returns migration data for specific shadcn component.

### 6. list_all_modus_components()
Lists all available Modus V2 components.

## Data Included

### Shadcn Migration Data
- `shadcn_migration/mapping/component_mappings.json` - Component mappings
- `shadcn_migration/md_prompts/workflow_shadcn.md` - Workflow guide
- `shadcn_migration/md_prompts/analyze_shadcn.md` - Analysis phase
- `shadcn_migration/md_prompts/migrate_shadcn.md` - Migration phase
- `shadcn_migration/md_prompts/verify_shadcn.md` - Verification phase
- `shadcn_migration/md_prompts/log_shadcn.md` - Logging phase

### Modus Component Data
- `modus_migration/component_analysis/v2_components.json` - All Modus V2 components
- `modus_migration/component_analysis/v2_react_framework_data.json` - React integration

## What's NOT Included (vs Master)

To keep this branch lightweight for local MCP server use:

- **No Modus V1 data** - Only V2 is needed for shadcn migration
- **No MUI migration data** - Separate from shadcn migration
- **No Connect UI data** - Not relevant for shadcn migration
- **No external repositories** - Excluded via .gitignore
- **No cloud/production server code** - This is local-only

## Use Cases

This branch is designed for:

1. **Local Development** - Run MCP server on your machine
2. **AI-Assisted Migration** - Connect to Claude Desktop, Cursor, etc.
3. **Testing** - Verify migration strategies before applying
4. **Learning** - Explore shadcn to Modus migration patterns

## Quick Start

```bash
# Switch to this branch
git checkout master-local

# Install dependencies
pip install -r requirements.txt

# Test the server
python3 test_mcp_server.py

# Run the server
python3 shadcn_mcp_server_local.py

# Or use the convenience script
./start_mcp_server.sh
```

## MCP Client Integration

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shadcn-modus-migration-local": {
      "command": "python3",
      "args": ["/absolute/path/to/modus-code-generator-migration/shadcn_mcp_server_local.py"]
    }
  }
}
```

### Cursor IDE

Configure MCP servers in Cursor settings with the same configuration.

## Documentation

- **SETUP_LOCAL.md** - Installation and configuration
- **README_LOCAL.md** - Complete tool reference and usage
- **shadcn_migration/md_prompts/** - Migration phase guides

## Testing

```bash
# Run all tests
python3 test_mcp_server.py

# Expected output:
# 🎉 All tests passed! MCP server is working correctly.
```

## Maintenance

### Updating Component Data

If Modus V2 components change:
1. Update `modus_migration/component_analysis/v2_components.json`
2. Update `shadcn_migration/mapping/component_mappings.json` if needed
3. Run `python3 test_mcp_server.py` to verify

### Adding New Tools

1. Add new `@mcp.tool()` function in `shadcn_mcp_server_local.py`
2. Add test in `test_mcp_server.py`
3. Document in `README_LOCAL.md`

## Version History

- **Initial Creation** (Feb 2026) - Created master-local branch with local MCP server
  - 6 MCP tools for shadcn migration
  - Comprehensive documentation
  - Test suite
  - Setup scripts

## Branch Strategy

- **master** - Main branch with all migration systems
- **master-local** - This branch, focused on local shadcn MCP server
- Keep synchronized with master for shared data (shadcn_migration/, modus_migration/)
- This branch adds local-specific files only

## Support

For help:
1. Read SETUP_LOCAL.md for installation issues
2. Read README_LOCAL.md for tool usage
3. Run `python3 test_mcp_server.py` for diagnostics
4. Check MCP client logs for connection issues

## Contributing

When making changes to this branch:
1. Maintain focus on local MCP server functionality
2. Keep documentation updated
3. Add tests for new features
4. Ensure backward compatibility with MCP clients

---

**Branch:** master-local  
**Created:** February 2026  
**Purpose:** Local MCP server for shadcn to Modus migration  
**Status:** Active Development
