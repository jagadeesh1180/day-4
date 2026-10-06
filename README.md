# FactoryPulse Edge AI

FactoryPulse Edge AI is a privacy-first factory intelligence prototype for small and medium-sized manufacturers.

It combines:
- Machine telemetry and energy signals
- Explainable anomaly detection
- Maintenance-risk scoring
- Local AI explanations through an OpenAI-compatible inference endpoint
- A dashboard designed for edge/CPU deployment

## Why this matters

Small factories often cannot justify expensive cloud AI infrastructure, while machine and production data can be sensitive. FactoryPulse Edge is designed around the idea that intelligence can run close to the machines.

The project is structured so the AI inference layer can be pointed at Kompact AI / SBox when access is available.

## Demo

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional AI endpoint:

```bash
export AI_BASE_URL="http://localhost:8000/v1"
export AI_API_KEY="your-key"
export AI_MODEL="your-model"
```

If no AI endpoint is configured, the application still provides deterministic anomaly detection and maintenance recommendations.

## Architecture

```
Machine / CSV telemetry
        |
        v
 Feature engineering
        |
        +----> Isolation Forest anomaly detection
        |
        +----> Energy efficiency scoring
        |
        v
 Risk engine
        |
        v
 AI explanation layer
        |
        v
 Factory dashboard
```

## Hackathon positioning

FactoryPulse Edge is a portfolio project for Build Next 2026. The Phase 2 architecture is intentionally inference-provider agnostic, with an OpenAI-compatible adapter so the same application can use Kompact AI as the core inference runtime when finalist access is provided.

The application focuses on practical impact: early anomaly detection, energy waste visibility, maintenance prioritisation, and privacy-preserving deployment.

## Important

This repository contains the original portfolio MVP. For the Build Next Phase 2 challenge, new challenge-period code should be written during the official challenge window and the Kompact AI Runtime should be used as required by the official rules.
