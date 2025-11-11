"""
model/model_utils.py
Helper functions used by training notebooks / scripts.
"""

import joblib
import os
import numpy as np
import pandas as pd

def save_model(model, path="model/saved_model.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    return path

def load_model(path="model/saved_model.pkl"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}")
    return joblib.load(path)

def predict_next_syscall(model, syscall_code, exec_time_norm):
    """Return predicted syscall code (int)."""
    X = np.array([[syscall_code, exec_time_norm]])
    pred = model.predict(X)
    return int(pred[0])
