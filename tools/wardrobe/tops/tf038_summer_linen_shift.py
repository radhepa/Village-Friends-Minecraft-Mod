"""Summer Linen Shift: a light cap-sleeved shift with a cross-stitched yoke, a string of beads and a braided wrist cord."""
from kit_female import chemise, trim
from paint import rnd

META = {
    "name": "Summer Linen Shift",
    "gender": "female",
    "description": "A light linen shift with cap sleeves and a cross-stitched yoke, a string of wooden beads and a braided cord.",
    "tags": ["casual", "relaxed", "simple"],
    "tucked": True,
}


def build(g):
    body, arms = chemise(g, "S", 4, "weave", 13801, neckline="boat", sleeve_rows=(0, 2), gather=False)
    trim(body.front, 2, "cross", "A2", "P2", x0=0, x1=7)
    trim(body.back, 0, "cross", "A2", "P2")
    for face in (body.right, body.left):
        trim(face, 0, "cross", "A2", "P2")
    for x, y in ((2, 1), (3, 2), (4, 2), (5, 1)):
        body.front.set(x, y, "L3" if x % 2 else "L2")                # wooden beads
    for arm in arms:
        arm.strip.hline(0, 15, 2, "A2")
        for x in range(16):
            if rnd(x, 3, 13802) < .5:
                arm.strip.set(x, 2, "S3")
    cord = g.part("left_arm")
    for x in range(16):
        cord.strip.set(x, 9, "A2" if x % 2 else "L2")                # a braided cord bracelet
