"""Deacon's Dalmatic: a wide-sleeved, knee-length dalmatic with two clavi from shoulder to hem, fringed edges and tasselled cords at the back, over alb sleeves."""
from kit import body, neckline, sleeves
from kit_male import sleeve_shapes
from kit_m05 import cord_end, over_panels

META = {
    "name": "Deacon's Dalmatic",
    "gender": "male",
    "description": "A deacon's knee-length dalmatic with short, wide sleeves, two bright clavi running from shoulder to fringed hem, and tasselled cords hanging behind, over the white alb.",
    "tags": ["holy", "robe", "fancy"],
    "locked_to": "b224_deacons_alb_hem",
    "covers_waist": True,
}


def clavi(face, xs, y0, y1):
    for x in xs:
        face.vline(x, y0, y1, "A2")
        face.set(x, y0, "A3")


def build(g):
    b = body(g, "P", "weave", 35120)
    neckline(b.front, "round", "P")
    b.front.set(3, 0, "S4"), b.front.set(4, 0, "S4")                   # the alb's amice at the throat
    for face in (b.front, b.back):
        clavi(face, (1, 6), 0, 11)
        face.vline(3, 3, 11, "P1")
    sleeves(g, "S", "weave", 35121, base=3, rows=(0, 10), cuff="S2")
    for s in sleeve_shapes(g, "dalmatic_sleeve", "P", -2.1, (5, 7, 5), "weave", 35122, inflate=.22):
        for face in s.sides:
            face.hline(0, face.w - 1, 4, "A2"), face.hline(0, face.w - 1, 5, "A3")
            face.hline(0, face.w - 1, 6, "P1")
        s.bottom.fill("P0")
    front, back, _ = over_panels(g, "dalmatic", 8, "P", "weave", 35123, top=10.2, width=10, sides=False)
    for face in (front, back):
        clavi(face, (2, 7), 0, 6)
        face.hline(2, 7, 5, "A2")
        face.vline(4, 1, 6, "P1")
        for x in range(10):
            face.set(x, 7, "A3" if x % 2 == 0 else "A1")                   # fringed hem
    for i, x in enumerate((-2.2, 2.2)):
        cord_end(g, f"back_cord_{i}", (x, .4, 2.7), 7, "A", 2, 35124 + i, knots=(3,), tassel="M3")
