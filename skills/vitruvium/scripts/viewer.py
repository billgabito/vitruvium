#!/usr/bin/env python3
"""Build the project's interactive 3D viewer: <project>/viewer.html (one self-contained file).

What the user can do in it: rotate / zoom / pan the part, standard views, section (cut) view along
X, Y or Z, switch each system/component on and off, show the FEA result (von Mises colour map,
deformed shape with a scale slider, supports and loads), and browse the full version history —
each version with what changed and why, its numbers, and the previous version as a ghost to compare.

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
    stamp = max([exp, os.path.getmtime(fea) if os.path.exists(fea) else 0, os.path.getmtime(idx) if os.path.exists(idx) else 0])
    return {"stamp": stamp, "exported": exp, "cad": cad, "stale": bool(lf) and cad > exp + 1}

def with_live(proj, versions):
    lf = live_files(proj)
    if lf:
        fea = os.path.join("05-simulation", "current")
        versions = versions + [{"version": "LIVE", "title": "Working copy (current CAD state)",
                                "why": "Updates automatically every time the model is exported.", "changes": [], "metrics": {},
                                "models": lf, "fea": fea if os.path.isdir(os.path.join(proj, fea)) else None, "date": ""}]
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
        out.append({k: e.get(k) for k in ("version", "title", "date", "why", "changes", "loop", "decision", "metrics")}
                   | {"models": models, "fea": fea})
    return out

HTML = r"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NAME__ · Vitruvium viewer</title>
<style>
:root{--parch:#F6EFDC;--ink:#2B2418;--sepia:#5A4A2A;--line:#E0D3B4}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 Inter,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--parch);display:flex;height:100vh;overflow:hidden}
aside{width:320px;min-width:260px;border-right:1px solid var(--line);overflow:auto;background:#FBF7EC}
aside h1{font-family:'Cormorant Garamond',Baskerville,Georgia,serif;letter-spacing:2px;font-size:22px;margin:14px 16px 4px}
aside .sub{margin:0 16px 10px;color:var(--sepia);font-size:12px}
.ver{margin:8px 10px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;cursor:pointer}
.ver.on{outline:2px solid #2A5CD6}.ver h3{margin:0;font-size:15px}.ver small{color:var(--sepia)}
.ver .why{border-left:3px solid #DC3C32;padding-left:8px;margin:6px 0}.ver ul{margin:4px 0 4px 18px;padding:0}
.ver table{font:12px 'JetBrains Mono',Menlo,monospace;border-collapse:collapse;margin-top:4px}.ver td{padding:1px 8px 1px 0}
main{flex:1;position:relative}canvas{display:block}
.panel{position:absolute;top:12px;right:12px;width:250px;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:12px;padding:10px 12px;max-height:calc(100% - 24px);overflow:auto}
.panel h4{margin:8px 0 4px;font-size:12px;letter-spacing:1px;color:var(--sepia);text-transform:uppercase}
.panel label{display:flex;gap:6px;align-items:center;margin:3px 0}.panel input[type=range]{width:100%}
.btns{display:flex;flex-wrap:wrap;gap:4px}.btns button{flex:1;padding:4px 6px;border:1px solid var(--line);background:#fff;border-radius:6px;cursor:pointer;font:inherit}
#legend{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:10px;padding:8px 10px;font:12px 'JetBrains Mono',Menlo,monospace;display:none}
#bar{width:220px;height:12px;border-radius:3px;background:linear-gradient(90deg,#2a5cd6,#18b2d6,#48be6e,#f2c428,#dc3c32)}
#banner{position:absolute;left:12px;top:12px;z-index:2;padding:6px 10px;border-radius:8px;font-size:12px;display:none}
#banner.live{display:block;background:#E6F4EA;color:#1E5631;border:1px solid #9FD3AE}#banner.stale{display:block;background:#FCE8E6;color:#8A1C14;border:1px solid #F1A39B}
#banner.snap{display:block;background:#fff;color:#5A4A2A;border:1px solid #E0D3B4}
#msg{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:var(--sepia)}
@media (max-width:760px){body{flex-direction:column}aside{width:100%;height:40vh}.panel{width:200px}}
</style>
<aside><h1>__NAME__</h1><p class="sub">Version history — click a version to open it. Newest first.</p><div id="list"></div></aside>
<main><div id="msg">Loading…</div><div id="banner"></div>
<div class="panel">
 <h4>View</h4><div class="btns"><button data-v="iso">Iso</button><button data-v="front">Front</button><button data-v="top">Top</button><button data-v="right">Right</button></div>
 <h4>Section</h4>
 <div class="btns"><button data-c="off">Off</button><button data-c="x">X</button><button data-c="y">Y</button><button data-c="z">Z</button></div>
 <input id="cut" type="range" min="0" max="1000" value="500"><label><input id="flip" type="checkbox">Flip side</label>
 <h4>Systems</h4><div id="layers"></div>
 <h4>Simulation</h4><div id="simbox"><small>No FEA for this version.</small></div>
 <h4>Compare</h4><label><input id="ghost" type="checkbox">Show previous version (blue ghost)</label>
</div>
<div id="legend"><div>von Mises [MPa] · nodal average</div><div id="bar"></div><div style="display:flex;justify-content:space-between"><span id="lo"></span><span id="hi"></span></div></div>
</main>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {STLLoader} from 'three/addons/loaders/STLLoader.js';
let DATA = __DATA__;
const main = document.querySelector('main');
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
renderer.localClippingEnabled = true; renderer.setPixelRatio(devicePixelRatio); main.prepend(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xF6EFDC);
scene.add(new THREE.HemisphereLight(0xffffff, 0x8a7a55, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(1, 2, 1.5); scene.add(sun);
const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 1e6); camera.up.set(0, 0, 1);
const head = new THREE.DirectionalLight(0xffffff, 1.4); head.position.set(0.3, 0.5, 1); camera.add(head); scene.add(camera);   // headlight: the side you look at is always lit
const controls = new OrbitControls(camera, renderer.domElement);
const plane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0); let cutAxis = 'off';
const root = new THREE.Group(), ghostRoot = new THREE.Group(); scene.add(root, ghostRoot);
let box = new THREE.Box3(), current = 0, layers = [], fea = null, feaMesh = null, bcGroup = null;

function resize(){ const w = main.clientWidth, h = main.clientHeight; renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }
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
        else n.material = solid(color); });
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
async function show(i, keepCamera = false){
  current = Math.min(i, DATA.versions.length - 1); i = current; const v = DATA.versions[i];
  document.querySelectorAll('.ver').forEach((el, k) => el.classList.toggle('on', k === i));
  root.clear(); ghostRoot.clear(); feaMesh = null; fea = v.fea;
  layers = await loadModels(v, root, false); unitFix(layers);
  const L = document.getElementById('layers'); L.innerHTML = layers.length ? '' : '<small>No geometry exported for this version.</small>';
  layers.forEach((l, k) => { const lab = document.createElement('label'); lab.innerHTML = `<input type="checkbox" checked> ${l.name}`;
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
  if (keepCamera){ const old = box.getSize(new THREE.Vector3()).length(); box = new THREE.Box3().setFromObject(root);
    const r = box.getSize(new THREE.Vector3()).length() / (old || 1);
    if (r > 1.3 || r < 0.7) fit(); else setCut(); }          // keep the user's camera unless the part changed size a lot
  else fit();
}
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function renderList(){
document.getElementById('list').innerHTML = DATA.versions.map((v, i) => {
  const p = DATA.versions[i + 1];
  const rows = Object.entries(v.metrics || {}).map(([k, x]) => `<tr><td>${esc(k)}</td><td>${esc(x)}</td><td>${p && p.metrics && p.metrics[k] !== undefined ? '← ' + esc(p.metrics[k]) : ''}</td></tr>`).join('');
  return `<div class="ver"><h3>${esc(v.version)} — ${esc(v.title)}</h3><small>${esc(v.date)}</small>` +
    (v.why ? `<div class="why"><b>Why:</b> ${esc(v.why)}</div>` : '') + (v.loop ? `<div><b>Loop:</b> ${esc(v.loop)}</div>` : '') +
    (v.decision ? `<div><b>Decision:</b> ${esc(v.decision)}</div>` : '') +
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
document.querySelectorAll('[data-c]').forEach(b => b.onclick = () => { cutAxis = b.dataset.c; setCut(); });
document.getElementById('cut').oninput = setCut; document.getElementById('flip').onchange = setCut;
document.getElementById('ghost').onchange = () => show(current);
resize(); renderer.setAnimationLoop(() => renderer.render(scene, camera));
// URL options to open a specific view: ?v=1&cut=y&pos=0.5&flip=1&ghost=1&sim=0&scale=0.5&view=top
const Q = new URLSearchParams(location.search);
if (Q.get('ghost') === '1') document.getElementById('ghost').checked = true;
if (DATA.versions.length) show(+(Q.get('v') || 0)).then(() => {
  if (Q.get('sim') === '0' && document.getElementById('simOn')){ const s = document.getElementById('simOn'); s.checked = false; s.onchange({target:s}); }
  if (Q.get('scale') && document.getElementById('scale')){ const s = document.getElementById('scale'); s.value = +Q.get('scale') * 1000; s.oninput({target:s}); }
  if (Q.get('view')) fit(Q.get('view'));
  if (Q.get('flip') === '1') document.getElementById('flip').checked = true;
  if (Q.get('cut')){ cutAxis = Q.get('cut'); document.getElementById('cut').value = (+(Q.get('pos') || .5)) * 1000; setCut(); }
}); else document.getElementById('msg').textContent = 'No versions logged yet.';
</script></html>"""

def data(proj):
    return {"versions": list(reversed(pack(proj, with_live(proj, load_versions(proj))))), "state": state(proj)}   # newest first

def build(proj):
    d = data(proj); versions = d["versions"]
    name = os.path.basename(proj.rstrip("/"))
    page = HTML.replace("__NAME__", name).replace("__DATA__", json.dumps(d, separators=(",", ":")))
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
