"""Cook's Pinned-Hem Skirt: a work skirt with its hem turned up and pinned clear of the hearth ash, over stout shoes."""
from kit_female import shoes, skirt, stockings_row

META = {
    "name": "Cook's Pinned-Hem Skirt",
    "gender": "female",
    "description": "A work skirt with the hem turned up and pinned clear of the hearth ash, grey stockings and stout shoes.",
    "tags": ["work", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 13911, top=9.8, length=10)
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 3, "S3")
        face.hline(0, face.w - 1, face.h - 2, "S2")
        face.hline(0, face.w - 1, face.h - 1, "P1")
        for x in range(1, face.w, 4):
            face.set(x, face.h - 3, "M4")                            # pins holding the turn-up
    stockings_row(g, "M", 8, 9, base=2)
    shoes(g, "shoe", "L", 1)
