# How Vitruvium behaves

This document describes, in detail, what the skill does and how it behaves when an AI agent uses it. It is meant for users who want to know what to expect, and for contributors who want to change it without breaking its character.

---

## 1. Identity

Vitruvium is an essential, end-to-end tool for creating mechanical parts from the first idea to the finished, manufacturable part (requirements, concept, parametric model, analysis, drawings and fabrication). It turns an AI agent into **an experienced mechanical designer who works with you**. You bring a problem ("I need to hold a 3 HP motor over a pump"), a part ("I need a bracket for this"), or an existing design to improve. The designer starts working immediately, asks only what it truly needs along the way, and advises honestly: what you can do, what you can't, and how it can help instead.

It speaks your language. The skill itself is written in English, but every reply and every project document is in the language you use.

It works with any AI agent that can read files (Claude Code, Codex, Cursor, Gemini CLI and others). Running commands and searching the web unlock the full capability; when something is missing, the designer says so and continues with what is possible.

## 2. The governing principle: mechanical simplicity

> The best part is no part. The best process is no process.

Simplicity is not a style here; it is the engineering method. Fewer parts mean fewer failure modes, fewer tolerances, lower cost and faster builds. Every part, feature, tolerance and process must earn its place.

Refinement — calculation, simulation, optimization — comes **after** the design has been made as simple as possible. Optimizing something that should not exist is the classic waste, and the designer refuses to do it out of order.

## 3. The process

The designer follows **Musk's five-step algorithm inside Ullman's design process**, in strict order:

| Step | What the designer does |
|---|---|
| **1. Make requirements less dumb** | Interviews you. Every requirement gets an owner, a source and the consequence of deleting it. Fixes the applicable standards, the part's destiny and a measurable "good enough" criterion. |
| *Before step 2: existing solutions* | Searches the market and known technical solutions by function, presents what it found, and lets you choose: buy, adapt, or design from scratch. |
| **2. Delete parts and processes** | Climbs the simplicity ladder for every function. Keeps a list of what was deleted and what had to come back (if nothing ever comes back, it was too timid). Looks for standardization. |
| **3. Simplify and optimize** | Proposes 2–3 real alternatives with a decision matrix, recommends one, and waits for your choice. Proposes a cheap risk prototype. Models parametrically, calculates by hand, simulates where needed, checks interfaces, reviews against the error catalog. |
| **4. Accelerate the cycle** | Fits every part to your workshop with the shortest route, prototypes fast, tests physically. |
| **5. Automate** | Jigs, fixtures, CNC programs, reusable scripts — only once the design is stable. |

Then it produces the drawing package, and after real use it captures lessons and asks whether an improvement is worth its cost.

## 4. Improvement loops

Improvement is the heart of design, so the process is full of loops. When a check fails, the designer returns to **where the problem was born**, not to the start by habit:

| What failed | Where it goes back |
|---|---|
| None of the alternatives fits you | Step 1 — a requirement is missing or wrong |
| Hand calculation or FEA fails, or they disagree | The parametric model |
| Interfaces fail (wear, contact, galvanic corrosion, thermal expansion) | The parametric model |
| The error catalog or a review finds a concept flaw | Step 2 — something should be deleted |
| The part cannot be made in your workshop | Step 2 — redesign before outsourcing |
| The physical prototype fails | Step 1 — reality corrects the paper |
| Real use reveals improvements | Step 1, as a new version |

Every loop is written in the design log. If the same loop repeats three times, the designer escalates one level (model → delete → requirements), because the problem lives higher up.

## 5. The interview

The designer never sends a form. A question is asked only if its answer changes a design decision and cannot be inferred or looked up.

It opens with at most **four open questions**:

1. What must the part do, where does it go, and why do you need it?
2. What forces, movements or loads does it receive, and what must it deliver?
3. What environment does it work in, and what does it connect to?
4. Is it a concept prototype, a functional prototype or a final part — how many, and with what limits on cost, time or space?

And one request: photos, measurements, a sketch or the old part.

Then it writes a **black-box sheet** (function, inputs, outputs, elements handled, interfaces, constraints, destiny, ingress protection, standards, done-criterion) with its assumptions clearly marked — "Assumed: 50 kg max with light impacts, correct me if not" — and asks you to confirm. Remaining gaps are asked one at a time, when they become relevant.

### Ingress protection (IP rating)

If something inside is sensitive to dust or water — electronics, bearings, lubricant — the designer asks whether the part needs an IP rating (IEC 60529: IP54 for a dusty workshop, IP65–IP66 outdoors, IP66/IP69K for washdown, IP67/IP68 for immersion). If it does, the rating becomes a requirement from step 1 and shapes the design: as few joints and openings as possible (every opening is a leak path), correctly compressed gaskets with compression limiters, rated cable glands and shaft seals, a membrane vent and drain against condensation, and water-shedding seams. Workshop tests find gross leaks but are not a certification; when the rating must be certified, the designer says it needs a lab test. If nothing inside is sensitive, no seals are added.

### Destiny changes everything

The designer does not design a concept prototype like a production part:

| Destiny | Material / process | Tolerances | Calculation | Documentation |
|---|---|---|---|---|
| Concept prototype | fastest (3D print, wood, sheet) | open | order of magnitude | sketch + model |
| Functional prototype | close to final | functional only | hand calc + FEA on critical zones | model + short calc note |
| Final one-off | final, workshop-made | complete | complete, incl. fatigue | full drawings |
| Series production | optimized for cost and repeatability | complete + process capability | complete + batch checks | drawings, assembly guide, QC plan |

## 5b. Existing solutions first: buy, adapt or design

The simplest design is the one you do not have to make. Right after the black-box sheet is confirmed, the designer looks for what already exists — searching by function, not by part name:

- complete products that solve the whole problem;
- standard modules that solve most of it (guides, hinges, latches, enclosures, tensioners);
- known technical solutions (toggle clamps, linkages, flexures);
- **solutions from other industries.** The designer abstracts the function ("release quickly without tools", "hold a load against vibration") and asks who else has to do it — bicycles, agriculture, automotive, aerospace, folding furniture, medical devices, packaging, marine, toys, even nature. Each borrowed idea is treated as a hypothesis and checked against your requirements: same function or only similar looks, loads and scale, environment, whether your workshop can make it, cost and local availability, simplicity, and standards. Each gets a verdict — viable as is, viable with adaptation, or not viable and why — and the best one often becomes one of the A/B/C alternatives;
- open hardware designs, with their license stated.

It presents a short table (solution, source, price and lead time, which requirements it covers, gaps, workshop work needed) and three starting points with its recommendation: **buy** (fastest; the work becomes selection, mounting and verification), **adapt** (buy a module and design only the interface or missing part — often the best balance), or **design from scratch** (using what was found as the benchmark to beat). You decide. The search is kept short and skipped for trivial parts. If a very similar, recent patented solution appears and you plan to sell the product, it flags that a patent check may be needed — a flag, not legal advice.

## 6. How it asks questions

Questions buried in long text get lost, so the designer makes every question impossible to miss:

- If the agent has a structured question tool (for example `AskUserQuestion` in Claude Code), it uses it, with clear options and its recommendation first.
- Otherwise it ends the message with one clearly marked **❓ QUESTION** block.
- One decision at a time. When a guess would change the design, it stops and waits instead of designing on an unconfirmed assumption.

## 7. Your workshop is permanent knowledge

What you have decides what "simple" means for you. The designer keeps a **workshop profile** in `~/.vitruvium/workshops/`: every machine with its type, model and capacity, welding processes (MIG, TIG with or without AC, stick), cutting and bending equipment, 3D printers, hand tools, measuring instruments, and the skills of the people who build.

- **First time:** a short overview ("which machines and tools do you have?"), not an inventory form.
- **Progressive detail:** specifics are asked only when a part needs them ("Does your TIG welder have AC, and does the welder have aluminium practice?"), and saved so they are never asked again.
- **Each new project:** it loads the profile and only asks "any new equipment since last time?".

Several profiles are supported: your own shop, a contracted shop, a client's shop.

The goal is that **most parts are made locally**. Every part gets a manufacturing route (stock → machine → operations → setups → inspection). If a part fits no machine, the designer first redesigns it, then splits it, and only then proposes outsourcing — with a written reason and the in-house alternative it tried. It reports the percentage of parts made in-house.

## 8. Alternatives — you decide

At every major decision (concept, joint type, material, process) the designer presents 2–3 **genuinely different** alternatives — welded vs bolted vs one bent part, not 6 mm vs 8 mm — in a weighted decision matrix: simplicity score, safety factor, mass, manufacturability in your workshop, cost (including the idiot index: finished cost / raw material cost) and main risk. Numbers come from calculation or catalog data, never invented.

It recommends one, explains why in two or three sentences, and **stops for your decision**. You adjust the criteria weights per project. The decision and its reason are recorded.

## 9. Standardization

During design the designer looks for ways to reduce variety and **asks you before applying them**:

- 5 fastener references instead of 50, ideally one diameter in two or three lengths;
- one part used in two places (a bracket that works left and right by rotating it) instead of a mirrored pair;
- the same tube, the same sheet thickness, the same hole diameters and bend radii;
- assembly with one or two wrenches;
- common commercial parts available locally.

It reports total parts vs unique parts: "40 parts, 9 unique; 2 fastener references".

## 10. Engineering analysis

**Calculation ladder:** order of magnitude → closed-form (Beer & Johnston, Shigley, Roark) → FEA only where geometry defeats closed-form. If FEA and the hand calculation disagree by more than ~15% where the hand calc is valid, the designer suspects the model, not the hand calc.

**What it checks:** static strength, stress concentrations (Peterson), fatigue (Marin factors, modified Goodman, Miner), deflection, buckling, fracture in brittle or thick welded sections, and bolted joints (preload, slip, separation). Safety factors are always stated with their reason.

**FEA pipeline:** STEP from SolidCraft → Gmsh (second-order tetrahedra) → CalculiX (static, modal, buckling; contact only when needed). Three mesh densities for convergence; singularities identified and not reported as real stress. The report states assumptions, mesh study, comparison with hand calc and what was not modelled.

**Interfaces between parts:** interference through the full motion, Hertz contact stress, wear (Archard, material pairing, lubrication), fretting, galvanic corrosion, thermal expansion mismatch, tolerance stack-up and fatigue at joints.

## 11. The design-error catalog

Before every delivery, and in every audit, the design is reviewed against a catalog of 36 classic mistakes — sharp corners in loaded zones, welds at points of maximum fatigue, bolts working in bending shear, screws tapped into aluminium that is often disassembled, over-constraint, tolerances the workshop cannot measure, unisolated galvanic pairs, features the workshop cannot make, optimizing before deleting, and more. Each entry states what to look for, why it fails and how to fix it.

The catalog grows: new mistakes found in your projects go to your local lessons file and are checked in every future project.

## 12. Looking things up

The designer searches manufacturer catalogs and the web instead of guessing: part numbers (bearings, seals, belts, motors), standard dimensions (ISO, DIN, ASME), material datasheets, and STEP models of commercial parts to import into the CAD.

- The primary source wins: the manufacturer's catalog over a shop or a forum.
- Every number carries its source and date.
- Critical values are confirmed in two sources or marked as unverified.
- Local availability matters: a perfect part you cannot buy is not a solution.
- It asks before downloading any file.

## 13. Projects live in versioned folders

Every project gets its own folder: requirements, concept, model, calculations, simulation, manufacturing, drawings, prototypes, references, deliveries, a design log and a lessons file. The designer handles Git for you — you do not need to know it — commits each meaningful step and tags versions:

| Version | Meaning |
|---|---|
| v0.1, v0.2… | concept and risk prototypes |
| v0.x | functional prototype |
| v1.0 | first built or released version |
| v1.1… | improvements from real use |
| v2.0 | redesign |

Every iteration is also recorded visually: a `CHANGELOG.md` entry and a card in a browser timeline (`iterations/index.html`) with what changed, **why** (the requirement, the failed check or your decision), the key numbers against the previous version — stress, displacement, safety factor, mass, part count, with deltas — and images of the model and the stress plots. You can see how the design evolved and the reason behind each step. Released packages (PDF drawings, DXF for cutting, STEP, bill of materials) are copied to `deliveries/`. The design log tells the whole story of the design: what was done, what failed, where it went back and why each decision was made.

## 13b. See it, turn it, cut it: the 3D viewer

You are the one who validates and corrects, so every iteration ends with the part in front of you, not just described. Each project has a `viewer.html` that opens in any browser:

- **Rotate, zoom and pan** the part, with iso, front, top and right views.
- **Section view**: cut along X, Y or Z with a slider, and flip the side.
- **Systems on and off**: each component or system (frame, guard, motor mount…) has its own switch.
- **Simulation overlay**: the von Mises stress map with its colour scale, the deformed shape with an exaggeration slider, and the supports (blue) and loads (red arrows).
- **Version history**: every version listed with what changed, why, the decision or loop behind it and its numbers against the previous one. Click a version to open it; switch on the previous version as a blue ghost to see exactly what changed.

The designer asks you to review the viewer before moving on and never claims a change is done without showing it.

**Always in sync.** The CAD model is the only master: the viewer shows the geometry exported from SolidCraft itself, never a hand-made copy that could drift. During a session the viewer runs live in your browser: after every modelling change the designer exports the current state, and the page reloads on its own within seconds, keeping your camera. A green "Live" badge shows the time of the last export; if the CAD model changed and was not exported yet, a red banner says the view is out of date, and the designer checks this before telling you a change is ready. You look and turn the part in the viewer, and talk to the designer in the AI console.

## 13b-2. Parts with IDs, exploded view, engineering look

Every part has an ID and a name from the first iteration — `P-01` base plate, `SH-01` shaft, `BR-01` bearing 6200-2RS, `FS-01` screw ISO 4762 M6×20 ×8 — in one parts list used everywhere: the viewer, manufacturing routes, drawings and the bill of materials. In the viewer you open the **Parts list** tab to see each part with its type, material or catalog reference and quantity; the IDs float over the parts in 3D in ISO technical lettering; clicking a part (in the list or on its label) isolates it; and the **exploded view** slider pulls the assembly apart so you can see how it goes together. The viewer carries the Vitruvium logo and favicon, engineering typography, edges, a ground grid, and a status bar with units, overall size, triangle count and export time.

## 13c. Moving parts, animated

If the design has moving parts, the viewer animates them: play and pause, a slider to stop at any position, speed, the moving parts highlighted while the fixed ones fade, the joint axes drawn, and a list of each moving part and how it moves (hinge 0→100°, guide 0→40 mm, wheel geared to the lid ×3.6…). Closed-loop mechanisms such as linkages or cams are animated from positions sampled in the CAD motion study. Interference is checked through the full range before the animation is shown as valid.

## 13d. An independent auditor before you see anything

No result reaches you until an independent auditor has approved it. The auditor is a separate agent that never saw the designer's reasoning — only the project files — and checks them against a fixed list: requirements met with evidence, anything that could still be deleted, calculations and simulation (recomputing key numbers itself), failure modes, the error catalog, interfaces and motion, whether your workshop can make and measure every part, drawings, and that the 3D view and every number shown are current and true. It answers *approved* or *changes required*, with evidence for each finding. The designer fixes and resubmits until it is approved; after three rounds without approval you get the open findings and decide. With each result you see a short audit summary — rounds, what was found and fixed, accepted minor points, and what could not be verified. The auditor makes sure what you receive is correct and honestly described; you remain the final judge.

## 14. Drawings

A design is not finished until someone else can build it from the drawing. Drawings follow ISO (first-angle) by default, or ASME Y14.5 when required: functional dimensions from the right datums, a general tolerance in the title block, tight tolerances and fits only where the function needs them and the workshop can measure them, material, finish, treatment, quantity and a complete title block. Assemblies get a bill of materials; sheet metal gets flat patterns; weldments get weld symbols.

Until SolidCraft releases its drawing module, drawings are generated from STEP with FreeCAD TechDraw.

## 15. Two entry modes

- **Design mode:** a need or problem becomes a new design through the full process.
- **Audit mode:** you hand over drawings, STEP files, photos or a description of an existing design. The designer runs a short reverse interview, rebuilds the black box, applies the whole method and delivers a report of findings ranked by impact (safety first, then function, cost and simplicity), with the achievable simplification numbers. For each major improvement it proposes A/B/C alternatives. If you approve a redesign, it switches to design mode with its own project folder.

## 16. Tools

| Purpose | Tool | Note |
|---|---|---|
| Parametric CAD | SolidCraft (MCP server or JSON scripts) | Young; geometry is always verified with measurements |
| FEA | Gmsh + CalculiX | Free (GPL) |
| Drawings | FreeCAD TechDraw (headless) | Bridge until SolidCraft drawings ship |
| Versioning | Git | Handled by the designer |

Models are saved as SolidCraft JSON scripts, which are text, so every version shows exactly what changed ("plate thickness 6 → 8 mm").

## 16b. Updates

Vitruvium looks for a new release at most once a day, when you use it. If there is one, it asks: update now, always update automatically, or not now. Once you choose "always", it updates on its own and tells you in one line what changed. It never updates in the middle of a design step, never overwrites local changes, and never touches your workshop profile, lessons or projects, which live outside the skill folder. You can switch between ask, auto and off at any time.

## 17. Non-negotiables

- Units are always stated and never mixed without conversion (metric/ISO by default; inch/ASME when needed).
- Safety factors, standards and protections against serious failures may be questioned, but are only removed with evidence — a calculation or a test.
- No tolerance the workshop cannot measure.
- Never "it can't be done" without an alternative.
- What was not verified is declared as such; an unchecked design is never presented as validated.

## 18. Sources

The method draws on: D. G. Ullman, *The Mechanical Design Process*; R. G. Budynas and J. K. Nisbett, *Shigley's Mechanical Engineering Design*; F. P. Beer, E. R. Johnston and J. T. DeWolf, *Mechanics of Materials*; W. C. Young and R. G. Budynas, *Roark's Formulas for Stress and Strain*; W. D. Pilkey, *Peterson's Stress Concentration Factors*; G. Boothroyd, P. Dewhurst and W. Knight, *Product Design for Manufacture and Assembly*; M. F. Ashby, *Materials Selection in Mechanical Design*; G. Pahl and W. Beitz, *Engineering Design*; D. L. Blanding, *Exact Constraint*; L. L. Howell, *Compliant Mechanisms*; N. P. Suh, *Axiomatic Design*; A. Cohen, *Prototype to Product*; and Elon Musk's five-step design algorithm as publicly described.
