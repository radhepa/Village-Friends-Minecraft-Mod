"""Gardener's Sackcloth Bib: a rough sackcloth bib with seed packets in its pockets and a trowel hung at the hip."""
from kit import roll
from kit_female import chemise, hanging, over_panel
from paint import fabric, solid

META = {
    "name": "Gardener's Sackcloth Bib",
    "gender": "female",
    "description": "A rough sackcloth bib and apron with seed packets in the pockets, rolled sleeves and a trowel at the hip.",
    "tags": ["work", "apron", "casual"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 4, "weave", 14801, neckline="round", sleeve_rows=(0, 6))
    roll(g, "S", 3.4, base=4)
    j = g.part("jacket")
    fabric(j.front, "L", "rib", 14802, 3, 1, 2, 6, 10)
    for x in (1, 6):
        j.front.vline(x, 0, 1, "L2")
        j.top.vline(x, 0, 3, "L2")
    j.back.hline(0, 7, 9, "L2")
    for face in (j.right, j.left):
        face.hline(0, 3, 9, "L2")
    j.front.hline(2, 5, 4, "L1"), j.front.vline(2, 4, 7, "L1"), j.front.vline(5, 4, 7, "L1")
    j.front.set(3, 4, "A3"), j.front.set(4, 4, "P3")                 # seed packets in the pocket
    face = over_panel(g, "apron", 8, "L", "rib", 14803, base=3, width=8, top=9.0)
    face.hline(0, 7, 3, "L2"), face.vline(3, 3, 6, "L2")
    face.set(1, 3, "A3"), face.set(5, 3, "S4")
    hanging(g, "trowel_loop", -3.4, 2, role="L", top=9.0)
    blade = g.piece("trowel", "TORSO", (-1, 2, -.1), (2, 3, 1), pivot=(-3.4, 9.0, -3.25), motion="flap_front")
    solid(blade, "M", "smooth", 14804, 2)
    blade.front.set(0, 2, "M1"), blade.front.set(1, 0, "L3")
