"""Slit-Front Trailing Skirt: a velvet skirt opening at the front over a bright underskirt, trailing a short train behind."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Slit-Front Trailing Skirt",
    "gender": "female",
    "description": "A velvet skirt split at the front over a bright underskirt, trailing a short train, with long-toed poulaines.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "velvet", 15211, top=9.8, length=12, back_length=13)
    f = s.front.front
    for y in range(5, 12):
        half = (y - 5) // 3
        for x in range(4 - half, 6 + half):
            f.set(x, y, "A2" if (x + y) % 5 else "A1")
        f.set(3 - half, y, "M3"), f.set(6 + half, y, "M3")
    train = g.piece("train", "TORSO", (-3, 12, .4), (6, 1, 4), pivot=(0, 9.8, 1.95), motion="flap_back")
    solid(train, "P", "velvet", 15212, 2)
    train.back.fill("A2")
    shoes(g, "pointed", "K", 2)
