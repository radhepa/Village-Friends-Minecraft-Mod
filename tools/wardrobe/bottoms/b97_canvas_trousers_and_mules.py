"""Canvas Trousers & Mules: canvas trousers turned up twice at the hem, worn with backless leather mules that bare the heel."""
from kit import SIDES, legs, waistband
from kit_male import toe_pieces
from paint import fabric

META = {
    "name": "Canvas Trousers & Mules",
    "gender": "male",
    "description": "Easy canvas workshop trousers turned up twice at the hem, worn with backless leather mules that leave the heel bare.",
    "tags": ["casual", "relaxed"],
}


def build(g):
    legs(g, "P", "twill", 9711, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 9712)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 7, "P3"), face.hline(0, face.w - 1, 8, "P1")    # double turn-up
            face.hline(0, face.w - 1, 9, "P3")
        for face in (pants.right, pants.front, pants.left):
            fabric(face, "L", "smooth", 9713, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "L0")
        pants.right.set(0, 10, None), pants.left.set(3, 10, None)       # the mule is open at the heel
        pants.back.hline(0, 3, 11, "L0")
        leg.bottom.fill("L0"), pants.bottom.fill("L0")
    for toe in toe_pieces(g, "mule_toe", (4, 1, 1), "L", base=2, y=10.9, z=-2.1):
        toe.front.set(1, 0, "L3")
