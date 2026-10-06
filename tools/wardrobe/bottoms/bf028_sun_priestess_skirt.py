"""Sun Priestess's Skirt: a floor-length temple skirt pleated in golden sunrays, a gilt hem and sandals with gold straps."""
from kit_female import shoes, skirt, trim
from paint import line

META = {
    "name": "Sun Priestess's Skirt",
    "gender": "female",
    "description": "A floor-length temple skirt with rays of gold spreading from the waist, a gilt hem and gold-strapped sandals.",
    "tags": ["holy", "robe", "fancy", "skirt", "long_skirt"],
    "locked_to": "tf028_sun_priestess_robe",
}


def rays(face):
    """Pleats fanning out from the waist like sunrays, alternating gold and accent."""
    for i, end in enumerate((0, 2, 4, 5, 7, 9)):
        start = 4 if end < 5 else 5
        line(face, start, 1, end, face.h - 3, "M3" if i % 2 else "A2")


def build(g):
    s = skirt(g, "S", "weave", 12811, base=3, top=9.8, length=12, folds=False)
    for face in s.wide_faces:
        rays(face)
    for face in s.faces:
        trim(face, face.h - 2, "triangles", "M3", "M4")
    shoes(g, "sandal", "M", 3)
