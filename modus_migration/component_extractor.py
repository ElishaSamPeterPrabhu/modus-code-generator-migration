import json
import re
import os
import sys
import subprocess
from typing import Dict, List
from pathlib import Path
import shutil
import stat


def handle_remove_error(func, path, exc_info):
    """Handle permission errors when removing files"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repo(repo_url, target_dir, skip_clone_if_exists: bool):
    """Clone a git repository to the specified directory.
    If skip_clone_if_exists is True, it will skip if the directory already exists.
    """
    if skip_clone_if_exists and os.path.exists(target_dir):
        print(
            f"Repository directory {target_dir} already exists, skipping clone as per configuration."
        )
        return True

    # The previous logic for removing the directory has been taken out as per user request.
    # Git will handle cloning into an existing directory (e.g. if it's already a git repo and clean, or if it's empty).
    # If the directory exists and is non-empty and not a git repo, git clone will fail, which is standard behavior.

    print(f"Attempting to clone {repo_url} into {target_dir}...")
    try:
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return False


def find_component_dir(repo_path: str, version: str) -> str:
    """
    Find the components directory based on version and repo structure.
    Handles different directory structures between v1 and v2.
    """
    # Common possible paths
    possible_paths = [
        os.path.join(repo_path, "packages", "web-components", "src", "components"),
        os.path.join(repo_path, "src", "components"),
        os.path.join(repo_path, "components"),
        os.path.join(repo_path, "packages", "components"),
        os.path.join(
            repo_path, "packages", "modus-web-components", "src", "components"
        ),
    ]

    # Version-specific paths
    if version == "v2":
        # Add v2-specific paths - prioritize src/components in v2
        possible_paths = [
            os.path.join(repo_path, "src", "components"),
            os.path.join(repo_path, "components"),
        ] + possible_paths

    # Check each path and return the first one that exists
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found components directory: {path}")
            return path

    # If no path is found, try to find any directory containing .tsx files
    print("No standard components directory found. Searching for component files...")
    for root, dirs, files in os.walk(repo_path):
        tsx_files = [f for f in files if f.endswith(".tsx")]
        if tsx_files:
            print(f"Found directory with .tsx files: {root}")
            return root

    print(f"WARNING: Could not find any component directory in {repo_path}")
    return os.path.join(repo_path, "src", "components")  # Return a default path


def find_storybook_dir(repo_path: str, version: str) -> str:
    """
    Find the storybook directory based on version and repo structure.
    - Modus 1.0: Storybook files are in a separate directory
    - Modus 2.0: Storybook files are alongside the component files
    """
    if version == "v1":
        # For v1, storybook is typically in a separate directory
        possible_paths = [
            os.path.join(repo_path, "packages", "web-components", "src", "stories"),
            os.path.join(repo_path, "packages", "storybook"),
            os.path.join(repo_path, "storybook"),
            os.path.join(repo_path, "stories"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found storybook directory for v1: {path}")
                return path
    else:
        # For v2, storybook files are typically alongside the component files,
        # so we return the component directory
        component_dir = find_component_dir(repo_path, version)
        print(f"Using component directory for v2 storybook: {component_dir}")
        return component_dir

    # If no storybook directory found, return None
    print(f"WARNING: Could not find storybook directory in {repo_path}")
    return None


def find_docs_dir(repo_path: str, version: str) -> str:
    """
    Find the documentation directory based on version and repo structure.
    """
    # Common possible paths
    possible_paths = [
        os.path.join(repo_path, "packages", "web-components", "src", "components"),
        os.path.join(repo_path, "docs"),
        os.path.join(repo_path, "documentation"),
        os.path.join(repo_path, "src", "docs"),
        os.path.join(repo_path, "packages", "docs"),
    ]

    # Version-specific paths
    if version == "v2":
        possible_paths = [
            os.path.join(repo_path, "docs"),
            os.path.join(repo_path, "documentation"),
        ] + possible_paths

    # Check each path and return the first one that exists
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found documentation directory: {path}")
            return path

    # If no path is found, look for any directory containing .md files
    for root, dirs, files in os.walk(repo_path):
        md_files = [f for f in files if f.endswith(".md") or f.endswith(".mdx")]
        if md_files and "node_modules" not in root:
            print(f"Found directory with .md files: {root}")
            return root

    print(f"WARNING: Could not find documentation directory in {repo_path}")
    return os.path.join(repo_path, "docs")  # Return a default path


def extract_storybook_and_docs(dir_path: str, is_v2: bool) -> dict:
    """Extract full storybook content and documentation."""
    result = {
        "documentation": "",
        "storybook_content": (
            "" if not is_v2 else None
        ),  # Don't create storybook_content for v2
        "examples": [],
        "variants": [],
        "prop_usage": {},
    }

    try:
        # Find story files and doc files
        story_files = [
            f
            for f in os.listdir(dir_path)
            if f.endswith(".stories.tsx") or f.endswith(".stories.ts")
        ]
        doc_files = [f for f in os.listdir(dir_path) if f.endswith(".mdx")]

        # Process story files
        for story_file in story_files:
            file_path = os.path.join(dir_path, story_file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Store full storybook content
                    if is_v2:
                        # For v2, add to documentation directly
                        result[
                            "documentation"
                        ] += f"\n\n--- {story_file} ---\n\n{content}"
                    else:
                        # For v1, store separately as we'll also have .mdx docs
                        result[
                            "storybook_content"
                        ] += f"\n\n--- {story_file} ---\n\n{content}"

                    # Extract tag examples for convenience
                    tag_prefix = "modus-wc-" if is_v2 else "modus-"
                    examples = re.findall(
                        f"<{tag_prefix}[^>]+>[^<]*</{tag_prefix}[^>]+>", content
                    )
                    examples.extend(re.findall(f"<{tag_prefix}[^/>]+/>", content))

                    # Extract from template literals
                    template_literals = re.findall(r"`(.*?)`", content, re.DOTALL)
                    for literal in template_literals:
                        if f"<{tag_prefix}" in literal:
                            examples.append(literal)

                    result["examples"].extend(examples[:5])

                    # Extract variants
                    variants = re.findall(
                        r'[\'"]variant[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', content
                    )
                    variants.extend(
                        re.findall(r'variant=[\'"]{([^}]+)}[\'""]', content)
                    )
                    variants.extend(re.findall(r'variant=[\'"]([^\'"]+)[\'"]', content))
                    result["variants"].extend(list(set(variants)))

                    # Extract prop usage
                    prop_pattern = r'(\w+)=[\'"]([^\'"]+)[\'"]'
                    prop_matches = re.findall(prop_pattern, content)
                    for prop, value in prop_matches:
                        if prop not in result["prop_usage"]:
                            result["prop_usage"][prop] = []
                        if value not in result["prop_usage"][prop]:
                            result["prop_usage"][prop].append(value)
            except Exception as e:
                print(f"Error processing story file {file_path}: {e}")

        # Process documentation files (primarily for v1)
        for doc_file in doc_files:
            file_path = os.path.join(dir_path, doc_file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    result["documentation"] += f"\n\n--- {doc_file} ---\n\n{content}"
            except Exception as e:
                print(f"Error processing documentation file {file_path}: {e}")

    except Exception as e:
        print(f"Error extracting storybook and docs from {dir_path}: {e}")

    return result


def parse_component_file(path: Path) -> dict:
    """Parse a component file to extract props, events, and slots."""
    try:
        with path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Extract props
        props_pattern = r"@Prop\s*(?:\([^)]*\))?\s*(\w+)"
        prop_names = re.findall(props_pattern, content)

        # Extract events
        events_pattern = r"@StencilEvent\s*(?:\([^)]*\))?\s*(\w+)"
        event_names = re.findall(events_pattern, content)

        slots = re.findall(r'<slot name="(\w+)"', content)

        # Fallback for props if using @property decorator
        if not prop_names:
            prop_names = re.findall(r"@property\(\s*\{\s*[^}]*\s*\}\s*\)\s*(\w+)", content)

        # Fallback for events if using @event decorator (less common for Stencil V2)
        if not event_names:
            event_names = re.findall(r"@event\(\s*\{\s*[^}]*\s*\}\s*\)\s*(\w+)", content)

        # Process props with details
        prop_details = []
        for prop_name_match in prop_names:
            prop_name = prop_name_match # prop_names from findall is already a list of strings
            escaped_prop_name = re.escape(prop_name)
            comment = ""

            jsdoc_pattern_prop = rf"(\/\*\*[\s\S]*?\*\/)\s*@Prop\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_prop_name}\b"
            single_line_pattern_prop = rf"(//[^\n]*)\n\s*@Prop\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_prop_name}\b"
            jsdoc_pattern_property = rf"(\/\*\*[\s\S]*?\*\/)\s*@property\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_prop_name}\b"
            single_line_pattern_property = rf"(//[^\n]*)\n\s*@property\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_prop_name}\b"

            match = re.search(jsdoc_pattern_prop, content)
            if match:
                comment = match.group(1).strip()
            else:
                match = re.search(single_line_pattern_prop, content)
                if match:
                    comment = match.group(1).strip("//").strip()
                else: 
                    match = re.search(jsdoc_pattern_property, content)
                    if match:
                        comment = match.group(1).strip()
                    else:
                        match = re.search(single_line_pattern_property, content)
                        if match:
                            comment = match.group(1).strip("//").strip()
            
            type_pattern = rf"\b{escaped_prop_name}\b\s*[:?!]\s*([^;=]+)"
            type_match = re.search(type_pattern, content)
            prop_type = ""
            if type_match:
                prop_type = type_match.group(1).strip()

            prop_details.append(
                {"name": prop_name, "description": comment, "type": prop_type}
            )

        # Process events with details
        event_details = []
        for event_name_match in event_names:
            event_name = event_name_match # event_names from findall is already a list of strings
            escaped_event_name = re.escape(event_name)
            comment = ""

            jsdoc_pattern_event = rf"(\/\*\*[\s\S]*?\*\/)\s*@StencilEvent\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_event_name}\b"
            single_line_pattern_event = rf"(//[^\n]*)\n\s*@StencilEvent\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_event_name}\b"
            # Fallback for @event decorator if needed
            jsdoc_pattern_alt_event = rf"(\/\*\*[\s\S]*?\*\/)\s*@event\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_event_name}\b"
            single_line_pattern_alt_event = rf"(//[^\n]*)\n\s*@event\s*(?:\([^)]*\))?[\s\S]*?\b{escaped_event_name}\b"

            match = re.search(jsdoc_pattern_event, content)
            if match:
                comment = match.group(1).strip()
            else:
                match = re.search(single_line_pattern_event, content)
                if match:
                    comment = match.group(1).strip("//").strip()
                else: # Fallback to @event patterns
                    match = re.search(jsdoc_pattern_alt_event, content)
                    if match:
                        comment = match.group(1).strip()
                    else:
                        match = re.search(single_line_pattern_alt_event, content)
                        if match:
                            comment = match.group(1).strip("//").strip()
            
            event_details.append({"name": event_name, "description": comment})

        # Extract default values for props
        default_values = {}
        for prop_detail_item in prop_details:
            current_prop_name = prop_detail_item["name"]
            escaped_current_prop_name = re.escape(current_prop_name)
            default_pattern = rf"\b{escaped_current_prop_name}\b\s*(?:[:?!][^=;]*)?\s*=\s*([^;]+?)\s*;"
            default_match = re.search(default_pattern, content)
            if default_match:
                default_values[current_prop_name] = default_match.group(1).strip()

        return {
            "props": prop_details,
            "events": event_details, # Now a list of dicts with name and description
            "slots": slots,
            "default_values": default_values,
        }
    except Exception as e:
        print(f"Error parsing file {path}: {e}")
        return {"props": [], "events": [], "slots": [], "default_values": {}}


def load_component_docs(repo_path: str, version: str) -> Dict[str, str]:
    """Load component documentation from the repository."""
    docs = {}

    # Find docs directory
    docs_dir = find_docs_dir(repo_path, version)

    if not os.path.exists(docs_dir):
        print(f"Documentation directory not found: {docs_dir}")
        return docs

    # Walk through all directories in the docs directory
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                component_name = os.path.splitext(file)[0]

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        docs[component_name.lower()] = content
                except Exception as e:
                    print(f"Error reading documentation file {file_path}: {e}")

    return docs


def extract_component_details(repo_path: str, version: str = "v1") -> Dict:
    """
    Extract component details from repository.

    Reads each component file and extracts properties, events, and slots.
    Also loads documentation and adds it to the details.
    """
    components = {}
    print(f"Extracting component details for {version} from {repo_path}")

    # Load component docs
    docs = load_component_docs(repo_path, version)

    # Find components directory
    components_dir = find_component_dir(repo_path, version)

    # Find storybook directory
    storybook_dir = find_storybook_dir(repo_path, version)

    if not os.path.exists(components_dir):
        print(f"Components directory not found: {components_dir}")
        return components

    # Walk through all directories in the components directory
    for root, dirs, files in os.walk(components_dir):
        for file in files:
            if file.endswith(".tsx") or file.endswith(".ts") or file.endswith(".js"):
                file_path = os.path.join(root, file)
                component_name = os.path.splitext(file)[0]

                # Skip storybook and test files
                if ".stories." in file or ".test." in file or ".spec." in file:
                    continue

                # Skip files that don't look like components
                if (
                    not component_name.startswith("modus-")
                    and "component" not in file.lower()
                ):
                    continue

                try:
                    # Parse the component file
                    parsed = parse_component_file(Path(file_path))

                    # Only add to components if it has props, events, or slots
                    if parsed["props"] or parsed["events"] or parsed["slots"]:
                        # Extract component directory name
                        component_dir = os.path.basename(os.path.dirname(file_path))
                        # Use the directory name if it's a modus component name
                        if component_dir.startswith("modus-"):
                            component_name = component_dir

                        # Add documentation if available
                        doc = docs.get(component_name.lower(), "")
                        parsed["documentation"] = doc

                        # Add storybook examples if available
                        if storybook_dir:
                            storybook_info = extract_storybook_and_docs(
                                storybook_dir, version == "v2"
                            )
                            parsed["storybook"] = storybook_info

                        components[component_name] = parsed
                        print(f"Extracted details for component: {component_name}")
                except Exception as e:
                    print(f"Error parsing component file {file_path}: {e}")

    return components


def save_analysis_to_json(component_details: Dict, output_file: str) -> None:
    """Save component analysis to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(component_details, f, indent=2)
    print(f"Analysis saved to {output_file}")


def create_manual_component_map() -> Dict:
    """
    Create a manual mapping of components between v1 and v2.
    This helps when automatic mapping is insufficient.
    """
    return {
        "v1_to_v2": {
            "modus-button": "modus-wc-button",
            "modus-alert": "modus-wc-alert",
            "modus-text-input": "modus-wc-text-input",
            "modus-textarea": "modus-wc-textarea",
            "modus-checkbox": "modus-wc-checkbox",
            "modus-radio": "modus-wc-radio",
            "modus-select": "modus-wc-select",
            "modus-breadcrumb": "modus-wc-breadcrumb",
            "modus-badge": "modus-wc-badge",
            "modus-toast": "modus-wc-toast",
            "modus-table": "modus-wc-table",
            "modus-modal": "modus-wc-modal",
        },
        "prop_mappings": {
            "modus-button": {
                "buttonStyle": "variant",
                "buttonSize": "size",
                "buttonType": "type",
            },
            "modus-alert": {
                "message": "alert-description",
                "button-text": "alert-button-text",
            },
        },
    }


def extract_framework_examples(
    repo_path: str,
    version: str,
    framework: str,
    example_repo_path_relative_to_version_root: str,
) -> Dict:
    """Extracts framework-specific examples."""
    examples = {}
    framework_examples_path = os.path.join(
        repo_path, example_repo_path_relative_to_version_root
    )

    if not os.path.exists(framework_examples_path):
        print(f"Framework examples path not found: {framework_examples_path}")
        return examples

    print(f"Extracting {framework} {version} examples from {framework_examples_path}")
    for item_name in os.listdir(framework_examples_path):
        item_path = os.path.join(framework_examples_path, item_name)
        if os.path.isfile(item_path) and (
            item_path.endswith(".tsx")
            or item_path.endswith(".ts")
            or item_path.endswith(".html")
        ):
            try:
                with open(item_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    examples[item_name] = content
                print(f"  Extracted example: {item_name}")
            except Exception as e:
                print(f"Error reading example file {item_path}: {e}")
        elif os.path.isdir(
            item_path
        ):  # Handle component-specific example folders (e.g. Angular v1)
            component_examples = {}
            for sub_item_name in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item_name)
                if os.path.isfile(sub_item_path) and (
                    sub_item_path.endswith(".tsx")
                    or sub_item_path.endswith(".ts")
                    or sub_item_path.endswith(".html")
                ):
                    try:
                        with open(sub_item_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            component_examples[sub_item_name] = content
                        print(f"  Extracted example: {item_name}/{sub_item_name}")
                    except Exception as e:
                        print(f"Error reading example file {sub_item_path}: {e}")
            if component_examples:
                examples[item_name] = component_examples

    return examples


def extract_framework_documentation(
    repo_path: str, mdx_file_path_relative_to_repo: str
) -> str:
    """Extracts the content of a framework-specific .mdx documentation file."""
    mdx_file_path = os.path.join(repo_path, mdx_file_path_relative_to_repo)
    documentation_content = ""
    if os.path.exists(mdx_file_path):
        try:
            with open(mdx_file_path, "r", encoding="utf-8") as f:
                documentation_content = f.read()
            print(f"Successfully extracted documentation from: {mdx_file_path}")
        except Exception as e:
            print(f"Error reading .mdx documentation file {mdx_file_path}: {e}")
    else:
        print(f".mdx documentation file not found: {mdx_file_path}")
    return documentation_content


def main():
    """Main function to extract component details from Modus 1.0 and 2.0 repositories"""
    print("Starting component extraction...")

    # Directory setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repos_dir = os.path.join(base_dir, "repos")
    output_dir = os.path.join(base_dir, "component_analysis")

    os.makedirs(repos_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Repository URLs and paths
    v1_repo_url = "https://github.com/trimble-oss/modus-web-components.git"
    v2_repo_url = "https://github.com/trimble-oss/modus-wc-2.0.git"

    v1_repo_path = os.path.join(repos_dir, "modus-web-components")
    v2_repo_path = os.path.join(repos_dir, "modus-wc-2.0")

    # Clone repositories if they don't exist
    clone_repo(v1_repo_url, v1_repo_path, False)
    clone_repo(v2_repo_url, v2_repo_path, False)

    # Modus 1.0 paths
    v1_components_dir = os.path.join(
        v1_repo_path, "stencil-workspace", "src", "components"
    )
    v1_storybook_dir = os.path.join(
        v1_repo_path, "stencil-workspace", "storybook", "stories", "components"
    )

    # Modus 2.0 paths
    v2_components_dir = os.path.join(v2_repo_path, "src", "components")

    # Framework example paths
    v1_angular_examples_path = os.path.join(
        "angular-workspace", "test-ng15", "src", "examples"
    )
    v1_react_examples_path = os.path.join(
        "react-workspace", "test-react-v17", "src", "examples"
    )  # Assuming v17 examples are representative for v1
    v2_react_examples_path_v17 = os.path.join(
        "integrations", "react", "test-react-v17", "src", "examples"
    )
    # V2 Angular does not have a dedicated examples directory like v1

    # Framework .mdx documentation paths
    v1_angular_mdx_path = os.path.join(
        "stencil-workspace",
        "storybook",
        "stories",
        "framework-integrations",
        "angular.mdx",
    )
    v1_react_mdx_path = os.path.join(
        "stencil-workspace",
        "storybook",
        "stories",
        "framework-integrations",
        "react.mdx",
    )
    v2_angular_mdx_path = os.path.join("src", "stories", "frameworks", "angular.mdx")
    v2_react_mdx_path = os.path.join("src", "stories", "frameworks", "react.mdx")

    # Validate paths
    print("\n=== Directory Validation ===")
    print(f"Modus 1.0 components directory exists: {os.path.exists(v1_components_dir)}")
    print(f"Modus 1.0 storybook directory exists: {os.path.exists(v1_storybook_dir)}")
    print(f"Modus 2.0 components directory exists: {os.path.exists(v2_components_dir)}")

    # Process Modus 1.0 components
    print("\n=== Extracting Modus 1.0 Components ===")
    v1_components = {}

    if os.path.exists(v1_components_dir):
        for component_name in os.listdir(v1_components_dir):
            component_dir = os.path.join(v1_components_dir, component_name)
            if os.path.isdir(component_dir) and component_name.startswith("modus-"):
                print(f"Processing component: {component_name}")

                # Find the main component file
                tsx_files = [
                    f
                    for f in os.listdir(component_dir)
                    if f.endswith(".tsx")
                    and not f.endswith(".spec.tsx")
                    and not f.endswith(".e2e.tsx")
                    and not f.endswith(".stories.tsx")
                ]

                if tsx_files:
                    # Use the first component file
                    component_file = os.path.join(component_dir, tsx_files[0])
                    component_details = parse_component_file(Path(component_file))

                    # Extract storybook and docs
                    docs_info = {
                        "documentation": "",
                        "storybook_content": "",
                        "examples": [],
                        "variants": [],
                        "prop_usage": {},
                    }
                    if os.path.exists(v1_storybook_dir):
                        component_story_dir = os.path.join(
                            v1_storybook_dir, component_name
                        )
                        if os.path.exists(component_story_dir):
                            print(
                                f"  Extracting docs and storybook content for: {component_name}"
                            )
                            docs_info = extract_storybook_and_docs(
                                component_story_dir, is_v2=False
                            )

                    component_details["documentation"] = docs_info["documentation"]
                    component_details["storybook_content"] = docs_info[
                        "storybook_content"
                    ]
                    component_details["storybook"] = {
                        "examples": docs_info["examples"],
                        "variants": docs_info["variants"],
                        "prop_usage": docs_info["prop_usage"],
                    }
                    component_details["tag_name"] = component_name
                    v1_components[component_name] = component_details

    # Process Modus 2.0 components
    print("\n=== Extracting Modus 2.0 Components ===")
    v2_components = {}

    if os.path.exists(v2_components_dir):
        for component_name in os.listdir(v2_components_dir):
            component_dir = os.path.join(v2_components_dir, component_name)
            if os.path.isdir(component_dir) and component_name.startswith("modus-wc-"):
                print(f"Processing component: {component_name}")

                # Find the main component file
                tsx_files = [
                    f
                    for f in os.listdir(component_dir)
                    if f.endswith(".tsx")
                    and not f.endswith(".spec.tsx")
                    and not f.endswith(".stories.tsx")
                ]

                if tsx_files:
                    # Use the first component file
                    component_file = os.path.join(component_dir, tsx_files[0])
                    component_details = parse_component_file(Path(component_file))

                    # Extract storybook and docs (for v2, they're in the same directory)
                    print(
                        f"  Extracting docs and storybook content for: {component_name}"
                    )
                    docs_info = extract_storybook_and_docs(component_dir, is_v2=True)

                    component_details["documentation"] = docs_info["documentation"]
                    component_details["storybook"] = {
                        "examples": docs_info["examples"],
                        "variants": docs_info["variants"],
                        "prop_usage": docs_info["prop_usage"],
                    }
                    component_details["tag_name"] = component_name
                    v2_components[component_name] = component_details

    # Create a simple mapping between v1 and v2 components
    component_mapping = {}
    for v1_name in v1_components:
        v2_name = v1_name.replace("modus-", "modus-wc-")

        # Special case for breadcrumbs (plural in v2)
        if v1_name == "modus-breadcrumb" and "modus-wc-breadcrumbs" in v2_components:
            v2_name = "modus-wc-breadcrumbs"

        if v2_name in v2_components:
            # Simple mapping - just component names
            component_mapping[v1_name] = {"v2_component": v2_name}

    # Extract framework-specific data (documentation and examples)
    print("\n=== Extracting Framework Specific Data ===")

    # V1 Angular
    v1_angular_docs = extract_framework_documentation(v1_repo_path, v1_angular_mdx_path)
    v1_angular_examples = extract_framework_examples(
        v1_repo_path, "v1", "Angular", v1_angular_examples_path
    )
    v1_angular_framework_data = {
        "documentation": v1_angular_docs,
        "examples": v1_angular_examples,
    }

    # V1 React
    v1_react_docs = extract_framework_documentation(v1_repo_path, v1_react_mdx_path)
    v1_react_examples = extract_framework_examples(
        v1_repo_path, "v1", "React", v1_react_examples_path
    )
    v1_react_framework_data = {
        "documentation": v1_react_docs,
        "examples": v1_react_examples,
    }

    # V2 Angular
    v2_angular_docs = extract_framework_documentation(v2_repo_path, v2_angular_mdx_path)
    # V2 Angular examples are not in a dedicated directory, so this will likely be empty or based on .mdx content if adapted later
    v2_angular_examples = (
        {}
    )  # Or adapt extract_framework_examples if specific v2 angular examples can be found elsewhere
    v2_angular_framework_data = {
        "documentation": v2_angular_docs,
        "examples": v2_angular_examples,
    }

    # V2 React
    v2_react_docs = extract_framework_documentation(v2_repo_path, v2_react_mdx_path)
    v2_react_examples_v17 = extract_framework_examples(
        v2_repo_path, "v2", "React v17", v2_react_examples_path_v17
    )
    # Consolidate v2 React examples if multiple versions are extracted (e.g., v18, v19)
    v2_react_examples_consolidated = {}
    if v2_react_examples_v17:
        v2_react_examples_consolidated.update(v2_react_examples_v17)
    v2_react_framework_data = {
        "documentation": v2_react_docs,
        "examples": v2_react_examples_consolidated,
    }

    # Save results
    with open(os.path.join(output_dir, "v1_components.json"), "w") as f:
        json.dump(v1_components, f, indent=2)

    with open(os.path.join(output_dir, "v2_components.json"), "w") as f:
        json.dump(v2_components, f, indent=2)

    # Generate and update component mapping
    # Path to the component_mapping.json file
    mapping_file_path = os.path.join(output_dir, "component_mapping.json")
    
    full_mapping_data = {"Mapping_v1_v2": {}, "verification_rules": [], "migration_plan": []} # Default structure

    # Try to load existing mapping file
    if os.path.exists(mapping_file_path):
        try:
            with open(mapping_file_path, "r", encoding="utf-8") as f:
                full_mapping_data = json.load(f)
            # Ensure essential keys exist and have correct types, or initialize them
            if not isinstance(full_mapping_data.get("Mapping_v1_v2"), dict):
                print(f"Warning: 'Mapping_v1_v2' key missing or not a dict in {mapping_file_path}. Initializing.")
                full_mapping_data["Mapping_v1_v2"] = {}
            if not isinstance(full_mapping_data.get("verification_rules"), list):
                full_mapping_data["verification_rules"] = []
            if not isinstance(full_mapping_data.get("migration_plan"), list):
                full_mapping_data["migration_plan"] = []
        except json.JSONDecodeError:
            print(f"Warning: Could not decode existing {mapping_file_path}. A new default structure will be used.")
            # full_mapping_data will use the default structure initialized above
    else:
        print(f"Note: {mapping_file_path} not found. A new one will be created with a default structure.")

    # Generate new mappings based on detected v1_components and v2_components
    script_generated_v1_to_v2_map = {}
    for v1_name_key in v1_components.keys(): # v1_components is a dict { "modus-button": {details...}, ... }
        v2_name_candidate = "" # Initialize candidate for each v1 component

        # Handle specific known mappings first
        if v1_name_key == "modus-breadcrumb":
            if "modus-wc-breadcrumbs" in v2_components:
                v2_name_candidate = "modus-wc-breadcrumbs"
        elif v1_name_key == "modus-switch":
            if "modus-wc-toggle" in v2_components: # As per user's likely preference from existing JSON
                v2_name_candidate = "modus-wc-toggle"
            elif "modus-wc-switch" in v2_components: # Fallback if modus-wc-toggle is not found
                 v2_name_candidate = "modus-wc-switch"
        elif v1_name_key == "modus-list":
            if "modus-wc-menu" in v2_components:
                v2_name_candidate = "modus-wc-menu"
        elif v1_name_key == "modus-list-item":
            if "modus-wc-menu-item" in v2_components:
                v2_name_candidate = "modus-wc-menu-item"
        # Add other specific, non-standard mappings here if necessary

        # Default rule if no special mapping produced a candidate
        if not v2_name_candidate:
            simple_candidate = v1_name_key.replace("modus-", "modus-wc-")
            if simple_candidate in v2_components:
                v2_name_candidate = simple_candidate

        # Assign to the script-generated map
        if v2_name_candidate: # If any rule resulted in a V2 component name
            script_generated_v1_to_v2_map[v1_name_key] = v2_name_candidate
        else:
            script_generated_v1_to_v2_map[v1_name_key] = "Not Found"
    
    # Update the Mapping_v1_v2 part of the loaded (or default) full_mapping_data
    # This ensures that mappings for components found by the script are updated/added,
    # while manual mappings for items not processed by the script (e.g., HTML tags) are preserved.
    full_mapping_data["Mapping_v1_v2"].update(script_generated_v1_to_v2_map)

    # Save the updated (or new) full mapping data, including preserved sections
    with open(mapping_file_path, "w", encoding="utf-8") as f:
        json.dump(full_mapping_data, f, indent=2)
    print(f"Component mapping updated and saved to {mapping_file_path}")

    # Save framework-specific data
    with open(os.path.join(output_dir, "v1_angular_framework_data.json"), "w") as f:
        json.dump(v1_angular_framework_data, f, indent=2)

    with open(os.path.join(output_dir, "v1_react_framework_data.json"), "w") as f:
        json.dump(v1_react_framework_data, f, indent=2)

    with open(os.path.join(output_dir, "v2_angular_framework_data.json"), "w") as f:
        json.dump(v2_angular_framework_data, f, indent=2)

    with open(os.path.join(output_dir, "v2_react_framework_data.json"), "w") as f:
        json.dump(v2_react_framework_data, f, indent=2)

    print(f"\nExtraction complete:")
    print(f"- Found {len(v1_components)} Modus 1.0 components")
    print(f"- Found {len(v2_components)} Modus 2.0 components")
    print(f"- Created mapping for {len(component_mapping)} components")
    print(
        f"- Extracted V1 Angular framework data (docs + {len(v1_angular_examples)} examples)"
    )
    print(
        f"- Extracted V1 React framework data (docs + {len(v1_react_examples)} examples)"
    )
    print(
        f"- Extracted V2 Angular framework data (docs + {len(v2_angular_examples)} examples)"
    )
    print(
        f"- Extracted V2 React framework data (docs + {len(v2_react_examples_consolidated)} examples)"
    )
    print(f"Results saved to the {output_dir} directory.")


if __name__ == "__main__":
    main()
