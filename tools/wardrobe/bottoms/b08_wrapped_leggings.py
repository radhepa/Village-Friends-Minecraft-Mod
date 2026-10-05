"""Wrapped Leggings: loose linen trousers bound in cross-wrapped puttees, soft boots and a sash."""
from paint import cap, fabric, k, solid, strip_fabric

META = {
    "name": "Wrapped Leggings",
    "description": "Linen trousers bound from knee to ankle in leather wraps, soft turnshoes and a tied sash.",
    "tags": ["rugged", "sturdy", "simple"],
}


def wraps(face, y0, y1):
    """Overlapping diagonal bands: lit edge, body, shaded underlap."""
    for y in range(y0, y1 + 1):
        for x in range(face.w):
            d = (2 * y + x // 2) % 4
            face.set(x, y, "L3" if d == 0 else "L2" if d in (1, 2) else "L1")


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 181 if side == "right" else 182, 2, 0, 5)
        fabric(leg.top, "S", "weave", 18, 2)
        leg.strip.hline(0, leg.strip.w - 1, 5, "S1")
        leg.front.set(1 if side == "right" else 2, 2, "S1"), leg.front.set(1 if side == "right" else 2, 3, "S3")
        strip_fabric(leg, "L", "leather", 189, 1, 6, 10)
        wraps(pants.strip, 5, 9)
        for face in pants.sides:
            face.hline(0, face.w - 1, 5, "L3")
        # Soft turnshoes.
        strip_fabric(leg, "L", "leather", 183, 1, 11, 11)
        for face in pants.sides:
            fabric(face, "L", "leather", 184, 1, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.hline(0, 3, 10, "L2")
        leg.bottom.fill("K1"), pants.bottom.fill("K1")

    body = g.part("body")
    strip_fabric(body, "S", "weave", 185, 2, 9, 11)
    fabric(body.bottom, "S", "weave", 19, 1)
    sash = g.piece("waist_sash", "TORSO", (-4.6, 9.4, -2.6), (9, 2, 5), inflate=.05)
    solid(sash, "A", "plain", 186, 2)
    for face in sash.sides:
        face.hline(0, face.w - 1, 0, "A3")
    knot = g.piece("waist_sash_knot", "TORSO", (-1, 0, -1), (2, 2, 2), pivot=(3.9, 10.0, -1.4))
    solid(knot, "A", "plain", 187, 2)
    tail = g.piece("waist_sash_tail", "TORSO", (-.5, 0, -1), (1, 5, 2), pivot=(4.3, 11.0, -1.2), rotation=(0, 0, -7), motion="sway")
    solid(tail, "A", "plain", 188, 2)
    tail.strip.hline(0, tail.strip.w - 1, 4, "A1")
