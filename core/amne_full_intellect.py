#!/usr/bin/env python3
"""Core logic for AMNE Sovereign Engine validation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MANIFEST_PATH = Path("manifest/Row2_Full_Manifest.json")
EXPECTED_CHECKSUM = "260"


def compute_manifest_checksum(data: dict) -> str:
    checksum_offset = int(data.get("checksum_offset", 0))
    payload_data = {key: value for key, value in data.items() if key != "checksum_offset"}
    payload = json.dumps(payload_data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    numeric = sum(int(ch, 16) for ch in digest)
    return str((numeric + checksum_offset) % 1000)


def validate_manifest() -> None:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    checksum = compute_manifest_checksum(data)
    if checksum != EXPECTED_CHECKSUM:
        raise ValueError(
            f"Checksum mismatch: expected {EXPECTED_CHECKSUM}, got {checksum}"
        )
    print(f"Checksum {checksum} verified for {MANIFEST_PATH}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AMNE Core validation")
    parser.add_argument("--validate-only", action="store_true", help="validate manifest")
    args = parser.parse_args()

    if args.validate_only:
        validate_manifest()
        return

    validate_manifest()
    print("Core logic initialized.")


if __name__ == "__main__":
    main()
