"""Barber-Surgeon's Striped Apron: a rolled-sleeve shirt under a bib apron striped like a barber's pole, a razor case and a bleeding bowl."""
from kit import body, neckline, roll, sleeves
from kit_m05 import cord_end
from paint import k, solid

META = {
    "name": "Barber-Surgeon's Striped Apron",
    "gender": "male",
    "description": "A barber-surgeon's bib apron striped on the slant like his pole, over a rolled-sleeve shirt, a razor case in the bib pocket and a notched brass bleeding bowl at the hip.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def pole(face, x0, x1, y0, y1, oy=0):
    """Barber's-pole stripes running on the slant."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            face.set(x, y, "A2" if (x + y + oy) % 4 < 2 else "S4")


def build(g):
    b = body(g, "S", "weave", 35040, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 35041, base=3, rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    pole(jf, 1, 6, 3, 11)
    jf.vline(0, 3, 11, "A1"), jf.vline(7, 3, 11, "A1")                 # bound edges of the bib
    jf.hline(1, 6, 3, "A1")
    jf.vline(1, 0, 2, "L2"), jf.vline(6, 0, 2, "L2")                   # neck straps
    jacket.top.vline(1, 0, 3, "L2"), jacket.top.vline(6, 0, 3, "L2")
    for y in range(0, 9):                                               # straps crossed on the back
        jb.set(min(7, 1 + y * 6 // 8), y, "L2"), jb.set(max(0, 6 - y * 6 // 8), y, "L2")
    jb.hline(0, 7, 9, "S1"), jacket.right.hline(0, 3, 9, "S1"), jacket.left.hline(0, 3, 9, "S1")
    jf.hline(4, 6, 5, "A1"), jf.hline(4, 6, 6, "S2")                   # bib pocket mouth
    # Razor case standing in the pocket.
    case = g.piece("razor_case", "TORSO", (-.5, -2, -.5), (1, 3, 1), pivot=(1.5, 5.4, -2.65))
    solid(case, "L", "leather", 35042, 1)
    case.strip.hline(0, case.strip.w - 1, 0, "M3")
    # The apron's lap, over any skirt.
    lap = g.piece("apron_lap", "TORSO", (-4, 0, 0), (8, 7, 1), pivot=(0, 10.4, -3.15), motion="flap_front")
    solid(lap, "S", "weave", 35043, 3)
    pole(lap.front, 0, 7, 0, 6, oy=2)
    lap.front.vline(0, 0, 6, "A1"), lap.front.vline(7, 0, 6, "A1"), lap.front.hline(0, 7, 6, "A1")
    lap.front.hline(0, 7, 0, "S2")
    for i, x in enumerate((-.6, .6)):
        cord_end(g, f"apron_tie_{i}", (x, 9.6, 2.7), 4, "S", 3, 35044 + i, rotation=(0, 0, 14 if i else -14))
    # Bleeding bowl: a brass dish with the notch for the arm, slung at the hip.
    thong = g.piece("bowl_thong", "TORSO", (-.5, 0, -.5), (1, 1, 1), pivot=(-3.0, 9.2, -3.55), motion="flap_front")
    solid(thong, "L", "plain", 35046, 2, edge=False)
    bowl = g.piece("bleeding_bowl", "TORSO", (-1.5, 1, -.5), (3, 3, 1), pivot=(-3.0, 9.2, -3.55), motion="flap_front")
    solid(bowl, "M", "smooth", 35047, 3, edge=False)
    f = bowl.front
    f.set(0, 0, "M4"), f.set(1, 0, "K2"), f.set(2, 0, "M4")
    f.set(0, 1, "M3"), f.set(1, 1, "M2"), f.set(2, 1, "M3")
    f.set(0, 2, "M1"), f.set(1, 2, "M3"), f.set(2, 2, "M1")
    bowl.top.set(1, 0, k("K", 2))
