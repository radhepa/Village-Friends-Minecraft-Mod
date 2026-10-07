"""Hermit's Sackcloth: a coarse sackcloth robe with tattered sleeves, a knotted rope girdle and a whittled wooden cross."""
from kit import belt, body, sleeves
from kit_male import blk, flecks

META = {
    "name": "Hermit's Sackcloth",
    "gender": "male",
    "description": "A forest hermit's coarse sackcloth robe with tattered sleeves, a knotted rope girdle and a whittled wooden cross on a thong.",
    "tags": ["holy", "simple"],
    "locked_to": "b95_hermits_rag_wrapped_feet",
    "covers_waist": True,
}


def sacking(face, seed=0):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, "S1" if (x + y) % 2 == 0 and (x // 2 + y // 2) % 2 else "S2")
    flecks(face, "L2", 9500 + seed, .025)


def build(g):
    b = body(g, "S", "tweed", 9501)
    for face in b.sides:
        sacking(face)
    b.front.clear(3, 0), b.front.clear(4, 0)
    sleeves(g, "S", "tweed", 9502, rows=(0, 9))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        sacking(arm.strip, 1)
        for x in range(arm.strip.w):
            if x % 3 == 0:
                arm.strip.set(x, 9, None)                               # tattered edge
            if x % 3 == 1:
                arm.strip.set(x, 10, "S1")
    rope = belt(g, "rope_girdle", 9.6, role="L", base=3, height=1, buckle=None)
    for face in rope.sides:
        for x in range(face.w):
            face.set(x, 0, "L4" if x % 2 else "L2")
    end = blk(g, "rope_end", (-1.4, 10.2, -2.85), (1, 5, 1), "L", 3, "plain", 9503, motion="sway")
    end.strip.hline(0, end.strip.w - 1, 2, "L1")
    blk(g, "cross_upright", (0, 3.4, -2.6), (1, 3, 1), "L", 3, "plain", 9504, edge=False)
    blk(g, "cross_arm", (0, 4.0, -2.65), (3, 1, 1), "L", 3, "plain", 9505, edge=False)
