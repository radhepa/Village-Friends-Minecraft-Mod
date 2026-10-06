"""Ink-Hemmed Skirt: a pale skirt with a deep dark hem band stitched with rows of script, over felt slippers."""
from kit_female import shoes, skirt

META = {
    "name": "Ink-Hemmed Skirt",
    "gender": "female",
    "description": "A pale linen-wool skirt with a deep dark hem band embroidered with lines of script, and felt slippers.",
    "tags": ["scholarly", "simple", "skirt", "long_skirt"],
}


def script(face):
    h = face.h
    for y in range(h - 4, h):
        face.hline(0, face.w - 1, y, "P1")
    for y in (h - 3, h - 2):
        for x in range(face.w):
            if (x * 7 + y * 3) % 5 in (0, 2):
                face.set(x, y, "S3")
    face.hline(0, face.w - 1, h - 4, "P0")


def build(g):
    s = skirt(g, "S", "weave", 12611, base=3, top=9.8, length=12)
    s.paint(script)
    shoes(g, "slipper", "P", 1)
