"""Tracker's Fur-Lined Hood Jerkin: a sleeveless laced jerkin with fur at the armholes, a deep hood thrown back
with a shaggy fur ruff, a sheathed skinning knife and a bundle of arrow shafts tied at the hip."""
from kit import sleeves
from kit_female import arm_rings, fur_box, girdle, lacing, neck
from kit_f04 import back_prop, front_prop
from paint import fabric, solid, strip_fabric

META = {
    "name": "Tracker's Fur-Lined Hood Jerkin",
    "gender": "female",
    "description": "A sleeveless laced jerkin with fur-trimmed armholes, a deep hood thrown back with a shaggy fur "
                   "ruff, a skinning knife and a bundle of arrow shafts at the hip.",
    "tags": ["rugged"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "twill", 54201, 2)
    fabric(b.top, "P", "twill", 54201, 3), fabric(b.bottom, "P", "twill", 54201, 1)
    neck(b.front, "v", "P", 2, edge="P3")
    lacing(b.front, 3, 3, 8, "ladder", lace="L3", under="S3", eyelet="M2")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "P1")
    b.back.vline(3, 1, 11, "P1"), b.back.vline(4, 1, 11, "P3")       # back seam
    # The shirt sleeves, pushed up, with a fur ring round each armhole of the jerkin.
    sleeves(g, "S", "weave", 54202, base=3, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 7, "S2"), arm.strip.hline(0, 15, 8, "S4")
        arm.front.vline(1, 2, 6, "S2")
    for box in arm_rings(g, "armhole_fur", -2.3, 2, 5, inflate=.14):
        fur_box(box, "L", 54203, 3)
    # The hood, thrown back over the shoulders; the fur ruff round its face opening lies uppermost.
    hood = g.piece("hood", "TORSO", (-4, 0, 0), (8, 5, 2), pivot=(0, -.6, 2.4), rotation=(18, 0, 0))
    solid(hood, "P", "twill", 54205, 2)
    hood.back.vline(3, 0, 4, "P1"), hood.back.vline(4, 0, 4, "P3")    # the centre seam
    hood.back.hline(0, 7, 4, "P1")
    ruff = g.piece("hood_ruff", "TORSO", (-4.5, -1, -.5), (9, 2, 3), pivot=(0, -.2, 2.9), rotation=(18, 0, 0))
    fur_box(ruff, "L", 54206, 3)
    girdle(g, "belt", 8.4, role="L", height=1)
    # Skinning knife on the left front hip, hilt up.
    sheath = front_prop(g, "knife_sheath", 2.4, (1, 4, 1), drop=.8, rotation=(0, 0, 12))
    solid(sheath, "L", "leather", 54207, 1)
    sheath.front.set(0, 0, "M3"), sheath.front.set(0, 3, "M2")
    hilt = front_prop(g, "knife_hilt", 2.4, (1, 2, 1), drop=-1.2, rotation=(0, 0, 12))
    solid(hilt, "S", "smooth", 54208, 3, edge=False)
    hilt.front.set(0, 1, "M3")
    # A bundle of fresh arrow shafts tied with cord, slung behind the right hip.
    for i, (dx, key) in enumerate(((-.8, "L"), (0.0, "S"), (.8, "L"))):
        shaft = back_prop(g, f"shaft_bundle_{i}", -2.6 + dx, (1, 9, 1), drop=-3.0, z=2.45 + (i % 2) * .5,
                          rotation=(0, 0, 18))
        solid(shaft, key, "smooth", 54209 + i, 3, edge=False)
        shaft.strip.hline(0, shaft.strip.w - 1, 0, "A3" if i == 1 else "S4")
    tie = back_prop(g, "shaft_bundle_tie", -2.6, (3, 1, 2), drop=1.6, z=2.4, rotation=(0, 0, 18))
    solid(tie, "S", "plain", 54212, 2, edge=False)
