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
