#!/bin/bash
# Script to export MUI migration files to main repository

echo "Exporting MUI migration files..."

# Create directory structure
mkdir -p ../mui_migration_export/mapping
mkdir -p ../mui_migration_export/md_prompts
mkdir -p ../mui_migration_export/component_extraction
mkdir -p ../mui_migration_export/test

# Copy mapping files
cp mui_migration/mapping/mui_to_modus_mapping.json ../mui_migration_export/mapping/
cp mui_migration/mapping/modus_to_mui_mapping.json ../mui_migration_export/mapping/

# Copy prompt files
cp mui_migration/md_prompts/*.md ../mui_migration_export/md_prompts/

# Copy extraction scripts
cp mui_migration/component_extraction/extract_mui_advanced.js ../mui_migration_export/component_extraction/
cp mui_migration/component_extraction/extract_mui_components_auto.py ../mui_migration_export/component_extraction/
cp mui_migration/component_extraction/package.json ../mui_migration_export/component_extraction/
cp mui_migration/component_extraction/README.md ../mui_migration_export/component_extraction/

# Copy MCP server
cp mui_migration/mcp_server_mui.py ../mui_migration_export/

# Copy test file
cp mui_migration/test/UserForm.jsx ../mui_migration_export/test/

# Copy main README
cp mui_migration/README.md ../mui_migration_export/

echo "Export complete! Files are in ../mui_migration_export/"
echo "You can now copy these files to your main branch."

