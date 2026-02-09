from mcp.server.fastmcp import FastMCP
import json
import logging
import os
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Shadcn to Modus Migration Server")


@mcp.tool()
def get_shadcn_component_mapping() -> str:
    """
    Get the complete mapping between shadcn/ui components and Modus V2 web components
    
    Returns:
        JSON string with bidirectional component mappings:
        - shadcn_to_modus: Maps shadcn component names to Modus V2 tags
        - modus_to_shadcn: Maps Modus V2 tags to shadcn component names
    
    Example:
        >>> get_shadcn_component_mapping()
    """
    logger.info("Retrieving shadcn to Modus component mappings")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "shadcn_migration",
            "mapping",
            "component_mappings.json"
        )
        
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
            
        return json.dumps(mapping_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading component mappings: {e}")
        return json.dumps({"error": f"Error loading component mappings: {str(e)}"})


@mcp.tool()
def get_migration_workflow_guide() -> str:
    """
    Get the complete migration workflow documentation for shadcn/ui to Modus V2 migration
    
    This includes:
    - Overview of the migration process
    - Phase-by-phase workflow (Analyze, Migrate, Verify, Log)
    - Key differences from other migrations
    - Best practices and checklist
    
    Returns:
        Markdown string with complete workflow guidance
    
    Example:
        >>> get_migration_workflow_guide()
    """
    logger.info("Retrieving migration workflow guide")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workflow_path = os.path.join(
            script_dir,
            "shadcn_migration",
            "md_prompts",
            "workflow_shadcn.md"
        )
        
        with open(workflow_path, "r") as f:
            workflow_content = f.read()
            
        return workflow_content
        
    except Exception as e:
        logger.error(f"Error loading workflow guide: {e}")
        return json.dumps({"error": f"Error loading workflow guide: {str(e)}"})


@mcp.tool()
def get_migration_phase_guide(phase: str) -> str:
    """
    Get detailed guidance for a specific migration phase
    
    Args:
        phase: The migration phase name ("analyze", "migrate", "verify", or "log")
    
    Returns:
        Markdown string with phase-specific guidance
    
    Example:
        >>> get_migration_phase_guide("analyze")
        >>> get_migration_phase_guide("migrate")
    """
    logger.info(f"Retrieving migration guide for phase: {phase}")
    
    valid_phases = ["analyze", "migrate", "verify", "log"]
    
    if phase.lower() not in valid_phases:
        return json.dumps({
            "error": f"Invalid phase '{phase}'. Valid phases are: {', '.join(valid_phases)}"
        })
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(
            script_dir,
            "shadcn_migration",
            "md_prompts",
            f"{phase.lower()}_shadcn.md"
        )
        
        with open(guide_path, "r") as f:
            guide_content = f.read()
            
        return guide_content
        
    except Exception as e:
        logger.error(f"Error loading phase guide for {phase}: {e}")
        return json.dumps({"error": f"Error loading phase guide: {str(e)}"})


@mcp.tool()
def get_modus_component_data(component_name: str) -> str:
    """
    Get detailed component data for a Modus V2 web component
    
    Args:
        component_name: The name of the Modus component (e.g., 'button', 'alert', 'text-input')
                       Can be provided with or without 'modus-wc-' prefix
    
    Returns:
        JSON string with component properties, events, slots, and documentation
    
    Example:
        >>> get_modus_component_data('button')
        >>> get_modus_component_data('modus-wc-text-input')
    """
    logger.info(f"Retrieving Modus component data for: {component_name}")
    
    # Standardize component name
    if component_name.startswith("modus-wc-"):
        component_name = component_name.replace("modus-wc-", "")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        v2_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "v2_components.json"
        )
        
        with open(v2_path, "r") as f:
            v2_components = json.load(f)
        
        # Try to find the component
        v2_tag = f"modus-wc-{component_name}"
        v2_file = f"{v2_tag}.tsx"
        component_data = v2_components.get(v2_file)
        
        if not component_data:
            # Try flexible matching
            for key in v2_components.keys():
                if component_name.lower() in key.lower():
                    component_data = v2_components[key]
                    v2_file = key
                    v2_tag = key.replace(".tsx", "")
                    break
        
        if not component_data:
            available_components = [
                key.replace("modus-wc-", "").replace(".tsx", "")
                for key in v2_components.keys()
                if key.startswith("modus-wc-")
            ]
            return json.dumps({
                "error": f"Component '{component_name}' not found",
                "available_components": sorted(available_components)
            })
        
        result = {
            "component_name": component_name,
            "tag_name": v2_tag,
            "file": v2_file,
            "props": component_data.get("props", []),
            "events": component_data.get("events", []),
            "slots": component_data.get("slots", []),
            "documentation": component_data.get("documentation", "")
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading component data: {e}")
        return json.dumps({"error": f"Error loading component data: {str(e)}"})


@mcp.tool()
def get_shadcn_to_modus_migration_data(shadcn_component: str) -> str:
    """
    Get complete migration data for converting a specific shadcn component to Modus V2
    
    Args:
        shadcn_component: The shadcn component name (e.g., 'Button', 'Input', 'Card')
    
    Returns:
        JSON string with:
        - shadcn component name
        - Modus V2 equivalent tag
        - Modus component specification
        - Migration guidance and notes
    
    Example:
        >>> get_shadcn_to_modus_migration_data('Button')
        >>> get_shadcn_to_modus_migration_data('AlertDialog')
    """
    logger.info(f"Retrieving migration data for shadcn component: {shadcn_component}")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load mapping
        mapping_path = os.path.join(
            script_dir,
            "shadcn_migration",
            "mapping",
            "component_mappings.json"
        )
        
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
        
        # Get Modus equivalent
        modus_tag = mapping_data.get("shadcn_to_modus", {}).get(shadcn_component)
        
        if modus_tag is None:
            return json.dumps({
                "shadcn_component": shadcn_component,
                "modus_equivalent": None,
                "note": "No direct Modus equivalent available for this shadcn component",
                "suggestion": "Consider custom implementation or alternative approach",
                "available_shadcn_components": list(mapping_data.get("shadcn_to_modus", {}).keys())
            })
        
        # Load Modus component data
        v2_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "v2_components.json"
        )
        
        with open(v2_path, "r") as f:
            v2_components = json.load(f)
        
        # Get component data
        component_name = modus_tag.replace("modus-wc-", "")
        v2_file = f"{modus_tag}.tsx"
        modus_data = v2_components.get(v2_file, {})
        
        result = {
            "shadcn_component": shadcn_component,
            "modus_tag": modus_tag,
            "modus_component_name": component_name,
            "modus_data": {
                "props": modus_data.get("props", []),
                "events": modus_data.get("events", []),
                "slots": modus_data.get("slots", []),
                "documentation": modus_data.get("documentation", "")
            },
            "migration_notes": {
                "import_change": "Remove shadcn import, use Modus web component",
                "jsx_syntax": f"Use <{modus_tag}></{modus_tag}> instead of <{shadcn_component}></{shadcn_component}>",
                "styling": "Convert Tailwind classes to Modus props/CSS",
                "events": "Update event handlers to Modus event names"
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving migration data: {e}")
        return json.dumps({"error": f"Error retrieving migration data: {str(e)}"})


@mcp.tool()
def list_all_modus_components() -> str:
    """
    List all available Modus V2 web components with their descriptions
    
    Returns:
        JSON string with array of all Modus components and their capabilities
    
    Example:
        >>> list_all_modus_components()
    """
    logger.info("Listing all Modus V2 components")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        v2_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "v2_components.json"
        )
        
        with open(v2_path, "r") as f:
            v2_components = json.load(f)
        
        components = []
        
        for file_name, data in v2_components.items():
            if file_name.startswith("modus-wc-"):
                component_name = file_name.replace("modus-wc-", "").replace(".tsx", "")
                tag_name = file_name.replace(".tsx", "")
                
                components.append({
                    "name": component_name,
                    "tag": tag_name,
                    "description": data.get("documentation", "")[:200] + "..." if len(data.get("documentation", "")) > 200 else data.get("documentation", ""),
                    "props_count": len(data.get("props", [])),
                    "events_count": len(data.get("events", []))
                })
        
        components.sort(key=lambda x: x["name"])
        
        result = {
            "total_components": len(components),
            "components": components
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error listing components: {e}")
        return json.dumps({"error": f"Error listing components: {str(e)}"})


# Execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
