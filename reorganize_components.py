#!/usr/bin/env python3
"""
Reorganize component files into a single folder with version suffixes.
This script moves all component files from v1_components/ and v2_components/ 
into the main component_analysis folder with -v1 and -v2 suffixes.
"""

import os
import shutil
import json
from pathlib import Path

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
