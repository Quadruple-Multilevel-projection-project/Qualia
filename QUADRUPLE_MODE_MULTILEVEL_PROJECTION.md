# Quadruple Mode Multilevel Projection — Bunker Smart Contracting Edition

This projection compiles the repository into a four-mode, multi-level execution model focused on preparing the **MA-OS Bunker** for **smart-contract-native attestation**.

## Scope compiled (current files)
1. `README.md`
2. `LICENSE`
3. `QUADRUPLE_MODE_MULTILEVEL_PROJECTION.md`

## Mode 1 — System Projection (What exists)
### Level 1: Mission
- Define a deterministic decision infrastructure where contract actions are gated by signed attestations.

### Level 2: Primitive components
- Raqia filter concept for inbound noise/integrity control.
- Saadia bunker concept for bounded reasoning and safe termination.
- Signed seal concept for forensic audit and external verification.

### Level 3: Delivery condition
- No executable verifier artifacts yet; system currently in architecture/specification stage.

## Mode 2 — Risk Projection (What can break)
### Level 1: Integrity risk
- Unsigned or improperly signed outputs could trigger unauthorized contract behavior.

### Level 2: Replay risk
- Previously valid attestations can be replayed unless uniqueness/freshness guards are enforced.

### Level 3: Complexity risk
- Unbounded reasoning depth can produce unstable outputs without deterministic termination controls.

## Mode 3 — Contract Projection (What must be true on-chain)
### Level 1: Verification truth
- Contract must verify attestation signature against allowlisted key set.

### Level 2: Data truth
- Contract/off-chain adapter must confirm hash integrity and schema version compatibility.

### Level 3: Policy truth
- Contract logic must reject stale, replayed, or policy-violating attestations.

## Mode 4 — Execution Projection (What to build now)
### Level 1: Protocol hardening
1. Freeze `maos.attestation.v1` schema.
2. Define decision status taxonomy and invariant rules.

### Level 2: Implementation hardening
1. Build append-only JSONL audit ledger with hash chain.
2. Implement signer service with Ed25519 key rotation policy.

### Level 3: Integration hardening
1. Publish verifier interface for EVM-compatible adapters.
2. Add test vectors: valid, stale, replayed, tampered, invalid-signature.

## Bunker Readiness Gate
The bunker is considered ready for smart contracting only when:
- Signature verification passes for canonical test vectors.
- Replay and freshness controls are enforced in integration tests.
- Termination events emit deterministic, signed failure attestations.
- Audit replay can reconstruct and validate every historical decision.

## Start compiling now
Active compile queue:
1. **Schema compile**: add `/spec/attestation.schema.json` with strict field typing.
2. **Ledger compile**: add `/examples/sample-attestations.jsonl` with digest chaining examples.
3. **Verifier compile**: add `/spec/verifier-interface.md` for contract-side validation.
4. **Threat compile**: add `/docs/threat-model.md` covering spoof, replay, and drift scenarios.
