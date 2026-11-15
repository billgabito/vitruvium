# Analysis: hand calculation, FEA and interfaces

## Calculation ladder

1. Order of magnitude (free-body diagram, load path, rough section).
2. Closed-form (Beer & Johnston, Shigley, Roark): stresses, deflections, buckling, fatigue.
3. FEA only where geometry defeats closed-form (complex shapes, contact, combined loading).

Rule: if FEA and the hand calc disagree by more than ~15% in a region where the hand calc is valid, suspect the model (boundary conditions, units, mesh), not the hand calc.

## Checklist per part

- Static: von Mises (ductile) or Coulomb-Mohr / max normal (brittle); yield and ultimate.
- Stress concentrations: Kt from Peterson/Pilkey at holes, fillets, keyways, shoulders, weld toes; Kf = 1 + q(Kt − 1) for fatigue.
- Fatigue (Shigley ch. 6): Marin-corrected endurance limit, modified Goodman (or Gerber/ASME elliptic), Miner for variable loading. Weld fatigue uses weld detail categories, not base-metal curves.
- Deflection and stiffness limits (often govern before strength).
- Buckling: Euler / Johnson for columns; plate buckling for thin walls.
- Fracture: brittle materials, low temperature, thick welded sections — consider K_IC.
- Bolted joints: preload, joint stiffness, separation, slip (VDI 2230 approach). Bolts should clamp, carrying shear by friction where possible.
- Safety factor: state it and why (Shigley's uncertainty-based guidance, typically 1.5–3; codes override).

## FEA pipeline (STEP → Gmsh → CalculiX)

Use the bundled script instead of writing one each time:

```
python3 scripts/fea.py part.step --out 05-simulation/v0.3/size2 --E 210000 --nu 0.3 --size 2 --yield 250 \
    --fix "xmin ymin zmin xmax ymax zmax" --load "xmin ymin zmin xmax ymax zmax Fx Fy Fz"
```

Units mm, N, MPa. Supports and loads are selected by bounding boxes in model coordinates (get them from SolidCraft `measure`); a load is the total force spread over the nodes in its box. Run it at three element sizes for the convergence study. It writes `results.json` and `summary.md` (and stress/displacement PNGs when ccx2paraview and PyVista are installed). Validated on a cantilever: tip deflection within 0.5% of beam theory; the root stress keeps rising with refinement because of the fixed-edge singularity — exactly the behaviour described in step 5 below.

The steps the script follows, and what to check:

1. Export STEP from SolidCraft. Defeature only what does not affect the result (cosmetic fillets far from stress paths), and say what you removed.
2. Mesh with Gmsh: second-order tetrahedra (C3D10), refined at stress raisers; export directly to CalculiX/Abaqus format (`.inp`).
3. CalculiX input (.inp): material (E, ν, density), boundary conditions that match reality (avoid over-constraining — fixed faces stiffen and create false peaks), loads distributed over realistic areas.
4. Analyses: static linear; modal (*FREQUENCY) when there is vibration or rotating equipment; linear buckling (*BUCKLE) for slender or thin parts; contact or nonlinear only when needed.
5. Convergence: at least three mesh densities; peak stress of interest changes < 5% between the last two. Ignore singularities (sharp re-entrant corners, point loads, fixed edges) — they never converge; report stress at a distance or model the real fillet.
6. Results: read numbers from the `.dat` file (*EL PRINT / *NODE PRINT); for images convert `.frd` → `.vtu` with `ccx2paraview` and render von Mises stress and displacement with PyVista (off-screen PNG).
7. Report: model assumptions, mesh study, max stress vs allowable, deflection, safety factor, comparison with hand calc, images of stress and displacement, what was not modelled.

Tools, sources and install commands: tools-setup.md (run `scripts/check_tools.sh`).

## Interfaces between parts (systems)

Check every pair of parts that touch:

| Phenomenon | How |
|---|---|
| Interference and clearance through full motion | SolidCraft interference + motion study |
| Contact stress (rollers, pins, cams, gears) | Hertz; CalculiX contact if needed |
| Wear | Archard; material pairing, hardness difference, lubrication, PV limits for bushings |
| Fretting | small relative slip in fits and bolted joints — increase clamp, reduce slip |
| Galvanic corrosion | galvanic series; isolate dissimilar metals (e.g. stainless + aluminium in wet environments) |
| Thermal expansion mismatch | clearance at min and max temperature |
| Tolerance stack-up | worst case and RSS statistical |
| Fatigue at the joint | weld toes, threads, holes — Kf and detail categories |
