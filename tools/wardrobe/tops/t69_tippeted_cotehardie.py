"""Tippeted Cotehardie: a side-laced cotehardie with long tippets streaming from the elbows and a leaf-dagged hem."""
from kit import body, sleeves
from kit_male import lacing, tippets
from paint import solid

META = {
    "name": "Tippeted Cotehardie",
    "gender": "male",
    "description": "A close cotehardie laced up the side, long accent tippets streaming from the elbows, a plaque belt and a leaf-dagged hem.",
    "tags": ["fancy", "slim"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 6901)
    b.front.clear(3, 0), b.front.clear(4, 0)
    for face in (b.front, b.back):
        face.vline(0, 1, 11, "P1"), face.vline(7, 1, 11, "P3")
    lacing(b.left, 1, 2, 9, "A3", "P0")
    sleeves(g, "P", "velvet", 6902, rows=(0, 10))
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 4, "A2")               # the tippet band
    tippets(g, "A", 8, y=2.4, base=2, seed=6903, key_end="A3")
    hip = g.piece("plaque_belt", "TORSO", (-4.6, 10.8, -2.6), (9, 1, 5), inflate=.08)
    solid(hip, "L", "leather", 6905, 1, edge=False)
    for face in hip.sides:
        for x in range(1, face.w, 2):
            face.set(x, 0, "M3")
    for name, z, motion, face_name in (("dagged_front", -2.85, "flap_front", "front"),
                                        ("dagged_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 11.6, z), motion=motion)
        solid(panel, "P", "velvet", 6906, 2)
        face = getattr(panel, face_name)
        for x in range(9):
            face.set(x, 2, "P1" if x % 3 == 1 else "A2")                 # leaf-shaped dags
            if x % 3 == 1:
                face.set(x, 1, "A2")
