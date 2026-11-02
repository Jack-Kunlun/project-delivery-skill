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

## Resumption entry point and ownership

Add a short entry point in an appropriate place in the project's existing README or AGENTS file, preserving its current rules. Onboarding should make clear what to read before work starts, who updates tasks, who accepts the work, where interruptions are recorded, how issues are logged, and how work is resumed at closeout. One person may hold multiple roles; use “unassigned” when no actual person is known. Organizational job titles or six AI agents are not prerequisites for using this process.

Version repository documentation with its branch. A new workspace should include the relevant documentation commit; hand off uncommitted content explicitly rather than claiming it is synchronized, and do not maintain mutable state through absolute paths into another workspace. If an external system is authoritative, preserve its permissions and project mapping.

## Progress reporting

The overview should list product scope, milestones, target/date commitments, current acceptance evidence, blockers, next steps, and the update date. If no date is committed, say so; do not estimate duration from the number of tasks.

Prefer milestone reporting that says which outcomes have been accepted and which lack evidence. If a percentage is needed, define:

- **Denominator:** Delivery units and weights within the committed baseline. Exclude uncommitted ideas, duplicate defect reports, and administrative tasks alone.
- **Numerator:** The weights of delivery units accepted as complete under the agreed definition of done.
- **Source and date:** Link the tasks, evidence, and baseline. Preserve both the old and new measurement basis when scope changes; do not make progress look better by changing the denominator.

Do not describe task counts, lines of code, passing test counts, or document counts directly as the product completion rate.

## Onboarding acceptance

The entry point is findable; each record has one authoritative source; the current work and known issues have destinations; history, current state, and goals are separated; the overview agrees with the ledger; and at least one actionable next task and its acceptance conditions are recorded. Links, identifier/status consistency, and a check of actual differences can show that the documentation has been onboarded; they do not prove that product behavior or continuous improvement is effective. For a legacy project that cannot yet run, continue recording its limits according to [Gradual Takeover of Legacy Projects](legacy-project.md).
