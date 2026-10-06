import pandas as pd
import pytest

from app import REQUIRED, analyze, energy_insights, make_demo_data, probable_cause, validate


def test_demo_data_has_six_machines():
    df = make_demo_data(n=48)
    assert set(df["machine_id"]) == {"M-01", "M-02", "M-03", "M-04", "M-05", "M-06"}
    assert REQUIRED.issubset(df.columns)
    assert len(df) == 288


def test_validate_rejects_invalid_timestamp():
    df = pd.DataFrame({
        "timestamp": ["not-a-date"], "temperature_c": [60],
        "vibration_mm_s": [2], "power_kw": [7], "load_pct": [70]
    })
    with pytest.raises(ValueError, match="invalid dates"):
        validate(df)


def test_validate_adds_default_machine_id():
    df = pd.DataFrame({
        "timestamp": ["2026-01-01"], "temperature_c": [60],
        "vibration_mm_s": [2], "power_kw": [7], "load_pct": [70]
    })
    assert validate(df)["machine_id"].tolist() == ["M-01"]


def test_analysis_produces_valid_scores():
    out = analyze(make_demo_data(n=60))
    assert {"risk_score", "anomaly", "anomaly_score"}.issubset(out.columns)
    assert out["risk_score"].between(0, 100).all()
    assert out["anomaly"].dtype == bool


def test_energy_baseline_is_per_machine():
    out = energy_insights(make_demo_data(n=60))
    assert len(out) == 6
    assert (out["estimated_excess_kwh"] >= 0).all()
    assert (out["estimated_waste_rupees"] >= 0).all()


def test_probable_cause_is_actionable():
    data = analyze(make_demo_data(n=60))
    cause = probable_cause(data.iloc[-1], data)
    assert isinstance(cause, str) and len(cause) > 5


def test_validate_rejects_non_numeric_and_invalid_ranges():
    base = {
        "timestamp": ["2026-01-01"],
        "temperature_c": [60],
        "vibration_mm_s": [2],
        "power_kw": [7],
        "load_pct": [70],
    }
    bad_numeric = pd.DataFrame({**base, "power_kw": ["bad"]})
    with pytest.raises(ValueError, match="power_kw"):
        validate(bad_numeric)

    bad_load = pd.DataFrame({**base, "load_pct": [101]})
    with pytest.raises(ValueError, match="load_pct"):
        validate(bad_load)
