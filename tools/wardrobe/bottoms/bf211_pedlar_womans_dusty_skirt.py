"""Pedlar Woman's Dusty Skirt: a mid-calf road skirt faded with dust toward the hem, a darned patch,
knitted stockings, ankle boots and a coin purse on a cord."""
from kit import SIDES
from kit_f07 import dust, patch, prop
from kit_female import shoes, skirt
from paint import fabric

META = {
    "name": "Pedlar Woman's Dusty Skirt",
    "gender": "female",
    "description": "A mid-calf wool skirt pale with road dust toward the hem, a darned patch, knitted stockings, "
                   "ankle boots and a coin purse swinging on a cord.",
    "tags": ["casual", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 57021, top=9.8, length=9, flare=6)
    s.paint(lambda f: dust(f, rows=3, delta=1, y_end=f.h - 2))
    s.hem("P1")
    patch(s.front.front, 6, 3, 3, 3, "P3", "P0")                    # a darned patch over a tear
    patch(s.back.back, 1, 2, 3, 3, "P3", "P0")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        fabric(leg.strip, "S", "knit", 57022 + (side == "left"), 2, 0, 7, 16, 2)
    shoes(g, "ankle", "L", 2, top=9)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.set(0, 10, "L3"), face.set(face.w - 1, 11, "K0")     # scuffed toes
    # A coin purse on a cord, tucked under the waistband at the left hip.
    prop(g, "waist_purse_cord", "TORSO", (0, 0, -1), (1, 2, 1), pivot=(2.4, 9.4, -3.0),
         role="L", base=3, seed=57024, motion="flap_front", edge=False)
    purse = prop(g, "waist_purse", "TORSO", (-.5, 2, -1.2), (2, 2, 1), pivot=(2.4, 9.4, -3.0),
                 role="L", texture="leather", base=2, seed=57025, motion="flap_front")
    purse.front.hline(0, 1, 0, "L1"), purse.front.set(1, 1, "M3")
    band = prop(g, "waist_band", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.4, 0), role="L",
                texture="leather", base=1, seed=57026, edge=False, inflate=.05)
    band.front.set(5, 0, "M3")
