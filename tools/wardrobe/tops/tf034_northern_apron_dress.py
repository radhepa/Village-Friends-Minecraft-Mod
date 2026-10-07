"""Northern Apron Dress: an apron dress hung from two oval brooches with strings of beads, over a long-sleeved underdress."""
from kit import body, sleeves
from kit_female import over_flaps, trim
from paint import fabric, solid

META = {
    "name": "Northern Apron Dress",
    "gender": "female",
    "description": "A strapped apron dress pinned with two oval brooches and swags of glass beads, over a long underdress.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 13401, base=3)
    b.front.clear(3, 0), b.front.clear(4, 0)
    sleeves(g, "S", "weave", 13402, base=3, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        trim(arm.strip, 10, "zigzag", "A2", "P2")
    j = g.part("jacket")
    for face in (j.front, j.back):
        fabric(face, "P", "weave", 13403, 2, 0, 3, 8, 9)
        trim(face, 3, "checker", "A2", "S3")
        for x in (1, 6):
            face.vline(x, 0, 2, "P2")                                # shoulder straps
    for face in (j.right, j.left):
        fabric(face, "P", "weave", 13404, 2, 0, 4, 4, 8)
    for x in (1, 6):
        j.top.vline(x, 0, 3, "P2")
    for x, y in ((2, 4), (3, 5), (4, 5), (5, 4)):
        j.front.set(x, y, "A3" if x % 2 else "M3")                   # a swag of beads
    for x, y in ((2, 6), (3, 7), (4, 7), (5, 6)):
        j.front.set(x, y, "M4" if x % 2 else "A2")
    for name, x in (("brooch_right", -2.6), ("brooch_left", 2.6)):
        dome = g.piece(name, "TORSO", (-1, -1, -.5), (2, 3, 1), pivot=(x, 3.4, -2.6), inflate=.1)
        solid(dome, "M", "smooth", 13405, 3, edge=False)
        dome.front.set(0, 1, "M4"), dome.front.set(1, 1, "M2")
    f, bk = over_flaps(g, "apron_dress", 11, "P", "weave", 13406, width=8, top=9.0)
    for face in (f, bk):
        face.vline(0, 0, 10, "P1"), face.vline(7, 0, 10, "P1")
        trim(face, 9, "checker", "A2", "S3")
