"""
model/train_model.py
Standalone script to train the model (mirrors src/optimizer.py but provides extra logging).
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

DATA_FILE = "data/processed_data.csv"
MODEL_FILE = "model/saved_model.pkl"

def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} not found. Run pipeline to generate data.")
    df = pd.read_csv(DATA_FILE)
    X = df[["SysCall_Code", "ExecTime_Normalized"]]
    y = df["SysCall_Code"].shift(-1).fillna(df["SysCall_Code"].mode()[0]).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Classification Report:")
    print(classification_report(y_test, preds))
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    print(f"Saved model to {MODEL_FILE}")

if __name__ == "__main__":
    main()
