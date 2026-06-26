#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Release gate for jgs-magic-sysmlv1-pro.

Runs four check classes and exits non-zero on any failure (RR-B-15):
  1. required files present
  2. forbidden paths absent
  3. forbidden content absent (leak sentinels)
  4. per-file headers present on first-party shippable docs (RR-B-03)
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "LICENSE", "COPYRIGHT", "NOTICE", "README.md", "CHANGELOG.md",
    "SECURITY.md", "RELEASE-INFO.txt", ".gitignore",
    "jgs-sysmlv1-pro.jar", "docs/index.html", "docs/.nojekyll",
    "docs/tiers.html", "docs/faq.html", "docs/assets/og.png",
]

# Human-facing surface that MUST contain no em dash (RR-B-24 / RR-B-28).
EM_DASH_GLOBS = [
    "README.md", "CHANGELOG.md", "SECURITY.md",
    "docs/index.html", "docs/tiers.html", "docs/faq.html",
]

# Shipped HTML pages MUST publish no price/dollar amount (RR-B-19 / RR-B-30).
PRICE_RE = re.compile(r"\$[0-9]|/mo\b|per month|pricing", re.IGNORECASE)
PRICE_GLOBS = ["docs/index.html", "docs/tiers.html", "docs/faq.html"]

# Paths that must never ship.
FORBIDDEN_PATHS = ["server/", "keygen", "private", ".env"]

# Content sentinels that must not appear in shipped text files.
FORBIDDEN_CONTENT = [
    "CONFIDENTIAL — Not for external distribution",
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
]

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd."
# First-party docs that must carry the header. (Vendored/governance text exempt.)
HEADER_GLOBS = ["README.md", "CHANGELOG.md", "SECURITY.md"]

TEXT_SUFFIXES = {".md", ".txt", ".html", ".py", ".sh", ".json", ".yml", ".yaml"}


def fail(msg: str, bucket: list[str]) -> None:
    bucket.append(msg)


def main() -> int:
    errors: list[str] = []

    # 1. required files
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(f"required file missing: {rel}", errors)

    # 2. forbidden paths
    for pat in FORBIDDEN_PATHS:
        for hit in ROOT.rglob("*"):
            if pat.rstrip("/") in hit.relative_to(ROOT).as_posix() and ".git/" not in hit.as_posix():
                fail(f"forbidden path present: {hit.relative_to(ROOT)} (matched '{pat}')", errors)
                break

    # 3. forbidden content (text files only)
    self_path = Path(__file__).resolve()
    for path in ROOT.rglob("*"):
        if path.is_dir() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git/" in path.as_posix():
            continue
        if path.resolve() == self_path:  # the gate defines the sentinels it scans for
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for sentinel in FORBIDDEN_CONTENT:
            if sentinel in text:
                fail(f"forbidden content '{sentinel}' in {path.relative_to(ROOT)}", errors)

    # 4. headers present on first-party docs
    for rel in HEADER_GLOBS:
        p = ROOT / rel
        if p.exists() and HEADER_SENTINEL not in p.read_text(encoding="utf-8", errors="ignore"):
            fail(f"missing per-file header in {rel}", errors)

    # 5. no em dash in human-facing surface (RR-B-24 / RR-B-28)
    for rel in EM_DASH_GLOBS:
        p = ROOT / rel
        if p.exists() and "—" in p.read_text(encoding="utf-8", errors="ignore"):
            fail(f"em dash present in human-facing file: {rel}", errors)

    # 6. no price/dollar amount in shipped HTML pages (RR-B-19 / RR-B-30)
    for rel in PRICE_GLOBS:
        p = ROOT / rel
        if p.exists() and PRICE_RE.search(p.read_text(encoding="utf-8", errors="ignore")):
            fail(f"price/dollar amount in shipped page: {rel}", errors)

    # bonus: JAR digest matches RELEASE-INFO.txt
    info = (ROOT / "RELEASE-INFO.txt").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"jar_sha256=([0-9a-f]{64})", info)
    jar = ROOT / "jgs-sysmlv1-pro.jar"
    if m and jar.exists():
        digest = hashlib.sha256(jar.read_bytes()).hexdigest()
        if digest != m.group(1):
            fail(f"JAR sha256 mismatch: file={digest} info={m.group(1)}", errors)

    if errors:
        print("RELEASE GATE: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("RELEASE GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
