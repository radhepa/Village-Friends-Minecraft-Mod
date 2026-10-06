"""Milkmaid's Puff Bodice: a ribbon-laced bodice, puffed chemise sleeves and a white kerchief crossed at the throat."""
from kit_female import bodice, chemise, lacing, puffs
from paint import fabric

META = {
    "name": "Milkmaid's Puff Bodice",
    "gender": "female",
    "description": "Ribbon-laced bodice over puffed short chemise sleeves, with a white fichu crossed and tucked in.",
    "tags": ["casual", "whimsical"],
}


def build(g):
    chemise(g, "S", 3, "weave", 10201, neckline="wide", sleeve_rows=(0, 3))
    puffs(g, "S", "weave", 10202, base=3, y=-2.4, h=4, band_key="A2")
    b = bodice(g, "P", "weave", 10203, rows=(4, 9), straps=False, point=True)
    lacing(b.front, 3, 5, 8, "ladder", lace="A3", under="S3", eyelet=None, edge="P1")
    b.front.hline(0, 7, 4, "P3")
    # The fichu: a white kerchief over the shoulders, crossed on the chest and tucked into the bodice.
    j = g.part("jacket")
    front = [(0, 0), (1, 0), (2, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
             (7, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (2, 3), (3, 3), (4, 3), (5, 3), (3, 4), (4, 4)]
    for x, y in front:
        j.front.set(x, y, "S4")
    for x, y in [(2, 1), (5, 1), (3, 2), (4, 3)]:
        j.front.set(x, y, "S3")                            # the crossing fold
    for y in range(6):
        for x in range(8):
            if abs(x - 3.5) <= 3.6 - y * .6:
                j.back.set(x, y, "S4" if y < 4 else "S3")
    for face in (j.right, j.left):
        face.hline(0, 3, 0, "S4"), face.hline(0, 3, 1, "S3")
    fabric(j.top, "S", "weave", 10204, 4)
