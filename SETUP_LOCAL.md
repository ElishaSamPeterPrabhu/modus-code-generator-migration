# Local MCP Server Setup Guide

This guide will help you set up the Shadcn to Modus Migration MCP Server on the `master-local` branch.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone and Navigate to the Repository

```bash
cd /path/to/modus-code-generator-migration
git checkout master-local
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Required packages:
- `mcp>=0.3.1` - Model Context Protocol library
- `fastapi>=0.104.0` - Web framework (for future extensions)
- `pydantic>=2.4.2` - Data validation
- Other supporting libraries

### 4. Verify Installation

Run the test script to ensure everything is working:

```bash
python3 test_mcp_server.py
```

You should see:
```
🎉 All tests passed! MCP server is working correctly.
```

## Running the Server

### Option 1: Direct Python Command

```bash
python3 shadcn_mcp_server_local.py
```

### Option 2: Using the Start Script

```bash
./start_mcp_server.sh
```

The server runs in stdio mode and communicates via standard input/output.

## MCP Client Configuration

### For Claude Desktop

1. Locate your Claude Desktop config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "shadcn-modus-migration-local": {
      "command": "python3",
      "args": [
        "/absolute/path/to/modus-code-generator-migration/shadcn_mcp_server_local.py"
      ],
      "env": {}
    }
  }
}
```

**Important:** Replace `/absolute/path/to/` with your actual path!

3. Restart Claude Desktop

### For Cursor IDE

1. Open Cursor settings
2. Navigate to MCP configuration
3. Add the server with the same configuration as above

### For Other MCP Clients

Refer to your client's documentation for adding MCP servers. The key configuration is:
- Command: `python3` (or `python`)
- Args: Full path to `shadcn_mcp_server_local.py`
- Transport: stdio

## Verifying the Setup

### In Claude Desktop / Cursor

Once configured, you should be able to use the MCP tools:

```
Can you list all available Modus components?
```

The AI should use the `list_all_modus_components()` tool to respond.

### Manual Testing

You can also test individual functions by importing them:

```python
python3 -c "
from shadcn_mcp_server_local import get_shadcn_component_mapping
import json
result = get_shadcn_component_mapping()
data = json.loads(result)
print(f'Found {len(data[\"shadcn_to_modus\"])} component mappings')
"
```

## Troubleshooting

### "No module named 'mcp'"

The MCP library is not installed. Run:
```bash
pip install mcp
```

### "command not found: python"

Use `python3` instead of `python`, or create an alias:
```bash
alias python=python3
```

### "FileNotFoundError" when loading data

Check that you're running the server from the correct directory:
```bash
cd /path/to/modus-code-generator-migration
python3 shadcn_mcp_server_local.py
```

### Server Not Responding in MCP Client

1. Check that the path in your config is absolute (not relative)
2. Verify the path exists: `ls -la /path/to/shadcn_mcp_server_local.py`
3. Test the script directly: `python3 /path/to/shadcn_mcp_server_local.py`
4. Check MCP client logs for errors

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Available Tools

Once set up, the following MCP tools are available:

1. **get_shadcn_component_mapping()** - Get component mappings
2. **get_migration_workflow_guide()** - Get workflow documentation
3. **get_migration_phase_guide(phase)** - Get phase-specific guide
4. **get_modus_component_data(component)** - Get Modus component specs
5. **get_shadcn_to_modus_migration_data(component)** - Get migration data
6. **list_all_modus_components()** - List all available components

See `README_LOCAL.md` for detailed tool documentation.

## Next Steps

1. Read `README_LOCAL.md` for complete tool documentation
2. Review `shadcn_migration/md_prompts/workflow_shadcn.md` for migration workflow
3. Start migrating your shadcn components!

## Support

For issues:
1. Check this setup guide
2. Review `README_LOCAL.md`
3. Run `python3 test_mcp_server.py` for diagnostics
4. Check the MCP client logs

## Quick Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the server
python3 test_mcp_server.py

# Run the server
python3 shadcn_mcp_server_local.py

# Or use the start script
./start_mcp_server.sh
```

## What's Different in This Branch?

The `master-local` branch contains:
- **Streamlined MCP server** (`shadcn_mcp_server_local.py`) - Only shadcn migration tools
- **Focused data** - Only shadcn and Modus V2 component data (no V1, MUI, or Connect)
- **Local configuration** - Optimized for running locally
- **Comprehensive docs** - Setup guides and tool documentation
- **Test suite** - Verify everything works

## Branch Purpose

This branch is specifically designed for:
- Running the MCP server locally (not as a cloud service)
- Providing shadcn to Modus migration assistance
- Connecting to MCP clients like Claude Desktop, Cursor, etc.
- Development and testing of migration workflows

---

**Branch:** `master-local`  
**Last Updated:** February 2026
