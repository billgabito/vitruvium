# Ingress protection (IP code, IEC 60529)

Decide in step 1 whether the part or assembly must keep out dust or water. If it does, the required IP rating becomes a requirement with an owner, and it shapes the design from the concept stage — sealing added at the end is expensive and leaks.

## Does it need protection? Ask (as part of the environment question)

- Does it house electronics, bearings, lubricant, or anything damaged by dust or water?
- Where does it work: indoors dry, outdoors, washdown (food, pharma), dusty (mining, wood, cement), submerged?
- Is a rating required by a client, a standard or a certification?

If nothing inside is sensitive, no rating is needed — do not add seals nobody needs (simplicity first).

## The code: IP + first digit (solids) + second digit (liquids)

| 1st | Solids | 2nd | Liquids |
|---|---|---|---|
| 0 | none | 0 | none |
| 1 | > 50 mm (hand) | 1 | vertical drips |
| 2 | > 12.5 mm (finger) | 2 | drips at 15° tilt |
| 3 | > 2.5 mm (tools) | 3 | spray up to 60° |
| 4 | > 1 mm (wires) | 4 | splashing from any direction |
| 5 | dust-protected (limited ingress, no harm) | 5 | water jets (6.3 mm nozzle) |
| 6 | dust-tight | 6 | powerful jets (12.5 mm nozzle) |
| | | 7 | temporary immersion (up to 1 m, 30 min) |
| | | 8 | continuous immersion (beyond IP67, conditions set by the manufacturer) |
| | | 9K | high-pressure, high-temperature washdown (ISO 20653 / IEC 60529 amendment) |

"X" means not tested for that digit (e.g. IPX4). Ratings are not cumulative beyond 6: IP67 does not imply IP66 — state both if both are needed (IP66/IP67).

## Typical choices

| Environment | Usual rating |
|---|---|
| Indoor, dry, protected from touch | IP20–IP40 |
| Indoor workshop, some dust and splashes | IP54 |
| Outdoor, rain, hose cleaning | IP65–IP66 |
| Washdown (food, pharma) | IP66/IP69K |
| Temporary flooding / puddles | IP67 |
| Submerged | IP68 (state depth and time) |

## Design rules

**Simplicity: every opening is a leak path.** Minimize joints, penetrations and covers. A one-piece housing with one cover beats five panels. Group cable entries in one place. Ask whether the sensitive component can be moved somewhere dry instead of sealing it (step 2: delete the problem).

**Gaskets and O-rings**
- Static O-ring squeeze roughly 15–30% of cross-section; groove volume larger than O-ring volume (aim ~75–85% fill) so it can deform. Use the O-ring manufacturer's groove tables (e.g. Parker O-Ring Handbook ORD 5700) for exact dimensions.
- Flat foam/elastomer gaskets: design for the manufacturer's compression range (often ~20–40%). Add compression limiters (metal-to-metal stops, shoulder bushings) so tightening cannot crush the gasket.
- Continuous sealing land, no gaps at corners; specify flatness and surface finish of sealing faces.
- Bolt spacing close enough that the flange does not lift between bolts — check flange deflection between fasteners; thin covers need more bolts or stiffening ribs.
- Gasket material for the environment: EPDM (water, weather, UV; not oils), NBR (oils), silicone (temperature range, food grades), FKM (chemicals, heat).

**Penetrations**: rated cable glands sized to the cable; sealed connectors with their own IP rating; shafts with lip seals or V-rings (the rotating interface is usually the weakest point).

**Breathing and condensation**: sealed boxes that see temperature swings pump moist air and collect condensation. Add a pressure-equalizing membrane vent (ePTFE) and, if condensation is unavoidable, a drain at the lowest point. Orient seams and covers so water runs off, not into them (no horizontal joints on top).

**Dust (IP5X/6X)**: labyrinths and overlaps for IP5X; continuous gaskets for IP6X.

**Manufacturing**: continuous welds (not stitch welds) on sealed seams; sealed corners on sheet-metal boxes; powder coat or plating compatible with the gasket contact. Check the workshop can achieve the flatness the gasket needs.

## Verification

- Calculate gasket compression at minimum and maximum tolerance (stack-up), not only nominal.
- Workshop checks (hose test, immersion in a tank) find gross leaks but are **not** a certification. If the rating must be certified, it requires testing to IEC 60529 by a qualified lab — say so in the requirements.
- State the target rating on the drawing and in the requirements; mark it "design intent, not certified" until tested.
