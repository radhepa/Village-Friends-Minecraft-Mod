"""Illuminator's Ink-Splashed Skirt: a pale linen work skirt where ink has run down from the lap in thin
drips, each ending in a drop, and a stained pen-wiping rag is tucked into the waistband at the hip."""
from kit_female import OVER_FRONT, shoes, skirt
from paint import solid

META = {
    "name": "Illuminator's Ink-Splashed Skirt",
    "gender": "female",
    "description": "A pale linen skirt with thin ink drips running down from the lap, and an ink-stained wiping rag tucked at the hip.",
    "tags": ["work", "casual", "skirt", "long_skirt"],
}

# (column, first row, length) of each drip; a few spatters around where they started.
DRIPS_FRONT = [(2, 2, 5), (3, 3, 2), (6, 2, 7), (8, 4, 3)]
DRIPS_BACK = [(4, 3, 3)]


def drips(face, spec):
    for x, y, n in spec:
        face.vline(x, y, y + n - 1, "K2")
        face.set(x, y + n, "K1")                                       # the drop gathering at the end
        if face.inside(x + 1, y - 1):
            face.set(x + 1, y - 1, "K2")


def build(g):
    s = skirt(g, "S", "plain", 55371, base=3, top=9.8, length=11, back_length=11, flare=5, folds=True, gather=True)
    drips(s.front.front, DRIPS_FRONT)
    drips(s.back.back, DRIPS_BACK)
    s.hem("S1")
    shoes(g, "turnshoe", "L", 2)
    # The wiping rag, tucked into the waistband and hanging over the skirt at the left hip.
    rag = g.piece("waist_rag", "TORSO", (-1.5, 0, -.2), (3, 4, 1), pivot=(3.0, 9.4, OVER_FRONT - .1), motion="flap_front")
    solid(rag, "S", "plain", 55372, 2)
    rag.front.set(0, 1, "K2"), rag.front.set(1, 2, "K1"), rag.front.set(2, 3, "A2")
    rag.front.hline(0, 2, 0, "S3")
    for x in range(3):
        rag.front.set(x, 3, "S1" if x % 2 else rag.front.get(x, 3))
