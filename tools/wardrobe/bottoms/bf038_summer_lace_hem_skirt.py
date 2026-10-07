"""Summer Lace-Hem Skirt: a light calf-length linen skirt with a drawn-thread lace border, bare ankles and sandals."""
from kit_female import shoes, skirt, trim

META = {
    "name": "Summer Lace-Hem Skirt",
    "gender": "female",
    "description": "A light calf-length linen skirt finished with drawn-thread lace, bare ankles and leather sandals.",
    "tags": ["relaxed", "simple", "skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 13811, base=4, top=9.8, length=9)
    for face in s.faces:
        trim(face, face.h - 3, "ricrac", "S2", "S3")
        face.hline(0, face.w - 1, face.h - 1, "S3")
    shoes(g, "sandal", "L", 2)
