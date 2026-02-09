from mcp.server.fastmcp import FastMCP
import json
import logging
import os
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Complete Modus Migration Server - All UI Libraries")


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


@mcp.tool()
def get_mui_component_mapping() -> str:
    """
    Get the complete mapping between Material UI (MUI) components and Modus V2 web components
    
    Returns:
        JSON string with bidirectional component mappings:
        - mui_to_modus: Maps MUI component names to Modus V2 tags
        - modus_to_mui: Maps Modus V2 tags to MUI component names
    
    Example:
        >>> get_mui_component_mapping()
    """
    logger.info("Retrieving MUI to Modus component mappings")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "mui_migration",
            "mapping",
            "component_mappings.json"
        )
        
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
            
        return json.dumps(mapping_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading MUI component mappings: {e}")
        return json.dumps({"error": f"Error loading MUI component mappings: {str(e)}"})


@mcp.tool()
def get_mui_migration_guide(phase: str) -> str:
    """
    Get detailed guidance for a specific MUI migration phase
    
    Args:
        phase: The migration phase name ("analyze", "migrate", "verify", "log", or "workflow")
    
    Returns:
        Markdown string with phase-specific guidance for MUI migration
    
    Example:
        >>> get_mui_migration_guide("analyze")
        >>> get_mui_migration_guide("workflow")
    """
    logger.info(f"Retrieving MUI migration guide for phase: {phase}")
    
    valid_phases = ["analyze", "migrate", "verify", "log", "workflow"]
    
    if phase.lower() not in valid_phases:
        return json.dumps({
            "error": f"Invalid phase '{phase}'. Valid phases are: {', '.join(valid_phases)}"
        })
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(
            script_dir,
            "mui_migration",
            "md_prompts",
            f"{phase.lower()}_mui.md"
        )
        
        with open(guide_path, "r") as f:
            guide_content = f.read()
            
        return guide_content
        
    except Exception as e:
        logger.error(f"Error loading MUI phase guide for {phase}: {e}")
        return json.dumps({"error": f"Error loading MUI phase guide: {str(e)}"})


@mcp.tool()
def get_connect_ui_component_mapping() -> str:
    """
    Get the complete mapping between Connect UI components and Modus V2 web components
    
    This includes detailed property mappings, migration notes, and event mappings
    for each Connect UI component.
    
    Returns:
        JSON string with comprehensive Connect UI to Modus migration data
    
    Example:
        >>> get_connect_ui_component_mapping()
    """
    logger.info("Retrieving Connect UI to Modus component mappings")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "connect_migration",
            "component_analysis",
            "connect_ui_to_modus_mapping.json"
        )
        
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
            
        return json.dumps(mapping_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading Connect UI component mappings: {e}")
        return json.dumps({"error": f"Error loading Connect UI component mappings: {str(e)}"})


@mcp.tool()
def get_connect_migration_guide(phase: str) -> str:
    """
    Get detailed guidance for a specific Connect UI migration phase
    
    Args:
        phase: The migration phase name ("analyze", "migrate", "verify", "log", or "workflow")
    
    Returns:
        Markdown string with phase-specific guidance for Connect UI migration
    
    Example:
        >>> get_connect_migration_guide("migrate")
    """
    logger.info(f"Retrieving Connect UI migration guide for phase: {phase}")
    
    valid_phases = ["analyze", "migrate", "verify", "log", "workflow"]
    
    if phase.lower() not in valid_phases:
        return json.dumps({
            "error": f"Invalid phase '{phase}'. Valid phases are: {', '.join(valid_phases)}"
        })
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(
            script_dir,
            "connect_migration",
            "docs",
            f"{phase.lower()}_connect.md"
        )
        
        with open(guide_path, "r") as f:
            guide_content = f.read()
            
        return guide_content
        
    except Exception as e:
        logger.error(f"Error loading Connect UI phase guide for {phase}: {e}")
        return json.dumps({"error": f"Error loading Connect UI phase guide: {str(e)}"})


@mcp.tool()
def get_modus_v1_to_v2_mapping() -> str:
    """
    Get the complete mapping between Modus V1 and Modus V2 web components
    
    This includes which V1 components have V2 equivalents and which are deprecated.
    
    Returns:
        JSON string with Modus V1 to V2 component mappings
    
    Example:
        >>> get_modus_v1_to_v2_mapping()
    """
    logger.info("Retrieving Modus V1 to V2 component mappings")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "component_mapping.json"
        )
        
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
            
        # Return just the mapping portion
        result = {
            "Mapping_v1_v2": mapping_data.get("Mapping_v1_v2", {}),
            "verification_rules": mapping_data.get("verification_rules", []),
            "migration_plan": mapping_data.get("migration_plan", [])
        }
            
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading Modus V1 to V2 mappings: {e}")
        return json.dumps({"error": f"Error loading Modus V1 to V2 mappings: {str(e)}"})


@mcp.tool()
def get_modus_v1_component_data(component_name: str) -> str:
    """
    Get detailed component data for a Modus V1 web component
    
    Args:
        component_name: The name of the Modus V1 component (e.g., 'button', 'alert')
                       Can be provided with or without 'modus-' prefix
    
    Returns:
        JSON string with component properties, events, and documentation
    
    Example:
        >>> get_modus_v1_component_data('button')
        >>> get_modus_v1_component_data('modus-alert')
    """
    logger.info(f"Retrieving Modus V1 component data for: {component_name}")
    
    # Standardize component name
    if not component_name.startswith("modus-"):
        component_name = f"modus-{component_name}"
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        v1_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "v1_components.json"
        )
        
        with open(v1_path, "r") as f:
            v1_components = json.load(f)
        
        # Try to find the component
        v1_file = f"{component_name}.js"
        component_data = v1_components.get(v1_file)
        
        if not component_data:
            # Try flexible matching
            for key in v1_components.keys():
                if component_name.lower() in key.lower():
                    component_data = v1_components[key]
                    v1_file = key
                    break
        
        if not component_data:
            available_components = [
                key.replace("modus-", "").replace(".js", "")
                for key in v1_components.keys()
                if key.startswith("modus-")
            ]
            return json.dumps({
                "error": f"Component '{component_name}' not found",
                "available_components": sorted(available_components)
            })
        
        result = {
            "component_name": component_name,
            "file": v1_file,
            "props": component_data.get("props", []),
            "events": component_data.get("events", []),
            "slots": component_data.get("slots", []),
            "documentation": component_data.get("documentation", "")
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error loading Modus V1 component data: {e}")
        return json.dumps({"error": f"Error loading Modus V1 component data: {str(e)}"})


@mcp.tool()
def get_migration_system_overview() -> str:
    """
    Get an overview of all available migration systems and their capabilities
    
    Returns:
        JSON string with information about all four migration systems:
        - Shadcn UI → Modus V2
        - Material UI (MUI) → Modus V2
        - Connect UI → Modus V2
        - Modus V1 → Modus V2
    
    Example:
        >>> get_migration_system_overview()
    """
    logger.info("Providing migration system overview")
    
    overview = {
        "migration_systems": [
            {
                "name": "shadcn/ui to Modus V2",
                "description": "Migrate shadcn/ui (React + Radix UI + Tailwind) components to Modus V2 web components",
                "components_covered": "42+ shadcn components",
                "key_challenges": [
                    "Tailwind CSS conversion",
                    "Radix UI primitive mapping",
                    "Copy-paste component model",
                    "Composition patterns"
                ],
                "tools_available": [
                    "get_shadcn_component_mapping()",
                    "get_migration_workflow_guide()",
                    "get_migration_phase_guide(phase)",
                    "get_shadcn_to_modus_migration_data(component)"
                ]
            },
            {
                "name": "Material UI (MUI) to Modus V2",
                "description": "Migrate Material UI React components to Modus V2 web components",
                "components_covered": "40+ MUI components",
                "key_challenges": [
                    "Theme system conversion",
                    "sx prop handling",
                    "Style overrides",
                    "Component variants"
                ],
                "tools_available": [
                    "get_mui_component_mapping()",
                    "get_mui_migration_guide(phase)"
                ]
            },
            {
                "name": "Connect UI to Modus V2",
                "description": "Migrate Connect UI (Trimble internal) components to Modus V2",
                "components_covered": "50+ Connect UI components",
                "key_challenges": [
                    "Custom component patterns",
                    "Internal dependencies",
                    "Event handler mapping",
                    "Slot-based composition"
                ],
                "tools_available": [
                    "get_connect_ui_component_mapping()",
                    "get_connect_migration_guide(phase)"
                ]
            },
            {
                "name": "Modus V1 to Modus V2",
                "description": "Upgrade from Modus V1 web components to Modus V2",
                "components_covered": "All Modus V1 components",
                "key_challenges": [
                    "Breaking API changes",
                    "Deprecated components",
                    "Property renames",
                    "Event updates"
                ],
                "tools_available": [
                    "get_modus_v1_to_v2_mapping()",
                    "get_modus_v1_component_data(component)",
                    "get_modus_component_data(component)"
                ]
            }
        ],
        "common_tools": [
            "get_modus_component_data(component) - Get Modus V2 component specs",
            "list_all_modus_components() - List all Modus V2 components"
        ],
        "migration_workflow": [
            "Phase 1: Analyze - Identify components and migration strategies",
            "Phase 2: Migrate - Transform components to Modus V2",
            "Phase 3: Verify - Validate correctness and best practices",
            "Phase 4: Log - Generate reports and consolidate results"
        ]
    }
    
    return json.dumps(overview, indent=2)


# Execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
