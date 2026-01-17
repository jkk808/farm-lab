#!/usr/bin/env python3
"""
BH1750 Light Sensor Reader
Reads ambient light levels in lux
"""

import time
import board
import busio
import adafruit_bh1750
from datetime import datetime

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bh1750.BH1750(i2c)

def read_light():
    """Returns light reading in lux"""
    return {
        "timestamp": datetime.now().isoformat(),
        "light_lux": round(sensor.lux, 2)
    }

def main(interval=5):
    print("=" * 40)
    print("BH1750 Light Sensor Monitor")
    print(f"Reading every {interval} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    print()
    
    try:
        while True:
            reading = read_light()
            lux = reading["light_lux"]
            
            # Simple light level description
            if lux < 10:
                level = "Dark"
            elif lux < 50:
                level = "Dim"
            elif lux < 200:
                level = "Indoor"
            elif lux < 1000:
                level = "Bright indoor"
            elif lux < 10000:
                level = "Overcast"
            else:
                level = "Direct sunlight"
            
            print(f"{reading['timestamp']} | {lux:>8.2f} lux | {level}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read BH1750 light sensor")
    parser.add_argument("-i", "--interval", type=int, default=5,
                        help="Seconds between readings (default: 5)")
    args = parser.parse_args()
    main(interval=args.interval)