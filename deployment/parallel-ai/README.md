# Parallel AI Platform Deployment Pack

This folder prepares MA-OS attestation workflows for **parallel operation across multiple AI platforms**.

## Purpose
Run several AI providers at once (OpenAI, Anthropic, Google/Gemini, local OSS) while preserving one deterministic output contract:
1. Each provider emits a candidate decision.
2. A shared normalizer converts provider outputs into `maos.attestation.v1` compatible payloads.
3. A single verifier/signer policy decides whether to approve, reject, or terminate.
4. Downstream smart-contract actions consume only signed attestations.

## Included Files
- `platform-manifest.yaml` — canonical parallel topology and routing policy.
- `openai.env.example` — OpenAI worker environment template.
- `anthropic.env.example` — Anthropic worker environment template.
- `gemini.env.example` — Gemini worker environment template.
- `local-oss.env.example` — local model worker template.
- `docker-compose.parallel.yml` — reference orchestrator for running workers in parallel.

## How to Use
1. Copy each `*.env.example` to a real `.env` file and fill secrets.
2. Ensure all workers point to the same attestation schema path: `spec/attestation.schema.json`.
3. Start services with compose:
   - `docker compose -f deployment/parallel-ai/docker-compose.parallel.yml up -d`
4. Send a test decision request to `orchestrator`.
5. Verify emitted records in `examples/sample-attestations.jsonl` style.

## Parallel Decision Policy (recommended default)
- **Mode:** quorum
- **Minimum agreeing workers:** 2 of 3 external providers
- **Tie-breaker:** local-oss worker
- **Fail-safe:** if no quorum -> `status=terminated`

## Security Requirements
- Provider keys must be isolated per worker.
- `decision_id` must be globally unique across all workers.
- Replay protection and freshness checks must run before signing.
- Signer keys are never exposed inside provider workers.
