"""Pikeman's Tassets: steel thigh plates strapped over knee breeches, with wool stockings and shoes."""
from kit import SIDES, footwear, leg_ring, waistband
from kit_m04 import lames, leg_prop
from paint import fabric, strip_fabric, solid

META = {
    "name": "Pikeman's Tassets",
    "gender": "male",
    "description": "Broad steel tassets of riveted lames hung over the thighs, over full knee breeches with banded knees, "
                   "wool stockings and plain shoes.",
    "tags": ["armor", "martial", "sturdy"],
    "requires": ["martial", "rugged"],
}

S = 34020


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "P", "weave", S + (side == "left"), 2, 0, 6)
        fabric(leg.top, "P", "weave", S, 2)
        strip_fabric(leg, "S", "knit", S + 2, 3, 7, 9)
        leg.front.vline(1 if side == "right" else 2, 1, 5, "P1")          # breeches fold
    waistband(g, "P", "weave", S + 3)
    footwear(g, "shoe", top=10)
    for ring in leg_ring(g, "knee_band", 6.0, "A", base=2, size=(5, 1, 5)):
        ring.front.set(2, 0, "M3")
    for i, side in enumerate(SIDES):
        tasset = leg_prop(g, "tasset", side, (-2.5, 0, -1), (5, 5, 1), "M", 2, "smooth", S + 4 + i,
                          pivot=(0, -.4, -2.45), rotation=(-6, 0, 0))
        f = tasset.front
        f.hline(0, 4, 0, "L2"), f.set(2, 0, "M3")                          # the hanging strap and buckle
        lames(f, 1, 4, "M", 2, step=2, rivet="M4", rivet_step=3)
        f.set(0, 4, "M0"), f.set(4, 4, "M0")
    fauld = g.piece("waist_fauld", "TORSO", (-4.6, 9.6, -2.6), (9, 2, 5), inflate=.06)
    solid(fauld, "M", "smooth", S + 6, 2, edge=False)
    for face in fauld.sides:
        lames(face, 0, 1, "M", 2, step=2, rivet="M4", rivet_step=2)
