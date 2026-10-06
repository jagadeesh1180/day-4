import os
import json
import requests
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="FactoryPulse Edge AI", page_icon="⚙️", layout="wide")

st.title("⚙️ FactoryPulse Edge AI")
st.caption("Privacy-first machine intelligence for MSMEs")

def make_data(n=240, seed=7):
    rng = np.random.default_rng(seed)
    t = pd.date_range("2026-01-01", periods=n, freq="h")
    temp = 61 + rng.normal(0, 2.0, n)
    vibration = 2.1 + rng.normal(0, 0.18, n)
    power = 7.2 + rng.normal(0, 0.35, n)
    load = 70 + rng.normal(0, 6, n)

    # Synthetic fault windows for a realistic demo.
    for start, end in [(70, 78), (155, 163), (210, 216)]:
        temp[start:end] += rng.normal(10, 2, end-start)
        vibration[start:end] += rng.normal(1.5, .25, end-start)
        power[start:end] += rng.normal(2.4, .4, end-start)
        load[start:end] -= rng.normal(12, 3, end-start)

    return pd.DataFrame({
        "timestamp": t,
        "temperature_c": temp.round(2),
        "vibration_mm_s": vibration.round(2),
        "power_kw": power.round(2),
        "load_pct": load.round(2)
    })

def detect_anomalies(df):
    features = ["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]
    model = IsolationForest(
        n_estimators=150,
        contamination=0.08,
        random_state=42
    )
    df = df.copy()
    df["anomaly_score"] = -model.decision_function(df[features])
    df["anomaly"] = model.predict(df[features]) == -1

    # A simple interpretable maintenance risk score.
    z = (df[features] - df[features].mean()) / df[features].std()
    df["risk_score"] = (
        0.30 * z["temperature_c"].abs()
        + 0.35 * z["vibration_mm_s"].abs()
        + 0.20 * z["power_kw"].abs()
        + 0.15 * z["load_pct"].abs()
    ).clip(0, 5) / 5 * 100
    return df

def ai_explanation(row):
    base_url = os.getenv("AI_BASE_URL", "").strip()
    api_key = os.getenv("AI_API_KEY", "").strip()
    model = os.getenv("AI_MODEL", "").strip()

    prompt = f"""You are a factory maintenance assistant.
Analyze this machine telemetry event and give:
1. likely cause,
2. immediate action,
3. maintenance priority.

Telemetry:
temperature={row.temperature_c:.1f} C
vibration={row.vibration_mm_s:.2f} mm/s
power={row.power_kw:.2f} kW
load={row.load_pct:.1f}%
risk={row.risk_score:.0f}/100
"""

    if not (base_url and model):
        if row.risk_score >= 75:
            return "High priority: inspect bearings, alignment and cooling system before continued heavy operation."
        if row.risk_score >= 50:
            return "Medium priority: inspect vibration trend and power draw during the next maintenance window."
        return "Normal: continue monitoring and compare against the machine baseline."

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        r = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a concise industrial maintenance assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            },
            timeout=20
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"AI endpoint unavailable; deterministic recommendation used. ({type(exc).__name__})"

uploaded = st.sidebar.file_uploader("Upload telemetry CSV", type=["csv"])
df = pd.read_csv(uploaded) if uploaded else make_data()

required = {"timestamp", "temperature_c", "vibration_mm_s", "power_kw", "load_pct"}
if not required.issubset(df.columns):
    st.error("CSV must contain: timestamp, temperature_c, vibration_mm_s, power_kw, load_pct")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = detect_anomalies(df)

latest = df.iloc[-1]
high_risk = int((df["risk_score"] >= 75).sum())
energy = df["power_kw"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Machine status", "⚠️ ATTENTION" if latest.anomaly else "✅ NORMAL")
c2.metric("Current risk", f"{latest.risk_score:.0f}/100")
c3.metric("Mean power", f"{energy:.2f} kW")
c4.metric("High-risk events", high_risk)

st.subheader("Machine telemetry")
chart = df.set_index("timestamp")[["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]]
st.line_chart(chart)

st.subheader("Detected anomalies")
anomalies = df[df.anomaly].copy()
st.dataframe(
    anomalies[["timestamp", "temperature_c", "vibration_mm_s", "power_kw", "load_pct", "risk_score"]]
    .sort_values("risk_score", ascending=False)
    .head(12),
    use_container_width=True,
    hide_index=True
)

st.subheader("AI maintenance explanation")
selected_index = st.selectbox(
    "Select an event",
    anomalies.index.tolist() if len(anomalies) else [df.index[-1]],
    format_func=lambda i: str(df.loc[i, "timestamp"])
)
selected = df.loc[selected_index]
st.info(ai_explanation(selected))

with st.expander("Why this project is edge-first"):
    st.write(
        "Telemetry analysis is performed locally. The AI explanation layer uses an "
        "OpenAI-compatible endpoint and can be connected to a local CPU inference runtime. "
        "This keeps sensitive factory data inside the deployment boundary when the local "
        "runtime is used."
    )
