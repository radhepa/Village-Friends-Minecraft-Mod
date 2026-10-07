"""Gored Panel Skirt: a skirt cut from alternating colored gores, edged with a ribbon band, and pointed shoes."""
from kit_female import shoes, skirt, stripes, trim

META = {
    "name": "Gored Panel Skirt",
    "gender": "female",
    "description": "A tailor's showpiece skirt of alternating gores, a woven ribbon above the hem and pointed shoes.",
    "tags": ["tailored", "fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 12411, top=9.8, length=12, folds=False)
    for face in s.wide_faces:
        stripes(face, ["P2", "P2", "P2", "S3", "S3"], 1, vertical=True, y0=1, h=face.h - 1, offset=1)
        for x in range(face.w):
            if face.get(x, 2) == "S3":
                face.set(x, 2, "S2")
    for face in s.faces:
        trim(face, face.h - 3, "diamond", "A2", "M3")
    s.hem("P1")
    shoes(g, "pointed", "L", 2)
