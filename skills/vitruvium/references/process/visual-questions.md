# Questions with a picture

A question about shape, layout, alternatives, motion, assembly or where something goes is hard to answer from text. Every such question comes with a **conceptual image** — a picture is worth a thousand words. Pure data questions ("how many units?", "budget?") do not need one.

## What to show

| Question about | Picture |
|---|---|
| Alternatives A/B/C | one sketch per option, side by side, same view and scale, labelled A / B / C |
| Where a part goes, an orientation, a direction | the assembly with the candidate positions marked (arrows, numbered spots) |
| A load, a motion, a support | the part with arrows: loads in red, motion in purple, supports in blue |
| A dimension or envelope | the part with the dimension line in question |
| An assembly order or access | the step with the insertion direction and the tool |
| A detail (fillet, joint, weld) | a close-up or section of that detail |

## How to make it (cheapest that is clear)

1. **Concept sketch (SVG)** — written directly as an SVG file: simple outlines in an isometric or orthographic view, part IDs, arrows and dimension lines, Vitruvium colours (ink `#2B2418` lines, parchment `#F6EFDC` background, blue `#2A5CD6` / red `#DC3C32` / purple `#7F77DD` for supports / loads / motion), ISO-style lettering (font-family `osifont, 'Barlow Condensed', sans-serif`). Clean, not artistic; seconds to make.
2. **Quick concept models** — when the shapes are already in SolidCraft, export them and take a screenshot from the viewer (one image per option).
3. **The current model** — a viewer screenshot with marks, when the question is about the existing design.

Save images in the project under `00-questions/<n>-<slug>/` (e.g. `00-questions/03-joint-type/A.svg`).

## How to show it

- **Live viewer**: write `00-questions/current.json`; the viewer shows a prominent **Question** panel over the 3D view with the text and the option images side by side. Delete or rename the file once answered and the panel disappears.

```json
{"question": "Which joint should hold the lever to the base?",
 "context": "All three fit your workshop; B is the simplest.",
 "options": [
   {"label": "A — Welded", "image": "00-questions/03-joint-type/A.svg", "note": "strongest, not removable"},
   {"label": "B — Bolted M5 (Recommended)", "image": "00-questions/03-joint-type/B.svg", "note": "removable, 2 parts more"},
   {"label": "C — Pin + clip", "image": "00-questions/03-joint-type/C.svg", "note": "fastest to assemble"}]}
```

- **In the conversation**: also attach or display the image if the host can (file card, image preview, inline widget), next to the question asked with the question tool. If the host cannot show images, give the file path and keep the viewer panel as the visual.
- The answer still comes back through the conversation; the picture supports the question, it does not replace it.
