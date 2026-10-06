"""Long Hime Cut: blunt bangs and chin-length sidelocks, waist-length blunt panels and a slim ribbon headband."""
from anime import cel_box, ring_shell
from anime_female import SIDES
from paint import k, scalp, solid

META = {"name": "Long Hime Cut", "gender": "female",
        "description": "A princess cut: blunt bangs, chin-length sidelocks, waist-length hair and a slim headband."}


def build(g):
    scalp(g, 5501, side_rows=7, back_rows=8, sideburn=0)
    ring_shell(g, 5502, side_rows=7, back_rows=8)
    # Blunt bangs in three panels so the cut line has a little depth.
    for i, (x, w, z) in enumerate(((-3.0, 3, -4.4), (0, 3, -4.3), (3.0, 3, -4.4))):
        panel = g.piece(f"fringe_{i}", "HEAD", (-w / 2, 0, -.5), (w, 3, 1), pivot=(x, -8.6, z))
        cel_box(panel, 5510 + i, ring=0)
    for side, sign in SIDES:
        lock = g.piece(f"{side}_sidelock", "HEAD", (-1, 0, -.5), (2, 8, 1), pivot=(4.25 * sign, -7.6, -3.4))
        cel_box(lock, 5520 + (sign > 0), ring=1)
        curtain = g.piece(f"{side}_curtain", "HEAD", (-.5, 0, -2.5), (1, 8, 5), pivot=(4.4 * sign, -7.8, 1.1), rotation=(0, 0, -2 * sign))
        cel_box(curtain, 5525 + (sign > 0), ring=1)
        band = g.piece(f"{side}_band", "HEAD", (-.5, 0, -1), (1, 3, 2), pivot=(4.7 * sign, -8.6, -2.3), inflate=.08)
        solid(band, "A", "plain", 5528, 2, edge=False)
    top = g.piece("band_top", "HEAD", (-4.5, -1, -1), (9, 1, 2), pivot=(0, -8.45, -2.3), inflate=.08)
    solid(top, "A", "plain", 5529, 2, edge=False)
    for f in top.sides:
        f.hline(0, f.w - 1, 0, k("A", 3))
    # Waist-length blunt panels: each a different length and tilt, so the hem steps rather than slabs.
    for i, (x, w, length, z, rz) in enumerate(((-3.6, 2, 18, 4.3, 3), (-1.9, 3, 20, 4.65, 1), (0, 3, 21, 4.3, 0),
                                                (1.9, 3, 19, 4.65, -1), (3.6, 2, 17, 4.3, -3))):
        panel = g.piece(f"back_{i}", "HEAD", (-w / 2, 0, -.5), (w, length, 1), pivot=(x, -7.8, z), rotation=(-3, 0, rz), motion="sway")
        cel_box(panel, 5530 + i, ring=1)
        for y in range(2, length):   # a parting shadow down each panel's edge keeps the panels apart
            panel.back.set(0, y, k("H", 1)), panel.front.set(w - 1, y, k("H", 1))
