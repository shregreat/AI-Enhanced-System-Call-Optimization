"""
tests/test_data_preprocessing.py
Basic test for preprocessing module.
Run: python -m pytest tests/test_data_preprocessing.py  (if pytest installed)
"""

import os
import sys
# ensure src package path
sys.path.insert(0, os.path.abspath("src"))
from preprocessor import preprocess_data

def test_preprocessing_runs():
    # Ensure sample file exists (create quick if not)
    sample = "data/sample_logs.csv"
    if not os.path.exists(sample):
        # generate small sample
        from data_collector import generate_system_call_logs
        generate_system_call_logs(filename=sample, num_entries=50)
    df = preprocess_data(input_file=sample, output_file="data/processed_data.csv")
    assert not df.empty
    assert "SysCall_Code" in df.columns
    print("[TEST] preprocess_data passed")
