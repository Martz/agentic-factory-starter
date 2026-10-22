---
description: |
  Factory improvement loop (learn). Weekly, an agent reads recent factory pull requests, their reviews and CI
  results, finds mistakes that keep coming back, and proposes AGENTS.md rules in one issue. A human decides which
  rules to adopt.

on:
  schedule: weekly
  workflow_dispatch:

permissions:
  contents: read
  issues: read
  pull-requests: read
  actions: read

tools:
  github:
    toolsets: [pull_requests, issues, repos, actions]

safe-outputs:
  create-issue:
    title-prefix: "[factory] learn: "
    labels: [factory-learn]
    max: 1

timeout-minutes: 15
---

# Learn station

You run the improvement loop for the software factory in ${{ github.repository }}.

1. Look at pull requests labelled `factory` from the last 30 days: their review comments (from the review station
   and from humans), requested changes, CI failures, and whether they were merged or closed.
2. Find problems that happened more than once, or that a human had to fix by hand.
3. Read `AGENTS.md`. For each repeated problem not already covered, draft one short, testable rule.
4. If you found at least one, open one issue titled with the main theme. List up to 5 proposed rules, each with
   the exact text to add to AGENTS.md and links to the PRs it came from. Suggest a CI check when a rule could be
   enforced by code instead.
5. If there is nothing worth proposing, do not open an issue.

A human decides which rules go into AGENTS.md. Do not propose changes to anything else.
