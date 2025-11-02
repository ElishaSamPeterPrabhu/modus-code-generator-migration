#!/usr/bin/env python3
"""
Extract MUI v7 component data and create JSON files similar to Modus component structure.
This script will create a comprehensive list of MUI components with their properties, events, and types.
"""

import json
import os
from typing import Dict, List, Any

# MUI v7 component list with their properties and mapping information
MUI_COMPONENTS = {
    "Button": {
        "component_name": "Button",
        "import_path": "@mui/material/Button",
        "props": [
            {"name": "children", "type": "React.ReactNode", "description": "The content of the button"},
            {"name": "color", "type": "'inherit' | 'primary' | 'secondary' | 'success' | 'error' | 'info' | 'warning'", "description": "The color of the button"},
            {"name": "disabled", "type": "boolean", "description": "If true, the button will be disabled"},
            {"name": "disableElevation", "type": "boolean", "description": "If true, no elevation is used"},
            {"name": "disableFocusRipple", "type": "boolean", "description": "If true, the keyboard focus ripple will be disabled"},
            {"name": "disableRipple", "type": "boolean", "description": "If true, the ripple effect will be disabled"},
            {"name": "endIcon", "type": "React.ReactNode", "description": "Element placed after the children"},
            {"name": "fullWidth", "type": "boolean", "description": "If true, the button will take up the full width of its container"},
            {"name": "href", "type": "string", "description": "The URL to link to when the button is clicked"},
            {"name": "size", "type": "'small' | 'medium' | 'large'", "description": "The size of the button"},
            {"name": "startIcon", "type": "React.ReactNode", "description": "Element placed before the children"},
            {"name": "variant", "type": "'text' | 'outlined' | 'contained'", "description": "The variant to use"},
            {"name": "onClick", "type": "(event: React.MouseEvent<HTMLButtonElement>) => void", "description": "Callback fired when the button is clicked"},
            {"name": "sx", "type": "SxProps<Theme>", "description": "The system prop that allows defining system overrides as well as additional CSS styles"}
        ],
        "events": ["onClick"],
        "default_values": {
            "color": "primary",
            "disabled": False,
            "disableElevation": False,
            "disableFocusRipple": False,
            "disableRipple": False,
            "fullWidth": False,
            "size": "medium",
            "variant": "text"
        }
    },
    "TextField": {
        "component_name": "TextField",
        "import_path": "@mui/material/TextField",
        "props": [
            {"name": "autoComplete", "type": "string", "description": "This prop helps users to fill forms faster"},
            {"name": "autoFocus", "type": "boolean", "description": "If true, the input element will be focused during the first mount"},
            {"name": "color", "type": "'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'", "description": "The color of the component"},
            {"name": "defaultValue", "type": "any", "description": "The default value of the input element"},
            {"name": "disabled", "type": "boolean", "description": "If true, the input element will be disabled"},
            {"name": "error", "type": "boolean", "description": "If true, the label will be displayed in an error state"},
            {"name": "fullWidth", "type": "boolean", "description": "If true, the input will take up the full width of its container"},
            {"name": "helperText", "type": "React.ReactNode", "description": "The helper text content"},
            {"name": "id", "type": "string", "description": "The id of the input element"},
            {"name": "label", "type": "React.ReactNode", "description": "The label content"},
            {"name": "multiline", "type": "boolean", "description": "If true, a textarea element will be rendered instead of an input"},
            {"name": "name", "type": "string", "description": "Name attribute of the input element"},
            {"name": "onChange", "type": "(event: React.ChangeEvent<HTMLInputElement>) => void", "description": "Callback fired when the value is changed"},
            {"name": "placeholder", "type": "string", "description": "The short hint displayed in the input before the user enters a value"},
            {"name": "required", "type": "boolean", "description": "If true, the label is displayed as required"},
            {"name": "rows", "type": "string | number", "description": "Number of rows to display when multiline option is set to true"},
            {"name": "size", "type": "'small' | 'medium'", "description": "The size of the text field"},
            {"name": "type", "type": "string", "description": "Type of the input element"},
            {"name": "value", "type": "any", "description": "The value of the input element"},
            {"name": "variant", "type": "'filled' | 'outlined' | 'standard'", "description": "The variant to use"}
        ],
        "events": ["onChange", "onBlur", "onFocus"],
        "default_values": {
            "color": "primary",
            "disabled": False,
            "error": False,
            "fullWidth": False,
            "multiline": False,
            "required": False,
            "size": "medium",
            "variant": "outlined"
        }
    },
    "Checkbox": {
        "component_name": "Checkbox",
        "import_path": "@mui/material/Checkbox",
        "props": [
            {"name": "checked", "type": "boolean", "description": "If true, the component is checked"},
            {"name": "color", "type": "'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'", "description": "The color of the component"},
            {"name": "defaultChecked", "type": "boolean", "description": "The default checked state"},
            {"name": "disabled", "type": "boolean", "description": "If true, the checkbox will be disabled"},
            {"name": "disableRipple", "type": "boolean", "description": "If true, the ripple effect will be disabled"},
            {"name": "icon", "type": "React.ReactNode", "description": "The icon to display when the component is unchecked"},
            {"name": "checkedIcon", "type": "React.ReactNode", "description": "The icon to display when the component is checked"},
            {"name": "id", "type": "string", "description": "The id of the input element"},
            {"name": "indeterminate", "type": "boolean", "description": "If true, the component appears indeterminate"},
            {"name": "indeterminateIcon", "type": "React.ReactNode", "description": "The icon to display when the component is indeterminate"},
            {"name": "inputProps", "type": "object", "description": "Attributes applied to the input element"},
            {"name": "inputRef", "type": "React.Ref<HTMLInputElement>", "description": "Pass a ref to the input element"},
            {"name": "name", "type": "string", "description": "Name attribute of the input element"},
            {"name": "onChange", "type": "(event: React.ChangeEvent<HTMLInputElement>) => void", "description": "Callback fired when the state is changed"},
            {"name": "required", "type": "boolean", "description": "If true, the input element will be required"},
            {"name": "size", "type": "'small' | 'medium' | 'large'", "description": "The size of the checkbox"},
            {"name": "value", "type": "any", "description": "The value of the component"}
        ],
        "events": ["onChange"],
        "default_values": {
            "color": "primary",
            "disabled": False,
            "disableRipple": False,
            "indeterminate": False,
            "required": False,
            "size": "medium"
        }
    },
    "Select": {
        "component_name": "Select",
        "import_path": "@mui/material/Select",
        "props": [
            {"name": "autoWidth", "type": "boolean", "description": "If true, the width of the popover will automatically be set according to the items inside the menu"},
            {"name": "children", "type": "React.ReactNode", "description": "The option elements to populate the select with"},
            {"name": "defaultOpen", "type": "boolean", "description": "If true, the component is initially open"},
            {"name": "defaultValue", "type": "any", "description": "The default value"},
            {"name": "disabled", "type": "boolean", "description": "If true, the select will be disabled"},
            {"name": "displayEmpty", "type": "boolean", "description": "If true, a value is displayed even if no items are selected"},
            {"name": "error", "type": "boolean", "description": "If true, the label will be displayed in an error state"},
            {"name": "fullWidth", "type": "boolean", "description": "If true, the input will take up the full width of its container"},
            {"name": "IconComponent", "type": "elementType", "description": "The icon that displays the arrow"},
            {"name": "id", "type": "string", "description": "The id of the wrapper element"},
            {"name": "input", "type": "element", "description": "An Input element"},
            {"name": "inputProps", "type": "object", "description": "Attributes applied to the input element"},
            {"name": "label", "type": "React.ReactNode", "description": "The label content"},
            {"name": "labelId", "type": "string", "description": "The ID of an element that acts as an additional label"},
            {"name": "MenuProps", "type": "object", "description": "Props applied to the Menu element"},
            {"name": "multiple", "type": "boolean", "description": "If true, value must be an array and the menu will support multiple selections"},
            {"name": "name", "type": "string", "description": "Name attribute of the select or hidden input element"},
            {"name": "native", "type": "boolean", "description": "If true, the component will be using a native select element"},
            {"name": "onChange", "type": "(event: SelectChangeEvent<T>) => void", "description": "Callback fired when a menu item is selected"},
            {"name": "onClose", "type": "(event: React.SyntheticEvent) => void", "description": "Callback fired when the component requests to be closed"},
            {"name": "onOpen", "type": "(event: React.SyntheticEvent) => void", "description": "Callback fired when the component requests to be opened"},
            {"name": "open", "type": "boolean", "description": "If true, the component is shown"},
            {"name": "renderValue", "type": "(value: T) => React.ReactNode", "description": "Render the selected value"},
            {"name": "required", "type": "boolean", "description": "If true, the label is displayed as required"},
            {"name": "value", "type": "T", "description": "The input value"},
            {"name": "variant", "type": "'filled' | 'outlined' | 'standard'", "description": "The variant to use"}
        ],
        "events": ["onChange", "onClose", "onOpen"],
        "default_values": {
            "autoWidth": False,
            "defaultOpen": False,
            "disabled": False,
            "displayEmpty": False,
            "error": False,
            "fullWidth": False,
            "multiple": False,
            "native": False,
            "required": False,
            "variant": "outlined"
        }
    },
    "Card": {
        "component_name": "Card",
        "import_path": "@mui/material/Card",
        "props": [
            {"name": "children", "type": "React.ReactNode", "description": "The content of the component"},
            {"name": "raised", "type": "boolean", "description": "If true, the card will use raised styling"},
            {"name": "sx", "type": "SxProps<Theme>", "description": "The system prop that allows defining system overrides"}
        ],
        "events": [],
        "default_values": {
            "raised": False
        }
    },
    "Dialog": {
        "component_name": "Dialog",
        "import_path": "@mui/material/Dialog",
        "props": [
            {"name": "children", "type": "React.ReactNode", "description": "Dialog children, usually the included sub-components"},
            {"name": "disableEscapeKeyDown", "type": "boolean", "description": "If true, hitting escape will not fire the onClose callback"},
            {"name": "fullScreen", "type": "boolean", "description": "If true, the dialog will be full-screen"},
            {"name": "fullWidth", "type": "boolean", "description": "If true, the dialog stretches to maxWidth"},
            {"name": "maxWidth", "type": "'xs' | 'sm' | 'md' | 'lg' | 'xl' | false", "description": "Determine the max-width of the dialog"},
            {"name": "onClose", "type": "(event: object, reason: 'escapeKeyDown' | 'backdropClick') => void", "description": "Callback fired when the component requests to be closed"},
            {"name": "open", "type": "boolean", "description": "If true, the component is shown"},
            {"name": "PaperComponent", "type": "elementType", "description": "The component used to render the body of the dialog"},
            {"name": "PaperProps", "type": "object", "description": "Props applied to the Paper element"},
            {"name": "scroll", "type": "'body' | 'paper'", "description": "Determine the container for scrolling the dialog"},
            {"name": "TransitionComponent", "type": "elementType", "description": "The component used for the transition"},
            {"name": "transitionDuration", "type": "number | object", "description": "The duration for the transition"}
        ],
        "events": ["onClose"],
        "default_values": {
            "disableEscapeKeyDown": False,
            "fullScreen": False,
            "fullWidth": False,
            "maxWidth": "sm",
            "open": False,
            "scroll": "paper"
        }
    },
    "Alert": {
        "component_name": "Alert", 
        "import_path": "@mui/material/Alert",
        "props": [
            {"name": "action", "type": "React.ReactNode", "description": "The action to display"},
            {"name": "children", "type": "React.ReactNode", "description": "The content of the component"},
            {"name": "closeText", "type": "string", "description": "Override the default label for the close popup icon button"},
            {"name": "color", "type": "'error' | 'info' | 'success' | 'warning'", "description": "The main color for the alert"},
            {"name": "icon", "type": "React.ReactNode | false", "description": "Override the icon displayed before the children"},
            {"name": "iconMapping", "type": "object", "description": "The component maps the severity prop to a range of different icons"},
            {"name": "onClose", "type": "(event: React.SyntheticEvent) => void", "description": "Callback fired when the component requests to be closed"},
            {"name": "severity", "type": "'error' | 'info' | 'success' | 'warning'", "description": "The severity of the alert"},
            {"name": "variant", "type": "'filled' | 'outlined' | 'standard'", "description": "The variant to use"}
        ],
        "events": ["onClose"],
        "default_values": {
            "closeText": "Close",
            "severity": "success",
            "variant": "standard"
        }
    },
    "Chip": {
        "component_name": "Chip",
        "import_path": "@mui/material/Chip",
        "props": [
            {"name": "avatar", "type": "element", "description": "Avatar element"},
            {"name": "clickable", "type": "boolean", "description": "If true, the chip will appear clickable"},
            {"name": "color", "type": "'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'", "description": "The color of the component"},
            {"name": "deleteIcon", "type": "element", "description": "Override the default delete icon element"},
            {"name": "disabled", "type": "boolean", "description": "If true, the chip will be disabled"},
            {"name": "icon", "type": "element", "description": "Icon element"},
            {"name": "label", "type": "React.ReactNode", "description": "The content of the label"},
            {"name": "onDelete", "type": "(event: React.SyntheticEvent) => void", "description": "Callback fired when the delete icon is clicked"},
            {"name": "size", "type": "'small' | 'medium'", "description": "The size of the chip"},
            {"name": "variant", "type": "'filled' | 'outlined'", "description": "The variant to use"}
        ],
        "events": ["onClick", "onDelete"],
        "default_values": {
            "clickable": False,
            "color": "default",
            "disabled": False,
            "size": "medium",
            "variant": "filled"
        }
    },
    "Switch": {
        "component_name": "Switch",
        "import_path": "@mui/material/Switch",
        "props": [
            {"name": "checked", "type": "boolean", "description": "If true, the component is checked"},
            {"name": "color", "type": "'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'", "description": "The color of the component"},
            {"name": "defaultChecked", "type": "boolean", "description": "The default checked state"},
            {"name": "disabled", "type": "boolean", "description": "If true, the switch will be disabled"},
            {"name": "disableRipple", "type": "boolean", "description": "If true, the ripple effect will be disabled"},
            {"name": "edge", "type": "'end' | 'start' | false", "description": "If given, uses a negative margin to counteract the padding on one side"},
            {"name": "id", "type": "string", "description": "The id of the input element"},
            {"name": "inputProps", "type": "object", "description": "Attributes applied to the input element"},
            {"name": "inputRef", "type": "React.Ref<HTMLInputElement>", "description": "Pass a ref to the input element"},
            {"name": "onChange", "type": "(event: React.ChangeEvent<HTMLInputElement>) => void", "description": "Callback fired when the state is changed"},
            {"name": "required", "type": "boolean", "description": "If true, the input element will be required"},
            {"name": "size", "type": "'small' | 'medium'", "description": "The size of the switch"},
            {"name": "value", "type": "any", "description": "The value of the component"}
        ],
        "events": ["onChange"],
        "default_values": {
            "color": "primary",
            "disabled": False,
            "disableRipple": False,
            "edge": False,
            "required": False,
            "size": "medium"
        }
    },
    "Table": {
        "component_name": "Table",
        "import_path": "@mui/material/Table",
        "props": [
            {"name": "children", "type": "React.ReactNode", "description": "The content of the table, normally TableHead and TableBody"},
            {"name": "padding", "type": "'normal' | 'checkbox' | 'none'", "description": "Allows TableCells to inherit padding of the Table"},
            {"name": "size", "type": "'small' | 'medium'", "description": "Allows TableCells to inherit size of the Table"},
            {"name": "stickyHeader", "type": "boolean", "description": "Set the header sticky"}
        ],
        "events": [],
        "default_values": {
            "padding": "normal",
            "size": "medium",
            "stickyHeader": False
        }
    },
    "Tabs": {
        "component_name": "Tabs",
        "import_path": "@mui/material/Tabs",
        "props": [
            {"name": "action", "type": "React.Ref<TabsActions>", "description": "Callback fired when the component mounts"},
            {"name": "allowScrollButtonsMobile", "type": "boolean", "description": "If true, the scroll buttons aren't forced hidden on mobile"},
            {"name": "aria-label", "type": "string", "description": "The label for the Tabs as a string"},
            {"name": "aria-labelledby", "type": "string", "description": "An id or list of ids separated by a space that label the Tabs"},
            {"name": "centered", "type": "boolean", "description": "If true, the tabs will be centered"},
            {"name": "children", "type": "React.ReactNode", "description": "The content of the component"},
            {"name": "indicatorColor", "type": "'primary' | 'secondary'", "description": "Determines the color of the indicator"},
            {"name": "onChange", "type": "(event: React.SyntheticEvent, value: any) => void", "description": "Callback fired when the value changes"},
            {"name": "orientation", "type": "'horizontal' | 'vertical'", "description": "The tabs orientation"},
            {"name": "scrollButtons", "type": "'auto' | false | true", "description": "Determine behavior of scroll buttons when tabs are set to scroll"},
            {"name": "selectionFollowsFocus", "type": "boolean", "description": "If true the selected tab changes on focus"},
            {"name": "TabIndicatorProps", "type": "object", "description": "Props applied to the tab indicator element"},
            {"name": "TabScrollButtonProps", "type": "object", "description": "Props applied to the TabScrollButton element"},
            {"name": "textColor", "type": "'inherit' | 'primary' | 'secondary'", "description": "Determines the color of the Tab"},
            {"name": "value", "type": "any", "description": "The value of the currently selected Tab"},
            {"name": "variant", "type": "'fullWidth' | 'scrollable' | 'standard'", "description": "Determines additional display behavior of the tabs"}
        ],
        "events": ["onChange"],
        "default_values": {
            "allowScrollButtonsMobile": False,
            "centered": False,
            "indicatorColor": "primary",
            "orientation": "horizontal",
            "scrollButtons": "auto",
            "selectionFollowsFocus": False,
            "textColor": "primary",
            "variant": "standard"
        }
    },
    "Accordion": {
        "component_name": "Accordion",
        "import_path": "@mui/material/Accordion",
        "props": [
            {"name": "children", "type": "React.ReactNode", "description": "The content of the component"},
            {"name": "defaultExpanded", "type": "boolean", "description": "If true, expands the accordion by default"},
            {"name": "disabled", "type": "boolean", "description": "If true, the component will be disabled"},
            {"name": "disableGutters", "type": "boolean", "description": "If true, it removes the margin between two expanded accordion items"},
            {"name": "expanded", "type": "boolean", "description": "If true, expands the accordion, otherwise collapse it"},
            {"name": "onChange", "type": "(event: React.SyntheticEvent, expanded: boolean) => void", "description": "Callback fired when the expand/collapse state is changed"},
            {"name": "square", "type": "boolean", "description": "If true, rounded corners are disabled"},
            {"name": "TransitionComponent", "type": "elementType", "description": "The component used for the transition"},
            {"name": "TransitionProps", "type": "object", "description": "Props applied to the transition element"}
        ],
        "events": ["onChange"],
        "default_values": {
            "defaultExpanded": False,
            "disabled": False,
            "disableGutters": False,
            "square": False
        }
    },
    "Badge": {
        "component_name": "Badge",
        "import_path": "@mui/material/Badge",
        "props": [
            {"name": "anchorOrigin", "type": "{ horizontal: 'left' | 'right', vertical: 'bottom' | 'top' }", "description": "The anchor of the badge"},
            {"name": "badgeContent", "type": "React.ReactNode", "description": "The content rendered within the badge"},
            {"name": "children", "type": "React.ReactNode", "description": "The badge will be added relative to this node"},
            {"name": "color", "type": "'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'", "description": "The color of the component"},
            {"name": "invisible", "type": "boolean", "description": "If true, the badge will be invisible"},
            {"name": "max", "type": "number", "description": "Max count to show"},
            {"name": "overlap", "type": "'circular' | 'rectangular'", "description": "Wrapped shape the badge should overlap"},
            {"name": "showZero", "type": "boolean", "description": "Controls whether the badge is hidden when badgeContent is zero"},
            {"name": "variant", "type": "'dot' | 'standard'", "description": "The variant to use"}
        ],
        "events": [],
        "default_values": {
            "anchorOrigin": { "horizontal": "right", "vertical": "top" },
            "color": "default",
            "invisible": False,
            "max": 99,
            "overlap": "rectangular",
            "showZero": False,
            "variant": "standard"
        }
    },
    "Avatar": {
        "component_name": "Avatar",
        "import_path": "@mui/material/Avatar",
        "props": [
            {"name": "alt", "type": "string", "description": "Used in combination with src or srcSet to provide an alt attribute"},
            {"name": "children", "type": "React.ReactNode", "description": "Used to render icon or text elements inside the Avatar"},
            {"name": "imgProps", "type": "object", "description": "Attributes applied to the img element if the component is used to display an image"},
            {"name": "sizes", "type": "string", "description": "The sizes attribute for the img element"},
            {"name": "src", "type": "string", "description": "The src attribute for the img element"},
            {"name": "srcSet", "type": "string", "description": "The srcSet attribute for the img element"},
            {"name": "variant", "type": "'circular' | 'rounded' | 'square'", "description": "The shape of the avatar"}
        ],
        "events": [],
        "default_values": {
            "variant": "circular"
        }
    },
    "Tooltip": {
        "component_name": "Tooltip",
        "import_path": "@mui/material/Tooltip",
        "props": [
            {"name": "arrow", "type": "boolean", "description": "If true, adds an arrow to the tooltip"},
            {"name": "children", "type": "element", "description": "Tooltip reference element"},
            {"name": "describeChild", "type": "boolean", "description": "Set to true if the title acts as an accessible description"},
            {"name": "disableFocusListener", "type": "boolean", "description": "Do not respond to focus-visible events"},
            {"name": "disableHoverListener", "type": "boolean", "description": "Do not respond to hover events"},
            {"name": "disableInteractive", "type": "boolean", "description": "Makes a tooltip not interactive"},
            {"name": "disableTouchListener", "type": "boolean", "description": "Do not respond to long press touch events"},
            {"name": "enterDelay", "type": "number", "description": "The number of milliseconds to wait before showing the tooltip"},
            {"name": "enterNextDelay", "type": "number", "description": "The number of milliseconds to wait before showing the tooltip when one was already recently opened"},
            {"name": "enterTouchDelay", "type": "number", "description": "The number of milliseconds a user must touch the element before showing the tooltip"},
            {"name": "followCursor", "type": "boolean", "description": "If true, the tooltip follow the cursor over the wrapped element"},
            {"name": "id", "type": "string", "description": "This prop is used to help implement the accessibility logic"},
            {"name": "leaveDelay", "type": "number", "description": "The number of milliseconds to wait before hiding the tooltip"},
            {"name": "leaveTouchDelay", "type": "number", "description": "The number of milliseconds after the user stops touching an element before hiding the tooltip"},
            {"name": "onClose", "type": "(event: React.SyntheticEvent | Event) => void", "description": "Callback fired when the component requests to be closed"},
            {"name": "onOpen", "type": "(event: React.SyntheticEvent | Event) => void", "description": "Callback fired when the component requests to be open"},
            {"name": "open", "type": "boolean", "description": "If true, the component is shown"},
            {"name": "placement", "type": "'bottom-end' | 'bottom-start' | 'bottom' | 'left-end' | 'left-start' | 'left' | 'right-end' | 'right-start' | 'right' | 'top-end' | 'top-start' | 'top'", "description": "Tooltip placement"},
            {"name": "title", "type": "React.ReactNode", "description": "Tooltip title"}
        ],
        "events": ["onClose", "onOpen"],
        "default_values": {
            "arrow": False,
            "describeChild": False,
            "disableFocusListener": False,
            "disableHoverListener": False,
            "disableInteractive": False,
            "disableTouchListener": False,
            "enterDelay": 100,
            "enterNextDelay": 0,
            "enterTouchDelay": 700,
            "followCursor": False,
            "leaveDelay": 0,
            "leaveTouchDelay": 1500,
            "placement": "bottom"
        }
    },
    "Slider": {
        "component_name": "Slider",
        "import_path": "@mui/material/Slider",
        "props": [
            {"name": "aria-label", "type": "string", "description": "The label of the slider"},
            {"name": "aria-labelledby", "type": "string", "description": "The id of the element containing a label for the slider"},
            {"name": "aria-valuetext", "type": "string", "description": "A string value that provides a user-friendly name for the current value of the slider"},
            {"name": "color", "type": "'primary' | 'secondary'", "description": "The color of the component"},
            {"name": "defaultValue", "type": "number | number[]", "description": "The default value"},
            {"name": "disabled", "type": "boolean", "description": "If true, the component will be disabled"},
            {"name": "disableSwap", "type": "boolean", "description": "If true, the active thumb doesn't swap when moving pointer over a thumb while dragging another thumb"},
            {"name": "getAriaLabel", "type": "(index: number) => string", "description": "Accepts a function which returns a string value that provides a user-friendly name for the thumb labels of the slider"},
            {"name": "getAriaValueText", "type": "(value: number, index: number) => string", "description": "Accepts a function which returns a string value that provides a user-friendly name for the current value of the slider"},
            {"name": "marks", "type": "boolean | Mark[]", "description": "Marks indicate predetermined values to which the user can move the slider"},
            {"name": "max", "type": "number", "description": "The maximum allowed value of the slider"},
            {"name": "min", "type": "number", "description": "The minimum allowed value of the slider"},
            {"name": "name", "type": "string", "description": "Name attribute of the hidden input element"},
            {"name": "onChange", "type": "(event: Event, value: number | number[], activeThumb: number) => void", "description": "Callback function that is fired when the slider's value changed"},
            {"name": "onChangeCommitted", "type": "(event: React.SyntheticEvent | Event, value: number | number[]) => void", "description": "Callback function that is fired when the mouseup is triggered"},
            {"name": "orientation", "type": "'horizontal' | 'vertical'", "description": "The orientation of the slider"},
            {"name": "scale", "type": "(value: number) => number", "description": "A transformation function, to change the scale of the slider"},
            {"name": "size", "type": "'small' | 'medium'", "description": "The size of the slider"},
            {"name": "step", "type": "number", "description": "The granularity with which the slider can step through values"},
            {"name": "track", "type": "'inverted' | 'normal' | false", "description": "The track presentation"},
            {"name": "value", "type": "number | number[]", "description": "The value of the slider"},
            {"name": "valueLabelDisplay", "type": "'auto' | 'off' | 'on'", "description": "Controls when the value label is displayed"},
            {"name": "valueLabelFormat", "type": "string | ((value: number, index: number) => React.ReactNode)", "description": "The format function the value label's value"}
        ],
        "events": ["onChange", "onChangeCommitted"],
        "default_values": {
            "color": "primary",
            "disabled": False,
            "disableSwap": False,
            "marks": False,
            "max": 100,
            "min": 0,
            "orientation": "horizontal",
            "size": "medium",
            "step": 1,
            "track": "normal",
            "valueLabelDisplay": "off"
        }
    },
    "Autocomplete": {
        "component_name": "Autocomplete",
        "import_path": "@mui/material/Autocomplete",
        "props": [
            {"name": "autoComplete", "type": "boolean", "description": "If true, the portion of the selected suggestion that has not been typed by the user will appear inline in the textbox"},
            {"name": "autoHighlight", "type": "boolean", "description": "If true, the first option is automatically highlighted"},
            {"name": "autoSelect", "type": "boolean", "description": "If true, the selected option becomes the value of the input when the Autocomplete loses focus"},
            {"name": "blurOnSelect", "type": "'mouse' | 'touch' | boolean", "description": "Control if the input should be blurred when an option is selected"},
            {"name": "clearIcon", "type": "React.ReactNode", "description": "The icon to display in place of the default clear icon"},
            {"name": "clearOnBlur", "type": "boolean", "description": "If true, the input's text is cleared on blur if no value is selected"},
            {"name": "clearOnEscape", "type": "boolean", "description": "If true, clear all values when the user presses escape and the popup is closed"},
            {"name": "clearText", "type": "string", "description": "Override the default text for the clear icon button"},
            {"name": "closeText", "type": "string", "description": "Override the default text for the close popup icon button"},
            {"name": "defaultValue", "type": "any", "description": "The default value"},
            {"name": "disableClearable", "type": "boolean", "description": "If true, the input can't be cleared"},
            {"name": "disableCloseOnSelect", "type": "boolean", "description": "If true, the popup won't close when a value is selected"},
            {"name": "disabled", "type": "boolean", "description": "If true, the component is disabled"},
            {"name": "disabledItemsFocusable", "type": "boolean", "description": "If true, will allow focus on disabled items"},
            {"name": "disableListWrap", "type": "boolean", "description": "If true, the list box in the popup will not wrap focus"},
            {"name": "disablePortal", "type": "boolean", "description": "If true, the Popper content will be under the DOM hierarchy of the parent component"},
            {"name": "filterOptions", "type": "(options: T[], state: FilterOptionsState<T>) => T[]", "description": "A function that determines the filtered options to be rendered on search"},
            {"name": "filterSelectedOptions", "type": "boolean", "description": "If true, hide the selected options from the list box"},
            {"name": "forcePopupIcon", "type": "'auto' | boolean", "description": "Force the visibility display of the popup icon"},
            {"name": "freeSolo", "type": "boolean", "description": "If true, the Autocomplete is free solo, meaning that the user input is not bound to provided options"},
            {"name": "fullWidth", "type": "boolean", "description": "If true, the input will take up the full width of its container"},
            {"name": "getLimitTagsText", "type": "(more: number) => React.ReactNode", "description": "The label to display when the tags are truncated"},
            {"name": "getOptionDisabled", "type": "(option: T) => boolean", "description": "Used to determine the disabled state for a given option"},
            {"name": "getOptionLabel", "type": "(option: T) => string", "description": "Used to determine the string value for a given option"},
            {"name": "groupBy", "type": "(option: T) => string", "description": "If provided, the options will be grouped under the returned string"},
            {"name": "handleHomeEndKeys", "type": "boolean", "description": "If true, the component handles the Home and End keys"},
            {"name": "id", "type": "string", "description": "This prop is used to help implement the accessibility logic"},
            {"name": "includeInputInList", "type": "boolean", "description": "If true, the highlight can move to the input"},
            {"name": "inputValue", "type": "string", "description": "The input value"},
            {"name": "isOptionEqualToValue", "type": "(option: T, value: T) => boolean", "description": "Used to determine if the option represents the given value"},
            {"name": "limitTags", "type": "number", "description": "The maximum number of tags that will be visible when not focused"},
            {"name": "loading", "type": "boolean", "description": "If true, the component is in a loading state"},
            {"name": "loadingText", "type": "React.ReactNode", "description": "Text to display when in a loading state"},
            {"name": "multiple", "type": "boolean", "description": "If true, value must be an array and the menu will support multiple selections"},
            {"name": "noOptionsText", "type": "React.ReactNode", "description": "Text to display when there are no options"},
            {"name": "onChange", "type": "(event: React.SyntheticEvent, value: T | T[], reason: AutocompleteChangeReason, details?: AutocompleteChangeDetails<T>) => void", "description": "Callback fired when the value changes"},
            {"name": "onClose", "type": "(event: React.SyntheticEvent, reason: AutocompleteCloseReason) => void", "description": "Callback fired when the popup requests to be closed"},
            {"name": "onHighlightChange", "type": "(event: React.SyntheticEvent, option: T, reason: AutocompleteHighlightChangeReason) => void", "description": "Callback fired when the highlight option changes"},
            {"name": "onInputChange", "type": "(event: React.SyntheticEvent, value: string, reason: AutocompleteInputChangeReason) => void", "description": "Callback fired when the input value changes"},
            {"name": "onOpen", "type": "(event: React.SyntheticEvent) => void", "description": "Callback fired when the popup requests to be opened"},
            {"name": "open", "type": "boolean", "description": "If true, the component is shown"},
            {"name": "openOnFocus", "type": "boolean", "description": "If true, the popup will open on input focus"},
            {"name": "openText", "type": "string", "description": "Override the default text for the open popup icon button"},
            {"name": "options", "type": "T[]", "description": "Array of options"},
            {"name": "PaperComponent", "type": "elementType", "description": "The component used to render the body of the popup"},
            {"name": "popupIcon", "type": "React.ReactNode", "description": "The icon to display in place of the default popup icon"},
            {"name": "readOnly", "type": "boolean", "description": "If true, the component becomes readonly"},
            {"name": "renderGroup", "type": "(params: AutocompleteRenderGroupParams) => React.ReactNode", "description": "Render the group"},
            {"name": "renderInput", "type": "(params: AutocompleteRenderInputParams) => React.ReactNode", "description": "Render the input"},
            {"name": "renderOption", "type": "(props: React.HTMLAttributes<HTMLLIElement>, option: T, state: AutocompleteRenderOptionState) => React.ReactNode", "description": "Render the option"},
            {"name": "renderTags", "type": "(value: T[], getTagProps: AutocompleteGetTagProps) => React.ReactNode", "description": "Render the selected value"},
            {"name": "selectOnFocus", "type": "boolean", "description": "If true, the input's text is selected on focus"},
            {"name": "size", "type": "'small' | 'medium'", "description": "The size of the component"},
            {"name": "slotProps", "type": "object", "description": "The props used for each slot inside"},
            {"name": "value", "type": "T | T[]", "description": "The value of the autocomplete"}
        ],
        "events": ["onChange", "onClose", "onHighlightChange", "onInputChange", "onOpen"],
        "default_values": {
            "autoComplete": False,
            "autoHighlight": False,
            "autoSelect": False,
            "blurOnSelect": False,
            "clearOnBlur": True,
            "clearOnEscape": False,
            "clearText": "Clear",
            "closeText": "Close",
            "disableClearable": False,
            "disableCloseOnSelect": False,
            "disabled": False,
            "disabledItemsFocusable": False,
            "disableListWrap": False,
            "disablePortal": False,
            "filterSelectedOptions": False,
            "forcePopupIcon": "auto",
            "freeSolo": False,
            "fullWidth": False,
            "handleHomeEndKeys": True,
            "includeInputInList": False,
            "limitTags": -1,
            "loading": False,
            "loadingText": "Loading…",
            "multiple": False,
            "noOptionsText": "No options",
            "openOnFocus": False,
            "openText": "Open",
            "readOnly": False,
            "selectOnFocus": True,
            "size": "medium"
        }
    },
    "Pagination": {
        "component_name": "Pagination",
        "import_path": "@mui/material/Pagination",
        "props": [
            {"name": "boundaryCount", "type": "number", "description": "Number of always visible pages at the beginning and end"},
            {"name": "color", "type": "'primary' | 'secondary' | 'standard'", "description": "The active color"},
            {"name": "count", "type": "number", "description": "The total number of pages"},
            {"name": "defaultPage", "type": "number", "description": "The page selected by default when the component is uncontrolled"},
            {"name": "disabled", "type": "boolean", "description": "If true, the component is disabled"},
            {"name": "getItemAriaLabel", "type": "(type: 'first' | 'last' | 'next' | 'previous' | 'page', page: number, selected: boolean) => string", "description": "Accepts a function which returns a string value that provides a user-friendly name for the current page"},
            {"name": "hideNextButton", "type": "boolean", "description": "If true, hide the next-page button"},
            {"name": "hidePrevButton", "type": "boolean", "description": "If true, hide the previous-page button"},
            {"name": "onChange", "type": "(event: React.ChangeEvent<unknown>, page: number) => void", "description": "Callback fired when the page is changed"},
            {"name": "page", "type": "number", "description": "The current page"},
            {"name": "renderItem", "type": "(item: PaginationItem) => React.ReactNode", "description": "Render the item"},
            {"name": "shape", "type": "'circular' | 'rounded'", "description": "The shape of the pagination items"},
            {"name": "showFirstButton", "type": "boolean", "description": "If true, show the first-page button"},
            {"name": "showLastButton", "type": "boolean", "description": "If true, show the last-page button"},
            {"name": "siblingCount", "type": "number", "description": "Number of always visible pages before and after the current page"},
            {"name": "size", "type": "'small' | 'medium' | 'large'", "description": "The size of the component"},
            {"name": "variant", "type": "'outlined' | 'text'", "description": "The variant to use"}
        ],
        "events": ["onChange"],
        "default_values": {
            "boundaryCount": 1,
            "color": "standard",
            "count": 1,
            "defaultPage": 1,
            "disabled": False,
            "hideNextButton": False,
            "hidePrevButton": False,
            "shape": "circular",
            "showFirstButton": False,
            "showLastButton": False,
            "siblingCount": 1,
            "size": "medium",
            "variant": "text"
        }
    }
}

def save_component_data():
    """Save individual component JSON files and create a unified index."""
    
    # Create output directory
    output_dir = "mui_migration/component_extraction"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual component files
    for component_name, component_data in MUI_COMPONENTS.items():
        filename = f"{component_name.lower()}-mui-v7.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(component_data, f, indent=2)
        
        print(f"✓ Saved {filename}")
    
    # Create unified components index
    mui_v7_components = []
    for component_name, component_data in MUI_COMPONENTS.items():
        mui_v7_components.append({
            "file": f"{component_name.lower()}-mui-v7.json",
            "component_name": component_name,
            "import_path": component_data["import_path"],
            "props_count": len(component_data["props"]),
            "events_count": len(component_data["events"]),
            "has_children": any(p["name"] == "children" for p in component_data["props"])
        })
    
    # Save unified index
    unified_index = {
        "description": "MUI v7 Components Index",
        "version": "7.x",
        "total_components": len(MUI_COMPONENTS),
        "components": mui_v7_components
    }
    
    index_path = os.path.join(output_dir, "mui_v7_components.json")
    with open(index_path, 'w') as f:
        json.dump(unified_index, f, indent=2)
    
    print(f"\n✓ Saved unified index: mui_v7_components.json")
    print(f"✓ Total components extracted: {len(MUI_COMPONENTS)}")

def main():
    """Main function to extract MUI component data."""
    print("Extracting MUI v7 component data...")
    save_component_data()
    print("\nExtraction complete!")

if __name__ == "__main__":
    main()
