"""Cook's Crossback Apron: a checked bib apron whose straps cross behind, over a blouse with sleeves rolled for the hearth."""
from kit import roll
from kit_female import checks, chemise, hanging, over_panel, sub
from paint import line, solid

META = {
    "name": "Cook's Crossback Apron",
    "gender": "female",
    "description": "A checked bib apron with straps crossed behind, over a rolled-sleeve blouse, and a tasting spoon on a cord.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 3, "weave", 13901, neckline="round", sleeve_rows=(0, 5))
    roll(g, "S", 2.8, base=3)
    j = g.part("jacket")
    checks(sub(j.front, 1, 2, 6, 9), "S4", "A3", 1, c="A2")
    for x in (1, 6):
        j.front.vline(x, 0, 1, "A2")
        j.top.vline(x, 0, 3, "A2")
    line(j.back, 1, 0, 6, 9, "A2"), line(j.back, 6, 0, 1, 9, "A2")
    for face in (j.right, j.left):
        face.hline(0, 3, 9, "A2")
    j.back.hline(0, 7, 9, "A2")
    j.front.hline(2, 5, 4, "S2"), j.front.hline(2, 5, 6, "S2")       # the bib pocket seams
    face = over_panel(g, "apron", 9, "S", "weave", 13902, base=4, width=9, top=9.0)
    checks(face, "S4", "A3", 1, c="A2")
    face.hline(0, 8, 0, "A2"), face.hline(0, 8, 8, "A1")
    hanging(g, "spoon_cord", 3.6, 2, role="L", top=9.0)
    spoon = g.piece("tasting_spoon", "TORSO", (-.5, 2, -.1), (1, 4, 1), pivot=(3.6, 9.0, -3.25), motion="flap_front")
    solid(spoon, "L", "smooth", 13903, 3)
    spoon.front.set(0, 3, "L2")
