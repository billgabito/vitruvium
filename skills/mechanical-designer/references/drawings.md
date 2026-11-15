# Manufacturing drawings

A design is not finished until someone else can build it from the drawing: an outside shop, a lathe operator, or anyone who reads drawings.

## Standard

ISO, first-angle projection by default (ISO 128 views and lines, ISO 129-1 dimensioning, ISO 2768 general tolerances, ISO 286 fits, ISO 1101 geometric tolerances, ISO 21920 surface texture, ISO 7200 title block). ASME Y14.5, third-angle, when the user or client requires it. State the projection symbol on every sheet.

## Every part drawing contains

- Views needed to define the part, plus sections and details where hidden features matter; no redundant views.
- Functional dimensions from the datums that matter for assembly, not from wherever is convenient to draw. No double dimensioning.
- General tolerance in the title block (e.g. ISO 2768-m). Tight tolerances and fits (e.g. H7/g6) only where function requires and the workshop can measure.
- Geometric tolerances only when size tolerances cannot control the function.
- Material and condition, heat treatment, surface finish, coating, quantity, edge break note ("break sharp edges 0.5 × 45°").
- Title block: part number, name, revision, scale, units, author, date, projection, sheet.

Assemblies: assembly drawing, bill of materials (including commercial parts with manufacturer part numbers), exploded view if useful. Sheet metal: flat pattern with bend lines, direction and inside radius. Weldments: weld symbols per ISO 2553 (or AWS A2.4).

## Delivery package (per part)

PDF drawing + DXF for cutting (flat parts) + STEP model. Put released packages in `deliveries/vX.Y/`.

## Tooling

SolidCraft drawings are not released yet. Bridge: export STEP → FreeCAD TechDraw run headless with `freecadcmd` and a Python script (views, dimensions, title block) → PDF/DXF. Automatic dimension placement usually needs cleanup: render the sheet, look at it, fix overlaps before delivery. If FreeCAD is unavailable, deliver a dimension table (feature, nominal, tolerance, datum) plus a SolidCraft DXF view, and say the drawing is not formal.
