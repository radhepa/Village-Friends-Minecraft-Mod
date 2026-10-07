"""Combed Side Part: a deep part on the wearer's left, the front combed across in glossy locks that
dip over the right temple, the crown combed back, short tidy sides and a neat tapered nape."""
from anime_male import chain, clump, combed_face, fade, hat_ring, plate, taper
from paint import scalp

META = {"name": "Combed Side Part", "gender": "male",
        "description": "A deep side part with the front combed across in glossy locks, short tidy sides."}

# (z, thickness, length across the crown)
SWEEP = [(-3.25, 2, 8), (-1.7, 1, 8), (-.15, 1, 7)]


def build(g):
    scalp(g, 3301, side_rows=5, back_rows=7, sideburn=1)
    head = g.part("head")
    for face, rows in ((head.right, 5), (head.left, 5), (head.back, 7)):
        fade(face, 3302 + face.x0, rows - 2, rows - 1, base=1, start=.9, end=.45)
    hat = hat_ring(g, 3303, rows={"back": 5, "right": 2, "left": 2})
    combed_face(hat.top, 3304, 3)
    hat.top.vline(6, 0, 7, "H0")
    hat.front.hline(0, 7, 0, "H2")
    # Locks combed from the part across the front of the crown, then down over the right temple.
    for i, (z, thick, length) in enumerate(SWEEP):
        y = -8.75 - (thick - 1) * .4 - (.15 if i % 2 else 0)
        chain(g, f"sweep_{i}", (2.7, y, z), [(thick, length, 2, (0, 0, 87)), (1, 3 - i % 2, 2, (0, 0, 12)), (1, 1, 1, (0, 0, 4))],
              seed=3310 + i * 7, ring=1, overlap=.45)
    # Behind them the crown is combed straight back.
    for i, (x, w) in enumerate(((-2.4, 3), (.6, 3), (3.0, 2))):
        plate(g, f"crown_{i}", (x, -8.3 - (i % 2) * .12, 2.2), (w, 1, 5), rotation=(-4, 0, x * 2), seed=3330 + i, sheen=2)
    # The narrow side beyond the part, combed down toward the left ear.
    plate(g, "part_left", (3.5, -8.25, -1.6), (2, 1, 5), rotation=(0, 0, 16), seed=3350, sheen=2)
    side = clump(g, "side_left", (4.4, -7.9, .6), (1, 3, 6), seed=3351, ring=None)
    combed_face(side.left, 3352, 2, across_y=True)
    # A neat, tapered nape.
    for i, (x, rz) in enumerate(((-2.4, 6), (0, 0), (2.4, -6))):
        taper(g, f"nape_{i}", (x, -7.6, 4.4), (4, 0, rz), ((3, 4, 1), (1, 1, 1)), seed=3360 + i * 3, ring=1)
