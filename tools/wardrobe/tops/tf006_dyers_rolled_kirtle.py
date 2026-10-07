"""Dyer's Rolled Kirtle: a stained kirtle, chemise sleeves rolled high over dyed forearms, a stirring paddle on the back."""
from kit import body, roll
from kit_female import chemise, lacing, neck, splotch
from paint import fabric, line, solid

META = {
    "name": "Dyer's Rolled Kirtle",
    "gender": "female",
    "description": "A dye-splashed kirtle, sleeves rolled high over vat-stained forearms and a stirring paddle slung behind.",
    "tags": ["work"],
}


def build(g):
    chemise(g, "S", 3, "weave", 10601, neckline="slit", sleeve_rows=(0, 3), gather=False)
    roll(g, "S", .6, base=3)
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for x in range(16):
            for y in range(7 + (x % 3 == 0), 12):
                arm.strip.set(x, y, "A1" if (x + y) % 5 == 0 else "A2")     # forearms dyed to the elbow
    b = body(g, "P", "twill", 10602)
    neck(b.front, "slit", "P", 2)
    lacing(b.front, 3, 1, 4, "spiral", lace="L3", under="S3", eyelet=None)
    splotch(b.front, "A1", 10603, count=3, y0=6, y1=10)
    splotch(b.front, "A2", 10604, count=2, y0=8, y1=11)
    splotch(b.back, "A2", 10605, count=2, y0=7, y1=11)
    j = g.part("jacket")
    line(j.front, 7, 0, 1, 9, "L2")                        # the paddle's carrying strap
    line(j.back, 0, 0, 6, 9, "L2")
    j.top.vline(6, 0, 3, "L2")
    paddle = g.piece("paddle", "TORSO", (-.5, -7, -.5), (1, 13, 1), pivot=(.8, 5.6, 2.9), rotation=(0, 0, -28))
    solid(paddle, "L", "smooth", 10606, 3)
    blade = g.piece("paddle_blade", "TORSO", (-1, 6, -.5), (2, 3, 1), pivot=(.8, 5.6, 2.9), rotation=(0, 0, -28))
    solid(blade, "L", "smooth", 10607, 3)
    for face in blade.sides:
        face.hline(0, face.w - 1, 1, "A2"), face.hline(0, face.w - 1, 2, "A1")
