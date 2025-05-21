from mcp.server.fastmcp import FastMCP
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Modus Web Components Server")


@mcp.tool()
def list_components(version: str = "2.0") -> str:
    """
    Lists all available web components with descriptions of their functionality

    Args:
        version: The version of Modus components to list ("1.0" or "2.0")

    Returns:
        JSON string with component names and descriptions

    Example:
        >>> list_components()
        >>> list_components(version="1.0")
    """
    logger.info(f"Listing all available components for version {version}")

    # Determine which file to load based on version
    file_name = "v1_components.json" if version == "1.0" else "v2_components.json"
    component_key = "v1_components" if version == "1.0" else "v2_components"
    tag_prefix = "modus-" if version == "1.0" else "modus-wc-"
    file_extension = ".js" if version == "1.0" else ".tsx"

    # Load components file from the modus_migration/component_analysis folder
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", file_name
        )

        with open(data_path, "r") as f:
            components_data = json.load(f)
            logger.info(f"Loaded {file_name} with {len(components_data)} components")
    except Exception as e:
        logger.error(f"Error loading {file_name}: {e}")
        return json.dumps({"error": f"Error loading component data: {str(e)}"})

    components = []

    # Extract component information
    for file_name, data in components_data.items():
        if file_name.startswith(tag_prefix):
            component_name = file_name.replace(tag_prefix, "").replace(
                file_extension, ""
            )

            # Get component description from documentation or first prop description
            description = data.get("documentation", "")
            if not description and data.get("props") and len(data["props"]) > 0:
                for prop in data["props"]:
                    if prop.get("description"):
                        description = (
                            f"A component that supports {prop.get('description')}"
                        )
                        break

            # Get component capabilities based on props and events
            capabilities = []

            # Add prop-based capabilities
            for prop in data.get("props", []):
                prop_name = prop.get("name", "")
                if prop_name:
                    capabilities.append(f"Can be configured with '{prop_name}'")

            # Add event-based capabilities
            for event in data.get("events", []):
                event_name = event.get("name", "")
                if event_name:
                    capabilities.append(f"Emits '{event_name}' event")

            # Add slot-based capabilities
            for slot in data.get("slots", []):
                slot_name = slot.get("name", "")
                if slot_name:
                    if slot_name == "default":
                        capabilities.append("Accepts content in default slot")
                    else:
                        capabilities.append(f"Accepts content in '{slot_name}' slot")

            components.append(
                {
                    "name": component_name,
                    "tag_name": f"{tag_prefix}{component_name}",
                    "version": version,
                    "description": description,
                    "capabilities": capabilities[
                        :5
                    ],  # Limit to 5 capabilities to avoid overwhelming
                }
            )

    # Sort components by name
    components.sort(key=lambda x: x["name"])

    result = {
        "components": components,
        "total_count": len(components),
        "version": version,
    }

    return json.dumps(result, indent=2)


@mcp.tool()
def generate_component(component_name: str, version: str = "2.0") -> str:
    """
    Extract component data from v1_components.json or v2_components.json for the requested web component

    Args:
        component_name: The name of the component (e.g., 'button', 'alert', 'autocomplete')
        version: The version of Modus components to use ("1.0" or "2.0")

    Returns:
        JSON string with component properties, events, and other metadata

    Example:
        >>> generate_component('button')
        >>> generate_component('button', version="1.0")
    """
    logger.info(f"Extracting data for component: {component_name} (version {version})")

    # Determine which file to load based on version
    file_name = "v1_components.json" if version == "1.0" else "v2_components.json"
    tag_prefix = "modus-" if version == "1.0" else "modus-wc-"
    file_extension = ".js" if version == "1.0" else ".tsx"

    # Possible filenames for the component
    possible_files = [
        f"{tag_prefix}{component_name}{file_extension}",
    ]

    # Load components file from the modus_migration/component_analysis folder
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", file_name
        )

        with open(data_path, "r") as f:
            components_data = json.load(f)
            logger.info(f"Loaded {file_name} with {len(components_data)} components")
    except Exception as e:
        logger.error(f"Error loading {file_name}: {e}")
        return json.dumps({"error": f"Error loading component data: {str(e)}"})

    # Find component data
    component_data = None
    for file_name in possible_files:
        if file_name in components_data:
            component_data = components_data[file_name]
            break

    if not component_data:
        # Try case-insensitive search
        for file_name, data in components_data.items():
            if file_name.lower() in [f.lower() for f in possible_files]:
                component_data = data
                break

    if not component_data:
        available_components = []
        for file_name in components_data.keys():
            if file_name.startswith(tag_prefix):
                component = file_name.replace(tag_prefix, "").replace(
                    file_extension, ""
                )
                available_components.append(component)

        return json.dumps(
            {
                "error": f"Component '{component_name}' not found in {file_name}",
                "available_components": sorted(available_components),
                "tip": f"Use list_components(version='{version}') to see all available components with descriptions",
            }
        )

    # Return component data
    tag_name = f"{tag_prefix}{component_name}"

    result = {
        "component_name": component_name,
        "tag_name": tag_name,
        "version": version,
        "props": component_data.get("props", []),
        "events": component_data.get("events", []),
        "slots": component_data.get("slots", []),
        "documentation": component_data.get("documentation", ""),
    }

    return json.dumps(result, indent=2)


# execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
