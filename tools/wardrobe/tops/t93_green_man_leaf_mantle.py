"""Green Man's Leaf Mantle: a May-Day guise of overlapping leaves over the shoulders and back, an ivy garland and leafy cuffs."""
from kit import body, sleeves
from kit_male import back_drape, sleeve_shapes, shoulder_cape
from paint import line

META = {
    "name": "Green Man's Leaf Mantle",
    "gender": "male",
    "description": "A May-Day guise of overlapping leaves layered over the shoulders and down the back, a berried ivy garland and leafy cuffs.",
    "tags": ["whimsical", "rugged"],
    "locked_to": "b93_green_man_leaf_skirt",
    "covers_waist": True,
}


def leaves(face, offset=0):
    """Overlapping leaf scales: a lit tip, a dark midrib, a shaded base on each 3x3 leaf."""
    for y in range(face.h):
        for x in range(face.w):
            row = y // 3
            lx, ly = (x + face.x0 + offset + row * 2) % 3, y % 3
            key = "P3" if ly == 2 and lx == 1 else "P1" if lx == 1 else "P2"
            face.set(x, y, key)


def build(g):
    b = body(g, "L", "weave", 9301)
    sleeves(g, "L", "weave", 9302, rows=(0, 10))
    mantle = shoulder_cape(g, "leaf_mantle", "P", "plain", 9303, length=5, width=12, depth=6)
    for face in mantle.faces:
        leaves(face)
    back = back_drape(g, "leaf_drape", "P", 10, "plain", 9304, width=10, y=3.0, z=3.2, tilt=4)
    for face in back.faces:
        leaves(face, 1)
    for s in sleeve_shapes(g, "leaf_cuff", "P", 6.6, (5, 3, 5), "plain", 9305, inflate=.14):
        for face in s.faces:
            leaves(face, 2)
    jacket = g.part("jacket")
    line(jacket.front, 0, 5, 7, 8, "P2")
    for x in range(0, 8, 2):
        jacket.front.set(x, 5 + x * 3 // 7, "A3")                         # ivy berries on the garland
