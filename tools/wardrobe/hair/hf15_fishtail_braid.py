"""Fishtail Braid: a flat herringbone braid from the crown to the waist, curtain bangs and loose wavy wisps."""
from anime import ring_shell
from anime_female import fall, finish, link, strand, world, SIDES
from paint import k, scalp


META = {"name": "Fishtail Braid", "gender": "female",
        "description": "A flat herringbone fishtail braid down the back, with curtain bangs and loose wisps."}


def herringbone(face, base=2, flip=False):
    """Fine V-shaped strands crossing at the middle of the braid."""
    mid = (face.w - 1) / 2
    for y in range(face.h):
        for x in range(face.w):
            v = int(abs(x - mid) + y + (1 if flip else 0)) % 2
            s = base + (1 if v == 0 else 0)
            if face.w > 1 and x in (0, face.w - 1) and y == face.h - 1:
                s = base - 1
            face.set(x, y, k("H", s))


def build(g):
    scalp(g, 6501, side_rows=6, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 6502, side_rows=5, back_rows=6)
    hat.top.vline(3, 0, 7, "H1")
    for side, sign in SIDES:
        strand(g, f"{side}_curtain", (.3 * sign, -8.75, -4.35), (-6, 0, 56 * -sign), ((2, 4), (1, 1)), 1, 6510 + (sign > 0), ring=None)
        strand(g, f"{side}_wisp", (4.35 * sign, -7.6, -3.5), (0, 0, -4 * sign), ((1, 4), (1, 3, .5 * sign), (1, 2, -.3 * sign)), 1,
               6515 + (sign > 0), texture="wave")
        strand(g, f"{side}_side", (4.45 * sign, -7.8, 1.2), (0, 0, -2 * sign), ((1, 5),), 4, 6518 + (sign > 0))
    fall(g, "gather", [(-2.3, -7.6, 4.45, ((3, 4),), 0, 18), (2.3, -7.6, 4.45, ((3, 4),), 0, -18)], 6520)
    pivot = (0, -5.4, 4.75)
    rot = (-3, 0, 0)
    for i in range(10):
        w = 3 if i < 7 else 2
        lobe = link(g, f"fishtail_{i}", pivot, world(pivot, rot, (0, i * 1.5, 0)), rot, (w, 2, 1), "sway", dx=.25 if i % 2 else -.25)
        for f in lobe.sides:
            herringbone(f, 2, bool(i % 2))
        lobe.top.fill(k("H", 3)), lobe.bottom.fill(k("H", 1))
    finish(g, "fishtail", pivot, world(pivot, rot, (0, 9 * 1.5 + 2, 0)), rot, 2, 1, "A", ((2, 2), (1, 2)), seed=6540)
