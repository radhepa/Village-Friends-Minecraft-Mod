"""Brewster's Hop Bodice: a kirtle bodice embroidered with a climbing hop vine, sleeves rolled and a mash ladle at the hip."""
from kit import roll
from kit_female import bodice, chemise, girdle, hanging, motif
from paint import solid

META = {
    "name": "Brewster's Hop Bodice",
    "gender": "female",
    "description": "A brewster's bodice with a hop vine climbing the front, rolled chemise sleeves and a wooden mash ladle.",
    "tags": ["work", "casual"],
}


def build(g):
    chemise(g, "S", 3, "weave", 11101, neckline="round", sleeve_rows=(0, 5))
    roll(g, "S", 2.8, base=3)
    b = bodice(g, "P", "weave", 11102, rows=(1, 9), neckline="scoop", edge="P3")
    for y in range(2, 10):
        b.front.set(3 if y % 2 else 4, y, "P0")                     # the twining hop bine
    for x, y in ((1, 3), (5, 5), (1, 7)):
        motif(b.front, x, y, "diamond", a="A2", b="A3")             # hop cones
    b.front.set(2, 4, "P3"), b.front.set(5, 3, "P3"), b.front.set(5, 8, "P3")   # leaves
    for y in range(1, 9):
        b.back.set(3 if y % 2 else 4, y, "P0")
    motif(b.back, 4, 3, "diamond", a="A2", b="A3")
    girdle(g, "girdle", 7.8, role="L", height=1)
    handle = hanging(g, "ladle_handle", 2.6, 7, role="L", base=3, top=8.8, texture="smooth")
    handle.front.set(0, 0, "L4")
    bowl = g.piece("ladle_bowl", "TORSO", (-1, 7, -.6), (2, 2, 2), pivot=(2.6, 8.8, -3.25), motion="flap_front")
    solid(bowl, "L", "smooth", 11103, 3)
    bowl.top.fill("L1")
