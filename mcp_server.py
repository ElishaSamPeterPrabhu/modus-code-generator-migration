from mcp.server.fastmcp import FastMCP
import json
import logging
import os
import re
from typing import Dict, Any, List

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
                    if isinstance(prop, dict) and prop.get("description"):
                        description = (
                            f"A component that supports {prop.get('description')}"
                        )
                        break

            # Get component capabilities based on props and events
            capabilities = []

            # Add prop-based capabilities
            for prop in data.get("props", []):
                # Ensure prop is a dictionary before accessing its properties
                if not isinstance(prop, dict):
                    continue

                prop_name = prop.get("name", "")
                if prop_name:
                    capabilities.append(f"Can be configured with '{prop_name}'")

            # Add event-based capabilities
            for event in data.get("events", []):
                # Ensure event is a dictionary before accessing its properties
                if not isinstance(event, dict):
                    continue

                event_name = event.get("name", "")
                if event_name:
                    capabilities.append(f"Emits '{event_name}' event")

            # Add slot-based capabilities
            for slot in data.get("slots", []):
                # Ensure slot is a dictionary before accessing its properties
                if not isinstance(slot, dict):
                    continue

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

    # Possible filenames for the component - try multiple variations
    possible_files = [
        f"{tag_prefix}{component_name}{file_extension}",
        f"{tag_prefix}{component_name}",
        f"{component_name}{file_extension}",
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
    found_key = None

    # 1. Try exact match
    for file_name in possible_files:
        if file_name in components_data:
            component_data = components_data[file_name]
            found_key = file_name
            break

    # 2. Try case-insensitive match
    if not component_data:
        for data_key in components_data.keys():
            for pattern in possible_files:
                if data_key.lower() == pattern.lower():
                    component_data = components_data[data_key]
                    found_key = data_key
                    break
            if component_data:
                break

    # 3. Try substring match
    if not component_data:
        for data_key in components_data.keys():
            # Check if component_name is part of any key
            if component_name.lower() in data_key.lower():
                component_data = components_data[data_key]
                found_key = data_key
                break

    if not component_data:
        available_components = []
        for file_key in components_data.keys():
            if file_key.startswith(tag_prefix):
                component = file_key.replace(tag_prefix, "").replace(file_extension, "")
                available_components.append(component)
            # Also check for components without the standard prefix/extension
            elif component_name.lower() in file_key.lower():
                component = file_key.replace(file_extension, "")
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
        "found_key": found_key,  # Include the actual key found for debugging
        "version": version,
        "props": component_data.get("props", []),
        "events": component_data.get("events", []),
        "slots": component_data.get("slots", []),
        "documentation": component_data.get("documentation", ""),
    }

    return json.dumps(result, indent=2)


@mcp.tool()
def get_migration_guide() -> str:
    """
    Get migration guidance for converting Modus 1.0 components to Modus 2.0

    This function provides guidance on how to approach the migration process.
    It encourages the agent to identify specific components needing migration
    and then request detailed migration data for those components.

    Returns:
        JSON string with migration guidance
    """
    logger.info("Providing migration guidance")

    # Load migration plan and verification rules
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "component_mapping.json",
        )

        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)

    except Exception as e:
        logger.error(f"Error loading migration guidance: {e}")
        return json.dumps({"error": f"Error loading migration guidance: {str(e)}"})

    # Format the migration guidance
    migration_guide = {
        "migration_workflow": [
            "1. Identify which Modus 1.0 components need to be migrated using list_components(version='1.0')",
            "2. Check which Modus 2.0 components are available using list_components(version='2.0')",
            "3. For each component to migrate, request specific migration data using get_component_migration_data(component_name)",
            "4. Check the 'related_components' section to discover components that might be used together or nested inside each other",
            "5. Request migration data for any related components as needed based on the suggestions",
            "6. If there is a component that is available in version 1.0 but not in version 2.0, add a comment on top of the component that its not available in version 2.0",
            "7. If there is a component whose features are not available in version 2.0, add a comment that the feature is not available in version 2.0, do it even if multiple features are missing, then migrate what is available",
            "8. Apply the migration rules from the verification rules and migration plan",
        ],
        "verification_rules": mapping_data.get("verification_rules", []),
        "migration_plan": mapping_data.get("migration_plan", []),
        "common_components": [
            "button",
            "alert",
            "badge",
            "card",
            "checkbox",
            "chip",
            "modal",
            "navbar",
            "select",
            "switch",
            "table",
            "tabs",
        ],
        "relationship_discovery": "The system dynamically discovers component relationships by analyzing documentation and examples. No predefined relationships are used - all discoveries are made at runtime.",
        "example_request": "To migrate a component, first call get_component_migration_data('component_name'), then check the related_components section to discover other components that might be used with it.",
    }

    return json.dumps(migration_guide, indent=2)


@mcp.tool()
def get_component_migration_data(component_name: str) -> str:
    """
    Get migration data for a specific component

    This function retrieves data needed to migrate a specific component from
    Modus 1.0 to Modus 2.0, including definitions for both versions and mapping information.

    Args:
        component_name: The name of the component to get migration data for (e.g., 'button', 'alert')

    Returns:
        JSON string with component-specific migration data
    """
    logger.info(f"Getting migration data for component: {component_name}")

    # Standardize component name (remove any prefix)
    if component_name.startswith("modus-"):
        component_name = component_name.replace("modus-", "")
    elif component_name.startswith("modus-wc-"):
        component_name = component_name.replace("modus-wc-", "")

    # Load required data
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "component_mapping.json",
        )
        v1_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", "v1_components.json"
        )
        v2_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", "v2_components.json"
        )

        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)

        with open(v1_path, "r") as f:
            v1_components = json.load(f)

        with open(v2_path, "r") as f:
            v2_components = json.load(f)

    except Exception as e:
        logger.error(f"Error loading component data: {e}")
        return json.dumps({"error": f"Error loading component data: {str(e)}"})

    # Get v1 component data with improved lookup
    v1_tag = f"modus-{component_name}"
    v1_file = f"{v1_tag}.js"
    v1_component_data = v1_components.get(v1_file, {})

    if not v1_component_data:
        # Try alternative formats with more flexible matching
        for key in v1_components.keys():
            if component_name.lower() in key.lower():
                v1_component_data = v1_components[key]
                v1_file = key
                break

    # Get v2 component data with improved lookup
    v2_tag = f"modus-wc-{component_name}"
    v2_file = f"{v2_tag}.tsx"
    v2_component_data = v2_components.get(v2_file, {})

    if not v2_component_data:
        # Try alternative formats with more flexible matching
        for key in v2_components.keys():
            if component_name.lower() in key.lower():
                v2_component_data = v2_components[key]
                v2_file = key
                v2_tag = key.replace(".tsx", "")
                break

    # Get mapping information with improved lookup
    component_mapping = None
    for k, v in mapping_data.get("Mapping_v1_v2", {}).items():
        if (
            k == v1_tag
            or k.lower() == v1_tag.lower()
            or component_name.lower() in k.lower()
        ):
            component_mapping = {"v1_tag": k, "v2_tag": v.get("v2_component", "")}
            break

    # If still no mapping found but we have component data, create a default mapping
    if not component_mapping and (v1_component_data or v2_component_data):
        component_mapping = {"v1_tag": v1_tag, "v2_tag": v2_tag}

    # If we couldn't find any data, return an error
    if not v1_component_data and not v2_component_data:
        return json.dumps(
            {
                "error": f"Could not find component data for '{component_name}' in either version",
                "v1_file_checked": v1_file,
                "v2_file_checked": v2_file,
                "suggestion": "Try using list_components() to see available components",
            }
        )

    # Compile component migration data
    migration_data = {
        "component_name": component_name,
        "v1_component": {"tag": v1_tag, "file": v1_file, "data": v1_component_data},
        "v2_component": {"tag": v2_tag, "file": v2_file, "data": v2_component_data},
        "mapping": component_mapping,
        "migration_guidance": {
            "tag_change": f"Change {v1_tag} to {v2_tag}",
            "attribute_changes": get_attribute_mappings(
                component_name, v1_component_data, v2_component_data
            ),
        },
        "related_components": detect_related_components(
            component_name, v2_component_data, v2_components
        ),
        "verification_rules": [
            rule
            for rule in mapping_data.get("verification_rules", [])
            if "component" not in rule or rule.get("component") == component_name
        ],
    }

    return json.dumps(migration_data, indent=2)


def get_attribute_mappings(component_name, v1_data, v2_data):
    """Helper function to determine attribute mappings between v1 and v2 components"""

    # Default mappings for common components
    if component_name == "button":
        return {
            "buttonStyle": "color",
            "note": "Add aria-label attribute if not present",
        }
    elif component_name == "alert":
        return {"severity": "type"}

    # For other components, compare props and suggest mappings
    attribute_mappings = {}

    v1_props = {prop.get("name"): prop for prop in v1_data.get("props", [])}
    v2_props = {prop.get("name"): prop for prop in v2_data.get("props", [])}

    # Find props with similar names
    for v1_name, v1_prop in v1_props.items():
        if v1_name in v2_props:
            # Same name in both versions
            attribute_mappings[v1_name] = v1_name
        else:
            # Look for similar names
            for v2_name in v2_props.keys():
                if v1_name.lower() == v2_name.lower() or v1_name.replace(
                    "-", ""
                ) == v2_name.replace("-", ""):
                    attribute_mappings[v1_name] = v2_name
                    break

    return attribute_mappings


def detect_related_components(component_name, v2_component_data, v2_components):
    """Dynamically detect components that might be related to the current component"""
    related = []

    # If we have component documentation, analyze it for component references
    if (
        v2_component_data
        and isinstance(v2_component_data, dict)
        and "documentation" in v2_component_data
    ):
        doc = v2_component_data.get("documentation", "")

        # Search for component references in documentation
        for other_component in v2_components.keys():
            component_tag = other_component.replace(".tsx", "")
            if component_tag in doc and component_name not in component_tag.lower():
                # Extract the simple component name
                simple_name = component_tag.replace("modus-wc-", "")

                # Skip the component itself and avoid duplicates
                if simple_name != component_name and not any(
                    r["name"] == simple_name for r in related
                ):
                    related.append(
                        {
                            "name": simple_name,
                            "tag": component_tag,
                            "relationship": "referenced-in-docs",
                            "suggestion": f"This component is referenced in the {component_name} documentation",
                            "action": f"Consider getting data for this component with get_component_migration_data('{simple_name}')",
                        }
                    )

    # Check for common examples in storybook examples
    if (
        v2_component_data
        and isinstance(v2_component_data, dict)
        and "storybook" in v2_component_data
    ):
        examples = v2_component_data.get("storybook", {}).get("examples", [])
        for example in examples:
            if isinstance(example, str):
                # Find all component tags in the example
                tags = re.findall(r"<([^>\s]+)[^>]*>", example)
                for tag in tags:
                    if (
                        tag.startswith("modus-wc-")
                        and component_name not in tag.lower()
                    ):
                        simple_name = tag.replace("modus-wc-", "")

                        # Skip duplicates
                        if not any(r["name"] == simple_name for r in related):
                            related.append(
                                {
                                    "name": simple_name,
                                    "tag": tag,
                                    "relationship": "used-in-examples",
                                    "suggestion": f"This component appears in {component_name} examples",
                                    "action": f"Consider getting data for this component with get_component_migration_data('{simple_name}')",
                                }
                            )

    return related


@mcp.tool()
def get_migration_data() -> str:
    """
    Get complete migration dataset for all components

    This function returns the complete migration dataset including all component
    definitions for both versions, mapping rules, verification rules, and migration plan.

    For a more targeted approach, consider using get_component_migration_data(component_name)
    to get migration data for specific components.

    Returns:
        JSON string with complete migration dataset
    """
    logger.info("Providing complete migration dataset")

    # Load all migration data
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "modus_migration",
            "component_analysis",
            "component_mapping.json",
        )
        v1_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", "v1_components.json"
        )
        v2_path = os.path.join(
            script_dir, "modus_migration", "component_analysis", "v2_components.json"
        )

        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)

        with open(v1_path, "r") as f:
            v1_components = json.load(f)

        with open(v2_path, "r") as f:
            v2_components = json.load(f)

    except Exception as e:
        logger.error(f"Error loading migration data: {e}")
        return json.dumps({"error": f"Error loading migration data: {str(e)}"})

    # Compile complete migration dataset
    migration_data = {
        "component_mapping": mapping_data.get("Mapping_v1_v2", {}),
        "verification_rules": mapping_data.get("verification_rules", []),
        "migration_plan": mapping_data.get("migration_plan", []),
        "v1_components": v1_components,
        "v2_components": v2_components,
        "usage_guidance": {
            "process": "For a more targeted approach, use get_component_migration_data(component_name) to get migration data for specific components."
        },
    }

    return json.dumps(migration_data, indent=2)


# execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
