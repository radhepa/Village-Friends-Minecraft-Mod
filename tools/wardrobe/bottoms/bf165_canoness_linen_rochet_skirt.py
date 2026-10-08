"""Canoness's Linen Rochet Skirt: the knee-length skirt of a white linen rochet, finely pleated and edged
with a band of lace, falling over a dark floor-length cassock and black shoes."""
from kit_female import shoes, skirt, tier, trim

META = {
    "name": "Canoness's Linen Rochet Skirt",
    "gender": "female",
    "description": "A knee-length white linen rochet, finely pleated and lace-edged, over a dark floor-length cassock skirt.",
    "tags": ["holy", "fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "plain", 55171, base=1, top=9.8, length=12, back_length=12, folds=False, gather=False)
    for face in s.wide_faces:
        for x in range(1, face.w, 3):
            face.vline(x, 7, face.h - 2, "P0")
    s.hem("P0")
    # The rochet: a white pleated layer over the upper skirt, sharing its hinges.
    for face in tier(g, s, "rochet", 0, 7, role="S", texture="plain", seed=55172, base=4, grow=1, flare=6):
        for x in range(face.w):
            if x % 2:
                face.vline(x, 1, face.h - 3, "S3")                       # fine linen pleats
        face.hline(0, face.w - 1, 0, "S4")
        trim(face, face.h - 2, "scallop", "S3", "S2")                    # the lace border
    shoes(g, "shoe", "K", 2)
