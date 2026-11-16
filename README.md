<p align="center"><img src="brand/logo.png" width="560" alt="Vitruvium — Mechanical Designer"></p>

# Vitruvium

*Named after Vitruvius, the Roman engineer-architect of strength, utility and beauty. Visual identity: [brand/BRAND.md](brand/BRAND.md).*

An agent skill for **any AI agent** (Claude Code, Codex, Cursor, Gemini CLI and others): an experienced mechanical designer whose core principle is mechanical simplicity. It is an essential, end-to-end tool for creating mechanical parts from the first idea to the finished, manufacturable part (requirements, concept, parametric model, analysis, drawings and fabrication). It follows the open Agent Skills format — a `SKILL.md` with references and templates — so any agent that reads files can use it.

Full description of how it behaves: [docs/BEHAVIOR.md](docs/BEHAVIOR.md).

- Interviews you with few, well-chosen questions and learns your workshop once.
- Checks first whether the problem is already solved on the market — buy, adapt or design from scratch.
- Runs Musk's 5 steps inside Ullman's process, with improvement loops.
- Proposes A/B/C alternatives with a decision matrix — you decide.
- Models in SolidCraft (MCP), checks by hand calc (Beer, Shigley, Roark) and FEA (Gmsh + CalculiX).
- Fits parts to your machines and checks that every assembly can be put together (sequence, insertion paths, tool access), standardizes, reviews against a design-error catalog.
- Every project in its own versioned folder with a design log and lessons.
- An interactive 3D viewer per project (Vitruvium look, engineering lettering): rotate, shaded / wireframe / x-ray, section, explode, parts list with IDs, systems on/off, stress overlay, animation of moving parts, step-by-step assembly sequence and the full version history.
- An independent auditor approves every iteration before it is shown to the user; an expert conciliator settles disagreements after the second round.
- Review mode for existing designs: ranked improvement report.

## Install

Install it as a Git clone so it can update itself:
```
git clone https://github.com/billgabito/vitruvium.git ~/vitruvium
```
Claude Code:
```
ln -s ~/vitruvium/skills/vitruvium ~/.claude/skills/vitruvium
```
Independent auditor and conciliator (Claude Code subagents, recommended):
```
mkdir -p ~/.claude/agents && ln -s ~/vitruvium/agents/vitruvium-*.md ~/.claude/agents/
```
Other agents: point the agent at `skills/vitruvium/SKILL.md` (the root `AGENTS.md` already does this for agents that read it), or link the skill folder into the agent's skills directory. Copying the folder works too, but then it cannot update itself.

## Updates

Vitruvium checks for a new release at most once a day, when it is used. It asks before updating; if you choose "always update automatically" it updates without asking from then on. Your workshop profile, lessons and projects live outside the skill folder (`~/.vitruvium/`, your projects folder), so updates never touch them. Manual control:
```
sh ~/vitruvium/skills/vitruvium/scripts/update.sh check --force   # look now
sh ~/vitruvium/skills/vitruvium/scripts/update.sh mode ask         # ask | auto | off
```

Plugin packaging (marketplace) comes with the status band in v0.4.

Optional tools: `solidcraft-cli` (CAD), `gmsh` + `ccx` (FEA), `freecadcmd` (drawings), `git`. Check what you have with `sh skills/vitruvium/scripts/check_tools.sh`; verified download links and install commands for every OS are in [references/tools/tools-setup.md](skills/vitruvium/references/tools/tools-setup.md).

## Repository structure

```
vitruvium/
├── skills/vitruvium/            ← the skill (what agents load)
│   ├── SKILL.md                 principles, session start, workflow A–K, loops, toolbox
│   ├── references/              read per phase, only when needed
│   │   ├── process/             interview, existing-solutions, simplicity, alternatives,
│   │   │                        project-folder, review-existing-design
│   │   ├── engineering/         analysis, design-errors, parts, motion, ingress-protection
│   │   ├── manufacturing/       manufacturing, assembly, workshop, catalog-search, drawings
│   │   ├── quality/             audit-gate (auditor + conciliator loop)
│   │   └── tools/               solidcraft, tools-setup
│   ├── scripts/                 fea.py, viewer.py, log_iteration.py, check_tools.sh, update.sh
│   └── assets/                  templates/ (profile, requirements, logs), brand/ (logo, favicon)
├── agents/                      vitruvium-auditor.md, vitruvium-conciliator.md
├── docs/BEHAVIOR.md             full description of how the skill behaves
├── brand/                       visual identity (BRAND.md, icons, logos, generators)
├── AGENTS.md                    entry point for agents that read it
├── CHANGELOG.md · CITATION.cff · LICENSE (MIT)
└── .claude-plugin/plugin.json
```

## Roadmap

Done (see [CHANGELOG.md](CHANGELOG.md)): core process, existing-solutions search, IP rating, tool setup, self-update, FEA script, iteration log, live 3D viewer, animation, parts with IDs and reasons, exploded view, independent auditor and conciliator.

Next:
- Drawing script (FreeCAD TechDraw from STEP); switch to SolidCraft drawings when released
- Filled section caps in the viewer
- Status band (project · version · step · pending question)
- First real project to validate the whole flow with SolidCraft exports

## Credits

Created by **William Campos V.** — github.com/billgabito

## License

MIT — see [LICENSE](LICENSE).

## How to cite (IEEE)

> [1] W. Campos V., *Vitruvium: An AI agent skill for parametric mechanical design based on mechanical simplicity*, ver. 0.15.0. (2026). [Online]. Available: https://github.com/billgabito/vitruvium

Machine-readable metadata is in [CITATION.cff](CITATION.cff).
