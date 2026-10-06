"""Traveller's Hooded Cloak: a long wool cloak with its hood thrown back and a brooch at the throat, over a plain kirtle."""
from kit import body, sleeves
from kit_female import brooch, cloak, hood_down, mantle, neck
from paint import fabric

META = {
    "name": "Traveller's Hooded Cloak",
    "gender": "female",
    "description": "A long hooded wool cloak over a plain kirtle, the hood thrown back and a round brooch at the throat.",
    "tags": ["rugged", "casual"],
}


def build(g):
    b = body(g, "S", "weave", 13301, base=2)
    neck(b.front, "round", "S", 2)
    sleeves(g, "S", "weave", 13302, base=2, rows=(0, 11))
    j = g.part("jacket")
    for face in (j.front,):
        fabric(face, "P", "weave", 13303, 1, 0, 0, 2, 12)
        fabric(face, "P", "weave", 13303, 1, 6, 0, 2, 12)
        face.vline(1, 0, 11, "P2"), face.vline(6, 0, 11, "P2")
    shoulders = mantle(g, "cloak_shoulders", "P", "weave", 13304, 1, height=4, width=17, depth=6, y=-.7)
    for face in shoulders.sides:
        face.hline(0, face.w - 1, 3, "P0")
    shoulders.front.vline(8, 0, 3, "P0")
    upper, tail = cloak(g, "cloak", "P", "weave", 13305, base=1, width=10, length=11, tail=9, z=2.75)
    for face in (upper, tail):
        face.vline(2, 0, face.h - 1, "P0"), face.vline(7, 0, face.h - 1, "P2")
    tail.hline(0, 9, 8, "P0")
    hood_down(g, "hood", "P", "weave", 13306, 1, lining="S3")
    brooch(g, "brooch", (0, .4, -3.2), size=(2, 2, 1), gem="A2")
