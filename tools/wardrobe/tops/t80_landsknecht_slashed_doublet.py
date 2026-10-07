"""Landsknecht Slashed Doublet: a mercenary's doublet slashed across the chest, with huge puffed and slashed sleeves."""
from kit import body, sleeves
from kit_male import sleeve_shapes
from paint import solid

META = {
    "name": "Landsknecht Slashed Doublet",
    "gender": "male",
    "description": "A swaggering mercenary's doublet slashed across the chest to show the lining, with huge puffed and slashed upper sleeves.",
    "tags": ["martial", "fancy", "whimsical"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 8001)
    for face in (b.front, b.back):
        for i in range(4):
            y = 2 + i * 2
            for x in range(1, 7):
                if (x + i) % 3 == 0:
                    face.set(x, y, "A3"), face.set(x, y + 1, "A2")       # diagonal chest slashes
    b.front.vline(4, 0, 11, "P0")
    sleeves(g, "P", "velvet", 8002, rows=(0, 10), cuff="A2")
    for s in sleeve_shapes(g, "upper_puff", "P", -1.6, (5, 5, 5), "velvet", 8003, inflate=.22):
        for face in s.sides:
            for x in range(face.w):
                if x % 2 == 0:
                    face.vline(x, 1, 3, "A3")                            # lining showing through the slashes
            face.hline(0, face.w - 1, 4, "P1")
    for s in sleeve_shapes(g, "elbow_puff", "A", 4.4, (5, 2, 5), "plain", 8005, base=3, inflate=.12):
        for face in s.sides:
            for x in range(1, face.w, 2):
                face.vline(x, 0, 1, "P1")
    hip = g.piece("sword_girdle", "TORSO", (-4.6, 10.0, -2.6), (9, 1, 5), inflate=.08)
    solid(hip, "L", "leather", 8007, 1, edge=False)
    hip.front.set(4, 0, "M3")
