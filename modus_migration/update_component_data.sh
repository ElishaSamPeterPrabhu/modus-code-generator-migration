#!/bin/bash
# update_component_data.sh
# Run this script each sprint after a Modus release to refresh all component data.
# Usage: ./modus_migration/update_component_data.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================"
echo "  Modus Component Data Update"
echo "============================================"
echo "Project: $PROJECT_DIR"
echo ""

# Step 1: The extractor now handles git pull internally (clone_repo was fixed).
# Just run the pipeline scripts directly.

echo "[1/3] Running component extractor (pulls latest repos + regenerates JSON)..."
cd "$PROJECT_DIR"
python3 modus_migration/component_extractor.py

echo ""
echo "[2/3] Splitting bulk JSONs into per-component files..."
python3 split_components.py

echo ""
echo "[3/3] Reorganizing files, fixing mappings, generating unified index..."
python3 reorganize_components.py

echo ""
echo "============================================"
echo "  Done! Component data is up to date."
echo "  Files updated in: modus_migration/component_analysis/"
echo "============================================"
