# Existing solutions first: buy, adapt or design

The simplest design is the one you do not have to make. Right after the black-box sheet is confirmed — before deleting, sketching or calculating — find out whether the problem is already solved, on the market or as a known technical solution. Then let the user choose the starting point.

## What to look for

| Kind | Examples | Where |
|---|---|---|
| **Complete product** that solves the whole problem | a ready-made motor base, a commercial clamp, a gearmotor with mounting kit | manufacturer catalogs, industrial suppliers (e.g. McMaster-Carr, Misumi, RS, local distributors), marketplaces |
| **Standard module** that solves most of it | linear guides, slewing rings, hinges, latches, enclosures, adjustable feet, tensioners | component manufacturers' catalogs |
| **Known technical solution** (a mechanism or principle) | toggle clamp, four-bar linkage, Geneva drive, flexure hinge, scissor lift | mechanism handbooks, textbooks, patents as technical literature |
| **Analogous solution from another industry** | a bicycle quick-release for a fixture, an agricultural hitch for a trailer | search by function ("quick release clamp", "self-locking hinge"), TRIZ principles |
| **Open hardware designs** | published brackets, jigs, printable parts | GrabCAD, Printables, Thingiverse, OpenBuilds — check the license before reuse |

Search by **function**, not by the user's name for the part ("hold a motor and tension a belt", not "motor bracket"). Prefer suppliers the user can actually buy from locally.

## Borrow from other industries (transfer of solutions)

The best idea often lives in a different industry, solving the same function at another scale or for another purpose. Look deliberately outside the user's field:

1. **Abstract the function.** Strip the context: verb + noun + physical principle ("hold a load against vibration", "convert rotation into a short linear stroke", "release quickly without tools", "keep a seal under thermal cycling").
2. **Search across lenses.** Ask "who else has to do this?":

| Lens | Typical strengths worth borrowing |
|---|---|
| Bicycles and motorsport | quick releases, light tubes, tensioners, cam locks |
| Agriculture | rugged, field-repairable, weld-and-bolt simplicity, hitches |
| Automotive | mass-produced cheap mechanisms, latches, bushings, seals |
| Aerospace | weight-efficient structures, fail-safe fasteners, inspection access |
| Furniture and folding products | hinges, slides, flat-pack joints, knock-down fittings |
| Medical devices and lab equipment | precision with simple parts, cleanable designs, flexures |
| Packaging and food machinery | washdown design, tool-less changeover |
| Construction and scaffolding | modular clamps, standard tube systems, adjustability |
| Marine | corrosion resistance, sealing, galvanic isolation |
| Robotics and automation | compact transmissions, standard actuators and guides |
| Toys and consumer products | snap-fits, living hinges, one-piece moulded mechanisms |
| Nature (biomimicry) | compliant joints, efficient load paths, self-cleaning surfaces |

   Use TRIZ's 40 inventive principles as a second prompt (segmentation, nesting, the other way round, prior action…) when the obvious lenses give nothing.
3. **Evaluate viability against the user's requirements** — an idea from another industry is a hypothesis, not a solution. Check each candidate:

| Check | Question |
|---|---|
| Function | Does it really perform the same function, or only look similar? |
| Scale and loads | Does it survive the user's loads, speeds and cycles? Scaling changes stresses (area grows with L², mass with L³). |
| Environment | Temperature, water, dust, chemicals, UV, cleanliness requirements |
| Manufacturability | Can the user's workshop make or buy it? Mass-production solutions (moulding, stamping) may not transfer to one-off fabrication. |
| Cost and availability | Can the part or its equivalent be bought locally? |
| Simplicity | Does it reduce parts and processes, or add a clever complication? |
| Standards and safety | Does the original rely on a certification or context that does not carry over? |

   Verdict per idea: **viable as is**, **viable with adaptation** (say what changes), or **not viable** (say why — this is useful knowledge too).

4. **Present the transferred ideas** in the same table as the market findings, with a column "origin industry" and the viability verdict. The best transferred idea usually becomes one of the A/B/C alternatives.

## Keep it short

Time-box the search (a few targeted searches, not a market study). If nothing reasonable appears quickly, say so and move on. For a trivial part (a spacer, a simple plate), skip it and say why.

## Present what you found

| # | Solution | Origin industry | Source (link, date) | Price / lead time | Covers requirements | Gaps | Workshop work needed | Viability |
|---|---|---|---|---|---|---|---|---|

Then give three starting points, with your recommendation first, and ask the user to choose (question tool):

1. **Buy** — a product covers the requirements. Fastest and usually simplest; the design work becomes selection, mounting and verification (check its ratings against the loads and environment).
2. **Adapt** — buy a standard product or module and design only the interface or the missing part. Usually the best balance.
3. **Design from scratch** — nothing fits, it is too expensive, unavailable locally, or the user wants to own the design. Use what was found as inspiration and benchmark (dimensions, mechanisms, price to beat).

Record the choice and the reason in `02-concept/decision.md`, and keep the search table in `references/` of the project. In design-from-scratch, the commercial options remain useful as the baseline in the A/B/C matrix ("our design must beat this product on cost, simplicity or fit").

## Intellectual property and licenses (be honest, not legal)

- Learning from a product or a published mechanism is normal engineering. Copying a protected design is not.
- Open designs carry licenses (CC BY, CC BY-NC, GPL…); state the license and whether commercial use is allowed.
- If a very similar, recent and patented solution shows up and the user plans to sell the product, mention that a patent check (freedom to operate) may be needed. This is a flag, not legal advice.
