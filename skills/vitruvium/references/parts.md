# Parts breakdown: IDs, names and the parts list

Every part of a design gets an **ID** and a **name** from the first iteration, and a single parts list (`parts.json`) is the master used everywhere: the viewer (parts list, ID labels in 3D, exploded view), manufacturing routes, drawings and bill of materials, the auditor and the changelog counts.

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
| CP | Other commercial part | linear guide, handle, cable gland |
| AS | Sub-assembly | lid assembly |

Identical parts share one ID with a quantity (eight identical screws = `FS-01`, qty 8).

## parts.json

```json
[
  {"id": "P-01", "name": "Base plate", "type": "fabricated", "material": "S275 8 mm", "qty": 1, "source": "make", "route": "plasma → drill"},
  {"id": "SH-01", "name": "Hinge pin", "type": "shaft", "material": "C45 Ø10 h9", "qty": 1, "source": "make", "route": "lathe"},
  {"id": "BR-01", "name": "Deep groove ball bearing", "type": "bearing", "spec": "6200-2RS", "qty": 2, "source": "buy", "supplier": "SKF / local"},
  {"id": "FS-01", "name": "Socket head cap screw", "type": "fastener", "standard": "ISO 4762 M6×20 8.8 zinc", "qty": 8, "source": "buy"},
  {"id": "P-02", "name": "Lid", "type": "fabricated", "material": "AlMg3 3 mm", "qty": 1, "source": "make", "explode": [0, 0, 1]}
]
```

Optional fields: `spec` / `standard` (catalog number or standard designation), `supplier`, `route`, `mass_kg`, `drawing`, `explode` (direction for the exploded view; default: away from the assembly centre).

## Linking parts to the 3D view

Export each part from SolidCraft with its **ID as the file name** (`03-model/current/P-01.stl`, `FS-01.stl`…) or as the glTF node name. The viewer then labels it with its ID in 3D, lets the user click it in the parts list to isolate it, and moves it in the exploded view. Put `parts.json` in `03-model/current/` for the live copy and pass `--parts` to `log_iteration.py` for versions.

## Rules

- Keep IDs stable across versions; the changelog says when a part is added, deleted (ID retired) or merged.
- Total vs unique parts and the number of fastener references come from this list (simplicity metrics).
- Use the same IDs in manufacturing routes, drawings (title blocks, balloons) and the bill of materials.
