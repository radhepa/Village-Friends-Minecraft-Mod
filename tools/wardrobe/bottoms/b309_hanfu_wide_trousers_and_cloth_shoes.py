"""Hanfu Wide Trousers and Cloth Shoes: wide pale trousers and black cloth shoes on white soles with upturned cloud-head toes."""
from kit import SIDES, legs, waistband
from kit_male import toe_pieces
from paint import fabric, strip_fabric

META = {
    "name": "Hanfu Wide Trousers and Cloth Shoes",
    "gender": "male",
    "description": "Wide pale trousers falling loose to the ankle, and black cloth shoes on white layered soles, each toe turned up in a cloud-head scroll.",
    "tags": ["scholarly", "robe"],
    "locked_to": "t309_song_scholars_hanfu_robe",
}


def build(g):
    legs(g, "S", "weave", 38541, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 38542, base=3)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(pants, "S", "weave", 38543 + i, 3, 0, 9)              # wide legs stand off the shin
        for x in range(1, pants.strip.w, 4):
            pants.strip.vline(x, 2, 8, "S2")
        pants.strip.hline(0, pants.strip.w - 1, 9, "S1")
        fabric(leg.strip, "K", "plain", 38545, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "K", "plain", 38546, 2, 0, 10, face.w, 1)
            face.hline(0, face.w - 1, 11, "S4")                            # white layered sole
        leg.bottom.fill("S3"), pants.bottom.fill("S2")
    for toe in toe_pieces(g, "shoe_toe", (2, 1, 1), "K", base=2, y=11.0, z=-2.0, seed=38547):
        toe.top.fill("K3")
        toe.front.fill("S4")
    for tip in toe_pieces(g, "cloud_toe", (2, 2, 1), "K", base=2, y=9.4, z=-2.6, seed=38549):
        tip.front.set(0, 0, "S4"), tip.front.set(1, 0, "S4"), tip.front.set(0, 1, "S3")   # the cloud scroll
        tip.top.fill("K3")
