"""Construye los logos y la hoja de marca de Vitruvium. Uso: python3 generate.py && python3 board.py
Render a PNG con Chrome sin interfaz (ver README de brand)."""
import re, subprocess

SERIF = "'Cormorant Garamond', Baskerville, Georgia, serif"
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Menlo, monospace"
INK, PARCH, SEPIA, NIGHT, GOLD = "#2B2418", "#F6EFDC", "#5A4A2A", "#1E1A14", "#C9B98F"

def inner(svg):
    return re.sub(r"^<svg[^>]*>|</svg>$", "", svg).replace("<title>Vitruvium</title>", "")

def logo(mark_file, text, sub, bg=None, W=1400, H=380):
    bgr = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{bgr}'
            f'<svg x="20" y="20" width="340" height="340" viewBox="16 22 480 480">{inner(open(mark_file).read())}</svg>'
            f'<text x="400" y="210" font-family="{SERIF}" font-size="132" font-weight="600" letter-spacing="10" fill="{text}">VITRUVIUM</text>'
            f'<text x="406" y="272" font-family="{SANS}" font-size="34" letter-spacing="8" fill="{sub}">MECHANICAL DESIGNER</text></svg>')

open("logo.svg", "w").write(logo("mark.svg", INK, SEPIA))
open("logo-dark.svg", "w").write(logo("mark-light.svg", PARCH, GOLD, NIGHT))

PAL = [("Pergamino", PARCH, INK), ("Tinta", INK, PARCH), ("Sepia", SEPIA, PARCH), ("Noche", NIGHT, PARCH),
       ("Frío · seguro", "#2A5CD6", "#FFFFFF"), ("Cian", "#18B2D6", "#FFFFFF"), ("Verde", "#48BE6E", "#FFFFFF"),
       ("Ámbar · atención", "#F2C428", INK), ("Rojo · crítico", "#DC3C32", "#FFFFFF")]
W, H = 1800, 1220
t = lambda x, y, s, txt, f=SANS, c=SEPIA, extra="": f'<text x="{x}" y="{y}" font-family="{f}" font-size="{s}" fill="{c}" {extra}>{txt}</text>'
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#FBF7EC"/>',
     t(60, 90, 60, "VITRUVIUM · IDENTIDAD VISUAL", SERIF, INK, 'font-weight="600" letter-spacing="6"'),
     t(62, 130, 22, "El Hombre de Vitruvio como malla de elementos finitos: proporción, ingeniería y simplicidad."),
     '<image href="icon.svg" x="60" y="170" width="460" height="460"/>',
     '<image href="logo.svg" x="560" y="170" width="1180" height="320"/>',
     f'<rect x="560" y="470" width="1180" height="160" rx="16" fill="{NIGHT}"/>',
     '<image href="logo-dark.svg" x="580" y="480" width="520" height="141"/>',
     t(1180, 545, 20, "Versión sobre fondo oscuro", c=GOLD), t(1180, 575, 20, "Malla clara · marco dorado", c=GOLD)]
y = 690
s.append(t(60, y, 20, "PALETA", extra='font-weight="700" letter-spacing="3"'))
for i, (n, c, tc) in enumerate(PAL):
    x = 60 + i * 190
    s.append(f'<rect x="{x}" y="{y+20}" width="176" height="150" rx="12" fill="{c}" stroke="#D8CCAE"/>'
             + t(x + 14, y + 130, 17, n, c=tc, extra='font-weight="600"') + t(x + 14, y + 156, 16, c, MONO, tc))
s.append(t(60, y + 205, 18, "La escala de colores es la de un mapa de esfuerzos: azul = seguro, rojo = crítico. Úsela con ese significado, nunca como decoración."))
y = 945
s += [t(60, y, 20, "TIPOGRAFÍA", extra='font-weight="700" letter-spacing="3"'),
      t(60, y + 70, 56, "Cormorant Garamond", SERIF, INK, 'font-weight="600"'), t(60, y + 105, 18, "Nombre y títulos · clásica, romana"),
      t(60, y + 165, 40, "Inter — textos e interfaz", c=INK), t(60, y + 225, 30, "JetBrains Mono — σ = 142.6 MPa · FS 2.4", MONO, INK),
      t(1000, y, 20, "VARIANTES DEL ICONO", extra='font-weight="700" letter-spacing="3"')]
for i, (k, lab) in enumerate([("icon", "Color"), ("icon-dark", "Oscuro"), ("icon-mono", "Monocromo"), ("icon-small", "Pequeño")]):
    x = 1000 + i * 180
    s.append(f'<image href="{k}.svg" x="{x}" y="{y+25}" width="160" height="160"/>' + t(x + 80, y + 215, 17, lab, extra='text-anchor="middle"'))
s.append('<image href="icon-small.svg" x="1726" y="' + str(y + 120) + '" width="32" height="32"/>' + t(1742, y + 175, 14, "32 px", extra='text-anchor="middle"'))
open("brand-board.svg", "w").write("".join(s) + "</svg>")

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def render(name, w, h, transparent=True):
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}", f"--screenshot={name}.png"]
    if transparent: args.append("--default-background-color=00000000")
    subprocess.run(args + [f"file://{__import__('os').getcwd()}/{name}.svg"], capture_output=True)

for n, w, h in [("brand-board", W, H), ("logo", 1400, 380), ("logo-dark", 1400, 380), ("icon", 512, 512),
                ("icon-dark", 512, 512), ("icon-mono", 512, 512), ("icon-small", 512, 512)]:
    render(n, w, h)
