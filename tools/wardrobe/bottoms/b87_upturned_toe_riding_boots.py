"""Upturned-Toe Riding Boots: loose riding trousers in tall boots with embroidered tops and toes that curl upward."""
from kit import SIDES, footwear, legs, waistband
from kit_male import embroider, toe_pieces

META = {
    "name": "Upturned-Toe Riding Boots",
    "gender": "male",
    "description": "Loose steppe riding trousers stuffed into tall leather boots with embroidered tops and toes that curl upward.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 8711, rows=(0, 3), crease=False)
    waistband(g, "P", "weave", 8712)
    footwear(g, "boot", top=3, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 3, "A2")
            embroider(face, 4, "diamond", "A3", "A1")
            face.vline(0, 7, 10, "L1")
    for toe in toe_pieces(g, "boot_toe", (2, 1, 2), "L", base=2, y=10.9, z=-2.1):
        toe.top.fill("L3")
    for tip in toe_pieces(g, "boot_toe_curl", (2, 2, 1), "L", base=3, y=9.6, z=-4.0, rotation=(20, 0, 0)):
        tip.front.set(0, 0, "A2"), tip.front.set(1, 0, "A2")
