"""Receding Swept-Back: an older man's cut, the hairline receded at both temples into an M, the
thinning top combed straight back, short neat sides and nape."""
from anime_male import SIDES, clump, combed_face, fade, plate, taper
from paint import hair_face, k

META = {"name": "Receding Swept-Back", "gender": "male",
        "description": "Receded at the temples, the thinning top combed back over short neat sides."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 7301, 2)
    # Receded temples (the front corners of the crown) and a thin patch the scalp shows through.
    for x, y in ((0, 7), (1, 7), (0, 6), (6, 7), (7, 7), (7, 6), (0, 5), (7, 5)):
        head.top.set(x, y, None)
    for x, y in ((3, 4), (4, 3), (2, 2), (5, 5), (3, 6), (4, 6)):
        head.top.set(x, y, "X1")
    for face, rows in ((head.right, 5), (head.left, 5), (head.back, 7)):
        hair_face(face, 7302 + face.x0, 1, rows=range(rows))
        fade(face, 7303 + face.x0, rows - 2, rows - 1, base=1, start=.9, end=.45)
    for y in range(3):   # the temples recede on the sides too
        head.right.set(7, y, None), head.right.set(6, y, None)
        head.left.set(0, y, None), head.left.set(1, y, None)
    head.front.hline(2, 5, 0, "H1")
    for y in range(8):
        for x in range(2, 6):
            hat.top.set(x, y, k("H", 3 - (1 if x % 2 else 0)))
    for x in (1, 6):
        for y in range(6):
            hat.top.set(x, y, "H2")
    sub = type(hat.back)(hat.layer, hat.back.x0, hat.back.y0, 8, 4, "back")
    combed_face(sub, 7304, 2)
    hat.front.hline(2, 5, 0, "H2")
    # Thin combed-back sections from the receded peak.
    for i, (x, z) in enumerate(((-1.1, -1.0), (1.1, -1.2), (0, .6))):
        plate(g, f"combed_{i}", (x, -8.1 - (i % 2) * .1, z), (2, 1, 6), rotation=(-4, 0, -x * 2), seed=7310 + i, sheen=2)
    for side, sign in SIDES:
        side_box = clump(g, f"{side}_side", (4.4 * sign, -7.6, 1.2), (1, 3, 5), seed=7320 + (sign > 0))
        combed_face(side_box.right if sign < 0 else side_box.left, 7322 + (sign > 0), 2, across_y=True)
    for i, (x, rz) in enumerate(((-2.4, 6), (0, 0), (2.4, -6))):
        taper(g, f"nape_{i}", (x, -7.0, 4.4), (4, 0, rz), ((3, 3, 1), (1, 1, 1)), seed=7330 + i * 3, ring=1)
