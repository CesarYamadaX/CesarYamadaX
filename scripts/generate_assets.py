"""Generates the animated SVG assets for the CesarYamadaX profile README.

Usage: python3 generate_assets.py <output_dir> [portrait.jpg]
Without a portrait photo the VISUAL.MAP panel only cycles the data shapes.
Edit INFO / TYPING / RADARS below and re-run to update the cards.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

OUT = Path(sys.argv[1])
PHOTO = Path(sys.argv[2]) if len(sys.argv) > 2 else None
OUT.mkdir(parents=True, exist_ok=True)
random.seed(7)

# ----------------------------------------------------------------- content
INFO = [
    ("Subject", "César Yamada"),
    ("Role", "Data / AI Engineer"),
    ("Origin", "México"),
    ("Education", "Data Science & Math Eng · Tec de Monterrey"),
    ("Status", "Building + Analyzing + Learning"),
    ("ToolChain", "Antigravity · Git · OpenRouter"),
    ("Core.Lang", "Python · SQL · R · JavaScript"),
    ("Core.ML", "pandas · XGBoost · TensorFlow"),
    ("Core.Agents", "LangChain · MCP · RAG"),
    ("Core.BI", "Power BI · Tableau · DAX"),
    ("Core.Apps", "React Native · Flask · Streamlit"),
    ("Core.Database", "SQL Server · MySQL · MongoDB"),
    ("Core.Infra", "AWS · GCP · Stripe"),
    ("Grid.LinkedIn", "/in/cesaryamada"),
    ("Grid.GitHub", "CesarYamadaX"),
]
TYPING = [
    "César - Data / AI Engineer",
    "BI Specialist @ Honor México",
    "Data Science & Mathematics Engineer",
    "Building AI agents for BI",
]
HANDLE = "@CesarYamadaX"
# Radar axes are years of hands-on experience (max 4).
RADARS = [
    ("Data & BI", [("Python", 3), ("SQL", 3), ("Power BI", 3), ("Excel", 4),
                   ("Plotly", 3), ("R", 2), ("Tableau", 1)]),
    ("ML & AI", [("TensorFlow", 2), ("Keras", 2), ("XGBoost", 2), ("Statsmodels", 2),
                 ("SHAP", 1), ("LangChain", 2), ("AI tooling", 2)]),
]
RADAR_MAX = 4

THEMES = {
    "light": dict(win="#f6f8fc", bar="#ffffff", panel="#e9eff6", line="#d3dce8",
                  label="#7b8794", value="#1f2937", accent="#0e9aa7", dots="#3b9cf2",
                  typing="#3b9cf2", chip="#c9e9ee", muted="#9aa5b4",
                  radar="#1f8a4c", radar_fill="#1f8a4c", grid="#d3dce8"),
    "dark": dict(win="#0f1520", bar="#131b29", panel="#161f30", line="#27344a",
                 label="#7d8aa0", value="#dbe4f0", accent="#2dd4bf", dots="#8fd0ff",
                 typing="#8fd0ff", chip="#12363b", muted="#5f6c82",
                 radar="#34d399", radar_fill="#34d399", grid="#27344a"),
}
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------- dot shapes
S = 300  # shapes are drawn on an S x S canvas; pixel value = dot density


def canvas():
    im = Image.new("L", (S, S), 0)
    return im, ImageDraw.Draw(im)


def shape_bars():
    im, d = canvas()
    hs = [70, 110, 95, 150, 190]
    for i, h in enumerate(hs):
        x = 48 + i * 44
        d.rectangle([x, 250 - h, x + 28, 250], fill=90 + i * 22)
    d.line([30, 256, 275, 256], fill=255, width=3)
    d.line([30, 40, 30, 256], fill=255, width=3)
    pts = [(62 + i * 44, 250 - h - 22) for i, h in enumerate(hs)]
    d.line(pts, fill=255, width=4)
    for p in pts:
        d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=255)
    return im


def shape_database():
    im, d = canvas()
    for i, y in enumerate([196, 136, 76]):
        d.rectangle([70, y, 230, y + 40], fill=70)
        d.ellipse([70, y + 20, 230, y + 60], fill=70)
        d.arc([70, y + 20, 230, y + 60], 0, 180, fill=255, width=4)
        d.line([70, y, 70, y + 40], fill=255, width=3)
        d.line([230, y, 230, y + 40], fill=255, width=3)
        d.ellipse([70, y - 20, 230, y + 20], fill=0)
        d.ellipse([70, y - 20, 230, y + 20], outline=255, width=5)
        d.ellipse([110, y - 8, 190, y + 8], fill=150)
    return im


def shape_network():
    im, d = canvas()
    layers = [(60, 3), (150, 4), (240, 2)]
    nodes = []
    for x, n in layers:
        gap = 220 / n
        nodes.append([(x, 40 + gap / 2 + i * gap) for i in range(n)])
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                d.line([p, q], fill=170, width=3)
    for layer in nodes:
        for x, y in layer:
            d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=235)
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=90)
    return im


def shape_portrait(path, invert=False, grid=176):
    """Photo -> dots through error-diffusion dithering, which keeps facial detail.

    invert=False: dots mark the dark areas (for light backgrounds).
    invert=True:  dots mark the bright areas (for dark backgrounds).
    """
    rgb = Image.open(path).convert("RGB")
    # studio background = everything connected to the top corners
    marked = rgb.copy()
    for seed in ((2, 2), (rgb.width - 3, 2)):
        ImageDraw.floodfill(marked, seed, (255, 0, 255), thresh=40)
    r, g, b2 = marked.split()
    bg = Image.merge("RGB", (r.point(lambda v: 255 if v == 255 else 0),
                             g.point(lambda v: 255 if v == 0 else 0),
                             b2.point(lambda v: 255 if v == 255 else 0))).convert("L").point(lambda v: 255 if v == 255 else 0)
    im = rgb.convert("L")
    # square crop around head and collar
    w, h = im.size
    side = int(w * 0.84)
    box = ((w - side) // 2, int(h * 0.012), (w - side) // 2 + side, int(h * 0.012) + side)
    im, bg = im.crop(box), bg.crop(box)
    im = im.resize((grid * 2, grid * 2), Image.LANCZOS)
    bg = bg.resize((grid, grid), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
    im = ImageOps.autocontrast(im, cutoff=1)
    im = im.filter(ImageFilter.UnsharpMask(radius=9, percent=160, threshold=0))
    im = im.resize((grid, grid), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=0))
    if invert:
        tone = im.point(lambda v: int(255 * (1 - min(0.8, (v / 255) ** 1.7 * 0.95))))
    else:
        tone = im.point(lambda v: int(255 * (1 - min(0.8, (1 - v / 255) ** 1.7 * 1.05))))
    tone.paste(255, mask=bg)
    bits = tone.convert("1")  # Floyd-Steinberg dithering
    px = bits.load()
    cell = S / grid
    return [((x + 0.5) * cell + random.uniform(-0.25, 0.25), (y + 0.5) * cell + random.uniform(-0.25, 0.25))
            for y in range(grid) for x in range(grid) if px[x, y] == 0]


def stipple(im, step=3.0):
    px = im.load()
    pts = []
    y = step / 2
    while y < S:
        x = step / 2
        while x < S:
            jx = x + random.uniform(-1.1, 1.1)
            jy = y + random.uniform(-1.1, 1.1)
            v = px[min(S - 1, max(0, int(jx))), min(S - 1, max(0, int(jy)))]
            if random.random() < v / 255:
                pts.append((jx, jy))
            x += step
        y += step
    return pts


BASE_SHAPES = [stipple(f()) for f in (shape_bars, shape_database, shape_network)]
SHAPES_BY_THEME = {"light": list(BASE_SHAPES), "dark": list(BASE_SHAPES)}
if PHOTO:
    SHAPES_BY_THEME["light"].insert(0, shape_portrait(PHOTO, invert=False))
    SHAPES_BY_THEME["dark"].insert(0, shape_portrait(PHOTO, invert=True))
SUB = 4  # each shape is split into SUB layers that fade in one after another


def dots_path(pts):
    return "".join(f"M{x:.1f} {y:.1f}h.01" for x, y in pts)


# ---------------------------------------------------------- terminal card
def terminal(t):
    c = THEMES[t]
    SHAPES = SHAPES_BY_THEME[t]
    W, H = 1000, 560
    n = len(SHAPES)
    seg = 100 / n
    css = [
        f"text{{font-family:{MONO}}}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.15}}",
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}",
        "@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(300px)}}",
        "@keyframes type{0%{transform:translateX(0)}35%,82%{transform:translateX(410px)}100%{transform:translateX(0)}}",
        ".live{animation:blink 1.4s steps(1) infinite}",
        ".ok{animation:pulse 2.4s ease-in-out infinite}",
        ".scan{animation:scan 4s linear infinite}",
        ".cover{animation:type 4s steps(39) infinite}",
    ]
    nt = len(TYPING)
    for i in range(nt):
        a, b = i * 100 / nt, (i + 1) * 100 / nt
        # typing line i is visible only during its 4s slot
        if i == 0:
            css.append(f"@keyframes t{i}{{0%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}}}")
        else:
            css.append(f"@keyframes t{i}{{0%{{opacity:0}}{a:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}}}")
        css.append(f".t{i}{{animation:t{i} {nt * 4}s steps(1) infinite}}")
    dur = n * 4.5
    for i in range(n):
        a, b = i * seg, (i + 1) * seg
        for j in range(SUB):
            s0 = a + (0.6 + j * 1.3) * 4 / n
            s1 = s0 + 2.2 * 4 / n
            e0 = b - (3.2 - j * 0.5) * 4 / n
            e1 = e0 + 1.6 * 4 / n
            css.append(
                f"@keyframes s{i}{j}{{0%,{s0:.2f}%{{opacity:0}}{s1:.2f}%,{e0:.2f}%{{opacity:1}}"
                f"{e1:.2f}%,100%{{opacity:0}}}}"
            )
            css.append(f".s{i}{j}{{opacity:0;animation:s{i}{j} {dur}s linear infinite}}")

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="César Yamada - Data / AI Engineer, BI Specialist at Honor México">',
         "<style>" + "".join(css) + "</style>",
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{c["win"]}" stroke="{c["line"]}"/>',
         f'<path d="M1 13a12 12 0 0 1 12-12h{W-26}a12 12 0 0 1 12 12v35H1z" fill="{c["bar"]}"/>',
         f'<path d="M1 48.5h{W-2}" stroke="{c["line"]}"/>',
         '<circle cx="26" cy="25" r="6" fill="#ff5f57"/><circle cx="46" cy="25" r="6" fill="#febc2e"/>'
         '<circle cx="66" cy="25" r="6" fill="#28c840"/>',
         f'<text x="{W/2}" y="29" font-size="12" fill="{c["label"]}" text-anchor="middle">profile.py --live</text>']

    # left panel: dot matrix
    lx, ly, lw, lh = 24, 68, 372, 424
    o.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="6" fill="{c["panel"]}" stroke="{c["line"]}"/>')
    o.append(f'<path d="M{lx} {ly+34.5}h{lw}" stroke="{c["line"]}"/>')
    o.append(f'<text x="{lx+14}" y="{ly+22}" font-size="12" letter-spacing="1" fill="{c["accent"]}">VISUAL.MAP</text>')
    o.append(f'<text x="{lx+lw-14}" y="{ly+22}" font-size="9" fill="{c["muted"]}" text-anchor="end">300×300 / 1-BIT</text>')
    gx, gy = lx + (lw - S) / 2, ly + 62
    k = c["muted"]
    o.append(f'<path d="M{gx-14} {gy}v-12h12M{gx+S+2} {gy-12}h12v12M{gx-14} {gy+S}v12h12M{gx+S+2} {gy+S+12}h12v-12" '
             f'fill="none" stroke="{k}"/>')
    o.append(f'<g transform="translate({gx} {gy})">')
    o.append(f'<rect class="scan" x="0" y="0" width="{S}" height="1.5" fill="{c["accent"]}" opacity=".35"/>')
    for i, pts in enumerate(SHAPES):
        groups = [[] for _ in range(SUB)]
        for p in pts:
            groups[random.randrange(SUB)].append(p)
        for j, g in enumerate(groups):
            o.append(f'<path class="s{i}{j}" d="{dots_path(g)}" stroke="{c["dots"]}" stroke-width="{1.45 if len(pts) > 6000 else 1.9}" '
                     f'stroke-linecap="round" fill="none"/>')
    o.append("</g>")
    total = sum(len(p) for p in SHAPES)
    o.append(f'<text x="{lx+14}" y="{ly+lh-12}" font-size="9" fill="{c["muted"]}">PTS {total} · {len(SHAPES)} FRAMES / LOOP</text>')

    # right panel: system info
    rx, ry, rw, rh = 412, 68, 564, 424
    o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="6" fill="{c["panel"]}" stroke="{c["line"]}"/>')
    o.append(f'<path d="M{rx} {ry+34.5}h{rw}" stroke="{c["line"]}"/>')
    o.append(f'<text x="{rx+14}" y="{ry+22}" font-size="12" letter-spacing="1" fill="{c["accent"]}">SYSTEM.INFO</text>')
    o.append(f'<circle class="live" cx="{rx+rw-186}" cy="{ry+18}" r="3.5" fill="#ef4565"/>')
    o.append(f'<text x="{rx+rw-176}" y="{ry+22}" font-size="10" letter-spacing="1" fill="#ef4565">LIVE</text>')
    o.append(f'<rect x="{rx+rw-134}" y="{ry+7}" width="122" height="21" rx="10.5" fill="{c["chip"]}"/>')
    o.append(f'<text x="{rx+rw-73}" y="{ry+22}" font-size="11" fill="{c["accent"]}" text-anchor="middle">{esc(HANDLE)}</text>')
    y0, rowh = ry + 60, 22.5
    for i, (kk, v) in enumerate(INFO):
        y = y0 + i * rowh
        o.append(f'<text x="{rx+14}" y="{y:.1f}" font-size="12" fill="{c["label"]}">{esc(kk)}</text>')
        o.append(f'<text x="{rx+rw-16}" y="{y:.1f}" font-size="12.5" fill="{c["value"]}" text-anchor="end">{esc(v)}</text>')
    fy = ry + rh - 12
    o.append(f'<path d="M{rx+14} {fy-16.5}h{rw-28}" stroke="{c["line"]}"/>')
    o.append(f'<circle class="ok" cx="{rx+18}" cy="{fy-3}" r="4" fill="#10b981"/>')
    o.append(f'<text x="{rx+30}" y="{fy}" font-size="9" letter-spacing="1" fill="#10b981">ALL SYSTEMS NOMINAL</text>')
    o.append(f'<text x="{rx+rw-16}" y="{fy}" font-size="9" fill="{c["muted"]}" text-anchor="end">UTC-6 · MX NODE</text>')

    # typing line
    ty = 530
    o.append(f'<text x="34" y="{ty}" font-size="16" fill="{c["accent"]}">$</text>')
    for i, line in enumerate(TYPING):
        o.append(f'<text class="t{i}" x="56" y="{ty}" font-size="16" letter-spacing="1" fill="{c["typing"]}" '
                 f'opacity="{1 if i == 0 else 0}">{esc(line)}</text>')
    o.append(f'<g class="cover"><rect x="56" y="{ty-18}" width="600" height="26" fill="{c["win"]}"/>'
             f'<rect class="live" x="57" y="{ty-14}" width="9" height="17" fill="{c["typing"]}"/></g>')
    o.append("</svg>")
    (OUT / f"terminal-{t}.svg").write_text("\n".join(o), encoding="utf-8")


# ------------------------------------------------------------ radar chart
def radar(t):
    c = THEMES[t]
    W, H = 900, 400
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Skill radar: years of experience per tool">',
         f"<style>text{{font-family:{SANS}}}"
         "@keyframes grow{0%{transform:scale(.2);opacity:0}100%{transform:scale(1);opacity:1}}"
         ".poly{transform-box:fill-box;transform-origin:center;animation:grow 1.2s ease-out both}</style>",
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{c["win"]}" stroke="{c["line"]}"/>',
         f'<path d="M{W/2} 1v{H-2}" stroke="{c["line"]}"/>']
    R = 118
    for idx, (title, axes) in enumerate(RADARS):
        cx, cy = W / 4 + idx * W / 2, 218
        n = len(axes)
        ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
        o.append(f'<text x="{cx}" y="34" font-size="13" font-weight="700" fill="{c["value"]}" text-anchor="middle">{esc(title)}</text>')
        o.append(f'<text x="{cx}" y="50" font-size="9.5" fill="{c["label"]}" text-anchor="middle">years of hands-on experience</text>')
        for lvl in range(1, RADAR_MAX + 1):
            r = R * lvl / RADAR_MAX
            pts = " ".join(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}" for a in ang)
            o.append(f'<polygon points="{pts}" fill="none" stroke="{c["grid"]}" stroke-width="{1 if lvl < RADAR_MAX else 1.4}"/>')
        for a in ang:
            o.append(f'<path d="M{cx} {cy}L{cx + R*math.cos(a):.1f} {cy + R*math.sin(a):.1f}" stroke="{c["grid"]}"/>')
        vp = [(cx + R * v / RADAR_MAX * math.cos(a), cy + R * v / RADAR_MAX * math.sin(a))
              for (_, v), a in zip(axes, ang)]
        o.append('<g class="poly">')
        o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in vp)}" fill="{c["radar_fill"]}" '
                 f'fill-opacity=".18" stroke="{c["radar"]}" stroke-width="2" stroke-linejoin="round"/>')
        for x, y in vp:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{c["radar"]}"/>')
        o.append("</g>")
        for (name, v), a in zip(axes, ang):
            lx, ly = cx + (R + 18) * math.cos(a), cy + (R + 18) * math.sin(a)
            ca = math.cos(a)
            anchor = "middle" if abs(ca) < 0.3 else ("start" if ca > 0 else "end")
            if abs(ca) < 0.3:
                ly += -10 if math.sin(a) < 0 else 12
            o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="11.5" font-weight="600" fill="{c["value"]}" text-anchor="{anchor}">{esc(name)}</text>')
            o.append(f'<text x="{lx:.1f}" y="{ly+13:.1f}" font-size="9.5" fill="{c["label"]}" text-anchor="{anchor}">{v} yr{"s" if v != 1 else ""}</text>')
    o.append("</svg>")
    (OUT / f"signals-{t}.svg").write_text("\n".join(o), encoding="utf-8")


for theme in THEMES:
    terminal(theme)
    radar(theme)
for p in sorted(OUT.glob("*.svg")):
    print(p.name, p.stat().st_size // 1024, "KB")
