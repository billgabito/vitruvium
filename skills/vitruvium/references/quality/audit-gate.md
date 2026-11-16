# Independent audit gate (before the user sees a result)

No iteration is presented to the user as a result until an **independent auditor** has reviewed it and approved it. The designer must not audit its own work: it knows what it meant to do and will see that instead of what is there.

## What "independent" means

- A **separate agent with a fresh context**: it does not receive the designer's reasoning, drafts or conversation — only the artifacts and the requirements.
  - Claude Code: launch the `vitruvium-auditor` subagent (this plugin's `agents/vitruvium-auditor.md`) with the Agent tool.
  - Other agents: start a separate session or sub-agent with the prompt in `agents/vitruvium-auditor.md` (a different model is even better).
- If the host cannot run a separate agent, do a cold review with the same checklist, and **tell the user plainly that the audit was not independent**. The same applies to the conciliator.

## What the auditor receives

Paths only, no explanations: `01-requirements/` (black box, requirements), `02-concept/decision.md`, `03-model/` (current export, parts.json, assembly.json, motion.json), `04-calculations/`, `05-simulation/current/` (results.json, summary.md), `06-manufacturing/`, `07-drawings/` if any, the workshop profile, the latest `CHANGELOG.md` entry, and the viewer state (`curl -s http://127.0.0.1:8765/state` or "no live viewer").

## Checklist (the auditor verifies, it does not trust)

0. **Every part and every change has a reason — and the reason holds.** Each part in `parts.json` has a function, the requirements it serves and why it must exist as a separate part; each non-obvious feature has its reason; each change in the changelog has its why. The auditor does not accept the reason on trust: it challenges it — does the part really need to be separate (moves? different material? assembly/maintenance?), does the requirement really exist, does the feature really do what the reason claims (check the number)? Missing reason = finding; reason that does not hold = finding with the deletion, merge or correction it implies.
1. **Requirements**: every requirement is met and verified, with evidence; none silently dropped or changed after freeze.
2. **Simplicity**: parts or processes that could still be deleted; unnecessary tolerances, fasteners, variety.
3. **Calculations**: units consistent; loads match the black box; hand calculation present; FEA agrees with it (±15% where valid); mesh study done; singularities not reported as real stress; safety factors stated and adequate.
4. **Failure modes**: fatigue, buckling, joints, wear, corrosion, sealing/IP — whatever applies.
5. **Design-error catalog**: every item checked (`references/engineering/design-errors.md`).
6. **Interfaces and motion**: interference through the full range; motion.json matches the CAD joints.
7. **Manufacturability and assembly**: every part routed to a machine in the workshop profile; tolerances measurable there; outsourcing justified. **The design can be assembled**: `assembly.json` exists for multi-part designs; every step has a free insertion path at its moment in the sequence, tool access and evidence; no trapped parts; fits allow assembly; wear and service parts can be removed. A design that cannot be assembled is a blocker, whatever its other qualities.
8. **Drawings** (if produced): dimensions and tolerances complete and consistent with the model.
9. **Faithful presentation**: the 3D export is current (`stale: false`); numbers in the changelog match the result files; nothing claimed that was not verified.

Independence is not optional: the auditor works only from the files, never from the designer's explanations in conversation. If a reason is not written in the project, for the auditor it does not exist.

## Verdict format

```
VERDICT: APPROVED | CHANGES REQUIRED
Round: N
Findings:
1. [blocker|major|minor] <what is wrong> — evidence: <file, number> — expected: <what would be correct>
...
Not verified: <what the auditor could not check and why>
```

Blockers and majors must be fixed (or overturned by the conciliator's ruling). Minors may be accepted, but are shown to the user.

## Loop (nothing reaches the user without approval)

```
designer builds the iteration
        │
        ▼
 auditor round 1 ──APPROVED──────────────────────────────► present to the user
        │ CHANGES REQUIRED
        ▼
 designer corrects + writes response (fixed / disputed)
        │
        ▼
 auditor round 2 ──APPROVED──────────────────────────────► present to the user
        │ still CHANGES REQUIRED
        ▼
 expert conciliator: binding ruling for designer and auditor
        │
        ▼
 designer applies the ruling → auditor round 3 checks compliance with the ruling
        │ APPROVED ──────────────────────────────────────► present to the user
        │ not achievable
        ▼
 user gets a report clearly marked NOT APPROVED (ruling, open findings, options) and decides
```

1. **Round 1.** Designer finishes the iteration (model exported, calcs/FEA done, parts justified, changelog drafted). Auditor reviews → `09-audits/<version>-round-1.md`.
2. **Correction.** For `CHANGES REQUIRED`, the designer fixes each finding where it was born (improvement-loop table), re-exports, and writes `09-audits/<version>-round-1-response.md`: each finding answered **fixed** (with evidence) or **disputed** (with technical reasoning).
3. **Round 2.** The auditor re-reviews against its findings and the response → `09-audits/<version>-round-2.md`.
4. **Conciliator.** If round 2 is still `CHANGES REQUIRED`, do not loop again: call the **expert conciliator** (`agents/vitruvium-conciliator.md`), run on the most capable model available. It reads the project files, both audit reports and the designer's response, and issues `09-audits/<version>-ruling.md`: for each open finding, *auditor upheld*, *designer upheld* or *alternative solution* — and it may propose a better idea altogether. **The ruling is binding for both.**
5. **Round 3 — compliance.** The designer applies the ruling; the auditor checks only that the ruling was implemented correctly and nothing new broke → `09-audits/<version>-round-3.md`.
6. **Present only after APPROVED**: the viewer, the changelog entry, and a short audit summary (rounds, findings fixed, ruling if any, accepted minors, what was not verified).
7. If the ruling cannot be implemented (physics, workshop limits, a requirement conflict), the user gets a report **clearly marked NOT APPROVED** — never presented as a result — with the ruling, the open findings and the options, and decides.

The user remains the final validator: the audit makes sure what reaches them is correct and honestly described — it does not replace their review.
