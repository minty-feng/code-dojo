#!/bin/bash
# Initial build script
# For first-time Sphinx documentation build

set -e  # Exit on error

echo "Frontend Tutorial - Initial Build Script"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python environment..."
python3 --version || { echo "❌ Python3 not installed"; exit 1; }

# Check if in correct directory
if [ ! -f "conf.py" ]; then
    echo "❌ Please run this script in the project root directory"
    exit 1
fi

# Create virtual environment (recommended)
VENV_DIR="${VENV_DIR:-venv}"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "📥 Upgrading pip..."
python3 -m pip install -q --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
python3 -m pip install -q -r requirements.txt

# Clean old build
echo "🧹 Cleaning old build..."
rm -rf _build/html

# Build documentation
echo "🔨 Building HTML documentation..."
python3 -m sphinx -b html . _build/html

# Verify build result
if [ ! -f "_build/html/index.html" ]; then
    echo "❌ Build failed: index.html not found"
    exit 1
fi

# Minify and obfuscate JavaScript files
echo "🔧 Minifying JavaScript files..."
JS_DIR="_build/html/_static"
if [ -d "$JS_DIR" ]; then
    # Check if terser is available
    if ! command -v terser >/dev/null 2>&1; then
        echo "❌ terser not installed, please install: npm install -g terser"
        exit 1
    fi
    
    while IFS= read -r -d '' js_file; do
        filename=$(basename "$js_file")
        # Only minify custom JS (e.g., copy-code.js), skip third-party libraries
        if [[ "$filename" == "copy-code.js" ]]; then
            if terser "$js_file" -c -m --comments false -o "${js_file}.tmp" 2>/dev/null; then
                mv "${js_file}.tmp" "$js_file"
                echo "    ✓ Minified: $filename"
            else
                echo "    ❌ Minification failed: $filename"
                exit 1
            fi
        fi
    done < <(find "$JS_DIR" -name "*.js" -type f ! -name "*.min.js" -print0)
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "📊 Build statistics:"
HTML_COUNT=$(find _build/html -name "*.html" | wc -l)
SIZE=$(du -sh _build/html | cut -f1)
echo "  - HTML files: $HTML_COUNT"
echo "  - Build directory size: $SIZE"
echo ""
echo "💡 Tip: After building, you can use the following scripts:"
echo "  - package-nginx.sh  # Create Nginx deployment package"
