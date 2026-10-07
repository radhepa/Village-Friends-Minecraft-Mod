"""Lozenge-Woven Trews: trews woven in a diamond twill with accent lozenges, and soft ankle boots folded at the top."""
from kit import SIDES, footwear, waistband
from kit_male import lozenge

META = {
    "name": "Lozenge-Woven Trews",
    "gender": "male",
    "description": "Close trews woven in a diamond twill with small accent lozenges, worn in soft ankle boots folded at the top.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        lozenge(leg.strip, "P", 2, step=4, ox=i * 2, rows=range(0, 10))
        lozenge(leg.top, "P", 2, step=4)
        for y in range(1, 10, 4):
            for x in range(leg.strip.w):
                if (x + i * 2 + y) % 4 == 2 and (x + i * 2 - y) % 4 == 2:
                    leg.strip.set(x, y, "A2")
    waistband(g, "P", "twill", 6311)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L4"), face.hline(0, face.w - 1, 10, "L1")
