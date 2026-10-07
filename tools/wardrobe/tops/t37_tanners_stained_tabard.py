"""Tanner's Stained Tabard: a side-tied leather tabard over a shirt, long wet-leather gloves and a fleshing blade."""
from kit import body, flaps, neckline, sleeves
from kit_male import blk, flecks, sleeve_shapes
from paint import fabric

META = {
    "name": "Tanner's Stained Tabard",
    "gender": "male",
    "description": "A tanyard tabard of stained leather tied at the sides, elbow-length wet-leather gloves and a two-handled fleshing blade.",
    "tags": ["work", "rugged"],
}


def build(g):
    b = body(g, "S", "weave", 3701, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 3702, base=3, rows=(0, 4))
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        fabric(face, "L", "leather", 3703, 2)
        flecks(face, "L0", 3704, .06)
        face.hline(0, 7, 0, "L3")
        face.rect(1, 6, 2, 2, "L1"), face.rect(5, 3, 2, 2, "L1")   # tan-pit stains
    jacket.front.hline(2, 5, 0, None), jacket.front.hline(3, 4, 1, None)
    jacket.front.set(2, 1, "L0"), jacket.front.set(5, 1, "L0")
    fabric(jacket.top, "L", "leather", 3705, 3)
    jacket.top.hline(2, 5, 1, None), jacket.top.hline(2, 5, 2, None)
    for face in (jacket.right, jacket.left):
        for y in (4, 8):
            face.hline(1, 2, y, "L2")                              # side ties
    # Elbow-length gloves, dark with wet, flaring at the cuff.
    for side in ("right", "left"):
        glove = g.part(f"{side}_sleeve")
        fabric(glove.strip, "L", "leather", 3706, 1, 0, 5, glove.strip.w, 7)
        glove.strip.hline(0, glove.strip.w - 1, 8, "L2")
        glove.bottom.fill("L0")
    for cuff in sleeve_shapes(g, "glove_cuff", "L", 2.7, (5, 2, 5), "leather", 3707, base=2, inflate=.18):
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "L3")
    blade = blk(g, "fleshing_blade", (0, 9.8, -2.6), (5, 1, 1), "M", 3, "smooth", 3709, edge=False)
    for face in blade.sides:
        face.set(0, 0, "L3"), face.set(face.w - 1, 0, "L3")
    for face in flaps(g, "tabard", 3, "L", "leather", 3710, width=8, top=11.2):
        face.hline(0, 7, 2, "L1")
        flecks(face, "L0", 3711, .1)
