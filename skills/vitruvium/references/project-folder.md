# Project folder and versioning

## Where

Ask once where the user keeps projects (default `~/mechanical-projects/`), remember it in `~/.vitruvium/config.yaml`, and create one folder per project with a short kebab-case name (`pump-motor-mount`). Folder and file names stay in English for portability; document contents are in the user's language.

## Structure

```
<project>/
├── README.md              what it is, status, current version, workshop profile used
├── 01-requirements/       interview.md, black-box.md, requirements.md
├── 02-concept/            deleted.md, alternatives.md, decision.md
├── 03-model/              SolidCraft JSON scripts, .sc, STEP exports
├── 04-calculations/       calc notes with sources
├── 05-simulation/         meshes, CalculiX inputs/results, report
├── 06-manufacturing/      routes.md, outsource.md
├── 07-drawings/           PDF, DXF, bill of materials
├── 08-prototypes/         photos, tests, results
├── references/           catalogs, datasheets, links with dates
├── deliveries/            released packages (v1.0/, v1.1/…) ready to send
├── DESIGN-LOG.md          step-by-step: what was done, what failed, where we went back
├── LESSONS.md             what we learned
└── .mech/state.json       current step, version, pending question (for status displays)
```

Create folders as they are needed, not all empty at once. Templates in `assets/templates/`.

## Git (handled by you, invisible to the user)

- `git init` at project creation; commit at each meaningful step with a clear message in the user's language.
- Tag versions: v0.1, v0.2… concept and risk prototypes; v0.x functional prototype; v1.0 first built or released; v1.1… field improvements; v2.0 redesign.
- On release, copy the drawing/STEP/BOM package to `deliveries/vX.Y/`.
- If Git is not installed, tell the user and fall back to `deliveries/` snapshots only.

## Design log entry format

```
## YYYY-MM-DD — vX.Y — <step>
What was done:
Result / numbers:
Loop: <failed check> → returned to <step> (if any)
Decision and reason:
```

## Lessons

At each version and at project close, write lessons in `LESSONS.md` (what worked, what failed, what to do differently). Copy generalizable ones to `~/.vitruvium/lessons.md`, which you read at the start of every project.

## state.json

```json
{"project": "pump-motor-mount", "version": "v0.3", "step": "3-simulation", "pending_question": "Choose alternative A/B/C", "workshop": "home-shop"}
```
Update it whenever the step, version or pending question changes.
