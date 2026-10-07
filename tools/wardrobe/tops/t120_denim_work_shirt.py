"""Denim Work Shirt: a denim shirt with twin flap pockets, snap buttons and sleeves rolled up."""
from kit_casual import chest_pocket, collar_points, long_sleeves, placket, rolled_cuffs, shirt_body

META = {
    "name": "Denim Work Shirt",
    "gender": "male",
    "description": "A denim work shirt with twin flap pockets, metal snaps and sleeves rolled to the forearm.",
    "tags": ["casual", "modern", "work"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "D", 2, "twill", 12001)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    placket(f, "D", 2, y0=1, y1=11, x=4, buttons=(2, 6, 9), button="M3")
    chest_pocket(f, "D", 2, x0=0, y0=2, flap=True, snap="M3")
    chest_pocket(f, "D", 2, x0=5, y0=2, flap=True, snap="M3")
    body.back.hline(0, 7, 2, "M2")   # yoke, top-stitched
    body.back.hline(0, 7, 3, "D1")
    long_sleeves(g, "D", 2, "twill", 12002, end=5)
    rolled_cuffs(g, "D", 3, y=2.4)
    collar_points(g, "D", 3, spread=20)
