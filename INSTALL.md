# Installing Vitruvium — instructions for the AI agent

You are installing the Vitruvium skill for the user. Follow these steps in order, tell the user in one line what each step does, reply in the user's language, and **ask before installing any software or changing any configuration outside `~/vitruvium`**.

1. **Get the repository.** If `~/vitruvium` is not already a clone of `https://github.com/billgabito/vitruvium.git`, clone it there; if it is, run `git -C ~/vitruvium pull --ff-only`. If access is denied (private repository), tell the user they need access (e.g. `gh auth login`) and stop.

2. **Make the skill visible to you — link, do not copy** (a link keeps self-update working):
   - Claude Code: `ln -s ~/vitruvium/skills/vitruvium ~/.claude/skills/vitruvium`
   - Other agents with a skills folder: link `~/vitruvium/skills/vitruvium` into it.
   - Agents that use AGENTS.md: ask before adding a pointer to `~/vitruvium/skills/vitruvium/SKILL.md` in the user's global instructions.

3. **Auditor and conciliator** (recommended). If your host supports subagents, ask whether to link them (Claude Code: `mkdir -p ~/.claude/agents && ln -s ~/vitruvium/agents/vitruvium-*.md ~/.claude/agents/`). Otherwise tell the user audits will run in a separate session.

4. **Tools.** Run `sh ~/vitruvium/skills/vitruvium/scripts/check_tools.sh` and show the result. For each missing tool, give the command for the user's OS from `skills/vitruvium/references/tools/tools-setup.md` and install it only if the user agrees.

5. **CAD.** If `solidcraft-cli` is installed, ask whether to register its MCP server (Claude Code: `claude mcp add solidcraft -- solidcraft-cli mcp`; other hosts: `solidcraft-cli mcp setup`).

6. **Updates.** Ask how Vitruvium should update itself — ask each time (recommended), automatic, or off — and run `sh ~/vitruvium/skills/vitruvium/scripts/update.sh mode ask|auto|off`.

7. **Verify.** Confirm the skill is visible to you, run `sh ~/vitruvium/skills/vitruvium/scripts/update.sh check --force`, and give a short summary: what was installed, what is missing, and how to start ("I need to design a bracket for…").
