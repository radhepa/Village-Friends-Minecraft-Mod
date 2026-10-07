"""Girdle-Book Kirtle: a high-necked kirtle with a white collar band, ink-stained cuffs and a book hung from the girdle."""
from kit import body, sleeves
from kit_female import girdle, hanging, neck
from paint import solid

META = {
    "name": "Girdle-Book Kirtle",
    "gender": "female",
    "description": "A high-necked kirtle with a linen collar band, ink-stained cuffs and a little girdle-book on its strap.",
    "tags": ["scholarly", "simple"],
}


def build(g):
    b = body(g, "P", "weave", 12601)
    neck(b.front, "round", "P", 2)
    for face in (b.front, b.back):
        face.hline(0, 7, 0 if face is b.back else 1, "S4")
    b.front.set(2, 0, "S4"), b.front.set(5, 0, "S4")
    for face in (b.right, b.left):
        face.hline(0, 3, 0, "S4")
    for x in (2, 5):
        b.front.vline(x, 3, 11, "P1")                                # princess seams
    sleeves(g, "P", "weave", 12602, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S4"), arm.strip.hline(0, 15, 11, "S3")
    ink = g.part("right_arm")
    for x, y in ((5, 10), (6, 11), (9, 10), (4, 11)):
        ink.strip.set(x, y, "K1")                                    # ink on the cuff
    girdle(g, "girdle", 7.8, role="L", height=1)
    strap = hanging(g, "book_strap", -2.6, 4, role="L", top=8.8)
    book = g.piece("girdle_book", "TORSO", (-1.5, 4, -.2), (3, 4, 1), pivot=(-2.6, 8.8, -3.25), motion="flap_front")
    solid(book, "L", "leather", 12603, 2)
    book.front.vline(1, 0, 3, "L1"), book.front.set(0, 1, "M3"), book.front.set(2, 2, "M3")
    book.bottom.fill("S4"), book.left.vline(0, 0, 3, "S4")
