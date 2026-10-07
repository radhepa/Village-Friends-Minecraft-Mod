"""Side-Laced Kirtle: a weaver's close-fitting kirtle laced up both sides, with tablet-woven bands at neck and cuffs."""
from kit import body, sleeves
from kit_female import band, girdle, hanging, neck, side_lacing, trim
from paint import solid

META = {
    "name": "Side-Laced Kirtle",
    "gender": "female",
    "description": "A weaver's fitted kirtle, laced up both sides, with tablet-woven bands and a long woven belt.",
    "tags": ["casual", "tailored"],
}


def build(g):
    b = body(g, "P", "weave", 10401)
    neck(b.front, "round", "P", 2)
    trim(b.front, 1, "diamond", "A2", "S3", x0=0, x1=7)
    trim(b.back, 0, "diamond", "A2", "S3")
    for face in (b.right, b.left):
        trim(face, 0, "diamond", "A2", "S3")
    side_lacing(b, 3, 10, lace="S3", under="P0")
    for face in (b.front, b.back):
        face.vline(1, 4, 11, "P1"), face.vline(6, 4, 11, "P1")      # fitted seams
    sleeves(g, "P", "weave", 10402, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        band(arm, 9, "diamond", "A2", "S3")
    belt = girdle(g, "woven_belt", 7.6, role="A", base=2, height=1, buckle=None, texture="plain")
    for face in belt.sides:
        for x in range(1, face.w, 2):
            face.set(x, 0, "S3")
    knot = g.piece("belt_knot", "TORSO", (-1, -.5, -.5), (2, 2, 1), pivot=(-1.8, 8.2, -2.9))
    solid(knot, "A", "plain", 10403, 2)
    for i, (x, length) in enumerate(((-2.2, 9), (-1.3, 7))):
        tail = hanging(g, f"belt_tail_{i}", x, length, role="A", top=8.8, end="S3")
        for y in range(1, length - 1, 2):
            tail.front.set(0, y, "S3")
