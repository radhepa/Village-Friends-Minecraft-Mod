"""Kilted-Up Skirt: a skirt hitched into the girdle at both hips, showing a lace-edged petticoat, bare calves and sandals."""
from kit import SIDES
from kit_female import shoes, skirt, trim, waist_belt
from paint import solid, strip_fabric

META = {
    "name": "Kilted-Up Skirt",
    "gender": "female",
    "description": "An overskirt kilted up at both hips over a lace-edged petticoat, bare calves and strap sandals.",
    "tags": ["casual", "relaxed", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10711, top=9.8, length=8, side_length=5, flare=9)
    s.hem("P1")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "weave", 10712, 3, 3, 6)
        trim(leg.strip, 6, "dots", "S4", x0=0, x1=15)
        leg.strip.hline(0, 15, 3, "S2")
    for side, x in (("right", -5.9), ("left", 5.9)):
        tuck = g.piece(f"waist_tuck_{side}", "TORSO", (-1, 0, -1.5), (2, 3, 3), pivot=(x, 9.4, 0))
        solid(tuck, "P", "weave", 10713, 2)
        for f in tuck.sides:
            f.vline(0, 0, 2, "P1"), f.hline(0, f.w - 1, 2, "P1")
    waist_belt(g, "waist_cord", 9.2, role="A", base=2, height=1, buckle=None, texture="plain")
    shoes(g, "sandal", "L", 2)
