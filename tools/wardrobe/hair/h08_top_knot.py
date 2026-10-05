"""Top Knot: hair drawn up into a knot at the crown, bound with a metal band, temple strands loose."""
from paint import hair_box, k, scalp, shell, solid

META = {"name": "Top Knot", "description": "Pulled up into a crown knot with a metal band; two loose strands at the temples."}


def build(g):
    scalp(g, 701, side_rows=5, back_rows=8, sideburn=1)
    head = g.part("head")
    for y in range(8):   # combed up toward the knot
        head.top.set(3, y, "H1"), head.top.set(5, y, "H3")
    shell(g, 702, side_rows=3, back_rows=6, front=[(0, 1), (7, 1)])
    hat = g.part("hat")
    for f in (hat.right, hat.left, hat.back):
        for x in range(f.w):
            if x % 2:
                f.vline(x, 0, 1, "H3")
    band = g.piece("knot_band", "HEAD", (-1.5, -1, -1.5), (3, 1, 3), pivot=(0, -8.4, 1.6), inflate=.12)
    solid(band, "M", "smooth", 711, 2, edge=False)
    band.front.set(1, 0, "M4")
    # A rounded bun: a wide coil under a smaller crown.
    knot = g.piece("knot", "HEAD", (-2, -2, -2), (4, 2, 4), pivot=(0, -9.1, 1.8), rotation=(-12, 0, 4))
    hair_box(knot, 712, 2, sheen_row=0, top_delta=1)
    for f in knot.sides:
        f.set(1, 0, "H3"), f.set(2, 1, "H1")
    knot_top = g.piece("knot_top", "HEAD", (-1.5, -1, -1.5), (3, 1, 3), pivot=(.05, -10.9, 1.4), rotation=(-12, 0, 4))
    hair_box(knot_top, 713, 3, top_delta=1)
    for side, x, rz in (("right", -4.55, 5), ("left", 3.55, -5)):
        strand = g.piece(f"{side}_temple_strand", "HEAD", (0, 0, -.5), (1, 5, 1), pivot=(x, -7.4, -3.7), rotation=(0, 0, rz))
        hair_box(strand, 720 + (side == "left"), 2, sheen_row=0)
