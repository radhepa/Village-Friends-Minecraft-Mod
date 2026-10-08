"""Gusseted Peasant Shirt: a roomy untucked shirt cut from squares, gathered at the neck on a tie, with shoulder straps, diamond gussets and wristbands."""
from kit import SIDES, body, flaps, sleeves
from kit_m10 import tie
from paint import dark_seams

META = {
    "name": "Gusseted Peasant Shirt",
    "gender": "male",
    "description": "A roomy linen shirt cut from plain squares and worn loose: the neck gathered on a tied cord, contrast shoulder straps, diamond gussets let into the armpits and full sleeves gathered into wristbands.",
    "tags": ["casual", "simple", "relaxed"],
    "covers_waist": True,
}

GUSSET = {(0, 2): "S2", (0, 3): "S4", (0, 4): "S2", (1, 3): "S2"}


def build(g):
    b = body(g, "S", "weave", 40620, base=3)
    f, bk = b.front, b.back
    # Neck gathered on a drawcord.
    f.clear(3, 0), f.clear(4, 0), f.clear(4, 1)
    for face in (f, bk):
        for x in range(face.w):
            if face.get(x, 0):
                face.set(x, 0, "S2" if x % 2 else "S4")
        for x in range(1, 7, 2):
            face.set(x, 1, "S2")                                          # gathers falling from the neckband
    f.vline(4, 2, 3, "S1")
    # Contrast shoulder straps over the top of the shoulders.
    for face in (f, bk):
        face.hline(0, 1, 0, "P2"), face.hline(6, 7, 0, "P2")
    for x in range(b.top.w):
        for y in range(b.top.h):
            if x < 2 or x > 5:
                b.top.set(x, y, "P3")
    # Diamond gussets where the sleeves meet the body.
    for (x, y), key in GUSSET.items():
        f.set(x, y, key), f.set(7 - x, y, key)
    dark_seams(b, faces=("right", "left"))
    # Full sleeves gathered into narrow wristbands.
    sleeves(g, "S", "weave", 40621, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.top.fill("P3")
        arm.strip.hline(0, arm.strip.w - 1, 0, "P2")                      # the strap's end on the sleeve head
        inner = arm.left if side == "right" else arm.right
        inner.set(0 if side == "right" else 3, 1, "S2"), inner.set(0 if side == "right" else 3, 2, "S4")
        for x in range(arm.strip.w):
            arm.strip.set(x, 8, "S2" if x % 2 else "S4")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P2"), arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
    for j, x in enumerate((-.4, .4)):
        tie(g, f"neck_cord_{j}", "TORSO", (x, 1.4, -2.2), "S", 2, 2, 40622 + j, rotation=(0, 0, 4 - 8 * j))
    for face in flaps(g, "shirt_hem", 4, "S", "weave", 40624, base=3, top=11.2):
        face.vline(0, 1, 3, "S2"), face.vline(8, 1, 3, "S2")
        face.hline(1, 7, 3, "S2")
