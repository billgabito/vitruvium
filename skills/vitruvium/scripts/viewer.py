#!/usr/bin/env python3
"""Build the project's interactive 3D viewer: <project>/viewer.html (one self-contained file).

What the user can do in it: rotate / zoom / pan the part, standard views, section (cut) view along
X, Y or Z, switch each system/component on and off, show the FEA result (von Mises colour map,
deformed shape with a scale slider, supports and loads), and browse the full version history —
each version with what changed and why, its numbers, and the previous version as a ghost to compare.

Look: engineering UI (Barlow, DIN-style), ISO 3098 lettering (osifont) for part IDs and annotations, Vitruvium logo and
favicon (assets/brand/), edges, ground grid, status bar with units, size and triangle count; parts list with IDs (parts.json),
ID labels in 3D, click-to-isolate, and an exploded view.

Data it reads (written by the other scripts):
  iterations/index.json            version list (log_iteration.py) with "models" and "fea" per version
  03-model/<file>.glb|.gltf|.stl   geometry exported from SolidCraft (one file per system/component, or one glTF with nodes)
  05-simulation/<run>/fea_view.json   FEA surface results (fea.py)

Usage: python3 viewer.py --project <folder> [--open]            static snapshot (viewer.html, can be shared)
       python3 viewer.py --project <folder> --serve --open      live: reloads automatically on every new export
Live working copy: export the CAD state to 03-model/current.glb (or .stl, or several files in 03-model/current/)
after every modelling change; FEA of the current state goes to 05-simulation/current/. A red banner warns when the
CAD file is newer than the export (the 3D view would be out of date).
Needs internet the first time it is opened (three.js loads from cdn.jsdelivr.net).
"""
import argparse, base64, json, os, subprocess, sys, webbrowser

def load_versions(proj):
    idx = os.path.join(proj, "iterations", "index.json")
    if os.path.exists(idx):
        return json.load(open(idx))
    # no iteration log yet: one version per model file found
    md = os.path.join(proj, "03-model")
    files = sorted(f for f in os.listdir(md) if f.lower().endswith((".glb", ".gltf", ".stl"))) if os.path.isdir(md) else []
    return [{"version": os.path.splitext(f)[0], "title": f, "why": "", "changes": [], "metrics": {},
             "models": [f"03-model/{f}"], "fea": None, "date": ""} for f in files]

MODEL_EXT = (".glb", ".gltf", ".stl")

def live_files(proj):
    """Working copy exported after every modelling change: 03-model/current.* or 03-model/current/*."""
    md = os.path.join(proj, "03-model")
    files = [os.path.join(md, f) for f in os.listdir(md) if f.startswith("current.") and f.lower().endswith(MODEL_EXT)] if os.path.isdir(md) else []
    cd = os.path.join(md, "current")
    if os.path.isdir(cd):
        files += [os.path.join(cd, f) for f in sorted(os.listdir(cd)) if f.lower().endswith(MODEL_EXT)]
    return files

def state(proj):
    """Freshness of the 3D view: newest export time, and whether the CAD file is newer than the export."""
    lf = live_files(proj)
    exp = max((os.path.getmtime(f) for f in lf), default=0)
    md = os.path.join(proj, "03-model")
    cad = max((os.path.getmtime(os.path.join(md, f)) for f in os.listdir(md) if f.endswith((".sc", ".solidcraft", ".json"))), default=0) if os.path.isdir(md) else 0
    fea = os.path.join(proj, "05-simulation", "current", "fea_view.json")
    idx = os.path.join(proj, "iterations", "index.json")
    mot = live_motion(proj)
    stamp = max([exp, os.path.getmtime(fea) if os.path.exists(fea) else 0, os.path.getmtime(idx) if os.path.exists(idx) else 0,
                 os.path.getmtime(mot) if mot else 0])
    return {"stamp": stamp, "exported": exp, "cad": cad, "stale": bool(lf) and cad > exp + 1}

def live_motion(proj):
    for f in (os.path.join(proj, "03-model", "current", "motion.json"), os.path.join(proj, "03-model", "motion.json")):
        if os.path.exists(f):
            return f
    return None

def live_parts(proj):
    for f in (os.path.join(proj, "03-model", "current", "parts.json"), os.path.join(proj, "03-model", "parts.json")):
        if os.path.exists(f):
            return f
    return None

def with_live(proj, versions):
    lf = live_files(proj)
    if lf:
        fea = os.path.join("05-simulation", "current")
        versions = versions + [{"version": "LIVE", "title": "Working copy (current CAD state)",
                                "why": "Updates automatically every time the model is exported.", "changes": [], "metrics": {},
                                "models": lf, "fea": fea if os.path.isdir(os.path.join(proj, fea)) else None, "date": "",
                                "motion": live_motion(proj), "parts": live_parts(proj)}]
    return versions

def pack(proj, versions):
    out = []
    for e in versions:
        models = []
        for m in e.get("models") or []:
            p = m if os.path.isabs(m) else os.path.join(proj, m)
            if os.path.exists(p):
                models.append({"name": os.path.splitext(os.path.basename(p))[0],
                               "type": os.path.splitext(p)[1].lower().lstrip("."),
                               "b64": base64.b64encode(open(p, "rb").read()).decode()})
            else:
                print(f"warning: model not found for {e['version']}: {m}")
        fea = None
        if e.get("fea"):
            f = os.path.join(proj, e["fea"], "fea_view.json") if not os.path.isabs(e["fea"]) else os.path.join(e["fea"], "fea_view.json")
            if os.path.exists(f):
                fea = json.load(open(f))
        motion = None
        if e.get("motion"):
            mp = e["motion"] if os.path.isabs(e["motion"]) else os.path.join(proj, e["motion"])
            if os.path.exists(mp):
                motion = json.load(open(mp))
            else:
                print(f"warning: motion file not found for {e['version']}: {e['motion']}")
        parts = None
        pp = e.get("parts")
        if pp:
            pp = pp if os.path.isabs(pp) else os.path.join(proj, pp)
            parts = json.load(open(pp)) if os.path.exists(pp) else None
        out.append({k: e.get(k) for k in ("version", "title", "date", "why", "changes", "loop", "decision", "metrics", "audit")}
                   | {"models": models, "fea": fea, "motion": motion, "parts": parts})
    return out

HTML = r"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NAME__ · Vitruvium</title><link rel="icon" type="image/png" href="__FAVICON__">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600&family=Cormorant+Garamond:wght@600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
@font-face{font-family:osifont;src:url(https://cdn.jsdelivr.net/gh/hikikomori82/osifont@master/osifont-lgpl3fe.woff) format('woff')}  /* ISO 3098 technical lettering */
:root{--iso:osifont,'Barlow Condensed',sans-serif;--ink:#2B2418;--sepia:#5A4A2A;--parch:#F6EFDC;--panel:#FBFAF6;--line:#DDD6C6;--muted:#7A6E57;--blue:#2A5CD6;--red:#DC3C32;--green:#2E7D4F;--mono:'JetBrains Mono',Menlo,monospace}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;font:13px/1.45 Barlow,'Helvetica Neue',Arial,sans-serif;color:var(--ink);background:var(--panel);display:grid;grid-template-rows:48px 1fr 26px;grid-template-columns:300px 1fr 268px;grid-template-areas:"top top top" "side view props" "status status status";overflow:hidden}
header{grid-area:top;display:flex;align-items:center;gap:14px;padding:0 14px;background:var(--ink);color:var(--parch)}
header img{width:30px;height:30px;border-radius:7px}
.brand{font-family:'Cormorant Garamond',Baskerville,Georgia,serif;font-weight:600;font-size:21px;letter-spacing:4px}
.brand small{display:block;font:500 8.5px Barlow,sans-serif;letter-spacing:2.4px;color:#C9B98F;margin-top:-4px}
.sep{width:1px;height:26px;background:#5A4A2A}
.proj{font-weight:600}.proj span{color:#C9B98F;font-weight:400;margin-left:8px;font-family:var(--mono);font-size:12px}
.grow{flex:1}
.badge{font:500 11px var(--mono);padding:3px 9px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
#banner.live{background:#E6F4EA;color:#1E5631}#banner.stale{background:#FCE8E6;color:#8A1C14}#banner.snap{background:#3A3122;color:#E8DCC2;border-color:#5A4A2A}
#auditBadge.ok{background:#E6F4EA;color:#1E5631}#auditBadge.no{background:#FCE8E6;color:#8A1C14}
aside{grid-area:side;border-right:1px solid var(--line);overflow:auto;background:var(--panel)}
.ph{position:sticky;top:0;background:var(--panel);padding:10px 14px 8px;border-bottom:1px solid var(--line);font:600 11px Barlow;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted);z-index:1}
.ver{margin:8px 10px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;cursor:pointer;transition:border-color .15s}
.ver:hover{border-color:#B9AE94}.ver.on{border-color:var(--blue);box-shadow:inset 3px 0 0 var(--blue)}
.ver h3{margin:0;font-size:13.5px;font-weight:600}.ver h3 code{font:500 12px var(--mono);color:var(--blue);margin-right:6px}
.ver small{color:var(--muted);font-family:var(--mono);font-size:11px}
.ver .why{border-left:2px solid var(--red);padding-left:8px;margin:6px 0;color:#3E3526}.ver ul{margin:4px 0 4px 16px;padding:0}
.ver table{font:11.5px var(--mono);border-collapse:collapse;margin-top:6px;width:100%}.ver td{padding:1px 6px 1px 0;border-top:1px dotted #E6E0D2}.ver td:first-child{color:var(--muted)}
main{grid-area:view;position:relative;background:linear-gradient(180deg,#EEF1F4 0%,#D9DFE5 100%)}canvas{display:block}
.props{grid-area:props;border-left:1px solid var(--line);overflow:auto;background:var(--panel)}
.grp{padding:10px 14px;border-bottom:1px solid var(--line)}
.grp h4{margin:0 0 7px;font:600 11px Barlow;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted)}
.grp label{display:flex;gap:7px;align-items:center;margin:4px 0;cursor:pointer}.grp input[type=range]{width:100%;accent-color:var(--blue)}
.grp input[type=checkbox]{accent-color:var(--blue)}
.seg{display:flex;border:1px solid var(--line);border-radius:7px;overflow:hidden;margin-bottom:6px}
.seg button,.btn{flex:1;padding:5px 4px;border:0;border-right:1px solid var(--line);background:#fff;cursor:pointer;font:500 12px Barlow;color:var(--ink)}
.seg button:last-child{border-right:0}.seg button:hover,.btn:hover{background:#F1ECE0}.seg button.on{background:var(--ink);color:var(--parch)}
.btn{border:1px solid var(--line);border-radius:7px;flex:none;padding:5px 12px}
select{font:500 12px Barlow;border:1px solid var(--line);border-radius:7px;padding:4px;background:#fff}
#legend{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.95);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font:11px var(--mono);display:none;box-shadow:0 1px 3px rgba(0,0,0,.06)}
#bar{width:230px;height:10px;border-radius:2px;background:linear-gradient(90deg,#2a5cd6,#18b2d6,#48be6e,#f2c428,#dc3c32);margin:4px 0 2px}
#card{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:min(560px,calc(100% - 24px));background:rgba(255,255,255,.97);border:1px solid var(--line);border-top:3px solid var(--ink);border-radius:8px;padding:10px 14px 12px;box-shadow:0 4px 16px rgba(43,36,24,.12);display:none;z-index:3}
#card .hd{display:flex;align-items:baseline;gap:10px}#card .cid{font:20px var(--iso);color:var(--blue)}#card .cn{font-weight:600;font-size:15px;flex:1}
#card .x{border:0;background:none;font-size:18px;cursor:pointer;color:var(--muted)}#card dl{display:grid;grid-template-columns:110px 1fr;gap:3px 10px;margin:8px 0 0;font-size:12.5px}
#card dt{color:var(--muted);font:600 10.5px Barlow;letter-spacing:1px;text-transform:uppercase;padding-top:2px}#card dd{margin:0}#card ul{margin:0;padding-left:16px}
#card .warn{color:#8A1C14;font-weight:600}
#msg{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:var(--muted)}
.mono{font-family:var(--mono)}
footer{grid-area:status;display:flex;gap:18px;align-items:center;padding:0 14px;border-top:1px solid var(--line);background:#F1ECE0;font:11px var(--mono);color:var(--sepia)}
footer b{font-weight:500;color:var(--ink)}
.tag{font:13px var(--iso);color:var(--ink);background:rgba(255,255,255,.92);border:1px solid var(--ink);border-radius:3px;padding:0 5px;white-space:nowrap;pointer-events:auto;cursor:pointer}
.tag.on{background:var(--ink);color:#fff}
.bom{width:100%;border-collapse:collapse;font-size:12px}.bom th{font:600 10.5px Barlow;letter-spacing:1px;text-transform:uppercase;color:var(--muted);text-align:left;padding:3px 4px;border-bottom:1px solid var(--line)}
.bom td{padding:3px 4px;border-bottom:1px dotted #E6E0D2;vertical-align:top}.bom td.id{font:13px var(--iso);white-space:nowrap}.bom tr{cursor:pointer}.bom tr:hover td{background:#F1ECE0}.bom tr.on td{background:#E3EBFB}
.bom small{color:var(--muted)}.pf{font-size:11.5px;margin-top:3px;color:#3E3526}.pf.warn{color:#8A1C14;font-weight:600}
.pfeat{margin:3px 0 0 14px;padding:0;font-size:11.5px;color:#3E3526}
#motlist div{padding:2px 0;border-top:1px dotted #E6E0D2;font-size:12px}
@media (max-width:900px){body{grid-template-columns:1fr;grid-template-rows:48px 38vh 1fr auto 26px;grid-template-areas:"top" "view" "props" "side" "status"}aside,.props{border:0}}
</style>
<header><img src="__FAVICON__" alt="Vitruvium"><div class="brand">VITRUVIUM<small>MECHANICAL DESIGNER</small></div><div class="sep"></div>
<div class="proj">__NAME__<span id="curVer"></span></div><div class="grow"></div><span id="auditBadge" class="badge"></span><span id="banner" class="badge"></span></header>
<aside><div class="ph"><span class="seg" style="margin:0"><button id="tabV" class="on">Versions</button><button id="tabP">Parts list</button></span></div>
<div id="list"></div><div id="bomWrap" style="display:none;padding:8px 10px"><div id="bom"></div><label style="margin-top:8px;display:flex;gap:6px"><input id="tags" type="checkbox" checked> Show part IDs in 3D</label></div></aside>
<main><div id="msg">Loading…</div><div id="card"></div>
<div id="legend"><div>von Mises [MPa] · nodal average</div><div id="bar"></div><div style="display:flex;justify-content:space-between"><span id="lo"></span><span id="hi"></span></div></div>
</main>
<div class="props">
 <div class="grp"><h4>View</h4><div class="seg"><button data-v="iso">Iso</button><button data-v="front">Front</button><button data-v="top">Top</button><button data-v="right">Right</button></div>
  <label style="justify-content:space-between">Exploded view <span class="mono" id="exv">0%</span></label><input id="explode" type="range" min="0" max="1000" value="0">
  <label><input id="edges" type="checkbox" checked> Edges</label><label><input id="grid" type="checkbox" checked> Ground grid</label></div>
 <div class="grp"><h4>Section</h4><div class="seg"><button data-c="off" class="on">Off</button><button data-c="x">X</button><button data-c="y">Y</button><button data-c="z">Z</button></div>
  <input id="cut" type="range" min="0" max="1000" value="500"><label><input id="flip" type="checkbox"> Flip side</label></div>
 <div class="grp"><h4>Systems</h4><div id="layers"></div></div>
 <div class="grp"><h4>Simulation</h4><div id="simbox"><small>No FEA for this version.</small></div></div>
 <div class="grp" id="motbox" style="display:none"><h4>Motion</h4>
  <div style="display:flex;gap:6px;margin-bottom:6px"><button id="play" class="btn">▶ Play</button><select id="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></div>
  <input id="pose" type="range" min="0" max="1000" value="0">
  <label><input id="hl" type="checkbox" checked> Highlight moving parts</label><label><input id="axes" type="checkbox" checked> Show joint axes</label>
  <div id="motlist"></div></div>
 <div class="grp"><h4>Compare</h4><label><input id="ghost" type="checkbox"> Previous version as blue ghost</label></div>
</div>
<footer><span>Units <b>mm · N · MPa</b></span><span>Size <b id="dims">—</b></span><span>Triangles <b id="tris">—</b></span><span id="expt"></span><span class="grow"></span><span>Vitruvium viewer</span></footer>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {STLLoader} from 'three/addons/loaders/STLLoader.js';
import {CSS2DRenderer, CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';
let DATA = __DATA__;
const main = document.querySelector('main');
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true, alpha:true});
const labeler = new CSS2DRenderer(); labeler.domElement.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none'; main.append(labeler.domElement);
renderer.localClippingEnabled = true; renderer.setPixelRatio(devicePixelRatio); main.prepend(renderer.domElement);
const scene = new THREE.Scene();   // background: CSS gradient behind a transparent canvas
scene.add(new THREE.HemisphereLight(0xffffff, 0x8a7a55, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(1, 2, 1.5); scene.add(sun);
const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 1e6); camera.up.set(0, 0, 1);
const head = new THREE.DirectionalLight(0xffffff, 1.4); head.position.set(0.3, 0.5, 1); camera.add(head); scene.add(camera);   // headlight: the side you look at is always lit
const controls = new OrbitControls(camera, renderer.domElement);
const plane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0); let cutAxis = 'off';
const root = new THREE.Group(), ghostRoot = new THREE.Group(); scene.add(root, ghostRoot);
let box = new THREE.Box3(), current = 0, layers = [], fea = null, feaMesh = null, bcGroup = null;

function resize(){ const w = main.clientWidth, h = main.clientHeight; renderer.setSize(w, h); labeler.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }
addEventListener('resize', resize);
const clip = () => cutAxis === 'off' ? [] : [plane];
// DoubleSide: correct shading even if an exported file has inverted normals, and the inside shows through a section cut
function solid(color){ return new THREE.MeshStandardMaterial({color, metalness:.1, roughness:.6, side:THREE.DoubleSide, clippingPlanes:clip()}); }
function b64(s){ const b = atob(s), a = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return a.buffer; }
const COLORS = [0xB9A27A, 0x7E9BB5, 0x9DB58A, 0xC99B7A, 0xA493B8, 0x86B3AE];
async function loadModels(ver, target, ghost){
  const out = [];
  for (const [i, m] of ver.models.entries()){
    let objs = [];
    if (m.type === 'stl'){ const g = new STLLoader().parse(b64(m.b64)); g.computeVertexNormals(); objs = [[m.name, new THREE.Mesh(g)]]; }
    else { const gl = await new GLTFLoader().parseAsync(b64(m.b64), ''); const kids = gl.scene.children.length > 1 ? gl.scene.children : [gl.scene];
           objs = kids.map((k, j) => [k.name || `${m.name} ${j + 1}`, k]); }
    for (const [name, o] of objs){
      const color = COLORS[(out.length) % COLORS.length];
      o.traverse(n => { if (!n.isMesh) return;
        if (ghost){ n.material = new THREE.MeshBasicMaterial({color:0x2A5CD6, transparent:true, opacity:.35, depthTest:false, depthWrite:false, clippingPlanes:clip()}); n.renderOrder = 10; }
        else { n.material = solid(color);
          const e = new THREE.LineSegments(new THREE.EdgesGeometry(n.geometry, 30), new THREE.LineBasicMaterial({color:0x2B2418, transparent:true, opacity:.55, clippingPlanes:clip()}));
          e.userData.edge = true; e.visible = document.getElementById('edges').checked; n.add(e); } });
      target.add(o); out.push({name, obj:o});
    }
  }
  return out;
}
function unitFix(objs){ // glTF is in metres by spec; FEA and STL from SolidCraft are in mm
  if (!fea || !objs.length) return; const b = new THREE.Box3(); objs.forEach(o => b.expandByObject(o.obj));
  const fb = new THREE.Box3().setFromArray(fea.pos); const r = fb.getSize(new THREE.Vector3()).length() / b.getSize(new THREE.Vector3()).length();
  if (r > 300 && r < 3000) objs.forEach(o => o.obj.scale.multiplyScalar(1000));
}
function jet(t){ const s = [[42,92,214],[24,178,214],[72,190,110],[242,196,40],[220,60,50]]; t = Math.min(1, Math.max(0, t)) * 4; const i = Math.min(3, Math.floor(t)), f = t - i;
  return s[i].map((c, k) => (c + f * (s[i + 1][k] - c)) / 255); }
function buildFea(scale){
  if (feaMesh){ root.remove(feaMesh); feaMesh.geometry.dispose(); }
  const n = fea.vm.length, pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
  let lo = Infinity, hi = -Infinity; for (const v of fea.vm){ if (v < lo) lo = v; if (v > hi) hi = v; }
  for (let i = 0; i < n; i++){ for (let k = 0; k < 3; k++) pos[3*i+k] = fea.pos[3*i+k] + scale * fea.u[3*i+k];
    const c = jet((fea.vm[i] - lo) / ((hi - lo) || 1)); col.set(c, 3 * i); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.setIndex(fea.tris); g.computeVertexNormals();
  feaMesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({vertexColors:true, roughness:.7, side:THREE.DoubleSide, clippingPlanes:clip(),
    polygonOffset:true, polygonOffsetFactor:-2, polygonOffsetUnits:-2}));   // drawn over the CAD surface, no flicker
  feaMesh.visible = document.getElementById('simOn').checked; root.add(feaMesh);
  document.getElementById('lo').textContent = lo.toFixed(1); document.getElementById('hi').textContent = hi.toFixed(1);
}
function buildBC(){
  bcGroup = new THREE.Group(); const size = new THREE.Box3().setFromArray(fea.pos).getSize(new THREE.Vector3()).length();
  const fb = new THREE.Box3().setFromArray(fea.pos);
  const clampBox = b => new THREE.Box3(new THREE.Vector3(...b.slice(0, 3)), new THREE.Vector3(...b.slice(3, 6))).intersect(fb.clone().expandByScalar(size * .01));
  for (const f of fea.fix){ const b = clampBox(f), s = b.getSize(new THREE.Vector3()).addScalar(size * .01);
    const m = new THREE.Mesh(new THREE.BoxGeometry(s.x, s.y, s.z), new THREE.MeshBasicMaterial({color:0x2A5CD6, transparent:true, opacity:.35}));
    m.position.copy(b.getCenter(new THREE.Vector3())); bcGroup.add(m); }
  for (const l of fea.loads){ const b = clampBox(l), F = new THREE.Vector3(l[6], l[7], l[8]); if (!F.length()) continue;
    const dir = F.clone().normalize(), c = b.getCenter(new THREE.Vector3()), L = size * .25;
    bcGroup.add(new THREE.ArrowHelper(dir, c.clone().addScaledVector(dir, -L), L, 0xDC3C32, L * .3, L * .15)); }
  bcGroup.visible = document.getElementById('bcOn').checked; root.add(bcGroup);
}
function fit(view = 'iso'){
  box = new THREE.Box3().setFromObject(root); if (box.isEmpty()) return;
  const c = box.getCenter(new THREE.Vector3()), v = THREE.MathUtils.degToRad(camera.fov), h = 2 * Math.atan(Math.tan(v / 2) * camera.aspect);
  const r = box.getSize(new THREE.Vector3()).length() / 2 / Math.sin(Math.min(v, h) / 2) * 1.05;   // whole part visible in any window shape
  const d = {iso:[1, -1.2, .9], front:[0, -1, 0], top:[0, -0.0001, 1], right:[1, 0, 0]}[view];
  camera.position.copy(c).add(new THREE.Vector3(...d).normalize().multiplyScalar(r)); camera.near = r / 1000; camera.far = r * 100;
  camera.updateProjectionMatrix(); controls.target.copy(c); controls.update(); setCut();
}
function setCut(){
  const ax = {x:0, y:1, z:2}[cutAxis];
  if (ax !== undefined){ const t = document.getElementById('cut').value / 1000, mn = box.min.getComponent(ax), mx = box.max.getComponent(ax);
    const n = new THREE.Vector3(); n.setComponent(ax, document.getElementById('flip').checked ? 1 : -1);
    plane.normal.copy(n); plane.constant = (document.getElementById('flip').checked ? -1 : 1) * (mn + t * (mx - mn)); }
  scene.traverse(o => { if (o.material) o.material.clippingPlanes = clip(); });
}
// ---------- exploded view ----------
let explodeK = 0, exploded = [];
function setupExplode(parts){
  const all = new THREE.Box3().setFromObject(root), c = all.getCenter(new THREE.Vector3()), size = all.getSize(new THREE.Vector3()).length();
  exploded = layers.map(l => { const b = new THREE.Box3().setFromObject(l.obj), lc = b.getCenter(new THREE.Vector3());
    const p = (parts || []).find(x => x.id === l.name);
    let dir = p && p.explode ? new THREE.Vector3(...p.explode).normalize() : lc.clone().sub(c);   // parts.json may give a direction
    if (dir.length() < 1e-6) dir.set(0, 0, 1); dir.normalize();
    return {obj:l.obj, basePos:l.obj.position.clone(), off:dir.multiplyScalar(size * .6)}; });
  applyExplode();
}
function explodeOffset(obj){ const e = exploded.find(x => x.obj === obj); return e ? e.off.clone().multiplyScalar(explodeK) : new THREE.Vector3(); }
function applyExplode(){
  for (const e of exploded) if (e.obj.matrixAutoUpdate) e.obj.position.copy(e.basePos).add(e.off.clone().multiplyScalar(explodeK));
  if (motion) applyPose(+document.getElementById('pose').value / 1000);
  if (axesGroup) axesGroup.visible = explodeK === 0 && document.getElementById('axes').checked;   // axes only make sense assembled
}
document.getElementById('explode').oninput = e => { explodeK = e.target.value / 1000; document.getElementById('exv').textContent = Math.round(explodeK * 100) + '%'; applyExplode(); };

// ---------- motion (see references/engineering/motion.md) ----------
let motion = null, moving = [], axesGroup = null, playing = false, phase = 0, lastT = 0;
function jointValue(j, s, seen = {}){
  if (j.follows){ const d = motion.joints.find(x => x.part === j.follows); if (!d || seen[j.part]) return 0; seen[j.part] = 1;
    return (j.ratio ?? 1) * jointValue(d, s, seen) + (j.offset ?? 0); }
  return j.range[0] + (j.range[1] - j.range[0]) * s;
}
function poseFromPhase(p){ return (motion.loop === 'cycle') ? p % 1 : 0.5 - 0.5 * Math.cos(2 * Math.PI * p); }
function kfMatrix(k, s){
  const t = k.t; let i = 0; while (i < t.length - 2 && s > t[i + 1]) i++;
  const f = Math.min(1, Math.max(0, (s - t[i]) / ((t[i + 1] - t[i]) || 1)));
  const tr = k.translate ? k.translate[i].map((v, n) => v + f * (k.translate[i + 1][n] - v)) : [0, 0, 0];
  const r0 = k.rotate ? k.rotate[i] : [0, 0, 1, 0], r1 = k.rotate ? k.rotate[i + 1] : [0, 0, 1, 0];
  const ax = new THREE.Vector3(r0[0] + f * (r1[0] - r0[0]), r0[1] + f * (r1[1] - r0[1]), r0[2] + f * (r1[2] - r0[2])).normalize();
  const ang = THREE.MathUtils.degToRad(r0[3] + f * (r1[3] - r0[3])), o = new THREE.Vector3(...(k.origin || [0, 0, 0]));
  return new THREE.Matrix4().makeTranslation(tr[0] + o.x, tr[1] + o.y, tr[2] + o.z)
    .multiply(new THREE.Matrix4().makeRotationAxis(ax, ang)).multiply(new THREE.Matrix4().makeTranslation(-o.x, -o.y, -o.z));
}
function applyPose(s){
  for (const m of moving){
    let M;
    if (m.kf) M = kfMatrix(m.kf, s);
    else if (m.j.type === 'prismatic'){ const a = new THREE.Vector3(...m.j.axis).normalize().multiplyScalar(jointValue(m.j, s)); M = new THREE.Matrix4().makeTranslation(a.x, a.y, a.z); }
    else { const o = new THREE.Vector3(...(m.j.origin || [0, 0, 0])), a = new THREE.Vector3(...m.j.axis).normalize();
      M = new THREE.Matrix4().makeTranslation(o.x, o.y, o.z).multiply(new THREE.Matrix4().makeRotationAxis(a, THREE.MathUtils.degToRad(jointValue(m.j, s))))
        .multiply(new THREE.Matrix4().makeTranslation(-o.x, -o.y, -o.z)); }
    const x = explodeOffset(m.obj);
    m.obj.matrix.copy(new THREE.Matrix4().makeTranslation(x.x, x.y, x.z).multiply(M).multiply(m.base)); m.obj.matrixWorldNeedsUpdate = true;
  }
}
function highlight(){
  const on = document.getElementById('hl').checked, ids = new Set(moving.map(m => m.obj));
  for (const l of layers) l.obj.traverse(n => { if (!n.isMesh) return; const mv = ids.has(l.obj);
    n.material.emissive?.setHex(on && mv ? 0x7a5200 : 0x000000); n.material.transparent = on && !mv; n.material.opacity = on && !mv ? .3 : 1; n.material.needsUpdate = true; });
  if (axesGroup) axesGroup.visible = document.getElementById('axes').checked;
}
function setupMotion(mo){
  motion = mo; moving = []; playing = false; phase = 0; document.getElementById('play').textContent = '▶ Play';
  if (axesGroup){ root.remove(axesGroup); axesGroup = null; }
  const box = document.getElementById('motbox');
  if (!mo){ box.style.display = 'none'; return; }
  const find = name => layers.find(l => l.name === name);
  const size = new THREE.Box3().setFromObject(root).getSize(new THREE.Vector3()).length(), rows = [];
  axesGroup = new THREE.Group();
  for (const j of mo.joints || []){ const l = find(j.part); if (!l){ rows.push(`<div>⚠ ${esc(j.part)}: no system with this name</div>`); continue; }
    l.obj.updateMatrix(); l.obj.matrixAutoUpdate = false; moving.push({obj:l.obj, base:l.obj.matrix.clone(), j});
    const a = new THREE.Vector3(...j.axis).normalize(), o = new THREE.Vector3(...(j.origin || l.obj.position.toArray()));
    if (j.type === 'prismatic') axesGroup.add(new THREE.ArrowHelper(a, new THREE.Box3().setFromObject(l.obj).getCenter(new THREE.Vector3()), Math.abs(j.range[1] - j.range[0]) || size * .2, 0x7F77DD, size * .04, size * .02));
    else { axesGroup.add(new THREE.ArrowHelper(a, o.clone().addScaledVector(a, -size * .15), size * .3, 0x7F77DD, size * .04, size * .02)); }
    const unit = j.type === 'prismatic' ? ' mm' : '°';
    rows.push(`<div><b>${esc(j.label || j.part)}</b> — ${esc(j.type)}${j.follows ? `, follows ${esc(j.follows)} ×${j.ratio ?? 1}` : `, ${j.range[0]}→${j.range[1]}${unit}`}</div>`); }
  for (const [name, k] of Object.entries(mo.keyframes || {})){ const l = find(name); if (!l){ rows.push(`<div>⚠ ${esc(name)}: no system with this name</div>`); continue; }
    l.obj.updateMatrix(); l.obj.matrixAutoUpdate = false; moving.push({obj:l.obj, base:l.obj.matrix.clone(), kf:k});
    rows.push(`<div><b>${esc(name)}</b> — path (${k.t.length} keyframes)</div>`); }
  root.add(axesGroup);
  document.getElementById('motlist').innerHTML = rows.join('') || '<small>No moving parts found.</small>';
  box.style.display = 'block'; highlight(); applyPose(0);
}
document.getElementById('play').onclick = () => { playing = !playing; document.getElementById('play').textContent = playing ? '❚❚ Pause' : '▶ Play';
  const s = document.getElementById('simOn'); if (playing && s && s.checked){ s.checked = false; s.onchange({target:s}); } };
document.getElementById('pose').oninput = e => { playing = false; document.getElementById('play').textContent = '▶ Play'; phase = 0; applyPose(e.target.value / 1000); };
document.getElementById('hl').onchange = highlight; document.getElementById('axes').onchange = highlight;
const ray = new THREE.Raycaster(); let downAt = null;
renderer.domElement.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 4) return;    // it was a rotation, not a click
  const r = renderer.domElement.getBoundingClientRect();
  ray.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1), camera);
  const hits = ray.intersectObjects(layers.map(l => l.obj), true).filter(h => h.object.isMesh && !h.object.userData.edge && h.object.visible &&
    (!h.object.material.clippingPlanes || !h.object.material.clippingPlanes.length || h.object.material.clippingPlanes[0].distanceToPoint(h.point) >= 0));
  if (!hits.length){ selectPart(null); return; }
  let o = hits[0].object; const owner = layers.find(l => { let x = o; while (x){ if (x === l.obj) return true; x = x.parent; } return false; });
  if (owner) selectPart(owner.name);
});

function tick(now){
  if (playing && motion){ const dt = Math.min(.1, (now - (lastT || now)) / 1000); phase += dt * (+document.getElementById('speed').value) / (motion.duration_s || 4);
    const s = poseFromPhase(phase); applyPose(s); document.getElementById('pose').value = s * 1000; }
  lastT = now; renderer.render(scene, camera); labeler.render(scene, camera);
}

async function show(i, keepCamera = false){
  current = Math.min(i, DATA.versions.length - 1); i = current; const v = DATA.versions[i];
  document.querySelectorAll('.ver').forEach((el, k) => el.classList.toggle('on', k === i));
  root.clear(); ghostRoot.clear(); feaMesh = null; fea = v.fea;
  layers = await loadModels(v, root, false); unitFix(layers);
  const L = document.getElementById('layers'); L.innerHTML = layers.length ? '' : '<small>No geometry exported for this version.</small>';
  layers.forEach((l, k) => { const lab = document.createElement('label'), pn = (v.parts || []).find(x => x.id === l.name);
    lab.innerHTML = `<input type="checkbox" checked> <span class="mono">${esc(l.name)}</span>${pn ? ' <small style="color:var(--muted)">' + esc(pn.name) + '</small>' : ''}`;
    lab.firstChild.onchange = e => { l.obj.visible = e.target.checked; }; L.appendChild(lab); });
  const sim = document.getElementById('simbox');
  if (fea){ sim.innerHTML = '<label><input id="simOn" type="checkbox" checked> von Mises stress</label><label><input id="bcOn" type="checkbox" checked> Supports and loads</label>Deformation ×<span id="sv">0</span><input id="scale" type="range" min="0" max="1000" value="0">';
    let umax = 1e-12; for (const v of fea.u) umax = Math.max(umax, Math.abs(v)); const size = new THREE.Box3().setFromArray(fea.pos).getSize(new THREE.Vector3()).length();
    const maxScale = size * .15 / umax;
    document.getElementById('scale').oninput = e => { const s = e.target.value / 1000 * maxScale; document.getElementById('sv').textContent = s.toFixed(0); buildFea(s); };
    document.getElementById('simOn').onchange = e => { feaMesh.visible = e.target.checked; document.getElementById('legend').style.display = e.target.checked ? 'block' : 'none'; };
    document.getElementById('bcOn').onchange = e => { bcGroup.visible = e.target.checked; };
    buildFea(0); buildBC(); document.getElementById('legend').style.display = 'block';
  } else { sim.innerHTML = '<small>No FEA for this version.</small>'; document.getElementById('legend').style.display = 'none'; }
  if (document.getElementById('ghost').checked && i + 1 < DATA.versions.length){ const g = await loadModels(DATA.versions[i + 1], ghostRoot, true); unitFix(g); }
  document.getElementById('msg').style.display = (layers.length || fea) ? 'none' : 'block';
  document.getElementById('msg').textContent = 'No geometry or FEA for this version.';
  explodeK = 0; document.getElementById('explode').value = 0; document.getElementById('exv').textContent = '0%';
  setupMotion(v.motion); setupParts(v.parts); setupExplode(v.parts); info(v);
  if (keepCamera){ const old = box.getSize(new THREE.Vector3()).length(); box = new THREE.Box3().setFromObject(root);
    const r = box.getSize(new THREE.Vector3()).length() / (old || 1);
    if (r > 1.3 || r < 0.7) fit(); else setCut(); }          // keep the user's camera unless the part changed size a lot
  else fit();
}
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let gridHelper = null, partTags = [];
function info(v){
  document.getElementById('curVer').textContent = v.version + (v.title ? ' — ' + v.title : '');
  const a = document.getElementById('auditBadge');
  if (v.version === 'LIVE'){ a.className = 'badge no'; a.textContent = 'NOT AUDITED · WORK IN PROGRESS'; }
  else if (v.audit){ const ok = /^APPROVED/i.test(v.audit); a.className = 'badge ' + (ok ? 'ok' : 'no'); a.textContent = (ok ? '✔ ' : '✖ ') + 'AUDIT: ' + v.audit.split(',')[0].toUpperCase(); }
  else { a.className = 'badge no'; a.textContent = 'AUDIT NOT RECORDED'; }
  const b = new THREE.Box3().setFromObject(root), s = b.getSize(new THREE.Vector3());
  document.getElementById('dims').textContent = b.isEmpty() ? '—' : `${s.x.toFixed(1)} × ${s.y.toFixed(1)} × ${s.z.toFixed(1)} mm`;
  let tri = 0; root.traverse(o => { if (o.isMesh && !o.userData.edge){ const g = o.geometry; tri += g.index ? g.index.count / 3 : g.attributes.position.count / 3; } });
  document.getElementById('tris').textContent = tri.toLocaleString();
  const st = (DATA.state || {}).exported; document.getElementById('expt').innerHTML = st ? `Export <b>${new Date(st * 1000).toLocaleString()}</b>` : '';
  if (gridHelper) scene.remove(gridHelper);
  if (!b.isEmpty()){ const n = Math.pow(10, Math.ceil(Math.log10(Math.max(s.x, s.y) * 2))) ; gridHelper = new THREE.GridHelper(n, 20, 0x8A97A6, 0xBAC3CD);
    gridHelper.rotation.x = Math.PI / 2; gridHelper.position.set(b.getCenter(new THREE.Vector3()).x, b.getCenter(new THREE.Vector3()).y, b.min.z - s.z * .02);
    gridHelper.material.transparent = true; gridHelper.material.opacity = .6; gridHelper.visible = document.getElementById('grid').checked; scene.add(gridHelper); }
}
// ---------- parts list (parts.json, see references/engineering/parts.md) ----------
function setupParts(parts){
  partTags.forEach(t => t.parent && t.parent.remove(t)); partTags = []; curParts = parts || []; selected = null; showCard(null);
  const el = document.getElementById('bom');
  if (!parts || !parts.length){ el.innerHTML = '<small>No parts list for this version (parts.json).</small>'; return; }
  const find = id => layers.find(l => l.name === id);
  el.innerHTML = '<table class="bom"><tr><th>ID</th><th>Name</th><th>Qty</th></tr>' + parts.map(p =>
    `<tr data-id="${esc(p.id)}"><td class="id">${esc(p.id)}</td><td>${esc(p.name)}<br><small>${esc([p.type, p.spec || p.standard, p.material, p.source].filter(Boolean).join(' · '))}</small>` +
    (p.function ? `<div class="pf"><b>Function:</b> ${esc(p.function)}${(p.requirements || []).length ? ' <small>(' + p.requirements.map(esc).join(', ') + ')</small>' : ''}</div>` : '') +
    (p.why ? `<div class="pf"><b>Why:</b> ${esc(p.why)}</div>` : `<div class="pf warn">⚠ No reason recorded — justify, merge or delete</div>`) +
    ((p.features || []).length ? '<ul class="pfeat">' + p.features.map(f => `<li>${esc(f.feature)} — <i>${esc(f.why)}</i></li>`).join('') + '</ul>' : '') +
    `</td><td class="mono">${esc(p.qty ?? 1)}</td></tr>`).join('') + '</table>';
  for (const p of parts){ const l = find(p.id); if (!l) continue;
    const d = document.createElement('div'); d.className = 'tag'; d.textContent = p.id; d.title = p.name; d.onclick = () => selectPart(p.id);
    const o = new CSS2DObject(d), b = new THREE.Box3().setFromObject(l.obj), at = b.getCenter(new THREE.Vector3()); at.z = b.max.z;
    l.obj.updateMatrixWorld(true); o.position.copy(l.obj.worldToLocal(at)); o.scale.setScalar(1);
    o.visible = document.getElementById('tags').checked; l.obj.add(o); partTags.push(o); }
  el.querySelectorAll('tr[data-id]').forEach(r => r.onclick = () => selectPart(r.dataset.id));
}
let selected = null, curParts = [];
function showCard(id){
  const c = document.getElementById('card'), p = curParts.find(x => x.id === id);
  if (!id){ c.style.display = 'none'; return; }
  const row = (k, v) => v ? `<dt>${k}</dt><dd>${v}</dd>` : '';
  const spec = [p && p.spec, p && p.standard].filter(Boolean).map(esc).join(' · ');
  c.innerHTML = `<div class="hd"><span class="cid">${esc(id)}</span><span class="cn">${esc(p ? p.name : 'Part without entry in parts.json')}</span><button class="x" title="Close">×</button></div>` + (p ? '<dl>' +
    row('Type', esc(p.type)) + row('Specification', spec) + row('Material', esc(p.material)) + row('Quantity', esc(p.qty ?? 1)) +
    row('Function', esc(p.function) + ((p.requirements || []).length ? ` <small>(${p.requirements.map(esc).join(', ')})</small>` : '')) +
    row('Why it exists', p.why ? esc(p.why) : '<span class="warn">⚠ No reason recorded — justify, merge or delete</span>') +
    row('Features', (p.features || []).length ? '<ul>' + p.features.map(f => `<li>${esc(f.feature)} — <i>${esc(f.why)}</i></li>`).join('') + '</ul>' : '') +
    row('Source', esc([p.source, p.supplier].filter(Boolean).join(' · '))) + row('Route', esc(p.route)) + row('Mass', p.mass_kg ? esc(p.mass_kg) + ' kg' : '') +
    row('Drawing', esc(p.drawing)) + '</dl>' : '<dl><dt>Note</dt><dd class="warn">Add this part to parts.json with its name, specification, function and reason.</dd></dl>');
  c.querySelector('.x').onclick = () => selectPart(null);
  c.style.display = 'block';
}
function selectPart(id){
  selected = (id === null || selected === id) ? null : id; showCard(selected);
  document.querySelectorAll('.bom tr[data-id]').forEach(r => r.classList.toggle('on', r.dataset.id === selected));
  partTags.forEach(t => t.element.classList.toggle('on', t.element.textContent === selected));
  for (const l of layers) l.obj.traverse(n => { if (!n.isMesh || n.userData.edge) return;
    const dim = selected && l.name !== selected; n.material.transparent = dim; n.material.opacity = dim ? .15 : 1; n.material.needsUpdate = true; });
}
document.getElementById('tabV').onclick = () => { tabV.classList.add('on'); tabP.classList.remove('on'); list.style.display = ''; bomWrap.style.display = 'none'; };
document.getElementById('tabP').onclick = () => { tabP.classList.add('on'); tabV.classList.remove('on'); list.style.display = 'none'; bomWrap.style.display = ''; };
document.getElementById('tags').onchange = e => partTags.forEach(t => t.visible = e.target.checked);
document.getElementById('edges').onchange = e => root.traverse(o => { if (o.userData.edge) o.visible = e.target.checked; });
document.getElementById('grid').onchange = e => { if (gridHelper) gridHelper.visible = e.target.checked; };

function renderList(){
document.getElementById('list').innerHTML = DATA.versions.map((v, i) => {
  const p = DATA.versions[i + 1];
  const rows = Object.entries(v.metrics || {}).map(([k, x]) => `<tr><td>${esc(k)}</td><td>${esc(x)}</td><td>${p && p.metrics && p.metrics[k] !== undefined ? '← ' + esc(p.metrics[k]) : ''}</td></tr>`).join('');
  return `<div class="ver"><h3><code>${esc(v.version)}</code>${esc(v.title)}</h3><small>${esc(v.date)}</small>` +
    (v.why ? `<div class="why"><b>Why:</b> ${esc(v.why)}</div>` : '') + (v.loop ? `<div><b>Loop:</b> ${esc(v.loop)}</div>` : '') +
    (v.decision ? `<div><b>Decision:</b> ${esc(v.decision)}</div>` : '') +
    (v.version === 'LIVE' ? '<div style="color:#8A1C14"><b>Not audited yet</b> — work in progress</div>' :
      v.audit ? `<div style="color:${/^APPROVED/i.test(v.audit) ? '#1E5631' : '#8A1C14'}"><b>Audit:</b> ${esc(v.audit)}</div>` : '<div style="color:#8A1C14"><b>Audit:</b> not recorded</div>') +
    ((v.changes || []).length ? `<ul>${v.changes.map(c => `<li>${esc(c)}</li>`).join('')}</ul>` : '') + (rows ? `<table>${rows}</table>` : '') + '</div>'; }).join('');
document.querySelectorAll('.ver').forEach((el, i) => el.onclick = () => show(i));
document.querySelectorAll('.ver').forEach((el, k) => el.classList.toggle('on', k === current));
}
renderList();
function banner(){
  const b = document.getElementById('banner'), s = DATA.state || {}, t = s.exported ? new Date(s.exported * 1000).toLocaleTimeString() : '—';
  const live = location.protocol.startsWith('http');
  if (s.stale){ b.className = 'stale'; b.textContent = 'Out of date: the CAD model changed after the last export — re-export to see the current design.'; }
  else if (live){ b.className = 'live'; b.textContent = `● Live — last export ${t}`; }
  else { b.className = 'snap'; b.textContent = `Snapshot — open with viewer.py --serve for live updates`; }
}
banner();
let stamp = (DATA.state || {}).stamp;
if (location.protocol.startsWith('http')) setInterval(async () => {   // live mode: reload when a new export appears
  try { const s = await (await fetch('state', {cache:'no-store'})).json();
    if (s.stamp !== stamp){ stamp = s.stamp; DATA = await (await fetch('data.json', {cache:'no-store'})).json(); renderList(); await show(current, true); }
    DATA.state = s; banner(); } catch (e) { const b = document.getElementById('banner'); b.className = 'stale'; b.textContent = 'Live server not reachable — the view may be out of date.'; }
}, 1500);
document.querySelectorAll('[data-v]').forEach(b => b.onclick = () => fit(b.dataset.v));
document.querySelectorAll('[data-c]').forEach(b => b.onclick = () => { cutAxis = b.dataset.c; setCut();
  document.querySelectorAll('[data-c]').forEach(x => x.classList.toggle('on', x === b)); });
document.getElementById('cut').oninput = setCut; document.getElementById('flip').onchange = setCut;
document.getElementById('ghost').onchange = () => show(current);
resize(); renderer.setAnimationLoop(tick);
// URL options to open a specific view: ?v=1&cut=y&pos=0.5&flip=1&ghost=1&sim=0&scale=0.5&view=top&pose=0.5&play=1
const Q = new URLSearchParams(location.search);
if (Q.get('ghost') === '1') document.getElementById('ghost').checked = true;
if (DATA.versions.length) show(+(Q.get('v') || 0)).then(() => {
  if (Q.get('sim') === '0' && document.getElementById('simOn')){ const s = document.getElementById('simOn'); s.checked = false; s.onchange({target:s}); }
  if (Q.get('scale') && document.getElementById('scale')){ const s = document.getElementById('scale'); s.value = +Q.get('scale') * 1000; s.oninput({target:s}); }
  if (Q.get('view')) fit(Q.get('view'));
  if (Q.get('flip') === '1') document.getElementById('flip').checked = true;
  if (Q.get('explode')){ const s = document.getElementById('explode'); s.value = +Q.get('explode') * 1000; s.oninput({target:s}); }
  if (Q.get('tab') === 'parts') document.getElementById('tabP').click();
  if (Q.get('select')) selectPart(Q.get('select'));
  if (Q.get('pose') && motion){ document.getElementById('pose').value = +Q.get('pose') * 1000; applyPose(+Q.get('pose')); }
  if (Q.get('play') === '1' && motion) document.getElementById('play').click();
  if (Q.get('cut')){ cutAxis = Q.get('cut'); document.getElementById('cut').value = (+(Q.get('pos') || .5)) * 1000; setCut(); }
}); else document.getElementById('msg').textContent = 'No versions logged yet.';
</script></html>"""

def data(proj):
    return {"versions": list(reversed(pack(proj, with_live(proj, load_versions(proj))))), "state": state(proj)}   # newest first

def build(proj):
    d = data(proj); versions = d["versions"]
    name = os.path.basename(proj.rstrip("/"))
    fav = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "brand", "icon-128.png")
    favicon = "data:image/png;base64," + base64.b64encode(open(fav, "rb").read()).decode() if os.path.exists(fav) else ""
    page = HTML.replace("__FAVICON__", favicon).replace("__NAME__", name).replace("__DATA__", json.dumps(d, separators=(",", ":")))
    path = os.path.join(proj, "viewer.html"); open(path, "w").write(page)
    return path, len(versions)

def serve(proj, port, open_it):
    """Live mode: the page polls /state and reloads the model as soon as a new export appears."""
    import http.server, socketserver
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=proj, **k)
        def log_message(self, *a): pass
        def _json(self, obj):
            b = json.dumps(obj, separators=(",", ":")).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if self.path.startswith("/state"): return self._json(state(proj))
            if self.path.startswith("/data.json"): return self._json(data(proj))
            if self.path in ("/", "/index.html"): build(proj); self.path = "/viewer.html"
            return super().do_GET()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), H) as srv:
        url = f"http://127.0.0.1:{port}/"
        print(f"live viewer: {url}  (Ctrl+C to stop)", flush=True)
        if open_it: webbrowser.open(url)
        srv.serve_forever()

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True); ap.add_argument("--open", action="store_true")
    ap.add_argument("--serve", action="store_true", help="live mode: local server, auto-reload on every new export")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    proj = os.path.abspath(os.path.expanduser(a.project))
    path, n = build(proj)
    print(f"viewer: {path} ({n} versions)")
    if a.serve:
        serve(proj, a.port, a.open)
    elif a.open:
        webbrowser.open("file://" + path)

if __name__ == "__main__":
    main()
