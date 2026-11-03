# Delivery Phases, Testing, and Design Gates

Phases describe responsibilities and acceptance conditions and may be combined. A lightweight change may mark a phase not applicable and explain why. A recipient is a responsibility; it does not require a new role, agent, or user approval. Perform only phases that apply to the current task and checks required by the project.

## From requirements to release

| Phase | Expected deliverable | Pass and acceptance conditions | Where to return on failure |
| --- | --- | --- | --- |
| Initiation/scope | User problem, goal, success criteria, scope/non-goals, dependencies, risks, and task | The requirements owner can determine why the work is needed, what it includes, and its authorized scope; unknowns have a destination | Clarify goal/scope while preserving independently actionable work |
| PRD/specification | Roles, main flows, business rules, permissions, exceptions, acceptance, and requirement version | Design/development/test have no material ambiguity about observable behavior; small changes may be specified on the task card | Requirements or change record |
| Prototype/UI/UX | States and interactions, content and components, visual baseline, applicable viewport/theme/language | The business flow is usable, conventions are reused, applicable states are actually checked, and design/development accept it | Design task and defects |
| Technical breakdown/contract | Module responsibilities, data authority, interfaces/errors, dependencies, slices, and test plan | Upstream and downstream can implement/verify from the contract; compatibility and high-risk tradeoffs are resolved | Specification/contract task |
| Development | Code/configuration/documentation within controlled scope, necessary tests, diff, and self-check | Implementation matches specification, required checks pass, carryover is clear, and the candidate handed to testing is identifiable | Implementation task |
| Testing | Scenario list, actual execution results, coverage boundaries, defects, and retest | Applicable required items have valid evidence; failures, skips, and unknowns are not called passes | Defect fix or test preparation |
| Product/design acceptance | Candidate compared with requirements and visual baseline, evidence, and carryover disposition | The designated recipient confirms scope and result; internal acceptance and user acceptance are recorded separately | Related requirements/design/implementation task |
| Release preparation | Exact candidate, applicable CI/build evidence, release steps, dependencies, observation, and rollback assessment | Evidence matches the candidate; blockers are resolved; authorization and project release requirements are met | Gap task; do not substitute a pass from an older version |
| Release | Version/artifact delivered using the project's existing method and actual execution record | Target environment, candidate identity, configuration/migrations, and health meet project requirements | Stop or roll back under the established plan and retain the event record |
| Post-release observation | Key-flow/error/feedback observations, delivery record, issues, and lessons | The agreed observation scope has evidence; anomalies are recorded and follow-up ownership is clear | Defect and improvement loop |

Release methods, required checks, backup/recovery, and observation windows come from the target project. Do not turn a project's container image, workflow, or manual steps into universal hard requirements. Without release authorization, complete the authorized preparation and state the missing final step; do not assume a commit, push, or deployment is authorized.

## Prototype, UI, and UX

First confirm the valid design version and the sources of existing components/styles. If a legacy project has no conventions, record the actual current baseline and known inconsistencies, then define locally acceptable constraints for this change; do not redesign the whole site without authorization.

For the change scope, create an applicability list across pages/components × states × viewports × themes/languages; not every project needs exhaustive testing of the full Cartesian product. A site-wide style migration needs a complete list of affected entry points/shared components, with migrated items, reasons for exemptions, and unaccepted items identified. Do not declare the whole site consistent after looking only at representative pages.

Applicable checks include:

- **Alignment and structure:** Icon and text baselines, vertical alignment for single/multiple lines, header/content column alignment, list spacing, and inline button/input layout; neighboring actions must not shift when an error appears.
- **Spacing and dimensions:** Container padding, child gaps, first/last item margins, scrolling/fixed regions, safe areas, and usable dialog/drawer space; avoid doubled spacing, missing margins, overflow, and occlusion.
- **Content and states:** Empty/loading/failure/disabled, long text/multiple languages, zero/extreme values, different data volumes, permission differences, and interaction feedback; check keyboard, focus, and assistive reading when applicable.
- **Visual consistency:** Current tokens/theme, type hierarchy, icon sizing, and component variants; do not use universal centering, font-size, or fixed-pixel rules in place of project conventions.
- **UX completeness:** Main path, back/cancel/recovery, error correction, confirmation of critical actions, and consistent data meaning; a successful prototype does not prove upload, save, external interface, or production-flow validation.

Verify with actual rendering and explicit comparison. Automated geometry/visual differences help find issues; direct visual review assesses readability and design intent. Record the pages/configuration actually reviewed; do not describe a count of automated screenshots as a screenshot-by-screenshot review. Explain expected differences when updating snapshots; do not accept all new images merely to make tests pass.

For flow or explanatory diagrams, prioritize the main path, exceptions, and supporting layers, expanding detail as needed. At actual size, inspect text, connectors, wrapping, and narrow-screen readability; counts of nodes and links do not prove a diagram is readable.

### Rendered acceptance for UI-affecting work

Use a compact record in the existing task or acceptance document; a separate report per page is unnecessary. Derive its scope from the changed components, conditional branches, and shared style consumers, not only the route list. A page visited in its default state does not prove its conditional layouts were reviewed.

1. **State and relationship inventory:** Identify affected elements and their relationships: adjacent sections/notices, parent padding, first/last items, text/icon alignment, and wrapping. Select reachable states that change those relationships: base state, each affected conditional block, and coexisting blocks where allowed. Include relevant widths and long content. Record excluded combinations and why; do not demand an exhaustive Cartesian product or invent business states merely for testing.
2. **Expected result before verdict:** Identify the current design revision, component/token rule, or agreed local baseline. State the expected relationship and an appropriate numeric value/range when the design defines one. For example, a notice and a preceding summary should use the project's specified section gap. Do not invent a universal 8/16/24px rule or assume touching panels are wrong when the design intentionally groups them. Missing design inputs stay explicit; a proposed local baseline is not an already approved design.
3. **Actual rendered comparison:** In the selected states and widths, inspect the actual rendering and compare it with the baseline. For a spacing defect, record the neighboring element bounds and actual separation (for vertical siblings, next top minus previous bottom), plus relevant computed styles or parent layout when needed. Internal `gap` does not prove external sibling spacing; CSS declarations and no-overflow checks cannot establish it. Geometry complements direct visual review for readability, optical alignment, and design intent. Use existing permitted browser tools or reproducible manual evidence; do not introduce a new automation stack merely to fill a record.
4. **Evidence and acceptance:** For each selected case retain candidate/environment, route/component, reproducible state/data setup, viewport, baseline reference, expected versus observed result, evidence location or dated direct observation, pass/fail/unverified, and issue/disposition. Respect screenshot restrictions; an authorized direct observation plus measurements may suffice without saving images. If the browser, state, baseline, or required evidence is unavailable, record the missing check and next action; do not mark UI accepted or infer a pass from build/tests. Report implementation status separately from UI acceptance, and do not report UI-dependent release readiness while its required gate is open. If the project permits an exception, record the authorized tradeoff explicitly without relabeling a failed check as passed.
5. **Regression and recurrence:** Reproduce the reported state and inspect affected sibling states/shared consumers. For a recurring measurable defect, retain a runnable scoped assertion or repeatable manual check tied to the relationship and baseline; demonstrate fail-before/pass-after when feasible. Determine whether the prior escape came from unread rules, an omitted state, a missing/incorrect assertion, a baseline mismatch, or a different candidate. Do not convert all route visits or aggregate test counts into layout coverage. Follow [Continuous improvement](improvement.md), including a separately pending later effectiveness check.

A bounded layout regression may check that a conditional notice has the agreed separation when shown, that coexisting notices do not collapse together, and that hiding a notice leaves no unintended empty space. These are examples of relationships to derive from the project, not fixed components or spacing values.

## Test boundaries and coverage definitions

Map requirements/risks → scenarios → cases → execution evidence → issues/acceptance. At minimum, distinguish:

| Evidence | What it can prove | What it cannot replace |
| --- | --- | --- |
| Source/static constraints | Structure, types, or specific coding patterns | Successful behavior or visual correctness |
| Unit/module behavior | Outputs for given inputs within tested boundaries | Real database/permissions/external services |
| Database or service integration | Data and service interactions in a specified environment | Browser layout or a third party's actual environment |
| Browser interaction | Actual page states and operations | Services not connected or production behavior |
| Rendering/visual review | Specified viewport, state, theme, and content | Unreviewed pages/states or all business behavior |
| Real external/production observation | Observed results for a specified target and time | Permanent correctness or another candidate |

Define the scope and denominator of the scenario set first, for example roles/permissions, main flows, errors/boundaries, cross-module behavior, regression, and UI states. Version changes to the scenario set and explain exclusions. Multiple cases for one scenario do not count that scenario multiple times; if any required assertion for a scenario fails, that scenario cannot be counted as passing.

- **Design coverage** = in-scope scenarios with executable cases / confirmed in-scope scenarios.
- **Execution coverage** = scenarios with applicable checks completed and results recorded in this candidate environment / confirmed in-scope scenarios; failures count as executed, skips/blocks do not count as completed.
- **Pass coverage** = scenarios for which all applicable required checks validly passed in this candidate environment / confirmed in-scope scenarios.
- **Execution pass rate** = passed scenarios / scenarios with completed execution; report execution coverage as well, so a small number of passing checks cannot hide what was not tested.
- **Code coverage** is reported separately with its tool and file/package scope and lines/branches/functions; it is not scenario coverage.

Report numerator/denominator, scope baseline, candidate/environment, failures/skips/unknowns, and exclusions. If the denominator has not been confirmed, write “coverage not yet calculable”; do not guess from the number of test files. Set thresholds based on project risk and agreements; there is no universal 100% requirement. Do not dilute a critical acceptance condition for this task with an overall percentage.

## Verification budget and evidence reuse

List direct behavior checks and project-required commands first, then run affected-module checks if needed. For low-impact documentation, a diff/reference check is usually enough; for shared modules, consider consumers; for high-risk work, verify according to project requirements and arrange an independent review. Do not override repository-mandated gates or omit failed checks.

Reliable passing evidence may be reused when content, inputs, specifications, tools/configuration, and environment are the same. When a candidate changes, first check the affected scope; a relevant identity change or failure means the prior pass cannot be reused. Record why checks could not be run and the remaining risk; required acceptance that has not been verified remains unpassed. Record only commands, agents, models, and checks actually used; a plan is not execution.
