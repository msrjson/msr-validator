#!/usr/bin/env python3
"""Fetch the schema from the immutable specification tag and verify its digest."""

from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

TAG = "v2.0.0"
URL = f"https://raw.githubusercontent.com/msrjson/specification/{TAG}/schemas/msr-2.0.json"
SHA256 = "9a991c88739d5ee46bc60e92cbdb44957683fd4113b2df1f1a9474866bed931c"
DESTINATION = Path(__file__).parents[1] / "src" / "msr_validator" / "schema" / "msr-2.0.json"


def main() -> None:
    payload = urllib.request.urlopen(URL, timeout=30).read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != SHA256:
        raise SystemExit(f"schema digest mismatch: expected {SHA256}, received {digest}")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(payload)


if __name__ == "__main__":
    main()
