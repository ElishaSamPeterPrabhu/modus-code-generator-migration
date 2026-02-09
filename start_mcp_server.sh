#!/bin/bash

# Start the Shadcn to Modus Migration MCP Server (Local)

echo "Starting Shadcn to Modus Migration MCP Server..."
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null
then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Determine Python command
PYTHON_CMD="python"
if ! command -v python &> /dev/null
then
    PYTHON_CMD="python3"
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "Dependencies installed."
echo ""

# Run the MCP server
echo "Starting MCP server..."
echo "Server running in stdio mode. Press Ctrl+C to stop."
echo ""
$PYTHON_CMD shadcn_mcp_server_local.py
