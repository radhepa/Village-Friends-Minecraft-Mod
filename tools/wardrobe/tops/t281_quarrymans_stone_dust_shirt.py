"""Quarryman's Stone-Dust Shirt: a tucked work shirt whitened with stone dust toward the cuffs and hem, a knotted neckerchief and leather wrist straps."""
from kit import SIDES, body, roll, sleeves
from kit_male import blk
from paint import k, solid

META = {
    "name": "Quarryman's Stone-Dust Shirt",
    "gender": "male",
    "description": "A heavy work shirt tucked into the waistband, whitened with stone dust that thickens toward the hem and the pushed-up sleeves, a neckerchief knotted at the throat and leather straps bound round the wrists.",
    "tags": ["work", "rugged", "simple"],
    "tucked": True,
}


def dusted(face, y0: int, y1: int, key: str = "S4"):
    """Settled dust in an ordered dither: sparse at row y0, every other texel by row y1."""
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        step = 4 if t < .34 else 3 if t < .67 else 2
        for x in range(face.w):
            if (x + face.x0 + y * (step // 2 + 1)) % step == 0:
                face.set(x, y, key)


def build(g):
    b = body(g, "P", "weave", 37420)
    f = b.front
    f.clear(3, 0), f.clear(4, 0), f.clear(4, 1), f.clear(4, 2)
    f.set(3, 1, "P0"), f.set(3, 2, "P0"), f.set(5, 0, "P3")              # an open slit placket
    for face in b.sides:
        dusted(face, 8, 11)
    sleeves(g, "P", "weave", 37421, rows=(0, 5))
    roll(g, "P", 2.6, base=3, accent="S4")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        dusted(arm.strip, 4, 5)
        arm.strip.hline(0, arm.strip.w - 1, 8, "L2"), arm.strip.hline(0, arm.strip.w - 1, 9, "L1")   # wrist straps
        arm.strip.set(1 if side == "right" else 9, 8, "M3")
    # The neckerchief: a triangle hanging down the back, a knot at the throat with two short ends.
    tri = g.piece("kerchief_back", "TORSO", (-2.5, 0, 0), (5, 2, 1), pivot=(0, -.1, 2.15))
    solid(tri, "A", "plain", 37422, 2, edge=False)
    tri.back.hline(0, 4, 1, "A1")
    tip = g.piece("kerchief_point", "TORSO", (-.5, 0, 0), (1, 2, 1), pivot=(0, 1.9, 2.15))
    solid(tip, "A", "plain", 37423, 1, edge=False)
    band = g.piece("kerchief_band", "TORSO", (-4.3, 0, -2.4), (9, 1, 5), pivot=(-.1, -.2, 0), inflate=.02)
    solid(band, "A", "plain", 37424, 2, edge=False)
    knot = blk(g, "kerchief_knot", (-1.2, .4, -2.6), (2, 1, 1), "A", 3, "plain", 37425, edge=False)
    knot.front.set(0, 0, "A4")
    for i, (x, rz) in enumerate(((-1.6, 18), (-.8, -14))):
        end = blk(g, f"kerchief_end_{i}", (x, 1.2, -2.6), (1, 2, 1), "A", 2, "plain", 37426 + i, rotation=(0, 0, rz),
                  edge=False)
        end.strip.hline(0, 3, 1, k("A", 1))
