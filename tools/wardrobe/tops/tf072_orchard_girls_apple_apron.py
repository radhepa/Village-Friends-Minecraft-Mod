"""Orchard Girl's Apple Apron: a bodice with pushed-up sleeves and a picking apron whose hem is buttoned up
to the waistband, making a deep pouch heaped with apples."""
from kit_female import OVER_FRONT, bodice, chemise, girdle, over_panel
from kit_f01 import produce
from paint import k, solid

META = {
    "name": "Orchard Girl's Apple Apron",
    "gender": "female",
    "description": "A bodice with sleeves pushed up and a picking apron buttoned up at the hem into a deep pouch heaped with apples.",
    "tags": ["work", "casual", "apron"],
    "covers_waist": True,
}

HINGE = (0, 8.6, OVER_FRONT)


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51440, neckline="scoop", sleeve_rows=(0, 7))
    for arm in arms:
        arm.strip.hline(0, 15, 6, "S4"), arm.strip.hline(0, 15, 7, "S2")      # pushed up in soft folds
        for x in range(1, 16, 4):
            arm.strip.set(x, 5, "S2")
    b = bodice(g, "P", "weave", 51441, rows=(2, 9), neckline="scoop", edge="P3", point=True)
    for y in range(3, 9):
        b.front.set(3, y, "P1"), b.front.set(4, y, "P3")
    for y in (4, 6, 8):
        b.front.set(3, y, "A2")                                       # ribbon ties down the front
    girdle(g, "apron_band", 8.0, role="S", base=2, height=1, buckle=None, texture="weave", wide=True)
    apron = over_panel(g, "apron", 3, "S", "twill", 51442, base=2, width=9, top=8.6)
    apron.hline(0, 8, 2, "S1")
    # The pouch: the apron's hem turned up and buttoned to the band, bulging with fruit.
    pouch = g.piece("apron_pouch", "TORSO", (-4, 1.4, -1.6), (8, 3, 2), pivot=HINGE, motion="flap_front", inflate=.08)
    solid(pouch, "S", "twill", 51443, 2)
    for f in pouch.sides:
        f.hline(0, f.w - 1, 0, "S3")
        for x in range(1, f.w, 3):
            f.vline(x, 1, f.h - 1, "S1")                              # the cloth dragged into folds by the weight
    pouch.front.set(0, 0, "M3"), pouch.front.set(7, 0, "M3")         # buttons holding the hem up
    pouch.top.fill("S1")
    for i, (x, y, z) in enumerate(((-2.6, .2, -1.3), (-.6, -.1, -.9), (1.5, .2, -1.4), (3.0, .4, -.7), (.4, .7, -2.0))):
        apple = produce(g, f"apple_{i}", "TORSO", HINGE, 2, role="A", base=2, stem="L1", motion="flap_front",
                        origin=(x - 1, y, z - 1), seed=51444 + i)
        apple.front.set(1, 1, k("A", 1))
    leaf = g.piece("apple_leaf", "TORSO", (-.4, -.2, -1.6), (2, 1, 1), pivot=HINGE, rotation=(0, 0, -25),
                   motion="flap_front")
    solid(leaf, "P", "plain", 51449, 3, edge=False)
