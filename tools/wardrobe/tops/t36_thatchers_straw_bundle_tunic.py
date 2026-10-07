"""Thatcher's Straw-Bundle Tunic: a tunic with a leather shoulder yoke, a bound yealm of straw on the back and hazel spars."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk
from paint import fabric, strip_fabric

META = {
    "name": "Thatcher's Straw-Bundle Tunic",
    "gender": "male",
    "description": "A roofer's tunic with a leather shoulder yoke, a bound bundle of straw slung on the back and hazel spars at the belt.",
    "tags": ["work", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 3601)
    neckline(b.front, "v", "P")
    sleeves(g, "P", "weave", 3602, rows=(0, 9))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 8, "L2"), arm.strip.hline(0, arm.strip.w - 1, 9, "L1")
    # Leather yoke across the shoulders, where the bundles ride.
    jacket = g.part("jacket")
    strip_fabric(jacket, "L", "leather", 3603, 2, 0, 2)
    fabric(jacket.top, "L", "leather", 3603, 3)
    for face in jacket.sides:
        face.hline(0, face.w - 1, 2, "L1")
    jacket.front.clear(3, 0), jacket.front.clear(4, 0)
    # The yealm: a bound bundle of straw, cut ends up and down.
    yealm = g.piece("straw_yealm", "TORSO", (-2, 0, -1.5), (4, 10, 3), pivot=(.4, .4, 3.9), rotation=(4, 0, 24))
    for face in yealm.sides:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, ("S2", "S3", "S4")[(x + face.x0 + y // 5) % 3])
        face.hline(0, face.w - 1, 2, "L1"), face.hline(0, face.w - 1, 7, "L1")
    yealm.top.fill("S1"), yealm.bottom.fill("S1")
    yealm.top.set(1, 1, "S3"), yealm.bottom.set(2, 1, "S3")
    belt(g, "belt", 9.6)
    for i, (x, rz) in enumerate(((2.6, -16), (3.4, -30))):
        spar = blk(g, f"hazel_spar_{i}", (x, 7.6, -2.75), (1, 4, 1), "L", 3, "plain", 3604 + i, rotation=(0, 0, rz))
        spar.strip.hline(0, spar.strip.w - 1, 3, "L4")
    for face in flaps(g, "hem", 3, "P", "weave", 3606, top=11.0):
        face.hline(0, 8, 2, "P1")
