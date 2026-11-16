# Vitruvium changelog

Newest first. Each version: what changed and why.

## v0.9.0 — 2026-11-15
- **Animation of moving parts** in the viewer from `motion.json` (revolute, prismatic, coupled parts, keyframes for closed loops): play/pause, position slider, speed, highlighted moving parts, joint axes, list of motions. *Why:* the user must see which parts move and how, not read it.
- **Independent audit gate**: `vitruvium-auditor` agent (fresh context, project files only) approves each iteration or returns findings with evidence; verdicts in `09-audits/`, shown in changelog and viewer. *Why:* the designer must not audit its own work; what reaches the user must be correct.

## v0.8.0 — 2026-11-15
- **Live viewer** (`viewer.py --serve`): the working copy (`03-model/current.*`) appears as LIVE and the page reloads by itself after every export, keeping the camera; red banner and `/state` flag when the CAD is newer than the export; camera fit respects window shape. *Why:* what the user sees must always be the current design — one source of truth (SolidCraft), never a second model rebuilt in three.js.

## v0.7.0 — 2026-11-15
- **Interactive 3D viewer** (`scripts/viewer.py` → `viewer.html`): rotate, standard views, section along X/Y/Z, systems on/off, FEA overlay (stress map, deformed shape, supports and loads), version history with reasons and the previous version as a ghost. *Why:* the user validates and corrects the design, and can only judge what they can see.
- `fea.py` now writes `fea_view.json` (outward-oriented surface, nodal von Mises, displacements); `log_iteration.py` takes `--model` and rebuilds the viewer.

## v0.6.0 — 2026-11-15
- **FEA script** (`scripts/fea.py`): STEP → Gmsh (C3D10) → CalculiX → max von Mises, max displacement, safety factor, optional stress images. *Why:* every project was rewriting the same pipeline; validated on a cantilever (deflection within 0.5% of beam theory).
- **Visual iteration log** (`scripts/log_iteration.py`): `CHANGELOG.md` and `iterations/index.html` per project, with what changed, why, numbers vs the previous iteration and images. *Why:* the user must be able to see how a design evolved and the reason behind each change.

## v0.5.1
- CLI vs MCP decided per tool (MCP only for SolidCraft); ccx2paraview and PyVista added for FEA images; third-party MCP servers listed as optional. *Why:* simplest interface that works in any agent.

## v0.5.0
- Daily update check with ask / auto / off. *Why:* users get improvements without reinstalling, and only with their consent.

## v0.4.2
- Verified tool sources and install commands per OS, plus `check_tools.sh`. *Why:* no searching for tools on every install.

## v0.4.1
- Transfer of solutions from other industries, with a viability check. *Why:* the best idea often lives in another field.

## v0.4.0
- Existing solutions first: buy, adapt or design from scratch. *Why:* the simplest design is the one you do not have to make.

## v0.3.0
- Ingress protection (IP rating, IEC 60529) in requirements and design. *Why:* sealing must be designed in from step 1.

## v0.2.x
- Renamed to Vitruvium; visual identity (Vitruvian man as an FEA mesh); refined figure. *Why:* a name and identity of its own, without clashing with existing brands.

## v0.1.x
- Core process (Musk's 5 steps inside Ullman), interview, workshop profile, alternatives, analysis, error catalog, drawings, project folders, audit mode; agent-agnostic; MIT license and IEEE citation.
