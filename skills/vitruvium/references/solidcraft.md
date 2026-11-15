# Modelling in SolidCraft

SolidCraft (github.com/tangency-labs/solidcraft) is an open-source parametric CAD (Rust) with a built-in MCP server. It is young: verify geometry with measurements rather than trusting a command succeeded.

## Setup

Install and MCP registration for every OS: see tools-setup.md.

- MCP: register `solidcraft-cli mcp` as an MCP server in your agent host (Claude Code: `claude mcp add solidcraft -- solidcraft-cli mcp`; other hosts: the same command in their MCP settings). Add `--connect` to drive the running desktop app so the user can watch.
- If the MCP tools are not available, tell the user how to add them; meanwhile you can still write the JSON command script and run it with `solidcraft-cli run script.json --out part.step`.
- Before modelling, read SolidCraft's own guidance through its `skill_reference` tool (`solidcraft-modeling`, `solidcraft-mechanisms`). Those skills teach *how* to operate it; this skill decides *what* to build.

## Working rules

- Parameters first: every driving dimension is a named parameter with units (`plate_t = 6 mm`, `hole_d = 9 mm`). Derived values are expressions (`flange_w = 4 * hole_d`). This makes sweeps and redesign cheap.
- Build in a few `batch` calls and check each stage with `measure` / `expect` (volume, bounding box, mass). A step that "succeeds" with wrong geometry is the common failure.
- Assign the real material so mass properties are meaningful.
- Assemblies: use joints, run interference checks and motion studies through the full range of motion.
- Sheet metal: use the sheet-metal features so flat patterns come out right.
- Save the JSON command script in `03-model/` — it is text, so Git shows exactly what changed between versions ("plate_t 6 → 8 mm"). Also save the `.sc` design and export STEP for FEA, drawings and outsourcing.

## Known gaps (as of late 2026)

- No FEA → use the Gmsh + CalculiX pipeline (analysis.md).
- Drawings not released yet (only DXF of the current view) → FreeCAD TechDraw from STEP (drawings.md). Switch to native drawings when available.
- No CAM.
