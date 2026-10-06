"""Buzz & Fringe: a close clip faded at the sides and nape, the short crown combed forward into a
straight-cut fringe of small points."""
from anime_male import clipped, clipped_scalp, combed_face, plate, taper

META = {"name": "Buzz & Fringe", "gender": "male",
        "description": "A close clip faded at the sides, the short crown combed forward into a neat fringe of small points."}


def build(g):
    clipped_scalp(g, 3101, base=1, side_rows=6, back_rows=7, fade_rows=3, sideburn=1)
    hat = g.part("hat")
    combed_face(hat.top, 3102, 2)
    for face in (hat.right, hat.left, hat.back):
        clipped(face, 3103 + face.x0, 1, rows=[0])
    hat.front.hline(0, 7, 0, "H2")
    # The short crown, combed forward in small flat plates.
    for i, (x, z, ry) in enumerate(((-2.2, -2.3, 6), (.4, -2.6, -4), (2.6, -2.1, -10), (-1.5, .7, 10), (1.5, .9, -6), (0, 3.0, 0))):
        plate(g, f"crown_{i}", (x, -8.3, z), (3, 1, 3), rotation=(-4, ry, 0), seed=3110 + i, sheen=1)
    # A straight-cut fringe of short points, alternately a texel longer.
    for i, x in enumerate((-3.3, -1.65, 0, 1.65, 3.3)):
        taper(g, f"fringe_{i}", (x, -8.5, -4.35), (-8, 0, 0), ((2, 2 - i % 2, 1), (1, 1, 1)), seed=3120 + i * 3, ring=0)
