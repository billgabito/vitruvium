# Vitruvium changelog

Newest first. Each version: what changed and why.

## v0.18.1 — 2026-11-15
- **Install prompt** for any AI agent (README and `docs/INSTALL-PROMPT.md`, English and Spanish): clone, link the skill, optional auditor/conciliator, tool check, SolidCraft MCP, update mode, verification — asking before every system change. *Why:* installing should be one copy-paste.

## v0.18.0 — 2026-11-15
- **Visual fidelity rule** (`engineering/parts.md`): parts modelled as they are — springs as helices, screws with heads and drives, nuts, bearings with rings, gears with teeth, shafts with steps, catalog parts from manufacturer STEP; never placeholders; fine tessellation for export; checked by the auditor.
- **Medium–high rendering**: studio environment reflections, filmic tone mapping, soft shadow on a ground plane, creased normals for smooth round surfaces, real-material look from `parts.json` materials (steel, stainless, zinc, aluminium, brass, copper, rubber, engineering plastics, 3D-print plastics, wood) with a "colour by part" alternative. *Why:* things must look like what they are, without heavy graphics effort.

## v0.17.0 — 2026-11-15
- **Systems organized as an expanded tree** by group (fabricated parts, shafts, bearings, gears, springs, seals, fasteners, motors, sensors and electronics, commercial parts — or `group` in parts.json for functional systems), with a switch per group; the parts list uses the same groups; new ID code `SN` for sensors and electronics. *Why:* seeing which code belongs to which system at a glance.

## v0.16.0 — 2026-11-15
- **Parts always solid**: no automatic transparency (selection highlights in colour, moving parts in amber; x-ray mode removed). **Per-part show/hide and opacity** in the parts list, synchronized with the systems list; labels of hidden parts hide too; parts table fits the side panel; live server accepts view URLs with options. *Why:* parts must look solid and real; transparency only where the user chooses it.

## v0.15.0 — 2026-11-15
- **Display modes** in the viewer: shaded, shaded + edges, wireframe (feature edges only; the selected part stays solid) and x-ray; one function now decides every surface's look (display mode, selection, motion highlight). *Why:* wireframe lets the user see through the assembly and judge hidden parts and clearances.

## v0.14.0 — 2026-11-15
- **Assemblability is mandatory** (principle 7, `references/manufacturing/assembly.md`): every multi-part design has an `assembly.json` sequence (order, insertion direction, tool, torque, check with evidence of free path and tool access, disassembly of service parts), verified in SolidCraft by moving parts along their paths with interference checks; new loop "not assemblable → model"; auditor treats a non-assemblable design as a blocker; seven assembly errors added to the catalog (43 in total); `log_iteration.py --assembly` records steps, failed and unchecked steps and warns; viewer **Assembly sequence** panel plays the sequence step by step with failures in red. *Why:* a design that cannot be built is wrong, however good it looks.

## v0.13.0 — 2026-11-15
- **Skill reorganized**: `SKILL.md` rewritten around principles → session start → workflow A–K (one table with what to do and what to read per phase) → loops → showing → talking → modes → updates → toolbox → non-negotiables; references grouped in `process/`, `engineering/`, `manufacturing/`, `quality/`, `tools/` (audit mode renamed `review-existing-design.md`); all links updated; README with repository structure; BEHAVIOR sections renumbered. *Why:* the skill had grown by additions; one clear structure is easier to follow for the agent and for people.
- **Part detail card**: click a part in 3D (or its label or list row) to see ID, descriptive name, type, specification, material, quantity, function, requirements, why it exists, features, source, route and drawing; systems list shows ID + name. Descriptive names rule in `parts.md` ("Socket head cap screw M5×12", never "screw"). *Why:* an ID alone does not say what a part is.

## v0.12.0 — 2026-11-15
- **Expert conciliator** (`agents/vitruvium-conciliator.md`, most capable model): if the auditor does not approve after round 2, it issues a binding ruling per open finding (auditor upheld / designer upheld / alternative) and may propose a better solution; round 3 checks compliance. Designer responses per finding (fixed / disputed) are recorded in `09-audits/`. Nothing reaches the user without approval; an unimplementable ruling produces a report marked NOT APPROVED. *Why:* avoid endless audit loops on complex parts while keeping the approval gate.

## v0.11.0 — 2026-11-15
- **Every part, feature and change must have a reason**: `parts.json` requires `function`, `requirements` and `why` (plus `features` with their reasons); `log_iteration.py` warns and counts `unjustified_parts`; the viewer shows function and why per part and flags missing reasons; the independent auditor challenges each reason against the files (checklist item 0). *Why:* nothing should be in a design without a logic that someone can verify.

## v0.10.0 — 2026-11-15
- **Professional viewer UI**: Vitruvium logo and favicon, engineering typography (Barlow; ISO 3098 osifont for IDs and annotations), header with version, audit and live badges, edges, ground grid, status bar (units, size, triangles, export time). *Why:* the visualization must look professional and engineering-grade.
- **Parts breakdown with IDs** (`parts.json`, `references/engineering/parts.md`): ID convention (P, SH, BR, FS, SP, SE, G, MO, CP, AS), parts list tab, ID labels in 3D, click to isolate, parts metrics in the changelog. *Why:* every screw, shaft, bearing and part must be named and traceable.
- **Exploded view** slider (direction per part optional). *Why:* to see how the assembly goes together.

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
