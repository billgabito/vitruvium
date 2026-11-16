# Parts breakdown: IDs, names and the parts list

Every part of a design gets an **ID**, a **name** and a **reason to exist** from the first iteration, and a single parts list (`parts.json`) is the master used everywhere: the viewer (parts list, ID labels in 3D, exploded view), manufacturing routes, drawings and bill of materials, the auditor and the changelog counts.

## ID convention

`<code>-<two-digit number>`, numbered in order of appearance and never reused (a deleted part keeps its number retired):

| Code | Category | Examples |
|---|---|---|
| P | Fabricated part (made in the workshop or outsourced) | base plate, bracket, cover |
| SH | Shaft, axle, pin | drive shaft, hinge pin |
| BR | Bearing, bushing | 6204-2RS, bronze bushing |
| FS | Fastener | screw ISO 4762 M6×20, nut, washer, rivet |
| SP | Spring | compression spring |
| SE | Seal, gasket, O-ring | O-ring 30×2 NBR |
| G | Gear, pulley, sprocket, wheel | pulley T5 20T |
| MO | Motor, actuator | gearmotor 24 V |
| SN | Sensor, switch, electronics | limit switch, proximity sensor, encoder, PCB |
| CP | Other commercial part | linear guide, handle, cable gland |
| AS | Sub-assembly | lid assembly |

Identical parts share one ID with a quantity (eight identical screws = `FS-01`, qty 8).

## The name says what the part is

The ID alone is not enough: the `name` must tell anyone what the part is, with its key specification, and the full designation goes in `spec` / `standard`:

| ID | Name (what it is) | spec / standard |
|---|---|---|
| FS-01 | Socket head cap screw M5×12 | ISO 4762 M5×12 8.8 zinc |
| FS-02 | Hex nut M5 | ISO 4032 M5 8 |
| BR-01 | Deep groove ball bearing 6200-2RS | SKF 6200-2RS1 (10×30×9) |
| P-03 | L-shaped lever, 6 mm plate | drawing P-03 |
| SH-01 | Hinge pin Ø10 × 60 | C45 Ø10 h9 |

In the viewer, the systems panel and the parts list are organized as an expanded tree by group — fasteners together, bearings together, sensors together — each group with its own show/hide switch.

Never "part 1", "bracket" or "screw" alone. In the viewer, clicking a part (in 3D, on its ID label or in the parts list) opens a detail card at the top with ID, name, type, specification, material, quantity, function and requirements, why it exists, features with their reasons, source, route and drawing.

## Every part must justify its existence

Nothing is in the design "because": each part carries
- `function` — what it does, verb + noun ("locates the lid", "transmits torque to the wheel");
- `requirements` — the requirement IDs it serves (`R1`, `R4`…); a part that serves none is a deletion candidate;
- `why` — why it must be a **separate** part and cannot be deleted or merged (Boothroyd's test: it moves relative to its neighbours, it must be a different material, or it must be separate for assembly or maintenance — or another stated reason);
- `features` (optional but expected for fabricated parts) — the reason for each non-obvious feature: `{"feature": "R5 fillet at the bend", "why": "Kt 2.8 → 1.6, fatigue FS 1.3 → 2.1"}`. Holes, slots, fillets, chamfers, thickness, tolerances tighter than general — each has a reason.

Changes follow the same rule: every alteration between versions is logged with its why (`log_iteration.py --why`, mandatory). `log_iteration.py` warns about parts without `function` or `why` and counts them as `unjustified_parts`; the independent auditor treats any unjustified part or feature as a finding.

## parts.json

```json
[
  {"id": "P-01", "name": "Base plate", "type": "fabricated", "material": "S275 8 mm", "qty": 1, "source": "make", "route": "plasma → drill",
   "function": "carries the motor and transfers its load to the frame", "requirements": ["R1", "R2"],
   "why": "different material and thickness than the frame; must be removable for motor service",
   "features": [{"feature": "4 slotted holes 9×20", "why": "belt tension adjustment ±10 mm (R5)"}]},
  {"id": "SH-01", "name": "Hinge pin", "type": "shaft", "material": "C45 Ø10 h9", "qty": 1, "source": "make", "route": "lathe",
   "function": "guides the lid rotation", "requirements": ["R3"], "why": "the lid rotates relative to the base: needs a separate pivot"},
  {"id": "BR-01", "name": "Deep groove ball bearing", "type": "bearing", "spec": "6200-2RS", "qty": 2, "source": "buy", "supplier": "SKF / local",
   "function": "supports the drive shaft with low friction", "requirements": ["R4"], "why": "rotating interface; catalog part beats a machined bushing at 1500 rpm"},
  {"id": "FS-01", "name": "Socket head cap screw", "type": "fastener", "standard": "ISO 4762 M6×20 8.8 zinc", "qty": 8, "source": "buy",
   "function": "clamps the base plate to the frame", "requirements": ["R2"], "why": "plate must be removable for service (no weld); one screw size for the whole assembly"},
  {"id": "P-02", "name": "Lid", "type": "fabricated", "material": "AlMg3 3 mm", "qty": 1, "source": "make", "explode": [0, 0, 1],
   "function": "closes the enclosure (IP54)", "requirements": ["R6"], "why": "must open for access: moves relative to the base"}
]
```

Optional fields: `group` (to group by functional system instead of by category, e.g. "Drive", "Lid", "Electrical" — otherwise the viewer groups by ID code: fabricated parts, shafts, bearings, gears, springs, seals, fasteners, motors, sensors, commercial parts), `spec` / `standard` (catalog number or standard designation), `supplier`, `route`, `mass_kg`, `drawing`, `explode` (direction for the exploded view; default: away from the assembly centre).

## Visual fidelity: parts look like what they are (medium–high detail)

The user validates what they see, so every part must be recognizable for what it is. Not photorealism — the characteristic geometry:

| Part | Must show | May simplify |
|---|---|---|
| Spring | the helix: wire diameter, coil count, pitch, closed/ground ends | — |
| Screw / bolt | head shape and drive (hex socket, hex head, Phillips), shank, length | thread as cosmetic (plain cylinder at major diameter) |
| Nut / washer | hexagon with chamfers / ring with real inner and outer diameter | thread |
| Bearing | inner and outer rings, seals or shields, width | balls and cage |
| Gear / pulley / sprocket | teeth (count and module or pitch), hub, bore, keyway | exact involute (approximate profile is fine) |
| Belt / chain | the band or the links following the path | individual teeth or rollers on long runs |
| Shaft | steps, shoulders, chamfers, keyways, grooves for retaining rings | — |
| Seal / O-ring | the toroid or lip profile at its real section | — |
| Motor / sensor / commercial part | the manufacturer's STEP model when available (catalog-search.md); otherwise the real envelope with its mounting features and connector | internal detail |
| Welds | weld beads where they are | — |

**Never** a cylinder for a spring, a screw or a nut, a disc for a gear, or a box for a motor when its real shape is known. Prefer the manufacturer's STEP for catalog parts; model fabricated parts with their fillets, chamfers, holes and bends. In SolidCraft use the matching features (coil for springs, modelled or cosmetic threads, sheet metal for bent parts). The auditor checks this as part of a faithful presentation.

Export for the viewer with fine tessellation (glTF preferred; chord tolerance about 0.05 mm, facet angle about 10°) so round parts look round.

## Linking parts to the 3D view

Export each part from SolidCraft with its **ID as the file name** (`03-model/current/P-01.stl`, `FS-01.stl`…) or as the glTF node name. The viewer then labels it with its ID in 3D, lets the user click it in the parts list to isolate it, and moves it in the exploded view. Put `parts.json` in `03-model/current/` for the live copy and pass `--parts` to `log_iteration.py` for versions.

## Rules

- No `function` / `why` → not finished. If you cannot state why a part exists, try to delete it (references/process/simplicity.md).
- Keep IDs stable across versions; the changelog says when a part is added, deleted (ID retired) or merged.
- Total vs unique parts and the number of fastener references come from this list (simplicity metrics).
- Use the same IDs in manufacturing routes, drawings (title blocks, balloons) and the bill of materials.
