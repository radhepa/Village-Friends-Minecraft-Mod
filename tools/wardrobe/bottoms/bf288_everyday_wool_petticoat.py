"""Everyday Wool Petticoat: a mid-calf wool petticoat with a braid-bound hem, tied shut at the left hip, over ribbed stockings."""
from kit_female import hose, shoes, skirt
from kit_f10 import cord
from paint import solid

META = {
    "name": "Everyday Wool Petticoat",
    "gender": "female",
    "description": "A mid-calf wool petticoat bound at the hem with woven braid and tied shut at the left hip, over ribbed knitted stockings.",
    "tags": ["casual", "simple", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 60100, top=9.8, length=9, flare=6)
    s.band(2, "line", "P1", from_bottom=True)
    s.band(1, "braid", "A2", "A3", from_bottom=True)
    slit = s.left.left
    slit.vline(2, 1, 4, "P0"), slit.vline(3, 1, 4, "P3")              # the placket the tie closes
    hose(g, "S", rows=(7, 11), base=3, texture="rib", seam=False)
    shoes(g, "turnshoe", "L", 2)
    knot = g.piece("waist_tie_knot", "TORSO", (-.5, -.5, -1), (1, 1, 2), pivot=(5.55, 10.2, 0))
    solid(knot, "A", "plain", 60101, 2, edge=False)
    cord(g, "waist_tie_end_front", (5.75, 10.6, -.6), 4, role="A", base=2, end="A4", rotation=(0, 0, -9))
    cord(g, "waist_tie_end_back", (5.75, 10.6, .6), 3, role="A", base=3, end="A4", rotation=(0, 0, -7))
