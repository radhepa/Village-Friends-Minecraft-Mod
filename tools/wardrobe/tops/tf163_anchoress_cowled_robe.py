"""Anchoress's Cowled Robe: the walled-in recluse's coarse robe, a deep rolled cowl heaped about the neck,
long sleeves that swallow the hands, darned patches and a knotted rope girdle with a plain wooden cross."""
from kit import body, sleeves
from kit_female import OVER_FRONT, arm_rings, girdle, hanging, hood_down
from kit_f05 import dangle
from paint import fabric, solid

META = {
    "name": "Anchoress's Cowled Robe",
    "gender": "female",
    "description": "A coarse darned robe with a deep rolled cowl, sleeves long enough to hide the hands and a knotted rope girdle.",
    "tags": ["holy", "robe", "simple"],
    "locked_to": "bf163_anchoress_plain_robe_skirt",
    "covers_waist": True,
}


def darn(face, x, y, w=2, h=2):
    """A sewn-on patch: a lighter square of cloth inside a ring of dark stitching."""
    fabric(face, "P", "plain", 55095 + x, 2, x, y, w, h)
    for xx in range(x - 1, x + w + 1):
        face.set(xx, y - 1, "P0"), face.set(xx, y + h, "P0")
    for yy in range(y, y + h):
        face.set(x - 1, yy, "P0"), face.set(x + w, yy, "P0")


def build(g):
    b = body(g, "P", "plain", 55081, base=1)
    for face in (b.front, b.back):
        face.vline(2, 3, 11, "P0"), face.vline(5, 4, 11, "P2")
    darn(b.front, 5, 8), darn(b.back, 1, 5)
    for arm in sleeves(g, "P", "plain", 55082, base=1, rows=(0, 11)):
        arm.front.vline(1, 3, 9, "P0")
        # Long sleeves past the fingertips: the hands are tucked away inside them.
    for box in arm_rings(g, "long_sleeve", 6.5, 5, 5, inflate=.06):
        solid(box, "P", "weave", 55083, 1)
        for face in box.sides:
            face.vline(1, 1, 4, "P0"), face.hline(0, face.w - 1, 4, "P0")
        box.bottom.fill("K0")
    # The cowl: a thick roll of cloth round the neck, a heavy fold drooping onto the breast.
    roll = g.piece("cowl_roll", "TORSO", (-5, -1.6, -3.2), (10, 3, 6), inflate=.1)
    solid(roll, "P", "weave", 55084, 2)
    for face in roll.sides:
        face.hline(0, face.w - 1, 0, "P3"), face.hline(0, face.w - 1, 2, "P0")
        for x in range(1, face.w, 3):
            face.vline(x, 0, 1, "P1")
    fabric(roll.top, "P", "weave", 55084, 3)
    for x in range(2, 8):
        for y in range(2, 5):
            roll.top.set(x, y, "K0")                                    # the dark opening of the cowl
    droop = g.piece("cowl_droop", "TORSO", (-3.5, 0, 0), (7, 3, 2), pivot=(0, 1.2, -3.4), rotation=(-8, 0, 0))
    solid(droop, "P", "weave", 55085, 2)
    droop.front.hline(0, 6, 0, "P3"), droop.front.hline(1, 5, 2, "P0"), droop.front.vline(3, 0, 1, "P1")
    hood_down(g, "cowl_hood", "P", "weave", 55086, 1)
    # The knotted rope girdle with its long knotted end and a plain wooden cross.
    girdle(g, "rope_girdle", 8.0, role="S", base=2, height=1, buckle=None, texture="plain")
    end = hanging(g, "rope_end", 2.0, 10, role="S", base=2, top=8.8)
    for y in (2, 5, 8):
        end.front.set(0, y, "S0"), end.back.set(0, y, "S0")
    dangle(g, "cross_cord", -2.2, 0, (1, 2, 1), "L", 1, "plain", top=8.8, seed=55087, edge=False)
    upright = dangle(g, "cross_upright", -2.2, 2, (1, 5, 1), "L", 3, "plain", top=8.8, seed=55088, edge=False)
    for face in upright.sides:
        face.set(0, 4, "L2")
    arms = g.piece("cross_arms", "TORSO", (-1.5, 3, -.25), (3, 1, 1), pivot=(-2.2, 8.8, OVER_FRONT - .1),
                   motion="flap_front")
    solid(arms, "L", "plain", 55089, 3, edge=False)
    arms.front.set(0, 0, "L2"), arms.front.set(2, 0, "L2")
