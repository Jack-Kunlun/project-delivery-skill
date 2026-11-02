# Gradual Takeover of Legacy Projects

Old technology, missing tests, or the absence of a ledger does not mean the project must be rewritten. First establish a trustworthy picture of its current state and maintainable scope, then add quality constraints with each change.

## Identify the takeover state

| Existing material/capability | Baseline to record now | Do not claim |
| --- | --- | --- |
| Source code and a runnable local environment | Record startup conditions, representative scenarios, current output, and issues | Running locally means production is healthy |
| Source code, but it fails to run or a dependent service is missing | Record attempts, failure conditions, source observations, and a recovery task | An inference from source code means behavior passed |
| No Git history, an old package, or scattered backups | Identify the copy that may be changed, snapshot time, and file hashes; mark gaps in provenance | Treating the newest file timestamp as the official version or inventing commit history |
| Only production is accessible | Record authorized read-only observations or redacted materials; register a need for a copy or test environment | Experimental writes in production, automatic collection of sensitive data, or a direct upgrade |
| Documentation conflicts with implementation | Record “documented requirement / implementation observation / decision pending” side by side | Assuming the old implementation is the correct requirement or changing code by default to match old documentation |

If this task is only to onboard project tracking, register environment recovery, dependency updates, and product fixes as follow-up tasks; do not perform them without authorization. Startup commands may migrate databases, access production, or invoke paid services. First check the environment and what the scripts do, and use an authorized isolated or read-only method.

## Minimum current-state baseline

Record only the areas affected by this task; there is no requirement to cover every module at once:

- **Business and capabilities:** Main roles, business flows, module entry points, and which items are existing, documentation-only, or unknown.
- **Technology and runtime:** Actual frameworks, runtimes, declared dependencies, startup/build methods, required services and configuration names, and environment availability; do not copy secret values. Verify version-sensitive claims such as support periods or vulnerabilities against a reliable current source; do not draw conclusions from age alone.
- **Boundaries and constraints:** Data/state authority, upstream and downstream consumers, compatibility contracts, important scheduled jobs/scripts, writable and read-only areas, and people/service dependencies.
- **Quality state:** Existing tests and their effective scope, representative behavior and visual snapshots, user-reported issues, and reasons the project cannot run or an issue cannot be reproduced. No tests is a gap; it does not mean testing was performed and coverage was 0%. If the scenario denominator is undefined, coverage is unknown.
- **Delivery state:** Whether the project can build/deploy, its actual release method, observability, and existing recovery capabilities. Record facts only; do not change CI or production to onboard governance.

Prefer an actual commit or artifact digest for version identity. If there is no version control, use a clearly labeled read-only snapshot or manifest hash. Introducing Git, migrating directories, or cleaning up backups is a separate decision, not an implied part of setting up records.

## Distinguish three kinds of work

1. **This delivery:** The behavior change or documentation takeover the user actually requested, with its scope and acceptance conditions.
2. **Work required for a safe delivery now:** For example, documenting affected-module behavior, adding a repeatable check, or creating an isolated fixture. Explain the reason and impact in the task.
3. **Historical debt/modernization:** Refactors, outdated dependencies, full UI migrations, historical documentation, and other work that does not affect this task. List it separately for assessment. Schedule it only when authorized; do not slip it in, and do not record an existing defect as newly introduced by this round.

If a serious security or data risk related to this task is found, pause the dangerous operation, continue the unaffected inventory, and follow the project's risk rules. Do not use “legacy” as a reason to skip boundaries that this task must uphold.

## Minimum slice for each change

1. Choose one observable goal and identify the modules and upstream/downstream areas touched; state non-goals and read related historical defects and limits.
2. Record enough of the current-versus-target difference and acceptance conditions to execute the work; do not reconstruct a complete historical PRD. If a requirement is unclear, investigate it first; a person with authority must decide any material behavior tradeoff.
3. **When changing behavior,** preferably preserve a repeatable baseline check before making the change. Options include existing automated tests, a characterization test at the affected boundary, an isolated service, or explicit manual regression steps. Track known errors separately instead of cementing them as permanently correct expectations; add separate assertions for the intended fix.
4. Make the smallest change and record compatibility impact in the contract; do not opportunistically replace frameworks or upgrade lockfiles.
5. Compare before and after, affected consumers, and required acceptance. If no real environment is available, report source-level/local evidence accurately; missing required acceptance cannot be relabeled as a pass.
6. Update the ledger and current-state baseline. Effective new checks or lessons become entry points for the next task. Expand the maintainable scope gradually through actual changes.

Project-level unknowns do not block all documentation onboarding. Whether they block a specific implementation or acceptance depends on whether they affect correctness for that work. Avoid both “understand the entire old system before doing anything” and “tests cannot run, so acceptance can be waived.”

## Meaning of “takeover complete”

“Process taken over” means only that an entry point, current task/issues, evidence boundaries, and a resumable next step are in place. It does not mean historical debt is cleared, all modules have been accepted, or the project has been modernized. State which modules have a baseline and which remain unknown, who owns the next action, and what should trigger expansion to other modules.
