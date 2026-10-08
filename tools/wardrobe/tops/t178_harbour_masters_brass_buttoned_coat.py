"""Harbour Master's Brass-Buttoned Coat: a double-breasted wool sea coat with two rows of brass buttons, a stand
collar, broad buttoned cuffs and a brass speaking horn hung at the hip from a cord across the chest."""
from kit import body, collar, flaps, sleeves
from kit_male import arm_blk, blk
from paint import line

META = {
    "name": "Harbour Master's Brass-Buttoned Coat",
    "gender": "male",
    "description": "A double-breasted wool sea coat with two rows of brass buttons, a stand collar, broad buttoned cuffs "
                   "and a brass speaking horn hung at the hip on a cord.",
    "tags": ["tailored", "sea", "fancy"],
    "covers_waist": True,
}

HORN = (2.6, 9.8, -3.9)      # the horn's cord meets it here; mouthpiece, tube and bell share the hinge


def build(g):
    b = body(g, "P", "twill", 33280)
    f = b.front
    f.vline(5, 1, 11, "P3"), f.vline(6, 1, 11, "P1")                    # the wide overlapping front edge
    for y in range(2, 10, 2):
        f.set(1, y, "M3"), f.set(4, y, "M3")                             # two rows of brass buttons
        f.set(1, y + 1, "P1"), f.set(4, y + 1, "P1")
    f.hline(1, 6, 1, "P3")
    for face in (b.right, b.left):
        face.vline(1 if face is b.right else 2, 1, 11, "P1")            # side seams
    b.back.vline(3, 6, 11, "P1"), b.back.set(3, 6, "M3")                 # back vent with its button
    sleeves(g, "P", "twill", 33281, rows=(0, 10))
    for side in ("right", "left"):
        cuff = arm_blk(g, f"{side}_turned_cuff", side, 6.6, (5, 3, 5), "P", 3, "twill", 33282 + (side == "left"),
                       inflate=.1)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "P4")
            face.hline(0, face.w - 1, 2, "P1")
        outer = cuff.right if side == "right" else cuff.left
        outer.set(1, 1, "M3"), outer.set(3, 1, "M3")
        cuff.front.set(2, 1, "M3")
    stand = collar(g, "stand_collar", "P", "twill", base=2, height=2, y=-1.2)
    for face in stand.sides:
        face.hline(0, face.w - 1, 0, "A2")
    stand.front.set(3, 1, "M3"), stand.front.set(5, 1, "M3")
    # The horn's cord, from the right shoulder down across the chest to the left hip.
    jacket = g.part("jacket")
    line(jacket.front, 0, 0, 6, 9, "A2"), line(jacket.back, 7, 0, 1, 9, "A2")
    jacket.top.vline(0, 0, 3, "A2")
    # The speaking horn: a brass mouthpiece, a tapering tube and a flared bell, hanging bell down.
    mouth = blk(g, "speaking_horn_mouth", HORN, (1, 1, 1), "M", 3, "smooth", 33284, origin=(-.5, 0, -.5),
                motion="flap_front", edge=False)
    mouth.top.fill("K1")
    tube = blk(g, "speaking_horn_tube", HORN, (2, 2, 2), "M", 2, "smooth", 33285, origin=(-1, 1.0, -1),
               motion="flap_front", edge=False)
    tube.front.set(0, 0, "M4")
    bell = blk(g, "speaking_horn_bell", HORN, (3, 2, 2), "M", 3, "smooth", 33286, origin=(-1.5, 3.0, -1),
               motion="flap_front")
    for face in bell.sides:
        face.hline(0, face.w - 1, face.h - 1, "M4")
    bell.front.set(0, 0, "M4")
    bell.bottom.fill("K1")
    for face in flaps(g, "coat_skirt", 5, "P", "twill", 33287, top=10.8, slit=True):
        face.hline(0, 8, 4, "P1")
        face.set(3, 1, "M3"), face.set(5, 1, "M3")
