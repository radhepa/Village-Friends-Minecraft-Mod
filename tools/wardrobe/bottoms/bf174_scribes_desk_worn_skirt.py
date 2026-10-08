"""Scribe's Desk-Worn Skirt: an ankle-length wool skirt with a stitched leather lap guard where the desk
edge rubs, worn shiny in the middle and spotted with ink, over soft leather slippers."""
from kit_f05 import lap_panel
from kit_female import shoes, skirt

META = {
    "name": "Scribe's Desk-Worn Skirt",
    "gender": "female",
    "description": "An ankle-length wool skirt with a stitched leather lap guard, rubbed shiny and spotted with ink, over soft slippers.",
    "tags": ["scholarly", "casual", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 55391, base=1, top=9.8, length=11, back_length=11, flare=5, folds=True, gather=True)
    s.band(1, "line", "P0", from_bottom=True)
    s.hem("P2")
    guard = lap_panel(g, 9.8, "lap_guard", 1.6, 4, 8, "L", 2, "leather", 55392)
    f = guard.front
    for x in range(8):
        f.set(x, 0, "L3" if x % 2 else "L1")                             # running stitches round the edge
        f.set(x, 3, "L3" if x % 2 else "L1")
    for y in range(4):
        f.set(0, y, "L3" if y % 2 else "L1"), f.set(7, y, "L3" if y % 2 else "L1")
    f.hline(2, 5, 1, "L4"), f.hline(3, 4, 2, "L3")                       # rubbed shiny by the desk edge
    f.set(5, 2, "K1"), f.set(2, 2, "K2")                                  # ink spots
    shoes(g, "slipper", "L", 2)
