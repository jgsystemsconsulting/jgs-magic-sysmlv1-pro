#!/usr/bin/env bash
# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
#
# Idempotent publish-time platform configuration for jgs-magic-sysmlv1-pro.
# Run ONCE after making the repo PUBLIC (Pages, branch protection, and Pro-only
# features require a public repo). Re-running is safe.
#
# Configures: About panel (RR-B-21), GitHub Pages from main:/docs (RR-B-20),
# and default-branch protection (RR-B-23). Requires: gh (authenticated).
set -euo pipefail

OWNER=jgsystemsconsulting
REPO=jgs-magic-sysmlv1-pro
SLUG="$OWNER/$REPO"
PAGES_URL="https://jgsystemsconsulting.github.io/$REPO/"

echo "==> About panel (description, homepage, topics)"
gh repo edit "$SLUG" \
  --description "Licensed pro-extension JAR for the JGS SysML v1 MCP Bridge. Unlocks write-tier and pro model tools for AI agents in CATIA Magic." \
  --homepage "$PAGES_URL"
gh api -X PUT "repos/$SLUG/topics" \
  -H "Accept: application/vnd.github+json" \
  -f names[]=mcp -f names[]=sysml -f names[]=mbse \
  -f names[]=catia-magic -f names[]=cameo-systems-modeler \
  -f names[]=model-context-protocol -f names[]=claude-code -f names[]=plugin

echo "==> GitHub Pages (main:/docs)"
gh api -X POST "repos/$SLUG/pages" \
  -H "Accept: application/vnd.github+json" \
  -f "source[branch]=main" -f "source[path]=/docs" 2>/dev/null \
  || gh api -X PUT "repos/$SLUG/pages" \
       -H "Accept: application/vnd.github+json" \
       -f "source[branch]=main" -f "source[path]=/docs"

echo "==> Default-branch protection (solo-maintainer profile)"
# No CI job in this artifact-only repo, so required_status_checks is null.
gh api -X PUT "repos/$SLUG/branches/main/protection" \
  -H "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

echo "==> Done. Verify:"
echo "    gh repo view $SLUG --json description,homepageUrl,repositoryTopics"
echo "    gh api repos/$SLUG/pages --jq .html_url"
echo "    curl -fsSL -o /dev/null -w '%{http_code}\n' $PAGES_URL"
