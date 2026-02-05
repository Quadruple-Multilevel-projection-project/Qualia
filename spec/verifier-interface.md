# Verifier Interface (Draft)

This document defines a minimal verifier contract interface for consuming MA-OS attestations.

## Verification responsibilities
1. Verify Ed25519 signature against approved signer registry.
2. Validate freshness window from `timestamp`.
3. Enforce replay protection on `decision_id`.
4. Enforce policy constraints (`status`, `max_depth`, and profile-specific rules).

## Suggested contract-facing function

```solidity
function verifyAndConsume(
    bytes calldata canonicalAttestation,
    bytes calldata signature,
    bytes32 decisionId,
    uint64 timestamp,
    bytes32 inputHash,
    bytes32 decisionHash,
    uint8 status
) external returns (bool ok);
```

## Decision semantics
- `approved`: downstream action may proceed if all checks pass.
- `rejected`: action must not proceed; optionally emit rejection event.
- `terminated`: action must not proceed; emit safe-stop event.

## Required events
- `AttestationAccepted(bytes32 decisionId, bytes32 decisionHash)`
- `AttestationRejected(bytes32 decisionId, string reason)`

## Rejection reasons (minimum)
- `INVALID_SIGNATURE`
- `STALE_ATTESTATION`
- `REPLAY_ATTEMPT`
- `POLICY_VIOLATION`
- `UNSUPPORTED_SCHEMA_VERSION`
