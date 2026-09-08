#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Render every shipped docs page at two breakpoints and fail on horizontal overflow.

Dev tool for the GATES.md render gate (RR-B-24): needs the playwright package
(`pip install playwright` plus `playwright install chromium`). Screenshots land
in .playwright-mcp/ (gitignored). Exit non-zero if any page overflows.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "tiers.html", "faq.html"]
VIEWPORTS = [(1280, 900, "desktop"), (390, 844, "mobile")]


def main() -> int:
    out = ROOT / ".playwright-mcp"
    out.mkdir(exist_ok=True)
    bad = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width, height, tag in VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": height})
            for name in PAGES:
                page.goto((ROOT / "docs" / name).as_uri())
                page.wait_for_load_state("networkidle")
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                page.screenshot(path=str(out / f"{name.rstrip('.html')}-{tag}.png"), full_page=True)
                print(f"{name} {tag} ({width}px): overflow_x={overflow}px")
                if overflow > 0:
                    bad.append(f"{name} {tag}")
            page.close()
        browser.close()
    if bad:
        print("RENDER CHECK: FAIL", ",".join(bad))
        return 1
    print("RENDER CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
