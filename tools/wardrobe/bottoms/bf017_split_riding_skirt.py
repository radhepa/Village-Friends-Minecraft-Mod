"""Split Riding Skirt: a divided wool skirt cut like wide culottes for the saddle, over tall folded riding boots."""
from kit import SIDES, leg_bone, legs, waistband
from kit_female import pleats, shoes
from paint import solid

META = {
    "name": "Split Riding Skirt",
    "gender": "female",
    "description": "A divided riding skirt, each leg cut wide and pleated like a skirt, over tall riding boots.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "weave", 11711, rows=(0, 9), crease=False)
    body = waistband(g, "P", "weave", 11712)
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "L2")
    for side in SIDES:
        upper = g.piece(f"{side}_culotte", leg_bone(side), (-2.5, -.2, -2.5), (5, 6, 5), inflate=.1)
        solid(upper, "P", "weave", 11713, 2)
        flare = g.piece(f"{side}_culotte_flare", leg_bone(side), (-3, 5, -3), (6, 3, 6), inflate=.05)
        solid(flare, "P", "weave", 11714, 2)
        for box in (upper, flare):
            for face in box.sides:
                pleats(face, "P", 2, 2, y0=1, lit=False)
        for face in flare.sides:
            face.hline(0, face.w - 1, 2, "P1")
        flare.bottom.fill("P0")
    shoes(g, "boot", "L", 2, top=6)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(1 if side == "right" else 2, 8, 10, "L3")
