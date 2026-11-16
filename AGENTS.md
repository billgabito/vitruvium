# AGENTS.md

This repository contains **Vitruvium**, an agent skill for mechanical design based on mechanical simplicity. It follows the open Agent Skills format (a `SKILL.md` with YAML frontmatter plus `references/` and `assets/`), so any AI agent that reads files can use it.

When the user asks to design, redesign, audit or fabricate a mechanical part, mechanism or assembly, read and follow:

`skills/vitruvium/SKILL.md`

Before presenting any iteration to the user, run an independent audit with the prompt in `agents/vitruvium-auditor.md` in a separate agent or session. If it is still not approved after round 2, run the expert conciliator (`agents/vitruvium-conciliator.md`) on the most capable model available; its ruling is binding (see `skills/vitruvium/references/audit-gate.md`).

Load the files in `skills/vitruvium/references/` only when the step you are on needs them.
