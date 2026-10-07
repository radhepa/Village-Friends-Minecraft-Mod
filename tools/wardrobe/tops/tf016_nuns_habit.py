"""Nun's Habit: a dark habit with a white wimple, a veil down the back, a scapular, wide sleeves and a rosary."""
from kit import body, sleeves
from kit_female import bells, girdle, hanging, over_panel
from paint import fabric, solid

META = {
    "name": "Nun's Habit",
    "gender": "female",
    "description": "A sister's habit: white wimple and dark veil, a long scapular, wide sleeves, a knotted cord and a rosary.",
    "tags": ["holy", "robe"],
    "locked_to": "bf016_nuns_habit_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 11601, base=1)
    j = g.part("jacket")
    for face in (j.front, j.back):
        fabric(face, "P", "weave", 11602, 0, 2, 0, 4, 12)            # the scapular
        face.vline(2, 0, 11, "P1"), face.vline(5, 0, 11, "P1")
    fabric(j.top, "P", "weave", 11602, 1, 2, 0, 4, 4)
    sleeves(g, "P", "weave", 11603, base=1, rows=(0, 11))
    for box in bells(g, "P", "weave", 11604, base=1, y=4.0, h=6, size=6, lining="S4"):
        for face in box.sides:
            face.hline(0, face.w - 1, 5, "P0")
    wimple = g.piece("wimple", "TORSO", (-4.5, -1.4, -2.6), (9, 2, 5), inflate=.12)
    solid(wimple, "S", "plain", 11605, 4, edge=False)
    bib = g.piece("wimple_bib", "TORSO", (-3, 0, 0), (6, 4, 1), pivot=(0, -.8, -2.8))
    solid(bib, "S", "plain", 11606, 4)
    bib.front.hline(0, 5, 3, "S3"), bib.front.hline(1, 4, 0, "S3")
    veil = g.piece("veil", "TORSO", (-4.5, 0, 0), (9, 10, 1), pivot=(0, -.6, 2.45), rotation=(6, 0, 0))
    solid(veil, "K", "plain", 11607, 2)
    veil.back.vline(2, 1, 9, "K1"), veil.back.vline(6, 1, 9, "K1"), veil.back.hline(0, 8, 9, "K1")
    for name, back in (("scapular_front", False), ("scapular_back", True)):
        face = over_panel(g, name, 12, "P", "weave", 11608, base=0, width=4, top=9.0, back=back)
        face.vline(0, 0, 11, "P1"), face.vline(3, 0, 11, "P1")
    girdle(g, "cord", 7.8, role="S", base=3, height=1, buckle=None, texture="plain")
    end = hanging(g, "cord_end", 2.2, 9, role="S", base=3, top=8.8)
    for y in (2, 5, 8):
        end.front.set(0, y, "S1")                                     # three knots
    rosary = hanging(g, "rosary", -2.4, 7, role="M", base=2, top=8.8)
    for y in range(0, 7, 2):
        rosary.front.set(0, y, "M4")
    cross = g.piece("rosary_cross", "TORSO", (-1, 7, -.1), (2, 2, 1), pivot=(-2.4, 8.8, -3.25), motion="flap_front")
    solid(cross, "M", "smooth", 11609, 3)
    cross.front.set(0, 1, "M1")
