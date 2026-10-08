"""Carder's Lap-Cloth Skirt: a long wool skirt with a square leather lap-cloth tied over the front for carding
on the knee, wisps of fleece caught on it, and felt slippers."""
from kit_female import SKIRT_FRONT, shoes, skirt
from paint import fabric, solid

META = {
    "name": "Carder's Lap-Cloth Skirt",
    "gender": "female",
    "description": "A long wool skirt with a square leather lap-cloth tied over the front for carding on the knee, fleece wisps clinging to it, and felt slippers.",
    "tags": ["work", "simple", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51380, top=9.8, length=12, flare=5)
    s.band(1, "line", "P1", from_bottom=True)
    # The lap-cloth: a square of soft leather tied at the hips with thongs, riding the front panel.
    lap = g.piece("lap_cloth", "TORSO", (-4, .2, -1.1), (8, 7, 1), pivot=(0, 9.8, SKIRT_FRONT), motion="flap_front")
    solid(lap, "L", "leather", 51381, 3)
    face = lap.front
    face.hline(0, 7, 0, "L4")
    face.vline(0, 1, 6, "L2"), face.vline(7, 1, 6, "L2"), face.hline(0, 7, 6, "L1")
    for x, y in ((0, 0), (7, 0)):
        face.set(x, y, "L1")                                          # the tie holes
    for x, y in ((2, 2), (5, 4), (3, 5)):
        face.set(x, y, "S4"), face.set(x + 1, y, "S3")                # fleece wisps
    fabric(lap.back, "L", "leather", 51382, 2)
    for name, x in (("lap_tie_right", -4.6), ("lap_tie_left", 4.6)):
        tie = g.piece(name, "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, 10.2, SKIRT_FRONT - .6), motion="flap_front",
                      rotation=(0, 0, 10 if x < 0 else -10))
        solid(tie, "L", "plain", 51383, 2, edge=False)
    shoes(g, "slipper", "S", 1)
