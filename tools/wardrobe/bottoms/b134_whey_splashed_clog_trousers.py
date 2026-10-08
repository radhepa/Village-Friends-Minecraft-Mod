"""Whey-Splashed Clog Trousers: twill trousers drawn tight at the ankle and splashed pale with whey, over tall-soled dairy clogs with leather uppers and a brass clasp."""
from kit import SIDES, legs, waistband
from kit_male import flecks, leg_blk, toe_pieces
from paint import k, strip_fabric

META = {
    "name": "Whey-Splashed Clog Trousers",
    "gender": "male",
    "description": "Twill trousers drawn tight at the ankle and splashed pale with whey from the churn, over tall wooden-soled dairy clogs with leather uppers and a brass clasp.",
    "tags": ["work", "casual", "sturdy"],
}


def build(g):
    leg_boxes = legs(g, "P", "twill", 31715, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 31716)
    for i, (side, leg) in enumerate(zip(SIDES, leg_boxes)):
        pants = g.part(f"{side}_pants")
        for face in leg.sides:
            face.vline(1, 1, 7, "P1")
        flecks(leg.strip, "S4", 31717 + i, .1, rows=range(4, 9))            # whey splashes, thickest low down
        flecks(leg.strip, "S3", 31719 + i, .06, rows=range(1, 5))
        cuff = leg_blk(g, f"{side}_ankle_cuff", side, 8.0, (5, 1, 5), "P", 2, "twill", 31721 + i, inflate=.12)
        for face in cuff.sides:
            for x in range(face.w):
                face.set(x, 0, k("P", 3) if x % 2 else k("P", 1))          # drawn tight on a cord
        # Leather upper over the instep, the tall wooden sole below.
        strip_fabric(leg, "L", "smooth", 31723, 2, 9, 9)
        for face in leg.sides:
            face.hline(0, face.w - 1, 10, "L3"), face.hline(0, face.w - 1, 11, "L4")
        leg.bottom.fill("L1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L3"), face.hline(0, face.w - 1, 10, "L2")
            face.hline(0, face.w - 1, 11, "L4")                           # the pale wooden sole
        pants.front.set(1, 9, "M3")                                       # brass clasp
        pants.bottom.fill("L1")
        sole = leg_blk(g, f"{side}_clog_sole", side, 11.6, (5, 1, 6), "L", 3, "plain", 31724, inflate=.02)
        for face in sole.sides:
            face.hline(0, face.w - 1, 0, "L4")
        sole.bottom.fill("L1")
    for toe in toe_pieces(g, "clog_nose", (4, 2, 1), "L", base=3, texture="plain", seed=31724, y=9.9, z=-2.3):
        toe.front.set(0, 1, "L4"), toe.front.set(3, 1, "L4"), toe.front.hline(1, 2, 0, "L2")
