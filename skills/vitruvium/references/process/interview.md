# Interview and requirements (step 1)

Goal: understand the real problem with the fewest questions, then turn it into requirements that can be checked.

## Opening (maximum four questions + one request)

Ask open questions that invite the user to tell a story, not to tick boxes. Adapt the wording to what they already said; skip any question they already answered.

1. "Tell me what the part must do, where it goes, and why you need it." → function, context, the real problem behind the request.
2. "What forces, movements or loads does it receive, and what must it deliver?" → inputs and outputs, with orders of magnitude.
3. "What environment does it work in, and what does it connect to?" → material, protection, interfaces. If something inside is sensitive to dust or water (electronics, bearings, lubricant), also ask whether it needs an IP rating — see references/engineering/ingress-protection.md.
4. "Is it a concept prototype, a functional prototype or a final part? How many, and are there limits on cost, time or space?" → design depth and constraints.

Request: "If you have photos, measurements, a sketch or the old part, share them." One photo saves ten questions.

Do not ask about the workshop here — it is in the profile. Ask only "any new equipment since last time?".

## Black-box sheet (write it, mark assumptions, ask for confirmation)

| Field | Content |
|---|---|
| Function | verb + noun ("support the pump motor") |
| Inputs | loads (magnitude, direction, static/dynamic/impact, cycles), motions, energy |
| Outputs | motion, force, position, flow… |
| Elements handled | water, chemicals, food, heat, UV, dust, human contact |
| Interfaces | neighbouring parts, fasteners, shafts, existing structure |
| Constraints | space envelope, mass, budget, deadline, quantity |
| Destiny | concept / functional / final one-off / series |
| Ingress protection | IP rating needed? (e.g. IP54, IP66/IP67) and whether it must be certified |
| Standards | which apply (safety, food contact, pressure, lifting…) |
| Good enough | measurable done-criterion |

Mark each inferred value as an assumption: "Assumed: 50 kg max with light impacts — correct me if not." Then ask the remaining gaps one at a time, only when they matter.

## Requirements list

Each requirement: ID, statement (measurable), owner (named person or role, never "the department"), source, consequence of deleting it, verification method. Requirements without an owner are questioned first. Requirements from smart people are questioned too.

After the user picks an alternative, freeze the requirements. Later changes go through change control: state the change, its impact on cost/time/risk, and get the user's approval before applying it.

## How destiny changes depth

| Destiny | Material/process | Tolerances | Calculation | Documentation |
|---|---|---|---|---|
| Concept prototype | fastest: 3D print, wood, sheet | open | order of magnitude | sketch + model |
| Functional prototype | close to final | functional only | hand calc + FEA on critical zones | model + short calc note |
| Final one-off | final, workshop-made | complete | complete incl. fatigue | full drawings |
| Series | optimized for cost and repeatability | complete + process capability | complete + batch checks | drawings, assembly guide, QC plan |

Do not design a concept prototype like a production part.

## Planning and margins

For anything beyond a one-afternoon part, state a short stage plan with rough time and cost, padded 20–30% for surprises. Surprises get more expensive the later they are found, so the plan front-loads the riskiest questions.
