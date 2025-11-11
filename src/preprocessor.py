"""
src/preprocessor.py
Cleans and prepares system call data for machine learning analysis.
"""

import pandas as pd
import os

def preprocess_data(input_file="data/sample_logs.csv", output_file="data/processed_data.csv"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found. Run data_collector.py first.")

    df = pd.read_csv(input_file)
    # Basic cleaning
    df.dropna(inplace=True)
    df["ExecTime(ms)"] = df["ExecTime(ms)"].astype(float)
    # Add categorical code for SysCall
    df["SysCall_Code"] = df["SysCall"].astype('category').cat.codes
    # Normalization
    if df["ExecTime(ms)"].max() != df["ExecTime(ms)"].min():
        df["ExecTime_Normalized"] = (
            df["ExecTime(ms)"] - df["ExecTime(ms)"].min()
        ) / (df["ExecTime(ms)"].max() - df["ExecTime(ms)"].min())
    else:
        df["ExecTime_Normalized"] = 0.0
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"[+] Preprocessed data saved to {output_file}")
    return df

if __name__ == "__main__":
    preprocess_data()
