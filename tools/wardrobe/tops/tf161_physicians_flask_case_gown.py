"""Physician's Flask-Case Gown: a long closed gown with a buttoned throat, and the physician's wicker
urine-flask case hung at the hip on a cross-body strap."""
from kit import body, sleeves
from kit_female import girdle, neck, over_flaps
from kit_f05 import dangle
from paint import fabric, k, line

META = {
    "name": "Physician's Flask-Case Gown",
    "gender": "female",
    "description": "A long sober gown buttoned at the throat, banded cuffs, and a lidded wicker flask case slung at the hip.",
    "tags": ["scholarly", "robe"],
    "covers_waist": True,
}


def wicker(face, a="L3", b="L1", c="L2"):
    """Basketwork: alternating over-under rows of short stakes."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, a if (x + (y // 1)) % 2 == 0 else (b if y % 2 else c))


def build(g):
    b = body(g, "P", "twill", 55001, base=2)
    neck(b.front, "round", "P", 2, edge="P3")
    for y in (1, 2, 3, 4):
        b.front.set(4, y, "M3" if y % 2 else "P1")                    # buttoned throat
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P1"), face.vline(6, 2, 11, "P1")
    for arm in sleeves(g, "P", "twill", 55002, rows=(0, 11)):
        arm.strip.hline(0, 15, 9, "S3"), arm.strip.hline(0, 15, 10, "S4"), arm.strip.hline(0, 15, 11, "S2")
        arm.front.vline(1, 2, 8, "P1")
    # The strap: over the left shoulder, across the breast to the right hip.
    j = g.part("jacket")
    for dx, key in ((0, "L3"), (1, "L1")):
        line(j.front, 7 - dx, 0, 0, 7 - dx, key)
        line(j.back, 0 + dx, 0, 7, 7 - dx, key)
    j.top.vline(1, 0, 3, "L2"), j.left.hline(0, 3, 0, "L2")
    girdle(g, "girdle", 8.0, role="L", base=1, height=1, buckle="M")
    f, bk = over_flaps(g, "gown", 12, "P", "twill", 55003, width=10, top=9.0, hem="P0")
    for face in (f, bk):
        face.vline(2, 1, 10, "P1"), face.vline(7, 1, 10, "P1"), face.vline(8, 2, 9, "P3")
    f.vline(4, 0, 11, "P1"), f.vline(5, 0, 11, "P3")                  # the gown's closed front seam
    # The flask case rides the stride at the right hip: lid, wicker body, the flask's glass neck.
    case = dangle(g, "flask_case", -2.6, .6, (3, 5, 2), "L", 2, "leather", top=8.6, seed=55004)
    for face in case.sides:
        wicker(face)
        face.hline(0, face.w - 1, 0, "L1")
        face.hline(0, face.w - 1, face.h - 1, "L0")
    case.bottom.fill("L0")
    lid = dangle(g, "flask_lid", -2.6, -.6, (3, 1, 2), "L", 1, "leather", top=8.6, seed=55005, edge=False)
    lid.top.fill("L2"), lid.front.set(1, 0, "M3")
    neck_ = dangle(g, "flask_neck", -2.6, -1.6, (1, 1, 1), "S", 4, "plain", top=8.6, seed=55006, edge=False)
    neck_.top.fill("S3")
    fabric(case.top, "L", "plain", 55007, 1)
    # A small physician's purse on the girdle's other side.
    purse = dangle(g, "physic_purse", 2.6, .2, (2, 2, 1), "A", 2, "plain", top=8.6, seed=55008)
    purse.front.hline(0, 1, 0, "A3"), purse.front.set(1, 1, k("M", 3))
