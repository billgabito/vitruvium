# Install Vitruvium with your AI agent

Copy the prompt below and paste it into your AI agent (Claude Code, Codex, Cursor, Gemini CLI or any agent that can run commands). It installs Vitruvium step by step and asks you before anything that changes your system.

## Prompt (English)

```text
Install the Vitruvium mechanical design skill for me. Follow these steps in order, tell me what you are doing in one line per step, and ask me before installing any software or changing any configuration outside the Vitruvium folder.

1. Check that git is available. Clone the repository into ~/vitruvium:
   git clone https://github.com/billgabito/vitruvium.git ~/vitruvium
   If ~/vitruvium already exists and is a clone of that repository, run "git -C ~/vitruvium pull --ff-only" instead. If the clone fails because the repository is private, tell me I need access (for example "gh auth login") and stop.

2. Make the skill available to you (the agent), choosing the method that fits your host:
   - Claude Code: ln -s ~/vitruvium/skills/vitruvium ~/.claude/skills/vitruvium
   - Another agent with a skills directory: link ~/vitruvium/skills/vitruvium into that directory.
   - An agent that reads AGENTS.md: tell me to open my projects with ~/vitruvium/AGENTS.md available, or add a pointer to ~/vitruvium/skills/vitruvium/SKILL.md in my global agent instructions (ask me first).
   Do not copy the folder: a link keeps the skill able to update itself.

3. Independent auditor and conciliator (recommended). If your host supports subagents (Claude Code: ~/.claude/agents), ask me whether to link them:
   mkdir -p ~/.claude/agents && ln -s ~/vitruvium/agents/vitruvium-*.md ~/.claude/agents/
   If your host has no subagents, tell me the skill will run audits in a separate session and will say when a review was not independent.

4. Check the engineering tools without installing anything:
   sh ~/vitruvium/skills/vitruvium/scripts/check_tools.sh
   Show me the result. For each missing tool, give me the install command from ~/vitruvium/skills/vitruvium/references/tools/tools-setup.md for my operating system, and install it only if I say yes.

5. CAD connection. If solidcraft-cli is installed, ask me whether to register its MCP server (Claude Code: claude mcp add solidcraft -- solidcraft-cli mcp; other hosts: solidcraft-cli mcp setup, or add {"command": "solidcraft-cli", "args": ["mcp"]} to the MCP settings).

6. Updates. Ask me how Vitruvium should update itself — ask before each update (recommended), update automatically, or never — and run:
   sh ~/vitruvium/skills/vitruvium/scripts/update.sh mode ask    (or auto / off)

7. Verify: read ~/vitruvium/skills/vitruvium/SKILL.md, confirm the skill is visible to you, and run:
   sh ~/vitruvium/skills/vitruvium/scripts/update.sh check --force
   Then give me a short summary: what was installed, what is missing, and how to start ("I need to design a bracket for…").

Reply in my language.
```

## Prompt (español)

```text
Instálame la skill de diseño mecánico Vitruvium. Sigue estos pasos en orden, dime en una línea qué haces en cada paso y pregúntame antes de instalar cualquier software o cambiar cualquier configuración fuera de la carpeta de Vitruvium.

1. Verifica que git esté disponible. Clona el repositorio en ~/vitruvium:
   git clone https://github.com/billgabito/vitruvium.git ~/vitruvium
   Si ~/vitruvium ya existe y es un clon de ese repositorio, ejecuta "git -C ~/vitruvium pull --ff-only". Si la clonación falla porque el repositorio es privado, dime que necesito acceso (por ejemplo "gh auth login") y detente.

2. Deja la skill disponible para ti (el agente), con el método que corresponda a tu entorno:
   - Claude Code: ln -s ~/vitruvium/skills/vitruvium ~/.claude/skills/vitruvium
   - Otro agente con carpeta de skills: enlaza ~/vitruvium/skills/vitruvium en esa carpeta.
   - Un agente que lee AGENTS.md: dime que abra mis proyectos con ~/vitruvium/AGENTS.md disponible, o agrega una referencia a ~/vitruvium/skills/vitruvium/SKILL.md en mis instrucciones globales (pregúntame antes).
   No copies la carpeta: el enlace permite que la skill se actualice sola.

3. Auditor independiente y conciliador (recomendado). Si tu entorno admite subagentes (Claude Code: ~/.claude/agents), pregúntame si los enlazo:
   mkdir -p ~/.claude/agents && ln -s ~/vitruvium/agents/vitruvium-*.md ~/.claude/agents/
   Si no admite subagentes, dime que la skill hará las auditorías en una sesión separada y avisará cuando una revisión no haya sido independiente.

4. Revisa las herramientas de ingeniería sin instalar nada:
   sh ~/vitruvium/skills/vitruvium/scripts/check_tools.sh
   Muéstrame el resultado. Para cada herramienta que falte, dame el comando de instalación de ~/vitruvium/skills/vitruvium/references/tools/tools-setup.md para mi sistema operativo, e instálala solo si te digo que sí.

5. Conexión con el CAD. Si solidcraft-cli está instalado, pregúntame si registro su servidor MCP (Claude Code: claude mcp add solidcraft -- solidcraft-cli mcp; otros entornos: solidcraft-cli mcp setup, o agregar {"command": "solidcraft-cli", "args": ["mcp"]} a la configuración MCP).

6. Actualizaciones. Pregúntame cómo debe actualizarse Vitruvium —preguntar antes de cada actualización (recomendado), automáticamente o nunca— y ejecuta:
   sh ~/vitruvium/skills/vitruvium/scripts/update.sh mode ask    (o auto / off)

7. Verifica: lee ~/vitruvium/skills/vitruvium/SKILL.md, confirma que la skill está visible para ti y ejecuta:
   sh ~/vitruvium/skills/vitruvium/scripts/update.sh check --force
   Luego dame un resumen corto: qué quedó instalado, qué falta y cómo empezar ("Necesito diseñar un soporte para…").

Respóndeme en mi idioma.
```
