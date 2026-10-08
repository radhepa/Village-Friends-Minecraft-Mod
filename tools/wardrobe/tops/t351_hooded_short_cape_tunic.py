"""Hooded Short Cape over Tunic: a plain belted tunic under an elbow-length wool cape with its hood thrown back,
blanket-stitched round the edge and closed at the throat by a wooden toggle."""
from kit import SIDES, belt, body, flaps, neckline, sleeves
from kit_male import blk, hood_down, shoulder_cape
from paint import k

META = {
    "name": "Hooded Short Cape over Tunic",
    "gender": "male",
    "description": "A plain belted tunic under a short wool cape reaching the elbows, its hood thrown back, the edge blanket-stitched in a bright yarn and a wooden toggle at the throat.",
    "tags": ["casual", "simple", "rugged"],
    "covers_waist": True,
}


def build(g):
    tunic = body(g, "S", "weave", 40300, base=3)
    neckline(tunic.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 40301, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "S2")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S1")
    belt(g, "belt", 9.4, height=1)
    for face in flaps(g, "tunic_hem", 3, "S", "weave", 40302, base=3, top=11.2):
        face.hline(0, 8, 2, "S1")
    # The cape: from the neck to the elbows, open down the front.
    cape = shoulder_cape(g, "short_cape", "P", "weave", 40303, length=5, width=16, depth=7, y=-.8)
    cf = cape.front
    cf.vline(7, 1, 4, "P0"), cf.vline(8, 1, 4, "P3")
    for face in cape.sides:
        face.hline(0, face.w - 1, 0, "P3")
        face.hline(0, face.w - 1, face.h - 1, "A2")                        # blanket-stitched edge
        for x in range(1, face.w, 3):
            face.set(x, face.h - 2, "A1")
    for x in (2, 5, 10, 13):
        cape.back.vline(x, 2, 3, "P1")                                    # soft folds over the shoulders
    cape.bottom.fill("P0")
    # Toggle and loop at the throat.
    toggle = blk(g, "throat_toggle", (0, .3, -3.05), (2, 1, 1), "L", 3, "smooth", 40304, edge=False)
    toggle.front.set(1, 0, "L1")
    loop = blk(g, "throat_loop", (.9, .1, -3.0), (1, 1, 1), "L", 1, "plain", 40305, edge=False)
    # Hood lying back over the cape.
    hood = hood_down(g, "P", "weave", 40306, width=7, y=-.6, z=3.25, tilt=18, lining="S3")
    for face in hood.sides:
        face.hline(0, face.w - 1, face.h - 1, k("A", 2))
