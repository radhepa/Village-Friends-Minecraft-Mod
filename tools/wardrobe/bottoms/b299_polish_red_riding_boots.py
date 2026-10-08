"""Polish Red Riding Boots: slim trousers in tall boots of dyed morocco leather, iron-tipped heels and a stitched front seam."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk, toe_pieces

META = {
    "name": "Polish Red Riding Boots",
    "gender": "male",
    "description": "Slim trousers tucked into tall boots of bright dyed morocco leather, the tops rising to a curve at the front, with iron-tipped heels and a stitched front seam.",
    "tags": ["sturdy", "fancy"],
}


def build(g):
    legs(g, "S", "twill", 38141, rows=(0, 4), crease=False)
    waistband(g, "S", "twill", 38142)
    footwear(g, "boot", top=4, role="A", base=2, toe="A3")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in (leg.front, pants.front):
            face.set(1, 3, "A3"), face.set(2, 3, "A3")                       # the curved top rises at the shin
            face.vline(1, 5, 10, "A1")                                       # stitched front seam
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "A4")
        outer = pants.right if side == "right" else pants.left
        outer.vline(2, 5, 10, "A1")
        heel = leg_blk(g, f"{side}_boot_heel", side, 10.4, (3, 2, 1), "K", 2, "smooth", 38143, dz=2.15)
        for face in heel.sides:
            face.hline(0, face.w - 1, 1, "M3")                              # the iron heel tip
    for toe in toe_pieces(g, "boot_toe", (2, 1, 1), "A", base=2, y=11.0, z=-2.0, seed=38145):
        toe.top.fill("A3")
