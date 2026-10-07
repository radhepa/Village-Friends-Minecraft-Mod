"""Water Carrier's Yoke: a laced shirt under a carved wooden yoke across the shoulders, rope drops, and a water skin."""
from kit import body, neckline, sleeves
from kit_male import blk
from paint import solid

META = {
    "name": "Water Carrier's Yoke",
    "gender": "male",
    "description": "A laced work shirt under a carved wooden shoulder yoke with rope drops and iron hooks, and a stoppered water skin.",
    "tags": ["casual", "work"],
    "tucked": True,
}


def build(g):
    b = body(g, "S", "weave", 4901, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 4902, base=3, rows=(0, 10), cuff="S2")
    for face in b.sides:
        face.vline(0, 1, 8, "S2")                                      # side seams
    # The yoke rests across the shoulders behind the neck.
    yoke = g.piece("shoulder_yoke", "TORSO", (-9, 0, -1), (18, 1, 2), pivot=(0, -.4, 3.0))
    solid(yoke, "L", "plain", 4903, 3, edge=False)
    for face in (yoke.front, yoke.back, yoke.top):
        face.set(0, 0, "L1"), face.set(face.w - 1, 0, "L1")
        face.set(8, 0, "L4"), face.set(9, 0, "L4")
    pad = blk(g, "yoke_pad", (0, .3, 2.4), (6, 1, 2), "L", 1, "leather", 4904)
    pad.top.fill("L2")
    for i, x in enumerate((-8.4, 8.4)):
        rope = blk(g, f"rope_drop_{i}", (x, 1.0, 3.0), (1, 4, 1), "S", 2, "plain", 4905 + i, motion="sway")
        for y in range(4):
            rope.strip.hline(0, rope.strip.w - 1, y, "S3" if y % 2 else "S1")
        blk(g, f"rope_hook_{i}", (x, 5.0, 3.0), (1, 1, 1), "M", 2, "smooth", 4907 + i, edge=False)
    skin = blk(g, "water_skin", (2.9, 7.8, -2.6), (2, 3, 2), "L", 2, "leather", 4909)
    skin.front.set(0, 0, "L3"), skin.bottom.fill("L1")
    blk(g, "water_skin_stopper", (2.9, 7.0, -2.6), (1, 1, 1), "L", 4, "plain", 4910, edge=False)
