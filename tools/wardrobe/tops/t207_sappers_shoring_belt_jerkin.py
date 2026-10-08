"""Sapper's Shoring-Belt Jerkin: a laced leather jerkin, a heavy tool belt with pick and maul, and shoring timbers on the back."""
from kit import SIDES, body, roll, sleeves
from kit_male import flecks, lacing
from kit_m04 import hanging
from paint import fabric, solid

META = {
    "name": "Sapper's Shoring-Belt Jerkin",
    "gender": "male",
    "description": "A laced leather jerkin over an earth-stained shirt with rolled sleeves, a broad ringed belt carrying "
                   "a pick and a wooden maul, and a bundle of shoring timbers lashed across the back.",
    "tags": ["rugged", "work", "martial"],
    "covers_waist": True,
}

S = 34440


def build(g):
    body(g, "S", "weave", S)
    jacket = g.part("jacket")
    for face in jacket.sides:
        fabric(face, "L", "leather", S + 1, 2)
        face.hline(0, face.w - 1, 11, "L1")
        flecks(face, "L0", S + 2, .06, rows=range(6, 12))
    fabric(jacket.top, "L", "leather", S + 1, 3)
    f = jacket.front
    f.rect(3, 0, 2, 3, None)                                               # open laced neck
    lacing(f, 3, 3, 9, "S3", "L0")
    f.vline(2, 0, 11, "L3"), f.vline(5, 0, 11, "L1")
    jacket.top.rect(2, 2, 4, 2, None)
    sleeves(g, "S", "weave", S + 3, rows=(0, 5))
    roll(g, "S", 2.4, base=3)
    for side in SIDES:
        flecks(g.part(f"{side}_arm").strip, "L1", S + 4, .08, rows=range(0, 6))
    belt = g.piece("shoring_belt", "TORSO", (-4.6, 9.2, -2.6), (9, 2, 5), inflate=.08)
    solid(belt, "L", "leather", S + 5, 1, edge=False)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
        for x in range(1, face.w, 3):
            face.set(x, 1, "M3")                                           # iron rings
    belt.front.hline(3, 5, 0, "M3"), belt.front.set(4, 1, "L0")
    # Pick: haft down the right hip, iron head across its top.
    haft = hanging(g, "pick_haft", -2.5, 10.4, (1, 6, 1), "L", 3, "plain", S + 6, top=10.4, dz=-.1)
    haft.front.vline(0, 0, 5, "L3"), haft.front.set(0, 5, "L1")
    head = hanging(g, "pick_head", -2.5, 9.6, (3, 1, 1), "M", 2, "smooth", S + 7, top=10.4, dz=-.1)
    head.front.set(0, 0, "M1"), head.front.set(2, 0, "M4")
    # Maul at the left hip.
    handle = hanging(g, "maul_handle", 2.8, 10.6, (1, 3, 1), "L", 3, "plain", S + 8, top=10.4, dz=-.3)
    handle.front.set(0, 2, "L1")
    maul = hanging(g, "maul_head", 2.8, 13.6, (2, 2, 3), "L", 2, "plain", S + 9, top=10.4, dz=.4)
    for face in maul.sides:
        face.vline(0, 0, 1, "L3"), face.set(face.w - 1, 1, "L1")
    maul.front.fill("L1"), maul.front.set(0, 0, "L3")
    # Shoring timbers lashed upright across the back.
    for i, (x, h, y) in enumerate(((-2.2, 10, 1.0), (0.0, 11, 0.4), (2.2, 10, 1.2))):
        post = g.piece(f"timber_{i}", "TORSO", (x - 1, y, 2.4), (2, h, 2))
        solid(post, "L", "plain", S + 10 + i, 3)
        for face in post.sides:
            face.vline(0, 0, h - 1, "L2")
            face.set(1, 2 + i, "L1")                                       # grain knot
            for yy in (2, 7):
                face.hline(0, 1, yy - int(y), "S2")                        # rope lashings
        post.top.fill("L4")
