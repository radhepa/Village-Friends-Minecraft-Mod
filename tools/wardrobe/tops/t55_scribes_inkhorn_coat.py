"""Scribe's Inkhorn Coat: an off-centre buttoned coat with an inky cuff, a penner and inkhorn on a cord and a quill."""
from kit import belt, body, flaps, sleeves
from kit_male import blk, buttons, flecks

META = {
    "name": "Scribe's Inkhorn Coat",
    "gender": "male",
    "description": "A copyist's coat buttoned off-centre, one cuff spotted with ink, a penner and inkhorn on a cord and a quill at the belt.",
    "tags": ["scholarly", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 5501)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.vline(2, 0, 11, "P0")
    buttons(b.front, 1, 1, 9, 2, "M3")
    b.front.hline(3, 5, 0, "S3")                                         # shirt at the throat
    sleeves(g, "P", "twill", 5502, rows=(0, 10), cuff="P1")
    flecks(g.part("right_arm").strip, "K2", 5503, .25, rows=range(8, 11))   # the writing hand's cuff
    belt(g, "belt", 9.4, height=1)
    horn = blk(g, "inkhorn", (2.4, 10.4, -2.8), (1, 2, 1), "S", 3, "plain", 5504)
    horn.strip.hline(0, horn.strip.w - 1, 1, "S2")
    blk(g, "inkhorn_stopper", (2.4, 9.8, -2.8), (1, 1, 1), "K", 2, "plain", 5505, edge=False)
    penner = blk(g, "penner", (3.3, 10.0, -2.8), (1, 4, 1), "L", 2, "leather", 5506)
    penner.strip.hline(0, penner.strip.w - 1, 0, "M3")
    quill = blk(g, "quill", (-2.8, 7.6, -2.75), (1, 4, 1), "S", 4, "plain", 5507, rotation=(0, 0, 14))
    quill.strip.hline(0, quill.strip.w - 1, 3, "K2")
    quill.strip.hline(0, quill.strip.w - 1, 2, "S2")
    for face in flaps(g, "coat_skirt", 5, "P", "twill", 5508, top=10.8, slit=True):
        face.hline(0, 8, 4, "P1")
