"""Breton Embroidered Chupenn Vest: a short open chupenn faced in black velvet and embroidery, over a close-buttoned waistcoat, with a plume fan on the back."""
from kit import SIDES, body, sleeves
from kit_male import embroider
from paint import fabric, grid, strip_fabric

META = {
    "name": "Breton Embroidered Chupenn Vest",
    "gender": "male",
    "description": "A short open chupenn faced with black velvet bands and bright embroidery, worn over a waistcoat closed with two close rows of buttons, a fan of embroidered plumes across the back.",
    "tags": ["fancy", "casual"],
}

PLUME_FAN = ["a.b..b.a",
             ".a.bb.a.",
             "..abba..",
             "...cc..."]


def build(g):
    vest = body(g, "S", "weave", 38281)
    f = vest.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "S4"), f.set(5, 0, "S4")                                   # the shirt collar
    for y in range(1, 11, 2):
        f.set(3, y, "M3"), f.set(4, y, "M3")                               # two close rows of buttons
    jacket = g.part("jacket")
    strip_fabric(jacket, "P", "velvet", 38282, 2)
    fabric(jacket.top, "P", "velvet", 38282, 3)
    fabric(jacket.bottom, "P", "velvet", 38283, 1)
    jf = jacket.front
    for y in range(12):
        for x in (2, 3, 4, 5):
            jf.clear(x, y)                                                 # the chupenn hangs open
        for x in (1, 6):
            jf.set(x, y, "A3" if y % 2 == 0 else "K2")                     # black velvet facing, embroidered
        jf.set(0, y, "M3" if y % 3 == 1 else jf.get(0, y))
        jf.set(7, y, "M3" if y % 3 == 1 else jf.get(7, y))
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "K2")
    embroider(jacket.back, 10, "dots", "A3", x0=0)
    grid(jacket.back, 0, 1, PLUME_FAN, {"a": "A3", "b": "M3", "c": "A1"})
    jacket.back.hline(0, 7, 6, "K2")
    sleeves(g, "P", "velvet", 38284, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for y in (8, 9, 10):
            arm.strip.hline(0, arm.strip.w - 1, y, "K2")
        embroider(arm.strip, 9, "dots", "A3")
        arm.strip.hline(0, arm.strip.w - 1, 7, "A2")
