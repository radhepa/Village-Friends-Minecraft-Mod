"""Two-Tone Panelled Skirt: a skirt with a broad centre panel in one color between side gores in another, the seams piped."""
from kit_female import shoes, skirt
from paint import fabric

META = {
    "name": "Two-Tone Panelled Skirt",
    "gender": "female",
    "description": "A long skirt with a broad centre panel in one color set between side gores in another, the seams piped in a bright cord and one narrow band across the hem.",
    "tags": ["casual", "tailored", "skirt", "long_skirt"],
}


def panel(face, seed):
    w, h = face.w, face.h
    fabric(face, "S", "weave", seed, 2, 0, 0, 2, h)
    fabric(face, "S", "weave", seed, 2, w - 2, 0, 2, h)
    face.vline(2, 0, h - 1, "A2"), face.vline(w - 3, 0, h - 1, "A2")       # piped seams
    face.vline(3, 2, h - 2, "P3"), face.vline(w - 4, 2, h - 2, "P1")
    face.vline(w // 2, 3, h - 3, "P1")
    face.hline(0, w - 1, h - 2, "A2")                                    # the narrow band across the hem
    face.hline(0, w - 1, h - 1, "P1")
    face.hline(0, 1, h - 1, "S1"), face.hline(w - 2, w - 1, h - 1, "S1")


def build(g):
    s = skirt(g, "P", "weave", 60580, top=9.8, length=11, flare=6, folds=False, gather=False)
    for face in s.wide_faces:
        panel(face, 60581)
    for box in (s.right, s.left):
        for face in box.faces:
            fabric(face, "S", "weave", 60582, 2)
        for face in box.sides:
            face.hline(0, face.w - 1, face.h - 2, "A2")
            face.hline(0, face.w - 1, face.h - 1, "S1")
            face.hline(0, face.w - 1, 0, "S3")
    shoes(g, "turnshoe", "L", 2)
