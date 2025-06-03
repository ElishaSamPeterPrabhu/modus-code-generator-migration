# Modus Component Migration Workflow

## Overview
This document outlines the end-to-end workflow for migrating Modus V1 components to Modus V2 within a codebase. The process has distinct phases (Analyze, Migrate, Verify, Log) with user confirmation gates. Each phase attempts to use a dedicated server tool for guidance; if unavailable, it falls back to local prompt files.

## Phase 1: Analyze

*   **Objective**: Examine source code, identify V1 components, determine framework context, and propose V2 migration strategies.
*   **Agent Action**:
    1.  **Primary**: Call `mcp_modus_migration_server_get_analyze_guidance` to retrieve the `analyze.md` prompt (`guidance_text`), `component_data`, and `directory_paths`.
    2.  **Fallback (if primary tool call fails/unavailable)**: Attempt to read `md_prompts/analyze.md` directly. For associated data, attempt to use locally available `component_data.json` (or similar for individual component files) and assume a default output directory like `analysis_reports/`.
*   **Prompt To Execute**: The content of `analyze.md` obtained via the Primary or Fallback method.
*   **Key Inputs (sourced from tool call or local files/defaults)**:
    *   Source code file(s).
    *   `component_mapping.json`, `v1_components.json`, `v2_components.json`.
    *   `v2_react_framework_data.json`, `v2_angular_framework_data.json`.
*   **Key Outputs from `analyze.md` Execution**:
    *   An `analysis_report.md` for each source file. As per `analyze.md` guidance, this report is saved to `analysis_reports/[replicated_source_directory_path]/[original_filename].analysis.md` (e.g., an analysis for `src/components/button.js` will be at `analysis_reports/src/components/button.js.analysis.md`). The `analysis_reports/` directory and any necessary subdirectories are created if they don't exist.
*   **Agent Action**: Inform user of analysis completion and the specific report location (e.g., "Analysis of `src/components/button.js` complete. Report saved to `analysis_reports/src/components/button.js.analysis.md`.").
*   **User Prompt**: "Analysis reports ready. Review and reply 'proceed to migrate' or specify changes."
    *   *(Agent: Await user confirmation.)*

## Phase 2: Migrate

*   **(Pre-condition: User confirmed after analysis review.)**
*   **Objective**: Transform V1 components to V2 based on the `analysis_report.md`.
*   **Agent Action**:
    1.  **Primary**: Call `mcp_modus_migration_server_get_migrate_guidance` to retrieve `migrate.md` (`guidance_text`) and `component_data`.
    2.  **Fallback**: Attempt to read `md_prompts/migrate.md` and use local `component_data.json`.
*   **Prompt To Execute**: The content of `migrate.md` (from Primary or Fallback).
*   **Key Inputs (sourced accordingly)**:
    *   Original source code file(s).
    *   Corresponding `analysis_report.md`.
    *   `v2_react_framework_data.json`, `v2_angular_framework_data.json`, `v2_components.json`.
*   **Key Outputs from `migrate.md` Execution**:
    *   New Migrated Source Code File(s) (e.g., `[original_filename].migrated.js`). Original unchanged.
    *   `migration.log` (potential save to `migration_logs` directory).
*   **Agent Action**: Summarize migration (e.g., "Migration complete. V2 code in `[new_filename]`.") and provide `migration.log`.
*   **User Prompt**: "Migration attempt complete. Review new file(s) and log. Reply 'proceed to verify' or specify changes."
    *   *(Agent: Await user confirmation.)*

## Phase 3: Verify

*   **(Pre-condition: User confirmed after migration review.)**
*   **Objective**: Ensure correct migration and V2 integration.
*   **Agent Action**:
    1.  **Primary**: Call `mcp_modus_migration_server_get_verify_guidance` for `verify.md` (`guidance_text`), `component_data`, and `gold_standard`.
    2.  **Fallback**: Attempt to read `md_prompts/verify.md`, use local `component_data.json`, and look for local `gold_standard.md`.
*   **Prompt To Execute**: The content of `verify.md` (from Primary or Fallback).
*   **Key Inputs (sourced accordingly)**:
    *   Original and New Migrated Source Code File(s).
    *   `analysis_report.md`, `migration.log`.
    *   `v2_components.json`, `v2_react_framework_data.json`, `v2_angular_framework_data.json`.
    *   `gold_standard.md`.
*   **Key Outputs from `verify.md` Execution**:
    *   `verification.report`.
*   **Agent Action**: Present `verification.report` to user.
*   **User Prompt**: "Verification complete. Review `verification.report`. Reply 'finish' or 'log results' or specify changes."
    *   *(Agent: Await user confirmation.)*

## Phase 4: Log (Optional)

*   **(Pre-condition: User opted to log results.)**
*   **Objective**: Consolidate all reports and logs.
*   **Agent Action**:
    1.  **Primary**: Call `mcp_modus_migration_server_get_log_guidance` for `log.md` (`guidance_text`) and `directory_paths` (for `migration_logs`).
    2.  **Fallback**: Attempt to read `md_prompts/log.md` and assume default `migration_logs` output (e.g., `./migration_logs/`).
*   **Prompt To Execute**: The content of `log.md` (from Primary or Fallback).
*   **Key Inputs**:
    *   All `analysis_report.md`, `migration.log`, `verification.report` files.
    *   Path to `migration_logs` directory.
*   **Key Outputs**:
    *   Consolidated `overall_migration_summary.md` in `migration_logs` directory.
*   **Agent Action**: Inform user: "Reports consolidated into `[migration_logs_path]/overall_migration_summary.md`."
*   **User Prompt**: "Process complete. Consolidated logs available."

## Overall Guiding Principles:

*   **Modular Tooling with Fallback**: Each phase prioritizes calling a specific MCP server tool. If unavailable, it attempts to use local prompt files.
*   **Sequential Execution with User Gates**: Phases are distinct, requiring user confirmation to proceed.
*   **Data-Driven**: Steps rely on previous outputs and data from tools or local fallbacks.
*   **Clear Reporting**: Logs and reports are key for user understanding.

---
This workflow aims for a structured, resilient process with clear user checkpoints.