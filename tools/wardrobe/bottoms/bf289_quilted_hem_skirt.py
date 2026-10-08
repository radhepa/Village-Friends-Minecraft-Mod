"""Quilted-Hem Skirt: a plain skirt finished with a deep padded hem roll quilted in waves, over low leather shoes."""
from kit_female import shoes, skirt, tier, trim

META = {
    "name": "Quilted-Hem Skirt",
    "gender": "female",
    "description": "A plain wool skirt finished with a deep padded hem roll, quilted in rows of waves to weight it against the wind, over low shoes.",
    "tags": ["casual", "sturdy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 60140, top=9.8, length=11, flare=5)
    roll = tier(g, s, "padded_hem", y=7, h=4, role="P", texture="plain", seed=60141, grow=2, flare=7)
    for face in roll:
        face.fill("P2")
        face.hline(0, face.w - 1, 0, "P3")
        trim(face, 1, "wave", "P1")                       # quilted waves, stitched in two rows
        for x in range(face.w):
            if face.get(x, 1) == "P2":
                face.set(x, 1, "P3")                                   # the puff above each dip of stitching
        face.hline(0, face.w - 1, 3, "P0")                             # the bound bottom edge
    shoes(g, "shoe", "K", 2, toe="K3")
