"""Guard's Riding Breeches: close wool breeches gathered under the knee, tall cuffed boots and a scabbard on the hip."""
from kit import SIDES, legs, waistband
from kit_female import leg_ring_fold, shoes, waist_belt
from paint import solid

META = {
    "name": "Guard's Riding Breeches",
    "gender": "female",
    "description": "Close wool breeches gathered under the knee, tall cuffed boots and a sword scabbard on the hip.",
    "tags": ["sturdy", "martial"],
}


def build(g):
    legs(g, "P", "twill", 12111, rows=(0, 6), crease=False)
    waistband(g, "P", "twill", 12112)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for x in range(1, 16, 2):
            leg.strip.set(x, 5, "P1")                                # gathered under the knee
        leg.strip.hline(0, 15, 6, "P3")
    shoes(g, "boot", "L", 2, top=6)
    leg_ring_fold(g, "boot_cuff", 5.4, "L", 2)
    waist_belt(g, "waist_belt", 9.4, height=1)
    scabbard = g.piece("waist_scabbard", "TORSO", (-.5, 0, -1), (1, 9, 2), pivot=(5.0, 10.0, .2), rotation=(-14, 0, -6))
    solid(scabbard, "L", "leather", 12113, 1)
    for face in scabbard.sides:
        face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 8, "M3")
    hilt = g.piece("waist_hilt", "TORSO", (-.5, -3, -.5), (1, 3, 1), pivot=(5.0, 10.0, .2), rotation=(-14, 0, -6))
    solid(hilt, "M", "smooth", 12114, 3)
    hilt.strip.hline(0, hilt.strip.w - 1, 2, "M4")
