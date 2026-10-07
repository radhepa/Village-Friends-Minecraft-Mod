"""Crusader's Mail Chausses: mail leggings laced behind the calf, domed knee cops, and leather shoes with prick spurs."""
from kit import SIDES, waistband
from kit_male import leg_blk, mail
from paint import fabric

META = {
    "name": "Crusader's Mail Chausses",
    "gender": "male",
    "description": "Riveted mail chausses laced behind the calf, domed steel knee cops, and leather shoes with prick spurs.",
    "tags": ["armor", "martial", "holy"],
    "locked_to": "t76_crusaders_cross_surcoat",
}


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        mail(leg.strip, rows=range(0, 10))
        mail(leg.top)
        leg.back.vline(1, 1, 9, "L2")                                     # lacing behind the calf
        fabric(leg.strip, "L", "leather", 7611, 1, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "L", "leather", 7612, 1, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
    waistband(g, "P", "quilt", 7613)
    for i, side in enumerate(SIDES):
        cop = leg_blk(g, f"{side}_knee_cop", side, 2.8, (4, 3, 1), "M", 2, "smooth", 7614 + i, dz=-2.4)
        cop.front.hline(1, 2, 0, "M4"), cop.front.set(1, 1, "M3"), cop.front.hline(0, 3, 2, "M1")
        spur = leg_blk(g, f"{side}_spur", side, 10.2, (1, 1, 2), "M", 3, "smooth", 7616 + i, dz=2.7)
        spur.back.fill("M4")
