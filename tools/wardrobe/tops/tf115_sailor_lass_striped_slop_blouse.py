"""Sailor Lass's Striped Slop Blouse: a loose boat-necked slop blouse in broad deck stripes, bloused over a
knotted sash with its tails at the hip, three-quarter sleeves and a dark neckerchief tied sailor-fashion."""
from kit_female import chemise, girdle, hanging
from paint import fabric, solid

META = {
    "name": "Sailor Lass's Striped Slop Blouse",
    "gender": "female",
    "description": "A loose boat-necked blouse in broad deck stripes, bloused over a knotted sash, with a dark neckerchief tied at the throat.",
    "tags": ["sea", "casual", "relaxed"],
}

SEED = 53150


def deck_stripes(face, y0=0, y1=None, offset=0):
    """Broad stripes, three rows of cloth to two of stripe, with a soft shade under each stripe."""
    y1 = face.h - 1 if y1 is None else y1
    for y in range(y0, y1 + 1):
        phase = (y + offset) % 5
        for x in range(face.w):
            if not face.get(x, y):
                continue
            if phase in (3, 4):
                face.set(x, y, "P2" if phase == 3 else "P1")
            elif phase == 0:
                face.set(x, y, "S2")


def build(g):
    body, arms = chemise(g, "S", 3, "weave", SEED, neckline="boat", sleeve_rows=(0, 8), gather=False)
    for face in body.sides:
        deck_stripes(face, 1, 11)
    for arm in arms:
        deck_stripes(arm.strip, 0, 7, offset=1)
        arm.strip.hline(0, 15, 8, "S2")                               # a plain hemmed edge
    # Bloused fullness on the jacket layer: the blouse hangs loose over the sash.
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "S", "weave", SEED + 1, 3, 0, 5, face.w, 3)
        deck_stripes(face, 5, 7, offset=4)
        for x in range(0, face.w, 2):
            face.set(x, 7, "S2")                                     # folds where it pouches over
    girdle(g, "sash", 8.0, role="A", base=2, height=2, buckle=None, texture="weave")
    knot = g.piece("sash_knot", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(-2.4, 8.0, -2.25))
    solid(knot, "A", "plain", SEED + 2, 2, edge=False)
    knot.front.set(0, 0, "A3"), knot.front.set(1, 1, "A1")
    for i, (x, n) in enumerate(((-2.9, 5), (-1.9, 4))):
        tail = hanging(g, f"sash_tail_{i}", x, n, role="A", base=2 - i, top=9.0)
        tail.front.set(0, n - 1, "A3")
    # A dark neckerchief: a ring round the throat, knotted low in front with two short ends.
    ring = g.piece("neckerchief", "TORSO", (-4.5, -.5, -2.5), (9, 1, 5), inflate=.06)
    solid(ring, "K", "plain", SEED + 3, 3, edge=False)
    point = g.piece("neckerchief_point", "TORSO", (-2, 0, 0), (4, 2, 1), pivot=(0, -.2, 2.3), rotation=(8, 0, 0))
    solid(point, "K", "plain", SEED + 4, 3)
    point.back.hline(1, 2, 1, "K1")
    front = g.piece("neckerchief_knot", "TORSO", (-1, 0, 0), (2, 1, 1), pivot=(0, 1.6, -2.75))
    solid(front, "K", "plain", SEED + 5, 4, edge=False)
    for i, rot in enumerate((14, -14)):
        end = g.piece(f"neckerchief_end_{i}", "TORSO", (-.5, 0, 0), (1, 2, 1), pivot=(-.5 + i, 2.5, -2.75), rotation=(0, 0, rot))
        solid(end, "K", "plain", SEED + 6, 3)
