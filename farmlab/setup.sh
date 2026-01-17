#!/bin/bash
set -e

echo "=== FarmLab Setup ==="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Setup complete ==="
echo "Run sensors with: ./run.sh"