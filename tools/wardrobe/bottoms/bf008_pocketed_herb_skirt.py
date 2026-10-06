"""Pocketed Herb Skirt: a long skirt sprigged with embroidery at the hem, with tie-on pockets at both hips."""
from kit_female import motif, scatter, shoes, skirt
from paint import solid

META = {
    "name": "Pocketed Herb Skirt",
    "gender": "female",
    "description": "A long wool skirt sprigged with embroidered herbs at the hem, tie-on linen pockets and soft ankle boots.",
    "tags": ["casual", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10811, top=9.8, length=12)
    for f in s.wide_faces:
        scatter(f, "sprig", "A2", "A3", step=(4, 4), y0=7, y1=10, c="P3")
    s.hem("P1")
    for side, x in (("right", -5.65), ("left", 5.65)):
        pocket = g.piece(f"waist_pocket_{side}", "TORSO", (-.5, 0, -1.5), (1, 3, 3), pivot=(x, 9.8, -.6))
        solid(pocket, "S", "weave", 10812, 3)
        face = pocket.right if side == "right" else pocket.left
        face.hline(0, 2, 0, "S2")
        motif(face, 0, 0, "flower", a="A2", b="A3")
    shoes(g, "ankle", "L", 2)
