"""Basque Abarka Sandals and Trousers: dark knee breeches buttoned at the knee, white knitted stockings and rawhide abarkak gathered over the toes."""
from kit import SIDES, waistband
from kit_male import toe_pieces
from paint import fabric, strip_fabric

META = {
    "name": "Basque Abarka Sandals and Trousers",
    "gender": "male",
    "description": "Dark wool knee breeches slit and buttoned at the knee, thick white knitted stockings and rawhide abarkak puckered over the toes, their thongs wound round the ankle.",
    "tags": ["rugged", "work", "simple"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "twill", 38221 + i, 1, 0, 5)
        fabric(leg.top, "P", "twill", 38221, 1)
        strip_fabric(pants, "P", "twill", 38223 + i, 1, 0, 5)              # the breeches stand off the thigh
        pants.strip.hline(0, pants.strip.w - 1, 5, "P0")
        outer = pants.right if side == "right" else pants.left
        outer.vline(1, 2, 5, "P0")                                         # the knee slit
        for y in (2, 3, 4):
            outer.set(2, y, "M3")
        fabric(leg.strip, "S", "knit", 38225 + i, 3, 0, 6, leg.strip.w, 4)  # white knitted stockings
        fabric(leg.strip, "L", "leather", 38227, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "L", "leather", 38228, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "L3")
            face.hline(0, face.w - 1, 11, "L1")
        for y in (7, 8, 9):                                                 # thongs wound round the ankle
            for x in range(pants.strip.w):
                if (x + 2 * y + i) % 6 == 0:
                    pants.strip.set(x, y, "L2")
                    pants.strip.set((x + 1) % pants.strip.w, y, "L1")
        leg.bottom.fill("L1"), pants.bottom.fill("L0")
    waistband(g, "P", "twill", 38229, base=1)
    for toe in toe_pieces(g, "abarka_toe", (3, 1, 2), "L", base=2, y=11.0, z=-1.9, seed=38230):
        for x in range(3):
            toe.top.vline(x, 0, 1, "L3" if x % 2 == 0 else "L1")            # the rawhide puckered over the toes
        toe.front.set(1, 0, "L1")
