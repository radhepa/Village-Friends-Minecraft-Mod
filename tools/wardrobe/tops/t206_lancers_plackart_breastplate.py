"""Lancer's Plackart Breastplate: a ridged steel breastplate with a pointed plackart, a bolted lance rest and a big left pauldron."""
from kit import SIDES, body, sleeves
from kit_male import arm_blk, mail
from kit_m04 import lames
from paint import fabric, k, solid

META = {
    "name": "Lancer's Plackart Breastplate",
    "gender": "male",
    "description": "A ridged steel breastplate with a pointed plackart riveted over the belly and a lance rest bolted to "
                   "the right breast, a broad guard-pauldron on the left shoulder and a smaller one on the right, couters "
                   "at the elbows and a fauld of lames.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}

S = 34400


def build(g):
    body(g, "S", "quilt", S)
    jacket = g.part("jacket")
    for face in jacket.sides:
        fabric(face, "M", "smooth", S + 1, 2)
        face.hline(0, face.w - 1, 0, "M4")
    fabric(jacket.top, "M", "smooth", S + 1, 3)
    jacket.front.rect(2, 0, 4, 1, None), jacket.top.rect(2, 2, 4, 2, None)
    f = jacket.front
    f.vline(3, 1, 5, "M4"), f.vline(4, 1, 5, "M1")                       # the medial ridge
    f.vline(0, 1, 11, "M1"), f.vline(7, 1, 11, "M1")
    for y, (x0, x1) in zip(range(5, 12), ((3, 4), (2, 5), (1, 6), (0, 7), (0, 7), (0, 7), (0, 7))):
        f.hline(x0, x1, y, "M3")                                           # the plackart, pointed upward
        f.set(x0, y, "M4"), f.set(x1, y, "M1")
    for x, y in ((3, 5), (1, 8), (6, 8)):
        f.set(x, y, "M4")                                                  # its rivets
    f.hline(0, 7, 11, "M0")
    bk = jacket.back
    bk.vline(3, 1, 9, "M3"), bk.vline(4, 1, 9, "M1")
    lames(bk, 9, 11, "M", 2, step=2)
    for face in (jacket.right, jacket.left):
        for y in (3, 8):
            face.hline(0, 3, y, "L1"), face.set(1, y, "M4")                # side straps and buckles
    sleeves(g, "M", "smooth", S + 2, rows=(0, 10))
    for side in SIDES:
        arm, sl = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        mail(arm.strip, rows=range(0, 11))
        for face in sl.sides:
            fabric(face, "M", "smooth", S + 3, 2, 0, 6, face.w, 4)        # vambraces
            face.hline(0, face.w - 1, 6, "M4"), face.hline(0, face.w - 1, 9, "M1")
    # Couters at the elbows.
    for i, side in enumerate(SIDES):
        cop = arm_blk(g, f"{side}_couter", side, 3.2, (5, 2, 5), "M", 2, "smooth", S + 4 + i, inflate=.16)
        for face in cop.sides:
            face.hline(0, face.w - 1, 0, "M4"), face.hline(0, face.w - 1, 1, "M1")
        (cop.right if side == "right" else cop.left).set(2, 0, "M3")
    # Pauldrons: a broad guard on the left, a cut-away one on the right to clear the lance.
    for side, size, tilt in (("right", (6, 2, 5), -10), ("left", (7, 3, 6), 16)):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        cx = -1.0 if side == "right" else 1.0
        w, h, d = size
        p = g.piece(f"{side}_pauldron", bone, (cx - w / 2, -2.6, -d / 2), size, pivot=(0, 0, 0), rotation=(0, 0, tilt),
                    inflate=.1)
        solid(p, "M", "smooth", S + 6 + (side == "left"), 2)
        fabric(p.top, "M", "smooth", S + 8, 3)
        for face in p.sides:
            lames(face, 0, h - 1, "M", 2, step=h if h > 1 else 2, rivet="M4", rivet_step=3)
            face.hline(0, face.w - 1, 0, "M4")
    guard = g.piece("left_haute_piece", "LEFT_ARM", (-1.8, -4.4, -2.5), (1, 2, 5), rotation=(0, 0, 16))
    solid(guard, "M", "smooth", S + 9, 3, edge=False)
    guard.top.fill("M4")
    # Lance rest: a bracket bolted to the right breast.
    plate = g.piece("lance_rest_plate", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(-2.4, 4.0, -2.35))
    solid(plate, "M", "smooth", S + 10, 2, edge=False)
    plate.front.set(0, 0, "M4"), plate.front.set(1, 1, "M4")
    arm_ = g.piece("lance_rest_arm", "TORSO", (-.5, 0, -2), (1, 1, 2), pivot=(-2.4, 4.6, -3.35))
    solid(arm_, "M", "smooth", S + 11, 3, edge=False)
    hook = g.piece("lance_rest_hook", "TORSO", (-.5, -1, -1), (1, 2, 1), pivot=(-2.4, 4.6, -5.35))
    solid(hook, "M", "smooth", S + 12, 3, edge=False)
    hook.front.set(0, 0, "M4")
    # Fauld of steel lames.
    for name, z, motion, face_name in (("fauld_front", -2.85, "flap_front", "front"), ("fauld_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 10.8, z), motion=motion)
        solid(panel, "M", "smooth", S + 13, 2)
        for face in panel.sides:
            lames(face, 0, 2, "M", 2, step=1)
        lames(getattr(panel, face_name), 0, 2, "M", 2, step=3, rivet="M4", rivet_step=4)
        getattr(panel, face_name).hline(0, 8, 2, k("M", 0))
