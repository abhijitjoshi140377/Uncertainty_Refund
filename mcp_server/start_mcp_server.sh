#!/bin/bash

echo "========================================"
echo "MCP Server for Refund Estimation System"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if FastAPI backend is running
echo "Checking if FastAPI backend is running..."
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo ""
    echo "WARNING: FastAPI backend is not running!"
    echo "Please start the backend first:"
    echo "  cd backend"
    echo "  python main.py"
    echo ""
    exit 1
fi

echo "Backend is running!"
echo ""

# Start MCP server
echo "Starting MCP Server..."
echo ""
python refund_mcp_server.py

# Made with Bob
