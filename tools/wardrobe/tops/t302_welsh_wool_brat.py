"""Welsh Wool Brat: a fringed wool mantle crossing from the left shoulder to the right hip over a plain tunic, a penannular brooch and an archer's bracer."""
from kit import belt, body, flaps, sleeves
from kit_male import arm_blk, back_drape, blk
from paint import fabric, k, strip_fabric

META = {
    "name": "Welsh Wool Brat",
    "gender": "male",
    "description": "A fringed woollen brat thrown over the left shoulder and across to the right hip, pinned with a penannular brooch over a plain belted tunic, a leather bracer on the bow arm.",
    "tags": ["rugged", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 38241)
    b.front.clear(3, 0), b.front.clear(4, 0)
    sleeves(g, "S", "weave", 38242, rows=(0, 10), cuff="S1")
    jacket = g.part("jacket")
    jf = jacket.front
    # The brat crosses from the left shoulder (x 7) down to the right hip, its edge striped and fringed.
    for y in range(11):
        xc = 6 - round(y * .6)
        for x in range(xc - 2, xc + 3):
            if 0 <= x < 8:
                jf.set(x, y, "P1" if (x + y) % 6 == 0 else "P2")
        if 0 <= xc - 2 < 8:
            jf.set(xc - 2, y, "A2")                                        # woven stripe along the edge
        if 0 <= xc - 3 < 8 and y % 2 == 0:
            jf.set(xc - 3, y, "P3")                                        # fringe
    for face in (jacket.back, jacket.left):
        fabric(face, "P", "weave", 38243, 2)
    fabric(jacket.top, "P", "weave", 38243, 3, 4, 0, 4, 4)
    shoulder = g.part("left_sleeve")                                        # the brat falls over the left shoulder
    for face in shoulder.sides:
        fabric(face, "P", "weave", 38249, 2, 0, 0, face.w, 3)
        for x in range(face.w):
            if x % 2 == 0:
                face.set(x, 3, "P3")                                       # fringe
    fabric(shoulder.top, "P", "weave", 38249, 3)
    jacket.back.hline(0, 7, 0, "P3")
    drape = back_drape(g, "brat_drape", "P", 12, "weave", 38244, width=9, y=.5, z=2.55, tilt=6)
    for face in drape.sides:
        face.hline(0, face.w - 1, 9, "A2")
        for x in range(face.w):
            face.set(x, 11, "P3" if x % 2 == 0 else "P1")                    # fringed lower edge
    drape.back.vline(2, 1, 8, "P1"), drape.back.vline(6, 2, 8, "P1")
    ring = blk(g, "penannular_ring", (2.4, .6, -2.85), (2, 2, 1), "M", 3, "smooth", 38245, edge=False)
    ring.front.set(1, 1, "M1"), ring.front.set(0, 0, "M4")
    pin = blk(g, "penannular_pin", (2.3, .1, -3.15), (1, 3, 1), "M", 2, "smooth", 38246, rotation=(0, 0, 35), edge=False)
    pin.front.set(0, 0, "M4")
    bracer = arm_blk(g, "archer_bracer", "left", 5.0, (5, 3, 5), "L", 2, "leather", 38247, inflate=.04)
    for face in bracer.sides:
        face.hline(0, face.w - 1, 0, "L3")
        face.set(1, 1, "L0"), face.set(3, 1, "L0")
    belt(g, "belt", 9.4, height=1)
    for face in flaps(g, "tunic_hem", 3, "S", "weave", 38248, top=10.6):
        face.hline(0, 8, 2, "S1")
