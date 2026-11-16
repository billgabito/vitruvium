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
├── 09-audits/             independent auditor verdicts per version and round (audit-gate.md)
├── references/           catalogs, datasheets, links with dates
├── deliveries/            released packages (v1.0/, v1.1/…) ready to send
├── viewer.html            interactive 3D viewer: rotate, section, systems on/off, FEA overlay, version history (viewer.py)
├── iterations/            one folder per version with images; index.json; index.html (visual timeline)
├── CHANGELOG.md           per iteration: what changed, why, numbers vs previous (written by log_iteration.py)
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

## Iteration log (visual)

At the end of every iteration (each version tag), run:

```
python3 scripts/log_iteration.py --project <project> --version v0.3 --title "Thicker base plate" \
  --why "FEA safety factor 1.4 < 2.0 required" --loop "analysis -> model" --change "plate_t: 6 -> 8 mm" \
  --fea 05-simulation/v0.3 --metric mass_kg=2.41 --metric parts=7 --image 03-model/v0.3.png
```

- `--why` is mandatory: every change carries its reason. Add `--loop` when an improvement loop triggered it and `--decision` when the user chose it.
- Export the geometry of each version from SolidCraft into `03-model/` and pass it with `--model` (repeat once per system/component: frame, guard, motor…; or one glTF whose top-level nodes are the systems). STL is in mm; glTF is in metres by spec — the viewer rescales it automatically when an FEA result shows the mismatch.
- Pass `--motion <motion.json>` when parts move (motion.md); for the live copy put it in `03-model/current/motion.json`.
- Pass `--audit "APPROVED, round N (…)" --audit-file 09-audits/<version>-round-<N>.md` once the independent auditor approved; an iteration without a recorded audit is flagged in the changelog and the viewer.
- Pass `--fea <run folder>` so the viewer can overlay the stress map, deformed shape, supports and loads.
- Save a model screenshot for the changelog (`03-model/vX.Y.png`) and attach the FEA plots.
- Live mode during a session: `python3 scripts/viewer.py --project <project> --serve --open` serves the viewer at http://127.0.0.1:8765 and reloads it automatically whenever `03-model/current.*` (the working copy, exported after every change) or `05-simulation/current/` changes. `/state` reports `stale: true` when a CAD file in `03-model/` is newer than the export. The working copy appears at the top of the history as **LIVE**.
- Rebuild the static snapshot alone with `python3 scripts/viewer.py --project <project> --open` (a single file you can send to others). Useful URL options to open a specific view: `viewer.html?v=1&cut=x&pos=0.4&scale=0.5&ghost=1&sim=0&view=top`. The page loads three.js from cdn.jsdelivr.net, so the first opening needs internet.
- It rebuilds `CHANGELOG.md` (newest first, with a metrics table and deltas against the previous version) and `iterations/index.html`, a timeline the user can open in any browser to see the design evolve.

## Lessons

At each version and at project close, write lessons in `LESSONS.md` (what worked, what failed, what to do differently). Copy generalizable ones to `~/.vitruvium/lessons.md`, which you read at the start of every project.

## state.json

```json
{"project": "pump-motor-mount", "version": "v0.3", "step": "3-simulation", "pending_question": "Choose alternative A/B/C", "workshop": "home-shop"}
```
Update it whenever the step, version or pending question changes.
