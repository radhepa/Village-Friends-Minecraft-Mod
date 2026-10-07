"""Frogged Riding Jacket: a short fitted riding jacket closed with corded frogs, turned-back cuffs and a linen jabot."""
from kit import body, sleeves
from kit_female import over_flaps
from paint import solid

META = {
    "name": "Frogged Riding Jacket",
    "gender": "female",
    "description": "A short fitted riding jacket closed with corded frogs, deep turned-back cuffs, a peplum and a linen jabot.",
    "tags": ["tailored", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 15801)
    for y in range(2, 10, 2):
        b.front.hline(1, 6, y, "M3")                                 # corded frogs
        b.front.set(0, y, "M2"), b.front.set(7, y, "M2")
        b.front.set(3, y, "M4"), b.front.set(4, y, "M4")
    b.back.vline(2, 2, 11, "P1"), b.back.vline(5, 2, 11, "P1")
    sleeves(g, "P", "twill", 15802, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in (8, 9):
            arm.strip.hline(0, 15, y, "S3")
        arm.strip.hline(0, 15, 10, "S4")
        arm.front.set(1, 8, "M3")
    jabot = g.piece("jabot", "TORSO", (-1.5, 0, -.5), (3, 4, 1), pivot=(0, -.6, -2.6))
    solid(jabot, "S", "plain", 15803, 4)
    for y in range(4):
        jabot.front.set(0 if y % 2 else 2, y, "S3")
    stock = g.piece("stock", "TORSO", (-4.5, -1.2, -2.6), (9, 1, 5), inflate=.08)
    solid(stock, "S", "plain", 15804, 4, edge=False)
    f, bk = over_flaps(g, "peplum", 2, "P", "twill", 15805, width=10, top=9.0)
    for face in (f, bk):
        face.hline(0, 9, 1, "M2")
        face.vline(5, 0, 1, "P0")
