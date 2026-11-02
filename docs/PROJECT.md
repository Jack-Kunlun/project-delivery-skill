# Project record

Updated: 2026-11-02 (Asia/Shanghai).

## Purpose and scope

Publish and maintain the reusable `project-delivery` skill. The skill supports projects with established tracking, projects without a ledger, and gradual adoption of legacy projects. This repository owns the distributable skill; each adopting project owns its own requirements, tasks, decisions, and evidence.

## Authoritative records

This file is the repository's task, decision, and event record. `README.md` is the English public entry point; `README.zh-CN.md` is its Chinese counterpart. The maintained skill is under `skills/project-delivery/`. Personal installations are copies, not another authoring source.

## Current work

| ID | Work | Status | Scope and acceptance |
| --- | --- | --- | --- |
| PD-001 | Publish the initial standalone skill repository | Ready to publish | English README and Chinese counterpart, MIT license, unchanged validated skill, package/link/install checks, personal-account public repository and verified Git push. |

Owner/acceptance: current maintainer acting through the coding assistant; internal verification is separate from user acceptance. No delivery dates are inferred. This single packaging task is not a product-completion percentage.

## Decisions

- 2026-11-02: The owner requested a new standalone project, English primary README, Chinese documentation, and publication through their personal GitHub account.
- 2026-11-02: The owner explicitly selected a public repository and MIT licensing. Target: `Jack-Kunlun/project-delivery-skill`.
- Preserve the existing skill behavior and Chinese instructions for this publication. Explain the content language in both READMEs; translating the skill itself is outside this task.

## Events

- 2026-11-02: PD-001 started before packaging. Personal GitHub account and repository-name availability checked. Existing unrelated project changes remain outside this repository.

## Acceptance and verification plan

S3 / medium: one bounded packaging change with an authorized public GitHub write. Verify the skill files against the installed baseline, run the skill format check, check documentation and repository contents, exercise the documented installation in a temporary profile, and verify the final remote commit/visibility/license. No product tests, production deployment, or new CI are part of this task. Expand only if these checks expose a concrete issue.

## Evidence and remaining work

Packaging checks passed on 2026-11-02: 13 intended repository files; 7 skill files byte-identical to the validated baseline; skill-creator format check and UI metadata valid; 23 local documentation links resolve. English and Chinese shell instructions match. The documented manual copy was exercised with only its destination replaced by an isolated temporary profile: a fresh install matched all 7 files; an existing directory and a dangling symlink were refused without modification. No HOME or CODEX_HOME override was used. GitHub publication is the remaining step. Prior isolated skill exercises are historical evidence only: one established-project case and one legacy/no-ledger case; first-pass traceability and recurrence-follow-up omissions were corrected and rechecked. Do not claim comprehensive effectiveness across arbitrary projects.

- 2026-11-02: PD-001 moved to Ready to publish after the bounded package, link, and installation checks. No skill behavior changed, so prior isolated exercise evidence was not rerun or presented as fresh execution.
