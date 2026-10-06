"""Tasseled Ankle Boots: slim pressed trousers over soft ankle boots with a swinging tassel at each instep."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from paint import solid

META = {
    "name": "Tasseled Ankle Boots",
    "gender": "male",
    "description": "Slim pressed trousers over soft ankle boots, each tied at the instep with a cord ending in a swinging tassel.",
    "tags": ["casual", "slim"],
}


def build(g):
    legs(g, "P", "twill", 6411, rows=(0, 9))
    waistband(g, "P", "twill", 6412)
    footwear(g, "boot", top=9, base=3)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 9, "A2")                                  # tie cord
        tassel = g.piece(f"{side}_tassel", leg_bone(side), (-.5, 0, -.5), (1, 2, 1), pivot=(0, 9.4, -2.6),
                         motion="sway")
        solid(tassel, "A", "plain", 6413 + i, 2)
        tassel.strip.hline(0, tassel.strip.w - 1, 0, "A3"), tassel.strip.hline(0, tassel.strip.w - 1, 1, "A1")
