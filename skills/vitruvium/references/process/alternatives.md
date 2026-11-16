# Alternatives A/B/C and the user's decision

At every major decision (overall concept, joint type, material, process) propose 2–3 genuinely different alternatives — not cosmetic variants. Different working principles (welded vs bolted vs single bent part) are real alternatives; 6 mm vs 8 mm is a parameter, not an alternative.

## Decision matrix (Ullman / Pugh style)

| Criterion | Weight | A | B | C |
|---|---|---|---|---|
| Part count / simplicity score | | | | |
| Safety factor (governing mode) | | | | |
| Mass | | | | |
| Workshop-manufacturable (which machines) | | | | |
| Cost estimate (incl. idiot index) | | | | |
| Main risk | | | | |
| **Weighted score** | | | | |

- Default weights are a starting point; the user adjusts them per project.
- Numbers must come from calculation or catalog data, labelled as estimate when rough. Never invent precision.
- Name the main failure risk of each option in words.

Then give a recommendation with the reason in two or three sentences, and stop for the user's choice (ask with the question tool). Record the choice and reason in `02-concept/decision.md`. If none fits, go back to step 1.

## Risk prototype

After the choice, name the single most uncertain thing (a joint, a material, a mechanism, a fit) and propose the cheapest test that answers it (3D print, wood, one loose part) before detailed modelling. Surprises cost more the later they are found.
