"""Mountain Herder's Felt Leggings and Skirt: a knee-length wool skirt bordered with felt applique
triangles, thick felt leggings stitched down the shin and soft boots with rolled felt cuffs."""
from kit import SIDES
from kit_female import leg_ring_fold, shoes, skirt
from paint import fabric

META = {
    "name": "Mountain Herder's Felt Leggings and Skirt",
    "gender": "female",
    "description": "A knee-length wool skirt bordered with felt applique triangles, over thick felt leggings "
                   "stitched down the shin and soft boots with rolled felt cuffs.",
    "tags": ["rugged", "casual", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 58021, top=9.8, length=7, side_length=6, flare=6, folds=False)
    s.band(2, "triangles", "A2", from_bottom=True)
    s.band(0, "line", "S3", from_bottom=True)
    for face in s.wide_faces:
        for x in range(1, face.w, 3):
            face.vline(x, 2, 3, "P1")                                # soft pleats under the waist
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        fabric(leg.strip, "S", "plain", 58022 + (side == "left"), 2, 0, 4, leg.strip.w, 6)
        for face in leg.sides:
            face.hline(0, face.w - 1, 4, "S3")
        # A felt strip appliqued down each shin between two stitched seams.
        f = leg.front
        for y in range(5, 10):
            f.set(0, y, "S1"), f.set(3, y, "S1")
            f.set(1, y, "A2"), f.set(2, y, "A1")
        f.hline(1, 2, 5, "A3")
    shoes(g, "boot", "L", 2, top=10)
    for box in leg_ring_fold(g, "felt_cuff", 9.2, role="S", base=1, size=5):
        for face in box.sides:
            face.set(0, 1, "S0"), face.set(face.w - 1, 1, "S0")
