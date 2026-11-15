# Audit mode: improving an existing design

Input: drawings, STEP, photos, the physical part, or a description.

1. **Reverse interview** (few questions): what does it do, what fails or annoys, what do you want improved, are there original requirements? Ask for load and usage data you cannot infer.
2. **Rebuild the black box** from the design and ask the user to confirm it.
3. **Apply the full method:**
   - 5 steps: which requirements are dumb, which parts/processes can go;
   - the design-error catalog, item by item;
   - hand calculation (and FEA if needed) of the critical zones;
   - interfaces between parts;
   - standardization (part and fastener variety);
   - manufacturability in the user's workshop;
   - the market: is there now a commercial product or standard module that would replace part or all of the design? (existing-solutions.md)
4. **Report**, findings ranked by impact (safety first, then function, cost, simplicity):

| # | Finding | Evidence | Risk / impact | Proposed fix | Effort |
|---|---|---|---|---|---|

   Also give the summary numbers: parts total/unique, fastener references, processes, outsourced parts, and the simplicity gains achievable.
5. **For each major improvement**, propose A/B/C and let the user decide.
6. If the user approves a redesign, switch to design mode with its own project folder (the audit report goes in `01-requirements/`).

Mark clearly anything you could not verify from the information given (e.g. "load unknown — fatigue not assessed").
