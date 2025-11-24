




# dashboard/dashboard_app.py
"""
Streamlit dashboard for AI-Enhanced System Call Optimization
Includes:
- Model Output / static charts
- Real-Time Monitor (live metrics + AI inference)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import joblib

from model.model_utils import load_model, predict_next_syscall
from src.live_monitor import get_live_metrics


st.set_page_config(page_title="AI System Call Optimization", layout="wide")
st.title("🧠 AI-Enhanced System Call Optimization")

DATA_PATH = "data/processed_data.csv"
MODEL_PATH = "model/saved_model.pkl"

# Sidebar navigation
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Choose View", ["Model Output", "Real-Time Monitor", "About"])


def safe_load_model():
    try:
        if os.path.exists(MODEL_PATH):
            return load_model(MODEL_PATH)
        return None
    except:
        return None


# ------------------ ABOUT PAGE -------------------
if page == "About":
    st.markdown("""
    ### AI-Enhanced System Call Optimization Dashboard  
    **Features**:
    - System call performance visualization
    - Real-Time OS resource monitor
    - ML-based load prediction & scheduling recommendations

    **Developers:**
    - 🧑‍💻 Ayush Ranjan (Real-Time Monitoring + Dashboard Enhancements)
    - 🧠 Srayansh Singh Verma (Pipeline, ML Model & Integration)
    """)


# ------------------ MODEL OUTPUT PAGE -------------------
if page == "Model Output":
    if not os.path.exists(DATA_PATH):
        st.error("Data not found. Run `python src/main.py` to generate.")
        st.stop()

    df = pd.read_csv(DATA_PATH)

    st.subheader("📋 Sample Data")
    st.dataframe(df.head())

    st.subheader("System Call Frequency")
    freq = df["SysCall"].value_counts().reset_index()
    freq.columns = ["SysCall", "Count"]
    fig1 = px.bar(freq, x="SysCall", y="Count", title="SysCall Frequency")
    st.plotly_chart(fig1, width="stretch")

    st.subheader("Execution Time Distribution")
    fig2 = px.box(df, x="SysCall", y="ExecTime(ms)", title="Exec Time Distribution")
    st.plotly_chart(fig2, width="stretch")

    model = safe_load_model()
    if model:
        st.subheader("🔮 Predict Next SysCall")
        syscall_list = sorted(df["SysCall"].unique())
        current = st.selectbox("Current SysCall", syscall_list)
        time_ms = st.slider("Execution Time (ms)", 0, 1000, 200)

        if st.button("Predict"):
            pred = predict_next_syscall(model, syscall_list.index(current), time_ms / 1000)
            st.success(f"Next predicted system call: **{pred}**")


# ------------------ REAL TIME MONITOR PAGE -------------------
if page == "Real-Time Monitor":
    st.subheader("🔴 Real-Time OS Resource Monitoring")

    model = safe_load_model()

    start = st.button("Start Live")
    stop = st.button("Stop")

    cpu_box = st.empty()
    mem_box = st.empty()
    proc_box = st.empty()
    disk_box = st.empty()
    net_box = st.empty()
    load_box = st.empty()
    chart_area = st.empty()

    refresh = st.slider("Refresh Interval (sec)", 1, 5, 1)

    history = {"timestamp": [], "cpu": [], "memory": []}

    if start:
        st.session_state["run"] = True
    if stop:
        st.session_state["run"] = False

    if "run" not in st.session_state:
        st.session_state["run"] = False

    while st.session_state["run"]:
        metrics = get_live_metrics()

        history["timestamp"].append(metrics["timestamp"])
        history["cpu"].append(metrics["cpu"])
        history["memory"].append(metrics["memory"])

        cpu_box.metric("CPU Usage", f"{metrics['cpu']} %")
        mem_box.metric("Memory Usage", f"{metrics['memory']} %")
        proc_box.metric("Processes", metrics["process_count"])
        disk_box.write(f"Disk Read {metrics['disk_read_bytes']} B | Write {metrics['disk_write_bytes']} B")
        net_box.write(f"Net Sent {metrics['net_sent']} B | Recv {metrics['net_recv']} B")

        if model:
            if metrics["cpu"] < 30:
                load = "LOW"
                rec = "Round Robin / FCFS"
            elif metrics["cpu"] < 70:
                load = "MEDIUM"
                rec = "Priority Scheduling"
            else:
                load = "HIGH"
                rec = "Shortest Job First / Preemptive"
            load_box.info(f"CPU Load: **{load}** — Recommended: **{rec}**")

        df_hist = pd.DataFrame(history)
        fig = px.line(df_hist, x="timestamp", y=["cpu", "memory"], title="Live System Usage")
        chart_area.plotly_chart(fig, width="stretch")

        time.sleep(refresh)

