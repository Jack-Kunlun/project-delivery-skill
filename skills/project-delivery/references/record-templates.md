# Record Templates and Traceability

The following are fields, not a mandatory file list. If an existing issue, ticket, or document carries the same information, complete that record; small projects may combine records. Keep the project's existing identifiers. If none exist, define a stable, unique identifier scheme; do not reuse or reorder historical identifiers.

Traceability: source/requirement → task → design/contract → artifact → case/evidence → acceptance → release/observation. Issues link failed evidence to fix tasks, changes link old and new scope, and lessons link specific issues to prevention tasks. Not every item needs its own identifier or file as long as it can be located.

## Task and current status

```text
ID/type/title:
Source/goal or milestone:
Goal and observable acceptance:
Scope/non-goals/allowed workspace:
Owner/actual recipient: write unassigned if not assigned
Status/priority/target version or committed date: state unknown or uncommitted as applicable
Dependencies/blockers/next action:
Risks and basis/limited check budget/conditions for expanding checks:
Applicable design or contract version/matching lesson:
Artifacts/actual checks/evidence/acceptance result:
Not yet verified/carryover/resumption point:
```

Status should match the definition of done. Completing an investigation task may mean that a conclusion was reached; it does not close the related product issue. A task card's progress should point to the same authoritative status rather than duplicating it in a role-based ledger.

## Issue (may be a task type)

```text
ID/discovery or record date/report source:
Observed behavior/expected/actual:
Candidate and environment/entry point/role/prerequisites/reproduction steps: state unknown if not known
Evidence level: user report / source observation / reproduced / fix reverified
Severity (impact)/priority (handling order) and basis:
Occurrence/impact/ownership/verification boundaries:
Lead and related module/investigation or fix task/next step:
Implementation root cause/why the original check missed it: label as a hypothesis until verified
Fix artifact/similar consumers/prevention measure and task:
Closure conditions/reviewer and evidence/follow-up effectiveness recheck:
```

Preserve reasons and destinations for issues that cannot be reproduced, are duplicates, out of scope, canceled, or transferred; do not describe them as fixed. When merging, retain the original ID and point it to the receiving item. For recurrence, append an event and reassess; do not delete the old “pass” record.

## Temporary request and decision

```text
ID/source wording/date recorded:
Category: clarification or addition / defect / new feature / emergency response / idea
Original scope and current change/reason:
Affected requirements, modules, consumers, acceptance, and target version:
Priority/dependencies/schedule or risk tradeoff (write pending assessment if not estimated):
Decision/decision-maker and authorization basis/which part of which decision it replaces:
Related task: reuse the original or create a new one, and explain why
Interrupted task's status/completed and remaining work/resumption point/resumption conditions:
```

Recording an idea does not commit to it; emergency defects still retain their scope and minimum necessary verification. Replace old conclusions by appending revisions; do not silently rewrite the user's original request.

## Module and phase handoff

```text
Module/contract version/source module → target module:
Responsibilities/in-scope and out-of-scope:
Data and state authority/who may write/readers and consumers:
Inputs: source, format, prerequisites, permissions, validation
Outputs: structure, semantics, completion status, errors, and side effects
Failure, timeout, retry/idempotency, and fallback ownership: fill in as applicable
Upstream dependencies/downstream consumers/compatibility or migration impact:
Deliverable and version/actual sender/recipient:
Acceptance conditions/checks and evidence/open items:
Rejection reason/return task/conditions for reacceptance:
```

Source-code responsibilities are facts; collaboration responsibilities are agreements; future decomposition is a plan. Keep them separate. Do not silently change upstream semantics, bypass permissions, or swallow errors to make an integration work. Track every affected consumer when a contract changes; create an investigation task for unknown consumers. There is no requirement to split a monolith into services.

## Test case and evidence

```text
Case ID/related requirement, task, module, and risk:
Role/environment/prerequisite data (redacted or isolated)/page and state:
Steps/inputs/expected assertions/explicit failure conditions:
Level: source/unit/module/database/browser/visual/external integration/production observation
Automated or manual/entry point to run:
Actual candidate or snapshot/specification and design version/tools and configuration/execution time:
Actual result: pass / fail / skipped / blocked / not run
Evidence location/related issue/uncovered areas/retest trigger:
```

For files that change continuously, a path alone may not be enough to restore the candidate; add a commit, artifact digest, or file hash as appropriate for the project. Store evidence only in repository-approved locations or authorized systems. Keep temporary tests and large artifacts local when project rules require it, and explain their availability in the delivery notes. Do not commit secrets or every temporary artifact just to create a trail.

### UI comparison record (for selected affected cases)

```text
Related task/issue; candidate/environment; route/component:
State/data setup and coexisting conditional regions; viewport/theme/language:
Design revision or local baseline; affected relationship or shared consumer:
Expected appearance/geometry; observed rendering/measurements:
Direct visual review and evidence (path or dated observation); actual tool:
Result: pass / fail / unverified; defect/disposition or exclusion reason:
Regression entry point; remaining checks and resumption action:
```

Use the [rendered UI acceptance gate](delivery-gates.md) to choose meaningful cases. Keep unknowns and exclusions visible; an empty record or a source-only check is not visual acceptance.

## Events, existing outcomes, and improvements

- **Event:** Date and event type, related ID, actual operator, previous state → new state, reason, artifact/evidence. Record key starts, blockers, interruptions, acceptance, cancellation/merger, and closeout; do not copy every tool log. For backfills, distinguish the record date from when the event actually occurred.
- **Existing outcome:** Capability/module, user-observable behavior, source/history, separate implementation/acceptance/release/production-verification statuses, version/date (if known), limits, and current issues. A new defect does not erase the historical delivery fact.
- **Improvement/lesson:** Pattern, source issue, applicable trigger, implementation root cause and escape reason, before/after rule, affected modules, prevention task, effectiveness check and retest time, replacement/retirement relationship. Close the loop according to [Continuous Improvement](improvement.md).

## Closeout record

State what was and was not completed this round, actual verification scope, current status, blockers, next steps, workspace/candidate identity, and location of uncommitted material. Do not hide acceptance gaps behind “follow-up improvements,” and do not assign planned work by default to a nonexistent person or agent.
