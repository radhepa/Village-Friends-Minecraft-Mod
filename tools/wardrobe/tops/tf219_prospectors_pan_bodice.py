"""Prospector's Pan Bodice: a laced leather-edged bodice over a rolled-sleeve shirt, a wide round washing pan
slung on her back, a pouch of nuggets and a stoppered vial on the belt."""
from kit import roll
from kit_f07 import front_hung, prop
from kit_female import bodice, chemise, girdle, lacing

META = {
    "name": "Prospector's Pan Bodice",
    "gender": "female",
    "description": "A leather-edged laced bodice over a rolled-sleeve shirt, a wide round washing pan slung on her "
                   "back, a pouch of nuggets and a stoppered vial of gold dust on the belt.",
    "tags": ["work", "rugged"],
}


def build(g):
    chemise(g, "S", 3, "weave", 57901, neckline="v", sleeve_rows=(0, 5))
    roll(g, "S", 2.8, base=3)
    b = bodice(g, "P", "plain", 57902, rows=(1, 9), neckline="deep_square", edge="L2")
    lacing(b.front, 3, 3, 8, "ladder", lace="L3", under="P1", eyelet="M3")
    for face in b.sides:
        face.hline(0, face.w - 1, 9, "L2")
    for face in (b.right, b.left):
        face.vline(0, 1, 9, "L2"), face.vline(3, 1, 9, "L2")
    # The pan's carrying cord over the left shoulder and round under the right arm.
    j = g.part("jacket")
    j.top.vline(6, 0, 3, "L2")
    j.front.set(6, 0, "L2"), j.front.set(7, 1, "L2")
    for y in range(0, 7):
        j.back.set(1 + y // 2, y, "L1")
    girdle(g, "belt", 8.2, role="L", height=1)
    # The washing pan: a broad round dish built from two crossed slabs, a dark ring where the riffles run.
    for i, (w, h) in enumerate(((8, 6), (6, 8))):
        pan = prop(g, f"gold_pan_{i}", "TORSO", (-w / 2, -h / 2, 0), (w, h, 1), pivot=(.2, 4.6, 2.45 + .02 * i),
                   role="M", texture="smooth", seed=57903 + i, base=2)
        face = pan.back
        cx, cy = (w - 1) / 2, (h - 1) / 2
        for y in range(h):
            for x in range(w):
                d = max(abs(x - cx), abs(y - cy)) + min(abs(x - cx), abs(y - cy)) * .5
                face.set(x, y, "M1" if d > 3.4 else "M3" if d < 1.3 else "M0" if 2.2 < d < 2.9 else "M2")
    # A pouch of nuggets and a little stoppered vial on the belt.
    pouch = front_hung(g, "nugget_pouch", 2.8, (-1, 0, -1.5), (2, 3, 2), role="L", texture="leather", seed=57905,
                       top=8.6)
    pouch.front.hline(0, 1, 0, "L3"), pouch.top.fill("L1")
    for i, dx in enumerate((-.8, .2)):
        nug = front_hung(g, f"nugget_{i}", 2.8, (dx, -1, -1.2 + .4 * i), (1, 1, 1), role="A", seed=57906 + i,
                         base=3, top=8.6)
        nug.top.fill("A4")
    vial = front_hung(g, "dust_vial", -2.6, (-.5, 0, -1), (1, 2, 1), role="S", seed=57908, base=4, top=8.6)
    vial.front.set(0, 1, "A3")
    cork = front_hung(g, "dust_vial_cork", -2.6, (-.5, -1, -1), (1, 1, 1), role="L", seed=57909, base=2, top=8.6)
    cork.top.fill("L3")
