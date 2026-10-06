"""Fishwife's Striped Bodice: a sea-striped bodice, sleeves rolled high, a creel strap and a knitted shawl on the back."""
from kit import roll
from kit_female import bodice, chemise, girdle, lacing
from paint import fabric, line, solid

META = {
    "name": "Fishwife's Striped Bodice",
    "gender": "female",
    "description": "A sea-striped bodice over a rolled-up chemise, a creel strap, a gutting knife and a knitted shoulder shawl.",
    "tags": ["sea", "casual"],
}


def build(g):
    chemise(g, "S", 3, "weave", 11301, neckline="scoop", sleeve_rows=(0, 3))
    roll(g, "S", 1.0, base=3)
    b = bodice(g, "P", "weave", 11302, rows=(2, 9), neckline="square", edge="P3")
    for face in b.sides:
        for y in range(3, 10, 2):
            for x in range(face.w):
                if face.get(x, y):
                    face.set(x, y, "S3")                             # sea stripes
    lacing(b.front, 3, 3, 8, "ladder", lace="L3", under="P0", eyelet=None)
    line(b.front, 7, 0, 0, 9, "L2")                                  # creel strap
    line(b.back, 0, 0, 7, 9, "L2")
    b.top.vline(6, 0, 3, "L2")
    girdle(g, "girdle", 8.0, role="L", height=1)
    knife = g.piece("knife_sheath", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(2.6, 6.6, -2.95), rotation=(0, 0, -12))
    solid(knife, "L", "leather", 11303, 1)
    knife.strip.hline(0, knife.strip.w - 1, 0, "M3")
    shawl = g.piece("shawl", "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, -.2, 2.3), rotation=(8, 0, 0))
    point = g.piece("shawl_point", "TORSO", (-2.5, 0, 0), (5, 3, 1), pivot=(0, 2.7, 2.7), rotation=(8, 0, 0))
    for box in (shawl, point):
        solid(box, "S", "knit", 11304, 2)
    for x in range(1, 9, 2):
        shawl.back.set(x, 2, "S1")
    point.back.hline(0, 4, 2, "S1"), point.back.set(2, 2, "A2")
