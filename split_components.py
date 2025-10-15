#!/usr/bin/env python3
"""
Split large component JSON files into individual component files.
This improves data management and reduces file size for GitHub/n8n retrieval.
"""

import json
import os
from pathlib import Path


def split_components_json(input_file: str, output_dir: str, version: str):
    """Split a components JSON file into individual component files."""
    print(f"\n{'='*60}")
    print(f"Splitting {input_file} into {output_dir}/")
    print(f"{'='*60}")
    
    # Load the large JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        components_data = json.load(f)
    
    print(f"Found {len(components_data)} components")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each component to its own file
    for component_name, component_data in components_data.items():
        # Clean component name for filename (remove prefix)
        clean_name = component_name.replace('modus-wc-', '').replace('modus-', '')
        output_file = os.path.join(output_dir, f"{clean_name}.json")
        
        # Add component name to the data
        component_data_with_name = {
            "component_name": component_name,
            "version": version,
            **component_data
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(component_data_with_name, f, indent=2)
        
        print(f"  ✓ Saved: {clean_name}.json ({len(json.dumps(component_data)):,} bytes)")
    
    print(f"\n✅ Successfully split {len(components_data)} components")
    return len(components_data)


def create_index_file(output_dir: str, version: str):
    """Create an index file listing all components."""
    print(f"\nCreating index file for {output_dir}/")
    
    # Get all JSON files in the directory
    json_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.json') and f != '_index.json'])
    
    index_data = {
        "version": version,
        "total_components": len(json_files),
        "components": []
    }
    
    for json_file in json_files:
        file_path = os.path.join(output_dir, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            component_data = json.load(f)
        
        component_name = component_data.get('component_name', json_file.replace('.json', ''))
        props_count = len(component_data.get('props', []))
        events_count = len(component_data.get('events', []))
        slots_count = len(component_data.get('slots', []))
        
        index_data["components"].append({
            "file": json_file,
            "component_name": component_name,
            "props_count": props_count,
            "events_count": events_count,
            "slots_count": slots_count
        })
    
    # Save index file
    index_file = os.path.join(output_dir, '_index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    
    print(f"  ✓ Created index: _index.json")
    return index_data


def move_framework_data():
    """Move framework data files to framework_data folder."""
    print(f"\n{'='*60}")
    print("Organizing framework data files")
    print(f"{'='*60}")
    
    base_dir = os.path.join(os.path.dirname(__file__), 'modus_migration', 'component_analysis')
    framework_dir = os.path.join(base_dir, 'framework_data')
    
    framework_files = [
        'v1_angular_framework_data.json',
        'v1_react_framework_data.json',
        'v2_angular_framework_data.json',
        'v2_react_framework_data.json'
    ]
    
    for file_name in framework_files:
        src_path = os.path.join(base_dir, file_name)
        if os.path.exists(src_path):
            # Just create a symlink or note - don't actually move to preserve existing structure
            print(f"  ✓ Found: {file_name}")
        else:
            print(f"  ✗ Missing: {file_name}")
    
    print(f"\n📝 Note: Framework data files remain in place for backwards compatibility")


def main():
    """Main function to split all component files."""
    base_dir = os.path.join(os.path.dirname(__file__), 'modus_migration', 'component_analysis')
    
    print("\n" + "="*60)
    print("MODUS COMPONENT DATA MODULARIZATION")
    print("="*60)
    print("Converting large JSON files into modular component files")
    print("This improves:")
    print("  • Data management and maintenance")
    print("  • GitHub API retrieval performance")
    print("  • n8n workflow efficiency")
    print("="*60)
    
    # Split V1 components
    v1_input = os.path.join(base_dir, 'v1_components.json')
    v1_output = os.path.join(base_dir, 'v1_components')
    
    if os.path.exists(v1_input):
        v1_count = split_components_json(v1_input, v1_output, 'v1')
        v1_index = create_index_file(v1_output, 'v1')
    else:
        print(f"❌ Error: {v1_input} not found")
        v1_count = 0
    
    # Split V2 components
    v2_input = os.path.join(base_dir, 'v2_components.json')
    v2_output = os.path.join(base_dir, 'v2_components')
    
    if os.path.exists(v2_input):
        v2_count = split_components_json(v2_input, v2_output, 'v2')
        v2_index = create_index_file(v2_output, 'v2')
    else:
        print(f"❌ Error: {v2_input} not found")
        v2_count = 0
    
    # Note about framework data
    move_framework_data()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"V1 Components: {v1_count} components split into individual files")
    print(f"V2 Components: {v2_count} components split into individual files")
    print(f"Total Files Created: {v1_count + v2_count + 2} (including 2 index files)")
    print("\nDirectory Structure:")
    print("  component_analysis/")
    print("    ├── v1_components/")
    print(f"    │   ├── _index.json")
    print(f"    │   ├── button.json")
    print(f"    │   ├── alert.json")
    print(f"    │   └── ... ({v1_count} total)")
    print("    ├── v2_components/")
    print(f"    │   ├── _index.json")
    print(f"    │   ├── button.json")
    print(f"    │   ├── alert.json")
    print(f"    │   └── ... ({v2_count} total)")
    print("    ├── component_mapping.json")
    print("    ├── v1_angular_framework_data.json")
    print("    ├── v1_react_framework_data.json")
    print("    ├── v2_angular_framework_data.json")
    print("    └── v2_react_framework_data.json")
    print("="*60)
    print("\n✅ Modularization complete!")
    print("\nNext steps:")
    print("  1. Update component_extractor.py to use modular structure")
    print("  2. Update MCP tool descriptions")
    print("  3. Test GitHub API retrieval with smaller files")


if __name__ == "__main__":
    main()

