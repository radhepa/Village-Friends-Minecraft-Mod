"""Joggers: soft knit joggers with ribbed cuffs gathered at the ankle and a drawstring."""
from kit_casual import shoes, trousers
from kit import leg_ring
from paint import solid

META = {
    "name": "Joggers",
    "gender": "male",
    "description": "Soft knit joggers with ribbed ankle cuffs, a drawstring waist and canvas shoes.",
    "tags": ["casual", "modern", "relaxed"],
}


def build(g):
    trousers(g, "P", 2, "plain", 11601, end=8, loops=False)
    for ring in leg_ring(g, "ankle_cuff", 8.2, "P", 2, size=(5, 2, 5), texture="rib", ):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P3")
    for i, x in enumerate((-.6, .6)):
        end = g.piece(f"waist_drawstring_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, 9.8, -2.6),
                      rotation=(0, 0, -10 + 20 * i))
        solid(end, "S", "plain", 11602, 3, edge=False)
    shoes(g, "canvas")
