"""Star-Hem Skirt: a deep night-colored skirt scattered with stars toward a silver moon-wave border, and soft pointed boots."""
from kit_female import scatter, shoes, skirt, trim

META = {
    "name": "Star-Hem Skirt",
    "gender": "female",
    "description": "A night-colored skirt scattered with stars that thicken toward a silver wave border, over soft pointed boots.",
    "tags": ["whimsical", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "velvet", 12911, base=1, top=9.8, length=12)
    for face in s.wide_faces:
        scatter(face, "star", "M3", "M4", step=(5, 4), y0=5, y1=9)
        face.set(2, 3, "M3"), face.set(7, 2, "M4")
    for face in s.faces:
        trim(face, face.h - 2, "wave", "M3", "M4")
    shoes(g, "pointed", "P", 1)
