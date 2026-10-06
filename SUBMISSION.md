# Build Next 2026 — Phase 1 Portfolio Submission

## Project
**FactoryPulse Edge AI — Privacy-First Factory Intelligence for MSMEs**

## Problem
Small and medium-sized factories generate machine telemetry but often lack affordable predictive-maintenance and energy-intelligence systems. Cloud-only AI can add recurring inference costs and create data-sovereignty concerns.

## Solution
FactoryPulse Edge AI analyzes machine temperature, vibration, power and load locally to identify abnormal operating conditions and prioritize maintenance actions. An OpenAI-compatible local inference adapter provides natural-language explanations without requiring the application architecture to be tied to a single cloud provider.

## AI components
- Isolation Forest anomaly detection
- Interpretable risk scoring
- Energy-consumption monitoring
- AI-generated maintenance explanations
- Edge/local inference adapter

## Expected impact
- Earlier identification of machine abnormalities
- Reduced unplanned downtime
- Better visibility into energy waste
- Lower cloud dependency
- Stronger privacy for industrial telemetry

## Phase 2 direction
When finalist access to Kompact AI Runtime is provided, the inference adapter will be configured to use the Kompact runtime as the core AI inference layer. The final challenge implementation will follow the official fresh-code and technology requirements.

## Demo
```bash
pip install -r requirements.txt
streamlit run app.py
```
