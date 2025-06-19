#!/bin/bash
# Development environment setup script for Anki Cards Etymology Enhancer

echo "🚀 Setting up Anki Cards Etymology Enhancer development environment..."
echo ""

# Check Python version
echo "📍 Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "   Found: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo ""
    echo "   ✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run initial checks
echo ""
echo "🔍 Running initial checks..."
echo ""

# Format check
echo "▶ Checking code formatting..."
black . --check --diff 2>/dev/null || echo "   ⚠️  Some files need formatting (run 'make format')"

# Lint check
echo ""
echo "▶ Checking code quality..."
flake8 . --count --statistics 2>/dev/null || echo "   ⚠️  Some linting issues found (run 'make lint' for details)"

# Type check
echo ""
echo "▶ Checking type hints..."
mypy . 2>/dev/null || echo "   ⚠️  Some type issues found (run 'make mypy' for details)"

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the main script: make run"
echo "   3. Run tests: make test"
echo "   4. See all commands: make help"
echo ""
echo "Happy coding! 🎉"