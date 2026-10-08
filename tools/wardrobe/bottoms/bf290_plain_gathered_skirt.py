"""Plain Gathered Skirt: a full skirt cartridge-gathered into a narrow buttoned waistband, falling in close ripples to a rolled hem."""
from kit_female import shoes, skirt, stockings_row
from paint import k

META = {
    "name": "Plain Gathered Skirt",
    "gender": "female",
    "description": "A full plain skirt cartridge-gathered into a narrow buttoned waistband, falling in close even ripples to a rolled hem.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def ripples(face):
    for y in range(face.h):
        for x in range(face.w):
            if y <= 1:
                key = k("P", 3 if (x + y) % 2 == 0 else 1)            # cartridge gathers under the band
            else:
                phase = x % 3
                key = k("P", 1 if phase == 0 else 3 if phase == 2 and 3 <= y < face.h - 2 else 2)
            face.set(x, y, key)
    face.hline(0, face.w - 1, face.h - 1, "P1")


def build(g):
    s = skirt(g, "P", "plain", 60180, top=9.8, length=11, back_length=12, flare=6, gather=False, folds=False)
    s.paint(ripples, sides=False)
    body = g.part("body")
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "P3")
        face.hline(0, face.w - 1, 10, "P2")
    body.front.set(5, 9, "M3")                                         # the waistband's one button
    stockings_row(g, "S", 9, 9, base=2)
    shoes(g, "turnshoe", "L", 2)
