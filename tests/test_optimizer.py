"""
tests/test_optimizer.py
Simple check that training runs and produces a model file.
"""

import os
import sys
sys.path.insert(0, os.path.abspath("src"))
from optimizer import train_model

def test_train_model_creates_file():
    # Ensure processed data exists
    if not os.path.exists("data/processed_data.csv"):
        from data_collector import generate_system_call_logs
        from preprocessor import preprocess_data
        generate_system_call_logs(num_entries=100)
        preprocess_data()
    res = train_model()
    assert os.path.exists(res["model_path"])
    assert res["accuracy"] >= 0.0
    print(f"[TEST] train_model produced {res['model_path']} with acc {res['accuracy']}")
