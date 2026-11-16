# Simplicity: delete, then standardize (step 2)

## The simplicity ladder

For each function, take the first rung that works:

0. Buy a product that already solves the whole problem (see references/process/existing-solutions.md).
1. Delete the function — is it really needed? Who owns it?
2. Let an existing part do it (combine functions).
3. A catalog part (off-the-shelf, locally available).
4. A flat part (laser/plasma/waterjet cut, or sawn bar).
5. A bent or printed part.
6. A machined part.
7. An assembly of several parts.

Also consider compliant (flexure) mechanisms (Howell): one elastic part can replace hinge + spring + pin.

## Questions that delete parts (Boothroyd–Dewhurst)

A part may stay as a separate part only if at least one is true:
- it moves relative to the parts it touches;
- it must be a different material (insulation, wear, corrosion);
- it must be separate for assembly, disassembly or maintenance.
Otherwise, try to merge it.

## Deletion log and the 10% rule

Keep `02-concept/deleted.md`: what was deleted, why, and whether it had to come back. If almost nothing comes back, you were too timid. Safety factors, regulations and protections against serious failures are only deleted with evidence.

## First principles and follow the load

- Start from physics: the load, its path, the material — not "how it's usually done".
- Draw the load path from application point to support first. A direct path is stiffer, lighter and simpler; detours create bending and stress concentrations.
- Prefer exact constraint (Blanding): constrain each degree of freedom once. Over-constraint demands tight tolerances or forced fits.
- Idiot index = cost of finished part / cost of its raw material. A high index means the process is complicating the part; ask why.

## Standardization (ask the user before applying)

| Strategy | Example |
|---|---|
| Few fastener types | 5 references instead of 50; ideally one diameter in 2–3 lengths |
| One part, used differently | one bracket that works left and right by rotation instead of mirrored pair |
| Same stock | one tube size, one sheet thickness — one purchase, less scrap |
| Repeated features | same hole diameters and bend radii — one drill, one die |
| Few assembly tools | everything assembled with one or two wrenches |
| Common commercial parts | bearings, bushings, profiles available locally |

Report: total parts vs unique parts, and fastener references ("40 parts, 9 unique; 2 fastener references"). When you spot near-duplicates, ask: "I found 3 almost identical brackets — unify them?"

## Simplicity score (for comparing alternatives)

Count: parts, unique parts, processes, machines, setups, critical tolerances, % catalog parts, redundant constraints, outsourced parts. Lower is simpler. Use it inside the decision matrix, not instead of it.
