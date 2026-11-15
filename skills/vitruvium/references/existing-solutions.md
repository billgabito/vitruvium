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

## Keep it short

Time-box the search (a few targeted searches, not a market study). If nothing reasonable appears quickly, say so and move on. For a trivial part (a spacer, a simple plate), skip it and say why.

## Present what you found

| # | Solution | Source (link, date) | Price / lead time | Covers requirements | Gaps | Workshop work needed |
|---|---|---|---|---|---|---|

Then give three starting points, with your recommendation first, and ask the user to choose (question tool):

1. **Buy** — a product covers the requirements. Fastest and usually simplest; the design work becomes selection, mounting and verification (check its ratings against the loads and environment).
2. **Adapt** — buy a standard product or module and design only the interface or the missing part. Usually the best balance.
3. **Design from scratch** — nothing fits, it is too expensive, unavailable locally, or the user wants to own the design. Use what was found as inspiration and benchmark (dimensions, mechanisms, price to beat).

Record the choice and the reason in `02-concept/decision.md`, and keep the search table in `references/` of the project. In design-from-scratch, the commercial options remain useful as the baseline in the A/B/C matrix ("our design must beat this product on cost, simplicity or fit").

## Intellectual property and licenses (be honest, not legal)

- Learning from a product or a published mechanism is normal engineering. Copying a protected design is not.
- Open designs carry licenses (CC BY, CC BY-NC, GPL…); state the license and whether commercial use is allowed.
- If a very similar, recent and patented solution shows up and the user plans to sell the product, mention that a patent check (freedom to operate) may be needed. This is a flag, not legal advice.
