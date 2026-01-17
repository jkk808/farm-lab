#!/usr/bin/env python3
"""
FarmLab Sensor Reader
"""

import time
import board
import busio
import json
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
available_sensors = []

try:
    import adafruit_bh1750
    light_sensor = adafruit_bh1750.BH1750(i2c)
    available_sensors.append("light")
    print("✓ BH1750 light sensor found")
except Exception as e:
    light_sensor = None
    print(f"✗ BH1750 not found: {e}")

try:
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    ads = ADS.ADS1115(i2c)
    soil_channel = AnalogIn(ads, ADS.P0)
    available_sensors.append("soil")
    print("✓ ADS1115 (soil moisture) found")
except Exception as e:
    soil_channel = None
    print(f"✗ ADS1115 not found: {e}")

try:
    import adafruit_scd4x
    scd4x = adafruit_scd4x.SCD4X(i2c)
    scd4x.start_periodic_measurement()
    available_sensors.append("co2")
    print("✓ SCD40 CO2 sensor found")
except Exception as e:
    scd4x = None
    print(f"✗ SCD40 not found: {e}")


def read_light():
    if light_sensor:
        return {"light_lux": round(light_sensor.lux, 2)}
    return {}


def read_soil():
    if soil_channel:
        raw = soil_channel.value
        dry_value = 26000
        wet_value = 13000
        moisture_pct = max(0, min(100, (dry_value - raw) / (dry_value - wet_value) * 100))
        return {
            "soil_moisture_pct": round(moisture_pct, 1),
            "soil_raw": raw
        }
    return {}


def read_co2():
    if scd4x and scd4x.data_ready:
        return {
            "co2_ppm": scd4x.CO2,
            "temperature_c": round(scd4x.temperature, 1),
            "humidity_pct": round(scd4x.relative_humidity, 1)
        }
    return {}


def collect_all():
    reading = {
        "timestamp": datetime.now().isoformat(),
        "sensors_active": available_sensors
    }
    reading.update(read_light())
    reading.update(read_soil())
    reading.update(read_co2())
    return reading


def main(interval=5):
    print(f"\nFarmLab Sensor Monitor")
    print(f"Active sensors: {', '.join(available_sensors) or 'None'}")
    print(f"Interval: {interval}s | Ctrl+C to stop\n")
    
    if scd4x:
        print("Waiting for CO2 sensor...")
        time.sleep(5)
    
    try:
        while True:
            print(json.dumps(collect_all(), indent=2))
            print("-" * 40)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", type=int, default=5)
    args = parser.parse_args()
    main(args.interval)