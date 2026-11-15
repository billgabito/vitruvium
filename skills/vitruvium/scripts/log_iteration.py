#!/usr/bin/env python3
"""Record one design iteration: what changed, why, key numbers vs the previous iteration, and images.

Writes, inside the project folder:
  iterations/<version>/          copies of the images for this iteration
  iterations/index.json          all iterations (data)
  CHANGELOG.md                   human-readable log, newest first
  iterations/index.html          visual timeline (open in a browser)
  viewer.html                    interactive 3D viewer with the version history (viewer.py)

Example:
  python3 log_iteration.py --project ~/mechanical-projects/pump-motor-mount --version v0.3 \
    --title "Thicker base plate" --why "FEA: safety factor 1.4 < 2.0 required (loop: analysis -> model)" \
    --change "plate_t: 6 -> 8 mm" --change "fillet r: 2 -> 5 mm at the bend" \
    --loop "FEA failed -> parametric model" --decision "user chose B (bolted) on 2026-11-15" \
    --fea 05-simulation/v0.3 --metric "mass_kg=2.41" --metric "parts=7" \
    --image 03-model/v0.3.png --model 03-model/v0.3.glb
Metrics from --fea (results.json) are added automatically: max_von_mises_MPa, max_displacement_mm,
safety_factor_yield, elements.
"""
import argparse, datetime, html, json, os, shutil

KEYS = ["max_von_mises_MPa", "max_displacement_mm", "safety_factor_yield", "elements"]

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def delta(new, old):
    a, b = num(new), num(old)
    if a is None or b is None:
        return ""
    d = a - b
    pct = f" ({d / b * 100:+.0f}%)" if b else ""
    return f"{d:+.4g}{pct}"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True); ap.add_argument("--version", required=True)
    ap.add_argument("--title", required=True); ap.add_argument("--why", required=True, help="reason for the change")
    ap.add_argument("--change", action="append", default=[], help="what changed (repeatable)")
    ap.add_argument("--loop", default="", help="improvement loop that triggered it, if any")
    ap.add_argument("--decision", default="", help="user decision behind it, if any")
    ap.add_argument("--fea", help="folder with results.json from fea.py (relative to project or absolute)")
    ap.add_argument("--metric", action="append", default=[], help="name=value (repeatable)")
    ap.add_argument("--image", action="append", default=[], help="image to attach (repeatable)")
    ap.add_argument("--model", action="append", default=[], help="3D model of this version for the viewer: .glb/.gltf/.stl exported from SolidCraft (repeatable, one per system)")
    a = ap.parse_args()

    proj = os.path.abspath(os.path.expanduser(a.project))
    it_dir = os.path.join(proj, "iterations"); os.makedirs(os.path.join(it_dir, a.version), exist_ok=True)
    idx_path = os.path.join(it_dir, "index.json")
    index = json.load(open(idx_path)) if os.path.exists(idx_path) else []
    index = [e for e in index if e["version"] != a.version]           # re-logging a version replaces it

    metrics = {}
    if a.fea:
        rj = os.path.join(a.fea if os.path.isabs(a.fea) else os.path.join(proj, a.fea), "results.json")
        r = json.load(open(rj))
        metrics.update({k: r[k] for k in KEYS if r.get(k) is not None})
    for m in a.metric:
        k, _, v = m.partition("=")
        metrics[k.strip()] = num(v) if num(v) is not None else v.strip()

    images = []
    for img in a.image:
        src = img if os.path.isabs(img) else os.path.join(proj, img)
        if os.path.exists(src):
            dst = os.path.join(it_dir, a.version, os.path.basename(src)); shutil.copy2(src, dst)
            images.append(f"{a.version}/{os.path.basename(src)}")
        else:
            print(f"warning: image not found, skipped: {img}")

    prev = index[-1] if index else None
    entry = {"version": a.version, "date": datetime.date.today().isoformat(), "title": a.title, "why": a.why,
             "changes": a.change, "loop": a.loop, "decision": a.decision, "metrics": metrics, "images": images,
             "models": a.model, "fea": a.fea,
             "previous": prev["version"] if prev else None}
    index.append(entry)
    json.dump(index, open(idx_path, "w"), indent=2, ensure_ascii=False)

    # CHANGELOG.md — rebuilt from the index, newest first
    md = ["# Changelog", "", "Each iteration: what changed, why, and how the numbers moved. Visual timeline: `iterations/index.html`.", ""]
    for i in range(len(index) - 1, -1, -1):
        e, p = index[i], index[i - 1] if i else None
        md += [f"## {e['version']} — {e['title']} ({e['date']})", "", f"**Why:** {e['why']}"]
        if e["loop"]: md.append(f"**Loop:** {e['loop']}")
        if e["decision"]: md.append(f"**Decision:** {e['decision']}")
        if e["changes"]: md += ["", "**Changes:**"] + [f"- {c}" for c in e["changes"]]
        if e["metrics"]:
            md += ["", f"| Metric | {e['version']} | {p['version'] if p else '—'} | Δ |", "|---|---|---|---|"]
            for k, v in e["metrics"].items():
                old = p["metrics"].get(k, "—") if p else "—"
                md.append(f"| {k} | {v} | {old} | {delta(v, old)} |")
        if e["images"]: md += [""] + [f"![{os.path.basename(x)}](iterations/{x})" for x in e["images"]]
        md.append("")
    open(os.path.join(proj, "CHANGELOG.md"), "w").write("\n".join(md))

    # iterations/index.html — simple visual timeline, newest first
    cards = []
    for i in range(len(index) - 1, -1, -1):
        e, p = index[i], index[i - 1] if i else None
        rows = "".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(str(v))}</td>"
                       f"<td>{html.escape(str(p['metrics'].get(k, '—')) if p else '—')}</td>"
                       f"<td>{html.escape(delta(v, p['metrics'].get(k)) if p else '')}</td></tr>" for k, v in e["metrics"].items())
        imgs = "".join(f'<a href="{html.escape(x)}"><img src="{html.escape(x)}" alt=""></a>' for x in e["images"])
        ch = "".join(f"<li>{html.escape(c)}</li>" for c in e["changes"])
        extra = "".join(f"<p><b>{lbl}:</b> {html.escape(e[k])}</p>" for k, lbl in (("loop", "Loop"), ("decision", "Decision")) if e[k])
        cards.append(f'<section><h2>{html.escape(e["version"])} — {html.escape(e["title"])} <small>{e["date"]}</small></h2>'
                     f'<p class="why"><b>Why:</b> {html.escape(e["why"])}</p>{extra}<ul>{ch}</ul>'
                     + (f'<table><tr><th>Metric</th><th>{html.escape(e["version"])}</th><th>{html.escape(p["version"]) if p else "—"}</th><th>Δ</th></tr>{rows}</table>' if rows else "")
                     + f'<div class="imgs">{imgs}</div></section>')
    name = html.escape(os.path.basename(proj))
    open(os.path.join(it_dir, "index.html"), "w").write(f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} — iterations</title>
<style>body{{font:15px/1.5 Inter,Helvetica,Arial,sans-serif;background:#FBF7EC;color:#2B2418;max-width:980px;margin:0 auto;padding:24px 16px}}
h1{{font-family:'Cormorant Garamond',Baskerville,Georgia,serif;letter-spacing:2px}}section{{background:#fff;border:1px solid #E5D9BC;border-radius:12px;padding:16px 20px;margin:16px 0}}
h2{{margin:0 0 8px;font-size:19px}}small{{color:#5A4A2A;font-weight:400}}.why{{border-left:3px solid #DC3C32;padding-left:10px}}
table{{border-collapse:collapse;margin:8px 0;font-family:'JetBrains Mono',Menlo,monospace;font-size:13px}}td,th{{border:1px solid #E5D9BC;padding:4px 10px;text-align:left}}
.imgs{{display:flex;flex-wrap:wrap;gap:10px}}.imgs img{{max-width:300px;max-height:220px;border:1px solid #E5D9BC;border-radius:8px}}</style>
<h1>{name} · iterations</h1>{''.join(cards)}""")
    import viewer                                       # same folder: rebuild the interactive 3D viewer
    vpath, _ = viewer.build(proj)
    print(f"logged {a.version}: CHANGELOG.md, iterations/index.html and {os.path.basename(vpath)} updated ({len(index)} iterations)")

if __name__ == "__main__":
    main()
