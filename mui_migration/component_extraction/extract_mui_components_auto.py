#!/usr/bin/env python3
"""
Extract MUI v7 component data directly from MUI packages/documentation.
This script fetches component information from MUI's actual source rather than hardcoding.
"""

import json
import os
import requests
import subprocess
from typing import Dict, List, Any
import ast
import re

def fetch_mui_component_api(component_name: str) -> Dict[str, Any]:
    """
    Fetch component API documentation from MUI's API docs.
    
    Args:
        component_name: The component name (e.g., 'button', 'text-field')
    
    Returns:
        Dict containing component API information
    """
    # MUI API documentation URL pattern
    base_url = "https://raw.githubusercontent.com/mui/material-ui/master/docs/pages/material-ui/api"
    
    try:
        # Try to fetch the component's API JSON
        response = requests.get(f"{base_url}/{component_name}.json")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching {component_name}: {e}")
    
    return None

def extract_from_typescript_definitions():
    """
    Extract component props from MUI TypeScript definitions.
    This requires having @mui/material installed.
    """
    try:
        # Install MUI if not already installed
        subprocess.run(["npm", "install", "@mui/material@latest", "--save-dev"], 
                      capture_output=True, text=True)
        
        # Path to MUI type definitions
        mui_types_path = "node_modules/@mui/material"
        
        components_data = {}
        
        # List of core MUI components to extract
        mui_components = [
            "Accordion", "Alert", "AppBar", "Autocomplete", "Avatar", "Backdrop",
            "Badge", "BottomNavigation", "Box", "Breadcrumbs", "Button", "ButtonGroup",
            "Card", "Checkbox", "Chip", "CircularProgress", "Collapse", "Container",
            "Dialog", "Divider", "Drawer", "Fab", "FormControl", "FormControlLabel",
            "FormGroup", "FormHelperText", "FormLabel", "Grid", "Icon", "IconButton",
            "ImageList", "Input", "InputAdornment", "InputBase", "InputLabel",
            "LinearProgress", "Link", "List", "ListItem", "ListItemAvatar",
            "ListItemButton", "ListItemIcon", "ListItemText", "Menu", "MenuItem",
            "Modal", "Pagination", "Paper", "Popover", "Popper", "Radio",
            "RadioGroup", "Rating", "Select", "Skeleton", "Slider", "Snackbar",
            "SpeedDial", "Stack", "Step", "StepButton", "StepContent", "StepIcon",
            "StepLabel", "Stepper", "Switch", "Tab", "Table", "TableBody",
            "TableCell", "TableContainer", "TableHead", "TablePagination",
            "TableRow", "Tabs", "TextField", "ToggleButton", "ToggleButtonGroup",
            "Toolbar", "Tooltip", "Typography"
        ]
        
        for component in mui_components:
            component_path = os.path.join(mui_types_path, component, "index.d.ts")
            
            if os.path.exists(component_path):
                with open(component_path, 'r') as f:
                    content = f.read()
                    
                # Extract props interface using regex
                props_match = re.search(rf"export interface {component}Props[^{{]*{{([^}}]+)}}", 
                                      content, re.DOTALL)
                
                if props_match:
                    props_content = props_match.group(1)
                    props = parse_typescript_props(props_content)
                    
                    components_data[component] = {
                        "component_name": component,
                        "import_path": f"@mui/material/{component}",
                        "props": props,
                        "has_types": True
                    }
        
        return components_data
        
    except Exception as e:
        print(f"Error extracting from TypeScript definitions: {e}")
        return {}

def parse_typescript_props(props_content: str) -> List[Dict[str, str]]:
    """
    Parse TypeScript interface content to extract prop definitions.
    """
    props = []
    
    # Basic regex to extract prop definitions
    # This is simplified - a full parser would be more complex
    prop_pattern = r'^\s*(\w+)\??:\s*([^;]+);'
    
    for match in re.finditer(prop_pattern, props_content, re.MULTILINE):
        prop_name = match.group(1)
        prop_type = match.group(2).strip()
        
        # Skip internal props
        if prop_name.startswith('_'):
            continue
            
        props.append({
            "name": prop_name,
            "type": prop_type,
            "description": f"Property {prop_name} of type {prop_type}",
            "required": not match.group(0).strip().startswith(prop_name + '?')
        })
    
    return props

def fetch_from_mui_docs_api():
    """
    Fetch component data from MUI's documentation API endpoints.
    """
    # MUI documentation API endpoints
    api_base = "https://mui.com/api"
    
    # Core components list
    components = [
        "accordion", "alert", "app-bar", "autocomplete", "avatar", "backdrop",
        "badge", "bottom-navigation", "box", "breadcrumbs", "button", "button-group",
        "card", "checkbox", "chip", "circular-progress", "collapse", "container",
        "dialog", "divider", "drawer", "fab", "form-control", "form-control-label",
        "grid", "icon", "icon-button", "linear-progress", "link", "list",
        "menu", "modal", "pagination", "paper", "popover", "radio",
        "rating", "select", "skeleton", "slider", "snackbar", "speed-dial",
        "stack", "stepper", "switch", "tabs", "text-field", "toggle-button",
        "toolbar", "tooltip", "typography"
    ]
    
    components_data = {}
    
    for component in components:
        try:
            # Construct API documentation URL
            url = f"{api_base}/{component}/"
            
            # Note: This would need proper web scraping or API access
            # For now, we'll structure the data format
            component_key = component.replace('-', '_').title().replace('_', '')
            
            components_data[component_key] = {
                "component_name": component_key,
                "import_path": f"@mui/material/{component_key}",
                "api_url": url,
                "props": [],  # Would be populated from actual API/scraping
                "events": [],
                "slots": []
            }
            
        except Exception as e:
            print(f"Error processing {component}: {e}")
    
    return components_data

def extract_from_mui_github():
    """
    Extract component information directly from MUI's GitHub repository.
    """
    github_api = "https://api.github.com/repos/mui/material-ui/contents"
    components_base = "/packages/mui-material/src"
    
    try:
        # Get list of components from GitHub
        response = requests.get(f"{github_api}{components_base}")
        
        if response.status_code == 200:
            items = response.json()
            components_data = {}
            
            for item in items:
                if item['type'] == 'dir' and item['name'][0].isupper():
                    component_name = item['name']
                    
                    # Try to fetch the component's props interface
                    props_url = f"{github_api}{components_base}/{component_name}/{component_name}.d.ts"
                    props_response = requests.get(props_url)
                    
                    if props_response.status_code == 200:
                        # Parse the TypeScript definition file
                        content = requests.get(props_response.json()['download_url']).text
                        
                        # Extract props (simplified parsing)
                        props = extract_props_from_content(content, component_name)
                        
                        components_data[component_name] = {
                            "component_name": component_name,
                            "import_path": f"@mui/material/{component_name}",
                            "props": props,
                            "github_path": item['path']
                        }
            
            return components_data
            
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
        return {}

def extract_props_from_content(content: str, component_name: str) -> List[Dict[str, Any]]:
    """
    Extract props from TypeScript definition content.
    """
    props = []
    
    # Look for the props interface
    pattern = rf"export interface {component_name}Props(?:.*?){{(.*?)}}"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        props_content = match.group(1)
        
        # Extract individual props (simplified)
        prop_pattern = r'^\s*(\w+)\??:\s*([^;]+);.*?(?:/\*\*(.*?)\*/)?'
        
        for prop_match in re.finditer(prop_pattern, props_content, re.MULTILINE | re.DOTALL):
            prop_name = prop_match.group(1)
            prop_type = prop_match.group(2).strip()
            prop_desc = prop_match.group(3) or ""
            
            if prop_desc:
                prop_desc = " ".join(prop_desc.split())
            
            props.append({
                "name": prop_name,
                "type": prop_type,
                "description": prop_desc.strip() if prop_desc else f"{prop_name} property",
                "required": '?' not in prop_match.group(0)
            })
    
    return props

def generate_extraction_script():
    """
    Generate a Node.js script to extract MUI component data.
    """
    node_script = """
const fs = require('fs');
const path = require('path');

// This script should be run in a project with @mui/material installed
// npm install @mui/material @emotion/react @emotion/styled

async function extractMUIComponents() {
  const components = {};
  
  try {
    // Import all MUI components
    const mui = await import('@mui/material');
    
    // List of component names to extract
    const componentNames = [
      'Accordion', 'Alert', 'AppBar', 'Autocomplete', 'Avatar',
      'Badge', 'Box', 'Breadcrumbs', 'Button', 'ButtonGroup',
      'Card', 'CardContent', 'CardActions', 'Checkbox', 'Chip',
      'CircularProgress', 'Container', 'Dialog', 'Divider', 'Drawer',
      'Fab', 'FormControl', 'FormControlLabel', 'FormGroup', 'FormHelperText',
      'Grid', 'Icon', 'IconButton', 'LinearProgress', 'List', 'ListItem',
      'Menu', 'MenuItem', 'Modal', 'Pagination', 'Paper', 'Popover',
      'Radio', 'RadioGroup', 'Rating', 'Select', 'Skeleton', 'Slider',
      'Snackbar', 'Stack', 'Stepper', 'Switch', 'Tab', 'Table',
      'Tabs', 'TextField', 'ToggleButton', 'ToggleButtonGroup',
      'Toolbar', 'Tooltip', 'Typography'
    ];
    
    for (const name of componentNames) {
      const Component = mui[name];
      
      if (Component) {
        // Extract component information
        components[name] = {
          component_name: name,
          import_path: `@mui/material/${name}`,
          displayName: Component.displayName || name,
          // Note: Props would need to be extracted from TypeScript definitions
          // This is a runtime extraction which has limitations
          props: [],
          events: []
        };
      }
    }
    
    // Save the extracted data
    fs.writeFileSync(
      'mui_components_extracted.json',
      JSON.stringify(components, null, 2)
    );
    
    console.log('Extraction complete! Check mui_components_extracted.json');
    
  } catch (error) {
    console.error('Error extracting components:', error);
  }
}

extractMUIComponents();
"""
    
    # Save the Node.js extraction script
    with open('mui_migration/component_extraction/extract_mui_node.js', 'w') as f:
        f.write(node_script)
    
    print("Generated extract_mui_node.js - run with: node extract_mui_node.js")

def main():
    """
    Main function to coordinate MUI component extraction.
    """
    print("MUI Component Data Extraction")
    print("=" * 50)
    
    # Method 1: Try to extract from TypeScript definitions
    print("\n1. Attempting to extract from TypeScript definitions...")
    ts_data = extract_from_typescript_definitions()
    
    # Method 2: Try to fetch from GitHub
    print("\n2. Attempting to extract from GitHub...")
    github_data = extract_from_mui_github()
    
    # Method 3: Generate Node.js extraction script
    print("\n3. Generating Node.js extraction script...")
    generate_extraction_script()
    
    # Combine data from different sources
    combined_data = {**ts_data, **github_data}
    
    # Save combined data
    output_path = "mui_migration/component_extraction/mui_v7_components_auto.json"
    with open(output_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"\nExtracted data for {len(combined_data)} components")
    print(f"Saved to: {output_path}")
    
    # Instructions for complete extraction
    print("\nFor complete extraction:")
    print("1. Run: npm install @mui/material@latest")
    print("2. Run: node mui_migration/component_extraction/extract_mui_node.js")
    print("3. Use TypeScript compiler API for detailed prop extraction")

if __name__ == "__main__":
    main()
