"""Mason's Shoulder-Pad Smock: a yoked smock with a leather pad for carrying stone, a mason's mark and a chisel roll."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import arm_blk, blk, embroider, flecks
from paint import grid

META = {
    "name": "Mason's Shoulder-Pad Smock",
    "gender": "male",
    "description": "A stone-dusted smock with a smocked yoke, a leather pad on the shoulder, his mason's mark on the chest and a chisel roll.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}

MARK = ["a.a",
        ".a.",
        ".a."]


def build(g):
    b = body(g, "S", "weave", 3801, base=3)
    neckline(b.front, "keyhole", "S", base=3)
    for face in b.sides:
        embroider(face, 2, "zig", "S1", "S1")                 # smocked yoke
        flecks(face, "S1", 3802, .05, rows=range(5, 12))
    grid(b.front, 4, 5, MARK, {"a": "S0"})
    sleeves(g, "S", "weave", 3803, base=3, rows=(0, 10), cuff="S1")
    pad = arm_blk(g, "stone_pad", "left", -2.6, (5, 2, 6), "L", 2, "leather", 3804, inflate=.12)
    for face in pad.sides:
        face.hline(0, face.w - 1, 0, "L3")
        face.set(face.w // 2, 1, "L0")
    belt(g, "belt", 9.6, height=1)
    roll = blk(g, "chisel_roll", (-2.8, 9.4, -2.75), (3, 2, 1), "L", 2, "leather", 3805)
    roll.front.hline(0, 2, 0, "L3")
    for i, x in enumerate((-3.4, -2.4)):
        ch = blk(g, f"chisel_{i}", (x, 7.6, -2.75), (1, 2, 1), "M", 2 + i, "smooth", 3806 + i, edge=False)
        ch.front.set(0, 1, "L3")
    for face in flaps(g, "hem", 4, "S", "weave", 3808, base=3, top=10.6):
        flecks(face, "S1", 3809, .12)
        face.hline(0, 8, 3, "S2")
