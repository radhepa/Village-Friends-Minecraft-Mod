"""Embroidered Festival Vest: a short bolero vest with zigzag embroidery, a billowing shirt and a knotted sash."""
from kit import body, neckline, sleeves
from paint import solid

META = {
    "name": "Embroidered Festival Vest",
    "gender": "male",
    "description": "Feast-day best: a short embroidered vest over a full-sleeved shirt and a knotted sash.",
    "tags": ["casual", "fancy"],
    "tucked": True,
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 2601, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 2602, base=3, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            face.hline(0, face.w - 1, 9, "A2")
            face.set(1, 10, "M3") if face.name == "front" else None
    vest = body(g, "P", "velvet", 2603, layer="jacket", rows=(0, 7))
    vf = vest.front
    for y in range(8):
        vf.clear(3, y), vf.clear(4, y)
        # Zigzag embroidery along both front edges.
        vf.set(2, y, "A3" if y % 2 else "M3"), vf.set(5, y, "M3" if y % 2 else "A3")
    for face in vest.sides:
        for x in range(face.w):
            face.set(x, 7, "A2" if x % 2 else "M3")
    vest.back.vline(3, 1, 5, "A2"), vest.back.vline(4, 1, 5, "A2")
    sash = g.piece("sash", "TORSO", (-4.6, 8.6, -2.6), (9, 2, 5), inflate=.06)
    solid(sash, "A", "plain", 2604, 2)
    for face in sash.sides:
        face.hline(0, face.w - 1, 0, "A3")
    knot = g.piece("sash_knot", "TORSO", (-1, -1, -1), (2, 2, 2), pivot=(-3.6, 9.6, -2.0))
    solid(knot, "A", "plain", 2605, 2)
    tail = g.piece("sash_tail", "TORSO", (-.5, 0, -1), (1, 5, 2), pivot=(-4.3, 10.4, -1.8), rotation=(0, 0, 8), motion="sway")
    solid(tail, "A", "plain", 2606, 2)
    tail.strip.hline(0, tail.strip.w - 1, 4, "M3")
