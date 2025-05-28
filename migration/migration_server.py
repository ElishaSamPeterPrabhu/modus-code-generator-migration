from mcp.server.fastmcp import FastMCP
import json
import logging
import os
import re
from typing import Any
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
migration_mcp = FastMCP("Modus Migration Data Provider")

print("FastMCP instance created. Registering tools...")

# --- MCP Tools ---


def _get_migration_data(guidance_type: str) -> dict:
    """Loads migration-related data from files based on the guidance type.

    Args:
        guidance_type: Specifies the type of guidance data to load
                       (e.g., "analyze", "migrate", "verify", "log", "workflow").

    Returns:
        A dictionary containing the requested data.
        If an error occurs, returns a dict with an 'error' key.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        loaded_data = {
            "md_prompts": {},
            "component_data": {},
            "gold_standard": None,
            "directories": {},
        }

        # Determine which MD files to load
        md_files_to_load_map = {
            "analyze": ["analyze.md"],
            "migrate": ["migrate.md"],
            "verify": ["verify.md"],
            "log": ["log.md"],
            "workflow": [
                "analyze.md",
                "migrate.md",
                "verify.md",
                "log.md",
                "workflow.md",
            ],
        }
        md_files_to_load = md_files_to_load_map.get(guidance_type, [])

        if md_files_to_load:
            md_prompts_dir = os.path.join(script_dir, "..", "md_prompts")
            for md_file_name in md_files_to_load:
                md_path = os.path.join(md_prompts_dir, md_file_name)
                key = md_file_name.replace(".md", "")
                if os.path.exists(md_path):
                    with open(md_path, "r", encoding="utf-8") as f:
                        loaded_data["md_prompts"][key] = f.read()
                else:
                    logger.warning(
                        f"Markdown file not found for {guidance_type}: {md_path}"
                    )
                    loaded_data["md_prompts"][key] = f"{md_file_name} not found."

        # Load component data if needed
        if guidance_type in ["analyze", "migrate", "verify", "workflow"]:
            component_analysis_dir = os.path.join(
                script_dir, "..", "modus_migration", "component_analysis"
            )
            component_mapping_path = os.path.join(
                component_analysis_dir, "component_mapping.json"
            )
            v1_components_path = os.path.join(
                component_analysis_dir, "v1_components.json"
            )
            v2_components_path = os.path.join(
                component_analysis_dir, "v2_components.json"
            )

            if os.path.exists(component_mapping_path):
                with open(component_mapping_path, "r") as f:
                    loaded_data["component_data"]["component_mapping"] = json.load(f)
            else:
                logger.warning(
                    f"Component mapping file not found for {guidance_type}: {component_mapping_path}"
                )

            if os.path.exists(v1_components_path):
                with open(v1_components_path, "r") as f:
                    loaded_data["component_data"]["v1_components"] = json.load(f)
            else:
                logger.warning(
                    f"V1 components file not found for {guidance_type}: {v1_components_path}"
                )

            if os.path.exists(v2_components_path):
                with open(v2_components_path, "r") as f:
                    loaded_data["component_data"]["v2_components"] = json.load(f)
            else:
                logger.warning(
                    f"V2 components file not found for {guidance_type}: {v2_components_path}"
                )

        # Load gold standard if needed
        if guidance_type in ["verify", "workflow"]:
            gold_standard_path = os.path.join(script_dir, "gold_standard.md")
            if os.path.exists(gold_standard_path):
                with open(gold_standard_path, "r", encoding="utf-8") as f:
                    loaded_data["gold_standard"] = f.read()
            else:
                logger.warning(
                    f"Gold standard file not found for {guidance_type}: {gold_standard_path}"
                )
                loaded_data["gold_standard"] = "Gold_standard.md not found."

        # Define and ensure directories exist if needed
        if guidance_type in ["analyze", "workflow"]:
            analysis_reports_path = os.path.join(script_dir, "..", "analysis_reports")
            loaded_data["directories"]["analysis_reports"] = analysis_reports_path
            if not os.path.exists(analysis_reports_path):
                os.makedirs(analysis_reports_path)

        if guidance_type in ["log", "workflow"]:
            migration_logs_path = os.path.join(script_dir, "..", "migration_logs")
            loaded_data["directories"]["migration_logs"] = migration_logs_path
            if not os.path.exists(migration_logs_path):
                os.makedirs(migration_logs_path)

        if guidance_type == "workflow":
            workflow_md_key = (
                "workflow"  # Key for workflow.md in loaded_data["md_prompts"]
            )
            if workflow_md_key in loaded_data["md_prompts"]:
                workflow_content = loaded_data["md_prompts"][workflow_md_key]
                # Check if the content is not the "not found" message
                if "not found" not in workflow_content.lower():
                    primary_directive = (
                        "- **PRIMARY DIRECTIVE: The agent MUST meticulously read and STRICTLY ADHERE to ALL rules, "
                        "instructions, output formats, and interaction protocols detailed within the specific markdown files "
                        "(`analyze.md`, `migrate.md`, `verify.md`, `log.md`) for each migration step. "
                        "Deviation from these authoritative documents is not permitted. This is the paramount rule.**"
                    )

                    rules_header_marker = "## Rules"
                    lines = workflow_content.splitlines()
                    insertion_line_index = -1
                    for i, line in enumerate(lines):
                        if line.strip() == rules_header_marker:
                            insertion_line_index = (
                                i + 1
                            )  # Insert on the line after "## Rules"
                            break

                    if insertion_line_index != -1:
                        lines.insert(insertion_line_index, primary_directive)
                        loaded_data["md_prompts"][workflow_md_key] = "\n".join(lines)
                    else:
                        # Log a warning if the '## Rules' section isn't found, so the directive isn't added.
                        logger.warning(
                            f"'{workflow_md_key}.md': '{rules_header_marker}' section not found. "
                            "Primary directive was not added."
                        )

        logger.info(
            f"Selective migration data loaded for guidance_type='{guidance_type}'."
        )
        return loaded_data

    except Exception as e:
        logger.error(
            f"Failed to load migration data for guidance_type='{guidance_type}': {e}"
        )
        return {"error": str(e)}


@migration_mcp.tool()
def get_analyze_guidance() -> str:
    """Return guidance for the 'Analyze' step, including analyze.md, component data, and relevant directory paths.

    Returned JSON structure:
    {
      "guidance_text": "...content of analyze.md...",
      "component_data": { ...component_mapping, v1_components, v2_components... },
      "directories": { "analysis_reports": "path/to/analysis_reports" }
    }
    """
    migration_data = _get_migration_data(guidance_type="analyze")
    if "error" in migration_data:
        return json.dumps(
            {
                "error": True,
                "message": f"Failed to load migration data for 'analyze' step: {migration_data.get('error', 'Unknown error')}",
            }
        )
    return json.dumps(
        {
            "guidance_text": migration_data.get("md_prompts", {}).get(
                "analyze", "Analyze.md not found."
            ),
            "component_data": migration_data.get("component_data", {}),
            "directories": {
                "analysis_reports": migration_data.get("directories", {}).get(
                    "analysis_reports", ""
                )
            },
        },
        indent=2,
    )


@migration_mcp.tool()
def get_migrate_guidance() -> str:
    """Return guidance for the 'Migrate' step, including migrate.md and component data.

    Returned JSON structure:
    {
      "guidance_text": "...content of migrate.md...",
      "component_data": { ...component_mapping, v1_components, v2_components... }
    }
    """
    migration_data = _get_migration_data(guidance_type="migrate")
    if "error" in migration_data:
        return json.dumps(
            {
                "error": True,
                "message": f"Failed to load migration data for 'migrate' step: {migration_data.get('error', 'Unknown error')}",
            }
        )
    return json.dumps(
        {
            "guidance_text": migration_data.get("md_prompts", {}).get(
                "migrate", "Migrate.md not found."
            ),
            "component_data": migration_data.get("component_data", {}),
        },
        indent=2,
    )


@migration_mcp.tool()
def get_verify_guidance() -> str:
    """Return guidance for the 'Verify' step, including verify.md, component data, and the gold standard.

    Returned JSON structure:
    {
      "guidance_text": "...content of verify.md...",
      "component_data": { ...component_mapping, v1_components, v2_components... },
      "gold_standard": "...content of gold_standard.md..."
    }
    """
    migration_data = _get_migration_data(guidance_type="verify")
    if "error" in migration_data:
        return json.dumps(
            {
                "error": True,
                "message": f"Failed to load migration data for 'verify' step: {migration_data.get('error', 'Unknown error')}",
            }
        )
    return json.dumps(
        {
            "guidance_text": migration_data.get("md_prompts", {}).get(
                "verify", "Verify.md not found."
            ),
            "component_data": migration_data.get("component_data", {}),
            "gold_standard": migration_data.get(
                "gold_standard", "Gold_standard.md not found."
            ),
        },
        indent=2,
    )


@migration_mcp.tool()
def get_log_guidance() -> str:
    """Return guidance for the 'Log' step, including log.md and relevant directory paths.

    Returned JSON structure:
    {
      "guidance_text": "...content of log.md...",
      "directories": { "migration_logs": "path/to/migration_logs" }
    }
    """
    migration_data = _get_migration_data(guidance_type="log")
    if "error" in migration_data:
        return json.dumps(
            {
                "error": True,
                "message": f"Failed to load migration data for 'log' step: {migration_data.get('error', 'Unknown error')}",
            }
        )
    return json.dumps(
        {
            "guidance_text": migration_data.get("md_prompts", {}).get(
                "log", "Log.md not found."
            ),
            "directories": {
                "migration_logs": migration_data.get("directories", {}).get(
                    "migration_logs", ""
                )
            },
        },
        indent=2,
    )


@migration_mcp.tool()
def get_workflow_guidance() -> str:
    """Return the overall workflow guidance (workflow.md) and all supporting data.

    This tool provides workflow.md and also includes all other markdown prompts,
    component data, the gold standard, and directory paths for a complete overview.

    Returned JSON structure:
    {
      "workflow_specific_guidance": "...content of workflow.md...",
      "all_guidance_documents": {
        "analyze": "...markdown...",
        "migrate": "...markdown...",
        "verify": "...markdown...",
        "log": "...markdown...",
        "workflow": "...markdown..." (repeated for completeness if desired)
      },
      "component_data": { ...component_mapping, v1_components, v2_components... },
      "gold_standard": "...content of gold_standard.md...",
      "directories": { "analysis_reports": "...", "migration_logs": "..." }
    }
    """
    migration_data = _get_migration_data(guidance_type="workflow")
    if "error" in migration_data:
        return json.dumps(
            {
                "error": True,
                "message": f"Failed to load migration data for 'workflow' step: {migration_data.get('error', 'Unknown error')}",
            }
        )
    return json.dumps(
        {
            "workflow_specific_guidance": migration_data.get("md_prompts", {}).get(
                "workflow", "Workflow.md not found."
            ),
            "all_guidance_documents": migration_data.get("md_prompts", {}),
            "component_data": migration_data.get("component_data", {}),
            "gold_standard": migration_data.get("gold_standard", ""),
            "directories": migration_data.get("directories", {}),
        },
        indent=2,
    )


if __name__ == "__main__":
    print("Starting migration server with context-rich agentic workflow...")
    migration_mcp.run(transport="stdio")
