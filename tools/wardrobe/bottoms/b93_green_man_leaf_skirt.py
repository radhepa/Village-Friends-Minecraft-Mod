"""Green Man's Leaf Skirt: a short skirt of layered leaves over leaf-scaled leggings and bark-brown turnshoes."""
from kit import SIDES, footwear, waistband
from kit_male import skirt_panels

META = {
    "name": "Green Man's Leaf Skirt",
    "gender": "male",
    "description": "A short skirt of layered leaves over leggings sewn with overlapping leaf scales, and bark-brown turnshoes.",
    "tags": ["whimsical", "rugged"],
    "locked_to": "t93_green_man_leaf_mantle",
}


def leaves(face, offset=0, rows=None):
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            lx, ly = (x + face.x0 + offset + (y // 3) * 2) % 3, y % 3
            face.set(x, y, "P3" if ly == 2 and lx == 1 else "P1" if lx == 1 else "P2")


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leaves(leg.strip, rows=range(0, 10))
        leaves(leg.top)
    body = waistband(g, "P", "weave", 9311)
    for face in body.sides:
        leaves(face, rows=range(9, 12))
    footwear(g, "turnshoe", top=10, role="L", base=1)
    front, back, sides = skirt_panels(g, "leaf_skirt", 4, "P", "plain", 9312, top=10.4, sides=False)
    for face in (front, back):
        leaves(face, 1)
        for x in range(1, face.w, 3):
            face.set(x, 3, "P3")                                         # leaf points at the hem
