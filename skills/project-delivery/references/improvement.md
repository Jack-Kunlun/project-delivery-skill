# Issue Boundaries and Continuous Improvement

The goal is to help the next related task avoid the same kind of mistake, not merely to add another lesson.

## Record the issue first, then establish its boundaries

Record an issue even if it has not been reproduced, and distinguish reported facts from inferences. Record four boundaries:

1. **Occurrence boundary:** Candidate, entry point, environment, role, data/state, and trigger conditions; identify what remains unverified.
2. **Impact boundary:** Affected functionality, shared components and consumers, historical versions, and data/external side effects; distinguish confirmed from possible impact.
3. **Ownership boundary:** Who owns the rule/implementation/state, who leads investigation and repair, and how upstream/downstream teams accept the change; do not simply assign the issue to the page where the error appears.
4. **Verification boundary:** What the old checks did and did not test, which candidate the evidence covers, what layer proves the current fix, and what limits remain.

Every issue needs an owner and a destination; crossing module boundaries is not a reason to leave it unowned. Investigate unknown key ownership; do not infer root cause from the page where the issue appears.

## When to expand investigation or escalate

| Signal | What to do |
| --- | --- |
| The same pattern recurs or the user corrects it again | Reopen or link the original issue; check why the old fix, case, and rule did not prevent it |
| A shared component/rule causes problems on multiple pages | List affected consumers, check the common cause and representative states, then add checks for the scoped impact |
| Cross-module conflict in data authority or input/output semantics | Update the handoff contract, failure ownership, and compatibility handling; verify downstream acceptance |
| The original test passed but the underlying issue escaped | Distinguish gaps in source assertions, mocks, and real behavior; adjust scenarios/check level |
| Major security, permission, data, migration, production, or similar impact | Follow the project's high-risk path and obtain an independent review when needed; do not accept a general risk rationale to bypass mandatory constraints |
| Fixes repeatedly fail or root cause remains unclear | Stop repeating the same attempt, preserve new evidence, narrow hypotheses, and use bounded research or request a necessary decision under the project's retry budget |

Escalation is evidence-driven. It does not mean every issue needs a repository-wide refactor, full test run, or new approval. When expanding scope, state the added impact, check budget, and stop conditions.

## Close the loop

1. Establish a reproduction or evidence that explains the issue and preserve the original failure. If it cannot be reproduced, record attempts and the next step.
2. Confirm or label as a hypothesis why the implementation failed and why the original design/review/test allowed it to pass. “Carelessness” alone is not a sufficient escape cause.
3. Link repair and prevention tasks. For a small issue, one task may have separate acceptance conditions to avoid duplicate effort. Prevention may be a shared component, check, contract, design convention, or explicit manual review step; choose what best matches the failure cause.
4. Retest the original issue and affected consumers. When feasible, show that the new check fails on the old error and passes after the fix. If automation is not possible, provide repeatable steps, the actual review scope, and evidence; do not claim an automated regression test that did not run.
5. Keep acceptance separate: the fix works; the prevention measure is implemented; the prevention measure remains effective in a later applicable scenario. If no later trigger has occurred, mark the effectiveness check pending. Do not indefinitely block local fix acceptance, and do not claim permanent prevention.
6. Assign an owner/task to recheck effectiveness at the next related change, shared-consumer onboarding, or applicable release. No new complaint, trigger, or observation does not prove effectiveness.

## Make lessons inputs to the next task

Record the pattern, trigger, source issue, applicable modules/states, required checks, prevention task, evidence, and effectiveness recheck in the project's authoritative lessons/rules. The project entry point should require related tasks to read and link matching lessons before starting; closeout records the check results.

When updating a rule, preserve the old and new rules, reason, evidence, affected consumers, and replacement scope. Explicitly retire rules that are obsolete or superseded by a new design; do not restore old styles from historical records. Lessons should address reproducible patterns, not codify the dimensions of one screenshot or one project's default layout.

For recurrence, append an event and reassess boundaries, preserving the evidence that previously passed so the gap in the defense can be located. Do not create a record of continuous success by deleting failures or overwriting history. Only actual execution results can prove that an improvement is effective; documentation, reminders, skill installation, or planned CI do not prove that automatic protection is active.
