#!/bin/sh
# Shows which external tools Vitruvium can use on this machine. Changes nothing.
# Install sources: references/tools-setup.md

ok()   { printf '  [ok]      %-12s %s\n' "$1" "$2"; }
miss() { printf '  [missing] %-12s %s\n' "$1" "$2"; }
first() { for c in "$@"; do command -v "$c" >/dev/null 2>&1 && { echo "$c"; return; }; [ -x "$c" ] && { echo "$c"; return; }; done; }

echo "Vitruvium — tool check"

c=$(first solidcraft-cli "/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli" "/c/Program Files/SolidCraft/solidcraft-cli.exe")
[ -n "$c" ] && ok SolidCraft "$c" || miss SolidCraft "https://solidcraft.io/download"

c=$(first gmsh)
if [ -n "$c" ]; then ok Gmsh "$c"
elif python3 -c "import gmsh" >/dev/null 2>&1; then ok Gmsh "python module (pip)"
else miss Gmsh "pip install --upgrade gmsh"; fi

c=$(first ccx ccx_2.23 ccx_2.22 ccx_2.21)
[ -n "$c" ] && ok CalculiX "$c" || miss CalculiX "see references/tools-setup.md (conda-forge, apt, or source)"

c=$(first freecadcmd FreeCADCmd "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd" "/Applications/FreeCAD.app/Contents/Resources/bin/FreeCADCmd")
[ -n "$c" ] && ok FreeCAD "$c" || miss FreeCAD "https://www.freecad.org/downloads.php"

c=$(first git);     [ -n "$c" ] && ok Git "$c"     || miss Git "https://git-scm.com/downloads"
c=$(first python3); [ -n "$c" ] && ok Python3 "$c" || miss Python3 "https://www.python.org/downloads/"
