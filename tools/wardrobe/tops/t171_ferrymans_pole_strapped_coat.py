"""Ferryman's Pole-Strapped Coat: a knee-length wool coat crossed by a pole strap that ends in a leather pole socket,
a padded shoulder for bracing the punt pole, a coin pouch and a brass toll token."""
from kit import belt, body, collar, flaps, pouch, sleeves
from kit_male import arm_blk, blk
from paint import k, line, solid

META = {
    "name": "Ferryman's Pole-Strapped Coat",
    "gender": "male",
    "description": "A knee-length wool coat crossed by a leather pole strap ending in a pole socket at the hip, a padded bracing "
                   "shoulder, a coin pouch and a brass toll token swinging from it.",
    "tags": ["casual", "sea", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 33000)
    f = b.front
    for x in (3, 4):
        f.clear(x, 0)
    f.vline(5, 1, 11, "P1")                                              # the coat's wrap edge
    f.vline(6, 1, 11, "P3")
    sleeves(g, "P", "weave", 33001, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "P3")
    # The pole strap: over the right shoulder, down across the chest to the left hip, and across the back.
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    line(jf, 0, 0, 6, 9, "L2"), line(jf, 1, 0, 7, 9, "L3"), line(jf, 0, 1, 5, 9, "L1")
    line(jb, 7, 0, 1, 9, "L2"), line(jb, 6, 0, 0, 9, "L1")
    jacket.top.vline(0, 0, 3, "L2"), jacket.top.vline(1, 0, 3, "L3")
    jf.set(3, 4, "M3")                                                  # strap ring on the chest
    # The bracing shoulder: a stitched leather pad where the punt pole rides.
    pad = arm_blk(g, "pole_pad", "right", -2.4, (4, 1, 4), "L", 2, "leather", 33002, inflate=.12)
    for face in (pad.top,):
        face.hline(0, 3, 1, "L1"), face.hline(0, 3, 3, "L1")
    for face in pad.sides:
        face.hline(0, face.w - 1, 0, "L3")
    collar(g, "standing_collar", "P", "weave", base=2, height=2, y=-1.1)
    belt(g, "belt", 9.4, height=1)
    # The pole socket: a leather cup with an iron rim at the strap's end.
    cup = blk(g, "pole_socket", (3.0, 8.4, -2.9), (2, 3, 2), "L", 2, "leather", 33003)
    cup.top.fill("K1")
    for face in cup.sides:
        face.hline(0, 1, 0, "M3")
    pouch(g, "coin_pouch", (-2.4, 9.9, -3.0), (2, 2, 1), flap="M3")
    token = g.piece("toll_token", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(-2.4, 11.9, -3.0), motion="sway")
    solid(token, "M", "smooth", 33004, 3, edge=False)
    for face in (token.front, token.back):
        face.set(0, 0, "M4"), face.set(1, 1, "M1")
    cord = g.piece("toll_token_cord", "TORSO", (-.5, -1, -.5), (1, 1, 1), pivot=(-2.4, 12.0, -3.0), motion="sway")
    solid(cord, "L", "plain", 33005, 1, edge=False)
    for face in flaps(g, "coat_skirt", 6, "P", "weave", 33006, top=11.0, slit=True, hem="P1"):
        face.hline(0, 8, 4, "P3")
        face.set(0, 0, "P1"), face.set(8, 0, "P1")
    for name, x in (("coat_skirt_right", -5.0), ("coat_skirt_left", 4.0)):
        side = blk(g, name, (x + .5, 12.0, 0), (1, 5, 4), "P", 2, "weave", 33007)
        for face in side.sides:
            face.hline(0, face.w - 1, 4, "P1")
