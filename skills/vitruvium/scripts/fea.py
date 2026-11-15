#!/usr/bin/env python3
"""Linear static FEA: STEP -> Gmsh (C3D10) -> CalculiX -> results (+ images if available).

Units: mm, N, MPa (E in MPa). Supports and loads are picked by bounding boxes, so no GUI is needed.

Example (cantilever fixed at x=0, 100 N down on the x=100 face):
  python3 fea.py part.step --out 05-simulation/run1 --E 210000 --nu 0.3 --size 2 \
      --fix "-0.1 -1e9 -1e9 0.1 1e9 1e9" --load "99.9 -1e9 -1e9 100.1 1e9 1e9 0 0 -100"

--fix  "xmin ymin zmin xmax ymax zmax"               nodes inside are fixed in x, y, z (repeatable)
--load "xmin ymin zmin xmax ymax zmax Fx Fy Fz"      total force spread equally on nodes inside (repeatable)
Writes job.inp, job.dat, job.frd, results.json and summary.md in --out; job.vtu and PNGs when
ccx2paraview and pyvista are installed.
"""
import argparse, json, math, os, re, shutil, subprocess, sys

def parse_box(s, n):
    v = [float(x) for x in s.split()]
    if len(v) != n:
        sys.exit(f"expected {n} numbers, got: {s!r}")
    return v

def inside(p, b):
    return b[0] <= p[0] <= b[3] and b[1] <= p[1] <= b[4] and b[2] <= p[2] <= b[5]

def mesh(step, size, order, out):
    """Mesh with the gmsh CLI (works for pip, uv, Homebrew or binary installs) and read back the .inp."""
    exe = os.environ.get("GMSH") or shutil.which("gmsh")
    if not exe:
        sys.exit("gmsh not found — see references/tools-setup.md")
    msh = os.path.join(out, "mesh.inp")
    r = subprocess.run([exe, step, "-3", "-order", str(order), "-clmax", str(size), "-clmin", str(size / 4),
                        "-format", "inp", "-o", msh], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(msh):
        sys.exit("gmsh failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    want = "C3D10" if order == 2 else "C3D4"
    nodes, elems, block = {}, [], None
    for line in open(msh):
        s = line.strip()
        if s.startswith("*"):
            u = s.upper().replace(" ", "")
            block = "N" if u.startswith("*NODE") else ("E" if u.startswith("*ELEMENT") and f"TYPE={want}" in u else None)
            continue
        if not s:
            continue
        v = [x for x in s.split(",") if x.strip()]
        if block == "N":
            nodes[int(v[0])] = tuple(float(x) for x in v[1:4])
        elif block == "E":
            elems.append([int(x) for x in v[1:]])
    if not elems:
        sys.exit(f"gmsh produced no {want} elements — is the STEP a closed solid?")
    return nodes, elems

def write_inp(path, nodes, elems, order, E, nu, fixes, loads):
    used = {n for e in elems for n in e}
    nodes = {k: v for k, v in nodes.items() if k in used}
    L = ["*HEADING", "Vitruvium FEA (mm, N, MPa)", "*NODE"]
    L += [f"{k}, {x:.6g}, {y:.6g}, {z:.6g}" for k, (x, y, z) in sorted(nodes.items())]
    L.append(f"*ELEMENT, TYPE={'C3D10' if order == 2 else 'C3D4'}, ELSET=EALL")
    L += [f"{i + 1}, " + ", ".join(map(str, e)) for i, e in enumerate(elems)]
    fixed = sorted({k for b in fixes for k, p in nodes.items() if inside(p, b)})
    if not fixed:
        sys.exit("no nodes inside the --fix box(es): check coordinates and units")
    L += ["*NSET, NSET=NFIX"] + [", ".join(map(str, fixed[i:i + 12])) for i in range(0, len(fixed), 12)]
    L += ["*MATERIAL, NAME=MAT", "*ELASTIC", f"{E}, {nu}", "*SOLID SECTION, ELSET=EALL, MATERIAL=MAT",
          "*STEP", "*STATIC", "*BOUNDARY", "NFIX, 1, 3, 0.0", "*CLOAD"]
    applied = []
    for b in loads:
        ln = [k for k, p in nodes.items() if inside(p, b[:6])]
        if not ln:
            sys.exit(f"no nodes inside --load box {b[:6]}")
        applied.append({"box": b[:6], "force_N": b[6:], "nodes": len(ln)})
        for d, F in enumerate(b[6:], 1):
            if F:
                L += [f"{k}, {d}, {F / len(ln):.8g}" for k in ln]
    L += ["*NODE FILE", "U", "*EL FILE", "S", "*NODE PRINT, NSET=NALL", "U", "*EL PRINT, ELSET=EALL", "S", "*END STEP"]
    alln = sorted(nodes)
    k = L.index("*MATERIAL, NAME=MAT")
    L[k:k] = ["*NSET, NSET=NALL"] + [", ".join(map(str, alln[i:i + 12])) for i in range(0, len(alln), 12)]
    open(path, "w").write("\n".join(L) + "\n")
    return len(nodes), len(fixed), applied

def ccx_cmd():
    for c in [os.environ.get("CCX", ""), "ccx", "ccx_2.23", "ccx_2.22", "ccx_2.21"]:
        if c and shutil.which(c):
            return c
    sys.exit("CalculiX (ccx) not found — see references/tools-setup.md")

def read_dat(path):
    """Max displacement magnitude and max von Mises (integration points) from job.dat."""
    umax, smax, mode = 0.0, 0.0, None
    num = re.compile(r"^\s*\d+(\s+\d+)?(\s+-?\d\.\d+E[+-]\d+)+\s*$")
    for line in open(path):
        if "displacements" in line: mode = "U"; continue
        if "stresses" in line: mode = "S"; continue
        if not num.match(line):
            continue
        v = line.split()
        if mode == "U" and len(v) == 4:
            umax = max(umax, math.sqrt(sum(float(x) ** 2 for x in v[1:])))
        elif mode == "S" and len(v) == 8:
            sx, sy, sz, sxy, sxz, syz = map(float, v[2:])
            vm = math.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (sxy ** 2 + sxz ** 2 + syz ** 2))
            smax = max(smax, vm)
    return umax, smax

def images(out):
    """Optional: .frd -> .vtu (ccx2paraview) -> PNGs (pyvista). Returns list of files or a reason."""
    try:
        import ccx2paraview, pyvista as pv
    except ImportError:
        return "images skipped: install ccx2paraview and pyvista (references/tools-setup.md)"
    ccx2paraview.Converter(os.path.join(out, "job.frd"), ["vtu"]).run()
    vtus = sorted(f for f in os.listdir(out) if f.endswith(".vtu"))
    if not vtus:
        return "images skipped: no .vtu produced"
    grid = pv.read(os.path.join(out, vtus[-1])); pv.OFF_SCREEN = True; files = []
    for name in grid.point_data.keys():
        if name.upper().startswith(("S", "U")):
            p = pv.Plotter(off_screen=True); p.add_mesh(grid, scalars=name, cmap="jet", show_edges=False)
            p.add_scalar_bar(title=name); f = os.path.join(out, f"{name.replace(' ', '_')}.png")
            p.screenshot(f); p.close(); files.append(os.path.basename(f))
    return files

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step"); ap.add_argument("--out", required=True)
    ap.add_argument("--E", type=float, required=True, help="Young's modulus, MPa")
    ap.add_argument("--nu", type=float, default=0.3); ap.add_argument("--size", type=float, required=True, help="max element size, mm")
    ap.add_argument("--order", type=int, choices=[1, 2], default=2)
    ap.add_argument("--fix", action="append", required=True); ap.add_argument("--load", action="append", required=True)
    ap.add_argument("--yield", dest="sy", type=float, help="yield strength, MPa, to report the safety factor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    nodes, elems = mesh(os.path.abspath(a.step), a.size, a.order, a.out)
    nn, nfix, applied = write_inp(os.path.join(a.out, "job.inp"), nodes, elems, a.order, a.E, a.nu,
                                  [parse_box(f, 6) for f in a.fix], [parse_box(l, 9) for l in a.load])
    r = subprocess.run([ccx_cmd(), "-i", "job"], cwd=a.out, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(os.path.join(a.out, "job.dat")):
        sys.exit("CalculiX failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    umax, smax = read_dat(os.path.join(a.out, "job.dat"))
    res = {"elements": len(elems), "nodes": nn, "element_type": "C3D10" if a.order == 2 else "C3D4",
           "mesh_size_mm": a.size, "fixed_nodes": nfix, "loads": applied, "E_MPa": a.E, "nu": a.nu,
           "max_displacement_mm": round(umax, 6), "max_von_mises_MPa": round(smax, 3)}
    if a.sy:
        res["safety_factor_yield"] = round(a.sy / smax, 2) if smax else None
    res["images"] = images(a.out)
    json.dump(res, open(os.path.join(a.out, "results.json"), "w"), indent=2)
    open(os.path.join(a.out, "summary.md"), "w").write(
        f"# FEA summary\n\n- Mesh: {res['elements']} {res['element_type']} elements, {nn} nodes, size {a.size} mm\n"
        f"- Material: E = {a.E} MPa, ν = {a.nu}\n- Max displacement: {umax:.4g} mm\n"
        f"- Max von Mises (integration points): {smax:.4g} MPa\n"
        + (f"- Safety factor on yield: {res['safety_factor_yield']}\n" if a.sy else "")
        + "\nCheck before trusting: mesh convergence (run 3 sizes), singularities at fixed edges and point loads,"
          " and agreement with the hand calculation (references/analysis.md).\n")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
