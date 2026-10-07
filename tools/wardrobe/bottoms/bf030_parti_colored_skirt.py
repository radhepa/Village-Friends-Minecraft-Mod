"""Parti-Colored Skirt: a mi-parti skirt, one half in each color, with a dagged hem and little bells on the points."""
from kit_female import shoes, skirt

META = {
    "name": "Parti-Colored Skirt",
    "gender": "female",
    "description": "A minstrel's mi-parti skirt, split down the middle into two colors, with a dagged hem hung with bells.",
    "tags": ["whimsical", "skirt"],
}


def parti(face, flip):
    for y in range(face.h):
        for x in range(face.w):
            left = x < face.w // 2
            role = "S" if left != flip else "P"
            base = 3 if role == "S" else 2
            face.set(x, y, f"{role}{base - (1 if (x + y) % 11 == 0 else 0)}")
    for x in range(face.w):
        face.set(x, face.h - 1, "K1" if x % 2 else face.get(x, face.h - 2))
        if x % 4 == 1:
            face.set(x, face.h - 2, "M3")


def build(g):
    s = skirt(g, "P", "weave", 13011, top=9.8, length=10, folds=False, gather=False)
    parti(s.front.front, False)
    parti(s.back.back, True)
    for box, role in ((s.right, "S"), (s.left, "P")):
        for face in box.sides:
            for y in range(face.h):
                face.hline(0, face.w - 1, y, f"{role}{3 if role == 'S' else 2}")
    shoes(g, "pointed", "K", 2)
    for side in ("right", "left"):
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, 15, 9, "S3" if side == "right" else "P2")
