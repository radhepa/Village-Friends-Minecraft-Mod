"""Stained Apron Skirt: a dark work skirt under a leather-bound apron splashed with dye, and wooden pattens."""
from kit_female import shoes, skirt, splotch
from paint import solid

META = {
    "name": "Stained Apron Skirt",
    "gender": "female",
    "description": "A dark work skirt and a leather-bound linen apron splashed with dye, over raised wooden pattens.",
    "tags": ["work", "apron", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 10611, base=1, top=9.8, length=12)
    s.hem("P0")
    apron = g.piece("apron", "TORSO", (-3.5, 0, 0), (7, 9, 1), pivot=(0, 9.4, -3.05), motion="flap_front")
    solid(apron, "S", "weave", 10612, 3)
    f = apron.front
    f.vline(0, 0, 8, "L2"), f.vline(6, 0, 8, "L2"), f.hline(0, 6, 8, "L2"), f.hline(0, 6, 0, "L3")
    splotch(f, "A2", 10613, count=3, y0=2, y1=7)
    splotch(f, "A1", 10614, count=2, y0=3, y1=7, size=1)
    band = g.piece("waist_apron_tie", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.2, 0), inflate=.05)
    solid(band, "S", "weave", 10615, 3, edge=False)
    shoes(g, "patten", "L", 1)
