"""Magnate's Floor Houppelande: a floor-length pleated gown belted high, with vast funnel sleeves and a standing fur collar."""
from kit import body, collar, sleeves
from kit_male import fur, sleeve_shapes
from paint import solid

META = {
    "name": "Magnate's Floor Houppelande",
    "gender": "male",
    "description": "A great man's floor-length houppelande in deep pleats, belted high, with vast funnel sleeves lined in accent and a fur collar.",
    "tags": ["fancy", "robe"],
    "locked_to": "b62_houppelande_train_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 6201)
    for face in b.sides:
        for x in range(0, face.w, 2):
            face.vline(x, 6, 11, "P1")                                   # pleats below the belt
    sleeves(g, "P", "velvet", 6202, rows=(0, 10))
    for s in sleeve_shapes(g, "funnel_sleeve", "P", 1.0, (6, 9, 6), "velvet", 6203, inflate=.2):
        for face in s.sides:
            for x in range(0, face.w, 2):
                face.vline(x, 2, 8, "P1")
            face.hline(0, face.w - 1, 8, "A2")
        s.bottom.fill("A2")
    fur(collar(g, "fur_collar", "S", "plain", base=3, height=2, y=-1.2, inflate=.1), "S", 6205, 3)
    high = g.piece("high_belt", "TORSO", (-4.6, 5.6, -2.6), (9, 1, 5), inflate=.08)
    solid(high, "L", "leather", 6206, 2, edge=False)
    high.front.set(4, 0, "M3")
