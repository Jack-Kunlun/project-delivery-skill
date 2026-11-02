---
name: project-delivery
description: "Initialize project delivery and keep it active through project-local agent instructions. Use when initializing or taking over a project, establishing a work ledger, managing delivery, or continuing substantive work in a project that adopted this workflow. Covers tasks/issues, scope changes, design, handoffs, acceptance, and recurring-defect improvement. Reuse existing records; a standalone package-scaffolding command or conceptual question does not by itself authorize full project onboarding."
---

# Project Delivery

Make work resumable, issues traceable, and delivery verifiable. Records should serve current work; their volume is not evidence of progress or quality.

## Choose the adoption path

1. **Existing ledger or process:** Read the project entry point, current task, recent decisions, and relevant lessons. Reuse its files, external systems, identifiers, and states. Do not create a second mutable status source.
2. **No ledger:** Follow [Project adoption](references/adopt-project.md) to inventory the project and create its first records. A small project can start with one document; create actionable records before a collection of empty files.
3. **Legacy or poorly understood project:** Also read [Legacy-project takeover](references/legacy-project.md). Establish a current-state baseline and adopt incrementally. Missing PRDs, tests, Git history, or a runnable environment do not prevent documentation, but never invent verification.
4. **Process questions or proposal review only:** Answer the question or offer recommendations. Without a request to write or an existing project convention, do not automatically adopt the entire project.

First establish the actual project root, worktree, and current authorization. The current directory may be a prototype or backup. If candidate identity is uncertain, continue only safe inventory work; do not implement in the wrong project. Read applicable AGENTS and existing conventions, and preserve user changes. The project's own security, testing, design, and release requirements take precedence over these default templates.

## Initialization defaults

A request to initialize or adopt the project's workflow includes persistent integration; the user does not need to list those steps or ask for future automatic use. Read [Project adoption](references/adopt-project.md) and, within the authorized project scope:

- Establish or reuse the authoritative records and register initialization itself.
- Create or update the effective project-local `AGENTS.md` instruction entry point, accounting for applicable overrides. A README link alone does not complete this step.
- Install concrete record pointers and the start/update/accept/closeout rules for later substantive tasks. Preserve existing rules and identifiers; update an existing integration instead of duplicating it.
- Verify the integration and a fresh-context continuation without a workflow reminder. Record what actually ran; missing validation or an unwritable effective instruction file remains an explicit gap.

For a project previously adopted by this skill, repair a missing or outdated persistence integration when the skill next runs within the authorized project scope, preserving current records. After adoption, ordinary substantive work follows the persisted project instructions without reinitializing the project or requiring the user to repeat `$project-delivery`. Use the current task and applicable references. This is task-driven instruction use, not a background service or a claim that a skill is loaded on every turn.

## Read references as needed

| Current work | Reference |
| --- | --- |
| Initial adoption, overview, progress, and authoritative-source mapping | [Project adoption](references/adopt-project.md) |
| Old systems, missing records, broken environments, or uncertain historical behavior | [Legacy-project takeover](references/legacy-project.md) |
| Tasks, issues, interruptions, handoffs, evidence, and wrap-up | [Record templates](references/record-templates.md); use only applicable fields |
| Requirements through release, prototypes/UI, testing boundaries, and scenario coverage | [Delivery gates](references/delivery-gates.md) |
| Recurrence, escaped defects, expanded ownership/impact, and improvement effectiveness | [Continuous improvement](references/improvement.md) |

Do not load every reference or scan the whole repository on every turn. Start with the authoritative records needed for the current task.

## The work loop

1. **Restore context:** Identify the current goal, baseline/design version, task state, dependencies, recent changes, applicable lessons, and unverified items. When sources conflict, distinguish observed behavior, intended behavior, and history.
2. **Record and bound the work:** Before substantive execution, associate an existing task or create one. Record the goal, scope/non-goals, source, actual ownership, observable acceptance criteria, dependencies, risk, and a bounded verification budget. Keep small steps under the same task instead of creating a task for every command. Retain the source, handling entry point, and next step even for an issue that has not been reproduced.
   Initial adoption and documentation are substantive work too: record them in the authoritative ledger, not just future product requests. Key events can live inside the task; a separate event-log file is not required.
3. **Execute and hand off:** Follow project conventions. For cross-module work, first establish inputs/outputs, state authority, failure ownership, and receiving criteria. Upstream completion does not establish downstream integration success. Record receiving evidence even when one person fills multiple roles; do not imply that an agent or independent review actually ran.
4. **Verify and accept:** Run applicable gates and mandatory project checks. Record the actual candidate, environment, tools, results, and gaps. Return failures to the relevant task and retain critical unknowns as unresolved. Expand checks only for new impact, a failed check, or a project requirement.
5. **Wrap up and resume:** Update the single authoritative status ledger. Append key events and decisions, link artifacts/evidence, and record remaining work, blockers, the resumption point, and the next step. Separate user acceptance from the executor's internal acceptance; do not describe an unconfirmed result as user approval.

Preserve the project's state model. If none exists, a useful default is: Needs clarification → Not started → In progress → Awaiting acceptance → Accepted. Retain reasons and links for blocked, canceled, merged, or reopened work. Record implemented, accepted, released, and production-verified states separately; a generic “done” must not hide environment boundaries. Stages may be combined or marked not applicable, with reasons and remaining receiving criteria. Do not add approval at every stage.

## Overall progress and changes

- Include existing product capabilities, delivered outcomes, current goals, milestones, risks/dependencies, and next steps in the overview. Do not report only the current documentation tasks.
- Give each status one authoritative source. The overview is a dated, baseline-specific summary; role views and module inventories link to tasks rather than maintain another live status list.
- Define scope, completion criteria, and weights before reporting percentages. Without them, describe the specific accepted, pending, or blocked scope; unknown is neither 0% nor 100%. Backfill history only from evidence, never invented dates, people, commitments, or tests.
- Classify interruptions as clarification/addition, defect, new feature, urgent response, or idea. Record the original wording/source, impact, and tradeoff; link tasks and affected acceptance criteria. Leave a resumption point when interrupting work. Separate defect severity from scheduling priority; an interruption is not automatically top priority.
- Continue clear, small changes within existing authorization. Request a decision only for material product choices, scope/date commitment conflicts, or irreversible consequences. A backlog entry is not execution or release authorization.

## Reusable quality constraints

- Prototype and UI delivery should reuse the project's visual language and components and inspect actual rendering. Check alignment, spacing, long text, and applicable states using [Delivery gates](references/delivery-gates.md). Producing screenshots or asserting source text alone does not prove visual correctness.
- Use an agreed scenario set as the coverage denominator. Distinguish designed, executed, passed, and code coverage; identify mocks, skips, missing configuration, and checks that were not run.
- On recurrence signals such as “again,” “recurring,” or “already fixed,” read [Continuous improvement](references/improvement.md). Issue records need an investigation/fix path and a follow-up path for prevention, similar consumers, and effectiveness checks. Before reproduction, these may be requirements for later investigation; never invent an implemented safeguard. A recorded lesson is not proof that recurrence has been prevented.
- Keep project lessons and rules in the project's authoritative records and establish an entry point that relevant future tasks must read. A single project's experience must not automatically modify personal global memory, this skill, or another project.
- This documentation workflow does not itself provide automatic audits, continuous monitoring, or CI blocking. Track automation as separately authorized work with acceptance criteria and evidence.

## Delivery report

State what changed and where, which level of completion was reached, which checks actually ran, and the remaining work/next step. On initial adoption, give the single entry point and record-keeping responsibilities; afterward report the increment. Avoid repeating the whole process. Commits, pushes, releases, and messages to others remain subject to actual authorization and existing project requirements.
