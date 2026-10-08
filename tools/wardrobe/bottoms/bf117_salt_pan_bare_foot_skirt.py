"""Salt-Pan Bare-Foot Skirt: a knee-length wrap skirt lapped across the front and tied at the left hip, its
hem dark with brine and crusted white with salt, worn barefoot on the clay of the pans."""
from kit_f03 import wet_hem
from kit_female import skirt
from paint import line, solid

META = {
    "name": "Salt-Pan Bare-Foot Skirt",
    "gender": "female",
    "description": "A knee-length wrap skirt tied at the left hip, its hem dark with brine and crusted white with salt, worn barefoot.",
    "tags": ["sea", "work", "relaxed", "skirt"],
}

SEED = 53225


def brine(face):
    wet_hem(face, 3, SEED, deep_rows=1)
    y = face.h - 4
    for x in range(face.w):
        face.set(x, y, ("S4", "S3", None)[(x + face.x0) % 3] or face.get(x, y))   # salt dried at the tide line


def build(g):
    s = skirt(g, "P", "weave", SEED, top=9.8, length=7, side_length=6, flare=5, folds=False)
    f = s.front.front
    line(f, 6, 1, 8, f.h - 1, "P3")                                  # the lapped front edge
    line(f, 5, 1, 7, f.h - 1, "P1")
    for x, y in ((2, 3), (3, 2), (8, 3)):
        f.vline(x, y, f.h - 2, "P1")
    b = s.back.back
    for x in (2, 5, 8):
        b.vline(x, 2, b.h - 2, "P1")
    s.paint(brine)
    # The tie at the left hip: a knot and two short ends riding the stride.
    knot = g.piece("waist_wrap_knot", "TORSO", (-1, 0, -.5), (2, 1, 1), pivot=(3.4, 10.0, -3.2))
    solid(knot, "P", "plain", SEED + 1, 3, edge=False)
    for i, (x, n) in enumerate(((3.0, 4), (4.0, 3))):
        end = g.piece(f"waist_wrap_tie_{i}", "TORSO", (-.5, .2, -.6), (1, n, 1), pivot=(x, 9.8, -2.95), motion="flap_front")
        solid(end, "P", "plain", SEED + 2 + i, 3)
        end.front.set(0, n - 1, "P1")
