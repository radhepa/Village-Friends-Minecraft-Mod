"""Pattened Shoes: woollen hose and low shoes raised on wooden pattens strapped over the instep against the mud."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk

META = {
    "name": "Pattened Shoes",
    "gender": "male",
    "description": "Wool trousers and pale hose over low shoes, raised on wooden pattens strapped across the instep against the mud.",
    "tags": ["work", "simple"],
}


def build(g):
    legs(g, "P", "weave", 4011, rows=(0, 8), crease=False)
    waistband(g, "P", "weave", 4012)
    footwear(g, "shoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, leg.strip.w - 1, 8, "P1")
        leg.strip.hline(0, leg.strip.w - 1, 9, "S3")                  # a band of hose above the shoe
        sole = leg_blk(g, f"{side}_patten", side, 11.0, (4, 1, 5), "L", 3, "plain", 4013 + i, inflate=.3)
        for face in sole.sides:
            face.set(0, 0, "L2"), face.set(face.w - 1, 0, "L2")       # rounded wooden ends
        sole.bottom.fill("L1")
        strap = leg_blk(g, f"{side}_patten_strap", side, 9.8, (4, 1, 3), "L", 1, "leather", 4015 + i, dz=-1.0,
                        inflate=.3)
        strap.front.set(1, 0, "M3"), strap.front.set(2, 0, "M3")
