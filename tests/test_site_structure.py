#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Structural gate for the shipped docs site (RR-B-30).

Asserts the claims the site makes that must never silently drift:
the shared stylesheet, the licence-enquiry link, the footer REV against
RELEASE-INFO.txt, section anchors, and cross-page link resolution.
"""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = ["index.html", "tiers.html", "faq.html"]
LICENCE_ENQUIRY = "https://labs.jgsystemsconsulting.com/licensing.html"


def page(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


class TestSiteStructure(unittest.TestCase):
    def test_every_page_links_shared_stylesheet(self):
        for name in PAGES:
            self.assertIn('<link rel="stylesheet" href="site.css">', page(name), name)
            self.assertNotIn("<style>", page(name), f"{name} still has an inline style block")

    def test_every_page_links_licence_enquiry(self):
        for name in PAGES:
            self.assertIn(LICENCE_ENQUIRY, page(name), name)

    def test_footer_rev_matches_release_info(self):
        info = (ROOT / "RELEASE-INFO.txt").read_text(encoding="utf-8")
        version = re.search(r"(?m)^version=(\S+)", info).group(1)
        for name in PAGES:
            self.assertIn(f"REV {version}", page(name), name)

    def test_expected_section_anchors_exist(self):
        self.assertIn('id="install"', page("index.html"))
        self.assertIn('id="tiers"', page("tiers.html"))

    def test_relative_page_links_resolve(self):
        for name in PAGES:
            for target in re.findall(r'href="([a-z]+\.html)"', page(name)):
                self.assertTrue((DOCS / target).exists(), f"{name} -> {target}")


if __name__ == "__main__":
    unittest.main()
