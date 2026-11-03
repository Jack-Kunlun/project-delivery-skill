# Project record

Updated: 2026-11-03 (Asia/Shanghai).

## Purpose and authoritative sources

Publish and maintain the reusable `project-delivery` skill for established projects, first-time recordkeeping, and gradual legacy adoption. Each adopting project owns its requirements, tasks, decisions, and evidence.

This file is this repository's task, decision, event, and evidence record. The maintained package is `skills/project-delivery/`; personal installations are copies, not another authoring source. `README.md` is the English public entry point; `README.zh-CN.md` is its Chinese counterpart.

## Current work

| ID | Work | Status | Scope and acceptance |
| --- | --- | --- | --- |
| PD-001 | Publish the standalone skill repository | Accepted | English skill instructions, references, UI metadata and primary README; Chinese README; MIT license; semantic/package/link/install checks; personal-account public repository and verified Git push. |
| PD-002 | Persist delivery rules during initialization | Accepted | Default project-local agent instructions, authoritative record pointers, resumable task handling, idempotent initialization, a fresh follow-up exercise, local installation sync and GitHub push. |
| PD-003 | Provide a complete Chinese documentation path | Accepted | Chinese skill guide and reference pages, localized project/license explanations, same-language navigation, unchanged English runtime package, link/translation checks, and GitHub push. |
| PD-004 | Require state-specific rendered UI acceptance | Awaiting publication | Bind design expectations to rendered state evidence, audit conditional adjacency and scoped consumers, persist the UI gate, verify with an isolated exercise, and synchronize/publish bilingual instructions. |

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

## PD-003: Language-consistent documentation navigation

- Source: the owner pointed out that the Chinese README's Skill instructions link opens English content, and requested corresponding Chinese child documents throughout Chinese documentation.
- Scope: add a Chinese reader-documentation tree, localize README navigation and corresponding reference links, and explain the English runtime source versus Chinese reading copies. Keep the executable/discoverable skill instructions and metadata in English. Project-record translation is a reading view, not a second status authority; the original MIT license remains authoritative.
- Acceptance: Chinese navigation stays in Chinese documents except explicitly labeled language switches or authoritative English source links; English navigation stays English; all local links resolve; translated content reflects current requirements including default initialization; no duplicate discoverable skill is created; the English runtime package remains byte-identical.
- Budget: S2 / low. Two direct checks: translation/navigation and unchanged-package verification, then diff/write/remote verification. No product or behavioral tests are needed for reader-documentation changes.
- Event, 2026-11-02: PD-003 registered before edits. The existing Chinese README links directly to the English SKILL.md and project record, and no Chinese reference-document tree exists.
- Changes: added a Chinese skill guide, five corresponding references, a synchronized project-record reading view, and a license explanation. Both READMEs now have corresponding same-language documentation navigation; explicitly labeled language/source switches remain available. Repository guidance requires maintaining translations alongside their English sources.
- Primary review: compared the guide and all five reference translations with their current English sources, including initialization persistence, legacy constraints, visual comparison, coverage definitions, handoffs, and recurrence follow-up. The Chinese project view preserves the task IDs, historical evidence, and single-authority boundary.
- Direct check: all 74 local Markdown links across 18 Markdown documents resolve, including 12 explicitly labeled language/source switches. Locale routing, table widths, fenced blocks, five reference structures, matching task states, and historical commit identifiers passed. The candidate contains 21 intended files; all seven runtime files and the personal installation are byte-identical to the pre-edit baseline. Both README installation snippets remain unchanged.
- Check correction: the first inventory check matched the lowercase reader filename as SKILL.md on the case-insensitive filesystem. Renamed the reader guide to guide.md; the repeated check passed with exactly one SKILL.md. The guide remains outside the installable skill tree. No failed result was counted as a pass.
- Verification boundary: these are reader-documentation, semantic, and navigation checks. No new product, UI, behavior, or host-discovery tests ran; runtime behavior is unchanged. Temporary validation artifacts remain local.
- Event, 2026-11-02: PD-003 moved to Awaiting publication after the scoped review and direct checks.
- Publication evidence, 2026-11-02: revision `2fea9362040c71907e5c251db34c15f682d4f271` was pushed to `main`; the GitHub API returned the identical SHA and author `Jack-Kunlun`. The named 12-file staged diff passed whitespace checks, and installed repository files matched the reviewed hashes. The worktree was clean after publication.
- Closure: PD-003 is internally accepted. This closeout synchronizes only the English authoritative record and its Chinese reading view; it does not change the verified guide, references, installation, or runtime package. Existing semantic/link/package evidence remains applicable.
- Remaining: none for the requested same-language documentation navigation. No new runtime behavior or UI-acceptance requirements were added.


## PD-004: State-specific rendered UI acceptance

- Source: the owner reported touching informational and conditional-notice panels in a project that had adopted this skill. The screenshot is a reported visual failure; no production access or business operation is authorized by that report.
- Findings: current rules mention spacing and rendered comparisons but do not require a compact expectation/result record for each selected UI state or explicitly persist that gate. Read-only project evidence distinguishes a previously checked page-level error gap from the conditional notices inside a card; source observations do not establish the live candidate identity. No private project paths, identifiers, or screenshot are included in this public record.
- Scope: strengthen the existing UI gate and initialization integration, preserve project-specific design values, synchronize Chinese reader docs and usage guidance, and update the existing personal installation. Product implementation, deployment, new CI, and unrelated projects are outside this task.
- Acceptance: derive affected conditional states and layout relationships; compare actual rendering against an identified design/token/current baseline; retain expected/observed/evidence and unresolved items; missing or failed required UI evidence cannot be labeled accepted. Repeated layout failures need a scoped prevention check and a separately pending effectiveness follow-up.
- Budget: S3 / medium. One documentation/package check and one isolated forward exercise covering conditional UI states at desktop/narrow widths plus an unavailable-evidence decision. At most one evidence-based correction/recheck; no product suite or production checks.
- Event, 2026-11-03: registered before changing the skill. Preserve existing task history and separate package acceptance from any adopting project's UI acceptance.
- Changes: the skill entry point routes UI work to a rendered acceptance gate. The existing delivery reference now requires affected state/relationship selection, a project-specific baseline, actual rendering and spacing measurements when relevant, per-case expected/observed evidence, and explicit failure/unverified dispositions. Added a compact comparison template and a concrete UI rule to persistent initialization. English and Chinese references/usage are synchronized; no default pixel value, CI system, or new runtime dependency was added.
- Escape analysis: a subsequent read-only project record corroborated that a previous page-level spacing check had not exercised the in-card conditional states, while its summary was broader than the actual evidence. Existing skill requirements were not fully executed. More specific skill instructions support enforcement by the executor; they do not prove automatic prevention or eliminate the executor's acceptance responsibility. Product repair remains in that project's own task and evidence.
- Static check: 21-file inventory, 84 local Markdown links and language routing, five reference structure pairs, aligned task states, unchanged discovery metadata and installation snippets passed. Skill-creator validation passed after using an already cached YAML module; the initial system-Python run lacked that module. No dependency was installed or modified.
- Forward exercise: an independent implementation agent received the candidate skill, a synthetic membership page, its approved local design, two task records, and a normal acceptance/fix request, without the suspected defect or proposed fix. Initial Chrome rendering exposed zero separation between visible conditional panels. A one-rule layout correction used the sample's own 18px token. The retained browser script passed 10 state/viewport cases (five selected states at 1280px and 390px), including no/single/coexisting notices and long content; it measured panel separation, hidden-panel space, footer spacing, and overflow. The evaluator directly reviewed the two long-notice after-images. An unrelated task with only a build-success note and no candidate remained unaccepted, with actionable missing evidence.
- Primary verification: inspected the actual HTML change, scoped assertion script, measurements, task records, narrow before/after images, and desktop after-image. The stored candidate hash matches the reviewed file. Reused the unchanged successful browser run instead of rerunning it. The exercise checks these specific decisions and layout relationships, not complete visual review of all ten cases.
- Boundaries: isolated file-based Chrome/Playwright evidence; no backend, user acceptance, release, host auto-discovery, or real-project behavior was tested. The skill was explicitly supplied to the evaluator. Revised initialization wording was checked as documentation; it was not a new host-discovery trial. Temporary fixtures/images/checks remain local, and later real-world prevention effectiveness remains unproven.
- Event, 2026-11-03: PD-004 moved to Awaiting publication after the scoped forward exercise and primary acceptance. No real project source or production state was changed in this task.
- Remaining: synchronize the reviewed package and personal installation, check the named staged diff, and publish under the existing personal-repository authorization.
