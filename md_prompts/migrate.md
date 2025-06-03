# Modus Component Migration: Migration Phase

## Objective
Transform Modus V1 component usage in the source code to Modus V2, based on the framework identified and migration strategy outlined in the `analysis_report.md` for each file.

## Inputs
*   Source code file(s) containing Modus V1 components.
*   Path to the `analysis_report.md` (e.g., `analysis_reports/src/components/button.js.analysis.md`): The analysis report corresponding to the source file being migrated. This report is CRUCIAL and dictates the migration actions. It specifies:
    *   Detected framework (React, Angular, Vanilla JS).
    *   V1 components found.
    *   The target V2 **web component tag** (e.g., `modus-wc-button`) or, in exceptional cases, a specific importable V2 framework component.
    *   Attribute mappings.
    *   Pointers to consult `v2_react_framework_data.json` or `v2_angular_framework_data.json` for framework-specific integration instructions for web components.
*   `v2_react_framework_data.json`: **How-to guide** for using Modus V2 web components in React (JSX syntax, `defineCustomElements` loader, event handling, attribute conventions).
*   `v2_angular_framework_data.json`: **How-to guide** for using Modus V2 web components in Angular (template syntax, `CUSTOM_ELEMENTS_SCHEMA`, event/property binding).
*   `component_mapping.json` (for reference on attribute mappings if needed, though analysis report should be primary).
*   `v2_components.json` (for reference on V2 web component properties/events if needed).

## Migration Steps (for each component instance identified in the analysis report):

1.  **Read Analysis Report**: For the current V1 component instance, extract its V2 target (usually a web component tag like `modus-wc-button`) and any framework-specific notes from the `analysis_report.md`.
    *   **Consistency Check for V2 Target**: Before proceeding with migration for a V1 component instance, verify the V2 target information in the `analysis_report.md`. If the report for that specific V1 component *explicitly and unambiguously* states "**No V2 equivalent found**" (or similar, indicating it was deemed unmappable during analysis based on `component_mapping.json` or `v2_components.json` validation), then this component **MUST be treated as unmigratable.** Do not proceed with tag transformation or attribute mapping for this instance, even if other parts of the analysis report for this component might (erroneously) contain migration suggestions for it. The "No V2 equivalent found" determination from the analysis phase is final for that component.

2.  **Locate V1 Component in Code**: Find the exact V1 component instance in the source file.

3.  **Determine Migratability based on Finalized Analysis**: Based on the `analysis_report.md` (and the consistency check in step 1):
    *   If the component was determined to have **"No V2 equivalent found"** or is **"Blocked by Parent"**: This component instance is **NOT to be migrated**. Proceed to step 4 (Handle Skipped Components).
    *   Else (a valid V2 target was identified and the component is not blocked): Proceed with framework-specific transformation (step 3 continued below, now renumbered effectively as the main transformation logic path).

3.  **Framework-Specific Transformation** (Continued - only if component is deemed migratable):

    *   **If Framework is Vanilla JS (or general HTML analsysis)**:
        *   Replace the V1 tag (e.g., `modus-button`) with the V2 web component tag (e.g., `modus-wc-button`).
        *   Apply attribute mappings as per the analysis report.
        *   If JavaScript is used to create/manipulate the component, update `document.createElement('modus-button')` to `document.createElement('modus-wc-button')` and adjust property/method calls based on `v2_components.json`.
        *   Ensure any necessary global setup for V2 web components (like calling a loader script if V1 didn't require it but V2 does) is considered (this might be a global note for the file).

    *   **If Framework is React**:
        *   **Target V2 Web Component Tag (Default Path)**:
            *   In the JSX, replace the V1 tag (e.g., `<modus-button>`) with the V2 web component tag (e.g., `<modus-wc-button>`).
            *   **Apply JSX-specific transformations guided by `v2_react_framework_data.json`**:
                *   **Attribute and Structural Mapping (Constraint)**:
                    *   Map V1 attributes that have direct V2 attribute equivalents on the primary V2 component (e.g., `color` on `modus-button` to `color` on `modus-wc-button`) based on `analysis_report.md`.
                    *   If the analysis report suggested a structural change for a V1 attribute (e.g., V1 `left-icon="add"` on `modus-button` should become a nested `<modus-wc-icon name="add">` within `modus-wc-button`):
                        *   **Create the valid V2 nested component** (e.g., `modus-wc-icon`) using only its own valid attributes as defined in `v2_components.json` (e.g., `<modus-wc-icon name="add">`).
                        *   Place this nested V2 component as a child of the parent V2 component (e.g., inside `<modus-wc-button>`).
                        *   **Crucially: Do NOT assign non-existent attributes to the nested V2 component.** For instance, do not add `slot="icon-start"` to `modus-wc-icon` if `modus-wc-icon` does not itself have a `slot` property documented in `v2_components.json`.
                        *   **Similarly, do NOT assume the parent V2 component (e.g., `modus-wc-button`) has special undeclared slots (like an "icon-start" slot) that the nested component should try to fill.** The V2 parent component will render its children based on its standard rendering logic and documented slots only.
                        *   If the V1 attribute (e.g., `left-icon`) implies a specific visual positioning that is not automatically achieved by simple valid nesting of V2 components, **add a comment in the migrated code**: `// MODUS MIGRATION: V1 attribute '[v1_attr_name]' on '[V1_Component_Name]' resulted in a nested '<[V2_Nested_Component_Tag_Name]>'. Review layout: Manual CSS or further adjustments may be needed to achieve precise V1 visual positioning of the nested component within '<[V2_Parent_Component_Tag_Name]>', as per [V2_Parent_Component_Tag_Name]'s capabilities.`
                        *   Log this for potential manual review: `"[V1_Component_Name] attribute '[v1_attr_name]': Migrated to nested <[V2_Nested_Component_Tag_Name]>. Manual review of layout within <[V2_Parent_Component_Tag_Name]> may be needed."`
                    *   For other V1 attributes (e.g., `onClick={handler}`, `value={val}`), map them to the V2 component's attributes/properties as per React conventions and `v2_react_framework_data.json` guidance.
                *   **Event Handling**: Adapt event handling. If V1 used `onClick={handler}`, check `v2_react_framework_data.json` for the recommended V2 pattern for web components (it might still be `onClick`, or it might require `ref` and `addEventListener` in `useEffect`).
                *   **Boolean Attributes**: Handle boolean attributes correctly for web components in JSX (e.g., presence of attribute means true, or `attribute={true}`).
                *   **Class Styling**: Convert `class` to `className` if the V1 component was a custom element where `class` was directly used as a prop (less common for standard HTML elements). For web components, `class` usually works as expected.
        *   **Target Importable React Component (Exceptional Path, only if analysis report EXPLICITLY specifies this)**:
            *   If the analysis report mapped V1 `modus-special-button` to an importable `ModusSpecialButton`, replace `<modus-special-button>` with `<ModusSpecialButton>`.
            *   Add the necessary import: `import { ModusSpecialButton } from '@trimble-oss/moduswebcomponents-react';` (or the specified library).
            *   Map attributes to props as per React conventions for this specific wrapper.

    *   **If Framework is Angular**:
        *   **Target V2 Web Component Tag (Default Path)**:
            *   In the template, replace the V1 tag (e.g., `<modus-button>`) with the V2 web component tag (e.g., `<modus-wc-button>`).
            *   **Apply Angular-specific transformations guided by `v2_angular_framework_data.json`**:
                *   **Attributes/Properties**: Map V1 attributes to V2 attributes/properties. Use Angular binding syntax as needed (e.g., `[property]="value"`, `attribute="literal"`).
                *   **Event Handling**: Convert V1 event bindings to V2 web component event bindings using Angular's syntax (e.g., `(clickEventName)="handler($event)"`). The exact event name must match the V2 web component's event.
            *   **Ensure `CUSTOM_ELEMENTS_SCHEMA`**: Verify that the relevant Angular module has `CUSTOM_ELEMENTS_SCHEMA` in its `schemas` array to allow web component tags. The migration tool should flag if this is likely missing.

4.  **Handle Skipped Components / Components Deemed Unmigratable** (This step now primarily handles the commenting and logging for components identified as unmigratable in step 3 above):
    *   If the component instance was determined to be unmigratable in step 3 (due to "No V2 equivalent found" or "Blocked by Parent" from the analysis report):
        *   **Ensure the V1 component tag and its attributes in the source code are left untouched.**
        *   Add a comment directly above the V1 component instance: `// MODUS MIGRATION: Component '[V1 Component Name]' - No V2 equivalent found (or blocked by parent). Original V1 component retained for manual assessment.`
        *   Log this action clearly: `"[V1 Component Name] in [filename] - SKIPPED: No V2 equivalent specified / Blocked by parent, based on analysis report."`
    *   (The previous sub-bullet about "MANUAL REVIEW RECOMMENDED for complex aspects" for *migrated* components still applies but is part of the transformation logic in step 3, not here in step 4 which is for *unmigrated* components.)

5.  **Code Formatting**: Ensure the generated code is well-formatted.

## Output

The LLM/tool executing this prompt is responsible for creating the following files in an accessible location within the user's project. **Do not store these files in a temporary, inaccessible, or server-side-only location.**

1.  **Migrated Source Code File**:
    *   Instead of modifying the original file, the migrated V2 code **must be written to a NEW file.**
    *   **Directory Structure for Migrated Code**:
        *   All migrated code files must be saved within a top-level directory named `migrated_code/` relative to the project root.
        *   **Crucially, if the original file being migrated is in a subdirectory (e.g., `src/components/button.js`), that same subdirectory structure MUST be replicated inside the `migrated_code/` directory.**
        *   For example, the migrated version of `frontend/src/web-components/Navigation/Navigation.js` MUST be saved within `migrated_code/frontend/src/web-components/Navigation/`.
        *   The directory path (e.g., `migrated_code/frontend/src/web-components/Navigation/`) MUST be created if it does not already exist *before* attempting to save the file.
    *   **File Naming for Migrated Code**: Use the convention `[original_filename].migrated.[original_extension]` (e.g., if migrating `my-component.js`, save as `my-component.migrated.js`). Ensure the naming is consistent.
    *   **Path Construction and Verification**: The agent/tool is responsible for correctly constructing the full path to the migrated file and ensuring the target directory is created.
    *   **User Accessibility**: The user must be able to directly access these generated migrated files.

2.  **Migration Log (`migration.log`)**:
    *   A detailed migration log must be generated for each source file processed.
    *   **Directory Structure for Migration Logs**:
        *   All migration logs must be saved within a top-level directory named `migration_logs/` relative to the project root.
        *   **The log file should also follow the replicated subdirectory structure of the original source file.**
        *   For example, the migration log for `frontend/src/web-components/Navigation/Navigation.js` MUST be saved as `migration_logs/frontend/src/web-components/Navigation/Navigation.js.migration.log`.
        *   The directory path (e.g., `migration_logs/frontend/src/web-components/Navigation/`) MUST be created if it does not already exist *before* attempting to save the file.
    *   **File Naming for Migration Logs**: Use `[original_filename].migration.log`.
    *   **Content**: The log must include:
        *   List of successfully migrated component instances (V1 tag, V2 tag/component, original file location, new migrated file location).
        *   List of V1 component instances that were skipped in the original file, with precise reasons (e.g., "No V2 equivalent found", "Blocked by Parent").
        *   Any warnings or errors encountered during migration for that specific file.
        *   Notes on aspects of *migrated* components that require manual review (e.g., layout adjustments for nested icons).
    *   **User Accessibility**: The user must be able to directly access these generated log files.

3.  **Error Handling during Save (for both Migrated Code and Logs)**:
    *   If, after attempting to create directories and save any file, an error still occurs (e.g., permission issues, unexpected file system errors), the agent MUST:
        *   Clearly inform the user about the failure to save the specific file to its intended structured path.
        *   Specify the exact path it attempted to save to.
        *   As a **fallback only** for the *content* of the file it failed to save (e.g., the migrated code content, or the log content), provide it directly into the chat or in a raw format that the user can copy and save manually. This fallback should only be used if the primary structured save fails for that specific file.

## Important Considerations for the LLM Implementing This:

*   **DO NOT ADD `defineCustomElements`**: The migration script **must not** add `import { defineCustomElements } ...` or any calls to `defineCustomElements()` into the migrated files. This setup is the sole responsibility of the user at their application's entry point. The script should only transform component instances within the file being processed.
*   **Adhere Strictly to Analysis Report AND V2 Component Definitions (`v2_components.json`) for ALL Component Attributes and Structure**:
    *   The `analysis_report.md` guides V2 targets and direct attribute mappings.
    *   **For any structural changes (e.g., nesting an icon for a V1 `left-icon` attribute) or when assigning ANY attribute to ANY V2 component (parent or nested child like `modus-wc-icon`):**
        *   **ULTRA-STRICT RULE**: An attribute (e.g., `name`, `color`, `size`, OR `slot`) may ONLY be applied to a V2 component (e.g., `modus-wc-icon` or `modus-wc-button`) if that attribute is **explicitly documented as a configurable property or supported attribute for THAT SPECIFIC V2 COMPONENT in its `v2_components.json` entry.**
        *   **Do NOT infer or assume an attribute (ESPECIALLY `slot`) is supported by a V2 component just because it seems logical or was suggested (even if incorrectly) by an analysis report.** Always verify against `v2_components.json` for the component receiving the attribute.
        *   Specifically for `slot` attributes on a child (e.g., `<modus-wc-icon slot="icon-start">`): This is ONLY permissible if `modus-wc-icon` itself is documented in `v2_components.json` to have `slot` as one of its own configurable properties (which is highly unlikely for this use case, as slots are typically defined by the parent).
        *   If a V1 attribute implies a nested V2 component (e.g., `left-icon="add"` implies `<modus-wc-icon name="add">`): Create the nested V2 component using only its own documented attributes from `v2_components.json`. Place it as a standard child of the V2 parent component.
        *   If this valid nesting doesn't achieve the V1 visual layout, a comment (`// MODUS MIGRATION: V1 attribute '[v1_attr_name]'... Review layout...`) MUST be added, indicating manual CSS/layout review is needed. **DO NOT attempt to force layout by adding undocumented `slot` attributes to the child or assuming undocumented consuming slots on the parent.**
*   **Prioritize Web Component Tags**: The default migration path is to use the V2 web component tag (e.g., `<modus-wc-button>`) directly in React/Angular, relying on the `v2_react/angular_framework_data.json` for integration instructions.
*   **Importable Wrappers are Exceptions**: Only use importable framework-specific wrappers (e.g., `ModusButton` from a library) if the analysis report *explicitly* specified this based on an exceptional mapping in `component_mapping.json`.
*   **Idempotency (Ideal)**: If run again, the migrator should ideally not re-migrate already migrated components (though this can be complex). Focus on a correct first pass.
*   **Preserve Code Structure**: Minimize changes to non-Modus code.
*   **Clear Logging**: The log is essential for the user to understand what happened and what might need manual attention.

---

**Remember**: The goal is to automate as much as possible, but complex cases or framework intricacies (especially with event handling or complex data for web components in React/Angular) might require highlighting for manual review, guided by the `_framework_data.json` files.