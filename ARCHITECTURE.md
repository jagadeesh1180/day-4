# FactoryPulse Edge — Architecture

## Product thesis

FactoryPulse is not a generic chatbot. It is an edge-native decision system for factories where connectivity, cloud cost and data sovereignty matter.

## Data flow

1. Machine sensors or CSV telemetry provide temperature, vibration, power and load.
2. Local feature engineering creates rolling baselines and deviations.
3. Isolation Forest detects multivariate anomalies.
4. An interpretable risk engine combines signal deviations into a maintenance risk score.
5. A deterministic cause engine maps signal combinations to likely failure modes.
6. An optional OpenAI-compatible inference adapter turns the evidence into a concise maintenance explanation.
7. The dashboard exposes machine state, energy waste, anomaly queue and recommended action.

## Why edge-first?

Factory telemetry can be commercially sensitive. The default application does not require a cloud AI API. The inference adapter is isolated so a local CPU runtime can be used without changing the product layer.

For Build Next Phase 2, the adapter can target the official Kompact AI Runtime supplied to finalists.

## Designed for measurable engineering

The dashboard includes a local benchmark for the anomaly pipeline. It intentionally labels this as a local pipeline benchmark, not a Kompact benchmark. This prevents unsupported performance claims.

Phase 2 should add:
- Kompact inference latency
- CPU utilization
- RAM footprint
- throughput
- offline operation
- quality comparison against the baseline explanation path

## Why this can scale

The same pattern works for textile machines, pumps, compressors, CNC equipment, motors and other industrial assets. The sensor schema can be extended without changing the inference boundary.
