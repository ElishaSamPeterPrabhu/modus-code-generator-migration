#!/usr/bin/env python3
"""
Reorganize component files into a single folder with version suffixes.
This script moves all component files from v1_components/ and v2_components/ 
into the main component_analysis folder with -v1 and -v2 suffixes.
Also generates a lightweight components-v1-v2-unified.json mapping index.
"""

import os
import shutil
import json
from pathlib import Path

# V1 components that have partial V2 equivalents (not all features carry over)
PARTIAL_MAPPINGS = {
    "modus-data-table",  # maps to modus-wc-table but missing many V1 sub-features
}

# Manual mapping overrides for components the extractor marks as "Not Found"
# but which do have V2 equivalents
MAPPING_OVERRIDES = {
    "modus-spinner": "modus-wc-loader",
    "modus-progress-bar": "modus-wc-progress",
    "modus-dropdown": "modus-wc-dropdown-menu",
    "modus-radio-group": "modus-wc-radio",
    "modus-date-input": "modus-wc-date",
    "modus-date-picker": "modus-wc-date",
    "modus-textarea-input": "modus-wc-textarea",
    "modus-time-picker": "modus-wc-time-input",
    "modus-sentiment-scale": "modus-wc-rating",
    "modus-accordion-item": "modus-wc-accordion",
    "modus-icons": "modus-wc-icon",
    "modus-data-table": "modus-wc-table",
}


def v2_tag_to_filename(v2_tag: str) -> str:
    """Convert a modus-wc-* tag to its -v2.json filename.
    E.g. 'modus-wc-button' -> 'button-v2.json'
         'modus-wc-dropdown-menu' -> 'dropdown-menu-v2.json'
    """
    if not v2_tag or v2_tag == "Not Found":
        return None
    stem = v2_tag.replace("modus-wc-", "")
    return f"{stem}-v2.json"


def v1_tag_to_filename(v1_tag: str, component_analysis_dir: Path) -> str:
    """Convert a V1 tag to its -v1.json filename if the file exists.
    E.g. 'modus-button' -> 'button-v1.json'
    """
    stem = v1_tag.replace("modus-", "")
    candidate = f"{stem}-v1.json"
    if (component_analysis_dir / candidate).exists():
        return candidate
    return None


def generate_v1_v2_unified_mapping(component_analysis_dir: Path):
    """Generate components-v1-v2-unified.json — a lightweight lookup index
    mapping each V1 component to its V2 equivalent, with file references."""

    mapping_path = component_analysis_dir / "component_mapping.json"
    if not mapping_path.exists():
        print("  ⚠️  component_mapping.json not found, skipping unified mapping.")
        return

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    raw_mapping = mapping_data.get("Mapping_v1_v2", {})

    # Apply overrides for known "Not Found" entries that do have V2 equivalents
    for v1_tag, v2_tag in MAPPING_OVERRIDES.items():
        if raw_mapping.get(v1_tag) == "Not Found":
            raw_mapping[v1_tag] = v2_tag

    # Persist the updated mapping back so component_mapping.json stays in sync
    mapping_data["Mapping_v1_v2"] = raw_mapping
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, indent=2)
    print("  ✅ Updated component_mapping.json with corrected mappings")

    # Build the unified index (only for modus-* V1 components, skip HTML tag aliases)
    unified = {}
    for v1_tag, v2_tag in sorted(raw_mapping.items()):
        # Skip HTML tag aliases (label, p, h1..h6, button, hr, textarea, input type=...)
        if not v1_tag.startswith("modus-") and not v1_tag.startswith("flex-"):
            continue

        v2_resolved = v2_tag if v2_tag != "Not Found" else None
        v2_file = v2_tag_to_filename(v2_resolved) if v2_resolved else None
        v1_file = v1_tag_to_filename(v1_tag, component_analysis_dir)

        unified[v1_tag] = {
            "v1_tag": v1_tag,
            "v2_tag": v2_resolved,
            "v1_file": v1_file,
            "v2_file": v2_file,
            "partial": v1_tag in PARTIAL_MAPPINGS,
        }

    unified_path = component_analysis_dir / "components-v1-v2-unified.json"
    with open(unified_path, "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2)

    mapped = sum(1 for v in unified.values() if v["v2_tag"])
    not_found = sum(1 for v in unified.values() if not v["v2_tag"])
    partial = sum(1 for v in unified.values() if v["partial"])
    print(
        f"  ✅ Created components-v1-v2-unified.json "
        f"({mapped} mapped, {not_found} not found, {partial} partial)"
    )


def reorganize_components():
    """Reorganize all component files into single folder with version suffixes"""
    
    # Base paths
    base_dir = Path("/Users/eprabhu/Desktop/Projects/modus-code-generator-migration")
    component_analysis_dir = base_dir / "modus_migration" / "component_analysis"
    
    # Source directories
    v1_dir = component_analysis_dir / "v1_components"
    v2_dir = component_analysis_dir / "v2_components"
    
    print("🔄 Starting component reorganization...")
    print(f"Target folder: {component_analysis_dir}")
    
    # Check if source directories exist
    if not v1_dir.exists():
        print(f"❌ V1 directory not found: {v1_dir}")
        return False
        
    if not v2_dir.exists():
        print(f"❌ V2 directory not found: {v2_dir}")
        return False
    
    # Process V1 components
    print(f"\n📁 Processing V1 components from {v1_dir}")
    v1_files = list(v1_dir.glob("*.json"))
    
    for file_path in v1_files:
        if file_path.name == "_index.json":
            # Rename index file
            new_name = "components-index-v1.json"
        else:
            # Add -v1 suffix to component files
            component_name = file_path.stem  # filename without extension
            new_name = f"{component_name}-v1.json"
        
        new_path = component_analysis_dir / new_name
        
        # Copy file to new location
        shutil.copy2(file_path, new_path)
        print(f"  ✅ {file_path.name} → {new_name}")
    
    # Process V2 components
    print(f"\n📁 Processing V2 components from {v2_dir}")
    v2_files = list(v2_dir.glob("*.json"))
    
    for file_path in v2_files:
        if file_path.name == "_index.json":
            # Rename index file
            new_name = "components-index-v2.json"
        else:
            # Add -v2 suffix to component files
            component_name = file_path.stem  # filename without extension
            new_name = f"{component_name}-v2.json"
        
        new_path = component_analysis_dir / new_name
        
        # Copy file to new location
        shutil.copy2(file_path, new_path)
        print(f"  ✅ {file_path.name} → {new_name}")
    
    # Create unified index file
    print(f"\n📋 Creating unified component index...")
    
    # Load both index files
    v1_index_path = component_analysis_dir / "components-index-v1.json"
    v2_index_path = component_analysis_dir / "components-index-v2.json"
    
    unified_index = {
        "description": "Unified index of all Modus components (V1 and V2)",
        "total_components": 0,
        "v1_components": {},
        "v2_components": {},
        "file_naming": {
            "v1_pattern": "{component_name}-v1.json",
            "v2_pattern": "{component_name}-v2.json",
            "index_v1": "components-index-v1.json",
            "index_v2": "components-index-v2.json"
        },
        "usage": {
            "get_v1_component": "Use filename: {component_name}-v1.json",
            "get_v2_component": "Use filename: {component_name}-v2.json",
            "examples": [
                "button-v1.json (V1 button component)",
                "button-v2.json (V2 button component)",
                "text-input-v1.json (V1 text input)",
                "text-input-v2.json (V2 text input)"
            ]
        }
    }
    
    # Load V1 index
    if v1_index_path.exists():
        with open(v1_index_path, 'r', encoding='utf-8') as f:
            v1_data = json.load(f)
            unified_index["v1_components"] = v1_data.get("components", {})
            print(f"  📊 Loaded {len(unified_index['v1_components'])} V1 components")
    
    # Load V2 index
    if v2_index_path.exists():
        with open(v2_index_path, 'r', encoding='utf-8') as f:
            v2_data = json.load(f)
            unified_index["v2_components"] = v2_data.get("components", {})
            print(f"  📊 Loaded {len(unified_index['v2_components'])} V2 components")
    
    unified_index["total_components"] = len(unified_index["v1_components"]) + len(unified_index["v2_components"])
    
    # Save unified index
    unified_index_path = component_analysis_dir / "components-unified-index.json"
    with open(unified_index_path, 'w', encoding='utf-8') as f:
        json.dump(unified_index, f, indent=2)
    
    print(f"  ✅ Created unified index: {unified_index_path.name}")
    
    # Generate lightweight V1→V2 unified mapping index
    print(f"\n🗺️  Generating V1→V2 unified mapping index...")
    generate_v1_v2_unified_mapping(component_analysis_dir)

    # Summary
    print(f"\n🎉 Reorganization Complete!")
    print(f"📊 Summary:")
    print(f"  • V1 files moved: {len(v1_files)}")
    print(f"  • V2 files moved: {len(v2_files)}")
    print(f"  • Total files in folder: {len(v1_files) + len(v2_files) + 1} (including unified index)")
    print(f"  • Target folder: modus_migration/component_analysis/")
    
    # Show sample files
    print(f"\n📁 Sample files created:")
    sample_files = list(component_analysis_dir.glob("*-v*.json"))[:10]
    for file_path in sample_files:
        print(f"  • {file_path.name}")
    
    if len(sample_files) >= 10:
        remaining = len(list(component_analysis_dir.glob("*-v*.json"))) - 10
        print(f"  • ... and {remaining} more files")
    
    return True

if __name__ == "__main__":
    success = reorganize_components()
    if success:
        print(f"\n✅ All files ready for n8n!")
        print(f"📂 Use folder: modus_migration/component_analysis/")
        print(f"📋 File pattern: {{component_name}}-{{version}}.json")
    else:
        print(f"\n❌ Reorganization failed!")
