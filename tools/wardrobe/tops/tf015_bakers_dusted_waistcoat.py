"""Baker's Dusted Waistcoat: a buttoned waistcoat with a floury handprint, over chemise sleeves bunched up the arm."""
from kit_female import arm_rings, buttons, chemise, neck
from paint import fabric, grid, rnd, solid, strip_fabric

META = {
    "name": "Baker's Dusted Waistcoat",
    "gender": "female",
    "description": "A buttoned waistcoat marked with a floury handprint, chemise sleeves bunched above the elbow, dusty forearms.",
    "tags": ["work", "casual"],
}

HAND = [".a.a.", ".aaaa", "aaaa.", ".aaa.", "..a.."]


def build(g):
    chemise(g, "S", 3, "weave", 11501, neckline="v", sleeve_rows=(0, 5))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in range(6, 12):
            for x in range(16):
                if rnd(x, y, 11502) < .2:
                    arm.strip.set(x, y, "S4")                          # flour up to the elbow
    for box in arm_rings(g, "bunched_sleeve", 1.6, 2, 5, inflate=.1):
        solid(box, "S", "weave", 11503, 3)
        for face in box.sides:
            for x in range(1, face.w, 2):
                face.vline(x, 0, 1, "S2")
    j = g.part("jacket")
    strip_fabric(j, "P", "weave", 11504, 2, 0, 10)
    fabric(j.top, "P", "weave", 11504, 3)
    neck(j.front, "deep_v", "P", 2)
    buttons(j.front, 3, 4, 10, "M3", step=2, placket="P1")
    j.front.vline(4, 4, 10, "P3")
    for face in j.sides:
        face.hline(0, face.w - 1, 10, "P1")
    grid(j.front, 4, 5, HAND, {"a": "S4"})                           # a floury handprint
    for y in range(7, 11):
        for x in range(8):
            if rnd(x, y, 11505) < .15:
                j.front.set(x, y, "S4")
    j.back.vline(3, 1, 10, "P1"), j.back.vline(4, 1, 10, "P1")
    j.back.hline(2, 5, 8, "A2")                                       # the back half-belt
