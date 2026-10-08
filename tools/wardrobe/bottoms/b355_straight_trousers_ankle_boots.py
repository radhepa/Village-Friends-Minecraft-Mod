"""Straight Wool Trousers and Ankle Boots: dark pressed wool trousers falling straight onto ankle boots with a buckled strap and a heel pull-tab."""
from kit import SIDES, leg_bone
from kit_casual import leather_belt, shoes, trousers
from kit_m10 import outer
from paint import solid

META = {
    "name": "Straight Wool Trousers and Ankle Boots",
    "gender": "male",
    "description": "Dark wool trousers pressed with a sharp crease and falling straight onto stout ankle boots, each closed by a buckled strap round the ankle, with a pull-tab at the heel.",
    "tags": ["casual", "tailored", "sturdy"],
}


def build(g):
    legs, body = trousers(g, "K", 2, "twill", 40480, end=8, crease=True)
    for side, leg in zip(SIDES, legs):
        outer(leg, side).vline(2, 1, 8, "K1")
        leg.strip.hline(0, leg.strip.w - 1, 8, "K1")
    shoes(g, "boot", top=10)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L1")                            # the ankle strap
        o = outer(pants, side)
        o.set(1, 9, "M3")
        buckle = g.piece(f"{side}_boot_buckle", leg_bone(side), (-.5, -.5, -.5), (1, 1, 1),
                         pivot=(-2.4 if side == "right" else 2.4, 9.5, -.6))
        solid(buckle, "M", "smooth", 40481 + i, 3, edge=False)
        tab = g.piece(f"{side}_heel_tab", leg_bone(side), (-.5, 0, 0), (1, 2, 1), pivot=(0, 7.4, 2.15), rotation=(-12, 0, 0))
        solid(tab, "L", "leather", 40483 + i, 2, edge=False)
        tab.back.set(0, 0, "L3")
        g.part(f"{side}_pants").strip.hline(0, 15, 8, "K1")              # trouser hem breaking on the boot
    leather_belt(g)
