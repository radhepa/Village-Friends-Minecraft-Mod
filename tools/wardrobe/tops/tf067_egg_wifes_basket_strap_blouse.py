"""Egg Wife's Basket-Strap Blouse: a full blouse under a short open waistcoat, a padded carrying strap across
the chest and a cloth-lined basket of eggs hung on her left forearm."""
from kit_female import chemise
from kit_f01 import produce, wicker
from paint import fabric, k, solid

META = {
    "name": "Egg Wife's Basket-Strap Blouse",
    "gender": "female",
    "description": "A full blouse under a short open waistcoat, a padded strap across the chest and a cloth-lined basket of eggs carried on her forearm to market.",
    "tags": ["casual", "simple"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51240, neckline="round", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4"), arm.strip.hline(0, 15, 11, "S3")
    # The short open waistcoat: two front panels and a full back, ending at the waist.
    j = g.part("jacket")
    for x0 in (0, 6):
        fabric(j.front, "P", "twill", 51241, 2, x0, 0, 2, 9)
    j.front.vline(1, 0, 8, "P3"), j.front.vline(6, 0, 8, "P1")
    j.front.hline(0, 1, 8, "P1"), j.front.hline(6, 7, 8, "P1")
    fabric(j.back, "P", "twill", 51242, 2, 0, 0, 8, 9)
    j.back.hline(0, 7, 8, "P1")
    for face in (j.right, j.left):
        fabric(face, "P", "twill", 51243, 2, 0, 0, 4, 9)
        face.hline(0, 3, 8, "P1")
    fabric(j.top, "P", "twill", 51244, 3)
    for y in (2, 4, 6):
        j.front.set(1, y, "M3")                                       # horn buttons on the open edge
    # The padded strap from the right shoulder across to the left hip, quilted in short stitches.
    for y in range(0, 12):
        x = round(y * 0.62)
        j.front.set(x, y, "L2" if y % 2 else "L3")
        j.front.set(x + 1, y, "L1")
    for y in range(0, 7):
        j.back.set(7 - round(y * 1.0), y, "L2")
    j.top.set(0, 2, "L2"), j.top.set(0, 3, "L2")
    # The egg basket on her left forearm: wicker body, a bound rim, a bow handle and eggs on a cloth.
    basket = g.piece("egg_basket", "LEFT_ARM", (3.1, 6.0, -2.0), (4, 3, 4))
    for f in basket.sides:
        wicker(f, "L", 2, offset=f.x0)
    basket.bottom.fill("L1"), basket.top.fill("S2")
    rim = g.piece("egg_basket_rim", "LEFT_ARM", (3.1, 5.6, -2.0), (4, 1, 4), inflate=.12)
    solid(rim, "L", "smooth", 51245, 3, edge=False)
    rim.top.fill("S3")
    for name, x in (("egg_basket_bow_inner", 3.1), ("egg_basket_bow_outer", 6.1)):
        post = g.piece(name, "LEFT_ARM", (x, 2.6, -.5), (1, 3, 1))
        solid(post, "L", "smooth", 51246, 3, edge=False)
    bow = g.piece("egg_basket_bow_top", "LEFT_ARM", (3.1, 1.8, -.5), (4, 1, 1))
    solid(bow, "L", "smooth", 51247, 3, edge=False)
    for i, (x, y, z) in enumerate(((4.2, 4.7, -1.2), (5.7, 4.9, -1.0), (4.8, 4.6, 1.2))):
        egg = produce(g, f"egg_{i}", "LEFT_ARM", (x, y, z), 2, role="S", base=4, stem=None, seed=51248 + i)
        for f in egg.sides:
            f.set(0, 0, "S4"), f.set(1, 0, "S4"), f.set(1, 1, "S3"), f.set(0, 1, "S4")
        egg.top.fill("S4")
    # A folded cloth under the eggs, its corner hanging over the rim.
    cloth = g.piece("egg_basket_cloth", "LEFT_ARM", (5.6, 5.6, -2.2), (1, 2, 1))
    solid(cloth, "A", "plain", 51253, 2, edge=False)
    cloth.front.set(0, 1, k("A", 3))
