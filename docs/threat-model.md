# Threat Model — Bunker to Smart Contract Path

## Objective
Prevent unauthorized or low-integrity decisions from triggering on-chain actions.

## Key threats

### 1) Signature spoofing
- **Threat:** forged attestation passes as trusted output.
- **Control:** strict signer allowlist + cryptographic verification.

### 2) Replay attacks
- **Threat:** old valid attestation retriggered for new action.
- **Control:** unique `decision_id` tracking + timestamp freshness window.

### 3) Payload tampering
- **Threat:** attestation body altered after issuance.
- **Control:** recompute and validate `input_hash` and `decision_hash`.

### 4) Reasoning instability
- **Threat:** over-complex input causes unsafe output.
- **Control:** Saadia bunker depth/complexity ceiling + deterministic termination.

### 5) Policy drift
- **Threat:** verifier accepts previously disallowed states.
- **Control:** explicit schema versioning and governance-controlled policy updates.

## Residual risk
- Key compromise remains critical; requires rapid rotation and signer revocation runbook.
