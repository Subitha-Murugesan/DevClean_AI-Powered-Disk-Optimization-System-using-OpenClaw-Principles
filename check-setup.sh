#!/bin/bash

# DevClean - OpenClaw Hackathon Quick Start
# Run this script to check if you're ready to go!

echo "🎉 DevClean - OpenClaw Hackathon Setup Check"
echo "=============================================="
echo ""

# Check Python
echo "📦 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Install from python.org"
    exit 1
fi

# Check Node.js
echo ""
echo "📦 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION"
else
    echo "❌ Node.js not found. Install from nodejs.org"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm $NPM_VERSION"
else
    echo "❌ npm not found. Install Node.js from nodejs.org"
    exit 1
fi

# Check if .env exists
echo ""
echo "🔑 Checking API Configuration..."
if [ -f "devclean/.env" ]; then
    echo "✅ .env file exists"
    
    # Check for OpenRouter API key
    if grep -q "OPENROUTER_API_KEY=sk-or-v1-" devclean/.env; then
        echo "✅ OpenRouter API key configured"
    else
        echo "⚠️  OpenRouter API key not set in .env"
        echo "   1. Get free $10 credits at openrouter.ai"
        echo "   2. Redeem promo code at openrouter.ai/redeem"
        echo "   3. Add OPENROUTER_API_KEY to devclean/.env"
    fi
else
    echo "⚠️  .env file not found"
    echo "   Run: cp devclean/.env.example devclean/.env"
    echo "   Then add your OPENROUTER_API_KEY"
fi

# Check backend dependencies
echo ""
echo "📦 Checking Backend Dependencies..."
cd devclean
if [ -f "requirements.txt" ]; then
    if pip3 show fastapi &> /dev/null; then
        echo "✅ Backend dependencies installed"
    else
        echo "⚠️  Backend dependencies not installed"
        echo "   Run: cd devclean && pip install -r requirements.txt"
    fi
fi
cd ..

# Check frontend dependencies
echo ""
echo "📦 Checking Frontend Dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  Frontend dependencies not installed"
    echo "   Run: cd frontend && npm install"
fi

echo ""
echo "=============================================="
echo "🚀 Ready to Start?"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd devclean && uvicorn backend:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend && npm run dev"
echo ""
echo "Then open: http://localhost:5173"
echo ""
echo "Need help? Check HACKATHON_README.md"
echo "=============================================="
