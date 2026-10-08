"""Sheaf Binder's Straw-Tied Skirt: a calf-length skirt girt with a twisted straw band knotted at the hip,
linen wraps on the shins bound with more straw, and turnshoes."""
from kit_female import leg_rings, shoes, skirt, wraps
from kit_f01 import twist
from paint import k, solid

META = {
    "name": "Sheaf Binder's Straw-Tied Skirt",
    "gender": "female",
    "description": "A calf-length skirt girt with a twisted straw band knotted at the hip, linen shin wraps bound with straw and soft turnshoes.",
    "tags": ["work", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 51140, top=9.8, length=10, flare=5)
    s.hem("P1")
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 2, "P3")
    # The straw band round the hips, its knot and two stiff ends at the right side.
    band = g.piece("waist_straw_band", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 10.0, 0), inflate=.1)
    for f in band.faces:
        twist(f, 0, "M3", "M1", rows=f.h)
    knot = g.piece("waist_straw_knot", "TORSO", (-1, -1, -1), (2, 2, 2), pivot=(-4.4, 10.5, -2.6), inflate=.05)
    for f in knot.faces:
        twist(f, 0, "M3", "M2", rows=f.h)
    for i, rot in enumerate((14, -10)):
        end = g.piece(f"waist_straw_end_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-4.6 + i * .9, 11.2, -3.1),
                      rotation=(-8, 0, rot), motion="flap_front")
        solid(end, "M", "plain", 51141 + i, 3, edge=False)
        end.front.set(0, 2, "M4")
    # Linen wraps on the shins, bound with a straw band above the ankle.
    for side in ("right", "left"):
        leg = g.part(f"{side}_leg")
        for face in leg.sides:
            wraps(face, 8, 10, "S", 3, step=4)
    for box in leg_rings(g, "shin_straw", 8.4, 1, 5, inflate=.05):
        for f in box.faces:
            twist(f, 0, "M3", "M1", rows=f.h)
    shoes(g, "turnshoe", "L", 2, top=11)
    for side in ("right", "left"):
        g.part(f"{side}_pants").front.set(1, 11, k("L", 3))
