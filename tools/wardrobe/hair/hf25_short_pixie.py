"""Short Pixie: cropped close at the sides and nape, a soft textured top and a long fringe swept across the brow."""
from anime import ring_shell
from anime_female import paint, pointed, strand, SIDES
from paint import scalp

META = {"name": "Short Pixie", "gender": "female",
        "description": "A close-cropped pixie with a soft textured top, a long swept fringe and pointed sideburns."}


def build(g):
    scalp(g, 7501, side_rows=5, back_rows=7, sideburn=1, part=5)
    hat = ring_shell(g, 7502, side_rows=3, back_rows=5)
    hat.top.vline(5, 0, 7, "H1")
    for i, (x, z, rx, rz) in enumerate(((-1.6, -1.2, -8, 10), (1.6, -.4, -10, -14), (0, 2.0, -18, 4))):
        top = g.piece(f"top_lock_{i}", "HEAD", (-1.5, -1, -2), (3, 1, 4), pivot=(x, -8.3, z), rotation=(rx, 0, rz))
        paint(top, "cel", 7505 + i * 3, 2, ring=None)
    strand(g, "sweep_0", (2.7, -8.7, -4.35), (-8, 0, 70), ((2, 5), (1, 1)), 1, 7510, ring=None)
    strand(g, "sweep_1", (1.0, -8.65, -4.35), (-8, 0, 58), ((2, 4), (1, 1)), 1, 7511, ring=None)
    pointed(g, "sweep_fall", (-4.2, -7.6, -3.7), (0, 0, 10), 2, 3, 2, seed=7512)
    for side, sign in SIDES:
        strand(g, f"{side}_sideburn", (4.25 * sign, -6.4, -2.6), (0, 0, -2 * sign), ((1, 3), (1, 1)), 1, 7520 + (sign > 0), ring=None)
    for i, (x, rz) in enumerate(((-2.4, 10), (0, 0), (2.4, -10))):
        strand(g, f"nape_point_{i}", (x, -2.6, 4.35), (12, 0, rz), ((2, 2), (1, 1)), 1, 7530 + i, ring=None)
