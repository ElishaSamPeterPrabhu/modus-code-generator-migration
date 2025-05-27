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
migration_mcp = FastMCP("Migration Process Server")

print("FastMCP instance created. Registering tools...")

# --- MCP Tools ---


@migration_mcp.tool()
def get_analysis_flow(
    file_content: str,
    additional_info: str = None,
    save_analysis: bool = False,
) -> str:
    """
    Analyze the provided file content for Modus-v1 component usage.

    • When `save_analysis` is False (default) → returns a preview containing the analysis
      report and instructions from `md_prompts/analysis.md` (if present), plus a prompt
      telling the agent/user to reply "save" to persist.
    • When `save_analysis` is True  → writes `analysis_report.json` in the project root
      and confirms completion.
    """

    logger.info(f"Analyzing code for migration (content length: {len(file_content)})")
    if additional_info:
        logger.info(f"Additional analysis info: {additional_info}")
    # Load v1 component data and mapping
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        v1_path = os.path.join(
            script_dir,
            "..",
            "modus_migration",
            "component_analysis",
            "v1_components.json",
        )
        mapping_path = os.path.join(
            script_dir,
            "..",
            "modus_migration",
            "component_analysis",
            "component_mapping.json",
        )
        with open(v1_path, "r") as f:
            v1_components_data = json.load(f)
        with open(mapping_path, "r") as f:
            component_mapping_data = json.load(f).get("Mapping_v1_v2", {})
    except Exception as e:
        analysis_results = {
            "lines_of_code": len(file_content.splitlines()),
            "identified_v1_components": [],
            "migration_suggestions": [],
            "status": "Analysis Pending",
            "error": f"Failed to load component data: {str(e)}",
        }
        analysis_results["status"] = "Analysis Failed - Component Data"
        logger.error(f"Component data load failed: {e}")
        return json.dumps(analysis_results, indent=2)
    analysis_results = {
        "lines_of_code": len(file_content.splitlines()),
        "identified_v1_components": [],
        "migration_suggestions": [],
        "status": "Analysis Pending",
        "error": None,
    }
    try:
        identified_v1_components_details = {}
        v1_component_names = [
            k.replace("modus-", "").replace(".js", "")
            for k in v1_components_data.keys()
            if k.startswith("modus-")
        ]
        for comp_name in v1_component_names:
            count = 0  # Initialize count for each component
            v1_tag = f"modus-{comp_name}"
            occurrences = re.findall(f"<{v1_tag}[^>]*>", file_content)

            if occurrences:
                count = len(occurrences)
                if v1_tag not in identified_v1_components_details:
                    identified_v1_components_details[v1_tag] = {
                        "count": 0,  # Initialize here as well for safety
                        "v2_equivalent": "N/A",
                    }
                identified_v1_components_details[v1_tag]["count"] += count

                v2_mapping = component_mapping_data.get(v1_tag)
                v2_component_name = (
                    v2_mapping
                    if v2_mapping and v2_mapping != "Not Found"
                    else "Not Found"
                )

                identified_v1_components_details[v1_tag][
                    "v2_equivalent"
                ] = v2_component_name

                analysis_results["migration_suggestions"].append(
                    f"Consider migrating '{v1_tag}' (found {count} times) to '{v2_component_name}'."
                )
            else:
                analysis_results["migration_suggestions"].append(
                    f"Component '{v1_tag}' (found {count} times) has no direct v2 mapping in component_mapping.json."
                )
        analysis_results["identified_v1_components"] = [
            {"name": k, "count": v["count"], "v2_equivalent": v["v2_equivalent"]}
            for k, v in identified_v1_components_details.items()
        ]
        analysis_results["status"] = "Analysis Complete"
    except Exception as e:
        logger.error(f"Error during component analysis: {str(e)}")
        analysis_results["error"] = f"Component analysis failed: {str(e)}"
        analysis_results["status"] = "Analysis Failed - Component Scan"
        # Keep any partial results we gathered before the error

    # Always try to load analysis.md instructions
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        analysis_md_path = os.path.join(script_dir, "..", "md_prompts", "analysis.md")
        with open(analysis_md_path, "r", encoding="utf-8") as f:
            analysis_md = f.read()
    except Exception as e:
        logger.warning(f"Could not load analysis.md: {e}")
        analysis_md = ""

    # Set appropriate prompt based on analysis status
    if analysis_results["error"]:
        prompt = f"Analysis encountered an error but produced partial results. {analysis_results['error']}. Reply 'save' to persist or 'proceed' to continue migration."
    else:
        prompt = "Review analysis. Reply 'save' to persist or 'proceed' to continue migration."

    analysis_file_path = "analysis_report.json"

    if save_analysis:
        try:
            with open(analysis_file_path, "w") as f_out:
                json.dump(analysis_results, f_out, indent=2)
            status_msg = f"Analysis saved to {analysis_file_path}"
            status = "Saved"
        except Exception as e:
            status_msg = f"Failed to save analysis: {str(e)}"
            status = "SaveFailed"
        return json.dumps(
            {
                "status": status,
                "message": status_msg,
                "analysis_file": analysis_file_path if status == "Saved" else None,
                "analysis_report": analysis_results,
            },
            indent=2,
        )
    else:
        # Preview
        return json.dumps(
            {
                "analysis_report": analysis_results,
                "analysis_md": analysis_md,
                "prompt": prompt,
            },
            indent=2,
        )


@migration_mcp.tool()
def get_all_migration_data() -> str:
    """
    Returns the complete migration dataset including all v2 component definitions, mappings, migration rules, and checklists.
    The agent should call this ONCE at the start of a migration session and cache the data for all subsequent lookups.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_path = os.path.join(
            script_dir,
            "..",
            "modus_migration",
            "component_analysis",
            "component_mapping.json",
        )
        v2_path = os.path.join(
            script_dir,
            "..",
            "modus_migration",
            "component_analysis",
            "v2_components.json",
        )
        migrate_md_path = os.path.join(
            script_dir,
            "..",
            "md_prompts",
            "migrate.md",
        )
        with open(mapping_path, "r") as f:
            mapping_data = json.load(f)
        with open(migrate_md_path, "r") as f:
            migrate_md = f.read()

        with open(v2_path, "r") as f:
            v2_components = json.load(f)
        result = {
            "component_mapping": mapping_data.get("Mapping_v1_v2", {}),
            "migration_plan": mapping_data.get("migration_plan", []),
            "v2_components": v2_components,
            "migrate_md": migrate_md,
            "prompt": "Cache this data for the entire migration session. Use it for all lookups and migration steps.",
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error loading migration data: {str(e)}"})


@migration_mcp.tool()
def get_verification_rules(
    migrated_file_content: str,
) -> str:
    """
    Provide verification guidance for agentic/AI evaluation.

    • Loads and returns the contents of `md_prompts/verify.md`, which enumerates the
      authoritative verification rules/checklist for Modus 2.0 migrations.
    • No rule evaluation is done here; that is delegated to the agentic layer or
      downstream AI that consumes this data.

    The returned JSON structure is:
        {
          "verification_report": {
              "verify_md": "<full markdown content>"
          }
        }
    """
    logger.info("Verifying migrated code using rule-based checks (no AI).")
    # In the new design we simply load verify.md for downstream consumption.
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        verify_md_path = os.path.join(
            script_dir,
            "..",
            "md_prompts",
            "verify.md",
        )
        with open(verify_md_path, "r", encoding="utf-8") as f:
            verify_md = f.read()
    except Exception as e:
        logger.error(f"Failed to load verify.md: {e}")
        verify_md = ""

    verification_rules = {"verify_md": verify_md}

    return json.dumps({"verification_report": verification_rules}, indent=2)


@migration_mcp.tool()
def log_migration_summary(
    analysis_report_json: Any = None,
    generation_report_json: Any = None,
    verification_report_json: Any = None,
    additional_info: str = None,
    save_log: bool = False,
) -> str:
    """
    Logs a summary of the entire migration process.
    Returns a final message and does not proceed further automatically.
    """
    logger.info("Logging migration summary.")
    if additional_info:
        logger.info(f"Additional log info: {additional_info}")
    log_content = {
        "summary": "Migration Process Log",
        "timestamp": str(datetime.datetime.now()),
    }
    try:
        if analysis_report_json:
            if not isinstance(analysis_report_json, str):
                analysis_report_json = json.dumps(analysis_report_json)
            log_content["analysis"] = json.loads(analysis_report_json)
        if generation_report_json:
            if not isinstance(generation_report_json, str):
                generation_report_json = json.dumps(generation_report_json)
            log_content["code_generation"] = json.loads(generation_report_json)
        if verification_report_json:
            if not isinstance(verification_report_json, str):
                verification_report_json = json.dumps(verification_report_json)
            log_content["verification"] = json.loads(verification_report_json)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing report JSON for logging: {e}")
        log_content["logging_error"] = f"Failed to parse one or more reports: {str(e)}"
    if additional_info:
        log_content["final_notes"] = additional_info

    # Load log.md instructions
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_md_path = os.path.join(script_dir, "..", "md_prompts", "log.md")
        with open(log_md_path, "r", encoding="utf-8") as f:
            log_md = f.read()
    except Exception as e:
        logger.error(f"Failed to load log.md: {e}")
        log_md = ""

    log_file_path = "migration_log.json"

    if save_log:
        try:
            with open(log_file_path, "w") as f_log:
                json.dump(log_content, f_log, indent=2)
            status_message = f"Migration summary logged to {log_file_path}"
            log_status = "Logging Complete"
        except Exception as e:
            logger.error(f"Failed to write migration log: {str(e)}")
            status_message = f"Failed to write migration log: {str(e)}"
            log_status = "Logging Failed"
        return json.dumps(
            {
                "log_file": log_file_path if log_status == "Logging Complete" else None,
                "message": status_message,
                "status": log_status,
                "prompt": "Migration summary logged. Workflow complete.",
            },
            indent=2,
        )
    else:
        # Preview mode: return content & instructions
        return json.dumps(
            {
                "log_file_suggestion": log_file_path,
                "log_content": log_content,
                "log_md": log_md,
                "prompt": "Review the proposed log. Reply 'save' to write it to migration_log.json.",
            },
            indent=2,
        )


@migration_mcp.tool()
def run_migration_workflow(
    user_input: str, file_content: str = None, previous_state: dict = None
) -> str:
    """
    Orchestrates the migration workflow in agentic mode using the new robust approach.
    Steps: analyze_file_for_migration → get_all_migration_data → get_verification_rules → log_migration_summary
    """
    if previous_state is None or previous_state.get("step") == "start":
        analysis_report_json = get_analysis_flow(
            file_content=file_content, save_analysis=False
        )
        analysis_report_data = json.loads(analysis_report_json)
        return json.dumps(
            {
                "step": "analysis",
                "analysis_report": analysis_report_data,
                "prompt": "Analysis complete. Reply 'proceed' to continue to migration data generation.",
                "file_content": file_content,
            }
        )
    elif previous_state.get("step") == "analysis" and user_input.lower() in [
        "proceed",
        "migrate",
        "yes",
    ]:
        migration_data_json = get_all_migration_data()
        migration_data = json.loads(migration_data_json)
        return json.dumps(
            {
                "step": "migration_data",
                "migration_data": migration_data,
                "prompt": "Migration data ready. Reply 'verify' to verify migrated code.",
                "file_content": previous_state["file_content"],
                "analysis_report": previous_state["analysis_report"],
                "verification_rules": migration_data.get("verification_rules", []),
            }
        )
    elif (
        previous_state.get("step") == "migration_data"
        and user_input.lower() == "verify"
    ):
        migrated_file_content = previous_state.get("migrated_file_content", "")
        verification_rules = previous_state.get("verification_rules", [])
        verification_report_json = get_verification_rules(
            migrated_file_content=migrated_file_content,
            verification_rules=verification_rules,
        )
        verification_report_data = json.loads(verification_report_json)
        return json.dumps(
            {
                "step": "verification",
                "verification_report": verification_report_data,
                "prompt": "Verification complete. Reply 'log' to log the migration summary.",
                "file_content": previous_state["file_content"],
                "analysis_report": previous_state["analysis_report"],
                "migration_data": previous_state["migration_data"],
                "verification_rules": verification_rules,
            }
        )
    elif previous_state.get("step") == "verification" and user_input.lower() == "log":
        preview_json = log_migration_summary(
            analysis_report_json=previous_state["analysis_report"],
            generation_report_json=previous_state["migration_data"],
            verification_report_json=previous_state["verification_report"],
            save_log=False,
        )
        preview_data = json.loads(preview_json)
        return json.dumps(
            {
                "step": "log_preview",
                "log_preview": preview_data,
                "analysis_report": previous_state["analysis_report"],
                "migration_data": previous_state["migration_data"],
                "verification_report": previous_state["verification_report"],
                "prompt": preview_data["prompt"],
            }
        )
    elif previous_state.get("step") == "log_preview" and user_input.lower() == "save":
        final_json = log_migration_summary(
            analysis_report_json=previous_state["analysis_report"],
            generation_report_json=previous_state["migration_data"],
            verification_report_json=previous_state["verification_report"],
            save_log=True,
        )
        final_data = json.loads(final_json)
        return json.dumps(
            {
                "step": "logged",
                "log_report": final_data,
                "prompt": final_data["prompt"],
            }
        )
    elif previous_state.get("step") == "analysis" and user_input.lower() == "save":
        if (
            "file_content" not in previous_state
            or "analysis_report" not in previous_state
        ):
            error_payload = {
                "error": "Invalid previous_state for saving analysis. Missing 'file_content' or 'analysis_report'.",
                "step": "error",
                "expected_fields_in_previous_state": [
                    "step",
                    "analysis_report",
                    "prompt",
                    "file_content",
                ],
                "previous_state_received": previous_state,  # Echo back what was received for debugging
            }
            logger.error(
                f"Invalid previous_state for 'save' analysis: {json.dumps(error_payload)}"
            )
            return json.dumps(error_payload, indent=2)

        saved_json = get_analysis_flow(
            file_content=previous_state["file_content"], save_analysis=True
        )
        saved_data = json.loads(saved_json)
        return json.dumps(
            {
                "step": "analysis_saved",
                "analysis_saved": saved_data,
                "analysis_report": previous_state["analysis_report"],
                "prompt": "Analysis saved. Reply 'proceed' to continue to migration data generation.",
                "file_content": previous_state["file_content"],
            }
        )
    else:
        return json.dumps(
            {
                "step": previous_state.get("step", "start"),
                "prompt": "Please reply with 'proceed', 'verify', or 'log' as appropriate.",
                "file_content": previous_state.get("file_content"),
                "analysis_report": previous_state.get("analysis_report"),
                "migration_data": previous_state.get("migration_data"),
                "verification_report": previous_state.get("verification_report"),
            }
        )


if __name__ == "__main__":
    print("Starting migration server...")
    migration_mcp.run(transport="stdio")
