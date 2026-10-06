# Judge Demo Checklist

## Before demo

- Open the repository at the main branch.
- Confirm the README is the first navigation point.
- Start the app locally.
- Keep `sample_telemetry.csv` available for upload.
- Verify no API key is present in the repository or shell history used for recording.

## 120-second sequence

1. **Problem — 15s:** explain the MSME factory constraint.
2. **Factory floor — 20s:** show six machines and the attention state.
3. **Anomaly — 20s:** select an abnormal machine and show the four signals.
4. **Maintenance — 20s:** show risk, evidence, likely cause, and action.
5. **Energy — 15s:** show machine-local baseline and estimated excess.
6. **Edge — 15s:** show local benchmark and privacy boundary.
7. **Close — 15s:** state why local operational intelligence is the product.

## Questions to expect

### Why Isolation Forest?

It is a practical unsupervised baseline when labelled failure data is scarce. It is not presented as proof of failure.

### Why not cloud AI?

The core telemetry path does not require cloud connectivity. Optional explanation is isolated behind an adapter.

### Where is Kompact?

Phase 1 is a portfolio project. Kompact is required for the finalist Phase 2 build; the repository deliberately does not fabricate unavailable Phase-2 measurements.

### What is novel?

The claim is not algorithmic novelty. The product differentiation is the focused MSME workflow, local-first boundary, interpretable decisions, energy + maintenance combination, and evidence discipline.

### What would you build next?

Connect real sensors, establish labelled failure/maintenance outcomes, integrate Kompact, and benchmark the complete system on target CPU hardware.
