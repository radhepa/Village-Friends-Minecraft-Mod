"""Cowherd's Horn-Slung Tunic: a split-front wool tunic with patched elbows, a tablet-woven belt with a little cowbell, and a big curved cow horn slung on a cord across the chest."""
from kit import body, flaps, neckline, sleeves
from kit_male import blk, embroider
from kit_m01 import patch
from paint import k, line, solid

META = {
    "name": "Cowherd's Horn-Slung Tunic",
    "gender": "male",
    "description": "A split-front wool tunic with patched elbows and a tablet-woven belt hung with a little cowbell, a big curved cow horn with a brass mouthpiece slung across the chest on a cord.",
    "tags": ["work", "casual", "rugged"],
    "covers_waist": True,
}

TOP = 10.8


def build(g):
    b = body(g, "P", "weave", 31550)
    neckline(b.front, "round", "P")
    for face in (b.right, b.left):
        face.vline(1, 2, 11, "P1")
    sleeves(g, "P", "weave", 31551, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        patch(arm.back, 0, 3, 4, 3, "S", 3)                   # patched elbows
        for face in (arm.right, arm.left):
            face.vline(2, 1, 9, "P1")
    # The horn's cord: from the left shoulder across the chest to the right hip, and down the back.
    jacket = g.part("jacket")
    line(jacket.front, 7, 0, 1, 7, "L2"), line(jacket.back, 0, 0, 6, 8, "L2")
    jacket.top.vline(6, 0, 3, "L2")
    # A tablet-woven belt: a band of little woven diamonds.
    belt = g.piece("woven_belt", "TORSO", (-4.6, 9.5, -2.6), (9, 1, 5), inflate=.06)
    solid(belt, "A", "weave", 31552, 2, edge=False)
    for face in belt.sides:
        for x in range(face.w):
            face.set(x, 0, "S3" if (x + face.x0) % 3 == 0 else "A2" if (x + face.x0) % 3 == 1 else "A1")
    blk(g, "belt_knot", (2.2, 9.4, -2.9), (1, 1, 1), "A", 3, "plain", 31553, edge=False)
    # The cow horn: a broad pale mouth bound in brass at the right hip, curving to a dark tip.
    mouth = blk(g, "horn_mouth", (-2.6, 6.6, -3.3), (2, 2, 2), "S", 3, "smooth", 31554, edge=False)
    for face in mouth.sides:
        face.vline(0, 0, 1, "M3")                                         # brass rim band
    mouth.right.fill("K1")                                                # the open bell of the horn
    mouth.right.set(0, 0, "M3"), mouth.right.set(1, 1, "M2")
    mid = blk(g, "horn_mid", (-.9, 6.9, -3.3), (2, 1, 1), "S", 3, "smooth", 31555, rotation=(0, 0, 10), edge=False)
    mid.front.set(0, 0, "S4"), mid.front.set(1, 0, "S2")
    bend = blk(g, "horn_bend", (.6, 6.4, -3.3), (1, 1, 1), "S", 2, "smooth", 31556, rotation=(0, 0, 30), edge=False)
    bend.front.fill("L2")
    tip = blk(g, "horn_tip", (1.2, 5.5, -3.3), (1, 1, 1), "K", 2, "smooth", 31557, rotation=(0, 0, 40), edge=False)
    tip.top.fill("M3")                                                    # brass mouthpiece
    tip.front.fill("K3")
    # The little cowbell at the left hip, swinging with the hem.
    bell = g.piece("cowbell", "TORSO", (1.8, 10.5 - TOP, -2), (2, 2, 2), pivot=(0, TOP, -2.95), motion="flap_front")
    solid(bell, "M", "smooth", 31558, 2, edge=False)
    bell.front.set(0, 0, "M4"), bell.front.hline(0, 1, 1, "M1")
    bell.bottom.fill("K0")
    clapper = g.piece("cowbell_clapper", "TORSO", (2.3, 12.5 - TOP, -1.5), (1, 1, 1), pivot=(0, TOP, -2.95),
                      motion="flap_front")
    solid(clapper, "M", "smooth", 31559, 1, edge=False)
    for face in flaps(g, "tunic_skirt", 4, "P", "weave", 31560, top=TOP, slit=True):
        face.hline(0, 8, 3, k("P", 1))
        for x in range(0, 9, 2):
            face.set(x, 2, "A2")
