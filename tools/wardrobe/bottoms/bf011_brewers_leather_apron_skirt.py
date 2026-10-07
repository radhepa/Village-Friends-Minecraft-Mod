"""Brewer's Leather Apron Skirt: an undyed wool skirt under a heavy riveted leather apron, with dark stockings."""
from kit_female import shoes, skirt, stockings_row
from paint import solid

META = {
    "name": "Brewer's Leather Apron Skirt",
    "gender": "female",
    "description": "An undyed wool skirt under a heavy riveted leather apron for the mash tun, dark stockings and turnshoes.",
    "tags": ["work", "apron", "skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 11111, base=2, top=9.8, length=11)
    s.hem("S1")
    apron = g.piece("apron", "TORSO", (-4, 0, 0), (8, 9, 1), pivot=(0, 9.4, -3.05), motion="flap_front")
    solid(apron, "L", "leather", 11112, 2)
    f = apron.front
    f.hline(0, 7, 0, "L3"), f.set(0, 0, "M3"), f.set(7, 0, "M3")
    f.vline(0, 1, 8, "L1"), f.vline(7, 1, 8, "L1"), f.hline(0, 7, 8, "L1")
    f.set(2, 5, "L1"), f.set(3, 5, "L1"), f.set(5, 3, "L3")           # scuffs from the mash tun
    tie = g.piece("waist_apron_tie", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.2, 0), inflate=.05)
    solid(tie, "L", "leather", 11113, 1, edge=False)
    stockings_row(g, "P", 9, base=1)
    shoes(g, "turnshoe", "L", 1)
