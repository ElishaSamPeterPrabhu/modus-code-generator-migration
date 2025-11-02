#!/usr/bin/env node
/**
 * Advanced MUI component extraction using TypeScript Compiler API
 * This extracts complete component information including props, types, and documentation
 */

const ts = require('typescript');
const fs = require('fs');
const path = require('path');

// Configuration
const MUI_PACKAGE_PATH = 'node_modules/@mui/material';
const OUTPUT_DIR = './mui_migration/component_extraction';

/**
 * Extract props from a TypeScript interface
 */
function extractPropsFromInterface(checker, symbol) {
  const props = [];
  
  if (symbol && symbol.members) {
    symbol.members.forEach((prop, propName) => {
      const propType = checker.getTypeOfSymbolAtLocation(prop, prop.valueDeclaration);
      const propTypeString = checker.typeToString(propType);
      
      // Get JSDoc comments
      const jsDocs = prop.getJsDocTags();
      const description = jsDocs
        .filter(tag => tag.name === 'description')
        .map(tag => tag.text)
        .join(' ') || '';
      
      // Check if required
      const isOptional = prop.valueDeclaration && 
        ts.isPropertySignature(prop.valueDeclaration) && 
        prop.valueDeclaration.questionToken;
      
      props.push({
        name: propName.toString(),
        type: propTypeString,
        description: description || `${propName} property`,
        required: !isOptional,
        default: extractDefaultValue(jsDocs)
      });
    });
  }
  
  return props;
}

/**
 * Extract default value from JSDoc
 */
function extractDefaultValue(jsDocs) {
  const defaultTag = jsDocs.find(tag => tag.name === 'default');
  return defaultTag ? defaultTag.text : undefined;
}

/**
 * Parse a component file to extract props
 */
function extractComponentData(componentPath, componentName) {
  const program = ts.createProgram([componentPath], {
    target: ts.ScriptTarget.ESNext,
    module: ts.ModuleKind.ESNext,
    jsx: ts.JsxEmit.React,
    esModuleInterop: true,
    allowSyntheticDefaultImports: true,
  });
  
  const checker = program.getTypeChecker();
  const sourceFile = program.getSourceFile(componentPath);
  
  if (!sourceFile) {
    console.error(`Could not load ${componentPath}`);
    return null;
  }
  
  const componentData = {
    component_name: componentName,
    import_path: `@mui/material/${componentName}`,
    props: [],
    events: [],
    slots: []
  };
  
  // Visit AST nodes
  function visit(node) {
    // Look for interface declarations
    if (ts.isInterfaceDeclaration(node)) {
      const interfaceName = node.name.text;
      
      // Check if this is the props interface
      if (interfaceName === `${componentName}Props` || 
          interfaceName === `${componentName}PropsWithRef`) {
        const symbol = checker.getSymbolAtLocation(node.name);
        componentData.props = extractPropsFromInterface(checker, symbol);
      }
    }
    
    // Look for exported component
    if (ts.isExportAssignment(node) || ts.isExportDeclaration(node)) {
      // Extract additional metadata if needed
    }
    
    ts.forEachChild(node, visit);
  }
  
  visit(sourceFile);
  
  // Extract events from props (props that start with 'on')
  componentData.events = componentData.props
    .filter(prop => prop.name.startsWith('on'))
    .map(prop => ({
      name: prop.name,
      type: prop.type,
      description: prop.description
    }));
  
  return componentData;
}

/**
 * Get all MUI components
 */
function getAllMUIComponents() {
  const componentsDir = path.join(MUI_PACKAGE_PATH, 'src');
  const components = [];
  
  if (fs.existsSync(componentsDir)) {
    const items = fs.readdirSync(componentsDir);
    
    for (const item of items) {
      const itemPath = path.join(componentsDir, item);
      const stat = fs.statSync(itemPath);
      
      // Check if it's a component directory
      if (stat.isDirectory() && /^[A-Z]/.test(item)) {
        // Look for the main component file
        const componentFiles = [
          path.join(itemPath, `${item}.d.ts`),
          path.join(itemPath, `${item}.tsx`),
          path.join(itemPath, `${item}.js`),
          path.join(itemPath, 'index.d.ts')
        ];
        
        for (const file of componentFiles) {
          if (fs.existsSync(file)) {
            components.push({
              name: item,
              path: file
            });
            break;
          }
        }
      }
    }
  }
  
  return components;
}

/**
 * Extract component API from package.json exports
 */
function extractFromPackageExports() {
  const packageJsonPath = path.join(MUI_PACKAGE_PATH, 'package.json');
  
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    
    // Extract component list from exports
    if (packageJson.exports) {
      const components = [];
      
      for (const [key, value] of Object.entries(packageJson.exports)) {
        if (key.startsWith('./') && !key.includes('*')) {
          const componentName = key.slice(2); // Remove './'
          if (/^[A-Z]/.test(componentName)) {
            components.push(componentName);
          }
        }
      }
      
      return components;
    }
  }
  
  return [];
}

/**
 * Main extraction function
 */
async function extractAllComponents() {
  console.log('MUI Component Extraction Started...\n');
  
  // Ensure MUI is installed
  if (!fs.existsSync(MUI_PACKAGE_PATH)) {
    console.error('MUI not found! Please run: npm install @mui/material');
    process.exit(1);
  }
  
  // Create output directory
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }
  
  // Get all components
  const components = getAllMUIComponents();
  const packageComponents = extractFromPackageExports();
  
  console.log(`Found ${components.length} components in source`);
  console.log(`Found ${packageComponents.length} components in exports\n`);
  
  const allComponentData = {};
  const componentIndex = [];
  
  // Extract data for each component
  for (const component of components) {
    console.log(`Extracting ${component.name}...`);
    
    try {
      const data = extractComponentData(component.path, component.name);
      
      if (data) {
        allComponentData[component.name] = data;
        
        // Save individual component file
        const outputPath = path.join(
          OUTPUT_DIR, 
          `${component.name.toLowerCase()}-mui-v7-auto.json`
        );
        fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
        
        // Add to index
        componentIndex.push({
          file: `${component.name.toLowerCase()}-mui-v7-auto.json`,
          component_name: component.name,
          import_path: data.import_path,
          props_count: data.props.length,
          events_count: data.events.length,
          has_slots: data.slots.length > 0
        });
      }
    } catch (error) {
      console.error(`Error extracting ${component.name}:`, error.message);
    }
  }
  
  // Save unified index
  const indexData = {
    description: "MUI v7 Components (Auto-extracted)",
    version: "7.x",
    extraction_date: new Date().toISOString(),
    total_components: Object.keys(allComponentData).length,
    components: componentIndex
  };
  
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'mui_v7_components_auto_complete.json'),
    JSON.stringify(indexData, null, 2)
  );
  
  // Save all components data
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'all_mui_components_auto.json'),
    JSON.stringify(allComponentData, null, 2)
  );
  
  console.log(`\nExtraction complete!`);
  console.log(`- Extracted ${Object.keys(allComponentData).length} components`);
  console.log(`- Output directory: ${OUTPUT_DIR}`);
}

// Run extraction
extractAllComponents().catch(console.error);
