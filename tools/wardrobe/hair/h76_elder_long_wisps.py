"""Elder's Long Wisps: a high bald crown, the hair that is left grown long and thin, falling in
separate wisps from the sides and back to the shoulders."""
from anime import cel_face
from anime_male import SIDES, taper
from paint import hair_face

META = {"name": "Elder's Long Wisps", "gender": "male",
        "description": "A high bald crown with long thin wisps falling from the sides and back to the shoulders."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face, top in ((head.right, 3), (head.left, 3), (head.back, 2)):
        hair_face(face, 7601 + face.x0, 2, rows=range(top, 8))
    for face, top in ((hat.right, 3), (hat.left, 3), (hat.back, 2)):
        sub = type(face)(face.layer, face.x0, face.y0 + top, face.w, 8 - top, face.name)
        cel_face(sub, 7602 + face.x0, 2, None)
    # Wisps in front of the ears, outside the cheeks.
    for side, sign in SIDES:
        taper(g, f"{side}_front", (4.45 * sign, -5.4, -3.2), (-4, 0, -3 * sign), ((1, 6, 1), (1, 2, 1)), seed=7610 + (sign > 0), ring=1)
        for j, (z, length, tilt) in enumerate(((-1.4, 5, 5), (.8, 5, 8), (3.0, 8, 4))):
            taper(g, f"{side}_wisp_{j}", (4.5 * sign, -5.6, z), (j * 4, 0, -tilt * sign), ((1, length, 1), (1, 2, 1)),
                  seed=7620 + j * 3 + (sign > 0) * 11, ring=1)
    for i, (x, length, rz) in enumerate(((-3.2, 8, 6), (-1.6, 9, 3), (0, 8, 0), (1.6, 9, -3), (3.2, 8, -6))):
        taper(g, f"back_{i}", (x, -6.2, 4.5), (6, 0, rz), ((1, length, 1), (1, 2, 1)), seed=7650 + i * 3, ring=1, motion="sway")
