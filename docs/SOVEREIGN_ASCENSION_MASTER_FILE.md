# 📜 Sovereign Ascension: Deployment Master-File

## Target
Automated, encrypted deployment of the AMNE (Abulafia-Maimonides Neural Engine).

## 1) Infrastructure Layer

### S3 + KMS
- Provision private S3 bucket `sovereign-vault` with:
  - Versioning enabled.
  - Object Lock enabled (governance retention).
  - SSE-KMS default encryption.
- Provision customer-managed KMS key alias `alias/sovereign-master-key`.

### IAM Role Requirements
Runtime role must include:
- `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`.
- Multipart operations: `s3:CreateMultipartUpload`, `s3:UploadPart`, `s3:CompleteMultipartUpload`, `s3:AbortMultipartUpload`, `s3:ListMultipartUploadParts`.
- KMS operations: `kms:Encrypt`, `kms:Decrypt`, `kms:GenerateDataKey`, `kms:DescribeKey`.

See `infra/cloudformation/sovereign-vault.yaml`.

## 2) Sovereign Multipart Upload Engine

File: `scripts/s3_multipart_upload.py`

Highlights:
- 50MB chunks (`PART_SIZE = 50 * 1024 * 1024`).
- Crash-resume via `state.json`.
- SHA256 injected into object metadata for future integrity validation.
- Server-side encryption through KMS key ID.

## 3) Ascension CI/CD Pipeline

File: `.github/workflows/ascension-deploy.yml`

- Trigger: pushes to `releases/**`.
- Auth: GitHub OIDC -> AWS role assumption.
- Uploads each file from `releases/` to S3 with KMS encryption.
- Performs SHA256 integrity validation against S3 metadata; mismatch fails workflow.

## 4) AMNE Logical Compiler

Directory: `amne/`

- Lark grammar parses core modal relations in Hebrew/English.
- Built-in vocabulary for terms like `שכל פועל`, `נבואי`, `צירוף`, `נמצא`.
- Exports:
  - JSON-LD graph structure.
  - RDF/Turtle triples.

## 5) Semantic Dashboard

File: `dashboard/app.py`

- Dash + Cytoscape app for ontology graph visualization.
- Real-time tension gauge (`λ₂`) rendered as a status panel.
- Reads compiled graph artifacts and displays interactive nodes/edges.

## 6) Runbook for Jules

1. Deploy CloudFormation stack (`infra/cloudformation/sovereign-vault.yaml`).
2. Configure IAM OIDC trust from AWS to GitHub repository.
3. Install Python dependencies and run AMNE compiler to generate artifacts.
4. Start Dash dashboard inside VPC for operational monitoring.

## Memory Log
- Subject: Unified sovereign deployment protocol for Jules.
- Action: Consolidated infrastructure, automation, compiler, and dashboard into one operational playbook.
- Status: **DEPLOYMENT READY**.
