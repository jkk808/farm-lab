#!/bin/bash
set -e

echo "=== FarmLab Setup ==="

# Update package lists and install system dependencies
echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-lgpio python3-libgpiod libgpiod-dev swig build-essential python3-dev

# Remove existing venv if present
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment with system site packages
echo "Creating virtual environment with system site packages..."
python3 -m venv venv --system-site-packages

# Activate and install Python dependencies
source venv/bin/activate
echo "Installing Python dependencies..."
pip install adafruit-blinka adafruit-circuitpython-bh1750

echo ""
echo "Adding alias to ~/.bashrc..."
if ! grep -q 'alias farmlab=' ~/.bashrc; then
    echo 'alias farmlab="~/farmlab/start.sh"' >> ~/.bashrc
fi

echo ""
echo "=== Setup complete ==="
echo "Run 'source ~/.bashrc' to activate the alias"
echo "Then run sensors with: farmlab"