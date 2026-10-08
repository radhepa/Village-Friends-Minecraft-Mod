"""Pardoner's Relic-Hung Coat: a buttoned knee coat pinned all over with pilgrim badges, little gilt reliquaries hung on a cord across the breast, and a wallet stuffed so full his hood bulges out of it."""
from kit import belt, body, collar, flaps, sleeves
from kit_male import blk, buttons
from kit_m05 import strap
from paint import grid, solid

META = {
    "name": "Pardoner's Relic-Hung Coat",
    "gender": "male",
    "description": "A travelling pardoner's buttoned knee coat pinned all over with pewter pilgrim badges, three little gilt reliquaries hung on a cord across his breast, and a wallet crammed so full of pardons that his hood bulges out of it.",
    "tags": ["holy", "casual", "whimsical"],
    "covers_waist": True,
}

SHELL = ["a.a", "aaa"]
FLASK = [".a.", "aaa"]
KEY = ["aa", ".a"]


def badges(face, spots):
    for (x, y), glyph in spots:
        grid(face, x, y, glyph, {"a": "M3"})
        face.set(x + len(glyph[0]) // 2, y, "M4")


def build(g):
    b = body(g, "P", "twill", 35280)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.vline(4, 1, 11, "P1")
    buttons(b.front, 3, 1, 11, 2, "M2")
    sleeves(g, "P", "twill", 35281, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.front.set(1, 9, "M3"), arm.front.set(2, 9, "M3")
        over = g.part(f"{side}_sleeve")                                      # badges up the sleeves
        badges(over.front, [((1, 1), SHELL)])
        badges(over.right if side == "right" else over.left, [((0, 3), FLASK), ((2, 0), KEY)])
    stand = collar(g, "collar", "P", "twill", base=2, height=1, y=-.5)
    stand.front.set(4, 0, "P0")
    jacket = g.part("jacket")
    badges(jacket.front, [((0, 1), SHELL), ((1, 4), FLASK), ((0, 7), KEY)])
    badges(jacket.back, [((1, 1), SHELL), ((5, 2), FLASK), ((2, 5), KEY), ((5, 6), SHELL)])
    strap(g, "L2", "L1", from_side="left", low=9)
    belt(g, "belt", 9.6, height=1)
    # Three little gilt reliquaries on the cord: a casket, a crystal phial and a tiny house-shrine.
    for i, (x, y, w, h) in enumerate(((1.9, 2.4, 2, 2), (.2, 4.9, 1, 2), (-1.5, 6.6, 2, 2))):
        rel = blk(g, f"reliquary_{i}", (x, y, -2.75), (w, h, 1), "M", 3, "smooth", 35282 + i, edge=False)
        rel.front.fill("M2")
        if w == 2:
            rel.front.set(0, 0, "M4"), rel.front.set(1, h - 1, "A3")
        else:
            rel.front.set(0, 0, "S4"), rel.front.set(0, 1, "A3")
    roof = blk(g, "reliquary_roof", (-1.5, 6.1, -2.75), (2, 1, 1), "A", 2, "plain", 35285, edge=False, rotation=(0, 0, 0))
    roof.front.set(0, 0, "M4")
    # The wallet at the right hip, his hood stuffed in on top.
    wallet = blk(g, "wallet", (-2.6, 9.4, -2.6), (3, 3, 2), "L", 2, "leather", 35286, motion="flap_front")
    wallet.front.hline(0, 2, 0, "L3"), wallet.front.set(1, 1, "M3")
    hood = g.piece("wallet_hood", "TORSO", (-1.5, -1, -.5), (3, 1, 1), pivot=(-2.6, 9.4, -2.6), motion="flap_front")
    solid(hood, "P", "weave", 35287, 3, edge=False)
    hood.front.set(1, 0, "P1")
    tip = g.piece("wallet_hood_tip", "TORSO", (.5, -2, -.5), (1, 1, 1), pivot=(-2.6, 9.4, -2.6), motion="flap_front")
    solid(tip, "P", "weave", 35288, 3, edge=False)
    front, back = flaps(g, "coat_skirt", 6, "P", "twill", 35289, top=10.6, hem="P1")
    front.vline(4, 0, 5, "P1")
    buttons(front, 3, 0, 4, 2, "M2")
    badges(back, [((5, 1), SHELL)])
