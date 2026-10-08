"""Cockle Gatherer's Rake-Strap Bodice: a yoked wool bodice crossed by a broad leather strap that carries
a short toothed cockle rake on her back, and a drawstring sack of cockles at the hip."""
from kit_f03 import front_prop
from kit_female import bodice, chemise, lacing
from paint import fabric, line, solid

META = {
    "name": "Cockle Gatherer's Rake-Strap Bodice",
    "gender": "female",
    "description": "A yoked wool bodice crossed by a broad leather strap that carries a toothed cockle rake on her back, a sack of cockles at the hip.",
    "tags": ["sea", "work", "rugged"],
}

SEED = 53090
RAKE_PIVOT, RAKE_ROT = (0.2, 4.6, 3.3), (0, 0, -32)


def build(g):
    body, arms = chemise(g, "S", 3, "weave", SEED, neckline="round", sleeve_rows=(0, 6))
    for arm in arms:
        arm.strip.hline(0, 15, 5, "A2")                               # sleeves tied up with a cord
        for x in range(0, 16, 2):
            arm.strip.set(x, 6, "S2")
        arm.front.vline(1, 1, 4, "S2")
    b = bodice(g, "P", "weave", SEED + 1, rows=(1, 9), neckline="round", edge="P3")
    for face in (b.front, b.back):                                   # a pieced yoke across the shoulders
        fabric(face, "S", "tweed", SEED + 2, 2, 0, 1, face.w, 2)
        face.hline(0, face.w - 1, 3, "P3")
    b.front.clear(3, 0), b.front.clear(4, 0)
    lacing(b.front, 3, 4, 8, "tight", lace="L2", under=None, eyelet=None)
    # The broad rake strap: over the right shoulder, down to the left hip, front and back.
    for dx, key in ((0, "L2"), (1, "L1")):
        line(b.front, dx, 0, 6 + dx, 9, key)
        line(b.back, 7 - dx, 0, 1 - dx, 9, key)
    b.top.vline(0, 0, 3, "L2"), b.top.vline(1, 0, 3, "L1")
    b.front.set(4, 5, "M3")                                          # strap buckle
    # The cockle rake hangs down the back along the strap: handle up, toothed head at the left hip.
    handle = g.piece("rake_handle", "TORSO", (-.5, -4.5, 0), (1, 10, 1), pivot=RAKE_PIVOT, rotation=RAKE_ROT)
    solid(handle, "L", "smooth", SEED + 3, 3)
    handle.back.set(0, 0, "L4")
    head = g.piece("rake_head", "TORSO", (-2.5, 5.5, -.3), (5, 1, 1), pivot=RAKE_PIVOT, rotation=RAKE_ROT, inflate=.05)
    solid(head, "L", "smooth", SEED + 4, 2, edge=False)
    for f in head.sides:
        f.hline(0, f.w - 1, 0, "L3")
    for i, x in enumerate((-2.5, -.5, 1.5)):
        tooth = g.piece(f"rake_tooth_{i}", "TORSO", (x, 6.5, -.2), (1, 2, 1), pivot=RAKE_PIVOT, rotation=RAKE_ROT)
        solid(tooth, "M", "smooth", SEED + 5, 2, edge=False)
        tooth.back.set(0, 0, "M3"), tooth.back.set(0, 1, "M1")
    loop = g.piece("rake_loop", "TORSO", (-.5, -.5, -1.4), (1, 1, 2), pivot=(-1.6, 1.9, 3.3), inflate=.05)
    solid(loop, "L", "leather", SEED + 6, 1, edge=False)
    # A drawstring sack of cockles hanging at the left hip, riding the stride.
    sack = front_prop(g, "cockle_sack", 2.6, (3, 3, 2), y=.6, role="S", base=2, texture="tweed", seed=SEED + 7)
    for f in sack.sides:
        f.hline(0, f.w - 1, 0, "S1")
        f.set(1, 2, "S1")
    sack.top.fill("S3")
    sack.top.set(1, 0, "S4"), sack.top.set(0, 1, "M3"), sack.top.set(2, 1, "S4")    # cockles peeping out
    neck = front_prop(g, "cockle_sack_neck", 2.6, (1, 1, 1), y=-.4, role="A", base=2, seed=SEED + 8, edge=False)
    neck.front.fill("A3")
