"""Arrow-Bag Thigh Trousers: twill trousers with a linen arrow bag strapped to the right thigh, fletchings showing, and boots."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from paint import solid

META = {
    "name": "Arrow-Bag Thigh Trousers",
    "gender": "male",
    "description": "Twill field trousers with a linen arrow bag strapped to the right thigh, its fletchings showing, over laced boots.",
    "tags": ["martial", "rugged"],
}


def build(g):
    legs(g, "P", "twill", 7411, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 7412)
    footwear(g, "boot", top=9, base=2)
    straps = g.part("right_pants").strip
    for y in (1, 5):
        straps.hline(0, straps.w - 1, y, "L1")                            # thigh straps holding the bag
    for side in SIDES:
        g.part(f"{side}_leg").front.vline(1 if side == "right" else 2, 1, 8, "P1")
    bone = leg_bone("right")
    bag = g.piece("arrow_bag", bone, (-1, 0, -1.5), (2, 6, 3), pivot=(-2.6, .6, 0), rotation=(0, 0, 6))
    solid(bag, "S", "weave", 7413, 2)
    for face in bag.sides:
        face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 3, "L2")
    for i, dz in enumerate((-.8, .6)):
        fl = g.piece(f"arrow_fletch_{i}", bone, (-.5, -2, -.5), (1, 2, 1), pivot=(-2.6, .6, dz), rotation=(0, 0, 6))
        solid(fl, "A" if i else "S", "plain", 7414 + i, 3)
        fl.strip.hline(0, fl.strip.w - 1, 1, "L3")
