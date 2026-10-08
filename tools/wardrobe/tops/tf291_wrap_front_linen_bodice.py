"""Wrap-Front Linen Bodice: a linen bodice wrapped right over left, its long ties wound twice round the waist and bowed behind."""
from kit import SIDES, body
from kit_female import girdle, hanging
from paint import fabric, line, solid, strip_fabric

META = {
    "name": "Wrap-Front Linen Bodice",
    "gender": "female",
    "description": "A light linen bodice wrapped across the chest, its long ties wound twice round the waist and bowed at the back, with slit three-quarter sleeves.",
    "tags": ["casual", "relaxed"],
}


def build(g):
    b = body(g, "P", "weave", 60200, base=3)
    f = b.front
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (5, 1), (4, 2), (5, 2), (5, 3)]:
        f.clear(x, y)                                                  # the deep wrapped V
    line(f, 1, 0, 3, 3, "P2")                                          # the under-wrap's edge
    line(f, 6, 0, 1, 8, "P4")                                          # the upper wrap's lit edge
    line(f, 7, 0, 2, 8, "P1")                                          # and the fold it casts
    f.set(6, 1, "P2"), f.set(6, 2, "P2"), f.set(6, 3, "P2")
    b.back.vline(3, 1, 11, "P2"), b.back.vline(4, 1, 11, "P4")
    for face in (b.right, b.left):
        face.vline(2, 1, 11, "P2")
    # Three-quarter sleeves, slit at the cuff.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60201 + (side == "left"), 3, 0, 7)
        fabric(arm.top, "P", "weave", 60203, 4)
        arm.strip.hline(0, 15, 7, "P2")
        outer = arm.right if side == "right" else arm.left
        outer.vline(1, 4, 7, "P1"), outer.set(2, 5, "P4")
    # The ties wound twice round the waist, crossing at the front.
    for i, y in enumerate((7.2, 8.3)):
        tie = girdle(g, f"wrap_tie_{i}", y, role="P", base=3, height=1, buckle=None, texture="plain")
        for face in tie.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if (x + i) % 3 else "P2")
        tie.front.set(4 - i, 0, "P4"), tie.front.set(5 - i, 0, "P1")
    # The bow at the small of the back.
    knot = g.piece("bow_knot", "TORSO", (-1, -.5, -.5), (2, 1, 1), pivot=(0, 8.0, 2.75))
    solid(knot, "P", "plain", 60204, 3, edge=False)
    for side, x, rot in (("right", -1.5, 28), ("left", 1.5, -28)):
        loop = g.piece(f"bow_loop_{side}", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(x, 7.9, 2.7), rotation=(0, 0, rot))
        solid(loop, "P", "plain", 60205, 3)
        loop.back.set(1 if side == "right" else 0, 1, "P1")
    for i, (x, length) in enumerate(((-.6, 5), (.6, 4))):
        tail = hanging(g, f"bow_tail_{i}", x, length, role="P", base=3, top=8.6, back=True, end="P2")
        tail.back.set(0, 1, "P2")
