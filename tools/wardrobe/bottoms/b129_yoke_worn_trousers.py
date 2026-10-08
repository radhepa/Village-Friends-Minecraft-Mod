"""Yoke-Worn Trousers: heavy hemp trousers worn thin from long days beside the team, darned at the knees, a shiny worn seat and frayed hems over low turnshoes."""
from kit import SIDES, footwear, legs, waistband

META = {
    "name": "Yoke-Worn Trousers",
    "gender": "male",
    "description": "Heavy hemp trousers worn thin from long days walking beside the team: faded thighs, criss-cross darning over both knees, a shiny worn seat and frayed hems over low turnshoes.",
    "tags": ["work", "simple", "rugged"],
}


def darn(face, x0, y0, w, h):
    """Darning: a woven grid of pale thread over a worn-through patch."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            face.set(x, y, "S3" if (x + y) % 2 == 0 else "P1")


def build(g):
    leg_boxes = legs(g, "P", "twill", 31590, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 31591)
    footwear(g, "turnshoe", top=10, base=2)
    for side, leg in zip(SIDES, leg_boxes):
        f = leg.front
        for y in range(0, 3):                                             # faded where the thighs rub
            for x in range(1, 3):
                f.set(x, y, "P3")
        if side == "right":
            darn(f, 1, 4, 3, 2)                                           # darned over the knee
            f.hline(1, 3, 3, "P1")
        else:
            darn(f, 0, 5, 2, 2)
            f.hline(0, 1, 4, "P1")
        leg.back.hline(0, 3, 0, "P3"), leg.back.set(1, 1, "P4")            # the worn, shiny seat
        for face in (leg.right, leg.left):
            face.vline(2, 1, 8, "P1")
    body = g.part("body")
    body.back.hline(1, 6, 11, "P3"), body.back.set(3, 10, "P4")
    # Frayed hems: the cloth ends raggedly over the ankle, loose threads standing off it.
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for x in range(leg.strip.w):
            if (x + i) % 3 == 0:
                leg.strip.set(x, 9, None)                                 # bare ankle through the fray
            elif (x + i) % 3 == 1:
                leg.strip.set(x, 9, "P1")
        for x in range(pants.strip.w):
            pants.strip.set(x, 7, "P2" if x % 2 else "P3")
            if (x + i) % 2 == 0:
                pants.strip.set(x, 8, "P1")                               # threads hanging loose
