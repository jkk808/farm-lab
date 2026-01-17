#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python light_sensor.py "$@"