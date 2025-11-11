"""
dashboard/dashboard_app.py
Streamlit dashboard for visualization and simple model inference demo.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from model.model_utils import load_model, predict_next_syscall

st.set_page_config(page_title="AI-Enhanced System Call Optimization", layout="wide")
st.title("🧠 AI-Enhanced System Call Optimization")

DATA_PATH = "data/processed_data.csv"
MODEL_PATH = "model/saved_model.pkl"

if not os.path.exists(DATA_PATH):
    st.error("Data not found. Run 'python src/main.py' to generate and preprocess data.")
    st.stop()

df = pd.read_csv(DATA_PATH)
st.sidebar.markdown("## Controls")
show_sample = st.sidebar.checkbox("Show sample data", True)
if show_sample:
    st.subheader("Sample System Call Data")
    st.dataframe(df.head(15))

st.subheader("System Call Frequency")
freq = df["SysCall"].value_counts().reset_index()
freq.columns = ["SysCall", "Frequency"]
fig = px.bar(freq, x="SysCall", y="Frequency", title="System Call Frequency")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Execution Time Distribution")
fig2 = px.box(df, x="SysCall", y="ExecTime(ms)", title="Exec Time Distribution per SysCall")
st.plotly_chart(fig2, use_container_width=True)

# Model inference demo
st.subheader("Model Inference Demo")
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    syscall_map = dict(enumerate(df["SysCall"].astype('category').cat.categories))
    inv_map = {v:k for k,v in syscall_map.items()}
    selected_syscall = st.selectbox("Current System Call", list(syscall_map.values()))
    exec_time = st.slider("Execution time (ms)", float(df["ExecTime(ms)"].min()), float(df["ExecTime(ms)"].max()), float(df["ExecTime(ms)"].median()))
    # normalize
    min_t, max_t = df["ExecTime(ms)"].min(), df["ExecTime(ms)"].max()
    exec_norm = 0.0 if max_t==min_t else (exec_time - min_t)/(max_t - min_t)
    if st.button("Predict next syscall"):
        code = inv_map[selected_syscall]
        pred_code = predict_next_syscall(model, code, exec_norm)
        pred_name = syscall_map.get(pred_code, "Unknown")
        st.success(f"Predicted next syscall: **{pred_name}** (code {pred_code})")
else:
    st.warning("Model not found. Run training first (pipeline will train).")
