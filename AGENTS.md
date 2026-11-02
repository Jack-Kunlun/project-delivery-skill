# Repository guidance

Read [docs/PROJECT.md](docs/PROJECT.md) before substantive work. Keep the task, decision, evidence, and resumption record there; do not create a second live ledger.

- This repository distributes a documentation-based skill. The maintained package is `skills/project-delivery/`; do not edit personal installed copies as the source of truth.
- Use English for the main README and keep `README.zh-CN.md` aligned when public usage changes. The skill itself is currently Chinese; translation is a separate scoped change.
- Preserve progressive disclosure and the adopting project's own conventions. Do not turn a project-specific lesson into a universal rule.
- For packaging/documentation changes, inspect the diff, metadata, relative links, and the applicable installation instructions. Run the available skill-creator validator when changing skill metadata. Behavioral changes need a bounded realistic exercise when warranted; wording-only assertions are not behavioral evidence.
- Keep temporary exercises, credentials, private project data, and local verification artifacts out of commits. Record the actual result and verification limits in the project record.
- Follow the user's actual commit, push, and publication authorization. Do not add CI, background automation, or deployment infrastructure as an incidental documentation change.
