"""Dairymaid's Churn Apron Bodice: a long pinned bib apron for the churn over a bodice and banded elbow
sleeves, a pair of ribbed butter hands standing in its pocket."""
from kit_female import OVER_FRONT, bodice, chemise, girdle, over_panel
from paint import fabric, k, solid

META = {
    "name": "Dairymaid's Churn Apron Bodice",
    "gender": "female",
    "description": "A long white churn apron pinned high on the bodice, banded elbow sleeves over bare forearms and two ribbed butter paddles standing in the apron pocket.",
    "tags": ["work", "apron", "simple"],
    "covers_waist": True,
}

HINGE = (0, 9.0, OVER_FRONT)


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51200, neckline="round", sleeve_rows=(0, 6))
    for arm in arms:
        arm.strip.hline(0, 15, 5, "A2"), arm.strip.hline(0, 15, 6, "S2")   # a band gathering the sleeve
    b = bodice(g, "P", "weave", 51201, rows=(1, 9), neckline="square", edge="P3")
    j = g.part("jacket")
    # The bib, pinned at its two top corners, and its broad strings round the back.
    fabric(j.front, "S", "weave", 51202, 4, 1, 2, 6, 10)
    j.front.vline(1, 2, 11, "S3"), j.front.vline(6, 2, 11, "S3")
    j.front.set(1, 2, "M4"), j.front.set(6, 2, "M4")
    for y in range(4, 11, 3):
        j.front.hline(2, 5, y, "S3")                                    # pressed creases across the bib
    b.back.hline(0, 7, 8, "S3"), b.back.hline(0, 7, 9, "S4")
    for face in (b.right, b.left):
        face.hline(0, 3, 8, "S3"), face.hline(0, 3, 9, "S4")
    girdle(g, "apron_band", 8.4, role="S", base=4, height=1, buckle=None, texture="weave", wide=True)
    apron = over_panel(g, "apron", 11, "S", "weave", 51203, base=4, width=9, top=9.0)
    apron.vline(0, 0, 10, "S3"), apron.vline(8, 0, 10, "S3"), apron.hline(0, 8, 10, "S3")
    apron.vline(3, 2, 9, "S3"), apron.vline(6, 2, 9, "S3")              # long folds for the churn
    # The pocket and the two butter hands standing in it, grips up.
    for x in range(1, 5):
        apron.set(x, 3, "S2")
    apron.vline(1, 3, 6, "S3"), apron.vline(4, 3, 6, "S3"), apron.hline(1, 4, 6, "S3")
    for i, (x, tilt) in enumerate(((-2.8, -6), (-.6, 6))):
        blade = g.piece(f"butter_hand_{i}", "TORSO", (x - 1, 1.0, -1.05), (2, 3, 1), pivot=HINGE, rotation=(0, 0, tilt),
                        motion="flap_front")
        solid(blade, "L", "smooth", 51204 + i, 3, edge=False)
        for f in (blade.front, blade.back):
            f.vline(0, 0, 2, "L2"), f.set(1, 1, "L2")                  # the ribbed paddle face
            f.hline(0, 1, 2, "L4")
        stem = g.piece(f"butter_hand_grip_{i}", "TORSO", (x - .5, -1.0, -1.05), (1, 2, 1), pivot=HINGE,
                       rotation=(0, 0, tilt), motion="flap_front")
        solid(stem, "L", "smooth", 51206 + i, 2, edge=False)
        stem.front.set(0, 0, k("L", 3))
