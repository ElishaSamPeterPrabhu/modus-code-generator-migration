#!/usr/bin/env python3
"""
MCP Server for MUI to Modus Migration
Provides guidance and transformation tools for migrating from Material-UI v7 to Modus V2 components.
"""

from mcp.server.fastmcp import FastMCP
import json
import logging
import os
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("MUI to Modus Migration Server")

# Helper function to load JSON data
def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load and return JSON data from a file."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filepath)
        
        with open(full_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return {}

# Cache for loaded data
CACHED_DATA = {
    'mapping': None,
    'mui_components': None,
    'modus_components': None,
    'analyze_guidance': None,
    'migrate_guidance': None,
    'verify_guidance': None,
    'log_guidance': None,
    'workflow_guidance': None
}

def get_cached_data(key: str, filepath: str) -> Dict[str, Any]:
    """Get cached data or load from file if not cached."""
    if CACHED_DATA[key] is None:
        CACHED_DATA[key] = load_json_file(filepath)
    return CACHED_DATA[key]

def load_md_file(filepath: str) -> str:
    """Load and return markdown content from a file."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filepath)
        
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return f"Error: Could not load {filepath}"

@mcp.tool()
def get_mui_analyze_guidance() -> Dict[str, Any]:
    """
    Return guidance for the 'Analyze' step of MUI migration, including analyze_mui.md, 
    component data, and relevant directory paths.
    
    Returns:
        Dictionary containing:
        - guidance_text: Content of analyze_mui.md
        - component_data: MUI to Modus mapping and component information
        - directories: Paths for saving analysis reports
    """
    logger.info("Retrieving MUI analyze guidance")
    
    return {
        "guidance_text": load_md_file("md_prompts/analyze_mui.md"),
        "component_data": {
            "mui_to_modus_mapping": get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json'),
            "mui_components": get_cached_data('mui_components', 'component_extraction/mui_v7_components.json'),
            "modus_v2_components": get_cached_data('modus_components', '../modus_migration/component_analysis/v2_components.json')
        },
        "directories": {
            "analysis_reports": "analysis_reports/mui"
        }
    }

@mcp.tool()
def get_mui_migrate_guidance() -> Dict[str, Any]:
    """
    Return guidance for the 'Migrate' step of MUI migration, including migrate_mui.md 
    and component data.
    
    Returns:
        Dictionary containing:
        - guidance_text: Content of migrate_mui.md
        - component_data: MUI to Modus mapping and component information
    """
    logger.info("Retrieving MUI migrate guidance")
    
    return {
        "guidance_text": load_md_file("md_prompts/migrate_mui.md"),
        "component_data": {
            "mui_to_modus_mapping": get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json'),
            "mui_components": get_cached_data('mui_components', 'component_extraction/mui_v7_components.json'),
            "modus_v2_components": get_cached_data('modus_components', '../modus_migration/component_analysis/v2_components.json')
        }
    }

@mcp.tool()
def get_mui_verify_guidance() -> Dict[str, Any]:
    """
    Return guidance for the 'Verify' step of MUI migration, including verify_mui.md,
    component data, and the gold standard.
    
    Returns:
        Dictionary containing:
        - guidance_text: Content of verify_mui.md
        - component_data: MUI to Modus mapping and component information
        - gold_standard: Best practices for Modus V2 usage
    """
    logger.info("Retrieving MUI verify guidance")
    
    return {
        "guidance_text": load_md_file("md_prompts/verify_mui.md"),
        "component_data": {
            "mui_to_modus_mapping": get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json'),
            "modus_v2_components": get_cached_data('modus_components', '../modus_migration/component_analysis/v2_components.json')
        },
        "gold_standard": load_md_file("../migration/gold_standard.md")
    }

@mcp.tool()
def get_mui_log_guidance() -> Dict[str, Any]:
    """
    Return guidance for the 'Log' step of MUI migration, including log_mui.md 
    and relevant directory paths.
    
    Returns:
        Dictionary containing:
        - guidance_text: Content of log_mui.md
        - directories: Paths for migration logs
    """
    logger.info("Retrieving MUI log guidance")
    
    return {
        "guidance_text": load_md_file("md_prompts/log_mui.md"),
        "directories": {
            "migration_logs": "migration_logs/mui"
        }
    }

@mcp.tool()
def get_mui_workflow_guidance() -> Dict[str, Any]:
    """
    Return the overall MUI migration workflow guidance (workflow_mui.md) and all supporting data.
    
    Returns:
        Dictionary containing:
        - workflow_specific_guidance: Content of workflow_mui.md
        - all_guidance_documents: All markdown prompts
        - component_data: Complete component mapping and specifications
        - gold_standard: Best practices
        - directories: All relevant directory paths
    """
    logger.info("Retrieving complete MUI workflow guidance")
    
    return {
        "workflow_specific_guidance": load_md_file("md_prompts/workflow_mui.md"),
        "all_guidance_documents": {
            "analyze": load_md_file("md_prompts/analyze_mui.md"),
            "migrate": load_md_file("md_prompts/migrate_mui.md"),
            "verify": load_md_file("md_prompts/verify_mui.md"),
            "log": load_md_file("md_prompts/log_mui.md"),
            "workflow": load_md_file("md_prompts/workflow_mui.md")
        },
        "component_data": {
            "mui_to_modus_mapping": get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json'),
            "mui_components": get_cached_data('mui_components', 'component_extraction/mui_v7_components.json'),
            "modus_v2_components": get_cached_data('modus_components', '../modus_migration/component_analysis/v2_components.json')
        },
        "gold_standard": load_md_file("../migration/gold_standard.md"),
        "directories": {
            "analysis_reports": "analysis_reports/mui",
            "migration_logs": "migration_logs/mui",
            "verification_reports": "verification_reports/mui"
        }
    }

@mcp.tool()
def get_mui_component_mapping(component_name: str) -> Dict[str, Any]:
    """
    Get the Modus equivalent and migration details for a specific MUI component.
    
    Args:
        component_name: The MUI component name (e.g., 'Button', 'TextField')
        
    Returns:
        Dictionary containing:
        - mui_component: Original MUI component name
        - modus_component: Target Modus component
        - confidence: Migration confidence level
        - complexity: Migration complexity
        - notes: Migration notes and considerations
        - related_components: Any related component mappings
    """
    logger.info(f"Getting mapping for MUI component: {component_name}")
    
    mapping_data = get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json')
    
    if component_name in mapping_data.get('mapping', {}):
        result = {
            "mui_component": component_name,
            **mapping_data['mapping'][component_name]
        }
    elif component_name in mapping_data.get('no_direct_mapping', []):
        result = {
            "mui_component": component_name,
            "modus_component": None,
            "confidence": "none",
            "notes": "No direct Modus equivalent. See migration_notes for alternatives.",
            "complexity": "high"
        }
    else:
        result = {
            "mui_component": component_name,
            "error": f"Unknown MUI component: {component_name}"
        }
    
    # Add general migration notes
    result['migration_notes'] = mapping_data.get('migration_notes', {})
    
    return result

@mcp.tool()
def transform_mui_props(component_name: str, props: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform MUI component props to Modus component props based on mapping rules.
    
    Args:
        component_name: The MUI component name
        props: Dictionary of MUI props
        
    Returns:
        Dictionary containing:
        - modus_props: Transformed props for Modus component
        - unmapped_props: Props that couldn't be mapped
        - transformation_notes: Notes about the transformation
    """
    logger.info(f"Transforming props for MUI {component_name}")
    
    # Get component mapping
    mapping = get_mui_component_mapping(component_name)
    
    if 'error' in mapping or not mapping.get('modus_component'):
        return {
            "error": f"Cannot transform props - no mapping for {component_name}",
            "original_props": props
        }
    
    # Basic prop transformations (simplified - in real implementation would be more comprehensive)
    modus_props = {}
    unmapped_props = {}
    transformation_notes = []
    
    # Common transformations
    prop_mappings = {
        "Button": {
            "variant": {"contained": "filled", "outlined": "outlined", "text": "borderless"},
            "color": {"primary": "primary", "secondary": "secondary", "error": "danger", "warning": "warning"},
            "size": {"small": "sm", "medium": "md", "large": "lg"},
            "disabled": "disabled",
            "fullWidth": "full-width"
        },
        "TextField": {
            "error": "invalid",
            "disabled": "disabled",
            "required": "required",
            "placeholder": "placeholder",
            "value": "value",
            "defaultValue": "value"
        },
        "Checkbox": {
            "checked": "checked",
            "disabled": "disabled",
            "required": "required",
            "color": {"primary": "primary", "secondary": "secondary"},
            "size": {"small": "sm", "medium": "md"}
        }
    }
    
    # Apply transformations
    if component_name in prop_mappings:
        for mui_prop, mui_value in props.items():
            prop_map = prop_mappings[component_name].get(mui_prop)
            
            if prop_map is None:
                unmapped_props[mui_prop] = mui_value
            elif isinstance(prop_map, dict):
                # Value mapping
                if mui_value in prop_map:
                    modus_props[mui_prop] = prop_map[mui_value]
                else:
                    unmapped_props[mui_prop] = mui_value
                    transformation_notes.append(f"No mapping for {mui_prop}='{mui_value}'")
            else:
                # Direct mapping
                modus_props[prop_map] = mui_value
    
    # Handle special cases
    if component_name == "Button" and "startIcon" in props:
        transformation_notes.append("startIcon requires nested modus-wc-icon element")
    
    if component_name == "TextField" and "label" in props:
        transformation_notes.append("label requires separate modus-wc-input-label element")
    
    return {
        "modus_component": mapping['modus_component'],
        "modus_props": modus_props,
        "unmapped_props": unmapped_props,
        "transformation_notes": transformation_notes
    }

@mcp.tool()
def list_mui_components() -> Dict[str, List[str]]:
    """
    List all MUI components with their Modus mapping status.
    
    Returns:
        Dictionary containing:
        - mapped_components: List of MUI components with Modus equivalents
        - no_mapping_components: List of MUI components without direct Modus equivalents
        - total_components: Total count of MUI components
    """
    logger.info("Listing all MUI components and their mapping status")
    
    mapping_data = get_cached_data('mapping', 'mapping/mui_to_modus_mapping.json')
    mui_data = get_cached_data('mui_components', 'component_extraction/mui_v7_components.json')
    
    mapped = []
    no_mapping = mapping_data.get('no_direct_mapping', [])
    
    # Get mapped components
    for component, details in mapping_data.get('mapping', {}).items():
        status = f"{component} → {details.get('modus_component', 'N/A')} ({details.get('confidence', 'unknown')} confidence)"
        mapped.append(status)
    
    # Sort lists
    mapped.sort()
    no_mapping.sort()
    
    return {
        "mapped_components": mapped,
        "no_mapping_components": no_mapping,
        "total_components": len(mapped) + len(no_mapping),
        "mapping_rate": f"{len(mapped) / (len(mapped) + len(no_mapping)) * 100:.1f}%"
    }

# Run the server
if __name__ == "__main__":
    mcp.run()
