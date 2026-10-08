"""Sailor's Striped Slop Frock: a loose banded linen frock with a wide boat neck, three-quarter sleeves rolled at the
forearm and a neckerchief knotted at the throat."""
from kit import body, flaps, roll, sleeves
from kit_male import blk, stripes
from paint import solid

META = {
    "name": "Sailor's Striped Slop Frock",
    "gender": "male",
    "description": "A loose linen slop frock in broad bands, a wide boat neck, three-quarter sleeves rolled at the "
                   "forearm and a neckerchief knotted at the throat.",
    "tags": ["casual", "sea", "relaxed"],
    "covers_waist": True,
}

BANDS = ["S3", "S3", "P2", "P2"]


def build(g):
    b = body(g, "S", "weave", 33080, base=3)
    for face in b.sides:
        stripes(face, BANDS, rows=range(2, 12), offset=0)
        face.hline(0, face.w - 1, 11, "P1")
    b.right.vline(3, 2, 11, "S2"), b.left.vline(0, 2, 11, "S2")
    sleeves(g, "S", "weave", 33081, base=3, rows=(0, 7))
    for side in ("right", "left"):
        stripes(g.part(f"{side}_arm").strip, BANDS, rows=range(2, 8), offset=0)
    roll(g, "S", 5.0, base=3)
    # Neckerchief: a cloth ring round the neck, knotted in front with two loose ends.
    ring = g.piece("neckerchief", "TORSO", (-3.5, -.8, -2.5), (7, 2, 5), inflate=.08)
    solid(ring, "A", "plain", 33082, 2, edge=False)
    for face in ring.sides:
        face.hline(0, face.w - 1, 1, "A1")
        face.set(1, 1, "A2"), face.set(face.w - 2, 0, "A3")
    knot = blk(g, "neckerchief_knot", (0, 1.1, -2.75), (2, 1, 1), "A", 3, "plain", 33083, edge=False)
    knot.front.set(1, 0, "A1")
    for i, (x, rz) in enumerate(((-.6, 10), (.7, -14))):
        end = g.piece(f"neckerchief_end_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 1.8, -2.75),
                      rotation=(0, 0, rz), motion="sway")
        solid(end, "A", "plain", 33084 + i, 2)
        end.front.set(0, 2, "A1")
    for face in flaps(g, "frock_hem", 3, "S", "weave", 33086, base=3, top=11.0):
        stripes(face, BANDS, rows=range(0, 2), offset=1)
        face.hline(0, 8, 2, "S1")
