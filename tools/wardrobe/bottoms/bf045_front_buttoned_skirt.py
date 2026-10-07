"""Front-Buttoned Skirt: a sturdy dark skirt buttoned down the front placket, with slit pockets and tall boots."""
from kit_female import buttons, shoes, skirt

META = {
    "name": "Front-Buttoned Skirt",
    "gender": "female",
    "description": "A sturdy dark skirt buttoned down a front placket, with slit hip pockets, over tall walking boots.",
    "tags": ["tailored", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 14511, base=1, top=9.8, length=10, folds=False)
    f = s.front.front
    f.vline(4, 1, 9, "P0"), f.vline(5, 1, 9, "P2")
    buttons(f, 5, 1, 9, "M3", step=2)
    f.hline(1, 2, 2, "P0"), f.hline(7, 8, 2, "P0")                   # slit pockets
    s.back.back.vline(4, 2, 9, "P0")
    s.hem("P0")
    shoes(g, "boot", "L", 2, top=8)
