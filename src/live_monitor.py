# import psutil
# import time

# def get_system_metrics():
#     cpu = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory().percent
#     disk = psutil.disk_usage('/').percent
#     processes = len(psutil.pids())
#     net_io = psutil.net_io_counters()
#     disk_io = psutil.disk_io_counters()

#     return {
#         "cpu": cpu,
#         "memory": memory,
#         "disk": disk,
#         "processes": processes,
#         "bytes_sent": net_io.bytes_sent,
#         "bytes_recv": net_io.bytes_recv,
#         "read_bytes": disk_io.read_bytes,
#         "write_bytes": disk_io.write_bytes
#     }




# import psutil
# import time
# import pandas as pd

# def get_live_metrics():
#     cpu = psutil.cpu_percent(interval=1)
#     mem = psutil.virtual_memory().percent
#     processes = len(psutil.pids())
#     disk_read = psutil.disk_io_counters().read_bytes
#     disk_write = psutil.disk_io_counters().write_bytes

#     data = {
#         "cpu": cpu,
#         "memory": mem,
#         "process_count": processes,
#         "disk_read": disk_read,
#         "disk_write": disk_write,
#         "timestamp": time.time()
#     }
#     return data

# def stream_metrics(duration=60):
#     logs = []
#     for _ in range(duration):
#         logs.append(get_live_metrics())
#     return pd.DataFrame(logs)



# src/live_monitor.py
"""
Real-time system metrics collector using psutil
"""

import psutil
import datetime

def get_live_metrics():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    process_count = len(psutil.pids())

    disk = psutil.disk_io_counters()
    net = psutil.net_io_counters()

    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "cpu": cpu_percent,
        "memory": mem,
        "process_count": process_count,
        "disk_read_bytes": disk.read_bytes,
        "disk_write_bytes": disk.write_bytes,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv
    }
