"""Scholar's Hood & Girdle Book: a gown with a fur-rimmed academic hood, rivet spectacles on a cord and a book at the belt."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk
from paint import fabric, line, solid

META = {
    "name": "Scholar's Hood & Girdle Book",
    "gender": "male",
    "description": "A master's gown with a fur-rimmed academic hood down the back, rivet spectacles on a cord and a girdle book at the belt.",
    "tags": ["scholarly", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 5401)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 5402, rows=(0, 10), cuff="A2")
    hood = g.piece("academic_hood", "TORSO", (-3, 0, 0), (6, 7, 1), pivot=(0, .2, 2.6), rotation=(4, 0, 0))
    solid(hood, "P", "velvet", 5403, 2)
    hood.back.vline(0, 0, 6, "A2"), hood.back.vline(5, 0, 6, "A2"), hood.back.hline(0, 5, 6, "A2")
    hood.back.vline(2, 1, 5, "A1"), hood.back.vline(3, 1, 5, "A3")      # the lining turned out
    rim = blk(g, "hood_fur_rim", (0, -.6, 2.6), (8, 1, 2), "S", 4, "plain", 5404)
    rim.back.set(2, 0, "S2"), rim.back.set(5, 0, "S2")
    jf = g.part("jacket").front
    line(jf, 2, 0, 3, 4, "K3"), line(jf, 5, 0, 4, 4, "K3")               # the spectacles' cord
    specs = blk(g, "rivet_spectacles", (0, 4.6, -2.65), (3, 1, 1), "M", 3, "smooth", 5405, edge=False)
    specs.front.set(0, 0, "K3"), specs.front.set(2, 0, "K3")
    belt(g, "belt", 9.4, height=1)
    blk(g, "girdle_book_tail", (2.6, 9.8, -2.8), (1, 1, 1), "L", 2, "leather", 5406, edge=False)
    book = blk(g, "girdle_book", (2.6, 10.6, -2.8), (2, 3, 1), "L", 1, "leather", 5407, motion="sway")
    book.front.set(1, 1, "M3"), book.right.fill("S4"), book.bottom.fill("S3")
    for face in flaps(g, "gown", 5, "P", "weave", 5408, top=10.8):
        face.hline(0, 8, 4, "A2")
