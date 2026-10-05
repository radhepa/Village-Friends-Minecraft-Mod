"""Student's Open Gown: a long open academic gown with bell sleeves over a plain tunic."""
from kit import body, neckline, sleeves
from paint import solid

META = {
    "name": "Student's Open Gown",
    "description": "A long, open scholar's gown with wide bell sleeves and an accent-faced collar over a tunic.",
    "tags": ["scholarly", "robe"],
}


def build(g):
    b = body(g, "S", "weave", 3001, base=3)
    neckline(b.front, "round", "S", base=3)
    gown = body(g, "P", "velvet", 3002, layer="jacket")
    gf = gown.front
    for y in range(12):
        for x in (2, 3, 4, 5):
            gf.clear(x, y)
        gf.set(1, y, "A2"), gf.set(6, y, "A2")
    gown.back.vline(3, 1, 11, "P1"), gown.back.vline(4, 1, 11, "P3")
    sleeves(g, "P", "velvet", 3003, rows=(0, 5))
    sleeves(g, "S", "weave", 3004, base=3, rows=(6, 10), cuff="S2")
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        bell = g.piece(f"{side}_bell_sleeve", bone, (ox - .8, 2.4, -2.8), (5, 5, 5), inflate=.15)
        solid(bell, "P", "velvet", 3005, 2)
        for face in bell.sides:
            face.hline(0, face.w - 1, 4, "A2")
        bell.bottom.fill("A1")
    collar = g.piece("collar", "TORSO", (-4.5, -.7, -2.6), (9, 1, 5), inflate=.05)
    solid(collar, "A", "plain", 3006, 2, edge=False)
    for name, x, w in (("gown_front_right", -4.5, 3), ("gown_front_left", 1.5, 3)):
        panel = g.piece(name, "TORSO", (0, 0, 0), (w, 7, 1), pivot=(x, 11.2, -2.85), motion="flap_front")
        solid(panel, "P", "velvet", 3007, 2)
        panel.front.vline(2 if x < 0 else 0, 0, 6, "A2")
    back = g.piece("gown_back", "TORSO", (-4.5, 0, 0), (9, 7, 1), pivot=(0, 11.2, 1.85), motion="flap_back")
    solid(back, "P", "velvet", 3008, 2)
    back.back.vline(4, 0, 6, "P1")
