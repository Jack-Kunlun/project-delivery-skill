# Project record

Updated: 2026-11-02 (Asia/Shanghai).

## Purpose and authoritative sources

Publish and maintain the reusable `project-delivery` skill for established projects, first-time recordkeeping, and gradual legacy adoption. Each adopting project owns its requirements, tasks, decisions, and evidence.

This file is this repository's task, decision, event, and evidence record. The maintained package is `skills/project-delivery/`; personal installations are copies, not another authoring source. `README.md` is the English public entry point; `README.zh-CN.md` is its Chinese counterpart.

## Current work

| ID | Work | Status | Scope and acceptance |
| --- | --- | --- | --- |
| PD-001 | Publish the standalone skill repository | Accepted | English skill instructions, references, UI metadata and primary README; Chinese README; MIT license; semantic/package/link/install checks; personal-account public repository and verified Git push. |
| PD-002 | Persist delivery rules during initialization | Accepted | Default project-local agent instructions, authoritative record pointers, resumable task handling, idempotent initialization, a fresh follow-up exercise, local installation sync and GitHub push. |

Owner/acceptance: current maintainer acting through the coding assistant. Internal verification is separate from user acceptance. No delivery date is inferred, and the number of packaging tasks is not a product-completion percentage.

## Decisions

- The owner requested a standalone project, English primary README, Chinese documentation, and publication through their personal GitHub account.
- The owner explicitly selected public visibility and MIT licensing. Target: `Jack-Kunlun/project-delivery-skill`.
- The initial scope retained Chinese instructions. The owner subsequently required English skill instructions, superseding that language decision. Translate the complete instruction package and display metadata while preserving behavior; keep the Chinese README.
- This repository is the maintained distribution source. The maintainer's local installed copy is synchronized to the same English package.

## Events

All dates below are record dates in Asia/Shanghai.

- 2026-11-02: PD-001 started before packaging. The personal GitHub account and repository-name availability were verified. Unrelated project changes stayed outside this repository.
- 2026-11-02: Initial packaging checks passed for 13 intended files and the unchanged seven-file Chinese skill baseline. The English and Chinese README installation commands were exercised in an isolated profile.
- 2026-11-02: Commit `98b613c` was pushed to the personal public repository. GitHub reported owner type `User`, visibility `public`, default branch `main`, and license `MIT`.
- 2026-11-02: The owner clarified that skill instructions must be English. PD-001 stayed open for the English revision and a follow-up push; the initial Chinese distribution remains in Git history.
- 2026-11-02: All seven instruction/metadata files were translated. An implementation agent translated the five references; the primary agent translated the entry point and metadata and reviewed every translated reference. The identifier-scheme wording and visual-review wording were clarified without changing the intended workflow.
- 2026-11-02: Fresh English-package checks passed. The package is ready for the authorized follow-up publication.

## Verification

Risk/budget: S3 / medium, a bounded documentation-based skill publication. No product tests, production deployment, or new CI are part of this work. Expand only for a concrete failure or newly discovered impact.

English package checks on 2026-11-02:

- Exactly 13 intended repository files, including seven skill files; no machine-specific source-project paths or credentials in the candidate.
- Skill-creator format validation and UI metadata checks passed; all instruction/reference/metadata content is English.
- The primary agent compared translated meaning against the Chinese baseline. Existing-ledger reuse, first-time recordkeeping, legacy limitations, authorization, evidence boundaries, lifecycle gates, coverage definitions, and recurrence follow-up were retained. Heading hierarchy, table-row counts, and relative references were also checked; structural checks alone are not semantic proof.
- All 23 repository-relative documentation links resolve. English and Chinese installation commands match.
- The documented manual install was run with only its destination expansion replaced by an isolated temporary profile. A fresh copy matched all seven English skill files. An existing directory and a dangling symlink were refused without changes. HOME and CODEX_HOME were not modified.
- The translator's first structural checker used incorrect hardcoded counts; it was corrected to compare source and destination. No failed checker result was presented as a pass.

The original Chinese skill was exercised in two isolated sample projects: an established ledger and a legacy/no-ledger project without a runnable environment. First-pass traceability and recurrence-follow-up omissions were corrected and rechecked. These remain historical exercises, not newly executed English-language behavioral tests. No automatic skill-picker UI or live product verification is claimed.

## Publication acceptance

- English revision `f059e871e6b021e51ed3452e7bf924bcdd2c73e2` was pushed and independently read back through the GitHub API. Remote SHA matched local HEAD, GitHub attributed the commit to `Jack-Kunlun`, and the repository reported public visibility, personal owner type `User`, default branch `main`, and MIT licensing.
- The worktree was clean at that verification point. All seven personally installed skill files matched the repository package byte for byte.
- 2026-11-02: PD-001 was internally accepted after those checks. This closeout changes only the maintenance record and clarifies evidence wording in the two READMEs; the verified skill package and installation commands remain unchanged. The final remote head is available in GitHub history rather than being embedded recursively in its own commit.

## Remaining work

None for the requested repository creation, English instruction package, bilingual README, MIT licensing, and GitHub push. Future behavior changes should get their own scoped record and applicable checks. Installation alone does not automatically adopt other projects or create continuous monitoring.

## PD-002: Initialization that persists into later work

- Source: the owner required initialization to set up ongoing workflow use automatically, without listing those steps in the prompt.
- Scope: strengthen the English skill's initialization contract and project-local instruction integration; update bilingual usage documentation; preserve existing project rules/ledgers; synchronize the installed package and publish the change. No global instruction changes, background jobs, or CI hooks.
- Acceptance: initialization creates or updates the effective project instruction entry point, preserves existing rules and record authority, resolves actual paths, avoids duplicate integration on repeated setup, and hands a plain follow-up request to a fresh agent context that records and closes its work using the project rules.
- Budget: S3 / medium. Skill/links/package checks plus one bounded initialization-and-continuation exercise with a repeat-initialization check. At most one evidence-based correction round before reassessing. No full product suite or production operation.
- Event, 2026-11-02: PD-002 registered and started before implementation. The existing skill permits an entry point in README or AGENTS; it does not require a persistent project instruction block or a fresh-context continuation check. This is the specific gap to close.
- Changes: initialization now integrates the effective project-local agent instruction file by default, with actual record pointers and start/update/accept/closeout rules. Existing instructions and authority remain intact; a single managed integration is reused on repeat setup. Previously adopted projects can repair a missing integration on the next authorized skill use. Implicit invocation is explicitly enabled. English instructions and both READMEs describe the behavior and its limits.
- Static verification: the skill-creator validator, UI metadata, 13-file package/7-file skill inventory, English instruction content, 24 relative links, and Markdown table checks passed. Installation commands are unchanged; their prior bounded installation evidence is retained.
- Initialization exercise: an isolated five-file project had existing AGENTS rules, a W ledger, and a working feature task. Initialization preserved the original rules and business files, created one managed integration, reused the ledger, and recorded W-02 while keeping its continuation check pending. Repeating the request reused the same integration and two work items and appended a repeat event.
- Fresh-context exercise: a new isolated context received project instructions and the ordinary request “Make summarize([]) return 'No items'. Keep the existing formatting for nonempty inputs.” No user workflow reminder or earlier conversation was supplied. The executor reused W-01, recorded scope/acceptance, changed the function, added a regression case, ran `python3 -m unittest -v` (2 tests passed), updated the overview, and left results and a resumption point.
- Disclosed deviations and bounded recheck: the first executor used read-only `git status` despite the exercise's no-Git constraint and recorded that deviation; its unavailable `python` command was followed by a successful `python3` run. One fresh recheck under an explicit tool allowlist again completed the same two tests and task trace without a reported Git command. That executor omitted an earlier historical note while rewriting W-01; the primary reviewer restored it from the initialization snapshot and recorded the intervention. These results demonstrate continuation with review, not perfect unaided compliance.
- Primary verification: inspected both actual source/test/ledger outputs, confirmed their implementations match, checked original instruction preservation, one integration/two work items after repeat setup, concrete links and resumption records. Reused the executors' unchanged two-test results rather than rerunning them. Temporary exercises and detailed hashes stay local.
- Discovery boundary: generated project instructions and the skill catalog/path were explicitly supplied or read in fresh isolated contexts. This verifies instruction-driven continuation, not desktop/CLI auto-discovery or a guarantee that every future turn loads the skill. No global instructions, background jobs, real product code, or CI were changed.
- Event, 2026-11-02: PD-002 moved to Awaiting publication after the bounded initialization, repeat, continuation, recheck, primary review, and static validation. The review interventions and untested host boundary remain visible.
- Publication evidence, 2026-11-02: revision `c841b29fe877ca3127406ea5cb833e48d9dc5953` was pushed to `main`; the GitHub API returned the identical SHA and author `Jack-Kunlun`. All seven installed skill files matched the repository package; the worktree was clean. PD-002 is internally accepted with the disclosed exercise deviations and host-discovery boundary retained.
- Remaining: none for this scoped default-initialization update. This closeout changes only the project record; it does not expand verification claims. PD-001 remains accepted as historical publication work.
