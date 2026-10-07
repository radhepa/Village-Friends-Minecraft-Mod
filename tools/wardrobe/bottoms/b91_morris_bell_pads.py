"""Morris Bell Pads: white dancing breeches with leather pads of jingling bells strapped to the shins, ribbons streaming, black shoes."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import leg_blk
from paint import solid

META = {
    "name": "Morris Bell Pads",
    "gender": "male",
    "description": "White dancing breeches with leather pads of jingling bells strapped to the shins, ribbons streaming from them, and black shoes.",
    "tags": ["whimsical", "casual"],
    "locked_to": "t91_morris_dancers_baldrics",
}


def build(g):
    legs(g, "S", "weave", 9111, base=4, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 9112, base=4)
    footwear(g, "shoe", top=10, role="K", base=1, sole="K0")
    for i, side in enumerate(SIDES):
        pad = leg_blk(g, f"{side}_bell_pad", side, 5.0, (5, 3, 5), "L", 2, "leather", 9113 + i, inflate=.1)
        for face in pad.sides:
            for x in range(face.w):
                face.set(x, 1, "M4" if x % 2 == 0 else "M2")                # rows of little bells
            face.hline(0, face.w - 1, 0, "A2")
        ribbon = g.piece(f"{side}_pad_ribbon", leg_bone(side), (-.5, 0, -.5), (1, 3, 1),
                         pivot=(-2.4 if side == "right" else 2.4, 5.4, -.6), motion="sway")
        solid(ribbon, "A" if side == "right" else "P", "plain", 9115 + i, 3)
