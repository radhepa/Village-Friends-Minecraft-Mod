"""Half-Up Bun: the top half gathered into a small bun, the rest falling to the shoulders."""
from anime import back_fan, bangs, cel_box, ring_shell, sidelocks
from paint import scalp, solid

META = {"name": "Half-Up Bun", "gender": "male", "description": "A small bun from the top half of the hair; the rest falls loose to the shoulders."}


def build(g):
    scalp(g, 2101, side_rows=7, back_rows=8, sideburn=0, part=5)
    ring_shell(g, 2102, side_rows=6, back_rows=8)
    bangs(g, "bang", [(-4.15, ((2, 4), (1, 1)), 10), (-1.6, ((3, 2), (1, 1)), 14), (0.8, ((3, 2), (1, 1)), 6), (3.1, ((2, 2), (1, 1)), -6)], 2110)
    sidelocks(g, "sidelock", 8, 2120, flare=3)
    bun = g.piece("bun", "HEAD", (-1.5, -1.5, -1.5), (3, 3, 3), pivot=(0, -7.6, 4.9), rotation=(10, 0, 0))
    cel_box(bun, 2130, ring=0)
    band = g.piece("bun_band", "HEAD", (-1.5, -.5, -1), (3, 1, 2), pivot=(0, -7.6, 3.9), inflate=.1)
    solid(band, "M", "smooth", 2131, 3, edge=False)
    back_fan(g, "fall", [(-3.0, ((3, 8), (2, 1), (1, 1)), 5, 6), (0, ((3, 9), (2, 1), (1, 1)), 0, 5), (3.0, ((3, 8), (2, 1), (1, 1)), -5, 6)],
             2140, z=4.3)
