"""Houppelande Skirt: the houppelande's deep-pleated floor-length skirt with a fur hem and a sweeping train."""
from kit_female import fur, pleats, shoes, skirt, sub
from paint import solid

META = {
    "name": "Houppelande Skirt",
    "gender": "female",
    "description": "The houppelande's floor-length skirt in deep organ pleats, a fur hem and a wide sweeping train.",
    "tags": ["fancy", "gown", "robe", "skirt", "long_skirt"],
    "locked_to": "tf053_houppelande_bodice",
}


def build(g):
    s = skirt(g, "P", "velvet", 15311, top=9.8, length=12, back_length=13, folds=False, flare=7)
    for face in s.wide_faces:
        pleats(face, "P", 2, 2, y0=1, lit=False)
    s.paint(lambda f: fur(sub(f, 0, f.h - 2, f.w, 2), "S", 15312 + f.x0, 3))
    train = g.piece("train", "TORSO", (-5, 12, 1), (10, 1, 5), pivot=(0, 9.8, 1.95), motion="flap_back")
    solid(train, "P", "velvet", 15313, 2)
    for x in range(0, 10, 2):
        train.top.vline(x, 0, 4, "P1")
    fur(train.back, "S", 15314, 3)
    shoes(g, "pointed", "K", 2)
