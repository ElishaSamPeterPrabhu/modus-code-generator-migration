# Modus Code Generation and Migration

A toolkit for generating and migrating Modus Web Components code between versions.

## Overview

This project provides utilities for working with Modus Web Components, including:

- Component data extraction and analysis
- Code generation tools
- Migration helpers between Modus 1.0 and 2.0
- MCP (Model Context Protocol) integration for IDE assistance

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the MCP server:
   ```
   python mcp_server.py
   ```

## Features

- **Component Analysis**: Compare properties, events, and slots between v1 and v2 components
- **Code Generation**: Generate component code snippets with proper attributes and properties
- **Migration Tools**: Utilities to help migrate from Modus 1.0 to Modus 2.0
- **MCP Integration**: Model Context Protocol server for IDE integration (Cursor, VS Code, etc.)

## Project Structure

- `mcp_server.py`: Main server implementation for MCP integration
- `modus_migration/`: Migration utilities and component analysis
  - `component_analysis/`: Component data files for v1 and v2
- `index.html`: Example implementation of Modus components

## License

MIT License 