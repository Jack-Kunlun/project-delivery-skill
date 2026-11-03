# Project Onboarding and Initial Recordkeeping

## Bounded inventory

Start with the entry points, directories, configuration, and current task, then read selectively to resolve key unknowns. Do not use “setting up a ledger” as a reason to audit every module. At minimum, answer:

- Which repository/workspace contains the actual implementation, and which branch, commit, or snapshot is it? Which items are prototypes, historical backups, or generated artifacts?
- What problem does the project solve, who uses it, and how is it currently run or delivered?
- What capabilities and modules actually exist, and which are only planned or described in prototypes or historical records?
- Where are the authoritative sources for requirements, design, interfaces, tasks, defects, releases, and lessons?
- What is the current goal and committed scope? What is already complete, and what known issues, dependencies, and maintenance limits exist?

Gather evidence from current code and configuration, existing documentation, and historical records. Use connected tools when they are available and can add evidence. If external sources cannot be read, record the gap; do not claim they are synchronized. Do not copy secrets, raw production data, or links containing credentials.

## Reuse, fill gaps, or establish records for the first time

**Existing project tracking:** Map where records live, preserving identifiers, statuses, and existing ownership. Do not copy external issue statuses into a second manual ledger; link the repository entry point to the authoritative system, and date any necessary snapshot while marking it as non-authoritative. Writing to an external system still requires authorization for this task. Inconsistent formatting is not a reason to rebuild the ledger.

Register the onboarding/documentation work itself in the authoritative ledger (it may be linked to an existing task), with a start record, outcome, and evidence; do not record only future product requirements. If there is no separate activity log, append key events to the task. Mark omitted historical events as backfilled; do not make it appear they were recorded at the time.

**No project ledger:** First create the smallest set of records that suits the project. By default, `docs/project/README.md` can be the entry point, or use an existing project directory. For a small project, a single `docs/PROJECT.md` can contain:

1. Project overview, scope baseline, main capabilities, and current operating limits.
2. Existing capabilities and historical deliveries: capability, source-code/documentation/runtime evidence, verification level, and known defects.
3. Work and issue ledger: current tasks, known feedback, and next steps; mark unknowns for verification.
4. Decisions and key events, acceptance evidence, and the next resumption point.

Record the current recordkeeping task before continuing the inventory. If there are no historical records yet, backfill only facts supported by evidence. Existing code does not prove that it was accepted, released, or managed under the new process at the time. Preserve user-reported issues that have not yet been reproduced; if ownership is unclear, mark it for verification rather than assigning a fix to the wrong project.

Split records further as they grow in practice. Optional files include `TASKS.md`, `CHANGES.md`, `ACTIVITY.md`, `ACCEPTANCE.md`, `MODULE-BOUNDARIES.md`, `LESSONS.md`, and `EVIDENCE.md`. Keep PRDs, design, tests, and delivered capabilities in the files the project already uses. Do not create empty shells. Fields may share a document, but their responsibilities and traceability must remain clear.

## Persistent instructions are part of initialization

When the user requests initialization, onboarding, or project takeover, do this integration by default within the authorized project scope. Do not ask them to restate “update AGENTS,” “record future tasks,” or “make it automatic.” A request for conceptual advice or only a package-scaffolding command does not authorize full onboarding.

1. **Find the effective project instruction file.** Read existing project `AGENTS.md`, applicable `AGENTS.override.md`, and relevant nested instructions. Use the root `AGENTS.md` when it is effective; create it if missing. If an override replaces it, integrate in the effective project file rather than writing instructions the host would ignore. Preserve higher-priority and more specific rules; do not remove an override or change global user instructions. Check the intended working directory, not just the repository root.
2. **Resolve the record map.** Find the actual project overview, authoritative task/issue source, decisions/events, acceptance rules, and lessons. Small projects may put them in sections of one document. Use working repository-relative links or the established external authority; do not invent files or create empty documents merely to satisfy a template.
3. **Merge a compact persistence block.** Keep existing instructions outside the integration unchanged. Use one `project-delivery:begin` / `project-delivery:end` block, or extend an equivalent existing integration. On repeat initialization, update that block and reuse the ledger/IDs instead of appending another block or starting a new ledger. Reconcile user edits; do not blindly replace the whole file. A README can link to the entry point but does not replace the effective agent instructions.
4. **Keep the lifecycle active.** The block requires later substantive tasks to read current records, register work before execution, track changes/issues and relevant lessons, apply appropriate acceptance checks, and leave results and a resumption point. Persist a UI-specific rule and the actual local design/acceptance pointers: for UI-affecting work, inspect conditional states and adjacent regions, compare rendered results with the current baseline, and keep UI acceptance open when required evidence is missing or fails. Do not substitute a generic “run checks” instruction for this rule. It should tell the agent to use `project-delivery` when available. If the skill is unavailable, the concrete local rules still apply; report the availability gap without inventing a successful invocation or automatically blocking unrelated safe work.
5. **Verify before claiming complete.** Follow the acceptance checks below and record actual results in the initialization task. If effective project instructions cannot be written within scope, complete authorized documentation work and record the remaining integration gap; do not mark persistent initialization complete. Existing authorization should not turn into repeated approval requests for routine steps.

Use the following as a compact example, adapting all record paths and responsibilities to the project. Replace every placeholder before writing; the generated instructions must be usable without the initialization chat or the author's machine paths.

```text
<!-- project-delivery:begin -->
## Project delivery workflow
For substantive project work, apply project-delivery without waiting for a
workflow reminder. Use the installed skill when available; otherwise follow
these project-local rules and report the missing-skill limitation.
- Entry point: {actual relative overview path}.
- Authoritative records: {actual task/issue, decision/event, acceptance,
  and lesson paths or sections; reuse established external authority}.
- Before execution, read the current task, recent decisions, and relevant
  lessons; associate or create the work item and define scope and acceptance.
- During work, record material changes, issues, blockers, and resumption points.
- Before handoff, run applicable checks; record actual evidence, unresolved
  gaps, task status, and the next step. Keep acceptance and release separate.
- For UI changes, read {actual design/acceptance path or section}; check affected
  conditional states and neighboring regions in the rendered UI against that
  baseline. Record expected/observed results and evidence; absent or failing
  required visual checks mean UI acceptance is still open.
- Preserve existing project rules and record authority. Continue existing
  work; do not reinitialize the project for every task or assume release rights.
<!-- project-delivery:end -->
```

Name actual ownership/receiving responsibilities, or mark them unassigned when unknown. One person may fill multiple roles; a fixed team or agent roster is not required. Pure explanations without a new decision, issue, scope change, or commitment do not need a fabricated work item.

Version repository documentation with its branch. A new worktree must contain the applicable instructions and records; hand off uncommitted content explicitly rather than claiming it is synchronized. Do not maintain mutable state through absolute paths into another worktree. For an external authority, preserve its permissions and project mapping.

## Executable acceptance during adoption

Follow [Automated acceptance](automated-acceptance.md) to install a project-owned runner, map the current task and applicable commands, and wire guarded completion plus historical audit into existing entry points. Inspect existing records first: reuse complete valid evidence; execute only missing or invalidated checks. Keep scope mapping explicit, and do not replay production operations or rerun unrelated suites merely to create new-format receipts. Existing records can be validated through a provenance-preserving adapter when all required bindings are available. Record unwired paths or unsupported external transitions as gaps; do not claim automated enforcement until a failing completion is actually blocked.

## Progress reporting

The overview should list product scope, milestones, target/date commitments, current acceptance evidence, blockers, next steps, and the update date. If no date is committed, say so; do not estimate duration from the number of tasks.

Prefer milestone reporting that says which outcomes have been accepted and which lack evidence. If a percentage is needed, define:

- **Denominator:** Delivery units and weights within the committed baseline. Exclude uncommitted ideas, duplicate defect reports, and administrative tasks alone.
- **Numerator:** The weights of delivery units accepted as complete under the agreed definition of done.
- **Source and date:** Link the tasks, evidence, and baseline. Preserve both the old and new measurement basis when scope changes; do not make progress look better by changing the denominator.

Do not describe task counts, lines of code, passing test counts, or document counts directly as the product completion rate.

## Onboarding acceptance

Check these observable outcomes, not just the presence of filenames:

- The effective project instructions contain one usable persistence integration; prior rules remain intact and the relevant override/directory scope has been checked.
- Its concrete record pointers resolve. Each status has one authority, overview and ledger agree, history/current state/goals are distinct, and current work and known issues have owners or handling destinations.
- Initialization itself has a traceable task and evidence. Repeated initialization reuses the integration and records without duplicating blocks, tasks, or status sources; a rerun may append a new event to the same work item.
- A fresh context receives the project instructions and a normal bounded follow-up request, **without** a user prompt naming this skill or asking for task bookkeeping. Verify the actual resulting task/issue record, relevant checks, result, and resumption point. Use an authorized isolated copy for an exercise instead of inventing live product work. Do not pass the earlier conversation or expected answer to the fresh agent.
- Separate what was validated: instruction content/links; a fresh agent consuming those instructions; and the actual host's automatic instruction/skill discovery. Manually supplying the generated instructions to an isolated agent can validate continuation behavior, but does not prove host auto-loading. If the environment cannot support the continuation check, mark it unverified and leave an actionable verification item rather than claiming it passed.

Initialization should not require the user to add these steps to each prompt. Its completion report identifies the effective instruction file, authoritative entry point, actual continuation evidence, and remaining limits. Documentation/continuation acceptance does not prove all product behavior, ongoing monitoring, or permanent prevention. For a legacy project that cannot yet run, keep its limits according to [Gradual Takeover of Legacy Projects](legacy-project.md).
