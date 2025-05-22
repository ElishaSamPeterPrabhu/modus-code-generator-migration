from mcp.server.fastmcp import FastMCP
import json
import logging
import os
import re
from typing import Dict, Any, List
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
migration_mcp = FastMCP("Migration Process Server")

# --- Helper Functions ---


def _load_json_data(filename: str) -> Dict[str, Any]:
    """Loads JSON data from the specified file in the modus_migration/component_analysis directory."""
    try:
        # Corrected path assuming migration_server.py is in the 'migration' folder
        # and the JSON files are in '../modus_migration/component_analysis/'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(
            script_dir, "..", "modus_migration", "component_analysis", filename
        )
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Error: {filename} not found at {data_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode JSON from {filename}")
        return {}
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading {filename}: {e}")
        return {}


def _get_v1_components_data() -> Dict[str, Any]:
    return _load_json_data("v1_components.json")


def _get_v2_components_data() -> Dict[str, Any]:
    return _load_json_data("v2_components.json")


def _get_component_mapping_data() -> Dict[str, Any]:
    return _load_json_data("component_mapping.json")


def _find_component_data(
    component_name_part: str,
    all_components_data: Dict[str, Any],
    expected_prefix: str,
    expected_suffix: str,
) -> Dict[str, Any]:
    """Finds component data by trying various key patterns."""
    # Try direct match with common prefixes/suffixes
    # component_name_part is assumed to be the core name e.g. "button"
    key_variations = [
        f"{expected_prefix}{component_name_part}{expected_suffix}",
        f"{expected_prefix}{component_name_part}",  # Prefix only
        f"{component_name_part}{expected_suffix}",  # Suffix only
        component_name_part,  # Raw name
    ]
    for key in key_variations:
        if key in all_components_data:
            return all_components_data[key]

    # Try case-insensitive and substring matching
    for actual_key, data in all_components_data.items():
        if component_name_part.lower() in actual_key.lower():
            return data
    return {}


# --- MCP Tools ---


@migration_mcp.tool()
def analyze_code_for_migration(file_content: str, additional_info: str = None) -> str:
    """
    Analyzes the provided file content to identify Modus v1 elements for migration.
    Returns a JSON string representing the analysis report and a prompt for user confirmation.
    """
    logger.info(f"Analyzing code for migration (content length: {len(file_content)})")
    if additional_info:
        logger.info(f"Additional analysis info: {additional_info}")
    v1_components_data = _get_v1_components_data()
    component_mapping_data = _get_component_mapping_data().get("Mapping_v1_v2", {})
    analysis_results = {
        "lines_of_code": len(file_content.splitlines()),
        "identified_v1_components": [],
        "migration_suggestions": [],
        "status": "Analysis Pending",
    }
    try:
        identified_v1_components_details = {}
        v1_component_names = [
            k.replace("modus-", "").replace(".js", "")
            for k in v1_components_data.keys()
            if k.startswith("modus-")
        ]
        for comp_name in v1_component_names:
            v1_tag = f"modus-{comp_name}"
            occurrences = re.findall(f"<{v1_tag}[^>]*>", file_content)
            if occurrences:
                count = len(occurrences)
                if v1_tag not in identified_v1_components_details:
                    identified_v1_components_details[v1_tag] = {
                        "count": 0,
                        "v2_equivalent": "N/A",
                    }
                identified_v1_components_details[v1_tag]["count"] += count
                v2_mapping = component_mapping_data.get(v1_tag)
                if v2_mapping and isinstance(v2_mapping, dict):
                    identified_v1_components_details[v1_tag]["v2_equivalent"] = (
                        v2_mapping.get("v2_component", "N/A")
                    )
                    analysis_results["migration_suggestions"].append(
                        f"Consider migrating '{v1_tag}' (found {count} times) to '{identified_v1_components_details[v1_tag]['v2_equivalent']}'."
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
        logger.error(f"Error during analysis: {str(e)}")
        analysis_results["error"] = f"Analysis failed: {str(e)}"
        analysis_results["status"] = "Analysis Failed"
    result = {
        "analysis_report": analysis_results,
        "prompt": "Analysis complete. Review the report and confirm if you want to proceed to code generation (generate_migrated_code).",
    }
    return json.dumps(result, indent=2)


@migration_mcp.tool()
def generate_migrated_code(
    original_file_content: str,
    analysis_report_json: Any = None,
    additional_info: str = None,
) -> str:
    """
    Generates migrated code by transforming the provided file content.
    Requires a valid, stringified JSON analysis report. Returns a prompt for user confirmation before verification.
    """
    logger.info(
        f"Generating migrated code (content length: {len(original_file_content)})"
    )
    if additional_info:
        logger.info(f"Additional code generation info: {additional_info}")
    if not analysis_report_json:
        return json.dumps(
            {
                "error": "No analysis_report_json provided. Please run analyze_code_for_migration first and pass its output as analysis_report_json.",
                "status": "Code Generation Blocked",
                "prompt": "Please run analyze_code_for_migration and confirm before proceeding.",
            },
            indent=2,
        )
    try:
        # Accept whatever Cursor/MCP gives: string, dict, or object
        if isinstance(analysis_report_json, str):
            analysis_report_obj = json.loads(analysis_report_json)
        else:
            analysis_report_obj = analysis_report_json
        # If the report is wrapped (from analyze_code_for_migration), extract the actual report
        if "analysis_report" in analysis_report_obj:
            analysis_report = analysis_report_obj["analysis_report"]
        else:
            analysis_report = analysis_report_obj
    except Exception as e:
        return json.dumps(
            {
                "error": f"Invalid analysis_report_json: {str(e)}. Please ensure you pass the output of analyze_code_for_migration as a string or object.",
                "status": "Code Generation Blocked",
                "prompt": "Please rerun analyze_code_for_migration and confirm before proceeding.",
            },
            indent=2,
        )
    if not analysis_report or analysis_report.get("status") != "Analysis Complete":
        return json.dumps(
            {
                "error": "Analysis report is missing or incomplete. Please rerun analyze_code_for_migration and confirm before proceeding.",
                "status": "Code Generation Blocked",
                "prompt": "Please rerun analyze_code_for_migration and confirm before proceeding.",
            },
            indent=2,
        )
    v1_components_data_full = _get_v1_components_data()
    v2_components_data_full = _get_v2_components_data()
    changes_applied = []
    try:
        migrated_content = original_file_content
        identified_components = analysis_report.get("identified_v1_components", [])
        for comp_info in identified_components:
            v1_tag_name = comp_info.get("name")
            v2_tag_name = comp_info.get("v2_equivalent")
            if v2_tag_name and v2_tag_name != "N/A":
                # Replace all occurrences of the v1 tag with the v2 tag
                migrated_content, n = re.subn(
                    f"<{v1_tag_name}(\s|>)", f"<{v2_tag_name}\\1", migrated_content
                )
                migrated_content, n2 = re.subn(
                    f"</{v1_tag_name}>", f"</{v2_tag_name}>", migrated_content
                )
                if n or n2:
                    changes_applied.append(
                        f"Replaced {v1_tag_name} with {v2_tag_name} ({n+n2} changes)"
                    )
            else:
                # No v2 equivalent, add a comment
                migrated_content = re.sub(
                    f"(<{v1_tag_name}[^>]*>)",
                    r"<!-- No v2 equivalent for this tag -->\\1",
                    migrated_content,
                )
                changes_applied.append(
                    f"No v2 equivalent for {v1_tag_name}, added comment."
                )
        result = {
            "migrated_file_content": migrated_content,
            "changes_applied": changes_applied,
            "status": "Code Generation Complete",
            "prompt": "Code generation complete. Review the migrated code and confirm if you want to proceed to verification (verify_migration_with_gold_standard).",
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps(
            {
                "error": f"Code generation failed: {str(e)}",
                "status": "Code Generation Failed",
                "prompt": "Please review the error and try again.",
            },
            indent=2,
        )


@migration_mcp.tool()
def verify_migration_with_gold_standard(
    migrated_file_content: str,
    gold_standard_content: str = None,
    additional_info: str = None,
) -> str:
    """
    Verifies the migrated code against the gold standard using AI.
    Always loads and uses gold_standard.md for verification.
    """
    logger.info("Verifying migrated code with gold standard (AI-driven).")
    # Always load gold standard from file
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gold_standard_path = os.path.join(script_dir, "gold_standard.md")
        with open(gold_standard_path, "r", encoding="utf-8") as f:
            gold_standard_content = f.read()
    except Exception as e:
        logger.error(f"Failed to load gold_standard.md: {e}")
        gold_standard_content = ""

    # --- AI-driven verification ---
    ai_prompt = (
        "You are an expert Modus Web Components reviewer. "
        "Given the following migrated code and the gold standard, "
        "evaluate if the code fully complies with the gold standard. "
        "If not, explain what is missing or incorrect.\n\n"
        "Migrated Code:\n"
        f"{migrated_file_content}\n\n"
        "Gold Standard:\n"
        f"{gold_standard_content}\n"
    )
    # Example: ai_response = call_your_llm(ai_prompt)
    ai_response = (
        "AI verification placeholder: (replace with actual LLM call and response)."
    )

    verification_result = {
        "verification_report": ai_response,
        "prompt": "Verification complete. Review the results and confirm if you want to proceed to logging the migration summary (log_migration_summary).",
    }
    return json.dumps(verification_result, indent=2)


@migration_mcp.tool()
def log_migration_summary(
    analysis_report_json: Any = None,
    generation_report_json: Any = None,
    verification_report_json: Any = None,
    additional_info: str = None,
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

    log_file_path = "migration_log.json"
    try:
        with open(log_file_path, "w") as f_log:
            json.dump(log_content, f_log, indent=2)
        status_message = f"Migration summary logged to {log_file_path}"
        log_status = "Logging Complete"
    except Exception as e:
        logger.error(f"Failed to write migration log: {str(e)}")
        status_message = f"Failed to write migration log: {str(e)}"
        log_status = "Logging Failed"

    log_result = {
        "log_file": log_file_path if log_status == "Logging Complete" else None,
        "message": status_message,
        "status": log_status,
        "prompt": "Migration summary logged. This is the final step.",
    }
    return json.dumps(log_result, indent=2)


@migration_mcp.tool()
def run_migration_workflow(
    user_input: str, file_content: str = None, previous_state: Dict[str, Any] = None
) -> str:
    """
    Orchestrates the migration workflow in agentic mode.
    Always starts with analysis, and only proceeds to the next step if the user confirms.
    The workflow state is passed as a dictionary between calls.
    """
    if previous_state is None or previous_state.get("step") == "start":
        # Step 1: Analyze
        analysis_report = analyze_code_for_migration(file_content)
        return json.dumps(
            {
                "step": "analysis",
                "analysis_report": analysis_report,
                "prompt": "Analysis complete. Reply 'proceed' to continue to code migration.",
                "file_content": file_content,
            }
        )
    elif previous_state.get("step") == "analysis" and user_input.lower() in [
        "proceed",
        "migrate",
        "yes",
    ]:
        # Step 2: Migrate
        migrated_code = generate_migrated_code(
            previous_state["file_content"],
            analysis_report_json=previous_state["analysis_report"],
        )
        return json.dumps(
            {
                "step": "migration",
                "migrated_code": migrated_code,
                "prompt": "Migration complete. Reply 'verify' to verify against the gold standard.",
                "file_content": previous_state["file_content"],
                "analysis_report": previous_state["analysis_report"],
            }
        )
    elif previous_state.get("step") == "migration" and user_input.lower() == "verify":
        # Step 3: Verify
        migrated_file_content = json.loads(previous_state["migrated_code"]).get(
            "migrated_file_content", ""
        )
        verification_report = verify_migration_with_gold_standard(
            migrated_file_content=migrated_file_content
        )
        return json.dumps(
            {
                "step": "verification",
                "verification_report": verification_report,
                "prompt": "Verification complete. Reply 'log' to log the migration summary.",
                "file_content": previous_state["file_content"],
                "analysis_report": previous_state["analysis_report"],
                "migrated_code": previous_state["migrated_code"],
            }
        )
    elif previous_state.get("step") == "verification" and user_input.lower() == "log":
        # Step 4: Log
        log_report = log_migration_summary(
            analysis_report_json=previous_state["analysis_report"],
            generation_report_json=previous_state["migrated_code"],
            verification_report_json=previous_state["verification_report"],
        )
        return json.dumps(
            {
                "step": "logged",
                "log_report": log_report,
                "prompt": "Migration summary logged. Workflow complete.",
            }
        )
    else:
        return json.dumps(
            {
                "step": previous_state.get("step", "start"),
                "prompt": "Please reply with 'proceed', 'verify', or 'log' as appropriate.",
                "file_content": previous_state.get("file_content"),
                "analysis_report": previous_state.get("analysis_report"),
                "migrated_code": previous_state.get("migrated_code"),
                "verification_report": previous_state.get("verification_report"),
            }
        )


# To run this server (example):
import datetime  # Add this at the top if you uncomment the timestamp line

if __name__ == "__main__":
    migration_mcp.run(transport="stdio")
