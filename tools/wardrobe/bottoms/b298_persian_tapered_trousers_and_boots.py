"""Persian Tapered Trousers and Boots: pin-striped silk trousers tapering into soft knee boots peaked at the front."""
from kit import SIDES, footwear, waistband
from kit_male import embroider, leg_blk, stripes, toe_pieces

META = {
    "name": "Persian Tapered Trousers and Boots",
    "gender": "male",
    "description": "Fine pin-striped silk trousers full at the hip and tapering into soft knee boots, each boot top rising to a peak over the shin with an embroidered band.",
    "tags": ["casual", "sturdy"],
}

STRIPE = ["S3", "S2", "A1", "S2"]


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        stripes(leg.strip, STRIPE, vertical=True, offset=i, rows=range(0, 5))
        stripes(leg.top, STRIPE, vertical=True)
        stripes(pants.strip, STRIPE, vertical=True, offset=i + 2, rows=range(0, 3))   # full at the hip
        pants.strip.hline(0, pants.strip.w - 1, 2, "S1")
    body = waistband(g, "S", "twill", 38101, base=3)
    body.front.vline(4, 10, 11, "S1")
    footwear(g, "boot", top=5, role="L", base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in (leg.front, pants.front):                              # the peak rising over the shin
            face.set(1, 3, "L3"), face.set(2, 3, "L3"), face.set(1, 4, "L2"), face.set(2, 4, "L2")
        for face in pants.sides:
            embroider(face, 6, "dots", "A3")
            face.hline(0, face.w - 1, 7, "A1")
        outer = pants.right if side == "right" else pants.left
        outer.vline(2, 8, 10, "L1")                                        # the side seam
        heel = leg_blk(g, f"{side}_boot_heel", side, 10.9, (2, 1, 1), "K", 2, "smooth", 38102, dz=2.1)
        heel.back.fill("K1")
    for toe in toe_pieces(g, "boot_toe", (2, 1, 1), "L", base=2, y=11.0, z=-2.0, seed=38104):
        toe.top.fill("L3")
