# Farm Lab

Raspberry Pi agricultural sensor monitoring system.

## Supported Sensors

- BH1750 - Light (lux)
- ADS1115 + Capacitive probe - Soil moisture
- SCD40 - CO2, temperature, humidity

## Setup
```bash
# Clone the repo
git clone https://github.com/jkapali/farm-lab.git
cd farmlab

# Run setup
chmod +x setup.sh run.sh
./setup.sh
```

## Usage
```bash
# Start readings (default 5s interval)
./run.sh

# Custom interval
./run.sh -i 10
```

## Make Alias
```bash
echo 'alias farmlab="~/farmlab/start.sh"' >> ~/.bashrc
source ~/.bashrc
```

## Monitor
```bash
# Using screen (install first: sudo apt install screen)
screen -S sensors
farmlab
# Press Ctrl+A then D to detach

# Reconnect later with:
screen -r sensors
```

## Prerequisites

Enable I2C on your Pi:
```bash
sudo raspi-config
# Interface Options → I2C → Enable
```