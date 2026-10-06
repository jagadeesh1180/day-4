# Evaluation Readiness

## Important constraint

The public Build Next 2026 page describes Phase 1 as online screening through a portfolio-project submission and Phase 2 as a fresh-code challenge using the Kompact AI Runtime. The public page does not publish a detailed numeric judging rubric.

Official reference: https://www.ziroh.com/hackathon

Therefore this matrix is an engineering preparation framework, **not an official scoring rubric**.

## Likely evaluation dimensions

| Dimension | What judges can verify | FactoryPulse evidence |
|---|---|---|
| Real-world impact | Clear operational problem and target user | MSME factory maintenance + energy workflow |
| AI/technical depth | Meaningful analysis rather than a static dashboard | Isolation Forest + multivariate risk + deterministic reasoning |
| Edge value | Local execution and measurable efficiency | No cloud AI required; local benchmark |
| Product usability | Clear operator decision flow | Detect → Explain → Prioritise → Save energy |
| Correctness | Reproducible inputs and defensive validation | Data contract + smoke tests + deterministic seeds |
| Honesty/evidence | Claims match measurements | DOES_NOT_CLAIM + explicit demo labels |
| Engineering quality | Tests, CI, containerization, documentation | pytest + GitHub Actions + Docker |
| Scalability | Clear path beyond demo | Adapter boundary and extensible telemetry schema |
| Privacy/security | Sensitive telemetry handled deliberately | Local-first default + security policy |
| Phase-2 readiness | Clear Kompact integration plan | Isolated inference adapter + measurement plan |

## What we must not do

- Do not claim that the current portfolio project uses Kompact.
- Do not claim production predictive accuracy from synthetic data.
- Do not present estimated energy waste as an actual electricity bill.
- Do not present local CPU benchmark numbers as Kompact numbers.
- Do not claim a public competitor's feature as our own.
- Do not add Phase-2 code that violates the fresh-code requirement.

## Judge-proofing strategy

A reviewer should be able to clone the repository, understand the architecture, run the app, load sample telemetry, inspect the evidence, and find the limitations without needing verbal clarification.
