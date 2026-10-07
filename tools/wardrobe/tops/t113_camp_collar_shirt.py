"""Camp-Collar Shirt: a short-sleeved button-up with an open, flat collar, worn loose."""
from kit_casual import chest_pocket, collar_points, placket, short_sleeves, shirt_body

META = {
    "name": "Camp-Collar Shirt",
    "gender": "male",
    "description": "A loose short-sleeved button-up with an open flat collar and a breast pocket.",
    "tags": ["casual", "modern", "relaxed"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "A", 2, "weave", 11301)
    f = body.front
    for x, y in ((3, 0), (4, 0), (3, 1), (4, 1), (4, 2)):
        f.clear(x, y)
    f.set(2, 1, "A3"), f.set(5, 1, "A1"), f.set(3, 2, "A3"), f.set(4, 3, "A1")
    placket(f, "A", 2, y0=4, y1=11, x=4, buttons=(5, 8), button="S4")
    chest_pocket(f, "A", 2, x0=1, y0=4)
    body.back.hline(0, 7, 2, "A1")
    short_sleeves(g, "A", 2, "weave", 11302, length=5)
    collar_points(g, "A", 3, spread=34, y=.2)
