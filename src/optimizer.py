"""
src/optimizer.py
Train a simple ML model to predict the next system call (as a demonstration).
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


def train_model(data_file="data/processed_data.csv", model_file="model/saved_model.pkl"):
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file '{data_file}' not found. Run preprocessor.py first.")

    os.makedirs("model", exist_ok=True)
    df = pd.read_csv(data_file)

    # Features: current syscall code and normalized exec time
    X = df[["SysCall_Code", "ExecTime_Normalized"]]
    # Label: next syscall code (shifted)
    y = df["SysCall_Code"].shift(-1).fillna(df["SysCall_Code"].mode()[0]).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
#     preds = model.predict(X_test)
#     acc = accuracy_score(y_test, preds)

#     joblib.dump(model, model_file)
#     print(f"[+] Model trained with accuracy: {acc * 100:.2f}%")
#     print(f"[+] Model saved → {model_file}")



    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # === New Evaluation: Confusion Matrix ===
    cm = confusion_matrix(y_test, preds)
    print("\nCONFUSION MATRIX:\n", cm)

    # Plot and save confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix - System Call Prediction")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    os.makedirs("reports", exist_ok=True)
    cm_path = "reports/confusion_matrix.png"
    plt.savefig(cm_path)
    plt.close()

    # === New evaluation: classification metrics ===
    print("\nCLASSIFICATION REPORT:\n")
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(model, model_file)
    print(f"[+] Model trained with accuracy: {acc * 100:.2f}%")
    print(f"[+] Model saved → {model_file}")
    print(f"[+] Confusion Matrix saved → {cm_path}")
    return {"accuracy": acc, "model_path": model_file}
if __name__ == "__main__":
    train_model()
