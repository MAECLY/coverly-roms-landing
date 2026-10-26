#!/usr/bin/env python3
"""Draw the six-views window of the "More than covers" section.

  gen_views.py [--site site]

Rewrites <figure class="vw"> in site/index.html and site/en/index.html:
a drawn app window (toolbar, sidebar with system glyphs) whose eight
tiles (covers from assets/art/covers.svg, two missing slots from kit.svg)
sit in the Covers layout, plus each view's lines and slots, and the view
buttons with the app's view names (locales/{es,en}/ui.json, layouts.*).
It prints the tile layout table that site/assets/views.js carries in L;
paste it there when the numbers change.
"""

import sys, re
from pathlib import Path

def R(x, y, w, h): return f"M{x} {y}h{w}v{h}h-{w}z"
def H(x, y, x2): return f"M{x} {y}H{x2}"
def V(x, y, y2): return f"M{x} {y}V{y2}"
def g(x): return f"{x:g}"

TILES = [("c-02", 0), None, ("c-12", 2), ("c-15", 3), None, ("c-23", 5), ("c-31", 1), ("c-38", 4)]
SEL = 2
L = []
L.append([(160 + (i % 4) * 98, 50 + (i // 4) * 136, 1.9) for i in range(8)])
L.append([(156, 66 + i * 34, 0.7) for i in range(8)])
L.append([(452, 56, 2.8) if i == SEL else (312, 50 + i * 26, 0.5) for i in range(8)])
L.append([(279, 48, 5) if i == SEL else (210 + i * 36, 282, 0.9) for i in range(8)])
L.append([(156, 48 + i * 37, 0.75) for i in range(8)])
L.append([(160 + (i % 4) * 76, 66 + (i // 4) * 130, 1.9) for i in range(8)])

def deco():
    out = []
    # 0 covers: caption bars
    ln = "".join(R(x, y + 82, 44, 4) + R(x, y + 90, 26, 3) for x, y, _ in L[0])
    out.append(f'<g class="vd v0"><path class="ln" d="{ln}"/></g>')
    # 1 details
    rows = range(8)
    rl = H(148, 62.5, 560) + "".join(H(148, 62.5 + (i + 1) * 34, 560) for i in rows)
    ln = R(186, 50, 40, 5) + R(310, 50, 34, 5) + R(400, 50, 24, 5) + R(470, 50, 46, 5)
    ws = [110, 84, 120, 96, 70, 104, 88, 116]
    ic = ""
    ap = ""; ds = ""
    for i in rows:
        y = 62 + i * 34
        ln += R(186, y + 14, ws[i], 5) + R(326, y + 15, 40, 4) + R(400, y + 15, 26, 4)
        ic += R(310, y + 13, 11, 8)
        miss = TILES[i] is None
        for k, x in enumerate((470, 488, 506)):
            have = not miss and (k == 0 or (i + k) % 3 != 0)
            if have: ap += R(x, y + 12, 8, 10)
            else: ds += R(x + .5, y + 12.5, 7, 9)
    out.append(f'<g class="vd v1"><path class="rl" d="{rl}"/><path class="ln" d="{ln}"/><path class="ic" d="{ic}"/><path class="ap" d="{ap}"/><path class="dsh" d="{ds}"/></g>')
    # 2 columns
    rl = V(228.5, 36, 350) + V(308.5, 36, 350) + V(430.5, 36, 350)
    hl = R(148, 44, 80, 22) + R(229, 44, 79, 22) + R(309, 46 + SEL * 26, 121, 24)
    fl = ic = ""
    for i in range(9):
        ic += R(154, 51 + i * 26, 11, 8); fl += R(170, 53 + i * 26, [40, 30, 46, 36, 28, 42, 34, 38, 30][i], 4)
    for i in range(3):
        ic += R(236, 50 + i * 26, 12, 9); fl += R(254, 53 + i * 26, [30, 40, 24][i], 4)
    ln = ""
    for i in range(8):
        if i != SEL: ln += R(332, 57 + i * 26, [80, 64, 0, 72, 58, 84, 66, 76][i], 4)
    ln += R(332, 57 + SEL * 26, 70, 4) + R(452, 178, 84, 6) + R(452, 192, 60, 4) + R(452, 202, 70, 4) + R(452, 212, 52, 4)
    out.append(f'<g class="vd v2"><path class="hl" d="{hl}"/><path class="rl" d="{rl}"/><g class="v2f"><path class="ic" d="{ic}"/><path class="ln" d="{fl}"/></g><path class="ln" d="{ln}"/></g>')
    # 3 gallery
    hl = "M279.5 279.5h32v41h-32z"
    ln = R(446, 56, 96, 6) + R(446, 70, 70, 4) + R(446, 80, 80, 4)
    ap = R(446, 98, 10, 12) + R(446, 116, 10, 12) + R(446, 134, 10, 12)
    ln += R(462, 102, 40, 4) + R(462, 120, 46, 4) + R(462, 138, 36, 4)
    rl = H(148, 270.5, 560)
    out.append(f'<g class="vd v3"><path class="rl" d="{rl}"/><path class="sel" d="{hl}"/><path class="ln" d="{ln}"/><path class="ap" d="{ap}"/></g>')
    # 4 art slots
    ds = ""; ln = ""; rl = ""; tints = ""
    for i in range(8):
        y = 48 + i * 37
        miss = TILES[i] is None
        d = ""
        for k, x in enumerate((182, 226)):
            if miss or (i + k) % 4 == 3: ds += R(x + .5, y + .5, 39, 29)
            else: d += R(x, y, 40, 30)
        if d: tints += f'<path class="tint ink-{TILES[i][1]}" d="{d}"/>'
        ln += R(278, y + 9, [100, 80, 120, 90, 70, 110, 86, 96][i], 5) + R(278, y + 19, 50, 3)
        if i: rl += H(148, y - 3.5, 560)
    out.append(f'<g class="vd v4"><path class="rl" d="{rl}"/>{tints}<path class="dsh" d="{ds}"/><path class="ln" d="{ln}"/></g>')
    # 5 shelves
    rl = H(148, 143.5, 556) + H(148, 273.5, 556)
    cap = H(148, 143.5, 172) + H(148, 273.5, 172)
    ic = R(152, 48, 11, 8) + R(152, 178, 11, 8)
    ln = R(168, 50, 60, 5) + R(168, 180, 44, 5)
    pr = R(520, 50, 28, 4) + R(520, 180, 28, 4)
    out.append(f'<g class="vd v5"><path class="rule" d="{rl}"/><path class="cap" d="{cap}"/><path class="ic" d="{ic}"/><path class="ln" d="{ln}"/><path class="pr" d="{pr}"/></g>')
    return "".join(out)

def chrome():
    ch = R(0, 0, 560, 36) + R(0, 36, 140, 314)
    rl = H(0, 36.5, 560) + V(140.5, 36, 350)
    ln = R(16, 14, 70, 8)
    ic = ""; sb = ""
    for i in range(9):
        y = 50 + i * 30
        ic += (f"M14 {y}h14v10h-14zm3 2v6h8v-6z" if i % 2 else f"M16 {y-1}h10v12h-10zm2 2v5h6v-5z"); sb += R(36, y + 3, [56, 64, 44, 70, 50, 60, 40, 66, 48][i], 4) + R(112, y + 3, 16, 4)
    vb = "".join(f'<path class="vb b{k}" d="{R(258 + k * 22, 9, 18, 18)}"/>' for k in range(6))
    return (f'<path class="ch" d="{ch}"/><path class="hl" d="{R(6, 44, 128, 26)}"/><path class="rl" d="{rl}"/>'
            f'<path class="fld" d="M150.5 9.5h96v17h-96z"/><path class="ln" d="{ln}{sb}"/><path class="ic" fill-rule="evenodd" d="{ic}"/>{vb}'
            f'<path class="pr" d="{R(410, 9, 84, 18)}"/><path class="fld" d="M500.5 9.5h48v17h-48z"/>')

def tiles(pre):
    out = []
    for i, t in enumerate(TILES):
        x, y, s = L[0][i]
        tr = f'translate({g(x)} {g(y)})scale({g(s)})'
        inner = '<use class="gd" href="#hg"/>' + (f'<use class="ink-{t[1]}" href="{pre}assets/art/covers.svg#{t[0]}" width="30" height="40"/>' if t else f'<use class="gm" href="{pre}assets/art/kit.svg#sm" width="30" height="40"/>')
        out.append(f'<g class="vt" transform="{tr}">{inner}</g>')
    return "".join(out)

def svg(pre):
    return ('<svg class="art vw-art" viewBox="0 0 560 350" width="560" height="350" aria-hidden="true" focusable="false">'
            '<path class="fr" d="M8 .5h544a7.5 7.5 0 0 1 7.5 7.5v334a7.5 7.5 0 0 1-7.5 7.5H8A7.5 7.5 0 0 1 .5 342V8A7.5 7.5 0 0 1 8 .5z"/>'
            + chrome() + '<path class="fo" d="M8 .5h544a7.5 7.5 0 0 1 7.5 7.5v334a7.5 7.5 0 0 1-7.5 7.5H8A7.5 7.5 0 0 1 .5 342V8A7.5 7.5 0 0 1 8 .5z"/>'
            + deco() + tiles(pre) + '</svg>')

TXT = {
 "es": dict(pre="", group="Vistas de la biblioteca",
   label="Ilustración: una ventana de Coverly ROMs con los sistemas a la izquierda. Las mismas portadas cambian de sitio al pasar por las seis vistas.",
   views=[("Portadas", "Portadas: una cuadrícula, con un hueco discontinuo donde falta la portada."),
          ("Detalles", "Detalles: una tabla con las columnas que eliges y el arte que tiene cada juego."),
          ("Columnas", "Columnas: sistema, carpeta, juego y vista previa."),
          ("Galería", "Galería: el arte en grande y una tira con los demás juegos."),
          ("Huecos de arte", "Huecos de arte: portada, pantalla de título y captura, una al lado de otra."),
          ("Estantes", "Estantes: una fila por sistema.")],
),
 "en": dict(pre="../", group="Library views",
   label="Illustration: a Coverly ROMs window with the systems on the left. The same covers move into place as it steps through the six views.",
   views=[("Covers", "Covers: a grid, with a dashed slot where a cover is missing."),
          ("Details", "Details: a table with the columns you pick and the art each game has."),
          ("Columns", "Columns: system, folder, game and preview."),
          ("Gallery", "Gallery: large art with a filmstrip of the other games."),
          ("Art slots", "Art slots: cover, title screen and screenshot side by side."),
          ("Shelves", "Shelves: one row per system.")],
),
}

def figure(d):
    bs = "".join(f'<button class="btn btn-small" type="button" aria-pressed="{"true" if k == 0 else "false"}" data-say="{say}" hidden>{name}</button>'
                 for k, (name, say) in enumerate(d["views"]))
    return (f'<figure class="vw" data-v="0">\n<div class="vw-box" role="img" aria-label="{d["label"]}">{svg(d["pre"])}</div>\n'
            f'<div class="dm-ctl vw-ctl" role="group" aria-label="{d["group"]}">{bs}</div>\n'
            f'<figcaption class="demo-status vw-say">{d["views"][0][1]}</figcaption>\n</figure>')

def main(argv: list[str]) -> int:
    site = Path(argv[argv.index("--site") + 1]) if "--site" in argv else Path("site")
    for lang, rel in (("es", "index.html"), ("en", "en/index.html")):
        p = site / rel
        s = p.read_text(encoding="utf-8")
        m = re.search(r'<figure class="vw".*?</figure>', s, re.S)
        if not m:
            print(f"gen_views: no <figure class=\"vw\"> in {p}", file=sys.stderr)
            return 1
        p.write_text(s[:m.start()] + figure(TXT[lang]) + s[m.end():], encoding="utf-8")
    print(";".join(",".join(f"{g(x)} {g(y)} {g(s)}".replace("0.", ".") for x, y, s in v) for v in L))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
