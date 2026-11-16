# Assembly: if it cannot be assembled, it is wrong

A design that cannot be put together — or taken apart where it must be — is incorrect, however good it looks on paper. A spring inside a fully closed part, a screw no wrench can reach, a bearing that has to pass through a smaller bore: these are design errors, not workshop problems. Assembly is designed **with** the parts, from the first iteration, and checked in every iteration by the designer and by the auditor.

## The assembly sequence (`assembly.json`)

Every design with more than one part has a written sequence: which part goes in, in what order, from which direction, how it is held, with which tool.

```json
{
  "steps": [
    {"n": 1, "parts": ["P-01"], "action": "place", "note": "Base plate on the bench, slots up"},
    {"n": 2, "parts": ["BR-01"], "action": "press", "direction": [0, 0, -1], "distance": 30,
     "tool": "arbor press + Ø30 drift", "note": "Press bearing into P-01 bore until it seats on the shoulder",
     "check": {"path_clear": true, "tool_access": true, "evidence": "SolidCraft interference at 10 positions: none"}},
    {"n": 3, "parts": ["FS-01"], "qty": 4, "action": "fasten", "direction": [0, 0, -1], "distance": 25,
     "tool": "4 mm hex key", "torque": "5.9 N·m", "note": "Screws M5×12 through P-02 into P-01",
     "check": {"path_clear": true, "tool_access": true, "evidence": "Ø20 clearance above each screw head for the key"}}
  ],
  "disassembly": "Reverse of steps 3 → 2; BR-01 is a wear part: replaceable without removing P-01 from the frame",
  "method": "insertion paths checked in SolidCraft by moving each part along its direction in 10 steps and running interference"
}
```

- `parts`: IDs from `parts.json`; `direction`: unit vector of the insertion movement (from outside toward the final position); `distance`: approach length in mm (used by the viewer to animate the part flying in).
- `action`: place, insert, press, slide, fasten, weld, bond, clip, adjust.
- `check` is mandatory for every step except the first: whether the path is clear, whether the tool can reach, and the evidence.
- Put it in `03-model/current/assembly.json` (live) and pass `--assembly` to `log_iteration.py` for versions. The viewer plays it step by step.

## What makes a design assemblable (check every iteration)

1. **Every part has a free insertion path** to its final position, at the moment of its step (parts already installed can block later ones). Verify in SolidCraft: move the part along its direction in steps and run interference — the same model, no second geometry.
2. **No trapped parts**: nothing must end up inside a cavity it cannot enter (springs, seals, magnets, nuts inside closed housings). If it must be enclosed, the housing needs a split, a cover or an opening.
3. **Tool access**: wrench, hex key, screwdriver, press drift, welding torch, rivet gun — the tool and the hand fit, with swing room for wrenches.
4. **A feasible order**: the sequence can be followed without removing parts already installed; sub-assemblies are complete units.
5. **Few directions, top-down preferred** (gravity helps); one fastener size and one tool where possible (simplicity.md).
6. **Fits allow assembly**: clearance, transition or press fit chosen on purpose; press fits have a lead-in chamfer and a press available in the workshop; thermal fits have a stated temperature.
7. **Self-locating and error-proof**: chamfers and lead-ins; features that make wrong orientation impossible (poka-yoke) or symmetry that makes it irrelevant.
8. **Disassembly where needed**: wear parts, seals, bearings, batteries, filters and anything serviceable can be removed without destroying other parts; welded or bonded joints only where nothing will ever need to come apart.
9. **Workshop reality**: the assembly can be done with the tools and people in the workshop profile (a two-person lift, a press, a welding positioner).
10. **Sealing during assembly**: gaskets and O-rings are not cut or rolled when the part goes in (lead-ins, no sharp edges over the seal).

A step that fails any of these sends the design back (improvement loops: assembly failure → the model, or → delete/merge parts).

## Showing it

The viewer's **Assembly** panel plays the sequence: installed parts stay, the current part flies in along its insertion direction, future parts are hidden, and the step text (action, tool, torque, note, check) is shown. The user and the auditor see the logic of assembly, not just the final shape.
