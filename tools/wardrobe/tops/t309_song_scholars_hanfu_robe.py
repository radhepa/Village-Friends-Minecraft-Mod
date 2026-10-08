"""Song Scholar's Hanfu Robe: a long crossed-collar robe bordered in black, with deep hanging sleeves, a sash with long ends and a jade pendant."""
from kit import SIDES, body, sleeves
from kit_male import arm_blk, sash
from kit_m08 import coat_skirt, crossed_collar, hanging_tail

META = {
    "name": "Song Scholar's Hanfu Robe",
    "gender": "male",
    "description": "A long scholar's robe with a crossed collar closing to the right, every edge bordered in black, deep hanging sleeves, a silk sash with long ends and a jade pendant.",
    "tags": ["scholarly", "robe", "fancy"],
    "locked_to": "b309_hanfu_wide_trousers_and_cloth_shoes",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 38521)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    crossed_collar(f, "K2", "P0", x_top=5, y_end=7, width=2)
    f.set(2, 0, "K2"), f.set(1, 0, "K1")                                   # the under collar at the neck
    b.back.hline(1, 6, 0, "K2")
    b.back.vline(3, 2, 11, "P1")
    sleeves(g, "P", "weave", 38522, rows=(0, 10))
    for i, side in enumerate(SIDES):
        s = arm_blk(g, f"{side}_hanging_sleeve", side, 1.0, (5, 9, 7), "P", 2, "weave", 38523 + i,
                    dx=-.5 if side == "right" else .5, inflate=.05)
        for face in s.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 8, "K2")                              # black border at the opening
            face.set(0, 7, "P1"), face.set(face.w - 1, 7, "P1")
        s.front.vline(2, 1, 6, "P1"), s.back.vline(2, 1, 6, "P1")
        s.bottom.fill("K2")
        s.bottom.rect(1, 2, 3, 3, "P0")
    band = sash(g, "dai_sash", "S", y=8.4, height=2, texture="smooth", seed=38525, tails=())
    for face in band.sides:
        face.hline(0, face.w - 1, 1, "S2")
    for j, x in enumerate((-.6, .6)):
        end = hanging_tail(g, f"dai_end_{j}", (x, 10.4, -3.4), (1, 8, 1), "S", "smooth", 38526 + j, motion="flap_front")
        end.front.set(0, 7, "S1")
    jade = hanging_tail(g, "jade_pendant", (2.2, 10.4, -3.4), (1, 4, 1), "A", "smooth", 38528, motion="flap_front")
    for face in jade.sides:
        face.vline(0, 0, 1, "K1")                                          # the cord
        face.set(0, 2, "A3"), face.set(0, 3, "A2")
    front, back, sides = coat_skirt(g, "hanfu_skirt", 11, "P", "weave", 38529, top=10.8, hem="K2")
    front.vline(0, 0, 10, "K2"), front.vline(1, 0, 10, "P0")                # the overlap down the right side
    back.vline(4, 1, 9, "P1")
