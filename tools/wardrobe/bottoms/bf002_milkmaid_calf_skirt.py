"""Milkmaid's Calf Skirt: a calf-length skirt over a striped petticoat that peeks below the hem, and wooden clogs."""
from kit import SIDES
from kit_female import shoes, skirt, stripes
from paint import solid

META = {
    "name": "Milkmaid's Calf Skirt",
    "gender": "female",
    "description": "A calf-length wool skirt with a red-striped petticoat peeking beneath, worn with wooden clogs.",
    "tags": ["casual", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10211, top=9.4, length=9)
    s.hem("P1")
    # The petticoat hangs from a lower hinge, so it always stays behind the outer skirt.
    for name, z, motion, face in (("petticoat_front", -2.85, "flap_front", "front"), ("petticoat_back", 1.85, "flap_back", "back")):
        p = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 11, 1), pivot=(0, 10.0, z), motion=motion)
        solid(p, "S", "weave", 10212, 3)
        for f in p.sides:
            stripes(f, ["S4", "S4", "A2"], 1, y0=6)
            f.hline(0, f.w - 1, 10, "S2")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        stripes(leg.strip, ["S4", "S4", "A2"], 1, y0=6, h=4, offset=0)
    shoes(g, "clog", "L", 3)
