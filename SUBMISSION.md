# Build Next 2026 — Phase 1 Portfolio Submission

## FactoryPulse Edge

**Autonomous, privacy-first factory intelligence for MSMEs**

### One-line pitch

FactoryPulse Edge turns machine telemetry into explainable maintenance priorities and energy-waste signals locally, so small factories can use AI without making cloud infrastructure a prerequisite.

### Problem

Many smaller factories have machine data but limited access to predictive-maintenance systems. Cloud-first AI can introduce recurring inference costs, connectivity dependence and data-sovereignty concerns.

### What we built

FactoryPulse provides one operator workflow:

**Detect → Explain → Prioritise → Save energy**

It includes:
- Multivariate Isolation Forest anomaly detection.
- Rolling local baselines.
- Interpretable maintenance-risk scoring.
- Evidence-based probable-cause classification.
- Energy baseline and excess-consumption estimation.
- Six-machine factory-floor view.
- Local anomaly-pipeline benchmark.
- Optional OpenAI-compatible inference adapter.
- Docker and automated smoke tests.

### Why edge is the product

The project does not merely put a cloud application on an edge device. Its default telemetry analysis is local. The AI explanation layer is isolated behind an inference adapter, allowing a CPU-local runtime to be used without changing the operator workflow.

### What we intentionally do not claim

We do not claim current Kompact performance, production energy savings, real factory failure rates, or real-world predictive accuracy. Those require measurement.

### Phase 2 plan if selected

Use the official Kompact AI Runtime as the core inference component and measure:
- End-to-end latency.
- CPU utilization.
- Memory footprint.
- Throughput.
- Offline operation.
- Explanation quality.
- Cost/TCO implications.

All Phase 2 implementation will follow the official fresh-code requirement.

### Demo

    pip install -r requirements.txt
    streamlit run app.py

### Repository

https://github.com/jagadeesh1180/day-4
