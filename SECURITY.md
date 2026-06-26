<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
-->

# Security Policy

## Reporting a vulnerability

Report security issues through GitHub, not by email:

- **Sensitive / exploitable issues** — open a **private security advisory**
  (the repository's **Security → Advisories → Report a vulnerability**). This
  keeps the report confidential until a fix is available.
- **Non-sensitive hardening suggestions** — open a pull request with the fix,
  or a regular issue.

Please do not disclose a vulnerability publicly until it has been addressed.

## Scope

This repository distributes a single compiled artifact — the pro-extension
plugin JAR (`jgs-sysmlv1-pro.jar`). Relevant reports include tampering with the
distributed JAR, integrity of the published SHA-256 digest in `RELEASE-INFO.txt`,
or unsafe behaviour when the JAR is loaded by the free base plugin.

## Response

We aim to acknowledge a valid report within **5 working days** and to agree a
remediation timeline with the reporter. Fixes ship as a new tagged release with
an updated `RELEASE-INFO.txt` digest and a `CHANGELOG.md` entry.
