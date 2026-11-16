# Looking up parts, standards and data

Look things up instead of guessing. Use web search and fetch tools when available.

| Need | Where to look first |
|---|---|
| By part number (bearings, seals, belts, motors, pneumatics) | the manufacturer's catalog (e.g. SKF, NSK, Gates, Festo, igus, Parker) |
| Standard dimensions (screws, nuts, keys, profiles) | the ISO/DIN/ASME standard or a manufacturer table quoting it (e.g. ISO 4762 socket head cap screws) |
| Material properties | the material producer's datasheet; MatWeb for orientation |
| 3D models of commercial parts | manufacturer STEP downloads, TraceParts and similar libraries → import into SolidCraft |
| Local availability and price | suppliers in the user's country/city |

## Data quality rules

- Primary source wins: manufacturer catalog over a shop listing or a forum.
- Every number used in a calculation carries its source (URL or document, and date) in `references/` and the calc note.
- Critical values (load ratings, yield strength, dimensions that drive fits) are confirmed in two sources, or marked "unverified".
- Prefer parts the user can actually buy locally; a perfect part they can't get is not a solution.
- Ask the user before downloading files, and only from manufacturer sites or recognized libraries. Save downloads under the project's `references/` folder.
