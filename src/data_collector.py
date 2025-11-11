"""
src/data_collector.py
Simulates or captures system call data and stores it in CSV format.
"""

import csv
import random
import time
from datetime import datetime
import os

def generate_system_call_logs(filename="data/sample_logs.csv", num_entries=150):
    """
    Generates dummy system call logs for simulation.
    Each record includes: PID, System Call, ExecTime(ms), Timestamp.
    """
    os.makedirs("data", exist_ok=True)
    system_calls = [
        "read", "write", "open", "close", "fork", "exec",
        "wait", "exit", "stat", "getpid", "kill", "sleep"
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PID", "SysCall", "ExecTime(ms)", "Timestamp"])
        for _ in range(num_entries):
            pid = random.randint(1000, 9999)
            call = random.choice(system_calls)
            exec_time = round(random.uniform(0.5, 20.0), 3)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([pid, call, exec_time, timestamp])
            time.sleep(0.002)
    print(f"[+] Generated {num_entries} system call entries → {filename}")

if __name__ == "__main__":
    generate_system_call_logs(num_entries=200)
