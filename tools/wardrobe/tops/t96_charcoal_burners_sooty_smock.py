"""Charcoal Burner's Sooty Smock: a smock blackened with soot towards the hem, a leather shoulder cape and a long clamp rake."""
from kit import belt, body, sleeves
from kit_male import flecks, shoulder_cape
from paint import solid

META = {
    "name": "Charcoal Burner's Sooty Smock",
    "gender": "male",
    "description": "A collier's smock blackened with soot from the hem up, a leather shoulder cape against sparks and a long rake for the clamp.",
    "tags": ["work", "rugged"],
    "locked_to": "b96_charcoal_burners_sooty_trousers",
    "covers_waist": True,
}


def sooty(face, seed, top=0):
    for y in range(face.h):
        density = max(0.0, (y + top - 5) / 24)
        flecks(face, "K3", seed, density, rows=range(y, y + 1))
    face.hline(0, face.w - 1, face.h - 1, "K3")                           # the hem dragged through ash


def build(g):
    b = body(g, "S", "weave", 9601, base=2)
    for face in b.sides:
        sooty(face, 9602)
    sleeves(g, "S", "weave", 9603, rows=(0, 10))
    for side in ("right", "left"):
        sooty(g.part(f"{side}_arm").strip, 9604, top=2)
    cape = shoulder_cape(g, "spark_cape", "L", "leather", 9605, length=3, width=11)
    for face in cape.sides:
        face.hline(0, face.w - 1, 2, "L1")
        flecks(face, "K2", 9606, .12)
    belt(g, "belt", 9.6, height=1)
    shaft = g.piece("rake_shaft", "TORSO", (-.5, 0, -.5), (1, 15, 1), pivot=(-3.2, -3.4, 3.0), rotation=(0, 0, -10))
    solid(shaft, "L", "plain", 9607, 3)
    head = g.piece("rake_head", "TORSO", (-2, -1, -.5), (4, 1, 1), pivot=(-3.2, -3.4, 3.0), rotation=(0, 0, -10))
    solid(head, "M", "smooth", 9608, 1, edge=False)
