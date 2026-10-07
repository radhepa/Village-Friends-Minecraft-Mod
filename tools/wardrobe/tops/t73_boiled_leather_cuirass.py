"""Boiled-Leather Cuirass: a hardened, tooled leather breastplate buckled at the sides, cupped rerebraces and a strip fauld."""
from kit import body, sleeves
from kit_male import arm_blk
from paint import fabric, solid

META = {
    "name": "Boiled-Leather Cuirass",
    "gender": "male",
    "description": "A cuir-bouilli breastplate tooled with a border and buckled at the sides, cupped leather rerebraces and a fauld of strips.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}


def build(g):
    body(g, "P", "quilt", 7301)
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        fabric(face, "L", "smooth", 7302, 2, 0, 1, 8, 10)
        face.hline(0, 7, 1, "L4"), face.hline(0, 7, 10, "L1")
        face.vline(0, 1, 10, "L3"), face.vline(7, 1, 10, "L1")
        face.vline(1, 2, 9, "L3"), face.vline(6, 2, 9, "L1")             # tooled border
    jacket.front.vline(3, 3, 9, "L3"), jacket.front.vline(4, 3, 9, "L1")   # the ridge
    for face in (jacket.right, jacket.left):
        for y in (3, 7):
            face.hline(0, face.w - 1, y, "L2")
            face.set(1, y, "M3")                                         # side buckles
    jacket.top.vline(1, 0, 3, "L2"), jacket.top.vline(6, 0, 3, "L2")
    sleeves(g, "P", "quilt", 7303, rows=(0, 10), cuff="P1")
    for i, side in enumerate(("right", "left")):
        cup = arm_blk(g, f"{side}_rerebrace", side, -1.2, (5, 4, 5), "L", 2, "smooth", 7304 + i, inflate=.12)
        for face in cup.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 3, "L1")
            face.set(2, 1, "M3")
    for name, z, motion, face_name in (("fauld_front", -2.85, "flap_front", "front"),
                                        ("fauld_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 4, 1), pivot=(0, 10.8, z), motion=motion)
        solid(panel, "L", "smooth", 7306, 2)
        face = getattr(panel, face_name)
        for x in range(0, 9, 3):
            face.vline(x, 0, 3, "L0")                                    # separate strips
        face.hline(0, 8, 0, "L3")
        for x in range(1, 9, 3):
            face.set(x, 2, "M3")
