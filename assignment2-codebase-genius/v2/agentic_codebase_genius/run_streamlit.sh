#!/bin/bash
# Streamlit App Launcher for Agentic Codebase Genius

echo "🤖 Agentic Codebase Genius - Streamlit UI"
echo "=========================================="
echo ""
echo "Starting Streamlit app..."
echo "App will be available at: http://localhost:8501"
echo ""
echo "Available modes:"
echo "• Jac Cloud (Recommended) - Modern agentic approach"
echo "• Flask API - Traditional web service"
echo "• Direct Python - Local execution"
echo ""
echo "Make sure you have:"
echo "1. Activated the virtual environment"
echo "2. Installed all dependencies (pip install -r requirements.txt)"
echo "3. Installed system Graphviz (sudo apt install graphviz)"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Run: source ../../../venv/bin/activate"
fi

# Start Streamlit
streamlit run streamlit_app/app.py --server.headless true --server.port 8501