# Telemetry Data Contract

FactoryPulse accepts CSV telemetry with the following fields.

| Field | Type | Unit | Required | Rules |
|---|---|---|---|---|
| timestamp | datetime | ISO/date-time | yes | Must parse successfully |
| machine_id | string | — | optional | Defaults to M-01; non-empty when supplied |
| temperature_c | numeric | °C | yes | Finite numeric value |
| vibration_mm_s | numeric | mm/s | yes | Finite and non-negative |
| power_kw | numeric | kW | yes | Finite and non-negative |
| load_pct | numeric | % | yes | 0–100 |

## Processing contract

1. Input is copied before transformation.
2. Timestamps are parsed and rows are ordered by machine and time.
3. Numeric columns are coerced and validated.
4. Oversized uploads are rejected above the application safety limit.
5. Each machine is analyzed independently.
6. The anomaly model and risk engine operate on the four telemetry features.
7. Energy estimates use a machine-local rolling power baseline.

The schema is intentionally small so the same contract can be populated from CSV exports, gateways, or future sensor adapters.
