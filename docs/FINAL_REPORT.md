# FactoryPulse Edge — Final Technical Report

## 1. Executive summary

FactoryPulse Edge is a local-first industrial intelligence prototype for resource-constrained MSME factories. It converts machine telemetry into three operator-facing outputs: machine-health risk, maintenance evidence, and energy-waste signals.

The central product decision is to keep the default telemetry-analysis path local. This makes connectivity and cloud AI availability non-essential to the core workflow.

## 2. Problem

Smaller manufacturers may have useful telemetry but lack the infrastructure, budget, or data-governance appetite associated with cloud-heavy industrial AI. A practical system therefore needs to be lightweight, interpretable, and deployable near the machines.

## 3. Solution

FactoryPulse implements:

- Multivariate Isolation Forest anomaly detection.
- Rolling local baselines.
- Interpretable weighted risk scoring.
- Deterministic probable-cause classification.
- Machine-local energy baseline and excess-consumption estimation.
- Six-machine factory-floor visualization.
- Optional OpenAI-compatible explanation adapter.
- Local CPU anomaly-pipeline timing.
- CSV validation and a reproducible demo dataset.

## 4. Architecture

```
Sensors / CSV
    |
    v
Validation + normalization
    |
    v
Per-machine feature analysis
    |
    +--> Isolation Forest
    |
    +--> Risk engine
    |
    +--> Energy baseline
    |
    v
Maintenance evidence
    |
    +--> Local deterministic explanation
    |
    +--> Optional inference adapter
    |
    v
Operator dashboard
```

The inference adapter is intentionally isolated so a future local runtime can replace the optional endpoint without redesigning the product layer.

## 5. Current evidence

The current project demonstrates software behaviour using synthetic telemetry and local computation. The repository includes automated tests, CI configuration, Docker packaging, a telemetry contract, and explicit evidence controls.

The local benchmark measures the anomaly pipeline only. It is not a Kompact benchmark.

## 6. Limitations

- Synthetic telemetry is not equivalent to production sensor data.
- Isolation Forest anomaly labels are unsupervised and are not proof of equipment failure.
- Probable-cause classification is rule-based and should be treated as maintenance triage, not a diagnosis.
- Energy waste is an estimate based on a local baseline and tariff assumption; it is not a metered bill.
- No production accuracy, savings, uptime, or ROI claim is made.

## 7. Validation strategy

The test suite checks:

1. six-machine deterministic demo generation;
2. required-column validation;
3. invalid timestamp rejection;
4. default machine-ID behaviour;
5. numeric/range validation;
6. anomaly/risk output shape and bounds;
7. per-machine energy output;
8. maintenance-cause output.

GitHub Actions runs Python compilation and the test suite.

## 8. Security and privacy

Telemetry is processed locally by default. Optional inference is opt-in through environment variables. Production deployment should enforce TLS, endpoint allow-listing, authentication, egress controls, access control, retention policies, and appropriate privacy/legal review.

## 9. Competitive position

The project does not claim that edge AI or predictive maintenance is novel by itself. The intended differentiation is the combination of:

- MSME-focused deployment assumptions;
- local-first telemetry processing;
- one operational workflow joining maintenance and energy;
- inspectable decision logic;
- explicit evidence discipline;
- a replaceable inference boundary for future edge runtimes.

## 10. Phase-2 plan

If selected, Phase 2 should use the official Kompact AI Runtime as a core inference component and measure, rather than assume:

- end-to-end latency;
- CPU utilization;
- memory footprint;
- throughput;
- offline behaviour;
- explanation quality;
- model/resource trade-offs;
- total deployment cost.

All Phase-2 challenge-period implementation should be fresh code and should comply with the published challenge rules.

## 11. Release decision

**Phase-1 portfolio status: submission-ready.**

The repository is structured so a reviewer can reproduce the demo and audit the claims. Remaining uncertainty is intentionally empirical: real factory telemetry and Phase-2 Kompact measurements are required before making production-performance claims.
