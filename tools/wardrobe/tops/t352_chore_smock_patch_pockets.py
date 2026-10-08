"""Chore Smock with Patch Pockets: a loose canvas smock with a gathered yoke, half placket and two deep hip patch pockets."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import blk
from paint import dark_seams

META = {
    "name": "Chore Smock with Patch Pockets",
    "gender": "male",
    "description": "A loose canvas chore smock gathered under a shoulder yoke, a two-button half placket, buttoned cuffs and two deep patch pockets at the hips, a wooden dibber poking from one.",
    "tags": ["casual", "simple", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 40340, base=2)
    f, bk = b.front, b.back
    f.clear(3, 0), f.clear(4, 0)
    # Shoulder yoke and the gathers below it.
    for face in (f, bk):
        face.hline(0, 7, 2, "P3")
        for x in (1, 3, 5):
            face.vline(x, 3, 4, "P1")
    # Half placket with two buttons.
    f.vline(4, 1, 6, "P3"), f.vline(3, 1, 6, "P1")
    f.set(4, 2, "L3"), f.set(4, 4, "L3")
    dark_seams(b, faces=("right", "left"))
    collar(g, "smock_collar", "P", "twill", base=3, height=1, y=-.5)
    # Full sleeves with a buttoned cuff.
    sleeves(g, "P", "weave", 40341, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 8, "P1")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "P2")
        (arm.right if side == "right" else arm.left).set(2, 9, "L3")
    # Two deep patch pockets standing proud at the hips.
    for name, x in (("right", -2.2), ("left", 2.2)):
        pocket = blk(g, f"{name}_patch_pocket", (x, 7.4, -2.4), (3, 3, 1), "P", 2, "weave", 40342 + (name == "left"))
        for face in pocket.sides:
            face.hline(0, face.w - 1, 0, "P4")
        pocket.front.set(0, 1, "P1"), pocket.front.set(2, 1, "P1")
        pocket.front.hline(0, 2, 2, "P1")
    dibber = blk(g, "dibber", (2.6, 5.8, -2.3), (1, 3, 1), "L", 3, "smooth", 40344, edge=False)
    dibber.front.set(0, 0, "L4"), dibber.top.fill("L4")
    # Smock skirt to the upper thigh, side seams vented.
    for face in flaps(g, "smock_hem", 4, "P", "weave", 40345, top=11.0):
        face.hline(0, 8, 3, "P1")
        face.vline(0, 1, 3, "P1"), face.vline(8, 1, 3, "P1")
