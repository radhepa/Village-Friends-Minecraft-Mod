"""Laced Sleeveless Overdress: a sleeveless overdress ladder-laced down the front, its skirts parted at the knee over the underdress."""
from kit import SIDES, body
from kit_female import lacing, neck, over_panel
from paint import fabric, strip_fabric

META = {
    "name": "Laced Sleeveless Overdress",
    "gender": "female",
    "description": "A sleeveless wool overdress ladder-laced down the front, its knee-length skirts parted at the centre, over a plain long-sleeved underdress.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 60320, base=3)
    neck(b.front, "square", "S", 3)
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 60321 + (side == "left"), 3, 0, 11)
        fabric(arm.top, "S", "weave", 60323, 4)
        arm.strip.hline(0, 15, 10, "S2"), arm.strip.hline(0, 15, 11, "S4")
        arm.front.vline(2, 1, 9, "S2")
    j = g.part("jacket")
    strip_fabric(j, "P", "weave", 60324, 2, 0, 11)
    for x in (0, 1, 6, 7):
        j.top.vline(x, 0, 3, "P3")                                     # the shoulder straps
    for face in (j.right, j.left):
        for y in range(0, 4):
            for x in range(4):
                face.clear(x, y)
        face.hline(0, 3, 4, "P3")                                      # deep armholes
    neck(j.front, "deep_square", "P", 2, edge="P3")
    for x in (2, 3, 4, 5):
        j.back.clear(x, 0)
    j.back.hline(2, 5, 1, "P3")
    lacing(j.front, 3, 3, 9, "ladder", lace="A3", under="S2", eyelet="M3")
    for face in (j.front, j.back):
        face.vline(1, 4, 11, "P1"), face.vline(6, 4, 11, "P1")
    j.back.vline(3, 2, 11, "P1"), j.back.vline(4, 2, 11, "P3")
    # The overdress skirts: parted in front, whole behind.
    for name, x in (("skirt_front_right", -2.6), ("skirt_front_left", 2.6)):
        face = over_panel(g, name, 8, "P", "weave", 60325, 2, width=4, top=9.0, x=x)
        inner = 3 if x < 0 else 0
        face.vline(inner, 0, 7, "A2")                                  # the bound opening
        face.vline(1 if x < 0 else 2, 2, 6, "P1")
        face.hline(0, 3, 7, "P1")
    back = over_panel(g, "skirt_back", 9, "P", "weave", 60326, 2, width=10, top=9.0, back=True)
    for x in (2, 5, 8):
        back.vline(x, 2, 7, "P1")
    back.hline(0, 9, 8, "P1")
