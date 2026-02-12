# FarmLab - Raspberry Pi 5 Sensor Monitor

A simple agricultural monitoring system for Raspberry Pi 5 with BH1750 light sensor.

## Hardware Requirements

- Raspberry Pi 5
- BH1750 Stemma QT Light Sensor

## Wiring

Connect the BH1750 to the Pi 5 GPIO header:

| BH1750 Pin | Wire Color (Stemma QT) | Pi 5 Pin | GPIO |
|------------|------------------------|----------|------|
| VIN | Red | Pin 1 | 3.3V |
| GND | Black | Pin 6 | GND |
| SDA | Blue | Pin 3 | GPIO 2 |
| SCL | Yellow | Pin 5 | GPIO 3 |

## Installation

### 1. Enable I2C

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
# Reboot when prompted
```

### 2. Run Setup

```bash
git clone https://github.com/jkapali/farm-lab.git
cd ~/farmlab
chmod +x setup.sh start.sh
./setup.sh
```

### 3. Verify Sensor Connection

```bash
i2cdetect -y 1
```

You should see `23` in the output grid (BH1750 default address).

## Usage

sudo apt update
sudo apt install python3-lgpio python3-libgpiod libgpiod-dev

source venv/bin/activate
pip install lgpio

sudo apt update
sudo apt install swig build-essential python3-dev

rm -rf venv
python3.11 -m venv venv --system-site-packages
source venv/bin/activate
pip install adafruit-blinka adafruit-circuitpython-bh1750

### Start Sensor Readings

```bash
# Default 5-second interval
./start.sh

# Custom interval (e.g., 2 seconds)
./start.sh -i 2
```

### Run via SSH

```bash
ssh user@your-pi-ip
cd ~/farmlab
./start.sh
```

### Run in Background

```bash
# Using screen
screen -S farmlab
./start.sh
# Detach: Ctrl+A then D
# Reattach: screen -r farmlab

# Using nohup
nohup ./start.sh > readings.log 2>&1 &
tail -f readings.log
```

### Add Alias for Quick Access

```bash
echo 'alias farmlab="~/farmlab/start.sh"' >> ~/.bashrc
source ~/.bashrc

# Now just run:
farmlab
```

## Output Example

```
========================================
BH1750 Light Sensor Monitor
Reading every 5 seconds
Press Ctrl+C to stop
========================================

2025-01-17T15:42:03.123456 |   347.50 lux | Bright indoor
2025-01-17T15:42:08.125678 |   352.25 lux | Bright indoor
```

## Light Level Reference

| Lux Range | Description |
|-----------|-------------|
| < 10 | Dark |
| 10 - 50 | Dim |
| 50 - 200 | Indoor |
| 200 - 1000 | Bright indoor |
| 1000 - 10000 | Overcast / shade |
| > 10000 | Direct sunlight |

## Troubleshooting

### ModuleNotFoundError: lgpio

Run setup again or manually install:

```bash
sudo apt install python3-lgpio python3-dev swig liblgpio-dev -y
source venv/bin/activate
pip install lgpio
```

### Sensor Not Detected (i2cdetect shows nothing)

1. Check wiring connections
2. Ensure I2C is enabled: `sudo raspi-config`
3. Check for loose connections on Stemma QT connector

### Permission Denied on I2C

```bash
sudo usermod -aG i2c $USER
# Log out and back in
```
