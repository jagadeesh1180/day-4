import os
import time
import requests
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="FactoryPulse Edge", page_icon="⚙️", layout="wide")

REQUIRED = {"timestamp", "temperature_c", "vibration_mm_s", "power_kw", "load_pct"}
NUMERIC_COLUMNS = ["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]
MAX_UPLOAD_ROWS = 100_000

@st.cache_data
def make_demo_data(n=480, seed=42):
    rng = np.random.default_rng(seed)
    t = pd.date_range("2026-09-15", periods=n, freq="h")
    machines = ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06"]
    frames = []
    for idx, machine in enumerate(machines):
        temp = 58 + idx * 0.7 + rng.normal(0, 1.7, n)
        vibration = 1.8 + idx * 0.08 + rng.normal(0, 0.14, n)
        power = 5.8 + idx * 0.45 + rng.normal(0, 0.28, n)
        load = 68 + rng.normal(0, 7, n)
        if idx == 2:
            for a, b in [(115, 128), (330, 341)]:
                temp[a:b] += rng.normal(12, 1.8, b-a)
                vibration[a:b] += rng.normal(1.8, .22, b-a)
        elif idx == 3:
            for a, b in [(205, 219)]:
                power[a:b] += rng.normal(3.8, .45, b-a)
                temp[a:b] += rng.normal(7, 1.5, b-a)
        elif idx == 4:
            for a, b in [(390, 405)]:
                load[a:b] += rng.normal(22, 3, b-a)
                power[a:b] += rng.normal(2.5, .35, b-a)
        frames.append(pd.DataFrame({
            "timestamp": t, "machine_id": machine,
            "temperature_c": temp.round(2), "vibration_mm_s": vibration.round(2),
            "power_kw": power.round(2), "load_pct": load.clip(0, 100).round(2)
        }))
    return pd.concat(frames, ignore_index=True)

def validate(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Telemetry input must be a CSV table.")
    if len(df) > MAX_UPLOAD_ROWS:
        raise ValueError(f"Telemetry file is too large. Maximum supported rows: {MAX_UPLOAD_ROWS:,}.")
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError("timestamp contains invalid dates.")
    if "machine_id" not in df.columns:
        df["machine_id"] = "M-01"
    df["machine_id"] = df["machine_id"].fillna("M-01").astype(str).str.strip()
    if (df["machine_id"] == "").any():
        raise ValueError("machine_id contains empty values.")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        if df[column].isna().any():
            raise ValueError(f"{column} contains non-numeric or missing values.")
        if not np.isfinite(df[column].to_numpy()).all():
            raise ValueError(f"{column} contains non-finite values.")
    if (df["vibration_mm_s"] < 0).any() or (df["power_kw"] < 0).any():
        raise ValueError("vibration_mm_s and power_kw cannot be negative.")
    if ((df["load_pct"] < 0) | (df["load_pct"] > 100)).any():
        raise ValueError("load_pct must be between 0 and 100.")
    return df.sort_values(["machine_id", "timestamp"]).reset_index(drop=True)
def score_machine(group):
    group = group.copy()
    features = ["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]
    x = group[features].astype(float)
    model = IsolationForest(n_estimators=180, contamination=0.06, random_state=42)
    group["anomaly"] = model.fit_predict(x) == -1
    group["anomaly_score"] = (-model.decision_function(x)).clip(-1, 1)
    baseline = x.rolling(24, min_periods=6).mean().bfill()
    deviation = ((x - baseline) / baseline.replace(0, np.nan)).abs().fillna(0)
    group["risk_score"] = (
        0.30 * (deviation["temperature_c"] * 100).clip(0, 100)
        + 0.35 * (deviation["vibration_mm_s"] * 100).clip(0, 100)
        + 0.20 * (deviation["power_kw"] * 100).clip(0, 100)
        + 0.15 * (deviation["load_pct"] * 100).clip(0, 100)
    ).clip(0, 100)
    return group

def analyze(df):
    return df.groupby("machine_id", group_keys=False, sort=False).apply(score_machine, include_groups=False).reset_index(drop=True)

def machine_state(row):
    if row.risk_score >= 75 or row.anomaly:
        return "🔴 CRITICAL"
    if row.risk_score >= 45:
        return "🟡 WATCH"
    return "🟢 HEALTHY"

def probable_cause(row, history):
    recent = history[history.machine_id == row.machine_id].tail(24)
    d = {
        "temperature_c": (row.temperature_c - recent.temperature_c.mean()) / max(recent.temperature_c.std(), .01),
        "vibration_mm_s": (row.vibration_mm_s - recent.vibration_mm_s.mean()) / max(recent.vibration_mm_s.std(), .01),
        "power_kw": (row.power_kw - recent.power_kw.mean()) / max(recent.power_kw.std(), .01),
        "load_pct": (row.load_pct - recent.load_pct.mean()) / max(recent.load_pct.std(), .01),
    }
    if d["vibration_mm_s"] > 1.5 and d["temperature_c"] > 1:
        return "Bearing / alignment degradation"
    if d["power_kw"] > 1.8 and d["temperature_c"] > 1:
        return "Electrical inefficiency or motor stress"
    if d["load_pct"] > 1.8 and d["power_kw"] > 1:
        return "Overload / process bottleneck"
    return "Unclassified multi-signal anomaly"

def energy_insights(df):
    """Estimate excess energy against each machine's own robust local baseline."""
    rows = []
    for machine_id, group in df.groupby("machine_id"):
        group = group.sort_values("timestamp")
        baseline = group["power_kw"].rolling(24, min_periods=6).median()
        excess_kw = (group["power_kw"] - baseline).clip(lower=0).fillna(0)
        rows.append({
            "machine_id": machine_id,
            "avg_kw": group["power_kw"].mean(),
            "peak_kw": group["power_kw"].max(),
            "hours": len(group),
            "baseline_kw": baseline.median() if baseline.notna().any() else group["power_kw"].median(),
            "estimated_excess_kwh": excess_kw.sum(),
            "estimated_waste_rupees": excess_kw.sum() * 8.5,
        })
    return pd.DataFrame(rows).set_index("machine_id").sort_values(
        "estimated_waste_rupees", ascending=False
    )

def local_or_edge_explanation(row, history):
    base_url = os.getenv("AI_BASE_URL", "").strip()
    model = os.getenv("AI_MODEL", "").strip()
    api_key = os.getenv("AI_API_KEY", "").strip()
    cause = probable_cause(row, history)
    fallback = (
        f"**{machine_state(row)} — {cause}.** "
        f"Temperature {row.temperature_c:.1f}°C, vibration {row.vibration_mm_s:.2f} mm/s, "
        f"power {row.power_kw:.2f} kW and load {row.load_pct:.0f}%. "
        + ("Inspect the machine before continued heavy operation." if row.risk_score >= 75
           else "Keep monitoring the next operating cycle.")
    )
    if not (base_url and model):
        return fallback
    prompt = (
        "Act as an industrial maintenance copilot. Do not invent sensor facts. "
        "Give a concise cause, evidence, immediate action and priority.\n"
        f"Machine: {row.machine_id}\nTemperature: {row.temperature_c:.2f} C\n"
        f"Vibration: {row.vibration_mm_s:.2f} mm/s\nPower: {row.power_kw:.2f} kW\n"
        f"Load: {row.load_pct:.1f}%\nRisk: {row.risk_score:.0f}/100\n"
        f"Rule-based signal: {cause}"
    )
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        r = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json={"model": model, "messages": [
                {"role": "system", "content": "You are a safety-conscious factory maintenance assistant."},
                {"role": "user", "content": prompt}
            ], "temperature": 0.1},
            timeout=8
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return fallback

def cpu_benchmark(df):
    sample = df[["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]].head(256)
    start = time.perf_counter()
    for _ in range(10):
        model = IsolationForest(n_estimators=80, contamination=.06, random_state=7)
        model.fit(sample)
        model.predict(sample)
    return (time.perf_counter() - start) / 10 * 1000

st.title("⚙️ FactoryPulse Edge")
st.markdown("### Autonomous, privacy-first factory intelligence — designed for CPU/edge deployment")
st.caption("Detect → Explain → Prioritise → Save energy. Keep sensitive telemetry inside the factory.")

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Telemetry CSV", type=["csv"])
    st.divider()
    st.caption("Demo mode uses synthetic machine telemetry. No external AI call is required.")
    st.caption("Optional inference adapter: set AI_BASE_URL, AI_MODEL and AI_API_KEY.")

try:
    raw = pd.read_csv(uploaded) if uploaded else make_demo_data()
    data = analyze(validate(raw))
except Exception as exc:
    st.error(str(exc))
    st.stop()

machines = sorted(data.machine_id.unique())
selected_machine = st.sidebar.selectbox("Machine", machines)
machine = data[data.machine_id == selected_machine]
latest = machine.iloc[-1]
energy = energy_insights(data)
anomalies = data[data.anomaly].sort_values("risk_score", ascending=False)
critical = int((data.risk_score >= 75).sum())
waste = float(energy.estimated_waste_rupees.sum())

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Factory state", "🔴 ATTENTION" if critical else "🟢 STABLE")
m2.metric("Machines", len(machines))
m3.metric("Critical events", critical)
m4.metric("Avg power", f"{data.power_kw.mean():.1f} kW")
m5.metric("Est. waste", f"₹{waste:,.0f}")

st.subheader("Factory floor")
cols = st.columns(3)
for i, mid in enumerate(machines):
    last = data[data.machine_id == mid].iloc[-1]
    with cols[i % 3]:
        st.metric(mid, machine_state(last), f"Risk {last.risk_score:.0f}/100")
        st.caption(f"{last.power_kw:.1f} kW · {last.temperature_c:.1f}°C · {last.vibration_mm_s:.2f} mm/s")

st.subheader(f"{selected_machine} — operating profile")
st.line_chart(machine.set_index("timestamp")[["temperature_c", "vibration_mm_s", "power_kw", "load_pct"]])

left, right = st.columns([1, 1])
with left:
    st.subheader("🔧 Maintenance intelligence")
    st.markdown(f"**State:** {machine_state(latest)}")
    st.markdown(f"**Risk score:** {latest.risk_score:.0f}/100")
    st.markdown(f"**Likely cause:** {probable_cause(latest, data)}")
    st.info(local_or_edge_explanation(latest, data))
with right:
    st.subheader("⚡ Energy intelligence")
    top = energy.head(5).copy()
    top["estimated_waste_rupees"] = top["estimated_waste_rupees"].round(0)
    st.dataframe(top[["avg_kw", "peak_kw", "estimated_excess_kwh", "estimated_waste_rupees"]],
                 use_container_width=True)
    st.caption("Waste estimate is a transparent demo heuristic, not a metered bill.")

st.subheader("🚨 Anomaly queue")
if len(anomalies):
    st.dataframe(
        anomalies[["timestamp", "machine_id", "temperature_c", "vibration_mm_s",
                   "power_kw", "load_pct", "risk_score"]].head(15),
        use_container_width=True, hide_index=True
    )
else:
    st.success("No anomalies detected in the current telemetry window.")

with st.expander("🧪 Edge performance & privacy"):
    latency = cpu_benchmark(data)
    st.metric("Local anomaly-pipeline benchmark", f"{latency:.1f} ms / 256-row batch")
    st.write("This measures the local anomaly pipeline only; it is not a Kompact AI benchmark.")
    st.write("For Phase 2, the inference layer will be benchmarked on the provided Kompact runtime.")
    st.write("Privacy mode: telemetry analysis is local by default. The optional AI endpoint is called only when explicitly configured.")

with st.expander("🏗️ Architecture"):
    st.code("""Machine sensors / CSV
        ↓
Local feature engineering
        ↓
Isolation Forest + interpretable risk engine
        ├── Maintenance cause inference
        ├── Energy waste estimation
        └── AI explanation adapter
                    ↓
        Local CPU / Kompact AI runtime
                    ↓
          FactoryPulse dashboard
""", language="text")

st.divider()
st.caption("FactoryPulse Edge • Build Next 2026 Phase-1 portfolio project • Kompact integration is isolated behind an inference adapter.")
