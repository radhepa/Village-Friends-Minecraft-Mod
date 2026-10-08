"""Ferrywoman's Waxed Breeches: close knee breeches rubbed with wax against the spray, a glossy sheen down
each leg, buckled knee straps over ribbed stockings, low tied shoes and a rope belt knotted at the hip."""
from kit import SIDES, legs, waistband
from kit_female import shoes
from paint import fabric, solid

META = {
    "name": "Ferrywoman's Waxed Breeches",
    "gender": "female",
    "description": "Wax-rubbed knee breeches with a glossy sheen, buckled knee straps over ribbed stockings, low shoes and a knotted rope belt.",
    "tags": ["sea", "work", "sturdy"],
}

SEED = 53135


def build(g):
    legs(g, "P", "twill", SEED, rows=(0, 7), crease=False)
    waistband(g, "P", "twill", SEED + 1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:                                     # the waxed outer layer
            fabric(face, "P", "smooth", SEED + 2, 1, 0, 0, face.w, 7)
            face.hline(0, face.w - 1, 6, "P0")
        shine = 1 if side == "right" else 2
        for y in range(0, 6):
            if y % 3 != 2:
                pants.front.set(shine, y, "P3")                     # the wax catching the light
        pants.front.set(shine + (1 if side == "right" else -1), 1, "P4")
        for face in (pants.right, pants.left):
            face.vline(2 if face is pants.right else 1, 0, 5, "P2")
        for y in range(8, 10):                                       # ribbed stockings below the knee
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "S2" if x % 2 else "S3")
        leg.strip.hline(0, leg.strip.w - 1, 7, "L2")                # the knee strap
        for face in pants.sides:
            face.hline(0, face.w - 1, 7, "L2")
        pants.front.set(2 if side == "right" else 1, 7, "M3")       # its buckle
    shoes(g, "shoe", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "S4"), pants.front.set(2, 10, "S4")  # the ties over the instep
    # A rope belt knotted at the left hip, its ends hanging.
    rope = g.piece("waist_rope", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.3, 0), inflate=.06)
    solid(rope, "S", "plain", SEED + 3, 2, edge=False)
    for f in rope.sides:
        for x in range(f.w):
            f.set(x, 0, "S3" if (x + f.x0) % 2 else "S1")
    knot = g.piece("waist_rope_knot", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(3.0, 9.0, -3.3))
    solid(knot, "S", "plain", SEED + 4, 2, edge=False)
    knot.front.set(0, 0, "S3"), knot.front.set(1, 1, "S1")
    end = g.piece("waist_rope_end", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(3.4, 10.6, -3.3), motion="flap_front")
    solid(end, "S", "plain", SEED + 5, 2)
    end.front.set(0, 2, "S4")
