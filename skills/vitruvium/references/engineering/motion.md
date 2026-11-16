# Moving parts: animation in the viewer

When a design has moving parts, the user must see **which parts move and how** — not read it. Describe the motion in a `motion.json` next to the model and the viewer animates it: play/pause, a position slider, speed, the moving parts highlighted, their joint axes drawn, and a list of every moving part with its joint type and range.

## Where it lives

- Working copy: `03-model/current/motion.json` (or `03-model/motion.json`) — the live viewer picks it up like the geometry.
- Versions: pass `--motion <file>` to `log_iteration.py`.

Take axes, origins and ranges from the joints defined in SolidCraft (the same numbers that drive its motion study), so the animation and the CAD agree. Coordinates are in **mm**, in the model's coordinate system; angles in **degrees**. `part` is the name of a system in the viewer (the model file name without extension, or the glTF node name).

## Format

```json
{
  "joints": [
    {"part": "lid",    "type": "revolute",  "axis": [0, 1, 0], "origin": [0, 0, 40], "range": [0, 110], "label": "Lid hinge"},
    {"part": "slider", "type": "prismatic", "axis": [1, 0, 0], "range": [0, 60], "label": "Linear guide"},
    {"part": "gear2",  "type": "revolute",  "axis": [0, 0, 1], "origin": [80, 0, 0], "follows": "gear1", "ratio": -0.5}
  ],
  "keyframes": {
    "rocker": {"t": [0, 0.5, 1], "translate": [[0,0,0],[0,4,2],[0,0,0]], "rotate": [[0,0,1,0],[0,0,1,25],[0,0,1,0]], "origin": [120, 0, 0]}
  },
  "duration_s": 4,
  "loop": "pingpong"
}
```

- `revolute`: rotation about `axis` through `origin`, from `range[0]` to `range[1]` degrees.
- `prismatic`: translation along `axis`, from `range[0]` to `range[1]` mm.
- `follows` + `ratio` (+ optional `offset`): a part driven by another (gears, belts, coupled levers). `ratio` multiplies the driver's value; negative reverses.
- `spring`: an elastic part that **deforms** with the mechanism. It stretches or compresses between a fixed `anchor` point and an `attach.point` carried by another part (`attach.part`), and turns to follow the line between them. Give the physics so the viewer can show it: `k` (N/mm), `free_length` and `solid_length` (mm). The viewer shows the live length and force (F = k·(free length − length), compression or tension) and flags **coil bind** in red when the length drops below the solid length. Model the spring at the length it has in the assembled pose (pose 0).
  `{"part": "SP-01", "type": "spring", "anchor": [70, 20, 6], "attach": {"part": "P-02", "point": [70, 20, 30]}, "k": 2.0, "free_length": 28, "solid_length": 12}`
- `keyframes`: for closed-loop mechanisms (four-bar linkages, cams, toggles) whose motion a simple joint cannot express. Sample the SolidCraft motion study at a few instants (`t` from 0 to 1) and give each part's translation (mm) and rotation (axis x, y, z and angle in degrees) about `origin`; the viewer interpolates.
- `loop`: `pingpong` (back and forth, default) or `cycle` (0 → 1 and restart, for continuous rotation).
- `allowed_contacts`: pairs of parts that touch by design (a pin in its bore, a spring seated on its base, a part resting on a stop): `[["SP-01", "P-01"], ["SH-01", "P-02"]]`. Every other contact is reported as a collision. A spring never collides with the part that carries its free end.

## Physics and collisions — the animation must be real

- Motion follows the real kinematics: the same axes, origins, ranges and ratios as the SolidCraft joints; closed loops from the motion study, not invented paths.
- Elastic parts deform (springs compress and stretch); nothing that should deform is moved as a rigid block, and nothing rigid is stretched.
- **Collisions are checked between real part geometry** while the animation plays: colliding parts turn red and the panel names the pair. The button **"Check collisions over full range"** samples 72 positions and reports every collision and coil bind with the part of the range where it happens.
- The viewer check is the visual confirmation; the authoritative check stays in SolidCraft (motion study + interference). Both must agree before the motion is presented as valid.

## Rules

- Every moving part appears in the animation; parts that do not move stay grey-transparent while playing so the motion reads clearly.
- Check interference through the full range in SolidCraft and with the viewer's full-range check before showing the animation as valid; a collision or coil bind is a design error — say where and at what position, and go back to the model.
- If the motion is approximate (e.g. a closed loop sampled with few keyframes), say so.
