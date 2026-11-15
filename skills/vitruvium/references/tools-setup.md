# External tools: where they live and how to install them

Sources verified on 2026-11-15. Use these instead of searching. Before installing anything, tell the user what will be installed and from where, and ask. Run `scripts/check_tools.sh` first to see what is already there.

All tools are free and open source.

| Tool | Used for | License |
|---|---|---|
| SolidCraft (`solidcraft-cli`) | Parametric CAD, MCP server | Apache-2.0 |
| Gmsh | Meshing STEP for FEA | GPL |
| CalculiX (`ccx`) | FEA solver | GPL |
| FreeCAD (`freecadcmd`) | Drawings (TechDraw), headless | LGPL-2.1 |
| Git | Project versioning | GPL-2.0 |
| Python 3 | Scripts (mesh, solver input, drawings) | PSF |

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

## FreeCAD (headless drawings)

- Home and downloads: https://www.freecad.org/downloads.php · Repository: https://github.com/FreeCAD/FreeCAD
- Install:
  - macOS: `brew install --cask freecad`, or the DMG (arm64 / x86_64) from the downloads page
  - Windows: installer `.exe` from the downloads page
  - Linux: AppImage from the downloads page, or the distribution package
- Headless command: `freecadcmd` (older versions: `FreeCADCmd`). On macOS it is inside the app bundle, usually `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd` — confirm the path with `ls` (not verified for every version).
- Check: `freecadcmd --version`

## Git and Python

- Git: https://git-scm.com/downloads (macOS: `xcode-select --install` or `brew install git`; Linux: package manager; Windows: Git for Windows).
- Python 3: https://www.python.org/downloads/ (often already present).

## What works without each tool

| Missing | Still possible |
|---|---|
| SolidCraft | requirements, concept, hand calculations, written dimensioned spec; JSON scripts ready to run later |
| Gmsh or CalculiX | hand calculations (Beer, Shigley, Roark); FEA marked "not performed" |
| FreeCAD | dimension table + SolidCraft DXF view, marked "not a formal drawing" |
| Git | `deliveries/` snapshots only |
