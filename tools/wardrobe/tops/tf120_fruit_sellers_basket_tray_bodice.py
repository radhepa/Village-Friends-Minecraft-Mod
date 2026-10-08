"""Fruit Seller's Basket-Tray Bodice: a sweetheart-necked laced bodice with ruffled elbow sleeves and a wide
shallow wicker tray of apples and pears carried at the waist on straps from both shoulders."""
from kit_female import arm_rings, bodice, chemise, lacing
from kit_f03 import basket
from paint import k, solid

META = {
    "name": "Fruit Seller's Basket-Tray Bodice",
    "gender": "female",
    "description": "A sweetheart bodice with ruffled elbow sleeves and a wide wicker tray of apples and pears carried at the waist on shoulder straps.",
    "tags": ["casual", "work", "whimsical"],
}

SEED = 53300
TRAY = (0, 6.8, -4.3)
FRUIT = [(-2.2, -3.5, "A", 6.2), (0, -3.4, "S", 6.0), (2.2, -3.6, "A", 6.3), (-1.2, -5.3, "S", 6.4), (1.2, -5.2, "A", 6.2)]


def build(g):
    body, arms = chemise(g, "S", 3, "weave", SEED, neckline="sweetheart", sleeve_rows=(0, 5))
    for box in arm_rings(g, "sleeve_ruffle", 3.0, 2, 5, inflate=.12):
        solid(box, "S", "weave", SEED + 1, 3, edge=False)
        for f in box.sides:
            for x in range(f.w):
                f.set(x, 0, k("S", 4 if x % 2 else 2))
                f.set(x, 1, k("S", 3 if x % 2 else 1))
        box.bottom.fill("S1")
    b = bodice(g, "P", "weave", SEED + 2, rows=(2, 9), neckline="sweetheart", point=True, edge="A2")
    lacing(b.front, 3, 3, 8, "x", lace="A3", under="S3", eyelet="M3")
    # The tray straps run from both shoulders down to the tray's back corners.
    for face, xs in ((b.front, (0, 7)), (b.back, (1, 6))):
        for x in xs:
            face.vline(x, 0, 7 if face is b.front else 9, "L2")
    for x in (0, 7):
        b.top.vline(x, 0, 3, "L2")
    tray = basket(g, "fruit_tray", "TORSO", (-3.5, 0, -2), (7, 3, 4), pivot=TRAY, role="L", base=2, inside="L1")
    for f in tray.sides:
        f.hline(0, f.w - 1, 2, "L1")
    tray.front.set(0, 0, "L4"), tray.front.set(6, 0, "L4")
    for i, (x, z, role, y) in enumerate(FRUIT):
        fruit = g.piece(f"fruit_{i}", "TORSO", (-1, -1, -1), (2, 2, 2), pivot=(x, y, z))
        base = 2 if role == "A" else 3
        solid(fruit, role, "plain", SEED + 3 + i, base, edge=False)
        for f in fruit.sides:
            f.set(0, 0, k(role, base + 2)), f.set(1, 1, k(role, base - 1))   # a shine and a shadow on each
        fruit.top.fill(k(role, base + 1))
        fruit.top.set(1, 0, "L1")                                     # the stalk
