"""Mounted Lancer's Breastplate: a ridged steel breastplate with a lance rest bolted to the right breast, plate
faulds, a backplate on crossed straps, couters at the elbows and mail at the shoulders."""
from kit import sleeves
from kit_female import arm_rings, mail, over_flaps
from kit_f04 import lames
from paint import fabric, solid, strip_fabric

META = {
    "name": "Mounted Lancer's Breastplate",
    "gender": "female",
    "description": "A ridged steel breastplate with a lance rest bolted to the right breast, plate faulds, a "
                   "backplate, round couters at the elbows and mail at the shoulders.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "weave", 54361, 2)                          # the arming doublet beneath
    fabric(b.top, "P", "weave", 54361, 3), fabric(b.bottom, "P", "weave", 54361, 1)
    for face in (b.right, b.left):
        face.vline(1, 1, 10, "L2"), face.set(1, 3, "M3"), face.set(1, 7, "M3")   # side straps and buckles
    sleeves(g, "P", "weave", 54362, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        mail(arm.strip, "M", 2, 0, 2)
        strip_fabric(arm, "M", "smooth", 54363, 2, 7, 11)             # vambraces
        arm.strip.hline(0, 15, 7, "M4"), arm.strip.hline(0, 15, 11, "M1")
        arm.front.vline(1, 8, 10, "M3")
    # The breastplate: a box over the chest with a raised medial ridge and a rolled neck edge.
    plate = g.piece("breastplate", "TORSO", (-4.5, 0, -1), (9, 8, 1), pivot=(0, .6, -2.25), inflate=.05)
    solid(plate, "M", "smooth", 54364, 2, edge=False)
    f = plate.front
    f.hline(0, 8, 0, "M4"), f.hline(0, 8, 7, "M1")
    f.vline(4, 1, 6, "M4"), f.vline(3, 1, 6, "M3"), f.vline(5, 1, 6, "M1")
    f.vline(0, 1, 6, "M1"), f.vline(8, 1, 6, "M1")
    ridge = g.piece("breastplate_ridge", "TORSO", (-.5, 0, -1), (1, 6, 1), pivot=(0, 1.6, -3.25))
    solid(ridge, "M", "smooth", 54365, 3, edge=False)
    ridge.front.vline(0, 0, 5, "M4")
    back = g.piece("backplate", "TORSO", (-4.5, 0, 0), (9, 8, 1), pivot=(0, .6, 2.25), inflate=.05)
    solid(back, "M", "smooth", 54366, 2, edge=False)
    back.back.hline(0, 8, 0, "M4"), back.back.hline(0, 8, 7, "M1"), back.back.vline(4, 1, 6, "M3")
    # The lance rest: a hinged bracket on the right breast with an upturned hook.
    rest = g.piece("lance_rest", "TORSO", (-1, 0, -2), (2, 1, 2), pivot=(-2.6, 5.0, -3.25))
    solid(rest, "M", "smooth", 54367, 2, edge=False)
    rest.top.fill("M3"), rest.front.set(0, 0, "M4")
    hook = g.piece("lance_rest_hook", "TORSO", (-1, -2, -1), (2, 2, 1), pivot=(-2.6, 5.0, -5.25))
    solid(hook, "M", "smooth", 54368, 2, edge=False)
    hook.front.hline(0, 1, 0, "M3")
    for x in (-3.4, -1.8):
        bolt = g.piece(f"lance_rest_bolt_{'r' if x < -2 else 'l'}", "TORSO", (-.5, -.5, -.5), (1, 1, 1),
                       pivot=(x, 4.0, -3.4))
        solid(bolt, "M", "smooth", 54369, 3, edge=False)
    # Faulds: three lames below the breastplate, riding the stride.
    f, bk = over_flaps(g, "faulds", 4, "M", "smooth", 54370, base=2, width=10, top=8.6)
    for face in (f, bk):
        lames(face, "M", 2, step=2)
        face.set(0, 0, "M4"), face.set(face.w - 1, 0, "M4")
    # Couters: round plates over each elbow with a fan on the outer side.
    for box in arm_rings(g, "couter", 3.6, 3, 5, inflate=.12):
        solid(box, "M", "smooth", 54371, 2)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 2, "M1")
            face.set(face.w // 2, 1, "M4")
    for side, bone in (("right", "RIGHT_ARM"), ("left", "LEFT_ARM")):
        ax = -4.4 if side == "right" else 3.4
        fan = g.piece(f"{side}_couter_fan", bone, (ax, 3.6, -1), (1, 3, 2))
        solid(fan, "M", "smooth", 54372, 2, edge=False)
        out = fan.right if side == "right" else fan.left
        out.vline(0, 0, 2, "M4"), out.vline(1, 0, 2, "M2"), out.set(0, 2, "M1")
