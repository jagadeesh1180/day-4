# Security and Privacy

## Scope

FactoryPulse is designed for industrial telemetry that may be commercially sensitive. The default path performs telemetry analysis locally.

## Secrets

- Never commit `AI_API_KEY`, credentials, tokens, or production telemetry.
- Configure optional inference credentials through environment variables or a secret manager.
- The dashboard does not display the configured API key.

## Network boundary

The optional AI endpoint is disabled unless `AI_BASE_URL` and `AI_MODEL` are explicitly configured. When enabled, telemetry-derived context is sent to that configured endpoint.

For a production deployment, use an allow-listed internal endpoint, TLS, authentication, network egress controls, and an audit policy appropriate for the factory.

## Data handling

Use synthetic or anonymized data for demos. Production deployments should define retention, access control, incident response, and data-subject handling consistent with applicable law and organizational policy.

## Reporting

Do not publish confidential factory telemetry, credentials, or personal data in issues. Report security concerns privately to the project owner.
