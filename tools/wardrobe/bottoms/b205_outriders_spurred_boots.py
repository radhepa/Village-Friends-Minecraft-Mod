"""Outrider's Spurred Boots: dusty funnel-topped thigh boots with spur leathers over the instep and big star rowels."""
from kit import SIDES, footwear, legs, waistband
from kit_male import flecks
from kit_m04 import sides_of, spur
from paint import solid

META = {
    "name": "Outrider's Spurred Boots",
    "gender": "male",
    "description": "Breeches in road-dusted thigh boots that flare into wide stiff funnel tops, spur leathers buckled across "
                   "the instep and long-necked spurs with big star rowels.",
    "tags": ["rugged", "sturdy", "martial"],
}

S = 34380


def build(g):
    legs(g, "P", "twill", S, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", S + 2)
    footwear(g, "boot", top=3, base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            flecks(face, "L4", S + 3, .05, rows=range(9, 11))              # road dust
        pants.front.hline(0, 3, 10, "L0")                                  # spur leather over the instep
        getattr(pants, sides_of(side)[0]).set(2, 10, "M3")
        pants.back.hline(0, 3, 10, "L0")
    for i, side in enumerate(SIDES):
        funnel = g.piece(f"{side}_boot_funnel", "RIGHT_LEG" if side == "right" else "LEFT_LEG", (-2.5, 0, -3), (5, 2, 6),
                         pivot=(0, 1.4, 0))
        solid(funnel, "L", "leather", S + 4 + i, 2, edge=False)
        for face in funnel.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 1, "L1")
            face.set(2, 1, "L2"), face.set(4, 0, "L3")
        neck, star = spur(g, side, y=9.8, seed=S + 6 + 2 * i, z=2.2)
        cross = g.piece(f"{side}_spur_rowel_cross", "RIGHT_LEG" if side == "right" else "LEFT_LEG", (-.5, 0, .6),
                        (1, 1, 3), pivot=(0, 9.8, 2.2))
        solid(cross, "M", "smooth", S + 10 + i, 3, edge=False)
        for face in (cross.right, cross.left):
            face.set(0, 0, "M4"), face.set(2, 0, "M4"), face.set(1, 0, "M1")
