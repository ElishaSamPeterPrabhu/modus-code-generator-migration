# Modus Component Migration: Verification Phase

## Objective
Verify that the Modus V1 to V2 component migration has been performed correctly according to the analysis report and the migration guidelines. This involves checking the transformed code and the migration log.

## Inputs
*   **Original Source Code File(s)** (or a copy).
*   **Migrated Source Code File(s)**: Path to the migrated code, e.g., `migrated_code/frontend/src/web-components/Navigation/Navigation.migrated.js`.
*   Path to the `analysis_report.md` for each migrated file, e.g., `analysis_reports/frontend/src/web-components/Navigation/Navigation.js.analysis.md`.
*   Path to the `migration.log` for each migrated file, e.g., `migration_logs/frontend/src/web-components/Navigation/Navigation.js.migration.log`.
*   `v2_components.json`: Details about V2 web components.
*   `v2_react_framework_data.json`: How-to guide for using V2 web components in React.
*   `v2_angular_framework_data.json`: How-to guide for using V2 web components in Angular.
*   `component_mapping.json`.
*   **(Optional) Gold Standard Files**: If available, known good V2 versions of the migrated files/components for comparison.

## Verification Steps (for each migrated file):

1.  **Review Migration Log**:
    *   Check for any errors or warnings reported during the migration for this file.
    *   Note any components that were skipped and verify the reasons (e.g., "No V2 equivalent," "Blocked by parent"). Ensure these components remain as V1 in the migrated code.
    *   Pay attention to any notes about required manual steps or reviews.

2.  **Code Review (Comparing Migrated Code to Original and Analysis Report)**:

    *   **Framework Consistency**: Confirm the migration respected the framework (Vanilla JS, React, Angular) identified in the analysis report.
    *   **Component Tag Transformation**:
        *   For each V1 component instance identified in the analysis report that was supposed to be migrated:
            *   Verify it has been changed to its target V2 **web component tag** (e.g., `modus-button` -> `modus-wc-button`) as specified in the analysis.
            *   **Exception**: If the analysis *explicitly* targeted an importable V2 framework component (e.g., `ModusSpecialButton`), verify that specific component was used and imported.
        *   Ensure V1 components marked "Do Not Migrate" (or similar) in the analysis are untouched.
    *   **Attribute/Property Mapping**:
        *   Verify that V1 attributes have been correctly mapped to V2 attributes/properties for the migrated components, as per the analysis report.
        *   Check for correct casing and syntax (e.g., HTML standard for web component attributes).
    *   **Framework-Specific Integration (React/Angular using Web Components)**:
        *   **If React**:
            *   If V2 web components are used, confirm that the usage in JSX aligns with the guidance in `v2_react_framework_data.json`. This includes:
                *   Correct attribute/property passing (e.g., string literals, boolean attributes, bound values).
                *   Event handling patterns (e.g., direct `onEventName` or `ref` + `addEventListener`).
            *   Check for the presence of `import { defineCustomElements } from '@trimble-oss/modus-web-components/loader';` and the call to `defineCustomElements()` if web components were introduced/migrated.
        *   **If Angular**:
            *   If V2 web components are used, confirm that the usage in templates aligns with `v2_angular_framework_data.json`. This includes:
                *   Correct attribute/property binding (`[]`, `{{}}`).
                *   Event binding (`()`).
            *   Check if `CUSTOM_ELEMENTS_SCHEMA` is present in the relevant Angular module(s) if web components are used.
            *   Check for the call to `defineCustomElements()` in the application (e.g., `main.ts`).
    *   **Preservation of Non-Modus Code**: Ensure that application logic, structure, and non-Modus UI elements outside the migrated components have not been unintentionally altered.
    *   **Removal of Obsolete V1 Imports**: If V1 Modus libraries were imported (e.g., specific V1 Modus JS files), check if these are now obsolete and can be removed if all their components are migrated. (This might be a broader, multi-file check).

3.  **Static Analysis / Linting**:
    *   Run any available static analysis tools or linters on the migrated code to catch syntax errors or potential issues.
    *   Pay attention to errors related to unknown components or incorrect property types, especially in React/Angular contexts.

4.  **(Optional) Functional Testing / "Smoke Test"**:
    *   If possible, run the application or relevant parts to perform a basic functional test or "smoke test" of the migrated components.
    *   Check for console errors in the browser.
    *   Verify basic interactivity of the migrated components.

5.  **(Optional) Comparison with Gold Standard**:
    *   If gold standard files exist, compare the migrated code against them. This is a very effective way to catch subtle differences.

## Output

The LLM/tool executing this prompt is responsible for creating the following file(s) in an accessible location within the user's project. **Do not store these files in a temporary, inaccessible, or server-side-only location.**

*   **Verification Report (`verification.report.md`)**:
    *   A detailed verification report must be generated for each migrated source file processed.
    *   **Directory Structure for Verification Reports**:
        *   All verification reports must be saved within a top-level directory named `verification_reports/` relative to the project root.
        *   **The report file should also follow the replicated subdirectory structure of the original source file.**
        *   For example, the verification report for `frontend/src/web-components/Navigation/Navigation.js` (after migration) MUST be saved as `verification_reports/frontend/src/web-components/Navigation/Navigation.js.verification.report.md`.
        *   The directory path (e.g., `verification_reports/frontend/src/web-components/Navigation/`) MUST be created if it does not already exist *before* attempting to save the file.
    *   **File Naming for Verification Reports**: Use `[original_filename].verification.report.md`.
    *   **Content**: The report must include:
        *   Summary of verification findings for each file.
        *   List of any discrepancies found (e.g., "V1 `modus-table` attribute `sortable-cols` not correctly mapped to V2 `modus-wc-table` equivalent in `data-grid.js`").
        *   Confirmation of issues noted in the migration log.
        *   Any new issues identified during verification that require attention or manual fixes.
        *   Status: "Verified," "Verified with Issues," or "Needs Rework."
    *   **User Accessibility**: The user must be able to directly access these generated report files.

*   **(If applicable) List of suggested further manual changes or fixes.**

*   **Error Handling during Save (for Verification Reports)**:
    *   If, after attempting to create directories and save the report, an error still occurs (e.g., permission issues, unexpected file system errors), the agent MUST:
        *   Clearly inform the user about the failure to save the verification report to its intended structured path.
        *   Specify the exact path it attempted to save to.
        *   As a **fallback only** for the *content* of the report it failed to save, provide it directly into the chat or in a raw format that the user can copy and save manually. This fallback should only be used if the primary structured save fails.

## Important Considerations for the LLM Implementing This:

*   **Systematic Approach**: Follow the checklist methodically for each component and file.
*   **Focus on the Analysis Report**: The analysis report is the key document defining the expected outcome.
*   **Understand Framework Nuances for Web Components**: Verification must account for how web components are integrated into React (JSX, `defineCustomElements`) and Angular (templates, `CUSTOM_ELEMENTS_SCHEMA`, `defineCustomElements`). The `v2_react/angular_framework_data.json` files are critical references here.
*   **Be Conservative**: If unsure about a change or its correctness, flag it for human review.
---

**Remember**: The verification step is crucial for ensuring the quality and correctness of the automated migration. It catches errors made by the migration script and ensures the application remains functional. 