"""Messy Work Bun: hair twisted up in a hurry around a wooden stick, loose strands falling everywhere."""
from anime import ring_shell
from anime_female import paint, points, strand, swept_sides, SIDES
from paint import k, scalp, solid

META = {"name": "Messy Work Bun", "gender": "female",
        "description": "A loose bun twisted up around a wooden stick, with stray strands at the face and nape."}

# Tufts of the bun: (x, y, z, rx, rz, size); each sits at its own angle so the knot looks hastily wound.
TUFTS = [(0, -8.0, 4.6, -50, 6, (4, 2, 3)), (-1.0, -9.0, 4.0, -20, 30, (3, 2, 3)), (1.2, -8.8, 4.3, -30, -34, (3, 2, 3)),
         (.2, -9.7, 3.4, 10, 8, (3, 2, 2))]


def build(g):
    scalp(g, 7201, side_rows=8, back_rows=8, sideburn=0)
    swept_sides(g)
    hat = ring_shell(g, 7202, side_rows=3, back_rows=6)
    for i, (x, y, z, rx, rz, size) in enumerate(TUFTS):
        w, h, d = size
        tuft = g.piece(f"bun_tuft_{i}", "HEAD", (-w / 2, -h / 2, -d / 2), size, pivot=(x, y, z), rotation=(rx, 0, rz))
        paint(tuft, "cel", 7210 + i * 3, 2 + (i % 2), ring=0)
    stick = g.piece("bun_stick", "HEAD", (-4, -.5, -.5), (8, 1, 1), pivot=(.2, -8.9, 4.4), rotation=(10, 18, 28))
    solid(stick, "L", "leather", 7220, 3, edge=False)
    stick.front.set(0, 0, k("L", 1)), stick.front.set(7, 0, k("L", 4))
    strand(g, "bun_stray", (1.3, -9.6, 4.6), (40, 0, -40), ((1, 3), (1, 2)), 1, 7225, ring=None)
    points(g, "bang", [(-2.4, 3, 2, 2, 18), (.2, 2, 2, 2, -6), (2.4, 3, 2, 2, -20)], 7230, rx=-6)
    for side, sign in SIDES:
        strand(g, f"{side}_loose", (4.35 * sign, -7.6, -3.6), (0, 0, -(4 if sign < 0 else 9) * sign),
               ((1, 4), (1, 3, .5 * sign), (1, 2, -.3 * sign)), 1, 7240 + (sign > 0), texture="wave", motion="sway")
        strand(g, f"{side}_ear_strand", (4.4 * sign, -6.5, -.6), (10, 0, -6 * sign), ((1, 4), (1, 2)), 1, 7244 + (sign > 0),
               ring=None, motion="sway")
    for i, (x, rz, n) in enumerate(((-2.2, 14, 3), (.4, -4, 4), (2.6, -16, 3))):
        strand(g, f"nape_strand_{i}", (x, -2.4, 4.35), (10, 0, rz), ((1, n), (1, 1)), 1, 7250 + i, ring=None, motion="sway")
