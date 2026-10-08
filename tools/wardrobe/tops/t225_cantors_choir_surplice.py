"""Cantor's Choir Surplice: a full pleated white surplice with great bell sleeves over a dark cassock, a choir book held against the arm."""
from kit import body, sleeves
from kit_male import sleeve_shapes
from kit_m05 import over_panels

META = {
    "name": "Cantor's Choir Surplice",
    "gender": "male",
    "description": "A cantor's knee-length white surplice gathered in fine pleats from a plain yoke, with great bell sleeves, over a dark cassock, and a clasped choir book carried on his arm.",
    "tags": ["holy", "robe"],
    "covers_waist": True,
}


def pleats(face, y0, y1, ox=0):
    for y in range(y0, y1 + 1):
        for x in range(face.w):
            face.set(x, y, "S2" if (x + ox) % 2 == 0 else "S4")


def build(g):
    b = body(g, "P", "smooth", 35160, base=1)
    b.front.hline(2, 5, 0, "P0")
    surplice = body(g, "S", "weave", 35161, base=3, layer="jacket")
    for face in surplice.sides:
        pleats(face, 3, 11, face.x0)
        face.hline(0, face.w - 1, 2, "S1")                              # where the pleats gather to the yoke
    for x in (2, 3, 4, 5):
        surplice.front.clear(x, 0)                                      # the cassock collar shows at the throat
    surplice.front.clear(3, 1), surplice.front.clear(4, 1)
    b.front.set(3, 1, "P0"), b.front.set(4, 1, "P0")
    sleeves(g, "P", "smooth", 35162, base=1, rows=(0, 10))
    for side in ("right", "left"):                                      # pleated upper sleeve on the overlay
        over = g.part(f"{side}_sleeve")
        pleats(over.strip, 0, 4, 0)
        over.top.fill("S3")
    for s in sleeve_shapes(g, "bell_sleeve", "S", 2.4, (6, 6, 6), "weave", 35163, base=3, inflate=.08):
        for face in s.sides:
            face.hline(0, face.w - 1, 0, "S3")
            pleats(face, 1, 4, face.x0)
            face.hline(0, face.w - 1, 5, "S2")
        s.top.fill("S3"), s.bottom.fill("S1")
    front, back, sides = over_panels(g, "surplice", 7, "S", "weave", 35164, base=3, top=10.2, width=10, side_len=6)
    for face in (front, back):
        pleats(face, 1, 5)
        face.hline(0, 9, 6, "S1")
    for box in sides:
        for face in box.sides:
            pleats(face, 0, face.h - 2, face.x0)
            face.hline(0, face.w - 1, face.h - 1, "S1")
    # A small clasped choir book carried on the left forearm.
    book = g.piece("choir_book", "LEFT_ARM", (-1.5, 0, -.5), (3, 4, 1), pivot=(1.0, 6.4, -3.9), rotation=(-8, 0, 0))
    for face in book.faces:
        face.fill("S4")
    book.front.fill("L2"), book.back.fill("L1")
    book.front.hline(0, 2, 0, "L3"), book.front.set(2, 1, "M3"), book.front.set(2, 2, "M3")
    book.front.set(0, 3, "M2"), book.front.set(0, 0, "M3")
    book.right.fill("L1")                                               # the spine
    book.top.set(1, 0, "A2")                                            # ribbon marker
