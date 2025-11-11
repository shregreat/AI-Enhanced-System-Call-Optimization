"""
utils/logger.py
Simple logging helper.
"""

import datetime
import os

def log(message, logfile="data/logs.txt"):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[LOG] {message}")
