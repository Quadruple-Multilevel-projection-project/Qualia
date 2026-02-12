# Qualia

Sovereign deployment scaffold for the AMNE (Abulafia-Maimonides Neural Engine).

## Components
- **Infrastructure**: `infra/cloudformation/sovereign-vault.yaml` provisions S3, KMS, and OIDC-backed IAM role.
- **Upload Engine**: `scripts/s3_multipart_upload.py` supports resumable 50MB multipart uploads with SHA256 metadata.
- **CI/CD**: `.github/workflows/ascension-deploy.yml` uploads `releases/**` artifacts via AWS OIDC and verifies integrity.
- **Compiler**: `amne/compiler.py` parses Hebrew/English modal relation statements into graph outputs (`JSON`, `JSON-LD`, `RDF Turtle`).
- **Dashboard**: `dashboard/app.py` renders the semantic graph and λ₂ tension gauge.
- **Master Document**: `docs/SOVEREIGN_ASCENSION_MASTER_FILE.md`.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Compile sample ontology text:
```bash
cat > sample.txt <<'TXT'
שכל פועל נמצא נמצא
Moses prophetic Active_Intellect
TXT
python amne/compiler.py --input sample.txt --out-dir build
```

Run dashboard:
```bash
python dashboard/app.py
```

Visit `http://localhost:8050`.
