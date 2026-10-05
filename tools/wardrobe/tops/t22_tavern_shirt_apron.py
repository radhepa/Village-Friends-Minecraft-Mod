"""Tavern Shirt & Half-Apron: rolled sleeves held with garters, a half-apron tied at the waist, a towel on the shoulder."""
from kit import body, neckline, roll, sleeves
from paint import fabric, k, solid

META = {
    "name": "Tavern Shirt & Half-Apron",
    "description": "Sleeve garters, a long half-apron tied at the waist and a serving towel over one shoulder.",
    "tags": ["casual", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 2201)
    neckline(b.front, "v", "P")
    b.front.vline(4, 4, 10, "P1")
    for y in (5, 8):
        b.front.set(4, y, "S4")
    sleeves(g, "P", "weave", 2202, rows=(0, 6))
    roll(g, "P", 3.6, base=3)
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        garter = g.piece(f"{side}_garter", bone, (ox - .2, .6, -2.2), (4, 1, 4), inflate=.12)
        solid(garter, "A", "plain", 2203, 2, edge=False)
    band = g.piece("apron_band", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.06)
    solid(band, "S", "weave", 2204, 3, edge=False)
    apron = g.piece("apron", "TORSO", (-3.5, 0, 0), (7, 8, 1), pivot=(0, 10.2, -2.9), motion="flap_front")
    solid(apron, "S", "weave", 2205, 3)
    apron.front.vline(0, 0, 7, "S2"), apron.front.vline(6, 0, 7, "S2"), apron.front.hline(0, 6, 7, "S2")
    apron.front.hline(1, 3, 2, "S1"), apron.front.set(2, 3, "S2")   # a pocket
    towel = g.piece("shoulder_towel", "TORSO", (-1, 0, -3), (2, 1, 6), pivot=(3.4, -.4, 0), rotation=(0, 0, 8))
    solid(towel, "S", "weave", 2206, 4, edge=False)
    for name, z in (("towel_front", -3.15), ("towel_back", 2.35)):
        hang = g.piece(name, "TORSO", (-1, 0, 0), (2, 4, 1), pivot=(3.2, .2, z))
        solid(hang, "S", "weave", 2207, 4)
        hang.strip.hline(0, hang.strip.w - 1, 3, "A2")
