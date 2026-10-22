#!/usr/bin/env bash
# One-time setup for your copy of this repository: the factory's labels, one Actions setting, and the
# Copilot token. Needs the GitHub CLI (https://cli.github.com), logged in. Run it from your clone.
set -euo pipefail
command -v gh >/dev/null || { echo "Install the GitHub CLI first: https://cli.github.com"; exit 1; }
gh aw version >/dev/null 2>&1 || gh extension install github/gh-aw
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Setting up the factory in $repo"

label() { gh label create "$1" --color "$2" --description "$3" --repo "$repo" --force >/dev/null && echo "  ✓ label $1"; }
label factory       FF8A1F "Factory: write a spec for this issue (maintainers add this)"
label build         3CC8D3 "Factory: spec approved, build it (maintainers add this)"
label spec-ready    46C46A "Factory: spec written, waiting for approval"
label needs-info    D27CFF "Factory: the spec has open questions"
label factory-learn 9AA4B5 "Factory: proposed AGENTS.md rules"

# Safe outputs open pull requests with the workflow token, which needs this repository setting.
gh api -X PUT "repos/$repo/actions/permissions/workflow" -f default_workflow_permissions=read \
  -F can_approve_pull_request_reviews=true >/dev/null && echo "  ✓ Actions may open pull requests"

cat <<'TXT'

1/2  The Copilot engine needs a fine-grained token: Account permissions → Copilot Requests: Read.
     Create it here (the link pre-fills it), then paste it below. Input is hidden.
     https://github.com/settings/personal-access-tokens/new?name=COPILOT_GITHUB_TOKEN&description=GitHub+Agentic+Workflows+-+Copilot+engine+authentication&user_copilot_requests=read
     (In an organisation with Copilot billing you can skip this: add `copilot-requests: write` under
      `permissions:` in each .github/workflows/factory-*.md and run `gh aw compile`.)
TXT
gh aw secrets set COPILOT_GITHUB_TOKEN --repo "$repo"

cat <<'TXT'

2/2  Optional, recommended: CI and the review station on the factory's own pull requests.
     PRs opened by the workflow token don't start other workflows, so without this token you click
     "Ready for review" on the draft PR to start them. Fine-grained token for this repository only,
     Repository permissions → Contents: Read and write:
     https://github.com/settings/personal-access-tokens/new?name=GH_AW_CI_TRIGGER_TOKEN&description=GitHub+Agentic+Workflows+-+CI+trigger&contents=write
TXT
read -r -p "     Set it now? [y/N] " yn
if [[ "$yn" =~ ^[Yy] ]]; then gh aw secrets set GH_AW_CI_TRIGGER_TOKEN --repo "$repo"; fi

echo
echo "Done. Open an issue with the 'Factory ticket' template (examples/first-ticket.md is a good first one),"
echo "then add the 'factory' label and watch the Actions tab."
