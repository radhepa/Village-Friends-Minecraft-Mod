"""Plain Wool Trousers: straight wool trousers on a narrow belt with a long metal-tipped tongue, over soft turnshoes."""
from kit import SIDES, belt, footwear, legs, waistband
from kit_m10 import outer, tie

META = {
    "name": "Plain Wool Trousers",
    "gender": "male",
    "description": "Straight, well-cut wool trousers with stitched side seams, a narrow belt whose metal-tipped tongue hangs long, and soft turnshoes.",
    "tags": ["casual", "simple"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "twill", 40020, rows=(0, 9), crease=False)):
        o = outer(leg, side)
        o.vline(2, 1, 9, "P1")                                            # side seam
        x = 1 if side == "right" else 2
        leg.front.vline(x, 4, 6, "P1" if side == "right" else "P2")       # soft knee fold
        leg.strip.hline(0, leg.strip.w - 1, 9, "P1")                      # the hem breaks over the shoe
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "P2")
    body = waistband(g, "P", "twill", 40021)
    body.front.vline(4, 10, 11, "P1")
    footwear(g, "turnshoe", top=10, base=2)
    belt(g, "waist_belt", 9.4, height=1, buckle="M")
    end = tie(g, "waist_belt_tongue", "TORSO", (1.6, 10.2, -2.75), "L", 3, 2, 40022)
    end.front.set(0, 2, "M3")
