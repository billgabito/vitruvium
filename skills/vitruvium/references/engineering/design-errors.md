# Design-error catalog

Review every design against this list before delivery, and again in audits. Each entry: what to look for → why it fails → fix. When a project reveals a new error, add it to the user's local lessons file (`~/.vitruvium/lessons.md`); generic lessons can be proposed for this catalog.

## Stress and fatigue
1. Sharp internal corner in a loaded zone → stress concentration, fatigue crack start → add a fillet (r ≥ thickness/2 where possible), move the feature out of the high-stress region.
2. Hole, notch or keyway at the point of max bending → Kt multiplies peak stress → relocate to the neutral axis or a low-moment zone.
3. Abrupt section change on a shaft → shoulder Kt 2–3 → generous fillet, relief groove, gradual taper.
4. Weld at the point of max fatigue stress / weld toe across the stress flow → weld fatigue is far below base metal → move the weld to a low-stress zone, use continuous welds, grind toes, or bolt instead.
5. Static check only on a cyclically loaded part → fails in fatigue below yield → always ask about cycles; run Goodman.
6. Slender member in compression without buckling check → sudden collapse → Euler/Johnson check, shorten, brace, use a closed section.
7. Thin wall under compression or shear → local buckling → stiffeners, thicker wall, or ribs.
8. Point loads and knife edges in reality (not just in FEA) → local yielding, indentation → spread loads with washers, pads, larger contact areas.

## Joints and fasteners
9. Bolt carrying shear by bending through a clearance hole → fatigue, ovalization → preload for friction grip, or fitted bolts/dowels for location.
10. Insufficient preload / no locking in vibration → self-loosening → correct torque, adequate grip length, prevailing-torque nuts or wedge washers.
11. Repeatedly removed screw tapped directly into aluminium or plastic → thread strip → threaded inserts or through-bolts with nuts.
12. Short thread engagement in soft material → stripping → engagement ≥ 1.5–2× d in aluminium.
13. Too many fastener types → assembly errors, stock cost → standardize.
14. Welding hardened, galvanized or dissimilar materials without procedure → cracks, fumes, porosity → choose weldable grades, remove coatings, specify procedure.

## Fits, tolerances, constraint
15. Over-constrained parts (more locating features than DOF) → binding, forced assembly, tight tolerances → exact constraint: locate each DOF once.
16. Tolerance tighter than the function needs → cost and rework → general tolerance (ISO 2768-m) except functional features.
17. Tolerance the workshop cannot measure → unverifiable part → match tolerances to the measuring tools in the profile.
18. Unchecked tolerance stack → parts don't assemble → worst-case/RSS stack on critical chains.
19. Ignoring thermal expansion between materials → seizure or looseness → compute clearances at temperature extremes.

## Materials and environment
20. Dissimilar metals in contact with moisture → galvanic corrosion → isolate, same material, coatings.
21. Plastics under sustained load without creep check → slow deformation → derate, metal insert, or metal part.
22. Material chosen by habit, not by performance index → heavy or expensive → Ashby index for the governing requirement.
23. Unavailable material or stock size locally → delays → check local suppliers early.

## Manufacturing
24. Feature the workshop cannot make (deep pocket, internal sharp corner from milling, bend too close to a hole) → outsourcing or redesign late → check against the workshop profile during design.
25. Bend radius below material minimum / hole too close to a bend → cracking, distortion → follow sheet metal rules (references/manufacturing/manufacturing.md).
26. Part that can be assembled the wrong way → errors → make it symmetric or obviously asymmetric (poka-yoke).
27. No access for tools, wrenches, welding torch → can't build or maintain → check tool access in the model.
28. Mirrored left/right parts when one symmetric part would do → double inventory → unify.

## Assembly
29. Part trapped in a closed cavity (spring, nut, magnet, seal inside a housing with no opening) → cannot be assembled → split the housing, add a cover or an opening.
30. Insertion path blocked by a part installed earlier → impossible sequence → reorder, change the insertion direction or split the blocking part.
31. Fastener without tool access or wrench swing room → cannot be tightened → move it, use a different head or drive, or change the joint.
32. Bearing or shaft that must pass through a smaller bore → cannot be assembled → step the diameters the right way.
33. Press fit without lead-in chamfer or without a press in the workshop → damaged parts → chamfer, fit class, or a clearance fit with a retainer.
34. Wear part that can only be replaced by destroying others → unserviceable → make it removable.
35. O-ring or gasket cut when the part slides over an edge → leak → lead-in chamfer, no sharp edges over the seal.

## Sealing and ingress protection
36. Sealing added at the end, or more openings than needed → leaks → decide the IP rating in step 1; minimize joints and penetrations.
37. Gasket without compression limit, or compression checked only at nominal → crushed or loose gasket → compression limiters; check compression at tolerance extremes.
38. Fully sealed box with temperature swings and no vent or drain → condensation inside → membrane vent and drain at the lowest point.
39. Cable or shaft entries without rated glands/seals → the rating is only as good as the weakest entry → rated glands, lip seals.

## Process
40. Optimizing or simulating before deleting → polishing waste → follow the 5 steps in order.
41. Requirements added after freeze without impact analysis → schedule and cost creep → change control.
42. Testing only at the end → expensive surprises → risk prototype early.
43. Developing new technology when a catalog part exists → cost and risk → use proven parts.
