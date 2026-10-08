"""Mushroom Gatherer's Moss-Green Shawl: a fringed knitted triangle shawl over a plain kirtle, its point down
her back and its ends crossed over the breast, with a little basket of red-capped mushrooms at the hip."""
from kit import body, sleeves
from kit_f07 import front_hung, prop, wicker_box
from kit_female import neck
from paint import fabric, k

META = {
    "name": "Mushroom Gatherer's Moss-Green Shawl",
    "gender": "female",
    "description": "A fringed knitted triangle shawl with its point down her back and its ends crossed over the "
                   "breast, and a little basket of speckled mushroom caps at her hip.",
    "tags": ["casual", "knit"],
}


def build(g):
    b = body(g, "S", "weave", 57501)
    neck(b.front, "round", "S", 2, edge="S3")
    sleeves(g, "S", "weave", 57502, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 11, "S1")
    j = g.part("jacket")
    # The shawl's ends crossing over the breast, knitted, two texels wide.
    for y in range(0, 8):
        for x0, lit in ((y - 1, True), (6 - y, False)):
            for dx in (0, 1, 2):
                x = x0 + dx
                if 0 <= x < 8:
                    edge = dx == (0 if lit else 2)
                    j.front.set(x, y, "P3" if edge else "P1" if dx == 1 and (y % 2) else "P2")
    j.front.set(3, 3, "P1"), j.front.set(4, 4, "P1")
    for face in (j.right, j.left):
        fabric(face, "P", "knit", 57503, 2, 0, 0, 4, 3)
    fabric(j.back, "P", "knit", 57504, 2, 0, 0, 8, 2)
    for face in (j.right, j.left, j.back, j.front):
        face.hline(0, face.w - 1, 8, "L1")                          # a plain belt where the ends tuck in
    j.front.set(4, 8, "L3")
    wrap = prop(g, "shawl_wrap", "TORSO", (-5, 0, -3), (10, 2, 6), pivot=(0, -.5, .1), role="P", texture="knit",
                seed=57505, base=2, inflate=.05)
    fabric(wrap.top, "P", "knit", 57505, 3)
    # The point down her back, stepped in knitted rows with a fringe on every edge.
    for i, (w, y) in enumerate(((10, 1.4), (8, 3.4), (6, 5.4), (4, 7.4), (2, 9.4))):
        step = prop(g, f"shawl_point_{i}", "TORSO", (-w / 2, 0, 0), (w, 2, 1), pivot=(0, y, 2.3), role="P",
                    texture="knit", seed=57506 + i, base=2, edge=False)
        for x in range(w):
            step.back.set(x, 1, "P1" if x % 2 else "P3")
        step.back.hline(0, w - 1, 0, "P2")
        if w > 2:
            step.back.set(0, 0, "P3"), step.back.set(w - 1, 0, "P3")
    # A small round basket of mushrooms on the left hip.
    basket = front_hung(g, "mushroom_basket", 3.4, (-2, 0, -3), (4, 3, 3), role="L", seed=57511, top=8.8)
    wicker_box(basket, "L", 2, 57511)
    for i, (dx, dz) in enumerate(((-1.6, -2.6), (.1, -1.6))):
        cap = front_hung(g, f"mushroom_cap_{i}", 3.4, (dx, -1, dz), (2, 1, 2), role="A", seed=57512 + i, top=8.8,
                         base=2)
        cap.top.fill("A2"), cap.top.set(0, 0, "S4"), cap.top.set(1, 1, "S4")
        for face in cap.sides:
            face.set(0, 0, "A3")
