"""Buttoned Gaiters: canvas trousers under wool gaiters buttoned up the outside of each shin."""
from kit import SIDES, footwear, legs, waistband
from paint import fabric

META = {
    "name": "Buttoned Gaiters",
    "gender": "male",
    "description": "Canvas trousers under wool gaiters buttoned up the outer shin, with low boots.",
    "tags": ["casual", "sturdy", "rugged"],
}


def build(g):
    legs(g, "S", "twill", 1401, rows=(0, 9))
    waistband(g, "S", "twill", 1402)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            fabric(face, "P", "weave", 1403, 2, 0, 5, face.w, 5)
            face.hline(0, face.w - 1, 5, "P3")
            face.hline(0, face.w - 1, 9, "P1")
        outer = pants.right if side == "right" else pants.left
        outer.vline(2 if side == "right" else 1, 5, 9, "P1")
        for y in (6, 8):
            outer.set(1 if side == "right" else 2, y, "M3")
    footwear(g, "boot", top=10)
