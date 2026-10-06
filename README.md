# FactoryPulse Edge

## Autonomous, privacy-first factory intelligence for MSMEs

FactoryPulse Edge turns machine telemetry into three things an operator can act on:

1. **Machine health** — multivariate anomaly detection and interpretable risk scoring.
2. **Maintenance intelligence** — evidence-backed likely-cause classification and action priority.
3. **Energy intelligence** — local baselines and transparent estimates of abnormal consumption.

The default application works without a cloud AI service. The inference boundary is isolated so a local CPU inference runtime can be used without redesigning the product.

## Why this project is different

Generic AI assistants compete on model size and conversation quality. FactoryPulse competes on **where AI runs, what data it sees, and whether the decision can be acted on**.

The project is intentionally built around an MSME factory because smaller manufacturers need useful intelligence without assuming a GPU cluster, constant connectivity, or willingness to export sensitive production telemetry.

## Competitive research

Public projects show that industrial edge AI is already a crowded technical area. Examples include:
- A predictive-maintenance project using LightGBM, ONNX and a Streamlit dashboard.
- A more elaborate platform combining Kafka, ONNX Runtime, PostgreSQL, Redis, RAG and an LLM incident agent.
- MSME-focused projects combining offline predictive maintenance and energy optimization.
- TinyML projects running vibration/fault detection on microcontrollers.

FactoryPulse therefore does **not** claim novelty simply because it says "edge AI" or "predictive maintenance".

Our differentiation is the combination of:
- A deliberately small MSME deployment target.
- A single operator workflow: detect → explain → prioritise → save energy.
- Local-first operation with no required AI API.
- Transparent, inspectable risk logic instead of an unsupported "failure probability" claim.
- Built-in local performance measurement.
- An explicit inference adapter ready for the Kompact AI Runtime in Phase 2.
- Evidence discipline: current measurements are separated from future Kompact measurements.

## Product demo

The dashboard shows:
- Six simulated machines on a factory floor.
- Health state and risk for each machine.
- Temperature, vibration, power and load trends.
- Anomaly queue.
- Likely maintenance cause.
- Energy waste table.
- Local CPU anomaly-pipeline benchmark.
- Privacy/edge architecture.

Run:

    pip install -r requirements.txt
    streamlit run app.py

Optional AI-compatible endpoint:

    AI_BASE_URL=http://localhost:8000/v1
    AI_MODEL=your-model
    AI_API_KEY=your-key

Without those variables, FactoryPulse still runs locally.

## Architecture

    Machine sensors / CSV
             |
             v
    Local feature engineering
             |
             +--> Isolation Forest
             |
             +--> Interpretable risk engine
             |
             +--> Energy baseline engine
             |
             v
       Maintenance reasoning
             |
             v
       AI explanation adapter
             |
             v
    Local CPU / future Kompact runtime
             |
             v
       FactoryPulse UI

## Phase 1 / Phase 2 boundary

Phase 1 is the portfolio project. The current repository contains the portfolio implementation.

If selected for Phase 2, the challenge-period implementation must follow the official fresh-code requirement and use the Kompact AI Runtime as a core component. We will then measure actual Kompact latency, CPU utilization, memory, throughput and offline behaviour rather than inventing benchmark numbers.

## Engineering quality

- Python 3.12
- Streamlit
- Pandas / NumPy
- Scikit-learn Isolation Forest
- Requests-based inference adapter
- Dockerfile
- Pytest smoke tests
- Architecture and demo documentation

## Evidence policy

See DOES_NOT_CLAIM.md. FactoryPulse never presents simulated savings, synthetic telemetry or future Kompact benchmarks as real-world measurements.

## License

MIT


## Submission readiness

- **Reproducible demo:** `sample_telemetry.csv` contains multiple machines and an intentionally abnormal operating window.
- **Automated validation:** `pytest -q` covers input validation, six-machine demo generation, anomaly scoring, energy estimation and maintenance-cause output.
- **Continuous integration:** GitHub Actions runs compilation and the smoke suite on pushes and pull requests.
- **Energy methodology:** waste is estimated against each machine's own rolling power baseline, avoiding a cross-machine baseline.
- **Evidence discipline:** synthetic telemetry, heuristic savings estimates and future Kompact measurements are explicitly labelled; no production claims are presented as measured facts.

## Judge-facing differentiation

FactoryPulse is deliberately narrow: **edge-native operational intelligence for resource-constrained MSME factories**. The product combines anomaly detection, interpretable risk, maintenance evidence and energy signals in one local workflow. The edge boundary is a product requirement, not a deployment afterthought.

For Phase 2, the isolated inference adapter is the integration point for the official Kompact AI Runtime. We will report measured latency, CPU, memory, throughput and offline behaviour rather than inventing benchmark numbers.
