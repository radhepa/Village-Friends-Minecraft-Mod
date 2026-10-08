"""Plain Underdress Skirt: the long pale skirt of an underdress, pin-tucked below the waist, a narrow rolled hem and cloth slippers."""
from kit_female import shoes, skirt
from paint import k

META = {
    "name": "Plain Underdress Skirt",
    "gender": "female",
    "description": "The long pale linen skirt of an underdress, fine pin-tucks fanning below the waist, a narrow rolled hem and soft cloth slippers.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def pintucks(face):
    for x in range(face.w):
        if x % 2 == 0:
            for y in range(1, 5):
                face.set(x, y, "S4")                                   # each tuck catches the light
            face.set(x, 5, "S3")
        else:
            face.vline(x, 1, 4, "S2")
    face.hline(0, face.w - 1, face.h - 1, "S2")
    for x in range(face.w):
        face.set(x, face.h - 2, k("S", 4 if x % 2 else 3))             # the rolled hem's little ridge


def build(g):
    s = skirt(g, "S", "weave", 60340, base=3, top=9.8, length=12, flare=5, gather=False)
    for face in s.wide_faces:
        pintucks(face)
    for box in (s.right, s.left):
        for face in (box.right, box.left, box.front, box.back):
            face.hline(0, face.w - 1, face.h - 1, "S2")
    shoes(g, "slipper", "A", 2)
