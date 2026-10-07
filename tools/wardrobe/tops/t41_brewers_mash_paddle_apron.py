"""Brewer's Mash-Paddle Apron: a knee-length linen apron with a wet hem, hop cones on the tie and a mash paddle on the back."""
from kit import belt, body, neckline, sleeves
from kit_male import blk
from paint import fabric, solid

META = {
    "name": "Brewer's Mash-Paddle Apron",
    "gender": "male",
    "description": "An alewright's knee-length linen apron with a wort-darkened hem, hop cones tied at the waist and a mash paddle on the back.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 4101)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 4102, rows=(0, 10), cuff="P1")
    jacket = g.part("jacket")
    fabric(jacket.front, "S", "weave", 4103, 3, 0, 5, 8, 7)
    jacket.front.hline(0, 7, 5, "S4")
    belt(g, "apron_tie", 8.6, role="S", base=2, height=1, buckle=None)
    skirt = g.piece("apron_skirt", "TORSO", (-4, 0, 0), (8, 8, 1), pivot=(0, 11.0, -2.85), motion="flap_front")
    solid(skirt, "S", "weave", 4104, 3)
    skirt.front.vline(0, 0, 7, "S2"), skirt.front.vline(7, 0, 7, "S2")
    skirt.front.hline(0, 7, 6, "S2"), skirt.front.hline(0, 7, 7, "S1")      # wort-soaked hem
    for i, (x, y) in enumerate(((-2.8, 9.4), (-2.0, 9.6), (-2.4, 10.4))):
        cone = blk(g, f"hop_cone_{i}", (x, y, -2.8), (1, 1, 1), "A", 2 + (i == 1), "plain", 4105 + i, edge=False)
        cone.top.fill("A3")
    # The mash paddle, slung diagonally across the back: a long shaft and a slotted blade.
    shaft = g.piece("paddle_shaft", "TORSO", (-.5, 0, -.5), (1, 8, 1), pivot=(2.8, -1.6, 2.9), rotation=(0, 0, 28))
    solid(shaft, "L", "plain", 4108, 3)
    blade = g.piece("paddle_blade", "TORSO", (-1.5, 8, -.5), (3, 4, 1), pivot=(2.8, -1.6, 2.9), rotation=(0, 0, 28))
    solid(blade, "L", "plain", 4109, 4)
    for face in (blade.back, blade.front):
        face.vline(1, 1, 2, "L2")
