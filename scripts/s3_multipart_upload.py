#!/usr/bin/env python3
"""Resumable, KMS-encrypted multipart upload with SHA256 metadata."""

import argparse
import hashlib
import json
from pathlib import Path

import boto3

PART_SIZE = 50 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_state(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to local artifact")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True, help="S3 object key")
    parser.add_argument("--kms-key-id", required=True)
    parser.add_argument("--state", default="state.json")
    args = parser.parse_args()

    src = Path(args.file)
    state_file = Path(args.state)
    s3 = boto3.client("s3")

    file_hash = sha256_file(src)
    size = src.stat().st_size

    state = load_state(state_file)
    upload_id = state.get("upload_id")
    parts = state.get("parts", [])

    if not upload_id:
        response = s3.create_multipart_upload(
            Bucket=args.bucket,
            Key=args.key,
            ServerSideEncryption="aws:kms",
            SSEKMSKeyId=args.kms_key_id,
            Metadata={"sha256": file_hash},
        )
        upload_id = response["UploadId"]
        state = {
            "upload_id": upload_id,
            "parts": [],
            "bucket": args.bucket,
            "key": args.key,
            "file": str(src),
        }
        save_state(state_file, state)

    uploaded = {p["PartNumber"]: p["ETag"] for p in parts}
    next_part = 1

    with src.open("rb") as f:
        while True:
            chunk = f.read(PART_SIZE)
            if not chunk:
                break
            if next_part in uploaded:
                next_part += 1
                continue

            res = s3.upload_part(
                Bucket=args.bucket,
                Key=args.key,
                UploadId=upload_id,
                PartNumber=next_part,
                Body=chunk,
            )
            state["parts"].append({"PartNumber": next_part, "ETag": res["ETag"]})
            save_state(state_file, state)
            next_part += 1

    s3.complete_multipart_upload(
        Bucket=args.bucket,
        Key=args.key,
        UploadId=upload_id,
        MultipartUpload={"Parts": sorted(state["parts"], key=lambda p: p["PartNumber"])}
    )

    head = s3.head_object(Bucket=args.bucket, Key=args.key)
    remote_hash = head.get("Metadata", {}).get("sha256")
    if remote_hash != file_hash:
        raise RuntimeError(f"Hash mismatch: local={file_hash} remote={remote_hash}")

    if state_file.exists():
        state_file.unlink()

    print(f"Upload completed: s3://{args.bucket}/{args.key}")
    print(f"sha256={file_hash}")


if __name__ == "__main__":
    main()
