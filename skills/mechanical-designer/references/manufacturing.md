# Manufacturing: fit the design to the workshop (step 4)

## Route every part

For each part write the route in `06-manufacturing/routes.md`: part → stock → machine → operations → setups → inspection. Example: "base plate: 8 mm S275 plate → plasma cut → drill press, 4 × Ø9 → deburr → caliper check".

If a part fits no machine in the profile, in this order:
1. Redesign so it fits (preferred).
2. Split it into parts that fit.
3. Outsource it — list it in `06-manufacturing/outsource.md` with the reason and the in-house alternative that was tried.

Report the % of parts made in-house. Between equivalent options, prefer fewer different machines and fewer setups.

## Process rules of thumb (verify against the actual machine and material)

**Turning**: keep length/diameter < ~4 unsupported (use tailstock or steady beyond); standard thread pitches; relief grooves at thread ends and shoulders; avoid internal features the boring bar cannot reach.

**Milling**: internal vertical corners have a radius ≥ tool radius — design it in; pocket depth ≲ 3–4× tool diameter; fewer setups by putting features on as few faces as possible; avoid thin walls that chatter.

**Drilling/tapping**: standard drill sizes; blind tapped holes need extra drill depth; drill on flat surfaces perpendicular to the bit; tap drill per thread table.

**Sheet metal**: inside bend radius ≥ material minimum (≈ 1× t for mild steel, more for aluminium alloys and stainless — check); holes ≥ ~2 t + bend radius from a bend line; flange length ≥ ~4 t; add bend reliefs at corners; keep one thickness across the part family.

**Cutting (laser/plasma/oxy)**: plasma has kerf taper and heat-affected edges — not for precision holes (drill them after); minimum hole ≈ thickness for plasma.

**Welding**: choose the process the workshop and operator master (MIG/MAG, TIG — AC needed for aluminium, SMAW/stick); design for access; minimize weld volume and distortion (balanced welds, fixtures); keep welds out of max-fatigue zones; specify weld size; avoid welding galvanized parts without fume control.

**3D printing (FDM)**: anisotropic — load along layers, not across; walls in multiples of nozzle width; avoid unsupported overhangs > 45°; heat-set inserts for repeated screws.

**Measurement**: the finest tolerance you specify must be checkable with the instruments in the profile (caliper ≈ ±0.02–0.05 mm, micrometer ≈ ±0.005 mm).

## Accelerate the cycle

Fast prototypes (print, wood, cardboard), fewest setups, shortest routes, and a parametric model that updates in minutes. Automate (jigs, fixtures, CNC programs, scripts) only after the design is stable.
