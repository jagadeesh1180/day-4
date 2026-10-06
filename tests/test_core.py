import pandas as pd
from app import make_demo_data, validate, analyze, probable_cause

def test_demo_schema():
    df = make_demo_data(40)
    checked = validate(df)
    assert {"timestamp", "machine_id", "temperature_c", "vibration_mm_s", "power_kw", "load_pct"} <= set(checked.columns)

def test_analysis_adds_health_signals():
    df = analyze(validate(make_demo_data(60)))
    assert "anomaly" in df.columns
    assert "risk_score" in df.columns
    assert df["risk_score"].between(0, 100).all()

def test_cause_engine_returns_actionable_category():
    df = analyze(validate(make_demo_data(80)))
    row = df.iloc[-1]
    cause = probable_cause(row, df)
    assert isinstance(cause, str)
    assert len(cause) > 5
