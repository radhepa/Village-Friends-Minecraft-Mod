"""Velvet Court Skirt: a floor-length velvet skirt with a brocade forepart, a pearl hem and a sweeping train."""
from kit_female import lozenges, shoes, skirt, trim
from paint import solid

META = {
    "name": "Velvet Court Skirt",
    "gender": "female",
    "description": "A floor-length velvet skirt with a brocade forepart, pearl-edged hem, a short train and pointed shoes.",
    "tags": ["fancy", "gown", "skirt", "long_skirt"],
    "locked_to": "tf010_velvet_court_bodice",
}


def build(g):
    s = skirt(g, "P", "velvet", 11011, top=9.6, length=12, back_length=14, side_length=12, flare=6)
    lozenges(s.front.front, 3, 1, 4, 10, "A2", "M3", "A1")
    s.front.front.vline(2, 1, 11, "M3"), s.front.front.vline(7, 1, 11, "M3")
    for f in s.faces:
        trim(f, f.h - 1, "pearls", "S4", "M4")
    train = g.piece("train", "TORSO", (-5, 13, 1), (10, 1, 4), pivot=(0, 9.6, 1.95), motion="flap_back")
    solid(train, "P", "velvet", 11012, 2)
    trim(train.back, 0, "pearls", "S4", "M4")
    shoes(g, "pointed", "K", 2)
