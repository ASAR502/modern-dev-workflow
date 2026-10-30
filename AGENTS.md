## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` at the repo root plus `docs/adr/`. See `docs/agents/domain.md`.

## Skill Usage

- Before starting a coding task, inspect the available skills and identify the relevant ones.
- Read the relevant skill's `SKILL.md` instructions before performing the task.
- Follow the skill's workflow when implementing features, fixing bugs, writing tests, or reviewing code.
- For non-trivial changes, plan the implementation before modifying code.
- For bug fixes, investigate the root cause before applying a fix.
- Run relevant tests and checks after making changes.
- Review the final changes for correctness, security, edge cases, and regressions.
- Do not claim to have used a skill unless its instructions were actually read and followed.
- Do not load unrelated skills or force every skill into every task.
