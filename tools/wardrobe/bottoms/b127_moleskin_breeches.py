"""Moleskin Breeches: soft napped moleskin breeches tied below the knee with thongs, a leather kneeling pad on the right knee, ribbed stockings and laced ankle boots."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_m01 import outer
from kit_male import blk, lacing, ribbing
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Moleskin Breeches",
    "gender": "male",
    "description": "Soft napped moleskin breeches tied below the knee with leather thongs, a worn kneeling pad strapped to the right knee, ribbed wool stockings and laced ankle boots.",
    "tags": ["work", "casual", "simple"],
}


def nap(face, rows, ox=0):
    """Moleskin: a short dense nap that catches the light in soft diagonal streaks."""
    for y in rows:
        for x in range(face.w):
            d = (x + ox + y) % 7
            face.set(x, y, "P3" if d == 0 else "P1" if d == 4 else "P2")


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "velvet", 31540 + i, 2, 0, 5)
        nap(leg.strip, range(0, 6), i * 3)
        fabric(leg.top, "P", "velvet", 31540, 2)
        strip_fabric(pants, "P", "velvet", 31542 + i, 2, 0, 4)
        nap(pants.strip, range(0, 5), i * 3 + 1)
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "P1")
        o = outer(leg, side)
        lacing(o, 1, 3, 5, "L3", "L1")                                    # thong-laced knee opening
        ribbing(leg.strip, "S", 2, rows=range(6, 9))                       # ribbed stockings
        leg.strip.hline(0, leg.strip.w - 1, 5, "P0")
        tie = blk(g, f"{side}_knee_thong", (-2.4 if side == "right" else 2.4, 5.6, 0), (1, 2, 1), "L", 3, "plain",
                  31544 + i, bone=leg_bone(side), motion="sway", edge=False)
        tie.strip.hline(0, tie.strip.w - 1, 1, "L1")
    waistband(g, "P", "velvet", 31546)
    body = g.part("body")
    for face in body.sides:
        nap(face, range(10, 12), 2)
    body.front.vline(4, 9, 11, "P0"), body.front.set(3, 10, "M3")
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        lacing(pants.front, 1, 9, 10, "L4", "L1")
    # The kneeling pad: worn leather over the right knee, strapped behind, scuffed with soil.
    pad = g.piece("right_kneel_pad", "RIGHT_LEG", (-2, 0, -1), (4, 3, 1), pivot=(0, 3.4, -2.35))
    solid(pad, "L", "leather", 31547, 2)
    pad.front.hline(0, 3, 0, "L3"), pad.front.set(1, 1, "L1"), pad.front.set(2, 2, "K2"), pad.front.set(0, 2, "K3")
    strap = g.piece("right_kneel_strap", "RIGHT_LEG", (-2.5, 0, -2.5), (5, 1, 5), pivot=(0, 4.2, 0), inflate=.12)
    solid(strap, "L", "leather", 31548, 1, edge=False)
    outer(strap, "right").set(2, 0, k("M", 3))
