"""Prioress's Rosary-Girdle Habit: a habit of fine dark wool with fur-turned cuffs, a crisply pleated
white barbe under the chin, a long black veil with a white under-veil edge, a girdle strung as a rosary
of coral beads gauded with gold that loops down to a tassel, and a gold brooch on the breast."""
from kit import body, sleeves
from kit_female import arm_rings, fur, hanging
from paint import fabric, solid

META = {
    "name": "Prioress's Rosary-Girdle Habit",
    "gender": "female",
    "description": "A fine dark habit with a pleated white barbe, a long veil, fur cuffs, a gold brooch and a rosary worn as a girdle.",
    "tags": ["holy", "robe", "fancy"],
    "locked_to": "bf167_prioress_fine_habit_skirt",
    "covers_waist": True,
}


def beads(face, y, coral="A3", shade="A1", gaud="M4", every=5):
    """A string of round beads across a face row: coral beads, every fifth a gold gaud."""
    for x in range(face.w):
        face.set(x, y, gaud if x % every == every - 1 else (coral if x % 2 == 0 else shade))


def build(g):
    b = body(g, "P", "velvet", 55221, base=1)
    for face in (b.front, b.back):
        face.vline(1, 4, 11, "P0"), face.vline(6, 4, 11, "P0")
        face.vline(3, 5, 11, "P2")
    for arm in sleeves(g, "P", "velvet", 55222, base=1, rows=(0, 11)):
        arm.strip.vline(2, 2, 8, "P0"), arm.strip.vline(10, 2, 8, "P0")
    for box in arm_rings(g, "fur_cuff", 7.6, 2, 5, inflate=.08):
        for face in box.faces:
            fur(face, "L", 55223, 3)
    # The barbe: white linen pleated from chin to breast, over a white wimple ring.
    wimple = g.piece("wimple", "TORSO", (-4.5, -1.4, -2.6), (9, 2, 5), inflate=.12)
    solid(wimple, "S", "plain", 55224, 4, edge=False)
    barbe = g.piece("barbe", "TORSO", (-3.5, 0, 0), (7, 5, 1), pivot=(0, -.6, -2.85))
    solid(barbe, "S", "plain", 55225, 4)
    for x in range(7):
        barbe.front.vline(x, 1, 4, "S3" if x % 2 else "S4")              # crisp pleats
    barbe.front.hline(0, 6, 4, "S2")
    # The long black veil with the white under-veil showing at its edge.
    veil = g.piece("veil", "TORSO", (-4.5, 0, 0), (9, 10, 1), pivot=(0, -.6, 2.45), rotation=(5, 0, 0))
    solid(veil, "K", "plain", 55226, 2)
    veil.back.vline(0, 0, 9, "S4"), veil.back.vline(8, 0, 9, "S4")
    veil.back.vline(3, 1, 9, "K1"), veil.back.vline(5, 1, 9, "K1")
    veil.back.hline(1, 7, 9, "K1")
    # The gold brooch on the breast, a coral stone at its heart.
    brooch = g.piece("brooch", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(0, 5.6, -2.55), inflate=.04)
    solid(brooch, "M", "smooth", 55227, 3, edge=False)
    brooch.front.set(0, 0, "M4"), brooch.front.set(1, 1, "A3")
    # The rosary girdle round the waist, and its loop of beads hanging down the front to a tassel.
    ring = g.piece("rosary_girdle", "TORSO", (-4.6, 7.6, -2.6), (9, 1, 5), inflate=.06)
    solid(ring, "A", "plain", 55228, 2, edge=False)
    for face in ring.sides:
        beads(face, 0)
    for i, (x, n) in enumerate(((-1.6, 8), (-0.6, 7))):
        loop = hanging(g, f"rosary_loop_{i}", x, n, role="A", base=2, top=8.6)
        for y in range(n):
            key = "M4" if y % 5 == 4 else ("A3" if y % 2 == 0 else "A1")
            loop.front.set(0, y, key), loop.back.set(0, y, key)
    tassel = g.piece("rosary_tassel", "TORSO", (-1, 8, -.2), (2, 2, 1), pivot=(-1.1, 8.6, -3.25), motion="flap_front")
    solid(tassel, "M", "plain", 55229, 3, edge=False)
    tassel.front.set(0, 1, "M1"), tassel.front.set(1, 0, "M4")
    fabric(tassel.top, "M", "plain", 55229, 4)
