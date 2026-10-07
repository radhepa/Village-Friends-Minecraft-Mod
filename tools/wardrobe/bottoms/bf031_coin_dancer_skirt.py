"""Coin Dancer's Skirt: a flowing gauzy skirt under a coin-fringed hip scarf, with bells at the bare ankles."""
from kit import SIDES
from kit_female import leg_rings, skirt
from paint import solid, strip_fabric

META = {
    "name": "Coin Dancer's Skirt",
    "gender": "female",
    "description": "A flowing gauzy skirt under a coin-fringed hip scarf, with little bells tied at the bare ankles.",
    "tags": ["fancy", "whimsical", "skirt", "long_skirt"],
    "locked_to": "tf031_coin_dancer_bodice",
}


def build(g):
    s = skirt(g, "S", "plain", 13111, base=4, top=9.8, length=11, body_rows=(8, 11), flare=8)
    for face in s.wide_faces:
        for x in range(1, face.w, 3):
            face.vline(x, 2, face.h - 2, "S3")
    s.hem("A2")
    body = g.part("body")
    strip_fabric(body, "A", "velvet", 13112, 2, 8, 9)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "M4" if x % 2 else "M2")
    for name, z, motion, face_name in (("hip_scarf_front", -3.05, "flap_front", "front"), ("hip_scarf_back", 2.05, "flap_back", "back")):
        scarf = g.piece(name, "TORSO", (-5, 0, 0), (10, 3, 1), pivot=(0, 9.4, z), motion=motion)
        solid(scarf, "A", "velvet", 13113, 2)
        face = getattr(scarf, face_name)
        for x in range(10):
            face.set(x, 2, "M4" if x % 2 else "M2")                  # coins along the hem
        face.hline(3, 6, 2, "A1"), face.set(4, 2, "M4"), face.set(5, 2, "M3")
        face.hline(0, 9, 0, "M3")
    for side in SIDES:
        g.part(f"{side}_leg").bottom.fill("K1")
    for ring in leg_rings(g, "ankle_bells", 10.2, 1, 5, inflate=.06):
        solid(ring, "M", "smooth", 13114, 3, edge=False)
        for face in ring.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, "M4")
