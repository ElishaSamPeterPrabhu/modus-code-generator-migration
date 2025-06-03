# Modus Migration Analyze Tool

## Purpose
Analyze provided code for Modus V1 components. For each V1 component, identify its V2 web component equivalent and outline the migration approach based on the detected framework (React, Angular, or Vanilla JS). This analysis will serve as the blueprint for the `migrate.md` phase.

## Data Sources
- `component_mapping.json`: Maps V1 component tags to their V2 **web component** equivalents (e.g., `modus-button` maps to `modus-wc-button`). This file may also contain notes on specific attribute changes or, in *exceptional cases*, map a V1 component to a specific V2 importable framework component name if one is intentionally provided and distinct from the web component tag.
- `v1_components.json`: Details about V1 web components.
- `v2_components.json`: Details about V2 **web components** (e.g., `modus-wc-button`, `modus-wc-alert`). This is the source of truth for existing V2 web components, their properties, and events.
- `v1_angular_framework_data.json`: V1 Angular integration context.
- `v1_react_framework_data.json`: V1 React integration context.
- `v2_angular_framework_data.json`: **How-to guide** for using Modus V2 **web components** (e.g., `<modus-wc-button>`) within Angular. This includes instructions on setup (e.g., `CUSTOM_ELEMENTS_SCHEMA`), attribute/property binding conventions for web components in Angular templates, event handling, and any necessary imports for a web component-centric approach. **This file is NOT primarily a list of pre-built, importable Angular wrapper components.**
- `v2_react_framework_data.json`: **How-to guide** for using Modus V2 **web components** (e.g., `<modus-wc-button>`) within React (JSX). This includes instructions on setup (e.g., calling `defineCustomElements()`), attribute/property conventions for web components in JSX (typically standard HTML attribute naming), event handling, and any necessary imports (e.g., from `@trimble-oss/modus-web-components/loader`). **This file is NOT primarily a list of pre-built, importable React wrapper components (like `ModusButton`).**

## Core Analysis Objective
For each source file, produce an `analysis_report.md` detailing:
*   **Framework Identification**: Clearly state the detected framework (React, Angular, or Vanilla JS/Web Components). This is CRITICAL.
*   **V1 Components Found**: List each Modus V1 component, its attributes, and context.
*   **Proposed V2 Migration Strategy**:
    *   **Identify V2 Web Component**: Use `component_mapping.json` to find the direct V2 **web component** tag (e.g., `modus-wc-button` for a V1 `modus-button`). Verify its existence and details in `v2_components.json`. This is the primary V2 target.
    *   **(Optional) Identify Specific Framework Component**: If `component_mapping.json` *explicitly and exceptionally* maps a V1 component directly to an importable V2 React/Angular component name (e.g., `v1-special-widget` -> `ModusReactSpecialWidget`), note this specific target. Otherwise, the target is the V2 web component tag.
    *   **Migration Approach Based on Framework (using the V2 web component tag as the default target)**:
        *   **Vanilla JS**: Target is the direct usage of the V2 web component tag.
        *   **React**:
            *   The default target is to use the V2 **web component tag** directly in JSX (e.g., `<modus-wc-button id="btn">`).
            *   The analysis must state that `v2_react_framework_data.json` will be consulted by the `migrate.md` phase for instructions on:
                *   Ensuring `defineCustomElements()` is called.
                *   Correctly passing attributes/properties to the web component in JSX.
                *   Handling events on the web component in JSX.
            *   If (and only if) `component_mapping.json` explicitly mapped the V1 component to an importable React component, that becomes the target. Otherwise, **do not assume or invent importable React wrappers.** If `component_mapping.json` maps V1 `modus-some-component` to V2 web component `modus-wc-some-component`, the migration should target usage of `<modus-wc-some-component>`, not an invented import like `ModusSomeComponent` or `ModusWcSomeComponent`.
        *   **Angular**:
            *   The default target is to use the V2 **web component tag** directly in Angular templates (e.g., `<modus-wc-button id="btn">`).
            *   The analysis must state that `v2_angular_framework_data.json` will be consulted by the `migrate.md` phase for instructions on:
                *   Declaring `CUSTOM_ELEMENTS_SCHEMA`.
                *   Attribute/property binding syntax for the web component.
                *   Event handling for the web component.
            *   Similar to React, only target an importable Angular component if explicitly mapped in `component_mapping.json`.
*   **Migration Feasibility**: High, Medium, Low. Confidence is higher if the V2 web component exists and the framework integration patterns (from `_framework_data.json`) are clear for web component usage.
*   **Potential Issues/Notes**:
    *   If `component_mapping.json` explicitly indicates NO V2 equivalent for `[V1 Component Name]` (e.g., maps to "N/A", or the component is not found in the mapping, or its V2 target is not in `v2_components.json`): "**No V2 equivalent found for `[V1 Component Name]` in available mappings or V2 component list.** This component will be skipped by the migration process and will require manual replacement or removal."
    *   Else if blocked by parent: "Migration blocked because parent component `[Parent Component Name]` has no V2 equivalent (or was itself skipped)."
    *   Else (a V2 target is identified): "Key attribute changes: (List any). Consult `v2_react/angular_framework_data.json` for framework integration details for the V2 component `[V2 Component Name/Tag]`. Manual review may be needed for complex event handlers or dynamic property settings."
    *   **Complex Attribute Conversion (e.g., V1 `left-icon` on `modus-button`)**:
        *   If a V1 attribute (like `left-icon="add"` on `modus-button`) implies a V2 structure (like a nested `modus-wc-icon` within `modus-wc-button`), the **analysis report's "Proposed V2 Migration" section for that component (when generated by the LLM executing this `analyze.md` prompt) should specify the following**:
            *   "The V1 attribute `left-icon='[icon-name]'` suggests nesting a `<modus-wc-icon name='[icon-name]'></modus-wc-icon>` within the `<modus-wc-button>`."
            *   "The `<modus-wc-icon>` should be described in the analysis output with **only its own valid V2 attributes** (e.g., `name`) as per its entry in `v2_components.json`. **The analysis must NOT suggest adding a `slot` attribute to the `modus-wc-icon` (e.g., `slot='icon-start') UNLESS `slot` is explicitly listed as a configurable property of `modus-wc-icon` itself in `v2_components.json`.**" (Note: Elements are typically *placed into* slots defined by a parent; they don't usually have `slot` as one of their own direct configurable properties).
            *   "The `modus-wc-button` will render this nested child. If `modus-wc-button` has specific named slots defined in its `v2_components.json` documentation that could be used for icon placement, the analysis may note these as a *manual refinement option* for the user (e.g., 'User may consider wrapping the icon like `<div slot="documented-button-slot-name"><modus-wc-icon ... /></div>` if `modus-wc-button` defines `documented-button-slot-name`). Otherwise, the analysis should state: 'The positioning of the nested `modus-wc-icon` will depend on the standard child rendering flow of `modus-wc-button`. Manual CSS may be required by the user to achieve the precise V1 visual layout.'"
            *   The goal is for the `analysis_report.md` to propose a structure using only documented V2 features and not to invent `slot` attributes for child components to fill parent slots, nor assume parent slots that aren't documented.

## Analysis Rules & Steps:

1.  **Load Data**: Parse all JSON data sources.
2.  **For Each File**:
    a.  **Framework Detection**: Identify React, Angular, or Vanilla JS.
    b.  **V1 Component Identification**.
    c.  **Parent-Child Rule**: If a V1 parent can't migrate, children also don't.
    d.  **V1 to V2 Web Component Mapping**:
        *   For each V1 tag (e.g., `modus-button`):
            *   Consult `component_mapping.json`.
            *   **If `component_mapping.json` indicates "Not Found", "N/A", or the V1 component is entirely unlisted, or its listed V2 target is present but NOT verifiable as an existing component in `v2_components.json` (e.g., `v2_components.json` has no entry for the suggested V2 tag)**:
                *   The **analysis report (generated by the LLM executing this `analyze.md` prompt) MUST clearly state for this V1 component**: "**No V2 equivalent found for `[V1 Component Name]` in available mappings or V2 component list.** This component will be skipped by the migration process and will require manual replacement or removal."
                *   The analysis report **MUST NOT** propose any V2 tag, attribute mappings, or framework integration guidance for this specific V1 component. All further analysis for this specific component instance should stop here, and the report should only contain the "No V2 equivalent found" statement for it.
            *   Else (a valid V2 web component equivalent IS found through `component_mapping.json` AND this V2 target is verified to exist in `v2_components.json`):
                *   Note this V2 web component tag as the primary V2 target in the analysis report.
                *   Proceed to analyze attributes, complex conversions (like icons, following the non-inventing-slots rule), and framework integration notes for this valid V2 target, to be included in the analysis report.
            *   As a separate step after determining basic V2 web component target or lack thereof: Check if `component_mapping.json` *also* provides an explicit V2 importable framework component name (e.g., `ModusReactSpecialButton`) for this V1 tag. If so, this is an alternative or specific V2 target to note in the analysis report, but its existence and validity must also be considered (e.g., is it a known part of a V2 framework library).
            *   If the component is part of a parent-child relationship and its parent's analysis has already determined "No V2 equivalent found" (or the parent is blocked for other reasons), then this child component should be marked as "Blocked by Parent" in the analysis report, and no V2 migration should be proposed for it, regardless of its own individual mapping status.
    e.  **Detailing Framework-Specific Integration Guidance (for `migrate.md`)**:
        *   The analysis report will note the primary V2 target (usually the web component tag).
        *   It will then state that for React/Angular, the `migrate.md` process must refer to `v2_react_framework_data.json` or `v2_angular_framework_data.json` for detailed instructions on how to correctly use this V2 web component tag within that framework.
    f.  **Unknown Components**: Note if not in `v1_components.json`.
3.  **Output Generation**:
    *   Save analysis as `<original-filename>.analysis.md`.
    *   Report must clearly state the identified framework and the primary V2 **web component tag** to be used (or the exceptional importable framework component if explicitly mapped).

## Output Generation (for the LLM executing this prompt)

1.  **Report Content**: For each input source file, compile an analysis report in Markdown format. This report must include:
    *   The detected framework.
    *   A list of V1 components found, their attributes, and context.
    *   The proposed V2 migration strategy for each, detailing the target V2 web component tag (or exceptional framework component), attribute mappings, and references to `v2_react/angular_framework_data.json` for integration guidance.
    *   Specific handling for complex attributes (like `left-icon`), ensuring no non-existent V2 slots/properties are invented. This should follow the detailed guidance provided in the "Core Analysis Objective" or "Potential Issues/Notes" section regarding how the analysis report itself should describe these complex conversions (i.e., not inventing slots, suggesting manual CSS for layout if V2 components don't automatically achieve V1 visual layout).
    *   Migration feasibility and any potential issues, including clear statements if no V2 equivalent is found for a component.

2.  **Saving the Report**:
    *   The generated Markdown analysis report **must be saved within the user's project workspace.**
    *   **File Naming**: Use the convention `[original_filename].analysis.md` (e.g., if analyzing `my-component.js`, save as `my-component.js.analysis.md`).
    *   **Report Directory Structure**:
        *   All analysis reports must be saved within a top-level directory named `analysis_reports/` relative to the project root.
        *   **Crucially, if the original file being analyzed is in a subdirectory (e.g., `src/components/button.js`), that same subdirectory structure MUST be replicated inside the `analysis_reports/` directory.**
        *   For example, an analysis report for `frontend/src/web-components/Navigation/Navigation.js` MUST be saved as `analysis_reports/frontend/src/web-components/Navigation/Navigation.js.analysis.md`.
        *   The directory path `analysis_reports/frontend/src/web-components/Navigation/` (excluding the filename itself) MUST be created if it does not already exist *before* attempting to save the file.
    *   **Path Construction and Verification**:
        *   The agent/tool is responsible for correctly constructing the full absolute or relative path to the report file, including the replicated subdirectory structure under `analysis_reports/`.
        *   Before saving, the agent/tool should verify if the target directory (e.g., `analysis_reports/frontend/src/web-components/Navigation/`) exists.
        *   If the directory does not exist, it **MUST be created programmatically.**
    *   **User Accessibility**: The user must be able to directly access these generated report files within their project structure after this phase completes. **Do not store these reports in a temporary, inaccessible, or server-side-only location.**
    *   **Error Handling during Save**: If, after attempting to create directories and save the file, an error still occurs (e.g., permission issues, unexpected file system errors), the agent MUST:
        *   Clearly inform the user about the failure to save the report to the intended structured path.
        *   Specify the exact path it attempted to save to.
        *   As a **fallback only**, save the report content directly into the chat or provide it in a raw format that the user can copy and save manually. This fallback should only be used if the primary structured save fails.

## Output Format (for the .md report)

*   **Title and Summary**: Heading: `Analysis Report for <filename>`. Summary: "Detected Framework: [React/Angular/VanillaJS]. This report outlines V2 migration targets, primarily focusing on V2 web components and referencing framework-specific integration guides (`v2_react/angular_framework_data.json`) for their use in React/Angular."
*   **Detailed Component Breakdown**: For each V1 component:
    *   V1 Tag Name, attributes, context.
    *   **Proposed V2 Migration**:
        *   **Target V2 Equivalent**: (e.g., "V2 Web Component: `modus-wc-button`" OR, if explicitly mapped: "V2 React Component: `ModusSpecialButton` (import from library)")
        *   **Framework-Specific Integration Guidance (for `migrate.md`)**:
            *   **If React (and target is web component)**: "Migrate to `<modus-wc-button ... />` in JSX. `migrate.md` process to consult `v2_react_framework_data.json` for: `defineCustomElements()` setup, JSX attribute/property conventions for this web component, and event handling patterns."
            *   **If Angular (and target is web component)**: "Migrate to `<modus-wc-button ... />` in template. `migrate.md` process to consult `v2_angular_framework_data.json` for: `CUSTOM_ELEMENTS_SCHEMA`, property/event binding for this web component."
            *   **If Vanilla JS**: "Migrate to standard web component usage of `modus-wc-button`."
            *   **If target is an explicit framework component (e.g., `ModusSpecialButton`)**: "Migrate to `<ModusSpecialButton ... />`. Import from specified library. Consult `v2_react_framework_data.json` for any specific usage notes if available."
        *   Key attribute changes (V1 attr -> V2 attr for the V2 web component or specific framework component).
    *   Migration Feasibility.
    *   **Notes**:
        *   If `component_mapping.json` explicitly indicates NO V2 equivalent for `[V1 Component Name]` (e.g., maps to "N/A", or the component is not found in the mapping, or its V2 target is not in `v2_components.json`): "**No V2 equivalent found for `[V1 Component Name]` in available mappings or V2 component list.** This component will be skipped by the migration process and will require manual replacement or removal."
        *   Else if blocked by parent: "Migration blocked because parent component `[Parent Component Name]` has no V2 equivalent (or was itself skipped)."
        *   Else (a V2 target is identified): "Key attribute changes: (List any). Consult `v2_react/angular_framework_data.json` for framework integration details for the V2 component `[V2 Component Name/Tag]`. Manual review may be needed for complex event handlers or dynamic property settings."
        *   **Complex Attribute Conversion (e.g., V1 `left-icon` on `modus-button`)**:
            *   If a V1 attribute (like `left-icon="add"` on `modus-button`) implies a V2 structure (like a nested `modus-wc-icon` within `modus-wc-button`), the **analysis report's "Proposed V2 Migration" section for that component (when generated by the LLM executing this `analyze.md` prompt) should specify the following**:
                *   "The V1 attribute `left-icon='[icon-name]'` suggests nesting a `<modus-wc-icon name='[icon-name]'></modus-wc-icon>` within the `<modus-wc-button>`."
                *   "The `<modus-wc-icon>` should be described in the analysis output with **only its own valid V2 attributes** (e.g., `name`) as per its entry in `v2_components.json`. **The analysis must NOT suggest adding a `slot` attribute to the `modus-wc-icon` (e.g., `slot='icon-start') UNLESS `slot` is explicitly listed as a configurable property of `modus-wc-icon` itself in `v2_components.json`.**" (Note: Elements are typically *placed into* slots defined by a parent; they don't usually have `slot` as one of their own direct configurable properties).
                *   "The `modus-wc-button` will render this nested child. If `modus-wc-button` has specific named slots defined in its `v2_components.json` documentation that could be used for icon placement, the analysis may note these as a *manual refinement option* for the user (e.g., 'User may consider wrapping the icon like `<div slot="documented-button-slot-name"><modus-wc-icon ... /></div>` if `modus-wc-button` defines `documented-button-slot-name`). Otherwise, the analysis should state: 'The positioning of the nested `modus-wc-icon` will depend on the standard child rendering flow of `modus-wc-button`. Manual CSS may be required by the user to achieve the precise V1 visual layout.'"
                *   The goal is for the `analysis_report.md` to propose a structure using only documented V2 features and not to invent `slot` attributes for child components to fill parent slots, nor assume parent slots that aren't documented.