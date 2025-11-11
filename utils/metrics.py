"""
utils/metrics.py
Calculate simple performance metrics from processed_data.csv
"""

import pandas as pd
import os

def calculate_performance_metrics(data_file="data/processed_data.csv", out_file="data/performance_metrics.csv"):
    if not os.path.exists(data_file):
        raise FileNotFoundError("Processed data not found.")
    df = pd.read_csv(data_file)
    avg = df["ExecTime(ms)"].mean()
    mn = df["ExecTime(ms)"].min()
    mx = df["ExecTime(ms)"].max()
    rows = [
        {"metric":"avg_exec_ms", "value":avg},
        {"metric":"min_exec_ms", "value":mn},
        {"metric":"max_exec_ms", "value":mx},
        {"metric":"rows", "value":len(df)}
    ]
    out_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    out_df.to_csv(out_file, index=False)
    print(f"[+] Metrics saved to {out_file}")
    return out_df
