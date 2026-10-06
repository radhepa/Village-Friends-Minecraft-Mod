"""Abbess's Habit: a white habit under a dark open mantle, white wimple and black veil, a pectoral cross and the abbey keys."""
from kit import body, sleeves
from kit_female import bells, cloak, girdle, hanging
from paint import fabric, solid

META = {
    "name": "Abbess's Habit",
    "gender": "female",
    "description": "A white habit under a long dark mantle, wimple and veil, a gilt pectoral cross and the abbey's keys.",
    "tags": ["holy", "robe", "fancy"],
    "locked_to": "bf027_abbess_habit_skirt",
    "covers_waist": True,
}


def build(g):
    body(g, "S", "weave", 12701, base=3)
    j = g.part("jacket")
    for face in (j.front,):
        fabric(face, "P", "weave", 12702, 1, 0, 0, 2, 12)
        fabric(face, "P", "weave", 12702, 1, 6, 0, 2, 12)
        face.vline(1, 0, 11, "P2"), face.vline(6, 0, 11, "P2")
    for face in (j.right, j.left, j.back):
        fabric(face, "P", "weave", 12703, 1)
    fabric(j.top, "P", "weave", 12703, 2)
    sleeves(g, "S", "weave", 12704, base=3, rows=(0, 11))
    bells(g, "P", "weave", 12705, base=1, y=3.5, h=6, size=6, lining="S3")
    cloak(g, "mantle", "P", "weave", 12706, base=1, width=10, length=11, tail=10, z=2.6)
    wimple = g.piece("wimple", "TORSO", (-4.5, -1.4, -2.6), (9, 2, 5), inflate=.12)
    solid(wimple, "S", "plain", 12707, 4, edge=False)
    veil = g.piece("veil", "TORSO", (-4, 0, 0), (8, 4, 1), pivot=(0, -1.0, 3.7), rotation=(4, 0, 0))
    solid(veil, "K", "plain", 12708, 2)
    cross = g.piece("pectoral_cross", "TORSO", (-1.5, 0, -.5), (3, 4, 1), pivot=(0, 2.0, -2.75))
    solid(cross, "M", "smooth", 12709, 3)
    face = cross.front
    face.set(0, 0, "S3"), face.set(2, 0, "S3"), face.set(0, 2, "S3"), face.set(2, 2, "S3"), face.set(0, 3, "S3"), face.set(2, 3, "S3")
    face.set(1, 1, "A2")
    girdle(g, "girdle", 8.0, role="S", base=3, height=1, buckle=None, texture="plain")
    hanging(g, "key_chain", 2.6, 4, role="M", top=8.8)
    keys = g.piece("abbey_keys", "TORSO", (-1, 4, -.1), (2, 3, 1), pivot=(2.6, 8.8, -3.25), motion="flap_front")
    solid(keys, "M", "smooth", 12710, 3)
    keys.front.set(0, 1, "M1"), keys.front.set(1, 2, "M4")
