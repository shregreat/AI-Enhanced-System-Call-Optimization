"""
src/main.py
Run the full pipeline (generate data -> preprocess -> train model).
"""

import subprocess
import sys
import os
from data_collector import generate_system_call_logs
from preprocessor import preprocess_data
from optimizer import train_model

def run_pipeline():
    print("\n🚀 Starting pipeline: generate -> preprocess -> train\n")
    # 1. Generate sample logs
    generate_system_call_logs(num_entries=300)

    # 2. Preprocess
    df = preprocess_data()

    # 3. Train model
    result = train_model()
    print(f"\n✅ Pipeline finished. Model accuracy: {result['accuracy'] * 100:.2f}%")

    # 4. Offer to launch dashboard
    answer = input("Launch Streamlit dashboard now? (y/n): ").strip().lower()
    if answer == 'y':
        # Ensure streamlit installed, then run
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard/dashboard_app.py"])
        except Exception as e:
            print("Failed to launch dashboard:", e)

if __name__ == "__main__":
    run_pipeline()
