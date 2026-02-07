#!/bin/bash
# publish_package.sh - Build and publish coeai package

# Exit on error
set -e

echo "🚀 Starting build process for coeai v4.0.0..."

# Change to project directory
cd "$(dirname "$0")"

# 1. Install/Upgrade build tools
echo "📦 Installing build dependencies (build, twine)..."
python3 -m pip install --upgrade build twine

# 2. Clean old builds
echo "🧹 Cleaning old build artifacts..."
rm -rf dist/ build/ *.egg-info/

# 3. Build package
echo "🔨 Building package (sdist and wheel)..."
python3 -m build

# 4. Check distribution
echo "🔍 Checking distribution artifacts..."
python3 -m twine check dist/*

echo ""
echo "✅ Build successful!"
echo "------------------------------------------------"
echo "Artifacts created in dist/:"
ls -lh dist/
echo "------------------------------------------------"
echo ""
echo "READY TO PUBLISH?"
echo "To upload to PyPI, run the following command and enter your API token:"
echo ""
echo "    python3 -m twine upload dist/*"
echo ""
