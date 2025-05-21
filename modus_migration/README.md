# Modus Component Migration Tool

This tool extracts component details from Modus 1.0 and Modus 2.0 repositories to help with component migrations.

## Overview

The tool performs the following operations:
1. Clones both Modus 1.0 and 2.0 repositories
2. Extracts component details including props, events, slots, and storybook examples
3. Creates a mapping between Modus 1.0 and 2.0 components based on naming patterns and properties
4. Outputs JSON files with the extracted information

## Directory Structure

```
modus_migration/
├── component_analysis/    # Output JSON files go here
├── repos/                 # Cloned repositories are stored here
├── component_extractor.py # Main extraction script
└── README.md             # This file
```

## Usage

Run the component extractor script:

```bash
python component_extractor.py
```

## Output Files

The script generates three JSON files in the `component_analysis` directory:

1. `v1_components.json` - Contains details of all Modus 1.0 components
2. `v2_components.json` - Contains details of all Modus 2.0 components
3. `component_mapping.json` - Contains mappings between Modus 1.0 and 2.0 components

## Component Information

Each component entry contains:

- Props with descriptions and types
- Events
- Slots
- Documentation
- Storybook examples
- Default values
- Variant information

## Requirements

- Python 3.6+
- Git (for repository cloning)

## Components

- **component_extractor.py**: Script to extract component details from Modus repositories
- **modusagent.py**: Core LangGraph workflow for migrating components
- **run_modus.py**: Entry point script to run the migration workflow
- **utils.py**: Utility functions for the migration process
- **cache.py**: Caching utilities for LLM calls

## Directories

- **component_analysis/**: Contains extracted component data in JSON format
- **data/**: Storage for workflow state
- **setup/**: Setup scripts including comment extraction

## Usage

To run the component extraction:

```bash
python component_extractor.py
```

To run the migration workflow:

```bash
python run_modus.py
```

## Workflow

1. The component extractor analyzes Modus repositories to extract component details
2. The migration workflow uses LangGraph to:
   - Ingest repositories
   - Analyze component structures
   - Identify migration constraints
   - Generate a migration plan
   - Verify changes
   - Test with code examples
   - Output migrated code

## Key Differences Between Modus 1.0 and 2.0

- **Naming Pattern**: Modus 1.0 uses "modus-component" while 2.0 uses "modus-wc-component"
- **Directory Structure**: Different organization of storybook files
- **Property Changes**: Many properties have different names (e.g., buttonStyle → variant) 