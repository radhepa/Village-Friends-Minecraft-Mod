"""Pearl-Scattered Silk Skirt: a sheened silk skirt sewn with scattered seed pearls and a scalloped gilt hem."""
from kit_female import shoes, skirt, trim

META = {
    "name": "Pearl-Scattered Silk Skirt",
    "gender": "female",
    "description": "A sheened silk skirt sewn with scattered seed pearls, a scalloped gilt hem and satin slippers.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "smooth", 15911, top=9.8, length=12)
    for face in s.faces:
        for y in range(2, face.h - 2):
            for x in range(face.w):
                if (x * 3 + y * 5 + face.x0) % 9 == 0:
                    face.set(x, y, "S4")
        trim(face, face.h - 2, "scallop", "M3", "M4")
    for face in s.wide_faces:
        for x in (1, 6):
            face.vline(x, 2, face.h - 4, "P3")                       # silk sheen
    shoes(g, "slipper", "S", 3)
