"""Oxford Button-Down: a crisp long-sleeved oxford shirt, tucked, with a buttoned-down collar."""
from kit_casual import chest_pocket, collar_points, long_sleeves, placket, shirt_body

META = {
    "name": "Oxford Button-Down",
    "gender": "male",
    "description": "A crisp long-sleeved oxford shirt tucked in, with a buttoned-down collar and a breast pocket.",
    "tags": ["casual", "modern", "tailored"],
    "tucked": True,
}


def build(g):
    body = shirt_body(g, "S", 3, "weave", 11401, hem=False)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(3, 1, "S2")
    placket(f, "S", 3, y0=1, y1=11, x=4, buttons=(2, 5, 8, 11), button="M3")
    chest_pocket(f, "S", 3, x0=5, y0=3)
    body.back.hline(0, 7, 2, "S2")
    body.back.vline(4, 3, 11, "S2")   # box pleat below the yoke
    long_sleeves(g, "S", 3, "weave", 11402, cuff="S4")
    collar_points(g, "S", 4, spread=16, button="M3")
