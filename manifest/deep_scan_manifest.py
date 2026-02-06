import json
from pathlib import Path
from typing import Iterable


ACCIDENT_TERMS = {"accident", "מקרה"}


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_strings(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for item in value.values():
            yield from collect_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from collect_strings(item)
    elif isinstance(value, str):
        yield value


def deep_scan_manifest(path: Path) -> list[str]:
    manifest = load_manifest(path)
    issues: list[str] = []

    header = manifest.get("header", {})
    checksum = header.get("checksum")
    if checksum != 260:
        issues.append(f"Checksum mismatch: expected 260, found {checksum!r}.")

    lowered_strings = {text.casefold() for text in collect_strings(manifest)}
    if ACCIDENT_TERMS & lowered_strings:
        issues.append("Manifest contains Accident/מקרה term, which violates checksum 260.")

    return issues


def main() -> None:
    manifest_path = Path(__file__).with_name("Row2_Full_Manifest.json")
    issues = deep_scan_manifest(manifest_path)

    print("--- Deep Scan Results ---")
    if issues:
        for issue in issues:
            print(f"❌ {issue}")
        raise SystemExit(1)
    print("✅ No contradictions detected against checksum 260.")


if __name__ == "__main__":
    main()
