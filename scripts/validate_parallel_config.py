from pathlib import Path
import json


def validate_manifest_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    required = ["version:", "providers:", "orchestrator:", "signing:"]
    missing = [k for k in required if k not in text]
    if missing:
        raise SystemExit(f"manifest missing required sections: {missing}")


def validate_json_schema(path: Path) -> None:
    # Structural parse validation only (no external deps)
    json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = root / "deployment" / "parallel-ai" / "platform-manifest.yaml"
    schema = root / "spec" / "attestation.schema.json"

    if not manifest.exists():
        raise SystemExit("platform-manifest.yaml not found")
    if not schema.exists():
        raise SystemExit("attestation schema not found")

    validate_manifest_text(manifest)
    validate_json_schema(schema)
    print("parallel config validation: ok")


if __name__ == "__main__":
    main()
