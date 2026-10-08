"""Haymaker's Rolled-Sleeve Bodice: a hook-fronted bodice over a chemise rolled up to the shoulder, a sweat
cloth at the girdle and a long-toothed wooden hay rake carried over the shoulder."""
from kit import roll
from kit_female import bodice, chemise, girdle, hanging, lacing
from kit_f01 import handle
from paint import k, solid

META = {
    "name": "Haymaker's Rolled-Sleeve Bodice",
    "gender": "female",
    "description": "A hook-fronted bodice over chemise sleeves rolled up to the shoulder, a sweat cloth at the girdle and a wooden hay rake over the shoulder.",
    "tags": ["work", "casual"],
}

RAKE = (2.6, 10.2, 3.3)          # where the rake's handle rests against the small of her back
RAKE_ROT = (-6, 0, -31)
LENGTH = 16


def build(g):
    chemise(g, "S", 3, "weave", 51040, neckline="wide", sleeve_rows=(0, 3))
    roll(g, "S", 1.2, base=3)
    b = bodice(g, "P", "weave", 51041, rows=(2, 9), neckline="square", edge="A2")
    b.front.vline(3, 3, 9, "P1"), b.front.vline(4, 3, 9, "P3")       # the closed front edge
    for y in range(3, 10, 2):
        b.front.set(3, y, "M3")                                       # hooks and eyes
    for face in (b.right, b.left):
        face.vline(1, 2, 9, "P1")
    b.back.vline(3, 2, 9, "P1"), b.back.vline(4, 2, 9, "P3")
    girdle(g, "girdle", 7.8, role="L", height=1)
    # The sweat cloth tucked into the girdle at her right hip.
    cloth = hanging(g, "sweat_cloth", -2.8, 5, role="S", base=3, width=2, top=8.4, texture="weave")
    cloth.front.hline(0, 1, 0, "S4"), cloth.front.hline(0, 1, 2, "A2"), cloth.front.hline(0, 1, 4, "S2")
    # The hay rake: a long ash handle across her back, its toothed head up over the right shoulder.
    handle(g, "rake_handle", "TORSO", RAKE, LENGTH, rotation=RAKE_ROT, origin=(-.5, -LENGTH, -.5), base=3, seed=51042)
    head = g.piece("rake_head", "TORSO", (-3.5, -LENGTH - 1, -.5), (7, 1, 1), pivot=RAKE, rotation=RAKE_ROT, inflate=.05)
    solid(head, "L", "smooth", 51043, 2, edge=False)
    for f in head.sides:
        f.set(0, 0, "L1"), f.set(f.w - 1, 0, "L1")
    for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        tooth = g.piece(f"rake_tooth_{i}", "TORSO", (x - .5, -LENGTH - 3, -.5), (1, 2, 1), pivot=RAKE, rotation=RAKE_ROT)
        solid(tooth, "S", "plain", 51044 + i, 3, edge=False)
        tooth.top.fill("S4")
    for name, dx in (("rake_brace_right", -1.6), ("rake_brace_left", 1.6)):
        brace = g.piece(name, "TORSO", (dx - .5, -LENGTH + 1, -.5), (1, 1, 1), pivot=RAKE, rotation=RAKE_ROT)
        solid(brace, "L", "smooth", 51048, 2, edge=False)
    # The rake's carrying strap across the chest.
    j = g.part("jacket")
    for y in range(0, 10):
        j.front.set(round(y * 0.75), y, "L2")
    j.top.set(0, 3, "L2"), j.top.set(0, 2, "L2")
    for y in range(0, 6):
        j.back.set(7 - round(y * 0.6), y, k("L", 2))
