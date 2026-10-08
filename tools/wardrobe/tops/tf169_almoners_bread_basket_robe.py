"""Almoner's Bread-Basket Robe: a plain buttoned robe with a broad linen collar and turned linen cuffs,
and a wicker basket of round loaves carried in the crook of her left arm for the day's dole."""
from kit import body, sleeves
from kit_female import buttons, collar_flat, girdle, neck
from paint import fabric, solid


META = {
    "name": "Almoner's Bread-Basket Robe",
    "gender": "female",
    "description": "A plain buttoned robe with a broad linen collar and cuffs, a wicker basket of round loaves on her arm.",
    "tags": ["holy", "simple", "work"],
}


def wicker(face):
    """Basketwork: upright stakes with the weavers passing over and under them."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, "L3" if (x + y) % 2 == 0 else "L2")
    face.hline(0, face.w - 1, 0, "L4")
    face.hline(0, face.w - 1, face.h - 1, "L1")


def build(g):
    b = body(g, "P", "weave", 55261, base=2)
    neck(b.front, "round", "P", 2)
    buttons(b.front, 4, 3, 11, "P3", step=2, placket="P1")
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P1"), face.vline(6, 3, 11, "P1")
    for arm in sleeves(g, "P", "weave", 55262, base=2, rows=(0, 11)):
        arm.strip.hline(0, 15, 9, "S4"), arm.strip.hline(0, 15, 10, "S3"), arm.strip.hline(0, 15, 11, "S2")
    collar_flat(g, "linen_collar", "S", 4, edge="S2")
    girdle(g, "girdle", 8.2, role="L", base=1, height=1, buckle="M")
    # The basket rides in the crook of the left arm, in front of the forearm.
    basket = g.piece("bread_basket", "LEFT_ARM", (-1.5, 4.5, -5.6), (6, 3, 4))
    for face in basket.sides:
        wicker(face)
    fabric(basket.bottom, "L", "plain", 55263, 1)
    fabric(basket.top, "S", "plain", 55264, 3)                       # a cloth laid under the loaves
    for i, x in enumerate((-1.2, 1.4)):
        loaf = g.piece(f"loaf_{i}", "LEFT_ARM", (x, 3.5, -5.0), (2, 1, 2), inflate=.1)
        solid(loaf, "L", "plain", 55265 + i, 3, edge=False)
        loaf.top.fill("L4"), loaf.top.set(0, 0, "L3")
        for face in loaf.sides:
            face.set(1, 0, "L4")
    round_loaf = g.piece("loaf_2", "LEFT_ARM", (0, 3.0, -4.0), (2, 2, 2), inflate=.05)
    solid(round_loaf, "L", "plain", 55267, 3, edge=False)
    round_loaf.top.fill("L4"), round_loaf.front.set(0, 0, "L4"), round_loaf.front.hline(0, 1, 1, "L2")
    # The handle arches up over the forearm.
    for name, x in (("basket_handle_r", -1.5), ("basket_handle_l", 3.5)):
        post = g.piece(name, "LEFT_ARM", (x, 1.5, -3.1), (1, 3, 1))
        solid(post, "L", "plain", 55268, 2, edge=False)
    bar = g.piece("basket_handle_top", "LEFT_ARM", (-1.5, .5, -3.1), (6, 1, 1))
    solid(bar, "L", "plain", 55269, 2, edge=False)
    bar.front.hline(0, 5, 0, "L3")
