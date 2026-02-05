# Qualia — MA-OS Bunker for Smart Contracting

Qualia now defines the **Bunker pattern** for smart-contract-integrated decision systems.

The goal is to move from opaque prediction to **verifiable attestation**:
- Inputs are filtered for instability/noise.
- Decisions are constrained by deterministic safety gates.
- Every decision emits a cryptographically verifiable evidence trail.
- Smart contracts consume attestations, not raw model output.

## Core Principle
> We do not predict. We attest.

## Bunker Architecture (Operational View)

### 1) Input Stream
Untrusted data enters from markets, APIs, user prompts, or agent outputs.

### 2) Raqia Filter (Boundary Security)
The Raqia layer inspects and normalizes incoming data, rejecting malformed, adversarial, or high-noise payloads before they reach the reasoning core.

### 3) Saadia Bunker (Safe Termination)
The core enforces bounded reasoning depth and complexity thresholds.
If inquiry instability is detected, execution hard-stops and emits a deterministic failure attestation.

### 4) Signed Seal (Forensic Immutability)
Each accepted decision is serialized into an append-only record and signed (Ed25519), with content digesting (SHA-256) to support tamper-evident replay.

### 5) Contract Action Layer (Smart Contract Native)
On-chain automation is triggered only from signed attestations that satisfy policy constraints (freshness, signer set, decision type, and integrity checks).

## Minimal Attestation Envelope

```json
{
  "version": "maos.attestation.v1",
  "decision_id": "uuid",
  "timestamp": "2026-01-01T00:00:00Z",
  "subject_ratio": 0.982,
  "input_hash": "sha256:...",
  "decision_hash": "sha256:...",
  "policy": {
    "max_depth": 100,
    "termination_mode": "dynamic_truncation"
  },
  "status": "approved|rejected|terminated",
  "signature": {
    "scheme": "ed25519",
    "key_id": "raqia-main-01",
    "sig": "base64..."
  }
}
```

## Smart Contract Integration Requirements

A contract that consumes MA-OS attestations should validate:
1. **Signature validity** against an allowlisted verifier key.
2. **Message integrity** by recomputing digest fields.
3. **Freshness window** (`timestamp` and optional nonce/epoch).
4. **Policy conformance** (`status`, `max_depth`, and allowed decision classes).
5. **Replay resistance** (`decision_id` uniqueness and/or monotonic sequence).

## Bunker Preparation Checklist

- [ ] Define canonical attestation schema and versioning policy.
- [ ] Define signer key management and rotation process.
- [ ] Implement append-only JSONL audit log and digest chaining.
- [ ] Build verifier library (off-chain + on-chain compatible format).
- [ ] Add policy engine for termination and rejection thresholds.
- [ ] Create integration tests for signature/replay/freshness failures.
- [ ] Publish smart-contract verifier interface and reference adapter.

## Immediate Build Plan

### Phase A — Protocol Freeze
- Freeze schema for `maos.attestation.v1`.
- Freeze error taxonomy (`rejected`, `terminated`, `invalid_signature`, etc.).

### Phase B — Reference Implementation
- Build a deterministic pipeline: filter -> bunker -> seal.
- Emit signed attestations and append-only audit entries.

### Phase C — Chain Adapter
- Implement a minimal verifier contract/API adapter.
- Accept only valid attestations and reject replay/expired records.

### Phase D — Governance & Audit
- Add external verification guide.
- Add operational runbooks for key rotation and incident handling.

## Repository Status
Current repository contains concept docs only. Next step is to add:
- `/spec/attestation.schema.json`
- `/spec/verifier-interface.md`
- `/docs/threat-model.md`
- `/examples/sample-attestations.jsonl`


## Parallel Multi-Platform Deployment
For running MA-OS across multiple AI platforms in parallel, use:
- `deployment/parallel-ai/platform-manifest.yaml`
- `deployment/parallel-ai/docker-compose.parallel.yml`
- Provider env templates in `deployment/parallel-ai/*.env.example`

Validation helper:
- `python scripts/validate_parallel_config.py`
