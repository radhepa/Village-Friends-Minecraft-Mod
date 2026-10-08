"""Gamekeeper's Gaiters: windowpane-check breeches under thigh-high leather leggings strapped and buckled twice up the outside, over nailed boots."""
from kit import SIDES, footwear, legs, waistband
from kit_m07 import leg_shell, outer, windowpane

META = {
    "name": "Gamekeeper's Gaiters",
    "gender": "male",
    "description": "Windowpane-check wool breeches under stiff leather leggings that climb past the knee, strapped and buckled twice up the outside, over hobnailed boots for wet coverts.",
    "tags": ["sturdy", "rugged", "work"],
}


def build(g):
    legs(g, "P", "twill", 37220, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 37221)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        windowpane(leg.strip, "P", 2, rows=range(0, 3))
    body = g.part("body")
    windowpane(body.front, "P", 2, ox=2, rows=range(10, 12)), windowpane(body.back, "P", 2, ox=2, rows=range(10, 12))
    footwear(g, "boot", top=10, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            for x in range(0, face.w, 2):
                face.set(x, 11, "M1")                                    # hobnails round the sole
    for side, shell in zip(SIDES, leg_shell(g, "legging", 2.6, 8, "L", 2, "leather", 37222)):
        for face in shell.sides:
            face.hline(0, face.w - 1, 0, "L3")                           # the rolled top edge
            face.hline(0, face.w - 1, 7, "L1")
            for y in (2, 5):
                face.hline(0, face.w - 1, y, "L1")                       # strap bands
        o = outer(shell, side)
        for y in (2, 5):
            o.set(3, y, "M3")                                            # buckles on the outer face
        o.vline(2, 1, 6, "L1")                                           # the overlap seam
        shell.front.vline(2, 2, 6, "L3")                                 # a moulded ridge over the shin
