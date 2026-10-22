# agentic-factory-starter

A basic **software factory built from [GitHub Agentic Workflows](https://github.github.com/gh-aw/)**. Label an issue and get a spec. Approve it and get a tested pull request. An independent agent reviews it, and you merge.

There's nothing to host: it runs in GitHub Actions on your Copilot subscription. Each station is a Markdown file of plain-English instructions.

```
 issue ─◆ label factory ─▶ SPEC ─▶ spec comment ─◆ label build ─▶ BUILD ─▶ draft PR ─▶ CI gates + REVIEW ─◆ you merge
 (you)    (you)            agent                    (you approve)   agent               code     2nd model    (you)

 weekly: LEARN reads the factory's PRs and reviews, and proposes AGENTS.md rules in an issue. You decide.
```

> Companion to the talk *Software Factories: from driving an agent to designing the line*. Want to read and own the orchestrator itself? See [factory-starter](https://github.com/Martz/factory-starter), the same line as about 800 lines of Python that you run anywhere.

## Set up in 5 minutes

You need a GitHub account with Copilot, and the [GitHub CLI](https://cli.github.com).

1. **Use this template** (the green button above) to create your own repository, then clone it.
2. Run **`./setup.sh`**. It installs the `gh aw` extension, creates the labels, lets Actions open pull requests, and stores your Copilot token. It links to a pre-filled token page, so you only click *Generate* and paste.
3. Open an issue with the **Factory ticket** template. [`examples/first-ticket.md`](examples/first-ticket.md) is a good first one: *Split the bill evenly*.
4. Add the label **`factory`**. A spec comment with testable acceptance criteria appears in a couple of minutes. Read it.
5. Happy with it? Add the label **`build`**. A draft pull request appears, with an evidence table that maps each criterion to the test that proves it.

Then CI runs the gates and the review station posts an independent review. This happens automatically if you set the optional `GH_AW_CI_TRIGGER_TOKEN` during setup; otherwise click **Ready for review** on the draft PR. Read the evidence and the review, then merge. Or don't.

## The stations

| Station | File | Trigger | The agent may | It writes only through |
|---|---|---|---|---|
| Spec | `factory-spec.md` | you add `factory` | read the issue and code | one comment, plus `spec-ready` or `needs-info` |
| ◆ Approve | n/a | **you** add `build` | n/a | n/a |
| Build | `factory-build.md` | `build` label | edit and run tests in its sandbox | one **draft** PR |
| Gates | `ci.yml` | the PR | n/a (plain code) | test · compile · `tests_kept` (no test may disappear) |
| Review | `factory-review.md` | the PR (label `factory`) | read and run tests, using **a different model family** from the builder | inline comments and one review: comment or request changes, never approve |
| ◆ Merge | n/a | **you** | n/a | n/a |
| Learn | `factory-learn.md` | weekly, or manually | read PRs, reviews and CI | one issue proposing `AGENTS.md` rules |

The builder uses a Claude Sonnet model and the reviewer a GPT-5 model, both through your Copilot subscription. They are set as `model: sonnet` and `model: gpt-5` (gh-aw aliases), so the review comes from another vendor's model with a fresh context. Change them in each file's `engine:` block.

## Agents propose, code disposes: how gh-aw keeps it safe

- **The agent job is read-only.** It runs in a sandbox behind a network firewall, with no write permissions.
- **Writes are *safe outputs*.** The agent can only *ask* for the outputs a workflow allows (a comment, labels, one PR), up to the limits you set. A separate job with write permission validates and applies them, after an automatic threat-detection job has scanned them for prompt injection, leaked secrets and malicious code. The build agent's commits arrive as a git bundle, and that separate job opens the PR. Drafts are enforced by policy.
- **Protected files.** A PR from an agent can't change dependency manifests or agent instruction files such as `AGENTS.md`. That's why `learn` *proposes* rules in an issue and a human edits the guide.
- **Untrusted input is fenced.** Only people with write access can trigger the stations, because labels are the trigger. In public repositories, content from untrusted authors is filtered out of the agent's context (`min-integrity: approved`).
- **Nothing merges itself.** The review can't approve, and the factory has no merge permission. You merge.

## Change it

The `.md` files are the source; the `.lock.yml` files are generated GitHub Actions. After editing a station, run `gh aw compile` and commit both. Ideas:

- **Your own repo:** copy `.github/workflows/factory-*.md`, `ci.yml`, `.github/scripts/` and `AGENTS.md`. Put your real test and lint commands in `ci.yml` and in the build station's step 4, and rewrite `AGENTS.md` for your codebase.
- **Organisation billing:** add `copilot-requests: write` under `permissions:`. Then no personal token is needed.
- **Other engines:** `engine: claude` (with `ANTHROPIC_API_KEY`) or `engine: codex` (with `OPENAI_API_KEY`).
- **More stations:** browse [githubnext/agentics](https://github.com/githubnext/agentics), e.g. `gh aw add-wizard githubnext/agentics/ci-doctor`.
- **Other ingress:** `repository_dispatch` lets Jira, PagerDuty or any HTTP caller start a workflow ([triggers](https://github.github.com/gh-aw/reference/triggers/)).
- **Watch it:** `gh aw logs`, `gh aw audit <run>` and `gh aw health` show what each station did and what it cost.

## Cost and limits

Each station run is one Copilot agent session, billed as premium requests on the token's account. GitHub Agentic Workflows is in **public preview**, so details change; `gh aw upgrade` updates the workflows. Start on a low-risk repository and keep the human merge.

## Licence

MIT. See [LICENSE](LICENSE).
