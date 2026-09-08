<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
-->

# Release gates: jgs-magic-sysmlv1-pro v0.1.0

Ledger of the checks that verify the v0.1.0 release, in the CHECK / EXPECT /
EVIDENCE form. Each CHECK is rerunnable from the repo root in Git Bash; the
EVIDENCE line records the passing run (date, key output, reference). Re-run
the full ledger after any change to the JAR, the docs site, or the release
artifacts, and update the EVIDENCE lines to match.

Release under verification: version 0.1.0, tag `v0.1.0`
(git tag on `main`; JAR digest in G4). Ledger last run: 2026-09-09.

- [x] G1: release gate passes (required files, forbidden paths/content,
      headers, em-dash and price scans, JAR digest)
  CHECK: python scripts/check_release.py
  EXPECT: RELEASE GATE: PASS
  EVIDENCE: exit=0, "RELEASE GATE: PASS", run 2026-09-09 at commit e7ff70e

- [x] G2: structural site tests pass (shared stylesheet, licence-enquiry
      link, footer REV vs RELEASE-INFO, anchors, cross-page links)
  CHECK: python -m unittest discover -s tests -q
  EXPECT: OK
  EVIDENCE: exit=0, "Ran 5 tests ... OK", run 2026-09-09; also green as the
  "Site structure tests" step in CI run 34291202130

- [x] G3: version is single-sourced (RELEASE-INFO == CHANGELOG top ==
      CITATION.cff == intended tag)
  CHECK: python -c "import re; i=open('RELEASE-INFO.txt').read();
        v=re.search(r'(?m)^version=(\S+)',i).group(1);
        t=re.search(r'(?m)^Tag: v(\S+)',i).group(1);
        c=re.search(r'(?m)^version: .([^.]+).$',open('CITATION.cff').read()).group(1);
        g=[l for l in open('CHANGELOG.md') if l.startswith('## [')][0].split('[')[1].split(']')[0];
        print(v,'v'+t,c,g); assert v==t==c==g"
  EXPECT: 0.1.0 v0.1.0 0.1.0 0.1.0, no AssertionError
  EVIDENCE: run 2026-09-09, printed "version=0.1.0 changelog_top=0.1.0
  citation=0.1.0 tag=v0.1.0 OK"; enforced in CI as the "Version
  single-source consistency" step of run 34291202130

- [x] G4: shipped JAR digest matches RELEASE-INFO.txt
  CHECK: sha256sum jgs-sysmlv1-pro.jar
  EXPECT: c56cec3a5b2d89142a9d1fe7130f5911d5cce49220bf7363fd3cfc29eaadcb7a
  EVIDENCE: run 2026-09-09, digest equals the jar_sha256 recorded in
  RELEASE-INFO.txt (also asserted inside the G1 gate)

- [x] G5: release-repo-standard audit is clean (25 machine checks incl.
      licence, headers, commit identity, BOM, machine-local paths)
  CHECK: python ~/.zcode/skills/release-repo-standard/tools/audit.py --repo . --profile base
  EXPECT: 0 FAIL, 0 WARN, 25 PASS
  EVIDENCE: run 2026-09-09 at commit e7ff70e: "0 FAIL, 0 WARN, 25 PASS"

- [x] G6: GitHub Release v0.1.0 is published and its notes carry the
      licence-enquiry URL
  CHECK: gh release view v0.1.0 --json body --jq .body | grep -c "labs.jgsystemsconsulting.com/licensing"
  EXPECT: 1
  EVIDENCE: run 2026-09-09, count=1 (footer appended to the original notes
  on 2026-09-08)

- [x] G7: live site serves, shares the stylesheet, and links the
      licence-enquiry page
  CHECK: curl -fsSL -o /dev/null -w "%{http_code}\n" https://jgsystemsconsulting.github.io/jgs-magic-sysmlv1-pro/ https://jgsystemsconsulting.github.io/jgs-magic-sysmlv1-pro/site.css https://labs.jgsystemsconsulting.com/licensing.html
  EXPECT: 200 three times
  EVIDENCE: run 2026-09-09 after the Pages build for e7ff70e: site 200,
  site.css 200 (first deploy of the shared stylesheet), licensing 200

- [x] G8: every external link on the customer surface resolves
      (README + shipped pages; JSON-LD context URLs excluded)
  CHECK: for u in $(grep -ohE "https?://[^\"<> ]+" README.md docs/*.html | tr -d '""' | sort -u | grep -v schema.org); do curl -fsSL -o /dev/null -w "%{http_code} $u\n" "$u"; done
  EXPECT: 200 on every line, no BROKEN output
  EVIDENCE: run 2026-09-09, 12/12 URLs 200 after fixing the JSON-LD
  author/publisher url (bare org Pages root 404ed; now labs site)

- [x] G9: every shipped page renders clean at desktop and mobile widths
  CHECK: python scripts/render_check.py
  EXPECT: RENDER CHECK: PASS
  EVIDENCE: run 2026-09-09 on the site.css build: overflow_x=0px for all
  three pages at 1280px and 390px; screenshots under .playwright-mcp/
  (gitignored), spot-checked for masthead/nav/H1 left edge and single-line
  desktop nav
