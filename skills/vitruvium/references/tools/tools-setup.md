# External tools: where they live and how to install them

Sources verified on 2026-11-15. Use these instead of searching. Before installing anything, tell the user what will be installed and from where, and ask. Run `scripts/check_tools.sh` first to see what is already there.

All tools are free and open source.

| Tool | Used for | Interface Vitruvium uses | Needed? | License |
|---|---|---|---|---|
| SolidCraft | Parametric CAD | **MCP** (official, `solidcraft-cli mcp`); CLI + JSON scripts as fallback | Yes | Apache-2.0 |
| Gmsh | Meshing STEP for FEA (exports CalculiX `.inp` directly) | CLI `gmsh` or Python API (`import gmsh`) | Yes, for FEA | GPL |
| CalculiX | FEA solver | CLI `ccx` | Yes, for FEA | GPL |
| ccx2paraview | Converts CalculiX results `.frd` → `.vtu` | CLI / Python | Yes, for FEA images | GPL-3.0 |
| PyVista | Renders stress and displacement images from `.vtu` | Python | Yes, for FEA images | MIT |
| FreeCAD | Drawings (TechDraw), headless | CLI `freecadcmd` + Python | Yes, for drawings | LGPL-2.1 |
| Git | Project versioning, skill updates | CLI | Yes | GPL-2.0 |
| Python 3 | All scripts | CLI | Yes | PSF |
| ParaView | Interactive viewing of results by the user | GUI | Optional | BSD |

Why CLI and not MCP for most tools: the agent runs these as commands and reads their files, which is simpler, works in any agent, and adds no extra server to maintain. Only SolidCraft is used through MCP, because modelling is an interactive, many-step session and its MCP is official.

## SolidCraft

- Home: https://solidcraft.io · Docs: https://docs.solidcraft.io · Downloads: https://solidcraft.io/download
- Repository: https://github.com/tangency-labs/solidcraft (install options: `docs/downloads.md`; MCP: `docs/mcp.md`)
- Install:
  - macOS: `solidcraft-macos-universal.dmg` from the downloads page, drag to Applications. On start, the app links `solidcraft-cli` into `/opt/homebrew/bin` or `/usr/local/bin` (menu *Help > Install solidcraft-cli command* if those folders are not writable).
  - Windows: `solidcraft-windows-x64.msi` (also arm64/x86 and a portable zip). Older installers may not put `solidcraft-cli` on PATH; default path `C:\Program Files\SolidCraft\solidcraft-cli.exe`.
  - Linux: `sudo snap install solidcraft`, or AppImage / .deb / .rpm / Flatpak from the downloads page.
  - Browser (no install, no CLI): https://solidcraft.io/app
- Register the MCP server:
  - Claude Code: `claude mcp add solidcraft -- solidcraft-cli mcp`
  - Any MCP client: `solidcraft-cli mcp setup` configures installed clients, or add to the client's config: `{"mcpServers": {"solidcraft": {"command": "solidcraft-cli", "args": ["mcp"]}}}`
- Check: `solidcraft-cli commands`

## Gmsh

- Home and downloads: https://gmsh.info (#Download) · Repository: https://gitlab.onelab.info/gmsh/gmsh
- Install:
  - Any OS with Python (recommended, includes the Python API): `pip install --upgrade gmsh`
  - macOS/Linux with Homebrew: `brew install gmsh`
  - Or the official binaries (macOS DMG for Intel/ARM, Windows zip, Linux tgz) from gmsh.info
- Check: `gmsh --version` or `python3 -c "import gmsh; print(gmsh.__version__)"`

## CalculiX (ccx)

- Home: http://www.calculix.de · Downloads: http://www.dhondt.de · Source mirror: https://github.com/Dhondtguido/CalculiX
- Install:
  - Conda (any OS where conda-forge has a build): `conda install conda-forge::calculix`
  - Debian/Ubuntu: `sudo apt install calculix-ccx`
  - Linux: official executable `ccx_<version>.tar.bz2` from dhondt.de
  - Windows: third-party builds linked from dhondt.de (bConverged, SourceForge)
  - macOS: there is no Homebrew formula and no official binary. Use conda-forge if it offers a macOS build for the user's chip; otherwise build from source (`ccx_<version>.src.tar.bz2`, needs a Fortran compiler, SPOOLES and ARPACK) or run it in a Linux container. Tell the user this before starting.
- The executable may be named `ccx` or `ccx_<version>` (e.g. `ccx_2.23`).
- Check: `ccx -v`

## ccx2paraview (results conversion)

- Package: https://pypi.org/project/ccx2paraview · conda-forge: `ccx2paraview`
- Install: `pip install ccx2paraview`
- Use: `ccx2paraview job.frd vtu` (writes `job.vtu`; several time steps also write a `.pvd`). For binary `.frd`, the separate package `frd2vtu` (https://pypi.org/project/frd2vtu/) is an alternative.
- Check: `python3 -c "import ccx2paraview"`

## PyVista (result images)

- Home: https://pyvista.org · Repository: https://github.com/pyvista/pyvista
- Install: `pip install pyvista`
- Use: load the `.vtu`, plot von Mises stress / displacement with a scalar bar, save PNG (off-screen rendering) for the FEA report.
- Check: `python3 -c "import pyvista"`

## ParaView (optional, for the user)

- Downloads: https://www.paraview.org/download/ — open the `.vtu`/`.pvd` to explore results interactively.

## FreeCAD (headless drawings)

- Home and downloads: https://www.freecad.org/downloads.php · Repository: https://github.com/FreeCAD/FreeCAD
- Install:
  - macOS: `brew install --cask freecad`, or the DMG (arm64 / x86_64) from the downloads page
  - Windows: installer `.exe` from the downloads page
  - Linux: AppImage from the downloads page, or the distribution package
- Headless command: `freecadcmd` (older versions: `FreeCADCmd`). On macOS it is inside the app bundle, usually `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd` — confirm the path with `ls` (not verified for every version).
- Check: `freecadcmd --version`

## Third-party MCP servers (optional, not required)

Community projects exist that wrap these tools as MCP servers. Vitruvium does not need them (it uses the CLIs directly), and they are not official — review the code, license and maintenance before using one, and never install them without the user's consent:

- CalculiX + Gmsh: casys-ai `mcp-calculix` (https://jsr.io/@casys/mcp-calculix); Cai-aa CAE-Agent-Hub `mcp-calculix` (https://mcpservers.org/servers/github-com-cai-aa-cae-agent-hub-tree-main-mcp-calculix)
- FreeCAD (drive a running FreeCAD GUI through an addon): neka-nat `freecad-mcp` (https://mcpservers.org/servers/github-com-neka-nat-freecad-mcp), theosib `FreeCAD-MCP-Server` (https://github.com/theosib/FreeCAD-MCP-Server), spkane `freecad-robust-mcp` (https://pypi.org/project/freecad-robust-mcp/)

A FreeCAD MCP can be useful only if the user wants to watch drawings being built live in FreeCAD; headless `freecadcmd` covers the drawing workflow.

## Git and Python

- Git: https://git-scm.com/downloads (macOS: `xcode-select --install` or `brew install git`; Linux: package manager; Windows: Git for Windows).
- Python 3: https://www.python.org/downloads/ (often already present).

## What works without each tool

| Missing | Still possible |
|---|---|
| SolidCraft | requirements, concept, hand calculations, written dimensioned spec; JSON scripts ready to run later |
| Gmsh or CalculiX | hand calculations (Beer, Shigley, Roark); FEA marked "not performed" |
| ccx2paraview or PyVista | FEA numbers from the CalculiX `.dat` output; report without stress images |
| FreeCAD | dimension table + SolidCraft DXF view, marked "not a formal drawing" |
| Git | `deliveries/` snapshots only |
