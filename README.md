# Project Delivery

A reusable agent skill for traceable project delivery: requirements, design, implementation, testing, acceptance, release, and continuous improvement.

[中文说明](README.zh-CN.md) · [Skill instructions](skills/project-delivery/SKILL.md) · [MIT License](LICENSE)

Project Delivery helps a coding agent maintain a project's actual work and evidence. It adapts to existing records, starts small when records are missing, and supports gradual adoption of legacy systems.

## What it covers

- Project overview, existing capabilities, milestones, and evidence-based progress.
- Tasks and issues with ownership, dependencies, acceptance criteria, and resumption points.
- Ad hoc requirements and scope changes, including interrupted work.
- PRDs, prototypes, UI/UX delivery, implementation, testing, acceptance, and release gates.
- Module responsibilities, input/output contracts, state ownership, and handoffs.
- Scenario coverage, verification boundaries, visual checks, and unresolved gaps.
- Recurring defects, prevention work, and follow-up checks that test whether improvements work.

## Three adoption paths

| Project situation | How the skill responds |
| --- | --- |
| Existing ledger or issue tracker | Reuse its authoritative records, identifiers, and states. Fill gaps without creating a second mutable task list. |
| No ledger | Create a minimal overview and work/issue record from available code, documents, and feedback. Mark unsupported history as unknown. |
| Legacy or poorly documented project | Establish a current-state baseline and improve the affected scope incrementally. Missing PRDs, tests, Git history, or a runnable environment do not require an immediate rewrite. |

A small project can start with one document. Larger projects can split records when that improves maintenance. The skill does not require a fixed team structure, technology stack, module count, or release mechanism.

## Installation

The distributable skill is **`skills/project-delivery/`**. The repository root contains publishing and maintenance documentation; it is not the skill installation directory.

### Install through Codex's skill installer

If your Codex environment provides `$skill-installer`, ask:

```text
Use $skill-installer to install the skill from
https://github.com/Jack-Kunlun/project-delivery-skill/tree/main/skills/project-delivery
```

For a pinned version, replace `main` with a tag listed in the repository's [releases](https://github.com/Jack-Kunlun/project-delivery-skill/releases). If the skill is already installed, compare and deliberately update the existing copy instead of creating a duplicate.

### Manual installation (macOS / Linux)

Clone the repository:

```sh
git clone https://github.com/Jack-Kunlun/project-delivery-skill.git
cd project-delivery-skill
```

From the repository root, copy the skill into the Codex skills directory. This command refuses to overwrite an existing installation:

```sh
(
  destination="${CODEX_HOME:-$HOME/.codex}/skills/project-delivery"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf '%s\n' "Already exists: $destination. Compare it before updating."
    exit 1
  fi
  mkdir -p "$(dirname "$destination")"
  cp -R skills/project-delivery "$destination"
)
```

Invoke the skill in a subsequent task. Other agents may use different discovery directories; use their installation mechanism and preserve the entire skill folder.

## Usage

Open the target project and ask:

```text
Use $project-delivery to establish or update this project's delivery process
and work ledger. Start with the current state and existing records.
```

For a legacy project:

```text
Use $project-delivery to take over this legacy project. Document its current
capabilities, evidence gaps, known issues, and next steps. Do not restore the
runtime or upgrade dependencies as part of this documentation task.
```

For an interruption or recurring defect:

```text
Use $project-delivery to record this new requirement and recurring UI issue.
Assess the affected work, preserve the current task's resumption point, and
track the investigation, prevention work, and acceptance evidence.
```

Invoke it for project adoption and delivery management. A routine single-file coding request does not automatically require a full project audit or a new governance structure.

## How it works

1. Locate the actual project and read its applicable instructions and authoritative records.
2. Associate substantive work with a task, including documentation and initial adoption.
3. Define scope, ownership, dependencies, observable acceptance, and a bounded verification plan.
4. Execute and hand off work using the project's own contracts and requirements.
5. Record actual results, unresolved gaps, decisions, and the next resumption point.

The skill reads only the references relevant to the task. It keeps **implemented**, **accepted**, **released**, and **verified in production** separate. Test coverage uses a defined scenario denominator; source inspection, mocks, browser checks, visual review, and live integration are different kinds of evidence.

## Language and compatibility

The main README is English; [README.zh-CN.md](README.zh-CN.md) provides the Chinese version. The skill instructions, references, and Codex display metadata are currently **written in Chinese**. An English README does not imply that the entire skill has been translated.

The package contains Markdown instructions and optional Codex UI metadata. It has no application runtime, package-manager dependencies, background services, or bundled executable automation. Actual tool availability and skill discovery depend on the host agent.

## Repository layout

```text
skills/project-delivery/
  SKILL.md                       Skill entry point and routing
  agents/openai.yaml             Codex display metadata
  references/
    adopt-project.md             Existing records and first-time adoption
    legacy-project.md            Gradual takeover of legacy systems
    record-templates.md          Tasks, issues, changes, handoffs, evidence
    delivery-gates.md            Lifecycle, UI/UX, tests, and acceptance
    improvement.md               Recurrence and improvement follow-up

docs/PROJECT.md                  This repository's maintenance record
```

## Validation and limits

The original skill was exercised on two isolated sample projects: one with an established ledger and one legacy project without records or a runnable environment. First-pass omissions in documenting the adoption task and recurring-defect follow-up were corrected and rechecked. These were bounded exercises, not proof of effectiveness across every project.

Publication checks cover package identity, skill metadata, local links, the documented manual installation, and protection of an existing installation. See [the project record](docs/PROJECT.md) for actual results and publication status.

Installing this skill does not create CI gates, continuous monitoring, or an immutable audit system. It does not automatically adopt other projects, resolve their defects, or authorize commits, deployments, production access, or external messages. Project instructions and the user's actual authorization remain authoritative.

## Contributing

Open an issue with a concrete scenario, expected behavior, observed result, and relevant evidence. Do not include credentials, private project material, or production data.

Keep changes focused. Update both READMEs when public usage changes, keep the skill entry point concise, and verify that its referenced files remain usable. Behavioral changes should be checked against realistic, isolated scenarios rather than assertions that merely match instruction wording.

## License

[MIT](LICENSE) © 2026 Fenglan.
