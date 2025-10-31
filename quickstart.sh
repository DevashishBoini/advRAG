#!/bin/bash

# Quick Start Script for AdvRAG Backend
# This script helps you get started quickly

echo "======================================"
echo "AdvRAG Backend - Quick Start"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your credentials:"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_KEY"
    echo "   - SUPABASE_SERVICE_ROLE_KEY"
    echo "   - DATABASE_URL"
    echo "   - OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

if ! python3 -c 'import sys; assert sys.version_info >= (3, 11)' 2>/dev/null; then
    echo "   ✗ Python 3.11+ required"
    exit 1
fi
echo "   ✓ Python version OK"
echo ""

echo "2. Installing dependencies..."
pip install -e . --quiet
echo "   ✓ Dependencies installed"
echo ""

echo "3. Initializing database..."
python backend/scripts/init_db.py
if [ $? -eq 0 ]; then
    echo "   ✓ Database initialized"
else
    echo "   ✗ Database initialization failed"
    echo "   Please check your .env configuration"
    exit 1
fi
echo ""

echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start the server:"
echo "  cd backend"
echo "  python -m app.main"
echo ""
echo "Or use uvicorn directly:"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "API Documentation will be available at:"
echo "  http://localhost:8000/docs"
echo ""
