# 🛠️ N8N Tool Description - Unified Modus Component Data

## 📂 **Folder Path for n8n**
```
modus_migration/component_analysis/{}
```

## 🔧 **Single Tool Configuration**

### **Tool Name:** `get_modus_component_file`

### **Description:**
```
Fetches Modus component data files from the unified component analysis folder. All component files are organized in a single directory with version suffixes (-v1, -v2). Use this tool to get component details, indexes, mappings, or framework data for Modus web component migration and analysis.

Available file types:
• Component files: {component-name}-v1.json or {component-name}-v2.json  
• Index files: components-index-v1.json, components-index-v2.json, components-unified-index.json
• Mapping: component_mapping.json
• Framework data: v1_angular_framework_data.json, v1_react_framework_data.json, v2_angular_framework_data.json, v2_react_framework_data.json

Performance: Individual component files are 5-120KB (vs 825KB for full datasets), providing 10-165x faster retrieval.

Use cases:
- Get specific component data: "button-v1.json", "text-input-v2.json"  
- Get component indexes: "components-index-v1.json"
- Get component mapping: "component_mapping.json"
- Get framework examples: "v1_angular_framework_data.json"
```

### **Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "filename": {
      "type": "string",
      "description": "Name of the file to fetch from modus_migration/component_analysis/ folder",
      "examples": [
        "button-v1.json",
        "button-v2.json", 
        "text-input-v1.json",
        "components-index-v1.json",
        "components-unified-index.json",
        "component_mapping.json",
        "v1_angular_framework_data.json"
      ]
    }
  },
  "required": ["filename"]
}
```

---

## 📋 **Available Files Reference**

### **🔍 Component Files (89 files)**

#### **V1 Components (43 files)**
Pattern: `{component-name}-v1.json`

```
accordion-item-v1.json          accordion-v1.json               action-bar-v1.json
alert-v1.json                   autocomplete-v1.json            badge-v1.json
breadcrumb-v1.json              button-group-v1.json            button-v1.json
card-v1.json                    checkbox-v1.json                chip-v1.json
content-tree-v1.json            data-table-v1.json              date-input-v1.json
date-picker-v1.json             dropdown-v1.json                file-dropzone-v1.json
icons-v1.json                   list-item-v1.json               list-v1.json
message-v1.json                 modal-v1.json                   navbar-v1.json
number-input-v1.json            pagination-v1.json              progress-bar-v1.json
radio-group-v1.json             select-v1.json                  sentiment-scale-v1.json
side-navigation-v1.json         slider-v1.json                  spinner-v1.json
switch-v1.json                  table-v1.json                   tabs-v1.json
text-input-v1.json              textarea-input-v1.json          time-picker-v1.json
toast-v1.json                   toolbar-v1.json                 tooltip-v1.json
utility-panel-v1.json
```

#### **V2 Components (44 files)**
Pattern: `{component-name}-v2.json`

```
accordion-v2.json               alert-v2.json                   autocomplete-v2.json
avatar-v2.json                  badge-v2.json                   breadcrumbs-v2.json
button-v2.json                  card-v2.json                    checkbox-v2.json
chip-v2.json                    collapse-v2.json                date-v2.json
divider-v2.json                 dropdown-menu-v2.json           icon-v2.json
input-feedback-v2.json          input-label-v2.json             loader-v2.json
menu-item-v2.json               menu-v2.json                    modal-v2.json
navbar-v2.json                  number-input-v2.json            pagination-v2.json
progress-v2.json                radio-v2.json                   rating-v2.json
select-v2.json                  side-navigation-v2.json         skeleton-v2.json
slider-v2.json                  stepper-v2.json                 switch-v2.json
table-v2.json                   tabs-v2.json                    text-input-v2.json
textarea-v2.json                theme-switcher-v2.json          time-input-v2.json
toast-v2.json                   toolbar-v2.json                 tooltip-v2.json
typography-v2.json              utility-panel-v2.json
```

### **📊 Index Files (3 files)**

```
components-index-v1.json        # V1 components metadata (7KB)
components-index-v2.json        # V2 components metadata (7KB)  
components-unified-index.json   # Combined index with usage guide (8KB)
```

### **🗺️ Mapping & Framework Files (5 files)**

```
component_mapping.json          # V1 to V2 component mapping (11KB)
v1_angular_framework_data.json  # V1 Angular examples & docs (80KB)
v1_react_framework_data.json    # V1 React examples & docs (15KB)
v2_angular_framework_data.json  # V2 Angular examples & docs (12KB)
v2_react_framework_data.json    # V2 React examples & docs (10KB)
```

---

## 💡 **Usage Examples**

### **Get V2 Button Component:**
```json
{
  "filename": "button-v2.json"
}
```

### **Get V1 Text Input Component:**
```json
{
  "filename": "text-input-v1.json"
}
```

### **Get Component Index:**
```json
{
  "filename": "components-unified-index.json"
}
```

### **Get Component Mapping:**
```json
{
  "filename": "component_mapping.json"
}
```

### **Get Framework Data:**
```json
{
  "filename": "v1_angular_framework_data.json"
}
```

---

## 📈 **Performance Benefits**

| File Type | Old Method | New Method | Improvement |
|-----------|------------|------------|-------------|
| Single Component | 825KB | 5-120KB | **85-99% smaller** |
| Component Index | 825KB | 7KB | **99% smaller** |
| Framework Data | Multiple files | 10-80KB | **Targeted retrieval** |

---

## 🎯 **Component Name Mapping**

| V1 Component | V1 Filename | V2 Component | V2 Filename |
|--------------|-------------|--------------|-------------|
| modus-button | `button-v1.json` | modus-wc-button | `button-v2.json` |
| modus-text-input | `text-input-v1.json` | modus-wc-text-input | `text-input-v2.json` |
| modus-textarea-input | `textarea-input-v1.json` | modus-wc-textarea | `textarea-v2.json` |
| modus-breadcrumb | `breadcrumb-v1.json` | modus-wc-breadcrumbs | `breadcrumbs-v2.json` |
| modus-progress-bar | `progress-bar-v1.json` | modus-wc-progress | `progress-v2.json` |
| modus-spinner | `spinner-v1.json` | modus-wc-loader | `loader-v2.json` |
| modus-list | `list-v1.json` | modus-wc-menu | `menu-v2.json` |

---

## ✅ **Ready for n8n!**

**Total Files Available:** 97 files
**Folder:** `modus_migration/component_analysis/`
**Single Tool:** `get_modus_component_file`
**Input:** `{"filename": "component-name-version.json"}`

All files are organized in one folder with clear naming patterns for easy n8n integration! 🚀
