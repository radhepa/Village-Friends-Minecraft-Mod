"""Linen Drawstring Skirt: a light linen skirt gathered on a cord through a casing at the hips, its knotted ends hanging in front, over clogs."""
from kit_f10 import panel_prop
from kit_female import shoes, skirt, stockings_row
from paint import solid

META = {
    "name": "Linen Drawstring Skirt",
    "gender": "female",
    "description": "A light linen skirt gathered on a cord run through a casing at the hips, the knotted ends hanging down the front, over wooden clogs.",
    "tags": ["casual", "relaxed", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 60420, base=3, top=9.8, length=10, flare=6, folds=False)
    for face in s.wide_faces:
        for x in range(1, face.w, 3):
            face.vline(x, 2, face.h - 2, "P2")                         # long soft creases in the linen
        face.hline(0, face.w - 1, face.h - 1, "P1")                    # a narrow rolled hem
    s.hem("P1")
    casing = g.piece("waist_casing", "TORSO", (-5.5, 9.3, -3.05), (11, 1, 6), inflate=.08)
    solid(casing, "P", "plain", 60421, 3, edge=False)
    for face in casing.sides:
        for x in range(face.w):
            face.set(x, 0, "P4" if x % 3 else "P2")
    casing.front.set(5, 0, "A2")                                       # where the cord comes out
    for i, (x, length) in enumerate(((-.5, 4), (.5, 3))):
        end = panel_prop(g, f"waist_cord_{i}", s, x, .55, (1, length, 1), role="A", base=2, texture="plain",
                         seed=60422)
        for face in end.sides:
            face.set(0, length - 1, "A1")
            face.set(0, length - 2, "A3")                              # the knot near each end
    stockings_row(g, "S", 8, 9, base=3)
    shoes(g, "clog", "L", 3)
